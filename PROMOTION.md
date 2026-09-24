# Promotion Content (Copy-Paste Ready)

Ready-to-use content for social media, blogs, and communities.

---

## 🐦 Twitter Thread

**Post 1:**
```
🚀 Introducing plusultra: text classification that never leaves your machine.

Most AI tools send your data to the cloud. We said no.

✅ 140ms latency
✅ 100% local inference
✅ Works offline
✅ Browser + Python + Rust
✅ Open source (MIT)

github.com/Sebx/plusultra

#MachineLearning #Privacy #OpenSource
```

**Post 2:**
```
The problem: Cloud APIs cost money and leak data.

- AWS Comprehend: $1,200/month for 1M requests
- Privacy risk: Your text goes to their servers
- Latency: 500ms–5s waiting for response

What if you could classify text locally in 140ms for free?
```

**Post 3:**
```
plusultra runs the GLiClass model (143M params) locally:

🌐 Browser → WebAssembly (WASM)
🐍 Python → ONNX Runtime  
🦀 Rust → Native binary

Same model. Same API. Pick your runtime.

Choose based on where you need it:
- Website? Browser.
- Django app? Python.
- Microservice? Rust.
```

**Post 4:**
```
Proof it works: We built an AI that plays Doom by reading game sensors (not pixels).

The same model that classifies text also handles real-time decision-making in a video game.

4–5 FPS. 0 API calls. 0 latency excuses.

Watch: [link to video or doom.html]
```

**Post 5:**
```
Compare to laya-mlx (which we love):

laya-mlx: 7–14ms, Apple Silicon only, Python
plusultra: 140–180ms, Linux/Mac/Windows, Browser/Python/Rust

Different tradeoffs. Same mission: local inference.

Both beat cloud. Both respect privacy.
```

**Post 6:**
```
Three ways to use plusultra right now:

1. Open a URL (browser)
2. pip install + Python
3. cargo build + Rust CLI

Benchmark it. Integrate it. Deploy it.

Full docs: github.com/Sebx/plusultra

Open source. MIT licensed. Zero tracking.
```

---

## ✍️ Dev.to Article Draft

**Title:** "Local Text Classification Without Cloud APIs: Building plusultra"

```markdown
# Local Text Classification Without Cloud APIs: Building plusultra

## TL;DR

Cloud APIs are expensive and leak data. We built plusultra: a text classifier that runs 100% locally on your machine.

- **140–180ms latency** (p50)
- **$0 cost** (no API calls)
- **3 runtimes**: Browser, Python, Rust
- **100% open source** (MIT)

[GitHub](https://github.com/Sebx/plusultra) · [Live Demo](http://localhost:8787) · [Benchmarks](https://github.com/Sebx/plusultra/blob/master/BENCHMARKS.md)

---

## The Problem: Cloud Text Classification Is Expensive & Risky

When you use AWS Comprehend, Hugging Face Inference API, or Google Cloud Natural Language:

1. **Your text is sent to their servers** (privacy risk)
2. **You pay per request** ($1,200/month for 1M queries)
3. **You depend on network latency** (500ms–5s)
4. **You're locked into their model** (can't customize)

Example cost: Running a support ticket classifier on 1M tickets/month costs you ~$1,200 in API fees alone.

What if you could do it for free, offline, on your own hardware?

---

## The Solution: Local Inference with plusultra

plusultra runs the **GLiClass Multilang Edge model** (143M parameters) directly on your machine using:

- **Browser** (WebAssembly) — Zero setup
- **Python** (ONNX Runtime) — Easy integration
- **Rust** (Native binary) — Production deployment

All three use the **same model**, same API, same accuracy. Pick the runtime that fits your use case.

### Performance

| Metric | Value |
|--------|-------|
| p50 latency | 140–180 ms |
| p95 latency | 280–350 ms |
| Throughput | 6–8 queries/sec |
| Memory | 350 MB (model) + 420 MB (peak) |
| Privacy | ✅ 100% local |
| Cost | $0 |

---

## Three Ways to Use It

### 1. Browser (Easiest)

```bash
git clone https://github.com/Sebx/plusultra
cd plusultra
bash start-mac.sh  # or start-windows.cmd
```

Open http://localhost:8787 → Click "Load local engine" → Works offline.

### 2. Python (Best for Integration)

```python
pip install onnxruntime transformers

