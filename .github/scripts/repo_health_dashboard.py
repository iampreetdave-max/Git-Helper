#!/usr/bin/env python3
"""
Modular Repo Health Dashboard Generator

Generates a beautiful Markdown dashboard from collected metrics.
Designed to be injected into README.md
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class RepoHealthDashboard:
    """Generates a health dashboard from metrics."""

    def __init__(self, metrics_file: str = "repo_health_metrics.json"):
        """
        Initialize dashboard generator.

        Args:
            metrics_file: Path to metrics JSON file
        """
        self.metrics_file = Path(metrics_file)
        self.metrics: Optional[Dict[str, Any]] = None

    def load_metrics(self) -> bool:
        """
        Load metrics from JSON file.

        Returns:
            True if successful, False otherwise
        """
        if not self.metrics_file.exists():
            print(f"❌ Metrics file not found: {self.metrics_file}")
            return False

        try:
            with open(self.metrics_file) as f:
                self.metrics = json.load(f)
            print(f"✅ Loaded metrics from {self.metrics_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to load metrics: {e}")
            return False

    def generate_dashboard(self) -> str:
        """
        Generate complete dashboard markdown.

        Returns:
            Dashboard markdown string
        """
        if not self.metrics:
            raise ValueError("Metrics not loaded. Call load_metrics() first.")

        sections = [
            self._generate_header(),
            self._generate_overview(),
            self._generate_code_quality(),
            self._generate_contributors(),
            self._generate_activity(),
            self._generate_hotspots(),
            self._generate_footer(),
        ]

        return "\n\n".join(sections)

    def _generate_header(self) -> str:
        """Generate dashboard header."""
        timestamp = self.metrics.get("timestamp", "Unknown")
        try:
            dt = datetime.fromisoformat(timestamp)
            formatted_time = dt.strftime("%B %d, %Y at %H:%M UTC")
        except:
            formatted_time = timestamp

        return f"""## 📊 Repository Health Dashboard

> Last updated: **{formatted_time}**"""

    def _generate_overview(self) -> str:
        """Generate overview section with key metrics."""
        coverage = self.metrics.get("code_coverage", {})
        lint = self.metrics.get("lint_score", {})
        contributors = self.metrics.get("active_contributors", {})
        commits = self.metrics.get("commit_frequency", {})

        # Get values with defaults
        coverage_pct = coverage.get("percentage", 0)
        lint_score = lint.get("overall_score", 0)
        active_contrib = contributors.get("count", 0)
        commits_30d = commits.get("total_commits", 0)

        # Status emojis
        coverage_emoji = self._get_status_emoji(coverage_pct, 80, 50)
        lint_emoji = self._get_status_emoji(lint_score, 7, 5)

        return f"""### 🎯 Key Metrics

| Metric | Value | Status |
|--------|-------|--------|
| 🔬 Code Coverage | **{coverage_pct}%** | {coverage_emoji} |
| ✨ Lint Score | **{lint_score}/10** | {lint_emoji} |
| 👥 Active Contributors (90d) | **{active_contrib}** | {self._get_contributor_emoji(active_contrib)} |
| 📈 Commits (30d) | **{commits_30d}** | {self._get_activity_emoji(commits_30d)} |"""

    def _generate_code_quality(self) -> str:
        """Generate code quality section."""
        coverage = self.metrics.get("code_coverage", {})
        lint = self.metrics.get("lint_score", {})

        coverage_pct = coverage.get("percentage", 0)
        lines_covered = coverage.get("lines_covered", 0)
        lines_total = coverage.get("lines_total", 0)
        coverage_status = coverage.get("status", "unknown")

        lint_score = lint.get("overall_score", 0)
        pylint_score = lint.get("pylint_score", "N/A")
        flake8_issues = lint.get("flake8_issues", 0)
        total_issues = lint.get("total_issues", 0)

        # Coverage bar
        coverage_bar = self._generate_progress_bar(coverage_pct, 100)

        # Lint bar
        lint_bar = self._generate_progress_bar(lint_score, 10)

        coverage_detail = ""
        if coverage_status == "measured":
            coverage_detail = f"\n- **Lines Covered:** {lines_covered:,} / {lines_total:,}"

        lint_detail = ""
        if pylint_score != "N/A":
            lint_detail = f"\n- **Pylint Score:** {pylint_score}/10\n- **Flake8 Issues:** {flake8_issues}\n- **Total Issues:** {total_issues}"

        return f"""### 📊 Code Quality

