/model claude-gw-tier1b   (use claude-gw-tier2 when claude-gw-tier1b is not in your /model list)

# Next steps for #606

Plan boundary: after step 2

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at the default level), or you do after `--pipeline none`.

1. Assemble the spec from the issue comments with the body's own command, unless `.dev/issues/409/visual-parity/REDESIGN-SPEC.md` already exists on the branch (its sha256 must equal the one in the comment marker lines, `a5fc4f9b6862432bd46700abaca1be1149591999c718225f7908547c9f9ffbd6`):
   `mkdir -p .dev/issues/409/visual-parity && gh issue view 606 --repo IronbellyOrg/IronClaude --json comments --jq '[.comments[] | select(.body|startswith("<!-- REDESIGN-SPEC part")) | .body | sub("^[^\n]*\n";"")] | join("\n")' > .dev/issues/409/visual-parity/REDESIGN-SPEC.md`
   - Input: the three REDESIGN-SPEC comments on the issue
2. `/sc:workflow @.dev/issues/409/visual-parity/REDESIGN-SPEC.md --depth standard --handoff none`
   - Input: `@.dev/issues/606/issue-summary.md` for the cheatsheet; read the printed plan `.dev/tasks/to-do/<id>/<id>.md` and its advisory check result, then stop here for a human approval.
3. `/sc:implement <plan path printed by step 2>` (after approval; each phase ends with its render gate, and no phase starts before the previous gate closes)
4. Rebase on `origin/master`, then `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."` (only when a PR is requested; it targets `IronbellyOrg/IronClaude`)

- Effort estimate: 56 hours
- Open item before step 2: the Phase 0 inputs (`VP/inputs/tools/render_current.py`, baseline captures) and the evidence trail exist only untracked in `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/` (see `accuracy-check.md`). They are not on any branch, so the plan cannot rely on them until a person decides to push or rebuild them. Never edit that checkout.
- Default row not used: Feature, complex (brainstorm, design, workflow, implement). The issue already carries a complete phased spec, so the brainstorm and design steps would repeat finished work.
