PASS 1 (input order: Variant 1 then Variant 2)

Variant 1 = Proposal A (`variant-1-original.md`: per-environment launch adapters, raw-id `claude -p --model` with transcript identity check, class-word Agent call kept for `reflect-reviewer`, reflect ceiling widened). Variant 2 = Proposal B (`variant-2-original.md`: class-word dispatch only, no raw-id launcher in the core). Requirement source: conflict row C-07 (both positions, the "Why undecidable" clause, research files 04, 03, 06, 07, 13, GQ-049, INV-G, INV-L, INV-F) plus the position-paper sections. Each variant is judged as written in its original text. Debate and diff evidence is cited only where it shows a defect that was found and confirmed against the code: `debate:R1/advocate-A`, `debate:R2/advocate-B`, `diff:X-009`, and so on. Nothing the debate later built (the gated hybrid) is credited to either variant. Section numbers `sN` refer to the variant's own H2 sections. A verdict of 1 needs a located or quoted evidence item; otherwise 0.

## Completeness

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| C1 Covers all explicit requirements from source input | Variant 1 | 0 | Position, INV-G/L/F, PR-review, rf-qa, test and objection are covered, but explicit row elements are absent. GQ-049 never appears (searched s1-s7); the "family-alias resolution not verified" clause is not mentioned (s7 names only "the Agent enum, `resolvedModel`"); of research files 04, 03, 06, 07, 13 only r04 and r13 are cited (r08 and w02 are extra; no r03, r06, r07). quant-score.py: 24 of 30 topics, missing swarm, family-alias, r03, r06, r07, GQ-049. |
| C1 Covers all explicit requirements from source input | Variant 2 | 1 | Header "Conflict IDs: C-S6, CO-10, FX-13" and "Invariants at stake: INV-G (HIGH), INV-L (MEDIUM), INV-F (MEDIUM)"; s9 "(GQ-049, r04 gap 3)"; s3.2 and s9 name the family-alias edge case "(`docs/reference/model-aliases.md`, 'not verified')"; E2/E3 cover Bash left open; s5 item 1 covers the missing comparison and cost; swarm transport in s1. r04, r13, r06 (E9 "r06 line 290") are cited. r03 and r07 are not cited, but the dispatch-collapse content of r07 appears through E11 and r04. quant-score.py: 28 of 30 topics. |
| C2 Addresses edge cases and failure scenarios | Variant 1 | 1 | s6 M-1: "Wrong if mismatches cannot be told from a legitimate failover, or if the observed field is empty for gateway ids"; M-2: "If wrong, A narrows to `agent-class` plus an unproven `claude-p`"; s4 INV-B: "A launch failure reaches the merge as a missing reviewer". |
| C2 Addresses edge cases and failure scenarios | Variant 2 | 1 | E11: "The orchestrator can drop the argument: in run A-r3 all three reviewers and three calibrators were dispatched with no `model`"; s5 item 6 fall-back trigger ("a workspace cannot export the class map before the session starts"); s7 item 6 residuals. |
| C3 Includes dependencies and prerequisites | Variant 1 | 1 | s4 "Dependencies on adjudicated slots, stated exactly": C-01 (shared layer, "no change to `cli/reflect`"), C-02 (open `--resolution` fallback), C-03 (condition 5, INV-007), C-06 (persisted session, "`--no-session-persistence`"), C-08. |
| C3 Includes dependencies and prerequisites | Variant 2 | 1 | s8 states consistency and "Dependency on one: C-03 condition 3"; s2 table rows "Slot C-08 ... B needs the capture to exist" and "Slot C-09 ... B needs one owner for the model-to-class-word map"; s9 open facts. |
| C4 Defines success/completion criteria | Variant 1 | 1 | s6 M-1: "Right if every attempt has an observed id, every mismatch is recorded as a mismatch (zero unrecorded swaps), and at least one id is served that the `agent-class` path cannot request"; M-2 and M-3 have right/wrong rules. |
| C4 Defines success/completion criteria | Variant 2 | 1 | s5 item 1: "B is right if the identity match under (a) is not worse than under (b) beyond the noise band ... B is wrong if (a) shows a served-versus-intended mismatch rate above (b) that a data edit cannot remove". Items 2-6 give tests with predictions. |
| C5 Specifies what is explicitly out of scope | Variant 1 | 1 | s2: "Where that row is stored is slot C-08, not decided here"; s4: "this proposal does not settle that fallback" (C-02) and "I do not claim it closes INV-007" (C-03); no change to engine or ledger. |
| C5 Specifies what is explicitly out of scope | Variant 2 | 1 | s9 title "Open facts the position depends on (not decided here)"; s2: "B does not choose the owner" (C-09) and "it does not choose its home" (C-08); s6: r13 Q3 "remains the owner's decision in C-11". |

