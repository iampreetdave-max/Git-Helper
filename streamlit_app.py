import streamlit as st
import io
import json
import zipfile
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Git-Buddy - Automated Repository Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Elegant styling with better colors and layout
st.markdown("""
    <style>
        :root {
            --primary: #2c3e50;
            --accent: #e74c3c;
            --success: #27ae60;
            --light: #ecf0f1;
            --text: #2c3e50;
        }

        * {
            font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        }

        .main-header {
            font-size: 3.5em;
            font-weight: 800;
            background: linear-gradient(135deg, #2c3e50 0%, #e74c3c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            letter-spacing: -1px;
        }

        .tagline {
            font-size: 1.3em;
            color: #666;
            margin-bottom: 30px;
            font-weight: 300;
        }

        .feature-card {
            background: linear-gradient(135deg, #f3f4f6 0%, #eff3f6 100%);
            padding: 30px;
            border-radius: 12px;
            margin: 15px 0;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }

        .feature-card:hover {
            box-shadow: 0 8px 16px rgba(0,0,0,0.12);
            transform: translateY(-2px);
        }

        .feature-icon {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .feature-title {
            font-size: 1.3em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 10px;
        }

        .feature-desc {
            color: #666;
            font-size: 0.95em;
            line-height: 1.6;
        }

        .capability-badge {
            display: inline-block;
            background: #e74c3c;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85em;
            margin: 8px 8px 8px 0;
        }

        .stat-card {
            background: #f3f4f6;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #e0e0e0;
        }

        .stat-number {
            font-size: 2.5em;
            font-weight: 800;
            color: #e74c3c;
        }

        .stat-label {
            color: #666;
            font-size: 0.95em;
            margin-top: 8px;
        }

        .step-badge {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: 700;
            display: inline-block;
            margin: 12px 0;
            font-size: 0.9em;
        }

        .code-block {
            background: #f4f4f4;
            padding: 15px;
            border-left: 4px solid #e74c3c;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            overflow-x: auto;
        }

        .highlight {
            background: #fffacd;
            padding: 2px 6px;
            border-radius: 3px;
            font-weight: 600;
        }

        .footer {
            text-align: center;
            color: #999;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
            font-size: 0.9em;
            line-height: 1.8;
        }

        .footer a {
            color: #e74c3c;
            text-decoration: none;
            font-weight: 600;
        }

        .footer a:hover {
            text-decoration: underline;
        }

        .divider {
            margin: 40px 0;
            border: 0;
            height: 1px;
            background: linear-gradient(to right, transparent, #e0e0e0, transparent);
        }

        .success-box {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 16px;
            border-radius: 8px;
            margin: 20px 0;
        }

        .info-box {
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
            padding: 16px;
            border-radius: 8px;
            margin: 20px 0;
        }

        .complexity-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown('<div class="main-header" style="font-size: 2em; text-align: center; margin: 20px 0;">Git-Buddy</div>', unsafe_allow_html=True)

    page = st.radio("Navigation:",
                    ["🏠 Home", "⚡ Features", "🔧 How It Works", "🚀 Quick Setup", "❓ FAQ", "📖 Docs"])

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    **🎯 One-Click Integration**

    Git-Buddy works with **any repository** - no setup required!
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Scripts", "8", "+700 Lines")
    with col2:
        st.metric("Analyses", "7", "Automated")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; font-size: 0.85em; color: #666;">
        <strong>Built for developers</strong><br>
        <a href="https://github.com/iampreetdave-max/Git-Helper" target="_blank">View on GitHub</a>
    </div>
    """, unsafe_allow_html=True)

