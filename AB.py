import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Comparador de Descontos", layout="centered")
st.title("💸 Comparador de Descontos")

# --- Definição dos valores padrão iniciais ---
DEFAULTS = {
    'aluguer': 280.0,
    'perc_aluguer': 7.0,
    'seguro': 45.0,
    'perc_seguro': 12.0,
    'manutencao': 50.0
}

# Inicializa o estado da sessão
if 'show_inputs' not in st.session_state:
    st.session_state.show_inputs = False

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- Entradas do Usuário ---
st.header("Entradas do Usuário")

apuro = st.number_input("💰 Apuro total (€)", min_value=0.0, value=700.0, step=10.0, help="O valor total bruto que você recebeu.")
desc_combustivel = st.number_input("⛽ Desconto de Combustível (€)", min_value=0.0, value=200.0, step=1.0, help="O valor que você gasta com combustível e que é deduzido do apuro.")
horas_trabalho = st.number_input("⏱️ Número de horas trabalhadas", min_value=1.0, value=40.0, step=1.0, help="Total de horas trabalhadas no período.")

st.markdown("---")

# --- Opções da Empresa ---
st.header("Opções da Empresa")

if st.button("Modificar Opções Padrão"):
    st.session_state.show_inputs = not st.session_state.show_inputs

if st.session_state.show_inputs:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Alugado")
        st.number_input("🏠 Aluguer (€)", min_value=0.0, value=st.session_state.aluguer, step=1.0, key='aluguer')
        st.number_input("👔 Percentual (%)", min_value=0.0, value=st.session_state.perc_aluguer, step=0.5, key='perc_aluguer')
    with col2:
        st.subheader("Próprio")
        st.number_input("🛡️ Seguro (€)", min_value=0.0, value=st.session_state.seguro, step=1.0, key='seguro')
        st.number_input("👔 Percentual (%)", min_value=0.0, value=st.session_state.perc_seguro, step=0.5, key='perc_seguro')
        st.number_input("🛠️ Manutenção (€)", min_value=0.0, value=st.session_state.manutencao, step=1.0, key='manutencao')
else:
    st.info("Valores padrão das
