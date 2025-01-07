def add_planned_expense(session, Category, PlannedExpense, category_name, monthly_budget):
    """
    Adds a planned expense to the database.
    
    :param session: SQLAlchemy session object
    :param Category: SQLAlchemy model for the category
    :param PlannedExpense: SQLAlchemy model for the planned expense
    :param category_name: Name of the category for the planned expense
    :param monthly_budget: Budget planned for the category
    :return: None
    """

    try:
        # Check if the category exists in the Category table
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            print(f"Category '{category_name}' not found. Please add the category first.")
            return

        # Check if the category already exists in the PlannedExpense table
        existing_expense = session.query(PlannedExpense).filter_by(category=category.name).first()
        if existing_expense:
            print(f"Planned expense for category '{category_name}' already exists.")
            return

        # Calculate the left budget (initially equal to the monthly budget)
        left_budget = monthly_budget

        # Create a new planned expense
        planned_expense = PlannedExpense(
            category=category.name,
            monthly_budget=monthly_budget,
            consumed_budget=0,
            left_budget=left_budget
        )
        session.add(planned_expense)
        session.commit()
        print("Planned expense added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Failed to add planned expense: {e}")
