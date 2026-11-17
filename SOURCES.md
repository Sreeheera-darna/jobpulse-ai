# JobPulse AI — Data Sources

## Primary data source

JobPulse AI collects job listings from publicly accessible
Greenhouse Job Board APIs.

API format:
https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs

The collector requests job descriptions and listing details
using the public job board endpoint.

## Configured company boards

| Company | Greenhouse Board Token |
|---|---|
| Stripe | stripe |
| Twilio | twilio |
| GitLab | gitlab |
| Rubrik | rubrik |
| Elastic | elastic |
| Okta | okta |
| Pure Storage | purestorage |
| MongoDB | mongodb |
| Anthropic | anthropic |
| Fivetran | fivetran |
| Netskope | netskope |
| InMobi | inmobi |
| DevRev | devrev |
| Coinbase | coinbase |
| Druva | druva |
| Airbnb | airbnb |
| Instawork | instawork |

## Data collection process

1. Fetch listings from configured Greenhouse boards.
2. Normalize job titles and location fields.
3. Remove duplicate listings using job URLs.
4. Filter listings whose locations identify India.
5. Save the collected listings as JSON.
6. Classify job descriptions using an LLM.

## Responsible data collection

- Uses publicly accessible job board endpoints.
- Does not bypass authentication or access controls.
- Does not scrape LinkedIn or Naukri.
- Does not collect applicant personal information.
- Job descriptions and application links remain attributable
  to their original employers.

## Limitations

- The available listings depend on each company's live job board.
- Not every India-based listing is suitable for fresh graduates.
- A job's eligibility must be checked against its description.
- The dataset is a snapshot and may change as employers update
  or remove vacancies.