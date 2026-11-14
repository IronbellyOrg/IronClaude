# Proposal B: one trust design for every consumer

## Answer

Promise one trust design: the grant format, signing and verification chosen under #339 (Orchestrator mode) is the only one, and the observer (#409), Orchestrator v2 (#423) and the workspace listener (Coder#477) all use it rather than defining their own.

## What happens next if the owner picks it

- The ledger records "Q16: one trust design" with the date (XC-01).
- #409 decision 6 keeps "Decide one design, not two." (no wording change in OB-08).
- The #423 rewrite (V2-01) and the Coder#477 text adopt review 03's Edit 7 wording: "The grant format is the one chosen in IronbellyOrg/IronClaude#339 ... This issue does not define a second format." (diff-analysis.md line 89).
- SW-12's Phase 4 (trust layer) row in #534 is scoped as the single design that all three consumers will import.

## What it unlocks

- One mechanism to build, review and test, instead of three local ones that share only words.
- A clear single owner: every trust question is answered in #339's trust layer, and no other issue may invent a second format.
- Cross-program features (v2 relaying to agents, a remote listener) would not need a translation layer later.

## What it costs or risks

- The debate leaned against it (66 percent for the narrower promise, X-005, ADJ line 382): the three consumers have different threat models. The observer is read-only on one host, the watcher's trust is "a different, local model" (V3 itself), and the listener would cross workspaces.
- A shared design tends toward signing; #339 comment 2 says "encryption alone is not enough", and signing does not stop poisoned content, so one design could give a false sense of safety for relayed text (ADJ line 295).
- Commits three issues to a design that does not exist yet (SW-12 Phase 4 is unbuilt); if the design later fits one consumer badly, three issue texts must change.

## What stays unresolved

- What the design actually is (signing, key handling, scopes); none of it is specified.
- How poisoned content is handled, which a grant design alone does not answer.
