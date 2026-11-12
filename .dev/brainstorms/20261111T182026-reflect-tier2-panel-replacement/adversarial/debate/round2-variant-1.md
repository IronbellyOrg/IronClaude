---
round: 2
advocate: Variant 1 (opus:architect)
generated: 2026-11-11
reads_this_round: diff-analysis.md; round1-variant-1/2/3.md; variant-1-opus-architect.md:214-282; skills/sc-reflect-protocol/SKILL.md:1172-1193; cli/review/findings.py:360-408; cli/reflect/ensemble.py:784-819 (code paths under src/superclaude/). Lines cited from Round 1 reads are marked "(R1 read)".
---

# Round 2, Variant 1 (architect): rebuttal

## Responses to criticisms

Each criticism raised against Variant 1 in Round 1 by Variant 2 (V2) or Variant 3 (V3), with my answer.

1. **"V1 ships debate removal before the evidence" (V2 critique; V3 weakness 1).** Partly conceded, partly answered.
   - The answer: removal is gated on the measurement, not just on calendar time. Stage 2's exit requires "first measurement run and **passed**" plus 20 or more shadow runs in which the debate stays authoritative. Stage 3's entry requires the Stage 2 exit (variant-1:277-278, read). The shadow paragraph says "The debate result is authoritative" (variant-1:252, read).
   - The concession: the measurement that gates removal has no T1 arm and uses a 0.10 non-inferiority margin. With 60 seeded defects, that margin is too wide to show the debate is dispensable. The summary also says "removed by default" as the target state. That claims more than agreement-only evidence supports (X-006).
   - Final position: the pre debate stays as the finalizer through Stage 4. Deterministic merge becomes a post-measurement option. It must pass V2's three-arm design (T1, current T2, panel-fed T2), with V1's shared-card pairing used inside the two T2 arms.

2. **"`merge_method: panel` collides with EV-2" (V2 weakness 1, X-005).** Conceded as a first-shipment matter. V1 classified the change correctly as a major version (X-004), and every critic agrees it is major. But a 2.0.0 is not needed while the debate stays. With the debate kept, `merge_method` stays `adversarial`, and the 1.9.0 additive panel fields are the only contract change. `panel` and 2.0.0 move to an optional later stage behind V2's measurement gate.

3. **"Cost range overshoots the hard kill; the 30% saving rests on an assumed debate lane" (V2 weaknesses 2 and 6, X-013).** Conceded in Round 1. I take V3's figures and units. V2 is also right that the saving came entirely from the debate lane. Once the debate is kept, V1 claims no token saving for the first shipment. Its case is maintenance: one resolver, one finding shape, and one merge.

4. **"`--cap 1` writes ESCALATE" (V2 weakness 3, X-017).** Conceded. The fix is V3's: disable automatic clearing, and record the ledger decision as non-authoritative. Better still, suppress the decision with a PROPOSED `--no-decision` option, so the record on disk does not carry a misleading ESCALATE.

5. **"Calibration sidecar contradicts the post debate input" (V2 weakness 4, V3 weakness 5, X-009).** Conceded. Today's rule is "Cards are passed to Wave 4 with calibrated scores attached" (SKILL.md:1192, read). V1 now keeps the full embedded calibration block in each card, as today. Raw reviewer bytes are kept as a separate immutable file (V3's "materialize a calibrated view"). `calibration.json` becomes an index only.

6. **"Gateway alias dispatch left UNVERIFIED" (V2 weakness 8, X-010).** Conceded. I adopt V2's rule: a non-null `launch` value goes to an agent session, and a null value goes to the swarm. I add V3's integrity rule: any `T2ModelNN` override is applied before the resolution is frozen, never after.

