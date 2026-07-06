# Task Validation Consolidated Findings

**Task file:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/TASK-RF-detection-contract-20260701-164700.md
**Sources:** qa-task-validation-b2-report.md, qa-task-validation-structure-report.md
**Overall verdict:** FAIL

## Already-applied orchestrator fixes
- Added frontmatter `created`, `template: "02-complex-task"`, `tracks: 1`.
- Repointed `template_schema_doc` to `/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (source of truth, not `.claude/` mirror).
- Added an `### Execution Command` section with the positive `/task <abs path>` instruction.
- Replaced the broad `git add -A` in Step 5.6 with explicit per-path staging plus a `.claude/`-staged rejection gate.
- Normalized completion-gate wording across items (no longer auto-completes on blocker).
- Fixed `reflect_pre.skip_reason: "no-spec"`.

## Remaining findings for the fix agent

### CRITICAL
1. Batch QA items (Step 1 gate ~169-179; Step 2 gate ~221-227; Step 3 gate ~249-255; Step 4 gate ~293-299; Step 5 ~315, ~317, ~321, ~323): each consolidates + conditionally spawns fix + spawns verification in one checkbox. Split each into separate items: consolidate → decide fix → single fix agent (fix_authorization: true) → structural verify → content verify → gate PASS.
2. Agent-spawning items do not embed full standalone prompts (QA_MODE, lens, assigned inputs, checklist, output path, verdict rule). Expand each spawned-agent instruction into a fully embedded prompt so it survives session rollover.
3. Multi-file creation items batch two outputs in one checkbox (lockgate.py + writer.py; test_contract_setup_evidence.py + test_contract_setup_validation.py; test_contract_setup_writer.py + test_contract_setup_pr_submit_integration.py). Split into one item per file.

### IMPORTANT
4. Replace remaining relative path tokens inside actionable checklist text (`.claude/`, `.claude/commands/`, `.claude/skills/`, `.dev/pr-monitor/detection-contract.locked.md`, `.claude/settings.json`) with absolute `/config/workspace/IronClaude/...` paths while keeping the source-of-truth warnings.
5. Multi-command validation items (Step 4.8, Step 5.2) run pytest + ruff (+ verify-sync) in one checkbox. Split into one item per command, each capturing output to its own artifact and a shared verdict file updated at the end.
6. Ensure every checklist item has an explicit B2 "because ..." context rationale tied to its output, not just a file list.

## Verdict
FAIL — apply all above via a single serialized fix agent, then re-verify.
