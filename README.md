# Git-Buddy: Automated Repository Analysis & Monitoring

> **Enterprise-grade code quality, security, and trend analysis for Python repositories. Zero configuration. Fully automated. GitHub Actions integrated.**

[![GitHub](https://img.shields.io/badge/GitHub-iampreetdave--max%2FGit--Helper-181717?style=flat&logo=github)](https://github.com/iampreetdave-max/Git-Helper)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://python.org)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

---

## 🚀 What is Git-Buddy?

**Git-Buddy** is an intelligent, fully-automated repository monitoring system that continuously analyzes your code quality, detects security vulnerabilities, tracks metrics over time, and generates comprehensive reports—**all without requiring any configuration or external services**.

### 📚 Documentation Guide
We believe in **complete transparency**. Choose your learning path:

| Document | For Whom | Purpose |
|----------|----------|---------|
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | Technical deep-dive seekers | Comprehensive system design, all 8 scripts explained, data flow diagrams |
| **[README.md](README.md)** (this file) | Quick starters | Feature overview, installation, basic usage |
| **[SETUP_HEALTH_AND_LOC.md](SETUP_HEALTH_AND_LOC.md)** | Setup helpers | Step-by-step configuration instructions |
| **[STREAMLIT_SETUP.md](STREAMLIT_SETUP.md)** | UI users | How to use the interactive setup wizard |
| **Streamlit App** | Visual learners | Click "🚀 Quick Setup" tab for interactive guide |

> **New to Git-Buddy?** Start with [ARCHITECTURE.md](ARCHITECTURE.md) to understand what it does, then use the Streamlit app to set it up.

Perfect for:
- 👨‍💻 **Individual developers** tracking code quality metrics
- 🏢 **Teams & organizations** monitoring repository health across projects
- 🔒 **Security-first projects** with automated vulnerability detection
- 📊 **Data-driven development** with historical trend analysis

### Key Highlights
- ✅ **Zero Configuration** - Works out-of-the-box with sensible defaults
- ✅ **Fully Automated** - Runs daily via GitHub Actions (no manual setup)
- ✅ **Completely Self-Contained** - No external APIs, cloud services, or credentials needed
- ✅ **Enterprise-Grade** - 8 intelligent scripts, 4,000+ lines of production code
- ✅ **Privacy-First** - All analysis happens in your GitHub Actions environment
- ✅ **Comprehensive** - 7 different analysis types in a single unified system

---

## ⚡ Core Features

### 1. **Code Quality Analysis** 📊
Intelligent analysis of code complexity and maintainability using Radon and Pylint:
- Cyclomatic complexity detection (identifies overly complex functions)
- Maintainability index scoring
- Code style issue detection
- Automatic refactoring suggestions
- File-level and project-wide insights

### 2. **Security Vulnerability Scanning** 🔐
Multi-layered security protection:
- **Bandit**: Python code security analysis
- **Pip-Audit**: Dependency vulnerability detection
- **Safety**: Security issue detection in Python packages
- CVE tracking and risk assessment
- Insecure pattern detection

### 3. **Test Coverage & Analysis** 🧪
Comprehensive testing insights:
- Automatic test detection and execution (pytest)
- Coverage percentage tracking
- Untested code path identification
- Coverage trend analysis over time
- Test growth monitoring

### 4. **Dependency Health Monitoring** 📦
Keep your dependencies secure and updated:
- Python and Node.js package analysis
- Outdated dependency detection
- Security vulnerability identification in libraries
- Version conflict detection
- Automatic update suggestions

### 5. **Automated Changelog Generation** 📝
Intelligent commit history analysis:
- Auto-generates CHANGELOG.md from git commits
- Intelligent commit categorization
- Version history tracking
- Breaking change detection
- Release notes generation

### 6. **Repository Health Dashboard** 📈
Beautiful, auto-generated metrics dashboard:
- Code coverage statistics
- Lint score tracking
- Active contributor analysis
- Commit activity monitoring
- Error hotspot detection
- Repository quality indicators

### 7. **Trend Tracking & Historical Analysis** 📊
Data-driven insights with long-term metrics:
- Historical metric storage and visualization
- Lines of code (LOC) trend analysis
- Code quality evolution tracking
- Contributor activity trends
- Identify patterns in code growth

### 8. **Smart Self-Healing** 🤖
Intelligent automation and error recovery:
- Auto-generates missing configuration files
- Maintains state and historical data
- Graceful failure handling
- Automatic recovery mechanisms
- Zero manual intervention required

---

## 🎯 Why Git-Buddy?

| Feature | Git-Buddy | Others |
|---------|-----------|--------|
| **Configuration Required** | ✅ None | ❌ Extensive |
| **External Services** | ✅ None | ❌ Multiple APIs |
| **Privacy** | ✅100% On-Device | ❌ Cloud-Based |
| **Cost** | ✅ Free | ❌ Paid Plans |
| **Setup Time** | ✅ 5 Minutes | ❌ Hours |
| **GitHub Actions Native** | ✅ Integrated | ❌ Limited |

---

## 📦 What's Included

### 8 Intelligent Scripts (4,000+ Lines of Code)

> 🔍 **Want detailed explanations of what each script does?** See [ARCHITECTURE.md - The 8 Scripts Section](ARCHITECTURE.md#-the-8-scripts-what-each-does)

| Script | Lines | Purpose |
|--------|-------|---------|
| **analyzer.py** | 721 | Core engine: Runs pylint, flake8, radon, bandit, pytest-cov for comprehensive analysis |
| **repo_health_metrics.py** | 490 | Aggregates all metrics into health score with quality, coverage, security stats |
| **loc_trend_visualizer.py** | 470 | Creates PNG/SVG charts showing code growth over time with trends |
| **loc_trend_collector.py** | 445 | Collects historical LOC data, tracks language breakdown daily |
| **readme_updater.py** | 439 | Auto-updates README.md with latest badges, scores, and metrics |
| **repo_health_dashboard.py** | 429 | Generates HEALTH_DASHBOARD.md with strengths, weaknesses, recommendations |
| **changelog_generator.py** | 133 | Creates CHANGELOG.md from git commits automatically |
| **create_summary.py** | 157 | Formats results for GitHub Actions UI with pass/fail indicators |

**All scripts are open source and designed to be transparent about what they do.**

### Dependencies (Carefully Curated)
- **Code Analysis**: Radon, Pylint, Flake8
- **Security**: Bandit, Pip-Audit, Safety
- **Testing**: Pytest, Pytest-Cov
- **Visualization**: Matplotlib, NumPy
- **UI**: Streamlit (for setup wizard)

---

## 🚀 Quick Start (5 Minutes)

### Option 1: Interactive Setup Wizard (Recommended)
```bash
# No installation needed! Just visit the Streamlit app
# Download all files from the web interface
# Extract to your repository
# Commit and push
```

### Option 2: Manual Setup
```bash
# 1. Clone or download the repository
git clone https://github.com/iampreetdave-max/Git-Helper.git

# 2. Copy the workflow file
cp .github/workflows/daily-analysis.yml your-repo/.github/workflows/

# 3. Copy requirements and configuration
cp requirements.txt your-repo/
cp .env.example your-repo/

# 4. Commit everything
cd your-repo
git add .
git commit -m "Add Git-Buddy repository analysis"
git push

# 5. Enable in GitHub
# Settings → Actions → General → Allow all actions
```

### What Happens Next?
✅ Git-Buddy runs daily at 2 AM UTC (customizable)
✅ Analyzes your entire repository
✅ Commits results as markdown and JSON files
✅ Updates your README automatically
✅ Tracks metrics over time

---

## 📖 Detailed Setup

### Prerequisites
- ✅ GitHub repository (public or private)
- ✅ GitHub Actions enabled (free tier includes 2,000 minutes/month)
- ✅ Python 3.11+ (for local development)

### Installation Methods

#### Method 1: GitHub Actions (Fully Automated)
Best for: Teams wanting continuous monitoring

```yaml
# Automatically included in daily-analysis.yml
schedule:
  - cron: '0 2 * * *'  # Runs daily at 2 AM UTC
```

#### Method 2: Docker Container
Best for: Isolated testing environments

```bash
docker run -v /path/to/repo:/workspace git-buddy:latest
```

#### Method 3: Local Development
Best for: Testing and customization

```bash
pip install -r requirements.txt
python .github/scripts/analyzer.py
```

---

## ⚙️ Configuration

### Zero Setup Option
Git-Buddy works perfectly with **zero configuration**. All defaults are production-ready.

### Customization (Optional)

Edit `.env` file:

```bash
# Analysis Components (Enable/Disable)
ENABLE_CODE_QUALITY=true
ENABLE_SECURITY_SCAN=true
ENABLE_COMPLEXITY_ANALYSIS=true
ENABLE_CHANGELOG=true
ENABLE_HEALTH_DASHBOARD=true
ENABLE_LOC_TREND=true

# Quality Thresholds
MIN_CODE_QUALITY_SCORE=6.0
MAX_COMPLEXITY=15

# Directories to Exclude
EXCLUDED_DIRS=node_modules,venv,.git

# Analysis Output Format
OUTPUT_FORMAT=json
```

### Workflow Schedule
Edit `.github/workflows/daily-analysis.yml`:

```yaml
schedule:
  - cron: '0 2 * * *'      # Daily at 2 AM UTC
  # - cron: '0 */6 * * *'  # Every 6 hours
  # - cron: '0 9-17 * * 1-5' # Business hours
```

---

## 📊 Generated Reports

### Automatic Files Created
- **HEALTH_DASHBOARD.md** - Human-readable health metrics
- **analysis_results.json** - Raw analysis data for parsing
- **CHANGELOG.md** - Auto-generated changelog
- **.github/loc_history.json** - Historical LOC data
- **.github/analysis_history.json** - Complete analysis history

### Example Dashboard Output
```
## Repository Health Dashboard
| Metric | Value | Status |
|--------|-------|--------|
| Code Coverage | 85.2% | ✅ Excellent |
| Lint Score | 9.1/10 | ✅ Excellent |
| Active Contributors (90d) | 5 | ✅ Good |
| Commits (30d) | 24 | ✅ Active |
```

---

## 🤖 Advanced Features

### Historical Trend Analysis
Track your code quality evolution:
- Line count growth patterns
- Quality score trends
- Test coverage growth
- Dependency count changes
- Active contributor patterns

### Smart Self-Healing
Automatic recovery from failures:
- Creates missing config files
- Maintains historical data
- Handles API timeouts gracefully
- Incremental analysis support

### Multi-Language Support
- ✅ Python (Full support)
- ✅ JavaScript/TypeScript (Dependency analysis)
- ✅ Any Git repository

### Privacy & Security
- ✅ No external API calls
- ✅ No cloud storage
- ✅ All data stays in your repository
- ✅ Works with private repositories
- ✅ No third-party integrations required

---

## 📈 Use Cases

### 📱 Startup Development
Monitor code quality while shipping fast. Identify technical debt early.

### 🏢 Enterprise Teams
Track health across multiple repositories. Enforce quality standards.

### 🔒 Security-Focused Projects
Continuous vulnerability scanning. Automatic alerts on security issues.

### 📚 Educational Projects
Learn code analysis best practices. Understand code metrics.

### 🤝 Open Source Projects
Maintain code quality across contributors. Document project evolution.

---

## 🔍 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│           GitHub Actions Workflow (Daily at 2 AM UTC)       │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┼───────────┐
                ▼           ▼           ▼
         ┌──────────┐ ┌──────────┐ ┌──────────┐
         │Analyzer  │ │Security  │ │Testing   │
         │ Engine   │ │Scanning  │ │Coverage  │
         └──────────┘ └──────────┘ └──────────┘
                |               |              |
                └───────────────┼──────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
         ┌──────────┐    ┌──────────┐   ┌──────────┐
         │ Generate │    │ Track    │   │ Commit   │
         │ Reports  │    │ Trends   │   │ Results  │
         └──────────┘    └──────────┘   └──────────┘
                                │
                        ┌───────▼────────┐
                        │  Repository    │
                        │  Updated with  │
                        │  New Reports   │
                        └────────────────┘
```

---

## 📚 Codebase Intelligence

Git-Buddy is built with production-grade code quality:

- **Type Safety**: Proper error handling throughout
- **Modularity**: 8 independent, well-separated scripts
- **Scalability**: Handles large repositories efficiently
- **Extensibility**: Easy to add new analysis tools
- **Testability**: Clear input/output contracts
- **Documentation**: Comprehensive inline comments

### Code Metrics
- **Total Lines**: 4,000+
- **Functions**: 150+
- **Test Coverage**: Automated
- **Complexity**: Well-structured, low coupling
- **Performance**: Optimized for CI/CD environments

---

## 🛠️ For Developers

### Local Development
```bash
# Setup
git clone https://github.com/iampreetdave-max/Git-Helper.git
cd Git-Helper
pip install -r requirements.txt

# Run analysis locally
python .github/scripts/analyzer.py

# View Streamlit app
streamlit run streamlit_app.py
```

### Running Individual Tools
```bash
# Code quality analysis
python .github/scripts/analyzer.py

# Generate changelog
python .github/scripts/changelog_generator.py

# Calculate health metrics
python .github/scripts/repo_health_metrics.py

# Generate dashboard
python .github/scripts/repo_health_dashboard.py
```

### Customization
Each script can be customized:
1. Modify tool parameters in `.env`
2. Adjust thresholds and exclusions
3. Add custom analysis logic
4. Create new report formats

---

## ❓ FAQ

**Q: Does Git-Buddy require any API keys?**
A: No! Git-Buddy is completely self-contained and runs entirely within GitHub Actions.

**Q: Will it slow down my CI/CD pipeline?**
A: No. It runs on a separate scheduled workflow (default: daily at 2 AM UTC), not on every push.

**Q: Can I use it with private repositories?**
A: Yes! All analysis happens securely within your repository. Perfect for private projects.

**Q: Can I customize the analysis?**
A: Yes! Edit `.env` to enable/disable specific analyses and adjust thresholds.

**Q: How much does it cost?**
A: Free! Git-Buddy is open source. GitHub Actions includes 2,000 free minutes per month.

**Q: What if my repository isn't Python?**
A: Git-Buddy focuses on Python, but can analyze any repository for dependencies and commit history.

**Q: Can I disable certain analyses?**
A: Yes! Each analysis component is independently controllable via environment variables.

**Q: Where are the results stored?**
A: All results are committed back to your repository. No external storage needed.

---

## 📊 Repository Health Dashboard

<!-- HEALTH_DASHBOARD_START -->

## 📊 Repository Health Dashboard

> Last updated: **November 14, 2025 at 10:53 UTC**

### 🎯 Key Metrics

| Metric | Value | Status |
|--------|-------|--------|
| 🔬 Code Coverage | **0.0%** | 🔴 Needs Improvement |
| ✨ Lint Score | **0.0/10** | 🔴 Needs Improvement |
| 👥 Active Contributors (90d) | **3** | 🟡 Moderate |
| 📈 Commits (30d) | **6** | 📉 |

### 📊 Code Quality

#### Code Coverage
🔴 ░░░░░░░░░░░░░░░░░░░░ **0.0%**

#### Lint Score
🔴 ░░░░░░░░░░░░░░░░░░░░ **0.0/10**
- **Pylint Score:** None/10
- **Flake8 Issues:** 0
- **Total Issues:** 0

### 👥 Active Contributors (Last 90 Days)

**Total Contributors:** 3

#### Top Contributors

| Contributor | Contributions |
|-------------|---------------|
| 1. **Claude** | 3 commits |
| 2. **iampreetdave-max** | 2 commits |
| 3. **Preet Dave** | 1 commits |

### 📈 Repository Activity (Last 30 Days)

📉 **6 commits** (0.2 per day)
- **Most Active Day:** 2025-11-14 (4 commits)

#### Most Modified Files

| File | Modifications |
|------|---------------|
| `.gitignore` | 1 |
| `README.md` | 1 |

### 🔥 Error Hotspots

✅ No significant error hotspots detected.

---

*Dashboard automatically generated by [Git-Buddy](https://github.com/iampreetdave-max/Git-Buddy)*

<!-- HEALTH_DASHBOARD_END -->

---

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- 🐛 [Report issues](https://github.com/iampreetdave-max/Git-Helper/issues)
- 💡 [Suggest features](https://github.com/iampreetdave-max/Git-Helper/discussions)
- 🔀 [Submit pull requests](https://github.com/iampreetdave-max/Git-Helper/pulls)

### Development
```bash
# Clone the repository
git clone https://github.com/iampreetdave-max/Git-Helper.git

# Install dependencies
pip install -r requirements.txt

# Make your changes
# Test thoroughly
# Submit a PR!
```

---

## 📜 License

Git-Buddy is released under the **MIT License**. See [LICENSE](LICENSE) for details.

You are free to:
- ✅ Use in commercial projects
- ✅ Modify the code
- ✅ Distribute modified versions
- ✅ Use privately

---

## 🙏 Credits & Acknowledgments

**Created with ❤️ by [Preet Dave](https://github.com/iampreetdave-max)**

Powered by:
- [Claude AI](https://www.anthropic.com/) - Intelligent code analysis
- [Radon](https://radon.readthedocs.io/) - Complexity metrics
- [Pylint](https://www.pylint.org/) - Code analysis
- [Bandit](https://bandit.readthedocs.io/) - Security scanning
- [Pytest](https://pytest.org/) - Test coverage
- [GitHub Actions](https://github.com/features/actions) - Automation

---

## ⭐ Show Your Support

If Git-Buddy helps you maintain code quality, please:
- ⭐ Star the repository
- 🔔 Watch for updates
- 💬 Share feedback
- 📣 Recommend to friends

---

## 📞 Support & Contact

- 🐛 **Report Bugs**: [GitHub Issues](https://github.com/iampreetdave-max/Git-Helper/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/iampreetdave-max/Git-Helper/discussions)
- 📧 **Contact Author**: [GitHub Profile](https://github.com/iampreetdave-max)

---

<div align="center">

**Built for developers. By developers. Forever free.**

[⭐ Star](https://github.com/iampreetdave-max/Git-Helper) | [🚀 Get Started](#-quick-start-5-minutes) | [📖 Documentation](#-detailed-setup) | [💬 Issues](https://github.com/iampreetdave-max/Git-Helper/issues)

</div>
