review: 3 of 3

# Re-review of the revised spec (RE-REVIEW prompt, review 3 of 3)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 150cd2160e83032be24b36d6510052c36e52b128ef009a46dab2f911fab14ca3
baseline: .dev/orca-command-refactor/specs/history/spec-v2.md sha256 0e53b436d774ed5d6bf97ec9ffac93472d2f0ec0eb53b20ecebda159b8c5d3e2 (equals the candidate hash recorded in round2.md, so the baseline is the text round 2 reviewed)
prior: .dev/orca-command-refactor/review/round2.md sha256 6f0f74c9cd11d1585521c639d333dea16bf70ae7ae95aae47d71ead7f61d3546 (review: 2 of 3, verdict FAIL)
lint: .dev/orca-command-refactor/review/lint-3.md sha256 c3e0d92d5416188d1db064a9a9b936708f25e973eb38381e9b412e9d79b13a81 (review-lint/1, "No findings"; its header records the candidate hash 150cd2...)
reviewer model: claude-haiku-5-5
coverage: changed lines (diff -w against the baseline: lines 85 and 194) and the nine prior blocking findings M2, M4, M6, M8, M9, M10, M11, M12, N1. Rejected ids M1, M3, M5, M7 are noted, not prior blockers, and are not re-checked.
rf-qa: `.claude/agents/rf-qa.md` (project) and `~/.claude/agents/rf-qa.md` are not in the sandbox (the sandbox home holds only `rules/prompts/document_review_loop_prompts.md`), so the Review Loop rules in this report stand alone (command.md:258).
unattended: not run (no `--unattended` in the brief), so `~/.claude/WORKER-CONTRACT.md` is not read (command.md:457-465).
lint ids: none to address (lint-3 has no findings; lint hash matches the candidate).
VERIFY step: not run, because no open blocking finding remains (document_review_loop_prompts.md, VERIFY prompt).

## Step 1 evidence block

`diff -w BASELINE CANDIDATE` hunks: 85c85, 194c194. No other line differs.

BEFORE (baseline), lines starting `<`:

< | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | M6: the P0 briefs omit `--unattended`, which P1 adds, so the command lines above are the P0 lines. Steps 1, 2, 5, 6 and 7 pass as written; step 5 also shows that no Agent-tool call precedes the command. Step 3 passes when `worker_done` arrives and its report path is the command's existing report (`REPORT.md` for troubleshoot; the existing `return-contract.yaml` for workflow and adversarial, section 3.1 "Report today" column). Step 4 is replaced by `test -s <existing report>`; the YAML key check applies only to workflow's existing contract, which has `status` and no `command` key (`INV-B:272`). Record the results in the phase report; a failure here reopens section 1 |

AFTER (candidate), lines starting `>`:

> | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; add `--output-dir <dir>` in P1 (N1, M2), after which the output directory is no longer fixed, so parallel audits each pass their own `--output-dir` (WC-11) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | M6: the P0 briefs omit `--unattended`, which P1 adds, so the command lines above are the P0 lines. Steps 1, 2, 5, 6 and 7 pass as written; step 5 also shows that no Agent-tool call precedes the command. Step 3 passes when `worker_done` arrives and its report path is the command's existing report (`REPORT.md` for troubleshoot; the existing `return-contract.yaml` for workflow and adversarial, section 3.1 "Report today" column). Step 4 is replaced by `test -s <existing report>` and no YAML key check runs, because workflow's existing contract has `status` and no `command` key (`INV-B:272`), so step 4's `d['command']` assertion (line 183) would raise KeyError on a correct run (M6). Record the results in the phase report; a failure here reopens section 1 |

Self-check (grep -nF, run before the verdict): each AFTER quote was found in the candidate (lines 85 and 194) and each BEFORE quote in the baseline (lines 85 and 194). Roles were not swapped.

