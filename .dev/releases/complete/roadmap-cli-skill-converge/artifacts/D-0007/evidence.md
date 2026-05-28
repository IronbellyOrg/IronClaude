# D-0007 — Evidence: `sc-roadmap-protocol/refs/extraction-pipeline.md` Collapse to Single-Pass

| Field | Value |
|---|---|
| Task | T02.05 |
| Roadmap Item | R-007 |
| Drift Item | B-7 |
| Deliverable | D-0007 |
| Date | 2026-05-26 |
| Source File Edited | `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` |
| CLI Reference | `build_extract_prompt` (`src/superclaude/cli/roadmap/prompts.py:180`); `build_extract_prompt_tdd` (`src/superclaude/cli/roadmap/prompts.py:328`); single-step wiring (`src/superclaude/cli/roadmap/executor.py:2001-2025`); gate (`EXTRACT_GATE` / `EXTRACT_TDD_GATE` at `executor.py:2019`). |
| Decision Posture | Option 1 (collapse to single-pass reference mirroring `build_extract_prompt`) — see `design-decision.md` row B-7 |
| Source Claim Status | VERIFIED (`verification.md:138-147`) — skill ref described 8 sequential steps (`refs/extraction-pipeline.md:7-9` pre-edit); CLI executes a single `Step(id="extract", ...)` built by `build_extract_prompt` or `build_extract_prompt_tdd` with no per-aspect retry, no chained intermediate outputs, and no inter-aspect gates. |

## Linkage

- **B-7 → D-0007.** `release-scope.md:126-130` and `verification.md:138-147` capture the claim: pre-edit, `refs/extraction-pipeline.md:7-9` opened with `"## 8-Step Extraction Pipeline"` followed by `"Process the specification file in 8 sequential steps. Each step produces structured output that feeds into subsequent steps."`. CLI evidence: `cli/roadmap/prompts.py:180` defines `def build_extract_prompt(...)` and `:328` defines `def build_extract_prompt_tdd(...)`; both are single-prompt builders that return one prompt string. `cli/roadmap/executor.py:2001-2025` constructs **one** `Step(id="extract", ...)` whose `prompt=` argument selects between the two builders by `config.input_type == "tdd"`. There is no `extract-1` ... `extract-8` step sequence, no per-aspect `Step(...)`, no aspect-level retry, and no chained intermediate output paths between aspects.
- `design-decision.md:37` row B-7 selected **Option 1**: "Convert the 8 steps into checklist/rationale inside a single-pass extraction description." `solutions.md:227-258` recommends Solution 1 — "the 8-step framing is more pedagogy than process."
- **D-0007** is the resulting source-file edit at `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` plus this evidence record.

## Source-file parity check

### CLI canonical builders cited in the edit

`src/superclaude/cli/roadmap/prompts.py:180`:

```
def build_extract_prompt(
    spec_file: Path,
    retrospective_content: str | None = None,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
    """Prompt for step 'extract'. ..."""
```

`src/superclaude/cli/roadmap/prompts.py:328`:

```
def build_extract_prompt_tdd(
    spec_file: Path,
    retrospective_content: str | None = None,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
    """Prompt for step 'extract' when input is a TDD ...
    Extends the standard extract prompt with 6 additional body sections ...
    All 8 standard sections are retained for backward compatibility ..."""
```

### CLI single-step wiring cited in the edit

`cli/roadmap/executor.py:2001-2025` builds the single `Step(id="extract", ...)`:

```
Step(
    id="extract",
    prompt=(
        build_extract_prompt_tdd(...) if config.input_type == "tdd"
        else build_extract_prompt(...)
    ),
    output_file=extraction,
    gate=EXTRACT_TDD_GATE if config.input_type == "tdd" else EXTRACT_GATE,
    timeout_seconds=1800 if config.input_type == "tdd" else 300,
    inputs=...,
    retry_limit=1,
)
```

The `retry_limit=1` knob is a single transport-level retry on the one step; it is **not** a per-aspect regenerate loop.

### CLI canonical TDD body sections cited in the edit

`cli/roadmap/prompts.py:383-465` instructs the LLM to produce **14 structured sections** when `--input-type tdd` is selected: the 8 standard sections (Functional Requirements, Non-Functional Requirements, Complexity Assessment, Architectural Constraints, Risk Inventory, Dependency Inventory, Success Criteria, Open Questions) plus 6 TDD-specific sections (Data Models and Interfaces `:411`, API Specifications `:420`, Component Inventory `:429`, Testing Strategy `:437`, Migration and Rollout Plan `:445`, Operational Readiness `:454`). The frontmatter additionally declares six new TDD counters (`data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified` at `:367-372`).

