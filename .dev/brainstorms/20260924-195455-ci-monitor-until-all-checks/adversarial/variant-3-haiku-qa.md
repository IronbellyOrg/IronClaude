---
variant: 3
persona: qa
model: haiku
generated: 2026-09-24
topic: ci-monitor-until-all-checks
bias: acceptance-criteria-and-failure-modes
source: ../seed-brief.md
live_pr: https://github.com/IronbellyOrg/IronClaude/pull/237
---

# Variant 3 — CI monitor until ALL checks complete (QA / haiku)

Binding authority: **testable acceptance criteria**. If a later merge drops an
AC, the corresponding requirement is untestable and MUST be rewritten or
deleted — not left as prose. This is a requirements spec, not an
implementation. No new FSM. `fsm.py` stays byte-identical (INV-CI-7).

Grounded this session (2026-09-24): `src/superclaude/pr_submit/ci.py`
`classify_checks`; `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh`
(`as_array` + `--argjson`); SKILL.md Wave 8 gate; `tests/pr_submit/test_ci_classify.py`;
seed-brief abort paths; live PR #237 (Test 3.10/3.11/3.12 pending + `HALT_MAX_ROUNDS`).

## 1. Problem (falsifiable)

`sc:pr-submit --monitor 3` on PR #237 stopped while GitHub Actions jobs were
still `pending`. Two independent abort paths:

1. **Wave 8 never armed.** SKILL.md: Wave 8 starts only after Augment
   `clean` / `REPORT_ONLY`. `DEFAULT_MAX_ROUNDS=2` fired `HALT_MAX_ROUNDS`
   first. Wait never started.
2. **Poller not fail-soft.** Empty `gh pr checks` stdout → `as_array` can
   return empty (jq exit 0, empty stdout) → `--argjson req ""` dies under
   `set -e`. Live residual: `poll-ci-checks.sh:47`. Monitor gets no JSON line.

**Fail if:** the in-session Monitor exits, classifies `clean`, or crashes
while any check in the **chosen list** (`--required` if nonempty, else all)
still has `bucket=pending`.

"ALL checks" = all checks in that chosen list. Not Codecov-by-name. Not a
new `--ci-timeout` flag. Not a new `EventType` / FSM edge.

## 2. Goals / non-goals

| ID | Goal | Fail if |
|----|------|---------|
| G-1 | Pending stays `polling` | Any `pending` in chosen list maps to `clean` or `findings` |
| G-2 | Poller always one JSON line, exit 0 | Empty stdout, exit 8, or parse miss → no line / nonzero (usage=2 excepted) |
| G-3 | Wave 8 after Augment halt | `HALT_MAX_ROUNDS` skips CI wait while jobs pending |
| G-4 | Empty `checks` is `clean` only for no-Actions | Parse-fail / empty stdout classified as `clean` |
| G-5 | `--required` then all | Nonempty required ignored, or empty-parse of required skips fallback |
| G-6 | No new FSM | `fsm.py` diff, new `EventType`, new `--monitor` ordinal |

**Out of scope (do not test as if shipped):** `--ci-timeout`; `gh run rerun`;
`classifier.py` / `DetectionContract` edits; CI auto-fix on a **separate**
round budget after Augment halt (wait-only is the default; auto-fix stays
shared `max_rounds`). Raise default timeout only if 600s-after-reset is
proven insufficient — not part of this AC set.

## 3. Acceptance criteria

Each AC is Given / When / Then. Reviewer evidence MUST cite `file:line` of
production code **or** the test ID. "Looks right" is not evidence.

### 3.1 Classifier (`classify_checks`)

Authoritative mapping already in `ci.py` (keep; add the missing mix / parse
rows). Empty `checks=[]` remains FR-CI-4 **only** when the poller honestly
observed no Actions.

