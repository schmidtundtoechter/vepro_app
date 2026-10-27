frappe.ui.form.on("Purchase Order", {
	refresh: vepro_sync_endkunde,
	customer: vepro_sync_endkunde,
	validate: vepro_sync_endkunde,
});

function vepro_sync_endkunde(frm) {
	if (frm.doc.docstatus === 0 && frm.doc.customer && frm.doc.custom_endkunde !== frm.doc.customer) {
		return frm.set_value("custom_endkunde", frm.doc.customer);
	}
}
