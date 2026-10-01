# Research 02: sc-reflect-protocol Skill Protocol Anchors

Status: Complete

## Scope

- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md`
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/`

## File inventory

Reference files currently present under `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/`:

- `cost-profile.yaml`
- `coverage-mapping.md`
- `deviation-taxonomy.md`
- `grader-extensions.md`
- `input-resolution.md`
- `ops-integration.md`
- `promotion-adapters.md`
- `reflection-rubric.md`
- `remediation-handoff.md`
- `report-template.md`
- `reviewer-spec.md`

The skill's own ref registry is at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:1656-1672`. Related existing entries:

- `refs/reflection-rubric.md` is loaded by Wave 1D / Wave 3C for calibrated confidence scoring at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:1661`.
- `refs/deviation-taxonomy.md` is loaded by Wave 1B (UC-2) and Wave 5 at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:1662`.
- `refs/report-template.md` is loaded by Wave 5 at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:1665`.
- `refs/ops-integration.md` is the build-time/WARN catalog ref at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:1667`.
- `refs/grader-extensions.md` is the eval-time assertion-extension ref at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:1668`.
- `refs/cost-profile.yaml` is the pre-invocation budget mirror at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:1670`.

A targeted search for `reachability`, `oracle`, `admissib`, `no-reachability`, `spec-absent`, `semantic fallback`, `contracted-sink`, and `sink` found no existing reachability/oracle contract; only the generic output-sink rule matched `sink` in `SKILL.md`. FR-RH1 therefore appears additive rather than an edit to an existing reachability subsection.

## Primary SKILL.md anchors and insertion points

### Wave map: add Wave 1A Step 5.6

Current high-level wave map names Wave 1A as real-code grounding and Wave 1B as mode-specific evidence gathering at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:142-145`.

Current Wave 1A symbolic chain lists Step 5.5 as `mcp__serena__execute_shell_command (scoped verify)` and Step 6 as citation re-read at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:472-475`.

Recommended insertion point:

- Insert `5.6` immediately after `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:474` and before citation re-read at line 475.
- Add the explanatory paragraph after the current Step 5.5 paragraph at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:490`, before the Step 4a paragraph at line 492.

Reason: Step 5.5 already establishes the UC-2 default-on verification triangle, skip reasons, and Grounding Gap degradation path at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:490`; Step 5.6 can reuse this adjacency but should remain a distinct contracted-sink reachability/oracle-admissibility gate rather than being folded into `execute_shell_command`.

### Verification safety/skips pattern to mirror

The existing verification triangle is UC-2 default-on, gated by `execute_shell_command_available`, `read_only`, and `--no-verify`, and skips with `verification_skip_reason` while degrading Regression detection to task-log claim + Grounding Gap at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:490`.

The existing stable fields for the verification triangle live at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:705-710`:

- `verification_ran`
- `verification_invocations`
- `verification_failures`
- `verification_regressions_detected`
- `verification_skip_reason`

Recommended FR-RH1 field insertion point:

- Add top-level `reachability_*` fields directly after `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:710`, keeping UC-2 verification/reachability surfaces adjacent.
- Include field-presence and consistency rules in the same stable-contract subsection so they are not buried in telemetry.

### Contract version bump to stable `1.6.0`

Current stable contract heading and literal value are `1.5.0` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:660-663`.

Other contract-version anchors to update:

- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:804` says each flag has report-template semantics and contract version is `v1.5.0`.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:877` defines a minor version as purely additive top-level fields, which fits stable `1.6.0` if FR-RH1 only adds fields and does not rename/retype existing fields.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:1772` currently asserts `return-contract.yaml contract_version == "1.5.0"` in the Testability Map.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/report-template.md:13-15` renders `contract_version: 1.5.0` in the REPORT header.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:1555-1558` maps metrics `skill_version` to the contract version from §9.1, so no literal edit is needed there unless examples change.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:1641` has a JSONL example with `"skill_version": "1.5.0"`; update example if examples are part of the task.

### UC-2 field-presence / consistency rules

Existing stable-contract rules are centralized in §9.1, and the consumer field map starts at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:851-868`.

Recommended insertion points:

- Stable schema: after verification fields at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:705-710`.
- One-line field semantics promise: update `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:804` and `refs/report-template.md` required field prose.
- Consumer map: add a row near existing UC-2 consumers at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:857-864`, likely for the in-skill Wave 7 promotion adapter and/or task/sprint consumers if `reachability_*` gates promotion.
- Testability map: add assertions near `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:1766-1773`, adjacent to deviation taxonomy, grounding gaps, and contract version checks.

