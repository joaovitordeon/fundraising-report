import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
from app import load_info_sidebar, plot_title


def formatar_reais(valor):
    valor_formatado = "{:,.2f}".format(valor)
    return f'R${valor_formatado.replace(",", ";").replace(".", ",").replace(";", ".")}'

if 'data' not in st.session_state:
    st.info("🚨 Ops! Você ainda não fez o upload do arquivo na página 🏠Home")
else:
    plot_title()

    #load dataset
    df = st.session_state['data']

    # ------------------------------------------------- BIG NUMBERS ----------------------------------------------------------------
    grid = st.columns([3, 3, 3, 3])
    grid[0].metric("**Total arrecadado**", value=formatar_reais(df.valor.sum()))
    grid[1].metric("**Quantidade de doações únicas**", value=df.shape[0])
    grid[2].metric("**Quantidade de doadores únicos**", value=df.id.nunique())
    grid[3].metric("**Ticket médio por doação**", value=formatar_reais(df.valor.mean()))
    st.divider()

    # ------------------------------------------------- PLOTS ----------------------------------------------------------------

    # ### Total Donations -------------------------------------------------
    gp1 = df.groupby(['ano'])['valor'].sum().reset_index()
    gp1.sort_values(by='ano', inplace=True)
    gp1['ano'] = gp1['ano'].astype(str)

    gp1_ = df.groupby(['mes-ano'])[['valor']].sum()
    gp1_.reset_index(inplace=True)

    st.markdown("**Total arrecadado**")
    period = st.radio(
        label="periodo",
        label_visibility = 'hidden',
        options = ["Por mês","Por ano"],
        horizontal=True,
        key='p1'
    )

    if period == 'Por ano':
        st.area_chart(gp1, x="ano", y="valor", color="#64EB84")
    elif period == 'Por mês':
        st.area_chart(gp1_, x="mes-ano", y="valor", color="#64EB84")
    else:
        st.info("No chart do plot")


    # ### Total Donors -------------------------------------------------
    gp2 = df.groupby(['ano'])['id'].nunique().reset_index()
    gp2.sort_values(by='ano', inplace=True)
    gp2.columns = ['ano','doadores únicos']
    gp2['ano'] = gp2['ano'].astype(str)

    gp2_ = df.groupby(['mes-ano'])[['id']].nunique()
    gp2_.reset_index(inplace=True)
    gp2_.columns = ['mes-ano','doadores únicos']

    st.markdown("**Total de doadores**")
    period = st.radio(
        label="periodo",
        label_visibility = 'hidden',
        options = ["Por mês","Por ano"],
        horizontal=True,
        key='p2'
    )

    if period == 'Por ano':
        st.area_chart(gp2, x="ano", y="doadores únicos", color="#64EBEB")
    elif period == 'Por mês':
        st.area_chart(gp2_, x="mes-ano", y="doadores únicos", color="#64EBEB")
    else:
        st.info("No chart do plot")

    # ### Ticket médio por ano ---------------------------------------
    gpt = df.groupby(['ano','classe'])['valor'].mean().reset_index()
    gpt.sort_values(by='ano', inplace=True)
    gpt['valor'] = gpt['valor'].round(2)

    gpt.columns = ['ano','classe','ticket médio']
    gpt['ano'] = gpt['ano'].astype(str)
    gpt['classe'] = gpt['classe'].astype(str)

    st.markdown("**Ticket médio por ano (agrupado por classe de valor)**")
    st.area_chart(gpt, x="ano", y="ticket médio", color="classe")

    # ### Doadores que doaram apenas uma vez no ano (Single Gift Donors) -------------------------
    counts = df.groupby(['ano', 'id']).size().reset_index(name='contagem')
    unique_ids = counts[counts['contagem'] == 1]
    unique_ids['ano'] = unique_ids['ano'].astype(str) 

    gp3 = unique_ids.groupby('ano')['id'].nunique().reset_index(name='contagem')
    gp3['ano'] = gp3['ano'].astype(str)

    st.markdown("**Quantidade de doadores com doações únicas por ano**")
    grid = st.columns([7,3])
    grid[0].area_chart(gp3, x="ano", y="contagem", color="#6DB5F5")
    grid[1].expander("dados").dataframe(unique_ids)


    # ### Quantidade de doadores recorrentes (Recurring Donors) ----------------------------------
    counts_ = df.groupby(['ano', 'id']).size().reset_index(name='contagem')
    doadores_freq = counts_[counts_['contagem'] >= 3].copy()
    doadores_freq['ano'] = doadores_freq['ano'].astype(str)

    gp4 = doadores_freq.groupby('ano')['id'].nunique().reset_index(name='contagem')
    gp4['ano'] = gp4['ano'].astype(str)

    st.markdown("**Quantidade de doadores recorrentes (>=3 doações por ano)**")
    grid = st.columns([7,3])
    grid[0].area_chart(gp4, x="ano", y="contagem", color="#6D88F5")
    grid[1].expander("dados").dataframe(doadores_freq)


    # ### Para cada ano, calcule a taxa de retenção (Retention Rate) ----------------------------------
    res = []
    for ano_atual in sorted(df['ano'].unique()):
        ano_anterior = ano_atual - 1
        ids_ano_atual = set(df[df['ano'] == ano_atual]['id'])

        ids_ano_anterior = set(df[df['ano'] == ano_anterior]['id'])
        doadores_renovados = ids_ano_anterior.intersection(ids_ano_atual)

        try:
            taxa_retencao = len(doadores_renovados) / len(ids_ano_anterior) * 100
        except:
            taxa_retencao = 0

        res.append({'ano': ano_atual, 'taxa_retencao': taxa_retencao})

    gp5 = pd.DataFrame(res)
    gp5 = gp5.round(2)
    gp5['ano'] = gp5['ano'].astype(str)

    st.markdown("**Taxa de Retenção (em %) de doadores por ano**")
    st.area_chart(gp5, x="ano", y="taxa_retencao", color="#DE6DF5")


    # ### Doações médias por ano (Donation Frequency by year) ----------------------------------
    gp6 = df.groupby(['id', 'ano']).size().reset_index(name='quantidade')

    gp6 = gp6.groupby('ano')['quantidade'].mean().reset_index().round(2)
    gp6['ano'] = gp6['ano'].astype(str)

    st.markdown("**Quantidade média de doações por doador em cada ano**")
    st.area_chart(gp6, x="ano", y="quantidade", color="#BAF56D")

    btn = st.button(f"Próxima análise")
    if btn:
        switch_page("Crescimento")

#-----------------------------
load_info_sidebar()
