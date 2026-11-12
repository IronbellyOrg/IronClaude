## Position summary

Variant 2 argues for a stage-gated panel-fed Tier 2: take reviewer resolution and clustering now, keep the debate, calibration and evidence gate, and remove the debate only after a measurement that first asks whether T2 beats T1 at all. I concede that V2's Q4 template is invalid as written (X-001) and that its cost units and calibration-sidecar claim are wrong (X-008, X-012); on contract hygiene V3 is stronger, and on kernel depth V1 is stronger.

## Steelman

### Variant 1 (opus:architect)
V1's strongest argument: the maintenance unit is the layer, not the command. Reviewer identity lives in three places (reflect rotation, the `T2Model0N` env pool, the panel tier file), finding shape in two, and merge in two. A four-layer kernel with schema ids collapses each to one implementation (V1 "Chosen architecture", reason 1). V1 also designs the strongest mechanical safeguards: a deterministic citation pre-check that can only add drops, a hard executor-exclusion input, a scripted seeded-defect corpus that avoids the ledger circularity (V1 "First measurement"), and a shared-card shadow run that isolates the merge and halves cost. It also acknowledges that widening `merge_method` is a major version change and lists every consumer. It is right that the recorded convergence (1.0 in 4 of 5, 0.97 in one) gives the debate no demonstrated value in pre-execution.
Critique: V1 ships the removal before the evidence. It concedes the sample is 6 runs but still makes the deterministic merge the Stage 3 and 4 default. It also invents `merge_method: panel`, which collides with the EV-2 rule "Reflect MUST NOT synthesize its own merge" (X-005).

### Variant 3 (haiku:backend)
V3's strongest argument: do not change the meaning of a shipping verdict while replacing the transport. Keeping a real adversarial finalizer leaves `merge_method`, `adversarial_convergence_score` and gate 9 untouched, so no consumer migrates. V3 alone treats failure honestly. It has five completion states, an idempotency identity so retries never add votes, an atomic publish because `merge_cmd.py` writes the report before the ledger (merge_cmd.py:113-116 per the diff analysis), and a "safety failure fails regardless of savings" test rule. V3 is also right that concatenating plan and spec into one document makes citations fragile (X-007), and its cost section keeps output tokens, retrieval tokens and turn-budget figures apart.
Critique: V3's dedupe key hashes normalized claim text, so two reviewers phrasing the same defect differently never cluster. That defeats the reason for deterministic matching. V3 also measures only legacy vs shared with the debate held constant, so it cannot tell whether T2 is worth keeping. Its design adds a manifest state machine and five new schemas with no cost estimate for that engineering.

## Strengths claimed

1. **It measures the question the others skip (U-008, A-001).** V2's first experiment has a T1-only arm and a stop rule: if T2 recall does not beat T1 by 15 points, shrink T2 to 2 reviewers rather than migrate (V2 "First measurement"). V1 and V3 only compare panel vs legacy, so a pass would certify a migration of something never shown to be worth running. The six recorded runs show agreement, not quality.
2. **It uses real card evidence for why calibration and the gate stay (U-009).** The calibrator scored F1-F3 at 0.60/0.50/0.55 ("fit major better than blocking"; reviewer-1-card.yaml:88-90, 101 as V2 cites), and the final gate dropped `source.md:143` because a heading does not support the claim (REPORT.md:130-132). A quote-locates check passes that citation. That is why V2 puts the pre-check in front of the validator, not in place of it.
3. **It does not force a contract change before data (C-006, C-015).** Stages 1-4 keep all 1.8.0 values; only optional stage 5 needs a version, and V2 states the reason (EV-2 at SKILL.md:666, 789). V1 plans a 2.0.0 at Stage 3, before its measurement is trusted.
4. **It reads the panel code accurately on the points that matter.** The fixed-slot bug is exactly where V2 points: `resolve_slot` for a fixed slot returns `candidates[0]` and ignores `exclude` (panel.py:402-403). Random and round-robin fall back to the full list when the pool empties. V2's risk 10 spots that exclusion can empty the only tier1b model in anthropic-only. I confirmed by reading `review-tiers.default.json:28`: the `stand_ins` object has no `tier1b` key. V2 also spots the Fable id in `available` and `names` (lines 14, 27) and adds a forbidden-model filter (U-013); V1 only half-notes it (X-020).
5. **It carries per-reviewer engine selection from the data.** The `launch` field (non-null spawns an agent session; null means swarm, explicit `T2ModelNN` wins) follows review-tiers.default.json:20, 29 directly and preserves today's override behaviour (C-008).
6. **Cost honesty on net effect.** V2 says the migration's case is composition and consistency, not savings (net 0 to -2k) and names the debate-shrink assumption as the weak point. V1's "30% saving" rests entirely on an assumed 15-30k debate lane.