7. **"same_defect_v2 can combine distinct tasks through a common requirement citation" (V3 weakness 6).** Conceded. This is the strongest new criticism, and I verified it against today's matcher.
   - **Today:** `same_defect` merges either on an equal fingerprint with non-empty refs (same section and same refs), or on intersecting or empty refs **and** finding spans within ±3 lines (findings.py:371-378, read). On one document, the spans belong to the finding's own anchors.
   - **Variant 1 as written:** rule (b) accepts a match on "**some** citation of a and **some** citation of b" (variant-1:226, read). Line 228 states the consequence outright: two findings on different plan tasks merge through a shared `spec` citation plus a shared REQ ref. That is looser than v1, and it hides a defect. It breaks V1's own principle that "a split costs a duplicate report line, not a lost finding".
   - **Fix:** rule (b) compares **primary citations only**: the reviewed-artifact role, which is `plan` in pre and `source` or `diff` in post. Secondary citations never cause a merge. This restores v1 semantics on the reviewed file and keeps cross-file identity.
   - **Why not V3's exact key:** it still cannot cluster paraphrased duplicates. With the debate kept, though, an under-merge is cheap, so this point is narrower than I argued in Round 1.

8. **"Mechanical pre-check cannot justify a stronger-grounding claim" (V3 weakness 7, A-010).** Conceded, with a correction to my own Round 1 concession.
   - The correction: the locator flattens whitespace (findings.py:276-304, cited by V3; V2 notes the same). So line wrapping is not a failure case. Paraphrase is.
   - The new position: the pre-check drops a citation only when its file is missing or its line range is out of bounds. A quote mismatch is flagged for the validator. The sentence "grounding is at least as strong as today" (variant-1:246, read) still holds, because the agent validator is unchanged and runs on every surviving citation. "Stronger" is not claimed.

9. **"Executor exclusion degrades to T1" (V2 C-017 voted for V1; V3 X-002).** Already conceded in Round 1. New supporting text: SKILL.md:1190 (read) says the three pools "SHOULD be pairwise disjoint", and "When all three pools cannot be made pairwise disjoint, the partition degrades and the affected pool emits its `*_diversity: degraded` telemetry". The existing policy therefore says degrade-and-report, not raise. V1's `hard_exclude` must:
   - replace an ineligible fixed anchor before resolution (V3);
   - fall back to a degraded composition with telemetry when no replacement exists;
   - degrade to T1 only below N = 2.

