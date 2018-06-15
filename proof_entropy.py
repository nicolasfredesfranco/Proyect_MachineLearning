# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 14:51:58 2018

@author: Nicolas Fredes
"""

from gensim.models import Word2Vec
from nltk import word_tokenize
import unicodedata 
import pickle
import math
#import array 
import numpy as np
from numpy import linalg as LA
abc={'q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m',' ','.'}#,'1','2','3','4','5','6','7','8','9'}

stop_words=['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'mas', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'si', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'tambien', 'me', 'hasta', 'hay', 'donde', 'quien', 'desde', 'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mi', 'antes', 'algunos', 'que', 'unos', 'yo', 'otro', 'otras', 'otra', 'el', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tu', 'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras', 'vosostros', 'vosostras', 'os', 'mio', 'mia', 'mios', 'mias', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras', 'esos', 'esas', 'estoy', 'estas', 'esta', 'estamos', 'estais', 'estan', 'este', 'estes', 'estemos', 'esteis', 'esten', 'estare', 'estaras', 'estara', 'estaremos', 'estareis', 'estaran', 'estaria', 'estarias', 'estariamos', 'estariais', 'estarian', 'estaba', 'estabas', 'estabamos', 'estabais', 'estaban', 'estuve', 'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'estuviera', 'estuvieras', 'estuvieramos', 'estuvierais', 'estuvieran', 'estuviese', 'estuvieses', 'estuviesemos', 'estuvieseis', 'estuviesen', 'estando', 'estado', 'estada', 'estados', 'estadas', 'estad', 'he', 'has', 'ha', 'hemos', 'habeis', 'han', 'haya', 'hayas', 'hayamos', 'hayais', 'hayan', 'habre', 'habras', 'habra', 'habremos', 'habreis', 'habran', 'habria', 'habrias', 'habriamos', 'habriais', 'habrian', 'habia', 'habias', 'habiamos', 'habiais', 'habian', 'hube', 'hubiste', 'hubo', 'hubimos', 'hubisteis', 'hubieron', 'hubiera', 'hubieras', 'hubieramos', 'hubierais', 'hubieran', 'hubiese', 'hubieses', 'hubiesemos', 'hubieseis', 'hubiesen', 'habiendo', 'habido', 'habida', 'habidos', 'habidas', 'soy', 'eres', 'es', 'somos', 'sois', 'son', 'sea', 'seas', 'seamos', 'seais', 'sean', 'sere', 'seras', 'sera', 'seremos', 'sereis', 'seran', 'seria', 'serias', 'seriamos', 'seriais', 'serian', 'era', 'eras', 'eramos', 'erais', 'eran', 'fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron', 'fuera', 'fueras', 'fueramos', 'fuerais', 'fueran', 'fuese', 'fueses', 'fuesemos', 'fueseis', 'fuesen', 'sintiendo', 'sentido', 'sentida', 'sentidos', 'sentidas', 'siente', 'sentid', 'tengo', 'tienes', 'tiene', 'tenemos', 'teneis', 'tienen', 'tenga', 'tengas', 'tengamos', 'tengais', 'tengan', 'tendre', 'tendras', 'tendra', 'tendremos', 'tendreis', 'tendran', 'tendria', 'tendrias', 'tendriamos', 'tendriais', 'tendrian', 'tenia', 'tenias', 'teniamos', 'teniais', 'tenian', 'tuve', 'tuviste', 'tuvo', 'tuvimos', 'tuvisteis', 'tuvieron', 'tuviera', 'tuvieras', 'tuvieramos', 'tuvierais', 'tuvieran', 'tuviese', 'tuvieses', 'tuviesemos', 'tuvieseis', 'tuviesen', 'teniendo', 'tenido', 'tenida', 'tenidos', 'tenidas', 'tened','asi','q','d']

#Se cargar el diccionario anterior, debe estar archivo "FrecWords" o sino habra error

infile = open('FrecWords','rb')
frec_words = pickle.load(infile)
infile.close()


#esta funcion elmina todos los signos que no son palabras
def elimina_sign(text):
    for i in range(len(text)-1):
        if text[i] not in abc:
             text=text[:i] + ' ' +text[i + 1:]
    if text[len(text)-1] not in abc:
        text=text[:len(text)-1]
    return text

def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


def processing(text):
    output=list()        
    
    #quita el enlace
    #text=text.split('https')[0]

    #pasa todo a minusculas
    text = text.lower()

    #elmina signos de puntuacion
    text=elimina_tildes(text)

    #elimina caracteres
    text=elimina_sign(text)

    #separa el texto por frases u oraciones
    frases=text.split('.');

    #separa por las palabras
    for fr in frases:
        if len(fr)!=0: 
            words_sw = word_tokenize(fr)
            words=[]
            for i in words_sw:
                if i not in stop_words:
                    words.append(i)
                    
                    if i not in frec_words.keys():
                        frec_words[i]=1;
                    else:
                        frec_words[i]=frec_words[i]+1


            if len(words)!=0:            
                output.append(words)
                
    return output

def save_dict():
    filename = 'FrecWords'
    outfile = open(filename,'wb')
    pickle.dump(frec_words,outfile)
    outfile.close()

#el modelo ocupado debe estar seteado con min count 1 o sino no agregara palabras nuevas por aparecer una vez

#entropia solo
def mapear(text_2):
    model=Word2Vec.load('prueba_entropia4')
    model.build_vocab(text_2, update=True, keep_raw_vocab=True)
    model.train(text_2, total_examples=model.corpus_count, epochs=model.iter)
    n_palabras=sum(frec_words.values())
    vec=np.array([0.0]*200)
    et=0.0
    for i in text_2:
       for j in i:
           
           e=math.log(n_palabras/frec_words[j],2)
           vec += np.multiply(model[j],e)
           et += e
    x=np.divide(vec,et)
    return x

#entropia normalizado
def mapear_1(text_2):
    model=Word2Vec.load('prueba_entropia4')
    model.build_vocab(text_2, update=True, keep_raw_vocab=True)
    model.train(text_2, total_examples=model.corpus_count, epochs=model.iter)
    n_palabras=sum(frec_words.values())
    vec=np.array([0.0]*200)
    et=0.0
    for i in text_2:
       for j in i:
           
           e=math.log(n_palabras/frec_words[j],2)
           v = np.divide(model[j],LA.norm(model[j]))
           vec += np.multiply(v,e)
           et += e
    x=np.divide(vec,et)
    return x

#promedio simple
def mapear_2(text_2):
    model=Word2Vec.load('prueba_entropia4')
    model.build_vocab(text_2, update=True, keep_raw_vocab=True)
    model.train(text_2, total_examples=model.corpus_count, epochs=model.iter)
    vec=np.array([0.0]*200)
    count=0.0
    for i in text_2:
       for j in i:
           count += 1
           vec += model[j]
    x=np.divide(vec,count)
    return x

#promedio simple normalizado
def mapear_3(text_2):
    model=Word2Vec.load('prueba_entropia4')
    model.build_vocab(text_2, update=True, keep_raw_vocab=True)
    model.train(text_2, total_examples=model.corpus_count, epochs=model.iter)
    vec=np.array([0.0]*200)
    count=0.0
    for i in text_2:
       for j in i:
           count += 1
           v = np.divide(model[j],LA.norm(model[j]))
           vec += v
    x=np.divide(vec,count)
    return x

def mapping(text,n):
    text_2 = processing(text)
    save_dict()
    if n == 0:
        v = mapear(text_2)
    if n == 1:
        v = mapear_1(text_2)  
    if n == 2:
        v = mapear_2(text_2)
    if n == 3:
        v = mapear_3(text_2)    
    else:
        v = mapear(text_2)
    return v

# Mapeos: 0= entropia, 1= entropia normalizado, 2= promedio simple, 3= promedio simple normalizado 
    
if __name__ == '__main__':


    text=input('Ingresa un frase por favor: ')
    n=input('Tipo de mapeo: ')
    text_2 = processing(text)
    save_dict()
    #print(text_2)
    if n == 0:
        v = mapear(text_2)
    if n == 1:
        v = mapear_1(text_2)  
    if n == 2:
        v = mapear_2(text_2)
    if n == 3:
        v = mapear_3(text_2)    
    else:
        v = mapear(text_2)
    print(v)
    #return v




