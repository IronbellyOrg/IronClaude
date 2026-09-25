# QA Report — Task Integrity (B2 self-containment)

**Topic:** CI doctor native-install prerequisite
**Date:** 2026-09-24
**Phase:** task-integrity
**Fix cycle:** N/A
**Fix authorization:** false

---

## Overall Verdict: FAIL

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Eight single-paragraph checkbox items and contextual reads | PASS | Read task lines 97–135: 1.1, 2.1, 3.1–3.3, 4.1–4.3 each occupy one checkbox paragraph and name source material and actions. |
| 2 | Explicit deliverables and integrated verification per item | FAIL | Task lines 101, 107, 113, 117, 121, 127, 131, 135: outputs and `ensuring` clauses are present, but Step 4.2's runner invocation lacks the required full prompt and independent artifact checks; see issues 1–2. |
| 3 | Completion gates and blocked-path honesty | PASS | All eight paragraphs end in a completion gate and name blocker logging; Step 4.3 lines 133–135 requires acceptable POST result and blocked status otherwise. |
| 4 | Native install then real doctor test, fail-closed | PASS | Task line 117 explicitly calls the real `uv run superclaude doctor --verbose` before and after `uv run superclaude install` with expected nonzero/zero exits and output capture. Research notes lines 10–13, doctor.py lines 52–103, main.py lines 180–198, test_update_command.py lines 113–151 corroborate the intended distinction; this is an execution instruction, NOT evidence that the commands have already passed. |
| 5 | No real-HOME write, unauthorized commit/push, or workflow edit during task authoring | PASS | BUILD-REQUEST lines 17–20 limits builder scope; task lines 59, 69–72, 101, 117, 127, 135 prohibit those operations or require later authorization. Nothing was executed beyond read-only inspection in this review. |
| 6 | POST runner self-contained against source skill/template | FAIL | Task Step 4.2 (line 131) was compared with template 01 B2 (lines 155–165), task-builder SKILL.md lines 2217–2233 and reflect SKILL.md lines 48–56, 77–99, 1513–1533. The dedicated runner prompt, structural-wave attestation, disk corroboration, and promotion policy are insufficiently specified. |
| 7 | Template format consistency and evidence-bound item Context | FAIL | All eight checkbox items omit literal `Verify:`; task-builder template B2 expects integrated `ensuring` (template 01 lines 155–165), while rf-qa task-integrity TB-Add-6 requires `Verify:`. Task items cite code surfaces without file:line or justified evidence absence (TB-Add-8; examples: lines 107, 117, 131). See issue 4. |

## Summary
- Checks passed: 4 / 7; checks failed: 3.
- Critical issues: 1; important issues: 3; issues fixed in-place: 0 (not authorized).

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Task Step 4.2, line 131 | `spawn one dedicated ... runner ... to invoke` is not an embedded runner prompt. The specified command is only arguments in the executor's item, not an instruction to the spawned runner to invoke the Skill tool; no full runner role, skill-tool call, wave requirements, return schema, incomplete-run sentinel or audit attestation are supplied. The source task-builder skill-mode arm explicitly requires the COMPLETE prompt verbatim (SKILL.md lines 2217–2229). This can falsely count a simulated or partial POST review as complete. | Embed the full dedicated-runner prompt in the single item, including actual skill invocation, tier-dependent waves, `RUN_INCOMPLETE` on partial failure, `{verdict, run_id, report, resolved_tier, waves_attestation}` return and no hand-rolled substitute. Resolve the reflect skill's invocation boundary (reflect SKILL.md lines 48–56 says only via `/sc:reflect`) with the builder's skill-tool runner requirement rather than leaving incompatible instructions. |
| 2 | IMPORTANT | Task Steps 4.2–4.3, lines 131–135 | A disk report plus verdict is insufficient verification of a full POST run. Missing independent on-disk Tier-2 `adversarial/merged-verdict.yaml`/`merge_method`, calibrated reviewer-card count and fallback/audit corroboration; missing explicit Tier-1 grounding/card/calibration attestation and TCS-derived depth/tier floor. Source task-builder SKILL.md lines 2230–2233 requires these checks and bounded malformed-run handling. Fixed `--depth standard` is not shown to be derived from task TCS. | Require executor-side evidence inspection for the resolved tier and TCS depth calculation before spawn; enforce floor and bounded retry/block when artifacts or waves are missing. Do not mark PASS just because a report exists. |
| 3 | IMPORTANT | Task Step 4.2, line 131 | POST skill defaults to Wave-7 task-directory promotion (reflect SKILL.md lines 94–99, 1504–1533, 1564–1571). The item both demands no runner edit and omits `--no-promote`; a permitted successful promotion moves `.dev/tasks/to-do/...` to `done/` before Step 4.3 reopens the original to-do path. Even if current incomplete frontmatter happens to prevent promotion, the item does not enforce that invariant. | Explicitly disable promotion for the POST review (`--no-promote`) or provide an authorized, ordered promotion/closeout path; independently confirm the task file is still at the path Step 4.3 uses. |
| 4 | IMPORTANT | All checklist items, lines 101–135 | The 8 items use `ensuring` but no `Verify:` prefix required by TB-Add-6. Code-surface Context references lack per-item `file:line` or `<!-- evidence-absence: ... -->` justification required by TB-Add-8 (e.g. workflow in 2.1 line 107, installer/doctor in 3.2 line 117, reflect specification in 4.2 line 131). These are structural gates independent of whether cross-file references happen to be accurate. | Add `Verify:` to each item's verification clause and bind each code-referencing Context to an actual file:line checked against source (or justify an absence); retain one paragraph per item. |

## Actions Taken
- Read-only verification; only this QA report was written. No task file, workflow, source, test or HOME was changed. No commit or push was made.

## Recommendations
- Resolve all four issues before treating the task file as runnable. The local real-install/doctor exercise and remote CI success are planned future checks, not results of this review.

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (seven scoped B2/safety checks; three verified as FAIL). No unchecked or unverifiable checks in this lens. This is not a claim that the entire 27-check task-integrity rubric was run.
**Tool engagement:** Read: 16 | Grep: 4 | Glob: 4 | Bash: 1 (source, task, spec and template inspection; the Bash call confirmed the QA output parent). No external lookup required.

## QA Complete
