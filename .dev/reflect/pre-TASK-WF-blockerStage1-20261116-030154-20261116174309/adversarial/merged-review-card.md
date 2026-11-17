# Merged review card: stage 1 plan TASK-WF-blockerStage1-20261116-030154 (second review)

PLAN is `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md`. SPEC is `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`. PLAN:n and SPEC:n are their line numbers; T-numbers are the spec's tests. Every path:line was re-read during this merge.

<!-- Source: Variant 3 (base), verdict wording per refactor plan -->
## Verdict

NEEDS-REVISION: one blocking finding (M-F1), nine non-blocking (M-F2 to M-F10).

The verdict is not PASS because Task 7's grep acceptance line (PLAN:125) fails under default Python settings right after Task 7's own test run, so a correct implementation cannot meet it as written.

<!-- Source: V3 (base); F1, F5 labels per PC-11 (V1, X-002) -->
## First-review findings

- F1: fixed in text; the grep fails (M-F1). PLAN:125 now has the end point "Until Task 10 adds an importer" and names the allowed importers.
- F2: fixed, PLAN:64, 70, 223, 230-231. The stoprule and `finding-grader` row is `installed-only`, names two `~/.claude/` paths, and is exempt from the exists check and from T4.
- F3: fixed, PLAN:66, 73. Both code files are `allowed`, and `stage3-request.md:14` names both ("`cli/roadmap/remediate_parser.py`, `cli/pipeline/fmea_classifier.py`").
- F4: fixed, PLAN:120, 124, 237. The version 1 decision, the ledger adapters and the Task 16 audit report are stated.
- F5: fixed in text, residual gap M-F2. PLAN:62, 144, 182, 221: columns, path root and the `none` label are fixed, and Tasks 9, 12 and 15 depend on Task 3. The `labels` grammar and the multi-path cell remain open.
- F6: fixed, PLAN:157. Task 10 depends on Task 7 and Task 9.
- F7: fixed, PLAN:146, 159, 171, 196. The question functions precede their tests; T12's second half is in Task 13.
- F8: fixed with a leftover, PLAN:56, 184. One subcommand name is wrong (`verify`); see M-F9.
- F9: fixed, PLAN:81, 87. `sweep-flagged` is a ninth state and its passage names no rollout stage.

## Findings

<!-- Source: V3 R3-F1 (base); fix per A-002, INV-001, A3 Round 2 -->
### M-F1 [BLOCKING] Task 7's grep also lists `.pyc` files, so its acceptance line fails after Task 7's own test run

Evidence:
- PLAN:125: "Until Task 10 adds an importer, `grep -rln "follow_ups" src/superclaude/cli/review` lists only `follow_ups.py`. From Task 10 on, the only other files it may list are `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`".
- PLAN:123 runs `uv run pytest tests/review/test_review_follow_ups.py -v` first. That import writes `__pycache__/follow_ups.cpython-311*.pyc`, which holds the module name.
- Live check, this merge: `grep -rln "ledger" src/superclaude/cli/review` lists 15 files, 10 of them `.pyc` in `__pycache__/`.
- `.gitignore:2` is "`__pycache__/`": these files exist after any test run but are not code.
- Qualification: it fails under default Python settings (bytecode on). `-B` or `PYTHONDONTWRITEBYTECODE=1` would pass, and the plan sets neither (A1 checked).
- `follow_ups.py` need not contain the word `follow_ups`, so even the fixed grep can print nothing, which "lists only" does not cover (INV-001).

Consequence: after Task 7's first acceptance command, the grep prints `follow_ups.py` plus at least one `.pyc`; from Task 10 on, also the importers' compiled copies. The executor halts, or ignores the extra lines and the check stops being a check.

Fix: rewrite both sentences of PLAN:125:
- "Until Task 10 adds an importer, `grep -rln --include='*.py' "follow_ups" src/superclaude/cli/review` lists no file other than `follow_ups.py`."
- "From Task 10 on, the same grep lists no file other than `follow_ups.py`, `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`."

Source: R3-F1, R1-F1, R2-F1; C-001, A-001, A-002, A-003; INV-001.

<!-- Source: Variant 3 R3-F2 (base) + Variant 1 R1-F2 separator; fix per A3 Round 2 -->
### M-F2 [NON-BLOCKING] The scale map's `labels` grammar has no family key, no conditional token and no multi-path separator

Evidence:
- PLAN:62: `labels` holds "`LABEL=Outcome` pairs separated by semicolons (outcomes: Blocking, Medium, Note)", and "the `defining file` cell holds the path".
- PLAN:146 (`ReviewerJudge`, "read through the scale map as 0 or 1") and PLAN:184 (the matrix) do not say which family row a label is looked up in.
- The same word maps differently by row: SPEC:742 tasklist "Medium: Blocking today"; SPEC:744 `card_convert.py` ("`important` and `medium` map to non-blocking"); SPEC:211 "an rf-qa IMPORTANT reads as blocking".
- Conditional rows: SPEC:739 MAJOR is "Blocking only when it names a concrete wrong outcome, else Medium"; SPEC:740 "B1, B2 and B3 together: Blocking; otherwise Note or Medium".
- Multi-path rows: PLAN:62 gives the code-assigned row two defining files and PLAN:64 names two `~/.claude/` paths; A3 found at least three rows needing two files.

Consequence: Tasks 3, 9, 12 and 15 must invent a lookup key, a single outcome for conditional rows, and a separator. The shadow numbers then rest on choices the spec never made.

Fix:
- Task 9: "the family is taken from the protocol name in the ledger row's `origin`/`source` cell and matched to the `family` column".
- Task 3: allow a conditional outcome token, and `ReviewerJudge` returns UNSET for a conditional pair. Do not write `MAJOR=Blocking` (that drops the SPEC:739 condition).
- Task 3: a row may name several files separated by " + "; Task 15's T4 checks that each file exists and that each label is present in at least one of them.

Source: R3-F2, R1-F2; C-002.

<!-- Source: Variant 3 R3-F3 (base) -->
### M-F3 [NON-BLOCKING] REQ-09 (cross-run matching) is owned by no task

