# Refactor Plan — `/task` Skill Edits (Phase 6 / T06.02)

**Task:** T06.02 — Refactor plans: `/task` skill edits & MDTM frontmatter extensions
**Roadmap Item:** R-020
**Tier:** STRICT
**Generated:** 2026-05-15
**Status:** Driving input for Phase 7 execution. Every change row is an eight-column directive that Phase 7 will translate into a concrete edit against `[src] src/superclaude/skills/task/SKILL.md`, with `[.claude]` refreshed by `make sync-dev`.

**Inputs (1:1 referenced):**
- `transfer-manifest.md` (T05.03) — TU-1..TU-8, ME-1..ME-9, R-RULE-06 / R-RULE-10 / R-RULE-11 governing principles.
- `merge-roadmap.md` (T06.01) — CS-M1-A..CS-M3-D macro-level change-sets, dependency graph, side-tagged path verification table.
- `extension-point-contracts.md` (T03.02) — extension-point rows 1, 2, 4, 8, 10, 11, 13 (the seven `/task` SKILL.md attach surfaces this refactor touches).
- `[src] src/superclaude/skills/task/SKILL.md` (recipient attach target; **byte-identical** to `[.claude] .claude/skills/task/SKILL.md` per CP-P05-END drift audit).

**Companion artifact:** `refactor-mdtm-frontmatter.md` — covers the one new MDTM frontmatter field (`Tier:`) and the per-item inline marker schema introduced by TU-1, including the INV-04 backward-compat treatment for existing `.dev/tasks/to-do/TASK-*/` files.

**Scope boundary (R-RULE-06 + R-RULE-11):**
- This refactor absorbs *control patterns* from the manifest TUs only. It does **NOT** re-propose any `rejected-features-ledger.md` entry (cross-checked in § 4).
- This refactor only edits the `/task` skill package. The `/sc:task` deprecation, donor-reference enumeration, distribution surface, and documentation are out of scope (covered by T06.03 / T06.04).
- Donor ceremony explicitly dropped by the manifest (D09b classifier, D15c per-tier procedure synthesis, D23 step 5/6 heading-insert and resume-from-inserted, D25 3-strike FULL STOP, donor verifier-replacement semantics, donor F1-halting TFEP) is **not** carried into any change row.

---

## 0. Side-tagging convention (R-RULE-10)

Every operative file path below is tagged `[src]` (source of truth — `src/superclaude/...`) or `[.claude]` (dev-copy mirror — `.claude/...`). Phase 7 must edit `[src]` first, then run `make sync-dev` to refresh `[.claude]`. `make verify-sync` must return 0 before commit. T06.01 confirmed **zero byte-level drift** between the two sides on every path this refactor touches.

**Single recipient attach target:** `[src] src/superclaude/skills/task/SKILL.md` (32951 B at T06.01 verification). The `[.claude]` mirror is refreshed by sync, never edited directly.

---

## 1. Column legend

Every change row below carries the eight columns required by T06.02 acceptance criterion #1:

