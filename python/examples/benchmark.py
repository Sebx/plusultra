#!/usr/bin/env python3
"""
Benchmark: Measure plusultra inference latency.

Run from python/ directory:
    python examples/benchmark.py
"""

import sys
import time
import json
from pathlib import Path
from typing import List, Dict

sys.path.insert(0, str(Path(__file__).parent.parent))

import plusultra


TEST_CASES = [
    {
        "name": "Billing (short)",
        "text": "I was billed twice.",
        "questions": {
            "department": {
                "type": "choice",
                "instructions": "Which team?",
                "criteria": ["billing", "technical", "sales"]
            }
        }
    },
    {
        "name": "Outage (medium)",
        "text": "System is completely down and we cannot process orders. This is urgent.",
        "questions": {
            "urgency": {
                "type": "score",
                "instructions": "How urgent?",
                "criteria": ["not urgent", "soon", "critical"]
            }
        }
    },
    {
        "name": "Refund (long)",
        "text": "I purchased a subscription last month but the product doesn't work as advertised. I would like a refund because I'm not satisfied with the service.",
        "questions": {
            "is_refund": {
                "type": "noul",
                "instructions": "Does customer request refund?"
            }
        }
    },
]


def benchmark_single(agent, num_runs: int = 10) -> Dict:
    """Benchmark single predictions."""
    results = {
        "num_runs": num_runs,
        "test_cases": {}
    }

    for test in TEST_CASES:
        latencies = []

        for i in range(num_runs):
            result = agent.predict(test["text"], test["questions"])
            latencies.append(result["total_time_ms"])

        latencies_sorted = sorted(latencies)

        results["test_cases"][test["name"]] = {
            "p50_ms": latencies_sorted[len(latencies) // 2],
            "p95_ms": latencies_sorted[int(len(latencies) * 0.95)],
            "p99_ms": latencies_sorted[int(len(latencies) * 0.99)],
            "mean_ms": sum(latencies) / len(latencies),
            "min_ms": min(latencies),
            "max_ms": max(latencies),
            "samples": latencies
        }

    return results


def benchmark_throughput(agent, duration_sec: int = 10) -> Dict:
    """Benchmark queries per second."""
    query = TEST_CASES[0]  # Use first test case

    count = 0
    start = time.perf_counter()

    while time.perf_counter() - start < duration_sec:
        agent.predict(query["text"], query["questions"])
        count += 1

    elapsed = time.perf_counter() - start
    qps = count / elapsed

    return {
        "duration_sec": elapsed,
        "queries": count,
        "queries_per_second": qps,
        "ms_per_query": 1000.0 / qps
    }


def main():
    print("🏃 plusultra Benchmark Suite\n")
    print("=" * 60)

    # Load model
    print("\n📦 Loading model...")
    try:
        agent = plusultra.load("../model", verify_hash=False)
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("\n💡 Make sure you have:")
        print("   1. ONNX Runtime: pip install onnxruntime")
        print("   2. Transformers: pip install transformers")
        print("   3. Model in ../model/ directory")
        return

    print("✓ Model loaded\n")

    # Benchmark 1: Latency
    print("📊 Benchmark 1: Latency (10 runs per test case)")
    print("-" * 60)
    latency_results = benchmark_single(agent, num_runs=10)

    for name, stats in latency_results["test_cases"].items():
        print(f"\n{name}:")
        print(f"  p50:  {stats['p50_ms']:.1f}ms")
        print(f"  p95:  {stats['p95_ms']:.1f}ms")
        print(f"  p99:  {stats['p99_ms']:.1f}ms")
        print(f"  mean: {stats['mean_ms']:.1f}ms")
        print(f"  min:  {stats['min_ms']:.1f}ms, max: {stats['max_ms']:.1f}ms")

    # Benchmark 2: Throughput
    print("\n\n📈 Benchmark 2: Throughput (10-second run)")
    print("-" * 60)
    throughput = benchmark_throughput(agent, duration_sec=10)

    print(f"Duration:     {throughput['duration_sec']:.1f}s")
    print(f"Queries:      {throughput['queries']}")
    print(f"Throughput:   {throughput['queries_per_second']:.2f} q/s")
    print(f"Per query:    {throughput['ms_per_query']:.1f}ms")

    # Save results
    print("\n\n💾 Saving results...")
    output = {
        "latency": latency_results,
        "throughput": throughput
    }

    with open("benchmark_results.json", "w") as f:
        json.dump(output, f, indent=2, default=str)

    print("✓ Results saved to benchmark_results.json")
    print("\n" + "=" * 60)
    print("✅ Benchmark complete!")


if __name__ == "__main__":
    main()
