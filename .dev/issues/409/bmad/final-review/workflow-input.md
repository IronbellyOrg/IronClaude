# Input for `/sc:workflow`: Orca read-only observer (IronClaude issue 409)

Prepared in step 5 (final review), 2026-11-08. Paths are in the IronClaude worktree, where the code will live:
`/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/` (called BMAD below). Each folder is a byte-identical copy of the Coder planning folder (proved with `diff -r` in step 5).

## Documents to pass

| Role | Path (under BMAD) | Notes |
|---|---|---|
| Spec (source of truth for behaviour) | `spec-orca-observer/SPEC.md` plus its companions in the same folder: `acceptance-tests.md`, `adapter-contract.md`, `release-gates.md`, `rendering-rules.md`, `stack.md`, `unverified-register.md`, `owner-decisions-and-risks.md`, `write-back-future-stage.md` | Ranks above PRD, UX and architecture when they disagree. |
| Snapshot contract | `spec-orca-observer/snapshot-export-schema.md`; field list source: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/tuibbs-review/architecture-options.md` | Version 1, fields only ever added, never removed or renamed. |
| PRD | `prd-orca-observer/prd.md`, `prd-orca-observer/addendum.md` | |
| UX | `ux-orca-observer/DESIGN.md`, `ux-orca-observer/EXPERIENCE.md` | |
| Architecture | `architecture-orca-observer/ARCHITECTURE-SPINE.md` | AD-1 to AD-20 adopted (AD-2's timing is conditional on CD-1); CD-1 to CD-16 wait on owner answers, each with a default. |
| Owner decisions | `../owner-decisions-20261108.md` (binding); `final-review/owner-decision-pack.md` (23 open decisions, none needed for the first tasks) | |
| Final review | `final-review/REPORT.md`, `final-review/findings.md` | Review 3 left one blocking item (NEW-R3-1: architecture CD-16 said the shared worktree id shows in the inspector only, the UX says inspector and plain-text export). The owner had it fixed by edit, NOT re-reviewed: CD-16 now matches the UX. |

## Staged-release gating (plan only what the current gate allows)

1. **R0, fixture replay (plan now).** Offline only: the synthetic `base` fixture and its variants stand in because no recorded worker-list sample exists yet (redacted samples are recorded at the first permitted live read, part of the R1 gate); no live Orca call, no command registered in the shipped CLI (`release-gates.md`, production-integration reading 1 applies until the owner confirms otherwise).
2. **Direction selection (owner gate, not a release).** The owner's dated record. Nothing ships.
3. **R1, live worker list.** Only after the direction record and the confirmed production-integration reading. Includes the JSON snapshot.
4. **R2 question list** after the question-observation gate; **R3 links view** after the question-link gate; write-back is a future stage outside the read-only boundary. Do not plan these as implementation steps yet.

## Tasks that can start before any owner answer (all R0)

1. **Key-reader spike** (first task, AD-14): raw keyboard reader with Rich Live, tested in a pseudo-terminal with `pexpect`; judged against the six proposed criteria; on failure switch to Textual, never both.
2. **Snapshot schema test** (AD-12): JSON Schema for snapshot v1 with `additionalProperties: false`, validated against fixture output; written against the default answers to the owner decision pack's D9 and D10.
3. **Adapter allow-list with a fake runner** (AD-4, AD-5): the adapter accepts one fixed command template and rejects everything else; tested only through the house `Runner` seam, never a live Orca process.
4. **Sanitizer** (AD-9): every string from the source passes one sanitizer, which strips terminal escape sequences, control characters and invisible format characters (bidi controls included), and is rendered literally so no markup is interpreted; cut-off text uses `>` unless the owner changes it.

## Constraints every plan step must keep

- **Read-only.** No write path to Orca, no controls, no reuse of R1 code as a write path (AD-17).
- **No AGPL code.** No TUIBBS code is copied, linked or imported; the snapshot file is the only connection (licence opinion open).
- **Unknown is never zero or false.** Missing data renders as unknown, with counts as `n+? (k unknown)`; a lost source never lowers a count (AD-8).
- **Evidence labels stay.** Every fact keeps its label; unchecked things stay UNVERIFIED; no Orca API field is invented.
- **Tooling.** UV only; no `python -m`, no bare `pip`.

## Suggested command

```
/sc:workflow "Build R0 (fixture replay) of the read-only Orca observer for issue 409 in src/superclaude/cli/observe/: key-reader spike first, then snapshot schema test, adapter allow-list with fake runner, sanitizer. Inputs: .dev/issues/409/bmad/final-review/workflow-input.md" --depth standard --handoff none
```
