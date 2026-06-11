frappe.ui.form.on('Contact', {
	custom_auswahl_position: function(frm) {
		frm.set_value('designation', frm.doc.custom_auswahl_position || '');
	}
});
