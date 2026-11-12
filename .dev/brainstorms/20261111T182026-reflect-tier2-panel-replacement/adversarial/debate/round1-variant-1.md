---
round: 1
advocate: Variant 1 (opus:architect)
generated: 2026-11-11
reads_this_round: panel.py:130-149 and 390-424; SKILL.md:784-791 and 946-955; ledger.py:84-97; ensemble.py:70-77; refs/cost-profile.yaml:40-74; merge_cmd.py:21-40; contract.py:290-327 (all under src/superclaude/)
---

# Round 1, Variant 1 (architect): layered review kernel

## Position summary

Variant 1 has the best long-term structure. It splits the shared model into four layers, each with a schema id: resolution (K1), dispatch (K2), findings (K3) and merge (K4). It gives a concrete, validator-legal reflect template, a superset finding format that leaves spec-panel's parser path alone, and a staged migration with a consumer-by-consumer contract plan. It is wrong or weaker than Variant 3 on six points: executor-exclusion failure, calibration storage, cost units, the hard-kill limit, failure states, and keeping 1.8.0 stable. I adopt Variant 3's handling on those points and Variant 2's measurement arm and dispatch rule.

## Steelman

### Variant 2 (sonnet:analyzer): stage-gated panel-fed T2

**Strongest version.** The panel today has only `resolve` and `validate`, and merge takes exactly one `--doc` (merge_cmd.py:29-34, read: `required=True`, "The candidate reviewed in this round"). So the panel cannot take over dispatch, calibration or the evidence gate. The honest move is to adopt what exists (resolution and clustering), keep the debate until a measurement says otherwise, and ask first whether T2 beats T1 at all. Variant 2 is the only variant that asks that question (its First measurement section: "Three arms ... T1 only; current T2; panel-fed T2"). Its dispatch rule is also the only one that works with the Agent tool's model enum without guessing: `launch` non-null means an agent session, `launch` null means a swarm worker. Its reading of the real card (calibrator scores 0.60/0.50/0.55, and a heading citation dropped by the semantic validator) is the best evidence in any variant that a deterministic locate check cannot replace the validator.

**What it gets right.** It measures T2 against T1. Its dispatch rule matches the tool. It keeps the debate until data says otherwise. It names the forbidden-model filter.

**Critique.** Its central template does not validate. It needs two fixed slots, sonnet "`t1b`, fixed" and calibrator "fixed `cal` slot". The validator rejects that: `if fixed != 1: errors.append(f"exactly one slot must be 'fixed' (the anchor); found {fixed}")` (panel.py:140-141, read). A `cal` slot would also be dispatched as a reviewer. Concatenating the plan and spec into one `review-doc.md` loses source identity, and the validator then has to re-read synthetic line numbers. Its claim that calibration sidecars exist "as it does now" is false: calibration is embedded in the card (X-008). Calling stage 5 an "additive 1.9.0" contradicts the versioning rule. Minor versions allow "no semantic change to existing fields", and a major version covers any "semantic change" (SKILL.md:952-953, read). Widening EV-2's exact legal set (SKILL.md:789, read) is a semantic change.

### Variant 3 (haiku:backend): snapshot-bound kernel with real adversarial finalizer

**Strongest version.** The hard constraint says 1.8.0 stays stable. EV-2 says "LEGAL VALUES ARE EXACTLY {adversarial, single-reviewer-fallback}" and "Reflect MUST NOT synthesize its own merge" (SKILL.md:789, read). So the only design that ships the shared kernel with zero consumer migration keeps a real debate as the finalizer and uses clustering only to prepare its input. Variant 3 also designs failure honestly:

- five completion states;
- an idempotency key under which a retry never adds a vote;
- atomic publish, because `merge_cmd.py` writes the report before the ledger;
- cost units kept apart, including the hard kill. The profile says "1 turn ≈ 1k claude tokens" (cost-profile.yaml:54) and "abort runs that exceed 1.25× the midpoint" (cost-profile.yaml:69-70), so the abort point is about 65.6k.

It is also the only variant that replaces an ineligible anchor before resolution, not after the slot is emptied.

**What it gets right.** It keeps the contract stable, designs failure states, keeps cost units and the hard kill straight, handles the executor-excluded anchor, and keeps calibration attached to the card.

