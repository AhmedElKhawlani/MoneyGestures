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

            # Add the budget
            budget = Budget(
                name=data['name'].strip(),
                balance=0 
            )

            Session.add(budget)
            Session.commit()
            flash("Budget added successfully!", "success")
        except Exception as e:
            Session.rollback()
            logging.error("Error adding budget: %s", e)
            flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('budgets'))
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

            # Add the budget
            account = Account(
                name=data['name'].strip(),
                balance=0 
            )

            Session.add(account)
            Session.commit()
            flash("Account added successfully!", "success")
        except Exception as e:
            Session.rollback()
            logging.error("Error adding budget: %s", e)
            flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('accounts'))
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


if __name__ == '__main__':
    app.run(debug=True)
