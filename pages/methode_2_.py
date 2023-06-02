#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 07:08:14 2023

@author: chaimanemir
"""

import re
import spacy
import streamlit as st
import os
import enchant 


"# Recherche !"

mot = st.text_input(label="Entrez un mot clé", value='')
search = st.button('Lacncez la recherche')


#ouvrir et lire le fichier
def read_files(file_path):
   with open(file_path, 'r') as file:
      return file.read()

#calculer le nombre d'occ des mots dans un file
def count_occ(liste_mot):
    cpt={}
    for i in liste_mot:    
        cpt[i]=liste_mot.count(i)
    return cpt
#tester si le mot existe dans un fichier 
def trouver_mot(word, dict_of_files):
    liste=[]
    for key in dict_of_files.keys():
        k=key
    if word in dict_of_files[k]:
            liste.append((k,dict_of_files[k][word]))
 
    return liste
 
 
nlp= spacy.load("fr_core_news_sm")
# enlever les stops words , chiffre et punctuation
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

# Proposer un mot similaire en cas d'erreur de saisie
def suggest_word(word):
    d = enchant.Dict("fr_FR")
    if d.check(word):
        return word
    else:
        suggest = d.suggest(word)
        if len(suggest) == 0:
            return None
        else:
            new_word = st.selectbox('vous voulez dire: ',suggest)
            return new_word

# Fonction pour lancer la recherche
def search_word(word, dic_words):
    exist_list = trouver_mot(word, dic_words)
    exist=[];apparence=[]
    if len(exist_list)!=0:
        exist.append(True)
        for i in range(0,len(exist_list)):
            apparence.append((exist_list[i][1],exist_list[0][i]))
            # st.write("le mot", word, "est apparu", exist_list[i][1],"fois dans le fichier",exist_list[0][i])
    else: 
        exist.append(False)
        #st.write("le mot ", word, "n'apparait dans aucun fichier")
    #     new_word = suggest_word(word)
    #     if new_word is not None:
    #         search_word(new_word, dic_words)
    # if ((True not in exist)and (False in exist)):
    #     st.write("le mot ", word, "n'apparait dans aucun fichier")
    # else : 
    #     st.write(f'<span style="color:green"><b>Le mot "{mot}" est apparu :</b></span>', unsafe_allow_html=True)
    #     for i in range(len(apparence)):
    #         st.write(" -", apparence[i][0],"fois dans le fichier :",f'<span style="color:blue"><b>{apparence[i][1]}</b></span>', unsafe_allow_html=True)

        # else:
        #     st.write("Aucun mot similaire trouvé")
    return apparence,exist

            
#definir le chemin du directory     
path ="/Users/chaimanemir/Desktop/files"
#changer le directory
os.chdir(path)
#iterer sur tous les fichiers du dossier
dic_words={}

nombre_occ=[];
for file in os.listdir():

   if file.endswith('.txt'): # recup le chemin du fichier
      file_path =f"{path}/{file}"
      file_name = os.path.basename(file_path) # extraire le nom de fichier
      l= read_files(file_path) # appeller la fonction pour lire l fichier

      cleaned= clean_text(l) #appeller la focntion pour nettoyer le text
      cleaned= cleaned.strip('    ')    # j'ai du  rajouter ca pcq ca me retourne un espace au debut  
      words_with_rep = re.findall(r'\w+', cleaned) # extraire tous les mots avec repetition

      cpt= count_occ (words_with_rep) # compter le nombre d'occurence de chaque mot
      dic_words[file_name]= cpt #crer un dictionnaire contenant le nombre d'occ de chaque mot dans chaque fichier
      apparence, exist=search_word(mot,dic_words)
     
   if ((True not in exist)and (False in exist)):
      # st.write("le mot ", mot, "n'apparait dans aucun fichier")
      new_word = suggest_word(mot)
      if new_word is not None:
          apparence2,exist2=search_word(new_word, dic_words)
          if True not in exist2:
            st.write("le mot ", mot, "n'apparait dans aucun fichier")  
          else:
              st.write(f'<span style="color:green"><b>Le mot "{mot}" est apparu :</b></span>', unsafe_allow_html=True)
              for i in range(len(apparence2)):
                  st.write(" -", apparence2[i][0],"fois dans le fichier :",f'<span style="color:blue"><b>{apparence2[i][1]}</b></span>', unsafe_allow_html=True)

   else : 
      st.write(f'<span style="color:green"><b>Le mot "{mot}" est apparu :</b></span>', unsafe_allow_html=True)
      for i in range(len(apparence)):
          st.write(" -", apparence[i][0],"fois dans le fichier :",f'<span style="color:blue"><b>{apparence[i][1]}</b></span>', unsafe_allow_html=True)


              
# ------------------------------------------ sans libraires ------------------


# stop_word = ["alors","au","aussi","autre","avant","avec","bon","bientôt","car","ce","cela","ces","ceux","chaque","ci",
# "comme","comment","dans","des","du","dedans","dehors","depuis","deux","donc","début","en","encore","et","eu","haut",
# "hors","ici","la","le","les","leur","là", "ma","maintenant","mais","mes","moins","mon","même","ni","notre","ou","où",
# "par","parce","pas","peu","plupart","pour","pourquoi","quand","quel","que","quelle","quelles","quels","qui","sa","sans",
# "ses","seulement","si","sien","son","sous","sur","ta","tandis","tellement","tels","tes","ton","tous","tout","trop","très","tu",
# "votre","vous","vu","afin","ainsi","aprés","assez","aucun","aucune","auprés","auquel","auquelles","auquels","aussitôt","autres",
# "aux","beaucoup","ceci","celle","celles","celui","cependant","certes","cet","cette","chacun","chacune","chez"]

# digits= [0,1,2,3,4,5,6,7,8,9]
# punctuation = [".", ",", ";", ":", "etc","'","!","?","`","(",")","[","]","{","}"]

# #enlever les stop words , chiffres et la punctuations
# def clean_text2(s,stop_word,digits,punctuation):
#     sw= stop_word
#     l=" "
#     s=s.lower()
#     s=s.split()
#     for i in s: 
#         if ((i not in sw)&(i not in punctuation)):
#             l+= " "
#             l+= i
#     doc=l.split()
#     l=' '
#     for i in range(len(doc)):
#         if ((doc[i] not in digits)or (doc[i]+doc[i+1]not in digits)or (doc[i]+doc[i+1]+doc[i+2]not in digits)or(doc[i]+doc[i+1]+doc[i+2]+doc[i+3]not in digits)):
#           l+=' '
#           l+= doc[i]
#     return l

# #definir le chemin du directory     
# path ="/Users/chaimanemir/Desktop/files"
# #changer le directory
# os.chdir(path)
# #iterer sur tous les fichiers du dossier
# dic_words={}

# nombre_occ=[];
# for file in os.listdir():

#     if file.endswith('.txt'): # recup le chemin du fichier
#       file_path =f"{path}/{file}"
#       file_name = os.path.basename(file_path) # extraire le nom de fichier
#       l= read_files(file_path) # appeller la fonction pour lire l fichier

#       cleaned= clean_text2(l) #appeller la focntion pour nettoyer le text
#       cleaned= cleaned.strip('    ')    # j'ai du  rajouter ca pcq ca me retourne un espace au debut  
#       words_with_rep = re.findall(r'\w+', cleaned) # extraire tous les mots avec repetition

#       cpt= count_occ (words_with_rep) # compter le nombre d'occurence de chaque mot
#       dic_words[file_name]= cpt #crer un dictionnaire contenant le nombre d'occ de chaque mot dans chaque fichier
#       search_word(mot,dic_words)
