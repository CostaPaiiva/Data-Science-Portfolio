import streamlit as st # Importa a biblioteca Streamlit para criar aplicativos web interativos.
import requests # Importa a biblioteca requests para fazer requisições HTTP (e.g., baixar páginas web).
from bs4 import BeautifulSoup # Importa BeautifulSoup para parsear e extrair dados de documentos HTML e XML.
import pandas as pd # Importa a biblioteca pandas para manipulação e análise de dados, especialmente com DataFrames.
import spacy # Importa a biblioteca spaCy para processamento de linguagem natural (NLP).
from sklearn.feature_extraction.text import TfidfVectorizer # Importa TfidfVectorizer do scikit-learn para converter texto em matrizes de recursos TF-IDF.
from collections import Counter # Importa Counter do módulo collections para contar a frequência de itens em uma lista.
import re # Importa o módulo re para trabalhar com expressões regulares.
from io import BytesIO # Importa BytesIO do módulo io para lidar com dados binários em memória, útil para downloads de arquivos.

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
    ): # Itera sobre elementos HTML que correspondem aos seletores CSS para remover ruído.
        el.decompose() # Remove o elemento do documento BeautifulSoup.

def _extrair_texto_principal(soup: BeautifulSoup) -> str: # Define uma função para extrair o texto principal de uma página HTML.
    candidatos = [] # Inicializa uma lista para armazenar elementos candidatos a conter o texto principal.
    for sel in ["article", "main", "section"]: # Itera sobre seletores HTML comuns para conteúdo principal.
        candidatos.extend(soup.select(sel)) # Adiciona elementos encontrados com esses seletores à lista de candidatos.

    candidatos.extend(soup.select(
        "div[class*='content'], div[class*='post'], div[class*='entry'], div[class*='article'], div[id*='content']"
    )) # Adiciona divs com classes/ids que indicam conteúdo principal.

    textos = [] # Inicializa uma lista para armazenar o texto extraído dos candidatos.
    for c in candidatos: # Itera sobre cada elemento candidato.
        t = c.get_text(" ", strip=True) # Extrai o texto do elemento, usando espaço como separador e removendo espaços em branco.
        if len(t) >= 300: # Verifica se o comprimento do texto é maior ou igual a 300 caracteres.
            textos.append(t) # Se for longo o suficiente, adiciona o texto à lista.

    if textos: # Verifica se a lista de textos não está vazia.
        return max(textos, key=len) # Retorna o texto mais longo encontrado entre os candidatos.

    # Fallback (sua lógica original)
    textos_p = [p.get_text(" ", strip=True) for p in soup.find_all("p")] # Extrai o texto de todos os parágrafos (<p>) da página, limpando espaços.
    titulos = [h.get_text(" ", strip=True) for h in soup.find_all(["h1", "h2", "h3"])] # Extrai o texto de todos os títulos (<h1>, <h2>, <h3>) da página, limpando espaços.
    listas = [li.get_text(" ", strip=True) for li in soup.find_all("li")] # Extrai o texto de todos os itens de lista (<li>) da página, limpando espaços.
    tabelas = [row.get_text(" ", strip=True) for row in soup.find_all("tr")] # Extrai o texto de todas as linhas de tabela (<tr>) da página, limpando espaços.

    return " ".join(textos_p + titulos + listas + tabelas) # Combina todos os textos extraídos em uma única string, separados por espaço.

def _meta(soup: BeautifulSoup): # Define uma função para extrair metadados como título e descrição da página.
    def get_meta(**kwargs): # Define uma função interna para buscar tags <meta> com atributos específicos.
        m = soup.find("meta", attrs=kwargs) # Procura uma tag <meta> no objeto BeautifulSoup com os atributos fornecidos.
        return (m.get("content", "").strip() if m else "") # Retorna o conteúdo do atributo 'content' da meta tag, se encontrada, ou uma string vazia.

    og_title = get_meta(property="og:title") # Extrai o título Open Graph (usado em redes sociais) da meta tag.
    og_desc = get_meta(property="og:description") # Extrai a descrição Open Graph da meta tag.
    std_desc = get_meta(name="description") # Extrai a descrição padrão da meta tag.

    title = og_title or (soup.title.get_text(strip=True) if soup.title else "") # Define o título usando o título Open Graph, ou o título da tag <title> se disponível.
    description = og_desc or std_desc # Define a descrição usando a descrição Open Graph, ou a descrição padrão.
    return title, description # Retorna o título e a descrição extraídos.

