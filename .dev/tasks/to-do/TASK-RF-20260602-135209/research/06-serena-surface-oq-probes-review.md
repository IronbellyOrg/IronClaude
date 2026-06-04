# Research: Serena Surface + OQ Probes + Review Findings

Topic type: Solution Research + Doc Cross-Validator
Scope: Serena tool surface (version facts), matrix per-row evidence, OQ runtime-probe procedures, spec-panel review R/A/C findings, read-only posture/exclusions
Status: Complete
Date: 2026-06-02

---

NOTE ON SOURCING: This is documentation-derived research. Where the matrix
cites the live Serena MCP tool surface, claims are tagged [MATRIX-SOURCED]
(not [CODE-VERIFIED]) — the actual Serena MCP is external and not inspectable
at task-build time. The OQ probes exist precisely because these facts are not
code-verifiable from this repo.

A small number of claims in this file ARE code-verifiable against this repo
(SKILL.md anchors, refs/ directory contents) and are tagged [CODE-VERIFIED].

---

## 1. Serena version facts (per-FR version floors)

All version facts below are [MATRIX-SOURCED] — sourced from the matrix's
CHANGELOG citations, not from inspecting the live Serena MCP. The matrix cites
`https://github.com/oraios/serena/blob/main/CHANGELOG.md` for each.

### Version gate inventory

| Serena version | Date | What it introduced / changed | Matrix evidence | Affected FRs |
|---|---|---|---|---|
| **v1.1.2** | 2026-04-14 | JetBrains `FindSymbolTool` force-overrides `search_deps=True` when `relative_path` is an external dep; LSP backend respects the flag | matrix:223, matrix:242, matrix:255 | FR-4 (behavior hardened here; `search_deps` itself predates v1.0) |
| **v1.2.0** | (matrix cites changelog, no explicit date) | Path-traversal guard: memory names containing `..` are **forbidden/rejected**; "always provide full activation message upon `activate_project`"; prompt provision session-aware (HTTP mode); `serena_info` tool-inventory probe | matrix:478, matrix:489, matrix:298, matrix:349, matrix:216 | FR-8 (slug sanitization), FR-6 (activation message carries onboarding), FR-3 (serena_info probe) |
| **v1.3.0** | **2026-05-11** | LSP backend adds `find_declaration`, `find_implementations`, `get_diagnostics_for_file`, `get_diagnostics_for_symbol`; Lombok-generated methods included; TS cross-package via `additional_workspace_folders` | matrix:44, matrix:74, matrix:105, matrix:137, matrix:66, matrix:70 | **FR-1, FR-2 (floor = v1.3.0)** |
| **v1.5.0** | **2026-05-18** | (a) `check_onboarding_performed` tool **DELETED** (info moved into `activate_project` message); (b) memory `mem:` cross-reference convention — `rename_memory` propagates references automatically; (c) "Extended Symbol Information" — `find_symbol` + `find_referencing_symbols` now return docstrings + signatures (the absorption of `find_referencing_code_snippets`); (d) `memory_maintenance` seed memory | matrix:336, matrix:361, matrix:440, matrix:493, matrix:181, matrix:185, matrix:349 | **FR-6, FR-8 (floor = v1.5.0)**, FR-3 (absorption) |

### Per-FR version floors (authoritative — from spec OQ-7, spec:525)

| FR | Tool(s) | Version floor | Source | Behavior below floor |
|---|---|---|---|---|
| FR-1 | `find_implementations` | **v1.3.0** | matrix:74, spec:525 | tool-not-found → fail-open degrade → Grep fallback |
| FR-2 | `find_declaration` | **v1.3.0** | matrix:137, spec:525 | tool-not-found → fail-open degrade → Grep fallback |
| FR-3 | `find_referencing_symbols(include_info)` | none beyond existing chain (include_info enriched at v1.5.0) | spec:195, matrix:185 | OQ-1 runtime probe gates; if standalone tool still present, route to OQ-1 |
| FR-4 | `find_symbol(search_deps=True)` | `search_deps` predates v1.0; hardened v1.1.2 | matrix:255 | LSP-unindexed → `degraded:["search_deps:lsp_unindexed"]`, claim stays `[INFERRED]` |
| FR-5 | `summarize_changes` | pre-v1.0 (prompt-based meta-tool) | matrix:310 | session-mismatch → `serena_summary_corroboration: unavailable` |
| FR-6 | `activate_project` parse (NOT `check_onboarding_performed`) | **v1.5.0** (the old tool is gone) | matrix:336, matrix:361, spec:525 | treat `serena_version: unknown` as `<v1.5` (C2) |
| FR-7 | `get_current_config` | pre-v1.0 (stable v1.0+); Windows hang fixed v0.1.3 | matrix:398, matrix:413 | parse failure → `degraded:["get_current_config"]`, `serena_version: unknown` |
| FR-8 | `delete_memory` / `rename_memory` / `edit_memory` | `delete_memory` pre-v1.0; **`rename_memory`+`edit_memory`+`mem:` propagation = v1.5.0** | matrix:493, spec:525 | on `<v1.5` or `unknown` → write-only-no-retention, no rename-propagation (C2) |

