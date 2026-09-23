//! Inference agent for plusultra

use anyhow::Result;
use std::collections::HashMap;
use std::path::PathBuf;
use std::time::Instant;
use crate::types::{Answer, Metadata, PredictionResult, Question, QuestionType};

/// Local inference agent for GLiClass text classification
pub struct Agent {
    model_path: PathBuf,
    tokenizer_path: PathBuf,
}

impl Agent {
    /// Create a new agent
    pub fn new(model_path: PathBuf, tokenizer_path: PathBuf) -> Result<Self> {
        Ok(Agent {
            model_path,
            tokenizer_path,
        })
    }

    /// Classify text and answer structured questions
    ///
    /// # Arguments
    ///
    /// * `state` - Input text to classify
    /// * `questions` - Vector of question definitions
    ///
    /// # Returns
    ///
    /// Prediction result with answers, latencies, and metadata
    ///
    /// # Example
    ///
    /// ```ignore
    /// let questions = vec![
    ///     Question {
    ///         id: "department".to_string(),
    ///         question_type: QuestionType::Choice,
    ///         instructions: "Which team?".to_string(),
    ///         criteria: vec!["billing", "technical", "sales"],
    ///     }
    /// ];
    ///
    /// let result = agent.predict("I was billed twice", questions)?;
    /// ```
    pub fn predict(&self, state: &str, questions: Vec<Question>) -> Result<PredictionResult> {
        let start_time = Instant::now();
        let mut answers = HashMap::new();
        let mut latencies_ms = HashMap::new();
        let mut token_count = 0;

        // Process each question
        for question in questions {
            let q_start = Instant::now();

            // Simplified mock inference (real implementation would use ONNX Runtime)
            let answer = self.classify_question(state, &question)?;
            token_count += estimate_tokens(state);

            answers.insert(question.id.clone(), answer);
            latencies_ms.insert(question.id, q_start.elapsed().as_secs_f32() * 1000.0);
        }

        let total_time = start_time.elapsed().as_secs_f32() * 1000.0;

        Ok(PredictionResult {
            answers,
            latencies_ms,
            total_time_ms: total_time,
            metadata: Metadata {
                model: "GLiClass Multilang Edge".to_string(),
                parameters: "143M".to_string(),
                tokens_used: token_count,
                questions: questions.len(),
            },
        })
    }

    /// Classify a single question
    fn classify_question(&self, state: &str, question: &Question) -> Result<Answer> {
        match question.question_type {
            QuestionType::Choice => {
                // Mock: return first criterion
                let answer = question
                    .criteria
                    .first()
                    .cloned()
                    .unwrap_or_default();
                Ok(Answer::Choice(answer))
            }
            QuestionType::Score => {
                // Mock: return middle score
                let score = question.criteria.len() as f32 / 2.0;
                Ok(Answer::Score(score))
            }
            QuestionType::Noul => {
                // Mock: return true if text contains keywords
                let has_refund = state.to_lowercase().contains("refund")
                    || state.to_lowercase().contains("money back");
                Ok(Answer::Boolean(has_refund))
            }
        }
    }

    /// Get model path
    pub fn model_path(&self) -> &PathBuf {
        &self.model_path
    }

    /// Get tokenizer path
    pub fn tokenizer_path(&self) -> &PathBuf {
        &self.tokenizer_path
    }
}

/// Estimate token count (simplified)
fn estimate_tokens(text: &str) -> usize {
    // Rough heuristic: ~1.3 tokens per word
    text.split_whitespace().count() + (text.split_whitespace().count() / 4)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_token_estimation() {
        let text = "I was billed twice for my subscription";
        let tokens = estimate_tokens(text);
        assert!(tokens > 0);
    }
}
