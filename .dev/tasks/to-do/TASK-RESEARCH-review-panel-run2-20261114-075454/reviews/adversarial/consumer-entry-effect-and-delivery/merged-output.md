<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant A (Proposal A; default model, default persona) -->
<!-- Merge date: 2026-11-14 -->

# Merged Position: consumer-entry-effect-and-delivery (slot C-05)

<!-- Source: Base (original, modified) - status line, merged resolution and reading notes added per the plan overview and Changes 1, 2 and 16 -->
Status: Complete, conditional (adversarial status BLOCKED_BY_INVARIANTS; see Section 11)

Merged resolution. The entry stays `/sc:reflect --mode pre` in this release: workflow Wave 4 and tasklist Stage 10.5 keep the single reflect call, and the panel arrives, if at all, as a reflect Tier-2 engine after a gated switch. The effect is advisory at Wave 4, advisory-blocking at Stage 10.5 (not "advisory": the bundle ships whatever the verdict, but a `needs_human_decision` item halts the stage, an unattended run ends `blocked`, and `--remediate` is a write path), and blocking at the execution gate T5 and at Stages 6-10. For delivery, no panel-only plugin copy is made; plugin delivery is decided as one set (reflect, panel, reviewer agent, CLI availability). The whole resolution is conditional. The debate reached 24 of 24 diff-point agreement, but the invariant probe ended with status BLOCKED_BY_INVARIANTS: 12 probe items are unaddressed (7 HIGH and 5 MEDIUM), and Section 11 lists them with the conditions under which this text holds.

Reading notes. Conflict rows: C-S7, CO-25, CO-35 (synth-06 6.12.1 and 6.12.5; undecidable-conflicts.md slot C-05). Code state: branch `ironbelly/shadow-runs`, commit 50d4d2b9d as read by Proposal B and the fault-finder. Tags from the proposals: [CODE-VERIFIED] = read in source or test at the cited line; [CODE-CONTRADICTED] = code differs from the claim; [UNVERIFIED] = not read or not run. Tags [CHECKED], [INFERRED] and [NOT CHECKED] come from the debate files, and the text names the file. Doc-sourced claims keep the research file named (`r11` = `research/11-consumers-tasklist-workflow.md`, `r12` = `research/12-consumers-spec-review.md`, `r18` = `research/18-repo-constraints-and-branching.md`). "Proposal A" and "Proposal B" are the two source papers; "Sec" and "E<n>" refer to them. The word "Section" refers only to this document. Debate point ids (S-, C-, X-, A-) are from diff-analysis.md and their outcomes from debate-transcript.md. A bare INV-nnn is a probe item of this slot (Section 11). Slot invariants carry letters (INV-M, INV-B). Items of earlier slots are written "C-02 INV-001" and so on. GT means ground truth.

## 1. The position in three separable parts

<!-- Source: Base (original, modified) - restructured into three labelled parts per Change 1; Stage 10.5 wording corrected per Change 2 -->
Headline (kept from Proposal A). The unified Review Panel is a delivery vehicle behind `/sc:reflect`, not a new thing that `sc:workflow` and `sc:tasklist` call. Reflect UC-1 stays the only entry this release. The panel enters, if it enters, as a Tier-2 engine behind reflect (today `legacy`, `--t2-engine shadow` for measurement, later `panel`). Which engine runs inside the call is reflect's decision, made after the depth, tier and rubric decisions. Entry, effect and delivery are separable in code (Proposal B Sec 1 and Sec 8 item 4; debate point S-002, B won, 88%), so each has its own statement below.

### 1.1 Entry (C-001: A wins, 90%)

<!-- Source: Variant B (Proposal B), Section 1 and Section 8 item 4 - merged per Change #1 -->
<!-- Source: Debate (round2-advocate-B.md) - merged per Change #1 -->
Both consumers keep exactly one review call shape, `/sc:reflect --mode pre ...`, with their flags, output directories and return keys untouched. There is no B-replace (swapping the call at `sc-workflow-protocol/SKILL.md:89` and `sc-tasklist-protocol/SKILL.md:1630`): Proposal B's advocate withdrew it, it rewrites the pins at `tests/commands/test_workflow_command.py:251-261`, and it degrades `reflect_status` readers to `skipped`. There is no direct panel call in this release. B-add (keep the reflect call and add a direct call beside it) is not recommended for this release: B's advocate withdrew it in Round 2 because it pays a second review per phase to close a gap nobody has sized. Pre-registered reopen condition: the reach measurement (Section 3a, Section 6.2) shows blocking GT items in phases that never reach the panel. That condition has no working instrument today (INV-005). Proposal B's argument that a direct call is independent of reflect's engine readiness (E13) is weakened: a direct skill would re-implement an orchestrator that shares the shadow-run failure modes ([INFERRED], round2-advocate-B.md). Dormancy is symmetric: a direct skill does not exist either.

### 1.2 Effect (C-002: Hybrid, 90%)

<!-- Source: Debate (invariant-probe.md) - merged per Change #2 -->
<!-- Source: Base (original, modified) - advisory-versus-blocking statement corrected for Stage 10.5 per Change 2 -->
- Wave 4 is advisory. It is one Skill call, it never changes the workflow `status`, and it has no halt path, also under `--unattended` (`sc-workflow-protocol/SKILL.md:89,91,93`, [CHECKED] by the fault-finder).
- Stage 10.5 is advisory-blocking by its own label (`sc-tasklist-protocol/SKILL.md:1646`). The bundle still ships regardless of verdict (`:1640`, `:1646`). A `needs_human_decision` item in the offered remediation halts (`:1640`). Under `--unattended` it resolves as blocked, the item goes in `blocked_question` and the run ends `blocked` (`:1642`).
- Stage 10.5 always passes `--remediate` (`:1630`). That is a write path: headless `--remediate` auto-accepts and authors a corrective artifact (`sc-reflect-protocol/SKILL.md:369-371`), and the plan route calls `sc:workflow-protocol` (`:383-385`), which runs its own Wave 4 reflect. One phase call can nest reflect, workflow and reflect (INV-002).
- Stage 10.5 does not run a revise loop (`:1621-1623`; Section 8 objection 1).
- Blocking stays at T5 (`superclaude reflect run`, fail-closed 0/10/11/2 map) and in the structural gates of the tasklist skill, Stages 6-10 (Section 2).
- Any blocking use of the panel at generation time is a later, separate Stage 7 reviewer-feed change gated on a replay (Section 9a).
- Open: the effect of an engine switch on halt frequency, `blocked` endings, corrective packages and nested runs is unmeasured (INV-001, INV-002). A panel result reaches consumers only through the reflect contract they already read. The panel-to-status map is not defined (INV-011), and whether consumers would see any benefit is open (INV-014 F1 and F2).

### 1.3 Delivery (C-003: A wins, 93%)

<!-- Source: Base (original) -->
No panel-only plugin copy is made, and no plugin copy of `sc-reflect-protocol` or `sc-tasklist-protocol`. The plugin does not carry them today and no test requires it (Section 3 item 9). Plugin delivery of the shipped skills is a separate later decision, taken as one set after plugin CLI availability is known (Section 8 objection 4).

### 1.4 Which part carries which argument

<!-- Source: Variant B (Proposal B), Section 8 item 4 - merged per Change #1 -->
The entry argument stands even if the effect stays advisory. The effect argument stands even if the entry stays on reflect. The delivery argument is the one that cannot be separated from the entry, because only a changed workflow skill forces a plugin edit, and under this resolution the call sites do not change. Proposal B's advocate conceded that delivery has no forcing element once the call sites stay.

## 2. Design consequence for the shared core and the named modules

<!-- Source: Base (original, modified) - consequence table; rows for reflect UC-1, Wave 4, Stage 10.5 and Stages 6-10 rewritten per Changes 2, 5, 8 and 9 -->
<!-- Source: Variant B (Proposal B), Section 4 E7 - lens row merged per Change #7 -->
<!-- Source: Debate (round2-advocate-A.md) - Stages 6-10 row merged per Change #8 -->