Evidence:
- SPEC:396: "A new run on the same deliverable matches earlier `declined`, `filed` and `resolved` rows by the identity tuple without the run namespace".
- PLAN:120 names REQ-07, REQ-08 and REQ-10 and the identity tuple, not REQ-09.
- Grep for `REQ-09|across runs|cross-run` over all four `TASK-WF-blockerStage*` plans finds nothing (re-run in this merge).
- SPEC:1185 resolves spec INV-002 by "REQ-09 (cross-run identity)".

Consequence: no stage implements REQ-09, and earlier declined or filed rows are offered again.

Fix: add to Task 7 a lookup of earlier `declined`, `filed` and `resolved` rows by the identity tuple without the run namespace, with one test in `test_review_follow_ups.py`; or name stage 2's offer task as its owner.

Source: R3-F3, R1-F3; C-003.

<!-- Source: V2 R2-F2, R2-F3 (regraded); fix per A1/A3 Round 2 -->
### M-F4 [NON-BLOCKING] Task 10 lacks the M absence precheck and the D decision-basis input, yet pins "S, W and D always"

Grade note: this is a close call. A1 put the odds that a judge would call it BLOCKING near 45 percent. A2, the variant's own advocate, withdrew its BLOCKING grade because no failing stage 1 exit test, wrong gate outcome or missing deliverable could be shown.

Evidence:
- SPEC:512: M needs "code confirms the section or deliverable is not present by name first; the required-item list".
- SPEC:516: D needs "the decision-basis excerpts (section 4.3)". SPEC:522: Option Q replaces D at upstream gates and "Code then checks that the named consumer exists".
- SPEC:615 item 3: "Enable the classifier only for deliverable kinds where section 4.3 says the basis exists, and report how many table rows had a decision basis."
- PLAN:159: the supplier "returns three things" (required items, constraints, evidence) and `questions_to_ask` "returns S, W and D always". PLAN:164 pins "S, W and D are always present".
- Why not blocking: stage 1 has only `FixtureJudge` and `ReviewerJudge` (PLAN:146), the classifier has no authority (PLAN:21, OD4), and SPEC:945 names no exit test for this.

Consequence: the tests pass without the absence check; an implementation that withheld D without a basis would fail PLAN:164; the SPEC:615 basis count has no owner in stage 1 or 2.

Fix:
- `questions_to_ask` returns M only with the list plus a code-confirmed absence by name.
- It returns D only with decision-basis excerpts, else UNSET; replace the "D always present" assertion at PLAN:164.
- Add a basis count line to Task 12's input-count lines.

Source: R2-F2, R2-F3; C-007, C-008; A-004.

<!-- Source: Variant 1 R1-F4 -->
### M-F5 [NON-BLOCKING] The `classifier` column is written for rows the follow-ups ledger does not hold

Evidence:
- PLAN:184: "writes the verdict, band and judge id with version into the ledger row's `classifier` column".
- SPEC:348: the Items table holds "Medium findings and needs-your-decision rows". SPEC:364 defines the `classifier` column there.
- SPEC:592: shadow mode writes "into the ledger row and the finding record".
- Task 7 (PLAN:120) builds one reader and one writer and names no call that updates one column of an existing row.

Consequence: the plan does not say where the verdict of a finding graded Blocking is stored, or which call updates a row.

Fix: in Task 12, write the verdict to the finding record for every finding and to the Items row only when one exists; in Task 7, add an update call for one field with the expected-revision check.

Source: R1-F4; C-009.

<!-- Source: V3 R3-F5 (base); fix from V1 R1-F5 -->
### M-F6 [NON-BLOCKING] Task 8 names the resolver script but not how code calls or fakes it

Evidence:
- PLAN:132: "the target comes from the `origin_repo.py` script of `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py`", and only "the `gh` call" is injected.
- `origin_repo.py:7-9` is a command-line usage block ("Print ``owner/repo`` parsed from ``git remote get-url origin``"); it defines `parse_origin_url` (`origin_repo.py:86`) and `read_origin` (`origin_repo.py:156`).
- `tests/issue_watch/test_origin_parity.py:3`: "The script (``sc-issue-protocol/scripts/origin_repo.py``) is not a package".
- PLAN:137 needs `<R>` "from the resolver".

Consequence: the implementer must choose between a subprocess and a path load, and invent a fake for T8's wrong-repository case.

Fix: in Task 8, "the resolver is an injected function like `gh`; the default loads `origin_repo.py` by file path and calls `read_origin()`; tests pass a fake resolver".

Source: R3-F5 (fix replaced), R1-F5; C-004.

<!-- Source: Variant 3 R3-F4 (base) merged with invariant probe INV-004 -->
### M-F7 [NON-BLOCKING] Task 4's copy of spec section 6.6 breaks Task 5's folder grep, and Tasks 4 and 5 have no `src/superclaude` check

Evidence:
- PLAN:81: Task 4 copies "spec sections 6.1 to 6.7", including "the location rule (REQ-07)".
- SPEC:485: "`.dev/pr-monitor/` is gitignored".
- PLAN:97: "`grep -rn "\.dev/\|artifacts/" src/superclaude/skills/sc-review-severity` prints nothing".
- Tasks 1 to 3 check for `src/superclaude` (PLAN:42, 56, 74); Tasks 4 and 5 do not.
- The copied sections hold two such paths: SPEC:404 "`src/superclaude/cli/review/ledger.py`" and SPEC:447 "`src/superclaude/commands/issue.md`". PLAN:28 forbids them in installed primitives, and T3 (PLAN:223) checks only `digest` and `canonical` rows.

Consequence: a faithful Task 4 copy fails Task 5, and a copied `src/superclaude` path would ship unchecked.

Fix: in Task 4, "copy the pr-submit exception without the `.dev/pr-monitor/` path, and name no `src/superclaude/` path"; add `grep -rn "src/superclaude" src/superclaude/skills/sc-review-severity` prints nothing to Task 5.

Source: R3-F4, R1-F6; C-005; INV-003, INV-004.

<!-- Source: Variant 3 R3-F6 sub-item (base) -->
### M-F8 [NON-BLOCKING] Task 1 runs its entry gate after the work

