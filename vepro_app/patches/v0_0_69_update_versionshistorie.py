import frappe


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.69</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-10-26</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocType <code>Vertretung Freigabe</code>: Client Script löst nach dem Speichern denselben Status- und Rollenabgleich wie das tägliche Scheduler-Script aus; beide verwenden die gemeinsame API-Funktion <code>sync_vertretung_freigabe</code></td>
</tr>"""

DESCRIPTION_SECTION = """<h4>Client Script – Vertretung Freigabe</h4>
<p>Das Client Script <code>Vertretung Freigabe sofort synchronisieren</code> ruft nach dem Speichern denselben serverseitigen Status- und Rollenabgleich wie das tägliche Scheduler-Script auf. Beide verwenden die API-Funktion <code>sync_vertretung_freigabe</code>.</p>"""


def execute():
	if frappe.db.exists("Help Article", "Versionshistorie"):
		article = frappe.get_doc("Help Article", "Versionshistorie")
		if "<strong>0.0.69</strong>" not in article.content:
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
