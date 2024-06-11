# Copyright (c) 2024, aqiq Budget and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from collections import defaultdict

class MonthlyBudgetDistributionTool(Document):
	pass
@frappe.whitelist(allow_guest=True)
def create_budget(name):
    print(name)
    doc = frappe.get_doc('Monthly Budget Distribution Tool', name)
    print(doc.monthly_budget_distribution_table)
    period = frappe.db.sql(f"""SELECT period FROM `tabMonthly Distribution Map Table` WHERE parent='{doc.monthly_distribution_template}'""", as_dict=True)
    print(period)
    periods_count = len(period)
    percentages = []

    # Dictionary to hold the total amount for each account
    account_total = defaultdict(float)

    # Calculate total amount for each account
    for t in doc.monthly_budget_distribution_table:
        for index, month in enumerate(period, start=1):
            year_field = f'year_{index}'
            amount = getattr(t, year_field, 0)
            account_total[t.account] += amount

    percentages = []

    # Calculate percentage allocation for each account
    for t in doc.monthly_budget_distribution_table:
        for index, month in enumerate(period, start=1):
            year_field = f'year_{index}'
            amount = getattr(t, year_field, 0)
            total_amount = account_total[t.account]
            percentage_allocation = (amount / total_amount) * 100 if total_amount != 0 else 0
            print(percentage_allocation)
            if percentage_allocation > 0.0:
                percentages.append({
                    'account': t.account,
                    'month': month['period'],
                    'percentage_allocation': f"{percentage_allocation}",
                    'total_amount': total_amount
                })

    print("Percentages collected:", percentages)
    grouped_percentages = defaultdict(list)
    for percentage_data in percentages:
        account = percentage_data['account']
        total_amount = percentage_data['total_amount']
        grouped_percentages[account].append({
            'month': percentage_data['month'],
            'percentage_allocation': percentage_data['percentage_allocation'],
            'total_amount': total_amount
        })

    for account, percentages_list in grouped_percentages.items():
        distribution_id = f"{doc.fiscal_year}-{account.replace(' ', '-')}"
        if doc.applicable_on_material_request == 1:
            if doc.budget_against == 'Project':
                new_monthly_distribution_doc = frappe.get_doc({
                    'doctype': 'Monthly Distribution',
                    'distribution_id': distribution_id,
                    'fiscal_year': doc.fiscal_year,
                    'account': account,
                    'percentages': percentages_list,
                })
                new_budget_doc = frappe.get_doc({
                    'doctype': 'Budget',
                    'budget_against': doc.budget_against,
                    'company': doc.company,
                    'project': doc.project,
                    'monthly_distribution': distribution_id,
                    'applicable_on_material_request': doc.applicable_on_material_request,
                    'action_if_annual_budget_exceeded_on_mr': doc.action_if_annual_budget_exceeded_on_mr,
                    'action_if_accumulated_monthly_budget_exceeded_on_mr': doc.action_if_accumulated_monthly_budget_exceeded_on_mr,
                    'applicable_on_purchase_order': doc.applicable_on_purchase_order,
                    'action_if_annual_budget_exceeded_on_po': doc.action_if_annual_budget_exceeded_on_po,
                    'action_if_accumulated_monthly_budget_exceeded_on_po': doc.action_if_accumulated_monthly_budget_exceeded_on_po,
                    'applicable_on_booking_actual_expenses': doc.applicable_on_booking_actual_expenses,
                    'action_if_annual_budget_exceeded_on_actual': doc.action_if_annual_budget_exceeded_on_actual,
                    'action_if_accumulated_monthly_budget_exceeded_on_actual': doc.action_if_accumulated_monthly_budget_exceeded_on_actual,
                    'fiscal_year': doc.fiscal_year,
                    'accounts': [{'account': account, 'budget_amount': total_amount}],
                })
            elif doc.budget_against == 'Cost Center':
                new_monthly_distribution_doc = frappe.get_doc({
                    'doctype': 'Monthly Distribution',
                    'distribution_id': distribution_id,
                    'fiscal_year': doc.fiscal_year,
                    'account': account,
                    'percentages': percentages_list,
                })
                new_budget_doc = frappe.get_doc({
                    'doctype': 'Budget',
                    'budget_against': doc.budget_against,
                    'company': doc.company,
                    'cost_center': doc.cost_center,
                    'monthly_distribution': distribution_id,
                    'applicable_on_material_request': doc.applicable_on_material_request,
                    'action_if_annual_budget_exceeded_on_mr': doc.action_if_annual_budget_exceeded_on_mr,
                    'action_if_accumulated_monthly_budget_exceeded_on_mr': doc.action_if_accumulated_monthly_budget_exceeded_on_mr,
                    'applicable_on_purchase_order': doc.applicable_on_purchase_order,
                    'action_if_annual_budget_exceeded_on_po': doc.action_if_annual_budget_exceeded_on_po,
                    'action_if_accumulated_monthly_budget_exceeded_on_po': doc.action_if_accumulated_monthly_budget_exceeded_on_po,
                    'applicable_on_booking_actual_expenses': doc.applicable_on_booking_actual_expenses,
                    'action_if_annual_budget_exceeded_on_actual': doc.action_if_annual_budget_exceeded_on_actual,
                    'action_if_accumulated_monthly_budget_exceeded_on_actual': doc.action_if_accumulated_monthly_budget_exceeded_on_actual,
                    'fiscal_year': doc.fiscal_year,
                    'accounts': [{'account': account, 'budget_amount': total_amount}],
                })
            else:
                pass
            if not frappe.db.exists("Monthly Distribution", {"name": distribution_id}):
                print(new_monthly_distribution_doc)
                new_monthly_distribution_doc.insert()
                new_budget_doc.insert()
                new_budget_doc.submit()
                frappe.db.commit()
        else:
            if doc.budget_against == 'Project':
                new_monthly_distribution_doc = frappe.get_doc({
                    'doctype': 'Monthly Distribution',
                    'distribution_id': distribution_id,
                    'fiscal_year': doc.fiscal_year,
                    'account': account,
                    'percentages': percentages_list,
                })
                new_budget_doc = frappe.get_doc({
                    'doctype': 'Budget',
                    'budget_against': doc.budget_against,
                    'company': doc.company,
                    'project': doc.project,
                    'monthly_distribution': distribution_id,
                    'applicable_on_material_request': doc.applicable_on_material_request,
                    'applicable_on_purchase_order': doc.applicable_on_purchase_order,
                    'Applicable on booking actual expenses': doc.applicable_on_booking_actual_expenses,
                    'fiscal_year': doc.fiscal_year,
                    'accounts': [{'account': account, 'budget_amount': total_amount}],
                })
            elif doc.budget_against == 'Cost Center':
                new_monthly_distribution_doc = frappe.get_doc({
                    'doctype': 'Monthly Distribution',
                    'distribution_id': distribution_id,
                    'fiscal_year': doc.fiscal_year,
                    'account': account,
                    'percentages': percentages_list,
                })
                new_budget_doc = frappe.get_doc({
                    'doctype': 'Budget',
                    'budget_against': doc.budget_against,
                    'company': doc.company,
                    'cost_center': doc.cost_center,
                    'monthly_distribution': distribution_id,
                    'applicable_on_material_request': doc.applicable_on_material_request,
                    'applicable_on_purchase_order': doc.applicable_on_purchase_order,
                    'fiscal_year': doc.fiscal_year,
                    'accounts': [{'account': account, 'budget_amount': total_amount}],
                })
            else:
                pass
            if not frappe.db.exists("Monthly Distribution", {"name": distribution_id}):
                print(new_monthly_distribution_doc)
                new_monthly_distribution_doc.insert()
                new_budget_doc.insert()
                new_budget_doc.submit()
                frappe.db.commit()

@frappe.whitelist()
def test():
    account
    new_monthly_distribution_doc = frappe.get_doc({
            'doctype': 'Monthly Distribution',
            'distribution_id': distribution_id,
            'fiscal_year': doc.fiscal_year,
            'account': account,
            'percentages': percentages_list,
        })


        

@frappe.whitelist(allow_guest=True)
def get_period(name):
    period=frappe.db.sql(f"""SELECT period from `tabMonthly Distribution Map Table` where parent='{name}'""")
    return period

def test():
    pass