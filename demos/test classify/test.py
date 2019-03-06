from gensim.models.doc2vec import Doc2Vec
from scipy.cluster.vq import vq,kmeans,whiten
from lexer import get_token_list
import os
import gensim.models.keyedvectors
import numpy as np

import os.path
def processDirectory(dirname):
    file_names = []
    counter = 0
    for dirpath, dirnames, filenames in os.walk(dirname):
        print('Directory', dirpath)
        for filename in filenames:
            if filename[len(filename)-3:len(filename)]==".py":
                print(' File', filename)
                file_names.append(dirpath+'\\'+filename)
                counter+=1
    print(counter)
    return file_names


def load_code(file_dir):
    contents = []
    files_names = []
    listdir('data\\svm',files_names)
    listdir('data\\fp', files_names)
    return files_names


def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)


import pickle
def test_classify():
    model_path ="model/wiki_en_doc2vec.model.bin"#"model/wiki_en_doc2vec.model.bin" # "model/model_doc2vec"#"
    model = Doc2Vec.load(model_path)
    file_names = load_code('data')
    vectors = []
    pkl_file = open('sens.pkl', 'rb')
    sens = pickle.load(pkl_file)
    for file in file_names:
        targets = get_token_list( file)
        targets,string = process_code(targets)
        vector = model.infer_vector(targets, steps=6, alpha=0.025)
        sims = model.docvecs.most_similar([vector], topn=10)
        #print(sens[sims[0][0]])
        #print(sims[0][0])
        vectors.append(vector)
    vectors = np.array(vectors)
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    pca.fit(vectors)
    import matplotlib.pyplot as plt
    new_vectors = pca.transform(vectors)
    centroid = kmeans(new_vectors, 2)[0]
    label = vq(new_vectors, centroid)[0]
    for i in range(0,len(new_vectors)):
        if i<=len(new_vectors)/2:
            plt.scatter(new_vectors[i][0],new_vectors[i][1],c='r')
        else:
            plt.scatter(new_vectors[i][0], new_vectors[i][1], c='b')
    print(label)
    plt.show()


import re
def process_code(targets):
    targets2= []
    for target in targets:
        x = re.split("[\. _]", target)
        targets2.extend(x)
    results = []
    for x in targets2:
        if x != '':
            last_index = 0
            cur_index = 1
            for char in x:
                if char>='A' and char<='Z':
                    results.append(x[last_index:cur_index-1])
                    last_index = cur_index-1
                cur_index+=1
            results.append(x[last_index:cur_index-1])
    final_string = ''
    for x in results:
        final_string = final_string + ' '+x
    return results,final_string


if __name__ == '__main__':
    test_classify()
    #processDirectory('codeSet')
    #process_code("testCal")