frappe.ui.form.on("Sales Invoice", {
	custom_incoterm_benutzen: function(frm) {
		if (frm.doc.custom_incoterm_benutzen) {
			if (!frm.doc.incoterm) {
				frm.set_value("incoterm", "CPT");
			}
		} else {
			frm.set_value("incoterm", "");
			frm.set_value("named_place", "");
		}
	},
});