def _sentencas(texto: str): # Define uma função privada para dividir um texto em sentenças.
    partes = re.split(r'(?<=[\.\!\?])\s+', texto.strip()) # Divide o texto em partes usando regex, procurando por '.','!' ou '?' seguidos de espaço.
    return [p.strip() for p in partes if len(p.strip()) > 40] # Retorna uma lista de sentenças, removendo espaços e filtrando por comprimento mínimo de 40 caracteres.

def _resumo_tfidf(texto: str, stop_words, n_frases=4): # Define uma função privada para gerar um resumo de texto usando TF-IDF.
    sents = _sentencas(texto) # Divide o texto fornecido em sentenças usando a função auxiliar _sentencas.
    if len(sents) <= n_frases: # Verifica se o número de sentenças é menor ou igual ao número desejado de frases para o resumo.
        return " ".join(sents) # Se sim, retorna todas as sentenças unidas, pois não há o que resumir.

    vec = TfidfVectorizer(stop_words=stop_words, max_features=2000) # Inicializa um TfidfVectorizer com stopwords e limite de 2000 recursos.
    X = vec.fit_transform(sents) # Calcula as pontuações TF-IDF para cada sentença e as armazena na matriz X.
    scores = X.sum(axis=1).A1 # Soma as pontuações TF-IDF para cada sentença para obter uma pontuação total.

    top_idx = scores.argsort()[::-1][:n_frases] # Obtém os índices das N sentenças com as maiores pontuações TF-IDF.
    top_idx_sorted = sorted(top_idx) # Ordena os índices das sentenças selecionadas para manter a ordem original no resumo.
    return " ".join([sents[i] for i in top_idx_sorted]) # Retorna o resumo unindo as sentenças selecionadas e ordenadas.

