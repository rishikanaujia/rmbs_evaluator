"""
Setup script for the RMBS Code Evaluation Framework
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rmbs-evaluator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Framework for evaluating RMBS credit rating implementations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rmbs-evaluator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "pytest>=6.2.0",
        "coverage>=6.0.0",
    ],
    entry_points={
        "console_scripts": [
            "rmbs-evaluator=rmbs_evaluator.main:main",
        ],
    },
)