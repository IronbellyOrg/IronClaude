# Reflect REPORT (UC-1 pre-execution): merge-guard design spec vs. its 13-task plan

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.71
citations_total: 51
citations_revalidated: 51
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```


Run: `pre-TASK-WF-designSpec-20261107-075614-comboB-r3` (tier 2 pinned, engine shadow). Spec: `source.md` (378 lines). Plan: `TASK-WF-designSpec-20261107-075614.md` (200 lines, 13 tasks).
Status is **partial** because the evidence validator dropped 1 of 51 report citations (see Dropped citation). Code facts are checked at base commit e8db2fe6 (`artifacts/base-grounding.md`); HEAD has since gained the landed feature and is not evidence of what the plan could know.

## Verdict

The plan is largely faithful to the spec: all 12 named scenario tests, every section 4.1 decision table, the fold table, the flag, the script, the ref and the docs are carried by a task. No blocking finding. One MAJOR non-blocking defect and 14 MINOR findings remain (15 merged findings: the 11 reviewer findings combined into 9, plus 5 fault-finder items and the engage-row ordering quirk raised in the debate).

- **Fix before execution (F1, MAJOR):** `resume_decision` row 4 says to re-enter `release_decision`, but its signature has no `applied_edits` or `target_sha`, `GuardAction` has no re-enter member, and Task 4's criterion names no action for row 4. Give `resume_decision` those two inputs (and say what row 4 returns), or state that the SKILL performs the re-entry.
- **Cheap plan edits (F3, F4, F5, F7):** rename or retarget Task 12's grep, require boolean `autoMergeRequest` in Task 7, drop the conditional `_RESOLUTION_SCRIPTS` wording, add `Depends on: Task 1` to Tasks 9, 10, 12, 13.
- **Spec gaps the plan inherits (F10, F11, F12, F13, F15):** `disabled_cause` for `user_override`, the `cycle_id` update rule, the report value for a halt before any request, a zero-edit release over an earlier hold, and the null-guard order of the engage rows.

## Coverage (UC-1)

- Pass 1 (regex): 0 parsed IDs (the spec's labels do not match `R-/REQ-/SPEC-/T-`). `coverage_pct: null`.
- Pass 2 (inference): 75 quote-pinned rows, 61 matched by the 0.6 containment rule; `coverage_pct_union: 0.8133`. `coverage_degraded: parsed-sparse` forbade a Tier-1 stop.
- The 14 mechanically unmatched rows were read by hand: 12 are covered by a task whose wording differs from the quote (for example INF-021 by Task 3, INF-023 by Task 4, INF-055 by Task 13); two have no acceptance criterion (INF-036 inertness below ordinal 3, INF-037 `RunConfig` unchanged), both MINOR and not raised as findings.

## Findings (merged, validated)

### F1 (MAJOR, non-blocking, contradiction)

resume_decision row 4 says re-enter release_decision, but the signature lacks applied_edits and target_sha (needed by release rows 7-8), GuardAction has no re-enter member, and Task 4 names no returned action for row 4, so a wrong implementation passes.

Evidence: spec source.md:109; spec source.md:166; spec source.md:155-156; plan plan.md (TASK-WF-designSpec-20261107-075614.md):70; plan plan.md (TASK-WF-designSpec-20261107-075614.md):77.

### F2 (MINOR, non-blocking, missing-requirement)

No criterion checks that the push events and rereview_requested carry the cycle id minted for the guard; Task 8 checks only where it is minted and Task 11 only event order. A mismatch leaves held_cycle_published false and the PR draft (fail-safe).

Evidence: spec source.md:251; spec source.md:108; plan plan.md (TASK-WF-designSpec-20261107-075614.md):127; plan plan.md (TASK-WF-designSpec-20261107-075614.md):170-171.

### F3 (MINOR, non-blocking, unpassable-check)

Task 12 expects grep -n "merge-guard" to show the section heading, but the plan names the section "Merge guard" (with a space); the hyphenated grep cannot match that heading.

Evidence: plan plan.md (TASK-WF-designSpec-20261107-075614.md):182; plan plan.md (TASK-WF-designSpec-20261107-075614.md):185.

### F4 (MINOR, non-blocking, missing-requirement)

No task requires the script to turn gh's autoMergeRequest object or null into the boolean the spec example shows and GuardRead.auto_merge_armed needs; Task 7's criterion only checks that the key is printed.

Evidence: spec source.md:230; spec source.md:89; plan plan.md (TASK-WF-designSpec-20261107-075614.md):111.

### F5 (MINOR, non-blocking, other)

Task 7's criterion that the script passes the _RESOLUTION_SCRIPTS tests is vacuous if the executor, per the conditional wording, decides not to add the script to that list.

Evidence: plan plan.md (TASK-WF-designSpec-20261107-075614.md):108; plan plan.md (TASK-WF-designSpec-20261107-075614.md):113.

### F6 (MINOR, non-blocking, missing-requirement)

No criterion checks the written event key format guard:<run_id>:<cycle_id>:<to>:a<k> or the first-request-only timeline_baseline at the point of writing; Tasks 3 and 5 test only the fold side, and Task 8 omits spec section 4.2.

Evidence: spec source.md:184-185; plan plan.md (TASK-WF-designSpec-20261107-075614.md):60-62; plan plan.md (TASK-WF-designSpec-20261107-075614.md):124.

### F7 (MINOR, non-blocking, other)

Spec section 10 requires one Depends on line per consumed output, but Tasks 9, 10, 12 and 13 read ./artifacts/pre-build-gate.md without listing Task 1; the dependency holds only transitively, so no implementation outcome changes.

Evidence: spec source.md:363; plan plan.md (TASK-WF-designSpec-20261107-075614.md):134-137; plan plan.md (TASK-WF-designSpec-20261107-075614.md):148-150; plan plan.md (TASK-WF-designSpec-20261107-075614.md):179-182; plan plan.md (TASK-WF-designSpec-20261107-075614.md):190-195.

### F8 (MINOR, non-blocking, missing-requirement)

Spec section 10 bans file:NNN pointers in the plan's protocol prose, but no criterion checks for them: Task 8's protocol test checks only src/superclaude and the SKILL.md criteria of Tasks 9 and 10 check the fence, src/superclaude and two forbidden words.

Evidence: spec source.md:369; plan plan.md (TASK-WF-designSpec-20261107-075614.md):128; plan plan.md (TASK-WF-designSpec-20261107-075614.md):143; plan plan.md (TASK-WF-designSpec-20261107-075614.md):154.

### F9 (MINOR, non-blocking, other)

The spec never states the string values of Phase, while Task 5 asserts lowercase held and engage_pending; the convention is obvious, but only Task 5 would force it.

Evidence: spec source.md:80; plan plan.md (TASK-WF-designSpec-20261107-075614.md):90.

### F10 (MINOR, non-blocking, missing-requirement)

The fold row for settled(any, skipped, user_override) sets phase and owned_draft but not disabled_cause, yet guard_status needs DISABLED with cause user_override to report user_override; no criterion folds a foreign-toggle log into guard_status.

Evidence: spec source.md:112; spec source.md:206; plan plan.md (TASK-WF-designSpec-20261107-075614.md):60-61.

### F11 (MINOR, non-blocking, missing-requirement)

No fold row sets cycle_id and engage row 7 writes no request for a second cycle while HELD, so after a held release and a crash in the next cycle held_cycle_published can match the earlier cycle's push; no criterion folds a two-cycle log.

Evidence: spec source.md:190; spec source.md:139; spec source.md:108; plan plan.md (TASK-WF-designSpec-20261107-075614.md):62.

### F12 (MINOR, non-blocking, contradiction)

Spec says a draft_guard_unavailable halt reports unavailable, but guard_status has no halt input and engage rows 3 and 8 halt before any request, leaving no guard record, which maps to released; Task 3 asserts that no-record case as released.

Evidence: spec source.md:112; spec source.md:135; spec source.md:140; plan plan.md (TASK-WF-designSpec-20261107-075614.md):61.

### F13 (MINOR, non-blocking, missing-requirement)

Release row 7 (applied_edits == 0) precedes the head check in row 8, and applied_edits is per cycle, so a HELD guard carried from an unpublished earlier cycle is released no_edits by a later zero-edit cycle; Task 4 asserts that release without a publication proof.

Evidence: spec source.md:155-156; spec source.md:107; plan plan.md (TASK-WF-designSpec-20261107-075614.md):75.

### F14 (MINOR, non-blocking, other)

Ordering rules of the ref are checked by phrase presence and only the SKILL.md Wave 6 bullet gets an order assertion, so a ref that releases after the S5a re-trigger could pass; the scenario driver tests the author's own driver, not the prose.

Evidence: plan plan.md (TASK-WF-designSpec-20261107-075614.md):128-129; plan plan.md (TASK-WF-designSpec-20261107-075614.md):153; plan plan.md (TASK-WF-designSpec-20261107-075614.md):166.

### F15 (MINOR, non-blocking, contradiction)

engage_decision rows 2 and 5-7 read guard.phase before row 10 handles guard is None, and Task 4 tests rows by number without stating that a missing guard skips rows 2 and 5-7.

Evidence: spec source.md:134; spec source.md:137-139; spec source.md:142; plan plan.md (TASK-WF-designSpec-20261107-075614.md):73.


Low-severity fault-finder notes, not raised as findings: INV-002 (`release_decision` accepts `RELEASE_PENDING` without an ownership test; flows guard it), INV-007 (the RECONCILE count ignores `failed_mutations`; fails safe), INV-008 (`next_cycle_number` numeric vs text compare; unlikely under the round cap).

## Dropped citation (evidence validator)

- F7, plan lines 148-150: the span shows Task 10 depending on Task 9 only; Task 10 names `pre-build-gate.md` at line 154, outside the span. F7 stands on its other citations (plan 134-137, 179-182, 190-195). This drop forces `status: partial`.

## Tier 2 process

- Reviewers (shadow panel, dispatched with explicit classes): 1 analyzer (sonnet class, pin claude-sonnet-5-5), 2 qa (haiku class, pin claude-haiku-5-5), 3 refactorer (opus class, pin claude-opus-5-5). 11 findings, 3/3 valid findings blocks on first parse, calibration 11/11, `panel_parity: true`.
- Identity: `requested-pinned`. Reviewer 2 self-reported "OpenAI GPT" against its haiku pin: `identity_mismatch_suspected: true`. No claim of verified independence.
- Blind calibration (sonnet-class calibrator; no disjoint class available, `calibrator_diversity: degraded`): T1 0.71, cards 0.70 / 0.61 / 0.70.
- Debate (`sc:adversarial` Mode A, standard): 2 rounds + invariant probe + one verification round; convergence 0.94 (16 of 17 points); base variant 3; `merge_method: adversarial`. Judge = orchestrator (claude-gw-tier1b, sonnet class): class collision with reviewer 1 and the advocates, recorded.
- The fault-finder reported two HIGH invariants; a verification round downgraded them (INV-001 to MEDIUM, INV-002 to LOW), so none blocks convergence.
- Disagreement kept: whether F1 is blocking (advocate 1 yes; advocates 2 and 3 no). Merged as MAJOR, non-blocking.
- Model diversity: `t2_model_class_diversity: full`, `t2_vendor_diversity: single` (all aliases are `claude-gw-*`, warn-only).

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|

| INF-001 | release when the fix push is confirmed on the PR head, before replies and the re-trigger; an unreadable tim... | source.md:6 | containment T8 (0.82) |
| INF-002 | Rule: the core DECIDES and the SKILL performs, the same split as the push triad and the re-trigger (NFR-6).... | source.md:51 | containment T1 (0.60) |
| INF-003 | Nothing mutates. A held guard found in the log is reported with the clear command. | source.md:57 | none (best T8 0.56) |
| INF-004 | Wave 0 loads the ref (Resume and Exit report) before Wave 1: unsettled requests are reconciled before any e... | source.md:58 | containment T8 (0.75) |
| INF-005 | Wave 0 prints once: "Remediation is unprotected: --merge-guard off." No draft call is made. | source.md:59 | containment T9 (1.00) |
| INF-006 | The final report prints "PR #N is still mergeable; this run's fixes are local only." | source.md:60 | containment T9 (0.91) |
| INF-007 | Read, decide, request, `--to draft`, settle. Print the clear command once. | source.md:61 | containment T8 (0.67) |
| INF-008 | Settle `skipped/already_draft`, phase `disabled`, never mutate. | source.md:62 | containment T3 (0.86) |
| INF-009 | Release, cause `no_edits`. | source.md:63 | containment T4 (1.00) |
| INF-010 | Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing. | source.md:64 | containment T8 (1.00) |
| INF-011 | Release, cause `pushed`, before reply, resolve and the S5a re-trigger. | source.md:65 | containment T8 (0.75) |
| INF-012 | Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, report. | source.md:66 | none (best T3 0.55) |
| INF-013 | Do not release; report `held (timeline unreadable)`; keep pushing. | source.md:67 | containment T8 (0.71) |
| INF-014 | Halt before any edit: `terminal_halted`, reason `draft_guard_unavailable`. | source.md:68 | containment T8 (1.00) |
| INF-015 | PR stays draft; report `held` with the clear command. | source.md:69 | containment T8 (0.86) |
| INF-016 | No `gh` or `git` word on any line, comments included (F6). Imports only `enum`, `dataclasses`, `re`, `.conf... | source.md:75 | containment T3 (0.77) |
| INF-017 | `ValueError` otherwise or when `n < 1`. Never collides with `CONFLICT_CYCLE_PREFIXES`. | source.md:101 | containment T3 (0.71) |
| INF-018 | 1 + the highest `<kind>-<n>` seen in any event's `cycle_id`; 1 when none. | source.md:102 | containment T3 (0.78) |
| INF-019 | `applied_edits` is THIS cycle's count of applied edits; it is not the run-wide `applied_edits` output field | source.md:107 | containment T4 (0.90) |
| INF-020 | `True` when `guard` is not `None` and the log holds a `push_completed` event whose `cycle_id` equals `guard... | source.md:108 | containment T3 (0.78) |
| INF-021 | a test imports both modules and asserts equality, because the core cannot import `recovery`. | source.md:109 | none (best T3 0.40) |
| INF-022 | A halt with reason `draft_guard_unavailable` reports `unavailable`. | source.md:112 | containment T8 (0.80) |
| INF-023 | `classify_toggles(guard, read)` (the only foreign-toggle test; no actor identity, F11): | source.md:114 | none (best T4 0.56) |
| INF-024 | `failed_mutations` keeps a call that failed on the client but landed on the server from being read as a use... | source.md:127 | containment T4 (0.60) |
| INF-025 | `mode == OFF`, or `ordinal < 3`, or `is_conflict_cycle(cycle_id)` | source.md:133 | containment T3 (1.00) |
| INF-026 | `not read.complete` or `read.transitions is None` | source.md:140 | containment T4 (1.00) |
| INF-027 | `push_completed` and `read.head_sha == target_sha` | source.md:156 | containment T4 (0.75) |
| INF-028 | live state matching the request's direction and `observed == run_toggles + 1` settles `confirmed, changed: ... | source.md:165 | containment T3 (0.73) |
| INF-029 | re-enter `release_decision` with `push_completed=True` | source.md:166 | containment T4 (1.00) |
| INF-030 | Add to `EventType` in `models.py` (43 to 45, update the docstring and the `models.py:3,24` count, and the 4... | source.md:175 | containment T2 (0.71) |
| INF-031 | # appended and fsynced BEFORE the draft/ready call | source.md:178 | containment T7 (0.60) |
| INF-032 | `fold_draft_guard(events)` returns `None` or this dict, and `run_log.rebuild_state()` stores it as `state["... | source.md:187 | containment T5 (0.77) |
| INF-033 | It is NOT `DISABLED`, so a crash before the call does not leave later cycles unguarded. | source.md:201 | none (best T8 0.43) |
| INF-034 | `original_is_draft` is never read from GitHub after the first record, so a resumed run cannot mistake its o... | source.md:208 | none (best T1 0.50) |
| INF-035 | `DEFAULT_MERGE_GUARD = "draft"` | source.md:214 | containment T6 (1.00) |
| INF-036 | Effective only at `--monitor 3`; accepted and inert below. | source.md:216 | none (best T12 0.50) |
| INF-037 | `RunConfig` and `run_skill` do not change (F5): the guard is SKILL-orchestrated. | source.md:217 | none (best T6 0.43) |
| INF-038 | `set -euo pipefail`, same `die`, same `--repo` resolution from the origin remote, numeric `--pr` check, exi... | source.md:221 | containment T7 (0.88) |
| INF-039 | `gh pr view "$PR" --repo "$REPO" --json state,isDraft,headRefOid,autoMergeRequest` | source.md:230 | containment T7 (0.89) |
| INF-040 | `--to` is idempotent, so a retry or a resume re-issue is safe. | source.md:234 | none (best T8 0.50) |
| INF-041 | Loaded lazily at L3 Wave 3, Wave 6 and Wave 8. | source.md:240 | containment T8 (0.71) |
| INF-042 | The Wave 0 bullet is a flat line placed before the Wave 1 bullet and contains no L3 or `draft` condition | source.md:241 | containment T9 (1.00) |
| INF-043 | Its event-type enumeration says the enum has 43 members; update it to 45 and name `draft_guard_requested` a... | source.md:242 | containment T2 (0.93) |
| INF-044 | Respect the wait-only sentences pinned at `test_static_grep.py:791`. | source.md:243 | containment T1 (0.71) |
| INF-045 | `--merge-guard {draft,off}` in the argument-hint and the Options table | source.md:244 | containment T12 (1.00) |
| INF-046 | Flag row and a paragraph: what it does, the clear command, `held` meaning, default on. | source.md:245 | containment T12 (0.67) |
| INF-047 | A `held` report always carries the reason and `gh pr ready <N> --repo <REPO>` | source.md:247 | containment T8 (0.90) |
| INF-048 | The SKILL mints it at the end of Wave 3 and uses the same id as the `cycle_id` of the push triad (`push_ide... | source.md:251 | containment T8 (0.85) |
| INF-049 | The `read-only` category is not used for these calls (a `gh pr ready` mutation is never read-only). | source.md:255 | containment T7 (0.89) |
| INF-050 | Acceptance trace (must appear in this order in the run log): `draft_guard_requested(draft)`, `draft_guard_s... | source.md:270 | containment T11 (0.92) |
| INF-051 | Without `published` no row would match and the PR would stay draft. | source.md:280 | containment T4 (0.83) |
| INF-052 | next checkpoint: `state != OPEN` -> halt `pr_not_open`, nothing pushed, report the local commit `<target_sh... | source.md:281 | containment T8 (0.75) |
| INF-053 | Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/supe... | source.md:301 | containment T8 (0.92) |
| INF-054 | the final task runs the FULL suite (`uv run pytest -q tests`) and compares its failures with the base-commi... | source.md:301 | containment T1 (0.87) |
| INF-055 | Never stage `.claude/`. | source.md:301 | none (best T3 0.33) |
| INF-056 | Unchanged and must still pass: `test_idempotency.py:89` (7 sets), the one-python-fence tests | source.md:301 | containment T2 (0.67) |
| INF-057 | `merge_guard.py` into the zero-token file set | source.md:299 | containment T8 (0.83) |
| INF-058 | A static test asserts `merge_guard.py` has no `gh` or `git` word. | source.md:322 | containment T3 (1.00) |
| INF-059 | No task makes a live PR call, and the run that opens the PR must not enable the feature (`--merge-guard off`). | source.md:326 | containment T1 (0.83) |
| INF-060 | The user guide states that draft behaviour is unverified until then, and the PR body states the gate plainly. | source.md:326 | containment T1 (1.00) |
| INF-061 | Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, the test t... | source.md:362 | none (best T1 0.56) |
| INF-062 | Declare dependencies completely, one `Depends on:` line per dependency | source.md:363 | none (best T8 0.50) |
| INF-063 | The protocol wiring covers the Wave 0 resume and `off` hook as well as Waves 3, 6 and 8 (section 4.5), with... | source.md:364 | containment T8 (0.61) |
| INF-064 | The fold, `guard_status`, resume-reason and per-cycle `applied_edits` rules of sections 3 and 4.1 each get ... | source.md:366 | none (best T8 0.56) |
| INF-065 | The pre-build record task states the release-gate decision of section 8 and records the base-commit lint re... | source.md:367 | containment T1 (0.87) |
| INF-066 | Protocol prose written by the plan never carries `file:NNN` pointers and never contains the words `evidence... | source.md:369 | containment T10 (0.74) |
| INF-067 | its acceptance criterion is a test that the literal line is in `SKILL.md`, and a fresh L2 run must not depe... | source.md:374 | containment T9 (0.85) |
| INF-068 | the crash scenario tests derive branches from a real `RunLog` through `detect_crash_window` and `resolve_cr... | source.md:375 | none (best T11 0.57) |
| INF-069 | the acceptance criteria test both directions and the fresh baseline. | source.md:376 | containment T3 (0.83) |
| INF-070 | scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions (p... | source.md:377 | containment T11 (0.69) |
| INF-071 | the byte-identical checks for the pinned S5a and Wave 6 pre-push sentences compare against literal string c... | source.md:377 | containment T10 (0.81) |
| INF-072 | the Wave 0 bullet sits before the Wave 1 bullet and has no L3 or `draft` condition. | source.md:378 | containment T9 (1.00) |
| INF-073 | `src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh` | source.md:292 | containment T7 (1.00) |
| INF-074 | `tests/pr_submit/test_merge_guard.py`, `test_set_draft_state.py` | source.md:297 | containment T3 (0.80) |
| INF-075 | How scripts are granted and invoked in the SKILL front matter | source.md:340 | containment T1 (1.00) |

Postscript: no inferred row was dropped (all 75 quotes re-checked on their cited spec lines at validation); the union fields are unchanged.

## Notes and limits

- Not checked: no code was executed; the plan was audited against the spec and base-commit excerpts only. Rows in each reviewer slice were reported verified without per-row evidence by reviewer 2.
- Memory persistence skipped on purpose: the experiment workspace froze `docs/memory/reflect/deviation-patterns-brainstorm-reflect-panel.md`; this run's entry is in `artifacts/memory-entry.md`.
- Wave 7 promotion does not apply (UC-1). Tier 3 not requested.

