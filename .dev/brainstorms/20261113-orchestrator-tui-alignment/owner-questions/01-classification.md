# Classification of the 33 owner questions

Written 2026-11-14 by the orchestrating session. Inputs: each question's quick three-way debate (`Q<nn>/final.md`, record in `Q<nn>/adversarial/`) and its rating block. The three-way debates all ran spawned advocate agents (`fallback_mode: false` for every question that reported it). Q1 part (a) was answered by the owner ("fix") on 2026-11-13 (`owner-answers.md`).

## The rule I applied

A question is **accepted for the agent's recommendation** only if all of these hold. Otherwise it goes to the owner.

1. The recommended answer grants no authority and accepts no risk in writing.
2. It is easy to undo.
3. It affects only this program (no other repo's issue text, no other people).
4. It needs none of the owner's own intent, taste or knowledge.
5. The debate converged (3 of 3, or a clear majority with no split on the points).
6. Security stakes are none or low, or the answer is the restrictive one that leaves the safe default in place.

I did not follow the workers' own suggestion blindly: it is advisory. I overrode three: Q6 (suggested safe, I accept only half), Q32 and Q18 (suggested human, accepted because the recommendation only keeps the default and grants nothing).

## Result: 12 accepted, 21 to the owner

| Q | Topic in plain words | Debate result | Why it matters | Call |
|---|---|---|---|---|
| Q1 | The sweep's git-config hole (INV-008): which fix shape, and how many routes | re-run after your "fix" answer: refuse and report `unscanned`, counting only programs that could actually run, all six routes; 60%; 3 of 3 | security high; accepts or rejects a risk; costly after merge; blocks the #539 merge and most later work | **OWNER** (part (a) already answered "fix") |
| Q2 | Watcher claim level, and accepting in writing that the first test session runs with permission checks off | C, 72%, converged | security high; written risk acceptance | **OWNER** |
| Q3 | Coder#477: keep, narrow or close | A, 55%, converged on points | rewrites an issue in another repo; your intent | **OWNER** |
| Q4 | What "TUI Panel" meant in your comment | merged B/A, 64% | only you know what you meant | **OWNER** (quick) |
| Q5 | Keep both programs with one contract note, or merge | B, 75%, converged | reversible; provisional; low cost | **ACCEPTED** |
| Q6 | When to switch on the observer's questions panel, and its scope | C, 67%, converged | accepted half: do not switch on before the seeded test (restrictive, equals the default). The scope sentence stays yours and returns later | **ACCEPTED (half)** |
| Q7 | Will you write the pass record and commit or archive the records that exist only in a sibling worktree | B+A+C, 65% | needs your own action and knowledge; written record of your decision | **OWNER** |
| Q8 | Will you write the dated direction-selection record | C extended, 68% | only you can write it | **OWNER** |
| Q9 | Store the sweep JSON, capture from stdout, or neither | A, 73%, converged | restrictive: not now; reversible | **ACCEPTED** |
| Q10 | May the sweep read Orca messages | C amended, 73%, converged | restrictive: the observer's alone for now; allow-list unchanged; wording fix happens after #539 merges | **ACCEPTED** |
| Q11 | What the "static report in chat" is | B, 85%, converged | tiny, reversible | **ACCEPTED** |
| Q12 | A routing-guide row for the observer | C, 78%, converged | tiny, reversible, own small PR after #539 | **ACCEPTED** |
| Q13 | Is bare `orca` acceptable for the observer | A, 72%, converged | low, but it is a written acceptance of a known (small) risk, so I leave it to you | **OWNER** (quick) |
| Q14 | What "#339 is complete" means for #423's gate | C, 80%, converged | your roadmap; cost medium | **OWNER** |
| Q15 | May v2 ever send corrections to non-worker sessions | B, 82%, converged | "report only" is the restrictive answer, but it fixes the scope of the proactive orchestrator you described, so it is your product call | **OWNER** |
| Q16 | One trust design, or one grant vocabulary and audit format | C, 70%, converged | security high; reaches other repos | **OWNER** |
| Q17 | Should the observer ever show sweep facts | B, 65%, converged | restrictive: not now, written re-ask trigger | **ACCEPTED** |
| Q18 | Copy the observer snapshot to the TUIBBS machine | A, 70%, converged | restrictive: not yet; the default already does this; the later Coder#477 post is a separate grant | **ACCEPTED** |
| Q19 | Which of the reviewer's four asks comes first | C direction + A, 55%, **split** | your priorities | **OWNER** |
| Q20 | Who owns the watcher's agent, and up to 6 unreviewed sessions a day | B, 70%, converged | security high; names a person; accepts a risk | **OWNER** |
| Q21 | May the sweep label machine-started sessions (Phase 2, after the first live test) | B, 78%, converged | reversible, internal, with a stop rule | **ACCEPTED** |
| Q22 | How old a snapshot or record must be to count as stale | A (a rule giving about 75 s), 70% | your number; the text lands in another repo's issue | **OWNER** (quick) |
| Q23 | Is a "reclaimable" worker live, historical, or its own state | C, 75%, converged | internal wording; reversible | **ACCEPTED** |
| Q24 | Who runs the shared read-only Orca capture and the id comparison | A, 65%, converged | live Orca work; you name the actor | **OWNER** |
| Q25 | Who runs `/sc:pr-submit --monitor 3` for each program PR | A, 55%, **split** | security high; authority; costly | **OWNER** |
| Q26 | Where the coordinator runs and which branch holds its ledger | A, 60%, **split** | decides your main checkout's branch; authority | **OWNER** |
| Q27 | May SW-02's own plan package be committed in PR #539 | C, 88%, converged | a verified tool rule decides it (the plan executor only runs a plan in the same checkout); undone by dropping a few plan files before the merge. Note: the spec's default for this question cannot run, which is why the recommendation is yes | **ACCEPTED** |
| Q28 | What `/sc:pr-submit` may do on PR #539 | A amended, 55%, **split** | security high; costly | **OWNER** |
| Q29 | How this host's `superclaude` CLI gets the sweep command | B amended, 70% | removing a shadowing install under `~/.local` needs your approval | **OWNER** |
| Q30 | Which disposable coordinator Run the live-layout test may read; accepting that its questions may be consumed | C amended, 85%, converged | written risk acceptance | **OWNER** |
| Q31 | Does your 2026-11-05 recurring-check order apply to this coordinator | C, 70%, converged | only you know | **OWNER** (quick) |
| Q32 | May helper sessions make their own local commit | B, 65%, converged | recommended answer is "no", equals the default, grants nothing | **ACCEPTED** (override of the worker's suggestion) |
| Q33 | Which session is the author of PR #539's changes and pushes | A, 55%, **split** | security-relevant authority; nothing records who owns the checkout | **OWNER** |

## Why Q22, Q27 and Q18 were close calls

- **Q22** looks like a tunable, but the spec reserves it as "your number" and the answer is posted to another repo's issue, so it stays with you as a quick confirm.
- **Q27** adds files to a contested PR. I accepted it because the plan executor only runs a plan that sits in the same checkout as its code, every other placement fails or needs heavier machinery, and the commit and push still need their own grants and Q33.
- **Q18** is rated security high because copying the snapshot to another host is sensitive, but "not yet" does nothing and equals the default.

## What this classification does not change

- The 12 accepted answers are recorded as delegated, reversible, and carry no grants (`accepted-answers.md`).
- Q1 part (a) is your answer, not a delegation.
- Merged spec section 3 still lists the original recommended answers and defaults; where a debate refined an answer, the refinement is in `Q<nn>/final.md`.
