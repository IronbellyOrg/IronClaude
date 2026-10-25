# PR #296 review fixes: resume rule and chain regression test

Context: PR #296 (IronbellyOrg/IronClaude) removed the `--depth deep` task-builder//task route from /sc:auggie-review. Augment's review left two medium comments. Two independent proposals (`.dev/pr-review/pr-296/proposal-minimal.md`, `.dev/pr-review/pr-296/proposal-robust.md`) were compared; this plan is the chosen merge: the minimal resume rule plus one clause from the robust proposal, and a pruned version of the robust test.

## Constraints

- Edit only `src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md`, the new test file, and (for mirrors only) gitignored `.claude/` output via the sync recipes. Never stage any `.claude/` path.
- Keep the pinned strings intact: the `--remediation-offer` row start in `commands/auggie-review.md`, `quick` in the `--depth` row, `prism-b` in the `--auggie-model` row, `--model "${AUGGIE_MODEL:-prism-b}"` in SKILL.md.
- Primitive text must not tell an agent to read a `src/superclaude/...` path. The test file may read repo files.
- Out of scope: `troubleshoot.md`, `HOW-WE-WORK.md`, `reflect.md`, and any other file.
- `make` is not installed here. Sync with `bash /tmp/sync-dev.sh` and `bash /tmp/verify-sync.sh` if those files still exist; otherwise re-extract the `sync-dev` and `verify-sync` recipes from `Makefile` (strip the leading tab and `@`, turn `$$` into `$`) and run them with bash.

## Task 1: Fix the legacy-state resume rule (Augment comment on remediation-handoff.md line 151)

In `src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md`, in the Resumability section, keep the first sentence of the paragraph that starts "When the user re-invokes the skill with `--resume <output_dir>`, the chain picks up at the recorded phase." and replace everything after it on that same line with exactly:

"A state file written with the older key names ignores `task_file_path` and `task_reflect_*` and keeps `plan_path`. If the recorded phase's input is missing, re-run the phase that produces it: `plan_path` (needed by Phases C, D and E) comes from Phase B, and `spec_path` (needed by Phase B) comes from Phase A, so a state with neither restarts at Phase A. If an older state was recorded at Phase D or E, tell the user before resuming that anything already executed from its retired task file is not tracked by this chain."

Do not change the JSON example or any other line.

Acceptance criteria:
- The paragraph is still one line and its first sentence is unchanged.
- The text states that a state with neither `spec_path` nor `plan_path` restarts at Phase A, and that a state missing only `plan_path` re-runs Phase B.
- The text contains the Phase D/E notice about work executed from the retired task file.
- `grep -inE 'task-builder|MDTM|/task\b|--type task' src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md` returns no lines.
- `git diff` for this file shows only that one line changed.

## Task 2: Add the regression test for the single remediation chain (Augment comment on SKILL.md line 336)

Depends on: Task 1

Create `tests/commands/test_auggie_review_remediation_chain.py` (next to `tests/commands/test_auggie_review_revagent.py`; follow that file's conventions: `REPO_ROOT = Path(__file__).resolve().parents[2]`, read SOURCE files under `src/superclaude/`, section slices with `str.index`, no `~/.claude` or `.claude/` reads). It must contain these tests and nothing else:

1. Four surfaces, sliced by section: the `--remediation-offer` table row in `commands/auggie-review.md` (the line starting "| `--remediation-offer`"); the command's "### Remediation chain" section up to "## Boundaries"; SKILL.md Wave 5 step 4 (from "4. If the user accepts" up to "5. Return the structured output"); the ref's offer prompt (from "## The offer prompt" up to "## Phase A").
2. `test_chain_order` (parametrized over the four surfaces): the tokens `/sc:design`, `sc:workflow`, `--mode pre`, `/sc:implement`, `--mode post` appear in that order within the surface (search forward from the end of the previous token).
3. `test_dispatch_never_branches_on_depth` (parametrized over the same four surfaces): `re.search(r"\bdeep\b", surface)` is None.
4. `test_dispatch_literals`: step 4 and the whole ref each contain `` never `--handoff implement` ``; step 4 also contains `Skill sc:workflow-protocol`, `--handoff none`, `/sc:implement <pkg>/<id>.md`, `/sc:reflect --mode post` and `does NOT auto-execute`.
5. `test_removed_deep_route_is_gone_from_the_primitive`: sweep `commands/auggie-review.md`, `agents/auggie-reviewer.md` and every `.md`, `.json`, `.yaml`, `.yml` file under `skills/sc-auggie-review-protocol/` line by line for these patterns: `task[- ]builder` (case-insensitive), `\bMDTM\b` (case-insensitive), `(?<![\w:])/task\b`, `--type task\b`, and `\b(?:plan|mdtm)[ -]route\b|Route selection` (case-insensitive). A line naming `task_file_path` or `task_reflect_` is allowed only if it also contains the word `ignore`. Collect offenders as `relative/path:line [label]` strings and assert the list is empty, so a failure names file, line and marker.

Do not pin prose beyond those literals (no exact "same chain for every review depth" sentence, no exact resume wording, no counts of how often a word appears). Add a module docstring that says what the tests protect: every `--depth` dispatches to one chain, and the removed deep route (task-builder, MDTM task file, user-run /task) must not return.

Acceptance criteria:
- `uv run pytest tests/commands/test_auggie_review_remediation_chain.py -q` passes on the current tree.
- Run against the pre-PR sources: in a fresh directory under /tmp create `tests/commands/` containing the new test, and `src/superclaude/{commands/auggie-review.md,agents/auggie-reviewer.md,skills/sc-auggie-review-protocol/}` extracted with `git archive 29b3a308` from this repo; `uv run pytest` on that copy fails (at least the chain-order, depth and removed-route tests). The repo working tree is not modified by this check.
- Mutation check in a /tmp copy of the current sources: adding the text "for `--depth deep` run the alternate chain" to SKILL.md step 4 makes `test_dispatch_never_branches_on_depth` fail; adding `task-builder` anywhere in the ref makes the sweep fail. The repo working tree is not modified by this check.
- `uv run ruff check tests/commands/test_auggie_review_remediation_chain.py` and `uv run ruff format --check tests/commands/test_auggie_review_remediation_chain.py` both pass.
- `uv run pytest tests/commands/test_auggie_review_revagent.py tests/cli/reflect/test_remediation_source_template.py -q` still passes.

## Task 3: Sync mirrors and final gate

Depends on: Task 2

Run the sync and verify-sync recipes (see Constraints), then `uv run pytest tests/commands tests/cli/reflect tests/pr_submit tests/core/test_how_we_work_routing_table.py -q`.

Acceptance criteria:
- The verify-sync recipe exits 0.
- The pytest run passes with no failures.
- `git diff --cached --name-only` shows no path beginning with `.claude/`.
- `git status --short` shows only `src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md` modified and `tests/commands/test_auggie_review_remediation_chain.py` plus the untracked `.dev/` entries.
