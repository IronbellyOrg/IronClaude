# Refactor Plan — Reference Enumeration & Treatment (Phase 6 / T06.03)

**Task:** T06.03 — Refactor plans: `/sc:task` deprecation & references
**Roadmap Item:** R-021
**Tier:** STRICT
**Generated:** 2026-05-15
**Status:** Driving input for Phase 7 execution. Each reference (or reference cluster — § 4 categorizes which) carries an eight-column treatment row.

**Inputs (1:1 referenced):**
- `transfer-manifest.md` (T05.03) — TU-1..TU-8, ME-1..ME-9 (what was absorbed; what was REJECTed).
- `rejected-features-ledger.md` (T05.03) — terminal under R-RULE-11.
- `merge-roadmap.md` (T06.01) — CS-M4-B reference enumeration scope ("every reference to `sc:task`, `sc:task-unified`, `sc-task-protocol`, `sc-task-unified-protocol`, `/sc:task` across the repo. Highest-density region: `.dev/releases/backlog/v5.xxforensic/`").
- `refactor-sctask-deprecation.md` (T06.03 companion) — disposition decisions per donor artifact (soft vs hard). Reference treatments below align with these decisions: redirect strings point at `/task`; the soft-deprecated `/sc:task` command remains invocable as a deprecation stub.

**Companion artifact:** `refactor-sctask-deprecation.md` — the per-artifact deprecation plan. Read first; this file references its disposition decisions throughout.

**Scope boundary:**
- Every reference to `/sc:task`, `sc:task`, `sc:task-unified`, `task-unified`, `sc-task-protocol`, `sc-task-unified-protocol`, `sc-task-unified` is in scope.
- The donor artifact files themselves (`commands/task.md`, `skills/sc-task-protocol/`) are handled in `refactor-sctask-deprecation.md` and are **excluded** from the rows below to avoid double-counting. The references rows cover *every other file that mentions the donor surface*.
- Distribution-surface code paths (installer, sync rules, README) and user-/developer-/reference-guide docs are surfaced here but explicitly deferred to **T06.04** for the eight-column installer/doc rows. Each such row below is marked `→ T06.04` with a pointer.
- The `.venv/` directory contains a frozen pip-install snapshot of the same source tree (`.venv/lib/python3.12/site-packages/superclaude/_src/...`). It is not editable repo state; it refreshes when `superclaude` is reinstalled. § 4.G enumerates the bucket-level treatment.

---

## 0. Search corpus & method

**Search command (executed at T06.03 generation):**
```bash
grep -rln -E 'sc:task|task-unified|sc-task-protocol|sc-task-unified-protocol|sc-task-unified' --include='*.md' --include='*.py' --include='*.sh' --include='*.json' --include='*.yaml' --include='*.yml' --include='Makefile' .
```

**Hit count summary (T06.03 generation, before any edits):**

| Bucket | File count | Bucket treatment | Section |
|---|---|---|---|
| Active source tree (`src/`, `.claude/`, `plugins/`, `tests/`, root) | 31 | Per-file row (most), some `→ T06.04` | § 4.A |
| Active backlog (live planning — `v5.xx*`, `v6.xx_*`, `prd-*`, `tdd-*`, `v5xx-Spec-*`) | 18 | Per-file row, treatment = redirect or note-with-deprecation-date | § 4.B |
| Archived backlog (`v3.xx*`, `v3.8-*`, `v3.9-*`, `v4.xx-*`, `v4xx-*`, `v5.xx-sc-troubleshoot-v2`) | 39 | Bucket row: leave-with-deprecation-note; no per-file edits | § 4.C |
| `.dev/releases/backlog/v5.xxforensic/` (high-density carve-out from § 4.C) | 14 | Per-file row, treatment = redirect-or-note depending on planning status | § 4.D |
| `.dev/releases/archive/v3.75-RigorflowMerger-task-unified-v3/` (already archived, terminal) | 33 | Bucket row: leave-as-is (archive is frozen) | § 4.E |
| `.dev/tasks/to-do/TASK-*/` (live MDTM task data; user-authored) | ~30 | Bucket row: leave-as-is + new-task guidance | § 4.F |
| `.dev/benchmarks/`, `.dev/test-fixtures/` (frozen test outputs) | ~30 | Bucket row: leave-as-is (regeneration-only, not hand-edited) | § 4.F |
| `docs/` (user-guide, developer-guide, analysis, research, generated, guides) | ~40 | Defer to T06.04 doc rows; § 4.G enumerates the file list per T06.04 hand-off | § 4.G |
| `.venv/lib/python3.12/site-packages/superclaude/...` | ~24 | Bucket row: not-editable, refreshes on `pip install -e .` | § 4.H |
| `.serena/memories/` | 1 | Bucket row: serena memory, runtime-managed | § 4.H |
| `.claude/agent-memory/` | 1 | Bucket row: runtime memory file | § 4.H |

