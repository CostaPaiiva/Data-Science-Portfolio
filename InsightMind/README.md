# InsightMind

Dashboard Streamlit para analise automatica de datasets CSV.

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-blue">
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-Dashboard-red">
  <img alt="Plotly" src="https://img.shields.io/badge/Plotly-Visuals-6f42c1">
  <img alt="Data Quality" src="https://img.shields.io/badge/Data%20Quality-Automated-success">
</p>

## At a glance

| Signal | Value |
|---|---|
| Focus | Automatic CSV profiling and insights |
| Main stack | Streamlit, Plotly, Python |
| Output | Quality metrics, charts, and reports |
| Strength | Quick data diagnosis before analysis |

## Funcionalidades

- Upload de CSV com leitura inteligente.
- Preview do dataset.
- Metricas de qualidade.
- Resumo estatistico por coluna.
- Graficos com Plotly.
- Diagnostico automatico com recomendacoes.
- Pipeline de limpeza.
- Download do CSV tratado.
- Relatorio HTML e PDF.

## Estrutura

```text
InsightMind/
|-- app.py
|-- requirements.txt
|-- runtime.txt
|-- core/
|   |-- cleaning.py
|   |-- insights.py
|   |-- loader.py
|   |-- profiler.py
|   |-- report.py
|   `-- visuals.py
`-- README.md
```

## Instalacao

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

No Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

## Como rodar

```bash
python -m streamlit run app.py
```

## Como usar

1. Envie um arquivo CSV.
2. Revise o preview e as metricas.
3. Gere graficos somente quando precisar.
4. Aplique limpeza se necessario.
5. Exporte CSV tratado ou relatorio.

## Observacoes

- Graficos e relatorios podem ser pesados em datasets grandes.
- Para exportar imagens Plotly/PDF, `kaleido` precisa estar instalado.
- Se o app ficar lento, reduza o preview e use amostras menores.
