import json
import os
import flask
current_dir = os.getcwd()
dbpath = os.path.join(current_dir, 'JPMCjobs.db')
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

conn.close()
