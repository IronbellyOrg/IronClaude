# Revise 1: worker-contract spec, blocking findings B-1, B-2, B-3

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (edited in place). Cited below as `spec:N` (line numbers of the revised file; the line count is unchanged at 285).
- Prompt: REVISE, `home/.claude/rules/prompts/document_review_loop_prompts.md` (read in full).
- Brief: revise only the ids the VERIFY step confirmed, B-1, B-2 and B-3 (`review/verify-1.md:15`, `confirmed: B-1, B-2, B-3`). Source of the findings: `review/round1.md` (Reviser brief at `review/round1.md:19,150-151`).
- Not in this brief: B-4 (see table). Medium and minor findings M-1 to M-17 and m-1 to m-4 are untouched.
- Evidence limits: this worker checked only files under `.dev/orca-command-refactor/inventory/` and the candidate. `command.md` and every `src/`, `tests/`, `.dev/` citation outside the inventories are UNVERIFIED and were not relied on.

## Byte accounting

| Measure | Baseline (before) | Revised (after) | Net |
|---|---|---|---|
| Candidate bytes | 57763 | 59236 | +1473 |
| Candidate sha256 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` | `c0bcf427b1adbc33a7a7d8ed59cafb19f0ae4373145c6ccaac5362de30dbc042` | |

The baseline is `specs/history/spec-v1.md`, byte-identical to the candidate before this revision (same sha256 as `verify-1.md:4`). Added and deleted bytes are counted per changed word token (`diff` on space-split tokens; the spaces themselves are not counted), so the two columns sum to the true changed text. Per-finding net is taken from whole changed lines, which sum exactly to +1473.

| Finding | Lines changed (after) | Added bytes | Deleted bytes | Net bytes (whole lines) |
|---|---|---|---|---|
| B-1 | 61, 114, 235 | 406 | 38 | +436 |
| B-2 | 62, 79, 90, 92, 120 | 815 | 80 | +876 |
| B-3 | 112, 195, 265 | 148 | 13 | +161 |
| B-4 | none (not confirmed, not actioned) | 0 | 0 | 0 |
| Total | | 1369 | 131 | +1473 |

The file-level totals are 6101 bytes of new whole lines and 4628 bytes of old whole lines in the changed-line diff, because whole lines were re-read; the per-finding word-level figures above are the ones to use for added and deleted bytes.

## Findings

| Id | Status | Where applied (spec line) | Change |
|---|---|---|---|
| B-1 | applied | `spec:61` (WC-3) | `ask` never answers a person-owned gate: the implement Ruling (`INV-A:66`, citing `qa.md:238`), the cli-portify approval gates (`INV-A:45`), and any run-time approval of an outward action (WC-9). Those gates resolve blocked under WC-2 (c) with no `ask`, unless D2 option (b) is chosen. `ask` is limited to informational questions. Evidence cell extended with `INV-A:66` and `INV-A:45`. |
| B-1 | applied | `spec:114` (pr-submit row, section 3.2) | "the worker may use `ask` or `escalation`" changed to "resolve as blocked with no `ask` (WC-3, B-1)", so operator HALTs follow the new WC-3 exclusion. |
| B-1 | applied | `spec:235` (D2 option (b)) | Added that choosing (b) lifts WC-3's exclusion for the Ruling gate. D2(a) and the implement row (`spec:109`, "the Ruling rule itself is unchanged") were already consistent and are unchanged. |
| B-2 | applied | `spec:62` (WC-4) | `<output-dir>` is the directory the brief names through the command's directory flag, set per command in section 3. `--output` is not a directory flag. Where a command's only output flag takes a file (tdd, `INV-B:47`), the brief gives a fresh directory and names the file inside it. A command whose report path is generated (workflow, `INV-B:272-273`) must accept an output directory from the brief. Evidence cell extended with `INV-B:47` and `INV-B:272-273`. |
| B-2 | applied | `spec:79` (section 3.1 intro) | Added that the workflow row needs P1's `--output-dir` before its report path can be briefed. The ready count (10) is unchanged. |
| B-2 | applied | `spec:90` (tdd row, 3.1) | The brief passes `--output <file>` inside a fresh directory it names. |
| B-2 | applied | `spec:92` (workflow row, 3.1) | Brief adds `--output-dir <dir>` (P1). Report column notes that `<id>` is generated, so the path is not known before dispatch (`INV-B:272-273`). Small fix: accept `--output-dir`, write the contract there, keep the package path in `plan_path` (`INV-B:272`, which lists `plan_path` among the contract fields). |
| B-2 | applied | `spec:120` (spec-panel row, 3.2) | "add `--output`" replaced with "add a directory flag, not `--output`". The review's reading of `command.md:460` (file-valued `--output`) is marked UNVERIFIED here, because `command.md` is outside this worker's evidence. P2 must confirm the flag before fixing its name. |
| B-3 | applied | `spec:195` (AC-1.1) | The test now exempts `/sc:load` by name, requires that its section names no report file, and keeps the rest of the check. |
| B-3 | applied | `spec:112` (load row, 3.2) | "none (see note)" changed to "none; exempt from AC-1.1 by name (B-3; Decisions `/sc:load` row)". The note it pointed to did not exist. |
| B-3 | applied | `spec:265` (Decisions, `/sc:load` handling) | Added that AC-1.1 exempts load by name (B-3). The recorded decision (use it inside a brief; no report file, `INV-B:65`) is unchanged. |
| B-4 | noted, unactioned | none | Not in this brief. VERIFY rejected it (`verify-1.md:13`): the row at `spec:85` states the one-audit-at-a-time limit, so the overwrite needs a parallel dispatch that the stated text forbids. The spec text at `spec:85` and `spec:73` is unchanged. The next re-review treats B-4 as a note (`round1.md:2`). |

## Checks

- Every added sentence cites a finding id (B-1, B-2 or B-3) in the same cell or sentence.
- No section, mechanism or phase was added beyond what the three findings call for. The new P1 `--output-dir` for workflow is within the existing P1 scope ("output flags for commands that lack one", `spec:159`).
- Section 3.2 phase column, the 10/27/6 split (`spec:75`), and the AC-C checks (`spec:170-176`) are unchanged.
- Grep for the three ids in the revised candidate returns 11 lines (`spec:61,62,79,90,92,112,114,120,195,235,265`), matching the table above.
- Not run here: the spec-panel and live-worker checks (out of scope for this REVISE step), and no PASS is claimed. The next step is a RE-REVIEW against the baseline `specs/history/spec-v1.md`.
