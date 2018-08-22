from ppsing import ptext
from metrics import simCluster
from metrics import map_sentiment
import numpy as np
import tweepy #https://github.com/tweepy/tweepy


#Twitter API credentials
consumer_key = "YG9t6aMkiK3rvGdSbIkNbVKoG"
consumer_secret = "xhyivSyaesMQ2PvJdceI7BwBX3sjXxzhHsvC2pZcV0i2VTZ16R"
access_key = "879488168525004801-2wqBqwGmQzUNbvZLC1Oja7dyOF0ztLK"
access_secret = "ajMqqwF7TBf2tQZpLQyNZfe9jSLh8K6USWJHjXkp1Ohwg"

def senti_tweet(vocab,links,class_clusters,tweet,mode='manual'):
	"""Función que clasifica sentimentalmente un tweet.
		Se puede escribir el tweet a analizar de forma manual o
		se puede ingresar la URL respectiva del tweet.
		affinity = Matriz W
		vocab = vocabulario
		links = creado desde metrics.links_clusters
		class_clusters = creado desde metrics.classification_clusters
		tweet = puede ser una frase un una url
		mode = puede tomar los valores 'manual' o 'URL'	
	"""	
	if(mode=='manual'):
		tweet_pp = ptext(tweet)
	elif(mode=='URL'):
		new_tweets = api.user_timeline(screen_name = tweet,count=1,tweet_mode='extended')

		"""AGREGAR CODIGO: 
						bajar tweet desde tweepy por medio de 
						la URL y asignarselo a la variable tweet 
		"""
		tweet=new_tweets[0].full_text
		print('El tweet:\n',tweet,'\n')
		tweet_pp = ptext(tweet)
		  
	else: 
		print('Mode no existente')
		return

	sentences = []
	for i in tweet_pp:
		sentences += i

	funcional = simCluster(vocab,sentences,links)
	dic_class = map_sentiment(funcional,class_clusters)

	n = len(dic_class)
	sentimientos = [0]*n
	peso_sentimientos = [0]*n
	den = sum(dic_class.values())
	cont = 0
	frase_final =''
	for i in dic_class:
		sentimientos[cont] = i
		peso_sentimientos[cont] = (dic_class[i]/den)*100
		frase_final += ', '+sentimientos[cont]+': '+str(peso_sentimientos[cont])+'%'
		cont += 1

	lista=list()
	for n,m in dic_class.items():
		lista.append((m,n))
	lista.sort()
	 
	senti_max = lista[-1][1]
	
	print(f'El tweet se considera sentimentalmente {senti_max}.\n')
	 
	print(f'Además posee la carga porcentual por sentimiento de{frase_final}.')

	return dic_class

def senti_tweet_test(vocab,links,class_clusters,tweet):
	"""Función que clasifica sentimentalmente un tweet.
		Se puede escribir el tweet a analizar de forma manual o
		se puede ingresar la URL respectiva del tweet.
		affinity = Matriz W
		vocab = vocabulario
		links = creado desde metrics.links_clusters
		class_clusters = creado desde metrics.classification_clusters
		tweet = puede ser una frase un una url
		mode = puede tomar los valores 'manual' o 'URL'	
	"""	
	
	tweet_pp = ptext(tweet)

	sentences = []
	for i in tweet_pp:
		sentences += i

	funcional = simCluster(vocab,sentences,links)
	dic_class = map_sentiment(funcional,class_clusters)

	lista=list()
	for n,m in dic_class.items():
		lista.append((m,n))
	lista.sort()
	

	return lista[-1][1]


def test(fr_sent,vocab,links,class_clusters):
	result=dict()
	clas_result=dict()
	for sent in fr_sent:
		if sent not in result.keys():
			result[sent]=[]
			clas_result[sent]=dict()
		for tweet in fr_sent[sent]:
			label=senti_tweet_test(vocab,links,class_clusters,tweet)
			result[sent].append((tweet,sent,label))
			if label not in clas_result[sent].keys():
				clas_result[sent][label]=0
			clas_result[sent][label]+=1

	return clas_result,result

