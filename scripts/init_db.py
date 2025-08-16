# scripts/init_db.py

import os
import sys

# --- Add project root to the Python path ---
# This allows us to import from the 'app' module.
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)
# -------------------------------------------

from backend.app.database import Base, engine
# We need to import all the models so that Base knows about them
from backend.app.models import user, waste, product, transaction, points


def initialize_database():
    """
    Drops all existing tables (if any) and creates new ones based on the models.
    Use with caution in a production environment.
    """
    print("Initializing database...")

    # The 'bind=engine' part tells SQLAlchemy which database to connect to.
    # Base.metadata.create_all looks at all classes that inherit from Base
    # and creates corresponding tables in the database.
    try:
        # For development, it can be useful to drop tables first for a clean slate.
        # In a real production scenario, you would use migrations instead.
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)

        print("Creating all tables...")
        Base.metadata.create_all(bind=engine)
        print("Database initialized successfully. Tables are created.")
    except Exception as e:
        print(f"An error occurred during database initialization: {e}")


if __name__ == "__main__":
    initialize_database()