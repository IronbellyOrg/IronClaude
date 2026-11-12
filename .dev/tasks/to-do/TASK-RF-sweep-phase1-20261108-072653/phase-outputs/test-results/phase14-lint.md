# Phase 14 lint (item 14.2)

Run 2026-11-12. Each block: the command, its exit code, the last 30 lines of output and one PASS or FAIL line.

## Check 1

Command: `make lint`
```text
  ✅ [Check 9]: sc:reflect-protocol ends in -protocol
  ✅ [Check 9]: sc:release-split-protocol ends in -protocol
  ✅ [Check 9]: sc:review-translation-protocol ends in -protocol
  ✅ [Check 9]: sc:roadmap-protocol ends in -protocol
  ✅ [Check 9]: sc:swarm-wizard-protocol ends in -protocol
  ✅ [Check 9]: sc:sweep-protocol ends in -protocol
  ✅ [Check 9]: sc:task-protocol ends in -protocol
  ✅ [Check 9]: sc:tasklist-protocol ends in -protocol
  ✅ [Check 9]: sc:troubleshoot-protocol ends in -protocol
  ✅ [Check 9]: sc-validate-roadmap-protocol ends in -protocol
  ✅ [Check 9]: sc:validate-tests-protocol ends in -protocol
  ✅ [Check 9]: sc:workflow-protocol ends in -protocol

=== Check 10: Workspace Suffix Blocklist ===
  ✅ [Check 10]: no *-workspace directories under .claude/skills/

=== Check 11: Contract Constant Anti-Duplication (Contract #5 + #8) ===
  ✅ [Check 11]: no contract-constant duplications

=== Checks 5/7: NEEDS DESIGN (skipped) ===
  ℹ️  Check 5 (inline protocol detection) — pending design
  ℹ️  Check 7 (activation references correct skill) — pending design

=== Summary ===
  Errors:   0
  Warnings: 5
  ✅ PASS — architecture policy compliant (5 warning(s))
Running linter...
uv run ruff check .
All checks passed!
(exit 0)
```
Check 1: PASS (exit 0)

## Check 2

Command: `uv run ruff check .`
```text
All checks passed!
(exit 0)
```
Check 2: PASS (exit 0)

## Check 3

Command: `uv run ruff format --check src/ tests/`
```text
140 + {{SC_PLACEHOLDER: data_model_code}}
141 | ```
    |

unformatted: File would be reformatted
  --> tests/roadmap/fixtures/recurrence/dispatch_reachability/skipped_verification_step_case.md:44:30
   |
43 |     steps = _build_steps(config)
   -     execute_pipeline(steps)          # ends at remediate
44 +     execute_pipeline(steps)  # ends at remediate
45 |     # verify-implementation / certify terminal steps NEVER dispatched
   |

unformatted: File would be reformatted
  --> tests/roadmap/fixtures/recurrence/retry_contract/retry_loop_no_terminal_case.md:41:17
   |
40 |     id="spec-fidelity",
   -     prompt="",            # deterministic: output is f(inputs), inputs unchanged
41 +     prompt="",  # deterministic: output is f(inputs), inputs unchanged
42 |     output_file=spec_fidelity_file,
43 |     gate=SPEC_FIDELITY_GATE,
44 |     timeout_seconds=600,
   -     inputs=[spec_file, roadmap_file],   # never rewritten between attempts
   -     retry_limit=2,        # <-- futile: attempt 2 == attempt 1, byte-identical
45 +     inputs=[spec_file, roadmap_file],  # never rewritten between attempts
46 +     retry_limit=2,  # <-- futile: attempt 2 == attempt 1, byte-identical
47 | )
   |

12 files would be reformatted, 1823 files already formatted
(exit 1)
```
Check 3: FAIL (exit 1)

## Pre-existing format failures (check 3)

`uv run ruff format --check --output-format=concise src/ tests/` lists 12 files, all Markdown files with embedded Python code blocks (`ruff format` formats the code blocks inside Markdown):

```text
src/superclaude/examples/release-spec-template.md
src/superclaude/skills/sc-cleanup-audit-protocol/rules/dynamic-use-checklist.md
src/superclaude/skills/sc-cli-portify-protocol/refs/code-templates.md
src/superclaude/skills/sc-cli-portify-protocol/refs/pipeline-spec.md
src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md
src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md
src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md
src/superclaude/skills/sc-validate-tests-protocol/SKILL.md
src/superclaude/templates/documents/release-spec-template.md
tests/roadmap/fixtures/recurrence/dispatch_reachability/skipped_verification_step_case.md
tests/roadmap/fixtures/recurrence/retry_contract/retry_loop_no_terminal_case.md
```

None of the 12 is a file this task created or edited: `git diff --quiet 5dc29d23` and `git status --short` show no change for each of them, and all 12 exist at the base commit `5dc29d23` (`git ls-tree` count 12). The item allows a FAIL only in a file this task did not touch; these are logged as pre-existing findings in `### Phase 14 Findings` and do not fail the item. Every Python file this task created or edited passes the format check (the 1823 formatted files include `src/superclaude/cli/sweep/`, `tests/sweep/`, `tests/commands/test_sweep_command.py`, `tests/skills/test_worker_contract.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py` and `src/superclaude/cli/main.py`).

Result: checks 1 and 2 PASS (exit 0); check 3 FAIL only in the 12 pre-existing files above, so the item is PASS with the pre-existing failures logged.
