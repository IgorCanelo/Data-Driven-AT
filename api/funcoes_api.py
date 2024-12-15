from statsbombpy import sb
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from datetime import timedelta

def get_match(match_id):
    """
    Retorna os eventos de uma partida específica.

    Parâmetros:
        match_id (int): O ID da partida.

    Retorna:
        pd.DataFrame: Um DataFrame contendo os dados da partida.
    """
    try:
        events = sb.events(match_id=match_id)
        
        if not events.empty:
            print(f"Dados da partida {match_id} carregados com sucesso!")
            return events
        else:
            print(f"Nenhum dado encontrado para o ID {match_id}")
            return pd.DataFrame()
    
    except Exception as e:
        print(f"Erro ao carregar os dados para o ID {match_id}: {e}")

        return pd.DataFrame()



def contexto_eventos_principais(df):
    """
    Identifica os principais eventos de uma partida de futebol. E passa para uma LLM realizar uma análise descritiva
    
    Parâmetros:
        df (pd.DataFrame): DataFrame contendo os dados da partida.

    Retorna:
        str: A análise feita pela LLM dos principais pontos do jogo.
    """
    gol_v1 = df[['team', 'shot_outcome']].dropna()
    gol = gol_v1[gol_v1['shot_outcome'] == 'Goal']

    times = df['team'].dropna().unique().tolist()
    time1, time2 = times
    gols = gol
    assistencias = df[df['pass_shot_assist'] == True]
    cartoes = df[df['foul_committed_card'].notnull()]
    substituicoes = df[df['type'] == 'Substitution']
    faltas = df[df['type'] == 'Foul Committed']
    faltas_sofridas = df[df['type'] == 'Foul Won']
    defesas = df[(df['type'] == 'Goal Keeper') & (df['goalkeeper_outcome'] == 'Saved')]
    chutes = df[df['type'] == 'Shot']

    eventos_principais = {
        'Times': f'{time1} vs {time2}',
        'Gols': gols,
        'Assistências': assistencias,
        'Cartões': cartoes,
        'Substituições': substituicoes,
        'Faltas Cometidas': faltas,
        'Faltas Sofridas': faltas_sofridas,
        'Defesas': defesas,
        'Chutes': chutes
    }

    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyDUm58IAr5Ufp6kTw-HWRKnIoU0hBBI-qc")

    messages = f"""
    Você é um comentarista esportivo com especialidade em futebol. Responda como se estivesse apresentando uma análise envolvente para uma audiência de TV. Aqui estão as informações a serem incluídas:

    Instruções:
    Visão Geral da Partida:

    -Descreva a importância do jogo (partida de liga, eliminatória, rivalidade, etc.).
    -Especifique quando e onde o jogo aconteceu.
    -Forneça o resultado final. Que está representado por essa tabela, onde tem o nome do time e o gol, caso necessite some para cada time e somente forneça o resultado final a partir de: {gols}
    -Destaque jogadores-chave e seus papéis.
    -Mencione quaisquer decisões surpreendentes ou ausências notáveis.

    Contexto e Perspectivas:

    -Explique as implicações mais amplas do jogo (rivalidade, classificação da liga ou enredos importantes).

    Entrega Envolvente:

    -Use um tom animado, profissional e informativo, tornando o comentário atraente para fãs de todos os níveis de conhecimento.
    
    Os detalhes da partida são fornecidos conforme a seguir:
    {eventos_principais}

    Placar:
    {gols}

    Ofereça uma análise especializada do jogo como se estivesse em uma transmissão esportiva.
    Comece a sua análise agora e envolva o público com suas percepções. O começo da análise deve começar assim:

    Inicio da análise: "Olá a todos! Eu assisti à partida entre [Time da Casa] e [Time Visitante], o placar foi [Placar Time da Casa] contra [Placar Time Visitante]..."
    """

    resposta = llm.invoke(messages).content

    return resposta


def estatisticas_jogador(match_id, player_name) -> str:
    """
    Cria um perfil detalhado de um jogador específico em uma partida.

    Parâmetros:
        match_id (int): ID da partida.
        player_name (str): Nome do jogador que será analisado.

    Retorna:
        dict: Dicionário com as estatísticas detalhadas do jogador.
    """
    try:
        events = sb.events(match_id=match_id)

        if events.empty:
            return {"Erro": "Nenhum evento encontrado para a partida."}

        player_events = events[events['player'] == player_name]

        if player_events.empty:
            return {"Erro": f"Jogador '{player_name}' não encontrado na partida {match_id}."}

        # Estatísticas
        estatisticas_jogador = {
            "player": player_name,
            "passes_completed": player_events[(player_events['type'] == 'Pass') & (player_events['pass_outcome'].isna())].shape[0],
            "passes_attempted": player_events[player_events['type'] == 'Pass'].shape[0],
            "shots": player_events[player_events['type'] == 'Shot'].shape[0],
            "shots_on_target": player_events[(player_events['type'] == 'Shot') & (player_events['shot_outcome'] == 'On Target')].shape[0],
            "fouls_committed": player_events[player_events['type'] == 'Foul Committed'].shape[0],
            "fouls_won": player_events[player_events['type'] == 'Foul Won'].shape[0],
            "tackles": player_events[player_events['type'] == 'Tackle'].shape[0],
            "interceptions": player_events[player_events['type'] == 'Interception'].shape[0],
            "dribbles_successful": player_events[(player_events['type'] == 'Dribble') & (player_events['dribble_outcome'] == 'Complete')].shape[0],
            "dribbles_attempted": player_events[player_events['type'] == 'Dribble'].shape[0],
        }

    except KeyError as e:
        return {"Erro": f"Erro na obtenção dos dados: {e}"}

    except Exception as e:
        return {"Erro": f"Ocorreu um erro inesperado: {e}"}
    
    return estatisticas_jogador
