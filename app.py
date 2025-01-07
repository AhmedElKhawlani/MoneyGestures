from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import func
from datetime import datetime
from utils.model import Transaction, Budget, Account, PlannedExpense, Category, Income, engine
import secrets
import logging

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Database session with scoped_session for thread safety
Session = scoped_session(sessionmaker(bind=engine))

@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

@app.route('/show_transactions', methods=['GET'])
def show_transactions():
    try:
        transactions = Session.query(Transaction).all()
        return render_template('show_transactions.html', transactions=transactions)
    except Exception as e:
        logging.error("Error fetching transactions: %s", e)
        flash("An error occurred while loading transactions. Please try again later.", "danger")
        return redirect(url_for('show_transactions'))

@app.route('/record_unplanned_expense', methods=['GET', 'POST'])
def record_unplanned_expense():
    categories = Session.query(Category.name).distinct().all()
    category_list = [category.name for category in categories]
    budgets = Session.query(Budget.name).distinct().all()
    budget_list = [budget[0] for budget in budgets]
    accounts = Session.query(Account.name).distinct().all()
    account_list = [account[0] for account in accounts]
    if request.method == 'POST':
        try:
            data = request.form
            print(f"Form data received: {data}")
            # Validate form data
            required_fields = ['description', 'category', 'amount', 'account', 'budget']
            print(data)
            for field in required_fields:
                if (not field in data) or (not data[field].strip()):
                    flash("All fields are required!", "danger")
                    return redirect(url_for('record_unplanned_expense'))

            # Parse and validate specific fields
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    flash("Amount must be greater than 0!", "danger")
                    return redirect(url_for('record_unplanned_expense'))
                
                budget_name = data['budget'].strip()
                budget = Session.query(Budget).filter_by(name=budget_name).first()
                if amount > budget.balance:
                    flash(f"The amount exceeds the available budget '{budget_name}'.", "danger")
                    print(f"The amount exceeds the available budget '{budget_name}'.", "danger")
                    return redirect(url_for('record_unplanned_expense'))
                
                account_name = data['account'].strip()
                account = Session.query(Account).filter_by(name=account_name).first()
                if amount > account.balance:
                    flash(f"The amount exceeds the balance in account '{account_name}'.", "danger")
                    print(f"The amount exceeds the balance in account '{account_name}'.", "danger")
                    return redirect(url_for('record_unplanned_expense'))

                budget.balance-= amount

                account.balance -= amount

            except ValueError as e:
                flash("Invalid date/time or amount format!", "danger")
                print(f"Parsing error: {e}")
                return redirect(url_for('record_unplanned_expense'))
            
            
            # Add the transaction
            transaction = Transaction(
                description=data['description'].strip(),
                category=data['category'].strip(),
                nature="Unplanned Expense",
                amount=amount,
                account=data['account'].strip(),
                budget=data['budget'].strip()
            )

            Session.add(transaction)
            Session.commit()
            flash("Transaction added successfully!", "success")
        except Exception as e:
            Session.rollback()
            logging.error("Error adding transaction: %s", e)
            flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('show_transactions'))
    return render_template('record_unplanned_expense.html', categories=category_list, budgets=budget_list, accounts=account_list)


@app.route('/record_income', methods=['GET', 'POST'])
def record_income():
    incomes = Session.query(Income.name).distinct().all()
    income_list = [income[0] for income in incomes]
    budgets = Session.query(Budget.name).distinct().all()
    budget_list = [budget[0] for budget in budgets]
    accounts = Session.query(Account.name).distinct().all()
    account_list = [account[0] for account in accounts]
    if request.method == 'POST':
        try:
            data = request.form
            print(f"Form data received: {data}")
            # Validate form data
            required_fields = ['description', 'amount', 'account', 'budget']
            print(data)
            for field in required_fields:
                if (not field in data) or (not data[field].strip()):
                    flash("All fields are required!", "danger")
                    return redirect(url_for('record_income'))

            # Parse and validate specific fields
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    flash("Amount must be greater than 0!", "danger")
                    return redirect(url_for('record_income'))
                
                budget_name = data['budget'].strip()
                budget = Session.query(Budget).filter_by(name=budget_name).first()
                
                account_name = data['account'].strip()
                account = Session.query(Account).filter_by(name=account_name).first()
                
                budget.balance += amount

                account.balance += amount

            except ValueError as e:
                flash("Invalid date/time or amount format!", "danger")
                print(f"Parsing error: {e}")
                return redirect(url_for('record_income'))
            
            
            # Add the transaction
            transaction = Transaction(
                description=data['description'].strip(),
                category="Income",
                nature="Income",
                amount=amount,
                account=data['account'].strip(),
                budget=data['budget'].strip()
            )

            Session.add(transaction)
            Session.commit()
            flash("Transaction added successfully!", "success")
        except Exception as e:
            Session.rollback()
            logging.error("Error adding transaction: %s", e)
            flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('show_transactions'))
    return render_template('record_income.html', budgets=budget_list, accounts=account_list, incomes=income_list)

