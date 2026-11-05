# Round 1 — Variant 2 Advocate (reviewer-2, qa, default model)

## Position summary
Variant 2 is the qa-lens card. Its strongest parts hold up: the third "Historical record" class is a necessary deviation, not drift (R2-F2); the plan only proves internal checkouts are unchanged, never that they still work (R2-F3); it rejects T1 F2 and F3 cleanly. Its coverage claim is wrong: `missing_requirements: []` misses scripts/eval_runner.py, and R2-F4 misquotes its evidence.

## Steelman
### Variant 1
Most thorough on correctness: the only card that flags pre-PR check 3 as well as check 1 (CLAUDE.md:66 "close it immediately and reopen" acts on an upstream PR). R1-2's correction is verified: POST-REFLECT-TASK.md:6 reads `status: "🔴 Blocked"`.
### Variant 3
The only finding that changes the plan's scope: scripts/eval_runner.py:138 builds `REPO_ROOT.parent / "IronClaude-eval-master"`, :143 runs `["git", "worktree", "add", ...]` as list arguments the plan :19 regex cannot match; no `worktree remove` in the file; fits none of the four exceptions at plan :57. R3-F4 and R3-F5 are real gaps.

## Strengths claimed
1. Correct class for the third class (R2-F2 necessary; Variant 1 agrees; Variant 3 never weighs it).
2. Exposes the vacuous AC at plan :135 and shows the tests are runnable (test_implement_retry_revert.py:613).
3. Clear T1 disputes: F3 is not a deviation at all (stricter than Variant 1's "authorized").
4. Coverage reported explicitly, which made its error checkable.

## Weaknesses identified in other variants
1. Variant 3 labels all six findings drift; R3-F4 is a safety gap; never assesses the third class.
2. Variant 3 misses check 3 (CLAUDE.md:66).
3. Variant 1's R1-3 is a labelling issue; plan :89 keeps the entry deliberately.
4. Variant 1 leaves the sc-pr-submit SKILL.md:267 tension as an inferred claim, not a finding.

## Concessions
- X-002: Variant 3 is right; `missing_requirements: []` is wrong.
- R2-F4 misquotes .gitignore:129 (real text: "(R3) Lookup-cache tracked artifacts — user-authorized exception (merged-requirements.md Gitignore Exception)"); the plan's constraint copies repo CLAUDE.md wording, so any staleness belongs there. Withdrawn or downgraded to informational.
- Did not raise C-001 at all.
- R2-F3's recommendation has the A-003 flaw.

## Shared assumption responses
- A-001: ACCEPT. Only tests/core/test_how_we_work_routing_table.py:352 reads root CLAUDE.md, for an `@HOW-WE-WORK` import (:355-356); other matches read core src/superclaude/core/CLAUDE.md (test_claude_md_routing_block.py:16, test_issue_body_templates.py:18). Hooks and primitives not searched.
- A-002: QUALIFY. Holds on this host (/home/coder/workspaces/worktrees/IronClaude/...); not checkable for every host; the kept `.dev/worktrees/` entry (plan :89) limits damage.
- A-003: QUALIFY. test_git_replay_integration.py:56-68 module-level skipif on shallow clones; test_implement_retry_revert.py:357 skips as root. A pass is evidence only if the AC requires zero skips (`-rs`).

## Per-point positions
| Point | Superior | Evidence |
|---|---|---|
| S-001 | 2 | Only explicit missing-requirements statement, checkable (and proven wrong) |
| S-002 | 1 | Uses necessary/authorized/drift; V3 all drift |
| S-003 | 1 | Engages all four T1 findings with verified corrections |
| C-001 | 1 | Covers CLAUDE.md:64 and :66 |
| C-002 | tie | All cite CLAUDE.md:251 and propose a grep AC |
| C-003 | 1 | Same class as V2 plus the verified Blocked status |
| C-004 | 2 | Same three files plus fixture evidence at :613; both lack a no-skip guard |
| C-005 | 2 | "Interacted with" literally covers fetch and pull |
| X-001 | 2 | Plan :73 "no ... link ... that resolves to it"; :251 is such a link |
| X-002 | 3 | eval_runner.py:143 list arguments, no worktree remove |
| A-001 | tie | All silent; check supports the assumption |
| A-002 | tie | All accept; holds on this host only |
| A-003 | 3 | V3 makes no claim depending on it; V1/V2 ignore the skip at :56 |
