from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.sql import func
from utils.initialise_db import initialise_db

DATABASE_URL = 'mysql+pymysql://root:12040412@localhost/money_management'

# Check if the database exists, and create it if not
if not database_exists(DATABASE_URL):
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
    amount = Column(Float, nullable=False, default=0)

class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_creation = Column(DateTime, nullable=False, default=func.now())
    name = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False, default=0)

class Income(Base):
    __tablename__ = 'incomes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_creation = Column(DateTime, nullable=False, default=func.now())
    name = Column(String(50), nullable=False)

class Categorie(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_creation = Column(DateTime, nullable=False, default=func.now())
    name = Column(String(50), nullable=False)

class PlannedExpense(Base):
    __tablename__ = 'planned_expenses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    categorie = Column(String(50), nullable=False)
    monthly_budget = Column(Float, nullable=False, default=0)
    consumed_budget = Column(Float, nullable=False, default=0)
    left_budget = Column(Float, nullable=False, default=0)

# Create the tables in the database
Base.metadata.create_all(engine)
print("Tables created successfully!")

# Set up the session
Session = sessionmaker(bind=engine)
session = Session()
