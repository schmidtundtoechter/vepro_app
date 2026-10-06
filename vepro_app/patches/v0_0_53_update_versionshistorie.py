import frappe


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.53</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-10-05</td>
<td style="border:1px solid #d1d8dd;padding:6px;">Neuer DocType <code>Vertretung Freigabe</code> mit den Feldern <code>Vertreter</code> (Link auf User), <code>Vertretung aktiv</code>, <code>Von</code> und <code>Bis</code></td>
</tr>"""


def execute():
	if not frappe.db.exists("Help Article", "Versionshistorie"):
		return

	article = frappe.get_doc("Help Article", "Versionshistorie")
	if "<strong>0.0.53</strong>" in article.content:
		return

	article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
	article.flags.ignore_permissions = True
	article.save()