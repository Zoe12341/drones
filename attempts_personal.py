import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from datetime import datetime
import re

# Connect to PostgreSQL
conn = psycopg2.connect(
    # dbname='my_new_db',
    dbname='drone_data',
    user='gperez42', # replace with your username
    password='your_password',
    host='localhost',
    port='5432'
)
cur = conn.cursor()

# # Clear the table before inserting new data
# cur.execute("DELETE FROM professional;")
# conn.commit()
# print("Table cleared successfully.")

# Create the table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS professional (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    date TIMESTAMP,
    filepath TEXT  -- changed to TEXT for longer file paths
);
""")
conn.commit()
print("Table created successfully.")

# NEW CODE FOR PERSONAL TABLE

# Create the table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS personal (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    date TIMESTAMP,
    filepath TEXT
);
""")
conn.commit()
print("Personal table created successfully.")

# Path to the folder containing the files
# folder_path = '/Users/caseymacgibbon/Downloads/October 10th/files'
folder_path = '/Users/gperez42/Documents/CSC 230/Final Project/Data'

# Loop through files in the folder
for filename in os.listdir(folder_path):
    if filename.startswith("DJI_") and "_" in filename:
        # Process professional files (starts with DJI_)
        parts = filename.split("_")
        
        try:
            raw_date = parts[1]  # e.g., '202410171502'
            file_title = "_".join(parts[3:])  # everything after the second underscore
            # Parse the date string to datetime
            parsed_date = datetime.strptime(raw_date, "%Y%m%d%H%M")
            # Create full filepath
            full_path = os.path.join(folder_path, filename)

            # Check if file is already in the professional table
            cur.execute("SELECT 1 FROM professional WHERE name = %s;", (filename,))
            if cur.fetchone() is None:  # Only insert if the file isn't already in the table
                # Insert into professional table
                cur.execute("""
                    INSERT INTO professional (name, date, filepath)
                    VALUES (%s, %s, %s)
                """, (
                    filename,
                    parsed_date,
                    full_path
                ))
                print(f"Inserted into professional: {filename}")
            else:
                print(f"File {filename} already exists in professional table.")

        except Exception as e:
            print(f"Skipping professional {filename}: {e}")

    elif filename.count('.') == 1:
        try:
            # Split at the dot
            date_part = filename.split('.')[0]        # e.g., '10'
            day_and_rest = filename.split('.')[1]     # e.g., '23Bahamas2020Exports'

            # Extract the day (assumed to be first two digits after the dot)
            day = day_and_rest[:2]                    # '23'
            rest_of_name = day_and_rest[2:]           # 'Bahamas2020Exports'

            # Try to find a year in the remaining part
            match = re.search(r'(20\d{2})', rest_of_name)
            if match:
                year = match.group(1)                 # e.g., '2020'
            else:
                year = "2024"                         # Default year if none found

            # Construct the full date string
            full_date = f"{year}-{date_part}-{day}"
            parsed_date = datetime.strptime(full_date, "%Y-%m-%d")

            # Full file path
            full_path = os.path.join(folder_path, filename)

            # Check for duplicates
            cur.execute("SELECT 1 FROM personal WHERE name = %s;", (filename,))
            if cur.fetchone() is None:
                cur.execute("""
                    INSERT INTO personal (name, date, filepath)
                    VALUES (%s, %s, %s)
                """, (
                    filename,
                    parsed_date,
                    full_path
                ))
                print(f"Inserted into personal: {filename}")
            else:
                print(f"File {filename} already exists in personal table.")

        except Exception as e:
            print(f"Skipping personal {filename}: {e}")


# Commit all changes to the database
conn.commit()

# Query and check the inserted data from both tables
cur.execute("SELECT * FROM professional;")
rows = cur.fetchall()
print("Rows in professional table:")
for row in rows:
    print(row)

cur.execute("SELECT * FROM personal;")
rows = cur.fetchall()
print("Rows in personal table:")
for row in rows:
    print(row)


# Close the connection
cur.close()
conn.close()