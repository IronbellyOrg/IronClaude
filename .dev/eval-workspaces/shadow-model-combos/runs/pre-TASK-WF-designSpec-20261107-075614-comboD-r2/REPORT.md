# Reflect REPORT: pre-execution audit of the pr-submit merge guard plan (UC-1)

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.66
citations_total: 151
citations_revalidated: 72
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 72` — the validator re-Read all 61 citations of the 14 merged findings and 11 of the 90 inferred-requirement rows (the other 79 rows passed the script's verbatim-quote check, not a validator re-Read).
> - `citations_dropped: 1` — drops observed in the sample only (M-001, `tasklist:168` is the "Acceptance criteria:" header; the criteria start at 169). This is the field that gates promotion (not applicable in UC-1).
> - `citations_dropped_extrapolated: 2` — `round(1 x (151 / 72))`. Recording-only.
> The extrapolated value is telemetry, not a verdict. The sample-count is what the validator actually examined; the extrapolation is what it would have found if the budget had permitted a full re-Read.

## Summary

- Spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (design spec v3, 378 lines). Plan: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (13 tasks).
- Result: **0 blocking findings, 6 MAJOR and 8 MINOR non-blocking.** The plan is executable with amendments; status is `partial` because the evidence validator dropped one citation, and the debate convergence is `BLOCKED_BY_INVARIANTS` (one HIGH invariant, INV-001, stayed unaddressed at depth standard).
- Coverage: `coverage_pct` null (the spec's FR-/F-/G-/O- labels do not match the ID regex, so 0 parsed ids); `coverage_pct_union` 0.8222 (74 of 90 inferred rows matched by word-overlap); `coverage_degraded: parsed-sparse` forced Tier 2 together with the `--tier 2` pin. All 16 unmatched rows have a covering task on a manual read, so the gap list below does not come from them.
- Tier 2 panel: 3 reviewers (analyzer / qa / refactorer) on the sonnet, haiku and opus classes, 3 of 3 complete, 19 findings, 19 of 19 calibrated; adversarial debate at depth standard (2 rounds plus invariant probe), convergence 0.9524 (20 of 21 points), merged into 14 findings.
- Attribution: the plan was already executed (PR #428). Findings are plan or spec defects only; nothing here rests on post-implementation HEAD state, except the corroboration noted in M-001 that the shipped code added a `REBIND` action (`src/superclaude/pr_submit/merge_guard.py:438-442`).
## Merged findings

All findings are Grounded (cited lines re-read by the evidence validator). UC-1 has no deviation classes; severity and blocking are the Round 2 rulings.
### Finding M-001 (MAJOR, blocking: no): The guard record's cycle_id is never set or rebound by any fold row

- **Category:** missing-requirement
- **Sources:** V1 F1, V2 F4
- **Claim:** The guard record's cycle_id is never set or rebound by any fold row, yet held_cycle_published and resume row 4 key on it; engage row 7 returns NOOP for a later cycle, and no decision row enforces once-per-cycle (a RELEASED guard re-engages at row 11).
- **Citations:** source.md:190-206, 139, 143, 108, 166; tasklist:52-60 (SPEC = `source.md`, PLAN = `tasklist` in `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`)
### Finding M-002 (MAJOR, blocking: no): Task 8 builds refs/merge-guard.md from spec sections 3

- **Category:** contradiction
- **Sources:** V1 F2
- **Claim:** Task 8 builds refs/merge-guard.md from spec sections 3, 4.1, 4.5, 4.6, 5 while the spec says it carries sections 3 and 4.1 to 4.4; event fields, key format and the --read JSON are not required by any criterion.
- **Citations:** source.md:240; tasklist:124 (SPEC = `source.md`, PLAN = `tasklist` in `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`)
### Finding M-003 (MAJOR, blocking: no): After a failed first engage the guard is RELEASE_PENDING with owned_draft false and engage row 6 holds without

- **Category:** missing-requirement
- **Sources:** V1 F4
- **Claim:** After a failed first engage the guard is RELEASE_PENDING with owned_draft false and engage row 6 holds without re-checking the live draft; reachable on resume or a later cycle, not covered by any task criterion.
- **Citations:** source.md:199, 138, 170; tasklist:60, 70 (SPEC = `source.md`, PLAN = `tasklist` in `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`)
### Finding M-004 (MAJOR, blocking: no): No criterion checks that the protocol passes this cycle's applied_edits (not the run-wide count) to release_de

- **Category:** unpassable-check
- **Sources:** V2 F1, F9
- **Claim:** No criterion checks that the protocol passes this cycle's applied_edits (not the run-wide count) to release_decision, and Task 1's O1 criterion passes whether or not a single cycle-id source exists. Fails closed.
- **Citations:** source.md:107, 366, 251; tasklist:75, 37, 127-130, 166 (SPEC = `source.md`, PLAN = `tasklist` in `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`)
### Finding M-005 (MAJOR, blocking: no): Release row 7 (zero edits) precedes the head check

- **Category:** safety
- **Sources:** INV-001
- **Claim:** Release row 7 (zero edits) precedes the head check, so a zero-edit cycle after a committed but unpublished earlier cycle releases the PR while that earlier fix was never pushed; the plan tests only a zero after a published cycle. Unresolved HIGH invariant.
- **Citations:** source.md:155-156, 69, 107; tasklist:75 (SPEC = `source.md`, PLAN = `tasklist` in `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`)
### Finding M-006 (MAJOR, blocking: no): Resume row 4 (published) is evaluated before rows 5 and 6

- **Category:** contradiction
- **Sources:** V1 F5
- **Claim:** Resume row 4 (published) is evaluated before rows 5 and 6, and the spec never says where resume gets target_sha; task 4 tests published=True only with no dangling branch.
- **Citations:** source.md:166-168, 156; tasklist:77 (SPEC = `source.md`, PLAN = `tasklist` in `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`)
### Finding M-007 (MINOR, blocking: no): The spec says a draft_guard_unavailable halt reports unavailable

- **Category:** contradiction
- **Sources:** V1 F3
- **Claim:** The spec says a draft_guard_unavailable halt reports unavailable, but read-failed and unreadable-timeline engage halts write no event, so guard_status returns released; plan pins no record at ordinal 3 as released.
- **Citations:** source.md:112, 135, 140; tasklist:61 (SPEC = `source.md`, PLAN = `tasklist` in `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`)
### Finding M-008 (MINOR, blocking: no): guard_status OFF wording can hide a held draft that resume row 2 must report

- **Category:** contradiction
- **Sources:** V1 F6, F7
- **Claim:** guard_status OFF wording can hide a held draft that resume row 2 must report, and resume row 6 has no phase condition unlike row 5.
- **Citations:** source.md:112, 164, 167-168; tasklist:61, 77 (SPEC = `source.md`, PLAN = `tasklist` in `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`)
### Finding M-009 (MINOR, blocking: no): One cycle id shared by guard events

- **Category:** missing-requirement
- **Sources:** V2 F3
- **Claim:** One cycle id shared by guard events, push key and rereview_requested is required; the acceptance trace asserts event order only.
- **Citations:** source.md:251; tasklist:170 (SPEC = `source.md`, PLAN = `tasklist` in `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`)
### Finding M-010 (MINOR, blocking: no): The PR body release-gate statement and the --merge-guard off rule for the opening run have no producing task a

- **Category:** missing-requirement
- **Sources:** V2 F5
- **Claim:** The PR body release-gate statement and the --merge-guard off rule for the opening run have no producing task and no criterion.
- **Citations:** source.md:326; tasklist:33, 182 (SPEC = `source.md`, PLAN = `tasklist` in `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`)
### Finding M-011 (MINOR, blocking: no): Several stated requirements sit only in task bodies: Task 9 flag and wave-line tests

- **Category:** missing-requirement
- **Sources:** V2 F6, F7, F8, F10, F11
- **Claim:** Several stated requirements sit only in task bodies: Task 9 flag and wave-line tests, the no file:NNN rule outside Task 8, original_is_draft never re-read, the engage-failure message; Task 10 lacks a Depends on Task 8 line.
- **Citations:** tasklist:137, 139-144, 124, 128, 148, 129; source.md:363, 369, 274 (SPEC = `source.md`, PLAN = `tasklist` in `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`)
### Finding M-012 (MINOR, blocking: no): The byte-identical check compares live text with a start-text constant

- **Category:** unpassable-check
- **Sources:** V2 F2
- **Claim:** The byte-identical check compares live text with a start-text constant, so a changed tail would pass; weak because the spec mandates literal constants.
- **Citations:** tasklist:154; source.md:377 (SPEC = `source.md`, PLAN = `tasklist` in `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`)
### Finding M-013 (MINOR, blocking: no): Task 2's grep criterion for 43 is a judgment call because a legitimate 42nd-43rd comment remains.

- **Category:** unpassable-check
- **Sources:** V3 F1
- **Claim:** Task 2's grep criterion for 43 is a judgment call because a legitimate 42nd-43rd comment remains.
- **Citations:** tasklist:49 (SPEC = `source.md`, PLAN = `tasklist` in `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`)
### Finding M-014 (MINOR, blocking: no): Advisory: a conflict cycle arriving while the guard is HELD

- **Category:** other
- **Sources:** INV-002..004
- **Claim:** Advisory: a conflict cycle arriving while the guard is HELD, the trace holding by construction, and the auto-merge disarm note have no criterion.
- **Citations:** source.md:149, 143, 333, 270; tasklist:166, 170, 153 (SPEC = `source.md`, PLAN = `tasklist` in `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`)
## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | engage at the first verified Medium-or-higher finding routed to a fix | source.md:6 | Task 8 (0.875) |
| INF-002 | release when the fix push is confirmed on the PR head, before replies and the re-trigger | source.md:6 | Task 8 (0.889) |
| INF-003 | an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports | source.md:6 | Task 8 (0.778) |
| INF-004 | Nothing mutates. A held guard found in the log is reported with the clear command. | source.md:57 | none (0.556); manual read: covered |
| INF-005 | Wave 0 loads the ref (Resume and Exit report) before Wave 1: unsettled requests are reconciled before any edit, release or re-trigger; a held guard is reported with the clear command. | source.md:58 | Task 8 (0.722) |
| INF-006 | Wave 0 prints once: "Remediation is unprotected: --merge-guard off." No draft call is made. | source.md:59 | Task 9 (1.0) |
| INF-007 | The line is written in the SKILL.md output table, which every run loads, not only in the guard ref. | source.md:60 | Task 9 (0.9) |
| INF-008 | Read, decide, request, `--to draft`, settle. Print the clear command once. | source.md:61 | Task 8 (0.667) |
| INF-009 | Settle `skipped/already_draft`, phase `disabled`, never mutate. | source.md:62 | Task 3 (0.857) |
| INF-010 | Diagnosis ends with no edit (`applied_edits == 0`) | source.md:63 | none (0.5); manual read: covered |
| INF-011 | Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing. | source.md:64 | Task 8 (1.0) |
| INF-012 | Release, cause `pushed`, before reply, resolve and the S5a re-trigger. | source.md:65 | Task 8 (0.75) |
| INF-013 | Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, report. | source.md:66 | none (0.545); manual read: covered |
| INF-014 | Do not release; report `held (timeline unreadable)`; keep pushing. | source.md:67 | Task 8 (0.714) |
| INF-015 | Halt before any edit: `terminal_halted`, reason `draft_guard_unavailable`. | source.md:68 | Task 8 (1.0) |
| INF-016 | PR stays draft; report `held` with the clear command. | source.md:69 | Task 8 (0.857) |
| INF-017 | No `gh` or `git` word on any line, comments included (F6). Imports only `enum`, `dataclasses`, `re`, `.conflicts.is_conflict_cycle`. | source.md:75 | Task 3 (0.769) |
| INF-018 | Never collides with `CONFLICT_CYCLE_PREFIXES`. | source.md:101 | Task 3 (0.667) |
| INF-019 | 1 + the highest `<kind>-<n>` seen in any event's `cycle_id`; 1 when none. | source.md:102 | Task 3 (0.667) |
| INF-020 | Guard requests with no matching settle, matched by `idempotency_key` | source.md:104 | Task 3 (0.833) |
| INF-021 | `applied_edits` is THIS cycle's count of applied edits; it is not the run-wide `applied_edits` output field | source.md:107 | Task 4 (1.0) |
| INF-022 | `True` when `guard` is not `None` and the log holds a `push_completed` event whose `cycle_id` equals `guard.cycle_id` | source.md:108 | Task 3 (0.778) |
| INF-023 | a test imports both modules and asserts equality, because the core cannot import `recovery`. | source.md:109 | none (0.455); manual read: covered |
| INF-024 | phase `DISABLED` with cause `already_draft` gives `off` (the PR was a draft before the run, nothing is guarded) | source.md:112 | Task 3 (0.727) |
| INF-025 | A halt with reason `draft_guard_unavailable` reports `unavailable`. | source.md:112 | Task 8 (0.8) |
| INF-026 | `classify_toggles(guard, read)` (the only foreign-toggle test; no actor identity, F11): | source.md:114 | Task 4 (0.667) |
| INF-027 | `failed_mutations` keeps a call that failed on the client but landed on the server from being read as a user action | source.md:127 | Task 4 (0.6) |
| INF-028 | `mode == OFF`, or `ordinal < 3`, or `is_conflict_cycle(cycle_id)` | source.md:133 | Task 3 (1.0) |
| INF-029 | `RETRY_RELEASE` (release first, then re-decide) | source.md:137 | Task 1 (0.6) |
| INF-030 | `guard` exists and `classify_toggles == "foreign"` | source.md:141 | Task 4 (0.75) |
| INF-031 | `guard is None` and `read.is_draft` | source.md:142 | Task 3 (0.75) |
| INF-032 | `ENGAGE`; `notes` carries `auto_merge_armed` when set | source.md:143 | Task 4 (0.8) |
| INF-033 | `push_completed` and `read.head_sha == target_sha` | source.md:156 | Task 4 (0.75) |
| INF-034 | `HOLD(head_mismatch or push_not_completed)` | source.md:157 | none (0.333); manual read: covered |
| INF-035 | `(ordinal < 3 or mode == OFF)` and phase not in (`RELEASED`, `DISABLED`) | source.md:164 | Task 3 (1.0) |
| INF-036 | `RECONCILE`, with `reason` one of `resume_reconciled`, `not_applied`, `ambiguous` | source.md:165 | Task 4 (1.0) |
| INF-037 | re-enter `release_decision` with `push_completed=True` | source.md:166 | Task 4 (1.0) |
| INF-038 | `dangling_branch == "not_landed"` and phase `HELD` | source.md:167 | Task 4 (1.0) |
| INF-039 | `HOLD(ambiguous_remote_tip)` | source.md:168 | Task 4 (1.0) |
| INF-040 | Add to `EventType` in `models.py` (43 to 45, update the docstring and the `models.py:3,24` count, and the 43 text at `run_log.py:117`): | source.md:175 | Task 2 (0.769) |
| INF-041 | appended and fsynced BEFORE the draft/ready call | source.md:178 | Task 7 (0.6) |
| INF-042 | `idempotency_key` = `guard:<run_id>:<cycle_id>:<to>:a<k>` (`k` = 1 + prior requests with the same cycle and direction) | source.md:184 | Task 3 (0.667) |
| INF-043 | default `None`, added to `_NEW_KEY_DEFAULTS` | source.md:187 | Task 5 (0.75) |
| INF-044 | It is NOT `DISABLED`, so a crash before the call does not leave later cycles unguarded. | source.md:201 | none (0.429); manual read: covered |
| INF-045 | `original_is_draft` is never read from GitHub after the first record, so a resumed run cannot mistake its own draft for an original one. | source.md:208 | none (0.5); manual read: covered |
| INF-046 | The matcher `pending_requests` uses the same key pairing as `detect_crash_window`, but over the two guard event types, so push recovery and guard recovery stay independent. | source.md:210 | none (0.467); manual read: covered |
| INF-047 | `choices=["draft", "off"]` (same shape as `--conflict-max-tier`, F5) | source.md:214 | Task 6 (0.667) |
| INF-048 | Effective only at `--monitor 3`; accepted and inert below. | source.md:216 | none (0.4); manual read: covered |
| INF-049 | `RunConfig` and `run_skill` do not change (F5): the guard is SKILL-orchestrated. | source.md:217 | none (0.429); manual read: covered |
| INF-050 | `set -euo pipefail`, same `die`, same `--repo` resolution from the origin remote, numeric `--pr` check, exit 127 when `gh` or `jq` is missing. | source.md:221 | Task 7 (0.882) |
| INF-051 | Exit codes: 0 success; 1 `gh` failure or failed verification (the JSON line is still printed with `ok:false`); 2 usage; 127 missing dependency. | source.md:234 | Task 7 (0.706) |
| INF-052 | `--to` is idempotent, so a retry or a resume re-issue is safe. | source.md:234 | none (0.5); manual read: covered |
| INF-053 | Loaded lazily at L3 Wave 3, Wave 6 and Wave 8. | source.md:240 | Task 8 (0.75) |
| INF-054 | No new python fence (the one-fence tests, | source.md:241 | Task 9 (1.0) |
| INF-055 | Its event-type enumeration says the enum has 43 members; update it to 45 and name `draft_guard_requested` and `draft_guard_settled`, without the words `gh` or `git` | source.md:242 | Task 2 (1.0) |
| INF-056 | Overlay note: the guard phases are fold values, not `MonitorState` members. | source.md:243 | Task 10 (0.875) |
| INF-057 | `--merge-guard {draft,off}` in the argument-hint and the Options table; a short "Merge guard" section next to "Merge-conflict handling". | source.md:244 | Task 12 (1.0) |
| INF-058 | Flag row and a paragraph: what it does, the clear command, `held` meaning, default on. | source.md:245 | Task 13 (0.778) |
| INF-059 | A `held` report always carries the reason and `gh pr ready <N> --repo <REPO>` | source.md:247 | Task 8 (0.889) |
| INF-060 | The SKILL mints it at the end of Wave 3 and uses the same id as the `cycle_id` of the push triad (`push_idempotency_key`) and of `rereview_requested`, so the guard, the push and the re-trigger of one cycle share a key. | source.md:251 | Task 8 (0.789) |
| INF-061 | With `--merge-guard off` nothing changes. | source.md:251 | Task 8 (0.8) |
| INF-062 | is a hit of `WRITE_VERB_RE` and needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` | source.md:255 | Task 9 (0.8) |
| INF-063 | The `read-only` category is not used for these calls (a `gh pr ready` mutation is never read-only). | source.md:255 | Task 7 (0.889) |
| INF-064 | Acceptance trace (must appear in this order in the run log) | source.md:270 | Task 11 (0.833) |
| INF-065 | next checkpoint: `state != OPEN` -> halt `pr_not_open`, nothing pushed, report the local commit `<target_sha>`. | source.md:281 | Task 8 (0.75) |
| INF-066 | Record `make lint`, `uv run ruff format --check src/ tests/` and the full-suite result | source.md:301 | Task 1 (0.923) |
| INF-067 | so the final task runs the FULL suite (`uv run pytest -q tests`) and compares its failures with the base-commit record. | source.md:301 | Task 1 (0.857) |
| INF-068 | Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/` | source.md:301 | Task 8 (0.917) |
| INF-069 | the final task also runs `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q` | source.md:301 | Task 13 (1.0) |
| INF-070 | export the public guard names | source.md:291 | Task 5 (1.0) |
| INF-071 | fake `gh` on PATH, exit codes 0/1/2/127, `--repo` on every call, an old log folds to `draft_guard: None` | source.md:320 | Task 7 (0.692) |
| INF-072 | A static test asserts `merge_guard.py` has no `gh` or `git` word. | source.md:322 | Task 3 (1.0) |
| INF-073 | a test that `BRANCH_LANDED`, `BRANCH_NOT_LANDED` and `BRANCH_AMBIGUOUS` equal the `recovery.py` constants | source.md:322 | Task 3 (1.0) |
| INF-074 | a crash after a normal `push_completed` (no dangling window, `published` true) releases before the re-trigger | source.md:318 | Task 11 (1.0) |
| INF-075 | ledger test: observed above `run_toggles + slack`; ready-then-draft round trip (FR-12, FR-13) | source.md:316 | none (0.538); manual read: covered |
| INF-076 | No task makes a live PR call, and the run that opens the PR must not enable the feature (`--merge-guard off`). | source.md:326 | Task 1 (0.833) |
| INF-077 | The user guide states that draft behaviour is unverified until then, and the PR body states the gate plainly. | source.md:326 | Task 1 (1.0) |
| INF-078 | Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, the test that asserts the event count), never by bare line number | source.md:362 | none (0.562); manual read: covered |
| INF-079 | Declare dependencies completely, one `Depends on:` line per dependency | source.md:363 | none (0.429); manual read: covered |
| INF-080 | The protocol wiring covers the Wave 0 resume and `off` hook as well as Waves 3, 6 and 8 (section 4.5), with a test for each bullet. | source.md:364 | none (0.583); manual read: covered |
| INF-081 | The fold, `guard_status`, resume-reason and per-cycle `applied_edits` rules of sections 3 and 4.1 each get an acceptance criterion that a wrong implementation would fail. | source.md:366 | none (0.429); manual read: covered |
| INF-082 | The pre-build record task states the release-gate decision of section 8 and records the base-commit lint result. | source.md:367 | Task 1 (0.857) |
| INF-083 | Protocol prose written by the plan never carries `file:NNN` pointers and never contains the words `evidence-validator` or `conflict-intent.md` on a new SKILL.md line. | source.md:369 | Task 10 (0.737) |
| INF-084 | each ends with adding its `WRITE_VERB_CLASSIFICATION` entries (exact stripped line, category `never-worker`) and runs `uv run pytest tests/skills/test_worker_contract.py -q`. | source.md:373 | Task 8 (0.833) |
| INF-085 | The L2 line is written into the SKILL.md output table; its acceptance criterion is a test that the literal line is in `SKILL.md` | source.md:374 | Task 9 (0.909) |
| INF-086 | the crash scenario tests derive branches from a real `RunLog` through `detect_crash_window` and `resolve_crash_window` | source.md:375 | Task 11 (0.8) |
| INF-087 | scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions (pytest would collect them twice) | source.md:377 | Task 11 (0.786) |
| INF-088 | is asserted on `RunLog.read_events()` | source.md:377 | Task 2 (0.667) |
| INF-089 | the byte-identical checks for the pinned S5a and Wave 6 pre-push sentences compare against literal string constants taken from the existing pins, not against `git show HEAD:` | source.md:377 | Task 10 (0.8) |
| INF-090 | the Wave 0 bullet sits before the Wave 1 bullet and has no L3 or `draft` condition. | source.md:378 | Task 9 (1.0) |

POSTSCRIPT: 0 inferred rows were dropped (all 90 quotes are verbatim on their cited line by script; 11 re-read by the validator, 11 of 11 founded). `coverage_pct_union` 0.8222, `unmapped_requirements_union` 16 ids (INF-004, 010, 013, 023, 034, 044, 045, 046, 048, 049, 052, 075, 078, 079, 080, 081), `S_dev_density` 0.1778, all unchanged by the validator.

## Tier 2 panel and shadow-mode notes

- Panel resolution (`panel/resolution.json`): sonnet (t1b-1), haiku (t4-1), opus (t1a-1); `panel_parity: true`. This run's alias env: sonnet = `claude-gw-tier1b[1m]`, haiku = `claude-haiku-5-5`, opus = `gpt-6-luna`; the resolution records the class rotation, not the served model.
- Identity: `identity_source: requested-pinned`. Reviewer 3 self-reported `gpt-6-luna` against the pin `claude-opus-5-5`, so `identity_mismatch_suspected: true` (expected for this alias set, not an error). Reviewers 1 and 2 self-reported `claude-gw-tier1b[1m]` and `claude-haiku-5-5`. No claim of verified independence is made.
- Calibration: every card calibrated blind by the opus class; the opus class is also reviewer 3's class, so `calibrator_diversity: degraded`. Card scores 0.67 / 0.71 / 0.61; T1 card 0.64.
- Debate: orchestrator and judge are `claude-gw-tier1b[1m]` (sonnet class), the same class as reviewer 1, so `judge_class_collision: true`. The dual-pass position-bias check was not run as two independent evaluations (`fallback_mode: true`).
- Cluster agreement 0.3357 is telemetry only; the cluster command grouped seven distinct reviewer-1 findings with reviewer 3's single finding in cluster C1 (identical fingerprint with empty refs), so it understates both agreement and distinctness.
- Pre-check: 8 quote-not-found flags, all reviewer 2's quotes with markdown backticks stripped; the merged citations are line ranges and were re-read by the validator.

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 151` = 0.00

