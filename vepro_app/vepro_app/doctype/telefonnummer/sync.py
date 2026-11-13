import frappe

from vepro_app.vepro_app.doctype.telefonnummer.telefonnummer import normalize_phone_number

PAGE_SIZE = 500


def _get_all_rows(doctype, fields, filters=None, order_by="name asc"):
	start = 0
	while True:
		rows = frappe.get_all(
			doctype,
			fields=fields,
			filters=filters,
			order_by=order_by,
			limit_start=start,
			limit_page_length=PAGE_SIZE,
		)
		yield from rows
		if len(rows) < PAGE_SIZE:
			break
		start += len(rows)


def _add_phone(phones, contact, number, phone_type, primary, contact_details):
	phone_number = (number or "").strip()
	search_number = normalize_phone_number(phone_number)
	if not search_number:
		return

	key = (contact, search_number)
	existing = phones.get(key)
	if existing:
		existing["primaernummer"] = int(bool(existing["primaernummer"] or primary))
		if phone_type == "Mobiltelefon":
			existing["typ"] = phone_type
		existing.update(contact_details)
		return

	phones[key] = {
		**contact_details,
		"telefonnummer": phone_number,
		"kontakt": contact,
		"typ": phone_type,
		"primaernummer": int(bool(primary)),
		"suchnummer": search_number,
	}


def _collect_contact_phone_numbers():
	contact_meta = frappe.get_meta("Contact")
	contact_fieldnames = {field.fieldname for field in contact_meta.fields}
	contact_fields = ["name"]
	contact_fields.extend(
		fieldname
		for fieldname in (
			"phone",
			"mobile_no",
			"custom_kunde",
			"full_name",
			"custom_abteilung",
			"custom_ort",
			"designation",
		)
		if fieldname in contact_fieldnames
	)

	phone_table = contact_meta.get_field("phone_nos")
	phone_table_doctype = (
		phone_table.options
		if phone_table and phone_table.fieldtype == "Table" and phone_table.options
		else None
	)
	phone_table_fields = set()
	if phone_table_doctype:
		phone_table_fields = {
			field.fieldname for field in frappe.get_meta(phone_table_doctype).fields
		}
		if "phone" not in phone_table_fields:
			phone_table_doctype = None

	phones = {}
	start = 0
	while True:
		contacts = frappe.get_all(
			"Contact",
			fields=contact_fields,
			order_by="name asc",
			limit_start=start,
			limit_page_length=PAGE_SIZE,
		)
		if not contacts:
			break

		contact_details_by_name = {}
		for contact in contacts:
			contact_details = {
				"kunde": contact.get("custom_kunde"),
				"name_komplett": contact.get("full_name"),
				"abteilung": contact.get("custom_abteilung"),
				"ort": contact.get("custom_ort"),
				"position": contact.get("designation"),
			}
			contact_details_by_name[contact.name] = contact_details
			_add_phone(
				phones,
				contact.name,
				contact.get("phone"),
				"Telefon",
				True,
				contact_details,
			)
			_add_phone(
				phones,
				contact.name,
				contact.get("mobile_no"),
				"Mobiltelefon",
				True,
				contact_details,
			)

		if phone_table_doctype:
			child_fields = ["parent", "phone"]
			child_fields.extend(
				fieldname
				for fieldname in ("is_primary_phone", "is_primary_mobile_no")
				if fieldname in phone_table_fields
			)
			for phone in _get_all_rows(
				phone_table_doctype,
				child_fields,
				filters={
					"parent": ["in", [contact.name for contact in contacts]],
					"parenttype": "Contact",
					"parentfield": "phone_nos",
				},
				order_by="parent asc, idx asc",
			):
				is_mobile = bool(phone.get("is_primary_mobile_no"))
				_add_phone(
					phones,
					phone.parent,
					phone.get("phone"),
					"Mobiltelefon" if is_mobile else "Telefon",
					bool(phone.get("is_primary_phone") or is_mobile),
					contact_details_by_name[phone.parent],
				)

		start += len(contacts)
		if len(contacts) < PAGE_SIZE:
			break

	return phones


def sync_all_contact_phone_numbers(_doc=None, _method=None):
	del _doc, _method
	desired_phones = _collect_contact_phone_numbers()
	existing_phones = {}
	duplicates = []

	for phone in _get_all_rows(
		"Telefonnummer",
		[
			"name",
			"telefonnummer",
			"kontakt",
			"kunde",
			"name_komplett",
			"abteilung",
			"ort",
			"position",
			"typ",
			"primaernummer",
			"suchnummer",
		],
	):
		search_number = phone.get("suchnummer") or normalize_phone_number(phone.get("telefonnummer"))
		key = (phone.get("kontakt"), search_number)
		if not phone.get("kontakt") or not search_number:
			duplicates.append(phone["name"])
		elif key in existing_phones:
			duplicates.append(phone["name"])
		else:
			existing_phones[key] = phone

	for key, values in desired_phones.items():
		existing = existing_phones.pop(key, None)
		if not existing:
			frappe.get_doc({"doctype": "Telefonnummer", **values}).insert(ignore_permissions=True)
			continue

		changes = {
			fieldname: value
			for fieldname, value in values.items()
			if existing.get(fieldname) != value
		}
		if changes:
			frappe.db.set_value(
				"Telefonnummer",
				existing["name"],
				changes,
			)

	for phone in existing_phones.values():
		frappe.delete_doc("Telefonnummer", phone["name"], ignore_permissions=True)
	for name in duplicates:
		frappe.delete_doc("Telefonnummer", name, ignore_permissions=True)


def delete_contact_phone_numbers(doc, _method=None):
	del _method
	phone_records = list(
		_get_all_rows(
			"Telefonnummer",
			["name"],
			filters={"kontakt": doc.name},
		)
	)
	for phone in phone_records:
		frappe.delete_doc("Telefonnummer", phone["name"], ignore_permissions=True)
