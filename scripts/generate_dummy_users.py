# scripts/generate_dummy_users.py

import os
import sys

# --- Add project root to the Python path ---
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)
# -------------------------------------------

from faker import Faker
from backend.app.database import SessionLocal
from backend.app.services import user_service
from backend.app.schemas import user_schema
from backend.app.models.user import UserRole


def generate_users(num_uploaders=5, num_upcyclers=3):
    """
    Generates and saves dummy users to the database.
    """
    db = SessionLocal()
    fake = Faker()

    print("Generating dummy users...")

    # --- Create a default Admin User ---
    admin_email = "admin@ecomorph.com"
    if not user_service.get_user_by_email(db, email=admin_email):
        admin_user = user_schema.UserCreate(
            email=admin_email,
            full_name="Admin User",
            password="password123",
            role=UserRole.ADMIN
        )
        user_service.create_user(db=db, user=admin_user)
        print(f"  Created Admin: {admin_email}")

    # --- Create Uploader Users ---
    for i in range(num_uploaders):
        email = f"uploader{i + 1}@test.com"
        if not user_service.get_user_by_email(db, email=email):
            uploader = user_schema.UserCreate(
                email=email,
                full_name=fake.name(),
                password="password123",
                role=UserRole.UPLOADER
            )
            user_service.create_user(db=db, user=uploader)
            print(f"  Created Uploader: {email}")

    # --- Create Upcycler Users ---
    for i in range(num_upcyclers):
        email = f"upcycler{i + 1}@test.com"
        if not user_service.get_user_by_email(db, email=email):
            upcycler = user_schema.UserCreate(
                email=email,
                full_name=fake.name(),
                password="password123",
                role=UserRole.UPCYCLER
            )
            user_service.create_user(db=db, user=upcycler)
            print(f"  Created Upcycler: {email}")

    db.close()
    print("\nDummy user generation complete.")


if __name__ == "__main__":
    generate_users()