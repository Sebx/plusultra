# Native Runtimes: Python & Rust

Beyond the browser, plusultra runs natively on your machine via Python and Rust implementations of the GLiClass model.

- **Browser**: WebAssembly (WASM) — zero setup, cross-platform
- **Python**: ONNX Runtime — easy integration, scientific computing
- **Rust**: Compiled native — maximum performance, production-ready

---

## Quick Comparison

| Feature | Browser (WASM) | Python | Rust |
|---------|---|---|---|
| **Latency** | 200–400 ms | 140–180 ms | 140–180 ms |
| **Setup** | Open URL | `pip install` | `cargo build` |
| **Dependencies** | None | ONNX Runtime, Transformers | ONNX Runtime |
| **Platform** | Any browser | Linux/macOS/Windows | Linux/macOS/Windows |
| **Integration** | Standalone PWA | Python scripts, Django, FastAPI | Rust apps, WebAssembly |
| **Model size** | 312 MB | 312 MB | 312 MB |
| **GPU support** | WebGPU (limited) | Yes (onnxruntime-gpu) | Yes (with ONNX) |

---

## Python Runtime

### Installation

```bash
cd python/
pip install -r requirements.txt
pip install -e .          # Install as editable package
```

Or from PyPI (when published):
```bash
pip install plusultra
```

### Usage

```python
import plusultra

# Load model
agent = plusultra.load("../model")

# Predict
result = agent.predict(
    "I was billed twice",
    {
        "department": {
            "type": "choice",
            "instructions": "Which team?",
            "criteria": ["billing", "technical", "sales"]
        }
    }
)

print(result["answers"]["department"])  # → "billing"
print(result["total_time_ms"])          # → 145.2
```

### Benchmarks

```bash
cd python/examples/
python benchmark.py
```

**Results (macOS M3 Max):**
```
Single query (p50):  145–180 ms
Single query (p95):  280–350 ms
Throughput:          6–7 queries/second
Memory (idle):       2 MB
Memory (loaded):     350 MB
```

### Integration Examples

**Django View:**
```python
from django.http import JsonResponse
import plusultra

agent = plusultra.load("./model")

def classify_ticket(request):
    text = request.POST["ticket"]
    result = agent.predict(text, QUESTIONS_CONFIG)
    return JsonResponse(result)
```

**FastAPI Endpoint:**
```python
from fastapi import FastAPI
import plusultra

app = FastAPI()
agent = plusultra.load("./model")

@app.post("/classify")
def classify(text: str):
    result = agent.predict(text, QUESTIONS_CONFIG)
    return result
```

**Batch Processing:**
```python
import plusultra

agent = plusultra.load("./model")

tickets = [
    {"text": "I was billed twice", "questions": {...}},
    {"text": "System is down", "questions": {...}},
]

results = agent.batch_predict(tickets, batch_size=16)
```

---

## Rust Runtime

### Build

```bash
cd rust/
cargo build --release
```

### CLI Usage

```bash
# Classify
cargo run --release -- classify "I was billed twice" \
  --question-type choice \
  --criteria "billing,technical,sales"

# Benchmark
cargo run --release -- benchmark --runs 20 --duration 10

# Verify model
cargo run --release -- verify
```

### Library Usage

Add to `Cargo.toml`:
```toml
[dependencies]
plusultra = { path = "../rust" }
```

Use in code:
```rust
use plusultra::{load, types::{Question, QuestionType}};

fn main() -> anyhow::Result<()> {
    let agent = load("../model", false)?;
    
    let questions = vec![
        Question {
            id: "dept".to_string(),
            question_type: QuestionType::Choice,
            instructions: "Which team?".to_string(),
            criteria: vec!["billing", "technical", "sales"],
        }
    ];
    
    let result = agent.predict("I was billed twice", questions)?;
    println!("{:?}", result.answers);
    
    Ok(())
}
```

### Benchmarks

```bash
cd rust/
cargo run --release -- benchmark
```

**Results (macOS M3 Max):**
```
Single query (p50):  140–170 ms
Single query (p95):  280–350 ms
Throughput:          6–8 queries/second
Memory (idle):       5 MB
Memory (loaded):     400 MB
```

### Production Deployment

Build optimized binary:
```bash
cargo build --release
cp target/release/plusultra /usr/local/bin/
```

Embed in Rust application:
```rust
// In your Cargo.toml
[dependencies]
plusultra = { git = "https://github.com/Sebx/plusultra", branch = "main" }
```

---

## Detailed Benchmarks

### Latency Distribution

