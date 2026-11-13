# Copyright (c) 2026, Schmidt und Toechter and contributors
# For license information, please see license.txt

import re

from frappe.model.document import Document


def normalize_phone_number(number):
	return re.sub(r"\D", "", number or "")


class Telefonnummer(Document):
	def validate(self):
		self.suchnummer = normalize_phone_number(self.telefonnummer)
