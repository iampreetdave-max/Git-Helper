import streamlit as st
import io
import json
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Git-Helper Setup Wizard",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
        .main-header {
            font-size: 3em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
        }
        .feature-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .step-badge {
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("📚 Navigation")
    page = st.radio("Select a page:",
                    ["🏠 Home", "🚀 Quick Setup", "📖 How It Works", "❓ FAQ", "⚙️ Advanced"])

    st.divider()
    st.info("💡 **Tip:** Start with 'Quick Setup' for automatic installation!")

# ===== HOME PAGE =====
if page == "🏠 Home":
    st.markdown('<div class="main-header">🔧 Git-Helper</div>', unsafe_allow_html=True)
    st.markdown("## Automated Repository Health Monitoring for Everyone")

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("""
        ### What is Git-Helper?

        Git-Helper is an **intelligent GitHub Actions automation** that monitors your repository's health,
        analyzes code quality, detects security issues, and tracks progress over time—all **without any coding required**!

        Perfect for:
        - 👨‍💻 Beginner developers who want code insights
        - 🏢 Teams tracking repository health
        - 🔒 Projects requiring security analysis
        - 📊 Organizations monitoring code quality trends

        **Just add the files to your repo, and Git-Helper handles the rest!**
        """)

    with col2:
        st.image("https://via.placeholder.com/300x200?text=Git+Helper+Dashboard",
                caption="Auto-generated Health Dashboard")

    st.divider()

    # Key Features
    st.markdown("### ✨ Key Features")

    cols = st.columns(3)

    features = [
        ("📊 Code Quality Analysis",
         "Detects complexity, style issues, and potential bugs using industry-standard tools"),
        ("🔐 Security Scanning",
         "Identifies vulnerabilities, unsafe dependencies, and security risks"),
        ("📈 Trend Tracking",
         "Monitors lines of code, complexity trends, and historical metrics")
    ]

    for i, (title, desc) in enumerate(features):
        with cols[i]:
            st.markdown(f'<div class="feature-card"><b>{title}</b><br>{desc}</div>',
                       unsafe_allow_html=True)

    cols2 = st.columns(3)

    features2 = [
        ("📋 Auto Changelog",
         "Generates detailed changelogs from git history automatically"),
        ("🎯 Health Dashboard",
         "Beautiful markdown dashboard with all metrics in one place"),
        ("⚡ Zero Configuration",
         "Works out of the box—just copy files and enable the workflow")
    ]

    for i, (title, desc) in enumerate(features2):
        with cols2[i]:
            st.markdown(f'<div class="feature-card"><b>{title}</b><br>{desc}</div>',
                       unsafe_allow_html=True)

    st.divider()

    # Call to action
    st.markdown("### 🚀 Ready to Get Started?")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("⚡ Go to Quick Setup →", key="home_setup", use_container_width=True):
            st.switch_page("pages/Quick Setup.py")

# ===== QUICK SETUP PAGE =====
elif page == "🚀 Quick Setup":
    st.title("⚡ Quick Setup Wizard")
    st.markdown("Get Git-Helper running in **3 steps**—no coding required!")

    st.divider()

    # Step 1
    st.markdown(f'<span class="step-badge">STEP 1</span> Download Configuration Files',
               unsafe_allow_html=True)
    st.markdown("""
    Click the button below to download the required files. These files will be added to your repository.
    """)

    col1, col2 = st.columns(2)

    # Create downloadable files
    env_example = """# Git-Helper Configuration File
# Copy this to your repository root as `.env` or add to your GitHub Secrets

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

    github_workflow = """name: 📊 Daily Repository Analysis

on:
  schedule:
    # Runs at 2 AM UTC daily
    - cron: '0 2 * * *'
  workflow_dispatch:
    # Allow manual trigger from GitHub Actions tab

permissions:
  contents: write
  pull-requests: write

jobs:
  analyze:
    runs-on: ubuntu-latest
    name: Repository Health Check

    steps:
      - name: 📥 Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: 🐍 Setup Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: 📦 Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: 🔍 Run Repository Analysis
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

      - name: 📝 Create Job Summary
        if: always()
        run: python .github/scripts/create_summary.py

      - name: 📤 Commit Analysis Results
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git diff --quiet && git diff --staged --quiet || git commit -m "📊 Update repository analysis results"
          git push
"""

    with col1:
        st.download_button(
            label="📥 Download .env File",
            data=env_example,
            file_name=".env.example",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        st.download_button(
            label="📥 Download GitHub Workflow",
            data=github_workflow,
            file_name="daily-analysis.yml",
            mime="text/plain",
            use_container_width=True
        )

    st.info("""
    **Where to put these files:**
    - `.env.example` → Your repo root (rename to `.env` or add to GitHub Secrets)
    - `daily-analysis.yml` → `.github/workflows/daily-analysis.yml`
    """)

    st.divider()

    # Step 2
    st.markdown(f'<span class="step-badge">STEP 2</span> Copy Analysis Scripts',
               unsafe_allow_html=True)
    st.markdown("""
    Clone or download the analysis scripts from our GitHub repository and add them to your `.github/scripts/` directory.

    **Or use git to copy them:**
    ```bash
    # Clone the Git-Helper repo
    git clone https://github.com/iampreetdave-max/Git-Helper.git temp-git-helper

    # Copy scripts to your repo
    cp -r temp-git-helper/.github/scripts .github/
    cp temp-git-helper/requirements.txt .

    # Cleanup
    rm -rf temp-git-helper
    ```
    """)

    st.divider()

    # Step 3
    st.markdown(f'<span class="step-badge">STEP 3</span> Enable & Run',
               unsafe_allow_html=True)
    st.markdown("""
    1. **Commit and push** the files to your repository
    2. **Navigate** to `Settings → Actions → General` in your repo
    3. **Enable** `Allow all actions and reusable workflows`
    4. **Go to** the `Actions` tab and manually trigger the workflow
    5. **Watch** as Git-Helper analyzes your repository!

    **That's it!** 🎉 The workflow will now run daily at 2 AM UTC.
    """)

    st.success("✅ Your repository will now automatically receive health insights!")

# ===== HOW IT WORKS PAGE =====
elif page == "📖 How It Works":
    st.title("📖 How Git-Helper Works")

    st.markdown("""
    ### The Big Picture

    Git-Helper is an **automated pipeline** that runs in GitHub Actions. Here's what happens:
    """)

    st.image("https://via.placeholder.com/800x400?text=Git+Helper+Pipeline",
            caption="Git-Helper Analysis Pipeline")

    st.divider()

    st.markdown("### 🔄 The Analysis Pipeline")

    col1, col2 = st.columns([1, 2])

    with col1:
        steps = [
            ("1️⃣", "Checkout", "Git pulls latest code"),
            ("2️⃣", "Analyze", "Checks quality, security"),
            ("3️⃣", "Calculate", "Computes health metrics"),
            ("4️⃣", "Generate", "Creates dashboards"),
            ("5️⃣", "Commit", "Pushes results to repo"),
        ]

        for emoji, title, desc in steps:
            st.markdown(f"**{emoji} {title}**: {desc}")

    with col2:
        st.markdown("""
        ### What Gets Analyzed?

        **Code Quality:**
        - Code complexity (Cyclomatic)
        - Style violations (PEP 8)
        - Potential bugs
        - Documentation coverage

        **Security:**
        - Vulnerable dependencies
        - Unsafe code patterns
        - Security vulnerabilities

        **Trends:**
        - Lines of code growth
        - Complexity trends
        - Historical metrics
        """)

    st.divider()

    st.markdown("### 📁 Generated Files")

    files_generated = {
        "analysis_results.json": "Detailed analysis data in JSON format",
        "HEALTH_DASHBOARD.md": "Visual dashboard with all metrics",
        "CHANGELOG.md": "Auto-generated changelog from git history",
        "LOC_TREND.png": "Graph showing lines of code trends",
        "README.md": "Updated with analysis badge and summary"
    }

    for filename, description in files_generated.items():
        st.markdown(f"- **{filename}**: {description}")

# ===== FAQ PAGE =====
elif page == "❓ FAQ":
    st.title("❓ Frequently Asked Questions")

    faqs = [
        ("Can I use this with my existing repository?",
         """Yes! Git-Helper works with any GitHub repository. Just add the files and enable the workflow.
         It won't interfere with existing CI/CD pipelines."""),

        ("Is it really no-code?",
         """Absolutely! Just download files, copy them to your repo, and enable the GitHub Actions workflow.
         No coding or configuration required. It works out of the box!"""),

        ("How often does it run?",
         """By default, Git-Helper runs daily at 2 AM UTC. You can also trigger it manually anytime from
         the GitHub Actions tab in your repository settings."""),

        ("Will it work with private repositories?",
         """Yes, it works perfectly with private repos! The analysis happens in your GitHub Actions,
         so all data stays within your organization."""),

        ("Can I customize the analysis?",
         """Yes! Use environment variables in your `.env` file to enable/disable specific analyses
         and set custom thresholds for code quality and complexity."""),

        ("What if my repository is very large?",
         """Git-Helper is optimized for large repositories. However, initial analysis might take a few minutes.
         Subsequent runs will be much faster due to incremental analysis."""),

        ("Can I disable certain analyses?",
         """Yes! Edit the `.env` file and set `ENABLE_CODE_QUALITY=false` (or other analyses) to skip them."""),

        ("Where are the results stored?",
         """All results are committed back to your repository as files (HEALTH_DASHBOARD.md, analysis_results.json, etc.).
         No external storage is used—everything stays in your repo!"""),
    ]

    for question, answer in faqs:
        with st.expander(f"❓ {question}"):
            st.markdown(answer)

