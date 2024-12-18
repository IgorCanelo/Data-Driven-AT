import streamlit as st
from funcoes_app import get_match, estatisticas_jogador, contexto_eventos_principais
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Configurações da página
st.set_page_config(layout="wide",
                   page_title="Football Matches App",
                   page_icon="⚽️")

# Título e descrição
st.title("Análise Futebol ⚽️")
st.write("Selecione abaixo os critérios escolhidos para obter análises aprofundadas das partidas de futebol!")

def init():
    # Selecionar ID da partida
    if "id_partida_init" in st.session_state:
        id_selecionado = st.number_input(
            "Digite o ID (somente números):",
            min_value=0,
            format="%d",
            value=st.session_state["id_partida_init"]
        )
    else:
        id_selecionado = st.number_input(
            "Digite o ID (somente números):",
            min_value=0,
            format="%d"
        )
    st.session_state["id_partida_init"] = id_selecionado
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


def narrativa():
    st.header("Selecione o ID de uma partida específica")

    if "id_partida_init" in st.session_state:
        id_selecionado = st.number_input(
            "Digite o ID (somente números):",
            min_value=0,
            format="%d",
            value=st.session_state["id_partida_init"]
        )
    else:
        id_selecionado = st.number_input(
            "Digite o ID (somente números):",
            min_value=0,
            format="%d"
        )

    st.session_state["id_partida_init"] = id_selecionado

    st.write(f"Você selecionou o ID: {id_selecionado}")
    st.markdown("---")

    df = get_match(id_selecionado)

    if df.empty:
        st.warning("Selecione um ID de partida válido.")
    else:
        st.header("Escolha o tipo de narrativa")
        estilo_usuario = st.selectbox(
            "Selecione o estilo desejado:",
            options=["Humorístico", "Formal", "Técnico"],
        )

        st.write(f"Você selecionou o estilo: **{estilo_usuario}**")

        if st.button("Gerar Narrativa"):

            narrativa = contexto_eventos_principais(df, estilo=estilo_usuario)
            st.markdown("### Narrativa Gerada:")
            st.write(narrativa)
        


def filtros():
    st.header("Selecione o ID de uma partida específica")

    if "id_partida_init" in st.session_state:
        id_selecionado = st.number_input(
            "Digite o ID (somente números):",
            min_value=0,
            format="%d",
            value=st.session_state["id_partida_init"]
        )
    else:
        id_selecionado = st.number_input(
            "Digite o ID (somente números):",
            min_value=0,
            format="%d"
        )

    st.session_state["id_partida_init"] = id_selecionado

    st.write(f"Você selecionou o ID: {id_selecionado}")
    st.markdown("---")

    df = get_match(id_selecionado)

    if df.empty:
        st.warning("Selecione um ID de partida válido.")
    else:
        st.header("Exploração de Dados com Filtros Dinâmicos")
        colunas_padrao = ["player", "team", "pass_type", "shot_end_location"]
        colunas_selecionadas = st.multiselect(
            "Selecione as colunas que deseja visualizar:",
            options=df.columns,
            default=colunas_padrao,
            )

        df_filtrado = df[colunas_selecionadas]

        st.subheader("Tabela Filtrada")
        st.dataframe(df_filtrado)
        graficos()


