# Revise 2

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Input: `review/round2.md` (Reviser brief: L1 only, `round2.md` "Reviser brief"), with the L1 sub-findings N1-N5, N8, N9 read in `review/round2-t1b-1.md:128-161`. No spec-panel was run. Spec line numbers below are post-edit lines of the candidate (`S:N`). Citations to files outside the workspace (`src/`, `CLAUDE.md`, `.dev/codegraph-migration/`) are UNVERIFIED and were not touched. The pre-edit copy is `specs/history/spec-v2.md` (byte-identical to the candidate before this revision).

## Byte accounting

Before 59544 bytes, after 60359 bytes (`wc -c`), net +815. Word-level diff against `specs/history/spec-v2.md`: 990 bytes added, 178 deleted. Per-sub-finding figures are the full replaced spans (old span deleted, new span added; unchanged words inside a span are counted in both):

| id | added | deleted | note |
|---|---|---|---|
| L1 / N1 | 180 | 123 | WC-5 yields to AC-0.4 before P1 |
| L1 / N2 | 515 | 277 | WC-4 sentence, cleanup-audit and index-repo rows, AC-1.2 |
| L1 / N3 | 185 | 102 | AC-0.4 step 3 report path |
| L1 / N4 | 86 | 69 | WC-4 status clause |
| L1 / N5 | 365 | 175 | section 3.1 intro, section 2.3 |
| L1 / N9 | 443 | 213 | WC-6, section 2.3 |
| L1 total (spans) | 1774 | 959 | |

## Finding rows

| id | action | where / reason |
|---|---|---|
| L1 N1 (WC-5 vs AC-0.4) | applied | WC-5 (S:63) now starts the failure mapping "From P1 on (P0 runs have no contract and follow AC-0.4)", so the two texts no longer give opposite outcomes. |
| L1 N2 (no output option, no contract path) | applied | WC-4 (S:62) allows "a fixed contract path" in the row; cleanup-audit row (S:85) fixes `.claude-audit/return-contract.yaml` from its fixed output dir (`round2-t1b-1.md:136`); index-repo row (S:86) uses `PROJECT_INDEX.md.return-contract.yaml` under WC-4's beside-a-file rule; AC-1.2 (S:201) no longer requires `--output <dir>` on commands without one. |
| L1 N3 (P0 report path undefined) | applied | AC-0.4 (S:199) step 3 takes a non-empty file in the brief's output directory (workflow: its package directory) as the report path, since P0 fixes no filename; this removes the dependency on the "contract, but filename not fixed" cell. |
| L1 N4 (existing `status` key) | applied | WC-4 (S:62): "a contract that already has a `status` key with other values maps them onto these four", replacing "kept under its own name". The existing vocabulary stays UNVERIFIED (`round2-t1b-1.md:145`). |
| L1 N5 (3.1 "only" sentence; 2.3 silent on P2-P4) | applied | Section 3.1 intro (S:79) adds the P1 section; section 2.3 (S:73) passes `--unattended` from the phase that gives the command its section. |
| L1 N8 (ask cap, missing `worker_done` action, write order, missing core file, schema version) | rejected | Requirements the document never states, not stated text that does harm (`round2-t1b-1.md:158-159`; FIRST-REVIEW grading check in `document_review_loop_prompts.md`). The brief says to add no rule that a finding does not call for; adding five policies would widen the spec. Same rejection as revise 1 (`revise1.md`, row "L1 t2 F15 ..."). |
| L1 N9 (fresh path vs resume and fixed output dirs) | applied | WC-6 (S:64) and section 2.3 (S:73): a fresh attempt gets a new path, a resume run reuses the earlier path, and cleanup-audit and index-repo (fixed output location) run one attempt at a time (WC-11). |

## Fix map

```fixmap-v1
{"id": "L1", "action": "applied", "reason": "N1-N5 and N9 repaired by narrowing wording in WC-4, WC-5, WC-6, sections 2.3, 3.1, AC-0.4 and AC-1.2; N8 rejected as unstated requirements (Medium)."}
```
