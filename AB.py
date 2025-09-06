import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# --- Configuração da página ---
st.set_page_config(page_title="Comparador de Descontos", layout="wide")
st.title("💸 Comparador de Descontos - Dashboard Interativo com Histórico")

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

if "historico" not in st.session_state:
    st.session_state.historico = []  # lista para guardar simulações

# --- Entradas do usuário ---
with st.container():
    st.header("⚙️ Entradas do Usuário")
    col1, col2 = st.columns([1,1])
    with col1:
        apuro = st.number_input("💰 Apuro total (€)", min_value=0.0, value=800.0, step=10.0, format="%.2f")
    with col2:
        desc_combustivel = st.number_input("⛽ Desconto de Combustível (€)", min_value=0.0, value=200.0, step=1.0, format="%.2f")

apuro_liquido = apuro - desc_combustivel
st.info(f"📌 **Apuro Líquido:** {apuro_liquido:,.2f} €")
st.markdown("---")

# --- Opções da empresa ---
with st.expander("⚖️ Modificar Opções Padrão"):
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

# --- Cálculo automático ---
sobra_opcao1 = calcular_sobra(apuro_liquido, st.session_state.perc_aluguer, st.session_state.aluguer)
sobra_opcao2 = calcular_sobra(apuro_liquido, st.session_state.perc_seguro, st.session_state.seguro, st.session_state.manutencao)

# Determinar vencedor
if sobra_opcao1 > sobra_opcao2:
    vencedor = "Opção 1"
    cor1, cor2 = "#4CAF50", "#D3D3D3"
elif sobra_opcao2 > sobra_opcao1:
    vencedor = "Opção 2"
    cor1, cor2 = "#D3D3D3", "#4CAF50"
else:
    vencedor = "Empate"
    cor1, cor2 = "#2196F3", "#2196F3"

# --- Resultados atuais ---
st.header("📊 Resultados Comparativos")
col3, col4 = st.columns(2)

with col3:
    st.markdown(
        f"""
        <div style="background-color:{cor1}; padding:20px; border-radius:15px; text-align:center; color:white;">
            <h2>🏠 Opção 1</h2>
            <h3>{sobra_opcao1:,.2f} €</h3>
            <p>Aluguer: {st.session_state.aluguer:,.2f} €</p>
            <p>Percentual: {st.session_state.perc_aluguer}%</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div style="background-color:{cor2}; padding:20px; border-radius:15px; text-align:center; color:white;">
            <h2>🛡️ Opção 2</h2>
            <h3>{sobra_opcao2:,.2f} €</h3>
            <p>Seguro: {st.session_state.seguro:,.2f} €</p>
            <p>Manutenção: {st.session_state.manutencao:,.2f} €</p>
            <p>Percentual: {st.session_state.perc_seguro}%</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if vencedor == "Empate":
    st.info("⚖️ As duas opções resultam no mesmo valor.")
else:
    st.success(f"🎉 A **{vencedor}** é a melhor escolha!")

# --- Gráfico comparativo ---
st.header("📊 Comparação Visual")
fig, ax = plt.subplots(figsize=(8, 4))
opcoes = ['Opção 1', 'Opção 2']
valores = [sobra_opcao1, sobra_opcao2]
cores = [cor1, cor2]

bars = ax.bar(opcoes, valores, color=cores, edgecolor='black', width=0.5)
ax.set_ylabel('€ Restantes')
ax.set_title('Comparação entre Opções', fontsize=14, fontweight='bold')

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 5, f"{height:,.2f} €", ha='center', fontweight='bold')

st.pyplot(fig)

st.markdown("---")

# --- Histórico de simulações ---
st.header("📝 Histórico de Simulações")

if st.button("💾 Salvar Simulação no Histórico"):
    st.session_state.historico.append({
        "Apuro Líquido (€)": apuro_liquido,
        "Opção 1 (€)": sobra_opcao1,
        "Opção 2 (€)": sobra_opcao2,
        "Melhor Escolha": vencedor
    })
    st.success("Simulação salva com sucesso!")

if st.session_state.historico:
    df_hist = pd.DataFrame(st.session_state.historico)
    st.dataframe(df_hist, use_container_width=True)

    # Gráfico histórico
    st.markdown("### 📈 Evolução das Simulações")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(df_hist.index, df_hist["Opção 1 (€)"], marker="o", label="Opção 1")
    ax2.plot(df_hist.index, df_hist["Opção 2 (€)"], marker="o", label="Opção 2")
    ax2.set_title("Histórico de Sobra (€)")
    ax2.set_xlabel("Simulação")
    ax2.set_ylabel("€ Restantes")
    ax2.legend()
    st.pyplot(fig2)
