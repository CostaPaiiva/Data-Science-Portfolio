import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import re
from io import BytesIO

# Carregar modelo spaCy local (precisa instalar: python -m spacy download pt_core_news_sm)
nlp = spacy.load("pt_core_news_sm")

def _limpar_html(soup: BeautifulSoup):
    # Remover ruído comum
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form", "noscript"]):
        tag.decompose()

    # Remover blocos por id/class comuns (cookie, ads, menu etc.)
    for el in soup.select(
        "[class*='cookie'], [id*='cookie'], [class*='banner'], [class*='ads'], [id*='ads'], "
        "[class*='sidebar'], [id*='sidebar'], [class*='menu'], [id*='menu']"
    ):
        el.decompose()

def _extrair_texto_principal(soup: BeautifulSoup) -> str:
    candidatos = []
    for sel in ["article", "main", "section"]:
        candidatos.extend(soup.select(sel))

    candidatos.extend(soup.select(
        "div[class*='content'], div[class*='post'], div[class*='entry'], div[class*='article'], div[id*='content']"
    ))

    textos = []
    for c in candidatos:
        t = c.get_text(" ", strip=True)
        if len(t) >= 300:
            textos.append(t)

    if textos:
        return max(textos, key=len)

    # Fallback (sua lógica original)
    textos_p = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    titulos = [h.get_text(" ", strip=True) for h in soup.find_all(["h1", "h2", "h3"])]
    listas = [li.get_text(" ", strip=True) for li in soup.find_all("li")]
    tabelas = [row.get_text(" ", strip=True) for row in soup.find_all("tr")]

    return " ".join(textos_p + titulos + listas + tabelas)

def _meta(soup: BeautifulSoup):
    def get_meta(**kwargs):
        m = soup.find("meta", attrs=kwargs)
        return (m.get("content", "").strip() if m else "")

    og_title = get_meta(property="og:title")
    og_desc = get_meta(property="og:description")
    std_desc = get_meta(name="description")

    title = og_title or (soup.title.get_text(strip=True) if soup.title else "")
    description = og_desc or std_desc
    return title, description

def _sentencas(texto: str):
    partes = re.split(r'(?<=[\.\!\?])\s+', texto.strip())
    return [p.strip() for p in partes if len(p.strip()) > 40]

def _resumo_tfidf(texto: str, stop_words, n_frases=4):
    sents = _sentencas(texto)
    if len(sents) <= n_frases:
        return " ".join(sents)

    vec = TfidfVectorizer(stop_words=stop_words, max_features=2000)
    X = vec.fit_transform(sents)
    scores = X.sum(axis=1).A1

    top_idx = scores.argsort()[::-1][:n_frases]
    top_idx_sorted = sorted(top_idx)
    return " ".join([sents[i] for i in top_idx_sorted])

def extrair_insights(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        return pd.DataFrame({
            "URL": [url],
            "Título": [""],
            "Descrição": [""],
            "Texto Completo": ["Erro ao acessar página: " + str(e)],
            "Resumo": [""],
            "Palavras-chave": [""],
            "Temas": [""],
            "Entidades (Top)": [""],
            "Entidades por Tipo": [""],
            "Top Palavras Frequentes": [""],
            "Palavras": [0],
            "Frases": [0],
            "Leitura (min)": [0]
        })

    soup = BeautifulSoup(response.text, "html.parser")
    _limpar_html(soup)

    titulo, descricao = _meta(soup)
    texto_unico = _extrair_texto_principal(soup)

    # Se vier curto, enriquece com metadados
    if len(texto_unico) < 500:
        texto_unico = f"{titulo}. {descricao}. {texto_unico}".strip()

    if not texto_unico.strip():
        return pd.DataFrame({
            "URL": [url],
            "Título": [titulo],
            "Descrição": [descricao],
            "Texto Completo": ["Nenhum texto encontrado."],
            "Resumo": [""],
            "Palavras-chave": [""],
            "Temas": [""],
            "Entidades (Top)": [""],
            "Entidades por Tipo": [""],
            "Top Palavras Frequentes": [""],
            "Palavras": [0],
            "Frases": [0],
            "Leitura (min)": [0]
        })

    doc = nlp(texto_unico)
    stop_words_pt = list(nlp.Defaults.stop_words)

    # Palavras-chave + bigrams
    vectorizer = TfidfVectorizer(stop_words=stop_words_pt, max_features=25, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([texto_unico])
    feats = vectorizer.get_feature_names_out()

    unigrams = [f for f in feats if " " not in f][:12]
    bigrams = [f for f in feats if " " in f][:10]
    temas = unigrams[:6] + bigrams[:4]

    # Resumo sem LLM
    resumo = _resumo_tfidf(texto_unico, stop_words_pt, n_frases=4)

    # Entidades: dedup + top
    ents = [ent.text.strip() for ent in doc.ents if ent.text.strip()]
    ent_counter = Counter(ents)
    top_ents = [f"{e} ({c})" for e, c in ent_counter.most_common(10)]

    # Entidades por tipo
    ents_by_label = {}
    for ent in doc.ents:
        ents_by_label.setdefault(ent.label_, [])
        ents_by_label[ent.label_].append(ent.text.strip())
    ents_by_label = {k: list(dict.fromkeys(v))[:10] for k, v in ents_by_label.items()}

    # Frequência de palavras (tokens spaCy)
    palavras = [t.text.lower() for t in doc if t.is_alpha and not t.is_stop]
    freq = pd.Series(palavras).value_counts().head(12)

    # Métricas
    n_palavras = len([t for t in doc if t.is_alpha])
    n_frases = max(1, len(_sentencas(texto_unico)))
    leitura_min = max(1, round(n_palavras / 200))  # ~200 palavras/min

    return pd.DataFrame({
        "URL": [url],
        "Título": [titulo],
        "Descrição": [descricao],
        "Texto Completo": [texto_unico],
        "Resumo": [resumo],
        "Palavras-chave": [", ".join(feats)],
        "Temas": [", ".join(temas)],
        "Entidades (Top)": [", ".join(top_ents)],
        "Entidades por Tipo": [str(ents_by_label)],
        "Top Palavras Frequentes": [", ".join(freq.index)],
        "Palavras": [n_palavras],
        "Frases": [n_frases],
        "Leitura (min)": [leitura_min]
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

        # --------- DOWNLOAD CSV (opção) ----------
        csv_data = all_data.to_csv(index=False).encode("utf-8-sig")  # melhor pro Excel BR
        st.download_button(
            label="📥 Baixar CSV",
            data=csv_data,
            file_name="insights.csv",
            mime="text/csv"
        )

        # --------- DOWNLOAD EXCEL (opção) ----------
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            all_data.to_excel(writer, index=False, sheet_name="Insights")
        output.seek(0)

        st.download_button(
            label="📥 Baixar Excel",
            data=output,
            file_name="insights.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.success("Arquivo(s) pronto(s) para download!")
    else:
        st.warning("Nenhuma URL válida foi fornecida.")