import numpy as np


def metric(T_ant,T_sin,labels):
    """ Calcula el costo asociado al modelo 

        cuenta la cantidad de antonimos en un mismo cluster
        y la cantidad de sinonimos fuera del cluster
    """

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


def show_cluster (vocab,labels,word ):
    """ entrega el cluster(palabras) donde se encuentra
        la palbra word.
    """   
    try:
        label=labels[vocab.index(word)]
    except:
        print('no existe esa frase en el vocabulario')
        return 1

    cluster=list()
    for i in range(len(labels)):
        if (label==labels[i]):
            cluster.append(vocab[i])
    return cluster


def links_clusters (affinity,labels,senti_labels=None):
    """
        Genera una estructura de datos que guarda los links positivos,
        links negativos y el volumen de los clusters de interes (sentimentales)
        
        entradas:
            affinity : np.array, matriz de afinidad del grafo.
            labels: list(), lista de etiquetas al aplicar el clustering al grafo.
            senti_labels: set(), conjunto de etiquetas de interes.

        Salida:
            links: dict(), diccionario donde la primera llave es el cluster de interes,
            y entrega diccionario donde las llave son:
                 
                 'vol'(volumen del cluster)
                 'neg'(links-)
                 'pos'(links+) 

        ejemplo: links[1]['vol']--> volumen del cluster 1.
        La complejidad es n
    """    


    if (senti_labels==None):
        senti_labels=set(labels)

    links=dict()
    for i in range(len(labels)):

        etiqueta=labels[i]
        if etiqueta in senti_labels:
            
            if etiqueta not in links.keys():
                links[etiqueta]=dict()
                X=np.absolute(affinity[:,i])
                links[etiqueta]['vol']=X.sum(axis=0)
                links[etiqueta]['neg']=0.5*(X-affinity[:,i])
                links[etiqueta]['pos']=0.5*(X+affinity[:,i])

            else:
                        
                X=np.absolute(affinity[:,i])
                links[etiqueta]['vol']=links[etiqueta]['vol']+X.sum(axis=0)
                links[etiqueta]['neg']=links[etiqueta]['neg']+0.5*(X-affinity[:,i])
                links[etiqueta]['pos']=links[etiqueta]['pos']+0.5*(X+affinity[:,i])
    
    return links












