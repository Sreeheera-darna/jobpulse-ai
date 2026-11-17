
# JobPulse AI — Manual Audit Results

## Audit methodology

A sample of 50 India-based job listings was manually reviewed.
The sample included all 15 AI-predicted fresher-eligible listings
and 35 randomly selected listings predicted as ineligible.

Human reviewers checked the job descriptions and assigned:
- Human experience level
- Human fresher eligibility
- Audit notes explaining the decision

## Fresher eligibility results

| Metric | Result |
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

## Observations

The classifier identified all 12 human-confirmed eligible
listings in the audited sample.

Three false positives were identified:
- Field Operations Executive
- QA Interns || Robotics
- Trainer Intern

These cases demonstrate why job descriptions must be checked
rather than relying only on titles or internship labels.

## Limitations

This is a targeted sample containing every AI-positive listing
and a random sample of AI-negative listings. It is not a
representative random sample of the entire dataset.

The metrics evaluate fresher eligibility only. They do not
measure city or role-category accuracy.
