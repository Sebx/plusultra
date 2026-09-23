"""
plusultra: Local text classification engine

Run the GLiClass model natively on your machine without cloud APIs.
No servers. No accounts. No telemetry.

Example:
    import plusultra

    agent = plusultra.load("../model")
    result = agent.predict(
        "I was billed twice for my subscription",
        {
            "department": {
                "type": "choice",
                "instructions": "Which team should handle this?",
                "criteria": ["billing", "technical", "sales"]
            }
        }
    )
    print(result["answers"]["department"])  # → "billing"
"""

__version__ = "0.1.0"
__author__ = "plusultra contributors"

from .agent import Agent
from .loader import load

__all__ = ["Agent", "load"]