| Column | Meaning |
|---|---|
| **CR-ID** | Stable change-row identifier (`CR-TASK-NN`) for cross-reference from `merge-master.md` and Phase 7 commits. |
| **File path (side-tagged)** | `[src]` path (the merge target) + line-anchor description from SKILL.md. The `[.claude]` mirror is implicit (`make sync-dev` refreshes it). |
| **Change** | The edit operation: `edit-in-place` (modify an existing block) / `add hook` (insert a new block at the extension point) / `add new section` / `add field-validator` / `add side-channel hook`. |
| **Manifest feature(s)** | The TU-N / ME-N / donor row(s) the change implements (one-to-many traceability per acceptance #1). |
| **Priority (P0–P3)** | P0 = ship-together foundation (blocks every other row); P1 = directly depends on P0; P2 = tier-conditioned behavior layered on P0+P1; P3 = post-completion / sync mechanics. |
| **Effort (XS–XL)** | Approximate edit size: XS ≤ 5 lines, S ≤ 15, M ≤ 30, L ≤ 60, XL > 60. Manifest "shape of change" lines inform the estimate. |
| **Dependencies** | Build-order edges (other CR-TASK-NN rows that must land first). Ship-together obligations carry both directions. |
| **Acceptance criteria** | Observable post-condition — the Task Log line, file presence, or schema-validated value Phase 7 verifies before marking the row done. Matches the manifest's "Observable post-condition" entries verbatim where possible. |
| **Risk assessment** | The INV-NN (and/or ME-NN) the change could violate if applied wrong, plus the named mitigation — i.e., the bound manifest exception that constrains the implementation to the safe shape. |

---

## 2. Change rows — `/task` SKILL.md edits

Twelve change rows (CR-TASK-01..CR-TASK-12). Order follows the merge-roadmap milestone partition; M1 ships atomically (CR-TASK-01..04), M2 layers on top (CR-TASK-05..06), M3 follows the TFEP internal ordering (CR-TASK-07..10), and CR-TASK-11..12 are the sync-and-validate mechanics.

### CR-TASK-01 — Insert `path_override_check` at Task File Validation gate (row 1, fires FIRST)

| Column | Value |
|---|---|
| **CR-ID** | CR-TASK-01 |
| **File path (side-tagged)** | `[src] src/superclaude/skills/task/SKILL.md` — *Validating the Task File* section (lines 65–73, "### Validating the Task File" through bullet-list end). Insert immediately after the existing four-bullet validation list, BEFORE any new tier-field-validate step. |
| **Change** | `add hook` — new pure-read function `path_override_check(task_target_paths) → forced_stance ∈ {STRICT, LIGHT, none}`. Critical path-glob set (`auth/`, `security/`, `crypto/`, `models/`, `migrations/`) and trivial path-glob set (`*.md`, `docs/`, `*test*.py`) sourced **verbatim** from `[src] src/superclaude/skills/sc-task-protocol/SKILL.md:121` and `:123` and inlined — no runtime dependency on the donor file after merge. |
| **Manifest feature(s)** | TU-2 (Critical/Trivial Path Override) + IS-ADOPT-1; donor rows D17 + D18; stack-rank row 1 (Net=20.0, highest-scored feature in the sprint). CR-7 runtime-ordering obligation: `path_override_check → tier_field_validate → gate_1_dispatch` at row 1. |
| **Priority** | **P0** — ship-together with CR-TASK-02 atomically (ME-6 + CR-7). Runtime ordering MUST hold from the first deployment. |
| **Effort** | **S** (~10 lines per manifest TU-2 "Shape of change"). |
| **Dependencies** | None upstream. Ship-together with CR-TASK-02 (CR-TASK-01 must fire BEFORE CR-TASK-02's validator/dispatcher at row 1). |
| **Acceptance criteria** | Task Log line `path-override: forced_stance=STRICT (matched: <path-glob>)` OR `path-override: forced_stance=LIGHT (all paths inside trivial-glob set)` OR `path-override: no-match (forced_stance=none)` is emitted once at task entry, BEFORE any tier-field-validate or gate-1-dispatch line. The flag is read by CR-TASK-02 (Gate 1) and CR-TASK-05 (Gate 2). |
| **Risk assessment** | **INV at risk: INV-01 (loop control integrity)** + **CR-7 / CR-8 (runtime integration order)**. If the override fires AFTER Gate 1 or AFTER Gate 2's stance-select, the wrong-stance dispatch window the override exists to close re-opens. **Mitigation:** ordering is enforced **in the inserted code text itself** — the validator block reads top-to-bottom `path_override_check → tier_field_validate → gate_1_dispatch`. CR-TASK-02's validator MUST consume the flag set by this row, never re-derive it. **ME-NN bound:** none direct on TU-2; CR-7 / CR-8 are load-bearing. |

### CR-TASK-02 — Add `Tier:` closed-enum validator + Gate 1 dispatch block (PRE-LOOP ONLY)

| Column | Value |
|---|---|
| **CR-ID** | CR-TASK-02 |
| **File path (side-tagged)** | `[src] src/superclaude/skills/task/SKILL.md` — *Validating the Task File* section (lines 65–73). Insert AFTER the CR-TASK-01 `path_override_check` block: a closed-enum validator for the new optional `Tier:` frontmatter field, then a Gate 1 dispatch block that fires **once at task entry**. |
| **Change** | `add field-validator` (closed-enum check on the new `Tier:` field, malformed → refusal diagnostic) + `add hook` `gate_1_dispatch(forced_stance, tier_value) → execution_profile`. Dispatch logic: `LIGHT`/`EXEMPT` → lightweight profile (skip TFEP baseline TU-5, skip D15b pre-flight TU-4, reduced Phase-Gate QA budget; Post-Completion Validation STILL FIRES per INV-03 floor); `STANDARD` → existing profile; `STRICT` → full profile (D15b pre-flight + TFEP baseline + widened Phase-Gate QA + TFEP incident-report Post-Completion check). |
| **Manifest feature(s)** | TU-1 (Tier field + Gate 1 dispatch — ship-together unit) + IS-ADOPT-3 + IS-ADOPT-6; donor rows D04 cluster + D09a + D10 (donor-traceability, command-side dispatch absorbed at the recipient's validation surface); stack-rank rows 3 + 6 + 7. Extension-point rows touched: 13 (frontmatter schema slot) + 1 (Task File Validation gate) + 4 (F1 EXECUTE per-item read — implemented in CR-TASK-03). |
| **Priority** | **P0** — foundation; every CR-TASK-NN that consumes `Tier:` or `execution_profile` depends on this row. |
| **Effort** | **M** (~5 lines frontmatter schema text in *Validating the Task File* + ~5–10 lines closed-enum validator + ~10–15 lines Gate 1 dispatch block = ~20–30 lines aggregate per manifest TU-1 "Shape of change"). |
| **Dependencies** | CR-TASK-01 (must fire FIRST at row 1 — Gate 1 reads `forced_stance` set by the path-override-check). CR-TASK-01 ↔ CR-TASK-02 is a ship-together atomic merge (ME-6 + CR-7). |
| **Acceptance criteria** | (1) Closed-enum validator rejects any `Tier:` value outside `{STRICT, STANDARD, LIGHT, EXEMPT}` with a refusal diagnostic. (2) Single Task Log line `gate-1: dispatch_profile=<STRICT\|STANDARD\|LIGHT\|EXEMPT> source=<path-override\|tier-field\|default>` is emitted once at task entry, **never again per-item**. (3) STRICT-only side-effect files (`research/test-baseline.yaml` from CR-TASK-07, `research/tfep-incident-report.md` from CR-TASK-10) appear if and only if STRICT profile dispatched. |
| **Risk assessment** | **INV at risk: INV-01 (loop control)** if dispatch fires per-item inside F1 EXECUTE instead of pre-loop — Gate 1 would re-evaluate loop control each iteration. **Mitigation: ME-1 (PRE-LOOP DISPATCH ONLY)** — Gate 1 fires once at task-entry, never per-item. Per-item per-tier dispatch is auto-REJECT under INV-01. Additional **risk: ME-6 violation** if D09a (frontmatter field) ships without Gate 1 or vice versa — D09a alone is inert metadata; Gate 1 alone has nothing to dispatch on. **Mitigation: ship-together with CR-TASK-01 + CR-TASK-03 in the same merge.** Additional risk: re-introducing donor classifier (D09b, ledger row 21, LR-REJECT-3) by deriving `Tier:` at runtime — **mitigation:** `Tier:` arrives declaratively via frontmatter only; no runtime classifier authored in this row. |

### CR-TASK-03 — Add per-item `Tier:` annotation read in F1 EXECUTE

| Column | Value |
|---|---|
| **CR-ID** | CR-TASK-03 |
| **File path (side-tagged)** | `[src] src/superclaude/skills/task/SKILL.md` — *F1 Execution Loop — EXECUTE step* (lines 89–96, the "If the item says to..." dispatch list inside step 3 EXECUTE). Add a per-item inline-marker read at the top of the EXECUTE step. |
| **Change** | `edit-in-place` — extend the EXECUTE step (~3 lines) to read an optional per-item inline marker `(Tier: LIGHT)` / `(Tier: STRICT)` / `(Tier: EXEMPT)` / `(Tier: STANDARD)` immediately after the item's `- [ ]` prefix. If present, the per-item marker overrides the task-level `Tier:` for that item only **for tier-conditioned read-only checks** (e.g., CR-TASK-07 baseline skip decision applied per-item). It does **NOT** re-fire Gate 1 dispatch (ME-1: PRE-LOOP DISPATCH ONLY remains binding); the execution profile is already set by CR-TASK-02 and is not re-evaluated. |
| **Manifest feature(s)** | TU-1 (per-item annotation supported as inline marker, task-level value is the fallback) — extension-point row 4 (F1 EXECUTE item-type dispatch). |
| **Priority** | **P0** — ships in the same merge as CR-TASK-01 / CR-TASK-02 (the TU-1 unit). |
| **Effort** | **XS** (~3 lines per manifest TU-1 "Shape of change"). |
| **Dependencies** | CR-TASK-02 (consumes the closed-enum `Tier:` semantic and the task-level fallback). Atomic ship-together with CR-TASK-01 + CR-TASK-02. |
| **Acceptance criteria** | A checklist item written as `- [ ] (Tier: LIGHT) trivial doc-typo fix` is read by EXECUTE with `tier_value=LIGHT` for that item's tier-conditioned read-only checks; missing inline marker → fall back to task-level `Tier:`. The per-item marker NEVER triggers a new Gate 1 dispatch line. The task-level Gate 1 line emitted at task-entry remains the canonical execution-profile record. |
| **Risk assessment** | **INV at risk: INV-01** if the per-item marker is allowed to re-fire Gate 1 dispatch mid-loop. **Mitigation: ME-1 (PRE-LOOP DISPATCH ONLY)** explicitly binds Gate 1 to task-entry; per-item markers are a tier-conditioned READ for behaviors already gated (e.g., TFEP baseline collection skip), not a re-dispatch. Additional risk: drift from CR-TASK-02's closed-enum if the inline-marker parser accepts values the task-level validator rejects — **mitigation:** the inline-marker parser uses the same closed-enum set authored once for CR-TASK-02. |

### CR-TASK-04 — Insert `path_override_check` consumption at Phase-Gate QA Verification (row 10)

| Column | Value |
|---|---|
| **CR-ID** | CR-TASK-04 |
| **File path (side-tagged)** | `[src] src/superclaude/skills/task/SKILL.md` — *Phase-Gate QA Verification* section (lines 182–211). Insert the override-flag read at the top of the "Spawn rf-qa" step (around line 191), BEFORE any tier-based budget/roster selection added by CR-TASK-05. |
| **Change** | `edit-in-place` — Gate 2 stance-select reads the `forced_stance` flag set by CR-TASK-01 FIRST (CR-8). If `forced_stance=STRICT`, STRICT profile applies regardless of `Tier:`. If `forced_stance=LIGHT`, LIGHT profile applies. If `forced_stance=none`, fall through to the tier-based mapping authored by CR-TASK-05. |
| **Manifest feature(s)** | TU-2 (Critical/Trivial Path Override) — extension-point row 10 (Phase-Gate QA Verification). CR-8 runtime-ordering obligation. |
| **Priority** | **P0** — ships in the M1 atomic merge with CR-TASK-01 so the row-10 runtime integration order locks together. |
| **Effort** | **XS** (~5 lines per manifest TU-2 "Shape of change at row 10"). |
| **Dependencies** | CR-TASK-01 (consumes its `forced_stance` flag). CR-TASK-05 layers ON TOP of this read at row 10 (CR-TASK-05 is M2 and depends on this row's hook landing first). |
| **Acceptance criteria** | Phase-Gate QA report at `${TASK_DIR}reviews/qa-phase-[N]-report.md` includes a leading line indicating which axis selected the profile: `qa-stance-source: path-override` (when `forced_stance ≠ none`) OR `qa-stance-source: tier-field` (when CR-TASK-05's mapping applied) OR `qa-stance-source: default`. STRICT-by-path-override items receive the STRICT profile (5K/60s + roster widening) even when `Tier:` is STANDARD/LIGHT/EXEMPT. |
| **Risk assessment** | **INV at risk: INV-03 (rf-qa adversarial-stance floor)** + **CR-8 (runtime ordering at row 10)**. If Gate 2 reads `Tier:` first and ignores `forced_stance`, the override loses its row-10 teeth. **Mitigation: CR-8 baked into the inserted code text** — `path_override_check → gate_2_stance_select` is the read order; CR-TASK-05 will see the flag already-consumed and only fires for `forced_stance=none`. Additional risk: replacing `rf-qa` (ME-2 violation) by allowing the override to silently swap verifiers — **mitigation:** this row does NOT touch verifier identity; only profile selection. Verifier identity is the property of CR-TASK-05 alone (and CR-TASK-05 supplements, never replaces, per ME-2). |

### CR-TASK-05 — Phase-Gate QA tier-conditional budget + roster widening (ADAPT)

| Column | Value |
|---|---|
| **CR-ID** | CR-TASK-05 |
| **File path (side-tagged)** | `[src] src/superclaude/skills/task/SKILL.md` — *Phase-Gate QA Verification* section (lines 182–211). Insert ~25 lines tier→budget+roster mapping, immediately after the CR-TASK-04 override-flag read inside the "Spawn rf-qa" step. |
| **Change** | `edit-in-place` — inline a tier→{budget, timeout, roster} mapping into the existing Phase-Gate QA section (NOT a separate "verification routing table" — that donor framing is dropped, R-RULE-06). Mapping: **STRICT** → ~5K token budget, 60s timeout, roster = `[rf-qa, quality-engineer]` (`quality-engineer` is *additional*, not a replacement — ME-2). **STANDARD** → existing budget, roster = `[rf-qa]`. **LIGHT / EXEMPT** → ~1.5K budget, 20s timeout, roster = `[rf-qa]`. |
| **Manifest feature(s)** | TU-3 (Gate 2 Verification routing widening — ADAPT); donor cluster Gate 2 + D15a (donor-traceability) + D16 (catalog row 34, ADAPTABLE-subsumed); stack-rank rows 10 + 11. Extension-point row 10. |
| **Priority** | **P1** — depends on M1 (CR-TASK-02 for `Tier:`, CR-TASK-01/04 for `forced_stance`). |
| **Effort** | **M** (~25 lines per manifest TU-3 "Shape of change"). |
| **Dependencies** | CR-TASK-02 (consumes `Tier:` value); CR-TASK-01 + CR-TASK-04 (consumes `forced_stance` flag from the row-10 read inserted by CR-TASK-04). |
| **Acceptance criteria** | (1) Phase-Gate QA report includes `verifier_roster: [rf-qa, quality-engineer]` for STRICT (or path-override-STRICT) items; `verifier_roster: [rf-qa]` otherwise. (2) Report includes a `budget: <tokens>/<timeout>` line matching the tier mapping. (3) Task Log line `gate-2: profile=<STRICT\|STANDARD\|LIGHT\|EXEMPT> budget=<n>/<s> roster=[...]` emitted once per phase-gate. (4) `rf-qa` is **always** in the roster — `quality-engineer` only adds, never replaces. |
| **Risk assessment** | **INV at risk: INV-03 (rf-qa adversarial-stance floor)**. If a future variant of this row substitutes `quality-engineer` for `rf-qa` on STRICT (donor's verifier-replacement semantic), the adversarial floor collapses. **Mitigation: ME-2 (`rf-qa` SUPPLEMENTED NOT REPLACED)** — `quality-engineer` is *additional* on STRICT; replacing `rf-qa`'s adversarial stance is auto-REJECT under INV-03. The inserted mapping authors `roster: [rf-qa, quality-engineer]` literally (rf-qa first, additive comma); future edits that drop `rf-qa` from a STRICT roster row are an ME-2 violation. Additional risk: re-importing donor's standalone "verification routing table" as a separate config artifact — **mitigation:** mapping is inlined into the existing Phase-Gate QA section, no new standalone artifact authored (R-RULE-06 ceremony drop). |

### CR-TASK-06 — First Item Protocol tier-gated pre-flight scaffolding (ADAPT, D15b only)

| Column | Value |
|---|---|
| **CR-ID** | CR-TASK-06 |
| **File path (side-tagged)** | `[src] src/superclaude/skills/task/SKILL.md` — *First Item Protocol* section (lines 100–102, currently a single paragraph). Expand to ~15–25 lines with a tier-gated pre-loop pre-flight block inserted between the existing status-update paragraph and the prelude to F2 (line 104). |
| **Change** | `add new section` — *Pre-loop pre-flight* block, tier-gated and **additive pre-loop setup only**, NEVER per-item, NEVER inside F1 EXECUTE. **STRICT** (or `forced_stance=STRICT`): `serena_activate_if_available` → `git_status_clean_tree_check` → `codebase_retrieval_on_relevant_code_if_available` → `list_memories_read_memory_for_relevant_prior_context`. **STANDARD**: `codebase_retrieval_on_relevant_code_if_available` only. **LIGHT / EXEMPT**: skipped entirely. Each step conditional on tool availability; graceful skip on unavailability (`serena` / `codebase-retrieval` are MCP-dependent). |
| **Manifest feature(s)** | TU-4 (D15b Layer 2 pre-flight scaffolding — ADAPT); donor row D15 split → D15b only (D15c REJECTed via ledger row 26 / LR-REJECT-7); stack-rank row 12. Extension-point row 2. |
| **Priority** | **P1** — depends on M1 (consumes `Tier:` + Gate 1 dispatch). |
| **Effort** | **M** (~15–25 lines per manifest TU-4 "Shape of change"). |
| **Dependencies** | CR-TASK-02 (consumes `Tier:` + Gate 1 dispatch); CR-TASK-01 (consumes `forced_stance` for forced-STRICT promotion). |
| **Acceptance criteria** | Task Log line `gate-1.5: pre-flight tier=<STRICT\|STANDARD> ran=[serena, git, codebase-retrieval, memory]` (STRICT) OR `ran=[codebase-retrieval]` (STANDARD) OR `ran=[]` (LIGHT/EXEMPT) emitted once before the first F1 iteration. On tool-unavailability: `skipped=[<tool>: not-available]` recorded for the unavailable tool, and the loop continues. The pre-flight block does **NOT** create any new checklist items (INV-05 floor). |
| **Risk assessment** | **INV at risk: INV-01 (loop control) + INV-05 (items must come from disk read, not runtime synthesis)** if a future variant synthesizes pre-flight steps as runtime checklist items inside F1 EXECUTE (donor D15c pattern). **Mitigation: ME-5 (NO PER-ITEM EXECUTE SUBSTITUTION)** — pre-flight is additive pre-loop setup; D15c-style synthesis is auto-REJECT. The inserted section is anchored under *First Item Protocol* (before F1 starts), never inside *F1 Execution Loop*. Additional risk: re-importing donor's "Layer 2" framing as a named runtime artifact — **mitigation:** steps inlined as setup actions, no named layer authored (R-RULE-06 ceremony drop). Additional risk: re-proposing D15c on a future pass — explicitly blocked by ledger LR-REJECT-7 (R-RULE-11). |

### CR-TASK-07 — First Item Protocol tier-gated TFEP baseline snapshot (TU-5)

| Column | Value |
|---|---|
| **CR-ID** | CR-TASK-07 |
| **File path (side-tagged)** | `[src] src/superclaude/skills/task/SKILL.md` — *First Item Protocol* section (lines 100–102, co-attached with CR-TASK-06). Insert ~15 lines for baseline collection AFTER the CR-TASK-06 pre-flight block. |
| **Change** | `add new section` — *Pre-loop TFEP baseline* block, tier-gated to STRICT/STANDARD only (ME-4). Before F1's first iteration: run `uv run pytest --collect-only -q` to enumerate test IDs, then `uv run pytest --tb=no -q` (or equivalent) to capture each test ID's PASS/FAIL state. Persist to `${TASK_DIR}research/test-baseline.yaml` — YAML schema is a list of `{test_id, status}` records. **LIGHT / EXEMPT** profile: skip baseline collection entirely (uniform-cost-without-uniform-value floor). |
| **Manifest feature(s)** | TU-5 (TFEP Test baseline snapshot — ADOPT); donor row D21; stack-rank row 8. Extension-point row 2. |
| **Priority** | **P2** — depends on M1 (for `Tier:` gating) and recommended-order after CR-TASK-06 (so serena/codebase-retrieval are warm before baseline collection per DM-7 recommended-order). |
| **Effort** | **M** (~15 lines per manifest TU-5 "Shape of change"). |
| **Dependencies** | CR-TASK-02 (consumes `Tier:` for the tier-gate); CR-TASK-06 (recommended runs first at row 2 so MCP tools are warm). |
| **Acceptance criteria** | File `${TASK_DIR}research/test-baseline.yaml` exists on disk for STRICT/STANDARD tasks BEFORE F1's first iteration. The YAML lists every collected test ID with a `status: PASS\|FAIL` field. For LIGHT/EXEMPT tasks, the file is **absent** (skip is silent — verified by file-not-present). Task Log line `gate-1.6: tfep-baseline tier=<STRICT\|STANDARD> tests_collected=<N> baseline_file=research/test-baseline.yaml` (or `skipped` for LIGHT/EXEMPT). |
| **Risk assessment** | **Risk: ME-4 violation** if a future variant runs baseline collection on every task regardless of tier. The uniform-baseline-on-every-task variant falls cost on LIGHT typo fixes for zero TFEP value. **Mitigation: ME-4 (BASELINE TIER-GATED to STRICT/STANDARD)** — auto-REJECT for uniform variants. Additional **risk: INV-04 (resumability)** if the baseline file is written non-atomically and a mid-collection session restart leaves a partial YAML on disk that confuses CR-TASK-09 (escalation classifier). **Mitigation:** write the baseline file via the Incremental Writing Protocol (Critical Rule #2 of SKILL.md, lines 252–263, ZERO TOLERANCE) — Write the file header first, then Edit each `{test_id, status}` block in. Mid-restart resumption reads any complete records; an incomplete record at end-of-file is detected by the YAML parser and the baseline collection re-runs (LIGHT/STANDARD/STRICT idempotent). |

### CR-TASK-08 — Error Handling TFEP Prohibitions + Carve-outs (D19 + D20)

| Column | Value |
|---|---|
| **CR-ID** | CR-TASK-08 |
| **File path (side-tagged)** | `[src] src/superclaude/skills/task/SKILL.md` — *Error Handling* section (lines 170–179). Insert ~15 + ~10 lines forming a *TFEP Prohibitions (D19)* block and a nested *TFEP Carve-outs (D20)* block, AFTER the existing 4-bullet error-handling list. |
| **Change** | `add side-channel hook` — new pure-decision function `tfep_prohibition_check(blocker_type) → {allow, refuse}` fires when a blocker is classified as a test failure. Three VIOLATION strings (`VIOLATION-1` ad-hoc test fix without root cause; `VIOLATION-2` modify test expectations without adversarial validation; `VIOLATION-3` one-shot patch from test output alone) sourced **verbatim** from `[src] src/superclaude/skills/sc-task-protocol/SKILL.md:127–135` and inlined. Three D20 carve-outs (single ImportError/NameError in agent-authored scaffolding ≤2 tests, lint/format failures, deprecation warnings) sourced **verbatim** from `:137–140`. On carve-out match → return `allow`; F1 proceeds with normal blocker logging. Crucially, **F1 does NOT halt** on a refusal — the failing item flips to `- [x]` via existing Error Handling step 3 (line 176, unrecoverable blocker logging), and the loop continues. |
| **Manifest feature(s)** | TU-6 (TFEP Prohibitions + Permitted exceptions — ADOPT); donor rows D19 + D20; stack-rank rows 2 + 4. Extension-point row 8. |
| **Priority** | **P2** — independent of M1 (TFEP prohibitions/carve-outs apply uniformly on test-failure blockers regardless of `Tier:`). Can land independently inside M3. Recommended sequencing inside M3: BEFORE CR-TASK-09 (prohibition_check fires before escalation classification at row 8). |
| **Effort** | **M** (~25 lines per manifest TU-6 "Shape of change"). |
| **Dependencies** | None upstream from M1 (TFEP cluster ADOPT entry point per DM-8). Recommended order inside M3: before CR-TASK-09. |
| **Acceptance criteria** | (1) On a test-failure blocker matching a VIOLATION → Task Log line `tfep: prohibition-refusal item=<id> rule=<VIOLATION-NN> reason=<reason>`. (2) On a test-failure blocker matching a carve-out → Task Log line `tfep: carve-out item=<id> rule=<carve-out-N> reason=<reason>`; NO VIOLATION line emitted. (3) In both cases, the failing item is **still** marked `- [x]` with the failure recorded via existing blocker logging — **F1 continues** (no halt). |
| **Risk assessment** | **INV at risk: INV-01 (loop control)** if a future variant halts F1 on TFEP engagement (donor's F1-HALTING behavior). **Mitigation: ME-3 (SIDE-CHANNEL ONLY, NO F1 HALT)** — the prohibition_check is a side-channel emit, NOT a loop-control branch. Halting F1 on TFEP engagement is auto-REJECT under INV-01. Additional **risk: drift from `sc-task-protocol/SKILL.md:127–135` / `:137–140`** if the verbatim strings are paraphrased on transcription. **Mitigation:** the inserted strings are copy-pasted character-for-character from the donor file path captured in T06.01 § 1 (path verified, md5-stable); Phase 7 must `diff` the inserted block against the donor source before commit. |

### CR-TASK-09 — Error Handling TFEP Escalation trigger detection (D22)

| Column | Value |
|---|---|
| **CR-ID** | CR-TASK-09 |
| **File path (side-tagged)** | `[src] src/superclaude/skills/task/SKILL.md` — *Error Handling* section (lines 170–179, co-located with CR-TASK-08). Insert ~15 lines AFTER the CR-TASK-08 prohibition+carve-out block. |
| **Change** | `add side-channel hook` — new pure-decision function `tfep_escalation_check(failing_tests, baseline) → {trigger | none}`. On test failure during F1, classify each failing test: **pre-existing** (in `research/test-baseline.yaml` from CR-TASK-07 AND was FAILING in baseline) or **new** (not in baseline OR was PASSING in baseline). Evaluate three MUST-escalate triggers sourced **verbatim** from `[src] src/superclaude/skills/sc-task-protocol/SKILL.md:200–210`: (1) any pre-existing test fails after this task's changes (regression); (2) ≥3 new tests fail simultaneously (systemic break); (3) runtime exception in implementation code (not test scaffolding). On trigger fire → route to `rf-qa` for adjudication using the existing INV-03 surface (Phase-Gate QA's existing 3-cycle fix loop — NO new escalation budget authored; LR-REJECT-2 ledger row blocks D25's 3-strike FULL STOP). |
| **Manifest feature(s)** | TU-7 (TFEP Escalation trigger detection — ADOPT); donor row D22; stack-rank row 9. Extension-point row 8. |
| **Priority** | **P2** — depends on CR-TASK-07 (consumes `research/test-baseline.yaml` as comparator per DM-7) and recommended-order after CR-TASK-08 at row 8 (prohibition_check + carve_out_check run BEFORE escalation classification). |
| **Effort** | **S** (~15 lines per manifest TU-7 "Shape of change"). |
| **Dependencies** | CR-TASK-07 (baseline file); CR-TASK-08 (recommended order before this row inside the Error Handling block). |
| **Acceptance criteria** | (1) On any trigger fire → Task Log line `tfep: escalation-trigger fired=<N> tests=[...] classification={pre-existing\|new}`. (2) Route to `rf-qa` via the existing Phase-Gate QA verifier-spawn pattern (lines 191–198 of SKILL.md) — NO new escalation gate authored, NO new budget. (3) If `rf-qa` adjudicates the failure as resolved in-task, CR-TASK-10 writes the incident report at Post-Completion. (4) F1 continues during and after trigger detection (ME-3). |
| **Risk assessment** | **INV at risk: INV-01 (loop control)** + **INV-03 (rf-qa adversarial-stance floor)**. Variant risk: re-introducing donor's "3-strike FULL STOP" escalation budget (D25, ledger row 20 / LR-REJECT-2) — duplicates Phase-Gate QA's existing 3-cycle loop. **Mitigation:** routes only to `rf-qa` via the existing surface; NO new budget mechanism authored (R-RULE-11 cross-check Section 4). Additional **risk: ME-3 violation** if a future variant halts F1 on trigger fire — **mitigation: ME-3 (SIDE-CHANNEL ONLY, NO F1 HALT)** binds the cluster. Additional **risk: drift from `sc-task-protocol/SKILL.md:200–210`** trigger strings — **mitigation:** verbatim transcription, Phase 7 must `diff` against the donor source before commit. |

### CR-TASK-10 — Post-Completion Validation TFEP incident-report check (D24)

| Column | Value |
|---|---|
| **CR-ID** | CR-TASK-10 |
| **File path (side-tagged)** | `[src] src/superclaude/skills/task/SKILL.md` — *Post-Completion Validation* section (lines 213–248). Insert ~20 lines (template + Post-Completion check) at the end of Step 1 (rf-qa structural validation block, lines 219–226). |
| **Change** | `add side-channel hook` — at TFEP-resolve time (D22 escalation triggered AND failure resolved in same task), write `${TASK_DIR}research/tfep-incident-report.md` as a side-effect FILE (NEVER as an inserted heading inside the task file — D23 Step 5 is REJECTed at this attach surface, ledger LR-DEFER-6). Schema preserved **verbatim** from `[src] src/superclaude/skills/sc-task-protocol/SKILL.md:222–234` with seven fields: Trigger, Escalation count, Failing tests (IDs + classification), Root cause, Solution, Outcome, Forensic artifacts. Post-Completion Validation reads the file (for STRICT items with test-failure history) and verifies the seven-field schema is populated; missing-field → validation failure routed to `rf-qa`. |
| **Manifest feature(s)** | TU-8 (TFEP Incident reporting — ADOPT); donor row D24; stack-rank row 5. Extension-point row 11. |
| **Priority** | **P2** — depends on CR-TASK-07 + CR-TASK-08 + CR-TASK-09 (DM-9: incident report records the side-effects of the TFEP cluster firing). |
| **Effort** | **M** (~20 lines per manifest TU-8 "Shape of change"). |
| **Dependencies** | CR-TASK-07 (baseline as comparator for `Failing tests` field classification); CR-TASK-08 (carve-out / VIOLATION context); CR-TASK-09 (the trigger that authored the report). |
| **Acceptance criteria** | (1) File `${TASK_DIR}research/tfep-incident-report.md` exists on disk for STRICT items where D22 escalation fired during the task. (2) The file's seven-field schema (Trigger, Escalation count, Failing tests, Root cause, Solution, Outcome, Forensic artifacts) is populated. (3) Post-Completion Validation step 1 (rf-qa structural, lines 219–226) verifies the seven-field schema and routes any missing-field to `rf-qa`. (4) The incident report is a **side-effect FILE** — no `## Failure Remediation Plan (Adjudicated)` heading is inserted into the task file itself (R-RULE-11 enforces LR-DEFER-6 D23 Step 5 REJECT at this attach surface). |
| **Risk assessment** | **INV at risk: F4 (task-file modification restriction) + INV-01 (loop control) + INV-05 (items must come from disk read)** if a future variant inserts the D23 Step 5 heading into the task file or implements D23 Step 6's "resume from inserted task." Both REJECTed at this attach surface (manifest § 2 TU-8 "Donor ceremony dropped" + ledger LR-DEFER-6). **Mitigation:** the report is written to a side-effect FILE at `${TASK_DIR}research/tfep-incident-report.md`; the task file's structure is untouched (F4 floor preserved). The Post-Completion check is read-only on the report. Additional **risk: ME-3 violation** if a future variant routes incident-report writing through F1 — **mitigation: ME-3 (SIDE-CHANNEL ONLY)** binds; the write is a side-channel file operation at Post-Completion validation time, not an F1 EXECUTE item. Additional risk: tier-gating drift — **mitigation:** tier-gated to STRICT items with test-failure history (transitively inherits ME-4 via CR-TASK-07's baseline dependency). |

### CR-TASK-11 — `make sync-dev` refresh of `[.claude]` mirror

| Column | Value |
|---|---|
| **CR-ID** | CR-TASK-11 |
| **File path (side-tagged)** | `[.claude] .claude/skills/task/SKILL.md` — refreshed by `make sync-dev` from `[src] src/superclaude/skills/task/SKILL.md` (NOT edited directly). Makefile target at `Makefile` lines 107–122 (verified in `merge-roadmap.md` § 1 row 9). |
| **Change** | `edit-in-place` (mechanical, via tooling) — after CR-TASK-01..10 land on `[src]`, run `make sync-dev` once to rsync `src/superclaude/skills/task/` → `.claude/skills/task/`. No manual edit of `.claude/` allowed (R-RULE-10 + global memory feedback rule "Never edit `.claude/` directly"). |
| **Manifest feature(s)** | R-RULE-10 enforcement; mechanical consequence of CR-TASK-01..10. Not a TU itself — this is the sync step the manifest requires after every `[src]` edit. |
| **Priority** | **P3** — runs after every CR-TASK-NN merge in this refactor. |
| **Effort** | **XS** (tooling invocation, no hand-edit). |
| **Dependencies** | CR-TASK-01..10 (all must be in `[src]` before this sync runs). |
| **Acceptance criteria** | (1) `md5sum [src] src/superclaude/skills/task/SKILL.md [.claude] .claude/skills/task/SKILL.md` returns identical hashes after sync. (2) `make verify-sync` returns 0. (3) `[.claude]` SKILL.md reflects all CR-TASK-01..10 edits byte-for-byte. |
| **Risk assessment** | **Risk: R-RULE-10 violation** if Phase 7 commits a manual `[.claude]` edit. **Mitigation:** every edit lands in `[src]` first; `make sync-dev` is the only mechanism to update `[.claude]`. The global memory `feedback_hooks_source_of_truth.md` row in MEMORY.md re-affirms this as a binding feedback rule. Additional **risk: drift** if `make sync-dev` is skipped before commit — **mitigation:** `make verify-sync` runs in CI per `CLAUDE.md` "Component Sync" section and must return 0 to commit. |

### CR-TASK-12 — Phase 7 commit-time `diff` audit against donor verbatim sources

| Column | Value |
|---|---|
| **CR-ID** | CR-TASK-12 |
| **File path (side-tagged)** | (audit step, no file edit) — verifies CR-TASK-01 path-glob sets and CR-TASK-08 / CR-TASK-09 / CR-TASK-10 verbatim donor strings against `[src] src/superclaude/skills/sc-task-protocol/SKILL.md:121`, `:123`, `:127–135`, `:137–140`, `:200–210`, `:222–234`. |
| **Change** | (no file edit) — a Phase 7 commit-time audit step that runs a textual `diff` of the donor strings inlined by CR-TASK-01 / CR-TASK-08 / CR-TASK-09 / CR-TASK-10 against the donor file lines they cite. Verbatim transcription is a manifest obligation (R-RULE-06 absorbs patterns, but where the manifest says "sourced verbatim," paraphrasing is a behavior shift the manifest did not authorize). |
| **Manifest feature(s)** | TU-2, TU-6, TU-7, TU-8 "verbatim from `sc-task-protocol/SKILL.md:NNN`" obligations. Cross-row guard against silent paraphrase drift. |
| **Priority** | **P3** — runs at Phase 7 commit time, after CR-TASK-11. |
| **Effort** | **XS** (one shell `diff` invocation per verbatim block; six total). |
| **Dependencies** | CR-TASK-01 + CR-TASK-08 + CR-TASK-09 + CR-TASK-10 (the rows that inline verbatim donor strings); CR-TASK-11 (sync must have run). |
| **Acceptance criteria** | Six `diff` invocations (path-glob critical set, path-glob trivial set, three VIOLATION strings, three D20 carve-outs, three D22 triggers, seven-field D24 schema) all return zero differences. Any non-zero diff blocks the commit until the inserted text is corrected to verbatim. |
| **Risk assessment** | **Risk: silent semantic drift** if a donor verbatim string is paraphrased on transcription (e.g., "≥3 new tests fail simultaneously" → "3 or more new tests fail" loses the inclusive-equality semantics in the trigger condition). The drift could mask a TFEP escalation that should fire. **Mitigation:** mechanical `diff` against the side-tagged donor source; CR-TASK-08's risk-row already names this for verbatim donor strings. CR-TASK-12 is the cross-row enforcement step. **INV protected: INV-03 (rf-qa adversarial-stance floor)** — incorrect trigger thresholds would route fewer escalations to `rf-qa` than the manifest absorbs. |

---

## 3. Change-row roll-up

### 3.1 By milestone

| Milestone | Change rows | Effort total | Priority floor |
|---|---|---|---|
| M1 — Foundation (atomic merge) | CR-TASK-01, CR-TASK-02, CR-TASK-03, CR-TASK-04 | S + M + XS + XS ≈ **M (aggregate ≈ 40 lines)** | **P0** |
| M2 — Tier-Conditioned Behaviors | CR-TASK-05, CR-TASK-06 | M + M ≈ **M+ (~40–50 lines)** | **P1** |
| M3 — TFEP Cluster | CR-TASK-07, CR-TASK-08, CR-TASK-09, CR-TASK-10 | M + M + S + M ≈ **L (~70 lines)** | **P2** |
| M-sync — sync + audit | CR-TASK-11, CR-TASK-12 | XS + XS ≈ **XS** | **P3** |

**Aggregate effort estimate:** ~150–170 lines net additions to `[src] src/superclaude/skills/task/SKILL.md`, mostly concentrated in *Validating the Task File* (CR-TASK-01..03), *First Item Protocol* (CR-TASK-06 + CR-TASK-07), and *Error Handling* (CR-TASK-08 + CR-TASK-09). No deletions, no renames.

### 3.2 By extension-point row touched (R-RULE-06 cross-check)

| Extension-point row | SKILL.md line range | Change rows touching it | TU(s) |
|---|---|---|---|
| Row 1 — Task File Validation gate | 65–73 | CR-TASK-01, CR-TASK-02 | TU-1, TU-2 |
| Row 2 — First Item Protocol | 100–102 | CR-TASK-06, CR-TASK-07 | TU-4, TU-5 |
| Row 4 — F1 EXECUTE item-type dispatch | 89–96 | CR-TASK-03 | TU-1 |
| Row 8 — Error Handling / blocker logging | 170–179 | CR-TASK-08, CR-TASK-09 | TU-6, TU-7 |
| Row 10 — Phase-Gate QA Verification | 182–211 | CR-TASK-04, CR-TASK-05 | TU-2, TU-3 |
| Row 11 — Post-Completion Validation | 213–248 | CR-TASK-10 | TU-8 |
| Row 13 — Required frontmatter schema slot | (frontmatter description at line 68) | CR-TASK-02 (closed-enum validator) — schema field itself documented in companion `refactor-mdtm-frontmatter.md` | TU-1 |

Seven extension-point rows touched; matches the seven rows the manifest names as absorption surfaces. **No untouched manifest extension point** (forward traceability).

### 3.3 By manifest exception (ME-NN binding)

| ME | Title | Bound change rows |
|---|---|---|
| ME-1 | PRE-LOOP DISPATCH ONLY | CR-TASK-02 (primary), CR-TASK-03 (per-item marker MUST NOT re-fire dispatch) |
| ME-2 | `rf-qa` SUPPLEMENTED NOT REPLACED | CR-TASK-05 (roster widening, never substitution); CR-TASK-04 (Gate 2 override read MUST NOT swap verifiers) |
| ME-3 | SIDE-CHANNEL ONLY, NO F1 HALT | CR-TASK-08, CR-TASK-09, CR-TASK-10 (and transitively CR-TASK-07 — baseline is pre-loop, not F1-halting) |
| ME-4 | BASELINE TIER-GATED | CR-TASK-07 (primary); CR-TASK-10 (transitively, via baseline-dependent classification) |
| ME-5 | NO PER-ITEM EXECUTE SUBSTITUTION | CR-TASK-06 (REJECTs D15c at the attach surface) |
| ME-6 | TIER FIELD + GATE 1 SHIP TOGETHER | CR-TASK-01 ↔ CR-TASK-02 ↔ CR-TASK-03 (atomic ship-together merge) |
| ME-7 | D08 DEFERRED UNTIL PARSER SHIPS | (no change row authored — LR-DEFER-5 stays in ledger; this refactor MUST NOT emit a classification header. § 4 cross-check confirms.) |
| ME-8 | D01 DEFERRED UNTIL LOADER + RULE 6 SPLIT | (no change row authored — LR-DEFER-4 stays in ledger; this refactor MUST NOT add `allowed-tools:` to the task SKILL.md frontmatter. § 4 confirms.) |
| ME-9 | D02/Layer A REJECT (R-RULE-06 override) | (no change row authored in this refactor — handled by T06.03 / CS-M4-A `mcp-servers:` removal on the donor side. Listed for completeness.) |

Six MEs are actively bound by rows in this refactor (ME-1, ME-2, ME-3, ME-4, ME-5, ME-6). Three are observed-but-not-emitted (ME-7, ME-8, ME-9 → confirmed in § 4 cross-check).

---

## 4. R-RULE-11 cross-check — no ledger entry re-proposed

Every change row in § 2 traces to a manifest TU. None re-propose a `rejected-features-ledger.md` entry. Spot-checks against the highest-risk ledger entries:

| Ledger entry | Re-proposal risk in this refactor? | Mitigation in change row |
|---|---|---|
| LR-REJECT-3 (D09b — runtime tier classifier inside `/task`) | Could be silently reintroduced if CR-TASK-02 derived `Tier:` from keyword scanning. | **No re-proposal.** CR-TASK-02 reads `Tier:` declaratively from frontmatter only. The closed-enum validator rejects malformed values rather than guessing them. |
| LR-REJECT-2 (D25 — 3-strike FULL STOP escalation budget) | Could be silently reintroduced if CR-TASK-09 authored a new escalation budget. | **No re-proposal.** CR-TASK-09 routes to `rf-qa` via the existing Phase-Gate QA 3-cycle loop. No new budget authored. |
| LR-REJECT-4 (Gate 5 — user-toggleable override flags) | Could be silently reintroduced if CR-TASK-01 added flag inputs to `path_override_check`. | **No re-proposal.** CR-TASK-01's override is **path-glob-keyed**, not flag-keyed. No `--strict` / `--explain` CLI plumbing authored. |
| LR-REJECT-7 (D15c — per-tier procedure synthesis at execute-time) | Could be silently reintroduced if CR-TASK-06 placed pre-flight steps inside F1 EXECUTE. | **No re-proposal.** CR-TASK-06 is anchored at *First Item Protocol* (BEFORE F1 starts) and never authors per-item runtime steps (ME-5). |
| LR-DEFER-4 (D01 — `allowed-tools:` frontmatter) | Could be silently reintroduced if a change row added `allowed-tools:` to the task SKILL.md frontmatter. | **No re-proposal.** No change row in § 2 touches `allowed-tools:`. ME-8 binds. |
| LR-DEFER-5 (D08 — classification header emission) | Could be silently reintroduced if a change row added a `## Classification:` heading emit. | **No re-proposal.** No change row in § 2 emits a classification header. ME-7 binds. |
| LR-DEFER-6 (D23 — six-step flow / heading insert / resume-from-inserted) | Could be silently reintroduced if CR-TASK-10 inserted a `## Failure Remediation Plan (Adjudicated)` heading into the task file. | **No re-proposal.** CR-TASK-10 writes a side-effect FILE (`research/tfep-incident-report.md`). The task file's structure is untouched. F4 floor preserved. |

**Cross-check result: zero ledger entries re-proposed across CR-TASK-01..12.**

---

## 5. Dependency graph (change-row level)

```text
                M1 ATOMIC MERGE (ship-together per ME-6)
            ┌─────────────────────────────────────────┐
            │                                         │
            │    CR-TASK-01 ──► CR-TASK-02            │
            │   (path_override)  (Tier field +        │
            │                     Gate 1 dispatch)    │
            │         │              │                │
            │         │              ▼                │
            │         │         CR-TASK-03            │
            │         │      (per-item Tier read      │
            │         │       in F1 EXECUTE)          │
            │         │                               │
            │         ▼                               │
            │    CR-TASK-04 (Gate 2 override read     │
            │     at row 10 — CR-8 ordering)          │
            └─────────────────────────────────────────┘
                              │
                              ▼
                M2 TIER-CONDITIONED BEHAVIORS
            ┌─────────────────────────────────────────┐
            │                                         │
            │  CR-TASK-05 (Phase-Gate QA widening)    │
            │  CR-TASK-06 (First-Item pre-flight)     │
            └────────────┬────────────────────────────┘
                         │
                         ▼
                M3 TFEP CLUSTER (DM-7 / DM-9 internal ordering)
            ┌─────────────────────────────────────────┐
            │                                         │
            │  CR-TASK-07 (baseline)                  │
            │    │                                    │
            │    │   CR-TASK-08 (prohibitions+carves) │
            │    │     │                              │
            │    ▼     ▼                              │
            │  CR-TASK-09 (escalation classification) │
            │    │                                    │
            │    ▼                                    │
            │  CR-TASK-10 (incident-report file)      │
            └─────────────────────────────────────────┘
                              │
                              ▼
                M-sync (mechanical)
            ┌─────────────────────────────────────────┐
            │  CR-TASK-11 (make sync-dev)             │
            │  CR-TASK-12 (verbatim-diff audit)       │
            └─────────────────────────────────────────┘
```

**Acyclicity confirmed.** Topological order: CR-TASK-01 ≡ CR-TASK-02 ≡ CR-TASK-03 ≡ CR-TASK-04 (M1 atomic) → {CR-TASK-05, CR-TASK-06} (M2) → {CR-TASK-07 → CR-TASK-09; CR-TASK-08 → CR-TASK-09} (M3 partial) → CR-TASK-10 (M3 cap) → CR-TASK-11 → CR-TASK-12.

---

## 6. Acceptance Criteria recap (T06.02)

1. **`refactor-task-skill.md` exists; every change row has file path, change, manifest-feature ref, priority, effort, dependencies, acceptance criteria, risk assessment.** ✅ — Twelve rows (CR-TASK-01..12), eight columns each (§ 1 + § 2).
2. **Every file path is auggie-verified and side-tagged (R-RULE-10).** ✅ — All edits target `[src] src/superclaude/skills/task/SKILL.md` (verified present at 32951 B in `merge-roadmap.md` § 1 row 1; byte-identical to `[.claude]` mirror per CP-P05-END drift audit). Donor reference paths cited verbatim from `[src] src/superclaude/skills/sc-task-protocol/SKILL.md` (verified present at 14925 B, byte-identical to `[.claude]` mirror per merge-roadmap § 1 row 3). `Makefile` (sync-dev target lines 107–122) verified present per merge-roadmap § 1 row 9.
3. **Every risk assessment names the INV-NN at risk and its mitigation.** ✅ — Twelve risk-assessment cells reference at least one of INV-01, INV-03, INV-04, INV-05, F4, and/or the bound manifest exception (ME-1..ME-6) that constrains the implementation to the safe shape.
4. **The MDTM frontmatter additions and their backward-compat behavior live in the companion file `refactor-mdtm-frontmatter.md`** (T06.02 acceptance #3 — INV-04 resumability).

**T06.02 (refactor-task-skill.md) deliverable: COMPLETE.** Phase 7 has 12 ordered, eight-column change rows driving every `/task` SKILL.md edit implied by the manifest ADOPT/ADAPT features, with explicit ME-NN / INV-NN safety bindings on every row.
