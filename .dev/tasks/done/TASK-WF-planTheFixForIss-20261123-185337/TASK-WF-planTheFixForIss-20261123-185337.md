---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-planTheFixForIss-20261123-185337
version: "1"
priority: Medium
created_date: "2026-11-23"
---

# Repair the refactor-find follow-up

Source: ./source.md
Goal: The refactor-find review mode suggests the shipped report-comparison command with accepted real report-file inputs, with regression evidence and matching current documentation.

## Constraints

- This package is a plan only. Generating it does not authorize implementation. Execute only after the person approves execution. Do not commit, push, open a pull request, post an issue comment or launch paid/model-backed reviews.
- Limit production edits to src/superclaude/cli/swarm/lenses/refactor_find.py and the fresh-run recommendation-building block of run_cmd in src/superclaude/cli/swarm/commands.py. Use existing test files and update only the matching current documentation and wizard guidance named in Task 4 (MR-B1).
- The extra existing-review placeholder is not a separate issue to fix everywhere. Adjust refactor-find's bundled handoff only as required by the chosen consumer. Leave every other lens's recommendation, shared reducer, resume behavior, normalization, reviewer output content and success-status policy unchanged.
- Preserve refactor-find's experimental status, suspect=False, worker defaults, and absence of automatic downstream execution. Preserve explicit caller-provided templates and substitutions; do not replace custom instructions or silently validate/rewrite caller-owned inputs under this change.
- The replacement compares and combines reports, not application source. Never add a new command solely to preserve the stale recommendation. The supported command is /sc:adversarial --compare with a comma-separated list of 2-10 existing readable files, per src/superclaude/commands/adversarial.md and the active sc-adversarial-protocol skill.
- No credentials in files or logs; use environment references only. All Python/test operations use UV. Network-free stub reviewer transport is sufficient; never run the downstream adversarial skill or a model-backed swarm to satisfy these tasks.
- Diagnosis is evidence, not repaired-state acceptance. The previous diagnosis reproduced the stale instruction, but has no fix-applied positive witness. Do not relabel that historical report or clear its blocker by assertion. Task 3 must supply new observed red-to-green regression results and actual repaired CLI output.
- Keep task-owned evidence under ./artifacts/ using package-relative links. Keep intermediate evidence. Stage .dev/tasks, including this package and its artifacts, as project policy requires; staging is not a commit. Do not stage generated .claude mirrors. Final independent whole-plan review and archiving belong to the executor, not a separate task here.

## Phase 1: Capture the defect in regression tests

## Task 1: Add missing-command and complete-handoff regression checks

Use tests/swarm/test_bundled_lenses.py for a focused refactor-find availability check and tests/swarm/test_commands_run.py for a real CLI stub-transport handoff regression. Reuse the existing LENSES import, _runnable_spec and _write_spec helpers where applicable, and the pattern in test_run_cmd_stub_transport_dispatches_workers_not_noop. Read src/superclaude/cli/swarm/lenses/refactor_find.py, the run_cmd recommendation block in src/superclaude/cli/swarm/commands.py, and src/superclaude/commands/adversarial.md before authoring assertions. Do not change production code in this task.

Assert that the command token emitted for default refactor-find resolves to an actual packaged src/superclaude/commands/<name>.md file; a separately installed or differently namespaced plugin is not a substitute. Assert the full expected /sc:adversarial --compare form, parse its one comma-separated file-list argument, and compare that list to the successful workers' actual final_path values from the generated return-contract.yaml. Check readable file existence and input count, not merely that the template contains text or that the command name looks plausible. Run the generated CLI through the public swarm_group entry point with --transport stub, rather than mocking its reducer or constructing the expected contract directly. Standard-library parsing and existing YAML/test dependencies suffice.

Acceptance criteria:
- The new availability regression fails on the current source because /sc:code-review has no packaged command. The complete-handoff regression also fails for the current emitted instruction or its invalid argument list. Capture assertion failures, invoked test selectors and exit statuses in ./artifacts/regression-before.txt; an import error, bad fixture or proxy/environment failure does not count as reproducing the bug.
- The CLI check uses a target clearing the existing 50-non-whitespace-byte floor, writes reports under pytest's temporary output directory, and checks actual generated output_files and recommended_next_command. It invokes no network/model endpoint and no suggested downstream command.
- This task is complete when the new tests are correctly installed and the expected product-defect failures are observed, not when production is already green. Record those intentional failures explicitly; do not weaken assertions to make them pass. Existing unrelated baseline tests remain unchanged.

## Phase 2: Select the shipped report-comparison command

## Task 2: Replace the refactor-find lens's stale command template

Depends on: Task 1

In src/superclaude/cli/swarm/lenses/refactor_find.py, change only LENS.recommended_next_command_template from /sc:code-review --apply {compare_files} to /sc:adversarial --compare {compare_files}. Keep the existing placeholder name for substitution by the caller, rather than adding a new command, new lens field or suspect-file workaround. The LENS constant is imported into src/superclaude/cli/swarm/lenses/__init__.py and copied into default JobSpecs by _build_spec_from_lens in commands.py and the default-lens expansion in preflight.py; preserve those existing flows without editing them.

Acceptance criteria:
- The new focused command-availability assertion from Task 1 passes against the real packaged command, with --compare verified from src/superclaude/commands/adversarial.md; --apply is absent from this lens's recommendation.
- LENS still declares suspect=False, stability=experimental, the same recipe/normalizer and worker settings. tests/swarm/test_bundled_lenses.py and tests/swarm/test_lens_defaults.py pass. The existing suspect coupling rule in lenses/_validate.py is unchanged and still passes.
- Record results in ./artifacts/lens-template.txt. The complete CLI argument-list test may still fail until Task 3; record that honestly rather than claiming the fix complete after this template-only change.

