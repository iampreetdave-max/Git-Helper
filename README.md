# Git-Helper

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)

An automated repository-analysis toolkit that runs code-quality, security, coverage, and trend checks inside GitHub Actions and commits the results back to your repo — no external services required.

## Overview

Git-Helper (presented in the UI as "Git-Buddy") packages a set of Python analysis scripts and a GitHub Actions workflow that, on a daily schedule, inspect a repository and generate health reports, dashboards, changelogs, and trend charts. Everything runs within the repository's own Actions environment, so code is never sent to third-party APIs. A bundled Streamlit app serves as the project's documentation site and a one-click generator for the setup package you drop into a target repository.

## Key Features

- **Code quality analysis** — complexity and maintainability via Radon, Pylint, and Flake8
- **Security scanning** — Bandit, pip-audit, and Safety for code and dependency vulnerabilities
- **Test coverage** — pytest with coverage reporting
- **Dependency checks** — detects outdated or vulnerable packages
- **Health scoring** — aggregates metrics into a repository health score (`repo_health_metrics.json`)
- **LOC trend tracking** — appends daily lines-of-code history and renders charts with Matplotlib/NumPy
- **Automated changelog** — generates `CHANGELOG.md` from git commit history
- **Health dashboard** — produces `HEALTH_DASHBOARD.md` with strengths, weaknesses, and recommendations
- **README updater** — inserts metrics/badges into a README using HTML-comment markers, preserving surrounding content
- **GitHub Actions job summary** — formats results for the Actions UI
- **Streamlit docs site** — feature overview, how-it-works, FAQ, and a downloadable setup package

## How It Works

The workflow runs on a daily cron (and on manual dispatch) and executes the scripts in `.github/scripts/` as a pipeline:

```
GitHub Actions (daily)
  → analyzer.py                 # run pylint, flake8, radon, bandit, pip-audit, safety, pytest-cov
  → repo_health_metrics.py      # aggregate into health scores + history
  → loc_trend_collector.py      # append daily LOC history
  → loc_trend_visualizer.py     # render trend charts
  → changelog_generator.py      # build CHANGELOG.md from git log
  → repo_health_dashboard.py    # build HEALTH_DASHBOARD.md
  → readme_updater.py           # update README metrics
  → create_summary.py           # write the Actions job summary
  → git add/commit/push         # results committed back to the repo
```

Behavior is toggled through environment variables (see Configuration), and the tooling is designed to run with sensible defaults and no API keys.

## Tech Stack

- **Language:** Python 3.11+
- **UI / docs:** Streamlit
- **Analysis:** Pylint, Flake8, Radon, Bandit, pip-audit, Safety, pytest + pytest-cov
- **Visualization:** Matplotlib, NumPy
- **Automation:** GitHub Actions
- **HTTP:** Requests

## Getting Started

### Prerequisites

- Python 3.11+
- A GitHub repository with Actions enabled (for the automated pipeline)

### Install dependencies

```bash
git clone https://github.com/iampreetdave-max/Git-Helper.git
cd Git-Helper
pip install -r requirements.txt
```

### Run the documentation / setup app

```bash
streamlit run streamlit_app.py
```

The app provides feature documentation and a downloadable ZIP containing the workflow file, `requirements.txt`, a `.env.example`, and helper setup scripts to add Git-Helper to another repository.

### Helper installer

```bash
python install.py
```

### Enable the automated analysis in a target repo

1. Add the workflow and `requirements.txt` to the target repository.
2. Enable GitHub Actions for that repository.
3. The analysis runs on the configured schedule and commits reports back automatically.

## Configuration

Copy `.env.example` to `.env` to adjust behavior. Toggles and thresholds include:

| Variable | Purpose |
|---|---|
| `ENABLE_CODE_QUALITY` | Toggle code-quality analysis |
| `ENABLE_SECURITY_SCAN` | Toggle security scanning |
| `ENABLE_TEST_COVERAGE` | Toggle coverage reporting |
| `ENABLE_DEPENDENCY_CHECK` | Toggle dependency checks |
| `ENABLE_CHANGELOG` | Toggle changelog generation |
| `ENABLE_README_UPDATE` | Toggle README updating |
| `ENABLE_HEALTH_DASHBOARD` | Toggle dashboard generation |
| `ENABLE_LOC_TRENDS` | Toggle LOC trend tracking |
| `MIN_COVERAGE_PERCENT` | Minimum coverage threshold (default 70) |
| `MIN_LINT_SCORE` | Minimum lint score (default 7.0) |
| `MAX_COMPLEXITY_THRESHOLD` | Max cyclomatic complexity (default 10) |
| `EXCLUDED_DIRS` / `EXCLUDED_FILES` | Paths to skip |
| `OUTPUT_FORMAT` · `GENERATE_CHARTS` · `LOG_LEVEL` · `VERBOSE` | Output and logging options |

## Project Structure

```
Git-Helper/
├── streamlit_app.py            # Streamlit docs + setup-package generator
├── install.py                  # Helper installer
├── requirements.txt
├── .env.example
├── repo_health_metrics.json    # Sample aggregated metrics
├── .github/
│   ├── scripts/                # Analysis pipeline scripts
│   ├── workflows/              # Daily-analysis workflow
│   └── loc_history.json        # LOC history data
├── .streamlit/                 # Streamlit config
├── ARCHITECTURE.md · FEATURES_GUIDE.md · HEALTH_DASHBOARD.md
├── STREAMLIT_SETUP.md · ZERO_CODE_SETUP.md · SETUP_HEALTH_AND_LOC.md
├── LICENSE
└── README.md
```

## Documentation

Additional guides live alongside this README: `ARCHITECTURE.md`, `FEATURES_GUIDE.md`, `STREAMLIT_SETUP.md`, `ZERO_CODE_SETUP.md`, and `SETUP_HEALTH_AND_LOC.md`.

## License

See the [LICENSE](LICENSE) file.
