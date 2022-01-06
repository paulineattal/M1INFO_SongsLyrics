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

import spacy

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from graph_of_words import GraphOfWords
import nltk



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

    corpus = pd.read_csv("~/Documents/M1/algo avance/Projet/python_chanson/corpus.csv")
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
    sm_french = pd.read_csv("~/Documents/M1/algo avance/Projet/python_chanson/Stop-mots.txt", header=None)
    sm_french = sm_french[0].tolist()
    
    
    

    
    nlp = spacy.load("fr_core_news_sm")
    doc = nlp(texte)
    text_list = []
    head_list = []
    for token in doc:
        if token.is_alpha:
            if not token.is_stop:
                text_list.append(token.lemma_)
                head_list.append(token.head.text.lower())
    df = pd.DataFrame(list(zip(text_list, head_list)), 
                   columns =['text', 'head'])
    combos = df.groupby(['text','head']).size().reset_index().rename(columns={0:'count'}).sort_values('count', ascending=False)
    
    
    
    
    
    str_test = "amour aimer aime sexe dans le lit avec mon fiance et le mariage"
    graph = GraphOfWords(window_size=2)
    graph.build_graph(
        'Roses are red. Violets are blue',
        # OR a sentences list['Roses  are  red.', 'Violets are blue'],
        remove_stopwords=False,
        workers=4
    )
    graph.display_graph()
    
            
            
    
    def display_topics(model, feature_names, no_top_words):
        for topic_idx, topic in enumerate(model.components_):
            print("Topic {}:".format(topic_idx))
            str_words = " ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])
            print(str_words)
            
            graph = GraphOfWords(window_size=2)
            graph.build_graph(
                str_words,
                workers=4
            )
            graph.display_graph()
            graph.write_graph_edges('edges_list.txt')
               
    
    
    
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=1000, stop_words=sm_french)
    tf=tf_vectorizer.fit_transform(list_chanson)
    tf_feature_names = tf_vectorizer.get_feature_names()
    # Créer le modèle LDA
    lda = LatentDirichletAllocation(n_components=1, max_iter=5, learning_method='online', learning_offset=50., random_state=0)
    lda.fit(tf)
    #run function
    display_topics(lda, tf_feature_names, 10)
    
    
    
    
    
    

#########################################################
#graphique en nuage de mot d'un texte
    
    # nombre de mots à afficher
    limit = 50
    fontcolor = '#000000'
    bgcolor = '#ffffff' # couleur de fond
        
    wordcloud = WordCloud(
        max_words=limit,
        stopwords= sm_french, # liste de mots-outils
        mask=imread('~/OneDrive/Documents/Master1_Informatique/Algo/python_chanson/mask.png'),
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
    
###################################################3
    
    
    
    
    
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




