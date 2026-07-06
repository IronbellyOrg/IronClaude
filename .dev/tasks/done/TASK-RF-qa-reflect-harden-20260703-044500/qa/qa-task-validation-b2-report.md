# QA Report — Task Integrity (B2 Self-Containment Lens)

**Topic:** RF QA + /sc:reflect hardening vs PR #209 (F1-F4 regression-guards)
**Date:** 2026-07-03
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix authorization:** false (report-only)
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

Zero-tolerance gate: 6 issues found (3 IMPORTANT, 3 MINOR). No CRITICAL forbidden-item
violations — the builder correctly avoided all five prohibited CODE-CONTRADICTED items.
`fix_authorization: false` → report-only; issues documented for the orchestrator/fix cycle.

---

## Confidence

**Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

B2 lens dimensions (7): (1) 5-component presence, (2) no prior-context reliance,
(3) embedded spawn prompts, (4) path/anchor specificity+existence, (5) measurable
verification incl. FX5 differential, (6) no batch items, (7) no forbidden
CODE-CONTRADICTED items. All 7 checked with tool evidence.

**Tool engagement:** Read: 4 | Grep: 0 (grep run via Bash) | Glob: 0 | Bash: 8

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All 5 B2 components (context+action+output+verification+completion gate) per item | PASS | Every item follows a rigid "Read X … then [action] … writing to [abs path] … ensuring […] … If unable, log … then mark complete. Once done, mark complete." template. Read all 40+ items across Phases 1-5 + Post-Completion. |
| 2 | No item relies on prior-item in-context state without restating | PASS | Handoffs are done by explicit OUTPUT-FILE path (e.g. 2.2 reads `fx3-questions-inventory.md`, GA.5 reads `gateA-fix-verdict.md`), not "as computed above." Survives session rollover. |
| 3 | Agent-spawning items embed FULL prompt (no "see above"/"use SKILL.md template") | PASS (w/ caveat) | GA.2/GB.2/GC.2/PC.4/PC.8 each embed QA_PHASE, LENS, adversarial framing, the job, report path, and PASS/FAIL+file:line verdict format inline. No "see above." Caveat → Issue #1 (relative `research/NN` refs handed to fresh subagents). |
| 4 | File paths specific; cited anchors/symbols exist | FAIL | Code file paths are absolute + anchors verified by grep (questions.py `_answer_default`:52/`_evidence_attr`:64; candidate.py `_path_resolves`:360, `required_unobserved`:47; lockgate `_paths_resolve`:119; ensemble `build_reflect_contract`:492, reviewer_count:517, :550/:551/:560; contract `_VERIFICATION_SKIP_EXEMPTIONS`:36; rf-qa-qualitative :639/:660/:670-676; reflect-reviewer `tools:`:5, `persona_lens`:54, mindset:42; taxonomy :5/:26-38/:129). BUT: `research/NN` refs are relative + non-resolvable (Issue #1); `run_tier2` symbol does not exist (Issue #4); `_degraded_reason` line range points to internal logic not the def (Issue #5). |
| 5 | Verification measurable; FX5 differential "mutation-must-fail" encoded | PASS | Steps 2.5/2.6 explicitly require a DIFFERENTIAL test that "MONKEYPATCHES the helper to a naive/mutated implementation … and asserts a downstream observation flips … proves the mutation is DETECTED" + a `HELPER_TEST_MAP` recording negative+differential names, and 2.7 collector FAILs if either is missing. Measurable, not "verify it works." |
| 6 | No batch items (each test file / field group / brief edit is its own item) | FAIL | Step 3.3 modifies 4 files / ~5 edits in one item (Issue #2). Step 3.4 authors tests across 3 test files + fixtures in one item (Issue #3). |
| 7 | No items on CODE-CONTRADICTED/UNVERIFIED findings (5 forbidden checks) | PASS | (a) no "rename internal-consistency lens" — FX2 augments Code Compat items 4-6 in place; (b) no 5th deviation category — FX1 is advisory parallel `## Correctness-gap`; (c) "(15 items)" header preserved (Step 4.1 + Open-Q explicitly guard it); (d) no `status:"degraded"` / no exemption-set edit — HARD-prohibited in Step 3.2 + Key Constraints; (e) F1-F4 framed as already-fixed regression-guards throughout. NONE present. |

---

## Summary

- Checks passed: 5 / 7 (checks 4 and 6 fail)
- Checks failed: 2
- Critical issues: 0
- Important issues: 3
- Minor issues: 3
- Issues fixed in-place: 0 (`fix_authorization: false`)

Strong positives: the forbidden-item guard (check 7) is fully clean — the builder honored
the documentation-staleness override on all five prohibited items. FX5's differential
"mutation-must-fail" is genuinely encoded as a measurable step (lens focus item 5 satisfied).
All CODE-anchor line numbers spot-checked resolve exactly to the current source.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | All items citing `research/NN-*.md` (R-002..R-008; Steps 2.1, 2.2, 2.4, 2.5, 2.6, 2.7, 3.1, 3.2, 4.1, 4.2, 4.3; spawn items GA.2/GB.2/GC.2/PC.4/PC.8) | Bare relative `research/01-…`.md paths do NOT resolve from the items' own stated cwd `cd /config/…/pr209-harden` — verified: `research/` does not exist at worktree root; it lives at `.dev/tasks/to-do/TASK-RF-…/research/`. The task preamble (L183) asserts each item is "complete self-contained … context loaded in early batches is NOT available later," yet spawn items hand fresh subagents (zero task context, cwd reset per agent-thread rules) an unresolvable relative ref. | Replace every `research/NN-*.md` with the absolute path `/config/workspace/IronClaude/.dev/worktrees/pr209-harden/.dev/tasks/to-do/TASK-RF-qa-reflect-harden-20260703-044500/research/NN-*.md` (or define `${TASK_DIR}` inside each spawn prompt as already done for the qa/ dir). Aligns with the absolute-paths mandate. |
| 2 | IMPORTANT | Step 3.3 (L283) | Batch/atomicity violation (B2 check 6 "each contract field group is its own item"; general item 10). One item modifies FOUR files with ~5 distinct edits: `models.py` (append `ReflectResult` fields), `contract.py` `_make_result` (populate), `runner.py` `_build_reflect_post_value` (append keys), `runner.py` `write_sidecar` (append), plus OPTIONAL `--skip-if-pass` reader hardening. Cannot be executed without scrolling; multiple distinct file modifications. | Split into ≥3 items: (a) `models.py` field append + `contract.py _make_result` populate; (b) `runner.py` `_build_reflect_post_value` + `write_sidecar` append; (c) optional `--skip-if-pass` fail-closed hardening as its own item (it is behaviorally distinct and marked "OPTIONALLY"). |
| 3 | IMPORTANT | Step 3.4 (L287) | Batch violation (B2 check 6 "each test-update is its own item"). One item authors new tests across THREE test files (`test_ensemble_unit.py` 3 tests, `test_verdict_mapping.py`, `test_writeback.py`) plus new fixtures under `fixtures/`. Distinct modules + fixture authoring in a single item. | Split per test module (3 items) + a fixtures item, OR at minimum separate fixture creation from test authoring. Each test-file update should be independently checkable. |
| 4 | MINOR | R-004 (L120), Step 3.1 (L275), Step 3.2 (L279) | Symbol does not exist as cited: items reference "the call site `run_tier2`" but the actual function is `run_tier2_ensemble` (ensemble.py:168). Line numbers are correct (`reviewers = int(config.reviewers)`:191, builder call:302), so executor risk is low, but the named symbol is wrong (B2 check 4 spot-check). | Rename `run_tier2` → `run_tier2_ensemble` in R-004, Step 3.1, Step 3.2. |
| 5 | MINOR | R-004 (L120), Step 3.1 (L275), Step GB.2 (L308) | Line-range conflation: cited as "Trigger-12 `_degraded_reason` L288-291", but `_degraded_reason` is DEFINED at contract.py:249; L288-291 is the `skip_reason not in _VERIFICATION_SKIP_EXEMPTIONS` check inside it. Symbol exists; the range points to internal logic, not the def. | Clarify as "`_degraded_reason` (def :249; Trigger-12 skip-reason check :288-291)". |
| 6 | MINOR | Step 4.5 (L347) | Muddled/ambiguous action. The item runs `ruff format --check …cli/reflect/*.py 2>&1; true` "as a no-op guard" inside a MARKDOWN-lint step for the FX2/FX1 brief `.md` files — mixing an unrelated Python check into a markdown item, with `; true` swallowing the exit so the check is meaningless. The real action ("run any repo markdown gate … if configured … otherwise record no gate") is conditional and non-deterministic — the executor cannot know a priori what to run. | Remove the nonsensical `ruff …cli/reflect/*.py; true` line. State the markdown-lint action deterministically (name the exact pre-commit hook or explicitly "no markdown gate is configured — visual review only," per the repo's known toolchain). |

---

## Notes on Lens-Focus Items (explicit checks requested)

- **FX5 differential encoded as measurable (focus item 5):** SATISFIED. Steps 2.5/2.6 require the monkeypatch-mutation-must-be-detected assertion, not merely a negative test; the 2.7 collector enforces both per helper via `HELPER_TEST_MAP`.
- **Spot-checked anchors (focus item 4):** rf-qa-qualitative.md :639 (closed AX vocab), :660 ("#### Checklist (15 items)"), :670 (##### Code Compatibility), items 5/6 at :674/:676 — all resolve. ensemble.py `build_reflect_contract`:492 and :517/:550/:551/:560 — exact. candidate.py `_path_resolves`:360 — exact. questions.py helpers :52/:64 — exact. All CODE anchors verified; only the `research/` relative-path, `run_tier2` name, and `_degraded_reason` range are imprecise.
- **Forbidden-item audit (focus item 7 a–e):** ALL CLEAR — none of the five prohibited items were created. This is the load-bearing anti-drift property and it holds.

---

## Recommendations (before proceeding to execution)

1. Fix Issue #1 (absolute `research/` paths) — highest leverage; it undermines the task's own
   self-contained-across-rollover guarantee for every research-consulting and spawn item.
2. Split Steps 3.3 and 3.4 (Issues #2, #3) into atomic per-file items.
3. Correct the two anchor imprecisions (#4, #5) and de-muddle Step 4.5 (#6).
4. Re-run this B2 gate after fixes; all are mechanical edits with no scope change.

## QA Complete
