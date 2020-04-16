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
    print("----------------------------------------")
    print("    Tesla Stock and Sir Tweets-A-Lot    ")
    print("    A data collection project by A^2.   ")
    print("----------------------------------------\n")
    
    ## Create Elon_Value.db
    cur, conn = set_up_main_db()


    ## Restart the data to begin recollection?
    clear_s_data = input("Reset the Stock Table? (y/n): ")
    if clear_s_data.lower() == 'y':
        clear_stocks_table(cur, conn)
    clear_t_data = input("Reset the Stock Table? (y/n): ")
    if clear_t_data.lower() == 'y':
        clear_tweets_table(cur, conn)


    print("\nCurrent table statuses:")
    print(" - Not Implemented -\n")
    ## STATUS BARS!!!!

    ## Collect Data based on user input.
    collect_s_data = input("Collect more Stock Data? (y/n): ")
    if collect_s_data.lower() == 'y':
        ## collect more data
        get_limited_stock_data("TSLA", cur, conn)
    
    collect_t_data = input("Collect more Twitter Data? (y/n): ")
    if collect_t_data.lower() == 'y':
        get_limited_tweet_data(cur,conn)
        print("COLLECTEDDDD!!!")
        ## print status
        
    ## Draw Graphs?



if __name__ == '__main__':
    __main__()