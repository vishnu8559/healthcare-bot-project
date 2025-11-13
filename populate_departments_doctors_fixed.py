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
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO departments (hospital_id, name) VALUES (?, ?)',
                (hospital_id, dept_name)
            )
            dept_count += 1
        except sqlite3.IntegrityError as e:
            pass  # Department already exists

conn.commit()
print(f"✅ Added {dept_count} departments across {len(hospital_ids)} hospitals")

# Step 2: Get all Department IDs - FRESH QUERY
conn.execute('COMMIT')  # Make sure all data is committed
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

# Step 3: Add doctors for each hospital
doctor_count = 0
error_count = 0

for hospital_name, hospital_id in sorted(hospital_ids.items()):
    print(f"\n🏥 Adding doctors for: {hospital_name} (ID: {hospital_id})")
    
    for doctor_name, specialization, default_waiting in standard_doctors:
        # Find the corresponding department
        dept_key = (hospital_id, specialization)
        
        if dept_key not in dept_map:
            print(f"   ⚠️  Department '{specialization}' not found for hospital {hospital_id}")
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
            print(f"   ❌ Error adding {doctor_name}: {e}")
            error_count += 1

conn.commit()

# Step 4: Verify data
total_doctors = conn.execute('SELECT COUNT(*) as count FROM doctors').fetchone()['count']
total_departments = conn.execute('SELECT COUNT(*) as count FROM departments').fetchone()['count']

print("\n" + "=" * 60)
print("📊 FINAL SUMMARY:")
print("=" * 60)
print(f"✅ Hospitals:        {len(hospital_ids)}")
print(f"✅ Departments:      {total_departments} ({total_departments // len(hospital_ids) if hospital_ids else 0} per hospital)")
print(f"✅ Doctors Added:    {doctor_count}")
print(f"❌ Errors:           {error_count}")
print("=" * 60)

# Show sample data
print("\n📋 SAMPLE DATA (First Hospital):")
if hospital_ids:
    first_hospital_id = list(hospital_ids.values())[0]
    doctors = conn.execute('''
        SELECT d.doctor_name, d.specialization, d.available, d.waiting_patients, dp.name as dept_name
        FROM doctors d
        JOIN departments dp ON d.department_id = dp.department_id
        WHERE d.hospital_id = ?
        LIMIT 5
    ''', (first_hospital_id,)).fetchall()
    
    print(f"\nDoctors in first hospital:")
    for doc in doctors:
        status = "✅" if doc['available'] else "⏳"
        print(f"  {status} {doc['doctor_name']} - {doc['specialization']} ({doc['waiting_patients']} waiting)")

conn.close()
print("\n🎉 Done!")
