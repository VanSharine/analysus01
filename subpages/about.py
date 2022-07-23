import streamlit as st


def  about():
    st.title("Sobre")
    
    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        st.image('src/view/assets/image/logo.png',width = 130)
    with col_2:
        st.markdown('##### Equipe Outliers, pertencente ao Atlântico Academy Bootcamp.')
    with col_3:
        st.image('src/view/assets/image/academy-logo.png',width = 150)
    
    st.markdown("""---""")
    
    col_igor_1, col_igor_2, col_igor_3 = st.columns(3)
    with col_igor_1:
        st.image('src/view/assets/image/contact/igor.png',width = 100)
    with col_igor_2:
        st.subheader('Igor Duarte')
    with col_igor_3:
        st.markdown('Psicólogo; Trabalha com análise de dados de saúde pública.')
    
    st.markdown("""---""")
    
    col_josue_1, col_josue_2, col_josue_3 = st.columns(3)
    with col_josue_1:
        st.image('src/view/assets/image/contact/josue.png',width = 100)
    with col_josue_2:
        st.subheader('Josué Santos')
    with col_josue_3:
        st.markdown('Formado em Sistemas e Mídias Digitais. Trabalha como Desenvolvedor no Sistema Verdes Mares')
    
    st.markdown("""---""")
    
    col_vanessa_1, col_vanessa_2, col_vanessa_3 = st.columns(3)
    with col_vanessa_1:
        st.image('src/view/assets/image/contact/vanessa.png',width = 100)
    with col_vanessa_2:
        st.subheader('Vanessa Sharine Careaga Camelo')  
    with col_vanessa_3:
        st.markdown('Cientista de Dados; Trabalha como pesquisadora em Agile Vehicle Data Automation System na Ford')
