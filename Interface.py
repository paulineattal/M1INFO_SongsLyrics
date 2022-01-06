#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
#lecture avec pickle pour avoir tous les objets serialises 
with open("corpus_chanson.pkl", "rb") as f:
    while True:
        try:
            df_corpus = pd.concat([df_corpus, pickle.load(f)], axis = 0).reset_index(drop=True)
        except EOFError:
            break
list_chanson = df_corpus['Paroles graphes'].tolist()
#lecture du fichier des mots stop
with open("Stop-mots.txt", "r", encoding='utf8') as f:
    sm_french = [line.rstrip("\n") for line in f.readlines()]
    
    
########## TFIDF ##########

# instanciation de l'ojet TfidfVectorizer 
vectorizer = TfidfVectorizer()
# fit les donnees et les transformer en vecteur
X = vectorizer.fit_transform(list_chanson)
# convertir X en matrice transpose
X = X.T.toarray()
# creer un DataFrame et fixer le vocabulaire comme index
df = pd.DataFrame(X, index=vectorizer.get_feature_names())


chanson = Corpus(df_corpus)
indice_list_chanson = chanson.get_similar_song(word, df, list_chanson, vectorizer)
#sous dataframe qui contient seulement les chansons selectionnees par l'algorithme
df_chanson_sel = df_corpus.iloc[indice_list_chanson].reset_index(drop=True)
list_chanson_index = len(df_chanson_sel)


#pour chaque chanson trouvees 
for i in range(list_chanson_index) :
    #creer le nuage de mot    
    word_cloud = Graph(df_chanson_sel['Paroles graphes'][i], df_chanson_sel['Titre'][i], df_chanson_sel['Auteur'][i] )
    word_cloud.word_cloud(20,sm_french)
    
    
    ########## LDA ##########
    
    # instanciation de l'ojet CountVectorizer 
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=1000, stop_words=sm_french)
    tf=tf_vectorizer.fit_transform(df_chanson_sel['Paroles graphes'][i].split(" "))
    tf_feature_names = tf_vectorizer.get_feature_names()
    # instanciation de l'ojet LatentDirichletAllocation 
    lda = LatentDirichletAllocation(n_components=4, max_iter=5, learning_method='online', learning_offset=50., random_state=0)
    lda.fit(tf)
    
    
    #creer le graphe de mots 
    word_graph = Clique(df_chanson_sel['Paroles graphes'][i], df_chanson_sel['Titre'][i], df_chanson_sel['Auteur'][i], tf_feature_names)
    word_graph.display_clique()
    
    