## Correctness

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| K1 No factual errors or hallucinated claims | Variant 1 | 0 | Confirmed errors: the additive `adapters` key is claimed to leave tests and D4 undisturbed, but `validate_tiers` rejects any unknown environment key (`panel.py:371-373`) and `load_tiers` raises (`debate:R2/advocate-A` N1); s2 says filling `gateway.launch` would "change D4's trigger", which `SKILL.md:320` refutes in part because "gateway" is a separate trigger (`diff:X-003`); s3 point 6 and point 11 overstate "silent swap" and "no check at all today" (`diff:X-005`; `debate:R1/advocate-A` concessions citing `SKILL.md:341`); the full commit id in the header line is not a valid object (`debate:R2/advocate-A` N8). |
| K1 No factual errors or hallucinated claims | Variant 2 | 0 | s2 and s4 state that "Position A rewrites the same test" (`test_review_panel.py:303-308`); the test asserts `launch is None` and passes under A's additive form (`diff:X-002`). E7 repeats "silent swap" (`diff:X-005`). The central data edit, filling the packaged `gateway.launch` with class words, was withdrawn by B as wrong (`debate:R2/advocate-B` section 0, item 1). |
| K2 Technical approaches are feasible with stated constraints | Variant 1 | 0 | As written the `adapters` map cannot load (`debate:R2/advocate-A` N1, `panel.py:371-373`); the ceiling check as specified (`adapter == claude-p`) reads no `read_only` marker (`diff:X-009`); the identity evidence ran under `bypassPermissions` while the read-only adapter needs `--restricted`, which refuses it (`diff:X-008`); the `agent-class` adapter has no executor in a Python module (`debate:R1/advocate-B` W1, conceded in `debate:R2/advocate-A`). |
| K2 Technical approaches are feasible with stated constraints | Variant 2 | 0 | The one edit B makes to clear the `--env gateway` refusal is infeasible as packaged: over 400 run ids `reflect-pre` slot `t4` varies across three models, the documented default binding disagrees with every tier-4 model, and any packaged tier edit changes `tiers_sha256` and orphans recorded shadow runs (`debate:R2/advocate-B` section 0 item 1, `reflect_shadow_exit.py:128-132`). The dispatch-error rule is a prompt rule with no enforcer (`debate:R1/advocate-A` W3; conceded in `debate:R2/advocate-B`). |
| K3 Terminology used consistently and accurately throughout | Variant 1 | 0 | The central term "launch adapter" is applied to `agent-class`, which launches nothing (the orchestrator makes the Agent call); `debate:R1/advocate-A` concedes "the `agent-class` adapter is not a launcher". s2 also carries two parallel maps, `launch` and `adapters`, with no stated precedence (`debate:R2/advocate-A` B-W4). "Silent swap" is a misnomer for a ladder step that is logged (`diff:X-005`). |
| K3 Terminology used consistently and accurately throughout | Variant 2 | 1 | s2 defines "Dispatch contract" = "the resolution JSON plus one rule" and uses `launch` word, class word, core, and engine-local adapter in that sense throughout s2, s4, s5, s7. One slip, "silent swap" in E7 (`diff:X-005`, Low), does not change the vocabulary. |
| K4 No internal contradictions | Variant 1 | 0 | Two intra-variant contradictions recorded: `diff:X-008` (identity evidence from a `bypassPermissions` flag set versus a read-only adapter that needs `--restricted`) and `diff:X-009` (s1 widens the ceiling only for a "mechanically restricted" process, s2 accepts any `adapter == claude-p`, s4 says a module must refuse `read_only: unproven`). IC in quant-score-output.json: 2 contradictions over 17 tagged claims. |
| K4 No internal contradictions | Variant 2 | 1 | `diff-analysis.md` Summary: "intra-variant 2: X-008, X-009, both in Variant A"; none recorded for Variant B. s2 ("launches nothing") and E9 (raw-id substrate exists outside `cli/review`) differ in scope, which `diff:X-006` calls "both true at their stated scope". IC: 0 contradictions over 28 tagged claims. |
| K5 Claims supported by evidence or rationale within the document | Variant 1 | 1 | s3 numbers 11 evidence points, each with file:line and a tag, for example point 5: "`run-reviewer.sh:48` runs `claude -p --model \"$MODEL\" ...`; `:51` reads the unique `message.model` ...; `:56` sets `MODEL_OK`"; each design claim in s2 carries a reason (additive key tied to `test_review_panel.py:303-307` and `SKILL.md:320`). |
| K5 Claims supported by evidence or rationale within the document | Variant 2 | 1 | s3.1 is a 15-row table (E1-E15) with Claim, Evidence and Tag columns, for example E4 with the `results.jsonl` field `reviewer_requested_served` and the `logs/block-3.launch` launch values; s3.2 lists what the evidence does not show. |

