import sqlite3

# Connect to database
conn = sqlite3.connect('healthcare.db')
cursor = conn.cursor()

# Add location columns if not exist
try:
    cursor.execute("ALTER TABLE hospitals ADD COLUMN lat REAL")
    cursor.execute("ALTER TABLE hospitals ADD COLUMN lon REAL")
    conn.commit()
    print("✅ Location columns added\n")
except sqlite3.OperationalError:
    print("ℹ️ Location columns already exist\n")

# 50 Hospitals - 10 per area with departments
hospitals_data = [
    # ==================== AZIZNAGAR (10 hospitals) ====================
    ("Omega Hospitals", "Aziznagar", "Main Road, Aziznagar, Hyderabad", "040-44556677", 17.2150, 78.2890),
    ("Mark Hospital", "Aziznagar", "Plot 25, Aziznagar, Hyderabad", "040-44667788", 17.2160, 78.2895),
    ("Dr Laxmi Vision Hospital", "Aziznagar", "Aziznagar Main Road, Hyderabad", "040-44778899", 17.2140, 78.2880),
    ("Mythri Hospital", "Aziznagar", "Near Bus Stop, Aziznagar, Hyderabad", "040-44889900", 17.2170, 78.2900),
    ("Care Medical Center", "Aziznagar", "Aziznagar Colony, Hyderabad", "040-44990011", 17.2155, 78.2885),
    ("Apollo Clinic Aziznagar", "Aziznagar", "Aziznagar Main Road, Hyderabad", "040-45001122", 17.2165, 78.2910),
    ("Vijaya Hospital", "Aziznagar", "Plot 12, Aziznagar, Hyderabad", "040-45112233", 17.2145, 78.2875),
    ("Sri Sai Hospital Aziznagar", "Aziznagar", "Aziznagar Cross Road, Hyderabad", "040-45223344", 17.2175, 78.2905),
    ("Prathima Multi Specialty Aziznagar", "Aziznagar", "Aziznagar Village, Hyderabad", "040-45334455", 17.2150, 78.2892),
    ("Medicover Hospital Aziznagar", "Aziznagar", "Main Road, Aziznagar, Hyderabad", "040-45445566", 17.2162, 78.2897),
    
    # ==================== KUKATPALLY (10 hospitals) ====================
    ("Apollo Hospital Kukatpally", "Kukatpally", "KPHB Colony, Kukatpally, Hyderabad", "040-44445678", 17.4936, 78.3995),
    ("Rainbow Children's Hospital", "Kukatpally", "KPHB, Kukatpally, Hyderabad", "040-49998888", 17.4942, 78.3998),
    ("Omni Hospital Kukatpally", "Kukatpally", "Kukatpally Main Road, Hyderabad", "040-30303030", 17.4950, 78.3980),
    ("KIMS Hospital Kukatpally", "Kukatpally", "Kondapur, Kukatpally, Hyderabad", "040-44447777", 17.4928, 78.3990),
    ("Medicover Hospital Kukatpally", "Kukatpally", "KPHB Phase 1, Hyderabad", "040-68886868", 17.4945, 78.4000),
    ("Continental Hospital Kukatpally", "Kukatpally", "Kukatpally Housing Board, Hyderabad", "040-67679999", 17.4932, 78.3985),
    ("Care Hospital Kukatpally", "Kukatpally", "KPHB Colony, Hyderabad", "040-61659999", 17.4938, 78.3992),
    ("Aware Hospital Kukatpally", "Kukatpally", "Miyapur Road, Hyderabad", "040-30217777", 17.4955, 78.4005),
    ("Lotus Hospital Kukatpally", "Kukatpally", "Bachupally, Kukatpally, Hyderabad", "040-42022222", 17.4925, 78.3978),
    ("KIMS Icon Hospital Kukatpally", "Kukatpally", "Kondapur, Hyderabad", "040-44889900", 17.4948, 78.3996),
    
    # ==================== NARSINGI (10 hospitals) ====================
    ("Continental Hospital Narsingi", "Narsingi", "IT Park Road, Narsingi, Hyderabad", "040-67678000", 17.3897, 78.3635),
    ("Astra Healthcare Narsingi", "Narsingi", "OU Colony, Narsingi, Hyderabad", "040-48523456", 17.3910, 78.3640),
    ("Shadan Hospital Narsingi", "Narsingi", "Peerancheruvu, Narsingi, Hyderabad", "040-24142020", 17.3880, 78.3620),
    ("Andani Women & Children Hospital", "Narsingi", "Narsingi Heights, Hyderabad", "040-48555566", 17.3905, 78.3645),
    ("Apollo Hospitals Narsingi", "Narsingi", "Jubilee Hills Road, Hyderabad", "040-23551234", 17.3890, 78.3638),
    ("Bhoomi Hospitals Narsingi", "Narsingi", "Narsingi Main Road, Hyderabad", "040-48666677", 17.3915, 78.3650),
    ("Prerana Hospital Narsingi", "Narsingi", "Manikonda Road, Narsingi, Hyderabad", "040-48777788", 17.3875, 78.3615),
    ("JBI Hospital Narsingi", "Narsingi", "Puppalguda, Narsingi, Hyderabad", "040-48888899", 17.3900, 78.3642),
    ("Avasa Hospital Narsingi", "Narsingi", "Narsingi Village, Hyderabad", "040-48999900", 17.3885, 78.3625),
    ("MaxCure Hospitals Narsingi", "Narsingi", "Narsingi Main Road, Hyderabad", "040-49001122", 17.3908, 78.3648),
    
    # ==================== JUBILEE HILLS (10 hospitals) ====================
    ("Apollo Hospital Jubilee Hills", "Jubilee Hills", "Jubilee Hills, Hyderabad", "040-23550000", 17.3850, 78.4420),
    ("Yashoda Hospital Jubilee Hills", "Jubilee Hills", "Raj Bhavan Road, Jubilee Hills, Hyderabad", "040-23550001", 17.3870, 78.4430),
    ("Care Hospital Jubilee Hills", "Jubilee Hills", "Jubilee Hills Main Road, Hyderabad", "040-61656565", 17.3860, 78.4425),
    ("Rainbow Hospital Jubilee Hills", "Jubilee Hills", "Jubilee Hills Area, Hyderabad", "040-44110000", 17.3880, 78.4435),
    ("Fernandez Hospital Jubilee Hills", "Jubilee Hills", "Bogulkunta, Hyderabad", "040-24403215", 17.3840, 78.4415),
    ("KIMS Hospital Jubilee Hills", "Jubilee Hills", "Minister Road, Hyderabad", "040-44885566", 17.3865, 78.4428),
    ("Continental Hospital Jubilee Hills", "Jubilee Hills", "Jubilee Hills Circle, Hyderabad", "040-67671234", 17.3855, 78.4422),
    ("Virinchi Hospital Jubilee Hills", "Jubilee Hills", "Road No 1, Jubilee Hills, Hyderabad", "040-44888999", 17.3875, 78.4432),
    ("Aware Hospital Jubilee Hills", "Jubilee Hills", "Ring Road, Jubilee Hills, Hyderabad", "040-30211111", 17.3845, 78.4418),
    ("Star Hospital Jubilee Hills", "Jubilee Hills", "Lakdikapul, Hyderabad", "040-40021111", 17.3858, 78.4426),
    
    # ==================== SHAMSHABAD (10 hospitals) ====================
    ("Apollo Airport Hospital Shamshabad", "Shamshabad", "Airport Road, Shamshabad, Hyderabad", "040-66693333", 17.2403, 78.4294),
    ("Medicover Hospital Shamshabad", "Shamshabad", "Shamshabad Main Road, Hyderabad", "040-68887777", 17.2415, 78.4300),
    ("Aware Hospital Shamshabad", "Shamshabad", "NH 44, Shamshabad, Hyderabad", "040-30219999", 17.2395, 78.4288),
    ("Continental Hospital Shamshabad", "Shamshabad", "Airport Road, Hyderabad", "040-67672222", 17.2425, 78.4305),
    ("Rainbow Hospital Shamshabad", "Shamshabad", "Shamshabad Village, Hyderabad", "040-44112222", 17.2390, 78.4285),
    ("KIMS Hospital Shamshabad", "Shamshabad", "Shamshabad, Hyderabad", "040-44885555", 17.2408, 78.4292),
    ("Sri Sai Hospital Shamshabad", "Shamshabad", "Main Road, Shamshabad, Hyderabad", "040-24567890", 17.2420, 78.4298),
    ("Care Hospital Shamshabad", "Shamshabad", "Airport Road, Hyderabad", "040-61658888", 17.2398, 78.4290),
    ("Yashoda Hospital Shamshabad", "Shamshabad", "Shamshabad, Hyderabad", "040-23889999", 17.2412, 78.4296),
    ("Virinchi Hospital Shamshabad", "Shamshabad", "NH 44, Hyderabad", "040-44887777", 17.2405, 78.4293),
]