@app.route('/show_planned_expenses', methods=['GET'])
def show_planned_expenses():
    try:
        planned_expenses = Session.query(PlannedExpense).all()
        return render_template('show_planned_expenses.html', planned_expenses=planned_expenses)
    except Exception as e:
        logging.error("Error fetching planned expenses: %s", e)
        flash("An error occurred while loading planned expenses. Please try again later.", "danger")
        return redirect(url_for('show_planned_expenses'))
    
@app.route('/record_planned_expense', methods=['GET', 'POST'])
def record_planned_expense():
    categories = Session.query(PlannedExpense.category).distinct().all()
    category_list = [category[0] for category in categories]
    accounts = Session.query(Account.name).distinct().all()
    account_list = [account[0] for account in accounts]
    if request.method == 'POST':
        try:
            data = request.form
            print(f"Form data received: {data}")
            # Validate form data
            required_fields = ['description', 'category', 'amount', 'account']
            print(data)
            for field in required_fields:
                if (not field in data) or (not data[field].strip()):
                    flash("All fields are required!", "danger")
                    return redirect(url_for('record_planned_expense'))

            # Parse and validate specific fields
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    flash("Amount must be greater than 0!", "danger")
                    return redirect(url_for('record_planned_expense'))
                category_name = data['category'].strip()
                planned_expense = Session.query(PlannedExpense).filter_by(category=category_name).first()
                if amount > planned_expense.left_budget:
                    flash(f"The amount exceeds the remaining budget for category '{category_name}'.", "danger")
                    print(f"The amount exceeds the remaining budget for category '{category_name}'.", "danger")
                    return redirect(url_for('record_planned_expense'))
                
                budget_name = "Planned Expense Budget"
                budget = Session.query(Budget).filter_by(name=budget_name).first()
                if amount > budget.balance:
                    flash(f"The amount exceeds the available budget '{budget_name}'.", "danger")
                    print(f"The amount exceeds the available budget '{budget_name}'.", "danger")
                    return redirect(url_for('record_planned_expense'))
                
                account_name = data['account'].strip()
                account = Session.query(Account).filter_by(name=account_name).first()
                if amount > account.balance:
                    flash(f"The amount exceeds the balance in account '{account_name}'.", "danger")
                    print(f"The amount exceeds the balance in account '{account_name}'.", "danger")
                    return redirect(url_for('record_planned_expense'))
                
                planned_expense.consumed_budget += amount
                planned_expense.left_budget -= amount

                budget.balance-= amount

                account.balance -= amount

            except ValueError as e:
                flash("Invalid date/time or amount format!", "danger")
                print(f"Parsing error: {e}")
                return redirect(url_for('record_planned_expense'))
            
            
            # Add the transaction
            transaction = Transaction(
                description=data['description'].strip(),
                category=data['category'].strip(),
                nature="Planned Expense",
                amount=amount,
                account=data['account'].strip(),
                budget="Planned Expense Budget"
            )

            Session.add(transaction)
            Session.commit()
            flash("Transaction added successfully!", "success")
        except Exception as e:
            Session.rollback()
            logging.error("Error adding transaction: %s", e)
            flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('show_transactions'))
    return render_template('record_planned_expense.html', categories=category_list, accounts=account_list)


