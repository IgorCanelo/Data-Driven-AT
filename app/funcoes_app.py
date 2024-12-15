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



def contexto_eventos_principais(df, estilo='formal'):
    """
    Identifica os principais eventos de uma partida de futebol. E passa para uma LLM realizar uma análise descritiva com base em uma narrativa
    
    Parâmetros:
        df (pd.DataFrame): DataFrame contendo os dados da partida.

    Retorna:
        dict: Um dicionário com DataFrames filtrados por tipo de evento.
    """

    if estilo == "formal":
        narrativa = """
        Formal: Torne a descrição mais objetiva e precisa, refletindo o tom sério. 
        
        Exemplo:
        "Uma partida marcada por equilíbrio técnico e decisões estratégicas. O resultado reflete o empenho das equipes e a importância do confronto no contexto do campeonato."
        """

    elif estilo == "humoristico":
        narrativa = """
        Humorístico: Utilize mais analogias engraçadas e inclua pequenos exageros para gerar humor. 
        
        Exemplo:
        "O campo parecia uma pista de dança, com dribles dignos de TikTok e algumas quedas que dariam um Oscar! No final, o placar foi só um detalhe; o show foi o verdadeiro prêmio."
        """

    elif estilo == "tecnico":
        narrativa = """
        Técnico: Insira análises detalhadas sobre táticas e estatísticas. 
        
        Exemplo:
        "O esquema tático 4-4-2 implementado pela equipe visitante contrastou com o 4-3-3 do time da casa, evidenciando o domínio do meio-campo através de triangulações e inversões de jogo."
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
    Você é um comentarista esportivo com especialidade em futebol. Responda como se estivesse apresentando uma análise envolvente para uma audiência de TV. 

    ⚠️ **Instrução Importante:** Mantenha o tom "{estilo}" em **todo o texto**, do início ao fim. Cada descrição, momento da partida ou análise deve refletir o tom escolhido pelo usuário, sem exceções. 
    Se o estilo for "humorístico", use expressões engraçadas, analogias divertidas e linguagem leve e inclusive emojis. 
    Se o estilo for 'tecnico', utilize palavras mais robustas e faça uma ánalise mais profunda e com muito mais detalhes. 
    Se o estilo for 'formal' utilize também palavras mais robustas e formais mas mantendo uma objetividade.
    Não "esqueça" o tom ao relatar os eventos da partida. Seu texto deve ser fluido e contínuo, sem dividir a análise em seções como "Visão Geral", "Momentos" ou "Conclusão". O objetivo é criar uma narrativa envolvente.

    **Aqui estão os detalhes que você deve incluir, mas de forma natural, em uma narrativa contínua:**
    - Descreva a importância do jogo (partida de liga, eliminatória, rivalidade, etc.), quando e onde o jogo aconteceu, o resultado final (a partir de: {gols}) e as implicações para os times.
    - Mencione jogadores-chave e os momentos mais marcantes da partida, sempre com o tom "{estilo}" escolhido.
    - Inclua quaisquer decisões surpreendentes ou ausências notáveis, mantendo a fluidez e o tom da narrativa.
    - Detalhe os momentos principais do jogo com a linguagem, estilo e tom correspondente ao que foi escolhido ("humorístico", "formal", "técnico").
    
    Aqui estão os eventos da partida que devem ser usados para criar sua narrativa:
    {eventos_principais}

    Placar:
    {gols}

    Comece a sua análise assim:

    **Inicio da análise:** "Olá a todos! Eu assisti à partida entre [Time da Casa] e [Time Visitante], o placar foi [Placar Time da Casa] contra [Placar Time Visitante]..."

    Lembre-se: cada trecho deve respeitar o estilo "{estilo}". Se for humorístico, faça a audiência rir! Se for formal, inspire com seriedade e objetividade. Se for técnico, detalhe com precisão. **Mantenha uma narrativa contínua e envolvente**, sem se preocupar com divisões tradicionais de seções.
    Exemplo de narrativa: {narrativa}
    """

    resposta = llm.invoke(messages).content

    return resposta

df = get_match(3795221)

print(contexto_eventos_principais(df, estilo='humoristico'))