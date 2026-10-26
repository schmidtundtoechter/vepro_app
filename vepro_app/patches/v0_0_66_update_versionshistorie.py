import frappe


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.66</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-10-23</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocType <code>Auftragsposition</code>: neues Kontrollkästchen <code>custom_not_included_in_total</code> („nicht in Gesamtsumme aufnehmen“) nach <code>net_amount</code></td>
</tr>"""

DESCRIPTION_SECTION = """<h4>Custom Fields – Auftragsposition</h4>
<p>In <code>Sales Order Item</code> steht nach <code>net_amount</code> das Kontrollkästchen <code>custom_not_included_in_total</code> („nicht in Gesamtsumme aufnehmen“).</p>"""


def execute():
	if frappe.db.exists("Help Article", "Versionshistorie"):
		article = frappe.get_doc("Help Article", "Versionshistorie")
		if "<strong>0.0.66</strong>" not in article.content:
			if "<tbody>" not in article.content:
				frappe.throw("Versionshistorie: Changelog-Tabelle fehlt.")
			article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
			article.save(ignore_permissions=True)

	if not frappe.db.exists("Help Article", "anpassungen"):
		return

	article = frappe.get_doc("Help Article", "anpassungen")
	if "<code>Sales Order Item</code>" not in article.content:
		article.content += DESCRIPTION_SECTION
		article.save(ignore_permissions=True)
