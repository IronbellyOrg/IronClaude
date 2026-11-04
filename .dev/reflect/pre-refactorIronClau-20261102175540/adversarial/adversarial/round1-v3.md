# Round 1 — Variant 3 Advocate (reviewer-3, refactorer, default model)

## Position summary
Variant 3 is the only review that finds a real gap in coverage the spec's search cannot see: scripts/eval_runner.py:143 runs `["git", "worktree", "add", str(worktree_path), "master"]` and never removes that worktree. It also has the best-grounded findings on what the plan's tests and Orca flags cover. Weak points: all six findings labelled "drift"; narrower than Variant 1 on the pre-PR checks.

## Steelman
### Variant 1
Most complete reading of the fork-rule contradiction: check 3 at CLAUDE.md:66 ("close it immediately and reopen") is itself an action on upstream, which Variant 3 missed. Widest classification range. Confirmed POST-REFLECT-TASK.md:6 `status: "🔴 Blocked"`, correcting plan line 37. U-007 catches a bare `gh repo view` outside the hit set.
### Variant 2
Clearest structure: the explicit `missing_requirements` section is the right place for a coverage verdict. Its dispute of T1 F3 is the most faithful reading of source.md:1.

## Strengths claimed
1. U-001 / X-002: eval_runner.py:138 path `REPO_ROOT.parent / "IronClaude-eval-master"`; :143 list arguments the plan :19 regex cannot match; no "remove" in the file; none of the four exceptions at plan :57 covers it.
2. U-003: tests/skills/test_sc_recommend_routing_contract.py:27, 29, 130 reads all three Task 5 files; plan :116 does not run it.
3. U-004: sc-post-release-protocol/SKILL.md:91 offers a `git worktree add` / `git archive` checkout with no location or removal; fails plan :57 although plan :36 classes it internal.
4. U-002: plan :23 confirmed list lacks `--json`, `--issue`, `--pr`; plan :54, :56, :76 write them; only `orca worktree rm` gets a `--help` check (plan :58).

## Weaknesses identified in other variants
1. Variant 2's `missing_requirements: []` is disproved by eval_runner.py:143.
2. Variants 1 and 2 never question the grep as the full scope.
3. Variants 1 and 2 propose a test run that can pass vacuously: test_git_replay_integration.py:56-68 skips the module when pinned parent commits are missing.
4. Variant 2's R2-F4 misquotes .gitignore:129.
5. Variant 1's R1-6 calls the fetch/pull ban "authorized"; it is a literal reading, not a deviation.

## Concessions
- C-001: Variant 1 is better (covers CLAUDE.md:64 and :66).
- S-002: all-drift labelling is poor calibration; R3-F1 is a spec gap (source.md:1 puts the grep in parentheses and the plan follows it), R3-F4 a coverage gap.
- S-003: Variant 1's T1 disputes are broader and better reasoned.
- C-003, C-004: Variant 3 was silent; the others raised them correctly.

## Shared assumption responses
- A-001: QUALIFY. Only tests/core/test_how_we_work_routing_table.py:352 reads root CLAUDE.md, for an `@HOW-WE-WORK` import; other CLAUDE.md tests read src/superclaude/core/CLAUDE.md (test_claude_md_routing_block.py:16). Safe unless the new text adds an `@` import. Hooks not checked.
- A-002: QUALIFY. On this host Orca places worktrees outside the main checkout (/home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths); "every host" depends on Orca configuration nobody checked; Task 4 keeps .gitignore:242, limiting risk.
- A-003: REJECT as stated. test_git_replay_integration.py:56 skips the module on a shallow clone; test_implement_retry_revert.py:357 skips one test as root. The AC needs `-rs` and a zero-skip assertion.

## Per-point positions
| Point | Superior | Evidence |
|---|---|---|
| S-001 | 2 | missing_requirements section is the right structure |
| S-002 | 1 | Mixed labels fit the taxonomy |
| S-003 | 1 | Disputes F1-F4 with reasons |
| C-001 | 1 | Covers CLAUDE.md:66 as well as check 1 |
| C-002 | 1 | Concrete narrowing wording plus a verification artifact |
| C-003 | 1 | Cites POST-REFLECT-TASK.md:6 Blocked; V3 silent |
| C-004 | 1 | Named artifact (V2 equal in substance); both need a no-skip check |
| C-005 | 2 | source.md:1 covers fetch and pull literally |
| X-001 | 1 | "(gh, git or Orca)" at plan :73 qualifies "link", so the wording is ambiguous |
| X-002 | 3 | eval_runner.py:143 list arguments, no removal |
| A-001 | 3 | Only routing_table.py:352 reads root CLAUDE.md, for an import pattern |
| A-002 | tie | Unverified by every variant; true on this host |
| A-003 | 3 | skipif at test_git_replay_integration.py:56 makes a pass vacuous |

Note (advocate): on A-001..A-003 "3" means evidence gathered for this statement, not content in variant-3-original.md.
