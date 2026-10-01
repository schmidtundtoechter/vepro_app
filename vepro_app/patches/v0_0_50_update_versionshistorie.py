import frappe


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.50</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-10-01</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocType <code>Ausgangsrechnung</code>: neue Data-Felder <code>custom_abrechnungszeitraum</code> („Abrechnungszeitraum“) unter <code>custom_leistungsort</code>, <code>custom_betreff_freitext</code> („Betreff (Freitext)“) darunter und schreibgeschütztes <code>custom_rechnungsart</code> („Rechnungsart“) unter <code>amended_from</code>; Rechnungsart ist in Listenansicht, Standardfilter und globaler Suche verfügbar</td>
</tr>"""


def execute():
	if not frappe.db.exists("Help Article", "Versionshistorie"):
		return

	article = frappe.get_doc("Help Article", "Versionshistorie")
	if "<strong>0.0.50</strong>" in article.content:
		return

	article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
	article.flags.ignore_permissions = True
	article.save()