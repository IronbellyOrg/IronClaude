# Base Selection Report (D07, topology)

Variant A = variant-1-original.md (OURS). Variant B = variant-2-original.md (CLAY). Pass 1 was done by the orchestrator in input order (A then B). Pass 2 was done by an independent agent in reverse order (B then A) without sight of pass 1: scoring-pass-2.md.

## Quantitative Scoring (50% weight)

Computed by grep and counts on the two files (read-only commands; word and token counts in the notes).

| Metric | Weight | Variant A (OURS) | Variant B (CLAY) |
|--------|--------|------------------|------------------|
| requirement_coverage | 0.30 | 1.000 (12 of 12 terms: registry, one per repo, in flight, multi-org, `.dev/coordinators`, `orca repo list`, `issue-watch.d`, `COORD-`, and the four required paper parts) | 0.833 (10 of 12: no `orca repo list` and no `issue-watch.d` anywhere in the file) |
| internal_consistency | 0.25 | 0.933 (1 intra-paper contradiction, X-005, among 15 scorable claims) | 1.000 (0 of 16) |
| specificity_ratio | 0.15 | 1.000 (168 numeric tokens, 24 line cites, 0 vague words) | 1.000 (146 numeric tokens, 32 line cites, 0 vague words) |
| dependency_completeness | 0.15 | 1.000 (every abbreviation defined in the key; no broken internal reference) | 1.000 (same) |
| section_coverage | 0.15 | 1.000 (6 H2 sections) | 1.000 (6 H2 sections) |
| **quant_score** | | **0.983** | **0.950** |

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Both passes scored all 30 criteria for both variants with a cited reason. Pass 1 (orchestrator) gave A 20 and B 22. Pass 2 (independent, reverse order) gave A 23 and B 23. Twelve criterion-variant pairs disagreed (table below); each was re-evaluated with both pieces of evidence and the re-evaluation is final.

### Dimension subtotals after reconciliation

| Dimension | Variant A | Variant B | Reason in one line |
|-----------|-----------|-----------|--------------------|
| Completeness (5) | 3 | 3 | Both lack success criteria (C4) and out-of-scope lines (C5) |
| Correctness (5) | 3 | 5 | A: branch name used two ways (K3) and a one-per-project claim beside a per-scope fact (K4). B: "owner of record" is ambiguous, which is a clarity fault, not a false statement |
| Structure (5) | 5 | 5 | Same required order, key, six sections |
| Clarity (5) | 4 | 2 | B: "owner of record" does not say who (L1), design codes undefined (L4), no next step (L5). A: codes ADD2, ADD3 undefined (L4) |
| Risk Coverage (5) | 3 | 3 | Neither gives probability or impact (R1) or a mitigation for every risk (R2) |
| Invariant and Edge Case (5) | 5 | 5 | Both cover limits, state across components, guards, counts and interactions with evidence |
| **qual_score** | **23/30 = 0.767** | **23/30 = 0.767** | |

### Edge Case Floor Check
Both variants score 5/5 on Invariant and Edge Case Coverage (floor is 1/5). Both eligible as base.

## Position-Bias Mitigation

