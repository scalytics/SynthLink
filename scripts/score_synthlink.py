import pandas as pd
import markdown
import json
from collections import Counter
from bs4 import BeautifulSoup
import glob

# Metric Functions (as defined above)
def compute_f1(pred, truth): ...
def compute_p_at_5(pred_docs, relevant_docs): ...
def compute_rqs(pred, expected_steps): ...
def compute_fcs(pred, sources): ...
def compute_ie(logs, truth, max_iterations=5): ...

# Parse Markdown Files
def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    html = markdown.markdown(md_content)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    headers = [th.text.strip() for th in table.find('tr').find_all('th')]
    rows = []
    for tr in table.find_all('tr')[1:]:
        row = [td.text.strip() for td in tr.find_all('td')]
        rows.append(dict(zip(headers, row)))
    return rows

# Load Questions
questions = []
for md_file in glob.glob('*/*/SynthLink_*.md'):
    questions.extend(parse_markdown(md_file))

# Load Predictions
with open('predictions.json', 'r') as f:
    predictions = json.load(f)

# Score Responses
scores = []
for q in questions:
    pred = next((p for p in predictions if p['question_id'] == q['Question ID']), None)
    if not pred:
        continue
    f1 = compute_f1(pred['predicted_answer'], q['Expected Answer Summary'])
    p_at_5 = compute_p_at_5(pred['retrieved_docs'], q['Traceable Sources'].split(', '))
    rqs = compute_rqs(pred['predicted_answer'], q['Reasoning Steps'].split('. ')[:-1])
    fcs = compute_fcs(pred['predicted_answer'], pred['sources_verified'])
    ie = compute_ie(pred['iterations'], q['Expected Answer Summary'])
    score = (0.3 * f1) + (0.2 * p_at_5) + (0.3 * rqs) + (0.1 * fcs) + (0.1 * ie)
    scores.append({
        'question_id': q['Question ID'],
        'category': q['Question ID'].split('-')[0],
        'f1': f1,
        'p_at_5': p_at_5,
        'rqs': rqs,
        'fcs': fcs,
        'ie': ie,
        'aggregate_score': score
    })

# Aggregate Results
df_scores = pd.DataFrame(scores)
category_scores = df_scores.groupby('category').mean(numeric_only=True)
overall_score = df_scores['aggregate_score'].mean()

# Save Results
df_scores.to_csv('synthlink_scores.csv', index=False)
category_scores.to_csv('synthlink_category_scores.csv')
with open('synthlink_overall_score.txt', 'w') as f:
    f.write(f"Overall Aggregate Score: {overall_score:.4f}")

print(f"Overall Score: {overall_score:.4f}")
print("\nCategory Scores:")
print(category_scores)