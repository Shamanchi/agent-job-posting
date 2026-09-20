"""Unit-тесты сопоставления: без сети, детерминированы."""

import pytest

from app.services.matcher import match
from app.services.skills import extract_skills


def test_extract_skills() -> None:
    assert extract_skills("Python FastAPI Docker k8s") == ["docker", "fastapi", "kubernetes", "python"]
    assert extract_skills("nothing here at all") == []


def test_match_scores() -> None:
    result = match("Python FastAPI Docker", "Python FastAPI SQL")
    assert result.match_score == 0.67
    assert result.matched == ["fastapi", "python"]
    assert result.missing == ["docker"]
    assert result.verdict == "fit"


def test_strong_verdict() -> None:
    result = match("Python SQL", "Python SQL Docker")
    assert result.match_score == 1.0
    assert result.verdict == "strong"


def test_weak_verdict() -> None:
    result = match("Python FastAPI Docker Kubernetes", "Python")
    assert result.match_score == 0.25
    assert result.verdict == "weak"


def test_explicit_required() -> None:
    result = match("anything", "I know Go", required_skills=["Go", "Rust"])
    assert result.required == ["go", "rust"]
    assert result.matched == ["go"]
    assert result.missing == ["rust"]


def test_bad_input_rejected() -> None:
    with pytest.raises(ValueError):
        match("", "Python resume")
    with pytest.raises(ValueError):
        match("Python job", "   ")
    with pytest.raises(ValueError):
        match("nothing here", "also nothing")
