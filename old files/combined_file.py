import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import re
from datetime import datetime

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname='drone_data',
    user='caseymacgibbon',
    password='your_password',  # Replace with your actual password or use os.environ
    host='localhost',
    port='5432'
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

# Create tables if they don't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS professional (
    name VARCHAR(100) PRIMARY KEY,
    date TIMESTAMP,
    filepath TEXT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS professional_coordinates (
    id SERIAL PRIMARY KEY,
    professional_name VARCHAR(100) REFERENCES professional(name) ON DELETE CASCADE,
    lat FLOAT,
    lon FLOAT,
    sequence INT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS personal (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    date TIMESTAMP,
    filepath TEXT
);
""")
conn.commit()
print("Tables created successfully.")

# Define path to the data folder
folder_path = '/Users/caseymacgibbon/Downloads/October 10th/files'

# Extract coordinates from MRK files
def extract_lat_lon_all(mrk_file):
    coords = []
    try:
        with open(mrk_file, "r") as f:
            for idx, line in enumerate(f):
                lat_match = re.search(r"([-+]?\d*\.\d+),Lat", line)
                lon_match = re.search(r"([-+]?\d*\.\d+),Lon", line)
                if lat_match and lon_match:
                    coords.append((float(lat_match.group(1)), float(lon_match.group(1)), idx))
    except Exception as e:
        print(f"Error reading {mrk_file}: {e}")
    return coords

# Loop through files/folders in directory
for item in os.listdir(folder_path):
    full_path = os.path.join(folder_path, item)

    # PROFESSIONAL folders (DJI_)
    if os.path.isdir(full_path) and item.startswith("DJI_") and "_" in item:
        parts = item.split("_")
        try:
            raw_date = parts[1]  # e.g., '202410171502'
            parsed_date = datetime.strptime(raw_date, "%Y%m%d%H%M")

            # Check if already in professional table
            cur.execute("SELECT 1 FROM professional WHERE name = %s;", (item,))
            if cur.fetchone() is None:
                cur.execute("""
                    INSERT INTO professional (name, date, filepath)
                    VALUES (%s, %s, %s)
                """, (item, parsed_date, full_path))
                print(f"Inserted into professional: {item}")
            else:
                print(f"Professional folder {item} already exists.")

            # Handle .MRK coordinate file
            mrk_file = next((os.path.join(full_path, f) for f in os.listdir(full_path) if f.lower().endswith(".mrk")), None)
            if mrk_file:
                coords = extract_lat_lon_all(mrk_file)
                for lat, lon, seq in coords:
                    cur.execute("""
                        INSERT INTO professional_coordinates (professional_name, lat, lon, sequence)
                        VALUES (%s, %s, %s, %s);
                    """, (item, lat, lon, seq))
                print(f"Inserted {len(coords)} coordinate(s) for {item}")
        except Exception as e:
            print(f"Skipping professional {item}: {e}")

    # PERSONAL files (with a dot and one extension)
    elif os.path.isfile(full_path) and item.count('.') == 1:
        try:
            date_part = item.split('.')[0]
            day_and_rest = item.split('.')[1]

            day = day_and_rest[:2]
            rest_of_name = day_and_rest[2:]

            match = re.search(r'(20\d{2})', rest_of_name)
            year = match.group(1) if match else "2024"

            full_date = f"{year}-{date_part}-{day}"
            parsed_date = datetime.strptime(full_date, "%Y-%m-%d")

            cur.execute("SELECT 1 FROM personal WHERE name = %s;", (item,))
            if cur.fetchone() is None:
                cur.execute("""
                    INSERT INTO personal (name, date, filepath)
                    VALUES (%s, %s, %s)
                """, (item, parsed_date, full_path))
                print(f"Inserted into personal: {item}")
            else:
                print(f"Personal file {item} already exists.")
        except Exception as e:
            print(f"Skipping personal {item}: {e}")

# Final commit
conn.commit()

# Summarize inserted data
print("\nFlights:")
cur.execute("SELECT name, date FROM professional;")
for row in cur.fetchall():
    print(row)

print("\nSample coordinates:")
cur.execute("""
    SELECT professional_name, lat, lon, sequence
    FROM professional_coordinates
    ORDER BY professional_name, sequence
    LIMIT 10;
""")
for row in cur.fetchall():
    print(row)

print("\nPersonal files:")
cur.execute("SELECT name, date FROM personal;")
for row in cur.fetchall():
    print(row)

# Cleanup
cur.close()
conn.close()
