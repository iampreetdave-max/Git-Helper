#!/usr/bin/env python3
"""
Modular LOC Trend Visualizer

Generates PNG/SVG charts for:
- Daily LOC changes
- Added/deleted code trends
- Language distribution over time

Uses matplotlib for visualization.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.patches import Rectangle
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  matplotlib not available. Install with: pip install matplotlib")


class LOCTrendVisualizer:
    """Generates visualizations from LOC trend data."""

    def __init__(self, history_file: str = ".github/loc_history.json"):
        """
        Initialize visualizer.

        Args:
            history_file: Path to history JSON file
        """
        self.history_file = Path(history_file)
        self.history: List[Dict[str, Any]] = []
        self.output_dir = Path("loc_charts")

        if not MATPLOTLIB_AVAILABLE:
            print("❌ matplotlib is required for visualization")
            sys.exit(1)

    def load_history(self) -> bool:
        """
        Load history from file.

        Returns:
            True if successful, False otherwise
        """
        if not self.history_file.exists():
            print(f"❌ History file not found: {self.history_file}")
            return False

        try:
            with open(self.history_file) as f:
                self.history = json.load(f)
            print(f"✅ Loaded {len(self.history)} historical records")
            return len(self.history) > 0
        except Exception as e:
            print(f"❌ Failed to load history: {e}")
            return False

    def generate_all_charts(self, formats: List[str] = ["png", "svg"]) -> None:
        """
        Generate all available charts.

        Args:
            formats: List of output formats (png, svg)
        """
        if not self.history:
            print("❌ No history data to visualize")
            return

        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        print(f"📁 Output directory: {self.output_dir}")
        print()

        # Generate each chart
        self.generate_loc_trend_chart(formats)
        self.generate_change_activity_chart(formats)
        self.generate_language_distribution_chart(formats)
        self.generate_combined_overview_chart(formats)

    def generate_loc_trend_chart(self, formats: List[str] = ["png"]) -> None:
        """
        Generate LOC trend over time chart.

        Args:
            formats: Output formats
        """
        print("📊 Generating LOC trend chart...")

        if len(self.history) < 2:
            print("  ⚠️  Need at least 2 data points")
            return

        # Prepare data
        dates = []
        total_lines = []
        code_lines = []

        for record in sorted(self.history, key=lambda x: x.get("date", "")):
            try:
                date = datetime.strptime(record["date"], "%Y-%m-%d")
                dates.append(date)
                total_lines.append(record.get("total_lines", 0))
                code_lines.append(record.get("code_lines", 0))
            except Exception:
                continue

        if not dates:
            print("  ⚠️  No valid data")
            return

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot lines
        ax.plot(dates, total_lines, label="Total Lines", marker='o', linewidth=2)
        ax.plot(dates, code_lines, label="Code Lines", marker='s', linewidth=2)

        # Formatting
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Lines of Code", fontsize=12)
        ax.set_title("Lines of Code Trend", fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()

        # Save in requested formats
        for fmt in formats:
            output_file = self.output_dir / f"loc_trend.{fmt}"
            plt.savefig(output_file, format=fmt, dpi=300 if fmt == 'png' else None)
            print(f"  ✅ Saved: {output_file}")

        plt.close()

    def generate_change_activity_chart(self, formats: List[str] = ["png"]) -> None:
        """
        Generate code change activity chart (added/deleted lines).

        Args:
            formats: Output formats
        """
        print("📊 Generating change activity chart...")

        # Calculate daily changes
        dates = []
        changes = []

        sorted_history = sorted(self.history, key=lambda x: x.get("date", ""))

        for i in range(1, len(sorted_history)):
            prev = sorted_history[i - 1]
            curr = sorted_history[i]

            try:
                date = datetime.strptime(curr["date"], "%Y-%m-%d")
                prev_lines = prev.get("code_lines", 0)
                curr_lines = curr.get("code_lines", 0)
                change = curr_lines - prev_lines

                dates.append(date)
                changes.append(change)
            except Exception:
                continue

        if not dates:
            print("  ⚠️  No change data available")
            return

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))

        # Create colors for positive/negative changes
        colors = ['green' if c >= 0 else 'red' for c in changes]

        # Plot bars
        ax.bar(dates, changes, color=colors, alpha=0.7, width=0.8)

        # Add zero line
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

        # Formatting
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Lines Changed", fontsize=12)
        ax.set_title("Daily Code Changes (Added/Removed)", fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha='right')

        # Add legend
        green_patch = Rectangle((0, 0), 1, 1, fc="green", alpha=0.7)
        red_patch = Rectangle((0, 0), 1, 1, fc="red", alpha=0.7)
        ax.legend([green_patch, red_patch], ['Added', 'Removed'])

        plt.tight_layout()

        # Save in requested formats
        for fmt in formats:
            output_file = self.output_dir / f"change_activity.{fmt}"
            plt.savefig(output_file, format=fmt, dpi=300 if fmt == 'png' else None)
            print(f"  ✅ Saved: {output_file}")

        plt.close()

    def generate_language_distribution_chart(self, formats: List[str] = ["png"]) -> None:
        """
        Generate language distribution over time chart.

        Args:
            formats: Output formats
        """
        print("📊 Generating language distribution chart...")

        if not self.history:
            print("  ⚠️  No history data")
            return

        # Get latest snapshot for current distribution
        latest = self.history[-1]
        languages = latest.get("languages", {})

        if not languages:
            print("  ⚠️  No language data available")
            return

        # Prepare data for pie chart
        lang_names = []
        lang_lines = []

        for lang, data in sorted(
            languages.items(),
            key=lambda x: x[1].get("code", 0),
            reverse=True
        ):
            code_lines = data.get("code", 0)
            if code_lines > 0:
                lang_names.append(lang)
                lang_lines.append(code_lines)

        if not lang_names:
            print("  ⚠️  No language data")
            return

        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Pie chart
        colors = plt.cm.Set3(range(len(lang_names)))
        ax1.pie(lang_lines, labels=lang_names, autopct='%1.1f%%',
                colors=colors, startangle=90)
        ax1.set_title("Language Distribution (Current)", fontsize=14, fontweight='bold')

        # Bar chart
        ax2.barh(lang_names, lang_lines, color=colors)
        ax2.set_xlabel("Lines of Code", fontsize=12)
        ax2.set_title("Lines of Code by Language", fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')

        plt.tight_layout()

        # Save in requested formats
        for fmt in formats:
            output_file = self.output_dir / f"language_distribution.{fmt}"
            plt.savefig(output_file, format=fmt, dpi=300 if fmt == 'png' else None)
            print(f"  ✅ Saved: {output_file}")

        plt.close()

    def generate_combined_overview_chart(self, formats: List[str] = ["png"]) -> None:
        """
        Generate a combined overview chart with multiple metrics.

        Args:
            formats: Output formats
        """
        print("📊 Generating combined overview chart...")

        if len(self.history) < 2:
            print("  ⚠️  Need at least 2 data points")
            return

        # Prepare data
        dates = []
        total_lines = []
        file_counts = []
        language_counts = []

        for record in sorted(self.history, key=lambda x: x.get("date", "")):
            try:
                date = datetime.strptime(record["date"], "%Y-%m-%d")
                dates.append(date)
                total_lines.append(record.get("total_lines", 0))
                file_counts.append(record.get("file_count", 0))
                language_counts.append(len(record.get("languages", {})))
            except Exception:
                continue

        if not dates:
            print("  ⚠️  No valid data")
            return

        # Create figure with 3 subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

        # Plot 1: Total lines trend
        ax1.plot(dates, total_lines, marker='o', linewidth=2, color='blue')
        ax1.set_ylabel("Total Lines", fontsize=11)
        ax1.set_title("Repository Overview", fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)

        # Plot 2: File count trend
        ax2.plot(dates, file_counts, marker='s', linewidth=2, color='green')
        ax2.set_ylabel("File Count", fontsize=11)
        ax2.grid(True, alpha=0.3)

        # Plot 3: Language count trend
        ax3.plot(dates, language_counts, marker='^', linewidth=2, color='orange')
        ax3.set_xlabel("Date", fontsize=12)
        ax3.set_ylabel("Language Count", fontsize=11)
        ax3.grid(True, alpha=0.3)

        # Format x-axis dates for all subplots
        for ax in [ax1, ax2, ax3]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.tight_layout()

        # Save in requested formats
        for fmt in formats:
            output_file = self.output_dir / f"overview.{fmt}"
            plt.savefig(output_file, format=fmt, dpi=300 if fmt == 'png' else None)
            print(f"  ✅ Saved: {output_file}")

        plt.close()

    def generate_summary_markdown(self) -> str:
        """
        Generate markdown summary with embedded charts.

        Returns:
            Markdown string
        """
        if not self.history:
            return "No data available"

        latest = self.history[-1]

        md = f"""## 📈 Lines of Code Trends