#### Code Coverage
{coverage_bar} **{coverage_pct}%**{coverage_detail}

#### Lint Score
{lint_bar} **{lint_score}/10**{lint_detail}"""

    def _generate_contributors(self) -> str:
        """Generate contributors section."""
        contributors = self.metrics.get("active_contributors", {})

        count = contributors.get("count", 0)
        top_contributor = contributors.get("top_contributor")
        contrib_list = contributors.get("contributors", [])

        if count == 0:
            return """### 👥 Contributors

No contributors found in the last 90 days."""

        # Top 5 contributors
        top_5 = contrib_list[:5]
        contributor_rows = "\n".join([
            f"| {i+1}. **{c['name']}** | {c['commits']} commits |"
            for i, c in enumerate(top_5)
        ])

        return f"""### 👥 Active Contributors (Last 90 Days)

**Total Contributors:** {count}

#### Top Contributors

| Contributor | Contributions |
|-------------|---------------|
{contributor_rows}"""

    def _generate_activity(self) -> str:
        """Generate activity section."""
        commits = self.metrics.get("commit_frequency", {})
        top_files = self.metrics.get("top_modified_files", {})

        total_commits = commits.get("total_commits", 0)
        commits_per_day = commits.get("commits_per_day", 0)
        most_active = commits.get("most_active_day")
        files = top_files.get("files", [])

        activity_emoji = self._get_activity_emoji(total_commits)

        most_active_str = ""
        if most_active:
            most_active_str = f"\n- **Most Active Day:** {most_active['date']} ({most_active['commits']} commits)"

        # Top 5 files
        file_rows = ""
        if files:
            top_5_files = files[:5]
            file_rows = "\n\n#### Most Modified Files\n\n| File | Modifications |\n|------|---------------|\n"
            file_rows += "\n".join([
                f"| `{f['path']}` | {f['modifications']} |"
                for f in top_5_files
            ])

        return f"""### 📈 Repository Activity (Last 30 Days)

{activity_emoji} **{total_commits} commits** ({commits_per_day} per day){most_active_str}{file_rows}"""

    def _generate_hotspots(self) -> str:
        """Generate error hotspots section."""
        hotspots = self.metrics.get("error_hotspots", {})

        hotspot_list = hotspots.get("hotspots", [])
        total_issues = hotspots.get("total_issues", 0)

        if not hotspot_list:
            return """### 🔥 Error Hotspots

✅ No significant error hotspots detected."""

        # Top 5 hotspots
        top_5 = hotspot_list[:5]
        hotspot_rows = "\n".join([
            f"| `{h['file']}` | {h['total_issues']} | {self._format_issue_types(h['issue_types'])} |"
            for h in top_5
        ])

        return f"""### 🔥 Error Hotspots

**Total Issues Across Codebase:** {total_issues}

| File | Issues | Types |
|------|--------|-------|
{hotspot_rows}"""

    def _generate_footer(self) -> str:
        """Generate dashboard footer."""
        return """---

