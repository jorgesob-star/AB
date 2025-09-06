import streamlit as st
import matplotlib.pyplot as plt

# --- Configuração da página ---
st.set_page_config(page_title="Comparador de Descontos", layout="wide")
st.title("💸 Comparador de Descontos")

# --- Valores padrão ---
DEFAULTS = {
    'aluguer': 280.0,
    'perc_aluguer': 7.0,
    'seguro': 45.0,
    'perc_seguro': 12.0,
    'manutencao': 20.0
}

# Inicializa valores no estado da sessão
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- Entradas do usuário ---
with st.container():
    st.header("Entradas do Usuário")
    col1, col2 = st.columns([1,1])
    with col1:
        apuro = st.number_input("💰 Apuro total (€)", min_value=0.0, value=800.0, step=10.0, format="%.2f")
    with col2:
        desc_combustivel = st.number_input("⛽ Desconto de Combustível (€)", min_value=0.0, value=200.0, step=1.0, format="%.2f")

apuro_liquido = apuro - desc_combustivel
st.markdown(f"**Apuro Líquido:** {apuro_liquido:,.2f} €")
st.markdown("---")

# --- Opções da empresa ---
with st.expander("Modificar Opções Padrão"):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Opção 1")
        st.number_input("🏠 Aluguer (€)", min_value=0.0, value=st.session_state.aluguer, step=1.0, key='aluguer', format="%.2f")
        st.number_input("👔 Percentual (%)", min_value=0.0, value=st.session_state.perc_aluguer, step=0.1, key='perc_aluguer', format="%.2f")
    with col2:
        st.subheader("Opção 2")
        st.number_input("🛡️ Seguro (€)", min_value=0.0, value=st.session_state.seguro, step=1.0, key='seguro', format="%.2f")
        st.number_input("👔 Percentual (%)", min_value=0.0, value=st.session_state.perc_seguro, step=0.1, key='perc_seguro', format="%.2f")
        st.number_input("🛠️ Manutenção (€)", min_value=0.0, value=st.session_state.manutencao, step=1.0, key='manutencao', format="%.2f")

st.markdown("---")

# --- Função de cálculo ---
def calcular_sobra(apuro_liquido, percentual, fixo, manutencao=0):
    return apuro_liquido - (apuro_liquido * percentual / 100) - fixo - manutencao

# --- Botão de cálculo ---
if st.button("Calcular 🔹"):
    sobra_opcao1 = calcular_sobra(apuro_liquido, st.session_state.perc_aluguer, st.session_state.aluguer)
    sobra_opcao2 = calcular_sobra(apuro_liquido, st.session_state.perc_seguro, st.session_state.seguro, st.session_state.manutencao)

    # --- Resultados em cards lado a lado ---
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### 📈 Opção 1")
        st.metric("Sobra (€)", f"{sobra_opcao1:,.2f}")
        st.markdown(f"**Aluguer:** {st.session_state.aluguer:,.2f} €\n\n**Percentual:** {st.session_state.perc_aluguer}%")
    with col4:
        st.markdown("### 📈 Opção 2")
        st.metric("Sobra (€)", f"{sobra_opcao2:,.2f}")
        st.markdown(f"**Seguro:** {st.session_state.seguro:,.2f} €\n\n**Manutenção:** {st.session_state.manutencao:,.2f} €\n\n**Percentual:** {st.session_state.perc_seguro}%")

    # Mensagem de recomendação
    if sobra_opcao1 > sobra_opcao2:
        st.success(f"🎉 A **Opção 1** é a melhor escolha, com diferença de {(sobra_opcao1 - sobra_opcao2):,.2f} €.")
    elif sobra_opcao2 > sobra_opcao1:
        st.success(f"🎉 A **Opção 2** é a melhor escolha, com diferença de {(sobra_opcao2 - sobra_opcao1):,.2f} €.")
    else:
        st.info("As duas opções resultam no mesmo valor.")

    st.markdown("---")

    # --- Gráfico comparativo moderno ---
    st.markdown("### 📊 Comparação Visual")
    fig, ax = plt.subplots(figsize=(8, 4))
    opcoes = ['Opção 1', 'Opção 2']
    valores = [sobra_opcao1, sobra_opcao2]
    cores = ['#4CAF50' if sobra_opcao1 >= sobra_opcao2 else '#2196F3',
             '#4CAF50' if sobra_opcao2 > sobra_opcao1 else '#2196F3']

    bars = ax.bar(opcoes, valores, color=cores, edgecolor='black', width=0.5)
    ax.set_ylabel('€ Restantes')
    ax.set_title('Comparação entre Opções', fontsize=14, fontweight='bold')

    # Adiciona valores sobre as barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 5, f"{height:,.2f} €", ha='center', fontweight='bold')

    st.pyplot(fig)
