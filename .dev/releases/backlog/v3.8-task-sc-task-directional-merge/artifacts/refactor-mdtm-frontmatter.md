# Refactor Plan — MDTM Frontmatter Extensions (Phase 6 / T06.02)

**Task:** T06.02 — Refactor plans: `/task` skill edits & MDTM frontmatter extensions
**Roadmap Item:** R-020
**Tier:** STRICT
**Generated:** 2026-05-15
**Status:** Driving input for Phase 7 execution. Defines the new MDTM frontmatter field introduced by the manifest, the per-item inline-marker schema that complements it, and the **INV-04 backward-compat treatment** for every existing `.dev/tasks/to-do/TASK-*/` file already on disk.

**Companion artifact:** `refactor-task-skill.md` — the twelve eight-column change rows that edit `[src] src/superclaude/skills/task/SKILL.md` to consume the schema authored here.

**Scope boundary (R-RULE-11):** This refactor authors **exactly one** new MDTM frontmatter field (`Tier:`) plus its companion per-item inline marker — both introduced by TU-1. No other manifest TU introduces a frontmatter field (TU-2..TU-8 introduce side-channel hooks, side-effect files, and runtime-emitted Task Log lines, but no MDTM frontmatter additions). LR-DEFER-4 (D01 `allowed-tools:`) and LR-DEFER-5 (D08 classification header) explicitly REMAIN deferred — neither is added by this refactor.

---

## 0. Side-tagging convention (R-RULE-10)

The schema authored here is consumed by `[src] src/superclaude/skills/task/SKILL.md` (the task SKILL — the *consumer* of the schema). Existing MDTM files on disk live under `.dev/tasks/to-do/TASK-*/` (no `[src]`/`[.claude]` side — task-data, not distributable code, not synced).

---

## 1. Column legend

Every frontmatter change row carries the same eight columns as `refactor-task-skill.md`:

