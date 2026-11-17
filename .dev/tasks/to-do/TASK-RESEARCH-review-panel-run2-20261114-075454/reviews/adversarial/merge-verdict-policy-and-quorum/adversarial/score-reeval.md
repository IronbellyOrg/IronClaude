# Score re-evaluation: slot C-03 (merge-verdict-policy-and-quorum)

Evaluator: tie-resolving pass. Inputs read in full: variant-1-original.md (Proposal A), variant-2-original.md (Proposal B), plus score-pass1.md and score-pass2.md rows for S3 and I2, and the debate transcript lines on `pending`, `_brief_ids`, `defer` and `merge_round`. Variants are scored as written in the original files. Debate evidence is used only to locate known gaps.

## Dispute 1: S3 "Clear separation of concerns between sections", Variant 1 (Proposal A)

CLAIM: Proposal A keeps design, evidence, invariants, test, effect and objection in separate sections, so concerns are clearly separated.

EVIDENCE:
- Top-level structure: s1 position, s2 "Design consequence for the shared core and the named modules", s3 "Evidence" (3.1 code today, 3.2 alternatives' machinery, 3.3 external), s4 "Invariants" (4.1 Preserved, 4.2 Endangered), s5 "The test or measurement", s6 "Effect on future PR code review and rf-qa replacement", s7 "Strongest objection and the answer". Each heading names one concern and the content under it matches the heading.
- Blemishes pass 1 relied on, checked against the text:
  - s2.2 Reflect bullet carries test-pin evidence (`test_i3_partial_two_of_three_distinct_pass_eligible`, `test_fx7_reviewer_shortfall_token_does_not_over_degrade`, `ensemble.py:762-764`) and one sentence beginning "Note for the debate: ... [CODE-CONTRADICTED] by the pins above". That is real mixing, about one bullet in size.
  - s2.3 (exit codes) cites `ledger_cmd.py:13`, `models.py:38-49` and test lines inside the design section.
- These are inline justifications of a design choice, not a collapse of the section structure. Section 3 does not duplicate them, so the pin evidence lives only in 2.2, which is a placement flaw but not a blending of sections.

Bar-consistency check (Variant 2 on S3): Proposal B's s2.1 items 4-6 also carry inline code citations and tags (`contract.py:31-33, 274-275`, `findings_v2.py:96-97`, `cluster.py:12-13`), and s2.3 is a scope note ("What B takes from common ground and does not argue") inside the design section. Pass 1 gave B a MET on S3 despite this. Applying the same bar, inline citations in the design section and a short scope note do not defeat S3. A's one debate aside is the only item with no counterpart in B, and it is a single sentence, not a mixed section.

VERDICT: MET (1). Section-level separation is explicit and each section holds its own concern. The pass 1 cited defects are minor placement and inline-citation issues that B shares in kind.

FINAL VERDICT: MET

## Dispute 2: I2 "Handles state variable interactions across component boundaries", Variant 2 (Proposal B)

CLAIM: Proposal B identifies and specifies how state moves across component boundaries (manifest, ledger/core, reflect contract) and how its new state interacts with the existing state.

EVIDENCE (what B does say, as written):
- s2.1 item 5: quorum "computed from recorded completion states (`manifest.py:52`, `reviewers_complete` at `manifest.py:20-21, 269-274` [CODE-VERIFIED]) and from served model ids", defaulting to the existing Tier-2 gate (`fallback.py:75-82`, `contract.py:282-288` [CODE-VERIFIED]). This joins manifest state with served-model state and the reflect gate. s3.1 E11 cites `QuorumState`.
- s2.1 item 1: the carrier is named, `policy(rows, panel_state, adjudication) -> verdict`, plus item 2, a per-row adjudication record stored as additive optional keys in `review-ledger/1`.
- s2.1 item 4: adjudication stage down falls back to `union` and the outcome is DEGRADED, never PASS, with the reflect map cited (`contract.py:31-33, 274-275`).
- s4 Preserved, INV-B: "Adjudication failures reach it through fields it already reads (`degraded_components` with `evidence-validator`, `adversarial_unavailable`, `adversarial_subrun_status`), which E7 shows are already degrade triggers." This is a specific, code-cited mapping of core state onto existing reflect contract inputs.
- s3.1 E1, E2, E5: only `blocking` and `open`/`regressed` reach `_brief_ids` and `_decision`; `ledger.py` uses none of the kernel's `disputed`, `support` or `cluster_agreement`, nor the manifest stages.

EVIDENCE (what B does not say, the pass 2 points, confirmed):
- s2.1 item 3 says `pending` blockers "stay open, count in the headline, and block PASS" while only `confirmed` blockers drive the brief. B never traces this through `_brief_ids`, `merge_round`'s `"FAIL" if brief else "PASS"`, `defer`, or the stored round verdict, and s4 says the 0/10/11 exit contract is unchanged. A pending-only round has no honest verdict or exit code in that contract (debate:R1/A W1-W2, conceded debate:R2/B). B also never states that `merge_round` takes no manifest input, although that follows from E5.
- So the most important new state variable (`pending`) is not reconciled with the ledger's `status` and brief state.

Bar-consistency check (Variant 1 on I2): A has the stronger treatment. It states "`ledger.merge_round` never reads the manifest", names the carrier (round entry gains `requested`, `resolved`, per-reviewer `completion`), covers derive-on-read versus the stored verdict (`ledger.py:363-372`), and flags the shared 10/11 exit numbers (s2.3). But A also leaves its DEGRADED outcome without a fix-loop transition, cap accounting or `defer` interaction (debate: A-003 rejected for both papers; stored-verdict point). Pass 2 still scored A MET. Applying one bar to both: a variant meets I2 when it cites specific cross-boundary state flows with a named carrier, even if it leaves a corner of the interaction unspecified. Under a strict "all interactions" reading both would fail; under the reading pass 2 applied to A, B's cited flows (manifest to quorum, core adjudication to reflect `degraded_components`/`adversarial_unavailable`, per-row record in the ledger schema) also qualify. Pass 2's asymmetry is not supported by a difference in kind, only in completeness.

VERDICT: MET (1). B gives specific, code-cited cross-boundary state handling at two boundaries (manifest to quorum precondition; core adjudication state to the reflect contract's existing degrade inputs) and names the carriers. The `pending` versus `_brief_ids`/`defer` gap is real and is recorded here as a weakness; it limits B's completeness but is the same class of gap A has with DEGRADED, and A is MET.

FINAL VERDICT: MET
