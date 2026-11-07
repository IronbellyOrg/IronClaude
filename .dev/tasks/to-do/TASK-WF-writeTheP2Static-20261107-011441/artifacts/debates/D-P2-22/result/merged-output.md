<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (option A, original) -->
<!-- Merge date: 2026-11-07 -->

# D-P2-22 decision: replace the two false P1 lines in workflow.md (option A wins)

<!-- Source: Base (original) -->
## Decision

Choose option A. In `src/superclaude/commands/workflow.md`, the `## Unattended mode` section replaces exactly two P1 lines in place: the "Contract" bullet (line 72) and the "Nested invocations" bullet (line 75). The old "Nested invocations" line says the reflect step "runs as today, without `--unattended`"; under P2 it receives `--unattended --output <report-dir>/nested/reflect-<n>/`, so the old sentence is false. The old "Contract" line names the `.dev/reflect/` run directory (reflect's default `--output`, `reflect.md:101`); with the nested directory that wording is false too. The Check ADDITIVE rule (zero deleted lines per command file) gets a named exemption for exactly these two lines of workflow.md (and one line of brainstorm.md, D-P2-1).

No file edit follows from this decision: the working tree already holds option A.

<!-- Source: Base (original) -->
## Why A wins (debate result, convergence 100%, score 0.822 vs 0.710)

- The whole section is true when a worker runs it under `--unattended`. Option B leaves `.dev/reflect/` beside `nested/reflect-<n>/` (a coordinator would be pointed outside the report directory, WC-4); option B2 leaves "runs as today, without `--unattended`" beside "receives `--unattended`", the opposite of spec line 62. `WORKER-CONTRACT.md` has no rule that ranks a later line over an earlier one.
- It is what the spec names: spec line 222 (P2 row) lists the workflow section edit; spec line 152 says "from P2, the reflect step ... passes `--unattended` and a nested report directory".
- It is already built and pinned: `tests/skills/test_worker_contract.py:1679-1712` asserts the old wording is gone and has mutation checks for both old phrasings; `ac-c5.txt:18` records `vs HEAD [2 2] (named exemption: exactly 2 deleted lines)`. B and B2 would fail that test and need it, its mutation checks and `ac-c5.txt` rewritten.
- A person's run is unchanged: the section applies only when `--unattended` is a standalone token (`workflow.md:70`), so SA-1 holds.

<!-- Source: Base (original, modified) - bounded exemption wording, merged per Change #1 (Variant 2 advocate, weakness 1) -->
## Why the exemption is bounded

It is exactly two deleted lines in workflow.md (one in brainstorm.md), both false under `--unattended`, in a section that is inert in a standalone run. It is not a general loosening of SA-4 (spec line 211).

<!-- Source: Base (original, modified) - count kept enforceable, merged per Change #2 (Variant 2 advocate, weakness 3) -->
## Keeping the count enforceable

Keep the words "exactly 2 deleted lines" in the workflow row of `ac-c5.txt`, so a third deleted line in workflow.md fails the review.

<!-- Source: Base (original) -->
## What A costs (honest weaknesses)

- B2 is the only option that passes AC-C5 literally with zero deletions; A needs a hand-made exemption (B needs one too, for one line).
- Line 72 is long, so the in-place replacement diff looks larger than the one phrase that changed.
- The literal AC-C5 command compares against the merge base of master; the P2 edits touch lines P1 added, so that column reads `[15 0]` while local master is behind HEAD (`ac-c5.txt:2`). Once P1 is on master, the same check reads `[2 2]`, so the exemption is still needed.
