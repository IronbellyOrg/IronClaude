---
variant: 1
persona: architect
model: opus
generated: 2026-09-24
topic: ci-monitor-until-all-checks
domain: code
status: draft-spec
parent_spec: .dev/specs/pr-submit-ci-monitor.md
soT_skill: src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
soT_poller: src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh
soT_classifier: src/superclaude/pr_submit/ci.py
---

# Variant 1 — Keep CI monitor active until ALL checks complete (architect)

Requirements spec, not code. Binding sources: `seed-brief.md`, parent
`.dev/specs/pr-submit-ci-monitor.md` v1.0.2, live PR
https://github.com/IronbellyOrg/IronClaude/pull/237.

This is a **delta** on the existing Wave 8 / `source=ci` design. It does
not add a skill, FSM, `--monitor` ordinal, or `EventType` member.

---

## 1. Problem

`sc:pr-submit --monitor 3` on PR #237 stopped while GitHub Actions still
had Test 3.10 / 3.11 / 3.12 `pending`. Two independent abort paths:

| # | Abort | Where | Why Wave 8 never finished |
|---|-------|-------|---------------------------|
| A | Augment round cap | `DEFAULT_MAX_ROUNDS=2` → `HALT_MAX_ROUNDS` | Parent spec §4 and SKILL Wave 8 start **only** after Augment `TERMINAL_CLEAN` / `REPORT_ONLY`. `HALT_MAX_ROUNDS` is listed as a terminal that **must not** start CI. FM-CI-7 encodes that. |
| B | Poller not fail-soft | `poll-ci-checks.sh` `as_array` | Empty `gh pr checks` stdout: `jq` can exit 0 with empty output; `--argjson req ""` then dies under `set -e`. Monitor gets no JSON line. Residual finding at `poll-ci-checks.sh:47`. |

