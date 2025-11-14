# Git-Buddy Advanced Features Guide

**Complete guide to all analysis capabilities, metrics, and advanced features.**

---

## 📊 Core Metrics Explained

### Code Quality Score (0-10)
- **Source:** Pylint analysis
- **Measures:** Code style, complexity, errors, warnings
- **Interpretation:**
  - 8-10: Excellent code quality
  - 6-8: Good quality, room for improvement
  - 4-6: Needs refactoring
  - 0-4: Critical issues
- **Action:** Scores below 6.0 trigger recommendations

### Cyclomatic Complexity
- **Source:** Radon analysis
- **Measures:** Number of decision paths in code
- **Interpretation:**
  - 1-5: Simple, easy to test
  - 5-7: Moderate, testable
  - 7-15: Complex, refactor suggested
  - 15+: Very complex, definitely refactor
- **Action:** Default threshold is 15

### Test Coverage (%)
- **Source:** pytest-cov
- **Measures:** Percentage of code executed by tests
- **Interpretation:**
  - 80-100%: Excellent
  - 60-80%: Good
  - 40-60%: Needs improvement
  - <40%: Critical gap
- **Action:** Coverage gaps highlighted in reports

### Security Vulnerabilities
- **Sources:** Bandit (code), pip-audit & safety (dependencies)
- **Types:**
  - **Critical:** Security risk, must fix immediately
  - **High:** Significant risk, fix soon
  - **Medium:** Moderate risk, plan fix
  - **Low:** Minor risk, monitor
- **Action:** Any vulnerability triggers alert

---

## 🔧 Advanced Features

### 1. Technical Debt Index
**Composite metric combining multiple factors to show overall debt burden.**

**Components (weighted):**
- Code Quality Issues (30%)
- Complexity Hotspots (25%)
- Test Coverage Gaps (20%)
- Dependency Vulnerabilities (15%)
- Code Duplication (10%)

**Severity Levels:**
- 0-20: HEALTHY
- 20-40: ACCEPTABLE
- 40-60: WARNING
- 60-80: CRITICAL
- 80-100: EXTREME

**Generated:** In analysis reports and HEALTH_DASHBOARD.md

---

### 2. Metric Degradation Alerts
**Automatically detects when metrics are getting worse.**

**Monitored Changes:**
- Code quality declined by >0.5 points
- Complexity increased by >1.0
- Test coverage dropped by >2%
- New vulnerabilities detected

**Alert Severity:**
- CRITICAL: Security issue (new vulnerabilities)
- WARNING: Quality declining, coverage dropping
- MEDIUM: Complexity increasing

**Actions:**
- Displayed in HEALTH_DASHBOARD.md
- Included in GitHub Actions summary
- Can trigger GitHub issues (if configured)

---

### 3. Code Duplication Detection
**Identifies repeated code blocks that should be refactored.**

**Detection Method:**
- Line-by-line comparison after normalization
- Ignores whitespace and comments
- Identifies duplicate code blocks
- Shows percentage of duplicated code

**Thresholds:**
- 0-5%: Acceptable
- 5-15%: Needs attention
- 15%+: Significant issue

**Recommendations:**
- Extract to shared functions
- Use inheritance for similar classes
- Apply DRY principle

---

### 4. Historical Trend Analysis
**Tracks metrics over time to identify patterns and trends.**

**Data Collected:**
- **Daily:** Code quality, coverage, LOC, complexity
- **Preserved:** All history never deleted
- **Visualized:** Trend charts with growth patterns
- **Analyzed:** Linear regression for trend direction

**Available Trends:**
- LOC growth/shrinkage
- Quality improvement/decline
- Coverage progress
- Complexity changes
- Contributor activity

**Insights Provided:**
- Growth trajectory
- Pace of improvement
- Anomalies and spikes
- Velocity indicators

---

### 5. Repository Health Dashboard
**Comprehensive human-readable health report.**