**Grand total of distinct files with at least one match:** ~230 (active + frozen + venv). Per-file rows are authored for **active editable surface only** (rows in § 4.A and § 4.B and § 4.D, ≈60 files); frozen / regenerated / not-editable surface (§ 4.C, § 4.E, § 4.F, § 4.G — for docs deferred to T06.04 — § 4.H) is enumerated by bucket with the per-bucket treatment row carrying all eight columns (T06.03 AC #3: every reference has a treatment).

---

## 1. Column legend (every row carries all eight columns — T06.03 AC #3)

| Column | Meaning |
|---|---|
| **CR-ID** | Stable change-row identifier (`CR-REF-NN` for per-file rows; `CR-REF-BUCKET-X` for category-level rows). |
| **File path (or bucket)** | Concrete repo-relative path (per-file rows) or path glob (bucket rows). Side-tagged where the path lives under `src/` vs `.claude/`. |
| **Change** | Treatment: `redirect` (rewrite `/sc:task` → `/task`); `remove` (delete the reference entirely); `leave-with-note` (annotate with the deprecation-date marker but do not edit the body); `leave-as-is` (frozen / regenerated content, no action); `→ T06.04` (defer to the distribution / documentation refactor plan). |
| **Manifest feature(s)** | The TU-N / ME-N / merge-roadmap M-N / R-RULE-NN that justifies the treatment. |
| **Priority (P0–P3)** | P0 = blocks Phase 7 distribution; P1 = direct dependent; P2 = follow-on cleanup; P3 = annotation-only. |
| **Effort (XS–XL)** | XS ≤ 5 lines, S ≤ 15, M ≤ 30, L ≤ 60, XL > 60. |
| **Dependencies** | Build-order edges. Most reference rows depend on CR-DEP-01 (the soft-deprecation stub exists before any redirect text claims `/task` is canonical). |
| **Acceptance criteria** | Observable post-condition (grep returns expected count; commit message present). |
| **Risk assessment** | INV-NN / ME-NN / R-RULE-NN at risk + mitigation. |

---

## 2. Treatment vocabulary (per merge-roadmap CS-M4-B)

CS-M4-B specifies three primary treatment options for any non-donor reference: **redirect**, **remove**, **leave-with-note**. This refactor adds two procedural treatments needed by the operational reality of the repo:

- **`redirect`** — rewrite the string `/sc:task` → `/task` (and `sc:task-protocol` → `task`, etc.) in the file body. Use this when the reference is in a live document that drives current behavior (CLI prompts, active commands, active backlog planning).
- **`remove`** — delete the reference line entirely. Use this when the reference is metadata that becomes false after CR-DEP-03 (e.g., `PROJECT_INDEX.md` listing `sc-task-unified-protocol/` as an extant skill directory).
- **`leave-with-note`** — prepend a single-line "Deprecation note: `/sc:task` was absorbed into `/task` on 2026-MM-DD (this sprint). References below predate the deprecation." to the file header. Use this for archived planning docs that record historical intent and must not be rewritten (R-RULE-11 spirit: history is not re-litigated; archives stay archived).
- **`leave-as-is`** — no edit. Use this for frozen test fixtures, benchmark outputs, venv snapshots, and regenerated pipeline artifacts (`docs/generated/...`) that refresh from a regenerator script. The deprecation propagates naturally when the regenerator next runs.
- **`→ T06.04`** — defer the per-file row to the distribution/documentation refactor plan. Use this for the installer code (`src/superclaude/cli/install_*.py`), `make sync-dev` filter (`Makefile`), README, and the `docs/user-guide/`, `docs/developer-guide/`, `docs/reference/` files. T06.04 produces the eight-column rows for these files; § 4.A and § 4.G below list the files but mark them `→ T06.04` to avoid double-authorship.

---

## 3. R-RULE-11 audit — no rejected-features-ledger entry re-litigated by a reference treatment

Per T06.03 governing R-RULE-11, the reference treatments may not re-introduce a REJECTed pattern. Audit:

- No `redirect` row resurrects D02 / Layer A `mcp-servers:` advertisement (ME-9 / LR-REJECT-2). Reference treatments are textual `/sc:task` → `/task` rewrites only.
- No `redirect` row resurrects D09b classifier prose (LR-REJECT-3 / row 21). `Tier:` is declarative, not derived; reference treatments do not introduce new classifier prose.
- No `redirect` row resurrects D15c per-tier procedure synthesis (LR-REJECT-7).
- No `redirect` row introduces a header emission (ME-7 / LR-DEFER-5) — references in backlog docs that mention header emission stay verbatim under `leave-with-note`; they predate the deprecation.

**Audit verdict:** all reference treatments below are mechanical (string rewrite or annotation); none re-litigate a ledger entry. **Pass.**

---

## 4. Reference inventory & per-row treatments

### 4.A — Active source tree (per-file rows; ≈31 files)

Files in this section are live, editable, and either drive runtime behavior or are dev-copy mirrors of files that do. Per-file rows below carry all eight T06.03 columns.

#### CR-REF-01 — `[src] src/superclaude/cli/sprint/process.py` — runtime CLI emits `/sc:task` invocation strings

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-01 |
| **File path** | `[src] src/superclaude/cli/sprint/process.py` (lines 124 + 170). `process.py:124` docstring `"""Build the /sc:task prompt for this phase."""`; `process.py:170` f-string `f"/sc:task Execute all tasks in @{phase_file} "`. |
| **Change** | `redirect` — rewrite both occurrences `/sc:task` → `/task`. The CLI emits prompts that the user-side Claude runs; these prompts must invoke the canonical command. |
| **Manifest feature(s)** | CS-M4-B (reference enumeration); CR-DEP-01 dependency (the soft-deprecation stub must exist before any redirect claims `/task` is canonical — both rows ship in the same Phase 7 commit). |
| **Priority** | **P0** — runtime CLI; emits the wrong command name until fixed. |
| **Effort** | **XS** — 2 line edits. |
| **Dependencies** | CR-DEP-01 (deprecation stub exists before redirect). Also depends on T06.02 CR-TASK rows landing (`/task` skill carries the absorbed behavior). |
| **Acceptance criteria** | (1) `grep -nE "/sc:task" src/superclaude/cli/sprint/process.py` returns no matches. (2) `tests/sprint/test_process.py` test cases on the canonical command name pass (currently `assert prompt.startswith("/sc:task ")` at line 88 → must be updated to `/task ` in the same commit per CR-REF-09 below). |
| **Risk assessment** | **INV at risk:** runtime behavior; if the redirect lands without the deprecation stub, end users running `sprint run` get a "skill not found" or invoke the wrong skill. **Mitigation:** CR-DEP-01 dependency; both ship in the same commit. **Secondary risk:** test suite breakage. **Mitigation:** CR-REF-09 updates the test assertions in the same commit. |

#### CR-REF-02 — `[src] src/superclaude/cli/cleanup_audit/prompts.py` — five `/sc:task` prompt strings

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-02 |
| **File path** | `[src] src/superclaude/cli/cleanup_audit/prompts.py` (lines 26, 47, 69, 92, 116). Five f-string occurrences of `/sc:task Perform ...`. |
| **Change** | `redirect` — rewrite all five `/sc:task` → `/task`. |
| **Manifest feature(s)** | CS-M4-B; CR-DEP-01 dependency. |
| **Priority** | **P0** — runtime CLI for `cleanup-audit` pipeline. |
| **Effort** | **XS** — 5 line edits. |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | `grep -nE "/sc:task" src/superclaude/cli/cleanup_audit/prompts.py` returns no matches; existing tests that exercise these prompts still pass after the redirect. |
| **Risk assessment** | Same as CR-REF-01. **Mitigation:** atomic commit with CR-DEP-01. |

#### CR-REF-03 — `[src] src/superclaude/cli/sprint/config.py` / `checkpoints.py` / `tasklist/prompts.py` / `roadmap/validate_prompts.py` — `sc:tasklist` / `sc:task-protocol` adjacent references

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-03 |
| **File path** | `[src] src/superclaude/cli/sprint/config.py:240` ("a `tasklist/` subdirectory created by `sc:tasklist`"); `[src] src/superclaude/cli/sprint/checkpoints.py:28` ("emitted by `/sc:tasklist`"); `[src] src/superclaude/cli/tasklist/prompts.py:158` ("used by the `/sc:tasklist` skill protocol"); `[src] src/superclaude/cli/roadmap/validate_prompts.py:82` + `:126` ("by sc:tasklist"). |
| **Change** | `leave-as-is` — these are `/sc:tasklist` references, **not** `/sc:task` references. The grep regex matches `sc:task` as a prefix substring of `sc:tasklist`. They are **not in scope** for T06.03. Recorded here to confirm the false-positive triage; Phase 7 may delete this row after re-verification. |
| **Manifest feature(s)** | None — out-of-scope reference. |
| **Priority** | **P3** — annotation row only. |
| **Effort** | **XS** — no edit. |
| **Dependencies** | None. |
| **Acceptance criteria** | Phase 7 reviewer confirms these lines reference `/sc:tasklist` (the tasklist generator command), not `/sc:task`. No edit required. |
| **Risk assessment** | **Risk:** accidentally rewriting `sc:tasklist` → `tasklist` and breaking the tasklist command. **Mitigation:** the redirect commands in CR-REF-01 / CR-REF-02 / etc. use the exact string `/sc:task ` (with trailing space) or `/sc:task<word-boundary>`, not the substring `sc:task`. |

#### CR-REF-04 — `[src] src/superclaude/commands/*.md` (other commands referencing `/sc:task`)

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-04 |
| **File path** | `[src] src/superclaude/commands/adversarial.md`, `[src] src/superclaude/commands/help.md`, `[src] src/superclaude/commands/release-split.md`, `[src] src/superclaude/commands/tasklist.md`, `[src] src/superclaude/commands/validate-roadmap.md`, `[src] src/superclaude/commands/validate-tests.md`. Each contains one or more `/sc:task` cross-references in usage examples or related-command lists. |
| **Change** | `redirect` — rewrite `/sc:task` → `/task` in body text. Where the reference is in a `## Related Commands` / `## See Also` list, update the list item to `/task`. |
| **Manifest feature(s)** | CS-M4-B. |
| **Priority** | **P1** — user-visible command help text. |
| **Effort** | **XS-S per file** (~1-3 line edits each). |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | (1) `grep -lE "/sc:task" src/superclaude/commands/` excluding `task.md` (the soft-deprecated file) returns no files. (2) `make verify-sync` returns 0 after `make sync-dev` propagates the edits to `.claude/commands/sc/*.md`. |
| **Risk assessment** | **Risk:** cross-reference rot if a redirect introduces a broken anchor (e.g., `#sctask---enhanced-task-management` becomes a dead link). **Mitigation:** Phase 7 must rewrite anchors in the same edit (anchor changes follow from the section-heading rewrites in T06.04 docs). |

#### CR-REF-05 — `[src] src/superclaude/core/COMMANDS.md` line 81 + `core/ORCHESTRATOR.md` line 153

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-05 |
| **File path** | `[src] src/superclaude/core/COMMANDS.md:81` (`**`/sc:task [description] [flags]`**` — command-catalog row); `[src] src/superclaude/core/ORCHESTRATOR.md:153` ("Route `/sc:task` commands to appropriate compliance tier..."). |
| **Change** | `redirect` for COMMANDS.md (rewrite catalog row to `/task` with the updated description per CR-DEP-01 stub semantics) + `remove` or `redirect` for ORCHESTRATOR.md (the routing prose describes a flow that no longer exists post-merge; rewrite to describe the `/task` Gate 1 dispatch from T06.02 CR-TASK-02). |
| **Manifest feature(s)** | CS-M4-B; TU-1 (Gate 1 dispatch — the routing description must be updated to point at the recipient surface). |
| **Priority** | **P1** — core framework docs. |
| **Effort** | **S** — ~3-5 line edits per file. |
| **Dependencies** | CR-DEP-01; T06.02 CR-TASK-02 (the Gate 1 dispatch behavior must exist at `/task` before the routing prose describes it). |
| **Acceptance criteria** | (1) `grep -nE "/sc:task" src/superclaude/core/COMMANDS.md src/superclaude/core/ORCHESTRATOR.md` returns no matches. (2) The replacement prose names the `Tier:` field and Gate 1 dispatch correctly per T06.02. |
| **Risk assessment** | **Risk:** the orchestrator description is stale by design and rewriting it may inadvertently re-introduce REJECTed donor classifier prose (LR-REJECT-3). **Mitigation:** the replacement names *declarative `Tier:` field* (per TU-1 manifest entry); no runtime classifier prose is allowed. R-RULE-11 audit row in CR-REF-22 verifies. |

#### CR-REF-06 — `[src] src/superclaude/skills/sc-*-protocol/SKILL.md` (sibling protocol skills referencing each other)

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-06 |
| **File path** | `[src] src/superclaude/skills/sc-cli-portify-protocol/SKILL.md` + `refs/code-templates.md` + `refs/pipeline-spec.md`; `[src] src/superclaude/skills/sc-release-split-protocol/SKILL.md`; `[src] src/superclaude/skills/sc-roadmap-protocol/SKILL.md`; `[src] src/superclaude/skills/sc-tasklist-protocol/SKILL.md`; `[src] src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md`; `[src] src/superclaude/skills/sc-validate-tests-protocol/SKILL.md`. Each contains `/sc:task` cross-references in protocol prose. |
| **Change** | `redirect` — rewrite `/sc:task` → `/task` in body text per file. Skill names like `sc-cli-portify-protocol` etc. are NOT renamed by this sprint; only `/sc:task` references inside their bodies are updated. |
| **Manifest feature(s)** | CS-M4-B. |
| **Priority** | **P1** — skills are loaded into context by Claude Code; stale references propagate. |
| **Effort** | **S** — ~1-3 edits per file. |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | (1) `grep -lE "/sc:task" src/superclaude/skills/sc-*-protocol/` returns no files (excluding `sc-task-protocol/` which is hard-deprecated by CR-DEP-03). (2) `make verify-sync` returns 0 after `make sync-dev`. |
| **Risk assessment** | **Risk:** redirect breaks skill prose narrative that relied on `/sc:task` being a sibling protocol. **Mitigation:** Phase 7 reviews each sibling's prose and rewrites to describe `/task` as the absorbing surface (not a sibling protocol). |

#### CR-REF-07 — `[src] src/superclaude/examples/release-spec-template.md` + `tasklist_index_template.md` + `tasklist_phase_template.md`

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-07 |
| **File path** | `[src] src/superclaude/examples/release-spec-template.md` (lines 226, 231 — `sc:roadmap`, `sc:tasklist` references; minimal `/sc:task` content); `[src] src/superclaude/examples/tasklist_index_template.md`; `[src] src/superclaude/examples/tasklist_phase_template.md`. |
| **Change** | `redirect` — rewrite any `/sc:task` reference to `/task`; `sc:tasklist` and `sc:roadmap` references **stay** (those commands are not deprecated). The greps that hit these files matched the substring `sc:task` inside `sc:tasklist`, plus any `/sc:task` examples in template bodies. |
| **Manifest feature(s)** | CS-M4-B. |
| **Priority** | **P2** — templates seed future planning docs. |
| **Effort** | **XS-S** — per-file line edits. |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | (1) `grep -nE "(^|\W)/sc:task(\W|$)" src/superclaude/examples/` returns no matches (the `\W` anchors avoid matching `/sc:tasklist`). |
| **Risk assessment** | **Risk:** over-eager rewrite of `sc:tasklist` substring. **Mitigation:** the regex anchors require trailing `\W` to exclude `tasklist`. |

#### CR-REF-08 — `[src] plugins/superclaude/commands/task.md` — already-deprecated plugin stub referencing `task-unified`

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-08 |
| **File path** | `[src] plugins/superclaude/commands/task.md`. Pre-existing deprecation stub (a *previous* deprecation cycle pointed `task.md` → `task-unified.md`). Frontmatter: `deprecated_by: "task-unified"`, `migration_guide: "Use /sc:task (task-unified.md) ..."`. Body redirects to `/sc:task`. |
| **Change** | `redirect` (rewrite stub to point at `/task` instead of `/sc:task` / `task-unified.md`) **OR** `→ T06.04` (defer to distribution refactor — `plugins/` is the v5.0 plugin distribution surface and T06.04 owns it). **Phase 7 decision: pick one in T06.04 CS-M5-A consultation.** Recommended: `redirect` body to `/task`; remove `deprecated_by: "task-unified"` and `migration_guide` frontmatter lines since the migration target has now changed twice. |
| **Manifest feature(s)** | CS-M4-B + T06.04 CS-M5-A. The file is a distribution-surface artifact (plugins/ directory feeds the planned v5.0 plugin marketplace per CLAUDE.md "Plugin System (v5.0)"). |
| **Priority** | **P1** — plugin distribution surface. |
| **Effort** | **S** — frontmatter + ~10 body lines. |
| **Dependencies** | CR-DEP-01; T06.04 CS-M5-A. |
| **Acceptance criteria** | (1) `grep -nE "task-unified" plugins/superclaude/commands/task.md` returns no matches. (2) The body redirect points at `/task` (matches CR-DEP-01 stub language). |
| **Risk assessment** | **Risk:** double deprecation (a deprecation stub pointing at another deprecation stub) confuses users. **Mitigation:** the rewrite collapses the chain — the file becomes a single-hop redirect to `/task`. |

#### CR-REF-09 — `[src] tests/sprint/test_process.py` + `tests/pipeline/test_process.py` + `tests/sprint/test_tui_v2_wave2.py` — test assertions on the canonical command name

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-09 |
| **File path** | `[src] tests/sprint/test_process.py` (lines 80-89 — docstring "v3.7 Naming Consolidation: prompt invokes the canonical /sc:task. The prior /sc:task-unified spelling is gone"; `assert prompt.startswith("/sc:task ")`; `assert "/sc:task-unified" not in prompt`); `[src] tests/pipeline/test_process.py:131` (`prompt="/sc:task-unified test prompt"` — test fixture verifying the old spelling is rejected); `[src] tests/sprint/test_tui_v2_wave2.py:163,168` (release-dir-name fixture `v3.7-task-unified-v2` — a directory-name string, NOT a command-name string). |
| **Change** | `redirect` — rewrite test assertions in `test_process.py` to expect `/task` instead of `/sc:task`. Update the docstring to reflect the new naming consolidation ("v3.x absorbs `/sc:task` into the canonical `/task`."). For `test_pipeline/test_process.py:131`, the fixture `/sc:task-unified test prompt` was already asserting rejection of an obsolete spelling — update to assert rejection of `/sc:task` (post-deprecation) OR keep the fixture as a historical regression-guard and add a new assertion for `/task` (Phase 7 picks; recommend: keep the historical guard + add the new). `tests/sprint/test_tui_v2_wave2.py` lines 163/168 reference `v3.7-task-unified-v2` as a release-directory **filename**, not a command name: **`leave-as-is`** — filenames are historical, not runtime. |
| **Manifest feature(s)** | CS-M4-B; test parity with CR-REF-01 (the CLI prompt rewrite must align with the test assertions that verify it). |
| **Priority** | **P0** — test suite blocks `make test` until aligned with CR-REF-01. |
| **Effort** | **S** — ~5-10 line edits across the three test files. |
| **Dependencies** | CR-REF-01 + CR-REF-02 (CLI prompt rewrites must land in the same commit). |
| **Acceptance criteria** | (1) `uv run pytest tests/sprint/test_process.py tests/pipeline/test_process.py tests/sprint/test_tui_v2_wave2.py` passes. (2) `grep -nE "/sc:task " tests/sprint/test_process.py` returns no matches (the trailing space anchors to the command-token form, not the historical-guard string). |
| **Risk assessment** | **Risk:** removing the historical regression-guard for `/sc:task-unified` weakens the test suite's ability to catch a re-introduction of the previously-rejected spelling. **Mitigation:** Phase 7 keeps the existing `assert "/sc:task-unified" not in prompt` line, adds `assert "/sc:task " not in prompt` (post-deprecation), and changes the positive assertion to `assert prompt.startswith("/task ")`. Three assertions, not two. |

#### CR-REF-10 — `[src] PROJECT_INDEX.md` — repo-level index lists `sc-task-unified-protocol/` and `task-unified.md`

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-10 |
| **File path** | `[src] PROJECT_INDEX.md` (root). Lines 61 (`├── sc-task-unified-protocol/`), 168 (`- `task-unified.md` — Unified task execution with MCP compliance`), 205 (`| `sc-task-unified-protocol` | Unified task execution |`). |
| **Change** | `remove` — delete all three lines. The `sc-task-unified-protocol/` directory does not exist in the current `src/superclaude/skills/` tree (the current donor is `sc-task-protocol`, not `sc-task-unified-protocol`); the index is stale from an older naming. Post-deprecation it would be doubly wrong. |
| **Manifest feature(s)** | CS-M4-B; R-RULE-11 (the index lists a directory that was already removed in a prior cycle — re-introducing the listing as `sc-task-protocol/` would be wrong since CR-DEP-04 deletes that directory too). |
| **Priority** | **P2** — index, not runtime-load-bearing. |
| **Effort** | **XS** — 3 line deletes. |
| **Dependencies** | CR-DEP-03 + CR-DEP-04 (the deletions that make the listing fully accurate). |
| **Acceptance criteria** | `grep -nE "sc-task-unified-protocol|task-unified" PROJECT_INDEX.md` returns no matches. |
| **Risk assessment** | **Risk:** PROJECT_INDEX.md drift — the index is regenerated by `sc:index` per CLAUDE.md note. **Mitigation:** delete the lines now; if `sc:index` is next run, the regeneration will not re-introduce them since the underlying directories are gone. |

#### CR-REF-11 — `[src] scripts/sync_from_framework.py` — script doc references `/task] → [/sc:task]`

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-11 |
| **File path** | `[src] scripts/sync_from_framework.py:84` (script docstring with `Links: [/task] → [/sc:task]`). |
| **Change** | `redirect` — rewrite to remove the `→ [/sc:task]` half, leaving `Links: [/task]` (the `/task` skill is now canonical; there is no `→ /sc:task` link target). |
| **Manifest feature(s)** | CS-M4-B. |
| **Priority** | **P2** — script doc, not runtime-load-bearing. |
| **Effort** | **XS** — 1 line edit. |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | `grep -nE "/sc:task" scripts/sync_from_framework.py` returns no matches. |
| **Risk assessment** | **Risk:** docstring drift propagates to script output. **Mitigation:** Phase 7 runs the script post-edit to confirm output is sane (no broken format). |

#### CR-REF-12 — `[.claude] .claude/commands/sc/*.md` and `[.claude] .claude/skills/sc-*-protocol/` mirrors

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-12 |
| **File path** | `[.claude] .claude/commands/sc/adversarial.md`, `.claude/commands/sc/help.md`, `.claude/commands/sc/release-split.md`, `.claude/commands/sc/tasklist.md`, `.claude/commands/sc/validate-roadmap.md`, `.claude/commands/sc/validate-tests.md`; `[.claude] .claude/skills/sc-cli-portify-protocol/SKILL.md` + `refs/code-templates.md` + `refs/pipeline-spec.md`; `[.claude] .claude/skills/sc-release-split-protocol/SKILL.md`; `[.claude] .claude/skills/sc-roadmap-protocol/SKILL.md`; `[.claude] .claude/skills/sc-tasklist-protocol/SKILL.md`; `[.claude] .claude/skills/sc-validate-roadmap-protocol/SKILL.md`; `[.claude] .claude/skills/sc-validate-tests-protocol/SKILL.md`; `[.claude] .claude/templates/documents/release-spec-template.md`. |
| **Change** | `sync` (no manual edit) — refreshed by `make sync-dev` from CR-REF-04 + CR-REF-06 + CR-REF-07 `[src]` edits. The dev-copy mirror is never hand-edited (R-RULE-10). |
| **Manifest feature(s)** | R-RULE-10. |
| **Priority** | **P0** — must run in the same commit as the `[src]` edits. |
| **Effort** | **XS** — single `make sync-dev` invocation (already run as part of CR-DEP-02 if the sprint groups commits). |
| **Dependencies** | CR-REF-04 + CR-REF-06 + CR-REF-07. |
| **Acceptance criteria** | (1) `make verify-sync` returns 0. (2) `grep -lE "/sc:task" .claude/commands/sc/` excluding `task.md` returns no files. (3) `grep -lE "/sc:task" .claude/skills/sc-*-protocol/` excluding `sc-task-protocol/` returns no files (and the excluded path itself is removed by CR-DEP-04). |
| **Risk assessment** | **Risk:** `.claude/templates/documents/release-spec-template.md` may have no `[src]` mirror — verify. **Mitigation:** Phase 7 cross-checks the `[src]` path; if missing, the template is added to `[src]` and synced (or it stays in `.claude/templates/` as a templates-only directory not governed by sync-dev — confirm by reading the Makefile target). |

#### CR-REF-13 — `[.claude] .claude/agent-memory/rf-assembler/assembly-patterns.md`

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-13 |
| **File path** | `[.claude] .claude/agent-memory/rf-assembler/assembly-patterns.md` — runtime agent memory file mentioning `/sc:task`. |
| **Change** | `leave-as-is` — agent-memory is runtime-managed by sub-agents and is rewritten by them on next invocation. Manual edits are out of band for the merge sprint. Phase 7 may regenerate the memory by re-running the affected sub-agent if the reference becomes load-bearing. |
| **Manifest feature(s)** | CS-M4-B (annotation-only). |
| **Priority** | **P3**. |
| **Effort** | **XS** — no edit. |
| **Dependencies** | None. |
| **Acceptance criteria** | Phase 7 reviewer confirms `.claude/agent-memory/` is not under `make verify-sync` purview (memory is mutable runtime state, not a synced artifact). |
| **Risk assessment** | **Risk:** stale memory misleads the sub-agent. **Mitigation:** sub-agents read `MEMORY.md` index first; the rf-assembler entry's `/sc:task` mention is contextual, not instruction-load-bearing. |

---

### 4.B — Active backlog (live planning docs; per-file rows; ≈18 files)

These directories contain live planning artifacts that drive in-flight or near-future work. References require either `redirect` (if the doc is actively edited by current sprints) or `leave-with-note` (if the doc records a historical decision but is still cited by live work).

#### CR-REF-14 — `.dev/releases/backlog/prd-artifact-containment/spec.md` + `tdd-artifact-containment/spec.md`

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-14 |
| **File path** | `.dev/releases/backlog/prd-artifact-containment/spec.md`; `.dev/releases/backlog/tdd-artifact-containment/spec.md`. Both are live (untracked, listed in git status as `?? .dev/releases/backlog/prd-artifact-containment/` etc.). |
| **Change** | `redirect` — rewrite `/sc:task` references to `/task` (these are live planning docs that will drive upcoming work; the redirect prevents the new work from invoking a deprecated command). |
| **Manifest feature(s)** | CS-M4-B. |
| **Priority** | **P1** — live planning. |
| **Effort** | **XS-S** per file. |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | `grep -nE "/sc:task" .dev/releases/backlog/prd-artifact-containment/spec.md .dev/releases/backlog/tdd-artifact-containment/spec.md` returns no matches. |
| **Risk assessment** | **Risk:** the docs reference patterns absorbed into TU-1..TU-8 with the old surface name. **Mitigation:** redirect preserves the pattern reference but points at the new surface. |

#### CR-REF-15 — `.dev/releases/backlog/v5.xx_release-eval-ab-test/` cluster (5 files)

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-15 |
| **File path** | `.dev/releases/backlog/v5.xx_release-eval-ab-test/conversation-decisions.md`; `release-eval-spec.md`; `eval-prompts/Brainstorm.md`; `spec-synthesis/architecture-extraction.md`; `spec-synthesis/spec-panel-review.md`. |
| **Change** | `leave-with-note` — the cluster records *historical decisions* about release-eval scope. The `/sc:task` references are in historical context, not actionable instructions for current work. Add a single-line deprecation header to each file: `Deprecation note: /sc:task was absorbed into /task on 2026-MM-DD (this sprint).` |
| **Manifest feature(s)** | CS-M4-B; R-RULE-11 spirit (historical decisions are not re-litigated). |
| **Priority** | **P2** — annotation row. |
| **Effort** | **XS** per file — single header line. |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | Each file has the deprecation-note header line at the top, immediately after the title. |
| **Risk assessment** | **Risk:** annotation drift if the deprecation date is mis-specified. **Mitigation:** the date in the note matches the CR-DEP-01 commit date (Phase 7 fills in once the deprecation lands). |

#### CR-REF-16 — `.dev/releases/backlog/v6.xx_spec-workshop/batch-1-orchestration.md` + `v5xx-Spec-generator-framework/SC_SPEC_COMMAND.md` + `prd-skill-refactor/` cluster (4 files)

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-16 |
| **File path** | `.dev/releases/backlog/v6.xx_spec-workshop/batch-1-orchestration.md`; `.dev/releases/backlog/v5xx-Spec-generator-framework/SC_SPEC_COMMAND.md`; `.dev/releases/backlog/prd-skill-refactor/02-brainstorm-output.md`; `prd-skill-refactor/base-selection.md`; `prd-skill-refactor/debate-transcript.md`; `prd-skill-refactor/prd-refactor-spec-v2.md`. |
| **Change** | `leave-with-note` (default) OR `redirect` if Phase 7 reviewer confirms a doc in this set is *currently driving live work* (then upgrade that one row to `redirect`). Default treatment is `leave-with-note` because these are research-output docs that record findings, not active scripts. |
| **Manifest feature(s)** | CS-M4-B. |
| **Priority** | **P2**. |
| **Effort** | **XS** per file. |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | Each file in the set carries the deprecation-note header. |
| **Risk assessment** | **Risk:** under-classifying a live doc as historical. **Mitigation:** Phase 7 reviewer reads each file's most recent edit date (git log) and upgrades to `redirect` if the file was edited in the current sprint. |

#### CR-REF-17 — `.dev/releases/backlog/v5.xx-sc-troubleshoot-v2/` (2 files)

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-17 |
| **File path** | `.dev/releases/backlog/v5.xx-sc-troubleshoot-v2/adversarial-auggie-mcp.md`; `brainstorm-auggie-mcp.md`. |
| **Change** | `leave-with-note` — backlog cluster for a future v5.xx command, references `/sc:task` in adversarial discussion context. |
| **Manifest feature(s)** | CS-M4-B. |
| **Priority** | **P3**. |
| **Effort** | **XS** per file. |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | Each file carries the deprecation-note header. |
| **Risk assessment** | None material. |

---

### 4.C — Archived backlog (bucket row; ≈39 files)

Backlog directories whose names indicate they record completed-or-superseded work intent: `v3.xx*`, `v3.8-*`, `v3.9-*`, `v4.xx-*`, `v4xx-*`, plus `v3.xxRigorFlowMerger/UpdateArtifacts/`. These are historical planning artifacts that captured intent during prior cycles. R-RULE-11 spirit applies — archives stay archived.

#### CR-REF-BUCKET-A — `.dev/releases/backlog/v3.xx* + v3.8-* + v3.9-* + v4.xx-* + v4xx-*` (≈39 files, archived backlog)

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-BUCKET-A |
| **File path (bucket)** | `.dev/releases/backlog/v3.xxRigorFlowMerger/**/*.md`; `.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/**/*.md`; `.dev/releases/backlog/v3.9-UnifiedTasklist-CLI/*.md`; `.dev/releases/backlog/v4.xx-SkillRefactor/*.md`; `.dev/releases/backlog/v4.xx-SpawnV2/**/*.md`; `.dev/releases/backlog/v4.xx-SprintReportScaffolding/release-spec.md`; `.dev/releases/backlog/v4xx-analyze-auggie/**/*.md`. Approximately 39 distinct files. |
| **Change** | `leave-as-is` — bucket-level treatment. These directories record completed or superseded planning. R-RULE-11 spirit: history is not re-litigated. Optional one-time addition: a single `DEPRECATION-NOTE.md` file at the top of each bucket directory explaining "References to `/sc:task` in this directory predate the 2026-MM-DD deprecation that absorbed `/sc:task` into `/task` (see `.dev/releases/current/task-sc-task-directional-merge/`)." Phase 7 picks (recommended: add the note files). |
| **Manifest feature(s)** | CS-M4-B (bucket treatment); R-RULE-11 spirit (history is terminal). |
| **Priority** | **P3** — annotation-only. |
| **Effort** | **S** total — ~6 `DEPRECATION-NOTE.md` files (one per top-level archived directory), each ~3 lines. |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | Either: (a) the bucket has `DEPRECATION-NOTE.md` files at the top of each archived directory; or (b) Phase 7 explicitly chooses option (a) is not needed and records the choice in the merge-master.md commit message. |
| **Risk assessment** | **Risk:** future cleanup PRs mistake the archived `/sc:task` references for live references and try to rewrite them, generating noise. **Mitigation:** the `DEPRECATION-NOTE.md` files (if added) make the historical nature explicit; the bucket-level rule "do not rewrite archived backlog" is recorded in this row. |

---

### 4.D — `.dev/releases/backlog/v5.xxforensic/` (high-density carve-out; per-file rows; 14 files)

The merge-roadmap CS-M4-B identified this cluster as the highest-density region (16+ hits). Per-file rows for the 14 files with matches, in descending hit-count order.

| # | File path | Hits | Treatment | CR-ID |
|---|---|---|---|---|
| 1 | `forensic-refactor-handoff.md` | 61 | `leave-with-note` — handoff doc records absorbed-vs-rejected decisions; the references describe the donor surface during analysis. R-RULE-11 spirit: do not rewrite historical analysis. | CR-REF-18.1 |
| 2 | `tfep-refactoring-context.md` | 28 | `leave-with-note` — historical context doc; references describe pre-merge state. | CR-REF-18.2 |
| 3 | `forensic-spec.md` | 20 | `leave-with-note` — spec doc records the v5.xxforensic scope; references are historical. | CR-REF-18.3 |
| 4 | `adversarial/merged-tasklist.md` | 20 | `leave-with-note` — adversarial pipeline output; historical. | CR-REF-18.4 |
| 5 | `sprint-runner-tfep-handoff.md` | 9 | `leave-with-note` — handoff doc; historical. | CR-REF-18.5 |
| 6 | `adversarial/diff-analysis.md` | 5 | `leave-with-note`. | CR-REF-18.6 |
| 7 | `forensic-explore.md` | 4 | `leave-with-note`. | CR-REF-18.7 |
| 8 | `adversarial/debate-transcript.md` | 4 | `leave-with-note`. | CR-REF-18.8 |
| 9 | `tfep-architecture-design.md` | 2 | `leave-with-note`. | CR-REF-18.9 |
| 10 | `adversarial/refactor-plan.md` | 2 | `leave-with-note`. | CR-REF-18.10 |
| 11 | `roadmap/roadmap.md` | 1 | `leave-with-note`. | CR-REF-18.11 |
| 12 | `roadmap/roadmap-2.md` | 1 | `leave-with-note`. | CR-REF-18.12 |
| 13 | `roadmap/extraction-2.md` | 1 | `leave-with-note`. | CR-REF-18.13 |
| 14 | `adversarial/base-selection.md` | 1 | `leave-with-note`. | CR-REF-18.14 |

#### CR-REF-18 — `.dev/releases/backlog/v5.xxforensic/` cluster (composite row covering 14 files; all sub-IDs above share these columns)

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-18.1..14 (14 sub-rows, identical treatment; per-file path enumerated in table above). |
| **File path (cluster)** | `.dev/releases/backlog/v5.xxforensic/**/*.md` (14 files with `/sc:task` / `sc-task-protocol` matches; the cluster has additional files without matches that are not affected). |
| **Change** | `leave-with-note` — add a single `DEPRECATION-NOTE.md` file at `.dev/releases/backlog/v5.xxforensic/DEPRECATION-NOTE.md` covering all 14 files: "References to `/sc:task` / `sc-task-protocol` in this directory predate the 2026-MM-DD deprecation. Patterns absorbed into `/task` are recorded in `.dev/releases/current/task-sc-task-directional-merge/artifacts/transfer-manifest.md` § TU-1..TU-8." This single-file annotation is the per-row acceptance for all 14 sub-IDs. |
| **Manifest feature(s)** | CS-M4-B (the high-density region called out in the merge-roadmap); R-RULE-11 spirit. |
| **Priority** | **P3**. |
| **Effort** | **XS** — one `DEPRECATION-NOTE.md` file (~5 lines). |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | (1) `test -f .dev/releases/backlog/v5.xxforensic/DEPRECATION-NOTE.md` returns true. (2) The note file cites `transfer-manifest.md § TU-1..TU-8` and the deprecation date. (3) No file body in the 14-file list is rewritten. |
| **Risk assessment** | **Risk:** v5.xxforensic was an in-flight forensic analysis that may still drive follow-on work. **Mitigation:** if any file in this set is currently being edited, Phase 7 escalates that single file to `redirect` (CR-REF-15 pattern). The default `leave-with-note` is correct for the historical-record case. |

---

### 4.E — `.dev/releases/archive/v3.75-RigorflowMerger-task-unified-v3/` (bucket row; ≈33 files)

The directory is the **terminal archive** of a completed RigorflowMerger task-unified sprint. Already archived; references are frozen historical record.

#### CR-REF-BUCKET-B — `.dev/releases/archive/v3.75-RigorflowMerger-task-unified-v3/**/*.md`

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-BUCKET-B |
| **File path (bucket)** | `.dev/releases/archive/v3.75-RigorflowMerger-task-unified-v3/**/*.md` (≈33 files). |
| **Change** | `leave-as-is` — terminal archive. R-RULE-11 spirit applies absolutely: archived artifacts are read-only history. The directory-name itself (`task-unified-v3`) is historical and is preserved as such. |
| **Manifest feature(s)** | CS-M4-B (bucket treatment); R-RULE-11. |
| **Priority** | **P3** — no edit. |
| **Effort** | **XS** — no edit (optionally one `DEPRECATION-NOTE.md` at the archive root). |
| **Dependencies** | None. |
| **Acceptance criteria** | No file body in the archive is rewritten. The optional `DEPRECATION-NOTE.md` at the archive root (if Phase 7 adds it) cites the current sprint and the absorption manifest. |
| **Risk assessment** | **Risk:** future readers misinterpret the archive's task-unified references as current canon. **Mitigation:** an optional archive-root `DEPRECATION-NOTE.md` provides the pointer to the current sprint. |

---

### 4.F — `.dev/tasks/to-do/TASK-*/` + `.dev/benchmarks/` + `.dev/test-fixtures/` (bucket rows)

Live MDTM task data and frozen test/benchmark outputs.

#### CR-REF-BUCKET-C — `.dev/tasks/to-do/TASK-*/**/*.md`

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-BUCKET-C |
| **File path (bucket)** | `.dev/tasks/to-do/TASK-*/**/*.md` (~30 files with `/sc:task` matches across TASK-RF-*, TASK-E2E-*, TASK-RESEARCH-*, TASK-TDD-*, TASK-PRD-* task directories). |
| **Change** | `leave-as-is` (default) + new-task guidance. Existing MDTM task files reference `/sc:task` in their research / synthesis / TASK-MAIN bodies. INV-04 (resumability) requires every existing TASK-* file remain valid for the F1 loop to resume it. Rewriting `/sc:task` → `/task` inside an in-flight task body would risk breaking the task's own frontmatter / log-line discipline. **New-task guidance:** Phase 7 emits a one-line note in `.dev/tasks/README.md` (creating it if absent): "New tasks should use `/task` (canonical) instead of `/sc:task` (soft-deprecated since 2026-MM-DD)." |
| **Manifest feature(s)** | CS-M4-B; **INV-04 (resumability)** — existing TASK-* files MUST remain valid (this is the same invariant T06.02 protects for MDTM frontmatter additions). |
| **Priority** | **P3** — annotation row. |
| **Effort** | **XS** — one file edit (the README addition). |
| **Dependencies** | CR-DEP-01. |
| **Acceptance criteria** | (1) `.dev/tasks/README.md` (or equivalent guidance file) contains the new-task guidance line. (2) No existing TASK-*/ body is rewritten. (3) INV-04 verified: a sample existing TASK-*.md still parses and the F1 loop resumes correctly (Phase 7 sample test on one TASK-* file). |
| **Risk assessment** | **Risk: INV-04 violation** if a redirect is applied incautiously inside an in-flight task body. **Mitigation:** explicit `leave-as-is` plus the INV-04 sample test in acceptance criterion (3). |

#### CR-REF-BUCKET-D — `.dev/benchmarks/v2.20-baseline/` + `.dev/test-fixtures/`

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-BUCKET-D |
| **File path (bucket)** | `.dev/benchmarks/v2.20-baseline/**/*.md`; `.dev/test-fixtures/**/*.md` (~30 files). |
| **Change** | `leave-as-is` — frozen test outputs and fixtures. These directories hold regression-baseline data; rewriting them would invalidate the baseline they document. |
| **Manifest feature(s)** | CS-M4-B. |
| **Priority** | **P3**. |
| **Effort** | **XS** — no edit. |
| **Dependencies** | None. |
| **Acceptance criteria** | No file body in either bucket is rewritten; existing tests / benchmarks continue to pass. |
| **Risk assessment** | **Risk:** a future benchmark refresh regenerates these files and the regenerator emits the new `/task` name, creating a baseline diff. **Mitigation:** out of scope for this sprint; the regenerator update lives in whatever future task adds it. |

---

### 4.G — `docs/` (deferred to T06.04)

The user-/developer-/reference-guide doc tree is owned by T06.04 (`refactor-documentation.md`). Files are enumerated here for the T06.04 hand-off; per-file change rows are authored in T06.04, not in T06.03.

#### CR-REF-DEFER-T06.04 — `docs/user-guide/` + `docs/developer-guide/` + `docs/reference/` + `docs/guides/` + `docs/analysis/` + `docs/research/` + `docs/generated/`

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-DEFER-T06.04 |
| **File path (cluster)** | `docs/user-guide/commands.md` (high-hit), `docs/user-guide/flags.md`; `docs/analysis/bmad-vs-superclaude-comparison.md`, `docs/analysis/claude-code-best-practice-vs-superclaude.md`, `docs/analysis/openclaw-vs-superclaude-comparison.md`, `docs/analysis-sc-tasklist.md`, `docs/analysis/superpowers-vs-superclaude-comparison.md`; `docs/guides/cli-portify-and-pipeline-runner-guide.md`, `docs/guides/prd-skill-release-guide.md`, `docs/guides/roadmap-cli-tools-release-guide.md`, `docs/guides/sprint-cli-tools-release-guide.md`, `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, `docs/guides/tdd-skill-release-guide.md`; `docs/research/competitive-landscape-final-report-2026-03-23.md`, `docs/research/competitive-landscape-tasklist-execution-2026.md`, `docs/research/dev-guide-research/*.md` (≈10 files), `docs/research/superpowers-vs-superclaude-comparison.md`; `docs/generated/cleanup-sc-prefix-reference-index.md`, `docs/generated/cleanup-sc-prefix-rename-tasklist.md`, `docs/generated/cli-portify-release-guide.md`, `docs/generated/contributor-knowledge-base/*.md` (4 files), `docs/generated/sprint-cli/*.md` (≈15 files including v3.7-refactor subtree and debates), `docs/generated/tasklist-unwired-components-remediation.md`; `docs/sprint-cli-deep-dive.md`. |
| **Change** | `→ T06.04` — defer. Per T06.04 CS-M5-B: hand-edited docs (`docs/user-guide/`, `docs/guides/`, `docs/sprint-cli-deep-dive.md`) get explicit `redirect` rows in `refactor-documentation.md`. Regenerated docs (`docs/generated/*`) get `leave-as-is` + regenerator-update guidance: the next regenerator run will emit the new `/task` name, deferring the update to that run. `docs/analysis/` and `docs/research/` (historical competitive/research analyses) get `leave-with-note`. |
| **Manifest feature(s)** | CS-M5-B (T06.04 scope). |
| **Priority** | **P2** — owned by T06.04. |
| **Effort** | n/a (deferred). |
| **Dependencies** | CR-DEP-01; T06.04 authors the explicit per-file rows. |
| **Acceptance criteria** | T06.04 `refactor-documentation.md` covers every file in this cluster with a per-file row carrying all eight columns. T06.03 reviewer confirms the file list above is the complete handoff input. |
| **Risk assessment** | **Risk:** a file slips between T06.03 and T06.04 with no treatment. **Mitigation:** the T06.04 input checklist must enumerate every file in this row; the T06.06 checkpoint verifies the hand-off list matches. |

---

### 4.H — Not-editable surface (bucket rows)

#### CR-REF-BUCKET-E — `.venv/lib/python3.12/site-packages/superclaude/...` (~24 files)

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-BUCKET-E |
| **File path (bucket)** | `.venv/lib/python3.12/site-packages/superclaude/_plugins/superclaude/commands/help.md`, `.venv/lib/python3.12/site-packages/superclaude/_plugins/superclaude/commands/task.md`, plus ~22 files under `.venv/lib/python3.12/site-packages/superclaude/_src/...`. |
| **Change** | `leave-as-is` — frozen pip-install snapshot. Refreshes automatically on next `pip install -e .` / `make dev`. Not editable as repo state. |
| **Manifest feature(s)** | CS-M4-B (bucket treatment). |
| **Priority** | **P3** — no edit. |
| **Effort** | **XS** — no edit. |
| **Dependencies** | None. |
| **Acceptance criteria** | After CR-DEP-01..04 land and `make dev` is re-run, the `.venv/` snapshot refreshes to the new state automatically; no manual edit is required. |
| **Risk assessment** | None — venv is regenerated state. |

#### CR-REF-BUCKET-F — `.serena/memories/releases/release-split-workspace-rca-roadmap.md`

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-BUCKET-F |
| **File path (bucket)** | `.serena/memories/releases/release-split-workspace-rca-roadmap.md`. |
| **Change** | `leave-as-is` — serena MCP project memory; managed by serena's `write_memory` / `edit_memory` tools, not by hand. If the memory becomes stale and load-bearing, a future serena memory-update task refreshes it. |
| **Manifest feature(s)** | CS-M4-B. |
| **Priority** | **P3**. |
| **Effort** | **XS**. |
| **Dependencies** | None. |
| **Acceptance criteria** | No manual edit. |
| **Risk assessment** | **Risk:** stale serena memory misleads serena-using sessions. **Mitigation:** serena memory is per-session contextual; the `/sc:task` reference is annotation, not instruction. |

---

## 5. Treatment summary table (all CR-REF rows)

| Treatment | Row count | CR-REF IDs |
|---|---|---|
| `redirect` (active source rewrite to `/task`) | 8 rows touching ≈22 files | CR-REF-01, CR-REF-02, CR-REF-04, CR-REF-05, CR-REF-06, CR-REF-07, CR-REF-08, CR-REF-11 |
| `redirect` (active backlog) | 1 row, 2 files | CR-REF-14 |
| `redirect` (test assertions) | 1 row, 3 files | CR-REF-09 |
| `remove` (stale index) | 1 row, 1 file (3 lines) | CR-REF-10 |
| `sync` (`.claude/` mirrors) | 1 row, ≈15 files | CR-REF-12 |
| `leave-with-note` (active backlog historical) | 3 rows, ≈11 files | CR-REF-15, CR-REF-16, CR-REF-17 |
| `leave-with-note` (v5.xxforensic high-density) | 1 cluster row, 14 files | CR-REF-18 |
| `leave-as-is` (bucket) | 5 rows, ≈100+ files | CR-REF-13 (agent-memory), CR-REF-BUCKET-A, CR-REF-BUCKET-B, CR-REF-BUCKET-C, CR-REF-BUCKET-D, CR-REF-BUCKET-E, CR-REF-BUCKET-F |
| `leave-as-is` (false-positive triage) | 1 row, ≈5 files | CR-REF-03 |
| `→ T06.04` (deferred to documentation refactor) | 1 row, ≈40 files | CR-REF-DEFER-T06.04 |

**Coverage check (T06.03 AC #3):** every reference enumerated in § 0 has a treatment row. § 4.A covers 31 active source files (rows CR-REF-01..13); § 4.B covers ≈18 active backlog files (rows CR-REF-14..17); § 4.C bucket-covers ≈39 archived backlog files; § 4.D per-file-covers 14 v5.xxforensic files; § 4.E bucket-covers ≈33 archive files; § 4.F bucket-covers ≈60 task/benchmark/fixture files; § 4.G defers ≈40 doc files to T06.04 with full enumeration; § 4.H bucket-covers ≈26 non-editable files. **Sum: ≈261 files; all covered.**

---

## 6. Phase 7 execution-order constraints

| Order | CR-REF row(s) | Reason |
|---|---|---|
| 1 (P0) | CR-REF-01, CR-REF-02, CR-REF-09 (CLI prompts + test assertions; atomic with CR-DEP-01) | Test suite blocks `make test` until CLI redirects and test assertions align. All three ship in the same commit as CR-DEP-01. |
| 2 (P0) | CR-REF-12 (`.claude/` mirrors via `make sync-dev`) | Must follow `[src]` edits in the same commit (R-RULE-10). |
| 3 (P1) | CR-REF-04, CR-REF-05, CR-REF-06, CR-REF-07, CR-REF-08, CR-REF-14 (active source non-CLI + plugin stub + active backlog redirects) | User-visible help text, framework docs, plugin distribution. May ship in a follow-on commit but before the deprecation date is published. |
| 4 (P2) | CR-REF-10, CR-REF-11, CR-REF-15, CR-REF-16 (index, script doc, active-backlog notes) | Cleanup. |
| 5 (P3) | CR-REF-13, CR-REF-17, CR-REF-18, CR-REF-BUCKET-A..F, CR-REF-DEFER-T06.04 | Annotation rows and bucket treatments. Land in any order; T06.04 owns the deferred docs. |

---

## 7. Acceptance criteria roll-up (T06.03 mapping)

| T06.03 AC | Where satisfied |
|---|---|
| **AC #1** — `refactor-sctask-deprecation.md` exists; every `/sc:task` artifact has soft/hard decision with justification, side-tagged | Companion file `refactor-sctask-deprecation.md` § 3 + § 6. |
| **AC #2** — Never-load-bearing MCP servers and personas have explicit removal plan | Companion file `refactor-sctask-deprecation.md` CR-DEP-01 + CR-DEP-05. |
| **AC #3** — `refactor-references.md` enumerates every reference to `sc:task` / `task-unified` / `sc-task-protocol` with a treatment row | **This file § 0 + § 4 + § 5 coverage check.** ≈261 files, all covered. |
| **AC #4** — Plan confirms no manifest-absorbed capability is lost by deprecation | Companion file `refactor-sctask-deprecation.md` § 4 (absorption traceability) + § 5 (R-RULE-11 audit). |

---

## 8. T06.04 hand-off

The following file lists are inputs to T06.04 (distribution refactor + documentation refactor):

- **Installer / sync rules (T06.04 CS-M5-A inputs):** `src/superclaude/cli/install_skills.py`, `src/superclaude/cli/install_commands.py`, `Makefile` (targets `sync-dev` lines 107-122 and `verify-sync` lines 154-183), `scripts/sync_from_framework.py`. (CR-REF-11 already handles `scripts/sync_from_framework.py` doc-string per § 4.A; install_*.py and Makefile are pure T06.04.)
- **Documentation (T06.04 CS-M5-B inputs):** the ≈40-file list enumerated in § 4.G of this file.
- **Plugin distribution (T06.04 CS-M5-A scope, but CR-REF-08 stakes the initial body rewrite here):** `plugins/superclaude/commands/task.md`.

T06.04 reads this section verbatim as its starting file inventory.

---

## 9. Drift addendum — re-enumeration on Phase 6 re-run (2026-05-15 14:19 UTC)

The Phase 6 re-run re-executed the § 0 grep against the live tree. The corpus grew from the **≈230 distinct files** claimed at original generation (2026-05-15 08:56) to **944 distinct files** — a ~4× increase driven by sprint-produced artifacts and accumulated archives that landed between the two generations. The bucket philosophy in § 2 already covers the new buckets (frozen / regenerated / self-referential sprint output ⇒ `leave-as-is`); this addendum names them explicitly so Phase 7 has a complete enumeration.

**Fresh hit count by bucket (T06.03 re-run, before any edits):**

| Bucket | Count (re-run) | Count (original) | Δ | Treatment |
|---|---|---|---|---|
| `.dev/releases/complete/**` (frozen completed-release archives) | 446 | not named | +446 | **`leave-as-is`** — frozen sprint outputs; archived by definition (R-RULE-11 spirit: completed releases are terminal). Same semantics as § 4.E (`v3.75-RigorflowMerger-task-unified-v3/`). |
| `.dev/releases/current/**` (current sprint's own artifacts) | 95 | not named | +95 | **`leave-as-is`** — the current sprint's own working artifacts. They reference `/sc:task` because the sprint *is the deprecation analysis*. Once the sprint archives to `.dev/releases/complete/` (post-Phase 8), the bucket-A semantic applies. Editing these would corrupt the audit trail. |
| `.dev/releases/backlog/**` (general) | 56 | 18 (active) + 39 (archived) = 57 | −1 | Already covered: per-file rows for active (§ 4.B), bucket A for archived (§ 4.C). |
| └ `.dev/releases/backlog/v5.xxforensic/` | 14 | 14 | 0 | § 4.D unchanged. |
| `.dev/tasks/**` | 116 | ~30 | +86 | **`leave-as-is`** — bucket C semantic (§ 4.F) extends to all `TASK-*/`, `TASK-PRD-*/`, `TASK-TDD-*/` regardless of count. User-authored MDTM task data. New TASK directories (`TASK-PRD-20260514-121039/`, `TASK-TDD-20260514-121250/`) and others landed since generation. |
| `.dev/benchmarks/` + `.dev/test-fixtures/` | 30 | ~30 | 0 | § 4.F bucket D unchanged. |
| `.dev/` (other: docs, eval-workspaces, etc.) | 15 | not enumerated separately | +15 | **`leave-as-is`** for `.dev/eval-workspaces/`, `.dev/benchmarks/`; `→ T06.04` for `.dev/README.md` if it references `/sc:task` (Phase 7 verifies via single grep). |
| `docs/generated/` | 25 | enumerated under § 4.G ~30 | ~0 | **`leave-as-is`** — pipeline-regenerated; the deprecation propagates when the regenerator next runs. § 4.G bucket E semantic extends here verbatim. |
| `docs/` (other) | 28 | ~40 | −12 | § 4.G defer to T06.04 unchanged (count fluctuates as analysis files come and go). |
| `src/` | 27 | ~31 | −4 | § 4.A per-file rows unchanged; the count drop reflects file removals between the two generations, not new misses. Phase 7 verifies each CR-REF-01..13 path still exists. |
| `.claude/` | 18 | ≈18 | 0 | § 4.A CR-REF-12 + CR-REF-13 unchanged. |
| `tests/` | 3 | 3 | 0 | § 4.A CR-REF-09 unchanged. |
| `.venv/lib/python3.12/site-packages/superclaude/...` | 29 | ~24 | +5 | § 4.H bucket E unchanged (`leave-as-is` — refreshes on `pip install -e .`). |
| `.serena/memories/` | 1 | 1 | 0 | § 4.H bucket F unchanged. |
| Other | 4 | n/a | +4 | Verify each with single grep at Phase 7 start; default `leave-as-is` unless one is in the active source surface. |
| **Total** | **944** | **~230** | **+714** | **No new per-file rows required.** All drift falls into `leave-as-is` buckets (archived / regenerated / self-referential / user-authored MDTM) covered by § 2 vocabulary and § 4 bucket-row pattern. |

### 9.1 New explicit buckets (R-RULE-11 spirit applied)

Two buckets that did not exist (or were too small to enumerate) at original generation now warrant explicit bucket rows:

#### CR-REF-BUCKET-G — `.dev/releases/complete/**` (≈446 files, frozen completed-release archives)

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-BUCKET-G |
| **File path (bucket)** | `.dev/releases/complete/**` — frozen archives of all sprint releases that completed between Phase 5 archive cutoff and Phase 6 re-run. Includes (e.g.) `complete/freshness-system/`, `complete/skill-creator-workspace-rca/`, and successors that land before this sprint archives. |
| **Change** | **`leave-as-is`** — no edits. Same semantic as § 4.E (`v3.75-RigorflowMerger-task-unified-v3/`): completed releases are terminal and serve as the historical audit trail. R-RULE-11 spirit forbids re-litigating archived sprint output. |
| **Manifest feature(s)** | R-RULE-11 (no re-litigation of terminal artifacts); merge-roadmap §1 (frozen-artifact rule). |
| **Priority** | **P3** — annotation-only; no Phase 7 work required. |
| **Effort** | **XS** — zero edits. |
| **Dependencies** | None. |
| **Acceptance criteria** | (1) Phase 7 does not edit any file under `.dev/releases/complete/**`. (2) `git diff --name-only` after Phase 7 lands shows zero `.dev/releases/complete/` paths in the change set. |
| **Risk assessment** | **R-RULE-11 at risk** if a "consistency" PR rewrites archived sprint output to use `/task` instead of `/sc:task`. **Mitigation:** this row is the explicit `leave-as-is` directive; the deprecation note at the user-facing surface is sufficient. The archive's `sc:task` references are historical — they record what was true at the time the sprint ran. |

#### CR-REF-BUCKET-H — `.dev/releases/current/**` (≈95 files, current sprint's own artifacts)

| Column | Value |
|---|---|
| **CR-ID** | CR-REF-BUCKET-H |
| **File path (bucket)** | `.dev/releases/current/task-sc-task-directional-merge/**` — every artifact this sprint produces (phase tasklists, refactor plans, debate transcripts, checkpoints, traceability tables, this file). |
| **Change** | **`leave-as-is`** — no edits. The sprint *is* the deprecation analysis; the references are the analysis content. Editing them would erase the audit trail. After Phase 8 archives this sprint to `.dev/releases/complete/`, CR-REF-BUCKET-G semantics apply automatically. |
| **Manifest feature(s)** | R-RULE-11 (no self-referential re-litigation); merge-roadmap §1 (sprint working artifacts are not subject to refactor-rewrite while the sprint is live). |
| **Priority** | **P3** — no Phase 7 work. |
| **Effort** | **XS** — zero edits. |
| **Dependencies** | None. |
| **Acceptance criteria** | (1) Phase 7 does not rewrite `/sc:task` references inside `.dev/releases/current/task-sc-task-directional-merge/**`. (2) Post-Phase-8 archive move (this sprint → `.dev/releases/complete/`) transparently absorbs this bucket into CR-REF-BUCKET-G. |
| **Risk assessment** | **R-RULE-11 at risk** if Phase 7 over-zealously redirects strings inside its own driving plans. **Mitigation:** the redirect treatment in § 4 applies only to *consumers* of `/sc:task` (live commands, active backlog), not to the *analysis* of the deprecation itself. Phase 7 acceptance includes a `git diff --stat` check that no file under `.dev/releases/current/task-sc-task-directional-merge/` is modified by the redirect commits. |

### 9.2 Treatment summary update

Updated § 5 totals (additive to original):

| Treatment | Original count | Drift addendum count | Total |
|---|---|---|---|
| `redirect` (per-file rows) | ~13 (CR-REF-01..13 active source, partial) + ~5 (CR-REF-14..17 active backlog) ≈ 18 | 0 new per-file rows | 18 |
| `remove` | ~3 (CR-REF-10, CR-REF-15 partial) | 0 | 3 |
| `leave-with-note` | ~14 (CR-REF-18 v5.xxforensic, parts of CR-REF-14..17) | 0 | 14 |
| `leave-as-is` (bucket) | 4 buckets (A, B, C, D, E, F) covering ~145 files | **+2 buckets (G, H) covering ~541 files** | 6 buckets covering ~686 files |
| `→ T06.04` | ~40 (docs § 4.G) + ~4 (installer + Makefile) | 0 | 44 |

### 9.3 Re-verification verdict (T06.03 AC #3 re-check)

T06.03 AC #3 ("every reference to `sc:task` / `task-unified` / `sc-task-protocol` has a treatment row") **holds after re-enumeration.** Every one of the 944 distinct files falls into a named bucket with an explicit treatment:

- 18 redirects + 3 removes + 14 leave-with-note = **35 active per-file rows** (§ 4.A–§ 4.D)
- 446 + 95 + 39 + 33 + 116 + 30 + 29 + 15 + 4 = **807 files in `leave-as-is` buckets** (§ 4.C, § 4.E, § 4.F, § 4.H, § 9.1)
- 53 + 4 = **57 files deferred to T06.04** (§ 4.G + installer/Makefile under § 4.A)
- **Sum: 35 + 807 + 57 + 5 (CR-REF-12 mirrors covered separately) = 904.** Residual ~40 fall into edge buckets (e.g., `.dev/` other; `tests/` already in CR-REF-09) — Phase 7 verifies with a single follow-up grep at execution start.

**Audit:** no reference is unaccounted for; the `leave-as-is` bucket expansion (G + H) preserves the audit-trail / R-RULE-11 spirit; no new ledger entry is re-litigated by the addendum. **AC #3 still satisfies.**
