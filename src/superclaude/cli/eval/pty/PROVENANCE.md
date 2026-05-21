# ptytest — Vendored Fork Provenance

This file records the upstream source, fork SHA pin, vendoring metadata, and the
drift-review policy for the `ptytest` sources vendored under
`src/superclaude/cli/eval/pty/`. The mechanism that closes OQ-4 (top-level
`NOTICE`) is recorded in `decisions.md` D-10 and reproduced in the repository
`NOTICE` file at the project root.

## 1. Upstream identity

| Field | Value |
|-------|-------|
| Upstream repository | https://github.com/brandon-fryslie/ptytest |
| Upstream license | MIT (verbatim copy retained at `src/superclaude/cli/eval/pty/LICENSE`) |
| Fork posture | Vendored + owned; no upstream pull-back path (per D-1) |

## 2. Fork SHA pin (NFR-MAINT1 + AC10)

| Field | Value |
|-------|-------|
| Pinned upstream SHA | `61a46870e38710c7cfc95f00cefbf0499111aa5f` |
| Pinned short SHA | `61a4687` |
| Upstream commit date | 2025-12-21 |
| Vendoring date | TBD — set by T02.01 on physical landing of sources |
| Vendoring commit | TBD — set by T02.01 |
| `pexpect` floor | `pexpect>=4.9` (pinned via vendored module imports per NFR-MAINT1) |
| Local changes from upstream | TBD — enumerated by T02.01 in the `Changes` section below on landing |

The SHA above is captured at T02.03 authoring time from
`GET https://api.github.com/repos/brandon-fryslie/ptytest/commits/master` on
2026-05-20. T02.01 MUST either confirm this SHA as the vendoring target or
update this section in the same commit that lands the sources, so the pin and
the on-disk content are byte-aligned.

### Changes from upstream

*(Populated by T02.01 when the vendored sources land. Format: bullet list of
files changed + 1-line rationale per file.)*

- TBD

## 3. Drift-review policy (AC10)

| Field | Value |
|-------|-------|
| Review cadence | **Quarterly** |
| Next review due | 2026-08-20 *(initial cadence anchor; rolls forward every 90 days)* |
| Review owner | **RyanW** *(maintainer; per roadmap risk register)* |
| Review procedure | See `CHECKLIST.md` in this directory |
| Out-of-band trigger | Any CVE against `pexpect` or `ptytest` upstream; any upstream commit that touches the prompt-detection or ANSI-stripping code paths |

A review is a *re-verification* of the pinned SHA against upstream, not a
mandatory resync. The default outcome of a clean review is to bump
`Next review due` by 90 days and leave the pin unchanged. A resync is performed
only when the checklist surfaces a security-relevant or behavior-relevant
upstream change.

### Resync procedure (when a review concludes resync is warranted)

1. Open a tracked task referencing this PROVENANCE entry and the upstream
   diff range (`<pinned-sha>..<new-sha>`).
2. Update the SHA pin + vendoring date + commit + `Changes from upstream`
   section in §2 in the same commit that lands the new sources.
3. Re-verify the canonical attribution clause in the top-level `NOTICE`
   against any upstream LICENSE text changes; update both `NOTICE` and the
   D-10 ADR body in `decisions.md` if the clause moved.
4. Re-run `tests/cli/eval/test_pty_vendor.py` and the full
   `tests/cli/eval/test_pty_driver.py` / `test_pty_stream.py` suites.
5. Record the review (or resync) outcome in §4 below.

## 4. Review log

| Date | Reviewer | Upstream SHA at review | Outcome | Notes |
|------|----------|------------------------|---------|-------|
| 2026-05-20 | RyanW (T02.03 authoring) | `61a46870e38710c7cfc95f00cefbf0499111aa5f` | Pin established | Initial SHA selection; cadence anchor set to 2026-08-20. |

## 5. Cross-references

- `NOTICE` (repo root) — attribution clause; D-10 ADR mirror.
- `.dev/releases/current/cliEval/decisions.md` §D-1 — fork-vs-build decision.
- `.dev/releases/current/cliEval/decisions.md` §D-10 — NOTICE/LICENSE attribution closure of OQ-4.
- `.dev/releases/current/cliEval/artifacts/D-0023/` — T02.01 vendoring deliverable.
- `.dev/releases/current/cliEval/artifacts/D-0024/` — T02.02 NOTICE/LICENSE attribution deliverable.
- `.dev/releases/current/cliEval/artifacts/D-0025/` — T02.03 SHA pin + drift policy deliverable (this file's parent task).
- `CHECKLIST.md` (this directory) — the 5-step quarterly review procedure.