## Structure

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| S1 Logical section ordering | Variant 1 | 1 | s1 position, s2 design consequence, s3 evidence, s4 invariants, s5 consumers, s6 test, s7 objection: each section rests on the ones before. Only s1 forward-points to "section 6, M-2". |
| S1 Logical section ordering | Variant 2 | 1 | s1 position, s2 consequence, s3 evidence (3.1, 3.2), s4 invariants, s5 test, s6 consumers, s7 objection, s8 consistency with C-01 to C-03, s9 open facts; E-rows are defined in s3 before s4, s5 and s7 cite them. |
| S2 Consistent hierarchy depth | Variant 1 | 1 | Seven H2 sections and no subsections; evidence is a flat numbered list 1-11, so there are no orphans. |
| S2 Consistent hierarchy depth | Variant 2 | 1 | Nine H2 sections; H3 appears only under s3 (3.1 and 3.2, two siblings), so no orphaned subsection. |
| S3 Clear separation of concerns between sections | Variant 1 | 1 | Each H2 holds one concern (position, consequences, evidence, invariants, consumer effect, test, objection); s4 labels its three blocks "Preserved", "Endangered", "Dependencies on adjudicated slots". The mix inside s4 is the Low-severity layout point of `diff:S-002`. |
| S3 Clear separation of concerns between sections | Variant 2 | 1 | Invariants (s4), consistency with adjudicated slots (s8) and open facts (s9) are separate sections; s3.2 separates "what the evidence does not show" from s3.1. |
| S4 Navigation aids present | Variant 1 | 1 | Cross-references and a legend: line 7 defines `r04:n`, `E2@6c09843`, `s05`, `s06` and the tags; internal pointers "(section 6, M-2)" in s1 and "(point 4)", "point 11" in s7. quant-score.py: 13 of 13 internal references resolve. |
| S4 Navigation aids present | Variant 2 | 1 | Line 7 legend of citation forms; header block with conflict IDs; E-row ids cited from s4, s5, s7 ("E11", "E9", "E1"). quant-score.py: 60 of 60 internal references resolve. |
| S5 Follows conventions of the artifact type | Variant 1 | 1 | Status line "Status: Complete" and the position-paper sections: position, design consequence, evidence, invariants, PR-review and rf-qa effect, test or measurement, strongest objection and answer; consistency with C-01, C-02 and C-03 sits in s4 rather than a separate section. |
| S5 Follows conventions of the artifact type | Variant 2 | 1 | "Status: Complete", "Position: B", conflict IDs and code state in a header block, the same section set, plus a separate s8 on C-01 to C-03 and a s9 on open facts. |

