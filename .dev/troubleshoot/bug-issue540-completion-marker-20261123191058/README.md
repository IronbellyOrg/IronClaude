# Issue 540 investigation: start here

This folder preserves the investigation **before** the completion-marker fix. The 61 original files remain byte-identical to the [transfer receipt](transfer-receipt.json). This guide was added after the transfer so the work can be revisited without relying on another worktree.

## Where to start

- [Original diagnosis](REPORT.md): what failed before the fix. Its `blocked` result describes that investigation, not the later implementation.
- [Original evidence review](evidence-validation.md): review of the diagnosis, not approval of the repair.
- [Reproduction commands and observations](tier1-observation.md).
- [Completed fix: start here](../../tasks/done/TASK-WF-createACheckedFi-20261123-195635/README.md): current plan, implementation ledger, final review and positive command-line evidence.
- [Path audit](../../research/issue540-transfer-path-audit-20261124.json): integrity checks and historical citation caveats.
- [Portable file-location index](../../research/issue540-current-file-locations.json): repository-relative locations for the original investigation and completed fix records.

## How to interpret paths in the original files

Links in this guide are relative to this folder and work in a different checkout. Paths in captured stdout, contracts, worker outputs and audit records are **historical recorded values**, not instructions to use the old worktree. Do not replay those commands unchanged.

The captured source worktree was `/home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s`. For files in this package, use the matching suffix beneath this folder; the portable index supplies the exact repository-relative location. For source code, read the recorded revision, not the repaired working tree:

```bash
git show db57e231863078dbbb8e4e5fb37a61371c89806c:src/superclaude/cli/swarm/commands.py
```

Source paths such as `src/...`, `tests/...` and `docs/...` start at the repository root. The recorded commit exists in the local Git history. Source line numbers in the diagnosis belong to that revision; current source and documentation have changed.

One original quote pointer in [the constraint card](wave1_5-branch-C.md) names `preflight.py:966`; its quoted words start at **968-970** in that revision. The quote exists; use that corrected range. Installed skill references under `~/.claude/` and rescued release documents were external context, not part of the transfer. They are indexed in the path audit but are not promised to exist on another machine.

## Intentionally absent or unavailable evidence

- `artifacts/foreground/done.json` and `artifacts/resume/done.json` are intentionally absent: their absence is the pre-fix negative evidence. Do not create them here. See [the negative witness](artifacts/negative-witness.txt).
- The three foreground `*.raw.md` paths recorded in [the original result contract](artifacts/foreground/return-contract.yaml) are **unavailable** in both the old location and this transfer. They were never listed in the transfer receipt. Do not treat them as working links or fabricate replacement raw outputs.
- The corresponding preserved outputs are [worker 0](artifacts/foreground/bare-review-00-lens-default-model-0.final.md), [worker 1](artifacts/foreground/bare-review-01-lens-default-model-0.final.md) and [worker 2](artifacts/foreground/bare-review-02-lens-default-model-0.final.md). These are normalized outputs, **not** substitutes claiming to be raw captures.
- Optional files explicitly reported absent, and the unrelated shared diagnostic counter, are not missing transfer deliverables.

## Original file inventory

<!-- INVENTORY: Generated from transfer-receipt.json; every listed link must resolve. -->

### Reports and investigation cards

- [REPORT.md](REPORT.md)
- [REPORT.md.draft](REPORT.md.draft)
- [audit.log](audit.log)
- [contract-ledger.md](contract-ledger.md)
- [diagnosability-context.md](diagnosability-context.md)
- [diagnosability-tasklist.md](diagnosability-tasklist.md)
- [doc-context.md](doc-context.md)
- [effective-input.md](effective-input.md)
- [evidence-validation.md](evidence-validation.md)
- [execution-locus.md](execution-locus.md)
- [hardening-applicability.md](hardening-applicability.md)
- [producers.md](producers.md)
- [runtime-entrypoint.md](runtime-entrypoint.md)
- [tier1-calibration.md](tier1-calibration.md)
- [tier1-callers.md](tier1-callers.md)
- [tier1-hypothesis.md](tier1-hypothesis.md)
- [tier1-observation.md](tier1-observation.md)
- [unmask-sweep.md](unmask-sweep.md)
- [wave1_5-branch-A.md](wave1_5-branch-A.md)
- [wave1_5-branch-B.md](wave1_5-branch-B.md)
- [wave1_5-branch-C.md](wave1_5-branch-C.md)
- [wave1_6-branch-A.md](wave1_6-branch-A.md)
- [wave1_6-branch-B.md](wave1_6-branch-B.md)

### Shared capture and review artifacts

- [baseline-tests.txt](artifacts/baseline-tests.txt)
- [evidence-validation-round1.md](artifacts/evidence-validation-round1.md)
- [foreground-check.json](artifacts/foreground-check.json)
- [foreground.stdout.txt](artifacts/foreground.stdout.txt)
- [home/.keep](artifacts/home/.keep)
- [hypothesis-first-receipt.md](artifacts/hypothesis-first-receipt.md)
- [import-paths.txt](artifacts/import-paths.txt)
- [negative-witness.txt](artifacts/negative-witness.txt)
- [report-before-review-correction.md](artifacts/report-before-review-correction.md)
- [resume-check.json](artifacts/resume-check.json)
- [resume.stdout.txt](artifacts/resume.stdout.txt)
- [shared-counter-observation.diff](artifacts/shared-counter-observation.diff)
- [source-revision.txt](artifacts/source-revision.txt)
- [target.txt](artifacts/target.txt)

### Foreground capture

- [State](artifacts/foreground/.swarm-state.json)
- [Manifest](artifacts/foreground/manifest.json)
- [JSONL log](artifacts/foreground/execution-log.jsonl)
- [Markdown log](artifacts/foreground/execution-log.md)
- [Result contract](artifacts/foreground/return-contract.yaml)
- [Merged output](artifacts/foreground/merged.md)
- [Worker 0 output](artifacts/foreground/bare-review-00-lens-default-model-0.final.md)
- [Worker 0 metadata](artifacts/foreground/bare-review-00-lens-default-model-0.meta.json)
- [Worker 1 output](artifacts/foreground/bare-review-01-lens-default-model-0.final.md)
- [Worker 1 metadata](artifacts/foreground/bare-review-01-lens-default-model-0.meta.json)
- [Worker 2 output](artifacts/foreground/bare-review-02-lens-default-model-0.final.md)
- [Worker 2 metadata](artifacts/foreground/bare-review-02-lens-default-model-0.meta.json)

### Resume capture

- [State](artifacts/resume/.swarm-state.json)
- [Manifest](artifacts/resume/manifest.json)
- [JSONL log](artifacts/resume/execution-log.jsonl)
- [Markdown log](artifacts/resume/execution-log.md)
- [Result contract](artifacts/resume/return-contract.yaml)
- [Merged output](artifacts/resume/merged.md)
- [Worker 0 output](artifacts/resume/bare-review-00-lens-default-model-0.final.md)
- [Worker 0 metadata](artifacts/resume/bare-review-00-lens-default-model-0.meta.json)
- [Worker 1 output](artifacts/resume/bare-review-01-lens-default-model-0.final.md)
- [Worker 1 metadata](artifacts/resume/bare-review-01-lens-default-model-0.meta.json)
- [Worker 2 output](artifacts/resume/bare-review-02-lens-default-model-0.final.md)
- [Worker 2 metadata](artifacts/resume/bare-review-02-lens-default-model-0.meta.json)