@app.route('/show_budgets', methods=['GET'])
def show_budgets():
    try:
        budgets = Session.query(Budget).all()
        return render_template('show_budgets.html', budgets=budgets)
    except Exception as e:
        logging.error("Error fetching budgets: %s", e)
        flash("An error occurred while loading budgets. Please try again later.", "danger")
        return redirect(url_for('show_budgets'))

@app.route('/add_budget', methods=['GET', 'POST'])
def add_budget():
    if request.method == 'POST':
        try:
            data = request.form
            print(f"Form data received: {data}")

            # Validate form data
            required_fields = ['name']
            for field in required_fields:
                if not data.get(field) or not data[field].strip():
                    flash("All fields are required!", "danger")
                    return redirect(url_for('add_budget'))
                
            budget_name = data['name'].strip()

            # Check if the budget already exists
            existing_budget = Session.query(Budget).filter_by(name=budget_name).first()
            if existing_budget:
                flash(f"A budget with the name '{budget_name}' already exists!", "danger")
                return redirect(url_for('add_budget'))
            
            # Add the budget
            budget = Budget(
                name=budget_name,
                balance=0 
            )

            Session.add(budget)
            Session.commit()
            flash("Budget added successfully!", "success")
        except Exception as e:
            Session.rollback()
            logging.error("Error adding budget: %s", e)
            flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('show_budgets'))
    return render_template('add_budget.html')

@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    if request.method == 'POST':
        try:
            data = request.form
            print(f"Form data received: {data}")

            # Validate form data
            required_fields = ['name']
            for field in required_fields:
                if not data.get(field) or not data[field].strip():
                    flash("All fields are required!", "danger")
                    return redirect(url_for('add_account'))
            
            account_name = data['name'].strip()
            # Check if the account already exists
            existing_account = Session.query(Account).filter_by(name=account_name).first()
            if existing_account:
                flash(f"An account with the name '{account_name}' already exists!", "danger")
                return redirect(url_for('add_account'))
            
            # Add the budget
            account = Account(
                name=account_name,
                balance=0 
            )

            Session.add(account)
            Session.commit()
            flash("Account added successfully!", "success")
        except Exception as e:
            Session.rollback()
            logging.error("Error adding budget: %s", e)
            flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('show_accounts'))
    return render_template('add_account.html')

@app.route('/show_accounts', methods=['GET'])
def show_accounts():
    try:
        accounts = Session.query(Account).all()
        return render_template('show_accounts.html', accounts=accounts)
    except Exception as e:
        logging.error("Error fetching accounts: %s", e)
        flash("An error occurred while loading accounts. Please try again later.", "danger")
        return redirect(url_for('show_accounts'))

@app.route('/add_planned_expense', methods=['GET', 'POST'])
def add_planned_expense():
    try:
        if request.method == 'GET':
            # Fetch all categories
            all_categories = Session.query(Category).all()
            used_categories = Session.query(PlannedExpense.category).distinct().all()
            used_category_names = {category[0] for category in used_categories}

            # Filter unused categories
            available_categories = [
                category for category in all_categories if category.name not in used_category_names
            ]

            return render_template('add_planned_expense.html', categories=available_categories)

        elif request.method == 'POST':
            data = request.form

            # Validate category selection
            if 'category' not in data or not data['category'].strip():
                flash("Category is required!", "danger")
                return redirect(url_for('add_planned_expense'))

            category_name = data['category'].strip()

            # Add new planned expense
            new_planned_expense = PlannedExpense(
                category=category_name,
                monthly_budget=0,
                consumed_budget=0,
                left_budget=0
            )
            Session.add(new_planned_expense)
            Session.commit()

            flash("Planned expense added successfully!", "success")
            return redirect(url_for('show_planned_expenses'))

    except Exception as e:
        Session.rollback()
        logging.error("Error adding planned expense: %s", e)
        flash("An error occurred while adding the planned expense. Please try again.", "danger")
        return redirect(url_for('add_planned_expense'))

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    try:
        if request.method == 'GET':
            return render_template('add_category.html')

        elif request.method == 'POST':
            data = request.form

            # Validate category name
            if 'name' not in data or not data['name'].strip():
                flash("Category name is required!", "danger")
                return redirect(url_for('add_category'))

            category_name = data['name'].strip()

            # Check if category already exists
            existing_category = Session.query(Category).filter_by(name=category_name).first()
            if existing_category:
                flash("Category already exists!", "danger")
                return redirect(url_for('add_category'))

            # Add new category
            new_category = Category(name=category_name)
            Session.add(new_category)
            Session.commit()

            flash("Category added successfully!", "success")
            return redirect(url_for('add_category'))

    except Exception as e:
        Session.rollback()
        logging.error("Error adding category: %s", e)
        flash("An error occurred while adding the category. Please try again.", "danger")
        return redirect(url_for('add_category'))