10. **"Opus on every calibrator breaks 'sparingly'" (V2's C-018 vote, X-016).** Rejected, with new evidence. SKILL.md:1181 (read) says: "pick the highest-capability calibrator class from the disjoint set". Take the anthropic-only case with reviewers {sonnet, haiku}. The disjoint set holds Opus, so today's rule already picks Opus. V1 does not add Opus. It moves Opus from a reviewer card to a calibrator re-grade, and that is less Opus output than today. V3 conceded this in Round 1: its own lower-tier-first preference "changes existing policy".

11. **"V1 misreads the contract version" (X-003).** Conceded in Round 1, with new context below: the "1.0" constant belongs only to the headless post builder.

12. **Line-cite and launch-map errors (X-018, X-020).** Conceded. The two map entries look only at different lines of the same file (`review-tiers.default.json`). Whether the forbidden-model filter and the launch map would interact is not checked.

## Updated assessment of other variants

**Variant 2, steelmanned.** V2 asks the only question that can kill the whole migration: does pre T2 beat T1? It adds a stop rule (a 15-point recall gain), and its dispatch rule is the only one that fits the Agent tool's `model` enum. Its Round 1 concessions are candid: the invalid template, wrong units, the false sidecar claim, the version label and the off-by-one cite.

After Round 1, V2 has no concrete composition that runs. It needs V1's one-fixed-slot template with the calibrator chosen outside the panel template, and it agrees with that (V2 concession 1). Its concatenated document is withdrawn in all but name (V2 concession 7).

V3 makes a good point against V2's `T2ModelNN` precedence: an override applied after resolution makes the recorded hashes describe a different selection from the one dispatched. Final view: V2 provides the measurement design and the dispatch rule. It is not the base architecture.

**Variant 3, steelmanned.** V3 is right about the first shipment: share the transport, keep the verdict meaning, and make failure explicit. After Round 2, V1 agrees on everything that ships first:
- keep the debate;
- `merge_method: adversarial`;
- embedded calibration;
- replace the anchor before resolution;
- separate cost units.

The remaining V3 advantages are:
- completion states;
- an idempotency identity;
- atomic publish (`merge_cmd.py` writes the report before the ledger, per V3's merge_cmd.py:113-118 citation);
- the advisory `channel`.

These should be grafted onto V1's K2 and K4. V3's own concessions narrow its position:
- its lower-tier calibrator preference changes current policy;
- its two-class quorum tightens SKILL.md's N = 2 floor;
- its manifest is not a multi-file transaction for existing readers;
- its exact key under-merges.

V3 also still has no concrete template and no command-level adapter. An implementer would have to design K1 and K4 again, and V1 already supplies them. Final view: V3 supplies the policy for Stages 0-4 and the failure model. V1 supplies the structure, the template, the schema and the migration table.

**Convergence.** All three advocates now agree on six things:
- keep the pre debate until measured;
- add a T1 arm;
- keep calibration attached to the card;
- replace the anchor before resolution;
- use V3's units;
- require a byte-identical spec-panel test.

The real remaining split is narrow: which variant's skeleton is the base, and how loose the dedupe key should be.

## New evidence

1. **The headless contract builder is post-only.** `ensemble.py:797` (read) hard-codes `"mode": "post"`, and `:788` writes `REFLECT_CONTRACT_VERSION` (which is "1.0", ensemble.py:74, R1 read). Pre-execution reflect therefore never goes through the headless builder.
   - Consequence for X-003 and C-015: the "1.8.0 unchanged" claim (V2, V3) is correct for the pre agent-session path. It is wrong only for headless post.
   - Consequence for V1: a pre-only contract change, whether 1.9.0 additive fields or a later `panel` value, never touches the "1.0" builder. Reconciling the two builders is a Stage 5 (post) entry item, not a pre blocker.
   - This narrows the X-003 damage for all three variants.
2. **The headless gap is real and has more than one field.** `ensemble.py:808` (read) has `"verification_ran": False`, and `:814-818` has `verification_verified: False`, `regression_verified: False`, `citations_dropped: 0` and `citations_dropped_extrapolated: 0`. V1's Stage 5 item (C-022) is a concrete fix for `citations_dropped`. V3's "never copy the constant 0" is a rule without a mechanism. The verification fields stay False either way, because reviewers never execute.
3. **Today's calibrator rule already selects Opus in anthropic-only** (SKILL.md:1181, read). See response 10 above. This settles X-016 and C-018 on policy grounds, not on taste.
4. **The three-way partition is "SHOULD" with degraded telemetry** (SKILL.md:1190, read). This is the governing text for X-002 and C-017. It rules out V1's raise. It also rules out a V3 reading in which an executor-class collision blocks the run, because SKILL.md requires degradation, not refusal.
5. **Today's matcher keys on the finding's own anchors** (findings.py:363-364 `_spans` reads `span` and `span2`, and :371-378, read). V1's "some citation" generalization is therefore a semantic loosening, not a mirror of v1, and the primary-citation fix brings it back to v1. This also answers V2's C-005 reasoning: V2's span overlap on one concatenated document has the same cross-task merge risk, because both tasks' anchors can sit near a shared requirement line.

## Final shared assumption responses

Only the promoted assumptions where Round 1 responses differed are listed. A-003, A-005, A-008 and A-012 were unanimous, so they are unchanged.

- A-001: QUALIFY. Pre T2 may add recall, but nothing measured shows it. V2's T1 arm is a hard entry criterion for any pre change beyond resolution-only adoption.
- A-002: QUALIFY. Haiku stand-in results certify mechanics and anthropic-only behaviour only. A gateway default needs its own gateway run, and no variant has planned one yet.
- A-004: REJECT (changed from QUALIFY). The card holds five dimension scores, per-finding reasons and notes. Any reduction to a findings block loses them, so the full embedded block stays authoritative. My Round 1 QUALIFY already prescribed that, so REJECT is the accurate label.
- A-006: REJECT (changed from QUALIFY). As stated ("straightforward mapping") it is false: SKILL.md:1180 (read) lists classes that the gateway tier models do not match. An explicit per-model `class` map is a precondition for exclusion and for the disjoint rule.
- A-009: REJECT (changed from QUALIFY). The documented consumer map missed the "1.0" headless post constant (new evidence 1). Completeness is disproven, not merely unproven. A repo-wide grep is a hard Stage 3 entry criterion, and builder reconciliation is a Stage 5 entry criterion.
- A-010: REJECT. A quote mismatch from paraphrase is not proof of an unfounded citation. Wrapping is already tolerated by the whitespace-flattening locator. The pre-check may drop only missing files and out-of-range lines.
- A-014: QUALIFY (changed from ACCEPT). Non-interference is a property to test, not to assume. The v1 byte-identical merge test, with new flags off by default, is the acceptance criterion for all three variants.

## Per-point positions

| Point | Winner | Changed from R1? | Reason |
|---|---|---|---|
| S-001 | NONE | No | Same order in all three. |
| S-002 | V1 | No | Five candidates with verdicts plus a matrix; all three advocates agree. |
| S-003 | V1 | No | Separates enrichment provenance from lines read; V3 copied a timestamp. |
| S-004 | NONE | Yes | Heading style only; V1 and V2 both lead with a direct-answer label. |
| S-005 | V3 | Yes | Answering Q5/Q7 in place serves the reader; V2 and V3 are right that forward pointers cost lookup. |
| S-006 | V1 | No | "v1?" and "Set by" columns expose field ownership. |
| S-007 | V1 | No | Command-level steps; V3's execution contract is credited under S-008. |
| S-008 | V3 | No | Only state machine, idempotency and resume rule; graft onto K2/K4. |
| S-009 | V1 | No | "What ships" plus entry, exit and rollback per stage. |
| S-010 | V1 | No | Consumer-level change list with the verified wrapper guards (contract.py:299-300, 317-318, R1 read). |
| S-011 | V3 | No | Keeps units apart and ties to the hard kill. |
| S-012 | V1 | No | Full PROPOSED-name inventory. |
| C-001 | V1 | No | Widest candidate set; D and E are named stages and rollbacks. |
| C-002 | V1 | No | Kernel skeleton as the base, with V3's policy for Stages 0-4 (debate kept, adversarial merge method); V1's own Stages 0-2 already match it. |
| C-003 | V1 | No | Most complete take, lack and stay map; V3's completion states belong under C-024. |
| C-004 | V1 | No | Superset keeps one parser for spec-panel; add V3's completion state and `channel` as optional v2 fields. |
| C-005 | V1 | No | With the primary-citation fix it equals v1 on the reviewed file and clusters paraphrases; V3's exact key cannot, and V2 shares the cross-task risk. |
| C-006 | V2 | No | Keep the pre debate until a measurement with a T1 arm. |
| C-007 | V1 | No | Pre-cluster plus a kept debate, with calibrated cards (fixed per X-009). |
| C-008 | V2 | No | The `launch` null/non-null rule fits the tool enum; add V3's override-before-freeze rule. |
| C-009 | V1 | No | Only concrete template that passes panel.py:140-141 (R1 read). |
| C-010 | V1 | No | Most executable pre flow; add V3's input-drift recheck. |
| C-011 | V3 | No | Retries are attempts; no automatic clearing. |
| C-012 | V3 | No | Correct units and within the 65.6k hard kill. |
| C-013 | V2 | No | Numeric 15-point gate for a larger panel. |
| C-014 | V1 | No | Shadow stage and byte-identity exit test; Stage 3 now gated on V2's measurement. |
| C-015 | V3 | No | No contract change for the first pre shipment; the headless "1.0" builder is post-only (ensemble.py:797). |
| C-016 | V3 | No | A real child score keeps gate 9 meaning. |
| C-017 | V3 | No | Replace the anchor before resolution; SKILL.md:1190 requires degrade, not raise. |
| C-018 | V1 | No | Opus calibrator is today's rule (SKILL.md:1181); embedded-calibration fix adopted. |
| C-019 | V1 | No | Pre-check drops only a missing file or range, then the unchanged validator. |
| C-020 | V2 | No | Three arms including T1; V1's shared cards inside the T2 arms. |
| C-021 | V3 | No | Resolves a disjoint judge and records collisions. |
| C-022 | V1 | No | A concrete mechanism for the verified constant 0 (ensemble.py:817). |
| C-023 | V1 | No | Role-qualified documents keep identity, the same idea as V3 but concrete. |
| C-024 | V3 | No | Five completion states. |
| C-025 | NONE | Yes | Names have no intrinsic merit; V2 and V3 are right. |
| X-001 | V1 | No | One fixed slot; V3 offers no template to test. |
| X-002 | V3 | No | Anchor replacement before resolution, consistent with SKILL.md:1190. |
| X-003 | NONE | No | All misstated; damage limited to headless post (ensemble.py:797). |
| X-004 | V1 | No | A widened legal set is a major change; all advocates agree. |
| X-005 | V3 | No | Keeps the adversarial merge, so the no-own-merge rule holds. |
| X-006 | V2 | No | Keep until measured; agreement is not recall. |
| X-007 | V1 | No | Separate documents via role-qualified `--doc`; concatenation loses identity. |
| X-008 | V3 | No | Calibration stays embedded as today; V1's sidecar is withdrawn to an index. |
| X-009 | V3 | No | V1's gap is real and conceded. |
| X-010 | V2 | No | Its dispatch rule avoids the enum limit. |
| X-011 | V2 | No | The recorded pre card shows pre use exists. |
| X-012 | V3 | No | Turn-budget figures are not output tokens. |
| X-013 | V3 | No | Computes the hard kill; V1's range exceeded it. |
| X-014 | V3 | No | Arithmetic right; target vs allowance explained. |
| X-015 | V3 | No | V2's net figures contradict each other. |
| X-016 | V1 | No | Opus as calibrator follows SKILL.md:1181 and is less Opus than today. |
| X-017 | V3 | No | No misleading ESCALATE in the ledger. |
| X-018 | V2 | No | V2's ledger cites are correct; V1's are wrong. |
| X-019 | V1 | No | 405 and 408 are correct. |
| X-020 | V2 | No | Names the Fable entry and a resolve-time filter. |
| A-001 | V2 | No | Only V2 tests T2 vs T1. |
| A-002 | NONE | No | No variant plans a gateway run. |
| A-003 | NONE | Yes | All three still carry a quote field; none establishes lossless conversion of line-only evidence. |
| A-004 | V3 | No | Keeps the full calibration record with the card. |
| A-005 | V3 | No | Keeps units separate. |
| A-006 | V1 | No | The explicit per-model `class` map is the concrete fix. |
| A-008 | V3 | No | Requires an independent post trial before narrowing. |
| A-009 | V1 | No | The only variant that makes the consumer grep a hard stage-entry gate. |
| A-010 | V3 | No | Adds no automatic quote-based drop. |
| A-012 | V2 | No | Seeded defects paired with a union ledger of natural findings. |
| A-014 | V1 | No | The only explicit byte-identical spec-panel test. |

Tally: V1 28, V2 11, V3 23, NONE 6. Changed from Round 1: 4 (S-004, S-005, C-025, A-003).

## Remaining disagreements

- **C-002, C-003, C-004, C-010:** V3 votes V3 on all four, and V2 votes V2 on C-002. I hold that V1's skeleton (template, K1-K4 schema ids, command lines) should be the base, with V3's policy and failure model grafted on. V3's design leaves the template and the merge interface undesigned.
- **C-005:** V3 favours the exact key. I hold that V1's matcher, fixed to primary citations only, is the only key that clusters paraphrased duplicates without cross-task merging. V2's single-document span overlap shares the cross-task risk.
- **C-007:** V2 and V3 each vote for themselves. All three keep the post debate, so the difference is V1's pre-cluster input, which I consider worth keeping.
- **C-008:** V3 favours its immutable binding. I keep V2's concrete null/non-null rule, plus V3's freeze rule.
- **C-018 and X-016:** V2 and V3 read "sparingly" as a reason to avoid an Opus calibrator. SKILL.md:1181 already selects it, so avoiding it would be a policy change, which V3 itself conceded.
- **C-022:** V3 votes V3. A rule without a mechanism does not close the verified `citations_dropped: 0` gap.
- **C-023 and X-007:** V2 and V3 vote V3. Both V1 and V3 keep the documents separate. V1 is the concrete one.
- **X-001:** V3 votes V3, but V3 has no template that can be checked against panel.py:140-141.
- **A-006 and A-009:** V2 and V3 vote V3. V1 is the only variant with a concrete class map, and the only one with a hard grep gate. The missed "1.0" builder shows why a hard gate, rather than a "re-check", is needed.
- **C-014:** V3 prefers V2's resolution-only first step. V1's Stage 0-2 is equally small at runtime, because it is shadow-only with the debate authoritative, and it adds the spec-panel byte-identity exit.
