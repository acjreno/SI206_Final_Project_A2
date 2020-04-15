## Alex Jones, Ashley Thompson
## SI 206 - Data Oriented Programming
## University of Michigan
##
## The main function for our data collection project.

from utility import (set_up_main_db, 
                     twitter_api_date_to_standard, 
                     stock_api_date_to_standard,
                     clear_stocks_table,
                     clear_tweets_table)

from stock_api_getter import get_limited_stock_data
from tweet_api_getter import get_limited_tweet_data

def __main__():
    #print("Welcome to Elon's Expensive Stocks, a data collection project by Ashley Thompson and Alex ")
    
    ## Create Elon_Value.db
    cur, conn = set_up_main_db()

    clear_stocks_table(cur, conn)
    ## Restart?
    ## Collect Data?
    print("Current table statuses:")
    ## STATUS BARS!!!!


    collect_s_data = input("Collect more Stock Data? (y/n): ")
    if collect_s_data == 'y':
        ## collect more data
        get_limited_stock_data("TSLA", cur, conn)
        ## print status
        print("Stock data collected.")
        ## print count in table
    
    collect_t_data = input("Collect more Twitter Data? (y/n): ")
    if collect_t_data == 'y':
        get_limited_tweet_data(cur,conn)
        print("COLLECTEDDDD!!!")
        ## print statusn
        ## print count in table

    ## Draw Graphs?



if __name__ == '__main__':
    __main__()