# Diff Analysis: Reviewer Card Comparison

## Metadata
- Generated: 2026-11-08T18:41:08Z
- Variants compared: 2
  - Variant A = `variant-1-original.md` (reviewer-1, analyzer persona, sonnet; findings F1-F10)
  - Variant B = `variant-2-original.md` (reviewer-2, qa persona, haiku; findings QA-001-QA-005)
- Audited plan: `.dev/tasks/to-do/TASK-WF-spec-20261108-181640/TASK-WF-spec-20261108-181640.md` ("plan:N") against `source.md` in the same folder ("source.md:N")
- Focus areas: correctness, coverage, deviation-classification
- Total differences found: 32 (S + C + X + U); shared assumptions recorded separately: 9
- Categories: structural (5), content (9), contradictions (1), unique (17), shared assumptions (9; 2 promoted as [SHARED-ASSUMPTION], 1 CONTRADICTED)
- Debate taxonomy tags: L1 surface (wording/format), L2 structural (organization/design), L3 state-mechanics (state/guard/boundary/invariant/validation rule). Priority L3 > L2 > L1.
- Grounding spot-checks made for this analysis: plan:42, 49, 52, 71, 76, 89, 103, 110, 172-174 read; source.md:24-40, 81, 86-96, 105-110, 199-229 read; `tests/skills/test_review_severity_rule.py:36-56` read (`_tracked_text` builds its file set from `git ls-files`).

## Structural Differences

