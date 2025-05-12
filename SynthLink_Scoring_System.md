# Performance Criteria for SynthLink Benchmark

This document defines target performance thresholds for the SynthLink Catalog’s five evaluation metrics. These criteria represent near-optimal system behavior when answering complex, multi-hop research questions.

---

## Aggregate Score

Responses are aggregated using the weighted sum:

```text
Aggregate Score = 0.3·F1 + 0.2·P@5 + 0.3·RQS + 0.1·FCS + 0.1·IE
```

**Target Aggregate Score:** ≥ 0.90

---

## 1. F1 Score (Answer Accuracy)

* **Definition:** Harmonic mean of token-level precision and recall against the reference summary.
* **Calculation:**

  * Precision = $|P ∩ T| / |P|$
  * Recall = $|P ∩ T| / |T|$
  * F1 = $2 · Precision · Recall / (Precision + Recall)$
* **Target Range:** 0.90–1.00
* **Rationale:** Indicates comprehensive coverage of key facts with minimal omissions.

---

## 2. Precision\@5 (Retrieval Quality)

* **Definition:** Proportion of top-five retrieved documents that are relevant.
* **Calculation:**

  $$
    P@5 = \frac{|D_{pred} ∩ D_{relevant}|}{5}
  $$
* **Target Range:** 0.80–1.00
* **Rationale:** Ensures robust source selection for evidence chaining.

---

## 3. Reasoning Quality Score (RQS)

* **Definition:** Fraction of predefined reasoning steps present in the system’s explanation, capped at 1.0.
* **Calculation:**

  $$
    RQS = \min\Bigl(\frac{1}{n} \sum_{i=1}^{n} \mathbb{I}(s_i \text{ present}), 1.0\Bigr)
  $$
* **Target Range:** 0.90–1.00
* **Rationale:** Validates that all critical inference steps are articulated.

---

## 4. Fact-Checking Score (FCS)

* **Definition:** Proportion of factual claims that are verifiable against cited sources.
* **Calculation:**

  $$
    FCS = \frac{1}{m} \sum_{j=1}^{m} \mathbb{I}(c_j \text{ verified})
  $$
* **Target Value:** 1.00
* **Rationale:** Guarantees that all assertions are grounded in evidence, especially for speculative topics.

---

## 5. Iterative Efficiency (IE)

* **Definition:** Inverse of the number of iterations (k) required to produce the first correct answer, with k capped at 5.
* **Calculation:**

  $$
    IE = \frac{1}{\min(k, 5)}
  $$
* **Target Range:** 0.50–1.00
* **Rationale:** Measures the system’s convergence speed on complex queries.

---

*Document last updated: May 2025*
