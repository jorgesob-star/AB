import streamlit as st

# --- Configuração da página ---
st.set_page_config(page_title="Comparador de Descontos", layout="centered")
st.title("💸 Comparador mensal")

# --- Valores padrão ---
DEFAULTS = {
    'aluguer': 1200.0,
    'perc_aluguer': 7.0,
    'seguro': 180.0,
    'perc_seguro': 12.0,
    'manutencao': 200.0
}

# Inicializa o estado da sessão
if 'show_inputs' not in st.session_state:
    st.session_state.show_inputs = False
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- Entradas ---
st.header("Entradas do Usuário")
apuro = st.number_input("💰 Apuro total (€)", min_value=0.0, value=3333.0, step=10.0)
desc_combustivel = st.number_input("⛽ Desconto de Combustível (€)", min_value=0.0, value=900.0, step=1.0)
horas_trabalho = st.number_input("⏱️ Número de horas trabalhadas", min_value=1.0, value=240.0, step=1.0)
st.markdown("---")

# --- Opções ---
st.header("Opções da Empresa")
if st.button("Modificar Opções Padrão"):
    st.session_state.show_inputs = not st.session_state.show_inputs

if st.session_state.show_inputs:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Alugado")
        st.session_state.aluguer = st.number_input("🏠 Aluguer (€)", min_value=0.0, value=st.session_state.aluguer, step=1.0, key='input_aluguer')
        st.session_state.perc_aluguer = st.number_input("👔 Percentual (%)", min_value=0.0, max_value=100.0, value=st.session_state.perc_aluguer, step=0.5, key='input_perc_aluguer')
    with col2:
        st.subheader("Próprio")
        st.session_state.seguro = st.number_input("🛡️ Seguro (€)", min_value=0.0, value=st.session_state.seguro, step=1.0, key='input_seguro')
        st.session_state.perc_seguro = st.number_input("👔 Percentual (%)", min_value=0.0, max_value=100.0, value=st.session_state.perc_seguro, step=0.5, key='input_perc_seguro')
        st.session_state.manutencao = st.number_input("🛠️ Manutenção (€)", min_value=0.0, value=st.session_state.manutencao, step=1.0, key='input_manutencao')
else:
    st.info("Valores padrão das opções estão sendo usados. Clique no botão acima para modificá-los.")

st.markdown("---")

# --- Função para barras horizontais ---
def barra_horizontal(valor, label, cor, max_valor):
    proporcao = abs(valor) / max_valor if max_valor > 0 else 0
    proporcao = min(proporcao, 1.0)
    st.markdown(f"""
        <div style="display:flex; align-items:center; margin-bottom:5px;">
            <div style="width:150px;">{label}</div>
            <div style="flex:1; background-color:#e0e0e0; border-radius:5px;">
                <div style="width:{proporcao*100}%; background-color:{cor}; padding:5px 0; border-radius:5px;"></div>
            </div>
            <div style="width:80px; text-align:right;">{valor:,.2f} €</div>
        </div>
    """, unsafe_allow_html=True)

