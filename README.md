# RMBS Code Evaluation Framework

A comprehensive framework for evaluating residential mortgage-backed securities (RMBS) credit rating implementations. This tool helps assess code submissions based on structure, code quality, algorithm correctness, performance, test quality, and documentation.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/rmbs-evaluator.git
   cd rmbs-evaluator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the evaluator on a directory containing multiple repository submissions:

```bash
python -m rmbs_evaluator.main /path/to/repos --output results.csv --visualize
```

### Command Line Arguments

- `repos_dir`: Path to the directory containing candidate repositories
- `--output`, `-o`: Path to save the evaluation results CSV (default: evaluation_results.csv)
- `--visualize`, `-v`: Generate visualization charts
- `--parallel`, `-p`: Run evaluations in parallel (faster but less stable)

## Evaluation Criteria

The framework evaluates submissions based on:

1. **Repository Structure** (10%)
   - Presence of required files
   - Organization

2. **Code Quality** (20%)
   - Documentation/comments
   - Function organization
   - Input validation
   - Code complexity

3. **Algorithm Correctness** (30%)
   - Correct implementation of RMBS rating algorithm
   - Handling of edge cases

4. **Test Quality** (20%)
   - Test coverage
   - Test variety and completeness

5. **Performance** (10%)
   - Execution speed with large datasets

6. **Documentation** (10%)
   - README completeness
   - Installation and usage instructions
   - Architecture and design explanations

## Test Cases

The framework includes several test cases to verify algorithm correctness:

- Basic mixed-risk case
- High-risk mortgage portfolio (should yield "C" rating)
- Low-risk mortgage portfolio (should yield "AAA" rating)
- Empty portfolio (edge case)
- Large portfolio (1000 mortgages for performance testing)

## Output

The evaluation produces:

1. CSV file with detailed metrics for each submission
2. Visualization charts (if enabled):
   - Overall score distribution
   - Correctness vs performance scatter plot
   - Radar chart of top 5 submissions
   - Component scores for top 10 submissions
   - Correlation heatmap

## Architecture

```
rmbs_evaluator/
├── __init__.py
├── main.py                    # Entry point script
├── evaluator.py               # Main evaluator class
├── test_cases.py              # Test case definitions
├── evaluators/
│   ├── __init__.py
│   ├── structure_evaluator.py # Evaluate repository structure
│   ├── test_evaluator.py      # Evaluate tests and coverage
│   ├── quality_evaluator.py   # Evaluate code quality
│   ├── algorithm_evaluator.py # Evaluate algorithm correctness
│   ├── performance_evaluator.py # Evaluate performance
│   └── documentation_evaluator.py # Evaluate documentation
├── visualizers/
│   ├── __init__.py
│   └── result_visualizer.py   # Generate visualizations
└── utils/
    ├── __init__.py
    ├── repo_utils.py          # Repository handling utilities
    └── scoring_utils.py       # Scoring utilities
```

## Examples

### Example Output CSV

| repo_name | overall_score | structure_score | test_score | code_quality_score | algorithm_score | performance_score | documentation_score |
|-----------|--------------|-----------------|------------|-------------------|-----------------|-------------------|---------------------|
| repo1     | 4.25         | 5.0             | 4.5        | 3.8               | 5.0             | 3.2               | 3.5                 |
| repo2     | 3.80         | 5.0             | 3.2        | 4.1               | 4.2             | 2.8               | 2.9                 |
| ...       | ...          | ...             | ...        | ...               | ...             | ...               | ...                 |

### Example Visualization

The visualizations include:
- Distribution of overall scores
- Correlation between algorithm correctness and performance
- Radar charts showing component scores for top submissions

## Extending the Framework

To add new evaluation criteria:

1. Create a new evaluator module in the `evaluators/` directory
2. Update the main `evaluator.py` to include the new component
3. Adjust the weights in `evaluator.py` as needed