## Recommendations

### Recommendation R-001: Define when the guard's cycle_id is set and how a later cycle reuses a held draft
- **File:** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (fold effect table and engage rows) and Task 3 of the plan
- **Change:** Add a fold effect row that sets `cycle_id` on a request and a decision for "later cycle finds the guard HELD" (rebind or refuse), and state which function enforces "once per cycle id".
- **Verifier:** a Task 3 fold test and a Task 4 engage test that fail if `cycle_id` stays stale or a RELEASED guard re-engages for the same id; `uv run pytest tests/pr_submit/test_merge_guard.py -q`
- **Linked deviation(s):** M-001
- **Priority:** P1

### Recommendation R-002: Resolve the zero-edit release against an unpublished earlier cycle
- **File:** `source.md` release table (rows 7 and 8) and plan Task 4
- **Change:** Say whether `applied_edits == 0` may release when an earlier cycle's fix is committed but unpublished, and add the missing release condition or an explicit accepted-risk sentence.
- **Verifier:** a Task 4 test with an earlier HOLD cycle followed by a zero-edit cycle asserts the chosen outcome
- **Linked deviation(s):** M-005, M-004
- **Priority:** P1

### Recommendation R-003: Restore spec sections 4.2 to 4.4 to Task 8 and add a call-site criterion for the per-cycle edit count
- **File:** plan Task 8 (source sections and acceptance criteria)
- **Change:** Change "sections 3, 4.1, 4.5, 4.6 and 5" to cover 3 and 4.1 to 4.4, 4.5, 4.6 and 5; add criteria that the ref names the event fields (`timeline_baseline`, `original_is_draft`, the idempotency key) and passes this cycle's applied-edit count, and make Task 1's O1 criterion require a single named source.
- **Verifier:** `uv run pytest tests/pr_submit/test_merge_guard_protocol.py -q` with new phrase assertions
- **Linked deviation(s):** M-002, M-004
- **Priority:** P1

