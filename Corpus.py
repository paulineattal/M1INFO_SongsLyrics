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
        #return f"Paroles de la chanson {self.df['Titre']}, par {self.df['Auteur']}\n {self.df['Paroles originales']}"
        
    def get_similar_song(self, w, df, list_chanson, vectorizer):
        print("Voici les chansons contanant le mot " + w + " affichées par ordre de pertinance : \n")
        # Convertir le mot en vecteur
        w = [w]
        w_vec = vectorizer.transform(w).toarray().reshape(df.shape[0],)
        sim = {}
        # Ccalcul de la similarite cosinus
        for i in range(10):
            sim[i] = np.dot(df.loc[:, i].values, w_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(w_vec)
      
        # tri des valeurs 
        sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
        #stocke les indices du dataframe des chansons selectionnees
        list_indice_chanson_sel = []
        #afficher les chanson par ordre de similarite
        for k, v in sim_sorted:
            if v != 0.0:
                print(list_chanson[k])
                list_indice_chanson_sel.append(k)
        #liste des indices des chansons selectionnees
        return list_indice_chanson_sel
              
