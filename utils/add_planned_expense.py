
from model import PlannedExpense, Categorie, Session


def add_planned_expense(categorie_name, monthly_budget):
    """
    Adds a planned expense to the database.
    
    :param categorie_name: Name of the category for the planned expense
    :param monthly_budget: Budget planned for the category
    :return: None
    """
    session = Session()
    try:
        # Check if the category exists
        categorie = session.query(Categorie).filter_by(name=categorie_name).first()
        if not categorie:
            print(f"Category '{categorie_name}' not found. Please add the category first.")
            return
        
        # Calculate the left budget (initially equal to the monthly budget)
        left_budget = monthly_budget
        
        # Create a new planned expense
        planned_expense = PlannedExpense(
            categorie=categorie.name,
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
