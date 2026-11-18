82d11bf42844283094fc7d3967c5b2c7e46ac038
Review one task for spec compliance.

Task brief: ## Task 7: Update the user guide and the architecture reference for the new default
In `docs/user-guide/commands.md` update the `/sc:issue` section: in the options table (line 368) set the `--pipeline` default to `full` and say omitted means `full`; in the levels table move "(default)" from `worktree` (line 377) to `full` (line 378); in the paragraph after the options table, make the `E-SUBMIT-NEEDS-FULL` sentence say `--submit` with `--pipeline worktree`, `--pipeline none` or no `--pipeline` stops; add `/sc:issue --claim 302 --pipeline worktree` to the examples; add one sentence that the issue watcher always passes `--pipeline none`. Leave the guard and ship-gate paragraph unchanged. In `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` change line 1557 (the `--pipeline` default `worktree`) to `full` and make line 1635 (`--submit` with a value or without `--pipeline full`) also name the case of no `--pipeline`; in the Impact cell of the row at line 1557 ("`--submit` with a pipeline other than `full`, or with a value, is refused") add that a `--submit` with no `--pipeline` is refused too.
Acceptance criteria (ids):
T7.AC1: `grep -n "worktree. (default)" docs/user-guide/commands.md` prints nothing and the `full` row of the levels table carries "(default)".
T7.AC2: The syntax block, the ClickUp table and the guard paragraph are unchanged.
T7.AC3: Re-reading lines 1557 and 1635 of the architecture reference shows `full` as the default and the no `--pipeline` case in the `--submit` condition and in the Impact cell of the line 1557 row.
Global constraints: ## Constraints
- Edit only source files: `src/superclaude/...`, `tests/...`, `docs/...` and the one mirror file `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. Never edit or stage anything under `.claude/`; Task 10 regenerates those copies with `make sync-dev`.
- The default level applies to a bare `--claim`. The issue watcher always passes `--pipeline none` (`build_claim_prompt` in `src/superclaude/cli/issue_watch/launch.py`, pinned by `tests/issue_watch/test_launch.py`). Do not edit either file and do not add any human-versus-agent detection.
- The default level does not authorize a commit, a push or a pull request: `E-SUBMIT-NEEDS-FULL` keeps its meaning, so a `--submit` with no `--pipeline` still stops and `--submit` needs an explicit `--pipeline full` (the design record `docs/designs/sc-issue-claim-pipeline-flag.md` line 85 already says so).
- No file under `src/superclaude/skills/sc-issue-protocol/` and not `src/superclaude/commands/issue.md` may contain the text `src/superclaude/` (`tests/skills/test_issue_protocol.py::test_no_source_tree_path_in_skill_files` and `tests/commands/test_issue_command.py::test_no_source_tree_path` forbid it): in those files cite code by file name, never by its `src/superclaude/` path.
- New lines in command and skill files must not contain `git add`, `git commit`, `git push`, `git merge`, `gh pr` or `gh api`: `tests/skills/test_worker_contract.py` audits those verbs line by line.
- Leave the ship-gate sentences (OB-H1, OB-H2, OB-H3) and the `--pipeline none` coordinator-handoff paragraph exactly as written. The worktree `claim-handoff-planb` edits the same files (`issue.md`, `SKILL.md`, `refs/claim.md`, `HOW-WE-WORK.md`), so keep every edit narrow and rebase onto `origin/master` before any pull request.
- Out of scope: `/tech-research`, `/task-builder` and `/task` handling, the complex bug row, model tiers, `orca_worktree.py`, every other chain row, and the command version (it stays 1.1.0, which `tests/commands/test_issue_command.py` pins).
- Also out of scope, recorded on purpose: `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` lines 17-19 (the coordinator path keeps its brainstorm step for simple work); the owner-run bare launch prompts in `docs/designs/issue-watcher-setup.md` lines 616-619 (a launch with them now starts at `full`; update them before reuse if a claim-only capture is wanted); and the dated records `docs/designs/issue-watcher.md` lines 41 and 48 and `docs/designs/issue-watcher-setup.md` line 575.
- Known risk, not fixed here: a person's bare `/sc:issue --claim <N>` on an issue that a coordinator already owns reuses its worktree and starts a second agent, now at `full`, because only the claim's own launch step writes the launch record (`cmd_pending` in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` writes only a pending record). Do not claim such an issue without `--pipeline none`.
Start sha: 82d11bf42844283094fc7d3967c5b2c7e46ac038
Diff against the start snapshot: diff --git a/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md b/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md
index 278a62975..63b1aab1e 100644
--- a/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md
+++ b/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md
@@ -1554,7 +1554,7 @@ Settings and flags that change behavior, with the default of each build kept sep
 | `orchestrationHeartbeatIntervalMinutes` | Minutes between heartbeats | 5; range 1-60; anything else (0, 61, 2.5, strings) becomes 5 (`orchestration-heartbeat.ts:6,10-12,15-31`, re-read) | The "two missed intervals" threshold (`:9`) is a warning only in the retired scheduler (`coordinator-task-dispatch.ts:16-34`); on the live surface Orca derives no verdict from heartbeat age. Heartbeat age as a stall indicator is IronClaude policy (S-table, deadline W) |
 | `IR7_REFUSE` (L2 pre-push refusal) | Whether a missing L2 hook refuses the launch | CHECKOUT: no such switch; the claim warns `W-L2-ABSENT` only (`orca_worktree.py:800-801`). ORIGIN/MASTER and the installed copy: `IR7_REFUSE = False` (research 04 F5, installed line 819, not traced further) | Warning only in both; ORIGIN/MASTER also installs an owned L2 pre-push hook |
 | `--unattended` and `--report-dir <dir>` (command flags, `WORKER-CONTRACT.md:12-15`) | Switch a command to worker mode; the one report directory | off; `--unattended` counts only as a standalone token outside quotes | Person-mode flags (`--interactive`, `--format interactive`, `--mode socratic`, `--watch`, `--monitor 1`) are refused with `worker_status: failed`; neither or both report directories is refused with the exact chat error at `:38`. The `--monitor 1` clause has no implementing `## Unattended mode` section in pr-submit (owner question C2) |
