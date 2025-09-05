import streamlit as st

# Configuração da página
st.set_page_config(page_title="Comparador de Descontos", layout="centered")
st.title("💸 Comparador de Descontos")

# Entradas ajustáveis
apuro = st.number_input("💰 Apuro (€)", min_value=0.0, value=800.0, step=10.0)
desc_combustivel = st.number_input("⛽ Desconto Combustível (€)", min_value=0.0, value=200.0, step=1.0)

st.markdown("---")
st.subheader("Opções da Empresa")

# Opção 1
aluguer = st.number_input("🏠 Aluguer (€)", min_value=0.0, value=280.0, step=1.0)
perc_aluguer = st.number_input("👔 Empresa sobre Apuro (%)", min_value=0.0, value=7.0, step=0.5)

# Opção 2
seguro = st.number_input("🛡️ Seguro (€)", min_value=0.0, value=45.0, step=1.0)
perc_seguro = st.number_input("👔 Empresa sobre Apuro (%)", min_value=0.0, value=12.0, step=0.5)

st.markdown("---")

if st.button("Calcular 🔹"):
    st.subheader("📊 Resultados:")

    # Subtrair combustível do apuro
    apuro_liquido = apuro - desc_combustivel

    # Cálculo do que sobra em cada opção
    sobra_opcao1 = apuro_liquido - (apuro * perc_aluguer / 100) - aluguer
    sobra_opcao2 = apuro_liquido - (apuro * perc_seguro / 100) - seguro

    # Mostrar resultados
    st.markdown(f"💰 **Opção 1:** {perc_aluguer}% do apuro + {aluguer} € aluguer → **Sobra: {sobra_opcao1:.2f} €**")
    st.markdown(f"💰 **Opção
