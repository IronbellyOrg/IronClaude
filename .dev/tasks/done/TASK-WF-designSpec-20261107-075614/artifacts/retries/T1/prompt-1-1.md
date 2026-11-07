69f360d58d89456f559ad3de21ea75027cd72bb0
Review one task for spec compliance.

Task brief: ## Task 1: Write the pre-build record `./artifacts/pre-build-gate.md`

Create `./artifacts/pre-build-gate.md` in this package from ./source.md sections 6, 8 and 10. First record the base-commit state: run `make lint`, `uv run ruff format --check src/ tests/` and the full suite `uv run pytest -q tests` before any code edit and write each exit code, the pass count and every failing test id (or "clean") into the file, so later failures can be told apart from this feature's. Then record the release-gate decision of ./source.md section 8 in the owner's words: the build proceeds with no GitHub calls (fake `gh` in tests); gates G1 (live part), G2 (live part), G4, G5 and G6 are a release gate that the owner runs on a disposable fork PR before the feature is merged or turned on by default; the user guide states that draft behaviour is unverified until then; the PR body states the gate plainly; the run that opens the PR must pass `--merge-guard off`. Then close the open items by reading the code: O1, where `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` (Wave 3 to Wave 6 and Wave 8 text) and `refs/loop-guard.md` assign a fix or CI cycle's `cycle_id` today and whether any test under `tests/pr_submit/` pins a value; O2, how scripts are granted and invoked in the SKILL front matter and what `test_allowed_tools_cover_every_program` in `tests/pr_submit/test_conflict_sync_protocol.py` and the `_RESOLUTION_SCRIPTS` tests in `tests/pr_submit/test_static_grep.py` require of a new script; O3, every exact-text pin and line-content rule (for example `test_intent_and_validator_lines_say_tier_2`, `test_skill_forbids_force_push`, the wait-only sentences pinned for `refs/state-machine.md`, and the `WRITE_VERB_CLASSIFICATION` table with its stale-entry test in `tests/skills/test_worker_contract.py`) on `SKILL.md`, `refs/state-machine.md`, `refs/loop-guard.md` and `src/superclaude/commands/pr-submit.md` that the later additive edits must avoid; O4, that the S5a re-trigger sentence in `SKILL.md` stays unchanged and where the new release sentence goes relative to it; and the literal start text of the S5a sentence and of the Wave 6 pre-push sentence as the existing pins write them, so later tests can compare against string constants.

Acceptance criteria:
- T1.AC1: `./artifacts/pre-build-gate.md` has the base-commit record (three commands, exit codes, the full-suite pass count and failing test ids, or "clean") and one row each for G1 to G6: G1 to G3 `CONFIRMED` for the locally verifiable part with the evidence named in ./source.md, G1 and G2 live parts, G4, G5 and G6 `OPEN` as a release gate with the owner decision quoted.
- T1.AC2: O1 to O4 each carry the finding with the file and symbol read in this task (no bare line numbers); O1 names one single place where the guard-enabled cycle id is minted so the push triad and `rereview_requested` use the same id, or states that no id is minted today and which sentence will mint it.
- T1.AC3: The file lists every exact-text pin and line-content rule found for O3, including the classification table rule (exact line key, category, stale-entry test), and the literal start text of the two pinned sentences of O4, so Tasks 7 to 13 can avoid or reuse them; no GitHub or network call is made.
Global constraints: - Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
Start sha: 69f360d58d89456f559ad3de21ea75027cd72bb0
Diff against the start snapshot: NEW FILE .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md (full contents, 11808 bytes):
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

