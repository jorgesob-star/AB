import streamlit as st

# Configuração da página
st.set_page_config(page_title="Comparador de Descontos", layout="centered")
st.title("💸 Comparador de Descontos")

# --- Entradas do Usuário ---
st.header("Entradas do Usuário")

apuro = st.number_input("💰 Apuro total (€)", min_value=0.0, value=800.0, step=10.0, help="O valor total bruto que você recebeu.")
desc_combustivel = st.number_input("⛽ Desconto de Combustível (€)", min_value=0.0, value=200.0, step=1.0, help="O valor que você gasta com combustível e que é deduzido do apuro.")

st.markdown("---")

# --- Lógica para mostrar as opções ---
st.header("Opções da Empresa")

# Define os valores padrão para as opções
aluguer_padrao = 280.0
perc_aluguer_padrao = 7.0
seguro_padrao = 45.0
perc_seguro_padrao = 12.0

# Inicializa o estado de exibição se ainda não existir
if 'show_inputs' not in st.session_state:
    st.session_state.show_inputs = False

# Botão para alternar a visibilidade dos campos de entrada
if st.button("Modificar Opções Padrão"):
    st.session_state.show_inputs = not st.session_state.show_inputs

if st.session_state.show_inputs:
    # Colunas para organizar as opções lado a lado, apenas quando os inputs estão visíveis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Opção 1")
        # Chaves são usadas para armazenar os valores no session_state
        aluguer = st.number_input("🏠 Aluguer (€)", min_value=0.0, value=aluguer_padrao, step=1.0, key='aluguer_input')
        perc_aluguer = st.number_input("👔 Percentual sobre o Apuro (%)", min_value=0.0, value=perc_aluguer_padrao, step=0.5, key='perc_aluguer_input')

    with col2:
        st.subheader("Opção 2")
        seguro = st.number_input("🛡️ Seguro (€)", min_value=0.0, value=seguro_padrao, step=1.0, key='seguro_input')
        perc_seguro = st.number_input("👔 Percentual sobre o Apuro (%)", min_value=0.0, value=perc_seguro_padrao, step=0.5, key='perc_seguro_input')

else:
    # Usa os valores padrão se os inputs não estiverem visíveis
    aluguer = aluguer_padrao
    perc_aluguer = perc_aluguer_padrao
    seguro = seguro_padrao
    perc_seguro = perc_seguro_padrao
    st.info("Valores padrão das opções estão sendo usados. Clique no botão acima para modificá-los.")

st.markdown("---")

# Botão para iniciar o cálculo
if st.button("Calcular 🔹", type="primary"):
    # Subtrair combustível do apuro para obter o valor líquido
    apuro_liquido = apuro - desc_combustivel

    # Pega os valores atuais (padrão ou modificados)
    aluguer_atual = st.session_state.get('aluguer_input', aluguer_padrao)
    perc_aluguer_atual = st.session_state.get('perc_aluguer_input', perc_aluguer_padrao)
    seguro_atual = st.session_state.get('seguro_input', seguro_padrao)
    perc_seguro_atual = st.session_state.get('perc_seguro_input', perc_seguro_padrao)

    # Cálculo do que sobra em cada opção
    sobra_opcao1 = apuro_liquido - (apuro * perc_aluguer_atual / 100) - aluguer_atual
    sobra_opcao2 = apuro_liquido - (apuro * perc_seguro_atual / 100) - seguro_atual
    
    st.subheader("📊 Resultados:")
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
    * Dedução da Empresa: {apuro:,.2f} € * ({perc_aluguer_atual} / 100) = **{(apuro * perc_aluguer_atual / 100):,.2f} €**
    * Dedução de Aluguer: **{aluguer_atual:,.2f} €**
    * **Valor Final:** {apuro_liquido:,.2f} - {(apuro * perc_aluguer_atual / 100):,.2f} - {aluguer_atual:,.2f} = **{sobra_opcao1:,.2f} €**
    """)
    
    st.markdown(f"""
    **Cálculo da Opção 2:**
    * Apuro Líquido: {apuro_liquido:,.2f} €
    * Dedução da Empresa: {apuro:,.2f} € * ({perc_seguro_atual} / 100) = **{(apuro * perc_seguro_atual / 100):,.2f} €**
    * Dedução de Seguro: **{seguro_atual:,.2f} €**
    * **Valor Final:** {apuro_liquido:,.2f} - {(apuro * perc_seguro_atual / 100):,.2f} - {seguro_atual:,.2f} = **{sobra_opcao2:,.2f} €**
    """)
