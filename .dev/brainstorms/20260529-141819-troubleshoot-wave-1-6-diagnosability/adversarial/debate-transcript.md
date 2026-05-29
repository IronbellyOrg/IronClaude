# Adversarial Debate Transcript

## Metadata

- Depth: standard (Round 1 parallel + Round 2 rebuttal, executed inline by orchestrator after V4 promotion)
- Rounds completed: 2 (Round 3 skipped — convergence on 4/5 disputed axes by end of Round 2)
- Convergence achieved: 0.78 (4 of 5 disputed axes resolved with clear winners; 1 axis — tasklist handoff — converges on hybrid)
- Convergence threshold: 0.75 — MET
- Focus areas: branch count, card filename, contract additions, `--depth deep` interaction, tasklist handoff
- Settled-fork lock: V4 scope/placement/mechanism positions tagged DISQUALIFIED before debate; only V4's 7 additives debated

## Axis 1 — Branch count (3 vs 2)

**Steelman V1 (3 branches)**: Wave 1.5 already has 3 parallel branches with named schemas; adding Wave 1.6 in the same shape costs zero new tax in the protocol's mental model. Branch F (symptom-coverage) is semantically distinct from D and E because it does pure synthesis against the 3 W's of the symptom — neither D (call-density) nor E (config reachability) answers "would the existing instrumentation, if it had fired, have answered the user's question?" That question is the actual sufficiency verdict, not a downstream computation.

**Steelman V3 (2 branches)**: Exception-handler richness lives on the same code surface as logger calls — one auggie query captures both. Adding a third branch for what's already in the result set burns ~500-700 Claude tokens for synthesis with no orthogonal retrieval. The 3 W's synthesis can happen in the orchestrator's post-branch step (no separate Task spawn needed).

**Critique V1 → V3**: Folding symptom-coverage into orchestrator synthesis loses the lazy-loaded ref discipline. If symptom-coverage scoring lives in `SKILL.md` itself rather than a branch agent prompt, it doesn't get the iteration-friendly refinement that branch-agent prompts get. Wave 1.5 deliberately put the per-branch logic in `refs/doc-discovery.md` so tuning happens in one place.

**Critique V3 → V1**: Branch F is not actually a retrieval branch — it's pure synthesis with no MCP call. Calling it a "branch" is a structural-symmetry pun. Real branches reduce wall-clock by parallelizing retrieval; F adds 0 parallelism (it waits for D + E) and adds a Task spawn overhead (~300 tokens).

**Verdict**: V3 wins. **2 branches.** The 3 W's synthesis happens in the orchestrator's post-branch step (mirrors Wave 1.5's Step 4 — the orchestrator synthesizes the Documentation Context Card after branches return). V1's symptom-coverage scoring is preserved as the orchestrator's synthesis logic, documented in `refs/diagnosability-audit.md` Section 4 alongside the sufficiency rubric. Confidence: 78%. (V1 advocate conceded that "Branch F is not actually a retrieval branch" weakens the structural-symmetry argument.)

## Axis 2 — Audit card filename (`diagnosability-audit.md` vs `diagnosability-context.md`)

**Steelman V1**: `diagnosability-audit.md` matches the verb-noun pattern of the wave ("audit"); the card IS the audit's product.

**Steelman V3**: `diagnosability-context.md` parallels `doc-context.md` from Wave 1.5; the card IS the context downstream waves consume.

**Verdict**: V3 wins on naming-symmetry grounds (`doc-context.md` precedent at Wave 1.5 establishes the `*-context.md` pattern for synthesized cards). **`diagnosability-context.md`**. Confidence: 72%. Low-stakes — either is defensible; pick by precedent.

## Axis 3 — Contract field count (3 + enum vs 4)

**Steelman V1 (3 fields + `status` enum extension)**: Adding a new enum value to `status` (`halted_diagnosability`) keeps the contract control-flow signal in one field; downstream consumers that switch on `status` will hit a default branch and inhibit auto-apply (which is the safe default per existing protocol).

**Steelman V3 (4 separate fields, no enum change)**: Extending the `status` enum is a semver-minor change that ripples to every downstream consumer's switch statement. A dedicated `diagnosability_hard_stop: bool` field is purely additive and lets consumers opt-in to caring about the hard-stop signal without touching their `status` handlers.

**Critique V1 → V3**: A `bool` for hard-stop duplicates information that the verdict (`insufficient`) + complexity (which isn't surfaced in V3's contract) implies. The `status` enum is the existing control-flow axis; extending it is the SemVer-correct move.

**Critique V3 → V1**: Adding to the `status` enum forces every downstream consumer that exhaustively switches on `status` to add a case. That's a breaking change to consumers who treated `status` as exhaustive (even though the protocol's contract is "treat unknown statuses as soft-fail"). The `bool` is strictly safer.

