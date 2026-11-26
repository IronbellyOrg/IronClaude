# Issue 703 architecture analysis

## Scope

Command: `/sc:analyze src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g4/703/analyze`.

Static architecture review of the single implementation file named by issue 703, with its controlling workflow/reflection instructions and regression tests checked as immediate consumers. No source edits, runtime tests, installs, staging or GitHub writes. Checkout: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863` on 2026-11-24.

Codegraph: index_state=fresh, checked_at=2026-11-24T13:55:11Z; degraded: none

The graph located the archive entry point, its CLI caller and 11 direct dependencies; direct source reads confirmed the relevant behavior. Markdown instructions and tests were checked through Read/Grep rather than inferred from the graph.

## Findings

1. **Medium: archive warning detection is too broad.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py:434-443` searches the entire contract for any case-insensitive occurrence of `superseded`. An unrelated prose mention or a `superseded_by` key suppresses insertion of this package's SUPERSEDED warning. The move and replacement key are separate operations, so this is not evidence that archive movement itself fails. Existing duplicate-warning coverage is confined to genuine unresolved-list warnings in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/skills/test_workflow_remediation.py:224-230`.
2. **Medium: instruction drift about copy-only repair.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:81` still says repairs are made “in place”, contradicting the copy-and-place rule at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-workflow-protocol/refs/remediation.md:3,43-57`.
3. **Low: abbreviated routing docs omit two controlling counts.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/README.md:63-64` mentions blocker count alone. The actual rule in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py:73-82` first returns none for zero blockers, then allows surgical only with blockers <=3, HIGH-labelled findings <=5 and Medium findings <=9, otherwise regenerates (or escalates after regeneration).
4. **Low: durable route recording is overstated.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-workflow-protocol/SKILL.md:101` promises recorded counts and route for none. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-workflow-protocol/refs/remediation.md:31` does not distinguish printed forced-selection output from durable recording. The route CLI only prints JSON (`remediate.py:96-105`); the mark writer accepts only regenerate route metadata (`:559-569,776`), and place writes surgical metadata (`:651-654`).
5. **Low: an implemented placement guard lacks direct regression coverage.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py:608-609` refuses placement if the old package still exists in to-do or its archived directory is absent. Every located `rm.place` call in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/skills/test_workflow_remediation.py` follows archive, including the leaf-refusal test at `:332-350`; none directly exercises placement before archive.

These match all five still-open items in issue 703. The three items the issue already calls fixed remain represented by the pre-existing undo-file refusal at `remediate.py:447-451`, rollback tests at `test_workflow_remediation.py:661-710`, and coordinator-supplied diff instructions at `refs/remediation.md:71-73`.

## Recommendations

Keep issue 703 open as a small follow-up, not a new architecture project. Restrict warning recognition to an unresolved-list item starting with SUPERSEDED and add positive and negative regression cases; repair the three documentation descriptions without adding a new metadata writer; add a direct placement-before-archive refusal test. Preserve the zero-blocker route, existing placement guard, rollback behavior, and real-warning deduplication. Update canonical sources and their actual workflow plugin mirrors together in a later implementation, not in this audit.

## Evidence and limitations

- Live issue 703 is OPEN with no comments. Its linked PR 696 is MERGED at `f2904292eed1f6710ebc5dca2eb48394fd1775f6`; PR 705 is a later, separately merged restricted-reviser fix at `1a6c8723fe9e6caa85bfffcdb97b2dc434978bf9`, not completion of these five items.
- Read-only `cmp` returned 0 for the workflow script, SKILL.md and refs/remediation.md against their corresponding `plugins/superclaude/skills/sc-workflow-protocol/` files. Comparing a reflection handoff plugin mirror failed because that path does not exist; Glob found no `remediation-handoff.md` anywhere under `plugins/superclaude/`. Do not invent or require that mirror.
- The issue's real example still contains an unrelated superseded mention at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/tasks/to-do/TASK-WF-blockerStage4-20261117-170451/return-contract.yaml:14`. This was read statically, not archived or modified.
- Searches: all test definitions, all `rm.place(` calls in the named regression file, PR searches for 703 and surgical remediation, and the local history of the named implementation files. Search hits alone were not treated as fixes: a PR 736 hit was unrelated wording with a coincidental line number.
- UNVERIFIED: runtime reproduction, current test/lint results, full sync gate, and remote branch content beyond the live PR metadata. The brief forbids uv and any writes outside this report directory, so none of those execution gates ran.
- Two initial report edits were refused by the freshness hook; the required report Read was then performed and the same edits succeeded. No alternate writer bypassed that refusal.
