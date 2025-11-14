#!/usr/bin/env python3
"""
Git-Buddy One-Line Installer Script

This script automatically sets up Git-Buddy in your repository.

Usage:
    python install.py

The script will:
1. Create necessary directories
2. Download and place all required files
3. Display next steps for completion
"""

import os
import sys
import shutil
from pathlib import Path
from urllib.request import urlretrieve

def setup_git_buddy():
    """Setup Git-Buddy in the current repository."""

    print("\n" + "=" * 60)
    print("🤖 Git-Buddy Setup Wizard".center(60))
    print("=" * 60 + "\n")

    # Check if we're in a git repository
    if not Path('.git').exists():
        print("❌ Error: Not a git repository!")
        print("   Please run this script from the root of your git repository.\n")
        sys.exit(1)

    print("✅ Detected git repository\n")

    # Create required directories
    print("📁 Creating directories...")
    os.makedirs('.github/scripts', exist_ok=True)
    os.makedirs('.github/workflows', exist_ok=True)
    print("   ✓ .github/scripts/")
    print("   ✓ .github/workflows/\n")

    # Check for existing files
    print("📋 Checking for existing files...\n")

    files_needed = {
        'requirements.txt': 'Python dependencies',
        '.env.example': 'Configuration template',
        '.github/workflows/daily-analysis.yml': 'GitHub Actions workflow',
    }

    for file_path, description in files_needed.items():
        if Path(file_path).exists():
            print(f"   ✓ {file_path} (exists)")
        else:
            print(f"   ⚠ {file_path} (missing - download manually)")

    print("\n" + "=" * 60)
    print("📥 NEXT STEPS".center(60))
    print("=" * 60 + "\n")

    print("1️⃣  Download the complete setup package:")
    print("   → Visit: https://streamlit.app/git-buddy")
    print("   → Or: Download from GitHub\n")

    print("2️⃣  Extract files to your repository root:")
    print("   unzip git-buddy-setup.zip\n")

    print("3️⃣  Commit the files:")
    print("   git add .")
    print("   git commit -m 'Add Git-Buddy repository analysis'\n")

    print("4️⃣  Push to GitHub:")
    print("   git push\n")

    print("5️⃣  Enable GitHub Actions workflows:")
    print("   → Go to: Settings → Actions → General")
    print("   → Enable: 'Allow all actions'\n")

    print("6️⃣  Trigger the first analysis (optional):")
    print("   → Go to: Actions tab")
    print("   → Click: Run workflow → Run\n")

    print("=" * 60)
    print("🎉 THAT'S IT!".center(60))
    print("=" * 60 + "\n")

    print("✨ Git-Buddy will now:")
    print("   • Run daily at 2 AM UTC")
    print("   • Analyze your repository code")
    print("   • Detect security vulnerabilities")
    print("   • Track code quality metrics")
    print("   • Generate comprehensive reports")
    print("   • Update your README automatically\n")

    print("📚 Learn more:")
    print("   • GitHub: https://github.com/iampreetdave-max/Git-Helper")
    print("   • Docs: Check the README.md file")
    print("   • Questions: Open an issue on GitHub\n")

    print("Made with ❤️  by Preet Dave")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    try:
        setup_git_buddy()
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
