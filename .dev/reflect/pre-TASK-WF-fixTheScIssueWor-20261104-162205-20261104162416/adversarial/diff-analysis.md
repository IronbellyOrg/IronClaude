# Diff Analysis: Tier-2 Reviewer Card Comparison (sc:reflect UC-1)

## Metadata
- Generated: 2026-11-04T16:42:37Z
- Mode: A (--compare), depth standard, focus correctness, coverage, deviation-classification, convergence threshold 0.80, non-interactive
- Plan under audit: `.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/TASK-WF-fixTheScIssueWor-20261104-162205.md` (78 lines)
- Spec: `.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/source.md` (1 line)
- Variants compared: 3
  - Variant 1: `variant-1-original.md` (reviewer 1, analyzer, sonnet), 6 findings, verdict PASS, confidence 0.80
  - Variant 2: `variant-2-original.md` (reviewer 2, qa, haiku), 5 findings, verdict PASS, confidence 0.86
  - Variant 3: `variant-3-original.md` (reviewer 3, refactorer, opus), 6 findings, verdict PASS, confidence 0.80
- Total differences found: 23
- Categories: structural (3), content (9), contradictions (2), unique (9), shared assumptions (3 promoted)
- Debate diff points (convergence denominator S+C+X+A): 17

## Finding Clusters (deduplicated, used for the merged verdict)

Every one of the 17 variant findings maps to exactly one cluster.

| Cluster | Topic | Source findings | Classes proposed | Severities proposed |
|---|---|---|---|---|
| M-01 | Early section `## Your files are tool inputs, not reports` goes beyond source.md:1 (spec names only the Rules section); authority is plan prose (plan:19) quoting a coordinator message stored in no package file | R1-F1 (part), R2-2, R3-F5 (part) | authorized (R1), drift (R2), grounding_gap (R3) | minor (all) |
| M-02 | Task 3 SKILL.md spawn-rule line: SKILL.md is not in the spec's Files list (source.md:1); plan:20 calls it "judged needed" | R1-F1 (part), R2-1, R3-F5 (part) | authorized (R1), drift (R2), grounding_gap (R3) | minor (all) |
| M-03 | Rules bullet (plan:29) is a pointer to the early section; it omits `E-WORKER-NO-OUTPUT`, the consumers (`gh --body-file`, `/sc:recommend`) and the harness-note exemption that source.md:1 asks to be in the Rules section | R1-F2, R2-3 | necessary (R1), drift (R2) | minor (both) |
| M-04 | `flags-user.md` omitted from the worker file list (plan:21) is grounded in refs/create.md | R1-F3 | necessary | minor (no change) |
| M-05 | Negative tests (plan:47-48) do not first assert the removed text exists exactly once in the real file (existing pattern, test file:163) | R1-F4 | drift | minor |
| M-06 | Exact texts (plan:24-32) are inline code spans that contain backticks; outer delimiter, two-space indent and trailing-period boundary are ambiguous for a byte-identical contract | R1-F5, R2-5, R3-F1 | grounding_gap (all) | minor (all) |
| M-07 | `make verify-sync` (plan:72-77) could fail for unrelated drift with no instruction | R1-F6 | grounding_gap | minor |
| M-08 | Reviewer brief coverage slice lists only INF-004/005 (audit record, not plan) | R2-4 | grounding_gap | minor (no plan change) |
| M-09 | "the reports under `analysis/`" (plan:26) repeats the harness trigger words "report"/"analysis" in the sentence that says these files are not reports | R3-F2 | drift | minor |
| M-10 | Parenthetical "(`gh --body-file` posts and `/sc:recommend`)" (plan:26) reads as the full consumer list; flags-t1.md feeds the adversarial --compare, scout.md/flags.md/draft-notes.md are read by the orchestrator | R3-F3 | drift | minor |
| M-11 | SKILL.md line (plan:32) "names each exact path" cannot hold for `analysis/` (name chosen by /sc:analyze, only when out_of_date); refs' spawn lists name no paths and stay unchanged | R3-F4 | drift | minor |
| M-12 | Helper (plan:45) checks the Rules bullet is inside `## Rules` but not that it directly follows the "Writing only under" bullet, as plan:27 requires | R3-F6 | drift | minor |