def graficos():
    st.header("Visualização de Estatísticas dos Jogadores")
    
    id_atual = st.session_state.get("id_partida_init", None)
    if id_atual is None:
        st.error("ID da partida não definido.")
        return
    
    df_graficos = get_match(id_atual)

    
    players = df_graficos['player'].dropna().unique()
    player = st.selectbox("Selecione o jogador:", players)
    df_player = df_graficos[df_graficos['player'] == player]

    # Cálculo de estatísticas
    df_passes_completos = df_player[(df_player['type'] == 'Pass') & (df_player['pass_outcome'].isna())].shape[0]
    df_passes_incompletos = df_player[df_player['type'] == 'Pass'].shape[0] - df_passes_completos
    df_chutes = df_player[df_player['type'] == 'Shot'].shape[0]
    df_chutes_alvo = df_player[(df_player['type'] == 'Shot') & (df_player['shot_outcome'] == 'On Target')].shape[0]
    df_faltas_cometidas = df_player[df_player['type'] == 'Foul Committed'].shape[0]
    df_faltas_sofridas = df_player[df_player['type'] == 'Foul Won'].shape[0]
    df_tomada_bola = df_player[df_player['type'] == 'Tackle'].shape[0]
    df_interceptacao = df_player[df_player['type'] == 'Interception'].shape[0]
    df_dribles = df_player[(df_player['type'] == 'Dribble') & (df_player['dribble_outcome'] == 'Complete')].shape[0]
    df_dribles_incompletos = df_player[df_player['type'] == 'Dribble'].shape[0] - df_dribles

    # Gráficos
    st.subheader(f"Estatísticas de {player}")
    st.markdown("### Passes")
    fig_passes = px.bar(
        x=['Completos', 'Incompletos'],
        y=[df_passes_completos, df_passes_incompletos],
        labels={'x': 'Tipo de Passe', 'y': 'Quantidade'},
        title='Passes Completos vs Incompletos',
        color=['Completos', 'Incompletos'],
        color_discrete_sequence=['#636EFA', '#EF553B']
    )
    st.plotly_chart(fig_passes)

    # Gráfico de pizza para chutes
    st.markdown("### Chutes")
    fig_chutes = px.pie(
        values=[df_chutes_alvo, df_chutes - df_chutes_alvo],
        names=['No Alvo', 'Fora do Alvo'],
        title='Distribuição de Chutes',
        color=['No Alvo', 'Fora do Alvo'],
        color_discrete_sequence=['#636EFA', '#EF553B']
    )
    st.plotly_chart(fig_chutes)

    # Gráfico de barras para faltas
    st.markdown("### Faltas")
    fig_faltas = px.bar(
        x=['Cometidas', 'Sofridas'],
        y=[df_faltas_cometidas, df_faltas_sofridas],
        labels={'x': 'Tipo de Faltas', 'y': 'Quantidade'},
        title='Faltas Cometidas vs Sofridas',
        color=['Cometidas', 'Sofridas'],
        color_discrete_sequence=['#636EFA', '#EF553B']
    )
    st.plotly_chart(fig_faltas)

    # Gráfico de barras para outras ações
    st.markdown("### Outras Ações")
    fig_acoes = px.bar(
        x=['Tomadas de Bola', 'Interceptações', 'Dribles Completos', 'Dribles Incompletos'],
        y=[df_tomada_bola, df_interceptacao, df_dribles, df_dribles_incompletos],
        labels={'x': 'Ação', 'y': 'Quantidade'},
        title='Outras Ações do Jogo',
        color=['Tomadas de Bola', 'Interceptações', 'Dribles Completos', 'Dribles Incompletos'],
        color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96', '#AB63FA']
    )
    st.plotly_chart(fig_acoes)



