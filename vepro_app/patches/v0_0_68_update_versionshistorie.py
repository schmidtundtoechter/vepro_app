import frappe


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.68</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-10-26</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocTypes <code>Bestellung</code> (<code>Purchase Order</code>) und <code>Lieferschein</code> (<code>Delivery Note</code>): Pflichtfeld <code>custom_ansprechperson_bei_vepro_east</code> (Link auf <code>User</code>) nach <code>has_unit_price_items</code> bzw. <code>is_return</code>; alle fünf Felder sind Pflichtfelder und im Fixture-Export registriert</td>
</tr>"""

DESCRIPTION_SECTION = """<h4>Custom Fields – Bestellung und Lieferschein</h4>
<p>In <code>Purchase Order</code> und <code>Delivery Note</code> ist das Pflichtfeld <code>custom_ansprechperson_bei_vepro_east</code> („Ansprechperson bei Vepro-East“, Link auf <code>User</code>) nach <code>has_unit_price_items</code> bzw. <code>is_return</code> platziert. Das Feld ist auch in <code>Quotation</code>, <code>Sales Order</code> und <code>Sales Invoice</code> ein Pflichtfeld.</p>"""


def execute():
	if frappe.db.exists("Help Article", "Versionshistorie"):
		article = frappe.get_doc("Help Article", "Versionshistorie")
		if "<strong>0.0.68</strong>" not in article.content:
			if "<tbody>" not in article.content:
				frappe.throw("Versionshistorie: Changelog-Tabelle fehlt.")
			article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
			article.save(ignore_permissions=True)

	if not frappe.db.exists("Help Article", "anpassungen"):
		return

	article = frappe.get_doc("Help Article", "anpassungen")
	if DESCRIPTION_SECTION not in article.content:
		article.content += DESCRIPTION_SECTION
		article.save(ignore_permissions=True)