def extrair_insights(url): # Define uma função para extrair insights de uma URL.
    headers = { # Define um dicionário para os cabeçalhos da requisição HTTP.
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36" # Define o User-Agent para simular um navegador.
    }

    try: # Inicia um bloco try para capturar exceções durante a requisição.
        response = requests.get(url, headers=headers, timeout=15) # Faz uma requisição GET para a URL com cabeçalhos e timeout.
        response.raise_for_status() # Lança uma exceção para códigos de status HTTP de erro (4xx ou 5xx).
    except Exception as e: # Captura qualquer exceção que ocorra durante a requisição.
        return pd.DataFrame({ # Retorna um DataFrame pandas com informações de erro.
            "URL": [url], # Coluna URL com a URL que causou o erro.
            "Título": [""], # Coluna Título vazia.
            "Descrição": [""], # Coluna Descrição vazia.
            "Texto Completo": ["Erro ao acessar página: " + str(e)], # Mensagem de erro.
            "Resumo": [""], # Coluna Resumo vazia.
            "Palavras-chave": [""], # Coluna Palavras-chave vazia.
            "Temas": [""], # Coluna Temas vazia.
            "Entidades (Top)": [""], # Coluna Entidades (Top) vazia.
            "Entidades por Tipo": [""], # Coluna Entidades por Tipo vazia.
            "Top Palavras Frequentes": [""], # Coluna Top Palavras Frequentes vazia.
            "Palavras": [0], # Coluna Palavras com valor zero.
            "Frases": [0], # Coluna Frases com valor zero.
            "Leitura (min)": [0] # Coluna Leitura (min) com valor zero.
        })

    soup = BeautifulSoup(response.text, "html.parser") # Cria um objeto BeautifulSoup para parsear o HTML da resposta.
    _limpar_html(soup) # Chama a função auxiliar para remover ruído HTML da página.

    titulo, descricao = _meta(soup) # Extrai o título e a descrição da página usando a função auxiliar.
    texto_unico = _extrair_texto_principal(soup) # Extrai o texto principal da página usando a função auxiliar.

    # Se vier curto, enriquece com metadados
    if len(texto_unico) < 500: # Verifica se o comprimento do texto principal é inferior a 500 caracteres.
        texto_unico = f"{titulo}. {descricao}. {texto_unico}".strip() # Adiciona título e descrição ao texto principal para enriquecê-lo.

    if not texto_unico.strip(): # Verifica se o texto principal, após limpeza, está vazio.
        return pd.DataFrame({ # Retorna um DataFrame pandas indicando que nenhum texto foi encontrado.
            "URL": [url], # Coluna URL com a URL processada.
            "Título": [titulo], # Coluna Título com o título extraído.
            "Descrição": [descricao], # Coluna Descrição com a descrição extraída.
            "Texto Completo": ["Nenhum texto encontrado."], # Mensagem indicando ausência de texto.
            "Resumo": [""], # Coluna Resumo vazia.
            "Palavras-chave": [""], # Coluna Palavras-chave vazia.
            "Temas": [""], # Coluna Temas vazia.
            "Entidades (Top)": [""], # Coluna Entidades (Top) vazia.
            "Entidades por Tipo": [""], # Coluna Entidades por Tipo vazia.
            "Top Palavras Frequentes": [""], # Coluna Top Palavras Frequentes vazia.
            "Palavras": [0], # Coluna Palavras com valor zero.
            "Frases": [0], # Coluna Frases com valor zero.
            "Leitura (min)": [0] # Coluna Leitura (min) com valor zero.
        })

    doc = nlp(texto_unico) # Processa o texto principal com o modelo spaCy para análise de NLP.
    stop_words_pt = list(nlp.Defaults.stop_words) # Obtém a lista de stopwords em português do spaCy.

    # Palavras-chave + bigrams
    vectorizer = TfidfVectorizer(stop_words=stop_words_pt, max_features=25, ngram_range=(1, 2)) # Inicializa um TfidfVectorizer para extrair palavras-chave e bigramas.
    tfidf_matrix = vectorizer.fit_transform([texto_unico]) # Calcula a matriz TF-IDF para o texto principal.
    feats = vectorizer.get_feature_names_out() # Obtém os nomes das features (palavras-chave e bigramas) com maior pontuação TF-IDF.

    unigrams = [f for f in feats if " " not in f][:12] # Filtra os unigramas (palavras únicas) das features.
    bigrams = [f for f in feats if " " in f][:10] # Filtra os bigramas (pares de palavras) das features.
    temas = unigrams[:6] + bigrams[:4] # Combina os principais unigramas e bigramas para formar os temas.

    # Resumo sem LLM
    resumo = _resumo_tfidf(texto_unico, stop_words_pt, n_frases=4) # Gera um resumo do texto usando a função TF-IDF.

    # Entidades: dedup + top
    ents = [ent.text.strip() for ent in doc.ents if ent.text.strip()] # Extrai todas as entidades nomeadas do texto processado pelo spaCy.
    ent_counter = Counter(ents) # Conta a frequência de cada entidade.
    top_ents = [f"{e} ({c})" for e, c in ent_counter.most_common(10)] # Obtém as 10 entidades mais comuns com suas contagens.

    # Entidades por tipo
    ents_by_label = {} # Inicializa um dicionário para armazenar entidades agrupadas por tipo.
    for ent in doc.ents: # Itera sobre as entidades encontradas pelo spaCy.
        ents_by_label.setdefault(ent.label_, []) # Garante que a chave para o tipo de entidade exista no dicionário.
        ents_by_label[ent.label_].append(ent.text.strip()) # Adiciona a entidade à lista correspondente ao seu tipo.
    ents_by_label = {k: list(dict.fromkeys(v))[:10] for k, v in ents_by_label.items()} # Remove duplicatas e limita a 10 entidades por tipo.

    # Frequência de palavras (tokens spaCy)
    palavras = [t.text.lower() for t in doc if t.is_alpha and not t.is_stop] # Extrai palavras alfabéticas e não stopwords do texto.
    freq = pd.Series(palavras).value_counts().head(12) # Conta a frequência das palavras e pega as 12 mais comuns.

    # Métricas
    n_palavras = len([t for t in doc if t.is_alpha]) # Conta o número total de palavras alfabéticas no texto.
    n_frases = max(1, len(_sentencas(texto_unico))) # Conta o número de frases no texto, garantindo pelo menos 1.
    leitura_min = max(1, round(n_palavras / 200)) # Estima o tempo de leitura em minutos (aproximadamente 200 palavras por minuto).

    return pd.DataFrame({ # Retorna um DataFrame pandas com todos os insights extraídos.
        "URL": [url], # URL da página.
        "Título": [titulo], # Título da página.
        "Descrição": [descricao], # Descrição da página.
        "Texto Completo": [texto_unico], # Texto principal completo da página.
        "Resumo": [resumo], # Resumo gerado do texto.
        "Palavras-chave": [", ".join(feats)], # Palavras-chave e bigramas extraídos.
        "Temas": [", ".join(temas)], # Temas identificados.
        "Entidades (Top)": [", ".join(top_ents)], # As 10 entidades nomeadas mais frequentes.
        "Entidades por Tipo": [str(ents_by_label)], # Entidades agrupadas por tipo.
        "Top Palavras Frequentes": [", ".join(freq.index)], # As 12 palavras mais frequentes.
        "Palavras": [n_palavras], # Número total de palavras.
        "Frases": [n_frases], # Número total de frases.
        "Leitura (min)": [leitura_min] # Tempo de leitura estimado em minutos.
    })

# ---------------- UI ----------------
st.title("Web2Excel Insights") # Define o título principal do aplicativo Streamlit.

