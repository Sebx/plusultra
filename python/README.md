# plusultra: Python Native Runtime

Run the GLiClass classification model natively on your machine without any cloud APIs.

**Zero telemetry. Zero accounts. 100% local inference.**

```python
import plusultra

agent = plusultra.load("../model")
result = agent.predict(
    "I was billed twice for my subscription",
    {
        "department": {
            "type": "choice",
            "criteria": ["billing", "technical", "sales"]
        }
    }
)
print(result["answers"]["department"])  # → "billing"
```

---

## Quick Start

### 1. Install Dependencies

```bash
pip install onnxruntime transformers
```

### 2. Export Model to ONNX (if needed)

```bash
# From the model directory
python -m transformers.models.export onnx \
  --model-name-or-path knowledgator/gliclass-multilang-edge \
  --output model.onnx
```

Or use the pre-exported model if available.

### 3. Run Example

```bash
cd python/
python examples/basic_classification.py
```

Expected output:
```
📋 Ticket: I was charged twice for my subscription this month...

🔍 Classifying...

📊 Results:
  department        → billing               (145.2ms)
  urgency           → critical             (142.8ms)
  is_refund         → True                 (138.5ms)

⏱️  Total time: 426.5ms
```

---

## API Reference

### `load(model_dir, verify_hash=True)`

Load a plusultra model from disk.

**Args:**
- `model_dir` (str): Path to model directory (contains `.onnx`, `tokenizer.json`, `manifest.json`)
- `verify_hash` (bool): Verify SHA-256 hashes against manifest.json

**Returns:**
- `Agent`: Ready-to-use inference agent

**Example:**
```python
agent = plusultra.load("../model")
```

---

### `Agent.predict(state, questions, dtype="float32")`

Classify text and answer structured questions.

**Args:**
- `state` (str): Input text to classify
- `questions` (dict): Question definitions, each with:
  - `type`: "choice", "score", or "noul"
  - `instructions`: Question prompt
  - `criteria`: List of options (choice/score) or None (noul)
- `dtype` (str): "float32" or "float16"

**Returns:**
```python
{
    "answers": {"department": "billing", ...},
    "latencies_ms": {"department": 145.2, ...},
    "total_time_ms": 426.5,
    "metadata": {
        "model": "GLiClass Multilang Edge",
        "parameters": "143M",
        "tokens_used": 127
    }
}
```

**Example:**
```python
result = agent.predict(
    "I want to upgrade to pro",
    {
        "department": {
            "type": "choice",
            "instructions": "Which team?",
            "criteria": ["billing", "technical", "sales"]
        },
        "urgency": {
            "type": "score",
            "instructions": "How urgent?",
            "criteria": ["not urgent", "soon", "critical"]
        },
        "is_refund": {
            "type": "noul",
            "instructions": "Requesting refund?"
        }
    }
)

print(result["answers"]["department"])  # → "sales"
print(result["total_time_ms"])           # → 380.5
```

---

## Question Types

### 1. Choice (Multi-class Classification)

Select one option from a list.

```python
{
    "department": {
        "type": "choice",
        "instructions": "Which team should handle this?",
        "criteria": ["billing", "technical", "sales"]
    }
}
```

**Output:** String (one of the criteria)

---

### 2. Score (Ordinal Regression)

Rate on a numeric scale.

```python
{
    "urgency": {
        "type": "score",
        "instructions": "How urgent is this?",
        "criteria": ["not urgent", "soon", "critical"]
    }
}
```

**Output:** Float (0.0–2.0 for 3-level scale)

---

### 3. Noul (Yes/No with Nuance)

Binary classification with confidence.

```python
{
    "is_refund": {
        "type": "noul",
        "instructions": "Does customer request a refund?"
    }
}
```

**Output:** Boolean (True/False)

---

## Benchmarks

Run the benchmark suite:

```bash
python examples/benchmark.py
```

### Sample Results (M3 MacBook Pro)

| Metric | Value |
|--------|-------|
| Single query (p50) | 145–180 ms |
| Single query (p95) | 300–400 ms |
| 10-query throughput | 6–7 q/s |
| Memory (idle) | 2 MB |
| Memory (model loaded) | 350 MB |
| Memory (peak inference) | 420 MB |

---

## Comparison: plusultra-py vs laya-mlx

| Aspect | plusultra-py | laya-mlx | Winner |
|--------|--------------|----------|--------|
| Latency (p50) | 145–180 ms | 7–14 ms | 🏆 laya-mlx (10–25× faster) |
| Model size | 143M | 322–421M | 🏆 plusultra |
| Setup | `pip install` | `pip install` | 🏆 Tie |
| Dependencies | ONNX Runtime | MLX (Apple Silicon only) | 🏆 plusultra (more portable) |
| Accuracy | GLiClass (Multilang) | Laya (typed-decisions) | Different models |

**Context:** laya-mlx is optimized for production latency on Apple Silicon; plusultra-py prioritizes portability and ease of use.

---

## Installation from Source

```bash
cd python/
pip install -e .
```

This installs `plusultra` as a development package.

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'onnxruntime'`

Install ONNX Runtime:
```bash
pip install onnxruntime
```

Or with GPU support:
```bash
pip install onnxruntime-gpu
```

### `FileNotFoundError: model.onnx`

Export the model to ONNX format. See "Quick Start" → step 2.

### Slow Inference

- ONNX Runtime defaults to CPU. For GPU acceleration, install `onnxruntime-gpu`
- Close other applications to reduce system load
- Check that you're using release mode (not debug)

---

## Contributing

See [../CONTRIBUTING.md](../CONTRIBUTING.md) for how to contribute.

---

## License

MIT (see [../LICENSE](../LICENSE))

Model weights: Apache 2.0 (GLiClass, see [../licenses/](../licenses/))

---

**Questions?** Open an issue on [GitHub](https://github.com/Sebx/plusultra).
