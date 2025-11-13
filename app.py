from flask import Flask, request, render_template, redirect, url_for, jsonify, flash
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DB = 'healthcare.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# ==================== HOSPITALS MANAGEMENT ====================

@app.route('/admin/hospitals')
def list_hospitals():
    """List all hospitals with edit/delete options"""
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    
    # Select hospital_id, name, area, address, phone, lat, lon
    cursor.execute("SELECT hospital_id, name, area, address, phone, lat, lon FROM hospitals ORDER BY area, name")
    hospitals = cursor.fetchall()
    conn.close()
    
    return render_template('hospitals_list.html', hospitals=hospitals)

@app.route('/admin/hospital/<int:hospital_id>/edit', methods=['GET', 'POST'])
def edit_hospital(hospital_id):
    """Edit a hospital with lat/lon support"""
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        area = request.form.get('area')
        address = request.form.get('address')
        phone = request.form.get('phone')
        lat = request.form.get('lat')
        lon = request.form.get('lon')
        
        # Validate
        if not name or not area:
            conn.close()
            return "Name and Area are required!", 400
        
        # Convert lat/lon to float
        try:
            lat = float(lat) if lat else None
            lon = float(lon) if lon else None
        except ValueError:
            lat = None
            lon = None
        
        # Update hospital
        cursor.execute("""
            UPDATE hospitals 
            SET name=?, area=?, address=?, phone=?, lat=?, lon=?
            WHERE hospital_id=?
        """, (name, area, address, phone, lat, lon, hospital_id))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('list_hospitals'))
    
    # GET request - show edit form
    cursor.execute("SELECT hospital_id, name, area, address, phone, lat, lon FROM hospitals WHERE hospital_id=?", (hospital_id,))
    hospital = cursor.fetchone()
    conn.close()
    
    if not hospital:
        return "Hospital not found", 404
    
    return render_template('edit_hospital.html', hospital=hospital)

@app.route('/admin/hospital/<int:hospital_id>/delete', methods=['GET'])
def delete_hospital(hospital_id):
    """Delete a hospital"""
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM hospitals WHERE hospital_id=?", (hospital_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('list_hospitals'))

@app.route('/admin/hospitals/add', methods=['GET', 'POST'])
def add_hospital():
    """Add a new hospital"""
    if request.method == 'POST':
        data = request.form
        conn = get_db()
        conn.execute('''INSERT INTO hospitals 
            (name, area, address, phone, receptionist_phone, ambulance_available, emergency_services)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (data['name'], data['area'], data['address'], data['phone'], data['receptionist_phone'],
             int('ambulance_available' in data), int('emergency_services' in data)))
        conn.commit()
        conn.close()
        return redirect(url_for('list_hospitals'))
    return render_template('add_hospital.html')

# ==================== DEPARTMENTS ====================

@app.route('/admin/departments', methods=['GET', 'POST'])
def manage_departments():
    """Manage hospital departments"""
    conn = get_db()
    if request.method == 'POST':
        hospital_id = request.form['hospital_id']
        name = request.form['name']
        conn.execute('INSERT INTO departments (hospital_id, name) VALUES (?, ?)', (hospital_id, name))
        conn.commit()
    hospitals = conn.execute('SELECT hospital_id, name FROM hospitals').fetchall()
    departments = conn.execute('SELECT d.department_id, d.name, h.name as hospital_name FROM departments d JOIN hospitals h ON d.hospital_id = h.hospital_id').fetchall()
    conn.close()
    return render_template('departments.html', hospitals=hospitals, departments=departments)

# ==================== DOCTORS ====================

@app.route('/admin/doctors', methods=['GET', 'POST'])
def manage_doctors():
    """Manage hospital doctors"""
    conn = get_db()
    if request.method == 'POST':
        hospital_id = request.form['hospital_id']
        department_id = request.form['department_id']
        doctor_name = request.form['doctor_name']
        specialization = request.form['specialization']
        available = int('available' in request.form)
        waiting_patients = int(request.form['waiting_patients'] or 0)
        conn.execute('''
            INSERT INTO doctors (hospital_id, department_id, doctor_name, specialization, available, waiting_patients)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (hospital_id, department_id, doctor_name, specialization, available, waiting_patients))
        conn.commit()

    hospitals = conn.execute('SELECT hospital_id, name FROM hospitals').fetchall()
    departments = conn.execute('SELECT department_id, name FROM departments').fetchall()
    doctors = conn.execute('''
        SELECT d.doctor_id, d.doctor_name, d.specialization, d.available, d.waiting_patients,
               h.name as hospital_name, dep.name as department_name
        FROM doctors d
        JOIN hospitals h ON d.hospital_id = h.hospital_id
        JOIN departments dep ON d.department_id = dep.department_id
    ''').fetchall()
    conn.close()
    return render_template('doctors.html', hospitals=hospitals, departments=departments, doctors=doctors)

