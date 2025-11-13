import sqlite3

conn = sqlite3.connect('healthcare.db')

# Hospitals with area
conn.execute('''
CREATE TABLE IF NOT EXISTS hospitals (
    hospital_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    area TEXT,
    address TEXT,
    phone TEXT,
    receptionist_phone TEXT,
    ambulance_available BOOLEAN,
    emergency_services BOOLEAN
)
''')

# Departments linked to hospital
conn.execute('''
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_id INTEGER,
    name TEXT,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
)
''')

# Doctors linked to hospital and department
conn.execute('''
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_id INTEGER,
    department_id INTEGER,
    doctor_name TEXT,
    specialization TEXT,
    available BOOLEAN,
    waiting_patients INTEGER,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
)
''')\

# Daily hospital stats table
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


conn.commit()
conn.close()
print("DB ready")
