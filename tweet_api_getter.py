import tweepy
import requests
import json

auth = tweepy.OAuthHandler('wovXmgwNTBOaGiSvHHxFWA8c7', 'tRttLbA13KzUyTlFk96wwX9ACqzuI0RgqHYCBVcECgcSGB44Hw')
auth.set_access_token('3299016720-cgw3M5OKYbf8BzUHgaVBdVctynygwLTYzngbLsT', '2SjWmJS6VHCd4ITPIKBWBXJdGBVG74ys2OhGoKoN2Pika')

api = tweepy.API(auth)

# user = api.get_user('elonmusk')
# print(user.followers_count)

# for status in tweepy.Cursor(user.user_timeline).items(200):
#     print(status)

r = requests.get('https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=twitterapi&count=2')
response = json.loads(r.text)

print(response)

