import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from io import BytesIO  # <<< ADICIONADO

# Carregar modelo spaCy local (precisa instalar: python -m spacy download pt_core_news_sm)
nlp = spacy.load("pt_core_news_sm")

def extrair_insights(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return pd.DataFrame({
            "URL": [url],
            "Texto Completo": ["Erro ao acessar página: " + str(e)],
            "Palavras-chave": [""],
            "Entidades": [""],
            "Top Palavras Frequentes": [""]
        })

    soup = BeautifulSoup(response.text, "html.parser")

    # Capturar vários elementos da página
    textos = [p.get_text() for p in soup.find_all("p")]
    titulos = [h.get_text() for h in soup.find_all(["h1","h2","h3"])]
    listas = [li.get_text() for li in soup.find_all("li")]
    tabelas = [row.get_text() for row in soup.find_all("tr")]

    # Unir tudo em um texto único
    texto_unico = " ".join(textos + titulos + listas + tabelas)

    if not texto_unico.strip():
        return pd.DataFrame({
            "URL": [url],
            "Texto Completo": ["Nenhum texto encontrado."],
            "Palavras-chave": [""],
            "Entidades": [""],
            "Top Palavras Frequentes": [""]
        })

    # Extrair entidades com spaCy
    doc = nlp(texto_unico)
    entidades = [ent.text for ent in doc.ents]

    # Stopwords em português via spaCy
    stop_words_pt = list(nlp.Defaults.stop_words)

    # Palavras-chave com TF-IDF
    vectorizer = TfidfVectorizer(stop_words=stop_words_pt, max_features=15)
    tfidf_matrix = vectorizer.fit_transform([texto_unico])
    palavras_chave = vectorizer.get_feature_names_out()

    # Frequência simples das palavras
    palavras = [w.lower() for w in texto_unico.split() if w.isalpha()]
    freq = pd.Series(palavras).value_counts().head(10)

    return pd.DataFrame({
        "URL": [url],
        "Texto Completo": [texto_unico],
        "Palavras-chave": [", ".join(palavras_chave)],
        "Entidades": [", ".join(entidades)],
        "Top Palavras Frequentes": [", ".join(freq.index)]
    })

# Interface Streamlit
st.title("Web2Excel Insights")

urls = st.text_area("Cole aqui as URLs (uma por linha)").splitlines()

if st.button("Coletar Insights"):
    all_data = pd.DataFrame()
    for url in urls:
        if url.strip():
            df = extrair_insights(url.strip())
            all_data = pd.concat([all_data, df], ignore_index=True)

    if not all_data.empty:
        st.write(all_data)

        # >>> AO INVÉS DE SALVAR AUTOMATICAMENTE, GERAR EM MEMÓRIA E EXIBIR BOTÃO <<<
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            all_data.to_excel(writer, index=False, sheet_name="Insights")
        output.seek(0)

        st.download_button(
            label="📥 Baixar insights.xlsx",
            data=output,
            file_name="insights.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.success("Arquivo pronto para download!")
    else:
        st.warning("Nenhuma URL válida foi fornecida.")