## Phase 3 of #323: commands, skills and agents use codegraph; new `/sc:impact` and `/sc:graph`

Phase 1 removed Serena and codebase-memory; Phase 2 installs and registers codegraph 1.6.2. This phase makes IronClaude's primitives use codegraph where it is the simplest correct tool, always above the existing Grep/Read fallback, and adds two commands. Plan: `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/` (14 tasks, each reviewed by a fresh reviewer; ledger in `progress.md`). Decision log: `.dev/codegraph-migration/decisions/P3X-execution-log.md`.

### What changes

| Group | What | Commits |
|---|---|---|
| 0 Prerequisite experiments | Gate G1-G6 passed (seven-tool branch); baselines recorded; experiments E-1 (index freshness: Outcome A), E-2 (CLI flags), E-3 (exact per-verb allowlists work), E-6 (all four agents reach codegraph in foreground and background), E-7 (Phase 1 slots map) | e4b7d131, 903cf368 |
| A Shared guide and core docs | New `src/superclaude/core/CODEGRAPH.md`, installed as `~/.claude/CODEGRAPH.md`: readiness check, closed list of 14 `graph:*` tokens, tool table, nine standing rules and the call-site procedure. Core `CLAUDE.md`, orchestration mode and the auggie guide point to it | 86e5e888, 8ed5e57b |
| B Agents | troubleshoot-analyst, reflect-reviewer, reuse-auditor and auggie-reviewer get exact codegraph tool names and a run-state rule | fd249cc9 |
| C Troubleshoot and other skills | Troubleshoot Tier 1 writes codegraph caller rows to `tier1-callers.md` on a fresh index and keeps the Grep floor otherwise; validate-roadmap, brainstorm, task, tasklist, cleanup-audit and auggie-review use codegraph above their floors | 28e3597a, e6724a7d, afc075af |
| D New commands | `/sc:graph` (readiness report; `/sc:graph init` is user-typed only) and `/sc:impact` (production and test dependents with shown/total, call sites checked by reading the code, optional advisory test list; writes `impact.md` and `return-contract.yaml`, never stops a caller) | 959e9e3d, 922adcc3, 5eb4d336, ccfa410f |
| E Reflect | Reflect's evidence chain uses codegraph above its floor; Step 1B.3 calls `/sc:impact` for counts that are logged only; `graph:*` tokens never halt reflect (pinned by a test) | eb806c2e, f8b356c9, 57d9affc |
| F Callers and routing | `/sc:impact` is called (warnings and context only) from implement Q1/Q6, pr-submit Waves 3-4 and VG-1, troubleshoot `--fix` Phase A, auggie-review Wave 1 and task STRICT step 6; `/sc:load` points to `/sc:graph status`; `/sc:explain` gains a one-hop callers/callees view; the routing guide lists both commands | 49614436, ad9aa379 |
| G Verification | Changelog, user-guide paragraph, full checks and live smoke; `Edit` added to the two new skills' allowlists after the smoke | 31cdca12, 4dc5cd9b, and the record commit of this PR |
| Review fixes | Augment review (4 Medium findings, all verified): `/sc:impact` diff defaults compare against `HEAD`, diff mode without codegraph lists changed files as unmapped (`no_graph`), call-site checks cover direct callers only, and name patterns are `$`-safe (also the guide's CS2); Phase 3 test files formatted | b356399c |

Nothing in this PR changes a gate, severity, verdict or touched-file rule: every codegraph answer is a lead that is Read before it is cited, an empty graph result never proves absence, and `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` sends every primitive back to Grep/Read. No primitive syncs, rebuilds or removes an index, and none names `codegraph_explore` or a wildcard allowlist.

### Verification (`.dev/codegraph-migration/experiments/P3-T11-smoke.md`)

- Dev-copy sync and `verify-sync`: pass. `make` is not installed on the build host, so the two Makefile recipes ran unchanged through a small runner (logged).
- Installed-path count: 157, equal to the starting count.
- No old Serena or codebase-memory tool names, no `codegraph_explore`, no wildcard allowlist, no mutating CLI verb outside `/sc:graph init`; version pin 1.6.2 matches the installer.
- Targeted test set: 2104 passed, 0 failed (start of phase: 1897 passed, 0 failed); no new failing test.
- Live smoke in fresh headless sessions: `/sc:graph status` reports `fresh` (972 files); `/sc:impact install_core_files` lists `install` and `update` in `src/superclaude/cli/main.py` as production dependents with `resolution: call-site-verified` (after the `Edit` allowlist fix); troubleshoot writes `tier1-callers.md` with both callers verified.

### Known limits

- The installed `~/.claude/skills/sc-troubleshoot-protocol` on the build host predates this branch and takes precedence over the project copy, so the troubleshoot smoke followed this branch's skill copy. After merge and `superclaude install`, run `/sc:troubleshoot "install_core_files skips files" --depth quick` once to confirm the installed command writes `tier1-callers.md`.
- `~/.claude/CODEGRAPH.md` exists only after `superclaude install`; until then primitives read the labelled in-checkout fallback `src/superclaude/core/CODEGRAPH.md`.

### Deferred ideas (source section 2.3; not in this phase)

| Idea | Reopen when |
|---|---|
| Reflect severity from production-only counts | 10 shadow runs reviewed |
| `dependent-impact` finding class in auggie-review | 20 shadow reviews meet the thresholds |
| `changed-area` plus `affected` as the real VG-1 gate | a 20-change backtest passes |
| Implement post-edit "untouched dependents" check | E-1 Outcome A (now met) |
| Cleanup-audit: nonzero callers move DELETE to REVIEW | a spike shows a hit Grep missed |
| Reflect UC-2 "mapped tests neither changed nor run" | E-1 Outcome A (now met) |
| Workflow informational impact note | a consumer asks for it |

### Progress comments on #323

Group 0: https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6544339802 · A: https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6544466471 · B: https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6544514469 · C: https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6544681062 · D: https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6544874463 · E: https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6545041697 · F: https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6545142355

Merging is a human decision.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
