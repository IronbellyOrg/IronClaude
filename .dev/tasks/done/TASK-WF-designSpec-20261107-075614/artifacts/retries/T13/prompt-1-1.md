28a5b46514d9cf2b448aa3ceb519553702a2787d
Review one task for spec compliance.

Task brief: ## Task 13: Document the flag in the user guides, sync, and run the final checks

Depends on: Task 2
Depends on: Task 10
Depends on: Task 11
Depends on: Task 12

Edit `docs/user-guide/commands.md`: add `[--merge-guard {draft,off}]` to the `/sc:pr-submit` usage line and a paragraph after the "Merge conflicts" paragraph describing the guard, its default, the `held` state, the clear command `gh pr ready <N> --repo <REPO>` and that draft behaviour is unverified until the owner runs the disposable-PR gate. Edit `docs/user-guide/flags.md`: add a `--merge-guard` row beside the `--conflict-max-tier` row with values `draft` (default) and `off`. Then run `make sync-dev`, `make verify-sync`, `make lint`, `uv run ruff format --check src/ tests/`, the full suite `uv run pytest -q tests`, and `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q`, and write the outputs, the full-suite pass count and every failing test id (compared with the base-commit record of Task 1) to `./artifacts/final-checks.md`.

Acceptance criteria:
- T13.AC1: `grep -n "merge-guard" docs/user-guide/commands.md docs/user-guide/flags.md` shows the usage entry, the paragraph and the flags row; the paragraph names the clear command and the unverified-until-release-gate statement.
- T13.AC2: `make verify-sync` exits 0, the full suite `uv run pytest -q tests` shows no failing test id that is absent from the base-commit record of Task 1, and `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q` passes; `make lint` and `uv run ruff format --check src/ tests/` exit 0, or every remaining failure is listed in `./artifacts/final-checks.md` as present in the base-commit record of Task 1.
- T13.AC3: `git status --short` lists changes only under `src/superclaude/`, `tests/`, `docs/user-guide/`, `.dev/` and gitignored `.claude/` mirrors; no `.claude/` path other than `.claude/settings.json` is staged, and `.dev/tasks` is staged with `git add .dev/tasks`.
Global constraints: - Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
Start sha: 28a5b46514d9cf2b448aa3ceb519553702a2787d
Diff against the start snapshot: diff --git a/docs/user-guide/commands.md b/docs/user-guide/commands.md
index ccd97311..eec2bcee 100644
--- a/docs/user-guide/commands.md
+++ b/docs/user-guide/commands.md
@@ -487,7 +487,7 @@ PM Agent:
 **Syntax:**
 
 ```
-/sc:pr-submit [--monitor {0,1,2,3}] [--max-rounds N≤5] [--poll-interval ≥30] [--timeout 600] [--silence-timeout 300] [--base <branch>] [--head <branch>] [--title ...] [--body ...] [--pr <N>] [--conflict-max-tier {0,1,2}] [--output-dir <dir>] [--resume <run-log.jsonl>]
+/sc:pr-submit [--monitor {0,1,2,3}] [--max-rounds N≤5] [--poll-interval ≥30] [--timeout 600] [--silence-timeout 300] [--base <branch>] [--head <branch>] [--title ...] [--body ...] [--pr <N>] [--conflict-max-tier {0,1,2}] [--merge-guard {draft,off}] [--output-dir <dir>] [--resume <run-log.jsonl>]
 ```
 
 **Merge conflicts:** `--monitor` defaults to `3`, but `--conflict-max-tier` defaults to `0` (detect and report only). These are independent ceilings: raising the conflict cap does not grant more monitor authority. Monitor 0 skips conflict handling; monitor 1 and above detect conflicts before the first review and report a per-file plan before editing. A branch that is merely behind the base is reported, not automatically rebased.
@@ -500,6 +500,8 @@ PM Agent:
 
 Tier 3 conflicts need human resolution: for example protected/migration paths, binary files, symlinks, mode changes, unsupported lock/generated files or unclear intent. They are reported at monitor 1 or 2 and halt at monitor 3. There is at most one conflict cycle per run; late text conflicts halt rather than triggering continuous repair. A Tier 1 sync push uses no review round and sends no reviewer re-trigger, reply or thread resolution; it does not clear a non-clean review outcome. After a merge push, CI follows the new head: expected-but-missing checks keep polling and may time out as `ci_not_started`; unresolved conflicts skip CI as `pr_conflicting`.
 
