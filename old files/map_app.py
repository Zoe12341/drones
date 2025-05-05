from flask import Flask, jsonify, render_template
import psycopg2

app = Flask(__name__)

def get_flight_data():
    conn = psycopg2.connect(
        dbname='drone_data',
        user='caseymacgibbon',
        password='your_password',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT professional_name, lat, lon, sequence
        FROM professional_coordinates
        ORDER BY professional_name, sequence;
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()

    # Organize data into flight paths
    flights = {}
    for name, lat, lon, seq in data:
        if name not in flights:
            flights[name] = []
        flights[name].append([lat, lon])
    return flights

@app.route('/api/flights')
def api_flights():
    return jsonify(get_flight_data())

@app.route('/')
def index():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
