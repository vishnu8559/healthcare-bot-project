# Create file: add_location_columns.py

import sqlite3

conn = sqlite3.connect('healthcare.db')
cursor = conn.cursor()

print("🔧 Adding location columns to hospitals table...\n")

try:
    cursor.execute("ALTER TABLE hospitals ADD COLUMN lat REAL")
    print("✅ Added 'lat' column")
except sqlite3.OperationalError as e:
    print(f"ℹ️ lat column already exists: {e}")

try:
    cursor.execute("ALTER TABLE hospitals ADD COLUMN lon REAL")
    print("✅ Added 'lon' column")
except sqlite3.OperationalError as e:
    print(f"ℹ️ lon column already exists: {e}")

conn.commit()
conn.close()

print("\n✅ Database updated!")
