import frappe

from vepro_app.patches.v0_0_66_update_versionshistorie import DESCRIPTION_SECTION


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.67</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-10-23</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocType <code>Auftragsposition</code>: Währungsfeld <code>custom_gesetzter_preis</code> („gesetzter Preis“) nach <code>custom_not_included_in_total</code></td>
</tr>"""

DESCRIPTION = """<p>Das Währungsfeld <code>custom_gesetzter_preis</code> („gesetzter Preis“) folgt direkt darauf. Der Preis kann frei festgelegt und im Druckformat angezeigt werden.</p>"""


def execute():
	if frappe.db.exists("Help Article", "Versionshistorie"):
		article = frappe.get_doc("Help Article", "Versionshistorie")
		if "<strong>0.0.67</strong>" not in article.content:
			if "<tbody>" not in article.content:
				frappe.throw("Versionshistorie: Changelog-Tabelle fehlt.")
			article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
			article.save(ignore_permissions=True)

	if not frappe.db.exists("Help Article", "anpassungen"):
		return

	article = frappe.get_doc("Help Article", "anpassungen")
	complete_section = DESCRIPTION_SECTION + "\n" + DESCRIPTION
	if complete_section not in article.content:
		if DESCRIPTION_SECTION in article.content:
			article.content = article.content.replace(DESCRIPTION_SECTION, complete_section, 1)
		else:
			article.content += complete_section
		article.save(ignore_permissions=True)
