#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#pour l'interface
import tkinter as tk
from PIL import ImageTk
#propres classes crees
from Classes import Graph, Clique
from Corpus import Corpus
#pour deserialiser les donnees
import pickle
#pour manipuler les donnees
import pandas as pd
#pour le traitement des textes
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
#pour creer et effacer un dossier
import shutil
import os

#creation de la fenetre de la barre de recherche
window = tk.Tk()
window.title('Trouve ta chanson')
window.tk.call('wm', 'iconphoto', window._w, ImageTk.PhotoImage(file='img/icon.ico'))
window.config(padx=10, pady=10)

title_label = tk.Label(window, text = 'Entrez un mot a rechercher dans une chanson')
title_label.config(font=('Arial', 32))
title_label.pack(padx=10, pady=10)

target_information = tk.Label(window)
target_information.config(font=("Arial", 20))
target_information.pack(padx=10, pady=10)

entree = tk.Entry(window) #demande la valeur
entree.pack() #integration du widget a la fenetre principale
entree.config(font=("Arial", 20))
entree.pack(padx=10, pady=10)

#fonction qui permet de sauvegarder la valeur saisie et de fermet la fenetre
def close_window():
    global word
    word = entree.get()
    window.destroy()

#configuration du boutton 
B = tk.Button(window, text = "Rechercher", command = close_window)
B.config(font=("Arial", 20))
B.pack(padx=10, pady=10)
B.pack()

#lancer la fenetre
window.mainloop()

#recuperation des donnees scrapees au prealable avec Selenium et serialise avec pickle
df_corpus = pd.DataFrame()
#lecture avec pickle pour avoir tous les objets serialises 
with open("datas/corpus_chanson.pkl", "rb") as f:
    while True:
        try:
            df_corpus = pd.concat([df_corpus, pickle.load(f)], axis = 0).reset_index(drop=True)
        except EOFError:
            break
list_chanson = df_corpus['Paroles graphes'].tolist()
#lecture du fichier des mots stop
with open("datas/Stop-mots.txt", "r", encoding='utf8') as f:
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

#si des chansons ont etes trouves avec le mot saisie
if size_list_chanson_index > 0 :
    os.makedirs("img_tkinter")    
    #pour chaque chanson trouvees 
    for i in range(size_list_chanson_index) :
        #creer le nuage de mot    
        word_cloud = Graph(df_chanson_sel['Paroles graphes'][i], df_chanson_sel['Titre'][i], df_chanson_sel['Auteur'][i] )
        wc = word_cloud.word_cloud(20,sm_french)
        #enregistrement des words cloud dans un dossier pour pouvoir les ouvrir avec tkinter
        wc.savefig('img_tkinter/cloud'+str(i)+'.png')
        
        ########## LDA ##########
        #permet de faire une selection des mots important dans un texte
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
        #enregistrement des graphes de mots dans un dossier pour pouvoir les ouvrir avec tkinter
        wg.savefig('img_tkinter/graph'+str(i)+'.png')
        
        
    #la fenetre, avec les options de grille qui vont bien
    result = tk.Tk()
    result.title('Resultat des chansons contenant le mot '+ word)
    result.grid_rowconfigure(3, weight=1)
    result.grid_columnconfigure(3, weight=1)
    #le canvas
    cnv = tk.Canvas(result,width=1200, height=900)
    cnv.grid(row=0, column=0, sticky='nswe')
    #les scrollbars
    hScroll = tk.Scrollbar(result, orient=tk.HORIZONTAL, command=cnv.xview)
    hScroll.grid(row=1, column=0, sticky='we')
    vScroll = tk.Scrollbar(result, orient=tk.VERTICAL, command=cnv.yview)
    vScroll.grid(row=0, column=1, sticky='ns')
    cnv.configure(xscrollcommand=hScroll.set, yscrollcommand=vScroll.set)
    #frame dans le canvas
    frm = tk.Frame(cnv)
    
    gifsdict={} 
    #on va recuperer les images des graphes et les paroles a afficher dans la frame
    for j in range(size_list_chanson_index):
        tk.Label(frm, text=df_chanson_sel['Paroles originales'][j]).grid(row=j, column =0)
        cloud = tk.PhotoImage(file='img_tkinter/cloud'+str(j)+'.png')
        gifsdict['img_tkinter/cloud'+str(j)+'.png'] = cloud 
        tk.Label(frm, image = cloud).grid(row =j, column =1)
        graph = tk.PhotoImage(file='img_tkinter/graph'+str(j)+'.png')
        gifsdict['img_tkinter/graph'+str(j)+'.png'] = graph 
        tk.Label(frm, image = graph).grid(row =j, column =2)
        
    frm.update()
    #creation de la window dans le Canvas
    cnv.create_window(0, 0, window=frm, anchor=tk.NW)
    #la scrollregion est la boite englobante pour tout ce qu'il y a dans le Canvas
    cnv.configure(scrollregion=cnv.bbox(tk.ALL))
    #lancer la fenetre de resultats
    result.mainloop()

    #ecraser le dossier qui contient les graphies en png
    shutil.rmtree("img_tkinter", ignore_errors=True)
    
#si aucune chanson n'a ete trouvees avec le mot siasi
else :
    window = tk.Tk()
    window.title('Recherche de chanson')
    #window.tk.call('wm', 'iconphoto', window._w, ImageTk.PhotoImage(file='icon.ico'))
    window.config(padx=10, pady=10)
    
    title_label = tk.Label(window, text = 'Pas de chanson contenant de mot '+word+' dans notre base de donnees')
    title_label.config(font=('Arial', 32))
    title_label.pack(padx=10, pady=10)
    
    window.mainloop()



