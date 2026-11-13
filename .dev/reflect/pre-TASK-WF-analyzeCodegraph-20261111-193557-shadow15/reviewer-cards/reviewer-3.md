# Reviewer 3 card (refactorer, structural / tech-debt lens)

**Reviewer persona**: refactorer
**Grounding root**: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
**Scope**: analyze.md codegraph integration at current HEAD (after PR #511, #513, #515)
**Timestamp**: 2026-11-13

## Verdict

The integration holds together structurally. Section sizing is within budget, run state is threaded consistently, and I found no contradiction between analyze.md and the guide. I raise three MINOR items, none blocking.

## What I checked

- **Sizing**: the Codegraph section is lines 61-70, 10 lines, against the budget of about 25. It is long in characters, not in lines. The single "Leads, not citations" bullet at line 67 holds about six rules in one line.
- **Run-state threading**:
  - The readiness check is stated once, before step 1 (line 30).
  - `index_state`, `access`, `checked_at` and `worktree_root` are kept for the whole run.
  - Steps 1-3 gate on fresh state.
  - Step 5 reports the state, and the Subagents bullet (line 70) passes it to fan-out.
  - The Codegraph section (line 65) points back to the single check rather than restating it.
  - The cli/none path correctly bars even `codegraph_files`.
- **Tool names and fallbacks**: Tool Coordination (line 52) lists exactly the tools the steps call. The guide's tool table (section 4) agrees, including the `symbolsOnly:true` outline and the `path` argument for `codegraph_files`.
- **Evolution drift (PR #513 and #515)**: line count is unchanged at 139. The wording changes (60 s wait, `date` for `checked_at`, `includeCode` scoping, `graph:empty` token) all match guide section 2 steps 3 and 7 and the section 3 token list. I found no byte-drift that matters.
- **Rule duplication**: this is where the three findings come from.

## Deviations

None in the spec-relative 4-class sense. Structural debt only, listed below.

## Adherence summary

- Spec units audited: 4 (section size, readiness-once, fresh-only gating, boundaries preserved)
- Fully adherent: 4
- Authorized expansion: 0 | Necessary deviation: 0 | Drift: 0 | Regression: 0

## Notes

- Wave 1 listed 12 findings; none were carried into this card.
- I did not read reflect.md for parity.
- H1 from the T1 card (the `symbolsOnly` prohibition has no matching AC) stays open. The guide section 7 forbids file mode without `symbolsOnly:true`, and analyze.md only uses it inline.

## Findings block

```json
{"id":"F1","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"Guide section 7 says it is the only section that names the forbidden verbs, but analyze.md line 68 restates init, index, sync, explore and context. A guide change to that list must now be mirrored here or the two drift.","refs":["INF-005","INF-012"],"citations":[{"role":"plan","path":"src/superclaude/commands/analyze.md","line_start":68,"line_end":68,"quote":"never run `codegraph init`, `index`, `sync`, `explore` or `context`"},{"role":"spec","path":"src/superclaude/core/CODEGRAPH.md","line_start":87,"line_end":89,"quote":"The only section that names these:"}]}
{"id":"F2","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"analyze.md line 30 states the 60 s build wait unconditionally. Guide section 2 step 3 applies it only when the primitive's Bash allowlist permits pgrep. The command is a second statement of a guide rule and drops that condition.","refs":["INF-005"],"citations":[{"role":"plan","path":"src/superclaude/commands/analyze.md","line_start":30,"line_end":30,"quote":"on the MCP path it first waits up to 60 s for a running `init` or `index`"},{"role":"spec","path":"src/superclaude/core/CODEGRAPH.md","line_start":13,"line_end":13,"quote":"when the primitive's Bash allowlist permits `pgrep`"}]}
{"id":"F3","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"The 10-line section meets the 25-line budget only because the Leads bullet packs about six rules into one long line. The line-count AC is met, but the rules are hard to maintain and partly duplicate guide sections 3 and 5.","refs":["INF-012"],"citations":[{"role":"plan","path":"src/superclaude/commands/analyze.md","line_start":67,"line_end":67,"quote":"a caller list shorter than its total is `graph:truncated`"},{"role":"spec","path":"src/superclaude/core/CODEGRAPH.md","line_start":58,"line_end":64}]}
```

reviewer_model_self_report: claude-gw-tier1b[1m]