-| `/sc:issue --claim` launch level: command flags `--pipeline` and `--submit`; claim-helper argument `--level` | The command takes `--pipeline worktree\|full\|none` and `--submit` (only with `--pipeline full`) (`src/superclaude/commands/issue.md:43-44`). `--level worktree\|full` is not a command flag: it is the required argument of the helper subcommands `prompt` and `launch` (`orca_worktree.py:1448,1458`), together with `--submit`; the skill passes the level `<L>` to `launch` (`refs/claim.md:118`). The level word written to `pending/<nonce>` is `worktree`, `full`, or `full-submit` when `--submit` is given (`orca_worktree.py:1334`); `main` rejects `--submit` without `--level full` (`:1467-1468`) | `--pipeline`: `worktree`; `--submit`: off (`issue.md:43-44`); the helper's `--level` has no default (required) | `--pipeline none` ends the claim before Wave 7 and 8: no worktree, no agent (`refs/claim.md:93`). `--submit` with a pipeline other than `full`, or with a value, is refused before Activation with `E-SUBMIT-NEEDS-FULL` (`sc-issue-protocol/SKILL.md:144`) |
+| `/sc:issue --claim` launch level: command flags `--pipeline` and `--submit`; claim-helper argument `--level` | The command takes `--pipeline worktree\|full\|none` and `--submit` (only with `--pipeline full`) (`src/superclaude/commands/issue.md:43-44`). `--level worktree\|full` is not a command flag: it is the required argument of the helper subcommands `prompt` and `launch` (`orca_worktree.py:1448,1458`), together with `--submit`; the skill passes the level `<L>` to `launch` (`refs/claim.md:118`). The level word written to `pending/<nonce>` is `worktree`, `full`, or `full-submit` when `--submit` is given (`orca_worktree.py:1334`); `main` rejects `--submit` without `--level full` (`:1467-1468`) | `--pipeline`: `full`; `--submit`: off (`issue.md:43-44`); the helper's `--level` has no default (required) | `--pipeline none` ends the claim before Wave 7 and 8: no worktree, no agent (`refs/claim.md:93`). `--submit` with a pipeline other than `full`, with no `--pipeline`, or with a value, is refused before Activation with `E-SUBMIT-NEEDS-FULL` (`sc-issue-protocol/SKILL.md:144`) |
 | `onFailure` (Claude Code hook field) | Makes a failing or timed-out hook block | Not set on any registration here | DOCUMENTED: with `"block"` a timeout blocks (Claude Code v2.1.295 or later); the design rejects it because a broken hook would then block ungoverned sessions (`merged-requirements.md:98,694,701`, per `gap-P3-G06.md` 2) |
 | `disableAllHooks`, `allowManagedHooksOnly`, `--bare`, `CLAUDE_CODE_SIMPLE`, `--safe-mode` (Claude Code) | Switch the settings-registered guards off | not set on the research host (`disableAllHooks` only) | DOCUMENTED routes, not observed bypasses; `disableAllHooks` alone is detected by the claim preflight |
 | Worker start readiness `timeoutMs` (Orca) | Deadline for the agent to become ready | 60 s (`local-worker-start.ts:145,228`, ORCA-CHECKOUT) | Expiry throws "Agent did not become ready" for a terminal worker (`:245-257`); the 30 s ask limit of ccsession is chosen to stay under it. The resulting Dispatch state was not traced |
@@ -1632,7 +1632,7 @@ The 13 STOP codes of `sc-issue-protocol/SKILL.md:144-160`, with the recovery the
 
 | Code | Cause | Recovery |
 |---|---|---|