*Dashboard automatically generated by [Git-Helper](https://github.com/iampreetdave-max/Git-Helper)*"""

    # Helper methods for formatting

    def _generate_progress_bar(self, value: float, max_value: float, width: int = 20) -> str:
        """
        Generate a progress bar.

        Args:
            value: Current value
            max_value: Maximum value
            width: Bar width in characters

        Returns:
            Progress bar string
        """
        percentage = min(value / max_value, 1.0)
        filled = int(width * percentage)
        empty = width - filled

        bar = "█" * filled + "░" * empty

        # Color based on percentage
        if percentage >= 0.8:
            return f"🟢 {bar}"
        elif percentage >= 0.5:
            return f"🟡 {bar}"
        else:
            return f"🔴 {bar}"

    def _get_status_emoji(self, value: float, good_threshold: float, ok_threshold: float) -> str:
        """Get status emoji based on value and thresholds."""
        if value >= good_threshold:
            return "🟢 Excellent"
        elif value >= ok_threshold:
            return "🟡 Good"
        else:
            return "🔴 Needs Improvement"

    def _get_contributor_emoji(self, count: int) -> str:
        """Get emoji for contributor count."""
        if count >= 5:
            return "🟢 Active"
        elif count >= 2:
            return "🟡 Moderate"
        else:
            return "🔴 Low"

    def _get_activity_emoji(self, commits: int) -> str:
        """Get emoji for commit activity."""
        if commits >= 30:
            return "🔥"
        elif commits >= 10:
            return "📈"
        else:
            return "📉"

    def _format_issue_types(self, issue_types: Dict[str, int]) -> str:
        """Format issue types dictionary."""
        if not issue_types:
            return "—"

        # Show top 2 issue types
        sorted_types = sorted(issue_types.items(), key=lambda x: x[1], reverse=True)
        top_2 = sorted_types[:2]

        return ", ".join([f"{t[0]}: {t[1]}" for t in top_2])

    def save_dashboard(self, output_file: str = "HEALTH_DASHBOARD.md") -> None:
        """
        Save dashboard to markdown file.

        Args:
            output_file: Output filename
        """
        dashboard = self.generate_dashboard()

        try:
            with open(output_file, 'w') as f:
                f.write(dashboard)
            print(f"✅ Dashboard saved to {output_file}")
        except Exception as e:
            print(f"❌ Failed to save dashboard: {e}")
            sys.exit(1)

    def inject_into_readme(self, readme_file: str = "README.md") -> bool:
        """
        Inject dashboard into README.md.

        Args:
            readme_file: Path to README file

        Returns:
            True if successful, False otherwise
        """
        readme_path = Path(readme_file)

        if not readme_path.exists():
            print(f"❌ README not found: {readme_file}")
            return False

        try:
            with open(readme_path, 'r') as f:
                content = f.read()

            dashboard = self.generate_dashboard()

            # Markers for injection
            start_marker = "<!-- HEALTH_DASHBOARD_START -->"
            end_marker = "<!-- HEALTH_DASHBOARD_END -->"

            # Check if markers exist
            if start_marker in content and end_marker in content:
                # Replace existing dashboard
                start_idx = content.index(start_marker)
                end_idx = content.index(end_marker) + len(end_marker)

                new_content = (
                    content[:start_idx] +
                    f"{start_marker}\n\n{dashboard}\n\n{end_marker}" +
                    content[end_idx:]
                )
            else:
                # Append to end
                new_content = content.rstrip() + f"\n\n{start_marker}\n\n{dashboard}\n\n{end_marker}\n"

            # Write back
            with open(readme_path, 'w') as f:
                f.write(new_content)

            print(f"✅ Dashboard injected into {readme_file}")
            return True

        except Exception as e:
            print(f"❌ Failed to inject dashboard: {e}")
            return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate Repo Health Dashboard")
    parser.add_argument(
        "--metrics",
        default="repo_health_metrics.json",
        help="Path to metrics JSON file"
    )
    parser.add_argument(
        "--output",
        default="HEALTH_DASHBOARD.md",
        help="Output markdown file"
    )
    parser.add_argument(
        "--inject-readme",
        action="store_true",
        help="Inject dashboard into README.md"
    )
    parser.add_argument(
        "--readme",
        default="README.md",
        help="Path to README file"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("📊 Repository Health Dashboard Generator")
    print("=" * 60)
    print()

    dashboard = RepoHealthDashboard(args.metrics)

    if not dashboard.load_metrics():
        sys.exit(1)

    # Generate and save dashboard
    dashboard.save_dashboard(args.output)

    # Inject into README if requested
    if args.inject_readme:
        print()
        dashboard.inject_into_readme(args.readme)

    print()
    print("=" * 60)
    print("✅ Dashboard generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
