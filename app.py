from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

app = Flask(__name__)

db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='root',  # Change this
    database='DBMSPROJECT11'
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/park', methods=['GET', 'POST'])
def park():
    if request.method == 'POST':
        reg = request.form['reg_number']
        owner = request.form['owner_name']
        v_type = request.form['vehicle_type']

        cursor.execute("INSERT INTO Vehicles (registration_number, vehicle_type, owner_name) VALUES (%s, %s, %s)", (reg, v_type, owner))
        db.commit()

        cursor.execute("SELECT space_id FROM ParkingSpaces WHERE is_occupied = 0 LIMIT 1")
        space = cursor.fetchone()
        if not space:
            return "No space available"
        space_id = space[0]

        cursor.execute("UPDATE ParkingSpaces SET is_occupied = 1 WHERE space_id = %s", (space_id,))
        entry_time = datetime.now()
        cursor.execute("SELECT vehicle_id FROM Vehicles WHERE registration_number = %s", (reg,))
        vehicle_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO ParkingRecords (vehicle_id, space_id, entry_time) VALUES (%s, %s, %s)", (vehicle_id, space_id, entry_time))
        db.commit()
        return redirect('/view')
    return render_template('park.html')

@app.route('/exit', methods=['GET', 'POST'])
def vehicle_exit():
    if request.method == 'POST':
        reg = request.form['reg_number']
        cursor.execute("SELECT vehicle_id FROM Vehicles WHERE registration_number = %s", (reg,))
        vehicle = cursor.fetchone()
        if not vehicle:
            return "Vehicle not found."
        vehicle_id = vehicle[0]

        cursor.execute("SELECT record_id, space_id, entry_time FROM ParkingRecords WHERE vehicle_id = %s AND exit_time IS NULL", (vehicle_id,))
        record = cursor.fetchone()
        if not record:
            return "Vehicle is not currently parked."
        record_id, space_id, entry_time = record

        exit_time = datetime.now()
        duration = int((exit_time - entry_time).total_seconds())
        amount = duration * 0.10  # ₹0.10 per second

        cursor.execute("UPDATE ParkingSpaces SET is_occupied = 0 WHERE space_id = %s", (space_id,))
        cursor.execute("UPDATE ParkingRecords SET exit_time = %s, total_parking_duration = %s WHERE record_id = %s", (exit_time, duration, record_id))
        cursor.execute("INSERT INTO PaymentRecords (record_id, payment_amount, payment_time) VALUES (%s, %s, %s)", (record_id, amount, exit_time))
        db.commit()
        return f"Vehicle exited. Total time: {duration}s. Payment: ₹{round(amount,2)}"
    return render_template('exit.html')

@app.route('/view')
def view():
    cursor.execute("""
        SELECT v.registration_number, v.owner_name, v.vehicle_type, p.space_id, r.entry_time
        FROM Vehicles v
        JOIN ParkingRecords r ON v.vehicle_id = r.vehicle_id
        JOIN ParkingSpaces p ON p.space_id = r.space_id
        WHERE r.exit_time IS NULL
    """)
    vehicles = cursor.fetchall()
    return render_template('view.html', vehicles=vehicles)

@app.route('/reset')
def reset():
    cursor.execute("UPDATE ParkingSpaces SET is_occupied = 0")
    db.commit()
    return "All parking spaces have been reset."

if __name__ == '__main__':
    app.run(debug=True)
