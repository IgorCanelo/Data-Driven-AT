from funcoes_app import get_match, estatisticas_jogador
from langchain.tools import tool

# Tool 1: Consulta de Partida
@tool("get_match_tool", return_direct=True)
def get_match_tool(match_id=None, **kwargs):
    """
    Retorna os dados da partida especificada em um DataFrame pandas.
    Argumentos:
        match_id: O ID da partida.
    """
    try:
        if match_id is None:
            return "Erro: O ID da partida não foi fornecido."
        
        # Garantir que match_id seja um número inteiro
        match_id = int(match_id)
        df = get_match(match_id)
        return df
    except ValueError:
        return "Erro: O ID da partida deve ser um número válido."
    except Exception as e:
        return f"Erro ao buscar os dados da partida: {str(e)}"


# Tool 2: Comparação de Jogadores
@tool("compare_players_tool", return_direct=True)
def compare_players_tool(player1=None, player2=None, match_id=None):
    """
    Compara as estatísticas de dois jogadores na partida especificada.
    Argumentos:
        player1 (str): Nome do primeiro jogador.
        player2 (str): Nome do segundo jogador.
        match_id (int): O ID da partida.
    Exemplos de input: player1="Declan Rice", player2="Harry Maguire", match_id="3795221"
    """
    input_str = player1.strip().replace('"', '')
    player1, player2, match_id = input_str.split(", ")

    player1 = player1.strip()
    player2 = player2.strip()
    match_id = match_id.strip()

    try:
        stats1 = estatisticas_jogador(int(match_id), str(player1))
        stats2 = estatisticas_jogador(int(match_id), str(player2))

        if not stats1 or not stats2:
            return "Estatísticas de um ou ambos os jogadores não encontradas."

        comparison = f"""
        Comparação entre {player1} e {player2} na partida {match_id}:
        
        {player1}:
        {stats1}

        {player2}:
        {stats2}
        """
        return comparison
    except Exception as e:
        return f"Erro ao comparar jogadores: {str(e)}"


