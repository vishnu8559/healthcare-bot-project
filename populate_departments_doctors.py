import sqlite3

# Open the database
conn = sqlite3.connect('healthcare.db')

# Get all Hospital IDs
hospitals = conn.execute('SELECT hospital_id, name FROM hospitals').fetchall()
hospital_ids = {h[1]: h[0] for h in hospitals}

print(f"Found {len(hospital_ids)} hospitals")
print("Adding departments and doctors...")

# Define standard departments for all hospitals
standard_departments = [
    'General',
    'Fever',
    'First Aid',
    'Dentist',
    'Cardiology',
    'Neurology',
    'Orthopedics',
    'Pediatrics',
    'Emergency',
]

# Define standard doctors with their specialization
standard_doctors = [
    ('Dr. Raju', 'General'),
    ('Dr. Pawan', 'Fever'),
    ('Dr. Kalyan', 'Dentist'),
    ('Dr. Bharani', 'Neurology'),
    ('Dr. Vinay', 'Orthopedics'),
    ('Dr. Ajay', 'Pediatrics'),
    ('Dr. Suresh', 'Emergency'),
    ('Dr. Sameer', 'Cardiology'),
    ('Dr. Ramya', 'General'),
]

# Add departments for ALL hospitals
for hospital_name, hospital_id in hospital_ids.items():
    for dept_name in standard_departments:
        try:
            conn.execute(
                'INSERT INTO departments (hospital_id, name) VALUES (?, ?)',
                (hospital_id, dept_name)
            )
        except sqlite3.IntegrityError:
            # Department might already exist, skip
            pass

conn.commit()
print(f"✅ Departments added for all {len(hospital_ids)} hospitals")

# Get all Department IDs
depts = conn.execute('SELECT department_id, name, hospital_id FROM departments').fetchall()
dept_ids = {}
for d in depts:
    dept_ids[(d[2], d[1])] = d[0]

# Add doctors for each hospital
doctor_count = 0
for hospital_name, hospital_id in hospital_ids.items():
    for doctor_name, specialization in standard_doctors:
        # Find the corresponding department
        dept_key = (hospital_id, specialization)
        
        if dept_key in dept_ids:
            dept_id = dept_ids[dept_key]
            waiting_patients = [5, 0, 2, 1, 4, 3, 7, 4, 2][standard_doctors.index((doctor_name, specialization))]
            available = 1 if doctor_count % 2 == 0 else 0  # Alternate available/unavailable
            
            try:
                conn.execute(
                    '''INSERT INTO doctors 
                    (hospital_id, department_id, doctor_name, specialization, available, waiting_patients)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                    (hospital_id, dept_id, doctor_name, specialization, available, waiting_patients)
                )
                doctor_count += 1
            except sqlite3.IntegrityError:
                # Doctor might already exist, skip
                pass

conn.commit()
conn.close()

print(f"✅ {doctor_count} doctors added across all hospitals!")
print(f"✅ All {len(hospital_ids)} hospitals now have departments and doctors!")
print("\n📊 Summary:")
print(f"   - Hospitals: {len(hospital_ids)}")
print(f"   - Departments per hospital: {len(standard_departments)}")
print(f"   - Total departments: {len(hospital_ids) * len(standard_departments)}")
print(f"   - Doctors added: {doctor_count}")
