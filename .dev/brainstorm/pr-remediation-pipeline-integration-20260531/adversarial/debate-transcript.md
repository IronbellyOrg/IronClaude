# Adversarial Debate Transcript — BRV-MG A vs B

## Metadata
- Depth: standard (Round 1 + Round 2 + Round 2.5 invariant probe; Round 3 skipped — convergence met)
- Rounds completed: 2.5
- Convergence achieved: 0.84 (16 of 19 diff points resolved; X-001 architectural contradiction adjudicated; 3 minor edge cases left to merged-proposal trade-offs)
- Convergence threshold: 0.80
- Focus areas: architectural-coherence, OVM-composition, GitHub-platform-fit, layer-separation, falsifier-strength
- Advocate count: 2 (Advocate-A for "Third mode" / Advocate-B for "Sibling skill")
- Debate orchestrated inline; per-point steelman + critique applied to each Medium+ severity item and the X-001 architectural contradiction

## Round 1: Advocate Statements

### Advocate-A (Third Mode — `sc:reflect --mode pr-bot-validation`)

**Position summary.** The right home for the 6-way pipeline IS inside `sc:reflect`. Reflect is the canonical audit-class skill in the SuperClaude surface; bot-review validation is an audit; therefore it belongs there. A third mode parallel to `--mode pre` and `--mode post` is the protocol-native shape, and it lets us consolidate the contract surface (one `return-contract.yaml`, one promotion-gate file, one allowed-tools frontmatter). Operator cognitive load is minimized: they learn one skill instead of two.

**Steelman of B.** B's argument from §17.7 Kill #3 ("identity dilution") is genuinely sharp. The 6-way pipeline IS structurally a PR-scoped orchestration that calls reflect twice as a sub-step (Phase 4 and Phase 5 Variant A), which IS the literal definition of an orchestrator over reflect. B's PR-layer vs work-unit-layer distinction is also real — promoting a tasklist folder via `mv` and gating a PR merge via `gh pr merge` ARE categorically different operations. B's GitHub-status-check argument is technically correct: branch protection consumes status checks, not skill verdicts directly.

**Strengths claimed (citations from proposal-A.md):**

1. **Contract consolidation** (§3 / §9.1 additions): one `return-contract.yaml` carrying both OVM's `outcome_*` fields and PR-validation's `pr_bot_validation_*` fields lets downstream consumers (`sc:troubleshoot` Wave 6, `superclaude sprint run`) route on a single contract document rather than reconciling two.
2. **Gate cond 11 alongside cond 10** (§3 cond 11): the §14.5.2 gate stays the single load-bearing gate in the skill. Mode-conditional vacuity (cond 11 vacuous on UC-1/UC-2; OVM cond 10 vacuous on `--mode pr-bot-validation`) keeps both conditions non-conflicting.
3. **Concrete contract field family** (§3 contract fields): 12 namespaced `pr_bot_validation_*` fields + derived `pr_bot_validated` boolean. Field semantics are precise and reusable.
4. **Cost composition with OVM's `--budget-remaining`** (§6): derives ~9 turns/PR from §15 T2-midpoint ÷ 6 parallel PRs ≈ 8.7. Explicit budget-routing under §4 Wave 0 step 0.9.
5. **One CLI surface** (§3 trigger): `/sc:reflect --mode pr-bot-validation` is discoverable from the existing `/sc:reflect` help text; operators don't need to learn a new top-level command.

**Weaknesses identified in B:**

1. **Operator learns two skills.** Bot-validation as a sibling skill `sc:pr-bot-validate` means operators run `/sc:pr-bot-validate <N>` AND `/sc:reflect --mode pre|post`. Two CLI entries for one logical workflow.
2. **Skill proliferation.** Each new audit concern as its own skill grows the SuperClaude surface unboundedly. Where does it stop? Don't we end up with `sc:pr-bot-validate`, `sc:secret-scan-validate`, `sc:license-check-validate`, etc.?
3. **Reflect contract still consumed read-only by B** — so the dependency arrow isn't actually inverted; B's Wave 4 reads reflect's OVM contract. B's "orchestrator over reflect" argument is weakened by the fact that B IS still calling reflect, just from outside.

