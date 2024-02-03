import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
from app import load_info_sidebar, plot_title


if 'data' not in st.session_state:
    st.info("🚨 Ops! Você ainda não fez o upload do arquivo na página 🏠Home")
else:
    plot_title()

    #load dataset
    df = st.session_state['data']
    
    # Time between donations ------------------------------------
    doacoes_df = df.copy()
    doacoes_df.sort_values(by=['id', 'data'], inplace=True)
    doacoes_df['tempo_entre_doacoes'] = doacoes_df.groupby('id')['data'].diff().dt.days
    doacoes_df.dropna(subset='tempo_entre_doacoes', inplace=True)
    
    tempomedio = doacoes_df.groupby('id')['tempo_entre_doacoes'].mean().reset_index(name='tempo_medio_entre_doacoes').round(2)

    # Consider as recurrent donors the has mean time donation between 30 to 45 days
    recorrentes = tempomedio[tempomedio['tempo_medio_entre_doacoes'].between(0,45)]
    
    Qt = recorrentes['tempo_medio_entre_doacoes'].quantile(.9)

    st.metric(label="**90% dos doadores RECORRENTES tem um :blue[tempo médio entre as doações (em dias)] menor ou igual a:**", value=round(Qt,2)) 

    # get last donation of each reccurrent donor
    dtultimadoacao = doacoes_df.groupby('id')['data'].max().reset_index(name='data_ultima_doacao')
    recorrentes = recorrentes.merge(dtultimadoacao)
    recorrentes['dias_desde_ultima_doacao'] = (datetime.now() - recorrentes.data_ultima_doacao).dt.days

    for _ in range(2):
        st.text("\n")

    st.markdown("**Doadores RECORRENTES que o tempo médio entre suas doações é menor que 45 dias**")
    st.dataframe(recorrentes)

    btn = st.button(f"Próxima análise")
    if btn:
        switch_page("Doadores que fizeram upgrade")

#----------------------------------------
load_info_sidebar()
