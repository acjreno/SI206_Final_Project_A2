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

    ## The last Elon Musk tweet from April 14th
    intial_id = 1250212134971043840 

    ##create the tweets table(Primary key=Tweet_id)
    cur.execute("CREATE TABLE IF NOT EXISTS Tweets (tweet_id INTEGER PRIMARY KEY, tweet_num INTEGER , date_id INTEGER)")

    ##Check for most recent tweet id
    cur.execute("SELECT tweet_id FROM Tweets")
    if cur.fetchall() == []:
        ##if none exists, set start to inital
        start_id = intial_id
    else:
        ##get most recent id
        start_id = max(cur.fetchall())


    Tweets_per_page = 200
    cur.execute("SELECT tweet_num FROM Tweets")
    if cur.fetchall() == []:
        ##if none exists, set start to 1 for first tweet
        tweet_count = 1
    else:
        ##if tweets exist, fetch last tweet 
        tweet_count = max(cur.fetchall())

    page_number = (tweet_count//200 +1)

    ##get 100 items from tweepy
    elon_tweet_list = api.user_timeline(screen_name='elonmusk',max_id=start_id,count=100,page=page_number)

    for tweet in elon_tweet_list:
        tweet_count += 1
        tweet_id = tweet._json['id']
        tweet_num = tweet_count
        date = twitter_api_date_to_standard(tweet._json["created_at"])
        try:
            cur.execute("SELECT date_id FROM Dates WHERE date=?",(date,))
            date_id = cur.fetchone()[0]
        except:
            date_id = -1
        
        cur.execute("INSERT INTO Tweets (tweet_id, tweet_num , date_id) VALUES (?,?,?)",(tweet_id,tweet_num,date_id))
    
    conn.commit()


            




