# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 23:59:23 2018

@author: Nicolás I. Fredes Franco
"""

import ppsing
from gensim.models import Word2Vec 
import numpy as np
from scipy.spatial.distance import euclidean


def T_syn_ant(vocab,n):
    T_syn = np.array([[0.0]*n]*n)
    T_ant = np.array([[0.0]*n]*n)
    for i in range(n):
        syn,ant = ppsing.sin_ant(vocab[i])
        for j in syn:
            try: T_syn[i][vocab.index(j)]= 1.0
            except: continue 
        for j in ant:
            try: T_ant[i][vocab.index(j)]= -1.0
            except: continue  
    return T_syn,T_ant
    
def W_init(modelo,vocab,n,eps,sig):
    W=np.array([[0.0]*n]*n)
    for i in range(n):
        for j in range(i+1,n):    
            dis = euclidean(modelo[vocab[i]],modelo[vocab[j]])
            dis_exp = np.exp(np.divide(np.power(dis,2.0),-sig))
            if(dis_exp > eps):
                W[i][j]= dis_exp
                W[j][i]= dis_exp             
    return W
                
def W(modelo,vocab,gama,b_ant,b_syn,eps,sig):
    n = len(vocab)
    W = W_init(modelo,vocab,n,eps,sig)
    T_syn,T_ant = T_syn_ant(vocab,n)
    W_final = gama*W + b_ant*T_ant*W + b_syn*T_syn*W
    return W_final,W,T_syn,T_ant
                
#def matrix(W,n): 
#    W=W[0:3]
##    for i in range(len(W)):
#        W[i]=W[i][0:3]
#    return W                        