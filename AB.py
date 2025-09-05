import streamlit as st

# Configuração da página
st.set_page_config(page_title="Comparador de Descontos", layout="centered")
st.title("💸 Comparador de Descontos")

# --- Entradas ajustáveis ---
st.header("Entradas do Usuário")

apuro = st.number_input("💰 Apuro total (€)", min_value=0.0, value=800.0, step=10.0, help="O valor total bruto que você recebeu.")
desc_combustivel = st.number_input("⛽ Desconto de Combustível (€)", min_value=0.0, value=200.0, step=1.0, help="O valor que você gasta com combustível e que é deduzido do apuro.")

st.markdown("---")

# --- Opções da Empresa ---
st.header("Opções da Empresa")

# Colunas para organizar as opções lado a lado
col1, col2 = st.columns(2)

with col1:
    st.subheader("Opção 1")
    aluguer = st.number_input("🏠 Aluguer (€)", min_value=0.0, value=280.0, step=1.0)
    perc_aluguer = st.number_input("👔 Percentual sobre o Apuro (%)", min_value=0.0, value=7.0, step=0.5)

with col2:
    st.subheader("Opção 2")
    seguro = st.number_input("🛡️ Seguro (€)", min_value=0.0, value=45.0, step=1.0)
    perc_seguro = st.number_input("👔 Percentual sobre o Apuro (%)", min_value=0.0, value=12.0, step=0.5)

st.markdown("---")

# --- Lógica e Exibição dos Resultados ---
if st.button("Calcular 🔹"):
    st.subheader("📊 Resultados:")

    # Subtrair combustível do apuro para obter o valor líquido
    apuro_liquido = apuro - desc_combustivel

    # Cálculo do que sobra em cada opção
    sobra_opcao1 = apuro_liquido - (apuro * perc_aluguer / 100) - aluguer
    sobra_opcao2 = apuro_liquido - (apuro * perc_seguro / 100) - seguro
    
    st.markdown(f"**Apuro Líquido:** {apuro_liquido:,.2f} € (apuro total - combustível)")
    st.markdown("---")

    # Exibir resultados detalhados
    st.markdown("### Visão Geral")
    st.write(f"Na **Opção 1**, o valor final que sobra é: **{sobra_opcao1:,.2f} €**")
    st.write(f"Na **Opção 2**, o valor final que sobra é: **{sobra_opcao2:,.2f} €**")
    
    # Determinar e exibir a melhor opção
    if sobra_opcao1 > sobra_opcao2:
        st.success(f"🎉 A **Opção 1** é a melhor escolha, com uma diferença de **{(sobra_opcao1 - sobra_opcao2):,.2f} €**.")
    elif sobra_opcao2 > sobra_opcao1:
        st.success(f"🎉 A **Opção 2** é a melhor escolha, com uma diferença de **{(sobra_opcao2 - sobra_opcao1):,.2f} €**.")
    else:
        st.info("As duas opções resultam no mesmo valor.")
        
    st.markdown("---")
    
    # Detalhe dos cálculos
    st.markdown("### Detalhes dos Cálculos")
    st.markdown(f"""
    **Cálculo da Opção 1:**
    * Apuro Líquido: {apuro_liquido:,.2f} €
    * Dedução da Empresa: {apuro:,.2f} € * ({perc_aluguer} / 100) = **{(apuro * perc_aluguer / 100):,.2f} €**
    * Dedução de Aluguer: **{aluguer:,.2f} €**
    * **Valor Final:** {apuro_liquido:,.2f} - {(apuro * perc_aluguer / 100):,.2f} - {aluguer:,.2f} = **{sobra_opcao1:,.2f} €**
    """)
    
    st.markdown(f"""
    **Cálculo da Opção 2:**
    * Apuro Líquido: {apuro_liquido:,.2f} €
    * Dedução da Empresa: {apuro:,.2f} € * ({perc_seguro} / 100) = **{(apuro * perc_seguro / 100):,.2f} €**
    * Dedução de Seguro: **{seguro:,.2f} €**
    * **Valor Final:** {apuro_liquido:,.2f} - {(apuro * perc_seguro / 100):,.2f} - {seguro:,.2f} = **{sobra_opcao2:,.2f} €**
    """)
