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
import shutil

window = tk.Tk()

window.title('Recherche de chanson')
#window.tk.call('wm', 'iconphoto', window._w, ImageTk.PhotoImage(file='icon.ico'))
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

#recuperer les chansons selectionnees par TFIDF
chanson = Corpus(df_corpus)
indice_list_chanson = chanson.get_similar_song(word, df, list_chanson, vectorizer)
#sous dataframe qui contient seulement les chansons selectionnees par l'algorithme
df_chanson_sel = df_corpus.iloc[indice_list_chanson].reset_index(drop=True)
#taille du sous dataframe
size_list_chanson_index = len(df_chanson_sel)


os.makedirs("img_tkinter")


#pour chaque chanson trouvees 
for i in range(size_list_chanson_index) :
    #creer le nuage de mot    
    word_cloud = Graph(df_chanson_sel['Paroles graphes'][i], df_chanson_sel['Titre'][i], df_chanson_sel['Auteur'][i] )
    wc = word_cloud.word_cloud(20,sm_french)
    #enregistrement des words cloud
    wc.savefig('img_tkinter/cloud'+str(i)+'.png')
    
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
    wg = word_graph.display_clique()
    #enregistrement des graphes de mots
    wg.savefig('img_tkinter/graph'+str(i)+'.png')
    
    
## La fenetre, avec les options de grille qui vont bien
result = tk.Tk()
result.grid_rowconfigure(3, weight=1)
result.grid_columnconfigure(3, weight=1)
## Le canvas
cnv = tk.Canvas(result,width=1200, height=900)
cnv.grid(row=0, column=0, sticky='nswe')
## Les scrollbars
hScroll = tk.Scrollbar(result, orient=tk.HORIZONTAL, command=cnv.xview)
hScroll.grid(row=1, column=0, sticky='we')
vScroll = tk.Scrollbar(result, orient=tk.VERTICAL, command=cnv.yview)
vScroll.grid(row=0, column=1, sticky='ns')
cnv.configure(xscrollcommand=hScroll.set, yscrollcommand=vScroll.set)
## Le Frame, dans le Canvas, mais sans pack ou grid
frm = tk.Frame(cnv)

gifsdict={} 
for j in range(size_list_chanson_index):
    tk.Label(frm, text=df_chanson_sel['Paroles originales'][j]).grid(row=j, column =0)
    cloud = tk.PhotoImage(file='img_tkinter/cloud'+str(j)+'.png')
    gifsdict['img_tkinter/cloud'+str(j)+'.png'] = cloud 
    tk.Label(frm, image = cloud).grid(row =j, column =1)
    graph = tk.PhotoImage(file='img_tkinter/graph'+str(j)+'.png')
    gifsdict['img_tkinter/graph'+str(j)+'.png'] = graph 
    tk.Label(frm, image = graph).grid(row =j, column =2)
    
## Pour etre sur que les dimensions sont calculées
frm.update()
## Création de la window dans le Canvas
cnv.create_window(0, 0, window=frm, anchor=tk.NW)
## La scrollregion est la boite englobante pour tout ce qu'il y a dans le Canvas
cnv.configure(scrollregion=cnv.bbox(tk.ALL))
## C'est parti!
result.mainloop()





shutil.rmtree("img_tkinter", ignore_errors=True)