# Diff Analysis: sc:reflect Tier-2 reviewer-card Comparison

## Metadata
- Generated: 2026-11-04T07:45:00Z
- Variants compared: 3
  - Variant 1 = reviewer-1-card.yaml (analyzer, sonnet), verdict FAIL, 4 findings (2 blocking)
  - Variant 2 = reviewer-2-card.yaml (qa, haiku alias resolving to glm-5.3), verdict PASS, 5 findings (0 blocking)
  - Variant 3 = reviewer-3-card.yaml (refactorer, opus), verdict FAIL, 7 findings (1 blocking)
- Input warning: all three inputs are YAML, not markdown. Mode A type_check logged "Warn if file is not markdown"; proceeding. Variant copies wrap the YAML verbatim in a fenced block.
- Audited artifacts: plan = `.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md`; spec = `.../source.md`.
- Focus: correctness, coverage, deviation-classification.
- Severity rule (from caller): blocking only for wrong behaviour, a false claim, a missing required deliverable, or a security/data-loss risk; everything else is minor.
- Total differences found: 15 debated points (+ 8 unique contributions)
- Categories: structural (4), content (5), contradictions (2), unique (8), shared assumptions (4 promoted; 2 STATED not promoted)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Finding count and severity mix | 4 findings, 2 blocking (A-1, A-2) | 5 findings, 0 blocking | 7 findings, 1 blocking (S-1) | Medium |
| S-002 | Card metadata | reviewer, persona, model_class | adds `resolved_model: glm-5.3` (records alias resolution) | reviewer, persona, model_class | Low |
| S-003 | Deviation-category vocabulary | missing-requirement, ordering, unexecutable | weak-match, missing-requirement, missing-test, other | ordering, unexecutable, non-observable-ac, false-claim, other, scope | Medium |
| S-004 | Evidence granularity | plan/spec plus external repo files (sc-implement ledger.md, routing test) | plan/spec plus reflect artifacts (coverage-matrix.json) only | plan/spec plus external repo files (ledger.md, retry.md, routing test) | Low |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Variant 3 Approach | Severity |
|---|-------|-------------------|-------------------|-------------------|----------|
| C-001 | Task 16 (full suite, lint, verify-sync, `git add .dev/tasks`) depends on Tasks 14/15, which may end blocked | A-2 blocking/ordering: a blocked task halts the executor; Task 16 depends on Task 13 only, move 14/15 after it | Not raised; self-audit says no wrong behaviour found | S-1 blocking/ordering: `/sc:implement` stops on a blocked task (E-HALT-QA); renumber so suite task precedes the two smoke checks | High |
| C-002 | Source section 20 behavioural acceptance criteria not executed or recorded | A-1 blocking/missing-requirement: items 1-6 have no task, artifact or "not run" record; add a task + static assertions (incl. `--repo <R>` on every gh line in claim.md) | Q-3 minor/missing-test: ACs 2, 3, 6 unverified; plan declares residual at plan:25; add `t16-manual-acceptance.md` listing ACs 1-6, 8 as pending | Not raised | High |
| C-003 | `git fetch origin` only-origin rule (source:149, :321) not bound into Task 5/Task 3 bodies or a test | A-3 minor: add commands to claim.md and worker body + test assertion | Q-2 minor: add Wave 1 precondition to claim.md and "fetches only from origin" to agent body | Not raised | Low |
| C-004 | Task 11 AC "`git diff --stat` shows only this file" unobservable after earlier tasks changed tracked files | A-4 (part) minor: use `git diff -- <file>` | Not raised | S-3 minor/non-observable-ac: use `git diff -U0 -- <file>` with hunk range check | Low |
| C-005 | Task 10 new Other-commands row must be ASCII (and only live `/command` refs) | A-4 (part) minor: state ASCII-only | Not raised | S-6 minor: state ASCII and live-reference rule | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact |
|---|-------------------|-------------------|-------------------|-------------------|--------|
| X-001 | Overall verdict on the plan | `verdict: FAIL` | `verdict: PASS` | `verdict: FAIL` | High |
| X-002 | Is the section-20 gap a missing required deliverable? | A-1: "a missing required deliverable" (blocking) | self_audit: "no false claim, missing deliverable or security risk found"; Q-3 minor missing-test, residual declared at plan:25 | silent | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 (A-4 part) | Task 2 no_token check (plan:49) does not run with `env -u CLICKUP_API_TOKEN`; it would not print `no_token` if the shell exports a token | Low |
| U-002 | V2 (Q-1) | Five coverage-matrix rows carry best-task matches that do not satisfy them (INF-013, 054, 058, 059, 062) | Low |
| U-003 | V2 (Q-4) | source:132 requires the never-pass-`model` rule in SKILL.md and every ref; plan puts it only in SKILL.md (Task 6) and refs/tiers.md (Task 5) | Medium |
| U-004 | V2 (Q-5) | 67-row inferred matrix omits requirement-bearing regions; reviewer spot-checked each and found them covered | Low |
| U-005 | V3 (S-2) | Task 14 needs a session started after Task 13 with no stop/resume instruction; served-model evidence names no checkable source | Medium |
| U-006 | V3 (S-4) | Task 7 says the chains.md flag test reads `~/.claude/commands/sc/<name>.md` first "same check style as" a test that reads only source; installed read makes test machine-dependent (category false-claim) | Medium |
| U-007 | V3 (S-5) | Task 13 compares path-grep hits against local `master`, which can lag `origin/master` | Low |
| U-008 | V3 (S-7) | Task 14 writes `.dev/issues/smoke/` and Task 16 creates an Orca worktree outside the Constraints edit scope; the worktree is never removed | Low |

