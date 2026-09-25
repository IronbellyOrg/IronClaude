---
topic: "Brainstorm the necessary fixes to keep the CI monitor active until ALL CI tests come back."
domain: code
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-09-24T19:54:55Z
---

# Seed Brief: ci-monitor-until-all-checks

## Problem Statement

`sc:pr-submit --monitor 3` on PR #237 stopped before GitHub Actions finished.
Two independent abort paths fired:

1. **Augment round cap** (`DEFAULT_MAX_ROUNDS=2`) → `HALT_MAX_ROUNDS`. Spec
   Wave 8 starts only after Augment `TERMINAL_CLEAN` / `REPORT_ONLY`, so the
   CI wait never armed even though Test 3.10/3.11/3.12 were still `pending`.
2. **Poller not fail-soft.** `as_array` on empty `gh pr checks` stdout lets
   `jq` exit 0 with empty output; `--argjson req ""` then dies under `set -e`.
   Confirmed live: the residual Augment finding at
   `poll-ci-checks.sh:47` and a direct poller invocation.

"Keep active until ALL CI tests come back" means: while any check is
`pending`, keep polling; do not treat empty/required-missing/poller-crash as
`clean`; do not skip the wait because Augment already spent the round budget.

## Known Context

- Classifier already maps `bucket=pending` → `polling` (`ci.py`
  `classify_checks`). Empty `checks=[]` → `clean` (FR-CI-4: "no Actions").
- `--required` first; empty list falls back to all checks (FR-CI-11). If
  `as_array` yields empty, fallback never runs.
- `--timeout` default 600s (`fsm.py` `DEFAULT_TIMEOUT`). Clock resets at
  `source=ci` flip (FR-CI-12). Spec deferred `--ci-timeout`.
- Round tick is Augment-only (`INV-001` / `S5_AWAITING_REREVIEW → S2`).
  CI `clean` must not tick. Shared `max_rounds` still gates *entry* to
  Wave 8 via HALT.
- `gh pr checks` exit 8 = pending, JSON may still print. `|| echo '[]'` on
  the same stdout was already fixed; empty-stdout remains.
- Live PR: https://github.com/IronbellyOrg/IronClaude/pull/237
- `fsm.py` stays byte-identical (INV-CI-7). SKILL owns Wave 8.

## Constraints

- No new skill, FSM, `--monitor` ordinal, or `EventType` member.
- No `classifier.py` / `DetectionContract` edits.
- No `gh run rerun`.
- T-104: every `gh` call pins `--repo`.
- NFR-6: `ci.py` stays free of `gh`/`git` tokens.
- `--required` remains the optional-check filter (no Codecov-by-name).
- Fewest files: poller + SKILL Wave 8 entry + maybe `classify_checks` empty
  vs pending distinction. Do not add `--ci-timeout` unless 600s-after-reset
  is proven insufficient.

## Success Criteria

- While any check in the chosen list (`--required` or all) is `pending`,
  classify is `polling` and the in-session Monitor keeps looping.
- Poller always emits one JSON line, exit 0, even on empty stdout / exit 8.
- Wave 8 still runs after Augment `HALT_MAX_ROUNDS` (wait-until-complete;
  CI auto-fix remains budget-gated).
- `checks=[]` is `clean` only when both required and all lists are empty
  (no Actions), never when the poller failed to parse.
- Existing unit tests stay green; add the empty-stdout / pending-until-done
  cases.

## Open Questions

- Wait-only after Augment halt vs also allowing CI auto-fix on a separate
  CI round budget (spec said shared `max_rounds`).
- Whether 600s after source-flip covers `test.yml` matrix; if not, raise
  default timeout for the CI phase only (still no new flag if SKILL can
  reuse `--timeout` with a larger CI floor).

## Socratic auto-answers (non-interactive)

1. Entry: `poll-ci-checks.sh` + `classify_checks` + SKILL Wave 8 gate.
2. Scope: those three; not a new FSM.
3. Failure: monitor exits while jobs still `pending`.
4. Constraints: INV-CI-7, NFR-6, T-104, no new EventType.
5. Done: poll until no `pending`; Wave 8 reached even if Augment halted.
6. Align with existing pending→polling mapping; fix poller + entry gate.
7. Consumer: in-session `sc:pr-submit` operator.
8. Tests: unit for `as_array`/empty + classify pending; static T-104.
9. Forcing function: PR #237 still running tests.
10. Rollback: revert the SKILL gate + one-line `as_array` default.

## Enrichment Context

Codebase (primary): Wave 8 never arms on `HALT_MAX_ROUNDS`; `classify_checks` already stays `polling` on `pending`; poller dies on empty stdout (`as_array` + `--argjson`); live PR #237 still had 3.10/3.11/3.12 pending when the monitor halted. No new FSM. Fix the poller's fail-soft, the Wave 8 entry gate, and do not treat a failed parse as `clean`.
