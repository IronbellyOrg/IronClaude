# Merge Log

## Metadata

- Base: Variant 2 (Option B, original), `adversarial/variant-2-original.md`
- Sources: Variant 3 (Option C), Variant 1 (Option A), shared assumptions A-001 to A-006 from the debate
- Plan: `adversarial/refactor-plan.md` (8 planned changes, 4 rejected)
- Executor: merge-executor (sc:adversarial Step 5)
- Output: `merged-output.md` (38 lines)
- Changes applied: 8 of 8
- Status: COMPLETE, with 2 ambiguities reported to the orchestrator (see Contradiction rescan)
- Timestamp: 2026-10-30

## Changes Applied

### Change 1: Replace B's fallback with C's no-fallback rule
- Status: applied
- Before: "If the newest release is younger, the monitor may still bump to an older release that is eligible ..."
- After: "Candidate = the highest-semver release in the candidate set (in each set, when split by major line). If it is younger than `MIN_AGE_DAYS`, the run does nothing and never falls back to an older eligible release." The Base rationale's "the eligible release is the settled one" was replaced with the replay evidence (1.3.0 on 07-21, 1.6.1 on 10-13).
- Provenance tag: `Variant 3, Change 1`; rationale tagged `Base (original, modified), Change 1`
- Validation: the old fallback wording is gone from the document; no other bullet still allows an older pick.

### Change 2: Define the candidate set precisely
- Status: applied
- Before: "the newest non-draft, non-prerelease release that is newer than the pin"
- After: full release list minus drafts, prereleases, non-semver tags and releases without `published_at`; strictly newer than the pin by semver; ordered by semver; `releases/latest` endpoint and flag never used.
- Provenance tag: `Base (original, modified), Changes 2 and 3`
- Validation: all four filters, the semver ordering and the `releases/latest` ban are present.

### Change 3: Define the age boundary exactly
- Status: applied
- Before: "published at least 14 days before the run"
- After: eligible when `now_utc - published_at >= MIN_AGE_DAYS * 86400` seconds (inclusive); `MIN_AGE_DAYS = 14` kept as one constant in the bump script.
- Provenance tag: shared with Change 2 (same bullet)
- Validation: inclusive comparison and constant both stated once.

### Change 4: Add a stall warning to the run summary
- Status: applied
- Before: reporting clause inside Base bullet 2 ("the run summary says which newer release is waiting and when it becomes eligible")
- After: separate "Reporting" bullet: names the newest waiting release and its UTC eligibility date and time; stall warning when the oldest release newer than the pin is at least `2 * MIN_AGE_DAYS` (28) days old and the run bumps nothing; reporting only.
- Provenance tag: `Base (original, modified), Change 4`
- Validation: fixes Clar-3 (rule and reporting no longer mixed in one bullet).

### Change 5: Split the candidate set by major line according to M-a
- Status: applied
- Before: none (single set)
- After: new "Major lines" bullet after the candidate-set bullet: two sets when M-a keeps majors off the automated PR path; a pending major never blocks minor or patch bumps; the higher-major set goes to M-a handling once its candidate passes the 14-day rule; one set if M-a treats majors like minors; flagged for the user.
- Provenance tag: `Shared assumption A-005, Change 5`
- Validation: placed after bullet 1 as planned. The candidate bullet (Change 1) says "in each set, when split by major line" so the two bullets read consistently.

### Change 6: Tighten the manual override
- Status: applied
- Before: "`workflow_dispatch` input `min_age_days` overrides it for a manual run (for example a security fix)."
- After: whole number 0 or more, else fail before any download; scheduled runs always use `MIN_AGE_DAYS`; override changes only the age (same pick with no fallback, hash checks, attestation, proof, human merge); run summary and PR body record its use and value.
- Provenance tag: `Base (original, modified), Change 6`
- Validation: security-fix use moved to the Rationale bullet ("Security fixes go through the override").

