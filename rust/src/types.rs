//! Type definitions for plusultra

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Question type for classification
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum QuestionType {
    /// Multi-class classification (select one option)
    Choice,
    /// Ordinal regression (rate on a scale)
    Score,
    /// Binary classification (yes/no with nuance)
    Noul,
}

/// Question definition
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Question {
    pub id: String,
    #[serde(rename = "type")]
    pub question_type: QuestionType,
    pub instructions: String,
    /// Options for choice and score questions
    #[serde(default)]
    pub criteria: Vec<String>,
}

/// Prediction answer
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(untagged)]
pub enum Answer {
    Choice(String),
    Score(f32),
    Boolean(bool),
}

/// Prediction result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PredictionResult {
    pub answers: HashMap<String, Answer>,
    pub latencies_ms: HashMap<String, f32>,
    pub total_time_ms: f32,
    pub metadata: Metadata,
}

/// Model metadata
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Metadata {
    pub model: String,
    pub parameters: String,
    pub tokens_used: usize,
    pub questions: usize,
}

/// Benchmark results
#[derive(Debug, Serialize, Deserialize)]
pub struct BenchmarkResult {
    pub test_case: String,
    pub p50_ms: f32,
    pub p95_ms: f32,
    pub p99_ms: f32,
    pub mean_ms: f32,
    pub min_ms: f32,
    pub max_ms: f32,
    pub samples: Vec<f32>,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_question_type_serde() {
        let json = r#"{"type":"choice"}"#;
        let q: Question = serde_json::from_str(
            r#"{"id":"test","type":"choice","instructions":"Test","criteria":["a","b"]}"#
        ).unwrap();
        assert_eq!(q.question_type, QuestionType::Choice);
    }
}
