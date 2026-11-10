# Revise 1: blocking findings B-1 and B-2

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place. Input report: `.dev/orca-command-refactor/review/round1.md` (Reviser brief at round1.md:268-277). Citation keys: `SPEC:N` = line N of the candidate after this revision (line numbers are unchanged; every edit is within an existing line). `R1:N` = `round1.md`. `INV-A:N`, `INV-B:N` = the inventories. Citations to files outside the workspace are not used; a claim that rests on one is UNVERIFIED.

No award of PASS is made here; the reviewer decides.

## Byte accounting

| Measure | Bytes |
|---|---|
| Candidate before | 57763 (matches R1:6 and R1:276) |
| Candidate after | 58629 |
| Net change | +866 |

Per finding id (word-level diff of the 12 edits; "added" and "deleted" count only changed tokens, so an edit that rewrites part of a sentence does not count the unchanged words):

| Finding | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| B-1 | 906 | 278 | +628 |
| B-2 | 273 | 35 | +238 |
| Total | 1179 | 313 | +866 |

Every edit is B-1 or B-2. The Medium and minor items (M-*, n-*) were not touched. No section was added; no row was added. The 3.2 rows were not edited at all: the single rule in WC-4 now yields a contract path for each of them, which is why the many "no contract location" rows named at R1:92 needed no per-row change (narrowing instead of adding a column).

## Disposition, one row per finding id

| Finding | Disposition | Where applied | Reason / cited basis |
|---|---|---|---|
| B-1 | Applied | SPEC:62 (WC-4), SPEC:73 (section 2.3), SPEC:76 (section 3 preamble), SPEC:79 (section 3.1 intro), SPEC:83 (adversarial row), SPEC:92 (workflow row), SPEC:159 (P1 scope), SPEC:183 (live check step 4), SPEC:196 (AC-1.2), SPEC:200 (AC-2.2) | R1:90-95 and the grading sentence at R1:94. The rule "contract is `<output-dir>/return-contract.yaml`, `<output-dir>` is `--output`/`--output-dir`" gave a path under a regular file for tdd (`--output <file>`, SPEC:90) and init-lite (SPEC:87), and no knowable path for workflow (generated `<id>`, SPEC:92, INV-B:272), tasklist, research, implement, index-repo, cleanup-audit and review-translation (R1:92). Fix: the brief passes a directory-valued `--contract-dir <dir>` (R1:95 first option); the contract is `<contract-dir>/return-contract.yaml`, so the path is known before dispatch for every command. Where a command's `--output`/`--output-dir` is already a directory (reflect, brainstorm, release-split, roadmap, post-release, per R1:95) and no `--contract-dir` is given, that directory is used, so those rows and the AC-0/AC-3/AC-4 smoke lines that pass `--output <dir>` keep working unchanged. Adversarial (R1:93): its contract path was unnamed and inconsistent on disk (INV-A:35, INV-A:60), so the row now says it writes at the WC-4 path, replacing the earlier `<output>/adversarial/return-contract.yaml` which differed from the rule. Workflow (R1:94): the package contract stays; the same contract is also written to `<contract-dir>`, which gives the pre-creation STOP a directory to write into (INV-B:272 records that no package exists then). AC-2.2's tdd example (R1:94) now carries `--contract-dir <dir>`, and step 4 defines `<contract>` as the WC-4 path so `test -s` reads a path the text yields. |
| B-2 | Applied | SPEC:182 (live check step 3), SPEC:194 (AC-0.4) | R1:100-102 and the grading sentence at R1:101. P0 makes no command edit (SPEC:158) and WC-4 is built in P1 (SPEC:159), so step 3's "matches the contract's `status`" and "report path is the WC-4 contract path" could not be met for troubleshoot (contract only with `--caller task-unified`, INV-B:242). Fix, in the direction R1:102 gives: in P0 the command's existing report file stands in for the contract in step 3 (`--outcome` follows WC-5 applied to that report; the report path is that file), and step 4 is `test -s` on that file. The three smoke commands each have an existing report: troubleshoot `REPORT.md` and workflow's package contract (SPEC:91-92, INV-B:242, INV-B:272), adversarial's contract (INV-A:35). Which file counts for adversarial is left as "the existing report file" because INV-A:60 shows its on-disk path varies; that is an open M-level matter (M-12 and the adversarial row), not changed here. |

## Left alone, by instruction

All Medium and minor findings (M-1 to M-17, M-20, M-21, n-1 to n-9) stay as follow-up candidates (R1:262-266, R1:277).

Interactions worth the reviewer's eye, noted and not acted on:
- M-14 (load): the P1 scope line at SPEC:159 now also mentions `--contract-dir`; load's exemption is unchanged and still open.
- M-9 (unwritable or missing contract directory): `--contract-dir` is required only where `--output` is not already a directory; what happens if the brief omits it is not specified and stays under M-9.
- M-4/M-17 (retry in a fresh directory): `--contract-dir` makes the retry directory a coordinator choice per attempt, but the spec text on that was not changed.

## Check on the edits

- Every replaced string was unique in the file (the apply step asserted a count of 1 before each of the 12 replacements).
- Line count is unchanged at 285; `diff` against `.dev/orca-command-refactor/specs/history/spec-v1.md` shows 24 changed lines (12 old, 12 new).
- Each of the 12 additions carries `B-1` or `B-2` in the text itself (the step 4 definition and the AC-2.2 example were given a literal `B-1` after the first pass; the 11 bytes this added are counted in the table above).
- Not run: the spec-panel (forbidden by the brief); any command or test (nothing is implemented in this run).