@app.route('/add_income', methods=['GET', 'POST'])
def add_income():
    try:
        if request.method == 'GET':
            return render_template('add_income.html')

        elif request.method == 'POST':
            data = request.form

            # Validate the name field
            if not data.get('name') or not data['name'].strip():
                flash("Name is required!", "danger")
                return redirect(url_for('add_income'))

            # Add the income to the database
            new_income = Income(
                name=data['name'].strip()
            )

            Session.add(new_income)
            Session.commit()

            flash("Income added successfully!", "success")
            return redirect(url_for('dashboard'))

    except Exception as e:
        Session.rollback()
        logging.error("Error adding income: %s", e)
        flash("An error occurred while adding the income. Please try again.", "danger")
        return redirect(url_for('add_income'))

@app.route('/show_categories', methods=['GET'])
def show_categories():
    try:
        # Fetch all categories from the database
        categories = Session.query(Category).all()
        return render_template('show_categories.html', categories=categories)
    except Exception as e:
        logging.error("Error fetching categories: %s", e)
        flash("An error occurred while loading categories. Please try again.", "danger")
        return redirect(url_for('dashboard'))

@app.route('/show_incomes', methods=['GET'])
def show_incomes():
    try:
        # Fetch all incomes from the database
        incomes = Session.query(Income).all()
        return render_template('show_incomes.html', incomes=incomes)
    except Exception as e:
        logging.error("Error fetching incomes: %s", e)
        flash("An error occurred while loading incomes. Please try again.", "danger")
        return redirect(url_for('dashboard'))

@app.route('/delete_income/<int:income_id>', methods=['POST'])
def delete_income(income_id):
    try:
        income = Session.query(Income).filter_by(id=income_id).first()
        if not income:
            flash("Income not found!", "danger")
            return redirect(url_for('dashboard'))

        Session.delete(income)
        Session.commit()

        flash("Income deleted successfully!", "success")
        return redirect(url_for('dashboard'))
    except Exception as e:
        Session.rollback()
        logging.error("Error deleting income: %s", e)
        flash("An error occurred while deleting the income. Please try again.", "danger")
        return redirect(url_for('dashboard'))


@app.route('/')
def dashboard():
    try:
        # Fetch accounts and their balances
        accounts = Session.query(Account).all()

        # Fetch budgets and their balances
        budgets = Session.query(Budget).all()

        # Calculate sum of expenses (planned and unplanned) for the current month
        current_month_start = datetime(datetime.now().year, datetime.now().month, 1)
        total_expenses = Session.query(Transaction).filter(
            Transaction.nature.in_(["Planned Expense", "Unplanned Expense"]),
            Transaction.datetime >= current_month_start
        ).with_entities(func.sum(Transaction.amount)).scalar() or 0

        # Calculate sum of incomes for the current month
        total_incomes = Session.query(Transaction).filter(
            Transaction.nature == "Income",
            Transaction.datetime >= current_month_start
        ).with_entities(func.sum(Transaction.amount)).scalar() or 0

        return render_template(
            'dashboard.html',
            accounts=accounts,
            budgets=budgets,
            total_expenses=total_expenses,
            total_incomes=total_incomes
        )
    except Exception as e:
        logging.error("Error loading dashboard: %s", e)
        flash("An error occurred while loading the dashboard. Please try again later.", "danger")
        return redirect(url_for('show_transactions'))

