"""Model loading and initialization."""

import os
import json
import hashlib
from pathlib import Path

try:
    import onnxruntime as ort
except ImportError:
    raise ImportError(
        "onnxruntime is required. Install with: pip install onnxruntime"
    )

from .agent import Agent


def verify_model_integrity(model_dir: str) -> bool:
    """Verify model integrity using SHA-256 hashes from manifest.json."""
    manifest_path = Path(model_dir) / "manifest.json"

    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest.json not found in {model_dir}")

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    for file_info in manifest.get("files", []):
        file_path = Path(model_dir) / file_info["path"]
        expected_hash = file_info["sha256"]

        if not file_path.exists():
            print(f"⚠️  Missing: {file_path}")
            continue

        # Compute SHA-256
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)

        actual_hash = sha256_hash.hexdigest()
        if actual_hash != expected_hash:
            raise ValueError(
                f"Hash mismatch for {file_info['path']}: "
                f"expected {expected_hash}, got {actual_hash}"
            )

        print(f"✓ {file_info['path']}")

    return True


def load(model_dir: str = "../model", verify_hash: bool = True) -> Agent:
    """
    Load a plusultra model from disk.

    Args:
        model_dir: Path to model directory (contains weights and tokenizer)
        verify_hash: If True, verify SHA-256 hashes against manifest.json

    Returns:
        Agent: Ready-to-use inference agent

    Example:
        agent = load("./model")
        result = agent.predict("text", {...})
    """
    model_dir = Path(model_dir).resolve()

    if not model_dir.exists():
        raise FileNotFoundError(f"Model directory not found: {model_dir}")

    print(f"📦 Loading model from {model_dir}")

    # Verify integrity
    if verify_hash:
        print("🔐 Verifying SHA-256 hashes...")
        verify_model_integrity(str(model_dir))

    # Initialize ONNX Runtime session
    model_file = model_dir / "model.onnx"
    if not model_file.exists():
        # Try to find .onnx file
        onnx_files = list(model_dir.glob("*.onnx"))
        if not onnx_files:
            raise FileNotFoundError(
                f"No .onnx model file found in {model_dir}. "
                f"Export from HuggingFace with: "
                f"python -m transformers.models.export onnx ..."
            )
        model_file = onnx_files[0]

    print(f"🚀 Initializing ONNX Runtime session...")
    session = ort.InferenceSession(
        str(model_file),
        providers=["CPUExecutionProvider"]
    )

    # Load tokenizer
    tokenizer_path = model_dir / "tokenizer.json"
    if not tokenizer_path.exists():
        raise FileNotFoundError(f"tokenizer.json not found in {model_dir}")

    print(f"✓ Model loaded successfully")

    return Agent(session, model_dir, tokenizer_path)
