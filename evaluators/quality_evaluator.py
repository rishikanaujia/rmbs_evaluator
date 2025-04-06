"""
Evaluates code quality of RMBS implementations
"""

import os
import re
from pathlib import Path
from typing import Tuple, List


def evaluate_code_quality(repo_path: Path) -> Tuple[float, str]:
    """
    Evaluate code quality using metrics like documentation, complexity

    Args:
        repo_path: Path to the repository

    Returns:
        Tuple of (score, notes)
    """
    code_file = repo_path / "credit_rating.py"

    if not code_file.exists():
        return 0, "No credit_rating.py file found"

    try:
        # Parse the python file
        with open(code_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # Metrics to track
        metrics = {
            'total_lines': len(lines),
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'function_count': 0,
            'class_count': 0,
            'docstring_count': 0,
            'avg_function_length': 0,
            'max_function_length': 0,
            'has_main_function': False,
            'validation_score': 0
        }

        # Count basic metrics
        in_multiline_comment = False
        current_function_lines = 0
        function_lines_list: List[int] = []

        for line in lines:
            stripped = line.strip()

            # Skip blank lines
            if not stripped:
                metrics['blank_lines'] += 1
                continue

            # Handle multiline comments/docstrings
            if in_multiline_comment:
                metrics['comment_lines'] += 1
                if '"""' in stripped or "'''" in stripped:
                    in_multiline_comment = False
                continue

            # Start of multiline comment/docstring
            if stripped.startswith('"""') or stripped.startswith("'''"):
                metrics['comment_lines'] += 1
                metrics['docstring_count'] += 1
                if not (stripped.endswith('"""') and len(stripped) > 3) and not (
                        stripped.endswith("'''") and len(stripped) > 3):
                    in_multiline_comment = True
                continue

            # Single line comments
            if stripped.startswith('#'):
                metrics['comment_lines'] += 1
                continue

            # Count actual code lines
            metrics['code_lines'] += 1

            # Detect function definitions
            if stripped.startswith('def '):
                metrics['function_count'] += 1
                if current_function_lines > 0:
                    function_lines_list.append(current_function_lines)
                current_function_lines = 0

                # Check for main function
                if 'def main(' in stripped or 'def calculate_credit_rating(' in stripped:
                    metrics['has_main_function'] = True
            else:
                current_function_lines += 1

            # Detect class definitions
            if stripped.startswith('class '):
                metrics['class_count'] += 1

        # Add the last function if there was one
        if current_function_lines > 0:
            function_lines_list.append(current_function_lines)

        # Calculate function length metrics
        if function_lines_list:
            metrics['avg_function_length'] = sum(function_lines_list) / len(function_lines_list)
            metrics['max_function_length'] = max(function_lines_list)

        # Check for input validation
        validation_patterns = [
            r'if\s+not\s+\w+',
            r'if\s+\w+\s+is\s+None',
            r'if\s+not\s+isinstance',
            r'if\s+len\(\w+\)',
            r'raise\s+\w+',
            r'try\s*:',
            r'except\s+',
            r'assert\s+'
        ]

        for pattern in validation_patterns:
            if re.search(pattern, content):
                metrics['validation_score'] += 0.5

        # Cap validation score at 2.5
        metrics['validation_score'] = min(2.5, metrics['validation_score'])

        # Calculate documentation score (out of 2.5)
        doc_score = 0

        # Check docstring ratio (at least one docstring per function/class is good)
        expected_docstrings = metrics['function_count'] + metrics['class_count']
        if expected_docstrings > 0:
            docstring_ratio = min(1.0, metrics['docstring_count'] / expected_docstrings)
            doc_score += docstring_ratio * 1.5

        # Check comment ratio (5-15% is a good range)
        if metrics['total_lines'] > 0:
            comment_ratio = metrics['comment_lines'] / metrics['total_lines']
            if 0.05 <= comment_ratio <= 0.20:
                doc_score += 1.0
            elif comment_ratio > 0:
                doc_score += 0.5

        # Calculate complexity score (out of 2.5)
        complexity_score = 0

        # Function length penalty (longer functions are more complex)
        if 5 <= metrics['avg_function_length'] <= 20:
            complexity_score += 1.25
        elif metrics['avg_function_length'] < 5:
            complexity_score += 0.5  # Too short may indicate poor organization
        else:
            # Penalty for very long functions: 0.0-1.0 points based on length
            complexity_score += max(0, 1.25 - (metrics['avg_function_length'] - 20) / 100)

        # Code organization bonus
        if metrics['class_count'] > 0 and metrics['function_count'] >= 3:
            complexity_score += 0.75
        elif metrics['function_count'] >= 3:
            complexity_score += 0.5

        # Has main function or entry point
        if metrics['has_main_function']:
            complexity_score += 0.5

        # Combine scores
        quality_score = doc_score + metrics['validation_score']

        # Prepare notes
        notes = [
            f"Lines: {metrics['total_lines']} total, {metrics['code_lines']} code, {metrics['comment_lines']} comments",
            f"Functions: {metrics['function_count']}, Avg length: {metrics['avg_function_length']:.1f} lines",
            f"Classes: {metrics['class_count']}, Docstrings: {metrics['docstring_count']}",
            f"Has validation: {'Yes' if metrics['validation_score'] > 0 else 'No'}"
        ]

        return quality_score, "; ".join(notes)

    except Exception as e:
        return 0, f"Error evaluating code quality: {str(e)}"