-| `E-CREATE-ONLY-FLAG`, `E-CLAIM-ONLY-FLAG`, `E-SUBMIT-NEEDS-FULL` | A flag that belongs to the other mode (`--depth`, `--mode`, `--type` with `--claim`; `--pipeline`, `--submit` with `--create`), or `--submit` with a value or without `--pipeline full` (`SKILL.md:144`) | The command stops with usage before Activation; correct the flags. Remedy beyond that: none stated |
+| `E-CREATE-ONLY-FLAG`, `E-CLAIM-ONLY-FLAG`, `E-SUBMIT-NEEDS-FULL` | A flag that belongs to the other mode (`--depth`, `--mode`, `--type` with `--claim`; `--pipeline`, `--submit` with `--create`), or `--submit` with a value, without `--pipeline full` or with no `--pipeline` (`SKILL.md:144`) | The command stops with usage before Activation; correct the flags. Remedy beyond that: none stated |
 | `E-NO-ORIGIN` | No `origin` remote, git failed, or `origin` is not a GitHub URL; `origin_repo.py` exit 1 (`SKILL.md:145`; `origin_repo.py:45-50`) | The skill prints the script's stderr line with the STOP (`refs/claim.md:15`); no further remedy stated |
 | `E-FOREIGN-REPO` | The claim URL names a repository other than `origin`; `origin_repo.py` exit 3 (`SKILL.md:146`) | Same: stderr line printed; no further remedy stated |
 | `E-NOT-AN-ISSUE` | The argument is a pull request or not an issue number or URL; `origin_repo.py` exit 4 (`SKILL.md:153`; `refs/claim.md:40`) | Message "#N is a pull request, not an issue; not claimed."; no further remedy stated |
diff --git a/docs/user-guide/commands.md b/docs/user-guide/commands.md
index 9dcc68b22..331c82d9a 100644
--- a/docs/user-guide/commands.md
+++ b/docs/user-guide/commands.md
@@ -365,17 +365,17 @@ When codegraph, the index or its lookup tools are not usable, it falls back to G
 | `--depth quick\|standard\|deep` | create | `quick` | How hard the command checks your flags and fills the body; `deep` uses the complex template |
 | `--mode feature\|bug` | create | chosen by a worker | Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` or `bug` label |
 | `--type <type>` | create | chosen by a worker | Area of the change: `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install` or `other`; a feature in `tests` gets the issue type Test, otherwise the area is recorded in `flags.md` and no label is applied for it |
-| `--pipeline worktree\|full\|none` | claim | `worktree` | How far the launched agent goes (see the levels below); `worktree` and `full` create the worktree and launch an agent, `none` creates no worktree and launches no agent |
+| `--pipeline worktree\|full\|none` | claim | `full` | How far the launched agent goes (see the levels below); omitted means `full`; `worktree` and `full` create the worktree and launch an agent, `none` creates no worktree and launches no agent |
 | `--submit` | claim | off | Only with `--pipeline full`: the agent also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`. Takes no value |
 
-`--depth`, `--mode` and `--type` work with `--create` only; `--pipeline` and `--submit` work with `--claim` only (`E-CLAIM-ONLY-FLAG`), and `--submit` without `--pipeline full` stops with `E-SUBMIT-NEEDS-FULL`. There is no repository option: the repository is always `origin`.
+`--depth`, `--mode` and `--type` work with `--create` only; `--pipeline` and `--submit` work with `--claim` only (`E-CLAIM-ONLY-FLAG`), and `--submit` with `--pipeline worktree`, with `--pipeline none` or with no `--pipeline` stops with `E-SUBMIT-NEEDS-FULL` (write `--pipeline full --submit`, even though `full` is the default). The issue watcher never relies on the default: it always passes `--pipeline none`. There is no repository option: the repository is always `origin`.
 
 **Claim levels (`--pipeline`):**
 
 | Level | What the launched agent does | Commit, push, PR |
 |-------|------------------------------|------------------|
-| `worktree` (default) | Runs the steps of `next-steps.md` up to the plan boundary, prints the plan path and `Waiting for approval`, then waits until you run the printed implement command (a plain `approved` reply no longer releases it) | No |
-| `full` | Runs every step, implementation included, and leaves the changes in the working tree, nothing staged | No |
+| `worktree` | Runs the steps of `next-steps.md` up to the plan boundary, prints the plan path and `Waiting for approval`, then waits until you run the printed implement command (a plain `approved` reply no longer releases it) | No |
+| `full` (default) | Runs every step, implementation included, and leaves the changes in the working tree, nothing staged | No |
 | `full` with `--submit` | Does the same, then commits, pushes a feature branch to `origin` and opens a PR through `/sc:pr-submit --monitor 3` | Yes; never merges |
 | `none` | Stops after the comments: no worktree, no agent. You run `.dev/issues/<N>/next-steps.md` yourself from this checkout | No |
 
@@ -385,6 +385,7 @@ No level merges anything: people review and merge. The agent starts behind the c
 
 ```bash
 /sc:issue --claim 302
+/sc:issue --claim 302 --pipeline worktree
 /sc:issue --claim 302 --pipeline none
 /sc:issue --claim 302 --pipeline full
 /sc:issue --claim 302 --pipeline full --submit


Codegraph context
index_state: fresh
checked_at: 2026-11-18T05:09:43Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline
projectPath: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: the task changes Markdown or test text, not code symbols; no dependents outside the touched set were listed.

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
