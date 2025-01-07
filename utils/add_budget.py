
from model import Budget, Session


def add_budget(name, initial_amount=0):
    """
    Adds a budget to the database.
    
    :param name: Name of the budget
    :param initial_amount: Initial amount of the budget
    :return: None
    """
    session = Session()
    try:
        budget = Budget(
            name=name,
            amount=initial_amount,
        )
        session.add(budget)
        session.commit()
        print("Budget added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Failed to add budget: {e}")
