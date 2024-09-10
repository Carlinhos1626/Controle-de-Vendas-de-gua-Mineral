import streamlit as st
import pandas as pd
from datetime import datetime

# Função para carregar os dados em cache


@st.cache_data
def carregar_dados():
    return []

# Função para adicionar uma nova venda aos dados em cache


def adicionar_venda(dados, nova_venda):
    dados.append(nova_venda)
    return dados


# Carrega os dados (inicialmente vazios)
if 'dados_vendas' not in st.session_state:
    st.session_state.dados_vendas = carregar_dados()

# Sidebar para navegação
pagina = st.sidebar.selectbox(
    "Selecione a página", ["Registrar Venda", "Relatórios"])

if pagina == "Registrar Venda":
    st.title("Sistema de Controle de Venda de Águas")

    # Campos de entrada
    quantidade = st.number_input("Quantidade de Águas", min_value=1, step=1)
    torre = st.text_input("Torre")
    apartamento = st.text_input("Apartamento")
    validade_garrafao = st.text_input(
        "Validade do Garrafão")  # Input como texto aberto
    forma_pagamento = st.selectbox(
        "Forma de Pagamento", ["Dinheiro", "Cartão", "Pix"])
    condominio = st.text_input("Condomínio")

    # Botão de submissão
    if st.button("Registrar Venda"):
        data_venda = datetime.now().strftime("%Y-%m-%d")
        hora_venda = datetime.now().strftime("%H:%M:%S")
        nova_venda = {
            "Data": data_venda,
            "Hora": hora_venda,
            "Quantidade de Águas": quantidade,
            "Torre": torre,
            "Apartamento": apartamento,
            "Validade do Garrafão": validade_garrafao,
            "Forma de Pagamento": forma_pagamento,
            "Condomínio": condominio,
        }

        # Adiciona a nova venda aos dados em session_state
        st.session_state.dados_vendas = adicionar_venda(
            st.session_state.dados_vendas, nova_venda)
        st.success("Venda registrada com sucesso!")

elif pagina == "Relatórios":
    st.title("Relatório de Vendas")

    # Verifica se há dados
    if st.session_state.dados_vendas:
        # Converte os dados em um DataFrame
        df = pd.DataFrame(st.session_state.dados_vendas)

        # Filtro por data
        data_selecionada = st.date_input(
            "Selecione a data", value=datetime.now().date())

        # Filtra o dataframe pela data selecionada
        df['Data'] = pd.to_datetime(df['Data']).dt.date
        df_filtrado = df[df['Data'] == data_selecionada]

        # Calcula os resumos
        total_vendas = df_filtrado['Quantidade de Águas'].sum()
        faturamento_total = total_vendas * 5  # Supondo que cada água custa R$5

        # Exibe os cards
        st.metric("Águas Vendidas no Dia", total_vendas)
        st.metric("Faturamento Total", f"R$ {faturamento_total:.2f}")

        # Exibe a tabela
        st.subheader("Pedidos do Dia")
        st.dataframe(df_filtrado)
    else:
        st.warning("Nenhuma venda registrada ainda.")
