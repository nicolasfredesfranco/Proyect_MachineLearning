from pickle import load



if __name__ == '__main__':

    infile = open('dataTweets','rb')
    data=load(infile)
    infile.close()

    print(len(data))

    mst=input('mostrar?(s/n):')

    if mst=='s':
        print(data)

    print('fin')
