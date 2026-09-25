---
variant: 2
persona: refactorer
model: sonnet
generated: 2026-09-24
topic: ci-monitor-until-all-checks
bias: deletion-and-gating
---

# Variant 2 — Keep waiting; do not invent a CI FSM

The live abort is two existing gates over-firing, not a missing subsystem.
Delete the halt→skip-wait coupling. Make the poller fail-soft. Leave CI
auto-fix on the shared round budget. `fsm.py` stays byte-identical.

## 1. Problem

`sc:pr-submit --monitor 3` on
[PR #237](https://github.com/IronbellyOrg/IronClaude/pull/237) exited while
Test 3.10 / 3.11 / 3.12 were still `pending`. Two independent paths:

1. **Wait never armed.** Wave 8 starts only after Augment `clean` /
   `REPORT_ONLY` (`SKILL.md` Wave 8; spec FM-CI-7). `DEFAULT_MAX_ROUNDS=2`
   → `HALT_MAX_ROUNDS` at S2 findings. Shared `max_rounds` therefore blocks
   *entry* to the CI wait, even though a wait consumes no round
   (`INV-001` / INV-CI-5: tick is Augment-only).
2. **Poller not fail-soft.** `as_array` on empty `gh pr checks` stdout can
   leave `jq` exit 0 with empty output; `--argjson req ""` then dies under
   `set -e`. Confirmed at `poll-ci-checks.sh:47`. Exit 8 may still print
   JSON (already not `|| echo '[]'` on the same stdout). Empty stdout remains.

`classify_checks` already maps `bucket=pending` → `polling`. That mapping
is not the bug. The bug is: the Monitor never reaches it, or the poller
crashes before emitting a line, or a failed parse is collapsed to
`checks=[]` → `clean` (FR-CI-4 "no Actions").

**Goal:** while any check in the chosen list (`--required`, else all) is
`pending`, classify is `polling` and the in-session Monitor keeps looping
until those checks leave `pending` (or `--timeout` fires). Wave 8 wait
still runs after Augment `HALT_MAX_ROUNDS`. CI *auto-fix* stays
budget-gated.

## 2. Thesis (wait ≠ fix)

Wave 8 does two jobs today, gated as one:

| Job | Needs rounds? | Halt should block? |
|-----|---------------|--------------------|
| Wait until chosen checks are not `pending` | No | **No** |
| Auto-fix parseable CI `findings` (Waves 3–5) | Yes (FR-CI-8) | **Yes** |

FM-CI-7 ("CI phase never starts on `HALT_MAX_ROUNDS`") is the debt.
Split the gate. Do not add a second budget, a CI round counter, or a new
terminal.

After Augment halt: **wait-only**. If CI later classifies `findings`,
SKILL `REPORT_ONLY` (same as unparseable logs). Operator who wants auto-fix
raises `--max-rounds` and `--resume`. That is already the FM-CI-7 recovery
story; it stays for *fix*, not for *wait*.

Clock: `--timeout` default 600s already resets at `source=ci` (FR-CI-12).
Do not add `--ci-timeout`. Do not raise the default until a green matrix
is shown to exceed 600s after reset. Operator who needs longer already
passes `--timeout 1800`.

## 3. Functional requirements

Falsifiable. Existing IDs reused where the parent spec already holds.

| ID | Requirement |
|----|-------------|
| FR-W1 | While any check in the chosen list has `bucket=pending`, `classify_checks` returns `polling` and the Monitor does not send `transition(clean)`. (Already true in `ci.py`; keep it.) |
| FR-W2 | Wave 8 **wait** arms after Augment `clean`, `REPORT_ONLY`, **or** `HALT_MAX_ROUNDS`. Same intercept as today: do not `transition(clean)` yet; set `source=ci`, reset elapsed, swap to `poll-ci-checks.sh`. |
| FR-W3 | Wave 8 wait still does **not** arm on `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` / `TERMINAL_FAILED`. L0 never reaches Wave 8. |
| FR-W4 | After `HALT_MAX_ROUNDS`, Wave 8 is wait-only: `polling` loops; `clean` → `transition(clean)`; human-gate → `HALT_HUMAN`; `findings` → `REPORT_ONLY` (no Waves 3–5, no push). |
| FR-W5 | When `round_counter < max_rounds` at CI `findings`, existing FR-CI-8 auto-fix is unchanged (shared budget). No second counter. |
| FR-W6 | `poll-ci-checks.sh` always emits exactly one JSON line and exits 0 on a completed poll (usage errors still exit 2), including: empty stdout, `gh` exit 8, non-array stdout, `--required` empty. |
| FR-W7 | `--required` first; a **parsed empty array** falls back to all (FR-CI-11). An **unparsed / empty stdout** is not a parsed empty array: it must not skip fallback, and it must not become `clean`. |
| FR-W8 | `checks=[]` is `clean` only when both required and all lists **parsed as JSON arrays** and both have length 0 (no Actions). Poller crash, empty stdout, or `--argjson` failure is never `clean`. |
| FR-W9 | If the poller cannot parse checks, emit `state:"polling"` plus a payload flag the classifier already can see without new EventType — reuse `state` or a boolean `incomplete` on the **JSON line**, not a new `EventType` member. `classify_checks` returns `polling` for that payload. |
| FR-W10 | No `--ci-timeout`. Reuse `--timeout`. Clock reset at `source=ci` is the only timeout change (FR-CI-12). |
| FR-W11 | Every `gh` call in the poller still pins `--repo` (T-104). `ci.py` still has zero `gh`/`git` tokens (NFR-6 / INV-CI-4). |
| FR-W12 | `fsm.py` is byte-identical (INV-CI-7). No new skill, FSM, `--monitor` ordinal, or `EventType` member. No `classifier.py` / `DetectionContract` edits. No `gh run rerun`. |

## 4. What NOT to add

- New skill, FSM module, `MonitorState`, `EventType`, or `--monitor` ordinal.
- `source` on `transition()` / `RunConfig` / `fsm.py`.
- A CI-specific `max_rounds` / `ci_round_counter` / `--ci-max-rounds`.
- `--ci-timeout`, `--ci-only`, Codecov-by-name, `gh run rerun`.
- Parallel Augment+CI poller.
- Treating halt as non-terminal inside `fsm.py` (SKILL intercepts, as today).
- Fake `Finding` / pending sentinel check objects to dodge `checks=[]` → `clean`.
- Relaxing `is_groundable`.
- Speculative classify rewrite: pending→polling stays; only empty-vs-incomplete is in scope.

Skipped: `--ci-timeout` — add when 600s-after-reset is measured short on `test.yml`.
Skipped: CI auto-fix after halt — add when an operator actually `--resume`s to fix CI under a raised budget and wait-only is not enough.

## 5. Smallest file list

Three production files. Spec/docs only as needed to un-lie FM-CI-7.

| File | Change |
|------|--------|
| `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh` | `as_array`: empty/non-JSON → `[]` so `--argjson` never sees `""`. Track whether each `gh pr checks` stdout **parsed as an array**. Parsed empty required → fallback to all. Neither side parsed → `state:polling` + `incomplete` (or equivalent), not `clean`. |
| `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` | Wave 8 header + bullet: wait also after `HALT_MAX_ROUNDS`; auto-fix still `round_counter < max_rounds`. One sentence, not a new wave. |
| `src/superclaude/pr_submit/ci.py` | **Only if** SKILL always re-classifies the JSON line: `incomplete` (or `state=="polling"` with empty checks) → `polling`. Do not change the pending branch. Do not change genuine `checks=[]` → `clean`. |

Docs that currently say the wrong gate (edit if this variant is selected):

| File | Change |
|------|--------|
| `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` §5.2c | Halt still skips CI *fix*; wait may arm. |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md` | Empty stdout / incomplete ≠ clean. |
| `.dev/specs/pr-submit-ci-monitor.md` | Replace FM-CI-7: wait starts; auto-fix does not. |

Then `make sync-dev`. **Do not** edit `fsm.py`, `classifier.py`,
`DetectionContract`, `pr_submit/__init__.py`.

Rollback: revert the SKILL gate sentence + the `as_array` default (seed
socratic #10). Classifier incomplete branch rolls back with them.

## 6. Tests

Keep `tests/pr_submit/test_ci_classify.py` green (`test_classify_pending`,
`test_classify_empty`). Add the cases the live abort actually hit.

| Test | Asserts |
|------|---------|
| `test_as_array_empty_stdout_emits_json` | Fixture: both `gh pr checks` stdout empty. Script exit 0, one JSON object, valid `checks` array. Never `--argjson` fail. |
| `test_required_empty_falls_back_to_all_pending` | Required parsed `[]`, all has `bucket=pending` → chosen list is all → classify `polling`. |
| `test_unparsed_stdout_is_polling_not_clean` | Non-array / empty stdout on **both** lists → not `clean` (incomplete / polling). |
| `test_parsed_both_empty_is_clean` | Both sides parsed `[]` → `clean` (FR-CI-4 no Actions). Distinct from the row above. |
| `test_classify_pending` (existing) | Any `pending` → `polling`. |
| `test_classify_incomplete_is_polling` | Only if `ci.py` grows the incomplete branch. |
| T-104 static grep | `poll-ci-checks.sh` still in the `--repo` pin set (`test_static_grep.py`). |
| SKILL static | Wave 8 text allows wait after `HALT_MAX_ROUNDS`; still forbids wait on `HALT_HUMAN` / `TERMINAL_TIMEOUT`. |

No `transition()` / `source=` unit tests. No fsm fixture. Shell test may
stub `gh` on PATH; do not hit the network.

## 7. Ground facts this variant refuses to re-solve

- Pending → polling: done (`classify_checks`).
- Exit 8 JSON on stdout: do not re-add `\|\| echo '[]'` on the `gh` line.
- Clock reset at `source=ci`: done (FR-CI-12).
- INV-CI-7: no `fsm.py` edits.
- Round tick: Augment-only; CI `clean` must not tick.
- `--required` is the optional-check filter; no Codecov special case.
