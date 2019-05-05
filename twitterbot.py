import tweepy
import time
import os, random
import datetime
from multiprocessing import Process
import json

folder_path = "./images"
used_folder_path = "./images/used"
keywords = ['@bot phrase']
def credentials():
	consumer_key = ''
	consumer_secret = ''
	access_token = ''
	access_token_secret = ''
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

	return api

def tweet_photos(api):
	for x in range(len(next(os.walk(folder_path))[2])):
		file = random.choice(os.listdir(folder_path))
		status = ""
		try:
			if data["last-tweet-time"] == "":
				update_last_tweet_time(api)
			try:
				timed = datetime.datetime.now() - datetime.datetime.strptime(data["last-tweet-time"], '%Y-%m-%d %H:%M:%S')
			except:
				timed = datetime.datetime.now() - data["last-tweet-time"]
			if timed >= datetime.timedelta(hours=24):
				api.update_with_media(filename=folder_path + "/" + file, status=status)
				update_last_tweet_time(api)
				os.rename(folder_path + "/" + file, used_folder_path + "/" + file)
				print("Tweeted!")
			else:
				break
		except tweepy.TweepError as e:
			print(e.reason)
			print("Failed daily tweet!")
			break

def update_last_tweet_time(api):
	last_tweet = api.user_timeline(id=api.me, exclude_replies=True, include_rts=False)
	with open('./last_tweets.json', 'w') as write_file:
		data["last-tweet-time"] = last_tweet[0].created_at
		print(data["last-tweet-time"])
		json.dump(data, write_file, default = converter)

def converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

class MyStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		tweet = status.text
		directory = tweet[len('@k_o_n_a_m_i_bot '):]
		print(directory)
		sn = status.user.screen_name
		tweetId = status.id
		x = random.choice(os.listdir(folder_path + "/" + directory))
		status = '@{}'.format(sn)
		credentials().update_with_media(filename=folder_path + "/" + directory + "/" + x, status=status, in_reply_to_status_id = tweetId)
		print("Tweeted!")

if __name__ == "__main__":
	if os.path.exists('./last_tweets.json'):
		with open('./last_tweets.json', 'r') as read_file:
			data = json.load(read_file)
			print("Last Tweets json file found!")
	else:
		with open('./last_tweets.json', 'w') as write_file:
			data = {
			"last-tweet-time": "",
			"last-reply-id": ""
			}
			json.dump(data, write_file)
		print("Last Tweets json file created!")
	myStreamListener = MyStreamListener(credentials())
	myStream = tweepy.Stream(auth = credentials().auth, listener=myStreamListener)
	myStream.filter(track=keywords, is_async=True)
	while True:
		tweet_photos(credentials())
