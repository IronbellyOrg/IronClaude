# Research 01: Doc Cross-Validator / Spec Delta

Status: Complete

## Scope

- Patched report: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md`
- Merged requirements artifact to patch before implementation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md`

## 1. Patched report R1-R9 line map

| Patched requirement | Exact report lines | Implementation meaning |
|---|---:|---|
| R1 — proof bar: `unreachable` Regression is real-boot-only | `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:31-47` | Static binding absence, discarded result, and oracle mismatch are advisory recall signals only; they can create `unproven` Grounding Gaps but cannot set `regression_present` unless real boot proves sink absence. |
| R2 — `--no-reachability` is telemetry-only | `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:49-68` | Disable path must set skip telemetry only and must not create `grounding-gaps.yaml`, `needs_human_decision`, or `status: partial`. |
| R3 — spec-absent legacy behavior is telemetry-only | `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:70-89` | With neither `--spec` nor `--tasklist`, Step 5.6 cannot run a blocking gate and must not create a Grounding Gap or change status. |
| R4 — contract version is `1.6.0` | `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:91-101` | Any return contract containing new reachability fields must use `contract_version: "1.6.0"`; `1.5.0` remains D13-only. |
| R5 — wrapper plumbing required | `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:103-120` | `superclaude reflect run` needs an option/config path, prompt forwarding, docs updates, and help/prompt parity tests for `--no-reachability`. |
| R6 — producer-level eval fixture mandatory | `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:122-156` | Consumer/contract fixture tests are insufficient; an eval fixture must prove Step 5.6 produces reachability fields and ledger rows from real inputs. |
| R7 — field presence and consistency | `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:158-209` | UC-2 `1.6.0` return contracts must emit the reachability block consistently; UC-1 may omit it. |
| R8 — bounded work, not zero work | `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:211-227` | Replace zero-token/zero-turn claims with bounded caps: no new tool class, but 1-3 turns per requirement, max 12 requirements, cap 36 turns, max one real boot. |
| R9 — semantic fallback advisory only | `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:229-239` | v1 blocking gate requires explicit `durable_sink:` or `@sink`; semantic classification can emit advisory telemetry only and cannot create Grounding Gaps or status changes. |

The report also provides an implementation checklist summarizing the same repairs at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:241-253`, and declares original findings B1-B3/I1-I3 superseded by R1-R9 at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:255-266`.

## 2. Superseded or contradictory clauses still present in `merged-requirements.md`

### 2.1 R1 conflicts: non-real-boot paths still prove `unreachable` / Regression

- The top-level thesis says auto-`regression_present` is reserved for a real-boot-proven contradiction, which agrees with R1, but the same paragraph also says static fail-open scan and real-boot verifier are advisory recall aids and "never the gating mechanism" at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:26-28`. This is ambiguous against R1 because R1 still allows static signals to create a blocking `unproven` Grounding Gap; the phrase "never the gating mechanism" should be narrowed.
- The verdict table still allows `unreachable` when "binding unambiguously absent AND `oracle_mismatch` confirmed" at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:92`. This directly contradicts R1 at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:35-45`.
- The proposed Step 5.6 insertion repeats the same non-real-boot upgrade path: "real-boot observed ... OR binding unambiguously absent AND `oracle_mismatch` confirmed" at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:130-132`.
- The proposed §10.4 insertion says binding absence plus oracle mismatch can be Regression if unambiguous at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:143-148`.
- The proposed taxonomy mapping repeats the same non-real-boot Regression condition at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:229-237`.

Required patch: replace every "binding absent AND oracle_mismatch => unreachable/Regression" clause with "real boot observed contracted sink absent". Static binding absence plus oracle mismatch must become `unproven`.

### 2.2 R2 conflicts: `--no-reachability` still writes Grounding Gaps