+**Merge guard:** `--merge-guard` defaults to `draft` and acts only at monitor `3`. When a verified finding of Medium severity or higher is routed to a fix, the PR becomes a draft before any edit, so nobody merges it while the fix exists only locally; it becomes ready again only after the fix push is confirmed on the PR head, before the replies and the re-review request. A PR that was already a draft is never made ready by the run. If the run ends with unpublished or uncertain work, or cannot read the PR's draft and ready history, the PR stays a draft and the output reports `merge_guard: held` with the reason and the clear command, `gh pr ready <N> --repo <REPO>`, which marks it ready by hand. `--merge-guard off` leaves the PR untouched and prints "Remediation is unprotected: --merge-guard off." once. Drafts and ready transitions can change which reviews and workflows run; this behaviour is unverified until the owner runs the disposable-PR gate, so treat the guard as untested until then.
+
 **Examples (run in Claude Code, not a shell):**
 
 ```text

diff --git a/docs/user-guide/flags.md b/docs/user-guide/flags.md
index 5e6f5875..86349a5d 100644
--- a/docs/user-guide/flags.md
+++ b/docs/user-guide/flags.md
@@ -209,6 +209,7 @@ Since 5.0.0 `FLAGS.md` and `MODES.md` are no longer shipped, and old copies left
 | `--resume` | Rebuild state from a run log | Path to `monitor-run-<N>.jsonl` |
 | `--max-rounds` | Remediation cycles | Number (default `2`, hard cap `5`) |
 | `--conflict-max-tier` | Highest merge-conflict tier permitted, subject to the monitor ceiling | `0` (default: detect and report only), `1` (also root `uv.lock` regeneration, opt-in), `2` (also initial intent-based text/tree resolution at monitor `3`) |
+| `--merge-guard` | Hold the PR as a draft while a fix cycle runs, at monitor `3` only | `draft` (default), `off` |
 | `--head` / `--base` / `--title` / `--body` | PR details | Branch names, text |
 
 The monitor ceiling and conflict cap are independent: monitor defaults to `3`, conflict cap to `0`. Raising the cap does not authorize Tier 3 resolution or bypass monitor limits; monitor `0` skips conflict handling entirely. Eligible Tier 1 cases at monitor `1` propose, at `2` leave a validated uncommitted merge, and at `3` may push. Tier 2 requires monitor `3`, cap `2`, at least two remaining rounds and at most eight text-conflict files, and runs only before the first review. Thus `--max-rounds 1` cannot fund Tier 2 resolution. Only one conflict cycle is allowed per run; late text conflicts halt.

NEW FILE .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/final-checks.md (full contents, 2482 bytes):
# Final checks (Task 13)

Run on 2026-11-07T13:16Z in the worktree for issue 375, after `make sync-dev`. Base-commit record: `./artifacts/base-full-suite.log`, `./artifacts/base-lint.log`, `./artifacts/base-format.log` (Task 1).

## Results

| Command | Result |
|---|---|
| `make sync-dev` then `make verify-sync` | exit 0, "All components in sync." |
| `make lint` | exit 0, "All checks passed!" |
| `uv run ruff format --check src/ tests/` | exit 1, 12 files would be reformatted, 1763 already formatted; the 12 files are the same list as the base record (compared by file path; base: 12 reformatted, 1757 formatted) |
| `uv run pytest -q tests` | 2 failed, 17199 passed, 137 skipped, 2 xpassed (full output: `./artifacts/t13-full-suite.log`) |
| `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q` | 103 passed |

## Failing test ids against the base-commit record

Full suite failures this run:

- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval`
- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module`

Base-commit record after `make sync-dev` (3 failed, 16955 passed):

- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval`
- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module`
- `tests/unit/test_ccsession_tiers.py::test_a_busy_shim_is_never_stopped_by_a_new_launch`

Every failing id of this run is in the base record. The third base failure (`test_a_busy_shim_is_never_stopped_by_a_new_launch`) passed this run; it is a timing-dependent ccsession shim test and was not touched. No failing id is absent from the base record.

The 12 files that `ruff format --check` reports are Markdown files with Python code fences (for example `src/superclaude/examples/release-spec-template.md` and `tests/roadmap/fixtures/...`); the list, compared by file path, is identical to the base record, and this plan edited only one of them, `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`: its diagnostic is in the existing python fence (same position as in the base record), and the lines this plan added contain no python fence.

## Working tree

`git status --short` lists changes only under `src/superclaude/`, `tests/`, `docs/user-guide/` and `.dev/`; `git diff --cached --name-only` lists no `.claude/` path; `.dev/tasks` is staged with `git add .dev/tasks`.

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
