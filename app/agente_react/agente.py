from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
#from funcoes_app import get_match, estatisticas_jogador
from tools import get_match_tool, compare_players_tool


tools = [
    Tool(name="get_match_tool", func=get_match_tool, description="Consulta dados da partida. Passe apenas o ID da partida como um valor inteiro (ex: 3795221)."),
    Tool(name="compare_players_tool", func=compare_players_tool, description="""
        Compara as estatísticas de dois jogadores na partida especificada.
        Argumentos:
            player1 (str): Nome do primeiro jogador.
            player2 (str): Nome do segundo jogador.
            match_id (int): O ID da partida.
         Exemplo de argumentos a serem passados: "Declan Rice", "Harry Maguire", 3795221
         Utilize o exemplo como base de inputs para a função
        """)
]



llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyDUm58IAr5Ufp6kTw-HWRKnIoU0hBBI-qc")


# Inicializa o Agente
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

contexto = """
Você é um especialista em futebol que possui duas ferramentas para busca de dados e responder perguntas sobre futebol
Tools:
    get_match_tool - Serve para obter dados apenas
    compare_players_tool - Serve para obter estatisticas de dois jogadores

Utilize as ferramentas para atingir respostas satisfatórias. Os dados obtidos com suas respectivas colunas, são as: ['ball_receipt_outcome', 'ball_recovery_recovery_failure',
       'block_deflection', 'carry_end_location', 'clearance_aerial_won',
       'clearance_body_part', 'clearance_head', 'clearance_left_foot',
       'clearance_right_foot', 'counterpress', 'dribble_outcome',
       'duel_outcome', 'duel_type', 'duration', 'foul_committed_advantage',
       'foul_committed_card', 'foul_committed_offensive',
       'foul_committed_penalty', 'foul_committed_type', 'foul_won_advantage',
       'foul_won_defensive', 'foul_won_penalty', 'goalkeeper_body_part',
       'goalkeeper_end_location', 'goalkeeper_outcome', 'goalkeeper_position',
       'goalkeeper_punched_out', 'goalkeeper_shot_saved_off_target',
       'goalkeeper_technique', 'goalkeeper_type', 'id', 'index',
       'injury_stoppage_in_chain', 'interception_outcome', 'location',
       'match_id', 'minute', 'miscontrol_aerial_won', 'off_camera', 'out',
       'pass_aerial_won', 'pass_angle', 'pass_assisted_shot_id',
       'pass_body_part', 'pass_cross', 'pass_cut_back', 'pass_deflected',
       'pass_end_location', 'pass_height', 'pass_inswinging', 'pass_length',
       'pass_miscommunication', 'pass_no_touch', 'pass_outcome',
       'pass_outswinging', 'pass_recipient', 'pass_recipient_id',
       'pass_shot_assist', 'pass_switch', 'pass_technique',
       'pass_through_ball', 'pass_type', 'period', 'play_pattern', 'player',
       'player_id', 'player_off_permanent', 'position', 'possession',
       'possession_team', 'possession_team_id', 'related_events', 'second',
       'shot_aerial_won', 'shot_body_part', 'shot_end_location',
       'shot_first_time', 'shot_freeze_frame', 'shot_key_pass_id',
       'shot_one_on_one', 'shot_outcome', 'shot_saved_off_target',
       'shot_statsbomb_xg', 'shot_technique', 'shot_type',
       'substitution_outcome', 'substitution_outcome_id',
       'substitution_replacement', 'substitution_replacement_id', 'tactics',
       'team', 'team_id', 'timestamp', 'type', 'under_pressure']
    Utilize-as para obter dados relevantes para assim conseguir responder qualquer tipo de pergunta relacionada a futebol.
    Caso precise utilize a tool compare_players_tool, para obter statisticas sobre jogadores
"""
query = f"""
{contexto}
Qual jogador teve mais finalizações no primeiro tempo da partida 3795221?
"""
response = agent.invoke({"input": query})
# response = agent.invoke(query)

print(response)

#Com base na partida 3795221, realize a comparação entre Declan Rice e Harry Maguire.