Classifier is **not** the pending bug. `classify_checks` already maps
`bucket=pending` → `polling`. Empty `checks=[]` → `clean` (FR-CI-4: "no
Actions"). That mapping is correct **only** when both `--required` and
all-checks lists are real empty arrays. A failed parse must not look like
that.

"Keep active until ALL CI tests come back" means:

1. While any check in the chosen list (`--required`, else all) is
   `pending`, classify is `polling` and the in-session Monitor keeps
   looping.
2. Wave 8 still **arms** after Augment `HALT_MAX_ROUNDS` as
   wait-until-complete. CI auto-fix stays on the shared `max_rounds`
   budget (already spent → no new fix cycle).
3. Poller always emits one JSON line, exit 0, on a completed poll
   (usage errors still exit 2).

### 1.1 Ground facts (must not be contradicted)

- `classify_checks` already maps `pending` → `polling`; empty checks →
  `clean`.
- Wave 8 currently starts only after Augment `TERMINAL_CLEAN` /
  `REPORT_ONLY`.
- `HALT_MAX_ROUNDS` (`max_rounds` default 2) blocked Wave 8 on PR #237
  while Test 3.10/3.11/3.12 were still pending.
- `as_array` on empty `gh` stdout → `jq --argjson` dies under `set -e`.
- `fsm.py` stays byte-identical (INV-CI-7).
- `ci.py` stays free of `gh`/`git` tokens (INV-CI-4 / NFR-6).
- No `gh run rerun`. No Codecov-by-name. `--required` remains the
  optional-check filter (FR-CI-11).
- `gh pr checks` exit 8 = pending; JSON may still print. Do not
  `|| echo '[]'` on the same stdout (already fixed). Empty-stdout remains.
- Round tick is Augment-only (`INV-001` / `S5_AWAITING_REREVIEW → S2`).
  CI `clean` must not tick. Shared `max_rounds` still gates **auto-fix
  entry**, not the wait itself.
- `--timeout` default 600s (`fsm.py` `DEFAULT_TIMEOUT`). Clock resets at
  `source=ci` flip (FR-CI-12). No `--ci-timeout` unless 600s-after-reset
  is proven insufficient.
- T-104: every `gh` call pins `--repo`.

### 1.2 Design thesis (architect)

Keep the existing three-layer split. Add **one table** and **one
fail-soft helper**, not a new machine.

```
poll-ci-checks.sh     one poll, one JSON line, always valid JSON
classify_checks       buckets → polling | clean | findings
SKILL Wave 8          when to arm; wait vs wait+autofix
```

Extension scaffolding = the Wave 8 **entry table** in `refs/ci-poll.md`.
A future terminal that should wait-only is a new **row**, not Wave 9,
not a new FSM edge, not a new `EventType`.

`HALT_MAX_ROUNDS` stays an FSM terminal. The SKILL intercepts it the
same way it already intercepts Augment-`clean` (does not send
`transition(clean)`; continues the Monitor). `fsm.py` never learns
`source`.

---

## 2. Functional requirements

Each FR is falsifiable from the files in §5 plus the tests in §6.

### 2.1 Wave 8 entry (amends FR-CI-1, FM-CI-7)

**FR-W8-1.** Wave 8 entry is a closed table in `refs/ci-poll.md`,
referenced from SKILL.md Wave 8. SKILL.md MUST NOT keep a boolean
"clean / REPORT_ONLY only" gate.

| Augment outcome | Arm Wave 8? | CI mode |
|-----------------|-------------|---------|
| Augment classify would be `clean` (SKILL intercepts; no `transition(clean)` yet) | yes | wait + auto-fix if `round_counter < max_rounds` |
| `REPORT_ONLY` | yes | wait + auto-fix if `round_counter < max_rounds` |
| `HALT_MAX_ROUNDS` | yes | **wait-until-complete only** |
| `HALT_HUMAN` | no | — |
| `VALIDATION_FAIL` | no | — |
| `TERMINAL_TIMEOUT` | no | — |
| `TERMINAL_FAILED` | no | — |
| L0 (`--monitor 0`) | no | — |

**FR-W8-2.** Wait-until-complete (the `HALT_MAX_ROUNDS` row): set
`source=ci`, reset wait elapsed, swap to `poll-ci-checks.sh`, loop while
`classify_checks` is `polling`. Do **not** open Waves 3–5. Do **not**
push. Do **not** call `do_retrigger` / reply / resolve.

When classify leaves `polling`:

| Classify | SKILL action |
|----------|--------------|
| `clean` | `transition(clean)` → `TERMINAL_CLEAN` |
| `findings` (human-gate) | `HALT_HUMAN`, no Finding (FR-CI-5 unchanged) |
| `findings` (non-human) | `REPORT_ONLY` (budget already spent). Log fetch is optional; no fake `Finding`. |

**FR-W8-3.** Wait+auto-fix rows (Augment clean / `REPORT_ONLY`) keep
parent FR-CI-8: verified CI findings reuse Waves 3–5 under the **same**
`round_counter` / `max_rounds`. If the gate would fire
(`round_counter >= max_rounds`) on a CI `findings` event, degrade to
wait-until-complete rather than skip the wait. No second CI round
budget. No new flag.

**FR-W8-4.** Arming Wave 8 from `HALT_MAX_ROUNDS` MUST NOT call
`transition()` to leave that FSM state. The Monitor continues on the
SKILL side. Final CI `clean` is the only `transition(clean)` on this
path. This is the same intercept pattern as parent §3 / INV-CI-7.

**FR-W8-5.** On Wave 8 entry from any arming row, reset wait elapsed
(FR-CI-12). Reuse `--timeout` (default 600s). Do not add `--ci-timeout`.
Do not raise the default in `fsm.py`.

**FR-W8-6.** Operator-visible status after Augment halt MUST say the
monitor is still waiting on CI (not "done, max rounds"). Falsifier: a
run that hits `HALT_MAX_ROUNDS` while checks are `pending` still polls
until those checks leave `pending` or `--timeout` fires.

### 2.2 Poller fail-soft (amends parent §7)

**FR-W8-7.** `as_array` (or its replacement) MUST return the JSON token
`[]` whenever stdin/argument is empty, non-JSON, or a non-array. It MUST
NOT return an empty string. After this helper, every `--argjson`
argument is a JSON array token.

Falsifier: `REQUIRED_JSON=""` and `ALL_JSON=""` still produce one stdout
JSON line and exit 0. `jq --argjson` does not run.

**FR-W8-8.** Capture `gh pr checks` **exit status separately from
stdout**. Do not `|| echo '[]'` on the same stdout (parent already
forbids this).

| `gh pr checks` | stdout | Coarse `state` | `checks` |
|----------------|--------|----------------|----------|
| 0 | JSON array (possibly `[]`) | classify-equivalent hint | that array (after FR-CI-11) |
| 8 (pending) | JSON array | `polling` if any `pending` | that array |
| 8 | empty / non-array | `polling` | `[]` |
| other non-zero | anything | `polling` | sanitised array or `[]` |
| 0 | `[]` for **both** required and all | `clean` | `[]` |

Empty `gh pr view` remains: `state:polling`, `checks:[]`, exit 0
(current script lines 38–40).

**FR-W8-9.** A completed poll always: exactly one JSON line on stdout,
exit 0. Shape unchanged:

```json
{"pr": N, "head_sha": "...", "source": "ci", "state": "polling|clean|findings", "checks": []}
```

Usage errors (`--pr` missing, `gh`/`jq` missing, repo unresolved) still
exit 2. No new keys required. No new `EventType`. `poll_attempt` /
`poll_result` stay the 37-member set (INV-CI-1).

**FR-W8-10.** FR-CI-11 unchanged: `--required` first; empty required list
falls back to all checks. Fallback MUST run on a sanitised empty array
(`[]`), not on an empty string. Do not special-case any check by name
(no Codecov-by-name).

**FR-W8-11.** T-104 unchanged: every `gh` in the poller (and SKILL log
fetch) pins `--repo <owner/repo>`.

**FR-W8-12.** No `gh run rerun` anywhere in this delta.

### 2.3 Classifier empty vs parse-fail (amends FR-CI-4)

**FR-W8-13.** `classify_checks` keeps `bucket=pending` → `polling`. That
path MUST remain the primary "jobs still running" mapping.

**FR-W8-14.** `checks=[]` is `clean` **only** when the payload represents
a successful poll with both lists empty (no Actions). Falsifier: parent
`test_classify_empty` (`{"checks": []}` and `{}`) stays `clean`.

**FR-W8-15.** Disambiguate parse-fail without a new EventType or a new
payload key: if `checks` is missing/empty **and** `payload["state"] ==
"polling"`, return `polling`. The poller already emits coarse `state`.
`classify_checks` currently ignores it; this is the one allowed read.

Truth table (additive; existing rows stay):

| `checks` | `payload["state"]` | `wait_sha` mismatch | Result |
|----------|--------------------|---------------------|--------|
| any with `bucket=pending` | * | no | `polling` |
| `[]` / missing | `"polling"` | no | `polling` |
| `[]` / missing | absent / `"clean"` / other | no | `clean` |
| non-empty, no pending, any fail/cancel/`action_required` | * | no | `findings` |
| * | * | yes | `polling` (existing) |

**FR-W8-16.** `ci.py` still contains zero `gh` / `git` tokens (NFR-6).
No import of subprocess, no shell.

**FR-W8-17.** `classifier.py` and `DetectionContract` are not edited
(INV-CI-2).

---

## 3. Invariants

Parent INV-CI-1..7 remain in force. This delta adds:

| ID | Invariant |
|----|-----------|
| INV-W8-1 | `fsm.py` is byte-identical (INV-CI-7). No `source` on `transition()` / `RunConfig`. No new `MonitorState`. |
| INV-W8-2 | `EventType` remains 37 members. CI polls keep `poll_attempt` / `poll_result` with `source: "ci"`. |
| INV-W8-3 | No new skill, no new `--monitor` ordinal, no new FSM. Wave 8 stays Wave 8. |
| INV-W8-4 | Round tick stays `S5_AWAITING_REREVIEW → S2_CLASSIFY` (INV-001). CI wait does not tick. CI `clean` does not tick. |
| INV-W8-5 | Shared `max_rounds` (default 2, hard cap 5) gates CI **auto-fix**, not CI **wait**. Wait-until-complete may run after `HALT_MAX_ROUNDS`. |
| INV-W8-6 | `ci.py` has zero `gh`/`git` tokens. All GitHub I/O stays in `poll-ci-checks.sh` (+ SKILL one-shot `gh run view --log-failed`). |
| INV-W8-7 | `--required` is the only optional-check filter. No check-name allow/deny list. |
| INV-W8-8 | Wave 8 entry table is the only extension point for "should this terminal wait on CI?". Adding a row does not add a wave, flag, or EventType. |
| INV-W8-9 | G-arm / G-edit / G-push ordinals unchanged. L0 never polls CI. |
| INV-W8-10 | `do_retrigger` is not invoked when `source=ci` (INV-CI-3). Wait-until-complete also does not push. |

---

## 4. Non-goals

- New skill, new FSM, new `--monitor` ordinal, new `EventType` member.
- Any edit to `fsm.py`, `classifier.py`, `DetectionContract`,
  `pr_submit/__init__.py`.
- `gh run rerun` (flake retry).
- Codecov-by-name (or any name special-case).
- `--ci-timeout` / `--ci-only` / a second round budget / `max_ci_rounds`.
- Parallel Augment+CI polling.
- Treating `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` /
  `TERMINAL_FAILED` as Wave 8 entry.
- Un-terminalizing `HALT_MAX_ROUNDS` inside `fsm.py`.
- Fake `Finding.path` / `line=1` to sneak past `is_groundable`.
- Changing FR-CI-4's "no Actions ⇒ `clean`" for **successful** empty
  polls (do not hang on repos with no Actions).
- Re-export from `pr_submit/__init__.py`.
- `--resume` restoring `source=ci` (parent §14 skip; still skip).
- Raising `DEFAULT_TIMEOUT` in `fsm.py`.

Open question from the seed, **closed here**: wait-only after Augment
halt, not a separate CI round budget. Add a CI budget only if wait-only
leaves parseable CI failures unfixed **and** operators ask; that is a
later row/mode, not this delta.

---

## 5. File delta (fewest files)

Edit these. Do not add a Wave 9 file.

| File | Change | Why |
|------|--------|-----|
| `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh` | Fail-soft `as_array`; separate gh exit from stdout; empty stdout / exit 8 → `state:polling` + valid `[]`; never `--argjson` on `""` | Abort path B |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md` | Wave 8 entry table (FR-W8-1); fail-soft contract (FR-W8-7..10); empty-list disambiguation (FR-W8-15) | Extension scaffolding; SKILL stays thin |
| `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` | Wave 8 bullet: arm per table, including `HALT_MAX_ROUNDS` wait-only; drop "clean / REPORT_ONLY only" | Abort path A |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` | §5.2c: `HALT_MAX_ROUNDS` SKILL intercept → wait-only; still no new FSM edges | Stop the ref from contradicting the table |
| `src/superclaude/pr_submit/ci.py` | `classify_checks`: empty checks + `state=="polling"` → `polling`; no `gh`/`git` | Abort path B must not classify as `clean` |
| `tests/pr_submit/test_ci_classify.py` | Empty+polling; existing empty→clean stays | FR-W8-14/15 |
| `tests/pr_submit/test_static_grep.py` or a small `tests/pr_submit/test_poll_ci_checks.py` | Fake `gh` empty stdout / exit 8 → one JSON line, exit 0, `state=polling`; T-104 still greps | FR-W8-7..9 |
| `.dev/specs/pr-submit-ci-monitor.md` | Amend FR-CI-1, §4 last paragraph, FM-CI-7 to match the table | Parent currently forbids the fix |

Do **not** edit: `fsm.py`, `classifier.py`, `models.py` EventType,
`loop_guard.py`, command `--monitor` parser.

After skill edits: `make sync-dev` (do not stage `.claude/` mirrors).

Rollback: revert SKILL gate + `as_array` default + the one
`classify_checks` branch. Table in `ci-poll.md` rolls back with them.

---

## 6. Test plan

Existing `tests/pr_submit/test_ci_classify.py` stays green, including
`test_classify_pending` and `test_classify_empty`.

| Test | Asserts | Falsifies |
|------|---------|-----------|
| `test_classify_pending` (existing) | `bucket=pending` → `polling` | Regression on the already-correct path |
| `test_classify_empty` (existing) | `{"checks": []}` and `{}` → `clean` | Accidental hang on no-Actions |
| **new** `test_classify_empty_polling_state` | `{"state": "polling", "checks": []}` → `polling` | Parse-fail classified as clean |
| **new** `test_classify_empty_clean_state` | `{"state": "clean", "checks": []}` → `clean` | Coarse `clean` still means no Actions |
| **new** poller: empty stdout, `gh` exit 0 | stdout is one JSON object; `checks == []`; `state == "clean"`; process exit 0 | `--argjson` death; false polling on no Actions |
| **new** poller: empty stdout, `gh` exit 8 | one JSON line; `state == "polling"`; `checks == []`; process exit 0 | Exit 8 empty treated as crash or as clean |
| **new** poller: `--required` stdout `""`, all-checks a pending array | fallback uses all-checks; classify `polling` | Empty string skips FR-CI-11 fallback |
| **new** poller: `jq --argjson` never passed `""` | helper output is `[]` or a JSON array | Abort path B |
| T-104 static grep (existing) | no bare `gh` in poller / SKILL scripts | Unscoped `gh` |
| EventType count (existing) | still 37 | Accidental new member |
| **static** SKILL.md / `ci-poll.md` | Wave 8 table includes `HALT_MAX_ROUNDS` wait-only; does not say "clean / REPORT_ONLY only" | Abort path A left as docs-only |
| `make verify-sync` | `src/` and `.claude/` match after `make sync-dev` | Mirror drift |

No `transition()` tests that pass `source=`. `fsm.py` is not in the diff.

Runnable check for the poller logic: a fake `gh` on `PATH` that prints
nothing and exits 8; script must exit 0 with parseable JSON
`state=polling`.

---

## 7. Risks

| Risk | Ceiling | Mitigation / when to add |
|------|---------|--------------------------|
| 600s after source-flip is shorter than `test.yml` 3.10/3.11/3.12 | `TERMINAL_TIMEOUT` while jobs still pending | Measure on PR #237 after this delta. If it fires, raise CI wait in the SKILL by reusing `--timeout` (operator flag) or a SKILL-only floor. Still no `--ci-timeout` until that measurement. |
| SKILL continuing after an FSM terminal confuses `--resume` / run-log | Resume restarts Augment poll (parent §14 skip) | Document: wait-only is in-session only. Add `--resume` `source=ci` when someone actually resumes mid-CI. |
| Wait-only after halt leaves a red matrix unfixed | Shared budget already spent | Intended. Operator raises `--max-rounds` and re-runs. Do not add a CI-only budget in this delta. |
| Coarse `state` + empty `checks` dual-use | SKILL or a future poller sets `state:polling` on no-Actions | Contract: `state:polling` + empty checks is **only** for incomplete/failed fetch (FR-W8-8). Successful `[]`/`[]` is `state:clean`. |
| Entry table lives in two places (SKILL + ref) | Drift | Table is canonical in `ci-poll.md`; SKILL.md is a one-line pointer + wait-only behavior. |
| `HALT_MAX_ROUNDS` intercept looks like an FSM change in review | Reviewer edits `fsm.py` "to be clean" | INV-W8-1 is a reject criterion. Same pattern as Augment-clean intercept. |

---

## 8. Success criteria (from seed, restated as checks)

- While any check in the chosen list is `pending`, classify is `polling`
  and the Monitor keeps looping.
- Poller always emits one JSON line, exit 0, even on empty stdout / exit 8.
- Wave 8 runs after Augment `HALT_MAX_ROUNDS` (wait-until-complete; CI
  auto-fix remains budget-gated).
- `checks=[]` is `clean` only for a successful empty required+all poll,
  never when the poller failed to parse.
- Existing unit tests stay green; empty-stdout and pending-until-done
  cases are added.

---

## 9. Skipped (add when)

| Skip | Add when |
|------|----------|
| `--ci-timeout` | Operators hit `TERMINAL_TIMEOUT` on still-pending green CI after clock reset |
| Separate CI `max_rounds` | Wait-only after Augment halt leaves parseable CI failures that operators want auto-fixed without raising the Augment budget |
| `poll_ok` payload key | Coarse `state` disambiguation collides in production |
| `--resume` restores `source=ci` | Someone resumes mid-CI wait |
| Parallel Augment+CI poll | Sequential wait is routinely the long pole |
| `gh run rerun` | Measured flake rate on VAL-green pushes |
| New skill / FSM / EventType / `--monitor` 4 | Never for this problem |
