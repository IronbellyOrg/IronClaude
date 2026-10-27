---
title: "sc:reflect V3 — Serena Low-Complexity Adoption (Wave 1A + memory CRUD + version fingerprint)"
version: "1.0.0"
status: draft
feature_id: FR-RV3-LOW
parent_feature: null
spec_type: new_feature
complexity_score: 0.3
complexity_class: LOW
target_release: sc-reflect-v3
authors: [user, claude]
created: 2026-06-01
quality_scores:
  clarity: 8.5
  completeness: 8.0
  testability: 8.5
  consistency: 8.0
  overall: 8.2
---

## 1. Problem Statement

> What problem does this work solve? Why does it matter? What fails or is suboptimal today?

sc:reflect's grounding and operational-hygiene mechanisms lag behind the Serena MCP tool surface they were designed against. The skill's architectural bet (SKILL.md §1414, summarised in `03-conversation-context.md` §2) is that **Serena's symbolic chain is the load-bearing grounding mechanism** for deviation detection (UC-2) and coverage analysis (UC-1), with `think_about_*` demoted to non-load-bearing nudges and every Serena call fail-open. That bet is only as strong as the symbolic chain wired into Wave 1A (§6.1), the Wave 0 calibration probes, and the §6.3 memory lifecycle.

Three concrete gaps exist today against the current Serena release line (v1.3.0 symbol tools, v1.5.0 memory + onboarding changes):

1. **The Wave 1A chain (§6.1) cannot enumerate polymorphic or external surfaces.** It stops at `find_symbol → find_referencing_symbols`. It has no step for `find_implementations` (interface/abstract coverage — a recurring **Drift** failure mode: "interface added but no implementor wired") and no `find_declaration` entry point for the diff-hunk inputs that are UC-2's natural shape, forcing textual-guess `find_symbol` calls that produce false-positive overlap edges in the Wave 1B.3 cross-task scan.
2. **Wave 0 has a calibration blind spot.** sc:reflect probes alias env vars but never reads Serena's own active context/modes/tool-list, so `degraded_components` detection is incomplete and `S_dev_density` calibration cannot account for context-excluded tools or whether project onboarding ran.
3. **The §6.3 retention rule is specified but not implemented.** "Keep last 20 entries per key; expire >90 days" is aspirational — `write_memory` accumulates without pruning, an operational hazard at the 6-month horizon. The closing tools (`delete_memory`, `rename_memory`, `edit_memory`) exist but are unwired.

Two matrix rows additionally encode **upstream-drift hazards** that must be corrected rather than naively adopted: `check_onboarding_performed` was **deleted in Serena v1.5.0**, and `find_referencing_code_snippets` appears **absorbed into `find_referencing_symbols` extended-info**. Adopting either as written would emit MCP tool-not-found errors or wire a non-existent tool.

### 1.1 Evidence

> Concrete evidence that the problem exists. Links to issues, failing tests, user reports, forensic findings.

| Evidence | Source | Impact |
|----------|--------|--------|
| §6.1 chain ends at `find_referencing_symbols`; no `find_implementations`/`find_declaration` steps | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:354-367` | Polymorphic + external surfaces ungrounded; Drift class under-detected |
| §6.3 retention rule "keep last 20 / expire >90d" with only `write_memory` wired | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:373-383` | Unbounded memory growth; specified-but-unimplemented loop |
| Wave 0 (§4.0) probes env aliases (step 0.5) but not Serena's active context/modes | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:197-225` | `degraded_components` incomplete; context-excluded tools invisible |
| `check_onboarding_performed` removed in Serena v1.5.0 (2026-05-18) | `01-matrix-low-complexity.md:336,361` (CHANGELOG cite) | Matrix row 6 invalidated as written; must collapse into `activate_project` parse |
| `find_referencing_code_snippets` absent from current Tools page + active-tools log; absorbed into extended-info | `01-matrix-low-complexity.md:169-181,558` | Matrix row 3 reduces to `include_info: true`; needs runtime probe before wiring |

### 1.2 Scope Boundary

> What this spec addresses and explicitly does NOT address.

**In scope**: The 8 low-complexity / medium-to-high-value Serena adoptions enumerated in `01-matrix-low-complexity.md` — `find_implementations`, `find_declaration`, `find_referencing_code_snippets` (corrected to extended-info), `find_symbol(search_deps=True)`, `summarize_changes`, `check_onboarding_performed` (corrected to activate-project parse), `get_current_config`, and the memory-lifecycle CRUD trio (`delete_memory`/`rename_memory`/`edit_memory`). All wiring is additive to `SKILL.md` + `refs/*.md`; all calls inherit §6.5 fail-open semantics; all emit telemetry fields.

**Out of scope**:
- **Medium-complexity adoptions** (`execute_shell_command` allowlist, onboarding, Tier-3 handoff, `type_hierarchy`) — these belong to the separate `Reflect-V3.5-Serena_Mediums` release and a separate spec.
- **Symbolic editing / project-mutating tools** (`insert_before_symbol`, `replace_symbol_body`, `rename_symbol`, `safe_delete_symbol`, `replace_content`) — out of bounds under the §3 read-only-with-respect-to-source posture; route to Tier 3 task-builder per `03-conversation-context.md` §5.
- **Filesystem-native Serena ops** (`list_dir`, `find_file`, `read_file`) — excluded per `03-conversation-context.md` §5 (freshness-gap vs. CLAUDE.md S1, no offsetting benefit).
- **HTTP/SSE transport, custom Contexts/Modes, `switch_modes`, `initial_instructions`, dashboard surface** — excluded per `03-conversation-context.md` §5.
- **Source-code remediation** of any deviation sc:reflect detects — that is the Tier 3 / task-builder surface, never sc:reflect itself.
- **Task-file authoring** — downstream `/task-builder` responsibility, not this spec.

## 2. Solution Overview

> High-level description of the approach. What changes, what stays the same.

Extend sc:reflect's Serena footprint with eight additive, fail-open adoptions, wired at the precise wave-insertion points the matrix research identifies, behind a single `get_current_config` version-fingerprint substrate that gates the version-sensitive rows. The Wave 1A symbolic chain (§6.1) gains polymorphic enumeration (`find_implementations`) and a diff-hunk entry point (`find_declaration`); the existing `find_referencing_symbols` step gains `include_info: true` (the corrected form of the "absorbed" row 3); an optional external-dependency fan-out (`find_symbol(search_deps=True)`) and a UC-2 corroboration signal (`summarize_changes`) are added. Wave 0 gains a `get_current_config` snapshot and an onboarding-status parse (the corrected form of the deleted row 6). The §6.3 memory loop gains a retention sweep using the CRUD trio, gated on a v1.5 Serena fingerprint.

What stays the same: the wave/tier architecture (§4), the rubric (§5), the evidence-validator gate (Wave 5), the read-only-with-respect-to-source posture, and the per-step audit emit convention (§4 — every step emits one `audit.log` row). No new wave is introduced; every adoption plugs into an existing step.

### 2.1 Key Design Decisions