Evidence checked for the changed lines:
- Candidate line 183 still asserts `d['command']` (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:183`); line 194 now removes that check for P0 only.
- Line 83 says adversarial's existing contract has an unfixed filename; line 92 says workflow's path is `.dev/tasks/to-do/<id>/return-contract.yaml` with a fresh `<id>` per run; `--package-id` is added only in P1 (line 76).
- `.dev/orca-command-refactor/inventory/commands-b.md:272` lists workflow's contract fields as `status`, `plan_path` and `reflect_report_path`; no `command` field is listed. The refs file it cites (`sk/sc-workflow-protocol/refs/return-contract.md`) is outside the sandbox, so whether the file has no `command` key is UNVERIFIED here. The M6 fix depends on that fact only through this inventory line.
- `.dev/orca-command-refactor/inventory/commands-a.md:42` lists `progress.json` among the `.claude-audit/` outputs. Whether the checkpoint file moves under `--output-dir` is not stated in the spec or the inventory (UNVERIFIED).

## Prior blocking findings (from round2.md)

| id | status | evidence (candidate lines) |
|---|---|---|
| M2 | resolved | Lines 62 and 76 are unchanged in the diff. Line 85 now carries the P1 `--output-dir` flag (N1 fix), which agrees with line 76. No regression. |
| M4 | resolved | Line 185 is unchanged in the diff. |
| M6 | resolved | Line 194 now replaces step 4 for P0 with `test -s <existing report>` and runs no YAML key check. The grading sentence no longer holds: an implementer following line 194 does not assert `command` against workflow's P0 contract. The premise (no `command` key in workflow's contract) rests on `commands-b.md:272` (UNVERIFIED as a file fact, see above). Step 4 at line 183 still asserts `command` for P1 and later, where WC-4 (line 62) requires the field, so no conflict. |
| M8 | resolved | Line 79 is unchanged in the diff. |
| M9 | resolved | Lines 62 and 76 are unchanged in the diff. |
| M10 | resolved | Line 200 is unchanged in the diff. |
| M11 | resolved | Line 201 is unchanged in the diff. |
| M12 | resolved | Line 43 is unchanged in the diff. |
| N1 | resolved | Line 85 now says the `--output-dir <dir>` flag is added in P1 and that the directory is then no longer fixed, which is the fix direction round2.md gave. Line 76 says the same. No contradicting text remains on those lines. |

Regressed: none. Open: none.

## New findings on changed lines (none blocking)

### N2 (origin=changed, line 85; Medium)
- Location: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:85`, "so parallel audits each pass their own `--output-dir` (WC-11)", against `:69` (WC-11: two workers in one worktree must never write the same file).
- Grading sentence: an implementer who follows line 85 and runs two audits with different `--output-dir` values writes `progress.json` to the same place each time only if the checkpoint stays at its fixed location, and the spec does not say where `progress.json` lives. The sentence needs that assumption, so it is Medium and not blocking.
- Evidence: `.dev/orca-command-refactor/inventory/commands-a.md:42` lists `progress.json` among the `.claude-audit/` outputs, which suggests a fixed path (UNVERIFIED: no file of the command was read).
- Follow-up candidate: state the location of the checkpoint under `--output-dir`, or state that it is kept per output directory.

### N3 (origin=changed, line 194 step 3 and the adversarial and workflow rows; Medium)
- Location: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:194` ("its report path is the command's existing report ... the existing `return-contract.yaml` for workflow and adversarial"), with `:83` (adversarial, "contract, but filename not fixed") and `:92` (workflow, `<id>` fresh per run; `--package-id` added only in P1 at `:76`).
- Grading sentence: an implementer who checks P0 step 3 for adversarial or workflow has to choose which file counts as the expected report path, because the spec gives no fixed path before dispatch; the check therefore needs an assumption and is Medium.
- Evidence: `.dev/orca-command-refactor/inventory/commands-a.md:35` and `:60` say earlier runs wrote adversarial's contract in two different places; `commands-b.md:272` gives workflow's path with `<id>`.

### N4 (origin=changed, line 194 restates the step-3 pass rule; Medium)
- Location: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:194` ("Step 3 passes when `worker_done` arrives and its report path is the command's existing report") and `:182` (7.2 step 3, `--timeout-ms 900000`).
- Two points, each needing an assumption: (a) the P0 pass rule drops 7.2 step 3's "exactly one `worker_done`" and "outcome matches the contract's status" conditions, and the spec does not say that this narrowing is intended; (b) the spec does not say what happens if no `worker_done` arrives before the timeout, so the outcome of a stalled P0 run is undefined. Medium, not blocking.

## Guard Condition Boundary Table (changed lines only)

No guard conditions identified on changed line 85. Line 194 contains one pass rule (step 3), graded as N4. No GAP entries are produced on the changed lines, so this table does not block synthesis.

## Follow-up candidates (Medium; not blocking)
- N2 (line 85, progress.json location), see above.
- N3 (line 194 step 3 for adversarial and workflow, unfixed or per-run contract paths), see above.
- N4 (line 194 step 3 narrowing and no timeout outcome), see above.
- Medium items from round2.md (F1 to F5) are not re-graded in this review.

## Notes (minor)
- The M6 fix's premise, that workflow's contract has no `command` key, is supported only by the field list at `.dev/orca-command-refactor/inventory/commands-b.md:272` (UNVERIFIED as a file fact; the refs file is outside the sandbox).
- The changed line 194 still says "the existing `return-contract.yaml` for ... adversarial", which is the same unfixed path noted in N3.

## Result

All prior blocking findings (M2, M4, M6, M8, M9, M10, M11, M12, N1) are resolved on the current candidate, with no regression. No new blocking finding was found on the changed lines (85 and 194). The Reviser brief is omitted at review 3 (command.md:263), and no revision is needed.

scoped PASS: changed lines + prior blockers

verdict: PASS
