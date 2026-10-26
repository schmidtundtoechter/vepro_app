import frappe


ROLE_NAME = "Vepro Vertretung Freigabe"
ACTIVE_STATUS = "Vertretung ist aktiv"
INACTIVE_STATUS = "Vertretung nicht aktiv"


@frappe.whitelist()
def sync_vertretung_freigabe() -> None:
	frappe.only_for("System Manager")
	today = frappe.utils.getdate(frappe.utils.today())

	assignments = frappe.get_all(
		"Vertretung Freigabe",
		fields=["name", "vertreter", "vertretung_aktiv", "von", "bis", "status"],
	)
	active_users = set()

	for assignment in assignments:
		is_active = (
			assignment.vertretung_aktiv
			and assignment.vertreter
			and assignment.von
			and frappe.utils.getdate(assignment.von) <= today
			and (not assignment.bis or frappe.utils.getdate(assignment.bis) >= today)
		)
		status = ACTIVE_STATUS if is_active else INACTIVE_STATUS
		if assignment.status != status:
			frappe.db.set_value("Vertretung Freigabe", assignment.name, "status", status)
		if is_active:
			active_users.add(assignment.vertreter)

	role_holders = frappe.get_all(
		"Has Role",
		filters={"parenttype": "User", "parentfield": "roles", "role": ROLE_NAME},
		pluck="parent",
	)

	for user in active_users:
		set_vertretung_freigabe_role(user=user, enabled=True)

	for user in set(role_holders) - active_users:
		set_vertretung_freigabe_role(user=user, enabled=False)


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