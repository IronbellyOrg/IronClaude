# CI Poll (Wave 8) — the checks poller contract

This ref pins the CI poll surface for the SKILL's attended, in-session poll loop. The poll **script**
(`scripts/poll-ci-checks.sh`) performs a single `gh` poll and emits one JSON line;
`superclaude.pr_submit.ci.classify_checks` is the authoritative classifier. This
split keeps `gh` out of the deterministic core (NFR-6).

> Every `gh` call below pins the RESOLVED `--repo <owner/repo>` (origin's
> `owner/repo`, parsed from `git remote get-url origin`; FR-1.3 / AC-7). A bare
> `gh` without `--repo` is a defect.

## Poll surfaces (FR-CI-2 / FR-CI-10 / FR-CI-11)

```bash
gh pr view <N> --repo <owner/repo> --json number,url,headRefOid
gh pr checks <N> --repo <owner/repo> --required --json name,state,bucket,link,workflow
# if that list is empty, fall back to:
gh pr checks <N> --repo <owner/repo> --json name,state,bucket,link,workflow
```

No `conclusion` field — `gh pr checks --json` does not emit it. Empty, malformed, or multiple-document stdout is **not** a parsed empty array. A valid nonempty required list takes precedence; otherwise a valid all-checks list is used. If the chosen list is empty and either query failed to parse, emit `state:polling`, `checks:[]`; only two parsed empty arrays, with `expect_checks` false, justify `clean`; with `expect_checks` true an empty chosen list is `polling` (see Expected checks after a push). Pending exit 8 may still contain valid JSON — keep it.

## Wave 8 entry (SKILL-owned, not an FSM edge)

| Augment outcome | CI wait | CI fix |
|-----------------|---------|--------|
| `clean` / `REPORT_ONLY` | Arm; reset elapsed | Only while `round_counter < max_rounds` |
| `HALT_MAX_ROUNDS` | Arm, wait-only; report CI clean, failure, timeout, or human-gate alongside retained Augment halt | No: CI findings → `REPORT_ONLY` (the one Tier 1 sync push of Wave 8a is the only push allowed here, and it is not a fix) |
| `TERMINAL_AUGMENT_NO_RESPONSE` | Arm, wait-only; retain Augment status; report CI alongside. Never `transition(clean)` | No (the one Tier 1 sync push excepted) |
| `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` / `TERMINAL_FAILED` / L0 | Do not arm | No |

When the PR is still conflicting and no merge commit was pushed, the SKILL skips the CI wait with reason `pr_conflicting`: GitHub runs no `pull_request` checks on a conflicting PR, so the lists would read empty.

The wait consumes no remediation round. A `polling` result (including a failed check query) continues at the configured interval until completion or `--timeout`. A non-zero script exit (e.g. `gh` without `pr checks --json`) is not `polling`: stop and report the missing prerequisite. The observed CI matrix has run longer than the 600s default, so a CI wait needs a `--timeout` sized to the full check run; never promise an indefinite wait. When `--required` returns a nonempty parsed list it is the chosen set; otherwise use the parsed all-checks list. Optional checks outside the chosen set do not block completion.

- `headRefOid` = the head SHA. If it differs from the SHA this wait started on,
  `classify_checks(..., wait_sha=...)` returns `polling`.
- `--required` first; empty → all checks. That is the optional-check filter.
  Do not special-case any check by name.

`bucket` values: `pass` | `fail` | `pending` | `skipping` | `cancel`.

## Log fetch (SKILL, only after non-human findings)

```bash
gh run view <RUN_ID> --repo <owner/repo> --log-failed
```

`RUN_ID` parsed from `checks[].link` (`/actions/runs/(\d+)`). Missing link →
unparseable (no Finding; SKILL `REPORT_ONLY`).

## Expected checks after a push (`expect_checks`)

Right after a push the new head has no checks yet, so an empty list must not read as `clean`
when the repository has checks. The SKILL sets `expect_checks` once per push with
`superclaude.pr_submit.ci.expect_checks_after_push` and records it on the push records, so
`--resume` reuses it. Evidence for the replaced head and the base tip is commit-scoped:

```bash
scripts/poll-ci-checks.sh --evidence-sha <sha> --repo <owner/repo>
gh api repos/<owner/repo>/commits/<sha>/check-runs --jq .total_count
gh api repos/<owner/repo>/commits/<sha>/status --jq .total_count
```

The script runs the two reads and prints `{"evidence_sha": "<sha>", "evidence_checks": <n>, "source": "ci"}`,
with `n = -1` on a failed or unparsable read. `-1` counts as having checks (fail closed). Only when
checks were not seen earlier in the run and both evidence reads are 0 is an empty list `clean`. With
`expect_checks` true, expiry is the existing Wave 8 CI timeout with reason `ci_not_started`; it is
never `clean` and the report never says tests passed.

## Division of labour

- The **poll script** does one poll and returns a coarse `state` plus the raw
  `checks` array. It performs no arithmetic and holds no state.
- **`classify_checks`** maps buckets to `polling` / `clean` / `findings`.
- The **SKILL** owns `source=ci`, the wait-clock reset, human-gate →
  `HALT_HUMAN` only before Augment halts (otherwise report alongside the
  preserved halt), unparseable → `REPORT_ONLY`, and skipping S5a / S6 /
  RESOLVING after a CI-phase push.

<!--mc:threads:begin-->
<!--mc:rev {"ts":"2026-09-25T00:05:16.296Z","contentHash":"5a834620","sections":[{"heading":"CI Poll (Wave 8) — the checks poller contract","hash":"0fbef092"},{"heading":"Poll surfaces (FR-CI-2 / FR-CI-10 / FR-CI-11)","hash":"3ab2b3db"},{"heading":"if that list is empty, fall back to:","hash":"3462eeca"},{"heading":"Wave 8 entry (SKILL-owned, not an FSM edge)","hash":"e65512ab"},{"heading":"Log fetch (SKILL, only after non-human findings)","hash":"79b3e33e"},{"heading":"Division of labour","hash":"2fd691ab"}]}-->
<!--mc:threads:end-->
