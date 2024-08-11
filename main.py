from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Ensure the database directory exists
if not os.path.exists('db'):
    os.makedirs('db')

# Initialize the database
def init_db():
    conn = sqlite3.connect('db/water_footprint.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS water_usage
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  shower INTEGER, bath INTEGER, teeth INTEGER, shaving INTEGER,
                  handWash INTEGER, faceWash INTEGER, lawn INTEGER, carWash INTEGER,
                  pool INTEGER, waterFeatures INTEGER, dishwasher INTEGER,
                  dishHandWash INTEGER, cooking INTEGER, drinking INTEGER,
                  foodPrep INTEGER, laundry INTEGER, flush INTEGER, leaks INTEGER,
                  pets INTEGER, plants INTEGER)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calculator')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get form data
    data = request.form

    # Store data in the database
    conn = sqlite3.connect('db/water_footprint.db')
    c = conn.cursor()
    c.execute('''INSERT INTO water_usage 
                 (shower, bath, teeth, shaving, handWash, faceWash, lawn, carWash,
                  pool, waterFeatures, dishwasher, dishHandWash, cooking, drinking,
                  foodPrep, laundry, flush, leaks, pets, plants)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              tuple(data.values()))
    conn.commit()

    # Calculate user's total usage
    total_usage = sum(int(value) * 30 for value in data.values())  # Assuming all values are daily

    # Calculate averages
    c.execute('''SELECT AVG(shower), AVG(bath), AVG(teeth), AVG(shaving),
                 AVG(handWash), AVG(faceWash), AVG(lawn), AVG(carWash),
                 AVG(pool), AVG(waterFeatures), AVG(dishwasher), AVG(dishHandWash),
                 AVG(cooking), AVG(drinking), AVG(foodPrep), AVG(laundry),
                 AVG(flush), AVG(leaks), AVG(pets), AVG(plants)
                 FROM water_usage''')
    averages = c.fetchone()
    total_average_usage = sum(averages) * 30
    conn.close()

    # Prepare data for the result page
    result_data = {
        'total_average_usage': total_average_usage,
        'total_usage': total_usage,
        'user_values': data,
        'averages': averages
    }

    return render_template('result.html', **result_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)