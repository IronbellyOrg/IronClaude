# Research Notes: Change E — Calibrator Eval Cases Pin-Test Corpus (NEW FILE)

**Date:** 2026-05-27
**Scenario:** A (Explicit — target file path known, spec content fully captured in proposal)
**Depth Tier:** Standard
**Template selection:** Template 01 (Generic) — single new file creation with content fully specified in the proposal

---

## EXISTING_FILES

- (TARGET — new) `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` — does NOT currently exist; verified via `find src .claude -iname "*calibrator-eval-cases*"` (empty output). This task creates it.
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/` — existing refs directory; current contents include `escalation-rubric.md`, `hypothesis-card-template.md`, `triage-checklist.md`, etc. The new file lives here alongside them.
- `src/superclaude/agents/confidence-calibrator.md` — 118 lines — the agent under test by the corpus. Read-only for this task.
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` — 52 lines BEFORE Change A — the rubric the corpus's expected scores are computed against. Read-only for this task; the corpus's expected scores ASSUME Change A's formula is in place.
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` — 152 lines (post PR #89) — the card schema the corpus fixtures conform to. Read-only for this task.
- `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md` (in MAIN checkout) — Change E spec at L290-372 with FULL content inline.
- (For replay fixtures 7-9) `t4-pane-title-20260526-101500` directory — referenced by Fixture 7 spec line as the source of the real H3 card. Researcher must locate this directory in the main checkout to extract the real-card content for fixtures 7-9.

## PATTERNS_AND_CONVENTIONS

- The `refs/` subdirectory contains reference markdown that the skill body and agents read at runtime. Conventions: H1 title, brief intro, structured sections with H2/H3 headings.
- Source-of-truth rule + make sync-dev / verify-sync workflow (same as all other tracks).
- Markdownlint applies to the new file (it lives under `src/superclaude/skills/...`).
- Pre-commit `block-claude-generated-mirrors` hook excludes `.claude/` paths from being staged; new file must be added in `src/` only, then synced.

## GAPS_AND_QUESTIONS

- **Real-card replay sources (Fixtures 7-9):** the proposal references `t4-pane-title-20260526-101500` as the source of the real H1/H2/H3 cards. The researcher must locate this directory in the main checkout (`/config/workspace/IronClaude/...`), extract the actual card content for each of the three fixtures, and either (a) embed the full card text inline in the corpus, or (b) cross-reference the original card path. The proposal's content provides the EXPECTED behavior (calibrated scores, M3a cap activations) but not the literal card content for the replays. Researcher must decide the appropriate level of inline-vs-reference.
- **Fixture file extension and storage layout:** the proposal references fixtures as `fixture-h3-style.md`, etc. — are these standalone files (each in a `fixtures/` subdirectory), or are they sections WITHIN `calibrator-eval-cases.md`? The proposal's L298-370 content suggests they are sections within the single file (each fixture is a `### Fixture N — <name>` heading with a paragraph describing the card properties and expected calibrated score). Decision: treat them as sections within the single file unless researcher uncovers a competing convention.
- **Property test ID alignment with Change A/C formulas:** P1 says `evidence_grounding ≤ 0.5` ⟹ `calibrated ≤ 0.80` — this corresponds to Change A's `evidence_grounding + 0.30` gate. P2/P3 similarly tie to M2/M3a. Researcher must confirm the property assertions match the formula values in Change A's spec (0.30 buffer, 0.85 STOP gate, 0.70/0.84 M3a caps).
- **Dependency ordering:** Change E is LAST in the A→B→C→F→E sequence per the proposal's Implementation order (L488-495). The corpus's expected behavior REQUIRES A, B(done), and C to all have shipped before the corpus's expected scores are produceable. Document this prerequisite in the task file; the corpus task can be BUILT in parallel with A/C/F, but its execution (running the calibrator against the fixtures and confirming the expected scores match) only makes sense after A, C, F land.
- **Implementation hook (deferred):** the proposal L367-370 explicitly defers the pytest harness (`tests/troubleshoot/test_calibrator_eval_cases.py`) to a follow-up commit. This task ONLY creates the corpus markdown file; the pytest harness is a separate future task and SHOULD NOT be in scope.

## RECOMMENDED_OUTPUTS

| # | Researcher | Topic Type | Output File |
|---|------------|-----------|-------------|
| 1 | spec-extraction | Source Spec Extraction | research/01-change-e-spec-extraction.md |
| 2 | refs-conventions | Patterns & Conventions | research/02-refs-conventions.md |
| 3 | t4-real-cards | Data Flow Tracer | research/03-t4-real-cards-extraction.md |
| 4 | template-conventions | Template & Examples | research/04-template-and-conventions.md |

