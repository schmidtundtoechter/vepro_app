import frappe


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.58</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-10-07</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocType <code>Vertretung Freigabe</code>: Vertreter und Von sind Pflichtfelder; Erklärungstext rechts neben Vertreter; leeres Bis erlaubt unbefristete Aktivierung</td>
</tr>"""


def execute():
	if not frappe.db.exists("Help Article", "Versionshistorie"):
		return

	article = frappe.get_doc("Help Article", "Versionshistorie")
	if "<strong>0.0.58</strong>" in article.content:
		return

	article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
	article.flags.ignore_permissions = True
	article.save()