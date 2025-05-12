# SynthLink Catalog 

The SynthLink Catalog is a collection of complex, multi-hop questions designed for testing deep search / deep research systems. It is split into categories, each in a separate Markdown file:

- [Historical Impact Analysis](HIA/SynthLink_Historical_Impact_Analysis.md)
- [Economic and Industrial Shifts](EIS/SynthLink_Economic_Industrial_Shifts.md)
- [Environmental and Ecological Consequences](EEC/SynthLink_Environmental_Ecological_Consequences.md)
- [Scientific and Technological Evolution](STE/SynthLink_Scientific_Technological_Evolution.md)
- [Policy and Social Movements](PSM/SynthLink_Policy_Social_Movements.md)
- [STEM and Future Tech](SFT/SynthLink_STEM_Future_Tech.md)

## Scoring

The SynthLink Catalog evaluates deep search responses using a scoring system that measures answer accuracy, source relevance, reasoning quality, fact-checking, and search efficiency. Each question is scored on five metrics:

- **F1 Score**: Checks how well the answer matches the expected summary.
- **Precision@5 (P@5)**: Measures relevance of the top 5 retrieved sources.
- **Reasoning Quality Score (RQS)**: Assesses if all reasoning steps are covered.
- **Fact-Checking Score (FCS)**: Ensures answers are verifiable, avoiding false claims.
- **Iterative Efficiency (IE)**: Evaluates how quickly the correct answer is found.

Scores are combined into an aggregate score (0–1) with weights emphasizing accuracy and reasoning. For details, see [SynthLink_Scoring_System.md](SynthLink_Scoring_System.md). Run `scripts/score_synthlink.py` to compute scores automatically.