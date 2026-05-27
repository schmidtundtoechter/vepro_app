import re

import frappe
from frappe import _
from frappe.model.document import Document


class SiteBrandingRule(Document):
    def validate(self):
        self._validate_match_value()
        self._validate_css_or_badge()
        self._validate_regex()
        if self.priority is None:
            self.priority = 100

    def _validate_match_value(self):
        if not (self.match_value or "").strip():
            frappe.throw(_("Match Value is required."))

    def _validate_css_or_badge(self):
        has_css = bool((self.css or "").strip())
        has_badge = bool(self.badge_enabled and (self.badge_text or "").strip())
        if not has_css and not has_badge:
            frappe.throw(
                _(
                    "Provide either Custom CSS, or enable the Badge with a Badge Text."
                )
            )

    def _validate_regex(self):
        if self.match_type == "Regex":
            try:
                re.compile(self.match_value)
            except re.error as exc:
                frappe.throw(_("Invalid Regex pattern: {0}").format(str(exc)))