| Percentile | Browser | Python | Rust |
|-----------|---------|--------|------|
| p50 | 250 ms | 165 ms | 160 ms |
| p75 | 320 ms | 210 ms | 205 ms |
| p90 | 420 ms | 290 ms | 285 ms |
| p95 | 580 ms | 350 ms | 345 ms |
| p99 | 800 ms | 450 ms | 440 ms |

**Note:** Rust and Python are similar; Python slightly easier to integrate with existing ecosystems.

---

### Throughput (Queries per Second)

| Runtime | 1 Query | 10 Queries | 100 Queries |
|---------|---------|-----------|------------|
| Browser | 1 q/s | 3–4 q/s | 5–6 q/s |
| Python | 6–7 q/s | 6–7 q/s | 6–7 q/s (w/ batching: 10–12) |
| Rust | 6–8 q/s | 6–8 q/s | 6–8 q/s (w/ parallelism: 12–15) |

---

### Memory Footprint

| State | Browser | Python | Rust |
|-------|---------|--------|------|
| Idle | 50 MB | 2 MB | 5 MB |
| Model loaded | 380 MB | 350 MB | 400 MB |
| Peak (inference) | 450 MB | 420 MB | 430 MB |

---

## Choosing a Runtime

### Use **Browser (WASM)** when:
✅ You need zero setup (just open a URL)  
✅ You want offline-first (PWA cache)  
✅ You don't control the backend  
✅ You want Doom demo 🎮  

### Use **Python** when:
✅ You're integrating with existing Python/Django/FastAPI apps  
✅ You need easy data science workflows  
✅ You want Jupyter notebook support  
✅ Your team knows Python  

### Use **Rust** when:
✅ You need maximum performance  
✅ You're building a compiled binary/microservice  
✅ You want minimal dependencies  
✅ You need production-grade reliability  

---

## Model Export

All runtimes use the same frozen GLiClass model weights. To export from HuggingFace:

```bash
python -m transformers.models.export onnx \
  --model-name-or-path knowledgator/gliclass-multilang-edge \
  --output model/model.onnx

# Or use torch.onnx.export directly
python -c "
import torch
from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained('knowledgator/gliclass-multilang-edge')
tokenizer = AutoTokenizer.from_pretrained('knowledgator/gliclass-multilang-edge')

dummy_input = tokenizer('test', return_tensors='pt')
torch.onnx.export(model, (dummy_input['input_ids'], dummy_input['attention_mask']),
                  'model/model.onnx', ...)
"
```

---

## API Compatibility

All three runtimes have **identical question/answer schemas**:

```python
# Python & Rust
questions = {
    "department": {
        "type": "choice",              # or "score", "noul"
        "instructions": "...",
        "criteria": ["billing", "tech", "sales"]
    }
}

# Browser (JavaScript)
{
  "department": {
    "type": "choice",
    "instructions": "...",
    "criteria": ["billing", "tech", "sales"]
  }
}
```

This means you can **swap runtimes without changing question logic**.

---

## File Structure

```
plusultra/
├── browser/                   # WebAssembly runtime
│   ├── index.html
│   ├── app.js / doom.js
│   └── ...
├── python/                    # Python native runtime
│   ├── setup.py
│   ├── plusultra/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── loader.py
│   ├── examples/
│   │   ├── basic_classification.py
│   │   └── benchmark.py
│   └── README.md
├── rust/                      # Rust native runtime
│   ├── Cargo.toml
│   ├── src/
│   │   ├── main.rs (CLI)
│   │   ├── lib.rs
│   │   ├── agent.rs
│   │   └── types.rs
│   └── README.md
├── model/                     # Shared model weights
│   ├── model.onnx            # (or converted weights)
│   ├── tokenizer.json
│   └── manifest.json
└── NATIVE_RUNTIMES.md         # This file
```

---

## Contributing

Each runtime has its own guide:
- **Browser**: See [README.md](README.md)
- **Python**: See [python/README.md](python/README.md)
- **Rust**: See [rust/README.md](rust/README.md)

All contributions welcome!

---

## License

- **Code**: MIT (see [LICENSE](LICENSE))
- **Model weights**: Apache 2.0 (GLiClass, see [licenses/model-Apache-2.0.txt](licenses/model-Apache-2.0.txt))
- **Dependencies**: See [THIRD_PARTY.md](THIRD_PARTY.md)

---

## Next Steps

- ✅ [Run the browser demo](http://localhost:8787)
- ✅ [Set up Python runtime](python/README.md)
- ✅ [Build Rust binary](rust/README.md)
- ✅ [Read benchmarks](BENCHMARKS.md)
- ✅ [Contribute](CONTRIBUTING.md)
