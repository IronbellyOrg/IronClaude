# Evidence Validation Report

**Report under validation**: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/troubleshoot/untyped-install-core-files-skips-files-20261031152443/REPORT.md.draft
**Timestamp**: 2026-10-31T15:29:48Z
**Total citations**: 8 (7 numbered Evidence items; item 5 holds two separate locations, `main.py:178-179` and `main.py:365`)
**Verified**: 8
**Dropped**: 0
**Passed through (command, no reexec)**: 0
**Suggested report status**: success. This covers only the citation and structural gates. It does not certify runtime behavior and is not a verdict on the incident. The draft is deliberately `partial`, and the parent keeps that status regardless of this suggestion.

## Verified citations

I read each range from scratch in this turn. The snippets match semantically, and each sits in executable code, not a comment or docstring.

| # | Type | Location | Verdict |
|---|------|----------|---------|
| 1 | file:line | `src/superclaude/cli/install_core.py:29` | verified. Line 29 is `    target_path: Path = None, force: bool = False` inside the `install_core_files(` signature, which opens at line 28. |
| 2 | file:line | `src/superclaude/cli/install_core.py:66-68` | verified. The lines are `if dest_file.exists() and not force:`, `skipped.append(src_file.name)` and `continue`. |
| 3 | file:line | `src/superclaude/cli/install_core.py:83-88` | verified. Lines 83-88 build `⚠️  Skipped {len(skipped)} existing files (use --force to overwrite):` and then list each skipped name. |
| 4 | file:line | `src/superclaude/cli/install_core.py:100` | verified. Line 100 is `success = len(failed) == 0`, so `skipped` does not affect the flag. The "skipping alone is not failure" gloss holds. |
| 5a | file:line | `src/superclaude/cli/main.py:178-179` | verified. Line 178 is `core_success, core_message = install_core_files(force=force)` and line 179 is `click.echo(core_message)`. `force` is the `install` command's `--force` option (declared at line 36, parameter `force: bool` at line 46). |
| 5b | file:line | `src/superclaude/cli/main.py:365` | verified. Line 365 is `core_success, core_message = install_core_files(force=True)`. It sits under the "Updating core framework files" block, so the "update" gloss holds. |
| 6 | file:line | `tests/cli/test_how_we_work_install.py:53-75` | verified. This is `test_install_never_touches_existing_files_without_force`. It seeds files, calls `install_core_files(..., force=False)` and `install_commands(..., force=False)`, and asserts the bytes are unchanged. The "not-run" state is the author's own claim and is consistent with `tier1-observation.md:5`. |
| 7 | file:line | `docs/getting-started/installation.md:263` | verified. The table row is `` `--force` | `superclaude install --force` | Overwrite existing files ``. |

## Dropped citations

| # | Type | Location | Reason | Recommended action |
|---|------|----------|--------|--------------------|
| none | none | none | No line-mismatch, file-missing or snippet-mismatch was found. | none |

## Passed-through citations (command, allow_command_reexec=false)

| # | Command | Note |
|---|---------|------|
| none | none | The Evidence section cites no command and output pairs. The draft's "no installer runs or tests performed" matches `tier1-observation.md:5`; I cannot independently confirm it. |

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| A1 | no | — | — | The first conjunct (a definite enum token in Summary or Diagnosis) fails. `REPORT.md.draft:13` says "No unique cause is established". `REPORT.md.draft:24` says "Root cause: UNDETERMINED". `REPORT.md.draft:25` qualifies the cause class as "a conditional explanation, not a proven incident cause". The max calibrated value is 0.30 (`tier1-calibration.md:39`), which would satisfy the second conjunct, but the first one fails. The observation corpus is empty (`observation_paths=[]`, `tier1-observation.md:3`), so any definite token would count as unobserved. See the borderline note in Notes. |
| A2 | skipped | — | — | input absent: `diff_path` (null). No diff means no collector or invocation-site change to check. For information only, the draft does carry the linked row `capture` and the pending reasons (`REPORT.md.draft:27`, `REPORT.md.draft:50-52`). The required "stays `partial` until" form is at `REPORT.md.draft:50`. |
| A3 | no | — | — | `Date` is 2026-10-31T15:24:43Z (`REPORT.md.draft:11`). That is earlier than the draft mtime of 15:29:43 and is not T00:00:00Z. Calibration `Timestamp` 15:27:29Z (`tier1-calibration.md:6`) is earlier than its mtime of 15:29:36. Hypothesis `Timestamp` 15:24:43Z (`tier1-hypothesis.md:4`) is earlier than its mtime of 15:27:29. |
| A4 | no | — | — | `REPORT.md.draft:56` has `Closure verdict: not_applicable`, which is in the contract set. The table decisions at lines 60-61 are also `not_applicable`. |
| A5 | skipped | — | — | input absent: `candidate-fixes.md` (not in the run directory per Glob). The calibration states `evidence_class: source_static` (`tier1-calibration.md:10`), but no consensus claim exists anywhere in the artifacts (grep for "consensus" and "adversarial_invoked" returned no matches). The draft asserts no fix at `REPORT.md.draft:39`. |
| A6 | no | — | — | No Reference-context value exists to validate. Grep for "reference-context" across the run directory returned no matches. The control row has no literal expected value, only "Unknown: no passing arm identified" (`diagnosability-tasklist.md:18`). `first_instrumented_run={}` is unknown, so no `n/a` exemption was applied or needed. |
| A7 | no | — | — | RUN-SITE is `src/superclaude/cli/install_core.py:66-68 @ unknown` (`execution-locus.md:3`), not `pending-producers`. `producers.md:3` has `producer-count: 0`, so both conjuncts are false. |
| A8 | no | — | — | OBSERVE-VIA is `nobody` (`execution-locus.md:5`), not `artifact-file`. No CI failing arm is identified (`execution-locus.md:2-4`), and no `job-*.log` exists in the run directory. |
| A9 | no | — | — | No literal Reference-context value exists and no reference-arm observation was captured (`comparator=none`, `diagnosability-tasklist.md:13`). Per the rule, the comparison is exempt for an unobserved reference. This does not prove a control. |
| A10 | no | — | — | `capability-verdict: n/a` (`diagnosability-tasklist.md:5`), so the rule's precondition (blocked) is not met. For information, the Emitter search block exists with `usable-capture-routes: 1` (`diagnosability-tasklist.md:7-11`). |

