import frappe


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.71</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-11-09</td>
<td style="border:1px solid #d1d8dd;padding:6px;">Neuer app-eigener DocType <code>Autoreservierung</code> für Firmenwagenreservierungen mit Kalender- und Gantt-Ansicht</td>
</tr>"""

DESCRIPTION_SECTION = """<h4>DocType – Autoreservierung</h4>
<p>Der app-eigene DocType <code>Autoreservierung</code> verwaltet Firmenwagenreservierungen mit reservierendem Benutzer, Beginn und Ende, Fahrzeug, Status und Fahrtzweck. Die Kalender- und Gantt-Ansichten verwenden Beginn und Ende als Zeitraum und zeigen den reservierenden Benutzer als Titel.</p>"""


def execute():
	if frappe.db.exists("Help Article", "Versionshistorie"):
		article = frappe.get_doc("Help Article", "Versionshistorie")
		if "<strong>0.0.71</strong>" not in article.content:
			if "<tbody>" not in article.content:
				frappe.throw("Versionshistorie: Changelog-Tabelle fehlt.")
			article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
			article.save(ignore_permissions=True)

	if not frappe.db.exists("Help Article", "anpassungen"):
		return

	article = frappe.get_doc("Help Article", "anpassungen")
	if "<h4>DocType – Autoreservierung</h4>" not in article.content:
		article.content += DESCRIPTION_SECTION
		article.save(ignore_permissions=True)
