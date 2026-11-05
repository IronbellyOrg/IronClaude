b5d0068933eded0e9a9ec2821380406c3fe00bb8
Review one task for spec compliance.

Task brief: ## Task 6: Add CCSESSION_PERMISSIONS to the settings table in src/superclaude/skills/ccsession-tag/README.md

Depends on: Task 5

Source requirement: document the variable beside the other variables. The settings table (header `| Setting | Effect |`, rows such as `CCSESSION_SHOW_ALL_MODELS=1` and `CCSESSION_COOLDOWN_SECONDS`, around lines 498 to 515) is where the README lists ccsession's variables.

- Add a row `CCSESSION_PERMISSIONS=default` with the effect: start Claude without `--dangerously-skip-permissions` (only `--allowedTools=Grep` stays, so Grep and Glob remain available); shim and tier-model routing are unchanged; read from the shell environment, not `~/.claude/ccsession.env`; stays exported to nested launches; any other non-empty value exits 2 on every `ccsession` call, `--help` included; a non-empty `CC_CLAUDE_FLAGS` (from the shell or the env file) still wins; flags the caller passes (such as Orca's default `--dangerously-skip-permissions` option) still apply; under a bad value `ccsession-orca` also prints its "not a valid session name; ignoring it" warning before the exit. Add a second row `CC_CLAUDE_FLAGS` only if the table has none, stating it replaces the default flags and that an empty value takes the default.

Acceptance criteria:
- The README table contains a `CCSESSION_PERMISSIONS=default` row with all the points above and renders as a valid Markdown table (same column count on every row).
- `grep -n CCSESSION_PERMISSIONS src/superclaude/skills/ccsession-tag/README.md` shows the row.

AC ids (in source order):
T6.AC1: The README table contains a `CCSESSION_PERMISSIONS=default` row with all the points above and renders as a valid Markdown table (same column count on every row).
T6.AC2: `grep -n CCSESSION_PERMISSIONS src/superclaude/skills/ccsession-tag/README.md` shows the row.
Global constraints: ## Constraints

- Design is fixed by the user: option B, a new explicit opt-in variable. Do not implement the issue's other option (dropping the flags automatically on scripted launches) and do not touch `src/superclaude/cli/reflect/runner.py` or `src/superclaude/cli/pipeline/process.py`; callers such as the Coder `claude` wrapper opt in themselves.
- Do not change how an empty `CC_CLAUDE_FLAGS` is handled: the `:-` default expansion stays, so an empty or unset value still takes the default flags. A non-empty `CC_CLAUDE_FLAGS` still replaces the default completely, including when `CCSESSION_PERMISSIONS=default` is set.
- Decisions accepted by the user: with `CCSESSION_PERMISSIONS=default` the default flags become `--allowedTools=Grep` only (that flag is not a permission bypass, and dropping it would remove the Grep and Glob tools on Linux and macOS; see the comment above `CC_CLAUDE_FLAGS` in `src/superclaude/skills/ccsession-tag/ccsession`); any value other than empty or `default` (including `Default` and `bypass`) stops `ccsession` with exit status 2 and a message on standard error, so a typo can never fall back to the bypass.
- The exit-2 check applies to every `ccsession` invocation, `--help`, `--list` and the hook and installer helper calls included, because it runs at the flag-default line (line 124 before this plan) ahead of the argument dispatch. The docs state this and a test pins it. The check stays at that spot: do not move the `case` below the env-file sourcing (a later launch-scoping change must keep computing the flags at that spot and defer only the `exit 2`), or an env-file value would start choosing the flags and an env-file `CC_CLAUDE_FLAGS=""` would take the default.
- The variable is read from the shell environment at that spot, before `~/.claude/ccsession.env` is sourced, so it cannot be set from that file; the docs say so and a test pins it. The variable stays exported to nested launches (a nested `ccsession` or Claude Code started from inside the session inherits the non-bypass choice); the docs say so and a test pins it.
- `show_help` in `src/superclaude/skills/ccsession-tag/ccsession` (line 1652 before this plan) prints the header only up to the first line that starts with `# The wrapper always runs`. Do not change the first words of that line and do not edit `show_help`; new `--help` text goes above that line.
- Edit only `src/superclaude/` sources, tests, docs and `CHANGELOG.md`. The `.claude/` copies are gitignored sync output and are never staged.
- Delivery note, not a code task: the pull request that ships this plan must say in its description that it unblocks Coder PR 458 and link issue 390; `/sc:pr-submit` writes that description after the plan is approved and executed.
Start sha: b5d0068933eded0e9a9ec2821380406c3fe00bb8
Diff against the start snapshot: 
diff --git a/src/superclaude/skills/ccsession-tag/README.md b/src/superclaude/skills/ccsession-tag/README.md
index 1edd920e..2cf71df8 100644
--- a/src/superclaude/skills/ccsession-tag/README.md
+++ b/src/superclaude/skills/ccsession-tag/README.md
@@ -514,6 +514,8 @@ failure.
 | `CCSESSION_FIRST_BYTE_TIMEOUT` | Wait for a streamed tier reply to start before trying the next model (default 300) |
 | `CC_SHIM_PORT` | Base shim port (default 4010). Show-all, a non-standard env file, tier settings from the shell, or a workspace owner name or roles (every Coder session) get base + an offset; an explicitly set port is used as-is |
 | `CCSESSION_COMPACT_WINDOW`, `CCSESSION_COMPACT_PCT` | Override the auto-compact window or percentage, in tier mode too |
+| `CCSESSION_PERMISSIONS=default` | Start Claude without `--dangerously-skip-permissions`: only `--allowedTools=Grep` is added, so Grep and Glob stay available. The shim and tier-model routing are unchanged. Set it in the shell environment that starts `ccsession`; it is read before `~/.claude/ccsession.env` is sourced, so it cannot be set from that file. It stays exported to nested launches. Any other non-empty value exits with status 2 on every `ccsession` call, `--help` included (under a bad value `ccsession-orca` also prints its "not a valid session name; ignoring it" warning before the exit). A non-empty `CC_CLAUDE_FLAGS`, from the shell or the env file, still wins; flags the caller passes (such as Orca's default `--dangerously-skip-permissions` option) still apply. Unset or empty: no change |
+| `CC_CLAUDE_FLAGS` | Replaces the flags `ccsession` adds to every Claude it starts (default `--dangerously-skip-permissions --allowedTools=Grep`, or `--allowedTools=Grep` with `CCSESSION_PERMISSIONS=default`). An empty value takes the default |
 
 ---
 

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
