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

No `conclusion` field — `gh pr checks --json` does not emit it.

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
  `HALT_HUMAN`, unparseable → `REPORT_ONLY`, and skipping S5a / S6 / RESOLVING
  after a CI-phase push.
