# Pre-build record (Task 1)

Package: TASK-WF-designSpec-20261107-075614. Source: ./source.md sections 6, 8 and 10. Written 2026-11-07 on master `e8db2fe6` (branch `ironbelly/issue-375-pr-submit-draft-guard`). No GitHub or network call was made for this record.

## 1. Base-commit record (before any code edit)

Run on the unchanged code (the only untracked files are under `.dev/`; `make sync-dev` was run first because most base failures are `.claude/` mirror tests).

| Command | Exit code | Result | Log |
|---|---|---|---|
| `make lint` | 0 | architecture policy compliant (5 warnings), `ruff check .` "All checks passed!" | ./artifacts/base-lint.log |
| `uv run ruff format --check src/ tests/` | 1 | "12 files would be reformatted, 1757 files already formatted". The 12 files are Markdown files whose python code fences ruff reformats (for example `src/superclaude/examples/release-spec-template.md`, `src/superclaude/skills/sc-cleanup-audit-protocol/rules/dynamic-use-checklist.md`, `src/superclaude/skills/sc-cli-portify-protocol/refs/code-templates.md`, `.../refs/pipeline-spec.md`); this is pre-existing and not this feature's. Consequence for this plan: a new Markdown file under `src/` must not contain a python fence | ./artifacts/base-format.log |
| `uv run pytest -q tests` (full suite, after `make sync-dev`) | 1 | 3 failed, 16955 passed, 137 skipped (section 1a lists the 3 failing ids) | ./artifacts/base-full-suite.log |

The first run of the same suite before `make sync-dev` (not saved as a log) gave 16916 passed, 25 failed, 16 errors in 10 minutes; the failures were mirror tests in `tests/audit/`, `tests/cli/test_verify_sync_hooks.py`, `tests/cli/eval/test_claude_process_adapter.py` and `tests/unit/test_ccsession_tiers.py`.

### 1a. Full suite on the base commit, after `make sync-dev`

Command `uv run pytest -q -p no:cacheprovider tests`, exit code 1 (`rc=1` is the last line of ./artifacts/base-full-suite.log). Result line: `3 failed, 16955 passed, 137 skipped, 2 xpassed, 32 warnings in 567.82s (0:09:27)`. The failing test ids are the complete base-failure set; any other failing id after this plan's changes is this feature's:

- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval`
- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module`
- `tests/unit/test_ccsession_tiers.py::test_a_busy_shim_is_never_stopped_by_a_new_launch` (the log shows the shim under test failed to start; environment, not this feature)

The 25 failures and 16 errors of the earlier run before `make sync-dev` were `.claude/` mirror tests, and they pass once `make sync-dev` has run.

## 2. Release-gate decision (owner, 2026-11-07, relayed by the coordinator)

OWNER CHOSE: build now with no GitHub calls (fake `gh` in tests). Gates G1 (live part), G2 (live part), G4, G5 and G6 are OPEN and are a RELEASE gate: the owner runs them on a disposable fork PR before the feature is merged or turned on by default. The user guide states that draft behaviour is unverified until then. The PR body states this gate plainly. The run that opens the PR must not enable the feature: use `--merge-guard off` (or leave the feature unused) when `/sc:pr-submit --monitor 3` runs for this PR. No task of this plan makes a live PR call.

| Gate | Status |
|---|---|
| G1 `gh pr ready --undo` exists | CONFIRMED locally (gh 2.103.3 help and the manual; "subject to plan support"). Live token and plan check: OPEN, release gate |
| G2 timeline names `convert_to_draft`, `ready_for_review` | CONFIRMED in GitHub documentation. Live ordering and pagination: OPEN, release gate |
| G3 `gh pr view --json autoMergeRequest,isDraft,state,headRefOid` | CONFIRMED locally (field list of gh 2.103.3) |
| G4 a draft blocks merge via UI, API, auto-merge, merge queue; converting disarms an armed auto-merge | OPEN, release gate (needs a disposable fork PR run by the owner) |
| G5 Augment, Codex and the three `pull_request` workflows on draft and ready transitions | OPEN, release gate (`contract3-generator-constraint-lint.yml` lacks `ready_for_review`) |
| G6 `gh pr ready` when already in the requested state (error or no-op) | OPEN, release gate (the script checks the state first, so only the error text is affected) |

## 3. Open items closed by reading the code

### O1 cycle id

No sentence of `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` or `refs/` mints a fix-cycle or CI-cycle id. The id is an opaque string: `push_idempotency_key(run_id, cycle_id, pre_push_sha, target_branch)` in `src/superclaude/pr_submit/fsm.py` builds `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>`; the SKILL Wave 6 text (push triad, `rereview_requested`) and `refs/review-retrigger.md` only reuse an id ("reuse the `cycle_id` of the dangling push record"); `refs/loop-guard.md` says the prefixes `sync-` and `conflict-` are reserved for conflict cycles and a fix cycle's id never starts with either. No test pins a fix-cycle value (the run-log tests use the arbitrary strings `c1`, `c2`, `conflict-1`; the idempotency tests build their own ids). Single minting place for the guard-enabled cycle: the Engage section of `refs/merge-guard.md` (loaded by the new Wave 3 bullet) calls `fix_cycle_id(kind, next_cycle_number(events, kind))` once at the end of Wave 3 (`fix` for a review-fix cycle, `ci` for a CI-fix cycle) and that id is then used unchanged as the `cycle_id` of `push_decision`, `push_initiated`, `push_completed` and `rereview_requested`. With `--merge-guard off` nothing changes: no id is minted by the guard and the existing behaviour stands.

### O2 scripts

The SKILL front matter grants programs, not scripts: `allowed-tools: Read, Grep, Glob, Write, Edit, Bash(gh *), Bash(git *), Bash(uv *), Bash(make *), Bash(jq *), Task, Skill`. Scripts are invoked in refs and SKILL text as `scripts/<name>.sh ...` lines. `test_allowed_tools_cover_every_program` (`tests/pr_submit/test_conflict_sync_protocol.py`) reads only `NEW_REFS` (the two conflict refs) and checks that every fenced command starts with one of `git`, `gh`, `uv`, `make`, `jq` (`ALLOWED_PROGRAMS`); it needs no script registration, but the new ref `refs/merge-guard.md` will follow the same rule by its own test. The `_RESOLUTION_SCRIPTS` tuple in `tests/pr_submit/test_static_grep.py` lists the scripts whose origin-URL resolution line is tested (`test_repo_resolution_sed_handles_all_url_forms`, `test_repo_resolution_prefers_origin_over_gh_default`, `test_repo_resolution_runs_origin_first_then_falls_back`); a new script that copies the `retrigger-review.sh` resolution lines joins that list. `test_t105_runtime_repo_pin` checks only the poll script, so it is not the proof for the new script. `tests/unit/test_cli_install.py` `_assert_present` checks that listed baseline files exist; an unlisted new ref or script does not fail it.

### O3 pins and line-content rules the additive edits must respect

How this list was produced: `./artifacts/o3-pin-scan.py` (read-only, standard library only, no network call) reads every `.md` and `.sh` file under `src/superclaude/skills/sc-pr-submit-protocol/` plus `src/superclaude/commands/pr-submit.md`, and scans `tests/pr_submit/*.py`, `tests/skills/test_worker_contract.py`, `tests/commands/test_impact_command.py`, `tests/core/test_how_we_work_routing_table.py` and every other `tests/**/*.py` that names one of the six target tokens in the script header (`sc-pr-submit-protocol`, `pr-submit.md`, `state-machine.md`, `loop-guard.md`, `ci-poll.md`, `review-retrigger.md`). A reader is a test or helper that reads target text: it reads a constant that names a target file, loops over (or comprehends over) such constants and reads the loop variable, or calls a helper that does; the write-verb audit of `tests/skills/test_worker_contract.py` is forced in because it scans whole folders. Pass A lists every string literal of 8 or more characters, held by a reader or by a constant a reader uses, that appears verbatim in a target file; path-valued literals are included and only the length filter applies. Pass B lists every reader, one line each, tagged PIN (a plain contains check) or RULE (the body has a loop or comprehension, a `not in`, an `assert not`, an `is None` or a `re.*` call, so the rule lives in logic that the literals alone do not show). Every RULE reader has one hand-written card below.

