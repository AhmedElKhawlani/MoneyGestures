from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.sql import func
from .add_account import add_account
from .add_budget import add_budget
from .add_category import add_category
from .add_income import add_income
from .add_planned_expense import add_planned_expense

DATABASE_URL = 'mysql+pymysql://ahmedandamin:ahmedandamin@localhost/money_management'

populate = False
# Check if the database exists, and create it if not
if not database_exists(DATABASE_URL):
    populate = True
    create_database(DATABASE_URL)
    print(f"Database 'money_management' created successfully!")

# Set up the engine
engine = create_engine(DATABASE_URL)

# Define the base for ORM models
Base = declarative_base()

# Define the Transaction model
class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False, default=func.now())
    description = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    nature = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    account = Column(String(50), nullable=False)
    budget = Column(String(255), nullable=False)

class Budget(Base):
    __tablename__ = 'budgets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_creation = Column(DateTime, nullable=False, default=func.now())
    name = Column(String(50), nullable=False)
    balance = Column(Float, nullable=False, default=0)

class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_creation = Column(DateTime, nullable=False, default=func.now())
    name = Column(String(50), nullable=False)
    balance = Column(Float, nullable=False, default=0)

class Income(Base):
    __tablename__ = 'incomes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_creation = Column(DateTime, nullable=False, default=func.now())
    name = Column(String(50), nullable=False)

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_creation = Column(DateTime, nullable=False, default=func.now())
    name = Column(String(50), nullable=False)

class PlannedExpense(Base):
    __tablename__ = 'planned_expenses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(50), nullable=False)
    monthly_budget = Column(Float, nullable=False, default=0)
    consumed_budget = Column(Float, nullable=False, default=0)
    left_budget = Column(Float, nullable=False, default=0)



# Set up the session
Session = sessionmaker(bind=engine)
session = Session()

if populate:
    Base.metadata.create_all(engine)
    print("Tables created successfully!")

    add_account(session, Account, "Bank")
    add_account(session, Account, "Cash")

    add_budget(session, Budget, "Planned Expense Budget")

    add_category(session, Category, "Food Expense")
    add_category(session, Category, "Home Expense")
    add_category(session, Category, "Health Expense")
    add_category(session, Category, "Car Expense")
    add_category(session, Category, "Bills")

    add_income(session, Income, "Salary")
    add_income(session, Income, "Other")

    add_planned_expense(session, Category, PlannedExpense, "Food Expense", 2000)
    add_planned_expense(session, Category, PlannedExpense, "Home Expense", 1000)
    add_planned_expense(session, Category, PlannedExpense, "Health Expense", 500)
    add_planned_expense(session, Category, PlannedExpense, "Car Expense", 500)
    add_planned_expense(session, Category, PlannedExpense, "Bills", 700)