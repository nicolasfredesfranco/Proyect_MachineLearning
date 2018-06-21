
from nltk import word_tokenize
import unicodedata 
import pickle
from nltk.corpus import wordnet as wn 
from pattern.es import lemma, singularize, parse 
from constantes import stopWords, abc

#se carga el diccionario si no existe crea uno nuevo

name_dict='frec_words'
frec_words=dict()
try:
    infile = open(name_dict,'rb')
    frec_words = pickle.load(infile)
    infile.close() 
except FileNotFoundError:
    frec_words=dict()


#funcion que elmina todos los signos que no son palabras, puntos o espacios
def elimina_sign(text):
    text_out=''
    for i in text:
        if i not in abc:
             text_out+=' '
        else :
            text_out +=i
    return text_out



def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


# lemmatiza verbos y singulariza sustantivos y adjetivos
def pword(text):
    ind=parse(text).split('/')[1][0] 
    
    # verbo
    if ind=='V':
        word=lemma(text)

    # sustantivo o adjetivo    
    else:
        word=singularize(text)
    return word

# Encontrar Sinonimos y Antonimos
# entrega un conjunto de sinonimos y antonimos
def sin_ant(text):
    lema=wn.lemmas(text,lang='spa')
    antonimos=list()
    sinonimos=list()
    for i in lema:
        sinonimos.extend(i.synset().lemma_names(lang='spa'))
        for j in i.synset().lemmas():
            for k in j.antonyms():
                antonimos.extend(k.synset().lemma_names(lang='spa'))


    sinonimos=set(sinonimos)
    antonimos=set(antonimos)
    return sinonimos,antonimos

## text es un string que deseas preprocesar, modificas el diccionario.
def processing(text):
    output=list()        
    
    #quita el enlace
    text=text.split('https')[0]

    #pasa todo a minusculas
    text = text.lower()

    #elmina signos de puntuacion
    #text=elimina_tildes(text)

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
                if (len(i)>1):
                    if (i not in stopWords):
                        word=pword(i)
                        words.append(word)
                    
                        if word not in frec_words.keys():
                            frec_words[word]=1;
                        else:
                            frec_words[word]=frec_words[word]+1
            if len(words)!=0:            
                output.append(words)

    return output


# mismo codigo que processing salvo que quita las palabras 
# que no estan en el diccionario
# esta version se corre cuando el modelo ya esta creado.

def ptext(text):
    output=list()        
    
    #quita el enlace
    text=text.split('https')[0]

    #pasa todo a minusculas
    text = text.lower()

    #elmina signos de puntuacion
    #text=elimina_tildes(text)

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
                
                word=pword(i)
                if word in frec_words.keys():
                    words.append(word)

            if len(words)!=0:            
                output.append(words)

    return output




# funcion que guarda el diccionario, por default min_count=1, 
# si este valor distinto de 1, elimina todas las palbras de frec menor 
# a min_count del diccionario. (por implementar)
# si deseas puedes cambiar el nombre del diccionario donde se guardara

def save_dict(min_count=1,name=name_dict): 
    outfile = open(name_dict,'wb')
    pickle.dump(frec_words,outfile)
    outfile.close()




def save_data (frases):

    
    #Leer datos de tweets
    try:    
        infile = open('dataTweets','rb')
        data = pickle.load(infile)
        infile.close()   
    except FileNotFoundError:
        data=list()

    data.extend(frases)
    outfile = open('dataTweets','wb')
    pickle.dump(data,outfile)
    outfile.close()


