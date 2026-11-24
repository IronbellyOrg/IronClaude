<!-- Provenance: review-card merge, not an implementation-plan edit. -->

# Merged Plan Review

## Verdict

<!-- Source: V3 verdict; final Round 2; refactor Changes 1/8. -->
**FAIL**, from one Blocking (Missing) finding: Task 4's isolated reviewer cannot verify before/after invocation identity. Status, output-content, test-command and report-location checks remain possible. Five Medium warnings and three Notes do not cause FAIL or authorize edits.

Counts after deduplication: blocking 1, label_high 1, medium 5, note 3 (9 findings). Medium = two primary weaknesses plus three remedy limitations. INV-006 overlaps the three limitations; INV-004 folds into wrapping; INV-005 is addressed. Original V3 calibration 0.81 is not merged-card recalibration or product-success probability. Runtime model independence is unproven. No implementation approval.

## Blocking findings

<!-- Source: V3 F1; final Round 2; refactor Changes 1/2. -->
### F1: Missing Task 4 comparison inputs

Label HIGH, Grade Blocking (Missing), category drift from governing stand-alone rule. Candidate lines 80/82 require preserved prior observations and the same three CLI invocations as Task 2, but Task 4 and Constraints 17-27 name neither commands nor baseline/red paths. Workflow template line 15 requires every task to name its needed files/sections. Executor qa.md line 9 supplies task text plus Constraints and task diff, not sibling tasks.

Affected action: comparing before/after invocation identity, not checking every public-output property. Reconstructing commands from public-after proves only after. Proposed later correction: inline `uv run superclaude swarm validate-lenses --help`, `uv run superclaude swarm scaffold --help`, and `uv run superclaude swarm run --custom-prompt-dir <existing temporary directory>`, with comparison inputs `./artifacts/public-before.txt`, `./artifacts/validate-help-red.txt`, `./artifacts/scaffold-help-red.txt`, `./artifacts/parser-before.txt`. The existing-directory argument is required. Remedy is not proven exhaustive: retain the three Medium limitations below. No candidate correction or product fix has occurred.

## Follow-up candidates

<!-- Source: V3 F2/F3; V1 F1; final Round 2; INV-001/002/003/004/006; refactor Changes 2/3/4. -->
All five are Medium, nonblocking, and cannot start a fix pass.

- **F2, cross-task shorthand:** candidate 47/66 points to earlier symbols/tests. Constraints 20 names the only regression file and Task 3 identifies cases by behavior, so the reviewer can locate them. Future node names do not exist yet. Not a second blocker.
- **F3, wrapped negative token:** candidate 36/50 says normalize whitespace. Collapsing it can leave `--custom- prompt-dir`, missing exact option absence. Source `src/superclaude/cli/swarm/__init__.py` 69-72 sets width 100; historical validate-lenses-help 12-17 splits other hyphenated tokens, while target token at 7 is intact. Mechanism observed, future target failure unobserved. Positive JobSpec/custom_prompt_dir assertions protect current red witness. INV-004 extends risk to raw captures. Suggested follow-up: remove whitespace or join hyphen splits, without claiming repaired-output failure.
- **F5, whole-plan/task diff distinction:** candidate 79 describes whole-plan final diff; executor SKILL 123-124/137-139 and qa 9 supply task-start increment. Constraints 27 assigns whole-plan review to executor, but local wording is not qualified. Cumulative diff would remove limitation (INV-001).
- **F6, required baseline reads:** qa 31 excludes outside-touched-set citations unless acceptance requires reading them. Merely listing filenames is not proof of admissibility. Any future correction needs an explicit read/compare check (INV-002).
- **F7, retained evidence inventory:** candidate 83 requires more than four baseline paths; earlier outputs at 54/66-67 also include `./artifacts/validate-help-green.txt`, `./artifacts/validate-lenses-tests.txt`, `./artifacts/diagnostic-disposition.md` (INV-003). Aggregate sufficiency INV-006 overlaps F5-F7, adding no finding. No claim that fixing plan text repairs product.

## Notes and rejected candidates

<!-- Source: V3 F4; V1 F2/F3; V2 report requirements; refactor Changes 5/7. -->
- **F4, receipt-wording Note:** coverage receipt's unverified statement remains correct for future target-token splitting, not for observed general hyphen wrapping. Keep distinction; do not rewrite historical receipt.
- **Exact filename Note, rejected defect:** Constraints 27/candidate 83-84 require executor-owned independent review and persistence under artifacts. A fixed basename changes form, not deliverable.
- **Directory-placeholder Note, excluded defect:** `<custom-prompt-dir>/system.txt` is a directory placeholder, not the rejected option and outside the two named surfaces. Loose custom text is discriminated by positive JobSpec/field checks. No extra product scope.

## Scope and evidence

<!-- Source: V3 governing/slice audit; V1/V2 full-source checks; refactor Change 6. -->
Pre-execution only. Six V3 slice requirements plus V1/V2 full-source audits cover substantive source scope; literal task-body matching remains 6/12, not semantic omission, because Constraints are outside matching. Source cards checked two producers, supported field route, parser/schema/preflight boundaries, red/green order, five related suites and final review. Scoped stale-test-wording search found no pin; not exhaustive and no tests ran.

Historical diagnostic tasklist 19-23 has five pending rows, and historical REPORT 71 remains partial with stronger repaired-state closure blocked. Candidate Constraints 22-24/Task 2 preserve these; new evidence-backed applicability is required rather than invented passes. No historical edit.

Reference key: candidate is the package plan `TASK-WF-createACheckedIm-20261123-195709.md`; coverage receipt is the reflection-root `coverage-matrix.md`. Workflow template and executor qa/SKILL are the installed files under `/home/coder/.claude/skills/sc-workflow-protocol/refs/00_mdtm_template_simple_task.md` and `/home/coder/.claude/skills/sc-implement-protocol/{refs/qa.md,SKILL.md}`. Historical basenames resolve in this checkout's `.dev/troubleshoot/bug-swarm-custom-prompt-help-20261123191427/`. Review-card originals/probe/debate resolve in `./adversarial/` relative to this merged file. Main persisted merge-executor's returned text into the existing stub, section by section; final REPORT evidence validation is separate.
