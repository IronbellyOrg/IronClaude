PASS 2 (reverse order: Variant 2 then Variant 1)

Scope: slot C-07 (dispatch-and-launch-mechanism) position papers, original files only. Variant 1 = Proposal A (per-environment launch adapters), Variant 2 = Proposal B (class-word dispatch only). V1 = Variant 1, V2 = Variant 2 in the tables. Debate and diff evidence is cited as `debate:<round>/<advocate>`, `diff:<id>`, `probe:<id>`. Each variant is scored as written; the hybrid the debate later produced is not credited. Pass 1 files were not read.

## Completeness

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| C1 | V2 | MET | Position (section 1), module consequences (section 2), evidence E1-E15 (3.1), invariants INV-G/L/F (section 4), measurement (section 5), PR review and rf-qa effect (section 6), objection and answer (section 7); the conflict row's "E2 sessions leave Bash open" is E2 (3.1) and "Claude Code behaviours not pinned" is section 9 first bullet. |
| C1 | V1 | MET | Position (section 1), design consequence (section 2), 11 evidence points (section 3), invariants (section 4), PR and rf-qa effect (section 5), tests M-1 to M-4 (section 6), objection (section 7); Bash open is point 6(b), "not pinned" is point 3 and point 9, the relaxed ceiling is section 1 and section 2. |
| C2 | V2 | MET | E11 (orchestrator drops the `model` argument, 3 reviewers and 3 calibrators all served `claude-sonnet-5-5`); E7 (shim failover, ladder overwrite); "a missing argument is a dispatch error, not a fallback" (section 2); section 7 point 6 residuals (workspace cannot export the class map before launch). |
| C2 | V1 | MET | Point 4 (A-r3 collapse, `haiku` served `gpt-6.1-sol` in five calls); point 6(a) (`MODEL="$NEXT"` overwrites expected id); point 7 (shim failover on named ids); section 4 INV-B "A launch failure reaches the merge as a missing reviewer". |
| C3 | V2 | MET | Section 2 rows for slot C-08 ("Receives the served-model capture as input") and slot C-09 ("B needs one owner for the model-to-class-word map"); section 8 dependencies on C-01, C-02, C-03; section 9 open facts; E15 hook prerequisite (`SubagentStop`). |
| C3 | V1 | MET | Section 4 "Dependencies on adjudicated slots, stated exactly" (C-01, C-02, C-03, C-06 session persistence, C-08 record home); M-2 as a prerequisite for the `claude-p` adapter in an INV-G module (section 1). |
| C4 | V2 | MET | Section 5 item 1 "B is right if the identity match under (a) is not worse than under (b) beyond the noise band ... B is wrong if ..."; item 2 prediction "flags A-r3 and no other run"; item 3 test for `panel resolve --template @reflect-pre --env gateway`. |
| C4 | V1 | MET | M-1 "Right if every attempt has an observed id ... Wrong if mismatches cannot be told from a legitimate failover"; M-2 "Right if the transcript has no Bash/Edit/Write tool call and `git status` is unchanged"; M-3 "only permitted difference is the additive `adapter` key". |
| C5 | V2 | MET | Section 3.2 "What the evidence does not show"; section 2 "B does not choose the owner" (C-08, C-09); "Moving (b) is slot C-11"; section 7 point 4 "`live7` has no launcher under either position"; section 6 hook exchange "recorded here so the C-12 debate can weigh it". |
| C5 | V1 | MET | "Where that row is stored is slot C-08, not decided here" (section 2); "this proposal does not settle that fallback" (C-02, section 4); "I do not claim it closes INV-007" (C-03); "C-10's adapter to `Finding` is independent" (section 5); no change to `cli/reflect` (section 2). |

