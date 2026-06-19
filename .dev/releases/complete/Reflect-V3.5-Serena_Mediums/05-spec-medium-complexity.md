---
title: "sc:reflect V3 — Serena Medium-Complexity Adoption (execute_shell_command + onboarding + Tier-3 handoff + type_hierarchy)"
version: "1.0.0"
status: draft
feature_id: FR-RV3-MED
parent_feature: null
spec_type: new_feature
complexity_score: 0.6
complexity_class: MEDIUM
target_release: sc-reflect-v3
authors: [user, claude]
created: 2026-06-01
quality_scores:
  clarity: 8.8
  completeness: 9.0
  testability: 9.0
  consistency: 8.8
  overall: 8.9
---

## 1. Problem Statement

> What problem does this work solve? Why does it matter? What fails or is suboptimal today?

sc:reflect's architectural bet (SKILL.md §1, summarised in `03-conversation-context.md` §2) is that **Serena's symbolic chain is the load-bearing grounding mechanism** and that every Serena call is fail-open so depth degrades rather than breaking the skill. The low-complexity adoption (sibling spec `Reflect-V3-Serena/04-spec-low-complexity.md`) hardens the *symbolic-evidence* and *memory-lifecycle* surfaces. This spec closes the four remaining **medium-complexity, high-value** gaps — the ones that require a new conditional code path, a flag gate, a safety envelope, or a memory-schema addition rather than a one-line chain extension.

Four concrete gaps exist today against the current Serena release line:

1. **The biggest false-PASS path in UC-2 is unverified.** The §6.1 evidence chain (SKILL.md:354-367) ends at `get_diagnostics_for_file` (LSP issues) and a re-Read. There is **no mechanism that actually runs the tests**. The §10.4 Regression detector (SKILL.md:718-730) is reduced to "detect via task log or by re-running tests **if `--rerun-tests` set**" (SKILL.md:725) — an opt-in, off-by-default path. So in the common case sc:reflect classifies Regression from *what the task log claims*, not from *what the test suite does*. The single most common false-PASS — "task log says tests pass; they don't" — sails through the §14.5.2 promotion gate's condition 4 (`deviation_count_by_class.regression == 0`, SKILL.md:1097).
2. **Cold-start runs have no calibration baseline.** The first time sc:reflect runs on a project, Wave 0 memory hydrate (SKILL.md:134) finds nothing — `reflect/last-pass-{slug}` and `reflect/deviation-patterns-{slug}` are empty, and so are Serena's own project memories. There is no bootstrap step that analyses project structure / build system / test setup to seed that baseline, so first-run deviation calibration is at its weakest exactly when the operator most needs signal.
3. **The Tier 3 remediation handoff starts cold.** When `--remediate` escalates to Wave 6 task-builder (SKILL.md:417, 458), the next conversation must re-derive the rubric scores, deviation set, and evidence packet that Waves 1-5 already computed — re-running expensive grounding the handing-off run already paid for.
4. **Polymorphic family completeness is ungrounded.** Even with the low-spec's `find_implementations` adoption, sc:reflect cannot retrieve a type's *transitive* supertype/subtype family in one call. UC-1 coverage questions of the form "are all subclasses of `BaseAgent` wired into the registry?" degenerate to iterative grep heuristics on object-oriented codebases.

The dominant *hazard* this spec introduces — and the reason its panel focus carries `compliance` — is gap 1's fix: `execute_shell_command` runs arbitrary shell via `subprocess.Popen(command, shell=True)` with **no upstream allowlist or sandbox** (Serena Security Audit #380, cited `02-matrix:236,268`). The safety envelope (verb allowlist, timeout, output cap, no-mutation gate) is the bulk of the work and the core correctness surface; the integration itself is small.

### 1.1 Evidence

> Concrete evidence that the problem exists. Links to issues, failing tests, user reports, forensic findings.

