## Alex Jones, Ashley Thompson
## SI 206 - Data Oriented Programming
## University of Michigan
##
## This file is used to gather the data from the API hosted at financialmodelinggroup.com.
## Each time it is run, it adds Tesla stock data to the Stocks table in our database,
## 20 days at a time, with days as the primary key of both the Stocks and Tweets tables.

import requests
import json
import time

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


def __main__():
    # try:
    #     with open('TSLA_100_days_stock.json') as f:
    #         data = json.loads(f.read())
    #         print(len(data['historical']))
    #     print("Didn't Access The API!")
    # except FileNotFoundError:
    #     get_api_stock_data('TSLA')


if __name__ == '__main__':
    __main__()