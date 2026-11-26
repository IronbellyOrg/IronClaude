# /sc:analyze report: src/superclaude/cli/issue_pipeline (architecture, quick)

Command: /sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/3/analyze
Master: f2894fc44 (2026-11-24). Worktree: /home/coder/workspaces/worktrees/IronClaude/Realign
Codegraph: index_state=fresh, checked_at=2026-11-24T22:14:56Z; degraded: graph:empty (build_brief lookup returned no symbol; the real name is `build`)

## Scope and layout
Ten Python files, 2122 lines, one Click group `issue-pipeline` (cli.py:62-409, 11 verbs), plus one template `templates/worker-brief.txt`.
- Stores: `approval_record.py` (416 lines): locked, write-ahead rows; adoption states `reserved|started|uncertain` (`ADOPTION_STATES`, :44), approval states `recorded|instructed|acked|revoked` (:45). Verbs `adopt-create` (cli.py:109), `adopt-mark` (:118).
- Reads: `reads.py`, `stage_predicates.py`, `approval_line.py`, `plan_hash.py`: GitHub text turned into booleans inside jq; no GitHub text is kept.
- Brief: `brief.py` (80 lines) builds the worker brief from closed slots (issue number, stage word, route, nonce); `brief.py:1-10` states "No issue text can reach the brief".
- Writer: `complete.py` is the only module that writes to GitHub (GraphQL `updateProjectV2ItemFieldValue` at :124, `gh api` calls at :230, :322, :393, :416).

## Findings
1. MEDIUM, architecture: `brief.build` has no production caller and no CLI verb. `codegraph_node` on brief.py lists only `tests/issue_pipeline/test_brief.py` and `tests/hooks/test_launch_level_guard_worker.py` as users; `codegraph_impact build` reaches 18 symbols, all tests; cli.py has no `brief` command (verb list above). `WORKER-CONTRACT.md:297` says the brief is "built by `superclaude.cli.issue_pipeline.brief`". So how the coordinator reaches the builder is UNVERIFIED. Bears on #790 (template work) and #788 (start step).
2. MEDIUM, architecture: the adoption record is the owner-built store (PR #584), 12 callers (`codegraph_callers adopt_create`: 1 production, `cli.py:113`; 11 tests). It stores the Dispatch id in the adoption row (`adopt_mark`, approval_record.py:268). No `body_sha` anywhere in `src/superclaude/cli` (Grep for `body_sha`: none) and no `issues/<repo-key>__<N>.json` writer. Bears on #788 and #789.
3. LOW, boundary: the package keeps the "no GitHub text" rule in three places: brief.py:1-10, reads.py (body "never leaves jq"), approval_record.py docstring. A hash of the issue body (#789) fits the rule only if a script computes it; a 64-hex value matches `_HASH` (approval_record.py:40).
4. LOW, boundary: no Fixes/Refs or secrets sentence exists in `templates/worker-brief.txt` (31 lines) or in the package (Grep for `secret|token|credential`, case-insensitive: no match). The only PR-text writing place is the `submit` block of `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md` (step 4, `/sc:pr-submit --monitor 3 ... --body "..."`). Bears on #790.
5. INFO: Orca flags checked against the installed Orca by `--help` only: `worker-start (--task | --spec)` and `--retry-request` exist; `request-show --request <id>` exists and is read-only; `orca reference add|find|list|remove` exist (add takes full URLs plus `--worktree`); `worktree ps [--agent-wait]` exists. No run was made.

## Recommendations
- Read-only run: no source file was modified, nothing was committed, staged or pushed.
- Reuse the adoption row and the existing `brief.py` as the base for the three items; do not add a second record or a second template store (findings 1 and 2).
- Before any of the three items is built, decide how the coordinator invokes the brief builder (finding 1).
