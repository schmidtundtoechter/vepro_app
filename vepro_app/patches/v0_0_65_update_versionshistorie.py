import frappe


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.65</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-10-22</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocTypes <code>Timesheet</code>, <code>Artikel</code>, <code>Angebot</code> (Angebotsposition) und <code>Lieferantenauftrag</code>: Custom Fields <code>custom_verbundene_anfrage</code>, <code>custom_kundenname</code>, <code>custom_provision</code>, <code>custom_not_included_in_total</code>, <code>custom_gesetzter_preis</code> und <code>custom_anmerkung</code>; Timesheet-Felder <code>currency</code> und <code>exchange_rate</code> ausgeblendet und Feldreihenfolge angepasst; Beschreibungen der Angebotspositionsfelder aktualisiert</td>
</tr>"""

DESCRIPTION_SECTION = """<h4>Custom Fields – Artikel</h4>
<p>Im DocType <code>Item</code> steht das Feld <code>custom_provision</code> (Percent, „Provision“) nach <code>custom_art_des_artikels</code>.</p>
<h4>Custom Fields – Timesheet</h4>
<p>Im DocType <code>Timesheet</code> verknüpft <code>custom_verbundene_anfrage</code> (Link auf <code>Issue</code>) eine Anfrage; das schreibgeschützte Datenfeld <code>custom_kundenname</code> übernimmt den Wert aus <code>customer.customer_name</code>. Die nativen Felder <code>currency</code> und <code>exchange_rate</code> sind ausgeblendet; die Feldreihenfolge ist angepasst.</p>
<h4>Custom Fields – Angebotsposition</h4>
<p>In <code>Quotation Item</code> gibt es nach <code>item_tax_template</code> das Kontrollkästchen <code>custom_not_included_in_total</code> („nicht in Gesamtsumme aufnehmen“). Das Währungsfeld <code>custom_gesetzter_preis</code> folgt direkt darauf. Der Preis kann frei festgelegt und im Druckformat angezeigt werden; die Beschreibungen beider Felder erläutern ihre Verwendung.</p>
<h4>Custom Fields – Lieferantenauftrag</h4>
<p>Im DocType <code>Purchase Order</code> steht das Datenfeld <code>custom_anmerkung</code> („Anmerkung“) direkt nach <code>schedule_date</code>.</p>"""


def execute():
	if not frappe.db.exists("Help Article", "Versionshistorie"):
		return

	article = frappe.get_doc("Help Article", "Versionshistorie")
	if "<strong>0.0.65</strong>" not in article.content:
		if "<tbody>" not in article.content:
			frappe.throw("Versionshistorie: Changelog-Tabelle fehlt.")
		article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
		article.save(ignore_permissions=True)

	if not frappe.db.exists("Help Article", "anpassungen"):
		return

	article = frappe.get_doc("Help Article", "anpassungen")
	if "<code>custom_not_included_in_total</code>" not in article.content:
		article.content += DESCRIPTION_SECTION
		article.save(ignore_permissions=True)
