import frappe


def execute():
	# total_time_spent starts at 0 for all existing enrollments;
	# no historical session data exists to backfill.
	frappe.db.sql(
		"UPDATE `tabLMS Enrollment` SET total_time_spent = 0 WHERE total_time_spent IS NULL"
	)
