import tweepy
import ppsing #modulos de pre procesado
from gensim.models import Word2Vec
from time import sleep

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


def get_all_tweets(cant_tweets,oldest):

    print('bajando...\n')
    #salida, lista de listas de frases
    alltweets = list()    


    while (True):
        #Leer datos de tweets
        try:    
            new_tweets = api.search(q="place:%s" % place_id,tweet_mode='extended',since_id=oldest)   
        except :
            break
        
        
        if len(new_tweets) != 0:

            #guarda el id del ultimo
            oldest=new_tweets[-1].id-1 
            
            #por cada iteracion agrega las frases nuevas del tweets
            for tweet in new_tweets:
                alltweets.extend(ppsing.processing(tweet.full_text))         
            #vacio lista
            new_tweets=[]

        #duerme durante 1 minuto
        if (len(alltweets)>=cant_tweets):
            break
        else: 
            sleep(60)        
   
    return alltweets,oldest


def save_oldest (oldest):

    outfile = open('oldest','wb')
    ppsing.pickle.dump(oldest,outfile)
    outfile.close()

#main
if __name__ == '__main__':


    #indica cantidad de tweets en qu se bajara
    cant_tweets=int(input('cantidad de frases:'))   
    largo = 0

    # abrir oldest anterior
    try:
        infile = open('oldest','rb')
        oldest= ppsing.pickle.load(infile)
        infile.close()
    except:
        oldest=1

    
    while True:
       
        tweets,oldest=get_all_tweets(cant_tweets-largo,oldest)
        len_tweets=len(tweets)

        if (len_tweets != 0):
            ppsing.save_data(tweets)
            save_oldest(oldest)
            ppsing.save_dict()
            largo += len_tweets
            print('guardado...')

        print(largo)

        # si se cumple que largo es mayor
        if (largo >= cant_tweets):
            break
        
        # si no, duerme
        else:
            print('dormir...')
            sleep(16*60); # duerme 16 minutos

    print('fin\n')


