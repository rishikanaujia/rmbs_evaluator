"""
Utilities for repository management and Git operations
"""

import os
import subprocess
from pathlib import Path
from typing import List, Optional


def clone_repository(repo_url: str, target_dir: Path, branch: str = "main") -> bool:
    """
    Clone a Git repository to a target directory

    Args:
        repo_url: URL of the Git repository
        target_dir: Directory to clone the repository into
        branch: Branch to clone (default: main)

    Returns:
        True if successful, False otherwise
    """
    try:
        # Create target directory if it doesn't exist
        target_dir.mkdir(parents=True, exist_ok=True)

        # Clone the repository
        result = subprocess.run(
            ["git", "clone", "-b", branch, repo_url, str(target_dir)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        return True
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository {repo_url}: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error cloning repository {repo_url}: {str(e)}")
        return False


def list_repositories(base_dir: Path, github_format: bool = False) -> List[dict]:
    """
    List all Git repositories in a directory

    Args:
        base_dir: Base directory to search for repositories
        github_format: Whether to return in GitHub API format

    Returns:
        List of dictionaries with repository information
    """
    repositories = []

    for item in base_dir.iterdir():
        if not item.is_dir():
            continue

        git_dir = item / ".git"

        if git_dir.exists() and git_dir.is_dir():
            repo_info = {
                "name": item.name,
                "path": str(item),
                "url": get_repo_url(item)
            }

            if github_format:
                # Add GitHub API format fields
                repo_info["full_name"] = f"username/{item.name}"
                repo_info["html_url"] = repo_info["url"] or ""
                repo_info["description"] = get_repo_description(item)

            repositories.append(repo_info)

    return repositories


def get_repo_url(repo_path: Path) -> Optional[str]:
    """
    Get the remote URL of a Git repository

    Args:
        repo_path: Path to the repository

    Returns:
        Repository URL or None if not found
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "config", "--get", "remote.origin.url"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    except Exception:
        return None


def get_repo_description(repo_path: Path) -> str:
    """
    Get a description for the repository from the README

    Args:
        repo_path: Path to the repository

    Returns:
        Description string (first paragraph of README if available)
    """
    readme_candidates = [
        repo_path / "README.md",
        repo_path / "README.rst",
        repo_path / "README.txt",
        repo_path / "README"
    ]

    for readme in readme_candidates:
        if readme.exists():
            try:
                with open(readme, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Try to extract the first paragraph
                    paragraphs = content.split('\n\n')
                    if paragraphs:
                        # Clean up the first paragraph (remove headers, etc.)
                        first_para = paragraphs[0].strip()
                        first_para = first_para.replace('#', '').strip()

                        if first_para:
                            return first_para[:100] + ('...' if len(first_para) > 100 else '')
            except Exception:
                pass

    return "No description available"