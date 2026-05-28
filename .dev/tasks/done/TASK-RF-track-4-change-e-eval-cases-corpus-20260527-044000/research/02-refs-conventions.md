# Research Output: refs/ Directory Conventions

**Track:** 4 of 4 (Change E — calibrator-eval-cases.md)
**Topic:** Patterns & Conventions of the existing refs/ directory
**Date:** 2026-05-27
**Researcher:** refs-conventions
**Status:** Complete

---

## Purpose

Document the formatting, structural, and content conventions of the existing `src/superclaude/skills/sc-troubleshoot-protocol/refs/` directory so the NEW file `calibrator-eval-cases.md` lands consistent with its siblings.

---

## Section 1: Directory inventory

Path: `src/superclaude/skills/sc-troubleshoot-protocol/refs/`

| File | Lines | Purpose (1 sentence) | H1 heading style |
|------|-------|----------------------|------------------|
| `doc-discovery.md` | 182 | Defines Wave 1.5 documentation-grounding rules — three parallel discovery branches, per-branch schemas, and the synthesised Documentation Context Card template. | `# Documentation Grounding Rules` (L1) |
| `escalation-rubric.md` | 52 | Rubric for calibrating Tier 1 hypothesis confidence and deciding whether to escalate to Tier 2. | `# Escalation Rubric` (L1) |
| `hypothesis-card-template.md` | 152 | Template/schema each agent (root-cause-analyst, Tier 2 agents) uses to emit a single proposed cause-and-fix card. | `# Hypothesis Card Template` (L1) |
| `remediation-handoff.md` | 122 | Defines the Wave 6 Tier 3 remediation chain — user offer, task-builder phase, pre/post-execution gates. | `# Tier 3 Remediation Handoff (Wave 6)` (L1) |
| `report-template.md` | 196 | Template for the final REPORT.md deliverable of every `/sc:troubleshoot` invocation. | `# REPORT.md Template` (L1) |
| `triage-checklist.md` | 65 | Wave 1 checklist passed to the root-cause-analyst — pre-investigation grounding, cause-class scan, evidence-or-drop, fix sketch. | `# Triage Checklist (Wave 1)` (L1) |

(Source: `ls -la` of refs/ + `wc -l`.)

---

## Section 2: H1 title conventions

Every refs/ file opens with a single H1 on line 1 (`# Title Case Phrase`). Examples:

- `escalation-rubric.md:1` — `# Escalation Rubric`
- `hypothesis-card-template.md:1` — `# Hypothesis Card Template`
- `triage-checklist.md:1` — `# Triage Checklist (Wave 1)`
- `doc-discovery.md:1` — `# Documentation Grounding Rules`
- `remediation-handoff.md:1` — `# Tier 3 Remediation Handoff (Wave 6)`
- `report-template.md:1` — `# REPORT.md Template`

Observations:
- All Title Case.
- All exactly one H1 per file (the H1 is never repeated lower in the file).
- Some include a parenthetical wave label (`(Wave 1)`, `(Wave 6)`); others do not. Both forms are accepted.
- No emoji, no decorative characters.

**Confirmation for new file:** `# Calibrator Eval Cases` per proposal L299 is consistent with this pattern (Title Case, no parenthetical, single H1).

---

## Section 3: Intro paragraph conventions

Every refs/ file opens with a short (1–3 sentence) intro paragraph IMMEDIATELY after the H1 (single blank-line gap H1 → blank → paragraph). The intro describes WHO consumes the file and/or WHEN it is loaded.

Examples:

- `escalation-rubric.md:3` — "Used in Wave 1.7 (to calibrate the Tier 1 hypothesis confidence) and in Wave 2 (to decide whether to escalate to Tier 2)."
- `hypothesis-card-template.md:3` — "Used by every agent that produces a hypothesis — `root-cause-analyst` in Wave 1.7, and every Tier 2 agent in Wave 3."
- `triage-checklist.md:3` — "Passed to the `root-cause-analyst` agent as part of the Tier 1 brief. The agent uses this to structure its investigation; the skill itself does not iterate the checklist mechanically."
- `doc-discovery.md:3` — "Wave 1.5 of the sc:troubleshoot protocol. Loaded on demand by Wave 1.5 only."
- `remediation-handoff.md:3` — "Loaded only when `--fix` is set and Wave 5 produced a `success` (not `partial`) report. Drives the offer + task-builder chain."
- `report-template.md:3` — "The final deliverable of every `/sc:troubleshoot` invocation, regardless of tier. Loaded only in Wave 5."

