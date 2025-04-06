"""
Evaluates test quality and code coverage for RMBS implementations
"""

import os
import sys
import pytest
import coverage
from pathlib import Path
from typing import Tuple


def evaluate_tests(repo_path: Path) -> Tuple[float, str, float]:
    """
    Run tests if they exist and measure coverage

    Args:
        repo_path: Path to the repository

    Returns:
        Tuple of (score, notes, coverage_percentage)
    """
    test_file = repo_path / "test_credit_rating.py"

    if not test_file.exists():
        return 0, "No test file found", 0

    # Store original directory to restore later
    original_dir = os.getcwd()

    try:
        # Change to repo directory
        os.chdir(repo_path)

        # Set up coverage
        cov = coverage.Coverage()
        cov.start()

        # Capture test output
        class CaptureOutput:
            def __init__(self):
                self.output = []

            def write(self, text):
                self.output.append(text)

            def flush(self):
                pass

        capture = CaptureOutput()
        sys.stdout = capture

        # Run tests
        result = pytest.main(["-xvs", str(test_file)])

        # Restore stdout
        sys.stdout = sys.__stdout__

        cov.stop()
        cov.save()

        # Analyze test output
        test_output = "".join(capture.output)
        passed_count = test_output.count("PASSED")
        failed_count = test_output.count("FAILED")
        error_count = test_output.count("ERROR")
        total_tests = passed_count + failed_count + error_count

        # Calculate coverage percentage
        total_lines = 0
        covered_lines = 0

        credit_rating_file = repo_path / "credit_rating.py"
        if credit_rating_file.exists():
            analysis = cov.analysis(str(credit_rating_file))
            total_lines = len(analysis[1]) + len(analysis[2])  # Covered + missing lines
            covered_lines = len(analysis[1])

        coverage_pct = (covered_lines / total_lines * 100) if total_lines > 0 else 0

        # Calculate test score based on test count, success rate, and coverage
        # Maximum 5 points: 2.5 for tests passing and 2.5 for coverage
        if total_tests == 0:
            test_score = 0
            test_status = "No tests were run"
        else:
            success_rate = passed_count / total_tests
            test_points = min(2.5, success_rate * 2.5)
            coverage_points = min(2.5, coverage_pct / 100 * 2.5)
            test_score = test_points + coverage_points

            test_status = f"Tests: {passed_count} passed, {failed_count} failed, {error_count} errors"

        notes = f"{test_status}, Coverage: {coverage_pct:.2f}%"

        # Check for test variety
        with open(test_file, 'r') as f:
            test_content = f.read()

        # Check for different types of test cases
        has_edge_cases = any(
            term in test_content.lower() for term in ["edge case", "corner case", "special case", "error case"])
        has_invalid_input = any(
            term in test_content.lower() for term in ["invalid", "none", "null", "empty", "missing", "error"])

        test_variety = []
        if has_edge_cases:
            test_variety.append("edge cases")
        if has_invalid_input:
            test_variety.append("invalid inputs")

        if test_variety:
            notes += f"; Tests include: {', '.join(test_variety)}"

        return test_score, notes, coverage_pct

    except Exception as e:
        return 0, f"Error running tests: {str(e)}", 0

    finally:
        # Return to original directory
        os.chdir(original_dir)