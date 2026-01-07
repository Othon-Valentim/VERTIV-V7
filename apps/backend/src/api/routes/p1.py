from fastapi import APIRouter, HTTPException
from src.domain.schemas import P1GarimpoInput, P1GarimpoOutput
from src.engine.p1_screener import P1ScreenerEngine

router = APIRouter(prefix="/p1", tags=["P1: Garimpo"])
engine = P1ScreenerEngine()


@router.post("/analyze", response_model=P1GarimpoOutput)
async def analyze_opportunity(data: P1GarimpoInput):
    """
    Analyzes a Land Opportunity (Garimpo) and returns a Go/No-Go decision.
    """
    try:
        result = engine.analyze(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