## Clarity

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| L1 Unambiguous language | Variant 1 | 0 | No hedge words ("should consider", "might"). The gate itself is stated two non-equivalent ways: s1 "when the process is mechanically restricted to a read-only tool set" and s2 "accepts a reviewer whose `launch` is a class word or whose `adapter` is `claude-p`" (`diff:X-009`); no precedence is stated between `launch` and `adapters` (`debate:R2/advocate-A` B-W4). |
| L1 Unambiguous language | Variant 2 | 1 | The rule is one sentence: "a reviewer is launched with its `launch` word as the Agent `model` argument, and a missing argument is a dispatch error, not a fallback to the agent default"; evidence tags state what was read and what was not. |
| L2 Concrete rather than abstract | Variant 1 | 1 | s2 names files, lines and keys: "`_check_reflect_resolution` (`:137-157`) accepts a reviewer whose `launch` is a class word or whose `adapter` is `claude-p`"; s6 M-1 names five gateway ids, three attempts each, and reads `message.model`. quant-score.py: SR 1.0, no vague indicator found. |
| L2 Concrete rather than abstract | Variant 2 | 1 | s5 item 1 names the input `TASK-WF-designSpec-20261107-075614`, the panel `sonnet + luna + luna`, the noise band from rows B1-B3 and per-reviewer metrics; s2 table lists per-module edits. |
| L3 Each section has a clear purpose or can be summarized in one sentence | Variant 1 | 1 | Section titles state purpose ("The position", "Evidence", "Invariants", "Test or measurement that would show A right or wrong", "Strongest objection and answer"); s1 is one paragraph naming the position. |
| L3 Each section has a clear purpose or can be summarized in one sentence | Variant 2 | 1 | Titles such as "The test or measurement that would show B right or wrong" and "Open facts the position depends on (not decided here)"; s1 ends with the trade: "trades reach ... for the one property the research calls a HARD design point". |
| L4 Acronyms and domain terms defined on first use | Variant 1 | 1 | s1 defines the two adapters inline ("the orchestrator's Agent call with a class word `sonnet`, `opus`, `haiku`, `fable`"; "a child `claude -p --model <raw id>` process") and glosses "(INV-G)" as mechanically read-only reviewers; s4 glosses INV-A, INV-B, INV-I, INV-F by their rule. Line 7 defines citation forms. |
| L4 Acronyms and domain terms defined on first use | Variant 2 | 1 | s1 defines the class words and the intended path; s2 defines "Dispatch contract"; s4: "Definitions are those of synth-06 6.12.0" and each invariant row is glossed ("Reviewers mutually blind and mechanically read-only (INV-G, HIGH)"); line 7 defines `r04`, `W02`, `E2@6c09843`. |
| L5 Actionable next steps or decision points clearly identified | Variant 1 | 1 | s6 M-1 to M-4 each say what to run and what result decides it; M-2 states the consequence ("A narrows to `agent-class` plus an unproven `claude-p`"); s4 states that a module needing INV-G "must refuse such a reviewer". |
| L5 Actionable next steps or decision points clearly identified | Variant 2 | 1 | s5 items 1-6 are runnable, including item 6, the trigger that would send raw-id reach to an engine; s9 lists the open facts and their owning slots (C-08, C-09). |

