# Diff Analysis: Reviewer Card Comparison (pre-execution reflect, TASK-RF-issue-watcher-20261107-150955)

## Metadata
- Generated: 2026-11-07T19:20:00+00:00
- Variants compared: 3
  - Variant 1: reviewer-1-card.yaml (analyzer, sonnet; calibrated confidence 0.75) - 194 lines, 2261 words, 5 findings (all minor), 35 coverage rows
  - Variant 2: reviewer-2-card.md (qa, haiku; calibrated confidence 0.85) - 174 lines, 2529 words, 4 H2 sections, 2 findings (MEDIUM), 25 AC rows + 46 coverage-slice rows + 19 test-file rows
  - Variant 3: reviewer-3-card.yaml (refactorer, opus; calibrated confidence 0.85) - 347 lines, 2688 words, 8 findings (2 blocking, 6 minor), 60 coverage rows
- Subject of all three cards: `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md` (1029 lines) audited against `docs/designs/issue-watcher.md` (935 lines)
- Authority for declared deviations: `research/06-gap-fill-decisions.md` and the task file's Open Questions. A declared deviation is not a defect.
- Severity model for the merge: binary (blocking | minor), decided from evidence, not from reviewer labels.
- Total differences found: 28
- Categories: structural (4), content (11), contradictions (9), unique (5), shared assumptions (4: UNSTATED 3, STATED 0, CONTRADICTED 1)
- Taxonomy tags (L1 surface / L2 structural / L3 state mechanics) are given per point in the last column.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity | Level |
|---|------|-----------|-----------|-----------|----------|-------|
| S-001 | Card format | YAML: findings, coverage_judgements, self_audit, citations, calibration | Markdown tables (reviewer returned markdown instead of the requested YAML); calibration in a fenced YAML block | YAML, same schema as Variant 1 | Low | L1 |
| S-002 | Coverage unit set | 13 T-rows + 22 INF rows from the brief slice | AC-1..AC-25 as atomic units, plus 46 coverage-slice rows and a 19-row named-test-file table | ~60 INF/T rows (INF-105..INF-157 plus slice rows) | Medium | L2 |
| S-003 | Severity vocabulary | minor only (binary scale, no blocking) | MEDIUM (non-binary scale) | blocking / minor (binary scale) | Medium | L1 |
| S-004 | Category vocabulary | coverage_gap, sequencing, contradiction, wrong_citation, gate_weakness | Deviation taxonomy "Drift" (Authorized expansion / Necessary deviation / Drift / Regression) | sequencing, contradiction, gate_weakness, other | Low | L1 |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Variant 3 Approach | Severity | Level |
|---|-------|-------------------|-------------------|-------------------|----------|-------|
| C-001 | Withdrawn-commit branch of Step 10.2 vs the verbatim prompt rule of Step 10.6 | R1-003 (minor, contradiction): `<BASE SHA>` comes from `base-sha.txt`, which this branch never writes; no permitted substitution | Not raised; says the checkpoint sequence captures BASE before the commit | Not raised | Medium | L3 |
| C-002 | Step 8.10 xdist mechanism cited as "exactly as test.yml:29 does" | R1-004 (minor, wrong_citation): CI uses `uv pip install`, the gate uses `uv run --offline --with` | Not raised; Steps 8.10 and 9.6 accepted as running xdist | Not raised | Low | L1 |
| C-003 | Gate G-10 `git diff --exit-code pyproject.toml Makefile` misses staged changes | R1-005 (minor, gate_weakness): P10 allowlist catches it later | Not raised | INF-112 covered via Step 9.15 and 10.3 | Low | L3 |
| C-004 | Per-phase gate re-run loops have no attempt cap or HALT; post-gate fixes unreviewed | Not raised | Not raised | R3-003 (minor, gate_weakness) | Medium | L3 |
| C-005 | final-change-set.md written once in 9.F1 and never regenerated after fix cycles | Not raised | Not raised | R3-004 (minor, sequencing) | Medium | L3 |
| C-006 | Step 4.1a lets `record` import predicate functions; design 5.3 allows types only | INF-022 covered (architecture lint and AST test) | INF-022 covered | R3-005 (minor, contradiction): undeclared departure from design line 239 | Medium | L2 |
| C-007 | Marker-contract test reads real installed `~/.claude` copies | Not raised | INF-121-equivalent not raised; marker parity accepted | R3-006 (minor, other): conflicts with the tmp_path / no-real-HOME lens rule | Low | L2 |
| C-008 | Step 7.3 two-line main.py diff vs Step 7.9 pinned format fix over all of main.py | Not raised | Not raised | R3-007 (minor, contradiction) | Low | L2 |
| C-009 | Step 10.7 staging failure never reverts Done | Not raised | Not raised | R3-008 (minor, gate_weakness) | Low | L3 |
| C-010 | Overall verdict on the task file | No blocking defect; 5 minor | 2 MEDIUM drifts (planned-test adequacy), 23/25 AC adherent | 2 blocking, 6 minor | High | L2 |
| C-011 | Self-disclosed reading limits | Did not read Phases 1-3, Gates A-D, Final and M4 gate items (737-837), frontmatter, research/06 | Claims all 25 AC and 46 slice rows judged; no commands run | Did not read Gate D (619-672), bodies of 9.M4-9.M13, BUILD-REQUEST.md | Medium | L2 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact | Level |
|---|-------------------|-------------------|-------------------|-------------------|--------|-------|
| X-001 | POST reflect `--remediate` (Step 10.6) leaves source edits after the single checkpoint commit, ungated and unstaged (Step 10.7 stages only `.dev/tasks`) | R1-002: real, minor (sequencing) | Not a defect: "checkpoint sequence captures BASE before the single commit ... halts on commit/hook failure" | R3-001: real, blocking (sequencing); cites research/06:30 | High | L3 |
| X-002 | T-2 (`backoff_elapsed` with the `attempts` < 3 conjunct) | partially_covered; R1-001 minor: Step 4.1c drops the conjunct | covered (substance present despite missing token) | covered: "the attempts < 3 check is applied in run_cycle" | Medium | L3 |
| X-003 | INF-123 (`make test` as a gate) | partially_covered under declared DF-05 | covered under DF-05 | partially_covered under declared DF-05 | Low | L2 |
| X-004 | INF-155 (section 13 gates pass) | not judged | covered under authorized gate substitutions | partially_covered (make test replaced by G-2 under DF-05) | Low | L2 |
| X-005 | INF-016 (non-goals NG-1..NG-5) | partially_covered: only NG-2 has an explicit guard | covered | covered | Low | L2 |
| X-006 | INF-146 / AC-14 (every exit writes an audit line or the stderr fallback) | not judged | partially_covered; R2-002: no cycle-level append/save-failure injection test | covered (audit line on every exit; rotation keeps 4) | Medium | L3 |
| X-007 | AC-6 / INF-138 (final revalidation re-read before dispatch) | not judged | partially_covered; R2-001: Step 6.7 lacks lost-label, voided-approval, changed-Project-status re-read cases | INF-138 covered ("re-read failure skips") | Medium | L3 |
| X-008 | Full-tree lint gates: "exit 0" vs "a finding in an untouched file is recorded and NOT fixed" | Gate commands executable as written (check 3) | INF-124 covered | R3-002: blocking contradiction, no passing path and no halt rule | High | L3 |
| X-009 | Automatic requirement-to-item mapping in the brief | Not challenged | "Lexical matches were not accepted as proof" | Several automatic "none" mappings declared wrong (INF-108, INF-122, INF-135, INF-147, INF-153) | Low | L2 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | Variant 2 | AC-1..AC-25 coverage table with implementation, test-writing and test-running items per criterion | High |
| U-002 | Variant 2 | 19-row named-test-file table (creating item and first running item for each) | Medium |
| U-003 | Variant 3 | Corrections of wrong automatic mappings, plus pyproject.toml and Makefile line verification (lines 16, 54, 114, 179; Makefile:50) | Medium |
| U-004 | Variant 1 | More than 12 concrete external claims verified against real files (install_user_setup.py, main.py, swarm/atomic.py, Makefile, .pre-commit-config.yaml) | Medium |
| U-005 | Variant 3 | Widest coverage register (INF-105..INF-157) with declared-deviation notes (DF-05, DF-09, DF-10, DF-29, DF-55, DF-60) | High |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-----------|------------------|--------|--------|
| A-001 | [SHARED-ASSUMPTION] The task-file line numbers cited by every card match the current file state (no edit to the task file since the reviews); every cited excerpt exists at its line. | All three cite line numbers; none states that the file was unchanged between reviews | High (a finding whose cited text does not exist is dropped) | UNSTATED |
| A-002 | [SHARED-ASSUMPTION] `/sc:reflect --mode post --remediate` can modify source and test files outside `.dev/tasks` (the state change that makes X-001 a defect at all). | Variants 1 and 3 depend on it; Variant 2 is silent | High (decides whether X-001 is a defect) | UNSTATED |
| A-003 | [SHARED-ASSUMPTION] A pre-execution review can judge test adequacy and gate boundaries from item text alone, i.e. a scenario not named in an item will not be written by the executor or caught by a later guard (Step 9.17 semantic trace, Final lenses). | All three depend on it; Variant 2 notes Step 9.17 as a backstop but still reports | Medium (decides blocking vs minor for R2-001, R2-002, R1-001) | UNSTATED |
| A-004 | [SHARED-ASSUMPTION] The unchanged tree is lint-clean and format-clean under `make lint` and the pinned ruff (so the exit-0 gates are passable). | Variants 1 and 2 implicitly assume it is; Variant 3 assumes it may not be | High (decides whether X-008 is a defect) | CONTRADICTED |

## Summary
- Total structural differences: 4
- Total content differences: 11
- Total contradictions: 9
- Total unique contributions: 5
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 0, CONTRADICTED: 1)
- Highest-severity items: C-010, X-001, X-008, A-001, A-002, A-004
- Convergence denominator (S + C + X + A): 28
- Taxonomy coverage: L1 = S-001, S-003, S-004, C-002; L2 = S-002, C-006, C-007, C-008, C-010, C-011, X-003, X-004, X-005, X-009; L3 = C-001, C-003, C-004, C-005, C-009, X-001, X-002, X-006, X-007, X-008, A-001, A-002, A-003, A-004
- Similarity check: differences far exceed 10% of comparable items; debate proceeds.
