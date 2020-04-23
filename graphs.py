## Alex Jones, Ashley Thompson
## SI 206 - Data Oriented Programming
## University of Michigan
##
## This file contains various graphinf functions to handle the 
## calculated data from other parts of the project.

import plotly.express as px
from calculations import calc_tweet_value

def tweet_value_graph(cur,conn):
    """
    Use Plotly to graph the date on the x-axis and 
    the average value of Elon's tweets on that day on the y-axis.
    """
    ## Calculate the data.
    returned_list = calc_tweet_value(cur,conn)
    
    ## Compile a list of dates and a list 
    ## of values where the avg_tweet_value != "None".
    date_string_list = []
    value_of_tweet = []
    for date_str, avg_tweet_value in returned_list:
        if avg_tweet_value != "None":
            date_string_list.append(date_str)
            value_of_tweet.append(avg_tweet_value)
    
    ## Plot the data.
    fig = px.scatter(x=date_string_list, y=value_of_tweet)
    fig.show()