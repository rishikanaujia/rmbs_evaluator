"""
Evaluates the structure and organization of RMBS repository
"""

from pathlib import Path
from typing import Tuple

from rmbs_evaluator.test_cases import EVALUATION_PARAMS


def evaluate_structure(repo_path: Path) -> Tuple[float, str]:
    """
    Check if the repository follows the required structure

    Args:
        repo_path: Path to the repository

    Returns:
        Tuple of (score, notes)
    """
    expected_files = EVALUATION_PARAMS["expected_files"]
    found_files = [f for f in expected_files if (repo_path / f).exists()]

    score = len(found_files) / len(expected_files) * 5  # Score out of 5

    # Create detailed notes
    notes = []
    notes.append(f"Found {len(found_files)}/{len(expected_files)} expected files")

    # List missing files
    missing_files = set(expected_files) - set(found_files)
    if missing_files:
        notes.append(f"Missing: {', '.join(missing_files)}")

    # Check for additional structure (bonus points)
    has_additional_structure = False
    for item in repo_path.iterdir():
        if item.is_dir() and item.name not in ['.git', '__pycache__', '.pytest_cache']:
            has_additional_structure = True
            notes.append(f"Additional directory structure: {item.name}")

    # Small bonus for having organized directories
    if has_additional_structure:
        bonus = min(0.5, len(found_files) * 0.1)  # Cap the bonus
        score = min(5.0, score + bonus)  # Cap the total score at 5
        notes.append(f"Structure bonus: +{bonus:.1f} points")

    return score, "; ".join(notes)