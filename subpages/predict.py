import joblib
import streamlit as st
import pandas as pd


def predict():
    if "df" not in st.session_state:
        st.session_state.df = None

    if st.session_state.df is None:
        st.subheader('Realize as orientações na aba DataSUS')
    else:
        if "df_final" not in st.session_state:
            st.session_state.df_final = None
            
        if st.session_state.df_final is None:
            st.subheader('Acesse a aba Análise Exploratória')
        else:
            st.title("Predição")

            df_final = st.session_state.df_final
            data = df_final[['ANO_CMPT', 'MES_CMPT', 'CNES', 'fxetar5', 'sexo', 'DIAG_PRINC', 'qnt']]
            data.columns = ['ANO', 'MES', 'CNES', 'IDADE', 'SEXO', 'DIAG_PRINC', 'TOT_INTER']
            data = pd.get_dummies(data = data, columns=['IDADE', 'SEXO', 'DIAG_PRINC'])
            df = data.groupby(['ANO', 'MES', 'CNES']).sum().reset_index()


            model_mais_1  = joblib.load('./data/processed/best_model_mais_1.joblib')
            model_mais_2  = joblib.load('./data/processed/best_model_mais_2.joblib')

            col_model  = joblib.load('./data/processed/col_model.joblib')

            for col in col_model:
                if(not(col in df.columns)):
                    df[col] = 0

            X = df

            df['TOT_INTER_mais_1'] = model_mais_1.predict(X)
            df['TOT_INTER_mais_2'] = model_mais_2.predict(X)

            df['TOT_INTER_mais_1'] = df['TOT_INTER_mais_1'].map('{:,.0f}'.format)
            df['TOT_INTER_mais_2'] = df['TOT_INTER_mais_2'].map('{:,.0f}'.format)


            cnes = pd.read_csv('data/raw/cnes.csv', sep=";")
            cnes=cnes[cnes['CNES'].isin(df.CNES)]

            values = cnes['Estabelecimento'].tolist()
            options = cnes['CNES'].tolist()
            dic = dict(zip(options, values))

            selectbox = st.selectbox('Selecione um Hospital da lista:', options, format_func=lambda x: dic[x])

            df_select = df[['ANO', 'MES', 'CNES', 'TOT_INTER', 'TOT_INTER_mais_1', 'TOT_INTER_mais_2']].query("CNES == "+str(selectbox))
            df_select.columns = ['ANO', 'Mês Ref.', 'CNES', 'Internações do Mês', 'Predição Internações +1 Mês', 'Predição Internações +2 Meses']
            df_select = df_select.set_index('CNES')

            hide_table_row_index = """
            <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
            </style>
            """
            
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            
            st.table(df_select)

            

