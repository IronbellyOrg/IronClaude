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

OWNER CHOSE: build now with no GitHub calls (fake `gh` in tests). Gates G1 (live part), G2 (live part), G4, G5 and G6 are OPEN and are a RELEASE gate: the owner runs them on a disposable fork PR before the feature is merged or turned on by default. The user guide states that draft behaviour is unverified until then. The PR body states this gate plainly. The run that opens the PR must pass `--merge-guard off` when `/sc:pr-submit --monitor 3` runs for this PR. No task of this plan makes a live PR call.

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

How this list was produced: `./artifacts/o3-pin-scan.py` (read-only, standard library only, no network call) reads every `.md` and `.sh` file under `src/superclaude/skills/sc-pr-submit-protocol/` plus `src/superclaude/commands/pr-submit.md`, and scans `tests/pr_submit/*.py`, `tests/skills/test_worker_contract.py`, `tests/commands/test_impact_command.py`, `tests/core/test_how_we_work_routing_table.py` and every other `tests/**/*.py` whose text contains the substring `pr-submit` (which also covers `sc-pr-submit-protocol` and `pr-submit.md`). The six tokens in the script header (`sc-pr-submit-protocol`, `pr-submit.md`, `state-machine.md`, `loop-guard.md`, `ci-poll.md`, `review-retrigger.md`) and the module constants bound to them decide which functions are readers. A reader is a test or helper that reads target text: it reads a constant that names a target file, reads a function-local name assigned from target text (or from another such local), loops over (or comprehends over) such constants and reads the loop variable, or calls a helper that does; the write-verb audit of `tests/skills/test_worker_contract.py` is forced in because it scans whole folders. Pass A lists every string literal of 8 or more characters, held by a reader or by a constant a reader uses, that appears verbatim in a target file; path-valued literals are included and only the length filter applies. Pass B lists every reader, one line each, tagged PIN (a plain contains check) or RULE (the body has a loop or comprehension, a `not in`, an `assert not`, an `is None` or a `re.*` call, so the rule lives in logic that the literals alone do not show). Every RULE reader has one hand-written card below. The python package `src/superclaude/pr_submit/` is not a scan target; the tests that read it are in O3.3.

