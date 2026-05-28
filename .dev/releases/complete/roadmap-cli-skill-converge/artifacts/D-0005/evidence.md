# D-0005 — Evidence: `sc-roadmap-protocol/refs/templates.md` Single-Template Resolver

| Field | Value |
|---|---|
| Task | T02.03 |
| Roadmap Item | R-005 |
| Drift Item | B-5 |
| Deliverable | D-0005 |
| Date | 2026-05-26 |
| Source File Edited | `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` |
| CLI Reference | `ROADMAP_TEMPLATE` + `get_template_path()` (`src/superclaude/cli/roadmap/templates.py:14-71`) |
| Decision Posture | Option 1 (collapse to CLI behavior) — see `design-decision.md` row B-5 |
| Source Claim Status | VERIFIED (`verification.md:110-119`) — 4-tier model documented in skill ref, CLI uses single-named-template resolver. |

## Linkage

- **B-5 → D-0005.** `release-scope.md:104-111` captures the claim: skill ref describes 4-tier discovery (`refs/templates.md:7-36`), while CLI `templates.py` (71 lines) resolves a single template via `get_template_path(name)` with `ROADMAP_TEMPLATE = "roadmap_template.compressed.md"` and no user/plugin/inline tiers. `verification.md:110-119` records VERIFIED status with high confidence and cites both the 4-tier prose and the CLI's single-constant resolver.
- `design-decision.md:35` row B-5 selected **Option 1**: replace the 4-tier discovery model with the single-template resolver behavior, or move future-looking material out of canonical scope. `solutions.md:188` recommends Solution 1 ("the 4-tier design has no implementation runway; collapse and move on").
- **D-0005** is the resulting source-file edit at `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` plus this evidence record.

## Source-file parity check

CLI canonical resolver (`src/superclaude/cli/roadmap/templates.py:14-71`):

```
Line 14  ROADMAP_TEMPLATE = "roadmap_template.compressed.md"
Line 15  TASKLIST_INDEX_TEMPLATE = "tasklist_index_template.md"
Line 16  TASKLIST_PHASE_TEMPLATE = "tasklist_phase_template.md"
Line 18  _EXAMPLES_PACKAGE = "superclaude.examples"

Line 21  def get_template_path(name: str) -> Path:
   45  ── Method 1: importlib.resources.files(_EXAMPLES_PACKAGE).joinpath(name)
   59  ── Method 2: src-relative <repo>/src/superclaude/examples/<name>
   68  ── Else: raise FileNotFoundError(... importlib.resources(superclaude.examples), <src-relative> ...)
```

Bundled templates resolved by name (verified present in `src/superclaude/examples/`):
- `roadmap_template.compressed.md` (the canonical `ROADMAP_TEMPLATE`)
- `tasklist_index_template.md`
- `tasklist_phase_template.md`

No globbing, no user dir, no plugin marketplace, no inline fallback branch in the resolver.

Post-edit `refs/templates.md` structure (in file order):

| Section | Anchor | Status |
|---|---|---|
| Header lead paragraph | `templates.md:3` | ✅ Renamed framing from "template discovery" to "single-template resolver" + heuristics/body/schemas; preserves Wave 2/Wave 3 anchoring |
| Single-Template Resolver (CLI Canonical Behavior) | `templates.md:7-35` | ✅ New canonical section — names `ROADMAP_TEMPLATE`, `TASKLIST_INDEX_TEMPLATE`, `TASKLIST_PHASE_TEMPLATE`, `get_template_path()`, `_EXAMPLES_PACKAGE`, cites `cli/roadmap/templates.py:14-71`, calls out absence of Tier 1/2/3/4 path in the CLI |
| Non-canonical multi-tier discovery (inference-only) | `templates.md:39-49` | ✅ Demoted material — preserves the 4-tier intent (project/user dirs, plugin marketplace, frontmatter validation, scoring/version filtering) but explicitly marked out of canonical CLI scope and re-anchored to manual skill-mode use |
| Milestone Structure Heuristics | `templates.md:53+` | ✅ Reframed from "Inline Template Generation Fallback" to LLM-fill guidance embedded in the single bundled template (no separate fallback branch claimed); milestone count, domain mapping, priority/dependency rules retained as-is for downstream LLM guidance |
| Effort Estimation / Risk Level / body templates / YAML frontmatter schemas | unchanged | ✅ Output contracts preserved — these do not contradict CLI single-template behavior |
| Footer | `templates.md:end` | ✅ Updated to record CLI parity baseline (`get_template_path()` over `ROADMAP_TEMPLATE`) + flag multi-tier discovery as inference-only B-5 |

