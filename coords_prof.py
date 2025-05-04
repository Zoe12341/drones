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

# Clear existing tables if needed
cur.execute("DROP TABLE IF EXISTS professional_coordinates;")
cur.execute("DROP TABLE IF EXISTS professional;")
conn.commit()
print("Existing tables dropped successfully.")

# Create the tables
cur.execute("""
CREATE TABLE professional (
    name VARCHAR(100) PRIMARY KEY,
    date TIMESTAMP,
    filepath TEXT
);
""")

cur.execute("""
CREATE TABLE professional_coordinates (
    id SERIAL PRIMARY KEY,
    professional_name VARCHAR(100) REFERENCES professional(name) ON DELETE CASCADE,
    lat FLOAT,
    lon FLOAT,
    sequence INT
);
""")
conn.commit()
print("Tables created successfully.")

# Folder containing subfolders like DJI_...
folder_path = '/Users/caseymacgibbon/Downloads/October 10th/files'

# Extract all lat/lon from MRK file
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

# Loop through folders
for folder in os.listdir(folder_path):
    folder_full_path = os.path.join(folder_path, folder)

    if os.path.isdir(folder_full_path) and folder.startswith("DJI_") and "_" in folder:
        parts = folder.split("_")

        try:
            raw_date = parts[1]  # e.g., '202410171502'
            parsed_date = datetime.strptime(raw_date, "%Y%m%d%H%M")

            # Look for a .MRK file in this folder
            mrk_file = next(
                (os.path.join(folder_full_path, f) for f in os.listdir(folder_full_path) if f.lower().endswith(".mrk")),
                None
            )

            # Insert metadata
            cur.execute("""
                INSERT INTO professional (name, date, filepath)
                VALUES (%s, %s, %s)
                ON CONFLICT (name) DO NOTHING;
            """, (folder, parsed_date, folder_full_path))

            # Insert coordinates
            if mrk_file:
                coords = extract_lat_lon_all(mrk_file)
                for lat, lon, seq in coords:
                    cur.execute("""
                        INSERT INTO professional_coordinates (professional_name, lat, lon, sequence)
                        VALUES (%s, %s, %s, %s);
                    """, (folder, lat, lon, seq))

            print(f"Inserted: {folder} with {len(coords)} coordinate(s)")

        except Exception as e:
            print(f"Skipping {folder}: {e}")

# Finalize
conn.commit()

# Optional: print sample of inserted data
cur.execute("SELECT name, date FROM professional;")
print("\nFlights:")
for row in cur.fetchall():
    print(row)

cur.execute("""
    SELECT professional_name, lat, lon, sequence
    FROM professional_coordinates
    ORDER BY professional_name, sequence
    LIMIT 10;
""")
print("\nSample coordinates:")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()
