# Wave 1.5 Branch B (architectural-doc lookup), returned by troubleshoot-analyst; currency finalized by parent

Currency method (refs/doc-discovery.md Section 2): parent `stat` of each doc and of the code surface. All files share mtime 2026-11-07T20:35:30Z (the checkout time of this worktree), so Step 1 gives "fresh" for every doc, and no doc has a Status/Last reviewed marker (Step 2). Verdict = `current` by the rule table. Caveat: the mtimes carry no real age information here; git log gives 2026-11-07T09:16:43-05:00 for docs/designs/sc-issue-claim-pipeline-flag.md, consistent with "recent".

```json
[
  {"doc_path": "docs/designs/sc-issue-claim-pipeline-flag.md",
   "summary": "Rule: P7 launches the agent with `orca agent launch --agent claude --surface terminal` (a Claude CLI session), never a plain terminal and never `--surface chat`, because neither runs behind the ccsession shim. D2: worktree create uses no `--agent`. D10: `--surface terminal` always. A check reads the screen with `orca terminal read --screen` and warns W-LAUNCH-NOT-CCSESSION when no `[ccsession]` line or name question appears.",
   "currency_verdict": "current",
   "reason": "no header markers found; mtime fresh (checkout time 2026-11-07T20:35:30Z); git commit 2026-11-07T09:16:43-05:00"},
  {"doc_path": "docs/designs/sc-issue-launch-level-hook.md",
   "summary": "Design for the launch-level hook (#394): a pending record is written before `orca agent launch`; the prompt carries a `[sc-launch:v1:<nonce>]` marker. Lists `orca terminal send` and `tmux send-keys` as routes that bypass the guard. Assumes launches go through `orca agent launch`.",
   "currency_verdict": "current",
   "reason": "no header markers found (lowercase YAML keys do not match the regex); mtime fresh"},
  {"doc_path": "docs/designs/sc-issue-command.md",
   "summary": "Parent design for /sc:issue. B17 sets launch levels (worktree, full, none); the agent starts behind the ccsession shim through `orca agent launch --surface terminal`. B2 amended 2026-11-07: `--claim` creates an Orca worktree and launches one agent.",
   "currency_verdict": "current",
   "reason": "no header markers found; mtime fresh"},
  {"doc_path": "docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md",
   "summary": "Section 7.7 'Orca Orchestration: Commands as Workers': a coordinator is a hand-opened session; it creates Tasks and starts one worker per Task; workers are top-level Claude sessions running one /sc: command; rules in ~/.claude/WORKER-CONTRACT.md; WC-8: a command, skill or agent never calls worker-start, dispatch or task-create. Does not mention the Claude CLI versus New Terminal choice.",
   "currency_verdict": "current",
   "reason": "no header markers found; mtime fresh"},
  {"doc_path": "docs/testing/v5.0.0/user/D08-ccsession.md",
   "summary": "E2E guide for ccsession: `ccsession-orca` is Orca's Claude command; the name question is asked only with no task, no name and no resume and someone can answer; Step 17 sets Settings > Agents > Claude > Command to a ccsession-orca launcher; orchestrators should always pass a prompt or CCSESSION_NAME in the launch.",
   "currency_verdict": "current",
   "reason": "no header markers found; mtime fresh"},
  {"doc_path": "CLAUDE.md",
   "summary": "Orca worktree rule (about lines 305-343): every project worktree is created with `orca worktree create --name <name>` (optional --repo, --base-branch, --parent-worktree or --no-parent); bans raw git worktree add, EnterWorktree, and --issue/--pr link flags. Says nothing about starting agent sessions, `agent launch`, `worktree create --agent`, or Claude CLI versus New Terminal.",
   "currency_verdict": "current",
   "reason": "no header markers found; mtime fresh"},
  {"doc_path": "docs/user-guide/commands.md",
   "summary": "Line 115: the /sc:issue row says a claim does 'an Orca worktree and a launched agent'. Says nothing about which Orca surface.",
   "currency_verdict": "current",
   "reason": "no header markers found (only a Grep line was seen); mtime fresh"}
]
```

Not found: docs/analysis/ and docs/troubleshooting/ do not exist; PLANNING.md and KNOWLEDGE.md have no Orca mentions; docs/reference/ only mentions Orca in passing.