### CLI verbatim-ID preservation cited in the edit

`cli/roadmap/prompts.py:219-227` (and `:386-393` for the TDD path) instructs the LLM:

> "Use the spec's exact requirement identifiers verbatim as primary IDs. Do NOT create a new numbering scheme (e.g., do NOT renumber as FR-001, FR-002). If a spec uses FR-EVAL-001.1, use FR-EVAL-001.1. ... If the spec has no requirement IDs, then use FR-NNN as a fallback."

The post-edit Aspect 8 records this CLI parity reality — synthetic IDs are a fallback, not the default — replacing the pre-edit "Step 8: ID Assignment" framing that prescribed synthetic numbering as the only path.

### Chunked-extraction CLI parity cited in the edit

`cli/roadmap/prompts.py:217` and `:366` show the CLI's only chunking signal: the LLM populates `extraction_mode: (string) one of: standard, chunked` in the frontmatter. There is no CLI code path that builds a section index, assembles chunks, performs per-chunk extraction, deduplicates merge results, or runs the 4-pass completeness verification — grep on `cli/roadmap/executor.py` and `cli/roadmap/prompts.py` for `chunk` returns only the two `extraction_mode` mentions. The full chunked algorithm in `refs/extraction-pipeline.md` is therefore inference-only.

### Post-edit `refs/extraction-pipeline.md` structure (in file order)

| Section | Anchor | Status |
|---|---|---|
| Header lead paragraph | `extraction-pipeline.md:3` | ✅ Reframed from "8-step extraction pipeline + chunked + 4-pass verification" to "single-pass extraction step + eight-aspect coverage + TDD-extended aspects + advisory dictionaries + inference-only chunked/verification" |
| Single-Pass Extraction (CLI Canonical Behavior) | `extraction-pipeline.md:7-39` | ✅ New canonical section — names `build_extract_prompt` (`prompts.py:180`) and `build_extract_prompt_tdd` (`prompts.py:328`); shows the actual `Step(id="extract", ...)` wiring from `executor.py:2001-2025`; states there is no per-aspect retry, no chained intermediate outputs, no inter-aspect gates; cites `EXTRACT_GATE` / `EXTRACT_TDD_GATE` as the only mechanical gate |
| Eight-aspect coverage inside the single prompt | `extraction-pipeline.md:37-39` | ✅ New framing paragraph — preserves the eight original step descriptions as **aspects** of one prompt rather than chained phases; explicit "coverage rationale, not a required execution sequence"; cites verbatim-ID CLI preference |
| Aspects 1-8 (preserved bodies) | `extraction-pipeline.md:41-180` | ✅ Step heading renamed to Aspect heading (8 occurrences); all field tables, priority heuristics, classification algorithm, dependency table, success criteria table, risk table, and ID format table preserved verbatim. Aspect 8 gains a "CLI parity note" prepended to its body recording that the CLI prefers verbatim source-document IDs and that synthetic numbering is the fallback only. Four "Assigned in Step 8" field rows rewritten to point at "Aspect 8" and indicate verbatim-first / synthetic-fallback semantics |
| TDD-Extended Aspects (covered by `build_extract_prompt_tdd`) | `extraction-pipeline.md:182-199` | ✅ Reframed — replaces "TDD-Specific Extraction Steps (Steps 9-15)" header with "TDD-Extended Aspects (covered by `build_extract_prompt_tdd`)"; clarifies CLI uses `--input-type tdd` flag (not 4-signal inference scoring); adds a six-row mapping table from CLI body section → `prompts.py` line → frontmatter counter; adds a "CLI parity (B-7, partial)" note marking the 7 sub-aspects (originally Steps 9-15) as an inference-only finer-grained taxonomy that overlaps the 6 CLI body sections |
| Aspects 9-15 (preserved bodies) | `extraction-pipeline.md:201-258` | ✅ Step heading renamed to Aspect heading (7 occurrences); all storage-key tables and structures preserved verbatim. Aspect 11's cross-reference to Step 6 rewritten as cross-reference to Aspect 6 |
| PRD-Supplementary Extraction Context | `extraction-pipeline.md:261-281` | ✅ Preserved verbatim — the existing section already documents PRD context as conditional prompt enrichment blocks; this matches CLI behaviour (`prompts.py:302-323` for `build_extract_prompt`, equivalent block for `build_extract_prompt_tdd`) |
| Domain Keyword Dictionaries (LLM-advisory) | `extraction-pipeline.md:283-330` | ✅ Demoted — new "LLM-advisory" header with explicit scope note ("The CLI does not tokenise the spec, does not apply the weights, and does not enforce the classification algorithm"); seven dictionary bodies preserved verbatim |
| Chunked Extraction Protocol (Non-Canonical — Inference-Only) | `extraction-pipeline.md:333-450` | ✅ Demoted — new "Non-Canonical — Inference-Only" header with explicit scope note citing the `extraction_mode` frontmatter flag (`prompts.py:217`, `:366`) as the **only** CLI representation of chunking; section index, chunk assembly, per-chunk extraction, merge, deduplication, cross-reference resolution, and global ID assignment bodies preserved verbatim. Inline mentions of "8-step extraction pipeline (Steps 1-7 only; Step 8 deferred)" rewritten to "eight standard aspects (Aspects 1-7 only; Aspect 8 deferred)" |
| 4-Pass Completeness Verification (Inference-Only) | `extraction-pipeline.md:452-470` | ✅ Demoted — new "Inference-Only" header with CLI parity reminder citing `EXTRACT_GATE` / `EXTRACT_TDD_GATE` as the only mechanical extraction validation; 4-pass table and on-failure procedure preserved verbatim |
| Worked Example: 1500-Line Spec | `extraction-pipeline.md:472-526` | ✅ Preserved verbatim — sits inside the demoted Chunked-Extraction Protocol section, so the worked-example's "Step 1: Section Index", "Step 2: Chunk Assembly", "Step 7: Global ID Assignment" labels refer to the chunked-algorithm step list (which is itself inference-only), not to the canonical 8 aspects |
| Footer | `extraction-pipeline.md:529-531` | ✅ Updated to record the CLI parity baseline (B-7, VERIFIED) with source citations for `build_extract_prompt`, `build_extract_prompt_tdd`, the executor wiring, the eight-aspect taxonomy, the TDD-extended aspects, the advisory dictionaries, and the non-canonical chunked / 4-pass material |

