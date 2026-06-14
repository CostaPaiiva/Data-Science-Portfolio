# Web2Excel Insights

Aplicação em **Streamlit** para coletar conteúdo de páginas web (URLs), limpar ruído do HTML e gerar **insights** locais usando **spaCy + TF-IDF**, com exportação em **CSV** e **Excel** via botão de download.

> ✅ Sem LLM  
> ✅ Sem API paga  
> ✅ Simples e rápido (resumo, temas, entidades, métricas)

---

## ✨ O que o app faz

A partir de uma lista de URLs (uma por linha), o app:

- Baixa o HTML com `requests`
- Remove ruídos comuns (scripts, menus, cookie banners, sidebar, ads, etc.)
- Tenta extrair o **texto principal** (prioriza `article/main/section` e `divs` típicas de conteúdo)
- Extrai:
  - **Título** e **Descrição** (meta/og + `<title>`)
  - **Texto completo**
  - **Resumo (heurístico)**: top frases por relevância (TF-IDF)
  - **Palavras-chave** (TF-IDF)
  - **Temas** (combinação de unigrams + bigrams TF-IDF)
  - **Entidades** (spaCy): top entidades + entidades por tipo
  - **Top palavras frequentes** (tokens alpha sem stopwords)
  - **Métricas**: total de palavras, frases e tempo estimado de leitura

Por fim, exibe a tabela e disponibiliza botões para:
- 📥 Baixar CSV (`insights.csv`)
- 📥 Baixar Excel (`insights.xlsx`)

---

## 🧱 Estrutura do projeto

Exemplo simples:


web2excel-insights/

├─ app.py

├─ requirements.txt

└─ README.md


---

## ✅ Requisitos

- Python 3.9+ (recomendado 3.10 ou 3.11)
- Dependências:
  - streamlit
  - requests
  - beautifulsoup4
  - pandas
  - spacy
  - scikit-learn
  - openpyxl

Além disso, é necessário instalar o modelo PT do spaCy:
- `pt_core_news_sm`

---

## 🚀 Instalação

### 1) Clone (ou crie) a pasta do projeto
```bash
mkdir web2excel-insights
cd web2excel-insights
2) Crie e ative um ambiente virtual (recomendado)

Windows

python -m venv .venv
.venv\Scripts\activate

Linux/macOS

python -m venv .venv
source .venv/bin/activate
3) Instale dependências
pip install -r requirements.txt
4) Baixe o modelo do spaCy (Português)
python -m spacy download pt_core_news_sm
▶️ Como rodar
streamlit run app.py

Abra o link que o Streamlit mostrar no terminal (geralmente http://localhost:8501).

🧾 requirements.txt sugerido

Crie um arquivo requirements.txt com:

streamlit
requests
beautifulsoup4
pandas
spacy
scikit-learn
openpyxl

Se quiser travar versões (mais “produção”), execute:

pip freeze > requirements.txt
🧠 Como os insights são gerados (sem LLM)
1) Limpeza do HTML

Remove tags e seções que geralmente não são conteúdo:

script, style, nav, footer, header, aside, form, noscript

elementos com classes/ids contendo: cookie, banner, ads, sidebar, menu

2) Extração do texto principal

Prioriza conteúdo dentro de:

article, main, section

div comuns (content/post/entry/article)

Se não encontrar, usa fallback por tags:

p, h1/h2/h3, li, tr

3) Palavras-chave (TF-IDF)

Aplica TfidfVectorizer com:

stopwords do spaCy PT

ngram_range=(1,2) para unigrams e bigrams

4) Resumo heurístico

Divide o texto em frases e ranqueia cada frase pela soma do TF-IDF, pegando as 4 melhores (mantendo ordem natural).

5) Entidades (spaCy)

Extrai entidades nomeadas, deduplica e retorna:

Top entidades com contagem

Entidades agrupadas por tipo (PER, ORG, LOC, DATE, etc.)

6) Métricas

Total de palavras

Total de frases

Tempo de leitura estimado: palavras / 200 (aprox. 200 palavras/min)

🧩 Colunas do dataset final
Coluna	Descrição
URL	URL processada
Título	og:title ou <title>
Descrição	og:description ou meta description
Texto Completo	Conteúdo consolidado
Resumo	Top frases por relevância (TF-IDF)
Palavras-chave	Features TF-IDF (uni + bi)
Temas	Seleção curta de unigrams/bigrams
Entidades (Top)	Entidades mais comuns com contagem
Entidades por Tipo	Dicionário string com tipos e exemplos
Top Palavras Frequentes	Palavras mais frequentes (sem stopwords)
Palavras	Quantidade total de palavras
Frases	Quantidade de frases (estimada)
Leitura (min)	Tempo estimado de leitura
⚠️ Limitações conhecidas

Páginas que carregam conteúdo via JavaScript podem retornar pouco texto (ex.: alguns sites com renderização client-side).

Sites com bloqueios/Cloudflare podem falhar no requests.

O modelo pt_core_news_sm é leve (bom para performance), mas tem menos precisão que modelos maiores.

✅ Dicas para melhorar sem “complexidade”

Mantendo simples e sem API/LLM, você pode adicionar:

st.cache_data para evitar reprocessar URLs repetidas

barra de progresso por URL

seleção de colunas para exportação (checkbox/multiselect)

log básico de erros por URL

🛠️ Solução de problemas
Erro: OSError: [E050] Can't find model 'pt_core_news_sm'

Instale o modelo:

python -m spacy download pt_core_news_sm
Excel mostra caracteres estranhos no CSV

O app usa utf-8-sig para o Excel BR. Se mesmo assim der problema, teste abrir via “Importar Dados” no Excel.

Algumas URLs retornam texto vazio

Pode ser:

Site com conteúdo carregado por JS

Bloqueio do servidor

HTML com conteúdo dentro de containers não capturados (pode incluir seletores extras)

📄 Licença

Este projeto é distribuído sob licença MIT (ajuste conforme necessário).