## Weaknesses identified in other variants

1. **V1 `panel` breaks EV-2.** SKILL.md:789 (per the diff analysis X-005) limits legal `merge_method` values to `adversarial` and `single-reviewer-fallback`, and says reflect must not synthesize its own merge. V1 concedes a major bump, but then its Stage 2 shadow and Stage 3 flag depend on a consumer sweep V1 itself marks UNVERIFIED (grep of `contract_version` and `merge_method` equality, X-017/A-009).
2. **V1's cost range overshoots the profile hard kill (X-013).** `cost-profile.yaml:70` gives a 1.25x multiplier over the 52.5k midpoint, about 65.6k. V1's before-high (96k) and after-high (68k) both exceed it, and V1's before range is built from lane guesses, not the profile.
3. **V1 `--cap 1` records ESCALATE (X-017).** `ledger.py:93-96` gives `REVISE if n < cap else ESCALATE`, so every blocking round with cap 1 records ESCALATE. V1 lists this as UNVERIFIED and says it is "recorded and ignored", but a ledger file on disk that EV-1 treats as the merged record then carries a misleading decision.
4. **V1 calibration step contradicts itself (X-009).** Calibration lives in a sidecar and "reviewer output is never mutated", yet the post debate takes `--compare <calibrated cards>`, whose input is the card file (SKILL.md:645-647, 1192 per the diff analysis).
5. **V3 never tests whether T2 matters, and its debate-kept result is unfalsified (X-006).** "Agreement observations, not defect-recall measurements" is right, but V3 holds the debate constant in the first measurement and so cannot find out either. V2's C2 arm does.
6. **V3's exact dedupe key under-merges.** It includes normalized claim text and a quote hash, so independent reviewers rarely produce equal keys. It also asserts "related but not equal findings stay separate", which leaves the debate to do all the matching, the situation V2 candidate A describes as the weakness of today's design (cards are non-uniform).
7. **V3 reads as a platform.** The manifest, five completion states, idempotency identity and three new schemas are each defensible but there is no cost for building them, and the 96-run experiment costs 4.8M tokens by V3's own arithmetic. That is a heavy gate for a "first" measurement.
8. **V3 and V1 both skip an evidence point V2 verified.** Neither engages with the gateway `launch: {}` gap in the Agent tool as a blocking constraint with a swarm path; V1 leaves it as an "UNVERIFIED Stage 1 exit check" even though the Agent tool's `model` enum in this session is `sonnet|opus|haiku|fable` (X-010), so a tier alias cannot be passed.

## Concessions

1. **X-001: V2's template is invalid.** The Q4 mapping needs `t1b` as fixed and a `cal` slot as fixed. I read `panel.py:140-141`: "exactly one slot must be 'fixed' (the anchor); found {fixed}". Also every slot becomes a reviewer entry (panel.py:498-513 per the diff analysis), so a `cal` slot would be dispatched as a reviewer. The calibrator must be chosen outside the panel template, as V1 does.
2. **X-008: the sidecar claim is wrong.** V2 says the calibrator writes a sidecar "as it does now"; the card holds an embedded `calibration:` block. V1 is more accurate in saying its sidecar is a change.
3. **X-012 and A-005: V2 treats a turn-budget figure as output tokens.** The profile's 35k-70k are "claude tokens" derived from a turn budget (cost-profile.yaml:42, 50-54 per the diff analysis). V3 separates units; V2 does not.
4. **X-003: V2's contract table says `contract_version` is "1.8.0".** I confirmed in `ensemble.py:74, 788` that the headless builder writes `REFLECT_CONTRACT_VERSION = "1.0"`. V2 never read the constant.
5. **X-004: V2 labels stage 5 "additive 1.9.0" but edits EV-2 and gate 9.** By SKILL.md:952-953 that is a semantic change, hence major. V1's reading is correct.
6. **X-019: V2's `panel.py:405, 409` is off by one;** the fallbacks are at 405 and 408.
7. **Concatenating plan and spec (X-007) is a weak answer.** `merge_cmd.py:29-34` takes one `--doc`, so V2 chose concatenation, but V3 is right that it blurs source identity. V2 also admits it did not check whether the validator can re-read `anchor2` quotes in the combined file.
8. **V2 is thin on failure handling.** It has no state machine, no atomic publish and no completion taxonomy (U-014, U-015, U-017). V3 wins those.
9. **V2 did not open `cost-profile.yaml`, `SKILL.md` section 9.4 or `fallback.py`** and says so; the hard-kill figure and the version rules came from others.
10. **A-006 hits V2's mapping too.** V2's table maps reflect rotation entries onto tier slots without noting that `SKILL.md:1180` lists kimi and deepseek that the gateway tiers do not carry.