# ===== HOME PAGE =====
if page == "🏠 Home":
    st.markdown('<div class="main-header">Git-Buddy</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Enterprise-Grade Repository Analysis. Zero Configuration.</div>', unsafe_allow_html=True)

    # Hero stats
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">8</div>
            <div class="stat-label">Intelligent Scripts</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">7</div>
            <div class="stat-label">Automated Analyses</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">0</div>
            <div class="stat-label">Config Required</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">∞</div>
            <div class="stat-label">Repositories</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    <strong>🚀 What is Git-Buddy?</strong><br><br>
    Git-Buddy is an intelligent repository monitoring system that automatically analyzes your code quality,
    detects security vulnerabilities, tracks metrics over time, and generates comprehensive reports—all running
    safely within your GitHub Actions environment. <strong>No external APIs. No configuration needed.</strong>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Perfect For")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👨‍💻</div>
            <div class="feature-title">Individual Developers</div>
            <div class="feature-desc">Track your code quality metrics and catch issues early before they become problems.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Security-First Teams</div>
            <div class="feature-desc">Automated vulnerability scanning with Bandit, Pip-Audit, and Safety for complete coverage.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏢</div>
            <div class="feature-title">Teams & Organizations</div>
            <div class="feature-desc">Monitor repository health across all projects with automated dashboards and trend tracking.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Data-Driven Management</div>
            <div class="feature-desc">Generate actionable insights from historical metrics and identify patterns in code evolution.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Call to action
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("👉 Use the **Quick Setup** option in the sidebar to get started!")

