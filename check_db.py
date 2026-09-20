import sqlite3

db_path = "db/data/patient_case.db"

conn = sqlite3.connect(db_path)

tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
).fetchall()

print("DATABASE TABLES:")
for table in tables:
    print("-", table[0])

conn.close()