Observations:
- Intro starts with a verb participle or noun phrase describing role ("Used in...", "Passed to...", "Loaded only...", "The final deliverable...").
- Always sub-page length (1–2 sentences, occasionally 3).
- No prologue/abstract section headings (no `## Overview`, no `## Purpose`); the intro stands directly after H1.

**Confirmation for new file:** Proposal L301 supplies the intro: "Golden hypothesis cards + expected calibrated scores. Run before any change to `escalation-rubric.md`, `confidence-calibrator.md`, `hypothesis-card-template.md`, or `sc-troubleshoot-protocol/SKILL.md` ships. A regression on any fixture or property test blocks merge." — this is 3 sentences, role-stating, no decorative framing, and matches the convention.

---

## Section 4: Section-heading conventions

Every refs/ file uses `## H2` for top-level sections (no document repeats the H1, none use H1 as a section divider). `### H3` is used for sub-sections within an H2, and `####` is rare/absent.

Evidence:

- `escalation-rubric.md` uses 4 H2s: `## Confidence calibration (Wave 1.7)` (L5), `## Escalation decision (Wave 2)` (L23), `## Why 0.85?` (L44), `## What escalation does NOT mean` (L50).
- `hypothesis-card-template.md` uses 4 H2s: `## Template` (L7), `## Filling the card` (L116), `## Worked example (illustrative — not a real card)` (L123); H3s appear inside the embedded markdown code-fence template (L34, L38, L46, etc., they are content inside a fence — `### Sub-headings`).
- `triage-checklist.md` uses 5 H2s: `## Pre-investigation grounding` (L5), `## Cause-class scan` (L17), `## Evidence-or-drop check` (L37), `## Fix sketch` (L46), `## When to refuse Tier 1` (L56).
- `doc-discovery.md` uses 4 H2s (`## Section 1: ...`, `## Section 2: ...`, `## Section 3: ...`, `## Section 4: ...`, `## Loading discipline`) plus H3s for branch sub-sections (e.g. `### Branch A — Release-doc lookup`, `### Branch B — ...`).
- `remediation-handoff.md` uses 8 H2s — `## The user offer`, `## Decision matrix`, `## Phase A — Build the task file`, `## Phase B — Pre-execution review`, etc.
- `report-template.md` uses H2s for the major template + rule sections — `## Template` (L5), `## Rendering rules` (L143), `## Test-is-wrong rule` (L150), `## Behavior-is-documented rule` (L171), with H3s for sub-rules (`### Rendering rules when ...`).

Observations:
- Sentence-case or Title Case both appear; the dominant style is sentence-case with the first letter capitalised (e.g., `## Confidence calibration`, `## Cause-class scan`). H2 sections that name a structural artifact may be Title Case (`## Template`, `## Decision matrix`).
- Em-dashes are common in H3 sub-section names (e.g., `### Branch A — Release-doc lookup`, `### Phase A — Build the task file`).
- Horizontal rules (`---`) appear between major sections in some longer files (`doc-discovery.md` uses `---` at L8, L37, L70, L129, L177; `report-template.md` uses one `---` separating header metadata from body at L23).

**Confirmation for new file:** The proposal-specified H2 sections (`## Synthetic fixtures`, `## Real-card replay fixtures`, `## Property tests`, `## Suite integrity`, `## Implementation hook`) fit the H2-top-level convention. Sentence-case is consistent (`Synthetic fixtures`, `Real-card replay fixtures`, etc.). Use `### Fixture N — <name>` for individual fixtures, which mirrors the `### Branch A — ...` / `### Phase A — ...` em-dash pattern.

---

## Section 5: Table conventions

Markdown pipe tables are the standard tabular form across refs/. Headers use `**Bold**` only when emphasising a column name as a defined term; otherwise plain text.

Concrete examples:

- `escalation-rubric.md:11-17` — 4-column rubric table; column 1 cells are `**Bold**` term names (`**Evidence grounding**`, `**Symptom coverage**`, etc.); columns 2–4 are plain.
- `triage-checklist.md:20-34` — 2-column `| Class | Typical signals |` table; column 1 cells are `**Bold**` class names.
- `doc-discovery.md:61-66` — 3-column `| Step 1 mtime | Step 2 marker | Verdict |` cross-tab; cells use inline backticks for verdict literals (e.g. `` `current` ``, `` `stale` ``).
- `remediation-handoff.md:33-37` — 2-column `| User response | Action |` decision matrix.
- `hypothesis-card-template.md:97-101` — 4-column `| # | Kind | Source | Content |` evidence-shape table (inside an embedded markdown code-fence).