## Shared assumption responses

A-001: REJECT - whether pre-execution T2 beats T1 is unmeasured, so the design must test it first (V2's T1 arm) rather than assume it.
A-002: QUALIFY - Haiku stand-ins can validate mechanics, cost and compliance but not gateway-model quality, so any pass must be labelled anthropic-only evidence.
A-003: REJECT - the recorded card cites line refs only (`reviewer-1-card.yaml:12`: `evidence: [plan:57, ...]`), so quote anchors are a new burden; the diff analysis marks this CONTRADICTED, and V2's `cites` carries line ranges, which fits better than a quote-only model.
A-004: ACCEPT as a risk, not as a safe step - a findings block loses the five dimension scores and reason text, which is why V2 keeps the full card and joins a sidecar by `(reviewer_id, fid)`.
A-005: REJECT - profile tokens are turn-budget estimates, PN1 figures are output tokens and artifact bytes/4 mixes input copies, so none are comparable until measured per lane; I include my own V2 error here.
A-006: REJECT - `SKILL.md:1180` lists kimi and deepseek, which the gateway tier lists (review-tiers.default.json:5-10, read) do not contain, so exclusion and the disjoint rule need an explicit class map.
A-008: QUALIFY - post debate should stay until data exists, but the only post datapoint (0.836, `judge_class_collision`) is an unread snippet, so "needs the debate" is a defensible default, not a finding.
A-009: ACCEPT as an open risk - nobody has grepped tests and graders for `merge_method` or `contract_version` equality; V2 and V3 both defer it, and X-003 shows that even the version value was misread.
A-010: QUALIFY - a pre-check that exact-locates a quote will wrongly drop paraphrased or wrapped quotes, so it must flag rather than drop, or use whitespace-flattened matching as the panel's `locate` does (findings.py:276-304).
A-012: QUALIFY - seeded defects give clean ground truth but not natural plan defects, which is why V2 pairs them with a union ledger and V1's scripted injection is the better seed mechanism.
A-014: ACCEPT - reuse leaves spec-panel unchanged only if new flags are off by default and a byte-identical v1 test exists; V1 states this test, V2 and V3 only imply it.

## Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | NONE | Same order in all three; no decision value. |
| S-002 | V1 | A five-column matrix compares candidates most clearly. |
| S-003 | V2 | Path abbreviation and PROPOSED/UNVERIFIED markers keep citations auditable; V3 copied a timestamp. |
| S-004 | NONE | Heading style only. |
| S-005 | V3 | Answering Q5 and Q7 in place avoids forward-pointer hunting. |
| S-006 | V1 | The "v1?" and "Set by" columns show who may write each field, which V2's two tables lack. |
| S-007 | V1 | Concrete commands and a shadow paragraph make the sketch executable. |
| S-008 | V3 | Only V3 designs state, idempotency and resume. |
| S-009 | V1 | Includes "What ships" per stage. |
| S-010 | V1 | Versioning plan plus a consumer-by-consumer change list. |
| S-011 | V3 | Keeps output, retrieval and turn-budget units apart. |
| S-012 | V1 | Separates assumptions, UNVERIFIED and a PROPOSED-name inventory. |
| C-001 | V2 | Includes thin adoption and a no-debate variant as separate rungs. |
| C-002 | V2 | Stage-gated path commits to no unmeasured removal and keeps 1.8.0 through stage 4. |
| C-003 | V1 | Most complete takes/lacks split. |
| C-004 | V1 | Typed `citations[]` with roles fits multi-file findings better than `anchor2` plus `cites`. |
| C-005 | V1 | Citation-aware merge tolerates different phrasing; V3's claim-text key under-merges. |
| C-006 | V2 | Keeps debate until a measurement, with removal only in an optional stage. |
| C-007 | V2 | Keeps a cluster-table debate for class conflict at minimum. |
| C-008 | V2 | The `launch` field decides per reviewer, with `T2ModelNN` as override. |
| C-009 | V1 | Its three-slot template has one fixed slot and passes the validator; V2's does not (X-001). |
| C-010 | V1 | Most complete pre flow, including hard exclusion and citation pre-check. |
| C-011 | V3 | Retries are attempts, not votes, and automatic clearing is off. |
| C-012 | V3 | Keeps units separate and ties to the 65.6k hard kill. |
| C-013 | V2 | Names a numeric gate (15 points) and an Opus-calibrator ablation for the 4+ reviewer decision. |
| C-014 | V1 | Seven stages with shadow before opt-in, each with entry, exit and rollback. |
| C-015 | V3 | No contract change needed when the real debate stays. |
| C-016 | V3 | Refuses to disguise deterministic agreement as convergence. |
| C-017 | V1 | Hard exclusion also on fixed slots with a degrade-to-T1 path. |
| C-018 | V3 | Opus only when no lower-tier disjoint choice exists, matching "sparingly". |
| C-019 | V1 | A deterministic pre-check before the validator, add-only. |
| C-020 | V2 | Only V2 can show whether T2 beats T1. |
| C-021 | V3 | Resolves a disjoint judge, records collisions, never Fable or Tier 0. |
| C-022 | V1 | Closes the headless `citations_dropped` gap in a named stage. |
| C-023 | V3 | Keeps source identity separate; concatenation is fragile (X-007). |
| C-024 | V3 | Five completion states; quorum counts complete only. |
| C-025 | NONE | Names only. |
| X-001 | V1 | V1's template has one fixed slot and passes `panel.py:140-141`; V2's fails. |
| X-002 | NONE | Three incompatible failure behaviours, all PROPOSED; no variant is right as written. |
| X-003 | NONE | `ensemble.py:74` shows "1.0"; all three misread it. |
| X-004 | V1 | A widened legal-value set is a major change per SKILL.md:952-953. |
| X-005 | V3 | Avoids a non-adversarial `merge_method` altogether. |
| X-006 | V2 | Evidence is thin on both sides; keep until measured is the only supportable position. |
| X-007 | V3 | `merge_cmd.py:29-34` has a single `--doc`, so concatenation hides source identity. |
| X-008 | V1 | V1 treats the sidecar as a change; V2 misstated current behaviour. |
| X-009 | V3 | V3's cards carry calibration references into the debate. |
| X-010 | NONE | The Agent `model` enum rejects gateway aliases; no variant resolved it. |
| X-011 | V2 | V2 relies on the recorded pre card; V3's "not existing" claim is false for the run (the agent text is post-only). |
| X-012 | V3 | V3 correctly separates a turn-budget figure from output tokens. |
| X-013 | V3 | V3 computes the 65.6k hard kill. |
| X-014 | NONE | V3's 37-53k vs 37-56k is a minor text gap. |
| X-015 | NONE | V2's net figures are inconsistent in text. |
| X-016 | V3 | Opus not as routine anchor, closest to "sparingly". |
| X-017 | V1 | V1 flagged `_decision` under cap 1 as UNVERIFIED and it is real. |
| X-018 | NONE | Cite error in V1, substance right. |
| X-019 | V1 | V1 cites 405, 408 correctly; V2 is off by one. |
| X-020 | V2 | V2 and V3 note the Fable launch entry; V1 omitted it. |
| A-001 | V2 | Only V2 states and tests the assumption. |
| A-002 | NONE | No variant tests stand-in transfer. |
| A-003 | NONE | All three assume quote anchors against the recorded card. |
| A-004 | V3 | Preserves per-card calibration and refuses invented per-finding precision. |
| A-005 | V3 | Keeps units separate. |
| A-006 | V3 | Records actual class and vendor, and excludes on all fallbacks. |
| A-008 | NONE | The only post datapoint is unread; cannot be decided. |
| A-009 | V3 | Requires a consumer re-check before implementation. |
| A-010 | V3 | Keeps only the validator and flags ambiguity as a gap, not a drop. |
| A-012 | V1 | Scripted injection is the cleanest seed. |
| A-014 | V1 | Only V1 states a byte-identical spec-panel test. |
