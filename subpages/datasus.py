import pandas as pd
import streamlit as st

from src.controller.DataFrameController import DataFrameController


def datasus():
    st.image('src/view/assets/image/logo2.png', width = 200)
    
    st.subheader("Download dos dados")
    st.markdown("Os dados contidos no DataSUS podem ser acessados atraves do link abaixo.")
    st.markdown('[datasus-download](https://datasus-download.herokuapp.com/)')
    st.markdown("Escolha um período e baixe os dados.")

    st.markdown("""---""")

    st.markdown("Após a realização do download submeta o arquivo para análise no botão baixo.")

    data_file = st.file_uploader("Upload CSV",type=["csv"])
    
    if data_file is not None:
        with st.spinner('Wait for it...'):
            dataframe = pd.read_csv(data_file, sep=',')
            
            st.markdown("A base de dados selecionada possui **" + str(dataframe.shape[0]) + " registros** de todo o Ceará")
            
            dataframe = DataFrameController.filter_data(dataframe)
            
            st.session_state.df = dataframe
            
            st.markdown("**" + str(dataframe.shape[0]) + " registros** obtidos após o filtro para os pacientes recidentes em **Fortaleza** e atendidos em Fortaleza.")

            st.subheader("Liberado o acesso para a Análise Exploratória.")
