import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from app import load_info_sidebar, plot_title

if 'data' not in st.session_state:
    st.info("🚨 Ops! Você ainda não fez o upload do arquivo na página 🏠Home")
else:
    plot_title()

    st.write("Essa sessão se destina a mostrar os doadores que fizeram upgrade em doações e de quanto foi esse upgrade.")
    st.write("Upgrade é considerado um aumento de valor doado entre a menor e a maior doação que um doador já fez.")
    st.write("Isso pode ser extremamente útil para identificar doadores que são mais fiéis com a causa e podem entrar em campanhas de aumento de doação, aumentando seu LTV.")
    st.write("Entender quais doadores tem essa capacidade de aumento de LTV é uma estratégia de retenção poderosíssima.")

    st.info("**Entre em contato conosco para desbloquear essa funcionalidade**")

    btn = st.button(f"Próxima análise")
    if btn:
        switch_page("Matriz RFM")
        
#----------------------------------------
load_info_sidebar()
