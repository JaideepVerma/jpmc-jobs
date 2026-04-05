from flask import Flask, render_template
import sqlite3

# Step 1: Create the Flask app object
app = Flask(__name__)

# Step 2: Define your route
@app.route("/jpmcjobs")
def jobs():
    dbpath = f'C:/Users/jdver/OneDrive/Desktop/py/JPMCjobs.db'
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()

    c.execute("""
        SELECT company, role, description, responsibilities, qualifications, 
               location, posting_date,posted_at, job_family, job_function, apply_link , loaded_at
        FROM jobs ORDER BY posting_date DESC
    """)
    jobs = c.fetchall()
    conn.close()
    return render_template("JPMC.html", jobs=jobs)

# Step 3: Run the app
if __name__ == "__main__":
    app.run(debug=True)
