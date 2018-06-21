import ppsing
import wikipedia as wk




#main
if __name__ == '__main__':
    
    numero=int(input('cantidad de paginas:'))

    
    #cargar lista de ya bajados
    try:
        infile = open('wiki','rb')
        lwiki= ppsing.pickle.load(infile)
        infile.close()
    except:
        lwiki=list()

    wk.set_lang('es') # setear wk en español
    cant=0
    frases=list()
    print('bajando...')
    while cant<numero:
        tema=wk.random(1)

        if tema not in lwiki:
            lwiki.append(tema)
            new_page=wk.WikipediaPage(tema)
            frases.extend(ppsing.processing(new_page.content))
            cant+=1
    # guardar            
    ppsing.save_data(frases)
    ppsing.save_dict()
    
    outfile = open('wiki','wb')
    ppsing.pickle.dump(lwiki,outfile)
    outfile.close()
    
    print(len(frases))
    print('fin')
            
        
