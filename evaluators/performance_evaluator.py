"""
Evaluates the performance of RMBS credit rating implementation
"""

import sys
import time
import importlib.util
from pathlib import Path
from typing import Dict, Tuple, Any


def evaluate_performance(repo_path: Path, test_cases: Dict[str, Dict[str, Any]]) -> Tuple[float, str]:
    """
    Test performance with large datasets

    Args:
        repo_path: Path to the repository
        test_cases: Dictionary of test cases

    Returns:
        Tuple of (score, notes)
    """
    try:
        # Import the candidate's module
        sys.path.insert(0, str(repo_path))
        spec = importlib.util.spec_from_file_location("credit_rating", repo_path / "credit_rating.py")

        if not spec or not spec.loader:
            return 0, "Could not load credit_rating.py"

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Get the large test case
        large_case = test_cases.get("large_case", {}).get("input", {})

        # Try to find and execute the main function
        execution_time = None

        if hasattr(module, 'calculate_credit_rating'):
            # Warm-up run to handle any initialization overhead
            module.calculate_credit_rating(large_case)

            # Timed run
            start_time = time.time()
            module.calculate_credit_rating(large_case)
            execution_time = time.time() - start_time
        else:
            # Try to find a function that takes a dictionary input
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr) and not attr_name.startswith('_'):
                    try:
                        # Warm-up run
                        attr(large_case)

                        # Timed run
                        start_time = time.time()
                        attr(large_case)
                        execution_time = time.time() - start_time
                        break
                    except Exception:
                        continue

        # Clean up path
        if sys.path and str(repo_path) == sys.path[0]:
            sys.path.pop(0)

        if execution_time is not None:
            # Define performance benchmarks
            excellent_time = 0.1  # Under 100ms is excellent
            good_time = 0.5  # Under 500ms is good
            acceptable_time = 2.0  # Under 2 seconds is acceptable

            # Score based on execution time
            if execution_time < excellent_time:
                score = 5.0
                performance_rating = "Excellent"
            elif execution_time < good_time:
                score = 4.0
                performance_rating = "Good"
            elif execution_time < acceptable_time:
                score = 3.0
                performance_rating = "Acceptable"
            else:
                # Gradually decrease score for slower performance
                score = max(1.0, 3.0 - (execution_time - acceptable_time) / 2)
                performance_rating = "Needs improvement"

            notes = f"Execution time for 1000 mortgages: {execution_time:.4f} seconds ({performance_rating})"
        else:
            score = 0
            notes = "Could not measure performance - no suitable function found"

        return score, notes

    except Exception as e:
        # Clean up path
        if sys.path and str(repo_path) == sys.path[0]:
            sys.path.pop(0)

        return 0, f"Error testing performance: {str(e)}"