# Research Notes: OQ3 Path C — rf-team-lead Tavily refactor + audit test pin remediation

**Date:** 2026-05-25
**Scenario:** A (Explicit — BUILD_REQUEST provided GOAL, WHY, source files, full phase plan, 7 acceptance criteria)
**Depth Tier:** Standard (single concern, 1 source file refactored, 1 test file refactored, ~5 cross-reference files updated)
**Track Count:** 1
**Template:** 02 (Complex — discovery + refactor + verify + per-phase QA gates)

---

## EXISTING_FILES

### Refactor target

- `src/superclaude/agents/rf-team-lead.md` (431 lines)
  - **Line 417 verified**: `- **Fix Cycles**: If a phase pipeline returns issues, invoke another pipeline with a FIX request (max 3 cycles per phase). If max cycles exhausted, HALT and ask user — do NOT proceed with unresolved findings.`
  - **SHA-256 of line 417** (sed -n '417p' | sha256sum): `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` (matches pinned value)
  - **Bounding section**: `### Project Mode Architecture` (line 412) → `## Cleanup` (line 422). Line 417 is the Fix Cycles bullet within Project Mode Architecture.
  - **Frontmatter tools list** (lines 6-29 per proposal): currently `Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, NotebookEdit, Task, ...` — needs Tavily-first reorder
  - **"WebSearch — Understanding Unfamiliar Technologies" subsection** (lines 292-297 per proposal): full text to be replaced with "Web Research — Tavily-first Protocol"
  - **`## Critical Rules` list** (lines 343-353 per proposal): currently 1-10; new rule 11 added

### Audit test target

