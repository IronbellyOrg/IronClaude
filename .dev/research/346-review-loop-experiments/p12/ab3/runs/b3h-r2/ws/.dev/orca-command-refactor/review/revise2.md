# Revise 2: orca-worker-contract-spec.md

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (edited in place)
- brief: REVISE prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md`
- input report: `.dev/orca-command-refactor/review/round2.md` (review: 2 of 3, verdict FAIL)
- IDS: F-02, F-05 (the `Reviser brief` of round2.md, SPEC:139)
- reviser: claude-haiku-5-5

## Byte accounting

| Measure | Before | After | Net |
|---|---|---|---|
| Candidate bytes (`wc -c`) | 60216 | 60408 | +192 |
| Candidate lines (`grep -c ''`) | 290 | 290 | 0 |
| Candidate sha256 | `7f3af35e63f12d24d6eebc453c30497ba2705a10886e04c84b5f7497272961d3` | `06cb4bcd39e29ea26abacd7521abf23c5e125f1cefda82fb1736f725a01d24b0` | |

Bytes per finding id (exact substring counts from the edit script; the anchor text is counted as deleted and re-written with the addition):

| Finding id | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| F-02 | 166 | 44 | +122 |
| F-05 | 278 | 208 | +70 (two edits, SPEC:87 cells 2 and 3) |
| Total | 444 | 252 | +192 |

## Finding rows

| Id | Disposition | Where applied | Basis |
|---|---|---|---|
| F-02 | applied | WC-4, SPEC:62: one sentence added after "...the brief states that exact path (F-01)." It says `load` is the one section 3 command that writes no file and so writes no contract. | Round2 said WC-4 (SPEC:62) required a contract from every section 3 command, while the load row (SPEC:112) says "none (F-02 ...)" and AC-1.1 (SPEC:200) exempts `load`. The added sentence makes WC-4 match both. `load` writes no file: `INV-B:65` ("it only loads context ... and writes no file"), and `cmd/load.md:52` as quoted there. The load row (SPEC:112) and the decision row at SPEC:270 already agree with this and are unchanged. |
| F-05 | applied | init-lite row, SPEC:87. Column 2 now says the `--output` file sits in "a unique directory per worker and attempt" under `--unattended`. Column 4 now reads "Fresh output directory per attempt (WC-6): a `--retry-of` brief passes a new directory and the `--output` file inside it, so the first attempt's report and contract are kept (F-05)." | The round2 contradiction was: WC-6 (SPEC:64) requires a re-run to write "into a fresh output directory", while the old row (SPEC:87) gave only a fresh file, so WC-4's `<output-dir>/return-contract.yaml` would be the same path for both attempts. The row now requires a fresh directory, as round2's suggested repair said. The init-lite re-run overwrites its marked report (`INV-A:55`, quoting `S:66`), which is why a fresh directory is needed. `cmd/init-lite.md:32` is cited from the inventory and was not checked here: UNVERIFIED. |

Ids not in IDS and not changed: R2-01 to R2-06 and M-01 to M-19 (Medium and minor, not blocking, not in the brief). R2-05 (WC-4 zero-input case) sits on SPEC:62, the line edited for F-02; its text is unchanged and it remains open as a Medium follow-up.

## Checks run

- Each anchor string was matched exactly once in the candidate before replacement (the edit script asserts this). The pre-edit hash matched round2's candidate hash.
- After the edit, the three changed phrases were grepped in the file (SPEC:62 and SPEC:87).
- No file other than the candidate and this output was written. The baseline `specs/history/` files were not touched.
- Not run: the spec-panel, `uv run pytest`, and the `make verify-sync` check (planning-only spec, no code touched).

## Decisions

| Decision | Options | Rationale |
|---|---|---|
| F-02 wording | (1) add one sentence to WC-4; (2) delete "every outcome" from WC-4 for `load` | (1). It names the exception where the rule is stated and needs no change to the rule's other clauses. Round2 suggested the same. |
| F-05 wording | (1) keep "fresh file" and add a directory rule; (2) change the row to require a fresh directory | (2). Round2 suggested it, and one row change matches WC-6. |
| Wording of the F-02 exception | "writes no file" versus "has no Task" | "writes no file", because that is the reason `INV-B:65` gives. The load row keeps its existing "no Task" phrase. |

## Reviser note

The brief says to prefer deleting or narrowing. F-02 adds one sentence because the round2 repair needs a stated exception. F-05 narrows the row to a fresh directory and drops the "fresh file" wording. No rule, mechanism or section was added.

verdict: not issued (the reviser does not award a PASS)
