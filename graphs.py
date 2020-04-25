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
    colors = ['rgb(241, 230, 187)' if value > 0 else 'rgb(224, 103, 103)' for value in value_of_tweet]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date_string_list, 
                             y=value_of_tweet,
                             mode='markers',
                             marker=dict(color=colors, size=12)))

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Black')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Black')
    fig.update_yaxes(zeroline=True, zerolinewidth=4, zerolinecolor='Black')

    fig.update_layout(title='Value of a Single Tweet Per Date',
                      xaxis_title='Date',
                      yaxis_title='Tweet Value (Change in Stock Price / Number of Tweets)',
                      plot_bgcolor='rgb(43, 58, 62)',
                      paper_bgcolor="Black",
                      font=dict(size=16, color="White"))

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
    colors = ['rgb(241, 230, 187)',
              'rgb(241, 230, 187)',
              'rgb(241, 230, 187)',
              'rgb(241, 230, 187)',
              'rgb(224, 103, 103)']

    fig = go.Figure([go.Bar(x=day_string_list, 
                            y=average_daily_values,
                            marker_color=colors)])
    fig.update_traces(marker_line_color='Black',
                      marker_line_width=1)

    fig.update_yaxes(zeroline=True, zerolinewidth=4, zerolinecolor='Black')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Black')

    fig.update_layout(title_text='Average Tweet Value by Day of the Week',
                      xaxis_title='Day of the Week',
                      yaxis_title='Average Value of a Single Tweet',
                      plot_bgcolor='rgb(43, 58, 62)',
                      paper_bgcolor="Black",
                      font=dict(size=16, color="White"))

    # font=dict(family="Arial, sans-serif", 
    #                             size=26, 
    #                             color="rgb(0, 0, 0)")

    fig.show()