> Decisions made during brainstorming/design that shaped this spec. Each decision should have a rationale.

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| `find_implementations` (matrix row 1) | **adopt** | skip / defer | High value: directly strengthens UC-1 coverage ("are all implementations of `Handler` accounted for?") and catches the "interface added, implementor missing" **Drift** case. ~10 lines in §6.1 + one reflection-card field. (`01-matrix:15,40-97`) |
| `find_declaration` (matrix row 2) | **adopt** | skip / defer | Medium value: canonical diff-hunk → symbol entry point for UC-2; eliminates false-positive overlap edges from name collisions in Wave 1B.3. Ships with row 1 (shared v1.3.0 + shared card schema). (`01-matrix:16,101-161`) |
| `find_referencing_code_snippets` (matrix row 3) | **adopt — corrected to `find_referencing_symbols(include_info=True)`** | adopt-as-named / skip | Primary sources indicate the standalone tool was **absorbed into extended-info** in v1.0+. The "denser packaging / lower token cost" value transfers to adding `include_info: true` to the existing §6.1 step 4. Requires a Wave 0 runtime probe to confirm before merging. (`01-matrix:165-216,558`) |
| `find_symbol(search_deps=True)` (matrix row 4) | **adopt** | skip / defer | Medium value: grounds spec-cited third-party APIs ("matches FastAPI's `Depends` contract"), converting `[INFERRED]` **Necessary-deviation** findings into grounded ones. One-flag fan-out gated on "third-party API referenced". Depends on row 2. (`01-matrix:18,220-280`) |
| `summarize_changes` (matrix row 5) | **adopt — deferred to last / pilot first** | skip / adopt-early | Medium-but-marginal: prompt-based (returns instructions, not a computed diff), so corroboration is weaker than implied and session-bound. Ship last; pilot in eval workspace before promoting. (`01-matrix:19,284-329,559`) |
| `check_onboarding_performed` (matrix row 6) | **adopt — corrected to `activate_project` message parse + `list_memories` proxy** | adopt-as-named / skip | **DELETED in Serena v1.5.0.** Adopting as named emits tool-not-found on Serena ≥1.5. The grounding-confidence signal survives via the v1.5 activation-message body + `memory_maintenance` seed-presence proxy. No new tool call. (`01-matrix:20,336-382`) |
| `get_current_config` (matrix row 7) | **adopt — ship FIRST** | skip / defer | Medium value + structural prerequisite: the version-fingerprint substrate that gates rows 6 and 8, and the source of `degraded_components: ["serena:context-excluded"]`. Closes the Wave 0 active-context blind spot. (`01-matrix:21,386-432`) |
| `delete_memory` / `rename_memory` / `edit_memory` (matrix row 8) | **adopt — as one CRUD trio, v1.5-gated** | skip / wrap in task-builder | Medium value: closes the specified-but-unimplemented §6.3 retention loop; prevents unbounded `write_memory` growth. `rename_memory` `mem:`-reference propagation requires Serena ≥1.5 (gated on row 7's fingerprint). All three share state — one MDTM task, not three. (`01-matrix:22,436-525`) |

### 2.2 Workflow / Data Flow

> How the system works end-to-end after this change. Use ASCII diagrams for pipeline flows.

```
sc:reflect wave structure — Serena Low-Complexity adoption insertion map
(SKILL.md section anchors quoted; arrows show where each matrix row plugs in)

 WAVE 0  Parse + Validate + Activate Project + Memory Hydrate        [SKILL.md §4.0 :172-225]
 ├─ 0.5  env-var alias resolution                                    [SKILL.md :197]
 ├─ 0.5c get_current_config  ◀── ROW 7  (NEW step)                    [§4.0 insertion]
 │        → serena-config-snapshot.yaml; serena_context/modes/tool_count/excluded_tools
 │        → version fingerprint substrate  ──┐ gates ROW 6 + ROW 8
 ├─ 0.7  activate_project + memory hydrate                           [SKILL.md :134]
 │        ◀── ROW 6  parse activation message for onboarding marker  (NO new tool)
 │        ◀── ROW 6  list_memories seed-presence proxy (memory_maintenance)
 │        → onboarding_status: bootstrapped|not_bootstrapped|unknown
 └─ 0.8  open audit log

 WAVE 1  Tier 1 — Grounded Single-Agent Reflection
 ├─ 1A   §6.1 Mandatory evidence-gathering chain                     [SKILL.md §6.1 :354-367]
 │        1. activate_project (idempotent)
 │        2. get_symbols_overview <file>
 │        2a. find_declaration  ◀── ROW 2  (NEW; when input is a diff-hunk, not a name)
 │        3. find_symbol <symbol>
 │        3b. find_implementations  ◀── ROW 1  (NEW; when kind ∈ {Interface,Abstract,Protocol,Trait})
 │        4. find_referencing_symbols <symbol> + include_info:true  ◀── ROW 3 (corrected)
 │        5. get_diagnostics_for_file <file>
 │        6. re-Read cited file:line  [SKILL.md §6.2 :369-371 ; CLAUDE.md S1]
 │        7. find_symbol(search_deps=True)  ◀── ROW 4  (NEW; when spec/tasklist cites 3rd-party API)
 │        7'(UC-2). summarize_changes  ◀── ROW 5  (NEW; corroboration vs supplied diff)
 ├─ 1B.3 cross-task interaction-effects scan (UC-2, ≥3 tasks)        [SKILL.md §4.1 :233-241]
 │        ◀── ROW 2  find_declaration pre-step on diff-hunks lacking symbol context
 │        ◀── ROW 1  implementor-overlap edge = HIGH-severity interaction risk
 ├─ 1C   single-agent reflection
 └─ 1D   blind calibration (confidence-calibrator)

 WAVE 2  Tier-Decision Gate (rubric §5)   ── S_dev_density consumes ROW 1/2/4/6/7 signals
 WAVE 3  Tier 2 reviewers  ── ROW 1 implementations list lands in per-reviewer brief [§4.3 :245]
 WAVE 4  Adversarial merge
 WAVE 5  Synthesis + Evidence-Validator Gate + Report               [SKILL.md §4.5 :249-257]
 └─ §6.3 memory persist  ◀── ROW 8  retention sweep                  [SKILL.md §6.3 :373-383]
          list_memories → filter slug-prefix → IF count>20 OR age>90d: delete_memory
          rename_memory (slug-rule change; mem:-ref propagation, v1.5-gated by ROW 7)
          edit_memory (targeted append/provenance)
          → memory_retention_actions, memories_deleted/renamed/edited

 §6.4 think_about_* checkpoints (non-load-bearing)  → serena-checkpoints.log  [SKILL.md §6.4 :385-395]
          (unchanged; all new telemetry rows also flow to audit.log per §4 emit convention :124)

 §6.5 FAIL-OPEN ENVELOPE wraps every NEW call above                 [SKILL.md §6.5 :397-399]
          missing/error → degraded:[<tool>] audit entry → native Grep/Glob fallback → continue
```

## 3. Functional Requirements

> Numbered requirements. Each must be testable and traceable.
>
> **Identifier convention (resolves review finding R6)**: `FR-RV3-LOW.N` names a requirement; `FR-N.M` in its acceptance-criteria list is shorthand for "criterion M of FR-RV3-LOW.N" (e.g. `FR-1.3` ≡ criterion 3 of `FR-RV3-LOW.1`). Downstream task-builder should map `FR-N.M` → `FR-RV3-LOW.N.M`.

### FR-RV3-LOW.1: `find_implementations` polymorphic coverage in Wave 1A

**Description**: Extend the §6.1 chain (SKILL.md:354-367) with a conditional step 3b that invokes `mcp__serena__find_implementations` immediately after `find_symbol` when the located symbol's kind ∈ {Interface, AbstractMethod, Protocol, Trait, **Class**}. Enumerates the polymorphic surface a UC-1 coverage audit must account for and feeds the Drift detector ("interface added, implementor missing"). (`01-matrix:40-97`) **`Class` is included deliberately**: non-Python LSPs report traits/Protocols as `Class` (`01-matrix:69`), so gating on the pure-abstract kinds alone would silently skip implementor enumeration for Rust/TS abstracts (review finding C3). On a `Class` kind a non-empty result IS the polymorphic surface; an empty result is treated as "genuinely none" (no degrade — the call is cheap and fail-open). OQ-6 tracks the diagnostics disambiguation between LSP-error and genuine-empty.

**Acceptance Criteria**:

- [ ] FR-1.1 PASS when, for a UC-1 input whose spec references an abstract symbol, Wave 1A emits `find_implementations_invoked: true` in `audit.log` for ≥1 file.
- [ ] FR-1.2 PASS when `implementations_found: <int>` and `unmapped_implementations: <int>` are present in the audit row for that step.
- [ ] FR-1.3 PASS when the return contract (§9.1 UC-1 block) carries `implementation_coverage_pct: <float 0.0-1.0> | null` and `missing_implementations: [{abstract_name_path, expected_count, found_count}]`.
- [ ] FR-1.4 PASS when, on an explicit LSP error (not a merely-empty result), the chain emits `degraded: ["find_implementations:lsp_unsupported"]` and falls back to a `Grep` for `class .* extends|implements <name>` without blocking.
- [ ] FR-1.5 PASS when a symbol whose LSP kind is `Class` but which is actually a trait/Protocol still triggers `find_implementations` (guard includes `Class`) — verified by the misreported-trait fixture surfacing its implementors (resolves C3).
- [ ] FR-1.6 PASS when a UC-1 spec references NO symbol of an eligible kind: Wave 1A emits `find_implementations_invoked: false` and `implementation_coverage_pct: null` (degenerate no-op, not a failure — resolves C5).

**Telemetry**: `find_implementations_invoked`, `implementations_found`, `unmapped_implementations`; contract: `implementation_coverage_pct`, `missing_implementations`.

**Fail-open behavior** (§6.5, SKILL.md:397-399): explicit LSP error → `degraded: ["find_implementations:lsp_unsupported"]` → Grep fallback → continue. A merely-empty result on a `Class`/abstract kind is "genuinely none", NOT a degrade. The empty-vs-error distinction is made via the `get_diagnostics_for_file` path (OQ-6).

**Dependencies**: Serena ≥ v1.3.0 (tool introduced 2026-05-11). Co-ships with FR-RV3-LOW.2 (shared card schema).

### FR-RV3-LOW.2: `find_declaration` diff-hunk entry point in Wave 1A + 1B.3

**Description**: Add §6.1 step 2a — when the input is a diff-hunk rather than a symbol name, invoke `mcp__serena__find_declaration` (regex with one capture group + `containing_symbol_name_path`) to resolve the hunk's identifiers before continuing to `find_symbol`. Also add a `find_declaration` pre-step to Wave 1B.3 sub-step 1 (SKILL.md:235) for hunks lacking explicit symbol context, eliminating false-positive overlap edges from name collisions. (`01-matrix:101-161`)

**Acceptance Criteria**:

- [ ] FR-2.1 PASS when, for a UC-2 diff-hunk input, Wave 1A emits `find_declaration_invoked: true` in `audit.log` for ≥1 hunk.
- [ ] FR-2.2 PASS when `declaration_resolutions: <int>` and `find_declaration_no_match: <int>` are emitted (a no-match is recorded explicitly, never silently treated as "no declaration exists").
- [ ] FR-2.3 PASS when the return contract carries `hunk_to_declaration_map_path: <abs path>` (UC-2 only).
- [ ] FR-2.4 PASS when Wave 1B.3 overlap edges are anchored to resolved declaration identities rather than textual guesses (verified by absence of name-collision false positives in the eval case).

**Telemetry**: `find_declaration_invoked`, `declaration_resolutions`, `find_declaration_no_match`; contract: `hunk_to_declaration_map_path`.

**Fail-open behavior** (§6.5): on empty/error → `Grep` against the identifier project-wide → `degraded: ["find_declaration"]` → hunk remains in the un-anchored bucket; chain continues.

**Dependencies**: Serena ≥ v1.3.0. Co-ships with FR-RV3-LOW.1.

### FR-RV3-LOW.3: `find_referencing_symbols` extended-info (corrected `find_referencing_code_snippets`)

**Description**: The matrix's row 3 standalone tool appears absorbed into `find_referencing_symbols` extended-info as of v1.0+ (`01-matrix:169-181`). Implement the corrected path: add `include_info: true` to the existing §6.1 step 4 `find_referencing_symbols` call, capturing the denser grouped-excerpt return shape. A Wave 0 runtime tool-inventory probe MUST confirm the standalone tool's absence/presence before this row merges. (`01-matrix:196-216,558`)

**Acceptance Criteria**:

- [ ] FR-3.1 PASS when §6.1 step 4 emits `references_extended_info_used: true` in `audit.log` (this field replaces `find_referencing_code_snippets_invoked`).
- [ ] FR-3.2 PASS when a Wave 0 probe records the live Serena tool inventory and the audit notes whether `find_referencing_code_snippets` is present.
- [ ] FR-3.3 PASS when no new return-contract field is introduced (the substitution reuses existing `find_referencing_symbols` fields).
- [ ] FR-3.4 PASS when, on a Serena build that still exposes the standalone tool, the implementer's MDTM is directed to the §9 Open Item OQ-1 resolution rather than silently wiring the named tool.

**Telemetry**: `references_extended_info_used` (replaces `find_referencing_code_snippets_invoked`).

**Fail-open behavior** (§6.5): identical to existing `find_referencing_symbols` fallback — missing → Grep, `degraded: ["serena"]`, continue.

**Dependencies**: Runtime probe (OQ-1) MUST resolve before merge. No version floor beyond the existing chain.

### FR-RV3-LOW.4: `find_symbol(search_deps=True)` external-dependency grounding

**Description**: Add §6.1 conditional step 7 — when a spec/tasklist symbol resolves to an external dependency, fan out a second `find_symbol` with `search_deps: true` against the dep symbol to retrieve the upstream signature. Converts `[INFERRED]` Necessary-deviation findings into grounded ones. (`01-matrix:220-280`)

**Trigger predicate (operational, resolves review finding R4)**: A "third-party-API citation" is defined NOT by prose pattern-matching but by resolution: **a symbol named in the spec/tasklist whose `find_declaration` (FR-2) resolves to an `<ext:...>` path is, by definition, a third-party-API citation.** This makes the trigger deterministic and reuses FR-2's output — no separate heuristic. The step fires once per distinct `<ext:...>`-resolved symbol.

**Acceptance Criteria**:

- [ ] FR-4.1 PASS when, for an input containing a symbol whose `find_declaration` resolves to an `<ext:...>` path, Wave 1A emits `search_deps_invocations: <int> ≥ 1` in `audit.log`.
- [ ] FR-4.2 PASS when `external_symbols_resolved: <int>` and `external_resolution_failures: <int>` are emitted.
- [ ] FR-4.3 PASS when the return contract carries `third_party_api_grounding: [{api_name, dep_version, resolution_path}]` and a `third_party_api_verified` flag feeds the §10.2 Necessary-deviation classifier.
- [ ] FR-4.4 PASS when an un-indexed venv / missing `additional_workspace_folders` yields `degraded: ["search_deps:lsp_unindexed"]` and the third-party claim stays `[INFERRED]` per §11.1.

**Telemetry**: `search_deps_invocations`, `external_symbols_resolved`, `external_resolution_failures`; contract: `third_party_api_grounding`, `third_party_api_verified`.

**Fail-open behavior** (§6.5): external-resolution failure → `degraded: ["search_deps:lsp_unindexed"]` → skip verification → claim remains `[INFERRED]`; no main-verdict degradation.

**Dependencies**: FR-RV3-LOW.2 (`find_declaration` surfaces the `<ext:...>` path that this step consumes). Ships after the rows 1+2 PR.

### FR-RV3-LOW.5: `summarize_changes` UC-2 drift corroboration (deferred / pilot)

**Description**: Add §6.1 step 7' (UC-2 only) invoking `mcp__serena__summarize_changes` and storing the prompt-output narrative alongside the user-supplied diff as an independent Drift/Necessary-deviation corroboration signal. The tool is prompt-based (returns instructions, not a computed diff) and session-bound; treat output as model-generated narrative, not ground truth. Pilot in the eval workspace before promoting. (`01-matrix:284-329,559`)

**Acceptance Criteria**:

- [ ] FR-5.1 PASS when, in UC-2 mode within the same MCP session as the edits, Wave 1A emits `summarize_changes_invoked: true` and `summarize_changes_path: <output>/serena-change-summary.md`.
- [ ] FR-5.2 PASS when the return contract (§9.1 UC-2 block) carries `serena_summary_corroboration: agree | partial | disagree | unavailable`.
- [ ] FR-5.3 PASS when files named by the Serena summary but absent from the supplied diff feed the §10.3 Drift candidate set, and vice-versa feed the §10.2 Necessary-deviation set.
- [ ] FR-5.4 PASS when a cross-session invocation (reflect runs in a fresh session vs. the edit session) emits `serena_summary_corroboration: unavailable` and skips the Drift-boost logic without degrading the main verdict.

**Telemetry**: `summarize_changes_invoked`, `summarize_changes_path`; contract: `serena_summary_corroboration`.

**Fail-open behavior** (§6.5): session-boundary mismatch or absent tool → `serena_summary_corroboration: unavailable` → skip; `git diff` / `--commit-range` remains source-of-truth (this tool never replaces it).

**Dependencies**: None hard; signature OQ-3 SHOULD be runtime-probed. Ships last (lowest cost/benefit).

### FR-RV3-LOW.6: Onboarding-status signal (corrected `check_onboarding_performed`)

**Description**: `check_onboarding_performed` was **deleted in Serena v1.5.0** (`01-matrix:336,361`). Implement the surviving signal WITHOUT adding the defunct tool to `allowed-tools`: at Wave 0.7, parse the `activate_project` response message for the onboarding-status marker, with a `list_memories` seed-presence proxy (presence of the v1.5 `memory_maintenance` seed memory) as fallback. Feeds `S_dev_density` calibration (grounding-confidence weighted by whether project memory was bootstrapped). (`01-matrix:364-382`)

**Acceptance Criteria**:

- [ ] FR-6.1 PASS when Wave 0 emits `onboarding_status: bootstrapped | not_bootstrapped | unknown` and `onboarding_status_source: activation_msg | list_memories_proxy | unknown` in `audit.log`, using NO new tool call.
- [ ] FR-6.2 PASS when the return contract (§9.2 telemetry) carries `onboarding_status: <string>`.
- [ ] FR-6.3 PASS when `allowed-tools` does NOT contain `check_onboarding_performed` (static assertion against frontmatter — guards against re-introducing the defunct tool).
- [ ] FR-6.4 PASS when neither source is conclusive → `onboarding_status: unknown` and `S_dev_density` is NOT down-weighted (treated as no signal).

**Telemetry**: `onboarding_status`, `onboarding_status_source`; contract: `onboarding_status`.

**Fail-open behavior** (§6.5): inconclusive sources → `unknown` → no rubric impact.

**Dependencies**: FR-RV3-LOW.7 (version fingerprint informs which signal source applies). Ships in the Wave-0-calibration PR with row 7.

### FR-RV3-LOW.7: `get_current_config` Wave 0 version-fingerprint + config snapshot

**Description**: Add §4.0 step 0.5c — invoke `mcp__serena__get_current_config`, parse active context + modes + tool list + Serena version, and persist to `<output>/serena-config-snapshot.yaml`. This is the **version-fingerprint substrate** that gates FR-6 (v1.5 deletion) and FR-8 (v1.5 `rename_memory` propagation), and the source of deterministic `degraded_components: ["serena:context-excluded"]` detection. Ship FIRST. (`01-matrix:386-432`)

**Acceptance Criteria**:

- [ ] FR-7.1 PASS when Wave 0 emits `serena_context: <string>`, `serena_modes: [<list>]`, `serena_tool_count: <int>`, `serena_excluded_tools: [<list>]` in `audit.log`.
- [ ] FR-7.2 PASS when `<output>/serena-config-snapshot.yaml` is written and the return contract (§9.2) carries `serena_config_snapshot_path`, `serena_active_context`, `serena_active_modes`.
- [ ] FR-7.3 PASS when an active context that excludes a chain-critical tool (e.g. `get_diagnostics_for_file`) adds `["serena:context-excluded"]` to `degraded_components` and up-weights `S_dev_density`.
- [ ] FR-7.4 PASS when a **required** derived field `serena_version` is emitted with a three-valued domain `{ "<v1.5" | ">=v1.5" | "unknown" }` (resolves review finding A4). The field name is fixed (not "or equivalent"); when the version cannot be parsed from the `get_current_config` return, `serena_version: unknown` is emitted (never omitted). FR-6 and FR-8 gating branch on this three-valued field.

**Telemetry**: `serena_context`, `serena_modes`, `serena_tool_count`, `serena_excluded_tools`, `serena_version`; contract: `serena_config_snapshot_path`, `serena_active_context`, `serena_active_modes`.

**Fail-open behavior** (§6.5): call failure / tool unavailable in active context → `degraded: ["get_current_config"]` → `serena_version: unknown` → skip snapshot → rest of Wave 0 continues; version-gated rows (6, 8) take the `unknown`-treated-as-`<v1.5` conservative path (no-retention, no-rename-propagation — see FR-8.4 / C2).

**Dependencies**: None (prerequisite for FR-6, FR-8). Return-shape OQ-4 SHOULD be runtime-probed with defensive field-presence checks.

### FR-RV3-LOW.8: Memory-lifecycle retention sweep (`delete_memory` / `rename_memory` / `edit_memory`)

**Description**: Implement the specified-but-unimplemented §6.3 retention rule (SKILL.md:383) at Wave 5 persist using the CRUD trio: `list_memories` → filter by `reflect/last-pass-{slug}` / `reflect/deviation-patterns-{slug}` prefix → **exclude `read_only_memory_patterns`-matched and the current-run entry** → sort remaining by recency → `delete_memory` when count of *deletable* entries > 20 OR age > 90d (`>` strict on both boundaries). Use `rename_memory` (never delete+write) when slug-derivation rules change, to preserve v1.5 `mem:` cross-references. `edit_memory` provides targeted append/provenance. v1.5-gated (rename propagation) via FR-7's fingerprint; on `serena_version ∈ {"<v1.5","unknown"}`, fall back to write-only-no-retention. (`01-matrix:436-525`)

**Invariant (corrected per review finding C1 — CRITICAL)**: the retention guarantee is **"keep the last 20 *deletable* entries per key"**, NOT "keep last 20 total". Read-only memories are excluded from the 20-entry budget. When `(deletable_remaining_after_sweep)` still leaves total slug-prefixed count > 20 because read-only entries dominate, the count is **not** silently assumed bounded — the sweep emits `memory_retention_unbounded: true` + a WARN to `audit.log` so the operational-hygiene gap is loud, never silent. This makes the invariant provable (it ranges only over deletable entries).

**Acceptance Criteria**:

- [ ] FR-8.1 PASS when Wave 5 emits `memory_retention_sweep_invoked: true`, `memories_deleted: <int>`, `memories_renamed: <int>`, `memories_edited: <int>` in `audit.log`.
- [ ] FR-8.2 PASS when, given >20 *deletable* slug-prefixed memories, the sweep deletes the oldest down to 20 deletable and the return contract carries `memory_retention_actions: <int>` and `memory_retention_skipped_readonly: <int>`.
- [ ] FR-8.3 PASS when a slug-rule migration uses `rename_memory` (verified: `mem:` references in dependent memories still resolve post-rename) rather than delete+write.
- [ ] FR-8.4 PASS when `serena_version ∈ {"<v1.5","unknown"}` (from FR-7; `unknown` is treated as `<v1.5` — resolves C2), the sweep degrades to write-only-no-retention with `degraded: ["serena:pre-v1.5-no-rename-propagation"]` and never breaks the reference graph.
- [ ] FR-8.5 PASS when slug derivation sanitizes `..` (v1.2.0 path-traversal guard) and `read_only_memory_patterns`-matched memories are excluded from the deletable budget and counted in `memory_retention_skipped_readonly`.
- [ ] FR-8.6 PASS when read-only entries make the ≤20-total target unreachable: emit `memory_retention_unbounded: true` + WARN; do NOT delete read-only entries; do NOT block the report (resolves C1).
- [ ] FR-8.7 PASS when the slug-prefixed set is empty (first-ever run): emit `memory_retention_sweep_invoked: true` with all-zero counts (degenerate no-op, not skipped — resolves C4); AND the current-run entry is exempt from the age sweep (sweep runs against the pre-existing set before the current `write_memory`, OR excludes the top-recency entry).

**Telemetry**: `memory_retention_sweep_invoked`, `memories_deleted`, `memories_renamed`, `memories_edited`, `memory_retention_unbounded`; contract: `memory_retention_actions`, `memory_retention_skipped_readonly`.

**Fail-open behavior** (§6.5 + existing "Serena `write_memory` fails at Wave 5" row): retention is best-effort → `memory_retention_failed: true` → never blocks the report.

**Dependencies**: FR-RV3-LOW.7 (v1.5 fingerprint gates `rename_memory` propagation). Ships after the rows 1+2 and row 4 PRs.

## 4. Architecture

### 4.1 New Files

> Files created by this work. Include purpose and dependencies.

| File | Purpose | Dependencies |
|------|---------|-------------|
| `<output>/serena-config-snapshot.yaml` | Runtime artifact: `get_current_config` snapshot (context/modes/tools/version) written per-run at Wave 0.5c | FR-7 |
| `<output>/serena-change-summary.md` | Runtime artifact: `summarize_changes` prompt-output narrative (UC-2 only) | FR-5 |
| `.dev/eval-workspaces/sc-reflect/cases/serena-find-implementations/` | Eval case for FR-1 (interface-coverage Drift detection) | FR-1 |
| `.dev/eval-workspaces/sc-reflect/cases/serena-find-declaration/` | Eval case for FR-2 (diff-hunk anchoring, no name-collision false positives) | FR-2 |
| `.dev/eval-workspaces/sc-reflect/cases/serena-search-deps/` | Eval case for FR-4 (third-party API grounding) | FR-4 |
| `.dev/eval-workspaces/sc-reflect/cases/serena-wave0-config/` | Eval case for FR-6 + FR-7 (onboarding parse + config snapshot + version gate) | FR-6, FR-7 |
| `.dev/eval-workspaces/sc-reflect/cases/serena-memory-retention/` | Eval case for FR-8 (retention sweep + rename propagation) | FR-8 |
| `.dev/eval-workspaces/sc-reflect/cases/serena-summarize-changes/` | Eval case for FR-5 (UC-2 corroboration; pilot) | FR-5 |

> Note: `<output>/...` paths are per-run artifacts, not source files. They are listed for contract completeness; only the `.dev/eval-workspaces/sc-reflect/cases/*` directories are committed source.

### 4.2 Modified Files

> Existing files changed. Include nature of change.

| File | Change | Rationale |
|------|--------|-----------|
| `src/superclaude/skills/sc-reflect-protocol/SKILL.md` | §6.1 chain: add steps 2a (`find_declaration`), 3b (`find_implementations`), `include_info:true` on step 4, step 7 (`search_deps`), step 7' (`summarize_changes`). §4.0: add step 0.5c (`get_current_config`); augment step 0.7 (onboarding parse). §6.3: add retention-sweep block. §4.1 step 1B.3: add `find_declaration` pre-step. Frontmatter `allowed-tools`: add `find_implementations`, `find_declaration`, `get_current_config`, `summarize_changes`, `delete_memory`, `rename_memory`, `edit_memory`; MUST NOT add `check_onboarding_performed`. | Core wiring for all 8 FRs at their §-anchored insertion points |
| `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` | Add `S_dev_density` sub-terms: missing-implementor count (FR-1), onboarding-status weight (FR-6), context-exclusion up-weight (FR-7) | New rubric inputs introduced by FR-1/6/7 |
| `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` | Note `third_party_api_verified` (FR-4) and `serena_summary_corroboration` (FR-5) as Necessary-deviation / Drift classifier inputs | New deviation-classifier signals |
| `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` | Add `find_implementations` list + extended-info references to the per-reviewer brief grounding-hunks section (Wave 3 step 3B.0) | FR-1/FR-3 surface into reviewer briefs |
| `src/superclaude/skills/sc-reflect-protocol/refs/return-contract.yaml` *(if present — see OQ-5)* | Add the new contract fields enumerated in §5; bump `contract_version` to `1.1.0` per §9.4 evolution policy | Bulk minor contract bump for FR-1/2/4/8 |

> Per CLAUDE.md SoT discipline: all edits land in `src/superclaude/` then `make sync-dev`. **No `.claude/` paths are touched directly.**

### 4.3 Removed Files [CONDITIONAL: refactoring, portification]

N/A — this is a `new_feature` spec; no files are removed. (`check_onboarding_performed` removal is an *upstream Serena* change, not a file deletion in this repo; FR-6 adapts to it.)

### 4.4 Module Dependency Graph

```
                      FR-7 get_current_config  (version-fingerprint substrate; SHIP FIRST)
                        │  serena_version
            ┌───────────┼────────────────────┐
            ▼           ▼                     ▼
   FR-6 onboarding   FR-8 memory-retention   (degraded_components enrichment)
   (v1.5 signal)     (v1.5 rename-propagation gate)

   FR-1 find_implementations ──┐ (co-ship; shared reflection-card schema, shared v1.3.0)
   FR-2 find_declaration ──────┘
            │ surfaces <ext:...> path
            ▼
   FR-4 find_symbol(search_deps=True)

   FR-3 find_referencing_symbols(include_info) ── gated on OQ-1 runtime probe (independent)
   FR-5 summarize_changes ───────────────────── independent; ship last (pilot)
```

### 4.5 Data Models [CONDITIONAL: new_feature, portification]

> New or modified data structures. Include field definitions. These are the return-contract / audit-log additions (no Python dataclasses — sc:reflect is a skill protocol, not a Python module).

```yaml
# §9.1 RETURN-CONTRACT additions — these are versioned (contract_version 1.0.x → 1.1.0 per §9.4)
# §9.1 UC-1 block
implementation_coverage_pct: <float 0.0-1.0> | null      # FR-1
missing_implementations:                                  # FR-1
  - abstract_name_path: <string>
    expected_count: <int>
    found_count: <int>
# §9.1 UC-2 block
hunk_to_declaration_map_path: <abs-path>                  # FR-2
third_party_api_grounding:                                # FR-4
  - api_name: <string>
    dep_version: <string>
    resolution_path: <string>
third_party_api_verified: <bool>                          # FR-4
serena_summary_corroboration: agree|partial|disagree|unavailable   # FR-5

# §9.2 TELEMETRY block — observability fields, NON-contractual (NOT part of contract_version;
#                        additive telemetry may appear/change without a contract bump per §9.4).
#                        This telemetry-vs-contract split resolves review finding A3.
onboarding_status: bootstrapped|not_bootstrapped|unknown  # FR-6
serena_version: "<v1.5"|">=v1.5"|"unknown"                # FR-7 (required, three-valued — A4/C2)
serena_config_snapshot_path: <abs-path>                   # FR-7
serena_active_context: <string>                           # FR-7
serena_active_modes: [<string>]                           # FR-7
memory_retention_actions: <int>                           # FR-8
memory_retention_skipped_readonly: <int>                  # FR-8
memory_retention_unbounded: <bool>                        # FR-8 (C1 loud-gap flag)
```

### 4.6 Implementation Order

> Dependency-respecting order for implementation. Include parallelization opportunities.

> Note (resolves review findings A1/A2): this order is authoritative and §9 rollout phases map 1:1 to these steps. FR-6 ships WITH FR-7 in the same Wave-0-calibration PR (FR-6 collapses into FR-7's `activate_project` parse — it is not a separate later phase).

```
1. FR-7 get_current_config + FR-6 onboarding parse  -- Wave-0 calibration; FR-6 collapses into
                                                       FR-7's activate_project path (SHIP FIRST, one PR)
2. FR-1 + FR-2 symbol-chain extension  -- [parallel with step 1]; co-ship (shared v1.3.0 + card schema)
3. FR-4 search_deps                    -- depends on FR-2 (<ext:...> path surfacing)
4. FR-8 memory-retention sweep         -- depends on FR-7 (v1.5 rename-propagation gate)
5. FR-3 find_referencing_symbols(include_info)  -- gated on OQ-1 runtime probe; independent of 1-4
6. FR-5 summarize_changes              -- ship last (pilot in eval workspace first)
```

## 5. Interface Contracts [CONDITIONAL: portification, new_feature]

> API contracts, gate criteria, prompt specifications, CLI surface changes.

**New `audit.log` fields** (per-step emit convention, SKILL.md:124): `find_implementations_invoked`, `implementations_found`, `unmapped_implementations` (FR-1); `find_declaration_invoked`, `declaration_resolutions`, `find_declaration_no_match` (FR-2); `references_extended_info_used` (FR-3, replaces `find_referencing_code_snippets_invoked`); `search_deps_invocations`, `external_symbols_resolved`, `external_resolution_failures` (FR-4); `summarize_changes_invoked`, `summarize_changes_path` (FR-5); `onboarding_status`, `onboarding_status_source` (FR-6); `serena_context`, `serena_modes`, `serena_tool_count`, `serena_excluded_tools`, `serena_version` (FR-7); `memory_retention_sweep_invoked`, `memories_deleted`, `memories_renamed`, `memories_edited`, `memory_retention_failed`, `memory_retention_unbounded` (FR-8).

**Contract-versioned fields vs telemetry (resolves review finding A3)**: the `contract_version` bump to `1.1.0` covers the **§9.1 return-contract** additions only — `implementation_coverage_pct` + `missing_implementations` (FR-1), `hunk_to_declaration_map_path` (FR-2), `third_party_api_grounding` + `third_party_api_verified` (FR-4), `serena_summary_corroboration` (FR-5). The **§9.2 telemetry** fields added by FR-6/FR-7/FR-8 (`onboarding_status`, `serena_version`, `serena_config_snapshot_path`/`_active_context`/`_active_modes`, `memory_retention_*`) are **observability, NOT contract** — per §9.4 they may be added without a contract bump, so they are intentionally excluded from the version count. The bump is a single minor (additive, backward-compatible) bump bundling the four contract-bearing FRs (1/2/4/5).

**New rubric inputs** (`refs/reflection-rubric.md`): `S_dev_density` gains the missing-implementor term (FR-1), the onboarding-status weight (FR-6), and the context-exclusion up-weight (FR-7); the §10.2 Necessary-deviation classifier gains `third_party_api_verified` (FR-4); the §10.3 Drift classifier gains `serena_summary_corroboration` (FR-5).

**Fail-open `degraded_components` tokens** introduced: `find_implementations:lsp_unsupported`, `find_declaration`, `search_deps:lsp_unindexed`, `get_current_config`, `serena:context-excluded`, `serena:pre-v1.5-no-rename-propagation`.

### 5.1 CLI Surface [CONDITIONAL: new_feature, portification]

```
# No new user-facing CLI flags. All 8 adoptions are internal protocol behavior,
# auto-active and fail-open. They are observable only via audit.log / return-contract fields.
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| N/A — no new CLI options | N/A | N/A | All adoptions are internal, auto-active, fail-open; surfaced only through telemetry |

### 5.2 Gate Criteria [CONDITIONAL: portification]

N/A — not a pipeline/portification spec; no inter-step gate tiers.

### 5.3 Phase Contracts [CONDITIONAL: portification, infrastructure]

N/A — not a multi-phase pipeline; the wave structure already defines inter-wave contracts in SKILL.md §4.

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-RV3-LOW.1 | **Fail-open**: every new Serena call inherits §6.5 fail-open semantics (SKILL.md:397-399) | 100% of new calls degrade-and-continue on tool-missing/error; skill never aborts on Serena unavailability | Eval case with Serena disabled: skill completes with `status: partial` + populated `degraded_components`; zero hard aborts |
| NFR-RV3-LOW.2 | **Telemetry**: every new tool emits a `<tool>_invoked` field; failure paths emit a `degraded`/`<tool>_failed` field | Every FR's telemetry fields present in `audit.log` on both success and degraded paths | Grader `yaml_field` assertion over `audit.log` + return contract for each FR's named fields |
| NFR-RV3-LOW.3 | **Token budget**: per-feature delta stays within the existing T1/T2 envelopes (T1 ~3-8k Claude / T2 ~35-70k Claude per SKILL.md §15) | Aggregate Wave 0 + Wave 1A + Wave 5 additions ≤ **+1,000 Claude-orchestration tokens** over the T1 path (≈ +15% of the 6.5k T1 band midpoint), measured against a **named baseline**: current `master` HEAD run on the FR-1 eval fixture. `summarize_changes` (prompt-based) and `get_current_config` (single call) contribute near-zero. (resolves review finding R2 — single unit, named baseline) | Run the FR-1+FR-7 eval fixture on baseline vs. branch; diff total Claude output tokens from the run ledger; assert delta ≤ 1,000 |
| NFR-RV3-LOW.4 | **Citation freshness**: any new `file:line` citation passes the CLAUDE.md S1 re-Read rule (§6.2, SKILL.md:369-371) | 100% of citations entering the draft report were re-Read within the last 5 tool calls | Eval assertion: every cited `file:line` in the report has a preceding re-Read in the same wave; `find_implementations`/`find_declaration` outputs that become citations are re-Read before quoting |

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Adopting `check_onboarding_performed` as named → tool-not-found on Serena ≥1.5 | Medium | Medium | FR-6 corrects to `activate_project` parse; FR-6.3 statically asserts the tool is absent from `allowed-tools` |
| Wiring `find_referencing_code_snippets` as a standalone tool when it's been absorbed | Medium | Low | FR-3 corrects to `include_info:true`; OQ-1 runtime probe is a merge precondition |
| `rename_memory` used on pre-v1.5 Serena → `mem:` references break silently | Low | Medium | FR-8.4 gates on FR-7 version fingerprint; pre-v1.5 falls back to write-only-no-retention |
| `find_implementations` empty result misread as "no implementations" (LSP-unsupported language) | Medium | Medium | FR-1.4 disambiguates via diagnostics/kind re-check + Grep fallback before concluding |
| `summarize_changes` treated as ground truth when it's a model-generated narrative | Medium | Low | FR-5 marks it corroboration-only; `git diff`/`--commit-range` stays source-of-truth; `unavailable` on session mismatch |
| Token-budget creep from added Wave 1A chain steps pushing T1 over band | Low | Medium | NFR-3 caps aggregate delta; conditional steps (3b, 7, 7') only fire when their predicate holds |
| `get_current_config` return-shape parse failure (shape not version-stable) | Medium | Low | FR-7 fail-open + defensive field-presence checks (OQ-4); `degraded: ["get_current_config"]` |
| `edit_memory`/retention sweep multi-match silent error (`allow_multiple_occurrences=false` default) | Low | Low | FR-8 uses explicit sorted-prefix filters; eval case covers the multi-match footgun |

## 8. Test Plan

### 8.1 Unit Tests

> sc:reflect is a skill protocol; "unit" granularity here = eval-workspace cases at `.dev/eval-workspaces/sc-reflect/cases/`, one per feature minimum (enumerated, not authored here — authoring is downstream).

| Test | File | Validates |
|------|------|-----------|
| `serena-find-implementations` case | `.dev/eval-workspaces/sc-reflect/cases/serena-find-implementations/` | FR-1: `find_implementations_invoked` emitted; interface-coverage Drift caught; LSP-unsupported fallback |
| `serena-find-declaration` case | `.dev/eval-workspaces/sc-reflect/cases/serena-find-declaration/` | FR-2: diff-hunk anchoring; `find_declaration_no_match` recorded; no name-collision false positives in 1B.3 |
| `serena-referencing-extended-info` case | `.dev/eval-workspaces/sc-reflect/cases/serena-find-declaration/` (shared) | FR-3: `references_extended_info_used` emitted; Wave 0 inventory probe recorded |
| `serena-search-deps` case | `.dev/eval-workspaces/sc-reflect/cases/serena-search-deps/` | FR-4: `search_deps_invocations≥1`; `third_party_api_grounding` populated; un-indexed-venv degrade |
| `serena-summarize-changes` case | `.dev/eval-workspaces/sc-reflect/cases/serena-summarize-changes/` | FR-5: UC-2 corroboration; cross-session → `unavailable` |
| `serena-wave0-config` case | `.dev/eval-workspaces/sc-reflect/cases/serena-wave0-config/` | FR-6 + FR-7: onboarding parse (no defunct tool); config snapshot; context-exclusion → `degraded_components`; version fingerprint |
| `serena-memory-retention` case | `.dev/eval-workspaces/sc-reflect/cases/serena-memory-retention/` | FR-8: >20-entry prune; `rename_memory` ref-propagation; pre-v1.5 write-only fallback; readonly skip |

### 8.2 Integration Tests

| Test | Validates |
|------|-----------|
| Serena-disabled full run | NFR-1: all 8 adoptions degrade-and-continue; `status: partial`; `degraded_components` populated; zero hard aborts |
| Telemetry-completeness sweep | NFR-2: grader `yaml_field` over `audit.log` + contract confirms every FR's `<tool>_invoked` + degraded field on both paths |
| Contract-version bump regression | §5: `contract_version: 1.1.0` present; legacy `input_sha256` subset preserved per §9.4 backward-compat |
| Token-budget delta measurement | NFR-3: aggregate orchestration-token delta within T1/T2 band; conditional steps only fire on predicate |
| Citation-freshness audit | NFR-4: every cited `file:line` in the report re-Read within 5 tool calls (CLAUDE.md S1) |

### 8.3 Manual / E2E Tests [CONDITIONAL: infrastructure, portification]

N/A — eval-workspace cases (8.1) and the Serena-disabled integration run (8.2) provide the E2E coverage; no separate manual scenarios required for a `new_feature` protocol extension.

## 9. Migration & Rollout [CONDITIONAL: refactoring, portification]

> How to transition from current state to new state. Breaking changes, backwards compatibility.

**Rollout grouping** (one PR per phase, per the matrix "Cross-feature observations", `01-matrix:529-562`):

> Phases map 1:1 to §4.6 implementation order (resolves review findings A1/A2 — the two orderings no longer disagree, and FR-7 appears in exactly one phase).

- **Phase 0 — Reclassify FR-6 before wiring anything.** Cite the v1.5.0 deletion verbatim in the MDTM; prevent adding `check_onboarding_performed` to `allowed-tools`.
- **Phase 1 (single PR) — FR-7 `get_current_config` + FR-6 onboarding parse.** The Wave-0 calibration PR: FR-7 lands the version-fingerprint substrate and FR-6 collapses into its `activate_project` parse (shared §9.2 telemetry / `<output>/` artifact). FR-7 ships here and ONLY here.
- **Phase 2 (single PR) — FR-1 + FR-2** symbol-chain extension (shared v1.3.0, shared card schema, same §6.1 neighborhood).
- **Phase 3 (single PR) — FR-4 `search_deps`** (depends on FR-2; follows Phase 2).
- **Phase 4 (single PR) — FR-8 memory CRUD trio**, gated on FR-7's v1.5 fingerprint.
- **Phase 5 (low-priority) — FR-5 `summarize_changes`** last (marginal, prompt-based, pilot first).
- **Defer / verify upstream — FR-3** until the OQ-1 runtime probe confirms absorption.

> Verbatim one-sentence ordering recommendation (`01-matrix:562`): *"Ship `get_current_config` (row 7) first as the version-fingerprint substrate, then bundle `find_implementations` + `find_declaration` (rows 1 + 2) as a single v1.3.0-gated symbol-chain extension PR, then `find_symbol(search_deps=True)` (row 4), then the memory-lifecycle CRUD trio (row 8) gated on the v1.5 fingerprint — deferring `summarize_changes` (row 5) and the absorbed `find_referencing_code_snippets` (row 3) to a post-eval cleanup pass; the `check_onboarding_performed` row (row 6) collapses into row 7's activate-project parse rather than a separate tool call."*

- **Breaking changes**: None. All adoptions are additive and fail-open; absent Serena features degrade rather than break.
- **Backwards compatibility**: `contract_version` 1.0.x consumers tolerate the 1.1.0 minor bump (additive fields only) per the §9.4 evolution policy; legacy `input_sha256` subset preserved.
- **Rollback plan**: Each phase is an independent PR touching only `SKILL.md` + `refs/*` + eval cases. Revert the PR; `make sync-dev` restores the prior `.claude/` mirror. No data migration, no state mutation outside `<output>/`.

## 10. Downstream Inputs

> What this spec feeds into. How downstream consumers (sc:roadmap, sc:tasklist, etc.) use the output.

### For sc:roadmap

Three themes map to milestones: **(M1) Version-fingerprint + Wave-0 calibration** (FR-7, FR-6) — the prerequisite substrate; **(M2) Symbolic-chain grounding extension** (FR-1, FR-2, FR-4) — the load-bearing Wave 1A enrichment; **(M3) Operational hygiene** (FR-8 memory retention) + **(M4) Deferred/probe-gated** (FR-3, FR-5). Critical path: M1 → M2 → M3; M4 is independent post-eval cleanup.

### For sc:tasklist

Task breakdown follows §4.6 implementation order. Each FR is a self-contained MDTM task; FR-1+FR-2 are a single bundled task (shared schema). Every version-sensitive task (FR-6, FR-8) MUST include a Wave-0 `get_current_config` version check as its first step. The §11 Open Items are the runtime-probe / mechanical-check research items task-builder MUST create as preconditions — the full set is **OQ-1, OQ-2, OQ-3, OQ-4, OQ-5** (task-build-time probes/checks); **OQ-6 and OQ-7** are resolved during eval-authoring / Phase 1 respectively, not at task-build time (resolves review finding R1).

## 11. Open Items

> Unresolved questions. Each should have an owner and deadline. Empty section means all questions resolved.

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| OQ-1 | Is `find_referencing_code_snippets` still a standalone Serena tool, or fully absorbed into `find_referencing_symbols` extended-info? (`01-matrix:169-181,558` — sources contradictory) | Blocks FR-3 merge; determines whether wiring is `include_info:true` or a distinct tool | Runtime probe against live Serena MCP at adoption time (before Phase = Defer) |
| OQ-2 | Do SKILL.md's `§9.1`/`§9.2` return-contract+telemetry blocks and `§10.2`/`§10.3` deviation-classifier sections exist with those exact anchors? This spec's FR acceptance criteria and §5 contracts cite them but they were not re-verified against the live SKILL.md at authoring time (closes the OQ-numbering gap from review finding R1). | Mis-anchored FR criteria would target non-existent sections; affects FR-1.3/FR-4.3/FR-5.2/FR-5.3 wiring | Mechanical `grep -n` of `src/superclaude/skills/sc-reflect-protocol/SKILL.md` at task-build time; re-anchor any miss per CLAUDE.md S1 |
| OQ-3 | What is the exact `summarize_changes` tool signature / parameter shape? (`01-matrix:294-298,559` — "unknown / not surfaced"; prompt-based, not a computed diff) | Affects FR-5 invocation correctness; corroboration strength weaker than matrix implied | Pilot in `.dev/eval-workspaces/sc-reflect/cases/serena-summarize-changes/` before promoting from Phase 6 |
| OQ-4 | What is the `get_current_config` return shape? (`01-matrix:396-399,560` — inferred from startup-log shape, "not surfaced", not version-stable) | Affects FR-7 parse robustness and the version-fingerprint extraction that gates FR-6/FR-8 | Runtime probe at Wave 0 of the implementing run; defensive field-presence checks; fail-open on parse failure |
| OQ-5 | Does `refs/return-contract.yaml` exist as a separate file, or is the return contract inline in SKILL.md §9? | Determines whether §5 contract additions edit a YAML file or a SKILL.md section | Read `src/superclaude/skills/sc-reflect-protocol/refs/` at task-build time (mechanical check) |
| OQ-6 | `find_implementations` empty-result disambiguation: which exact diagnostics signal distinguishes "LSP-unsupported" from "genuinely no implementors"? (`01-matrix:71,94`) | Affects FR-1.4 fail-open correctness | Resolve in the FR-1 eval case using `get_diagnostics_for_file` output on an unsupported-language fixture |
| OQ-7 | Minimum supported Serena version for the whole adoption set: v1.3.0 (symbol tools) vs v1.5.0 (memory/onboarding)? Mixed-version behavior matrix | Determines FR-7 gating thresholds and whether the skill declares a hard floor | Decide during Phase 1 (FR-7) using the fingerprint; document per-FR floors (FR-1/2 = v1.3.0; FR-6/8 = v1.5.0) |

## 12. Brainstorm Gap Analysis

> Auto-populated by `sc:cli-portify` Phase 3c embedded brainstorm pass. For manually created specs, use `/sc:brainstorm` to identify gaps.

| Gap ID | Description | Severity | Affected Section | Persona |
|--------|-------------|----------|-----------------|---------|
| G-1 | Upstream-drift hazard: 2 of 8 matrix rows (FR-3, FR-6) reference tools that were deleted/absorbed; spec corrects both but relies on a runtime probe (OQ-1) for FR-3 | High | §3 FR-3/FR-6, §11 OQ-1 | architect |
| G-2 | `summarize_changes` corroboration value is weaker than the matrix value cell implies (prompt-based, session-bound, model-mediated) | Medium | §3 FR-5, §7 | correctness |
| G-3 | Three FR telemetry contracts rely on field names ("not surfaced" return shapes) that may not match runtime; mitigated by fail-open + defensive parse | Medium | §5, §11 OQ-3/OQ-4 | architect |
| G-4 | No explicit minimum-Serena-version declaration for the skill as a whole — per-FR floors exist but a global floor is unresolved | Medium | §11 OQ-7 | architect |

This spec adopts 8 low-complexity Serena features into sc:reflect at their precise wave-insertion points, with two upstream-drift corrections (FR-3 absorbed-tool, FR-6 deleted-tool) and a version-fingerprint substrate (FR-7) gating the version-sensitive rows. The dominant residual risk is **runtime divergence** between the matrix's documentation-derived tool signatures and the live Serena MCP surface — concentrated in OQ-1/OQ-3/OQ-4 and mitigated structurally by the §6.5 fail-open envelope that wraps every new call. No requirement blocks ship on its own; the critical path is FR-7 → {FR-1+FR-2} → FR-4 → FR-8.

---

## Appendix A: Glossary [CONDITIONAL: all types -- include if domain-specific terminology used]

| Term | Definition |
|------|-----------|
| UC-1 / UC-2 | sc:reflect's two use cases: UC-1 pre-execution coverage/gap audit of a strategy vs. its spec; UC-2 post-execution deviation audit of completed work |
| 4-category deviation taxonomy | Authorized expansion / Necessary deviation / Drift / Regression — the classes UC-2 sorts every divergence into (`03-conversation-context.md` §4) |
| §6.1 chain | The mandatory Wave 1A symbol-anchored evidence-gathering chain that replaces `think_about_collected_information` as the load-bearing grounding mechanism (SKILL.md:354-367) |
| Fail-open (§6.5) | Every Serena call degrades-and-continues on failure: missing → `degraded:[tool]` audit entry → native Grep/Glob fallback → never aborts (SKILL.md:397-399) |
| `S_dev_density` | Rubric structural signal: ratio of unmapped diff hunks (UC-2) or unmapped spec requirements (UC-1) to total; several FRs feed sub-terms into it |
| Version-fingerprint substrate | FR-7's `get_current_config` snapshot, the source of the Serena version that gates the v1.5-dependent FRs (FR-6, FR-8) |
| `<ext:...>` path | Serena external-dependency symbol identifier surfaced by `find_declaration`, consumed by `find_symbol(search_deps=True)`; not stable across LS restarts |

## Appendix B: Reference Documents [CONDITIONAL: all types -- include if external references needed]

| Document | Relevance |
|----------|-----------|
| `.dev/releases/current/Reflect-V3-Serena/01-matrix-low-complexity.md` | The 8-row feature-adoption matrix + per-row research deep-dives this spec is derived from |
| `.dev/releases/current/Reflect-V3-Serena/03-conversation-context.md` | Framing, read-only posture clarification (§3), deviation taxonomy (§4), exclusions (§5) |
| `src/superclaude/skills/sc-reflect-protocol/SKILL.md` | Target integration surface; §4 wave structure, §6 Serena usage, §6.5 fail-open policy |
| `src/superclaude/skills/sc-reflect-protocol/refs/` | `reflection-rubric.md`, `deviation-taxonomy.md`, `reviewer-spec.md`, `return-contract.yaml` (OQ-5) — the ref slices that gain content |
| [Serena CHANGELOG (oraios/serena)](https://github.com/oraios/serena/blob/main/CHANGELOG.md) | v1.3.0 symbol tools; v1.5.0 memory `mem:` propagation + `check_onboarding_performed` deletion |
| [Serena memories docs](https://github.com/oraios/serena/blob/main/docs/02-usage/045_memories.md) | Memory CRUD tool surface, `read_only_memory_patterns`, onboarding mechanism (FR-6, FR-8) |
