# Diff Analysis: reflect reviewer card comparison (Mode A, 3 cards)

## Metadata
- Generated: 2026-11-19T15:10:00Z
- Variants compared: 3
  - Variant 1 = `variant-1-original.md` (reviewer card 1, analyzer lens, sonnet class, calibrated 0.79)
  - Variant 2 = `variant-2-original.md` (reviewer card 2, qa lens, haiku class, calibrated 0.81)
  - Variant 3 = `variant-3-original.md` (reviewer card 3, refactorer lens, opus class, calibrated 0.87)
- Audited work: plan `.dev/tasks/to-do/TASK-WF-stage3CRequest-20261119-143901/TASK-WF-stage3CRequest-20261119-143901.md` against spec `.../source.md`
- Grading rule for every finding: `## Review severity rule` of `src/superclaude/agents/reflect-reviewer.md` (lines 117-123)
- Total differences found: 21 (structural 4, content 6, contradictions 3, unique 6, shared assumptions promoted 2)
- Categories: structural (4), content (6), contradictions (3), unique (6), shared assumptions (2 promoted of 4 extracted)
- Step 1 was run by the orchestrator as a neutral analytical pass (no advocate input). Facts the orchestrator spot-checked before writing this file: the plan has no case-insensitive match for `branch|origin/master|summary`; `git grep -n "reflect-reviewer" -- tests src` names 13 files, of which 4 are YAML fixtures and 2 are test files outside the plan's four (`tests/skills/test_worker_contract.py`, `tests/unit/test_cli_install.py`); `sha256sum .dev/stage3c-variants/brainstorm/reflect-reviewer.md` = `7696a2b2...c760ec0ed8`, equal to source.md:24.

