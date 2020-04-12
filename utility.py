## Alex Jones, Ashley Thompson
## SI 206 - Data Oriented Programming
## University of Michigan
##
## This file contains various utility functions and data points that are 
##  useful in the collection and sorting of data obtained from the API's.

import time
import re

def stock_api_date_to_standard(date_str):
    """
    Converts a date string in the format returned by the stock prices 
    API at financialmodelinggroup.com and converts it into the standard form

    MM/DD/YYYY

    where single digit months or days are preceded by a zero. 
    For use in creating a standardized primary key, the date of a data point.
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
    pass