## Correctness

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| K1 | V2 | NOT MET | Section 4 last paragraph: "Position A rewrites the same test" is false for A's additive form (diff:X-002; conceded debate:R1/advocate-B). Section 5 item 4: "I did not find such a test for `reflect-reviewer.md`" is false, `tests/cli/reflect/test_reviewer_readonly_tools.py` exists (diff:X-007; conceded). Section 4 INV-L "Preserved" ignores that any packaged tier edit changes `tiers_sha256` and orphans shadow runs (`reflect_shadow_exit.py:128-132`; withdrawn debate:R2/advocate-B). |
| K1 | V1 | NOT MET | Point 11 and section 7 "has no check at all today" is too strong, `SKILL.md:341` exists (conceded debate:R1/advocate-A). Point 6(a) "a silent swap" is overstated, `run-reviewer.sh:75` logs each fallback (diff:X-005, conceded). Section 2 says a filled `gateway.launch` would "change D4's trigger", but `SKILL.md:320` lists "gateway" as a separate trigger (diff:X-003, conceded). Header line 7 cites a full commit id that is not a valid object (debate:R2/advocate-A N8). |
| K2 | V2 | NOT MET | The one data edit in section 2 (fill packaged `environments.gateway.launch` with model-to-class-word pairs) was conceded wrong: `reflect-pre` slot `t4` varies across three models over 400 run ids, the documented `haiku` binding disagrees with every tier-4 model, and the edit changes `tiers_sha256` (debate:R2/advocate-B, probe:INV-013 ADDRESSED by withdrawal). A one-word-per-model map (`panel.py:364-368`) also cannot express E4's own runs E1-E3 where `opus` and `haiku` both served `gpt-6-luna` (probe:INV-001). |
| K2 | V1 | NOT MET | The section 2 `adapters` key is rejected by `validate_tiers` (`panel.py:371-373`) and `load_tiers` raises (`:477-481`), so the design is infeasible as written (debate:R2/advocate-A N1, probe:INV-008). Section 2 `_check_reflect_resolution` accepts `adapter == claude-p` without reading `read_only` (diff:X-009, conceded). The E2 identity results ran under `bypassPermissions`, which `--restricted` refuses, so they do not transfer to the read-only adapter (diff:X-008, conceded). |
| K3 | V2 | MET | One vocabulary throughout: "class word", "`launch` value", "dispatch contract", "intended" versus "served" model (section 1, section 2 "Dispatch contract = the resolution JSON plus one rule"); the tag legend fixes [CODE-VERIFIED] / [OBSERVED-RUNTIME] / [UNVERIFIED] and each E-row uses it. |
| K3 | V1 | NOT MET | Section 1 says "Every launch, under either adapter" and calls the Agent class-word call a launch adapter the core defines, but the Agent call is made by the orchestrator, not the core (conceded debate:R1/advocate-A). Section 1 widens the "launch ceiling" while section 2 keeps `launch` untouched and reads a separate `adapter` field; two parallel maps with no stated precedence (debate:R1/advocate-B weakness 4). |
| K4 | V2 | NOT MET | Section 2 prescribes a packaged `model -> one class word` map "in the form `anthropic-only.launch` already has", while E4 reports `haiku` served `claude-haiku-5-5` in D1-D3 and `gpt-6-luna` in E1-E3, and `opus` and `haiku` both served `gpt-6-luna` in E1-E3: one word has no single model and one model has two words (probe:INV-001). Section 2 also says a missing argument "is a dispatch error, not a fallback to the agent default" while the same table keeps `model: sonnet` as the agent default and E11 is the case where that default served (probe:INV-017). |
| K4 | V1 | NOT MET | Section 1 says the `claude-p` adapter is usable by an INV-G module "only after a read-only probe passes", while section 2 has `_check_reflect_resolution` accept `adapter == claude-p` with no read of `read_only` (diff:X-009). Section 3 point 5 evidences identity under `bypassPermissions` and `--disallowedTools Edit Write NotebookEdit`, while section 3 point 9 names `--restricted`, which refuses `bypassPermissions` (diff:X-008, both inside Variant 1). |
| K5 | V2 | MET | Every factual row E1-E15 carries file:line, command or run source and a tag (e.g. E1 `reflect-reviewer.md:5-8` [CODE-VERIFIED]; E4 `results.jsonl` field `reviewer_requested_served` [OBSERVED-RUNTIME]); section 7 gives six reasoned answer points. |
| K5 | V1 | MET | Evidence points carry file:line and tags (point 2 `panel.py:71-73`, `:153-156`; point 5 `run-reviewer.sh:48,51,56` via `git show`; point 8 `test_review_panel.py:249-257`); the additive-key choice is justified by two named pins (section 2). |

