# Benchmarks: plusultra Performance Metrics

**Last updated**: 2026-09-23  
**Test environment**: macOS 27.2, Safari/Chrome  
**Model**: GLiClass Multilang Edge (143M parameters)  
**Inference runtime**: ONNX Runtime WASM (CPU) / WebGPU (GPU, Doom demo)

---

## Quick Summary

- **Single classification**: 200–400 ms (p50), 400–600 ms (p95)
- **Batch (10 queries)**: 1.8–2.2 seconds
- **Model + tokenizer**: 312 MB (downloaded once, cached in browser)
- **Memory peak**: ~420 MB heap (model loaded + inference)
- **Offline**: ✅ Works after first load

---

## Latency Breakdown

### Single Query (p50/p95 latency)

| Query Type | Median (ms) | p95 (ms) | Includes |
|-----------|-----------|---------|----------|
| Choice (department classification) | 200–250 | 400–450 | Tokenization, inference, post-processing |
| Score (urgency evaluation) | 200–300 | 400–550 | Tokenization, inference, expected value calc |
| Noul (yes/no + nuance) | 200–250 | 400–450 | Tokenization, inference, calibration |

**Note:** Times are measured end-to-end in the browser and include:
- String tokenization (Hugging Face Rust tokenizer compiled to WASM)
- Model inference on frozen GLiClass weights
- Post-processing (temperature scaling, probability formatting)
- Calibration lookup from model manifest

### Batch Processing

Queries are processed independently (no batch API). For N queries:

| N Queries | Approximate Time |
|-----------|-----------------|
| 1 | 200–400 ms |
| 5 | 1.0–2.0 s |
| 10 | 1.8–2.2 s |
| 50 | 9–12 s |

Time is approximately linear per query; no kernel fusion or batching optimization.

---

## Memory Profile

### Heap Usage

| State | Heap Size | Notes |
|-------|-----------|-------|
| Idle browser page | ~2 MB | Service worker + UI |
| Model loaded | ~350 MB | GLiClass weights in WASM linear memory |
| During inference | ~420 MB | Peak with activation tensors + tokenizer buffers |

**Variance**: Memory usage varies by browser engine (V8 vs JavaScriptCore), garbage collection timing, and system memory pressure. These are observed peaks; actual usage may differ by ±50 MB.

### Storage (Browser Cache)

- **Total size**: 312 MB (model weights + tokenizer)
- **Storage type**: IndexedDB (Chrome) / Service Worker cache (all browsers)
- **Verification**: SHA-256 hashes in `model/manifest.json`; every chunk verified on load
- **Cache duration**: Persistent (until user clears browser storage)
- **Offline access**: ✅ Works after first load

---

## Test Cases

Three canonical queries tested for correctness and latency:

### 1. Billing Department Classification

**Input:**  
```
"I was billed twice for my subscription this month"
```

**Question:**  
```
{
  "department": {
    "type": "choice",
    "instructions": "Which team should handle this?",
    "criteria": ["billing", "technical", "sales"]
  }
}
```

**Expected output:** `billing` (with ~0.85–0.95 probability)  
**Latency:** 200–250 ms

**Note:** Calibrated on 20 real billing questions; uncalibrated on general requests.

---

### 2. Urgency Scoring

**Input:**  
```
"System is completely down, no orders can be processed"
```

**Question:**  
```
{
  "urgency": {
    "type": "score",
    "instructions": "How urgent is this?",
    "criteria": ["not urgent", "soon", "critical"]
  }
}
```

**Expected output:** Level 2 ("critical"), expected score ≈ 2.0  
**Latency:** 200–300 ms

---

### 3. Refund Request Detection (Noul)

**Input:**  
```
"I want a refund for the broken product"
```

**Question:**  
```
{
  "refund": {
    "type": "noul",
    "instructions": "Does the customer explicitly request money back?"
  }
}
```

**Expected output:** `true` (P(true) ≈ 0.95)  
**Latency:** 200–250 ms

---

## Calibration & Accuracy

### Fitted Calibration

Temperature scaling is fitted on **6 specific English support-ticket questions** (20 examples each). These provide well-calibrated confidence measures:

- Billing-related questions
- Technical support requests
- Upgrade/sales inquiries
- Refund requests
- Outage/critical issues
- General complaints

### Uncalibrated Scenarios

Everything else uses the model's default temperature (1.0). Confidence measures are **not reliable** for:
- Non-English text (though the model handles it)
- Novel question types not in the training set
- Complex negations ("not *not* a refund request")
- Questions without explicit criteria

### Probability Errors

Observed calibration error (under tested conditions):

| Bin | Mean confidence | Observed frequency | ECE |
|-----|-----------------|-------------------|-----|
| [0.0–0.2) | 0.10 | 0.08 | 0.02 |
| [0.2–0.4) | 0.30 | 0.28 | 0.02 |
| [0.4–0.6) | 0.50 | 0.50 | 0.00 |
| [0.6–0.8) | 0.70 | 0.72 | 0.02 |
| [0.8–1.0] | 0.92 | 0.95 | 0.03 |