- `tests/skills/test_worker_contract.py`: `WRITE_VERB_RE` matches whole-word `gh pr`, `gh api` and the git write verbs on every line under `src/superclaude/{skills,commands,agents}` (scripts included). Each hit must be a key of `WRITE_VERB_CLASSIFICATION`: (repo-relative path, verb text joined with `+` when a line has several, exact stripped line) with a category (`never-worker` for pr-submit, with the standard reason text) and a one-line reason. `test_every_write_verb_hit_is_classified` fails on an unclassified hit; `test_classification_table_has_no_stale_entries` fails when a classified line no longer exists, so the existing Wave 0, Wave 0 head binding, Wave 0 conflict check, Wave 6 and Wave 8a lines of `SKILL.md` are exact keys and must stay byte-identical; new Wave bullets are new physical lines.
- `tests/pr_submit/test_static_grep.py`: `CORE_PURE_FILES` (no whole word `gh` or `git` in `refs/state-machine.md`, `refs/severity-routing.md`, `refs/loop-guard.md`, the core modules and, after Task 5, `merge_guard.py`); `test_skill_binds_checkout_and_push_target_to_pr_head` (Wave 0 head-binding slice ends at `\n- **Wave 1`; the Wave 6 slice from `- **Wave 6 (L3 only):**` to `\n- **Wave 6b` holds ordered pinned phrases: head guard before `The deterministic core DECIDES`, `pr_head_ok(<local branch>, pre_push_sha,`, `then set `pre_push_sha := target_sha``, `commit all of them as exactly one commit`, `A crash re-drive (Branch B) skips this step`, the fix-commit-failed and operator-pending messages, `When this cycle made a fix commit, the message adds:`); `test_skill_forbids_force_push` (Will Not text and the push-line form); `test_wait_only_sentences_name_the_one_sync_exception`; `test_s5a_retrigger_widened_for_merge_cycles_only`; the `state-machine.md` sentences ("the commit to push must have exactly one parent, that same SHA", "The parent check applies only when the cycle applied edits").
- `tests/pr_submit/test_conflict_sync_protocol.py`: `SKILL_EDITS` pins (E1 to E13) with `test_skill_edit_present` and `test_skill_replaced_text_is_gone`; `test_skill_keeps_one_python_block` (exactly one python fence in `SKILL.md`); `test_intent_and_validator_lines_say_tier_2` (a line naming `evidence-validator` or `conflict-intent.md` must also say "Tier 2"; new lines avoid both words); `test_evidence_script_named_only_in_conflict_intent`; `test_gh_command_lines_are_repo_scoped`; `test_no_src_superclaude_path` (no `src/superclaude` text in skill or command files); `test_allowed_tools_cover_every_program`; `test_user_guides_document_conflict_cap_and_limits` and `test_command_summarizes_conflict_protocol_without_replacing_activation` (the command file keeps its Activation section and the conflict summary).
- `tests/pr_submit/test_cosmos_protocol.py` and `test_codex_reviews.py`: one python fence in `SKILL.md`; the `len(EventType)` pin (Task 2).
- `tests/pr_submit/test_run_log.py`: `_NEW_KEY_DEFAULTS` exact key-set pin (Task 5); the event-count test (Task 2).
- `src/superclaude/commands/pr-submit.md`: front matter `argument-hint`, `## Options`, `## Merge-conflict handling`, `## Activation` stay; additive edits only.
- `ruff format --check` formats python fences inside Markdown under `src/`: the new `refs/merge-guard.md` carries no python fence (the pure-module names appear as plain text).

### O4 S5a and Wave 6 pre-push text

The S5a re-trigger text sits inside the single Wave 6 line of `SKILL.md` (starts `- **Wave 6 (L3 only):** load `refs/thread-reply.md`.`). The sentence starting `**S5a re-trigger (FR-8):** load `refs/review-retrigger.md`; a push does NOT auto-trigger a re-review by either bot` and the sentence starting `**Pre-push head guard, before `push_decision`:** re-read` stay unchanged. The release sentence goes into the new Wave 6 bullet as its own physical line placed after the existing Wave 6 line (before `- **Wave 6b`): it says Release runs after `push_completed` and before reply, resolve and the S5a re-trigger, without editing either pinned sentence. The Wave 6 pre-push guard stays the place where the Pre-push open-state read of the ref is run.

## 4. Pinned literal starts for later string-constant tests

