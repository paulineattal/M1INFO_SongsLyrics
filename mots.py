#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 18:45:10 2021

@author: pauline
"""

import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import random
import matplotlib.pyplot as plt
from imageio import imread
from wordcloud import WordCloud


#compter le nombre de mot dans un text
#construire un type dict en faisant {mot1 : occ, mot2 : occ2, mot3 : occ3}
#trouver une librairie qui va regrouper les mots par theme 
#faire la construction des graphes par theme ou alors pour tous les mots en mettant les poids par rapport aux occurences 
#construire un concordancier



class graph :
    def __init__(self, ):
        pass
    
    
    corpus = pd.DataFrame()
    #lecture avec pickle
    #boucle pour avoir tous les objets serialises 
    with open("corpus_chanson.pkl", "rb") as f:
        while True:
            try:
                corpus = pd.concat([corpus, pickle.load(f)], axis = 0).reset_index(drop=True)
            except EOFError:
                break

    
    list_chanson = corpus['Paroles graphes'].tolist()


    # Instantiate a TfidfVectorizer object
    vectorizer = TfidfVectorizer()
    # It fits the data and transform it as a vector
    X = vectorizer.fit_transform(list_chanson)
    # Convert the X as transposed matrix
    X = X.T.toarray()
    # Create a DataFrame and set the vocabulary as the index
    df = pd.DataFrame(X, index=vectorizer.get_feature_names())
    print(df)

    def get_similar_articles(q, df, list_chanson, vectorizer):
        print("query:", q)
        print("Voici les articles avec les valeurs de similarité cosinus les plus élevées : ")
        # Convert the query become a vector
        q = [q]
        q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
        sim = {}
        # Calculate the similarity
        for i in range(10):
            sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
     
      
        # Sort the values 
        sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
        # Print the articles and their similarity values
        for k, v in sim_sorted:
            if v != 0.0:
                print("valeur similaire :", v)
                print(list_chanson[k])
              

    # Add The Query
    q1 = 'amour'
    # Call the function
    get_similar_articles(q1, df, list_chanson, vectorizer)
    

    texte = list_chanson[0]
    
    
    with open("Stop-mots.txt", "r", encoding='utf8') as f:
        sm_french = [line.rstrip("\n") for line in f.readlines()]
    
    
    # nombre de mots à afficher
    limit = 50
    fontcolor = '#000000'
    bgcolor = '#ffffff' # couleur de fond
        
    wordcloud = WordCloud(
        max_words=limit,
        stopwords= sm_french, # liste de mots-outils
        mask=imread('~/Documents/M1/algo avance/Projet/python_chanson/mask.png'),
        contour_width=3,
        background_color=bgcolor,
        #font_path=font
    ).generate(texte.lower()) 
        
    fig = plt.figure()
    # taille de la figure
    fig.set_figwidth(14)
    fig.set_figheight(18)
    #titre de la figure
    title = "Titre" #metre artiste et titre chanson
    
    #changer couleurs du texte
    def couleur(*args, **kwargs):
        return "rgb(0, 100, {})".format(random.randint(100, 255))
    
    plt.imshow(wordcloud.recolor(color_func=couleur))
    plt.title(title, color=fontcolor, size=30, y=1.01)
    plt.axis('off')
    plt.show()
    
    
    
    
    
    # #concordancier 
    # def concord(texte, pat, window):
    #     pattern = re.compile(pat)
    #     res = pattern.finditer(texte)
    #     pos_pattern = [m.span() for m in res]
    #     context_left = pd.DataFrame([texte[i-window:i-1] for (i, j) in pos_pattern])
    #     center = pd.DataFrame([texte[i: j] for (i, j) in pos_pattern])
    #     context_right = pd.DataFrame([texte[j+1:j+window] for (i, j) in pos_pattern])
    #     return (pd.concat([context_left, center, context_right], axis=1))
    
    # concord(texte, "amour", 50)
    
    
    
class noeud(graph) :
    pass
    
    
class clique(graph) :
    pass




