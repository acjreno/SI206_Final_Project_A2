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

    ##Authorize the Tweepy api with my api keys
    api = auth()

    ## The last Elon Musk tweet from April 15th(one before the counted id)
    intial_id = 1250212864951857154 

    ##create the tweets table(Primary key=Tweet_id)
    cur.execute("CREATE TABLE IF NOT EXISTS Tweets (tweet_id INTEGER PRIMARY KEY, tweet_num INTEGER , date_id INTEGER)")

    ##Check for most recent tweet id
    cur.execute("SELECT tweet_id FROM Tweets")
    tweet_id_list = cur.fetchall()
    if tweet_id_list == []:
        ##if none exists, set start to inital
        start_id = intial_id
    else:
        ##get most recent id
        start_id = tweet_id_list[0][0]
        for tweet in tweet_id_list:
            if tweet[0] < start_id:
                start_id = tweet[0]


    tweets_per_page = 200
    cur.execute("SELECT tweet_num FROM Tweets")
    tweet_num_list = cur.fetchall()
    if tweet_num_list == []:
        ##if none exists, set start to 1 for first tweet
        tweet_count = 0
    else:
        ##if tweets exist, fetch last tweet 
        tweet_count = tweet_num_list[0][0]
        for num in tweet_num_list:
            if num[0] > start_id:
                tweet_count = num[0]

    page_number = (tweet_count//tweets_per_page +1)

    ##get 100 items from tweepy
    elon_tweet_list = api.user_timeline(screen_name='elonmusk',max_id=start_id,count=100,page=page_number)
    new_data_point_count = 0
    for tweet in elon_tweet_list:
        if new_data_point_count < 20:
            if tweet._json['in_reply_to_status_id'] == None:
                tweet_count += 1
                tweet_id = tweet._json['id']
                if tweet_id != start_id:
                    tweet_num = tweet_count
                    date = twitter_api_date_to_standard(tweet._json["created_at"])
                    try:
                        cur.execute("SELECT date_id FROM Dates WHERE date=?",(date,))
                        date_id = cur.fetchone()[0]
                    except:
                        date_id = -1
                
                    new_data_point_count += 1
                    cur.execute("INSERT INTO Tweets (tweet_id, tweet_num , date_id) VALUES (?,?,?)",(tweet_id,tweet_num,date_id))
    
    conn.commit()


            




