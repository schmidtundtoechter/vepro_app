import json
import unittest
from datetime import date
from pathlib import Path
from types import SimpleNamespace


class TestVertretungFreigabeScript(unittest.TestCase):
	def setUp(self):
		fixture = Path(__file__).resolve().parents[3] / "fixtures" / "server_script.json"
		self.script = next(
			entry["script"] for entry in json.loads(fixture.read_text())
			if entry["name"] == "Vertretung Freigabe täglich"
		)
		self.assignments = []
		self.roles = set()

	def assignment(self, name, user, start="2026-10-06", end=None, enabled=1):
		row = {
			"name": name, "vertreter": user, "von": start, "bis": end,
			"vertretung_aktiv": enabled, "status": "Vertretung ist aktiv",
		}
		self.assignments.append(row)
		return row

	def run_script(self):
		def get_all(doctype, **kwargs):
			if doctype == "Vertretung Freigabe":
				return self.assignments
			self.assertEqual(doctype, "Has Role")
			self.assertEqual(kwargs["filters"], {
				"parenttype": "User", "parentfield": "roles",
				"role": "Vepro Vertretung Freigabe",
			})
			return list(self.roles)

		def call(method, user, enabled):
			self.assertEqual(method, "vepro_app.api.set_vertretung_freigabe_role")
			if enabled:
				self.roles.add(user)
			else:
				self.roles.discard(user)

		def set_value(doctype, name, field, value):
			self.assertEqual(doctype, "Vertretung Freigabe")
			next(row for row in self.assignments if row["name"] == name)[field] = value

		frappe = SimpleNamespace(
			get_all=get_all, call=call, db=SimpleNamespace(set_value=set_value),
			utils=SimpleNamespace(today=lambda: "2026-10-07", getdate=date.fromisoformat),
		)
		exec(self.script, {"frappe": frappe})

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