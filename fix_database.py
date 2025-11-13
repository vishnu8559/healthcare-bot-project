import sqlite3

conn = sqlite3.connect('healthcare.db')
cursor = conn.cursor()

print("🔧 Fixing database structure...\n")

# Add missing columns if they don't exist
columns_to_add = [
    ("area", "TEXT"),
    ("address", "TEXT"),
    ("phone", "TEXT"),
    ("lat", "REAL"),
    ("lon", "REAL")
]

for col_name, col_type in columns_to_add:
    try:
        cursor.execute(f"ALTER TABLE hospitals ADD COLUMN {col_name} {col_type}")
        conn.commit()
        print(f"✅ Added column: {col_name}")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print(f"ℹ️ Column '{col_name}' already exists")
        else:
            print(f"❌ Error: {e}")

print("\n✅ Database structure fixed!")
conn.close()
