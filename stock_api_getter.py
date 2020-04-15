## Alex Jones, Ashley Thompson
## SI 206 - Data Oriented Programming
## University of Michigan
##
## This file is used to gather the data from the API hosted at financialmodelinggroup.com.
## Each time it is run, it adds Tesla stock data to the Stocks table in our database,
## 20 days at a time, with days as the primary key of both the Stocks and Tweets tables.

import requests
import json

## Include utility functions to convert time and dates.
from utility import stock_api_date_to_standard

def get_api_stock_data(company_str):
    """
    Testing function that gathers data for 100 days and stores them in a file for offline viewing.
    """
    r = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{company_str}?timeseries=100")
    response = json.loads(r.text)

    with open('TSLA_100_days_stock.json', 'w') as f:
        f.write(r.text)

    for historical in response["historical"]:
        print(historical['date'])


def get_limited_stock_data(company_str, cur, conn):
    """
    Function to gather data from the stock API, and then store a 
    maximum of 20 data points in the Stocks table of the DB. 

    Requires: company_str - A string representing the Stock abbreviation of a company.
    Modifies: Upon initial run, stores the first 20 of 100 days worth of stock data 
              in the database. Creates a file to record the most recent date stored,
              and stores the next 20 dates on running the function again by reading 
              the supplemental file.

    """
    cur.execute("CREATE TABLE IF NOT EXISTS Stocks (date_id INTERGER PRIMARY KEY, stock_price REAL)")
    
    
    r = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{company_str}?from=2019-11-19&to=2020-04-14")
    response = json.loads(r.text)

    cur.execute("SELECT date_id FROM Stocks")

    for day in response['historical']:
        day['date']

        #cur.execute("INSERT INTO Stocks")

    conn.commit()


