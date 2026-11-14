# Proposal C: keep both programs, but write nothing yet; decide the relationship after PR #539 merges and the real ids are compared

## Answer

Keep both programs as they are, record "keep both, provisional" in the ledger, and defer any contract note, panel or merge until PR #539 has merged and the one real-id comparison between the observer and the sweep (XC-04) has run. Then decide with evidence.

## What happens next if the owner picks it

1. The ledger records the provisional answer with its date and the trigger "after #539 merges and XC-04 is recorded".
2. XC-05 (draft note) and XC-07 (land note) are held; nothing else waits on them except the texts that cite the note (the Coder#477 status record, the v2 field list, the #409 mapping table), which use plain descriptions of each program instead of the note's names.
3. When the trigger fires, the question is asked again with the comparison result and the merged sweep in hand.

## What it unlocks

- No document is written against a moving target: PR #539 still has two unresolved review threads and an open security ruling (Q1), so the sweep's constants, verbs and wording may change before merge.
- The decision is made after the one fact the debate could not establish: whether the observer's dispatch ids match the sweep's row ids on a real Run.
- Saves the cost of a note, a comparison test and a link PR if the owner later prefers a panel or a merge.

## What it costs or risks

- The confusion stays: two "v1" files, three vocabularies, two allow-lists that disagree on one command, and no written rule for either program's changes (ADJ Part 1.1).
- Three other planned texts lose the shared names they were going to cite; they must be reworded later.
- The debate called the note "the main product of the debate" (ADJ Part 2.3); deferring it delays the one agreed outcome.
- The draft (XC-05) could have been written now on a master-based branch at low cost; only its landing waits for #539.

## What stays unresolved

- The relationship itself, until the trigger.
- Q9 and Q17.
