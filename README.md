# Web2Excel Insights

Um sistema em Python com Streamlit que coleta textos de várias páginas web, extrai palavras-chave e entidades, e exporta automaticamente os insights para Excel.

---

## 🚀 Funcionalidades
- Interface simples via **Streamlit**.
- Entrada de múltiplas URLs (uma por linha).
- Coleta automática de textos das páginas.
- Extração de:
  - **Palavras-chave** (TF-IDF).
  - **Entidades nomeadas** (pessoas, locais, organizações).
- Exportação dos resultados para **Excel**.

---

## 🛠️ Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/web2excel-insights.git
cd web2excel-insights
pip install -r requirements.txt
Baixe o modelo de linguagem do spaCy para português:

bash
python -m spacy download pt_core_news_sm
▶️ Uso
Execute o sistema com:

bash
streamlit run app.py
Depois:

Abra o link gerado pelo Streamlit no navegador.

Cole as URLs (uma por linha).

Clique em Coletar Insights.

O sistema mostrará os resultados e salvará em insights.xlsx.

📂 Estrutura do Projeto:

Código
web2excel-insights/
│── app.py              # Código principal do sistema

│── requirements.txt    # Dependências

│── README.md           # Documentação

│── insights.xlsx       # Arquivo gerado (após execução)

📊 Exemplo de Saída

URL	Texto Original (trecho)	Palavras-chave	Entidades

https://exemplo.com	"Texto da página..."	economia, mercado, dados	Brasil, João, Microsoft
📜 Licença
Este projeto está sob a licença MIT.
Sinta-se livre para usar, modificar e compartilhar.