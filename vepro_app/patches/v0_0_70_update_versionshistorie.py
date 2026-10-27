import frappe


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.70</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-10-27</td>
<td style="border:1px solid #d1d8dd;padding:6px;">Bestellung (<code>Purchase Order</code>): Endkundenfelder <code>custom_endkunde</code> und <code>custom_name_endkunde</code> in die App aufgenommen; automatischer Abgleich mit dem Drop-Ship-Kunden im Formular und beim serverseitigen Speichern; ohne Drop-Ship-Kunden bleibt die manuelle Auswahl erhalten. Vollständiger Kundenname wird automatisch übernommen. Beide Server Scripts sind dem Modul <code>vepro_app</code> zugeordnet.</td>
</tr>"""

DESCRIPTION_SECTION = """<h4>Bestellung – Endkunde</h4>
<p>Das bearbeitbare Link-Feld <code>custom_endkunde</code> (Endkunde) steht direkt nach <code>custom_ansprechperson_bei_vepro_east</code>. Ist <code>customer</code> im Tab „Drop Ship“ gesetzt, wird exakt dieser Kunde im Formular und beim serverseitigen Speichern übernommen. Ohne Drop-Ship-Kunden bleibt der Endkunde unverändert und manuell auswählbar. Bereits gebuchte oder stornierte Bestellungen werden beim Öffnen nicht verändert.</p>
<p>Direkt danach steht <code>custom_name_endkunde</code> (Vollständiger Name des Endkunden), ein schreibgeschütztes Datenfeld mit automatischer Übernahme aus <code>custom_endkunde.customer_name</code>. Beide Felder sind als Fixtures mit Modulzuordnung <code>vepro_app</code> enthalten.</p>
<h4>Server Scripts – Modulzuordnung</h4>
<p>Die Server Scripts <code>Kontakt Kunde Sync</code> und <code>Vertretung Freigabe täglich</code> zeigen im Feld „Modul (für Export)“ den Wert <code>vepro_app</code>.</p>"""


def execute():
	if frappe.db.exists("Help Article", "Versionshistorie"):
		article = frappe.get_doc("Help Article", "Versionshistorie")
		if "<strong>0.0.70</strong>" not in article.content:
			if "<tbody>" not in article.content:
				frappe.throw("Versionshistorie: Changelog-Tabelle fehlt.")
			article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
			article.save(ignore_permissions=True)

	if not frappe.db.exists("Help Article", "anpassungen"):
		return

	article = frappe.get_doc("Help Article", "anpassungen")
	if DESCRIPTION_SECTION not in article.content:
		article.content += DESCRIPTION_SECTION
		article.save(ignore_permissions=True)
