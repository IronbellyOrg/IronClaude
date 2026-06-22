# Reflect Pre-Execution Report — FR-RH1 UC-2 Reachability Gate

**Mode:** pre (UC-1)
**Depth requested:** deep
**Tier reached:** 2 (forced by `--depth deep`)
**Status:** patched-success
**Calibrated confidence:** 0.91
**Spec:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md`
**Report generated:** 2026-06-20
**Patch status:** all recommended repairs from the original report are implemented below as a concrete requirements amendment.

## Executive verdict

The original audit correctly identified a valuable FR-RH1 concept: `/sc:reflect` UC-2 should not validate only observable divergence while missing whether a contracted side-effect reaches its durable sink. This patched report keeps that concept but replaces the ambiguous parts of the original spec with deterministic, implementation-ready rules.

**Patched verdict:** proceed only with the corrected v1 design below. The corrected design is narrower and safer than the original proposal:

- **Regression is real-boot-only.** Static evidence can create `unproven` Grounding Gaps, never `regression_present`.
- **`--no-reachability` is non-blocking telemetry.** It must not write a Grounding Gap and must restore prior behavior for rollback.
- **Spec-absent legacy paths are telemetry-only by default.** No spec/tasklist means no blocking reachability gate unless an explicit caller opts into fail-closed behavior in a later version.
- **The stable contract version is `1.6.0`.** The reachability fields are new top-level stable fields and must not ship under `1.5.0`.
- **Wrapper plumbing is in scope.** `superclaude reflect run` must expose and forward the same disable path as `/sc:reflect`.
- **Producer detection must be tested.** Contract fixture tests are not enough.
- **Field presence is specified.** UC-2 contracts must emit the reachability block consistently.
- **Cost is bounded, not zero.** The gate adds no new tool class, but it does add bounded work.

## Patched FR-RH1 requirements amendment

This section is the implementation-ready repair set. Apply it to the underlying FR-RH1 spec before building the task.

### R1 — Proof bar: `unreachable` Regression is real-boot-only

Replace all original text that allows static binding absence plus oracle mismatch to prove `unreachable` with the following rule:

```markdown
A reachability verdict is `unreachable` ONLY when a real-boot verifier runs and observes that the contracted sink is absent after exercising the booted entrypoint. Static signals — missing binding, discarded emitter result, or oracle mismatch — are advisory recall signals and can produce only `unproven` unless real boot proves the sink absence.
```

Corrected verdict mapping:

| Verdict | Condition | Class | Existing field set | Tier effect |
|---|---|---|---|---|
| `reachable` | Binding present, emitter result checked, and oracle observes the contracted sink | none | no reachability hard flag | none |
| `unreachable` | **Real boot ran and observed the contracted sink absent** | Regression | `reachability_unreachable += 1`, `verification_regressions_detected += 1`, `regression_present: true` | Trips §5.3 rule 3 |
| `unproven` | Any static fail-open signal without real-boot proof; unresolved sink identity; real boot unavailable; oracle mismatch without real-boot proof | Grounding Gap | one `grounding-gaps.yaml` row with `gap_kind` and `needs_human_decision: true` | Tier-1 preserved unless another rule escalates |

This resolves the original contradiction between “real boot is the only proof path” and “binding absence + oracle mismatch can be Regression.”

### R2 — Disable path: `--no-reachability` is telemetry-only

Replace any instruction saying `--no-reachability` “records the skip in Grounding Gaps” with:

```markdown
`--no-reachability` disables Step 5.6 and records only non-blocking telemetry/audit state: `reachability_gate_ran: false` and `reachability_skip_reason: --no-reachability`. It MUST NOT create or append to `grounding-gaps.yaml`, MUST NOT set `needs_human_decision`, and MUST NOT force `status: partial`. This flag is the operator rollback path and restores prior behavior for the reachability gate.
```

Required invariant:

```yaml
if reachability_skip_reason == "--no-reachability":
  reachability_gate_ran: false
  reachability_ledger_path: null
  reachability_requirements_scanned: 0
  reachability_unreachable: 0
  reachability_unproven: 0
  reachability_real_boot_ran: false
  # no reachability-created grounding gap
