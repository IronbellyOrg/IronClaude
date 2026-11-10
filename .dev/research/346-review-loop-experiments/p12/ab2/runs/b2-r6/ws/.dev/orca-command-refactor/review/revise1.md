# Revise 1: Orca worker-contract spec

Prompt followed: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` ("Repair only the blocking findings {{IDS}}..."). Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place. IDS: B-1, B-2 (confirmed at `.dev/orca-command-refactor/review/round1.md:2`, `verify-1.md` last line `confirmed: B-1, B-2`). Other inputs read: `round1.md:87-101,237-247`, `README.md`, `inventory/commands-b.md:31,65`. No PASS is claimed. The spec-panel was not run. Citations `SPEC:N` are lines of the candidate; line numbers are unchanged by the edits (all edits are inside existing lines).

## Byte accounting

| | Bytes |
|---|---|
| Before | 57763 (sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`) |
| After | 58012 (sha256 `89aa60a626c2210c7e3cd02a711923cbaf3990a333b6398f744d27073b0d61ba`) |
| Net | +249 |

| Finding | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| B-1 | 191 (SPEC:62 +167; SPEC:76 +24) | 35 (SPEC:76) | +156 |
| B-2 | 104 (SPEC:76 +18; SPEC:112 +32; SPEC:159 +18; SPEC:195 +18; SPEC:196 +18) | 11 (SPEC:112) | +93 |
| Total | 295 | 46 | +249 |

Counts are span-level (an inserted or replaced span counts in full); the per-finding nets sum to the file-size difference (156 + 93 = 249).

## Disposition per finding

| Id | Disposition | Where applied | What changed and why |
|---|---|---|---|
| B-1 | Applied | SPEC:62 (WC-4), SPEC:76 | The two contradicting texts were "`<output-dir>` is a directory" (SPEC:62) against tdd and init-lite passing `--output <file>` (SPEC:87, SPEC:90; `INV-A:55`, `INV-B:47,222`). Narrowing choice: keep the directory rule and add one clause to WC-4: when the output flag names a file, the contract is that path plus `.return-contract.yaml` (example `docs/TDD_AUTH.md.return-contract.yaml`). That path is known before dispatch from the brief alone, is never below a regular file, never occupies the TDD's own path, and is unique per file, so two workers in one directory do not share a contract (WC-11). SPEC:76 restated the old template `<output-dir>/return-contract.yaml`; that restatement was replaced by "path rule in WC-4", which deletes a second copy of the rule. No other row needed an edit: SPEC:183 step 4 (`<contract>`), SPEC:182 step 3 ("the WC-4 contract path") and SPEC:200 AC-2.2 resolve through WC-4; the substring `return-contract.yaml` still holds for AC-1.1 (SPEC:195). Rows SPEC:87 and SPEC:90 were left alone because WC-4 now covers them. |
| B-2 | Applied | SPEC:76, SPEC:112, SPEC:159, SPEC:195 (AC-1.1), SPEC:196 (AC-1.2) | Chose the smaller of the two fixes the review offered (`round1.md:100`): load stays out of the contract set, as SPEC:112 and SPEC:265 already decide (load only loads context, `INV-B:65`; `SPEC:139`). The "every command" wording that pulled load in was narrowed to "except load" at SPEC:76 (section 2.1 `## Unattended mode` section), SPEC:159 (P1 flag scope), SPEC:195 (AC-1.1) and SPEC:196 (AC-1.2); SPEC:112's report cell now says "none; outside the contract set". Load remains in P1 for its usage-line fix only (SPEC:112, SPEC:159 "load (usage line only)"). SPEC:265 and the load row's "not as its own Task" text are unchanged, so no text now requires load to have a contract or a live run. |

Rejected findings: none.

## Left alone

All Medium and minor findings (M-1 to M-15, n-1 to n-12) are untouched, as the brief requires. Known interactions, recorded for the next review and not acted on: the SPEC:92 workflow pre-creation STOP and the SPEC:83 adversarial path still have their own location questions (M-2); `SPEC:62` does not say who creates the parent directory of a file-valued `--output`; the 27-command count in SPEC:76 still includes load.
