import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os


conn = psycopg2.connect(
    dbname='my_new_db',
    user='caseymacgibbon',
    password='your_password',
    host='localhost',
    port='5432'
)

cur = conn.cursor()  

cur.execute("""
CREATE TABLE IF NOT EXISTS professional (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    date TIMESTAMP,
    filepath VARCHAR(100)
);
""")
conn.commit()
print("Table created successfully.")

# Now insert data correctly
from datetime import datetime

# cur.execute("""
#     INSERT INTO professional (name, date, filepath) 
#     VALUES (%s, %s, %s)
# """, (
#     'Bahamas',
#     datetime.now(),                   # current date/time
#     '/Users/caseymacgibbon/resume.pdf'
# ))
# conn.commit()
# print("Row inserted successfully.")

# Path to the folder containing the files
folder_path = '/Users/caseymacgibbon/Downloads/October 10th/files'

print(os.listdir(folder_path))
# Loop through files in the folder
for filename in os.listdir(folder_path):
    if filename.startswith("DJI_") and "_" in filename:
        parts = filename.split("_")
        
        try:
            raw_date = parts[1]  # e.g., '202410171502'
            file_title = "_".join(parts[3:])  # everything after the second underscore

            # Parse the date string to datetime
            parsed_date = datetime.strptime(raw_date, "%Y%m%d%H%M")

            # Create full filepath
            full_path = os.path.join(folder_path, filename)

            # Insert into database
            cur.execute("""
                INSERT INTO professional (name, date, filepath)
                VALUES (%s, %s, %s)
            """, (
                filename,
                parsed_date,
                full_path
            ))
            print(f"Inserted: {filename}")
        except Exception as e:
            print(f"Skipping {filename}: {e}")

cur.execute("SELECT * FROM professional;")
conn.close()