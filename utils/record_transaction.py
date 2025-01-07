
from model import Transaction, Session

def add_transaction(description, category, nature, amount, account, budget):
    """
    Adds a transaction to the database.
    
    :param description: Description of the transaction
    :param category: Category of the transaction
    :param nature: Nature of the transaction
    :param amount: Amount of the transaction
    :param account: Associated account name
    :param budget: Associated budget name
    :return: None
    """
    session = Session()
    try:
        # Create a new transaction instance
        transaction = Transaction(
            description=description,
            category=category,
            nature=nature,
            amount=amount,
            account=account,
            budget=budget
        )
        # Add and commit the transaction to the database
        session.add(transaction)
        session.commit()
        print("Transaction added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Failed to add transaction: {e}")