@app.route('/delete_planned_expense/<int:expense_id>', methods=['POST'])
def delete_planned_expense(expense_id):
    try:
        planned_expense = Session.query(PlannedExpense).filter_by(id=expense_id).first()
        if not planned_expense:
            flash("Planned expense not found!", "danger")
            return redirect(url_for('show_planned_expenses'))

        # Check if the left_budget is 0
        if planned_expense.left_budget != 0:
            flash("Cannot delete planned expense as its left budget is not 0!", "danger")
            print("Cannot delete planned expense as its left budget is not 0!", "danger")
            return redirect(url_for('show_planned_expenses'))

        Session.delete(planned_expense)
        Session.commit()

        flash("Planned expense deleted successfully!", "success")
        return redirect(url_for('show_planned_expenses'))
    except Exception as e:
        Session.rollback()
        logging.error("Error deleting planned expense: %s", e)
        flash("An error occurred while deleting the planned expense. Please try again.", "danger")
        return redirect(url_for('show_planned_expenses'))

@app.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    try:
        category = Session.query(Category).filter_by(id=category_id).first()
        if not category:
            flash("Category not found!", "danger")
            return redirect(url_for('show_categories'))

        # Check if the category is used by any planned expense
        if Session.query(PlannedExpense).filter_by(category=category.name).count() > 0:
            flash("Cannot delete category as it is used by a planned expense!", "danger")
            print("Cannot delete category as it is used by a planned expense!", "danger")
            return redirect(url_for('show_categories'))

        Session.delete(category)
        Session.commit()

        flash("Category deleted successfully!", "success")
        return redirect(url_for('show_categories'))
    except Exception as e:
        Session.rollback()
        logging.error("Error deleting category: %s", e)
        flash("An error occurred while deleting the category. Please try again.", "danger")
        return redirect(url_for('show_categories'))

@app.route('/delete_budget/<int:budget_id>', methods=['POST'])
def delete_budget(budget_id):
    try:
        budget = Session.query(Budget).filter_by(id=budget_id).first()
        if not budget:
            flash("Budget not found!", "danger")
            return redirect(url_for('show_budgets'))

        # Check if the budget balance is 0
        if budget.balance != 0:
            flash("Cannot delete budget as its balance is not 0!", "danger")
            return redirect(url_for('show_budgets'))

        Session.delete(budget)
        Session.commit()

        flash("Budget deleted successfully!", "success")
        return redirect(url_for('show_budgets'))
    except Exception as e:
        Session.rollback()
        logging.error("Error deleting budget: %s", e)
        flash("An error occurred while deleting the budget. Please try again.", "danger")
        return redirect(url_for('show_budgets'))

@app.route('/delete_account/<int:account_id>', methods=['POST'])
def delete_account(account_id):
    try:
        account = Session.query(Account).filter_by(id=account_id).first()
        if not account:
            flash("Account not found!", "danger")
            return redirect(url_for('show_accounts'))

        # Check if the account balance is 0
        if account.balance != 0:
            flash("Cannot delete account as its balance is not 0!", "danger")
            return redirect(url_for('show_accounts'))

        Session.delete(account)
        Session.commit()

        flash("Account deleted successfully!", "success")
        return redirect(url_for('show_accounts'))
    except Exception as e:
        Session.rollback()
        logging.error("Error deleting account: %s", e)
        flash("An error occurred while deleting the account. Please try again.", "danger")
        return redirect(url_for('show_accounts'))

@app.route('/edit_planned_expenses', methods=['GET', 'POST'])
def edit_planned_expenses():
    if request.method == 'GET':
        # Fetch all planned expenses
        planned_expenses = Session.query(PlannedExpense).all()
        return render_template('edit_planned_expenses.html', planned_expenses=planned_expenses)

    elif request.method == 'POST':
        try:
            data = request.form
            print(f"Form data received: {data}")

            # Update each planned expense
            for expense in Session.query(PlannedExpense).all():
                # Get the new monthly budget value from the form
                new_monthly_budget_key = f"monthly_budget_{expense.id}"
                if new_monthly_budget_key in data:
                    new_monthly_budget = float(data[new_monthly_budget_key])

                    # Update the expense fields
                    expense.monthly_budget = new_monthly_budget
                    expense.consumed_budget = 0
                    expense.left_budget = new_monthly_budget

            # Commit the changes
            Session.commit()
            flash("Planned expenses updated successfully!", "success")
        except Exception as e:
            Session.rollback()
            logging.error("Error updating planned expenses: %s", e)
            flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('edit_planned_expenses'))


if __name__ == '__main__':
    app.run(debug=True)
