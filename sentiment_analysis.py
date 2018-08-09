from ppsing import ptext
from metrics import simCluster
from metrics import map_sentiment
import numpy as np

def senti_tweet(affinity,vocab,links,class_clusters,tweet,mode='manual'):
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
	#elif(mode=='URL'):
		"""AGREGAR CODIGO: 
						bajar tweet desde tweepy por medio de 
						la URL y asignarselo a la variable tweet 
		"""
		#tweet_pp = ptext(tweet)
		  
	else: 
		print('Mode no existente')
		return

	sentences = []
	for i in tweet_pp:
		sentences += i

	funcional = simCluster(affinity,vocab,sentences,links)
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
	senti_max = sentimientos[np.argmax(peso_sentimientos)]

	print(f'El tweet se considera sentimentalmente {senti_max}.\n')
	
	print(f'Además posee la carga porcentual por sentimiento de{frase_final}.')

	return dic_class

