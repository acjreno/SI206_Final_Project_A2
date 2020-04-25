## Alex Jones, Ashley Thompson
## SI 206 - Data Oriented Programming
## University of Michigan
##
## This file contains various graphing functions to handle the 
## calculated data generated from the functions in calculations.py

import plotly.graph_objects as go
from calculations import calc_tweet_value, calc_daily_tweet_value

def tweet_value_graph(cur, conn):
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
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date_string_list, 
                             y=value_of_tweet,
                             mode='markers',
                             marker=dict(color='rgb(255, 242, 196)', size=12)))

    fig.update_layout(title='Value of a Single Tweet Per Date',
                      xaxis_title='Date',
                      yaxis_title='Tweet Value (Change in Stock Price / Number of Tweets)',
                      plot_bgcolor='rgb(47, 94, 86)')

    fig.show()


def daily_tweet_value_graph(cur, conn):
    """
    Use Plotly to graph the average change in 
    stock for a given weekday on a bar graph. 
    """
    ## Calculate the data.
    returned_list = calc_daily_tweet_value(cur, conn)

    ## Compile a list of weekdays and a list of the associated values.
    day_string_list = []
    average_daily_values = []
    for day, average_value in returned_list:
        day_string_list.append(day)
        average_daily_values.append(average_value)

    ## Plot the data.
    fig = go.Figure([go.Bar(x=day_string_list, y=average_daily_values)])
    fig.update_traces(marker_color='rgb(255, 242, 196)', 
                      marker_line_color='rgb(0,0,0)',
                      marker_line_width=2)

    fig.update_layout(title_text='Average Tweet Value by Day of the Week',
                      xaxis_title='Day of the Week',
                      yaxis_title='Average Value of a Single Tweet',
                      plot_bgcolor='rgb(47, 94, 86)')

    fig.show()