# Adjudication result: slot C-11 (rfqa-first-step-and-readonly-scope)

Run: `/sc:adversarial --compare proposal-a.md,proposal-b.md --depth standard --focus correctness,risk,test-coverage` (Mode A, no `--merge`, no `--interactive`). Orchestrated by the debate-orchestrator; the diff analyst, advocates, fault-finder, scorers, plan reviewer and merge-executor were separate agents.

## Winner

**Variant B (Proposal B) as the base, merged as the hybrid the debate itself produced: a lens-level first change.** The debate's own base selection (`base-selection.md`): "Selected Base: Variant B (Proposal B; `variant-2-original.md`)". The merged resolution is `merged-output.md`. Neither proposal won as written: after two rounds both advocates named the same outcome label on all 30 diff points (Variant B 9, Variant A 3, Hybrid 18, Neither 0). The hybrid shape (C-001, hybrid 88%, the same text in both Round 2 tables): the first rf-qa change adds one new read-only lens-reviewer agent definition and a replay oracle; no panel engine (`resolve`/`merge`/`ledger`) is wired into any rf-qa gate. Its only gate edit is conditional: the standard lens dimensions at `/task` steps 3-4 switch to the new agent only if arm 1a meets the pre-registered rule before merge AND the owner answers Q3 yes; otherwise `task/SKILL.md` stays byte-identical.

## Rationale (quoted from the debate's base selection and scores)

