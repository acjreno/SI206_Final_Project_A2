import tweepy 


auth = tweepy.OAuthHandler('wovXmgwNTBOaGiSvHHxFWA8c7', 'tRttLbA13KzUyTlFk96wwX9ACqzuI0RgqHYCBVcECgcSGB44Hw')
auth.set_access_token('3299016720-cgw3M5OKYbf8BzUHgaVBdVctynygwLTYzngbLsT', '2SjWmJS6VHCd4ITPIKBWBXJdGBVG74ys2OhGoKoN2Pika')

api = tweepy.API(auth)

start_id = 1250212134971043840
TWEETS_PER_PAGE = 200
page_number = 1


elon_tweet_list = api.user_timeline(screen_name='elonmusk',max_id=start_id,count=20,page=page_number)



