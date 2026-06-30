# QA Report — Task Integrity (B2 Self-Containment Lens)

**Topic:** sc:submit-pr PR Review Auto-Remediation Monitor (V1.0)
**Date:** 2026-06-11
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Task file:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-submit-pr-20260611-030241/TASK-RF-submit-pr-20260611-030241.md
**Template:** 02

---

## Adversarial Stance

Assuming the work contains errors. Targeting >=5 issues. A 0-issue verdict requires extraordinary evidence.

---

## Verification Log (appended incrementally)

### Structural baseline (verified via grep/awk)

- Total `- [ ]` checklist items: **89** (excludes template/findings sections, which correctly hold 0 items).
- Per-phase item counts: P1=4, P2=7, GateA=9, P4=7, P5=6, P6=6, P7=5, P8=10, P9=6, P10=3, P11=6, GateB=14, Post-Completion=6.
- Distinct test-module-create items: 19 (one `then create tests/submit_pr/test_*.py` per module). One module per item — NOT batched. B2-item-6 compliant (each test module has its own item).
- Distinct ref/script/Python-module create items: each ref (`state-machine.md`, `detection-contract.md`, `severity-routing.md`, `augment-poll.md`, `finding-verify.md`, `troubleshoot-dispatch.md`, `thread-reply.md`, `loop-guard.md`) and each script/module has its own item.

### Load-bearing correctness points (BUILD_REQUEST corrections) — ALL VERIFIED

| Point | Verdict | Evidence |
|---|---|---|
| R1 DET-probe = needs_human_decision HALT, writes PENDING, never auto-locks | PASS | Step 2.0 (L196): "record … a `needs_human_decision: PENDING` entry … ensuring this item NEVER auto-locks the contract, NEVER hard-guesses `augment_bot_login`". HALT-for-live-lock-only framing present. |
| Python core targets `src/superclaude/submit_pr/` (underscored) | PASS | Steps 2.2/2.3/4.2/5.1/6.2/7.4/8.2-8.4 all create under `src/superclaude/submit_pr/`. Key Constraint #1 (L131) + Source Areas (L118) confirm underscored/importable. |
| Coverage uses `--cov=superclaude.submit_pr` | PASS | Step 11.3 (L407): `--cov=superclaude.submit_pr`; correction documented L132. No hyphenated cov target appears as a command. |
| Exactly 4 pytest markers registered | PASS | Step 9.3 (L372): adds exactly `loop_guard`, `autonomy`, `recovery`, `p0`; explicit "NOT `loop`". Key Constraint #3 (L133). |
| `--depth quick --fix` appears only as a prohibition | PASS | 9 occurrences, all prohibitions/test-assertions ("NEVER emit", "no test asserts", adversarial-lens "find a `--depth quick --fix` emission"). Zero command emissions. |
| Hook edit is src/-only with make sync-dev (never git add .claude/hooks) | PASS | Step 9.2 (L369): "edit is to the `src/` source ONLY … do NOT edit or `git add` the `.claude/` mirror". Sync deferred to Step 11.1. No `git add .claude` anywhere. |

### B2 Self-Containment Checklist (7 items)

