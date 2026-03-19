import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import time
import os

# reset DB
if os.path.exists("results.db"):
    os.remove("results.db")

conn = sqlite3.connect("results.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE results(
roll TEXT PRIMARY KEY,
name TEXT,
prog INTEGER,
it INTEGER,
math INTEGER,
eng INTEGER,
pun INTEGER,
commerce INTEGER,
sgpa REAL
)
""")

conn.commit()

BASE_URL = "http://www.kcaexamination.org/ResultDetail?class=229001&mrno={}&session=2025&month=12"
headers = {"User-Agent": "Mozilla/5.0"}


def extract_marks(soup):

    subjects = {
        "prog": None,
        "it": None,
        "math": None,
        "eng": None,
        "pun": None,
        "commerce": None
    }

    rows = soup.find_all("tr")

    for r in rows:

        text = r.get_text().upper()

        nums = [int(x) for x in re.findall(r'\d+', text)]

        if len(nums) == 0:
            continue

        obtained = max(nums)  # ✅ total marks

        if "INTRODUCTION TO PROGRAMMING" in text:
            subjects["prog"] = obtained

        elif "INFORMATION TECHNOLOGY" in text:
            subjects["it"] = obtained

        elif "MATHEMATICS" in text:
            subjects["math"] = obtained

        elif "COMMUNICATION SKILLS" in text:
            subjects["eng"] = obtained

        elif "PUNJABI" in text:
            subjects["pun"] = obtained

        elif "COMMERCE" in text:
            subjects["commerce"] = obtained

    return subjects


def scrape(roll):

    url = BASE_URL.format(roll)

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text()

    if "Name:" not in text:
        return

    name = re.search(r'Name:\s*(.*?)\s*Father', text).group(1)

    # SGPA from website
    sgpa_match = re.search(r'SGPA\s*-\s*([\d.]+)', text)
    sgpa = float(sgpa_match.group(1)) if sgpa_match else None

    subjects = extract_marks(soup)

    cursor.execute("""
    INSERT INTO results
    VALUES(?,?,?,?,?,?,?,?,?)
    """,(
        roll,
        name,
        subjects["prog"],
        subjects["it"],
        subjects["math"],
        subjects["eng"],
        subjects["pun"],
        subjects["commerce"],
        sgpa
    ))

    conn.commit()

    print("Saved:", roll, name, sgpa)


# roll ranges
rolls = []
rolls += list(range(23110012113,23110012271))
rolls += list(range(24110018101,24110018322))
rolls += list(range(25110018101,25110018337))


for r in rolls:
    scrape(r)
    time.sleep(0.3)

conn.close()
print("Scraping finished")