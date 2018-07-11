import numpy as np






def metric(T_ant,T_sin,labels):
    n=len(T_ant)
    cost=0
    for i in range(n):
        for j in range(i+1,n):
            if(T_ant[i,j]<0.0):
                if (labels[i]==labels[j]):
                    cost+=1
            if (T_sin[i,j]>0.0):
                if (labels[i]!=labels[j]):
                    cost+=1

    return cost