- The proposed Step 5.6 text says disabled by `--no-reachability` and "records the skip in Grounding Gaps" at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:136-138`. This directly contradicts R2, which says disable must not create or append to `grounding-gaps.yaml`, set `needs_human_decision`, or force `status: partial` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:51-68`.
- The `reflect.md` flag row repeats that `--no-reachability` "records the skip in Grounding Gaps" at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:189-192`.

Required patch: rewrite both locations to telemetry-only skip with `reachability_gate_ran: false`, `reachability_skip_reason: --no-reachability`, `reachability_ledger_path: null`, zero counters, and no reachability-created Grounding Gap.

### 2.3 R3 conflicts: spec-absent diff-side probe still blocks

- The red-team decision table says no spec falls back to a diff-side probe yielding `unproven` or no-op and "never STOP" at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:55-56`. That sentence is internally ambiguous because `unproven` elsewhere routes to Grounding Gap/HALT.
- The trigger predicate says when neither `--spec` nor `--tasklist` is supplied, a touched emitter-shaped call with discarded result creates a single `unproven` row and Grounding Gap at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:71-75`. This contradicts R3 at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:70-89`.
- The proposed Step 5.6 insertion says spec/tasklist absent yields `unproven` and a §10.6 Grounding Gap at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:133-138`.
- The proposed taxonomy mapping says spec absent is `unproven` and creates a Grounding Gap at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:235-237`.

Required patch: make spec/tasklist absence a telemetry-only skip with reason `spec-and-tasklist-absent`; a diff-side probe may emit non-blocking telemetry only and must not set `reachability_unproven`, create a Grounding Gap, require human decision, or change status.

### 2.4 R4 conflicts: new reachability fields still attached to `1.5.0`

- The self-test section says to bump fixtures to `contract_version` `"1.5.0"` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:267-270`.
- The `reachability_unbound_sink.yaml` fixture includes new reachability fields while declaring `contract_version: "1.5.0"` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:272-305`.
- The `reachability_silent_bug_pregate.yaml` fixture declares `contract_version: "1.5.0"` and includes `reachability_gate_ran` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:307-333`.

Required patch: every fixture/report/template/eval assertion that includes reachability fields must declare `contract_version: "1.6.0"`; keep `1.5.0` limited to the D13 additive fields named by R4.

### 2.5 R5 gaps: wrapper plumbing is not present in the merged requirements' concrete edits

- The concrete edits add a slash-command flag row for `reflect.md` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:189-192`, but no concrete task in this artifact names the Python wrapper config/model field, Click option, `_build_prompt()` forwarding, or wrapper docs parity required by the patched report at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:103-120`.
- The DoD checklist only says edits 4.1-4.14, sync, tests, eval, format, and PR at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:418-424`; it does not include R5 wrapper parity acceptance checks.

Required patch: add a concrete wrapper section mirroring R5: config/model default enabled, Click flag, `_build_prompt()` forwarding exactly once when disabled, docs update, `--help` smoke/parity test.

### 2.6 R6 gap: consumer fixture tests are over-emphasized and producer fixture is only vague

- The merged artifact explicitly says deterministic tests prove contract→verdict wiring and that protocol-level detection is validated by an eval-workspace falsifier case at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:395-399`, and DoD mentions adding a §17.6 falsifier case at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:418-424`.
- However, it does not include the patched report's exact producer fixture shape and required assertions from `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:122-156`.

Required patch: add the R6 fixture tree and assertions explicitly, including `contract_version: "1.6.0"`, `reachability_gate_ran: true`, `reachability_unproven: 1`, `status: partial`, and a ledger row with `verdict: unproven`, `oracle_match: false`, and `gap_kind: oracle-mismatch`.

### 2.7 R7 gap: field-presence and consistency rules are incomplete

- The merged artifact lists stable reachability fields at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:151-162`, but it does not state the patched R7 rule that the block is mandatory for every UC-2 `1.6.0` return contract and optional/absent for UC-1, nor the consistency invariants at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:158-209`.

Required patch: insert the full R7 presence/consistency block into the requirements before implementation, including ran/skip/unreachable/unproven invariants.

### 2.8 R8 conflicts: zero-cost claims remain