def comparacao():
    st.header("Comparação entre dois Jogadores")
    
    if "id_partida_init" in st.session_state:
        id_selecionado = st.number_input(
            "Digite o ID (somente números):",
            min_value=0,
            format="%d",
            value=st.session_state["id_partida_init"]
        )
    else:
        id_selecionado = st.number_input(
            "Digite o ID (somente números):",
            min_value=0,
            format="%d"
        )

    st.session_state["id_partida_init"] = id_selecionado

    st.write(f"Você selecionou o ID: {id_selecionado}")
    st.markdown("---")

    df = get_match(id_selecionado)

    if df.empty:
        st.warning("Selecione um ID de partida válido.")
    else:
        df_graficos = df
        
        players = df_graficos['player'].dropna().unique()
        player_1 = st.selectbox("Selecione o primeiro jogador:", players)
        player_2 = st.selectbox("Selecione o segundo jogador:", players)
        st.markdown("---")

        if player_1 == player_2:
            st.warning("Selecione jogadores diferentes para comparação")
        else:
        
            estatisticas_jogador_1 = estatisticas_jogador(id_selecionado, player_1)
            estatisticas_jogador_2 = estatisticas_jogador(id_selecionado, player_2)

            categorias = [
                "Passes Completos", "Passes Incompletos", 
                "Chutes", "Chutes no Alvo", 
                "Faltas Cometidas", "Faltas Sofridas", 
                "Tomadas de Bola", "Interceptações", 
                "Dribles Completos", "Dribles Incompletos"
            ]
            
            valores_jogador_1 = [
                estatisticas_jogador_1['passes_completed'], 
                estatisticas_jogador_1['passes_attempted'] - estatisticas_jogador_1['passes_completed'], 
                estatisticas_jogador_1['shots'], estatisticas_jogador_1['shots_on_target'], 
                estatisticas_jogador_1['fouls_committed'], estatisticas_jogador_1['fouls_won'], 
                estatisticas_jogador_1['tackles'], estatisticas_jogador_1['interceptions'], 
                estatisticas_jogador_1['dribbles_successful'], 
                estatisticas_jogador_1['dribbles_attempted'] - estatisticas_jogador_1['dribbles_successful']
            ]
            
            valores_jogador_2 = [
                estatisticas_jogador_2['passes_completed'], 
                estatisticas_jogador_2['passes_attempted'] - estatisticas_jogador_2['passes_completed'], 
                estatisticas_jogador_2['shots'], estatisticas_jogador_2['shots_on_target'], 
                estatisticas_jogador_2['fouls_committed'], estatisticas_jogador_2['fouls_won'], 
                estatisticas_jogador_2['tackles'], estatisticas_jogador_2['interceptions'], 
                estatisticas_jogador_2['dribbles_successful'], 
                estatisticas_jogador_2['dribbles_attempted'] - estatisticas_jogador_2['dribbles_successful']
            ]
            
            # Gráfico comparativo para cada categoria
            for i, categoria in enumerate(categorias):
                st.subheader(categoria)

                df_temp = pd.DataFrame({
                    'Jogador': [player_1, player_2],
                    'Quantidade': [valores_jogador_1[i], valores_jogador_2[i]]
                })
                
                fig = px.bar(
                    df_temp,
                    x='Jogador',
                    y='Quantidade',
                    labels={'x': 'Jogador', 'y': 'Quantidade'},
                    color='Jogador',
                    color_discrete_sequence=['#636EFA', '#EF553B']
                )
                
                st.plotly_chart(fig, key=f"fig_{categoria}")
                st.markdown("---")



##################################################### PAGINAS ############################################################################

def pagina_inicial():
    init()

def narrativa_personalizada():
    narrativa()

def analise_exploratoria():
    filtros()
    #graficos()

def comparacao_jogadores():
    comparacao()

def Main():
    st.sidebar.title("Navegação")

    if "pagina_selecionada" not in st.session_state:
        st.session_state["pagina_selecionada"] = "Página Inicial"


    if st.sidebar.button("Página Inicial"):
        st.session_state["pagina_selecionada"] = "Página Inicial"
    if st.sidebar.button("Narrativa Personalizada"):
        st.session_state["pagina_selecionada"] = "Narrativa Personalizada"
    if st.sidebar.button("Análise Exploratória"):
        st.session_state["pagina_selecionada"] = "Análise Exploratória"
    if st.sidebar.button("Comparação Jogadores"):
        st.session_state["pagina_selecionada"] = "Comparação Jogadores"
   
    # Navegação condicional com base no estado da sessão
    if st.session_state["pagina_selecionada"] == "Página Inicial":
        pagina_inicial()
    elif st.session_state["pagina_selecionada"] == "Narrativa Personalizada":
        narrativa_personalizada()
    elif st.session_state["pagina_selecionada"] == "Análise Exploratória":
        analise_exploratoria()
    elif st.session_state["pagina_selecionada"] == "Comparação Jogadores":
        comparacao_jogadores()


if __name__ == "__main__":
    Main()
