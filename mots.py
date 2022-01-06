#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 18:45:10 2021

@author: pauline
"""

import random
import matplotlib.pyplot as plt
from imageio import imread
from wordcloud import WordCloud
from graph_of_words import GraphOfWords



class Graph :
    def __init__(self, mots, titre):
        self.mots = mots
        self.titre = titre
    
    def word_cloud(self, limit, sm_french) :
    
        #graphique en nuage de mot d'un texte
        fontcolor = '#000000' #couleur de la police
        bgcolor = '#ffffff' # couleur de fond
            
        wordcloud = WordCloud(
            max_words=limit,
            stopwords= sm_french, # liste de mots-outils
            mask=imread('mask.png'),
            contour_width=3,
            background_color=bgcolor,
            #font_path=font
        ).generate(self.mots.lower()) 
            
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


    
        
    # nlp = spacy.load("fr_core_news_sm")
    # doc = nlp(texte)
    # text_list = []
    # head_list = []
    # for token in doc:
    #     if token.is_alpha:
    #         if not token.is_stop:
    #             text_list.append(token.lemma_)
    #             head_list.append(token.head.text.lower())
    # df = pd.DataFrame(list(zip(text_list, head_list)), 
    #                columns =['text', 'head'])
    # combos = df.groupby(['text','head']).size().reset_index().rename(columns={0:'count'}).sort_values('count', ascending=False)
    
    
    

    
class Clique(Graph) :
    def __init__(self, mots, titre, nbMots):
        super().__init__(mots=mots, titre=titre)
        self.nbMots = nbMots  

    
    def display_topics(self, model, tf_feature_names):
        for topic_idx, topic in enumerate(model.components_):
            print("Topic {}:".format(topic_idx))
            str_words = " ".join([tf_feature_names[i] for i in topic.argsort()[:-self.nbMots - 1:-1]])
            
            graph = GraphOfWords(window_size=2)
            graph.build_graph(
                str_words,
                workers=4
            )
            graph.display_graph()
            graph.write_graph_edges('edges_list.txt')
               
    
    
    
    
    




