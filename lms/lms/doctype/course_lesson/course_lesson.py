# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import json

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.realtime import get_website_room
from frappe.utils.telemetry import capture

from lms.lms.utils import get_course_progress

from ...md import find_macros


class CourseLesson(Document):
	def on_update(self):
		self.validate_quiz_id()

	def validate_quiz_id(self):
		if self.quiz_id and not frappe.db.exists("LMS Quiz", self.quiz_id):
			frappe.throw(_("Invalid Quiz ID"))

		if self.content:
			self.save_lesson_details_in_quiz(self.content)

		if self.instructor_content:
			self.save_lesson_details_in_quiz(self.instructor_content)

	def save_lesson_details_in_quiz(self, content):
		content = json.loads(self.content)
		for block in content.get("blocks"):
			if block.get("type") == "quiz":
				quiz = block.get("data").get("quiz")
				if not frappe.db.exists("LMS Quiz", quiz):
					frappe.throw(_("Invalid Quiz ID in content"))
				frappe.db.set_value(
					"LMS Quiz",
					quiz,
					{
						"course": self.course,
						"lesson": self.name,
					},
				)


@frappe.whitelist()
def save_progress(lesson, course, scorm_details=None, member_override=None):
	"""
	Note: Pass the argument scorm_details as a dict if it is SCORM related save_progress.
	Pass member_override to act on behalf of a specific member (e.g. when called from grading context).
	"""
	member = member_override or frappe.session.user
	membership = frappe.db.exists("LMS Enrollment", {"course": course, "member": member})
	if not membership:
		return 0

	frappe.db.set_value("LMS Enrollment", membership, "current_lesson", lesson)
	progress_already_exists = frappe.db.exists(
		"LMS Course Progress", {"lesson": lesson, "member": member}
	)
	lesson_already_completed = frappe.db.exists(
		"LMS Course Progress",
		{"lesson": lesson, "member": member, "status": "Complete"},
	)

	quiz_completed = get_quiz_progress(lesson, member=member)
	assignment_completed = get_assignment_progress(lesson, member=member)

	if scorm_details:
		scorm_details = frappe._dict(**scorm_details)

	if not progress_already_exists and quiz_completed and assignment_completed and not scorm_details:
		frappe.get_doc(
			{
				"doctype": "LMS Course Progress",
				"lesson": lesson,
				"status": "Complete",
				"member": member,
			}
		).save(ignore_permissions=True)
	elif scorm_details and not lesson_already_completed and not progress_already_exists:
		# Create new SCORM progress
		frappe.get_doc(
			{
				"doctype": "LMS Course Progress",
				"lesson": lesson,
				"status": "Complete" if scorm_details.is_complete else "Partially Complete",
				"member": member,
				"scorm_content": "" if scorm_details.is_complete else scorm_details.scorm_content,
			}
		).save(ignore_permissions=True)
	elif scorm_details and not lesson_already_completed and progress_already_exists:
		# Update Existing SCORM Progress
		frappe.db.set_value(
			"LMS Course Progress",
			progress_already_exists,
			{
				"lesson": lesson,
				"status": "Complete" if scorm_details.is_complete else "Partially Complete",
				"member": member,
				"scorm_content": "" if scorm_details.is_complete else scorm_details.scorm_content,
			},
		)

	is_complete = bool(
		frappe.db.exists("LMS Course Progress", {"lesson": lesson, "member": member, "status": "Complete"})
	)
	progress = get_course_progress(course, member)
	capture_progress_for_analytics(progress, course)

	# Had to get doc, as on_change doesn't trigger when you use set_value. The trigger is necessary for badge to get assigned.
	enrollment = frappe.get_doc("LMS Enrollment", membership)
	enrollment.progress = progress
	enrollment.save()
	enrollment.run_method("on_change")

	frappe.publish_realtime(
		event="update_lesson_progress",
		room=get_website_room(),
		message={"course": course, "lesson": lesson, "progress": progress, "is_complete": is_complete},
		after_commit=True,
	)

	return progress


