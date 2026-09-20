"""Словарь навыков и извлечение из текста. Без сети."""

from __future__ import annotations

import re

SKILLS = [
    "python", "fastapi", "django", "flask", "sql", "postgres", "redis",
    "docker", "kubernetes", "terraform", "aws", "azure", "gcp",
    "react", "typescript", "javascript", "vue", "angular",
    "java", "kotlin", "go", "rust", "c++",
    "pandas", "numpy", "pytorch", "tensorflow", "scikit-learn",
    "git", "linux", "nginx", "rabbitmq", "kafka", "graphql", "rest",
]

_TOKEN_RE = re.compile(r"[a-zA-Z0-9+#]+")


def extract_skills(text: str) -> list[str]:
    """Найти известные навыки в тексте. Детерминировано."""
    tokens = {token.lower() for token in _TOKEN_RE.findall(text)}
    # Нормализация частых написаний.
    normalized = set(tokens)
    if "postgresql" in tokens:
        normalized.add("postgres")
    if "k8s" in tokens:
        normalized.add("kubernetes")
    if "js" in tokens:
        normalized.add("javascript")
    if "ts" in tokens:
        normalized.add("typescript")
    return sorted(skill for skill in SKILLS if skill in normalized)


def known_skills() -> list[str]:
    return list(SKILLS)