Evidence:
- PLAN:20: the stage "runs only after ... the go is recorded in the stage ledger (Task 1 checks that)".
- PLAN:36 creates `SKILL.md`; PLAN:39-40 then check the owner go and `stage0-summary-for-owner.md`.

Consequence: a failed gate leaves an untracked file behind. No wrong result follows; SPEC:945 rollback is "delete the new files".

Fix: move the go and stage 0 summary checks into the first sentence of Task 1's body.

Source: R3-F6; C-010, X-001.

<!-- Source: Variant 3 R3-F6 (base), Variant 2 R2-F5, invariant probe INV-006 -->
### M-F9 [NON-BLOCKING] Wording and count defects

Evidence and fix:
- PLAN:184 lists `verify` among subcommands "present today". The name is `verify-citations` (`src/superclaude/cli/review/verify_cmd.py:76`: `@click.command(name="verify-citations")`). Fix: rename.
- PLAN:223 has a stray ", ;" after the T3 pointer text. Fix: delete it.
- PLAN:223 says `installed-only` rows "are checked for pointer order only" and "the test never reads `~/.claude`". Those files exist only under `~/.claude`, so the check does nothing. Fix: "installed-only rows are not checked by T3 (excluded from CI, SPEC:725)".
- PLAN:52 "prints nothing outside the one fenced digest's own text" cancels itself. Fix: "prints nothing".
- PLAN:71 says tasklist Medium is blocking "on 7 lines" (SPEC:742 lists seven). `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` has 9 matching lines: 1439, 1450, 1531, 1537, 1567, 1571, 1608, 1610, 1614 (for example 1537 "blocking (High and Medium) corrections"). Fix: write 9, or drop the count.

Consequence: cosmetic; none changes a gate outcome.

Source: R3-F6, R2-F5; C-006, C-012; INV-006.

<!-- Source: invariant probe INV-010, INV-013 -->
### M-F10 [NON-BLOCKING] Follow-up candidates: an open-ended importer list and an untested lint check

Evidence:
- INV-010: PLAN:125 closes the importer list at Task 10 to 13 with no later end point. The stage 2 plan adds `sweep.py` (stage 2 plan line 41, read "only through the stage 1 reader") and `follow_ups_cmd.py` (line 56).
- INV-013: `make lint` runs `lint-architecture` (Makefile:48), whose Check 11 (Makefile:467-470) scans `src/superclaude/cli/` for contract constant names; `src/superclaude/tools/arch_lint.py:11` lists `THRESHOLDS`. Task 9 says "Thresholds live only in the JSON file" (PLAN:146), which invites such a constant. `make lint` is an acceptance line only in Task 7 (PLAN:126).

Consequence: harmless inside stage 1. Stage 2 makes PLAN:125 false, and a `THRESHOLDS` constant would pass every acceptance line yet fail `make lint`.

Fix: give PLAN:125 the end point "until stage 2 adds an importer"; add `make lint` to the acceptance lines of Tasks 9, 10, 12 and 13, or tell Task 9 not to name a module constant `THRESHOLDS`.

Source: INV-010, INV-013.

<!-- Source: debate-transcript.md, round2-rebuttals.md (PC-12) -->
## Debate outcome