Observations:
- All tables are pipe-style (`| col1 | col2 |`) with a `|---|---|` separator row.
- No explicit alignment markers (`:---:`, `---:`) are used — all columns left-align by default.
- Header rows are sentence-case noun phrases; no trailing punctuation.
- Cells are often short — most refs/ tables fit a single line per row.

**Confirmation for new file:** The Property tests 3-column table (`| ID | Property | Assertion |`) per proposal L353-360 is consistent (3 columns, sentence-case headers, no alignment markers, short cells). The Synthetic fixtures section is paragraph-based (bullet/prose), not tabular — also consistent (e.g., `escalation-rubric.md` mixes prose + one table).

---

## Section 6: Code-fence usage

Refs/ files use fenced code blocks for THREE purposes:

1. **Embedded markdown templates** (` ```markdown `): the largest use — show a template the agent must follow when emitting a new artifact. Examples:
   - `hypothesis-card-template.md:9-114` (the template body itself)
   - `hypothesis-card-template.md:125-152` (worked example)
   - `report-template.md:7-141` (the REPORT.md template body)
   - `doc-discovery.md:135-176` (Doc Context Card template)
   - `remediation-handoff.md:9-28` (user-offer prompt verbatim)

2. **Shell snippets** (` ```bash ` or unlabeled ` ``` `): rare; appear only in `doc-discovery.md`:
   - L45-47 (`stat -c '%Y' <doc_path>`)
   - L53-55 (`grep -E '^(Last reviewed|Status...'`)
   - L17-19 / L25-27 / L33-35 (auggie query templates — unlabeled fences treated as prose-prompt blocks)

3. **JSON schemas** (` ```json `): only in `doc-discovery.md` (L80-87, L91-93, L99-108, L116-124) — the per-branch structured-output schemas.

Observations:
- `triage-checklist.md` and `escalation-rubric.md` contain NO code fences — they are pure prose + tables + checklists.
- Refs/ files DO NOT typically embed Python, Bash, or other implementation-language code (the protocol is markdown-only; executable logic lives in agents/skills, not refs).

**Confirmation for new file:** The proposal-specified content for `calibrator-eval-cases.md` is bullet lists + one table + paragraph prose — NO code fences are needed. This matches the `escalation-rubric.md` / `triage-checklist.md` shape (rubric/checklist files with zero fences) rather than the `hypothesis-card-template.md` shape (which embeds a long markdown template).

---

## Section 7: Em-dash / Unicode conventions

Refs/ uses these Unicode characters (verified via grep):

| Char | U+ | Where it appears | Count across refs/ |
|------|-----|------------------|---|
| `—` (em-dash) | U+2014 | Heavily — separators in H3 headings, parenthetical-like asides in prose, table-cell separators | Dominant; e.g. 3 in `escalation-rubric.md` L7/L46/L48; many more across the directory |
| `≤` (less-equal) | U+2264 | `hypothesis-card-template.md:36`, `:82`, `:118`; `report-template.md:33` | 4 |
| `≥` (greater-equal) | U+2265 | `escalation-rubric.md:42`; `doc-discovery.md:65` | 2 |
| `∈` (set membership) | U+2208 | `doc-discovery.md:110` (`currency_verdict ∈ {current, stale, unknown}`); `hypothesis-card-template.md:91` (`evidence_class ∈ {source_static, doc_static, none}`) | 2 |

**Not currently used anywhere in refs/:**

- `⟹` (U+27F9 long-rightwards-double-arrow / "implies")
- `⇒` (U+21D2 rightwards-double-arrow)
- `→` (U+2192 right-arrow, used as bullet/flow elsewhere in some skills but not in these refs)

Evidence — `grep -n '⟹' refs/*.md` returns NO matches; `grep -n '→' refs/*.md` matched only in `escalation-rubric.md` (L37 `→ STOP at Tier 1`, L38 `→ ESCALATE`, etc., which is `→` U+2192) — but the proposal's Property tests use `⟹` (U+27F9 "implies"), which would be a NEW Unicode character introduced by `calibrator-eval-cases.md`.

**Recommendation for new file:**

- Introducing `⟹` (U+27F9) is acceptable but represents a new Unicode character not used elsewhere in refs/. Two alternatives are equally consistent and arguably safer for markdownlint / portability:
  - Use `⇒` (U+21D2) — same logical meaning, more common in math markdown.
  - Spell it: `implies`.
