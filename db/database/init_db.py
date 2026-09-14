from database.connection import create_tables, engine
from sqlalchemy import inspect


if __name__ == "__main__":
    print("Creating database tables...")

    create_tables()

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print("\nDatabase tables found:")

    for table in tables:
        print(f"- {table}")

    print("\nDatabase verification completed successfully!")