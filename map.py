from flask import Flask, request, jsonify, render_template_string
import psycopg2
from datetime import datetime
import sys

app = Flask(__name__)

DB_CONFIG = {
    'dbname': 'drone_data',
    'user': 'caseymacgibbon',  # REPLACE THIS WITH YOUR USERNAME
    'host': 'localhost'
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"🚨 Database connection failed: {e}", file=sys.stderr)
        raise

@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Flight Map</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    #map { height: 90vh; width: 100%; }
    body { margin: 0; font-family: sans-serif; }
  </style>
</head>
<body>
  <h2 style="padding: 1em;">Professional Drone Flights</h2>
  <div id="map"></div>

  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    const map = L.map('map').setView([42.38, -72.53], 10);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    fetch('/coordinates')
      .then(response => response.json())
      .then(data => {
        Object.keys(data).forEach(name => {
          const coords = data[name];
          const latlngs = coords.map(c => [c.lat, c.lon]);

          L.polyline(latlngs, { color: 'blue' }).addTo(map)
            .bindPopup(`<strong>${name}</strong>`);

          if (latlngs.length) {
            L.marker(latlngs[0]).addTo(map)
              .bindPopup(`<strong>Start of ${name}</strong>`);
          }s
        });
      })
      .catch(err => console.error('Failed to load coordinates:', err));
  </script>
</body>
</html>
    """)

@app.route('/coordinates')
def get_coordinates():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT professional_name, lat, lon, sequence
            FROM professional_coordinates
            ORDER BY professional_name, sequence;
        """)
        coords = cur.fetchall()
        results = {}
        for name, lat, lon, seq in coords:
            if name not in results:
                results[name] = []
            results[name].append({'lat': lat, 'lon': lon, 'sequence': seq})
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/search', methods=['GET'])
def search():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    imagery_type = request.args.get('imagery_type', 'all')
    
    if not date_from or not date_to:
        return jsonify({'error': 'Both date ranges are required'}), 400
    
    try:
        date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    results = []
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if imagery_type in ['all', 'professional']:
            cursor.execute("""
                SELECT name, capture_date, COALESCE(location, 'Unknown'), file_path, 'professional'
                FROM professional_imagery
                WHERE capture_date BETWEEN %s AND %s
                ORDER BY capture_date
            """, (date_from, date_to))
            results.extend(cursor.fetchall())
        
        if imagery_type in ['all', 'personal']:
            cursor.execute("""
                SELECT name, capture_date, location, file_path, 'personal'
                FROM personal_imagery
                WHERE capture_date BETWEEN %s AND %s
                ORDER BY capture_date
            """, (date_from, date_to))
            results.extend(cursor.fetchall())
        
        formatted_results = [{
            'name': row[0],
            'date': row[1].strftime('%Y-%m-%d'),
            'location': row[2],
            'file_path': row[3],
            'type': row[4]
        } for row in results]
        
        return jsonify({'results': formatted_results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'professional_imagery');
        """)
        if not cursor.fetchone()[0]:
            cursor.execute("""
                CREATE TABLE professional_imagery (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    capture_date DATE NOT NULL,
                    location VARCHAR(255),
                    file_path VARCHAR(512) NOT NULL,
                    flight_operator VARCHAR(255),
                    project_name VARCHAR(255),
                    resolution VARCHAR(50)
                );
                CREATE INDEX idx_professional_date ON professional_imagery(capture_date);
            """)
            print("Created professional_imagery table")
        
        cursor.execute("""
            SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'personal_imagery');
        """)
        if not cursor.fetchone()[0]:
            cursor.execute("""
                CREATE TABLE personal_imagery (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    capture_date DATE NOT NULL,
                    location VARCHAR(255),
                    file_path VARCHAR(512) NOT NULL,
                    owner VARCHAR(255),
                    tags VARCHAR(255)[]
                );
                CREATE INDEX idx_personal_date ON personal_imagery(capture_date);
            """)
            print("Created personal_imagery table")
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error initializing database: {str(e)}")
        raise e
    finally:
        cursor.close()
        conn.close()

def migrate_old_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO professional_imagery (name, capture_date, file_path)
            SELECT name, date, filepath
            FROM professional
            WHERE NOT EXISTS (
                SELECT 1 FROM professional_imagery 
                WHERE professional_imagery.file_path = professional.filepath
            );
        """)
        conn.commit()
        print("Migrated old data (if any)")
    except Exception as e:
        print(f"Migration skipped (no old data or error: {e})")
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    try:
        initialize_database()
        migrate_old_data()
        app.run(debug=True, use_reloader=False)
    except Exception as e:
        print(f"Failed to start: {e}")
        app.run(debug=False)