- If the proposal's literal text (with `⟹`) is preserved verbatim, no other refs/ file needs to change — the character is well-formed UTF-8 and renders in all standard environments.

Em-dash (U+2014) usage in the new file's `### Fixture N — <name>` headings, **bold-emphasis — explanation** patterns, and inline parentheticals is consistent with all six existing refs/ files.

---

## Section 8: Inline-backtick conventions

Backticks wrap THREE classes of content across refs/:

1. **File names / paths** — e.g. `` `escalation-rubric.md` ``, `` `path/to/file.py:142` ``, `` `tests/path/to/test_file.py::test_eval_run` ``. Evidence:
   - `hypothesis-card-template.md:42` — `` `path/to/file.py:142` — `result = Path(scratch_root) / "foo"` ``
   - `escalation-rubric.md:35` — `` `confidence < 0.85` ``
2. **Identifier / value literals** — variable names, enum values, command flags, schema keys. Evidence:
   - `hypothesis-card-template.md:16` — `` `static_defect` | `runtime_behavior` | `environment_dependent` | `config_value` | `doc_contract` | `mixed` ``
   - `hypothesis-card-template.md:23` — `` `runtime_repro` | `runtime_trace` | `log_evidence` | `source_static` | `doc_static` | `none` ``
   - `remediation-handoff.md:34` — `` `yes` (or affirmative variant: "y", "go", "proceed") ``
3. **Command snippets in prose** — short shell/Python invocations. Evidence:
   - `hypothesis-card-template.md:43` — `` Command: `uv run python -c "from src.module import target"` → `NameError: name 'Path' is not defined` ``
   - `report-template.md:58` — `` `uv run pytest tests/path/to/test_eval_run.py::test_basic -x` ``

Observations:
- Schema enum tokens like `runtime_behavior`, `source_static`, `doc_static` are ALWAYS backticked when referenced in prose — never bolded, never plain.
- File names in same-directory references are backticked even when the surrounding text is bold-emphasised. (Example: `hypothesis-card-template.md:105` — "MANDATORY in v2.0 (target: follow-up commit after pin-test corpus in `calibrator-eval-cases.md` confirms v1.5 stability)." — note: the new file is ALREADY pre-referenced from this existing file.)

**Confirmation for new file:** Proposal L298-370 backticks:
- Fixture filenames (`` `fixture-h3-style.md` ``) — consistent with file-name class.
- Schema values (`` `runtime_behavior` ``, `` `source_static` ``) — consistent with identifier class.
- Cross-references to other refs/ files (`` `escalation-rubric.md` ``, `` `confidence-calibrator.md` ``, `` `hypothesis-card-template.md` ``) — consistent with file-name class.

All backtick usage in the new file matches existing refs/ conventions.

---

## Section 9: Bold marker conventions

`**Bold**` is used for:

1. **Emphasised labels at line-start** — defined-term highlights inside bullets / before colon-introduced explanation. Evidence:
   - `escalation-rubric.md:13` (table cell) — `**Evidence grounding**`
   - `escalation-rubric.md:27` — `1. **Hard stops**`
   - `escalation-rubric.md:31` — `2. **Forced escalation**`
   - `hypothesis-card-template.md:118` — `- **Length cap**: ≤ 1 page in plain rendering`
   - `triage-checklist.md:22` — table cell `**Missing/wrong import**`
   - `report-template.md:67-77` — `**Files to change**:`, `**Files that MUST NOT change**`, `**Test to verify**:`, `**Apply with**:`
2. **Inline strong-emphasis within prose** — used sparingly for safety-critical wording. Evidence:
   - `hypothesis-card-template.md:40` — "Each item must be either a `file:line` citation with a quoted snippet, or a command + actual output." (Note: appears as `**Each item must be either ...**` for the load-bearing phrase.)
   - `escalation-rubric.md:7` — "The `root-cause-analyst` returns a self-reported confidence. The skill **re-grades** it against this rubric"
3. **Header metadata fields** — `**Field**:` pattern in templates. Evidence:
   - `hypothesis-card-template.md:11-13` — `**Agent**:`, `**Tier**:`, `**Timestamp**:` (inside the embedded template)
   - `report-template.md:10-22` — `**Target**:`, `**Type**:`, `**Tier reached**:`, etc.

