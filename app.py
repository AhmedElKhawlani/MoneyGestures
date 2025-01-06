from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
from model import Transaction, Budget, engine
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

@app.route('/transactions', methods=['GET'])
def transactions():
    try:
        transactions = Session.query(Transaction).all()
        return render_template('transactions.html', transactions=transactions)
    except Exception as e:
        logging.error("Error fetching transactions: %s", e)
        flash("An error occurred while loading transactions. Please try again later.", "danger")
        return redirect(url_for('transactions'))

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        try:
            data = request.form
            print(f"Form data received: {data}")
            # Validate form data
            required_fields = ['description', 'category', 'nature', 'amount', 'account', 'budget']
            print(data)
            for field in required_fields:
                if (not field in data) or (not data[field].strip()):
                    flash("All fields are required!", "danger")
                    return redirect(url_for('add_transaction'))

            # Parse and validate specific fields
            try:
                amount = float(data['amount'])
            except ValueError as e:
                flash("Invalid date/time or amount format!", "danger")
                print(f"Parsing error: {e}")
                return redirect(url_for('add_transaction'))
            
            
            # Add the transaction
            transaction = Transaction(
                description=data['description'].strip(),
                category=data['category'].strip(),
                nature=data['nature'].strip(),
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
        return redirect(url_for('transactions'))
    return render_template('add_transaction.html')


@app.route('/budgets', methods=['GET'])
def budgets():
    try:
        budgets = Session.query(Budget).all()
        return render_template('budgets.html', budgets=budgets)
    except Exception as e:
        logging.error("Error fetching budgets: %s", e)
        flash("An error occurred while loading budgets. Please try again later.", "danger")
        return redirect(url_for('budgets'))

@app.route('/add_budget', methods=['GET', 'POST'])
def add_budget():
    if request.method == 'POST':
        try:
            data = request.form
            print(f"Form data received: {data}")

            # Validate form data
            required_fields = ['name', 'initial_amount']
            for field in required_fields:
                if not data.get(field) or not data[field].strip():
                    flash("All fields are required!", "danger")
                    return redirect(url_for('add_budget'))

            # Parse and validate specific fields
            try:
                initial_amount = float(data['initial_amount'])
            except ValueError:
                flash("Invalid amount format!", "danger")
                return redirect(url_for('add_budget'))

            # Add the budget
            budget = Budget(
                name=data['name'].strip(),
                initial_amount=initial_amount,
                actual_amount=0  # Default value for actual_amount
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

if __name__ == '__main__':
    app.run(debug=True)
