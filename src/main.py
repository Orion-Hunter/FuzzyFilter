import streamlit as st
import pandas as pd
import os
from fuzzywuzzy import fuzz as fw

uri = 'data/bad_words.csv'

if os.path.exists(uri):
    print(True)
else:
    print(False)


data = pd.read_csv(uri) 
st.title("Filtro Anti Cancelamento com Lógica Fuzzy")
def compare_data(word):   
    x = []
    y = []
    for index, item in data.iterrows():
        com = fw.token_set_ratio(word, item['word'])
        if com >= 80:
           x.append(item['word'])
           y.append(com)
    if len(x): 
       return word, x,y
    return None 
    

def compare_text(text):
    l = text.split(" ")
    words_filtered = []
    terms_similarity = []
    probability = []
    for r in l:
        res = compare_data(r)
        if res != None:
           words_filtered.append(res[0])
           terms_similarity.append(res[1])
           probability.append(res[2])
    return words_filtered, terms_similarity
    

texto = st.text_area('Texto: ', height = 175)

filtro = st.button('Filtrar')
if filtro:
    words_filtered, terms_similarity = compare_text(texto)
    filtered = ''
    terms = ''
    if len(words_filtered) > 0:
       st.write("Seu texto possui {} termos potencialmente inadequados ou ofensivos.".format(len(words_filtered)))
       for t in words_filtered:
           filtered += t + "\n"
       st.text_area("",value=filtered, height=275)
       st.write()
       st.write("Os termos acima foram qualificados como potencialmente inadequados ou ofensivos por apresentarem graus de similiaridade significativos(a partir de 80%) com os seguintes termos:") 
       st.write()
       for ts in terms_similarity:
           for term in ts:
               terms+= term+"\n"
       st.text_area("", value = terms, height=275)