**Verdict**: V3 wins on backwards-compat safety. **4 fields: `diagnosability_verdict`, `diagnosability_tasklist_path`, `diagnosability_context_card_path`, `diagnosability_hard_stop`**. No `status` enum extension. Confidence: 70%. (V1 conceded that "forcing exhaustive-switch consumers to add a case is a real cost" weakens the SemVer-purity argument.)

## Axis 4 — `--depth deep` interaction (does NOT force hard-stop vs DOES force hard-stop on insufficient)

**Steelman V1 (does NOT force)**: `--depth deep` is orthogonal to evidence availability. The user invoking `--depth deep` is asserting "I want thoroughness against the available evidence." Forcing instrumentation on a clear NameError just because they typed `--depth deep` is wasteful. The hard-stop is reserved for the "no evidence to be thorough against" case.

**Steelman V3 (DOES force on insufficient)**: `--depth deep` is an explicit user request for thoroughness. If the audit verdict is `insufficient`, the most thorough next step IS to instrument — anything else is hypothesis-against-blind-code, which `--depth deep` should specifically reject.

**Critique V1 → V3**: V3's position couples two orthogonal axes (depth vs evidence). A user might want deep hypothesis exploration with what they have AND not want to be blocked on instrumentation — V3's rule denies that.

**Critique V3 → V1**: V1's position lets `--depth deep` produce a deep wrong answer against insufficient evidence. The whole point of the Wave 1.6 gate is to prevent that.

**Verdict**: V1 wins, but with a V4-inspired refinement. **`--depth deep` does NOT force hard-stop, BUT the soft-warn path becomes mandatory (cannot be suppressed) under `--depth deep`** — if `verdict ∈ {insufficient, partial}`, the tasklist is emitted AND a prominent "your hypothesis depth was constrained by insufficient evidence" banner appears in REPORT.md. This honors V1's orthogonality argument while preventing V3's "deep wrong answer" failure mode. Confidence: 68%. Compromise position synthesized in Round 2.

## Axis 5 — Tasklist handoff (standalone vs standalone + flag)

**Steelman V1 (standalone only, no `--diagnosability-handoff` flag in v1)**: Auto-handoff to task-builder couples Wave 1.6 to Wave 6's MDTM contract, which evolves on its own cadence. Ship the smallest correct thing first. V1.1 can add the flag if user feedback warrants.

**Steelman V3 (standalone + `--diagnosability-handoff` flag)**: The Tier 3 pattern already uses task-builder for fix application — the same machinery should be reusable for instrumentation without forcing the user to manually invoke `task-builder` against the tasklist. The flag is opt-in; default behavior is unchanged.

**Verdict**: V3 wins narrowly because the flag is purely additive and opt-in. **Standalone artifact (always) + `--diagnosability-handoff` opt-in flag that invokes task-builder against the tasklist**. The flag is documented as "advanced; equivalent to running `/task <tasklist-path>` after Wave 1.6 emits." If task-builder's contract changes in a way that breaks the handoff, the flag emits a clear error and falls back to standalone behavior. Confidence: 65%.

## Convergence Assessment

- Points resolved: 4 of 5 disputed axes with clear winners; 1 axis (Axis 4) resolved by Round-2 compromise
- Alignment: 0.78
- Threshold: 0.75
- Status: **CONVERGED**
- Unresolved points: none (all 5 axes have decisions)
- Settled-fork lock applied: V4 scope/placement/mechanism positions were not put to debate; V4's 7 additives were absorbed pre-debate via seed brief update.

## Scoring Matrix

| Diff point | Winner | Confidence | Evidence summary |
|------------|--------|------------|------------------|
| Branch count | V3 (2 branches) | 78% | V1 conceded Branch F is pure synthesis, not retrieval |
| Card filename | V3 (`diagnosability-context.md`) | 72% | Naming-symmetry with `doc-context.md` |
| Contract fields | V3 (4 fields, no enum) | 70% | Backwards-compat safety beats SemVer purity |
| `--depth deep` | V1 + Round-2 compromise | 68% | Orthogonality preserved + soft-warn-mandatory-under-deep refinement |
| Tasklist handoff | V3 (standalone + opt-in flag) | 65% | Additive opt-in beats v1.1-deferred |
| Branch F symptom-coverage logic | V1 (preserved as orchestrator synthesis, not branch) | n/a — graft | Best-of-both: V3's branch count + V1's symptom-coverage analytical content |
| 5-task worked tasklist | V3 | n/a — graft | High-value unique contribution; adopt verbatim shape |
| 7 V4 additives | V4 | n/a — pre-debate | Absorbed via seed brief; merge spec must surface |