# ==================== PUBLIC HOSPITAL PAGES ====================

@app.route('/hospital/<int:hospital_id>')
def hospital_page(hospital_id):
    """View specific hospital details"""
    conn = get_db()
    hospital = conn.execute('SELECT * FROM hospitals WHERE hospital_id=?', (hospital_id,)).fetchone()
    departments = conn.execute('SELECT * FROM departments WHERE hospital_id=?', (hospital_id,)).fetchall()
    doctors = conn.execute('''
        SELECT d.doctor_id, d.doctor_name, d.specialization, d.available, d.waiting_patients, dep.name as department_name
        FROM doctors d
        JOIN departments dep ON d.department_id = dep.department_id
        WHERE d.hospital_id=?
    ''', (hospital_id,)).fetchall()
    conn.close()
    if hospital is None:
        return "Hospital not found", 404
    return render_template('hospital_detail.html', hospital=hospital, departments=departments, doctors=doctors)

@app.route('/hospital/<int:hospital_id>/update', methods=['GET', 'POST'])
def update_hospital_doctors(hospital_id):
    """Update hospital statistics"""
    today = date.today().isoformat()
    conn = get_db()

    if request.method == 'POST':
        # Get updated stats from form
        patients_visited = request.form.get('patients_visited', 0)
        patients_joined = request.form.get('patients_joined', 0)
        patients_discharged = request.form.get('patients_discharged', 0)
        emergency_cases = request.form.get('emergency_cases', 0)
        deaths = request.form.get('deaths', 0)
        # Upsert the stats
        conn.execute('''
            INSERT OR REPLACE INTO hospital_stats
            (hospital_id, date, patients_visited, patients_joined, patients_discharged, emergency_cases, deaths)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (hospital_id, today, patients_visited, patients_joined, patients_discharged, emergency_cases, deaths))
        conn.commit()

    hospital = conn.execute('SELECT * FROM hospitals WHERE hospital_id=?', (hospital_id,)).fetchone()
    if not hospital:
        conn.close()
        return "Hospital not found", 404

    departments = conn.execute('SELECT * FROM departments WHERE hospital_id=?', (hospital_id,)).fetchall()
    doctors = conn.execute('''
        SELECT d.doctor_id, d.doctor_name, d.specialization, d.available, d.waiting_patients, dep.name as department_name
        FROM doctors d
        JOIN departments dep ON d.department_id = dep.department_id
        WHERE d.hospital_id=?
        ORDER BY dep.name, d.doctor_name
    ''', (hospital_id,)).fetchall()

    stats = conn.execute('SELECT * FROM hospital_stats WHERE hospital_id=? AND date=?', (hospital_id, today)).fetchone()
    conn.close()
    if not stats:
        stats = {
            'patients_visited': 0,
            'patients_joined': 0,
            'patients_discharged': 0,
            'emergency_cases': 0,
            'deaths': 0
        }

    return render_template('hospital_update.html', hospital=hospital, departments=departments, doctors=doctors, stats=stats)

# ==================== API ENDPOINTS ====================

@app.route('/api/hospitals')
def api_hospitals():
    """Get all hospitals as JSON"""
    conn = get_db()
    hospitals = conn.execute('SELECT * FROM hospitals').fetchall()
    conn.close()
    return jsonify([dict(h) for h in hospitals])

@app.route('/api/hospital/<int:hospital_id>/doctors')
def api_hospital_doctors(hospital_id):
    """Get doctors for a specific hospital"""
    conn = get_db()
    doctors = conn.execute('''
        SELECT d.doctor_id, d.doctor_name, d.specialization, d.available, d.waiting_patients, dep.name as department_name
        FROM doctors d
        JOIN departments dep ON d.department_id = dep.department_id
        WHERE d.hospital_id=?
        ORDER BY dep.name, d.doctor_name
    ''', (hospital_id,)).fetchall()
    conn.close()
    return jsonify([
        {
            'doctor_id': d['doctor_id'],
            'doctor_name': d['doctor_name'],
            'specialization': d['specialization'],
            'department_name': d['department_name'],
            'available': d['available'],
            'waiting_patients': d['waiting_patients']
        }
        for d in doctors
    ])

@app.route('/api/doctor_update', methods=['POST'])
def api_doctor_update():
    """Update doctor availability and waiting patients"""
    data = request.get_json()
    doctor_id = data['doctor_id']
    available = int(data['available'])
    waiting_patients = int(data['waiting_patients'])
    conn = get_db()
    conn.execute('UPDATE doctors SET available=?, waiting_patients=? WHERE doctor_id=?',
                 (available, waiting_patients, doctor_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

# if __name__ == '__main__':
#     app.run(debug=True)



if __name__ == '__main__':
       import os
       port = int(os.environ.get('PORT', 5000))
       app.run(host='0.0.0.0', port=port, debug=False)