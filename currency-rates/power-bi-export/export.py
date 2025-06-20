# Run this script using venv-BI
import pandas as pd
import sqlite3

# Inside PowerBI, the absolute path to .db file must be provided as argument to .connect()
conn = sqlite3.connect("_")
cur = conn.cursor()

sql = "SELECT * FROM brl_prices;"

res = cur.execute(sql)

df = pd.DataFrame.from_records(res.fetchall(), columns=["timestamp", "symbol", "price"])
conn.close()
print(df)

if __name__ == "__main__":
    df.to_csv("brl_prices.csv", index=False, encoding="utf-8")