**Critique.** Its dedupe key includes "normalized claim text". Two independent reviewers almost never word a claim the same way, so the exact key will rarely collapse anything. All matching then falls back to the debate, which is today's design with extra machinery. Its schema is a new envelope, so the panel's `findings-v1` path needs a "lossless adapter", a second parser to maintain. Variant 1's superset keeps one parser. It gives no concrete reflect template, only "one Tier 1b-capability anchor and two eligible independent slots". Its manifest state machine is valuable, but the variant itself warns that "scope grows into a generic workflow platform" (risk 9). It has no deterministic citation check, so headless runs keep no real `citations_dropped` until the agent validator is ported. Its claim that pre-execution reviewer support is "not existing" is false (X-011).

## Strengths claimed

1. **A legal, concrete reflect template.** The `@reflect-pre` JSON has exactly one `fixed` slot (t1b) plus two `random` slots (variant-1 lines 147-153). It satisfies `fixed != 1` (panel.py:140-141). Variant 2's template fails that check, and Variant 3 gives no template.
2. **Layer ownership as the maintenance unit.** Variant 1 names where reviewer identity, finding shape and merge each live today, and reduces each to one implementation with a schema id (variant-1 lines 86, 101-113). A third consumer then adds only a template, a brief and a contract mapping (line 92). This is the extension scaffolding the architecture domain asks for.
3. **A superset finding format with a single parser path.** findings-v2 keeps every v1 field and rule. `anchor` becomes optional only when `citations[]` is present, and a v1 line is valid v2 by construction (variant-1 lines 196-213). Spec-panel keeps its parser. Stage 1 exit requires that "v1 reports merge byte-identically with and without `--schema`" (line 276). That answers A-014 explicitly. Variants 2 and 3 only imply it.
4. **A dedupe key that actually clusters.** Fingerprint v2 adds path and class to the v1 key. `same_defect_v2` merges through a shared role and path within ±3 lines, or a shared REQ ref (lines 219-229). It is conservative toward splitting ("a split costs a duplicate report line, not a lost finding", line 389). It is neither too loose like Variant 2's single-document span overlap nor too strict like Variant 3's claim-text key.
5. **Correct version classification.** Variant 1 reads `merge_method: panel` as a major change under SKILL.md:953, read: "semantic change ... Breaking. All consumers in the §9.3 map MUST update before producing-side ships". It lists each consumer change (lines 285-334). Variant 2 mislabels the same change as additive (X-004).
6. **Found a real wrapper mis-fire.** Variant 1 says trigger 11 "would mis-fire on a pre panel run" (line 325). The code confirms it: `if tier_reached == 2 and contract.get("adversarial_convergence_score") is None: return "null-convergence"` (contract.py:299-300, read). Trigger 11b checks only `_score is not None` (contract.py:317-318). Any deterministic merge path needs the guard Variant 1 specifies. Variant 2's stage 5 reaches the same conclusion, and Variant 3 avoids the issue by keeping the debate.
7. **Accurate code-gap analysis of the panel resolver.** Fixed slots ignore exclusion, and random and round-robin fall back to all candidates. Variant 1 cites these correctly: `model = candidates[0]` at panel.py:402-403, and the `or candidates` fallbacks at panel.py:405 and 408 (read). Variant 2 is off by one (X-019).
8. **The shared-card shadow measurement isolates the merge.** Reviewers and calibrators run once, and both merges read identical calibrated cards (lines 408, 252). That removes reviewer sampling noise from the merge comparison and halves the cost. The seeded defects are scripted, so ground truth does not come from reviewer output (lines 402-406).
9. **A concrete plan for the headless `citations_dropped` gap.** Stage 5 runs the same deterministic pre-check headless, so the wrapper's citation trigger can fire there for the first time. That change is called out as a behaviour change at Stage 5 entry (lines 265, 327).
10. **Less Opus than today in anthropic-only.** Today's default third reviewer there is Opus. Moving Opus from a reviewer card (about 5-10k) to a disjoint calibrator re-grade (about 1-2k per card) cuts Opus output and turns `calibrator_diversity` from `degraded` to `full` (lines 157, U-005).

## Weaknesses identified in other variants

