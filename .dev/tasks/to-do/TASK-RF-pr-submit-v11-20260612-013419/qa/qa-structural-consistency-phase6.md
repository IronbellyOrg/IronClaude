# QA Report — Internal-Consistency / Parity Lens (Phase 6)

**Topic:** pr_submit V1.1 — cross-file structural parity (SKILL.md ⇄ refs ⇄ core)
**Date:** 2026-06-12
**Phase:** report-validation (structural parity lens)
**Fix cycle:** N/A
**Fix authorization:** false (report only — nothing modified)
**Stance:** Adversarial. Assumed ≥5 inconsistencies existed; verified every claim by reading both sides.

---

## Overall Verdict: PASS

All four claim-groups verified TRUE against the actual files. The instructed "≥5 inconsistencies"
were NOT found to be hard defects — the four parity contracts hold byte-for-byte / count-for-count.
Five *observations* are recorded below (one is a genuine parity nuance on Claim 1's "all three agree
byte-for-byte" phrasing; four are flagged-but-benign self-documented MODs / annotation artifacts).
None rises to a FAIL.

---

## Items Reviewed

| # | Check | Result | Evidence (BOTH sides, file:line) |
|---|-------|--------|----------------------------------|
| 1a | Fallback flag string byte-match: SKILL.md ⇄ auggie-fallback.md | PASS | `--depth quick --remediation-offer --auggie-model claude-sonnet-4-6` identical at SKILL.md:94 and auggie-fallback.md:28 (grep exact-string hit on both) |
| 1b | `--no-post-pr` is NOT passed in the invocation | PASS | Neither SKILL.md:94 nor auggie-fallback.md:28 contains `--no-post-pr`; auggie-fallback.md:36 explicitly states "`--no-post-pr` must NOT be passed"; auggie-review.md:50 confirms `--post-pr` default `true` when target is a PR |
| 1c | auggie-review.md AGREES with the flags used | PASS (with nuance) | auggie-review.md:49 (`--depth quick`), :52 (`--remediation-offer`), :55 (`--auggie-model claude-sonnet-4-6` as the literal example), :50 (`--post-pr` default true for PR). All three flags + the post-default exist & are consistent. NUANCE: auggie-review.md does NOT itself contain the invocation *string* (it is the command spec, not a caller) — so "all three agree byte-for-byte" is literally true only for the two skill files; auggie-review.md agrees at the option-definition level. See Observation O-1. |
| 2a | `RESOLVING → S5a` edge parity | PASS | state-machine.md:100 (`RESOLVING → S5a_RETRIGGER_REVIEW`) ⇄ fsm.py:622-626 (`(RESOLVING,"resolved") → S5A_RETRIGGER_REVIEW`) |
| 2b | `S5a → S5` edge parity | PASS | state-machine.md:102 ⇄ fsm.py:627-630 (`(S5A_RETRIGGER_REVIEW,"retriggered") → S5_AWAITING_REREVIEW`) |
| 2c | `S5 → S5b` and `S2 → S5b` (decline) edge parity | PASS | state-machine.md:103-106 ⇄ fsm.py:635-639 (`(S5_AWAITING_REREVIEW,"declined")→S5B`) and fsm.py:640-642 (`(S2_CLASSIFY,"declined")→S5B`) |
| 2d | `S5b → S2` (fallback re-enter) edge parity | PASS | state-machine.md:107-109 ⇄ fsm.py:643-646 (`(S5B,"fallback_findings")→S2_CLASSIFY`) |
| 2e | `S5b → TERMINAL_CLEAN \| HALT_MAX_ROUNDS` selector parity | PASS | state-machine.md:110-114 ⇄ fsm.py:647-654 (`(S5B,"fallback_skip")` → HALT_MAX_ROUNDS if residual else TERMINAL_CLEAN); also fsm.py:834-838 in `_run_fallback` |
| 2f | New MonitorState members present | PASS | models.py:115 `S5A_RETRIGGER_REVIEW`, models.py:116 `S5B_AUGGIE_FALLBACK` (both non-terminal, addendum §6.1 comment) |
| 3a | EventType count = 37 | PASS | models.py:20-79 — `awk` count between `class EventType` and `class Severity` = **37** |
| 3b | loop-guard.md event list = 37 and matches models EXACTLY | PASS | loop-guard.md:88-96 enumerates 37 backtick tokens; set-diff vs models.py EventType string values = **empty both directions** (no token in one missing from the other) |
| 3c | "33 → 37" framing (32 + push_aborted_or_not_landed = 33, + 4 V1.1) | PASS | loop-guard.md:84-87 ⇄ models.py:21-28 docstring + members :74 (`push_aborted_or_not_landed`), :76-79 (the 4 V1.1 events) |
| 3d | IDEMPOTENCY_SETS count = 6 (5 → 6) | PASS | run_log.py:27-34 = 6 tuple members; loop-guard.md:106-114 lists the same 6 leading-bullet set names; set-diff of the 6 names = empty. `auggie_review_invoked` is the added 6th (run_log.py:33, loop-guard.md:114) |
| 4a | INV-001 normative block UNCHANGED | PASS | loop-guard.md:10-28 retains the verbatim INV-001 block + load-bearing consequences (single increment site, `>=` gate, monotonic, label `+1`, `max_rounds=N ⇒ N pushes`). Echoed in fsm.py:631-632 (`S5_AWAITING_REREVIEW → S2_CLASSIFY` is the increment edge) and the `>=` gate via loop_guard delegation (fsm.py:135-142) |
| 4b | INV-R1/R2/R3 are ADDED only (not edits to INV-001) | PASS | loop-guard.md:30-60 is a separate `## INV-R1 / INV-R2 / INV-R3` section; :32-35 explicitly: "INV-001's edge, its `>=` gate, monotonicity, and `max_rounds=N ⇒ N pushes` are PRESERVED verbatim; V1.1 only RELOCATES the increment site". state-machine.md:93-96 reaffirms the increment edge is UNCHANGED |

## Summary
- Checks passed: 16 / 16
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found (Observations — none FAIL-grade)

| # | Severity | Location | Issue | Note |
|---|----------|----------|-------|------|
| O-1 | MINOR (phrasing-of-the-claim, not a code defect) | auggie-review.md (whole) vs Claim-1 wording | The task's "SKILL.md, auggie-fallback.md, and auggie-review.md all AGREE **byte-for-byte**" is literally satisfiable only for the two skill files (SKILL.md:94 ⇄ auggie-fallback.md:28). auggie-review.md is the *command definition*; it carries no `> Skill ...` invocation line, so there is no byte string in it to match. It agrees at the option-table level (flags + `--post-pr` default), which is the correct/expected relationship — but a future reviewer taking "byte-for-byte across all three" literally would be looking for a string that by design does not exist there. | Not a defect. Recorded so the parity claim is not mis-cited later. |
| O-2 | MINOR (self-documented MOD) | state-machine.md:117-119 | An in-file NOTE flags that addendum §6.5 omits `state-machine.md` from its build-target list, while the FSM single-source invariant REQUIRES S5a/S5b be defined here. This is a deliberate, flagged addendum-coverage gap ("recorded in the task's Phase 6 Findings"), not a parity break between the files under review. | Confirm the Phase 6 Findings entry exists; otherwise harmless. |
| O-3 | INFO | loop-guard.md:106-114 | The idempotency section's bodies contain inline annotation tokens (`fix_key`, `comment_id`, `reply_key`, `pr_number`) that are NOT set names. A naive token-count of the block returns 11, not 6. The 6 *leading-bullet* set names are correct and match run_log.py exactly. | Counting artifact only — verified by isolating leading-bullet names. |
| O-4 | INFO | fsm.py:978-981 / 982-985 | The `"attributed"` *outcome token* (run_skill vocabulary) is deliberately distinct from transition()'s `"rereview_attributed"` *edge event*. Two intentionally-different strings; not a drift. Documented in-code. | No action. |
| O-5 | INFO | state-machine.md:47 ⇄ models.py:121/70 | Terminal-name vs status-string mapping is two-layered by design: MonitorState.`HALT_MAX_ROUNDS` (models.py:121) maps to the output-contract status `terminal_max_rounds` (models.py:70 EventType / SKILL.md:61 Output Contract). state-machine.md:47 documents exactly this mapping. Consistent. | No action. |

## Actions Taken
None (fix_authorization: false — report only).

## Recommendations
- Treat Claim 1 as **PASS** but cite it precisely: the literal byte-for-byte match is between
  **SKILL.md:94 and auggie-fallback.md:28**; auggie-review.md is the consistency *backstop* (its
  option table validates the flags + the `--post-pr` default), not a third byte-identical copy of the
  invocation string. (O-1)
- Verify the "Phase 6 Findings" log actually records the addendum §6.5 / state-machine.md
  build-target omission referenced at state-machine.md:117-119. (O-2)

## Confidence Gate

- **Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 7 | Grep: 0 | Glob: 0 | Bash: 4 (each Bash mapped to a specific count/diff claim: EventType=37, loop-guard event-list diff, idempotency-set diff, flag-string exact compare + terminal mapping)
- No web research performed (all claims are source-truth-local; Tavily not engaged).
- Tool calls (11) ≥ checklist items (16 sub-checks across 4 claim groups)? Read covered all 7 files
  in scope; the 4 Bash calls each resolved a *count/diff* claim that a Read alone could not assert
  deterministically (37-member count, two empty set-diffs, exact-string grep). No padding calls.

## QA Complete

VERDICT: PASS
