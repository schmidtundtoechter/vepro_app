import frappe


VERSION_ROWS = """<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.49</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-09-21</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocType <code>Auftrag</code>: neues Custom Field <code>custom_zahlungsbedingung</code> (Small Text, „Zahlungsbedingung“) direkt unter <code>payment_schedule</code>; wird im Druckformat bei leerem Wert ausgeblendet</td>
</tr>
<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.48</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-09-21</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocType <code>Angebot</code>: neues Custom Field <code>custom_zahlungsbedingung</code> (Small Text, „Zahlungsbedingung“) direkt unter <code>payment_schedule</code>; wird im Druckformat bei leerem Wert ausgeblendet</td>
</tr>
<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.47</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-09-15</td>
<td style="border:1px solid #d1d8dd;padding:6px;">Doppelte Felder bereinigt: <code>custom_leistunsort</code> entfernt und vorhandene Werte nach <code>custom_leistungsort</code> übernommen</td>
</tr>
<tr>
<td style="border:1px solid #d1d8dd;padding:6px;"><strong>0.0.46</strong></td>
<td style="border:1px solid #d1d8dd;padding:6px;">2026-09-15</td>
<td style="border:1px solid #d1d8dd;padding:6px;">DocTypes <code>Angebot</code>, <code>Auftrag</code> und <code>Ausgangsrechnung</code>: Custom Field <code>custom_vor_ort</code> in <code>custom_leistungsort</code> („Leistungsort“) umbenannt; die Logik bleibt unverändert</td>
</tr>"""


def execute():
	if not frappe.db.exists("Help Article", "Versionshistorie"):
		return

	article = frappe.get_doc("Help Article", "Versionshistorie")
	if "<strong>0.0.49</strong>" in article.content:
		return

	article.content = article.content.replace("<tbody>", f"<tbody>\n{VERSION_ROWS}\n", 1)
	article.flags.ignore_permissions = True
	article.save()