## Acceptance criteria check (`phase-2-tasklist.md:261-266`)

- ✅ `refs/extraction-pipeline.md` describes one single-pass extraction step — see "Single-Pass Extraction (CLI Canonical Behavior)" (`extraction-pipeline.md:7-39`). The section quotes the `Step(id="extract", ...)` wiring directly and explicitly states "There is **no** sequential 8-step pipeline in the CLI today, no per-aspect retry, no chained intermediate outputs between aspects, and no inter-aspect ordering gate."
- ✅ `refs/extraction-pipeline.md` preserves the eight-aspect coverage as rationale rather than required sequence — see "Eight-aspect coverage inside the single prompt" (`extraction-pipeline.md:37-39`) plus the eight Aspect 1-8 sub-sections (`:41-180`). The framing paragraph reads "coverage rationale, not a required execution sequence — the LLM is free to address them in any order that produces the required body sections of `extraction.md`." Each Aspect heading uses the word "Aspect" rather than "Step". Aspect 8's body was additionally rewritten to fold the CLI's verbatim-ID preference into the ID-assignment guidance (synthetic numbering becomes the fallback path, not the default).
- ✅ `refs/extraction-pipeline.md` names `build_extract_prompt` and `build_extract_prompt_tdd` as the CLI extraction prompt-builder behavior described in the source documents — both function names appear in the new prompt-builder table (`extraction-pipeline.md:15-16`) with the exact line citations `prompts.py:180` and `:328` and the conditional `if config.input_type == "tdd"` selector quoted from the executor (`:23-29`). They also appear in the file's lead paragraph (`:3`), in the TDD-Extended Aspects header (`:182`), and in the footer CLI parity baseline (`:531`).
- ✅ Evidence at this path links B-7 → D-0007 and records the source's VERIFIED status — see the "Source Claim Status" row of the header table (records VERIFIED + `verification.md:138-147` anchor), the "Linkage" section above (B-7 to D-0007 chain with `release-scope.md:126-130` + `verification.md:138-147` + `design-decision.md:37` + `solutions.md:227-258` citations), and the footer CLI parity baseline that re-anchors B-7 in the file itself.

