import frappe


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.74</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-11-18</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocType <code>Dunning</code>: neues Datumsfeld <code>custom_stichtag</code> („Fälligkeits-Datum“) nach <code>customer_name</code></td>
</tr>"""


def execute():
	if not frappe.db.exists("Help Article", "Versionshistorie"):
		return

	article = frappe.get_doc("Help Article", "Versionshistorie")
	if "<strong>0.0.74</strong>" in article.content:
		return
	if "<tbody>" not in article.content:
		frappe.throw("Versionshistorie: Changelog-Tabelle fehlt.")

	article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
	article.save(ignore_permissions=True)
