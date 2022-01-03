#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 18:45:10 2021

@author: pauline
"""

import pickle
import re
import pandas as pd
import numpy as np

#compter le nombre de mot dans un text
#construire un type dict en faisant {mot1 : occ, mot2 : occ2, mot3 : occ3}
#trouver une librairie qui va regrouper les mots par theme 
#faire la construction des graphes par theme ou alors pour tous les mots en mettant les poids par rapport aux occurences 
#construire un concordancier





#recuperer les donnees
corpus = pd.DataFrame()
#lecture avec pickle
#boucle pour avoir tous les objets serialises pp
with open("corpus.pkl", "rb") as f:
    while True:
        try:
            corpus = pd.concat([corpus, pickle.load(f)], axis = 0).reset_index(drop=True)
        except EOFError:
            break

print(corpus)
list_chanson = corpus['Paroles'].tolist()


from sklearn.feature_extraction.text import TfidfVectorizer
# Instantiate a TfidfVectorizer object
vectorizer = TfidfVectorizer()
# It fits the data and transform it as a vector
X = vectorizer.fit_transform(list_chanson)
# Convert the X as transposed matrix
X = X.T.toarray()
# Create a DataFrame and set the vocabulary as the index
df = pd.DataFrame(X, index=vectorizer.get_feature_names())

print(df)

def get_similar_articles(q, df):
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
      print("Nilai Similaritas:", v)
      print(list_chanson[k])
      print()
# Add The Query
q1 = 'amour'
# Call the function
get_similar_articles(q1, df)


class graph :
    def __init__(self):
        pass
    
    
class noeud(graph) :
    pass
    
    
class clique(graph) :
    pass



#sac de mots    
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(list_chanson) 
print(X.toarray())
print(vectorizer.get_feature_names())


paroles_chanson = list_chanson[0]
#recherche d'un mot
start = paroles_chanson.find('Marqué')
print(start)
print(paroles_chanson[start-10:start+20])



#occurence du mot 
pattern = re.compile("MarqUé", re.IGNORECASE)
res = pattern.finditer(paroles_chanson)
start_pattern = [m.start() for m in res]
print(start_pattern)


#concordancier 
window = 50
def concord(texte, pat):
    pattern = re.compile(pat)
    res = pattern.finditer(texte)
    pos_pattern = [m.span() for m in res]
    context_left = pd.DataFrame([texte[i-window:i-1] for (i, j) in pos_pattern])
    center = pd.DataFrame([texte[i: j] for (i, j) in pos_pattern])
    context_right = pd.DataFrame([texte[j+1:j+window] for (i, j) in pos_pattern])
    return (pd.concat([context_left, center, context_right], axis=1))


concord(paroles_chanson, "aimé")


