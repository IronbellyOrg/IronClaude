# Summary of the throwaway re-runs B and E (2026-11-18)

Written by the coordinator (ORCH-IronClaude) from the two worker records. Throwaway invented material. The owner decides; nothing here is a stage 4 decision.

Records:
- B: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/rerun-20261118/B/RERUN-RECORD.md
- E: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/rerun-20261118/E/RERUN-RECORD.md

Setup that held: the installed reviewer agent /home/coder/.claude/agents/reflect-reviewer.md was byte-identical to master before both runs (`diff` printed nothing). The workers say no brief carried the severity rule. A, C and D never use the reflect reviewer (0 mentions in their records), so they were not re-run.

## Table

Old grades are from the first runs' records. "Reviewer cards" means the three reviewers' own deviation rows. Both runs ended FAIL.

| Run | Old finding | Old grade | New grade on the reviewer cards | New grade on the merged card |
|---|---|---|---|---|
| B | M6: the plan does not say ties are sorted before the top-N cut | Medium on the old merged card (Blocking only after the later debate) | Blocking (Decision) on 1 of 3 cards (reviewer 3); not raised by the other two | Blocking (Decision), finding B4 |
| B | B2: no task creates the `wordcount` command | Blocking on the old merged card (not Medium) | Split: Blocking (Missing) on reviewer 3, Medium on reviewer 1, "no defect" on reviewer 2 | Blocking (Missing), finding B2 |
| E | M2: the plan never states the `csv2jsonl:` message prefix | Blocking | Medium on 2 cards; not raised by reviewer 2 | Medium (M-03) |
| E | M4: "no output written" on unreadable input | Blocking | Medium on 2 cards; Blocking (Missing) on reviewer 2 | Medium (M-02) |
| E | M1: no task owns the JSON Lines writer | Blocking | Blocking (Missing) on all 3 cards | Blocking (Missing) (M-01) |

Rows E-M3 (exit 0 on success): old Blocking (contested), new Note on the merged card. Old M6 and B2 belong to run B only; run E has a different, unrelated "M6" (error hand-off), which stayed Medium.

## What the numbers say

- Grade words: all 13 reviewer rows in B and all 20 in E start with one of the five allowed grade words (0 rows without).
- B merged card: 8 Blocking, 7 Medium, 1 Note. E merged card: 1 Blocking, 5 Medium, 3 Notes.
- Severity column still disagrees with the grade: reviewer 2 in both runs writes Blocking in the cell and MEDIUM in the column.

## Limits of this test (read before trusting it)

1. Run B is contaminated. The worker created its own record file before the reviewers ran, and that file already named old M6 and old B2. Reviewer 3 and the merge agent read it. Their Blocking grades on those two findings may come from that hint, not from the agent file. Reviewer 1, which did not read it, graded B2 Medium. I did not forbid this in the brief, so it is my gap.
2. The prompt said two real blockers (M6 and B2) were labelled Medium. The old B record says B2 was Blocking on the old merged card; only M6 was Medium there.
3. Reviewer 2 ran on `gpt-6.1-sol` in both runs, not the model the alias names. In B the merge ran on one model family (opus).
4. Run E's first merge stalled for about 3 hours; the worker re-spawned it once. The second merge ran with background advocates and the contract says `partial`, `fallback_mode: true`; the merge agent did several rounds itself.
5. In E the plan header still points at the old run's folder (a copy artifact); three reviewers noticed.
6. Every count above is the workers' own. I did not recheck any grade.

## Workers' own judgment of wrong grades (not mine)

- B: B6 and B8 look over-graded (Medium or Note); B3 is weakly evidenced; S3 stayed Medium although its own reason names an acceptance check, which looks Blocking-shaped.
- E: M-03 and M-02 look under-graded: each names an acceptance check that fixing it would change, which is the rule's Decision test. The old E run graded both Blocking.

## RT1 reading (the coordinator's reading only; the owner decides)

RT1 would trip. In run E, two findings the old run called Blocking (M-03, the message prefix, and M-02, "no output written") sit in the new Medium list, and the worker's reading of the rule says each looks decision-changing. Run B's old M6 is no longer in a Medium list (it is Blocking on the merged card), but that result is weakened by the contamination above, and S3 in B has the same shape as the E findings.

(This reading is replaced by the section below, which uses the clean B run.)

## Clean B re-run (added 2026-11-18, after "Yes" to a clean second run of B)

Record: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/rerun-20261118/B-clean/RERUN-RECORD.md . Same spec and plan, same command, same agent file (identical to master). The worker kept notes about the old findings outside the repo and wrote its record last. It checked all 18 agent tool logs for reads of earlier runs' folders: 0 reads, so the run is clean (the check covers tool-call fields only).

| Old finding | Old grade | New grade on the reviewer cards | New grade on the merged card |
|---|---|---|---|
| B-M6: ties are not sorted before the top-N cut | Medium on the old merged card; the owner then ruled it a real blocker | Not raised by any of the three reviewers | Not raised. Only the debate's fault-finder noted it (INV-007), graded MEDIUM, and the merge left it out of the merged card on purpose |
| B-B2: no task creates the `wordcount` command | Blocking on the old merged card | Medium (reviewer 1), Blocking (Missing) (reviewer 3), not raised (reviewer 2) | Blocking (Missing) |

Merged verdict FAIL: 4 Blocking, 2 Medium, 5 Notes. All 17 reviewer rows start with a grade word. Reviewer 2 gave PASS with 0 findings (and ran on `gpt-6.1-sol`); the debate made it withdraw the PASS.

Also in this run (the worker's own reading): the tie-rule wording finding (plan line 15 drops "plain codepoint order") is Medium on the merged card although reviewer 3 graded it Blocking and the old run graded the same defect Blocking. The worker says it names an acceptance check, which reads as Blocking. Six findings from the fault-finder (INV-001, 003, 007, 008, 010, 014) are in no card at all.

Limits: the merge stayed `partial` (a high-severity invariant unaddressed because standard depth has no third round), reviewers and merge agents were all Anthropic models except reviewer 2, and I did not recheck any grade.

## RT1 reading, replaced (the coordinator's reading only; the owner decides)

RT1 would trip, on both runs. The one finding the owner ruled a real blocker (B-M6, the tie order before the cut) is, in a clean run, raised by no reviewer, absent from the merged card, and recorded only as a MEDIUM warning from the debate's fault-finder. That is a real blocker sitting in a Medium list, which is what the check looks for. In run E, two findings the old run called Blocking (M-03, M-02) sit in the Medium list, and the worker's reading says each names an acceptance check.
