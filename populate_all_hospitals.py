import sqlite3
import random

# Open the database
conn = sqlite3.connect('healthcare.db')
conn.row_factory = sqlite3.Row

print("=" * 70)
print("🏥 ADDING DEPARTMENTS & DOCTORS TO ALL HOSPITALS (ID 1-52)")
print("=" * 70)

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

# Step 1: Add departments for hospital_id 1 to 52
dept_count = 0
print("\n📍 STEP 1: Adding Departments to all 52 hospitals...")
print("-" * 70)

for hospital_id in range(1, 53):  # 1 to 52
    added_for_this_hospital = 0
    for dept_name in standard_departments:
        try:
            conn.execute(
                'INSERT INTO departments (hospital_id, name) VALUES (?, ?)',
                (hospital_id, dept_name)
            )
            added_for_this_hospital += 1
            dept_count += 1
        except sqlite3.IntegrityError:
            pass  # Department already exists
    
    if added_for_this_hospital > 0:
        print(f"   ✅ Hospital ID {hospital_id}: {added_for_this_hospital} departments added")

conn.commit()
print(f"\n✅ Total Departments Added: {dept_count}")

# Step 2: Get all Department IDs mapping
print("\n📍 STEP 2: Building department mappings...")
print("-" * 70)

depts = conn.execute('''
    SELECT department_id, name, hospital_id 
    FROM departments 
    WHERE hospital_id BETWEEN 1 AND 52
    ORDER BY hospital_id, name
''').fetchall()

dept_map = {}
for d in depts:
    key = (d['hospital_id'], d['name'])
    dept_map[key] = d['department_id']

print(f"✅ Found {len(dept_map)} department mappings")

# Step 3: Add doctors for each hospital (1-52)
print("\n📍 STEP 3: Adding Doctors to all 52 hospitals...")
print("-" * 70)

doctor_count = 0
error_count = 0

for hospital_id in range(1, 53):  # 1 to 52
    doctors_in_this_hospital = 0
    
    for doctor_name, specialization, default_waiting in standard_doctors:
        # Find the corresponding department
        dept_key = (hospital_id, specialization)
        
        if dept_key not in dept_map:
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
            doctors_in_this_hospital += 1
        except sqlite3.IntegrityError:
            pass  # Doctor already exists
    
    if doctors_in_this_hospital > 0:
        print(f"   ✅ Hospital ID {hospital_id}: {doctors_in_this_hospital} doctors added")

conn.commit()

# Step 4: Verify data
print("\n📍 STEP 4: Verifying data...")
print("-" * 70)

total_doctors = conn.execute(
    'SELECT COUNT(*) as count FROM doctors WHERE hospital_id BETWEEN 1 AND 52'
).fetchone()['count']

total_departments = conn.execute(
    'SELECT COUNT(*) as count FROM departments WHERE hospital_id BETWEEN 1 AND 52'
).fetchone()['count']

hospitals_with_data = conn.execute(
    'SELECT DISTINCT hospital_id FROM hospitals WHERE hospital_id BETWEEN 1 AND 52'
).fetchall()

print(f"✅ Total Hospitals (1-52): {len(hospitals_with_data)}")
print(f"✅ Total Departments: {total_departments}")
print(f"✅ Total Doctors: {total_doctors}")
print(f"❌ Errors: {error_count}")

# Step 5: Summary
print("\n" + "=" * 70)
print("📊 FINAL SUMMARY:")
print("=" * 70)
print(f"✅ Hospitals Processed:      52 (ID 1-52)")
print(f"✅ Departments per Hospital: {len(standard_departments)}")
print(f"✅ Total Departments:        {total_departments}")
print(f"✅ Doctors per Hospital:     {len(standard_doctors)}")
print(f"✅ Total Doctors:            {total_doctors}")
print(f"❌ Total Errors:             {error_count}")
print("=" * 70)

# Step 6: Show sample
print("\n📋 SAMPLE DATA (Hospital ID 1):")
print("-" * 70)

doctors = conn.execute('''
    SELECT d.doctor_name, d.specialization, d.available, d.waiting_patients
    FROM doctors d
    WHERE d.hospital_id = 1
    ORDER BY d.specialization
''').fetchall()

if doctors:
    for doc in doctors:
        status = "✅" if doc['available'] else "⏳"
        print(f"  {status} {doc['doctor_name']} ({doc['specialization']}) - {doc['waiting_patients']} waiting")
else:
    print("  No doctors found")

conn.close()

print("\n🎉 ✅ SUCCESS! All 52 hospitals now have departments and doctors!")
print("=" * 70)
