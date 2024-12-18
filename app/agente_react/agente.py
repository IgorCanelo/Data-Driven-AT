from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
#from funcoes_app import get_match, estatisticas_jogador
from tools import get_match_tool, compare_players_tool


tools = [
    Tool(name="get_match_tool", func=get_match_tool, description="Consulta dados da partida. Passe apenas o ID da partida como um valor inteiro (ex: 3795221)."),
    Tool(name="compare_players_tool", func=compare_players_tool, description=""" Utilize sempre essa ferramenta quando for necessário obter dados.
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
    
Utilize as ferramentas para atingir respostas satisfatórias. 
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