| AC | Given | When | Then | Test ID |
|----|-------|------|------|---------|
| AC-CLS-1 | ≥1 check `bucket=pending` | `classify_checks(payload)` | `polling` | T-CI-CLS-PENDING (exists: `test_classify_pending`) |
| AC-CLS-2 | All chosen checks `pass` and/or `skipping`; none pending/fail/cancel | classify | `clean` | T-CI-CLS-PASS (exists: `test_classify_all_pass`) |
| AC-CLS-3 | `checks=[]` **or** missing `checks`, payload is a successful no-Actions poll (`head_sha` present, no parse-error) | classify | `clean` (FR-CI-4, do not hang) | T-CI-CLS-EMPTY (exists: `test_classify_empty`) |
| AC-CLS-4 | Mix: ≥1 `pass` **and** ≥1 `pending` | classify | `polling` (pending wins; do not early-clean on the passes) | T-CI-CLS-MIX **NEW** |
| AC-CLS-5 | All chosen checks `pending` | classify | `polling` | T-CI-CLS-ALL-PENDING **NEW** |
| AC-CLS-6 | Mix `pass` + `fail`, no pending | classify | `findings` | T-CI-CLS-FAIL (exists: `test_classify_fail`) |
| AC-CLS-7 | `wait_sha` set and `head_sha` differs | classify | `polling` even if buckets are fail/pass | T-CI-CLS-STALE (exists: `test_classify_stale_head_is_polling`) |
| AC-CLS-8 | Non-dict payload or unreadable `checks` (not a list) | classify | **MUST NOT** be treated as honest empty-Actions `clean` if the SKILL/poller marked parse failure. Today `ci.py` returns `clean` for non-dict / empty — that is a **false-clean footgun**. Fix: poller never feeds that shape as a completed poll; if it must, emit `state=polling` and omit a fake empty success. Classifier may keep FR-CI-4 empty→clean for a well-formed `{checks:[]}`. | T-CI-CLS-NONDICT **NEW** (pin: poller+SKILL never call classify on crashed stdout) |

### 3.2 Poller (`poll-ci-checks.sh`)

Contract: one JSON line on stdout, `exit 0` after a completed poll; `exit 2`
only for usage (`--pr` missing). Fail-soft. T-104: every `gh` pins `--repo`.

| AC | Given | When | Then | Test ID |
|----|-------|------|------|---------|
| AC-POLL-1 | `gh pr checks --required` stdout is empty string; `--json` all-checks has a real array | `as_array` + choose list | Fallback to **all** runs (FR-CI-11). `--argjson` does not die. One JSON line, exit 0. | T-CI-POLL-EMPTY-REQ **NEW** |
| AC-POLL-2 | Both required and all stdout empty (no Actions, honest) | poll | One JSON line, `checks:[]`, coarse `state=clean`, exit 0 | T-CI-POLL-NO-ACTIONS **NEW** |
| AC-POLL-3 | `gh pr checks` **exit 8** (pending) **and** JSON array still printed | capture (`\|\| true` on the assignment, **not** `\|\| echo '[]'` on the same stdout) | Stdout is the JSON array, not `[]\n[]`. Chosen list keeps pending rows. Coarse `state=polling`. Exit 0. | T-CI-POLL-EXIT8 **NEW** |
| AC-POLL-4 | `gh pr checks` exit 8 **and** empty stdout | poll | One JSON line, exit 0. `state=polling` (unknown, still waiting). **Not** `clean`. `checks` may be `[]` only if paired with an explicit non-clean state or parse-miss flag the SKILL will not classify as FR-CI-4 clean. | T-CI-POLL-EXIT8-EMPTY **NEW** |
| AC-POLL-5 | `as_array` input is `""` | function | Emits `[]` (or equivalent JSON array token). Never empty string. Never causes `--argjson` to see `""`. | T-CI-POLL-AS-ARRAY-EMPTY **NEW** (live finding) |
| AC-POLL-6 | `as_array` input is already a JSON array | function | Pass-through compact array | T-CI-POLL-AS-ARRAY-OK **NEW** |
| AC-POLL-7 | `as_array` input is non-array JSON (`{}`, `"x"`) | function | `[]`, exit path still 0 for the script | T-CI-POLL-AS-ARRAY-JUNK **NEW** |
| AC-POLL-8 | Required list length > 0 | choose | Use required; do **not** merge optional pending into the list (FR-CI-11). Optional pending is not a wait. | T-CI-POLL-REQUIRED-WINS **NEW** |
| AC-POLL-9 | Required list `[]`, all list nonempty | choose | Use all | T-CI-POLL-FALLBACK **NEW** |
| AC-POLL-10 | `gh pr view` empty / fail | poll | Existing fail-soft: one line `state=polling`, `checks:[]`, exit 0 (do not classify this as no-Actions clean at SKILL layer without a later successful view) | T-CI-POLL-NO-PR (exists as script branch; add assertion) |
| AC-POLL-11 | Every `gh` in the script | static grep | `--repo` present (T-104). `ci.py` still zero `gh`/`git` tokens (T-N50 / NFR-6). | T-104, T-N50 (exists; keep green) |
| AC-POLL-12 | Mid-poll head SHA change | re-sample | Coarse `state=polling` (existing HEAD1≠HEAD2) | T-CI-POLL-TOCTOU (behavior exists; add test if missing) |

