import streamlit as st
from PIL import Image

from src.view.partials.navbar import streamlit_menu

from src.view.subpages.about import about
from src.view.subpages.predict import predict
from src.view.subpages.analytics_explore import analytics_explore
from src.view.subpages.datasus import datasus
from src.view.subpages.home import home


def main():
    favicon = Image.open('src/view/assets/image/favicon.png')
    st.set_page_config(page_title='Outliers - Analysus', page_icon=favicon)
    
    selected = streamlit_menu()

    if selected == "Home":
        home()
        
    if selected == "DataSUS":
        datasus()

    if selected == "Análise Exploratória":
        analytics_explore()

    if selected == "Predição":
        predict()

    if selected == "Sobre nós":
        about()
        
if __name__ == '__main__':
    main()
