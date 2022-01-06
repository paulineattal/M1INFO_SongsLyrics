# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 02:00:09 2022

@author: f_ati
"""

import tkinter as tk
import matplotlib.pyplot as plt
import os
import glob
import natsort
from PIL import Image
from PIL import ImageTk
from mots import Graph, Clique
from corpus import Corpus
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

window = tk.Tk()

window.title('Recherche de chanson')
window.tk.call('wm', 'iconphoto', window._w, ImageTk.PhotoImage(file='icon.ico'))

window.config(padx=10, pady=10)

title_label = tk.Label(window, text = 'Entrez un mot a rechercher dans une chanson')
title_label.config(font=('Arial', 32))
title_label.pack(padx=10, pady=10)

target_image = tk.Label(window)
target_image.pack(padx=10, pady=10)

target_information = tk.Label(window)
target_information.config(font=("Arial", 20))
target_information.pack(padx=10, pady=10)


photos_names_list = ["mask"]
#FUNCTION
def showimage():

    dir1 = r"python_chanson"
    path1 = os.path.join(dir1, '*g')
    files = glob.glob(path1)
    files1 = natsort.natsorted(files, reverse=False)
    for x in files1:
        img = plt.imread(x)
        image = Image.open(img)
        imag = ImageTk.PhotoImage(image)


    target_image.config(image=imag)
    target_image.image = imag




entree = tk.Entry(window)#demande la valeur
entree.pack() # integration du widget a la fenetre principale
entree.config(font=("Arial", 20))
entree.pack(padx=10, pady=10)


def close_window():
    global word
    word = entree.get()
    window.destroy()
    
B = tk.Button(window, text = "Rechercher", command = close_window)
B.config(font=("Arial", 20))
B.pack(padx=10, pady=10)
B.pack()


window.mainloop()



df_corpus = pd.DataFrame()
#lecture avec pickle
#boucle pour avoir tous les objets serialises 
with open("corpus_chanson.pkl", "rb") as f:
    while True:
        try:
            df_corpus = pd.concat([df_corpus, pickle.load(f)], axis = 0).reset_index(drop=True)
        except EOFError:
            break
#corpus = pd.read_csv("corpus.csv")
list_chanson = df_corpus['Paroles graphes'].tolist()

with open("Stop-mots.txt", "r", encoding='utf8') as f:
    sm_french = [line.rstrip("\n") for line in f.readlines()]
    
    
    

# Instantiate a TfidfVectorizer object
vectorizer = TfidfVectorizer()
# It fits the data and transform it as a vector
X = vectorizer.fit_transform(list_chanson)
# Convert the X as transposed matrix
X = X.T.toarray()
# Create a DataFrame and set the vocabulary as the index
df = pd.DataFrame(X, index=vectorizer.get_feature_names())


chanson = Corpus(df_corpus)
list_chanson = chanson.get_similar_song(word, df, list_chanson, vectorizer)

for song in list_chanson :
    word_cloud = Graph(song, "test")
    word_cloud.word_cloud(20,sm_french)


    ########class clique
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=1000, stop_words=sm_french)
    tf=tf_vectorizer.fit_transform(song)
    tf_feature_names = tf_vectorizer.get_feature_names()
    # Créer le modèle LDA
    lda = LatentDirichletAllocation(n_components=4, max_iter=5, learning_method='online', learning_offset=50., random_state=0)
    lda.fit(tf)
    
    
    word_graph = Clique(song, "titre", 10)
    word_graph.display_topics(lda, tf_feature_names)