def reset_lesson_progress(lesson, member, course):
	"""Deletes the Complete progress record for a lesson and recalculates enrollment progress."""
	existing = frappe.db.exists(
		"LMS Course Progress",
		{"lesson": lesson, "member": member, "status": "Complete"},
	)
	if existing:
		frappe.delete_doc("LMS Course Progress", existing, ignore_permissions=True)

	membership = frappe.db.get_value(
		"LMS Enrollment", {"course": course, "member": member}, "name"
	)
	if not membership:
		return

	progress = get_course_progress(course, member)
	enrollment = frappe.get_doc("LMS Enrollment", membership)
	enrollment.progress = progress
	enrollment.save()
	enrollment.run_method("on_change")

	frappe.publish_realtime(
		event="update_lesson_progress",
		room=get_website_room(),
		message={"course": course, "lesson": lesson, "progress": progress, "is_complete": False},
		after_commit=True,
	)


def capture_progress_for_analytics(progress, course):
	if progress in [25, 50, 75, 100]:
		capture("course_progress", "lms", properties={"course": course, "progress": progress})


def get_quiz_progress(lesson, member=None):
	if not member:
		member = frappe.session.user

	lesson_details = frappe.db.get_value("Course Lesson", lesson, ["body", "content"], as_dict=1)
	quizzes = []

	if lesson_details.content:
		content = json.loads(lesson_details.content)

		for block in content.get("blocks"):
			if block.get("type") == "quiz":
				quizzes.append(block.get("data").get("quiz"))
			if block.get("type") == "upload":
				quizzes_in_video = block.get("data").get("quizzes")
				if quizzes_in_video and len(quizzes_in_video) > 0:
					for row in quizzes_in_video:
						quizzes.append(row.get("quiz"))

	elif lesson_details.body:
		macros = find_macros(lesson_details.body)
		quizzes = [value for name, value in macros if name == "Quiz"]

	for quiz in quizzes:
		question_types = frappe.get_all(
			"LMS Quiz Question", filters={"parent": quiz}, pluck="type"
		)
		is_open_ended = bool(question_types) and all(t == "Open Ended" for t in question_types)

		if is_open_ended:
			if not frappe.db.exists(
				"LMS Quiz Submission",
				{"quiz": quiz, "member": member, "status": "Pass"},
			):
				return False
		else:
			passing_percentage = frappe.db.get_value("LMS Quiz", quiz, "passing_percentage")
			if not frappe.db.exists(
				"LMS Quiz Submission",
				{
					"quiz": quiz,
					"member": member,
					"percentage": [">=", passing_percentage],
				},
			):
				return False
	return True


def get_assignment_progress(lesson, member=None):
	if not member:
		member = frappe.session.user

	member_sector = frappe.db.get_value("User", member, "sector")

	lesson_details = frappe.db.get_value("Course Lesson", lesson, ["body", "content"], as_dict=1)
	assignments = []

	if lesson_details.content:
		content = json.loads(lesson_details.content)

		for block in content.get("blocks"):
			if block.get("type") == "assignment":
				assignment_name = block.get("data").get("assignment")

				# Mirror the sector filter applied by Lesson.vue: renderEditor().
				# If the member has a sector set, skip assignments tagged with a
				# different sector — the student was never shown those blocks.
				if member_sector:
					assignment_industry = frappe.db.get_value(
						"LMS Assignment", assignment_name, "industry"
					)
					if assignment_industry and assignment_industry != member_sector:
						continue

				assignments.append(assignment_name)

	elif lesson_details.body:
		macros = find_macros(lesson_details.body)
		assignments = [value for name, value in macros if name == "Assignment"]

	for assignment in assignments:
		submission = frappe.db.get_value(
			"LMS Assignment Submission",
			{"assignment": assignment, "member": member},
			["status", "score"],
			as_dict=True,
		)

		if not submission:
			return False

		assignment_details = frappe.db.get_value(
			"LMS Assignment", assignment, ["grade_assignment", "passing_score"], as_dict=True
		)

		# Text type with grade_assignment=0: any submission suffices
		if assignment_details.get("grade_assignment") == 0:
			continue

		# All other cases: must be Pass or Not Applicable
		if submission.status not in ["Pass", "Not Applicable"]:
			return False

		# Passing score gate (if configured)
		if assignment_details.get("passing_score") and submission.score is not None:
			if submission.score < assignment_details.passing_score:
				return False

	return True


@frappe.whitelist()
def get_lesson_info(chapter):
	return frappe.db.get_value("Course Chapter", chapter, "course")