# --- Cálculo e Visualização ---
if st.button("Calcular 🔹", type="primary"):
    # Validações
    errors = []
    
    if horas_trabalho <= 0:
        errors.append("O número de horas trabalhadas deve ser maior que zero.")
    
    if desc_combustivel > apuro:
        errors.append("O desconto de combustível não pode ser maior que o apuro total.")
    
    if apuro < 0:
        errors.append("O apuro total não pode ser negativo.")
    
    if st.session_state.perc_aluguer < 0 or st.session_state.perc_aluguer > 100:
        errors.append("O percentual de aluguer deve estar entre 0 e 100%.")
    
    if st.session_state.perc_seguro < 0 or st.session_state.perc_seguro > 100:
        errors.append("O percentual de seguro deve estar entre 0 e 100%.")
    
    if st.session_state.aluguer < 0:
        errors.append("O valor do aluguer não pode ser negativo.")
    
    if st.session_state.seguro < 0:
        errors.append("O valor do seguro não pode ser negativo.")
    
    if st.session_state.manutencao < 0:
        errors.append("O valor da manutenção não pode ser negativo.")
    
    if errors:
        for error in errors:
            st.error(error)
        st.stop()
    
    # Preparar dados
    opcoes = {k: st.session_state[k] for k in ['aluguer', 'perc_aluguer', 'seguro', 'perc_seguro', 'manutencao']}

    # Cálculos
    deducao_empresa_opcao1 = apuro * opcoes['perc_aluguer'] / 100
    deducao_empresa_opcao2 = apuro * opcoes['perc_seguro'] / 100
    
    sobra_opcao1 = apuro - desc_combustivel - deducao_empresa_opcao1 - opcoes['aluguer']
    sobra_opcao2 = apuro - desc_combustivel - deducao_empresa_opcao2 - opcoes['seguro'] - opcoes['manutencao']

    # Verificar resultados negativos
    if sobra_opcao1 < 0 or sobra_opcao2 < 0:
        st.warning("Atenção: Uma ou ambas as opções resultam em valores negativos, indicando que as deduções excedem o apuro. Considere ajustar os valores de entrada.")
    
    ganho_hora_opcao1 = sobra_opcao1 / horas_trabalho
    ganho_hora_opcao2 = sobra_opcao2 / horas_trabalho

    st.subheader("📊 Resultados:")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Apuro Total", f"{apuro:,.2f} €")
    with col2:
        st.metric("Horas Trabalhadas", f"{horas_trabalho:,.0f} h")
    st.markdown("---")

    # Melhor opção
    if sobra_opcao1 > sobra_opcao2:
        melhor_idx = 0
    elif sobra_opcao2 > sobra_opcao1:
        melhor_idx = 1
    else:
        melhor_idx = -1  # empate

    # --- Abas ---
    tab1, tab2 = st.tabs(["📈 Dashboard", "🧮 Detalhes dos Cálculos"])
    
    with tab1:
        st.write("### Comparação Visual com Destaque")

        max_sobra = max(abs(sobra_opcao1), abs(sobra_opcao2), 1)
        max_ganho = max(abs(ganho_hora_opcao1), abs(ganho_hora_opcao2), 1)

        # Sobra (€)
        st.write("**Sobra (€)**")
        barra_horizontal(sobra_opcao1, f"Alugado {'🏆' if melhor_idx==0 else ''}", '#4caf50' if melhor_idx==0 else '#a5d6a7', max_sobra)
        barra_horizontal(sobra_opcao2, f"Próprio {'🏆' if melhor_idx==1 else ''}", '#2196f3' if melhor_idx==1 else '#90caf9', max_sobra)

        # Ganho/Hora
        st.write("**Ganho por Hora (€/h)**")
        barra_horizontal(ganho_hora_opcao1, f"Alugado {'🏆' if melhor_idx==0 else ''}", '#4caf50' if melhor_idx==0 else '#a5d6a7', max_ganho)
        barra_horizontal(ganho_hora_opcao2, f"Próprio {'🏆' if melhor_idx==1 else ''}", '#2196f3' if melhor_idx==1 else '#90caf9', max_ganho)

        # Mensagem complementar
        if melhor_idx == 0:
            st.success(f"🎉 Melhor escolha: **Alugado**, diferença de **{sobra_opcao1 - sobra_opcao2:,.2f} €**")
        elif melhor_idx == 1:
            st.success(f"🎉 Melhor escolha: **Próprio**, diferença de **{sobra_opcao2 - sobra_opcao1:,.2f} €**")
        else:
            st.info("As duas opções resultam no mesmo valor.")

    with tab2:
        st.write("### Detalhes dos Cálculos")
        
        st.write("**Opção 1 (Alugado):**")
        st.write(f"- Apuro Total: {apuro:,.2f} €")
        st.write(f"- Desconto de Combustível: {desc_combustivel:,.2f} €")
        st.write(f"- Dedução da Empresa: {apuro:,.2f} € × ({opcoes['perc_aluguer']}%) = {deducao_empresa_opcao1:,.2f} €")
        st.write(f"- Dedução de Aluguer: {opcoes['aluguer']:,.2f} €")
        st.write(f"- **Valor Final: {sobra_opcao1:,.2f} €**")
        st.write(f"- Ganho por Hora: {ganho_hora_opcao1:,.2f} €/h")
        
        st.write("")  # Linha em branco para espaçamento
        
        st.write("**Opção 2 (Próprio):**")
        st.write(f"- Apuro Total: {apuro:,.2f} €")
        st.write(f"- Desconto de Combustível: {desc_combustivel:,.2f} €")
        st.write(f"- Dedução da Empresa: {apuro:,.2f} € × ({opcoes['perc_seguro']}%) = {deducao_empresa_opcao2:,.2f} €")
        st.write(f"- Dedução de Seguro: {opcoes['seguro']:,.2f} €")
        st.write(f"- Dedução de Manutenção: {opcoes['manutencao']:,.2f} €")
        st.write(f"- **Valor Final: {sobra_opcao2:,.2f} €**")
        st.write(f"- Ganho por Hora: {ganho_hora_opcao2:,.2f} €/h")
