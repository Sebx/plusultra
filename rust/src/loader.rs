//! Model loading and initialization

use anyhow::{anyhow, Result};
use sha2::{Sha256, Digest};
use std::fs;
use std::path::Path;
use crate::Agent;

/// Verify model integrity using SHA-256 hashes from manifest.json
pub fn verify_model_integrity(model_dir: &Path) -> Result<()> {
    let manifest_path = model_dir.join("manifest.json");

    if !manifest_path.exists() {
        return Err(anyhow!("manifest.json not found in {:?}", model_dir));
    }

    let manifest_content = fs::read_to_string(&manifest_path)?;
    let manifest: serde_json::Value = serde_json::from_str(&manifest_content)?;

    if let Some(files) = manifest.get("files").and_then(|v| v.as_array()) {
        for file_info in files {
            let path = file_info
                .get("path")
                .and_then(|v| v.as_str())
                .ok_or_else(|| anyhow!("Invalid manifest format"))?;

            let expected_hash = file_info
                .get("sha256")
                .and_then(|v| v.as_str())
                .ok_or_else(|| anyhow!("Missing hash for {}", path))?;

            let file_path = model_dir.join(path);

            if !file_path.exists() {
                println!("⚠️  Missing: {}", path);
                continue;
            }

            // Compute SHA-256
            let file_bytes = fs::read(&file_path)?;
            let mut hasher = Sha256::new();
            hasher.update(&file_bytes);
            let hash = hex::encode(hasher.finalize());

            if hash != expected_hash {
                return Err(anyhow!(
                    "Hash mismatch for {}: expected {}, got {}",
                    path, expected_hash, hash
                ));
            }

            println!("✓ {}", path);
        }
    }

    Ok(())
}

/// Load a plusultra model from disk
///
/// # Arguments
///
/// * `model_dir` - Path to model directory (contains model.onnx and tokenizer.json)
/// * `verify_hash` - If true, verify SHA-256 hashes against manifest.json
///
/// # Example
///
/// ```ignore
/// let agent = load("./model", true)?;
/// ```
pub fn load(model_dir: &str, verify_hash: bool) -> Result<Agent> {
    let model_path = Path::new(model_dir);

    if !model_path.exists() {
        return Err(anyhow!("Model directory not found: {:?}", model_dir));
    }

    println!("📦 Loading model from {:?}", model_path);

    // Verify integrity
    if verify_hash {
        println!("🔐 Verifying SHA-256 hashes...");
        verify_model_integrity(model_path)?;
    }

    // Find ONNX model file
    let model_file = model_path.join("model.onnx");
    let model_file = if model_file.exists() {
        model_file
    } else {
        // Try to find any .onnx file
        let onnx_files: Vec<_> = fs::read_dir(model_path)?
            .filter_map(|e| {
                e.ok().and_then(|entry| {
                    let path = entry.path();
                    if path.extension().and_then(|s| s.to_str()) == Some("onnx") {
                        Some(path)
                    } else {
                        None
                    }
                })
            })
            .collect();

        if onnx_files.is_empty() {
            return Err(anyhow!(
                "No .onnx model file found in {:?}. \
                Export from HuggingFace with: \
                python -m transformers.models.export onnx ...",
                model_path
            ));
        }
        onnx_files[0].clone()
    };

    println!("🚀 Initializing ONNX Runtime session...");

    // Load tokenizer
    let tokenizer_path = model_path.join("tokenizer.json");
    if !tokenizer_path.exists() {
        return Err(anyhow!("tokenizer.json not found in {:?}", model_path));
    }

    println!("✓ Model loaded successfully");

    Agent::new(model_file, tokenizer_path)
}
