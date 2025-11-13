import sqlite3

# Real coordinates for hospitals in Hyderabad
hospital_coords = {
    'Kukatpally': [
        ('Apollo Hospital Kukatpally', 17.4936, 78.3995),
        ('KIMS Hospital Kukatpally', 17.4928, 78.3990),
        ('Rainbow Children\'s Hospital', 17.4942, 78.3998),
        ('Continental Hospital Kukatpally', 17.4932, 78.3985),
        ('Care Hospital Kukatpally', 17.4938, 78.3992),
    ],
    'Aziznagar': [
        ('Apollo Clinic Aziznagar', 17.2165, 78.2910),
        ('Omega Hospitals', 17.2150, 78.2890),
        ('Vijaya Hospital', 17.2145, 78.2875),
        ('Sri Sai Hospital Aziznagar', 17.2175, 78.2905),
    ],
    'Narsingi': [
        ('Continental Hospital Narsingi', 17.3897, 78.3635),
        ('Apollo Hospitals Narsingi', 17.3890, 78.3638),
        ('Shadan Hospital Narsingi', 17.3880, 78.3620),
        ('KIMS Hospital Narsingi', 17.3905, 78.3645),
    ],
    'Jubilee Hills': [
        ('Apollo Hospital Jubilee Hills', 17.3745, 78.3936),
        ('Yashoda Hospital Jubilee Hills', 17.3750, 78.3940),
        ('Care Hospital Jubilee Hills', 17.3740, 78.3930),
        ('KIMS Hospital Jubilee Hills', 17.3755, 78.3945),
    ],
    'Shamshabad': [
        ('Apollo Airport Hospital Shamshabad', 17.3700, 78.5500),
        ('Medicover Hospital Shamshabad', 17.3705, 78.5510),
        ('Aware Hospital Shamshabad', 17.3695, 78.5490),
    ]
}

conn = sqlite3.connect('healthcare.db')
cursor = conn.cursor()

print("📍 Updating hospital coordinates...\n")

updated = 0
for area, hospitals in hospital_coords.items():
    for name, lat, lon in hospitals:
        cursor.execute(
            "UPDATE hospitals SET lat=?, lon=? WHERE name=? AND area=?",
            (lat, lon, name, area)
        )
        if cursor.rowcount > 0:
            updated += 1
            print(f"✅ {name} ({area})")

conn.commit()
conn.close()

print(f"\n✅ Updated {updated} hospitals with coordinates!")
