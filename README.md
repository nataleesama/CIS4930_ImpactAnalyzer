# CIS4930_ImpactAnalyzer
Term Project: Climate Change Impact Analyzer

Members: Natalee Sama (nataleesama), Miles Brosz (milesbrosz, gelatness), Aidan Mahoney (amahoney23), Tyler Zuluaga (tz33)

# Overview
This project is a Climate change analyzer that uses a linearRegression learning model to predict future precipitations for years outside of the sample size. The data is pooled from 3 stations over the course of 5 complete years (2020,2024), and is normalized and represented in mathematical plots. Main functionalities from the command-line interface (cli.py) include: prediction, anomaly distinction, and clustering.

# Setup
1. Clone this repository
2. Create a virutal environment: 'python3 -m venv venv'
3. Activate this environment
  - Windows: 'venv\Scripts\activate'
  - macOS/Linux: 'source venv/bin/activate'
4. And install all the dependencies: 'pip install -r requirements.txt'

# Usage
1. Change to directory of command-line interface with: 'cd src/'
2. Run the command-line interface with: 'python3 cli.py --x', with x being equal to the action you wish to trigger {'predict','anomalies', or 'cluster' }

# Running tests
python3 test_'x', x = {'algorithms.py', 'data_processor.py', 'visualizer.py'}, in ~/tests/

# Project structure
- 'src/': Source code
- 'tests/': Unit tests
- 'data/': Climate data (JSON format)
- 'requirements.txt': Project dependencies
- 'README.md': Project documentation

# Project features
this project also features usages of linearRegression learning models, normalization of datas, and a supplemental HTML interface.
