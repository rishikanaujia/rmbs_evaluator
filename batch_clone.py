#!/usr/bin/env python3
"""
Batch clone GitHub repositories for evaluation
"""

import os
import sys
import json
import argparse
import concurrent.futures
from pathlib import Path

from rmbs_evaluator.utils.repo_utils import clone_repository


def main():
    """
    Parse arguments and clone repositories in batch
    """
    parser = argparse.ArgumentParser(
        description="Clone multiple GitHub repositories for evaluation"
    )
    parser.add_argument(
        "--repos-file", "-f",
        required=True,
        help="JSON file containing repository URLs"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="./repos",
        help="Directory to clone repositories into"
    )
    parser.add_argument(
        "--parallel", "-p",
        action="store_true",
        help="Clone repositories in parallel"
    )
    parser.add_argument(
        "--branch", "-b",
        default="main",
        help="Branch to clone (default: main)"
    )

    args = parser.parse_args()

    # Check if repos file exists
    repos_file = Path(args.repos_file)
    if not repos_file.exists():
        print(f"Error: File '{args.repos_file}' does not exist")
        sys.exit(1)

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load repositories
    try:
        with open(repos_file, 'r') as f:
            repos_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: '{args.repos_file}' is not a valid JSON file")
        sys.exit(1)

    # Extract repository URLs
    if isinstance(repos_data, list):
        # If it's a list of strings, use them directly
        if all(isinstance(item, str) for item in repos_data):
            repos = repos_data
        # If it's a list of objects, extract URLs
        elif all(isinstance(item, dict) for item in repos_data):
            repos = [item.get("url") or item.get("html_url") or item.get("clone_url")
                     for item in repos_data if "url" in item or "html_url" in item or "clone_url" in item]
        else:
            print("Error: Unknown repository format in JSON file")
            sys.exit(1)
    elif isinstance(repos_data, dict):
        # Check if it's a GitHub API response
        if "items" in repos_data and isinstance(repos_data["items"], list):
            repos = [item.get("html_url") or item.get("clone_url")
                     for item in repos_data["items"] if "html_url" in item or "clone_url" in item]
        else:
            # Extract all values that look like URLs
            repos = [value for value in repos_data.values()
                     if isinstance(value, str) and (value.startswith("http") or value.startswith("git@"))]
    else:
        print("Error: JSON file must contain a list or dictionary")
        sys.exit(1)

    if not repos:
        print("Error: No repository URLs found in the JSON file")
        sys.exit(1)

    print(f"Found {len(repos)} repositories to clone")

    # Clone repositories
    if args.parallel:
        # Clone in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            future_to_repo = {
                executor.submit(
                    clone_repository,
                    repo,
                    output_dir / get_repo_name(repo),
                    args.branch
                ): repo for repo in repos
            }

            for future in concurrent.futures.as_completed(future_to_repo):
                repo = future_to_repo[future]
                try:
                    success = future.result()
                    if success:
                        print(f"Successfully cloned {repo}")
                    else:
                        print(f"Failed to clone {repo}")
                except Exception as exc:
                    print(f"Error cloning {repo}: {exc}")
    else:
        # Clone sequentially
        for repo in repos:
            target_dir = output_dir / get_repo_name(repo)
            print(f"Cloning {repo} to {target_dir}...")
            success = clone_repository(repo, target_dir, args.branch)

            if success:
                print(f"Successfully cloned {repo}")
            else:
                print(f"Failed to clone {repo}")

    print("Cloning complete")


def get_repo_name(repo_url: str) -> str:
    """
    Extract repository name from URL

    Args:
        repo_url: Repository URL

    Returns:
        Repository name
    """
    # Remove .git extension if present
    if repo_url.endswith(".git"):
        repo_url = repo_url[:-4]

    # Extract the last part of the URL
    if "/" in repo_url:
        parts = repo_url.rstrip("/").split("/")
        return parts[-1]

    return repo_url


if __name__ == "__main__":
    main()