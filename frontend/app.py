import streamlit as st
from pyswip import Prolog
import os
import random

st.set_page_config(page_title="Avaliador de Filmes", layout="wide")

st.title("🎬 CineAvaliador")

def formatar_nome(nome):
    return nome.replace("_", " ").title()

@st.cache_resource
def iniciar_prolog():
    prolog = Prolog()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    caminho = os.path.join(base_dir, "..", "backend", "regras.pl")
    caminho = os.path.abspath(caminho)

    prolog.consult(caminho)
    
    return prolog

prolog = iniciar_prolog()

# =========================
# SIDEBAR (FILTROS ATUALIZADOS)
# =========================
st.sidebar.header("🎯 Filtros")

# Nota Mínima (numérico)
nota_min = st.sidebar.slider("Nota mínima", 0, 100, 0)

# Gênero (string ou 'qualquer')
generos = [
    "qualquer",
    "acao",
    "aventura",
    "animacao",
    "comedia",
    "crime",
    "documentario",
    "drama",
    "fantasia",
    "familia",
    "ficcao_cientifica",
    "faroeste",
    "guerra",
    "historia",
    "misterio",
    "musica",
    "romance",
    "terror",
    "thriller",
    "cinema_tv"
]

def formatar_genero(g):
    return g.replace("_", " ").title()

genero_sel = st.sidebar.selectbox(
    "Gênero",
    generos,
    format_func=formatar_genero
)

genero_prolog = genero_sel

# Duração (Categorizada conforme sua regra Prolog)
duracao_opcoes = {"Qualquer": "qualquer", "Curto (≤ 90min)": "curto", "Longo (> 90min)": "longo"}
duracao_sel = st.sidebar.selectbox("Duração", list(duracao_opcoes.keys()))
duracao_prolog = duracao_opcoes[duracao_sel]

# Ano (Categorizado conforme sua regra Prolog)
ano_opcoes = {"Qualquer": "qualquer", "Recente (≥ 2016)": "recente", "Antigo (< 2016)": "antigo"}
ano_sel = st.sidebar.selectbox("Época", list(ano_opcoes.keys()))
ano_prolog = ano_opcoes[ano_sel]

# =========================
# CONSULTA USANDO A REGRA recomendar_filme
# =========================
# Note que passamos os átomos do Prolog sem aspas se forem variáveis ou 'qualquer'
query = f"recomendar_filme(X, {nota_min}, {genero_prolog}, {duracao_prolog}, {ano_prolog})"

resultados = list(prolog.query(query))

# =========================
# EXIBIÇÃO DOS RESULTADOS
# =========================
st.write(f"🎯 {len(resultados)} filmes encontrados")

if resultados:
    if st.button("🎲 Sortear Filme"):
        sorteado = random.choice(resultados)
        nome = sorteado["X"]

        st.success(f"🎬 Filme sorteado: {formatar_nome(nome)}")

        # Buscar detalhes
        info_nota = list(prolog.query(f"nota({nome}, N)"))
        info_ano = list(prolog.query(f"ano({nome}, A)"))
        info_dur = list(prolog.query(f"duracao({nome}, D)"))
        info_gen = list(prolog.query(f"genero({nome}, G)"))

        st.subheader(formatar_nome(nome))

        generos = [formatar_nome(g["G"]) for g in info_gen]
        if generos:
            st.write("🎭 Gêneros:", ", ".join(generos))

        if info_nota: st.write(f"⭐ {info_nota[0]['N']}")
        if info_ano: st.write(f"📅 {info_ano[0]['A']}")
        if info_dur: st.write(f"⏱️ {info_dur[0]['D']} min")

        st.divider()
else:
    st.warning("Nenhum filme encontrado para os filtros selecionados.")

for r in resultados:
    nome = r["X"]
    
    # Buscamos os detalhes adicionais para exibição
    # (Prolog retorna o nome do átomo, ex: 'matrix')
    info_nota = list(prolog.query(f"nota({nome}, N)"))
    info_ano = list(prolog.query(f"ano({nome}, A)"))
    info_dur = list(prolog.query(f"duracao({nome}, D)"))
    info_gen = list(prolog.query(f"genero({nome}, G)"))

    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader(formatar_nome(nome))
        generos = [formatar_nome(g["G"]) for g in info_gen]
        if generos:
            st.write("🎭 Gêneros:", ", ".join(generos))

    with col2:
        if info_nota: st.write(f"⭐ {info_nota[0]['N']}")
        if info_ano: st.write(f"📅 {info_ano[0]['A']}")
        if info_dur: st.write(f"⏱️ {info_dur[0]['D']} min")

    st.divider()

