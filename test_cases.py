"""
Test cases for evaluating RMBS credit rating algorithms
"""

from typing import Dict, Any

# Define test cases with expected outputs
RMBS_TEST_CASES = {
    "basic_case": {
        "input": {
            "mortgages": [
                {
                    "credit_score": 750,
                    "loan_amount": 200000,
                    "property_value": 250000,
                    "annual_income": 60000,
                    "debt_amount": 20000,
                    "loan_type": "fixed",
                    "property_type": "single_family"
                },
                {
                    "credit_score": 680,
                    "loan_amount": 150000,
                    "property_value": 175000,
                    "annual_income": 45000,
                    "debt_amount": 10000,
                    "loan_type": "adjustable",
                    "property_type": "condo"
                }
            ]
        },
        "expected_output": "BBB"  # Typical case with mixed risk factors
    },

    "high_risk_case": {
        "input": {
            "mortgages": [
                {
                    "credit_score": 600,
                    "loan_amount": 180000,
                    "property_value": 190000,
                    "annual_income": 40000,
                    "debt_amount": 25000,
                    "loan_type": "adjustable",
                    "property_type": "condo"
                },
                {
                    "credit_score": 620,
                    "loan_amount": 270000,
                    "property_value": 290000,
                    "annual_income": 55000,
                    "debt_amount": 30000,
                    "loan_type": "adjustable",
                    "property_type": "condo"
                }
            ]
        },
        "expected_output": "C"  # High risk mortgages
    },

    "low_risk_case": {
        "input": {
            "mortgages": [
                {
                    "credit_score": 790,
                    "loan_amount": 150000,
                    "property_value": 300000,
                    "annual_income": 100000,
                    "debt_amount": 10000,
                    "loan_type": "fixed",
                    "property_type": "single_family"
                },
                {
                    "credit_score": 760,
                    "loan_amount": 200000,
                    "property_value": 450000,
                    "annual_income": 120000,
                    "debt_amount": 15000,
                    "loan_type": "fixed",
                    "property_type": "single_family"
                }
            ]
        },
        "expected_output": "AAA"  # Low risk mortgages
    },

    "edge_case_empty": {
        "input": {
            "mortgages": []
        },
        "expected_output": None  # Empty case - should handle this appropriately
    },

    "large_case": {
        "input": {
            "mortgages": [
                {
                    "credit_score": 700 + (i % 150),
                    "loan_amount": 150000 + (i * 1000),
                    "property_value": 200000 + (i * 2000),
                    "annual_income": 50000 + (i * 500),
                    "debt_amount": 10000 + (i * 100),
                    "loan_type": "fixed" if i % 2 == 0 else "adjustable",
                    "property_type": "single_family" if i % 3 == 0 else "condo"
                } for i in range(1000)
            ]
        },
        "expected_output": None  # Not testing for correctness, just performance
    }
}

# Define the key parameters for evaluation
EVALUATION_PARAMS = {
    "weights": {
        "structure": 0.1,
        "tests": 0.2,
        "code_quality": 0.2,
        "algorithm": 0.3,
        "performance": 0.1,
        "documentation": 0.1
    },
    "expected_files": [
        "credit_rating.py",
        "test_credit_rating.py",
        "requirements.txt",
        "README.md"
    ]
}