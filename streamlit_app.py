import streamlit as st
import io
import json
import zipfile
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Git-Buddy Setup Wizard",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Monochrome styling
st.markdown("""
    <style>
        .main-header {
            font-size: 3em;
            font-weight: bold;
            color: #000000;
            margin-bottom: 20px;
        }
        .feature-card {
            background: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 4px solid #000000;
        }
        .step-badge {
            background: #333333;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            margin: 10px 0;
        }
        .footer {
            text-align: center;
            color: #666666;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #cccccc;
            font-size: 0.85em;
        }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("Git-Buddy")
    page = st.radio("Select a page:",
                    ["🏠 Home", "🚀 Quick Setup", "❓ FAQ"])

    st.divider()
    st.info("💡 **Tip:** Click 'Quick Setup' to download all files needed!")

# ===== HOME PAGE =====
if page == "🏠 Home":
    st.markdown('<div class="main-header">Git-Buddy</div>', unsafe_allow_html=True)
    st.markdown("### Automated Repository Health Monitoring for Everyone")

    st.markdown("""
    **Git-Buddy** is an intelligent GitHub Actions automation that monitors your repository's health,
    analyzes code quality, detects security issues, and tracks progress over time—all **without any coding required**!

    Perfect for:
    - 👨‍💻 Beginner developers who want code insights
    - 🏢 Teams tracking repository health
    - 🔒 Projects requiring security analysis
    - 📊 Organizations monitoring code quality trends

    **Just download the files, paste them in your repo, and everything works automatically!**
    """)

    st.divider()

    # Key Features
    st.markdown("### Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **📊 Code Quality Analysis**

        Detects complexity, style issues, and potential bugs

        **🔐 Security Scanning**

        Identifies vulnerabilities and security risks
        """)

    with col2:
        st.markdown("""
        **📈 Trend Tracking**

        Monitors metrics over time

        **📋 Auto Changelog**

        Generates changelogs from git history
        """)

    st.divider()

    # Call to action
    st.markdown("### Get Started")
    if st.button("📥 Download Setup Files", use_container_width=True, key="home_setup"):
        st.switch_page("streamlit_app.py")

# ===== QUICK SETUP PAGE =====
elif page == "🚀 Quick Setup":
    st.title("Quick Setup")
    st.markdown("Download all required files and get started in minutes—no coding required!")

    st.divider()

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

    st.markdown("### Download All Files")
    st.markdown("""
    Click the button below to download all 5 required files:
    1. `.env.example` - Configuration file
    2. `daily-analysis.yml` - GitHub workflow
    3. `requirements.txt` - Python dependencies
    4. `SETUP.sh` - Bash setup script
    5. `setup.py` - Python setup script
    """)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.download_button(
            label="📥 Download All Files (ZIP)",
            data=create_download_package(),
            file_name="git-buddy-setup.zip",
            mime="application/zip",
            use_container_width=True
        )

    st.divider()

    st.markdown("### Installation Steps")
    st.markdown("""
    1. **Download** the ZIP file using the button above
    2. **Extract** the files to your repository root
    3. **Commit** the files: `git add . && git commit -m "Add Git-Buddy"`
    4. **Push** to your repository: `git push`
    5. **Enable** workflows: Go to Settings → Actions → General
    6. **Run** the workflow: Go to Actions tab and trigger manually

    **That's it!** 🎉 Git-Buddy will now analyze your repository daily at 2 AM UTC.
    """)

    st.success("✅ Everything is ready. Download the files and follow the steps above.")


# ===== FAQ PAGE =====
elif page == "❓ FAQ":
    st.title("Frequently Asked Questions")

    faqs = [
        ("Can I use this with my existing repository?",
         """Yes! Git-Buddy works with any GitHub repository. Just add the files and enable the workflow.
         It won't interfere with existing CI/CD pipelines."""),

        ("Is it really no-code?",
         """Absolutely! Just download files, extract them to your repo, and enable the GitHub Actions workflow.
         No coding or configuration required. It works out of the box!"""),

        ("How often does it run?",
         """By default, Git-Buddy runs daily at 2 AM UTC. You can also trigger it manually anytime from
         the GitHub Actions tab in your repository."""),

        ("Will it work with private repositories?",
         """Yes, it works perfectly with private repos! The analysis happens in your GitHub Actions,
         so all data stays within your organization."""),

        ("Can I customize the analysis?",
         """Yes! Edit the `.env.example` file and set flags to enable/disable specific analyses
         and set custom thresholds for code quality and complexity."""),

        ("Does Git-Buddy need special API keys?",
         """No! Git-Buddy works without any API keys or external dependencies. All analysis is done
         locally in your GitHub Actions. It's completely self-contained."""),

        ("Can I disable certain analyses?",
         """Yes! Edit the `.env` file and set `ENABLE_CODE_QUALITY=false` (or other analyses) to skip them."""),

        ("Where are the results stored?",
         """All results are committed back to your repository as files (HEALTH_DASHBOARD.md, analysis_results.json, etc.).
         No external storage is used—everything stays in your repo!"""),
    ]

    for question, answer in faqs:
        with st.expander(question):
            st.markdown(answer)

# Footer with credits
st.divider()
st.markdown("""
<div class="footer">
    <strong>Git-Buddy</strong> - Automated Repository Analysis<br>
    <small>
    Innovated by <strong>Preet</strong> | Powered by Claude and Git-Bot<br>
    <a href="https://github.com/iampreetdave-max/Git-Buddy">GitHub Repository</a>
    </small>
</div>
""", unsafe_allow_html=True)