1. **Variant 2: an invalid template (X-001).** Two fixed slots break panel.py:140-141, and a `cal` slot would be dispatched as a reviewer. The chosen stage-1 composition does not run as written.
2. **Variant 2: concatenating plan and spec (X-007, C-023).** merge_cmd.py:29-34 takes one `--doc`. Variant 2 works around that by building a synthetic document, so its line numbers are not the real files' line numbers. The evidence-validator then has to map them back, and Variant 2 itself marks this UNVERIFIED in its last bullet.
3. **Variant 2: an "additive 1.9.0" that is a semantic change (X-004).** SKILL.md:952 forbids "semantic change to existing fields" in a minor version. Rewording gate 9 and widening EV-2 are semantic changes.
4. **Variant 2: confused cost units and an internal contradiction (X-012, X-015).** It treats the profile's 35-70k "claude tokens" as output tokens. The profile defines them through a turn budget (cost-profile.yaml:42, 54, read). It gives a net of "-5k to +3k" in one place and "0 to -2k" in another.
5. **Variant 3: wrong contract version (X-003, shared).** Its table says `contract_version` is "Constant `1.8.0` / Unchanged". The headless builder emits `REFLECT_CONTRACT_VERSION = "1.0"` (ensemble.py:74, read). Variants 1 and 2 share the error. Variant 3 makes the strongest stability claim, so it costs Variant 3 the most.
6. **Variant 3: its exact dedupe key barely dedupes (C-005).** Normalized claim text in the key means paraphrased duplicates stay separate. The cluster stage then saves no debate work, which undercuts its own savings hypothesis.
7. **Variant 3: the pre reviewer gap is misstated (X-011).** It says pre-execution reviewer support is a proposed change. The recorded pre run's card has `agent_type: reflect-reviewer` with `plan:` and `spec:` fields (diff-analysis X-011; I did not re-read the card).
8. **Variant 3: no concrete template, flag-level adapter or command lines.** "Resolve reviewer slots" stays abstract. An implementer has to design the template again.

## Concessions

1. **Executor exclusion on the fixed anchor (X-002, C-017).** In anthropic-only with a Sonnet executor, Variant 1's `hard_exclude` raises on tier1b, because there is no tier1b stand-in, and the run degrades to T1. Today reflect would still field Haiku plus Opus in that case. That is a regression. Variant 3's rule is right: replace an ineligible anchor before resolution. I adopt it.
2. **The contract version (X-003).** The versioning plan treats the current version as 1.8.0. The headless builder emits "1.0" (ensemble.py:74). The plan must reconcile the two builders before any bump.
3. **Calibration storage (X-009, A-004, X-008).** The sidecar `calibration.json` carries only a number plus `dims[5]`. It drops per-finding reasons, and the post debate reads cards that would no longer carry calibrated scores. Fix: keep the full calibration block embedded in the card, as today, and make the sidecar an index only. Variant 3's handling is better here.
4. **Cost units and the hard kill (X-012, X-013).** The before range of 49-96k is labelled output tokens, but it is anchored on a turn-budget figure. Its top, and the after-top of 68k, both exceed the 1.25 × 52.5k ≈ 65.6k abort point (cost-profile.yaml:50-51, 70). The figures are also inconsistent: 34-66k in the candidate block and comparison table, 35-68k in the cost model. Variant 3's cost section is the correct one.
5. **The debate claim is overstated (X-006).** "Separated nothing" is an agreement observation (convergence 1.0 four times and 0.97 once, single-vendor), not a recall measurement. The removal is gated on measurement, but the summary's wording claims more than the evidence supports. Variant 2's "keep until measured" is the calibrated stance.
6. **No T1 arm (A-001).** Variant 1's first measurement compares merges only. It cannot show whether pre T2 is worth 35-70k at all. Variant 2's T1 arm should be added.
7. **The `--cap 1` ledger records ESCALATE (X-017).** `_decision` returns `"REVISE" if n < ledger["cap_reviews"] else "ESCALATE"` (ledger.py:93-96, read). With cap 1, every blocking round writes ESCALATE into an on-disk record that EV-1 reads. Reflect ignores it, but a human reader of the ledger would be misled. Variant 3's "disable automatic clearing; REVISE is not permission" is cleaner.
8. **The pre-check can drop valid citations (A-010).** An exact flattened-quote `locate` fails on a paraphrased or line-wrapped quote. Because `citations_dropped > 0` forces partial status, the pre-check could degrade honest runs. Fix: the pre-check drops only a missing file or an out-of-range line. A quote mismatch is flagged for the validator, not dropped.
9. **Gateway alias dispatch (X-010).** The Agent tool `model` enum accepts only sonnet, opus, haiku and fable, so the tier-alias override fails. Variant 2's rule (null `launch` goes to swarm) replaces Variant 1's UNVERIFIED path.
10. **Smaller errors.** The ledger cites are wrong (X-018). The launch-map description omits the `fable` entry (X-020). Variant 1's kernel validation does reject Fable ids, but the description is incomplete.
11. **Failure states.** Variant 1 has a re-ask and the F2 path but no completion-state model, idempotency key or atomic publish (S-008, C-024, U-014 to U-017). Variant 3's state block should be grafted onto K2/K4.

