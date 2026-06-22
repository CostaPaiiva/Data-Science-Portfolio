# FastVision

Aplicacao Streamlit para visao computacional local com YOLO e reconhecimento facial com OpenCV.

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-blue">
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-App-red">
  <img alt="OpenCV" src="https://img.shields.io/badge/OpenCV-Vision-orange">
  <img alt="YOLO" src="https://img.shields.io/badge/YOLO-Object%20Detection-success">
</p>

## At a glance

| Signal | Value |
|---|---|
| Focus | Local computer vision and face recognition |
| Main stack | Streamlit, YOLO, OpenCV, SQLite |
| Output | Real-time detection and export tools |
| Strength | Practical CV app with an end-user interface |

## Funcionalidades

- Deteccao de objetos com YOLO/Ultralytics.
- Cadastro de pessoas e imagens em SQLite.
- Deteccao de faces com Haar Cascade.
- Treinamento de reconhecedor facial LBPH (`opencv-contrib-python`).
- Reconhecimento por nome em webcam ou RTSP.
- Exportacao de registros em CSV ou JSON.
- Opcao de gravar video anotado.

## Estrutura

```text
FastVision/
|-- app.py
|-- db.py
|-- exporters.py
|-- face_recog.py
|-- yolo_backend.py
|-- requirements.txt
|-- assets/
|   `-- haarcascade_frontalface_default.xml
|-- yolo11n.pt
|-- yolo11s.pt
`-- README.md
```

## Requisitos

- Python 3.10+.
- Webcam ou URL RTSP opcional.
- Pesos YOLO presentes na pasta (`yolo11n.pt` ou `yolo11s.pt`).
- Haar Cascade em `assets/haarcascade_frontalface_default.xml`.

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

Use apenas `opencv-contrib-python`, porque o LBPH depende de `cv2.face`.

## Como rodar

```bash
python -m streamlit run app.py
```

Acesse o endereco informado pelo Streamlit, normalmente `http://localhost:8501`.

## Fluxo de uso

1. Abra a aba de cadastro.
2. Cadastre uma pessoa e envie imagens com rosto visivel.
3. Treine ou atualize o modelo de reconhecimento.
4. Abra a aba Live.
5. Escolha webcam ou RTSP.
6. Ajuste confianca, IoU e tamanho de imagem.
7. Inicie a captura e exporte CSV/JSON se necessario.

## Solucao de problemas

- `ModuleNotFoundError: ultralytics`: instale as dependencias no mesmo ambiente em que roda o Streamlit.
- `cv2.face nao existe`: remova `opencv-python` e instale `opencv-contrib-python`.
- Haar Cascade nao encontrado: confirme o arquivo XML em `assets/`.
- Baixa performance em CPU: use `yolo11n.pt` e `imgsz` 416 ou 480.
