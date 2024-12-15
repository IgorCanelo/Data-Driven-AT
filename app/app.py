import streamlit as st
from funcoes_app import get_match, estatisticas_jogador
import plotly.express as px

# Configurações da página
st.set_page_config(layout="wide",
                   page_title="Football Matches App",
                   page_icon="⚽️")

# Título e descrição
st.title("Análise Futebol ⚽️")
st.write("Selecione abaixo os critérios escolhidos para obter análises aprofundadas das partidas de futebol!")

def init():
    # Selecionar ID da partida
    st.header("Selecione de ID de uma partida específica")
    id_selecionado = st.number_input(
        "Digite o ID (somente números):",
        min_value=0,
        format="%d"
    )
    st.write(f"Você selecionou o ID: {id_selecionado}")
    st.markdown("---")
    df = get_match(id_selecionado)
    if df.empty:
        st.warning("Selecione um ID de partida válido.")
    else:
        # Exibir DataFrame
        st.subheader("Detalhes da Partida")
        st.dataframe(df, height=400, use_container_width=True)
        df_shots = df[df['type'] == 'Shot'].groupby(['team', 'shot_outcome']).size().reset_index(name='count')
        fig_shots = px.bar(df_shots,
                        x='team',
                        y='count',
                        color='shot_outcome',
                        title='Finalizações por Time (Total e No Alvo)',
                        labels={'count': 'Quantidade de Finalizações', 'team': 'Time'},
                        barmode='group',
                        color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_shots)
        st.markdown("---")
        
        # Mostrar estatísticas de um jogador na partida selecionada
        if not df.empty:
            st.header("Selecione um jogador para visualizar as estatísticas básicas")
            lista_jogadores = df['player'].dropna().drop_duplicates().to_list()
            jogador_selecionado = st.selectbox('Escolha um jogador:', lista_jogadores)
            st.write(f'Jogador selecionado: {jogador_selecionado}')
            
            if jogador_selecionado:
                stats = estatisticas_jogador(id_selecionado, jogador_selecionado)

                # Título da seção
                st.subheader("📊 Estatísticas do Jogador")
                st.markdown(" ")

                # Ofensivas
                st.markdown("🟢 Estatísticas Ofensivas")
                col1, col2, col3 = st.columns(3)
                col1.metric("✅ Passes Completos", stats.get("passes_completed", 0))
                col2.metric("🎯 Passes Tentados", stats.get("passes_attempted", 0))
                col3.metric("⚽️ Chutes", stats.get("shots", 0))
                st.markdown("---")

                # Finalizações
                st.markdown("🔴 Estatísticas de Finalização")
                col1, col2, col3 = st.columns(3)
                col1.metric("🥅 Chutes no Alvo", stats.get("shots_on_target", 0))
                col2.metric("⚠️ Faltas Cometidas", stats.get("fouls_committed", 0))
                col3.metric("👍 Faltas Sofridas", stats.get("fouls_won", 0))
                st.markdown("---")

                # Defensivas
                st.markdown("🛡️ Estatísticas Defensivas")
                col1, col2, col3 = st.columns(3)
                col1.metric("🛑 Desarmes", stats.get("tackles", 0))
                col2.metric("🚧 Interceptações", stats.get("interceptions", 0))
                col3.metric("💨 Dribles Bem-Sucedidos", stats.get("dribbles_successful", 0))
                st.markdown("---")

                # Tentativas Gerais
                st.markdown("🔵 Tentativas Gerais")
                col1, col2, _ = st.columns(3)
                col1.metric("🔄 Tentativas de Dribles", stats.get("dribbles_attempted", 0))
                st.markdown("---")

            else:
                st.warning("Selecione um jogador para visualizar as estatísticas.")
    
    st.session_state.id_partida_init = id_selecionado 

def Main():
    init()

if __name__ == "__main__":
    Main()