| Column | Meaning |
|---|---|
| **CR-ID** | Stable change-row identifier (`CR-FM-NN` — "frontmatter"). |
| **File path (side-tagged)** | The consumer file (SKILL.md) whose frontmatter-schema documentation gains the field, AND the population scope (which `.dev/tasks/to-do/TASK-*/` files may carry the field). |
| **Change** | The schema operation: `add new frontmatter field` / `add inline marker schema` / `add compat shim` / `document optional`. |
| **Manifest feature(s)** | The TU-N / ME-N / donor row(s) the schema implements. |
| **Priority (P0–P3)** | Foundation (P0), depends-on-P0 (P1), tier-conditioned (P2), validation/audit (P3). |
| **Effort (XS–XL)** | Schema-doc edit size. |
| **Dependencies** | Build-order edges to other CR-FM-NN rows AND to CR-TASK-NN rows in the companion refactor. |
| **Acceptance criteria** | Observable post-condition — what a Phase 7 reviewer verifies (validator behavior, file existence, frontmatter content). |
| **Risk assessment** | INV-NN at risk + mitigation (with explicit INV-04 backward-compat treatment per T06.02 acceptance #3). |

---

## 2. Change rows — MDTM frontmatter schema additions

Four change rows: one new field, one companion inline-marker schema, one backward-compat default, one validator-side audit. Together they cover every schema delta TU-1 introduces and explicitly preserve INV-04 (resumability) for every existing TASK-* file.

### CR-FM-01 — Add new optional MDTM frontmatter field `Tier:`

| Column | Value |
|---|---|
| **CR-ID** | CR-FM-01 |
| **File path (side-tagged)** | **Schema documented in** `[src] src/superclaude/skills/task/SKILL.md` — *Validating the Task File* section (line 68 currently reads "Has YAML frontmatter with at least: `id`, `title`, `status`, `created_date`"). Extension-point row 13 of `extension-point-contracts.md:169-175` is the formal slot. **Population scope:** any **new** MDTM file (existing TASK-* files MAY add the field but are NOT required to — see CR-FM-03). |
| **Change** | `add new frontmatter field` — `Tier:` (singular, capitalized — matches donor convention from `src/superclaude/skills/sc-task-protocol/SKILL.md:121,123`). **Type:** string. **Value set (closed enum):** `STRICT` | `STANDARD` | `LIGHT` | `EXEMPT`. **Cardinality:** optional. **Default when absent:** `STANDARD` (resolved at Gate 1 dispatch by CR-TASK-02). |
| **Manifest feature(s)** | TU-1 (Tier field + Gate 1 dispatch); donor row D09a; stack-rank row 3. ME-1 (PRE-LOOP DISPATCH ONLY) constrains how the field is consumed. ME-6 (TIER FIELD + GATE 1 SHIP TOGETHER) binds the field to the validator/dispatcher merge. |
| **Priority** | **P0** — foundation field; CR-FM-02..04 and every consumer change row in `refactor-task-skill.md` depend on this row. |
| **Effort** | **XS** — ~1 line added to the validator's required-frontmatter list (turning the line into "at least: `id`, `title`, `status`, `created_date`; optionally `Tier:`") plus ~3 lines documenting the enum and default in the same section. |
| **Dependencies** | None upstream. Ship-together with CR-FM-02 + CR-TASK-01 + CR-TASK-02 + CR-TASK-03 (the TU-1 atomic merge). |
| **Acceptance criteria** | (1) The schema is **optional** — a task file without `Tier:` validates clean (resolved to `STANDARD` at Gate 1). (2) The schema is **closed-enum** — a task file with `Tier: AGGRESSIVE` (or any non-enum value) is REJECTed with a refusal diagnostic naming the closed set. (3) The schema is **singular** — no `tiers:` list, no `Tier-Override:`, no synonym. The donor's `Tier:` casing is preserved verbatim. |
| **Risk assessment** | **INV at risk: INV-04 (resumability)** if the field is made REQUIRED — every existing TASK-* file on disk would fail validation on next resumption. **Mitigation:** field is **optional**, default `STANDARD` resolves missing values silently. CR-FM-03 documents the compat shim explicitly. Additional **INV at risk: INV-01 (loop control)** if the validator hard-fails on unknown values without a refusal diagnostic mid-loop — **mitigation:** validation runs at task entry only (pre-loop), not per-item; closed-enum rejection produces a single refusal diagnostic and HALTS task entry cleanly (not mid-F1). Additional **risk: LR-DEFER-4 / LR-DEFER-5 re-proposal** by quietly bundling `allowed-tools:` or classification-header schema into this row — **mitigation:** this row introduces **exactly one** field (`Tier:`); ME-7 and ME-8 are observed-but-not-emitted in CR-FM-01..04. |

### CR-FM-02 — Per-item inline-marker schema `(Tier: <value>)`

| Column | Value |
|---|---|
| **CR-ID** | CR-FM-02 |
| **File path (side-tagged)** | **Schema documented in** `[src] src/superclaude/skills/task/SKILL.md` — *F1 Execution Loop — EXECUTE step* (lines 89–96, consumed by CR-TASK-03). **Population scope:** any individual checklist item in a new or existing MDTM file. |
| **Change** | `add inline marker schema` — an optional inline marker `(Tier: STRICT)` / `(Tier: STANDARD)` / `(Tier: LIGHT)` / `(Tier: EXEMPT)` immediately AFTER the item's `- [ ]` or `- [x]` prefix and BEFORE the item text. Example: `- [ ] (Tier: LIGHT) trivial doc-typo fix in README.md`. **Cardinality:** optional per-item. **Default when absent:** falls back to the task-level `Tier:` field (CR-FM-01) — which itself falls back to `STANDARD` when absent. |
| **Manifest feature(s)** | TU-1 ("Per-item annotation supported as inline marker, task-level value is the fallback" — manifest § 2 TU-1 Integration sketch). ME-1 (PRE-LOOP DISPATCH ONLY) binds: the marker is a tier-conditioned read for behaviors already gated, NEVER a re-dispatch trigger. |
| **Priority** | **P0** — ships in the TU-1 atomic merge with CR-FM-01. |
| **Effort** | **XS** — ~2 lines documenting the inline-marker grammar (regex `^- \[[ x]\] \(Tier: (STRICT\|STANDARD\|LIGHT\|EXEMPT)\) `) in the EXECUTE step. |
| **Dependencies** | CR-FM-01 (consumes the closed-enum set authored once); CR-TASK-03 (the consumer parser). |
| **Acceptance criteria** | (1) An item `- [ ] (Tier: LIGHT) trivial doc-typo` is parsed with `tier_value=LIGHT` for that item; the surrounding items inherit the task-level `Tier:` (or `STANDARD` if absent). (2) An item without the inline marker uses the task-level fallback (no warning, no error). (3) An item with `(Tier: AGGRESSIVE)` (non-enum) is logged as a malformed-marker WARNING in Task Log and falls back to the task-level value — does NOT halt F1 (ME-3 spirit: side-channel warning, not a loop-control branch). (4) The inline marker is **read-only** for the item — it never re-fires Gate 1 dispatch (ME-1 binding). |
| **Risk assessment** | **INV at risk: INV-01 (loop control)** if a future variant allows the per-item marker to re-fire Gate 1 — Gate 1 would re-evaluate loop control per-item. **Mitigation: ME-1 (PRE-LOOP DISPATCH ONLY)** binds; the marker is consumed by CR-TASK-03's read-only tier-conditioned check, never by `gate_1_dispatch`. Additional **INV at risk: INV-05 (items must come from disk read)** if the marker syntax is extended to *embed* runtime steps (e.g., `(Tier: STRICT; run: pytest)`) — **mitigation:** schema authored here is strictly `(Tier: <enum>)`; no other parenthesized parameters are permitted. Phase 7 must reject any future extension proposal without a fresh manifest entry (R-RULE-11). Additional **risk: drift from task-level closed-enum** if the inline-marker parser is authored with a different value set than CR-FM-01 — **mitigation:** parser uses the same closed-enum constant defined once for CR-FM-01 (single source of truth). |

### CR-FM-03 — Backward-compat default for existing `.dev/tasks/to-do/TASK-*/` files (INV-04)

| Column | Value |
|---|---|
| **CR-ID** | CR-FM-03 |
| **File path (side-tagged)** | **Schema documented in** `[src] src/superclaude/skills/task/SKILL.md` — *Validating the Task File* section (lines 65–73). **Population scope:** every existing MDTM file under `.dev/tasks/to-do/TASK-*/` at the time of merge (≥30 task directories observed during T06.02 spot-check, including but not limited to `TASK-PRD-20260514-121039/`, `TASK-E2E-20260326-tdd-pipeline/`, `TASK-RESEARCH-20260324-001/`, `TASK-RF-20260325-cli-tdd/`, every `TASK-*` directory in the listing). |
| **Change** | `add compat shim` — Gate 1 dispatch (CR-TASK-02) resolves a missing `Tier:` field to the **default `STANDARD`** silently. Validating-the-task-file documentation explicitly states: "Task files without a `Tier:` field are valid; they execute under the `STANDARD` profile. Existing tasks resumed after this refactor lands need NO migration — their behavior is unchanged from the pre-refactor `STANDARD` budget." NO migration of existing files is required, attempted, or recommended. |
| **Manifest feature(s)** | INV-04 (resumability) — the load-bearing invariant for this row. Manifest § 2 TU-1 Integration sketch: "Missing value defaults to `STANDARD` at Gate 1." ME-6 (Tier field + Gate 1 ship together) carries this default into Gate 1's logic. |
| **Priority** | **P0** — ships in the TU-1 atomic merge; without this compat shim every existing TASK-* file would fail validation on first resumption after merge. |
| **Effort** | **XS** — ~2 lines documentation in *Validating the Task File* + the existing default-resolution path inside CR-TASK-02's Gate 1 dispatch (already authored in `refactor-task-skill.md` CR-TASK-02). No code outside SKILL.md is touched. |
| **Dependencies** | CR-FM-01 (the field whose absence this row handles); CR-TASK-02 (the Gate 1 dispatcher that resolves the default). |
| **Acceptance criteria** | (1) A task file matching any existing TASK-* file on disk today (no `Tier:` field in frontmatter) validates clean and executes under the `STANDARD` profile. (2) Gate 1's Task Log line for such a task reads `gate-1: dispatch_profile=STANDARD source=default` (the third clause of CR-TASK-02's acceptance #2). (3) NO task file under `.dev/tasks/to-do/TASK-*/` is rewritten or backfilled by this refactor — the compat shim is a *read-time default*, not a *write-time migration*. (4) An existing in-progress task (status `🟠 Doing`) resumed after merge continues from its first unchecked item with **identical behavior** to pre-refactor, save that a `gate-1: ... source=default` line is now emitted at resumption-entry. |
| **Risk assessment** | **INV at risk: INV-04 (resumability)** — load-bearing for this row. If the field were made REQUIRED, every existing TASK-* file would fail validation on resumption. **Mitigation:** field is OPTIONAL by CR-FM-01; default `STANDARD` resolves missing values at Gate 1 by CR-TASK-02; documentation explicitly tells the reader no migration is needed. Additional **risk: silent behavior shift** if `STANDARD` profile semantics drift from the pre-refactor `/task` baseline (e.g., if "existing budget" is reinterpreted to mean something tighter post-refactor). **Mitigation:** STANDARD profile is defined in CR-TASK-02 as "existing budget profile: F1 + Phase-Gate QA (existing budget) + Post-Completion Validation" — i.e., the pre-refactor behavior is the explicit `STANDARD` definition. Phase 7 must `diff` pre/post-refactor Phase-Gate QA budgets to confirm `STANDARD` is unchanged from baseline. Additional **risk: re-classifying existing tasks** (e.g., post-hoc adding `Tier: STRICT` to a `TASK-PRD-*` directory mid-execution). **Mitigation:** the schema is task-file-author scoped — adding the field is a deliberate authoring act, not an automatic upgrade. CR-FM-03 explicitly states no migration is performed. |

### CR-FM-04 — Closed-enum validator placement audit (cross-cuts CR-FM-01..03)

| Column | Value |
|---|---|
| **CR-ID** | CR-FM-04 |
| **File path (side-tagged)** | (audit step, no schema edit) — verifies the closed-enum validator authored by CR-TASK-02 is the **single source of truth** for the `Tier:` and `(Tier: ...)` value set, and that CR-FM-03's compat shim resolves to `STANDARD` for every existing TASK-* file. |
| **Change** | (no schema edit) — Phase 7 audit step. Run two checks: (a) `grep -nE "STRICT\|STANDARD\|LIGHT\|EXEMPT" [src] src/superclaude/skills/task/SKILL.md` — every match must be the closed-enum constant authored once by CR-TASK-02, never a paraphrase or partial subset. (b) Spot-check N=5 existing `.dev/tasks/to-do/TASK-*/` files (one each from `TASK-PRD-*`, `TASK-E2E-*`, `TASK-RESEARCH-*`, `TASK-RF-*`, `TASK-SKILL-*` if present) and confirm their frontmatter has NO `Tier:` field and they validate clean under the post-refactor validator with `gate-1: ... source=default` emitted. |
| **Manifest feature(s)** | INV-04 enforcement audit; cross-row guard against silent closed-enum drift between CR-FM-01 (task-level field) and CR-FM-02 (inline marker). R-RULE-11 audit against LR-DEFER-4 / LR-DEFER-5 / LR-REJECT-3 re-proposal vectors. |
| **Priority** | **P3** — audit step, runs at Phase 7 commit time after CR-FM-01..03 + CR-TASK-01..12 land. |
| **Effort** | **XS** — one `grep` invocation + five `head` reads of existing TASK-* frontmatter. |
| **Dependencies** | CR-FM-01, CR-FM-02, CR-FM-03, CR-TASK-02, CR-TASK-03 (the rows whose output is being audited). |
| **Acceptance criteria** | (1) Closed-enum set appears in `[src] src/superclaude/skills/task/SKILL.md` exactly where CR-TASK-02 + CR-FM-02 author it (task-level validator + inline-marker parser); no duplicate paraphrase appears elsewhere in the file. (2) The five spot-checked existing TASK-* files validate clean post-refactor with `gate-1: dispatch_profile=STANDARD source=default` emitted at task entry. (3) No spot-checked existing TASK-* file is modified by this audit — files are read-only. (4) The audit log records the five spot-check file paths and their pre-audit and post-validation status (status frontmatter field unchanged). |
| **Risk assessment** | **INV protected: INV-04 (resumability)** + **R-RULE-11 enforcement**. The audit catches three failure modes: (a) closed-enum drift between task-level and per-item parser (CR-FM-01 vs CR-FM-02 inconsistency); (b) silent migration attempts that touch existing TASK-* file frontmatter (INV-04 breach by a misguided "helper" backfill); (c) LR-DEFER-4 / LR-DEFER-5 re-proposal by unauthorized adjacent schema additions (`allowed-tools:`, classification headers) creeping into the same merge as `Tier:`. **Mitigation by structure:** the audit is the cross-row enforcement gate; any failure blocks the Phase 7 commit until the offending row is corrected. The audit's read-only design guarantees it cannot itself breach INV-04. |

---

## 3. Schema roll-up

### 3.1 Field manifest (single new optional field)

| Field name | Type | Cardinality | Value set | Default | Source TU |
|---|---|---|---|---|---|
| `Tier:` | string | optional | `STRICT` \| `STANDARD` \| `LIGHT` \| `EXEMPT` | `STANDARD` (resolved at Gate 1) | TU-1 (donor D09a) |

**Total new MDTM frontmatter fields: 1** (matches manifest § 2 TU-1 "New field / hook: `Tier:` frontmatter field (only new field introduced by this sprint)"). No other TU introduces a frontmatter field.

### 3.2 Inline-marker schema (companion to the field)

| Marker syntax | Position | Cardinality | Value set | Fallback chain | Source TU |
|---|---|---|---|---|---|
| `(Tier: <value>)` | immediately AFTER `- [ ]`/`- [x]` and BEFORE item text | optional per-item | same closed-enum as task-level | per-item marker → task-level `Tier:` → `STANDARD` default | TU-1 (manifest § 2 Integration sketch) |

**Total new inline-marker schemas: 1**.

### 3.3 Backward-compat treatment matrix (INV-04 enforcement)

| Existing task-file state | Post-refactor behavior | Migration required? | Source CR |
|---|---|---|---|
| Task file has NO `Tier:` field, NO inline markers | Validates clean. Gate 1 emits `dispatch_profile=STANDARD source=default`. Execution profile = pre-refactor `STANDARD` (existing budget). | **No** | CR-FM-03 |
| Task file has NO `Tier:` field, items have `(Tier: ...)` inline markers | Validates clean. Gate 1 emits `dispatch_profile=STANDARD source=default`. Per-item markers apply tier-conditioned READ checks (e.g., CR-TASK-07 baseline-skip per-item) but do NOT re-fire Gate 1. | **No** | CR-FM-02 + CR-FM-03 |
| Task file has `Tier:` field with a valid enum value (added by author of new task) | Validates clean. Gate 1 emits `dispatch_profile=<value> source=tier-field`. Execution profile reflects the field. | **No** (new tasks only) | CR-FM-01 |
| Task file has `Tier:` field with a NON-enum value (typo, e.g., `Tier: AGGRESSIVE`) | Validation REJECTs the file with a refusal diagnostic naming the closed-enum set. Task entry HALTS cleanly (pre-loop, not mid-F1). Author corrects the value before resuming. | **No migration; corrective edit on the affected file only.** | CR-FM-01 + CR-FM-04 |
| Task file has a path-override-eligible target path AND no `Tier:` field (e.g., a task touching `auth/` with no `Tier:`) | `path_override_check` (CR-TASK-01) sets `forced_stance=STRICT` based on path glob; Gate 1 dispatches STRICT profile; Task Log emits `dispatch_profile=STRICT source=path-override`. Existing files automatically benefit from STRICT escalation on critical paths even without a `Tier:` field. | **No** (safer-by-default behavior; CR-TASK-01 path-override is path-keyed, not field-keyed) | CR-TASK-01 + CR-FM-03 |

**Every existing `.dev/tasks/to-do/TASK-*/` task file remains valid and resumable without modification.** INV-04 (resumability) is preserved by design.

### 3.4 Non-additions (R-RULE-11 cross-check against deferred/rejected schema)

Schema fields that this refactor explicitly does **NOT** add:

| Proposed field | Source | Why not added in this refactor |
|---|---|---|
| `mcp-servers:` | LR-REJECT-1 (D02/Layer A, ME-9 re-affirmed) | R-RULE-06 ceremony-without-teeth — no in-repo consumer; reaffirmed REJECT in manifest § 3. Not added here; donor-side advertisement removed by T06.03 / CS-M4-A. |
| `allowed-tools:` | LR-DEFER-4 (D01, ME-8) | Two-clause precondition unmet (loader honor-semantics + R-RULE-06 split). Not added here. ME-8 binds. |
| `## Classification: <tier>` (in-body section header, not frontmatter) | LR-DEFER-5 (D08, ME-7) | Parser-ships precondition unmet. Not added here. ME-7 binds. |
| `Strategy:`, `Persona:`, `Auto-trigger:` | LR-REJECT-5 / LR-REJECT-6 / LR-REJECT-8 / LR-REJECT-9 (D03/D04/D06/D13) | Terminal REJECTs in ledger; structural mismatch with `/task`'s Skill-invoked-on-a-file-path model. Not added here. |
| `--strict` / `--explain` / similar override flags as frontmatter | LR-REJECT-4 (Gate 5 Override flags) | Silent-misuse failure mode; path-override (CR-TASK-01) is path-keyed not flag-keyed. Not added here. |
| `tier-budget:` / `tier-roster:` / external YAML config refs | LR-DEFER-9 (D32) | Not in scope for this sprint; `/task` does not read external YAML in CR-TASK-01..12. Not added here. |
| `Failure Remediation Plan` heading inserted into task file | LR-DEFER-6 (D23 Step 5) | F4 violation at TU-8's attach surface; incident reporting writes a side-effect FILE (CR-TASK-10), never an in-task heading. Not added here. |

**Total non-additions verified: 7 classes** — every deferred/rejected schema field that could plausibly be silently bundled into this refactor is explicitly excluded. R-RULE-11 holds.

---

## 4. Dependency graph (frontmatter level)

```text
                TU-1 SHIP-TOGETHER ATOMIC MERGE
        ┌───────────────────────────────────────────────┐
        │                                               │
        │   CR-FM-01 ◄────────── CR-FM-02              │
        │  (Tier: field        (inline marker          │
        │   schema)             grammar; shares         │
        │     │                 closed-enum)            │
        │     │                                         │
        │     ▼                                         │
        │   CR-FM-03 (compat default for existing       │
        │           TASK-* files — INV-04 floor)        │
        │                                               │
        └───────────────────────┬───────────────────────┘
                                │
                                ▼
                ┌───────────────────────────────────────┐
                │ CR-FM-04 (closed-enum + compat audit  │
                │           at Phase 7 commit time)     │
                └───────────────────────────────────────┘
```

**Cross-refactor dependency edges (to `refactor-task-skill.md`):**

| From → To | Edge type | Rationale |
|---|---|---|
| CR-FM-01 → CR-TASK-02 | schema-to-validator | The closed-enum field defined here is parsed by the validator. |
| CR-FM-02 → CR-TASK-03 | schema-to-parser | The inline marker grammar defined here is read by F1 EXECUTE. |
| CR-FM-03 → CR-TASK-02 | compat-to-default-resolver | Gate 1's default `STANDARD` resolution honors this row's INV-04 commitment. |
| CR-FM-04 → CR-TASK-01..12 | audit-cross-row | Verifies post-merge that no closed-enum drift, migration attempt, or unauthorized schema addition crept in. |

**Acyclicity confirmed.** Topological order: CR-FM-01 ≡ CR-FM-02 ≡ CR-FM-03 (atomic with TU-1 merge) → CR-FM-04 (audit, runs last with CR-TASK-12).

---

## 5. Acceptance Criteria recap (T06.02, frontmatter half)

1. **`refactor-mdtm-frontmatter.md` exists; every change row has file path, change, manifest-feature ref, priority, effort, dependencies, acceptance criteria, risk assessment.** ✅ — Four rows (CR-FM-01..04), eight columns each (§ 1 + § 2).
2. **Every MDTM frontmatter addition specifies the backward-compat behavior for existing `TASK-*` files (INV-04).** ✅ — CR-FM-03 is the dedicated compat-shim row; § 3.3 enumerates the full compat treatment matrix (five existing-task-state rows, all "No migration required"). The five spot-check categories named in CR-FM-04 cover the observed populations under `.dev/tasks/to-do/`.
3. **Every risk assessment names the INV-NN at risk and its mitigation.** ✅ — Four risk-assessment cells reference at least one of INV-01, INV-04, INV-05 and the bound ME (ME-1, ME-3 spirit, ME-6) that constrains the shape.
4. **Every file path is auggie-verified and side-tagged.** ✅ — `[src] src/superclaude/skills/task/SKILL.md` is verified present per `merge-roadmap.md` § 1 row 1 (32951 B). The existing TASK-* directory population is verified present per merge-roadmap § 1 row 13 (multiple TASK-* dirs observed). No fictitious paths are referenced.

**T06.02 (refactor-mdtm-frontmatter.md) deliverable: COMPLETE.** Phase 7 has the full MDTM schema delta (1 new optional field + 1 inline-marker grammar) with an explicit, evidence-backed INV-04 compat treatment that guarantees every existing `.dev/tasks/to-do/TASK-*/` file remains valid and resumable without modification.
