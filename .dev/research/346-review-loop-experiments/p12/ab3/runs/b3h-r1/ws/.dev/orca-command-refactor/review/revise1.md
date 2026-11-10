# REVISE round 1 (revise1)

- Candidate (edited in place): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- Brief: `.dev/orca-command-refactor/review/round1.md:196-200` (Reviser brief: blocking ids F-01, F-02, F-03, F-04, F-05, F-06). Round-1 candidate sha256 matches `review/round1.md:7` (`d3cdbe57...425200d`).
- Prompt: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full).
- Evidence: the three inventory files and the round-1 report only. Citations to other files (`command.md`, `src/superclaude/...`) are marked UNVERIFIED.
- Scope: only the six ids. No Medium or minor finding (F-07 to F-15, m-01 to m-03) was edited. No review was run. No PASS is claimed.
- Line numbers below are the revised spec's; the edits did not change any line count.

## Byte accounting

| State | Bytes | sha256 |
|---|---|---|
| Before | 57763 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| After | 59746 | `e1f78b891d8bb255eebfc49ad5aa8456501e35c3ff87d61c58e99699e8350b62` |
| Net | +1983 | (deleted 1418, added 3401; check 57763 + 1983 = 59746) |

Per edit, gross bytes (edit location, finding):

| Edit (spec line) | Finding | Deleted | Added | Net |
|---|---|---|---|---|
| A: WC-4 contract sentence (:62) | F-01 (also carries the F-02 flag clause and the F-03 sub-path clause) | 166 | 508 | +342 |
| D: section 3 "Contract" note (:76) | F-01 | 67 | 83 | +16 |
| I: tdd row (:90) | F-01 | 73 | 110 | +37 |
| K: spec-panel row (:120) | F-02 | 86 | 275 | +189 |
| E: SA-3 (:148) | F-03 | 63 | 299 | +236 |
| J: workflow row (:92) | F-03 | 73 | 106 | +33 |
| B: WC-11 (:69) | F-06 | 240 | 541 | +301 |
| C: section 2.3 (:73) | F-06 | 112 | 233 | +121 |
| G: index-repo row (:86) | F-06 | 34 | 148 | +114 |
| H: init-lite row (:87) | F-06 | 130 | 257 | +127 |
| M: AC-0.4 (:194) | F-04 | 105 | 390 | +285 |
| L: AC-C1 (:172) | F-05 | 269 | 451 | +182 |

Per finding id: F-01 306 deleted, 701 added (includes edit A). F-02 86 / 275 (edit K; the flag clause inside edit A is counted under F-01). F-03 136 / 405. F-04 105 / 390. F-05 269 / 451. F-06 516 / 1179. Totals 1418 / 3401, matching the file-size change.

## Findings

| Id | Status | Where applied (revised spec) | Basis and citations |
|---|---|---|---|
| F-01 | Applied | WC-4 (:62): the contract goes in the directory the brief names. A file-valued output (init-lite and tdd `--output <file>`) puts it in that file's directory. A run whose brief omits the flag is refused before work, so WC-5 maps the missing report to `failed`. Section 3 intro (:76) and tdd row (:90) updated. | INV-A:55 (init-lite `--output <file>` or default path); INV-B:47 (tdd TDD file at `--output`). The review's "require a directory default" was not adopted: section 2.3 already requires the brief to state the output directory, so a refusal adds no new default. |
| F-02 | Applied in part; flag name UNVERIFIED | WC-4 (:62) names the directory flag per command. Spec-panel row (:120) names the directory flag its unattended mode uses. | The review says that flag is `--report-dir` (`command.md:459-461`). `command.md` is outside the inventories, so it was not read; the name is marked UNVERIFIED. INV-B:182 says spec-panel has no path and no `--output` flag today, which conflicts with the review's claim. The implementer must confirm the flag from the command before P2 (AC-2.1). |
| F-03 | Applied | SA-3 (:148) names two exceptions: the adversarial contract name (:83, a file a standalone run already writes, INV-A:35) and the workflow pre-creation STOP contract (:92, now written only under `--unattended`). WC-4 (:62) allows a sub-path for adversarial. | INV-A:35 (adversarial contract must be written on every run, no filename named); INV-B:272 (workflow contract not written for pre-creation STOPs). Both checked against the inventories. |
| F-04 | Applied | AC-0.4 (:194): step 3 uses the report path the command already writes (troubleshoot `REPORT.md`; workflow `return-contract.yaml`; adversarial contract). Step 4 runs only `test -s` in P0; the YAML assertion starts in P1. | INV-B:49 (troubleshoot `report_path` REPORT.md); INV-B:52 (workflow `.dev/tasks/to-do/<id>/return-contract.yaml`); INV-A:35,60 (adversarial contract). Disclosure: the step-4 change goes beyond the review's wording (which named only step 3), because REPORT.md is Markdown and fails the YAML assertion. It stays inside AC-0.4, which F-04 names. |
| F-05 | Applied | AC-C1 (:172): alternation with `\|` replaced by four `-e` patterns; `ccsession-tag` excluded with `--exclude-dir` instead of a pipe; `WORKER-CONTRACT.md` excluded by name (SA-2 allows it to name Orca). The HOW-WE-WORK Orca section stays in scope, and the pass cell says it must name no `orca` command. | Pattern tested in the sandbox on sample lines: it matches `orca orchestration`, `orca-ide worktree`, `orca-ide terminal`, `orca agent`, and not plain prose. It was not run against a repository, since none is in the sandbox. |
| F-06 | Applied | WC-11 (:69): each Dispatch writes under its own directory; each `--retry-of` gets a fresh one; index-repo and cleanup-audit are serialised until §3 gives a per-run path. Section 2.3 (:73): the coordinator orders fixed-path Tasks with `--deps`. Init-lite row (:87): a fresh `--output` per Dispatch, including retries. Index-repo row (:86): a per-run output directory flag (P1). | INV-A:55 (init-lite re-run overwrites its marked report); INV-A:53 (index-repo `PROJECT_INDEX.md`, location implied, UNVERIFIED); INV-A:42 (cleanup-audit fixed output directory). The cleanup-audit row already serialises (`:85`) and is unchanged. |

No finding was rejected.

## Decisions

| Decision | Options | Rationale |
|---|---|---|
| F-01: refuse a run with no output flag | Directory default vs refusal | Refusal adds no new default and follows section 2.3, which already requires the brief to state the output directory. |
| F-03: exempt adversarial by name, gate workflow | Exempt both vs gate both | Adversarial already writes a contract on every run (INV-A:35), so renaming it changes only the path. Workflow's new contract is gated, so no standalone file appears. |
| F-04: waive step 4's YAML check in P0 | Waive vs leave | Without it, AC-0.4 cannot pass for troubleshoot (REPORT.md is Markdown, INV-B:49). |
| F-06: add an index-repo output flag | Flag vs serialise only | The flag removes the shared file. Serialising alone would leave the file shared. The flag's existence in the command is UNVERIFIED (INV-A:53). |

## Unverified and disclosed

1. The spec-panel directory flag name (F-02). `command.md` was not read; INV-B:182 conflicts with the review's claim.
2. Index-repo's output location and whether it accepts any directory flag (INV-A:53). The new P1 flag is a change, not a confirmed existing option.
3. AC-C1 was tested on sample lines, not run on the repository.
4. AC-0.4's step-4 change is an extension of F-04 (see table).
