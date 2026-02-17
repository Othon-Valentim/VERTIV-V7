from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from src.services.llm_service import LLMService
from src.infrastructure.auth import get_current_user, CurrentUser
from fastapi import Depends

router = APIRouter()


class AnalysisRequest(BaseModel):
    financial_data: Dict[str, Any]


class AnalysisResponse(BaseModel):
    thesis: str


@router.post("/analyze/thesis", response_model=AnalysisResponse)
async def generate_thesis(
    request: AnalysisRequest,
    user: CurrentUser = Depends(get_current_user)
):
    """
    Generates an investment thesis based on the provided financial JSON.
    """
    try:
        thesis = LLMService.generate_investment_thesis(request.financial_data)
        return AnalysisResponse(thesis=thesis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