```

### R3 — Spec-absent legacy behavior: telemetry-only, not fail-closed

Replace the original spec-absent diff-side probe behavior with:

```markdown
When neither `--spec` nor `--tasklist` is supplied, Step 5.6 does not run a blocking reachability gate because there is no authoritative contracted sink. It may emit non-blocking telemetry if a diff-side discarded-emitter shape is observed, but it MUST NOT create a Grounding Gap, MUST NOT set `needs_human_decision`, and MUST NOT change the run status. The skip reason is `spec-and-tasklist-absent`.
```

Required invariant:

```yaml
if reachability_skip_reason == "spec-and-tasklist-absent":
  reachability_gate_ran: false
  reachability_ledger_path: null
  reachability_requirements_scanned: 0
  reachability_unreachable: 0
  reachability_unproven: 0
```

This preserves legacy callers while still allowing a future explicit opt-in fail-closed mode if needed.

### R4 — Contract version: bump reachability to `1.6.0`

The reachability stable fields are additive top-level fields, so the feature must ship as contract `1.6.0`, not `1.5.0`.

Patch the stable contract header to:

```yaml
contract_version: "1.6.0"   # 1.6.0 adds FR-RH1 runtime-reachability fields; 1.5.0 remains D13-only.
```

Update every fixture, report template reference, eval assertion, and version-stability test that includes the new reachability fields. `1.5.0` must continue to mean only the D13 additive contract: `coverage_pct_union`, `coverage_degraded`, and `unmapped_requirements_union`.

### R5 — Wrapper plumbing: `/sc:reflect` and `superclaude reflect run` must agree

Add implementation tasks for the Python wrapper path, not only slash-command documentation:

1. Add a wrapper config/model field for reachability, defaulting to enabled.
2. Add a Click option on `superclaude reflect run`, preferably `--reachability/--no-reachability` or a single `--no-reachability` flag.
3. Forward `--no-reachability` from `ReflectRunner._build_prompt()` into the generated `/sc:reflect` prompt when disabled.
4. Update `docs/guides/reflect-cli-tools-guide.md` and any generated command docs that list wrapper flags.
5. Add parity/smoke tests proving the wrapper option appears in `--help` and that `_build_prompt()` forwards `--no-reachability` exactly once.

Acceptance checks:

```text
superclaude reflect run --help includes --no-reachability
_build_prompt() includes --no-reachability when disabled
_build_prompt() omits --no-reachability by default
reflect CLI docs and Click option list stay in parity
```

### R6 — Producer-level eval fixture is mandatory

The deterministic `derive_verdict` fixture tests are retained, but they prove only consumer wiring. Add a producer-level eval fixture that forces Step 5.6 to produce the fields from real inputs.

Required eval fixture shape:

```text
.dev/eval-workspaces/sc-reflect/evals/uc2-reachability-unproven-proxy-oracle/
├── spec.md                 # contains an AC with explicit durable_sink: <sink-id>
├── tasklist.md             # maps the task to the durable_sink AC
├── before/                 # minimal source tree with contracted sink path wired or absent as required
├── after/                  # diff under audit: emitter-shaped call, missing binding or discarded result
├── tests/                  # proxy oracle that passes by checking stdout/journald/code-presence, not durable sink
└── expected.yaml           # expected reachability ledger + return-contract assertions
```

Required assertions:

```yaml
return-contract.yaml:
  contract_version: "1.6.0"
  reachability_gate_ran: true
  reachability_requirements_scanned: 1
  reachability_unreachable: 0
  reachability_unproven: 1
  needs_human_decision: true
  status: partial
runtime-reachability-ledger.yaml:
  - verdict: unproven
    contracted_sink: <sink-id>
    oracle_match: false
    gap_kind: oracle-mismatch
```

Add a second producer fixture for the real-boot-proven path only if a safe boot command can run under the Step 5.5 envelope; otherwise keep real-boot-proven Regression as an integration/eval-hardening follow-up.

### R7 — Field-presence and consistency rules

The reachability block is mandatory for every UC-2 return contract starting with `contract_version: "1.6.0"`. It is optional/absent for UC-1.

Stable fields:

```yaml
reachability_gate_ran: <bool>
reachability_ledger_path: <abs path> | null
reachability_requirements_scanned: <int>
reachability_unreachable: <int>
reachability_unproven: <int>
reachability_real_boot_ran: <bool>
reachability_skip_reason: --no-reachability|no-side-effect-requirements|spec-and-tasklist-absent|null
```

Consistency rules:

```yaml
# UC-2, gate ran
if reachability_gate_ran == true:
  reachability_skip_reason: null
  reachability_ledger_path: <non-null path>
  reachability_requirements_scanned: ">= 1"

