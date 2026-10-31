# Option B: 14 days minimum, newest eligible release wins

- Candidate = the newest non-draft, non-prerelease release that is newer than the pin AND published at least 14 days before the run (`MIN_AGE_DAYS = 14`, one constant in the bump script).
- If the newest release is younger, the monitor may still bump to an older release that is eligible (for example 1.7.0 at 20 days while 1.7.1 is 3 days old); the run summary says which newer release is waiting and when it becomes eligible.
- `workflow_dispatch` input `min_age_days` overrides it for a manual run (for example a security fix).
- Rationale: matches the user's two-week rule; upstream's own quick fixes usually land within days, so the eligible release is the settled one.
- Cost: a two-week lag on fixes; one more date comparison to test.
