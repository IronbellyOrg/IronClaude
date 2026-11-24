# Tier 1 observation

## Provenance
Run: local-reducer-1. Arm: failing. Transport: same-shell, authorized diagnosis. Command: uv run python -c importing the live refactor-find LENS and reduce_wave3, with no workers, mode=raw, emit_to_disk=False, and reading packaged/installed command-file existence. Exit: 0. The command is recorded in the session tool transcript. Runtime environment: this worktree's .venv; uv created it and installed the project's dependencies. No reviewer or model endpoint was called.

## Captured output
```text
lens=refactor-find
recommended_next_command=/sc:code-review --apply {compare_files}
packaged_command_exists=False
installed_command_exists=False
```

## Limits
The first observation uses the real reducer and lens constant without reviewers; its placeholders remain intentionally unsubstituted. The second observation below runs the production CLI with deterministic local stub reviewers, not a paid/model-backed review. It verifies the generated handoff, not review quality or execution of a replacement. Git status was clean at start. No source changes, test additions, commits or GitHub writes.

## Captured CLI observation
Run: local-cli-stub-1. Arm: failing recommendation, pipeline process exit 0. Command: `uv run superclaude swarm run --lens refactor-find --target src/superclaude/cli/swarm/lenses/refactor_find.py --output .dev/troubleshoot/bug-swarm-refactor-find-recommends-unavailable-20261123170314/stub-run --transport stub`.

Captured stdout:
```text
swarm run: dispatched job (mode=lens, workers=3, results=3)
```
Captured artifact: `stub-run/return-contract.yaml`, lines 1-70. The artifact reports `status: success`, `workers_succeeded: 3`, `caller_metadata.suspect: false`. Line 64 contains `/sc:code-review --apply <existing-review>,` followed by the three absolute `.final.md` paths listed at lines 27, 39 and 51. The paths exist. `<existing-review>` is literal text, not an existing input file. The unabridged line is preserved in the artifact and is authoritative for the exact generated command.

## Captured compatibility inspection
Run: local-input-check-1, same-shell, exit 0. Read the captured contract with yaml.safe_load, collected successful workers' final_path values, and checked file readability and input count against the installed adversarial command declaration. No replacement skill was executed.
```text
literal_existing_review_present=True
successful_report_count=3
all_reports_readable=True
candidate_input_shape_valid=True
candidate_command_packaged=True
candidate_command_installed=True
candidate_skill_installed=True
```
The inspected candidate is `/sc:adversarial --compare ` followed by only the three existing successful final_path values, comma-separated. Its name and --compare syntax match packaged/installed commands/adversarial.md:15,39 and installed skills/sc-adversarial-protocol/SKILL.md:54-62. This does not certify a future source fix, failed-worker handling, arbitrary path quoting or a full adversarial execution.

## Captured baseline tests
Command: `uv run pytest tests/swarm/test_bundled_lenses.py tests/swarm/test_reduce.py -q`, same-shell, exit 0.
```text
collected 76 items
76 passed in 0.92s
```
No new regression test was added. The existing tests pass with the defect present.

## Behaviour definitions
Definition fetch for row 1: local installed contract Read (this is this project's own natural-language command interface, not an external library API). Source: /home/coder/.claude/skills/sc-adversarial-protocol/SKILL.md:54-62.
```text
54 ### Mode A: Compare Existing Files (FR-001)
57 /sc:adversarial --compare file1.md,file2.md[,...,file10.md]
60 - Accepts 2-10 existing files for comparison, debate, and merge
61 - Files are copied to `<output>/adversarial/variant-N-original.md`
62 - Validation: All files must exist and be readable; 2-10 file count enforced
```
This is the declared governing input rule, not a demonstrated successful adversarial run. It establishes the replacement's required file syntax and rejects literal nonexistent external input. The actual replacement was not executed.
