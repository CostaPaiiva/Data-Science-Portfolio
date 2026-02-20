import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

# Carregar modelo spaCy local (precisa instalar: python -m spacy download pt_core_news_sm)
nlp = spacy.load("pt_core_news_sm")

def extrair_insights(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return pd.DataFrame({
            "URL": [url],
            "Texto Original": ["Erro ao acessar página: " + str(e)],
            "Palavras-chave": [""],
            "Entidades": [""]
        })

    soup = BeautifulSoup(response.text, "html.parser")
    textos = [p.get_text() for p in soup.find_all("p")]
    texto_unico = " ".join(textos)

    if not texto_unico.strip():
        return pd.DataFrame({
            "URL": [url],
            "Texto Original": ["Nenhum texto encontrado."],
            "Palavras-chave": [""],
            "Entidades": [""]
        })

    # Extrair entidades com spaCy
    doc = nlp(texto_unico)
    entidades = [ent.text for ent in doc.ents]

    # TF-IDF para palavras-chave
    vectorizer = TfidfVectorizer(stop_words="portuguese", max_features=10)
    tfidf_matrix = vectorizer.fit_transform([texto_unico])
    palavras_chave = vectorizer.get_feature_names_out()

    return pd.DataFrame({
        "URL": [url],
        "Texto Original": [texto_unico[:500]],  # limitar tamanho para não ficar gigante
        "Palavras-chave": [", ".join(palavras_chave)],
        "Entidades": [", ".join(entidades)]
    })

# Interface Streamlit
st.title("Coletor Automático de Insights (sem API de IA) → Excel")

urls = st.text_area("Cole aqui as URLs (uma por linha)").splitlines()

if st.button("Coletar Insights"):
    all_data = pd.DataFrame()
    for url in urls:
        if url.strip():
            df = extrair_insights(url.strip())
            all_data = pd.concat([all_data, df], ignore_index=True)

    if not all_data.empty:
        st.write(all_data)
        all_data.to_excel("insights.xlsx", index=False)
        st.success("Arquivo insights.xlsx gerado com sucesso!")
    else:
        st.warning("Nenhuma URL válida foi fornecida.")
