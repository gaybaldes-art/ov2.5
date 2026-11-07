"""Deterministic baseline football probability engine.

This module accepts expected-goal inputs; it does not fetch or invent team data.
"""
from math import exp, factorial
from typing import Any


def _poisson_pmf(rate: float, goals: int) -> float:
    return exp(-rate) * rate**goals / factorial(goals)


def score_matrix(home_xg: float, away_xg: float, max_goals: int = 10) -> list[list[float]]:
    """Return a normalized independent-Poisson score probability matrix."""
    _validate_inputs(home_xg, away_xg, max_goals)
    home = [_poisson_pmf(home_xg, i) for i in range(max_goals + 1)]
    away = [_poisson_pmf(away_xg, i) for i in range(max_goals + 1)]
    matrix = [[h * a for a in away] for h in home]
    total = sum(map(sum, matrix))
    return [[p / total for p in row] for row in matrix]


def _validate_inputs(home_xg: float, away_xg: float, max_goals: int) -> None:
    if not (0 <= home_xg <= 8 and 0 <= away_xg <= 8):
        raise ValueError("Expected goals must be between 0 and 8.")
    if not (3 <= max_goals <= 20):
        raise ValueError("max_goals must be between 3 and 20.")


def forecast(home_xg: float, away_xg: float, max_goals: int = 10) -> dict[str, Any]:
    """Calculate 1X2, totals and BTTS from one shared score matrix."""
    matrix = score_matrix(home_xg, away_xg, max_goals)
    home_win = sum(matrix[h][a] for h in range(len(matrix)) for a in range(len(matrix)) if h > a)
    draw = sum(matrix[h][a] for h in range(len(matrix)) for a in range(len(matrix)) if h == a)
    away_win = sum(matrix[h][a] for h in range(len(matrix)) for a in range(len(matrix)) if h < a)
    over_25 = sum(matrix[h][a] for h in range(len(matrix)) for a in range(len(matrix)) if h + a >= 3)
    btts = sum(matrix[h][a] for h in range(1, len(matrix)) for a in range(1, len(matrix)))
    return {
        "model": "independent_poisson_baseline_v1",
        "inputs": {"home_xg": home_xg, "away_xg": away_xg, "max_goals": max_goals},
        "probabilities": {
            "home_win": round(home_win, 6),
            "draw": round(draw, 6),
            "away_win": round(away_win, 6),
            "over_2_5": round(over_25, 6),
            "under_2_5": round(1 - over_25, 6),
            "both_teams_to_score": round(btts, 6),
            "no_both_teams_to_score": round(1 - btts, 6),
        },
        "disclaimer": "Model estimates from supplied expected-goal inputs; not guarantees or betting advice.",
    }