## Risk Coverage

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| R1 Identifies at least 3 risks with probability and impact assessment | Variant 1 | 1 | s4 "Endangered" lists four rated items: "INV-G (HIGH)", "INV-K / test pins (MEDIUM)", "INV-E (MEDIUM)", "INV-L via the golden files (MEDIUM)", each with its trigger ("They would break if the same value were put in `gateway.launch`"; "[UNVERIFIED which pins compare whole objects]"); s3 point 4 gives observed frequency (haiku served `gpt-6.1-sol` in five reviewer calls; run A-r3). |
| R1 Identifies at least 3 risks with probability and impact assessment | Variant 2 | 1 | s4 table marks INV-G "Endangered in two places" (HIGH in the header) and INV-K/N endangered by the files B touches (C-03 INV-013, LOW); E11 gives the probability of the collapse risk: "1 of 15 combo runs and 0 of the 12 under the tier-1b orchestrator"; s7 item 6 names the reach residual. |
| R2 Provides mitigation strategy for each identified risk | Variant 1 | 1 | INV-G: `read_only: unproven` marker, M-2 probe, `agent-class` default for untrusted diffs (s4, s7); INV-K: additive form (note it fails the validator, `debate:R2/advocate-A` N1); INV-E: "Isolation into one module that `panel.py` does not import is the mitigation"; golden files: `reflect_shadow_exit.py:117-177` reads named fields. |
| R2 Provides mitigation strategy for each identified risk | Variant 2 | 0 | s4 INV-G: "Endangered in two places B does not close", with (a) engine-level `ClaudeProcess` children and (b) the `/task` lens agents and `rf-qa`; (b) is handed to slot C-11. s7 item 6 "The residual B accepts". Identified risks with no mitigation in the document. |
| R3 Addresses failure modes and recovery procedures | Variant 1 | 1 | s7 answer controls (1) "detection at the end of every launch ... recorded as a violation and never counted as a verified independent reviewer", (3) `agent-class` stays default; s6 M-2 states the fallback position if the probe fails. |
| R3 Addresses failure modes and recovery procedures | Variant 2 | 1 | s2: "a missing argument is a dispatch error, not a fallback"; s4 INV-I: a differing served model "is recorded, not blocked"; s5 item 6 states when raw-id reach becomes necessary and who owns it (the engine). |
| R4 Considers external dependencies and their failure scenarios | Variant 1 | 1 | s7 objection: depends on "`--tools`/`--restricted` (and their version gate), the transcript's `message.model` field, and gateway failover ... A CLI update can silently turn a read-only reviewer into one that can write"; s3 point 9 names the 2.1.248 gate. |
| R4 Considers external dependencies and their failure scenarios | Variant 2 | 1 | s9 and s3.2: Agent enum, `resolvedModel`, family-alias behaviour "this repo does not pin it (GQ-049, r04 gap 3)"; E15 `SubagentStop` fields documented but "[UNVERIFIED] in this repo"; s6 `additionalContext` reaching a subagent [UNVERIFIED]. |
| R5 Includes monitoring or validation mechanism for risk detection | Variant 1 | 1 | s7 controls: the launcher reads "the transcript's tool names and observed model" on every launch; the per-environment probe M-2 "re-run at install"; s2 outcome row fields `model_requested`, `model_observed`, tool names. |
| R5 Includes monitoring or validation mechanism for risk detection | Variant 2 | 1 | s5 item 2 collapse-detector replay (`analysis/extract.py:46-76`, prediction "flags A-r3 and no other run"); item 4 read-only pin test; item 5 served-model spike under a `SubagentStop` hook. |