### Current Statistics (as of {latest.get('date', 'Unknown')})

- **Total Lines:** {latest.get('total_lines', 0):,}
- **Code Lines:** {latest.get('code_lines', 0):,}
- **Files:** {latest.get('file_count', 0):,}
- **Languages:** {len(latest.get('languages', {})):,}

### Visualizations

#### LOC Trend Over Time
![LOC Trend](loc_charts/loc_trend.png)

#### Daily Code Changes
![Change Activity](loc_charts/change_activity.png)

#### Language Distribution
![Language Distribution](loc_charts/language_distribution.png)

#### Repository Overview
![Overview](loc_charts/overview.png)

---

*Charts generated by [Git-Helper](https://github.com/iampreetdave-max/Git-Helper)*
"""

        return md

    def save_summary_markdown(self, output_file: str = "LOC_TRENDS.md") -> None:
        """
        Save markdown summary to file.

        Args:
            output_file: Output filename
        """
        md = self.generate_summary_markdown()

        try:
            with open(output_file, 'w') as f:
                f.write(md)
            print(f"✅ Summary saved to {output_file}")
        except Exception as e:
            print(f"❌ Failed to save summary: {e}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate LOC Trend Charts")
    parser.add_argument(
        "--history",
        default=".github/loc_history.json",
        help="Path to history JSON file"
    )
    parser.add_argument(
        "--format",
        nargs="+",
        default=["png"],
        choices=["png", "svg"],
        help="Output format(s)"
    )
    parser.add_argument(
        "--output-dir",
        default="loc_charts",
        help="Output directory for charts"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Generate markdown summary"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("📈 LOC Trend Visualizer")
    print("=" * 60)
    print()

    visualizer = LOCTrendVisualizer(args.history)
    visualizer.output_dir = Path(args.output_dir)

    if not visualizer.load_history():
        sys.exit(1)

    print()
    visualizer.generate_all_charts(args.format)

    if args.summary:
        print()
        visualizer.save_summary_markdown()

    print()
    print("=" * 60)
    print("✅ Visualization complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
