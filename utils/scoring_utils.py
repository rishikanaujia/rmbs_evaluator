"""
Utilities for score calculation and normalization
"""

from typing import Dict, List, Any


def calculate_weighted_score(scores: Dict[str, float], weights: Dict[str, float]) -> float:
    """
    Calculate a weighted score from component scores

    Args:
        scores: Dictionary of component scores
        weights: Dictionary of component weights

    Returns:
        Weighted total score
    """
    total_score = 0.0
    total_weight = 0.0

    for component, weight in weights.items():
        if component in scores:
            total_score += scores[component] * weight
            total_weight += weight

    # Normalize if weights don't sum to 1
    if total_weight > 0 and abs(total_weight - 1.0) > 1e-6:
        total_score /= total_weight

    return total_score


def normalize_score(score: float, min_score: float = 0.0, max_score: float = 5.0) -> float:
    """
    Normalize a score to be within a given range

    Args:
        score: Score to normalize
        min_score: Minimum score in the normalized range
        max_score: Maximum score in the normalized range

    Returns:
        Normalized score
    """
    return max(min_score, min(max_score, score))


def calculate_percentile_rank(results: List[Dict[str, Any]], score_key: str) -> Dict[str, float]:
    """
    Calculate percentile ranks for scores

    Args:
        results: List of result dictionaries
        score_key: Key for the score to rank

    Returns:
        Dictionary mapping repository names to percentile ranks
    """
    if not results:
        return {}

    # Extract scores
    scores = [(r["repo_name"], r.get(score_key, 0)) for r in results]

    # Sort by score (ascending)
    scores.sort(key=lambda x: x[1])

    # Calculate percentiles
    percentiles = {}
    total_repos = len(scores)

    for i, (repo_name, _) in enumerate(scores):
        percentile = (i / (total_repos - 1)) * 100 if total_repos > 1 else 50
        percentiles[repo_name] = percentile

    return percentiles


def generate_letter_grade(score: float, max_score: float = 5.0) -> str:
    """
    Convert a numeric score to a letter grade

    Args:
        score: Numeric score
        max_score: Maximum possible score

    Returns:
        Letter grade (A+, A, A-, B+, etc.)
    """
    # Normalize to 0-100 scale
    percent = (score / max_score) * 100

    if percent >= 97:
        return "A+"
    elif percent >= 93:
        return "A"
    elif percent >= 90:
        return "A-"
    elif percent >= 87:
        return "B+"
    elif percent >= 83:
        return "B"
    elif percent >= 80:
        return "B-"
    elif percent >= 77:
        return "C+"
    elif percent >= 73:
        return "C"
    elif percent >= 70:
        return "C-"
    elif percent >= 67:
        return "D+"
    elif percent >= 63:
        return "D"
    elif percent >= 60:
        return "D-"
    else:
        return "F"