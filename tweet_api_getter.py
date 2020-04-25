## Alex Jones, Ashley Thompson
## SI 206 - Data Oriented Programming
## University of Michigan
##
## This file is used to gather data from the Tweepy API 
## regarding Tweets made by Elon Musk, adding a max of 20 
## new data points to the DB each time the functions are used.

import tweepy 
from utility import twitter_api_date_to_standard


def auth(): 
    """
    Authorizes the Tweepy api, and returns the API object.
    """
    auth = tweepy.OAuthHandler('wovXmgwNTBOaGiSvHHxFWA8c7', 'tRttLbA13KzUyTlFk96wwX9ACqzuI0RgqHYCBVcECgcSGB44Hw')
    auth.set_access_token('3299016720-cgw3M5OKYbf8BzUHgaVBdVctynygwLTYzngbLsT', '2SjWmJS6VHCd4ITPIKBWBXJdGBVG74ys2OhGoKoN2Pika')

    api = tweepy.API(auth)

    return api


def get_limited_tweet_data(cur,conn):
    """
    Gathers a limited (20 or less) amount of Elon Musk's tweets and stores them to
    our database each time this function is called. Works backwards chronologically,
    i.e. the first tweet stored will be the most recent tweet from the date range.

    Requires connections to the database.

    Prints a message indicating that new data was added successfully.
    """
    ## Authorize the Tweepy api with my api keys
    api = auth()

    ## The last Elon Musk tweet from April 15th (The Tweet just after the date limit).
    INITIAL_ID = 1250212864951857154 
    ## The constant number of tweets per 'page' returned by the Tweepy API.
    TWEETS_PER_PAGE = 200

    ## Check for the oldest tweet_id stored in the database.
    cur.execute("SELECT tweet_id, tweet_num FROM Tweets")
    tweet_data_list = cur.fetchall()
    if tweet_data_list == []:
        ## If none exists, set start to inital and tweet count to 0.
        start_id = INITIAL_ID
        tweet_count = 0
    else:
        ## Otherwise, set start to the oldest tweet_id and
        ## set the count to the updated count.
        start_id = tweet_data_list[0][0]
        tweet_count = tweet_data_list[0][1]
        for tweet, num in tweet_data_list:
            if tweet < start_id:
                start_id = tweet

            if num > start_id:
                tweet_count = num
    

    ## Calculate the current page number for smooth Tweepy navigation.
    page_number = (tweet_count//TWEETS_PER_PAGE +1)

    ## Query the Tweepy API in order to collect new data.
    elon_tweet_list = api.user_timeline(screen_name='elonmusk',max_id=start_id,count=100,page=page_number)
    new_data_point_count = 0
    for tweet in elon_tweet_list:
        ## Ensure a max of 20 new data points are stored in the database.
        if new_data_point_count < 20:
            ## Filter out replies.
            if tweet._json['in_reply_to_status_id'] == None:
                tweet_count += 1
                tweet_id = tweet._json['id']
                if tweet_id != start_id:
                    tweet_num = tweet_count
                    raw_date_str = tweet._json["created_at"]
                    day_of_the_week = raw_date_str[:3]
                    standard_date = twitter_api_date_to_standard(raw_date_str)
                    
                    ## Get the foreign key for the date.
                    try:
                        cur.execute("SELECT date_id FROM Dates WHERE date=?",(standard_date,))
                        date_id = cur.fetchone()[0]
                    except:
                        date_id = -1

                    ## Get the foreign key for day of the week.
                    try:
                        cur.execute("SELECT day_of_the_week_id FROM Days WHERE day_str=?",(day_of_the_week,))
                        day_of_the_week_id = cur.fetchone()[0]
                    except:
                        day_of_the_week_id = -1

                    ## Insert the new data into the database and increment the count of new data.
                    new_data_point_count += 1
                    cur.execute("INSERT INTO Tweets (tweet_id, tweet_num , date_id, day_of_the_week_id) VALUES (?,?,?,?)", 
                                (tweet_id, tweet_num, date_id, day_of_the_week_id))
    
    ## Print confirmation and commit the changes to the database.
    print("Tweet data collected.")
    conn.commit()