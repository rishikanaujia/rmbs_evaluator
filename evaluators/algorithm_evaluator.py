"""
Evaluates the correctness of RMBS credit rating algorithm implementation
"""

import sys
import importlib.util
from pathlib import Path
from typing import Dict, Tuple, Any


def evaluate_algorithm(repo_path: Path, test_cases: Dict[str, Dict[str, Any]]) -> Tuple[float, str]:
    """
    Check if the algorithm produces correct results for test cases

    Args:
        repo_path: Path to the repository
        test_cases: Dictionary of test cases with expected outputs

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

        correct_test_cases = 0
        total_test_cases = 0
        test_notes = []

        # Exclude cases marked for performance testing only
        for case_name, case_data in test_cases.items():
            if case_name == "large_case":
                continue  # Skip large case for correctness testing

            total_test_cases += 1
            input_data = case_data["input"]
            expected = case_data["expected_output"]

            try:
                # Try to find and call the appropriate function
                if hasattr(module, 'calculate_credit_rating'):
                    result = module.calculate_credit_rating(input_data)

                    # For empty case, we're just checking it doesn't crash
                    if case_name == "edge_case_empty":
                        correct_test_cases += 1
                        test_notes.append(f"{case_name}: Handled without error")
                    elif result == expected:
                        correct_test_cases += 1
                        test_notes.append(f"{case_name}: Correct ({result})")
                    else:
                        test_notes.append(f"{case_name}: Incorrect (got {result}, expected {expected})")
                else:
                    # Try to find a function that takes a dictionary input
                    found_function = False
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if callable(attr) and not attr_name.startswith('_'):
                            try:
                                result = attr(input_data)
                                found_function = True

                                if case_name == "edge_case_empty":
                                    correct_test_cases += 1
                                    test_notes.append(f"{case_name}: Handled without error using {attr_name}")
                                elif result == expected:
                                    correct_test_cases += 1
                                    test_notes.append(f"{case_name}: Correct ({result}) using {attr_name}")
                                else:
                                    test_notes.append(
                                        f"{case_name}: Incorrect (got {result}, expected {expected}) using {attr_name}")
                                break
                            except Exception:
                                continue

                    if not found_function:
                        test_notes.append(f"{case_name}: Could not find appropriate function to test")
            except Exception as e:
                test_notes.append(f"{case_name}: Error: {str(e)}")

        # Clean up path
        if sys.path and str(repo_path) == sys.path[0]:
            sys.path.pop(0)

        # Calculate score (out of 5)
        score = (correct_test_cases / total_test_cases) * 5 if total_test_cases > 0 else 0
        notes = "; ".join(test_notes)

        return score, notes

    except Exception as e:
        # Clean up path
        if sys.path and str(repo_path) == sys.path[0]:
            sys.path.pop(0)

        return 0, f"Error checking algorithm: {str(e)}"