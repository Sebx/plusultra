# plusultra: Rust Native Runtime

High-performance local text classification in Rust. Run the GLiClass model directly without servers or APIs.

**Zero telemetry. Zero accounts. 100% local inference.**

```rust
use plusultra::{load, types::Question, types::QuestionType};

let agent = load("../model", false)?;
let questions = vec![
    Question {
        id: "department".to_string(),
        question_type: QuestionType::Choice,
        instructions: "Which team?".to_string(),
        criteria: vec!["billing", "technical", "sales"],
    }
];

let result = agent.predict("I was billed twice", questions)?;
println!("{:?}", result.answers);  // {"department": "billing"}
```

---

## Quick Start

### 1. Build

```bash
cd rust/
cargo build --release
```

### 2. Run CLI

```bash
# Classify text
cargo run --release -- classify "I was billed twice" \
  --question-type choice \
  --criteria "billing,technical,sales"

# Run benchmarks
cargo run --release -- benchmark --runs 10 --duration 10

# Verify model
cargo run --release -- verify
```

### 3. Use as Library

Add to `Cargo.toml`:

```toml
[dependencies]
plusultra = { path = "../rust" }
```

Then in your code:

```rust
use plusultra::{load, types::Question, types::QuestionType};

fn main() -> anyhow::Result<()> {
    let agent = load("../model", false)?;
    let questions = vec![/* ... */];
    let result = agent.predict("Your text here", questions)?;
    Ok(())
}
```

---

## API Reference

### `load(model_dir: &str, verify_hash: bool) -> Result<Agent>`

Load a plusultra model from disk.

**Arguments:**
- `model_dir` (str): Path to model directory
- `verify_hash` (bool): Verify SHA-256 hashes against manifest.json

**Returns:**
- `Agent`: Ready-to-use inference agent

**Example:**
```rust
let agent = load("../model", true)?;
```

---

### `Agent::predict(state: &str, questions: Vec<Question>) -> Result<PredictionResult>`

Classify text and answer structured questions.

**Arguments:**
- `state` (str): Input text to classify
- `questions` (Vec<Question>): Question definitions

**Returns:**
```rust
PredictionResult {
    answers: HashMap<String, Answer>,
    latencies_ms: HashMap<String, f32>,
    total_time_ms: f32,
    metadata: Metadata,
}
```

**Example:**
```rust
let result = agent.predict("I want a refund", vec![
    Question {
        id: "is_refund".to_string(),
        question_type: QuestionType::Noul,
        instructions: "Does customer request refund?".to_string(),
        criteria: vec![],
    }
])?;

println!("{:?}", result.answers["is_refund"]);  // Boolean(true)
```

---

## Question Types

### 1. Choice (Multi-class Classification)

```rust
Question {
    id: "department".to_string(),
    question_type: QuestionType::Choice,
    instructions: "Which team should handle this?".to_string(),
    criteria: vec!["billing", "technical", "sales"],
}
```

**Output:** `Answer::Choice(String)`

---

### 2. Score (Ordinal Regression)

```rust
Question {
    id: "urgency".to_string(),
    question_type: QuestionType::Score,
    instructions: "How urgent is this?".to_string(),
    criteria: vec!["not urgent", "soon", "critical"],
}
```

**Output:** `Answer::Score(f32)`

---

### 3. Noul (Yes/No with Nuance)

```rust
Question {
    id: "is_refund".to_string(),
    question_type: QuestionType::Noul,
    instructions: "Does customer request a refund?".to_string(),
    criteria: vec![],  // Empty for noul
}
```

**Output:** `Answer::Boolean(bool)`

---

## Benchmarks

Run the benchmark suite:

```bash
cargo run --release -- benchmark --runs 10 --duration 10
```

### Expected Results (M1/M2/M3 MacBook)

| Metric | Value |
|--------|-------|
| Single query (p50) | 140–180 ms |
| Single query (p95) | 280–350 ms |
| Throughput | 6–8 q/s |
| Memory (idle) | ~5 MB |
| Memory (model loaded) | ~400 MB |

**Note:** Latency varies by system load and tokenization complexity. These are representative values.

---

## Comparison: plusultra-rs vs laya-mlx

| Aspect | plusultra-rs | laya-mlx | Winner |
|--------|--------------|----------|--------|
| Latency | 140–180 ms | 7–14 ms | 🏆 laya-mlx (10–25× faster) |
| Language | Rust (compiled) | Python | 🏆 plusultra-rs (faster startup) |
| Setup | `cargo build` | `pip install` | 🏆 laya-mlx (easier) |
| Portability | Linux/macOS/Windows | Apple Silicon only | 🏆 plusultra-rs (universal) |
| Model size | 143M | 322–421M | 🏆 plusultra |

---

## CLI Usage

### Classify Command

```bash
cargo run --release -- classify "Your text here" \
  --question-type choice \
  --criteria "option1,option2,option3"
```

**Options:**
- `--question-type` (choice|score|noul): Type of question
- `--criteria`: Comma-separated list of options
- `--model-dir`: Path to model directory (default: ../model)

### Benchmark Command

```bash
cargo run --release -- benchmark --runs 20 --duration 15
```

**Options:**
- `--runs`: Number of latency measurement runs
- `--duration`: Throughput test duration in seconds
- `--model-dir`: Path to model directory

### Verify Command

```bash
cargo run --release -- verify
```

Verifies model integrity by checking:
- Directory structure
- Required files (model.onnx, tokenizer.json)
- SHA-256 hashes (if manifest.json present)

---

## Building for Release

For maximum performance:

```bash
cargo build --release

# Run optimized binary
./target/release/plusultra classify "text" --criteria "a,b,c"
```

Release build features:
- Link-time optimization (LTO)
- Single codegen unit (maximum optimization)
- Level 3 optimizations

---

## Project Structure

```
rust/
├── Cargo.toml                 # Dependencies and build config
├── src/
│   ├── main.rs               # CLI entry point
│   ├── lib.rs                # Library root
│   ├── agent.rs              # Inference agent
│   ├── loader.rs             # Model loading + verification
│   └── types.rs              # Type definitions
└── README.md                 # This file
```

---

## Troubleshooting

### `error: failed to resolve: use of undeclared type`

Make sure you have all dependencies:
```bash
cargo check
```

### Slow inference

- Build in release mode: `cargo build --release`
- Close other applications
- Check CPU temperature (thermal throttling)

### Model not found

Ensure the model directory exists and contains:
- `model.onnx` (or similar .onnx file)
- `tokenizer.json`
- `manifest.json` (optional, for integrity verification)

---

## Contributing

See [../CONTRIBUTING.md](../CONTRIBUTING.md) for how to contribute.

---

## License

MIT (see [../LICENSE](../LICENSE))

Model weights: Apache 2.0 (GLiClass, see [../licenses/](../licenses/))

---

**Questions?** Open an issue on [GitHub](https://github.com/Sebx/plusultra).
