import streamlit as st
import pandas as pd
from datetime import datetime
from app import load_data, load_info_sidebar, plot_title

if 'data' not in st.session_state:
    st.info("🚨 Ops! Você ainda não fez o upload do arquivo na página 🏠Home")
else:
    plot_title()

    st.write("""A matriz RFM (Recency, Frequency, Monetary) é uma ferramenta de análise usada para entender o comportamento do doador com base em três dimensões principais: 
             Recência, Frequência e Valor Monetário.    No contexto de Organizações da Sociedade Civil (OSCs), que fazem parte do terceiro setor, 
             a aplicação da matriz RFM pode ser adaptada para analisar o engajamento de doadores ou apoiadores. Vamos explorar como isso poderia funcionar:

    - Recency (Recência):
    Avalia o tempo desde a última doação ou interação com a organização. Quanto mais recente a interação, maior a pontuação.
    
    - Frequency (Frequência):
    Mede com que frequência um doador contribui ou interage com a organização. Quanto mais frequente a participação, maior a pontuação.
    
    - Monetary (Valor Monetário):
    Refere-se ao valor total doação ou apoio financeiro. Quanto maior o valor, maior a pontuação.
    
    A pontuação em cada dimensão pode ser atribuída em uma escala, por exemplo, de 1 a 5, onde 5 é a pontuação mais alta. 
    Essas pontuações podem ser somadas para obter uma pontuação geral de RFM para cada doador ou grupo de doadores.

    Depois de atribuir pontuações, a organização pode classificar os doadores em diferentes segmentos da seguinte forma:

    - Champions (Campeões): Alto em todas as dimensões (Recency, Frequency, Monetary). São os doadores mais valiosos e engajados.
    - Loyal Supporters (Apoiadores Leais): Alta Frequência e Valor Monetário, mas talvez não tão recentes em termos de interação.
    - Potential Loyalists (Potenciais Apoiadores Leais): Alta Recência e Frequência, mas talvez com um valor monetário menor.
    - At Risk (Em Risco): Baixa Recência, Frequência ou Valor Monetário. Pode precisar de esforços para reengajar.
    - Dormant (Inativos): Baixa Recência, Frequência e Valor Monetário. Pode ter sido um doador valioso no passado, mas agora precisa ser reativado.

    Essa segmentação permite que as OSCs personalizem suas estratégias de envolvimento, direcionando esforços específicos para reter, 
    reativar ou aprofundar o relacionamento com diferentes grupos de doadores.""")

    st.info("**Entre em contato conosco para desbloquear essa funcionalidade**")

#----------------------------------------
load_info_sidebar()
