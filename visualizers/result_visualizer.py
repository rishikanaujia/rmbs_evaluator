"""
Generates visualizations for RMBS evaluation results
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List, Dict, Any


def generate_visualizations(results: List[Dict[str, Any]]) -> None:
    """
    Generate summary visualizations of the evaluation results

    Args:
        results: List of evaluation result dictionaries
    """
    if not results:
        print("No results to visualize")
        return

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Create visualizations directory
    viz_dir = Path("evaluation_visualizations")
    viz_dir.mkdir(exist_ok=True)

    # Set up the style
    sns.set(style="whitegrid")

    # 1. Overall score distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df["overall_score"], bins=20, kde=True)
    plt.title("Distribution of Overall Scores", fontsize=16)
    plt.xlabel("Score", fontsize=14)
    plt.ylabel("Number of Submissions", fontsize=14)
    plt.tight_layout()
    plt.savefig(viz_dir / "overall_score_distribution.png", dpi=300)
    plt.close()

    # 2. Correctness vs Performance scatter plot
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        data=df,
        x="algorithm_score",
        y="performance_score",
        size="overall_score",
        sizes=(20, 200),
        alpha=0.7
    )
    plt.title("Algorithm Correctness vs Performance", fontsize=16)
    plt.xlabel("Algorithm Score", fontsize=14)
    plt.ylabel("Performance Score", fontsize=14)
    plt.tight_layout()
    plt.savefig(viz_dir / "correctness_vs_performance.png", dpi=300)
    plt.close()

    # 3. Radar chart for top submissions
    generate_radar_chart(df, viz_dir)

    # 4. Component scores for top 10 submissions
    generate_top10_chart(df, viz_dir)

    # 5. Correlation heatmap between components
    generate_correlation_heatmap(df, viz_dir)

    print(f"Summary visualizations saved to {viz_dir}")


def generate_radar_chart(df: pd.DataFrame, viz_dir: Path) -> None:
    """
    Generate radar charts for top submissions

    Args:
        df: DataFrame with evaluation results
        viz_dir: Directory to save visualizations
    """
    # Get top 5 submissions
    top5 = df.nlargest(5, "overall_score")

    # Define component columns
    components = [
        "structure_score", "test_score", "code_quality_score",
        "algorithm_score", "performance_score", "documentation_score"
    ]

    # Rename for better display
    component_names = {
        "structure_score": "Structure",
        "test_score": "Tests",
        "code_quality_score": "Code Quality",
        "algorithm_score": "Algorithm",
        "performance_score": "Performance",
        "documentation_score": "Documentation"
    }

    # Set up the figure
    plt.figure(figsize=(12, 10))

    # Number of variables
    N = len(components)

    # Create angles for each component
    angles = [n / float(N) * 2 * 3.14159 for n in range(N)]
    angles += angles[:1]  # Close the loop

    # Set up the subplot
    ax = plt.subplot(111, polar=True)

    # Draw one axis per variable and add labels
    plt.xticks(angles[:-1], [component_names[c] for c in components], fontsize=12)

    # Draw the y-axis labels (0-5)
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"], fontsize=10)
    plt.ylim(0, 5)

    # Plot each submission
    for i, row in top5.iterrows():
        values = [row[c] for c in components]
        values += values[:1]  # Close the loop

        # Plot values
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=row['repo_name'])
        ax.fill(angles, values, alpha=0.1)

    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), fontsize=12)
    plt.title('Top 5 Submissions - Component Comparison', fontsize=16)
    plt.tight_layout()
    plt.savefig(viz_dir / "radar_chart.png", dpi=300)
    plt.close()


def generate_top10_chart(df: pd.DataFrame, viz_dir: Path) -> None:
    """
    Generate component scores for top 10 submissions

    Args:
        df: DataFrame with evaluation results
        viz_dir: Directory to save visualizations
    """
    # Get top 10 submissions
    top10 = df.nlargest(10, "overall_score")

    components = [
        "structure_score", "test_score", "code_quality_score",
        "algorithm_score", "performance_score", "documentation_score"
    ]

    # Rename for better display
    component_names = {
        "structure_score": "Structure",
        "test_score": "Tests",
        "code_quality_score": "Code Quality",
        "algorithm_score": "Algorithm",
        "performance_score": "Performance",
        "documentation_score": "Documentation"
    }

    # Rename columns for better display
    renamed_top10 = top10.rename(columns=component_names)

    # Plot
    plt.figure(figsize=(14, 8))

    # Create horizontal bar chart for each component
    renamed_top10.set_index("repo_name")[list(component_names.values())].plot(
        kind="barh", figsize=(14, 8), width=0.8
    )

    plt.title("Component Scores for Top 10 Submissions", fontsize=16)
    plt.xlabel("Score (0-5)", fontsize=14)
    plt.ylabel("Repository", fontsize=14)
    plt.tight_layout()
    plt.savefig(viz_dir / "top10_component_scores.png", dpi=300)
    plt.close()


def generate_correlation_heatmap(df: pd.DataFrame, viz_dir: Path) -> None:
    """
    Generate correlation heatmap between evaluation components

    Args:
        df: DataFrame with evaluation results
        viz_dir: Directory to save visualizations
    """
    # Select score columns
    score_columns = [
        "structure_score", "test_score", "code_quality_score",
        "algorithm_score", "performance_score", "documentation_score",
        "overall_score"
    ]

    # Compute correlation matrix
    corr_matrix = df[score_columns].corr()

    # Rename for better display
    component_names = {
        "structure_score": "Structure",
        "test_score": "Tests",
        "code_quality_score": "Code Quality",
        "algorithm_score": "Algorithm",
        "performance_score": "Performance",
        "documentation_score": "Documentation",
        "overall_score": "Overall"
    }

    corr_matrix = corr_matrix.rename(index=component_names, columns=component_names)

    # Plot
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap='coolwarm',
        vmin=-1,
        vmax=1,
        fmt='.2f',
        linewidths=0.5
    )
    plt.title("Correlation Between Evaluation Components", fontsize=16)
    plt.tight_layout()
    plt.savefig(viz_dir / "correlation_heatmap.png", dpi=300)
    plt.close()