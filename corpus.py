#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

class Corpus :
    
    #classe qui recupere le dataframe des donnees deserialisees
    #la collecte des donnees a ete fait au prealable avec Selenium
    #le nettoyage des donnees a aussi ete fait lors de la collecte des donnees
    
    def __init__(self, df) : 
        self.df = df
        
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Dataframe : {self.df}"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"PDataframe {self.df}"
     
    # def __str__(self):
    #     return f"Paroles de la chanson {self.df['Titre']}, par {self.df['Auteur']}\n {self.df['Paroles originales']}"
        
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
        list_indice_chanson_sel = []
        for k, v in sim_sorted:
            if v != 0.0:
                print("valeur similaire :", v)
                print(list_chanson[k])
                list_indice_chanson_sel.append(k)
                
        return list_indice_chanson_sel
              
