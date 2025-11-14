# 🚀 Setup Guide: Repo Health Dashboard & LOC Trends

This guide will help you integrate the **Repository Health Dashboard** and **Lines of Code Trend Graphs** into your Git-Helper project.

## 📋 Table of Contents

- [Features Overview](#features-overview)
- [Quick Start](#quick-start)
- [Local Testing](#local-testing)
- [GitHub Actions Integration](#github-actions-integration)
- [Configuration](#configuration)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)

## ✨ Features Overview

### 🏥 Repository Health Dashboard

Generates a comprehensive health dashboard with:

- **Code Coverage** - Percentage and line counts
- **Lint Score** - Overall code quality score (0-10)
- **Active Contributors** - Contributors in the last 90 days
- **Commit Frequency** - Activity over last 30 days
- **Top Modified Files** - Most frequently changed files
- **Error Hotspots** - Files with most issues

### 📈 Lines of Code Trends

Generates beautiful visualizations showing:

- **LOC Trend** - Total and code lines over time
- **Change Activity** - Daily added/deleted lines
- **Language Distribution** - Code breakdown by language
- **Repository Overview** - Combined metrics

## 🚀 Quick Start

### Prerequisites

Make sure you have:
- Python 3.11+ installed
- Git repository initialized
- Existing analysis results (or run analyzer first)

### Installation

1. **Install Required Python Packages**

```bash
pip install matplotlib
```

2. **Install cloc (optional but recommended)**

For better LOC counting accuracy:

```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y cloc

# macOS
brew install cloc

# Windows (with Chocolatey)
choco install cloc
```

### Running Manually

You can test each component individually:

#### 1️⃣ Generate Health Dashboard

```bash
# Step 1: Collect metrics
python .github/scripts/repo_health_metrics.py

# Step 2: Generate dashboard
python .github/scripts/repo_health_dashboard.py --output HEALTH_DASHBOARD.md

# Step 3: Inject into README (optional)
python .github/scripts/repo_health_dashboard.py --inject-readme
```

#### 2️⃣ Generate LOC Trends

```bash
# Step 1: Collect LOC data
python .github/scripts/loc_trend_collector.py

# Step 2: Generate visualizations
python .github/scripts/loc_trend_visualizer.py --format png svg --summary
```

## 🧪 Local Testing

### Test the Complete Workflow

Run this comprehensive test to verify everything works:

```bash
#!/bin/bash
echo "🧪 Testing Repo Health Dashboard & LOC Trends"
echo "=============================================="
echo ""

# 1. Run main analyzer (if not already run)
echo "📊 Running main analyzer..."
python .github/scripts/analyzer.py
echo ""

# 2. Test Health Dashboard
echo "🏥 Testing Health Dashboard..."
python .github/scripts/repo_health_metrics.py
python .github/scripts/repo_health_dashboard.py --inject-readme
echo ""

# 3. Test LOC Trends
echo "📈 Testing LOC Trends..."
python .github/scripts/loc_trend_collector.py
python .github/scripts/loc_trend_visualizer.py --format png svg --summary
echo ""

# 4. Check generated files
echo "✅ Checking generated files..."
echo ""

if [ -f "repo_health_metrics.json" ]; then
    echo "✅ repo_health_metrics.json created"
else
    echo "❌ repo_health_metrics.json missing"
fi

if [ -f "HEALTH_DASHBOARD.md" ]; then
    echo "✅ HEALTH_DASHBOARD.md created"
else
    echo "❌ HEALTH_DASHBOARD.md missing"
fi

if [ -f ".github/loc_history.json" ]; then
    echo "✅ .github/loc_history.json created"
else
    echo "❌ .github/loc_history.json missing"
fi

if [ -d "loc_charts" ]; then
    echo "✅ loc_charts/ directory created"
    echo "   Files: $(ls -1 loc_charts/ | wc -l)"
else
    echo "❌ loc_charts/ directory missing"
fi

if [ -f "LOC_TRENDS.md" ]; then
    echo "✅ LOC_TRENDS.md created"
else
    echo "❌ LOC_TRENDS.md missing"
fi

echo ""
echo "=============================================="
echo "✅ Testing complete!"
```

Save this as `test_features.sh` and run:

```bash
chmod +x test_features.sh
./test_features.sh
```

## ⚙️ GitHub Actions Integration

### Automatic Integration

The features are **already integrated** into your GitHub Actions workflow!

The workflow will automatically:

1. ✅ Install required tools (matplotlib, cloc)
2. ✅ Collect health metrics
3. ✅ Generate health dashboard
4. ✅ Collect LOC data
5. ✅ Generate visualizations
6. ✅ Commit and push results

### Workflow Schedule

The workflow runs:

- **Daily at 2 AM UTC** (configurable)
- **On manual trigger** from GitHub Actions UI
- **When workflow files are modified**

### Manual Trigger

To trigger the workflow manually:

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **Advanced Repository Analysis**
4. Click **Run workflow**

## 🎨 Customization

### Health Dashboard Thresholds

Edit `.github/scripts/repo_health_dashboard.py`:

```python
# Line ~109 - Adjust status thresholds
coverage_emoji = self._get_status_emoji(coverage_pct, 80, 50)  # Good: 80%, OK: 50%
lint_emoji = self._get_status_emoji(lint_score, 7, 5)          # Good: 7, OK: 5
```

### LOC History Retention

Edit `.github/scripts/loc_trend_collector.py`:

```python
# Line ~373 - Change retention period
cutoff_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")  # Change 90 to desired days
```

### Chart Formats

Generate different formats:

```bash
# PNG only (default)
python .github/scripts/loc_trend_visualizer.py --format png

# SVG only
python .github/scripts/loc_trend_visualizer.py --format svg

# Both formats
python .github/scripts/loc_trend_visualizer.py --format png svg
```

### Chart Output Directory

```bash
python .github/scripts/loc_trend_visualizer.py --output-dir my_charts
```

## 📁 File Structure

After running, you'll have:

```
.
├── .github/
│   ├── scripts/
│   │   ├── repo_health_metrics.py        # Metrics collector
│   │   ├── repo_health_dashboard.py      # Dashboard generator
│   │   ├── loc_trend_collector.py        # LOC data collector
│   │   └── loc_trend_visualizer.py       # Chart generator
│   ├── workflows/
│   │   └── daily-analysis.yml            # Updated workflow
│   └── loc_history.json                  # LOC history data
├── loc_charts/                           # Generated charts
│   ├── loc_trend.png
│   ├── loc_trend.svg
│   ├── change_activity.png
│   ├── change_activity.svg
│   ├── language_distribution.png
│   ├── language_distribution.svg
│   ├── overview.png
│   └── overview.svg
├── repo_health_metrics.json              # Raw metrics data
├── HEALTH_DASHBOARD.md                   # Dashboard markdown
├── LOC_TRENDS.md                         # LOC summary with charts
└── README.md                             # Updated with dashboard
```

## 🔧 Configuration Options

### Repo Health Metrics

```bash
# Collect metrics
python .github/scripts/repo_health_metrics.py

# Custom output file
python .github/scripts/repo_health_metrics.py --output my_metrics.json
```

### Dashboard Generator

```bash
# Generate dashboard
python .github/scripts/repo_health_dashboard.py \
  --metrics repo_health_metrics.json \
  --output HEALTH_DASHBOARD.md \
  --inject-readme \
  --readme README.md
```

### LOC Collector

```bash
# Collect with custom history file
python .github/scripts/loc_trend_collector.py \
  --history-file .github/my_loc_history.json
```

### Chart Generator

```bash
# Full customization
python .github/scripts/loc_trend_visualizer.py \
  --history .github/loc_history.json \
  --format png svg \
  --output-dir my_charts \
  --summary
```

## 📊 README Integration

### Automatic Injection

The dashboard is automatically injected into README.md between markers:

```markdown
<!-- HEALTH_DASHBOARD_START -->

[Dashboard content will be here]

<!-- HEALTH_DASHBOARD_END -->
```

### Manual Markers

If you want to control where the dashboard appears, add these markers to your README:

```markdown
## Your Section

Some content...

<!-- HEALTH_DASHBOARD_START -->
<!-- HEALTH_DASHBOARD_END -->

More content...
```

The dashboard will be inserted between the markers on the next run.

## 🐛 Troubleshooting

### Issue: "matplotlib not available"

**Solution:**
```bash
pip install matplotlib
```

### Issue: "cloc command not found"

**Solution:**
The system falls back to manual counting. For better accuracy, install cloc:

```bash
# Ubuntu/Debian
sudo apt-get install cloc

# macOS
brew install cloc
```

### Issue: "No metrics data found"

**Solution:**
Run the main analyzer first:
```bash
python .github/scripts/analyzer.py
```

### Issue: "Not enough data for visualizations"

**Solution:**
You need at least 2 data points. Run the collector multiple times (or wait for daily runs):
```bash
# Run today
python .github/scripts/loc_trend_collector.py

# Run tomorrow and then generate charts
python .github/scripts/loc_trend_visualizer.py
```

### Issue: Charts not showing in README

**Solution:**
Make sure the chart paths are correct. If you changed the output directory, update the paths in `LOC_TRENDS.md`.

### Issue: GitHub Actions failing

**Solution:**
Check the Actions log for specific errors. Common issues:
- Python version compatibility
- Missing dependencies
- Permission issues

## 🎯 Best Practices

1. **Run analyzer first** - Health metrics depend on analysis results
2. **Commit charts to repo** - So they display in README
3. **Use both PNG and SVG** - PNG for GitHub, SVG for scalability
4. **Regular collection** - Daily runs provide best trends
5. **Monitor history size** - Old data is auto-cleaned after 90 days

## 📈 Usage Examples

### Example 1: Quick Health Check

```bash
# Get quick health snapshot
python .github/scripts/repo_health_metrics.py
cat repo_health_metrics.json | python -m json.tool
```

### Example 2: Generate Report for PR

```bash
# Generate complete report
python .github/scripts/repo_health_metrics.py
python .github/scripts/repo_health_dashboard.py --output HEALTH_REPORT.md

# Attach HEALTH_REPORT.md to your PR
```

### Example 3: Track Feature Development

```bash
# Before starting feature
python .github/scripts/loc_trend_collector.py

# ... develop feature ...

# After completing feature
python .github/scripts/loc_trend_collector.py
python .github/scripts/loc_trend_visualizer.py --format png --summary

# See the LOC impact of your feature
```

## 🔐 Security Notes

- Scripts run with `continue-on-error: true` in GitHub Actions
- No sensitive data is collected or stored
- All data stays in your repository
- Charts are generated locally, no external services

## 📞 Support

If you encounter issues:

1. Check this troubleshooting guide
2. Review GitHub Actions logs
3. Open an issue on the repository
4. Check script output for detailed error messages

## 🎉 You're All Set!

The features are now integrated and ready to use. The GitHub Actions workflow will automatically:

- ✅ Collect health metrics daily
- ✅ Generate beautiful dashboards
- ✅ Track LOC trends over time
- ✅ Create visualizations
- ✅ Update your README
- ✅ Commit results

Just sit back and watch your repository health improve! 🚀

---

**Made with ❤️ for Git-Helper**
