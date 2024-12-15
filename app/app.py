import streamlit as st
from funcoes_app import contexto_eventos_principais, get_match

st.set_page_config(layout="wide",
                   page_title="Football Matches App",
                   page_icon="⚽️")
st.title("Análise futebol")
st.write("Selecione abaixo os critérios escolhidos para obter análises aprofundadas das partidas de futebol!")

st.title("Seletor de ID")
id_selecionado = st.number_input(
    "Digite o ID (somente números):",
    min_value=0,  # Define o menor número permitido
    step=1,       # Incremento padrão ao usar os botões
    format="%d"   # Garante que apenas números inteiros são exibidos
)
# Mostra o valor inserido
st.write(f"Você selecionou o ID: {id_selecionado}")
df = get_match(id_selecionado)
st.dataframe(df)
