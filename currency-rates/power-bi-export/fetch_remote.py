# Run this script using venv-BI
import requests
import pandas as pd

# Replace with credentials
params = {"auth": "_"}

response = requests.get("https://USERNAME.pythonanywhere.com/endpoint", params=params)

df = pd.DataFrame.from_records(response.json()["data"])
print(df)

if __name__ == "__main__":
    df.to_csv("brl_prices.csv", index=False, encoding="utf-8")