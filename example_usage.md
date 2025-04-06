# RMBS Evaluator Example Usage

This guide demonstrates how to use the RMBS Evaluator to assess multiple candidate submissions.

## Setup

First, install the evaluation framework:

```bash
# Clone the evaluator repository
git clone https://github.com/yourusername/rmbs-evaluator.git
cd rmbs-evaluator

# Install the package
pip install -e .
```

## Workflow 1: GitHub Repository URLs

If you have a list of GitHub repository URLs:

1. Create a JSON file with the repository URLs:

```json
[
  "https://github.com/candidate1/rmbs-implementation.git",
  "https://github.com/candidate2/credit-rating-api.git",
  "https://github.com/candidate3/rmbs-rating.git",
  "..."
]
```

2. Clone all repositories:

```bash
python batch_clone.py --repos-file candidate_repos.json --output-dir ./candidate_repos --parallel
```

3. Run the evaluation:

```bash
rmbs-evaluator ./candidate_repos --output results.csv --visualize
```

## Workflow 2: Local Repositories

If you already have the repositories downloaded:

```bash
rmbs-evaluator /path/to/repos --visualize --parallel
```

## Analyzing Results

After running the evaluation, you'll have:

1. A CSV file (`results.csv` by default) with detailed metrics for each submission
2. Visualization charts in the `evaluation_visualizations` directory

### Example Analysis

To perform additional analysis on the results, you can use pandas:

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load results
results = pd.read_csv('results.csv')

# Show top 10 candidates by overall score
top_candidates = results.nlargest(10, 'overall_score')
print(top_candidates[['repo_name', 'overall_score']])

# Find candidates with best algorithm implementations
best_algorithms = results.nlargest(5, 'algorithm_score')
print(best_algorithms[['repo_name', 'algorithm_score', 'overall_score']])

# Find candidates with strong test coverage but weaker algorithm scores
good_testers = results[
    (results['test_score'] > 4.0) & 
    (results['algorithm_score'] < 3.0)
].sort_values('test_score', ascending=False)

print(good_testers[['repo_name', 'test_score', 'algorithm_score']])
```

## Customizing Evaluation

To customize the evaluation criteria or weights:

1. Edit the weights in `rmbs_evaluator/test_cases.py`:

```python
EVALUATION_PARAMS = {
    "weights": {
        "structure": 0.1,      # 10%
        "tests": 0.2,          # 20%
        "code_quality": 0.2,   # 20%
        "algorithm": 0.3,      # 30%
        "performance": 0.1,    # 10%
        "documentation": 0.1   # 10%
    },
    # ...
}
```

2. To add new test cases, add them to the `RMBS_TEST_CASES` dictionary in the same file.

## Generating HTML Report

To generate a detailed HTML report from the results:

```bash
python -m rmbs_evaluator.report_generator results.csv --output evaluation_report.html
```

This creates an interactive HTML report with:
- Sortable results table
- Interactive charts
- Detailed analysis of each candidate