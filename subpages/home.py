import streamlit as st


def home():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##")
        st.subheader(f"Predição de Internações SUS")

    with col2:
        st.image('src/view/assets/image/header.png', width = 250)

    st.image('src/view/assets/image/logo2.png', width = 200)

    st.markdown("A Atenção Primária à Saúde (APS) é o primeiro nível de atenção em saúde e se caracteriza por um conjunto de ações de saúde, no âmbito individual e coletivo, que abrange a promoção e a proteção da saúde, a prevenção de agravos, o diagnóstico, o tratamento, a reabilitação, a redução de danos e a manutenção da saúde com o objetivo de desenvolver uma atenção integral que impacte positivamente na situação de saúde das coletividades. Trata-se da principal porta de entrada do SUS e do centro de comunicação com toda a Rede de Atenção dos SUS.")
    st.markdown("O foco na atenção primária se torna um dos pontos principais na logística de recursos e atendimento. Já que evitando que enfermidades venham a se agravar, estaremos evitando a ocupação de leitos de internações, aliviando todo o sistema em cadeia.")
    st.markdown("**Objetivos**")
    st.markdown("Observando o poder computacional de auxílio na tomada de decisão, este projeto visa analisar os dados referentes às internações do SUS, levantando informações pertinentes para a melhoria no atendimento na atenção primária.")
    st.markdown("Utilizando-se de métodos preditivos de análise de dados é pretendido realizar um apontamento prévio com poucas informações iniciais no momento do atendimento primário, podendo sugerir uma maior prioridade em casos de maior probabilidade de uma futura internação.")
