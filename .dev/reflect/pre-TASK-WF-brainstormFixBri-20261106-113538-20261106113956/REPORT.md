```yaml
contract_version: 1.8.0
status: partial   # the evidence gate dropped 1 citation (in confirmation OK-2, not in a finding); a dropped citation forces partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.80   # blind score of the Tier 1 card; reviewer cards scored 0.74, 0.81, 0.81
citations_total: 106
citations_revalidated: 106    # the validator re-read 105; the one command result it could not re-run was re-run by the orchestrator and the merge executor
citations_dropped: 1
citations_dropped_extrapolated: 1
citations_inferred: 2         # M-09 and M-10
citation_budget_policy: full_reread   # every citation re-read, although the count is above 20
coverage_degraded: parsed-sparse
```

# Pre-execution reflection: brainstorm nested-analyze plan built from the amended brief

Spec (brief): `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/source.md` (the owner-amended brief, Part 4 amended 2026-11-06)
Tasklist: `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/TASK-WF-brainstormFixBri-20261106-113538.md` (7 tasks, 4 phases)
Paths are relative to the repository root. `plan:N` is line N of the tasklist, `source:N` line N of the brief, `spec:N` line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, `SKILL.md:N` of `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `analyze.md:N` of `src/superclaude/commands/analyze.md`, `qa.md:N` of `~/.claude/skills/sc-implement-protocol/refs/qa.md`, `lc10-result.md:N` of `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc10-result.md`. The full merged result is `adversarial/merged-verdict.yaml` in this folder; where this report narrows a merged finding (evidence gate), this report wins.

## Verdict

The plan can run under `/sc:implement` as written: no finding blocks execution (no P1), every task's anchors match the files on disk, and the five texts the plan copies from the brief are byte-exact (`plan:38`, `:54`, `:69`, `:122`, `:128` equal the quoted spans of `source:231`, `:232`, `:233`, `:223`, `:219`). The owner amendment did its job: the live-check sentence now requires the nested analyze folder only after an actual `Skill` call that invokes `sc:analyze`, so a `Task` prompt that only names the command no longer triggers it.

One P2 should be fixed before running. The brief says each task's acceptance criteria "must contain a check equivalent to its verifier" (`source:34`), and the F-1 and F-3 verifiers are byte-for-byte checks (`source:45`, `source:71`). No current acceptance criterion compares the whole copied text, so an executor that drops a clause of the long spec sentence (for example the `skipped` carve-out) would pass every Task 6 check; no test reads the spec. The fix (M-01) is four added acceptance criteria, tested read-only below.

Everything else is P3: six small plan edits and five owner items.

## How the review ran

- Tier 1 scored 0.80 in a blind re-grade (self 0.90), below the 0.85 floor, so rule 6 escalated to Tier 2. The brief's labels (`F-n`, `INV-n`) do not match the strict ID pattern, so strict parsing found 0 labelled requirements against 45 inferred ones; the sparse-labels guard (`coverage_degraded: parsed-sparse`) forbids a Tier 1 stop either way.
- Three read-only reviewers audited the plan: sonnet (analyzer lens), the haiku slot (qa lens) and opus (refactorer lens). Blind re-grades: 0.74, 0.81, 0.81. Every model class was already a reviewer, so calibrators ran on opus and calibrator diversity is degraded. The model that wrote the plan was not identified (`executor_class_resolved: false`).
- Orchestrator evidence gathered before the debate: E-1 `git status` shows none of the six plan files modified and only this package untracked under `.dev/tasks`; E-2 `make lint` exits 0 and `ruff format --check` is clean on the two test files and the two unrelated modified files; E-3 the per-task reviewer of `/sc:implement` gets the task text and checks "explicit instructions on the task" (`qa.md:9`, `qa.md:13-17`, `qa.md:21`); E-4 the five copied texts are byte-exact substrings of the brief.
- A three-advocate debate (each advocate on its card's model) over 22 differing points converged 22 of 22 in two rounds. The invariant probe found 0 HIGH and 3 MEDIUM items; all three concern the M-01 check itself (one path base, an extraction self-check, a backtick in one command) and are folded into M-01's text. Base card: the qa card (0.897; opus 0.825, sonnet 0.788).
- The evidence gate re-read all 106 citations: 101 supported, 3 narrowed, 1 dropped. The input files did not change during the run (tree hash `3567a459...` before and after).

## Coverage matrix

| Brief span | Plan task(s) | Result |
|---|---|---|
| Part 1: say the fallback tier writes no nested folder, in skill, command file and routing ref | Tasks 1, 2, 3 | matched |
| Part 1: pin the wording in tests | Tasks 4, 5 | matched |
| Part 1: sync copies, check the plugin copy | Task 7, Constraints | matched |
| Part 1: record the corrected live-check wording | Task 6 | matched; acceptance checks are substring pins only (M-01) |
| Part 1: run tests and lint | Task 7 | matched; lint passes today (E-2) |
| Part 2: keep 7 tasks in 4 phases | whole plan | matched |
| Part 3: 17 corrections F-1 to F-17 | Tasks 1 to 7, Constraints | all applied; 3 verifiers fail on wording only (see the next section) |
| Part 4: copy the texts exactly; record the residual risks | Tasks 1 to 3, 6 | texts byte-exact; risks 1, 2 and 4 paraphrased (M-02) |
| Part 5: open conflict, start state, six files, installed-text rule, UV | Constraints | matched |

Parsed requirement rows: 0 (`coverage_pct: null`). Inferred rows: 45, matched 39 (`coverage_pct_union: 0.8667`, `s_dev_density: 0.1333`). Matrix: `artifacts/coverage-matrix.yaml`. This run added rows for Part 2, the Part 3 preamble and all of Part 4, which the previous review's matrix lacked.

## Inferred requirements (Pass 2)

Thirty-nine of the 45 inferred rows matched a task by the containment rule (threshold 0.6). The six that did not are covered in other words:

| INF id | Brief line | Match result |
|---|---|---|
| INF-002 | `source:11` | ratio 0.593: covered by Tasks 4 and 5 together |
| INF-007 | `source:20` | ratio 0.550: 7 tasks in 4 phases (plan structure) |
| INF-008 | `source:34` | ratio 0.417: verifier-equivalent checks; checked per correction below, one gap (M-01) |
| INF-020 | `source:159` | ratio 0.583: F-12, covered by the shared pins in Tasks 4 and 5 |
| INF-026 | `source:215` | ratio 0.595: the amendment note, reflected in Constraints (`plan:20`) |
| INF-035 | `source:239` | ratio 0.500: "no known false FAIL", stated at `plan:133` |

No INF row was dropped by the evidence gate.

## Per-correction verifier check

Each correction's printed verifier, held literally against the plan (from the qa reviewer's card, confirmed in the debate):

| Correction | Result | Plan lines | Note |
|---|---|---|---|
| F-1 | pass | 122, 128, 131 | both sentences byte-exact; deviation recorded |
| F-2 | pass | 33, 44, 153, 158 | |
| F-3 | pass | 38, 54, 69, 87, 88, 108 | |
| F-4 | pass | 85, 87, 90, 93 | |
| F-5 | pass | 60, 85, 88, 93 | |
| F-6 | pass | 153, 157 | |
| F-7 | wording fail | 144 | an extra negative check beyond "exactly these pins"; keep it and record it (M-03) |
| F-8 | pass | 103, 109 | |
| F-9 | pass | 51, 61 | |
| F-10 | pass | 85, 101, 105 | |
| F-11 | pass | 140 | |
| F-12 | wording fail | 87, 88, 108 | the brief contradicts itself (M-12); the plan is right |
| F-13 | pass | 153 | |
| F-14 | wording fail | 45 | the absence check quotes the phrase it forbids (M-04) |
| F-15 | pass | 54 | |
| F-16 | pass | 25 | |
| F-17 | pass | 22 | |

## Findings

| ID | Priority | Finding | Evidence |
|---|---|---|---|
| M-01 | P2 | No acceptance criterion compares the whole copied text for Tasks 1, 2, 3 and 6, while the brief requires a check equivalent to the byte-for-byte verifiers. The other criteria are substring pins, diff shapes, existence checks or test runs. | `source:34`, `source:45`, `source:71`, `plan:44-47`, `plan:60-62`, `plan:75-77`, `plan:143-145` |
| M-02 | P3 | Residual risks 1, 2 and 4 are paraphrased (INV-022 and INV-023 dropped, spec line references turned into prose, "INFERRED" lower-cased), against Part 4's "copy exactly". Risk 4 is true as written (`spec:300`), so copy it, do not narrow it. | `source:213`, `source:240-244`, `plan:134`, `plan:135`, `plan:137` |
| M-03 | P3 | Task 6's second criterion adds a check that the old trigger wording is gone, beyond F-7's "exactly these pins". Keep it: three of the four positive pins are also in the old sentence (`.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/source.md:217`), so they cannot tell old from new. Record the departure. | `source:109-111`, `plan:144`, `plan:131` |
| M-04 | P3 | Task 1's criterion quotes "only for a nested command that ran" to say it is absent, so Task 1 contains the literal F-14 says it must not. Keep the check, write it as a regex. | `source:181`, `plan:45` |
| M-05 | P3 | Task 3 is the only wording task without a diff-shape criterion; text added on a new line after the bullet would pass every Task 3 and Task 5 check, because the test reads the whole section. | `plan:74-77`, `plan:46`, `plan:61`, `plan:145`, `tests/skills/test_worker_contract.py:483-496`, `:508-509` |
| M-06 | P3 | Task 5's HEAD check lacks the `git cat-file -e` guard Task 4 has (a wrong path prints 0 and passes); Task 4's "the pins fail" claims more than its greps test. | `plan:95`, `plan:111` |
| M-07 | P3 | No Task 7 log is told to record an exit status, and the pytest criterion has no exit wording. | `plan:153`, `plan:156-157` |
| M-08 | P3 | Review artifact: the coverage matrix has no rows for the 17 verifier lines; the per-correction table above fills that gap. No plan change. | `artifacts/coverage-matrix.yaml`, `source:45`, `source:111`, `source:161`, `source:181` |
| M-09 | P3 owner | [INFERRED] Spec 7.2 step 5 condition 2 wants the command call at the top level; the lc10 record applied it to nested calls; the skill runs enrichment through `Task` agents, and the amended sentence accepts the analyze call in a subagent file. A checker that follows lc10 would fail a correct run. | `spec:296`, `lc10-result.md:13`, `SKILL.md:183`, `plan:128` |
| M-10 | P3 owner | [INFERRED] `/sc:analyze` reports a refused directory only in chat, so "did not refuse that directory" is judged from chat text; a checker that misses it requires a folder that was never written. With M-09 this qualifies the brief's "no known false FAIL". The `--report-dir` match is literal (a relative path is missed: false PASS). | `analyze.md:97`, `plan:128`, `plan:133`, `source:239` |
| M-11 | P3 owner | "is required ... only when" states a necessary condition, not "exactly when". | `source:219`, `plan:128` |
| M-12 | P3 owner | F-12's verifier says every F-3 pin contains `no nested directory and no nested contract`, but F-3 also requires the separate ``only by a `/sc:analyze` call`` pin. Brief defect; the plan keeps both pins. | `source:63`, `source:68-69`, `source:161`, `plan:87-88`, `plan:108` |
| M-13 | P3 | Hardening notes for M-01: `grep -c` counts lines, not occurrences; never hard-code `.dev/tasks/to-do/` in a check, because the package moves to `done/`. | `adversarial/invariant-probe.md` (INV-006, INV-014) |
| M-14 | P3 owner | Carried from the previous review: research enrichment from P2 is an open conflict; no pointer for the P2 author to the new 7.2 step 4 sentence; the routing bullet's "with this tier's `quality_tier`" against a timeout's `skipped`; the companion sentence's installed twin is not edited. | `plan:26`, `plan:54`, `.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-021737/REPORT.md:83`, `:84`, `:107`, `:108`, `reflection-card.yaml` F-4 |

Confirmations (no defect): the five copied texts are byte-exact (E-4); the task anchors match the files (SKILL.md line 195 and its blank line 196, routing-ref lines 16, 22, 24, 31 and 33, `brainstorm.md:157`, `spec:62`, `spec:286`); Task 5's "+2 cases" holds (`tests/skills/test_worker_contract.py:519-531`); the five new acceptance-check extractions are non-empty and fail before the edit; `make lint` passes today; the amended sentence no longer fails the lc10 case.

## Fix text for M-01 (tested)

Add one criterion to each of Tasks 1, 2, 3 and 6. All run from the repository root, with `S` set to this package's `source.md` (do not hard-code `to-do/`):

- Task 1: "With `S` set to this package's `source.md` and the command run from the repository root, `X=$(sed -n '231s/.*with: "\(.*\)" Task 1 AC.*/\1/p' "$S")` is non-empty, `grep -cxF -- "$X"` on this plan prints 1, and `grep -cF -- "$X" src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` prints 1."
- Task 2: "With `S` as in Task 1, `X=$(sed -n '232s/.*31): "\(.*\)" .grep.*/\1/p' "$S")` is non-empty, `grep -cxF -- "$X"` on this plan prints 1, and `grep -cxF -- "$X" src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` prints 2."
- Task 3: "With `S` as in Task 1, `X=$(sed -n '233s/.*bullet: "\(.*\)" Leave.*/\1/p' "$S")` is non-empty, `grep -cxF -- "$X"` on this plan prints 1, and `grep -cF -- "$X" src/superclaude/commands/brainstorm.md` prints 1."
- Task 6: "With `S` as in Task 1, `X=$(sed -n 223p "$S")` and `Y=$(sed -n 219p "$S")` are non-empty, `grep -cxF` on this plan prints 1 for each, and `grep -cF` against `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` prints 1 for each."
- Task 6 body, appended to the deviation paragraph (`plan:131`): "The whole-text check in the acceptance criteria is required by the brief's rule that each correction's verifier has an equivalent check; it is not one of the pins correction F-7 lists."

Tested read-only on 2026-11-06 from the repository root: extraction lengths 412, 261, 361, 450 and 1210 characters; each matches its fenced line in the plan once; every target file prints 0 today, so each new check fails before the edit and passes only on an exact copy.

The small P3 plan edits (exact texts in `adversarial/refactor-plan.md`, Changes 2 to 7):
- M-02: replace `plan:134`, `:135`, `:137` with the texts of `source:240`, `:241`, `:243` after their numbers, as `- ` bullets (the workflow gate forbids numbered lines, `~/.claude/skills/sc-workflow-protocol/refs/quality-gates.md:29`).
- M-03: append to `plan:131`: "Task 6's second acceptance criterion also checks that the old trigger wording ``a `Skill`, `Agent` or `Task` tool call`` is gone; this goes beyond the pins correction F-7 lists, on purpose, because three of the four positive pins are also in the old sentence."
- M-04: in `plan:45`, replace `and does not contain "only for a nested command that ran".` with ``and a regular-expression search for `only for a nested command that r[a]n` finds nothing in it.`` (tested: the pattern matches the old literal).
- M-05: add to Task 3: "`git diff --stat -- src/superclaude/commands/brainstorm.md` shows one line changed (one insertion, one deletion)."
- M-06: append to `plan:111`: ", and `git cat-file -e HEAD:src/superclaude/commands/brainstorm.md` exits 0"; in `plan:95` replace "which shows the pins fail" with "which shows the shared directory pins fail".
- M-07: in `plan:153`, after the status-after sentence, insert "Append the line `exit=<status>` after each command's output in its log."

## Invariant probe disposition

| Item | Severity | Disposition | Status |
|---|---|---|---|
| INV-001 | MEDIUM | M-01 runs every path from the repository root with `S` = the package's `source.md` | addressed in the fix text |
| INV-002 | MEDIUM | M-01 checks each extraction is non-empty and equals its fenced plan line | addressed in the fix text |
| INV-015 | MEDIUM | with INV-001, INV-002 and INV-003 folded in, no other blocker found | addressed |
| INV-003 | LOW | Task 2 regex uses `.grep` instead of a backtick | addressed in the fix text |
| INV-006, INV-014 | LOW | hardening notes (M-13) | open, notes only |

The other nine probe rows were already addressed (see `adversarial/invariant-probe.md`).

## Dropped by validation

One citation was dropped: `adversarial/variant-2-original.md:155` in confirmation OK-2 (the line describes the brief's slicing pattern, not an on-disk anchor check). OK-2 stands on the other two cards. Three citations were narrowed (M-05, M-07, M-14) and five claims corrected (M-01, M-02, M-03, M-04, OK-4); this report carries the corrected forms. Details: `artifacts/evidence-validation.md`.

## Open items for the owner

- M-09 (top): decide that spec 7.2 step 5 condition 2 applies to the command under test only, and tell the P2 live-plan author.
- M-10: decide whether brief Part 4 gains two residual risks (the missed refusal, the condition-2 scope) and a narrower "no known false FAIL" lead-in. The plan copies Part 4 and cannot change it alone.
- M-11: optional: "exactly when" instead of "only when" in the live-check sentence.
- M-12: none needed for this plan; fix the F-12 verifier wording in future briefs.
- M-14: research enrichment from P2 (INV-021), the pointer for the P2 author (INV-020), the routing bullet's tier wording, the installed contract twin.
- The earlier plan packages `TASK-WF-brainstormFixBri-20261106-001016` and `TASK-WF-brainstormFixBri-20261106-021737` are still in `.dev/tasks/to-do/` and staged; two stale packages beside this one can confuse a later `/sc:implement`.

## Unverified

- How Claude Code's session file records a `Skill` call's input and a tool error (residual risk 2 in the plan).
- Whether any real checker misses a chat-only refusal (M-10) or reads condition 2 the lc10 way for nested calls (M-09); both are inferred from the documents, not reproduced.
- The planned edits were not executed; tests were read against the planned text, not run on it.

## Inferred-claim audit

- `citations_inferred: 2` (M-09, M-10). 2 of 106 citations; well under the half-of-total warning threshold.

## Recommendations

### Recommendation R-001: Add the whole-text checks before running the plan
- **File:** `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/TASK-WF-brainstormFixBri-20261106-113538.md` (Tasks 1, 2, 3 and 6)
- **Change:** add the four criteria and the one Task 6 sentence in "Fix text for M-01". This review does not edit the plan; edit it by hand, or regenerate with an instruction to include them.
- **Verifier:** each new criterion's extraction is non-empty and matches its fenced plan line once (`grep -cxF` prints 1); before execution every target count is 0.
- **Linked deviation(s):** none (proactive, M-01)
- **Priority:** P2

### Recommendation R-002: Apply the six small plan edits in the same pass
- **File:** the same plan (`plan:45`, `:95`, `:111`, `:131`, `:134`, `:135`, `:137`, `:153`, Task 3 criteria)
- **Change:** M-02 to M-07 as listed above.
- **Verifier:** each edit's verifier in `adversarial/refactor-plan.md` (Changes 2 to 7) passes; the plan still passes the workflow gate (no numbered or checkbox lines).
- **Linked deviation(s):** none (proactive)
- **Priority:** P3

### Recommendation R-003: Owner decisions before the P2 live plan
- **File:** n/a (owner); later the brief Part 4 and the spec's section 7.2
- **Change:** decide M-09 and M-10 (and optionally M-11); record INV-020 and INV-021 for the P2 author.
- **Verifier:** the decisions are written where the P2 live-plan author reads them.
- **Linked deviation(s):** none
- **Priority:** P3
