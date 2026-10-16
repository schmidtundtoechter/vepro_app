import frappe


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.62</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-10-16</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocTypes <code>Angebot</code>, <code>Auftrag</code> und <code>Ausgangsrechnung</code>: neues Link-Feld „Ansprechperson bei Vepro-East“ auf <code>User</code> direkt unter <code>amended_from</code>; im <code>Auftrag</code> ist das Feld Pflicht</td>
</tr>"""


def execute():
	if not frappe.db.exists("Help Article", "Versionshistorie"):
		return

	article = frappe.get_doc("Help Article", "Versionshistorie")
	if "<strong>0.0.62</strong>" in article.content:
		return

	article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
	article.flags.ignore_permissions = True
	article.save()
