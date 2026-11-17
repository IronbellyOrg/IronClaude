# T1 reflection card (UC-1 pre-execution), re-review of stage 1 plan

Plan: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (243 lines, 4 phases, 16 tasks). `PLAN:n` = line n of that file. Source request: `source.md` in the same folder (38 lines, byte copy of `stage-requests/stage1-request.md`, checked with cmp). Spec: `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` (`SPEC:n` = line n). Shared decisions: `stage-requests/revision2-brief.md`; owner answers: `OPEN-QUESTIONS.md`. First review: `.dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116030453/REPORT.md` (F1 to F9).

## Coverage (Step 1B.0, two passes)

Pass 1 found 0 labeled requirement ids in source.md. Pass 2 (requirements-analyst agent) returned 68 rows, every quote verified verbatim at its cited line by script (`artifacts/pass2-requirements-analyst.yaml`). Mechanical containment (threshold 0.6) matched 44 of 68 (coverage_pct_union 0.6471); the 24 mechanical misses are all covered by a manual read (Constraints block PLAN:18-30 or the task named in the matrix notes) and are listed in the matrix. S_dev_density (mechanical) = 24/68 = 0.3529. The parse-density guard fires (inferred 68 > parsed 0): Tier-1 stop forbidden.

## Check (a): are the first-review findings really fixed in the live plan?

| First-review finding | Live plan evidence | State |
|---|---|---|
| F1 Task 7 grep line has no end point | PLAN:125 now reads "Until Task 10 adds an importer, `grep -rln "follow_ups" src/superclaude/cli/review` lists only `follow_ups.py`. From Task 10 on, the only other files it may list are `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`..."; the words "command wiring" are gone | text fixed; see new finding N1 (the grep itself) |
| F2 stoprule row has no in-repo defining file | PLAN:64 marks the row `installed-only`, names the two `~/.claude/` paths, exempts it from the exists line and T4 (PLAN:70, PLAN:223, PLAN:231); both installed files exist (batch c12) | fixed |
| F3 allow-list narrower than stage 3 scan | PLAN:66 and PLAN:73 list `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py` as `allowed`; both files hold the phrases (batch c09) | fixed |
| F4 ledger mapping decision | PLAN:120 records "Version 1: follow-ups.md stays a separate file ... no mapping to review-ledger/1 rows"; PLAN:22 adds ledger.py to not-built; PLAN:237 reports the verdict | fixed |
| F5 scale-map shape | PLAN:62 fixes columns, pair format, path root, `none`, `installed-only`; Tasks 9, 12, 15 depend on Task 3 (PLAN:144, 182, 221) | fixed |
| F6 Task 10 dependency | PLAN:157 `Depends on: Task 7, Task 9` | fixed |
| F7 Task 11 tests need later code | `run_questions` in Task 9 (PLAN:146), `questions_to_ask` in Task 10 (PLAN:159); safety-route half of T12 in Task 13 (PLAN:196); Task 13 depends on 7 and 9 (PLAN:194) | fixed |
| F8 nits | Task 2 grep uses the full path (PLAN:56); Task 12 names seven subcommands (PLAN:184) | fixed (nit: PLAN:184 says `verify`, the command is named `verify-citations` in `verify_cmd.py`) |
| F9 sweep-flagged | PLAN:81 defines it as a ninth state, no rollout stage named (PLAN:87) | fixed |

## Check (b): new defects introduced by the revision

Mechanical structure (batch d01 to d05): 16 "Acceptance criteria:" labels for 16 tasks; `Depends on` targets are all lower task numbers; no checkbox or numbered-list lines; no absolute paths or `.dev/tasks/to-do/` prefixes; no "never staged" wording.

N1 (candidate, blocking). PLAN:125 acceptance line "lists only `follow_ups.py`" cannot be met as written. `grep -rln` also lists binary files, and `src/superclaude/cli/review/__pycache__/` holds `*.cpython-311.pyc` and `*-pytest-9.2.0.pyc` for every module (batch c01 and d20: the same grep for "ledger" lists 10 `.pyc` files besides the 5 `.py` files). Task 7's first acceptance line runs pytest, which writes `follow_ups.cpython-311*.pyc`, and from Task 10 on the importers' `.pyc` files also contain the name. The check lists extra paths whatever the code does. (`.gitignore:2` ignores `__pycache__/`, so the fix is to restrict the grep to `*.py`.)

N2 (candidate, non-blocking). Task 9 (PLAN:146) makes `ReviewerJudge` read the reviewer's label "through the scale map" from the `labels` column of `refs/scale-map.md`, but the same word has different outcomes in different rows (tasklist Medium is Blocking, `card_convert.py` medium is Note, rf-qa MINOR, auggie Medium). The plan never says which family row a finding's label is read against (the ledger `source`/`origin` columns could key it); Task 12's disagreement matrix (PLAN:184) has the same gap. An implementer must invent the key.

N3 (candidate, non-blocking). Task 3 fixes one outcome per label (PLAN:62: Blocking, Medium, Note), but SPEC:739 gives spec-panel MAJOR as "Blocking only when it names a concrete wrong outcome, else Medium" and SPEC:738 maps `false-claim` more broadly than the rule; a single `LABEL=Outcome` pair cannot hold a conditional mapping.

N4 (candidate, non-blocking). REQ-09 (SPEC:396, cross-run matching of declined, filed and resolved rows) is not named in Task 7 (PLAN:120) or in any T7 failure condition, although the identity tuple is.

N5 (candidate, minor). Task 8 (PLAN:132) takes the repository from `origin_repo.py`, which is a script, not an importable package (`tests/issue_watch/test_origin_parity.py:3`; `cli/issue_watch/launch.py:206` copies its rules), and says nothing about how code calls it or how the tests fake it.

N6 (candidate, minor). Task 4 copies spec sections 6.1 to 6.7; SPEC:485 mentions `.dev/pr-monitor/`, which Task 5's folder-wide grep (PLAN:97) forbids; Task 4 comes first, so the executor must drop it from the copy. The first review dropped this as an executor-avoidable point.

## Check (c): plan against the spec's stage 1 row (SPEC:945)

Stage 1 exit tests T1 to T4, T6 to T8, T11 to T13, T17: T1, T2, T3, T4, T14 in Task 15; T6, T11, T12a in Tasks 9 to 11; T12b and T17 in Task 13; T7 in Task 7; T8 in Task 8; T13 in Task 14. The skill folder, registry (19 rows: 11 digest, 1 canonical, 2 pointer-only, 5 installed-only), ledger codec and writer, fixture judge, property tests and install check are all present. No carrier is edited. Shared decisions 1 (retired carriers), 2 (follow-up carrier), 4 (no plugin surface) and 5 (ledger) are visible at PLAN:24, 25, 26 and 120. Registry paths named in Task 6 exist (batch d11, d12, d13).

## Candidate verdict and self-reported confidence

Candidate verdict: NEEDS-REVISION if N1 is confirmed as blocking, otherwise PASS with notes. Self-reported confidence 0.80. Tier decision inputs: S_scope 16, S_domains 4 (code, tests, docs, config), S_dev_density 0.3529, coverage_degraded parsed-sparse.