Canonical patched R7 rule shape for MDTM implementation (source: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:158-209`):

- UC-2 return contracts at `contract_version: "1.6.0"` MUST emit the stable reachability block: `reachability_gate_ran`, `reachability_ledger_path`, `reachability_requirements_scanned`, `reachability_unreachable`, `reachability_unproven`, `reachability_real_boot_ran`, and `reachability_skip_reason`.
- UC-1 may omit the block; do NOT add a task requirement that pre/UC-1 contracts must carry null/false reachability fields.
- When `reachability_gate_ran == true`: `reachability_skip_reason: null`, non-null `reachability_ledger_path`, and `reachability_requirements_scanned >= 1`.
- When `reachability_skip_reason == "--no-reachability"`: `reachability_gate_ran: false`, `reachability_ledger_path: null`, zero counters, `reachability_real_boot_ran: false`, and no reachability-created Grounding Gap / `needs_human_decision` / `status: partial`.
- When `reachability_skip_reason == "spec-and-tasklist-absent"`: `reachability_gate_ran: false`, `reachability_ledger_path: null`, zero scanned/unreachable/unproven counters, and telemetry-only behavior.
- When `reachability_unreachable > 0`: `reachability_real_boot_ran: true`, `regression_present: true`, and `verification_regressions_detected >= reachability_unreachable`.
- When `reachability_unproven > 0`: `grounding_gaps_path` non-null and `needs_human_decision: true`.

## Regression vs Grounding Gap mapping anchors

The current Regression definition says a change contradicting acceptance criteria, explicit constraints, or previously-passing tests is Regression at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:952-960`.

The current exit-code taxonomy explicitly says non-zero verification exits are not uniformly Regression and unmapped exits default to Grounding Gap at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:962-972`.

The parallel ref has the same mapping in `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md:99-112`.

The Grounding Gaps schema and consequences are at:

- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:984-1008`
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md:115-138`

Recommended FR-RH1 taxonomy edits:

- In `SKILL.md` §10.4, add contracted-sink reachability/oracle-admissibility rows to the existing by-evidence mapping rather than creating a new deviation class.
- In `refs/deviation-taxonomy.md`, mirror the same rows under the existing “Verification exit-code → deviation-class mapping” section, or rename that section to include reachability/oracle evidence if the gate is not exit-code based.
- Preserve the existing invariant from `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:974`: precedence is respected by evidence, not by assignment.

Canonical patched mapping pattern to encode (source: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:31-47` and `:229-239`):

- `unreachable` / Regression is ONLY proven when real boot runs and observes the contracted sink absent.
- Static binding absence, discarded emitter result, unresolved sink identity, oracle mismatch, or real-boot unavailable can produce only `unproven` where a blocking annotated sink exists; they MUST NOT set `regression_present`.
- `--no-reachability` and neither-spec-nor-tasklist are telemetry-only skips, not Grounding Gaps.
- Semantic-only fallback without explicit `durable_sink:` / `@sink` is advisory telemetry only in v1; it cannot create a Grounding Gap, cannot increment `reachability_unproven`, cannot set `needs_human_decision`, and cannot change `status`.

## No-reachability / spec-absent skip semantics

Existing skip semantics for unavailable verification are:

- Stable `verification_skip_reason` enum at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:709`.
- Verification triangle unavailable row at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:1309`, which continues, emits `verification_ran: false`, sets skip reason, degrades Regression detection to task-log claim + Grounding Gap, and emits a WARN.
- Ops WARN examples for read-only and context-excluded cases at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md:118-141`.

Recommended insertion points:

- Add reachability skip semantics after Step 5.6 explanatory block near `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:490-492`.
- Add a new failure-mode row near `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:1309`.
- Add WARN catalog entries in `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md` after the existing verification WARNs at lines 118-163.

Canonical patched skip semantics to encode (source: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:49-89`):

- `--no-reachability`: operator rollback path. Set `reachability_gate_ran: false`, `reachability_skip_reason: --no-reachability`, `reachability_ledger_path: null`, zero reachability counters, `reachability_real_boot_ran: false`; MUST NOT create/append `grounding-gaps.yaml`, set `needs_human_decision`, or force `status: partial`.
- `spec-and-tasklist-absent`: legacy no-authoritative-contract path. Set `reachability_gate_ran: false`, `reachability_skip_reason: spec-and-tasklist-absent`, `reachability_ledger_path: null`, zero scanned/unreachable/unproven counters; any diff-side shape is non-blocking telemetry only and MUST NOT create a Grounding Gap or status effect.
- `no-side-effect-requirements`: no eligible explicit side-effect requirements. Set `reachability_gate_ran: false`, `reachability_skip_reason: no-side-effect-requirements`, null ledger path, zero counters.
- Other oracle insufficiency with an explicit side-effect requirement may still route to `unproven` Grounding Gap only where patched R1/R7 allow it; do not generalize the telemetry-only skip paths into blocking gaps.

