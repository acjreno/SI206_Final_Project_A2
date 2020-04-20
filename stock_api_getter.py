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


def get_limited_stock_data(company_str, cur, conn):
    """
    Function to gather data from the stock API, and then store a 
    maximum of 20 data points in the Stocks table of the DB. 

    Requires: company_str - A string representing the stock abbreviation of a company.
    Modifies: Upon initial run, stores the first 20 of 100 days worth of stock data 
              in the database. Creates a file to record the most recent date stored,
              and stores the next 20 dates on running the function again by reading 
              the supplemental file.
    Effects:  Prints a completion message when the data has been collected.
              Returns nothing.
    """
    ## Make the request to the stock API.
    r = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{company_str}?from=2019-11-19&to=2020-04-14")
    stock_price_list = json.loads(r.text)['historical']
    
    ## Calculate the index to resume data collection from using the dates in the database.
    cur.execute("SELECT Dates.date FROM Dates JOIN Stocks WHERE Dates.date_id = Stocks.date_id")
    fetched_dates = cur.fetchall()
    if fetched_dates == []:
        ## If none, start at the first day.
        start_index = 0
    else:
        ## Get the last (most recent) date and its index to resume collecting data.
        for day in stock_price_list:
            if stock_api_date_to_standard(day['date']) == fetched_dates[-1][0]:
                start_index = stock_price_list.index(day) + 1

    ## Add a maximum of 20 new data values to the Stocks database.
    ## Loop through a slice of the API response, starting at the index found above.
    new_data_point_count = 0
    for item in stock_price_list[start_index:]:
        if new_data_point_count < 20:
            ## Get the date_id from the Dates table based on a standardized date.
            cur.execute("SELECT date_id FROM Dates WHERE date=?", (stock_api_date_to_standard(item['date']),))
            date_id = cur.fetchone()[0]

            ## Get the closing stock price for a given day, our main metric.
            stock_price = item['close']

            ## Insert the data into the Stocks table and incrememtnt the count.
            cur.execute("INSERT INTO Stocks (date_id, stock_price) VALUES (?,?)", (date_id, stock_price))
            new_data_point_count += 1
        else:
            ## Print a completion message and exit the loop.
            print("Stock data collected.")
            break

    conn.commit()


