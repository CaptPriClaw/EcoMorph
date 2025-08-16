# scripts/seed_data.py

import os
import sys
import random

# --- Add project root to the Python path ---
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)
# -------------------------------------------

from faker import Faker
from backend.app.database import SessionLocal
from backend.app.services import user_service, waste_service, product_service
from backend.app.schemas import waste_schema, product_schema
from backend.app.models.user import UserRole

# --- Sample Data Definitions ---
WASTE_TYPES = ["plastic bottle", "glass jar", "old t-shirt", "newspaper", "aluminum can", "cardboard box"]
PRODUCT_IDEAS = {
    "plastic bottle": "Vertical Planter",
    "glass jar": "Candle Lantern",
    "old t-shirt": "Reusable Tote Bag",
    "newspaper": "Seedling Pot",
    "aluminum can": "Pen Holder",
    "cardboard box": "Cat Scratcher"
}
IMAGE_PLACEHOLDER = "https://via.placeholder.com/150"


def seed_database(num_waste_items=10, num_products=8):
    """
    Seeds the database with waste and product items, linking them to existing users.
    """
    db = SessionLocal()
    fake = Faker()

    print("Seeding database with waste and product data...")

    # --- 1. Fetch Existing Users ---
    all_users = user_service.get_users(db, skip=0, limit=100)
    uploaders = [u for u in all_users if u.role == UserRole.UPLOADER]
    upcyclers = [u for u in all_users if u.role == UserRole.UPCYCLER]

    if not uploaders or not upcyclers:
        print("Error: No uploader or upcycler users found. Please run generate_dummy_users.py first.")
        db.close()
        return

    # --- 2. Seed Waste Items ---
    for _ in range(num_waste_items):
        uploader = random.choice(uploaders)
        material = random.choice(WASTE_TYPES)

        waste_item = waste_schema.WasteCreate(
            material_type=material,
            description=f"A discarded {material}.",
            weight_kg=round(random.uniform(0.1, 2.0), 2),
            image_url=IMAGE_PLACEHOLDER
        )
        waste_service.create_waste(db=db, waste=waste_item, uploader_id=uploader.id)
        print(f"  Created waste item '{material}' for user {uploader.email}")

    # --- 3. Seed Product Items ---
    for _ in range(num_products):
        upcycler = random.choice(upcyclers)
        base_material = random.choice(list(PRODUCT_IDEAS.keys()))
        product_name = f"{PRODUCT_IDEAS[base_material]} from {base_material}"

        product_item = product_schema.ProductCreate(
            name=product_name,
            description=fake.paragraph(nb_sentences=3),
            image_url=IMAGE_PLACEHOLDER,
            price_points=random.randint(50, 500)
        )
        product_service.create_product(db=db, product=product_item, upcycler_id=upcycler.id)
        print(f"  Created product '{product_name}' for user {upcycler.email}")

    db.close()
    print("\nDatabase seeding complete.")


if __name__ == "__main__":
    seed_database()