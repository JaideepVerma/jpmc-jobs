import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import json
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
try:
    from bs4 import BeautifulSoup
    _HAS_BS4 = True
except Exception:
    _HAS_BS4 = False
url = "https://amazon.jobs/api/jobs/search?is_als=true"

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "x-api-key": "PbxxNwIlTi4FP5oijKdtk3IrBF5CLd4R4oPHsKNh",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}

def fetch_jobs():
    size = 10
    start = 0
    all_records = []
    while start <=20 :
        payload = {
            "accessLevel": "EXTERNAL",
            "contentFilterFacets": [
                {
                    "name": "primarySearchLabel",
                    "requestedFacetCount": 9999
                }
            ],
            "excludeFacets": [
                {
                    "name": "isConfidential",
                    "values": [
                        {
                            "name": "1"
                        }
                    ]
                },
                {
                    "name": "businessCategory",
                    "values": [
                        {
                            "name": "a-confidential-job"
                        }
                    ]
                }
            ],
            "filterFacets": [
                {
                    "name": "optionalSearchLabels",
                    "requestedFacetCount": 9999,
                    "values": [
                        {
                            "name": "amazon.artificial-intelligence"
                        },
                        {
                            "name": "alexa-and-amazon-devices.team-machine-learning-and-science-job-family"
                        }
                    ]
                }
            ],
            "includeFacets": [],
            "jobTypeFacets": [],
            "locationFacets": [
                [
                    {
                        "name": "country",
                        "requestedFacetCount": 9999,
                        "values": [
                            {
                                "name": "IN"
                            }
                        ]
                    },
                    {
                        "name": "normalizedStateName",
                        "requestedFacetCount": 9999
                    },
                    {
                        "name": "normalizedCityName",
                        "requestedFacetCount": 9999
                    }
                ]
            ],
            "query": "",
            "size": size,
            "start": start,
            "treatment": "OM",
            "sort": {
                "sortOrder": "DESCENDING",
                "sortType": "CREATED_DATE"  # "SCORE" for sorting in 'relavant'
            }

        }

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        hits = data.get("searchHits", [])
        # move to next page
        if not hits:  # stop when no more results
            break

        for hit in hits:
            fields = hit.get("fields") or {}
            rec = normalize_fields(fields)
            if rec.get("job_id"):
                rec = add_loaded_timestamp(rec)  
                all_records.append(rec)
        start += size
    return all_records

from datetime import datetime, timezone, timedelta

def add_loaded_timestamp(record: Dict[str, Any]) -> Dict[str, Any]:
    ist = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist)
    #now = datetime.now(timezone.ist)
    record["loaded_at_iso"] = now.strftime("%Y-%m-%d %H:%M:%S") # now.isoformat()
    #record["loaded_at_epoch"] = int(now.timestamp())
    return record

#print(data)

#hit = data['searchHits'][0]        # TEST
#fields = hit.get("fields", {})     # TEST
#fields = hit.get("fields", {})     # TEST
#print(fields)                      # TEST

def unwrap_single(v: Any) -> Any:
    if isinstance(v, list) and len(v) == 1:
        return v[0]
    return v

def strip_html(s: Optional[str]) -> Optional[str]:
    if not s:
        return s
    if _HAS_BS4:
        return BeautifulSoup(s, "html.parser").get_text(separator=" ", strip=True)
    return re.sub(r"<[^>]+>", " ", s).replace("\n", " ").strip()

def parse_locations_field(val: Any) -> Dict[str, Any]:
    if not val:
        return {}
    v = unwrap_single(val)
    if isinstance(v, dict):
        return v
    if isinstance(v, str):
        try:
            return json.loads(v)
        except Exception:
            parts = [p.strip() for p in v.split(",")]
            out = {}
            if len(parts) >= 1: out["countryIso2a"] = parts[0]
            if len(parts) >= 2: out["region"] = parts[1]
            if len(parts) >= 3: out["city"] = parts[2]
            return out
    return {}

def epoch_to_iso_and_int(ts: Optional[Any]) -> (Optional[str], Optional[int]):
    if ts is None:
        return None, None
    try:
        t = int(str(ts))
        if t > 10**12:
            t = t // 1000
        iso = datetime.fromtimestamp(t, tz=timezone.utc).isoformat()
        return iso, t
    except Exception:
        return None, None

