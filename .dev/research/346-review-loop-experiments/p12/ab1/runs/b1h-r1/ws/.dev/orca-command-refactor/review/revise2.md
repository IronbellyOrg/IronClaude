review: 2 of 3
revise: 2 (REVISE prompt, document_review_loop_prompts.md; brief IDS = N1, N2)

# Revision 2: orca-worker-contract-spec.md

## Inputs

- Candidate (edited in place): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- Before: sha256 `260c7c0ee1cfff6f147fa7f24960981dd4f6f1f953afdeef2b24a0b090d875da`, 293 lines, 59812 bytes
- After: sha256 `1a2d2f425ac57ef3f2392d0bfdf09996e8bf26606b0e7b94ee731ab5d177867d`, 293 lines, 60176 bytes
- Prior report: `.dev/orca-command-refactor/review/round2.md` (`review: 2 of 3`, Reviser brief lists N1, N2, N3)
- VERIFY reply: `.dev/orca-command-refactor/review/verify-2.md` (`confirmed: N1, N2`; N3 rejected)
- Revision scope: the brief's IDS are N1 and N2 only. N3 is noted, unactioned, and was not revised. Minor and Medium findings (F1, F2) were not touched.

## Byte accounting

Byte size before: 59812. Byte size after: 60176. Net change: +364 (= +575 added, -211 deleted).

| finding id | location (after) | bytes added | bytes deleted | net |
|---|---|---|---|---|
| N2 | `spec:62` (WC-4 row, file-valued output sentence) | 371 | 143 | +228 |
| N1 | `spec:204` (AC-1.2 row) | 204 | 68 | +136 |
| total | | 575 | 211 | +364 |

Added and deleted counts are the byte lengths of the replaced span (new span and old span) for each id, from the Edit calls. No other line changed. A `diff -w` of the whole file would show the same two lines.

## Findings

| id | status | where applied | change | reason |
|---|---|---|---|---|
| N1 | applied | `spec:204` (AC-1.2). `spec:85` and `spec:86` already name one flag each (`--output-dir`), so they were not edited. | The AC-1.2 live check no longer passes `--output <dir>` to every P1 command. It now passes `--unattended` plus the one output flag section 3 names for that command: `--output-dir <dir>` for cleanup-audit, index-repo and workflow, and `--output <dir>` for the others. | Verifier confirmed (verify-2.md, row N1): `spec:86` gives index-repo only `--output-dir`, and `spec:204` passed `--output <dir>`, which the command would reject. Choosing one name per command in the AC removes the mismatch. |
| N2 | applied | `spec:62` (WC-4 row) | The file-valued sentence changed from "`<output-dir>` is that file's parent directory" to "the contract is not `<output-dir>/return-contract.yaml` but `<parent>/<stem>.return-contract.yaml`". `<stem>` is the output file name without its extension. The sentence cites [M1, N2]. | Verifier confirmed (verify-2.md, row N2): the parent-directory rule let two runs whose `--output` files share a parent (for example `a.md` and `b.md` under `.dev/superclaude/`) write the same contract path, so the second run overwrote the first. The stem in the name keeps each run's contract distinct. The `WC-11` (`spec:69`) text is unchanged. The `CAPS:115` premise is not relied on. |
| N3 | noted, unactioned (not in the brief's IDS; not revised) | none | none | Verifier rejected N3 (verify-2.md, row N3): step 6 (`spec:193`) applies its pass rule only to a "report-only command", and the candidate never classifies `/sc:workflow` or `/sc:troubleshoot` as report-only. The "P0 smoke runs use no output flag" claim is also false for `/sc:adversarial --output <dir>` (`spec:158`). The `INV-B:242` default-output claim for troubleshoot is UNVERIFIED here. The coordinator keeps N3 as a note under the VERIFY rule. |

## Checks

- Each new quoted text was found in the candidate by `grep -nF` (lines 62 and 204).
- No stale AC-1.2 text (`with \`--unattended --output <dir>\``) remains in the candidate.
- `return-contract.yaml` still appears in the candidate (13 lines). The AC-1.1 test assertion (`spec:203`) matches the substring, so it still holds after the stem-prefixed name in WC-4.
- No other section (M1 to M10 resolved text, section 3 rows, P0 to P4 phases) was changed.
- The spec-panel was not run. No review was started and no PASS was awarded.
- UNVERIFIED (carried, not checked here): the `cmd/`, `sk/` and `src/` citations cited in these rows are not in the sandbox. The `INV-B:52,242,272` and `CAPS:115` citations are UNVERIFIED in this workspace.

## Follow-up candidates (Medium, not revised per the REVISE rule)

- F1 (Medium, `spec:202`): adversarial's step-4 file is unnamed in AC-0.4.
- F2 (Medium, UNVERIFIED, `spec:202` with `spec:191`): the workflow contract may lack the `command` key that step 4 asserts.

verdict: not set. A REVISE output does not award a PASS; the next re-review decides.
