from add_account import add_account
from add_budget import add_budget
from add_category import add_category
from add_income import add_income
from add_planned_expense import add_planned_expense

def initialise_db():
    add_account("Bank")
    add_account("Cash")

    add_budget("Planned Expense Budget")

    add_category("Food Expense")
    add_category("Home Expense")
    add_category("Health Expense")
    add_category("Car Expense")
    add_category("Bills")

    add_income("Salary")
    add_income("Other")

    add_planned_expense("Food Expense", 2000)
    add_planned_expense("Home Expense", 1000)
    add_planned_expense("Health Expense", 500)
    add_planned_expense("Car Expense", 500)
    add_planned_expense("Bills", 700)
