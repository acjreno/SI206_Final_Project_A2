## Alex Jones, Ashley Thompson
## SI 206 - Data Oriented Programming
## University of Michigan
##
## This file contains various graphinf functions to handle the 
## calculated data from other parts of the project.

import plotly.express as px
from calculations import calc_tweet_value

def tweet_value_graph(cur,conn):
    returned_list = calc_tweet_value(cur,conn)
    dates = []
    value_of_tweet = []
    for date_id,num_tweets,stock_change in returned_list:
        if num_tweets != 0:
            dates.append(date_id)
            value_of_tweet.append(stock_change/num_tweets)
    
    date_string_list = []
    for date in dates:
        cur.execute("SELECT date FROM Dates WHERE date_id=?", (date,))
        date_string_list.append(cur.fetchone()[0])


    fig = px.scatter(x=date_string_list, y=value_of_tweet)
    fig.show()