import frappe
from frappe.model.document import Document
from collections import defaultdict
import time
import random

class MonthlyBudgetDistributionTool(Document):
    pass



def generate_unique_value():
    timestamp = int(time.time() * 1000)  # current timestamp in milliseconds
    random_number = random.randint(1, 1000)  # generate a random number
    unique_value = f"{timestamp}-{random_number}"
    return unique_value
def sort_months(months):
    # List of months in their natural order
    natural_order = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]

    # Create a dictionary to map month names to their respective indices
    month_indices = {month: index for index, month in enumerate(natural_order)}

    # Sort the input months list based on their indices in the natural order
    sorted_months = sorted(months, key=lambda month: month_indices[month])

    return sorted_months

@frappe.whitelist(allow_guest=True)
def create_budget(name):
    doc = frappe.get_doc('Monthly Budget Distribution Tool', name)
    
    period = frappe.db.sql(f"""SELECT period, fiscal_year FROM `tabMonthly Distribution Map Table` WHERE parent='{doc.monthly_distribution_template}'""", as_dict=True)

    # Group periods by fiscal year and sort months
    periods_by_year = defaultdict(list)
    for entry in period:
        periods_by_year[entry['fiscal_year']].append(entry['period'])

    for fiscal_year in periods_by_year:
        periods_by_year[fiscal_year] = sort_months(periods_by_year[fiscal_year])

    # Dictionary to hold the total amount for each account by fiscal year
    account_total_by_year = defaultdict(lambda: defaultdict(float))

    # Calculate total amounts for each account by fiscal year
    for t in doc.monthly_budget_distribution_table:
        for fiscal_year, months in periods_by_year.items():
            total_amount = sum(getattr(t, f"{month.lower()}", 0) for month in months)
            account_total_by_year[fiscal_year][t.account] += total_amount

    # Create Monthly Distribution and Budget documents
    for fiscal_year, months in periods_by_year.items():
        

        for t in doc.monthly_budget_distribution_table:
            unique_value = generate_unique_value()
            distribution_id = f"{fiscal_year}-monthly-distribution-{unique_value}"
            # Filter months to only include periods relevant to the fiscal year
            filtered_months = [month for month in months if getattr(t, month.lower(), 0)]

            # Calculate total amount for this account in this fiscal year
            total_amount = sum(getattr(t, f"{month.lower()}", 0) for month in filtered_months)

            # Calculate percentages and create documents
            if total_amount > 0:
                percentages = [{
                    'month': month,
                    'percentage_allocation': (getattr(t, f"{month.lower()}", 0) / total_amount) * 100
                } for month in filtered_months]

                # Create Monthly Distribution and Budget documents
                if doc.applicable_on_material_request == 1:
                    new_monthly_distribution_doc = frappe.get_doc({
                        'doctype': 'Monthly Distribution',
                        'distribution_id': distribution_id,
                        'fiscal_year': fiscal_year,
                        'account': t.account,
                        'percentages': percentages,
                    })
                    new_budget_doc = frappe.get_doc({
                        'doctype': 'Budget',
                        'budget_against': doc.budget_against,
                        'company': doc.company,
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
                        'fiscal_year': fiscal_year,
                        'accounts': [{'account': t.account, 'budget_amount': total_amount}],
                    })
                    if doc.budget_against == 'Project':
                        new_budget_doc.project = doc.project
                    elif doc.budget_against == 'Cost Center':
                        new_budget_doc.cost_center = doc.cost_center
                    if not frappe.db.exists("Monthly Distribution", {"name": distribution_id}):
                        new_monthly_distribution_doc.insert()
                        new_budget_doc.insert()
                        new_budget_doc.submit()
                        frappe.db.commit()
                else:
                    new_monthly_distribution_doc = frappe.get_doc({
                        'doctype': 'Monthly Distribution',
                        'distribution_id': distribution_id,
                        'fiscal_year': fiscal_year,
                        'account': t.account,
                        'percentages': percentages,
                    })
                    new_budget_doc = frappe.get_doc({
                        'doctype': 'Budget',
                        'budget_against': doc.budget_against,
                        'company': doc.company,
                        'monthly_distribution': distribution_id,
                        'applicable_on_material_request': doc.applicable_on_material_request,
                        'applicable_on_purchase_order': doc.applicable_on_purchase_order,
                        'applicable_on_booking_actual_expenses': doc.applicable_on_booking_actual_expenses,
                        'fiscal_year': fiscal_year,
                        'accounts': [{'account': t.account, 'budget_amount': total_amount}],
                    })
                    if doc.budget_against == 'Project':
                        new_budget_doc.project = doc.project
                    elif doc.budget_against == 'Cost Center':
                        new_budget_doc.cost_center = doc.cost_center
                    if not frappe.db.exists("Monthly Distribution", {"name": distribution_id}):
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
            'fiscal_year': entry['fiscal_year'],
            'account': account,
            'percentages': percentages_list,
        })


        

@frappe.whitelist(allow_guest=True)
def get_period(name):
    period=frappe.db.sql(f"""SELECT period from `tabMonthly Distribution Map Table` where parent='{name}'""")
    return period

def test():
    pass