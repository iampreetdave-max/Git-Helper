"""
Git-Buddy Global Logging Configuration
=====================================

Provides centralized logging setup for all analysis scripts.
Ensures transparency about what each script is doing.

Features:
- Consistent log format across all scripts
- Console + File logging
- Clear step-by-step execution visibility
- Error handling with context
- Performance tracking
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


class TransparentLogger:
    """
    Global logging configuration for Git-Buddy.

    Ensures all scripts log their operations transparently:
    - What they're doing
    - Why they're doing it
    - How long it takes
    - Any issues encountered
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TransparentLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if TransparentLogger._initialized:
            return

        self.logger = logging.getLogger('git-buddy')
        self.logger.setLevel(logging.DEBUG)

        # Create logs directory
        log_dir = Path('.github') / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)

        # Log file name with timestamp
        log_file = log_dir / f"git-buddy-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        # Log format: timestamp [LEVEL] script_name: message
        log_format = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

        # Console handler (INFO and above)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # File handler (DEBUG and above)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

        TransparentLogger._initialized = True

    def get_logger(self, script_name):
        """Get logger for a specific script"""
        return logging.getLogger(f'git-buddy.{script_name}')

    def log_step(self, logger, step_number, description, details=None):
        """
        Log a major step in the analysis process.

        Args:
            logger: logger instance
            step_number: Step number (1, 2, 3, etc.)
            description: What we're doing
            details: Optional additional info
        """
        message = f"[STEP {step_number}] {description}"
        if details:
            message += f" - {details}"
        logger.info("=" * 80)
        logger.info(message)
        logger.info("=" * 80)

    def log_result(self, logger, metric_name, value, status='OK'):
        """
        Log an analysis result.

        Args:
            logger: logger instance
            metric_name: Name of metric (e.g., 'Code Quality')
            value: The value/result
            status: OK, WARNING, ERROR
        """
        logger.info(f"✓ {metric_name}: {value} [{status}]")

    def log_warning(self, logger, issue, recommendation=None):
        """
        Log a potential issue.

        Args:
            logger: logger instance
            issue: What's wrong
            recommendation: Suggested fix
        """
        logger.warning(f"⚠ {issue}")
        if recommendation:
            logger.warning(f"  → Recommendation: {recommendation}")

    def log_error(self, logger, error, context=None):
        """
        Log an error with context.

        Args:
            logger: logger instance
            error: Error message
            context: What was happening when error occurred
        """
        if context:
            logger.error(f"✗ Error while {context}: {error}")
        else:
            logger.error(f"✗ {error}")

    def log_summary(self, logger, title, summary_dict):
        """
        Log a summary of results.

        Args:
            logger: logger instance
            title: Summary title
            summary_dict: Dictionary of results
        """
        logger.info("")
        logger.info("=" * 80)
        logger.info(f"SUMMARY: {title}")
        logger.info("=" * 80)
        for key, value in summary_dict.items():
            logger.info(f"  {key}: {value}")
        logger.info("=" * 80)


def get_transparent_logger(script_name):
    """
    Get a transparent logger for your script.

    Usage:
        logger = get_transparent_logger('analyzer')
        logger.info('Starting analysis...')

    Args:
        script_name: Name of your script (used in log messages)

    Returns:
        logging.Logger instance
    """
    transparent_logger = TransparentLogger()
    return transparent_logger.get_logger(script_name)


def log_execution(script_name, description):
    """
    Decorator to log script execution with timing.

    Usage:
        @log_execution('analyzer', 'Analyzing code quality')
        def analyze_code():
            ...
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            logger = get_transparent_logger(script_name)

            logger.info("")
            logger.info("=" * 80)
            logger.info(f"EXECUTION START: {description}")
            logger.info("=" * 80)

            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time

                logger.info("")
                logger.info("=" * 80)
                logger.info(f"EXECUTION COMPLETE: {description}")
                logger.info(f"Time elapsed: {elapsed:.2f} seconds")
                logger.info("=" * 80)

                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"✗ Execution failed after {elapsed:.2f} seconds")
                logger.error(f"Error: {str(e)}")
                raise

        return wrapper
    return decorator


# Example usage and documentation
if __name__ == '__main__':
    # This is just for reference - actual usage is in other scripts

    logger = get_transparent_logger('example')

    logger.info("This is how to use the transparent logging system:")
    logger.info("")
    logger.info("1. Import the logger:")
    logger.info("   from logging_config import get_transparent_logger")
    logger.info("")
    logger.info("2. Get a logger for your script:")
    logger.info("   logger = get_transparent_logger('my_script')")
    logger.info("")
    logger.info("3. Use it to log operations:")
    logger.info("   logger.info('Starting analysis...')")
    logger.info("   logger.warning('This is a warning')")
    logger.info("   logger.error('This is an error')")
    logger.info("")
    logger.info("All logs go to:")
    logger.info("   - Console (INFO and above)")
    logger.info("   - .github/logs/git-buddy-TIMESTAMP.log (DEBUG and above)")
