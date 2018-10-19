import matplotlib.pyplot as plt
import numpy as np
import itertools

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def plot(data,title):
    plt.figure()
    plot_confusion_matrix(data, classes=['positivo','neutro','negativo'],normalize=True,
                      title=title)
    plt.show()

import wordgraph as wg 
import sentiment_analysis as sa 

def resultado():
    out = wg.load_matrix('out')
    links = wg.load_matrix('links_real2')
    vocab = wg.load_matrix('vocab_real')
    class_clusters = wg.load_matrix('class_clusters_real2')
    result,otro=sa.test(out,vocab,links,class_clusters)
    print (result)
    return result