## Invariant & Edge Case Coverage

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| I1 Boundary conditions for collections (empty, single-element, maximum size) | Variant 1 | 1 | s2: "the 3-cap (`:143-146`) ... untouched"; `environments.gateway.launch` "stays `{}`" (the empty map) and gets one `adapters` entry per gateway model; s6 M-1 tests five ids, three attempts each. |
| I1 Boundary conditions for collections (empty, single-element, maximum size) | Variant 2 | 1 | E13: "at most 3 reviewers and launch in `sonnet`, `opus`, `haiku`"; s7 item 4: "a seven-reviewer `live7` panel has seven models and four class words"; s7 item 6: "more than three distinct gateway models". |
| I2 State variable interactions across component boundaries | Variant 1 | 1 | s3 point 7: a named raw id still passes shim failover, "The `claude -p` identity check is the only thing that catches it"; s2: `resolve` stays pure because the launcher is a module `panel.py` does not import (`test_review_panel.py:296-300`). |
| I2 State variable interactions across component boundaries | Variant 2 | 1 | E5 chain "class word, then `ANTHROPIC_DEFAULT_*_MODEL`, then a tier alias or raw id, then the shim"; s7 item 2: the resolver cannot make the session export the right map; s3.2: the same word means a different model outside a ccsession tier workspace. |
| I3 Guard condition gaps (missing validation, unguarded type assumptions) | Variant 1 | 1 | s3 point 6: `:76` `MODEL="$NEXT"` overwrites the expected id before `:58`, and `:48` disallows only `Edit Write NotebookEdit` under `bypassPermissions` so Bash stays open; s3 point 2: `_check_reflect_resolution` rejects any other `launch`, "including `None`" (`:153-156`). |
| I3 Guard condition gaps (missing validation, unguarded type assumptions) | Variant 2 | 1 | E7: the same `MODEL` overwrite at `run-reviewer.sh:51-56, :58, :76`; E9: `reviewer_profile` is "a permission-flag omission ... not an allowlist in the argv", so its effective tool surface is [UNVERIFIED]; s2: a missing `model` argument is an error, not a fallback to `model: sonnet`. |
| I4 Count divergence scenarios (off-by-one, inclusive/exclusive ranges) | Variant 1 | 1 | s3 point 4: run A-r3 "collapsed three reviewers and three calibrators onto `claude-sonnet-5-5` ... its contract still reports `calibrator_diversity: full`"; s4 C-03 dependency: `requested` "can collapse because `panel.resolve` drops skipped slots, `panel.py:636-656`". |
| I4 Count divergence scenarios (off-by-one, inclusive/exclusive ranges) | Variant 2 | 1 | E11 (one served model for three reviewers and three calibrators, "1 of 15 combo runs"); E12: `identity_source: observed` "appears in 1 of 15 combo contracts and 0 of 13 pilot contracts"; s8: C-03's INV-007 "`requested` can collapse to 1" is the same defect under either position. |
| I5 Interaction effects when features or components combine | Variant 1 | 1 | s2 and s4 INV-L: D4 (`SKILL.md:320`) keeps routing a gateway cell to the legacy rotation, and the widened ceiling takes effect only "when the effective engine is `panel`"; s4 C-06: a bounded re-ask needs a persisted session, E2 runs `--no-session-persistence`. |
| I5 Interaction effects when features or components combine | Variant 2 | 1 | s6 "Hook-based exchange (slot C-12)": E2 hook families "skip subagent calls by design (r09:130, r09:42)", a cost B places on C-12; s4 INV-L: the gateway data edit versus `panel_parity` (`reflect_shadow_exit.py:117-177`) compares persona and class, never `launch`. |

## Subtotals

| Dimension | Variant 1 | Variant 2 |
|---|---|---|
| Completeness | 4/5 | 5/5 |
| Correctness | 1/5 | 3/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 5/5 |
| Risk Coverage | 5/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| Total | 24/30 | 27/30 |
| qual_score (total / 30) | 0.800 | 0.900 |

Cross-check with the quantitative layer (`quant-score-output.json`): K4 matches IC (Variant 1 has 2 recorded intra-variant contradictions, Variant 2 none). Correctness is the dimension that separates the variants and the one where both lose points, since each has at least one claim the code refutes (`diff:X-002`, `diff:X-003`, N1 of `debate:R2/advocate-A`).

## Edge Case Floor Check

| Variant | Invariant & Edge Case score | Floor (at least 1/5) | Eligible as base |
|---|---|---|---|
| Variant 1 | 5/5 | Met | Yes |
| Variant 2 | 5/5 | Met | Yes |

Floor not suspended: both variants meet it.
