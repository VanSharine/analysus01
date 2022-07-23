import streamlit as st
from streamlit_option_menu import option_menu


menu = [
    "Home",
    "DataSUS",
    "Análise Exploratória",
    "Predição",
    "Sobre nós"
]

icons = [
    "house",
    "archive",
    "file-bar-graph",
    "calendar2-x",
    "book"
]

def streamlit_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu Principal",
            options=menu,  
            icons=icons,  
            menu_icon="cast",
            default_index=0
        )
        
        return selected
