"""Сопоставление вакансии и резюме."""

from __future__ import annotations

from pydantic import BaseModel

from app.services.skills import extract_skills


class MatchResult(BaseModel):
    required: list[str]
    resume_skills: list[str]
    matched: list[str]
    missing: list[str]
    match_score: float
    verdict: str


def match(
    job_description: str,
    resume: str,
    required_skills: list[str] | None = None,
    strong_threshold: float = 0.8,
    fit_threshold: float = 0.5,
) -> MatchResult:
    """Посчитать соответствие. Детерминировано."""
    if not job_description.strip() and not (required_skills or []):
        raise ValueError("job_description or required_skills must be given")
    if not resume.strip():
        raise ValueError("resume must not be empty")
    if required_skills:
        required = sorted({skill.strip().lower() for skill in required_skills if skill.strip()})
    else:
        required = extract_skills(job_description)
    if not required:
        raise ValueError("no known skills found in job description")
    resume_skills = extract_skills(resume)
    resume_set = set(resume_skills)
    matched = sorted(skill for skill in required if skill in resume_set)
    missing = sorted(skill for skill in required if skill not in resume_set)
    score = round(len(matched) / len(required), 2)
    if score >= strong_threshold:
        verdict = "strong"
    elif score >= fit_threshold:
        verdict = "fit"
    else:
        verdict = "weak"
    return MatchResult(
        required=required,
        resume_skills=resume_skills,
        matched=matched,
        missing=missing,
        match_score=score,
        verdict=verdict,
    )
