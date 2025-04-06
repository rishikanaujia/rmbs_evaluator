#!/usr/bin/env python3
"""
RMBS Code Evaluator - Main entry point
Evaluates multiple RMBS credit rating implementations
"""

import argparse
import sys
from pathlib import Path

from rmbs_evaluator.evaluator import RMBSEvaluator


def main():
    """
    Parse arguments and run the evaluator
    """
    parser = argparse.ArgumentParser(
        description="Evaluate RMBS credit rating code submissions"
    )
    parser.add_argument(
        "repos_dir",
        help="Directory containing all candidate repositories"
    )
    parser.add_argument(
        "--output", "-o",
        default="evaluation_results.csv",
        help="Output file for evaluation results (CSV)"
    )
    parser.add_argument(
        "--visualize", "-v",
        action="store_true",
        help="Generate visualization charts"
    )
    parser.add_argument(
        "--parallel", "-p",
        action="store_true",
        help="Run evaluations in parallel (faster but less stable)"
    )

    args = parser.parse_args()

    # Check if the repos directory exists
    repos_dir = Path(args.repos_dir)
    if not repos_dir.exists() or not repos_dir.is_dir():
        print(f"Error: Directory '{args.repos_dir}' does not exist or is not a directory")
        sys.exit(1)

    # Run the evaluator
    evaluator = RMBSEvaluator(
        repos_dir,
        output_file=args.output,
        visualize=args.visualize,
        parallel=args.parallel
    )

    evaluator.evaluate_all_repos()
    print(f"Evaluation complete. Results saved to {args.output}")

    if args.visualize:
        print("Visualization charts generated in 'evaluation_visualizations/' directory")


if __name__ == "__main__":
    main()