## Structure

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| S1 | V2 | MET | Order: position (1), design consequence (2), evidence (3), invariants (4), measurement (5), consumer effect (6), objection (7), consistency with adjudicated slots (8), open facts (9); evidence precedes the invariants that use it. |
| S1 | V1 | MET | Order: position (1), design (2), evidence (3), invariants (4), consumer effect (5), test (6), objection (7); evidence precedes invariants and tests. |
| S2 | V2 | MET | `##` sections 1-9; `###` only 3.1 and 3.2 under section 3 (two siblings); no orphaned subsection. |
| S2 | V1 | MET | `##` sections 1-7 with no `###` level at all, so depth is uniform and nothing is orphaned. |
| S3 | V2 | MET | Design (section 2), evidence (3.1) and evidence limits (3.2), invariants (4), tests (5), consumer effect (6), adjudicated-slot consistency (8) and open facts (9) are separate sections. |
| S3 | V1 | NOT MET | Section 4 holds invariants (Preserved, Endangered) and also the cross-slot dependency list (C-01, C-02, C-03, C-06, C-08) (diff:S-001, S-002); section 3 point 6 mixes design instructions ("defects ... the proposal must not inherit") into the evidence list. |
| S4 | V2 | MET | Header block (Status, Position, Conflict IDs, Code state) and tag and shorthand legend (`r04`, `W02`, `E2@6c09843`); stable row IDs E1-E15 referenced across sections 4-7; cross-references "section 8", "slot C-08". |
| S4 | V1 | MET | Citation-form legend (`r04:n`, `s05`, `s06`, `w02`, `E2@6c09843`); labelled tests M-1 to M-4 referenced from sections 1, 5 and 7 ("section 6, M-2"). |
| S5 | V2 | MET | All required position-paper elements present: position, core and module consequences, evidence, invariants, measurement, PR and rf-qa effect, strongest objection with answer; closes with "Status: Complete". |
| S5 | V1 | MET | Same required elements in sections 1-7 including "Strongest objection and answer"; opens with "Status: Complete". |

## Clarity

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| L1 | V2 | MET | Firm rules, no hedge words: "a missing argument is a dispatch error, not a fallback to the agent default" (section 2); "no `claude -p --model <raw id>` launcher ... is added to the core" (section 1); open points are labelled [UNVERIFIED] rather than softened. |
| L1 | V1 | MET | "marked `read_only: unproven` in data until the probe passes, and a module that requires INV-G must refuse such a reviewer" (section 4); "the 3-cap ... the Fable rule and the `classes` rule ... are untouched" (section 2). |
| L2 | V2 | MET | Names the exact edit: fill `environments.gateway.launch` (`:29`, today `{}`) in the form of `anthropic-only.launch` (`:35`) and rewrite `test_gateway_resolution_prints_launch_null` (`test_review_panel.py:303-308`). |
| L2 | V1 | MET | Names the additive `adapters` map (`model id -> adapter name`), the `adapter` key printed beside `launch` (`panel.py:666-681`), and the launcher's per-attempt row fields `model_requested`, `model_observed`, `identity_source`, fallback taken, tool names seen. |
| L3 | V2 | MET | Each section is one purpose by title (position, module consequence, evidence, invariants, measurement, consumer effect, objection, consistency, open facts); 3.1 is claims, 3.2 is what is not shown. |
| L3 | V1 | MET | Each of sections 1-7 is one purpose by title (position, design consequence, evidence, invariants, consumer effect, test, objection). |
| L4 | V2 | NOT MET | Header uses INV-G (HIGH), INV-L, INV-F, C-S6, CO-10, FX-13 with no gloss; section 4 defers to "Definitions are those of synth-06 6.12.0"; "shim", "tier alias", "sidechain", "swarm HTTP transport", "live7", "GQ-049" are never defined. |
| L4 | V1 | NOT MET | "E1 path", "E2's path", "D4", "FX-8", "CO-11", "INV-E", "INV-K", "shim", "tier-2b" are used without definition; only INV-G gets an inline gloss ("mechanically read-only reviewers (INV-G)", section 1). |
| L5 | V2 | MET | Section 5 items 1-6, including item 6 "Fall-back trigger for the position itself"; section 9 lists the open facts and owners (C-08, C-09); r13 Q3 is named as the owner's decision in C-11 (section 6). |
| L5 | V1 | MET | M-1 to M-4 each state a decision rule; M-2 states the consequence "If wrong, A narrows to `agent-class` plus an unproven `claude-p`"; section 5 states which adapter a PR panel uses until M-2 passes. |

