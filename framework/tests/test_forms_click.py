import os
import sys
from behave import runner_util
from behave.runner_util import load_step_modules
from framework.utils.driver_factory import DriverFactory

def main():
    # Load step modules
    load_step_modules()

    # Run behave tests
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    runner = runner_util.Runtime()
    runner.configure()
    runner.run()

if __name__ == "__main__":
    DriverFactory.get_driver()
    main()