### Advocate-B (Sibling Skill — `sc:pr-bot-validate`)

**Position summary.** The right home is a **new sibling skill** `sc:pr-bot-validate` at the same protocol layer as `sc:reflect`, `sc:auggie-review`, `sc:cleanup-audit`, `sc:troubleshoot`. Reflect's identity is *work-unit verification* (UC-1 pre, UC-2 post); the 6-way pipeline is *PR-scoped lifecycle orchestration* with a categorically different verification unit. The pipeline literally calls reflect twice as a sub-step (preamble §3 Phase 4 + Phase 5 Variant A), which is the SuperClaude protocol's textbook definition of an orchestrator-over-skill, not a peer mode. A's "consolidate the contract" reasoning is *exactly* the dilution §17.7 Kill #3 names: putting an orchestrator inside the thing it orchestrates.

**Steelman of A.** A's contract-consolidation argument is sound for *consumers*: a single `return-contract.yaml` is genuinely easier to parse than reading two. A's `--max-prs` budget composition with OVM is well-thought-out and reusable. A's claim that operators learn fewer skills is real — adding a new skill imposes adoption cost. A's namespaced `pr_bot_validation_*` field family is genuinely well-designed and should port into B's `merge-gate-decision.yaml` verbatim.

**Strengths claimed (citations from proposal-B.md):**

1. **§17.7 Kill #3 identity dilution** (§1 lines 17-19): reflect's own kill-list rejects adding orchestration surfaces *for exactly this reason*. The §17.7 precedent — "rejected interactive dialogue because it duplicates brainstorm's Wave 1 and dilutes reflect's identity as a validation tool" — applies symmetrically to PR-orchestration. The kill exists to prevent this drift.
2. **PR-layer vs work-unit-layer separation** (§1 line 21-23): OVM's §14.5.2 gate fires when a tasklist folder is ready to `mv`. The PR gate fires when `gh pr merge` is about to fire. These are categorically distinct operations on categorically distinct objects (folder vs PR). Putting them in the same gate conflates lifecycles.
3. **Branch protection consumes status checks, not skill verdicts** (§3.3): the merge-gate objective is literally "GitHub blocks merge". GitHub does this via required status checks. A skill that posts `gh api .../statuses/...` is doing the same primitive operation regardless of where it lives. B does it from a sibling skill native to that lifecycle.
4. **Reflect ships unchanged** (§3 zero changes to reflect): lower risk for the v1.1 release. OVM is already a substantial change to reflect; piling another mode + cond + ref onto the same release multiplies the surface area we have to validate.
5. **Pipeline already names reflect as a sub-step** (§1 line 25): preamble §3 Phase 4 = `/sc:reflect --mode pre`; Phase 5 = `/sc:reflect --mode post`. Both UNCHANGED reflect modes. If reflect's existing surface is sufficient as a sub-primitive, the orchestrator doesn't need to become a reflect mode.

**Weaknesses identified in A:**