## Risk Coverage

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| R1 | V2 | MET | Three risks of the position with frequency and impact: orchestrator drops the argument (E11 "1 of 15 combo runs and 0 of the 12", contract still says `calibrator_diversity: full`); silent served-model swap (E7 "2 `b4-muse-luna2` runs served by terra"); mutation by a write-capable reviewer (INV-G HIGH, "No mutation by an E2 reviewer with Bash is recorded", section 3.2). |
| R1 | V1 | NOT MET | Section 4 Endangered rates severity (INV-G HIGH, INV-K, INV-E, golden files MEDIUM) but gives no likelihood for its own risks: cost "was never measured" (section 5), golden fixtures "[UNVERIFIED which pins compare whole objects]", CLI drift turning a read-only reviewer writable has no frequency (section 7). The only rates in the paper (points 4-5) describe harms of the existing path. |
| R2 | V2 | NOT MET | The two INV-G endangered items are left open: "Endangered in two places B does not close" (engine `ClaudeProcess` children; `/task` lens agents), with "Moving (b) is slot C-11"; section 7 point 6 "The residual B accepts" for reach. No mitigation is given for those risks. |
| R2 | V1 | MET | Each endangered risk has a control: INV-G by `read_only: unproven`, probe M-2 and `agent-class` default for untrusted diffs (section 4, section 7); test pins by the additive form; INV-E by isolating the launcher in one module `panel.py` does not import; golden files by named-field reads (`reflect_shadow_exit.py:117-177`). |
| R3 | V2 | NOT MET | Failure is handled by recording or erroring, not recovery: "a missing argument is a dispatch error", a served-model mismatch is "recorded, not blocked" (section 4 INV-I), and section 1 adds "no ... fallback ladder". No re-dispatch or recovery procedure is given; item 6 is a trigger to change the position, not a runtime recovery. |
| R3 | V1 | MET | Section 2 takes the fallback ladder from the resolution `fallbacks` (`panel.py:677`); section 4 INV-B "A launch failure reaches the merge as a missing reviewer"; section 7 "an attempt that shows a tool outside the allowlist ... is recorded as a violation and never counted as a verified independent reviewer"; M-2 failure path "A narrows to `agent-class`". |
| R4 | V2 | MET | Section 9 "Claude Code behaviour that this repo does not pin (GQ-049, r04 gap 3)"; `muse-ember-1.0` served today unknown; E15 hooks behaviour external and [UNVERIFIED] in this repo; section 7 point 6 "any workspace that cannot export the class map before launch cannot run a gateway panel"; shim failover (E5, E7). |
| R4 | V1 | MET | Point 3 and point 9 (Agent enum, `--restricted` version gate 2.1.248, "behaviour with gateway model ids has only single E2 smoke rows"); point 7 shim failover; section 7 objection "A CLI update can silently turn a read-only reviewer into one that can write"; `--bare` versus host hooks cost (section 5). |
| R5 | V2 | MET | Section 5 item 2 collapse-detector replay over the 15 logs; item 4 read-only pin test; item 5 `SubagentStop` spike; E12 contract fields `identity_source`, `identity_mismatch_suspected`, `reviewer_models` as the existing detection channel. |
| R5 | V1 | MET | Launcher records `model_observed` and tool names seen per attempt (section 2, section 7 control 1); M-2 probe "re-run at install"; M-3 before-and-after resolve diff; M-1 "zero unrecorded swaps". |

