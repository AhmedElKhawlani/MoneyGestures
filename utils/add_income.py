from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..model import Income  # Import the Income model

# Database connection URL
DATABASE_URL = 'mysql+pymysql://root:12040412@localhost/money_management'

# Set up the engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def add_income(name):
    """
    Adds an income source to the database.
    
    :param name: Name of the income source
    :return: None
    """
    session = Session()
    try:
        income = Income(name=name)
        session.add(income)
        session.commit()
        print("Income source added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Failed to add income source: {e}")
    finally:
        session.close()
