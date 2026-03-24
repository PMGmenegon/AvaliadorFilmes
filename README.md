🎬 Avaliador de Filmes
📌 Descrição

O projeto Avaliador de Filmes tem como objetivo coletar dados de filmes a partir de páginas web e utilizá-los em um sistema lógico baseado em Prolog, permitindo consultas e recomendações de filmes com base em critérios como gênero, nota, duração e ano de lançamento.

🎯 Objetivo

Realizar web scraping para coletar dados de filmes

Armazenar os dados em formato JSON

Converter os dados em fatos lógicos (Prolog)

Permitir consultas inteligentes sobre os filmes

Criar uma interface simples utilizando Streamlit

🛠️ Tecnologias utilizadas

Python

BeautifulSoup

Requests

Streamlit

JSON

Prolog

📂 Estrutura do projeto
AvaliadorFilmes/
├── backend/
│ ├── PegaFilmes.py
│ ├── ConversorProlog.py
│ ├── filmes.json
│ └── filmes.pl
├── frontend/
│ └── app.py
├── requirements.txt
└── README.md

⚙️ Como executar o projeto

1. Clonar o repositório
   git clone <url-do-repositorio>
   cd AvaliadorFilmes

2. Criar ambiente virtual (opcional, recomendado)
   python -m venv venv

Ativar:

👉 Windows:
venv\Scripts\activate

👉 Linux/Mac:
source venv/bin/activate

3. Instalar dependências
   pip install -r requirements.txt

4. Instalar o SWI-Prolog (obrigatório)
   https://www.swi-prolog.org/

5. Executar o frontend (Streamlit)
   streamlit run frontend/app.py

📦 Dados do projeto

Os arquivos `filmes.json` e `filmes.pl` já estão incluídos no diretório `backend`, portanto não é necessário executar o scraping nem a conversão para Prolog.

📊 Dados coletados

O sistema coleta as seguintes informações dos filmes:

🎬 Título

⭐ Nota

⏱️ Duração

📅 Ano de lançamento

🎭 Gêneros

🧠 Integração com Prolog

Os dados coletados são convertidos em fatos lógicos, como:

filme(zootopia_2).
genero(zootopia_2, animacao).
nota(zootopia_2, 76).
duracao(zootopia_2, 108).
ano(zootopia_2, 2025).

Esses fatos permitem consultas como:

Filmes por gênero

Filmes com nota acima de X

Filmes lançados em determinado ano

🚀 Funcionalidades

Coleta automatizada de filmes

Armazenamento estruturado em JSON

Conversão para base lógica

Interface interativa com Streamlit

⚠️ Observações

O scraping depende da estrutura do site, podendo sofrer alterações

Algumas informações podem não estar disponíveis para todos os filmes
