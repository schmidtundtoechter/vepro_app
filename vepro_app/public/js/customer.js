frappe.ui.form.on('Customer', {
	refresh: function(frm) {
		vepro_set_supportvertrag_color(frm);
	},
	custom_supportvertrag: function(frm) {
		vepro_set_supportvertrag_color(frm);
	}
});

function vepro_set_supportvertrag_color(frm) {
	const color_map = {
		'24/7':               { bg: '#d4edda', border: '#28a745' }, // grün
		'+3h':                { bg: '#fff3cd', border: '#ffc107' }, // gelb
		'Standard':           { bg: '#cce5ff', border: '#007bff' }, // blau
		'kein Supportvertrag':{ bg: '#f8d7da', border: '#dc3545' }, // rot
	};

	const value = frm.doc.custom_supportvertrag;
	const style = color_map[value];
	const field = frm.get_field('custom_supportvertrag');

	if (!field || !field.$input) return;

	if (style) {
		field.$input.css({
			'background-color': style.bg,
			'border-color': style.border,
			'font-weight': 'bold'
		});
	} else {
		field.$input.css({
			'background-color': '',
			'border-color': '',
			'font-weight': ''
		});
	}
}
