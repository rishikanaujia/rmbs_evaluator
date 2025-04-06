"""
Evaluates documentation quality of RMBS implementations
"""

import re
from pathlib import Path
from typing import Tuple, Dict


def evaluate_documentation(repo_path: Path) -> Tuple[float, str]:
    """
    Evaluate documentation quality

    Args:
        repo_path: Path to the repository

    Returns:
        Tuple of (score, notes)
    """
    readme_file = repo_path / "README.md"

    if not readme_file.exists():
        return 0, "No README.md file found"

    try:
        with open(readme_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Calculate metrics
        metrics = {
            'length': len(content),
            'sections': 0,
            'code_blocks': 0,
            'has_installation': False,
            'has_usage': False,
            'has_examples': False,
            'has_architecture': False,
            'has_testing': False,
            'formatting_quality': 0
        }

        # Count sections (headers)
        header_pattern = r'^#+\s+.+$'
        metrics['sections'] = len(re.findall(header_pattern, content, re.MULTILINE))

        # Count code blocks
        code_block_pattern = r'```[\w]*[\s\S]*?```'
        metrics['code_blocks'] = len(re.findall(code_block_pattern, content))

        # Check for specific sections
        metrics['has_installation'] = any(
            term in content.lower() for term in ['installation', 'setup', 'getting started'])
        metrics['has_usage'] = any(term in content.lower() for term in ['usage', 'how to use', 'user guide'])
        metrics['has_examples'] = any(
            term in content.lower() for term in ['example', 'sample', 'demonstration', 'demo']) or '```' in content
        metrics['has_architecture'] = any(
            term in content.lower() for term in ['architecture', 'design', 'structure', 'implementation', 'approach'])
        metrics['has_testing'] = any(term in content.lower() for term in ['test', 'coverage', 'quality'])

        # Check formatting quality
        if metrics['sections'] >= 3:
            metrics['formatting_quality'] += 1

        if metrics['code_blocks'] >= 1:
            metrics['formatting_quality'] += 0.5

        # Check for lists
        list_pattern = r'^\s*[-*]\s+.+$'
        has_lists = len(re.findall(list_pattern, content, re.MULTILINE)) > 2
        if has_lists:
            metrics['formatting_quality'] += 0.5

        # Calculate component scores

        # Content completeness (out of 3)
        content_score = sum([
            metrics['has_installation'],
            metrics['has_usage'],
            metrics['has_examples'],
            metrics['has_architecture'],
            metrics['has_testing']
        ]) * 0.6

        # Length score (out of 1)
        # Ideal README is between 500-3000 chars
        if metrics['length'] < 200:
            length_score = metrics['length'] / 200 * 0.5
        elif metrics['length'] <= 3000:
            length_score = 1.0
        else:
            # Slight penalty for excessive length
            length_score = max(0.5, 1.0 - (metrics['length'] - 3000) / 10000)

        # Formatting score (out of 1)
        formatting_score = metrics['formatting_quality']

        # Total score (out of 5)
        total_score = content_score + length_score + formatting_score

        # Prepare notes
        present_sections = []
        if metrics['has_installation']:
            present_sections.append("Installation")
        if metrics['has_usage']:
            present_sections.append("Usage")
        if metrics['has_examples']:
            present_sections.append("Examples")
        if metrics['has_architecture']:
            present_sections.append("Architecture/Design")
        if metrics['has_testing']:
            present_sections.append("Testing")

        sections_note = ", ".join(present_sections) if present_sections else "None"

        notes = [
            f"Length: {metrics['length']} chars",
            f"Sections: {metrics['sections']}, Code blocks: {metrics['code_blocks']}",
            f"Key sections: {sections_note}"
        ]

        return total_score, "; ".join(notes)

    except Exception as e:
        return 0, f"Error evaluating documentation: {str(e)}"