"""Inference agent for plusultra."""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Union

try:
    from transformers import AutoTokenizer
except ImportError:
    raise ImportError(
        "transformers is required. Install with: pip install transformers"
    )


class Agent:
    """Local inference agent for GLiClass text classification."""

    def __init__(self, session: Any, model_dir: Path, tokenizer_path: Path):
        """
        Initialize agent with ONNX Runtime session and tokenizer.

        Args:
            session: ONNX Runtime InferenceSession
            model_dir: Path to model directory
            tokenizer_path: Path to tokenizer.json
        """
        self.session = session
        self.model_dir = model_dir
        self.tokenizer = AutoTokenizer.from_pretrained(str(model_dir))

        # Load calibration temperatures if available
        self.temperatures = self._load_temperatures()

    def _load_temperatures(self) -> Dict[str, float]:
        """Load temperature calibration values."""
        temps_file = self.model_dir / "temperatures.json"
        if temps_file.exists():
            with open(temps_file, "r") as f:
                return json.load(f)
        return {}

    def predict(
        self,
        state: str,
        questions: Dict[str, Dict[str, Any]],
        dtype: str = "float32",
        batch_size: int = 1,
    ) -> Dict[str, Any]:
        """
        Classify text and answer structured questions.

        Args:
            state: Input text to classify
            questions: Dict of question definitions, each with:
                - type: "choice", "score", or "noul"
                - instructions: Question prompt
                - criteria: List of options (choice/score) or None (noul)
            dtype: "float32" or "float16"
            batch_size: Number of questions per forward pass

        Returns:
            Dict with:
                - answers: Dict of question_id -> prediction
                - latencies: Dict of question_id -> inference_time_ms
                - metadata: Model info and tokens used

        Example:
            result = agent.predict(
                "I was billed twice",
                {
                    "department": {
                        "type": "choice",
                        "instructions": "Which team?",
                        "criteria": ["billing", "tech", "sales"]
                    }
                }
            )
            # → {"answers": {"department": "billing"}, ...}
        """
        start_time = time.perf_counter()

        answers = {}
        latencies = {}
        token_counts = []

        # Process each question
        for q_id, question in questions.items():
            q_start = time.perf_counter()

            q_type = question.get("type", "choice")
            criteria = question.get("criteria", [])
            instructions = question.get("instructions", "")

            # Format prompt (simplified; real implementation would match GLiClass schema)
            prompt = f"{instructions}\n\nText: {state}\n\nOptions: {', '.join(criteria)}"

            # Tokenize
            tokens = self.tokenizer(
                prompt,
                return_tensors="np",
                truncation=True,
                max_length=512
            )

            token_counts.append(tokens["input_ids"].shape[1])

            # Run inference
            input_ids = tokens["input_ids"].astype("int64")
            attention_mask = tokens.get("attention_mask", None)

            try:
                outputs = self.session.run(
                    None,  # All outputs
                    {"input_ids": input_ids, "attention_mask": attention_mask}
                    if attention_mask is not None
                    else {"input_ids": input_ids}
                )

                # Parse output based on question type
                if q_type == "choice" and len(criteria) > 0:
                    logits = outputs[0][0][:len(criteria)]
                    probabilities = self._softmax(logits)
                    best_idx = int(probabilities.argmax())
                    answer = criteria[best_idx]

                elif q_type == "score" and len(criteria) > 0:
                    logits = outputs[0][0][:len(criteria)]
                    probabilities = self._softmax(logits)
                    score = float(probabilities.dot(range(len(criteria))))
                    answer = score

                elif q_type == "noul":
                    logits = outputs[0][0][:2]  # Binary
                    probabilities = self._softmax(logits)
                    answer = probabilities[1] > 0.5  # P(True)

                else:
                    answer = None

                answers[q_id] = answer

            except Exception as e:
                print(f"⚠️  Error processing question '{q_id}': {e}")
                answers[q_id] = None

            q_latency = (time.perf_counter() - q_start) * 1000
            latencies[q_id] = q_latency

        total_time = (time.perf_counter() - start_time) * 1000

        return {
            "answers": answers,
            "latencies_ms": latencies,
            "total_time_ms": total_time,
            "metadata": {
                "model": "GLiClass Multilang Edge",
                "parameters": "143M",
                "tokens_used": sum(token_counts),
                "questions": len(questions),
            }
        }

    @staticmethod
    def _softmax(x):
        """Compute softmax."""
        import numpy as np
        x = x - x.max()
        return np.exp(x) / np.exp(x).sum()

    def batch_predict(
        self,
        queries: List[Dict[str, Any]],
        batch_size: int = 16
    ) -> List[Dict[str, Any]]:
        """
        Run multiple predictions efficiently.

        Args:
            queries: List of {"state": "...", "questions": {...}} dicts
            batch_size: Process this many queries per batch

        Returns:
            List of prediction results
        """
        results = []
        for i in range(0, len(queries), batch_size):
            batch = queries[i:i+batch_size]
            for query in batch:
                result = self.predict(query["state"], query["questions"])
                results.append(result)
        return results