# UC-2, no side-effect requirements
if reachability_skip_reason == "no-side-effect-requirements":
  reachability_gate_ran: false
  reachability_ledger_path: null
  reachability_requirements_scanned: 0
  reachability_unreachable: 0
  reachability_unproven: 0

# UC-2, no-reachability disabled
if reachability_skip_reason == "--no-reachability":
  reachability_gate_ran: false
  reachability_ledger_path: null
  reachability_unreachable: 0
  reachability_unproven: 0
  needs_human_decision must not be set solely by reachability

# UC-2, unreachable
if reachability_unreachable > 0:
  reachability_real_boot_ran: true
  regression_present: true
  verification_regressions_detected: ">= reachability_unreachable"

# UC-2, unproven
if reachability_unproven > 0:
  grounding_gaps_path: <non-null path>
  needs_human_decision: true
```

### R8 — Cost profile: bounded added work, not zero work

Replace `reachability_gate_added_tokens: 0` and `reachability_gate_added_turns: 0` with bounded estimates:

```yaml
reachability_gate_added_tool_classes: 0
reachability_gate_added_turns_per_side_effect_requirement: "1-3"
reachability_gate_max_side_effect_requirements_scanned: 12
reachability_gate_added_turns_cap: 36
reachability_gate_real_boot_invocations_cap: 1
```

Clarifying text:

```markdown
The gate adds no new tool class because it reuses Step 4 symbol references, Step 6 re-Read, and Step 5.5 verification. It still adds bounded orchestration work per side-effect requirement. The v1 cap is 12 side-effect-bearing requirements; overflow sets `reachability_sampled: true` in telemetry and routes unexamined rows to a non-blocking coverage warning unless a high-stakes `durable_sink:` annotation is present.
```

### R9 — Semantic fallback rollout: advisory until precision is proven

For v1, use explicit `durable_sink:` / `@sink` annotations as the only blocking trigger. Semantic classification may produce advisory telemetry but cannot create a Grounding Gap.

Patched trigger predicate:

```markdown
A side-effect-bearing requirement is blocking-gate eligible only when the acceptance criterion includes an explicit machine-readable `durable_sink:` or `@sink` annotation. Without an explicit annotation, semantic classification may record an advisory candidate but MUST NOT set `reachability_unproven`, MUST NOT write a reachability Grounding Gap, and MUST NOT affect `status`.
```

This prevents default-on halt fatigue while preserving the long-term path to semantic fallback after eval precision data exists.

## Patched implementation checklist

Use this checklist instead of the original “Recommended minimum repair set”:

- [ ] Replace all `binding absent AND oracle_mismatch => unreachable` language with real-boot-only Regression.
- [ ] Change `--no-reachability` to telemetry-only skip; no Grounding Gap, no `needs_human_decision`, no `status: partial`.
- [ ] Change spec-absent behavior to telemetry-only skip with `reachability_skip_reason: spec-and-tasklist-absent`.
- [ ] Bump the reachability contract version to `1.6.0` everywhere new fields appear.
- [ ] Add wrapper-level `--no-reachability` plumbing and docs parity tests.
- [ ] Add the producer-level eval fixture for `unproven` proxy-oracle behavior.
- [ ] Enforce reachability field-presence and consistency rules for UC-2 contracts.
- [ ] Replace zero-cost claims with bounded estimates and caps.
- [ ] Make semantic fallback advisory-only in v1; blocking gate requires explicit `durable_sink:` / `@sink`.

## Superseded original findings

The original report findings B1-B3 and I1-I3 are now superseded by the patched amendment above. They are not deleted conceptually; each maps to a repaired rule:

| Original finding | Patched by |
|---|---|
| B1 proof-bar contradiction | R1 real-boot-only Regression |
| B2 never-STOP / rollback conflict | R2 non-blocking disable path + R3 spec-absent telemetry-only |
| B3 contract-version violation | R4 contract `1.6.0` |
| I1 missing wrapper plumbing | R5 wrapper and docs parity tasks |
| I2 consumer-only tests | R6 producer-level eval fixture |
| I3 zero-cost and semantic fallback risk | R8 bounded cost + R9 advisory semantic fallback |

## Evidence-validator note

The patched report is an artifact-level requirements amendment. It does not modify the underlying source spec or code. The source citations from the original report were re-read before patching; no citation-grounding issue was found. The patched content intentionally removes the original ambiguity by replacing recommendations with concrete normative rules and acceptance checks.
