#!/usr/bin/env python3
"""
Modular Lines of Code (LOC) Trend Collector

Collects historical LOC data including:
- Daily LOC changes
- Added/deleted code
- Language breakdown over time
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict


class LOCTrendCollector:
    """Collects and tracks lines of code trends over time."""

    def __init__(self, repo_path: str = ".", history_file: str = ".github/loc_history.json"):
        """
        Initialize LOC trend collector.

        Args:
            repo_path: Path to repository root
            history_file: Path to history JSON file
        """
        self.repo_path = Path(repo_path).resolve()
        self.history_file = Path(history_file)
        self.history: List[Dict[str, Any]] = []

    def load_history(self) -> None:
        """Load existing history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file) as f:
                    self.history = json.load(f)
                print(f"✅ Loaded {len(self.history)} historical records")
            except Exception as e:
                print(f"⚠️  Could not load history: {e}")
                self.history = []
        else:
            print("📝 Creating new history file")
            self.history = []

    def save_history(self) -> None:
        """Save history to file."""
        try:
            # Create directory if it doesn't exist
            self.history_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
            print(f"✅ Saved history to {self.history_file}")
        except Exception as e:
            print(f"❌ Failed to save history: {e}")
            sys.exit(1)

    def collect_current_snapshot(self) -> Dict[str, Any]:
        """
        Collect current LOC snapshot.

        Returns:
            Snapshot data dictionary
        """
        print("📊 Collecting current LOC snapshot...")

        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_lines": 0,
            "code_lines": 0,
            "comment_lines": 0,
            "blank_lines": 0,
            "languages": {},
            "file_count": 0,
        }

        # Try using cloc if available
        if self._command_exists("cloc"):
            snapshot = self._collect_with_cloc()
        else:
            # Fallback to manual counting
            snapshot = self._collect_manual()

        return snapshot

    def _collect_with_cloc(self) -> Dict[str, Any]:
        """Collect LOC data using cloc tool."""
        print("  ➤ Using cloc for accurate counting...")

        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_lines": 0,
            "code_lines": 0,
            "comment_lines": 0,
            "blank_lines": 0,
            "languages": {},
            "file_count": 0,
        }

        try:
            # Run cloc with JSON output
            result = subprocess.run(
                ["cloc", ".", "--json", "--quiet"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)

                # Get summary (excluding 'header' and 'SUM' keys)
                if "SUM" in data:
                    summary = data["SUM"]
                    snapshot["file_count"] = summary.get("nFiles", 0)
                    snapshot["blank_lines"] = summary.get("blank", 0)
                    snapshot["comment_lines"] = summary.get("comment", 0)
                    snapshot["code_lines"] = summary.get("code", 0)
                    snapshot["total_lines"] = (
                        snapshot["blank_lines"] +
                        snapshot["comment_lines"] +
                        snapshot["code_lines"]
                    )

                # Get per-language breakdown
                for lang, lang_data in data.items():
                    if lang not in ["header", "SUM"] and isinstance(lang_data, dict):
                        snapshot["languages"][lang] = {
                            "files": lang_data.get("nFiles", 0),
                            "blank": lang_data.get("blank", 0),
                            "comment": lang_data.get("comment", 0),
                            "code": lang_data.get("code", 0),
                        }

        except Exception as e:
            print(f"    ⚠️  cloc failed: {e}")
            # Fall back to manual counting
            return self._collect_manual()

        return snapshot

    def _collect_manual(self) -> Dict[str, Any]:
        """Manually count LOC using find and wc."""
        print("  ➤ Using manual counting (less accurate)...")

        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_lines": 0,
            "code_lines": 0,
            "comment_lines": 0,
            "blank_lines": 0,
            "languages": {},
            "file_count": 0,
        }

        # Define file extensions for different languages
        language_extensions = {
            "Python": [".py"],
            "JavaScript": [".js", ".jsx"],
            "TypeScript": [".ts", ".tsx"],
            "Java": [".java"],
            "C": [".c", ".h"],
            "C++": [".cpp", ".cc", ".cxx", ".hpp"],
            "Go": [".go"],
            "Rust": [".rs"],
            "Ruby": [".rb"],
            "PHP": [".php"],
            "Shell": [".sh", ".bash"],
            "HTML": [".html", ".htm"],
            "CSS": [".css", ".scss", ".sass"],
            "Markdown": [".md"],
            "JSON": [".json"],
            "YAML": [".yml", ".yaml"],
            "XML": [".xml"],
        }

        total_files = 0
        total_lines = 0

        for lang, extensions in language_extensions.items():
            lang_lines = 0
            lang_files = 0

            for ext in extensions:
                try:
                    # Find files with this extension
                    result = subprocess.run(
                        ["find", ".", "-name", f"*{ext}", "-type", "f"],
                        cwd=self.repo_path,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )

                    if result.returncode == 0:
                        files = [f for f in result.stdout.splitlines() if f.strip()]
                        files = [f for f in files if not self._should_exclude(f)]

                        for filepath in files:
                            try:
                                # Count lines in file
                                wc_result = subprocess.run(
                                    ["wc", "-l", filepath],
                                    cwd=self.repo_path,
                                    capture_output=True,
                                    text=True,
                                    timeout=5
                                )

                                if wc_result.returncode == 0:
                                    lines = int(wc_result.stdout.split()[0])
                                    lang_lines += lines
                                    lang_files += 1

                            except Exception:
                                continue

                except Exception:
                    continue

            if lang_files > 0:
                snapshot["languages"][lang] = {
                    "files": lang_files,
                    "code": lang_lines,  # We can't separate blank/comment without parsing
                    "blank": 0,
                    "comment": 0,
                }
                total_files += lang_files
                total_lines += lang_lines

        snapshot["file_count"] = total_files
        snapshot["total_lines"] = total_lines
        snapshot["code_lines"] = total_lines  # Approximate

        return snapshot

    def collect_git_history(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Collect LOC changes from git history.

        Args:
            days: Number of days to look back

        Returns:
            List of daily change records
        """
        print(f"📈 Collecting git history (last {days} days)...")

        if not self._is_git_repo():
            print("  ⚠️  Not a git repository")
            return []

        changes = []

        try:
            # Get commits from the last N days
            since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

            result = subprocess.run(
                ["git", "log", f"--since={since_date}", "--format=%H|%ci|%an", "--reverse"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                return []

            commits = []
            for line in result.stdout.splitlines():
                if not line.strip():
                    continue

                parts = line.split("|")
                if len(parts) >= 3:
                    commits.append({
                        "hash": parts[0],
                        "date": parts[1].split()[0],  # Extract date
                        "author": parts[2],
                    })

            # Group by date
            daily_commits = defaultdict(list)
            for commit in commits:
                daily_commits[commit["date"]].append(commit)

            # Collect stats for each day
            for date, day_commits in sorted(daily_commits.items()):
                total_added = 0
                total_deleted = 0

                for commit in day_commits:
                    try:
                        # Get numstat for this commit
                        stat_result = subprocess.run(
                            ["git", "show", "--numstat", "--format=", commit["hash"]],
                            cwd=self.repo_path,
                            capture_output=True,
                            text=True,
                            timeout=10
                        )

                        if stat_result.returncode == 0:
                            for stat_line in stat_result.stdout.splitlines():
                                if not stat_line.strip():
                                    continue

                                parts = stat_line.split()
                                if len(parts) >= 3:
                                    try:
                                        added = int(parts[0]) if parts[0] != "-" else 0
                                        deleted = int(parts[1]) if parts[1] != "-" else 0
                                        total_added += added
                                        total_deleted += deleted
                                    except ValueError:
                                        continue

                    except Exception:
                        continue

                changes.append({
                    "date": date,
                    "commits": len(day_commits),
                    "lines_added": total_added,
                    "lines_deleted": total_deleted,
                    "net_change": total_added - total_deleted,
                })

        except Exception as e:
            print(f"  ⚠️  Failed to collect git history: {e}")

        return changes

    def update_history_with_snapshot(self, snapshot: Dict[str, Any]) -> None:
        """
        Add current snapshot to history.

        Args:
            snapshot: Current snapshot data
        """
        date = snapshot["date"]

        # Check if we already have a record for today
        existing_idx = None
        for i, record in enumerate(self.history):
            if record.get("date") == date:
                existing_idx = i
                break

        if existing_idx is not None:
            # Update existing record
            self.history[existing_idx] = snapshot
            print(f"  ➤ Updated existing record for {date}")
        else:
            # Add new record
            self.history.append(snapshot)
            print(f"  ➤ Added new record for {date}")

        # Keep only last 90 days
        cutoff_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        self.history = [
            record for record in self.history
            if record.get("date", "") >= cutoff_date
        ]

    # Helper methods

    def _is_git_repo(self) -> bool:
        """Check if current directory is a git repository."""
        return (self.repo_path / ".git").exists()

    def _command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH."""
        try:
            subprocess.run(
                ["which", command],
                capture_output=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def _should_exclude(self, filepath: str) -> bool:
        """Check if filepath should be excluded."""
        exclude_patterns = [
            ".git/",
            "node_modules/",
            "venv/",
            ".venv/",
            "__pycache__/",
            "dist/",
            "build/",
            ".egg-info/",
        ]

        return any(pattern in filepath for pattern in exclude_patterns)


def main():
    """Main entry point."""
    print("=" * 60)
    print("📈 LOC Trend Collector")
    print("=" * 60)
    print()

    collector = LOCTrendCollector()
    collector.load_history()

    # Collect current snapshot
    snapshot = collector.collect_current_snapshot()

    print()
    print("📊 Current Snapshot:")
    print(f"  • Total Lines: {snapshot['total_lines']:,}")
    print(f"  • Code Lines: {snapshot['code_lines']:,}")
    print(f"  • Files: {snapshot['file_count']:,}")
    print(f"  • Languages: {len(snapshot['languages'])}")

    # Update history
    print()
    collector.update_history_with_snapshot(snapshot)

    # Save history
    print()
    collector.save_history()

    print()
    print("=" * 60)
    print("✅ LOC trend collection complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
