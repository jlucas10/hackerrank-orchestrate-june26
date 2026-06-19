# Multi-Modal Damage Claim Verification Engine

This repository contains an automated, multi-modal AI agent built for the HackerRank Orchestrate challenge. The system parses unstructured claim text, aggregates user profile risk contexts, evaluates image assets against minimum compliance standards, and outputs deterministic, schema-validated claim predictions.

---

## 1. Setup & Installation Instructions

### Prerequisites

- macOS, Linux, or Windows terminal
- Python 3.9 or higher
- A Google AI Studio Paid/Pay-As-You-Go API Key

### Environment Configuration

1. Clone or extract this repository to your local directory.
2. In the root directory, create a `.env` file to securely store your API credentials:
   GEMINI_API_KEY=your_actual_api_key_here
3. Install the required system dependencies using pip:
   pip install -r requirements.txt

### Running the System

- To run the full production data generation pipeline:
  python3 code/main.py

  This reads data from `dataset/claims.csv` and outputs the final compiled predictions directly into `output.csv`.

- To run the developer validation and evaluation suite:
  python3 code/evaluation/main.py

  This validates system baseline accuracy against the known `dataset/sample_claims.csv` test set.

---

## 2. Engineering Approach & Core Architecture

The system transitions from a basic script into a production-ready, fault-tolerant AI Agent by leveraging a modular 4-stage pipeline:

1. **Context Aggregation Layer (`core/processor.py`)**: Merges row-level claims with historical user frequencies (`user_history.csv`) and maps the claim object type to its corresponding visual minimum photographic standard (`evidence_requirements.csv`).
2. **Deterministic Caching Engine (`code/main.py`)**: Computes a unique MD5 hash from input text parameters and image paths. If a claim has been previously evaluated, it bypasses the network completely and fetches the data instantly from a local `.cache/vlm_cache.json` file, protecting API budgets.
3. **Cognitive Visual Core (`core/vlm_client.py`)**: Dispatches multi-modal visual payloads to `gemini-2.5-flash`. The model executes entity cross-referencing to flag text-to-pixel contradictions and checks device signatures to identify structural device mismatches.
4. **Pydantic Serialization Layer (`core/prompt_factory.py`)**: Binds model outputs to a strict Pydantic class (`ClaimEvaluationSchema`), forcing the generative model to output precise lowercase enums to guarantee automated evaluation compatibility.

---

## 3. Production Resilience & Error Handling

- **Exponential Backoff Loop**: To handle high-throughput demands, the engine wraps external API calls in an error-catching structure. When hitting `503 UNAVAILABLE` or `429` resource blocks, the agent implements a baseline pause that doubles on subsequent failures, achieving a 100% completion rate across all 44 blind claims rows.
- **Cooperative Pacing**: Includes structural pacing delays between sequential network loops to align with enterprise API tier safety limits.
