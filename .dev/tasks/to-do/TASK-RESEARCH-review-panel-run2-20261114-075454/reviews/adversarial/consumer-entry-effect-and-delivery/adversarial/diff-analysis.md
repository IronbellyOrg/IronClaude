# Diff Analysis: Position Paper Comparison (slot C-05, consumer-entry-effect-and-delivery)

## Metadata
- Generated: 2026-11-14
- Variants compared: 2 (Variant A = `variant-1-original.md` = Proposal A; Variant B = `variant-2-original.md` = Proposal B)
- Artifact type: position paper on one conflict (entry, effect and delivery of the unified Review Panel for tasklist and workflow consumers)
- Total differences found: 24 debate points (structural 3, content 12, contradictions 4, shared assumptions promoted 5); the 14 unique contributions are listed but are not scored as debate points
- Categories: structural (3), content (12), contradictions (4), unique (14 across both variants), shared assumptions (7 surfaced: 5 promoted, 2 STATED and not promoted, 0 CONTRADICTED)
- Taxonomy tags: every row carries exactly one level (L1 surface, L2 structural, L3 state-mechanics); the coverage count is in the Summary.
- Total diff points used as the convergence denominator: S 3 + C 12 + X 4 + A 5 = 24

Variant A position: reflect UC-1 stays the only tasklist and workflow entry; the panel enters as a Tier-2 engine behind reflect; advisory at generation time, blocking at the execution gate; call sites unchanged; no plugin copy.
Variant B position: tasklist and workflow call the panel directly through a delegate-only skill with a new flag set and new return-contract keys beside `reflect_status`; a tasklist review may fail at generation time and drive a revise loop; the shipped skills get a plugin copy with a parity pin. B has two forms: B-add (keep the reflect call, add the direct call) and B-replace (swap the call). B states its own safe starting form is B-add with `effect: advisory`.

## Structural Differences