# Department mapping for each hospital
hospital_departments = {
    # Aziznagar
    "Omega Hospitals": ["General Medicine", "Cardiology", "Orthopedics", "Emergency"],
    "Mark Hospital": ["General Medicine", "Pediatrics", "Surgery", "Radiology"],
    "Dr Laxmi Vision Hospital": ["Ophthalmology", "General Medicine", "Emergency"],
    "Mythri Hospital": ["General Medicine", "Gynecology", "Pediatrics"],
    "Care Medical Center": ["General Medicine", "Dermatology", "ENT"],
    "Apollo Clinic Aziznagar": ["General Medicine", "Cardiology", "Neurology", "Emergency"],
    "Vijaya Hospital": ["General Medicine", "Orthopedics", "Physiotherapy"],
    "Sri Sai Hospital Aziznagar": ["General Medicine", "Surgery", "ICU", "Emergency"],
    "Prathima Multi Specialty Aziznagar": ["General Medicine", "Cardiology", "Nephrology", "Dialysis"],
    "Medicover Hospital Aziznagar": ["General Medicine", "Pediatrics", "Gynecology", "Lab"],
    
    # Kukatpally
    "Apollo Hospital Kukatpally": ["General Medicine", "Cardiology", "Neurology", "Oncology", "Emergency", "ICU"],
    "Rainbow Children's Hospital": ["Pediatrics", "Neonatology", "PICU", "NICU"],
    "Omni Hospital Kukatpally": ["General Medicine", "Orthopedics", "Surgery", "Emergency"],
    "KIMS Hospital Kukatpally": ["General Medicine", "Cardiology", "Neurosurgery", "Oncology"],
    "Medicover Hospital Kukatpally": ["General Medicine", "Pediatrics", "Gynecology", "Lab"],
    "Continental Hospital Kukatpally": ["General Medicine", "Cardiology", "Neurology", "Emergency"],
    "Care Hospital Kukatpally": ["General Medicine", "Surgery", "Orthopedics", "ICU"],
    "Aware Hospital Kukatpally": ["General Medicine", "ENT", "Dermatology"],
    "Lotus Hospital Kukatpally": ["Gynecology", "Obstetrics", "Pediatrics"],
    "KIMS Icon Hospital Kukatpally": ["General Medicine", "Cardiology", "Nephrology", "Dialysis"],
    
    # Narsingi
    "Continental Hospital Narsingi": ["General Medicine", "Cardiology", "Oncology", "Neurosurgery", "Emergency"],
    "Astra Healthcare Narsingi": ["General Medicine", "Orthopedics", "Physiotherapy"],
    "Shadan Hospital Narsingi": ["General Medicine", "Surgery", "Pediatrics", "ICU"],
    "Andani Women & Children Hospital": ["Gynecology", "Obstetrics", "Pediatrics", "NICU"],
    "Apollo Hospitals Narsingi": ["General Medicine", "Cardiology", "Neurology", "Oncology", "Emergency"],
    "Bhoomi Hospitals Narsingi": ["General Medicine", "Surgery", "Orthopedics"],
    "Prerana Hospital Narsingi": ["General Medicine", "Pediatrics", "ENT"],
    "JBI Hospital Narsingi": ["General Medicine", "Dermatology", "Radiology"],
    "Avasa Hospital Narsingi": ["General Medicine", "Surgery", "Emergency"],
    "MaxCure Hospitals Narsingi": ["General Medicine", "Cardiology", "Nephrology", "Dialysis"],
    
    # Jubilee Hills
    "Apollo Hospital Jubilee Hills": ["General Medicine", "Cardiology", "Neurology", "Emergency", "ICU"],
    "Yashoda Hospital Jubilee Hills": ["General Medicine", "Cardiology", "Surgery", "Emergency"],
    "Care Hospital Jubilee Hills": ["General Medicine", "Orthopedics", "Pediatrics", "ICU"],
    "Rainbow Hospital Jubilee Hills": ["General Medicine", "Gynecology", "Pediatrics"],
    "Fernandez Hospital Jubilee Hills": ["Gynecology", "Maternity", "Pediatrics"],
    "KIMS Hospital Jubilee Hills": ["General Medicine", "Neurology", "Oncology"],
    "Continental Hospital Jubilee Hills": ["General Medicine", "Cardiology", "Emergency"],
    "Virinchi Hospital Jubilee Hills": ["General Medicine", "Surgery", "Orthopedics"],
    "Aware Hospital Jubilee Hills": ["General Medicine", "ENT", "Dermatology"],
    "Star Hospital Jubilee Hills": ["General Medicine", "Cardiology", "Lab"],
    
    # Shamshabad
    "Apollo Airport Hospital Shamshabad": ["General Medicine", "Cardiology", "Emergency", "ICU"],
    "Medicover Hospital Shamshabad": ["General Medicine", "Pediatrics", "Gynecology"],
    "Aware Hospital Shamshabad": ["General Medicine", "Surgery", "Emergency"],
    "Continental Hospital Shamshabad": ["General Medicine", "Cardiology", "Emergency"],
    "Rainbow Hospital Shamshabad": ["General Medicine", "Pediatrics", "Orthopedics"],
    "KIMS Hospital Shamshabad": ["General Medicine", "Neurology", "ICU"],
    "Sri Sai Hospital Shamshabad": ["General Medicine", "Surgery", "Emergency"],
    "Care Hospital Shamshabad": ["General Medicine", "Cardiology", "Emergency"],
    "Yashoda Hospital Shamshabad": ["General Medicine", "Surgery", "Pediatrics"],
    "Virinchi Hospital Shamshabad": ["General Medicine", "ENT", "Orthopedics"],
}

