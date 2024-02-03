import pandas as pd
import streamlit as st
from st_pages import Page, show_pages
from streamlit_extras.switch_page_button import switch_page

# main configs
st.set_page_config(page_title='Fundraising Report', page_icon=':chart_with_upwards_trend:', layout="wide", initial_sidebar_state='expanded')

show_pages(
    [   
        Page("app.py", "Home", "🏠"),
        Page("pages/general_metrics.py", "Métricas gerais", "📊"),
        Page("pages/growth.py", "Crescimento", "📈"),
        Page("pages/time_between_d.py", "Tempo entre doações", "⏱️"),
        Page("pages/upgrade.py", "Doadores que fizeram upgrade", "🆙"),
        Page("pages/RFM.py", "Matriz RFM", "🧮"),

    ]
)

def plot_title():
    st.title("Fundraising Report 📈")
    for i in range(2):
        st.text("\n")

plot_title()

#-----------------------------------
st.session_state['data'] = None

def load_data():
    return st.session_state['data']

# function to read only csv files
def get_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file, sep=';')
    except Exception as e:
        df = None
    else:
        if len(df.columns) != 3:
            df = None

    return df

@st.cache_data
def get_data(uploaded_file):
    df = get_csv(uploaded_file)
    
    if df is None:
        raise Exception("CSV is out of configuration")

    else:
        df.columns = ['id','data','valor']
        df.id = df.id.astype(str)

        df['data'] = pd.to_datetime(df['data'], infer_datetime_format=True, dayfirst=True)

        df['dia'] = df['data'].dt.day
        df['mes'] = df['data'].dt.month
        df['ano'] = df['data'].dt.year
        df['mes-ano'] = df['data'].dt.to_period('M').astype(str)
        df['valor'] = df['valor'].apply(lambda x: str(x).replace(',','.')).astype(float) 

        # create value classes
        intervalos = [0, 10, 20, 50, 70, 100, float('inf')]
        rotulos = ['Abaixo de 10 reais', 'de 10 a 20 reais', 'de 20 a 50 reais', 'de 50 a 70 reais', 'de 70 a 100 reais', 'Acima de 100 reais']
        # pd.cut() to create new column for value classes
        df['classe'] = pd.cut(df['valor'], bins=intervalos, labels=rotulos, right=False)

        # sort df by date
        df.sort_values(by='data', inplace=True)
        
        return df.reset_index(drop=True)


@st.cache_resource
def load_info_sidebar():
    for i in range(14):
        st.sidebar.text('\n')

    st.sidebar.markdown(
        '<h5>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="30">&nbsp by J V L DEON ASSESSORIA</h5>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        '<h5>Contact e-mail:  joaovitordeon@gmail.com</h5>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        '<div style="margin-top: 1.5em;"><a href="https://www.buymeacoffee.com/joaovitordeon" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="45" width="184"></a></div>',
        unsafe_allow_html=True,
    )

    # make side bar extended
    st.markdown("""
        <style>
        div[data-testid='stSidebarNav'] ul {max-height:none}</style>
        """, unsafe_allow_html=True)
    
#-------------------------------------------------------------------------------------
with st.expander("Recomendações para o arquivo CSV...", expanded=True):
    st.markdown("<strong>OBS1:</strong> O arquivo deve conter três colunas: <strong>id, data e valor.</strong>", unsafe_allow_html=True)
    st.markdown("<strong>OBS2:</strong> O formato da data deve ser preferencialmente <strong>dia/mês/ano.</strong>", unsafe_allow_html=True)
    st.markdown("<strong>OBS3:</strong> O caractere de separação de campos deve ser o <strong>';' (ponto e vírgula)</strong>", unsafe_allow_html=True)
    st.markdown("<strong>OBS4:</strong> O arquivo deve estar salvo na formatação universal <strong>UTF-8.</strong>", unsafe_allow_html=True)

df_ex = pd.DataFrame({'id': {0: 'D0A1ddq201W0Q0TR00', 1: '0M0A010Y0mAgT210hQ', 2: '0A0GX01HHT00R002Q1', 3: 'Amg080o3AQ0000g11B', 4: 'TD100ZAQ0m01y00ZV2'}, 'data': {0: '10/11/2021', 1: '20/06/2021', 2: '11/04/2021', 3: '06/07/2021', 4: '07/12/2022'}, 'valor': {0: 20.0, 1: 25.0, 2: 55.0, 3: 60.0, 4: 20.0}})

with st.expander("Arquivo de exemplo..."):
    grid = st.columns([1, 1])
    grid[0].dataframe(df_ex)
    grid[1].markdown("**Explicação das colunas**:")
    grid[1].markdown("- <p><strong>id</strong> é o ID do doador, que deve ser sempre o mesmo para um doador X</p>", unsafe_allow_html=True)
    grid[1].markdown("- <p><strong>data</strong> é a data daquela doação</p>", unsafe_allow_html=True)
    grid[1].markdown("- <p><strong>valor</strong> é o valor doado naquela doação</p>", unsafe_allow_html=True)

for i in range(2):
    st.text("\n")

grid = st.columns([1,1])
uploaded_file = st.file_uploader(label=":black[**Faça o upload de um arquivo CSV**]", type=(["csv"]), accept_multiple_files=False, label_visibility='visible')

if uploaded_file is not None:
    # reset session states when user choose to select other file 
    try:
        del st.session_state['file_name']
        del st.session_state['data']
    except:
        pass
    
    # try to get data
    try:
        data = get_data(uploaded_file)
    # warn user when file is not well configurated
    except:
        st.error("🚨 Encontramos um erro em seu arquivo. Veja as recomendações acima e tente novamente...")
    else:
        # if csv upload was fine, then save data and name data in new session states
        st.session_state['file_name'] = uploaded_file.name
        st.session_state['data'] = data

# if session state keeps csv data, then show some UI infos
if 'data' in st.session_state:
    st.text(f"Arquivo atualmente selecionado: {st.session_state['file_name']}")
    st.text('\n')
    
    btn = st.button(f"Clique aqui para ver a mágina acontecer 🕵️‍♂️🪄✨")
    if btn:
        switch_page("Métricas gerais")
        
#------------------------------
load_info_sidebar()
