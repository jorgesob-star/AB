import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Comparador de Descontos", layout="centered")
st.title("💸 Comparador de Descontos")

# --- Valores padrão ---
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

# --- Entradas ---
st.header("Entradas do Usuário")
apuro = st.number_input("💰 Apuro total (€)", min_value=0.0, value=700.0, step=10.0)
desc_combustivel = st.number_input("⛽ Desconto de Combustível (€)", min_value=0.0, value=200.0, step=1.0)
horas_trabalho = st.number_input("⏱️ Número de horas trabalhadas", min_value=1.0, value=40.0, step=1.0)
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
    st.info("Valores padrão das opções estão sendo usados. Clique no botão acima para modificá-los.")
st.markdown("---")

# --- Cálculo ---
if st.button("Calcular 🔹", type="primary"):
    apuro_liquido = apuro - desc_combustivel
    aluguer_atual = st.session_state.aluguer
    perc_aluguer_atual = st.session_state.perc_aluguer
    seguro_atual = st.session_state.seguro
    perc_seguro_atual = st.session_state.perc_seguro
    manutencao_atual = st.session_state.manutencao

    sobra_opcao1 = apuro_liquido - (apuro * perc_aluguer_atual / 100) - aluguer_atual
    sobra_opcao2 = apuro_liquido - (apuro * perc_seguro_atual / 100) - seguro_atual - manutencao_atual
    ganho_hora_opcao1 = sobra_opcao1 / horas_trabalho
    ganho_hora_opcao2 = sobra_opcao2 / horas_trabalho

    st.subheader("📊 Resultados:")
    st.metric("Apuro Líquido", f"{apuro_liquido:,.2f} €")
    st.metric("Horas Trabalhadas", f"{horas_trabalho:,.0f} h")
    st.markdown("---")

    # --- Tabelas de resumo ---
    tab1, tab2 = st.tabs(["📈 Resumo", "🧮 Detalhes dos Cálculos"])
    with tab1:
        st.write("### Valores e Ganhos por Hora")
        df = pd.DataFrame({
            "Opção": ["Alugado", "Próprio"],
            "Sobra (€)": [sobra_opcao1, sobra_opcao2],
            "€/Hora": [ganho_hora_opcao1, ganho_hora_opcao2]
        })
        # Destacar a melhor opção por €/h
        melhor_idx = 0 if ganho_hora_opcao1 >= ganho_hora_opcao2 else 1
        cores = ["#FFD700" if i==melhor_idx else "#1f77b4" for i in range(2)]
        st.bar_chart(df[["Sobra (€)", "€/Hora"]], height=300)

        # Mostrar tabela com destaque
        st.dataframe(df.style.apply(lambda x: ["background-color: gold" if i==melhor_idx else "" for i in range(len(x))], axis=1))

        # Melhor escolha geral
        if sobra_opcao1 > sobra_opcao2:
            st.success(f"🎉 A **Opção 1 (Alugado)** é a melhor escolha, diferença de **{sobra_opcao1 - sobra_opcao2:,.2f} €**.")
        elif sobra_opcao2 > sobra_opcao1:
            st.success(f"🎉 A **Opção 2 (Próprio)** é a melhor escolha, diferença de **{sobra_opcao2 - sobra_opcao1:,.2f} €**.")
        else:
            st.info("As duas opções resultam no mesmo valor.")

    with tab2:
        st.write("### Detalhes dos cálculos")
        st.markdown(f"""
        **Opção 1 (Alugado):**
        - Apuro Líquido: {apuro_liquido:,.2f} €
        - Dedução da Empresa: {apuro:,.2f} € * ({perc_aluguer_atual}/100) = **{(apuro*perc_aluguer_atual/100):,.2f} €**
        - Dedução de Aluguer: **{aluguer_atual:,.2f} €**
        - Valor Final: {sobra_opcao1:,.2f} €
        - Ganho por Hora: {ganho_hora_opcao1:,.2f} €/h

        **Opção 2 (Próprio):**
        - Apuro Líquido: {apuro_liquido:,.2f} €
        - Dedução da Empresa: {apuro:,.2f} € * ({perc_seguro_atual}/100) = **{(apuro*perc_seguro_atual/100):,.2f} €**
        - Dedução de Seguro: **{seguro_atual:,.2f} €**
        - Dedução de Manutenção: **{manutencao_atual:,.2f} €**
        - Valor Final: {sobra_opcao2:,.2f} €
        - Ganho por Hora: {ganho_hora_opcao2:,.2f} €/h
        """)
