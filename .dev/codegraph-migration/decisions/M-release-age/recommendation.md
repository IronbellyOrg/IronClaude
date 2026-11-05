# Recommendation: M-b minimum release age before bumping

- Decision: M-release-age (M-b). Before the monitor bumps the codegraph pin, how old must a release be, and what does the monitor do when the newest release is too young?
- Method: `/sc:adversarial --compare option-a.md,option-b.md,option-c.md --depth quick --focus "fit with the user's two-week rule,exposure to pulled or quickly patched releases,lag on security fixes,testability offline"`. The run had one advocate per option, one debate round, two independent scoring passes (forward and reverse order), and a merge.
- Status: DONE. Pipeline status success, converged, 0 unresolved conflicts.
- Artifacts:
  - `adversarial/merged-output.md` (the merged rule)
  - `adversarial/adversarial/` (diff analysis, debate transcript, base selection, refactor plan, merge log, return contract)

## Winner and the rule to implement

The winner is a merge built on Option B (base), with the no-fallback rule taken from Option C. The monitor waits 14 days for the newest release and never falls back to an older one. On each run it looks at the highest semver release newer than the pin. It bumps to that release only once the release is at least 14 days old. If the release is younger, the run does nothing and reports what it is waiting for. A person can shorten the wait for one manual run, for example for a security fix.

- **Age constant:** `MIN_AGE_DAYS = 14`, one constant in the bump script. A release is eligible when `now_utc - published_at >= MIN_AGE_DAYS * 86400` seconds. The boundary is inclusive and measured in exact seconds.
- **Candidate set:** start from the full release list. Drop drafts, prereleases, tags that do not parse as semver, and releases without `published_at`. Keep only releases strictly newer than the pin by semver. Order by semver, never by date. Never use the `releases/latest` endpoint or flag.
- **Candidate pick:** the highest-semver release in the set. If it is younger than `MIN_AGE_DAYS`, do nothing this run. Never fall back to an older eligible release.
- **Major lines (depends on M-a):** if M-a handles majors separately from minors and patches (M-a options B or C), run the rule separately for releases within the pinned major and for releases with a higher major. A pending major never blocks minor or patch bumps. The higher-major candidate goes to the M-a path once it passes the same 14-day rule. If M-a treats majors like minors, use one set.
- **Manual override:** the `workflow_dispatch` input `min_age_days` must be a whole number, 0 or more. Any other value fails the run before any download. Scheduled runs always use `MIN_AGE_DAYS`. The override changes only the age. The pick (still no fallback), hash checks, attestation, proof and human merge stay the same. The run summary and the PR body record that the override was used and its value.
- **Reporting:** the run summary names the newest release that is waiting and the UTC date and time it becomes eligible. It adds a stall warning when the oldest release newer than the pin is at least 28 days old (`2 * MIN_AGE_DAYS`) and the run bumps nothing. The check runs per set when the sets are split, and a major handed to the M-a path counts as acted on. Reporting never changes the pick.
- **Pulled and re-tagged releases:** a deleted and re-created release gets a new `published_at`, so its clock restarts. A deleted release drops out of the set on the next run.
- **Tests (offline):** write the selection as a pure function of (release list JSON, now, pin, min age, major policy). It returns the candidate or none, plus a reason. Tests use fixture JSON and a fixed clock and must cover:
  - 14 days minus 1 second, exactly 14 days, and 14 days plus 1 second
  - an empty list, and a list with nothing newer than the pin
  - a list of only drafts or prereleases
  - a backport published after a higher version
  - a re-created release
  - override 0
  - a pending major alongside an eligible minor
  - the 2026 replay: with the pin below 1.3.0 and daily runs, the expected bumps are 08-04 to 1.5.0, 09-09 to 1.6.0, and 10-17 to 1.6.2

Today (2026-10-30) the pin is 1.6.2, which is the newest release, so this rule bumps nothing.

## Why

- It matches the user's two-week rule. All three advocates agreed on 14 days.
- Waiting for the newest release keeps patched releases out. In the 2026 replay, Option B's fallback would have bumped to 1.3.0 on 07-21 and to 1.6.1 on 10-13, after their patches already existed. The merged rule never picks a release that upstream has already patched.
- The proof checks the tool list and the registration shape, not tool semantics, and a merged pin reaches every workspace. So "the proof plus the human merge" (Option A) does not cover this risk. Option A's own advocate conceded this.
- The override covers security fixes without weakening the default.

## Scores per option

| Option | Quantitative (50%) | Qualitative (50%, of 30) | Combined | Debate points won |
|---|---|---|---|---|
| A: no minimum age | 0.771 | 18 (0.600) | 0.685 | 0 |
| B: 14 days, newest eligible (base) | 0.972 | 20 (0.667) | **0.819** | 6.5 |
| C: 7 days, latest only | 0.913 | 21 (0.700) | 0.806 | 2.5 |

B and C were within 5% of each other, so the tiebreaker on debate points decided the base: B won 6.5 to 2.5. C's no-fallback rule then replaced B's fallback in the merge.

## Convergence

- 14 of 14 diff points agreed (100%, threshold 80%). 12 were unanimous; 2 were decided 2 to 1.
- All three taxonomy levels were covered. The invariant probe was skipped because the depth was quick.
- Status: CONVERGED.

## Flagged for the user

1. **Source of the two-week rule.** The rule was stated by the coordinator. The closest rule found on disk is the harness rule that script versions must be at least two weeks old. If the user meant a different number, only `MIN_AGE_DAYS` changes.
2. **No fallback was a 2-to-1 vote.** Option B's advocate preferred a different rule: keep the fallback, but skip any release that already has a newer patch on the same major.minor line. That rule bumps more often when releases come close together; in July it would have added 1.3.1 and 1.4.1. It is recorded as the alternative if the stall warning fires often in practice.
3. **Major-line split depends on M-a.** It applies only if M-a handles majors separately (M-a option B, an issue, or option C, a draft PR). Under M-a option A, there is one set, and an unmerged major PR holds back later minors until a person merges or closes it.
4. **Open PR for a deleted release.** What happens to an already-open bump PR whose release upstream deletes is not decided here. It needs an owner, possibly the M-proof-failure decision.
5. **Confirm the timestamp field.** This run did not check GitHub's docs. The implementer should confirm that the release `published_at` field is the publish time, as opposed to `created_at`, before relying on it.
