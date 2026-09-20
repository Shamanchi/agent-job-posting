"""Эндпоинты сопоставления."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.config import Settings, get_settings
from app.services.matcher import MatchResult, match
from app.services.skills import known_skills

router = APIRouter()


class MatchRequest(BaseModel):
    job_description: str = Field(default="", max_length=10000)
    resume: str = Field(min_length=1, max_length=10000)
    required_skills: list[str] = Field(default_factory=list, max_length=100)


@router.get("/skills")
async def skills() -> dict:
    return {"skills": known_skills()}


@router.post("/match", response_model=MatchResult)
async def match_endpoint(
    request: MatchRequest,
    settings: Settings = Depends(get_settings),
) -> MatchResult:
    try:
        return match(
            request.job_description,
            request.resume,
            request.required_skills or None,
            strong_threshold=settings.strong_threshold,
            fit_threshold=settings.fit_threshold,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
