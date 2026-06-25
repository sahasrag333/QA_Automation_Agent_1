"""Entry point for AI QA Agent project.

This is a small starter that parses basic args and prints available agents.
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

def list_agents():
    agents_dir = PROJECT_ROOT / "agents"
    return [p.name for p in agents_dir.iterdir() if p.is_dir()]


def main():
    print("AI QA Agent starter")
    print("Project root:", PROJECT_ROOT)
    print("Detected agents:", list_agents())


if __name__ == "__main__":
    main()
