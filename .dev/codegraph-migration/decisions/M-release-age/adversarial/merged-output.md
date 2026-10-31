<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (Option B, original) -->
<!-- Merge date: 2026-10-30 -->

# Merged option: 14 days minimum, latest candidate only, no fallback

<!-- Source: Base (original, modified), Changes 2 and 3: candidate set and age boundary defined exactly (shared assumptions A-001 to A-004) -->
- Candidate set = the full release list, minus drafts, minus prereleases, minus tags that do not parse as semver, minus releases without `published_at`, keeping only releases strictly newer than the pin by semver. Order by semver, never by date. Never use the `releases/latest` endpoint or flag. A release is eligible when `now_utc - published_at >= MIN_AGE_DAYS * 86400` seconds (inclusive), with `MIN_AGE_DAYS = 14` as one constant in the bump script.
<!-- Source: Shared assumption A-005, Change 5: major-line split, depends on the M-a decision -->
- Major lines: if the M-a decision handles majors separately from minors and patches (M-a options B or C), the age rule runs separately on two sets: releases within the pinned major, and releases with a higher major. A pending major never blocks minor or patch bumps. The higher-major set goes to the M-a handling once its own candidate passes the same 14-day rule. If M-a treats majors like minors, there is one set. Flagged for the user until M-a is decided.
<!-- Source: Variant 3, Change 1: no-fallback rule replaces Base bullet 2 -->
- Candidate = the highest-semver release in the candidate set (in each set, when split by major line). If it is younger than `MIN_AGE_DAYS`, the run does nothing and never falls back to an older eligible release.
<!-- Source: Base (original, modified), Change 4: reporting split out of Base bullet 2; stall warning from Variants 1 and 3 -->
- Reporting: the run summary always names the newest release that is waiting, and the UTC date and time it becomes eligible. It adds a stall warning when the oldest release newer than the pin is at least `2 * MIN_AGE_DAYS` (28) days old and the run still bumps nothing. When the sets are split by major line, the check runs per set, and a higher-major candidate handed to the M-a path counts as acted on, not stalled. Reporting only; it never changes the pick.
<!-- Source: Base (original, modified), Change 6: override input validated, scoped and recorded -->
- Manual override: `workflow_dispatch` input `min_age_days`, a whole number, 0 or more. Any other value fails the run before any download. Scheduled runs always use `MIN_AGE_DAYS`. The override changes only the age; the candidate pick (no fallback), hash checks, attestation, proof and human merge stay the same. The run summary and the PR body record that the override was used, and its value.
<!-- Source: Base (original, modified), Change 1: "settled release" claim replaced with replay evidence -->
- Rationale: matches the user's about-two-weeks rule. Waiting for the newest release instead of falling back means a release that upstream patched within days is never picked: in the 2026 replay a fallback would have bumped to 1.3.0 on 07-21 and to 1.6.1 on 10-13, after their patches existed. Security fixes go through the override.
<!-- Source: Base (original, modified), Changes 1, 4 and 8: lag, starvation and test cost -->
- Cost: about 14 days of lag on fixes unless a person runs the override. A release train with gaps under 14 days delays bumps (example: no bump from 07-07 to 08-04 in the 2026 history); the stall warning surfaces long waits. More test cases than a single date comparison.

## Edge cases and tests

<!-- Source: Variant 1, Change 7: pulled and re-tagged releases -->
- A deleted and re-created release gets a new `published_at`, so its 14-day clock restarts.
- A deleted release drops out of the candidate set on the next run.
- What to do with an already-open bump PR whose release was deleted is out of scope here. It is flagged for the user.
<!-- Source: Shared assumption A-006, Change 8: offline pure-function tests -->
- The selection logic is a pure function of (release list JSON, now, pin, min age, major policy) that returns the candidate or none, plus a reason. Tests use saved fixture JSON and a fixed clock, with no network.
- Required cases:
  - the boundary at 14 days minus 1 second, exactly 14 days, and 14 days plus 1 second;
  - an empty list, and a list with nothing newer than the pin;
  - a list where everything is a draft or a prerelease;
  - a backport published after a higher version;
  - a re-created release;
  - override 0;
  - a pending major alongside an eligible minor;
  - the 2026 replay: with the pin below 1.3.0 and daily runs, the expected bumps are 08-04 1.5.0, 09-09 1.6.0 and 10-17 1.6.2.
