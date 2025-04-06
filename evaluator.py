"""
Main RMBS evaluator class that coordinates the evaluation process
"""

import os
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Any

from rmbs_evaluator.test_cases import RMBS_TEST_CASES
from rmbs_evaluator.evaluators.structure_evaluator import evaluate_structure
from rmbs_evaluator.evaluators.test_evaluator import evaluate_tests
from rmbs_evaluator.evaluators.quality_evaluator import evaluate_code_quality
from rmbs_evaluator.evaluators.algorithm_evaluator import evaluate_algorithm
from rmbs_evaluator.evaluators.performance_evaluator import evaluate_performance
from rmbs_evaluator.evaluators.documentation_evaluator import evaluate_documentation
from rmbs_evaluator.visualizers.result_visualizer import generate_visualizations


class RMBSEvaluator:
    """
    Main evaluator class for RMBS credit rating implementations
    """

    def __init__(self, repos_directory: str, output_file: str = "evaluation_results.csv",
                 visualize: bool = True, parallel: bool = False):
        """
        Initialize the evaluator

        Args:
            repos_directory: Path to directory containing all candidate repositories
            output_file: Path to save the evaluation results
            visualize: Whether to generate visualization charts
            parallel: Whether to run evaluations in parallel
        """
        self.repos_directory = Path(repos_directory)
        self.output_file = output_file
        self.visualize = visualize
        self.parallel = parallel
        self.results = []
        self.test_cases = RMBS_TEST_CASES

    def evaluate_all_repos(self) -> None:
        """
        Evaluate all repositories in the specified directory
        """
        # Get list of all repository directories
        repo_dirs = [d for d in self.repos_directory.iterdir() if d.is_dir()]

        if self.parallel and len(repo_dirs) > 1:
            # Use multiprocessing for parallel evaluation
            with ProcessPoolExecutor() as executor:
                # Submit all evaluation tasks
                future_to_repo = {
                    executor.submit(self._evaluate_repo_wrapper, repo_path): repo_path
                    for repo_path in repo_dirs
                }

                # Process results as they complete
                for future in as_completed(future_to_repo):
                    repo_path = future_to_repo[future]
                    try:
                        result = future.result()
                        self.results.append(result)
                        print(f"Evaluated: {repo_path.name} - Score: {result['overall_score']:.2f}")
                    except Exception as exc:
                        print(f"Error evaluating {repo_path.name}: {str(exc)}")
                        # Add failed evaluation to results
                        self.results.append({
                            "repo_name": repo_path.name,
                            "error": str(exc),
                            "overall_score": 0
                        })
        else:
            # Serial evaluation
            for repo_path in repo_dirs:
                try:
                    print(f"Evaluating: {repo_path.name}")
                    result = self.evaluate_repo(repo_path)
                    self.results.append(result)
                    print(f"Score: {result['overall_score']:.2f}")
                except Exception as exc:
                    print(f"Error evaluating {repo_path.name}: {str(exc)}")
                    # Add failed evaluation to results
                    self.results.append({
                        "repo_name": repo_path.name,
                        "error": str(exc),
                        "overall_score": 0
                    })

        # Save results to CSV
        self._save_results()

        # Generate summary visualizations if requested
        if self.visualize:
            generate_visualizations(self.results)

    def _evaluate_repo_wrapper(self, repo_path: Path) -> Dict[str, Any]:
        """
        Wrapper for parallel execution of repo evaluation
        """
        try:
            return self.evaluate_repo(repo_path)
        except Exception as exc:
            return {
                "repo_name": repo_path.name,
                "error": str(exc),
                "overall_score": 0
            }

    def evaluate_repo(self, repo_path: Path) -> Dict[str, Any]:
        """
        Evaluate a single repository

        Args:
            repo_path: Path to the repository

        Returns:
            Dictionary containing evaluation metrics
        """
        # Check repository structure
        structure_score, structure_notes = evaluate_structure(repo_path)

        # Run tests if they exist
        test_score, test_notes, test_coverage = evaluate_tests(repo_path)

        # Evaluate code quality
        code_quality_score, code_quality_notes = evaluate_code_quality(repo_path)

        # Check algorithm correctness
        algorithm_score, algorithm_notes = evaluate_algorithm(repo_path, self.test_cases)

        # Performance testing
        performance_score, performance_notes = evaluate_performance(repo_path, self.test_cases)

        # Documentation quality
        docs_score, docs_notes = evaluate_documentation(repo_path)

        # Calculate overall score (weighted average)
        weights = {
            "structure": 0.1,
            "tests": 0.2,
            "code_quality": 0.2,
            "algorithm": 0.3,
            "performance": 0.1,
            "documentation": 0.1
        }

        scores = {
            "structure": structure_score,
            "tests": test_score,
            "code_quality": code_quality_score,
            "algorithm": algorithm_score,
            "performance": performance_score,
            "documentation": docs_score
        }

        overall_score = sum(scores[k] * weights[k] for k in weights)

        return {
            "repo_name": repo_path.name,
            "overall_score": overall_score,
            "structure_score": structure_score,
            "structure_notes": structure_notes,
            "test_score": test_score,
            "test_coverage": test_coverage,
            "test_notes": test_notes,
            "code_quality_score": code_quality_score,
            "code_quality_notes": code_quality_notes,
            "algorithm_score": algorithm_score,
            "algorithm_notes": algorithm_notes,
            "performance_score": performance_score,
            "performance_notes": performance_notes,
            "documentation_score": docs_score,
            "documentation_notes": docs_notes
        }

    def _save_results(self) -> None:
        """
        Save evaluation results to CSV
        """
        df = pd.DataFrame(self.results)
        df.to_csv(self.output_file, index=False)