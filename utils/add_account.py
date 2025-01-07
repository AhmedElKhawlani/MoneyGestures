def add_account(session, Account, name, initial_amount=0):
    """
    Adds an account to the database.
    
    :param name: Name of the account
    :param initial_amount: Initial amount in the account
    :return: None
    """
    # Check if the category already exists
    
    try:
        existing_account = session.query(Account).filter_by(name=name).first()
        if existing_account:
            print(f"Account '{name}' already exists.")
            return
        
        account = Account(
            name=name,
            balance=initial_amount,
        )
        session.add(account)
        session.commit()
        print("Account added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Failed to add account: {e}")
    