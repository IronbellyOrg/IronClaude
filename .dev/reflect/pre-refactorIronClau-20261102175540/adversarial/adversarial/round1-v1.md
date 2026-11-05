# Round 1 — Variant 1 Advocate (reviewer-1, analyzer, default model)

## Position summary
Variant 1 is the most complete on the pre-PR contradiction. It is the only variant that covers both CLAUDE.md:64 and :66, and its deviation labels (necessary, authorized, drift) are the most precise. Variant 3 found the most important scope gap (scripts/eval_runner.py), and Variant 1 concedes that point to it.

## Steelman
### Variant 2
Its strongest argument is R2-F3. It cites tests/skills/test_implement_retry_revert.py:613 to show the fixtures are self-contained, and argues that an acceptance check for "unchanged" cannot tell a working checkout from a broken one. Its `missing_requirements` justification (every spec span maps to INF-001..INF-011) is the only explicit coverage audit of the three. Its reading of F3 is also sound: "interacted with" covers fetch and pull, so that is not a deviation.
### Variant 3
Its strongest argument is R3-F1, verified: scripts/eval_runner.py:143 runs `["git", "worktree", "add", str(worktree_path), "master"]` into `REPO_ROOT.parent / "IronClaude-eval-master"` (:138). Nothing in lines 136-162 removes it. The plan's regex (plan:19) cannot match list arguments, so the plan's goal (plan:15) fails silently. R3-F3 (unchecked `--json`/`--issue`/`--pr` flags against plan:23) and R3-F4 (contract test not run) are real and backed by evidence.

## Strengths claimed
1. Full coverage of C-001: CLAUDE.md:64 runs an unqualified `gh repo view`; CLAUDE.md:66 says "close it immediately", an action on an upstream PR. Plan line 73 bans any "tool call ... that resolves to it", and plan:78 names neither line. Variant 3 names check 1 only. Variant 1's acceptance check (`grep -n 'close it immediately'` prints nothing) catches it.
2. Precise deviation classes: R1-2 necessary deviation plus the Blocked status (POST-REFLECT-TASK.md:6); R1-6 authorized (MEMORY.md entry). Variant 3 labels all six findings drift.
3. R1-3: plan:35 classes .gitignore as "rewrite to Orca's default location", plan:89 keeps the entry.
4. Reproduced hit set: 108 hits in 17 files (confirms the plan's grep output, not the spec's full scope).
5. U-007: sc-pr-submit-protocol/SKILL.md:267 bare `gh repo view` fallback, the same problem as C-001 in an installed primitive.

## Weaknesses identified in other variants
1. Variant 2 misses C-001 entirely.
2. Variant 2's `missing_requirements: []` is wrong because eval_runner.py:143 is in the spec's "every tracked file" scope; R2-F4 misquotes .gitignore:129.
3. Variant 3's C-001 fix is partial: its AC passes with "close it immediately" still at :66, and it relies on an unchecked `gh repo set-default --view`.
4. Variant 3 classes every finding as drift; R3-F4 is a coverage gap, not drift.

## Concessions
- X-002 goes to Variant 3: "matched 108 hits" proves the grep output, not the spec's scope.
- R1-4's proof can pass vacuously: test_git_replay_integration.py:56-68 skips the module when replay commits are missing (shallow clone); test_implement_retry_revert.py:357 skips under root. The AC must require zero skips (`-rs`, assert no SKIPPED).
- R1-5's "ambiguous" call on X-001 is weaker: plan:73 says "no tool call or link", and the plain reading includes a markdown URL.
- Missed R3-F3, R3-F4 and R3-F5.

## Shared assumption responses
- A-001: QUALIFY. The only test that reads root CLAUDE.md is tests/core/test_how_we_work_routing_table.py:352 (checks only for an `@HOW-WE-WORK` import). No test pins "PR Target = Fork" or "Parallel Development with Git Worktrees" (grep finds only CLAUDE.md:39 and :295); no hook or settings entry matches. Safe; name that test as the guard.
- A-002: QUALIFY. On this host the Orca worktree is at /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths, outside the main checkout; not shown for every host. Task 4's comment should say "by default".
- A-003: REJECT. test_git_replay_integration.py:56 skips the module on a shallow clone; test_implement_retry_revert.py:357 skips as root. The AC must assert no skips.

## Per-point positions
| Point | Superior | Evidence |
|---|---|---|
| S-001 | 2 | Only explicit missing-requirements audit, even though its result was wrong |
| S-002 | 1 | Mixed labels match the taxonomy; R1-6 authorized backed by MEMORY.md |
| S-003 | 1 | Addresses all four T1 findings with evidence incl. POST-REFLECT-TASK.md:6 Blocked |
| C-001 | 1 | Covers CLAUDE.md:64 and :66; Variant 3 leaves the :66 upstream close |
| C-002 | tie | All three require a decision on CLAUDE.md:251 with a grep check |
| C-003 | 1 | Same class as Variant 2 plus the Blocked-status correction |
| C-004 | 1 | Names all three tests and an artifact path; needs no-skip assertion |
| C-005 | 2 | "Interacted with" literally covers fetch and pull |
| X-001 | 2 | Plan:73 "no tool call or link" — static URL contradicts it |
| X-002 | 3 | eval_runner.py:143 list-argument worktree add, no removal (:136-162) |
| A-001 | 1 | Only test_how_we_work_routing_table.py:352 reads root CLAUDE.md, for @-imports only |
| A-002 | tie | This host confirms outside-checkout; no variant checked other hosts |
| A-003 | 3 | test_git_replay_integration.py:56 skips on shallow clones, undercutting V1/V2 |
