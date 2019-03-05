import gensim
from test import processDirectory, get_token_list, process_code
import numpy as np
import pickle

TaggededDocument = gensim.models.doc2vec.TaggedDocument
def train_sentence():
    file_names = processDirectory('codeSet')
    sens = []
    counter = 0
    for file in file_names:
        targets = get_token_list(file)
        results, string = process_code(targets)
        if len(string)>=100:
            sens.append(string)
            counter+=1
            print(counter)
    output = open('sens.pkl', 'wb')
    pickle.dump(sens, output)
    output.close()
    dic = {}
    for i in range(0,len(sens)):
        dic[sens[i]]=i
    keys=dic.keys()
    x_train = []
    for key in keys:
        document = TaggededDocument(key, tags=[dic[key]])
        x_train.append(document)
    model_dm = gensim.models.Doc2Vec(x_train, min_count=1, window=3, vector_size=100, sample=1e-3, negative=5, workers=4)
    model_dm.train(x_train, total_examples=model_dm.corpus_count, epochs=70)
    model_dm.save('model/model_doc2vec')

if __name__ == '__main__':
    train_sentence()