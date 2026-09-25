# CI Poll (Wave 8) — the checks poller contract

This ref pins the CI poll surface for the in-session Monitor. The poll **script**
(`scripts/poll-ci-checks.sh`) performs a single `gh` poll and emits one JSON line;
`superclaude.pr_submit.ci.classify_checks` is the authoritative classifier. This
split keeps `gh` out of the deterministic core (NFR-6).

> Every `gh` call below pins the RESOLVED `--repo <owner/repo>` (origin's
> `nameWithOwner`, FR-1.3 / AC-7). A bare `gh` without `--repo` is a defect
> (T-104 greps for it).

## Poll surfaces (FR-CI-2 / FR-CI-10 / FR-CI-11)

```bash
gh pr view <N> --repo <owner/repo> --json number,url,headRefOid
gh pr checks <N> --repo <owner/repo> --required --json name,state,bucket,link,workflow
# if that list is empty, fall back to:
gh pr checks <N> --repo <owner/repo> --json name,state,bucket,link,workflow
```

No `conclusion` field — `gh pr checks --json` does not emit it. Empty, malformed, or multiple-document stdout is **not** a parsed empty array. A valid nonempty required list takes precedence; otherwise a valid all-checks list is used. If the chosen list is empty and either query failed to parse, emit `state:polling`, `checks:[]`; only two parsed empty arrays justify `clean`. Pending exit 8 may still contain valid JSON — keep it.

## Wave 8 entry (SKILL-owned, not an FSM edge)

| Augment outcome | CI wait | CI fix |
|-----------------|---------|--------|
| `clean` / `REPORT_ONLY` | Arm; reset elapsed | Only while `round_counter < max_rounds` |
| `HALT_MAX_ROUNDS` | Arm, wait-only; report CI clean, failure, timeout, or human-gate alongside retained Augment halt | No: CI findings → `REPORT_ONLY` |
| `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` / `TERMINAL_FAILED` / L0 | Do not arm | No |

The wait consumes no remediation round. A `polling` result (including a failed check query) continues at the configured interval until completion or `--timeout`. When `--required` returns a nonempty parsed list it is the chosen set; otherwise use the parsed all-checks list. Optional checks outside the chosen set do not block completion.

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
