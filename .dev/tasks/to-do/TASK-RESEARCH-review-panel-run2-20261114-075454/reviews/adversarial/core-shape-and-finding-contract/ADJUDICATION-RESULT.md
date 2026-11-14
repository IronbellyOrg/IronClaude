# Adjudication Result: slot C-01 (core-shape-and-finding-contract)

Run: `/sc:adversarial --compare proposal-a.md,proposal-b.md --depth standard --focus correctness,risk,test-coverage`, Mode A, 2 variants, 2 advocates (opus), one independent fault-finder, two independent qualitative scorers. Code state: HEAD 50d4d2b9d.
Protocol status: `partial`. Convergence score: 1.0 (23 of 23 points agreed after Round 2; 18 of 23 after Round 1). Debate status: `BLOCKED_BY_INVARIANTS` (one HIGH UNADDRESSED invariant, INV-003).

## Winner

A named hybrid that the debate itself produced, with Variant B as the selected base (`base-selection.md`: "Selected Base: Variant B"). In short: a thin shared contract now with per-module engines (Variant B's shape), plus the one engine-local change taken from Variant A: surface the anchor status of each blocking row in the per-row `### Lx` block that `render_merged_report` prints. Neither original proposal won as written.

What the hybrid contains, as both advocates left it after Round 2 (`merged-core-shape-and-finding-contract.md`):
- Shared now: finding id grammar `_ID`; one limits-constants module imported by both parsers; one repair step called from inside both `parse_block` functions (policy decided in C-06); the shared `refs_norm` token list with `T<PP>.<TT>` added once; hash and identity helpers.
- Engines per module: spec loop stays on v1 `findings.py`, `ledger.py`, `review-ledger/1` and v1 clustering; reflect stays on the v2 kernel; no change to `cli/reflect`.
- Withdrawn from Variant A: locator-agnostic `annotate`, `citations` in ledger rows, the clustering marker, the typed re-review line kind, `cluster_v2` for new ledgers. Withdrawn from Variant B: the typed `LedgerError` guard, the projection view, "closed at the PR adapter".
- Unknown keys open in both parsers; ledger passthrough keys deferred; `prior` lines unchanged (semantics to C-02); clearing that ignores block validity, and how an unlocated row may clear, routed to C-02 and C-03.
- Convergence to one engine only on a trigger: T-a (a module needs re-review rounds over citation-located findings from several reviewers), T-b (the pre-registered measurement shows citations resolve at least as often as anchors locate on documents), T-c (a verified defect fix needs a non-helper edit to both parsers or both clusterers), with the precondition that `same_defect_v2` first gets an anchor-span branch or a `spec`-role citation is derived from the located anchor span.

## Rationale (the debate's own base selection and scores)

Quoted from `adversarial/base-selection.md`:
- Quantitative layer: Variant A 0.985, Variant B 0.936.
- Qualitative layer (two independent passes, five disagreements re-evaluated): Variant A 23/30 = 0.767, Variant B 23/30 = 0.767. Dimension subtotals A / B: Completeness 5 / 4, Correctness 1 / 3, Structure 5 / 5, Clarity 3 / 3, Risk Coverage 4 / 3, Invariant & Edge Case Coverage 5 / 5.
- Combined: Variant A 0.8760, Variant B 0.8515. "Margin: 2.45 percent (below the 5 percent threshold)". "Tiebreaker applied: Yes, level 1 (debate performance, points won in Step 2)": Variant B won 10 of the 23 points, Variant A 2, HYBRID 7, NEITHER 4. Variant B selected as base. Sensitivity check recorded in the same file: with every position-bias disagreement resolved to Pass 2, A 0.8926 and B 0.8515 (margin 4.1 percent, still below 5 percent); the selection is unchanged.
- Selection rationale in the debate's words: the debate moved toward B's shape after both advocates verified in code that a citation-only line is rejected by `findings.py:104` before it can reach `annotate`, and that `cluster_v2` cannot cluster anchor-only findings (`cluster.py:128-181`, `test_review_cluster.py:279-293`). Variant A's Correctness score (1 of 5) reflects those two points; Variant B's lower Completeness (no FX-2 answer, no CL-X11 placement) and Risk Coverage are carried into the plan as items to take from Variant A.

## Conditions under which the winner holds

As recorded in the debate (Round 2 hybrids of both advocates, `merged-core-shape-and-finding-contract.md` sections 2.3, 5.4, 5.5):
1. The convergence triggers T-a, T-b, T-c have not fired. If one fires, the debate's recorded path is Variant A's one-engine design, after the anchor-span precondition above.
2. The pre-registered location-reliability measurement (merged T3 and 5.3) is run only after the snapshot plumbing is fixed and after the open question A-002 (how line numbers reach reviewers) is stated.
3. Tests: T1 (all existing pins pass unmodified, with `test_review_cluster.py:279-293` and `test_rendered_merged_report` added), merged T2 and 5.1, merged T3 and 5.3, rewritten T4 and 5.2 (pin today's rejection of a citation-only line, one reviewer and several reviewers), rewritten T5 (`span None` row, status surfaced, `ESCALATE` at the cap).
4. Anchor status is surfaced in the per-row `### Lx` block of `## Blocking findings`, not in the reviser-brief id line pinned by `test_review_ledger.py:459-467`, and without a prompt-file change.
5. The shared repair step must not invent an anchor for a citation-only line, and its policy belongs to C-06. The debate did not show that a rescuing policy and "T1: every pin unmodified" can both hold (INV-003 below).
6. Two disputes between the advocates were not reconciled and are recorded in the merged document: whether the locator policy is data with `on_missing`/`on_ambiguous` (advocate A) or hard-coded keep-and-surface (advocate B), and whether the next round is also asked to "say it is gone" (advocate A) or only to re-locate the row (advocate B).
7. Clearing rules (clearing ignores block validity; how an unlocated row may clear) are decided in C-02 and C-03, not here.

## Invariants the debate left unaddressed

From `adversarial/invariant-probe.md` (25 findings: 9 ADDRESSED, 16 UNADDRESSED; HIGH 1, MEDIUM 14, LOW 1) and `adversarial/return-contract.yaml` (`unaddressed_invariants`: INV-003). The debate ran at depth standard (no Round 3) and did not resolve any of them.

| ID | Severity | Category | Assumption left unaddressed |
|----|----------|----------|-----------------------------|
| INV-003 | HIGH | guard_conditions | A repair step inside both `parse_block` functions can rescue over-limit lines while T1 keeps every existing pin unmodified (`tests/review/test_review_findings.py:113` and `:117` pin `ok` False for an anchor of 201 and a claim of 301 characters; the orchestrator re-read confirmed). Blocks convergence. |
| INV-001 | MEDIUM | state_variables | Anchor status can be surfaced for every blocking row from data `render_merged_report` already has (the row stores neither flag) |
| INV-002 | MEDIUM | state_variables | Adding `T<PP>.<TT>` to the shared token list leaves ledgers already on disk behaving the same |
| INV-004 | MEDIUM | guard_conditions | The same repair gives the same benefit in the v2 parser (any error invalidates the whole v2 block) |
| INV-009 | MEDIUM | count_divergence | The 3-line clustering tolerance means the same thing in both engines (0-based half-open versus 1-based inclusive) |
| INV-010 | MEDIUM | count_divergence | The two parsers hold the only copies of the limits and the one repair is the only repair (`card_convert.py` has a third copy and its own truncation) |
| INV-014 | MEDIUM | collection_boundaries | A round whose only reviewer has only a repaired line merges like any other round |
| INV-015 | MEDIUM | collection_boundaries | A stuck row is one row, so surfacing its status once is enough (empty refs open a new span-less row each round) |
| INV-016 | MEDIUM | interaction_effects | The merged T2 gate catches every shared-contract change (a `refs_norm` change passes a parser-output gate but changes fingerprints) |
| INV-017 | MEDIUM | interaction_effects | Adding the token once in `refs_norm` updates every reference-token reader (`telemetry.py` keeps its own copy) |
| INV-018 | MEDIUM | interaction_effects | Shared helpers can move into a new module without touching pinned tests (`test_module_does_not_import_v1_cluster`) |
| INV-020 | MEDIUM | interaction_effects | "No change to `cli/reflect`" means the reflect pipeline's results do not change (shadow steps call the v2 parser and `refs_norm`) |
| INV-021 | MEDIUM | interaction_effects | The merged T2 has committed v1 ledger fixtures to replay |
| INV-022 | MEDIUM | interaction_effects | Whatever repair policy C-06 picks leaves locating and clustering of the rescued line well defined |
| INV-024 | MEDIUM | sufficiency_challenge | The consensus alone resolves FX-1 and leaves C-06 free to choose the repair policy (the repair reaches 2 of 3 validation paths) |
| INV-008 | LOW | count_divergence | One constant per limit is safe when equal numbers mean different things; the literal list is complete (omits `findings_v2.py:128`) |

## Artifact paths

Output folder: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/core-shape-and-finding-contract/`
- Merged file: `merged-core-shape-and-finding-contract.md`
- `adversarial/variant-1-original.md`, `adversarial/variant-2-original.md`
- `adversarial/diff-analysis.md`
- `adversarial/debate-transcript.md` (embeds `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`, which are also kept as files)
- `adversarial/invariant-probe.md`
- `adversarial/scorer-pass1.md`, `adversarial/scorer-pass2.md` (position-bias passes)
- `adversarial/base-selection.md`
- `adversarial/refactor-plan.md`
- `adversarial/merge-log.md` (11 of 11 changes applied; post-merge validation PASS)
- `adversarial/return-contract.yaml` (`status: partial`, `convergence_score: 1.0`, `base_variant`: Variant B)
