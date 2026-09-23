# Reused components

- [GLiClass Multilang Edge](https://huggingface.co/knowledgator/gliclass-multilang-edge), Apache 2.0, revision `d16c08ef70547514081952104e6fc3d190d9ee39`. The original model card is under `models/decision/README.md` and the license is under `models/decision/LICENSE`. The checkpoint was exported to ONNX and the vocabulary table was compressed. The published application retains these weights. An Open-Jev-trained candidate was rejected after a regression. No Bonsai distillation is claimed.
- [GLiClass 0.1.20](https://github.com/Knowledgator/GLiClass), Apache 2.0, used for model preparation and export.
- [ONNX Runtime 1.30.0](https://github.com/microsoft/onnxruntime), MIT, used for native, WebAssembly, and WebGPU execution.
- [Tokenizers.js 0.2.0](https://github.com/huggingface/tokenizers.js), Apache 2.0, used for shared local tokenization.
- [esbuild](https://github.com/evanw/esbuild), MIT, used for packaging.
- [Playwright](https://github.com/microsoft/playwright), Apache 2.0, used for development tests.
- [Open-Jev](https://github.com/Zefan-Cai/Open-Jev), MIT, revision `ed45657bf726c3b77408942830e5578f99df904e`. Unchanged utilities and provenance hashes are under `third_party/open_jev/`. plusultra reuses metrics, calibration logic, and a synthetic support-control generator. Confidence formulas were adapted to JavaScript. Generated examples declare CC0-1.0. Open-Jev Qwen models and unrelated datasets are not included.

JEV and Bonsai are external references. plusultra includes no proprietary JEV weights and does not distribute Bonsai.

## Browser Doom

- [Chocolate Doom](https://github.com/chocolate-doom/chocolate-doom), GPL-2.0-or-later, and the C bridge from the [jev-doom-agent fork](https://github.com/lukaske/jev-doom-agent/tree/318c32a24851444c1170bf083671c38723f3a35a). The fork is pinned to `318c32a24851444c1170bf083671c38723f3a35a`; the engine is pinned to `3e0cd5dc0cd0d5b6788100a2fbc1cdd4ce014b35`. The three runtime binaries are reused unchanged and verified in `third_party/doom/manifest.json`. Corresponding source and the Emscripten 4.0.14 build script are retained. The unlicensed TypeScript controller from that repository is not copied.
- [Freedoom 0.13.0](https://github.com/freedoom/freedoom/releases/tag/v0.13.0), BSD. The free WAD, license, and credits are under `third_party/doom/licenses/`. No commercial Doom WAD is distributed.
- SDL2 and Emscripten licenses remain in the same directory.
- `doom-source.tar.gz` contains engine source, build files, the free WAD, attribution, and plusultra integration code for review.
