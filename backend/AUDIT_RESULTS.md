
# JobPulse AI — Manual Audit Results

## Current sample

The current `manual_audit_50_review.csv` contains 50 randomly selected
classified listings. The human-label columns are blank, so current-snapshot
accuracy has not yet been measured. A reviewer should compare each full job
description with the AI fields and fill in:

- `manual_fresher_eligible` (`true` or `false`)
- `manual_experience_level`
- `manual_employment_type`
- `manual_role_category`
- `manual_city`
- `reviewer_notes` for ambiguous decisions

Run `python audit_metrics.py` from `backend/` after review. It reports metrics
for rows with both predicted and human labels; do not substitute the prior
sample's results for this audit.

## Historical sample (not the current snapshot)

An earlier 50-listing sample was reviewed for fresher eligibility only:

| Metric | Historical result |
|---|---:|
| Total audited | 50 |
| True positives | 12 |
| False positives | 3 |
| True negatives | 35 |
| False negatives | 0 |
| Accuracy | 94.00% |
| Precision | 80.00% |
| Recall | 100.00% |
| F1 score | 88.89% |

This targeted sample included every AI-predicted eligible listing and a
random subset of AI-predicted ineligible listings. Its results applied only
to fresher eligibility, not role, city, experience level, or employment type.
They are historical and are not an evaluation of the current 50-row sample.