| # | Area | Variant A | Variant B | Severity | Level |
|---|------|-----------|-----------|----------|-------|
| S-001 | Finding record schema | Fields `id`, `class`, `severity`, `title`, `citation` (list mixing plan, spec and repo lines), optional `detail`, `fix`. Citations in short form (`plan:89`). | Fields `id`, `class`, optional `subtype`, `severity`, `citation` (one full repo-relative path:line), `finding`, `evidence` (list), `fix`. No title. | Low | L1 |
| S-002 | Supporting sections outside findings | `correctness_gaps_advisory` (one advisory) and `confirmed_ok` (7 positively verified anchors: spec-panel.md section lines, routing test lines, worker-contract counting, loader pattern, brief phrase counts). | `grounding_root` and `notes` (scope read: all 12 tasks, full spec, all 35 coverage rows; owner rulings respected; no tests run; external S1 briefs not inspected). No positive-verification list. | Medium | L2 |
| S-003 | Finding count and severity distribution | 10 findings: 3 MEDIUM, 7 LOW; no HIGH. | 5 findings: 1 HIGH, 4 MEDIUM; no LOW. | Medium | L2 |
| S-004 | Audit target boundary | Every finding targets the plan (or the plan's interaction with repo tests, F1). | QA-003 targets the coverage-matrix artifact (`reflect-1/artifacts/coverage-matrix.json:230-239`), not the plan; its calibrator says "Flaw in the coverage artifact, not the plan." | Medium | L2 |
| S-005 | Calibration block extras | Calibrator adds `notes` reclassifying findings ("F1/F7 are not Regressions ... F10 is an omitted step"); 4 of 10 per-finding checks `partial`. | Calibrator adds `unraised_gaps` (one new gap: exclusive-create lock untested); 5 of 5 per-finding checks `true`. | Low | L1 |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity | Level |
|---|-------|-------------------|-------------------|----------|-------|
| C-001 | Task 7 fidelity checks for the variant command (overlapping area, plan:103 and plan:110) | F4: the drift guard ("every other `## ` section equals the parent's") does not exempt the edited `## Usage` section and does not name Review Loop and Diffgate as exceptions, so it would fail or need ad hoc exemptions. | QA-005: plan:103 promises both bullet sets are checked character for character by Task 7, but Task 7 (plan:110) pins only the seven Review Loop bullets; the six Diffgate bullets are checked for placement and lookup order only. | Medium | L3 |
| C-002 | Experiment-kit handling of loop terminal states (overlapping area, plan:172-174) | F5: `T10-R3-reviser.txt` ships a brief the design says never runs (review-3 FAIL halts; no third fix); fix is to keep it only under `source/` and exclude T10 in README. Calibrator: partial, plan already flags T10 as a coordinator decision. | QA-004: the scoring note always reads `proxy_all` from `<DIR>/result-r3.json`; an early PASS at review 1 or 2 closes the loop so that file never exists; add a branch reading the last `result-r<N>.json`. | Medium | L3 |
| C-003 | Verbatim-copy obligations from source.md | F2: Task 5 demands the subcommand table verbatim yet alters its `check` row (adds `proxy_all`), and the AC asserts an exact substring. F3: the source of the expected verbatim blocks for Task 5's test is unspecified (source.md moves on archive). | QA-002: the required disclosure sentence for `deferred.md` (source.md:40, "PASS in this loop is scoped to the reviewed surfaces; ...") is assigned to no task or AC. Confirmed absent from the plan. | Medium | L3 |
| C-004 | Severity calls and what counts as the top risk | Highest concerns are test-harness integrity (F1 vacuous pass, F2/F3 verbatim test design), all MEDIUM. Does not examine the review-1 deferral rule. | Highest concern is runtime correctness of the gate: QA-001 HIGH, Task 2 defers every finding without a hunk or prior id at every review, so review 1 (no surface, no priors) can turn all blockers into `deferred: pre-existing` and produce a false PASS. Grounded: source.md places this rule in the review-2 row (source.md:29) and the re-review bullet (source.md:81); plan:49 states it unconditionally. | High | L3 |
| C-005 | Deviation classification | Uses three classes: Regression (F1, F2, F7), Drift (F3-F6, F8, F10), Authorized expansion (F9). Own calibrator rejects Regression for F1 and F7 and calls F10 an omitted step. | Uses Drift only (QA-001-QA-005), one with `subtype: coverage gap`. QA-001 (a rule that yields a false PASS) is arguably closer to Regression than Drift; QA-003 is not a plan deviation at all. | Medium | L2 |
| C-006 | Treatment of plan-added content and owner rulings | F9 classifies the plan's pre-run gate and plan-authored T11 blindness-audit text as Authorized expansion and asks that the gate be listed in Constraints and T11 marked a coordinator-reviewable draft. | Notes state "Respected the owner rulings" and raises no finding on plan-added content; does not assess T11 text. | Low | L2 |
| C-007 | Verdict and confidence | `verdict: refactor`; self 0.78, calibrated 0.81 (under-confident by 0.03). | `verdict: refactor`; self 0.94, calibrated 0.85 (over-confident by 0.09). | Low | L1 |
| C-008 | Coverage breadth across plan tasks | Touches Tasks 1, 4, 5, 6, 7, 10, 11, 12 plus repo tests; no finding on Task 2 or Task 3 rules or on Task 4 outputs (`deferred.md`). | Touches Tasks 2, 4, 6/7, 12 plus the coverage matrix; no finding on Tasks 1, 3, 5, 8, 9, 10, 11 or on test-harness mechanics. The two cards cover largely disjoint task sets. | Medium | L2 |
| C-009 | Evidence strength per finding | 6 of 10 findings fully verified; F5, F6, F8, F9 partial (F9's "unverified base commit" overstated, since source.md:199 names `2cb683f5`). | 5 of 5 verified; QA-004's fix is noted as "a guess"; QA-001's calibrator adds that the spec itself repeats unconditional wording, so the plan inherited it. | Medium | L2 |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact | Level |
|---|-------------------|-------------------|-------------------|--------|-------|
| X-001 | Whether Task 7's test pins the six `## Diffgate` bullets character for character | F4 fix: "List exceptions explicitly (Usage after token swap, Review Loop and Diffgate pinned by bullet checks, ...)", which treats the Diffgate bullets as already pinned by Task 7's bullet checks (consistent with plan:103's claim). | QA-005: "Task 7 pins only the seven Review Loop bullets; the six Diffgate bullets are checked for placement and lookup order only." Plan:110 supports Variant B: it pins "the seven Review Loop bullets ... equal to source.md 3.1 item 4" and for `## Diffgate` checks only placement and lookup order. Variant A's exception list would exempt an unpinned section from the drift guard. | Medium | L3 |

## Unique Contributions

Every finding appears in only one card; no finding is duplicated across the two cards (C-001 and C-002 pair findings on the same task area, but each names a different defect).

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | F1: `test_review_severity_rule.py` reads only `git ls-files` output (verified at lines 36-51), so the new untracked command and skill files are never scanned and the Task 5, 6 and 10 severity-rule ACs pass vacuously; fix: `git add -N` new `src/` and `tests/` files (never `.claude/`) before the run. | High |
| U-002 | A | F2: Task 5's verbatim subcommand table conflicts with the added `proxy_all` text in the `check` row; an exact-substring AC cannot pass both ways. | Medium |
| U-003 | A | F3: source of Task 5's expected verbatim blocks unspecified; should be literals in the test file (as plan:110 already says for Task 7). | Medium |
| U-004 | A | F4: Task 7 drift guard lacks exemptions for the edited `## Usage` section and the new or replaced sections. | Medium |
| U-005 | A | F5: shipping `T10-R3-reviser.txt` as a template for a step the design never runs. | Low |
| U-006 | A | F6: reviser line appended after "Finish with worker_done" lands after the finishing instruction. | Low |
| U-007 | A | F7: README lacks the exemption of the plain-command blindness audit from the "plain `/sc:spec-panel` ran" void rule (source.md:229). | Medium |
| U-008 | A | F8: Task 1 permits "not implemented" stubs but requires one JSON object per path and CLI exit 2/3 tests. | Low |
| U-009 | A | F9: pre-run gate and T11 text are plan additions; list them in Constraints and mark T11 as a draft. | Low |
| U-010 | A | F10: no `make lint` step for the new Python files. | Low |
| U-011 | A | Advisory: Task 4 turns "about 35" test cases into a hard floor that parametrization can inflate. | Low |
| U-012 | B | QA-001: review-1 findings without hunk or prior id are deferred and never blocking, so review 1 can yield a false PASS; apply surface-based deferral only from review 2 and add an end-to-end review-1 test. | High |
| U-013 | B | QA-002: the `deferred.md` disclosure sentence (source.md:40) and preserved reviewer labels have no task or AC. | Medium |
| U-014 | B | QA-003: the coverage matrix omits rows for C1-C12, input limits and ledger locking (source.md:133, 144, 149). Targets the audit artifact, not the plan; the plan does cover these in Tasks 1-4. | Low |
| U-015 | B | QA-004: the scoring note has no branch for an early PASS where `result-r3.json` is never written. | Medium |
| U-016 | B | QA-005: plan:103's promise of character-for-character Diffgate bullets is not implemented by Task 7. | Medium |
| U-017 | B | Calibrator `unraised_gaps`: plan:42 tests symlink refusal and temp-file cleanup but not the exclusive-create lock of `load_ledger`/`save_ledger`. | Low |

## Shared Assumptions

| # | Agreement Point | Underlying Precondition | Classification | Level |
|---|-----------------|------------------------|----------------|-------|
| A-001 | Both give `verdict: refactor`. | The plan's phase and task structure is sound and every defect is fixable by editing task text or ACs; each finding carries a local `fix`. | STATED | L2 |
| A-002 | Both treat source.md as the oracle and the plan's owner rulings (plan:26-30) as binding overrides. | Owner rulings correctly scope which deviations from source.md are authorized. Variant B states it ("Respected the owner rulings"); Variant A accepts the no-Unattended ruling in `confirmed_ok` and F9. | STATED | L2 |
| A-003 | Both direct bullet-fidelity fixes into Task 7's test. | Task 7 is the enforcement point named by plan:103 ("checked by Task 7's test"). | STATED | L3 |
| A-004 | Both accept that the loop can end before or without a review-3 fix (F5: no third fix; QA-004: early PASS). | Terminal states from source.md:33 (derived PASS at any review, halt at review 3). | STATED | L3 |
| A-005 | Both rely on `uv run pytest ...` ACs as the verification mechanism for the new files. | The named tests actually read the new files. Variant B assumes it implicitly; Variant A's F1 and `test_review_severity_rule.py:36-51` show the severity-rule test reads tracked files only. | CONTRADICTED | L3 |
| A-006 | [SHARED-ASSUMPTION] Both audits are static and read-only; neither ran a test or a collect-only count. | Static reading suffices to judge test-AC adequacy (vacuous passes, the 35-case floor, verbatim-substring tests). Neither card states this limit as a risk; Variant B notes "no tests run" only as a fact. | UNSTATED | L2 |
| A-007 | [SHARED-ASSUMPTION] Neither challenges Task 4's flg-r1 fixture expectations (plan:76: all four blocking fix hunks allowed, minor-only hunk rejected, chains of length 3, `proxy_all` 5, `blocking` 4). | The fixture as described in source.md 3.4 yields exactly those counts under the `proxy_all` definition of plan:49 (4 new blockers plus 1 MAJOR graded minor). Neither card verifies the arithmetic or the fixture shape. | UNSTATED | L3 |
| A-008 | Neither objects to the variant keeping `--unattended` clauses in Review Loop bullet 1 and Diffgate bullet 1 while lacking the `## Unattended mode` section. | The residual is acceptable because briefs never pass `--unattended` (plan:29). | STATED | L3 |
| A-009 | Both treat the experiment kit (Tasks 11 and 12 under `.dev/brainstorms/346-diffgate/`) as in-scope deliverables audited against source.md sections 4 and 5. | Plan scope at plan:19 includes section 4 and the brief templates fed by section 5. | STATED | L2 |

## Summary
- Total structural differences: 5
- Total content differences: 9
- Total contradictions: 1
- Total unique contributions: 17 (Variant A: 11, Variant B: 6)
- Total shared assumptions: 9 (STATED 6; UNSTATED 2, promoted as [SHARED-ASSUMPTION]: A-006, A-007; CONTRADICTED 1: A-005)
- Taxonomy distribution over S/C/X/A points (24): L3 = 10 (C-001, C-002, C-003, C-004, X-001, A-003, A-004, A-005, A-007, A-008); L2 = 11 (S-002, S-003, S-004, C-005, C-006, C-008, C-009, A-001, A-002, A-006, A-009); L1 = 3 (S-001, S-005, C-007)
- Highest-severity items: C-004 (High; the review-1 false-PASS risk is covered only by Variant B), U-012 (High, QA-001), U-001 (High, F1 vacuous severity-rule test), X-001 (Medium, Diffgate bullet pinning), A-005 (CONTRADICTED precondition that the tests read the new files)
