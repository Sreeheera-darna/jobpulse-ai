import csv
from pathlib import Path

file_path = Path(__file__).parent / "manual_audit_50.csv"

with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))

tp = fp = tn = fn = 0

for row in rows:
    ai = str(row["AI Fresher Eligible"]).strip().lower() == "true"
    human = str(row["Human Fresher Eligible"]).strip().lower() == "true"

    if ai and human:
        tp += 1
    elif ai and not human:
        fp += 1
    elif not ai and human:
        fn += 1
    else:
        tn += 1

total = tp + fp + tn + fn

accuracy = (tp + tn) / total if total else 0
precision = tp / (tp + fp) if tp + fp else 0
recall = tp / (tp + fn) if tp + fn else 0
f1 = (
    2 * precision * recall / (precision + recall)
    if precision + recall else 0
)

print("MANUAL AUDIT RESULTS")
print("--------------------")
print("Total audited:", total)
print("True positives:", tp)
print("False positives:", fp)
print("True negatives:", tn)
print("False negatives:", fn)
print(f"Accuracy:  {accuracy:.2%}")
print(f"Precision: {precision:.2%}")
print(f"Recall:    {recall:.2%}")
print(f"F1 score:  {f1:.2%}")