def normalize_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    simple = {k: unwrap_single(v) for k, v in (fields or {}).items()}
    loc_parsed = parse_locations_field(simple.get("locations") or simple.get("location"))

    created_iso, created_epoch = epoch_to_iso_and_int(simple.get("createdDate"))
    updated_iso, updated_epoch = epoch_to_iso_and_int(simple.get("updatedDate"))

    record = {
        "company": 'AMAZON' #simple.get("companyName"),
        "job_id": simple.get("artJobId") or simple.get("icimsJobId") or simple.get("jobCode"),
        "role": simple.get("title"),
        #"team": simple.get("teamCategory") or simple.get("primarySearchLabel"),
        "job_family": simple.get("jobFamily"),
        "JobFunction" : 'JobFunction',
        #"job_role": simple.get("jobRole"),
        #"employment_type": simple.get("employeeClass") or simple.get("scheduleTypeId"),
        #"is_tech": int(simple.get("isTech")) if simple.get("isTech") is not None else None,
        #"is_intern": int(simple.get("isIntern")) if simple.get("isIntern") is not None else None,
        #"city": simple.get("city") or loc_parsed.get("city") or simple.get("normalizedCityName"),
        #"state": simple.get("normalizedStateName") or loc_parsed.get("normalizedStateName"),
        #"country": simple.get("normalizedCountryCode") or loc_parsed.get("normalizedCountryCode") or loc_parsed.get("countryIso2a"),
        "location": simple.get("normalizedLocation") or simple.get("location"),
        #"short_description": strip_html(simple.get("shortDescription")),
        #"description_text": strip_html(simple.get("description")),
        "description": strip_html(simple.get("description")),
        "responsibilities": 'responsibilities'
        "qualifications": strip_html(simple.get("basicQualifications")),
        #"preferred_qualifications": strip_html(simple.get("preferredQualifications")),
        #"category": simple.get("category") or simple.get("businessCategory"),
        #"apply_url": simple.get("urlNextStep") or simple.get("applyUrl"),
        #"created_at_iso": created_iso,
        #"created_at_epoch": created_epoch,
        "posting_date": created_iso + 'Updated at: ' + updated_iso,
        #"updated_at_iso": updated_iso,
        #"updated_at_epoch": updated_epoch,
        #"locations_raw": json.dumps(loc_parsed) if loc_parsed else None,
        "apply_link" : 'https://amazon.jobs/en/jobs/' + simple.get("icimsJobId")
    }
 # https://amazon.jobs/en/jobs/3206932/
    # Normalize empty strings to None
    for k, v in list(record.items()):
        if isinstance(v, str) and v.strip() == "":
            record[k] = None

    return record

#hits = data.get("searchHits", [])
#normalized_records = []
 
# TEST hit = data['searchHits'][0]
# TEST fields = hit.get("fields", {})

# ---------- Database helpers ----------
DB_FILE = "AMZjobs.db"

CREATE_TABLE_SQL = """
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
);
"""

CREATE_INDEXES_SQL = [
    "CREATE INDEX IF NOT EXISTS idx_jobs_country ON jobs(country);",
    "CREATE INDEX IF NOT EXISTS idx_jobs_city ON jobs(city);",
    "CREATE INDEX IF NOT EXISTS idx_jobs_created_epoch ON jobs(created_at_epoch);"
]

INSERT_SQL = """
INSERT OR REPLACE INTO jobs (
    job_id, title, company, team, job_family, job_role, employment_type,
    is_tech, is_intern, city, state, country, location_display,
    short_description, description_text, basic_qualifications, preferred_qualifications,
    category, apply_url, created_at_iso, created_at_epoch, updated_at_iso, updated_at_epoch,
    locations_raw,icimsJobId, loaded_at_iso
) VALUES (
    :job_id, :title, :company, :team, :job_family, :job_role, :employment_type,
    :is_tech, :is_intern, :city, :state, :country, :location_display,
    :short_description, :description_text, :basic_qualifications, :preferred_qualifications,
    :category, :apply_url, :created_at_iso, :created_at_epoch, :updated_at_iso, :updated_at_epoch,
    :locations_raw, :icimsJobId , :loaded_at_iso
);
"""

def create_db(db_file: str = DB_FILE):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.executescript(CREATE_TABLE_SQL)
    for idx_sql in CREATE_INDEXES_SQL:
        cur.execute(idx_sql)
    conn.commit()
    conn.close()

def insert_jobs(records: List[Dict[str, Any]], db_file: str = DB_FILE):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    with conn:
        cur.executemany(INSERT_SQL, records)
    conn.close()

import sqlite3
db = "AMZjobs.db"   # or DB_FILE you use
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute("PRAGMA table_info(jobs);")
cols = cur.fetchall()
conn.close()
print("columns:", cols)

#RUN below cmd if there is a new addition of a column in DB
'''
conn = sqlite3.connect("AMZjobs.db")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS jobs;")
conn.commit()
conn.close()
'''
# ---------- Main flow ----------
def main():
    print("Fetching jobs with pagination...")
    records = fetch_jobs()  # adjust max_pages as needed
    print(f"Fetched {len(records)} jobs")

    create_db()
    insert_jobs(records)
    print(f"Inserted {len(records)} jobs into {DB_FILE}")

if __name__ == "__main__":
    main()
'''

if __name__ == "__main__":
    # Example: load data from a JSON file or assume `data` variable exists
    # Option A: load from file
    # with open("search_results.json", "r", encoding="utf-8") as f:
    #     data = json.load(f)
    # Option B: assume `data` is already in memory

    # Replace the following with your actual data source
    try:
        data  # type: ignore
    except NameError:
        raise RuntimeError("Provide `data` variable containing the API response with key 'searchHits'")

    hits = data.get("searchHits", [])
    normalized_records = []
    for hit in hits:
        fields = hit.get("fields") or hit.get("Fields") or {}
        rec = normalize_fields(fields)
        if rec.get("job_id"):  # skip records without id
            normalized_records.append(rec)
            print(rec)
    record = normalize_fields(fields)  # your normalization function
    import pprint
    #pprint.pprint(record)
    #print("keys:", sorted(record.keys()))
    print("types:", {k: type(v).__name__ for k, v in record.items()})
    create_db()
    insert_jobs(normalized_records)
    print(f"Inserted {len(normalized_records)} jobs into {DB_FILE}")

'''
