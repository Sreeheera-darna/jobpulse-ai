# JobPulse AI — Data Sources

JobPulse uses public ATS job-board APIs and links each result to the employer's
original job listing. It does not use applicant data.

## Greenhouse

API: `https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs`

Configured boards: Stripe (`stripe`), Twilio (`twilio`), GitLab (`gitlab`),
Rubrik (`rubrik`), Elastic (`elastic`), Okta (`okta`), Pure Storage
(`purestorage`), MongoDB (`mongodb`), Anthropic (`anthropic`), Fivetran
(`fivetran`), Netskope (`netskope`), InMobi (`inmobi`), DevRev (`devrev`),
Coinbase (`coinbase`), Druva (`druva`), Airbnb (`airbnb`), and Instawork
(`instawork`).

## Lever

API: `https://api.lever.co/v0/postings/{board_token}?mode=json`

Configured boards: 100ms, Acceldata, CRED, Hevo Data, Meesho, Mindtickle,
Level AI, Mactores, Nium, Onit, Shield AI, ShyftLabs, Sonatype, Sophos,
TTEC Digital, and Turvo. Board identifiers are configured in
`backend/collect_jobs.py`.

## Ashby

API: `https://api.ashbyhq.com/posting-api/job-board/{board_token}`

Configured boards: AiPrise (`aiprise`), Atlan (`atlan`), Atlys (`atlys`),
Sarvam AI (`sarvam`), and Snowflake (`snowflake`).

## Collection and limitations

1. Fetch currently published postings from configured boards.
2. Normalize locations and descriptions, then deduplicate by normalized
   job URL.
3. Keep listings whose posted location identifies India.
4. Classify job description fields with Gemini.
5. Save listing data and classifications as JSON.

The collectors use public ATS endpoints without bypassing authentication or
access controls. No LinkedIn or Naukri pages are scraped. Public availability
does not imply that every listing is suitable for freshers; eligibility is
classified separately and ambiguous cases are not assumed eligible. Board
availability, API behavior, and live postings can change, so the dataset is
a daily snapshot rather than a guarantee that every employer link remains open.