Layer 1 (literals and the reader list, path literals included) is the unedited scan output: re-run it and diff. Layer 2 (rule cards) is written by hand. Check it two ways: `uv run python -I .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py --rule-names` must equal `rg -o '^#### RULE (\S+)' -r '$1' .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md | LC_ALL=C sort` (run the first command's output through `LC_ALL=C sort` too if the locale is not C), and each card must match its test's loop condition and constants. The completeness of the reader list is also checked by the text-only cross-check in O3.1 below.

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
tests/pr_submit/test_edge_cases.py::test_ec15_gh_not_installed_guarded_in_poll_script | src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | in | command -v gh
tests/pr_submit/test_edge_cases.py::test_ec16_base_branch_halt_documented | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Wrong origin
tests/pr_submit/test_edge_cases.py::test_ec16_base_branch_halt_documented | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | wrong-owner
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
tests/pr_submit/test_edge_cases.py::test_ec15_gh_not_installed_guarded_in_poll_script PIN
tests/pr_submit/test_edge_cases.py::test_ec16_base_branch_halt_documented PIN
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
pass A rows: 483
pass B readers: 65
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

These tests scan whole source folders through constants that name no pr-submit token, so Layer 1 does not list them. They were found with `rg --sort path -l -e 'rglob\(' -e '\.glob\(' -e 'os\.walk' -e 'iterdir\(' -e 'AUDIT_ROOTS' -e 'ls-files' tests --glob '*.py'` (111 files). The text-only filter that keeps files whose text names `superclaude`, `docs`, `docs/`, `_SRC` or `SRC ` leaves 106 candidates; the 5 dropped files are: `tests/hooks/fixtures/launch_level/live_probe.py`, `tests/troubleshoot/test_calibrator_assertions.py`, `tests/troubleshoot/test_headline_threshold.py`, `tests/troubleshoot/test_validator_assertions.py`, `tests/unit/test_eval_runner_master_checkout.py` (each scans only its own test fixtures or a temporary directory; checked by reading the scan lines). Of the 106 candidates, 4 were already carded (the pr-submit tests and the write-verb audit) and the other 102 were each read at their scan call sites by four read-only agents (groups 1 to 4, split by size). Their tables follow the cards: every file has a row saying what it scans and whether a rule reaches the planned edits (`src/superclaude/skills/sc-pr-submit-protocol/**`, `commands/pr-submit.md`, `src/superclaude/pr_submit/*.py`, `docs/user-guide/*.md`). The triage covers tests that scan folders. Tests that read one python module of `src/superclaude/pr_submit/` are in O3.3 below; a rule reached only through a helper in another folder would not be found by either method.


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

#### FOLDER tests/agents/test_tavily_tool_parity.py::test_prose_tavily_ids_are_declared
- **Files:** `src/superclaude/agents/**/*.md` and `src/superclaude/skills/**/*.md` (rglob, sorted). Only files whose front matter contains the tool-surface key are checked (others skipped).
- **Scope:** front matter and body separately. Split is `text.split("---", 2)` (parts[1] = front matter, parts[2] = body); a file not starting with `---` is treated as all body with empty front matter and is skipped.
- **Rule:** in a file that declares `tools:` or `allowed-tools:`, every Tavily tool id found in the body must also appear in the front matter. Id regex `mcp__tavily__tavily_[a-z]+`; key regex `^\s*(tools|allowed-tools):` (MULTILINE, applied to the front matter).
- **Exemptions:** none. Files without the key are skipped.
- **Applies to the planned edits?** Yes, scanned: `sc-pr-submit-protocol/SKILL.md` has `allowed-tools:` and the new `refs/merge-guard.md` and edited refs are .md under skills. It only fails if an edited body names an `mcp__tavily__tavily_*` id (the SKILL.md allowed-tools line declares none). Do not mention one.

#### FOLDER tests/agents/test_tavily_tool_parity.py::test_documenting_files_have_exact_parity
- **Files:** same as above (`src/superclaude/agents/**/*.md`, `src/superclaude/skills/**/*.md`).
- **Scope:** front matter vs body, as above.
- **Rule:** for a file with the tool-surface key whose body contains at least one Tavily id, the set of ids in the front matter must equal the set in the body. Regexes `mcp__tavily__tavily_[a-z]+` and `^\s*(tools|allowed-tools):`.
- **Exemptions:** files with an empty referenced set (no id in the body) are exempt.
- **Applies to the planned edits?** Yes, scanned, but only trips if an edited body names a Tavily id; the pr-submit files name none.

#### FOLDER tests/docs/test_retired_docs_absent.py::test_no_markdown_link_points_at_a_retired_file
- **Files:** `README.md`, and every `*.md` under `src/superclaude`, `plugins/superclaude` and `docs` (rglob, whole real tree, including `docs/user-guide/*.md`, `docs/generated/**`, `.md` under `skills/**/refs`).
- **Scope:** whole file text, markdown link targets only.
- **Rule:** no markdown link may resolve to a retired file. Link regex `\]\(([^)\s#]+)`; targets starting `http://`, `https://`, `mailto:` are skipped; the rest resolve relative to the linking file (`(path.parent / target).resolve()`) and are compared with the `_RETIRED` list: `src/superclaude/core/{ORCHESTRATOR,COMMANDS,PERSONAS,MODES,FLAGS,MCP}.md`, `plugins/superclaude/core/FLAGS.md`, `docs/reference/{examples-cookbook,basic-examples,advanced-workflows,advanced-patterns,integration-patterns,commands-list,suggested-commands,comprehensive-features}.md`, `docs/reference/suggested-commands.md`, `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, `docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md`. `read_text(encoding="utf-8")` runs on every file, so a non-UTF-8 .md would error.
- **Exemptions:** none (only the external-URL prefixes above).
- **Applies to the planned edits?** Yes: new `refs/merge-guard.md`, edited skill refs, `commands/pr-submit.md`, `docs/user-guide/commands.md`, `flags.md` and any other `docs/user-guide/*.md` are scanned. Do not link to any retired file (for example `../reference/commands-list.md`); `src/superclaude/core/FLAGS.md` is retired, so link `docs/user-guide/flags.md` instead.

#### FOLDER tests/skills/test_review_severity_rule.py::test_a_no_any_severity_wording_in_tracked_primitives
- **Files:** `git ls-files -z -- src plugins commands agents skills` run in the repo root (every tracked or staged file of any suffix; a file is decoded as UTF-8 and skipped on decode error); the test then keeps paths starting `src/`, `plugins/`, `commands/`, `agents/`. Untracked, unstaged new files are not seen until `git add`.
- **Scope:** each line, case-insensitive substring match.
- **Rule:** none of these phrases may appear on any line (`BANNED_SEVERITY_PHRASES`): "any issue of any severity", "issues of any severity", "gaps of any severity", "at any severity", "regardless of severity", "no severity level is exempt", "minor issues still pass", "must still be fixed", "still must be fixed", "must be perfect to pass", "ALL findings must be resolved", "CRITICAL, IMPORTANT, and MINOR issues".
- **Exemptions:** none.
- **Applies to the planned edits?** Yes: all of `src/superclaude/skills/sc-pr-submit-protocol/**` (SKILL.md, refs, the new .sh script), `commands/pr-submit.md` and `src/superclaude/pr_submit/*.py` (including merge_guard.py) are under `src/`. `docs/` and `tests/` are not scanned. Avoid the phrases above (for example "must still be fixed", "regardless of severity") in merge-guard, loop-guard or state-machine text.

#### FOLDER tests/skills/test_review_severity_rule.py::test_f_no_old_cap_numbers_outside_implement_protocol
- **Files:** tracked files under `src/` and `plugins/` (same `git ls-files` list), excluding any path containing `sc-implement-protocol`.
- **Scope:** each line, regex case-insensitive.
- **Rule:** no line may match `CAP_REGRESSION`: `(max(imum)?|after|up to) [3-9] (fix|fix-verify|correction) (cycles?|loops?|attempts?)|(failing|failed) [3-9] fix cycles|max-[3-9]-cycles?|\b[3-9]-(fix-)?cycles?\b|fix cycles?: [3-9]\b|after [3-9] failed cycles`.
- **Exemptions:** exactly two `(path, line text)` pairs, both in sc-cli-eval-protocol: `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md` with "Max 3 fix loops, then report blocked", and `src/superclaude/skills/sc-cli-eval-protocol/refs/create-pipeline.md` with "(max 3 fix loops), then report blocked". The test also fails if an allowlist entry goes unused.
- **Applies to the planned edits?** Yes: it reaches `sc-pr-submit-protocol/refs/loop-guard.md`, `state-machine.md`, `merge-guard.md` and `pr_submit/*.py` comments or docstrings. Wording such as "max 3 fix attempts", "after 3 fix cycles", "3-cycle" or "max-3-cycles" fails; write "rounds", or a number outside 3-9, or avoid the "fix/correction + cycles/loops/attempts" pairing. "Round counter" and "3 rounds" are not matched.

#### FOLDER tests/skills/test_review_severity_rule.py::test_i_no_swept_wording_in_tracked_primitives
- **Files:** tracked files under `src/`, `plugins/`, `commands/`, `agents/`, `skills/` (all of `_SCAN_TREES`).
- **Scope:** each line. Phrase matches are case-insensitive substrings; the F1-F6 regexes (case-insensitive) apply only when the line does not contain the word "blocking" (case-insensitive).
- **Rule:** no line may contain any of `SWEEP_PHRASES`: "FAIL: Issues found", "strictly fewer issues", "logged for human review", "zero-tolerance policy for errors", "issues of any severity". A line without "blocking" may not match: F1 `\bif (any )?(findings|issues) (exist|are found|found)\b`; F2 `\bfinds new issues\b`; F3 `\bissues remain unfixed\b`; F4 `\b(apply|applies|applying|applied) (all|ALL) (the )?(consolidated |collected |fidelity )?(fixes|findings|corrections)\b`; F5 `(fix(-| )agent|fix_authorization: true)[^\n]*\bconsolidated\b|\bconsolidated\b[^\n]*(fix(-| )agent|fix_authorization: true)`; F6 `\bif (any )?(unresolved )?(issues|findings) remain`.
- **Exemptions:** three `(path, stripped line)` pairs, all the pm-agent line "- Adds prevention checklist if issues found" in `agents/sc-pm-agent.md`, `src/superclaude/agents/pm-agent.md`, `plugins/superclaude/agents/pm-agent.md`. Each must be used (stale-entry check).
- **Applies to the planned edits?** Yes: new and edited pr-submit skill text, command text and `pr_submit/*.py` lines are scanned. Phrases like "if findings exist" or "if issues remain" in merge-guard.md or loop-guard.md fail unless the same line says "blocking".

#### FOLDER tests/skills/test_review_severity_rule.py::test_k_zero_tolerance_only_with_a_qualifier
- **Files:** tracked files under `src/`, `plugins/`, `commands/`, `agents/`, `skills/`.
- **Scope:** each line.
- **Rule:** a line matching `zero[- ]tolerance` (case-insensitive) must also match the qualifier regex `fabricat|forger|hallucinat|verification|verify|accuracy|dismissal|incremental writing|blocking|The "Zero tolerance" closing line is VERBATIM` (case-insensitive).
- **Exemptions:** two pairs: `src/superclaude/rules/core/anti_hallucination_task_completion_rules.md` and `src/superclaude/rules/core/anti_sycophancy.md`, each with the line "- This is a zero-tolerance rule with NO exceptions". Each must be used.
- **Applies to the planned edits?** Yes (same `src/` coverage as above), but only if an edit writes "zero tolerance"/"zero-tolerance" on a line without one of the qualifier words. Avoid the phrase.

#### FOLDER tests/skills/test_model_alias_policy.py::test_frontmatter_model_is_an_alias_when_present
- **Files:** src/superclaude/agents/*.md, src/superclaude/skills/*/SKILL.md (one level only), src/superclaude/commands/*.md (top level only). No exclusions.
- **Scope:** front matter only. File must start with `---\n`; head is the text before the first `\n---\n`; each line is split at the first `:` and the key `model` is read; value is stripped of whitespace and quotes. Files with no `model:` key are skipped.
- **Rule:** when a `model:` key exists, its value must be in `ALIASES = {"opus", "sonnet", "haiku", "inherit"}`; the three issue-worker agents must instead equal their pinned id.
- **Exemptions:** `ISSUE_WORKER_PINS` = `src/superclaude/agents/issue-worker-t3.md` -> `claude-gw-tier3`, `issue-worker-t2.md` -> `claude-gw-tier2`, `issue-worker-t1.md` -> `claude-gw-tier1a`.
- **Applies to the planned edits?** yes, but only if SKILL.md or commands/pr-submit.md front matter gains a `model:` key; the value must be opus, sonnet, haiku or inherit. Neither file has a `model:` key today (grep confirmed). refs/*.md and pr_submit/*.py are not scanned.

#### FOLDER tests/skills/test_model_alias_policy.py::test_python_selection_constants_are_not_full_model_ids
- **Files:** `SRC.rglob("*.py")` = every .py under src/superclaude (includes src/superclaude/pr_submit/*.py, new merge_guard.py, models.py, run_log.py, fsm.py, `__init__.py`). Skips paths starting `src/superclaude/skills/ccsession-tag/` and keys of `RESIDUAL_FULL_IDS` (empty dict). Files with SyntaxError are skipped.
- **Scope:** python AST; every `ast.Constant` string that is not a module/class/function docstring.
- **Rule:** no string constant may match `FULL_ID = re.compile(r"^claude-(opus|sonnet|haiku|fable)-\d")` (match anchored at the start of the whole string value).
- **Exemptions:** `src/superclaude/skills/ccsession-tag/` prefix; `RESIDUAL_FULL_IDS: dict[str, str] = {}` (empty).
- **Applies to the planned edits?** yes, new and edited pr_submit/*.py are scanned; it trips only if a string literal starts with `claude-opus-<digit>`, `claude-sonnet-<digit>`, `claude-haiku-<digit>` or `claude-fable-<digit>` (docstrings are exempt).

#### FOLDER tests/skills/test_model_alias_policy.py::test_markdown_does_not_pass_full_model_ids_to_model_flags
- **Files:** `_markdown_under("agents", "commands", "skills")` = `rglob("*.md")` under src/superclaude/agents, src/superclaude/commands, src/superclaude/skills (all depths, so skills/sc-pr-submit-protocol/SKILL.md and refs/*.md including new refs/merge-guard.md, and commands/pr-submit.md). Excludes any path containing `skills/ccsession-tag/`.
- **Scope:** each line of the file text.
- **Rule:** no line may match `MODEL_FLAG_WITH_FULL_ID = re.compile(r"--models?[ =]+`?claude-(opus|sonnet|haiku|fable)-\d")`.
- **Exemptions:** only the `skills/ccsession-tag/` path exclusion.
- **Applies to the planned edits?** yes, the edited and new .md files are scanned; it trips only if a line has `--model` or `--models` followed by space(s) or `=`, an optional backtick, then `claude-opus-`, `claude-sonnet-`, `claude-haiku-` or `claude-fable-` plus a digit. No such text exists in the pr-submit files now (grep confirmed).

#### FOLDER tests/roadmap/test_threshold_registry.py::test_constant_defined_exactly_once_in_src
- **Files:** `_SRC_ROOT.rglob("*.py")` with `_SRC_ROOT` = src/superclaude, so every .py under it including src/superclaude/pr_submit/*.py. No exclusions. Parametrized over five names. (An unparsable file raises SyntaxError; there is no skip.)
- **Scope:** python AST via `ast.walk`; counts every `ast.Assign` whose target is a bare `Name` equal to the constant name, and every `ast.AnnAssign` whose target is that `Name`, at any nesting depth (module, class, function locals).
- **Rule:** across all of src/superclaude, the names `ID_PATTERNS`, `CONVERGENCE_THRESHOLDS`, `GATE_FIELD_NAMES`, `THRESHOLDS`, `RETURN_CONTRACTS` are each bound exactly once in total, and that one place is src/superclaude/contracts/__init__.py.
- **Exemptions:** none; the only allowed binding is the canonical one in `src/superclaude/contracts/__init__.py`.
- **Applies to the planned edits?** yes, new and edited pr_submit/*.py are scanned; it trips only if a pr_submit module assigns a plain variable or annotated attribute named exactly `THRESHOLDS`, `ID_PATTERNS`, `CONVERGENCE_THRESHOLDS`, `GATE_FIELD_NAMES` or `RETURN_CONTRACTS` (for example a merge_guard.py constant called `THRESHOLDS`). Use other names such as `GUARD_THRESHOLDS`. Attribute targets (`self.THRESHOLDS = ...`) and tuple-unpacking targets are not counted.

#### FOLDER tests/docs/test_tavily_doc_alignment.py::test_tavily_version_single_pin
- **Files:** roots `src/superclaude` and `docs` (rglob "*"), files only. Suffixes: .md .py .yaml .yml .json .txt .sh .cfg .ini .toml (case-insensitive). Excluded dir names, checked only on the path relative to the root: `.dev`, `.claude`, `dist`, `node_modules`, `.venv`, `__pycache__`, `.git`.
- **Scope:** whole file text (regex finditer).
- **Rule:** every `tavily-mcp@<ver>` must have `<ver>` equal to `0.2.22`. Regex: `tavily-mcp@([A-Za-z0-9.\-]+)`.
- **Exemptions:** none beyond the excluded dirs and suffixes above.
- **Applies to the planned edits?** yes, in principle: every new or edited .md/.sh/.py under src/superclaude (skill, refs, scripts/set-draft-state.sh, pr_submit/*.py, commands/pr-submit.md) and docs/user-guide/*.md is scanned. It trips only if the text contains `tavily-mcp@` with a version other than 0.2.22; avoid writing that string.

#### FOLDER tests/docs/test_tavily_doc_alignment.py::test_no_stale_mcp_tavily_token
- **Files:** same as above (src/superclaude + docs, same suffixes and exclusions).
- **Scope:** whole file text.
- **Rule:** no stale capability token. Banned regex: `mcp\.tavily(?!\.com)`. The string `mcp.tavily.com` is allowed; `mcp_server.tavily` is the replacement.
- **Exemptions:** only the negative lookahead for `.com`.
- **Applies to the planned edits?** yes, same file set (every new or edited .md/.sh/.py in src/superclaude and docs). Trips only if the text contains `mcp.tavily` not followed by `.com`.

#### FOLDER tests/docs/test_tavily_doc_alignment.py::test_no_tavily_json_references
- **Files:** same as above (src/superclaude + docs, same suffixes and exclusions).
- **Scope:** whole file text.
- **Rule:** no file may contain the literal `configs/tavily.json` or match `\btavily\.json\b`.
- **Exemptions:** none.
- **Applies to the planned edits?** yes, same file set; trips only on the string `tavily.json`.

#### FOLDER tests/docs/test_tavily_doc_alignment.py::test_docs_no_default_params_duplication
- **Files:** root `docs` only (rglob "*"), same suffixes and excluded dir names as above.
- **Scope:** whole file text.
- **Rule:** docs must not restate the Tavily default parameters. Banned in any docs file: the literal `"search_depth"` (with double quotes), the literal `search_depth: basic`, or the regex `max_results['\"]?\s*[:=]\s*10`.
- **Exemptions:** none.
- **Applies to the planned edits?** yes for docs/user-guide/commands.md, docs/user-guide/flags.md and any other docs/user-guide/*.md; not for src/. Trips only if the new docs text contains one of those three patterns (for example a `max_results=10` example).

#### FOLDER tests/recommend/test_routing_refresh.py::test_command_dispositions_trace_appendix_c_and_inventory

- **Files:** `src/superclaude/commands/*.md` (top level), file names only.
- **Rule:** the set of command names (file stems, `README.md` excluded) minus `{graph, impact, issue}` must equal the 43 frozen active command names. Editing `commands/pr-submit.md` is safe; adding any new `.md` file in `src/superclaude/commands/` fails. The plan adds none.


#### FOLDER tests/unit/test_cli_install.py::TestInstalledPackageResources

- **Files:** a list of installed package members (a presence check, a subset rule).
- **Rule:** every listed member must exist as a file. New files (`refs/merge-guard.md`, `scripts/set-draft-state.sh`) do not trip it; deleting or renaming any listed pr-submit member does: `sc-pr-submit-protocol/SKILL.md`, `refs/{auggie-fallback,augment-poll,ci-poll,conflict-intent,conflict-mechanical,detection-contract,finding-verify,loop-guard,review-retrigger,severity-routing,state-machine,thread-reply,troubleshoot-dispatch}.md`, `scripts/{collect-conflict-evidence,finish-merge,poll-augment-review,poll-ci-checks,probe-merge,reply-resolve-thread,retrigger-review}.sh` and `commands/pr-submit.md`.


#### FOLDER triage table (every triaged file)

| file | scans | rule that reaches the planned edits (yes/no) |
|---|---|---|
| tests/agents/test_tavily_tool_parity.py | `src/superclaude/agents/**/*.md` and `src/superclaude/skills/**/*.md` (rglob); rf-* tests glob only `agents/rf-*.md` | yes: 2 tests (cards). rf-* tests: no |
| tests/cli/eval/test_coverage_gate_integration.py | eval run output dirs under a temp root (iterdir) | no rule |
| tests/cli/eval/test_single_command.py | eval run output dirs under a temp root | no rule |
| tests/cli/eval/test_symlink_attacks.py | scratch/temp dirs, symlink targets | no rule |
| tests/cli/prd/test_e2e.py | temp `where_dir` glob `scope-discovery*`, `research-notes*` | no rule |
| tests/cli/test_install_mcp_cli.py | `isolated_home` temp dir rglob | no rule |
| tests/commands/test_auggie_review_remediation_chain.py | `src/superclaude/skills/sc-auggie-review-protocol/**` (.md/.json/.yaml/.yml), `commands/auggie-review.md`, `agents/auggie-reviewer.md` | no: only the auggie-review primitive |
| tests/conftest.py | `docs/mistakes/*.md` file-name snapshot before/after the session; size of `docs/memory/solutions_learned.jsonl` | no: only docs/mistakes and docs/memory (no new files there) |
| tests/docs/test_retired_docs_absent.py | `README.md` + `src/superclaude/**/*.md`, `plugins/superclaude/**/*.md`, `docs/**/*.md` (rglob) | yes (card) |
| tests/pr_submit/test_contract_setup_pr_submit_integration.py | `sys.modules` names starting `superclaude.pr_submit.contract_setup` (their source text); `tmp_path.rglob` before/after | no: bans text only in `pr_submit/contract_setup/*.py`; planned edits are models.py, run_log.py, fsm.py, `__init__`, merge_guard.py (none match that prefix) |
| tests/skills/test_issue_worker_agents.py | `skills/sc-issue-protocol/refs/*.md`, `templates/*.md`, issue agents, `commands/issue.md` | no: issue skill only |
| tests/skills/test_review_severity_rule.py | `git ls-files -z -- src plugins commands agents skills` (tracked/staged text files, all suffixes) | yes: 4 tests (cards); other tests there read named files (pragmatic.md, S1_S3_FILES, fixture rows, sc-implement-protocol twins) and none names a pr-submit path |
| tests/skills/test_task_workspace_lifecycle.py | `src/superclaude/skills/sc-implement-protocol/**/*.md` line pointers | no: implement skill only |
| tests/sprint/e2e_real/test_e2e_abort_restore.py | temp `config.results_dir` | no rule |
| tests/sprint/test_handoff_backward_compat.py | temp handoff dir | no rule |
| tests/swarm/test_contract_emission.py | `tmp_path` / output_dir | no rule |
| tests/swarm/test_done_sentinel.py | `tmp_path` | no rule |
| tests/swarm/test_e2e_user_guide.py | temp out dirs | no rule |
| tests/swarm/test_inv007_empty_pool.py | `tmp_path` / output_dir | no rule |
| tests/swarm/test_no_response_cache.py | `src/superclaude/cli/swarm/**/*.py` (AST) | no: swarm package only |
| tests/swarm/test_reduce.py | `tmp_path` / output_dir | no rule |
| tests/swarm/test_resume_regenerates_merge.py | temp outside_dir | no rule |
| tests/unit/test_ccsession_tag.py | `skills/ccsession-tag/**` text (marker ban), temp homes/repos | no: ccsession-tag skill only |
| tests/unit/test_reflexion_pollution_guard.py | `docs/mistakes/test_*-<today>.md`, `unknown-<today>.md` | no: docs/mistakes only |
| tests/audit/test_invariant_preservation_NFR_6_through_10.py | `.dev/tasks/{to-do,done}/TASK-*/` immediate subdirs via iterdir (REPO_ROOT/.dev/tasks); fixture reads | no: only requires subdir names research, qa, synthesis, reviews, phase-outputs to exist somewhere under .dev/tasks; not a planned path |
| tests/cli/eval/test_atomic_setup.py | temp scratch root glob | no: temp dirs only |
| tests/cli/eval/test_eval_run.py | temp eval-runs dirs iterdir | no: temp dirs only |
| tests/cli/eval/test_hook_adapter.py | temp claude_dir hooks dir | no: temp dirs only |
| tests/cli/eval/test_retention_policy.py | reads the single file docs/eval/retention.md; rglob on a scratch root | no: docs/eval/retention.md only, not docs/user-guide |
| tests/cli/eval/test_schema_validate.py | `/tmp/eval-runs` rglob | no: outside the repo |
| tests/cli/test_install_hooks.py | temp settings.json, plus reads of src and plugins `hooks/hooks.json` and hook scripts | no: only hooks files, no planned path |
| tests/recommend/test_cache.py | temp cache dir iterdir | no: temp dirs only |
| tests/recommend/test_routing_refresh.py | reads named files: core/HOW-WE-WORK.md, skills/sc-recommend/SKILL.md, commands/{explain,improve,index-repo,release-split,tdd,build,cleanup,design}.md, fixture JSON, the frozen .dev/tasks research SPEC; one tree glob `commands/*.md` in `test_command_dispositions_trace_appendix_c_and_inventory` | no, see near-miss 1 |
| tests/roadmap/test_recurrence_regression.py | `src/superclaude/cli/roadmap/*.py` (AST of Step calls) and `src/superclaude/cli/**/*.py` (fragility-stub regex); fixture corpus under tests/roadmap/fixtures | no: only the cli tree; src/superclaude/pr_submit is a separate package |
| tests/skills/test_reflect_input_snapshot.py | text guards on skills/sc-reflect-protocol/SKILL.md and refs/input-resolution.md; src vs plugins mirror of sc-implement-protocol/refs/managed-workspace.md; rglob on a temp workunit | no: reflect and implement skill files only |
| tests/skills/test_repo_inventory_nongit.py | runs sc-cleanup-audit-protocol/scripts/repo-inventory.sh on a temp dir | no: temp dir only |
| tests/skills/test_workflow_archive.py | temp package rglob; reads sc-implement-protocol refs/retry.md | no: temp dirs and the implement skill |
| tests/sprint/e2e_real/test_e2e_rerun_happy_path.py | temp results dir glob | no: temp dirs only |
| tests/sprint/test_executor.py | one read of superclaude.cli.sprint.executor source (thread check); temp dirs | no: the sprint executor only |
| tests/sprint/test_rerun_tasks.py | temp results dir glob; fixture jsonl reads | no: temp dirs only |
| tests/swarm/test_amalgamation_modes.py | tmp_path iterdir | no: temp dirs only |
| tests/swarm/test_bare_review_parity.py | tmp out dir glob; golden fixtures | no: temp dirs and fixtures |
| tests/swarm/test_concurrency_python_only.py | `src/superclaude/cli/swarm/**` (rglob `*.py`, `*.sh`, and text suffixes) | no: swarm package only |
| tests/swarm/test_imm6_atomic_write.py | `src/superclaude/cli/swarm/**/*.py` rglob; tmp_path | no: swarm package only |
| tests/swarm/test_kill_cmd.py | tmp_path glob | no: temp dirs only |
| tests/swarm/test_manifest_emission.py | tmp_path iterdir | no: temp dirs only |
| tests/swarm/test_uv_enforcement.py | `src/superclaude/cli/swarm/**` rglob with suffixes .py .sh .md .toml .yaml .yml .cfg .ini | no: swarm package only |
| tests/troubleshoot/test_hc_rename_guard.py | `skills/sc-troubleshoot-protocol/SKILL.md`, `refs/*.md`, `refs/probe-packs/*.md` | no: troubleshoot skill only |
| tests/troubleshoot/test_inline_fallback_parity.py | 4 named surfaces (troubleshoot agent-assertions.md and SKILL.md, agents/evidence-validator.md, agents/confidence-calibrator.md); tests/troubleshoot/fixtures glob | no: troubleshoot files only |
| tests/unit/test_cli_install.py | presence list of installed package members under skills, commands, etc; temp install targets | no, see near-miss 2 |
| tests/cli/eval/test_claude_process_adapter.py | rglob("*.py") over src/superclaude/cli/eval (no-anthropic-import rule) | no, cli/eval only |
| tests/cli/eval/test_containment.py | iterdir of a tmp parent dir | no, temp dir |
| tests/cli/eval/test_hard_guard_real_home.py | iterdir of tmp/fake home and a real-home snapshot helper | no, not the repo |
| tests/cli/eval/test_home_isolation_extend.py | iterdir of a tmp fake_home | no, temp dir |
| tests/cli/eval/test_workflow_vs_task_builder_companion.py | rglob in fixture cleanup of its own mkdtemp roots; rglob on tmp cwd | no, temp dirs |
| tests/cli/reflect/test_no_nesting_guard.py | glob("*.py") over src/superclaude/cli/reflect; reads one fixed file src/superclaude/skills/task-builder/SKILL.md | no, cli/reflect and task-builder only |
| tests/cli/test_init_lite.py | rglob of tmp scaffold dirs | no, temp dirs |
| tests/commands/test_routing_plugin_parity.py | rglob over src/superclaude/skills/sc-recommend and plugins/superclaude/skills/sc-recommend; fixed 4 command mirrors | no, only sc-recommend and help/recommend/workflow/implement commands |
| tests/core/test_codegraph_guide.py | rglob in test_sentinel_only_in_the_guide only | no new card, already carded |
| tests/core/test_how_we_work_routing_table.py | rglob in test_guide_is_not_an_at_import_anywhere only | no new card, already carded |
| tests/roadmap/test_cli_contract.py | glob("*.md") of a tmp output dir | no, temp dir |
| tests/roadmap/test_no_fragility_stubs.py | rglob("*.py") over src/superclaude/cli | no, cli only (pr_submit is not under cli) |
| tests/roadmap/test_retry_contract.py | glob("*.py") over src/superclaude/cli/roadmap | no, cli/roadmap only |
| tests/roadmap/test_threshold_registry.py | rglob("*.py") over all of src/superclaude (test_constant_defined_exactly_once_in_src); rglob over src/superclaude/cli (orphan literals, arch_lint) | yes, one test (card below); the cli-only tests are no |
| tests/skills/test_implement_retry_revert.py | iterdir/rglob/git ls-files on tmp repos and tmp dirs | no, temp dirs |
| tests/skills/test_model_alias_policy.py | agents/skills/commands md frontmatter; all src *.py (AST); agents/commands/skills *.md lines; sc-cleanup-audit-protocol only | yes, three tests besides the already-carded tier-id test (cards below); the other tests read fixed files or sc-cleanup-audit-protocol only |
| tests/sprint/test_checkpoints.py | glob of a tmp results dir | no, temp dir |
| tests/sprint/test_handoff_store.py | glob("*.tmp") of a tmp handoff dir | no, temp dir |
| tests/sprint/test_resume.py | iterdir of tmp results dir | no, temp dir |
| tests/swarm/test_bare_review_golden_regen.py | glob("bare-review-*.md") in tests/swarm golden dir (GOLDEN_DIR) | no, test fixtures only |
| tests/swarm/test_crash_recovery_e2e.py | iterdir/glob of tmp out_dir | no, temp dir |
| tests/swarm/test_inv_suite.py | rglob("*.py") under src/superclaude/cli/swarm (dispatch.py, reduce.py, preflight.py, transports/) | no, cli/swarm only |
| tests/swarm/test_module_shape.py | iterdir of src/superclaude/cli/swarm (top-level .py and subpackages) | no, cli/swarm only |
| tests/swarm/test_no_external_frameworks.py | rglob("*.py") over src/superclaude/cli/swarm | no, cli/swarm only |
| tests/swarm/test_parallel_executor_routing.py | rglob("*.py") over src/superclaude/cli/swarm | no, cli/swarm only |
| tests/swarm/test_per_lens_templates.py | glob("*-output.md") over src/superclaude/cli/swarm/lenses/templates | no, cli/swarm only |
| tests/cli/eval/test_exit_codes.py | src/superclaude/cli/eval/**/*.py (rglob) for a text check; cwd=REPO_ROOT for CLI subprocesses | no (cli/eval only) |
| tests/cli/eval/test_parallel_15.py | iterdir of a temp home root | no (temp dirs) |
| tests/cli/eval/test_path_containment.py | iterdir of temp scratch_root / fake_home | no (temp dirs) |
| tests/cli/eval/test_path_traversal.py | rglob of tmp_path before/after | no (temp dir) |
| tests/cli/eval/test_schema_id_rejection.py | rglob of DEFAULT_SCRATCH_ROOT, tmp_path, sandbox | no (scratch/temp dirs) |
| tests/cli/prd/test_config.py | iterdir of tmp_path | no (temp dir) |
| tests/cli/test_install_codegraph.py | reads two files under .dev/codegraph-migration/evidence/; rest is fixture boxes | no |
| tests/cli/test_install_user_setup.py | src/superclaude/{templates,rules,output-styles} rglob (*.md text rules; personal home paths in .md/.contract/.json) | no (none of the planned paths are under those three folders) |
| tests/cli/test_issue_body_templates.py | src/superclaude/core/ISSUE-*.md and core/CLAUDE.md by name; glob skills/sc-issue*; commands rglob issue.md; plugins/superclaude sc-issue* | no (name-based, only issue primitives) |
| tests/commands/test_graph_command.py | src/superclaude/skills/*/SKILL.md (glob) for `sc:graph-protocol` | no (already carded: test_graph_no_skill_callers; its other tests read only commands/graph.md and the graph skill) |
| tests/commands/test_workflow_command.py | commands/workflow.md, skills/sc-workflow-protocol rglob *.md, plugins/superclaude/skills/sc-workflow-protocol, skills/sc-implement-protocol rglob (.md/.py) and its plugin mirror | no (workflow and implement skills only; sc-pr-submit-protocol not touched) |
| tests/docs/test_tavily_doc_alignment.py | src/superclaude + docs, rglob, text suffixes | YES (4 cards below) |
| tests/hooks/test_launch_job_identity.py | one script src/superclaude/hooks/scripts/launch-job-identity.sh; rglob only on temp job.root | no |
| tests/pr_submit/test_conflict_e2e.py | no tree scan of the real repo; builds temp git repos, iterdir/rglob on temp dirs; behavioural use of superclaude.pr_submit ci/conflicts/fsm/models/run_log and helpers from test_conflict_scripts | no (behavioural; see note) |
| tests/roadmap/test_nfr_compliance.py | src/superclaude/cli/pipeline/*.py (glob) and named files in cli/pipeline, cli/roadmap | no (cli/pipeline and cli/roadmap only) |
| tests/roadmap/test_phase7_hardening.py | iterdir of tmp_path | no (temp dir) |
| tests/roadmap/test_validate_executor.py | iterdir/read of tmp_path | no (temp dir) |
| tests/skills/test_issue_protocol.py | skills/sc-issue-protocol rglob (text: `{owner}/{repo}`, `src/superclaude/`), refs/*.md, agents/issue-worker-t{1,2,3}.md | no (sc-issue-protocol and issue-worker agents only) |
| tests/sprint/test_phase8_halt_fix.py | iterdir of a temp phase dir | no (temp dir) |
| tests/sprint/test_state_dir_isolation.py | `git ls-files` over the whole real repo, file-name suffix only | no (only fails for a tracked name ending `.sprint-exitcode`; see note) |
| tests/swarm/test_no_anthropic_routing.py | src/superclaude/cli/swarm/transports/**/*.py | no |
| tests/swarm/test_no_scoring_engine.py | src/superclaude/cli/swarm/**/*.py | no |
| tests/swarm/test_normalize.py | iterdir/glob of tmp_path and parent temp dirs | no (temp dirs) |
| tests/swarm/test_preflight.py | iterdir of tmp_path | no (temp dir) |
| tests/troubleshoot/test_diagnostic_worker_contract.py | skills/sc-troubleshoot-protocol/SKILL.md and refs rglob *.md, agents/troubleshoot-analyst.md | no (sc-troubleshoot-protocol only) |
| tests/unit/test_install_ccsession.py | skills/ccsession-tag copy and its hooks/session-name.sh; glob only on temp dirs | no |

Notes from the triage: `tests/pr_submit/test_conflict_e2e.py` has no tree rule but tests the `superclaude.pr_submit` package by behavior, so edits to `models.py`, `run_log.py` or `fsm.py` can break it through event or state names. `tests/sprint/test_state_dir_isolation.py` runs `git ls-files` over the whole repo but fails only on a tracked name ending `.sprint-exitcode`. The `tests/skills/test_review_severity_rule.py` tests read `git ls-files` (tracked or staged files), so a new untracked file is not scanned until it is staged.

### O3.1 cross-check

The reader rule of the scan could miss a reader, so completeness is also checked by a second method that does not use the rule. `--uncovered` is text-only: it lists every function of a scanned test file that is not in Pass B, whose body text names a target token (or a module name bound to one) and that contains a read call. Neither method sees tests that read the python package `src/superclaude/pr_submit/` (it is not a scan target); those are in O3.3. Its unedited output, with its command (`uv run python -I .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py --uncovered`):

```text
tests/pr_submit/test_codex_reviews.py::fake_gh | [str(SCRIPTS / script), *args],
tests/pr_submit/test_conflict_scripts.py::run_evidence | str(EVIDENCE),
tests/pr_submit/test_cosmos_poll.py::adapter | args = [str(SCRIPTS / script), "--pr", "266", "--repo", REPO]
tests/pr_submit/test_static_grep.py::test_ci_poll_script_rejects_gh_without_checks_json | str(SKILL_DIR / "scripts" / "poll-ci-checks.sh"),
tests/unit/test_cli_install.py::_install_hooks | assert "session-init.sh" in _PACKAGE_RESOURCES["scripts"]
```

Each row above is not a text pin, for the reason given:

- `tests/pr_submit/test_codex_reviews.py::fake_gh`: runs a script from a fake `gh` and returns its result; it reads no target text.
- `tests/pr_submit/test_conflict_scripts.py::run_evidence`: runs `collect-conflict-evidence.sh` in a temporary repository; the text rules of that script are on the card for `test_evidence_script_static_rules`.
- `tests/pr_submit/test_cosmos_poll.py::adapter`: runs the poll script against a fake `gh`; it reads no target text.
- `tests/pr_submit/test_static_grep.py::test_ci_poll_script_rejects_gh_without_checks_json`: runs `poll-ci-checks.sh` with a fake `gh`; it asserts the script's runtime message `gh pr checks --json` and exit code 2, which is the same text as the exempt `die` line in the `test_gh_command_lines_are_repo_scoped` card; no plan task edits that script.
- `tests/unit/test_cli_install.py::_install_hooks`: installs hook files; it names no pr-submit file (the matched name is the package resource list).

The files that name `pr-submit`, as listed by `rg` (command and unedited output), to compare with the `scanned test files` list in the footer of the scan block above:

```text
$ rg --sort path -l -e 'sc-pr-submit-protocol' -e 'pr-submit' tests --glob '*.py'
tests/commands/test_impact_command.py
tests/core/test_how_we_work_routing_table.py
tests/pr_submit/test_codex_reviews.py
tests/pr_submit/test_conflict_e2e.py
tests/pr_submit/test_conflict_scripts.py
tests/pr_submit/test_conflict_sync_protocol.py
tests/pr_submit/test_conflicts_core.py
tests/pr_submit/test_contract_setup_diagnosis.py
tests/pr_submit/test_contract_setup_pr_submit_integration.py
tests/pr_submit/test_cosmos_poll.py
tests/pr_submit/test_cosmos_protocol.py
tests/pr_submit/test_detection_contract.py
tests/pr_submit/test_edge_cases.py
tests/pr_submit/test_pre_pr_checks.py
tests/pr_submit/test_silence.py
tests/pr_submit/test_static_grep.py
tests/skills/test_worker_contract.py
tests/unit/test_cli_install.py
```

### O3.3 pr_submit package rules found by manual search

The scan targets the skill folder and the command file, not the python package `src/superclaude/pr_submit/`, which tasks T2 to T6 edit (`models.py`, `run_log.py`, `fsm.py`, the package exports and the new `merge_guard.py`). A test that reads one of its modules through a path constant (`PR_SUBMIT_PKG`) or an inline `Path(...)` chain carries no pr-submit token, so neither the reader rule nor `--uncovered` sees it. They were found by this search, whose unedited output is below; each file is explained after it:

```text
$ rg --sort path -l -e 'PR_SUBMIT_PKG' -e '/ "pr_submit"' -e 'superclaude/pr_submit/' -e 'getsource' tests --glob '*.py'
tests/audit/test_wiring_gate.py
tests/cli/eval/test_no_mcp_skip.py
tests/cli/eval/test_orchestrator.py
tests/cli/reflect/test_ensemble_unit.py
tests/pr_submit/conftest.py
tests/pr_submit/test_conflicts_core.py
tests/pr_submit/test_review_retrigger.py
tests/pr_submit/test_static_grep.py
tests/pr_submit/test_validation_gate.py
tests/roadmap/test_anti_instinct_recurrence.py
tests/roadmap/test_certify_gate_eval.py
tests/roadmap/test_cli_contract.py
tests/roadmap/test_convergence.py
tests/swarm/test_contract_emission.py
tests/swarm/test_dispatch.py
tests/swarm/test_openai_compat.py
```

- `tests/pr_submit/test_static_grep.py`: the cards `test_tn50_core_pure_no_gh_git_tokens` and `test_t1105_retrigger_token_in_script_not_core` above, and the two below.
- `tests/pr_submit/test_review_retrigger.py`: the third card below.
- `tests/pr_submit/test_conflicts_core.py`: three tests parse `src/superclaude/pr_submit/conflicts.py` (`test_conflicts_imports_only_allowed_modules`, `test_conflicts_makes_no_io_or_dynamic_calls`, `test_tomllib_import_is_guarded_for_python_3_10`) and one reads the repository `pyproject.toml`; the plan edits neither `conflicts.py` nor `pyproject.toml`, so they apply only if a task touches `conflicts.py`.
- `tests/pr_submit/test_validation_gate.py`: passes path strings to a function, reads no file.
- `tests/pr_submit/conftest.py`: `inspect.getsource` of four `contract_setup` gate modules (`candidate`, `lockgate`, `diagnosis`, `validation`); the plan edits none of them.
- `tests/audit/`, `tests/cli/`, `tests/roadmap/`, `tests/swarm/` files: `inspect.getsource` of modules of other packages.
- `tests/pr_submit/test_contract_setup_pr_submit_integration.py`, `test_contract_setup_writer.py` and `test_setup_questions_resolution.py` read `contract_setup` modules through `module.__file__`; the plan edits none of them.

#### PKG tests/pr_submit/test_static_grep.py::test_tn41_core_never_imports_anthropic

- **Files:** every `*.py` directly under `src/superclaude/pr_submit/` (`PR_SUBMIT_PKG.glob("*.py")`), so the new `merge_guard.py` is included.
- **Scope:** every physical line.
- **Rule:** no line may match `^\s*(import|from)\s+anthropic\b`.
- **Exemptions:** none. **Plan tasks at risk:** T3, T4, T5 (never import `anthropic`).

#### PKG tests/pr_submit/test_static_grep.py::test_tn51_run_log_redacts_credentials_static

- **Files:** `src/superclaude/pr_submit/run_log.py`.
- **Scope:** whole text, plain substrings.
- **Rule:** the text must still contain `_REDACTION_PATTERNS` and `[REDACTED]`.
- **Exemptions:** none. **Plan tasks at risk:** T5 (edits `run_log.py`; keep both strings).

#### PKG tests/pr_submit/test_review_retrigger.py::test_t1105_core_holds_no_hardcoded_trigger_literal

- **Files:** `src/superclaude/pr_submit/fsm.py`, built by an inline `Path(__file__).resolve().parents[2] / "src" / "superclaude" / "pr_submit" / "fsm.py"` chain.
- **Scope:** whole text, lower-cased.
- **Rule:** the lower-cased text must not contain `auggie review` (the same rule as the `test_t1105_retrigger_token_in_script_not_core` card). **Plan tasks at risk:** T6 (the `--merge-guard` flag lands in `fsm.py`).
- **Exemptions:** none.

#### PKG tests/pr_submit/test_run_log.py and tests/pr_submit/test_codex_reviews.py: event-count and state-key pins

- **Files:** `src/superclaude/pr_submit/models.py` (`EventType`) and `src/superclaude/pr_submit/run_log.py` (`rebuild_state`), by import, not by text.
- **Rule:** `len(EventType) == 43` and `len(list(EventType)) == 43` in `test_eventtype_is_43_members_with_silence_reviewer_and_conflict_events` (`tests/pr_submit/test_run_log.py`) and `len(EventType) == 43` in `test_event_enum_has_the_two_reviewer_events` (`tests/pr_submit/test_codex_reviews.py`); `set(state) == set(_LEGACY_EXPECTED) | set(_NEW_KEY_DEFAULTS)` and `state == {**_LEGACY_EXPECTED, **_NEW_KEY_DEFAULTS}` in `test_fold_old_log_without_kind_rebuilds_identically` (`tests/pr_submit/test_run_log.py`).
- **Plan tasks at risk:** T2 (adds two event types, so the three counts become 45 in the same task) and T5 (adds a state key, so `_NEW_KEY_DEFAULTS` gets the new key and its default in the same task).

#### PKG tests/pr_submit/test_idempotency.py::test_t1120_auggie_review_invoked_at_most_once

- **Files:** `src/superclaude/pr_submit/run_log.py` (the tuple `IDEMPOTENCY_SETS`), by import, not by text.
- **Rule:** `"auggie_review_invoked" in IDEMPOTENCY_SETS`, `"silence_rerequest_invoked" in IDEMPOTENCY_SETS` and `len(IDEMPOTENCY_SETS) == 7`.
- **Plan tasks at risk:** T5 (edits `run_log.py`; the plan adds no idempotency set, and the set count must stay 7; `./source.md` section 6 lists this pin as unchanged).

Count and set-size pins in `tests/pr_submit`, searched with the command and unedited output below (the rows about the modules the plan edits are covered by the two cards above; every other row counts test data, script output or a `contract_setup` module the plan does not edit):

```text
$ rg --sort path --no-heading --no-line-number 'len\(.*\) == [0-9]+' tests/pr_submit --glob '*.py' | rg -e 'EventType' -e 'IDEMPOTENCY_SETS' -e 'SETUP_QUESTIONS' -e 'MECHANICAL_RULES' -e 'MonitorState'
tests/pr_submit/test_codex_reviews.py:    assert len(EventType) == 43
tests/pr_submit/test_contract_setup_questions.py:    assert len(SETUP_QUESTIONS) == 16
tests/pr_submit/test_contract_setup_questions.py:    assert len({question.id for question in SETUP_QUESTIONS}) == 16
tests/pr_submit/test_idempotency.py:    assert len(IDEMPOTENCY_SETS) == 7
tests/pr_submit/test_run_log.py:    assert len(EventType) == 43
tests/pr_submit/test_run_log.py:    assert len(list(EventType)) == 43
```

Behavioral tests of these modules (run log, models, fsm) are not listed one by one: the final full-suite run of the last task is compared with the base failures in section 1a.

#### DOC readers of `docs/user-guide/` (task T13 edits `commands.md` and `flags.md`)

The docs folder is not a scan target either. The search below lists the tests that name `user-guide` (command, then unedited output):

```text
$ rg --sort path -l -e 'user-guide' tests --glob '*.py'
tests/audit/test_profiler.py
tests/pr_submit/test_conflict_sync_protocol.py
tests/skills/test_workflow_archive.py
tests/swarm/test_e2e_user_guide.py
```

Only `tests/pr_submit/test_conflict_sync_protocol.py` reads the pr-submit guides; the others name `user-guide` in a path string or a docs path of another topic (`tests/audit/test_profiler.py` classifies a path string, `tests/skills/test_workflow_archive.py` quotes it in a ledger fixture, and `tests/swarm/test_e2e_user_guide.py` runs the examples of `docs/swarm/user-guide.md`, a different guide). The folder rules that scan `docs/` are the `FOLDER` cards above.

#### DOC tests/pr_submit/test_conflict_sync_protocol.py::test_user_guides_document_conflict_cap_and_limits

- **Files:** `docs/user-guide/commands.md` and `docs/user-guide/flags.md` (one case each).
- **Scope:** prose form (`_prose`: `\n> ` becomes a space, whitespace collapsed).
- **Rule:** each guide must contain `` `--conflict-max-tier ``; match the regex `[Dd]efaults? to `0`|`0` \(default`; and contain `two remaining`, `eight text-conflict files` and `not a sandbox`.
- **Exemptions:** none. **Plan tasks at risk:** T13 (add the `--merge-guard` text as new lines; do not reword those five phrases).

Rules that are not text pins and that the block does not show:

- `tests/skills/test_worker_contract.py`: `WRITE_VERB_RE` matches whole-word `gh pr`, `gh api` and the git write verbs on every line under `src/superclaude/{skills,commands,agents}` (scripts included). Each hit must be a key of `WRITE_VERB_CLASSIFICATION`: (repo-relative path, verb text joined with `+` when a line has several, exact stripped line) with a category (`never-worker` for pr-submit, with the standard reason text) and a one-line reason. `test_every_write_verb_hit_is_classified` fails on an unclassified hit; `test_classification_table_has_no_stale_entries` fails when a classified line no longer exists, so the existing Wave 0, Wave 0 head binding, Wave 0 conflict check, Wave 6 and Wave 8a lines of `SKILL.md` are exact keys and must stay byte-identical; new Wave bullets are new physical lines.
- `ruff format --check` formats python fences inside Markdown under `src/`: the new `refs/merge-guard.md` carries no python fence (the pure-module names appear as plain text).

### O4 S5a and Wave 6 pre-push text

The S5a re-trigger text sits inside the single Wave 6 line of `SKILL.md` (starts `- **Wave 6 (L3 only):** load `refs/thread-reply.md`.`). The sentence starting `**S5a re-trigger (FR-8):** load `refs/review-retrigger.md`; a push does NOT auto-trigger a re-review by either bot` and the sentence starting `**Pre-push head guard, before `push_decision`:** re-read` stay unchanged. The release sentence goes into the new Wave 6 bullet as its own physical line placed after the existing Wave 6 line (before `- **Wave 6b`): it says Release runs after `push_completed` and before reply, resolve and the S5a re-trigger, without editing either pinned sentence. The Wave 6 pre-push guard stays the place where the Pre-push open-state read of the ref is run.

## 4. Pinned literal starts for later string-constant tests

- S5a: `**S5a re-trigger (FR-8):** load `refs/review-retrigger.md`; a push does NOT auto-trigger a re-review by either bot — AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`) or is a Tier 2 merge cycle (push kind `merge`; `superclaude.pr_submit.fsm.should_retrigger`), post **one re-trigger comment per present reviewer** BEFORE re-entering the S5 poll:`
- Wave 6 pre-push: `**Pre-push head guard, before `push_decision`:** re-read `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` and require `pr_head_ok(<local branch>, pre_push_sha, headRefName, headRefOid, isCrossRepository)` and `headRefName == HEAD_BRANCH`.`
