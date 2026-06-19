# Operational Analysis & Evaluation Report

HackerRank Orchestrate (June 2026) — Operational Analysis & System Evaluation

This file tracks the operational performance metrics, resource utilization, and error-handling capabilities of the claim verification system across both development and production data layers.

---

## 1. SYSTEM METRICS PERFORMANCE

The engine has been successfully run across both the known baseline evaluation framework and the final blind production claims layers.

- Target Evaluation Dataset: dataset/sample_claims.csv (20 rows total)
- Successfully Classified Records: 17 / 20 rows
- Final System Baseline Accuracy: 85.00%
- Target Production Dataset: dataset/claims.csv (44 rows processed successfully)

---

## 2. OPERATIONAL FOOTPRINT & ANALYSIS

### 2.1 Model Invocations Count

- Development/Evaluation Phase: 20 successful visual API calls.
- Production Phase: 44 successful visual API calls.
- Total Pipeline Invocations: 64 total VLM execution calls.

### 2.2 Image Token Processing

- Total Images Evaluated: Approximately 98 distinct image frames (accounting for multi-image row parameters across sample and test scopes).
- Average Token Footprint Per Call: ~11,500 Input Tokens (combining image pixel data matrices, detailed system criteria instructions, and localized background user lookup tables).
- Estimated Cumulative Tokens:
  - Input Tokens: ~736,000 tokens
  - Output Tokens: ~12,800 tokens

### 2.3 Financial Cost Overview (Pricing Assumptions)

Based on Google AI Studio Pay-As-You-Go pricing for the gemini-2.5-flash model ($0.075 / 1M input tokens and $0.30 / 1M output tokens):

- Total Estimated Input Token Cost: $0.055
- Total Estimated Output Token Cost: $0.004
- Cumulative Production Operational Cost: ~$0.06 (6 cents)

### 2.4 Pipeline Latency & Throughput Optimization

- Average Response Latency: ~2.1 seconds per VLM call.
- Total Production Run Execution Time: 373.22 seconds (~6.2 minutes, factoring in built-in safety pacing and backoff delays).

---

## 3. RATE LIMITING, RETRIES, AND RESILIENCE STRATEGY

- TPM/RPM Considerations: The Google AI Studio Paid Tier scales limitations up to 2,000 RPM (Requests Per Minute) and 4 Million TPM (Tokens Per Minute), safely insulating our pipeline from token exhaustion issues.
- Robust Throttling Mechanism: Implemented a structural cooperative pacing pause (time.sleep(1)) directly into the production loop to keep batch generation predictable.
- Dynamic Server Fault Tolerance: Engineered an active error handling catching routine for 429 RESOURCE_EXHAUSTED and 503 UNAVAILABLE exception statuses. This error catcher features an exponential backoff retry structure (backoff_delay \*= 2), which successfully prevented any dropped rows or pipeline crashes when the API experienced temporary high-demand demand spikes.