- Convergence 100 percent: 22 of 22 points, 21 unanimous and 1 (X-003) by majority. Invariant probe: 0 HIGH unaddressed; the 2 MEDIUM items (INV-001, INV-004) are in M-F1 and M-F7.
- Two regrades: C-007 and C-008 (R2-F2, R2-F3) moved from BLOCKING to NON-BLOCKING after A2 withdrew BLOCKING (no failing stage 1 exit test, wrong gate outcome, missing deliverable or data loss shown).
- Close call: C-008 (A1: about 45 percent BLOCKING odds), part of M-F4.
- C-001 stays BLOCKING (95 percent, all three advocates), qualified as "fails under default settings".
- Fix choices: load by path for the resolver (A3 conceded); the conditional token, not `MAJOR=Blocking` (A1 conceded).
- Dropped as not plan defects: C-011 (R2-F4, the review's own coverage matrix), X-003 (V1 header wording), X-004 (file inspection is not a command).
- Caveat: unanimity is weak evidence; the conceding advocate (A2) self-reported a different vendor.

<!-- Source: V3 (base), plus advocate and fault-finder checks -->
## Checked and found sound

- Tasks 1 to 16 are numbered without gaps, and every `Depends on:` names only lower tasks that match what each task reads.
- The 11 files holding "Grade every review finding as blocking or minor" are the 11 `digest` rows of Task 6; none contains `src/superclaude`. The 13 files with merge-rule phrases are covered by Task 3's allow-list plus the stage 3 carriers.
- The cap sentence at PLAN:49 equals `src/superclaude/output-styles/pragmatic.md:227` ("A review loop (review, fix, re-review) runs at most 2 fix cycles") and is the digest's last sentence (SPEC:207).
- The 6,400 count matches SPEC:551; the skill folder has the 6 files SPEC:877 names.
- `src/superclaude/cli/review/__init__.py:19-35` tolerates missing modules, so adding `"classify_cmd"` is safe; `tests/review/test_review_cli.py:47` checks only "panel", "merge", "ledger" and "telemetry".
- The wheel includes `src/**` (`pyproject.toml:81`), so the packaged refs are readable at runtime.
- Revision 2's shared decisions appear at PLAN:24-26 and 120; registry counts are 11, 1, 2 and 5 (PLAN:110). The SPEC:945 exit tests are all assigned.
- The stage 1 "Owner go" cell is blank (`stage-requests/README.md:18`), so Task 1 correctly halts until the owner says go.
- No other grep acceptance line is broken by bytecode (INV-002); among the copied sections only SPEC:485 clashes with Task 5 (INV-003); the plan's counts match the live files (INV-005).

<!-- Source: V3 (base), extended -->
## Not checked

- No test or `make` target was run. M-F1 rests on bytecode behaviour, the `.pyc` files on disk and the live greps, not on a run of Task 7.
- Whether later code in `doctor.py` would trip T2's fence scan.
- Low probe items not carried as findings: INV-007, INV-008, INV-009, INV-011.


<!-- REPORT.md BODY: the Write tool refused to create REPORT.md for a subagent, so the full report body is kept here for the team lead to write as REPORT.md. Everything below the next line, up to the end of this file, is the body. -->
<!-- BEGIN REPORT BODY -->
```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.83          # mean of the three blind reviewer calibrations (0.85, 0.82, 0.83); the T1 card alone calibrated 0.73
citations_total: 308
citations_revalidated: 308
citations_dropped: 9
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflect report (pre-execution), second review: plan TASK-WF-blockerStage1-20261116-030154

Run folder: `.dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116174309/`
Plan: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (4 phases, 16 tasks, 243 lines). Source: `source.md` in the same folder (38 lines, a byte copy of `stage-requests/stage1-request.md`, checked with cmp; it now carries the Revision 2 section). `PLAN:n` below means line n of the plan file; `SPEC:n` means line n of `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`.
First review: `.dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116030453/REPORT.md` (findings F1 to F9). This run is a fresh run in a new folder; the plan, source.md, return contract and everything under `.dev/tasks/` were read only.
Generated: 2026-11-16T18:30:47Z. Advisory: reflect never edits the plan.

## Verdict

**NEEDS-REVISION.** A three-reviewer ensemble (sonnet, haiku and opus classes), each card blind-calibrated by a separate opus-class calibrator and merged by an adversarial debate (22 of 22 points agreed; 21 unanimous, 1 by 2 of 3 majority), found 10 defects in the revised plan: 1 blocking and 9 non-blocking.

(a) The first-review findings: all nine are fixed in the live plan text. Two are fixed only in part: F1 (the Task 7 grep line now has its end point, but the grep itself still cannot be met, see M-F1) and F5 (the scale-map table shape is fixed, but its `labels` grammar still has no family key, conditional token or multi-path separator, see M-F2). (b) The revision introduced no broken task numbering or dependency, no acceptance line that a later task of this package makes false without an end point, and no contradiction with the brief's shared decisions 1, 2, 4 and 5; it left one blocking defect: the rewritten Task 7 line `grep -rln "follow_ups" src/superclaude/cli/review` lists only `follow_ups.py` (PLAN:125) also matches compiled `.pyc` files, so it fails right after Task 7's own test run. (c) Against the spec, the stage 1 exit tests T1 to T4, T6 to T8, T11 to T13 and T17 (SPEC:945) are all assigned to a task; the gaps found are non-blocking (M-F2 to M-F10).

The one blocking finding is a one-line repair. The other nine can ship as plan notes or be fixed in the same pass.

## Tier decision

Tier 2, rule 4 fired (the plan touches code, tests, skill docs and registry and JSON config, so domains are 4); rules 5 (`S_dev_density` 0.3529 above 0.20) and 6 (`C` 0.73 below 0.85) also match. The Step 1B.2b guard fired too: parsed requirements 0, inferred 68, so a Tier-1 stop was forbidden in any case. Blind calibration of the T1 card gave C = 0.73. Reviewer classes: sonnet (analyzer, calibrated 0.85), haiku (qa, 0.82) and opus (refactorer, 0.83). Calibrator class: opus; all three Anthropic classes were reviewers, so the disjoint set was empty and `calibrator_diversity: degraded`. Executor class: unknown (pre-execution run, no `--executor-model`, no environment variable, no task log), so no class was excluded and the anti-self-confirmation guarantee is weaker than designed. Single vendor, three model classes: `t2_model_class_diversity: full`, `t2_vendor_diversity: single`. Reviewer 2 (haiku pin) again self-reported an OpenAI model (`identity_mismatch_suspected`). Engine `legacy`; no panel code ran.

## Inferred requirements (Pass 2)

68 inferred rows from the requirements-analyst agent (`artifacts/pass2-requirements-analyst.yaml`; the full matrix is `artifacts/coverage-matrix.yaml`). Every quote is a verbatim substring of its cited `source.md` line (checked by script, then by the evidence validator). The mechanical containment rule matched 44 of 68 (`coverage_pct_union` 0.6471); it is noisy on prose, so the last column also gives the manual mapping. A manual read maps all 68 rows to a task or to the Constraints block; the rows INF-011 and INF-012 restate older request lines that Revision 2 supersedes (source.md:26, 30, 35-37) and are covered by their replacements; INF-013 stays live and maps to Task 2. INF-026 (the "until Task N" end-point rule) is honoured once, at PLAN:125, and that line has its own defect (M-F1).

| INF id | Verbatim quote (prefix, 150 characters at most) | Citation | Match result |
|---|---|---|---|
| INF-001 | Generate it only after the owner has read the stage 0 package's `./artifacts/stage0-summary-for-owner.md` and said go in chat, and after the stage led | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:3 | mechanical: containment (task 1, 0.778); manual: Task 1 (PLAN:34) |
| INF-002 | This stage creates new files only (the skill folder, new CLI modules, new tests, one doctor check); it edits no review-loop carrier. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:3 | mechanical: none (task 7, 0.556); manual: Constraints PLAN:20 |
| INF-003 | Reuse Tasks 11 to 25 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:7 | mechanical: none (task 16, 0.25); manual: provenance of the base text; Tasks 1 to 15 plus the exit task 16 (PLAN:34-243) |
| INF-004 | Read its `## Constraints` and carry over what applies to stage 1: spec and PF naming, owner-decision defaults, the not-built list | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:7 | mechanical: none (task 1, 0.286); manual: Constraints PLAN:18-30 |
| INF-005 | the classifier facts (M, C and E run only with code-supplied inputs; the "M or C is Y gives BLOCKING" row is never enabled; confidence is an ordinal b | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:7 | mechanical: none (task 9, 0.571); manual: Constraints PLAN:23; Tasks 9 and 10 (PLAN:146, 159) |
| INF-006 | `src/superclaude/` as source of truth with `make sync-dev`, UV only. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:7 | mechanical: none (task 1, 0.429); manual: Constraints PLAN:28-29 |
| INF-007 | State this package is stage 1: new files only, no carrier edited, every registry `digest` row stays `legacy`. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:11 | mechanical: containment (task 6, 0.714); manual (corrected after validation): Constraints PLAN:20; Task 6 (PLAN:102) |
| INF-008 | The next package (stage 2) starts only after the owner's go in chat. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:11 | mechanical: none (task 1, 0.556); manual: Constraints PLAN:20 |
| INF-009 | Drop the base plan's Phase 3 to 5 gate prose. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:11 | mechanical: none (task 6, 0.167); manual: no gate prose after Phase 4; 4 phases (PLAN:32-243) |
| INF-010 | The "Merge-rule allow-list" section lists files by path and never writes the three merge-rule phrases or the old definition sentence. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:12 | mechanical: containment (task 3, 0.929); manual: Task 3 (PLAN:58) |
| INF-011 | At stage 1 it lists the auggie file, `refs/rule.md` and the six stage 4 files. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:12 | mechanical: containment (task 3, 0.875); manual: Task 3 (PLAN:58) |
| INF-012 | Say in the task that the plugin mirror is added in stage 4, not here. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:12 | mechanical: none (task 3, 0.571); manual: superseded by Revision 2 (source.md:26, 37); PLAN:26, 66 say no plugin surface |
| INF-013 | `refs/rule.md` holds the GR5 sentence with the phrase `highest severity` (allow-listed) | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:13 | mechanical: containment (task 2, 0.875); manual: Task 2 (PLAN:45) |
| INF-014 | never quotes the old definition sentence "Grade every review finding as blocking or minor" outside the digest's own fence history | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:13 | mechanical: containment (task 2, 0.812); manual: Task 2 (PLAN:45) |
| INF-015 | state this as an acceptance line (`grep` of the old sentence over the skill folder prints nothing) | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:13 | mechanical: containment (task 5, 0.818); manual (corrected after validation): Task 2 (PLAN:45; acceptance PLAN:52) |
| INF-016 | No file under `src/superclaude/skills/sc-review-severity/` cites a `.dev/` or `./artifacts/` path | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:14 | mechanical: containment (task 3, 0.714); manual (corrected after validation): Task 5 (PLAN:90; acceptance PLAN:97) |
| INF-017 | (acceptance: `grep -rn "\.dev/\&#124;artifacts/" src/superclaude/skills/sc-review-severity` prints nothing) | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:14 | mechanical: containment (task 5, 1.0); manual: Task 5 (PLAN:90) |
| INF-018 | State the M, C and E input rule in words. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:14 | mechanical: none (task 4, 0.5); manual: Task 5 (PLAN:94) |
| INF-019 | Keep exactly 11 `digest` rows, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:15 | mechanical: containment (task 6, 0.9); manual: Task 6 (PLAN:102) |
| INF-020 | Say the analysis template is not a carrier row (merge-rule text only in stage 4). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:15 | mechanical: containment (task 6, 0.667); manual: Task 6 (PLAN:102) |
| INF-021 | T3's `src/superclaude` check applies to `digest` and `canonical` rows only | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:16 | mechanical: containment (task 15, 1.0); manual: Task 15 (PLAN:219) |
| INF-022 | `pointer-only` and `installed-only` rows are checked for pointer order only, and a `pointer-only` row only once its pointer is present | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:16 | mechanical: containment (task 15, 1.0); manual: Task 15 (PLAN:219) |
| INF-023 | the test never reads `~/.claude` | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:16 | mechanical: containment (task 15, 1.0); manual: Task 15 (PLAN:219) |
| INF-024 | T2 is non-strict (strict only in stage 4). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:16 | mechanical: containment (task 15, 0.6); manual: Task 15 (PLAN:219) |
| INF-025 | Acceptance includes a temporary-tree test of each exemption. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:16 | mechanical: containment (task 15, 0.667); manual: Task 15 (PLAN:219) |
| INF-026 | Acceptance lines inside this package** that a later task of the same package makes false get an end point ("until Task N"). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:17 | mechanical: none (task 4, 0.467); manual: Constraints PLAN:27; applied at PLAN:125 (see M-F1) |
| INF-027 | New final task: stage 1 exit summary for the owner. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:18 | mechanical: none (task 16, 0.571); manual: Task 16 (PLAN:233-243) |
| INF-028 | Write `./artifacts/stage1-summary-for-owner.md`: for each task its artifact or file and its observed test result (the commands run and their pass coun | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:18 | mechanical: containment (task 16, 0.643); manual: Task 16 (PLAN:233) |
| INF-029 | the list of files created | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:18 | mechanical: containment (task 16, 1.0); manual: Task 16 (PLAN:233) |
| INF-030 | a statement that no carrier was edited (`git diff --stat` over carriers is empty) | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:18 | mechanical: containment (task 16, 0.667); manual: Task 16 (PLAN:233) |
| INF-031 | the open items, and the sentence that the owner's go for stage 2 is given in chat and not by this file. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:18 | mechanical: containment (task 16, 1.0); manual: Task 16 (PLAN:233) |
| INF-032 | No edit of any carrier (`pragmatic.md`, agents, templates, rule prompts, task skill, tech-research, WORKER-CONTRACT) and no stage 2 to 4 task. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:22 | mechanical: none (task 6, 0.357); manual: Constraints PLAN:20, 22 |
| INF-033 | Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent target. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:22 | mechanical: none (task 2, 0.3); manual: Constraints PLAN:22 |
| INF-034 | No Jev call, key or account. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:22 | mechanical: none (task 8, 0.25); manual: Constraints PLAN:22 |
| INF-035 | Applied to the plan in place (plan file name, slug and frontmatter unchanged; still 16 tasks, 4 phases). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:26 | mechanical: none (task 1, 0.231); manual: 16 tasks and 4 phases (PLAN:32-243) |
| INF-036 | This section supersedes the older lines above where they differ | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:26 | mechanical: none (task 3, 0.571); manual: meta statement; Revision 2 text applied throughout |
| INF-037 | until Task 10 adds an importer, `grep -rln "follow_ups" src/superclaude/cli/review` lists only `follow_ups.py` | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:28 | mechanical: containment (task 7, 1.0); manual: Task 7 (PLAN:116) |
| INF-038 | from Task 10 on the only other files it may list are `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py` | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:28 | mechanical: containment (task 7, 1.0); manual: Task 7 (PLAN:116) |
| INF-039 | no task wires a command for `follow_ups` | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:28 | mechanical: none (task 7, 0.5); manual: Task 7 (PLAN:116-126) wires no command |
| INF-040 | the stoprule and `finding-grader` row is marked `installed-only`, names `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md` and `~/.clau | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:29 | mechanical: containment (task 3, 1.0); manual: Task 3 (PLAN:58) |
| INF-041 | cites no `.dev/` path, and is exempt from the exists-in-repository line | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:29 | mechanical: containment (task 3, 1.0); manual: Task 3 (PLAN:58) |
| INF-042 | Task 15's T4 carries the same exemption (OD10 stays undecided). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:29 | mechanical: none (task 3, 0.556); manual: Task 15 (PLAN:223, 231) |
| INF-043 | Task 3's allow-list section also lists `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py` as `allowed` (they hold the phrases and | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:30 | mechanical: containment (task 3, 0.917); manual: Task 3 (PLAN:58) |
| INF-044 | Task 7 records: `follow-ups.md` stays a separate file, no mapping to `review-ledger/1` rows, `ledger.py` untouched, the audit verdict decides whether  | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:31 | mechanical: containment (task 7, 0.889); manual: Task 7 (PLAN:116) |
| INF-045 | the "ledger adapters" are `follow_ups.py`, `classifier_inputs.py` and the classifier column writing of `classify_cmd.py`. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:31 | mechanical: containment (task 7, 0.875); manual: Task 7 (PLAN:116) |
| INF-046 | Task 16 reports the audit verdict to the owner. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:31 | mechanical: containment (task 7, 0.833); manual (corrected after validation): Task 16 (PLAN:233, 237) |
| INF-047 | `ledger.py` is added to the not-built list. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:31 | mechanical: none (task 7, 0.5); manual: Constraints PLAN:22 |
| INF-048 | Task 3 fixes the table columns (`family`, `defining file`, `labels`, `model`, `file kind`), the `LABEL=Outcome;` pair format, the path root (relative  | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:32 | mechanical: containment (task 3, 0.8); manual: Task 3 (PLAN:58) |
| INF-049 | the `none` value for a row without a native label (skipped by T4's label check) and `installed-only` rows. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:32 | mechanical: containment (task 15, 0.833); manual: Task 15 (PLAN:219) |
| INF-050 | Tasks 9, 12 and 15 gain `Depends on: Task 3`. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:32 | mechanical: containment (task 3, 0.714); manual (corrected after validation): Tasks 9, 12 and 15 (PLAN:144, 182, 221) |
| INF-051 | Task 10 depends on Task 7 and Task 9. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:33 | mechanical: containment (task 7, 0.833); manual (corrected after validation): Task 10 (PLAN:155; Depends on PLAN:157) |
| INF-052 | `run_questions(judge, finding, allowed)` is assigned to Task 9 and `questions_to_ask(inputs)` to Task 10, so Task 11's M, C and E test uses only funct | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:33 | mechanical: containment (task 11, 0.778); manual: Task 11 (PLAN:167) |
| INF-053 | The second half of T12 ("except through the safety route") moves to Task 13, which now depends on Task 9 as well. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:33 | mechanical: containment (task 11, 0.786); manual (corrected after validation): Task 13 (PLAN:192, 196); Task 11 (PLAN:167, 171) |
| INF-054 | Task 2's grep uses the full path | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:34 | mechanical: containment (task 2, 0.6); manual: Task 2 (PLAN:45) |
| INF-055 | Task 12 names the seven review subcommands present today and says `lint` and `estimate` are optional names without modules | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:34 | mechanical: containment (task 12, 0.733); manual: Task 12 (PLAN:180) |
| INF-056 | Task 4 defines `sweep-flagged` as a ninth state (the spec has eight; it comes from the stage 2 package's sweep) and the installed reference names no r | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:34 | mechanical: containment (task 4, 0.938); manual: Task 4 (PLAN:77) |
| INF-057 | Task 3 lists `skills/task/SKILL.md`, `skills/task-builder/` and `agents/rf-task-builder.md` as `exempt-by-retirement` (path only) | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:35 | mechanical: containment (task 3, 1.0); manual: Task 3 (PLAN:58) |
| INF-058 | with the sentence that the exemption ends when the retirement removes the file | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:35 | mechanical: containment (task 3, 1.0); manual: Task 3 (PLAN:58) |
| INF-059 | Task 16's carrier diff adds the task-builder folder. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:35 | mechanical: none (task 7, 0.429); manual: Task 16 (PLAN:237) |
| INF-060 | `/sc:implement`'s final review step records and prints only, the offer stays with the top-level session and the consent-bound filing path (OD15) | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:36 | mechanical: containment (task 4, 0.938); manual: Task 4 (PLAN:77) |
| INF-061 | `tech-research` writes the ledger and neither sweeps nor offers | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:36 | mechanical: containment (task 4, 1.0); manual: Task 4 (PLAN:77) |
| INF-062 | `sc-implement-protocol` joins the not-edited list and the Task 16 diff. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:36 | mechanical: none (task 7, 0.429); manual: Constraints PLAN:20, 25; Task 16 (PLAN:237) |
| INF-063 | Task 3 no longer says a plugin mirror comes in stage 4 | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:37 | mechanical: none (task 3, 0.571); manual: Task 3 (PLAN:66) |
| INF-064 | Task 6's canonical row has no plugin surface (the word `plugin` stays only on the two pointer-only rows whose hand-kept twins exist) | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:37 | mechanical: containment (task 6, 0.867); manual: Task 6 (PLAN:102) |
| INF-065 | Task 15's T2 note says why `plugins/` is still scanned | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:37 | mechanical: none (task 15, 0.444); manual: Task 15 (PLAN:223) |
| INF-066 | Task 16 diff adds `plugins`. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:37 | mechanical: containment (task 7, 0.6); manual (corrected after validation): Task 16 (PLAN:233, 237) |
| INF-067 | Registry counts unchanged: 11 `digest`, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:37 | mechanical: containment (task 6, 0.8); manual: Task 6 (PLAN:102) |
| INF-068 | which broke the one-label-per-task rule | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:38 | mechanical: none (task 1, 0.333); manual: one `Acceptance criteria:` label per task, 16 in all (checked) |

No inferred quote was dropped (all 68 are verbatim); six manual mappings that the validator found unfounded and two it found weak were corrected in the table above (marked "corrected after validation") and are counted in the dropped and shifted totals below.

## Findings

Full text with all citations: `adversarial/merged-review-card.md`. Severity follows the rule in the reviewer briefs: blocking means an executor following the plan as written cannot meet a stated requirement or acceptance check, would produce a wrong or missing result, or data loss; minor means wording, format or a real but non-blocking weakness.

| # | Blocking | Finding |
|---|---|---|
| M-F1 | yes | Task 7's grep line (PLAN:125) lists compiled `.pyc` files as well as `follow_ups.py`, so "lists only `follow_ups.py`" fails after Task 7's own pytest run (PLAN:123) and the importer list fails again from Task 10 on; fix with `--include='*.py'` and "lists no file other than" in both sentences. |
| M-F2 | no | The scale map's `labels` grammar (PLAN:62) has no family key, no conditional token and no multi-path separator, yet Task 9 (PLAN:146), Task 12 (PLAN:184) and Task 15's T4 (PLAN:223) read it. |
| M-F3 | no | REQ-09 (cross-run matching, SPEC:396) is owned by no task of any stage plan. |
| M-F4 | no | Task 10 lacks the M absence-by-name precheck (SPEC:512) and the D decision-basis input (SPEC:516, 522), yet PLAN:164 pins "S, W and D always"; a close call (about 45 percent odds of BLOCKING by one advocate). |
| M-F5 | no | Task 12 writes the `classifier` value into ledger rows, but the follow-ups ledger holds only Medium and needs-decision rows; Task 7 has no one-field update call. |
| M-F6 | no | Task 8 names `origin_repo.py` (a script, not a package) without saying how code calls it or how tests fake it; load by path is the better fix. |
| M-F7 | no | Task 4's copy of SPEC:485 (`.dev/pr-monitor/`) breaks Task 5's folder grep (PLAN:97), and Tasks 4 and 5 have no `src/superclaude` check although the copied sections hold two such paths (SPEC:404, 447). |
| M-F8 | no | Task 1 creates `SKILL.md` (PLAN:36) before its entry-gate checks (PLAN:39-40) run. |
| M-F9 | no | Wording and count nits: `verify` should be `verify-citations` (PLAN:184); stray ", ;" and a no-op check at PLAN:223; self-cancelling phrase at PLAN:52; tasklist Medium count 9, not 7 (PLAN:71). |
| M-F10 | no | Follow-up candidates: PLAN:125's importer list has no end point after stage 1; a `THRESHOLDS` constant would pass every acceptance line yet fail `make lint` check 11. |

### Validator corrections (apply when reading the card)

Two evidence validators re-read all 308 citations (112 in the merged card, 196 in this report body: 68 inferred quotes, 68 manual mappings and 60 other lines): 297 founded, 2 shifted, 9 unfounded. The nine unfounded items were dropped and replaced by the corrected text, so `citations_dropped` is 9 and the status is forced to `partial` by the protocol (this is not a defect in the plan findings: no grade or fix changed). The zero-drop flag is false.

- Corrected in the merged card: the SPEC:744 quote (now the exact words "`important` and `medium` map to non-blocking"; unfounded), the stage 2 plan line for `follow_ups_cmd.py` (63 to 56; unfounded), `__init__.py:19-29` (to 19-35; shifted).
- Corrected in this report: six manual mappings in the inferred table (INF-015 to Task 2, INF-016 to Task 5, INF-046 and INF-066 to Task 16, INF-050 to Tasks 9, 12 and 15, INF-051 to Task 10; all unfounded because the mechanical containment match was copied into the manual column without a separate read) and two weak ones (INF-007, INF-053); the supersession sentence (INF-013 is not superseded; unfounded); R-002's task label (PLAN:177 is in Task 11; shifted). All 68 quotes were verbatim.
- Not verifiable by the validators and checked by the orchestrator: the byte-level `.pyc` listing (validator A had no shell; orchestrator batch c01 listed 5 `.py` and 10 `.pyc` files for "ledger", 15 in all), the `cmp` of the source copy (identical), and the debate figures (no file:line citations).

### Reviewer disagreement, as settled by the debate

- M-F1 (C-001): all three reviewers graded it blocking; reviewers 1 and 3 showed the on-disk pycache evidence; two advocates re-ran the grep live; the debate qualified the claim to "fails under default Python settings" (`-B` or `PYTHONDONTWRITEBYTECODE=1` would pass) and the fault-finder added that the fixed grep can print nothing, so the wording must be "lists no file other than".
- M-F4 (C-007, C-008): the one real split. Reviewer 2 graded both BLOCKING; reviewers 1 and 3 graded them non-blocking. After Round 2 its own advocate withdrew BLOCKING (no failing stage 1 exit test, gate outcome, missing deliverable or data loss could be shown; stage 1 builds only `FixtureJudge` and `ReviewerJudge`, PLAN:146). Recorded as a close call.
- M-F2, M-F3, M-F5 to M-F9: non-blocking in every card that raised them; fix choices settled in the debate (conditional token, not `MAJOR=Blocking`; load by path, not a subprocess).
- Dropped by the debate as not plan defects: the reviewer-2 point on this review's own coverage matrix (C-011), the reviewer-1 header wording (X-003) and reviewer 2's "no commands run" inconsistency (X-004).
- Invariant probe (Round 2.5): 13 items, 0 HIGH unaddressed, 2 MEDIUM (INV-001 fix wording, in M-F1; INV-004 missing `src/superclaude` check, in M-F7), 7 LOW; INV-006, INV-010 and INV-013 are carried as M-F9 and M-F10.

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: 0 / 308 = 0.00

## Recommendations

### Recommendation R-001: Make Task 7's grep line meetable

- **File:** `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (Task 7 acceptance line, PLAN:125)
- **Change:** Rewrite both sentences with `grep -rln --include='*.py' "follow_ups" src/superclaude/cli/review` and the words "lists no file other than `follow_ups.py`" (and, from Task 10 on, "`follow_ups.py`, `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`").
- **Verifier:** after Task 7's pytest run, the command prints nothing but at most `follow_ups.py`; a grep of the plan finds `--include='*.py'` in both sentences.
- **Linked deviation(s):** M-F1
- **Priority:** P0

### Recommendation R-002: Give Task 10 the inputs M and D need, or defer them in words

- **File:** the same plan, Task 10 (PLAN:159, 164), Task 11 (PLAN:177) and Task 12 (PLAN:184, 190)
- **Change:** `questions_to_ask` returns M only with the required-item list plus a code-confirmed absence by name, and D only with decision-basis excerpts (else UNSET); replace the "D always present" assertion; add a decision-basis count line to Task 12; or state that both inputs wait for the task that builds a text-reading judge.
- **Verifier:** Task 10's acceptance lines test M without a confirmed absence and D without a basis with a recording judge; Task 12's count lines include the basis count.
- **Linked deviation(s):** M-F4
- **Priority:** P1

### Recommendation R-003: Fix the scale-map grammar

- **File:** the same plan, Task 3 (PLAN:62), Task 9 (PLAN:146), Task 15 (PLAN:223)
- **Change:** Task 9 names the lookup key (family from the ledger row's `origin` or `source`); Task 3 allows a conditional outcome token that `ReviewerJudge` returns as UNSET, and a " + " separator for rows with several defining files; T4 checks each file exists and each label is in at least one.
- **Verifier:** Task 3 shows the three grammar rules; T4's temporary-tree tests include a two-file row and a conditional label.
- **Linked deviation(s):** M-F2
- **Priority:** P1

### Recommendation R-004: Assign REQ-09

- **File:** the same plan, Task 7 (PLAN:120), or the stage 2 plan's offer task
- **Change:** add the cross-run lookup of earlier `declined`, `filed` and `resolved` rows with one test, or name the stage 2 task that owns it.
- **Verifier:** `grep -n "REQ-09"` finds an owner in the plan set.
- **Linked deviation(s):** M-F3
- **Priority:** P1

### Recommendation R-005: Settle where the classifier verdict is stored

- **File:** the same plan, Task 7 (PLAN:120) and Task 12 (PLAN:184)
- **Change:** Task 12 writes the verdict to the finding record for every finding and to the Items row only when one exists; Task 7 adds a one-field update call with the expected-revision check.
- **Verifier:** Task 12's tests cover a Blocking finding with no Items row.
- **Linked deviation(s):** M-F5
- **Priority:** P2

### Recommendation R-006: Say how Task 8 calls and fakes the resolver

- **File:** the same plan, Task 8 (PLAN:132, 137)
- **Change:** the resolver is an injected function like `gh`; the default loads `origin_repo.py` by file path and calls `read_origin()`; tests pass a fake.
- **Verifier:** Task 8's T8 wrong-repository test uses the fake resolver.
- **Linked deviation(s):** M-F6
- **Priority:** P2

### Recommendation R-007: Keep paths out of the new reference files, with a check

- **File:** the same plan, Task 4 (PLAN:81) and Task 5 (PLAN:97)
- **Change:** Task 4 copies the pr-submit exception without the `.dev/pr-monitor/` path and names no `src/superclaude/` path; Task 5 adds `grep -rn "src/superclaude" src/superclaude/skills/sc-review-severity` prints nothing.
- **Verifier:** both lines appear in the plan; the grep prints nothing on the finished folder.
- **Linked deviation(s):** M-F7
- **Priority:** P2

### Recommendation R-008: Tidy the order, wording and follow-up candidates

- **File:** the same plan, PLAN:36-40, PLAN:52, PLAN:71, PLAN:125, PLAN:184, PLAN:223
- **Change:** move Task 1's go and stage-0-summary checks into the first sentence of its body; rename `verify` to `verify-citations`; delete the stray ", ;"; say installed-only rows are "not checked by T3"; reword PLAN:52 to "prints nothing"; write 9 for the tasklist line count or drop it; give PLAN:125 the end point "until stage 2 adds an importer"; add `make lint` to the acceptance lines of Tasks 9, 10, 12 and 13 or tell Task 9 not to name a module constant `THRESHOLDS`.
- **Verifier:** a re-read of PLAN:36-40, 52, 71, 125, 184 and 223 shows each change.
- **Linked deviation(s):** M-F8, M-F9, M-F10
- **Priority:** P2

## Run notes

- Panel: reviewer 1 analyzer/sonnet, reviewer 2 qa/haiku, reviewer 3 refactorer/opus, all spawned as the read-only `reflect-reviewer` agent type with a model override; blind calibrators opus class; advocates sonnet, haiku and opus (general-purpose agents); scorers sonnet class (`judge_class_collision: true`: the judge class overlaps variant 1); fault-finder and merge-executor opus class; requirements-analyst for Pass 2.
- Deviations from the protocol: the live `sc-adversarial-protocol` probe was folded into the real Skill call (it loaded, so the F1/F2/F3 fallback did not fire); the T1 card was written inline by the orchestrator, not by `root-cause-analyst`; the diff analysis and refactor plan were drafted by the orchestrator (no separate analytical-agent review of the plan); advocate statements are persisted in condensed form under `adversarial/adversarial/debate/` (arguments, evidence, every per-point row and A-NNN answer kept); Wave 1A used targeted reads and two batch scripts of read-only checks plus one `codegraph_node` and one augment search, no degraded token.
- Reviewer-isolation snapshot (`--isolate-reviewers`) was not used: reviewers read the live tree; other reflect runs and plan revisions (stages 2 to 4) were active in the same worktree, but the input tree hash is unchanged (17 files, no drift).
- The orchestrator wrote the reviewer cards, calibration blocks and debate files from agent hand-backs; the merge-executor wrote the merged card and merge log itself. REPORT.md itself was refused by the Write tool for a subagent and is left for the team lead; this body is the text to write.
- Memory: not written. The team lead restricted output to this run folder, so no last-pass note, no deviation-patterns update and no `.dev/reflect/runs.jsonl` append were made. Memory hydrate at Wave 0 found the first review's last-pass note (it flagged the same pattern: acceptance lines that a later task makes false, and installed-only primitives).
<!-- END REPORT BODY -->