## Invariant & Edge Case Coverage

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| I1 | V2 | MET | Empty map: `environments.gateway.launch` is `{}` (`:29`) and "launch None is not one of sonnet, opus, haiku" (E13); maximum: 3-reviewer cap and `validate_reflect_profile` "still rejects Fable and more than 3 reviewers (`panel.py:122-133`)" (section 5 item 3); section 7 point 4 `live7` seven reviewers. |
| I1 | V1 | MET | Maximum: "`_REFLECT_MAX_REVIEWERS = 3` (`panel.py:71-73`)" and the cap kept (section 1, section 2); empty and null: `gateway.launch` is `{}`, "`_check_reflect_resolution` rejects any other `launch`, including `None`" (point 2). |
| I2 | V2 | MET | State crossing component boundaries: class word then `ANTHROPIC_DEFAULT_*_MODEL` then tier alias then shim (E5); "the resolution pins the intended model (`panel.py:674`) independently of any env variable" versus the served model read from the transcript (section 7 point 2); same word, different model per workspace (3.2). |
| I2 | V1 | MET | Class word to `ANTHROPIC_DEFAULT_*_MODEL` alias to shim (point 3); session state needed by C-06 re-ask versus `--no-session-persistence` (section 4, C-06 bullet); resolution `model` versus `model_observed` (section 4 INV-A). |
| I3 | V2 | MET | Guard gaps named: E11 argument omission with no enforcer; E2 ladder "overwrites `MODEL` before the meta file is written"; `launch: None` under `--env gateway` "is an error" (item 3); `permissionMode: plan` and effective tool surface of a `reviewer_profile` child [UNVERIFIED] (E9, item 4). |
| I3 | V1 | MET | Point 6(a) ladder overwrite and 6(b) Bash left open under `bypassPermissions`; point 2 `_check_reflect_resolution` guards only `launch`; point 8 the ceiling is "a template-class rule, not a limit of `resolve`"; `read_only: unproven` marker as an explicit guard. |
| I4 | V2 | MET | Count divergence: reflect ceiling of 3 reviewers equals the 3 class words (E13, E14); E11 three reviewers and three calibrators served one model; section 7 "`live7` has seven models and four class words"; item 6 "more than three (reflect) or four (any) distinct served models". |
| I4 | V1 | MET | Point 4 A-r3 "collapsed three reviewers and three calibrators onto `claude-sonnet-5-5`"; section 4 C-03 bullet "`requested` can collapse because `panel.resolve` drops skipped slots, `panel.py:636-656`"; C-02 `requested` versus `need = Q` fallback left open. |
| I5 | V2 | MET | Interactions: gateway data edit versus `panel_parity` and shadow fence (section 4 INV-L, `reflect_shadow_exit.py:117-177`); hook-exchange families skip subagents under B (section 6, C-12); new agent file versus `make sync-dev` and `verify-sync` blind spot (INV-K row). |
| I5 | V1 | MET | Additive key versus pins `test_review_panel.py:303-307` and D4 (`SKILL.md:320`) (section 2); widened ceiling versus shadow Stage 3 engine rule (section 2, INV-L); `adapter` key versus golden fixtures (section 4 INV-L via golden files); `--bare` versus `--settings` hooks (section 5). |

## Qualitative Summary (dimension subtotals)

| Dimension | Variant 2 | Variant 1 |
|---|---|---|
| Completeness | 5/5 | 5/5 |
| Correctness | 2/5 | 1/5 |
| Structure | 5/5 | 4/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 3/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **Total** | **24/30** | **23/30** |
| **qual_score** (total / 30) | **0.800** | **0.767** |

Pass 2 criterion-level notes for the reconciliation with Pass 1: the verdicts most likely to differ are V2 K3 (MET here), V1 K3 (NOT MET here, rests on the conceded "agent-class is not a launcher" point), V1 S3 (NOT MET, rests on diff:S-001/S-002), V1 R1 and V2 R2/R3 (each rests on whether the risk carries a likelihood or a mitigation or recovery step, not only a severity).

## Edge Case Floor Check

| Variant | Invariant & Edge Case score | Threshold | Status |
|---|---|---|---|
| Variant 2 | 5/5 | >= 1/5 | ELIGIBLE as base |
| Variant 1 | 5/5 | >= 1/5 | ELIGIBLE as base |

Both variants meet the floor; no suspension is needed.
