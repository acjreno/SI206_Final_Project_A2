## Alex Jones, Ashley Thompson
## SI 206 - Data Oriented Programming
## University of Michigan
##
## This file contains various calculating functions to handle the 
## collected data from other parts of the project.


## Calculate tweets per day

## Calculate stock change in price from one day to the next
    ## i.e. Day 1 has a value of day 1 - day 0
    ## Won't include the first day in the graphs

## Except the first day, stock_price_change[day] / tweets_per_day[day]
    ## Final list: [3.4, -1.2, 'undf'... 1.34] * len() = 99
    ## select stock_price,  join on date_id Stocks, Tweets

def calc_tweet_value(cur, conn):
    """
    Calculate the value of a single tweet per day based on the change in Tesla's stock price.
    Requires: cur, conn - Connections to the database file.
    """
    selected_data = cur.execute("""SELECT Dates.date_id, Stocks.stock_price, Tweets.tweet_num 
                                   FROM Dates JOIN Stocks ON Dates.date_id = Stocks.date_id 
                                   LEFT JOIN Tweets ON Stocks.date_id = Tweets.date_id""")

    data_tup_list = selected_data.fetchall()
    
    ## Generate a dict in the format {date_id: (tweet_count, stock_price)}
    date_id_dict = {}
    for tup in data_tup_list:
        date_id = tup[0]
        stock_price = tup[1]
        has_tweet = tup[2]

        tweet_count = date_id_dict.get(date_id, (0, None))[0]
        if has_tweet:
            tweet_count += 1
        
        date_id_dict[date_id] = (tweet_count, stock_price)

    ## Generate a list in the format [(tweets, stock_price_date - stock_price_previous)]
    ## Can be indexed as date_id - 1 (i.e. index 0 is date_id 1)
    calculated_data_list = []
    prev_date_data = date_id_dict[0]
    for date_id in range(1, 100):
        date_data = date_id_dict[date_id]

        calculated_data_list.append((date_data[0], round(date_data[1] - prev_date_data[1], 3)))

        prev_date_data = date_data