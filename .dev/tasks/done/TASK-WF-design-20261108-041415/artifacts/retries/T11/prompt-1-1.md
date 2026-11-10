35579d7f6d6573088ce542d477c22107bd65b666
Review one task for spec compliance.

Task brief: ## Task 11: Update HOW-WE-WORK.md and its plugin mirror

Depends on: Task 3

Edit `src/superclaude/core/HOW-WE-WORK.md` at line 329 (the `/sc:issue` row that says "labels from a fixed set"): change that phrase to "an issue type, the Complexity field and a mode label". Then copy the whole file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (same line 329). Then search `src/superclaude/core/CLAUDE.md` for the same phrase; if it appears (the level table copy), change it identically there, otherwise leave that file alone.

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` reports no difference.
- "labels from a fixed set" no longer appears in either file or in `src/superclaude/core/CLAUDE.md`.
- `uv run pytest tests -k "how_we_work or HOW_WE_WORK or level_table" -v` passes, or, if no test matches that expression, `grep -rl "HOW-WE-WORK" tests` names the tests that check the mirror and they pass.

AC ids:
T11.AC1: `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` reports no difference.
T11.AC2: "labels from a fixed set" no longer appears in either file or in `src/superclaude/core/CLAUDE.md`.
T11.AC3: `uv run pytest tests -k "how_we_work or HOW_WE_WORK or level_table" -v` passes, or, if no test matches that expression, `grep -rl "HOW-WE-WORK" tests` names the tests that check the mirror and they pass.
Global constraints: - Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits.
- Text inside the skill, command and agent files must not contain the string `src/superclaude/` (an installed-path rule; a test scans the skill folder for it).
- Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`. No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`.
- `--claim` behaviour and text stay unchanged, including its two-block part of the return contract. The T1 and T2 worker files, `refs/tiers.md`, `scripts/*.py` and the four issue-body templates stay unchanged.
- The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST).
- Nothing in this plan writes to GitHub while it is executed. The POST body, the `--type` flag and the silent-drop behaviour come from GitHub's docs and `gh` help and are UNVERIFIED by a real run; Task 12 leaves the owner a manual check for that.
- Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit.
- Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly `orgs/<owner of R>/issue-fields`; the `--type` area flag and its 11 values stay but no longer produce a label; the `bug` / `enhancement` mode labels stay.
Start sha: 35579d7f6d6573088ce542d477c22107bd65b666
Diff against the start snapshot: 
diff --git a/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md b/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
index d629e20f..1cf5ab70 100644
--- a/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
+++ b/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
@@ -326,7 +326,7 @@ Additional operations and explicit coordination choices. These entries can be re
 | `/sc:impact` | Report what depends on named symbols or on a diff (`--diff <base>`), production and test dependents with call-site checks, plus an advisory test list with `--tests`; it writes `impact.md` and `return-contract.yaml` and changes no code. |
 | `/sc:index` | Coordinated project docs/API/structure/README and requested output format; writes documentation. Distinct from a compact repo map. |
 | `/sc:index-repo` | Compact PROJECT_INDEX.md and PROJECT_INDEX.json map. Preserve documented keyword mode=quick or mode=update and existing-output intent. Verify invocation naming in the active copy; no measured token-savings promise. |
-| `/sc:issue` | Claim an existing GitHub issue on the origin repo (`--claim <number or url>`): it assigns the issue to you, checks its accuracy against today's code, writes a summary and a next-step prompt, then creates an Orca worktree and launches an agent in it at the `--pipeline` level (`worktree` by default: plan, then wait for approval; `full`: also implement; `--submit` with `full`: also commit, push and open a PR; `none`: no agent) and never merges. Create (`--create "<description>"`) files a templated GitHub issue on the origin repo with labels from a fixed set. Both post directly to GitHub and write `.dev/issues/`. |
+| `/sc:issue` | Claim an existing GitHub issue on the origin repo (`--claim <number or url>`): it assigns the issue to you, checks its accuracy against today's code, writes a summary and a next-step prompt, then creates an Orca worktree and launches an agent in it at the `--pipeline` level (`worktree` by default: plan, then wait for approval; `full`: also implement; `--submit` with `full`: also commit, push and open a PR; `none`: no agent) and never merges. Create (`--create "<description>"`) files a templated GitHub issue on the origin repo with an issue type, the Complexity field and a mode label. Both post directly to GitHub and write `.dev/issues/`. |
 | `/sc:load` | Load/refresh project context from the `.superclaude/memory/` files with supported type/refresh/analyze controls; needs no MCP server. Not executor resume or proof of complete checkpoint restoration; exclude undeclared example-only options. |
 | `/sc:pm` | Explicit PM coordination with requested strategy/verbosity and available protocol/tools. It can write memory/docs; verify dependencies. Not a default planner, automatic-start guarantee or universal executor-resume method. |
 | `/sc:save` | Persist requested session/learnings/context/all memory with supported summarize/checkpoint controls. Stores plain markdown files under `.superclaude/memory/` (no MCP server) and writes memory; not durable task execution state or a latency guarantee. |
diff --git a/src/superclaude/core/HOW-WE-WORK.md b/src/superclaude/core/HOW-WE-WORK.md
index d629e20f..1cf5ab70 100644
--- a/src/superclaude/core/HOW-WE-WORK.md
+++ b/src/superclaude/core/HOW-WE-WORK.md
@@ -326,7 +326,7 @@ Additional operations and explicit coordination choices. These entries can be re
 | `/sc:impact` | Report what depends on named symbols or on a diff (`--diff <base>`), production and test dependents with call-site checks, plus an advisory test list with `--tests`; it writes `impact.md` and `return-contract.yaml` and changes no code. |
 | `/sc:index` | Coordinated project docs/API/structure/README and requested output format; writes documentation. Distinct from a compact repo map. |
 | `/sc:index-repo` | Compact PROJECT_INDEX.md and PROJECT_INDEX.json map. Preserve documented keyword mode=quick or mode=update and existing-output intent. Verify invocation naming in the active copy; no measured token-savings promise. |
-| `/sc:issue` | Claim an existing GitHub issue on the origin repo (`--claim <number or url>`): it assigns the issue to you, checks its accuracy against today's code, writes a summary and a next-step prompt, then creates an Orca worktree and launches an agent in it at the `--pipeline` level (`worktree` by default: plan, then wait for approval; `full`: also implement; `--submit` with `full`: also commit, push and open a PR; `none`: no agent) and never merges. Create (`--create "<description>"`) files a templated GitHub issue on the origin repo with labels from a fixed set. Both post directly to GitHub and write `.dev/issues/`. |
+| `/sc:issue` | Claim an existing GitHub issue on the origin repo (`--claim <number or url>`): it assigns the issue to you, checks its accuracy against today's code, writes a summary and a next-step prompt, then creates an Orca worktree and launches an agent in it at the `--pipeline` level (`worktree` by default: plan, then wait for approval; `full`: also implement; `--submit` with `full`: also commit, push and open a PR; `none`: no agent) and never merges. Create (`--create "<description>"`) files a templated GitHub issue on the origin repo with an issue type, the Complexity field and a mode label. Both post directly to GitHub and write `.dev/issues/`. |
 | `/sc:load` | Load/refresh project context from the `.superclaude/memory/` files with supported type/refresh/analyze controls; needs no MCP server. Not executor resume or proof of complete checkpoint restoration; exclude undeclared example-only options. |
 | `/sc:pm` | Explicit PM coordination with requested strategy/verbosity and available protocol/tools. It can write memory/docs; verify dependencies. Not a default planner, automatic-start guarantee or universal executor-resume method. |
 | `/sc:save` | Persist requested session/learnings/context/all memory with supported summarize/checkpoint controls. Stores plain markdown files under `.superclaude/memory/` (no MCP server) and writes memory; not durable task execution state or a latency guarantee. |

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
