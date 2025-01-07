from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..model import Categorie

# Database connection URL
DATABASE_URL = 'mysql+pymysql://root:12040412@localhost/money_management'

# Set up the engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

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
    finally:
        session.close()
