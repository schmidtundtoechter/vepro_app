import frappe


ROLE_NAME = "Vepro Vertretung Freigabe"


@frappe.whitelist()
def set_vertretung_freigabe_role(user: str, enabled: bool) -> None:
	frappe.only_for("System Manager")
	if not frappe.db.exists("User", user):
		return

	filters = {
		"parent": user,
		"parenttype": "User",
		"parentfield": "roles",
		"role": ROLE_NAME,
	}

	if enabled:
		if not frappe.db.exists("Has Role", filters):
			frappe.get_doc({"doctype": "Has Role", **filters}).insert(ignore_permissions=True)
	else:
		frappe.db.delete("Has Role", filters)

	frappe.clear_cache(user=user)