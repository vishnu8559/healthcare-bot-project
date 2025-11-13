import sqlite3

# Open the database
conn = sqlite3.connect('healthcare.db')

# Get Hospital IDs
hospitals = conn.execute('SELECT hospital_id, name FROM hospitals').fetchall()
hospital_ids = {h[1]: h[0] for h in hospitals}

# Add Departments
departments = [
    # Nikhil Hospital departments
    (hospital_ids['Nikhil Hospital'], 'Fever'),
    (hospital_ids['Nikhil Hospital'], 'General'),
    (hospital_ids['Nikhil Hospital'], 'First Aid'),
    (hospital_ids['Nikhil Hospital'], 'Dentist'),
    (hospital_ids['Nikhil Hospital'], 'Bone Doctor'),
    (hospital_ids['Nikhil Hospital'], 'Neurologist'),
    # SRI CHAKRA departments
    (hospital_ids['SRI CHAKRA SUPER SPECIALITY HOSPITAL'], 'Emergency'),
    (hospital_ids['SRI CHAKRA SUPER SPECIALITY HOSPITAL'], 'ICU'),
    (hospital_ids['SRI CHAKRA SUPER SPECIALITY HOSPITAL'], 'Pediatrics'),
    (hospital_ids['SRI CHAKRA SUPER SPECIALITY HOSPITAL'], 'Cardiology'),
    (hospital_ids['SRI CHAKRA SUPER SPECIALITY HOSPITAL'], 'General Surgery'),
]

for hosp_id, dept_name in departments:
    conn.execute('INSERT INTO departments (hospital_id, name) VALUES (?, ?)', (hosp_id, dept_name))

conn.commit()

# Get Department IDs
depts = conn.execute('SELECT department_id, name, hospital_id FROM departments').fetchall()
dept_ids = {}
for d in depts:
    dept_ids[(d[2], d[1])] = d[0]

# Add Doctors to Nikhil Hospital
conn.execute('''INSERT INTO doctors (hospital_id, department_id, doctor_name, specialization, available, waiting_patients) VALUES
    (?, ?, ?, ?, ?, ?)''', (hospital_ids['Nikhil Hospital'], dept_ids[(hospital_ids['Nikhil Hospital'], 'General')], 'Raju', 'General', 1, 5))
conn.execute('''INSERT INTO doctors (hospital_id, department_id, doctor_name, specialization, available, waiting_patients) VALUES
    (?, ?, ?, ?, ?, ?)''', (hospital_ids['Nikhil Hospital'], dept_ids[(hospital_ids['Nikhil Hospital'], 'Fever')], 'Pawan', 'Fever', 0, 0))
conn.execute('''INSERT INTO doctors (hospital_id, department_id, doctor_name, specialization, available, waiting_patients) VALUES
    (?, ?, ?, ?, ?, ?)''', (hospital_ids['Nikhil Hospital'], dept_ids[(hospital_ids['Nikhil Hospital'], 'Dentist')], 'Kalyan', 'Dentist', 1, 2))
conn.execute('''INSERT INTO doctors (hospital_id, department_id, doctor_name, specialization, available, waiting_patients) VALUES
    (?, ?, ?, ?, ?, ?)''', (hospital_ids['Nikhil Hospital'], dept_ids[(hospital_ids['Nikhil Hospital'], 'Neurologist')], 'Bharani', 'Neurologist', 1, 1))
conn.execute('''INSERT INTO doctors (hospital_id, department_id, doctor_name, specialization, available, waiting_patients) VALUES
    (?, ?, ?, ?, ?, ?)''', (hospital_ids['Nikhil Hospital'], dept_ids[(hospital_ids['Nikhil Hospital'], 'Bone Doctor')], 'Vinay', 'Bone Doctor', 0, 0))

# Add Doctors to SRI CHAKRA SUPER SPECIALITY HOSPITAL
conn.execute('''INSERT INTO doctors (hospital_id, department_id, doctor_name, specialization, available, waiting_patients) VALUES
    (?, ?, ?, ?, ?, ?)''', (hospital_ids['SRI CHAKRA SUPER SPECIALITY HOSPITAL'], dept_ids[(hospital_ids['SRI CHAKRA SUPER SPECIALITY HOSPITAL'], 'Pediatrics')], 'Ajay', 'Pediatrics', 1, 3))
conn.execute('''INSERT INTO doctors (hospital_id, department_id, doctor_name, specialization, available, waiting_patients) VALUES
    (?, ?, ?, ?, ?, ?)''', (hospital_ids['SRI CHAKRA SUPER SPECIALITY HOSPITAL'], dept_ids[(hospital_ids['SRI CHAKRA SUPER SPECIALITY HOSPITAL'], 'Emergency')], 'Suresh', 'Emergency', 1, 7))
conn.execute('''INSERT INTO doctors (hospital_id, department_id, doctor_name, specialization, available, waiting_patients) VALUES
    (?, ?, ?, ?, ?, ?)''', (hospital_ids['SRI CHAKRA SUPER SPECIALITY HOSPITAL'], dept_ids[(hospital_ids['SRI CHAKRA SUPER SPECIALITY HOSPITAL'], 'ICU')], 'Ramya', 'ICU', 0, 0))
conn.execute('''INSERT INTO doctors (hospital_id, department_id, doctor_name, specialization, available, waiting_patients) VALUES
    (?, ?, ?, ?, ?, ?)''', (hospital_ids['SRI CHAKRA SUPER SPECIALITY HOSPITAL'], dept_ids[(hospital_ids['SRI CHAKRA SUPER SPECIALITY HOSPITAL'], 'Cardiology')], 'Sameer', 'Cardiology', 1, 4))
conn.execute('''INSERT INTO doctors (hospital_id, department_id, doctor_name, specialization, available, waiting_patients) VALUES
    (?, ?, ?, ?, ?, ?)''', (hospital_ids['SRI CHAKRA SUPER SPECIALITY HOSPITAL'], dept_ids[(hospital_ids['SRI CHAKRA SUPER SPECIALITY HOSPITAL'], 'General Surgery')], 'Ravi', 'General Surgery', 0, 0))

conn.commit()
conn.close()
print("Sample departments and doctors added!")