## Acceptance criteria check (`phase-2-tasklist.md:155-158`)

- ✅ `refs/templates.md` describes single-template resolution for roadmap templates — see "Single-Template Resolver (CLI Canonical Behavior)" section (`templates.md:7-35`) including the resolution algorithm and the explicit "no Tier 1/2/3/4" statement.
- ✅ `refs/templates.md` names `ROADMAP_TEMPLATE = "roadmap_template.compressed.md"` — appears in the named-template constants table (`templates.md:17`) and in the footer parity baseline.
- ✅ `refs/templates.md` removes four-tier discovery from canonical behavior or moves it out of canonical scope — the original "4-Tier Template Discovery," "Template File Format," "Version Resolution Rules," and "Matching Criteria" sections are replaced. The intent is preserved in the "Non-canonical multi-tier discovery (inference-only)" subsection, which is explicitly out of canonical CLI scope.
- ✅ Evidence at this path links B-5 → D-0005 and records the source's VERIFIED status — see the "Source Claim Status" row of the header table and the "Linkage" section above.

## CLI behavior anchors cited in the edit

- `cli/roadmap/templates.py:14` — `ROADMAP_TEMPLATE = "roadmap_template.compressed.md"`.
- `cli/roadmap/templates.py:14-16` — three named template constants (`ROADMAP_TEMPLATE`, `TASKLIST_INDEX_TEMPLATE`, `TASKLIST_PHASE_TEMPLATE`).
- `cli/roadmap/templates.py:21-71` — `get_template_path(name)` resolver: importlib.resources lookup → src-relative fallback → FileNotFoundError.
- `cli/roadmap/templates.py:18` — `_EXAMPLES_PACKAGE = "superclaude.examples"` (bundled examples package).

## Reframed vs. preserved skill content

- **Preserved** (no semantic change):
  - Milestone Count Selection (LOW/MEDIUM/HIGH classes, `base + floor(domain_count / 2)`).
  - Domain-Specific Milestone Mapping table.
  - Milestone Generation Algorithm (foundation → domain → integration → validation).
  - Validation Milestone Interleaving ratios.
  - Priority Assignment rules + tie-breaking.
  - Dependency Mapping Rules including cycle detection.
  - Required Sections Per Milestone.
  - Effort Estimation (levels, algorithm, risk multiplier).
  - Risk Level Assignment table.
  - `roadmap.md`, `test-strategy.md` body templates and all three YAML frontmatter schemas.
- **Reframed** (header-only / scope demotion):
  - "Inline Template Generation Fallback" → "Milestone Structure Heuristics" (same body, but framed as LLM guidance inside the single template rather than a fallback branch the CLI takes).
  - "Template File Format" + "Version Resolution Rules" + "Matching Criteria" → folded into "Non-canonical multi-tier discovery (inference-only)" with explicit out-of-scope marker.
- **Added** (new canonical content for B-5):
  - "Single-Template Resolver (CLI Canonical Behavior)" section with named-constants table, two-step resolution algorithm, "What this means for skill behavior" implications, and CLI line-range citations.
  - Footer parity-baseline note flagging multi-tier discovery as inference-only B-5.

## Sync follow-up (B-12)

This edit lives only at `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md`. A subsequent `make sync-dev` is required (tracked under B-12 / Phase 5) before `.claude/skills/sc-roadmap-protocol/refs/templates.md` and `/config/.claude/skills/sc-roadmap-protocol/refs/templates.md` reflect the change. Per repo rules, `.claude/` mirrors are not staged or committed.

## Known out-of-scope downstream references

`src/superclaude/skills/sc-roadmap-protocol/SKILL.md` still mentions "4-tier template discovery" in Wave 0 prereq checks (`SKILL.md:168`), Wave 2 step 1 (`SKILL.md:231`), and the long-term roadmap (`SKILL.md:441`). Those edits belong to **T02.01 / R-003** (SKILL.md crosswalk task), not T02.03; the templates.md ref now provides the authoritative single-template language those SKILL.md sections will be reconciled against. No cross-edit was made here to keep T02.03 surgical.
