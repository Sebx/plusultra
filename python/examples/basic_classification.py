#!/usr/bin/env python3
"""
Basic example: Classify a support ticket.

Run from python/ directory:
    python examples/basic_classification.py
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import plusultra


def main():
    print("🚀 plusultra: Local Text Classification\n")

    # Load model (from ../model directory)
    agent = plusultra.load("../model", verify_hash=False)

    # Define a support ticket
    ticket = "I was charged twice for my subscription this month. Please refund the duplicate charge."

    print(f"📋 Ticket: {ticket}\n")

    # Define classification questions
    questions = {
        "department": {
            "type": "choice",
            "instructions": "Which team should handle this request?",
            "criteria": ["billing", "technical", "sales"]
        },
        "urgency": {
            "type": "score",
            "instructions": "How urgent is this request?",
            "criteria": ["not urgent", "soon", "critical"]
        },
        "is_refund": {
            "type": "noul",
            "instructions": "Does the customer request a refund?"
        }
    }

    # Run prediction
    print("🔍 Classifying...\n")
    result = agent.predict(ticket, questions)

    # Display results
    print("📊 Results:")
    for q_id, answer in result["answers"].items():
        latency = result["latencies_ms"][q_id]
        print(f"  {q_id:15} → {answer:20} ({latency:.1f}ms)")

    print(f"\n⏱️  Total time: {result['total_time_ms']:.1f}ms")
    print(f"📈 Model: {result['metadata']['model']}")
    print(f"   Tokens: {result['metadata']['tokens_used']}")


if __name__ == "__main__":
    main()
