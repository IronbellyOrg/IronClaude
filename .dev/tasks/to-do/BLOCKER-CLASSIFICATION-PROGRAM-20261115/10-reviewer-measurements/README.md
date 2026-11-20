# Reviewer measurements for stage 3c and the Broken plan check (2026-11-17 to 2026-11-20)

The short set of records kept when the worktree `brainstorm-reflect-panel` was closed (owner, 2026-11-20: "Safe short set of records"). These files are copies. Paths written inside them point at that worktree (`/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/...`), which no longer exists; the reviewer cards, briefs, variant files and run folders they name were not kept.

What was measured: reviewer-only runs of the reflect reviewer agent text on two invented throwaway specs, E (csv2jsonl) and B (wordcount). Arms: X = master plus the stage 3c passage; Y = X plus the run B session's "Weak check" (never landed); Z = X plus the "Broken plan check" bullet (landed with stage 3c in PR 688).

| Folder | Content |
|---|---|
| `scores/` | Rounds 1 and 2 (candidate passages, 3 reviewers per arm), round 3 (X against Y), round 4 (Z), the blind rescore of rounds 3 and 4, and the arm key |
| `blind/` | The two blind scorers' raw tables with evidence quotes, and the key that maps shuffled card names to arms |
| `designs/` | Design records: the Broken plan check brainstorm (merged requirements and diff), the carry-scope variant design (rejected), the Weak check wording study and its diff (reverted, never landed) |
| `run-b/` | Run B and its reruns (B-rerun, B-rerun2, wording tests), the 2026-11-18 rerun summary of runs B and E, and the severity debate ruling |
| `handoffs/` | Status files of the two other sessions in that worktree and the unified summary of all three sessions' work |

Headline (blind rescore, 4 cards per arm): spec E prefix and "no output written" X 4/4 and 4/4, Z 4/4 and 3/4; spec B `tokenize.py` clash X 0/4, Y 4/4, Z 3/4; Blocking rows per card E X 4.0, Y 6.0, Z 3.25 and B X 1.75, Y 3.5, Z 2.0; ties sorted before the top-N cut raised by no arm (left unsolved this release by owner decision).
