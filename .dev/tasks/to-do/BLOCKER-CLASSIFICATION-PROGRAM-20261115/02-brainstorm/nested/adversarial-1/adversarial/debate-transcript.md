# Adversarial Debate Transcript

## Metadata

- Mode: B (generate from `seed-brief.md`, 3 agents), unattended
- Depth: standard (Round 1, Round 2, Round 2.5; no Round 3)
- Rounds completed: 2, plus the Round 2.5 invariant probe
- Convergence achieved (majority rule, 2 of 3 advocates): 100 percent in Round 2 (61 of 61 points); 90.2 percent in Round 1 (55 of 61)
- Unanimous points in Round 2: 52 of 61; majority-only points: 9
- Convergence threshold: 75 percent (`--convergence 0.75`)
- Focus areas: all
- Advocate count: 3 (Variant 1 opus architect, Variant 2 sonnet analyzer, Variant 3 haiku backend)
- Taxonomy coverage: L1 3 points, L2 29, L3 29 (all three levels covered, so the coverage gate passes)
- Full statements are kept in the files linked below (one file per advocate per round), not copied here, so that no statement is rewritten: `debate/round1-advocate-1-opus-architect.md`, `debate/round1-advocate-2-sonnet-analyzer.md`, `debate/round1-advocate-3-haiku-backend.md`, `debate/round2-advocate-1-opus-architect.md`, `debate/round2-advocate-2-sonnet-analyzer.md`, `debate/round2-advocate-3-haiku-backend.md`. Per-point tracking: `debate/convergence-tracking.tsv`.

## Round 1: Advocate Statements

Each advocate followed the steelman protocol, answered every shared assumption (A-001 to A-014; no omissions found), and filled a point table for all 61 diff points.

### Variant 1 advocate (opus, architect)

Position: the shared rule belongs in a delegate-only skill folder, because that location alone gets the installed copy, the project `.claude/` copy and the drift check with no new tooling; copies keep a short fenced digest that a registry-driven drift test compares word for word; new gates, judges and severity scales are one registry row. Conceded the four false claims the diff analysis listed against Variant 1 (the 81-file count, the plugin-build claim, the two table-defect examples, "monotone in every input"), plus X-006, X-007, X-009, X-010, X-011, C-014, C-017 and C-021.

### Variant 2 advocate (sonnet, analyzer)

Position: only Variant 2 explains why the rule over-blocks (six causes, of which the wording is one: the "highest severity wins" merge rule, no mechanical check of the fix pass, no consumer line for upstream gates), and only it makes the guardrails testable (blind audit, seeded-defect recall, Wilson-interval revert triggers). Conceded that "UNSET means send to a person" is false for S and D, that UNDETERMINED is not a sketch outcome, that its test-module count was incomplete, and that "highest severity" is in `tech-reference`, not task-builder or tech-research.

### Variant 3 advocate (haiku, backend)

Position: Variant 3 best protects stable finding identity, capture integrity, repeat-safe imports, one-issue batch filing bound to the user's approval, and fail-safe classifier handling (a missing safety answer never authorizes a downgrade). Conceded Variant 1's delivery scaffolding and run-level offers, Variant 2's causal analysis and audits, and its own development-surface (`.claude/REVIEW-SEVERITY.md` does not exist today), fallback and inventory gaps.

## Round 2: Rebuttals

Sequential: advocate 1, then 2 (saw 1), then 3 (saw 1 and 2).

### Variant 1 advocate

Moved to Variant 2 on rollout order (S-009) and on question count (C-012); moved to Variant 3 on unknown consequence (X-003), ledger path (C-009, because the pr-submit ledger path is gitignored at `.gitignore:250` and `WORKER-CONTRACT.md:34` keeps gitignored paths out of `artifacts`) and offer consent (C-006). Held on rule location (X-001) and inline digest plus pointer (X-002), since the plugin tree has no `pragmatic` hook match. Found a third "highest severity wins" line at `task/SKILL.md:361`.

### Variant 2 advocate

