# Claude Code Guide for plusultra

## Project Overview

**plusultra** is a browser-based text classification engine and Doom-playing agent that runs entirely client-side using ONNX Runtime. No servers, no API keys, 100% on-device inference.

- **Main use**: Text classification using a 143M-parameter GLiClass model
- **Demo**: AI-powered Doom player that uses game sensors (not pixels) to make decisions
- **Key constraint**: Everything must work offline after the first load

## Architecture

```
index.html / doom.html       → UI entry points
app.js / doom.js            → Application logic
worker.js / gpu-worker.js   → ONNX Runtime workers (CPU/WebGPU)
sw.js                       → Service worker (offline caching)
model/                      → GLiClass weights + tokenizer (312MB, split into chunks)
doom-engine/, runtime/      → Chocolate Doom WASM + ONNX Runtime binaries
```

## How to Run Locally

```bash
# Windows
start-windows.cmd           # Or pass -Port 9000

# macOS
bash start-mac.sh          # Or pass --port 9000 --no-browser

# Linux
python3 -m http.server 8787 --bind 127.0.0.1
```

Then open `http://localhost:8787` and click **Load local engine**.

**Important**: Never open `index.html` via `file://` — the app needs HTTP for service workers and module scripts to work.

## Key Files

| File | Purpose |
|------|---------|
| `index.html` | Decision Lab UI (text classification) |
| `doom.html` | Doom demo UI + trained policy head |
| `worker.js` | ONNX Runtime worker for CPU inference |
| `gpu-worker.js` | ONNX Runtime worker for WebGPU (Doom demo) |
| `sw.js` | Service worker for offline caching |
| `model/manifest.json` | Hash verification for all model weights |
| `doom-source.tar.gz` | Full Doom engine source + training code |
| `THIRD_PARTY.md` | Detailed license attribution |

## Model Details

- **Base model**: GLiClass Multilang Edge (Apache 2.0)
- **Size**: 143M parameters, ~312MB on disk (split into 50MB chunks for browser caching)
- **Verification**: SHA-256 hashes in `model/manifest.json`
- **Tokenizer**: Stored as JSON in `model/tokenizer.json`
- **Calibration**: Temperature scaling only fitted on 6 specific English support-ticket questions (20 examples each)

## Known Limitations

1. **Confidence ≠ correctness** — concentration measure, not accuracy
2. **Weak on negation** and uncalibrated `noul` questions without explicit criteria
3. **Doom demo** — validated on controlled MAP01 with 4 enemies, doesn't finish full levels
4. **Hardware**: Only tested on desktop browsers; not validated on physical mobile devices
5. **Not JEV-equivalent** — no Bonsai distillation included

## Testing & CI

- GitHub Actions workflow in `.github/workflows/ci.yml`
- Run scripts verify model hashes (see `scripts/verify-model-hashes.mjs`)
- No automated tests yet — manual validation in browser recommended

## Dependencies

All pinned and open-source:
- ONNX Runtime (WASM)
- Chocolate Doom (WebAssembly)
- Freedoom (free game WAD)
- Tokenizers.js
- SDL2, Emscripten

See `licenses/` and `doom-licenses/` for full attribution.

## Common Tasks

**Add a new classification question type:**
1. Update `app.js` to handle the new question format
2. Ensure it matches the model's expected input schema
3. Add temperature scaling calibration if possible
4. Document limitations in this file

**Modify the Doom policy:**
1. Extract and modify `doom-source.tar.gz`
2. Retrain the policy head
3. Replace the policy weights in `doom.js`
4. Test in 60-second benchmark mode

**Optimize model loading:**
1. Keep chunks at ~50MB (GitHub's recommended max)
2. Parallelize fetches in `worker.js` if needed
3. Monitor cache stats in browser DevTools

## Deployment Notes

- **PWA**: Installable after first load (service worker cached)
- **Offline**: Works completely offline after initial model download
- **Privacy**: Zero telemetry, zero external API calls
- **HTTPS requirement**: WebGPU demo needs HTTPS or localhost
- **Large files**: Use Git LFS for weights (currently stored as binary blobs)

## Contributing

- See `CONTRIBUTING.md` for setup and PR guidelines
- Read `CODE_OF_CONDUCT.md`
- Run local verification: `node scripts/verify-model-hashes.mjs`
- Test on both CPU (worker.js) and WebGPU (gpu-worker.js) paths

---

**Last updated**: 2026-09-23