# ===== ADVANCED PAGE =====
elif page == "⚙️ Advanced":
    st.title("⚙️ Advanced Configuration")

    st.markdown("### 🎛️ Environment Variables")

    config_table = """
    | Variable | Default | Description |
    |----------|---------|-------------|
    | `ENABLE_CODE_QUALITY` | `true` | Run code quality analysis |
    | `ENABLE_SECURITY_SCAN` | `true` | Run security vulnerability scan |
    | `ENABLE_COMPLEXITY_ANALYSIS` | `true` | Analyze code complexity |
    | `ENABLE_CHANGELOG` | `true` | Generate changelog |
    | `ENABLE_HEALTH_DASHBOARD` | `true` | Create health dashboard |
    | `ENABLE_LOC_TREND` | `true` | Track lines of code trends |
    | `MIN_CODE_QUALITY_SCORE` | `6.0` | Minimum quality score threshold |
    | `MAX_COMPLEXITY` | `15` | Maximum cyclomatic complexity |
    """

    st.markdown(config_table)

    st.divider()

    st.markdown("### 📝 Custom Configuration Example")

    custom_config = """# Disable security scan but keep everything else
ENABLE_CODE_QUALITY=true
ENABLE_SECURITY_SCAN=false
ENABLE_COMPLEXITY_ANALYSIS=true
ENABLE_CHANGELOG=true
ENABLE_HEALTH_DASHBOARD=true
ENABLE_LOC_TREND=true
MIN_CODE_QUALITY_SCORE=7.5
MAX_COMPLEXITY=10
"""

    st.code(custom_config, language="bash")

    st.divider()

    st.markdown("### 🔗 Integration with GitHub Secrets")

    st.info("""
    **Option 1: Use .env file (Recommended for simplicity)**
    - Add `.env` file to your repo
    - Git-Helper reads configuration automatically

    **Option 2: Use GitHub Secrets (Recommended for security)**
    - Go to `Settings → Secrets and variables → Actions`
    - Add each variable as a secret
    - The workflow automatically uses these values
    """)

st.divider()
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <small>
    🔧 Git-Helper | Made for developers, by developers<br>
    <a href="https://github.com/iampreetdave-max/Git-Helper">GitHub Repository</a> •
    <a href="https://github.com/iampreetdave-max/Git-Helper/issues">Report Issues</a>
    </small>
</div>
""", unsafe_allow_html=True)