- Quantitative layer: A 0.9284, B 1.0000 (requirement coverage A 0.7692 [10 of 13], B 1.0 [13 of 13]; internal consistency A 0.9906, B 1.0; specificity 1.0 each; dependency completeness 1.0 each; section coverage 1.0 each).
- Qualitative layer (30 criteria, two position-bias passes, 1 of 60 pairs re-evaluated): A 25/30 = 0.8333, B 25/30 = 0.8333. Dimensions: Completeness A 5/5, B 4/5; Correctness 3/5 each; Structure A 4/5, B 5/5; Clarity 4/5 each; Risk Coverage 4/5 each; Invariant & Edge Case 5/5 each. Both clear the edge-case floor.
- Combined: A 0.8809, B 0.9167. "Margin: 3.58% (below the 5% threshold)". "Tiebreaker applied: Yes, level 1 (debate performance). Variant B won 9 diff points outright against 3 for Variant A".
- The debate's stated reasons: the quantitative layer favours B and the qualitative layer ties. A's Correctness losses are code-checked (the packaged-templates count, A:28 says 8 and A:115 lists 9; the "one place / every lens reviewer of every phase gate" overreach, X-001, conceded by Advocate A). B's Correctness losses are also code-checked and conceded (the "schema change over all 8 packaged templates" claim, X-002; the install-list claim, A-006; a document-gate module with no host skill).
- What each side gave up in Round 2: Advocate A withdrew the per-slot `lens` key, the checklist completion predicate and the floor parameter, and agreed that Q3 goes to the owner (C-003, C-004, C-011 to B). Advocate B conceded that clause B-3 is refuted by its own M-B1 rule (the issue-331 Gate C overwrite, N1: a report-only lens overwrote another lens's report; verified by both advocates) and that the document-gate module leaves the first change.
- Convergence: 25 of 30 diff points agreed at text level (83.3%) against an 80% threshold; 30 of 30 on outcome label. Status BLOCKED_BY_INVARIANTS (see unaddressed invariants below). Round 1 outcome-label agreement was 16 of 30 (53.3%, upper bound).

## Conditions under which the winner holds (all stated in `merged-output.md`)

1. The switch at `/task` steps 3-4 lands only if arm 1a passes the pre-registered rule for a standard lens dimension before merge AND the owner answers Q3 yes. The pre-registered repeat count, variance bound and decision rule do not exist yet.
2. The debate rests on structure and on one audit finding, not on measured recall: no behavioural oracle exists for rf-qa (decided fact), whether Read/Grep/Glob reviewers match the recall of reviewers with Bash is "unmeasured", and the full M-B1 audit has not run. The transcript pilot covers one machine of unknown retention; N1 is one event; its damage count (2 or 3 blocking findings) is unsettled; the advocates' counts differ (366 raw, 278 after the skip rule, 571 non-fix; 118 versus 107 standard-lens-named).
3. The only observed class-(b) event occurred at a task-file gate item of a non-standard lens that the switch does not reach, and no standard-lens spawn through `/task` steps 3-4 was observed (N2, NB2: a B amendment, not answered by A).
4. No gate engine swap in the first change. Any later swap waits for the M-B4 anchor probe (C-01 trigger T-a), the C-03 floor-owner answer and C-02's `next`/`--resolution` caller rules, and runs in shadow with rf-qa as authority until a replay says otherwise.
5. Skill-embedded and task-file gate items, executing lenses and verifiers keep their agent in the first change; the exclusion scope itself is one of the five unresolved points.
6. Five points carry the same label but contradicting hybrid texts and are not decided: C-002, C-006, C-008, A-004 (does the step-8 verification pair switch with the standard lenses; is the exclusion scope "domain lenses" or "every lens or verifier that runs tests or mutates scratch copies") and A-001 (runtime write-probe as a test or as a recorded run). Advocate B spoke last and Round 3 does not exist at depth standard, so Advocate A never answered B's amendments (lens-identity blocker, the wider mutator list, the scoring-script pytest, the audit additions, the no-clobber check for skill-embedded gates).
7. The default does not satisfy INV-G for the skill-embedded and task-file gate items where N1 occurred, nor for executing lenses and verifiers.

## Invariants the debate left unaddressed

From `adversarial/invariant-probe.md` and the return contract: 18 findings, 2 ADDRESSED, 16 UNADDRESSED. Convergence was blocked by the six HIGH items; standard depth has no Round 3, so none was resolved.

| ID | Severity | Category | What is unaddressed |
|----|----------|----------|---------------------|
| INV-002 | HIGH | guard_conditions | The lens-identity check is undefined when a report's first line names no lens (across 517 reflect-reviewer returns only 37 start with the mandated heading); identity is self-declared. |
| INV-009 | HIGH | collection_boundaries | "The dispatched slot's path" is not unique for partition instances of one lens (`task/SKILL.md:264, 273-275`); no slot id exists in `/task` once the per-slot key was withdrawn, so the executor can recreate N1's overwrite. |
| INV-012 | HIGH | interaction_effects | The hash and lens-line checks sit in step 10, which runs after consolidation (6), fix (7), verification (8) and the proceed decision (9). |
| INV-015 | HIGH | sufficiency_challenge | The sha256 is taken over the executor's own write, proving later non-clobber, not equality with the returned text; return volume (p90 about 12 KB, max about 46 KB) and the returned-but-not-yet-written window are not handled. |
| INV-016 | HIGH | sufficiency_challenge | Arm 0 and arm 1a differ in more than the tool list: content lenses run `rf-qa-qualitative` (another body) in arm 0, and "zero-trust section" exists in `rf-qa.md` only inside the fix-cycle section the consensus drops (`rf-qa.md:418`). |
| INV-017 | HIGH | sufficiency_challenge | Pre-computed counts exist in the oracle but no changed gate step adds a pre-computation step at a production gate; single-document seeds cannot exercise the multi-file or partitioned checks. |
| INV-001 | MEDIUM | state_variables | The oracle's parent permission mode, installed hook set and model alias are not pre-registered, so arm 0 may not behave like production arm 0. |
| INV-003 | MEDIUM | guard_conditions | The tree-hash scope is unspecified: excluding `qa/` blinds it to N1's class; git state (the shared stash) and `/tmp` scratch are not covered. |
| INV-004 | MEDIUM | guard_conditions | The subset guard checks the source file; runtime resolves project `.claude/agents/` then `~/.claude/agents/` (`verify-sync` does not cover the installed copy); the reflect guard parses only the inline `tools:` form while `rf-qa.md` uses the YAML-list form. |
| INV-007 | MEDIUM | count_divergence | "The standard eight lens dimensions" does not map one-to-one onto what a gate spawns (floors 3+3 to 6+6; extra lenses at the 10 and 12 tiers); eight per-dimension pass decisions with no multiplicity control. |
| INV-008 | MEDIUM | count_divergence | The audit misses nested spawns (a lens that spawned a write-capable child), renamed tool names, and its counts are regex-dependent and already differ between advocates. |
| INV-010 | MEDIUM | collection_boundaries | The Confidence Gate formula is undefined at TOTAL = UNVERIFIABLE and rewards capability loss (1 verified item of 6 scores 100%); no production cap on the UNVERIFIABLE share. |
| INV-013 | MEDIUM | interaction_effects | `test_c_s1_s3_copied_verbatim` iterates a fixed 10-file tuple and does not reach a new agent file; an `rf-`-named file triggers the Tavily parity tests. |
| INV-014 | MEDIUM | interaction_effects | The `rf-qa.md` body and the installed SubagentStart hook tell agents to write their output file, which pushes a read-only agent to write or to return only a pointer. |
| INV-018 | MEDIUM | sufficiency_challenge | The conditional switch does not name the other spawn sites in `task/SKILL.md` (`:307`, `:320`, `:365` and others), and the step-8 verifier protocol lives in the fix-cycle section the consensus drops. |
| INV-006 | LOW | guard_conditions | The reflect-reviewer allowlist refused 7 calls across 517 runs, not 2 (including `codegraph_explore`); no rule for adding read-only tools as names change. |

ADDRESSED: INV-005 (LOW; the mutator set contains the spawn and message tools, confirmed as a real exposure) and INV-011 (LOW; an empty corpus gives no verdict).

Return contract `unaddressed_invariants` (HIGH only): INV-002, INV-009, INV-012, INV-015, INV-016, INV-017.

## Return contract

Status `partial`; convergence score 0.83 (25 of 30 = 0.8333); base variant `variant-2 (Proposal B; default model, default persona)`; unresolved conflicts 5 (C-002, C-006, C-008, A-001, A-004); fallback mode false; failure stage null; invocation method `task-agent`.

## Artifact paths

Output folder: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/rfqa-first-step-and-readonly-scope/`

- Merged file: `.../rfqa-first-step-and-readonly-scope/merged-output.md`
- Artifacts folder `.../rfqa-first-step-and-readonly-scope/adversarial/`:
  - `variant-1-original.md`, `variant-2-original.md` (variant copies)
  - `diff-analysis.md`
  - `debate-transcript.md` (with `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`)
  - `invariant-probe.md` (with `round2.5-fault-finder-raw.md`)
  - `base-selection.md` (with `score-pass1.md`, `score-pass2.md`, `score-reeval.md`, `quant-score.py`, `quant-score-output.json`)
  - `refactor-plan.md` (with `plan-review.md`)
  - `merge-log.md`
  - `return-contract.yaml`
