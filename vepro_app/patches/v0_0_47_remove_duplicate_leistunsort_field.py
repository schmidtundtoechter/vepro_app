import frappe


DOCTYPE_NAMES = ("Quotation", "Sales Order", "Sales Invoice")

VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.47</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-09-15</td>
<td style="border:1px solid #d1d8dd;padding:6px;">Doppelte Felder bereinigt: <code>custom_leistunsort</code> entfernt und vorhandene Werte nach <code>custom_leistungsort</code> übernommen</td>
</tr>"""


def execute():
	for doctype in DOCTYPE_NAMES:
		wrong_name = f"{doctype}-custom_leistunsort"

		if not frappe.db.exists("Custom Field", wrong_name):
			continue

		frappe.db.sql(
			f"""
			UPDATE `tab{doctype}`
			SET `custom_leistungsort` = `custom_leistunsort`
			WHERE (`custom_leistungsort` IS NULL OR `custom_leistungsort` = '')
				AND `custom_leistunsort` IS NOT NULL
				AND `custom_leistunsort` != ''
			"""
		)
		frappe.delete_doc("Custom Field", wrong_name, force=True, ignore_permissions=True)
		frappe.clear_cache(doctype=doctype)
		frappe.db.updatedb(doctype)

	update_versionshistorie()


def update_versionshistorie():
	if not frappe.db.exists("Help Article", "Versionshistorie"):
		return

	article = frappe.get_doc("Help Article", "Versionshistorie")
	if "<strong>0.0.47</strong>" in article.content:
		return

	article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
	article.flags.ignore_permissions = True
	article.save()