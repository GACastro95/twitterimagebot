import tweepy
from datetime import datetime
from threading import Timer
import os, random


folder_path = ""
def credentials():
	consumer_key = ''
	consumer_secret = ''
	access_token = ''
	access_token_secret = ''
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	return api

def tweet_photos(api):
	for x in range(len(next(os.walk(folder_path))[2])):
		file = random.choice(os.listdir(folder_path))
		status = ""
		try:
			api.update_with_media(filename=folder_path + "/" + x, status=status)
			print("Tweeted!")
			break
			sleep(86400)
		except Exception as e:
			print("Failed!")
			break

def reply_photos(api):
	TRIGGERS = ('@twitterbot send me something')

	for tweet in tweets:
		if tweet.text in TRIGGERS:
			sn = tweet.user.screen_name
			x = random.choice(os.listdir(folder_path))
			status = '@{}'.format(sn)
			api.update_with_media(filename=folder_path + "/" + x, status=status)
			print("Tweeted!")

if __name__ == "__main__":
	tweet_photos(credentials())
	reply_photos(credentials())