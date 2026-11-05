16d793956baff16afa0dbf4a1b257c4b240d8092
Review one task for spec compliance.

Task brief: ## Task 8: Update the permission sentence in the two v5.0.0 testing guides

Depends on: Task 5

Source requirement: docs that state the permission default must stay true. Two guides say `ccsession` starts Claude Code with `--dangerously-skip-permissions --allowedTools=Grep` "unless `CC_CLAUDE_FLAGS` is set (`ccsession:78-83,93`)": `docs/testing/v5.0.0/user/D08-ccsession.md` (line 23, which continues "Claude Code then runs tools without asking") and `docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md` (line 21, without that trailing clause).

- In each file, change only that one line: add that `CCSESSION_PERMISSIONS=default` is the other way out (then only `--allowedTools=Grep` is added), replace the stale citation `ccsession:78-83,93` with the line numbers of the permissions paragraph and of the flag-default block as they are after Task 5 (find them with `grep -n` in `src/superclaude/skills/ccsession-tag/ccsession`; do not copy numbers from this plan), and in D08 tie the trailing clause to the default launch ("by default Claude Code then runs tools without asking"). Do not add test steps and do not change the other `CC_CLAUDE_FLAGS` lines of D08 (lines 199 and 210); line 210 keeps its old `ccsession:78-83,93` citation on purpose, to keep the diff to the one sentence.

Acceptance criteria:
- Both sentences mention `CCSESSION_PERMISSIONS=default` and cite line numbers that `grep -n` on the changed `ccsession` shows hold the permissions paragraph and the flag-default block; the D08 sentence no longer claims Claude Code runs tools without asking in every case.
- `git diff --stat` for these two files shows one changed line each.

AC ids (in source order):
T8.AC1: Both sentences mention `CCSESSION_PERMISSIONS=default` and cite line numbers that `grep -n` on the changed `ccsession` shows hold the permissions paragraph and the flag-default block; the D08 sentence no longer claims Claude Code runs tools without asking in every case.
T8.AC2: `git diff --stat` for these two files shows one changed line each.
Global constraints: ## Constraints

- Design is fixed by the user: option B, a new explicit opt-in variable. Do not implement the issue's other option (dropping the flags automatically on scripted launches) and do not touch `src/superclaude/cli/reflect/runner.py` or `src/superclaude/cli/pipeline/process.py`; callers such as the Coder `claude` wrapper opt in themselves.
- Do not change how an empty `CC_CLAUDE_FLAGS` is handled: the `:-` default expansion stays, so an empty or unset value still takes the default flags. A non-empty `CC_CLAUDE_FLAGS` still replaces the default completely, including when `CCSESSION_PERMISSIONS=default` is set.
- Decisions accepted by the user: with `CCSESSION_PERMISSIONS=default` the default flags become `--allowedTools=Grep` only (that flag is not a permission bypass, and dropping it would remove the Grep and Glob tools on Linux and macOS; see the comment above `CC_CLAUDE_FLAGS` in `src/superclaude/skills/ccsession-tag/ccsession`); any value other than empty or `default` (including `Default` and `bypass`) stops `ccsession` with exit status 2 and a message on standard error, so a typo can never fall back to the bypass.
- The exit-2 check applies to every `ccsession` invocation, `--help`, `--list` and the hook and installer helper calls included, because it runs at the flag-default line (line 124 before this plan) ahead of the argument dispatch. The docs state this and a test pins it. The check stays at that spot: do not move the `case` below the env-file sourcing (a later launch-scoping change must keep computing the flags at that spot and defer only the `exit 2`), or an env-file value would start choosing the flags and an env-file `CC_CLAUDE_FLAGS=""` would take the default.
- The variable is read from the shell environment at that spot, before `~/.claude/ccsession.env` is sourced, so it cannot be set from that file; the docs say so and a test pins it. The variable stays exported to nested launches (a nested `ccsession` or Claude Code started from inside the session inherits the non-bypass choice); the docs say so and a test pins it.
- `show_help` in `src/superclaude/skills/ccsession-tag/ccsession` (line 1652 before this plan) prints the header only up to the first line that starts with `# The wrapper always runs`. Do not change the first words of that line and do not edit `show_help`; new `--help` text goes above that line.
- Edit only `src/superclaude/` sources, tests, docs and `CHANGELOG.md`. The `.claude/` copies are gitignored sync output and are never staged.
- Delivery note, not a code task: the pull request that ships this plan must say in its description that it unblocks Coder PR 458 and link issue 390; `/sc:pr-submit` writes that description after the plan is approved and executed.
Start sha: 16d793956baff16afa0dbf4a1b257c4b240d8092
Diff against the start snapshot: 
diff --git a/docs/testing/v5.0.0/user/D08-ccsession.md b/docs/testing/v5.0.0/user/D08-ccsession.md
index 364df4fb..2175250f 100644
--- a/docs/testing/v5.0.0/user/D08-ccsession.md
+++ b/docs/testing/v5.0.0/user/D08-ccsession.md
@@ -20,7 +20,7 @@
   - The throwaway `HOME` registers only the three ccsession hooks, so the other SuperClaude hooks, which write `~/.claude/state/` and `~/.claude/logs/`, do not run in Tier C (`src/superclaude/hooks/hooks.json:18,33-42,49,54-73`).
 - **Two warnings.**
   - Never run `pkill -f local-gateway-alias-proxy.py` during this test. One shim serves every ccsession session of yours with the same settings, so that command cuts the replies of every session you have open (`ccsession:798`; `CHANGELOG.md:22`). This guide stops only its own test shims, by their `/tmp/d08/home/...` path.
