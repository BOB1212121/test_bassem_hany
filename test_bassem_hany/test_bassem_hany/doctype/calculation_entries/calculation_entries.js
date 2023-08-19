// Copyright (c) 2023, Bassem Hany and contributors
// For license information, please see license.txt

frappe.ui.form.on('Calculation Entries', {
	customer: function(frm) {
		let customer=cur_frm.doc.customer;
		if (frm.is_new()) {
			frappe.call({
				method: "test_bassem_hany.test_bassem_hany.doctype.calculation_entries.calculation_entries.get_serial",
				args: {
					customer : customer,
				},
				callback: (r)=> {
				  cur_frm.set_value("serial", r.message.toString());
				}
			});
		}
		
	},
	before_save: function(frm) {
		if (!frm.is_new()) {
			frm.clear_table("monthly_average_tariff");
		}
	}
});