## Advisory-only semantic fallback anchors

Existing advisory-only fallback pattern is strongest in the reuse sweep:

- Agent unavailable fallback is inline `serena+ripgrep`, findings are capped at advisory L2, and the skill never stops at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:470-471`.
- The full Step 4a paragraph repeats that auggie-unavailable fallback findings are capped at advisory L2 and never stop at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:492`.
- The stable contract already includes `neighbour_search_degraded` for auggie-unavailable fallback capped at advisory L2 at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:719`.
- `refs/deviation-taxonomy.md` says weaker reuse signal, auggie-unavailable fallback, or insufficient grounding routes to Grounding Gaps and never `deviation-ledger.yaml` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md:1023`.

Recommended FR-RH1 edit:

- Model the semantic fallback after reuse sweep only in the limited sense of advisory telemetry: semantic-only reachability hints may populate advisory telemetry/report notes but must not increment `deviation_count_by_class.regression`, must not set `regression_present`, must not increment `reachability_unproven`, must not create a Grounding Gap, and must not satisfy a blocking reachability gate.
- Do NOT add a new stable field unless the patched R7 schema is explicitly amended. The canonical stable fields are exactly the R7 fields from `REPORT.md:162-172`; any extra field such as `reachability_semantic_fallback_used` must be treated as optional telemetry, not part of the stable `1.6.0` contract unless separately approved.

## Report-template anchors

`refs/report-template.md` header currently renders contract fields at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/report-template.md:13-25`, and required-field semantics at lines `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/report-template.md:27-35`.

Deviation rendering format is at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/report-template.md:52-69`.

Grounding Gaps rendering is at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/report-template.md:86-103`.

Per-task verdict rendering is at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/report-template.md:105-119`.

Recommended edits:

- Bump header `contract_version` from `1.5.0` to `1.6.0` at line 14.
- Add any load-bearing `reachability_*` header fields to the YAML header if operators/consumers need them in REPORT.md without reading `return-contract.yaml`.
- Add a conditional “Reachability / Oracle admissibility” section after the header/required fields and before deviations, or after deviations if the gate emits per-sink findings. It should explicitly distinguish deterministic findings from advisory semantic fallback.
- Render reachability Grounding Gaps only for `reachability_unproven > 0` cases arising from an explicit `durable_sink:` / `@sink` annotated side-effect requirement with insufficient reach/oracle proof. Do NOT render Grounding Gaps for `--no-reachability`, `spec-and-tasklist-absent`, or semantic-only fallback telemetry.

## Reflection-rubric anchors

Current rubric dimensions:

- Citation grounding at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:15-24`.
- Coverage completeness at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:26-35`.
- Deviation-classification clarity at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:37-46`.
- Risk surface coverage at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:48-57`.
- Recommendation actionability at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:59-68`.

Recommended edits:

- Add reachability/oracle-admissibility expectations under Citation grounding and Risk surface coverage.
- If FR-RH1 introduces a count/ratio such as `reachability_checked_count`, add it as a structural signal or as a sub-term to Coverage completeness rather than creating a sixth top-level dimension unless the spec explicitly requires it.

## Cost-profile anchors

SKILL.md cost table is at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:1537-1545`.

Machine-readable cost profile is at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml:21-70`:

- `cost_profile_version: "1.0.0"` at line 21.
- T1 bands at lines 33-44.
- T2 bands at lines 46-56.
- T3-added bands at lines 58-67.
- `hard_kill_multiplier: 1.25` at line 70.

Recommended edits:

- Add the patched R8 bounded-work language regardless of whether numeric cost bands change: `reachability_gate_added_tool_classes: 0`, `reachability_gate_added_turns_per_side_effect_requirement: "1-3"`, `reachability_gate_max_side_effect_requirements_scanned: 12`, `reachability_gate_added_turns_cap: 36`, and `reachability_gate_real_boot_invocations_cap: 1`.
- Remove/forbid zero-work claims such as `reachability_gate_added_tokens: 0` or `reachability_gate_added_turns: 0`.
- If cost bands change, update `refs/cost-profile.yaml` in lockstep and bump `cost_profile_version`; if bands do not change, still add the bounded-work prose/caps in SKILL.md/report-template/requirements so the gate is not documented as free.

## Ops / WARN anchors

Existing WARN catalog for verification degradations is in `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md:118-163`.

Recommended edits:

- Add WARN entries for `no-reachability`, `spec-absent`, and semantic fallback/advisory-only if these are operator-visible.
- Preserve current “loud-never-silent” behavior stated at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md:120`.

