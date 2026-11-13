import unittest
from types import SimpleNamespace
from unittest.mock import patch

from vepro_app.vepro_app.doctype.telefonnummer import sync


class Row(dict):
	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError as error:
			raise AttributeError(key) from error


class TestContactPhoneSync(unittest.TestCase):
	def setUp(self):
		self.contacts = []
		self.contact_phone_rows = []
		self.telephone_rows = []
		self.contact_phone_table = SimpleNamespace(fieldtype="Table", options="Contact Phone")
		self.contact_meta = SimpleNamespace(
			fields=[
				SimpleNamespace(fieldname=fieldname)
				for fieldname in (
					"phone",
					"mobile_no",
					"phone_nos",
					"custom_kunde",
					"full_name",
					"custom_abteilung",
					"custom_ort",
					"designation",
				)
			],
			get_field=lambda fieldname: self.contact_phone_table if fieldname == "phone_nos" else None,
		)
		self.phone_meta = SimpleNamespace(
			fields=[
				SimpleNamespace(fieldname=fieldname)
				for fieldname in ("parent", "phone", "is_primary_phone", "is_primary_mobile_no")
			]
		)

		def get_all(doctype, fields, filters=None, limit_start=0, limit_page_length=20, **kwargs):
			del kwargs
			if doctype == "Contact":
				rows = self.contacts
			elif doctype == "Contact Phone":
				rows = self.contact_phone_rows
				if filters:
					parents = filters["parent"][1]
					rows = [row for row in rows if row["parent"] in parents]
			else:
				self.assertEqual(doctype, "Telefonnummer")
				rows = self.telephone_rows
				if filters and "kontakt" in filters:
					rows = [row for row in rows if row["kontakt"] == filters["kontakt"]]

			page = rows[limit_start : limit_start + limit_page_length]
			return [Row({fieldname: row.get(fieldname) for fieldname in fields}) for row in page]

		def insert(document):
			row = dict(document)
			row["name"] = f"TEL-{len(self.telephone_rows) + 1}"
			self.telephone_rows.append(row)

		def set_value(doctype, name, fields, value=None, **kwargs):
			self.assertEqual(doctype, "Telefonnummer")
			del kwargs
			row = next(row for row in self.telephone_rows if row["name"] == name)
			row.update(fields if isinstance(fields, dict) else {fields: value})

		def delete_doc(doctype, name, ignore_permissions=False):
			self.assertEqual(doctype, "Telefonnummer")
			self.assertTrue(ignore_permissions)
			self.telephone_rows[:] = [row for row in self.telephone_rows if row["name"] != name]

		def get_doc(document):
			def insert_document(ignore_permissions=False):
				self.assertTrue(ignore_permissions)
				insert(document)

			return SimpleNamespace(insert=insert_document)

		self.frappe = SimpleNamespace(
			get_meta=lambda doctype: self.contact_meta if doctype == "Contact" else self.phone_meta,
			get_all=get_all,
			get_doc=get_doc,
			db=SimpleNamespace(set_value=set_value),
			delete_doc=delete_doc,
		)
		self.frappe_patch = patch.object(sync, "frappe", self.frappe)
		self.frappe_patch.start()
		self.addCleanup(self.frappe_patch.stop)

	def test_syncs_all_contact_fields_and_phone_rows_without_cross_contact_merging(self):
		self.contacts = [
			Row(
				name="CONTACT-1",
				phone="(030) 123",
				mobile_no="0170-100",
				custom_kunde="CUSTOMER-1",
				full_name="Max Mustermann",
				custom_abteilung="Abteilung A",
				custom_ort="Berlin",
				designation="Geschäftsführer",
			),
			Row(
				name="CONTACT-2",
				phone="030 123",
				mobile_no="",
				custom_kunde="CUSTOMER-2",
				full_name="Erika Beispiel",
				custom_abteilung="Abteilung B",
				custom_ort="Hamburg",
				designation="Leitung",
			),
		]
		self.contact_phone_rows = [
			Row(parent="CONTACT-1", phone="030123", is_primary_phone=1, is_primary_mobile_no=0),
			Row(parent="CONTACT-1", phone="0155-200", is_primary_phone=0, is_primary_mobile_no=1),
		]

		sync.sync_all_contact_phone_numbers()
		sync.sync_all_contact_phone_numbers()

		records = {(row["kontakt"], row["suchnummer"]): row for row in self.telephone_rows}
		self.assertEqual(
			set(records),
			{
				("CONTACT-1", "030123"),
				("CONTACT-1", "0170100"),
				("CONTACT-1", "0155200"),
				("CONTACT-2", "030123"),
			},
		)
		self.assertEqual(records[("CONTACT-1", "0155200")]["typ"], "Mobiltelefon")
		self.assertEqual(records[("CONTACT-1", "0155200")]["primaernummer"], 1)
		self.assertEqual(records[("CONTACT-1", "030123")]["kunde"], "CUSTOMER-1")
		self.assertEqual(records[("CONTACT-1", "030123")]["name_komplett"], "Max Mustermann")
		self.assertEqual(records[("CONTACT-1", "030123")]["abteilung"], "Abteilung A")
		self.assertEqual(records[("CONTACT-1", "030123")]["ort"], "Berlin")
		self.assertEqual(records[("CONTACT-1", "030123")]["position"], "Geschäftsführer")

	def test_updates_stale_entries_and_removes_numbers_when_contact_is_deleted(self):
		self.contacts = [
			Row(
				name="CONTACT-1",
				phone="111",
				mobile_no="",
				custom_kunde="CUSTOMER-NEW",
				full_name="New Name",
				custom_abteilung="New Department",
				custom_ort="Potsdam",
				designation="Manager",
			)
		]
		self.telephone_rows = [
			Row(
				name="OLD",
				telefonnummer="222",
				kontakt="CONTACT-1",
				typ="Telefon",
				primaernummer=1,
				suchnummer="222",
			),
			Row(
				name="KEEP",
				telefonnummer="111",
				kontakt="CONTACT-1",
				typ="Fax",
				primaernummer=0,
				suchnummer="111",
				kunde="CUSTOMER-OLD",
				name_komplett="Old Name",
				abteilung="Old Department",
				ort="Berlin",
				position="Old Position",
			),
		]

		sync.sync_all_contact_phone_numbers()
		self.assertEqual([row["name"] for row in self.telephone_rows], ["KEEP"])
		self.assertEqual(self.telephone_rows[0]["typ"], "Telefon")
		self.assertEqual(self.telephone_rows[0]["primaernummer"], 1)
		self.assertEqual(self.telephone_rows[0]["kunde"], "CUSTOMER-NEW")
		self.assertEqual(self.telephone_rows[0]["name_komplett"], "New Name")
		self.assertEqual(self.telephone_rows[0]["abteilung"], "New Department")
		self.assertEqual(self.telephone_rows[0]["ort"], "Potsdam")
		self.assertEqual(self.telephone_rows[0]["position"], "Manager")

		sync.delete_contact_phone_numbers(SimpleNamespace(name="CONTACT-1"))
		self.assertEqual(self.telephone_rows, [])