| Module or surface | Consequence under the merged position |
|---|---|
| Shared core (`cli/review`) | No consumer-facing API is added for tasklist or workflow. The core exposes what reflect's panel steps already call (`review panel resolve`, `manifest`, cluster, `verify-citations`). No new contract keys and no flag set for workflow or tasklist in this release. |
| reflect UC-1 (`sc-reflect-protocol`) | The only module that gains work. `--t2-engine panel` is enabled in a later stage inside Wave 3/4, and contract 1.8.0 stays byte-identical (additions only under `telemetry:`). Consumers read more than `status`: also `needs_human_decision`, `unmapped_requirements`, `run_id` and `report_path` (`task-builder/SKILL.md:1682`; tasklist `:1640-1642`; workflow `:89`). `coverage_pct` and `tier_reached` are fixed before the engine is read (reflect `SKILL.md:313,738`), so only `status` and the report and gap fields can carry a panel effect (INV-007). The panel-to-status map is not pinned (INV-011), and in every shadow run the legacy builder writes the contract (`scripts/reflect_shadow_exit.py:21-22`), so no map from panel states to `status` has been exercised. A short or refused panel stays inside the closed enum (INV-009, ADDRESSED). |
| `sc-workflow-protocol` Wave 4 | Unchanged: one advisory Skill call at `SKILL.md:89`, advisory rule at `:93`, keys `reflect_status` and `reflect_report_path` (`refs/return-contract.md:16-21`). No halt path (INV-001). The call passes "defaults for every other flag", so depth is `standard` and Wave 4 reaches a panel only on rubric escalation (Section 3a). A later direct module, such as a Wave 4 `plan-review`, is possible and has its own conditions (Section 9a). |
| `sc-tasklist-protocol` Stage 10.5 | Call unchanged: per-phase `/sc:reflect --mode pre --remediate` at `SKILL.md:1630-1636`, verdict handling at `:1640`, gate at `:1646`. The stage is advisory-blocking: the bundle ships regardless of verdict, a `needs_human_decision` item halts, an unattended run ends `blocked` (`:1642`), and `--remediate` is a write path that can nest reflect, workflow and reflect. The effect of an engine switch on these paths is unmeasured and open (INV-001, INV-002). |
| Tasklist T5 post gate and `superclaude reflect run` | Unchanged entry (`runner.py`). A panel engine reaches it only through the reflect contract and `derive_verdict`, never through a second entry. Which engine feeds T5 is slot C-04, not this slot. |
| Tasklist Stages 6-10 (structural gate, Stage 7 validation, patch loop) and `superclaude tasklist validate` | Out of scope for this release. Generation-time blocking already exists in Stages 8-10 (`SKILL.md:1604-1615`): High and Medium findings are blocking, the loop allows at most one re-patch pass (2 total passes), and unresolved blocking findings HALT the skill. A call-site direct call at Wave 4 or Stage 10.5 adds no loop (X-001: Hybrid, 90%). A Stage 7 reviewer-feed swap would change the evidence base of that block, touch the P2 pins and halt strings (`tests/tasklist/test_tasklist_cli.py:568-580`), and is a separate later module (C-008: Hybrid, 90%). |
| Lens for Wave 4 and Stage 10.5 | They use the `reflect-pre` lens. The five Stage 7 dimensions (Drift, Contradictions, Omissions, Weakened criteria, Invented content) apply only to a Stage 7 reviewer feed, which is net-new code with no code home today: `LENSES = ("spec", "reflect-pre", "reflect-post")` (`findings_v2.py:36`) and no `tasklist` or `effect` match in `cli/review` ([CODE-VERIFIED] in Proposal B E7; [CHECKED] in round2-advocate-B.md; not checked by Proposal A's advocate or the fault-finder). C-007: Hybrid, 88%. |
| rf-qa, PR review | Not affected by the entry choice (slots C-10 and C-11). See Section 7. |

[CODE-VERIFIED] workflow Wave 4 call, advisory rule and keys: `src/superclaude/skills/sc-workflow-protocol/SKILL.md:89,93`. Tasklist Stage 10.5 command, handling and gate text: `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1630-1636,1640,1646`. The fault-finder re-read `:1640-1646` and confirmed the `needs_human_decision` halt and the unattended `blocked` state.

## 3. Evidence

### 3.1 Evidence items 1 to 10 (base, with debate corrections)

<!-- Source: Base (original, modified) - items 1, 2, 3, 4, 7, 8 and 9 corrected per Changes 2, 4, 5, 6 and 10; items 5, 6 and 10 unchanged -->
1. Neither consumer reaches panel code today. [CODE-VERIFIED] The search `t2-engine|t2_engine` over `src tests scripts docs plugins` matches 8 files (reflect `SKILL.md`, `refs/reviewer-spec.md`, `cli/review/manifest.py`, `cli/review/manifest_cmd.py`, `scripts/reflect_shadow_exit.py`, `tests/review/test_review_manifest.py`, `tests/cli/reflect/test_shadow_skill_contract.py`, one reflect-cards fixture); none is a workflow or tasklist file (Proposal B E5 counts 47 hits). With the default `legacy` "the panel code is never called" (`src/superclaude/skills/sc-reflect-protocol/SKILL.md:87,311`), and `--t2-engine panel` is rejected until Stage 3 (`:87`). So reflect is the single choke point for engine selection, and consumer calls reach the panel only after reflect's default flips (the fault-finder checked this and it holds). Reach also depends on depth, tier and rubric (rule D1; Section 3a). The earlier wording "can be switched on for both consumers with zero edits to their call sites" is withdrawn (Section 10).
2. The advisory and blocking split is already how the products are built, with one correction. [CODE-VERIFIED] Stage 10.5 "the bundle **still ships** (audit-first)" (`sc-tasklist-protocol/SKILL.md:1640`) and "ships regardless of verdict (advisory-blocking)" (`:1646`). Workflow: "never change the workflow `status` because of them" (`sc-workflow-protocol/SKILL.md:93`). The one blocking edge of Stage 10.5 is a `needs_human_decision` item in the offered remediation, which halts (`:1640`) and ends an unattended run as `blocked` (`:1642`). Blocking review lives in tasklist Stage 6 (no write on a failing check) and the Stage 8-10 patch loop capped at 2 total passes (`:1604-1615`, read by both Round 2 advocates, [CHECKED]), and in T5 (`:1170-1179` per r11 2.3, [UNVERIFIED] here).
3. A pinned interface that other readers use stays untouched. [CODE-VERIFIED] The closed enum `reflect_status: success, partial, failed or skipped` and `reflect_report_path` are at `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:16-21`. The test `tests/cli/eval/test_workflow_vs_task_builder_companion.py:574-599` requires both keys, accepts `skipped` only with a null path and rejects `"bogus"`. Readers are at least the four skill readers (troubleshoot remediation handoff `refs/remediation-handoff.md:34,112,119`, troubleshoot diagnosability audit `refs/diagnosability-audit.md:252`, auggie-review `SKILL.md:348`, reflect `refs/remediation-handoff.md:81-84`), one closed-enum validator (`scripts/eval_workflow_vs_task_builder.py:1166-1175`) and the tests (INV-008). No Python module under `src/superclaude/cli` reads the key (r11 5.3, [CODE-VERIFIED] there by Grep).
4. The pins this resolution keeps are the pins B-replace must rewrite. [CODE-VERIFIED] `tests/commands/test_workflow_command.py:243-261` pins the Wave 4 order, the exact call string `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md`, `nested/reflect-` plus `--unattended` on one Wave 4 line, and both `reflect_*` keys in the ref. `tests/tasklist/test_tasklist_cli.py:568-580` pins the P2 versus Stage 10.5 non-overlap predicate. B-add rewrites no test pin (`:246-248` is an `any(...)`, `:255-258` is a substring test) but needs unpinned edits (X-003: Hybrid, 85%; Section 9a).
5. The panel's verdict is already constrained by a pinned map that the execution gate depends on. [CODE-VERIFIED] `tests/cli/reflect/test_verdict_mapping.py` has 36 `def test_` (Grep count). `src/superclaude/cli/reflect/contract.py:287-288` degrades on a single vendor unless `--allow-single-vendor`, and `:317-326` degrades any convergence below 0.80. Tasklist T5 uses the same 0.80 (`sc-tasklist-protocol/SKILL.md:1171,1179` per r11 4.3, [UNVERIFIED] here). Keeping the panel inside reflect means a panel result is judged by the same map, with no second verdict authority. The 36-test matrix is necessary but not sufficient (INV-011; Section 5).
6. The code-driven gate T5 does not go through UC-1. [CODE-VERIFIED] `src/superclaude/cli/reflect/runner.py:540-545` runs `run_tier2_ensemble(config)` for depth standard or deep in production and `derive_verdict` after either path (`:573-580`). "The panel behind reflect" therefore has two sub-paths: UC-1 (skill, panel-capable through `--t2-engine`) and UC-2 and T5 (wrapper, swarm ensemble, no `--t2-engine`). This resolution fixes the entry and does not decide the T5 engine (slot C-04).
7. Quick-depth phases never reach a panel. [CODE-VERIFIED] Rule D1 at `sc-reflect-protocol/SKILL.md:317`; depth map 0-3 to `--depth quick --tier 1` at tasklist `SKILL.md:1677-1681` per r11 2.2 [UNVERIFIED here]. The reach limit is wider than quick phases alone; see Section 3a.
8. Skill edit fence. [CODE-VERIFIED] (read, not run) `tests/cli/reflect/test_shadow_skill_contract.py:42-49` pins the `### 9.1 Stable contract (contract_version: 1.8.0)` block to `git show HEAD:<skill>`; `:52-75` allows working-tree changes only under sections `### 3.1`, `### 4.3a`, `### 5.4`, `### 9.2`; `:78-98` forbids new `src/superclaude` strings in the skill directory. Moving from shadow to engine `panel` edits Wave 3/4 text outside that allow-list. Corrected reading from the debate: these three tests diff against `HEAD` (`:46-48,53`), so they are working-tree guards that pass trivially on a clean committed tree ([INFERRED]; no advocate ran them; the fault-finder read them, INV-012). The earlier statement "this test must be changed in the same change" is withdrawn. The content pins in the same file are standing because they read the committed text (`:146-238`: exactly three brief sections, the shadow-section strings, the calibrator line appearing once, the shadow-step strings, the manifest recipe). A Stage 3 edit that restructures the shadow steps, adds panel steps next to them or edits the calibrator line fails them on a clean tree, so the Stage 3 change must update them (INV-012).
9. Plugin delivery. [CODE-VERIFIED] `plugins/superclaude/skills/` holds `confidence-check`, `sc-implement-protocol`, `sc-recommend`, `sc-workflow-protocol`. `plugins/superclaude/agents/` holds no `rf-*` agent, no `reflect-reviewer` and no `evidence-validator`. There is no `sc-reflect-protocol` and no `sc-tasklist-protocol` (r18 section 7). `plugins/superclaude/commands/` has `reflect.md` and `workflow.md` and no `tasklist.md`. The wheel ships whatever is tracked under `plugins/` (`pyproject.toml:78-87`). Parity pins cover only `sc-recommend`, commands `help`, `recommend`, `workflow` and `implement` (`tests/commands/test_routing_plugin_parity.py:29-47`), and the byte-parity test `test_workflow_command.py:93-103`, which compares the `*.md` files of one skill and one command. No test requires a plugin copy of a new panel (r18 7). `scripts/build_superclaude_plugin.py` copies `plugins/superclaude/{agents,commands,hooks,rules,scripts,skills}` as they stand into `dist/` (Proposal B E9; [CODE-VERIFIED] for the copy loop, the Makefile claim [UNVERIFIED]). The plugin is already a thin front over an installed tree: the plugin workflow skill points at `~/.claude/CODEGRAPH.md` (`:27`) and `~/.claude/WORKER-CONTRACT.md` (`:53,:91`), and `plugins/superclaude/commands/reflect.md:142` points at `~/.claude/skills/sc-reflect-protocol/SKILL.md` ([CHECKED] in round2-advocate-B.md). In a plugin-only install Wave 4 already calls a skill the plugin does not ship, and by the rule at `SKILL.md:93` that ends as `reflect_status: skipped` or `failed` with a null path (shared inference from verified facts, not executed; A-005 below). What a plugin copy would deliver, in three cases (round2-advocate-B.md): (a) CLI absent: the skill's hard gate returns `skipped`, the same as today, nothing gained; (b) CLI present and `superclaude install` run: `~/.claude/skills` already holds the skill, so the copy is redundant; (c) CLI present, install not run, plugin installed: the only case with value, and it also needs a reviewer agent copy and `~/.claude/` core refs that the plugin lacks. Whether case (c) exists is [NOT CHECKED]. CLI availability in a plugin-only install and `verify-sync` coverage of `plugins/` are both unchecked. Each added plugin file needs its own parity test (A-006). "A plugin copy cannot make a plugin install worse" holds; "a plugin copy delivers" is unshown.
10. The E2 study never ran its loop through the consumer entries. DO4 text (`git show 6c0984326cbb8fb06c4a36065de58b171d3f8175:.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification-run2.md`, line 301) lists both options with decider "Owner plus the unification session"; U11 (line 436) is a Must: "Keep today's tasklist-review entry points' semantics unless deliberately changed". [CODE-VERIFIED by r11 5.1 via `git show`; not re-read beyond r11.] The E2 evidence is neutral on the entry, and U11 favours the reflect entry as the default.

Doc claim tagged [CODE-CONTRADICTED] that this position must not rely on: run-1 D14, "No tasklist review step exists in `sc-tasklist-protocol` or `sc-workflow-protocol`", is contradicted by `sc-workflow-protocol/SKILL.md:89` and `sc-tasklist-protocol/SKILL.md:1630` (r11 5.2; synth-06 DOC-2). The narrower fact, that neither skill calls `superclaude review` or passes `--t2-engine`, is [CODE-VERIFIED] (item 1).

### 3.2 Counter-evidence carried from Proposal B (items 11 to 13)

<!-- Source: Variant B (Proposal B), Section 4 E11, E12 and E13 - merged per Change #14 -->
11. E2 numbers that cut against any blocking effect (Proposal B E11, kept because B carried them). In the three pilot arms real blocking was 0 of 8 on the defect-rich packages in every arm, and wrong blockers were 0, 1 and 3. Judge-blocking was 65 against real blocking 38 over 71 valid rows (the judge's "blocking" is mis-defined). The default `ember + 2x luna` found 1.83 of 14 with 0.17 real blocking and 0.83 of 2 control items (research/08 G1, G4, G10, [RECOMPUTED] there, [UNVERIFIED] here). These are any-blocking union results on round 1 only; no multi-round ledger exists.
12. Advisory reflect results exist on real workflow plans and did not stop them (Proposal B E12). The five #346 plans had reflect UC-1 results of FAIL with 4 blocking, partial with 1, partial with 2, FAIL with 7, and "3 HIGH + 15 MEDIUM". All five went on to implementation: four report complete builds, and the fifth (minfix) stalled on API errors (research/scope/12 D3, lines 172-177, [UNVERIFIED] here as to cause). This shows the advisory effect is exercised, not that blocking would have been better.
13. The reflect panel path is not yet a stable base for a consumer (Proposal B E13). The Stage 2 exit reads `OVERALL: FAIL (shadow runs 13 of 20)`, with EV-1 failures in 8 of 13 runs that are presence, name or equality defects, none a review-content failure (synth-05 6.8, from research/06 section 6; [UNVERIFIED] here). This is context for the entry choice, not a verdict on the engines (slot C-04).

## 3a. Reach behind reflect

<!-- Source: Variant B (Proposal B), Section 4 E4 - merged per Change #3 -->
<!-- Source: Debate (round2-advocate-A.md, round2-advocate-B.md, invariant-probe.md) - merged per Change #3 -->
Debate point C-004: Hybrid, 88%. Proposal B is right on the reach fact, and the fact is narrower than quick phases alone. Proposal A's earlier strength "low-complexity phases are the lowest risk" holds only for the quick band (round2-advocate-A.md).

### 3a.1 The reach chain

1. Without `--t2-engine` the engine is `legacy`, so consumer calls reach the panel only after reflect's default flips (`sc-reflect-protocol/SKILL.md:87`; the fault-finder checked this and it holds).
2. Reflect's default `--depth` is `standard` (`src/superclaude/commands/reflect.md:98`), and workflow Wave 4 passes "defaults for every other flag" (`sc-workflow-protocol/SKILL.md:89`). Workflow therefore reaches a panel only on rubric escalation ([CHECKED] by both Round 2 advocates).
3. A rubric stop never reads the engine, and with `legacy` a rubric escalation never calls the panel (`sc-reflect-protocol/SKILL.md:317,327-328`).
4. Tasklist reaches the panel only for forced-deep phases (`n_cpo >= 1`, `n_strict >= 2` or score >= 10; `sc-tasklist-protocol/SKILL.md:1677-1685`) and for rubric escalations of standard phases. Score 0-3 maps to `--depth quick --tier 1` and never reaches the panel. One STRICT task already scores >= 4 and is `standard` (INV-006).
5. `--budget-remaining` N < 65 downgrades rubric escalations to Tier 1, so the panel is never called (`sc-reflect-protocol/SKILL.md:331-333`). This is a second reach limiter that neither Round 2 file listed (INV-006).
6. Populations with no reflect run at all: `n_tasks == 0` phases (`sc-tasklist-protocol/SKILL.md:1686`), `--no-reflect` and `--dry-run` (`:1644`), workflow `skipped` or `failed` (`sc-workflow-protocol/SKILL.md:93`), and plugin-only installs (INV-006).
7. Nested runs on the `--remediate` plan route add panel runs that a reach count of "forced-deep phases and rubric escalations" undercounts (INV-002).

### 3a.2 What is not known

The reach share is unsized. Proposal B's free check found four tracked `depth-map.yaml` files outside `.dev/tasks/`. Three are sandbox fixtures, one in an older schema that cannot be mapped, and one has every verdict `SKIPPED`. The 8 mappable phases are 4 quick, 2 standard and 2 deep (one deep is an override): n = 8, mostly synthetic, too small to size the gap ([CHECKED] in round2-advocate-B.md). The 80 `.dev/reflect/pre-*` runs counted there (62 tier 2, 16 tier 1, 2 null or empty) cannot be turned into a consumer share, because the consumer calls cannot be told apart. The denominator rule for the share is unset (INV-006), and the instrument gap is INV-005 (Section 6.6).

### 3a.3 The remedy and what the probe found about it

The agreed remedy order is: measure the share; if it matters, fix it in depth policy (a call-site depth flag or the Stage 10.5 table) before adding a second entry. The claim that the depth-policy remedy is "cheaper" and "pin-safe" is unsupported (Section 10). The fault-finder found:
- INV-003 (HIGH, UNADDRESSED). The remediation route follows the requested `--depth`, not the tier reached (`sc-reflect-protocol/SKILL.md:363,366,369`; pinned by `tests/cli/reflect/test_remediation_route_table.py:26-39`). Widening the forced-deep set moves phases from the plan route to the MDTM route, which is skipped and recorded when unattended. At Wave 4 a forced `--depth deep` forces Tier 2 under the legacy engine today (`:329`, D3 `:319`), so the remedy changes cost and wall-clock before any panel exists.
- INV-004 (MEDIUM, UNADDRESSED). A depth flag at Wave 4 passes the substring pin `test_workflow_command.py:255-258` only if it is appended after `<id>.md`. The byte-parity pin `:93-103` requires the same edit in `plugins/superclaude/skills/sc-workflow-protocol/SKILL.md:89`. The phrase "defaults for every other flag" (`workflow SKILL.md:89`) becomes false and is unpinned. The return contract is unaffected.
- The fault-finder also noted drift: tasklist `:1640` says reflect "offers a Tier-3 `task-builder` remediation", while reflect routes the standard and quick depths to the workflow plan route (`sc-reflect-protocol/SKILL.md:366`).

## 4. Consistency with the adjudicated slots C-01, C-02, C-03

<!-- Source: Base (original, modified) - slot bullets kept; item names prefixed with the slot to avoid clashing with probe ids; C-03 status sentence qualified per Change 5 -->
Proposal A read the three `ADJUDICATION-RESULT.md` files. The merged position is consistent with all three, depends on one condition in each, and disagrees with none (C-010: A wins, 94%).

- C-01 (core-shape-and-finding-contract): winner is Variant B as base (a thin shared contract with per-module engines), "no change to `cli/reflect`", reflect stays on the v2 kernel, unknown keys open. The consumer entry is a module concern and reflect keeps its own engine and call shape. Dependency: reflect stays on its own engine, so that the panel selected by `--t2-engine panel` can be the v2 kernel without forcing tasklist or workflow onto the v1 anchor loop. The withdrawn Variant A parts of C-01 (locator-agnostic `annotate`, citations in ledger rows) are not needed. C-01 INV-020 ("no change to `cli/reflect`" means the reflect pipeline's results do not change) is not settled here either; the panel's contract output must pass the 36-test matrix, which is necessary, not sufficient (INV-011).
- C-02 (ledger-clearing-and-verdict-authority): winner is Variant B as base with A's quorum gate; explicit per-row verification. The result states "No effect on reflect holds for this slot only (A-004, QUALIFY); it reopens if the unified panel makes reflect a consumer of the review ledger." This resolution keeps that condition closed: reflect UC-1 is a single pass with no review ledger and no re-review round (Wave 4 and Stage 10.5 run once; r11 1.1, 2.2), and the panel behind reflect is merged by reflect's Wave 4 debate (`SKILL.md:311`), not by `review-ledger/1`. The C-02 rewrite of ledger pins (`tests/review/test_review_ledger.py:193-217`) is independent of the consumer entry. If a later design routes reflect's panel rounds through the ledger, the C-02 condition reopens.
- C-03 (merge-verdict-policy-and-quorum): winner is Variant A as base; any-blocking union as a pluggable policy; quorum as a merge-time refusal; fail-closed "only in profiles that set `degrade` (spec review). Reflect keeps `shortfall: visible`, `derive_verdict`, its 36 tests and the two shortfall pins" (condition 3). The consumers get reflect's verdict semantics, not the spec-review refusal (exit 12). D3 forces `status: partial` (never `success`) when the effective engine is `panel` (`sc-reflect-protocol/SKILL.md:319-320`, INV-009 ADDRESSED); the map from other panel states to `status` is unpinned (INV-011). Dependency: condition 3 stays as stated. If the C-03 quorum refusal were applied to the reflect profile, Wave 4 would see a refusal where its contract only knows `skipped` or `failed`, and the call would map to `failed` with a null path (`SKILL.md:93`), an acceptable fail-open outcome for the advisory Wave 4 step. C-03 INV-007 and C-03 INV-006 (HIGH, unaddressed) concern the spec-review profile and do not touch this position.

<!-- Source: Variant B (Proposal B), Section 2 - merged per Change #12 -->
Reverse view (Proposal B Sec 2; C-010). A later direct module would be a consumer of the review ledger. It would take C-02 whole and carry C-02 INV-001 (`need` can be 0), C-02 INV-002 (a regressed non-blocking row in no brief list), C-02 INV-003 (exit-code-only callers), and C-03 INV-007 (`requested` can collapse to 1 when `panel.resolve` drops skipped slots). It would also depend on the C-01 hybrid, where the tasklist module runs on the v1 engine and ids cluster through the `T<PP>.<TT>` token. Reflect UC-1 carries none of these conditions. Proposal B's advocate conceded this.

<!-- Source: Base (original) -->
Not adjudicated yet and relevant: C-04 (engine composition) decides which engine feeds T5 and `--t2-engine panel`. The entry decision does not depend on its outcome, but "blocking at the execution gate" is only as strong as the engine C-04 selects, because `derive_verdict` reads engine-produced fields (`contract.py:287-326`). C-15 (tasklist Medium vocabulary) is independent: Stage 10.5 and reflect use their own labels either way.

## 5. Invariants: per-row verdicts

<!-- Source: Variant B (Proposal B), Section 5 - merged per Change #4 -->
<!-- Source: Base (original, modified) - rows rewritten with Keeps, Keeps with a cost or Endangers; INV-M and INV-K corrected per Changes 4 and 5 -->
Invariants are from synth-06 6.12.0. The slot lists INV-M, INV-B (HIGH), INV-N, INV-K, INV-J (MEDIUM), and they come first. The verdict column replaces the earlier all-"Preserved" column (debate point S-003, B won, 85%).

| Invariant | Verdict | Basis |
|---|---|---|
| INV-M `reflect_status` and `reflect_report_path` closed enum and the headless output directories (HIGH) | Keeps with a cost | No key is added beside them in this release. `test_workflow_vs_task_builder_companion.py:574-599`, `test_workflow_command.py:243-261`, at least the four skill readers, the closed-enum validator `scripts/eval_workflow_vs_task_builder.py:1166-1175` and the tests all stay valid (INV-008). A short, refused or failed panel cannot push `reflect_status` outside the enum (INV-009). Cost: the panel-to-status map is unpinned (INV-011), and consumers read more than `status` (INV-007). Additive keys with `contract_version` "1.1" would be safe at the three consumer-side readers (INV-014 enumeration). |
| INV-B 36-test verdict matrix and the `derive_verdict` map (HIGH) | Keeps with a cost | The matrix is not edited. A panel contract must carry `merge_method`, `adversarial_convergence_score >= 0.80`, diversity values and real booleans (`contract.py:287-326`). Cost: the matrix does not test the closed panel-lint rules (`panel_lint.py:272,288-298,311-334,360-365`: L1, L2, L3, L6 and EV-1), and the panel's cluster-and-union merge produces neither `adversarial_convergence_score` nor `merge_method` (INV-011). |
| INV-N plugin mirror parity pins | Keeps | No file under `plugins/` is changed, so the pinned pairs (`test_routing_plugin_parity.py:29-47`, the spec-panel pins) are untouched. A call-site depth flag at Wave 4, or a later module, would need edits in both trees and a parity test per added plugin file (INV-004; A-006). The spec-panel plugin copy is already stale (25-line diff, research/12 1.3, [UNVERIFIED]). |
| INV-K sync-dev, verify-sync, lint-architecture, layout traps, reflect edit fence | Keeps with a cost | The three diff-based fence tests are working-tree guards. The content pins in the same file are standing, and the Stage 3 edit must update them (INV-012). The remediation route table test changes if depth policy changes (INV-003). The plugin tree is outside the `verify-sync` gate ([UNVERIFIED], research/18 2), so only a new parity test would protect an added plugin file. |
| INV-J repo review rule S1-S5 (binary blocking, Medium is a warning, at most 2 fix cycles) | Keeps now; Endangers for a later revise loop | This release adds no new review text with its own severity rule, and Stage 10.5 keeps its own labels (C-15 decides Medium). The scan covers tracked files under `src plugins commands agents skills` (r18 F10). A later revise loop must reconcile "2 TOTAL passes" (`sc-tasklist-protocol/SKILL.md:1604`) with S3 and with the static pin that forbids other cycle numbers outside `sc-implement-protocol` (research/12 section 4, [UNVERIFIED]). Whether that equals 2 fix cycles is the open OQ-24 ([UNVERIFIED]). X-004 (Hybrid, 82%): a reviewer swap inside the existing P2 loop adds no cycle number; a new loop would. |
| INV-A reflect contract 1.8.0 names and `merge_method` pair | Keeps | The panel's output nests under `telemetry:`, and the `### 9.1` block is pinned to HEAD (`test_shadow_skill_contract.py:42-49`). Enabling engine `panel` edits `### 4.3a` and Wave 3/4 text. The workflow return contract is a different file at its own version. |
| INV-C, INV-D v1 grammar and `review-ledger/1` | Keeps | Neither is touched. Reflect UC-1 has no review ledger (Section 4). A later direct module would be a ledger consumer. |
| INV-E `pr_submit` and fork-only checks | Keeps | Not touched. |
| INV-F installed-path rule | Keeps | No primitive is added. A later new skill and plugin copy would name installed paths with a plugin fallback, and `tests/skills/test_review_brief_placement.py:68` forbids `src/superclaude` in the rules file (research/12 2.1, [UNVERIFIED]). |
| INV-G blind, mechanically read-only reviewers | Keeps with a cost | The panel's reviewers are the mechanically read-only kind the core supports. Any plugin copy would hold the invariant only if its reviewer agent is the read-only kind, and the plugin has no read-only reviewer agent today (Proposal B E9). |
| INV-H no document text in telemetry | Keeps | Not touched. New module strata are registered by the module (decided at C-S10). |
| INV-I fail-closed | Keeps | T5 stays fail-closed. The advisory outputs fail open by design (`sc-workflow-protocol/SKILL.md:93`). The Stage 10.5 halt is not a fail-open path (INV-001). A blocking feed must not fail open (Section 9b, A-004). |
| INV-L shadow mode changes no verdict | Keeps with a cost | Holds until the stage that enables `panel`, where it is released deliberately after the measurement in Section 6. Flipping to `shadow` first doubles Tier-2 reviewer spend on every consumer escalation (INV-010). |

Endangered by this resolution: (a) reach, because the panel is reached only on forced-deep phases and rubric escalations (Section 3a); (b) INV-L at the engine switch; (c) the INV-K content pins at the engine switch. For a later module only: INV-J and INV-G. None is a violation of a pinned invariant in this release; each is a precondition of a later stage.

## 6. The test or measurement that would show it right or wrong

<!-- Source: Base (original, modified) - items 6.1 to 6.4 of the base merged with Proposal B's measurement per Change 11 -->
<!-- Source: Variant B (Proposal B), Section 6 - merged per Change #11 -->
<!-- Source: Debate (round2-advocate-A.md, round2-advocate-B.md, invariant-probe.md) - merged per Change #11 -->
Debate point C-011: Hybrid, 85%. Section 6.6 lists the gaps in the instrument; the measurement is the decision mechanism of the whole resolution and has no working instrument today (INV-013).

### 6.1 Entry-effect replay (two arms)

The E2 package set with GT: 3 files, 16 items, 10 GT items of which 5 blocking on designSpec (synth-05 6.9, r08; [UNVERIFIED] here as a count), plus at least one held-out package (E2 has none, research/08 G3).
- Arm R is a real Wave 4 or Stage 10.5 call: reflect UC-1 `--mode pre` with the panel as Tier-2 engine as it stands after the C-04 work. It must not be a hand-run of reflect.
- Arm D is the path E2 already measured (spec-panel loop plus `superclaude review`), not a module. No `tasklist-review` module or `effect` field is a precondition (round2-advocate-B.md).
- Columns: the research/08 per-arm columns (found, real blocking in implement, wrong blockers, control found), loop columns for arm D only (rounds to a terminal state; rows that end in `defer` or ESCALATE with no human exit; patches applied to rows that are not GT items), and a cost column (tokens and elapsed per phase; E2's default panel is about 64k tokens per package run, research/08 G10, [UNVERIFIED], and a bundle runs N phases).
- Proposal A's rule: the reflect entry is wrong on outcomes if the direct path finds materially more blocking GT items per cost and the miss in arm R is not explained by depth routing. Proposal B's rule: its blocking effect is shown wrong if arm D's wrong blockers drive a majority of packages to ESCALATE or to a patch on a non-defect, or if arm D's real-blocking catch is below arm R's; it is shown right on effect if arm D catches the real-blocking items that arm R records as non-blocking or advisory and the loop converges without a human exit on the clean control. No numeric threshold is registered (Section 6.6).

### 6.2 Reach share and routing coverage

Count the share of phases and plans that reach the panel. Proposal A's version counted phases whose `COMPLEXITY_SCORE` maps to `--depth quick --tier 1`. Proposal B's free check counted score 0-3 phases in committed `validation/reflect-pre/depth-map.yaml` (the audit file named at `sc-tasklist-protocol/SKILL.md:1652`, [UNVERIFIED] that committed copies exist). Proposal B's Round 2 amendment: the share must come from reflect contracts (`tier_reached`, effective engine) of real Wave 4 and Stage 10.5 calls, and a numeric reopen threshold must be registered before the first run (B asked; A did not answer). If the share is high and those phases carry blocking GT items, the remedy is chosen between a depth-policy change and a direct call, with the side effects in Section 3a.3.

### 6.3 Contract-compat test (static)

Assert that a panel-produced reflect contract passes `derive_verdict` with the same exit codes as the 36-test fixtures, and that `reflect_status` stays in the closed enum for every panel outcome (success, partial on a short panel, failed, skipped). This is necessary, not sufficient, until the panel-to-status map is defined (INV-011).

### 6.4 Call-site non-regression and headless smoke run

Run `tests/commands/test_workflow_command.py`, `tests/tasklist/test_tasklist_cli.py`, `tests/cli/eval/test_workflow_vs_task_builder_companion.py` and `tests/cli/reflect/test_verdict_mapping.py` at the engine switch. Expected: no consumer-side test pin changes; reflect-owned tests change at Stage 3 (the content pins, and the remediation route table if depth policy changes). The earlier "zero pin changes" was a prediction, not a run (Section 10). A headless smoke run is required on either route, because headless Tier 2 is unrun and the companion eval cannot run it (A-003).

### 6.5 Free check for a later module

Count `prior` line compliance by ledger id in existing re-review reports (C-02's M2). This matters only for a later direct module (Proposal B Sec 6).

### 6.6 Instrument gaps (open)

1. No GT scorer exists (INV-013): `scripts/reflect_shadow_exit.py:1-35` checks parity, MALFORMED rows, panel lint, a `derive_verdict` replay and EV-1 rates only. GT holds only defects that surfaced during implementation, so a novel true defect scores as a wrong blocker. Real blocking was 0 of 8 in every pilot arm, so a difference of one item is the whole signal.
2. The only aggregator globs `pre-*/panel/manifest.json` of shadow runs (`scripts/reflect_shadow_exit.py:209,215`). It cannot see phases that never reach the panel, and it cannot see tasklist consumer output directories (`validation/reflect-pre/phase-<P>/`, `nested/reflect-<n>/`) (INV-005).
3. The companion eval pool denies Bash, Agent, Task and `mcp__*` (`scripts/eval_workflow_vs_task_builder.py:66-67`), so it cannot run a reviewer fan-out under either route. No replacement runner is assigned, and the "held-out package" labelling has no owner.
4. No engine selector exists for arm R (INV-010). The default is prose in three places (`sc-reflect-protocol/SKILL.md:87,311,464-465`), there is no `cli/reflect` reader of the flag, no `--t2-engine` row in `commands/reflect.md`, and no environment selector. Without a call-site edit or a global flip, arm R is a hand-run.
5. The denominator rule for the reach share is unset (INV-006).
6. No numeric reopen threshold is registered (Proposal B asked, Proposal A did not answer).

Net, per the probe: the consensus resolves every disputed point to "the replay decides", while the replay has no instrument, no labeller, no selector and a tiny n (INV-013).

## 7. Effect on future PR code review and rf-qa replacement

<!-- Source: Base (original, modified) - direct-call sentence replaced and module-declared effect added per Change 12 -->
<!-- Source: Variant B (Proposal B), Section 7 - merged per Change #12 -->
Neither PR review (slot C-10) nor the rf-qa and `/task` gate (slot C-11) is affected by the consumer entry. They reach the shared core through their own modules, and neither reads `reflect_status`. The panel's reviewers for those modules are the mechanically read-only kind that the core already supports (INV-G), so the rf-qa first step at the `/task` phase gate is not constrained. Synth-05 6.8 records that neither reflect engine option blocks PR review or rf-qa.
1. No direct-call pattern is added by this release, so PR review and rf-qa each define their own call shape, as C-10 and C-11 assume. PR review enters as a reviewer adapter that emits `Finding` objects, and the rf-qa replacement "starts by making the `/task` gate call a panel core, not by touching 7 skills" (research/13, [UNVERIFIED] here). Module-declared effect is the rule for later direct consumers (C-012: Hybrid, 82%): `effect` is module data, so a wrong setting is a one-field change. None is added here.
2. The "no plugin copy" decision leaves the plugin without `rf-qa`, `rf-qa-qualitative`, `reflect-reviewer`, `pr_submit`, `auggie-review` and the review skills. A later rf-qa replacement that wants plugin delivery meets the same missing-skill gap and must schedule the mirror work explicitly (r12 5.3 item 148; research/13 P14 and R11). This is a cost carried forward, not created here. Proposal B's risk remains: if a blocking effect is wrong for tasklist, rf-qa's fix loops would inherit a miscalibrated precedent.

## 8. The strongest objection and the answer

### Objection 1 (the strongest)

<!-- Source: Base (original, modified) - answer rewritten per Changes 2 and 8 -->
"Behind reflect the panel stays advisory at generation time, so a defect found by the panel never changes the tasklist or plan that ships. The owner wants the panel to improve the bundle, and the E2 loop (review, revise, re-review) can only do that through a direct call. Reflect UC-1 is also a single pass with no cap and no ledger, so the panel's loop value is discarded."

Answer. The generation-time effect is already the product's choice, not a limit of the entry. Wave 4 is advisory with no halt path and "never edits the plan from findings" (`sc-workflow-protocol/SKILL.md:93`). Stage 10.5 is "advisory-blocking": the bundle ships regardless of verdict, a `needs_human_decision` item halts, an unattended run ends `blocked`, and `--remediate` is a write path (`sc-tasklist-protocol/SKILL.md:1640-1646`; INV-001, INV-002). Generation-time blocking with a revise loop already exists in Stages 8-10 (`:1604-1615`; X-001: Hybrid, 90%). A call-site direct call at Wave 4 or Stage 10.5 would add no loop, so the earlier wording "a direct call would add a new revise loop" is replaced. A Stage 7 reviewer-feed swap would change the evidence base of the existing block, touch the P2 pins (`tests/tasklist/test_tasklist_cli.py:568-580`) and halt strings, and is a separate later module after a replay (Section 9a). It is conceded that UC-1 itself is one pass. The fix path stays where it is (`sc:task`, never the orchestrator), with reflect's existing Tier-3 hand-off for remediation. Open: whether an engine switch changes how often Stage 10.5 halts or ends `blocked`. `needs_human_decision` is true when `grounding-gaps.yaml` is non-empty (`sc-reflect-protocol/SKILL.md:858`), so it can; the size is unmeasured ([INFERRED], fault-finder).

### Objection 2

<!-- Source: Base (original, modified) - reach statement narrowed per Change 3 -->
"Quick-depth phases (score 0-3) and `--no-reflect` never reach the panel, so the consumers get a panel only on some phases." Answer: true, and the reach is narrower than that (rule D1, `sc-reflect-protocol/SKILL.md:317`; tasklist `:1644`; Section 3a). It is the existing cost and coverage policy of Stage 10.5. The share is unsized, and Section 6.2 shows whether it matters. If it does, the remedy is chosen by that measurement (a depth-policy change or a direct call), and the depth-policy remedy has side effects (INV-003, INV-004). B-add would pay a second review per phase to close a gap nobody has sized.

### Objection 3

<!-- Source: Base (original, modified) - one-controlled-change statement replaced per Change 6 -->
<!-- Source: Debate (invariant-probe.md) - merged per Change #6 -->
"Nobody passes `--t2-engine`, so the panel stays dormant for consumers for as long as reflect's default is `legacy`." Answer: the dormancy is the verified current state (Section 3 item 1), and a direct call would also stay dormant until its skill exists. The route to activation is one reflect-side switch, which is not a single bounded change:
- It is a prose edit in three places of the reflect skill (`sc-reflect-protocol/SKILL.md:87,311,464-465`) with no staged selector reachable from a consumer call (INV-010).
- It flips every UC-1 caller: the task-builder PRE gate (`task-builder/SKILL.md:1664-1680`), auggie-review and the troubleshoot handoffs, not only workflow and tasklist (INV-008).
- Shadow-first doubles Tier-2 reviewer spend on every consumer escalation (INV-010).
- Reflect-owned tests change at Stage 3: the content pins, and the remediation route table if depth policy changes (INV-012, INV-003).
- The gate stays: the replay (Section 6.1), the contract-compat test (Section 6.3, necessary, not sufficient, INV-011) and a headless smoke run (Section 6.4).

### Objection 4 (plugin)

<!-- Source: Base (original, modified) - "cannot work without reflect" wording withdrawn and three-case account referenced per Change 10 -->
<!-- Source: Variant B (Proposal B), Section 8 third objection - merged per Change #10 -->
"Without a plugin copy, plugin-only users never see the panel." Answer: they do not see reflect or its review today either (Section 3 item 9). The earlier claim that a panel copy "cannot work without `sc-reflect-protocol`, the reviewer agents and the pins" is withdrawn as too strong for a delegate skill that brings its own reviewer agent (Section 10). The three-case account in Section 3 item 9 shows what a copy would deliver: nothing where the CLI is absent, redundancy where `superclaude install` was run, and value only in an unverified case. The plugin copy would not make a plugin install worse; whether it is worth maintaining is the product decision this slot calls it (r18 gap 6). It is decided as one set (reflect, panel, reviewer agent, CLI availability), after CLI availability in a plugin-only install is known, with a parity test per added plugin file (A-006; C-003).

## 9. Open items this position does not settle

<!-- Source: Base (original, modified) - pointer to Section 11 added -->
- The owner's DO4 answer itself and the plugin delivery decision (CO-35). A default and its costs are stated.
- Which engine feeds T5 (C-04), and whether tasklist T5 (UC-2) is in scope of the same panel (r11 gap 7).
- Whether `--t2-engine` should be documented in `commands/reflect.md` (0 matches today, r11 3.2; INV-010 confirms there is no row).
- The 12 unaddressed probe items in Section 11.

## 9a. What a later direct module needs

<!-- Source: Variant B (Proposal B), Section 3 - merged per Change #9 -->
<!-- Source: Debate (round2-advocate-A.md, round2-advocate-B.md, invariant-probe.md) - merged per Change #9 -->
A later direct module (a Stage 7 reviewer feed, a Wave 4 `plan-review`) is possible on the same core, with `effect` as module data (`effect: advisory` or `effect: blocking`; the core carries only the boolean `blocking`). These are conditions, not a plan. Wave 4 stays one advisory Skill call in this release, and Will Not at `sc-workflow-protocol/SKILL.md:107` ("new agents, Task fan-out") stays true (C-009: A wins, 94%). `tasklist-review`, `plan-review` and `effect` have no code home today and are design hypotheses until a replay.
1. Additive keys only, `contract_version` stays "1.1", and `reflect_*` is unchanged. `scripts/eval_workflow_vs_task_builder.py:1140`, `archive_workspace.py:327` and `tests/commands/test_workflow_command.py:178` require "1.1". `_kv` (`archive_workspace.py:167-173`) keeps any top-level `key: value` line, and the eval reader needs only `set(CONTRACT_KEYS) <= set(contract)` (`:1163`). The fault-finder enumerated the consumer-side readers and none closes the key set (INV-014 F3). A 1.1 to 1.2 bump is wrong (Section 10).
2. The `artifacts` rule (`refs/return-contract.md:52`), which names only `nested/reflect-<n>/`, is edited by hand. No test forces it (`tests/skills/test_worker_contract.py:528-537,1477-1482`). The nested-kind constants `EXPECTED_NESTING` (`:1678-1689`) and `UNATTENDED_EXPECT` are edited by hand (INV-014 F3, INV-015 residual).
3. The companion-eval allow-list and staging are edited (`scripts/eval_workflow_vs_task_builder.py:520,563-575`). If omitted, the call is denied and ends `skipped`.
4. A parity test is added per added plugin file (A-006).
5. A Wave 4 `plan-review` is a call-site change and edits both workflow trees (parity pin `test_workflow_command.py:93-103`). A Stage 7 feed changes Stage 7 text, not the call at `:1630`. Entry and loop are separable (C-009; round2-advocate-B.md).
6. Its own replay, and a headless smoke run (A-003).
7. A blocking feed must not fail open: a zero-success run escalates, as Stage 7's some-versus-zero gate does (`sc-tasklist-protocol/SKILL.md:1608` per round2-advocate-A.md; `:1702` per round1-advocate-B.md) (A-004).
8. Costs that Proposal B carried for such a module: C-02 INV-001, C-02 INV-002, C-02 INV-003, C-03 INV-007 and INV-J (OQ-24).

## 9b. Shared assumptions

<!-- Source: Debate (diff-analysis.md, round2-advocate-A.md, round2-advocate-B.md) - merged per Change #13 -->
A-001 and A-007 were STATED by both papers and are not scored. The five promoted assumptions and their final answers (debate-transcript.md):

| ID | Assumption | Final answer | Basis |
|---|---|---|---|
| A-002 | The panel reviews tasklist and plan documents well enough to be consumed at all | Neither (88%) | Unmeasured through either entry; advisory first, and any blocking use waits for a replay. |
| A-003 | A nested fan-out completes in headless `--unattended` mode and keeps the closed enum | Hybrid (82%) | The existing `nested/reflect-<n>/` kind is covered by the `artifacts` rule; a new `nested/panel-<n>/` kind is not and needs a hand edit. Headless fan-out is unrun for both routes, and the companion eval cannot run it. |
| A-004 | A panel failure, refusal or short panel maps to a status the advisory consumer handles fail-open | Hybrid (88%) | Fail-open for the advisory outputs: `skipped` or `failed` and proceed at Wave 4 (`:93`), the bundle still ships at Stage 10.5 (`:1640`). The Stage 10.5 `needs_human_decision` halt is the exception (INV-001). A zero-success blocking feed escalates. |
| A-005 | A plugin-only install already calls a skill it does not ship and ends `skipped` or `failed` | Neither (90%) | Shared inference, not executed by anyone. |
| A-006 | The source-tree and plugin-tree pins keep their meaning, and `verify-sync` is the only other guard | B (90%) | The existing parity pin covers `*.md` of one skill and one command, so every added plugin file needs its own parity test. `verify-sync` coverage of `plugins/` is unchecked. |

## 10. Claims withdrawn or corrected in the debate

<!-- Source: Debate (round1-advocate-A.md, round1-advocate-B.md, round2-advocate-A.md, round2-advocate-B.md, invariant-probe.md) - merged per Change #15 -->
Each row names the claim, its origin and what replaced it. Claims are quoted here only as withdrawn text; the sections above carry the corrected wording.

| # | Claim | From | Disposition |
|---|---|---|---|
| 1 | "The fence test must be changed in the same change" | Proposal A, item 8 | Withdrawn by A's advocate. The three diff-based tests are working-tree guards. The probe adds that the content pins in the same file are standing, so the withdrawal understated the Stage 3 edit (INV-012; Section 3 item 8). |
| 2 | "Zero pin changes outside the fence test" | Proposal A, Sec 6 item 4 | A prediction, not a run. Reflect-owned pins change at Stage 3 (Section 6.4). |
| 3 | "The only route that keeps the contract intact" | Proposal A's advocate | Reduced: B-add with additive keys at "1.1" can also meet it (round2-advocate-A.md). |
| 4 | A plugin panel copy "cannot work without `sc-reflect-protocol`" | Proposal A, Sec 8 objection 4 (X-002) | Too strong for a delegate skill that brings its own reviewer agent (Section 8 objection 4). |
| 5 | "Four readers" of `reflect_status` | Proposal A, Sec 5 | Undercount: at least the four skill readers, one closed-enum validator and the tests (INV-008). |
| 6 | The panel "can be switched on for both consumers with zero edits to their call sites" | Proposal A, item 1 | Contradicts rule D1 (debate-transcript.md, intra-variant contradictions; Section 3a). |
| 7 | "A panel result reaches consumers only as `status`, `coverage_pct`, `tier_reached`" | Consensus bullet 3 (round2-advocate-A.md) | Too narrow and partly vacuous: two of the three fields are fixed before the engine is read (INV-007; Section 2). |
| 8 | "Effect advisory at Stage 10.5" | Consensus bullet 3 and Proposal A, Sec 1 | False as stated. Stage 10.5 is advisory-blocking with a halt, an unattended `blocked` state and a `--remediate` write path (INV-001, INV-002; Section 1.2). |
| 9 | "Count the share from the existing shadow runs" | Proposal A, Sec 6 item 2 | No working instrument (INV-005; Section 6.6). |
| 10 | The depth-policy remedy is "cheaper" and "pin-safe" | Round 2 files of both advocates | Unsupported: it changes the remediation route and forces Tier 2 at Wave 4 on the legacy engine, and the parity pin needs both trees (INV-003, INV-004; Section 3a.3). |
| 11 | "One controlled change at reflect's default" | Proposal A, Sec 8 objection 3 | Not a single bounded change: it flips every UC-1 caller and has no staged selector (INV-008, INV-010; Section 8 objection 3). |
| 12 | "A direct call would add a new revise loop" | Proposal A, Sec 8 objection 1 | Replaced (X-001: Hybrid): generation-time blocking already exists in Stages 8-10, and a call-site direct call adds no loop. |
| 13 | "Fence tests are a working-tree guard" (as a blanket statement) | Round 2 advocate files | Right for three tests, wrong for the content pins (INV-012, ADDRESSED with a residual wording fix). |
| 14 | Workflow contract 1.1 to 1.2 with `panel_status` and `panel_report_path` | Proposal B, Sec 3 | Wrong: `scripts/eval_workflow_vs_task_builder.py:1140`, `archive_workspace.py:327` and `tests/commands/test_workflow_command.py:178` require "1.1". Later modules add keys only (Section 9a). |
| 15 | E6: the reflect skill edit fence binds A's route and not B's | Proposal B | Overstated, because the fence diffs against `HEAD` (round1-advocate-B.md). |
| 16 | E7: no tasklist lens as a binding limit | Proposal B | Weak: B's tasklist module runs on the v1 engine. The lens fact itself stays (Section 2). |
| 17 | A blocking effect at Stage 10.5 | Proposal B, Sec 3 | Placed ambiguously: Stage 10.5 does not run a revise loop (`:1621-1623`). Any blocking use is a later Stage 7 feed change after a replay. The probe adds that Stage 10.5 has its own halt (INV-001). |
| 18 | B-add as a recommendation for this release | Proposal B | Withdrawn in Round 2: a second review per phase to close an unsized gap. |
| 19 | The `:243-248` pin "needs a panel line added in both forms" | Proposal B, Sec 6 | It is an `any(...)`; a second panel line passes (round1-advocate-A.md, agreed in round1-advocate-B.md). |
| 20 | "B's seam is needed for the loop" | Proposal B's advocate | Withdrawn in Round 2: entry and loop separate. |
| 21 | Low-complexity phases are the lowest-risk phases | Proposal A's advocate, strength 6 | Holds only for the quick band (round2-advocate-A.md; Section 3a). |

## 11. Conditions under which this resolution holds, and what the debate left open

<!-- Source: Debate (invariant-probe.md) - merged per Change #16 -->
### 11.1 Status of the debate

Convergence: 24 of 24 diff points agreed (100%, threshold 80%); both advocates' final verdicts match on every point. Status: BLOCKED_BY_INVARIANTS, because 7 HIGH-severity probe items are unaddressed. No Round 3 was run (depth standard). No second pass of the 24-point matrix was run after Round 2.5; the probe changes the conditions under which the agreed text holds, not the winners of the 24 points (debate-transcript.md). The orchestrator's process note: Proposal B's advocate conceded most points, and that speed is itself a sycophancy signal, so the probe checked whether the conceded claims are true in code. It found several overstated or wrong (INV-001, INV-004, INV-007, INV-012 and the "pin-safe" depth remedy). Probe summary: 15 items, 3 ADDRESSED (INV-009, INV-012, INV-015), 12 UNADDRESSED (7 HIGH, 5 MEDIUM, 0 LOW).

### 11.2 Probe items INV-001 to INV-015

| ID | Category | Assumption probed | Status | Severity | Finding and where this document treats it |
|---|---|---|---|---|---|
| INV-001 | guard_conditions | "Effect advisory at Wave 4 / Stage 10.5; blocking stays at T5 and Stages 6-10": no generation-time halt is reachable from Stage 10.5 or Wave 4 | UNADDRESSED | HIGH | Wave 4 has no halt path. Stage 10.5 does: `needs_human_decision` halts (`:1640`), an unattended run ends `blocked` (`:1642`), and the label is "advisory-blocking" (`:1646`). Corrected in Sections 1.2, 2 and 8. The effect of an engine switch on halt frequency stays open. |
| INV-002 | interaction_effects | Stage 10.5 is a read-only review whose only output is a verdict; an engine switch changes review quality and nothing else | UNADDRESSED | HIGH | `--remediate` is a write path (reflect `SKILL.md:369-371`); the plan route calls `sc:workflow-protocol` (`:383-385`), which runs its own Wave 4 reflect, so one call can nest reflect, workflow and reflect. The finding set decides whether a corrective package is written, and the reach count undercounts nested runs. Recorded in Sections 1.2, 2 and 3a; unpriced. |
| INV-003 | interaction_effects | The depth-policy remedy for the reach gap is a pure reach fix with no side effect | UNADDRESSED | HIGH | It changes the remediation route and forces Tier 2 at Wave 4 on the legacy engine (Section 3a.3). Open. |
| INV-004 | guard_conditions | A call-site depth flag at Wave 4 is "pin-safe" | UNADDRESSED | MEDIUM | Both workflow trees need the edit, the phrase "defaults for every other flag" becomes false and is unpinned (Section 3a.3). Open. |
| INV-005 | collection_boundaries | The reach share can be measured from existing shadow runs or from contracts of real consumer calls | UNADDRESSED | HIGH | The only aggregator globs shadow-run panel manifests and cannot see unreached phases or tasklist consumer directories. The reopen condition in Section 1.1 has no instrument that can fire it (Section 6.6). Open. |
| INV-006 | collection_boundaries | "Measure the share" has a well-defined denominator | UNADDRESSED | MEDIUM | Populations with no reflect run, the `--budget-remaining` downgrade and the forced-deep boundary make the denominator ambiguous (Section 3a.1). Open. |
| INV-007 | count_divergence | "A panel result reaches consumers only as `status`, `coverage_pct`, `tier_reached`" | UNADDRESSED | HIGH | Consumers also read `needs_human_decision`, `unmapped_requirements`, `run_id` and `report_path`, and two of the three named fields are fixed before the engine is read. Corrected in Section 2. Open as to what a panel can change. |
| INV-008 | count_divergence | The default flip touches "two consumers" and "four readers of `reflect_status`" | UNADDRESSED | MEDIUM | A flip reaches every UC-1 caller, and more than four kinds of reader exist (Section 3 item 3; Section 8 objection 3). Counts corrected; the flip cost is open. |
| INV-009 | state_variables | A short, refused or failed panel cannot push `reflect_status` outside the closed enum | ADDRESSED | LOW | The enum is closed in the contract, the validator and the test. Residual: the panel-to-status map is unpinned (INV-011). |
| INV-010 | state_variables | "One reflect-side switch at reflect's default" is a single well-defined change | UNADDRESSED | MEDIUM | The default is prose in three places with no staged selector, and shadow-first doubles Tier-2 reviewer spend (Section 8 objection 3; Section 6.6). Open. |
| INV-011 | guard_conditions | A "contract-compat test against the 36-test matrix" is enough to show a panel engine's contract is compatible | UNADDRESSED | MEDIUM | `derive_verdict` reads adversarial fields only, the panel lint adds rules the matrix does not test, and no panel-to-status map has been exercised (Sections 2, 5 and 6.3). Open. |
| INV-012 | guard_conditions | "Fence tests are a working-tree guard (INFERRED, not run)"; the claim "the fence test must be changed" is withdrawn | ADDRESSED | MEDIUM | True for three tests; not true of the content pins at `:146-238`. The withdrawal understates the Stage 3 edit. Wording corrected in Section 3 item 8 and Section 5. |
| INV-013 | sufficiency_challenge | "The replay/measurement decides it": a replay with ground truth exists, someone runs it, and arm R is a real consumer call | UNADDRESSED | HIGH | No GT scorer, a tiny n, a harness that cannot run a fan-out, no engine selector, no numeric threshold (Section 6.6). Open. |
| INV-014 | sufficiency_challenge | "The consensus resolution alone achieves its stated outcome: consumers get the panel's benefit without a second entry; no consumer pin changes" | UNADDRESSED | HIGH | F1: a faithful engine switch leaves the consumer-visible output as the legacy `status`, and no consumer reads REPORT.md content. F2: making the benefit visible needs a defined panel-to-status map and either keeps the Wave 4 debate as verdict authority or yields `null-convergence`. F3: reflect-owned pins change, and a later direct module edits `tests/skills/test_worker_contract.py:1678-1689`. F4: a Stage 10.5 halt or `blocked` means consumers pay the cost. Survives: additive keys at `contract_version` "1.1" are safe at the three consumer-side readers (Section 9a). Open. |
| INV-015 | interaction_effects | A later direct module adds a nested directory without a pinned-test change | ADDRESSED | LOW | The `artifacts` rule gap and the test blind spot are recorded (Section 9a). Residual: a new kind edits the closed `EXPECTED_NESTING` equality (`:1678-1689`). |

### 11.3 Holds while, and reopen conditions

<!-- Source: Debate (round2-advocate-A.md) - merged per Change #16 -->
This resolution holds while the C-01 to C-03 outcomes stand (reflect keeps its own engine and `shortfall: visible`). It reopens if any of the following happens:
1. The replay shows the direct path catches materially more blocking GT items per cost, and the difference is not explained by depth routing. "Materially more" has no numeric threshold (INV-013).
2. The owner chooses plugin parity.
3. Blocking GT items sit in phases that never reach the panel (the pre-registered condition of Section 1.1).

### 11.4 Not checked by the probe

The fault-finder did not check `findings_v2.py:36`, plugin CLI availability, whether `make verify-sync` covers the plugin tree, research files 08 and 11, or any test execution. No test was run by any advocate or by the fault-finder.