| # | Area | Variant A | Variant B | Severity | Level |
|---|------|-----------|-----------|----------|-------|
| S-001 | Section order | Position, consequence table, evidence (items 1-10), slot consistency, invariants, tests, future effect, objections (4), open items | Position, slot dependence table, consequence, evidence (E1-E13), invariants, tests, future effect, objection (3), what evidence does not decide | Low | L1 |
| S-002 | Unit of position | One position; the three parts (entry, effect, delivery) are argued as one bundle | Two forms (B-add, B-replace) and three separable parts; section 8 item 4 says which part carries which argument | Medium | L2 |
| S-003 | Invariant table verdicts | Verdict per invariant "Preserved", with a closing paragraph listing three endangered items (a)-(c) | Verdict per invariant "Keeps", "Keeps with a cost", "Endangers" (INV-J, INV-G) in the table itself | Low | L1 |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity | Level |
|---|-------|--------------------|--------------------|----------|-------|
| C-001 | Consumer entry | `/sc:reflect --mode pre` stays the single call shape; the panel is a reflect Tier-2 engine (`legacy`, `shadow`, later `panel`) chosen inside reflect | Direct call through a new delegate-only skill (B-add beside reflect; B-replace instead of reflect) | High | L2 |
| C-002 | Effect at generation time | Advisory (bundle or plan ships whatever the verdict); blocking only at the T5 execution gate and the existing structural gates | A tasklist review may fail and drive a revise loop (reviewer side = panel, fixer side = `sc:task` PatchChecklist); workflow plan review advisory until measured, blocking only for `--handoff implement`; B says its safe starting form is advisory | High | L2 |
| C-003 | Plugin delivery | No plugin copy of the panel, `sc-reflect-protocol` or `sc-tasklist-protocol`; plugin delivery of shipped skills is a separate later owner decision | Copy the delegate-only skill, rules, brief file and a read-only reviewer agent into `plugins/superclaude/` with a byte-parity test and a `${CLAUDE_PLUGIN_ROOT}` lookup path; tasklist skill stays out | High | L2 |
| C-004 | Coverage of low-complexity phases | Accepts that depth-0-3 phases map to `--depth quick --tier 1` and never reach the panel (rule D1); states it as a limit and measures the share | Runs the direct call for every phase with `n_tasks > 0`; the depth table selects panel size, not whether the panel runs | Medium | L3 |
| C-005 | Return-contract and closed-enum surface (INV-M) | No new keys; panel verdict mapped onto `status`, `coverage_pct`, `tier_reached`; `reflect_status` closed enum untouched | Workflow contract 1.1 to 1.2 with additive `panel_status`, `panel_report_path` and the effect applied; `reflect_*` keys kept (B-add) or set to `skipped` and null (B-replace), which degrades the readers that surface the reflect result | High | L3 |
| C-006 | Activation path and edit fence | One controlled change at reflect's default, gated by measurement; the skill edit fence (`test_shadow_skill_contract.py`) must be extended in the same change; panel dormant for consumers until then | Edits neither the reflect skill nor `cli/reflect`; does not wait for the Stage 3 / C-04 engine switch | Medium | L3 |
| C-007 | Tasklist review data home | Review runs under reflect's `reflect-pre` lens and the four deviation classes, unchanged | New `tasklist-review` module with the five Stage 7 dimensions as lenses, text anchor with `T<PP>.<TT>` in `refs`; v2 kernel has no tasklist lens (`findings_v2.py:36`) | Medium | L2 |
| C-008 | Relation to Stages 6-10 patch loop | Out of scope; they keep their own blocking semantics; a direct call would add a third loop beside the Stage 7-10 loop and the `--remediate` offer | Moves the reviewer side of Stages 8-10 onto the panel with quorum, ledger and cap; says generation-time blocking already exists there | High | L2 |
| C-009 | Workflow Wave 4 handling | Unchanged: one Skill call at `SKILL.md:89`, advisory rule at `:93` | New `plan-review` module; delegate-only because Will Not at `:107` forbids Task fan-out; advisory until measured; blocking only for `--handoff implement`; edits both the src and plugin copies of the workflow skill | Medium | L2 |
| C-010 | Dependence on adjudicated slots | Relies on C-01 (reflect keeps its engine), C-02 (reflect has no ledger loop; condition stays closed), C-03 condition 3 (reflect keeps `shortfall: visible`); disagrees with none | Takes C-02 whole as a ledger consumer; sets the C-03 `degrade` profile; carries C-02 INV-001/002/003 and C-03 INV-007 as costs A does not carry | Medium | L2 |
| C-011 | Proposed measurement | (1) entry-effect replay of reflect UC-1 shadow versus the direct kernel; (2) routing coverage of depth 0-3; (3) static contract-compat test; (4) call-site non-regression | Static pin list per form; free checks (depth-map share, `prior` compliance); two-arm replay R versus D with loop columns; cost column | Medium | L2 |
| C-012 | Effect on future PR review and rf-qa | Keeps both independent of the consumer entry; no copyable "direct call" precedent; carries forward the plugin gap | Builds the direct-consumer seam first so later consumers inherit "module-declared effect"; effect is module data so a wrong setting is a one-field change | Medium | L2 |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact | Level |
|---|-------------------|--------------------|--------------------|--------|-------|
| X-001 | Is generation-time blocking new? | A direct call "would add a new revise loop beside two existing remediation surfaces" (A section 8, objection 1) | "B does not add generation-time blocking. It already exists in Stages 8-10" and B moves its reviewer feed (B section 8, answer 1) | High | L2 |
| X-002 | What a plugin copy needs to work | "A plugin copy of the panel alone cannot work without `sc-reflect-protocol`, the reviewer agents and the pins" (A section 8, objection 4) | The delegate-only skill plus a read-only reviewer agent is enough; where the CLI is absent the hard gate returns `skipped`, "which is exactly today's plugin result" (B section 8, third objection) | Medium | L2 |
| X-003 | Size of the pin change set | "A predicts zero pin changes outside the reflect fence test" (A section 6 item 4) | B-add keeps all pins but adds a panel line to the unattended-directory pin (`test_workflow_command.py:243-248`), a plugin parity test per added file, and byte-parity edits in both trees; B-replace rewrites `:251-261` (B section 6) | Medium | L3 |
| X-004 | INV-J (S1-S5 repo review rule) | Preserved: A adds no new review text with its own severity rule | Endangers: a tasklist revise loop must reconcile "2 TOTAL passes" with S3 and the static cycle-number pin (OQ-24) | Medium | L3 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Pins a panel result to reflect's 36-test verdict matrix and `contract.py:287-326` degrade rules (single vendor, convergence below 0.80): no second verdict authority | High |
| U-002 | A | Lists the four readers of `reflect_status` (troubleshoot handoff and diagnosability audit, auggie-review, reflect remediation handoff) and the test `test_workflow_vs_task_builder_companion.py:574-599` | High |
| U-003 | A | Points out T5 does not go through UC-1 (`runner.py:540-545` runs the swarm ensemble), so "behind reflect" has two sub-paths | High |
| U-004 | A | Names INV-L (shadow changes no verdict) as released deliberately at the engine switch, to be gated by measurement | Medium |
| U-005 | A | DO4 and U11 text from `git show` (U11 Must: keep today's entry-point semantics unless deliberately changed) | Medium |
| U-006 | A | Notes `tests/tasklist/test_tasklist_cli.py:568-580` P2 non-overlap predicate pins Stage 10.5 text | Medium |
| U-007 | B | E7: the v2 kernel has no tasklist-review lens (`LENSES = ("spec", "reflect-pre", "reflect-post")`) | High |
| U-008 | B | `effect` as module data, not a core constant; a wrong tasklist setting is a one-field change | Medium |
| U-009 | B | Return-contract extension is tolerated by the companion validator (`set(CONTRACT_KEYS) <= set(contract)`, `:1163-1175`) | Medium |
| U-010 | B | Workflow Will Not `:107` ("new agents, Task fan-out") forces a delegate-only skill for any direct call | Medium |
| U-011 | B | Carries the E2 numbers that cut against B (0 of 8 real blocking in every pilot arm; wrong blockers 0, 1, 3; judge 65 versus real 38) and E12 (five #346 plans went on after advisory FAIL results) | High |
| U-012 | B | E13: Stage 2 exit `OVERALL: FAIL (shadow runs 13 of 20)` as context against reflect panel path being a stable base | Medium |
| U-013 | B | Two-arm replay with loop columns (rounds to terminal state, rows ending in `defer` or ESCALATE, patches on non-defects) and a cost column | Medium |
| U-014 | B | Plugin build fact: `build_superclaude_plugin.py` copies `plugins/` as it stands and does not generate it from `src/`; the spec-panel plugin copy is already stale (25-line diff) | Medium |

## Shared Assumptions

Agreement points scanned: both papers accept Stage 10.5 as advisory and T5 as blocking; no consumer passes `--t2-engine`; the plugin ships four skills and lacks reflect and tasklist; DO4 and plugin delivery are owner product decisions; both sit inside C-01, C-02 and C-03; neither position decides C-04, X-15 (Medium vocabulary) or the T5 engine.

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status | Level |
|-------|-----------|------------------|----------------|--------|--------|-------|
| A-001 | Stage 10.5 is advisory and T5 is blocking, and that split is a fact to design around, not a choice of this slot | Both papers | STATED (A section 3 item 2, B E2) | Medium | Documented, not promoted | L2 |
| A-002 | The panel reviews tasklist and plan documents well enough to be consumed at all: the only measured tasklist review path is the spec-panel loop on a derivation set (16 items, 3 packages), and no run exists through either consumer entry | Both papers rely on a working panel for consumer artefacts | UNSTATED as an assumption (both state the evidence gap but design on it) | High | Promoted | L2 |
| A-003 | A nested fan-out (Skill call from inside the workflow or tasklist skill, then reviewer dispatch) completes in headless `--unattended` mode and writes under `nested/<kind>-<n>/` without breaking the closed-enum contract | Both keep a Skill-call shape and the `nested/` convention | UNSTATED | High | Promoted | L3 |
| A-004 | A panel failure, refusal, short panel or skipped slot can be mapped to a status the advisory consumer handles fail-open (`partial`, `failed`, `skipped` with a null path) without any harm to the shipped bundle or plan | A (objection 3 / C-03 section) and B (C-03 `degrade` profile; section 8) | UNSTATED as a shared precondition | High | Promoted | L3 |
| A-005 | In a plugin-only install, workflow Wave 4 already calls a skill the plugin does not ship and ends `reflect_status: skipped\|failed` with a null path | Both papers (A item 9; B E9) | STATED, marked inference, not executed | Medium | Documented; flagged for debate attention | L2 |
| A-006 | The source-tree and plugin-tree pins (`test_workflow_command.py:93-103`, parity tests) keep their current meaning, and `verify-sync` or an equivalent gate stays the only mechanical guard of the plugin tree | Both papers | UNSTATED | Medium | Promoted | L3 |
| A-007 | The owner can make a product decision (DO4, plugin delivery) after this slot reports; any default chosen here is revisable without migration cost beyond the stated pin edits | Both papers | STATED | Low | Documented, not promoted | L2 |

Promoted shared-assumption debate points: A-002, A-003, A-004, A-006 (UNSTATED, 4 points) plus A-005 (STATED but an inference neither paper executed, flagged for debate attention), counted as the fifth. A-001 and A-007 are STATED and excluded from the denominator.

## Summary
- Total structural differences: 3
- Total content differences: 12
- Total contradictions: 4
- Total unique contributions: 14 (6 from A, 8 from B)
- Total shared assumptions surfaced: 7 (UNSTATED: 4, STATED: 3, CONTRADICTED: 0); promoted into debate: 5 (A-002, A-003, A-004, A-005, A-006)
- Convergence denominator: 3 + 12 + 4 + 5 = 24
- Highest-severity items: C-001, C-002, C-003, C-005, C-008, X-001, A-002, A-003, A-004
- Taxonomy coverage (24 scored points): L1 = S-001, S-003 (2); L2 = S-002, C-001, C-002, C-003, C-007, C-008, C-009, C-010, C-011, C-012, X-001, X-002, A-002, A-005 (14); L3 = C-004, C-005, C-006, X-003, X-004, A-003, A-004, A-006 (8). All three levels have points. (A-001 and A-007 carry L2 tags but are not scored.)
- Similarity check: differences exceed 10 percent of comparable items; debate proceeds.