Pass 1 against Pass 2, only the pairs that disagreed (all other 48 pairs agreed):

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Re-evaluation reason |
|-----------|---------|--------|--------|-----------|-------|----------------------|
| K1 no factual errors | B | NOT MET | MET | DISAGREE | MET | DESIGN line 3 does call Clay "the owner", so "owner of record in the design" is literally true; the fault is ambiguity (L1) |
| K3 terminology | B | NOT MET | MET | DISAGREE | MET | "orchestrator", "poll", report session kept distinct; the owner ambiguity is scored once, under L1 |
| L1 unambiguous | B | MET | NOT MET | DISAGREE | NOT MET | The sentence does not say who; this is the root of the dispute (analysis FULL-REPORT item 6) |
| K1 no factual errors | A | NOT MET | MET | DISAGREE | MET | Quoted rows match the sources; the "built" claim names the dispatcher files; the `CALL_CAP` line is correct on the master snapshot |
| K3 terminology | A | MET | NOT MET | DISAGREE | NOT MET | Mechanism 3 says `Coordinator` branch, fact 1 says `coordinators` branch; flagged but unresolved |
| K4 no contradictions | A | MET | NOT MET | DISAGREE | NOT MET | One `COORD-<RepoName>` per project beside Q26's `<dev>--<N>` coordinators per scope (conceded in Round 2) |
| L4 terms defined | A | MET | NOT MET | DISAGREE | NOT MET | ADD2, ADD3, "day cap", "kill switch" undefined; B has the same fault, so held equal |
| R4 external dependencies | A | NOT MET | MET | DISAGREE | MET | Cron minimal environment and Orca list verified in fact 5; the rate-limit wait in mechanism 2 |
| R5 monitoring | A | NOT MET | MET | DISAGREE | MET | "checked at boot and on every watcher run", `run-all --dry-run`, origin check before launch |
| E1 collection boundaries | A | NOT MET | MET | DISAGREE | MET | `LOOP_CAP_S` stops starting children; a repository not reached is reported |
| E4 count divergence | A | NOT MET | MET | DISAGREE | MET | Fact 4 reconciles 31 test functions with 42 ledger cases; fact 9 the per-cycle budget of 35 against 65 |
| E5 interaction effects | A | NOT MET | MET | DISAGREE | MET | A dispatcher bug touches every project; PR 686 rewrites six of the same files |

Disagreements re-evaluated: 12. Final verdicts that differ from pass 1: 12 (each re-evaluation ended on pass 2's verdict, so pass 1 totals 20 and 22 became 23 and 23).

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (OURS) | 0.492 | 0.383 | **0.875** | 15.5 points won |
| B (CLAY) | 0.475 | 0.383 | **0.858** | 2.5 points won |

**Margin**: 1.7 points (inside the 5 percent threshold)
**Tiebreaker applied**: Yes, level 1 (debate performance): A won 15.5 of 18 contested points (a split counts half to each side); B won 2.5. Level 2 not needed.

Note on the scores: the two papers are the advocates' own papers and both are strong; the scores measure the papers, not the topologies. The decision rests on the debate matrix, the weighting rule and the invariant probe.

## Selected Base: Variant A (OURS)

### Selection Rationale
A wins the tiebreaker 15.5 to 2.5 on debate points and every high-severity topology point (C-001, C-002, C-003, C-008, X-001). It also meets the owner's weighting rule: CLAY showed clear evidenced benefits only for separable capabilities (C-004 cap, C-005 restart, C-007 settings keys), not for the topology itself. CLAY's own advocate conceded that no part of CLAY's topology still wins.

### Strengths to Preserve from Base
1. Session, branch, worktree and records in each project; Orca registration as the single act that adds a project (REQ R8, R16, R17).
2. One cron entry, one dispatcher, per-repo config, lock, kill switch and day cap (REQ R5).
3. Per-launch origin check (REQ R10, R13).
4. Shared-branch create-once claim files, as a design with a stated limit (acts at push time).

### Strengths to Incorporate from Non-Base Variants
1. From B: per-coordinator in-flight cap with a fail-closed count, with the six safety properties (CLAY rebuttal items 1 to 6), placed inside the child cycle after the sweep (INV-001), with a closing writer and an expiry (INV-002).
2. From B: restart of a dead coordinator that has acknowledged work in flight, guarded: an unreadable session list decides nothing, bounded restarts, resume only for acknowledged work (route.py `end_finished`).
3. From B: per-repo settings keys (merge method, release branch, reviewers, role, safety files), kept in a protected place or overridden by the live GitHub role (INV-011).
4. From B: org-wide search as an optional fail-open pre-check; per-issue exclusive-create state file beside the claim.
5. From B: validation that two repos never share a short name (INV-009).
