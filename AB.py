import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# --- Botão de cálculo ---
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

    # --- Abas ---
    tab1, tab2 = st.tabs(["📈 Resumo", "🧮 Detalhes dos Cálculos"])
    with tab1:
        col3, col4 = st.columns(2)
        with col3:
            st.metric(f"Sobra na Opção 1", f"{sobra_opcao1:,.2f} €")
            st.metric(f"Ganho/Hora Opção 1", f"{ganho_hora_opcao1:,.2f} €/h")
        with col4:
            st.metric(f"Sobra na Opção 2", f"{sobra_opcao2:,.2f} €")
            st.metric(f"Ganho/Hora Opção 2", f"{ganho_hora_opcao2:,.2f} €/h")

        # Gráfico
        categorias = ["Sobra (€)", "€/Hora"]
        valores_op1 = [sobra_opcao1, ganho_hora_opcao1]
        valores_op2 = [sobra_opcao2, ganho_hora_opcao2]
        x = range(len(categorias))
        largura = 0.35
        fig, ax = plt.subplots()
        bars1 = ax.bar([i - largura/2 for i in x], valores_op1, largura, label="Opção 1 - Aluguer", color="#4CAF50")
        bars2 = ax.bar([i + largura/2 for i in x], valores_op2, largura, label="Opção 2 - Próprio", color="#2196F3")
        ax.set_ylabel("Valores (€ e €/h)")
        ax.set_title("Comparação entre Opções")
        ax.set_xticks(x)
        ax.set_xticklabels(categorias)
        ax.legend()

        # Valores em cima das barras
        for idx, bar in enumerate(bars1):
            yval = bar.get_height()
            unidade = "€" if idx==0 else "€/h"
            ax.text(bar.get_x()+bar.get_width()/2, yval, f"{yval:,.2f} {unidade}", ha='center', va='bottom', fontsize=9, fontweight="bold")
        for idx, bar in enumerate(bars2):
            yval = bar.get_height()
            unidade = "€" if idx==0 else "€/h"
            ax.text(bar.get_x()+bar.get_width()/2, yval, f"{yval:,.2f} {unidade}", ha='center', va='bottom', fontsize=9, fontweight="bold")

        # Linhas referência
        ganho_medio = (ganho_hora_opcao1 + ganho_hora_opcao2)/2
        ganho_minimo = min(ganho_hora_opcao1, ganho_hora_opcao2)
        ganho_maximo = max(ganho_hora_opcao1, ganho_hora_opcao2)
        ax.axhline(ganho_medio, color="red", linestyle="--", linewidth=1)
        ax.text(len(categorias)-0.5, ganho_medio, f"Média: {ganho_medio:,.2f} €/h", color="red", va="bottom", ha="right", fontsize=9, fontweight="bold")
        ax.axhline(ganho_minimo, color="orange", linestyle="--", linewidth=1)
        ax.text(len(categorias)-0.5, ganho_minimo, f"Mínimo: {ganho_minimo:,.2f} €/h", color="orange", va="bottom", ha="right", fontsize=9, fontweight="bold")
        ax.axhline(ganho_maximo, color="green", linestyle="--", linewidth=1)
        ax.text(len(categorias)-0.5, ganho_maximo, f"Máx: {ganho_maximo:,.2f} €/h", color="green", va="bottom", ha="right", fontsize=9, fontweight="bold")

        # Destacar melhor opção €/h
        if ganho_hora_opcao1 > ganho_hora_opcao2:
            ax.plot(x[1]-largura/2, ganho_hora_opcao1, 'o', color="gold", markersize=12, markeredgecolor="black", label="Melhor €/h")
        elif ganho_hora_opcao2 > ganho_hora_opcao1:
            ax.plot(x[1]+largura/2, ganho_hora_opcao2, 'o', color="gold", markersize=12, markeredgecolor="black", label="Melhor €/h")
        else:
            # Se igual, marca as duas
            ax.plot([x[1]-largura/2, x[1]+largura/2], [ganho_hora_opcao1]*2, 'o', color="gold", markersize=12, markeredgecolor="black", label="Melhor €/h")

        st.pyplot(fig)

        # Melhor escolha geral
        if sobra_opcao1 > sobra_opcao2:
            st.success(f"🎉 A **Opção 1** é a melhor escolha, com diferença de **{sobra_opcao1 - sobra_opcao2:,.2f} €**.")
        elif sobra_opcao2 > sobra_opcao1:
            st.success(f"🎉 A **Opção 2** é a melhor escolha, com diferença de **{sobra_opcao2 - sobra_opcao1:,.2f} €**.")
        else:
            st.info("As duas opções resultam no mesmo valor.")

    with tab2:
        st.markdown(f"""
        **Opção 1:**
        - Apuro Líquido: {apuro_liquido:,.2f} €
        - Dedução da Empresa: {apuro:,.2f} € * ({perc_aluguer_atual}/100) = **{(apuro * perc_aluguer_atual / 100):,.2f} €**
        - Dedução de Aluguer: **{aluguer_atual:,.2f} €**
        - Valor Final: {sobra_opcao1:,.2f} €
        - Ganho por Hora: {ganho_hora_opcao1:,.2f} €/h

        **Opção 2:**
        - Apuro Líquido: {apuro_liquido:,.2f} €
        - Dedução da Empresa: {apuro:,.2f} € * ({perc_seguro_atual}/100) = **{(apuro * perc_seguro_atual / 100):,.2f} €**
        - Dedução de Seguro: **{seguro_atual:,.2f} €**
        - Dedução de Manutenção: **{manutencao_atual:,.2f} €**
        - Valor Final: {sobra_opcao2:,.2f} €
        - Ganho por Hora: {ganho_hora_opcao2:,.2f} €/h
        """)
