559d390ad5b61e5ceb7eab419efc5695a215a785
Review one task for spec compliance.

Task brief: ## Task 12: Sync the dev copies, run the checks and write the owner's manual check

Depends on: Task 8, Task 10, Task 11

Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source in `src/superclaude/`, never by editing `.claude/`. Then write `./artifacts/owner-manual-check.md` in this package. It states, in plain bullets, the single manual check the owner runs after merge because no step of this plan wrote to GitHub: file one test issue with `/sc:issue --create "<short test description>" --mode feature --type tests --depth standard` on `IronbellyOrg/IronClaude`, confirm the issue shows type Test and Complexity Medium, and check that the final output lists any `not set` line; repeat once with `--mode bug` and confirm type Bug. It also records the three UNVERIFIED points from the source section 3.4 (POST body, `--type` flag, silent drop without push access) and the four defaults the owner may reverse (the `orgs/` read exception, keeping the `--type` flag, keeping the mode labels, area `tests` giving Test).

Acceptance criteria:
- `make verify-sync` and `make lint` exit 0 and the whole `tests/skills/test_issue_protocol.py` file passes; the outputs are saved to `./artifacts/t12-checks.log`.
- `git status --short` shows no path under `.claude/` other than `.claude/settings.json` in the set of staged or tracked changes.
- `./artifacts/owner-manual-check.md` exists and holds the two test-issue checks, the three UNVERIFIED points and the four reversible defaults.

