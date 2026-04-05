import sqlite3

conn = sqlite3.connect("JPMCjobs.db")
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    job_id TEXT,
    role TEXT,
    description TEXT,
    responsibilities TEXT,
    qualifications TEXT,
    location TEXT,
    posting_date TEXT,
    job_family TEXT,
    job_function TEXT,
    apply_link TEXT,
    posted_at TEXT,
    loaded_at TEXT 
          
)
''')

conn.commit()
conn.close()
print("Jobs table updated successfully.")