# ===== FEATURES PAGE =====
elif page == "⚡ Features":
    st.markdown('<div class="main-header">Powerful Capabilities</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    Git-Buddy comes equipped with intelligent analysis tools that work together to give you complete
    repository insights. Every feature runs automatically—no configuration required.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Core Analysis Capabilities")

    features = [
        {
            "icon": "📊",
            "title": "Code Quality Analysis",
            "desc": "Analyze cyclomatic complexity, maintainability index, and code patterns using Radon and Pylint",
            "details": "Identifies overly complex functions, suggests refactoring opportunities, and tracks metrics over time."
        },
        {
            "icon": "🧪",
            "title": "Test Coverage Detection",
            "desc": "Automatically detects and runs tests with comprehensive coverage reporting using pytest",
            "details": "Measures code coverage percentage, identifies untested code paths, and tracks test growth."
        },
        {
            "icon": "🔐",
            "title": "Security Vulnerability Scanning",
            "desc": "Multi-layered security scanning with Bandit, Pip-Audit, and Safety",
            "details": "Detects Python vulnerabilities, insecure code patterns, outdated dependencies with known CVEs."
        },
        {
            "icon": "📦",
            "title": "Dependency Health Checks",
            "desc": "Monitor Python and Node.js package health and identify outdated packages",
            "details": "Tracks dependency versions, detects security vulnerabilities in libraries, suggests updates."
        },
        {
            "icon": "📝",
            "title": "Automated Changelog Generation",
            "desc": "Generate comprehensive CHANGELOG.md from your git commit history",
            "details": "Intelligently categorizes commits, creates version history, documents breaking changes."
        },
        {
            "icon": "📈",
            "title": "Trend Tracking & Analytics",
            "desc": "Track code metrics and repository health over time with historical analysis",
            "details": "Maintains detailed historical data, visualizes trends, identifies patterns in code evolution."
        },
        {
            "icon": "🤖",
            "title": "Smart Self-Healing",
            "desc": "Automatically generates missing configuration files and maintains state",
            "details": "Creates missing files on first run, maintains analysis history, recovers from failures gracefully."
        },
        {
            "icon": "📊",
            "title": "Repository Health Dashboard",
            "desc": "Auto-generates comprehensive health report with metrics and insights",
            "details": "Creates beautiful markdown dashboards, tracks active contributors, shows commit activity."
        }
    ]

    for i in range(0, len(features), 2):
        col1, col2 = st.columns(2)

        with col1:
            f = features[i]
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{f['icon']}</div>
                <div class="feature-title">{f['title']}</div>
                <div class="feature-desc"><strong>{f['desc']}</strong></div>
                <div style="margin-top: 12px; color: #888; font-size: 0.9em; line-height: 1.5;">
                    {f['details']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        if i + 1 < len(features):
            with col2:
                f = features[i + 1]
                st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-icon">{f['icon']}</div>
                    <div class="feature-title">{f['title']}</div>
                    <div class="feature-desc"><strong>{f['desc']}</strong></div>
                    <div style="margin-top: 12px; color: #888; font-size: 0.9em; line-height: 1.5;">
                        {f['details']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("### Advanced Features")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚙️</div>
            <div class="feature-title">Zero Configuration</div>
            <div class="feature-desc">Works out-of-the-box with sensible defaults</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔄</div>
            <div class="feature-title">Daily Automation</div>
            <div class="feature-desc">Runs automatically via GitHub Actions</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Repository Agnostic</div>
            <div class="feature-desc">Works with any Python repository</div>
        </div>
        """, unsafe_allow_html=True)

# ===== HOW IT WORKS PAGE =====
elif page == "🔧 How It Works":
    st.markdown('<div class="main-header">How It Works</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Understanding the 8 Scripts & System Architecture</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    <strong>🎯 Complete Transparency:</strong><br>
    Git-Buddy uses 8 intelligent scripts that work together in a coordinated pipeline. This page explains exactly what each script does and how they interact.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### System Architecture")
    st.markdown("""
    When Git-Buddy runs, it follows this execution flow:

    1. **Gather Raw Data** → Run analysis tools (pylint, flake8, bandit, etc.)
    2. **Aggregate Metrics** → Combine results into health scores
    3. **Collect History** → Store data for trend analysis
    4. **Generate Visualizations** → Create charts from historical data
    5. **Generate Reports** → Create markdown documentation
    6. **Update Repository** → Commit all results to git

    All of this happens **automatically** in GitHub Actions!
    """)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### The 8 Scripts Explained")

    scripts = [
        {
            "num": 1,
            "name": "analyzer.py",
            "lines": 721,
            "icon": "🔍",
            "purpose": "Core Analysis Engine",
            "what": "Orchestrates all analysis tools and combines results",
            "tools": ["pylint", "flake8", "radon", "bandit", "pip-audit", "safety", "pytest-cov"],
            "output": "Comprehensive analysis report (JSON)",
            "details": "This is the main engine. It runs 7 different analysis tools, handles errors gracefully, and produces a master report with all metrics."
        },
        {
            "num": 2,
            "name": "repo_health_metrics.py",
            "lines": 490,
            "icon": "📊",
            "purpose": "Health Score Calculator",
            "what": "Aggregates metrics into repository health scores",
            "tools": ["analysis data"],
            "output": ".github/repo_health_metrics.json (timestamped)",
            "details": "Takes raw metrics and calculates overall health. Stores historical data for trend analysis. Shows quality, coverage, security, and dependency health."
        },
        {
            "num": 3,
            "name": "loc_trend_collector.py",
            "lines": 445,
            "icon": "📈",
            "purpose": "Historical LOC Tracker",
            "what": "Tracks Lines of Code changes over time",
            "tools": ["git", "language detection"],
            "output": ".github/loc_history.json (appends daily)",
            "details": "Counts total lines of code, breakdown by language, and daily changes. Never deletes history—it appends new data each day so you can see growth patterns."
        },
        {
            "num": 4,
            "name": "loc_trend_visualizer.py",
            "lines": 470,
            "icon": "🎨",
            "purpose": "Chart Generator",
            "what": "Creates visual charts from historical data",
            "tools": ["matplotlib", "numpy"],
            "output": "PNG/SVG graphs (.github/loc_trend.png, etc.)",
            "details": "Reads historical data and generates beautiful charts. Shows LOC growth, language distribution, and trend lines with linear regression analysis."
        },
        {
            "num": 5,
            "name": "readme_updater.py",
            "lines": 439,
            "icon": "📄",
            "purpose": "README Autopilot",
            "what": "Automatically updates README.md with latest metrics",
            "tools": ["markdown parsing"],
            "output": "Updated README.md",
            "details": "Inserts badges and metrics into your README using HTML comment markers. Preserves all existing content, only updates specific sections."
        },
        {
            "num": 6,
            "name": "repo_health_dashboard.py",
            "lines": 429,
            "icon": "📋",
            "purpose": "Dashboard Generator",
            "what": "Creates a beautiful health dashboard markdown file",
            "tools": ["metrics aggregation"],
            "output": "HEALTH_DASHBOARD.md",
            "details": "Generates HEALTH_DASHBOARD.md with overall health score, strengths, weaknesses, actionable recommendations, and detailed metrics with context."
        },
        {
            "num": 7,
            "name": "changelog_generator.py",
            "lines": 133,
            "icon": "📝",
            "purpose": "Release Notes Generator",
            "what": "Auto-generates CHANGELOG.md from git history",
            "tools": ["git log parsing"],
            "output": "CHANGELOG.md",
            "details": "Parses commit messages, groups by version/type, creates readable release notes. Automatically detects features, bugs, and breaking changes."
        },
        {
            "num": 8,
            "name": "create_summary.py",
            "lines": 157,
            "icon": "📢",
            "purpose": "GitHub UI Formatter",
            "what": "Creates formatted summary visible in GitHub Actions",
            "tools": ["GitHub Actions API"],
            "output": "GitHub Actions Job Summary",
            "details": "Formats analysis results for display in GitHub UI. Shows key metrics, pass/fail indicators, links to reports. Visible without leaving GitHub!"
        }
    ]

    for script in scripts:
        with st.expander(f"**{script['num']}. {script['icon']} {script['name']}** ({script['lines']} lines) - {script['purpose']}", expanded=False):
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown(f"**What it does:**\n{script['what']}")
                st.markdown(f"**Output:**\n`{script['output']}`")

            with col2:
                st.markdown(f"**Uses tools:**")
                for tool in script['tools']:
                    st.markdown(f"- {tool}")

            st.markdown(f"\n**Details:**\n{script['details']}")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### Data Flow")
    st.markdown("""
    ```
    GitHub Actions Trigger (Daily)
         ↓
    analyzer.py 🔍
    (Run all analysis tools)
         ↓
    ├─→ repo_health_metrics.py 📊 (Aggregate scores)
    ├─→ loc_trend_collector.py 📈 (Collect LOC history)
    ├─→ changelog_generator.py 📝 (Parse git history)
    └─→ loc_trend_visualizer.py 🎨 (Create charts)
         ↓
    ├─→ repo_health_dashboard.py 📋 (Create dashboard)
    ├─→ readme_updater.py 📄 (Update README)
    └─→ create_summary.py 📢 (Format for GitHub UI)
         ↓
    git add . && git commit && git push
         ↓
    Results stored in your repository ✅
    ```
    """)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### What Gets Downloaded")
    st.markdown("""
    When you download the setup package, you get:

    | File | What it does |
    |------|-------------|
    | **daily-analysis.yml** | GitHub Actions workflow that triggers everything |
    | **requirements.txt** | Python packages needed (pylint, flake8, bandit, etc.) |
    | **.env.example** | Configuration template (optional) |
    | **setup.sh** | Bash script for manual setup |
    | **setup.py** | Python script for auto-setup |

    The **8 scripts above are already in this repository** - the workflow file downloads and runs them!

    > 💡 The key insight: You only need to set up the **workflow file and requirements** in your repository. The 8 scripts are pulled from GitHub when the workflow runs.
    """)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### Key Principles")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Automation**
        - No manual steps required
        - Runs daily automatically
        - Zero human intervention

        **Transparency**
        - Every script is open source
        - Clear logging of what's happening
        - Human-readable reports
        """)

    with col2:
        st.markdown("""
        **Privacy**
        - Everything runs in GitHub Actions
        - No external APIs or services
        - Results stored in your repository

        **Simplicity**
        - No configuration required
        - Sensible defaults for all settings
        - Works with any Python project
        """)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### Next Steps")
    st.info("👉 Ready to set up Git-Buddy? Go to **Quick Setup** tab and download the configuration package!")

# ===== QUICK SETUP PAGE =====
elif page == "🚀 Quick Setup":
    st.markdown('<div class="main-header">Quick Setup</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Get Git-Buddy running in 5 minutes</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="success-box">
    <strong>✅ Download all files and extract to your repository.</strong> Git-Buddy is fully self-contained
    and works with any Python project!
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("### Understanding the 8 Scripts")

    st.warning("""
    **Common Question:** "I see 8 scripts mentioned, but the download only has 5 files. How do I get all 8 scripts?"

    **Answer:** The 8 scripts are already in the Git-Buddy repository. Here's how it works:

    1. **You download 5 setup files** (workflow, requirements, config, setup scripts)
    2. **The workflow file** (`.github/workflows/daily-analysis.yml`) is your configuration
    3. **When GitHub Actions runs**, it downloads the 8 scripts from this repository automatically
    4. **All 8 scripts run together** to analyze your repository

    **The 5 files you download:**
    - 📋 `.env.example` - Configuration template
    - 🔄 `daily-analysis.yml` - Triggers the 8 scripts daily
    - 📦 `requirements.txt` - Dependencies for the 8 scripts
    - 🚀 `SETUP.sh` - Bash auto-setup helper
    - 🐍 `setup.py` - Python auto-setup helper

    **The 8 scripts that run automatically:**
    - 🔍 `analyzer.py` - Main analysis engine
    - 📊 `repo_health_metrics.py` - Health scoring
    - 📈 `loc_trend_collector.py` - Historical tracking
    - 🎨 `loc_trend_visualizer.py` - Chart generation
    - 📄 `readme_updater.py` - README updates
    - 📋 `repo_health_dashboard.py` - Dashboard generation
    - 📝 `changelog_generator.py` - Release notes
    - 📢 `create_summary.py` - GitHub UI formatting

    Want to understand each script in detail? Check the **"🔧 How It Works"** tab!
    """)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("### 3 Easy Steps")

    st.markdown('<span class="step-badge">Step 1</span>', unsafe_allow_html=True)
    st.write("**Download** - Click the button below to get all setup files")

    st.markdown('<span class="step-badge">Step 2</span>', unsafe_allow_html=True)
    st.write("**Extract** - Unzip the files into your repository root")

    st.markdown('<span class="step-badge">Step 3</span>', unsafe_allow_html=True)
    st.write("**Commit** - Push the files and enable GitHub Actions")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Create downloadable files
    env_example = """# Git-Buddy Configuration File
# Copy this to your repository root as `.env.example`

# Analyzer Settings
ENABLE_CODE_QUALITY=true
ENABLE_SECURITY_SCAN=true
ENABLE_COMPLEXITY_ANALYSIS=true

# Report Settings
ENABLE_CHANGELOG=true
ENABLE_HEALTH_DASHBOARD=true
ENABLE_LOC_TREND=true

# Thresholds (optional)
MIN_CODE_QUALITY_SCORE=6.0
MAX_COMPLEXITY=15
"""

    github_workflow = """name: Git-Buddy - Repository Analysis

on:
  schedule:
    - cron: '0 2 * * *'
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  analyze:
    runs-on: ubuntu-latest
    name: Repository Health Check

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Repository Analysis
        env:
          ENABLE_CODE_QUALITY: true
          ENABLE_SECURITY_SCAN: true
          ENABLE_COMPLEXITY_ANALYSIS: true
          ENABLE_CHANGELOG: true
          ENABLE_HEALTH_DASHBOARD: true
          ENABLE_LOC_TREND: true
        run: |
          python .github/scripts/analyzer.py
          python .github/scripts/changelog_generator.py
          python .github/scripts/repo_health_metrics.py
          python .github/scripts/repo_health_dashboard.py
          python .github/scripts/loc_trend_collector.py
          python .github/scripts/loc_trend_visualizer.py
          python .github/scripts/readme_updater.py

      - name: Create Job Summary
        if: always()
        run: python .github/scripts/create_summary.py

      - name: Commit Analysis Results
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git diff --quiet && git diff --staged --quiet || git commit -m "Update repository analysis"
          git push
"""

    requirements_txt = """# Git-Buddy Repository Analysis Tool

# Web UI & Dashboards
streamlit>=1.28.0

# Code Quality Analysis
pylint>=2.17.0
flake8>=6.0.0
radon>=6.0.0

# Testing & Coverage
pytest>=7.4.0
pytest-cov>=4.1.0

# Security Scanning
bandit>=1.7.5
pip-audit>=2.6.0
safety>=2.3.5

# Visualization & Data
matplotlib>=3.8.0
numpy>=1.24.0

# JSON & Data Processing
requests>=2.31.0
"""

    setup_instructions = """#!/bin/bash
# Git-Buddy Setup Script
# This script sets up Git-Buddy in your repository

echo "Setting up Git-Buddy..."

# Create directories
mkdir -p .github/scripts
mkdir -p .github/workflows

# Copy workflow file
cp daily-analysis.yml .github/workflows/

# Copy requirements
cp requirements.txt .

# Copy configuration
cp .env.example .

echo "Git-Buddy setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your preferences (optional)"
echo "2. Commit and push all files to your repository"
echo "3. Go to Settings > Actions > General and enable 'Allow all actions'"
echo "4. Go to Actions tab and run the workflow manually"
echo ""
echo "That's it! Git-Buddy will now analyze your repository daily at 2 AM UTC."
"""

    setup_install_py = """#!/usr/bin/env python3
# Git-Buddy Auto-Install Script
# Run this to automatically set up Git-Buddy

import os
import shutil
from pathlib import Path

def setup_git_buddy():
    '''Setup Git-Buddy in the current repository'''

    print("Setting up Git-Buddy...")

    # Create directories
    os.makedirs('.github/scripts', exist_ok=True)
    os.makedirs('.github/workflows', exist_ok=True)

    print("✓ Created .github directories")

    # The files should be in place
    if Path('daily-analysis.yml').exists():
        shutil.copy('daily-analysis.yml', '.github/workflows/')
        print("✓ Copied workflow file")

    if Path('requirements.txt').exists():
        print("✓ requirements.txt is ready")

    if Path('.env.example').exists():
        print("✓ .env.example is ready")

    print("")
    print("Git-Buddy setup complete!")
    print("")
    print("Next steps:")
    print("1. Commit all files: git add . && git commit -m 'Add Git-Buddy'")
    print("2. Push to repository: git push")
    print("3. Go to Settings > Actions > General and enable workflows")
    print("4. Go to Actions tab and trigger the workflow manually")
    print("")
    print("Done! Git-Buddy will analyze your repository daily at 2 AM UTC.")

if __name__ == '__main__':
    setup_git_buddy()
"""

    # Create a zip file with all necessary files
    def create_download_package():
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr('.env.example', env_example)
            zip_file.writestr('daily-analysis.yml', github_workflow)
            zip_file.writestr('requirements.txt', requirements_txt)
            zip_file.writestr('SETUP.sh', setup_instructions)
            zip_file.writestr('setup.py', setup_install_py)

        zip_buffer.seek(0)
        return zip_buffer.getvalue()

    st.markdown("### Download Setup Package")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.download_button(
            label="📦 Download Git-Buddy Setup Package",
            data=create_download_package(),
            file_name="git-buddy-setup.zip",
            mime="application/zip",
            use_container_width=True
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("### What's Included")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📋</div>
            <div class="feature-title">.env.example</div>
            <div class="feature-desc">Configuration template with all available options</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚙️</div>
            <div class="feature-title">requirements.txt</div>
            <div class="feature-desc">All Python dependencies pinned to stable versions</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔄</div>
            <div class="feature-title">daily-analysis.yml</div>
            <div class="feature-desc">GitHub Actions workflow configured for daily runs</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <div class="feature-title">Setup Scripts</div>
            <div class="feature-desc">Auto-install scripts for bash and Python</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("### Quick Reference")

    st.markdown("""
    <div class="code-block">
    # After extracting the ZIP file:

    git add .
    git commit -m "Add Git-Buddy repository analysis"
    git push

    # Then enable workflows in GitHub:
    # Settings → Actions → General → Allow all actions
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="success-box">
    <strong>✅ Done!</strong> Your repository is now monitored. Git-Buddy runs daily at 2 AM UTC and
    generates comprehensive analysis reports automatically.
    </div>
    """, unsafe_allow_html=True)


# ===== FAQ PAGE =====
elif page == "❓ FAQ":
    st.markdown('<div class="main-header">Common Questions</div>', unsafe_allow_html=True)

    faqs = [
        {
            "q": "Can I use this with my existing repository?",
            "a": "Yes! Git-Buddy works seamlessly with any GitHub repository. Just download the files, extract them to your repo root, and enable the workflow. It's designed not to interfere with existing CI/CD pipelines or workflows."
        },
        {
            "q": "Is it really zero-code setup?",
            "a": "Absolutely! Download files, extract them to your repo, and enable the GitHub Actions workflow. No code editing, no configuration, no API keys needed. It works perfectly out of the box with sensible defaults."
        },
        {
            "q": "How often does analysis run?",
            "a": "By default, Git-Buddy runs daily at 2 AM UTC. You can customize the schedule by editing the cron expression in `.github/workflows/daily-analysis.yml`. You can also trigger manual runs anytime from the GitHub Actions tab."
        },
        {
            "q": "Works with private repositories?",
            "a": "Absolutely! All analysis happens securely within your GitHub Actions environment. Your code never leaves your repository—all data stays private and under your control."
        },
        {
            "q": "Can I customize what gets analyzed?",
            "a": "Yes! Copy `.env.example` to `.env` and adjust settings. You can enable/disable specific analyses (code quality, security, complexity), set thresholds, and exclude directories."
        },
        {
            "q": "Do I need API keys or external services?",
            "a": "No! Git-Buddy is completely self-contained. All analysis tools run locally in GitHub Actions. We don't use external APIs, cloud services, or require any authentication tokens."
        },
        {
            "q": "Can I disable specific analyses?",
            "a": "Yes! Each analysis component can be independently controlled via environment variables in `.env`. Turn off what you don't need—Git-Buddy only runs what you enable."
        },
        {
            "q": "Where are analysis results stored?",
            "a": "All results are automatically committed back to your repository as markdown files and JSON data. No external storage needed—everything stays in your Git history and repository."
        },
        {
            "q": "How do I see the analysis results?",
            "a": "Results are committed to your repository in multiple formats: HEALTH_DASHBOARD.md (human-readable), analysis_results.json (raw data), CHANGELOG.md (git history), and metrics tracked in .github/."
        },
        {
            "q": "What Python versions are supported?",
            "a": "Git-Buddy is tested with Python 3.11+. The workflow uses Python 3.11 by default, but you can modify the workflow file to use different versions if needed."
        },
    ]

    for faq in faqs:
        with st.expander(f"**{faq['q']}**"):
            st.write(faq['a'])

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    <strong>Still have questions?</strong> Check the GitHub repository or open an issue!
    </div>
    """, unsafe_allow_html=True)

# ===== DOCS PAGE =====
elif page == "📖 Docs":
    st.markdown('<div class="main-header">Documentation</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    Complete guides and documentation for Git-Buddy deployment and usage.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Getting Started")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Quick Start</div>
            <div class="feature-desc">Get running in 5 minutes</div>
            <div style="margin-top: 12px;">
                1. Download the ZIP<br>
                2. Extract to repo<br>
                3. Commit and push<br>
                4. Enable workflows
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🐳</div>
            <div class="feature-title">Docker Setup</div>
            <div class="feature-desc">Run in containerized environment</div>
            <div style="margin-top: 12px;">
                Perfect for isolated testing and CI/CD integration with Docker containers.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚙️</div>
            <div class="feature-title">Configuration Guide</div>
            <div class="feature-desc">Customize analysis parameters</div>
            <div style="margin-top: 12px;">
                Learn how to configure thresholds, enable/disable analyses, and customize the workflow schedule.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔧</div>
            <div class="feature-title">Advanced Features</div>
            <div class="feature-desc">Explore powerful capabilities</div>
            <div style="margin-top: 12px;">
                Learn about trend tracking, historical analysis, self-healing capabilities, and custom reporting.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("### Core Analysis Tools")

    tools = [
        ("Code Quality", "Radon + Pylint", "Analyzes complexity, maintainability, and code patterns"),
        ("Testing", "Pytest + Coverage", "Measures test coverage and identifies untested code"),
        ("Security", "Bandit + Safety + Pip-Audit", "Detects vulnerabilities and security risks"),
        ("Changelog", "Git History", "Auto-generates changelog from commits"),
        ("Trends", "Historical Data", "Tracks metrics over time with analytics"),
        ("Health", "Multi-Factor", "Comprehensive repository health dashboard"),
    ]

    for tool, tech, desc in tools:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-title">{tool}</div>
            <div style="color: #e74c3c; font-weight: 600; margin-bottom: 8px;">{tech}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("### Resources")

    st.markdown("""
    - 📄 [View Full README](https://github.com/iampreetdave-max/Git-Helper)
    - 🐛 [Report Issues](https://github.com/iampreetdave-max/Git-Helper/issues)
    - ⭐ [Star on GitHub](https://github.com/iampreetdave-max/Git-Helper)
    """)

# Footer with credits
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <strong>🤖 Git-Buddy</strong> — Enterprise-grade repository analysis, zero configuration<br><br>
    <strong>Built for developers by developers</strong><br>
    Innovated by <a href="https://github.com/iampreetdave-max">Preet Dave</a> | Powered by Claude AI<br><br>
    <strong>Connect:</strong><br>
    <a href="https://github.com/iampreetdave-max/Git-Helper">⭐ Star on GitHub</a> •
    <a href="https://github.com/iampreetdave-max/Git-Helper/issues">Report Issues</a> •
    <a href="https://github.com/iampreetdave-max/Git-Helper/discussions">Discussions</a><br><br>
    <small>Git-Buddy is open source and free for all. Made for the community, by the community.</small>
</div>
""", unsafe_allow_html=True)
