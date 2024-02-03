import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from app import load_info_sidebar, plot_title


if 'data' not in st.session_state:
    st.info("🚨 Ops! Você ainda não fez o upload do arquivo na página 🏠Home")
else:
    plot_title()

    #load dataset
    df = st.session_state['data']

    # Growth
    # ### Annual Donation Growth ----------------------------------
    gr1 = df.groupby(['ano','classe']).agg({'id':'count', 'valor':'sum'}).reset_index()
    gr1.sort_values(by='ano', inplace=True)
    gr1.columns = ['ano','classe','doações','$ arrecadado']
    gr1['ano'] = gr1['ano'].astype(str)
    gr1['classe'] = gr1['classe'].astype(str)

    st.markdown("**Crescimento anual das doações (por classe)**")
    st.bar_chart(gr1, x="ano", y="$ arrecadado", color="classe")

    # ### Annual Donor Growth ------------------------------------
    gr2 = df.groupby(['ano','classe']).agg({'id':'nunique', 'valor':'sum'}).reset_index()
    gr2.sort_values(by='ano', inplace=True)
    gr2.columns = ['ano','classe','quantidade doadores','R$ arrecadado']
    gr2['ano'] = gr2['ano'].astype(str)
    gr2['classe'] = gr2['classe'].astype(str)

    st.markdown("**Crescimento anual dos doadores (por classe)**")
    st.bar_chart(gr2, x="ano", y="quantidade doadores", color="classe")

    btn = st.button(f"Próxima análise")
    if btn:
        switch_page("Tempo entre doações")

#----------------------------------------
load_info_sidebar()
