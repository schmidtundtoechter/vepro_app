import frappe


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.64</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-10-19</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocTypes <code>Angebot</code>, <code>Auftrag</code> und <code>Ausgangsrechnung</code>: neues optionales Datenfeld <code>custom_beschreibung</code> („Beschreibung“) direkt nach <code>custom_ansprechperson_bei_vepro_east</code>; beide Felder sind im Fixture-Export registriert</td>
</tr>"""

DESCRIPTION_SECTION = """<h4>Custom Fields – Angebot, Auftrag und Ausgangsrechnung</h4>
<p>In <code>Quotation</code>, <code>Sales Order</code> und <code>Sales Invoice</code> steht das optionale Datenfeld <code>custom_beschreibung</code> („Beschreibung“, Typ <code>Data</code>) direkt nach <code>custom_ansprechperson_bei_vepro_east</code>.</p>"""


def execute():
	article = frappe.get_doc("Help Article", "Versionshistorie")
	if "<strong>0.0.64</strong>" not in article.content:
		if "<tbody>" not in article.content:
			frappe.throw("Versionshistorie: Changelog-Tabelle fehlt.")
		article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
		article.save(ignore_permissions=True)

	article = frappe.get_doc("Help Article", "anpassungen")
	if "<code>custom_beschreibung</code>" not in article.content:
		article.content += DESCRIPTION_SECTION
		article.save(ignore_permissions=True)
