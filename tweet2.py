import tweepy
import ppsing #modulos de pre procesado
from gensim.models import Word2Vec
from unipath import Path

consumer_key = "YG9t6aMkiK3rvGdSbIkNbVKoG"
consumer_secret = "xhyivSyaesMQ2PvJdceI7BwBX3sjXxzhHsvC2pZcV0i2VTZ16R"
access_key = "879488168525004801-2wqBqwGmQzUNbvZLC1Oja7dyOF0ztLK"
access_secret = "ajMqqwF7TBf2tQZpLQyNZfe9jSLh8K6USWJHjXkp1Ohwg"

#configurar api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#ubicar chile    
places = api.geo_search(query="CHILE", granularity="country")
place_id = places[0].id


def get_all_tweets(num_tweets):

    #salida, lista de listas de frases
    alltweets = list()    

    #new_tweets= api.user_timeline(screen_name = screen_name,count=1,include_rts=False, tweet_mode="extended")

    counter=0
    while (counter<num_tweets):
        
        new_tweets = api.search(q="place:%s" % place_id,tweet_mode='extended')
        
        if len(new_tweets) != 0:

            #guarda el id del ultimo
            oldest=new_tweets[-1].id-1 
            
            #por cada iteracion agrega las frases nuevas del tweets
            for tweet in new_tweets:
                alltweets.extend(ppsing.processing(tweet.full_text))


            counter += 1
            new_tweets=[]
    #print(new_tweets[0].full_text)
    return alltweets

if __name__ == '__main__':


    num_tweets=int(input('ingrese cantidad de tweets:'))
    tweets=get_all_tweets(num_tweets)
    ppsing.save_dict()   
    print(tweets)