**OQ-7 (global floor) is NOT resolved at task-build time** (spec:525 — resolved during Phase 1 via the FR-7 fingerprint). Per-FR floors above are the authoritative gating thresholds. There is no single declared skill-wide minimum; G-4 (spec:536) tracks this as a Medium open gap.

---

## 2. OQ probe precondition items (the §10 directive)

Spec:511 (the "For sc:tasklist" directive) explicitly instructs task-builder:
> "The §11 Open Items are the runtime-probe / mechanical-check research items
> task-builder MUST create as preconditions — the full set is **OQ-1, OQ-2,
> OQ-3, OQ-4, OQ-5** (task-build-time probes/checks); OQ-6 and OQ-7 are
> resolved during eval-authoring / Phase 1 respectively, not at task-build time."

So the MDTM task MUST carry **five precondition items: OQ-1 through OQ-5**.
OQ-6 and OQ-7 are explicitly OUT of the precondition set (do NOT create them as
task-build-time items).

### OQ-1 (FR-3) — `find_referencing_code_snippets` absorption

**The matrix evidence** [MATRIX-SOURCED]:
- matrix:169 — the Tools page does **NOT** list `find_referencing_code_snippets`
  in the current active tool inventory (LSP/JetBrains backend tables).
- matrix:170 — the loaded-tools startup log (Issue #254, n=33 tools) does NOT
  show `find_referencing_code_snippets`; only `find_referencing_symbols` appears.
- matrix:171 — context7 `/oraios/serena` surfaced no current API entry; every
  hit landed on the v0.1 changelog footnote.
- matrix:181 (the CRITICAL status note) — quoting the matrix verbatim:
  > "the tool appears to have been **absorbed into `find_referencing_symbols`**
  > in v1.0 (the extended-info return shape covers what the standalone tool used
  > to provide). The matrix row may be obsolete — verify against the current
  > serena MCP tool list at adoption time."
- matrix:558 (Outstanding research gaps) — "primary-source data is thin … The
  v1.5 extended-info release note suggests absorption. Recommended: run a
  runtime probe against a live Serena MCP before wiring."

**Spec resolution**: FR-3 was REWRITTEN (spec:180-195) to implement the
corrected path — add `include_info: true` to the existing §6.1 step 4
`find_referencing_symbols` call (NOT a new standalone tool). FR-3.2 (spec:188)
makes the Wave-0 inventory probe a PASS criterion; FR-3.4 (spec:189) directs
the implementer to OQ-1 resolution if the standalone tool is still present.

**EXACT runtime probe procedure** (the precondition; spec:519, matrix:184, matrix:216):
1. At Wave 0 of the implementing reflect run, enumerate the live Serena MCP tool
   inventory. Two evidenced mechanisms:
   - **(a)** Invoke the `serena_info` tool (matrix:216 — "emit a `serena_info`
     probe … to enumerate the current Serena tool inventory"), introduced v1.2.0.
   - **(b)** Invoke `get_current_config` (FR-7) — its return includes the loaded
     tools list (matrix:399 — "loaded tools list").
2. Check whether the string `find_referencing_code_snippets` appears in the
   returned tool list.
3. **Branch:**
   - **ABSENT** (expected) → confirm absorption story. Wire the corrected path:
     `find_referencing_symbols(..., include_info=true)`. Emit
     `references_extended_info_used: true` to audit (FR-3.1, spec:185).
   - **PRESENT** (older pinned Serena <v1.0) → do NOT silently wire the named
     tool. Route to the OQ-1 resolution decision per FR-3.4 (spec:189). The
     matrix notes (matrix:189) that even if present, its signature is
     undocumented in current docs — prefer the extended-info path regardless.
4. Record the probe result in `audit.log` (FR-3.2, spec:188 — "the audit notes
   whether `find_referencing_code_snippets` is present").

**Gates:** FR-3 merge. This is a hard blocker — spec:195 "Runtime probe (OQ-1)
MUST resolve before merge."

### OQ-3 (FR-5) — `summarize_changes` signature

**What is known** [MATRIX-SOURCED]:
- matrix:294-298 — signature is "**unknown / not surfaced**"; no parameters
  documented in primary sources. matrix:296: the tool is a **prompt-provider**
  ("Provides instructions for summarizing the changes") — it returns
  instructions to the LLM rather than computing a diff.
- matrix:297 — return is inferred to be a prompt-template string instructing the
  LLM to summarize session changes.
- matrix:298 — v1.2.0 made prompt provision session-aware (HTTP mode);
  cross-session invocation outside an active session returns empty/generic.
- matrix:306 (gotcha) — "**Not a computed diff**" — the matrix's "independent
  check on what was actually changed" claim is **weaker than implied**:
  independent of the user-supplied diff, but still mediated by the same model.
- matrix:559 — "API signature **not surfaced** … only the tool's purpose is
  documented … Recommended: pilot in `.dev/eval-workspaces/sc-reflect/` cases
  before promoting from Phase … status."

**The pilot procedure** (the precondition; spec:521):
- OQ-3 is a **pilot, not a merge-blocking runtime probe**. Resolution method
  (spec:521): "Pilot in `.dev/eval-workspaces/sc-reflect/cases/serena-summarize-changes/`
  before promoting from Phase 6."
- FR-5 ships **last / lowest priority** (spec:231 — "Ships last (lowest
  cost/benefit)"; matrix:545 Phase 5/6).
- The pilot must: (1) invoke `summarize_changes` (paste-ready: `{"tool":
  "mcp__serena__summarize_changes", "arguments": {}}` — matrix:319, treat as
  zero-arg until probed); (2) observe the actual return shape; (3) confirm the
  same-MCP-session requirement (FR-5.1) is satisfiable in the eval harness — see
  review R5 (the harness has no stated session-identity mechanism, so FR-5 is
  "pilot-only, manual"); (4) set `serena_summary_corroboration` ∈
  {agree, partial, disagree, unavailable} (matrix:325, spec:223).
- Dependencies (spec:231): "None hard; signature OQ-3 SHOULD be runtime-probed."
  (SHOULD, not MUST — distinct from OQ-1's MUST.)

**Gates:** FR-5 promotion from deferred/pilot status (not a hard merge block).

### OQ-4 (FR-7) — `get_current_config` return shape

**What is known** [MATRIX-SOURCED]:
- matrix:396-399 — return shape is "**unknown / not surfaced**"; treated as
  zero-arg. matrix:399: the return is "a structured (likely YAML or JSON-rendered)
  string describing: active project, available projects, loaded tools list,
  current context, current modes, and language-backend selection" — **inferred
  from the startup-log shape** (Issue #254), NOT a documented contract.
- matrix:408 (gotcha) — "Output shape is **not stable across Serena versions** —
  context+modes evolved across v1.0 → v1.5. Parsers should defensively check
  field presence."
- matrix:560 — "return-shape **not surfaced** in any current doc; inferred from
  the Serena startup-log shape … Implementers should probe the return shape at
  Wave 0 of the implementing run and fail-open on parse failure."

**The defensive-parse + runtime-probe requirement** (the precondition; spec:522, spec:265):
1. **Runtime probe at Wave 0** of the implementing reflect run (spec:522):
   invoke `get_current_config`, observe the actual return shape against the live
   Serena MCP. This is the FR-7 implementation's own first step.
2. **Defensive field-presence checks** (spec:265 — "Return-shape OQ-4 SHOULD be
   runtime-probed with defensive field-presence checks"): never assume a field
   exists. For each consumed field (active context, modes, tool list, version),
   guard with presence checks; missing field → that derived value = `unknown`.
3. **Version-fingerprint extraction is load-bearing**: `get_current_config` is
   the source of `serena_version`, which gates FR-6 and FR-8 (matrix:553,
   spec:265). Per review A4 + C2, `serena_version` MUST be three-valued
   `{<v1.5, ≥v1.5, unknown}` with `unknown` as the fail-open default treated as
   `<v1.5`.
4. **Fail-open** (spec:257, matrix:429): parse failure → emit
   `degraded: ["get_current_config"]`, skip the snapshot, set
   `serena_version: unknown`, continue Wave 0.

**Gates:** FR-7 parse robustness; transitively FR-6 + FR-8 version gates. SHOULD
be probed (spec:265), not a hard merge block, but the defensive-parse is
mandatory because the shape is documented-unstable.

### OQ-2 (anchors) — RESOLVED POSITIVE by orchestrator

**Status: RESOLVED POSITIVE.** [CODE-VERIFIED] against
`src/superclaude/skills/sc-reflect-protocol/SKILL.md` in this session:
- §9.1 Stable contract → **SKILL.md:491** (`### 9.1 Stable contract (contract_version: 1.0)`) ✓
- §9.2 Telemetry → **SKILL.md:601** (`### 9.2 Telemetry (non-stable)`) ✓
- §10.2 Necessary deviation → **SKILL.md:689** (`### 10.2 Necessary deviation`) ✓
- §10.3 Drift → **SKILL.md:704** (`### 10.3 Drift`) ✓

All four anchors the FR acceptance criteria cite (FR-1.3, FR-4.3, FR-5.2,
FR-5.3) exist. OQ-2 was the closure for review finding R1's OQ-numbering gap
(spec:520).

**The mechanical check the builder includes anyway** (the precondition; spec:520):
Even though resolved positive, the §10 directive lists OQ-2 in the MUST-create
precondition set. The builder includes a mechanical `grep -n` check as a
belt-and-suspenders precondition (per CLAUDE.md S1 freshness discipline — anchors
can drift if SKILL.md is edited between authoring and build):
```
grep -n -E "^### 9\.1|^### 9\.2|^### 10\.2|^### 10\.3" \
  src/superclaude/skills/sc-reflect-protocol/SKILL.md
```
Expected: four hits at (or near) lines 491, 601, 689, 704. If any anchor is
missing or moved, re-anchor the affected FR criteria per CLAUDE.md S1 before the
FR merges. Mis-anchored criteria would target non-existent sections (spec:520).

**Gates:** FR-1.3, FR-4.3, FR-5.2, FR-5.3 wiring (the criteria that cite §9.1/§9.2/§10.2/§10.3).

### OQ-5 (refs) — RESOLVED

**Status: RESOLVED.** [CODE-VERIFIED] — `refs/return-contract.yaml` does **NOT**
exist in `src/superclaude/skills/sc-reflect-protocol/refs/`. Directory contents:
`cost-profile.yaml, coverage-mapping.md, deviation-taxonomy.md,
grader-extensions.md, input-resolution.md, ops-integration.md,
promotion-adapters.md, reflection-rubric.md, remediation-handoff.md,
report-template.md, reviewer-spec.md`. No `return-contract.yaml`.

**Conclusion**: the return contract is **inline in SKILL.md §9** (§9.1 at
SKILL.md:491, §9.2 at SKILL.md:601), not a separate YAML file. Therefore the §5
contract additions (the `contract_version: 1.0 → 1.1.0` bump and the new fields)
**edit the SKILL.md §9.1 section directly**, NOT a YAML file (spec:523).

**The mechanical check the builder includes** (the precondition; spec:523):
```
ls src/superclaude/skills/sc-reflect-protocol/refs/return-contract.yaml \
  2>/dev/null && echo "EDIT YAML" || echo "EDIT SKILL.md §9 inline"
```
Note: spec:318 and spec:561 reference `return-contract.yaml` "(if present — see
OQ-5)" / "(OQ-5)" conditionally — those conditional references resolve to the
SKILL.md-inline path since the file is absent.

**Gates:** determines whether §5 contract-field additions are YAML edits or
SKILL.md §9 edits. RESOLVED → SKILL.md §9 inline.

---

## 3. Per-row matrix deep dives (rows 1-8 → FR-1..FR-8)

The matrix's headline table is at matrix:13-22. Each row below records the
value / cost / risk the matrix assigns, plus the **corrected form** where the
matrix's named tool was wrong. All [MATRIX-SOURCED].

### Row 1 → FR-1 `find_implementations`
- **Cost (matrix:15):** Low. ~10 lines in §6.1 chain + one new schema field on
  the reflection card. Drop-in after `find_symbol` when kind ∈ {interface, abstract}.
- **Value (matrix:15):** **High.** Strengthens UC-1 coverage ("are all
  implementations of `Handler` accounted for?"). Catches "interface added but no
  impl wired" — a recurring **Drift** deviation.
- **Risk (matrix:69):** non-Python LSPs report `Class` instead of
  `Interface`/`Protocol`/`Trait`. matrix:71 — empty result is ambiguous
  ("no implementations" vs "LSP unsupported"); the fail-open path must
  distinguish via diagnostics or kind re-check.
- **Corrected form (review C3 → spec:146):** the kind-guard set **includes
  `Class`** — `kind ∈ {Interface, AbstractMethod, Protocol, Trait, Class}`. On
  `Class`, non-empty result IS the polymorphic surface; empty is "genuinely
  none" (no degrade — cheap + fail-open). OQ-6 tracks the empty-vs-error
  diagnostics disambiguation (resolved in eval-authoring, NOT a build-time OQ).
- **Wave / floor:** Wave 1A §6.1 step 3b (matrix:79); floor **v1.3.0**.

### Row 2 → FR-2 `find_declaration`
- **Cost (matrix:16):** Low. Step between `get_symbols_overview` and
  `find_symbol` when starting from a diff hunk rather than a symbol name.
- **Value (matrix:16):** **Medium.** Diff-hunk → symbol resolution; makes Wave
  1B.3 cross-task scan more precise — fewer false-positive overlap edges from
  name collisions.
- **Risk (matrix:132):** regex with zero matches → empty result (silent miss);
  emit `find_declaration_no_match: true`. matrix:133 — name paths case-sensitive,
  `/`-separated; mistyped `containing_symbol_name_path` → no match.
- **Form:** as-named (correct). Wave 1A §6.1 new step 2a + 1B.3 pre-step
  (matrix:142); floor **v1.3.0**. Bundled with FR-1 (shared schema, shared
  v1.3.0 floor — spec:511 "FR-1+FR-2 are a single bundled task").

### Row 3 → FR-3 `find_referencing_code_snippets` → **CORRECTED to `find_referencing_symbols(include_info=True)`**
- **Cost (matrix:17):** Low. Matrix proposed direct substitute in §6.1 step 4.
- **Value (matrix:17):** Medium. Reduces token cost of Wave 1A grounding when
  reference counts are high (top-30 cap truncates). "Same signal, denser
  packaging."
- **Risk / CORRECTION (matrix:181, matrix:558):** standalone tool **absorbed
  into `find_referencing_symbols` extended-info** (v1.0+/v1.5.0). The actual
  implementation is **`include_info: true` on the existing step-4 call** (spec:180).
  No new return-contract field (FR-3.3, spec:188). Gated on **OQ-1 runtime
  probe** (merge precondition).
- **Wave / floor:** Wave 1A §6.1 step 4 (matrix:197); no floor beyond existing chain.

### Row 4 → FR-4 `find_symbol(search_deps=True)`
- **Cost (matrix:18):** Low. One-flag addition, optional second `find_symbol`
  fan-out when spec/tasklist cites third-party APIs.
- **Value (matrix:18):** Medium. Catches **Necessary deviation** cases (task
  references upstream behavior, e.g. "matches FastAPI's `Depends` contract").
- **Risk (matrix:250-252):** LSP must have indexed deps (venv active);
  `<ext:...|HASH>` identifiers not stable across LS restarts (re-resolve via
  `find_declaration` each time); TS cross-package needs `additional_workspace_folders`.
- **Open predicate (review R4 → spec:40 rec):** "cites a third-party API by
  name" is undefined as written; the operationalized predicate is "a symbol
  whose `find_declaration` resolves to an `<ext:…>` path." Depends on FR-2.
- **Wave / floor:** Wave 1A §6.1 conditional step 7 (matrix:260); `search_deps`
  predates v1.0, hardened v1.1.2.

### Row 5 → FR-5 `summarize_changes`
- **Cost (matrix:19):** Low. Wave 1A UC-2 corroboration vs user-supplied diff.
- **Value (matrix:19):** Medium. Independent check on actual vs claimed changes
  — lever against **Drift**. matrix:306 weakens this: prompt-based, not a
  computed diff, still model-mediated.
- **Risk (matrix:306-307, OQ-3):** signature "not surfaced"; session-aware (must
  invoke in the SAME MCP session as the edits or there's nothing to summarize).
- **Form:** as-named. Wave 1A UC-2-only §6.1 new step 7 (matrix:315). **Ships
  last** (spec:231). Pilot-gated (OQ-3), not merge-blocked.

### Row 6 → FR-6 `check_onboarding_performed` → **CORRECTED to `activate_project` message parse + `list_memories` proxy**
- **Cost (matrix:20):** Low. Matrix proposed "plain check in Wave 0."
- **Value (matrix:20):** Medium. Weights grounding-confidence by whether project
  memory was bootstrapped — input to `S_dev_density` calibration.
- **Risk / CORRECTION (matrix:336, matrix:349, matrix:361):** the tool was
  **DELETED in v1.5.0** (2026-05-18). Adopting as-named emits MCP "tool not
  found" against any Serena ≥ v1.5. **Corrected form (matrix:364-379, spec:FR-6):**
  parse the `activate_project` response message (which reflect already calls at
  Wave 0.7) for the onboarding-status marker; fallback proxy = presence of the
  v1.5 `memory_maintenance` seed memory via `list_memories`. **No new tool added
  to `allowed-tools`** (matrix:382 — task-builder MUST cite the v1.5.0 deletion
  so the implementer doesn't add a defunct tool).
- **Wave / floor:** Wave 0.7 (matrix:365); floor **v1.5.0**.

### Row 7 → FR-7 `get_current_config`
- **Cost (matrix:21):** Low. Single call at Wave 0.
- **Value (matrix:21):** Medium. Deterministic `degraded_components` detection +
  rubric calibration. Reflect currently probes alias env vars but not Serena's
  own config — a blind spot.
- **Risk (matrix:408, OQ-4):** return shape "not surfaced" / not version-stable
  (inferred from startup-log). Defensive field-presence checks + runtime probe
  required. matrix:410 — some single-project contexts disable `activate_project`
  entirely; `get_current_config` reveals this.
- **Form:** as-named. Wave 0 step 0.5c (matrix:418). **No version floor** (it IS
  the version-fingerprint source). **Prerequisite for FR-6 and FR-8** (spec:265).

### Row 8 → FR-8 `delete_memory` / `rename_memory` / `edit_memory`
- **Cost (matrix:22):** Low. Plug into the existing §6.3 90-day TTL / 20-entry
  retention scheme.
- **Value (matrix:22):** Medium. §6.3 retention is **specified but NOT
  implemented** — `write_memory` accumulates without pruning. These three close
  the loop (operational hazard at 6-month horizon).
- **Risk (matrix:487-490):** `rename_memory` `mem:` propagation is **v1.5.0
  only** — on older Serena references break silently. `edit_memory`
  `allow_multiple_occurrences` default `false` is a footgun (multi-match silently
  errors). Path-traversal guard (v1.2.0) rejects `..` in names — slug derivation
  must sanitize. `read_only_memory_patterns` (v1.0.0) makes some memories
  non-deletable.
- **Critical correctness (review C1):** retention invariant is **unprovable**
  under read-only accumulation — see §4 below.
- **Wave / floor:** Wave 5 persist §6.3 (matrix:497); floor **v1.5.0** (for
  rename-propagation). MUST include Wave-0 `get_current_config` version check as
  first step (spec:511).

---

## 4. Spec-panel review findings (R1-R6, A1-A5, C1-C5)

Source: `04-spec-low-complexity.md.review.md` (Wiegers/Adzic/Cockburn +
Fowler/Newman/Hohpe/Nygard + correctness panel). Counts (review:10-14): 1
CRITICAL, 10 MAJOR, 5 MINOR.

### Requirements (R1-R6)
| ID | Sev | Issue | Spec resolution status |
|---|---|---|---|
| R1 | MAJOR (review:20) | OQ numbering gap: §11 had OQ-1,3,4,5,6,7 — no OQ-2; §10 list omitted OQ-6/7 | **RESOLVED** — spec:511 defines build-time set as OQ-1..OQ-5 (OQ-2 added = the anchor check), OQ-6/7 explicitly excluded from preconditions |
| R2 | MAJOR (review:27) | NFR-3 token budget mixes units (turns vs tokens); undefined baseline | Open — measurability fix (review:202 short-term). Builder should carry as a known NFR gap |
| R3 | MINOR (review:33) | `quality_scores` self-assigned, no rubric trace | Cosmetic (review:203) |
| R4 | MAJOR (review:37) | FR-4 "cites a third-party API by name" predicate undefined → FR-4.1 not deterministically testable | Partially addressed — operationalized predicate "symbol whose `find_declaration` resolves to `<ext:…>`" (review:40); carry as FR-4 invariant |
| R5 | MINOR (review:43) | FR-5 "same MCP session" not operationalized in harness | Open → ties to OQ-3 pilot; FR-5 marked pilot-only/manual |
| R6 | MINOR (review:48) | FR-id scheme inconsistent (`FR-RV3-LOW.N` vs `FR-N.M`) | Cosmetic (review:203) |

### Architecture (A1-A5)
| ID | Sev | Issue | Spec resolution status |
|---|---|---|---|
| A1 | MAJOR (review:57) | §4.6 order (FR-6 step 2) contradicts §9 rollout (FR-6 Phase 5) | Must be reconciled (review:201 immediate) |
| A2 | MAJOR (review:63) | FR-7 scheduled in BOTH Phase 1 and Phase 5 | **RESOLVED** — spec:488 "FR-7 ships here [Phase 1] and ONLY here" |
| A3 | MAJOR (review:68) | contract_version 1.1.0 rationale undercounts FR-6/7 fields | **RESOLVED** — spec:402 distinguishes §9.1 contract (FR-1/2/4/5) from §9.2 telemetry (FR-6/7/8, non-contractual, no bump) |
| A4 | MAJOR (review:73) | FR-7.4 `serena_version` "or equivalent" underspecified yet gates FR-6/8 | Addressed via C2 three-valued enum; carry as invariant |
| A5 | MINOR (review:78) | §4.1 mixes per-run artifacts with committed source | Cosmetic (review:203) |

### Correctness (C1-C5) — CRITICAL invariants to carry into the task

These five are the load-bearing correctness invariants. Each MUST become an
acceptance criterion / guard in the FR build items.

- **C1 (CRITICAL, review:89) — memory-retention invariant unprovable under
  read-only accumulation.** Attack trace (review:93-101): `list_memories N=40` →
  slug-filter `M=25`, of which 24 match `read_only_memory_patterns` → deletable
  = 25−24 = 1 → after sweep 24 readonly remain > 20. **INVARIANT VIOLATED.**
  **Required fix (review:104):** when `(M − readonly) > 20` after sweep, emit
  **`memory_retention_unbounded: true` + WARN** to audit; redefine the invariant
  as "keep last 20 **deletable** entries" (read-only excluded from the budget).
  → FR-8 invariant.

- **C2 (MAJOR, review:106) — FR-8.4 v1.5 gate doesn't cover "version unknown".**
  When the config probe fails, `serena_version = unknown` is in neither `{<v1.5}`
  nor `{≥v1.5}`. **Required fix (review:109):** three-valued gate; **treat
  `unknown` as `<v1.5`** (conservative: write-only-no-retention, no
  rename-propagation). State in FR-8.4 AND FR-7's fail-open clause. → FR-7 + FR-8 invariant.

- **C3 (MAJOR, review:111) — FR-1 kind-guard misses traits misreported as
  Class.** matrix:69 — non-Python LSPs report `Class` for traits/Protocols; a
  pure-abstract-kinds guard skips `find_implementations` entirely for Rust/TS
  abstracts → the exact "interface added, implementor missing" Drift is silently
  missed. **Required fix (review:114):** invoke `find_implementations`
  **opportunistically on `Class` kinds too**, empty = "genuinely none" (cheap,
  fail-open covers cost). Already absorbed into spec:146 (guard set includes
  `Class`). → FR-1 invariant.

- **C4 (MAJOR, review:116) — empty/degenerate retention cases unspecified.**
  Zero case (first-ever run, no slug memories) and all-stale case (every entry
  >90d → could delete the just-written current-pass entry). **Required fix
  (review:119):** specify zero case = emit `memory_retention_sweep_invoked: true`
  with all-zero counts; **protect the current-pass entry from the age sweep**
  (order the write AFTER the sweep, or exclude by recency rank). → FR-8 invariant.

- **C5 (MINOR, review:121) — UC-1 no-abstracts degenerate path uncovered.** When
  a UC-1 spec references no abstract/interface symbols, FR-1 step 3b never fires;
  absence-of-signal vs not-run is ambiguous for the grader. **Required fix
  (review:124):** add FR-1 criterion — "WHEN no symbol of kind ∈ {Interface,…}
  is located, emit `find_implementations_invoked: false`;
  `implementation_coverage_pct: null`." → FR-1 criterion.

### State Variable Registry (review:130-138) — quoted rows

These rows define the typed state the FR build items must respect:

| Variable | Type | Initial | Invariant |
|---|---|---|---|
| `serena_version` (FR-7.4) | enum `{<v1.5, ≥v1.5, unknown}` | `unknown` | MUST be one of the three before FR-6/FR-8 gating reads it |
| `slug_memory_count` (FR-8) | int ≥ 0 | actual `list_memories` count | After sweep: `deletable_remaining ≤ 20` (C1 — currently violable) |
| `degraded_components` (§9.2) | list[str] | `[]` | append-only within a run; no duplicates |
| `onboarding_status` (FR-6) | enum `{bootstrapped, not_bootstrapped, unknown}` | `unknown` | `unknown` ⇒ no `S_dev_density` down-weight (FR-6.4) |
| `S_dev_density` (§5.2) | float 0.0–1.0 | computed Wave 1B | monotonic under up-weighting; stays ≤ 1.0 |
| `implementation_coverage_pct` (FR-1.3) | float 0.0–1.0 \| null | `null` | `null` when guard never fired (C5) |
| `serena_summary_corroboration` (FR-5.2) | enum `{agree,partial,disagree,unavailable}` | `unavailable` | `unavailable` on session mismatch ⇒ no Drift boost |

**Guard Condition Boundary Table GAP rows** (review:144-159) — the cells that
must become explicit guards: retention count zero (→C4), `count=25,readonly=24`
(→C1 CRITICAL), current-pass sentinel (→C4), all-stale age (→C4), version gate
`unknown` (→C2 MAJOR), impl kind-guard `Class`-misreport (→C3 MAJOR), impl
no-abstracts (→C5 MINOR), 3rd-party predicate undefined (→R4 MAJOR).

**Expert consensus (review:194-197):** spec is strong on grounding + fail-open;
the dominant correctness hole is C1 (the one provably-wrong item, "must be fixed
before task-builder consumption"); A1/A2/A3 are the highest-leverage
requirements fixes; R4/A4/C2/C3 share the root cause of runtime-shape uncertainty
in the Serena surface (tracked in OQ-1/3/4).

---

## 5. Read-only posture / exclusions (what is OUT of scope)

Source: `03-conversation-context.md` §3 (posture) and §5 (exclusions). The
builder MUST NOT let any FR stray into these.

### Read-only boundary (conversation-context:57-70)
- ❌ sc:reflect **does NOT** mutate project source code, config, or tests
  (conversation-context:65). Source edits are the **Tier 3 task-builder → MDTM
  remediation handoff** target, NOT sc:reflect itself.
- ✅ sc:reflect **DOES** write `audit.log`, `serena-checkpoints.log`,
  `reviewer-briefs/`, the final report, return-contract YAML, and Serena memory
  blobs (conversation-context:66). → FR-8 memory CRUD is IN scope (writes to
  Serena memory, not project source).
- ✅ sc:reflect **MAY** run non-mutating verification — `pytest`, `ruff`, `mypy`,
  `make test`, `uv run`, build (conversation-context:67).
- ❌ sc:reflect **may NOT** `git commit`, `git push`, edit files outside its own
  `<output>/`, package installs, or any side-effecting state change
  (conversation-context:68).

### Excluded items — do NOT research/wire (conversation-context:89-101)
| Excluded | Why (conversation-context) |
|---|---|
| `list_dir`, `find_file`, `read_file` (Serena-native FS ops) | Worse than native `Read`/`Grep`/`Glob`; introduce a freshness re-verification gap vs CLAUDE.md S1, no offsetting benefit (cc:95) |
| Dashboard / built-in audit-log surface | Duplicates `audit.log` + `serena-checkpoints.log` (cc:96) |
| HTTP/SSE transport + multi-agent shared instance | High infra cost; cross-skill platform work, defer (cc:97) |
| `initial_instructions` | Marginal ~1K tokens/subagent; better spent on `reviewer-spec.md` (cc:98) |
| `restart_language_server` | Pure resilience, low impact; OK as unobtrusive fallback retry only (cc:99) |
| `switch_modes` + custom Contexts/Modes | Medium-high cost + upstream drift risk for Medium value (cc:100) |
| **Symbolic editing tools** — `insert_before_symbol`, `insert_after_symbol`, `replace_symbol_body`, `rename_symbol`, `safe_delete_symbol`, `replace_content` | **Mutate project source code** — out of scope under §3 posture. Route to **Tier 3 task-builder** as the remediation execution surface (cc:101) |

**Boundary note (cc:101):** the symbolic editing tools and `replace_content` are
explicitly NOT for sc:reflect — they belong to the Tier 3 remediation chain. No
FR-RV3-LOW item may wire them. (Distinguish from FR-8's `edit_memory` /
`rename_memory` / `delete_memory`, which operate on **Serena memory blobs**, not
project source — those ARE in scope.)

---

## 6. Summary tables

### OQ-probe precondition table (OQ → procedure → FR gated → blocking?)

The MDTM task MUST create OQ-1..OQ-5 as precondition items (spec:511). OQ-6/OQ-7
are NOT build-time preconditions.

| OQ | Probe / check procedure | Method | FR gated | Blocking? |
|---|---|---|---|---|
| **OQ-1** | At Wave 0, enumerate live Serena tool inventory (`serena_info` or `get_current_config` tool list); check for `find_referencing_code_snippets`. ABSENT → wire `find_referencing_symbols(include_info=true)`; PRESENT → route to OQ-1 decision per FR-3.4. Record in audit. | Runtime probe vs live Serena MCP at adoption | **FR-3 merge** | **YES — MUST resolve before merge (spec:195)** |
| **OQ-2** | `grep -n -E "^### 9\.1\|^### 9\.2\|^### 10\.2\|^### 10\.3" src/superclaude/skills/sc-reflect-protocol/SKILL.md` → expect hits ~491/601/689/704; re-anchor any miss per S1 | Mechanical grep at build time | FR-1.3, FR-4.3, FR-5.2, FR-5.3 wiring | **RESOLVED POSITIVE** (anchors verified) — check kept as belt-and-suspenders |
| **OQ-3** | Pilot `summarize_changes` (zero-arg) in `.dev/eval-workspaces/sc-reflect/cases/serena-summarize-changes/`; observe return shape; confirm same-MCP-session satisfiable (R5); set corroboration enum | Pilot in eval workspace | FR-5 promotion (Phase last) | SHOULD probe (spec:231) — pilot, not hard merge block |
| **OQ-4** | Runtime probe `get_current_config` at Wave 0 of implementing run; defensive field-presence checks; extract three-valued `serena_version`; fail-open → `unknown` | Runtime probe + defensive parse | FR-7 parse; transitively FR-6 + FR-8 version gates | SHOULD probe (spec:265); defensive-parse MANDATORY |
| **OQ-5** | `ls refs/return-contract.yaml` → absent → §5 contract edits target SKILL.md §9 inline | Mechanical check at build time | §5 contract-field placement | **RESOLVED** — file absent, edit SKILL.md §9 inline |
| OQ-6 | (NOT a build-time precondition) `find_implementations` empty-vs-error disambiguation via `get_diagnostics_for_file` | Resolved in FR-1 eval-authoring | FR-1.4 fail-open | excluded from preconditions (spec:524) |
| OQ-7 | (NOT a build-time precondition) global minimum Serena version | Decided in Phase 1 via FR-7 fingerprint | FR-7 gating thresholds | excluded; per-FR floors authoritative (spec:525) |

### Version-floor table (per-FR)

| FR | Tool | Floor | Treatment below floor / on `unknown` |
|---|---|---|---|
| FR-1 | `find_implementations` | **v1.3.0** | fail-open degrade → Grep |
| FR-2 | `find_declaration` | **v1.3.0** | fail-open degrade → Grep |
| FR-3 | `find_referencing_symbols(include_info)` | none (enriched v1.5.0) | OQ-1 probe gates |
| FR-4 | `find_symbol(search_deps=True)` | pre-v1.0 (hardened v1.1.2) | `degraded:["search_deps:lsp_unindexed"]`, claim `[INFERRED]` |
| FR-5 | `summarize_changes` | pre-v1.0 | `serena_summary_corroboration: unavailable` |
| FR-6 | `activate_project` parse (old tool deleted) | **v1.5.0** | `unknown` treated as `<v1.5` (C2) |
| FR-7 | `get_current_config` | pre-v1.0 (it's the fingerprint source) | parse fail → `serena_version: unknown` |
| FR-8 | `delete_memory`/`rename_memory`/`edit_memory` | **v1.5.0** (rename `mem:` propagation) | `<v1.5`/`unknown` → write-only-no-retention, no rename-propagation (C2) |

### Critical invariants the FR build items MUST carry

1. **C1** — `memory_retention_unbounded: true` + WARN when `(M − readonly) > 20`;
   invariant = "keep last 20 **deletable**" (→ FR-8).
2. **C2** — three-valued `serena_version`; `unknown` ≡ `<v1.5` (→ FR-7, FR-8).
3. **C3** — kind-guard set includes `Class`; empty-on-Class = "genuinely none"
   (→ FR-1).
4. **C4** — zero-case emits `invoked:true` + zero counts; current-pass entry
   exempt from age sweep (→ FR-8).
5. **C5** — no-abstracts no-op emits `find_implementations_invoked: false`,
   `implementation_coverage_pct: null` (→ FR-1).
6. **A2** — FR-7 ships in Phase 1 ONLY.
7. **A3** — contract_version 1.1.0 bump = §9.1 fields (FR-1/2/4/5) only; §9.2
   telemetry (FR-6/7/8) is non-contractual, no bump.
8. **R4/A4** — FR-4 predicate operationalized as "symbol whose `find_declaration`
   resolves to `<ext:…>`".

---

Status: Complete
