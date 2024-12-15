from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from funcoes_api import contexto_eventos_principais, get_match, estatisticas_jogador


# Pydantic Resumo
class MatchSummaryRequest(BaseModel):
    match_id: int

class MatchSummaryResponse(BaseModel):
    match_id: int
    match_summary: str


# Pydantic Stats
class PlayerProfileRequest(BaseModel):
    match_id: int
    player_name: str

class PlayerProfileResponse(BaseModel):
    player: str
    passes_completed: int
    passes_attempted: int
    shots: int
    shots_on_target: int
    fouls_committed: int
    fouls_won: int
    tackles: int
    interceptions: int
    dribbles_successful: int
    dribbles_attempted: int


app = FastAPI()


@app.post("/match_summary", response_model=MatchSummaryResponse)
async def match_summary(request: MatchSummaryRequest):
    try:
        df = get_match(request.match_id)
        resumo = contexto_eventos_principais(df)

        return MatchSummaryResponse(
            match_id=request.match_id,
            match_summary=resumo
        )

    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Dados da partida incorretos: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erro nos dados fornecidos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a partida: {str(e)}")


@app.post("/player_profile", response_model=PlayerProfileResponse)
async def player_profile(request: PlayerProfileRequest):
    try:
        estatisticas = estatisticas_jogador(request.match_id, request.player_name)

        return PlayerProfileResponse(**estatisticas)

    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Dados do jogador ou partida incorretos: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erro nos dados fornecidos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o perfil do jogador: {str(e)}")
