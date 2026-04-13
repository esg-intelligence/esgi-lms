# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
from frappe.model.document import Document
from frappe.utils import validate_url


class LMSAssignmentSubmission(Document):
	def before_save(self):
		self.handle_resubmission()

	def validate(self):
		self.validate_duplicates()
		self.validate_url()
		self.validate_status()

	def on_update(self):
		self.validate_private_attachments()

	def handle_resubmission(self):
		"""Reset status to Not Graded when a student re-submits after receiving a Fail.
		For Post-Test assignments, block re-submission after 2 failed attempts.
		"""
		if not self.is_new():
			doc_before_save = self.get_doc_before_save()
			if (
				frappe.session.user == self.member
				and doc_before_save.status == "Fail"
			):
				category = frappe.db.get_value(
					"LMS Assignment", self.assignment, "category"
				)
				if category == "Post-Test" and (doc_before_save.fail_count or 0) >= 2:
					frappe.throw(
						_("You have reached the maximum number of attempts for this Post-Test assignment.")
					)
				self.status = "Not Graded"

	def validate_duplicates(self):
		if frappe.db.exists(
			"LMS Assignment Submission",
			{"assignment": self.assignment, "member": self.member, "name": ["!=", self.name]},
		):
			lesson_title = frappe.db.get_value("Course Lesson", self.lesson, "title")
			frappe.throw(
				_("Assignment for Lesson {0} by {1} already exists.").format(lesson_title, self.member_name)
			)

	def validate_url(self):
		if self.type == "URL" and not validate_url(self.answer):
			frappe.throw(_("Please enter a valid URL."))

	def validate_status(self):
		if not self.is_new():
			doc_before_save = self.get_doc_before_save()
			status_changed = doc_before_save.status != self.status
			comments_changed = doc_before_save.comments != self.comments
			is_evaluator_action = frappe.session.user != self.member

			if (status_changed or comments_changed) and is_evaluator_action:
				self.trigger_update_notification()

			if status_changed and is_evaluator_action and self.lesson:
				chapter = frappe.db.get_value("Course Lesson", self.lesson, "chapter")
				course = frappe.db.get_value("Course Chapter", chapter, "course") if chapter else None
				if course:
					if self.status == "Pass":
						from lms.lms.doctype.course_lesson.course_lesson import save_progress
						save_progress(self.lesson, course, member_override=self.member)
					elif self.status == "Fail":
						self.fail_count = (self.fail_count or 0) + 1
						from lms.lms.doctype.course_lesson.course_lesson import reset_lesson_progress
						reset_lesson_progress(self.lesson, self.member, course)

	def validate_private_attachments(self):
		if self.type == "Text":
			from bs4 import BeautifulSoup

			soup = BeautifulSoup(self.answer, "html.parser")
			images = soup.find_all("img")
			self.attach_images_to_document(images)

	def attach_images_to_document(self, images):
		for img in images:
			src = img.get("src", "")
			if src.startswith("/private/files/"):
				file_name = frappe.db.get_value("File", {"file_url": src}, "name")
				if file_name:
					frappe.db.set_value(
						"File",
						file_name,
						{
							"attached_to_doctype": self.doctype,
							"attached_to_name": self.name,
							"attached_to_field": "answer",
						},
					)

	def trigger_update_notification(self):
		notification = frappe._dict(
			{
				"subject": _("There has been an update on your submission for assignment {0}").format(
					self.assignment_title
				),
				"email_content": self.comments,
				"document_type": self.doctype,
				"document_name": self.name,
				"for_user": self.owner,
				"from_user": self.evaluator,
				"type": "Alert",
				"link": f"/assignment-submission/{self.assignment}/{self.name}",
			}
		)
		make_notification_logs(notification, [self.member])


@frappe.whitelist()
def upload_assignment(
	assignment_attachment=None,
	answer=None,
	assignment=None,
	lesson=None,
	status="Not Graded",
	comments=None,
	submission=None,
):
	if frappe.session.user == "Guest":
		return

	assignment_details = frappe.db.get_value(
		"LMS Assignment", assignment, ["type", "grade_assignment"], as_dict=1
	)
	assignment_type = assignment_details.type

	if assignment_type in ["URL", "Text"] and not answer:
		frappe.throw(_("Please enter the URL for assignment submission."))

	if assignment_type == "File" and not assignment_attachment:
		frappe.throw(_("Please upload the assignment file."))

	if assignment_type == "URL" and not validate_url(answer):
		frappe.throw(_("Please enter a valid URL."))

	if submission:
		doc = frappe.get_doc("LMS Assignment Submission", submission)
	else:
		doc = frappe.get_doc(
			{
				"doctype": "LMS Assignment Submission",
				"assignment": assignment,
				"lesson": lesson,
				"member": frappe.session.user,
				"type": assignment_type,
			}
		)

	doc.update(
		{
			"assignment_attachment": assignment_attachment,
			"status": "Not Applicable"
			if assignment_type == "Text" and not assignment_details.grade_assignment
			else status,
			"comments": comments,
			"answer": answer,
		}
	)
	doc.save(ignore_permissions=True)
	return doc.name


@frappe.whitelist()
def get_assignment(lesson):
	assignment = frappe.db.get_value(
		"LMS Assignment Submission",
		{"lesson": lesson, "member": frappe.session.user},
		["name", "lesson", "member", "assignment_attachment", "comments", "status"],
		as_dict=True,
	)
	assignment.file_name = frappe.db.get_value(
		"File", {"file_url": assignment.assignment_attachment}, "file_name"
	)
	return assignment


@frappe.whitelist()
def grade_assignment(name, result, comments):
	doc = frappe.get_doc("LMS Assignment Submission", name)
	doc.status = result
	doc.comments = comments
	doc.save(ignore_permissions=True)


@frappe.whitelist()
def reset_post_test_submission(assignment, lesson, course):
	"""Allow a student who has exhausted Post-Test attempts to start over.
	Deletes the submission record so the student can re-submit fresh,
	and resets lesson progress.
	"""
	submission = frappe.db.get_value(
		"LMS Assignment Submission",
		{"assignment": assignment, "member": frappe.session.user},
		"name",
	)
	if not submission:
		frappe.throw(_("No submission found."))

	category = frappe.db.get_value("LMS Assignment", assignment, "category")
	if category != "Post-Test":
		frappe.throw(_("Only Post-Test assignments can be reset."))

	fail_count = frappe.db.get_value("LMS Assignment Submission", submission, "fail_count")
	if (fail_count or 0) < 2:
		frappe.throw(_("Maximum attempts have not been reached yet."))

	frappe.delete_doc("LMS Assignment Submission", submission, ignore_permissions=True)

	from lms.lms.doctype.course_lesson.course_lesson import reset_lesson_progress
	reset_lesson_progress(lesson, frappe.session.user, course)
