# Contributing to plusultra

Thanks for taking a look. This project is intentionally small in scope (a browser-only classifier and a Doom demo built on top of it), so most contributions fall into a few clear buckets below.

## Running it locally

```bash
git clone https://github.com/Sebx/plusultra.git
cd plusultra
python3 -m http.server 8787 --bind 127.0.0.1   # or start-mac.sh / start-windows.cmd
```

Open `http://localhost:8787` — don't open `index.html` via `file://`, the service worker and module scripts need a real origin. See the [Quickstart](README.md#quickstart) for OS-specific launchers.

## A note on the shipped JS

`app.js`, `doom.js`, `worker.js`, and `gpu-worker.js` are esbuild-bundled build artifacts, not hand-authored source. If you're proposing a behavioral change:

- For UI/logic changes, describe the change and the reasoning in your PR; small, targeted diffs against the bundled file are fine for this project's size.
- For changes to the **Doom policy head** specifically, the full training pipeline (synthetic data generator, feature engineering, and the training script) ships in `doom-source.tar.gz` under `browser-controller/`. Please retrain from there rather than hand-editing the embedded model weights in `doom.js`, and report the resulting validation/test accuracy in your PR description.

## Reporting issues

Please include:

- Browser + OS, and whether you're on the WASM or WebGPU backend (Doom demo).
- Whether the issue is about the Decision Lab, the Doom demo, or the model/licensing itself.
- For classifier accuracy issues: the exact text, question type, and criteria you used, plus whether it falls inside the calibrated scope described in the [Limitations](README.md#limitations-read-this) section.
- For Doom demo issues: the downloaded measurement JSON if you have one (the **Download measurement** button in the demo).

## Licensing boundary

plusultra's own code is MIT. The Doom demo bundles Chocolate Doom under **GPL-2.0-or-later** — if your contribution touches `doom-source.tar.gz`, the browser bridge, or the compiled engine, please keep that boundary in mind and check [`THIRD_PARTY.md`](THIRD_PARTY.md) before adding new third-party code.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Be kind.