## Reframed vs. preserved skill content

- **Preserved verbatim** (text identical, semantics demoted to coverage-rationale / inference-only):
  - All eight standard aspect bodies (Aspects 1-8 in the post-edit file = pre-edit Steps 1-8): field tables, priority heuristics, classification algorithm, dependency taxonomy, success-criteria fields, risk fields, ID assignment formats. Only the section labels changed (Step → Aspect) and Aspect 8 gained the CLI parity note.
  - All seven TDD aspect bodies (Aspects 9-15 = pre-edit Steps 9-15): storage-key tables, structure dictionaries, scoping notes.
  - PRD-Supplementary Extraction Context — preserved verbatim because it already matches CLI behaviour.
  - Seven domain keyword dictionaries — preserved verbatim under the new "LLM-advisory" header.
  - Chunked Extraction Protocol algorithm — preserved verbatim (section index, chunk assembly, per-chunk extraction, merge rules, deduplication checks, cross-reference resolution, global ID assignment) under the new "Non-Canonical — Inference-Only" header.
  - 4-Pass Completeness Verification table and on-failure procedure — preserved verbatim under the new "Inference-Only" header.
  - 1500-line worked example — preserved verbatim inside the demoted chunked section.
- **Removed from canonical scope** (folded under inference-only headers):
  - "8-Step Extraction Pipeline" framing as a chained sequence is gone — the post-edit canonical section explicitly states there is no 8-step pipeline in the CLI.
  - "Each step produces structured output that feeds into subsequent steps" framing — replaced by "coverage rationale, not a required execution sequence" framing.
  - "Steps 9-15 execute ONLY when TDD-format input is detected" via 4-signal inference scoring — replaced by "Selected when `--input-type tdd` is passed; the CLI uses an **explicit flag**, not the 4-signal inference heuristic in `scoring.md`."
  - Chunked extraction as a canonical CLI mechanism — demoted to inference-only with the CLI parity note that the only CLI signal is the `extraction_mode` frontmatter flag.
  - 4-pass completeness verification as a canonical CLI mechanism — demoted to inference-only with the CLI parity note that `EXTRACT_GATE` / `EXTRACT_TDD_GATE` is the only mechanical CLI gate.
  - Synthetic FR-NNN / NFR-NNN numbering as the default ID scheme — relegated to fallback path; verbatim source-document IDs are the default per `prompts.py:219-227` / `:386-393`.
- **Added** (new canonical content for B-7):
  - "Single-Pass Extraction (CLI Canonical Behavior)" section with the prompt-builder table, the actual `Step(id="extract", ...)` wiring quote, the gate citation, and the explicit "no per-aspect retry / no chained outputs / no inter-aspect gates" statement.
  - "Eight-aspect coverage inside the single prompt" framing paragraph.
  - CLI parity note on Aspect 8 (verbatim-ID preference, synthetic-numbering fallback).
  - CLI canonical TDD body sections mapping table (CLI section → `prompts.py` line → frontmatter counter) in the TDD-Extended Aspects header.
  - "CLI parity (B-7, partial)" note in the TDD-Extended Aspects header explaining the 7-skill-aspect vs 6-CLI-body-section mismatch and instructing readers to use the mapping table for what the CLI actually instructs.
  - "LLM-advisory" header and scope note for Domain Keyword Dictionaries.
  - "Non-Canonical — Inference-Only" header and scope note for the Chunked Extraction Protocol.
  - "Inference-Only" header and CLI parity reminder for 4-Pass Completeness Verification.
  - Footer CLI parity baseline (B-7, VERIFIED) note with citations.

## Cross-edit linkage

- `SKILL.md:134` already flags the canonical CLI step as "CLI emits a single-pass `extract` step using `build_extract_prompt` / `build_extract_prompt_tdd` (see B-7)" in the Wave 1B crosswalk row. The B-7 cross-reference now resolves directly to the post-edit `refs/extraction-pipeline.md` canonical section.
- `SKILL.md:208,213,214,217` still references "the 8-step extraction pipeline" in Wave 1B behavioral instructions. That prose continues to point at `refs/extraction-pipeline.md` as the loaded reference; with this edit, the reference itself documents the eight aspects under the single-pass canonical framing, so the SKILL.md prose is satisfied by the new content. SKILL.md prose changes for B-7 are out of scope for T02.05 — the crosswalk row at `:134` already names the CLI builders. If a follow-up wants the Wave 1B prose itself reframed in single-pass language, that is a separate edit.
- `refs/scoring.md` TDD-Format Detection Rule (4-signal weighted scoring) is referenced by the post-edit TDD-Extended Aspects section as the inference-only counterpart to the CLI's `--input-type tdd` flag. The two references are consistent: scoring.md describes the inference heuristic; extraction-pipeline.md states that the CLI uses the explicit flag instead.