### Recommendation R-004: Decide the failed-first-engage and resume row cases
- **File:** `source.md` engage row 6 and resume rows 4 to 6; plan Tasks 3, 4 and 11
- **Change:** Let engage row 6 check the live draft state, say where resume gets `target_sha`, give resume row 6 a phase condition, and add one test per case.
- **Verifier:** Task 4 parametrized tests per row; Task 11 crash scenario test
- **Linked deviation(s):** M-003, M-006, M-008
- **Priority:** P2

### Recommendation R-005: Give each body-only requirement an acceptance criterion and fix the dependency line
- **File:** plan Tasks 1, 9, 10, 11, 12
- **Change:** Add criteria for the flag-row and wave-line tests, the engage-failure message, the shared cycle id across guard, push and re-trigger events, the no `file:NNN` rule outside Task 8, the PR-body gate statement; add `Depends on: Task 8` to Task 10; replace Task 2's grep criterion with an exact-count assertion.
- **Verifier:** each new criterion is a named test; re-read the plan for one `Depends on:` line per consumed task
- **Linked deviation(s):** M-009, M-010, M-011, M-012, M-013
- **Priority:** P2

### Recommendation R-006: Reconcile `guard_status` with the unavailable halt
- **File:** `source.md` `guard_status` mapping and plan Task 3
- **Change:** State what is reported when an engage halt writes no event, and clarify the `OFF` wording.
- **Verifier:** a Task 3 `guard_status` case for the no-record halt
- **Linked deviation(s):** M-007, M-008
- **Priority:** P2
