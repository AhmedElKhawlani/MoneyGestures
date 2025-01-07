
from model import Categorie, Session


def add_category(name):
    """
    Adds a category to the database.
    
    :param name: Name of the category
    :return: None
    """
    session = Session()
    try:
        # Check if the category already exists
        existing_category = session.query(Categorie).filter_by(name=name).first()
        if existing_category:
            print(f"Category '{name}' already exists.")
            return

        # Create a new category
        category = Categorie(name=name)
        session.add(category)
        session.commit()
        print(f"Category '{name}' added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Failed to add category: {e}")
