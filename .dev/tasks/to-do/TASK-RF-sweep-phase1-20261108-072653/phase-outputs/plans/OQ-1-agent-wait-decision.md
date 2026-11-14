# OQ-1 (R5): may the sweep run `worktree ps --agent-wait`?

```yaml
needs_human_decision: false
status: RESOLVED    # DECIDED by the owner on 2026-11-08; recorded at task-build time
```

## Question

Master's coordinator sweep (`src/superclaude/core/WORKER-CONTRACT.md:110`) runs one prompt-wait listing, `worktree ps --agent-wait`. The INV-005 owner sign-off, condition 1 (SPEC section 13, NFR-014), said `worktree ps` never carries `--agent-wait`. May the sweep run it?

Options as first written:

- (a) extend the sign-off to `--agent-wait` after a lock check;
- (b) keep "never" and fix the master contract text in a later PR.

## Decision

OPERATOR DECISION: allow.
Chosen: allow `worktree ps --agent-wait`, with and without `--json`. This is option (a) without the extra lock-check condition: the owner waived it. Option (b) does not apply.
Decided by: the owner, 2026-11-08.
Decision source: the owner's words, relayed by the coordinator (run `run_93bfa00cae2b`, messages `msg_d95a87e312e1` and `msg_6ee5998d0874`): "Allow it, no conditions needed."
Decision source, direct confirmation (added 2026-11-12): Ryan Wiancko, owner, confirmed the relayed words directly in this session's question tool; answer recorded at 2026-11-12T00:10:31Z. The question read: "The review panel found that one earlier decision, OQ-1, rests on a message relayed by a coordinator session on 2026-11-08, not on your own answer: \"Allow it, no conditions needed.\" It lets the sweep's allowed Orca commands include `worktree ps --agent-wait` (with and without `--json`); Phase 1 never actually runs those two commands. Do you confirm it in your own words now?" The owner selected "Yes, confirm it (Recommended)", whose option text reads: "I record your selection as the direct source in the OQ-1 record and its row in owner-decisions.md, keep the relayed message as history, and the panel finding closes. The design stays as it is (10 allowed commands)." The relayed message above is kept as history. This confirms OQ-1 only; it grants nothing else.

## What stays in force

The rest of the INV-005 sign-off is NOT withdrawn:

- The exact Orca allowlist stays pinned by a test. It now has ten templates, still seven verbs.
- The report claim stays version-scoped: "unlikely (checked for Orca 1.4.245)", otherwise UNVERIFIED.
- `--include-remote` stays forbidden.

## Evidence for the record

The coordinator ran a live probe: 24 calls of `worktree ps --agent-wait` on one idle worktree.

- Results: 0 `index.lock` sightings at 5 ms polling, and 0 failed calls.
- Limits: locks shorter than 5 ms could be missed; only one idle worktree was tested; Orca 1.4.245.

## Applied by

Task items 6.1 to 6.4 apply the decision: they confirm this record, log it, edit DESIGN sections 7.3, 11, 13 and 15.1 plus the GQ-109 row, and run the mechanical checks. The R5 QA gate then closes it (items 6.5 to 6.22). `WORKER-CONTRACT.md:110` is not edited, because master's text already allows the listing.