1. **`--recursive` anti-pattern** (reflect §17 "Will Not" #1): reflect's own protocol forbids running reflection on its own intermediate output without `--recursive`. A's third mode would call reflect from within reflect (Phase 4 = `--mode pre` invoked from `--mode pr-bot-validation`). Even with mode-disambiguation, this is exactly the recursion surface §17 guards against.
2. **Promotion adapter table doesn't fit** (reflect §14.5.1): the existing adapters (`task`, `sprint-release`) move tasklist folders. A "PR adapter" would move... what? A's third mode either adds a no-op adapter or breaks the §14.5.5 mutation-semantics invariant.
3. **Cond 11 mode-conditional vacuity is a smell**: a gate condition that's vacuous in 2-of-3 modes is a "this doesn't really fit" warning sign. Adding a condition just for a different mode is structurally a different gate, dressed in cond-11 clothing.

## Round 2: Rebuttals

### Advocate-A responds

**On §17.7 Kill #3 (B's strongest argument).** *Conceded.* The kill-list argument is structurally sharp. Adding interactive dialogue to reflect was rejected for "identity dilution"; PR-orchestration would be the same shape of addition. I cannot defend this against B's framing without weakening the kill.

**On PR-layer vs work-unit-layer (B's U-004).** *Conceded.* The two lifecycles genuinely are different. The `mv` semantics in §14.5.5 are tasklist-folder-specific; there is no analog for `gh pr merge`. Trying to add a "PR adapter" to §14.5.1 either no-ops or breaks the existing invariant. B is right that the gate layers should be separated.

**On `--recursive` anti-pattern.** *Conceded.* My proposal would call `--mode pre` from within `--mode pr-bot-validation`, which is exactly the recursion surface §17 guards against. Even with mode-disambiguation logic, the smell is real.

**Standing.** A's contract field family (U-001) and budget composition (U-002) remain valuable and should port verbatim into B's `merge-gate-decision.yaml` schema. They are downstream-executable detail B's proposal sketches at higher altitude.

**Conclusion.** A concedes the architectural debate. The merged proposal should adopt B's sibling-skill architecture as base AND incorporate A's contract-field shapes and budget-composition mechanics where they map cleanly.

### Advocate-B responds

**Standing.** B's architectural arguments hold. With A's concessions, the merge is straightforward: B as base + A's U-001 (contract fields) + A's U-002 (budget composition) ported into the sibling skill's contract.

**Concession to A.** A's point about operator cognitive load is real. The merged proposal should make `/sc:pr-bot-validate` discoverable from `/sc:reflect` help text via a one-line "Related Commands" addition (low-cost cross-reference, no surface change). This is a single-line edit in sc:reflect-protocol/SKILL.md §16 "Related Commands" section, distinct from adding a mode.

## Round 2.5: Invariant Probe (fault-finder)

Six-category boundary-condition scan against the emerging consensus (B as base + A's strengths incorporated).

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|-----------|--------|----------|----------|
| INV-001 | state_variables | `pr_bot_validate_contract_version: 1.0` (sibling skill) and reflect's `contract_version: 1.1` (OVM) evolve independently without breaking consumers | ADDRESSED | LOW | B §3.5 explicitly states independent versioning; consumers read each contract's own version field |
| INV-002 | guard_conditions | The sibling skill's `gh api .../statuses/<sha>` write is idempotent across `synchronize` events; multiple writes to the same SHA's status with the same context name don't break branch protection | UNADDRESSED | **MEDIUM** | Neither proposal cites GitHub API docs confirming idempotency. Per GitHub API spec, multiple status writes are allowed but only the latest is consumed by branch protection — should be safe, but worth a one-line note in §5 trade-offs |
| INV-003 | count_divergence | `--max-prs 6` with `--budget-remaining` interaction: if budget can't support 6 PRs, does the skill error, degrade gracefully to ≤6, or silently truncate? | UNADDRESSED | LOW | A §6 says auto-degrades; B §3 says caps at 6 manual / 1 per CI trigger. Merged proposal must specify the degradation rule explicitly |
| INV-004 | collection_boundaries | Empty PR set (zero PRs match `refs/bot-review-sources.yaml` patterns): the skill exits cleanly with `status: success`, `prs_processed: 0`, `merge_gate_decision: not_applicable`; does NOT post a status check (no PR to attach to) | UNADDRESSED | LOW | Neither proposal explicitly addresses the zero-PR case. Merged proposal should clarify |
| INV-005 | interaction_effects | Multiple bots disagree on the same PR (e.g., Augment says "CONFIRMED on `foo.py:42`" + CodeRabbit says "FALSE_POSITIVE on `foo.py:42`"); how does the bucket logic adjudicate? | UNADDRESSED | **MEDIUM** | Both proposals process bots independently; cross-bot disagreement is not addressed. Merged proposal should defer to v1.2 explicitly in §9 out-of-scope, or sketch a per-finding "highest-validity-bucket-wins" rule with citation |
| INV-006 | sufficiency_challenge | Does the merged proposal close the bot-review-validation-as-merge-gate gap? Concretely: after sibling skill ships + workflow is wired + branch protection requires `sc-pr-bot-validate / merge-gate` status check, will a PR with an unresolved Augment-Code-flagged-as-CONFIRMED critical finding be BLOCKED from merging? | ADDRESSED | LOW | Trace: Wave 1 discovers PR → Wave 2 spawns subagent → /sc:auggie-review cross-validates Augment finding → finding bucketed as CONFIRMED → Wave 4 reflect-pre on PROPOSALS-normalized.md → if `confirmed_count + still_valid_count > 0` AND no post-remediation receipts, status check = FAIL → branch protection blocks merge. **Sufficient.** |

**Invariant-probe gate verdict:** 2 MEDIUM UNADDRESSED items (INV-002 idempotency, INV-005 multi-bot disagreement). No HIGH items. Per §convergence_detection.invariant_probe_gate: MEDIUM items don't block convergence; they're logged as warnings.

**Warnings appended to merge contract:**
- INV-002: Merged proposal §5 must note GitHub status-check write idempotency assumption
- INV-005: Merged proposal must either (a) defer multi-bot disagreement to v1.2 in §9 out-of-scope, or (b) sketch a per-finding precedence rule with concrete example
- INV-003: Merged proposal must specify the `--max-prs` + `--budget-remaining` interaction explicitly (degrade vs error vs truncate)
- INV-004: Merged proposal must clarify the empty-PR-set case behavior

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|-----------|--------|------------|-----------------|
| X-001 (architectural home) | **B** | **95%** | A conceded under §17.7 Kill #3 + PR-layer vs work-unit-layer arguments; no remaining defense |
| C-001 (third mode vs sibling) | B | 95% | Direct consequence of X-001 |
| C-002 (reflect changes) | B | 95% | Zero changes to reflect is structurally cleaner + safer for v1.1 release |
| C-004 (gate layer) | B | 90% | PR-layer / work-unit-layer separation correctness |
| C-009 (composition mechanism) | B | 85% | Read-only consumption of reflect's contract is cleaner than additive coupling |
| C-005 (version bump) | B | 80% | Independent sibling 1.0 doesn't multiply v1.1 release risk |
| C-010 (task-builder handoff) | B | 85% | Sibling stops at Wave 4; operator runs task-builder per preamble §9 |
| C-011 (force-push handling) | B | 85% | GitHub's native `synchronize` event is the right primitive |
| C-003 (status check mechanic) | Either | 100% | Same `gh api .../statuses/` primitive, different posting agent — no material difference |
| C-006 (ref file location) | B | 75% | Single-skill home for the ref file is cleaner; sibling skill owns its own refs |
| C-007 (triggers) | Either | 90% | Same mechanism, different skill name binding |
| C-008 (cost envelope) | Either | 100% | Same T2 cost; sibling inherits |
| **U-001 (A's contract fields)** | **Take from A** | **95%** | Port `pr_bot_validation_*` field family verbatim into B's `merge-gate-decision.yaml` schema |
| **U-002 (A's budget composition)** | **Take from A** | **90%** | `--max-prs` + `--budget-remaining` mechanics + §15 T2-midpoint derivation port directly |
| U-003 (B's kill-list argument) | Take from B | 95% | Load-bearing structural argument; preserve in merged §1 |
| U-004 (B's layer separation) | Take from B | 95% | Load-bearing; preserve in merged §1 + §4 |
| U-005 (B's status-check primitive) | Take from B | 95% | Platform-native; preserve in merged §3 |
| A-001 (gh CLI status-check stable) | Surface in §5 trade-offs | 80% | Document the assumption + fallback |

## Convergence Assessment

- Points resolved: 16 of 19 (X-001 decisive; 11 content C-NNN; 5 U-NNN incorporations decided; 1 shared-assumption A-001 → §5)
- Unresolved: 3 MEDIUM-priority invariant-probe items (INV-002, INV-003, INV-005) addressed via mechanism-text additions in merged proposal §3 / §5 / §9
- Alignment: **84% (16/19)**
- Threshold: 80%
- Status: **CONVERGED**
- Taxonomy coverage: L1 (CLI surface naming) covered; L2 (skill home, contract version) covered; L3 (gate layer, idempotency, budget interaction) covered. All levels covered.
- Invariant-probe gate: 0 HIGH UNADDRESSED. Convergence permitted.
- Round 3 not triggered.

**Net verdict.** B is the structurally-correct architecture. A conceded under direct rebuttal. Merge: B as base + A's contract-field shapes (U-001) + A's budget composition (U-002) + mechanism-text additions for the 4 invariant-probe warnings.