## Eval / grader anchors

Existing grader extension overview is at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md:7-24`.

Current useful assertion types:

- `yaml_field` exists in the baseline assertion set listed at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md:9`.
- `regex_present` and `regex_absent` are defined at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md:62-101`.
- `yaml_list_contains` is defined at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md:104-131`.

Recommended edits:

- Prefer existing `yaml_field`, `regex_present`, `regex_absent`, and `yaml_list_contains` assertions for FR-RH1 fixture checks unless contracted-sink reachability requires a new semantic assertion type.
- Add Testability Map rows in `SKILL.md` near `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md:1750-1778` for: contract_version `1.6.0`, required `reachability_*` fields, no-reachability/spec-absent skip semantics, deterministic Regression mapping, Grounding Gap mapping, and advisory-only semantic fallback non-gating behavior.

## Related refs that should be edited

Must edit:

1. `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/SKILL.md`
   - Add Wave 1A Step 5.6.
   - Bump stable contract to `1.6.0`.
   - Add `reachability_*` top-level fields and consistency rules.
   - Add Regression vs Grounding Gap mapping.
   - Add skip/fallback semantics and Testability Map rows.

2. `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/report-template.md`
   - Bump header to `1.6.0`.
   - Render reachability/oracle-admissibility fields or section.
   - Verify `--no-reachability` and `spec-and-tasklist-absent` render only skip telemetry/audit/WARN state, never Grounding Gaps, `needs_human_decision`, or `status: partial`.

3. `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md`
   - Mirror the Regression vs Grounding Gap mapping for reachability/oracle evidence.
   - Preserve 4-category taxonomy and separate Grounding Gap artifact.

4. `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md`
   - Add reachability/oracle-admissibility to citation grounding, risk surface, and possibly coverage completeness scoring.

5. `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml`
   - Edit only if Step 5.6 changes cost bands; otherwise leave numeric profile stable and add SKILL.md prose note only.

Likely edit:

6. `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md`
   - Add operator WARNs for reachability unavailable, spec/oracle absent, and advisory semantic fallback if operator-visible.

Optional / eval-dependent:

7. `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md`
   - Use existing assertion types if possible; add a new assertion only if deterministic reachability artifacts need semantic validation beyond `yaml_field`/`regex_*`/`yaml_list_contains`.

## Recommended MDTM task-item breakdown

1. Update `SKILL.md` Wave 1A chain with Step 5.6 and a detailed explanatory block after Step 5.5.
2. Bump stable contract from `1.5.0` to `1.6.0` across `SKILL.md`, report template, examples, and testability map.
3. Add `reachability_*` top-level stable fields under UC-2, with explicit presence/consistency rules and skip reasons.
4. Add reachability/oracle-admissibility Regression vs Grounding Gap mapping in both `SKILL.md` §10 and `refs/deviation-taxonomy.md`.
5. Add no-reachability/spec-absent skip semantics and advisory-only semantic fallback semantics, mirroring the existing verification/reuse fallback patterns.
6. Update `refs/report-template.md` to render the new contract fields/section and Grounding Gap rows.
7. Update `refs/reflection-rubric.md` so reviewers/calibrators score reachability/oracle grounding in the existing dimensions.
8. Decide whether cost bands change; if yes update both `SKILL.md` §15 and `refs/cost-profile.yaml`; if no, add only a prose note.
9. Add ops WARNs and eval/Testability Map assertions for all new contract and routing semantics.

## Gaps and Questions

None blocking after reconciliation. Canonical decisions are taken from the patched REPORT: real-boot-only Regression, telemetry-only `--no-reachability`, telemetry-only `spec-and-tasklist-absent`, explicit-annotation-only v1 blocking trigger, and R7's exact stable field names. Any earlier recommendations in this file that appear broader than those decisions are superseded by the canonical patched blocks above.

## Summary

FR-RH1 has no existing reachability/oracle subsection in the scoped files. The cleanest insertion is an additive UC-2 Wave 1A Step 5.6 immediately after the current Step 5.5 verification triangle, plus a minor stable contract bump to `1.6.0` with the exact R7 top-level `reachability_*` fields adjacent to existing verification fields. The most important related refs are `report-template.md`, `deviation-taxonomy.md`, `reflection-rubric.md`, and bounded-work cost docs; `ops-integration.md` and `grader-extensions.md` should be updated if WARN/eval surfaces are part of the implementation.