Observations:
- Bold is NOT used for general emphasis throughout running prose — its scarcity is what makes the `**re-grades**` style work.
- In tables, bold is reserved for one column (typically column 1, the term being defined).

**Confirmation for new file:** Proposal L301-365 uses `**Asserts**`, `**Expected calibrated**`, `**Mechanism**`, `**Result**` as label markers — consistent with the "emphasised labels at line-start" convention from `escalation-rubric.md` (`**Hard stops**`, `**Forced escalation**`) and `report-template.md` (`**Files to change**:`). The new file's bold usage matches the dominant pattern.

---

## Section 10: Length expectations

Existing refs/ file lengths (lines):

| File | Lines |
|------|-------|
| `escalation-rubric.md` | 52 |
| `triage-checklist.md` | 65 |
| `remediation-handoff.md` | 122 |
| `hypothesis-card-template.md` | 152 |
| `doc-discovery.md` | 182 |
| `report-template.md` | 196 |

Mean ≈ 128 lines; median ≈ 137 lines; min 52, max 196.

The proposal's `calibrator-eval-cases.md` content runs from spec L298-370 (≈72 lines of literal content) — this sits at the SHORT end of the distribution, comparable to `escalation-rubric.md` (52) and `triage-checklist.md` (65). It is well within the established range; no file in refs/ is shorter than 52 lines or longer than 196.

---

## Section 11: Recommended file size after creation

Per the proposal content (research-notes.md L17 references `CROSS-ENV-PROPOSAL-MERGED.md` L290-372):

- H1 title (1 line)
- Blank (1)
- Intro paragraph (1-3 lines)
- Blank (1)
- `## Synthetic fixtures` + ≈6 fixtures × ~5 lines each (~35 lines including blank separators)
- `## Real-card replay fixtures` + 3 fixtures (~18 lines)
- `## Property tests` + intro + 3-column 5-row table (~10 lines)
- `## Suite integrity` + 3-bullet rule list (~5 lines)
- `## Implementation hook` + deferred-pytest note (~3 lines)
- Trailing newline (1)

**Recommended total: ~75-90 lines** (within the 52-196 range; consistent with the shorter rubric-style refs files).

**No frontmatter expected** — refs/ files are plain markdown (no YAML frontmatter on any of the 6 existing files; confirmed via `head -1` returning the H1 in every case).

---

## Summary

The new file `calibrator-eval-cases.md` will fit the directory's conventions cleanly:

- H1 = `# Calibrator Eval Cases` (Title Case, single, line 1) — matches all 6 existing files.
- Intro paragraph (3 sentences, role-stating) immediately after H1 — matches the universal opening pattern.
- H2 sections (`## Synthetic fixtures`, `## Real-card replay fixtures`, `## Property tests`, `## Suite integrity`, `## Implementation hook`) — sentence-case, no decoration; consistent with `escalation-rubric.md` and `triage-checklist.md`.
- H3 sub-sections (`### Fixture N — <name>`) using em-dash separators — mirrors `doc-discovery.md`'s `### Branch A — Release-doc lookup`.
- One pipe-table for Property tests (3 cols, plain headers, no alignment markers) — consistent with all refs/ tables.
- NO code fences needed — the file is bullet-list + table + prose; matches `escalation-rubric.md` / `triage-checklist.md`.
- Inline backticks for fixture filenames, schema values, and cross-file references — universal convention.
- `**Bold**` line-start labels (`**Asserts**`, `**Expected calibrated**`) — consistent with `escalation-rubric.md`'s `**Hard stops**` / `**Forced escalation**` and `report-template.md`'s `**Files to change**:`.
- Em-dash (U+2014), `≤` (U+2264), `≥` (U+2265), `∈` (U+2208) — all already in use; safe to use.
- `⟹` (U+27F9) per proposal Property tests — **NOT currently used elsewhere in refs/**. Acceptable but new. Recommend either preserving as-is (UTF-8 safe, renders correctly) OR substituting `⇒` (U+21D2) or the word `implies` if maximum portability is desired. This is the only Unicode delta the new file introduces.
- Recommended length: ~75-90 lines — comfortably within the 52-196 line range of existing refs.
- No YAML frontmatter — plain markdown only, matching all 6 existing files.

The new file is structurally indistinguishable from a hybrid of `escalation-rubric.md` (compact, rubric-flavored) and `hypothesis-card-template.md` (cross-references other refs files; has worked examples). It will land cleanly in the directory with no consistency violations beyond the single new Unicode character flagged above.