Moved to Variant 3 on S-006, C-006, C-007, C-009, C-010, X-005, X-006, X-012; to Variant 1 on S-008, X-002. Retracted two of its own claims (highest severity in task-builder and tech-research; "WC-4 allows extra keys"). New checks: five Python files split table rows on a bare pipe; the S, M or C UNSET fix changes 336 of 4,096 sketch states; final gates exist at `task/SKILL.md:290` and `tech-research/SKILL.md:415`.

### Variant 3 advocate

Changed toward Variant 1's CLI boundary, registry-driven tests and explicit scale inventory, and toward Variant 2's explanation order, named-consumer evidence and old-rule shadow rollout; trimmed its own ledger machinery and worker fields; found more missed "highest severity" merges.

### Convergent proposal (all three)

One delegate-only skill (`sc-review-severity`) holding the rule, with a versioned inline digest in each carrier plus a pointer, tracked by a registry; unknown or UNSET inputs never demote; V3's ledger with stable identity and escaping; six decisive classifier questions; Variant 2's measured guardrails (blind audit, seeded defects, interval-bounded revert triggers); rollout as measure, scaffold, shadow beside the old rule, pilot, propagate; classifier authority is a separate owner decision, not a rollout stage.

## Round 2.5: Invariant Probe

See `invariant-probe.md`: 38 findings (14 ADDRESSED, 24 UNADDRESSED; UNADDRESSED: 9 HIGH, 13 MEDIUM, 2 LOW). The fault-finder also flagged conformity on 5 consensus points (C-017, A-006, C-010, X-003, S-009): agreed in the vote, but the content differs or the reason was not checked. It judged the 61 of 61 majority weak evidence (three voters with three options almost always give a majority), and named real, checked convergence on four items: six questions, the UNSET lift, installers skipping existing files, and the skill-folder location.

## Scoring Matrix

Winner per point from the Round 2 point tables; confidence is the mean of the agreeing advocates' stated confidence, plus 5 points when unanimous and minus 5 when majority-only, capped at 99 (never 100); evidence is the highest-confidence agreeing advocate's cell, truncated. Summary: points 61; unanimous 52; majority (2 of 3) 9; levels {'L2': 29, 'L3': 29, 'L1': 3}; winners {'V2': 19, 'V3': 19, 'V1': 9}.

