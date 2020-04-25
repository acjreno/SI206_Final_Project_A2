## Alex Jones, Ashley Thompson
## SI 206 - Data Oriented Programming
## University of Michigan
##
## The main function for our data collection project.

from utility import (set_up_main_db, 
                     twitter_api_date_to_standard, 
                     stock_api_date_to_standard,
                     clear_stocks_table,
                     clear_tweets_table,
                     print_data_status)

from stock_api_getter import get_limited_stock_data
from tweet_api_getter import get_limited_tweet_data

from calculations import calc_tweet_value, calc_daily_tweet_value
from graphs import tweet_value_graph

def __main__():
    print("----------------------------------------")
    print("    Tesla Stock and Sir Tweets-A-Lot    ")
    print("    A data collection project by A^2.   ")
    print("----------------------------------------\n")
    
    ## Create Elon_Value.db
    cur, conn = set_up_main_db()


    ## Restart the data to begin recollection?
    reset = input("Reset any tables? (y/n): ")
    if reset.lower() == 'y':
        clear_s_data = input("Reset the Stock Table? (y/n): ")
        if clear_s_data.lower() == 'y':
            clear_stocks_table(cur, conn)
        clear_t_data = input("Reset the Tweet Table? (y/n): ")
        if clear_t_data.lower() == 'y':
            clear_tweets_table(cur, conn)


    print("\nCurrent table statuses:")
    s_full = print_data_status("Stocks", cur, conn)
    t_full = print_data_status("Tweets", cur, conn)
    print(" ")

    ## Collect Data based on user input.
    if not s_full:
        collect_s_data = input("Collect more Stock Data? (y/n): ")
        if collect_s_data.lower() == 'y':
            get_limited_stock_data("TSLA", cur, conn)
    
    if not t_full:
        collect_t_data = input("Collect more Twitter Data? (y/n): ")
        if collect_t_data.lower() == 'y':
            get_limited_tweet_data(cur,conn)
        
    ## Calculate and display charts based on user input.
    if s_full and t_full:
        calculate_data = input("\nCalculate and graph visualizations? (y/n): ")
        if calculate_data == 'y':
            #tweet_value_graph(cur, conn)
            calc_daily_tweet_value(cur, conn)


if __name__ == '__main__':
    __main__()
