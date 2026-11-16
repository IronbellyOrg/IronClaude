# Severity-rule test: pre-registration (written 2026-11-16, before any run)

**Context for a reader with no history.** The "Review Panel" has cheap reviewer models report plan defects; a report marks some findings "blocking", which fails the review and triggers a fix. Too many blocking findings are wrong (they match no real defect). In a frozen hold-out comparison of a redesign (Recipe Ledger, `../20261116-holdout/RESULTS-HOLDOUT-20261116.md`) the only consistent benefit was fewer wrong blockers (0.50 per run against 0.95 for the control), with a higher share of blocking findings that hit a real defect (precision 0.44 against 0.27), at about 40% more time. This test asks whether a single cheap change, a narrower wording of the "contradiction" blocking clause in the reviewer's brief (the owner-approved wording of `../20261114-severity/PLAN.md`), gives that benefit alone, without recipes and without extra time. Background and open questions: `../OPEN-DECISIONS-20261115.md`.

## Arms

- **Z0:** the control brief exactly as used in the hold-out comparison (harness copy `harness-z0/`, byte-identical to the Recipe Ledger folder's `briefs/` and code at the time of copying).
- **S:** the same harness (`harness-s/`) with ONE change: in `briefs/base.txt` the sentence "Blocking needs a sentence that holds with no further assumption: two stated texts that contradict each other, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion cannot pass." is replaced by a version whose first cause requires that the contradiction "would, with high probability, change what ships" of a named final deliverable, and that a contradiction confined to text no deliverable reads or acts on is Medium. The data-loss, security/safety and unpassable-criterion causes are unchanged. The diff is the only difference between the two harness folders (`diff -rq` shows `briefs/base.txt` alone).

## Design

- Documents: HO-2, HO-3, HX-1, HX-3 (the hold-out plans and ground truth of the earlier comparison, `../20261114-recipe-ledger/holdout-gt/`). **Reuse disclosure:** these documents and their ground truth were already used once, for Recipe Ledger; they are not untouched for this test. The test is a different intervention on the same documents; no lever was tuned on their ground truth.
- 5 replicates x 4 documents x 2 arms = 40 panel runs, ember panel (`muse-ember-1.0` + 2x `gpt-6-luna`), block-randomised (one block per replicate, order shuffled with a recorded seed), one panel at a time, no fallback model, one lock slot (`with-slot.sh`), own sandbox root `/tmp/evalsb-sev`, sandbox rebuilt when a run leaves files.
- Judging: blind Opus judge for every run (arm marker removed by the anonymiser), a second judge on a 15% sample. Opus is used for nothing else.
- Same-day Z0 runs are made new (the 20 Z0 runs of the earlier comparison are NOT pooled; they may be shown as context).

## Gates (all five must pass for "adopt-candidate"; written before any run)

| Gate | Rule |
|---|---|
| G1 wrong blockers | S's wrong blockers per run at most 0.70 x Z0's (a 30% cut) |
| G2 real blockers kept | total blocking rows matching a real defect (all runs) for S at least Z0's |
| G3 recall kept | S's found fraction at least Z0's minus 0.02 |
| G4 time | pooled median panel time of S at most 1.10 x Z0's |
| G5 | (descriptive, no pass/fail) blocking rows per run, blocking precision, rows per run, per-document breakdown, and a bootstrap 90% interval (documents, then runs) for the wrong-blocker difference |

Decision text: "adopt-candidate" if G1 to G4 pass, else "do not adopt". An adopt-candidate is not an adoption: it would still need a check on documents outside this set and the owner's approval before any product file changes. The product files are NOT changed by this test.

## Pre-registered limits

One panel (ember); plans only; 36 ground-truth items, 10 blocking, two documents with none; ground truth written by a model session; a gateway slot is shared with another session's schedule running at the same time, which affects both arms alike (interleaved blocks) but widens the time measurement; the 5 per arm per document sample is small, so G2 is a floor, not proof.

## Method notes

Code for the schedule (`make-schedule.py`), the driver (`driver.sh`) and the analysis (`analyze_s.py`) are in this folder and are fixed by the commit that contains this file. Raw run folders and judge transcripts are not committed.
