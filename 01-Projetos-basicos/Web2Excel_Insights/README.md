# Web2Excel Insights

Aplicacao Streamlit para coletar conteudo de paginas web e exportar insights em CSV ou Excel.

## Funcionalidades

- Entrada de multiplas URLs.
- Download do HTML com `requests`.
- Limpeza de tags e blocos comuns de ruido.
- Extracao de texto principal.
- Metadados de titulo e descricao.
- Resumo heuristico com TF-IDF.
- Palavras-chave e temas.
- Entidades nomeadas com spaCy.
- Top palavras frequentes.
- Exportacao em CSV e Excel.

## Estrutura

```text
Web2Excel_Insights/
|-- app.py
|-- requirements.txt
|-- LICENSE
`-- README.md
```

## Instalacao

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip
python -m pip install -r requirements.txt
python -m spacy download pt_core_news_sm
```

No Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
python -m spacy download pt_core_news_sm
```

## Como rodar

```bash
python -m streamlit run app.py
```

## Limitacoes

- Paginas renderizadas por JavaScript podem retornar pouco texto.
- Sites com bloqueio ou Cloudflare podem falhar em `requests`.
- O modelo `pt_core_news_sm` e leve, mas menos preciso que modelos maiores.

## Solucao de problemas

- `Can't find model 'pt_core_news_sm'`: rode `python -m spacy download pt_core_news_sm`.
- CSV com caracteres estranhos no Excel: o app exporta com `utf-8-sig`; se necessario, use a opcao de importar dados do Excel.
