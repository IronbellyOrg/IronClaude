# Merge Master — Unified Merge Plan (Phase 6 / T06.05)

**Task:** T06.05 — Produce `merge-master.md` unified plan
**Roadmap Item:** R-023
**Tier:** STRICT
**Generated:** 2026-05-15
**Status:** Driving input for Phase 7 execution. Consolidates **every change row** from the five refactor-`*.md` files (six artifacts) into a single ordered table, merges per-area dependency edges into one acyclic graph, and locks the recommended execution order (M1+M2+M3 absorption into `/task` → M4 `/sc:task` deprecation → M5 distribution + documentation).

**Inputs (1:1 referenced, all auggie-/T06.01-verified present):**
- `merge-roadmap.md` (T06.01) — 5 milestones M1–M5; 12 macro change-sets CS-M1-A..CS-M5-B; acyclic dependency graph; 17 side-tagged file paths.
- `refactor-task-skill.md` (T06.02) — 12 change rows **CR-TASK-01..CR-TASK-12** (`/task` SKILL.md edits).
- `refactor-mdtm-frontmatter.md` (T06.02) — 4 change rows **CR-FM-01..CR-FM-04** (MDTM frontmatter schema additions).
- `refactor-sctask-deprecation.md` (T06.03) — 5 change rows **CR-DEP-01..CR-DEP-05** (donor artifact disposition).
- `refactor-references.md` (T06.03) — 17 per-file/cluster rows **CR-REF-01..CR-REF-18** + 8 bucket rows **CR-REF-BUCKET-A..H** (reference enumeration & treatment).
- `refactor-distribution.md` (T06.04) — 6 change rows **CR-DIST-01..CR-DIST-06** (installer / sync / plugin / README).
- `refactor-documentation.md` (T06.04) — 13 change rows **CR-DOC-01..CR-DOC-13** (docs).
- `transfer-manifest.md` (T05.03) — 8 transfer units TU-1..TU-8; 9 manifest exceptions ME-1..ME-9.
- `rejected-features-ledger.md` (T05.03) — 17 REJECT + 9 DEFER entries; terminal under R-RULE-11.

**Side-tagging convention (R-RULE-10):** every operative path is tagged `[src]` (source of truth, `src/superclaude/...`), `[.claude]` (dev-copy mirror), `[plugins]` (v5.0 plugin distribution surface), or `[docs]`/`[.dev]`/`[tests]`/`[Makefile]`/`[plugins]` as appropriate. `[.claude]` mirrors are **never edited directly** — refreshed by `make sync-dev` after `[src]` edits; `make verify-sync` returns 0 before commit.

**R-RULE-11 audit:** every consolidated row traces to a `transfer-manifest.md` TU-N or a derivative deprecation/distribution/documentation responsibility. § 4 enumerates the audit against the 26 `rejected-features-ledger.md` entries.

---

## 0. Column legend (unified — all rows carry the same eight columns)