Fired consequences: none. No partial, blocked or FAIL contribution comes from the A-rules. No timestamp line is recommended for dropping.

## Notes

- **A1 borderline.** The Diagnosis line "Cause class: Other: ..." carries a catch-all enum value. I treated it as not a definite headline token, because the headline is UNDETERMINED and the line says it is not a proven cause. If the parent reads "Other" as the token, A1's consequence is partial, which the draft already carries. Status would not change.
- **Skipped inputs.** `assertion_skipped: A2 (diff_path)`. `assertion_skipped: A5 (candidate-fixes.md absent from output_dir)`. These are skips, not passes.
- **Observation corpus.** `observation_paths` is empty. The A1 observation-corpus clause is therefore inapplicable, since there is no captured failing-run output and no token to look up.
- **Extra citation outside Evidence.** `REPORT.md.draft:61` cites `install_core.py:54-74`. I checked it and it holds. Line 54 is `core_files = sorted(core_source.glob("*.md"))`, lines 63-68 are the preserve branch, and lines 70-74 are the copy and failure branch.
- **Cross-artifact consistency (not citations).**
  - Confidence 0.30 matches `tier1-calibration.md:39`.
  - Diagnosability verdict partial, complexity trivial and round 1 of 3 match `diagnosability-tasklist.md:3-4` and `diagnosability-context.md:4-7`.
  - Locus fields match `execution-locus.md:5-7`.
  - The producer count of 0 matches `producers.md:3`.
- **Snippet at a different line.** None. Every snippet sat at its cited line.
- **Source freshness.** I read all cited source files in this turn. The `git status` snapshot given to me was truncated, so I cannot say whether any cited file changed after my read.
- **Sibling `REPORT.md`.** A `REPORT.md` already exists in the run directory (it appeared in the Glob). It was not among my inputs and I did not read it.
- **Scope.** This validation covers citation accuracy and structural rules only. I executed nothing. The report's explanation is a source-level reading. It is not proof of what happened in the user's unobserved run. The incident cause remains undetermined, as the draft says.
- **Upstream agents.** No dropped citations, so no upstream agent should be penalized.

## Self-Audit (zero-findings pass)

- **Snippet match.** I compared each of the 8 locations to the draft's quoted text and paraphrase, including the paraphrased claims. Examples are "skipping alone is not failure" against line 100, and "update passes force=True" against line 365 plus the "Updating" echo at line 360.
- **Comment and docstring trap.** The docstring at `install_core.py:39` ("force: Force overwrite if files already exist") is not what the draft cites. All cited install_core lines are executable code, and the test and doc citations are code and a table row.
- **Line drift.** I checked adjacent line numbers for off-by-one errors. Line 100 is the `success =` line and line 101 is the `return`. The calibration cites 101 for the return, and the draft's 100 for `success` is correct.
- **Variable provenance.** For `main.py:178`, I confirmed that `force` is the CLI option (`main.py:36`, `main.py:46`) and not a local value.
- **Rule inputs.** I Read or Globbed every input for A1-A10 before marking a rule skipped or not fired, and searched the run artifacts for rule-specific tokens. The searches (reference-context, consensus, adversarial_invoked, pending-producers, artifact-file, job-*.log) returned zero matches.
- **Limits.** I did not execute anything, so runtime behavior is not certified. The "not-run" test state and the "no installer run" claim rest on the author and on `tier1-observation.md`.

---
*End of report. The parent persists everything above this line to `evidence-validation.md`.*

| DONE | NEXT |
|---|---|
| All 8 Evidence citations match the source. No drops. A1-A10 evaluated, with A2 and A5 skipped for missing inputs. | Parent writes the report above to the sibling `evidence-validation.md` and keeps the draft's `partial` status. |
