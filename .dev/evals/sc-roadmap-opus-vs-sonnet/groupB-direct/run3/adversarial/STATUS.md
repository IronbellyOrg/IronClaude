# /sc:adversarial run3 — PIPELINE ABORTED (transport failure)

## Status

**status: failed**  •  **failure_stage: transport**  •  see `return-contract.yaml`

## What happened

The /sc:adversarial Mode B pipeline started at 18:33 UTC on
`feat/sc-troubleshoot-wave-1.5-doc-grounding`. Between 19:31 and 19:52 UTC, the
working tree underwent five checkouts in a parallel session interleaved with
three commits, while subagents were still producing pipeline artifacts. Because
`.dev/eval-roadmap/` is uncommitted-by-convention (gitignored at the project
level), the checkouts wiped untracked artifacts that did not exist on the
destination branches.

Git reflog evidence:

```
19:31  checkout: feat/sc-troubleshoot-wave-1.5-doc-grounding → chore/markdownlint-sweep
19:34  commit:    chore: apply markdownlint MD022/MD031/MD032/MD034 auto-format
19:35  checkout: chore/markdownlint-sweep → feat/cliEval-exit-codes
19:36  commit:    feat(cliEval): canonical exit_codes module + ... remediation
19:36  commit:    chore(releases): move cliEval from current/ to complete/
19:43  checkout: feat/cliEval-exit-codes → chore/task-graduation
19:43  commit:    chore(tasks): graduate 7 completed tasks
19:52  reset:     moving to HEAD
19:52  checkout: chore/task-graduation → feat/cliEval-exit-codes
```

## Artifacts destroyed mid-pipeline

| Step | File | Status |
|------|------|--------|
| Mode B variant gen | `variant-1-opus-default.md` (666 lines, written 18:39) | **destroyed** |
| Mode B variant gen | `variant-2-sonnet-default.md` (854 lines, written 18:39) | **destroyed** |
| Step 1 | `diff-analysis.md` (236 lines, 47 diff points: S=10 C=12 X=6 U=12 A=7) | **destroyed** |
| Step 2 R1 | `round-1-advocate-v1.md` (opus) | **destroyed** |
| Step 2 R1 | `round-1-advocate-v2.md` (sonnet) | **destroyed** |
| Step 2 R2 | `round-2-rebuttal-v1.md` (opus) | **destroyed** |

## Artifacts surviving

| Step | File | Notes |
|------|------|-------|
| Step 2 R2 | `round-2-rebuttal-v2.md` (sonnet, ~300 lines) | written 19:53, after final checkout |
| Step 2 R2.5 | `invariant-probe.md` (74 lines, 18 findings) | written 19:57; fault-finder explicitly reported that only `round-2-rebuttal-v2.md` was visible as input, so all other transcripts were missing when the probe was generated |

## Integrity warning on surviving probe

The 3 HIGH-severity UNADDRESSED items (INV-004, INV-012, INV-017) preserved in
`return-contract.yaml#unaddressed_invariants` are *suggestive evidence*, not a
completed invariant audit — the fault-finder never saw the variants, the diff
analysis, or the R1 transcripts, only V2's R2 rebuttal. They are worth a fresh
look on re-run, but they cannot be cited as the output of a properly grounded
Round 2.5 probe.

## Recovery

The source spec `.dev/eval-roadmap/inputs/merged-prd-tdd-user-auth.md` is
committed and unaffected. The run is fully reproducible.

Recommended re-run (paste-ready, single line):

```
/sc:adversarial --source /config/workspace/IronClaude/.dev/eval-roadmap/inputs/merged-prd-tdd-user-auth.md --generate roadmap --agents opus,sonnet --depth standard --output /config/workspace/IronClaude/.dev/eval-roadmap/groupB-direct/run3
```

To prevent another transport-layer failure, run on a branch that will not be
checkout-swapped during the pipeline (5–10 minutes of git-quiet time), or use an
isolated worktree (`EnterWorktree`) for the duration of the run.