| Column | Meaning |
|---|---|
| **CR-ID** | Stable identifier inherited verbatim from the source refactor file (`CR-TASK-NN`, `CR-FM-NN`, `CR-DEP-NN`, `CR-REF-NN`/`CR-REF-BUCKET-X`, `CR-DIST-NN`, `CR-DOC-NN`). |
| **File path (side-tagged)** | Primary `[src]` / `[plugins]` / `[docs]` / `[.dev]` / `[Makefile]` / `[tests]` target. `[.claude]` mirrors are refreshed by `make sync-dev` and called out in the source rows where relevant. |
| **Change** | Operation: `add hook` / `add field-validator` / `add new section` / `add side-channel hook` / `edit-in-place` / `add code path` / `remove code path` / `soft-deprecate` / `hard-deprecate` / `remove-field` / `redirect` / `remove` / `leave-with-note` / `leave-as-is` / `sync` / `audit`. |
| **Manifest feature(s)** | TU-N / ME-N / merge-roadmap CS-M-N / CR-rule the row implements or honors. |
| **Priority** | P0 = atomic-merge / ship-together / blocks `make test` / blocks the merge announcement; P1 = direct dependent of P0; P2 = tier-conditioned / consequential cleanup; P3 = audit-only / annotation / pipeline-deferred. |
| **Effort** | XS ≤ 5 lines; S ≤ 15; M ≤ 30; L ≤ 60; XL > 60. |
| **Dependencies** | Build-order edges (other CR-IDs that must land first). Ship-together obligations are flagged in § 5. |
| **Acceptance criteria** | Observable post-condition Phase 7 verifies before marking the row done (text in source refactor files is binding; this column is a one-line digest). |
| **Risk assessment** | INV-NN / ME-NN / R-RULE-NN at risk + mitigation (one-line digest pointing at the source refactor file's full risk row). |

Where a row's full eight-column entry is large, this file gives a one-line digest in the **Acceptance criteria** and **Risk assessment** columns and points at the source refactor file's section/CR-ID for the binding text. The full eight-column text in the five refactor files is the authoritative source; **this file is the consolidation index, not a replacement.**

---

## 1. Master ordered table — every change row across the five refactor files

The table is ordered by **execution order** (M1 atomic → M2 → M3 → M-sync → M4 → M5-distribution → M5-documentation → audits). Within a milestone, rows are ordered by priority (P0 → P3) then by CR-ID. The order is the recommended Phase 7 commit sequence; § 5 enumerates the explicit acyclic dependency graph that bounds it.

### 1.1 M1 — Foundation (atomic merge; TU-1 + TU-2; P0)

| # | CR-ID | Path (side-tagged) | Change | Manifest feature(s) | Prio | Effort | Deps | Acceptance (digest) | Risk (digest) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | CR-FM-01 | `[src] src/superclaude/skills/task/SKILL.md` (validator section, line 68 area) | `add new frontmatter field` (optional `Tier:` closed-enum) | TU-1 / D09a; ME-1; ME-6 | P0 | XS | (atomic w/ CR-FM-02, CR-TASK-01..03) | optional `Tier:` field validates; closed-enum `{STRICT, STANDARD, LIGHT, EXEMPT}`; default `STANDARD` (see `refactor-mdtm-frontmatter.md` CR-FM-01) | INV-04 (optional, default resolves missing); ME-7/ME-8 not bundled |
| 2 | CR-FM-02 | `[src] src/superclaude/skills/task/SKILL.md` (EXECUTE step, lines 89–96) | `add inline marker schema` `(Tier: <value>)` per-item | TU-1 (per-item marker) | P0 | XS | CR-FM-01 | parser reads marker; fallback to task-level; never re-fires Gate 1 (ME-1) | INV-01 + ME-1 binding; INV-05 (no embedded run-clauses) |
| 3 | CR-FM-03 | `[src] src/superclaude/skills/task/SKILL.md` (validator); read-only against `[.dev] .dev/tasks/to-do/TASK-*/` | `add compat shim` (default `STANDARD` for missing `Tier:`) | INV-04; TU-1 default; ME-6 | P0 | XS | CR-FM-01, CR-TASK-02 | existing TASK-* files validate clean post-merge; emit `gate-1: ... source=default`; NO migration | INV-04 load-bearing; no silent behavior shift in STANDARD |
| 4 | CR-TASK-01 | `[src] src/superclaude/skills/task/SKILL.md` *Validating the Task File* (lines 65–73) | `add hook` `path_override_check` (path-glob keyed; verbatim sets from `sc-task-protocol/SKILL.md:121,123`) | TU-2 / D17 + D18; CR-7 ordering | P0 | S | (ship-together w/ CR-TASK-02..04, CR-FM-01..03) | Task Log `path-override: forced_stance=…` emitted **first** at task entry | INV-01 + CR-7/CR-8; verbatim path-globs (mitigated by CR-TASK-12 diff) |
| 5 | CR-TASK-02 | `[src] src/superclaude/skills/task/SKILL.md` *Validating the Task File* | `add field-validator` (closed-enum) + `add hook` `gate_1_dispatch` (PRE-LOOP ONLY) | TU-1 / D04 + D09a + D10; ME-1; ME-6 | P0 | M | CR-TASK-01, CR-FM-01 | malformed `Tier:` rejected; single Task Log `gate-1: dispatch_profile=… source=…` once at entry | INV-01 + ME-1 binding; LR-REJECT-3 not re-introduced (no runtime classifier) |
| 6 | CR-TASK-03 | `[src] src/superclaude/skills/task/SKILL.md` *F1 EXECUTE* (lines 89–96) | `edit-in-place` per-item inline-marker read | TU-1 (per-item annotation) | P0 | XS | CR-TASK-02, CR-FM-02 | per-item `(Tier: …)` overrides task-level for tier-conditioned reads only; never re-fires Gate 1 | INV-01 + ME-1 binding |
| 7 | CR-TASK-04 | `[src] src/superclaude/skills/task/SKILL.md` *Phase-Gate QA Verification* (lines 182–211) | `edit-in-place` Gate 2 stance-select reads `forced_stance` first (CR-8) | TU-2 (row 10 integration); CR-8 | P0 | XS | CR-TASK-01 | qa-stance-source attribution emitted; `forced_stance=STRICT` overrides `Tier:` at Gate 2 | INV-03 (rf-qa floor) + ME-2 (verifier identity untouched here) |

**M1 atomicity rule (ME-6 + CR-7 + CR-9):** rows 1–7 ship in **one source-tree merge**. Splitting CR-FM-01 from CR-TASK-02 leaves `Tier:` as inert metadata; splitting CR-TASK-01 from CR-TASK-02 reopens the wrong-stance dispatch window at runtime row 1.

### 1.2 M2 — Tier-Conditioned Behaviors (P1; depends on M1)

| # | CR-ID | Path (side-tagged) | Change | Manifest feature(s) | Prio | Effort | Deps | Acceptance (digest) | Risk (digest) |
|---|---|---|---|---|---|---|---|---|---|
| 8 | CR-TASK-05 | `[src] src/superclaude/skills/task/SKILL.md` *Phase-Gate QA* | `edit-in-place` tier→{budget, timeout, roster} mapping inlined | TU-3 / D15a + D16; ME-2 | P1 | M | CR-TASK-02, CR-TASK-04 | `verifier_roster: [rf-qa, quality-engineer]` on STRICT; `rf-qa` always present | INV-03 floor + ME-2 (rf-qa supplemented, not replaced) |
| 9 | CR-TASK-06 | `[src] src/superclaude/skills/task/SKILL.md` *First Item Protocol* (lines 100–102) | `add new section` tier-gated pre-flight (serena / git / codebase-retrieval / memory; STANDARD: codebase-retrieval; LIGHT/EXEMPT: skip) | TU-4 / D15b; ME-5 | P1 | M | CR-TASK-01, CR-TASK-02 | Task Log `gate-1.5: pre-flight tier=… ran=[…]` once before F1 first iteration | INV-01 + INV-05 + ME-5 (no per-item synthesis; LR-REJECT-7 not revived) |

### 1.3 M3 — TFEP Cluster (P2; internal DM-7/DM-9 ordering)

| # | CR-ID | Path (side-tagged) | Change | Manifest feature(s) | Prio | Effort | Deps | Acceptance (digest) | Risk (digest) |
|---|---|---|---|---|---|---|---|---|---|
| 10 | CR-TASK-07 | `[src] src/superclaude/skills/task/SKILL.md` *First Item Protocol* | `add new section` tier-gated TFEP baseline (`research/test-baseline.yaml`) | TU-5 / D21; ME-4 | P2 | M | CR-TASK-02, CR-TASK-06 | baseline YAML present pre-F1 on STRICT/STANDARD; absent on LIGHT/EXEMPT | ME-4 (tier-gated) + INV-04 (Incremental Writing Protocol for atomic baseline write) |
| 11 | CR-TASK-08 | `[src] src/superclaude/skills/task/SKILL.md` *Error Handling* (lines 170–179) | `add side-channel hook` `tfep_prohibition_check` + carve-outs (verbatim from `sc-task-protocol/SKILL.md:127–135` + `:137–140`) | TU-6 / D19 + D20; ME-3 | P2 | M | (none from M1; recommended before CR-TASK-09) | `tfep: prohibition-refusal …` / `carve-out …` Task Log lines; **F1 continues** (no halt) | INV-01 + ME-3 (side-channel only); verbatim strings (CR-TASK-12 diff) |
| 12 | CR-TASK-09 | `[src] src/superclaude/skills/task/SKILL.md` *Error Handling* | `add side-channel hook` `tfep_escalation_check` (triggers verbatim from `sc-task-protocol/SKILL.md:200–210`) | TU-7 / D22; ME-3 | P2 | S | CR-TASK-07, CR-TASK-08 | `tfep: escalation-trigger fired=… classification=…`; route to existing `rf-qa` (no new budget; LR-REJECT-2 not revived) | INV-01 + INV-03 + ME-3; verbatim trigger strings (CR-TASK-12) |
| 13 | CR-TASK-10 | `[src] src/superclaude/skills/task/SKILL.md` *Post-Completion Validation* (lines 213–248) | `add side-channel hook` write `research/tfep-incident-report.md` (seven-field schema verbatim from `:222–234`); side-effect FILE (LR-DEFER-6 not revived) | TU-8 / D24; ME-3; ME-4 (transitive) | P2 | M | CR-TASK-07, CR-TASK-08, CR-TASK-09 | side-effect file present on STRICT items with TFEP fire; seven-field schema populated; NO `## Failure Remediation` heading inserted into task file | F4 + INV-01 + INV-05 + ME-3; verbatim schema (CR-TASK-12) |

### 1.4 M-sync — `make sync-dev` refresh + verbatim diff audit (P3)

| # | CR-ID | Path (side-tagged) | Change | Manifest feature(s) | Prio | Effort | Deps | Acceptance (digest) | Risk (digest) |
|---|---|---|---|---|---|---|---|---|---|
| 14 | CR-TASK-11 | `[.claude] .claude/skills/task/SKILL.md` (mirror); refreshed via `make sync-dev` | `sync` (mechanical, no manual edit) | R-RULE-10 | P3 | XS | CR-TASK-01..10, CR-FM-01..03 | `md5sum` matches; `make verify-sync` returns 0 | R-RULE-10 (no direct mirror edits; sync-dev only path) |
| 15 | CR-FM-04 | (audit step; no edit) covers `[src] src/superclaude/skills/task/SKILL.md` + spot-check `[.dev] .dev/tasks/to-do/TASK-*/` (N=5) | `audit` (closed-enum single-source + INV-04 spot-check) | INV-04 audit; R-RULE-11 audit (against LR-DEFER-4/-5 / LR-REJECT-3 sneak-in) | P3 | XS | CR-FM-01, CR-FM-02, CR-FM-03, CR-TASK-02, CR-TASK-03 | grep finds enum in exactly the authored locations; 5 spot-check TASK-* files validate clean | INV-04 + R-RULE-11 |
| 16 | CR-TASK-12 | (audit step; no edit) verifies six verbatim donor blocks vs `[src] src/superclaude/skills/sc-task-protocol/SKILL.md:121, :123, :127–135, :137–140, :200–210, :222–234` | `audit` (six `diff` invocations) | TU-2/TU-6/TU-7/TU-8 verbatim obligations | P3 | XS | CR-TASK-01, CR-TASK-08, CR-TASK-09, CR-TASK-10, CR-TASK-11 | six diffs return zero differences; any non-zero diff blocks commit | INV-03 (incorrect thresholds mask escalations) — mechanical mitigation |

### 1.5 M4 — `/sc:task` Deprecation (P0/P1; post-M1+M2+M3 absorption)

| # | CR-ID | Path (side-tagged) | Change | Manifest feature(s) | Prio | Effort | Deps | Acceptance (digest) | Risk (digest) |
|---|---|---|---|---|---|---|---|---|---|
| 17 | CR-DEP-01 | `[src] src/superclaude/commands/task.md` | `soft-deprecate` (rewrite body to ~10-line redirect stub) + `remove-field` (`mcp-servers:`, `personas:` lines) | CS-M4-A; ME-9; D10 donor-traceability | P0 | S | (M1+M2+M3 absorption complete: CR-TASK-01..10, CR-FM-01..03) | `/sc:task` emits single deprecation line and exits; `mcp-servers:`/`personas:` removed | ME-9; no INV at risk (deprecation w/ redirect) |
| 18 | CR-DEP-02 | `[.claude] .claude/commands/sc/task.md` (refreshed by `make sync-dev`) | `sync` (mechanical) | R-RULE-10 | P0 | XS | CR-DEP-01 | mirror md5 matches body (modulo layout reshape); `make verify-sync` returns 0 | R-RULE-10 |
| 19 | CR-DIST-02 | `[Makefile] Makefile` `sync-dev` target (lines 107–151) | `add code path` generic orphan-prune loop after line 124 | CS-M5-A; CR-DEP-04 mirror-cleanup mechanism; R-RULE-10 | P0 | S | (ship-together w/ CR-DEP-03 + CR-DEP-04) | `.claude/skills/sc-task-protocol/` absent after sync; `make verify-sync` returns 0 in the same commit | R-RULE-10 drift (generic predicate prevents wrong-deletion); R-RULE-06 (mechanism, not special-case) |
| 20 | CR-DEP-03 | `[src] src/superclaude/skills/sc-task-protocol/SKILL.md` | `hard-deprecate` (delete file) | CS-M4-A; R-RULE-06; TU-1..TU-8 absorbed at recipient | P1 | XS | CR-DEP-01, CR-DEP-02, CR-TASK-01..10 (absorbed) | file absent; no `Skill sc:task-protocol` invocation remains; § 4 of `refactor-sctask-deprecation.md` absorption traceability holds | INV-01/INV-03/INV-04 only if a pattern stranded — § 4 audit prevents |
| 21 | CR-DEP-04 | `[src] src/superclaude/skills/sc-task-protocol/__init__.py` + `rmdir` + `[.claude] .claude/skills/sc-task-protocol/` (via CR-DIST-02 prune) | `hard-deprecate` (delete `__init__.py`, rmdir dir, prune mirror) | CS-M4-A; R-RULE-10 | P1 | XS | CR-DEP-03, CR-DIST-02 | both `src/` and `.claude/` directories absent; `make verify-sync` returns 0 | R-RULE-10 (atomic w/ CR-DEP-03 + CR-DIST-02) |
| 22 | CR-DIST-01 | `[src] src/superclaude/cli/install_skills.py` (no edit) + `[tests] tests/cli/test_install_skills.py` (new regression test) | `audit` + add regression test (~10–15 lines) | CS-M5-A; CR-DEP-03/04 behavior verification | P1 | S | CR-DEP-03, CR-DEP-04 | `uv run pytest tests/cli/test_install_skills.py` passes; installer excludes `sc-task-protocol`; `superclaude doctor` clean | R-RULE-06 (no hard-coded special-case authored) |
| 23 | CR-DIST-04 | `[Makefile] Makefile` `verify-sync` (no edit; audit) | `audit` orphan rule fires on deletion | CS-M5-A; CR-DIST-02 sufficiency | P2 | XS | CR-DIST-02 | `make verify-sync` returns 0 post-prune; negative-test (stash CR-DIST-02 → verify-sync reports MISSING) documented in commit message | R-RULE-10 |
| 24 | CR-DEP-05 | (audit only) `[src] src/superclaude/commands/task.md` + `[.claude] .claude/commands/sc/task.md` | `audit` (re-affirm `mcp-servers:` / `personas:` removal) | ME-9; R-RULE-11 audit | P2 | XS | CR-DEP-01 | grep returns zero matches on both `[src]` and `[.claude]`; commit message cites ME-9 | R-RULE-11 (no silent re-introduction) |

### 1.6 M5-A — Distribution: Plugin stub + README (P1/P3)

| # | CR-ID | Path (side-tagged) | Change | Manifest feature(s) | Prio | Effort | Deps | Acceptance (digest) | Risk (digest) |
|---|---|---|---|---|---|---|---|---|---|
| 25 | CR-DIST-03 | `[plugins] plugins/superclaude/commands/task.md` | `edit-in-place` (rewrite redirect target to `/task`; remove obsolete `deprecated_by:` / `migration_guide:` frontmatter) | CS-M5-A; CR-REF-08 companion | P1 | S | CR-DEP-01 | grep returns no `task-unified` / `deprecated_by`; body uses CR-DEP-01 redirect language; `category: deprecated` | R-RULE-11 (no `mcp-servers:` / `personas:` re-introduction); v5.0 plugin spec forward-compatibility |
| 26 | CR-DIST-05 | `[src] README.md` | `audit` (no edit; README never named `/sc:task`) | CS-M5-A; R-RULE-11 (no re-litigation) | P3 | XS | (none) | post-merge grep returns 0 matches (same as pre-merge); commit message records no-op | none |
| 27 | CR-DIST-06 | (audit row over CR-DIST-01..05) | `audit` (R-RULE-11 cross-check) | R-RULE-11 | P3 | XS | CR-DIST-01..05 | § 4 audit table holds; Phase 7 reviewer confirms | R-RULE-11 |

### 1.7 M5-B — Active source reference redirects (P0/P1)

| # | CR-ID | Path (side-tagged) | Change | Manifest feature(s) | Prio | Effort | Deps | Acceptance (digest) | Risk (digest) |
|---|---|---|---|---|---|---|---|---|---|
| 28 | CR-REF-01 | `[src] src/superclaude/cli/sprint/process.py` (lines 124, 170) | `redirect` `/sc:task` → `/task` (2 line edits) | CS-M4-B | P0 | XS | CR-DEP-01 | grep `/sc:task` returns 0 in file; tests align (CR-REF-09) | runtime CLI; atomic w/ CR-DEP-01 |
| 29 | CR-REF-02 | `[src] src/superclaude/cli/cleanup_audit/prompts.py` (lines 26, 47, 69, 92, 116) | `redirect` (5 edits) | CS-M4-B | P0 | XS | CR-DEP-01 | grep returns 0 matches; existing tests pass | runtime CLI; atomic w/ CR-DEP-01 |
| 30 | CR-REF-09 | `[tests] tests/sprint/test_process.py` + `tests/pipeline/test_process.py` + `tests/sprint/test_tui_v2_wave2.py` | `redirect` assertions to `/task`; **keep** historical guard `/sc:task-unified not in prompt`; add new guard `/sc:task not in prompt`; **leave-as-is** filename refs (`v3.7-task-unified-v2`) | CS-M4-B; test parity w/ CR-REF-01/02 | P0 | S | CR-REF-01, CR-REF-02 | `uv run pytest` passes the three test files; three assertions per test, not two | regression-guard preserved |
| 31 | CR-REF-04 | `[src] src/superclaude/commands/{adversarial,help,release-split,tasklist,validate-roadmap,validate-tests}.md` | `redirect` body + cross-reference list rewrites; anchors updated | CS-M4-B | P1 | S | CR-DEP-01 | grep finds no `/sc:task` in non-`task.md` files under `src/superclaude/commands/`; `make verify-sync` returns 0 | anchor drift (mitigated by same-edit anchor rewrite) |
| 32 | CR-REF-05 | `[src] src/superclaude/core/COMMANDS.md:81`, `[src] src/superclaude/core/ORCHESTRATOR.md:153` | `redirect` (COMMANDS.md catalog row) + `remove`/`redirect` (ORCHESTRATOR.md routing prose to describe `/task` Gate 1) | CS-M4-B; TU-1 (Gate 1 description must match) | P1 | S | CR-DEP-01, CR-TASK-02 | grep returns 0 matches; replacement names declarative `Tier:` (R-RULE-11 audit) | LR-REJECT-3 (no runtime classifier prose) |
| 33 | CR-REF-06 | `[src] src/superclaude/skills/sc-{cli-portify,release-split,roadmap,tasklist,validate-roadmap,validate-tests}-protocol/...` | `redirect` body cross-references | CS-M4-B | P1 | S | CR-DEP-01 | grep returns no `/sc:task` in sibling protocol skill dirs (excluding `sc-task-protocol/` which CR-DEP-03 deletes) | sibling-prose narrative preserved |
| 34 | CR-REF-07 | `[src] src/superclaude/examples/{release-spec-template,tasklist_index_template,tasklist_phase_template}.md` | `redirect` `/sc:task` only (preserve `sc:tasklist` / `sc:roadmap`) | CS-M4-B | P2 | XS | CR-DEP-01 | anchored regex `(^\|\W)/sc:task(\W\|$)` returns 0; `/sc:tasklist` untouched | false-positive avoidance |
| 35 | CR-REF-08 | `[plugins] plugins/superclaude/commands/task.md` | `redirect` (companion to CR-DIST-03 — frontmatter cleanup + body redirect to `/task`) | CS-M4-B; CR-DIST-03 | P1 | S | CR-DEP-01, CR-DIST-03 | grep no `task-unified`; single-hop redirect to `/task` | double-deprecation collapsed |
| 36 | CR-REF-10 | `[src] PROJECT_INDEX.md` (lines 61, 168, 205) | `remove` 3 lines (stale `sc-task-unified-protocol/` + `task-unified.md`) | CS-M4-B; R-RULE-11 | P2 | XS | CR-DEP-03, CR-DEP-04 | grep returns 0 matches | index regeneration won't reintroduce (dirs gone) |
| 37 | CR-REF-11 | `[src] scripts/sync_from_framework.py:84` | `redirect` (remove `→ [/sc:task]` link half from docstring) | CS-M4-B | P2 | XS | CR-DEP-01 | grep returns 0; script output sane | docstring drift |
| 38 | CR-REF-12 | `[.claude] .claude/commands/sc/*.md` + `[.claude] .claude/skills/sc-*-protocol/*` + `[.claude] .claude/templates/documents/release-spec-template.md` | `sync` (refreshed by `make sync-dev` from CR-REF-04 + CR-REF-06 + CR-REF-07) | R-RULE-10 | P0 | XS | CR-REF-04, CR-REF-06, CR-REF-07 | `make verify-sync` returns 0; grep finds no `/sc:task` mirror leakage | R-RULE-10; template path verified vs Makefile target |
| 39 | CR-REF-03 | `[src] src/superclaude/cli/{sprint/config.py:240, sprint/checkpoints.py:28, tasklist/prompts.py:158, roadmap/validate_prompts.py:82+:126}` | `leave-as-is` (false-positive triage — references `/sc:tasklist`, NOT `/sc:task`) | n/a (false-positive) | P3 | XS | (none) | Phase 7 reviewer confirms substring `sc:tasklist`, not `/sc:task` | over-eager regex (mitigated by anchored regex) |
| 40 | CR-REF-13 | `[.claude] .claude/agent-memory/rf-assembler/assembly-patterns.md` | `leave-as-is` (runtime-managed by sub-agents) | CS-M4-B (annotation only) | P3 | XS | (none) | no manual edit; memory regenerates on next sub-agent invocation if needed | stale memory contextual only |

### 1.8 M5-C — Active backlog reference redirects + leave-with-note (P1/P2)

| # | CR-ID | Path (side-tagged) | Change | Manifest feature(s) | Prio | Effort | Deps | Acceptance (digest) | Risk (digest) |
|---|---|---|---|---|---|---|---|---|---|
| 41 | CR-REF-14 | `[.dev] .dev/releases/backlog/{prd,tdd}-artifact-containment/spec.md` | `redirect` (live planning docs) | CS-M4-B | P1 | S | CR-DEP-01 | grep returns 0 matches | live planning prevents new work invoking deprecated cmd |
| 42 | CR-REF-15 | `[.dev] .dev/releases/backlog/v5.xx_release-eval-ab-test/` (5 files) | `leave-with-note` (single deprecation header per file) | CS-M4-B; R-RULE-11 spirit | P2 | XS | CR-DEP-01 | each file has deprecation header; bodies unchanged | annotation only |
| 43 | CR-REF-16 | `[.dev] .dev/releases/backlog/v6.xx_spec-workshop/`, `v5xx-Spec-generator-framework/`, `prd-skill-refactor/` (4–6 files) | `leave-with-note` default; `redirect` per-file if Phase 7 confirms live | CS-M4-B | P2 | XS | CR-DEP-01 | each file annotated (or selectively redirected) | under-classification (mitigated by git-log review per file) |
| 44 | CR-REF-17 | `[.dev] .dev/releases/backlog/v5.xx-sc-troubleshoot-v2/` (2 files) | `leave-with-note` | CS-M4-B | P3 | XS | CR-DEP-01 | header present | none material |
| 45 | CR-REF-18 (cluster, 14 sub-rows) | `[.dev] .dev/releases/backlog/v5.xxforensic/` (14 files, 162 hits) | `leave-with-note` via single `DEPRECATION-NOTE.md` at cluster root | CS-M4-B (high-density); R-RULE-11 | P3 | XS | CR-DEP-01 | `DEPRECATION-NOTE.md` exists at cluster root; no body rewrites in 14 files | over-classification (mitigated: any live file escalates to redirect per CR-REF-15 pattern) |

### 1.9 M5-D — Frozen / archived / not-editable buckets (P3; bucket-level)

| # | CR-ID | Path (side-tagged) | Change | Manifest feature(s) | Prio | Effort | Deps | Acceptance (digest) | Risk (digest) |
|---|---|---|---|---|---|---|---|---|---|
| 46 | CR-REF-BUCKET-A | `[.dev] .dev/releases/backlog/{v3.xx*,v3.8-*,v3.9-*,v4.xx-*,v4xx-*}/` (~39 files) | `leave-as-is` + optional one-time `DEPRECATION-NOTE.md` per top archived dir | CS-M4-B; R-RULE-11 spirit | P3 | S | CR-DEP-01 | either bucket-root notes OR explicit no-op recorded in commit msg | future cleanup PR noise (mitigated by notes) |
| 47 | CR-REF-BUCKET-B | `[.dev] .dev/releases/archive/v3.75-RigorflowMerger-task-unified-v3/` (~33 files) | `leave-as-is` (terminal archive); optional archive-root note | CS-M4-B; R-RULE-11 | P3 | XS | (none) | no body rewrites in archive | archive is read-only history |
| 48 | CR-REF-BUCKET-C | `[.dev] .dev/tasks/to-do/TASK-*/` (~30 files; ~116 hits in re-run) | `leave-as-is` + new-task guidance in `[.dev] .dev/tasks/README.md` | CS-M4-B; **INV-04** | P3 | XS | CR-DEP-01 | README addition exists; **no existing TASK-* body rewritten**; INV-04 sample test on one TASK-* file | **INV-04 load-bearing**: redirect inside TASK body would corrupt MDTM frontmatter |
| 49 | CR-REF-BUCKET-D | `[.dev] .dev/benchmarks/v2.20-baseline/` + `.dev/test-fixtures/` (~30 files) | `leave-as-is` (frozen regression baselines) | CS-M4-B | P3 | XS | (none) | no body rewrites; existing benchmarks/fixtures pass | none — out of scope (benchmark refresh future task) |
| 50 | CR-REF-BUCKET-E | `[venv] .venv/lib/python3.12/site-packages/superclaude/...` (~24–29 files) | `leave-as-is` (frozen pip snapshot; refreshes on `make dev`) | CS-M4-B | P3 | XS | (none) | post-CR-DEP-01..04 + `make dev` re-run: snapshot reflects new state automatically | venv is regenerated state |
| 51 | CR-REF-BUCKET-F | `[.serena] .serena/memories/releases/release-split-workspace-rca-roadmap.md` | `leave-as-is` (serena MCP memory; managed via `write_memory`) | CS-M4-B | P3 | XS | (none) | no manual edit | stale memory contextual only |
| 52 | CR-REF-BUCKET-G | `[.dev] .dev/releases/complete/**` (~446 files, frozen completed-release archives) | `leave-as-is` (R-RULE-11 spirit; terminal archive) | R-RULE-11 | P3 | XS | (none) | `git diff --name-only` post-Phase-7 shows zero `.dev/releases/complete/` paths | R-RULE-11 (no consistency-PR re-litigation) |
| 53 | CR-REF-BUCKET-H | `[.dev] .dev/releases/current/task-sc-task-directional-merge/**` (~95 files, this sprint's own artifacts) | `leave-as-is` (self-referential analysis content; absorbs into G post-archive) | R-RULE-11 | P3 | XS | (none) | `git diff --stat` post-Phase-7 shows zero files in this sprint's artifacts dir modified by redirect commits | over-redirect of analysis content (mitigated by explicit no-op rule) |

### 1.10 M5-E — Hand-edited documentation redirects (P0/P1/P2)

| # | CR-ID | Path (side-tagged) | Change | Manifest feature(s) | Prio | Effort | Deps | Acceptance (digest) | Risk (digest) |
|---|---|---|---|---|---|---|---|---|---|
| 54 | CR-DOC-01 | `[docs] docs/user-guide/commands.md` (1570 lines; 27 hits; primary user-facing catalog) | `redirect` (body + section heading + anchor + cross-link rewrites; remove "Difference from /sc:task" comparison blocks) | CS-M5-B; CR-DEP-01; CR-TASK-02; R-RULE-06 | P0 | L | CR-DEP-01, CR-TASK-02 | anchored grep returns 0; mkdocs build passes; description names declarative `Tier:` (no classifier prose) | R-RULE-11 (LR-REJECT-3) + R-RULE-06 (no two-surface narrative) |
| 55 | CR-DOC-02 | `[docs] docs/user-guide/flags.md:81` (1 hit; section heading) | `redirect` heading + anchor + cross-link updates | CS-M5-B; CR-DEP-01 | P1 | XS | CR-DEP-01 | heading reads `### Task Command Flags (`/task`)`; cross-links resolve | anchor drift (mitigated by same-edit anchor rewrite) |
| 56 | CR-DOC-04 | `[docs] docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (8 hits) | `redirect` body; describe one-surface model post-absorption | CS-M5-B; CR-DEP-01/03/04; CR-TASK-02; ME-9 | P1 | M | CR-DEP-01, CR-DEP-03, CR-TASK-02 | grep returns 0; no `mcp-servers:` / `personas:` re-documented as load-bearing | LR-REJECT-2 + ME-9 |
| 57 | CR-DOC-05 | `[docs] docs/guides/{cli-portify-and-pipeline-runner-guide, sprint-cli-tools-release-guide, roadmap-cli-tools-release-guide, tdd-skill-release-guide, prd-skill-release-guide}.md` (5 files, 27 hits) | `redirect` body; align with CLI runtime (CR-REF-01/02) | CS-M5-B; CR-REF-01 + CR-REF-02 | P1 | M | CR-REF-01, CR-REF-02 | grep returns 0 in all five files | sample CLI output blocks regenerated if presented as transcripts |
| 58 | CR-DOC-03 | `[docs] docs/sprint-cli-deep-dive.md:672` (1 hit) | `redirect` prompt example to `/task`; replace `--compliance strict` reference with `Tier:` semantics | CS-M5-B; CR-DEP-01; CR-TASK-02 | P2 | XS | CR-DEP-01, CR-TASK-02 | grep returns 0; no `--compliance` / `--strategy` flag re-introduced | LR-REJECT-3 (no flag-derived strategy at runtime) |

### 1.11 M5-F — Historical analyses, research, generated docs (P2/P3)

| # | CR-ID | Path (side-tagged) | Change | Manifest feature(s) | Prio | Effort | Deps | Acceptance (digest) | Risk (digest) |
|---|---|---|---|---|---|---|---|---|---|
| 59 | CR-DOC-06 | `[docs] docs/analysis-sc-tasklist.md` (12 hits) | `leave-with-note` (single header) | CS-M5-B; R-RULE-11 spirit | P2 | XS | CR-DEP-01 | header present line 1/2; body unchanged | none |
| 60 | CR-DOC-07 | `[docs] docs/analysis/{bmad,claude-code-best-practice,openclaw,superpowers}-vs-superclaude-comparison.md` (4 files, 11 hits) | `leave-with-note` per file | CS-M5-B; R-RULE-11 spirit | P2 | XS | CR-DEP-01 | each file has header; bodies preserved | none |
| 61 | CR-DOC-08 | `[docs] docs/research/{competitive-landscape-final-report-2026-03-23, competitive-landscape-tasklist-execution-2026, superpowers-vs-superclaude-comparison}.md` (3 files, 6 hits) | `leave-with-note` per file | CS-M5-B; R-RULE-11 spirit | P2 | XS | CR-DEP-01 | each file annotated | none |
| 62 | CR-DOC-09 | `[docs] docs/research/dev-guide-research/*.md` (11 files, ~109 hits) | `leave-with-note` per file (extraction artifacts frozen at extraction time) | CS-M5-B; R-RULE-11 spirit | P3 | S | CR-DEP-01 | 11 files annotated; bodies preserved | R-RULE-11 (no extraction-record rewrites) |
| 63 | CR-DOC-10 | `[docs] docs/generated/contributor-knowledge-base/{architecture-guide,commands-skills-cross-reference,components-guide,visual-architecture-summary}.md` (4 files, 43 hits) | `leave-as-is` (pipeline-regenerated; refresh deferred) | CS-M5-B | P3 | XS | CR-DEP-01..04 | commit msg records deferral; next regenerator refresh emits `/task` | manual edits would create regenerator-vs-disk drift |
| 64 | CR-DOC-11 | `[docs] docs/generated/sprint-cli/{00,03,05,07,09,10}-*.md` + `v3.7-refactor/*.md` + `debates/*.md` (~17 files, ~75 hits) | `leave-as-is` for live sprint-cli pipeline outputs; `leave-with-note` for `v3.7-refactor/` + `debates/` (frozen) | CS-M5-B; R-RULE-11 spirit for v3.7-refactor | P3 | S | CR-DEP-01..04 | live files unchanged (regenerator refresh later); v3.7-refactor / debates files have deprecation header | R-RULE-11 (no v3.7-refactor rewrites) |
| 65 | CR-DOC-12 | `[docs] docs/generated/{cleanup-sc-prefix-reference-index, cleanup-sc-prefix-rename-tasklist, cli-portify-release-guide, tasklist-unwired-components-remediation}.md` (4 files, 25 hits) | `leave-as-is`; commit msg records deferral; demote to `leave-with-note` if regenerator itself deprecated | CS-M5-B | P3 | XS | CR-DEP-01..04 | commit msg present | stale-without-regenerator (mitigated by Phase 7 regenerator-existence check) |

### 1.12 M5-G — Audit closure (P3)

| # | CR-ID | Path (side-tagged) | Change | Manifest feature(s) | Prio | Effort | Deps | Acceptance (digest) | Risk (digest) |
|---|---|---|---|---|---|---|---|---|---|
| 66 | CR-DOC-13 | (audit row over CR-DOC-01..12) | `audit` (R-RULE-11 cross-check on doc rewrites) | R-RULE-11 | P3 | XS | CR-DOC-01..12 | § 4 doc-row audit table holds | R-RULE-11 |
| 67 | CR-DEFER-T06.04 ack | (handoff confirmation row from `refactor-references.md` § 4.G) | `audit` (every CR-REF-DEFER file appears as a CR-DOC row) | T06.03 → T06.04 hand-off | P3 | XS | CR-DOC-01..12 | § 6 coverage check (in `refactor-documentation.md`) holds | hand-off slippage (mitigated by § 6 of the doc-refactor file) |

---

## 2. Roll-up — counts and totals

| Source refactor | Rows | Of which P0 | P1 | P2 | P3 |
|---|---|---|---|---|---|
| `refactor-task-skill.md` (CR-TASK-01..12) | 12 | 4 | 2 | 4 | 2 |
| `refactor-mdtm-frontmatter.md` (CR-FM-01..04) | 4 | 3 | 0 | 0 | 1 |
| `refactor-sctask-deprecation.md` (CR-DEP-01..05) | 5 | 2 | 2 | 1 | 0 |
| `refactor-references.md` (CR-REF-01..18 + CR-REF-BUCKET-A..H) | 25 (17 per-file/cluster + 8 buckets) | 4 (01, 02, 09, 12) | 5 (04, 05, 06, 08, 14) | 5 (07, 10, 11, 15, 16) | 11 (03, 13, 17, 18, BUCKET-A..H) |
| `refactor-distribution.md` (CR-DIST-01..06) | 6 | 1 (02) | 2 (01, 03) | 1 (04) | 2 (05, 06) |
| `refactor-documentation.md` (CR-DOC-01..13) | 13 | 1 (01) | 3 (02, 04, 05) | 4 (03, 06, 07, 08) | 5 (09, 10, 11, 12, 13) |
| **Total** | **65** | **15** | **14** | **15** | **21** |

*(The master ordered table in § 1 enumerates 67 row-line-items; two are audit/handoff acknowledgements grouped under CR-DOC-13 and CR-DEFER-T06.04 ack and are not counted as independent change rows above. The 65-row figure counts independent CR-IDs across the five refactor files; the eight bucket rows count as one CR-REF-BUCKET-A..H aggregate per the source file's vocabulary.)*

---

## 3. Two-way traceability — manifest TU ↔ change rows

### 3.1 Forward (every TU has at least one change row)

| Manifest TU | Source refactor change rows | Confirmed |
|---|---|---|
| TU-1 (`Tier:` field + Gate 1 + per-item marker) | CR-FM-01, CR-FM-02, CR-FM-03, CR-TASK-02, CR-TASK-03 | ✅ |
| TU-2 (Critical/Trivial Path Override) | CR-TASK-01, CR-TASK-04 | ✅ |
| TU-3 (Gate 2 Verification routing widening) | CR-TASK-05 | ✅ |
| TU-4 (D15b Layer 2 pre-flight) | CR-TASK-06 | ✅ |
| TU-5 (TFEP Test baseline snapshot) | CR-TASK-07 | ✅ |
| TU-6 (TFEP Prohibitions + Carve-outs) | CR-TASK-08 | ✅ |
| TU-7 (TFEP Escalation trigger detection) | CR-TASK-09 | ✅ |
| TU-8 (TFEP Incident reporting) | CR-TASK-10 | ✅ |

**Forward coverage: 8/8 TUs mapped. Pass.**

### 3.2 Reverse (every change row traces to a TU OR a derivative responsibility)

| CR-ID family | Trace target | Trace type |
|---|---|---|
| CR-TASK-01..10 | TU-1..TU-8 (one-to-many; see § 3.1) | Direct absorption |
| CR-TASK-11 | R-RULE-10 sync mechanic for CR-TASK-01..10 | Derivative (mechanical) |
| CR-TASK-12 | TU-2/TU-6/TU-7/TU-8 verbatim obligations | Derivative (audit on absorption) |
| CR-FM-01..03 | TU-1 schema (1 new field + per-item marker + INV-04 compat) | Direct absorption |
| CR-FM-04 | INV-04 + R-RULE-11 audit on CR-FM-01..03 + CR-TASK-02/03 | Derivative (audit) |
| CR-DEP-01..04 | Donor artifact disposition consequent on TU-1..TU-8 absorption (CS-M4-A) | Derivative (deprecation) |
| CR-DEP-05 | ME-9 + R-RULE-11 audit on CR-DEP-01 | Derivative (audit) |
| CR-REF-01..02 | CLI runtime alignment with CR-DEP-01 (CS-M4-B) | Derivative (consequence of deprecation) |
| CR-REF-04..07, CR-REF-14 | Live source / live backlog rewrite consequent on CR-DEP-01 (CS-M4-B) | Derivative |
| CR-REF-08 | Plugin stub consequent on CR-DEP-01 + CR-DIST-03 | Derivative |
| CR-REF-09 | Test parity with CR-REF-01/02 | Derivative |
| CR-REF-10, CR-REF-11 | Repo-index + script-doc consequent on CR-DEP-03/04 | Derivative |
| CR-REF-12 | `make sync-dev` mirror refresh for CR-REF-04/06/07 (R-RULE-10) | Derivative (mechanical) |
| CR-REF-03, CR-REF-13, CR-REF-15..17, CR-REF-18 | Annotation / leave-as-is dispositions (CS-M4-B) | Derivative (treatment-only) |
| CR-REF-BUCKET-A..H | Bucket-level dispositions (R-RULE-11 spirit + INV-04 for BUCKET-C) | Derivative (treatment-only) |
| CR-DIST-01..06 | Installer / sync-dev / verify-sync / plugin / README mechanics consequent on CR-DEP-01..04 (CS-M5-A) | Derivative (distribution) |
| CR-DOC-01..05 | User-/developer-guide rewrites consequent on CR-DEP-01 + CR-TASK-02 (CS-M5-B) | Derivative (documentation) |
| CR-DOC-06..09 | Historical analyses annotation (R-RULE-11 spirit) | Derivative (treatment-only) |
| CR-DOC-10..12 | Generated docs deferral (CS-M5-B) | Derivative (regenerator-deferred) |
| CR-DOC-13 | R-RULE-11 audit on CR-DOC-01..12 | Derivative (audit) |

**Reverse coverage: 65/65 change rows trace to a TU or to a named derivative (deprecation / distribution / documentation / mechanical sync / audit) responsibility. Pass.**

**Two-way traceability complete:** 8 TUs ↔ {CR-TASK-01..10, CR-FM-01..03} (direct absorption); {CR-DEP-01..05, CR-DIST-01..06, CR-DOC-01..13, CR-REF-01..18, CR-REF-BUCKET-A..H} = derivative consequences of absorption. **No orphan rows. No unimplemented TUs.**

---

## 4. R-RULE-11 audit — no `rejected-features-ledger.md` entry re-proposed

Per T06.05 governing R-RULE-11, the consolidated plan may not silently re-propose a REJECT or DEFER entry. Per-source-file audits in T06.01 (§ 7), T06.02 (§ 4 of `refactor-task-skill.md` + § 3.4 of `refactor-mdtm-frontmatter.md`), T06.03 (§ 5 of `refactor-sctask-deprecation.md` + § 3 of `refactor-references.md`), and T06.04 (§ 4 of `refactor-distribution.md` + § 4 of `refactor-documentation.md`) all individually confirm zero re-proposals. This file's cross-cutting audit:

| Ledger entry | Status | Aggregate audit verdict |
|---|---|---|
| LR-REJECT-1 / LR-REJECT-2 (D02 / Layer A — `mcp-servers:` advertisement, ME-9 binding) | REJECTed | **Pass.** CR-DEP-01 + CR-DEP-05 + CR-DIST-03 + CR-DOC-04 all explicitly **remove** or **do not re-introduce** the advertisement. No change row in any of the five refactor files authors `mcp-servers:` content. |
| LR-REJECT-3 / Row 21 (D09b — runtime classifier with priority cascade + keyword tables) | REJECTed | **Pass.** CR-TASK-02 (Gate 1) reads `Tier:` declaratively from frontmatter; CR-DOC-01 + CR-DOC-04 + CR-REF-05 require the doc/orchestrator rewrites to name declarative `Tier:` semantics, not classifier prose. CR-DOC-03 forbids `--compliance` / `--strategy` re-introduction. |
| LR-REJECT-4 (Gate 5 — user-toggleable override flags) | REJECTed | **Pass.** CR-TASK-01's override is path-glob-keyed, not flag-keyed. No CR-* row authors a `--strict` / `--explain` flag. |
| LR-REJECT-5 / LR-REJECT-6 / LR-REJECT-8 / LR-REJECT-9 (D03 / D13 / D06 / D04 — persona auto-activation, auto-suggest keywords, auto-trigger heuristics, Strategy axis) | REJECTed | **Pass.** No CR-* row authors persona auto-activation, prompt-scanning, or a Strategy axis. CR-DOC-03 forbids `--strategy systematic` re-introduction. |
| LR-REJECT-7 (D15c — per-tier procedure synthesis at execute-time) | REJECTed | **Pass.** CR-TASK-06 is anchored at *First Item Protocol* (pre-loop), never authors per-item runtime steps (ME-5 binding). |
| LR-REJECT-10 / -11 / -12 / -13 / -14 / -15 / -16 / -17 (D05 / D07 / D11 / D12 / D28 / D29 / D30 / D31 — escalation philosophy / CLI flags / few-shot / will-blocks / worked examples / metrics) | REJECTed | **Pass.** No CR-* row authors any of these donor ceremonies. |
| LR-DEFER-1 / -3 (cluster-as-written aggregates) | DEFERRED | **Pass.** Only the absorbable subset (TU-1/TU-3/TU-5..TU-8) lands per the manifest; CR-* rows do not import wholesale clusters. |
| LR-DEFER-2 (D27 / Gate 3 — per-tier MCP matrix) | DEFERRED | **Pass.** No CR-* row authors a per-tier MCP advertisement; CR-DEP-01 + CR-DEP-05 explicitly remove the donor's `mcp-servers:` line. |
| LR-DEFER-4 (D01 — `allowed-tools:` enforcement, ME-8 binding) | DEFERRED | **Pass.** CR-FM-04 audit confirms `allowed-tools:` not added by CR-FM-01..03; CR-DEP-01 collapses `allowed-tools:` on the stub; CR-DOC-* rows do not announce enforcement. |
| LR-DEFER-5 (D08 — classification header emission, ME-7 binding) | DEFERRED | **Pass.** CR-FM-04 confirms no `## Classification:` header emit; no CR-DOC-* row documents header emission. |
| LR-DEFER-6 (D23 — six-step flow / heading insert / resume-from-inserted) | DEFERRED | **Pass.** CR-TASK-10 writes a side-effect FILE (`research/tfep-incident-report.md`); no heading inserted into task file; INV-05 + F4 preserved. |
| LR-DEFER-7 / -8 / -9 (D14 / D26 / D32 — confidence display bar / feedback calibration / external YAML refs) | DEFERRED | **Pass.** No CR-* row touches any of these surfaces. |

**Aggregate audit verdict:** zero `rejected-features-ledger.md` entries re-proposed across **all 65 change rows in the five refactor files**. R-RULE-11 holds at the consolidated level. (Per-source audits in T06.01–T06.04 individually concur.)

---

## 5. Consolidated dependency graph (acyclic)

The graph below merges the per-area dependency tables in the five refactor files into one. Solid arrows are build-order (must-precede) edges; double-headed `↔` arrows are ship-together (atomic-merge) obligations.

```text
                    ┌────────────────────────────────────────────────────────────────────┐
                    │  M1 — FOUNDATION (atomic merge per ME-6 + CR-7 + CR-9)             │
                    │                                                                    │
                    │   CR-FM-01 (Tier: field) ↔ CR-FM-02 (inline marker) ↔ CR-FM-03    │
                    │   (compat default; INV-04)                                         │
                    │       │                                                            │
                    │       ▼                                                            │
                    │   CR-TASK-01 (path_override_check) ───► CR-TASK-02 (Gate 1 PRE)   │
                    │       │                                       │                    │
                    │       │                                       ▼                    │
                    │       │                                  CR-TASK-03 (per-item read)│
                    │       │                                                            │
                    │       ▼                                                            │
                    │   CR-TASK-04 (Gate 2 override read at row 10 — CR-8)               │
                    └────────────┬───────────────────────────────────────────────────────┘
                                 │
                ┌────────────────┼────────────────────────────────────────┐
                ▼                ▼                                        ▼
        ┌──────────────┐  ┌──────────────────┐                ┌─────────────────────┐
        │ CR-TASK-05   │  │ CR-TASK-06       │                │   (CR-TASK-07 lives │
        │ Gate 2       │  │ First-Item       │                │   in M3 below; gated│
        │ widening     │  │ pre-flight       │                │   by Tier; ordered  │
        │ (M2)         │  │ (M2)             │                │   AFTER CR-TASK-06) │
        └──────────────┘  └─────────┬────────┘                └─────────────────────┘
                                    │
                                    ▼
                    ┌────────────────────────────────────────────────────┐
                    │  M3 — TFEP CLUSTER (DM-7 + DM-9 internal ordering) │
                    │                                                    │
                    │   CR-TASK-07 (baseline)                            │
                    │      │                                             │
                    │      │   CR-TASK-08 (prohibitions + carve-outs)    │
                    │      │      │                                      │
                    │      ▼      ▼                                      │
                    │   CR-TASK-09 (escalation classification)           │
                    │      │                                             │
                    │      ▼                                             │
                    │   CR-TASK-10 (incident-report side-effect FILE)    │
                    └────────────────────┬───────────────────────────────┘
                                         │
                                         ▼
                    ┌────────────────────────────────────────────────────┐
                    │  M-sync — mechanical sync + audits                 │
                    │                                                    │
                    │   CR-TASK-11 (make sync-dev → [.claude])           │
                    │   CR-FM-04   (closed-enum + INV-04 audit)          │
                    │   CR-TASK-12 (six verbatim donor diffs)            │
                    └────────────────────┬───────────────────────────────┘
                                         │
                                         ▼  (absorption-must-precede-deprecation)
                    ┌────────────────────────────────────────────────────────────────┐
                    │  M4 — /sc:task DEPRECATION                                     │
                    │                                                                │
                    │   CR-DEP-01 (soft-deprecate commands/task.md)                  │
                    │     │                                                          │
                    │     ▼                                                          │
                    │   CR-DEP-02 (sync mirror)                                      │
                    │     │                                                          │
                    │     ▼                                                          │
                    │   CR-DEP-03 (hard-delete sc-task-protocol/SKILL.md) ◄──┐       │
                    │     │                                                  │       │
                    │     ▼                                                  │       │
                    │   CR-DEP-04 (hard-delete __init__.py + rmdir) ◄────────┼──► CR-DIST-02
                    │     │                                                  │       │  (sync-dev
                    │     │ (ME-9 audit on CR-DEP-01 — same commit)          │       │   orphan-prune;
                    │     ▼                                                  │       │   ship-together
                    │   CR-DEP-05 (audit advertisement removal)              │       │   atomic w/
                    │                                                        │       │   CR-DEP-03/04)
                    │   ── distribution-side audits run in parallel ─────────┴──► CR-DIST-01
                    │                                                                │  (installer test)
                    │                                                              CR-DIST-04
                    │                                                                │  (verify-sync audit)
                    └────────────────────────────┬───────────────────────────────────┘
                                                 │
                                                 ▼
                    ┌────────────────────────────────────────────────────────────────┐
                    │  M5 — DISTRIBUTION + REFERENCES + DOCS                         │
                    │                                                                │
                    │   M5-A: CR-DIST-03 (plugin stub redirect) ←── CR-REF-08        │
                    │         CR-DIST-05 (README no-op audit)                        │
                    │         CR-DIST-06 (R-RULE-11 audit over CR-DIST)              │
                    │                                                                │
                    │   M5-B: CR-REF-01 + CR-REF-02 + CR-REF-09 (CLI + tests)        │
                    │            ──► CR-REF-12 (sync-dev refreshes mirrors of        │
                    │                            CR-REF-04 + CR-REF-06 + CR-REF-07)  │
                    │         CR-REF-04, CR-REF-05, CR-REF-06, CR-REF-07,            │
                    │         CR-REF-10, CR-REF-11, CR-REF-13, CR-REF-03             │
                    │                                                                │
                    │   M5-C: CR-REF-14 (live backlog redirect)                      │
                    │         CR-REF-15, CR-REF-16, CR-REF-17, CR-REF-18             │
                    │            (leave-with-note on active backlog)                 │
                    │                                                                │
                    │   M5-D: CR-REF-BUCKET-A..H (frozen / archived /                │
                    │            self-referential / venv / serena — leave-as-is)     │
                    │                                                                │
                    │   M5-E: CR-DOC-01 (user-guide commands.md — atomic w/          │
                    │            CR-DEP-01 + CR-TASK-02)                             │
                    │         CR-DOC-02, CR-DOC-04, CR-DOC-05, CR-DOC-03             │
                    │                                                                │
                    │   M5-F: CR-DOC-06..09 (leave-with-note historical)             │
                    │         CR-DOC-10..12 (leave-as-is regenerator-deferred)       │
                    │                                                                │
                    │   M5-G: CR-DOC-13 (R-RULE-11 audit over CR-DOC)                │
                    │         CR-DEFER-T06.04 ack (handoff confirmation)             │
                    └────────────────────────────────────────────────────────────────┘
```

**Critical cross-area dependency edges (the edges that bind multiple refactor files):**

| From → To | Edge type | Rationale | Source files crossed |
|---|---|---|---|
| CR-TASK-01..10, CR-FM-01..03 → CR-DEP-01 | absorption-must-precede-deprecation | Cannot soft-deprecate `/sc:task` until `/task` carries every absorbed pattern (T06.02 → T06.03; CS-M4-A rule). | task-skill + mdtm-frontmatter → sctask-deprecation |
| CR-DEP-03 + CR-DEP-04 ↔ CR-DIST-02 | atomic ship-together | `make verify-sync` fails between `[src]` delete and `[.claude]` prune absent atomicity. | sctask-deprecation ↔ distribution |
| CR-DEP-01 → CR-REF-01, CR-REF-02 | runtime-CLI alignment | CLI redirects must not claim `/task` is canonical until the deprecation stub exists for `/sc:task`. | sctask-deprecation → references |
| CR-REF-01 + CR-REF-02 ↔ CR-REF-09 | test-parity ship-together | Test assertions break `make test` if redirects ship without test updates. | references (self) |
| CR-REF-04 + CR-REF-06 + CR-REF-07 → CR-REF-12 | sync-mechanical | `[.claude]` mirrors refreshed by `make sync-dev` after `[src]` edits. | references (self) |
| CR-DEP-01 → CR-DIST-03 | redirect-language alignment | Plugin stub must use the same deprecation language as CR-DEP-01's stub. | sctask-deprecation → distribution |
| CR-DEP-01 + CR-TASK-02 → CR-DOC-01 | atomic announcement | User-guide must not describe `/task` as canonical (with Gate 1 + `Tier:`) before the recipient skill carries the behavior. | sctask-deprecation + task-skill → documentation |
| CR-REF-08 ↔ CR-DIST-03 | shared-target alignment | Same `plugins/superclaude/commands/task.md` rewrite — references row stakes scope, distribution row authors the eight-column directive. | references ↔ distribution |
| CR-REF-DEFER-T06.04 → CR-DOC-01..12 | handoff alignment | Every doc file deferred from references → documentation has a corresponding CR-DOC row (verified in § 5 of `refactor-documentation.md`). | references → documentation |
| CR-DEP-03 + CR-DEP-04 → CR-REF-10 | accurate-index-post-delete | PROJECT_INDEX.md only becomes correct after the donor directory is gone. | sctask-deprecation → references |

**Acyclicity check.** Treating the graph as a DAG with vertices = CR-IDs (or aggregated bucket rows) and edges = explicit dependencies enumerated in the five refactor files + the cross-area table above: a topological sort exists. Recommended canonical order is the row sequence in § 1.1–§ 1.12 (lines 1 through 67). No back-edge from a later row to an earlier row appears in any source file's dependency column. **Graph is acyclic. Pass (T06.05 AC #2 + § 5 verification).**

---

## 6. Recommended Phase 7 execution order (canonical commit sequence)

The order below is the recommended Phase 7 commit sequence. Each step lists the rows that ship together in one commit; the sequence respects every dependency edge in § 5 and the absorption→deprecation→distribution→documentation rule from `merge-roadmap.md` § 4 + § 2.

### Step 1 — M1 atomic-merge commit (P0)
- **Rows:** CR-FM-01, CR-FM-02, CR-FM-03, CR-TASK-01, CR-TASK-02, CR-TASK-03, CR-TASK-04.
- **Pre-commit gate:** `uv run pytest` passes on the recipient surface; `make verify-sync` returns 0 after the in-commit `make sync-dev`.
- **Rationale:** ME-6 + CR-7 + CR-9 ship-together obligation; splitting reopens the wrong-stance-dispatch window at runtime row 1.

### Step 2 — M2 commits (P1; M2 rows can interleave)
- **Rows:** CR-TASK-05 (Gate 2 widening), CR-TASK-06 (First-Item pre-flight).
- **Order between them is free.** Both depend on M1 only.

### Step 3 — M3 TFEP cluster (P2; internal DM-7 / DM-9 ordering)
- **Order (one or multiple commits):** CR-TASK-07 → CR-TASK-08 → CR-TASK-09 → CR-TASK-10.
- **Note:** CR-TASK-07 + CR-TASK-08 can interleave (TU-6 is independent of TU-5 per DM-8); CR-TASK-09 strictly depends on both at row 8; CR-TASK-10 caps the cluster at row 11.

### Step 4 — M-sync + audits (P3)
- **Rows:** CR-TASK-11 (`make sync-dev`), CR-FM-04 (closed-enum + INV-04 audit), CR-TASK-12 (six verbatim diffs).
- **Gate:** all three pass; commit blocked otherwise.

### Step 5 — M4-A commit: `/sc:task` soft-deprecation (P0, ME-9 audit included)
- **Rows:** CR-DEP-01, CR-DEP-02 (atomic in same commit so `make verify-sync` stays green), CR-DEP-05 (audit included in the commit message).
- **In the same commit, the M5-B P0 redirects MUST land too** so end-users running the CLI don't see "skill not found":
  - **Atomic add to Step 5:** CR-REF-01, CR-REF-02, CR-REF-09, plus the `make sync-dev` refresh of any mirrors touched by CR-DEP-01 (already covered by CR-DEP-02 for `commands/`).

### Step 6 — M4-B + M5-A coupled commit: hard-deprecation + sync-rule + plugin (P0/P1)
- **Rows:** CR-DEP-03 + CR-DEP-04 + **CR-DIST-02** (atomic in same commit; without atomicity `make verify-sync` fails between `[src]` delete and `[.claude]` prune), plus CR-DIST-01 (installer regression test) + CR-DIST-04 (verify-sync audit) follow in the same or immediately-following commit. CR-REF-10 (PROJECT_INDEX.md) joins this commit because the index is accurate only after the directory is gone.
- **CR-DIST-03 (plugin stub) + CR-REF-08** can land in this commit or the next (P1).

### Step 7 — M5-B remaining redirects + M5-C live backlog (P1/P2)
- **Rows:** CR-REF-04, CR-REF-05, CR-REF-06, CR-REF-07, CR-REF-11, CR-REF-14 + CR-REF-12 (`make sync-dev` mirror refresh of these `[src]` edits) all in one (or a small number of) commits.
- **R-RULE-10 gate:** `make verify-sync` returns 0 before commit.
- **CR-DIST-05 (README no-op audit)** and **CR-DIST-06 (R-RULE-11 audit)** also land here.

### Step 8 — M5-E: doc redirects (P0/P1/P2)
- **Atomic with Step 5 announcement OR follow-on commit:** CR-DOC-01 (user-guide commands.md) MUST land in the same commit as (or after) CR-DEP-01 + CR-TASK-02 — the user-guide must not describe `/task` as canonical before the recipient skill carries Gate 1 + `Tier:`.
- **Same/next commit:** CR-DOC-02, CR-DOC-04, CR-DOC-05, CR-DOC-03.
- **Doc-site build gate:** `mkdocs build` (or equivalent) returns 0 broken-link warnings.

### Step 9 — M5-C/M5-D/M5-F annotation pass (P2/P3)
- **Rows (single bundled commit recommended for ease of revert):** CR-REF-15, CR-REF-16, CR-REF-17, CR-REF-18, CR-DOC-06, CR-DOC-07, CR-DOC-08, CR-DOC-09, CR-DOC-11 (v3.7-refactor + debates portion only).
- **Buckets explicitly NOT touched** in this commit (recorded for traceability): CR-REF-BUCKET-A, B, C, D, E, F, G, H — all `leave-as-is`. (CR-REF-BUCKET-C also gets the new-task guidance edit in `.dev/tasks/README.md` per its row.)

### Step 10 — Audit closure + regenerator-deferral note (P3)
- **Rows:** CR-DOC-10, CR-DOC-11 (sprint-cli live portion — `leave-as-is`), CR-DOC-12 — commit message records "docs/generated/*: refresh deferred to next regenerator run".
- **Final audit row:** CR-DOC-13 (R-RULE-11 audit over CR-DOC-01..12).
- **Handoff confirmation:** CR-DEFER-T06.04 ack — § 5 coverage check in `refactor-documentation.md` confirms every CR-REF-DEFER-T06.04 file has a CR-DOC-NN row.

---

## 7. Acceptance criteria recap (T06.05)

| T06.05 AC | Satisfied where |
|---|---|
| **AC #1** — `merge-master.md` exists with every change row from the five refactor files consolidated into one ordered table. | § 1 — 12 sub-sections § 1.1–§ 1.12; **67 row-line-items consolidating 65 distinct CR-IDs** from refactor-task-skill (CR-TASK-01..12), refactor-mdtm-frontmatter (CR-FM-01..04), refactor-sctask-deprecation (CR-DEP-01..05), refactor-references (CR-REF-01..18 + CR-REF-BUCKET-A..H), refactor-distribution (CR-DIST-01..06), refactor-documentation (CR-DOC-01..13). All carry the same eight columns (or one-line digest pointing at the source refactor file for the binding text). |
| **AC #2** — A single acyclic dependency graph and a recommended execution order are present. | § 5 (ASCII graph with explicit ship-together / build-order edges + cross-area edge table; acyclicity check) + § 6 (10-step canonical commit sequence). |
| **AC #3** — Every `transfer-manifest.md` feature maps to at least one change row; every change row traces to a manifest feature OR a derivative responsibility. | § 3.1 (forward: 8/8 TUs mapped) + § 3.2 (reverse: 65/65 CR-IDs trace to a TU or to a named derivative deprecation/distribution/documentation/sync/audit responsibility). Two-way traceability complete. |
| **AC #4** — Execution order sequences `/task` absorption before `/sc:task` deprecation before distribution/doc changes. | § 6 — Step 1 (M1 absorption) → Steps 2–4 (M2/M3/M-sync continued absorption + audits) → Step 5 (M4-A soft-deprecation) → Step 6 (M4-B hard-deprecation + atomic CR-DIST-02) → Steps 7–9 (M5 distribution + references + docs) → Step 10 (audit closure). Absorption strictly precedes deprecation; deprecation strictly precedes distribution/doc changes. |

---

## 8. Validation hooks (T06.05 Validation block)

**Sub-agent verification:** § 5's dependency-graph claim (acyclic) and § 3's two-way traceability claim (every TU mapped both directions) are independently verifiable by an `Explore` or `general-purpose` sub-agent running the following checks (binding text is in the source refactor files, not paraphrased here):

1. **Acyclicity check.** For each CR-ID in § 1.1–§ 1.12, follow its Dependencies column to source rows. Confirm no chain returns to the starting CR-ID. (Mechanical: 65 rows × ≤6 deps each ≈ ≤390 edges; tractable by hand or `tsort`.)
2. **Forward traceability check.** For each TU-1..TU-8, confirm at least one CR-ID in § 1.1–§ 1.4 lists it in the Manifest feature(s) column. Pre-computed in § 3.1 (8/8 ✅).
3. **Reverse traceability check.** For each CR-ID, confirm its Manifest feature(s) column lists at least one TU-N OR a derivative responsibility (CS-M-N / R-RULE-NN / CR-rule). Pre-computed in § 3.2 (65/65 ✅).
4. **R-RULE-11 audit.** For each of the 17 REJECT + 9 DEFER entries in `rejected-features-ledger.md`, confirm no CR-ID's Change column re-introduces the rejected pattern. Pre-computed in § 4 (zero re-proposals across 26 ledger entries ✅).
5. **Order-respect check.** For the 10-step sequence in § 6, confirm each step's dependency edges all originate in earlier steps. Pre-computed implicitly by the step ordering; explicit reviewer spot-check recommended on the cross-area edges in § 5's table.

**Manual reviewer check (T06.05 Validation #2):** the recommended execution order in § 6 is dependency-consistent — every "must-precede" edge in § 5 lands the upstream CR-ID in an earlier step than the downstream CR-ID. Spot-checked: CR-TASK-01..10 + CR-FM-01..03 (Steps 1–3) all precede CR-DEP-01 (Step 5); CR-DEP-03/04 + CR-DIST-02 (Step 6) precede CR-DIST-03 (Step 6+) and CR-DOC-* (Step 8); CR-REF-12 sync (Steps 5 + 7) follows the `[src]` edits in each case.

---

## 9. Deliverable handoff to Phase 7

`merge-master.md` is the binding execution index for Phase 7. The five refactor files remain the authoritative source for the binding eight-column text per change row; this file gives the consolidated ordering, the merged dependency graph, the canonical 10-step commit sequence, and the cross-row R-RULE-11 audit.

**Phase 7 obligations carried forward:**
- Every `[src]` edit precedes its `[.claude]` mirror; `make verify-sync` returns 0 before every commit (R-RULE-10).
- Every commit message that touches a CR-DEP / CR-DIST / CR-DOC / CR-REF row cites the CR-ID(s) it implements (auditability).
- The atomic-merge obligations in Steps 1 + 5 + 6 are hard requirements (ME-6 + CR-7 + CR-9 + R-RULE-10).
- The six verbatim donor blocks (CR-TASK-12) must `diff` cleanly before any commit lands a CR-TASK-01/-08/-09/-10 edit.
- No CR-* row may silently re-litigate a `rejected-features-ledger.md` entry; if Phase 7 encounters a tempting "consistency" rewrite that re-introduces a REJECTed pattern, it stops and routes the question back to a new sprint (R-RULE-11 binding).

**T06.05 deliverable: COMPLETE.** Phase 6 closes with a single consolidated execution plan: **65 change rows, 10 canonical commit steps, one acyclic dependency graph, two-way traceability against 8 manifest TUs, zero ledger re-proposals.** Phase 7 has a binding, file-verified, fully traceable merge plan as input.