## Phase 3: Deliver accepted report inputs at the real CLI boundary

## Task 3: Build the refactor-find default handoff from successful report files

Depends on: Task 2

In src/superclaude/cli/swarm/commands.py, modify only the existing post-normalization next-command construction within run_cmd. When processing refactor-find's bundled default recommendation with no explicit compare_files substitution, supply the actual successful normalized worker final_path values, in their existing order, without adding the literal existing-review prefix. Do not globally remove that prefix or change the default mapping of bare-review, reflect-review, edge-case-hunt or any other lens. Respect explicit caller templates and substitutions exactly as the current precedence contract does, including spec-file invocations; a refactor-specific default must not silently replace them. Keep the use of the existing reducer/emitter.

For this bundled default only, do not emit a runnable --compare suggestion when fewer than two successful usable reports exist or when the generated input list cannot satisfy the documented consumer syntax/count. Leave the suggestion empty in that case while retaining existing result status and all artifacts; do not fabricate an input, truncate away a successful report to fit, introduce new CLI flags, or change the worker success policy. Handle ordinary output paths with spaces through appropriate argument quoting; an unrepresentable comma within a path must not silently become two comparison files. Do not apply these default guards to caller-owned custom templates/substitutions.

Extend the real CLI regression in tests/swarm/test_commands_run.py to cover ordinary all-success output, two-success partial output, insufficient-success default output, an output path with spaces, caller compare_files override, caller template override, and unchanged sibling behavior. Reuse existing fake-dispatch patterns only to control success/failure counts; the original three-success and path-delivery cases must use the real dispatch/normalization/reduction/emission chain with stub transport. Any additional count/path guard cases should use parameterization rather than a new framework.

Acceptance criteria:
- The same focused tests that exposed the original defect in Task 1 now pass, including packaged command availability and the complete emitted argument list. Record the before/after test selectors and observed results in ./artifacts/regression-after.txt; do not rewrite the saved negative witness.
- A three-success public CLI stub run produces a /sc:adversarial --compare recommendation whose parsed files equal exactly those three actual successful final_path values, all readable, with no existing-review text, unresolved placeholders, --apply or --suspect-source. Two-success partial output similarly contains exactly the successful files; insufficient-success output has no runnable default comparison suggestion.
- The caller override cases preserve the exact caller template and explicit compare_files values. At least bare-review and edge-case-hunt sibling handoffs retain their prior mapping; existing reflect/bare-review contracts are not rewritten. Preserve tests/swarm/test_e2e_user_guide.py, tests/swarm/test_bare_review_parity.py and tests/swarm/test_swarm_run_inputs.py alongside the focused tests. Any unrelated failure is reported, not fixed under this issue.
- Run uv run pytest tests/swarm/test_commands_run.py tests/swarm/test_bundled_lenses.py tests/swarm/test_lens_defaults.py tests/swarm/test_e2e_user_guide.py tests/swarm/test_bare_review_parity.py tests/swarm/test_swarm_run_inputs.py. Record actual results in ./artifacts/related-tests.txt. Do not substitute the previously passing 76-test baseline for this repaired-state evidence.
- Run the installed project entry point with uv run superclaude swarm run --lens refactor-find --target src/superclaude/cli/swarm/lenses/refactor_find.py --output pointing at this package's ./artifacts/repaired-cli/ directory and --transport stub. Preserve stdout/exit status in ./artifacts/repaired-cli.txt and the generated contract/reports in that output directory. Independently check its complete suggested command against the shipped consumer interface. Do not invoke that suggestion. This is the positive production-entrypoint witness missing from diagnosis.

## Phase 4: Align current refactor-find documentation

## Task 4: Update the current refactor-find handoff descriptions (MR-B1)

Depends on: Task 3

Update only refactor-find's handoff descriptions in docs/swarm/README.md (lens table), docs/swarm/lens-catalog.md (lens table and refactor-find subsection), docs/swarm/user-guide.md (choosing-a-lens table), docs/swarm/wizard-guide.md, and the matching wizard primitives src/superclaude/skills/sc-swarm-wizard-protocol/refs/cli-contract.md, src/superclaude/skills/sc-swarm-wizard-protocol/refs/interview.md and src/superclaude/commands/swarm-wizard.md (MR-B1). Edit the primitives only under src/superclaude/, then run make sync-dev and make verify-sync, and never stage generated .claude copies (MR-B1). Name /sc:adversarial --compare consistently and explain that the suggestion compares generated findings; it does not automatically change application code. Where the complete invocation is shown, its inputs are the actual successful report filenames delivered by Task 3. Keep the existing placeholder convention for a template clearly labeled as a template, not a nonexistent extra required report. Document the absence of a runnable suggestion when there are too few successful reports, without implying that a successful swarm status alone proves comparison validity.

Do not rewrite docs/swarm/release-notes-v1.md or docs/testing historical validation reports, and do not repair unrelated lens handoffs found during the search.
Acceptance criteria:
- A search of current docs/swarm/ and the wizard primitives under src/superclaude/ for the stale refactor-find follow-up (/sc:code-review and --apply) has every hit dispositioned as corrected or as an intentional historical/unrelated mention (MR-B1). No current refactor-find instruction in the files listed above remains stale, and other lens rows remain unchanged. make verify-sync passes.
- The documented complete command and file requirements agree with the repaired CLI capture in ./artifacts/repaired-cli/return-contract.yaml and the existing src/superclaude/commands/adversarial.md interface. Comparison is suggestion-only and not a promise to apply code refactors.
- Preserve the documentation search and source-agreement check in ./artifacts/documentation-check.txt. Distinguish intentional historical mentions from current instructions. No new feature, unrelated documentation cleanup or historical evidence rewrite is included.
