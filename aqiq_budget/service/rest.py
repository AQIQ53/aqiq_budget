import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def create_multiple_sales_invoice(name):
    doc = frappe.get_doc('Sales Order', name)
    
    for payment in doc.payment_schedule:
    
        if not frappe.db.exists("Sales Invoice Item", {"docstatus": 1,"custom_payment_schedule_id": payment.name}):
            sales_invoice = frappe.get_doc({
                'doctype': 'Sales Invoice',
                'customer': doc.customer,
                'set_posting_time': doc.transaction_date,
                'due_date': doc.delivery_date,
                'company': doc.company,
                'cost_center': doc.cost_center,
                'project': doc.project,
                'currency': doc.currency,
                'selling_price_list': doc.selling_price_list,
                'items': [],
                'payment_schedule': [{
                    'due_date': payment.due_date,
                    'payment_amount': payment.payment_amount,
                    'base_payment_amount': payment.base_payment_amount,
                    'outstanding': payment.outstanding
                }],
            })
            
            for item in doc.items:
                sales_invoice.append('items', {
                    'item_code': item.item_code,
                    'item_name': item.item_name,
                    'description': item.description,
                    'uom': item.uom,
                    'conversion_factor':item.conversion_factor,
                    'qty': item.qty,
                    'rate': payment.payment_amount,
                    'amount': item.amount,
                    'warehouse': item.warehouse,
                    'sales_order':doc.name,
                    'custom_payment_schedule_id':payment.name
                })
            
            sales_invoice.insert()
            sales_invoice.submit()
        else:
            frappe.msgprint(_("Sales invoice could not be created because sales invoice exists with same Payment ID {0}").format(payment.name))
