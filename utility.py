## Alex Jones, Ashley Thompson
## SI 206 - Data Oriented Programming
## University of Michigan
##
## This file contains various utility functions and data points that are 
##  useful in the collection and sorting of data obtained from the API's.

import sqlite3
import requests
import json
import os

def set_up_main_db():
    """
    Creates the elon_value.db file and populates the date_id table.
    """
    ## Connect to the database.
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'Elon_Value.db')
    cur = conn.cursor()

    ## Create our Dates table.
    cur.execute("CREATE TABLE IF NOT EXISTS Dates (date_id INTEGER PRIMARY KEY, date TEXT)")
    
    ## Populate the Dates table using a cheeky call to the stock API.
    if (cur.execute("SELECT date_id FROM Dates").fetchone() == tuple()):
        r = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/TSLA?from=2019-11-19&to=2020-04-14")
        response = json.loads(r.text)

        date_id = 0
        for item in response['historical']:
            date = stock_api_date_to_standard(item['date'])
            cur.execute("INSERT INTO Dates (date_id, date) VALUES (?,?)", (date_id, date))
            date_id += 1

    ## Commit the changes to the db file.
    conn.commit()

    return cur, conn


def clear_stocks_table(cur, conn):
    """
    Deletes the Stocks table to allow for a data reset.
    Prints a confirmation statement when a table is dropped.
    """
    cur.execute("DROP TABLE IF EXISTS Stocks")
    conn.commit()
    
    print("Stocks table reset. Ready for new data collection.")


def clear_tweets_table(cur, conn):
    """
    Deletes the Tweets table to allow for a data reset.
    Prints a confirmation statement when a table is dropped.
    """
    cur.execute("DROP TABLE IF EXISTS Tweets")
    conn.commit()
    
    print("Tweets table reset. Ready for new data collection.")


def stock_api_date_to_standard(date_str):
    """
    Converts a date string in the format returned by the stock prices 
    API at financialmodelinggroup.com and converts it into the standard form

    MM/DD/YYYY

    where single digit months or days are preceded by a zero. 
    For use in creating a standardized primary key: the date of a data point.
    """
    # 2020-04-07
    return f"{date_str[5:7]}/{date_str[-2:]}/{date_str[:4]}"


def twitter_api_date_to_standard(date_str):
    """
    Converts a date string in the format returned by the twitter API
    at twitter.com and converts it into the standard form

    MM/DD/YYYY

    where single digit months or days are preceded by a zero. 
    For use in creating a standardized primary key, the date of a data point.
    """
    # Tue Apr 14 23:59:35 +0000 2020
    months = {"Nov":"11", "Dec":"12", "Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04"}

    date_str_lst = date_str.split()
    return f"{months.get(date_str_lst[1])}/{date_str_lst[2]}/{date_str_lst[-1]}"