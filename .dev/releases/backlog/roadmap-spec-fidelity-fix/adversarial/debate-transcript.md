# Adversarial Debate Transcript — Spec-Fidelity Fix Ranking

## Metadata
- Depth: standard (2 rounds + invariant probe)
- Rounds completed: 2 + Round 2.5
- Convergence achieved: 92% (17/19 diff points resolved)
- Convergence threshold: 80%
- Focus areas: effectiveness, root-cause-coverage, implementation-risk, combined-synergy
- Advocate count: 6 (each Sx represented by its adversarial-refactor transcript)

## Round 1: Advocate Statements (synthesized from agent-reports/Sx-debate.md)

### S1 Advocate — "Sanitize the source"
- **Position**: Phantom findings cannot be remediated. Stop generating them. Removes 4 of 10 HIGHs at the cheapest point.
- **Steelman of S2**: "S2 is right that remediation needs targets — but routing noise to the roadmap means we'll add `docs/grouping-algorithm` rows to the roadmap that don't exist on disk, which other gates will then flag."
- **Concession**: "I cannot reach 0 HIGHs alone. The 2 legit manifest gaps and 4 NFR soft findings remain."

### S2 Advocate — "Give every finding a target + tell the agent what to do"
- **Position**: `files_affected=[]` is the load-bearing root cause. Even if S1 removes phantoms, the remaining legit HIGHs still can't be remediated. Routing alone isn't enough — `fix_guidance="Address {mismatch_type} in {dimension}"` is useless boilerplate; agents need per-mismatch action templates.
- **Steelman of S1**: "Removing phantoms IS the right first step — without S1 my routing sends agents to edit the roadmap with rows for nonexistent paths."
- **Concession**: "Routing all findings to one file collapses parallelism to a single worker; large patches may still trip the 30% guard. Mitigated by per-patch guard + Phase 2 chunking."

### S3 Advocate — "Tier the diff threshold"
- **Position**: Defensive value for the *71.3% rejection* pattern. Not the right fix for the 15→15→10 pattern.
- **Steelman of S2**: "S2 is correct that the 71.3% diff happened because agents edited the wrong file. Once routing is right, the diff stays small and S3 becomes unnecessary."
- **Self-concession**: "Refactored doc explicitly downgrades me to a defensive-future feature, not a current-failure fix."

### S4 Advocate — "Fix the books"
- **Position**: Math reconciliation: `available=35` is `61 - 46 + 20` (post-credit), not an anomaly. No real budget bug. Only observability and a latent refund rule.
- **Self-concession**: "Standalone confidence 25%. I fix nothing about the failing run."

### S5 Advocate — "Context-aware NFR severity"
- **Position**: `_section_text` joins NFR sections before regex scan, dropping `heading_path`. Refactor `check_nfrs` to iterate per-section; demote NFR-soft findings to MEDIUM unless heading contains strong tokens.
- **Steelman of S6**: "Demoting to MEDIUM is functionally similar to skipping — but it preserves visibility in the report, where S6's allowlist requires opt-in per release."
- **Concession**: "Heuristic is fuzzy; YAML allowlist is the relief valve."

### S6 Advocate — "Halt cleanly with MANUAL_TRIAGE"
- **Position**: Original silent-skip rejected because it inverted PASS semantics. Refactored to a new terminal status `MANUAL_TRIAGE` that still halts the pipeline (`passed=False`) but emits a `manual-triage.md` runbook with operator commands.
- **Steelman of S2**: "S2 is the right fix when findings are remediable. S6 is the right behavior when they aren't — they complement, not compete."
- **Concession**: "Doesn't fix anything; just halts gracefully. Should be paired with S1/S2."

## Round 2: Rebuttals

### S2 → S1
"S1 is necessary but insufficient. With S1 alone, after parser noise is gone, the remaining 6 HIGHs (2 legit manifest gaps + 4 NFR softs) still have `files_affected=[]` and the same 71.3% diff problem recurs. S1 reduces *scope* but doesn't *fix the mechanism*."

### S1 → S2
"S2 has a higher blast radius — it changes the `Finding` dataclass and the agent prompt format. Without S1 ahead of it, S2 routes 4 phantom HIGHs at the roadmap, which the next run will then flag as new defects (you've added rows for files that don't exist on disk)."

### S5 → S2
"S5 and S2 are orthogonal. S2 fixes the *route*; S5 fixes the *classification*. Both required: without S5, the 4 NFR HIGHs persist even after S2 routing because they aren't real roadmap defects."

### S3 → all
"I've already conceded I'm defensive. My place in the ranking is below the three load-bearing fixes."

### S4 → all
"I've already conceded I'm cosmetic. My place is dead last unless paired with a real fix."

### S6 → all
"I'm a complement, not a substitute. Useful as a safety net if S1+S2+S5 doesn't fully converge on the first re-run."

## Convergence Assessment

- Points resolved: 17 of 19
- Alignment: 92% (above 80% threshold)
- Unresolved:
  - X-001 (whether 30% threshold is root cause) — split: S3 says yes, S1/S2 say no. **Resolution**: re-classify as *symptom*. The actual root cause is mis-routing; once corrected, the threshold is appropriate. S3 is preserved as defensive, not promoted.
  - U-003 (S3's deletion-attack defence value) — uncontested but contingent on adopting S3 first; deferred to future work.
- Taxonomy coverage: L1 (style/naming, 1 point), L2 (architecture, 11 points), L3 (state/guards/invariants, 7 points) — all three levels covered.
- Invariant probe gate: 0 HIGH UNADDRESSED → gate clear.
- Status: **CONVERGED**

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| C-001 (parser noise target) | S1 | 95% | Only solution that addresses it at source; unanimous |
| C-002 (NFR soft findings target) | S5 | 92% | Only solution with context-aware severity; orthogonal to S2 |
| C-003 (legit manifest gap target) | S2 | 95% | Only solution that makes them remediable |
| C-004 (agent edits wrong file) | S2 | 90% | Routing is the direct fix; S3 is symptomatic |
| C-005 (actionable fix_guidance) | S2 | 100% | Only solution that touches this; unanimous concession |
| C-006 (escape hatch) | S6 | 85% | Refactored MANUAL_TRIAGE preferred over silent skip |
| C-007 (observability) | tie S3/S4/S6 | 60% | All three add useful telemetry; no overlap |
| C-008 (budget math) | S4 | 75% | Math reconciliation alone; not load-bearing |
| X-001 (threshold = root cause?) | S2 | 88% | S2's "symptom not cause" thesis prevails; S3 self-concedes defensive |
| X-002 (budget too small?) | S4 (refactored) | 100% | S4 falsified its own original premise |
| A-002 (TDD immutable) | unanimous | 100% | All solutions assume this; promoted from UNSTATED to STATED |
