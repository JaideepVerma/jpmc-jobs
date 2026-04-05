import sqlite3
import os
from jinja2 import Template

def get_jobs_from_db(db_path='JPMCjobs.db'):
    """Read all jobs from the database"""
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Change 'jobs' to your actual table name
        cursor.execute("SELECT company, role, description, responsibilities, qualifications, \
               location, posting_date,posted_at, job_family, job_function, apply_link , loaded_at \
        FROM jobs ORDER BY posting_date DESC")
        jobs = cursor.fetchall()
        
        jobs_list = [dict(job) for job in jobs]
        conn.close()
        
        print(f"✅ Read {len(jobs_list)} jobs from database")
        return jobs_list
    
    except Exception as e:
        print(f"❌ Error reading database: {e}")
        return []
def generate_static_site():
    """Generate static HTML from template"""
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    # Get jobs from database
    jobs = get_jobs_from_db('JPMCjobs.db')
    
    print(f"📊 Found {len(jobs)} jobs in database")
    
    # Read your template
    with open('templates/JPMC.html', 'r') as f:
        template_str = f.read()
    
    # Replace template variables with actual data
    from jinja2 import Template
    template = Template(template_str)
    
    html_content = template.render(
        jobs=jobs,
        total_jobs=len(jobs),
        total_salary=sum([job.get('salary', 0) for job in jobs]) if jobs else 0
    )
    
    # Save to output
    with open('output/index.html', 'w') as f:
        f.write(html_content)
    
    print(f"✅ Generated output/index.html")

if __name__ == '__main__':
    generate_static_site()

'''from flask import Flask, render_template
import sqlite3
import os
# Step 1: Create the Flask app object
app = Flask(__name__)

# Step 2: Define your route
@app.route("/jpmcjobs")
def jobs():
    dbpath = os.path.join(current_dir, 'JPMCjobs.db')
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
'''
