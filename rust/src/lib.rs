//! plusultra: Native Rust runtime for local text classification
//!
//! Run the GLiClass model locally without cloud APIs.
//!
//! # Example
//!
//! ```ignore
//! use plusultra::{Agent, load};
//!
//! let agent = load("../model")?;
//! let result = agent.predict(
//!     "I was billed twice for my subscription",
//!     vec![
//!         ("department", vec!["billing", "technical", "sales"]),
//!     ]
//! )?;
//!
//! println!("{:?}", result.answers);  // {"department": "billing"}
//! ```

pub mod agent;
pub mod loader;
pub mod types;

pub use agent::Agent;
pub use loader::load;
pub use types::{PredictionResult, QuestionType};
