import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Gestor de Despesas Pessoais",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização dos dados
def carregar_dados():
    """Carrega os dados do arquivo JSON ou inicializa com valores padrão"""
    if os.path.exists("despesas.json"):
        try:
            with open("despesas.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    # Dados iniciais se o arquivo não existir
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
    """Salva os dados no arquivo JSON"""
    with open("despesas.json", 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# Carregar dados
dados = carregar_dados()

# Título da aplicação
st.title("💰 Gestor de Despesas Pessoais")

# Barra lateral para navegação
st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Selecione a página:", 
                         ["📋 Visualizar Despesas", "✏️ Editar Despesas", "📊 Resumo Financeiro"])

# Função para calcular totais
def calcular_totais(dados):
    totais = {
        "mensal": sum(item["valor"] for item in dados["mensais"]),
        "trimestral": sum(item["valor"] for item in dados["trimestrais"]),
        "anual": sum(item["valor"] for item in dados["anuais"])
    }
    
    totais["anual_projetado"] = (totais["mensal"] * 12) + (totais["trimestral"] * 4) + totais["anual"]
    totais["mensal_medio"] = totais["anual_projetado"] / 12
    
    return totais

# Página: Visualizar Despesas
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
    
    # Mostrar totais
    totais = calcular_totais(dados)
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Mensal", f"{totais['mensal']:.2f} €")
    with col2:
        st.metric("Total Trimestral", f"{totais['trimestral']:.2f} €")
    with col3:
        st.metric("Total Anual", f"{totais['anual']:.2f} €")
    with col4:
        st.metric("Total Anual Projetado", f"{totais['anual_projetado']:.2f} €")

# Página: Editar Despesas
elif pagina == "✏️ Editar Despesas":
    st.header("✏️ Editar Despesas")
    
    categoria = st.selectbox("Selecione a categoria:", 
                            ["Mensais", "Trimestrais", "Anuais"])
    
    categoria_key = categoria.lower()
    
    st.subheader(f"Despesas {categoria}")
    
    # Formulário para editar despesas
    with st.form(f"form_{categoria_key}"):
        for i, item in enumerate(dados[categoria_key]):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text_input("Nome", value=item["nome"], key=f"nome_{categoria_key}_{i}", disabled=True)
            with col2:
                novo_valor = st.number_input("Valor (€)", value=float(item["valor"]), 
                                           min_value=0.0, step=5.0, 
                                           key=f"valor_{categoria_key}_{i}")
                dados[categoria_key][i]["valor"] = novo_valor
        
        submitted = st.form_submit_button("💾 Guardar Alterações")
        if submitted:
            salvar_dados(dados)
            st.success("Despesas atualizadas com sucesso!")
    
    # Adicionar nova despesa
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
            st.rerun()

# Página: Resumo Financeiro
elif pagina == "📊 Resumo Financeiro":
    st.header("📊 Resumo Financeiro")
    
    totais = calcular_totais(dados)
    
    # Métricas principais
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
    
    # Gráfico de distribuição de despesas
    st.subheader("Distribuição de Despesas")
    
    # Preparar dados para o gráfico
    chart_data = []
    for categoria, items in dados.items():
        for item in items:
            if item["valor"] > 0:
                chart_data.append({
                    "Categoria": categoria.capitalize(),
                    "Despesa": item["nome"],
                    "Valor": item["valor"],
                    "Ícone": item["icon"]
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
        st.info("Adicione valores às suas despesas para ver gráficos.")

# Informações na barra lateral
st.sidebar.divider()
st.sidebar.info("💡 Dica: Atualize os valores regularmente para manter seu orçamento sob controle!")

# Rodapé
st.sidebar.divider()
st.sidebar.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
