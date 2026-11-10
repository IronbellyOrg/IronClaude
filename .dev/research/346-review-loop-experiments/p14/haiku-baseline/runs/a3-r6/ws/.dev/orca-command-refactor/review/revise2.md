# Revise 2: orca-worker-contract-spec

Brief: repair only the blocking findings N-01 and N-02 listed in the Reviser brief of `review/round2.md:125-128`, in the candidate `specs/orca-worker-contract-spec.md`, under the REVISE prompt (`prompts:49-51`, the sandbox copy of `~/.claude/rules/prompts/document_review_loop_prompts.md`). Medium and minor findings were not touched. No PASS is awarded and no verdict is given; the candidate is returned for the next review.

## Files and hashes
- Before: `specs/history/spec-v2.md` (identical to the candidate before this revision), SHA-256 `ba714118121e521fcaa6d0492fe49f39e1fe607a6399a97a6d4b5fc9f802ffdb`, 58791 bytes, 285 lines.
- After: `specs/orca-worker-contract-spec.md`, SHA-256 `f8f6302199d147a422c4ace828ab0a5bd64e8d93cc92412e2478d4460e7d27ae`, 59613 bytes, 285 lines.
- Only `specs/orca-worker-contract-spec.md` and this file were written.

## Byte accounting
Method: line-level diff of `specs/history/spec-v2.md` against the revised candidate. Each changed line counts as its old bytes deleted and its new bytes added. Five lines changed, all single-line table rows or paragraphs.

| Line (`spec:N`) | Section | Finding | Bytes deleted | Bytes added | Net |
|---|---|---|---|---|---|
| 62 | WC-4 | N-01 | 1342 | 1469 | +127 |
| 64 | WC-6 | N-01 | 654 | 934 | +280 |
| 73 | 2.3 | N-01 (626 bytes) and N-02 (38 bytes) | 555 | 664 | +109 |
| 158 | P0 row | N-02 | 749 | 806 | +57 |
| 194 | AC-0.4 | N-02 | 463 | 712 | +249 |

Per finding:

| Finding | Deleted | Added | Net |
|---|---|---|---|
| N-01 | 2551 (1342 + 654 + 555) | 3029 (1469 + 934 + 626) | +478 |
| N-02 | 1212 (749 + 463) | 1556 (38 + 806 + 712) | +344 |
| Total | 3763 | 4585 | +822 |

The 38 bytes on line 73 are the string ` (from P1 on; P0 briefs omit it, N-02)`. The total net change, +822, equals 59613 - 58791.

## Findings

### N-01 (blocking): applied
Problem (`round2.md:59-66`): WC-6 and WC-4 required a new output directory for every retry, but the Resume column rows for adversarial, brainstorm, cleanup-audit, tdd, cli-portify, implement, pr-submit and roadmap need the first attempt's directory to resume.

Applied at:
- `spec:62` (WC-4): a retry of a row that WC-6 lists as resuming reuses that row's directory with the resume flag; a retry of any other row gets a new directory from the coordinator. The F-02 contract-reading sentence is kept.
- `spec:64` (WC-6): the resuming rows are listed by name: adversarial with `--pipeline-resume`, brainstorm, cleanup-audit, index-repo, tdd, cli-portify, implement, pr-submit, roadmap, release-split and save. Those rows keep their directory with the resume flag. Every other row gets a new directory for each retry. The Evidence cell changes to match.
- `spec:73` (2.3): the coordinator's brief uses the same rule.

Basis for the list: the Resume column rows at `spec:83` (adversarial), `spec:84` (brainstorm), `spec:85` (cleanup-audit), `spec:86` (index-repo), `spec:89` (release-split), `spec:90` (tdd), `spec:105` (cli-portify), `spec:109` (implement), `spec:114` (pr-submit), `spec:118` (roadmap), `spec:119` (save). The round-2 gloss at `spec:76` names only "Fresh dir", but the table also uses "fresh file" (`spec:116`), "Fresh package each run" (`spec:92`) and "fresh run" (`spec:117`). A rule keyed to the label would leave those rows undefined, so the rule names the resuming rows instead, and every other row defaults to a new directory.

Not verified: whether each listed command really has the resume flag or on-disk state named in its row. That needs the inventories (`inventory/commands-a.md`, `inventory/commands-b.md`), which I did not re-read. This list follows the spec's own Resume column and is UNVERIFIED against the inventories.

### N-02 (blocking): applied
Problem (`round2.md:68-73`): P0 runs the three commands without `--unattended`, while 2.3 required the flag in every brief and AC-0.4 gated unattended behaviour that the P0 commands do not have yet.

Applied at:
- `spec:73` (2.3): the brief states `--unattended` from P1 on, and P0 briefs omit it (38 bytes). This is the first option offered at `round2.md:73`.
- `spec:158` (section 6, P0 row): the three smoke runs are invoked directly and without `--unattended`, which the flag only accepts from P1.
- `spec:194` (AC-0.4): steps 1, 3, 6 and 7 are gated. Step 3's report-path check and step 4 use the command's existing report file, because the contract arrives in P1. Steps 2 and 5 are run and recorded, not gated: an `agentWait` or an `AskUserQuestion` found there is a P2 gate to convert, not a P0 failure. A failure of a gated step still reopens section 1. Step 5 is still run, because it is the check that the run is top-level, not wrapped in a subagent (`spec:65`, WC-7).

Not changed: the general 7.2 check (`spec:180-186`) still applies to P1 and later, as its own text says. The override is confined to AC-0.4.

### N-03 (Medium): not in the Reviser brief, left alone
`spec:147` and `spec:172` are untouched. Round 2 says this is a follow-up candidate (`round2.md:75-78`).

### N-04 (Medium): not in the Reviser brief, left alone
`spec:79`, `spec:112`, `spec:195` and `spec:265` are untouched (`round2.md:80-82`).

### M-03 (Medium, carried, sharpened by N-01 region): not in the Reviser brief, left alone
The sentence "In unattended mode the command never chooses its own output directory (F-02)" at `spec:64` is kept verbatim, as is the open question of an unattended run with no directory (`round2.md:84-85`).

### Carried Medium and minor findings: left alone
M-01, M-02, M-04 to M-08 and m-01 to m-05 (`round2.md:117-119`) are unchanged. No edit touches their lines.

## Coverage
- Read in full: `review/round2.md`, `README.md` (shared context, `README.md:30-31` rules), the REVISE section of `prompts`, the candidate, and `specs/history/spec-v2.md` (used as the baseline for byte counts).
- Not read: `command.md` and the inventory files. The brief's fixes are internal consistency edits and do not add any new inventory citation. The list of resuming rows is UNVERIFIED against the inventories (see N-01).
- No Orca call, no spec-panel run, no PR, no commit, and no file outside the assigned output and the candidate was written.
