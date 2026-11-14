# Proposal A: one shared set of facts: the observer gets a panel that reads the sweep's output

## Answer

Make the sweep the single source of classified session facts, as the #409 issue body proposes: the observer keeps its Orca worker ledger, and adds an optional panel that shows the sweep's classifications by reading a captured copy of the sweep's JSON, never by running the sweep itself. A short contract note still records both formats.

## What happens next if the owner picks it

1. The owner also answers Q17 "yes, later" and Q9 "caller-side stdout capture": the coordinator's WC-16 pass (the at-most-every-5-minutes sweep the coordinator runs) saves the JSON it already prints, so no sweep rule (NFR-001, one report file per run) changes.
2. XC-05 drafts the contract note as planned, with the captured JSON registered as a third artefact (path, owner, age rule).
3. After PR #539 merges and the real-id comparison (XC-04) shows the observer's dispatch ids match the sweep's row ids, an observer task adds the panel, reading the captured file with an age rule and treating every string as untrusted.

## What it unlocks

- One definition of "waiting on a person" or "stalled" on the person's screen, which is what #409 asks for: "If the observer built its own collector, two programs would classify the same session and could disagree" (#409 body, line 55).
- The observer can show proof-based classes (frozen plans, safe-to-close, contract questions) it cannot compute from Orca rows alone.
- No merge of the two programs; each keeps its own rules.

## What it costs or risks

- It reverses three debate verdicts for version 1 (X-013, 95 percent; X-017, 70 percent; A-001, 78 percent) and the recommended answers to Q9 and Q17 ("not now").
- The captured file exists only when a coordinator runs the sweep; on a host with no coordinator the panel is empty, and its age must be shown.
- Joining rows depends on a key that has never been compared on real ids (XC-04).
- A new file and a new reader mean a new untrusted-input path and more tests.

## What stays unresolved

- Who runs the capture and where the file lives (Q9).
- Whether the observer's own Orca view and the sweep's view disagree for the same worker, and which wins on screen.
