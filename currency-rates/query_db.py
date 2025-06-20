import sqlite3


conn = sqlite3.connect("currency.db")
cur = conn.cursor()

# Get statement as input
query = input("SQL>>> ")

# If no input, run this statement
sql = "SELECT * symbol, price FROM brl_prices WHERE symbol = 'USD' ORDER BY timestamp DESC LIMIT 10;"

if query.strip() == "":
    print(sql)
    res = cur.execute(sql)
else:
    res = cur.execute(query)

for row in res:
    print(row)

if not (query.lower().startswith("select") or query.strip() == ""):
    commit = input("Commit changes? (y/n) ")
else:
    commit = str()

if commit.lower() == "y": conn.commit()

conn.close()