import frappe


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.51</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-10-01</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocType <code>Ausgangsrechnung</code>: natives Feld <code>payment_terms_template</code> („Payment Terms Template“) erhält <code>no_copy: 0</code> („Keine Kopie“ ist deaktiviert)</td>
</tr>"""


def execute():
	if not frappe.db.exists("Help Article", "Versionshistorie"):
		return

	article = frappe.get_doc("Help Article", "Versionshistorie")
	if "<strong>0.0.51</strong>" in article.content:
		return

	article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
	article.flags.ignore_permissions = True
	article.save()