print("📊 Adding 50 hospitals with departments to database...\n")
print("=" * 70)

hospital_count = 0
department_count = 0

for name, area, address, phone, lat, lon in hospitals_data:
    try:
        # Insert hospital
        cursor.execute("""
            INSERT INTO hospitals (name, area, address, phone, lat, lon)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, area, address, phone, lat, lon))
        
        hospital_id = cursor.lastrowid
        hospital_count += 1
        
        # Insert departments
        if name in hospital_departments:
            departments = hospital_departments[name]
            for dept_name in departments:
                cursor.execute("""
                    INSERT OR IGNORE INTO departments (hospital_id, name)
                    VALUES (?, ?)
                """, (hospital_id, dept_name))
                department_count += 1
        
        print(f"✅ {hospital_count:2d}. {name}")
        print(f"    📍 {area} | 📞 {phone}")
        print(f"    🏥 Departments: {', '.join(hospital_departments.get(name, []))}\n")
        
    except sqlite3.IntegrityError as e:
        print(f"⚠️ {name} already exists, skipping...\n")
    except Exception as e:
        print(f"❌ Error adding {name}: {e}\n")

conn.commit()
conn.close()

print("=" * 70)
print(f"\n✅ Successfully added {hospital_count} hospitals!")
print(f"🏥 Total departments added: {department_count}")

# Verify
conn = sqlite3.connect('healthcare.db')
cursor = conn.cursor()

print("\n" + "=" * 70)
print("📊 Hospital count by area:")
print("-" * 70)

cursor.execute("SELECT area, COUNT(*) as count FROM hospitals GROUP BY area ORDER BY area")
for area, count in cursor.fetchall():
    print(f"  • {area:20s}: {count:2d} hospitals")

cursor.execute("SELECT COUNT(*) FROM hospitals WHERE lat IS NOT NULL")
total_with_location = cursor.fetchone()[0]

print(f"\n📍 Total hospitals with GPS location: {total_with_location}")
print(f"🏥 Total departments: {department_count}")

conn.close()
