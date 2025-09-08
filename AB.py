import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
import plotly.express as px

# Configuração da página e do layout
# Define o título da página no navegador, o ícone e o layout da aplicação.
st.set_page_config(
    page_title="Gestor de Despesas Pessoais",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Funções de Gestão de Dados ---
# A função a seguir lida com a leitura e inicialização dos dados.
# Em um ambiente de produção (nuvem), você usaria um banco de dados persistente.
def carregar_dados():
    """
    Carrega os dados do arquivo JSON local.
    Se o arquivo não existir ou for inválido, inicializa a estrutura de dados padrão.
    """
    try:
        if os.path.exists("despesas.json"):
            with open("despesas.json", 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        st.error("Arquivo de dados corrompido ou não encontrado. Inicializando com dados padrão.")
    
    # Estrutura de dados inicial caso o arquivo não exista ou esteja corrompido
    return {
        "mensais": [
            {"nome": "Casa", "valor": 0.0, "icon": "🏠"},
            {"nome": "Água", "valor": 0.0, "icon": "💧"},
            {"nome": "Luz", "valor": 0.0, "icon": "💡"},
            {"nome": "Telemóveis", "valor": 0.0, "icon": "📱"},
            {"nome": "Atelier", "valor": 0.0, "icon": "🎨"},
            {"nome": "Feira", "valor": 0.0, "icon": "🛒"},
            {"nome": "Catarina", "valor": 0.0, "icon": "👩"},
            {"nome": "Ginásticas", "valor": 0.0, "icon": "🏃"},
            {"nome": "Segurança Social", "valor": 0.0, "icon": "🏛️"},
            {"nome": "Extras Mensais", "valor": 0.0, "icon": "➕"}
        ],
        "trimestrais": [
            {"nome": "Contabilista", "valor": 0.0, "icon": "📊"},
            {"nome": "Extras Trimestrais", "valor": 0.0, "icon": "➕"}
        ],
        "anuais": [
            {"nome": "Seguro", "valor": 0.0, "icon": "🛡️"},
            {"nome": "IUC", "valor": 0.0, "icon": "🚗"},
            {"nome": "Contabilista", "valor": 0.0, "icon": "📊"},
            {"nome": "Extras Anuais", "valor": 0.0, "icon": "➕"}
        ]
    }

def salvar_dados(dados):
    """Salva os dados no arquivo JSON com formatação."""
    with open("despesas.json", 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def calcular_totais(dados):
    """Calcula os totais de despesas por categoria e projeção anual."""
    totais = {
        "mensal": sum(item["valor"] for item in dados["mensais"]),
        "trimestral": sum(item["valor"] for item in dados["trimestrais"]),
        "anual": sum(item["valor"] for item in dados["anuais"])
    }
    
    totais["anual_projetado"] = (totais["mensal"] * 12) + (totais["trimestral"] * 4) + totais["anual"]
    totais["mensal_medio"] = totais["anual_projetado"] / 12
    
    return totais

# --- Execução Principal da Aplicação ---
# Carrega os dados na primeira execução
dados = carregar_dados()

# Título da aplicação principal
st.title("💰 Gestor de Despesas Pessoais")

# Barra lateral para navegação
st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Selecione a página:", 
                         ["📋 Visualizar Despesas", "✏️ Editar Despesas", "📊 Resumo Financeiro"])

# Renderiza a página selecionada
if pagina == "📋 Visualizar Despesas":
    st.header("📋 Suas Despesas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("💰 Mensais")
        for item in dados["mensais"]:
            st.write(f"{item['icon']} {item['nome']}: {item['valor']:.2f} €")
    
    with col2:
        st.subheader("📅 Trimestrais")
        for item in dados["trimestrais"]:
            st.write(f"{item['icon']} {item['nome']}: {item['valor']:.2f} €")
    
    with col3:
        st.subheader("📊 Anuais")
        for item in dados["anuais"]:
            st.write(f"{item['icon']} {item['nome']}: {item['valor']:.2f} €")
    
    # Mostra os totais calculados
    st.divider()
    totais = calcular_totais(dados)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Mensal", f"{totais['mensal']:.2f} €")
    with col2:
        st.metric("Total Trimestral", f"{totais['trimestral']:.2f} €")
    with col3:
        st.metric("Total Anual", f"{totais['anual']:.2f} €")
    with col4:
        st.metric("Total Anual Projetado", f"{totais['anual_projetado']:.2f} €")

elif pagina == "✏️ Editar Despesas":
    st.header("✏️ Editar Despesas")
    
    categoria = st.selectbox("Selecione a categoria:", 
                            ["Mensais", "Trimestrais", "Anuais"])
    
    categoria_key = categoria.lower()
    
    st.subheader(f"Despesas {categoria}")
    
    # Formulário para editar os valores das despesas existentes
    with st.form(f"form_{categoria_key}"):
        for i, item in enumerate(dados[categoria_key]):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text_input("Nome", value=item["nome"], key=f"nome_{categoria_key}_{i}", disabled=True)
            with col2:
                # O valor é atualizado diretamente na estrutura de dados
                novo_valor = st.number_input("Valor (€)", value=float(item["valor"]), 
                                           min_value=0.0, step=5.0, 
                                           key=f"valor_{categoria_key}_{i}")
                dados[categoria_key][i]["valor"] = novo_valor
        
        submitted = st.form_submit_button("💾 Guardar Alterações")
        if submitted:
            salvar_dados(dados)
            st.success("Despesas atualizadas com sucesso!")
            st.rerun() # Reinicia a aplicação para refletir as mudanças

    # Seção para adicionar uma nova despesa
    st.divider()
    st.subheader("Adicionar Nova Despesa")
    
    with st.form(f"add_form_{categoria_key}"):
        novo_nome = st.text_input("Nome da nova despesa")
        novo_valor = st.number_input("Valor (€)", min_value=0.0, step=5.0, value=0.0)
        icon_options = ["🏠", "💧", "💡", "📱", "🎨", "🛒", "👩", "🏃", "🏛️", "➕", "📊", "🛡️", "🚗"]
        novo_icon = st.selectbox("Ícone", icon_options, index=len(icon_options)-1)
        
        submitted_add = st.form_submit_button("➕ Adicionar Despesa")
        
        if submitted_add and novo_nome:
            dados[categoria_key].append({
                "nome": novo_nome,
                "valor": novo_valor,
                "icon": novo_icon
            })
            salvar_dados(dados)
            st.success("Despesa adicionada com sucesso!")
            st.rerun() # Reinicia a aplicação para refletir as novas despesas

elif pagina == "📊 Resumo Financeiro":
    st.header("📊 Resumo Financeiro")
    
    totais = calcular_totais(dados)
    
    # Mostra as métricas principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Mensal", f"{totais['mensal']:.2f} €")
    with col2:
        st.metric("Total Trimestral", f"{totais['trimestral']:.2f} €")
    with col3:
        st.metric("Total Anual", f"{totais['anual']:.2f} €")
    with col4:
        st.metric("Total Anual Projetado", f"{totais['anual_projetado']:.2f} €")
    
    st.divider()
    
    # Gráficos de distribuição de despesas
    st.subheader("Distribuição de Despesas")
    
    # Prepara os dados para o DataFrame
    chart_data = []
    for categoria, items in dados.items():
        for item in items:
            if item["valor"] > 0:
                chart_data.append({
                    "Categoria": categoria.capitalize(),
                    "Despesa": item["nome"],
                    "Valor": item["valor"]
                })
    
    if chart_data:
        df = pd.DataFrame(chart_data)
        
        # Gráfico de pizza
        fig = px.pie(df, values='Valor', names='Despesa', 
                     title='Distribuição de Despesas por Categoria',
                     hover_data=['Categoria'])
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de barras
        fig2 = px.bar(df, x='Despesa', y='Valor', color='Categoria',
                     title='Valor das Despesas por Categoria',
                     labels={'Valor': 'Valor (€)', 'Despesa': 'Despesa'})
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Adicione valores às suas despesas para ver os gráficos.")

# --- Rodapé da Barra Lateral ---
st.sidebar.divider()
st.sidebar.info("💡 Dica: Atualize os valores regularmente para manter seu orçamento sob controle!")
st.sidebar.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
