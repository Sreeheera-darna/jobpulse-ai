import csv
import sys
from pathlib import Path


AUDIT_FILE = Path(__file__).resolve().parent / "manual_audit_50_review.csv"
COMPARISONS = [
    ("Experience level", "ai_experience_level", "manual_experience_level"),
    ("Employment type", "ai_employment_type", "manual_employment_type"),
    ("Role category", "ai_role_category", "manual_role_category"),
    ("City", "ai_city", "manual_city"),
]

CITY_ALIASES = {
    "bangalore": "bengaluru",
    "gurgaon": "gurugram",
    "bombay": "mumbai",
    "cochin": "kochi",
    "madras": "chennai",
}


def normalize(value):
    return " ".join(str(value or "").strip().casefold().split())


def normalize_city(value):
    city = normalize(value).strip(" ,.")
    return CITY_ALIASES.get(city, city)


def parse_boolean(value):
    normalized = normalize(value)
    if normalized in {"true", "yes", "1"}:
        return True
    if normalized in {"false", "no", "0"}:
        return False
    return None


def report_accuracy(rows, label, predicted_field, manual_field, normalizer=normalize):
    reviewed = [
        row for row in rows
        if normalize(row.get(predicted_field))
        and normalize(row.get(manual_field))
    ]
    if not reviewed:
        print(f"{label}: no human labels yet")
        return

    correct = sum(
        normalizer(row[predicted_field]) == normalizer(row[manual_field])
        for row in reviewed
    )
    print(f"{label} accuracy: {correct}/{len(reviewed)} ({correct / len(reviewed):.1%})")


def report_fresher_metrics(rows):
    reviewed = []
    for row in rows:
        predicted = parse_boolean(row.get("ai_fresher_eligible"))
        actual = parse_boolean(row.get("manual_fresher_eligible"))
        if predicted is not None and actual is not None:
            reviewed.append((predicted, actual))

    if not reviewed:
        print("Fresher eligibility: no human labels yet")
        return

    true_positive = sum(predicted and actual for predicted, actual in reviewed)
    false_positive = sum(predicted and not actual for predicted, actual in reviewed)
    true_negative = sum(not predicted and not actual for predicted, actual in reviewed)
    false_negative = sum(not predicted and actual for predicted, actual in reviewed)
    accuracy = (true_positive + true_negative) / len(reviewed)
    precision = (
        true_positive / (true_positive + false_positive)
        if true_positive + false_positive else 0
    )
    recall = (
        true_positive / (true_positive + false_negative)
        if true_positive + false_negative else 0
    )

    print(
        f"Fresher eligibility ({len(reviewed)} labeled): "
        f"accuracy {accuracy:.1%}, precision {precision:.1%}, "
        f"recall {recall:.1%}"
    )
    print(
        "Confusion counts: "
        f"TP={true_positive}, FP={false_positive}, "
        f"TN={true_negative}, FN={false_negative}"
    )


def main():
    with AUDIT_FILE.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    print(f"Audit rows: {len(rows)}")
    print("Metrics use only rows with both AI and human labels.")
    report_fresher_metrics(rows)

    for label, predicted_field, manual_field in COMPARISONS:
        normalizer = normalize_city if label == "City" else normalize
        report_accuracy(
            rows,
            label,
            predicted_field,
            manual_field,
            normalizer=normalizer,
        )

    if not rows:
        print("No audit rows found.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
