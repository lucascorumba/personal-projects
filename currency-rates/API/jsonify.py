import sqlite3
import json

def export_json(dp_path="/path/to/currency.db"):
    """
    Query database for every record and save fetched data in a .json file.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM brl_prices;")
    res = cur.fetchall()
    conn.close()

    res = parse_json(res)

    with open("brl_prices.json", "w") as f:
        json.dump(res, f)
        print("JSON file saved")


def export_query_json(db_path="/path/to/currency.db", lookup=None):
    """
    Query database for all records or for selected symbol. In both cases, return
    fetched data as a string in JSON format.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    if lookup:
        sql = f"SELECT * FROM brl_prices WHERE symbol = '{lookup.upper()}';"
    else:
        sql = "SELECT * FROM brl_prices;"
    cur.execute(sql)
    res = cur.fetchall()
    conn.close()

    return json.dumps(parse_json(res))


def parse_json(response):
    """
    Get response from database query and parse data as a dictionary.
    """
    data = [
        {
            "timestamp": row[0],
            "symbol": row[1],
            "price": row[2]
        }
        for row in response
    ]

    return {"data": data}


if __name__ == "__main__":
    export_json()