## Sync follow-up (B-12)

This edit lives only at `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`. A subsequent `make sync-dev` is required (tracked under B-12 / Phase 5) before `.claude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` and `/config/.claude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` reflect the change. Per repo rules, `.claude/` mirrors are not staged or committed.

## CLI behavior anchors cited in the edit

- `cli/roadmap/prompts.py:180` — `def build_extract_prompt(...)` definition.
- `cli/roadmap/prompts.py:213` — `domains_detected` frontmatter field (advisory domain-classification output).
- `cli/roadmap/prompts.py:217` — `extraction_mode: standard | chunked` frontmatter field (only CLI signal for chunking).
- `cli/roadmap/prompts.py:219-227` — verbatim-ID preservation instructions for the standard path.
- `cli/roadmap/prompts.py:302-323` — `--prd-file` supplementary context block for `build_extract_prompt`.
- `cli/roadmap/prompts.py:328` — `def build_extract_prompt_tdd(...)` definition.
- `cli/roadmap/prompts.py:362-372` — TDD frontmatter counters (six additional counters for TDD-extended sections).
- `cli/roadmap/prompts.py:366` — `extraction_mode: standard | chunked` frontmatter field for the TDD path.
- `cli/roadmap/prompts.py:383-465` — fourteen-section TDD body specification (8 standard + 6 TDD-specific).
- `cli/roadmap/prompts.py:386-393` — verbatim-ID preservation instructions for the TDD path.
- `cli/roadmap/prompts.py:411` — TDD body section "Data Models and Interfaces".
- `cli/roadmap/prompts.py:420` — TDD body section "API Specifications".
- `cli/roadmap/prompts.py:429` — TDD body section "Component Inventory".
- `cli/roadmap/prompts.py:437` — TDD body section "Testing Strategy".
- `cli/roadmap/prompts.py:445` — TDD body section "Migration and Rollout Plan".
- `cli/roadmap/prompts.py:454` — TDD body section "Operational Readiness".
- `cli/roadmap/executor.py:58-59` — imports for `build_extract_prompt` and `build_extract_prompt_tdd`.
- `cli/roadmap/executor.py:2001-2025` — single `Step(id="extract", ...)` wiring with conditional builder selection by `config.input_type`.

## 8-step → single-pass collapse record

Per `phase-2-tasklist.md:264` the evidence must record that the eight-aspect coverage is preserved as rationale rather than required sequence. Summary:

- **Behavior moved from "sequence" to "aspect taxonomy."** Pre-edit `refs/extraction-pipeline.md:7-9` instructed the operator/LLM to "Process the specification file in 8 sequential steps. Each step produces structured output that feeds into subsequent steps." Post-edit, those eight headings exist as **aspects of one prompt**, and the canonical section explicitly states the LLM is free to address them in any order that produces the required body sections of `extraction.md`.
- **Why moved.** CLI grep confirms one `def build_extract_prompt(...)` (`prompts.py:180`), one `def build_extract_prompt_tdd(...)` (`prompts.py:328`), and a single `Step(id="extract", ...)` in `executor.py:2001-2025`. There is no chained extract step list. The eight pre-edit headings map cleanly to the eight body-section headings the single CLI prompt instructs the LLM to write (`prompts.py:218-266` for the standard path), which is exactly what aspect-coverage framing captures.
- **What the CLI does instead.** Builds one prompt, runs one `ClaudeProcess` step, validates the single emitted `extraction.md` against one gate (`EXTRACT_GATE` or `EXTRACT_TDD_GATE`). Aspect ordering, intermediate validation between aspects, and per-aspect retry budgets do not exist; the single step has a `retry_limit=1` for transport-level retry only.
- **Reintroduction path.** If a future CLI release decomposes extraction into multiple `Step(id="extract-N", ...)` instances (with per-aspect prompts and gates), the eight Aspect headings can be promoted back to "Steps" and the canonical section updated to describe the chained sequence. The B-7 row in `release-scope.md` is the tracking point.