## Shared Assumptions

Agreement points scanned: no card raises Task 15 credential handling; no card raises a static `--repo` check as a finding; no card raises the AC 7 "static test" strength; no card reconciles "workers read-only git" with the Wave 1 `git fetch origin`.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | All cards silent on Task 15 (plan:215-224) | Task 15's in-session handling of `CLICKUP_API_TOKEN` (asked from the user, set in a Bash command's environment) keeps the token out of persisted storage, as plan:219 and source:296 require | UNSTATED | Yes |
| A-002 | All cards silent as a finding; V1 A-1 recommendation mentions a static `--repo <R>` assertion for refs/claim.md only | The `--repo <R>` invariant on every gh issue/pr/label call (source:319, AC 4 source:470) is adequately protected by prose instructions in Tasks 5/6 with no static test over SKILL.md, refs and worker bodies | UNSTATED (partially stated in V1 rec) | Yes |
| A-003 | All cards silent | A phrase-presence check ("never pass the `model` parameter" in SKILL.md and tiers.md, plan:121) satisfies AC 7's "the skill never passes `model` on an Agent call (static test)" (source:473) | UNSTATED | Yes |
| A-004 | V1 A-3 and V2 Q-2 both treat the fetch rule as a wording gap only | The plan's "workers make read-only `gh` and `git` calls only" (plan:55) is compatible with the Wave 1 worker running `git fetch origin` (source:149), which updates local refs | UNSTATED | Yes |
| (A-S1) | V1 A-2, V3 S-1 | The plan is executed by `/sc:implement`, where a non-complete task stops the run | STATED | No |
| (A-S2) | V1 A-1, V2 Q-3 | plan:25 limits live checks to Tasks 14/15 | STATED | No |

### Promoted [SHARED-ASSUMPTION] diff points

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | Token handling in Task 15 is safe | Unanimous silence | High (credential exposure) | Open for debate |
| A-002 | No static `--repo` test needed | Unanimous silence as a finding | High (fork-to-upstream misroute) | Open for debate |
| A-003 | Phrase test = AC 7 static test | Unanimous silence | Medium | Open for debate |
| A-004 | Read-only git vs `git fetch origin` | V1 and V2 agreement | Low | Open for debate |

## Debate taxonomy tags (AD-5)

| Point | Level | Signal |
|-------|-------|--------|
| S-001 | L2 | organization |
| S-002 | L1 | presentation |
| S-003 | L2 | organization/classification |
| S-004 | L1 | presentation |
| C-001 | L3 | state transition (blocked -> halt) |
| C-002 | L3 | validation rule |
| C-003 | L2 | dependency |
| C-004 | L1 | wording |
| C-005 | L1 | formatting |
| X-001 | L2 | organization of verdict |
| X-002 | L3 | validation rule |
| A-001 | L3 | guard |
| A-002 | L3 | guard / invariant |
| A-003 | L3 | validation rule |
| A-004 | L3 | state (local refs mutate) |

## Summary
- Total structural differences: 4
- Total content differences: 5
- Total contradictions: 2
- Total unique contributions: 8
- Total shared assumptions surfaced: 6 (UNSTATED: 4, STATED: 2, CONTRADICTED: 0)
- Convergence denominator (S + C + X + A): 15
- Highest-severity items: C-001, C-002, X-001, X-002, A-001, A-002
- Similarity check: differences well above 10% of comparable items; debate proceeds.
