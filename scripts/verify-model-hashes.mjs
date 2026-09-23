#!/usr/bin/env node
// Verifies that the shipped model files match the SHA-256 hashes recorded in
// model/manifest.json. This is the same integrity guarantee the app itself
// relies on before trusting a cached model in the browser — run here too so
// a corrupted or tampered file fails CI instead of failing silently at runtime.
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const modelDir = join(root, "model");
const manifest = JSON.parse(readFileSync(join(modelDir, "manifest.json"), "utf8"));

function sha256(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

let failures = 0;
function check(label, path, expected) {
  const actual = sha256(path);
  const ok = actual === expected;
  console.log(`${ok ? "OK  " : "FAIL"} ${label}`);
  if (!ok) {
    console.log(`     expected ${expected}`);
    console.log(`     actual   ${actual}`);
    failures++;
  }
}

// Files referenced directly by name in the manifest (tokenizer assets).
for (const [name, info] of Object.entries(manifest.files ?? {})) {
  if (name === "model.onnx") continue; // reference hash for the unsplit model; not shipped as a single file
  check(name, join(modelDir, name), info.sha256);
}

// The split model weight parts.
for (const part of manifest.parts ?? []) {
  check(part.name, join(modelDir, part.name), part.sha256);
}

if (failures > 0) {
  console.error(`\n${failures} file(s) failed hash verification.`);
  process.exit(1);
}
console.log("\nAll model files match model/manifest.json.");
