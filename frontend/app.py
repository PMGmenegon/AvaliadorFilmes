import streamlit as st
from pyswip import Prolog
import os

st.set_page_config(page_title="Avaliador de Filmes", layout="wide")

st.title("🎬 Avaliador de Filmes (Prolog)")

# =========================
# FUNÇÃO PRA FORMATAR NOME
# =========================
def formatar_nome(nome):
    return nome.replace("_", " ").title()

# =========================
# INICIAR PROLOG (CACHE)
# =========================
@st.cache_resource
def iniciar_prolog():
    prolog = Prolog()
    caminho = os.path.abspath("backend/filmes.pl")
    prolog.consult(caminho)
    return prolog

prolog = iniciar_prolog()

# =========================
# SIDEBAR (FILTROS)
# =========================
st.sidebar.header("🎯 Filtros")

nota_min = st.sidebar.slider("Nota mínima", 0, 100, 0)

ano_min, ano_max = st.sidebar.slider(
    "Ano",
    1900,
    2030,
    (2000, 2025)
)

duracao_min, duracao_max = st.sidebar.slider(
    "Duração (min)",
    0,
    300,
    (0, 300)
)

genero = st.sidebar.text_input("Gênero (ex: acao, comedia)")

# =========================
# CONSULTA BASE
# =========================
query = f"""
filme(X),
nota(X, N),
ano(X, A),
duracao(X, D),
N >= {nota_min},
A >= {ano_min},
A =< {ano_max},
D >= {duracao_min},
D =< {duracao_max}
"""

resultados = list(prolog.query(query))

# =========================
# PRÉ-CARREGAR DADOS (EVITA TRAVAR)
# =========================
dados_filmes = {}

for r in resultados:
    nome = r["X"]

    # pega tudo uma vez só
    generos_q = list(prolog.query(f"genero({nome}, G)"))
    nota_q = list(prolog.query(f"nota({nome}, N)"))
    ano_q = list(prolog.query(f"ano({nome}, A)"))
    duracao_q = list(prolog.query(f"duracao({nome}, D)"))

    dados_filmes[nome] = {
        "generos": [g["G"] for g in generos_q],
        "nota": nota_q[0]["N"] if nota_q else None,
        "ano": ano_q[0]["A"] if ano_q else None,
        "duracao": duracao_q[0]["D"] if duracao_q else None
    }

# =========================
# FILTRO DE GÊNERO
# =========================
filmes_filtrados = []

for nome, dados in dados_filmes.items():
    if genero:
        if genero.lower() not in dados["generos"]:
            continue

    filmes_filtrados.append(nome)

# =========================
# RESULTADOS
# =========================
st.write(f"🎯 {len(filmes_filtrados)} filmes encontrados")

# =========================
# EXIBIÇÃO
# =========================
for nome in filmes_filtrados:
    dados = dados_filmes[nome]

    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader(formatar_nome(nome))

        lista_generos = [formatar_nome(g) for g in dados["generos"]]

        if lista_generos:
            st.write("🎭 Gêneros:", ", ".join(lista_generos))

    with col2:
        if dados["nota"]:
            st.write(f"⭐ {dados['nota']}")
        if dados["ano"]:
            st.write(f"📅 {dados['ano']}")
        if dados["duracao"]:
            st.write(f"⏱️ {dados['duracao']} min")

    st.divider()