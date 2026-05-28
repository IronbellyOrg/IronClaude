# Refactor Plan — Documentation (Phase 6 / T06.04)

**Task:** T06.04 — Refactor plans: distribution surface & documentation
**Roadmap Item:** R-022
**Tier:** STRICT
**Generated:** 2026-05-15
**Status:** Driving input for Phase 7 execution. Every change row is an eight-column directive that Phase 7 will translate into a concrete doc-body edit, an annotation header insertion, or a regenerator-run record. Doc rows are mostly hand-edit `redirect` rows for live user/developer docs, `leave-with-note` for historical analyses, and `leave-as-is` + regenerator-update guidance for pipeline-generated docs.

**Inputs (1:1 referenced):**
- `transfer-manifest.md` (T05.03) — TU-1..TU-8, ME-1..ME-9.
- `merge-roadmap.md` (T06.01) — milestone **M5** / CS-M5-B (documentation refresh).
- `refactor-sctask-deprecation.md` (T06.03) — soft/hard deprecation decisions; doc rows below cite the canonical post-deprecation surface (`/task`) and the standard redirect language.
- `refactor-task-skill.md` (T06.02) — CR-TASK-02 names the `Tier:` field and Gate 1 dispatch behavior that user-guide / developer-guide docs must describe correctly post-merge.
- `refactor-references.md` (T06.03 companion) § 4.G + § 8 — explicit ≈40-file doc hand-off list, partitioned into hand-edited / regenerated / historical buckets.
- `refactor-distribution.md` (this task's first deliverable) — owns the README and the installer/sync/plugin rows; this file owns the `docs/` tree.
- `[src] docs/user-guide/commands.md` (auggie-verified, 1570 lines; 27 grep matches for `sc:task|sc-task-protocol|task-unified`).
- `[src] docs/user-guide/flags.md` (auggie-verified, 272 lines; 1 match: line 81 section heading `### Task Command Flags (`/sc:task`)`).
- `[src] docs/sprint-cli-deep-dive.md` (auggie-verified, 1629 lines; 1 match: line 672 prompt example `/sc:task-unified Execute all tasks in @<phase_file>`).
- `[src] docs/guides/` (6 files with matches: cli-portify-and-pipeline-runner-guide.md (15), sprint-cli-tools-release-guide.md (4), roadmap-cli-tools-release-guide.md (6), tdd-skill-release-guide.md (1), prd-skill-release-guide.md (1), SuperClaude-Developer-Guide-Commands-Skills-Agents.md (8)).
- `[src] docs/analysis/` (4 files with matches: bmad (2), claude-code-best-practice (1), openclaw (2), superpowers (6); plus `docs/analysis-sc-tasklist.md` (12)).
- `[src] docs/research/` (3 files at top level: competitive-landscape-final-report-2026-03-23 (4), competitive-landscape-tasklist-execution-2026 (1), superpowers-vs-superclaude (1)) and `docs/research/dev-guide-research/` (10 files with matches; high-hit subset: extract-haiku-12-skills-multi (24), extract-haiku-15-commands-examples (29), extract-opus-15-commands-examples (28), extract-opus-08-commands-core (10)).
- `[src] docs/generated/` (≈30 files with matches; pipeline-emitted, refreshed by regenerator scripts).

**Companion artifact:** `refactor-distribution.md` — owns the installer code paths, sync rules, plugin stub, and README. This file does **not** re-author those rows.

**Scope boundary:**
- This file covers every doc body (excluding README) that names `/sc:task`, `sc:task-protocol`, `task-unified`, or the two-surface model `/task` ↔ `/sc:task`.
- Pure `/sc:tasklist` references (the substring `sc:task` inside `sc:tasklist`) are NOT in scope — `/sc:tasklist` is a different command, not deprecated. The redirect regex anchors guard against the false-positive (see § 2).
- This refactor does **not** re-litigate any `rejected-features-ledger.md` REJECT/DEFER entry (cross-checked in § 4).

---

## 0. Side-tagging convention (R-RULE-10)

Documentation under `docs/` is **hand-edited or regenerated**, not synced via `make sync-dev`. The `docs/` tree has no `[.claude]` mirror counterpart, so all paths below carry `[src]` (the canonical edit target — `docs/...` under the repo root). One exception: `docs/generated/` paths are `[src]` for the on-disk file but conceptually `[regen]` because their source-of-truth is the regenerator script (the file should not be hand-edited; instead the regenerator emits an updated version when re-run).

**Auggie-verification of every operative path.** § 0.1 lists every file enumerated by row below with its grep-match count (verified 2026-05-15) as the basis for the per-row dispositions.

### 0.1 File inventory (auggie-verified grep counts, 2026-05-15)

The grep regex used: `'sc:task|sc-task-protocol|task-unified'`. Files with zero matches are not enumerated (they are already aligned with the post-merge state).

**Hand-edited live docs (`redirect` candidates):**

| # | Path | Hits | Bucket |
|---|---|---|---|
| 1 | `docs/user-guide/commands.md` | 27 | user-guide (highest-density) |
| 2 | `docs/user-guide/flags.md` | 1 | user-guide |
| 3 | `docs/sprint-cli-deep-dive.md` | 1 | root-level deep-dive |
| 4 | `docs/guides/cli-portify-and-pipeline-runner-guide.md` | 15 | guides |
| 5 | `docs/guides/sprint-cli-tools-release-guide.md` | 4 | guides |
| 6 | `docs/guides/roadmap-cli-tools-release-guide.md` | 6 | guides |
| 7 | `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | 8 | guides (developer) |
| 8 | `docs/guides/tdd-skill-release-guide.md` | 1 | guides |
| 9 | `docs/guides/prd-skill-release-guide.md` | 1 | guides |

**Historical analyses (`leave-with-note` candidates):**

| # | Path | Hits | Bucket |
|---|---|---|---|
| 10 | `docs/analysis-sc-tasklist.md` | 12 | analysis (top-level) |
| 11 | `docs/analysis/bmad-vs-superclaude-comparison.md` | 2 | analysis |
| 12 | `docs/analysis/claude-code-best-practice-vs-superclaude.md` | 1 | analysis |
| 13 | `docs/analysis/openclaw-vs-superclaude-comparison.md` | 2 | analysis |
| 14 | `docs/analysis/superpowers-vs-superclaude-comparison.md` | 6 | analysis |
| 15 | `docs/research/competitive-landscape-final-report-2026-03-23.md` | 4 | research |
| 16 | `docs/research/competitive-landscape-tasklist-execution-2026.md` | 1 | research |
| 17 | `docs/research/superpowers-vs-superclaude-comparison.md` | 1 | research |

**Research extraction artifacts (`leave-with-note` bucket; many high-hit files):**

| # | Path (or subset) | Hits | Bucket |
|---|---|---|---|
| 18 | `docs/research/dev-guide-research/00-file-inventory.md` | 2 | research-extract |
| 19 | `docs/research/dev-guide-research/extract-haiku-08-commands-core.md` | 3 | research-extract |
| 20 | `docs/research/dev-guide-research/extract-haiku-09-orchestrator-core.md` | 2 | research-extract |
| 21 | `docs/research/dev-guide-research/extract-haiku-12-skills-multi.md` | 24 | research-extract (high) |
| 22 | `docs/research/dev-guide-research/extract-haiku-15-commands-examples.md` | 29 | research-extract (high) |
| 23 | `docs/research/dev-guide-research/extract-opus-06-advanced-patterns.md` | 1 | research-extract |
| 24 | `docs/research/dev-guide-research/extract-opus-08-commands-core.md` | 10 | research-extract |
| 25 | `docs/research/dev-guide-research/extract-opus-09-orchestrator-core.md` | 1 | research-extract |
| 26 | `docs/research/dev-guide-research/extract-opus-12-skills-multi.md` | 8 | research-extract |
| 27 | `docs/research/dev-guide-research/extract-opus-15-commands-examples.md` | 28 | research-extract (high) |
| 28 | `docs/research/dev-guide-research/extract-opus-20-roadmap-v2-spec.md` | 1 | research-extract |

**Pipeline-generated docs (`leave-as-is` + regenerator-update guidance):**

| # | Path (or subset) | Hits | Bucket |
|---|---|---|---|
| 29 | `docs/generated/cleanup-sc-prefix-reference-index.md` | 11 | generated |
| 30 | `docs/generated/cleanup-sc-prefix-rename-tasklist.md` | 7 | generated |
| 31 | `docs/generated/cli-portify-release-guide.md` | 6 | generated |
| 32 | `docs/generated/tasklist-unwired-components-remediation.md` | 1 | generated |
| 33 | `docs/generated/contributor-knowledge-base/architecture-guide.md` | 2 | generated |
| 34 | `docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md` | 21 | generated (high) |
| 35 | `docs/generated/contributor-knowledge-base/components-guide.md` | 2 | generated |
| 36 | `docs/generated/contributor-knowledge-base/visual-architecture-summary.md` | 18 | generated (high) |
| 37 | `docs/generated/sprint-cli/00-overview.md` | 3 | generated |
| 38 | `docs/generated/sprint-cli/03-execution-engine.md` | 1 | generated |
| 39 | `docs/generated/sprint-cli/05-pm-agent.md` | 4 | generated |
| 40 | `docs/generated/sprint-cli/07-skills-commands.md` | 20 | generated (high) |
| 41 | `docs/generated/sprint-cli/09-wiring-validation.md` | 5 | generated |
| 42 | `docs/generated/sprint-cli/10-critique-validation.md` | 4 | generated |
| 43 | `docs/generated/sprint-cli/v3.7-refactor/chunk-03-naming-consolidation.md` | 15 | generated (v3.7-frozen) |
| 44 | `docs/generated/sprint-cli/v3.7-refactor/chunk-05-cross-cutting.md` | 2 | generated (v3.7-frozen) |
| 45 | `docs/generated/sprint-cli/v3.7-refactor/context-01-path-a-deficiencies.md` | 1 | generated (v3.7-frozen) |
| 46 | `docs/generated/sprint-cli/v3.7-refactor/context-03-v37-spec-gap-analysis.md` | 3 | generated (v3.7-frozen) |
| 47 | `docs/generated/sprint-cli/v3.7-refactor/MERGED-REFACTORING-RECOMMENDATION.md` | 6 | generated (v3.7-frozen) |
| 48 | `docs/generated/sprint-cli/v3.7-refactor/spec-gen-prompt-architect.md` | 12 | generated (v3.7-frozen) |
| 49 | `docs/generated/sprint-cli/v3.7-refactor/spec-gen-prompt-incremental.md` | 3 | generated (v3.7-frozen) |
| 50 | `docs/generated/sprint-cli/v3.7-refactor/spec-gen-prompt-qa.md` | 1 | generated (v3.7-frozen) |
| 51 | `docs/generated/sprint-cli/v3.7-refactor/spec-gen-adversarial/merged-spec-gen-prompt.md` | 12 | generated (v3.7-frozen) |
| 52 | `docs/generated/sprint-cli/debates/debate-file-preloading.md` | 1 | generated (frozen debate) |
| 53 | `docs/generated/sprint-cli/debates/debate-strict-halt.md` | 1 | generated (frozen debate) |

**Grand total: 53 files with at least one match.** Every file above carries a treatment in § 3. § 4.G of `refactor-references.md` listed ≈40 files; the auggie re-verification at T06.04 generation expanded the list to 53 (the additional 13 are mostly research-extract files that were under-counted in the T06.03 bucket).

---

## 1. Column legend (every row carries all eight columns — T06.04 AC #2 + AC #4)

| Column | Meaning |
|---|---|
| **CR-ID** | Stable change-row identifier (`CR-DOC-NN` for per-file or per-cluster rows). |
| **File path (side-tagged)** | `[src] docs/...` — every operative path. |
| **Change** | The disposition: `redirect` (rewrite body strings `/sc:task` → `/task`); `leave-with-note` (prepend a single-line deprecation header to the file; do NOT rewrite the body); `leave-as-is` (no edit; refresh on next regenerator run). |
| **Manifest feature(s)** | The TU-N / ME-N / merge-roadmap M-N / CR-DEP-NN / CR-TASK-NN that justifies the row. |
| **Priority (P0–P3)** | P0 = blocks the merge announcement; P1 = user-facing doc rows; P2 = developer-facing / historical analyses; P3 = generated / annotation-only. |
| **Effort (XS–XL)** | XS ≤ 5 lines; S ≤ 15; M ≤ 30; L ≤ 60; XL > 60. |
| **Dependencies** | Build-order edges. Most rows depend on CR-DEP-01 (deprecation stub exists; the redirect target is canonical). |
| **Acceptance criteria** | Observable post-condition (grep returns expected count; deprecation header present; etc.). |
| **Risk assessment** | INV-NN / ME-NN / R-RULE-NN at risk + named mitigation. |

---

## 2. Treatment vocabulary & regex guards

- **`redirect`** — rewrite the string `/sc:task` → `/task` (and `sc:task-protocol` → `task`, `task-unified` → `task` where contextually correct). Anchored regex: `(^|\W)/sc:task(\W|$)` (the trailing `\W` excludes the substring inside `/sc:tasklist`). Use this for live, hand-edited user/developer-facing docs.
- **`leave-with-note`** — prepend a single header line: `> **Deprecation note (2026-MM-DD):** /sc:task was absorbed into /task. References below predate the deprecation.` Use this for archived analyses and historical research extracts where R-RULE-11's spirit (history is not re-litigated; record the decision once) applies.
- **`leave-as-is`** — no edit. Use for pipeline-generated docs. The regenerator script (e.g., `superclaude sprint run`, `sc:index-repo`) emits the new `/task` name when re-run; deferring the update to that run keeps the regenerator → output flow as the single source of truth.

**Regex false-positive guard.** The grep regex used in § 0.1 matches the substring `sc:task` inside `sc:tasklist`. Phase 7 redirect rewrites MUST use the anchored form `(^|\W)/sc:task(\W|$)` (or `sed 's|/sc:task\([^l]\)|/task\1|g'` equivalent) so that `/sc:tasklist` is preserved. `refactor-references.md` CR-REF-03 already documented this triage for `src/`; the same guard applies to `docs/`.

---

## 3. Change rows — documentation edits

Twelve change rows (CR-DOC-01..CR-DOC-12). Order respects: user-guide first (highest user-impact), then guides, then sprint-cli-deep-dive, then historical analyses (annotation-only), then generated (deferred to regenerator). Final row is the R-RULE-11 audit.

### CR-DOC-01 — `[src] docs/user-guide/commands.md` — primary user-facing command catalog (27 matches)

| Column | Value |
|---|---|
| **CR-ID** | CR-DOC-01 |
| **File path (side-tagged)** | `[src] docs/user-guide/commands.md` (1570 lines; 27 grep hits clustered around: line 68 directory diagram, line 148 command index table, line 228 routing description, line 304 `/sc:workflow` cross-reference, line 310 section heading `### /sc:task - Enhanced Task Management`, lines 322/328/332 usage examples, line 365 `/sc:implement` cross-reference, line 982 capability table, line 997 PM hierarchy table, line 1029 PM section "/sc:task — Execution Coordination", lines 1036/1076/1082/1085 PM examples, lines 1099/1119–1122 decision-tree tables, lines 1138/1174/1177/1180 PM examples, line 1505 PM execution example, line 1509 cross-reference link list). |
| **Change** | `redirect` — anchored rewrite `/sc:task` → `/task` across the body. The section heading `### /sc:task - Enhanced Task Management` becomes `### /task — Enhanced Task Management`; in-body anchor `#sctask---enhanced-task-management` becomes `#task--enhanced-task-management` and every link target must be rewritten in the same edit (otherwise the index table at line 148 + the cross-reference link list at line 1509 break). For the directory diagram on line 68 (`├── task.md            # /sc:task - Task Management`), rewrite the comment to `# /task — Task Management (absorbed /sc:task on 2026-MM-DD)` to preserve the absorption context once. After the body redirect, the Gate 1 dispatch description (lines 228 area + lines 304/365 "Difference from /sc:task" comparisons) must be updated to match `refactor-task-skill.md` CR-TASK-02 semantics: the canonical surface is `/task` with optional `Tier:` frontmatter dispatch. The "Difference from /sc:task" comparison blocks (lines 304, 365) should be **removed or rewritten** because `/sc:task` no longer exists as a distinct surface — the comparison collapses into a single `/task` description. |
| **Manifest feature(s)** | CS-M5-B (documentation refresh); CR-DEP-01 (the soft-deprecation stub language for `/sc:task` — references in user-guide are rewritten to the canonical surface); CR-TASK-02 (the user-guide's description of dispatch must match the absorbed Gate 1 behavior, not the donor's classifier prose); R-RULE-06 (no donor ceremony — the "Difference from /sc:task" comparison blocks are dropped as redundant post-absorption); R-RULE-11 (no re-litigation — the rewrite uses declarative `Tier:` semantics from TU-1, not D09b classifier prose). |
| **Priority** | **P0** — user-facing command catalog; ships in the merge-announcement commit. |
| **Effort** | **L** — 27 occurrences plus anchor rewrites plus comparison-block removal; ~40–60 lines of mechanical edits. The anchor rewrite is the highest-risk part (every cross-link inside `commands.md` must be updated; Phase 7 should grep `#sctask---` across `docs/` after the edit to confirm no orphan anchor remains). |
| **Dependencies** | CR-DEP-01 (deprecation stub language canonical); CR-TASK-02 (Gate 1 dispatch behavior documented at the absorbed surface). |
| **Acceptance criteria** | (1) `grep -cE '(^\|\W)/sc:task(\W\|$)' docs/user-guide/commands.md` returns 0 (anchored regex excludes `/sc:tasklist`). (2) The section heading reads `### /task — Enhanced Task Management` and the in-body anchor `#sctask---enhanced-task-management` is renamed to `#task--enhanced-task-management` (or equivalent slug); every cross-link inside `commands.md` resolves. (3) The Gate 1 dispatch description names the declarative `Tier:` field (per TU-1), not a runtime classifier (R-RULE-11 audit). (4) The "Difference from /sc:task" blocks (lines 304, 365) are removed or rewritten as historical context, not active comparison. (5) `mkdocs build` (or equivalent doc-site tooling) succeeds with no broken-link warnings. |
| **Risk assessment** | **INV at risk:** none direct (doc, not runtime). **R-RULE-06 risk:** rewriting the "Difference from /sc:task" comparison blocks as "Difference between /task today and /task before v3.x" reintroduces donor ceremony as historical narrative. **Mitigation:** the comparison blocks are **removed**, not rewritten — the post-merge user-guide does not need to describe a surface that no longer exists. **R-RULE-11 risk:** the rewrite re-introduces donor classifier prose (LR-REJECT-3) if the redirect inadvertently expands the Gate 1 description into priority-cascade keyword tables. **Mitigation:** acceptance criterion (3) pins the description to declarative `Tier:` semantics only. **Secondary risk:** anchor drift breaks cross-links. **Mitigation:** anchor rewrite is part of the same edit; the `mkdocs build` gate (acceptance #5) catches broken links. **Tertiary risk:** the user-guide is referenced from `README.md:40` indirectly (via `docs/user-guide/freshness-hooks.md` link). **Mitigation:** the freshness-hooks doc carries no `/sc:task` references (verified zero); the README link target is unaffected. |

### CR-DOC-02 — `[src] docs/user-guide/flags.md` — single section heading

| Column | Value |
|---|---|
| **CR-ID** | CR-DOC-02 |
| **File path (side-tagged)** | `[src] docs/user-guide/flags.md` (272 lines; 1 grep hit at line 81: `### Task Command Flags (`/sc:task`)`). |
| **Change** | `redirect` — rewrite the section heading to `### Task Command Flags (`/task`)`. Anchor changes from `#task-command-flags-sctask` to `#task-command-flags-task`; if any in-doc link references this anchor, it must be updated in the same edit. |
| **Manifest feature(s)** | CS-M5-B; CR-DEP-01. |
| **Priority** | **P1** — user-facing flags reference. |
| **Effort** | **XS** — single line edit + anchor update. |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | (1) `grep -cE '(^\|\W)/sc:task(\W\|$)' docs/user-guide/flags.md` returns 0. (2) The heading reads `### Task Command Flags (`/task`)`. (3) Any in-repo cross-link to the old anchor (grep `docs/` for `#task-command-flags-sctask`) is updated. |
| **Risk assessment** | **INV at risk:** none. **Secondary risk:** anchor drift if other docs link to the old anchor. **Mitigation:** Phase 7 greps `docs/` for the old anchor string before commit. |

### CR-DOC-03 — `[src] docs/sprint-cli-deep-dive.md` — single prompt example with `sc:task-unified`

| Column | Value |
|---|---|
| **CR-ID** | CR-DOC-03 |
| **File path (side-tagged)** | `[src] docs/sprint-cli-deep-dive.md` (1629 lines; 1 grep hit at line 672: prompt example `/sc:task-unified Execute all tasks in @<phase_file> --compliance strict --strategy systematic`). |
| **Change** | `redirect` — rewrite the prompt example to use `/task` (the absorbing surface). The `--compliance strict --strategy systematic` flags are part of the donor command's flag set; post-absorption, the strategy flag stays on the donor (rejected — see ledger row 21 / LR-REJECT-3) and `--compliance` maps to the declarative `Tier:` frontmatter (TU-1). The example should be rewritten as `/task Execute all tasks in @<phase_file>` with a sentence note explaining that the `Tier: STRICT` (per item or task-level) supersedes the old `--compliance strict` flag. Alternatively, the example can be removed if the deep-dive doc is being retired (Phase 7 checks if this doc is still load-bearing; if not, `leave-with-note` is acceptable). |
| **Manifest feature(s)** | CS-M5-B; CR-DEP-01; CR-TASK-02 (the `Tier:` frontmatter supersedes the donor's `--compliance` flag — the doc must not re-introduce the flag-based dispatch). |
| **Priority** | **P2** — deep-dive doc; not primary user-facing. |
| **Effort** | **XS** — single line edit + ~2-line explanation note. |
| **Dependencies** | CR-DEP-01; CR-TASK-02. |
| **Acceptance criteria** | (1) `grep -cE '(sc:task-unified\|/sc:task)' docs/sprint-cli-deep-dive.md` returns 0. (2) The replacement example does **not** re-introduce a `--compliance` or `--strategy` flag (R-RULE-11 audit — those donor flags are not absorbed; LR-REJECT-3 prohibits classifier-derived strategy at runtime). |
| **Risk assessment** | **INV at risk:** none direct. **R-RULE-11 risk:** re-introducing `--compliance strict` as a flag re-litigates LR-REJECT-3. **Mitigation:** acceptance criterion (2) is the explicit guard; the rewrite uses `Tier:` semantics. |

### CR-DOC-04 — `[src] docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (8 hits)

| Column | Value |
|---|---|
| **CR-ID** | CR-DOC-04 |
| **File path (side-tagged)** | `[src] docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (8 grep hits). |
| **Change** | `redirect` — anchored rewrite. This is the canonical developer guide for the commands/skills/agents architecture; the rewrite must describe the post-absorption layout: `/task` is the canonical command, `sc-task-protocol` skill is hard-deprecated (CR-DEP-03), `commands/task.md` is the soft-deprecation stub (CR-DEP-01). If the guide describes the `mcp-servers:` / `personas:` frontmatter declarations (D02 / Layer A), Phase 7 must verify the rewrite does **not** re-document those declarations as load-bearing (LR-REJECT-2 / ME-9). |
| **Manifest feature(s)** | CS-M5-B; CR-DEP-01 + CR-DEP-03 + CR-DEP-04; CR-TASK-02; ME-9 (audit). |
| **Priority** | **P1** — developer-facing canonical guide. |
| **Effort** | **M** — 8 occurrences across longer narrative; needs careful rewrite of the two-surface description into one-surface. |
| **Dependencies** | CR-DEP-01 + CR-DEP-03; CR-TASK-02. |
| **Acceptance criteria** | (1) `grep -cE '(^\|\W)/sc:task(\W\|$)' docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` returns 0. (2) No `mcp-servers:` / `personas:` advertisement is documented as load-bearing (R-RULE-11 audit — LR-REJECT-2 / ME-9). (3) The guide describes one surface (`/task`), not two. |
| **Risk assessment** | **INV at risk:** none direct. **R-RULE-11 risk:** re-documenting the `mcp-servers:` advertisement as load-bearing re-litigates LR-REJECT-2. **Mitigation:** acceptance criterion (2). **R-RULE-06 risk:** preserving the two-surface description as historical narrative. **Mitigation:** rewrite to one surface; historical context moves to a single sentence in the changelog section if any. |

### CR-DOC-05 — `[src] docs/guides/cli-portify-and-pipeline-runner-guide.md` (15 hits) + `roadmap-cli-tools-release-guide.md` (6 hits) + `sprint-cli-tools-release-guide.md` (4 hits) + `tdd-skill-release-guide.md` (1 hit) + `prd-skill-release-guide.md` (1 hit)

| Column | Value |
|---|---|
| **CR-ID** | CR-DOC-05 |
| **File path (side-tagged)** | `[src] docs/guides/cli-portify-and-pipeline-runner-guide.md`; `[src] docs/guides/roadmap-cli-tools-release-guide.md`; `[src] docs/guides/sprint-cli-tools-release-guide.md`; `[src] docs/guides/tdd-skill-release-guide.md`; `[src] docs/guides/prd-skill-release-guide.md`. Five release-guide / pipeline-guide docs with a combined 27 grep hits. |
| **Change** | `redirect` — anchored rewrite `/sc:task` → `/task` across each file's body. Where a guide describes the pipeline as emitting `/sc:task` prompts (matches `refactor-references.md` CR-REF-01 / CR-REF-02 — the CLI now emits `/task` prompts), update the prose to match the runtime behavior. |
| **Manifest feature(s)** | CS-M5-B; CR-DEP-01; CR-REF-01 + CR-REF-02 (the prose must match the CLI runtime). |
| **Priority** | **P1** — release-guide docs are referenced from active sprints. |
| **Effort** | **M** — five files × ≤ 5 line edits each ≈ ~25 lines aggregate. |
| **Dependencies** | CR-DEP-01; CR-REF-01 + CR-REF-02 (CLI prompt redirects shipped). |
| **Acceptance criteria** | (1) `grep -clE '(^\|\W)/sc:task(\W\|$)' docs/guides/cli-portify-and-pipeline-runner-guide.md docs/guides/roadmap-cli-tools-release-guide.md docs/guides/sprint-cli-tools-release-guide.md docs/guides/tdd-skill-release-guide.md docs/guides/prd-skill-release-guide.md` returns 0 files. (2) Each guide's prompt-example, if any, matches the canonical `/task` form. |
| **Risk assessment** | **INV at risk:** none. **Secondary risk:** the pipeline-runner-guide is high-hit (15) and may contain detailed sample output that includes `/sc:task` as a literal verifiable string. **Mitigation:** the redirect treats only prose; sample CLI output blocks (denoted by code-fence) should be regenerated by re-running the pipeline if they are presented as actual transcripts. Phase 7 picks per file. |

### CR-DOC-06 — `[src] docs/analysis-sc-tasklist.md` (12 hits) — annotation header

| Column | Value |
|---|---|
| **CR-ID** | CR-DOC-06 |
| **File path (side-tagged)** | `[src] docs/analysis-sc-tasklist.md` (12 grep hits; top-level analysis doc, likely a one-shot research note about `sc-tasklist`). |
| **Change** | `leave-with-note` — prepend the single-line deprecation header. The doc analyzes `/sc:task` against `/sc:tasklist`; rewriting the body to use `/task` would invalidate the analysis (the analysis was performed against the donor surface at a specific point in time). Add the deprecation header; do not edit the body. |
| **Manifest feature(s)** | CS-M5-B; R-RULE-11 (spirit — historical analyses are not re-litigated). |
| **Priority** | **P2** — annotation row. |
| **Effort** | **XS** — single header line. |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | The file starts with the deprecation header (line 1 or line 2 after the title); body is unchanged. |
| **Risk assessment** | **Risk:** annotation drift if the deprecation date is wrong. **Mitigation:** date matches CR-DEP-01 commit date. |

### CR-DOC-07 — `[src] docs/analysis/*.md` cluster — historical competitive analyses (4 files, 11 hits)

| Column | Value |
|---|---|
| **CR-ID** | CR-DOC-07 |
| **File path (side-tagged)** | `[src] docs/analysis/bmad-vs-superclaude-comparison.md` (2 hits); `[src] docs/analysis/claude-code-best-practice-vs-superclaude.md` (1 hit); `[src] docs/analysis/openclaw-vs-superclaude-comparison.md` (2 hits); `[src] docs/analysis/superpowers-vs-superclaude-comparison.md` (6 hits). |
| **Change** | `leave-with-note` — prepend the deprecation header to each file. These are point-in-time competitive analyses; the bodies record what the competitor + SuperClaude looked like on the analysis date. R-RULE-11 spirit: historical decisions are not re-litigated. |
| **Manifest feature(s)** | CS-M5-B; R-RULE-11 spirit. |
| **Priority** | **P2** — annotation row. |
| **Effort** | **XS** per file — 4 single-line header insertions. |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | Each of the 4 files starts with the deprecation header. Bodies are unchanged. |
| **Risk assessment** | Same as CR-DOC-06. |

### CR-DOC-08 — `[src] docs/research/*.md` top-level cluster (3 files, 6 hits)

| Column | Value |
|---|---|
| **CR-ID** | CR-DOC-08 |
| **File path (side-tagged)** | `[src] docs/research/competitive-landscape-final-report-2026-03-23.md` (4 hits); `[src] docs/research/competitive-landscape-tasklist-execution-2026.md` (1 hit); `[src] docs/research/superpowers-vs-superclaude-comparison.md` (1 hit). |
| **Change** | `leave-with-note` — prepend the deprecation header. Same rationale as CR-DOC-07; these are research reports with a dated scope. |
| **Manifest feature(s)** | CS-M5-B; R-RULE-11 spirit. |
| **Priority** | **P2**. |
| **Effort** | **XS** per file. |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | Each file starts with the deprecation header. |
| **Risk assessment** | Same as CR-DOC-06. |

### CR-DOC-09 — `[src] docs/research/dev-guide-research/*.md` cluster (11 files, ≈109 hits) — frozen research extracts

| Column | Value |
|---|---|
| **CR-ID** | CR-DOC-09 |
| **File path (side-tagged)** | `[src] docs/research/dev-guide-research/00-file-inventory.md` (2); `extract-haiku-08-commands-core.md` (3); `extract-haiku-09-orchestrator-core.md` (2); `extract-haiku-12-skills-multi.md` (24); `extract-haiku-15-commands-examples.md` (29); `extract-opus-06-advanced-patterns.md` (1); `extract-opus-08-commands-core.md` (10); `extract-opus-09-orchestrator-core.md` (1); `extract-opus-12-skills-multi.md` (8); `extract-opus-15-commands-examples.md` (28); `extract-opus-20-roadmap-v2-spec.md` (1). |
| **Change** | `leave-with-note` — single header per file. These are *extraction artifacts* from research runs against a specific snapshot of the framework; rewriting them would falsify the extraction record. R-RULE-11 spirit: research artifacts are frozen at extraction time. Optionally, the entire `dev-guide-research/` subdirectory may be moved to `docs/research/_archive/` to make the "frozen" nature explicit (Phase 7 decision; not blocking). |
| **Manifest feature(s)** | CS-M5-B; R-RULE-11 spirit. |
| **Priority** | **P3** — annotation row. |
| **Effort** | **S** — 11 files × 1 header line each. |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | Each of the 11 files starts with the deprecation header. Bodies are unchanged. |
| **Risk assessment** | **R-RULE-11 risk:** rewriting the extraction bodies invalidates the research record. **Mitigation:** `leave-with-note` is annotation-only; bodies are explicitly preserved. |

### CR-DOC-10 — `[src] docs/generated/contributor-knowledge-base/` cluster (4 files, 43 hits) — regenerated by `sc:index-repo` / equivalent

| Column | Value |
|---|---|
| **CR-ID** | CR-DOC-10 |
| **File path (side-tagged)** | `[src] docs/generated/contributor-knowledge-base/architecture-guide.md` (2); `commands-skills-cross-reference.md` (21); `components-guide.md` (2); `visual-architecture-summary.md` (18). |
| **Change** | `leave-as-is` — these are pipeline-generated docs (per `refactor-references.md` § 4.G; `docs/generated/` is the canonical output of regenerator scripts). The next regenerator run will emit the new `/task` name, deferring the update to that run. Phase 7 must record in the commit message that the regenerator is the source of truth and the next regeneration will refresh the docs. If the regenerator runs as part of `make test` or CI, the commit that lands CR-DEP-01..04 + CR-DIST-01..06 may also trigger the regeneration automatically; if so, the regenerated docs land in the same commit. |
| **Manifest feature(s)** | CS-M5-B (T06.04 doc scope); CR-DEP-01..04 (the absorbed surface that the regenerator will name). |
| **Priority** | **P3** — pipeline-deferred. |
| **Effort** | **XS** — no manual edit. |
| **Dependencies** | CR-DEP-01..04 (the deprecation/absorption that the regenerator's next emission will reflect). |
| **Acceptance criteria** | (1) Commit message for the merge sequence includes the line "docs/generated/contributor-knowledge-base/: refresh deferred to next sc:index-repo run." (2) On next regeneration, the four files contain `/task` (not `/sc:task`); verifiable post-regeneration grep. (3) If the regenerator is run as part of `make test` / CI in the same commit, the regenerated docs land in the same commit and acceptance (2) is verified immediately. |
| **Risk assessment** | **Risk:** manual edits to `docs/generated/` create drift between the regenerator's expected output and the on-disk file. **Mitigation:** `leave-as-is` enforces the regenerator-as-source-of-truth contract. **Secondary risk:** the regenerator is never re-run and the docs stay stale indefinitely. **Mitigation:** Phase 7 reviewer schedules a follow-up `sc:index-repo` run within the same sprint (recommended) or documents the deferral. |

### CR-DOC-11 — `[src] docs/generated/sprint-cli/` cluster (≈14 files, ≈75 hits) — regenerated by sprint-cli pipeline

| Column | Value |
|---|---|
| **CR-ID** | CR-DOC-11 |
| **File path (side-tagged)** | `[src] docs/generated/sprint-cli/00-overview.md` (3); `03-execution-engine.md` (1); `05-pm-agent.md` (4); `07-skills-commands.md` (20); `09-wiring-validation.md` (5); `10-critique-validation.md` (4); `v3.7-refactor/chunk-03-naming-consolidation.md` (15); `v3.7-refactor/chunk-05-cross-cutting.md` (2); `v3.7-refactor/context-01-path-a-deficiencies.md` (1); `v3.7-refactor/context-03-v37-spec-gap-analysis.md` (3); `v3.7-refactor/MERGED-REFACTORING-RECOMMENDATION.md` (6); `v3.7-refactor/spec-gen-prompt-architect.md` (12); `v3.7-refactor/spec-gen-prompt-incremental.md` (3); `v3.7-refactor/spec-gen-prompt-qa.md` (1); `v3.7-refactor/spec-gen-adversarial/merged-spec-gen-prompt.md` (12); `debates/debate-file-preloading.md` (1); `debates/debate-strict-halt.md` (1). |
| **Change** | `leave-as-is` — same rationale as CR-DOC-10. These are sprint-cli pipeline outputs. Notably, the `v3.7-refactor/` subtree is **frozen** (it documents a previous refactor cycle and should not be re-emitted); for that subtree, the treatment is `leave-as-is` + the deprecation-note header from CR-DOC-09's mechanism. Phase 7 picks: option (a) treat `v3.7-refactor/` as historical (`leave-with-note`) and the rest of `sprint-cli/` as pipeline-deferred (`leave-as-is`); option (b) treat the entire subtree as pipeline-deferred. **Recommendation: (a)** — `v3.7-refactor/` is documented as the v3.7-cycle output and a deprecation header preserves the historical record; the rest of `sprint-cli/` is pipeline-deferred. |
| **Manifest feature(s)** | CS-M5-B; R-RULE-11 spirit (for `v3.7-refactor/`). |
| **Priority** | **P3**. |
| **Effort** | **S** — ~10 deprecation-header insertions for `v3.7-refactor/` (and `debates/`); no edits for the rest. |
| **Dependencies** | CR-DEP-01..04. |
| **Acceptance criteria** | (1) `v3.7-refactor/**` and `debates/**` files each start with the deprecation header. (2) `sprint-cli/00-overview.md`, `03`, `05`, `07`, `09`, `10` are unchanged; refresh deferred to next sprint-cli regenerator run. (3) The commit message records the deferral plan. |
| **Risk assessment** | **R-RULE-11 risk:** rewriting `v3.7-refactor/` would re-litigate v3.7-cycle decisions. **Mitigation:** `leave-with-note`, not `redirect`. |

### CR-DOC-12 — `[src] docs/generated/` remaining files (4 files, 25 hits)

| Column | Value |
|---|---|
| **CR-ID** | CR-DOC-12 |
| **File path (side-tagged)** | `[src] docs/generated/cleanup-sc-prefix-reference-index.md` (11 hits); `[src] docs/generated/cleanup-sc-prefix-rename-tasklist.md` (7 hits); `[src] docs/generated/cli-portify-release-guide.md` (6 hits); `[src] docs/generated/tasklist-unwired-components-remediation.md` (1 hit). |
| **Change** | `leave-as-is` — pipeline-generated; refresh deferred to next regenerator run. The two `cleanup-sc-prefix-*` files are particularly relevant: they may be the output of a *prior* prefix-cleanup pipeline and could become stale post-merge. Phase 7 confirms whether re-running the cleanup pipeline regenerates them with the new `/task` name; if yes, defer; if the pipeline is itself deprecated, mark `leave-with-note` instead. |
| **Manifest feature(s)** | CS-M5-B. |
| **Priority** | **P3**. |
| **Effort** | **XS** — no edit. |
| **Dependencies** | CR-DEP-01..04. |
| **Acceptance criteria** | Commit message records "docs/generated/cleanup-sc-prefix-*.md and cli-portify-release-guide.md: refresh deferred to next regenerator run." |
| **Risk assessment** | **Risk:** the regenerator is itself deprecated and the docs stay stale. **Mitigation:** Phase 7 verifies whether the cleanup-sc-prefix pipeline is still operational; if not, demote to `leave-with-note`. |

### CR-DOC-13 — R-RULE-11 audit on all CR-DOC rows

| Column | Value |
|---|---|
| **CR-ID** | CR-DOC-13 |
| **File path (side-tagged)** | All CR-DOC-NN rows above (audit-row over the set). |
| **Change** | `audit` — verify no CR-DOC row silently re-proposes a `rejected-features-ledger.md` REJECT or DEFER entry. Cross-checked in § 4. |
| **Manifest feature(s)** | R-RULE-11. |
| **Priority** | **P3**. |
| **Effort** | **XS**. |
| **Dependencies** | CR-DOC-01..12. |
| **Acceptance criteria** | § 4 confirms zero re-litigation; Phase 7 reviewer confirms. |
| **Risk assessment** | **INV at risk: R-RULE-11**. **Mitigation:** § 4 cross-check is the gate. |

---

## 4. R-RULE-11 audit — no rejected-features-ledger entry re-litigated by a doc row

| Ledger entry | Status | CR-DOC row that could re-introduce? | Audit verdict |
|---|---|---|---|
| LR-REJECT-2 (D02 / Layer A `mcp-servers:` advertisement) | REJECTed | CR-DOC-01, CR-DOC-04 (user/developer guides) | Acceptance criteria explicitly forbid re-documenting `mcp-servers:` as load-bearing. **Pass.** |
| LR-REJECT-3 (D09b runtime classifier prose) | REJECTed | CR-DOC-01, CR-DOC-04 (where Gate 1 dispatch is described) | Acceptance criteria pin the description to declarative `Tier:` semantics (CR-TASK-02). **Pass.** |
| LR-REJECT-7 (D15c per-tier procedure synthesis) | REJECTed | CR-DOC-01, CR-DOC-04, CR-DOC-05 | No CR-DOC row authors per-tier procedure prose; the `Tier:` description names the dispatch profile, not a procedure synthesis. **Pass.** |
| LR-DEFER-4 (D01 `allowed-tools:` enforcement) | DEFERRED (ME-8) | None | No doc row enforces `allowed-tools:`; docs describe the absorbed surface as it is. **Pass.** |
| LR-DEFER-5 (D08 header emission) | DEFERRED (ME-7) | None | No doc row introduces header emission. **Pass.** |
| All other REJECT/DEFER entries | Various | None | Doc rows are textual rewrites or annotations; do not touch the bound rejections. **Pass.** |

**Audit verdict:** zero ledger entries re-proposed; R-RULE-11 satisfied across all CR-DOC rows.

---

## 5. Coverage check — every enumerated doc file has a treatment

| § 0.1 row(s) | Path(s) | CR-DOC treatment |
|---|---|---|
| 1 | docs/user-guide/commands.md | CR-DOC-01 (redirect) |
| 2 | docs/user-guide/flags.md | CR-DOC-02 (redirect) |
| 3 | docs/sprint-cli-deep-dive.md | CR-DOC-03 (redirect) |
| 4 | docs/guides/cli-portify-and-pipeline-runner-guide.md | CR-DOC-05 (redirect) |
| 5 | docs/guides/sprint-cli-tools-release-guide.md | CR-DOC-05 (redirect) |
| 6 | docs/guides/roadmap-cli-tools-release-guide.md | CR-DOC-05 (redirect) |
| 7 | docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md | CR-DOC-04 (redirect) |
| 8 | docs/guides/tdd-skill-release-guide.md | CR-DOC-05 (redirect) |
| 9 | docs/guides/prd-skill-release-guide.md | CR-DOC-05 (redirect) |
| 10 | docs/analysis-sc-tasklist.md | CR-DOC-06 (leave-with-note) |
| 11–14 | docs/analysis/*.md (4 files) | CR-DOC-07 (leave-with-note) |
| 15–17 | docs/research/*.md top-level (3 files) | CR-DOC-08 (leave-with-note) |
| 18–28 | docs/research/dev-guide-research/*.md (11 files) | CR-DOC-09 (leave-with-note) |
| 33–36 | docs/generated/contributor-knowledge-base/*.md (4 files) | CR-DOC-10 (leave-as-is) |
| 37–53 | docs/generated/sprint-cli/**/*.md (≈17 files) | CR-DOC-11 (leave-as-is + leave-with-note for v3.7-refactor/) |
| 29–32 | docs/generated/ other (4 files) | CR-DOC-12 (leave-as-is) |

**Coverage verdict:** all 53 files enumerated in § 0.1 carry a treatment in § 3. **Pass (T06.04 AC #2).**

---

## 6. Consistency check against `refactor-references.md` § 4.G hand-off (T06.04 AC #3)

`refactor-references.md` CR-REF-DEFER-T06.04 (§ 4.G) handed off ≈40 doc files to T06.04 with the treatment scheme:
- Hand-edited docs (`docs/user-guide/`, `docs/guides/`, `docs/sprint-cli-deep-dive.md`) → explicit `redirect` rows. **This file: CR-DOC-01..05 cover those. Pass.**
- Regenerated docs (`docs/generated/*`) → `leave-as-is` + regenerator-update guidance. **This file: CR-DOC-10..12 cover those. Pass.**
- `docs/analysis/` and `docs/research/` (historical) → `leave-with-note`. **This file: CR-DOC-06..09 cover those. Pass.**

**Consistency verdict:** every § 4.G hand-off file has a corresponding treatment in this file with the matching scheme. **Pass.**

Additionally, the file inventory expanded from ≈40 (T06.03 estimate) to 53 (T06.04 re-verified count) because `dev-guide-research/` was under-counted in the T06.03 bucket. The additional 13 files are all in `dev-guide-research/` and are covered by CR-DOC-09 (`leave-with-note`), the same treatment the T06.03 bucket prescribed for the directory.

---

## 7. Phase 7 execution-order constraint (within M5-B)

CR-DEP-01 (deprecation stub language canonical) → **CR-DOC-01 + CR-DOC-02 + CR-DOC-04** (user-guide and developer-guide; P0/P1; ship-together in the merge-announcement commit so the user-facing surface is consistent) → **CR-DOC-05 + CR-DOC-03** (guides + deep-dive; P1/P2; follow-on commit) → **CR-DOC-06..09** (annotation headers on historical analyses; P2/P3; can land in any order; recommend bundling into a single commit for ease of revert) → **CR-DOC-10..12** (generated docs; P3; no edit; commit-message-only note + scheduled regenerator run) → **CR-DOC-13** (R-RULE-11 audit; post-hoc).

**Atomicity rule:** CR-DOC-01 (user-guide commands.md) must land in the same commit as (or after) CR-DEP-01 + CR-TASK-02 — the user-guide must not describe `/task` as the canonical surface before `/task` actually carries the Gate 1 dispatch behavior.

---

## 8. Acceptance criteria roll-up (T06.04 AC mapping)

| T06.04 AC | Where satisfied in this file |
|---|---|
| **AC #1** — owned by the companion `refactor-distribution.md` | n/a in this file. |
| **AC #2** — `refactor-documentation.md` exists with a change row for every doc referencing `/sc:task` or the two-surface model | § 0.1 enumerates 53 files; § 3 covers every file with a CR-DOC-NN row; § 5 verifies coverage. |
| **AC #3** — Distribution changes are consistent with the artifact-level deprecation decisions in T06.03 | § 6 (consistency with `refactor-references.md` § 4.G hand-off scheme; redirect / leave-with-note / leave-as-is partition matches T06.03's intent). |
| **AC #4** — Every change row carries the standard eight columns including risk assessment | § 3 — all 13 rows have all eight columns including a risk-assessment cell that names INV-NN/ME-NN/R-RULE-NN and the mitigation. |

---

## 9. Sibling artifact handoff (back to `refactor-distribution.md`)

`refactor-distribution.md` (this task's first deliverable) owns: README, installer code paths, `make sync-dev` filter rules, `make verify-sync` orphan rule audit, `plugins/superclaude/commands/task.md` plugin stub.

`refactor-documentation.md` (this file) owns: every `docs/` body that names `/sc:task` or the two-surface model.

Together, the two files close the distribution + documentation surface affected by the merge. The `merge-master.md` (T06.05) consolidates all CR-DIST + CR-DOC rows alongside CR-TASK / CR-MDTM / CR-DEP / CR-REF into one ordered execution plan.
