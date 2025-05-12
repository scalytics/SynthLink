# SynthLink Catalog

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Python Version](https://img.shields.io/badge/python-%3E%3D3.7-blue)](https://www.python.org/)

A benchmark of 60 complex, multi-hop questions designed for evaluating deep search systems. Organized across six categories, SynthLink challenges models to link iteratively, synthesize information, fact-check, and form novel connections without hallucinations.

---

## Table of Contents

* [Overview](#overview)
* [Scoring System](#scoring-system)

  * [Aggregate Score](#aggregate-score)
  * [1. F1 Score (Answer Accuracy)](#1-f1-score-answer-accuracy)
  * [2. Precision@5 (Retrieval Quality)](#2-precision5-retrieval-quality)
  * [3. Reasoning Quality Score (RQS)](#3-reasoning-quality-score-rqs)
  * [4. Fact-Checking Score (FCS)](#4-fact-checking-score-fcs)
  * [5. Iterative Efficiency (IE)](#5-iterative-efficiency-ie)
* [Implementation](#implementation)
* [Notes](#notes)
* [References](#references)

---

## Overview

The SynthLink Catalog comprises **60** intricate, multi-hop questions spanning six thematic areas:

| Category                                  | Abbreviation | Example File                                             |
| ----------------------------------------- | ------------ | -------------------------------------------------------- |
| Historical Impact Analysis                | HIA          | `HIA/SynthLink_Historical_Impact_Analysis.md`            |
| Economic and Industrial Shifts            | EIS          | `EIS/SynthLink_Economic_Industrial_Shifts.md`            |
| Environmental and Ecological Consequences | EEC          | `EEC/SynthLink_Environmental_Ecological_Consequences.md` |
| Scientific and Technological Evolution    | STE          | `STE/SynthLink_Scientific_Technological_Evolution.md`    |
| Policy and Social Movements               | PSM          | `PSM/SynthLink_Policy_Social_Movements.md`               |
| STEM and Future Tech                      | SFT          | `SFT/SynthLink_STEM_Future_Tech.md`                      |

Each question tests:

* **Iterative Linking:** Following chains of evidence
* **Synthesis:** Crafting cohesive narratives
* **Fact-Checking:** Verifying claims against sources
* **Novel Connections:** Avoiding hallucinations

This repository includes a scoring methodology (`score_synthlink.py`) defining five metrics to evaluate system responses.

---

## Scoring System

Each response is scored on five normalized metrics (range: 0 to 1) and combined into an **aggregate score**:

```text
Aggregate Score = 0.3 * F1 + 0.2 * P@5 + 0.3 * RQS + 0.1 * FCS + 0.1 * IE
```

Weights emphasize synthesis (F1, RQS), while balancing retrieval (P\@5), factual accuracy (FCS), and efficiency (IE).

### 1. F1 Score (Answer Accuracy)

**Purpose:** Measures alignment between the predicted answer and the ground-truth summary.

**Calculation:**

* Let `P` = predicted tokens, `T` = ground-truth tokens.
* Precision: `|P ∩ T| / |P|`
* Recall: `|P ∩ T| / |T|`
* F1: `2 * Precision * Recall / (Precision + Recall)` (or 0 if undefined)

**Example:**

> For HIA-01 (“Printing press and literacy”), omitting “Reformation” yields an approximate F1 of **0.8**.

### 2. Precision\@5 (P\@5) (Retrieval Quality)

**Purpose:** Evaluates relevance among the top five retrieved documents.

**Calculation:**

* Let `D_p` = predicted top‑5 documents, `D_r` = set of relevant sources.
* `P@5 = |D_p ∩ D_r| / 5`

**Example:**

> For EIS-09 (“Blockbuster’s decline”), 3 relevant docs ⇒ **P\@5 = 0.6**.

### 3. Reasoning Quality Score (RQS)

**Purpose:** Ensures complete coverage of reasoning steps.

**Calculation:**

* Let `S = {s₁, …, sₙ}` be the set of step keywords.
* RQS = `min((∑ᵢ I(sᵢ in prediction) / n), 1)`

  * I = 1 if keyword present, else 0

**Example:**

> For PSM-01 (“Silent Spring”), missing one out of three steps ⇒ **RQS = 0.67**.

### 4. Fact-Checking Score (FCS)

**Purpose:** Verifies each claim against provided sources (critical for speculative topics in SFT).

**Calculation:**

* Let `C = {c₁, …, cₘ}` be the set of claims.
* FCS = `(∑ᵢ I(cᵢ in sources) / m)`

**Example:**

> For SFT-03 (“ASI’s impact”), 1 unverified claim out of 5 ⇒ **FCS = 0.8**.

### 5. Iterative Efficiency (IE)

**Purpose:** Measures the number of iterations taken to reach a correct answer.

**Calculation:**

* Let `k` = iteration count of the first correct answer (if none, IE = 0).
* IE = `1 / min(k, 5)`

**Example:**

> For EEC-03 (“Amazon deforestation”), correct at iteration 2 ⇒ **IE = 0.5**.

---

## Implementation

The scoring system is implemented in **`score_synthlink.py`**. It:

1. Parses category Markdown files.

2. Loads predictions from `predictions.json`:

   ```json
   [
     {
       "question_id": "HIA-01",
       "predicted_answer": "The printing press made books cheaper, boosting literacy.",
       "retrieved_docs": ["https://en.wikipedia.org/wiki/Printing_press"],
       "iterations": [{"answers": ["Books cheaper"], "docs": []}],
       "sources_verified": ["Wikipedia text"]
     }
     // … other entries
   ]
   ```

3. Computes per-question scores.

4. Outputs:

   * `synthlink_scores.csv` (detailed scores for each question)
   * `synthlink_category_scores.csv` (average scores per category)
   * `synthlink_overall_score.txt`

**Dependencies:**

```bash
pip install pandas markdown beautifulsoup4
```

**Usage:**

```bash
python score_synthlink.py --predictions predictions.json --output-dir results/
```

---

## Notes

* **Validation:** Mock prediction tests confirmed robustness across categories.
* **Limitations:**

  * Keyword-based RQS may miss contextual nuance.
  * FCS uses simplistic text matching.
  * SFT requires integration with dynamic sources (e.g., arXiv).
* **Future Work:**

  * LLM-based reasoning evaluation.
  * Advanced fact-checking APIs.
  * Real-time source integration.

---

## References

* **SynthLink Catalog Repository:** [GitHub](https://github.com/your-org/synthlink-catalog)
* **Detailed Scoring Methodology:** `SynthLink_Scoring_System.md`
* **Implementation Script:** `scripts/score_synthlink.py`