- The cost-profile edit says the gate adds no new tool class and then sets `reachability_gate_added_tokens: 0` and `reachability_gate_added_turns: 0` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:251-259`. This directly contradicts R8 at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:211-227`.
- The slash-command flag row says the gate reuses the step-5.5 verification budget and has "no extra tool class" at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:189-192`; the no-extra-tool-class portion is compatible with R8, but it should not imply zero added work.

Required patch: replace zero token/turn fields with R8 bounded estimates and caps: `reachability_gate_added_tool_classes: 0`, `reachability_gate_added_turns_per_side_effect_requirement: "1-3"`, max 12 scanned requirements, turn cap 36, real boot cap 1, plus overflow telemetry behavior.

### 2.9 R9 conflicts: semantic fallback still blocks

- The trigger predicate allows semantic classification of the AC's effect noun into the side-effect taxonomy and says if classification cannot pin a unique sink, the row is `unproven` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:60-69`. Under R9, semantic classification without explicit `durable_sink:`/`@sink` can be advisory telemetry only and cannot create a Grounding Gap or status effect.
- The proposed Step 5.6 insertion also resolves `contracted_sink` by explicit annotation "when present, else by semantic classification" at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:113-119`.
- The risk table treats tightening to explicit `durable_sink:` only as a rollback mitigation at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md:406-407`; the patched report makes annotation-only the v1 default at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:229-239`.

Required patch: promote explicit annotation-only gating into the main v1 trigger predicate; semantic fallback should be advisory telemetry until eval precision proves it safe.

## 3. Recommended task-item breakdown for safely patching `merged-requirements.md` before implementation

1. **Patch proof-bar language first.** Replace all non-real-boot `unreachable`/Regression paths in verdict tables, Step 5.6 insertion text, §10.4 insertion text, and deviation-taxonomy mapping. Acceptance: no line in `merged-requirements.md` permits binding absence plus oracle mismatch to set `regression_present` without real boot.
2. **Patch skip semantics.** Rewrite `--no-reachability` and spec/tasklist-absent behavior to telemetry-only skips. Acceptance: no `--no-reachability` or `spec-and-tasklist-absent` clause creates Grounding Gaps, `needs_human_decision`, `status: partial`, or `reachability_unproven`.
3. **Patch contract version.** Change all reachability-bearing fixtures/assertions/templates from `1.5.0` to `1.6.0` and add text preserving `1.5.0` as D13-only. Acceptance: no reachability field appears under `contract_version: "1.5.0"` except in an explicitly labeled negative/backcompat fixture that asserts unknown-field tolerance without treating fields as stable.
4. **Add wrapper requirements.** Insert a concrete Python wrapper section and DoD items for config/model field, Click option, prompt forwarding, docs parity, `--help` test, and `_build_prompt()` tests. Acceptance: tasklist can route R5 to implementation without relying on another researcher to infer missing work.
5. **Add producer eval fixture requirements.** Insert the R6 eval-workspace tree and required assertions, distinct from contract consumer tests. Acceptance: tasklist includes both CI-level consumer tests and producer-level eval coverage.
6. **Add field-presence invariants.** Insert R7's mandatory UC-2 `1.6.0` block and consistency rules. Acceptance: implementer has exact invariants for gate-ran, skip, unreachable, and unproven cases.
7. **Patch cost profile.** Replace zero work claims with R8 caps and overflow behavior. Acceptance: no `reachability_gate_added_tokens: 0` or `reachability_gate_added_turns: 0` remains.
8. **Patch semantic fallback rollout.** Make explicit `durable_sink:` / `@sink` the only v1 blocking trigger; demote semantic classification to advisory telemetry. Acceptance: semantic fallback cannot create Grounding Gaps, `reachability_unproven`, `needs_human_decision`, or status changes.
9. **Run a final document grep/re-read pass before building implementation tasks.** Search the requirements artifact for `binding unambiguously absent`, `records the skip in Grounding Gaps`, `spec absent`, `contract_version: "1.5.0"`, `reachability_gate_added_tokens: 0`, `reachability_gate_added_turns: 0`, and `semantic classification`; re-read matches and confirm they now align with R1-R9.

## Gaps and Questions

None blocking. This research treats patched REPORT R1-R9 as canonical and `merged-requirements.md` as the artifact to patch before implementation. If the executor decides not to modify `merged-requirements.md` directly, it must create an explicit companion amendment and cite why the original artifact was left unchanged.

## Summary

The patched report is internally concrete and implementation-ready, but the merged requirements artifact still contains multiple superseded clauses from the pre-patch design. The highest-risk contradictions are: non-real-boot Regression paths, skip paths that still write Grounding Gaps, spec-absent blocking behavior, reachability fields under `1.5.0`, zero-cost claims, and semantic fallback as a blocking trigger. Patch the requirements artifact against R1-R9 before any code implementation task is issued.

Status: Complete
