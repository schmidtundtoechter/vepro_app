import frappe


VERSION_ROW = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.77</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-11-25</td>
<td style="border:1px solid #d1d8dd;padding:6px;">Anfrage: Produktkategorie, Checkfelder für DLAS und Bereitschaft sowie Lösungsfeld ergänzt; Priorität standardmäßig „Mittel“, weitere Felder ausgeblendet. Telefonnummer: Synchronisierungsausschluss und Schutz von mit Anfragen verknüpften Nummern vor dem Löschen.</td>
</tr>"""


def execute():
	if not frappe.db.exists("Help Article", "Versionshistorie"):
		return

	article = frappe.get_doc("Help Article", "Versionshistorie")
	if "<strong>0.0.77</strong>" in article.content:
		return
	if "<tbody>" not in article.content:
		frappe.throw("Versionshistorie: Changelog-Tabelle fehlt.")

	article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROW}\n", 1)
	article.save(ignore_permissions=True)
