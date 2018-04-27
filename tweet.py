import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
consumer_key = "YG9t6aMkiK3rvGdSbIkNbVKoG"
consumer_secret = "xhyivSyaesMQ2PvJdceI7BwBX3sjXxzhHsvC2pZcV0i2VTZ16R"
access_key = "879488168525004801-2wqBqwGmQzUNbvZLC1Oja7dyOF0ztLK"
access_secret = "ajMqqwF7TBf2tQZpLQyNZfe9jSLh8K6USWJHjXkp1Ohwg"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	counter = 0
	#keep grabbing tweets until there are no tweets left to grab
	while counter < 5:
		print ("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print ("...%s tweets downloaded so far" % (len(alltweets)))
		counter += 1
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode()] for tweet in alltweets]
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter=" ",quotechar="|",quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
		print("caca")
	
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("sebastianpinera")
