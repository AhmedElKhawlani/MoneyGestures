
from model import Income, Session


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
