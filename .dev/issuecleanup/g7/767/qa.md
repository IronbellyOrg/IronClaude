VERDICT: PASS

# QA of findings.md for issue 767

## Blocking defects

None.

## What I checked (all re-read live, not taken from findings.md)

- Live issue 767: OPEN, no labels, no comments, `closedByPullRequestsReferences` empty, updatedAt 2026-11-24T17:22:39Z. Body matches what findings.md says (WORKER-CONTRACT 288-290, SKILL 23-26, report.py 327-349 and 405-439, 816 unknown rows, 13 chunks, 16 compactions, 22m07s total, "no crash, data loss or stall asserted", "Done when" has a synthetic 800-row regression and a before/after measure).
- `src/superclaude/skills/sc-sweep-protocol/SKILL.md:25`: the Read-in-chunks-of-150-lines-until-`Report complete` rule is there, as cited.
- `src/superclaude/cli/sweep/report.py`: `Report complete` is on line 542; `_could_not_determine` is at 327-350; `_sessions` is at 405-443; `render` is at 608 and joins all 12 `SECTIONS`. `SECTIONS` holds both `_could_not_determine` and `_sessions`. `_sessions` filters out only the idle class, so unknown rows are in both. The duplication claim is true.
- `src/superclaude/cli/sweep/commands.py:219-241`: only `--run`, `--window`, `--root` and `--output`. No size, summary or limit option. True. A grep for budget/limit finds only the probe `Budget`, not an output budget.
- `src/superclaude/core/WORKER-CONTRACT.md:290` (WC-16): runs `/sc:sweep` and reads its report on each wake or wait timeout, at most once every 5 minutes. True. The issue's `~/.claude/...:288-290` is the installed copy; 288 is the heading.
- `tests/sweep/test_report.py:1027` is the show-cap line. The grep of `tests/sweep` found no test of report size or a size budget (only `> 40` lines at 1456 and `len(SECTIONS) == 12`). True.
- History: `git log` on `src/superclaude/cli/sweep` and `tests/sweep` shows only b46ecc1bd (#579) and 4d3c0b126 (#539). `git log --grep=767` is empty. `gh pr list --state all --search 767` is empty. Searches for "766" and open "sweep" PRs are empty. "No PR or commit addresses 767" holds.
- PRs: 539 merged (merge commit 4d3c0b126, 2026-11-14), 579 merged (b46ecc1bd, 2026-11-17), 708 merged (docs for #409, 2026-11-20). All as described. Findings.md names no PR 766 (it is an issue); no error there.
- Issues: 766 open, bug, "Read workers show as Could not Determine". 574 and 575 closed, COMPLETED (findings said 575's reason was not read; it is COMPLETED, which is consistent with "closed evaluations"). 339, 409, 423 open enhancements with the stated themes. 755 open, "Coordinator created multiple Orca Runs by default..." (findings marks relevance UNVERIFIED; fair).
- Complexity medium, size M, priority P2, the five next steps and the dependencies (no hard blocker, 766 soft, blocks nothing) are consistent with the evidence. The issue itself asserts no crash, data loss or stall, which supports P2. The UNVERIFIED flags on private-session numbers and the compaction root cause are correctly applied.

## Notes (not blocking)

1. `_sessions` ends at line 443, not 445; trivial range slip.
2. The "two documents" for the rule to change omit a third restatement: `src/superclaude/core/HOW-WE-WORK.md:360` repeats the every-wake `/sc:sweep` duty, and the `/sc:sweep` command file (`~/.claude/commands/sc/sweep.md`) probably does too. Step 3 should list these (findings.md hints at "HOW-WE-WORK-style copies if tests require"). It does not change size M or any step's direction.
3. `.claude/skills/sc-sweep-protocol` does not exist in this checkout, so `make sync-dev` is needed before the local mirror exists. This is consistent with step 3.
4. Findings.md calls 574/575 "evaluations of compaction and tool-output pruning". The titles say "Install and evaluate fast-jev compaction" and "jev-pruner", so this reading is fine.
