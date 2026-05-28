# Merge Roadmap — Phase 6 / T06.01

**Task:** T06.01 — Convert manifest to implementation roadmap with dependency graph
**Roadmap Item:** R-019
**Tier:** STRICT
**Generated:** 2026-05-15
**Status:** Driving input for T06.02–T06.05 (per-area refactor plans + unified `merge-master.md`).

**Inputs (1:1 referenced):**
- `transfer-manifest.md` (T05.03) — 8 transfer units TU-1..TU-8, 9 manifest exceptions ME-1..ME-9, locked execution order.
- `rejected-features-ledger.md` (T05.03) — 17 REJECT + 9 DEFER entries; terminal under R-RULE-11.
- `feature-dependency-matrix.md` (T05.01) — DM-1..DM-11 (sequencing) + CR-1..CR-16 (precedence resolutions).
- `extension-point-contracts.md` (T03.02) — extension-point rows referenced by every transfer unit.

**Side-tagging convention (R-RULE-10):** every file path below is tagged `[src]` (source of truth — `src/superclaude/...`) or `[.claude]` (dev copy — `.claude/...`). The recipient attach target re-affirmed in CP-P05-END is `[src] src/superclaude/skills/task/SKILL.md`; the `[.claude] .claude/skills/task/SKILL.md` mirror is byte-identical and is **NOT** the merge target — Phase 7 edits `[src]` then runs `make sync-dev`.

**R-RULE-11 audit (no silent re-litigation):** every roadmap node traces to a `transfer-manifest.md` TU-N. No node re-proposes an `rejected-features-ledger.md` entry. Section 7 enumerates the audit.

---

## 0. Governing principles carried forward

- **R-RULE-06:** every change-set absorbs a *control pattern* from the manifest, never donor ceremony. Where the manifest explicitly drops donor ceremony, this roadmap inherits the drop.
- **R-RULE-10:** `src/superclaude/` is source of truth; `.claude/` is the dev copy. Every file path is side-tagged. Drift is surfaced as an explicit finding (Section 6).
- **R-RULE-11:** the rejected-features ledger is terminal. No roadmap node re-proposes a REJECT/DEFER entry. Section 7 enumerates the cross-check.
- **9 manifest exceptions (ME-1..ME-9):** binding across every roadmap node touching the named TU(s). Listed at the head of each change-set when relevant.

---

## 1. File path verification table

Every file path referenced anywhere in this roadmap, verified via filesystem inspection (`ls`/`md5sum`/`diff`) and side-tagged per R-RULE-10. Sub-agent re-verification is the T06.01 validation step (Section 8).

| # | Path | Side | Status | Notes |
|---|---|---|---|---|
| 1 | `src/superclaude/skills/task/SKILL.md` | [src] | Present (32951 B) | **Recipient merge target.** Phase 7 edits this file. |
| 2 | `.claude/skills/task/SKILL.md` | [.claude] | Present (32951 B) | Byte-identical to row 1; refreshed by `make sync-dev` after row 1 edits. |
| 3 | `src/superclaude/skills/sc-task-protocol/SKILL.md` | [src] | Present (14925 B) | Donor protocol. Targeted by `/sc:task` deprecation (T06.03). |
| 4 | `.claude/skills/sc-task-protocol/SKILL.md` | [.claude] | Present (14925 B) | Byte-identical to row 3. |
| 5 | `src/superclaude/commands/task.md` | [src] | Present (md5 23f50ebc…) | `/sc:task` command file. Source of truth (note: `src/` uses flat layout, no `sc/` subdir). |
| 6 | `.claude/commands/sc/task.md` | [.claude] | Present (md5 23f50ebc…) | Byte-identical to row 5; nested under `sc/` in the dev-copy layout. |
| 7 | `src/superclaude/skills/task-builder/SKILL.md` | [src] | Present (91332 B) | Adjacent skill (task authoring). Referenced by LR-REJECT-3 routing note for D09b. Not modified in this sprint. |
| 8 | `.claude/skills/task-builder/SKILL.md` | [.claude] | Present (91332 B) | Byte-identical to row 7. |
| 9 | `Makefile` (target `sync-dev`, lines 107–122) | [src] | Present | `make sync-dev` rsyncs `src/superclaude/{skills,agents,commands}` → `.claude/`. Targeted by T06.04 distribution refactor for stop-syncing deprecated paths. |
| 10 | `Makefile` (target `verify-sync`, lines 154–183) | [src] | Present | CI-friendly drift detection; must remain green after T06.03 deprecation. |
| 11 | `src/superclaude/cli/install_skills.py` | [src] | Present | Installs skills to `~/.claude/skills/`. Targeted by T06.04 to stop installing deprecated `sc-task-protocol`. |
| 12 | `src/superclaude/cli/install_commands.py` | [src] | Present | Installs commands to `~/.claude/commands/sc/`. Targeted by T06.04 to stop installing deprecated `/sc:task` command. |
| 13 | `.dev/tasks/to-do/TASK-*/` | (no side — task data) | Present (multiple TASK-* dirs) | Existing MDTM consumer files. INV-04 resumability requires every existing file remain valid after T06.02 frontmatter additions. |
| 14 | `.dev/releases/backlog/v5.xxforensic/` | (no side — backlog text) | Present | Carries the highest density of `/sc:task` + `sc-task-protocol` + `sc:task-unified` references (16+ hits across roadmap, sprint-runner, refactor-handoff, tfep-context, forensic-explore). Targeted by T06.03 `refactor-references.md`. |
| 15 | `docs/user-guide/commands.md` | (docs, no side) | Present | References `/sc:task`. Targeted by T06.04 `refactor-documentation.md`. |
| 16 | `docs/user-guide/flags.md` | (docs, no side) | Present | References `/sc:task`. Targeted by T06.04 `refactor-documentation.md`. |
| 17 | `README.md` (root) | (docs, no side) | Present (no `sc:task` or `/task` hits per grep — Phase 6 will re-verify if rows are emitted) | T06.04 README-row check; emit a row only if a reference is found. |

