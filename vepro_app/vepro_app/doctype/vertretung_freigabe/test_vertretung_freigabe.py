import importlib.util
import json
import sys
import unittest
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


class TestVertretungFreigabeScript(unittest.TestCase):
	def setUp(self):
		fixtures = Path(__file__).resolve().parents[3] / "fixtures"
		server_scripts = json.loads((fixtures / "server_script.json").read_text())
		self.scheduler_script = next(
			entry["script"] for entry in server_scripts
			if entry["name"] == "Vertretung Freigabe täglich"
		)
		client_scripts = json.loads((fixtures / "client_script.json").read_text())
		self.client_script = next(
			entry["script"] for entry in client_scripts
			if entry["name"] == "Vertretung Freigabe sofort synchronisieren"
		)
		self.assignments = []
		self.roles = set()
		self.api_path = Path(__file__).resolve().parents[3] / "api.py"

	def assignment(self, name, user, start="2026-10-06", end=None, enabled=1):
		row = {
			"name": name, "vertreter": user, "von": start, "bis": end,
			"vertretung_aktiv": enabled, "status": "Vertretung ist aktiv",
		}
		self.assignments.append(row)
		return row

	def load_api(self):
		def get_all(doctype, **kwargs):
			if doctype == "Vertretung Freigabe":
				return [SimpleNamespace(**row) for row in self.assignments]
			self.assertEqual(doctype, "Has Role")
			self.assertEqual(kwargs["filters"], {
				"parenttype": "User", "parentfield": "roles",
				"role": "Vepro Vertretung Freigabe",
			})
			return list(self.roles)

		def set_value(doctype, name, field, value):
			self.assertEqual(doctype, "Vertretung Freigabe")
			next(row for row in self.assignments if row["name"] == name)[field] = value

		def role_exists(doctype, filters):
			if doctype == "User":
				return True
			self.assertEqual(doctype, "Has Role")
			return filters["parent"] in self.roles

		def insert_role(doctype, filters):
			self.assertEqual(doctype, "Has Role")
			self.roles.add(filters["parent"])

		def delete_roles(doctype, filters):
			self.assertEqual(doctype, "Has Role")
			self.roles.discard(filters["parent"])

		def get_doc(document):
			return SimpleNamespace(
				insert=lambda ignore_permissions: insert_role(document["doctype"], document)
			)

		frappe = SimpleNamespace(
			whitelist=lambda: lambda function: function,
			only_for=lambda role: self.assertEqual(role, "System Manager"),
			get_all=get_all,
			get_doc=get_doc,
			clear_cache=lambda **kwargs: None,
			db=SimpleNamespace(
				set_value=set_value,
				exists=role_exists,
				delete=delete_roles,
			),
			utils=SimpleNamespace(today=lambda: "2026-10-07", getdate=date.fromisoformat),
		)
		with patch.dict(sys.modules, {"frappe": frappe}):
			spec = importlib.util.spec_from_file_location("vepro_app_test_api", self.api_path)
			api = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(api)
		return api.sync_vertretung_freigabe

	def run_script(self):
		self.load_api()()

	def test_scheduler_and_client_script_call_shared_sync(self):
		self.assertIn('frappe.call("vepro_app.api.sync_vertretung_freigabe")', self.scheduler_script)
		self.assertIn('after_save(frm)', self.client_script)
		self.assertIn('frappe.call("vepro_app.api.sync_vertretung_freigabe")', self.client_script)

	def test_deleted_document_and_empty_assignments_revoke_roles(self):
		self.roles = {"orphan", "another-orphan"}
		self.run_script()
		self.assertEqual(self.roles, set())

	def test_validity_boundaries_status_and_overlapping_assignments(self):
		self.assignment("open", "open")
		self.assignment("start", "start", start="2026-10-07", end="2026-10-08")
		self.assignment("end", "end", end="2026-10-07")
		self.assignment("expired", "expired", end="2026-10-06")
		self.assignment("future", "future", start="2026-10-08")
		self.assignment("disabled", "disabled", enabled=0)
		self.assignment("overlap-old", "overlap", end="2026-10-06")
		self.assignment("overlap-current", "overlap")
		self.assignment("missing-start", "missing-start", start=None)
		self.assignment("missing-user", None)
		self.roles = {"expired", "future", "disabled", "overlap", "orphan"}
		self.run_script()
		self.assertEqual(self.roles, {"open", "start", "end", "overlap"})
		active_names = {"open", "start", "end", "overlap-current"}
		for row in self.assignments:
			self.assertEqual(row["status"],
				"Vertretung ist aktiv" if row["name"] in active_names else "Vertretung nicht aktiv")
		self.run_script()
		self.assertEqual(self.roles, {"open", "start", "end", "overlap"})

	def test_changed_representative_then_deletion(self):
		row = self.assignment("changed", "new-user")
		self.roles = {"old-user"}
		self.run_script()
		self.assertEqual(self.roles, {"new-user"})
		self.assignments.remove(row)
		self.run_script()
		self.assertEqual(self.roles, set())