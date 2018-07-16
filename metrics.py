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

        ejemplo: links[1]['vol']--> volumen del cluster 1
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






def sentence_to_graph (affinity,vocab,sentences,links):
    """
    Calcula un diccionario, que guarda los siguientes funcionales:
        S+(A,Ci)=(links+(A,Ci)+links-(A,Ci^c))/(vol(A)+vol(Ci))
        S-(A,Ci)=(links-(A,Ci)+links+(A,Ci^c))/(vol(A)+vol(Ci))
        Entradas:
            affinity: matriz de afinidad del grafo.
            vocab: vocabulario del modelo.
            sentences: lista de palabras.
            links: diccionario otorgado por links_clusters
        Salidas:
            functional: diccionario, con labels como llave y que guarda una lista con los funcionales.

        Ejemplo: functional[C_i]=[S+(A,C_i),S-(A,C_i)]
    """
    functional = dict()
    vol_A=0

    n=len(links.keys())
    X=np.array([[0,0]]*len(links.keys()))
    # obtiene indices de las palabras y volumen de la frase A
    for frase in sentences:
        try:
            i=vocab.index(frase)         
            vol_A=vol_A+np.absolute(affinity[:,i]).sum(axis=0)

            for label_1 in links:

                if (label_1 not in functional.keys()):
                    functional[label_1]=[0,0]
                
                for label_2 in links:
                    if (label_1==label_2):
                        functional[label_1][0]+=links[label_1]['pos'][i]
                        functional[label_1][1]+=links[label_1]['neg'][i]

                    else:
                        functional[label_1][0]+=links[label_2]['neg'][i]
                        functional[label_1][1]+=links[label_2]['pos'][i]
        except:
            print(i)

    for label in functional:
        functional[label][0]/=(vol_A+links[label]['vol'])
        functional[label][1]/=(vol_A+links[label]['vol'])  

    return functional








