import streamlit as st
from pyswip import Prolog
import os
import random

# Configuração da Página
st.set_page_config(page_title="CineAvaliador", layout="wide", page_icon="🎬")

# Estilização customizada para a logo e títulos
st.markdown("""
    <style>
    .main-title { font-size: 3rem; font-weight: bold; color: #FFFFFF; }
    .movie-card { background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 CineAvaliador")

def formatar_nome(nome):
    if not nome: return ""
    # Remove aspas simples que o Prolog pode retornar em strings e troca underscores
    return str(nome).replace("'", "").replace("_", " ").title()

@st.cache_resource
def iniciar_prolog():
    prolog = Prolog()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Ajuste o caminho conforme sua estrutura de pastas
    caminho = os.path.join(base_dir, "..", "backend", "regras.pl")
    caminho = os.path.abspath(caminho)
    prolog.consult(caminho)
    return prolog

prolog = iniciar_prolog()

# =========================
# SIDEBAR (FILTROS)
# =========================
st.sidebar.header("🎯 Filtros de Busca")

nota_min = st.sidebar.slider("Nota mínima", 0, 100, 70)

generos = [
    "qualquer", "acao", "aventura", "animacao", "comedia", "crime",
    "documentario", "drama", "fantasia", "familia", "ficcao_cientifica",
    "faroeste", "guerra", "historia", "misterio", "musica", "romance",
    "terror", "thriller", "cinema_tv"
]

genero_sel = st.sidebar.selectbox(
    "Gênero", generos, 
    format_func=lambda g: g.replace("_", " ").title()
)

duracao_opcoes = {"Qualquer": "qualquer", "Curto (≤ 90min)": "curto", "Longo (> 90min)": "longo"}
duracao_sel = st.sidebar.selectbox("Duração", list(duracao_opcoes.keys()))

ano_opcoes = {"Qualquer": "qualquer", "Recente (≥ 2016)": "recente", "Antigo (< 2016)": "antigo"}
ano_sel = st.sidebar.selectbox("Época", list(ano_opcoes.keys()))

# Preparação das variáveis para a Query
gen_p = genero_sel
dur_p = duracao_opcoes[duracao_sel]
ano_p = ano_opcoes[ano_sel]

# =========================
# CONSULTA UNIFICADA (RESOLVE O NESTEDQUERYERROR)
# =========================
# Buscamos o filme e seus atributos básicos em uma única prova lógica
query_string = f"recomendar_filme(X, {nota_min}, {gen_p}, {dur_p}, {ano_p}), nota(X, N), ano(X, A), duracao(X, D)"

# O list() aqui é CRUCIAL: ele exaure a query e libera o motor do Prolog
resultados = list(prolog.query(query_string))

# =========================
# EXIBIÇÃO
# =========================
st.write(f"### 🎯 {len(resultados)} filmes encontrados")

if resultados:
    # Seção de Sorteio
    if st.button("🎲 Sortear Filme do Dia"):
        sorteado = random.choice(resultados)
        nome_s = formatar_nome(sorteado['X'])
        st.balloons()
        st.success(f"### 🎬 Sugestão: {nome_s}")
        st.info(f"⭐ Nota: {sorteado['N']} | 📅 Ano: {sorteado['A']} | ⏱️ {sorteado['D']} min")
    
    st.divider()

    # Listagem de filmes (Iterando sobre a lista estática, sem novas queries de atributos)
    for r in resultados:
        nome_f = r["X"]
        
        # Como um filme pode ter múltiplos gêneros, fazemos uma query rápida aqui.
        # list() garante que ela feche antes da próxima iteração do loop.
        info_gen = list(prolog.query(f"genero({nome_f}, G)"))
        lista_generos = [formatar_nome(g["G"]) for g in info_gen]

        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(formatar_nome(nome_f))
                st.caption(f"🎭 {', '.join(lista_generos)}")
            with col2:
                st.write(f"⭐ **{r['N']}**")
                st.write(f"📅 {r['A']}")
                st.write(f"⏱️ {r['D']} min")
            st.divider()
else:
    st.warning("Nenhum filme corresponde aos filtros selecionados. Tente baixar a nota mínima!")