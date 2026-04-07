import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import os


from datetime import datetime, timezone, timedelta

def get_ist_timestamp():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

def scrape_jpmc():
    #url = "https://jpmc.fa.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.workLocation,requisitionList.otherWorkLocations,requisitionList.secondaryLocations,flexFieldsFacet.values,requisitionList.requisitionFlexFields&finder=findReqs;siteNumber=CX_1001,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=25,locationId=300000000289360,sortBy=POSTING_DATES_DESC"
    #url ="https://jpmc.fa.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.workLocation,requisitionList.otherWorkLocations,requisitionList.secondaryLocations,flexFieldsFacet.values,requisitionList.requisitionFlexFields&finder=findReqs;siteNumber=CX_1001,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=35,lastSelectedFacet=CATEGORIES,locationId=300000000289360,selectedCategoriesFacet=300000086250134%3B300000086152593,sortBy=POSTING_DATES_DESC"
    url = "https://jpmc.fa.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.workLocation,requisitionList.otherWorkLocations,requisitionList.secondaryLocations,flexFieldsFacet.values,requisitionList.requisitionFlexFields&finder=findReqs;siteNumber=CX_1001,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=35,lastSelectedFacet=CATEGORIES,locationId=300000000289360,selectedCategoriesFacet=300000086152753%3B300000086250134%3B300000086153065%3B300000086251864%3B300000086152593%3B300000086152512,sortBy=POSTING_DATES_DESC"
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    #print(data)
    jobs = []
    for item in data.get("items", []):
        for req in item.get("requisitionList", []):
            job_id = req.get("Id")
            role = req.get("Title", "N/A")
            description = req.get("ShortDescriptionStr", "N/A")
            responsibilities = req.get("ExternalResponsibilitiesStr", "N/A")
            qualifications = req.get("ExternalQualificationsStr", "N/A")
            location = req.get("PrimaryLocation", "N/A")
            posting_date = req.get("PostedDate", "N/A")
            apply_link = req.get("ExternalApplyLink", "N/A")
            JobFunction = req.get("JobFunction","N/A")
            JobFamily = req.get("JobFamily",'N/A')

            jobs.append({
                "company": "JPMC",
                "job_id": job_id,
                "role": role,
                "description": description,
                "JobFunction" : JobFunction,
                "JobFamily" : JobFamily,
                "responsibilities": responsibilities,
                "qualifications": qualifications,
                "location": location,
                "posting_date": posting_date,
                "apply_link": 'https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/job/' + job_id                
            })
    print(jobs)
    return jobs


def save_jobs(jobs):
    # Get current directory
    current_dir = os.getcwd()
    dbpath = os.path.join(current_dir, 'JPMCjobs.db')
    #dbpath = f'C:/Users/jdver/OneDrive/Desktop/py/JPMCjobs.db'
    print('Jobs added to : ' , dbpath)
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    for job in jobs:

        c.execute("SELECT * FROM jobs WHERE company=? AND job_id=?",
                  (job["company"], job["job_id"]))
        if not c.fetchone():
            c.execute("""INSERT INTO jobs 
                         (company, job_id, role, description, responsibilities, qualifications, location, posting_date, job_family, job_function, apply_link) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                      (job["company"], job["job_id"], job["role"], job["description"], job["responsibilities"], job["qualifications"], job["location"], job["posting_date"], job["JobFamily"], job["JobFunction"],job["apply_link"])) ##
    conn.commit()
    conn.close()

#Run Below if there is any new column 
'''
conn = sqlite3.connect("JPMCjobs.db")
cur = conn.cursor()
cur.execute("ALTER TABLE jobs ADD COLUMN loaded_at TEXT;")
conn.commit()
conn.close() 
'''
if __name__ == "__main__":
    jobs = scrape_jpmc()
    save_jobs(jobs)
    print
    print('Jobs saved to .db')import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import os


from datetime import datetime, timezone, timedelta

def get_ist_timestamp():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

def scrape_jpmc():
    #url = "https://jpmc.fa.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.workLocation,requisitionList.otherWorkLocations,requisitionList.secondaryLocations,flexFieldsFacet.values,requisitionList.requisitionFlexFields&finder=findReqs;siteNumber=CX_1001,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=25,locationId=300000000289360,sortBy=POSTING_DATES_DESC"
    #url ="https://jpmc.fa.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.workLocation,requisitionList.otherWorkLocations,requisitionList.secondaryLocations,flexFieldsFacet.values,requisitionList.requisitionFlexFields&finder=findReqs;siteNumber=CX_1001,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=35,lastSelectedFacet=CATEGORIES,locationId=300000000289360,selectedCategoriesFacet=300000086250134%3B300000086152593,sortBy=POSTING_DATES_DESC"
    url = "https://jpmc.fa.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.workLocation,requisitionList.otherWorkLocations,requisitionList.secondaryLocations,flexFieldsFacet.values,requisitionList.requisitionFlexFields&finder=findReqs;siteNumber=CX_1001,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=35,lastSelectedFacet=CATEGORIES,locationId=300000000289360,selectedCategoriesFacet=300000086152753%3B300000086250134%3B300000086153065%3B300000086251864%3B300000086152593%3B300000086152512,sortBy=POSTING_DATES_DESC"
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    #print(data)
    jobs = []
    for item in data.get("items", []):
        for req in item.get("requisitionList", []):
            job_id = req.get("Id")
            role = req.get("Title", "N/A")
            description = req.get("ShortDescriptionStr", "N/A")
            responsibilities = req.get("ExternalResponsibilitiesStr", "N/A")
            qualifications = req.get("ExternalQualificationsStr", "N/A")
            location = req.get("PrimaryLocation", "N/A")
            posting_date = req.get("PostedDate", "N/A")
            apply_link = req.get("ExternalApplyLink", "N/A")
            JobFunction = req.get("JobFunction","N/A")
            JobFamily = req.get("JobFamily",'N/A')

            jobs.append({
                "company": "JPMC",
                "job_id": job_id,
                "role": role,
                "description": description,
                "JobFunction" : JobFunction,
                "JobFamily" : JobFamily,
                "responsibilities": responsibilities,
                "qualifications": qualifications,
                "location": location,
                "posting_date": posting_date,
                "apply_link": 'https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/job/' + job_id                
            })
    print(jobs)
    return jobs


def save_jobs(jobs):
    # Get current directory
    current_dir = os.getcwd()
    dbpath = os.path.join(current_dir, 'JPMCjobs.db')
    #dbpath = f'C:/Users/jdver/OneDrive/Desktop/py/JPMCjobs.db'
    print('Jobs added to : ' , dbpath)
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    for job in jobs:

        c.execute("SELECT * FROM jobs WHERE company=? AND job_id=?",
                  (job["company"], job["job_id"]))
        if not c.fetchone():
            c.execute("""INSERT INTO jobs 
                         (company, job_id, role, description, responsibilities, qualifications, location, posting_date, job_family, job_function, apply_link) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                      (job["company"], job["job_id"], job["role"], job["description"], job["responsibilities"], job["qualifications"], job["location"], job["posting_date"], job["JobFamily"], job["JobFunction"],job["apply_link"])) ##
    conn.commit()
    conn.close()

#Run Below if there is any new column 
'''
conn = sqlite3.connect("JPMCjobs.db")
cur = conn.cursor()
cur.execute("ALTER TABLE jobs ADD COLUMN loaded_at TEXT;")
conn.commit()
conn.close() 
'''
if __name__ == "__main__":
    jobs = scrape_jpmc()
    save_jobs(jobs)
    print
    print('Jobs saved to .db')
