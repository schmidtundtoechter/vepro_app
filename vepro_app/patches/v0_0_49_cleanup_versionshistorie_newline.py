import frappe


def execute():
	if not frappe.db.exists("Help Article", "Versionshistorie"):
		return

	article = frappe.get_doc("Help Article", "Versionshistorie")
	if "\\n" not in article.content:
		return

	article.content = article.content.replace("\\n", "\n")
	article.flags.ignore_permissions = True
	article.save()