# WebSentix

Aplicacao FastAPI para analise de sentimento em portugues a partir de texto, URLs e arquivos.

## Funcionalidades

- Analise de texto manual.
- Analise de conteudo extraido de URL.
- Upload de arquivos `.txt`, `.pdf` e `.docx`.
- Classificacao em positivo, negativo ou neutro.
- Score de confianca e polaridade.
- Resumo extrativo.
- Extracao de palavras-chave.
- Historico local em JSON.
- Exportacao em PDF, TXT e Excel.
- Interface server-side com Jinja2.

## Estrutura

```text
WebSentix/
|-- app/
|   |-- config/
|   |-- models/
|   |-- routers/
|   |-- services/
|   |-- static/
|   |-- templates/
|   `-- utils/
|-- tests/
|-- data/
|-- requirements.txt
|-- Dockerfile
|-- run.py
`-- README.md
```

## Instalacao

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip
python -m pip install -r requirements.txt
copy .env.example .env
```

No Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
cp .env.example .env
```

## Como rodar

```bash
python run.py
```

Ou:

```bash
uvicorn app.main:app --reload
```

Acesse `http://127.0.0.1:8000`.

## Docker

```bash
docker build -t websentix .
docker run -p 8000:8000 websentix
```

## Testes

```bash
pytest -q
```

Observacao: os testes precisam das dependencias de `requirements.txt` instaladas. No ambiente atual, a coleta falhou por falta de `fastapi`, `pydantic-settings` e `yake`.

## Endpoints principais

| Metodo | Endpoint | Descricao |
| --- | --- | --- |
| GET | `/` | Interface principal |
| POST | `/api/analyze` | Analise via formulario |
| POST | `/api/analyze/json` | Analise com retorno JSON |
| GET | `/exports/latest/pdf` | Exporta o ultimo resultado em PDF |
| GET | `/exports/latest/txt` | Exporta o ultimo resultado em TXT |
| GET | `/exports/latest/excel` | Exporta o ultimo resultado em Excel |
| GET | `/exports/history/excel` | Exporta o historico em Excel |
| GET | `/health` | Healthcheck |

## Limitacoes

- Alguns sites podem bloquear scraping.
- PDFs escaneados em imagem exigem OCR, que nao esta incluido.
- O resumo e extrativo e heuristico.
- O modelo de sentimento e multilingue e pode precisar ajuste para dominios especificos.