## Shared assumption responses

- A-001: QUALIFY - Pre T2's value is unmeasured, so the first measurement must include a T1-only arm (Variant 2) before any pre migration is justified by more than maintenance.
- A-002: QUALIFY - Haiku stand-in results inform only the anthropic-only environment, so any gateway default needs its own gateway run, and no variant plans one.
- A-003: REJECT - The recorded card cites line refs with no quotes, so `quote` must be optional when `path` and a line range are given, with the semantic validator as the authority.
- A-004: QUALIFY - The calibration block (dimensions, per-finding reasons, notes) must stay intact on the card, and any sidecar is an index, not a reduction.
- A-005: REJECT - Profile "claude tokens" come from a turn budget (cost-profile.yaml:54), so they cannot be compared with PN1 output tokens or artifact bytes/4 without a conversion stated per lane.
- A-006: QUALIFY - Reflect's class list does not match the gateway tier models, so K1 needs an explicit per-model `class` map (Variant 1's proposal) before the exclusion and disjoint-calibrator rules can be trusted.
- A-008: QUALIFY - Keeping the post debate is the safe default, but its value is unproven, so post adoption needs its own class-accuracy trial before any narrowing.
- A-009: QUALIFY - The consumer inventory comes from documentation only, so a repo-wide grep for `merge_method`, `contract_version` and convergence readers must be a hard entry criterion (Variant 1 Stage 3), and it must include the "1.0" headless builder.
- A-010: REJECT - An exact quote locate can fail on a valid paraphrased or wrapped citation, so the pre-check may drop only a missing file or range and must flag quote mismatches to the validator.
- A-012: QUALIFY - Seeded defects are a recall proxy with known truth, but they must be paired with natural or authored defects (Variant 2's union ledger, Variant 3's authored cases) to avoid measuring only the injection types.
- A-014: ACCEPT - Spec-panel must stay unchanged, and Variant 1's byte-identical v1 merge test is the right mechanical check, so all three variants should adopt it.

## Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | NONE | All three share the same order; no meaningful difference. |
| S-002 | V1 | Five candidates including dispatcher-only and debate-always, each with a verdict and a matrix, show the staging logic. |
| S-003 | V1 | Marks enrichment provenance separately from lines read, which is the most honest citation convention. |
| S-004 | V1 | "Direct answer:" lead is scannable; tie with V2, V3 lacks the label. |
| S-005 | V1 | Q5/Q7 give a direct summary and point to one authoritative section, which avoids duplicated numbers drifting. |
| S-006 | V1 | The field table with "v1?" and "Set by" columns is the most implementable schema spec. |
| S-007 | V1 | Numbered steps with concrete command lines and a shadow-mode paragraph. |
| S-008 | V3 | Only variant with a state machine, idempotency and resume rule; V1 should adopt it. |
| S-009 | V1 | A "What ships" column plus entry/exit/rollback per stage is the clearest migration table. |
| S-010 | V1 | Consumer-level detail, including wrapper trigger guards verified at contract.py:299-300 and 317-318. |
| S-011 | V3 | Keeps units apart and ties to the hard kill; V1's layout carries wrong units. |
| S-012 | V1 | Risks with mitigations plus a full PROPOSED-names inventory. |
| C-001 | V1 | The widest, most useful candidate set, with D and E serving as named stage and rollback positions. |
| C-002 | V1 | The layered kernel is the best maintainable structure; with V3's anchor and calibration fixes, its debate removal stays behind a flag until measured. |
| C-003 | V1 | The owner-per-function table is the most complete take/lack/stay map. |
| C-004 | V1 | A superset keeps one parser for spec-panel; V3's envelope needs a second adapter, and V2 reuses the v1 info string as a hack. |
| C-005 | V1 | Clusters through shared files and refs; V3's claim-text key barely dedupes, and V2 depends on a synthetic doc. |
| C-006 | V2 | Keeping the pre debate until measured matches the evidence; V1 overclaims. |
| C-007 | V1 | Pre-cluster plus debate with an explicit, measurement-gated narrowing stage. |
| C-008 | V2 | The `launch` non-null to agent, null to swarm rule works with the Agent tool enum; V1's alias override does not. |
| C-009 | V1 | The only concrete template that passes panel.py:140-141. |
| C-010 | V1 | The most complete, executable pre flow. |
| C-011 | V3 | Disables automatic clearing and treats retries as attempts; V1's cap 1 writes ESCALATE (ledger.py:93-96). |
| C-012 | V3 | Correct units and within the 65.6k hard kill; V1's top exceeds it. |
| C-013 | V2 | Gives a measurable threshold (15-point recall gain) for calling a larger panel. |
| C-014 | V1 | Includes the spec-panel byte-identity exit test and a shadow stage. |
| C-015 | V3 | No contract change is needed for the first shipment; V1's major bump is correctly classified but deferrable. |
| C-016 | V3 | A real child score keeps `merge_method` and gate 9 meaning intact under SKILL.md:789. |
| C-017 | V3 | Replacing the anchor before resolution avoids V1's degrade-to-T1 regression. |
| C-018 | V1 | An explicit, minimal Opus use that also fixes `calibrator_diversity`; V2's `cal` slot is illegal. |
| C-019 | V1 | Validation before merge so only kept findings cluster, provided the pre-check only flags quote mismatches (A-010). |
| C-020 | V2 | A T2-vs-T1 arm answers the most basic open question; V1's shared-card design should be one of its arms. |
| C-021 | V3 | Resolves a disjoint judge and records collisions instead of leaving it UNVERIFIED. |
| C-022 | V1 | A concrete stage that makes headless `citations_dropped` real. |
| C-023 | V1 | Role-qualified documents keep source identity; V2's concatenation does not. |
| C-024 | V3 | Five completion states make incomplete runs explicit. |
| C-025 | V1 | `--t2-engine legacy\|shadow\|panel` names the three modes directly. |
| X-001 | V1 | V1's template has one fixed slot; V2's fails the validator. |
| X-002 | V3 | Anchor substitution before resolution; V1 regresses to T1, and V2's "drop the slot" breaks the one-fixed rule. |
| X-003 | NONE | All three assume 1.8.0; the headless builder emits "1.0" (ensemble.py:74). |
| X-004 | V1 | A widened legal set is a semantic change, so major (SKILL.md:953). |
| X-005 | V3 | Never needs a non-adversarial merge, so the no-own-merge rule (SKILL.md:789) holds without a major bump. |
| X-006 | V2 | "Keep until measured" fits thin agreement-only evidence. |
| X-007 | V1 | Role-qualified multi-doc beats concatenation; V3 proposes the same idea less concretely. |
| X-008 | V3 | Keeps calibration with the card as today; V2's "as it does now" is false and V1's sidecar loses data. |
| X-009 | V3 | Calibrated cards reach the debate intact; V1 has an internal gap. |
| X-010 | V2 | Its dispatch rule avoids the enum limit. |
| X-011 | V2 | Grounds pre reviewer use in the recorded pre card; V3's claim is false. |
| X-012 | V3 | Reads the profile units correctly (cost-profile.yaml:54). |
| X-013 | V3 | Computes the hard kill; V1's range exceeds it. |
| X-014 | V3 | V3 explains its target vs allowance in text; V1 has an unexplained 34-66 vs 35-68 mismatch. |
| X-015 | V3 | V2's net figures contradict each other; V3's arithmetic is reconciled. |
| X-016 | V1 | V1's Opus use is lower than today and justified by the disjoint rule; V3 reaches the same outcome in anthropic-only but less explicitly. |
| X-017 | V3 | Avoids writing a misleading ESCALATE decision into the ledger. |
| X-018 | V2 | V2's ledger cites (86-90, 93-96) are correct; V1's are wrong. |
| X-019 | V1 | V1 cites 405 and 408 correctly. |
| X-020 | V2 | Names the Fable entry and a resolve-time filter; V1's description is incomplete. |
| A-001 | V2 | Only variant that tests T2 vs T1. |
| A-002 | NONE | No variant plans a gateway run. |
| A-003 | V1 | Already decouples `anchor` from typed citations; making `quote` optional is a one-field change. |
| A-004 | V3 | Keeps the calibration record and its path/hash on the submission. |
| A-005 | V3 | Keeps output, retrieval and turn-budget units apart. |
| A-006 | V1 | Proposes the explicit per-model `class` map that resolves the mismatch. |
| A-008 | V3 | Requires an independent post trial before any change to the post debate. |
| A-009 | V1 | Makes a repo-wide grep a hard Stage 3 entry criterion. |
| A-010 | V3 | Does not rely on a quote-locate drop; V1 and V2 assume it is safe. |
| A-012 | V2 | Pairs seeded defects with a union ledger of natural findings. |
| A-014 | V1 | Only variant with an explicit byte-identical spec-panel test. |
