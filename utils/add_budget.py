
def add_budget(session, Budget, name, initial_amount=0):
    """
    Adds a budget to the database.
    
    :param name: Name of the budget
    :param initial_amount: Initial amount of the budget
    :return: None
    """
    try:
        existing_budget = session.query(Budget).filter_by(name=name).first()
        if existing_budget:
            print(f"Budget'{name}' already exists.")
            return
        budget = Budget(
            name=name,
            balance=initial_amount,
        )
        session.add(budget)
        session.commit()
        print("Budget added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Failed to add budget: {e}")
