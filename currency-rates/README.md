# Currency Rates Fetcher
ETL pipeline developed to automate the aquisition, processing, storage and continuous availability of currency exchange rates.

This process can work both locally and on the cloud, being deployed on [PythonAnywhere](pythonanywhere.com).

Makes use of the [exchangerates API](https://exchangeratesapi.io/) as data source and uses python's built-in module `sqlite3` to create and connect to a simple [SQLite3](https://www.sqlite.org/docs.html) database.
[Flask](https://flask.palletsprojects.com/en/stable/) was used to create the API, wich was set up to serve as data source for vizualization tools.

Setting up this API enabled easy access of work-ready data for both on-premise tools (PowerBI in this project) as well as web applications such as Grafana.
The *PythonAnywhere* Cloud service provides a scheduling similar to a `cron` job. This automated daily routine for ingestion ensures the data is always up to date.

## Overview
* **Data source**: [ExchangerateAPI](https://exchangeratesapi.io/documentation/)
* **Database**: SQLite3  via *[`sqlite3` python module]*(https://docs.python.org/3/library/sqlite3.html)
* **API**: [Flask](https://flask.palletsprojects.com/en/stable/quickstart/)
* **Visualization**: PowerBI and [Grafana Cloud](https://grafana.com/docs/grafana/latest/)
* **Execution**: Locally and cloud (via [PythonAnywhere cloud](https://help.pythonanywhere.com/pages/))
* **Refreshing**: `cron` style locally and via PythonAnywhere service.

## About the Scripts
* `get_rates.py`
    * Connection to database, processing and storage of fetched data.
* `utils.py`
    * Holds the logic for exchangerate API authentication and request. Also performs some simple data transformation procedures.
* `query_db.py`
    * Script to query the database using python's built-in module.
* `schedule.py`
    * Very simple "scheduler", only relies on `time`and `datetime` modules. 
    Prompts for number of fetches to be executes as well as hours and minutes intervals. Keeps process sleeping for 45 minutes and then checks if queued scheduled time is already reached. If so, it triggers `get_rates.py` to get and store API data.
    * *With the API running, this method is only a second choice.*
* `../power-bi-export`
    * This folder holds the script used by PowerBI to ingest or refresh data from a local or remote data source.
    * As PowerBI demands `pandas` and `matplotlib` modules to be imported in order to run a python script, both of them need to be installed. 
    * |__ `/fetch_remote.py`
        * Produces a `pd.DataFrame` fetching data from the Flask API running remotely on [pythonanywhere](pythonanywhere.com).
    * |__ `/export.py`
        * Produces a `pd.DataFrame` getting data localy. *The only automation implemented for this routine is the `schedule.py`, which still needs to be run daily.*    
        * When running localy, another solution is to install the [SQLite ODBC driver](http://www.ch-werner.de/sqliteodbc/) and connect PowerBI directly to the database. This removes the need of creating a `venv` and installing both `pandas` and `matplotlib`.

    * If using a `venv`, pay attention while setting python path. PowerBI should be provided the `.../venv/Scripts` folder instead of the global install, the former holds the `venv` interpreter.
* `../API`
    * In this folder are the scripts responsible for creating the API endpoint and routines for filtering and parse the stored data into `JSON`.
    * |__`/jsonify.py`
        * Procedures to serialize stored data into `JSON`. 
            * There is a routine that runs daily, along with the `runner` function of `get_rates.py`, generating a new `.json` file with all the data stored in the `.db` file. Even if this approach is not efficient in terms of storage, it was prefered as the processing time of the free tier is very limited and the files are pretty small. Everytime the endpoint was hit without aditional parameters, this `.json` file is used for the response.
            * When the request carries the `lookup` parameter, instead of responding with data from file processed ahead of time, another funtion is triggered to query the database for a refined result. As for now, it only allows filtering of one currency.
    * |__`/supply.py`
        * The API runs the same processes as the local version (`get_rates.py` and `utils.py`), wich in turn are managed by the service scheduler. This file defines the Flask app and it's enpoint route, as well as the procedures to be run depending on the request parameters.

## Requirements
It's recommended to not install required packages globally, but locally under a project subfolder using `venv`: 
```
python3 -m venv venv-name

# Windows
venv-name\Scripts\activate.bat    # cmd
venv-name\Scripts\activate.ps1    # PowerShell

# Unix
source venv-name/bin/activate
```
Libraries:
```
pip install requests

# Pandas and matplotlib are needed to export data to PowerBI through python script ingestion
pip install pandas
pip install matplotlib

# For the API
pip install Flask
```

## Usage
```
# To fetch latest rates
python3 get_rates.py

# To query the database through .py script
python3 query_db.py

# To schedule fetches
python3 schedule.py
```