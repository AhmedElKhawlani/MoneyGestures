
from model import Account, Session

def add_account(name, initial_amount=0):
    """
    Adds an account to the database.
    
    :param name: Name of the account
    :param initial_amount: Initial amount in the account
    :return: None
    """
    session = Session()
    try:
        account = Account(
            name=name,
            amount=initial_amount,
        )
        session.add(account)
        session.commit()
        print("Account added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Failed to add account: {e}")
    