from urllib.request import urlopen
import json
import numpy as np
import pandas as pd
import streamlit as st
import geopandas as gpd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.controller.DataFrameController import DataFrameController


def analytics_explore():
    if "df" not in st.session_state:
        st.session_state.df = None

    if st.session_state.df is None:
        st.subheader('Realize as orientações na aba DataSUS')
    else:
        st.title("Análise Exploratória")

        dataframe = st.session_state.df
        df_final = DataFrameController.data_enrichment(dataframe)

        st.session_state.df_final = df_final

        df_barchart = pd.DataFrame(df_final.groupby(['GRUPO'])["qnt"].sum())
        bar_chart = df_barchart.add_suffix('').reset_index()

        bar_chart['percent'] = round((bar_chart['qnt'] / bar_chart['qnt'].sum()) * 100, 2)

        top8 = bar_chart.nlargest(8, 'percent')
        top8 = top8.sort_values(by = 'qnt')

        percentual_top_8 = str(top8['percent'].sum())

        st.subheader("Grupos de diagnósticos")
        st.markdown('**8 Grupos de diagnósticos** resume cerca de **' + percentual_top_8 + '%** do total de internações por condições sensíveis à Atenção Primária no território Fortalezense.')
        
        top8 = top8.sort_values(by = 'qnt', ascending = False)
        
        percentual = top8['percent']
        valor_absoluto = top8['qnt']
        x = top8['GRUPO']


        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=percentual,
            y=x,
            marker=dict(
                color='rgba(255, 87, 87, 0.6)',
                line=dict(
                    color='rgba(255, 87, 87, 1.0)',
                    width=1),
            ),
            name='Valores relativos',
            orientation='h',
        ))

        fig.update_layout(
            title='8 Principais causas de Internações hospitalares por CSAP de acordo com o Grupo da CID-10',
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=True,
                domain=[0, 0.85],
            ),
            yaxis2=dict(
                showgrid=False,
                showline=True,
                showticklabels=False,
                linecolor='rgba(102, 102, 102, 0.8)',
                linewidth=2,
                domain=[0, 0.85],
            ),
            xaxis=dict(
                zeroline=False,
                showline=False,
                showticklabels=True,
                showgrid=True,
                domain=[0, 0.42],
            ),
            xaxis2=dict(
                zeroline=False,
                showline=False,
                showticklabels=True,
                showgrid=True,
                domain=[0.47, 1],
                side='top',
                dtick=2000,
            ),
            legend=dict(x=0.029, y=1.038, font_size=10),
            margin=dict(l=100, r=20, t=70, b=70),
            paper_bgcolor='rgb(248, 248, 255)',
            plot_bgcolor='rgb(248, 248, 255)',
        )
        #Adicionando anotações no gráfico
        annotations = []

        y_s = np.round(percentual, decimals=2)
        y_nw = np.rint(valor_absoluto)

        # Adicionando as labels
        for ydn, yd, xd in zip(y_nw, y_s, x):
            # Gráfico com valores relativos
            annotations.append(dict(xref='x1', yref='y1',
                                    y=xd, x=yd + 3,
                                    text=str(yd) + '%',
                                    font=dict(family='Arial', size=12,
                                            color='rgb(255, 87, 87)'),
                                    showarrow=False))
        # Fonte dos dados
        annotations.append(dict(xref='paper', yref='paper',
                                x=-0.1, y=-0.110,
                                text='Fonte dos dados: Departamento de Informática do SUS (DATASUS)',
                                font=dict(family='Arial', size=11, color='rgb(150,150,150)'),
                                showarrow=False))

        fig.update_layout(annotations=annotations)

        st.plotly_chart(fig)
        
        st.markdown("""---""")

        st.subheader("Taxa de Internações po CSAP por mil/hab")

        df_bairros = pd.DataFrame(df_final.groupby(['Bairro _formatado'])["qnt"].sum())
        df_bairros = df_bairros.add_suffix('').reset_index()

        mapa = gpd.read_file('data/raw/bairros_nomes.geojson')
        mapa_plot = mapa.merge(df_bairros, left_on='NOME', right_on='Bairro _formatado')

        export_bairros = pd.read_excel('data/raw/export_bairros.xltx')
        export_df = df_final.merge(export_bairros, left_on='Bairro _formatado', right_on='BAIRRO')

        plot_map = pd.DataFrame(export_df.groupby(['Bairro _formatado', 'GID', 'IDH-B'])["qnt"].sum())
        plot_map = plot_map.add_suffix('').reset_index()

        pop_bairros = pd.read_csv('data/raw/pop_idh_bairros.csv', sep=";")

        plot_map = plot_map.merge(pop_bairros, left_on='Bairro _formatado', right_on='Bairro _formatado', suffixes=('', '_delme'))

        plot_map['int_div'] = plot_map['qnt']
        plot_map['taxa_100_hab'] = round((plot_map['int_div'] / plot_map['pop_total']) * 1000, 2)
        plot_map['taxa_100_hab'].max()

        plot_map = mapa_plot.merge(plot_map, left_on='GID', right_on='GID')
        
        with urlopen('https://raw.githubusercontent.com/igorduartt/Fundacao/main/bairros_fortaleza%20(1).json') as response:
            counties = json.load(response)

        counties["features"][0]

        data_map = plot_map

        fig = px.choropleth_mapbox(data_map, geojson=counties, locations='id', color='taxa_100_hab',
            color_continuous_scale='ylorrd',
            hover_name="NOME", 
            hover_data={"IDH-B":True,"taxa_100_hab":True,"id":False},
            range_color=([0, 40]),
            mapbox_style="open-street-map",
            zoom=10, center = {"lat": -3.7272872, "lon": -38.5359292},
            opacity=0.6,
            labels={'taxa_100_hab':'Taxa de Internações po CSAP por mil/hab ', 'NOME': 'Bairro'}            
        )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_traces(hoverlabel=dict(bgcolor="white", font_size=15, font_family="Rockwell"))

        st.plotly_chart(fig)





        st.markdown("""---""")
        
        
        st.subheader("Dias de permanência de acordo com o Tipo de Leito")
        st.markdown('Média de dias de permanência de acordo com o tipo de leito.')
         
        #Criando um dataframe com o agrupamento da quantidade de internações de acordo com a data de internação
        dias_perman = pd.DataFrame(df_final.groupby(['ESPEC', 'sexo'])["DIAS_PERM"].mean())
        dias_perman = dias_perman.add_suffix('').reset_index()
        dias_perman['ESPEC'] = dias_perman['ESPEC'].map(str)
        dias_perman.info()
        
        #Substituindo os valores da coluna ESPEC por categorias de acordo com o dicionário de dados
        dias_perman = dias_perman.replace({'ESPEC':{"1":"Cirurgia", "2": "Obstetrícia", "3": "Clínica médica", "4": "Crônicos",
                                                    "5": "Psiquiatria", "6":"Pneumologia sanit.", "7":"Pediatria", 
                                                    "8":"Reabilitação", "9":"Hosp. dia (cirúrg.)", "10":"Hosp. dia (AIDS)", "11":"Hosp. dia (fibrose cística)",
                                                    "12":"Hosp. dia (intercor. pós transp. )", "13":"Hospital dia (geriatria)", "14":"Hospital dia (saúde mental)"}})
        dias_perman = dias_perman.sort_values(by = "DIAS_PERM", ascending = False)

        #Média de dias de permanência para cada tipo de leito hospitalar
        fig = px.box(dias_perman, x="DIAS_PERM", y="ESPEC")
        fig.update_traces(quartilemethod="linear",hovertemplate = None)
        st.plotly_chart(fig)
        
        
        st.markdown("""---""")

        st.subheader("Dias de permanência de acordo com o Sexo")
        st.markdown('Média de dias de permanência de acordo com o sexo do paciente.')
         
        ##################################     
        #Box_plot - Comparação de média de permanência entre os sexos.
        fig = px.box(dias_perman, x="sexo", y="DIAS_PERM", color = 'sexo')
        fig.update_traces(quartilemethod="linear") # or "inclusive", or "linear" by default
        st.plotly_chart(fig)
        