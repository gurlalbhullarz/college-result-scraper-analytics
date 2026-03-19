import sqlite3

conn = sqlite3.connect("results.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM results WHERE sgpa IS NOT NULL")

rows = cursor.fetchall()

students = []

for r in rows:

    roll,name,prog,it,math,eng,pun,commerce,sgpa = r

    students.append({
        "roll":roll,
        "name":name,
        "sgpa":sgpa,
        "prog":prog,
        "it":it,
        "math":math,
        "eng":eng,
        "pun":pun,
        "commerce":commerce
    })


# MERIT
students.sort(key=lambda x:x["sgpa"], reverse=True)

print("\n===== MERIT LIST =====\n")

rank = 1
for s in students:
    print(rank, s["roll"], s["name"], s["sgpa"])
    rank += 1


# SAFE TOPPER FUNCTION
def topper(sub):

    valid = [s for s in students if s[sub] is not None]

    if len(valid) == 0:
        return None

    valid.sort(key=lambda x:x[sub], reverse=True)

    return valid[0]


print("\n===== SUBJECT TOPPERS =====\n")

subjects = {
    "prog":"Programming in C",
    "it":"IT",
    "math":"Math",
    "eng":"English",
    "pun":"Punjabi",
    "commerce":"Commerce"
}

for key,name in subjects.items():

    t = topper(key)

    if t:
        print(name,":", t["name"], "-", t[key])
    else:
        print(name,": No data")

conn.close()