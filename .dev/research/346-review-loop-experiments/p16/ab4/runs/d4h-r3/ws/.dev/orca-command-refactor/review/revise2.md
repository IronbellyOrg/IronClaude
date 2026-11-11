# Revise 2 (REVISE prompt, document_review_loop_prompts.md)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (edited in place)
baseline (before revision): sha256 0e53b436d774ed5d6bf97ec9ffac93472d2f0ec0eb53b20ecebda159b8c5d3e2 (the text round 2 reviewed; checked with `sha256sum` before the first edit)
prior report: .dev/orca-command-refactor/review/round2.md (review: 2 of 3, verdict FAIL; Reviser brief at round2.md:79-83)
IDS revised: M6, N1

## Byte accounting

- Size before: 61053 bytes (sha256 0e53b436d774ed5d6bf97ec9ffac93472d2f0ec0eb53b20ecebda159b8c5d3e2)
- Size after: 61229 bytes (sha256 150cd2160e83032be24b36d6510052c36e52b128ef009a46dab2f911fab14ca3)
- Net: +176 bytes

Per finding id (bytes deleted / added / net; each edit is counted under the id it cites in its own text):

| Id | Edits | Deleted | Added | Net |
|---|---|---|---|---|
| M6 | 1 | 170 | 255 | +85 |
| N1 | 1 | 105 | 196 | +91 |
| Total | 2 | 275 | 451 | +176 |

Check: 61053 + 176 = 61229.

Byte counts were taken from the old and new sentence text of each edit (UTF-8), so they measure the edited sentences, not a full-file diff.

## Findings

| id | action | where applied (candidate line) | reason / evidence |
|---|---|---|---|
| M6 | applied | line 194 (AC-0.4 row, step 4 sentence) | Step 4 now reads `test -s <existing report>` with no YAML key check, because workflow's existing contract has `status` and no `command` key (`.dev/orca-command-refactor/inventory/commands-b.md:272`). The old text applied the `d['command']` assertion of line 183 to workflow, which raises KeyError on a correct run. Line 183 is unchanged; it still applies to P1-P4 commands, whose contracts gain `command` under WC-4 (line 62). |
| N1 | applied | line 85 (cleanup-audit row, Small fix column) | The row no longer says the output directory is fixed. It now says `--output-dir <dir>` is added in P1 (the same change as line 76), after which parallel audits each pass their own `--output-dir` (WC-11). The "Report today" column still gives the default `.claude-audit/pass<N>-summary.md`, which matches the inventory (`.dev/orca-command-refactor/inventory/commands-a.md:42`). Line 76 is unchanged. |
| F1 | not actioned | none | Medium follow-up candidate, not a blocking id in the Reviser brief (round2.md:80). The brief says to leave it alone. |
| F2 | not actioned | none | Medium follow-up candidate, not a blocking id (round2.md:80). Left alone. |
| F3 | not actioned | none | Medium follow-up candidate, not a blocking id (round2.md:80). Left alone. |
| F4 | not actioned | none | Medium follow-up candidate, not a blocking id (round2.md:80). Left alone. |
| F5 | not actioned | none | Medium follow-up candidate, not a blocking id (round2.md:80). Left alone. |

## Self-check

- `grep -nF` of the AFTER text of M6 (`Step 4 is replaced by ... and no YAML key check runs`) finds line 194 of the candidate.
- `grep -nF` of the AFTER text of N1 (`add `--output-dir <dir>` in P1 (N1, M2)`) finds line 85 of the candidate.
- `grep -c 'output dir is fixed'` on the candidate returns 0.
- No other line was edited. The candidate is 61229 bytes.

## Notes

- Verdict: not stated here. The REVISE prompt says the reviser does not award a PASS; the next review decides.
