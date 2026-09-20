from database.connection import get_db
from database.crud import create_user


db = get_db()

try:
    user = create_user(
        db=db,
        username="demo_clinician",
        email="demo.clinician@example.com",
        password_hash="demo_password_hash",
        role="clinician"
    )

    print("\nUser created successfully!")
    print("Database ID:", user.id)
    print("Username:", user.username)
    print("Email:", user.email)
    print("Role:", user.role)

finally:
    db.close()