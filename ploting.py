# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 22:20:25 2018

@author: ivan
"""

from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.cluster import SpectralClustering


modelo = Word2Vec.load("modelo")
ts = TSNE(2)
lista = list(modelo.wv.vocab.keys())

    
    
reduced_vecs = ts.fit_transform(modelo.wv[modelo.wv.vocab.keys()])
spectral = SpectralClustering(n_clusters = 7, eigen_solver='arpack', affinity="nearest_neighbors")
spectral.fit(modelo.wv[modelo.wv.vocab.keys()])
label = spectral.labels_


for i in range(len(reduced_vecs)):
    if(label[i]==0):
        c = 'k'
    elif(label[i]==1):
        c = 'c'
    elif(label[i]==2):
        c = 'm'
    elif(label[i]==3):
        c = 'b'
    elif(label[i]==4):
        c = 'r'
    elif(label[i]==5):
        c = 'g'
    elif(label[i]==6):
        c = 'y'
    plt.plot(reduced_vecs[i,0],reduced_vecs[i,1],marker = 'x',color = c, markersize = 8)
plt.show()

