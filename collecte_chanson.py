#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 17:55:50 2021

@author: pauline
"""

from selenium import webdriver
import pandas as pd
import time
import pickle
import re


titre = []
auteur = []
paroles_orig = []
paroles_graph = []
URL="https://www.paroles.net/les-plus-grands-succes-francophones"


for i in range(0,31):
    #ouverture de la page
    profile = webdriver.FirefoxProfile()
    profile.set_preference("dom.webnotifications.enabled", False)
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get(URL)
    time.sleep(3)
    
    #accepter les cookies (ne s'affiche pas forcement apres ouverture de plusieurs pages)
    accept_button = driver.find_elements_by_xpath("/html/body/div[6]/div[2]/div/div/div/div/div/div/div[2]/div[2]/button[2]/span")
    if len(accept_button) > 0 :
        driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div/div/div/div[2]/div[2]/button[2]/span").click()
    accept_button = driver.find_elements_by_xpath("/html/body/div[5]/div[2]/div/div/div/div/div/div/div[2]/div[2]/button[2]/span")
    if len(accept_button) > 0 :
        driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/div/div/div/div/div/div[2]/div[2]/button[2]/span").click()
    #recuperer titre et auteur
    time.sleep(3)
    titre_chanson = driver.find_element_by_xpath('/html/body/div[2]/section/div/div/div/div[1]/div/div[2]/div/table/tbody/tr['+str(i)+']/td[1]/p/a').text
    auteur_chanson = driver.find_element_by_xpath('/html/body/div[2]/section/div/div/div/div[1]/div/div[2]/div/table/tbody/tr['+str(i)+']/td[2]/p/a').text
    chanson = driver.find_element_by_xpath('/html/body/div[2]/section/div/div/div/div[1]/div/div[2]/div/table/tbody/tr['+str(i)+']/td[1]/p/a')
    chanson.click()
    time.sleep(3)
    #recuperer les paroles
    paroles_chanson_orig = driver.find_element_by_xpath('/html/body/div[2]/section/div/div/div/div[1]/div[3]/div[1]/div/div/div/div[5]/div/div/div[1]/div[2]').text

    #modification de la chaine de caractere des paroles
    paroles_chanson_graph = paroles_chanson_orig.lower()
    titre_chanson = titre_chanson.lower()
    auteur_chanson = auteur_chanson.lower()
    chaine_inutile = "paroles de la chanson " + titre_chanson + " par " + auteur_chanson + "\n"
    paroles_chanson_graph = paroles_chanson_graph.replace(chaine_inutile,"")
    paroles_chanson_graph = paroles_chanson_graph.replace('\n'," ")    
    paroles_chanson_graph = paroles_chanson_graph.replace("\\","")
    paroles_chanson_graph = paroles_chanson_graph.replace("’", "'") #remplacer les mauvauses apostrophes
    paroles_chanson_graph = re.sub(r"([a-zA-Z]+)(?=')", "", paroles_chanson_graph) #enleve les mots avant les apostrophes
    paroles_chanson_graph = paroles_chanson_graph.replace("\'","")  #enlever les apostrophes
    paroles_chanson_graph = paroles_chanson_graph.replace("\"","")  #enlever les guillemets

    #enregistrement des paroles, titre et auteur dasn des listes
    titre.append(titre_chanson)
    auteur.append(auteur_chanson)
    paroles_orig.append(paroles_chanson_orig)
    paroles_graph.append(paroles_chanson_graph)
    #fermeture de la page
    driver.close()
   
#creation de dataframe a partir des listes
df = {'Titre' : pd.Series(titre),
      'Auteur' : pd.Series(auteur),
      'Paroles originales' : pd.Series(paroles_orig),
      'Paroles graphes' : pd.Series(paroles_graph),
      }
data = pd.DataFrame(df)


#enlever les chansons en anglais
list_index = [0,1] 
data.drop(list_index , inplace=True)
data = data.reset_index(drop=True)

#si un fichier de donnees a ete deja enregistrer, le recuperer et coller les donnees ensembles
data_av = pd.read_csv('datas/data.csv')
data = pd.concat([data, data_av], axis = 0).reset_index(drop=True)
data.to_csv('datas/data.csv', index = False)


#pickling
# Ouverture d'un fichier, puis écriture avec pickle
with open("datas/corpus_chanson.pkl", 'wb') as f: #ab+
    pickle.dump(data, f)


#recuperer les donnees
corpus = pd.DataFrame()
#lecture avec pickle
#boucle pour avoir tous les objets serialises 
with open("datas/corpus_chanson.pkl", "rb") as f:
    while True:
        try:
            corpus = pd.concat([corpus, pickle.load(f)], axis = 0).reset_index(drop=True)
        except EOFError:
            break
#sauvegarder en csv 
corpus.to_csv('datas/corpus.csv', index = False)

 
 
 
