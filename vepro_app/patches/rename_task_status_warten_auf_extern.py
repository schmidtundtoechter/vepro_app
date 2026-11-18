import frappe


def execute():
	# Preserve existing tasks when the fixture replaces the old status option.
	# Avoid save hooks that could change progress, assignments or project totals.
	frappe.db.set_value(
		"Task",
		{"status": "Warten auf Kunde"},
		"status",
		"Warten auf Extern",
		update_modified=False,
	)