**Sections in HEALTH_DASHBOARD.md:**
- Overall Health Score
- Key Metrics (quality, coverage, security)
- Strengths (what's going well)
- Weaknesses (needs improvement)
- Trend Analysis (improving/declining)
- Actionable Recommendations
- Hotspot Identification
- Contributor Activity

---

### 6. Automated README Updates
**Keeps README.md synchronized with latest metrics.**

**Inserted Badges:**
- Code Quality Score
- Test Coverage Percentage
- Security Status
- Build Status
- Dependency Status

**Updated Sections:**
- Project Health
- Metrics Dashboard
- Recent Statistics
- Quality Indicators

**Preservation:**
- All existing content preserved
- Only updates marked sections
- Uses HTML comment markers
- Safe for manual edits outside markers

---

### 7. Automatic Changelog Generation
**Creates CHANGELOG.md from git commit history.**

**Features:**
- Intelligent commit categorization
- Version grouping
- Feature/bug/breaking change detection
- Contributor attribution
- Release date tracking

**Commit Message Parsing:**
- `feat:` → Features
- `fix:` → Bug Fixes
- `BREAKING:` → Breaking Changes
- `docs:` → Documentation
- `test:` → Tests

---

### 8. GitHub Actions Integration
**Results visible directly in GitHub without leaving the platform.**

**Displays:**
- Job Summary in Actions UI
- Key metrics in readable format
- Pass/fail indicators
- Links to generated reports
- Execution time and details

---

## 🎯 Use Cases

### For Individual Developers
**Goal:** Improve code quality

**Recommended Settings:**
```env
ENABLE_CODE_QUALITY=true
MIN_CODE_QUALITY_SCORE=7.0
MIN_TEST_COVERAGE=80
```

**Focus On:**
- Code Quality Score
- Test Coverage Gaps
- Technical Debt Index

---

### For Teams
**Goal:** Maintain standards across projects

**Recommended Settings:**
```env
ENABLE_CODE_QUALITY=true
ENABLE_SECURITY_SCAN=true
MIN_CODE_QUALITY_SCORE=6.0
MIN_TEST_COVERAGE=70
```

**Focus On:**
- Trend Analysis
- Metric Degradation Alerts
- Health Dashboard
- Dependency Vulnerabilities

---

### For Security-First Projects
**Goal:** Minimize security risks

**Recommended Settings:**
```env
ENABLE_SECURITY_SCAN=true
ENABLE_CODE_QUALITY=true
```

**Focus On:**
- Vulnerability Count
- Dependency Health
- Security Alerts
- Bandit Findings

---

### For Data-Driven Development
**Goal:** Understand code evolution

**Recommended Settings:**
```env
ENABLE_LOC_TREND=true
ENABLE_HEALTH_DASHBOARD=true
```

**Focus On:**
- Historical Trends
- Growth Patterns
- Quality Evolution
- Velocity Metrics

---

## 🚀 Performance Notes

### Execution Time
- **First Run:** 2-5 minutes (depends on repo size)
- **Subsequent Runs:** 1-3 minutes (cached analysis)
- **Trending Runs:** Minimal overhead

### Storage
- **Per Run:** ~100KB of JSON data
- **Monthly History:** ~3MB (30 days)
- **Yearly History:** ~36MB (365 days)
- **Artifacts:** 30-day retention in GitHub

### Resource Usage
- **CPU:** Minimal (analysis only)
- **Memory:** 256MB average, 512MB peak
- **GitHub Actions Minutes:** ~10-15 per run

---

## 🔐 Privacy & Security

### Data Handling
- ✅ All analysis happens locally in GitHub Actions
- ✅ No data sent to external services
- ✅ No tracking or analytics
- ✅ Results stored only in your repository
- ✅ Historical data never deleted (unless manually)

### Security Tools
- **Bandit:** Detects code security issues
- **Pip-Audit:** Finds vulnerable packages
- **Safety:** Checks for known CVEs
- **Pylint/Flake8:** Code quality/style

---

## 📈 Interpretation Guide

### Code Quality Declining
**What it means:** Issues introduced in recent commits
**Action:** Review recent changes and refactor problematic code

### Coverage Dropping
**What it means:** New code added without tests
**Action:** Write tests for new functionality before merging

### Complexity Increasing
**What it means:** Functions becoming harder to maintain
**Action:** Refactor large functions into smaller units

### New Vulnerabilities
**What it means:** Dependency packages have known CVEs
**Action:** Update packages immediately

### Technical Debt Increasing
**What it means:** Multiple issues accumulating
**Action:** Allocate time for refactoring in sprint planning

---

## 🛠️ Customization

### Adjusting Thresholds
Edit `.env` file in your repository:
```bash
MIN_CODE_QUALITY_SCORE=7.0  # Stricter than default
MAX_COMPLEXITY=10           # Lower than default
MIN_TEST_COVERAGE=85        # Higher than default
```

### Excluding Directories
```bash
EXCLUDED_DIRS=node_modules,venv,.git,tests/fixtures
```

### Running on Different Schedule
Edit `.github/workflows/daily-analysis.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours instead of daily
```

---

## 🔄 Integration with Your Workflow

### GitHub Issues
When critical issues are found, create GitHub issues to track them.

### Pull Requests
Quality checks can be run on PRs to prevent regressions.

### Slack/Discord
Integrate job summary with notifications for team awareness.

### Dashboards
Embed HEALTH_DASHBOARD.md in your project wiki or documentation.

---

## 📊 Example Dashboard Output

```markdown
## Repository Health Dashboard

### Overall Health Score: 78/100 ✅

### Key Metrics
| Metric | Value | Status |
|--------|-------|--------|
| Code Quality | 7.5/10 | ✅ Good |
| Test Coverage | 82% | ✅ Excellent |
| Security Vulnerabilities | 0 | ✅ Secure |
| Cyclomatic Complexity | 8.2 | ⚠️ Monitor |
| Lines of Code | 5,234 | 📈 Stable |

### Strengths
- ✅ No security vulnerabilities
- ✅ Good test coverage (82%)
- ✅ Code quality improving

### Weaknesses
- ⚠️ Some functions too complex
- 📝 3 areas of duplicate code
- 📊 Coverage gaps in utils/

### Recommendations
1. Refactor 2 complex functions (radon flags them)
2. Add tests for utility module (15% coverage gap)
3. Extract duplicated validator logic into shared function
```

---

## 🆘 Troubleshooting

### Metrics Not Updating
- Check GitHub Actions for errors
- Verify `.github/workflows/daily-analysis.yml` is present
- Check if GitHub Actions are enabled in settings

### Low Coverage Reported
- Check if pytest is finding tests
- Verify test files match discovery patterns
- Check for excluded test directories

### False Security Alerts
- Review vulnerability details
- Check if it applies to your code
- Update to patched version if available

### Trends Not Showing
- Need at least 2 days of history
- Wait for second daily run
- Check `.github/loc_history.json` exists

---

**Need Help?** See ARCHITECTURE.md or visit the "🔧 How It Works" tab in the Streamlit app!
