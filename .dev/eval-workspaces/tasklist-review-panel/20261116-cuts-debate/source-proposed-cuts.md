# Proposed cuts (source for the adversarial debate, 2026-11-16)

Context for a reader with no history: an evaluation of how to make a panel of cheap AI reviewer models find more real defects in implementation plans (folder `.dev/eval-workspaces/tasklist-review-panel/`, branch `ironbelly/eval-tasklist-review-panel`, fork `origin` only). Background and glossary: `OPEN-QUESTIONS-20261115.md`. The cuts below come from `TRIAGE-20261116.md`, which was made from two read-only audit agents (their claims were not independently re-verified). Facts to weigh:

- Recipe Ledger (RL) is the only design with a repeatable lead: 2.00 of 14 known defects per replicate against 0.67 for the plain panel (9 replicates, study packages only, exploratory, never frozen). It is 1.46x and 1.60x slower on two packages (cap 1.35) and passes its format check only with owner-approved allowances (strict reading fails 47 of 81 reports).
- A second session is RIGHT NOW running a frozen hold-out comparison of RL against the plain panel in `20261116-holdout/` using the RL code in `20261114-recipe-ledger/`. Its hold-out answer-author session is running. That RL code must not be changed under it.
- Owner decisions of 2026-11-16: model-usage infractions warn and are reported, never halt work; `/sc:workflow` and `/sc:implement` are the current workflow; `/sc:task` and task-builder are to be retired; only the Sprint run CLI suite is to be evaluated.
- Standing owner rules: keep intermediate files (rename or archive, never delete); no push without an order; Opus only for blind judging; at most 2 `claude` sessions at once.
- Size: Recipe Ledger folder 728 tracked files, about 19,500 lines of scripts (9,797 of them tests); Sweep Sheet folder 595 files, about 24,600 lines (stopped); collaboration folder `20261113-collab/` 1,620 files, about 24,400 lines (stopped).

## The cuts

| ID | Proposed cut | Kind | Claimed gain | Claimed risk |
|---|---|---|---|---|
| C1 | Remove from the master open-question and open-decision lists everything void or settled (all Sweep Sheet freeze, parity and control items; hold-out author and list now owned by RL; "3 tests each"; recipe review by a session; push policy; the 1.83 baseline; foreign scripts; host fault); mark deferred the severity change | Documentation edit | Readers see only what needs an answer | A dropped item was still needed; history lost |
| C2 | Replace the model-policy hook's 11-restriction decision list and 63-requirement plan with the smallest version: a 10-line policy file, one `superclaude model-report` command that scans output JSON and transcripts for restricted model ids, always exits 0, appends an incident log; keep the old design as history | Documentation edit (plus later a small build) | About 45 of 63 requirements cut; matches the owner's warn-and-report decision | The scan misses a gateway that serves another model behind an id; later enforcement needs the cut parts again |
| C3 | Build the `model-report` command (about 200 lines) through `/sc:workflow` and `/sc:implement` | New code | Catches both Opus incidents after the fact | Cost of a new feature nobody has used; layout of output files not fully checked |
| C4 | In the RL folder, cut code that no real run used: pre-registration and gates (`analysis/analyze.py` about 450 lines), ablation, report writer, "ran" audit, freeze and order scripts, card review records, sibling-sync manifest, 291-line judge audit | Code removal (archive) | About 18,000 of 19,500 lines gone | Breaks the running hold-out session; the frozen comparison may need the gates and freeze scripts the RL session already planned to use |
| C5 | Cut the RL re-ask path (about 350 lines; fired in 1 of 81 runs) and the spikes code | Code removal | Less to maintain | Used by the running hold-out for the ember reviewer |
| C6 | Archive the stopped Sweep Sheet and collaboration folders (about 49,000 lines, 2,215 files) off the working branch | Repository move | Smaller branch, less noise | Loses easy access to the failed-gate evidence and test fixtures; the files are already pushed |
| C7 | Delete the three foreign scripts in `20261111-a1/tools/tmp-scripts/` | Deletion | Tidiness | They might be someone's; owner said keep intermediates |
| C8 | Cut the format allowances (the forgiveness rules) | Code removal | Honest strict gate | RL result depends on them (58% fail strict); would invalidate the running hold-out arm |
| C9 | Drop the unbuilt Sweep Sheet forgiveness plan package in `.dev/tasks/to-do/TASK-WF-addOwnerApproved-20261115-210227/` | Remove an unbuilt plan | One fewer orphan package | The plan was reviewed; archive step moves it to done/ only on a finished build |

Rule of the debate: a cut survives only if its risk is acceptable now, with evidence, given the running hold-out session and the owner rules above.
