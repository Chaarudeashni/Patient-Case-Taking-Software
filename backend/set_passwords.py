import bcrypt
from database.connection import SessionLocal
from database.models import User

db = SessionLocal()

try:
    users = {
        "demo_clinician": "demo_password",
        "demo_clinician_2": "demo_password"
    }

    for username, password in users.items():
        user = db.query(User).filter(User.username == username).first()

        if user:
            hashed = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            user.password_hash = hashed
            print(f"Password updated for: {username}")
        else:
            print(f"User not found: {username}")

    db.commit()
    print("Done.")

finally:
    db.close()