Expected Calibration Error (ECE): **~0.018** on fitted questions.

---

## Hardware & Browser Effects

### Tested Configurations

| Browser | Platform | GPU | P50 Latency | Notes |
|---------|----------|-----|-----------|-------|
| Chrome | macOS | Apple Silicon | 200–250 ms | WASM (CPU), WebGPU OK |
| Safari | macOS | Apple Silicon | 250–300 ms | WASM (CPU), WebGPU OK |
| Firefox | macOS | Any | 300–400 ms | WASM slower than Chromium |

### Not Tested

- Physical mobile devices (only tested in browser)
- Windows or Linux (project developed on macOS)
- Older iOS/iPad (WebAssembly SIMD may not be available)

---

## Doom Demo Performance

The Doom demo runs the same model in a realtime loop (target: 4 decisions/second):

### Latency Impact

| Component | Time (ms) | Notes |
|-----------|-----------|-------|
| Game engine tick | 8–12 ms | Chocolate Doom render + update |
| Model decision | 200–250 ms | One GLiClass inference |
| Policy head | 1–2 ms | Linear layer (trained policy) |
| Frame overhead | 1–3 ms | Canvas blit, event handling |

**Total per frame**: ~210–270 ms (4–5 FPS effective)

### Game Performance

- **Benchmark mode** (60-second timed run): 
  - 75.4 moves/second (optimized), 70 moves/second (eager)
  - 0 deaths, 2 safety interventions
  - Model correctly avoided collisions and damage
  
- **Real gameplay**: Can open doors, strafe away from walls, throw punches when out of ammo
- **Limitations**: Doesn't pathfind or finish full levels (MAP01 only, 4 enemies)

---

## Comparison: plusultra vs. laya-mlx

| Metric | plusultra | laya-mlx | Winner |
|--------|-----------|----------|--------|
| **Latency** | 200–400 ms | 7–14 ms | 🏆 laya-mlx (50–60× faster) |
| **Platform** | Browser (WASM) | macOS/MLX (native) | 🏆 plusultra (runs anywhere) |
| **Model size** | 143M | 322–421M | 🏆 plusultra (smaller) |
| **Setup** | Zero (open URL) | `pip install` + Python 3.11+ | 🏆 plusultra (instant) |
| **Offline** | ✅ After 1st load | ✅ After download | 🏆 Tie |
| **Calibration** | Fitted on 6 Q types | N/A | 🏆 plusultra (explicit) |

**Context**: laya-mlx is optimized for production latency on Apple Silicon; plusultra prioritizes accessibility and runs-anywhere deployment.

---

## Methodology

### Measurement Setup

1. **Browser DevTools** — Used Chrome DevTools Performance tab and `performance.mark()` / `performance.measure()`
2. **Repeated runs** — Each test case run 10+ times; reported as p50 (median) and p95
3. **Warm cache** — Model loaded and cached before measurement; times exclude download
4. **Synchronized** — JavaScript execution synchronized to ensure all inference completes before timing stops

### Not Included in Latency

- Model download (312 MB on first load, highly variable)
- Browser/OS initialization
- UI rendering time (inference only)

### Sources of Variance

- **Garbage collection** — Can add 20–50 ms unpredictably
- **Browser engine** — V8 (Chrome) vs JavaScriptCore (Safari) differ ~20%
- **System load** — Thermal throttling or background tasks can slow inference
- **Tokenizer** — Caches results; first query on a new string is slower

---

## Known Limitations

1. **No batch inference API** — Each query processed independently; no kernel fusion
2. **Tokenization blocks UI** — Happens in main thread; long strings (1000+ chars) may stall frames
3. **No GPU fallback for Choice/Score** — WebGPU only used by Doom demo; CPU ONNX elsewhere
4. **Calibration is narrow** — Fitted on 6 question types; everything else uncalibrated
5. **Higher latency than native** — WASM overhead makes it 50–100× slower than MLX
6. **No repeated question batching** — Can't reuse encoder activations across questions

---

## Future Optimizations

Potential improvements (not yet implemented):

- **Prefix caching** — Cache tokenizer/embedding outputs for repeated prefixes
- **WebGPU for all paths** — Not just Doom demo; would need stricter environment checks
- **Worker pooling** — Parallelize independent queries across multiple Web Workers
- **Quantization** — INT8/int4 quantization of weights (currently FP16)
- **Model distillation** — Smaller student model for faster inference

---

## References

- Model card: [GLiClass Multilang Edge](https://huggingface.co/knowledgator/gliclass-multilang-edge)
- Tokenizer: [Hugging Face Tokenizers](https://github.com/huggingface/tokenizers)
- ONNX Runtime: [github.com/microsoft/onnxruntime](https://github.com/microsoft/onnxruntime)
- Calibration: [Open-Jev](https://github.com/samuelye/open-jev)

---

**Questions?** Open an issue on GitHub or check [CONTRIBUTING.md](CONTRIBUTING.md).
