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

def write_csv_file(filename, fieldnames, data):
    """
    Writes the calculated data to a .csv file with the passed filename.

    filename - The name for the file, without the .csv extension.
    fieldnames - A list of strings, each being a fieldname.
    data - A list of tuples containing the data, 
           in order of the passed fieldnames.
    """
    ## Create the header string based off passed fieldnames.
    header_str = ""
    for name in fieldnames[:-1]:
        header_str = header_str + name + ","
    header_str = header_str + fieldnames[-1] + '\n'

    ## Write the data to the .csv file.
    with open(f"{filename}.csv", 'w') as f:
        f.write(header_str)
        
        for item in data:
            line = ""
            for value in item[:-1]:
                line = line + str(value) + ","
            line += str(item[-1])

            f.write(line +'\n')


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

    ## Generate a list in the format [(date, avg_tweet_value), ...]
    calculated_data_list = []
    prev_date_data = date_id_dict[0]
    for date_id in range(1, 100):
        ## Get the date str from the Dates table in our DB.
        cur.execute("SELECT date FROM Dates WHERE date_id=?", (date_id,))
        date_str = cur.fetchone()[0]

        ## Calculate the average value of the tweets per day.
        date_data = date_id_dict[date_id]
        try: 
            avg_tweet_value = round((date_data[1] - prev_date_data[1]) / date_data[0], 3)
        except ZeroDivisionError:
            avg_tweet_value = "None"

        ## Add the info to the list.
        calculated_data_list.append((date_str, avg_tweet_value))

        ## Increment the day.
        prev_date_data = date_data

    ## Write the info to a file.
    fieldnames = ["date", "avg_tweet_value"]
    write_csv_file("tweet_value", fieldnames, calculated_data_list)
    
    ## Return the data for graphing.
    return calculated_data_list


def calc_daily_tweet_value(cur, conn):
    """
    Calculate the average value for a single tweet by Elon Musk
    per day of the week.
    Requires: cur, conn - Connections to the database file.
    """
    cur.execute("""SELECT Dates.date_id, Tweets.tweet_num, 
                          Stocks.stock_price, Tweets.day_of_the_week_id 
                   FROM Dates JOIN Stocks ON Dates.date_id = Stocks.date_id 
                   LEFT JOIN Tweets ON Stocks.date_id = Tweets.date_id""")

    ## In the form [(tweet_num, stock_price, day_of_the_week)]
    data_tup_list = cur.fetchall()

    ## Generate a dict in the format 
    ## {date_id: (tweet_count, stock_price, day_of_the_week)}
    date_id_dict = {}
    for tup in data_tup_list:
        date_id = tup[0]
        
        has_tweet = tup[1]
        stock_price = tup[2]
        day_of_the_week = tup[3]

        tweet_count = date_id_dict.get(date_id, (0, None))[0]
        if has_tweet:
            tweet_count += 1
        
        date_id_dict[date_id] = (tweet_count, stock_price, day_of_the_week)

    ## New dictionary??