## Structural Differences

| # | Area | Variant 1 (sonnet:analyzer) | Variant 2 (haiku:qa) | Variant 3 (opus:refactorer) | Severity | Level |
|---|------|-----------|-----------|-----------|----------|-------|
| S-001 | Finding count and ID scheme | 6 findings, `R1-Fn` | 5 findings, `R2-n` | 6 findings, `R3-Fn` | Low | L1 |
| S-002 | Self-audit grounding depth | Lists files read and scans checked; notes no plugins mirror exists | Enumerates every anchor with a line number (agent line 11; Writing-only bullet t1:26, t2:26, t3:25; SKILL.md:64), measures SKILL.md at 153 lines, checks red-run feasibility and file-list union | Reads spawn sections of refs/claim.md and refs/create.md in addition; checks insertion points and contradictions with Return value/Templates/no-Edit rules | Medium | L2 |
| S-003 | Class distribution | authorized 1, necessary 2, drift 1, grounding_gap 2 | drift 3, grounding_gap 2 | drift 4, grounding_gap 2 | Medium | L2 |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Variant 3 Approach | Severity | Level |
|---|-------|-------------------|-------------------|-------------------|----------|-------|
| C-001 | Scope expansion beyond source.md (M-01, M-02) | One finding: authorized, record the coordinator message and say SKILL.md is author's judgement | Two findings: both drift; record requester sign-off or descope Task 3; keep early section with rationale or fold into Rules | One finding: grounding_gap; save the coordinator message under the package `artifacts/` | High | L2 |
| C-002 | Rules bullet completeness against the spec rule (M-03) | necessary; make bullet self-contained or state it is a pointer | drift; add `E-WORKER-NO-OUTPUT` and ideally the tool calls | Silent | High | L2 |
| C-003 | Exact-text delimiter ambiguity (M-06) | grounding_gap; fenced blocks or state outer backticks are delimiters | grounding_gap; adds trailing-period ambiguity; module constants could be canonical | grounding_gap; adds two-space indent and the mechanism (consistent mis-copy in constant and agent text passes) | Low | L1 |
| C-004 | Test-design robustness (M-05, M-12) | Negative tests lack the exists-exactly-once pre-assertion | Silent; states red run feasible | Helper lacks the position check after "Writing only under" | Medium | L3 |
| C-005 | Completeness of the file list and consumer list in the early paragraph (M-04, M-10) | flags-user.md omission grounded, no change | File list equals union of worker-written files (self-audit) | Consumer parenthetical incomplete (flags-t1.md, scout.md, flags.md, draft-notes.md consumers) | Medium | L2 |
| C-006 | Wording that repeats harness trigger words (M-09) | Silent | Silent | "the reports under analysis/" should be "the files under analysis/" | Medium | L1 |
| C-007 | Feasibility of the SKILL.md spawn-line obligation "names each exact path" (M-11) | Silent | Silent (treats SKILL.md only as scope drift) | Cannot hold for `analysis/`; name the directory; record refs unchanged on purpose | Medium | L3 |
| C-008 | Verification-environment risk (M-07) | verify-sync could fail for unrelated drift; report, do not fix | 500-line cap measured, no breakage | Scans not hit | Low | L2 |
| C-009 | Audit-record gap (M-08) | Silent | Brief coverage slice lists only INF-004/005; attach INF-001..003 | Silent | Low | L2 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact | Level |
|---|-------------------|-------------------|-------------------|-------------------|--------|-------|
| X-001 | Deviation class of the scope expansion (early section + SKILL.md line) | authorized (coordinator message quoted in plan:19 is the authority) | drift (spec does not authorize; retry evidence does not prove the Rules-only rule is insufficient) | grounding_gap (the authorizing message is not stored, so the class cannot be verified) | High | L2 |
| X-002 | Deviation class of the pointer-style Rules bullet | necessary (content lives in the early section; deviation serves the goal) | drift (spec's rule content, incl. `E-WORKER-NO-OUTPUT`, is missing from Rules) | (silent) | Medium | L2 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | Variant 1 | flags-user.md omission is grounded (R1-F3) | Low |
| U-002 | Variant 1 | Negative-test vacuity without exists-once pre-assertion (R1-F4) | Medium |
| U-003 | Variant 1 | verify-sync unrelated-drift instruction (R1-F6) | Low |
| U-004 | Variant 2 | Reviewer brief coverage slice gap (R2-4) | Low |
| U-005 | Variant 2 | Retry evidence shows a general spawn-prompt statement failing, not that a Rules-section rule is insufficient (R2-1) | Medium |
| U-006 | Variant 3 | "reports under analysis/" repeats harness trigger words (R3-F2) | High |
| U-007 | Variant 3 | Consumer parenthetical incomplete (R3-F3) | Low |
| U-008 | Variant 3 | "names each exact path" infeasible for analysis/ (R3-F4) | Medium |
| U-009 | Variant 3 | Helper lacks Rules-bullet position check (R3-F6) | Low |

## Shared Assumptions

Agreement points scanned: all three verdicts PASS; all 17 findings minor; all three agree on the delimiter gap (C-003); all three self-audits state the new text hits no existing scan; none questions whether the plan proves the behaviour change.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | All verdicts PASS; no variant asks for behavioural proof | Text-pinning tests plus the three text edits are sufficient to make workers write their files under the live harness note; no acceptance criterion requires a live re-run (for example a re-claim like #365) showing `summary.md` is written | UNSTATED | Yes |
| A-002 | All variants accept "write it with the Write tool" as actionable | The Write tool is in each worker's tool allowlist (orchestrator check: `tools: Read, Grep, Glob, Write, Bash` at line 5 of each issue-worker-t*.md) | UNSTATED | Yes |
| A-003 | All variants accept `make sync-dev` as the deploy step | The runtime that failed on #365 reads a copy refreshed by `make sync-dev` (project `.claude/agents/`, read first per SKILL.md:62); the installed `~/.claude/agents/` copy needs `superclaude install`, which the plan does not mention | UNSTATED | Yes |
| A-004 | All self-audits | Insertion anchors exist exactly once in each target file | STATED (V2 self-audit lists them) | No |
| A-005 | All self-audits | New text hits no existing scan (gh repo scan, dual-surface, src path, 500-line cap) | STATED (all three) | No |

### Promoted [SHARED-ASSUMPTION] diff points

| A-NNN | Assumption | Source Agreement | Impact | Status | Level |
|---|---|---|---|---|---|
| A-001 | [SHARED-ASSUMPTION] Text-pinning tests are sufficient proof that workers will write files | All PASS, no behavioural AC | High | Open for debate | L3 |
| A-002 | [SHARED-ASSUMPTION] Write tool is in every worker's allowlist | "write it with the Write tool" accepted | Low | Open for debate (orchestrator found it true) | L2 |
| A-003 | [SHARED-ASSUMPTION] `make sync-dev` reaches the runtime copy | sync-dev accepted as sufficient | Medium | Open for debate | L2 |

## Taxonomy Tagging

- L1 (surface): S-001, C-003, C-006 (3)
- L2 (structural): S-002, S-003, C-001, C-002, C-005, C-008, C-009, X-001, X-002, A-002, A-003 (11)
- L3 (state mechanics: guard, validation rule, boundary): C-004, C-007, A-001 (3)
- All three levels covered: yes

## Summary
- Total structural differences: 3
- Total content differences: 9
- Total contradictions: 2
- Total unique contributions: 9
- Total shared assumptions surfaced: 5 (UNSTATED: 3, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-001, U-006, A-001
- Similarity check: variants differ on 23 items out of 17 findings; not substantially identical, debate proceeds