AC ids:
T12.AC1: `make verify-sync` and `make lint` exit 0 and the whole `tests/skills/test_issue_protocol.py` file passes; the outputs are saved to `./artifacts/t12-checks.log`.
T12.AC2: `git status --short` shows no path under `.claude/` other than `.claude/settings.json` in the set of staged or tracked changes.
T12.AC3: `./artifacts/owner-manual-check.md` exists and holds the two test-issue checks, the three UNVERIFIED points and the four reversible defaults.
Global constraints: - Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits.
- Text inside the skill, command and agent files must not contain the string `src/superclaude/` (an installed-path rule; a test scans the skill folder for it).
- Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`. No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`.
- `--claim` behaviour and text stay unchanged, including its two-block part of the return contract. The T1 and T2 worker files, `refs/tiers.md`, `scripts/*.py` and the four issue-body templates stay unchanged.
- The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST).
- Nothing in this plan writes to GitHub while it is executed. The POST body, the `--type` flag and the silent-drop behaviour come from GitHub's docs and `gh` help and are UNVERIFIED by a real run; Task 12 leaves the owner a manual check for that.
- Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit.
- Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly `orgs/<owner of R>/issue-fields`; the `--type` area flag and its 11 values stay but no longer produce a label; the `bug` / `enhancement` mode labels stay.
Start sha: 559d390ad5b61e5ceb7eab419efc5695a215a785
Diff against the start snapshot: 
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261108-041415/artifacts/owner-manual-check.md b/.dev/tasks/to-do/TASK-WF-design-20261108-041415/artifacts/owner-manual-check.md
new file mode 100644
index 00000000..e083cddb
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261108-041415/artifacts/owner-manual-check.md
@@ -0,0 +1,26 @@
+# Owner manual check for issue 438
+
+No step of this plan wrote to GitHub. Everything below needs a real run by the owner, after the change is merged.
+
+## Checks to run
+
+- Feature check: run `/sc:issue --create "<short test description>" --mode feature --type tests --depth standard` on `IronbellyOrg/IronClaude`. Confirm the new issue shows the issue type Test and the Complexity field Medium, carries the `enhancement` label, and that the final output lists a `not set` line for anything that did not apply.
+- Bug check: run `/sc:issue --create "<short test description>" --mode bug --depth quick` on the same repo. Confirm the issue type is Bug, the Complexity field is Simple, the `bug` label is present, and any `not set` line is listed in the final output.
+- Close both test issues afterwards.
+
+## UNVERIFIED points (from the design, section 3.4)
+
+- The POST body for the Complexity field (`{"issue_field_values":[{"field_id":<id>,"value":"<option name>"}]}`) comes from GitHub's documentation, not from a run. GitHub's example sends the header `X-GitHub-Api-Version: 2026-03-10`; the skill does not send it, so a 404 would show up as `not set: field Complexity ...: write failed`.
+- The `--type` flag of `gh issue create` comes from `gh` help (gh 2.103.3), not from a run.
+- GitHub drops the issue type silently when the caller has no push access. The skill detects this by reading the type back, and that read-back has not been exercised against a real issue.
+
+## Defaults the owner may reverse
+
+- The T3 lookup worker may read exactly one `orgs/` path (`orgs/<owner of R>/issue-fields`) to find the Complexity field id. Reversing it means giving the field id another way.
+- The `--type` flag and its 11 area values are kept, but they no longer produce a label; the area only decides issue type Test for a feature in `tests`.
+- The `bug` and `enhancement` mode labels are kept alongside the issue type.
+- Area `tests` on a feature gives issue type Test; every other feature gives Feature, and mode bug always gives Bug.
+
+## Known follow-up found while implementing
+
+- `tests/skills/test_worker_contract.py` fails 2 tests (`test_every_write_verb_hit_is_classified`, `test_classification_table_has_no_stale_entries`). That file keeps the exact text of every `gh api` line in the skills, commands and agents, and Tasks 2, 3 and 5 rewrote four of those lines and added new ones. The plan did not include this file, so it was not changed. The fix is to update the classification table in that file from the new line text (GET lookups read-only, the POST lines never-worker); the log is `./artifacts/t12-extra-suite.log`.
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261108-041415/artifacts/t12-checks.log b/.dev/tasks/to-do/TASK-WF-design-20261108-041415/artifacts/t12-checks.log
new file mode 100644
index 00000000..7cc15eac
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261108-041415/artifacts/t12-checks.log
@@ -0,0 +1,49 @@
+== make sync-dev
+🔄 Syncing src/superclaude/ → .claude/ for local development...
+✅ Sync complete.
+   Skills:    39 directories
+   Agents:    48 files
+   Commands:  46 files
+   Hooks:     15 files
+   Templates: 52 files
+sync-dev rc=0
+== make verify-sync
+  ✅ modularization-template-review/qa-qualitative-sufficiency_report_template.md
+  ✅ modularization-template-review/analyst-cross-validation_report_template.md
+  ✅ modularization-template-review/qa-acceptance-methodology-audit_template.md
+  ✅ modularization-template-review/pipeline-complete_report_template.md
+  ✅ modularization-template-review/qa-source-fidelity_template.md
+  ✅ modularization-template-review/qa-research-depth_report_template.md
+  ✅ modularization-template-review/web-research_template.md
+
+=== Installer Registration ===
+  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js
+
+=== Hooks Cross-Consistency ===
+  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes
+
+✅ All components in sync.
+verify-sync rc=0
+== make lint
+
+=== Check 11: Contract Constant Anti-Duplication (Contract #5 + #8) ===
+  ✅ [Check 11]: no contract-constant duplications
+
+=== Checks 5/7: NEEDS DESIGN (skipped) ===
+  ℹ️  Check 5 (inline protocol detection) — pending design
+  ℹ️  Check 7 (activation references correct skill) — pending design
+
+=== Summary ===
+  Errors:   0
+  Warnings: 5
+  ✅ PASS — architecture policy compliant (5 warning(s))
+Running linter...
+uv run ruff check .
+All checks passed!
+lint rc=0
+== uv run pytest tests/skills/test_issue_protocol.py -v (summary)
+tests/skills/test_issue_protocol.py::test_skill_md_states_the_create_rules_of_the_issue_type_and_field PASSED [ 99%]
+tests/skills/test_issue_protocol.py::test_command_and_skill_agree_on_the_new_create_boundaries PASSED [100%]
+
+============================= 114 passed in 0.18s ==============================
+protocol-tests rc=0

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
