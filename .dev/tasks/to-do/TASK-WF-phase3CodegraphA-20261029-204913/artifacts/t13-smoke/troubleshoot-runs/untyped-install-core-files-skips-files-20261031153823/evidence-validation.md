# Evidence Validation Report

**Report under validation**: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/troubleshoot/untyped-install-core-files-skips-files-20261031153823/REPORT.md.draft
**Timestamp**: 2026-10-31T15:43:44Z
**Total citations**: 8 (7 file:line, counting the repeat of installation.md:363 in Documentation Context, plus 1 command)
**Verified**: 7
**Dropped**: 0
**Passed through (command, no reexec)**: 1
**Suggested report status**: partial (A4 contributes partial; the prior merged `blocked` from the denied counter update stands, and this suggestion cannot lower it)

**Validation result**: PASS. There are no dropped citations and no structural FAIL (A6 and A7 did not fire).

## Verified citations

| # | Type | Location | Verdict |
|---|------|----------|---------|
| 1 | file:line | `src/superclaude/cli/install_core.py:66` (with 67-68) | verified. Line 66 is `if dest_file.exists() and not force:`, line 67 is `skipped.append(src_file.name)`, line 68 is `continue`. |
| 2 | file:line | `src/superclaude/cli/install_core.py:85` | verified. Line 85 is the f-string `Skipped {len(skipped)} existing files (use --force to overwrite):`. It is the skip message inside `messages.append(` (line 84). |
| 3 | file:line | `src/superclaude/cli/main.py:178` (with 179) | verified. Line 178 is `core_success, core_message = install_core_files(force=force)` and line 179 is `click.echo(core_message)`. |
| 4 | file:line | `src/superclaude/cli/main.py:365` (with 366) | verified. Line 365 is `core_success, core_message = install_core_files(force=True)` and line 366 is `click.echo(core_message)`. |
| 5 | file:line | `docs/getting-started/installation.md:363` | verified. The quoted sentence is present. The same text also supports the Documentation Context bullet. |
| 6 | file:line | `tests/cli/test_how_we_work_install.py:66` (with 73-75) | verified. Line 66 is the exact call with `force=False`. Lines 73-75 are the loop asserting `path.is_file()` and `path.read_bytes() == data`. |
| 7 | file:line | `docs/getting-started/installation.md:363` (Documentation Context repeat) | verified, same content as #5. |

## Dropped citations

| # | Type | Location | Reason | Recommended action |
|---|------|----------|--------|--------------------|
| none | | | | |

## Passed-through citations (command, allow_command_reexec=false)

| # | Command | Note |
|---|---------|------|
| 1 | `uv run python .dev/troubleshoot/untyped-install-core-files-skips-files-20261031153823/update-counter.py` (Evidence 7) | not re-executed by policy. The quoted denial text cannot be checked from files. `audit.log:34` independently records the denial in compatible wording ("denied by session dontAsk permissions") and says nothing ran. The report claims no execution output, which matches. |

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| A1 | no | - | - | The Summary and Diagnosis contain no definite enum token (Root cause is `UNDETERMINED`; `REPORT.md.draft:32`). `calibration_paths` is empty, so the max-calibrated clause is unknown. Confidence 0.0 is a declared sentinel, not a calibration. `observation_paths=[]` is an empty corpus, but with no definite token there is nothing to be unobserved. |
| A2 | skipped | - | - | input absent: `diff_path` is null |
| A3 | no | - | - | `Date: 2026-10-31T15:41:34Z` (`REPORT.md.draft:13`) is earlier than the draft mtime 15:43:37Z, so it is not later than mtime + 5 min, and it is not `T00:00:00Z`. "Duration: pending final timestamp" carries no timestamp. |
| A4 | yes | `verdict_not_in_contract` | partial | `REPORT.md.draft:80` says "HC0 not run: applicability unassessed" and gives no `pipeline_hardening_verdict` token from {pass, blocked, advisory, not_applicable, blocked-on-authorization}. Caveat: the rule text does not say what an absent verdict means. I read it conservatively as a firing. It has no status effect because the merged status is already `blocked`. |
| A5 | skipped | - | - | input absent: `candidate-fixes.md` is not in the run directory (checked by Glob), and there are no hypothesis cards or calibrations. Absence is recorded as a skipped input, not as evidence of consensus. |
| A6 | no | - | - | The draft states no Reference-context literal. `diagnosability-tasklist.md:22` says "No literal reference-context form is asserted." `first_instrumented_run` is unknown for both probes, so the `n/a` exemption was not applied. Core control predictions are "unknown" and are not presented as reference values (`REPORT.md.draft:37`). |
| A7 | no | - | - | `execution-locus.md:2` has RUN-SITE `src/superclaude/cli/install_core.py:85 @ unknown`, which is not `pending-producers`. `producers.md:2` has `producer-count: 0` and no data rows. |
| A8 | no | - | - | `execution-locus.md:4` has OBSERVE-VIA `nobody`, not `artifact-file`. No CI failing arm is identified. |
| A9 | skipped | - | - | No literal Reference-context value and no captured reference-arm observation. `CONTROL-PROOF: unknown` (`REPORT.md.draft:37`). Skipping does not certify a control. |
| A10 | no | - | - | `diagnosability-tasklist.md:4` has `capability-verdict: n/a`, so the blocked-verdict trigger is absent. The Emitter search block in the same file (lines 8-12) reports `usable-capture-routes: 1`. |

## Notes

- Absent inputs: `calibration_paths` (empty), `diff_path` (null), `observation_paths` (empty), `candidate-fixes.md` (not present), and per-probe `first_instrumented_run` (unknown). Skipped assertions: A2, A5, A9. The A1 max-calibrated clause was not evaluable. Records: `assertion_skipped: A2 (diff_path)`, `assertion_skipped: A5 (candidate-fixes.md)`, `assertion_skipped: A9 (no reference-arm observation or literal)`.
- No snippet sits at a different line from the one cited. No citation falls in a comment or docstring where it was cited as executable code.
- The draft's non-citation claims check out against the sources I read. Both callers print the returned message (`main.py:179`, `main.py:366`). The skip message names skipped files and the target (`install_core.py:85-98`). The prior counter value 1 matches `diagnosability-tasklist.md:38` and `audit.log:34`. The 16-file already-read count in the tasklist adds up when counted.
- Out of scope, not verified: the `doc-context.md` line cites to `tests/cli/test_how_we_work_install.py:54` and `:80` are inside the card, not the draft. The draft cites only the card's path.
- The run directory already holds `REPORT.md` and `evidence-validation.md`. I treated both as parent-owned and did not read or flag them. I assumed they will be overwritten at persistence.
- The draft is honest about its limits. It makes no causal claim, so nothing in it is overclaimed beyond what the citations support.

## Self-Audit

- Every evidence line was read at its cited range, and no result was inherited from upstream agents.
- The weakest call is A4, where the contract is silent on an absent verdict. Treating it as not fired would not change the outcome: the merged status stays `blocked` and the citation result stays PASS.
- No files were written, no commands were run, and no Skill was invoked.