- S5a: `**S5a re-trigger (FR-8):** load `refs/review-retrigger.md`; a push does NOT auto-trigger a re-review by either bot — AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`) or is a Tier 2 merge cycle (push kind `merge`; `superclaude.pr_submit.fsm.should_retrigger`), post **one re-trigger comment per present reviewer** BEFORE re-entering the S5 poll:`
- Wave 6 pre-push: `**Pre-push head guard, before `push_decision`:** re-read `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` and require `pr_head_ok(<local branch>, pre_push_sha, headRefName, headRefOid, isCrossRepository)` and `headRefName == HEAD_BRANCH`.`

NEW FILE .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/base-lint.log (full contents, 8301 bytes):
🔍 Checking architecture policy compliance...

=== Check 1/2: Bidirectional Command ↔ Skill Links ===
  ✅ [Check 1]: adversarial → sc-adversarial-protocol
  ✅ [Check 1]: auggie-review → sc-auggie-review-protocol
  ✅ [Check 1]: brainstorm → sc-brainstorm-protocol
  ✅ [Check 1]: cleanup-audit → sc-cleanup-audit-protocol
  ✅ [Check 1]: cli-eval → sc-cli-eval-protocol
  ✅ [Check 1]: cli-portify → sc-cli-portify-protocol
  ✅ [Check 1]: graph → sc-graph-protocol
  ✅ [Check 1]: impact → sc-impact-protocol
  ✅ [Check 1]: implement → sc-implement-protocol
  ✅ [Check 1]: init-lite → sc-init-lite-protocol
  ✅ [Check 1]: issue → sc-issue-protocol
  ✅ [Check 1]: pm → sc-pm-protocol
  ✅ [Check 1]: post-release → sc-post-release-protocol
  ✅ [Check 1]: pr-submit → sc-pr-submit-protocol
  ✅ [Check 1]: recommend → sc-recommend (utility skill; no -protocol suffix)
  ✅ [Check 1]: reflect → sc-reflect-protocol
  ✅ [Check 1]: release-split → sc-release-split-protocol
  ✅ [Check 1]: review-translation → sc-review-translation-protocol
  ✅ [Check 1]: roadmap → sc-roadmap-protocol
  ✅ [Check 1]: swarm-wizard → sc-swarm-wizard-protocol
  ✅ [Check 1]: task → sc-task-protocol
  ✅ [Check 1]: tasklist → sc-tasklist-protocol
  ✅ [Check 1]: troubleshoot → sc-troubleshoot-protocol
  ✅ [Check 1]: validate-roadmap → sc-validate-roadmap-protocol
  ✅ [Check 1]: validate-tests → sc-validate-tests-protocol
  ✅ [Check 1]: workflow → sc-workflow-protocol
  ✅ [Check 2]: sc-adversarial-protocol ← adversarial.md
  ✅ [Check 2]: sc-auggie-review-protocol ← auggie-review.md
  ✅ [Check 2]: sc-brainstorm-protocol ← brainstorm.md
  ✅ [Check 2]: sc-cleanup-audit-protocol ← cleanup-audit.md
  ✅ [Check 2]: sc-cli-eval-protocol ← cli-eval.md
  ✅ [Check 2]: sc-cli-portify-protocol ← cli-portify.md
  ✅ [Check 2]: sc-graph-protocol ← graph.md
  ✅ [Check 2]: sc-impact-protocol ← impact.md
  ✅ [Check 2]: sc-implement-protocol ← implement.md
  ✅ [Check 2]: sc-init-lite-protocol ← init-lite.md
  ✅ [Check 2]: sc-issue-protocol ← issue.md
  ✅ [Check 2]: sc-pm-protocol ← pm.md
  ✅ [Check 2]: sc-post-release-protocol ← post-release.md
  ✅ [Check 2]: sc-pr-submit-protocol ← pr-submit.md
  ✅ [Check 2]: sc-reflect-protocol ← reflect.md
  ✅ [Check 2]: sc-release-split-protocol ← release-split.md
  ✅ [Check 2]: sc-review-translation-protocol ← review-translation.md
  ✅ [Check 2]: sc-roadmap-protocol ← roadmap.md
  ✅ [Check 2]: sc-swarm-wizard-protocol ← swarm-wizard.md
  ✅ [Check 2]: sc-task-protocol ← task.md
  ✅ [Check 2]: sc-tasklist-protocol ← tasklist.md
  ✅ [Check 2]: sc-troubleshoot-protocol ← troubleshoot.md
  ✅ [Check 2]: sc-validate-roadmap-protocol ← validate-roadmap.md
  ✅ [Check 2]: sc-validate-tests-protocol ← validate-tests.md
  ✅ [Check 2]: sc-workflow-protocol ← workflow.md

=== Check 3/4: Command Size Limits ===
  ⚠️  WARN [Check 3]: brainstorm.md (217 lines, warn threshold 200)
  ⚠️  WARN [Check 3]: reflect.md (305 lines, warn threshold 200)
  ⚠️  WARN [Check 3]: spawn.md (210 lines, warn threshold 200)
  ⚠️  WARN [Check 3]: spec-panel.md (462 lines, warn threshold 200)
  ⚠️  WARN [Check 3]: troubleshoot.md (215 lines, warn threshold 200)

=== Check 6: Activation Section Present (for paired commands) ===
  ✅ [Check 6]: adversarial.md has ## Activation
  ✅ [Check 6]: auggie-review.md has ## Activation
  ✅ [Check 6]: brainstorm.md has ## Activation
  ✅ [Check 6]: cleanup-audit.md has ## Activation
  ✅ [Check 6]: cli-eval.md has ## Activation
  ✅ [Check 6]: cli-portify.md has ## Activation
  ✅ [Check 6]: graph.md has ## Activation
  ✅ [Check 6]: impact.md has ## Activation
  ✅ [Check 6]: implement.md has ## Activation
  ✅ [Check 6]: init-lite.md has ## Activation
  ✅ [Check 6]: issue.md has ## Activation
  ✅ [Check 6]: pm.md has ## Activation
  ✅ [Check 6]: post-release.md has ## Activation
  ✅ [Check 6]: pr-submit.md has ## Activation
  ✅ [Check 6]: reflect.md has ## Activation
  ✅ [Check 6]: release-split.md has ## Activation
  ✅ [Check 6]: review-translation.md has ## Activation
  ✅ [Check 6]: roadmap.md has ## Activation
  ✅ [Check 6]: swarm-wizard.md has ## Activation
  ✅ [Check 6]: task.md has ## Activation
  ✅ [Check 6]: tasklist.md has ## Activation
  ✅ [Check 6]: troubleshoot.md has ## Activation
  ✅ [Check 6]: validate-roadmap.md has ## Activation
  ✅ [Check 6]: validate-tests.md has ## Activation
  ✅ [Check 6]: workflow.md has ## Activation

=== Check 8: Skill Frontmatter Completeness ===
  ✅ [Check 8]: sc-adversarial-protocol frontmatter complete
  ✅ [Check 8]: sc-auggie-review-protocol frontmatter complete
  ✅ [Check 8]: sc-brainstorm-protocol frontmatter complete
  ✅ [Check 8]: sc-cleanup-audit-protocol frontmatter complete
  ✅ [Check 8]: sc-cli-eval-protocol frontmatter complete
  ✅ [Check 8]: sc-cli-portify-protocol frontmatter complete
  ✅ [Check 8]: sc-graph-protocol frontmatter complete
  ✅ [Check 8]: sc-impact-protocol frontmatter complete
  ✅ [Check 8]: sc-implement-protocol frontmatter complete
  ✅ [Check 8]: sc-init-lite-protocol frontmatter complete
  ✅ [Check 8]: sc-issue-protocol frontmatter complete
  ✅ [Check 8]: sc-pm-protocol frontmatter complete
  ✅ [Check 8]: sc-post-release-protocol frontmatter complete
  ✅ [Check 8]: sc-pr-submit-protocol frontmatter complete
  ✅ [Check 8]: sc-reflect-protocol frontmatter complete
  ✅ [Check 8]: sc-release-split-protocol frontmatter complete
  ✅ [Check 8]: sc-review-translation-protocol frontmatter complete
  ✅ [Check 8]: sc-roadmap-protocol frontmatter complete
  ✅ [Check 8]: sc-swarm-wizard-protocol frontmatter complete
  ✅ [Check 8]: sc-task-protocol frontmatter complete
  ✅ [Check 8]: sc-tasklist-protocol frontmatter complete
  ✅ [Check 8]: sc-troubleshoot-protocol frontmatter complete
  ✅ [Check 8]: sc-validate-roadmap-protocol frontmatter complete
  ✅ [Check 8]: sc-validate-tests-protocol frontmatter complete
  ✅ [Check 8]: sc-workflow-protocol frontmatter complete

=== Check 9: Protocol Naming Consistency ===
  ✅ [Check 9]: sc:adversarial-protocol ends in -protocol
  ✅ [Check 9]: sc:auggie-review-protocol ends in -protocol
  ✅ [Check 9]: sc:brainstorm-protocol ends in -protocol
  ✅ [Check 9]: sc:cleanup-audit-protocol ends in -protocol
  ✅ [Check 9]: sc:cli-eval-protocol ends in -protocol
  ✅ [Check 9]: sc-cli-portify-protocol ends in -protocol
  ✅ [Check 9]: sc:graph-protocol ends in -protocol
  ✅ [Check 9]: sc:impact-protocol ends in -protocol
  ✅ [Check 9]: sc:implement-protocol ends in -protocol
  ✅ [Check 9]: sc:init-lite-protocol ends in -protocol
  ✅ [Check 9]: sc:issue-protocol ends in -protocol
  ✅ [Check 9]: sc:pm-protocol ends in -protocol
  ✅ [Check 9]: sc:post-release-protocol ends in -protocol
  ✅ [Check 9]: sc:pr-submit-protocol ends in -protocol
  ✅ [Check 9]: sc:reflect-protocol ends in -protocol
  ✅ [Check 9]: sc:release-split-protocol ends in -protocol
  ✅ [Check 9]: sc:review-translation-protocol ends in -protocol
  ✅ [Check 9]: sc:roadmap-protocol ends in -protocol
  ✅ [Check 9]: sc:swarm-wizard-protocol ends in -protocol
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
rc=0

NEW FILE .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/base-format.log (full contents, 22995 bytes):
unformatted: File would be reformatted
   --> src/superclaude/examples/release-spec-template.md:142:18
    |
141 | ```python
    - {{SC_PLACEHOLDER:data_model_code}}
