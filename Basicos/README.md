# Projetos Basicos

Esta pasta reune projetos de nivel basico para portfolio de Ciencia de Dados, Machine Learning, Visao Computacional, NLP e automacoes.

## Projetos incluidos

| Projeto | Tipo | Como rodar |
| --- | --- | --- |
| `FabricadeModelosML` | AutoML com Streamlit e PyCaret | `python -m streamlit run app.py` |
| `FastVision` | Visao computacional com YOLO, OpenCV e Streamlit | `python -m streamlit run app.py` |
| `InsightMind` | Dashboard automatico para analise de CSV | `python -m streamlit run app.py` |
| `Machine_Learning` | Notebooks de estudos e modelos classicos | Abrir os notebooks `.ipynb` |
| `Visao_computacional` | Area reservada para projetos de visao computacional | Ver README da pasta |
| `Web2Excel_Insights` | Coleta de paginas web e exportacao CSV/Excel | `python -m streamlit run app.py` |
| `WebSentix` | Analise de sentimento com FastAPI | `python run.py` |

## Verificacao feita

- Codigo Python compilado com `py_compile`, excluindo ambientes virtuais.
- Testes do WebSentix foram acionados, mas o ambiente atual nao tem as dependencias instaladas (`fastapi`, `pydantic-settings`, `yake`).

## Recomendacao geral

Crie um ambiente virtual por projeto e instale as dependencias pelo `requirements.txt` quando existir.
