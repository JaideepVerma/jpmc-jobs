import json
import os
import flask
import sqlite3
import glob
os.makedirs("output", exist_ok=True)

# Find all DB files ending with jobs.db #
db_files = glob.glob("*jobs.db")
print("Found DB files:", db_files)

all_data = []

for db_file in db_files:
    print(f"Processing {db_file}...")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # List all tables in this DB
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", tables)

    # If you know the table is always called 'jobs'
    try:
        cursor.execute("SELECT * FROM jobs")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        all_data.extend(data)
    except sqlite3.OperationalError as e:
        print(f"Skipping {db_file}: {e}")

    conn.close()

# Save combined JSON
with open("output/data.json", "w") as f:
    json.dump(all_data, f, indent=2)
'''
os.makedirs("output", exist_ok=True)
current_dir = os.getcwd()
print('current_dir: ',current_dir)
dbpath = os.path.join(current_dir, 'JPMCjobs.db')
print('dbpath: ',dbpath)
# Connect to the DB created by your scraping script
conn = sqlite3.connect("JPMCjobs.db") 
cursor = conn.cursor()

# Adjust table name to match your schema
cursor.execute("SELECT * FROM jobs")
rows = cursor.fetchall()

# Convert rows into a list of dicts if you want column names
columns = [desc[0] for desc in cursor.description]
data = [dict(zip(columns, row)) for row in rows]

# Save as JSON inside output folder
with open("output/data.json", "w") as f:
    json.dump(data, f, indent=2)
with open("output/test.json", "w") as f:
    json.dump(data, f, indent=2)

conn.close()
'''