142 + {{SC_PLACEHOLDER: data_model_code}}
143 | ```
    |

unformatted: File would be reformatted
  --> src/superclaude/skills/sc-cleanup-audit-protocol/rules/dynamic-use-checklist.md:25:49
   |
24 | ```python
   - module = importlib.import_module(os.environ.get('PLUGIN_MODULE'))
   - handler = __import__(os.getenv('HANDLER_CLASS'))
25 + module = importlib.import_module(os.environ.get("PLUGIN_MODULE"))
26 + handler = __import__(os.getenv("HANDLER_CLASS"))
27 | ```
--------------------------------------------------------------------------------
88 | ```python
   - for path in Path('handlers').glob('*.py'):
89 + for path in Path("handlers").glob("*.py"):
90 |     importlib.import_module(f"handlers.{path.stem}")
   |

unformatted: File would be reformatted
   --> src/superclaude/skills/sc-cli-portify-protocol/refs/code-templates.md:250:40
    |
249 | # Collected for iteration
    - ALL_GATES: dict[str, GateCriteria] = {{
    -     {GATE_DICT_ENTRIES}
    - }}
250 + ALL_GATES: dict[str, GateCriteria] = {{{GATE_DICT_ENTRIES}}}
251 | ```
    |

unformatted: File would be reformatted
   --> src/superclaude/skills/sc-cli-portify-protocol/refs/pipeline-spec.md:23:20
    |
22  | Step(
    -     id="step-id",              # kebab-case, unique within pipeline
    -     prompt=build_X_prompt(),   # Function from prompts.py
    -     output_file="artifact.md", # Relative to work_dir
    -     gate=STEP_GATE,            # From gates.py
23  +     id="step-id",  # kebab-case, unique within pipeline
24  +     prompt=build_X_prompt(),  # Function from prompts.py
25  +     output_file="artifact.md",  # Relative to work_dir
26  +     gate=STEP_GATE,  # From gates.py
27  |     gate_mode=GateMode.BLOCKING,  # BLOCKING (default) or TRAILING
    -     timeout_seconds=600,       # Per-step timeout
    -     inputs=["dep1.md"],        # Files this step reads
    -     retry_limit=1,             # How many retries on gate failure
    -     model=None,                # None = use default from config
28  +     timeout_seconds=600,  # Per-step timeout
29  +     inputs=["dep1.md"],  # Files this step reads
30  +     retry_limit=1,  # How many retries on gate failure
31  +     model=None,  # None = use default from config
32  | )
--------------------------------------------------------------------------------
55  |     [parallel_step_a, parallel_step_b],  # Run concurrently
    -     single_step_2,                        # Waits for parallel group
56  +     single_step_2,  # Waits for parallel group
57  | ]
--------------------------------------------------------------------------------
78  |     """Pipeline-specific configuration."""
79  +
80  |     # Required: identify the input
81  |     source_path: Path
82  |
83  |     # Optional: control behavior
    -     depth: str = "standard"       # quick|standard|deep
84  +     depth: str = "standard"  # quick|standard|deep
85  |
--------------------------------------------------------------------------------
104 |     PASS = "pass"
    -     PASS_NO_SIGNAL = "pass_no_signal"    # Completed but no structured report
    -     PASS_NO_REPORT = "pass_no_report"    # Output exists but no result file
    -     INCOMPLETE = "incomplete"             # Budget exhausted
    -     HALT = "halt"                         # Step recommends stopping
    -     TIMEOUT = "timeout"                   # Hard timeout exceeded
    -     ERROR = "error"                       # Process crash
    -     SKIPPED = "skipped"                   # Skipped by config
105 +     PASS_NO_SIGNAL = "pass_no_signal"  # Completed but no structured report
106 +     PASS_NO_REPORT = "pass_no_report"  # Output exists but no result file
107 +     INCOMPLETE = "incomplete"  # Budget exhausted
108 +     HALT = "halt"  # Step recommends stopping
109 +     TIMEOUT = "timeout"  # Hard timeout exceeded
110 +     ERROR = "error"  # Process crash
111 +     SKIPPED = "skipped"  # Skipped by config
112 | ```
--------------------------------------------------------------------------------
205 |
206 +
207 | def _has_required_sections(content: str) -> bool:
--------------------------------------------------------------------------------
424 | from superclaude.cli.my_pipeline import my_pipeline_group
425 +
426 | app.add_command(my_pipeline_group)
--------------------------------------------------------------------------------
457 |
458 +
459 | @dataclass
--------------------------------------------------------------------------------
464 |
465 +
466 | # In executor:
--------------------------------------------------------------------------------
529 |     for result in prior_results[-3:]:  # Keep recent, compress older
    -         context_block += result.to_context_summary(verbose=(result == prior_results[-1]))
