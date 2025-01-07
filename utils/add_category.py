
def add_category(session, Category, name):
    """
    Adds a category to the database.
    
    :param name: Name of the category
    :return: None
    """
    try:
        # Check if the category already exists
        existing_category = session.query(Category).filter_by(name=name).first()
        if existing_category:
            print(f"Category '{name}' already exists.")
            return

        # Create a new category
        category = Category(name=name)
        session.add(category)
        session.commit()
        print(f"Category '{name}' added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Failed to add category: {e}")