- `tests/audit/test_dnsp_all_agents_fail_bypass.py` (645 lines)
  - **Line 70-72**: `RF_TEAM_LEAD_LINE_417_SHA256` constant — to be replaced by snapshot fixture mechanism
  - **Lines 65, 304**: `WRAPPER_SOURCES` tuple + `test_rf_team_lead_417_pointer_present_at_every_site` (cross-reference assertion)
  - **Lines 309-317**: `test_rf_team_lead_417_sha256_pin_present_at_every_site` — SHA propagation check (currently FAILING — wrapper sources don't actually contain the SHA)
  - **Lines 349-385**: `TestRfTeamLead417ByteStability` class with three tests pinning literal line 417
    - `test_line_417_sha256_matches_pinned_value` — uses `lines[416]` (CURRENTLY PASSING — protects line 417 byte-stability)
    - `test_line_417_names_max_3_cycles` — uses `lines[416]` (CURRENTLY PASSING)
    - `test_line_417_names_halt_and_ask_user` — uses `lines[416]` (CURRENTLY PASSING)
  - **Lines 618-630**: `test_rf_team_lead_417_contains_halt` — uses `lines[416]` (CURRENTLY PASSING)

### Cross-reference files (`rf-team-lead.md:417` string occurrences)

Verified via `grep -rn "rf-team-lead.md:417" src/superclaude/`:

| File | Line | Context |
|------|------|---------|
| `src/superclaude/agents/rf-qa.md` | 426 | "3-cycle hard cap at `rf-team-lead.md:417` remains as the fourth-precedence backstop" |
| `src/superclaude/skills/task-builder/SKILL.md` | 1018 | "the existing 3-cycle hard cap at `rf-team-lead.md:417` is preserved as the fourth-precedence backstop" |
| `src/superclaude/skills/task-builder/SKILL.md` | 1058 | "the global 3-cycle backstop at `rf-team-lead.md:417`" |
| `src/superclaude/skills/task-builder/SKILL.md` | 1074 | "the `rf-team-lead.md:417` 3-cycle backstop" |
| `src/superclaude/skills/task-builder/SKILL.md` | 1952 | "the global 3-cycle backstop at `rf-team-lead.md:417`" |
| `src/superclaude/agents/rf-task-builder.md` | 375 | "hard-cap fallback at `rf-team-lead.md:417`" |

**6 occurrences across 3 files.** Each needs replacement with a line-number-free reference (e.g., "rf-team-lead's Fix Cycles rule").

### SHA-256 string occurrences (`51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`)

Verified via `grep -rn` across src/ and tests/:

| File | Line | Context |
|------|------|---------|
| `tests/audit/test_dnsp_all_agents_fail_bypass.py` | 32 | docstring mention |
| `tests/audit/test_dnsp_all_agents_fail_bypass.py` | 71 | constant definition |

**Only in the test file itself.** No wrapper sources currently propagate the SHA (the failing `test_rf_team_lead_417_sha256_pin_present_at_every_site` test confirms this).

### Sibling-completed precedent

- `.dev/tasks/done/TASK-RF-20260522-203947-tavily-agents-refactor/` — parent task; rf-team-lead Phase 2 review PASSED (revert was a Phase 4 audit-pin issue, not content quality)
- The proposal `.dev/releases/current/TavilyAgents/rf-team-lead-tavily-refactor.md` is the exact spec applied to the other 9 agents in `feat/agents-tavily`

---

## PATTERNS_AND_CONVENTIONS

### Tavily-first frontmatter ordering (precedent from feat/agents-tavily commit 11795ec1)

The 9 successfully-refactored agents (rf-analyst, rf-qa, rf-qa-qualitative, etc.) all use this exact ordering:

```yaml
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - mcp__tavily__tavily-search    # PRIMARY web search (rare use; see body)
  - mcp__tavily__tavily-extract   # PRIMARY web content extraction (rare use)
  - WebSearch                      # FALLBACK only — Tavily unavailable
  - WebFetch                       # FALLBACK only — Tavily unavailable
  - NotebookEdit
  - Task
  ...
```

The Tavily-first protocol body section uses three Tavily-unavailable conditions (unknown tool, server error after retry, rate-limit) with the literal phrase "Do NOT use WebSearch or WebFetch as a first choice" and a `web_research_fallback: tavily=<reason>; used=<WebSearch|WebFetch>` observability line.

### Snapshot fixture pattern (proposed for Path C)

Convention: `tests/audit/fixtures/<file-slug>-<rule-slug>.txt` contains the exact bytes (no trailing newline trim) of the protected rule region. Test compares: (a) semantic substring presence + (b) SHA-256 of fixture bytes vs SHA-256 of extracted region from the live source.

Bounding rule: extract the natural section delimited by the nearest `### header` above and the next `##` or `###` header below. Line 417 lives inside `### Project Mode Architecture` (line 412) → bounded above by that header, below by `## Cleanup` (line 422). The fixture captures lines 412-421 (Project Mode Architecture section, which contains the Fix Cycles bullet plus context).

Alternative narrower fixture: just the Fix Cycles bullet (line 417) plus its surrounding context lines (415-418, which include the bullet's parent intro and the next sibling bullet). Decision: **use the narrower form** — fewer bytes to track, the protected content is exactly the Fix Cycles rule.

### Existing markdownlint policy (precedent from parent task's child)

`.markdownlint.json` is already configured with `MD029 { style: "one" }` (numbered lists use `1.` repeatedly). The Tavily refactor inserts a numbered list inside the "Web Research — Tavily-first Protocol" subsection — must use `1.` style.

### CLAUDE.md hard rules applied here

- **NEVER stage `.claude/` paths** — `src/superclaude/` is SoT; `make sync-dev` does the copy; `make verify-sync` enforces
- **UV only** for Python — no `python -m`, no bare `pip`
- **Pre-commit hooks must run cleanly** — no `--no-verify`

---

## GAPS_AND_QUESTIONS

### Resolved during scope discovery

1. ~~How many cross-reference occurrences of `rf-team-lead.md:417` exist?~~ → **Resolved: 6 occurrences across 3 files** (rf-qa.md, SKILL.md, rf-task-builder.md). NOT in rf-analyst.md or rf-qa-qualitative.md.
2. ~~Where does the SHA-256 string appear?~~ → **Resolved: only in the test file (2 occurrences — docstring + constant).** The `test_rf_team_lead_417_sha256_pin_present_at_every_site` test is currently FAILING because wrapper sources don't have it.
3. ~~What is the natural bounding region for the Fix Cycles rule fixture?~~ → **Resolved: `### Project Mode Architecture` (line 412) above, `## Cleanup` (line 422) below.** Narrower form: just the bullet line + 1-2 adjacent context lines.
4. ~~What's the current pytest status of this audit file?~~ → **Resolved: 10 failed / 40 passed.** The 10 failures are part of the project's 102-failed baseline. Tests currently passing (line-417 byte-stability suite) MUST continue passing post-refactor.

### Unresolved (assumptions documented)

1. **Should Path C ALSO fix the currently-failing wrapper-source tests?** The BUILD_REQUEST scope is limited to making the existing line-417 tests survive the rf-team-lead refactor. The wrapper-source tests (R-122 label, Path A/B/C labels, mutual-exclusivity phrasing, SHA pin propagation) are currently FAILING and out of Path C scope. **Decision: Path C does NOT touch those failing tests** — they're pre-existing baseline failures. Path C only converts the line-417 byte-stability mechanism from line-pinning to snapshot-pinning.

---

## RECOMMENDED_OUTPUTS

### Files to create

1. `tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt` — snapshot fixture (exact bytes of the Fix Cycles bullet region from rf-team-lead.md)
2. `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/TASK-RF-20260525-rf-team-lead-tavily-pathC.md` — the MDTM task file

### Files to modify

1. `src/superclaude/agents/rf-team-lead.md` — apply Tavily-first refactor per proposal (frontmatter tools reorder + WebSearch subsection replacement + Critical Rule 11 addition)
2. `tests/audit/test_dnsp_all_agents_fail_bypass.py` — replace line-index pinning with semantic + snapshot pinning
   - Replace `RF_TEAM_LEAD_LINE_417_SHA256` constant with a function that computes SHA-256 of the fixture file content
   - Rename `test_line_417_sha256_matches_pinned_value` → `test_fix_cycles_rule_present_and_byte_stable`
   - Replace `lines[416]` access in `test_line_417_names_max_3_cycles` and `test_line_417_names_halt_and_ask_user` and `test_rf_team_lead_417_contains_halt` with substring searches over the full file text (semantic checks, line-number-free)
   - Remove the currently-failing `test_rf_team_lead_417_sha256_pin_present_at_every_site` (since wrapper sources don't have it — out of Path C scope to add)
3. `src/superclaude/agents/rf-qa.md` — replace `rf-team-lead.md:417` (1 occurrence at L426) with `rf-team-lead's Fix Cycles rule`
4. `src/superclaude/skills/task-builder/SKILL.md` — replace `rf-team-lead.md:417` (4 occurrences at L1018, L1058, L1074, L1952) with `rf-team-lead's Fix Cycles rule`
5. `src/superclaude/agents/rf-task-builder.md` — replace `rf-team-lead.md:417` (1 occurrence at L375) with `rf-team-lead's Fix Cycles rule`

After src/ edits: `make sync-dev` propagates to .claude/.

---

## SUGGESTED_PHASES

Matches BUILD_REQUEST phase plan (7 phases). Per-phase QA gates required per `QA_GATE_REQUIREMENTS: PER_PHASE` (inferred from BUILD_REQUEST "Include phase-by-phase plans with per-phase QA gates").

- **Phase 1**: Setup + freshness re-Read (verify line 417 SHA still matches before any edits; capture baseline pytest count)
- **Phase 2**: Create snapshot fixture file by extracting Fix Cycles rule from current rf-team-lead.md (BEFORE refactor — preserves byte-stable baseline)
- **Phase 3**: Refactor the audit test (rename test, replace line-index access with semantic+snapshot, replace SHA constant with fixture-derived SHA, remove failing wrapper-source SHA-propagation test); verify pytest still binds against same content
- **Phase 4**: Apply Tavily-first refactor to rf-team-lead.md per proposal (frontmatter reorder + subsection replacement + Critical Rule 11); run `make sync-dev` + `make verify-sync`; run pytest
- **Phase 5**: Replace cross-references — 6 occurrences of `rf-team-lead.md:417` across 3 files; `make sync-dev`; verify lint clean
- **Phase 6**: Markdownlint remediation on rf-team-lead.md (same pattern as parent task's child)
- **Phase 7**: Final aggregation + commit + verify all 16 pre-commit hooks pass + Task Summary + move to done/

---

## TEMPLATE_NOTES

- **Template 02** (complex multi-phase): required because (a) discovery before edits in Phase 1, (b) per-phase verification gates, (c) conditional flows (if fixture extraction fails, halt), (d) aggregation in Phase 7
- **QA_GATE_REQUIREMENTS: PER_PHASE** — per BUILD_REQUEST "Include phase-by-phase plans with per-phase QA gates"
- **VALIDATION_REQUIREMENTS**: lint + verify-sync + pytest must all pass with 0 NEW failures vs 102-failed baseline; pre-commit hooks must run cleanly
- **TESTING_REQUIREMENTS**: UNIT (the audit test IS the test that proves the refactor preserves byte-stability of the Fix Cycles rule)
- **EXECUTION_CONTEXT_REQUIREMENTS: REQUIRED** — three named source areas: rf-team-lead agent, audit test, cross-reference files
- **L1 Discovery + L2 Build + L3 Test + L4 Review patterns** used across phases

---

## AMBIGUITIES_FOR_USER

None — the BUILD_REQUEST is fully specified. Path C scope is explicit: refactor audit test to snapshot mechanism + apply Tavily-first refactor + update cross-references. Pre-existing baseline failures (the 10 wrapper-source tests currently failing) are explicitly OUT of scope per Path C decision.

One scope-confirmation note logged in the task file's Open Questions section: "If user wants the wrapper-source tests fixed alongside, that becomes a separate task (the WRAPPER_SOURCES tuple covers rf-analyst.md and rf-qa-qualitative.md which don't currently have the strings; adding them would be a content edit to those agents)."
