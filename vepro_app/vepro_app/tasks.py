import frappe


def sync_kontakt_kunde():
	"""
	Läuft täglich um 3 Uhr nachts.
	Durchsucht alle Kontakte, bei denen custom_kunde leer ist.
	Findet einen verknüpften Kunden in der Dynamic-Links-Tabelle (tabDynamic Link)
	und trägt den ersten gefundenen Kunden in custom_kunde ein.
	"""
	kontakte = frappe.get_all(
		"Contact",
		filters={"custom_kunde": ["is", "not set"]},
		fields=["name"],
	)

	updated = 0
	for row in kontakte:
		# Erster verknüpfter Kunde aus der Dynamic-Links-Tabelle
		linked = frappe.db.get_value(
			"Dynamic Link",
			filters={
				"parenttype": "Contact",
				"parent": row["name"],
				"link_doctype": "Customer",
			},
			fieldname="link_name",
			order_by="idx asc",
		)

		if linked:
			frappe.db.set_value("Contact", row["name"], "custom_kunde", linked)
			updated += 1

	frappe.db.commit()
	frappe.logger().info(
		f"sync_kontakt_kunde: {updated} von {len(kontakte)} Kontakten aktualisiert."
	)
