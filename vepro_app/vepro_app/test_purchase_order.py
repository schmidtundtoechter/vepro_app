import unittest
from types import SimpleNamespace

from vepro_app.vepro_app.purchase_order import sync_endkunde


class TestPurchaseOrderEndkunde(unittest.TestCase):
	def test_customer_is_copied_exactly(self):
		doc = SimpleNamespace(customer="CUST-00042", custom_endkunde=None)
		sync_endkunde(doc)
		self.assertEqual(doc.custom_endkunde, "CUST-00042")

	def test_changed_customer_replaces_endkunde(self):
		doc = SimpleNamespace(customer="CUST-00043", custom_endkunde="CUST-00042")
		sync_endkunde(doc)
		self.assertEqual(doc.custom_endkunde, "CUST-00043")

	def test_missing_customer_preserves_manual_endkunde(self):
		for customer in (None, ""):
			with self.subTest(customer=customer):
				doc = SimpleNamespace(customer=customer, custom_endkunde="CUST-MANUAL")
				sync_endkunde(doc)
				self.assertEqual(doc.custom_endkunde, "CUST-MANUAL")
