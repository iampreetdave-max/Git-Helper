# Git-Helper

Automated repository analysis tool with GitHub Actions integration.

## Overview

Git-Helper is a comprehensive repository analysis system that automatically:
- Analyzes code complexity and maintainability
- Detects and runs tests with coverage reporting
- Scans for security vulnerabilities
- Checks dependency health
- Generates changelogs from git history
- Updates README with analysis results
- Provides historical trend tracking

## Features

- **Code Quality Analysis**: Cyclomatic complexity and maintainability index using Radon
- **Test Coverage**: Automatic test detection and coverage reporting with pytest
- **Security Scanning**: Vulnerability scanning with bandit, pip-audit, and npm audit
- **Dependency Health**: Identifies outdated Python and Node.js packages
- **Automated Documentation**: Auto-generates CHANGELOG.md and updates README
- **GitHub Actions Integration**: Runs daily analysis and commits results
- **Self-Healing**: Automatically creates missing configuration files
- **Historical Trends**: Tracks metrics over time

## Setup

### Prerequisites

- Python 3.11+
- Git repository

### Installation

The GitHub Actions workflow automatically installs required tools:
- Python: pylint, flake8, bandit, radon, pytest, pytest-cov, pip-audit, safety
- Node.js (optional): jshint, markdownlint-cli

### GitHub Actions Workflow

The workflow runs:
1. **Daily at 2 AM UTC** (configurable via cron schedule)
2. **On manual trigger** from GitHub Actions UI
3. **When workflow files are modified**

## Directory Structure

```
.
├── .github/
│   ├── workflows/
│   │   └── daily-analysis.yml      # Main workflow configuration
│   └── scripts/
│       ├── analyzer.py             # Core analysis engine
│       ├── changelog_generator.py  # CHANGELOG.md generator
│       ├── readme_updater.py       # README.md updater
│       └── create_summary.py       # GitHub Actions summary creator
└── README.md
```

## Usage

### Manual Analysis

Run the analysis locally:

```bash
python .github/scripts/analyzer.py
```

### Generate Changelog

```bash
python .github/scripts/changelog_generator.py
```

### Update README

```bash
python .github/scripts/readme_updater.py
```

## Configuration

### Workflow Schedule

Edit `.github/workflows/daily-analysis.yml` to customize:
- Cron schedule (default: daily at 2 AM UTC)
- Python version (default: 3.11)
- Tool installation options

### Analysis Settings

Modify `.github/scripts/analyzer.py` to adjust:
- Excluded directories
- File scan limits
- Timeout values
- Complexity thresholds

## Outputs

- **analysis_results.json**: Raw analysis data
- **CHANGELOG.md**: Auto-generated changelog from git history
- **README.md**: Updated with analysis results (below this section)
- **.github/analysis_history.json**: Historical trend data

## License

MIT License

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.
