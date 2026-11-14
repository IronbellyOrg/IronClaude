# Q22: what age makes a snapshot or workspace record stale?

## The question, verbatim

Spec row (merged-requirements.md section 3, line 549): "What age makes a snapshot or workspace record stale?"

Original wording (ADJ Part 7, line 792): "What age makes a snapshot or a workspace record \"stale\" (the observer's own feed uses 45 s; a file on disk has no liveness flag)?"

## Spec's recommended answer

"The owner's number; no debate recommendation" (merged-requirements.md line 549). ADJ line 792: "Your number; no debate recommendation."

## Default if unanswered

"ADJ: readers show any file older than the producer's own cycle as stale and print its age" (merged-requirements.md line 549; ADJ line 792).

## What it gates

- XC-05, drafting the contract note between the observer and the sweep (`docs/designs/observe-sweep-contract.md`, merged-requirements.md line 453): the note must list "the Q22 age policy" (line 476). Dependency row 108 (line 755): Q5, Q13, Q22, Q23 are decisions XC-05's content rests on.
- CO-02, completing the open placeholders of the narrowed Coder#477 text (line 354): "(1) `[N minutes: owner decides]` replaced by the Q22 number, or the line keeps the placeholder with 'owner decides' and the reply says so". Coder#477 is an issue in the separate `IronbellyOrg/Coder` repository about a read-only workspace status record.
- CO-04, the DEFERRED channel that would copy the observer snapshot to the TUIBBS host (line 356): "When opened: a transport, an identity envelope ..., an age rule (Q22) and re-sanitising are each specified." TUIBBS is the owner's separate terminal-UI platform on a different SSH host.
- Wave needed by: W1 (line 861 lists Q22 among W1 owner answers).

## Facts the question depends on

| Fact | Source |
|---|---|
| The observer (`superclaude observe`, the read-only terminal dashboard of Orca workers, issue #409, merged) polls every 15 s and, after failures, waits up to 60 s | `src/superclaude/cli/observe/collector.py:28,30` (`INTERVAL = 15.0`, `MAX_BACKOFF = 60.0`), read 2026-11-14 |
| The observer marks its own feed stale at 45 s: "three intervals without a successful poll, on the monotonic clock" | `src/superclaude/cli/observe/view.py:32-34`, read 2026-11-14 |
| The observer writes `snapshot.json` atomically; in live mode it rewrites it after each new cycle; with `--once --snapshot` it writes once | `observe/export.py:26`, `observe/commands.py:203-208,232-233,294-299,366-369`, read 2026-11-14 |
| The snapshot is last-writer-wins, stays on disk after the process exits, and has no pid or liveness flag; its `producer` is `{name, version}` only; the reader applies its own age rule to `generatedAt` | ADJ line 228; invariant probe INV-004 (`.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/invariant-probe.md` line 11): "Residual: no age threshold is set" |
| The sweep's "stale" means something different: a transcript-only row older than its 6 h window (`DEFAULT_WINDOW = "6h"`) | ADJ line 250 (mapping table row "stale"); `src/superclaude/cli/sweep/commands.py:27` |
| The mapping table rule for "stale": "say 'feed stale' or 'session stale'; never show one as the other" | ADJ line 250 |
| The narrowed Coder#477 text has the acceptance line "A record older than [N minutes: owner decides] is reported stale, never current." | ADJ line 634; round2-rebuttal-V3.md section 5.6 A |
| No reader of the snapshot or of a Coder workspace record exists today: the Coder#477 implementation (CO-03) and the TUIBBS copy channel (CO-04) are DEFERRED | merged-requirements.md lines 355, 356 |
| Consumer behaviour required by the spec: "Distinguish feed age, stored-file age, PARTIAL coverage and per-row evidence age. Use `generatedAt`, print the age, apply Q22's fallback ... An old snapshot is not a current process heartbeat." | merged-requirements.md line 279 |
| Version 1 of the note "publishes nothing new": neither program gains a file or key | ADJ line 222; merged-requirements.md line 453 |
| A later age rule may be added to the snapshot "as an optional key (stays v1) or v2" | merged-requirements.md line 1196 |
