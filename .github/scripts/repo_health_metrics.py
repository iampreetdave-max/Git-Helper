#!/usr/bin/env python3
"""
Modular Repo Health Metrics Collector

Collects comprehensive repository health metrics including:
- Code coverage
- Lint scores
- Active contributors
- Commit frequency
- Top modified files
- Error hotspots
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict


class RepoHealthMetrics:
    """Collects and calculates repository health metrics."""

    def __init__(self, repo_path: str = "."):
        """
        Initialize metrics collector.

        Args:
            repo_path: Path to repository root
        """
        self.repo_path = Path(repo_path).resolve()
        self.metrics: Dict[str, Any] = {}

    def collect_all_metrics(self) -> Dict[str, Any]:
        """
        Collect all available metrics.

        Returns:
            Dictionary containing all metrics
        """
        print("📊 Collecting repository health metrics...")

        self.metrics = {
            "timestamp": datetime.now().isoformat(),
            "code_coverage": self.get_code_coverage(),
            "lint_score": self.get_lint_score(),
            "active_contributors": self.get_active_contributors(),
            "commit_frequency": self.get_commit_frequency(),
            "top_modified_files": self.get_top_modified_files(),
            "error_hotspots": self.get_error_hotspots(),
        }

        return self.metrics

    def get_code_coverage(self) -> Dict[str, Any]:
        """
        Calculate code coverage from test results.

        Returns:
            Coverage metrics dictionary
        """
        print("  ➤ Analyzing code coverage...")

        coverage_data = {
            "percentage": 0.0,
            "lines_covered": 0,
            "lines_total": 0,
            "status": "unknown",
        }

        # Try to find coverage data from various sources
        coverage_files = [
            self.repo_path / "coverage.json",
            self.repo_path / ".coverage",
            self.repo_path / "htmlcov" / "index.html",
        ]

        # Check for coverage.json (pytest-cov)
        coverage_json = self.repo_path / "coverage.json"
        if coverage_json.exists():
            try:
                with open(coverage_json) as f:
                    data = json.load(f)
                    totals = data.get("totals", {})
                    coverage_data["percentage"] = round(totals.get("percent_covered", 0), 2)
                    coverage_data["lines_covered"] = totals.get("covered_lines", 0)
                    coverage_data["lines_total"] = totals.get("num_statements", 0)
                    coverage_data["status"] = "measured"
            except Exception as e:
                print(f"    ⚠️  Could not parse coverage.json: {e}")

        # Fallback: Try to run pytest with coverage
        elif self._command_exists("pytest"):
            try:
                result = subprocess.run(
                    ["pytest", "--cov=.", "--cov-report=json", "--quiet"],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode == 0 and coverage_json.exists():
                    return self.get_code_coverage()  # Recursive call after generating
            except Exception as e:
                print(f"    ⚠️  Could not run pytest: {e}")

        # Check analysis_results.json
        analysis_file = self.repo_path / "analysis_results.json"
        if analysis_file.exists() and coverage_data["status"] == "unknown":
            try:
                with open(analysis_file) as f:
                    data = json.load(f)
                    if "test_coverage" in data:
                        cov = data["test_coverage"]
                        coverage_data["percentage"] = cov.get("coverage_percentage", 0)
                        coverage_data["status"] = "measured"
            except Exception as e:
                print(f"    ⚠️  Could not parse analysis_results.json: {e}")

        return coverage_data

    def get_lint_score(self) -> Dict[str, Any]:
        """
        Calculate overall lint score from various linters.

        Returns:
            Lint score metrics dictionary
        """
        print("  ➤ Calculating lint score...")

        lint_data = {
            "overall_score": 0.0,
            "pylint_score": None,
            "flake8_issues": 0,
            "total_issues": 0,
            "status": "unknown",
        }

        # Check analysis_results.json for lint data
        analysis_file = self.repo_path / "analysis_results.json"
        if analysis_file.exists():
            try:
                with open(analysis_file) as f:
                    data = json.load(f)

                    # Get pylint score
                    if "code_quality" in data and "pylint" in data["code_quality"]:
                        pylint_data = data["code_quality"]["pylint"]
                        lint_data["pylint_score"] = pylint_data.get("score", 0)

                    # Get flake8 issues
                    if "code_quality" in data and "flake8" in data["code_quality"]:
                        flake8_data = data["code_quality"]["flake8"]
                        lint_data["flake8_issues"] = flake8_data.get("total_issues", 0)

                    # Calculate total issues
                    lint_data["total_issues"] = lint_data["flake8_issues"]

                    # Calculate overall score (0-100)
                    # Weight: 70% pylint, 30% flake8
                    if lint_data["pylint_score"] is not None:
                        pylint_normalized = lint_data["pylint_score"]  # Already 0-10
                        flake8_penalty = min(lint_data["flake8_issues"] * 0.1, 10)  # Max 10 points
                        lint_data["overall_score"] = round(
                            (pylint_normalized * 0.7 + (10 - flake8_penalty) * 0.3), 2
                        )
                        lint_data["status"] = "measured"
            except Exception as e:
                print(f"    ⚠️  Could not parse analysis data: {e}")

        return lint_data

    def get_active_contributors(self, days: int = 90) -> Dict[str, Any]:
        """
        Get active contributors in the last N days.

        Args:
            days: Number of days to look back

        Returns:
            Contributors data dictionary
        """
        print(f"  ➤ Finding active contributors (last {days} days)...")

        contributors_data = {
            "count": 0,
            "contributors": [],
            "top_contributor": None,
        }

        if not self._is_git_repo():
            return contributors_data

        try:
            since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

            # Get commit authors
            result = subprocess.run(
                ["git", "log", f"--since={since_date}", "--format=%aN"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                authors = [line.strip() for line in result.stdout.splitlines() if line.strip()]

                # Count commits per author
                author_counts = defaultdict(int)
                for author in authors:
                    author_counts[author] += 1

                # Sort by commit count
                sorted_contributors = sorted(
                    author_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                )

                contributors_data["count"] = len(sorted_contributors)
                contributors_data["contributors"] = [
                    {"name": name, "commits": count}
                    for name, count in sorted_contributors
                ]

                if sorted_contributors:
                    contributors_data["top_contributor"] = sorted_contributors[0][0]

        except Exception as e:
            print(f"    ⚠️  Could not get contributors: {e}")

        return contributors_data

    def get_commit_frequency(self, days: int = 30) -> Dict[str, Any]:
        """
        Calculate commit frequency over the last N days.

        Args:
            days: Number of days to analyze

        Returns:
            Commit frequency data dictionary
        """
        print(f"  ➤ Analyzing commit frequency (last {days} days)...")

        frequency_data = {
            "total_commits": 0,
            "commits_per_day": 0.0,
            "days_analyzed": days,
            "most_active_day": None,
        }

        if not self._is_git_repo():
            return frequency_data

        try:
            since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

            # Get commit dates
            result = subprocess.run(
                ["git", "log", f"--since={since_date}", "--format=%ci"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                commit_dates = [
                    line.split()[0]  # Extract date (YYYY-MM-DD)
                    for line in result.stdout.splitlines()
                    if line.strip()
                ]

                frequency_data["total_commits"] = len(commit_dates)
                frequency_data["commits_per_day"] = round(
                    len(commit_dates) / days, 2
                )

                # Find most active day
                if commit_dates:
                    day_counts = defaultdict(int)
                    for date in commit_dates:
                        day_counts[date] += 1

                    most_active = max(day_counts.items(), key=lambda x: x[1])
                    frequency_data["most_active_day"] = {
                        "date": most_active[0],
                        "commits": most_active[1]
                    }

        except Exception as e:
            print(f"    ⚠️  Could not analyze commit frequency: {e}")

        return frequency_data

    def get_top_modified_files(self, limit: int = 10) -> Dict[str, Any]:
        """
        Get most frequently modified files.

        Args:
            limit: Maximum number of files to return

        Returns:
            Top modified files data dictionary
        """
        print(f"  ➤ Finding top {limit} modified files...")

        files_data = {
            "files": [],
            "total_analyzed": 0,
        }

        if not self._is_git_repo():
            return files_data

        try:
            # Get file change counts
            result = subprocess.run(
                ["git", "log", "--format=", "--name-only", "--diff-filter=M"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                file_lines = [
                    line.strip()
                    for line in result.stdout.splitlines()
                    if line.strip()
                ]

                # Count modifications per file
                file_counts = defaultdict(int)
                for filepath in file_lines:
                    file_counts[filepath] += 1

                # Sort by modification count
                sorted_files = sorted(
                    file_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:limit]

                files_data["total_analyzed"] = len(file_counts)
                files_data["files"] = [
                    {"path": path, "modifications": count}
                    for path, count in sorted_files
                ]

        except Exception as e:
            print(f"    ⚠️  Could not get modified files: {e}")

        return files_data

    def get_error_hotspots(self) -> Dict[str, Any]:
        """
        Identify files with most errors/issues.

        Returns:
            Error hotspots data dictionary
        """
        print("  ➤ Identifying error hotspots...")

        hotspots_data = {
            "hotspots": [],
            "total_issues": 0,
        }

        # Check analysis_results.json for error data
        analysis_file = self.repo_path / "analysis_results.json"
        if not analysis_file.exists():
            return hotspots_data

        try:
            with open(analysis_file) as f:
                data = json.load(f)

            file_issues = defaultdict(lambda: {"total": 0, "types": defaultdict(int)})

            # Collect issues from various sources
            sources = [
                ("code_quality", "pylint", "issues"),
                ("code_quality", "flake8", "issues"),
                ("security", "bandit", "issues"),
            ]

            for source in sources:
                section = data
                for key in source[:-1]:
                    section = section.get(key, {})

                issues = section.get(source[-1], [])
                for issue in issues:
                    if isinstance(issue, dict) and "file" in issue:
                        filepath = issue["file"]
                        file_issues[filepath]["total"] += 1

                        issue_type = issue.get("type", "unknown")
                        file_issues[filepath]["types"][issue_type] += 1

            # Sort by issue count
            sorted_hotspots = sorted(
                file_issues.items(),
                key=lambda x: x[1]["total"],
                reverse=True
            )[:10]

            hotspots_data["hotspots"] = [
                {
                    "file": filepath,
                    "total_issues": data["total"],
                    "issue_types": dict(data["types"])
                }
                for filepath, data in sorted_hotspots
            ]

            hotspots_data["total_issues"] = sum(
                data["total"] for data in file_issues.values()
            )

        except Exception as e:
            print(f"    ⚠️  Could not identify error hotspots: {e}")

        return hotspots_data

    def save_metrics(self, output_file: str = "repo_health_metrics.json") -> None:
        """
        Save collected metrics to JSON file.

        Args:
            output_file: Output filename
        """
        output_path = self.repo_path / output_file

        try:
            with open(output_path, 'w') as f:
                json.dump(self.metrics, f, indent=2)
            print(f"\n✅ Metrics saved to {output_file}")
        except Exception as e:
            print(f"\n❌ Failed to save metrics: {e}")
            sys.exit(1)

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


def main():
    """Main entry point."""
    print("=" * 60)
    print("🏥 Repository Health Metrics Collector")
    print("=" * 60)
    print()

    collector = RepoHealthMetrics()
    metrics = collector.collect_all_metrics()
    collector.save_metrics()

    print()
    print("=" * 60)
    print("📊 Summary:")
    print(f"  • Code Coverage: {metrics['code_coverage']['percentage']}%")
    print(f"  • Lint Score: {metrics['lint_score']['overall_score']}/10")
    print(f"  • Active Contributors: {metrics['active_contributors']['count']}")
    print(f"  • Commits (30d): {metrics['commit_frequency']['total_commits']}")
    print(f"  • Error Hotspots: {len(metrics['error_hotspots']['hotspots'])}")
    print("=" * 60)


if __name__ == "__main__":
    main()
