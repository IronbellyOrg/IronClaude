# Revise 1: orca-worker-contract-spec

Input: `.dev/orca-command-refactor/review/round1.md` (review 1 of 3, verdict FAIL, Reviser brief ids `F-01, F-02, F-03`). Candidate edited in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Only the candidate and this file were changed. The spec-panel was not run, and no PASS is awarded.

## Byte accounting

| Measure | Value |
|---|---|
| Candidate size before (bytes) | 57763 (sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`, matches `round1.md:8`) |
| Candidate size after (bytes) | 58791 (sha256 `ba714118121e521fcaa6d0492fe49f39e1fe607a6399a97a6d4b5fc9f802ffdb`) |
| Net change | +1028 bytes |

Method: each edit is counted as the bytes of the replaced segment (deleted) and the bytes of its replacement (added). Segment byte counts were measured with `wc -c`. The per-edit totals reconcile to the file size change: 57763 + 1804 added - 776 deleted = 58791.

| Finding id | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| F-01 | 389 | 212 | +177 |
| F-02 | 790 | 306 | +484 |
| F-03 | 625 | 258 | +367 |
| Total | 1804 | 776 | +1028 |

Per-edit detail:
- F-01: AC-C1 scope (`spec:172`) 54 deleted, 33 added; AC-C1 pass cell (`spec:172`) 31 deleted, 146 added; SA-2 last sentence (`spec:147`) 127 deleted, 210 added.
- F-02: WC-4 (`spec:62`) 0 deleted, 131 added; WC-6 (`spec:64`) 233 deleted, 434 added (includes the owner cell); section 3 intro (`spec:76`) 0 deleted, 109 added; section 2.3 (`spec:73`) 73 deleted, 116 added.
- F-03: section 3.1 lead-in (`spec:79`) 64 deleted, 369 added; AC-1.1 (`spec:195`) 194 deleted, 256 added.

## Finding rows

| Finding | Disposition | Where applied (spec line after revision) | Reason or note |
|---|---|---|---|
| F-01 (AC-C1 blocks P0 because it scans `src/superclaude/core`, which must name Orca) | Applied | `spec:172`: `src/superclaude/core` removed from the grep scope; the pass cell now says core files are not scanned. `spec:147` (SA-2): the one allowed Orca mention is restated as the core contract file and the routing guide's Orca section (SA-5), and no changed command, skill or agent names Orca. | Round 1 `review/round1.md:35-38` (Sentence and Recommendation). The scope now matches the one SA-2 uses. |
| F-02 (WC-4 says the coordinator reads the contract where it passed the directory, WC-6 says a re-run writes a fresh directory) | Applied | `spec:62` (WC-4): a retry gets a new directory from the coordinator, and the coordinator reads the contract of the attempt it last dispatched. `spec:64` (WC-6): the coordinator owns the directory and passes a new one for each retry; the command never chooses its own directory in unattended mode; owner cell now reads "Coordinator picks the retry directory; command resumes". `spec:76`: "Fresh dir" is defined as the coordinator passing a new `<output-dir>`. `spec:73` (section 2.3): a new directory for each retry. | Round 1 `review/round1.md:41-45`. Chosen option: coordinator owns the directory, which matches `CAPS:116` (`worker-start --retry-of`, `inventory/orca-capabilities.md:116`). The other option (command subdirectory plus pointer file) was not taken, so no pointer file was added. |
| F-03 (AC-1.1 requires the section in every 3.1 and 3.2 command, but `spec:79` and the load row disagree) | Applied | `spec:79` (section 3.1 lead-in): the flag and the `## Unattended mode` section are added to all 37 commands in sections 3.1 and 3.2, including ready commands whose small fix is "None"; every one of them except `load` names the WC-4 contract; `load` writes none, per its row (`spec:112`) and the Decisions table (`spec:265`). `spec:195` (AC-1.1): the check covers every command in sections 3.1-3.2 except `load`, and checks that `load`'s section names no contract. | Round 1 `review/round1.md:47-51`. The count is 10 (3.1) plus 27 (3.2) = 37, matching `spec:76`. Option "remove load from AC-1.1" was taken rather than giving load a contract. |

## Not revised (out of brief)

Medium findings M-01 to M-08 and minor findings m-01 to m-05 (`review/round1.md:53-141`) were left unchanged, as the REVISE prompt requires (`home/.claude/rules/prompts/document_review_loop_prompts.md:51`). No PASS is awarded for this revision.

## Citation check

- The edited segments were checked by reading them back from the candidate. Each quoted segment appears on the lines listed above.
- Citations to `inventory/orca-capabilities.md` (`CAPS:116`) were read in this run (`inventory/orca-capabilities.md:116`).
- Citations to files outside the workspace were not used in any new text. Anything of that kind remains UNVERIFIED as in the candidate.
