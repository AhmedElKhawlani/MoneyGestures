def add_income(session, Income, name):
    """
    Adds an income source to the database.
    
    :param name: Name of the income source
    :return: None
    """
    try:
        existing_income = session.query(Income).filter_by(name=name).first()
        if existing_income:
            print(f"Income '{name}' already exists.")
            return
        income = Income(name=name)
        session.add(income)
        session.commit()
        print("Income source added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Failed to add income source: {e}")