Layer 1 (literals and the reader list, path literals included) is the unedited scan output: re-run it and diff. Layer 2 (rule cards) is written by hand. Check it two ways: `uv run python -I .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py --rule-names` must equal `rg -o '^#### RULE (\S+)' -r '$1' .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md | LC_ALL=C sort` (run the first command's output through `LC_ALL=C sort` too if the locale is not C), and each card must match its test's loop condition and constants.

<!-- o3-scan:begin -->
## Pass A: exact-text pins (test::owner | target file | how checked | literal)
tests/commands/test_impact_command.py::_SKILLS | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
tests/commands/test_impact_command.py::_IMPACT_CALLERS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | sc-pr-submit-protocol
tests/commands/test_impact_command.py::_IMPACT_CALLERS | src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | sc-troubleshoot-protocol/SKILL.md
tests/commands/test_impact_command.py::_IMPACT_CALLERS | src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | sc-troubleshoot-protocol
tests/commands/test_impact_command.py::_IMPACT_CALLERS | src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md | set member | sc-auggie-review-protocol/SKILL.md
tests/commands/test_impact_command.py::_IMPACT_CALLERS | src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | sc-auggie-review-protocol
tests/commands/test_impact_command.py::test_impact_callers_wired | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | in | Skill sc:impact-protocol
tests/commands/test_impact_command.py::test_impact_callers_wired | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | in | `status: blocked|failed` counts as `graph:absent`
tests/commands/test_impact_command.py::test_impact_callers_may_invoke_skill | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .get() | allowed-tools
tests/commands/test_impact_command.py::test_impact_callers_may_invoke_skill | src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | sc-troubleshoot-protocol/SKILL.md
tests/commands/test_impact_command.py::test_impact_callers_may_invoke_skill | src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md | set member | sc-auggie-review-protocol/SKILL.md
tests/commands/test_impact_command.py::test_impact_callers_wired | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | --caller
tests/pr_submit/test_codex_reviews.py::SKILL_MD | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | SKILL.md
tests/pr_submit/test_codex_reviews.py::_skill_gate | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | contract
tests/pr_submit/test_codex_reviews.py::_skill_gate | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | pushed_sha
tests/pr_submit/test_codex_reviews.py::_skill_gate | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | watermark
tests/pr_submit/test_codex_reviews.py::_skill_gate | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | codex_watermark
tests/pr_submit/test_codex_reviews.py::test_skill_gate_adds_the_codex_part_on_the_same_snapshot | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | compare | findings
tests/pr_submit/test_codex_reviews.py::test_skill_gate_codex_part_keeps_the_pushed_head_and_watermark_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | other | head_sha
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | dedup_groups(findings)
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | routes at its members' highest remapped tier
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | `fix_applied` is recorded for **every** member's `fix_key`
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | **every verified member's thread** is replied to and resolved
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | "flagged by: augment, codex"
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | covers **only the reviewers re-triggered in this cycle**
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | at least one\nre-triggered reviewer reaches `done`
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | reviewer_incomplete{reviewer, phase: "rereview"}
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | plus any merged Codex `findings`
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md | set member | rebuild_state()["absent_reviewers"]
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | pending_retriggers(
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | rereview_requested{cycle_id, reviewer, timestamp}
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | reuse the `cycle_id` of the dangling push record
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | poll_result
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | review_detected
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | findings_normalized
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | finding_verified
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | finding_unverified
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | route_decision
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | reply_posted
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | thread_resolved
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | rereview_requested
tests/pr_submit/test_codex_reviews.py::test_skill_gate_adds_the_codex_part_on_the_same_snapshot | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md | other | codex_state
tests/pr_submit/test_codex_reviews.py::test_skill_gate_adds_the_codex_part_on_the_same_snapshot | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | other | codex_routes
tests/pr_submit/test_codex_reviews.py::test_skill_gate_adds_the_codex_part_on_the_same_snapshot | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | other | activity
tests/pr_submit/test_codex_reviews.py::test_skill_gate_adds_the_codex_part_on_the_same_snapshot | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
tests/pr_submit/test_codex_reviews.py::test_skill_gate_codex_part_keeps_the_pushed_head_and_watermark_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md | other | codex_state
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | .index() | pending_retriggers
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | before the S5 poll
tests/pr_submit/test_codex_reviews.py::test_skill_gate_codex_part_keeps_the_pushed_head_and_watermark_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | other | codex_findings
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | Every event that concerns one reviewer
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | .index() | On `--resume`
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | **Resume of a re-triggered cycle:**
tests/pr_submit/test_codex_reviews.py::test_skill_gate_adds_the_codex_part_on_the_same_snapshot | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | other | codex_findings
tests/pr_submit/test_conflict_scripts.py::SKILL_DIR | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | sc-pr-submit-protocol
tests/pr_submit/test_conflict_scripts.py::PROBE | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | other | probe-merge.sh
tests/pr_submit/test_conflict_scripts.py::FINISH | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh | other | finish-merge.sh
tests/pr_submit/test_conflict_scripts.py::EVIDENCE | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | other | collect-conflict-evidence.sh
tests/pr_submit/test_conflict_scripts.py::ALL_EVIDENCE_FILES | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | worktree
tests/pr_submit/test_conflict_scripts.py::ALL_EVIDENCE_FILES | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | set member | diff-ours.txt
tests/pr_submit/test_conflict_scripts.py::ALL_EVIDENCE_FILES | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | set member | diff-theirs.txt
tests/pr_submit/test_conflict_scripts.py::POLL_CI | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | poll-ci-checks.sh
tests/pr_submit/test_conflict_scripts.py::test_probe_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | .startswith() | #!/usr/bin/env bash\n
tests/pr_submit/test_conflict_scripts.py::test_probe_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | in | \nset -u -o pipefail\n
tests/pr_submit/test_conflict_scripts.py::test_probe_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | set member | src/superclaude
tests/pr_submit/test_conflict_scripts.py::test_finish_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | .startswith() | #!/usr/bin/env bash\n
tests/pr_submit/test_conflict_scripts.py::test_finish_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | in | \nset -u -o pipefail\n
tests/pr_submit/test_conflict_scripts.py::test_finish_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | set member | src/superclaude
tests/pr_submit/test_conflict_scripts.py::test_evidence_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | .startswith() | #!/usr/bin/env bash\n
tests/pr_submit/test_conflict_scripts.py::test_evidence_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | in | \nset -u -o pipefail\n
tests/pr_submit/test_conflict_scripts.py::test_evidence_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | set member | src/superclaude
tests/pr_submit/test_conflict_scripts.py::SKILL_DIR | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | in | \nLIMIT_SECONDS=60\n
tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh | set member | --base-sha
tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | set member | --merge-base
tests/pr_submit/test_conflict_scripts.py::test_poll_ci_evidence_mode_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | .index() | if [ "$EVIDENCE_MODE" -eq 1 ]; then
tests/pr_submit/test_conflict_scripts.py::test_poll_ci_evidence_mode_static_rules | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | .index() | gh pr checks --repo
tests/pr_submit/test_conflict_scripts.py::test_probe_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | set member | ls-files
tests/pr_submit/test_conflict_scripts.py::test_finish_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | set member | ls-files
tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | .replace() | \nLIMIT_SECONDS=60\n
tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | #!/usr/bin/env bash\n
tests/pr_submit/test_conflict_scripts.py::test_evidence_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | set member | ls-files
tests/pr_submit/test_conflict_scripts.py::test_poll_ci_evidence_mode_static_rules | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | in | repos/${REPO}/
tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | other | \nLIMIT_SECONDS=
tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | other | sc-pr-submit-tmp
tests/pr_submit/test_conflict_sync_protocol.py::PUSH_LINE | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | other | git push origin <target_sha>:<HEAD_BRANCH>
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_DIR | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | sc-pr-submit-protocol
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_MD | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | SKILL.md
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_REF | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | other | conflict-mechanical.md
tests/pr_submit/test_conflict_sync_protocol.py::INTENT_REF | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | other | conflict-intent.md
tests/pr_submit/test_conflict_sync_protocol.py::STATE_MACHINE_REF | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | state-machine.md
tests/pr_submit/test_conflict_sync_protocol.py::PROBE_SCRIPT | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | other | probe-merge.sh
tests/pr_submit/test_conflict_sync_protocol.py::FINISH_SCRIPT | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh | other | finish-merge.sh
tests/pr_submit/test_conflict_sync_protocol.py::EVIDENCE_SCRIPT | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | other | collect-conflict-evidence.sh
tests/pr_submit/test_conflict_sync_protocol.py::POLL_CI_SCRIPT | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | poll-ci-checks.sh
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit --no-ff <base_sha>
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git checkout --ours -- uv.lock
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | uv lock --check
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git add -- uv.lock
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | merge_parent_ok(<parents>, pre_push_sha, base_sha)
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git merge-base --is-ancestor <base_sha> origin/<base>
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | The deterministic core DECIDES
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | set member | evaluate_sync_decision
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | sync_started
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | reason `pr_conflicting`
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | set member | --evidence-sha
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | expect_checks
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | push_rejected
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | push_failed
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git revert -m 1 <merge_sha>
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | Nothing was changed and nothing was pushed.
tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | never stash
tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | other | merge --no-commit --no-ff <base_sha>
tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | scripts/collect-conflict-evidence.sh
tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | evidence-validator
tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | One revision pass
tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | one sentence
tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | high-suspicion
tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | configured reviewers
tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | base_authored
tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git add -- <path>
tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git rm -- <path>
tests/pr_submit/test_conflict_sync_protocol.py::RECORD_FIELDS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | root_cause
tests/pr_submit/test_conflict_sync_protocol.py::RECORD_FIELDS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | ours_intent
tests/pr_submit/test_conflict_sync_protocol.py::RECORD_FIELDS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | theirs_intent
tests/pr_submit/test_conflict_sync_protocol.py::RECORD_FIELDS | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | set member | resolution
tests/pr_submit/test_conflict_sync_protocol.py::RECORD_FIELDS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | behavior_after
tests/pr_submit/test_conflict_sync_protocol.py::RECORD_FIELDS | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | set member | evidence
tests/pr_submit/test_conflict_sync_protocol.py::_PRE_EXISTING_VALIDATOR_LINES | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | read-only evidence-validator before diagnosis or edits.
tests/pr_submit/test_conflict_sync_protocol.py::_PRE_EXISTING_VALIDATOR_LINES | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | - **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent
tests/pr_submit/test_conflict_sync_protocol.py::test_evidence_script_named_only_in_conflict_intent | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | other | collect-conflict-evidence.sh
tests/pr_submit/test_conflict_sync_protocol.py::COMMAND_MD | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | other | commands
tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md | in | ## Merge-conflict handling
tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md | in | `--conflict-max-tier` (default 0)
tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | before the first review
tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md | in | at most one conflict cycle per run
tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md | in | uncommitted merge in progress
tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md | in | no review round
tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md | in | not a sandbox
tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md | in | Skill sc:pr-submit-protocol
tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | other | **Step 5. Resolve.**
tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | other | **Step 6
tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | <python> -I -c 'import json, sys; from superclaude.pr_submit.conflicts
tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | `uv run --no-sync python`
tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | never use plain `uv run`
tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | other | **Step 3. Write-ahead.**
tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | other | **Step 4.
tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | conflict_attempt(<run-log events>, cycle_id)
tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | cycle_dir := <output-dir>/sync/<cycle_id>/a<attempt>/
tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | in | --out <cycle_dir><n>/
tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | <cycle_dir>resolution.md
tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | in | `<cycle_dir>` (this attempt only) as `output_dir`
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E1'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | `--conflict-max-tier {0,1,2}` | No (default 0) | Highest merge-conflict tier the skill may act on: 0 (default) detect and report only, 1 also regenerate a conflicted root `uv.lock` (Tier 1, opt-in b [+144 chars]
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E2'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | **STOP** if `--monitor >= 1` and the PR cannot be confirmed on the resolved target repo (origin's\n`owner/repo`, parsed from `git remote get-url origin`): a wrong origin, or a returned URL whose `owne [+241 chars]
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E3'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | `push_count` | int | Landed fix, CI and Tier 2 merge pushes (`kind` on every push record; Tier 1 sync pushes are counted in `sync_push_count`); `<= max_rounds + 1` with the fallback's single push; 0 [+12 chars]
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E3'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | `sync_tier` | int or null | Highest merge-conflict tier seen this run (0 to 3; null when it could not be classified). |
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E3'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | `sync_outcome` | enum | `none` / `report_only` / `left_in_progress` / `pushed` / `aborted` / `halted`. |
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E3'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | `sync_push_count` | int | Landed Tier 1 sync pushes (`kind: "sync"`, at most `SYNC_CAP = 1`); never counted in `push_count`. |
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E4'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | Wave 0c: (L1+) conflict check + report ← loads refs/conflict-mechanical.md ONLY when the probe runs
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E4'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | C-initial: (L3, Tier 2) merge cycle before the first review poll ← loads refs/conflict-mechanical.md + refs/conflict-intent.md
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E4'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | Wave 8a: (L1+) act on a conflict before the CI wait ← loads refs/conflict-mechanical.md ONLY when the probe runs
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E5'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | and rebase if behind `origin/<base>` only at L0 (at L1+ the create path does not rebase and does not halt: the branch is already published when `gh pr create` runs, so report how many commits it is be [+538 chars]
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E6'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | - **Wave 0 conflict check (L1+ only; L0 skips it):** after the head binding, read `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus` (re-read an `UNKNOWN` up to 3 times, 10  [+521 chars]
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E7'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | `--monitor 0` remains no-monitor. **C-initial (L3, Tier 2, only when Wave 0 planned it under `--conflict-max-tier 2`):** after arming and before the first review poll, load `refs/conflict-intent.md` a [+156 chars]
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E8'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`) or is a Tier 2 merge cycle (push kind `merge`; `superclaude.pr_submit.fsm.should_retrigger`), post
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E9'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | load `refs/ci-poll.md`, then run Wave 8a (below) before the CI poll loop. These are
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E9'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | classify_checks(payload, wait_sha=<sha at flip or last push>, expect_checks=<the value recorded for that push, else false>)
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E9'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | without fetching logs, editing, or pushing a fix; the single Tier 1 sync push of Wave 8a (`SYNC_CAP = 1`) is the only push a wait-only path allows, and it is not a fix.
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E9'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | so this push too carries only the cycle's one fix commit; its triad passes `push_kind="ci"`, `review_terminal` and `expect_checks=True`.
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E9'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | Only parsed empty required **and** all-checks lists, with `expect_checks` false, prove there are no Actions; with `expect_checks` true an empty list is `polling`, and expiry is the CI timeout with rea [+34 chars]
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E10'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | - **Wave 8a (L1+, conflict act before the CI wait; same entry outcomes as Wave 8):** read `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus,headRefName,headRefOid,isCrossRep [+952 chars]
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E11'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | - Detect merge conflicts at Wave 0 (L1+), report the tier and plan before any edit, and resolve only within `--conflict-max-tier` and the ordinal ceiling, publishing a resolution only as one merge com [+50 chars]
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E11'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | - Rebase a published PR head (at L1+ the create path no longer rebases), stash, take one side for a whole tree, commit a merge without `scripts/finish-merge.sh`, or push a merge commit whose parents a [+73 chars]
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E12'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | Wrong origin / wrong-owner URL | HALT; instruct operator to close the misrouted PR (FM-11). |
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E12'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | Behind base branch (create path at L1+, or `--pr`) | Tier 0 report ("<N> commits behind"); no rebase, no halt. At L0 the create path still rebases. |
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E12'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | A merge, rebase, cherry-pick, revert or sequencer operation is in progress (L1+) | `terminal_halted`, reason `foreign_op_in_progress`, before anything is created; finish or abort that operation your [+20 chars]
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E12'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | Merge conflict that needs a human (Tier 3: submodule, symlink, mode change, protected or migration path, binary, lock or generated file without a rule, more than 8 text files, unclassifiable) | L3:  [+181 chars]
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E12'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | A conflict cycle stops (dirty tree, foreign merge, guard, finish gate, VAL, rejected or failed push) | `terminal_halted` with the reason from `refs/conflict-mechanical.md` (`merge_preflight_dirty`,  [+139 chars]
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E13'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | (push if you are ahead; `git pull --ff-only` if you are behind; this skill never rewrites a published branch)
tests/pr_submit/test_conflict_sync_protocol.py::_GH_MESSAGE_LINES[POLL_CI_SCRIPT] | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | set member | *) die "installed gh lacks 'gh pr checks --json' (see 'gh --version'); upgrade gh and confirm via 'gh pr checks --help' before CI wait" 2 ;;
tests/pr_submit/test_conflict_sync_protocol.py::test_no_src_superclaude_path | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | not in | src/superclaude
tests/pr_submit/test_conflict_sync_protocol.py::test_static_call_ceilings_in_conflict_mechanical | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh | in | --message-file
tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | with `--pr <N>`, at any level, do not rebase
tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | rebase if behind `origin/<base>`
tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | pr_head_ok(<local branch>, pre_push_sha,
tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | push_parent_ok(<parents>, pre_push_sha)
tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | The deterministic core DECIDES
tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | then set `pre_push_sha := target_sha`
tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/commands/pr-submit.md | in | push any commit besides the cycle's one fix commit
tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | in | the commit to push must have exactly one parent, that same SHA
tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | in | The parent check applies only when the cycle applied edits
tests/pr_submit/test_conflict_sync_protocol.py::SKILL_DIR | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
tests/pr_submit/test_conflict_sync_protocol.py::COMMAND_MD | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | **Step 1. Head check.**
tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | sync_started
tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | merge_preflight_ok
tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | **Step 10(a). Head re-read.**
tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | merge_parent_ok(<parents>, pre_push_sha, base_sha)
tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | --is-ancestor
tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | The deterministic core DECIDES
tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh | set member | --precheck
tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | lock_trust_findings
tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | sync_tier3
tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git checkout --ours -- uv.lock
tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | uv lock\n
tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | uv lock --check
tests/pr_submit/test_conflict_sync_protocol.py::test_trust_limit_is_documented_in_the_refs_skill_and_command | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | collaborators you trust with your credentials
tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_intent_record_fields_in_order | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | .index() | ## 6. The resolution record
tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_intent_record_fields_in_order | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | `## <path>`
tests/pr_submit/test_conflict_sync_protocol.py::test_skill_replaced_text_is_gone | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | **Wave 0 head binding (L1+ only
tests/pr_submit/test_conflict_sync_protocol.py::test_skill_replaced_text_is_gone | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | \n- **Wave 0 conflict check
tests/pr_submit/test_conflict_sync_protocol.py::test_skill_keeps_one_python_block | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .startswith() | ```python
tests/pr_submit/test_conflict_sync_protocol.py::test_the_only_checkout_is_the_lock_file_seed | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | conflict-mechanical.md
tests/pr_submit/test_conflict_sync_protocol.py::test_the_only_checkout_is_the_lock_file_seed | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git checkout
tests/pr_submit/test_conflict_sync_protocol.py::test_allowed_tools_cover_every_program | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | .startswith() | scripts/
tests/pr_submit/test_conflict_sync_protocol.py::test_static_call_ceilings_in_conflict_mechanical | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | scripts/probe-merge.sh
tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | - **Wave 6 (L3 only):**
tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | \n- **Wave 6b
tests/pr_submit/test_conflict_sync_protocol.py::test_intent_and_validator_lines_say_tier_2 | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | not in | conflict-intent.md
tests/pr_submit/test_conflict_sync_protocol.py::test_intent_and_validator_lines_say_tier_2 | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | not in | evidence-validator
tests/pr_submit/test_conflict_sync_protocol.py::test_allowed_tools_cover_every_program | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .startswith() | allowed-tools:
tests/pr_submit/test_conflict_sync_protocol.py::test_static_call_ceilings_in_conflict_mechanical | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | scripts/finish-merge.sh
tests/pr_submit/test_conflict_sync_protocol.py::test_static_call_ceilings_in_conflict_mechanical | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh | not in | --precheck
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | .parametrize() | resolved
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_requires_strict_time_attribution | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | .parametrize() | watermark
tests/pr_submit/test_cosmos_protocol.py::attended_gate | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | contract
tests/pr_submit/test_cosmos_protocol.py::attended_gate | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | pushed_sha
tests/pr_submit/test_cosmos_protocol.py::attended_gate | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | watermark
tests/pr_submit/test_cosmos_protocol.py::attended_gate | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | codex_watermark
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | other | isResolved
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | set member | classify
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | actionable_finding_comments
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | finding_from_comment
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | remap_severity
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | compare | findings
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | other | isResolved
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | other | head_sha
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | .setattr() | classify
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_incomplete_sources_do_not_normalize | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | .setattr() | finding_from_comment
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_incomplete_sources_do_not_normalize | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | comments_ok
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_incomplete_sources_do_not_normalize | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | reviews_ok
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_incomplete_sources_do_not_normalize | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | threads_ok
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | head_sha
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | set member | comments
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | compare | findings
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | other | isResolved
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | other | databaseId
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch | src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | other | severity_hint
tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | other | isResolved
tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | compare | findings
tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | compare | unverified
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | SKILL.md
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | refs/detection-contract.md
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | refs/augment-poll.md
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | set member | refs/review-retrigger.md
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | refs/severity-routing.md
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | refs/thread-reply.md
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | compare | auggie review
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | classify
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | other | actionable_finding_comments
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | watermark
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | current_head_sha
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | findings
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | compare | unverified
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | report-only
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | other | refs/detection-contract.md
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | findings
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_requires_strict_time_attribution | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_requires_strict_time_attribution | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | findings
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_incomplete_sources_do_not_normalize | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_incomplete_sources_do_not_normalize | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | findings
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | other | refs/detection-contract.md
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | findings
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | has_findings
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | findings_count
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | other | refs/detection-contract.md
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | findings
tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | findings
tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | report-only
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | RunConfig.rereview_outcome
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | optimistic legacy default
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | evidence-validator
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | without\nresetting elapsed time
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | Never pass `review_state="findings"` with an empty `findings` list
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | set member | not a stable\npublic API
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | set member | documentary fields, not runtime parser rules
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | set member | lower bound
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | set member | strictly\nnewer than `watermark`
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | observed_at
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | reviews_ok
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | comments_ok
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | threads_ok
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | set member | comments(first:1)
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | set member | pageInfo{hasNextPage endCursor}
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md | set member | all three flags false
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | body="auggie review"
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | payload.head_sha == pushed_sha
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | strictly newer
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | finding_from_comment(raw)
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | ValueError
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | LF or CRLF
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | verification_status="unverified"
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | set member | --thread-id
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | set member | no path/line lookalike match
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | set member | idempotency_skip BEFORE reply
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | set member | hasNextPage:false
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | set member | thread.isResolved:true
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | other | refs/detection-contract.md
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | augmentcode[bot]
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | augmentcode
tests/pr_submit/test_cosmos_protocol.py::attended_gate | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | SKILL.md
tests/pr_submit/test_cosmos_protocol.py::attended_gate | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | other | refs/detection-contract.md
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | submitted_at
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | commit_id
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | set member | COMMENTED
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | augmentcode[bot]
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | comments
tests/pr_submit/test_static_grep.py::SKILL_DIR | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | sc-pr-submit-protocol
tests/pr_submit/test_static_grep.py::PR_SUBMIT_PKG | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | other | pr_submit
tests/pr_submit/test_static_grep.py::RETRIGGER_SCRIPT | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | retrigger-review.sh
tests/pr_submit/test_static_grep.py::REVIEW_RETRIGGER_REF | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | review-retrigger.md
tests/pr_submit/test_static_grep.py::AUGGIE_FALLBACK_REF | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | other | auggie-fallback.md
tests/pr_submit/test_static_grep.py::test_t1115_auggie_fallback_flag_parity | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md | other | --depth quick --remediation-offer
tests/pr_submit/test_static_grep.py::_SKILL_MD | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | SKILL.md
tests/pr_submit/test_static_grep.py::PR_SUBMIT_PKG | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
tests/pr_submit/test_static_grep.py::CORE_PURE_FILES | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | state-machine.md
tests/pr_submit/test_static_grep.py::CORE_PURE_FILES | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | severity-routing.md
tests/pr_submit/test_static_grep.py::CORE_PURE_FILES | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | loop-guard.md
tests/pr_submit/test_static_grep.py::CORE_PURE_FILES | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | other | auggie-fallback.md
tests/pr_submit/test_static_grep.py::CORE_PURE_FILES | src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | other | severity_router.py
tests/pr_submit/test_static_grep.py::CORE_PURE_FILES | src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | other | loop_guard.py
tests/pr_submit/test_static_grep.py::AUGGIE_REVIEW_CMD | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | other | commands
tests/pr_submit/test_static_grep.py::test_t105_runtime_repo_pin | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | in | git remote get-url origin
tests/pr_submit/test_static_grep.py::test_skill_pins_inv_s1_silence_rerequest_tokens | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | in | check_idempotent("silence_rerequest_invoked"
tests/pr_submit/test_static_grep.py::test_skill_pins_inv_s1_silence_rerequest_tokens | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md | in | rerequested=
tests/pr_submit/test_static_grep.py::test_skill_pins_inv_s1_silence_rerequest_tokens | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md | in | rerequested_at=
tests/pr_submit/test_static_grep.py::test_t1105_retrigger_token_in_script_not_core | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | in | auggie review
tests/pr_submit/test_static_grep.py::test_t1105_retrigger_token_in_script_not_core | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | not in | auggie review
tests/pr_submit/test_static_grep.py::test_t1115_auggie_fallback_flag_parity | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md | set member | --remediation-offer
tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | in | gh api "repos/${REPO}/issues/${PR}/comments"
tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | in | gh api "repos/${REPO}/pulls/${PR}/comments"
tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | in | ($issue_comments[0] // []) + ($inline_comments[0] // [])
tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | in | --slurpfile issue_comments
tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | in | --slurpfile inline_comments
tests/pr_submit/test_static_grep.py::_RESOLUTION_SCRIPTS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md | other | poll-augment-review.sh
tests/pr_submit/test_static_grep.py::_RESOLUTION_SCRIPTS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | poll-ci-checks.sh
tests/pr_submit/test_static_grep.py::_RESOLUTION_SCRIPTS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | retrigger-review.sh
tests/pr_submit/test_static_grep.py::_RESOLUTION_SCRIPTS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | other | reply-resolve-thread.sh
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | after `gh pr create`, or on `--pr <N>` attach
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | --json headRefName,headRefOid,isCrossRepository
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | pr_head_ok(
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | HEAD_BRANCH := headRefName
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | pre_push_sha := headRefOid
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | `--resume` repeats this binding
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | pr_branch_ok(
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | Do not close the PR.
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | its `target_sha` when the push landed (Branch A)
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | the re-driven push first runs the Wave 6 pre-push head guard
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | At **L0 (`--monitor 0`)** the FSM never leaves `S0_IDLE` — open the PR and return, byte-for-byte identical to today (AC-1).
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | with `--pr <N>`, at any level, do not rebase
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | rebase if behind `origin/<base>`
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | rebase if behind `origin/<base>` only at L0
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Being behind the base branch is not a STOP at L1+
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | | Wrong origin / wrong-owner URL |
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | | Behind base branch (create path at L1+, or `--pr`) |
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | reason `pr_head_mismatch`; nothing pushed; do NOT close the PR
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | Pre-push head guard, before `push_decision`
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | pr_head_ok(<local branch>, pre_push_sha,
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | never local HEAD
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | target_branch := HEAD_BRANCH
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | then set `pre_push_sha := target_sha`
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | push_parent_ok(<parents>, pre_push_sha)
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | `terminal_halted` (reason `push_range_mismatch`)
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | | The commit to push is not exactly one commit on top of the PR head
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | after Branch A, the guard's parent check stops the next push
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | **Fix commit:**
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | commit all of them as exactly one commit
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Next, when the cycle applied edits (a zero-edit cycle has no fix commit
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | An L3 CI push runs the Wave 6 pre-push head guard and push triad with `target_branch := HEAD_BRANCH`
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | runs the guard's parent check (`push_parent_ok`)
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | `terminal_halted` (reason `fix_commit_failed`)
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | A crash re-drive (Branch B) skips this step
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Branch B: skip the Wave 6 fix commit, set `target_sha` from the record
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | pre-push head guard with the record's `pre_push_sha`
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | | The fix touched a file with the operator's own pending changes, the fix commit fails, or HEAD does not advance
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | staging only the files those edits changed (`git add -- <paths>`, never `git add -A` or `git add .`
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | committing with `git commit --only -- <paths>`
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Before the cycle's first edit, record the operator's pending files (`git status --porcelain=v1 -z --untracked-files=all`
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Before staging anything (before the `git add` above), if a path to commit is in `OPERATOR_PENDING`
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | The fix touched files that had your own uncommitted changes: <paths>
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | separate them by hand (do not discard the files)
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | A halted cycle replies to and resolves no thread.
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | The fix commit failed (<error>). Nothing was pushed
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Fix the cause, then either commit and push the fix yourself
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | make your checkout equal the new PR head, then re-run
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | When this cycle made a fix commit, the message adds:
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | This cycle's fixes are in local commit <target_sha>
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | in | the commit to push must have exactly one parent, that same SHA
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | in | The parent check applies only when the cycle applied edits
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/commands/pr-submit.md | in | push any commit besides the cycle's one fix commit
tests/pr_submit/test_static_grep.py::test_skill_forbids_force_push | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Force-push (`--force`, `--force-with-lease`, or a `+` refspec)
tests/pr_submit/test_static_grep.py::test_wait_only_sentences_name_the_one_sync_exception | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | the single Tier 1 sync push of Wave 8a (`SYNC_CAP = 1`) is the only push a wait-only path allows, and it is not a fix
tests/pr_submit/test_static_grep.py::test_wait_only_sentences_name_the_one_sync_exception | src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | in | never an additional fix or fix push. The single exception is the one Tier 1 sync push (5.2d), which is not a fix.
tests/pr_submit/test_static_grep.py::test_wait_only_sentences_name_the_one_sync_exception | src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md | in | the one Tier 1 sync push of Wave 8a is the only push allowed here, and it is not a fix
tests/pr_submit/test_static_grep.py::test_s5a_retrigger_widened_for_merge_cycles_only | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | or is a Tier 2 merge cycle (push kind `merge`; `superclaude.pr_submit.fsm.should_retrigger`)
tests/pr_submit/test_static_grep.py::test_s5a_retrigger_widened_for_merge_cycles_only | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`) or is a Tier 2 merge cycle (push kind `merge`; `superclaude.pr_submit.fsm.should_retrigger`), post
tests/pr_submit/test_static_grep.py::test_s5a_retrigger_widened_for_merge_cycles_only | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Next, when the cycle applied edits (a zero-edit cycle has no fix commit
tests/pr_submit/test_static_grep.py::test_s5a_retrigger_widened_for_merge_cycles_only | src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | in | The parent check applies only when the cycle applied edits
tests/pr_submit/test_static_grep.py::SKILL_DIR | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
tests/pr_submit/test_static_grep.py::AUGGIE_REVIEW_CMD | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
tests/pr_submit/test_static_grep.py::test_t1115_auggie_fallback_flag_parity | src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md | not in | --no-post-pr
tests/pr_submit/test_static_grep.py::test_t1115_auggie_fallback_flag_parity | src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md | not in | --auggie-model
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | .index() | The deterministic core DECIDES
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | .index() | pr_head_ok(<local branch>, pre_push_sha,
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | (reason `pr_head_mismatch`)
tests/pr_submit/test_static_grep.py::test_skill_forbids_force_push | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .search() | git push origin <target_sha>:<target_branch>
tests/pr_submit/test_static_grep.py::test_wait_only_sentences_name_the_one_sync_exception | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | state-machine.md
tests/pr_submit/test_static_grep.py::test_s5a_retrigger_widened_for_merge_cycles_only | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | state-machine.md
tests/pr_submit/test_static_grep.py::test_skill_pins_inv_s1_silence_rerequest_tokens | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | SKILL.md
tests/pr_submit/test_static_grep.py::test_t1115_auggie_fallback_flag_parity | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | SKILL.md
tests/pr_submit/test_static_grep.py::test_t1115_auggie_fallback_flag_parity | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md | .startswith() | > Skill sc:auggie-review-protocol
tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | in | gh pr view
tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | not in | comments
tests/pr_submit/test_static_grep.py::test_repo_resolution_sed_handles_all_url_forms | src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh | other | , expected
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | **Wave 0 head binding (L1+ only
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | \n- **Wave 1
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | - **Wave 6 (L3 only):**
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | \n- **Wave 6b
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | - **Wave 8 (L1+
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | - **Wave 4:**
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | \n- **Wave 5
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | state-machine.md
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/commands/pr-submit.md | .index() | **Will Not:**
tests/pr_submit/test_static_grep.py::test_skill_forbids_force_push | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | ## Will Not Do
tests/pr_submit/test_static_grep.py::test_wait_only_sentences_name_the_one_sync_exception | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | other | ci-poll.md
tests/pr_submit/test_static_grep.py::test_s5a_retrigger_widened_for_merge_cycles_only | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | - **Wave 6 (L3 only):**
tests/pr_submit/test_static_grep.py::test_s5a_retrigger_widened_for_merge_cycles_only | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | \n- **Wave 6b
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | other | commands
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
tests/pr_submit/test_static_grep.py::test_repo_resolution_sed_handles_all_url_forms | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | in | git remote get-url origin
tests/pr_submit/test_static_grep.py::test_repo_resolution_prefers_origin_over_gh_default | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | in | git remote get-url origin
tests/pr_submit/test_static_grep.py::test_repo_resolution_prefers_origin_over_gh_default | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | in | gh repo view --json nameWithOwner
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-auggie-review-protocol/SKILL.md', 'gh pr', [+151 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-auggie-review-protocol/SKILL.md', 'gh pr', [+157 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-auggie-review-protocol/SKILL.md', 'gh pr', [+55 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-auggie-review-protocol/SKILL.md', 'gh pr', [+48 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-auggie-review-protocol/SKILL.md', 'gh pr', [+103 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-auggie-review-protocol/SKILL.md', 'gh pr', [+80 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubri [+248 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-crash-recovery/SKILL.md', 'git commit', '- [+184 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-crash-recovery/refs/investigators.md', 'gi [+47 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/SKILL.md', 'git commit+gi [+1351 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/SKILL.md', 'git add', '** [+213 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/SKILL.md', 'git add', '-  [+93 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/SKILL.md', 'git add', '** [+299 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md', [+300 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md', [+102 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md', [+520 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md', [+207 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md', [+212 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md', [+283 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/refs/promotion-adapters.m [+258 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md', 'gh api', [+889 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md', 'gh api', [+241 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md', 'gh api', [+286 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/commands/auggie-review.md', 'gh pr', '- **Remote PR* [+60 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/agents/issue-worker-t1.md', 'gh pr+gh api', '- **Rea [+658 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/agents/issue-worker-t2.md', 'gh pr+gh api', '- **Rea [+658 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/agents/issue-worker-t3.md', 'gh api', '- **Read-only [+512 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/agents/issue-worker-t3.md', 'gh api+gh pr', '1. **Cl [+1044 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-issue-protocol/SKILL.md', 'gh api', '- Eve [+160 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-issue-protocol/refs/claim.md', 'gh api', ' [+146 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-issue-protocol/refs/claim.md', 'gh api', ' [+216 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-issue-protocol/refs/claim.md', 'gh pr', '- [+275 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-issue-protocol/refs/create.md', 'gh api',  [+269 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
tests/skills/test_worker_contract.py::test_read_only_entries_are_not_gh_api_posts | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | compare | read-only

## Pass B: readers of target text (test or helper), tagged PIN or RULE
tests/commands/test_impact_command.py::test_impact_callers_may_invoke_skill RULE
tests/commands/test_impact_command.py::test_impact_callers_wired PIN
tests/pr_submit/test_codex_reviews.py::_skill_gate RULE
tests/pr_submit/test_codex_reviews.py::test_skill_gate_adds_the_codex_part_on_the_same_snapshot RULE
tests/pr_submit/test_codex_reviews.py::test_skill_gate_codex_part_keeps_the_pushed_head_and_watermark_rules PIN
tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules RULE
tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout RULE
tests/pr_submit/test_conflict_scripts.py::test_evidence_script_static_rules RULE
tests/pr_submit/test_conflict_scripts.py::test_finish_script_static_rules RULE
tests/pr_submit/test_conflict_scripts.py::test_poll_ci_evidence_mode_static_rules RULE
tests/pr_submit/test_conflict_scripts.py::test_probe_script_static_rules RULE
tests/pr_submit/test_conflict_scripts.py::test_without_timeout_a_hung_read_is_stopped_at_the_budget PIN
tests/pr_submit/test_conflict_scripts.py::test_without_timeout_a_normal_run_still_succeeds PIN
tests/pr_submit/test_conflict_sync_protocol.py::test_allowed_tools_cover_every_program RULE
tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation PIN
tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_intent_pinned_phrases PIN
tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_intent_record_fields_in_order RULE
tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins PIN
tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_pinned_phrases PIN
tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory RULE
tests/pr_submit/test_conflict_sync_protocol.py::test_every_git_push_in_new_files_is_the_one_form RULE
tests/pr_submit/test_conflict_sync_protocol.py::test_evidence_script_named_only_in_conflict_intent RULE
tests/pr_submit/test_conflict_sync_protocol.py::test_fr21_prohibited_operation_scan RULE
tests/pr_submit/test_conflict_sync_protocol.py::test_gh_command_lines_are_repo_scoped RULE
tests/pr_submit/test_conflict_sync_protocol.py::test_intent_and_validator_lines_say_tier_2 RULE
tests/pr_submit/test_conflict_sync_protocol.py::test_no_src_superclaude_path RULE
tests/pr_submit/test_conflict_sync_protocol.py::test_skill_edit_present RULE
tests/pr_submit/test_conflict_sync_protocol.py::test_skill_keeps_one_python_block RULE
tests/pr_submit/test_conflict_sync_protocol.py::test_skill_replaced_text_is_gone RULE
tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive RULE
tests/pr_submit/test_conflict_sync_protocol.py::test_static_call_ceilings_in_conflict_mechanical RULE
tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock PIN
tests/pr_submit/test_conflict_sync_protocol.py::test_the_only_checkout_is_the_lock_file_seed RULE
tests/pr_submit/test_conflict_sync_protocol.py::test_trust_limit_is_documented_in_the_refs_skill_and_command RULE
tests/pr_submit/test_cosmos_protocol.py::attended_gate RULE
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context RULE
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override PIN
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean PIN
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_incomplete_sources_do_not_normalize PIN
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch PIN
tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_requires_strict_time_attribution PIN
tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates RULE
tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root RULE
tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments RULE
tests/pr_submit/test_static_grep.py::test_repo_resolution_prefers_origin_over_gh_default RULE
tests/pr_submit/test_static_grep.py::test_repo_resolution_runs_origin_first_then_falls_back RULE
tests/pr_submit/test_static_grep.py::test_repo_resolution_sed_handles_all_url_forms RULE
tests/pr_submit/test_static_grep.py::test_s5a_retrigger_widened_for_merge_cycles_only PIN
tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head RULE
tests/pr_submit/test_static_grep.py::test_skill_forbids_force_push RULE
tests/pr_submit/test_static_grep.py::test_skill_pins_inv_s1_silence_rerequest_tokens PIN
tests/pr_submit/test_static_grep.py::test_t105_runtime_repo_pin RULE
tests/pr_submit/test_static_grep.py::test_t1101_retrigger_gh_is_repo_scoped RULE
tests/pr_submit/test_static_grep.py::test_t1105_retrigger_token_in_script_not_core RULE
tests/pr_submit/test_static_grep.py::test_t1115_auggie_fallback_flag_parity RULE
tests/pr_submit/test_static_grep.py::test_tn50_core_pure_no_gh_git_tokens RULE
tests/pr_submit/test_static_grep.py::test_wait_only_sentences_name_the_one_sync_exception PIN
tests/skills/test_worker_contract.py::_check_all_classified RULE
tests/skills/test_worker_contract.py::_scan_write_verbs RULE
tests/skills/test_worker_contract.py::test_classification_table_has_no_stale_entries RULE
tests/skills/test_worker_contract.py::test_each_classification_has_one_category_and_a_reason RULE
tests/skills/test_worker_contract.py::test_every_write_verb_hit_is_classified PIN
tests/skills/test_worker_contract.py::test_read_only_entries_are_not_gh_api_posts RULE

## Footer
scanned test files:
  tests/commands/test_impact_command.py
  tests/core/test_how_we_work_routing_table.py
  tests/pr_submit/__init__.py
  tests/pr_submit/conftest.py
  tests/pr_submit/test_auggie_fallback.py
  tests/pr_submit/test_augment_review_remediation.py
  tests/pr_submit/test_autonomy_gates.py
  tests/pr_submit/test_ci_classify.py
  tests/pr_submit/test_codex_reviews.py
  tests/pr_submit/test_conflict_e2e.py
  tests/pr_submit/test_conflict_scripts.py
  tests/pr_submit/test_conflict_sync_protocol.py
  tests/pr_submit/test_conflicts_core.py
  tests/pr_submit/test_contract_setup_diagnosis.py
  tests/pr_submit/test_contract_setup_evidence.py
  tests/pr_submit/test_contract_setup_pr_submit_integration.py
  tests/pr_submit/test_contract_setup_questions.py
  tests/pr_submit/test_contract_setup_validation.py
  tests/pr_submit/test_contract_setup_writer.py
  tests/pr_submit/test_cosmos_poll.py
  tests/pr_submit/test_cosmos_protocol.py
  tests/pr_submit/test_cosmos_review.py
  tests/pr_submit/test_crash_recovery.py
  tests/pr_submit/test_detection_contract.py
  tests/pr_submit/test_edge_cases.py
  tests/pr_submit/test_finding_verify.py
  tests/pr_submit/test_gate_helper_coverage.py
  tests/pr_submit/test_gate_helper_differentials.py
  tests/pr_submit/test_idempotency.py
  tests/pr_submit/test_loop_guard.py
  tests/pr_submit/test_monitor_arm.py
  tests/pr_submit/test_pre_pr_checks.py
  tests/pr_submit/test_rate_limit.py
  tests/pr_submit/test_reply_resolve.py
  tests/pr_submit/test_review_retrigger.py
  tests/pr_submit/test_run_log.py
  tests/pr_submit/test_setup_questions_resolution.py
  tests/pr_submit/test_severity_router.py
  tests/pr_submit/test_silence.py
  tests/pr_submit/test_skill_parse.py
  tests/pr_submit/test_static_grep.py
  tests/pr_submit/test_timeout.py
  tests/pr_submit/test_troubleshoot_seed.py
  tests/pr_submit/test_validated_not_verified.py
  tests/pr_submit/test_validation_gate.py
  tests/skills/test_worker_contract.py
  tests/unit/test_cli_install.py
target files:
  src/superclaude/commands/pr-submit.md
  src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
  src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md
  src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md
  src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md
  src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md
  src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md
  src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md
  src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md
  src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md
  src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md
  src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md
  src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md
  src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md
  src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md
  src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh
  src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh
  src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh
  src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh
  src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh
  src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh
  src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh
pass A rows: 480
pass B readers: 63
command: uv run python -I .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py
cap: a pass A literal is shown up to 200 characters; the full text is in the named test
rule names: .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py --rule-names
<!-- o3-scan:end -->

### O3 rule cards

#### RULE tests/commands/test_impact_command.py::test_impact_callers_may_invoke_skill

- **Files:** six files, one per parameter `rel`: `src/superclaude/skills/sc-task-protocol/SKILL.md`, `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`, `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`, `src/superclaude/skills/sc-implement-protocol/SKILL.md`, `src/superclaude/skills/sc-reflect-protocol/SKILL.md`.
- **Scope:** the front matter block only (the text between the first two `---`), read key by key at the first colon.
- **Predicate:** when the file has a non-empty `allowed-tools` value, splitting that value on `,` and stripping each piece must give a set that contains the item `Skill`.
- **Exemptions:** none. A file with no `allowed-tools` value passes. Plan tasks at risk: T9 and T10 (they edit this SKILL.md; do not touch its front matter).
- **Not a pin:** no regex; nothing is fed to the test.

Helpers it calls: `_frontmatter`.

#### RULE tests/pr_submit/test_codex_reviews.py::_skill_gate

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` (the test file names it `SCRIPTS.parent / "SKILL.md"`).
- **Scope:** the whole file text, searched with the regex `` ```python\n(.*?)\n``` `` in DOTALL mode.
- **Predicate:** the regex must find exactly one block; that block is compiled and run with the names `payload`, `contract` (the detection contract), `pushed_sha`, `watermark` and `codex_watermark`, so it must still run without error. This helper is called by every Codex gate test, so a second fenced python block, or a change to the block, breaks them all.
- **Exemptions:** none. Plan tasks at risk: T9 and T10 (add no python fence and leave the block alone).
- **Not a pin:** the five namespace names are the test's own inputs, not text pins.

#### RULE tests/pr_submit/test_codex_reviews.py::test_skill_gate_adds_the_codex_part_on_the_same_snapshot

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` through the helper `_skill_gate` (the one python block).
- **Scope:** the one python block of SKILL.md, run on the fixture `findings336`.
- **Predicate:** the run must give `codex_state == "findings"`, three codex findings whose `reviewer` is `"codex"`, `codex_routes == ["--fix"] * 3`, `activity == {"augment": True, "codex": True}`, and `review_state` equal to `classify(findings336, CONTRACT)`.
- **Exemptions:** none. Plan tasks at risk: T9 and T10 (leave the block alone).
- **Not a pin:** the expected values are the test's own assertions about the block's output, not text in SKILL.md.

Helpers it calls: `_skill_gate`.

#### RULE tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`.
- **Scope:** the whole text for the thirteen literal fragments (all listed in Pass A for this test, for example `dedup_groups(findings)` and `rereview_requested{cycle_id, reviewer, timestamp}`); then three slices: `events` = from `Every event that concerns one reviewer` up to the first `On `--resume`` after it; `resume` = from `**Resume of a re-triggered cycle:**` to the end of the file.
- **Predicate:** each fragment is a literal substring of the whole text. Each of nine event names (`poll_result`, `review_detected`, `findings_normalized`, `finding_verified`, `finding_unverified`, `route_decision`, `reply_posted`, `thread_resolved`, `rereview_requested`) appears wrapped in backticks inside the `events` slice. In the `resume` slice the first `pending_retriggers` comes before the first `before the S5 poll`.
- **Exemptions:** none. Plan tasks at risk: T9 and T10 (add new text as new lines; do not move or reword the anchors above).
- **Not a pin:** the event names are the test's checklist, not a new pin on top of the fragments.

#### RULE tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh` (constant `EVIDENCE`).
- **Scope:** the whole file text.
- **Predicate:** when the caller passes `limit` other than 60, the text must contain the line `\nLIMIT_SECONDS=60\n` (a line holding exactly `LIMIT_SECONDS=60`); the test then writes a copy with that value replaced. After the run the directory `.git/sc-pr-submit-tmp` must not exist and stdout must be exactly one line.
- **Exemptions:** none. Plan tasks at risk: none (T7 writes a different script).
- **Not a pin:** the 90-second `sleep` wrapper and the tool list are test scaffolding.

#### RULE tests/pr_submit/test_conflict_scripts.py::test_evidence_script_static_rules

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh` and its git index entry (`git ls-files -s` of that path).
- **Scope:** the whole file text, including comments.
- **Predicate:** starts with `#!/usr/bin/env bash\n`; contains the line `set -u -o pipefail`; has the execute bit; none of these regexes matches anywhere: `(?i)\bpush\b`, `(?i)stash`, `(?i)force`, `\bgit\s+config\b`, `--no-verify\b`, `--amend\b`, `src/superclaude`, `\bgit\s+(checkout|switch|reset|commit|add|rm|worktree|rebase|merge)\b`, `\bgh\b`; if the index lists the path its mode starts with `100755 `.
- **Exemptions:** none. Plan tasks at risk: none (the plan does not edit this script).
- **Not a pin:** no sample inputs.

#### RULE tests/pr_submit/test_conflict_scripts.py::test_finish_script_static_rules

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh` and its git index entry.
- **Scope:** the whole file text, including comments.
- **Predicate:** starts with `#!/usr/bin/env bash\n`; contains the line `set -u -o pipefail`; has the execute bit; exactly one match of `\bgit\s+commit\b` and exactly one match of `\bgit commit -F "\$MESSAGE_FILE"`; none of these regexes matches: `\bgit\s+push\b`, `(?i)stash`, `(?i)force`, `\bgit\s+config\b`, `--no-verify\b`, `--amend\b`, `\bcommit\s+(-a|--all|--only)\b`, `src/superclaude`, `\bgit\s+(checkout|switch|reset|add|worktree|rebase|merge)\b`, `\bgh\b`; index mode `100755 ` when listed.
- **Exemptions:** none. Plan tasks at risk: none.
- **Not a pin:** no sample inputs.

#### RULE tests/pr_submit/test_conflict_scripts.py::test_poll_ci_evidence_mode_static_rules

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh`.
- **Scope:** the whole file text for the first and third rules; every physical line for the second rule (comment lines included).
- **Predicate:** `(?i)force` matches nowhere; every line matching `\bgh\s+api\b` also contains `repos/${REPO}/`; the first index of `if [ "$EVIDENCE_MODE" -eq 1 ]; then` is smaller than the first index of `gh pr checks --repo`.
- **Exemptions:** none. Plan tasks at risk: none (do not add the word `force` to this script).
- **Not a pin:** no sample inputs.

#### RULE tests/pr_submit/test_conflict_scripts.py::test_probe_script_static_rules

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh` and its git index entry.
- **Scope:** the whole file text, including comments.
- **Predicate:** starts with `#!/usr/bin/env bash\n`; contains the line `set -u -o pipefail`; has the execute bit; none of these regexes matches: `\bgit\s+push\b`, `\bstash\b`, `\bgit\s+config\b`, `--no-verify\b`, `--amend\b`, `--force\b`, `src/superclaude`, `\bgit\s+(checkout|switch|reset|commit|add|worktree|rebase)\b`, `\bgit\s+merge(\s|$)`, `\bgh\b`; index mode `100755 ` when listed.
- **Exemptions:** none. Plan tasks at risk: none.
- **Not a pin:** no sample inputs.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_allowed_tools_cover_every_program

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` front matter; `src/superclaude/pr_submit/conflicts.py` (`MECHANICAL_RULES`); `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md` and `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md` (`NEW_REFS`). The new `refs/merge-guard.md` is not in this set.
- **Scope:** the SKILL.md text before the first `\n---\n`, its `allowed-tools:` line; fenced lines only in the two refs (`_command_lines`, first word of each non-empty line).
- **Predicate:** the programs (`regenerate[0]` and `check[0]` of every rule plus every first word that is not a `scripts/` path) must be a subset of `{git, gh, uv, make, jq}` and of the set found by `Bash\((\S+) \*\)` in the `allowed-tools:` line; every `scripts/...` first word must name an existing file under the skill folder.
- **Exemptions:** none. Plan tasks at risk: T9 (do not drop a `Bash(<prog> *)` grant from the `allowed-tools:` line).
- **Not a pin:** the allowed-program set is the test's own constant.

Helpers it calls: `_fenced_first_words`, `_read`.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_intent_record_fields_in_order

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md`.
- **Scope:** the slice from `## 6. The resolution record` up to the next `\n## 7.`; inside it, the example from the first `> ## `.
- **Predicate:** in the slice the strings `` `## <path>` `` and then `` `kind:` ``, `` `root_cause:` ``, `` `ours_intent:` ``, `` `theirs_intent:` ``, `` `resolution:` ``, `` `behavior_after:` ``, `` `dropped:` ``, `` `evidence:` `` each appear and their first occurrences are in that order; in the example the lines `\n> kind: `, `\n> root_cause: `, ... `\n> evidence: ` appear in the same order.
- **Exemptions:** none. Plan tasks at risk: none.
- **Not a pin:** no sample inputs.

Helpers it calls: `_assert_in_order`, `_read`.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md` and `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md`.
- **Scope:** whole text; one slice, `step3` = from `**Step 3. Write-ahead.**` up to `**Step 4.` in the mechanical ref.
- **Predicate:** `step3` contains `conflict_attempt(<run-log events>, cycle_id)` and `cycle_dir := <output-dir>/sync/<cycle_id>/a<attempt>/`; the mechanical ref does not contain `sync/<cycle_id>/resolution.md`; the intent ref contains `--out <cycle_dir><n>/`, `<cycle_dir>resolution.md` and `` `<cycle_dir>` (this attempt only) as `output_dir` `` and does not contain `<output-dir>/sync/<cycle_id>/<n>/`.
- **Exemptions:** none. Plan tasks at risk: none.
- **Not a pin:** no sample inputs.

Helpers it calls: `_read`, `_section`.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_every_git_push_in_new_files_is_the_one_form

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md`, `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh` (`NEW_FILES`).
- **Scope:** the whole text of each file, regex `git push[^`\n]*` (one match runs to the next backtick or newline).
- **Predicate:** every match, stripped, must equal `git push origin <target_sha>:<HEAD_BRANCH>`; at least one match must exist across the five files.
- **Exemptions:** none. `refs/merge-guard.md` and `set-draft-state.sh` are not in this set, but `test_skill_forbids_force_push` scans them.
- **Not a pin:** no sample inputs.

Helpers it calls: `_read`.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_evidence_script_named_only_in_conflict_intent

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md` (must hold the name); the surface list = `src/superclaude/commands/pr-submit.md` plus every `.md` and `.sh` file found by `rglob` under `src/superclaude/skills/sc-pr-submit-protocol`. Any new `refs/merge-guard.md` and `scripts/set-draft-state.sh` join this list automatically.
- **Scope:** the whole text of each file, plain substring.
- **Predicate:** the intent ref contains `collect-conflict-evidence.sh`; no other file in the surface list, except the script itself, contains the string `collect-conflict-evidence.sh`.
- **Exemptions:** the intent ref and `scripts/collect-conflict-evidence.sh` itself. Plan tasks at risk: T7, T8, T9, T10, T12 (never write that file name in new text).
- **Not a pin:** no sample inputs.

Helpers it calls: `_read`.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_fr21_prohibited_operation_scan

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md`, `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh` (one test case per file).
- **Scope:** the whole text with MULTILINE regexes, comments and prose included.
- **Predicate:** none of these 15 regexes matches: `\bgit\s+stash\b`, `--no-verify\b`, `--amend\b`, `\badd\s+(-A|--all|\.)(\s|$|``)`, `--(ours|theirs)\s+(--\s+)?\.(\s|$|``)`, `\bcheckout\s+--(ours|theirs)\s*(``|$)`, `-X\s*(ours|theirs)\b`, `-s\s+ours\b`, `\breset\s+--hard\b`, `\bcommit\s+--only\b`, `\bcommit\s+(-a|--all)\b`, `\bgit\s+config\b`, `\bgit\s+worktree\b`, `\bgit\s+rebase\b`, `rerere\.enabled=true`; and every match of `\bgit\s+(checkout|switch)\b` must sit at a place where the text starts with `git checkout --ours -- uv.lock`.
- **Exemptions:** only the one lock-file checkout above. Plan tasks at risk: none (the plan edits none of the five files).
- **Not a pin:** the `forms` tuple in the sibling test `test_prohibited_operation_patterns_catch_each_form` is its own sample input.

Helpers it calls: `prohibited_operation_hits`.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_gh_command_lines_are_repo_scoped

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md`, `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh`.
- **Scope:** `_command_lines`: in `.md` only lines inside ``` fences (fence lines skipped); in `.sh` logical lines with comment lines (first non-blank character `#`) skipped and backslash continuations joined.
- **Predicate:** a line matching `\bgh\s+(pr|api|repo|release|run|auth|search|workflow)\b` must be repo-scoped (`_repo_scoped`): after removing a trailing `\s+#.*$`, it contains the whole token `--repo\b`, or matches `\bgh\s+repo\s+view\b`, or is a `gh api` line containing `repos/` or `graphql`.
- **Exemptions:** one verbatim line in `poll-ci-checks.sh` (`_GH_MESSAGE_LINES`): `*) die "installed gh lacks 'gh pr checks --json' (see 'gh --version'); upgrade gh and confirm via 'gh pr checks --help' before CI wait" 2 ;;`. The reverse check: each exempt line must still equal a stripped command line of that file.
- **Not a pin:** no sample inputs. `set-draft-state.sh` is not in this list; its own `--repo` pin is a design rule, not this test.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_intent_and_validator_lines_say_tier_2

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` and `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md`.
- **Scope:** every physical line of each file, prose included.
- **Predicate:** a line containing `conflict-intent.md` or `evidence-validator` must also contain `Tier 2`. Plan tasks at risk: T9, T10 (a new SKILL.md line that names `evidence-validator` or `conflict-intent.md` needs the words `Tier 2` on that same line).
- **Exemptions:** SKILL.md lines that contain `evidence-validator` but not `conflict-intent.md` and contain either `read-only evidence-validator before diagnosis or edits.` or `- **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent`. Reverse check: both strings must still occur in SKILL.md.
- **Not a pin:** no sample inputs.

Helpers it calls: `_read`.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_no_src_superclaude_path

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md`, `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh`, `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`, `src/superclaude/commands/pr-submit.md` (seven cases).
- **Scope:** the whole text of each file.
- **Predicate:** the substring `src/superclaude` must not occur. Plan tasks at risk: T9, T10, T12 (SKILL.md and the command file); the project rule applies the same ban to `refs/merge-guard.md` and the new script.
- **Exemptions:** none.
- **Not a pin:** no sample inputs.

Helpers it calls: `_read`.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_skill_edit_present

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`.
- **Scope:** the whole text, one case per key `E1` to `E13` of `SKILL_EDITS`.
- **Predicate:** every fragment string of the key is a literal substring of SKILL.md. The fragments are quoted in Pass A under this test (capped at 200 characters; the full text is in the test): `E1` flag row `--conflict-max-tier`, `E2` the STOP paragraph, `E3` four output-table rows, `E4` three wave lines, `E5` to `E13` the other edits. Plan tasks at risk: T9, T10 (add new text as new physical lines; do not reword any line that holds a fragment, and do not change the E3 rows).
- **Exemptions:** none.
- **Not a pin:** no sample inputs. The sibling test `test_skill_edits_cover_e1_to_e13` pins the key set to `E1`..`E13`.

Helpers it calls: `_read`.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_skill_keeps_one_python_block

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`.
- **Scope:** every physical line.
- **Predicate:** exactly one line starts with ```` ```python ```` (so a fence such as ```` ```python3 ```` also counts).
- **Exemptions:** none. Plan tasks at risk: T9, T10 (no python fence in new SKILL.md text; use a plain fence or none).
- **Not a pin:** no sample inputs.

Helpers it calls: `_read`.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_skill_replaced_text_is_gone

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`.
- **Scope:** the whole text for the first rule; for the second, the slice from `**Wave 0 head binding (L1+ only` up to `\n- **Wave 0 conflict check`.
- **Predicate:** the whole text must not contain `and rebase if behind `origin/<base>` (with `--pr <N>``; the slice must not contain `needs a force-push`.
- **Exemptions:** none. Plan tasks at risk: T9 (the Wave 0 hook is added near this slice; keep the words out of it).
- **Not a pin:** no sample inputs.

Helpers it calls: `_read`.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`, `src/superclaude/commands/pr-submit.md`, `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md`.
- **Scope:** SKILL.md whole text, plus the slice from `- **Wave 6 (L3 only):**` up to `\n- **Wave 6b`; the command file whole text; the state-machine ref in prose form (`_prose`: `\n> ` becomes a space, whitespace collapsed).
- **Predicate:** SKILL.md contains `with `--pr <N>`, at any level, do not rebase` and `rebase if behind `origin/<base>``; the Wave 6 slice contains `pr_head_ok(<local branch>, pre_push_sha,`, `push_parent_ok(<parents>, pre_push_sha)`, `The deterministic core DECIDES`, `then set `pre_push_sha := target_sha``; the command file contains `push any commit besides the cycle's one fix commit`; the prose of the state-machine ref contains `the commit to push must have exactly one parent, that same SHA` and `The parent check applies only when the cycle applied edits`.
- **Exemptions:** none. Plan tasks at risk: T10 (Wave 6 bullet and the state-machine overlay).
- **Not a pin:** no sample inputs.

Helpers it calls: `_prose`, `_read`.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_static_call_ceilings_in_conflict_mechanical

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md`.
- **Scope:** fenced lines only (`_command_lines`), each stripped.
- **Predicate:** exactly one line contains `scripts/probe-merge.sh`; exactly one line contains `scripts/finish-merge.sh` and not `--precheck`, and it contains `--message-file`; the lines matching `\bgit\s+push\b` are exactly `["git push origin <target_sha>:<HEAD_BRANCH>"]`.
- **Exemptions:** none. Plan tasks at risk: none.
- **Not a pin:** no sample inputs.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_the_only_checkout_is_the_lock_file_seed

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md`, `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh`.
- **Scope:** the whole text of each file, regex `\bgit\s+(checkout|switch)\b`.
- **Predicate:** the list of `(file name, matched text)` over the five files must be exactly `[("conflict-mechanical.md", "git checkout")]`: one `git checkout` in the mechanical ref, none anywhere else.
- **Exemptions:** none. Plan tasks at risk: none (the plan edits none of the five files).
- **Not a pin:** the `git switch main` string in the sibling pattern test is its own sample.

Helpers it calls: `_read`.

#### RULE tests/pr_submit/test_conflict_sync_protocol.py::test_trust_limit_is_documented_in_the_refs_skill_and_command

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md`, `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`, `src/superclaude/commands/pr-submit.md`.
- **Scope:** prose form (`_prose`: blockquote marker removed, whitespace collapsed).
- **Predicate:** each file's prose contains `collaborators you trust with your credentials`.
- **Exemptions:** none. Plan tasks at risk: T9, T12 (do not reword that sentence).
- **Not a pin:** no sample inputs.

Helpers it calls: `_prose`.

#### RULE tests/pr_submit/test_cosmos_protocol.py::attended_gate

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`.
- **Scope:** whole text, regex `` ```python\n(.*?)\n``` `` in DOTALL mode.
- **Predicate:** exactly one match; it is run with `payload`, `contract` (loaded from `refs/detection-contract.md`), `pushed_sha`, `watermark` = `2026-10-16T19:30:00Z` and `codex_watermark` = None. Called by every attended-gate test.
- **Exemptions:** none. Plan tasks at risk: T9, T10 (no new python fence).
- **Not a pin:** the namespace values are the test's own inputs.

#### RULE tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` (the python block, through `attended_gate`) and the fixture `cosmos-pr266.json`.
- **Scope:** the python block, run with spies on `classify`, `actionable_finding_comments`, `finding_from_comment`, `remap_severity` and `route`.
- **Predicate:** the block must call `classify` and `actionable_finding_comments` with the same call arguments, `payload` first and keyword arguments exactly `{"watermark": "2026-10-16T19:30:00Z", "current_head_sha": "13d246ec9e0d5aad4b6ea70529bebd9496a776e5"}`, and call each of the other three once; the result must be the single report-only finding with the ids asserted in the test.
- **Exemptions:** none. Plan tasks at risk: T9, T10 (leave the block alone).
- **Not a pin:** the fixture values are test data.

Helpers it calls: `attended_gate`.

#### RULE tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` plus `src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md`, `refs/augment-poll.md`, `refs/review-retrigger.md`, `refs/severity-routing.md`, `refs/thread-reply.md` (all under `src/superclaude/skills/sc-pr-submit-protocol`).
- **Scope:** the whole text of each file.
- **Predicate:** each file contains every fragment in its tuple (quoted in Pass A for this test, for example SKILL.md: `RunConfig.rereview_outcome`, `optimistic legacy default`, `evidence-validator`, `without\nresetting elapsed time`, `Never pass `review_state="findings"` with an empty `findings` list`); the loaded contract has `augmentcode[bot]` and `augmentcode` and its first trigger phrase is `auggie review`.
- **Exemptions:** none. Plan tasks at risk: T9, T10 (keep those SKILL.md fragments).
- **Not a pin:** no sample inputs.

#### RULE tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` (python block) and the poll adapter with fixture `cosmos-pr266.json`.
- **Scope:** the python block, run on a real poll payload built from two review pages and two thread pages.
- **Predicate:** the result must show `review_state == "findings"` with one finding with the asserted ids, `verification_status == "unverified"`, severity `LOW`, and `routes == ["report-only"]`; the adapter must have fetched `endCursor=c1` and `page=2`.
- **Exemptions:** none. Plan tasks at risk: T9, T10 (leave the block alone).
- **Not a pin:** the fixture is test data.

Helpers it calls: `attended_gate`.

#### RULE tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh`.
- **Scope:** whole text for the literal checks; `_command_lines` for the `gh pr view` lines.
- **Predicate:** must contain `gh api "repos/${REPO}/issues/${PR}/comments"`, `gh api "repos/${REPO}/pulls/${PR}/comments"`, `($issue_comments[0] // []) + ($inline_comments[0] // [])`, `--slurpfile issue_comments`, `--slurpfile inline_comments`; must not contain `(.comments // [])`, `--argjson issue_comments`, `--argjson inline_comments`; at least one command line contains `gh pr view` and none of them contains `comments`.
- **Exemptions:** none. Plan tasks at risk: none.
- **Not a pin:** no sample inputs.

Helpers it calls: `_command_lines`.

#### RULE tests/pr_submit/test_static_grep.py::test_repo_resolution_prefers_origin_over_gh_default

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh` (`_RESOLUTION_SCRIPTS`).
- **Scope:** every physical line.
- **Predicate:** the first line whose stripped start is `REPO=` or `[ -n` and that contains `git remote get-url origin` comes before the first such line that contains `gh repo view --json nameWithOwner`; both lines must exist.
- **Exemptions:** none. `set-draft-state.sh` is not in this set.
- **Not a pin:** no sample inputs.

#### RULE tests/pr_submit/test_static_grep.py::test_repo_resolution_runs_origin_first_then_falls_back

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh`.
- **Scope:** behavior: the test runs each script's resolution fragment through `_run_resolution`.
- **Predicate:** with an origin command that echoes `https://github.com/acme/widgets.git` the resolved repo is `acme/widgets`; with an origin command that exits 2 it falls back to `upstream/parent`.
- **Exemptions:** none. Plan tasks at risk: none.
- **Not a pin:** the two stub origin commands are test inputs.

Helpers it calls: `_run_resolution`.

#### RULE tests/pr_submit/test_static_grep.py::test_repo_resolution_sed_handles_all_url_forms

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh`.
- **Scope:** every line containing `git remote get-url origin` that also matches `sed -E '([^']*)'`; the first such line gives the sed program.
- **Predicate:** each script must have such a line, and its sed program, run over the five URLs `https://github.com/acme/widgets.git`, `https://github.com/acme/widgets`, `git@github.com:acme/widgets.git`, `ssh://git@github.com/acme/widgets.git`, `git@gitlab.com:acme/widgets.git`, must print `acme/widgets` for each.
- **Exemptions:** none. Plan tasks at risk: none.
- **Not a pin:** the five URLs are test inputs.

#### RULE tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`, `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md`, `src/superclaude/commands/pr-submit.md`.
- **Scope:** whole text plus four slices of SKILL.md: `binding` = from `**Wave 0 head binding (L1+ only` up to the first `\n- **Wave 1`; `wave6` = from `- **Wave 6 (L3 only):**` up to `\n- **Wave 6b`; `wave4` = from `- **Wave 4:**` up to `\n- **Wave 5`; `wave8` = from `- **Wave 8 (L1+` to the END of the file. The state-machine ref is read in prose form; the command file from `**Will Not:**` to the end.
- **Predicate:** required literals per slice are in Pass A (capped; full text in the test). The order rules are: in `wave6` the index of `Pre-push head guard, before `push_decision`` is smaller than that of `The deterministic core DECIDES`; `**Fix commit:**` comes before the guard; `pr_head_ok(<local branch>, pre_push_sha,` comes before `push_parent_ok(<parents>, pre_push_sha)`, which comes before `The deterministic core DECIDES`; `(reason `pr_head_mismatch`)` comes before the parent check. Banned: `branch (`origin/<default-branch>`) on the create path` anywhere; `the fixes are still in your working tree` in `wave6`. Whole-text pins include the AC-1 sentence and the two table rows `| Wrong origin / wrong-owner URL |` and `| Behind base branch (create path at L1+, or `--pr`) |`.
- **Exemptions:** none. Plan tasks at risk: T9 and T10 (new bullets go in as new physical lines; text inserted inside the Wave 6 slice must not sit between the guard, the parent check and `The deterministic core DECIDES`; anything added after `- **Wave 8 (L1+` is inside `wave8`).
- **Not a pin:** no sample inputs.

#### RULE tests/pr_submit/test_static_grep.py::test_skill_forbids_force_push

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` (the `## Will Not Do` section) and every `.md` and `.sh` file found by `rglob` under `src/superclaude/skills/sc-pr-submit-protocol` (new `refs/merge-guard.md` and `scripts/set-draft-state.sh` included).
- **Scope:** whole text of each file (comments and prose included); for the first check, the SKILL.md text from `## Will Not Do` to the end.
- **Predicate:** the Will Not Do section contains ``Force-push (`--force`, `--force-with-lease`, or a `+` refspec)``; the regex `\bgit push\b[^`\n]*?(\s--force\b|\s-f\b|\s\+\S)` finds no match in any file (a match needs `git push`, then no backtick or newline, then whitespace followed by `--force`, `-f` or `+x`).
- **Exemptions:** none. Plan tasks at risk: T7, T8, T9, T10 (a sentence such as `git push ... --force` on one line, even as a warning, fails).
- **Not a pin:** the four forced forms (`git push --force origin a:b`, `git push --force-with-lease origin a:b`, `git push -f origin a:b`, `git push origin +a:b`) and the plain `git push origin <target_sha>:<target_branch>` are the regex's own samples.

#### RULE tests/pr_submit/test_static_grep.py::test_t105_runtime_repo_pin

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh`.
- **Scope:** `_command_lines` (comment lines skipped, backslash continuations joined) for the line rules; whole text for the origin check.
- **Predicate:** the text contains `git remote get-url origin`; at least one line matches `\bgh\s+pr\b` and at least one matches `\bgh\s+api\b`; every `gh pr` line contains `--repo`; every `gh api` line contains `repos/` or `graphql`.
- **Exemptions:** none. Plan tasks at risk: none.
- **Not a pin:** no sample inputs.

Helpers it calls: `_command_lines`.

#### RULE tests/pr_submit/test_static_grep.py::test_t1101_retrigger_gh_is_repo_scoped

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md` and `src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh`.
- **Scope:** `_command_lines`: in the `.md` only fenced lines; in the `.sh` logical lines with comment lines skipped.
- **Predicate:** any line matching `\bgh\s+(pr|api|repo|release|run|auth|search|workflow)\b` must be repo-scoped: whole token `--repo\b`, or `\bgh\s+repo\s+view\b`, or a `gh api` line with `repos/` or `graphql` (a trailing `\s+#.*$` comment is removed first).
- **Exemptions:** none.
- **Not a pin:** no sample inputs.

Helpers it calls: `_command_lines`, `_repo_scoped`.

#### RULE tests/pr_submit/test_static_grep.py::test_t1105_retrigger_token_in_script_not_core

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh` and `src/superclaude/pr_submit/fsm.py`.
- **Scope:** whole text; the fsm text is lower-cased first.
- **Predicate:** the script contains `auggie review`; the lower-cased `fsm.py` must not contain `auggie review`. Plan tasks at risk: T6 (the `--merge-guard` flag lands in `fsm.py`; never write that phrase there, comments included).
- **Exemptions:** none.
- **Not a pin:** no sample inputs.

#### RULE tests/pr_submit/test_static_grep.py::test_t1115_auggie_fallback_flag_parity

- **Files:** `src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md`, `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`, `src/superclaude/commands/auggie-review.md`.
- **Scope:** whole text; table rows of the command file (lines whose stripped start is the quoted option cell); invocation lines are lines starting `> Skill sc:auggie-review-protocol` in the ref and the inline code spans `` `(> Skill sc:auggie-review-protocol[^`]*)` `` in SKILL.md.
- **Predicate:** the ref and SKILL.md contain `--depth quick --remediation-offer`; the command file has the table rows `| `--depth`` and `| `--remediation-offer``, the `--depth` row contains `quick`, the `--auggie-model` row contains `` `prism-b` ``; at least one invocation line exists and none of them contains `--no-post-pr` or `--auggie-model`.
- **Exemptions:** none. Plan tasks at risk: T9, T10 (keep SKILL.md's fallback invocation line).
- **Not a pin:** no sample inputs.

#### RULE tests/pr_submit/test_static_grep.py::test_tn50_core_pure_no_gh_git_tokens

- **Files:** nine files (`CORE_PURE_FILES`): `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md`, `src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md`, `src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md`, `src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md`, `src/superclaude/pr_submit/fsm.py`, `src/superclaude/pr_submit/severity_router.py`, `src/superclaude/pr_submit/loop_guard.py`, `src/superclaude/pr_submit/ci.py`, `src/superclaude/pr_submit/conflicts.py`. Plan task T5 adds `src/superclaude/pr_submit/merge_guard.py` to this list.
- **Scope:** every physical line of each file: prose, code, comments, docstrings and identifiers all count.
- **Predicate:** the regex `\bgh\b|\bgit\b` (case-sensitive, whole word) must match no line; each file must exist. So the words `gh` and `git` may not appear in any of these files, in the new `merge_guard.py`, in the loop-guard text edited by T2 or in the state-machine overlay edited by T10.
- **Exemptions:** none (no exempt line).
- **Not a pin:** no sample inputs. The words `GitHub` and `github` do not match (no word boundary around `git`).

#### RULE tests/skills/test_worker_contract.py::_check_all_classified

- **Files:** the whole result of `_scan_write_verbs` (all files under the three audit roots) against the table `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py`.
- **Scope:** every line of every file under `src/superclaude/skills`, `src/superclaude/commands`, `src/superclaude/agents` (see the `_scan_write_verbs` card).
- **Predicate:** the set of hit keys `(relative path, verb string, whole stripped line)` minus the set of table keys must be empty; the table key is the whole stripped line. Any new line with a write verb needs its own table entry, or `test_every_write_verb_hit_is_classified` fails.
- **Exemptions:** none.
- **Not a pin:** no sample inputs.

Helpers it calls: `_scan_write_verbs`.

#### RULE tests/skills/test_worker_contract.py::_scan_write_verbs

- **Files:** every file (any suffix, read as UTF-8; undecodable files skipped) found by `rglob` under three roots: `src/superclaude/skills`, `src/superclaude/commands`, `src/superclaude/agents`. New files such as `refs/merge-guard.md` and `scripts/set-draft-state.sh` are inside the roots.
- **Scope:** every physical line (prose, comments and code alike), stripped.
- **Predicate:** a line is a hit when `WRITE_VERB_RE` finds a match: `\b(?:git(?:\s+-C\s+\S+)?\s+(?:add|commit|push|merge|stash|update-ref|worktree\s+(?:add|remove))|gh\s+(?:pr|api))(?![\w-])`. The verb string is the match with `-C <path>` removed and whitespace collapsed; several different verbs on one line are joined with `+` in order of first appearance. Hit key = `(path relative to the repo, verb string, stripped line)`. So `gh pr ready` or `gh api graphql` anywhere in the new files is a hit that needs an entry.
- **Exemptions:** none. `git merge-base` is not a hit (the verb must not be followed by a word character or `-`).
- **Not a pin:** no sample inputs.

Helpers it calls: `_rel`.

#### RULE tests/skills/test_worker_contract.py::test_classification_table_has_no_stale_entries

- **Files:** the table `WRITE_VERB_CLASSIFICATION` against the live hit set of `_scan_write_verbs`.
- **Scope:** the whole table.
- **Predicate:** every table key must still be a live hit key: the path, the verb string and the stripped whole line must all match. Editing a classified line (for example the SKILL.md Wave 6 bullet) without updating its key in the same task makes the old key stale and fails here, and the edited line is then also unclassified.
- **Exemptions:** none.
- **Not a pin:** no sample inputs.

Helpers it calls: `_scan_write_verbs`.

#### RULE tests/skills/test_worker_contract.py::test_each_classification_has_one_category_and_a_reason

- **Files:** every entry of `WRITE_VERB_CLASSIFICATION` (one case per key).
- **Scope:** the value pair `(category, reason)`.
- **Predicate:** the category must match `^(?:wc9-allowed|deferred:P[1-4]|never-worker|no-command|read-only)$`; the reason must be non-blank and contain no newline.
- **Exemptions:** none.
- **Not a pin:** the category names are the test's own enum.

#### RULE tests/skills/test_worker_contract.py::test_read_only_entries_are_not_gh_api_posts

- **Files:** every entry of `WRITE_VERB_CLASSIFICATION` whose category is `read-only`.
- **Scope:** the key's whole stripped line (third element).
- **Predicate:** no `read-only` line may be a `gh api` post. `_is_gh_api_post` is true when the line matches `\bgh\s+api\b` and either matches `(?:--method|-X)\s+(?!GET\b)[A-Za-z]+`, or has no `(?:--method|-X)\s+GET\b` and matches `(?:^|\s)(?:-f|-F|--field|--raw-field|--input)(?=\s|=|$)|\bgh\s+api\s+graphql\b`. A `gh api graphql` line in `set-draft-state.sh` must therefore be classed `never-worker`, never `read-only`.
- **Exemptions:** none.
- **Not a pin:** no sample inputs.

Helpers it calls: `_is_gh_api_post`.

### O3 write-verb key cards

One card per key of `WRITE_VERB_CLASSIFICATION` (`tests/skills/test_worker_contract.py`) that holds a line of `SKILL.md` (eight) or of `src/superclaude/commands/pr-submit.md` (the command file's own key). The first-line text is the part of the key before its first `:**` (the whole line when it has none). Other pr-submit files that hold keys (counts): `src/superclaude/commands/pr-submit.md` 1, `refs/augment-poll.md` 6, `refs/ci-poll.md` 6, `refs/conflict-intent.md` 1, `refs/conflict-mechanical.md` 12, `refs/review-retrigger.md` 4, `refs/thread-reply.md` 4, `scripts/finish-merge.sh` 1, `scripts/poll-augment-review.sh` 6, `scripts/poll-ci-checks.sh` 10, `scripts/reply-resolve-thread.sh` 3, `scripts/retrigger-review.sh` 2; their lines stay byte-identical too.

#### KEY - **Wave 0 (all ordinals)

- **File:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`.
- **Verb string:** `gh pr`.
- **Category:** `never-worker`.
- **Rule:** the key is the whole stripped line; any edit to that line must update the key in the same task, or `test_classification_table_has_no_stale_entries` fails; any new line with a write verb needs its own entry, or `test_every_write_verb_hit_is_classified` fails.
- **Plan tasks at risk:** T9 (the Wave 0 hook is a new line next to it).

#### KEY - **Wave 0 conflict check (L1+ only; L0 skips it)

- **File:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`.
- **Verb string:** `gh pr`.
- **Category:** `never-worker`.
- **Rule:** the key is the whole stripped line; any edit to that line must update the key in the same task, or `test_classification_table_has_no_stale_entries` fails; any new line with a write verb needs its own entry, or `test_every_write_verb_hit_is_classified` fails.
- **Plan tasks at risk:** T9.

#### KEY - **Wave 0 head binding (L1+ only; L0 skips it)

- **File:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`.
- **Verb string:** `gh pr`.
- **Category:** `never-worker`.
- **Rule:** the key is the whole stripped line; any edit to that line must update the key in the same task, or `test_classification_table_has_no_stale_entries` fails; any new line with a write verb needs its own entry, or `test_every_write_verb_hit_is_classified` fails.
- **Plan tasks at risk:** T9.

#### KEY - **Wave 8a (L1+, conflict act before the CI wait; same entry outcomes as Wave 8)

- **File:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`.
- **Verb string:** `gh pr`.
- **Category:** `never-worker`.
- **Rule:** the key is the whole stripped line; any edit to that line must update the key in the same task, or `test_classification_table_has_no_stale_entries` fails; any new line with a write verb needs its own entry, or `test_every_write_verb_hit_is_classified` fails.
- **Plan tasks at risk:** T10.

#### KEY - **Wave 6 (L3 only)

- **File:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`.
- **Verb string:** `git add+git commit+gh pr+git push+gh api`.
- **Category:** `never-worker`.
- **Rule:** the key is the whole stripped line; any edit to that line must update the key in the same task, or `test_classification_table_has_no_stale_entries` fails; any new line with a write verb needs its own entry, or `test_every_write_verb_hit_is_classified` fails.
- **Plan tasks at risk:** T10 (the release bullet is a new physical line after it; never an edit inside it).

#### KEY unless both hold: (1) `gh pr checks --repo "$REPO" --help` lists `--json` (probe the installed CLI;

- **File:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`.
- **Verb string:** `gh pr`.
- **Category:** `never-worker`.
- **Rule:** the key is the whole stripped line; any edit to that line must update the key in the same task, or `test_classification_table_has_no_stale_entries` fails; any new line with a write verb needs its own entry, or `test_every_write_verb_hit_is_classified` fails.
- **Plan tasks at risk:** T9, T10 (leave the line alone).

#### KEY Wave 0: Open PR + verify target   ← (no ref; gh pr create --repo, pre-PR checks)

- **File:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`.
- **Verb string:** `gh pr`.
- **Category:** `never-worker`.
- **Rule:** the key is the whole stripped line; any edit to that line must update the key in the same task, or `test_classification_table_has_no_stale_entries` fails; any new line with a write verb needs its own entry, or `test_every_write_verb_hit_is_classified` fails.
- **Plan tasks at risk:** T9, T10 (leave the line alone).

#### KEY - `git add` any `.claude/` path except `.claude/settings.json`.

- **File:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`.
- **Verb string:** `git add`.
- **Category:** `never-worker`.
- **Rule:** the key is the whole stripped line; any edit to that line must update the key in the same task, or `test_classification_table_has_no_stale_entries` fails; any new line with a write verb needs its own entry, or `test_every_write_verb_hit_is_classified` fails.
- **Plan tasks at risk:** T9, T10 (leave the line alone).

#### KEY **STOP** if `--monitor >= 1` and the CI-wait preflight fails: `gh pr checks --repo <owner/repo> --help` must list `--json`, and the runtime must import `superclaude.pr_submit.ci`. The skill's CI-wait preflight is authoritative.

- **File:** `src/superclaude/commands/pr-submit.md`.
- **Verb string:** `gh pr`.
- **Category:** `never-worker`.
- **Rule:** the key is the whole stripped line; any edit to that line must update the key in the same task, or `test_classification_table_has_no_stale_entries` fails; any new line with a write verb needs its own entry, or `test_every_write_verb_hit_is_classified` fails.
- **Plan tasks at risk:** T12.

### O3 folder-wide readers the scan cannot see

These tests scan whole source folders through constants that name no pr-submit token, so Layer 1 does not list them. They were found with `rg -l -e 'rglob\(' -e 'glob\("\*/SKILL\.md"\)' -e 'AUDIT_ROOTS' -e 'glob\("\*\*/' tests --glob '*.py'` (53 files) and read at their scan lines; the others in that list scan other folders (agents, rules, templates, `sc-recommend`, `sc-workflow-protocol`, `sc-issue-protocol`, the troubleshoot skill, the implement skill, `ccsession-tag`, the CLI) and put no rule on new pr-submit files.

#### FOLDER tests/skills/test_model_alias_policy.py::test_tier_ids_appear_only_in_allowed_paths

- **Files:** every file with suffix `.md`, `.py`, `.json`, `.yaml`, `.yml`, `.sh`, `.txt` or `.toml` under `src/superclaude/agents`, `commands`, `skills`, `cli`, `hooks`, `core`.
- **Rule:** the text `claude-gw-tier` must not occur, except under the allow-list (the issue worker agents, `src/superclaude/skills/sc-issue-protocol/`, `src/superclaude/skills/ccsession-tag/`). New pr-submit text (T7, T8, T9, T10, T12) must not contain it.

#### FOLDER tests/core/test_codegraph_guide.py::test_sentinel_only_in_the_guide

- **Files:** every `.md` under `src/superclaude/{commands,skills,agents,core,modes}` and `plugins/superclaude`, except the two guide files.
- **Rule:** the sentence `Caller rows give the caller's definition line, not the call site.` must not occur in them.

#### FOLDER tests/core/test_how_we_work_routing_table.py::test_guide_is_not_an_at_import_anywhere

- **Files:** every `.md` under `src/superclaude` and `plugins/superclaude`.
- **Rule:** no line may match `^\s*@\S*HOW-WE-WORK` (multiline).

#### FOLDER tests/skills/test_worker_contract.py::_check_no_unattended_sections

- **Files:** every `*.md` directly under `src/superclaude/commands`.
- **Rule:** the set of commands that contain a line `## Unattended mode` must equal the keys of `UNATTENDED_EXPECT` (16 commands: adversarial, analyze, brainstorm, build, business-panel, cleanup-audit, design, document, explain, graph, impact, index, index-repo, init-lite, test, workflow). `pr-submit` is not one, so T12 must not add that heading to `src/superclaude/commands/pr-submit.md`.

#### FOLDER tests/commands/test_graph_command.py::test_graph_no_skill_callers

- **Files:** `src/superclaude/skills/*/SKILL.md` except `sc-graph-protocol`.
- **Rule:** the text `sc:graph-protocol` must not occur in them (T9 and T10 never write it).

Rules that are not text pins and that the block does not show:

- `tests/skills/test_worker_contract.py`: `WRITE_VERB_RE` matches whole-word `gh pr`, `gh api` and the git write verbs on every line under `src/superclaude/{skills,commands,agents}` (scripts included). Each hit must be a key of `WRITE_VERB_CLASSIFICATION`: (repo-relative path, verb text joined with `+` when a line has several, exact stripped line) with a category (`never-worker` for pr-submit, with the standard reason text) and a one-line reason. `test_every_write_verb_hit_is_classified` fails on an unclassified hit; `test_classification_table_has_no_stale_entries` fails when a classified line no longer exists, so the existing Wave 0, Wave 0 head binding, Wave 0 conflict check, Wave 6 and Wave 8a lines of `SKILL.md` are exact keys and must stay byte-identical; new Wave bullets are new physical lines.
- `ruff format --check` formats python fences inside Markdown under `src/`: the new `refs/merge-guard.md` carries no python fence (the pure-module names appear as plain text).

### O4 S5a and Wave 6 pre-push text

The S5a re-trigger text sits inside the single Wave 6 line of `SKILL.md` (starts `- **Wave 6 (L3 only):** load `refs/thread-reply.md`.`). The sentence starting `**S5a re-trigger (FR-8):** load `refs/review-retrigger.md`; a push does NOT auto-trigger a re-review by either bot` and the sentence starting `**Pre-push head guard, before `push_decision`:** re-read` stay unchanged. The release sentence goes into the new Wave 6 bullet as its own physical line placed after the existing Wave 6 line (before `- **Wave 6b`): it says Release runs after `push_completed` and before reply, resolve and the S5a re-trigger, without editing either pinned sentence. The Wave 6 pre-push guard stays the place where the Pre-push open-state read of the ref is run.

## 4. Pinned literal starts for later string-constant tests

- S5a: `**S5a re-trigger (FR-8):** load `refs/review-retrigger.md`; a push does NOT auto-trigger a re-review by either bot — AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`) or is a Tier 2 merge cycle (push kind `merge`; `superclaude.pr_submit.fsm.should_retrigger`), post **one re-trigger comment per present reviewer** BEFORE re-entering the S5 poll:`
- Wave 6 pre-push: `**Pre-push head guard, before `push_decision`:** re-read `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` and require `pr_head_ok(<local branch>, pre_push_sha, headRefName, headRefOid, isCrossRepository)` and `headRefName == HEAD_BRANCH`.`
