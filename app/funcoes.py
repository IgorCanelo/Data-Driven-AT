from statsbombpy import sb
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI

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
        dict: Um dicionário com DataFrames filtrados por tipo de evento.
    """

    times = df['team'].dropna().unique().tolist()
    time1, time2 = times
    gols = df[(df['type'] == 'Shot') & (df['shot_outcome'] == 'Goal')]
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
    print(eventos_principais)

    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyDUm58IAr5Ufp6kTw-HWRKnIoU0hBBI-qc")

    messages = f"""Analise o dicionário de informações fornecido sobre uma partida de futebol e elabore uma análise descritiva e textual detalhada. Certifique-se de:

    -Mencionar explicitamente os nomes dos times envolvidos.
    -Destacar os principais eventos da partida, como gols, cartões, substituições, chutes, assistências, faltas, defessas ou outros momentos importantes.
    -Jogadores não necessitam de nomes, caso necessário apenas se refira como jogador
    -Escrever de forma amigável, clara e envolvente, para que a saída seja agradável de ler.
    -Incluir observações sobre o desempenho dos times, jogadores de destaque, e o contexto geral da partida, caso relevante.
    -O texto deve estar no formato narrativo, como se estivesse contando a história da partida para um público leigo.

    Dados da partida: {eventos_principais}"""

    resposta = llm.invoke(messages).content

    return resposta


df = get_match(3795221)

resposta_v2 = contexto_eventos_principais(df)

print(resposta_v2)