530 +         context_block += result.to_context_summary(
531 +             verbose=(result == prior_results[-1])
532 +         )
533 |         context_block += "\n\n"
--------------------------------------------------------------------------------
550 |             return None
    -         remaining = [r.step.id for r in self.step_results
    -                      if r.status == MyStatus.PENDING]
551 +         remaining = [
552 +             r.step.id for r in self.step_results if r.status == MyStatus.PENDING
553 +         ]
554 |         return (
--------------------------------------------------------------------------------
562 |         """Estimate turns needed to complete remaining work."""
    -         remaining_steps = sum(1 for r in self.step_results
    -                               if r.status in (MyStatus.PENDING, MyStatus.INCOMPLETE))
563 +         remaining_steps = sum(
564 +             1
565 +             for r in self.step_results
566 +             if r.status in (MyStatus.PENDING, MyStatus.INCOMPLETE)
567 +         )
568 |         return remaining_steps * 25  # Default allocation per step
--------------------------------------------------------------------------------
584 |
585 +
586 | def run_programmatic_step(step, config) -> StepResult:
--------------------------------------------------------------------------------
591 |         PROGRAMMATIC_RUNNERS[step.id](config)
    -         return StepResult(step=step, status=StepStatus.PASS,
    -                          started_at=started, finished_at=time.time())
592 +         return StepResult(
593 +             step=step,
594 +             status=StepStatus.PASS,
595 +             started_at=started,
596 +             finished_at=time.time(),
597 +         )
598 |     except Exception as e:
    -         return StepResult(step=step, status=StepStatus.FAIL,
    -                          gate_failure_reason=str(e),
    -                          started_at=started, finished_at=time.time())
599 +         return StepResult(
600 +             step=step,
601 +             status=StepStatus.FAIL,
602 +             gate_failure_reason=str(e),
603 +             started_at=started,
604 +             finished_at=time.time(),
605 +         )
606 | ```
--------------------------------------------------------------------------------
624 |         return {
    -             "none": " ", "checking": "...",
    -             "pass": "ok", "fail_deferred": "!",
    -             "remediating": "~", "remediated": "ok",
625 +             "none": " ",
626 +             "checking": "...",
627 +             "pass": "ok",
628 +             "fail_deferred": "!",
629 +             "remediating": "~",
630 +             "remediated": "ok",
631 |             "halt": "X",
    |

unformatted: File would be reformatted
   --> src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:99:33
    |
98  | from superclaude.pr_submit import (
    -     actionable_finding_comments, classify, classify_codex, codex_finding_comments,
    -     finding_from_comment, remap_severity, reviewer_activity, route,
99  +     actionable_finding_comments,
100 +     classify,
101 +     classify_codex,
102 +     codex_finding_comments,
103 +     finding_from_comment,
104 +     remap_severity,
105 +     reviewer_activity,
106 +     route,
107 | )
--------------------------------------------------------------------------------
117 |     review_state = classify(
    -         payload, contract, watermark=watermark, current_head_sha=expected_head,
118 +         payload,
119 +         contract,
120 +         watermark=watermark,
121 +         current_head_sha=expected_head,
122 |     )
123 |     if review_state == "findings":
124 |         selected = actionable_finding_comments(
    -             payload, contract, watermark=watermark, current_head_sha=expected_head,
125 +             payload,
126 +             contract,
127 +             watermark=watermark,
128 +             current_head_sha=expected_head,
129 |         )
--------------------------------------------------------------------------------
148 |     codex_state = classify_codex(
    -         payload, contract, watermark=codex_watermark, current_head_sha=expected_head,
149 +         payload,
150 +         contract,
151 +         watermark=codex_watermark,
152 +         current_head_sha=expected_head,
153 |     )
154 |     if codex_state == "findings":
155 |         selected = codex_finding_comments(
    -             payload, contract, watermark=codex_watermark, current_head_sha=expected_head,
156 +             payload,
157 +             contract,
158 +             watermark=codex_watermark,
159 +             current_head_sha=expected_head,
160 |         )
161 |         try:
162 |             if not selected:
    -                 raise ValueError("Codex findings signal without actionable root details")
163 +                 raise ValueError(
164 +                     "Codex findings signal without actionable root details"
165 +                 )
166 |             codex_findings = [finding_from_comment(raw) for raw in selected]
    |

unformatted: File would be reformatted
   --> src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md:30:23
    |
29  | ```python
    - def citation_resolves(report_path: str, fixture_root: str = None) -> AssertionResult: ...
30  + def citation_resolves(
31  +     report_path: str, fixture_root: str = None
32  + ) -> AssertionResult: ...
33  | ```
--------------------------------------------------------------------------------
42  |
43  +
44  | def check_citation_resolves(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
49  |         rel_path, line_no = m.group(1), int(m.group(2))
    -         target = (fixture_root / rel_path) if not Path(rel_path).is_absolute() else Path(rel_path)
50  +         target = (
51  +             (fixture_root / rel_path)
52  +             if not Path(rel_path).is_absolute()
53  +             else Path(rel_path)
54  +         )
55  |         if not target.exists():
56  |             failed.append(f"{rel_path}:{line_no} (file missing)")
57  |             continue
58  |         lines = target.read_text(encoding="utf-8").splitlines()
    -         window = "\n".join(lines[max(0, line_no - 6):line_no + 5])
59  +         window = "\n".join(lines[max(0, line_no - 6) : line_no + 5])
60  |         # Optional snippet check: assertion may carry expected substring
--------------------------------------------------------------------------------
66  |     total = resolved + len(failed)
    -     return (len(failed) == 0, f"{resolved}/{total} citations resolved; failures={failed}")
67  +     return (
68  +         len(failed) == 0,
69  +         f"{resolved}/{total} citations resolved; failures={failed}",
70  +     )
71  | ```
--------------------------------------------------------------------------------
83  |
84  +
85  | def check_regex_present(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
90  |     if matches:
    -         return True, f"Pattern {assertion['pattern']!r} found {len(matches)} match(es) in {assertion['target']}"
91  +         return (
92  +             True,
93  +             f"Pattern {assertion['pattern']!r} found {len(matches)} match(es) in {assertion['target']}",
94  +         )
95  |     return False, f"Pattern {assertion['pattern']!r} NOT found in {assertion['target']}"
--------------------------------------------------------------------------------
108 |
109 +
110 | def check_regex_absent(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
115 |     if m is None:
    -         return True, f"Pattern {assertion['pattern']!r} correctly absent from {assertion['target']}"
    -     return False, f"Pattern {assertion['pattern']!r} unexpectedly present at offset {m.start()}: {m.group(0)[:80]!r}"
116 +         return (
117 +             True,
118 +             f"Pattern {assertion['pattern']!r} correctly absent from {assertion['target']}",
119 +         )
120 +     return (
121 +         False,
122 +         f"Pattern {assertion['pattern']!r} unexpectedly present at offset {m.start()}: {m.group(0)[:80]!r}",
123 +     )
124 | ```
--------------------------------------------------------------------------------
137 |
138 +
139 | def check_yaml_list_contains(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
149 |     if not isinstance(node, list):
    -         return False, f"field_path {assertion['field_path']!r} is not a list (got {type(node).__name__})"
150 +         return (
151 +             False,
152 +             f"field_path {assertion['field_path']!r} is not a list (got {type(node).__name__})",
153 +         )
154 |     expected = assertion["value"]
155 |     if expected in node:
    -         return True, f"List at {assertion['field_path']} contains {expected!r}; members={node}"
    -     return False, f"List at {assertion['field_path']} missing {expected!r}; members={node}"
156 +         return (
157 +             True,
158 +             f"List at {assertion['field_path']} contains {expected!r}; members={node}",
159 +         )
160 +     return (
161 +         False,
162 +         f"List at {assertion['field_path']} missing {expected!r}; members={node}",
163 +     )
164 | ```
--------------------------------------------------------------------------------
191 |     except (TypeError, ValueError):
    -         return False, f"count field {count_field!r} not an integer: {data.get(count_field)!r}"
192 +         return (
193 +             False,
194 +             f"count field {count_field!r} not an integer: {data.get(count_field)!r}",
195 +         )
196 |     actual = len(items)
--------------------------------------------------------------------------------
220 | ```python
    - def matrix_covers_items(matrix: str, source: str, threshold: float) -> AssertionResult: ...
221 + def matrix_covers_items(
222 +     matrix: str, source: str, threshold: float
223 + ) -> AssertionResult: ...
224 | ```
--------------------------------------------------------------------------------
230 |
231 +
232 | def check_matrix_covers_items(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
238 |     source_items = {item["id"] for item in source.get("items", [])}
    -     covered = {row["item_id"] for row in matrix if row.get("status") and row["status"] != "uncovered"}
239 +     covered = {
240 +         row["item_id"]
241 +         for row in matrix
242 +         if row.get("status") and row["status"] != "uncovered"
243 +     }
244 |     if not source_items:
245 |         return False, "Source fixture has no items to cover"
246 |     ratio = len(covered & source_items) / len(source_items)
247 |     if ratio >= threshold:
    -         return True, f"Coverage {ratio:.2%} >= {threshold:.2%} ({len(covered & source_items)}/{len(source_items)} items)"
    -     return False, f"Coverage {ratio:.2%} < {threshold:.2%}; missing={sorted(source_items - covered)}"
248 +         return (
249 +             True,
250 +             f"Coverage {ratio:.2%} >= {threshold:.2%} ({len(covered & source_items)}/{len(source_items)} items)",
251 +         )
252 +     return (
253 +         False,
254 +         f"Coverage {ratio:.2%} < {threshold:.2%}; missing={sorted(source_items - covered)}",
255 +     )
256 | ```
--------------------------------------------------------------------------------
268 |
269 +
270 | def check_checkpoint_logged(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
292 | ```python
    - def deviation_class_matches(report: str, annotated_fixture: str, diff_hunk_id: str) -> AssertionResult: ...
293 + def deviation_class_matches(
294 +     report: str, annotated_fixture: str, diff_hunk_id: str
295 + ) -> AssertionResult: ...
296 | ```
--------------------------------------------------------------------------------
302 |
303 +
304 | def check_deviation_class_matches(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    -     fixture = yaml.safe_load((base_dir / assertion["annotated_fixture"]).read_text(encoding="utf-8")) or {}
    -     report = yaml.safe_load((base_dir / assertion["report"]).read_text(encoding="utf-8")) or {}
305 +     fixture = (
306 +         yaml.safe_load(
307 +             (base_dir / assertion["annotated_fixture"]).read_text(encoding="utf-8")
308 +         )
309 +         or {}
310 +     )
311 +     report = (
312 +         yaml.safe_load((base_dir / assertion["report"]).read_text(encoding="utf-8"))
313 +         or {}
314 +     )
315 |     hunk_id = assertion["diff_hunk_id"]
    -     expected = next((h["deviation_class"] for h in fixture.get("hunks", []) if h["id"] == hunk_id), None)
    -     actual = next((e["deviation_class"] for e in report.get("deviation_register", []) if e.get("hunk_id") == hunk_id), None)
316 +     expected = next(
317 +         (h["deviation_class"] for h in fixture.get("hunks", []) if h["id"] == hunk_id),
318 +         None,
319 +     )
320 +     actual = next(
321 +         (
322 +             e["deviation_class"]
323 +             for e in report.get("deviation_register", [])
324 +             if e.get("hunk_id") == hunk_id
325 +         ),
326 +         None,
327 +     )
328 |     if expected is None:
--------------------------------------------------------------------------------
345 |
346 +
347 | def check_path_exists(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
367 |
368 +
369 | def check_path_does_not_exist(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
396 |
    - def check_falsifier_skeleton_present(assertion: dict, base_dir: Path) -> tuple[bool, str]:
397 +
398 + def check_falsifier_skeleton_present(
399 +     assertion: dict, base_dir: Path
400 + ) -> tuple[bool, str]:
401 |     case = base_dir / assertion["case_yaml"]
--------------------------------------------------------------------------------
409 |     if status == "skeleton-pending-iteration-3-fixture":
    -         return True, f"skeleton present (pending iteration-3 fixture); id={data.get('id')!r}"
410 +         return (
411 +             True,
412 +             f"skeleton present (pending iteration-3 fixture); id={data.get('id')!r}",
413 +         )
414 |     if status == "active":
--------------------------------------------------------------------------------
422 |         return True, f"active falsifier with canonical fields; id={data.get('id')!r}"
    -     return False, f"unexpected status {status!r}; expected 'skeleton-pending-iteration-3-fixture' or 'active'"
423 +     return (
424 +         False,
425 +         f"unexpected status {status!r}; expected 'skeleton-pending-iteration-3-fixture' or 'active'",
426 +     )
427 | ```
    |

unformatted: File would be reformatted
  --> src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md:41:31
   |
40 |     prompt=build_debate_prompt(diff_file, roadmap_a, roadmap_b, config.depth),
   -     output_file=debate_file,                  # out / "debate-transcript.md"
41 +     output_file=debate_file,  # out / "debate-transcript.md"
42 |     gate=DEBATE_GATE,
   |

unformatted: File would be reformatted
  --> src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md:25:47
   |
24 | if config.input_type == "tdd":
   -     extract_prompt = build_extract_prompt_tdd(..., tool_write=config.tool_write_extract_tdd)
25 +     extract_prompt = build_extract_prompt_tdd(
26 +         ..., tool_write=config.tool_write_extract_tdd
27 +     )
28 | else:
   |

unformatted: File would be reformatted
   --> src/superclaude/skills/sc-validate-tests-protocol/SKILL.md:254:20
    |
253 |     # Boost for compound phrases
    -     if context.get('compound_phrase_matched'):
254 +     if context.get("compound_phrase_matched"):
255 |         base_confidence = min(0.95, base_confidence + 0.15)
256 |
257 |     # Reduce for vague input
    -     if context.get('vague_input') or context.get('no_keywords'):
258 +     if context.get("vague_input") or context.get("no_keywords"):
259 |         base_confidence *= 0.7
    |

unformatted: File would be reformatted
   --> src/superclaude/templates/documents/release-spec-template.md:140:18
    |
139 | ```python
    - {{SC_PLACEHOLDER:data_model_code}}
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

12 files would be reformatted, 1757 files already formatted
rc=1

NEW FILE .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/base-full-suite.log (86613 bytes, too large to inline; read it at .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/base-full-suite.log)
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