1. **All 5 B2 components per item** — PASS. Every build item follows: Read-context-refs → create/edit-action → output-path → "ensuring…" verification → "If unable… log blocker" error-clause → "Once done, mark complete" gate. Spot-checked Steps 2.1, 4.2, 5.1, 6.2, 7.2, 8.3, 9.1, 10.1, 11.3.
2. **No prior-context references without restatement** — PASS. Zero hits for "see above"/"continue from previous"/"as described above". Items that depend on earlier outputs RE-CITE them by absolute path (e.g. Step 4.2 reads `state-machine.md` by path; Step 6.2 reads it again; Step 2.6 reads the summary file by path).
3. **Agent-spawning (QA-gate) items embed full prompt** — PARTIAL / see Issue #1. The spawn items specify agent type, lens, inputs (manifest+spec+artifact paths), the literal adversarial-stance string, output report path, `fix_authorization`, and required verdict shape. They do NOT embed a verbatim end-to-end agent prompt; they describe what to "instruct it" to do. This matches the project's documented `feedback_rfqa_adversarial_pattern` and is self-contained enough to execute, but is a soft deviation from a strict "fully embedded prompt (not paraphrased instruction)" reading.
4. **File paths specific (not "the relevant file")** — PASS. Zero hits for "the relevant file"/"the appropriate file". All paths are absolute or repo-rooted and verbatim.
5. **Verification criteria measurable (not "verify it works")** — PASS. Zero hits for "verify it works"/"ensure it works". Criteria are concrete (e.g. "exactly 33 members", "`round_counter==2` at max_rounds=2", "stdout contains BOTH `/sc:auggie-review` AND `/sc:submit-pr --monitor`").
6. **No batch items** — PASS (per rubric). Rubric item 6 permits per-*fixture-group* items. Fixtures are split into 2 grouped items (Step 10.2 = 10 finding fixtures, Step 10.3 = 8 review/sequence fixtures); each test module, ref, script, and Python module has its own item. See Issue #2 for a granularity note on Step 5.1.
7. **No items based on [CODE-CONTRADICTED]/[UNVERIFIED] findings** — PASS. No such tags appear; spec corrections are pre-authorized by BUILD_REQUEST and documented as deviations (L551), not unverified guesses.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | All QA-gate spawn items (PGA.2 ×5, PGB.2 ×3, PGB.3 ×3, PGB.7 ×3; fix-agent items PGA.4, PGB.5, PGB.8; verification items PGA.5, PGB.6) | B2 checklist item 3 (strict reading) wants the spawned agent's full prompt embedded verbatim. These items instead give a paraphrased "instruct it to…" directive plus the literal adversarial-stance string. Self-contained enough to execute (agent type, inputs by path, output path, fix_authorization, verdict shape, and the verbatim ADVERSARIAL STANCE line are all present), and consistent with project memory `feedback_rfqa_adversarial_pattern`, but not a byte-verbatim embedded prompt. | Acceptable as-is given the rf-qa/rf-analyst agents carry their own SKILL-level protocol; if strict B2 is required, expand each spawn into a fenced verbatim prompt block. Non-blocking. |
| 2 | MINOR | Step 5.1 (L269) | Item atomicity: creates THREE outputs in one item — the `severity-routing.md` ref, the `severity_router.py` module, AND a re-export edit to `__init__.py`. Borderline against B2-item-6/atomicity (one atomic change per item). The three are tightly coupled (ref defines the algorithm the module implements; re-export makes the module importable for tests), and the item stays self-contained, but it is the densest item in the file. | Optional: split into 5.1a (ref), 5.1b (module + `__init__` re-export). Non-blocking — coupling justifies the bundling and the item is still executable in one read. |
| 3 | MINOR | Step 4.3 (L250) | The `__init__.py` re-export item carries a conditional "add it now as a guarded forward import OR add it in Phase 5 and note it" branch for `remap_severity`. Self-contained but the dual-path instruction adds executor ambiguity (two valid outcomes). | Acceptable — both branches are fully specified and converge (Step 5.1 re-exports `remap_severity` regardless). The forward-plan note keeps it honest. Non-blocking. |

All three issues are MINOR and non-blocking. None is a true B2 self-containment failure: no item is unexecutable in isolation, no item references un-restated prior context, no vague paths, no vague verification, no batch-across-modules. The load-bearing correctness points (R1 HALT, underscored Python path, cov target, 4 markers, --depth-quick-fix prohibition-only, src-only hook edit) are all PASS.

---

## Summary

- B2 checklist items passed: 6 / 7 fully PASS; item 3 PARTIAL (paraphrased-not-verbatim spawn prompts).
- Load-bearing correctness points: 6 / 6 PASS.
- Issues found: 3 (0 CRITICAL, 0 IMPORTANT, 3 MINOR).
- No fixes applied (fix_authorization: false — report-only).

## Confidence

- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (13 = 7 B2-checklist items + 6 load-bearing correctness points; all checked with grep/awk/Read evidence)
- **Tool engagement:** Read: 5 | Grep: 0 | Glob: 0 | Bash: 4 (grep/awk via Bash). No web research performed (all verification is source-truth-local).

## Recommendations

- The task file is B2-self-contained and the BUILD_REQUEST corrections are all correctly encoded. The 3 MINOR issues are advisory and do not block execution.
- If a strict-verbatim spawn-prompt standard is later enforced, expand the QA-gate spawn items (Issue #1) into fenced prompt blocks; otherwise the current paraphrased+adversarial-string form is the established project pattern.

## QA Complete

VERDICT: PASS
