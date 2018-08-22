# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 23:59:23 2018

@author: Nicolas
"""

import ppsing
from gensim.models import Word2Vec 
import numpy as np
from scipy.spatial.distance import euclidean


def T_syn_ant(vocab):
    n = len(vocab)
    T_syn = [[0]*n]*n
    T_ant = [[0]*n]*n  
    count = 0
    for i in vocab:
        syn,ant = ppsing.sin_ant(i)
        for j in syn:
            try: T_syn[count][vocab.index(j)]=1
            except: continue 
        for j in ant:
            try: T_ant[count][vocab.index(j)]=-1
            except: continue 
        count +=1
    return np.array(T_syn,dtype='float'),np.array(T_ant,dtype='float')
    
def W_init(modelo,vocab,eps,sig,diag=0):
    n = len(vocab)
    W = [[0]*n]*n
    for i in range(n):
        for j in range(i+1,n):
            dis = euclidean(modelo[vocab[i]],modelo[vocab[j]])
            dis_exp = np.exp(np.divide(np.power(dis,2.0),-sig)) 
            if(dis_exp > eps):
                W[i][j]= dis_exp
                W[j][i]= dis_exp
    for i in range(n):
        W[i][i]= diag
    return np.array(W,dtype='float')
                
def W(modelo,gama,b_ant,b_syn,eps,sig):
    vocab =list(modelo.wv.vocab.keys())
    T_syn,T_ant = T_syn_ant(vocab)
    W = W_init(modelo,vocab,eps,sig,0)
    W_final = gama*W + b_ant*T_ant*W + b_syn*T_syn*W
    return W_final
                
        
    
                            