-  - `ccsession` starts Claude Code with `--dangerously-skip-permissions --allowedTools=Grep` unless `CC_CLAUDE_FLAGS` is set (`ccsession:78-83,93`): Claude Code then runs tools without asking. In Tier C, type only the prompts this guide gives.
+  - `ccsession` starts Claude Code with `--dangerously-skip-permissions --allowedTools=Grep` unless `CC_CLAUDE_FLAGS` is set or `CCSESSION_PERMISSIONS=default` is exported (then only `--allowedTools=Grep` is added) (`ccsession:119-125,135-140`): by default Claude Code then runs tools without asking. In Tier C, type only the prompts this guide gives.
 - Known issue, not part of this guide: the ccsession shim tests in `tests/unit/test_ccsession_tiers.py` can fail when the machine is busy (issue [#352](https://github.com/IronbellyOrg/IronClaude/issues/352), open). If you also run the unit tests from a checkout, rerun a failing shim test before you report it.
 
 ## What you're verifying

diff --git a/docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md b/docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md
index 5c8f0283..0b1cc43a 100644
--- a/docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md
+++ b/docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md
@@ -18,7 +18,7 @@
   - Tier A only reads. Tier B writes only under `/tmp/e01`, with a throwaway `HOME` and cache (`/tmp/e01/home`, `/tmp/e01/cache`), `CLAUDE_BIN=/bin/false` and `CCSESSION_MODELS_REFRESH=0`: it never starts Claude Code, never starts a gateway shim and never fetches the model data. Every Tier B launch is one the policy refuses, which ends before the shim and the session folder (`ccsession:1483-1489`; the launch stops at `ccsession:948,954,956`).
   - Tier C copies your real env file into `/tmp/e01/live.sh` (it may hold gateway settings; `/tmp/e01` is made readable only by you, and Cleanup removes it), and runs one Claude Code session with a second throwaway `HOME` (`/tmp/e01/c-home`). That `HOME` has no `settings.json`, so no SuperClaude hooks run: the hooks that write `~/.claude/state/` and `~/.claude/logs/` (`src/superclaude/hooks/hooks.json:18,49,104`) never touch your real `~/.claude`.
   - Never run `pkill -f local-gateway-alias-proxy.py`: one shim serves every ccsession session of yours with the same settings, so that command cuts all of them (`ccsession:766-768`). Cleanup stops only this guide's shim, by its `/tmp/e01/` path.
-  - `ccsession` starts Claude Code with `--dangerously-skip-permissions --allowedTools=Grep` unless `CC_CLAUDE_FLAGS` is set (`ccsession:78-83,93`). In Tier C, type only the prompts this guide gives.
+  - `ccsession` starts Claude Code with `--dangerously-skip-permissions --allowedTools=Grep` unless `CC_CLAUDE_FLAGS` is set or `CCSESSION_PERMISSIONS=default` is exported (then only `--allowedTools=Grep` is added) (`ccsession:119-125,135-140`). In Tier C, type only the prompts this guide gives.
 
 ## What you're verifying
 

Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (none)

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
