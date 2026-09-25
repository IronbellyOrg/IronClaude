---
title: "Keep CI monitor active until all chosen checks complete"
status: merged-requirements
parent_spec: .dev/specs/pr-submit-ci-monitor.md
base: variant-2-sonnet-refactorer
convergence: 0.92
created: 2026-09-24
live_pr: https://github.com/IronbellyOrg/IronClaude/pull/237
---

<!-- Provenance: /sc:adversarial via /sc:brainstorm. Base: Variant 2 (refactorer). -->

# Keep CI monitor active until all chosen checks complete

## 1. Problem

`sc:pr-submit --monitor 3` on PR #237 exited while Test 3.10 / 3.11 / 3.12 were still `pending`. Two abort paths:

1. **Wait never armed.** Wave 8 starts only after Augment `clean` / `REPORT_ONLY`. `DEFAULT_MAX_ROUNDS=2` → `HALT_MAX_ROUNDS`. Shared `max_rounds` blocked *entry* to the wait (a wait consumes no round).
2. **Poller not fail-soft.** Empty `gh pr checks` stdout → `as_array` can yield empty → `--argjson req ""` dies under `set -e` (`poll-ci-checks.sh:47`).

`classify_checks` already maps `pending` → `polling`. That is not the bug.

## 2. Thesis: wait ≠ fix

| Job | Needs rounds? | `HALT_MAX_ROUNDS` should block? |
|-----|---------------|----------------------------------|
| Wait until chosen checks are not `pending` | No | **No** |
| Auto-fix parseable CI `findings` | Yes (FR-CI-8) | **Yes** |

<!-- Source: Variant 2 -->

## 3. Wave 8 arm table

| Augment terminal | Arm wait? | CI auto-fix (Waves 3–5)? |
|------------------|-----------|---------------------------|
| `TERMINAL_CLEAN` / `REPORT_ONLY` | Yes | If `round_counter < max_rounds` |
| `HALT_MAX_ROUNDS` | **Yes (wait-only)** | No — `findings` → `REPORT_ONLY` |
| `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` / `TERMINAL_FAILED` | No | No |
| L0 | No | No |

<!-- Source: Variant 1 entry table, merged per Change #1 -->

## 4. Functional requirements

| ID | Requirement |
|----|-------------|
| FR-W1 | Any `bucket=pending` in the chosen list → `classify_checks` = `polling`. Mix pass+pending = `polling` (pending wins). |
| FR-W2 | Wave 8 **wait** arms after Augment `clean`, `REPORT_ONLY`, **or** `HALT_MAX_ROUNDS`. Reset elapsed; swap to `poll-ci-checks.sh`. Do not `transition(clean)` until CI is not pending. |
| FR-W3 | Wait does **not** arm on `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` / `TERMINAL_FAILED`. L0 never Wave 8. |
| FR-W4 | After `HALT_MAX_ROUNDS`, wait-only: `polling` loops; `clean` → `transition(clean)`; human-gate → `HALT_HUMAN`; `findings` → `REPORT_ONLY` (no push). |
| FR-W5 | If `round_counter < max_rounds` at CI `findings`, existing FR-CI-8 auto-fix unchanged. No second counter. |
| FR-W6 | `poll-ci-checks.sh` always one JSON line, exit 0 on completed poll (usage still 2), including empty stdout, `gh` exit 8, non-array stdout. |
| FR-W7 | `--required` first; **parsed** empty array falls back to all. Unparsed / empty stdout is not a parsed empty array — do not skip fallback, do not `clean`. |
| FR-W8 | `checks=[]` is `clean` only when both required and all **parsed as JSON arrays** with length 0. Poller crash is never `clean`. |
| FR-W9 | Parse miss: script emits `state:"polling"` (and `checks:[]` only with that state). No new `EventType`. `classify_checks`: if payload `state=="polling"` and checks empty → `polling` (not FR-CI-4 clean). |
| FR-W10 | `--timeout` still resets at source flip. No `--ci-timeout` until 600s-after-reset is measured short. |

## 5. Non-goals

- New skill / FSM / `--monitor` / `EventType`
- `fsm.py`, `classifier.py`, `DetectionContract` edits
- `gh run rerun`; Codecov-by-name
- Separate CI round budget
- `--ci-timeout`

## 6. File delta (fewest)

| File | Change |
|------|--------|
| `scripts/poll-ci-checks.sh` | `as_array`: `${1:-[]}`; never `--argjson` empty; parse miss → `state:polling` |
| `src/superclaude/pr_submit/ci.py` | empty checks + `state==polling` → `polling` (one branch) |
| `SKILL.md` Wave 8 + `refs/ci-poll.md` | arm table; HALT_MAX_ROUNDS wait-only |
| `refs/state-machine.md` | SKILL-owned: wait after halt (no new FSM edge) |
| `tests/pr_submit/test_ci_classify.py` | mix pending+pass; empty+polling |
| parent spec FM-CI-7 | rewrite: wait starts; fix does not |

Do not edit `fsm.py`. `make sync-dev` after skill edits.

## 7. Tests

| ID | Asserts |
|----|---------|
| existing `test_classify_pending` / `_all_pass` / `_empty` / `_fail` | keep |
| **NEW** mix pass+pending → `polling` | FR-W1 |
| **NEW** `{state:polling, checks:[]}` → `polling` | FR-W9 |
| **NEW** honest `{checks:[]}` without polling state → `clean` | FR-W8 |
| poller: empty stdin to as_array → `[]` and script still prints one JSON line | FR-W6 (shell or fixture) |
| T-104 still green | `--repo` pin |

## 8. Note (E9)

If `--required` is nonempty, optional pending checks are ignored (FR-CI-11). That is not a false clean. "ALL checks" = all in the **chosen** list.

## 9. Success

Monitor keeps looping while any chosen check is `pending`. Poller never dies on empty stdout. Wave 8 wait runs after Augment round-cap halt. CI auto-fix still respects `max_rounds`.
