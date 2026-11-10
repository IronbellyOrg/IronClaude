# Revise 1: spec revision for blocking findings F-02 and F-03

- Prompt: REVISE prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before this revision).
- Candidate edited in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
- Input from round 1: sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`, 57763 bytes (matches `review/round1.md:7`).
- Output: sha256 `00cb7b63ea6019f358ead17f8b721ad6058432fb1bebc97218c1af92404e5038`, 58776 bytes.
- Ids repaired (`IDS`): F-02, F-03, the two ids VERIFY confirmed (`review/round1.md:2`). F-01 and F-04 were rejected by VERIFY and are noted, unactioned; they were not revised here.
- Scope: no Medium or minor finding was touched. Line numbers of the spec are unchanged (no line was added or removed; the edits sit on spec:181, spec:182 and spec:194).
- No verdict is given in this file. The re-review (review 2 of 3) decides PASS or FAIL.

## Byte accounting

Bytes are counted on the replaced text: "deleted" is the old string's bytes, "added" the new string's bytes.

| Finding id | Bytes deleted | Bytes added | Net |
|---|---|---|---|
| F-02 | 172 | 776 | +604 |
| F-03 | 105 | 514 | +409 |
| Total | 277 | 1290 | +1013 |

Check: 57763 (before) + 1290 (added) - 277 (deleted) = 58776 (after), and `wc -c` on the output file gives 58776. No bytes were changed outside these two ids.

## Rows, one per finding id

| Finding id | Result | Where applied (spec line, after edit) | Cited evidence |
|---|---|---|---|
| F-02 | applied | spec:181 (7.2 step 2) and spec:182 (7.2 step 3) | `review/round1.md:31-38`; `inventory/orca-capabilities.md:63` (`check --wait --types "worker_done,escalation,question" --timeout-ms`, and `reply --id ... --body`); WC-10 at `spec:68` (4-minute bound) |
| F-03 | applied | spec:194 (P0 row AC-0.4) | `review/round1.md:40-46`; `inventory/commands-b.md:242` (troubleshoot writes `REPORT.md` as `report_path`; `return-contract.yaml` only with `--caller task-unified`) |
| F-01 | not actioned: rejected by VERIFY, kept as a note | none. The text stays at spec:61, spec:109 and spec:200 as the round-1 report quotes them | `review/round1.md:2` (verifier: the wrong outcome needs an assumption the candidate does not state) |
| F-04 | not actioned: rejected by VERIFY, kept as a note | none. The text stays at spec:112, spec:195 and spec:265 | `review/round1.md:2` (verifier: rejected as noted; the contradiction is not revised in this loop) |

## What changed, per finding

### F-02: the live check cannot satisfy its heartbeat check (spec:181, spec:182)

The defect: step 3 waited up to 900000 ms in one `check --wait`, but step 2 required a `worker-show` at least once per 5 minutes, so no `worker-show` could run during that wait. Step 3 also had no branch for `question`, although `question` is in its type list.

- Spec:181 (step 2) now says that, with step 3's 240 s waits, one `worker-show` runs between consecutive waits. Added 4-minute bound matches WC-10 (spec:68).
- Spec:182 (step 3) now repeats `check --wait` with `--timeout-ms 240000`, runs `worker-show` before each repeat, and ends only at `worker_done`. The `check --wait` type list and the `--timeout-ms` option are as cited at `inventory/orca-capabilities.md:63`.
- Spec:182 also states what the coordinator does on `question` (answer with `reply --id <message_id>` only from the brief or the person; otherwise ask the person) and on `escalation` (record it verbatim in the phase report and keep looping). Both are the "state what the coordinator does" the round-1 recommendation asks for (`review/round1.md:37`).
- Pass conditions of step 2 and step 3 are unchanged in substance.

### F-03: AC-0.4 applies a YAML check to a markdown report (spec:194)

The defect: step 4 parsed YAML and read `d['status']` from the file, but for `/sc:troubleshoot` the file is `REPORT.md` (`inventory/commands-b.md:242`), a markdown report.

- Spec:194 (AC-0.4) now says that in P0 step 4 is `test -s <report>` on the file the command already writes, with no YAML parse; for `/sc:troubleshoot` that file is `REPORT.md`. The YAML key check applies from P1, when the contract arrives.
- In P0, step 3's outcome is read from the report's first status line, and the phase report records that line as found. This follows the round-1 recommendation (`review/round1.md:45`, first option).
- UNVERIFIED: the format of the report's status line. The troubleshoot report template is not in the inventories, so no line format is asserted.

## Self-check

- Each quoted string added by this revision was located in the output file with `grep -nF`: the step 2 phrase at spec:181, the step 3 text at spec:182, and the AC-0.4 P0 text at spec:194.
- Exact-text check on the two cited inventory lines: `inventory/orca-capabilities.md:63` holds the `check --wait --types` type list, and `inventory/commands-b.md:242` holds the `REPORT.md` and `--caller task-unified` facts.

## Not checked, marked UNVERIFIED

- Whether `check --wait` returns after the 240 s timeout with no rows (an empty return). The fix in F-02 relies on it; `inventory/orca-capabilities.md:63` does not state the timeout return. UNVERIFIED.
- The format of the troubleshoot report's status line (see F-03 above). UNVERIFIED.
- Repository files outside the workspace were not read. Nothing in this revision depends on them.