**File-path drift summary:** rows 1↔2, 3↔4, 5↔6, 7↔8 each verified byte-identical. **Zero `src/` vs `.claude/` drift observed during T06.01 path verification.** Section 6 records this as a Phase 6 finding.

---

## 2. Milestones

The 8 transfer units cluster into four ADOPT/ADAPT milestones followed by a deprecation milestone and a distribution/documentation milestone. Order respects `transfer-manifest.md` § 5 build-order rule and the runtime integration-order constraints (CR-7 / CR-8) baked into the SKILL.md edits.

| Milestone | Title | Transfer units / activities | Ship-together? | Purpose |
|---|---|---|---|---|
| **M1** | Foundation — Tier field + Path Override | TU-1, TU-2 | **YES** (per ME-6 + CR-7) | `Tier:` schema + Gate 1 dispatch + Critical/Trivial Path Override land atomically so the row-1 runtime ordering `path_override_check → tier_field_validate → gate_1_dispatch` holds from the first deployment. |
| **M2** | Tier-Conditioned Behaviors | TU-3, TU-4 | No (independent) | Gate 2 widening (TU-3) and First-Item-Protocol pre-flight scaffolding (TU-4) layer on top of M1. Order between them is free. |
| **M3** | TFEP Cluster | TU-5, TU-6, TU-7, TU-8 | Internal ordering required (DM-7 / DM-9) | Test baseline (TU-5) → Prohibitions+Carve-outs (TU-6, independent of M1) → Escalation trigger (TU-7, needs TU-5) → Incident report (TU-8, needs TU-5+TU-6+TU-7). |
| **M4** | `/sc:task` Deprecation | T06.03 outputs (deprecation + reference enumeration); no new TU | No (post-absorption) | Soft/hard deprecation per artifact; reference treatment across `.dev/releases/backlog/*` and the wider repo. Must follow M1–M3 (cannot deprecate what hasn't been absorbed). |
| **M5** | Distribution & Documentation | T06.04 outputs (install, sync, README, user/dev/reference docs); no new TU | No (post-deprecation) | `superclaude install` component-install logic, `make sync-dev` filter rules, README rows, doc updates. Must follow M4. |

**Build-order sentence (per `transfer-manifest.md` § 5):** *M1 ships first as a single merge (TU-1 + TU-2 atomic). M2 + M3 layer on top of M1 (M2 and M3 can interleave; M3 has internal DM-7/DM-9 ordering). M4 follows after M1–M3 complete. M5 follows M4.*

---

## 3. Ordered change-sets per milestone

Each change-set names: **change-set ID** | **manifest TU / ledger source** | **operative paths (side-tagged)** | **extension-point row** | **bound manifest exceptions** | **observable post-condition tag**.

Each change-set in this roadmap is a **macro-level** description; T06.02–T06.05 expand each into the eight-column refactor rows (file path, change, manifest feature, priority, effort, dependencies, acceptance criteria, risk assessment) that drive Phase 7 execution.

### M1 — Foundation (TU-1 + TU-2, ship-together atomic merge)

#### CS-M1-A — `Tier:` field schema extension + Gate 1 dispatch (TU-1)
- **Manifest source:** TU-1 (donor rows D04 cluster + D09a + D10 donor-traceability).
- **Operative paths:** edit `[src] src/superclaude/skills/task/SKILL.md` (recipient attach target); sync `[.claude] .claude/skills/task/SKILL.md` via `make sync-dev`.
- **Extension-point rows touched:** row 13 (required frontmatter schema slot) + row 1 (Task File Validation gate) + row 4 (F1 EXECUTE item-type dispatch).
- **Bound manifest exceptions:** ME-1 (PRE-LOOP DISPATCH ONLY); ME-6 (ship together with Gate 1).
- **Observable post-condition tag:** `Tier:` field closed-enum-validated; single Task Log line `gate-1: dispatch_profile=<...> source=<...>`.
- **Internal ordering note (CR-7 baked in at row 1):** validator inserts the check sequence `path_override_check (CS-M1-B) → tier_field_validate → gate_1_dispatch` — must read as written when CS-M1-B lands in the same merge.

#### CS-M1-B — Critical/Trivial Path Override (TU-2)
- **Manifest source:** TU-2 (donor rows D17 + D18; subsumes catalog rows 35 + 36).
- **Operative paths:** edit `[src] src/superclaude/skills/task/SKILL.md`; sync `[.claude]`.
- **Extension-point rows touched:** row 1 (Task File Validation gate) + row 10 (Phase-Gate QA Verification).
- **Bound manifest exceptions:** none direct; **runtime integration ordering CR-7 + CR-8 hard-required**.
- **Observable post-condition tag:** Task Log line `path-override: forced_stance=<STRICT|LIGHT|none> (matched: <glob>)`.
- **Ship-together obligation:** **MUST** land in the same source-tree merge as CS-M1-A so the runtime row-1 sequence `path_override_check → tier_field_validate → gate_1_dispatch` is locked atomically (CR-7). Path-glob sets sourced verbatim from `[src] src/superclaude/skills/sc-task-protocol/SKILL.md:121` (critical) and `:123` (trivial); paths are read once and inlined — no runtime dependency on the donor file after merge.

### M2 — Tier-Conditioned Behaviors (depends on M1)

#### CS-M2-A — Gate 2 Verification routing widening (TU-3)
- **Manifest source:** TU-3 (donor cluster Gate 2 + D15a donor-traceability + D16 subsumed catalog row 34).
- **Operative paths:** edit `[src] src/superclaude/skills/task/SKILL.md` (Phase-Gate QA section, ~25 lines); sync `[.claude]`.
- **Extension-point row touched:** row 10 (Phase-Gate QA Verification).
- **Bound manifest exceptions:** ME-2 (`rf-qa` SUPPLEMENTED NOT REPLACED).
- **Observable post-condition tag:** Phase-Gate QA report includes `verifier_roster: [rf-qa, quality-engineer]` (STRICT) or `[rf-qa]` (STANDARD/LIGHT/EXEMPT); Task Log `gate-2: profile=<...> budget=<...> roster=[...]`.
- **Dependency:** CS-M1-A (consumes `Tier:`); CS-M1-B (consumes `forced_stance` from row 10 path-override-check).

#### CS-M2-B — D15b Layer 2 pre-flight scaffolding (TU-4)
- **Manifest source:** TU-4 (donor row D15 split → D15b only; D15c explicitly REJECTed via LR-REJECT-7).
- **Operative paths:** edit `[src] src/superclaude/skills/task/SKILL.md` (First Item Protocol section, ~15–25 lines); sync `[.claude]`.
- **Extension-point row touched:** row 2 (First Item Protocol).
- **Bound manifest exceptions:** ME-5 (NO PER-ITEM EXECUTE SUBSTITUTION).
- **Observable post-condition tag:** Task Log line `gate-1.5: pre-flight tier=<...> ran=[...]` (or `ran=[]` for LIGHT/EXEMPT).
- **Dependency:** CS-M1-A (consumes `Tier:` + Gate 1 dispatch).

### M3 — TFEP Cluster (internal DM-7 / DM-9 ordering)

#### CS-M3-A — TFEP Test baseline snapshot (TU-5)
- **Manifest source:** TU-5 (donor row D21).
- **Operative paths:** edit `[src] src/superclaude/skills/task/SKILL.md` (First Item Protocol, co-attached with TU-4, ~15 lines); sync `[.claude]`. **New side-effect file at runtime:** `${TASK_DIR}research/test-baseline.yaml` (file-resident; INV-04 safe; comparator for CS-M3-C).
- **Extension-point row touched:** row 2 (First Item Protocol).
- **Bound manifest exceptions:** ME-4 (BASELINE TIER-GATED to STRICT/STANDARD).
- **Observable post-condition tag:** `research/test-baseline.yaml` exists before F1's first iteration for STRICT/STANDARD tasks.
- **Dependency:** CS-M1-A (consumes `Tier:`); CS-M2-B (TU-4 lands at row 2 first so serena/codebase-retrieval are warm before baseline collection).

#### CS-M3-B — TFEP Prohibitions + Carve-outs (TU-6)
- **Manifest source:** TU-6 (donor rows D19 + D20).
- **Operative paths:** edit `[src] src/superclaude/skills/task/SKILL.md` (Error Handling / blocker logging, ~15 + ~10 lines); sync `[.claude]`. Three VIOLATION strings and three carve-out strings sourced verbatim from `[src] src/superclaude/skills/sc-task-protocol/SKILL.md:127-135` and `:137-140`.
- **Extension-point row touched:** row 8 (Error Handling / blocker logging).
- **Bound manifest exceptions:** ME-3 (SIDE-CHANNEL ONLY, NO F1 HALT).
- **Observable post-condition tag:** Task Log `tfep: prohibition-refusal item=<...> rule=<VIOLATION-NN> reason=<...>` OR `tfep: carve-out item=<...> rule=<carve-out-N> reason=<...>`. **F1 continues regardless** (failing item flips to `- [x]` via existing blocker logging).
- **Dependency:** none from M1 (TU-6 is the TFEP cluster ADOPT entry point; independent of `Tier:`). Recommended sequencing inside M3: land **before** CS-M3-C so prohibition_check / carve_out_check run before escalation classification at row 8.

#### CS-M3-C — TFEP Escalation trigger detection (TU-7)
- **Manifest source:** TU-7 (donor row D22).
- **Operative paths:** edit `[src] src/superclaude/skills/task/SKILL.md` (Error Handling, co-located with CS-M3-B, ~15 lines); sync `[.claude]`. Trigger strings sourced verbatim from `[src] src/superclaude/skills/sc-task-protocol/SKILL.md:200-210`.
- **Extension-point row touched:** row 8 (Error Handling / blocker logging).
- **Bound manifest exceptions:** ME-3 (inherited from TFEP cluster).
- **Observable post-condition tag:** Task Log `tfep: escalation-trigger fired=<N> tests=[...] classification={pre-existing|new}`; on trigger, route to `rf-qa` (existing INV-03 surface — no new gate authored, uses Phase-Gate QA's 3-cycle loop per LR-REJECT-2 rationale).
- **Dependency:** CS-M3-A (consumes `research/test-baseline.yaml` as comparator — DM-7); CS-M3-B (ordered after at row 8 — prohibition+carve-out fire first).

#### CS-M3-D — TFEP Incident reporting (TU-8)
- **Manifest source:** TU-8 (donor row D24).
- **Operative paths:** edit `[src] src/superclaude/skills/task/SKILL.md` (Post-Completion Validation, ~20 lines); sync `[.claude]`. **New side-effect file at runtime:** `${TASK_DIR}research/tfep-incident-report.md` (seven-field schema sourced verbatim from `[src] src/superclaude/skills/sc-task-protocol/SKILL.md:222-234`).
- **Extension-point row touched:** row 11 (Post-Completion Validation).
- **Bound manifest exceptions:** ME-3 (SIDE-CHANNEL ONLY); tier-gated to STRICT items with test-failure history (transitive ME-4 via CS-M3-A).
- **Observable post-condition tag:** `research/tfep-incident-report.md` exists for STRICT items where D22 escalation fired; Post-Completion validation reads the file and verifies the seven-field schema.
- **Dependency:** CS-M3-A + CS-M3-B + CS-M3-C (DM-9 — incident report records the side-effects of the TFEP cluster firing).

### M4 — `/sc:task` Deprecation (post-absorption; T06.03 produces detail)

The roadmap reserves M4 for the deprecation work that T06.03 will detail in `refactor-sctask-deprecation.md` + `refactor-references.md`. M4 cannot start until M1–M3 are absorbed — deprecation may not strand any pattern the manifest absorbed.

#### CS-M4-A — Donor artifact disposition (soft- vs hard-deprecation, per-artifact)
- **Targets (each side-tagged; T06.03 chooses soft vs hard per artifact and justifies):**
  - `[src] src/superclaude/commands/task.md` (the `/sc:task` command file).
  - `[.claude] .claude/commands/sc/task.md` (dev-copy mirror — md5-identical, follows `[src]` via `make sync-dev`).
  - `[src] src/superclaude/skills/sc-task-protocol/SKILL.md` (donor protocol).
  - `[.claude] .claude/skills/sc-task-protocol/SKILL.md` (mirror).
- **Never-load-bearing donor declarations (per Phase 2/4 findings):** the MCP-server list and persona-activation list inside the donor `sc-task-protocol/SKILL.md` were declared but never honored at runtime. M4 removes them explicitly (does not silently orphan them).
- **Bound manifest exceptions:** ME-9 (D02/Layer A REJECT re-affirmed — the `mcp-servers:` advertisement pattern stays out by R-RULE-06).
- **Observable post-condition tag:** every donor artifact has a justified soft/hard verdict in T06.03's `refactor-sctask-deprecation.md`; nothing is silently orphaned.

#### CS-M4-B — Reference enumeration & treatment
- **Scope (T06.03 produces `refactor-references.md`):** every reference to `sc:task`, `sc:task-unified`, `sc-task-protocol`, `sc-task-unified-protocol`, `/sc:task` across the repo. **Highest-density region observed during T06.01 grep:** `.dev/releases/backlog/v5.xxforensic/` (16+ hits across `roadmap.md`, `roadmap-2.md`, `extraction-2.md`, `sprint-runner-tfep-handoff.md`, `forensic-refactor-handoff.md`, `forensic-explore.md`, `tfep-refactoring-context.md`).
- **Treatment options per reference:** update redirect to `/task`; remove if obsolete; leave with a deprecation note pointing at this sprint and the deprecation date.
- **Tooling note:** T06.03 uses `mcp__auggie-mcp__codebase-retrieval` + Serena (`find_referencing_symbols`) for exhaustive enumeration so no reference is missed.

### M5 — Distribution & Documentation (post-M4; T06.04 produces detail)

#### CS-M5-A — Installer & sync-rule changes
- **Targets:**
  - `[src] src/superclaude/cli/install_skills.py` — stop installing `sc-task-protocol` once CS-M4-A's deprecation verdict (hard or soft-with-removed-files) lands.
  - `[src] src/superclaude/cli/install_commands.py` — stop installing the `/sc:task` command file on the same condition.
  - `[src] Makefile` `sync-dev` target (lines 107–122) — stop syncing the deprecated paths; `verify-sync` (lines 154–183) must stay green after the deprecated dirs are removed.
- **Observable post-condition tag:** a fresh `superclaude install` no longer creates `~/.claude/commands/sc/task.md` or `~/.claude/skills/sc-task-protocol/` (assuming hard deprecation); `make verify-sync` returns 0 with the deprecated paths absent on both sides.

#### CS-M5-B — README + user-/developer-/reference-guide updates
- **Targets (re-verified during T06.04):**
  - `docs/user-guide/commands.md` — references `/sc:task` (grep-confirmed).
  - `docs/user-guide/flags.md` — references `/sc:task` (grep-confirmed).
  - `docs/user-guide/*`, `docs/developer-guide/*`, `docs/reference/*` — re-enumerated by T06.04 for residual `sc:task` / `sc-task-protocol` / two-surface-model mentions.
  - `README.md` (root) — T06.01 grep returned no hits; T06.04 re-verifies and emits a row only if a reference exists.
- **Observable post-condition tag:** every doc that previously described `/sc:task` or the two-surface model is updated to reflect the single-surface `/task` post-absorption model OR is annotated with a deprecation note.

---

## 4. Dependency graph

The graph is acyclic. Within-TU co-bindings (DM-1 ↔ DM-2 inside TU-1) are ship-together obligations, not graph cycles.

```text
                     ┌─────────────────────────────────────────┐
                     │  M1 — Foundation (atomic merge)         │
                     │                                         │
                     │   CS-M1-A (TU-1)  ◄──── ship-together ──┼──► CS-M1-B (TU-2)
                     │   Tier: + Gate 1        per ME-6 / CR-7 │   Path Override
                     │                                         │   (runtime row 1: B → A.validate → A.dispatch)
                     └────────────┬────────────────────────────┘
                                  │
            ┌─────────────────────┼─────────────────────┐
            │                     │                     │
            ▼                     ▼                     ▼
  ┌──────────────────┐   ┌──────────────────┐  ┌──────────────────┐
  │ CS-M2-A (TU-3)   │   │ CS-M2-B (TU-4)   │  │ CS-M3-A (TU-5)   │
  │ Gate 2 widening  │   │ D15b pre-flight  │  │ TFEP baseline    │
  │ (uses Tier + FS) │   │ (uses Tier)      │  │ (Tier-gated)     │
  └──────────────────┘   └─────────┬────────┘  └─────────┬────────┘
                                   │                     │
                                   │  (recommended:      │
                                   │   land first so     │
                                   │   serena warm       │
                                   │   for baseline)     │
                                   ▼                     ▼
                       ┌──────────────────────────────────────────┐
                       │ M3 ordering:                             │
                       │                                          │
                       │ CS-M3-A (TU-5)  ──┐                      │
                       │                   ├──► CS-M3-C (TU-7)    │
                       │ CS-M3-B (TU-6) ───┘    (consumes         │
                       │ (independent)          baseline)         │
                       │                                          │
                       │ CS-M3-A + CS-M3-B + CS-M3-C ─► CS-M3-D   │
                       │                                (TU-8)    │
                       └──────────────────────────────────────────┘
                                          │
                                          ▼
                       ┌──────────────────────────────────────────┐
                       │ M4 — /sc:task Deprecation                │
                       │                                          │
                       │   CS-M4-A (donor artifact disposition)   │
                       │   CS-M4-B (reference enumeration)        │
                       │   (both depend on M1+M2+M3 absorbed)     │
                       └────────────┬─────────────────────────────┘
                                    │
                                    ▼
                       ┌──────────────────────────────────────────┐
                       │ M5 — Distribution & Documentation        │
                       │                                          │
                       │   CS-M5-A (installer / sync rules)       │
                       │   CS-M5-B (README + docs)                │
                       └──────────────────────────────────────────┘
```

**Inter-change-set dependency edges (explicit):**

| From → To | Edge type | Source |
|---|---|---|
| CS-M1-A ↔ CS-M1-B | ship-together (atomic merge) | ME-6 + CR-7 (runtime row-1 ordering must hold atomically) |
| CS-M1-A → CS-M2-A | build-order | DM-5 (TU-3 consumes Tier:) |
| CS-M1-B → CS-M2-A | build-order | CR-8 (Gate 2 reads forced_stance) |
| CS-M1-A → CS-M2-B | build-order | DM-10 (TU-4 consumes Tier:) |
| CS-M1-A → CS-M3-A | build-order | DM-6 (TU-5 tier-gated by Tier:) |
| CS-M2-B → CS-M3-A | recommended-order (intra-M3) | TU-4 runs first at row 2 so serena/codebase-retrieval are warm before baseline collection |
| CS-M3-A → CS-M3-C | build-order | DM-7 (TU-7 consumes baseline as comparator) |
| CS-M3-B → CS-M3-C | runtime-order at row 8 | prohibition_check + carve_out_check run before escalation classification |
| CS-M3-A + CS-M3-B + CS-M3-C → CS-M3-D | build-order | DM-9 (TU-8 records TFEP cluster side-effects) |
| (all of M1+M2+M3) → CS-M4-A | absorption-must-precede-deprecation | T06.03 may not strand absorbed patterns |
| CS-M4-A → CS-M4-B | natural-order | reference treatment depends on donor artifact disposition |
| CS-M4-A → CS-M5-A | natural-order | installer / sync rules stop installing artifacts deprecated in CS-M4-A |
| CS-M4-A + CS-M4-B → CS-M5-B | natural-order | docs reflect the deprecation decisions and reference enumeration |

**Acyclicity:** topological order CS-M1-A ≡ CS-M1-B (atomic) → {CS-M2-A, CS-M2-B} → {CS-M3-A → CS-M3-C; CS-M3-B → CS-M3-C} → CS-M3-D → {CS-M4-A → CS-M4-B} → {CS-M5-A, CS-M5-B}.

---

## 5. Manifest-exception binding map (where each ME applies)

| ME | Title | Bound change-sets |
|---|---|---|
| ME-1 | PRE-LOOP DISPATCH ONLY | CS-M1-A |
| ME-2 | `rf-qa` SUPPLEMENTED NOT REPLACED | CS-M2-A |
| ME-3 | SIDE-CHANNEL ONLY, NO F1 HALT | CS-M3-A, CS-M3-B, CS-M3-C, CS-M3-D |
| ME-4 | BASELINE TIER-GATED | CS-M3-A (and CS-M3-D transitively) |
| ME-5 | NO PER-ITEM EXECUTE SUBSTITUTION | CS-M2-B (REJECTs D15c) |
| ME-6 | TIER FIELD + GATE 1 SHIP TOGETHER | CS-M1-A ↔ CS-M1-B (atomic merge obligation) |
| ME-7 | D08 DEFERRED UNTIL PARSER SHIPS | **No M-N change-set authored** — LR-DEFER-5 stays in ledger; T06.04 doc-row must not announce header emission. |
| ME-8 | D01 DEFERRED UNTIL LOADER SEMANTICS + RULE 6 SPLIT | **No M-N change-set authored** — LR-DEFER-4 stays in ledger; T06.04 doc-row must not announce `allowed-tools:` enforcement. |
| ME-9 | D02 / Layer A REJECT (R-RULE-06 override) | CS-M4-A (removal of `mcp-servers:` advertisement is consistent with ME-9). |

Phase 6 downstream tasks (T06.02–T06.05) **must preserve every binding above verbatim**; relaxing any ME is a R-RULE-07 violation.

---

## 6. `src/` vs `.claude/` drift findings (R-RULE-10)

T06.01 path-verification ran `diff -q` and `md5sum` on every paired path. Findings:

| Path pair | Drift detected? | Method | Evidence |
|---|---|---|---|
| `[src] src/superclaude/skills/task/SKILL.md` ↔ `[.claude] .claude/skills/task/SKILL.md` | **No** | `diff -q` (silent) | Both 32951 B; identical |
| `[src] src/superclaude/skills/sc-task-protocol/SKILL.md` ↔ `[.claude] .claude/skills/sc-task-protocol/SKILL.md` | **No** | `diff -q` (silent) | Both 14925 B; identical |
| `[src] src/superclaude/commands/task.md` ↔ `[.claude] .claude/commands/sc/task.md` | **No (byte-identical)**; **layout difference noted** | `md5sum` | md5 `23f50ebc6a89bbc7ef04644af71840f6` on both. Layout: `[src]` keeps commands flat under `src/superclaude/commands/`; `[.claude]` nests under `commands/sc/`. The `sync-dev` Makefile target handles the reshape. |
| `[src] src/superclaude/skills/task-builder/SKILL.md` ↔ `[.claude] .claude/skills/task-builder/SKILL.md` | **No** | `diff -q` (silent) | Both 91332 B; identical |

**Aggregate finding:** **Zero byte-level drift between `src/` and `.claude/` on every path this sprint touches.** One **layout convention** difference (commands flat in `src/` vs nested under `sc/` in `.claude/`) is **architectural, not drift** — `make sync-dev` reshapes flat → nested deliberately. T06.04 distribution refactor must preserve this layout convention when adjusting installer / sync rules.

**Phase 7 obligation (re-affirmed):** every edit lands in `[src]` first; `make sync-dev` then refreshes `[.claude]`; `make verify-sync` must return 0 before commit.

---

## 7. R-RULE-11 cross-check — no ledger entry re-proposed

Every roadmap node above traces to a `transfer-manifest.md` TU-N (Section 8 confirms). The table below confirms no `rejected-features-ledger.md` entry is being re-proposed.

| Ledger entry | Concern | This-roadmap status |
|---|---|---|
| LR-REJECT-1 (D02/Layer A — `mcp-servers:`) | `mcp-servers:` advertisement re-proposed? | **No.** CS-M4-A explicitly **removes** never-load-bearing MCP declarations; ME-9 keeps the advertisement out. |
| LR-REJECT-2 (D25 — 3-strike FULL STOP) | New escalation budget? | **No.** CS-M3-C routes to `rf-qa` (existing INV-03 surface) and relies on Phase-Gate QA's existing 3-cycle loop. No new budget. |
| LR-REJECT-3 (D09b — Classifier) | Runtime classifier inside `/task`? | **No.** `Tier:` arrives declaratively via frontmatter; CS-M1-A reads the field, never classifies. |
| LR-REJECT-4 (Gate 5 — Override flags) | User-toggleable flags? | **No.** CS-M1-B's override is **path-glob-keyed**, not flag-keyed. No flag mechanism authored. |
| LR-REJECT-5 (D03 — Persona auto-activation) | Auto-spawn personas? | **No.** No change-set in this roadmap touches persona activation. |
| LR-REJECT-6 (D13 — Auto-suggest keywords) | Triggering-surface keywords? | **No.** `/task` remains Skill-invoked on a file path. |
| LR-REJECT-7 (D15c — per-tier procedure synthesis) | Execute-time procedure synthesis? | **No.** CS-M2-B is **additive pre-loop setup**, not per-item synthesis (ME-5 explicit). |
| LR-REJECT-8 (D06 — Auto-trigger heuristics) | Prompt-scanning attach? | **No.** No change-set scans prompts. |
| LR-REJECT-9 (D04 Strategy axis) | Strategy-routing layer? | **No.** Only the Compliance axis lands (via TU-1). |
| LR-REJECT-10 (D05 — escalation philosophy) | Philosophy docblock? | **No.** Intent already encoded in `rf-qa` 3-cycle loop and TU-7. |
| LR-REJECT-11 (D07 — CLI flag set) | `--strict` / `--explain` flags? | **No.** `/task` has no CLI surface. |
| LR-REJECT-12 (D11 — few-shot examples) | Few-shot ceremony? | **No.** No few-shot block authored. |
| LR-REJECT-13 / -14 / -16 (D12 / D28 / D30 — Will/Will-Not blocks) | Duplicate of F2/F4? | **No.** No will/will-not blocks authored. |
| LR-REJECT-15 (D29 — Worked examples) | Donor worked examples ported? | **No.** Any examples authored in T06.02–T06.05 are fresh-recipient-specific, not donor ports. |
| LR-REJECT-17 (D31 — Success-criteria metrics) | Metrics package? | **No.** No metrics surface in scope. |
| LR-DEFER-1 / -3 (cluster-as-written aggregates) | Wholesale cluster import? | **No.** Only the absorbable subset lands per TU-1/TU-3/TU-5/TU-6/TU-7/TU-8. |
| LR-DEFER-2 (D27/Gate 3 — per-tier MCP matrix) | Per-tier MCP advertisement? | **No.** Not in scope. CR-3's re-debate authorization remains future-sprint. |
| LR-DEFER-4 (D01 — `allowed-tools:`) | `allowed-tools:` adoption? | **No.** Explicitly bound by ME-8; T06.04 doc rows must not announce enforcement. |
| LR-DEFER-5 (D08 — classification header emission) | Header emission block? | **No.** Explicitly bound by ME-7; T06.04 doc rows must not announce emission. |
| LR-DEFER-6 (D23 — six-step flow + heading insert) | Step 5 heading insertion / Step 6 resume-from-inserted? | **No.** Both REJECTed at TU-8's attach surface; CS-M3-D writes a side-effect FILE only. |
| LR-DEFER-7 (D14 — confidence display bar) | Confidence bar in `/task`? | **No.** Not in scope. |
| LR-DEFER-8 (D26 — feedback collection) | Calibration store? | **No.** Not in scope. |
| LR-DEFER-9 (D32 — external config refs) | External YAML reads? | **No.** Not in scope; `/task` does not read external YAML in this sprint. |

**Cross-check result:** zero ledger entries re-proposed across CS-M1-A through CS-M5-B. R-RULE-11 holds.

---

## 8. Node-to-manifest traceability

Every change-set node traces back to a manifest TU-N (one-to-many allowed; one-to-zero not allowed).

| Change-set | Manifest TU(s) | Donor row(s) | Stack-rank row(s) |
|---|---|---|---|
| CS-M1-A | TU-1 | D04 cluster + D09a + D10 (donor-traceability) | 3 + 6 + 7 |
| CS-M1-B | TU-2 | D17 + D18 | 1 (subsumes catalog 35, 36) |
| CS-M2-A | TU-3 | cluster Gate 2 + D15a (donor-traceability) + D16 | 10 + 11 (subsumes catalog 34) |
| CS-M2-B | TU-4 | D15 split → D15b | 12 |
| CS-M3-A | TU-5 | D21 | 8 |
| CS-M3-B | TU-6 | D19 + D20 | 2 + 4 |
| CS-M3-C | TU-7 | D22 | 9 |
| CS-M3-D | TU-8 | D24 | 5 |
| CS-M4-A | (deprecation of donor artifacts whose patterns are now absorbed by TU-1..TU-8) | n/a (deprecation, not absorption) | n/a |
| CS-M4-B | (reference enumeration of `/sc:task` mentions across the repo) | n/a | n/a |
| CS-M5-A | (distribution-surface refactor consequent on CS-M4-A) | n/a | n/a |
| CS-M5-B | (documentation refactor consequent on M4) | n/a | n/a |

**Forward traceability (every TU has at least one change-set):**

| Manifest TU | Mapped change-set(s) |
|---|---|
| TU-1 | CS-M1-A |
| TU-2 | CS-M1-B |
| TU-3 | CS-M2-A |
| TU-4 | CS-M2-B |
| TU-5 | CS-M3-A |
| TU-6 | CS-M3-B |
| TU-7 | CS-M3-C |
| TU-8 | CS-M3-D |

**Two-way traceability complete: 8 TUs ↔ 8 absorption change-sets (CS-M1-A..CS-M3-D); 4 derivative change-sets (CS-M4-A, CS-M4-B, CS-M5-A, CS-M5-B) execute the deprecation/distribution consequences.**

---

## 9. Acceptance Criteria recap (T06.01)

1. **`merge-roadmap.md` exists with milestones, ordered change-sets, and a dependency graph.** ✅ — Sections 2 (5 milestones M1–M5), 3 (12 ordered change-sets CS-M1-A..CS-M5-B), 4 (acyclic dependency graph with edge table).
2. **Every file path in the roadmap is verified to exist via the T06.01 path-verification table and is side-tagged (R-RULE-10).** ✅ — Section 1 enumerates 17 paths with `[src]` / `[.claude]` tags; all verified present via `ls`/`diff`/`md5sum`.
3. **Every roadmap node traces to a `transfer-manifest.md` feature; no `rejected-features-ledger.md` entry is re-proposed (R-RULE-11).** ✅ — Section 7 cross-checks 26 ledger entries and confirms zero re-proposals; Section 8 confirms 1:1 forward and reverse traceability for the 8 absorption change-sets and routing/deprecation provenance for the 4 derivative change-sets.
4. **Any `src/` vs `.claude/` drift is recorded as an explicit finding.** ✅ — Section 6 reports **zero byte-level drift** across the four paired paths this sprint touches; one architectural layout convention (commands flat in `src/` vs nested in `.claude/sc/`) is recorded as a Phase 6 note for T06.04 to preserve.

---

## 10. Hand-off to T06.02–T06.05

This roadmap stops at the macro level: 12 ordered change-sets, dependency graph, milestone partitioning. The downstream tasks expand each change-set into the eight-column refactor rows required by Phase 7 execution:

- **T06.02 (R-020)** expands CS-M1-A..CS-M3-D into `refactor-task-skill.md` (every `/task` skill edit) and `refactor-mdtm-frontmatter.md` (the single new `Tier:` field with INV-04 backward-compat for existing `.dev/tasks/to-do/TASK-*/` files).
- **T06.03 (R-021)** expands CS-M4-A + CS-M4-B into `refactor-sctask-deprecation.md` (soft/hard per donor artifact) and `refactor-references.md` (exhaustive enumeration of `sc:task` / `task-unified` / `sc-task-protocol` mentions, including the `.dev/releases/backlog/v5.xxforensic/` cluster surfaced in this roadmap).
- **T06.04 (R-022)** expands CS-M5-A + CS-M5-B into `refactor-distribution.md` (installer / `sync-dev` filter / README) and `refactor-documentation.md` (user-guide / developer-guide / reference docs).
- **T06.05 (R-023)** consolidates the five refactor files plus this roadmap into `merge-master.md` with a single ordered table, the consolidated dependency graph, and the recommended execution order.

**T06.01 deliverable: COMPLETE.** Phase 6 has the binding manifest expressed as 5 milestones, 12 ordered change-sets, an acyclic dependency graph, 17 side-tagged file paths verified present, zero `src/` vs `.claude/` drift, and zero ledger re-proposals.
