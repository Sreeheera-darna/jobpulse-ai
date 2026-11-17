# JobPulse AI — AI Tools and Prompts

## AI tools used

| Tool | Purpose |
|---|---|
| ChatGPT | Development guidance, debugging, architecture planning and documentation |
| Google Gemini API | Job description classification |
| GitHub Copilot / VS Code (if used) | Code assistance |
| GitHub Actions | Automated daily job collection and classification |

## Gemini classification

Model: gemini-3.5-flash-lite

Purpose:
Classify India-based job listings based on their descriptions.

Output fields:
- role_category
- city
- experience_level
- employment_type
- is_fresher_eligible
- confidence

## Classification prompt

You are a job listing classification assistant.

Analyze the supplied job title, location and description.

Return structured JSON containing:

- role_category: The most appropriate job category.
- city: The city where the job is located.
- experience_level: Fresher, Entry-level, Experienced or Unknown.
- employment_type: Full-time, Internship, Contract or Unknown.
- is_fresher_eligible: Boolean.
- confidence: Confidence score between 0 and 1.

Rules:

1. Use the job description as the primary source of truth.
2. Mark fresher eligibility as true only when the description
   explicitly supports recent graduates, fresh graduates,
   entry-level applicants or candidates without prior experience.
3. Internship roles are eligible only when the description
   supports students or internship-eligible candidates.
4. Do not assume that a role is fresher-friendly just because
   its title contains the word "Intern".
5. If eligibility is unclear, classify it as false.
6. Do not invent missing information.
7. Return only structured output matching the required schema.

## Manual audit

A sample of 50 listings was manually reviewed.

The sample included:
- All 15 AI-predicted fresher-eligible listings.
- 35 randomly selected AI-predicted ineligible listings.

Results:
- Accuracy: 94.00%
- Precision: 80.00%
- Recall: 100.00%
- F1 score: 88.89%

These metrics evaluate fresher eligibility, not city or
role-category classification.

## Cost estimation

A test classification used:
- Input tokens: 1,664
- Output tokens: 66

Estimated cost for 1,000 similar classifications:
Approximately $0.66, using the pricing assumptions documented
in backend/COST_ESTIMATE.md.

Actual cost depends on the applicable Gemini model pricing
and token usage.