| Evidence | Source | Impact |
|----------|--------|--------|
| §6.1 chain ends at `get_diagnostics_for_file` + re-Read; no test-execution step | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:354-367` | UC-2 Regression class self-reported, not verified — largest false-PASS path |
| Regression detection is opt-in: "re-running tests **if `--rerun-tests` set**" | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:725` | Tests not run by default; promotion gate cond 4 (regression==0) trusts the task log |
| Promotion gate cond 4 blocks on `regression == 0` but has no verified-regression source | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:1097` | Unverified PASS promotes work-unit to `done`/`complete` |
| Wave 0 memory hydrate finds nothing on first run; no project-bootstrap step exists | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:134,373-383` | Cold-start deviation calibration has no baseline |
| Tier 3 task-builder handoff (Wave 6) re-derives Waves 1-5 context | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:417,458` | 30-60% redundant handoff context per `02-matrix:17` |
| `execute_shell_command` uses `shell=True`, no whitelist/sandbox; excluded by default in `ide-assistant`/`claude-code` + blocked by `read_only: true` | `02-matrix:236,256,267` (Security Audit #380, issue #494, issue #92) | Hazard surface requires consumer-side safety envelope; availability not guaranteed |
| `type_hierarchy` is JetBrains-strong / LSP-partial; coverage matrix unresolved | `02-matrix:40-43,64-66` (news entry vs README capability table) | Backend-dependent; must probe before invoking, degrade on unsupported |
| `prepare_for_new_conversation` signature is "the largest research gap of any of the four" | `02-matrix:194,369` | Parameter shape unknown; requires live-surface probe before wiring |

### 1.2 Scope Boundary

> What this spec addresses and explicitly does NOT address.

**In scope**: The 4 medium-complexity / high-value Serena adoptions enumerated in `02-matrix-medium-complexity.md` — `type_hierarchy` (row 1), `onboarding` (row 2), `prepare_for_new_conversation` (row 3), and `execute_shell_command` (row 4). All wiring is additive to `SKILL.md` + `refs/*.md`; all calls inherit §6.5 fail-open semantics (SKILL.md:397-399); all emit telemetry fields. `execute_shell_command` and `onboarding` introduce **new user-facing flags** (`--no-verify` and `--onboard` respectively); `type_hierarchy` introduces `--with-hierarchy`.

**Out of scope**:
- **Low-complexity adoptions** (`find_implementations`, `find_declaration`, `find_referencing_symbols(include_info)`, `find_symbol(search_deps)`, `summarize_changes`, onboarding-status parse, `get_current_config`, memory CRUD trio) — these belong to the sibling `Reflect-V3-Serena/04-spec-low-complexity.md`. **Note the cross-spec dependency**: FR-RV3-MED.1 (`type_hierarchy`) and FR-RV3-MED.2 (`onboarding`) both consume the low-spec's FR-RV3-LOW.7 `get_current_config` version-fingerprint / backend-probe substrate; see §11 OQ-M5.
- **Symbolic editing / project-mutating tools** (`insert_before_symbol`, `replace_symbol_body`, `rename_symbol`, `safe_delete_symbol`, `replace_content`) — out of bounds under the §3 read-only-with-respect-to-source posture; route to Tier 3 task-builder per `03-conversation-context.md` §5.
- **`switch_modes` / custom Contexts/Modes, HTTP/SSE transport, `initial_instructions`, `restart_language_server`, dashboard surface** — excluded per `03-conversation-context.md` §5.
- **Source-code remediation** of any deviation sc:reflect detects — Tier 3 / task-builder surface, never sc:reflect itself. `execute_shell_command` runs **non-mutating verification only** (tests/linters/type-checkers/build); it MUST NOT `git commit`, `git push`, install packages, or write outside `<output>/` (`03-conversation-context.md` §3).
- **Task-file authoring** — downstream `/task-builder` responsibility, not this spec.

## 2. Solution Overview

> High-level description of the approach. What changes, what stays the same.

Extend sc:reflect's Serena footprint with four additive, fail-open, medium-complexity adoptions, each wired at the precise wave-insertion point the matrix research identifies:

- **`execute_shell_command` (ship FIRST)** completes the **verification triangle** — `get_diagnostics_for_file` (LSP issues) + `summarize_changes` (what changed) + `execute_shell_command` (does it pass). A new §6.1 step 5.5 runs scoped verification commands behind a **consumer-side safety envelope** (verb allowlist, `timeout` wrap, output cap, no-mutation gate, per-call audit row). Real exit codes feed the §10.4 Regression detector and a new `verification_regressions_detected` count that deterministically promotes a hunk to the Regression class — closing the §14.5.2 condition-4 false-PASS path. Default-on in UC-2; `--no-verify` opt-out. This **subsumes the existing opt-in `--rerun-tests` semantics** (SKILL.md:725) into a default-on, allowlisted, time-boxed mechanism (see §2.1 / OQ-M2).
- **`onboarding` (ship SECOND)** adds an optional Wave 0 sub-step (0.7b), gated behind `--onboard` and on `list_memories` returning empty for the project slug, that seeds the cold-start calibration baseline. Never auto-triggers; verifies post-onboarding memory existence (silent-fail guard); one-shot per project.
- **`prepare_for_new_conversation` (ship THIRD)** defines a `reflect/handoff-{slug}-{timestamp}` memory schema written at Wave 5/6 just before the Wave 6 task-builder handoff, recovering rubric scores + deviation set + evidence packet so the remediation conversation resumes warm. Falls back to plain `write_memory` when the tool is context-excluded.
- **`type_hierarchy` (ship LAST)** extends the §6.1 chain (new step 4.5) and Wave 1B.3 with transitive supertype/subtype retrieval for registry-completeness verification, behind a Wave 0 backend probe and a `--with-hierarchy` opt-in; non-OO codebases see zero degradation when unshipped.

What stays the same: the wave/tier architecture (SKILL.md §4), the rubric (§5), the evidence-validator gate (Wave 5), the read-only-with-respect-to-source posture, the per-step audit emit convention (SKILL.md:124), and the §6.5 fail-open envelope. No new wave is introduced — every adoption plugs into an existing wave/step. The four adoptions ship as **separate PRs** per the matrix ordering (§8).

### 2.1 Key Design Decisions

> Decisions made during brainstorming/design that shaped this spec. Each decision should have a rationale.

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| `execute_shell_command` (matrix row 4) | **adopt — default-on in UC-2, `--no-verify` opt-out, ship FIRST** | skip / opt-in only / wrap in task-builder | Highest single-feature ROI: closes the largest false-PASS path in §10.4 Regression detection by moving from "task log *claims* PASS" to "orchestrator *verified* PASS". Within posture (`03-conversation-context.md` §3: reflect may run non-mutating verification). Complexity is the safety envelope, not the integration. (`02-matrix:18,352`) |
| Safety envelope location | **consumer-side (sc:reflect), not the tool** | rely on Serena tool-level limits | Serena imposes no allowlist/sandbox (`shell=True`, Security Audit #380) and no surfaced default timeout. The envelope MUST live in sc:reflect: verb allowlist, `timeout <N>` wrap, 50 KB output cap, no-mutation gate, per-call audit. (`02-matrix:24,261,269`) |
| `--rerun-tests` vs `--no-verify` | **subsume `--rerun-tests` into default-on verification; add `--no-verify` to disable** | keep `--rerun-tests` opt-in alongside | Two flags governing the same behavior is incoherent. The matrix recommends default-on + `--no-verify` (`02-matrix:18,25`). `--rerun-tests` (SKILL.md:725) becomes a deprecated alias for "verification on" (the default). Flag-migration tracked as OQ-M2. |
| `onboarding` (matrix row 2) | **adopt — opt-in `--onboard`, gated on empty memory, ship SECOND** | skip / default-on | High value at cold-start, near-zero on warm-start (`02-matrix:16`). MUST be opt-in: auto-onboarding surprised users by creating `.serena/` implicitly (discussion #1513, `02-matrix:128`), and it consumes significant context (`02-matrix:122`). One-shot per project. |
| `prepare_for_new_conversation` (matrix row 3) | **adopt — Tier 3 handoff bridge, ship THIRD** | skip / defer indefinitely | 30-60% token saving on the remediation chain, but ONLY realized when `--remediate` runs (`02-matrix:17,356`). Value scales with Tier 3 frequency. Treat as a Wave 6 enhancement, not a Wave 0/1 dependency. Signature is the largest research gap → runtime-probe before parameter-dependent wiring (OQ-M1). |
| `prepare_for_new_conversation` fallback | **fall back to `write_memory` with an inline-built summary blob** | hard-fail / skip handoff | Tool is excluded by default in `ide-assistant`/`claude-code` context (issue #494, `02-matrix:193`) — the most likely runtime path. Extend the existing §14 "Serena `write_memory` fails at Wave 5" handler (SKILL.md:1067). (`02-matrix:222`) |
| `type_hierarchy` (matrix row 1) | **adopt — `--with-hierarchy` opt-in, backend-probe gated, ship LAST** | skip / default-on | High UC-1 value on OO codebases, but JetBrains-strong / LSP-partial with an unresolved coverage matrix (`02-matrix:40-43,64`). `--with-hierarchy` default-off on LSP backends means non-OO codebases see no degradation. v1.1-grade enhancement after the first three stabilize. (`02-matrix:358,372`) |
| Cross-spec config dependency | **consume low-spec FR-RV3-LOW.7 `get_current_config`; provide a minimal inline probe if low-spec not yet merged** | duplicate the probe / hard-depend on low-spec | `type_hierarchy` backend detection and `execute_shell_command`/`onboarding` availability detection all need the active-context/version snapshot the low-spec's FR-7 provides. Reuse it; if this medium PR lands first, ship a minimal `get_current_config` probe and reconcile at low-spec merge. Tracked as OQ-M5. |
| Verification triangle co-design | **co-design `verify_*` audit shape with the existing `get_diagnostics_for_file` step** | independent schema | Avoids two consecutive contract minor bumps; the triangle is named explicitly in the matrix (`02-matrix:340,362`). |

### 2.2 Workflow / Data Flow

> How the system works end-to-end after this change. Use ASCII diagrams for pipeline flows.

```
sc:reflect wave structure — Serena Medium-Complexity adoption insertion map
(SKILL.md section anchors quoted; arrows show where each matrix row plugs in)

 WAVE 0  Parse + Validate + Activate Project + Memory Hydrate        [SKILL.md §4.0 :172-225]
 ├─ 0.5  env-var alias resolution                                    [SKILL.md :132,197]
 ├─ 0.5c get_current_config (backend + version + excluded_tools)     [low-spec FR-7; OQ-M5]
 │        → backend ∈ {jetbrains,lsp,none}; execute_shell_command_available; onboarding_available
 ├─ 0.7  activate_project + memory hydrate                           [SKILL.md :134]
 ├─ 0.7b onboarding bootstrap  ◀── ROW 2  (NEW; only when --onboard AND list_memories empty)
 │        → probe context-availability → onboarding() → verify memory delta (silent-fail guard)
 │        → onboarding_ran / onboarding_succeeded / onboarding_memories_written
 └─ 0.8  open audit log

 WAVE 1  Tier 1 — Grounded Single-Agent Reflection
 ├─ 1A   §6.1 Mandatory evidence-gathering chain                     [SKILL.md §6.1 :354-367]
 │        2. get_symbols_overview <file>
 │        3. find_symbol <symbol>
 │        4. find_referencing_symbols <symbol>
 │        4.5 type_hierarchy(hierarchy_type=both|subtypes, depth=0) ◀── ROW 1
 │            (NEW; only when backend supports it AND --with-hierarchy AND kind is a type)
 │        5. get_diagnostics_for_file <file>          ┐
 │        5.5 execute_shell_command (scoped verify)   │ ◀── ROW 4  (NEW; verification triangle)
 │            └─ SAFETY ENVELOPE: verb allowlist · timeout <N> wrap · 50KB cap ·
 │               no-mutation gate · per-call audit row · cwd=affected subtree
 │            → verify_exit_code feeds §10.4 Regression detector  [SKILL.md :718-730]
 │        6. re-Read cited file:line  [SKILL.md §6.2 :369-371 ; CLAUDE.md S1]
 │        verification triangle = diagnostics(5) + summarize_changes(low-spec) + verify(5.5)
 ├─ 1B.3 cross-task interaction-effects scan (UC-2, ≥3 tasks)        [SKILL.md §4.1 :233-241]
 │        ◀── ROW 1  type_hierarchy(subtypes) on shared base-class hotspots = HIGH-severity edge
 ├─ 1C   single-agent reflection
 └─ 1D   blind calibration (confidence-calibrator)

 WAVE 2  Tier-Decision Gate (rubric §5)   ── S_dev_density consumes ROW 1/ROW 4 signals  [:276-304]
 WAVE 3  Tier 2 reviewers  ── ROW 1 hierarchy slice + ROW 4 verify results land in briefs [§4.3 :245]
 WAVE 4  Adversarial merge
 WAVE 5  Synthesis + Evidence-Validator Gate + Report               [SKILL.md §4.5 :249-257]
 │        ◀── ROW 4  re-verify pre-synthesis; verification_regressions_detected → regression_present
 └─ §6.3 memory persist                                             [SKILL.md §6.3 :373-383]
          ◀── ROW 3  prepare_for_new_conversation → reflect/handoff-{slug}-{ts}  (when --remediate)

 WAVE 6  Tier 3 — Remediation Handoff (conditional, --remediate)    [SKILL.md §7 :417 ; §8 :458]
 │        ◀── ROW 3  write reflect/handoff-{slug}-{ts} BEFORE task-builder invoke
 │             fallback → write_memory(inline summary)  [extends §14 row :1067]
 └─ task-builder consumes handoff memory key → warm-start remediation

 WAVE 7  Promotion Mutation (UC-2 only — §14.5)                      [SKILL.md §14.5.2 :1090-1112]
          ◀── ROW 4  verification_regressions_detected > 0 → regression_present:true [:557]
              → gate condition 4 (regression==0, :1097) BLOCKS promotion  ← closes false-PASS path

 §6.5 FAIL-OPEN ENVELOPE wraps every NEW call above                 [SKILL.md §6.5 :397-399]
          missing/error/excluded → degraded:[<tool>] audit entry → degrade signal → continue
```

## 3. Functional Requirements

> Numbered requirements. Each must be testable and traceable.
>
> **Identifier convention**: `FR-RV3-MED.N` names a requirement; `FR-N.M` in its acceptance-criteria list is shorthand for "criterion M of FR-RV3-MED.N" (e.g. `FR-4.3` ≡ criterion 3 of `FR-RV3-MED.4`). Downstream task-builder should map `FR-N.M` → `FR-RV3-MED.N.M`. FRs are numbered by matrix row; **ship order is the reverse** (see §4.6 / §8): row 4 first, then 2, 3, 1.

### FR-RV3-MED.1: `type_hierarchy` transitive family coverage (Wave 1A + 1B.3)

**Description**: Add §6.1 step 4.5 (between `find_referencing_symbols` step 4 and `get_diagnostics_for_file` step 5, SKILL.md:362-363) invoking `mcp__serena__type_hierarchy(relative_path, name_path, hierarchy_type, depth=0)` to retrieve the transitive supertype/subtype family of a spec-referenced type, **only when** (a) the Wave 0 backend probe reports a hierarchy-capable backend, (b) `--with-hierarchy` is set, and (c) the located symbol is a type. Also add a `type_hierarchy(hierarchy_type=subtypes)` pass to Wave 1B.3 (SKILL.md:233-241) when the cross-task scan identifies a shared base-class symbol as a top-30 hotspot. Closes the structural gap that referencing call sites alone cannot derive a type's *family* (`02-matrix:97`). (`02-matrix:40-98`)

**Backend gating (operational)**: `type_hierarchy` is JetBrains-strong; LSP coverage is language-server-dependent and unresolved (`02-matrix:64-66`). The Wave 0 probe classifies the backend as `jetbrains | lsp | none`; `--with-hierarchy` defaults **off on `lsp`** until OQ-M3 empirically confirms per-language support, and is unavailable on `none`.

**Acceptance Criteria**:

- [ ] FR-1.1 PASS when, for a UC-1 input referencing a type on a hierarchy-capable backend with `--with-hierarchy` set, Wave 1A emits `type_hierarchy_invoked: true` in `audit.log` for ≥1 symbol.
- [ ] FR-1.2 PASS when `hierarchy_backend: jetbrains|lsp|none`, `hierarchy_nodes_examined: <int>`, and `hierarchy_gaps_found: <int>` are present in the audit row for that step.
- [ ] FR-1.3 PASS when the return contract (§9.1 UC-1 block) carries `hierarchy_slice_path: <abs-path>` (materialized at `<output>/artifacts/hierarchy-slice.yaml`) and `hierarchy_coverage_pct: <float 0.0-1.0> | null`, defined as **`registered_subtypes / total_subtypes_in_hierarchy`** (the share of the type's transitive subtype family that the tasklist/spec accounts for; `null` when the hierarchy is empty or the backend is unavailable — resolves m-ARC1).
- [ ] FR-1.4 PASS when the Wave 0 backend probe reports `none` (or `lsp` without `--with-hierarchy`): Wave 1A emits `type_hierarchy_invoked: false`, `hierarchy_backend: none|lsp-disabled`, and skips step 4.5 with **no degrade entry** (absence is expected, not a failure — resolves the degenerate-no-op case).
- [ ] FR-1.5 PASS when an explicit backend/LSP error (distinct from "backend unsupported") emits `degraded: ["type_hierarchy:backend_error"]` and falls back to the existing `find_implementations`/`find_referencing_symbols` chain without blocking.
- [ ] FR-1.6 PASS when Wave 1B.3 flags a shared base-class hotspot as a HIGH-severity interaction edge only after `type_hierarchy(subtypes)` confirms genuine shared lineage (not a name collision).

**Telemetry**: `type_hierarchy_invoked`, `hierarchy_backend`, `hierarchy_nodes_examined`, `hierarchy_gaps_found`; contract: `hierarchy_slice_path`, `hierarchy_coverage_pct`.

**Fail-open behavior** (§6.5, SKILL.md:397-399): backend `none`/`lsp-disabled` → skip step 4.5, no degrade (expected absence). Explicit backend error → `degraded: ["type_hierarchy:backend_error"]` → `find_implementations`/grep fallback → continue. The skill MUST never abort because hierarchy is unavailable.

**Dependencies**: low-spec **FR-RV3-LOW.7** (`get_current_config` backend probe) — see OQ-M5. Serena ≥ v1.0.0 (JetBrains backend; news entry dates JetBrains-side tool to 2026-01-11, `02-matrix:69`). Ships LAST.

### FR-RV3-MED.2: `onboarding` cold-start calibration bootstrap (Wave 0.7b, `--onboard`)

**Description**: Add Wave 0 sub-step 0.7b (after activate_project + memory hydrate, SKILL.md:134) that, **only when `--onboard` is set AND `list_memories` returns empty for the project slug**, probes whether the `onboarding` tool is exposed in the active context and, if so, invokes `mcp__serena__onboarding()` to seed Serena's project memories (`project_structure`, `suggested_commands`, `testing_setup`, etc.). Verifies a post-onboarding memory-count delta as the silent-fail guard. One-shot per project; never auto-triggers. Strengthens the §6.3 cold-start calibration baseline (`02-matrix:102-166`).

**Acceptance Criteria**:

- [ ] FR-2.1 PASS when, with `--onboard` set and no existing project memories on a context that exposes the tool, Wave 0 emits `onboarding_ran: true` in `audit.log`.
- [ ] FR-2.2 PASS when a post-onboarding `list_memories` delta of ≤ 0 emits `onboarding_succeeded: false` + a WARN ("onboarding completed but no new memories written"), and a positive delta emits `onboarding_succeeded: true` with `onboarding_memories_written: [<list>]` (silent-fail guard, `02-matrix:130`).
- [ ] FR-2.3 PASS when `--onboard` is set but the tool is excluded from the active context: emit `onboarding_ran: false`, `onboarding_skipped_reason: "context-excluded"`, and a WARN telling the operator to switch context — **never a hard STOP** (`02-matrix:162`).
- [ ] FR-2.4 PASS when `list_memories` is non-empty for the slug (warm start): step 0.7b is skipped with `onboarding_ran: false`, `onboarding_skipped_reason: "memories-present"` (gate-on-absence, `02-matrix:121`).
- [ ] FR-2.5 PASS when `--onboard` is NOT set: step 0.7b never executes and **never** creates a `.serena/` directory implicitly (anti-surprise, `02-matrix:128`).
- [ ] FR-2.6 PASS when a `global/memory_maintenance` memory is present: onboarding does NOT overwrite it (precedence honored, `02-matrix:123`).

**Telemetry**: `onboarding_ran`, `onboarding_succeeded`, `onboarding_memories_written`, `onboarding_skipped_reason`; contract: `onboarding_ran` (top-level), `onboarding_memories_count` (telemetry block).

**Fail-open behavior** (§6.5): tool unavailable in active context → skip with audit row + WARN; never block. Explicit `--onboard` against an excluding context → loud WARN, not STOP.

**Dependencies**: low-spec **FR-RV3-LOW.7** (active-context detection informs availability). Independent of FR-1/3/4. Ships SECOND.

### FR-RV3-MED.3: `prepare_for_new_conversation` Tier-3 handoff bridge (Wave 5/6)

**Description**: Define a new `reflect/handoff-{slug}-{timestamp}` memory schema carrying the in-flight rubric scores, deviation set, evidence packet, and reviewer verdicts. At Wave 6, immediately before the task-builder handoff (SKILL.md:417,458), invoke `mcp__serena__prepare_for_new_conversation` (or its verified-signature equivalent) to materialize that blob, then pass its key to task-builder so the remediation conversation resumes warm. **The tool signature is unverified** (`02-matrix:194`) — implementation MUST probe the live MCP surface before parameter-dependent wiring (OQ-M1). (`02-matrix:170-227`)

**Acceptance Criteria**:

- [ ] FR-3.1 PASS when, on a `--remediate`-accepted Tier 3 run with the tool available, Wave 6 emits `handoff_memory_written: true` and `handoff_memory_key: reflect/handoff-{slug}-{timestamp}` in `audit.log`, written BEFORE the task-builder invocation.
- [ ] FR-3.2 PASS when the return contract (§9.1 Tier 3 block) carries `handoff_memory_key: <serena-memory-name> | null` and `handoff_payload_size_bytes: <int>`.
- [ ] FR-3.3 PASS when the tool is context-excluded: the step falls back to `mcp__serena__write_memory` with an inline-built summary blob, emits `handoff_persist_method: write_memory_fallback`, and still hands the key to task-builder (extends SKILL.md:1067).
- [ ] FR-3.4 PASS when both the tool and `write_memory` fail: emit `handoff_persist_failed: true`, surface findings to task-builder WITHOUT the handoff key, and never block the report (`02-matrix:222`).
- [ ] FR-3.5 PASS when `--remediate` is NOT accepted (no Tier 3): the handoff step never runs; `handoff_memory_key: null` (degenerate no-op, not a failure).
- [ ] FR-3.6 PASS when the runtime-probed signature differs from the assumed shape: the implementer's MDTM is directed to OQ-M1 resolution rather than wiring assumed parameters.
- [ ] FR-3.7 PASS (M-ARC2) when the low-spec FR-RV3-LOW.8 retention sweep's prefix set is extended to include `reflect/handoff-*`, so handoff memories are pruned under the shared 90-day-expire / 20-entry-cap policy and do NOT accumulate unbounded across `--remediate` runs — verified by an eval asserting N>20 handoff entries trigger a sweep. (Cross-spec coordination: the sweep lives in the low-spec; this FR records the required prefix extension.)

**Telemetry**: `handoff_memory_written`, `handoff_payload_size_bytes`, `handoff_persist_method`, `handoff_persist_failed`; contract: `handoff_memory_key`.

**Fail-open behavior** (§6.5 + SKILL.md:1067): tool excluded → `write_memory` fallback; both fail → `handoff_persist_failed: true` → task-builder proceeds cold → report still ships.

**Dependencies**: signature OQ-M1 MUST resolve before parameter-dependent merge. Independent of FR-1/2/4. Ships THIRD; value scales with `--remediate` frequency.

### FR-RV3-MED.4: `execute_shell_command` verification triangle (Wave 1A step 5.5, default-on, `--no-verify`)

**Description**: Add §6.1 step 5.5 (between `get_diagnostics_for_file` step 5 and re-Read step 6, SKILL.md:363-364) that, **in UC-2 by default** (UC-1 verification is out of scope for v1 — see OQ-M4), runs scoped verification commands (`pytest`, `ruff`, `mypy`, `make test`, `uv run`, build) against the affected subtree via `mcp__serena__execute_shell_command`, behind a **consumer-side safety envelope**, and feeds real exit codes — **via the exit-code → deviation-class taxonomy below** — into the §10.4 Regression detector (SKILL.md:718-730). A *Regression-classified* non-zero exit on a tasklist-claimed-passing file sets `regression_present: true` (SKILL.md:557), which the §14.5.2 condition-4 gate (SKILL.md:1097) consumes to block promotion. This **subsumes the opt-in `--rerun-tests` path** (SKILL.md:725) into default-on behavior with a `--no-verify` opt-out. (`02-matrix:230-345`)

**Verify-state invariant (resolves review finding M-COR1)**: each step-5.5 invocation has exactly one terminal `verification_state ∈ {not-run, blocked, ran-pass, ran-fail, timeout, skipped}` (initial `not-run`); `regression_present` is a write-once latch within a run; `verification_regressions_detected` is monotonic non-decreasing. (Full State Variable Registry in the spec-panel review artifact `05-spec-medium-complexity.md.review.md`.)

**Safety envelope (mandatory — resolves CRITICAL C1)**: a first-token allowlist is **necessary but not sufficient** under Serena's `shell=True` execution (`02-matrix:236,247`) — an allowlisted first verb still lets shell metacharacters chain a mutation (e.g. `pytest ; rm -rf src`). The envelope therefore validates the **whole command structure**, not just the first token:
  - (a) **Template construction, not prose assembly** — the command MUST be built from a fixed allowlisted-verb template with arguments supplied as a vetted token list; the command string is NEVER assembled from raw spec/tasklist prose (which is untrusted by definition, `02-matrix:268`).
  - (b) **Verb allowlist** — first token ∈ {`pytest`,`ruff`,`mypy`,`make`,`uv`,`npm`,`tsc`,`cargo`,...}, else `verify_blocked`.
  - (c) **Metacharacter rejection (the C1 fix)** — reject outright with `verify_blocked_reason: "metachar-denied"` any command containing a shell control character (`; | & $ \` > < newline ( )`). A denylist of mutation *verbs* alone is insufficient against `shell=True` composition; the structural metachar gate is the load-bearing control.
  - (d) **Per-call timeout** — wrap as `timeout <N> <cmd>` (default 120s, max 600s) because Serena's tool-level timeout is unverified (`02-matrix:269`).
  - (e) **Output cap** — `max_answer_chars=51200` + defensive tail-truncate (tighter than the 200 KB default, `02-matrix:270`).
  - (f) **`cwd` scoping** — scope to the affected subtree as blast-radius reduction (`02-matrix:263`).
  - (g) **Per-invocation audit** — written to `<output>/verify-logs/invocations.yaml` and referenced via the audit row's `evidence_ref` field; NOT inlined into the fixed 5-field per-step audit row (SKILL.md:124 — resolves M-ARC1).
  - (h) **`--no-verify`** disables globally.

**Exit-code → deviation-class taxonomy (resolves CRITICAL C2)**: a non-zero exit is NOT uniformly a Regression. Classification (per-tool; defaults below, full table is OQ-M9):

| Tool / exit | Class | Effect |
|-------------|-------|--------|
| `pytest` exit 1 (test failed) | **Regression** candidate | `verification_regressions_detected += 1`; `regression_present: true` |
| `pytest` exit 2/3 (collection / internal error) | **Grounding Gap** (§10.6) | NOT a regression; `needs_human_decision` per §10.6 |
| `pytest` exit 5 (no tests collected) | **Drift / coverage** (§10.3) | claimed-added test absent; NOT a regression (respects §10.5 precedence *by evidence*, not by assignment) |
| `ruff` / `mypy` exit 1 (lint / type finding) | `S_dev_density` signal | feeds rubric; NOT `regression_present` |
| any tool exit 124 (timeout, FR-4.6) | **Grounding Gap** | `verify_timeout_hit: true`; NOT a regression |
| flaky (retry flips result, M-CMP2) | **Grounding Gap** + `verify_flaky_suspected: true` | single-retry-on-failure BEFORE classifying as Regression |

**Acceptance Criteria**:

- [ ] FR-4.1 PASS when, in a default UC-2 run on a verification-capable context, Wave 1A emits `verification_ran: true`, a scalar `verification_invocations: <int>` count, and an `evidence_ref` pointing at `<output>/verify-logs/invocations.yaml` (the per-invocation array `[{cmd, exit_code, duration_ms, stdout_path, stderr_path, blocked_reason, deviation_class}]` lives in that artifact, NOT inline in the fixed 5-field audit row — resolves M-ARC1).
- [ ] FR-4.2 PASS when a command whose first verb is NOT in the allowlist emits `verify_blocked: true` + `verify_blocked_reason: "verb '<v>' not in allowlist"` and is **not** invoked.
- [ ] FR-4.2b PASS (C1) when a command containing any shell control character (`; | & $ \` > < newline ( )`) is rejected with `verify_blocked: true` + `verify_blocked_reason: "metachar-denied"` and is **never** passed to `execute_shell_command` — verified by the injection-bypass fixtures (`pytest ; rm -rf src`, `pytest && curl x`, `pytest $(...)`, `pytest > /etc/x`).
- [ ] FR-4.3 PASS (C2) when exit codes are classified per the taxonomy: only `pytest` exit 1 (and the OQ-M9 per-tool Regression rows) on a tasklist-claimed-passing file sets `verification_regressions_detected ≥ 1` + `regression_present: true` (SKILL.md:557), forcing §5.3 rule-3 escalation and blocking §14.5.2 condition-4 promotion (SKILL.md:1097); exit 2/3/124 → Grounding Gap; exit 5 → Drift; `ruff`/`mypy` exit 1 → `S_dev_density` only.
- [ ] FR-4.3b PASS (M-CMP2) when a command that failed is retried once and the retry passes: it is classified `verify_flaky_suspected: true` → Grounding Gap, NOT `regression_present`.
- [ ] FR-4.4 PASS when `--no-verify` is set, OR the tool is context-excluded, OR the project is `read_only: true`: emit `verification_ran: false` + `verification_skip_reason: --no-verify | tool-unavailable | read-only-project`, degrade §10.4 Regression detection to "task log claims tests passed" with a Grounding Gap entry (SKILL.md:736-755), and **never block** the skill (`02-matrix:337`).
- [ ] FR-4.5 PASS when a command would mutate outside `<output>/` (matches the no-mutation denylist `git commit|push`, `pip install`, `rm`, repo-path redirects): it is rejected with `verify_blocked_reason: "mutation-denied"` and never invoked.
- [ ] FR-4.6 PASS when a command exceeds the timeout: `timeout` kills it, the invocation records `exit_code: 124` (timeout) + `verify_timeout_hit: true`, classified Grounding Gap, and the run continues (a hung verify never hangs the skill).
- [ ] FR-4.7 PASS when `read_only: true` is detected at Wave 0: emit the WARN "verification triangle disabled by Serena `read_only: true`; verdict will degrade to LSP-only signals" and proceed (`02-matrix:344`).
- [ ] FR-4.8 PASS (M-COR2) when a verification run writes build/test artifacts (`__pycache__`, `.pytest_cache`, `.coverage`, `*.pyc`): these are excluded from the Wave 5 `input_tree_sha256` recompute (SKILL.md:174,193) so a successful verify does NOT trip `input_drift_detected` and STOP the skill — verified by a fixture whose tests emit cache artifacts.

**Telemetry**: `verification_ran`, `verification_invocations`, `verification_skip_reason`, `verify_blocked`, `verify_blocked_reason`, `verify_timeout_hit`, `verify_flaky_suspected`, `verify_timeout_default`, `verify_invocations_path` (→ `<output>/verify-logs/invocations.yaml`); contract: `verification_ran`, `verification_invocations`, `verification_failures`, `verification_regressions_detected`, `regression_present`.

**Fail-open behavior** (§6.5, SKILL.md:397-399,1042): tool-unavailable / read-only / `--no-verify` → `verification_ran: false` + reason → fall back to `get_diagnostics_for_file` LSP signal only → degrade Regression class to task-log-claim + Grounding Gap → continue. No main-verdict abort.

**Dependencies**: low-spec **FR-RV3-LOW.7** (`get_current_config` for availability/`read_only` probe) — OQ-M5. Default timeout OQ-M2. Exit-code taxonomy OQ-M9. Input-hash artifact exclusion OQ-M10. Ships FIRST.

## 4. Architecture

### 4.1 New Files

> Files created by this work. Include purpose and dependencies.

| File | Purpose | Dependencies |
|------|---------|-------------|
| `<output>/artifacts/hierarchy-slice.yaml` | Runtime artifact: materialized `type_hierarchy` family slice (per-run) | FR-1 |
| `<output>/verify-logs/<cmd-hash>.stdout` / `.stderr` | Runtime artifacts: tail-truncated verification command output (per-invocation) | FR-4 |
| `<output>/verify-logs/invocations.yaml` | Runtime artifact: per-invocation array `[{cmd, exit_code, duration_ms, stdout_path, stderr_path, blocked_reason, deviation_class}]`, referenced by the audit row's `evidence_ref` (keeps the fixed 5-field audit-row schema intact — M-ARC1) | FR-4 |
| `.dev/eval-workspaces/sc-reflect/cases/serena-execute-verify/` | Eval case for FR-4 (verification triangle, allowlist, no-mutation, timeout, regression promotion) | FR-4 |
| `.dev/eval-workspaces/sc-reflect/cases/serena-verify-injection/` | Eval case for FR-4.2b / NFR-8 (C1 injection-bypass: metachar classes → zero invocations) | FR-4 |
| `.dev/eval-workspaces/sc-reflect/cases/serena-verify-exitcodes/` | Eval case for FR-4.3 (C2 exit-code → deviation-class taxonomy + flaky retry) | FR-4 |
| `.dev/eval-workspaces/sc-reflect/cases/serena-verify-drift-guard/` | Eval case for FR-4.8 (M-COR2 cache artifacts do not trip input-drift STOP) | FR-4 |
| `.dev/eval-workspaces/sc-reflect/cases/serena-onboarding/` | Eval case for FR-2 (cold-start bootstrap, silent-fail guard, context-excluded WARN, no-auto-trigger, NFR-7 budget) | FR-2 |
| `.dev/eval-workspaces/sc-reflect/cases/serena-handoff/` | Eval case for FR-3 (Tier-3 handoff blob, write_memory fallback, no-remediate no-op) | FR-3 |
| `.dev/eval-workspaces/sc-reflect/cases/serena-type-hierarchy/` | Eval case for FR-1 (backend probe, OO-coverage, LSP-disabled skip, 1B.3 lineage confirm) | FR-1 |

> Note: `<output>/...` paths are per-run artifacts, not source files. Only the `.dev/eval-workspaces/sc-reflect/cases/*` directories are committed source.

### 4.2 Modified Files

> Existing files changed. Include nature of change.

| File | Change | Rationale |
|------|--------|-----------|
| `src/superclaude/skills/sc-reflect-protocol/SKILL.md` | §6.1 chain: add step 4.5 (`type_hierarchy`) and step 5.5 (`execute_shell_command` + safety envelope). §4.0: add step 0.5c backend/availability probe (or consume low-spec FR-7) and step 0.7b (`onboarding`). §4.1 step 1B.3: add `type_hierarchy(subtypes)` lineage confirmation. §6.3 / Wave 6: add `prepare_for_new_conversation` handoff block. §10.4: replace opt-in `--rerun-tests` with default-on verification feeding `verification_regressions_detected`. §14: extend the `write_memory` fail row to cover handoff fallback. Frontmatter `allowed-tools`: add `type_hierarchy`, `onboarding`, `prepare_for_new_conversation`, `execute_shell_command`. | Core wiring for all 4 FRs at their §-anchored insertion points |
| `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` | Add `S_dev_density` sub-terms: hierarchy-gap count (FR-1), verification-failure weight (FR-4) | New rubric inputs from FR-1/FR-4 |
| `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` | Note `verification_regressions_detected` as the deterministic §10.4 Regression signal (FR-4) | New Regression-classifier input |
| `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` | Add hierarchy slice (FR-1) + verification results (FR-4) to the Wave 3 step 3B.0 per-reviewer brief grounding section (SKILL.md:245) | FR-1/FR-4 surface into reviewer briefs |
| `src/superclaude/skills/sc-reflect-protocol/refs/return-contract.yaml` *(if present — see OQ-M6)* | Add the new contract fields enumerated in §5; bump `contract_version` to `1.1.0` per §9.4 evolution policy | Minor contract bump for FR-1/3/4 |
| `src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md` | Add the FR-2/FR-4 operator WARN-message catalog entries (context-excluded, read-only-disabled, mutation-denied) | New operator-facing WARNs |

> Per CLAUDE.md SoT discipline: all edits land in `src/superclaude/` then `make sync-dev`. **No `.claude/` paths are touched directly.**

### 4.3 Removed Files [CONDITIONAL: refactoring, portification]

N/A — this is a `new_feature` spec; no files are removed. The `--rerun-tests` flag is **superseded, not removed**: it becomes a deprecated alias for default-on verification (FR-4 / OQ-M2), preserving backward compatibility.

### 4.4 Module Dependency Graph

```
   low-spec FR-RV3-LOW.7 get_current_config  (cross-spec substrate — backend/version/availability)
      │  (OQ-M5: consume if low-spec merged; else minimal inline probe)
      ├──────────────┬───────────────────────┬─────────────────────────┐
      ▼              ▼                         ▼                         ▼
  FR-4 execute_   FR-2 onboarding        FR-1 type_hierarchy      (read_only / context-excluded
  shell_command   (availability probe)   (backend probe)           degraded_components enrichment)
  (SHIP FIRST)    (SHIP SECOND)          (SHIP LAST)
      │
      ▼ verification_regressions_detected → regression_present (§9.1 :557)
      ▼ → §14.5.2 cond 4 promotion gate (:1097)

  FR-3 prepare_for_new_conversation ── independent; Wave 6 only; ship THIRD (signature OQ-M1)
```

### 4.5 Data Models [CONDITIONAL: new_feature, portification]

> New or modified data structures. These are the return-contract / audit-log additions (no Python dataclasses — sc:reflect is a skill protocol).

```yaml
# §9.1 RETURN-CONTRACT additions — versioned (contract_version 1.0.x → 1.1.0 per §9.4)
# §9.1 UC-1 block
hierarchy_slice_path: <abs-path> | null                  # FR-1
hierarchy_coverage_pct: <float 0.0-1.0> | null           # FR-1
# §9.1 UC-2 block / asymmetric-cost flags
verification_ran: <bool>                                  # FR-4
verification_invocations: <int>                           # FR-4 (count of verify_invocations[])
verification_failures: <int>                              # FR-4 (exit_code != 0 count)
verification_regressions_detected: <int>                  # FR-4 (non-zero on claimed-passing file)
verification_skip_reason: tool-unavailable|read-only-project|--no-verify|null   # FR-4
regression_present: <bool>                                # FR-4 — EXISTING field (SKILL.md:557), now verified-sourced
# §9.1 Tier 3 block
handoff_memory_key: <serena-memory-name> | null           # FR-3

# §9.2 TELEMETRY block — observability, NON-contractual (no contract bump per §9.4)
type_hierarchy_invoked: <bool>                            # FR-1
hierarchy_backend: jetbrains|lsp|none|lsp-disabled        # FR-1
hierarchy_nodes_examined: <int>                           # FR-1
hierarchy_gaps_found: <int>                               # FR-1
onboarding_ran: <bool>                                    # FR-2
onboarding_succeeded: <bool>                              # FR-2
onboarding_memories_count: <int>                          # FR-2
onboarding_skipped_reason: context-excluded|memories-present|null   # FR-2
handoff_memory_written: <bool>                            # FR-3
handoff_payload_size_bytes: <int>                         # FR-3
handoff_persist_method: prepare_for_new_conversation|write_memory_fallback   # FR-3
handoff_persist_failed: <bool>                            # FR-3
verify_timeout_hit: <bool>                                # FR-4
verify_flaky_suspected: <bool>                            # FR-4 (M-CMP2: retry flipped result)
verify_timeout_default: <int>                             # FR-4 (e.g. 120, forensic provenance)
verify_invocations_path: <abs-path>                       # FR-4 (M-ARC1: per-invocation array artifact)
```

**Minimal inline `get_current_config` probe contract (resolves M-ARC3).** Three of four FRs depend on the low-spec FR-RV3-LOW.7 substrate. When that substrate is not yet merged (OQ-M5), the Phase-1 PR MUST ship a minimal inline probe exposing exactly these fields, so FR-1/2/4 have a stable interface regardless of merge order:

```yaml
# minimal Wave-0 probe contract (inline fallback OR consumed from low-spec FR-7)
backend: jetbrains | lsp | none                 # gates FR-1 type_hierarchy
execute_shell_command_available: <bool>         # gates FR-4 (context-excluded detection)
onboarding_available: <bool>                    # gates FR-2 (context-excluded detection)
read_only: <bool>                               # FR-4.7 read_only:true → verification disabled
```

At low-spec merge, the inline probe is replaced by FR-7's richer snapshot; field names above are chosen to be a strict subset of FR-7's output so the swap is non-breaking.

### 4.6 Implementation Order

> Dependency-respecting order for implementation. Include parallelization opportunities.

> Note: this order is authoritative and §8 rollout phases map 1:1 to these steps. The matrix's explicit ordering recommendation (`02-matrix:350-374`) is the source: `execute_shell_command` FIRST (highest ROI, independent), then `onboarding`, then `prepare_for_new_conversation`, then `type_hierarchy` LAST (highest backend-dependency risk).

```
0. (Prereq) low-spec FR-RV3-LOW.7 get_current_config  -- if not yet merged, ship a minimal inline
                                                          backend/availability probe (OQ-M5)
1. FR-4 execute_shell_command + safety envelope   -- verification triangle; SHIP FIRST (standalone PR)
2. FR-2 onboarding                                -- [parallel with step 1]; Wave 0 conditional, --onboard
3. FR-3 prepare_for_new_conversation              -- Wave 6 only; signature probe (OQ-M1) first
4. FR-1 type_hierarchy                            -- depends on backend probe; SHIP LAST (--with-hierarchy)
```

## 5. Interface Contracts [CONDITIONAL: portification, new_feature]

> API contracts, gate criteria, prompt specifications, CLI surface changes.

**New `audit.log` fields** (per-step emit convention, SKILL.md:124): `type_hierarchy_invoked`, `hierarchy_backend`, `hierarchy_nodes_examined`, `hierarchy_gaps_found` (FR-1); `onboarding_ran`, `onboarding_succeeded`, `onboarding_memories_written`, `onboarding_skipped_reason` (FR-2); `handoff_memory_written`, `handoff_memory_key`, `handoff_payload_size_bytes`, `handoff_persist_method`, `handoff_persist_failed` (FR-3); `verify_invocations[]`, `verification_ran`, `verification_skip_reason`, `verify_blocked`, `verify_blocked_reason`, `verify_timeout_hit`, `verify_timeout_default` (FR-4).

**Contract-versioned fields vs telemetry**: the `contract_version` bump to `1.1.0` covers the **§9.1 return-contract** additions only — `hierarchy_slice_path` + `hierarchy_coverage_pct` (FR-1), `verification_ran`/`verification_invocations`/`verification_failures`/`verification_regressions_detected`/`verification_skip_reason` (FR-4), `handoff_memory_key` (FR-3). `regression_present` (FR-4) is an **existing** §9.1 field (SKILL.md:557) — its *source* changes (now verified) but no schema change. The **§9.2 telemetry** fields (all FR-1/FR-2/FR-3 `_invoked`/`_ran`/status fields and FR-4 `verify_timeout_*`) are observability, NOT contract — added without a bump per §9.4. The bump is a single minor (additive, backward-compatible) bump bundling FR-1/3/4.

**New rubric inputs** (`refs/reflection-rubric.md`): `S_dev_density` gains the hierarchy-gap term (FR-1) and the verification-failure weight (FR-4); the §10.4 Regression classifier gains the deterministic `verification_regressions_detected` signal (FR-4).

**Consumer impact (§9.3 Consumer Field Map, SKILL.md:620-636)**: `superclaude sprint run` (executor.py) and `sc-task-protocol` end-of-task hook MAY opt in to consume `verification_regressions_detected > 0` as a strong rollback signal; `regression_present` is already a load-bearing field for `sc-troubleshoot-protocol` Wave 6 (SKILL.md:626) — its semantics tighten (now verified-sourced) but the field contract is unchanged.

**Fail-open `degraded_components` tokens** introduced: `type_hierarchy:backend_error`, `execute_shell_command` (and skip reasons `tool-unavailable`/`read-only-project`/`--no-verify`), and the handoff-fallback marker is carried via `handoff_persist_method`/`handoff_persist_failed` rather than a `degraded` token.

### 5.1 CLI Surface [CONDITIONAL: new_feature, portification]

```
/sc:reflect --mode post [--no-verify] [--onboard] [--with-hierarchy] ...
# --no-verify       disable the verification triangle (FR-4); default = verification ON in UC-2
# --onboard         run one-shot Serena onboarding bootstrap when project memory is empty (FR-2)
# --with-hierarchy  enable type_hierarchy on hierarchy-capable backends (FR-1); default OFF on LSP
# (--rerun-tests   DEPRECATED alias → "verification on" = the default; see OQ-M2)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--no-verify` | flag | unset (verification ON in UC-2) | Disable `execute_shell_command` verification triangle (FR-4); sets `verification_skip_reason: --no-verify` |
| `--onboard` | flag | unset | Enable one-shot Serena onboarding bootstrap at Wave 0.7b when `list_memories` is empty (FR-2) |
| `--with-hierarchy` | flag | unset (OFF on LSP backends) | Enable `type_hierarchy` step 4.5 on a hierarchy-capable backend (FR-1) |
| `--rerun-tests` | flag (deprecated) | unset | Backward-compat alias; verification is now default-on. Emits a deprecation WARN (OQ-M2) |

### 5.2 Gate Criteria [CONDITIONAL: portification]

N/A — not a pipeline/portification spec; no inter-step gate tiers. (FR-4 does feed the existing §14.5.2 9-condition promotion gate, but that gate is defined in SKILL.md, not introduced here.)

### 5.3 Phase Contracts [CONDITIONAL: portification, infrastructure]

N/A — not a multi-phase pipeline; the wave structure already defines inter-wave contracts in SKILL.md §4.

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-RV3-MED.1 | **Fail-open**: every new Serena call inherits §6.5 fail-open semantics (SKILL.md:397-399) | 100% of new calls degrade-and-continue on tool-missing/error/excluded/read-only; skill never aborts on Serena unavailability | Eval case with Serena disabled AND with `read_only: true`: skill completes with `status: partial` + populated `degraded_components`/skip-reasons; zero hard aborts |
| NFR-RV3-MED.2 | **Telemetry**: every new tool emits a `<tool>_invoked`/`_ran` field; failure paths emit a `degraded`/skip-reason field | Every FR's telemetry fields present in `audit.log` on both success and degraded paths | Grader `yaml_field` assertion over `audit.log` + return contract for each FR's named fields |
| NFR-RV3-MED.3 | **Token budget**: per-feature delta within existing T1/T2 envelopes (T1 ~3-8k Claude / T2 ~35-70k per SKILL.md:1270-1271) | `type_hierarchy`/`onboarding`/handoff orchestration additions ≤ **+1,000 Claude-orchestration tokens** over the T1 path, measured vs a **named baseline** (current `master` HEAD on the FR-4 eval fixture). `execute_shell_command` Claude-side cost is near-zero (the test-suite *wall-clock* runs in the subprocess, not Claude tokens); `onboarding` is excluded from this cap as an explicit one-shot exception (`02-matrix:122` — "fills up the context window"), measured separately | Run the FR-4 eval fixture baseline vs branch; diff total Claude output tokens; assert delta ≤ 1,000 for FR-1/3/4; record `onboarding` cost separately |
| NFR-RV3-MED.4 | **Citation freshness**: any new `file:line` citation passes the CLAUDE.md S1 re-Read rule (§6.2, SKILL.md:369-371) | 100% of citations entering the draft report were re-Read within the last 5 tool calls | Eval assertion: every cited `file:line` in the report has a preceding re-Read; `type_hierarchy`/verification outputs that become citations are re-Read before quoting |
| NFR-RV3-MED.5 | **Verification safety**: `execute_shell_command` MUST NOT mutate state outside `<output>/` (`03-conversation-context.md` §3) | 0 commands invoked that fail the verb allowlist OR match the no-mutation denylist; 100% wrapped with `timeout`; 100% capped at 50 KB | Eval case asserts: denylisted/mutating commands are `verify_blocked`, never invoked; every invocation has a `timeout` prefix and a ≤51200-char captured output |
| NFR-RV3-MED.6 | **Verification liveness**: a hung or runaway verification command never hangs the skill | 100% of verify invocations terminate within `verify_timeout_default` (≤600s max); timeout → `exit_code: 124` + continue | Eval case with a deliberately-hanging command asserts `verify_timeout_hit: true`, `exit_code: 124`, and run completion |
| NFR-RV3-MED.7 | **Onboarding context budget** (resolves M-CMP1): `--onboard` MUST NOT starve the reflection waves despite its documented context-exhaustion hazard (`02-matrix:122`) | onboarding bounded by a hard turn/context budget (default = the §15 T1 band, hard-kill at 1.25× per SKILL.md:1274); on breach, abort onboarding and emit `onboarding_budget_exceeded: true` + degrade to `onboarding_succeeded: false` (not "bootstrapped"), never consuming the waves' budget | Eval case with an oversized fixture project asserts `onboarding_budget_exceeded: true` and that Waves 1-5 still run within their own budget |
| NFR-RV3-MED.8 | **Injection containment** (resolves CRITICAL C1): no shell-metacharacter command ever reaches `execute_shell_command` | 100% of metachar-bearing commands (`; & \| $ \` > < ( )`) are `verify_blocked: "metachar-denied"` before invocation; command strings are template-built, never prose-assembled | Injection-bypass fixture suite (FR-4.2b) asserts zero invocations for each metachar class |

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| `execute_shell_command` injection via `shell=True` command-chaining (allowlist bypass — CRITICAL C1) | Medium | **High** | **Structural metacharacter rejection** (FR-4 envelope (c) + NFR-8 + FR-4.2b): any `; \| & $ \` > < ( )` → `metachar-denied` before invocation; template construction (envelope (a)), never prose assembly; first-token allowlist is explicitly necessary-but-insufficient; injection-bypass fixture suite is the gating test |
| Exit-code conflation: non-zero ≠ Regression (CRITICAL C2) misclassifies lint/collection/no-tests as Regression, false-blocking promotion | Medium | **High** | Exit-code → deviation-class taxonomy (FR-4 + FR-4.3 + OQ-M9): only mapped Regression exits set `regression_present`; exit 2/3/124 → Grounding Gap, exit 5 → Drift, lint → `S_dev_density` |
| Verification side effects (`.pytest_cache`, `.pyc`) trip the `input_tree_sha256` drift guard → spurious STOP (M-COR2) | High | High | FR-4.8 + OQ-M10: exclude build/test artifacts from the input-hash recompute (SKILL.md:174,193); eval asserts a cache-emitting verify does not STOP |
| Flaky / non-deterministic verification → false Regression blocks promotion (M-CMP2) | Medium | Medium | FR-4.3b single-retry-on-failure → `verify_flaky_suspected` → Grounding Gap, not hard Regression |
| A verification command mutates the repo (e.g. a test with side effects, `pytest` writing fixtures) | Medium | High | No-mutation gate rejects writes outside `<output>/`; `cwd` scoped to affected subtree; FR-4.5 eval asserts mutation-denied; in-test side effects are best-effort only (OQ-M7) |
| Verification triangle silently OFF (`read_only: true` / context-excluded) → false confidence | Medium | High | FR-4.4/4.7 emit **loud** WARNs + `verification_skip_reason` + a Grounding Gap; never silent degrade (`02-matrix:266,337`) |
| Hung / long test suite blocks the run | Medium | Medium | NFR-6 `timeout <N>` wrap (default 120s, max 600s); `exit_code: 124` + continue |
| `prepare_for_new_conversation` signature wrong → invocation error | Medium | Low | FR-3 marks signature OQ-M1; runtime-probe before parameter-dependent wiring; `write_memory` fallback covers the failure |
| `onboarding` consumes large context (starves waves) and surprises operator with `.serena/` creation | Medium | Medium | FR-2 opt-in only (`--onboard`), gated on empty memory, never auto-trigger; **NFR-7 hard context budget** with `onboarding_budget_exceeded` abort (resolves M-CMP1) |
| Handoff memory namespace `reflect/handoff-*` accumulates unbounded (escapes low-spec retention sweep — M-ARC2) | Medium | Medium | FR-3.7: extend the FR-RV3-LOW.8 sweep prefix set to cover `reflect/handoff-*` under the shared 90-day/20-entry policy |
| `type_hierarchy` empty result misread as "no subtypes" on an unsupported LSP | Medium | Medium | FR-1.4/1.5 distinguish backend-unsupported (skip, no degrade) from explicit error (degrade + fallback); `--with-hierarchy` default-off on LSP until OQ-M3 |
| Cross-spec dependency on low-spec FR-7 not yet merged | Medium | Medium | OQ-M5: ship a minimal inline `get_current_config` probe in the FR-4 PR; reconcile at low-spec merge |
| `--rerun-tests` / `--no-verify` flag-semantics collision confuses operators | Low | Medium | FR-4 / OQ-M2: `--rerun-tests` becomes a deprecated alias with a WARN; single source of truth is "verification default-on" |
| Two consecutive contract minor bumps (low-spec 1.1.0 + this 1.1.0) collide | Medium | Low | OQ-M6: coordinate the version bump with the low-spec; if low-spec lands 1.1.0 first, this spec bumps to 1.2.0 |

## 8. Test Plan

### 8.1 Unit Tests

> sc:reflect is a skill protocol; "unit" granularity = eval-workspace cases at `.dev/eval-workspaces/sc-reflect/cases/`, one per feature minimum (enumerated, not authored here — authoring is downstream).

| Test | File | Validates |
|------|------|-----------|
| `serena-execute-verify` case | `.dev/eval-workspaces/sc-reflect/cases/serena-execute-verify/` | FR-4: verification triangle; allowlist block; no-mutation deny; timeout→124; `pytest` exit-1 → `regression_present` → promotion-gate block; `--no-verify` + read-only skip with WARN |
| `serena-verify-injection` case (M-TST1) | `.dev/eval-workspaces/sc-reflect/cases/serena-verify-injection/` | **FR-4.2b / NFR-8 (the gating safety test)**: each injection class (`pytest ; rm`, `pytest && curl`, `pytest \| sh`, `pytest $(x)`, `pytest \`x\``, `pytest > /etc/y`) → `metachar-denied`, **zero invocations** |
| `serena-verify-exitcodes` case (C2) | `.dev/eval-workspaces/sc-reflect/cases/serena-verify-exitcodes/` | FR-4.3: exit-code taxonomy — `pytest` 1→Regression, 2/3→Grounding Gap, 5→Drift, `ruff` 1→`S_dev_density`, 124→Grounding Gap; FR-4.3b flaky-retry→`verify_flaky_suspected` |
| `serena-verify-drift-guard` case (M-COR2) | `.dev/eval-workspaces/sc-reflect/cases/serena-verify-drift-guard/` | FR-4.8: a verify run emitting `.pytest_cache`/`.pyc` does NOT trip `input_tree_sha256` drift → no spurious STOP |
| `serena-onboarding` case | `.dev/eval-workspaces/sc-reflect/cases/serena-onboarding/` | FR-2: cold-start bootstrap; silent-fail guard (memory delta ≤0 → succeeded:false); context-excluded WARN (not STOP); warm-start skip; no-auto-trigger without `--onboard` |
| `serena-handoff` case | `.dev/eval-workspaces/sc-reflect/cases/serena-handoff/` | FR-3: handoff blob written before task-builder; `write_memory` fallback when context-excluded; both-fail → `handoff_persist_failed` + report ships; no-remediate no-op |
| `serena-type-hierarchy` case | `.dev/eval-workspaces/sc-reflect/cases/serena-type-hierarchy/` | FR-1: backend probe; OO subtype coverage; LSP-disabled skip (no degrade); explicit backend error → fallback; 1B.3 lineage confirmation |

### 8.2 Integration Tests

| Test | Validates |
|------|-----------|
| Serena-disabled + read-only full run | NFR-1/NFR-5: all 4 adoptions degrade-and-continue; `verification_ran:false` with reason; `status: partial`; zero hard aborts; no mutation outside `<output>/` |
| Verification-triangle regression promotion-block | FR-4 + §14.5.2: a tasklist-claimed-passing file with a failing test sets `regression_present:true`, escalates per §5.3 rule 3, and blocks Wave 7 promotion (cond 4) |
| Telemetry-completeness sweep | NFR-2: grader `yaml_field` over `audit.log` + contract confirms every FR's `_invoked`/`_ran` + degraded/skip field on both paths |
| Contract-version bump regression | §5: `contract_version: 1.1.0` (or 1.2.0 per OQ-M6) present; legacy fields preserved per §9.4 backward-compat |
| Token-budget delta measurement | NFR-3: FR-1/3/4 aggregate orchestration-token delta ≤ 1,000 vs named baseline; `onboarding` recorded separately |
| Citation-freshness audit | NFR-4: every cited `file:line` (incl. hierarchy/verify outputs) re-Read within 5 tool calls (CLAUDE.md S1) |
| Verification-liveness | NFR-6: deliberately-hanging command → `verify_timeout_hit:true`, `exit_code:124`, run completes |

### 8.3 Manual / E2E Tests [CONDITIONAL: infrastructure, portification]

N/A — eval-workspace cases (8.1) and the Serena-disabled/read-only integration run (8.2) provide E2E coverage; no separate manual scenarios required for a `new_feature` protocol extension.

## 9. Migration & Rollout [CONDITIONAL: refactoring, portification]

> How to transition from current state to new state. Breaking changes, backwards compatibility.

**Rollout grouping** (one PR per feature, per the matrix "Cross-feature observations", `02-matrix:348-374`):

> Phases map 1:1 to §4.6 implementation order. The matrix is explicit: "Ship `execute_shell_command` first as the highest-ROI standalone PR closing the verification-triangle gap, then `onboarding` and `prepare_for_new_conversation` in separate PRs sharing a co-designed memory-naming convention, and reserve `type_hierarchy` for a v1.1 enhancement gated on a backend-probe." (`02-matrix:374`)

- **Phase 0 — Cross-spec substrate.** Ensure low-spec FR-RV3-LOW.7 `get_current_config` is available, OR ship a minimal inline probe in the Phase 1 PR (OQ-M5).
- **Phase 1 (single PR) — FR-4 `execute_shell_command`** + safety envelope + verification triangle. Highest ROI; closes the largest false-PASS path. Subsumes `--rerun-tests`. "Ship this as a standalone PR; do not bundle." (`02-matrix:352`)
- **Phase 2 (single PR) — FR-2 `onboarding`** (Wave 0 conditional, `--onboard`). Independent, one-shot per project. (`02-matrix:354`)
- **Phase 3 (single PR) — FR-3 `prepare_for_new_conversation`** (Wave 6, signature-probed). Shares a co-designed `reflect/<category>-<slug>[-<timestamp>]` memory-naming convention with the §6.3 keys. (`02-matrix:356,364`)
- **Phase 4 (v1.1 PR) — FR-1 `type_hierarchy`** (backend-probe gated, `--with-hierarchy`). Ship after the first three are stable. (`02-matrix:358,365`)

> **Co-design note** (`02-matrix:363-364`): Phases 2 and 3 share the Serena memory namespace but have disjoint lifecycle/consumer surfaces — keep them in SEPARATE PRs, but decide the `reflect/<category>-<slug>[-<timestamp>]` naming + TTL/retention (90-day expire, 20-entry cap) ONCE across both (and the low-spec §6.3 keys).

- **Breaking changes**: None to the contract. **Behavioral change**: UC-2 now runs verification by default (previously opt-in via `--rerun-tests`); operators relying on no-test-execution must pass `--no-verify`. This is called out in the deprecation WARN.
- **Backwards compatibility**: `contract_version` 1.0.x consumers tolerate the 1.1.0 minor bump (additive fields only) per §9.4; `regression_present` semantics tighten but the field is unchanged; `--rerun-tests` keeps working as a default-on alias.
- **Rollback plan**: Each phase is an independent PR touching only `SKILL.md` + `refs/*` + eval cases. Revert the PR; `make sync-dev` restores the prior `.claude/` mirror. No data migration, no state mutation outside `<output>/` (the verification subprocess writes only to `<output>/verify-logs/`).

## 10. Downstream Inputs

> What this spec feeds into. How downstream consumers (sc:roadmap, sc:tasklist, etc.) use the output.

### For sc:roadmap

Four themes map to milestones: **(M1) Verification triangle** (FR-4) — the critical-path false-PASS closure, ships first; **(M2) Cold-start bootstrap** (FR-2) — independent calibration baseline; **(M3) Tier-3 handoff bridge** (FR-3) — remediation-chain token saving; **(M4) Polymorphic family coverage** (FR-1) — the v1.1 OO-codebase enhancement. Critical path: M1 (standalone) → {M2, M3 parallel} → M4. M1 depends on the cross-spec `get_current_config` substrate (low-spec M1).

### For sc:tasklist

Task breakdown follows §4.6 implementation order. Each FR is a self-contained MDTM task; **FR-4 is the largest task** (safety envelope is the bulk of the work) and MUST be built first. Every task MUST include a Wave-0 availability probe as its first step (backend/context/`read_only` detection). The §11 Open Items are the runtime-probe / decision research items task-builder MUST create as preconditions: **OQ-M1** (handoff signature), **OQ-M2** (default timeout + flag migration), **OQ-M3** (LSP type_hierarchy coverage), **OQ-M5** (cross-spec FR-7 availability), **OQ-M6** (contract-version coordination), **OQ-M8** (`return-contract.yaml` existence), and **OQ-M10** (input-hash artifact-exclude set) are task-build-time probes/decisions; **OQ-M4** (UC-1 verification scope), **OQ-M7** (side-effecting-test policy), and **OQ-M9** (full exit-code table) are resolved during eval-authoring.

## 11. Open Items

> Unresolved questions. Each should have an owner and deadline. Empty section means all questions resolved.

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| OQ-M1 | What is the exact `prepare_for_new_conversation` signature / parameter shape? (`02-matrix:181-184,194,369` — "the largest research gap"; no source surfaces it) | Blocks FR-3 parameter-dependent wiring; affects handoff-blob construction | Runtime probe against live Serena MCP (`--list-tools` or equivalent) before Phase 3 merge |
| OQ-M2 | What is the `execute_shell_command` default timeout, and how does `--rerun-tests` migrate to `--no-verify`? (`02-matrix:257,269` — global-config timeout exists but default not surfaced) | Affects FR-4 timeout-wrap default + flag-deprecation messaging | Consumer-side `timeout <N>` wrap (default 120s) regardless of Serena's; decide `--rerun-tests` deprecation copy at Phase 1 |
| OQ-M3 | Which LSP backends actually support `type_hierarchy`? (`02-matrix:64-66,372` — news entry says "JetBrains only", README capability table says LSP "yes"; contradictory) | Determines whether `--with-hierarchy` may default-on for any LSP language | Empirical probe: run `type_hierarchy` against Python/Java/TypeScript test projects, record per-language success; keep default-off on LSP until confirmed |
| OQ-M4 | Should the verification triangle (FR-4) extend to UC-1, or remain UC-2-only? (matrix recommends UC-2 default-on; UC-1 value less clear) | Determines FR-4 mode-gating scope | Decide during FR-4 eval-authoring; default UC-2-only for v1 |
| OQ-M5 | Is low-spec FR-RV3-LOW.7 `get_current_config` merged before this medium PR, or must FR-4/FR-1/FR-2 ship a minimal inline backend/availability probe? | Determines whether the Wave 0 probe is shared or duplicated | Check low-spec merge status at Phase 1 task-build; if unmerged, inline a minimal probe and reconcile at low-spec merge |
| OQ-M6 | Does this spec's `contract_version` bump collide with the low-spec's 1.1.0 bump? | Two specs both targeting 1.1.0 would conflict | Coordinate at task-build: if low-spec lands 1.1.0, this spec bumps to 1.2.0; both are additive minors |
| OQ-M7 | What is the policy for verification commands whose tests have side effects (write fixtures, hit network, mutate a DB)? | Affects FR-4 no-mutation gate scope — the gate catches writes outside `<output>/` but cannot catch in-test side effects | Document as operator responsibility in the FR-4 eval case; the no-mutation gate is best-effort on the *command*, not the *test internals* |
| OQ-M8 | Does `refs/return-contract.yaml` exist as a separate file, or is the contract inline in SKILL.md §9? | Determines whether §5 contract additions edit a YAML file or a SKILL.md section | Read `src/superclaude/skills/sc-reflect-protocol/refs/` at task-build time (mechanical check; shared with low-spec OQ-5) |
| OQ-M9 | What is the full per-tool exit-code → deviation-class table beyond the FR-4 defaults? (e.g. `mypy` exit 2, `make` non-zero, `cargo test` codes, `npm` codes) | Completeness of the C2 taxonomy; an unmapped exit defaults to Grounding Gap (never silently to Regression) | Enumerate during FR-4 eval-authoring; unmapped exit codes default to Grounding Gap (conservative — never a false Regression) |
| OQ-M10 | Exactly which build/test artifacts must be excluded from the `input_tree_sha256` recompute so verification side effects do not trip the drift guard? (`__pycache__`, `.pytest_cache`, `.coverage`, `*.pyc`, `node_modules/.cache`, `.mypy_cache`, target/) | FR-4.8 correctness; an incomplete exclude list re-introduces the M-COR2 spurious-STOP | Define the exclude glob set at Phase 1; verify against the SKILL.md:174 input-tree construction (mechanical) |

## 12. Brainstorm Gap Analysis

> Auto-populated by `sc:cli-portify` Phase 3c embedded brainstorm pass. For manually created specs, use `/sc:brainstorm` to identify gaps.

| Gap ID | Description | Severity | Affected Section | Persona |
|--------|-------------|----------|-----------------|---------|
| G-1 | `execute_shell_command` is the dominant hazard surface (`shell=True`, no upstream sandbox); the entire safety envelope is consumer-side. **Resolved**: spec-panel C1 (allowlist-bypass) closed by structural metachar rejection (FR-4 envelope (c), FR-4.2b, NFR-8) + injection-bypass gating eval | High → Mitigated | §3 FR-4, §6 NFR-5/6/8, §7, §8.1 | compliance |
| G-2 | Verification triangle silently OFF (`read_only`/context-excluded) produces false confidence. **Mitigated**: FR-4.4/4.7 loud WARNs + `verification_skip_reason` + Grounding Gap (never silent) | High → Mitigated | §3 FR-4.4/4.7, §7 | correctness |
| G-7 | spec-panel C2 (exit-code conflation): non-zero ≠ Regression. **Resolved**: exit-code → deviation-class taxonomy (FR-4, FR-4.3, OQ-M9) splits failures into Regression / Grounding Gap / Drift / lint-signal | High → Mitigated | §3 FR-4, §11 OQ-M9 | correctness |
| G-8 | spec-panel M-COR2: verify side effects trip the input-drift guard. **Resolved**: FR-4.8 + OQ-M10 exclude build/test artifacts from the input-hash recompute | High → Mitigated | §3 FR-4.8, §11 OQ-M10 | correctness |
| G-3 | Cross-spec dependency on low-spec FR-7 `get_current_config` is load-bearing for 3 of 4 FRs; if the low-spec slips, this spec must carry a minimal probe | Medium | §3 deps, §4.4, §11 OQ-M5 | architect |
| G-4 | `prepare_for_new_conversation` signature is unverified — the largest single research gap; all parameter-dependent FR-3 wiring is provisional until probed | Medium | §3 FR-3, §11 OQ-M1 | architect |
| G-5 | `--rerun-tests` → `--no-verify` flag migration changes default behavior (tests now run by default); risk of operator surprise without clear deprecation messaging | Medium | §3 FR-4, §9, §11 OQ-M2 | testing |
| G-6 | `type_hierarchy` LSP-vs-JetBrains coverage is empirically unresolved; shipping `--with-hierarchy` default-on on LSP risks empty-result misreads | Medium | §3 FR-1, §11 OQ-M3 | testing |

This spec adopts 4 medium-complexity Serena features into sc:reflect at their precise wave-insertion points. The dominant residual risk is **the operational-hazard surface of `execute_shell_command`** — mitigated structurally by an eight-part consumer-side safety envelope (template construction, verb allowlist, **structural metacharacter rejection**, timeout wrap, output cap, `cwd` scoping, per-call audit artifact, `--no-verify`) plus an exit-code → deviation-class taxonomy, and by loud-never-silent degradation when verification is unavailable. The spec-panel pass resolved both CRITICAL findings (C1 allowlist-bypass, C2 exit-code conflation) in-place and all seven MAJOR findings (M-COR1/2, M-ARC1/2/3, M-CMP1/2) either in-place or via §11 open items with explicit rationale. The remaining residual risk is **runtime divergence** between matrix-documented signatures and the live Serena surface — concentrated in OQ-M1 (handoff signature) and OQ-M3 (LSP hierarchy coverage), mitigated by the §6.5 fail-open envelope. No requirement blocks ship on its own; the critical path is FR-4 (standalone) → {FR-2, FR-3} → FR-1.

---

## Appendix A: Glossary [CONDITIONAL: all types -- include if domain-specific terminology used]

| Term | Definition |
|------|-----------|
| UC-1 / UC-2 | sc:reflect's two use cases: UC-1 pre-execution coverage/gap audit of a strategy vs. its spec; UC-2 post-execution deviation audit of completed work |
| 4-category deviation taxonomy | Authorized expansion / Necessary deviation / Drift / Regression — the classes UC-2 sorts every divergence into (`03-conversation-context.md` §4) |
| §6.1 chain | The mandatory Wave 1A symbol-anchored evidence-gathering chain that replaces `think_about_collected_information` as the load-bearing grounding mechanism (SKILL.md:354-367) |
| Verification triangle | `get_diagnostics_for_file` (LSP issues) + `summarize_changes` (what changed) + `execute_shell_command` (does it pass) — the three-signal correctness check FR-4 completes (`02-matrix:340`) |
| Safety envelope | The six consumer-side controls wrapping `execute_shell_command`: verb allowlist, `timeout` wrap, 50 KB output cap, no-mutation gate, per-call audit, `--no-verify` (FR-4, `02-matrix:24`) |
| Fail-open (§6.5) | Every Serena call degrades-and-continues on failure: missing/excluded/error → `degraded:[tool]`/skip-reason → fallback signal → never aborts (SKILL.md:397-399) |
| `S_dev_density` | Rubric structural signal: ratio of unmapped diff hunks (UC-2) or unmapped spec requirements (UC-1) to total; FR-1 and FR-4 feed sub-terms into it (SKILL.md:287) |
| `read_only: true` | Serena project-config flag that disables ALL editing tools including `execute_shell_command`; broader than sc:reflect's own read-only-against-source posture (`02-matrix:267`) |
| Handoff memory | FR-3's `reflect/handoff-{slug}-{timestamp}` blob bridging Waves 1-5 context into the Wave 6 task-builder remediation conversation |

## Appendix B: Reference Documents [CONDITIONAL: all types -- include if external references needed]

| Document | Relevance |
|----------|-----------|
| `.dev/releases/current/Reflect-V3.5-Serena_Mediums/02-matrix-medium-complexity.md` | The 4-row feature-adoption matrix + per-row research deep-dives this spec is derived from |
| `.dev/releases/current/Reflect-V3.5-Serena_Mediums/03-conversation-context.md` | Framing, read-only posture clarification (§3 — the `execute_shell_command` qualifier), deviation taxonomy (§4), exclusions (§5) |
| `.dev/releases/current/Reflect-V3-Serena/04-spec-low-complexity.md` | Sibling low-complexity spec; source of cross-spec dependency FR-RV3-LOW.7 (`get_current_config`) |
| `src/superclaude/skills/sc-reflect-protocol/SKILL.md` | Target integration surface; §4 wave structure, §6.1 chain, §6.5 fail-open, §10.4 Regression, §14.5.2 promotion gate |
| `src/superclaude/skills/sc-reflect-protocol/refs/` | `reflection-rubric.md`, `deviation-taxonomy.md`, `reviewer-spec.md`, `ops-integration.md`, `return-contract.yaml` (OQ-M8) — the ref slices that gain content |
| [Serena Security Audit Discussion #380](https://github.com/oraios/serena/discussions/380) | `execute_shell_command` `shell=True`, no whitelist/sandbox — the hazard basis for the FR-4 safety envelope |
| [Serena Tools reference](https://oraios.github.io/serena/01-about/035_tools.html) | `execute_shell_command`, `onboarding`, `prepare_for_new_conversation`, `type_hierarchy` tool semantics |
| [Serena Memories & Onboarding](https://oraios.github.io/serena/02-usage/045_memories.html) | Onboarding gating (skip when memories exist), context-window caution, `memory_maintenance` precedence (FR-2) |