import plusultra

agent = plusultra.load("./model")
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

### 3. Rust (Production)

```bash
cd rust/
cargo build --release
./target/release/plusultra classify "Your text" \
  --criteria "billing,technical,sales"
```

---

## How It Works

### Architecture

```
Input Text → Tokenizer → GLiClass Model → Decision Head → Answer
   ↓
SHA-256 Verified Weights (312 MB)
   ↓
ONNX Runtime (WASM / CPU / GPU)
```

The model processes text through:
1. **Tokenization** (HuggingFace Rust tokenizer)
2. **Encoder** (GLiClass backbone)
3. **Decision heads** (choice/score/noul)
4. **Calibration** (temperature scaling)

All on **your machine**. Nothing leaves.

### Proof It Works: Doom Demo

To validate that the model can handle real-time decision-making, we trained a policy head and hooked it up to Chocolate Doom.

The AI:
- Reads game sensors (enemy distance, health, ammo)
- Makes 4 decisions/second via GLiClass
- Plays the game autonomously
- Never generates text (just decisions)

[Watch it play](http://localhost:8787/doom.html)

---

## Benchmarks & Comparison

### vs Cloud APIs

| Scenario | AWS Comprehend | plusultra |
|----------|---|---|
| 1M requests/month | $1,200 | $0 |
| Setup time | 20 min (API keys) | 2 min (clone) |
| Privacy | ⚠️ Cloud | ✅ Local |
| Latency | 1–5s | 140–180ms |
| Offline | ❌ No | ✅ Yes |

**Cost savings**: $1,200/month per 1M requests.

### vs laya-mlx

We love laya-mlx (10–25× faster). Here's where each shines:

| Feature | laya-mlx | plusultra |
|---------|---|---|
| Latency | 7–14 ms | 140–180 ms |
| Platform | Apple Silicon only | Linux/Mac/Windows |
| Setup | `pip install` | `pip install` or browser |
| Browser support | No | ✅ Yes |
| Open model | No | ✅ Yes (Apache 2.0) |

Both are fast, private, and open. Different tradeoffs for different needs.

---

## Benchmarks in Detail

### Latency Percentiles (macOS M3)

- **p50**: 165 ms
- **p95**: 350 ms
- **p99**: 450 ms

Includes: tokenization + inference + post-processing.

### Throughput

- **Single query**: 140–180 ms
- **10 queries**: 1.4–1.8 seconds
- **Sustained**: 6–7 queries/second

### Memory

- Idle: 2 MB
- Model loaded: 350 MB
- Peak inference: 420 MB

See [full benchmarks](https://github.com/Sebx/plusultra/blob/master/BENCHMARKS.md).

---

## Use Cases

### 1. Support Ticket Routing

Classify incoming tickets to the right team:

```python
tickets = load_csv("support_tickets.csv")
for ticket in tickets:
    result = agent.predict(ticket.text, QUESTIONS)
    route_to(result["answers"]["department"])
```

Save $1,200/month vs AWS Comprehend.

### 2. Content Moderation

Classify user-generated content without sending it to a 3rd party:

```python
def moderate(user_message):
    result = agent.predict(user_message, {
        "spam": {"type": "choice", "criteria": ["yes", "no"]},
        "toxicity": {"type": "score", "criteria": ["clean", "mild", "toxic"]}
    })
    return result
```

### 3. Real-Time Analytics Dashboard

Run on edge devices, analyze locally, keep user data private.

### 4. Offline Web Apps

Progressive Web App (PWA) that works completely offline:

- Load model once (312 MB)
- Cache in browser
- Classify unlimited text
- No internet required

---

## Getting Started

### Installation

```bash
# Option 1: Browser (no installation)
git clone https://github.com/Sebx/plusultra
bash start-mac.sh

# Option 2: Python
pip install onnxruntime transformers
cd python && pip install -e .

# Option 3: Rust
cd rust && cargo build --release
```

### First Classification

```python
import plusultra

agent = plusultra.load("./model")
result = agent.predict("I want a refund", {
    "is_refund": {
        "type": "noul",
        "instructions": "Does customer request refund?"
    }
})
print(result["answers"]["is_refund"])  # → True
```

### Try the Doom Demo

Open http://localhost:8787/doom.html → Click **Prepare Doom + AI** → See it play in real-time.

---

## FAQ

**Q: Is this as accurate as cloud APIs?**  
A: Yes. Same model (GLiClass), same weights. The difference is where it runs (local vs cloud).

**Q: Can I fine-tune the model?**  
A: Not yet. The model is frozen for this release. We're exploring fine-tuning in a future update.

**Q: Does it work on mobile?**  
A: Browser version works on modern phones (WebAssembly support required). Python/Rust versions need a desktop.

**Q: How large is the model?**  
A: 312 MB total (split into 50 MB chunks for browser caching). Downloads once, cached forever.

**Q: Can I use this in production?**  
A: Yes! The Rust runtime is production-ready. Python is also stable. Browser is a demo/PWA.

---

## Next Steps

- ⭐ Star us on [GitHub](https://github.com/Sebx/plusultra)
- 📖 Read the [full docs](https://github.com/Sebx/plusultra/blob/master/README.md)
- 🏃 Run the [benchmark](https://github.com/Sebx/plusultra/blob/master/BENCHMARKS.md)
- 🦀 Try the [Rust CLI](https://github.com/Sebx/plusultra/tree/master/rust)
- 🐍 Integrate with [Python](https://github.com/Sebx/plusultra/tree/master/python)

---

## Contributions Welcome

- Issues: [GitHub Issues](https://github.com/Sebx/plusultra/issues)
- PRs: See [CONTRIBUTING.md](https://github.com/Sebx/plusultra/blob/master/CONTRIBUTING.md)
- Security: See [SECURITY.md](https://github.com/Sebx/plusultra/blob/master/SECURITY.md)

---

MIT licensed. Open source. No telemetry.
```

---

## 📰 HackerNews "Show HN"

**Title:** `Show HN: plusultra — Local text classification (140ms) without cloud APIs`

```
Inspired by laya-mlx (which we love), we built plusultra: a text classifier
that runs 100% locally in the browser, Python, or Rust.

Why local inference?
- No API costs ($1,200/month → $0)
- No privacy leaks (everything local)
- Works offline (cache once, use forever)
- 140–180ms latency (p50)

Three ways to use it:
1. Browser: Open URL → click "Load local engine" → offline PWA
2. Python: pip install → integrate with Django/FastAPI
3. Rust: cargo build → production CLI/microservice

Proof it works: We trained a policy head and hooked the model to Doom.
It reads game sensors and plays autonomously. Same model, real-time decisions.
[video/gif of Doom]

All on the same frozen GLiClass model (143M params). Same API across runtimes.
Pick whichever fits your use case.

Benchmarks: https://github.com/Sebx/plusultra/blob/master/BENCHMARKS.md
GitHub: https://github.com/Sebx/plusultra

Inspired by laya-mlx and made with ❤️ for privacy-first ML.
```

---

## 📱 Reddit Posts

### r/MachineLearning

```
Title: [R] plusultra: Local text classification without cloud APIs (140ms p50)

plusultra is a text classifier that runs 100% locally—no cloud APIs, no privacy
leaks, no monthly bills.

We built this to show that modern classification models don't need cloud
backends. Same frozen GLiClass model, three runtimes:

🌐 Browser (WASM) — Zero setup
🐍 Python (ONNX) — Easy integration
🦀 Rust — Production

Key stats:
- 140–180ms latency (p50)
- 143M parameters
- Works offline
- MIT open source

Proof of concept: We trained a policy head and connected it to Doom.
It reads sensors and plays the game autonomously in real-time.

Benchmarks: https://github.com/Sebx/plusultra/blob/master/BENCHMARKS.md
GitHub: https://github.com/Sebx/plusultra

Inspired by laya-mlx. Would love feedback from this community!
```

### r/LocalLLMs

```
Title: plusultra: Local text classification in the browser, Python, or Rust

For those building offline-first or privacy-respecting applications:

plusultra runs GLiClass (143M text classifier) locally. No external APIs.

- Browser PWA: Works offline after first load
- Python: Integrate with Django/FastAPI/notebooks
- Rust: Production-ready CLI and library

140–180ms latency. Zero cost. Zero privacy risk.

Currently in early release (v0.1), but fully functional with comprehensive
benchmarks and three working runtimes.

GitHub: https://github.com/Sebx/plusultra

Happy to answer questions about local inference, WASM, or ONNX Runtime!
```

### r/rust

```
Title: plusultra-rs: Native Rust runtime for local text classification

Released the Rust version of plusultra today.

CLI:
```bash
plusultra classify "I want a refund" --criteria "billing,tech,sales"
```

Latency: 140–180ms
Library usage: ONNX Runtime + tokenizers crate

Why Rust?
- Compiled binary (single-file deployment)
- Zero runtime dependencies (vs Python)
- Production-ready

Also available in Python and browser (WASM).

GitHub: https://github.com/Sebx/plusultra/tree/master/rust
Benchmarks: https://github.com/Sebx/plusultra/blob/master/BENCHMARKS.md

Open source (MIT). Inspired by laya-mlx. Looking for Rust-specific feedback!
```

### r/Python

```
Title: plusultra: Python library for local text classification

Just released the Python version of plusultra.

```python
import plusultra

agent = plusultra.load("./model")
result = agent.predict(
    "I was billed twice",
    {"department": {"type": "choice", "criteria": ["billing", "tech", "sales"]}}
)
print(result["answers"]["department"])  # "billing"
```

Features:
- ONNX Runtime for fast inference
- SHA-256 model verification
- Batch prediction support
- Full integration with Django/FastAPI

Also available as a standalone browser app or Rust CLI.

GitHub: https://github.com/Sebx/plusultra/tree/master/python
Benchmarks: https://github.com/Sebx/plusultra/blob/master/BENCHMARKS.md

Open source (MIT). Feedback welcome!
```

---

## 📊 Cost Comparison Infographic (Markdown)

```markdown
# Cost of Classifying 1 Million Support Tickets

## Cloud API (AWS Comprehend)
💰 **$1,200 / month**
- Standard pricing: $0.0001 per unit
- 1M queries = 1M units
- Monthly: 1,000,000 × $0.0001 = $1,200
- Data sent to AWS servers ⚠️

## plusultra (Local)
💰 **$0 / month**
- No API calls
- One-time model download: 312 MB
- Everything runs locally
- Completely offline after first download ✅

---

## Break-Even Analysis

| Volume | Cloud Cost | plusultra | Savings |
|--------|-----------|-----------|---------|
| 100K/month | $120 | $0 | $120 |
| 1M/month | $1,200 | $0 | $1,200 |
| 10M/month | $12,000 | $0 | $12,000 |
| **Annual (1M/month)** | **$14,400** | **$0** | **$14,400** |

---

## Hidden Costs Avoided

❌ Privacy breach if API compromised  
❌ Data residency / compliance issues  
❌ Vendor lock-in  
❌ Rate limits & throttling  
❌ Latency (500ms–5s vs 140ms local)  

plusultra avoids all of these.

---

## The Math

**Cloud APIs:** Pay per request forever
**plusultra:** Free forever after download

→ At scale, local always wins.
```

---

## Usage Tips

1. **Twitter**: Copy each post separately. Add relevant #hashtags (#AI #Privacy #OpenSource #LocalLLM)
2. **Dev.to**: Paste the article draft, tweak tone, publish
3. **HN**: Post to "Ask HN" or "Show HN" (read guidelines first)
4. **Reddit**: Tailor per subreddit, include GitHub link, ask for feedback
5. **Add to repos**: Create comparison graphics, benchmark charts

All content is ready to copy-paste. Customize with your own links/timing.
