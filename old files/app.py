# app.py

from flask import Flask, render_template, request, jsonify
import psycopg2
from datetime import datetime
import sys

# Configure Flask application
app = Flask(__name__)

DB_CONFIG = {
    'dbname': 'drone_data',
    'user': 'postgres',  # REPLACE THIS WITH YOUR USERNAME
    'host': 'localhost'
}

def get_db_connection():
    """Establish database connection with error handling"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"🚨 Database connection failed: {e}", file=sys.stderr)
        print("Please verify:")
        print(f"- Database is running (try: 'sudo service postgresql start')")
        print(f"- Connection details in DB_CONFIG are correct")
        print(f"- PostgreSQL user '{DB_CONFIG['user']}' has access to database '{DB_CONFIG['dbname']}'")
        raise




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    imagery_type = request.args.get('imagery_type', 'all')  # 'all', 'personal', 'professional'
    
    if not date_from or not date_to:
        return jsonify({'error': 'Both date ranges are required'}), 400
    
    try:
        # Convert dates to proper format
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
                SELECT 
                    name, 
                    capture_date as date, 
                    COALESCE(location, 'Unknown') as location, 
                    file_path, 
                    'professional' as type 
                FROM professional_imagery 
                WHERE capture_date BETWEEN %s AND %s
                ORDER BY capture_date
            """, (date_from, date_to))
            results.extend(cursor.fetchall())
        
        if imagery_type in ['all', 'personal']:
            cursor.execute("""
                SELECT name, capture_date, location, file_path, 'personal' as type 
                FROM personal_imagery 
                WHERE capture_date BETWEEN %s AND %s
                ORDER BY capture_date
            """, (date_from, date_to))
            results.extend(cursor.fetchall())
        
        # Format results
        formatted_results = []
        for row in results:
            formatted_results.append({
                'name': row[0],
                'date': row[1].strftime('%Y-%m-%d'),
                'location': row[2],
                'file_path': row[3],
                'type': row[4]
            })
        
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
        # Check if professional table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'professional_imagery'
            );
        """)
        professional_exists = cursor.fetchone()[0]
        
        if not professional_exists:
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
        
        # Check if personal table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'personal_imagery'
            );
        """)
        personal_exists = cursor.fetchone()[0]
        
        if not personal_exists:
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
    """One-time migration from old 'professional' table to new schema"""
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
        app.run(debug=True, use_reloader=False)  # Temporary workaround
    except Exception as e:
        print(f"Failed to start: {e}")
        print("Trying without debug mode...")
        app.run(debug=False)