### 3.3 Wave 8 entry (SKILL, not FSM)

`fsm.py` does not grow a CI state. SKILL intercepts.

| AC | Given | When | Then | Test ID |
|----|-------|------|------|---------|
| AC-W8-1 | Augment classify `clean` | Wave 8 | Arm CI poll: `source=ci`, reset wait elapsed (FR-CI-12), swap to `poll-ci-checks.sh`. Do **not** `transition(clean)` yet. | T-CI-W8-AFTER-CLEAN **NEW** (protocol grep + golden SKILL path) |
| AC-W8-2 | Augment `REPORT_ONLY` | Wave 8 | Same as AC-W8-1 | T-CI-W8-AFTER-REPORT **NEW** |
| AC-W8-3 | Augment `HALT_MAX_ROUNDS` with CI jobs still pending | Wave 8 | **Still arm wait-only CI poll.** Do not skip because the round budget is spent. CI auto-fix / Waves 3–5 stay gated by `max_rounds` (no extra budget). | T-CI-W8-AFTER-HALT **NEW** (PR #237 repro) |
| AC-W8-4 | `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` / `TERMINAL_FAILED` | Wave 8 | Still **does not** start. Halt-then-wait is **only** `HALT_MAX_ROUNDS`. | T-CI-W8-NO-OTHER-HALT **NEW** |
| AC-W8-5 | L0 `--monitor 0` | Wave 8 | Never reached | T-110 (exists) |
| AC-W8-6 | Chosen list has any `pending` | Monitor loop | Keep polling at ≥30s until no pending **or** `--timeout` (clock reset at `source=ci` flip). Do not emit `TERMINAL_CLEAN`. | T-CI-W8-KEEP-POLLING **NEW** |
| AC-W8-7 | Chosen list all `pass`/`skipping`, no pending | Monitor | `transition(clean)` → `TERMINAL_CLEAN` | T-CI-W8-THEN-CLEAN **NEW** |
| AC-W8-8 | After halt-then-wait, CI is `findings` | SKILL | Wait completed; auto-fix **does not** run (budget already spent). `REPORT_ONLY` or equivalent residual report. Not silent `clean`. | T-CI-W8-HALT-THEN-RED **NEW** |
| AC-W8-9 | CI `clean` | round counter | Must not tick (INV-CI-5). | T-CI-W8-NO-TICK **NEW** |
| AC-W8-10 | Protocol text | SKILL.md Wave 8 bullet | MUST NOT say "Does not start on `HALT_*`" as a blanket. Exception: `HALT_MAX_ROUNDS` starts wait-only. | T-CI-W8-SKILL-TEXT **NEW** |

### 3.4 Invariants (regression)

| AC | Invariant | Test ID |
|----|-----------|---------|
| AC-INV-1 | `fsm.py` byte-identical vs pre-change | T-CI-INV-7 (`git diff` / hash in CI, or empty diff assertion) |
| AC-INV-2 | No new `EventType` member (stays 37) | INV-CI-1 existing test |
| AC-INV-3 | `classifier.py` / `DetectionContract` unchanged | INV-CI-2 |
| AC-INV-4 | No `gh run rerun` in skill scripts | T-CI-NO-RERUN **NEW** grep |
| AC-INV-5 | No new `--monitor` value, no `--ci-timeout` | argparse choices test (existing T-101) + grep |
| AC-INV-6 | Existing `tests/pr_submit/test_ci_classify.py` stays green | `uv run pytest tests/pr_submit/test_ci_classify.py` |

## 4. Edge-case matrix (must have a row each)

This table **is** the regression boundary. An empty cell is a defect in the
spec. `chosen` = required if nonempty else all.

| Row | Scenario | Poller stdout / exit | Chosen list | `classify_checks` | Monitor | False-clean? |
|-----|----------|----------------------|-------------|-------------------|---------|--------------|
| E1 | Empty required, nonempty all with pending | req `[]`, all `[pending…]`, exit 0 | all | `polling` | loop | No |
| E2 | Empty required **parse** (blank stdout), all has pending | req `""` → must become `[]` then fallback | all | `polling` | loop | **Yes if `--argjson` dies or fallback skipped** |
| E3 | Honest no Actions | req `[]`, all `[]`, exit 0 | `[]` | `clean` | `TERMINAL_CLEAN` | No (FR-CI-4) |
| E4 | Exit 8, JSON printed, mix pass+pending | exit 8, array with pass+pending | that array | `polling` | loop | **Yes if `\|\| echo '[]'` concatenates** (already forbidden) |
| E5 | Exit 8, empty stdout | exit 8, `""` | unknown | **not** `clean` | loop / polling JSON | **Yes if mapped to FR-CI-4 empty** |
| E6 | All pending (3.10/3.11/3.12) | exit 8, three pending | those three | `polling` | loop | No if mapping held |
| E7 | Mix pass + pending (PR #237 shape) | several pass, 3.10/3.11/3.12 pending | all (if required empty) | `polling` | loop | **Yes if classifier prefers pass** |
| E8 | All pass | exit 0, all `pass`/`skipping` | all | `clean` | `TERMINAL_CLEAN` | No |
| E9 | Nonempty required all pass; optional still pending | required pass-only | required | `clean` | `TERMINAL_CLEAN` | **Not a false clean under FR-CI-11.** Document: "ALL" ≠ optional jobs. Do not special-case Codecov. |
| E10 | `HALT_MAX_ROUNDS` then jobs still pending | n/a (SKILL gate) | n/a | n/a | Wave 8 wait-only arms | **Yes if Wave 8 skipped** (PR #237) |
| E11 | `HALT_MAX_ROUNDS` then wait, then all pass | later poll all pass | all | `clean` | `TERMINAL_CLEAN` | No |
| E12 | `HALT_MAX_ROUNDS` then wait, then fail | later poll fail | all | `findings` | report, no auto-fix | No |
| E13 | `HALT_HUMAN` with pending CI | n/a | n/a | n/a | no Wave 8 | No |
| E14 | Poller crash (jq `--argjson` on `""`) | no JSON line, `set -e` death | n/a | never called | Monitor cannot continue | **Yes / abort** (live finding) |
| E15 | `PR_JSON` empty | polling JSON, `checks:[]` | `[]` | SKILL must treat as `polling`, not FR-CI-4 clean | loop | **Yes if SKILL classifies that payload as clean** |

## 5. What would make a false `clean`

Ranked. Any of these shipping is a P0 vs G-1/G-4.

| ID | Mechanism | Why it looks clean | Guard |
|----|-----------|--------------------|-------|
| FC-1 | `as_array("")` → `""` → `--argjson` fail | No line; operator may assume done / Monitor aborts | T-CI-POLL-AS-ARRAY-EMPTY, AC-POLL-5 |
| FC-2 | `as_array("")` "fixed" to `[]` **and** fallback skipped | `checks=[]` → FR-CI-4 `clean` while jobs exist | Distinguish E2 vs E3: fallback **must** run when all-stdout is nonempty |
| FC-3 | Exit 8 + `\|\| echo '[]'` on same stdout | Concatenated JSON / parse miss / empty | Already banned in script comment; T-CI-POLL-EXIT8 |
| FC-4 | Exit 8 + empty stdout classified as no-Actions | FR-CI-4 | AC-POLL-4: `state=polling` |
| FC-5 | Mix pass+pending classified `clean` because any pass | Wrong bucket fold | T-CI-CLS-MIX; pending-wins already in `ci.py` — **keep** |
| FC-6 | Wave 8 never starts on `HALT_MAX_ROUNDS` | Terminal status while 3.10/3.11/3.12 pending | T-CI-W8-AFTER-HALT (incident) |
| FC-7 | SKILL `transition(clean)` on Augment clean before CI wait | `TERMINAL_CLEAN` with Actions still running | AC-W8-1 |
| FC-8 | `classify_checks` non-dict → `clean` (`ci.py` today) | Garbage payload looks like success | Poller never feeds it; T-CI-CLS-NONDICT |
| FC-9 | Empty required (honest `[]`) without reading all | Optional/required-unset pending jobs ignored | FR-CI-11 fallback; T-CI-POLL-FALLBACK |
| FC-10 | Treating coarse script `state` as authoritative when it says `clean` on `checks=[]` after a parse miss | Script hint vs `classify_checks` | SKILL uses `classify_checks`; on poller `state=polling` with empty checks after exit 8, **do not** call empty→clean |
| FC-11 | Timeout clock **not** reset at `source=ci` | `TERMINAL_TIMEOUT` during matrix | FR-CI-12; not a `clean` but same user-visible "stopped while pending" |
| FC-12 | Nonempty `--required` that excludes the still-running matrix | Optional pending ignored | **Allowed** by FR-CI-11. Not FC. Document in operator notes. |

**Incident mapping (PR #237):** FC-6 fired (`terminal_max_rounds`, Wave 8 not
started). FC-1 was the residual poller finding. E7 was the live checks table.

## 6. Test IDs — inventory

### 6.1 Keep green (do not weaken)

| Test | File | Pins |
|------|------|------|
| `test_classify_pending` | `tests/pr_submit/test_ci_classify.py` | AC-CLS-1 |
| `test_classify_all_pass` | same | AC-CLS-2 |
| `test_classify_empty` | same | AC-CLS-3 / E3 |
| `test_classify_fail` / `test_classify_cancel` | same | findings, not pending |
| `test_classify_stale_head_is_polling` | same | AC-CLS-7 |
| `test_classify_required_fallback` | same | classify sees the list the script chose |
| T-104 / T-N50 / `ci.py` in `CORE_PURE_FILES` | `tests/pr_submit/test_static_grep.py` | NFR-6, T-104 |
| poll-ci-checks in `_RESOLUTION_SCRIPTS` | same | repo resolve |

### 6.2 Must add (minimum set)

No new test framework. Prefer one parametrized table plus one poller helper
that stubs `gh` via `PATH`.

| Test ID | Kind | Asserts |
|---------|------|---------|
| T-CI-CLS-MIX | unit | pass+pending → `polling` |
| T-CI-CLS-ALL-PENDING | unit | three pending → `polling` |
| T-CI-POLL-AS-ARRAY-EMPTY | shell unit | `""` → `[]`; `jq --argjson` succeeds |
| T-CI-POLL-EXIT8 | shell stub | exit 8 + JSON → pending preserved, exit 0, one line |
| T-CI-POLL-EXIT8-EMPTY | shell stub | exit 8 + `""` → one line, **not** SKILL-clean |
| T-CI-POLL-EMPTY-REQ | shell stub | empty required + pending all → fallback, `polling` |
| T-CI-POLL-NO-ACTIONS | shell stub | both `[]` → `checks:[]` + clean **only here** |
| T-CI-POLL-REQUIRED-WINS | shell stub | nonempty required used |
| T-CI-W8-AFTER-HALT | protocol / SKILL grep + scenario | Wave 8 wait-only after `HALT_MAX_ROUNDS` |
| T-CI-W8-SKILL-TEXT | grep | Wave 8 bullet no longer blanket-excludes all `HALT_*` |
| T-CI-W8-NO-OTHER-HALT | protocol | `HALT_HUMAN` / timeout / validation still skip Wave 8 |
| T-CI-INV-7 | static | `fsm.py` unchanged |
| T-CI-NO-RERUN | grep | no `gh run rerun` |

**Fixture:** add `tests/pr_submit/fixtures/checks-mix-pass-pending.json`
shaped like PR #237 (pass rows + Test 3.10/3.11/3.12 `pending`). Do not
re-type production JSON if a captured payload exists — prefer verbatim.

**Do not add:** FSM table rows, new EventType tests, live `gh` against
PR #237 in unit CI, Codecov-by-name filters.

## 7. Existing-suite gaps (why green is not enough)

| Gap | Today | Risk |
|-----|-------|------|
| No mix pass+pending fixture | `checks-pending.json` is pending-only; `checks-pass.json` is pass+skipping | FC-5 untested |
| No poller unit for `as_array` empty | Script comment documents exit 8; empty stdout untested | FC-1 ships again |
| `test_classify_empty` encodes FR-CI-4 | Correct for no-Actions; **cannot** see FC-2/FC-4 | False clean via empty parse |
| Wave 8 SKILL line is protocol-only | No test that halt still waits | FC-6 (the incident) |
| `classify_checks` non-dict → `clean` | Unasserted as a hazard | FC-8 |

## 8. Open questions — testable defaults (do not stall)

| OQ | Default for this spec | Revisit when |
|----|----------------------|--------------|
| Wait-only after Augment halt vs extra CI round budget | **Wait-only.** Auto-fix stays shared `max_rounds`. T-CI-W8-HALT-THEN-RED. | Operator asks for CI auto-fix after halt |
| 600s after source-flip vs matrix runtime | Keep 600s. Timeout-while-pending is FC-11 (abort, not clean). | `test.yml` 3.10/3.11/3.12 regularly exceeds 600s after reset — then raise CI-phase floor in SKILL, still no new flag |

## 9. Constraints (copy from seed; test them)

- No new skill, FSM, `--monitor` ordinal, or `EventType` member.
- No `classifier.py` / `DetectionContract` edits.
- No `gh run rerun`.
- T-104: every `gh` pins `--repo`.
- NFR-6: `ci.py` free of `gh`/`git` tokens.
- `--required` remains the optional-check filter.
- Fewest files: poller + SKILL Wave 8 entry + maybe `classify_checks` empty vs
  pending distinction. Do not add `--ci-timeout` unless 600s-after-reset is
  proven insufficient.

## 10. Done-when

1. E1–E15 each have a test row or an explicit "allowed under FR-CI-11" note (E9).
2. FC-1 and FC-6 cannot recur without a named test turning red.
3. `uv run pytest tests/pr_submit/test_ci_classify.py tests/pr_submit/test_static_grep.py` green.
4. `fsm.py` diff empty.
5. On a PR #237-shaped payload (mix pass+pending) the Monitor stays in
   `polling` until those pending buckets disappear.

Rollback: revert SKILL Wave 8 gate + `as_array` default. Tests in §6.2 should
fail after that revert — if they do not, the tests are fixture-fabricated.
)
