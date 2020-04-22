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
    if (cur.execute("SELECT date_id FROM Dates").fetchone() == None):
        r = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/TSLA?from=2019-11-19&to=2020-04-14")
        response = json.loads(r.text)

        date_id = 0
        for item in response['historical']:
            date = stock_api_date_to_standard(item['date'])
            cur.execute("INSERT INTO Dates (date_id, date) VALUES (?,?)", (date_id, date))
            date_id += 1

    ## Commit the changes to the db file.
    conn.commit()

    ## Create the Stocks table if it has been deleted to reset data collection.
    cur.execute("CREATE TABLE IF NOT EXISTS Stocks (date_id INTERGER PRIMARY KEY, stock_price REAL)")
    conn.commit()
    
    ##create the tweets table(Primary key=Tweet_id)
    cur.execute("CREATE TABLE IF NOT EXISTS Tweets (tweet_id INTEGER PRIMARY KEY, tweet_num INTEGER , date_id INTEGER)")
    conn.commit()

    return cur, conn


def clear_stocks_table(cur, conn):
    """
    Deletes the Stocks table to allow for a data reset.
    Prints a confirmation statement when a table is dropped.
    """
    cur.execute("DROP TABLE IF EXISTS Stocks")
    cur.execute("CREATE TABLE IF NOT EXISTS Stocks (date_id INTERGER PRIMARY KEY, stock_price REAL)")
    conn.commit()
    
    print("Stocks table reset. Ready for new data collection.")


def clear_tweets_table(cur, conn):
    """
    Deletes the Tweets table to allow for a data reset.
    Prints a confirmation statement when a table is dropped.
    """
    cur.execute("DROP TABLE IF EXISTS Tweets")
    cur.execute("CREATE TABLE IF NOT EXISTS Tweets (tweet_id INTEGER PRIMARY KEY, tweet_num INTEGER , date_id INTEGER)")
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


def print_data_status(table_name, cur, conn):
    """
    Prints a nice-looking status bar to represent how complete each tables'
    data set is. 
    Requires: table_name - MUST be one of Tweets, Stocks.
              cur, conn - Connections to Elon_Value.db
    Effects: Prints a status bar to the main console.
             Returns False until the data sets are true, then returns True.
    """
    cur.execute(f"SELECT date_id FROM {table_name}")
    date_id_list = [tup[0] for tup in cur.fetchall()]

    if table_name == "Stocks":
        bar_status_int = (max(date_id_list + [0]) + 1) // 10
    elif table_name == "Tweets":
        ## Remove the -1 dates from the status.
        date_id_list = [date_id for date_id in date_id_list if date_id != -1]
        bar_status_int = (100 - (min(date_id_list + [99]))) // 10

    if bar_status_int < 10:
        status = '+' * bar_status_int + '-' * (10 - bar_status_int)
        print(f"{table_name}: {status} >> {bar_status_int * 10}%")
        return False
    elif bar_status_int == 10:
        print(f"{table_name}: Dataset Complete.")
        return True