### Change 7: State the pulled and re-tagged release behavior
- Status: applied
- Before: none in Base (only Variant 1's cost bullet mentioned it)
- After: three bullets under `## Edge cases and tests`: re-created release restarts the 14-day clock; deleted release drops out on the next run; open PR for a deleted release is out of scope and flagged for the user.
- Provenance tag: `Variant 1, Change 7`
- Validation: matches the plan's three points; no handling for the open PR was invented.

### Change 8: Add offline test cases
- Status: applied
- Before: Base cost "one more date comparison to test"
- After: pure function of (release list JSON, now, pin, min age, major policy) returning candidate or none plus a reason; fixture JSON, fixed clock, no network; all 8 listed cases, including the 2026 replay (pin below 1.3.0, daily runs: 08-04 1.5.0, 09-09 1.6.0, 10-17 1.6.2). Cost bullet now says "More test cases than a single date comparison."
- Provenance tag: `Shared assumption A-006, Change 8`; cost tagged `Base (original, modified), Changes 1, 4 and 8`
- Validation: replay expectation matches the orchestrator check in `debate-transcript.md`.

## Post-Merge Validation

### Structural integrity
- Headings: one H1 (title), one H2 (`## Edge cases and tests`). No skipped levels, no orphaned or empty sections.
- Order matches the input style: rule bullets, then Rationale, then Cost, then the edge-case section.
- Provenance: 3 header comments plus 9 `Source:` tags; every bullet or bullet block has one.
- Style: 0 em dashes, 0 emojis, 38 lines (within the 25 to 45 target).

### Internal references
- Total: 12 kinds of reference checked; resolved: 12; broken: 0.
  - `MIN_AGE_DAYS` (5 uses): defined once as `= 14` in bullet 1; every other use refers to it.
  - `M-a` (5 uses): refers to the separate major-version decision (`decisions/M-major-versions/`); stated as pending and flagged.
  - `published_at`, `releases/latest`, `workflow_dispatch` / `min_age_days`, `2 * MIN_AGE_DAYS` (28), "candidate set", "each set", "override 0", "pending major", "re-created release", "2026 replay": each used term is defined in the rule bullets or matches a listed test case.

### Contradiction rescan
- No-fallback rule vs stall warning: no contradiction. The warning is reporting only and never changes the pick.
- No-fallback rule vs override: no contradiction. The override changes only the age and keeps the same pick with no fallback.
- No-fallback rule vs major-line split: no contradiction. The pick runs per set, and a pending major cannot block the in-major set.
- Override vs major-line split: no contradiction. The override changes only the age, so it applies the same way to each set.
- Ambiguity 1 (not a contradiction, reported, not resolved): the plan does not say whether the stall warning is checked per set. In split mode, a higher-major release held by the M-a handling for 28 days or more could be "the oldest release newer than the pin" and trigger the warning on runs where the in-major set has nothing to bump. The orchestrator or the user should decide whether the stall check uses only the in-major set.
- Ambiguity 2 (wording accuracy, reported): the 2026 example gap (07-07 to 08-04) is exactly 28 days, so the 28-day warning would reach its threshold on 08-04, the same day 1.5.0 is bumped, and would not fire in that example. The Cost bullet therefore says the stall warning "surfaces long waits" rather than claiming it fired in the example.
- Title note: the title's "latest candidate only" means the highest-semver candidate, not the `releases/latest` flag; bullet 1 states that explicitly, so there is no conflict.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 8 | 8 | 0 | 0 |

Rejected changes (C-001, C-004/A-003, C-002 minority, X-001) were not applied, as the plan says. Two ambiguities are reported for the orchestrator; no new content was added to resolve them.

## Orchestrator Resolution (2026-10-30, non-interactive default)

- Ambiguity 1: resolved. The stall check runs per set. A higher-major candidate handed to the M-a path counts as acted on, not stalled. This follows the debate intent for A-005: a pending major must not affect the in-major line, and the warning stays reporting only. One sentence was added to the Reporting bullet of `merged-output.md`; its provenance stays under the existing Change 4 tag.
- Ambiguity 2: accepted as written ("the stall warning surfaces long waits"). The executor's check is correct: the 28-day threshold is reached on the same day 1.5.0 would be bumped.
- Final status: merge complete. Validation is still clean after the edit: the new sentence references M-a and "set", both defined, and introduces no contradiction.
