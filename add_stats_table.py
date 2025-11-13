import sqlite3
from datetime import date

conn = sqlite3.connect('healthcare.db')

# Create the hospital_stats table if it doesn't exist
conn.execute('''
CREATE TABLE IF NOT EXISTS hospital_stats (
    hospital_id INTEGER,
    date TEXT,
    patients_visited INTEGER DEFAULT 0,
    patients_joined INTEGER DEFAULT 0,
    patients_discharged INTEGER DEFAULT 0,
    emergency_cases INTEGER DEFAULT 0,
    deaths INTEGER DEFAULT 0,
    PRIMARY KEY (hospital_id, date),
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
)
''')
print("hospital_stats table created (or already exists).")

# --- Insert a sample record for hospital_id=1 and today's date ---
today = date.today().isoformat()
hospital_id = 1  # Change this to match a hospital_id that exists in your hospitals table

# Check if a row already exists for this date/hospital
cur = conn.cursor()
cur.execute("SELECT 1 FROM hospital_stats WHERE hospital_id=? AND date=?", (hospital_id, today))
if not cur.fetchone():
    conn.execute('''
      INSERT INTO hospital_stats
        (hospital_id, date, patients_visited, patients_joined, patients_discharged, emergency_cases, deaths)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (hospital_id, today, 25, 10, 5, 2, 0))
    print(f"Sample stats row inserted for hospital_id={hospital_id} and date={today}.")
else:
    print(f"Stats record for hospital_id={hospital_id} and date={today} already exists.")

conn.commit()
conn.close()
print("Done!")
