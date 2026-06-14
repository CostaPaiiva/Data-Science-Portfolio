# Fabrica de Modelos ML

Sistema Streamlit para treinar modelos de Machine Learning a partir de CSV usando PyCaret.

## O que faz

- Upload de CSV.
- Limpeza basica de dados.
- Sugestao automatica de target.
- Deteccao de classificacao ou regressao.
- Comparacao de modelos com PyCaret.
- Ranking dos melhores modelos.
- Validacao CV vs holdout.
- Relatorio PDF.
- Exportacao do pipeline treinado (`best_model_pipeline.pkl`).
- App separado para predicoes com `predict_app.py`.

## Estrutura

```text
FabricadeModelosML/
|-- app.py
|-- predict_app.py
|-- best_model_pipeline.pkl
|-- README.md
```

## Requisitos

- Python 3.9 ou 3.10 recomendado para compatibilidade com PyCaret.
- Pacotes principais: `streamlit`, `pandas`, `numpy`, `matplotlib`, `scikit-learn`, `pycaret`, `reportlab`, `shap`.

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

## Treinar modelos

```bash
python -m streamlit run app.py
```

Fluxo recomendado:

1. Envie um CSV.
2. Confirme ou ajuste o target.
3. Mantenha o Hard Mode ligado para maior robustez.
4. Clique em `Rodar AutoML agora`.
5. Baixe o PDF e o modelo `best_model_pipeline.pkl`.

## Rodar predicoes

Depois de gerar ou informar um modelo `.pkl`:

```bash
python -m streamlit run predict_app.py
```

O app aceita um CSV novo e gera um arquivo `predicoes.csv`.

## Observacoes

- O CSV de predicao precisa ter colunas compativeis com as usadas no treino.
- Alguns modelos ou versoes do PyCaret podem nao expor probabilidades por classe.
- Se o treino falhar em algum modelo especifico, mantenha `errors="ignore"` pelo Hard Mode e revise colunas com muitos nulos ou alta cardinalidade.
