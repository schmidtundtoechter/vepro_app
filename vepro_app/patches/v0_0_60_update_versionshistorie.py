import frappe


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.60</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-10-15</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocTypes <code>Angebot</code>, <code>Auftrag</code>, <code>Ausgangsrechnung</code> und <code>Lieferschein</code>: <code>customer_address</code> ist ein Pflichtfeld</td>
</tr>"""


def execute():
	if not frappe.db.exists("Help Article", "Versionshistorie"):
		return

	article = frappe.get_doc("Help Article", "Versionshistorie")
	if "<strong>0.0.60</strong>" in article.content:
		return

	article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
	article.flags.ignore_permissions = True
	article.save()
