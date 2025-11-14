# Zero-Code Setup Guide

Get Git-Buddy running with just a few simple steps - no code editing required!

## Option 1: GitHub Actions (Recommended - Fully Automatic)

This is the easiest setup. Everything runs automatically!

### Steps:
1. **Copy the repo** to your GitHub account
2. **Enable GitHub Actions** in Settings → Actions → Allow all actions
3. **That's it!** 🎉

The workflow runs automatically:
- Daily at 2 AM UTC
- On manual trigger via GitHub Actions UI
- When workflow files change

### What Happens Automatically:
- ✅ Code quality analysis (pylint, flake8)
- ✅ Security scanning (bandit, pip-audit)
- ✅ Test coverage detection
- ✅ Dependency health checks
- ✅ Changelog generation
- ✅ README updates
- ✅ Health dashboard generation
- ✅ Lines of Code trends

---

## Option 2: Local Setup (5 minutes)

Want to run analysis on your machine? Follow these steps:

### Step 1: Clone & Enter Directory
```bash
git clone <repository-url>
cd Git-Buddy
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Copy Configuration (Optional)
```bash
cp .env.example .env
```

### Step 5: Run Analysis
Choose what you want to run:

**Run everything:**
```bash
python .github/scripts/analyzer.py
python .github/scripts/changelog_generator.py
python .github/scripts/readme_updater.py
python .github/scripts/repo_health_metrics.py
```

**Run specific analysis:**
```bash
# Code quality analysis
python .github/scripts/analyzer.py

# Generate changelog
python .github/scripts/changelog_generator.py

# Health dashboard
python .github/scripts/repo_health_metrics.py
```

---

## Option 3: Docker (One Command)

Don't want to install anything? Use Docker!

```bash
docker run --rm -v $(pwd):/repo -w /repo python:3.11 \
  bash -c "pip install -r requirements.txt && python .github/scripts/analyzer.py"
```

---

## Configuration (Optional)

Edit `.env` to customize behavior:

```bash
cp .env.example .env
# Edit .env with your settings
```

Available options:
- `ENABLE_CODE_QUALITY=true/false` - Toggle code analysis
- `ENABLE_SECURITY_SCAN=true/false` - Toggle security scanning
- `ENABLE_HEALTH_DASHBOARD=true/false` - Toggle health dashboard
- `MIN_COVERAGE_PERCENT=70` - Minimum code coverage threshold
- `EXCLUDED_DIRS=.git,__pycache__` - Directories to skip

---

## What Gets Generated?

After running, you'll get:

| File | Purpose |
|------|---------|
| `analysis_results.json` | Raw analysis data |
| `CHANGELOG.md` | Auto-generated changelog |
| `HEALTH_DASHBOARD.md` | Repository health metrics |
| `repo_health_metrics.json` | Health data (JSON) |
| `.github/loc_history.json` | Lines of code history |
| `README.md` | Updated with results |

---

## Troubleshooting

### Missing Python Tools
```bash
pip install -r requirements.txt
```

### Missing System Tools (cloc)
```bash
# Ubuntu/Debian
sudo apt-get install cloc

# macOS
brew install cloc

# Or skip it - analysis continues without it
```

### Permission Denied on Scripts
```bash
chmod +x .github/scripts/*.py
```

### Out of Memory
Reduce file scan limits in the scripts or exclude large directories in `.env`

---

## Key Features (No Code Writing Required)

✨ **Automatic Everything:**
- Copy configuration files ✓
- Install requirements ✓
- Run scripts ✓
- Review results ✓

📊 **Detailed Metrics:**
- Code complexity
- Test coverage
- Security vulnerabilities
- Dependency health
- Historical trends

🔄 **Continuous Integration:**
- Runs daily automatically
- Creates detailed reports
- Updates documentation
- Tracks metrics over time

---

## Next Steps

1. Choose your setup option above
2. Follow the steps
3. Check the generated reports
4. (Optional) Customize `.env` for your needs

That's it! No code editing required. 🚀
