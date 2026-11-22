# /sc:recommend output for #504

- Recorded: 2026-11-11T19:36:00Z
- Goal sent: Pick the next-step chain for GitHub issue https://github.com/IronbellyOrg/IronClaude/issues/504. Type: feature. Complexity: complex. Owner preference: five separate sessions in one new worktree (analyze, design, implement, workflow, general-purpose agent files); each command session runs /sc:design, then /sc:workflow, then /sc:implement. Recommend only.

The block below is the skill's output, copied verbatim.

````text
Goal: add codegraph (readiness check, then Grep/Read fallback) to /sc:analyze, /sc:design, /sc:implement, /sc:workflow and the ten general-purpose agent files, as five parallel sessions of one worktree.

Level: 3 (follow a checked implementation plan) - guide section 3.2, row `feature-existing`; the design step comes from row `focused-design` (section 3.13). guide_status: matched.

Changes files: yes. /sc:design writes design artifacts only; /sc:workflow writes one new package under .dev/tasks/to-do/<id>/; /sc:implement edits src/superclaude/ files, then make sync-dev.

Run these in order (one block per session; `<X>` = that session's file):

Command sessions (analyze, design, implement, workflow):
1. /sc:design <X command and its backing skill, if any> --type component --format spec
   - contract gap: `/sc:design` has no `--depth` flag (its formal usage is `--type`, `--format`, `--output`, `--unattended`, `--report-dir`), so the requested `--depth quick` is omitted.
2. /sc:workflow <design output from step 1> --depth quick --handoff none
3. read the printed plan path .dev/tasks/to-do/<id>/<id>.md and its advisory check, then /sc:implement <that printed plan path>

Agents session (ten general-purpose agent files; one rule, no design needed):
1. /sc:workflow "Add the one-line codegraph rule (use codegraph only when the caller passes index_state: fresh, otherwise Grep/Read) to the ten general-purpose agent files listed in .dev/issues/504/issue-summary.md" --depth quick --handoff none
2. /sc:implement <plan path printed by step 1>

Notes:
- Edit src/superclaude/ only, then run make sync-dev and make verify-sync (CLAUDE.md of the repo).
- The five sessions touch different files, so they can run side by side; /sc:analyze and /sc:design have no backing skill, so each of those two sessions edits only its command file.
- Work from origin/master: the local checkout is 49 commits behind.
- Default row "Feature, complex" (brainstorm, design, workflow --depth deep, implement) not used: the owner asked for per-file sessions, so brainstorm is skipped and quick depth is used.

Sources verified:
- /home/coder/.claude/HOW-WE-WORK.md (routing table, rows `feature-existing`, `focused-design`, `simple-plan`)
- /home/coder/.claude/commands/sc/design.md (Usage: --type, --format, --output; no --depth)
- /home/coder/.claude/commands/sc/workflow.md (--depth quick|standard|deep, --handoff none|design|implement|tasklist)
- /home/coder/.claude/commands/sc/implement.md (<path-or-prompt>, --resume, --ledger, --skip-final-review)
- auggie semantic rank: skipped (matched row)
````
