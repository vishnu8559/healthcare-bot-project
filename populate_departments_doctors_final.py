import sqlite3
import random

# Open the database
conn = sqlite3.connect('healthcare.db')
conn.row_factory = sqlite3.Row

# Get all Hospital IDs
hospitals = conn.execute('SELECT hospital_id, name FROM hospitals ORDER BY hospital_id').fetchall()
hospital_ids = {h['name']: h['hospital_id'] for h in hospitals}

print(f"✅ Found {len(hospital_ids)} hospitals")
print("=" * 60)

# Define standard departments for all hospitals
standard_departments = [
    'General',
    'Emergency',
    'Cardiology',
    'Pediatrics',
    'Orthopedics',
    'Neurology',
    'Dentist',
    'ICU',
]

# Define standard doctors with their specialization
standard_doctors = [
    ('Dr. Raju', 'General', 5),
    ('Dr. Pawan', 'Emergency', 7),
    ('Dr. Kalyan', 'Dentist', 2),
    ('Dr. Bharani', 'Neurology', 1),
    ('Dr. Vinay', 'Orthopedics', 3),
    ('Dr. Ajay', 'Pediatrics', 4),
    ('Dr. Suresh', 'Cardiology', 6),
    ('Dr. Ramya', 'ICU', 2),
]

# Step 1: Add departments for ALL hospitals
dept_count = 0
for hospital_name, hospital_id in sorted(hospital_ids.items()):
    for dept_name in standard_departments:
        try:
            conn.execute(
                'INSERT INTO departments (hospital_id, name) VALUES (?, ?)',
                (hospital_id, dept_name)
            )
            dept_count += 1
        except sqlite3.IntegrityError:
            pass  # Department already exists

conn.commit()  # FIXED: Proper commit
print(f"✅ Added {dept_count} departments across {len(hospital_ids)} hospitals")

# Step 2: Get all Department IDs - FRESH QUERY
depts = conn.execute('''
    SELECT department_id, name, hospital_id 
    FROM departments 
    ORDER BY hospital_id, name
''').fetchall()

# Build proper mapping
dept_map = {}
for d in depts:
    key = (d['hospital_id'], d['name'])
    dept_map[key] = d['department_id']

print(f"✅ Found {len(dept_map)} department mappings")
print("=" * 60)

# Step 3: Add doctors for each hospital
doctor_count = 0
error_count = 0

for hospital_name, hospital_id in sorted(hospital_ids.items()):
    print(f"🏥 Adding doctors for: {hospital_name} (ID: {hospital_id})")
    
    for doctor_name, specialization, default_waiting in standard_doctors:
        # Find the corresponding department
        dept_key = (hospital_id, specialization)
        
        if dept_key not in dept_map:
            print(f"   ⚠️  Department '{specialization}' not found")
            error_count += 1
            continue
        
        dept_id = dept_map[dept_key]
        available = random.choice([0, 1])  # Random availability
        waiting_patients = default_waiting
        
        try:
            conn.execute(
                '''INSERT INTO doctors 
                (hospital_id, department_id, doctor_name, specialization, available, waiting_patients)
                VALUES (?, ?, ?, ?, ?, ?)''',
                (hospital_id, dept_id, doctor_name, specialization, available, waiting_patients)
            )
            doctor_count += 1
            status = "✅" if available else "⏳"
            print(f"   {status} {doctor_name} - {specialization}")
        except sqlite3.IntegrityError as e:
            print(f"   ❌ Error: {e}")
            error_count += 1

conn.commit()  # FIXED: Proper commit

# Step 4: Verify data
total_doctors = conn.execute('SELECT COUNT(*) as count FROM doctors').fetchone()['count']
total_departments = conn.execute('SELECT COUNT(*) as count FROM departments').fetchone()['count']

print("\n" + "=" * 60)
print("📊 FINAL SUMMARY:")
print("=" * 60)
print(f"✅ Hospitals:        {len(hospital_ids)}")
print(f"✅ Departments:      {total_departments} ({total_departments // len(hospital_ids) if hospital_ids else 0} per hospital)")
print(f"✅ Doctors Added:    {total_doctors}")
print(f"❌ Errors:           {error_count}")
print("=" * 60)

conn.close()
print("\n🎉 Done! All hospitals now have departments and doctors!")