## SUGGESTED_PHASES

- **Researcher 1 — Source Spec Extraction:**
  - Scope: Read proposal L290-372 (Change E spec block — includes the full file content L298-370).
  - Focus: Extract the full file content verbatim (it's a complete markdown document already); separate Synthetic Fixtures 1-6 from Real-card Replay Fixtures 7-9; capture all 5 Property tests (P1-P5) with assertion text; capture Suite integrity rules (which file changes trigger the suite); capture the deferred Implementation hook note; capture the [V2 merged] provenance markers per fixture.
  - Output: research/01-change-e-spec-extraction.md
  - Other researchers covering: refs-conventions covers existing refs/ patterns; t4-real-cards covers replay-fixture source extraction; template-conventions covers Template 01 + Makefile.

- **Researcher 2 — Refs Directory Conventions:**
  - Scope: Read existing files in `src/superclaude/skills/sc-troubleshoot-protocol/refs/` — escalation-rubric.md, hypothesis-card-template.md, triage-checklist.md, and any other refs files present.
  - Focus: document the header conventions (H1 title, intro paragraph, section structure); note characteristic formatting (em-dashes, table styles, code-fence usage); confirm the new corpus file will fit the existing pattern with H1 "Calibrator Eval Cases", intro paragraph, H2 sections for Synthetic/Real-card/Property/Suite-integrity/Implementation-hook.
  - Output: research/02-refs-conventions.md
  - Other researchers covering: spec-extraction; t4-real-cards; template-conventions.

- **Researcher 3 — T4 Real Card Extraction (Data Flow Tracer):**
  - Scope: Locate `t4-pane-title-20260526-101500` directory in `/config/workspace/IronClaude/` (main checkout). If found, identify `tier2-h1-*.md`, `tier2-h2-*.md`, `tier2-h3-*.md` and any sibling `*-calibration.md` artifacts.
  - Focus: Extract the actual card content (or summarize fields) needed to make Fixtures 7-9 self-contained. Specifically: confirm Fixture 7 maps to `tier2-h3-options-subcommand.md` and capture its claim/evidence/Verdict pattern; confirm Fixture 8 maps to the H2 card with WebFetch GitHub URLs as evidence; confirm Fixture 9 maps to H1 with 0.82 self-reported CONFIRM and mixed source + log evidence. Recommend whether each fixture should embed the full card text inline or cross-reference the original card path (with reproducibility caveat). If the directory cannot be found, document the gap and recommend that Fixtures 7-9 ship with placeholder content + a TODO to backfill the real-card details in a follow-up commit.
  - Output: research/03-t4-real-cards-extraction.md
  - Other researchers covering: spec-extraction; refs-conventions.

- **Researcher 4 — Template & Conventions:**
  - Scope: Read MDTM Template 01; read Makefile sync targets; read .pre-commit-config.yaml markdownlint and block-claude-generated-mirrors hooks.
  - Focus: confirm Template 01 fits a new-file-creation + sync + lint flow; document Makefile sync-dev / verify-sync behavior; note the markdownlint gotcha (--fix may modify file → re-sync).
  - Output: research/04-template-and-conventions.md
  - Other researchers covering: spec-extraction; refs-conventions; t4-real-cards.

## TEMPLATE_NOTES

- Template 01 (Generic) — single-file creation with content fully specified in proposal. Same template as Change B / PR #89 (which was also additive markdown with deterministic content).
- Tier Standard (4 researchers).
- QA_GATE_REQUIREMENTS: FINAL_ONLY (executor-performed structural check at end).
- VALIDATION_REQUIREMENTS: "make sync-dev pass + make verify-sync exit 0 + markdownlint hook PASS on new file + all 9 fixtures present + all 5 property tests present + Suite integrity section present + Implementation hook note present"
- TESTING_REQUIREMENTS: NONE — this task creates the test corpus; it doesn't execute it. The pytest harness is deferred per the proposal.

## AMBIGUITIES_FOR_USER

- **Open Question (operational):** if researcher 3 cannot locate the `t4-pane-title-20260526-101500` directory in the main checkout, should Fixtures 7-9 ship with (a) placeholder content + TODO follow-up to backfill, or (b) be deferred entirely from this task and built as a follow-up after the real cards are located? Recommend option (a) — ship the corpus structure complete so Tracks A/C/F's CI gate (the corpus is referenced by their downstream consumers) has the section headers, and backfill the inline card content as a follow-up. The task file should encode this branch in a conditional phase.