# Inicializa estado
if "urls_text" not in st.session_state: # Verifica se 'urls_text' não está no estado da sessão do Streamlit.
    st.session_state.urls_text = "" # Se não estiver, inicializa 'urls_text' como uma string vazia no estado da sessão.
if "all_data" not in st.session_state: # Verifica se 'all_data' não está no estado da sessão do Streamlit.
    st.session_state.all_data = pd.DataFrame() # Se não estiver, inicializa 'all_data' como um DataFrame vazio no estado da sessão.

# Input das URLs (persistente)
st.session_state.urls_text = st.text_area( # Cria uma área de texto no Streamlit para inserir URLs.
    "Cole aqui as URLs (uma por linha)", # Rótulo da área de texto.
    value=st.session_state.urls_text # Define o valor inicial da área de texto usando o estado da sessão (para persistência).
)
urls = st.session_state.urls_text.splitlines() # Divide o texto da área em uma lista de URLs, separando por linha.

# Botões lado a lado (Coletar / Limpar)
col1, col2 = st.columns(2) # Cria duas colunas para dispor os botões lado a lado.

with col1: # Define o contexto para a primeira coluna.
    coletar = st.button("Coletar Insights", use_container_width=True) # Cria um botão "Coletar Insights" que ocupa a largura total da coluna.

with col2: # Define o contexto para a segunda coluna.
    limpar = st.button("🧹 Limpar resultados", use_container_width=True) # Cria um botão "Limpar resultados" que ocupa a largura total da coluna.

if limpar: # Verifica se o botão "Limpar resultados" foi clicado.
    st.session_state.all_data = pd.DataFrame() # Se clicado, redefine 'all_data' no estado da sessão para um DataFrame vazio.
    # Se quiser limpar também as URLs, descomente a linha abaixo:
    # st.session_state.urls_text = "" # (Comentado) Reinicializa 'urls_text' no estado da sessão para limpar a área de texto.
    st.rerun() # Força o aplicativo Streamlit a reroduzir do início, atualizando a interface.

if coletar: # Verifica se o botão "Coletar Insights" foi clicado.
    all_data = pd.DataFrame() # Inicializa um DataFrame vazio para armazenar os dados coletados nesta execução.
    for url in urls: # Itera sobre cada URL na lista.
        if url.strip(): # Verifica se a URL não está vazia após remover espaços em branco.
            df = extrair_insights(url.strip()) # Chama a função 'extrair_insights' para processar a URL.
            all_data = pd.concat([all_data, df], ignore_index=True) # Concatena o DataFrame resultante com 'all_data'.
    st.session_state.all_data = all_data # Armazena todos os dados coletados no estado da sessão.

# Renderiza resultados sempre que existirem (mesmo após clicar download)
if not st.session_state.all_data.empty: # Verifica se o DataFrame 'all_data' no estado da sessão não está vazio.
    st.write(st.session_state.all_data) # Exibe o DataFrame 'all_data' na interface do Streamlit.

    # --------- DOWNLOAD CSV (opção) ----------
    csv_data = st.session_state.all_data.to_csv(index=False).encode("utf-8-sig") # Converte o DataFrame para CSV, codifica em UTF-8 com BOM.
    st.download_button( # Cria um botão de download no Streamlit.
        label="📥 Baixar CSV", # Rótulo do botão.
        data=csv_data, # Dados a serem baixados (CSV).
        file_name="insights.csv", # Nome do arquivo CSV.
        mime="text/csv" # Tipo MIME do arquivo.
    )

    # --------- DOWNLOAD EXCEL (opção) ----------
    output = BytesIO() # Cria um objeto BytesIO para armazenar dados binários em memória.
    with pd.ExcelWriter(output, engine="openpyxl") as writer: # Cria um escritor de Excel usando openpyxl e o objeto BytesIO.
        st.session_state.all_data.to_excel(writer, index=False, sheet_name="Insights") # Escreve o DataFrame para o objeto Excel em memória.
    output.seek(0) # Retorna o ponteiro do BytesIO para o início.

    st.download_button( # Cria um segundo botão de download no Streamlit.
        label="📥 Baixar Excel", # Rótulo do botão.
        data=output, # Dados a serem baixados (Excel).
        file_name="insights.xlsx", # Nome do arquivo Excel.
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" # Tipo MIME do arquivo Excel.
    )

    st.success("Arquivo(s) pronto(s) para download!") # Exibe uma mensagem de sucesso na interface.
else: # Se o DataFrame 'all_data' no estado da sessão estiver vazio.
    st.info("Cole as URLs e clique em **Coletar Insights**.") # Exibe uma mensagem informativa na interface.