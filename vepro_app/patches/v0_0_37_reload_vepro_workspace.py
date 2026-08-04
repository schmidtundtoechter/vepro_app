import frappe
import json


def execute():
	json_path = frappe.get_app_path(
		"vepro_app", "vepro_app", "workspace", "vepro", "vepro.json"
	)

	with open(json_path) as f:
		doc_dict = json.load(f)

	if frappe.db.exists("Workspace", "VEPRO"):
		doc = frappe.get_doc("Workspace", "VEPRO")
		doc.update(doc_dict)
		doc.flags.ignore_permissions = True
		doc.save()
	else:
		frappe.get_doc(doc_dict).insert(ignore_permissions=True)

	frappe.db.commit()