| Diff point | Level | Winner or verdict | Confidence | Agreement | Evidence summary |
|---|---|---|---|---|---|
| A-001 | L2 | QUALIFY | 87% | unanimous | P:221 carries reviewer guidance outside the exact-definition sentence, so exact-copy counts do not establish coverage. |
| A-002 | L3 | QUALIFY | 86% | unanimous | Missing basis cannot establish harmlessness; the intermediate deferral needs a real final consumer of its ledger. |
| A-003 | L3 | ACCEPT | 95% | unanimous | `CANONICAL_CAP_TEXT` pinned (L5). |
| A-004 | L3 | QUALIFY | 84% | unanimous | W:39 makes the coordinator open the contract; ledger counts and capture status need explicit consumption too. |
| A-005 | L2 | QUALIFY | 89% | unanimous | Seed brief: inventory was empty; stage 3 needs 0b plus shadow runs if the table is late. |
| A-006 | L3 | QUALIFY | 88% | unanimous | NEW-1 is a pipe defect; N1 gives the convention and its reader limits. |
| A-007 | L2 | QUALIFY | 86% | unanimous | N7: no plugin hook match. |
| A-008 | L3 | QUALIFY | 75% | unanimous | Machine-readable extractors remain UNVERIFIED; absent inputs stay missing rather than inferred negative. |
| A-009 | L3 | REJECT | 94% | unanimous | Sketch `ORDER` has no UNDETERMINED. |
| A-010 | L2 | ACCEPT | 94% | unanimous | `pragmatic.md:228` exemption. |
| A-011 | L2 | ACCEPT | 80% | 2 of 3 | No key, no call; shadow with fixtures or approved judges only. |
| A-012 | L3 | QUALIFY | 84% | unanimous | T:256 excludes minor rechecks; a changed consequential finding needs linked escalation, not permanent immunity. |
| A-013 | L2 | QUALIFY | 86% | unanimous | Changed: I:25 is explicit-only, while W:23 forbids issue workers; generic consent does not silently remove invocation constraints. |
| A-014 | L3 | REJECT | 88% | unanimous | `install_core.py:70` and `install_skills.py:102` skip existing files unless forced (L9). |
| C-001 | L3 | V2 | 78% | unanimous | Changed: named consumer plus stated-reason test is more checkable; retain V3's required-behavior and acceptance-check wording. |
| C-002 | L3 | V3 | 80% | unanimous | V3:60-66 requires affected-action evidence and refuses to turn unverified protected risk into notes. |
| C-003 | L1 | V2 | 67% | unanimous | Changed: retain native Medium in prose and FOLLOW_UP internally, avoiding terminology churn without equating scales. |
| C-004 | L3 | V2 | 78% | unanimous | Changed: rests_on supplies a checkable consumer; retain V3's separate explanation of all blocking conditions. |
| C-005 | L2 | V1 | 87% | unanimous | Per-carrier stage/version registry plus reverse scan exposes missing copies rather than hiding them behind fallback. |
| C-006 | L2 | V3 | 68% | unanimous | Selected IDs and snapshot digest bind an actual answer to the offered set; notes remain opt-in. |
| C-007 | L3 | V3 | 67% | 2 of 3 | G:9 proves fixes can introduce defects; independent authorized work must retain ordinary validation. |
| C-008 | L3 | V3 | 89% | unanimous | Identity tuple, revision, atomic replace beat location plus hash (Q7). |
| C-009 | L2 | V3 | 69% | unanimous | One caller-fixed run path and nested references fit W:24-25; existing implement and PR records remain exceptions. |
| C-010 | L2 | V3 | 68% | unanimous | Visible capture failure is essential; N3 justifies reducing six fields to three explicit contract additions. |
| C-011 | L3 | V3 | 90% | unanimous | `/sc:issue` posts with no dry-run (V-26). |
| C-012 | L2 | V2 | 89% | unanimous | K:35 has six decisive inputs; four explanatory questions have no demonstrated gating benefit. |
| C-013 | L3 | V2 | 81% | unanimous | Reviewer-named, code-checked basis is strongest; N2 prevents assuming existing gates consume the ledger. |
| C-014 | L3 | V3 | 89% | unanimous | K:44-46 lifts U safety only; missing-answer policy must be an intentional correction, not a description of the sketch. |
| C-015 | L3 | V3 | 73% | unanimous | V3:365-379 bounds retries and versions caches; budgets remain proposed, not measured service guarantees. |
| C-016 | L3 | V2 | 82% | unanimous | Blind audit, seeded recall and final sweep are strongest; add all protected-risk disputes and N6's sampling correction. |
| C-017 | L3 | V2 | 94% | unanimous | Replace label-max merging and add fix checks; N5 finds semantic equivalents beyond T:252,361 and RF:513. |
| C-018 | L2 | V1 | 63% | unanimous | Changed: explicit scale inventory and tests beat an implicit boundary list; retain V3's separate adapter approvals. |
| C-019 | L2 | V3 | 60% | 2 of 3 | E:27 confirms 139 matches versus 120 lines; widen integration inventory with the N5 merge sites. |
| C-020 | L2 | V1 | 57% | 2 of 3 | Changed: V1 adds R/tests/review/test_review_rules_text.py:92; combine V3's transitive import at R/tests/audit/test_invariant_preservation_NFR_6_through_10.py:95-101. |
| C-021 | L2 | V2 | 93% | unanimous | File times give about 22 minutes, not 25. |
| C-022 | L3 | V3 | 74% | unanimous | Pin loop versions and expose stale consumers; R/src/superclaude/cli/install_skills.py:102-104 skips existing skills. |
| S-001 | L2 | V2 | 57% | 2 of 3 | Changed: causes and examples explain why delivery and operational contracts are needed, rather than starting from machinery. |
| S-002 | L1 | V2 | 83% | unanimous | Per-statement evidence labels remain best, but A2's retractions show labels still need verification. |
| S-003 | L2 | V2 | 95% | unanimous | RC2 is wider than I said: three lines (N5). |
| S-004 | L2 | V2 | 89% | unanimous | 14 graded cases; only V2 applies the rule to real Gate 1 rows. |
| S-005 | L2 | V1 | 92% | unanimous | R/Makefile:112-125,178 provides skill delivery and whole-folder drift checking without core-sync work. |
| S-006 | L2 | V3 | 67% | unanimous | Identity, observation receipts and batch states remain necessary; conditional tables remove needless empty structure. |
| S-007 | L2 | V1 | 80% | unanimous | Changed: the existing review CLI at R/src/superclaude/cli/review/__init__.py:14 fixes the installed boundary without dictating every module. |
| S-008 | L2 | V1 | 64% | unanimous | Accept the narrowed paragraph documenting existing boundaries, not speculative extension code. |
| S-009 | L2 | V2 | 75% | unanimous | Changed: V2:558 gathers rests_on while the old rule decides; V3's offline stage must precede it. |
| S-010 | L2 | V1 | 66% | unanimous | Changed: registry-driven coverage supplies a stronger test skeleton; retain V3's crash and consent cases. |
| S-011 | L2 | V2 | 89% | unanimous | RT2 Wilson lower bound is the only trigger testable at n = 60. |
| S-012 | L1 | V2 | 49% | 2 of 3 | Evidence column per risk; V3's required responses grafted. |
| X-001 | L2 | V1 | 93% | unanimous | Existing skill sync avoids V3's proposed but ungenerated core development surface. |
| X-002 | L2 | V1 | 80% | unanimous | Inline fenced digest delivers grading instructions even when the detail pointer is unread. |
| X-003 | L3 | V3 | 66% | 2 of 3 | Missing consequence never proves harmlessness; section 4 permits only an explicitly authorized intermediate deferral. |
| X-004 | L3 | V2 | 71% | unanimous | Changed: once per run plus a useful existing escalation avoids both per-loop noise and delaying an already needed decision. |
| X-005 | L3 | V3 | 77% | unanimous | V3:552 separates authority from propagation; both opponents now withdraw automatic stage-based authority. |
| X-006 | L3 | V3 | 82% | unanimous | `jev-uses.md:194`: the min is an upper bound. |
| X-007 | L3 | V3 | 95% | unanimous | Sketch line 44 lifts U, not UNSET (N4). |
| X-008 | L3 | V2 | 88% | unanimous | K:67-69 excludes UNSET comparisons; answered monotonicity and missing-input invariants need separate tests. |
| X-009 | L3 | V3 | 90% | unanimous | V3:365-366 applies approval to every external judge, including fallback models. |
| X-010 | L2 | V2 | 91% | unanimous | `stat` times and the PASS at review 3. |
| X-011 | L3 | V2 | 90% | unanimous | Destination cell wrong (`gate1-cycle-control.md:9`). |
| X-012 | L3 | V3 | 65% | 2 of 3 | Unsettled rows must be persisted but counted separately from confirmed non-blockers and excluded from their offer set. |
| X-013 | L2 | V3 | 57% | 2 of 3 | Preserve the warning that an eight-module inventory is incomplete; both additional pins must join the union. |

## Convergence Assessment

- Points resolved: 61 of 61 (52 unanimous, 9 by 2 of 3)
- Alignment: 100 percent by the majority rule (Round 1: 90.2 percent); the conformity caveat above means this number overstates independent agreement
- Threshold: 75 percent
- Taxonomy gate: passed (L1, L2, L3 all covered)
- Invariant gate: BLOCKED_BY_INVARIANTS (9 HIGH UNADDRESSED: INV-001, INV-007, INV-008, INV-009, INV-015, INV-023, INV-026, INV-027, INV-034). Standard depth has no Round 3, and the run is unattended, so these are not re-debated; each becomes an explicit requirement or owner decision in the refactoring plan (Step 4) and is re-checked against the merged output (Step 5). Any item not resolved there is listed in the return contract as `unaddressed_invariants`.
- Status: CONVERGED on the diff points, BLOCKED_BY_INVARIANTS pending the merge check
- Unresolved points: none by vote; the 5 conformity points are carried into the plan for a stated reason each
