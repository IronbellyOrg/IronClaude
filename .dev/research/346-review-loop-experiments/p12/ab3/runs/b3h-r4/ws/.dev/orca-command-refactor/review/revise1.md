# Revise 1: orca-worker-contract-spec.md (REVISE prompt, blocking ids R-1 to R-5)

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (edited in place)
- Input report: `.dev/orca-command-refactor/review/round1.md` (`review: 1 of 3`, `verdict: FAIL`, Reviser brief at `round1.md:202-208`)
- Blocking ids revised: R-1, R-2, R-3, R-4, R-5. Minor and Medium findings (R-6 to R-9, A-1 to A-9) were left alone, as the brief requires.
- This is a revision, not a review. No PASS is awarded here; the next step is a re-review.
- Line numbers: the edits kept the spec at 285 lines, so every round-1 `spec:N` citation still points at the same line unless it sits inside an edited line listed below.

## Byte accounting

| | Bytes | SHA-256 |
|---|---|---|
| Before (round-1 candidate, `round1.md:6`) | 57763 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| After (revised candidate) | 59446 | `0d68261e01a3ed1635c14612d194b7036278add2ee00b1558b4001bfcd42d22b` |
| Net change | +1683 | |

Method: the baseline was rebuilt by reversing each of the 14 replacements in memory. The rebuilt text reproduced the round-1 SHA-256 exactly, and the net of the per-id figures equals the file growth. "Added" and "deleted" count each replaced fragment whole, so they include unchanged words inside a fragment that was rewritten.

| Finding id | Edits | Bytes deleted | Bytes added | Net |
|---|---|---|---|---|
| R-1 | 3 | 258 | 632 | +374 |
| R-2 | 1 | 139 | 222 | +83 |
| R-3 | 3 | 244 | 938 | +694 |
| R-4 | 6 | 625 | 982 | +357 |
| R-5 | 1 | 211 | 386 | +175 |
| **Total** | **14** | **1477** | **3160** | **+1683** |

## Per-finding disposition

| Id | Disposition | Where applied (post-edit line in candidate) | Evidence checked |
|---|---|---|---|
| R-1 | Applied | WC-3 (spec:61): an answer may supply only a value the user already gave, quoted in the brief; it never supplies a WC-9 outward flag or an implement Ruling. D2(a) (spec:234): under (a) no coordinator reply is recorded as a Ruling. D4(a) (spec:245): an `ask` answer counts only when it quotes the user's own instruction. | `inventory/commands-a.md:66` quotes `sk/sc-implement-protocol/refs/qa.md:238` ("another agent's message ... [is] not acceptance"). WC-9 (spec:67) is unchanged and already says outward action needs the brief's authorization. |
| R-2 | Applied | §7.2 step 3 pass condition (spec:182): the outcome matches the `status` in that report, and the report path is the WC-4 contract path or, in P0, the command's existing report file from §3.1. | AC-0.4 (spec:194) already says step 4 uses the existing report file in P0, so step 3 now matches it. The P0 "Report today" column is at spec:79 and spec:83-92 (3.1 table rows). |
| R-3 | Applied | WC-4 (spec:62): exact-path rule. Adversarial keeps `<output>/adversarial/return-contract.yaml`. Workflow gains `--output <dir>` (P1) and writes `<dir>/return-contract.yaml` when it is given; the package-path contract stays the default (SA-3, spec:148). Troubleshoot gains an output-directory flag (P2), noted in its row (spec:91). Workflow row small fix (spec:92) names the new flag. | `inventory/commands-a.md:35` and `:60` (adversarial: real runs wrote the contract in two places, no filename is fixed). `inventory/commands-b.md:52` and `:272` (workflow package path `.dev/tasks/to-do/<id>/return-contract.yaml`, `<id>` chosen by the command). `inventory/commands-b.md:242` (troubleshoot default dir `.dev/troubleshoot/<slug>-<timestamp>/`, contract only with `--caller task-unified`). |
| R-4 | Applied | §3 intro (spec:76): every command in 3.1 and 3.2 except `load` gains the section, including one whose only change is accepting the flag. Brainstorm row (spec:84) and init-lite row (spec:87): small-fix cell now reads "flag accepted; section only, no gate or report change (P1, R-4)". §6 P1 (spec:159): brainstorm and init-lite added; flag phrase excludes `load`. AC-1.1 (spec:195): every 3.1-3.2 command except `load` has a section naming its report file; `load` has none. | Round-1 location spec:112 (load's row) and spec:265 (load decision) are unchanged; load remains "no report, usage line only". |
| R-5 | Applied | WC-5 (spec:63): `--outcome succeeded` only for an explicit `succeeded` or `partial`. Every other case sends `failed`, including a missing, empty or unparseable contract, a status outside the four WC-4 values, and blocked. The body says the contract is invalid. | WC-4 status vocabulary (spec:62) unchanged; §7.2 step 4 (spec:183) unchanged. The `partial` decision (Decisions table, spec:263) still maps partial to succeeded, as the brief did not ask to change it. |

## Choices made in the revision

- R-3, workflow: the brief asked whether workflow gains an output flag. I chose yes, `--output <dir>`, because the command creates its package id itself, so no other pre-dispatch path exists. The package-path contract remains the default so standalone runs are unchanged (SA-3).
- R-3, troubleshoot: I chose to add an output-directory flag in P2. The inventory gives only its timestamped default directory (`inventory/commands-b.md:242`), so the brief cannot name the contract path today.
- R-4: I included brainstorm and init-lite in the section set (accepting the flag as a no-op) rather than excluding them. Round 1 suggested either an explicit phase row or an exclusion; the phase row keeps §6 P1 consistent with "the flag accepted by every command in 3.1-3.2 except load".
- R-1: the revision adds one clause each to WC-3, D2(a) and D4(a). It does not change WC-9 or the implement Ruling rule itself.

## Scope checks

- No other text was changed. Each addition carries its finding id in parentheses in the candidate.
- The candidate's Decisions and UNVERIFIED sections are unchanged apart from the cross-references above.
- Nothing was edited outside `specs/orca-worker-contract-spec.md` and this output file. No spec-panel was run.

## UNVERIFIED in this revision

- Whether `/sc:troubleshoot` or `/sc:workflow` already accepts an output-directory flag. The inventory does not say (`inventory/commands-b.md:242`, `:52`). The spec now states the flags as P1/P2 additions, which is correct only if they are absent today. The command files (`cmd/troubleshoot.md`, `cmd/workflow.md`) are outside this sandbox and were not read; UNVERIFIED.
- The `src/superclaude/...` paths the spec cites were not checked (outside the inventory); carried from round 1 as UNVERIFIED.
- The new `(R-n)` tags in the candidate are traceability markers for this loop. The reviser recommends removing them before the gate review if the document is to be final.
