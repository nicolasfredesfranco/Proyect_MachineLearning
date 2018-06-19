# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 22:20:25 2018

@author: ivan
"""

from gensim.models import Word2Vec
import matplotlib.pyplot as plt
from sklearn.cluster import SpectralClustering


modelo = Word2Vec.load("modelo2d")
lista = list(modelo.wv.vocab.keys())


spectral = SpectralClustering(n_clusters = 3, eigen_solver='arpack', affinity="nearest_neighbors")
spectral.fit(modelo.wv[modelo.wv.vocab.keys()])
label = spectral.labels_


for i in range(len(label)):
    if(label[i]==0):
        c = 'k'
    elif(label[i]==1):
        c = 'c'
    elif(label[i]==2):
        c = 'm'
    elif(label[i]==3):
        c = 'b'
    elif(label[i]==4):
        c = 'y'
    else:
        continue
    plt.plot(modelo.wv[lista[i]][0],modelo.wv[lista[i]][1],marker = 'x',color = c, markersize = 5)
plt.plot(modelo.wv['amor'][0],modelo.wv['amor'][1], marker = 'o', color = 'g', markersize = 8)
plt.plot(modelo.wv['feliz'][0],modelo.wv['feliz'][1], marker = 'o', color = 'g', markersize = 8)
plt.plot(modelo.wv['enamorado'][0],modelo.wv['enamorado'][1], marker = 'o', color = 'g', markersize = 8)
plt.plot(modelo.wv['pena'][0],modelo.wv['pena'][1], marker = 'o', color = 'r', markersize = 8)
plt.plot(modelo.wv['ira'][0],modelo.wv['ira'][1], marker = 'o', color = 'r', markersize = 8)
plt.plot(modelo.wv['rabia'][0],modelo.wv['rabia'][1], marker = 'o', color = 'r', markersize = 8)
plt.plot(modelo.wv['tiempo'][0],modelo.wv['tiempo'][1], marker = 'o', color = 'b', markersize = 8)
plt.show()
print(modelo.wv[lista[0]][0])
print(modelo.wv[modelo.wv.vocab.keys()])
