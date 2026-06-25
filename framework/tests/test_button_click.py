import os
import sys
from behave import run_behave
from framework.utils.logger import get_logger

def main():
    logger = get_logger(__name__)
    try:
        run_behave()
        logger.info("Test execution completed successfully")
    except Exception as e:
        logger.error(f"Test execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()