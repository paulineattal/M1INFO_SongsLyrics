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


titre = []
auteur = []
paroles = []
URL="https://www.paroles.net/les-plus-grands-succes-francophones"


#premiere page avec l'acceptation des cookies
#ouverture de la page

profile = webdriver.FirefoxProfile()
profile.set_preference('permissions.default.desktop-notification', 1)
driver = webdriver.Firefox(firefox_profile=profile)

#driver = webdriver.Firefox()
driver.get(URL)
time.sleep(3)
#accepter les cookies
accept_button = driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div/div/div/div[2]/div[2]/button[2]/span")
accept_button.click()


#recuperer titre et auteur
time.sleep(3) # Wait for reviews to load
titre_chanson = driver.find_element_by_xpath('/html/body/div[4]/section/div/div/div/div[1]/div/div[2]/div/table/tbody/tr[1]/td[1]/p/a').text
auteur_chanson = driver.find_element_by_xpath('/html/body/div[4]/section/div/div/div/div[1]/div/div[2]/div/table/tbody/tr[1]/td[2]/p/a').text
chanson = driver.find_element_by_xpath('/html/body/div[4]/section/div/div/div/div[1]/div/div[2]/div/table/tbody/tr[1]/td[1]/p/a')
chanson.click()
time.sleep(3) # Wait for reviews to load
paroles_chanson = driver.find_element_by_xpath('/html/body/div[2]/section/div/div/div/div[1]/div[3]/div[1]/div/div/div/div[5]/div/div/div[1]/div[2]').text

#modification de la chaine de caractere des paroles
paroles_chanson = paroles_chanson.lower()
titre_chanson = titre_chanson.lower()
auteur_chanson = auteur_chanson.lower()
#modification de la chaine de caractere des paroles
chaine_inutile = "paroles de la chanson " + titre_chanson + " par " + auteur_chanson + "\n"
paroles_chanson = paroles_chanson.replace(chaine_inutile,"")
paroles_chanson = paroles_chanson.replace('\n'," ")    

#enregistrement des paroles, titre et auteur
titre.append(titre_chanson)
auteur.append(auteur_chanson)
paroles.append(paroles_chanson)
#fermeture de la page
driver.close()



for i in range(10,30):
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
    time.sleep(3) # Wait for reviews to load
    titre_chanson = driver.find_element_by_xpath('/html/body/div[2]/section/div/div/div/div[1]/div/div[3]/div/table/tbody/tr['+str(i)+']/td[1]/p/a').text
    auteur_chanson = driver.find_element_by_xpath('/html/body/div[2]/section/div/div/div/div[1]/div/div[3]/div/table/tbody/tr['+str(i)+']/td[2]/p/a').text
    chanson = driver.find_element_by_xpath('/html/body/div[2]/section/div/div/div/div[1]/div/div[3]/div/table/tbody/tr['+str(i)+']/td[1]/p/a')
    chanson.click()
    time.sleep(3) # Wait for reviews to load
    paroles_chanson = driver.find_element_by_xpath('/html/body/div[2]/section/div/div/div/div[1]/div[3]/div[1]/div/div/div/div[5]/div/div/div[1]/div[2]').text

    #modification de la chaine de caractere des paroles
    paroles_chanson = paroles_chanson.lower()
    titre_chanson = titre_chanson.lower()
    auteur_chanson = auteur_chanson.lower()
    chaine_inutile = "paroles de la chanson " + titre_chanson + " par " + auteur_chanson + "\n"
    paroles_chanson = paroles_chanson.replace(chaine_inutile,"")
    paroles_chanson = paroles_chanson.replace('\n'," ")
    paroles_chanson = paroles_chanson.replace("\\","")
   
   
    #enregistrement des paroles, titre et auteur
    titre.append(auteur_chanson)
    auteur.append(auteur_chanson)
    paroles.append(paroles_chanson)
    #fermeture de la page
    driver.close()
   


df = {'Titre' : pd.Series(titre),
      'Auteur' : pd.Series(auteur),
      'Paroles' : pd.Series(paroles)
       
      }
data = pd.DataFrame(df)


#pickling
# Ouverture d'un fichier, puis écriture avec pickle
with open("corpus.pkl", 'ab+') as f:
    pickle.dump(data, f)    


