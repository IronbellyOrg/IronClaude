# Revise 2: orca-worker-contract-spec.md

Revision of the candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` under the REVISE prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox path `home/.claude/rules/prompts/document_review_loop_prompts.md`).

- Input review: `.dev/orca-command-refactor/review/round2.md` (`review: 2 of 3`, verdict FAIL). Its Reviser brief lists one blocking id: `N-1` (`round2.md:153`).
- Verifier confirmation: `.dev/orca-command-refactor/review/verify-2.md:10` reads `confirmed: N-1`. `round2.md:2` agrees.
- `{{IDS}}` = `N-1`. No other id was confirmed, so no other id is revised.
- Round-2 Medium and minor findings (M-1 to M-4, m-1) and the noted F-01 are left alone, per the REVISE brief ("Leave minor and Medium findings alone").

## Byte accounting

| Measure | Bytes |
|---|---|
| Candidate before revision (sha256 `bfe20373dae030b64d0ab846cde01958172f4f46786bcfbad746ac335c6b4df6`) | 59081 |
| Candidate after revision (sha256 `39bbe6871713a48397dee32c0a486174eebbc1b08a14833316eed1593df495bb`) | 59343 |
| Net change | +262 |

Per finding id (bytes of the replaced substring, exact):

| Finding id | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| N-1 (edit 1, WC-4) | 294 | 51 | +243 |
| N-1 (edit 2, init-lite row) | 91 | 72 | +19 |
| **N-1 total** | **385** | **123** | **+262** |

No other edit was made. Totals match the file size change (59343 - 59081 = 262).

## Findings

| id | Disposition | Where applied | Reason |
|---|---|---|---|
| N-1 | Applied (narrowing and naming, no new mechanism) | `specs/orca-worker-contract-spec.md:62` (WC-4, F-02 clause) and `specs/orca-worker-contract-spec.md:87` (init-lite row, Report column) | `round2.md:75-81` gives the defect: a file-valued output takes the contract name `return-contract.yaml` in its parent directory, so `--output docs/a.md` and `--output docs/b.md` both write `docs/return-contract.yaml`, and the second write replaces the first (`verify-2.md:8` confirms the chain: SPEC:62, SPEC:87, SPEC:69). The fix takes the reviewer's first recommendation (`round2.md:81`): the contract is named `<output-stem>.return-contract.yaml` beside a file-valued output. The WC-4 clause carries the rule, so tdd (file-valued `--output` at `specs/orca-worker-contract-spec.md:90`, `INV-B:47`) is covered by the same rule. The init-lite row names the same path. No new mechanism, section or flag was added. The AC-1.1 test text (`specs/orca-worker-contract-spec.md:195`) still matches because `return-contract.yaml` remains a substring of the new name. |

## Not actioned (not in `{{IDS}}`)

| id | Status in this revision | Reason |
|---|---|---|
| M-1 (workflow `<id>` flag unnamed) | Left alone | Medium; `round2.md:84-88`. Not a blocking id. |
| M-2 (output flag for index-repo and cleanup-audit) | Left alone | Medium; `round2.md:90-94`. Not a blocking id. |
| M-3 (step-4 actor and `command` mapping) | Left alone | Medium; `round2.md:96-101`. Not a blocking id. |
| M-4 (AC-1.1 vs P1 Commands column) | Left alone | Medium; `round2.md:103-107`. Not a blocking id. |
| m-1 (index-repo `mode=update` location) | Left alone | Minor; `round2.md:109-111`. Not a blocking id. |
| F-01 (noted, not blocking) | Left alone | Noted by the VERIFY rejection at `round1.md:2`; `round2.md:71`. |

## Self-check

- The new WC-4 clause is found exactly once: `grep -nF` of `return-contract.yaml` in that directory matches `specs/orca-worker-contract-spec.md:62` only.
- The new init-lite contract path is found exactly once: `grep -nF` of `<output-stem>.return-contract.yaml` (P1` matches `specs/orca-worker-contract-spec.md:87` only.
- The evidence cited for the file-valued outputs is unchanged and was checked in this workspace: `inventory/commands-b.md:47` (tdd, TDD file at `--output`) and `inventory/commands-a.md:55` (init-lite, `--output`).
- No line outside `specs/orca-worker-contract-spec.md` was edited. The only other file written is this report.

## Coverage

Read in full: `README.md`, `review/round2.md`, `review/verify-2.md`, the REVISE and RE-REVIEW sections of the prompt file, and the candidate spec (WC-4 to WC-12, section 2.3, section 3.1 and 3.2 rows for init-lite, tdd and workflow, AC-1.1). Cited inventory lines were checked (`inventory/commands-a.md:55`, `inventory/commands-b.md:47`). Not checked: repo files outside the workspace (for example `src/superclaude/...`); any citation to them stays UNVERIFIED as the candidate already marks it. No `spec-panel` run was made, as the brief requires.
