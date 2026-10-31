# Option C: 7 days minimum, only the latest release

- Candidate = `releases/latest` only, bumped once it is at least 7 days old; if it is younger, do nothing this run (no fallback to an older eligible release).
- Rationale: shorter lag than two weeks while still skipping same-day re-releases.
- Cost: diverges from the user's two-week rule; a fast release train (a new patch every few days) can block bumping indefinitely because the latest is always young.
