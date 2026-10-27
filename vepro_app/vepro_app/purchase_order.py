from frappe.model.document import Document


def sync_endkunde(doc: Document, method: str | None = None) -> None:
	if doc.customer:
		doc.custom_endkunde = doc.customer
