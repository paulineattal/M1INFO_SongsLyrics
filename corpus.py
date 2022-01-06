#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 10:41:01 2022

@author: pauline
"""

import numpy as np

class Corpus :
    def __init__(self, df) : 
        self.df = df
        
        
    def get_similar_song(self, w, df, list_chanson, vectorizer):
        print("query:", w)
        print("Voici les articles avec les valeurs de similarité cosinus les plus élevées : ")
        # Convert the query become a vector
        w = [w]
        q_vec = vectorizer.transform(w).toarray().reshape(df.shape[0],)
        sim = {}
        # Calculate the similarity
        for i in range(10):
            sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
     
      
        # Sort the values 
        sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
        # Print the articles and their similarity values
        list_chanson_sel = []
        for k, v in sim_sorted:
            if v != 0.0:
                print("valeur similaire :", v)
                print(list_chanson[k])
                list_chanson_sel.append(list_chanson[k])
                
        return list_chanson_sel
              
