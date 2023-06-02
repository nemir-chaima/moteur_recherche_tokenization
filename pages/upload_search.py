#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 16:27:26 2023

@author: chaimanemir
"""

import re
import spacy
import streamlit as st
from io import StringIO

"# Télecharger et Chercher !"

mot = st.text_input(label="Entrez un mot clé", value='')
uploaded_files=st.file_uploader("choose a file ")#accept_multiple_files=True
search = st.button('Lacncez la recherche')


nlp= spacy.load("fr_core_news_sm")
#nettoyer les chiffres , stop word et punctuations
def clean_text(s):
    nlp=spacy.load("fr_core_news_sm")
    l=" "
    sw=nlp.Defaults.stop_words
    for i in s.split(): 
        if i not in sw:
            l+= " "
            l+= i
    doc = nlp(l)
    l=''
    for i in doc :
        if ((i.is_punct==False)&(i.is_digit==False)):
            l+= " "
            l+= i.text 
    return l.lower()
#extraire les mots sans repetitions 
def word_extract(liste_string):
    k=[]
    for i in liste_string:
        if i not in k :
            k.append(i)
    return k
#nombre d'occurence de tous les mots 
def count_occ(liste_mot):
    cpt={}
    for i in liste_mot:    
        cpt[i]=liste_mot.count(i)
    return cpt
#le test d'existance de mots 
def find_word(word, liste_word):
    if word in liste_word:  
        return True
    else :
        return False

if uploaded_files is not None:

        # pour lire le fichier mot par mot:
        bytes_data = uploaded_files.getvalue()
        s=StringIO(uploaded_files.getvalue().decode("utf-8"))
        l = s.read()

        cleaned= clean_text(l) # faire appel a la fonction pour nettoyer le text
        cleaned= cleaned.strip('    ')
        
        words_with_rep = re.findall(r'\w+', cleaned) #extraire tous les mots dans un text
        words_no_rep= word_extract(words_with_rep) # faire appl a la fonction pour supprimer la repition des mots 
        cpt= count_occ(words_with_rep) # compter le nombre d'occurrnce 
        exist=find_word(mot, words_no_rep) # parcourir la BDD pour voir si le mot introduit exist 
        if search: # affichage 
            if exist== True:
                nombre_occ= cpt[mot]
                st.write( " ce mot est apparue ", nombre_occ , "fois dans ce document")
            else :
                st.write('aucun document trouvé pour ', mot)