### Similarity check
Comparable items: 10 finding topics (branch, known limits, byte identity/acceptance pinning, test-discovery wording, backtick rendering, 83-test claim, authorized-expansion checks, coverage-matrix inventory, origin/master line drift, PR #605 merge state) plus 5 structural dimensions (verdict line, path style, unit granularity, placement of minor findings, label column) = 15. Items on which the cards differ: 13 of 15 (only "PR #605 not verified" and "three H2 sections" are identical). 13/15 = 87%, far above the 10% skip threshold. **Debate runs (Steps 2-3 not skipped).**

## Structural Differences

| # | Area | Variant 1 (analyzer) | Variant 2 (qa) | Variant 3 (refactorer) | Severity |
|---|------|----------------------|----------------|------------------------|----------|
| S-001 | Verdict line in header | None; verdict implied by "2 Blocking" in Total deviations | Explicit `**Verdict**: FAIL — two blocking omissions` | None; verdict stated in last line of Notes ("Findings 1 and 2 block") | Low |
| S-002 | Path style in Location/Evidence | Short `plan:N` / `source.md:N` | Full absolute paths throughout | Short `plan:N` / `source.md:N`, plus repo-relative paths | Low |
| S-003 | Adherence-summary unit granularity | 22 units, 18 adherent; units listed by kind | 45 units (43 matrix INF units + 2), 40 adherent; names INF ids | 30 units, 25 adherent; units listed by kind with counts | Medium |
| S-004 | Where minor findings sit | 2 Medium rows in table; one Note in a stray paragraph between table and summary | All minor items in Notes; table holds only the 2 Blocking rows | Medium row and an Authorized-expansion Note row in table; other Notes in Notes | Medium |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | Branch finding (spec source.md:3 "fresh branch made from `origin/master`") | Row 1 `Blocking (Missing)`, label HIGH; affected action = choosing the branch; evidence includes the grep that returns no match | Row 1 `Blocking (Missing)`, label MEDIUM; same affected action | Row 1 `Blocking (Missing)`, label HIGH; adds that the checked-out branch holds the stage 3b commits | Low |
| C-002 | Known-limits finding (source.md:65-69) | Row 2 `Blocking (Missing)`, HIGH; lists all three limits; says plan:21 "two real gaps" states a judgment as fact | Row 2 `Blocking (Missing)`, MEDIUM; lists all three limits incl. "digits and apostrophes rather than lowercase letters"; says "two real gaps" lacks the qualification; Notes: INF-036 containment match is not semantic | Row 2 `Blocking (Missing)`, HIGH; same three limits; says plan:21 contradicts the judgment limit | Medium |
| C-003 | Byte identity and acceptance pinning (source.md:24, 39-44; plan:22, 44-46) | Row 3 `Medium`: greps pin only start, end and join; sha256 and variant path not carried; nothing checks the needles were added | Notes: not a deviation, because the spec itself prescribes the partial greps and the manual diff | Row 3 `Medium`: sha256 and variant path dropped; middle-token error passes greps and needles; instruction itself is correct | High |
| C-004 | "Run every test file that output names" (source.md:34; plan:41) | Row 4 `Medium`: ambiguous, YAML fixtures match; wording from spec | Not raised; Notes say test-discovery record is carried | Notes (b) `Note`: names the 4 YAML fixtures and 2 extra test files; wording from spec | Medium |
| C-005 | Escaped backticks at plan:44 render broken in Markdown | Note (paragraph outside table) | Not raised | Note (Notes (a)) | Low |
| C-006 | "83 tests" claim at plan:39 | Not verified (Notes) | Not verified (last line) | `Note`: no artifact backs it; feeds no acceptance check | Low |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Is the byte-identity / partial-pinning gap a deviation at all? | Yes, Medium (row 3: "The plan carries neither the spec's sha256 ... nor the variant path") | No: "their limited automated coverage is **not** an additional plan deviation" (Notes) | Yes, Medium (row 3: "the plan drops the spec's way of checking byte identity") | Medium |
| X-002 | Grade of the test-discovery wording finding | `Medium` (row 4) | Not a finding ("test-discovery record ... carried") | `Note` (Notes (b): "The wording comes from the spec ... so this is a Note") | Low |
| X-003 | Grade of the known-limits finding | `Blocking (Missing)`; calibration 1 adds that Decision also applies (plan:21 "two real gaps" is an unsupported stated reason) | Card: `Blocking (Missing)`; its own blind calibration disagrees: "limits summary is owner-facing information; changes no executed behaviour or acceptance check; Medium" | `Blocking (Missing)`; calibration 3: "borderline row of the four" | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | Variant 1 | Sub-claim of row 3: "Nothing checks that the two new needles were added to the test tuple: `uv run pytest` passes whether or not they are there" (plan:46 / source.md:43 say "passes with the two new needles") | Medium |
| U-002 | Variant 2 | Coverage-inventory Note: the coverage matrix omits the copy-and-adapt and pre-review requirements of source.md:3 (artifacts/coverage-matrix.md:32-35); non-gating | Low |
| U-003 | Variant 2 | Explicit verdict line `FAIL — two blocking omissions` and a "Next" instruction (resolve findings 1 and 2 before execution) | Medium |
| U-004 | Variant 3 | Row 4 Authorized expansion, `Note`: plan:61 `git status --porcelain -- src plugins` check, plan:37 frontmatter field names, plan:60 richer final-run artifact; none crosses an exclusion; `make sync-dev` writes only under `.claude/` | Medium |
| U-005 | Variant 3 | Unverified risk: if `origin/master`'s agent line 122 differs from this worktree's, the anchor and the whole-file sha256 equality may fail on a fresh branch | Medium |
| U-006 | Variant 3 | Concrete enumeration of the extra files `git grep` names (4 YAML fixtures, `test_worker_contract.py`, `test_cli_install.py`) and whole-tree scan checks (BANNED_SEVERITY_PHRASES, SWEEP_PHRASES, CAP_REGRESSION, S-labels) with test-file line numbers | Medium |

## Shared Assumptions

Agreement points scanned: all three cards grade the branch and known-limits findings Blocking (Missing); all three call the verdict FAIL; all three report PR #605 merge state as not verified; none ran tests.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | C-001 (all cards: branch row Blocking) | "Run it on a fresh branch made from `origin/master`" (source.md:3) refers to executing the package with `/sc:implement`, not to the step of writing/copying and reviewing the package; so the plan, not the package-writing step, must carry it | UNSTATED | Yes |
| A-002 | C-002 / X-003 (all cards: known-limits row Blocking (Missing)) | "the plan's summary" (source.md:65) names a section of the plan document, so its absence from the plan is "a required ... section ... named by the task ... absent in substance", rather than a summary given elsewhere (for example the owner-facing chat summary or the reflect report) | UNSTATED | Yes |
| A-003 | C-001 | `/sc:implement` does not itself create a fresh branch, so an executor following the plan edits the checked-out branch | STATED (Variant 1 row 1: "As written, `/sc:implement` edits whatever is checked out"; Variant 3 row 1) | No |
| A-004 | All cards | The live worktree, not an isolated snapshot, is a valid grounding root for this pre-execution review | STATED (Variant 2 Notes: "The brief supplied a live grounding root rather than an isolated snapshot") | No |

Promoted [SHARED-ASSUMPTION] points:

| # | Assumption | Impact | Status |
|---|------------|--------|--------|
| A-001 | [SHARED-ASSUMPTION] "Run it on a fresh branch" applies to package execution and must be carried by the plan | High: if false, the branch row is not a plan deviation and the verdict could change | Open for debate |
| A-002 | [SHARED-ASSUMPTION] "the plan's summary" is a required section of the plan document | High: decides whether the known-limits row meets the Missing condition | Open for debate |

### Debate taxonomy tags
- L1 surface: S-001, S-002, C-005
- L2 structural: S-003, S-004, C-001, C-002, C-006, X-002
- L3 state mechanics (guard / validation rule / acceptance-check boundary): C-003, C-004, X-001, X-003, A-001, A-002

All three levels have at least one point.

## Summary
- Total structural differences: 4
- Total content differences: 6
- Total contradictions: 3
- Total unique contributions: 6
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 2, CONTRADICTED: 0)
- Convergence denominator (S + C + X + A): 4 + 6 + 3 + 2 = 15
- Highest-severity items: C-003, X-003, A-001, A-002
