"""
Git-Buddy Advanced Features
===========================

Implements advanced analysis features:
- Technical Debt Index calculation
- Metric degradation alerts
- Code duplication detection
- Automated issue suggestions

These features provide actionable insights beyond basic metrics.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import math


class TechnicalDebtIndex:
    """
    Calculate Technical Debt Index based on multiple metrics.

    Technical Debt = all the shortcuts and compromises in code that make future
    development slower and more expensive.

    Weighted calculation:
    - Code Quality Issues (30%): pylint score gaps
    - Complexity Hotspots (25%): functions/files that are too complex
    - Test Coverage Gaps (20%): code not covered by tests
    - Dependency Vulnerabilities (15%): known issues in packages
    - Code Duplication (10%): repeated code blocks
    """

    def __init__(self, metrics_file: str = '.github/repo_health_metrics.json'):
        self.metrics_file = Path(metrics_file)
        self.weights = {
            'code_quality': 0.30,
            'complexity': 0.25,
            'test_coverage': 0.20,
            'dependencies': 0.15,
            'duplication': 0.10,
        }

    def calculate_debt_index(self, current_metrics: Dict) -> Dict[str, Any]:
        """
        Calculate overall Technical Debt Index (0-100, higher = more debt).

        Args:
            current_metrics: Current analysis metrics

        Returns:
            Dictionary with debt index, components, and recommendations
        """
        components = {}

        # 1. Code Quality Component (0-100, lower is worse)
        code_quality_score = current_metrics.get('code_quality_score', 5.0)
        code_quality_debt = self._calculate_code_quality_debt(code_quality_score)
        components['code_quality'] = {
            'score': code_quality_debt,
            'metric': code_quality_score,
            'weight': self.weights['code_quality']
        }

        # 2. Complexity Component
        avg_complexity = current_metrics.get('avg_complexity', 7.0)
        complexity_debt = self._calculate_complexity_debt(avg_complexity)
        components['complexity'] = {
            'score': complexity_debt,
            'metric': avg_complexity,
            'weight': self.weights['complexity']
        }

        # 3. Test Coverage Component
        test_coverage = current_metrics.get('test_coverage', 50.0)
        coverage_debt = self._calculate_coverage_debt(test_coverage)
        components['test_coverage'] = {
            'score': coverage_debt,
            'metric': test_coverage,
            'weight': self.weights['test_coverage']
        }

        # 4. Dependency Vulnerabilities Component
        dep_vulns = current_metrics.get('dependency_vulnerabilities', 0)
        dep_debt = self._calculate_dependency_debt(dep_vulns)
        components['dependencies'] = {
            'score': dep_debt,
            'metric': dep_vulns,
            'weight': self.weights['dependencies']
        }

        # 5. Code Duplication Component
        duplication = current_metrics.get('code_duplication_percent', 5.0)
        dup_debt = self._calculate_duplication_debt(duplication)
        components['duplication'] = {
            'score': dup_debt,
            'metric': duplication,
            'weight': self.weights['duplication']
        }

        # Calculate weighted average
        total_debt = sum(
            c['score'] * c['weight']
            for c in components.values()
        )

        # Generate recommendations based on largest debt sources
        recommendations = self._generate_recommendations(components)

        return {
            'total_index': round(total_debt, 2),
            'components': components,
            'severity': self._classify_severity(total_debt),
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }

    def _calculate_code_quality_debt(self, score: float) -> float:
        """Convert pylint score (0-10) to debt index (0-100)"""
        # Perfect score (10) = 0% debt
        # Failing score (0) = 100% debt
        return max(0, min(100, (10 - score) * 10))

    def _calculate_complexity_debt(self, avg_complexity: float) -> float:
        """Convert average complexity to debt index (0-100)"""
        # Acceptable: < 7 (low debt)
        # Warning: 7-15 (medium debt)
        # Critical: > 15 (high debt)
        if avg_complexity < 7:
            return 0
        elif avg_complexity < 15:
            return (avg_complexity - 7) * (50 / 8)  # 0-50% debt
        else:
            return 50 + min(50, (avg_complexity - 15) * 5)  # 50-100% debt

    def _calculate_coverage_debt(self, coverage: float) -> float:
        """Convert test coverage (0-100%) to debt index (0-100)"""
        # 80%+ coverage = low debt
        # 50-80% coverage = medium debt
        # <50% coverage = high debt
        return max(0, (100 - coverage) * 0.75)

    def _calculate_dependency_debt(self, vulns_count: int) -> float:
        """Convert vulnerability count to debt index (0-100)"""
        # 0 vulns = 0% debt
        # Each vuln adds 10% debt (up to 100)
        return min(100, vulns_count * 10)

    def _calculate_duplication_debt(self, duplication_percent: float) -> float:
        """Convert code duplication % to debt index (0-100)"""
        # 0-5% = low debt (acceptable)
        # 5-15% = medium debt
        # >15% = high debt
        if duplication_percent < 5:
            return duplication_percent * 4  # 0-20% debt
        elif duplication_percent < 15:
            return 20 + (duplication_percent - 5) * 5  # 20-70% debt
        else:
            return 70 + min(30, (duplication_percent - 15) * 2)  # 70-100% debt

    def _classify_severity(self, debt_index: float) -> str:
        """Classify debt severity level"""
        if debt_index < 20:
            return "HEALTHY"
        elif debt_index < 40:
            return "ACCEPTABLE"
        elif debt_index < 60:
            return "WARNING"
        elif debt_index < 80:
            return "CRITICAL"
        else:
            return "EXTREME"

    def _generate_recommendations(self, components: Dict) -> List[Dict[str, str]]:
        """Generate actionable recommendations based on debt components"""
        recommendations = []

        for component_name, component_data in components.items():
            debt_score = component_data['score']

            if debt_score > 60:  # High debt
                if component_name == 'code_quality':
                    recommendations.append({
                        'priority': 'HIGH',
                        'area': 'Code Quality',
                        'issue': f"Code quality score is low ({component_data['metric']}/10)",
                        'action': 'Review pylint warnings and refactor the most problematic files',
                        'tool': 'pylint'
                    })
                elif component_name == 'complexity':
                    recommendations.append({
                        'priority': 'HIGH',
                        'area': 'Complexity',
                        'issue': f"Average complexity is high ({component_data['metric']:.1f})",
                        'action': 'Break down complex functions into smaller, testable units',
                        'tool': 'radon'
                    })
                elif component_name == 'test_coverage':
                    recommendations.append({
                        'priority': 'HIGH',
                        'area': 'Test Coverage',
                        'issue': f"Test coverage is low ({component_data['metric']:.1f}%)",
                        'action': 'Write tests for uncovered code paths, focus on critical paths',
                        'tool': 'pytest'
                    })
                elif component_name == 'dependencies':
                    recommendations.append({
                        'priority': 'CRITICAL',
                        'area': 'Security',
                        'issue': f"Found {int(component_data['metric'])} dependency vulnerabilities",
                        'action': 'Update packages to patched versions immediately',
                        'tool': 'pip-audit/safety'
                    })
                elif component_name == 'duplication':
                    recommendations.append({
                        'priority': 'MEDIUM',
                        'area': 'Code Duplication',
                        'issue': f"Code duplication is {component_data['metric']:.1f}%",
                        'action': 'Extract common code into reusable functions/modules',
                        'tool': 'radon'
                    })

        return sorted(recommendations, key=lambda x: x['priority'] == 'CRITICAL', reverse=True)


class MetricDegradationDetector:
    """
    Detect when code metrics are getting worse.

    Compares current metrics with recent history to identify:
    - Code quality declining
    - Complexity increasing
    - Coverage dropping
    - New vulnerabilities introduced
    """

    def __init__(self, metrics_file: str = '.github/repo_health_metrics.json'):
        self.metrics_file = Path(metrics_file)

    def detect_degradation(self, current_metrics: Dict) -> List[Dict[str, Any]]:
        """
        Detect metric degradation compared to recent history.

        Returns:
            List of degradation alerts with details
        """
        alerts = []

        if not self.metrics_file.exists():
            return alerts

        try:
            with open(self.metrics_file) as f:
                history = json.load(f)
        except (json.JSONDecodeError, IOError):
            return alerts

        if len(history) < 2:
            return alerts

        # Compare last 2 entries
        previous = history[-2] if len(history) > 1 else history[0]
        current = current_metrics

        # Check code quality decline
        prev_quality = previous.get('code_quality_score', 5.0)
        curr_quality = current.get('code_quality_score', 5.0)
        if curr_quality < prev_quality - 0.5:
            alerts.append({
                'type': 'QUALITY_DECLINE',
                'severity': 'WARNING',
                'metric': 'Code Quality',
                'previous': prev_quality,
                'current': curr_quality,
                'change': round(curr_quality - prev_quality, 2),
                'message': f'Code quality declined from {prev_quality} to {curr_quality}',
                'action': 'Review recent changes and address style/complexity issues'
            })

        # Check complexity increase
        prev_complexity = previous.get('avg_complexity', 7.0)
        curr_complexity = current.get('avg_complexity', 7.0)
        if curr_complexity > prev_complexity + 1.0:
            alerts.append({
                'type': 'COMPLEXITY_INCREASE',
                'severity': 'WARNING',
                'metric': 'Complexity',
                'previous': prev_complexity,
                'current': curr_complexity,
                'change': round(curr_complexity - prev_complexity, 2),
                'message': f'Complexity increased from {prev_complexity:.1f} to {curr_complexity:.1f}',
                'action': 'Refactor complex functions before adding more logic'
            })

        # Check coverage drop
        prev_coverage = previous.get('test_coverage', 50.0)
        curr_coverage = current.get('test_coverage', 50.0)
        if curr_coverage < prev_coverage - 2.0:
            alerts.append({
                'type': 'COVERAGE_DROP',
                'severity': 'MEDIUM',
                'metric': 'Test Coverage',
                'previous': prev_coverage,
                'current': curr_coverage,
                'change': round(curr_coverage - prev_coverage, 2),
                'message': f'Test coverage dropped from {prev_coverage:.1f}% to {curr_coverage:.1f}%',
                'action': 'Add tests for new code before committing'
            })

        # Check new vulnerabilities
        prev_vulns = previous.get('dependency_vulnerabilities', 0)
        curr_vulns = current.get('dependency_vulnerabilities', 0)
        if curr_vulns > prev_vulns:
            alerts.append({
                'type': 'NEW_VULNERABILITIES',
                'severity': 'CRITICAL',
                'metric': 'Security',
                'previous': prev_vulns,
                'current': curr_vulns,
                'change': curr_vulns - prev_vulns,
                'message': f'Found {curr_vulns - prev_vulns} new vulnerabilities',
                'action': 'Update dependencies immediately to patch known vulnerabilities'
            })

        return alerts


class CodeDuplicationAnalyzer:
    """
    Analyze code duplication to identify copy-paste issues.

    Helps identify:
    - Repeated code blocks
    - Similar functions that should be refactored
    - Opportunities for code reuse
    """

    def __init__(self):
        pass

    def analyze_duplication(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a Python file for code duplication.

        Uses simple line-based comparison to find duplicated code blocks.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except (IOError, UnicodeDecodeError):
            return {'duplicated_lines': 0, 'duplication_percent': 0}

        # Simple duplication detection
        # This is a simplified version - real implementation would use AST analysis
        total_lines = len(lines)
        duplicated_count = self._count_duplicate_lines(lines)

        return {
            'file': file_path,
            'total_lines': total_lines,
            'duplicated_lines': duplicated_count,
            'duplication_percent': round((duplicated_count / total_lines * 100) if total_lines > 0 else 0, 2)
        }

    def _count_duplicate_lines(self, lines: List[str]) -> int:
        """Count lines that appear more than once"""
        # Remove whitespace and comments for comparison
        normalized = [l.strip() for l in lines if l.strip() and not l.strip().startswith('#')]

        duplicated = 0
        for i, line in enumerate(normalized):
            # Check if this line appears elsewhere
            if line and normalized.count(line) > 1:
                duplicated += 1

        return duplicated


# Example usage
if __name__ == '__main__':
    # Example metrics
    example_metrics = {
        'code_quality_score': 6.5,
        'avg_complexity': 8.2,
        'test_coverage': 72.5,
        'dependency_vulnerabilities': 1,
        'code_duplication_percent': 6.5
    }

    # Calculate debt index
    debt_calculator = TechnicalDebtIndex()
    debt_info = debt_calculator.calculate_debt_index(example_metrics)

    print("Technical Debt Index Report:")
    print(f"Total Debt Index: {debt_info['total_index']}/100 ({debt_info['severity']})")
    print("\nRecommendations:")
    for rec in debt_info['recommendations'][:3]:
        print(f"  [{rec['priority']}] {rec['area']}: {rec['action']}")
