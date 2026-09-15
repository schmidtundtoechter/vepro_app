import frappe
from frappe.custom.doctype.custom_field.custom_field import rename_fieldname


FIELD_DEFAULTS = {
	"Quotation": "Remote und vor Ort. Für den Einsatz vor Ort kommen die o.g. Nebenkosten zum Tragen.",
	"Sales Order": None,
	"Sales Invoice": None,
}

VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.46</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-09-15</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocTypes <code>Angebot</code>, <code>Auftrag</code> und <code>Ausgangsrechnung</code>: Custom Field <code>custom_vor_ort</code> in <code>custom_leistungsort</code> („Leistungsort“) umbenannt; die Logik bleibt unverändert</td>
</tr>"""


def execute():
	for doctype, default in FIELD_DEFAULTS.items():
		old_name = f"{doctype}-custom_vor_ort"
		new_name = f"{doctype}-custom_leistungsort"

		if frappe.db.exists("Custom Field", old_name) and not frappe.db.exists("Custom Field", new_name):
			rename_fieldname(old_name, "custom_leistungsort")
			frappe.rename_doc("Custom Field", old_name, new_name, force=True)

		if frappe.db.exists("Custom Field", new_name):
			frappe.db.set_value(
				"Custom Field",
				new_name,
				{
					"default": default,
					"description": None,
					"fieldtype": "Data",
					"label": "Leistungsort",
				},
				update_modified=False,
			)
			frappe.clear_cache(doctype=doctype)
			frappe.db.updatedb(doctype)

	update_versionshistorie()


def update_versionshistorie():
	if not frappe.db.exists("Help Article", "Versionshistorie"):
		return

	article = frappe.get_doc("Help Article", "Versionshistorie")
	if "<strong>0.0.46</strong>" in article.content:
		return

	article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
	article.flags.ignore_permissions = True
	article.save()