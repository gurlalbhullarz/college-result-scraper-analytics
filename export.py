import sqlite3
import pandas as pd

conn = sqlite3.connect("results.db")

query = """
SELECT 
roll AS Roll,
name AS Name,
sgpa AS SGPA,
prog AS Programming,
it AS IT,
math AS Math,
eng AS English,
pun AS Punjabi,
commerce AS Commerce
FROM results
WHERE sgpa IS NOT NULL
ORDER BY sgpa DESC
"""

df = pd.read_sql_query(query, conn)

df.to_excel("final_results.xlsx", index=False)

conn.close()

print("Excel file created: final_results.xlsx")