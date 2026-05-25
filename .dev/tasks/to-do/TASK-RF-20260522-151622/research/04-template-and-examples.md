# Research: Template 02 + Spec-Edit Examples

**Topic type:** Template & Examples
**Scope:** MDTM template 02 PART 1, prior TASK-RF spec-edit examples
**Status:** In Progress
**Date:** 2026-05-22
---

## Section 1: Template 02 PART 1 rules (verbatim)

**Source:** `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` (PART 1 spans lines 46-870).

### A3. COMPLETE GRANULAR BREAKDOWN (lines 91-95, verbatim)

```
A3. COMPLETE GRANULAR BREAKDOWN
   - Break down EVERY workflow phase into atomic, verifiable checklist items
   - Create individual checklist items for EVERY file, component, or iteration
   - NO high-level or bulk operations allowed - everything must be granular
   - Include exact file paths, specific requirements, and measurable outcomes
```

### A4. ITERATIVE PROCESS STRUCTURE (lines 97-116, verbatim)

```
A4. ITERATIVE PROCESS STRUCTURE
   - For ANY process involving multiple items (files, components, etc.):
     * Pre-enumerate ALL items to be processed in initial step
     * Create individual checklist item for each specific item
     * Require incremental updates after each item
     * Include consolidation step only after all items complete
   - Use this pattern:
     ``` markdown
     **Step X.1:** Scan and enumerate all [items] in [location]
     - [ ] Complete [item] listing generated: [count] items identified

     **Step X.2:** Process each [item] individually:
     - [ ] [Item 1]: [exact identifier] - [specific action] completed
     - [ ] [Item 2]: [exact identifier] - [specific action] completed
     [Continue for each item]

     **Step X.3:** Consolidate all individual results
     - [ ] All [count] items processed and results logged
     - [ ] Consolidated output created per requirements
     ```
```

### B2. THE 6-ELEMENT SELF-CONTAINED ITEM PATTERN (lines 142-149, verbatim)

```
B2. EVERY CHECKLIST ITEM MUST BE A COMPLETE, SELF-CONTAINED PROMPT THAT INCLUDES:
   1. **Context Reference with WHY** - What file(s) to read and why that context is needed for this specific action
   2. **Action with WHY** - What to do with that context and why it needs to be done
   3. **Output Specification** - The exact output file name, location, what content to produce, and template to follow (if applicable)
   4. **Integrated Verification** - An "ensuring..." clause that specifies what must be verified (DO NOT assume, hallucinate, or make up any information - all content MUST be derived from source files referenced in the checklist item, 100% accuracy based on source materials, document negative evidence when verification fails)
   5. **Evidence on Failure Only** - Log to task notes ONLY if unable to complete due to blockers, missing info, or errors (successful completion is evidenced by the output file itself)
   6. **Explicit Completion Gate** - "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."
```

### B3. ONE-PARAGRAPH PROSE PATTERN (lines 150-153, verbatim)

```
B3. THE SELF-CONTAINED PATTERN
   Each checklist item should be written as ONE FULL PARAGRAPH (not multiple lines
   or bullets) that is verbose and explanatory. The item should read like a complete
   prompt that could be executed independently without any prior context.
```

### B5. FORBIDDEN PATTERNS (lines 164-184, key excerpts)

```
B5. FORBIDDEN PATTERNS:
   - Standalone "read context" items that don't produce output
     ...
   - Missing context reference (no source of truth)
     ...
   - Multi-line/bulleted checklist items (must be single paragraph)
     ...
   - Separate verification/confirmation items (integrate via "ensuring..." clause)
   - Overly granular items (e.g., "create directory" alone)
   - Separate REMINDER blocks between checklist items
```

### L1. DISCOVERY ITEM PATTERN (lines 737-747, verbatim)

```
L1. DISCOVERY ITEM PATTERN
   **When:** An item needs to explore the codebase, environment, or data and produce
   structured findings that later items will use as input.

   **Key rule:** The discovery file IS the deliverable. Later items read it directly.
   The discovery item must write a well-structured, machine-readable output file.
```

### L2. BUILD-FROM-DISCOVERY ITEM PATTERN (lines 749-759, verbatim)

```
L2. BUILD-FROM-DISCOVERY ITEM PATTERN
   **When:** An item creates an output based on a previous discovery item's findings.
   The item reads both the discovery file AND the original source files.

   **Key rule:** Always reference the discovery file path AND the source file path.
   The discovery file tells you WHAT to process; the source file provides the CONTENT.
```

### L3. TEST/EXECUTE ITEM PATTERN (lines 761-771, verbatim)

```
L3. TEST/EXECUTE ITEM PATTERN
   **When:** An item needs to run a command, script, or test suite and capture the
   results for later items to assess.

   **Key rule:** Always capture BOTH raw output AND a structured summary. The raw
   output preserves full detail; the summary enables quick assessment by later items.
```

### L4. REVIEW/QA ITEM PATTERN (lines 773-783, verbatim)

```
L4. REVIEW/QA ITEM PATTERN
   **When:** An item needs to assess the quality of a previous item's output by
   comparing it against source materials, specifications, or requirements.

   **Key rule:** The review must produce a structured verdict (PASS/FAIL) with
   specific findings. Never produce a vague "looks good" assessment.
```

### L5. CONDITIONAL-ACTION ITEM PATTERN (lines 785-797, verbatim)

```
L5. CONDITIONAL-ACTION ITEM PATTERN
   **When:** An item's behavior depends on the result of a previous item (typically
   a test or review item). The item reads a status/result file and takes different
   actions based on what it finds.

   **Key rule:** The item MUST handle BOTH branches (success AND failure). Specify
   exactly what to do in each case. The output file is always created regardless
   of which branch is taken.
```

### L6. AGGREGATION ITEM PATTERN (lines 799-805, verbatim)

```
L6. AGGREGATION ITEM PATTERN
   **When:** An item needs to consolidate multiple previous outputs into a single
   report, summary, or deliverable. Typically used as the final item in a phase.

   **Key rule:** Use Glob to find all relevant files, read each one, and produce
   a consolidated output. Don't hardcode file lists - discover them dynamically.
```

### M1. PHASE-GATE QA SEQUENCE (lines 843-850, verbatim)

```
M1. PHASE-GATE QA SEQUENCE
   A phase-gate QA sequence consists of 2-3 items inserted between phases:

   **Item 1 (Aggregation — L6 pattern):** Collect all outputs from the preceding phase into a summary or inventory file. Use Glob to find files dynamically if the phase produces a variable number of outputs.

   **Item 2 (QA Agent Spawn):** Spawn rf-qa (structural verification) with the appropriate phase type. The item MUST include: agent name, phase type, input file paths, output report path, verdict handling, and error clause. If qualitative QA is also required for the document type, spawn rf-qa-qualitative in a SEPARATE item immediately following (sequential — qualitative runs after structural passes).

   **Item 3 (Conditional Proceed — L5 pattern):** Read the QA report. IF verdict is PASS, proceed to next phase. IF verdict is FAIL, execute the fix cycle: address findings, re-run QA (up to the max cycles defined in I16), then re-check verdict.
```

### E1. Checkbox format / Acceptance Criteria (lines 278-292, key excerpts)

Template 02 uses `- [ ]` for unchecked actionable items and `- [x]` for completed items. There is no separate "Acceptance Criteria" section — every actionable claim IS a checkbox.

```
E1. CHECKBOX FORMAT
   - EVERY actionable item MUST be a checkbox: `- [ ] Action text`
   - NO nested checkboxes (flat structure only)
   - NO parent checkboxes that summarize children
   - Each checkbox is ONE atomic, verifiable action
   - Use **Step X.Y:** headers for grouping, NOT checkboxes
   - Checkboxes MUST appear in the exact order they will be completed
   ...
   - NEVER create parent checkbox items with child checkbox items - use descriptive headers instead
```

### Anti-orphaning rules for task-completion items (I13 + I17, lines 581-635, key excerpts)

```
I13. POST-COMPLETION ACTIONS (final task items only)
   - Every task MUST include a Post-Completion Actions section
   - Include items for: updating frontmatter (status, completion_date, updated_date), logging completion to Execution Log
   - Post-completion validation items (I17) handle output verification before the frontmatter update
   - Do NOT create a separate "Task Completion and Handoff Protocol" section in the task body
```

```
I17. POST-COMPLETION VALIDATION PROTOCOL
   Before the frontmatter status is set to Done, the task MUST include validation items that verify:
   1. All `- [ ]` items have been marked `- [x]` (no items skipped)
   2. All output files specified in checklist items exist on disk (verified via Glob)
   3. Any blocker entries in the Task Log have resolution notes
   4. If the task modified source code: all relevant tests pass

   These items appear in the ## Post-Completion Actions section of PART 2, BEFORE the frontmatter update item.
```

### Multi-anchor edit rule (no explicit rule — convention from A3 + B5)

Template 02 has no explicit "multi-anchor edit" rule. The implicit rule from A3 + B5 is: **one checklist item per edit anchor** (per file region with verbatim before/after text). Batching multiple anchors into one item is forbidden by B5 ("Multi-line/bulleted checklist items must be single paragraph") and A3 ("Create individual checklist items for EVERY file, component, or iteration").

### Grep-verification item rule (no explicit rule — implicit from L3 + B2)

Template 02 has no "L-pattern" specifically for grep checks. The convention (confirmed by Section 3 examples) is: **one combined L3 Test/Execute item per phase**, batching multiple greps into a single Bash invocation that captures all greps to one combined output file — because each grep is too small to merit its own item under A3.

### I18. Testing requirements for code-modifying tasks (lines 637-646, verbatim)

```
I18. TESTING REQUIREMENTS FOR CODE-MODIFYING TASKS
   If a task creates or modifies source code files (not documentation, not configuration), the orchestrator MUST include at least one testing checklist item. This item MUST:
   1. Specify the test command to run (e.g., "Run `uv run pytest tests/path/ -v`")
   2. Define pass criteria (e.g., "all tests pass with no regressions")
   3. Specify where test results are captured (e.g., a test-results file in phase-outputs/)
   4. Follow the self-contained item pattern from B2

   For Template 02 tasks: use the L3 (Test/Execute) pattern for testing items.
```

Note: I18 applies to "source code files (not documentation, not configuration)". A skill spec edit is documentation — testing is NOT required by I18.

---

## Section 2: Execution Context block rules (DM-001)

**Source:** `/config/workspace/IronClaude/src/superclaude/skills/task-builder/SKILL.md` lines 903-1004 (BUILD_REQUEST emitter rules) and lines 1755-1797 (rendered-form contract).

### Preamble (SKILL.md lines 908-927, verbatim)

```
    EXECUTION CONTEXT BLOCK (OPTIONAL, TASK-LEVEL ROLL-UP):
    Emit an `## Execution Context` section immediately after frontmatter
    (before # Title body content) when BUILD_REQUEST exposes enough rollup
    signal — typically when ≥3 distinct source areas can be inferred from
    research files. This is a READING aid for the executor, NOT a substitute
    for per-item Context fields.

    Signal control (API-001-M2): the `EXECUTION_CONTEXT_REQUIREMENTS`
    BUILD_REQUEST field overrides the AUTO heuristic when set. REQUIRED
    forces emission (degraded References-only form permitted on GOAL-only
    input); SUPPRESS forbids emission (per-item Context fields untouched);
    AUTO / omission applies the rollup-signal heuristic below. Violation of
    the signal (emit-under-SUPPRESS or omit-under-REQUIRED) is MALFORMED
    output and triggers the max-2 retry flow at SKILL.md A.9.
```

### R-033 — References emitter (SKILL.md lines 928-937, verbatim)

```
    - **References emitter (DM-001.References — R-033):** A single
      labeled bullet `**References:**` followed by `R-###: <ref-line>`
      entries separated by `; `. `###` is a zero-padded ordinal starting
      at `001`, assigned in stable input order: BUILD_REQUEST GOAL
      first, then WHY, then each related-doc ID in BUILD_REQUEST source
      order. `<ref-line>` is the verbatim text of the source field — do
      not rewrite or summarize; strip only trailing whitespace. ALWAYS
      present whenever the block is emitted; never blank, never omitted
      (under minimal-BUILD_REQUEST degradation, GOAL alone produces at
      least `R-001`).
```

### R-034 — Source areas emitter (SKILL.md lines 938-951, verbatim)

```
    - **Source areas emitter (DM-001.SourceAreas — R-034):** A single
      labeled bullet `**Source areas:**` followed by named modules or
      packages, comma-separated (e.g., "rf-qa agent prompts",
      "task-builder skill body"). Emit only when ≥3 distinct named areas
      can be inferred from the research files; otherwise OMIT the bullet
      entirely (do not emit a blank-but-present line). **No-file-paths
      guard (NFR-CONV.3 hidden-input determinism — MANDATORY
      pre-emission scan):** the rendered bullet MUST satisfy
      `grep -cE "src/|/.*:[0-9]+"` returning 0. If any hit is found,
      reject the candidate, rewrite area names to remove paths and `:NN`
      line numbers (rename a candidate like `src/superclaude/agents/rf-qa.md`
      to `rf-qa agent prompt`), and re-scan. Specific `path.py:NN`
      references belong in per-item Context fields and `research/*.md`,
      never here.
```

### R-035 — Key constraints emitter (SKILL.md lines 952-962, verbatim)

```
    - **Key constraints emitter (DM-001.KeyConstraints — R-035):** A
      single labeled bullet `**Key constraints:**` followed by 1–3
      entries separated by `; `. Entries are pulled **verbatim** from
      BUILD_REQUEST `QA_GATE_REQUIREMENTS` /
      `VALIDATION_REQUIREMENTS` / `TESTING_REQUIREMENTS` (priority
      order) or from the highest-severity invariants in research
      findings — do NOT paraphrase. Bounded strictly to 1–3 entries:
      when >3 candidates exist, keep the top 3 by priority order and
      drop the rest (do not concatenate beyond 3). OMIT the bullet
      entirely when BUILD_REQUEST and research findings produce no
      clear constraint shortlist.
```

### R-038 — Degradation rule (SKILL.md lines 972-984, verbatim)

```
    Degradation rule (R-038 — minimal BUILD_REQUEST → References-only):
    When BUILD_REQUEST is "minimal" — defined as GOAL is the only populated
    rollup-signal field (WHY may be empty or duplicate GOAL; no
    related_docs; no QA_GATE_REQUIREMENTS / VALIDATION_REQUIREMENTS /
    TESTING_REQUIREMENTS entries; <3 inferable source areas across all
    research files) — the block degenerates to a single `**References:**`
    bullet. The Source areas and Key constraints bullets are **absent**
    from the rendered block (not present-and-blank, not stub-bulleted).
    The block heading `## Execution Context` remains; the
    `<!-- OPTIONAL header ... -->` reader-aid comment remains; only the
    two omitted bullets are physically gone from the output. If even
    GOAL-derived References cannot be produced (truly empty BUILD_REQUEST),
    OMIT the entire block — heading included.
```

### R-039 — Header-wide hidden-input determinism guard (SKILL.md lines 986-1004, verbatim)

```
    Header-wide hidden-input guard (R-039 — NFR-CONV.3 enforcement at the
    block boundary, MANDATORY post-assembly scan): after the three
    emitters have run and the bullets have been concatenated into the
    candidate block, run `grep -cE "src/|/.*:[0-9]+"` against the byte
    range from the `## Execution Context` heading line through the
    closing `---` separator. The count MUST be 0. The per-emitter
    Source-areas guard at the rule above is a first line of defense; this
    header-wide guard is the final boundary check, catching any
    BUILD_REQUEST-derived path leak in References (verbatim GOAL/WHY text)
    or Key constraints (verbatim invariant text) that the per-emitter
    rules cannot reach. On any hit (count ≥ 1), DO NOT emit the block —
    rewrite the offending bullet to remove the path / `:NN` reference
    (e.g., a GOAL line mentioning `src/foo/bar.py:42` becomes "the foo
    module" or "the bar handler"), re-run the assembly, and re-scan.
    Allow at most one rewrite cycle; if the scan still hits, OMIT the
    entire block and surface a `header-leak-suppressed` annotation in
    the builder's return value. The check applies uniformly to the
    fully-populated 3-bullet form and to the degraded References-only
    form.
```

### Verdict for THIS task build (TASK-RF-20260522-151622)

The Wave 1.5 Documentation Grounding build qualifies for the **fully-populated 3-bullet form** under AUTO heuristic.

- **References (R-033):** R-001 from BUILD_REQUEST GOAL + R-002 from WHY → ≥1 entries always present ✓
- **Source areas (R-034, requires ≥3 distinct named modules):**
  1. "sc:troubleshoot command surface" — the slash command file
  2. "sc-troubleshoot-protocol skill body" — the SKILL.md
  3. "troubleshoot protocol refs subsystem" — the refs/ directory and its loader table

  Count = 3, threshold satisfied ✓ . R-034 pre-emission grep scan (`grep -cE "src/|/.*:[0-9]+"`) returns 0 — these are conceptual module names without paths or `:NN`.

- **Key constraints (R-035, 1-3 verbatim entries):**
  1. "Edit the canonical source tree only — never the dev-copy mirror directly" (rewritten from BUILD_REQUEST to avoid the `src/` substring that would trip R-039)
  2. "Do not reimplement other skills' protocols inline — load on demand only"
  3. "Diagnose-first contract unchanged — Wave 1.5 must not auto-execute fixes"

  Count = 3, satisfies 1–3 bound ✓. R-039 post-assembly grep scan returns 0 — no `src/` or `:NN` leaked.

**Important builder note:** If BUILD_REQUEST writes a Key constraint as "Edit src/superclaude/ only — never .claude/<not-settings.json>", the builder MUST rewrite at emission time to avoid the `src/` substring (R-039 scan would flag it). The TASK-RF-20260520-230051 task (Section 3 below) demonstrates this pattern: its Key constraints uses "Source of truth is the superclaude source tree; never edit the dev-copy tree directly" — clean of `src/` literal.

**Verdict:** `EXECUTION_CONTEXT_REQUIREMENTS: AUTO` (or omitted). Fully-populated 3-bullet form will emit. Builder must apply R-039 rewrite to Key constraint #1.

---

## Section 3: Prior TASK-RF spec-edit examples

### Example 1: TASK-RF-20260520-230051 — PR #64 remediation (SKILL.md + hook + JSON)

**Path:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260520-230051/TASK-RF-20260520-230051.md`
**Status:** 🟢 Done (executed successfully)
**Template:** 02
**Scope:** Three edits across three files — `src/superclaude/hooks/scripts/offer-pr-review.sh` (POSIX prefilter), `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` lines 163-170 (pipeline consolidation), `src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json` (3 empty `assertions: []` arrays populated). This is the closest analog to the Wave 1.5 build — a SKILL.md spec edit + sync-dev/verify-sync gate + per-file integrity gates.

#### Phase structure (lines 131-263)

- **Phase 1 — Preparation and Setup** (3 items): status update, verify handoff dirs, capture pre-edit baseline snapshots of all 3 modified regions to `phase-outputs/discovery/baseline-*.txt`.
- **Phase 2 — Fix 1 (M2) offer-pr-review.sh prefilter** (2 items): one Edit item with verbatim old_string/new_string embedded in Context, one L3 Test/Execute item batching 3 integrity checks (`bash -n`, `shellcheck`, `grep -F` for prefilter presence) to `fix-1-gates.txt`.
- **Phase 3 — Fix 2 (M1) SKILL.md pipeline consolidation** (2 items): one Edit item rewriting L163-170 with verbatim before/after embedded; one L3 Test/Execute item batching 3 integrity checks (frontmatter present, pipeline string present, `pre-commit run markdownlint`).
- **Phase 4 — Fix 3 (M4) evals.json assertions populated** (4 items): three Edit items (one per scenario in evals.json, with disambiguating old_string context) + one L3 Test/Execute item batching `jq .` (parse check) and `jq -e '[.evals[] | .assertions | length == 3] | all'` (assertion-count check).
- **Phase 5 — Sync, Validate, and Final QA Gate** (4 items): `make sync-dev`, `make verify-sync` (the SOLE src/↔.claude/ parity gate — NOT in CI), `make lint`, `make lint-architecture` — each its own L3 item capturing output to `phase-outputs/test-results/`.
- **Phase Gate — Quality Verification (FINAL_ONLY)** (3 items): L6 aggregation of all gate output files into a single report; rf-qa spawn with ADVERSARIAL STANCE + `fix_authorization: true`; final L5 conditional-proceed.

#### Execution Context block (lines 118-126, verbatim)

```
## Execution Context

<!-- Reader-aid header: rollup of references, source areas, and key constraints
     for the whole task. NO file:line paths here; those live in per-item Context. -->

- **References:** R-001: Land three targeted source-of-truth fixes on branch feature/sc-auggie-review-protocol that close M1 (offer-pr-review.sh prefilter), M2 (SKILL.md L163-170 rewrite), and M4 (evals.json assertions populated) from PR #64's auggie-review; R-002: PR #64 introduces the sc-auggie-review-protocol skill and the skill's self-review surfaced 4 Medium findings of which the top 3 are triaged here; R-003: PR #64 REVIEW.md report at the path documented in related_docs.
- **Source areas:** the offer-pr-review hook script, the sc-auggie-review-protocol SKILL.md, and the sc-auggie-review-protocol evals harness manifest.
- **Key constraints:** Source of truth is the superclaude source tree; never edit the dev-copy tree directly; the sync-dev make target produces the dev copies; the verify-sync make target is the sole parity gate between the two trees and is NOT in CI — it must run before commit; the hook script must remain fail-open (exit zero) and the prefilter MUST NOT introduce non-zero exit paths.
```

**Note R-039 compliance:** Source areas uses conceptual names ("offer-pr-review hook script", "sc-auggie-review-protocol SKILL.md", "sc-auggie-review-protocol evals harness manifest"). Key constraints uses "the superclaude source tree" rather than `src/superclaude/` — pre-emption of R-039 grep.

#### Per-anchor edit items pattern (lines 153, 165, 195, 209, 223)

**One item per edit anchor**, each item embeds:

- File path (absolute)
- Line range (e.g., "lines 17-21", "L163-170", "L10")
- Verbatim `old_string` block fully embedded in Action
- Verbatim `new_string` block fully embedded in Action
- "ensuring..." clause naming every byte-level invariant (quoting style, indent, fail-open contract, no-trailing-comma, etc.)
- Blocker logging clause to `### Phase N Findings` section
- Completion gate sentence

**Pitfall noted in the task itself (lines 161, 181):** the `grep -F` checks for verbatim presence MUST NOT be wrapped in `bash -c '...'` because the embedded single-quotes collide with the outer quoting and produce "unexpected EOF while looking for matching '". Empirically reproduced during QA review.

#### How sync-dev + verify-sync items were structured (lines 239, 243)

**One item per make target, in sequence:**

- Item 1 (L3): `cd /config/workspace/IronClaude && make sync-dev 2>&1` → tee `phase-outputs/test-results/sync-dev.txt`. Pass criterion: exit 0 + output mentions all 3 changed-file paths.
- Item 2 (L3): `cd /config/workspace/IronClaude && make verify-sync 2>&1` → tee `phase-outputs/test-results/verify-sync.txt`. Plus writes a conditional verdict file at `phase-outputs/plans/verify-sync-verdict.md` (L5 pattern embedded). Pass criterion: exit 0 with NO `❌ MISSING` or `⚠️ DIFFERS`.
- Item 3 (L3): `make lint` → tee `make-lint.txt`. Pass criterion: exit 0, no NEW ruff warnings vs baseline.
- Item 4 (L3): `make lint-architecture` → tee `make-lint-architecture.txt`. Pass criterion: exit 0.

#### How grep-verification items were structured (lines 157, 181, 231)

**One item per phase, batching multiple greps into a single Bash invocation** that runs all checks and tees combined output to `phase-outputs/test-results/fix-N-gates.txt`. Each grep is paired with a `&& echo "<TAG> OK" || echo "<TAG> FAIL"` so the output file is machine-grep-able for pass tags.

Example structure (Phase 2 fix-1-gates):

1. `bash -n offer-pr-review.sh && echo "SYNTAX OK"`
2. `shellcheck --severity=warning offer-pr-review.sh && echo "SHELLCHECK OK"`
3. `grep -F "<verbatim prefilter line>" offer-pr-review.sh && echo "PREFILTER PRESENT"`

All three commands redirect to the same combined file.

#### How L1-L6 handoff blocks were used

- **L1 Discovery:** Phase 1 Step 1.3 (baseline snapshots → `phase-outputs/discovery/baseline-*.txt`)
- **L3 Test/Execute:** Every integrity-gate item, every `make` item — 9 instances total
- **L5 Conditional-Action:** Embedded inside the verify-sync item (conditional verdict file based on exit code)
- **L6 Aggregation:** Phase Gate Step PG.1 (Glob all `phase-outputs/test-results/*.txt` + `*.json`, read each, build consolidated `phase-2-5-aggregation.md`)
- **L4 Review/QA + L5 Conditional-Proceed:** Final rf-qa spawn item with adversarial stance + fix_authorization + max-2-cycle fix loop

#### Pitfalls noted in the task itself

- Empirically reproduced QA pitfall: do NOT wrap grep-with-embedded-single-quotes inside `bash -c '...'` — quoting collisions cause "unexpected EOF" errors. Invoke grep directly via Bash tool.
- Disambiguating old_string for repeated patterns: when `"assertions": []` appears at 3 locations in evals.json, the Edit tool's "non-unique match" error fires. Each Edit item includes enough surrounding context (`"id": 1`, `"name": "local-pr"`) in old_string to disambiguate.
- Tab indentation on Makefile-style files: must use literal tabs, not spaces. The task verifies via `cat -A` for `^I` (tab byte).
- Markdownlint auto-fix side effect: `pre-commit run markdownlint` MAY auto-fix issues and leave the file dirty — the task instructs re-running the gate and re-staging.

---

### Example 2: TASK-RF-20260518-cliEval-P4-wire-and-ship — cliEval P4 wiring

**Path:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260518-cliEval-P4-wire-and-ship/TASK-RF-20260518-cliEval-P4-wire-and-ship.md`
**Status:** 🟡 To Do (not yet executed but built and validated)
**Template:** 02
**Scope:** Wire `eval_group` into `src/superclaude/cli/main.py` (2 lines), add `make eval-real` target to `Makefile`, append 3 patterns to `.gitignore`, add `.dev/eval-runs/.gitkeep`, create Click CliRunner tests at `tests/cli/test_eval/test_wiring.py`. This is a mixed code + config + spec edit task — useful comparison.

#### Phase structure (skimmed from grep)

- **Phase 1 — Setup & Prereq Verification** (3 items): P1+P2+P3 merged check via `git log`, branch creation, pre-test baseline capture
- **Phase 2 — Wire `eval_group` into `cli/main.py`** (3 items): insertion-point discovery (L1), the 2-line Edit (one item), help-output verification (L3 batching 2 greps)
- **Phase 3 — Add `eval-real` Makefile target + .gitignore patterns + .gitkeep** (4 items): one item per file edit + verifications
- **Phase 4 — onward** truncated in this preview but follows the same Discovery → Edit → L3-verify cadence

#### Execution Context block (lines 71-75, verbatim)

```
## Execution Context

<!-- Task-level READING aid. Per-item Context fields and research/*.md remain the evidence venue with file:line citations. This block contains NO specific path.py:NN references. -->

- **References:** R-001: cliEval-P4 wire-and-ship — wire `eval_group` into top-level CLI + Makefile target + gitignore + Click CliRunner tests + commit + PR; R-002: P4 is the user-visible ship gate for the cliEval harness (~50 LOC, smallest phase, depends on P1+P2+P3 all merged); R-003: BUILD-REQUEST-cliEval-P4-wire-and-ship; R-004: cliEval design-spec sections 3, 10, 17; R-005: existing top-level CLI add_command registration block (alphabetical insertion model — see per-item Context for line citations); R-006: Makefile verify-sync target (structural model for the new eval-real target — see per-item Context for line citations).
- **Source areas:** superclaude top-level CLI dispatcher, cliEval Click group, project Makefile, repo-root gitignore, cliEval wiring tests, eval-run artifact root.
- **Key constraints:** P1+P2+P3 MUST all be merged to master before P4 begins; `make verify-sync` MUST exit 0 post-P4 (no regression); full pytest suite MUST produce zero NEW failures vs. pre-P4 baseline; eval_group import + add_command must be placed alphabetically between `cli_portify` and `prd` registrations.
```

**Note R-039 compliance:** "Source areas" uses 6 conceptual names (no paths, no `:NN`). Key constraints embeds `make verify-sync` and `eval_group` as identifiers but no `src/` or `:NN` — clean. References R-005 says "see per-item Context for line citations" — explicitly cordoning evidence venues.

#### Effective patterns observed

- Pre-edit confirmation item (one per file): Read the current source, write a snapshot to `phase-outputs/discovery/`, compare against research-recorded line numbers — flag drift before editing.
- Pure-additive edit verification: `git diff` after each edit, item asserts "diff is precisely N lines added, zero lines removed".
- Machine-checkable help-output checks: `grep -E '^\s+eval\s'` on `superclaude --help` output for presence, and `grep -cE '^\s+(doctor|list|describe|run)\s'` for count ≥ 4.
- `make -n` (dry-run) for Makefile target verification without executing the real (expensive) workload.
- `git check-ignore -v` for both positive ("file IS ignored") and negative ("file NOT ignored") cases.
- Collision detection items: every Edit item has a fallback clause "If P1/P2/P3 already wired X (collision), log CRITICAL and skip" — graceful handling of dependency-already-done.

---

## Section 4: Common pitfalls + effective patterns

### Common A3 granularity failure modes

- **Batching all SKILL.md edits into one item.** If Wave 1.5 requires (a) inserting a wave header, (b) adding a row to the wave table, (c) adding a row to the loader table, (d) adding a row to the graceful-degradation table, that's 4 anchors → 4 items, not 1.
- **Batching multiple greps into one item without `--label`/`echo` tags.** A single grep item is fine, but the output must be machine-checkable for pass tags (e.g., `&& echo "WAVE-HEADER PRESENT"`).
- **Combining the edit + the verification into one item.** Forbidden by B5 (separate verification items). The "ensuring..." clause INSIDE the Edit item handles structural verification; the L3 grep gate is a separate downstream item per phase, batching all greps for that phase.
- **"Read SKILL.md to understand the structure"** as a standalone item. Forbidden by B5 ("Standalone read context items that don't produce output"). The Read must be paired with an Edit or write that produces an output file.

### Self-contained items for markdown spec edits (verbatim quotes pattern)

Both prior examples demonstrate:

- **Embed the verbatim `old_string` and `new_string` directly in the Action field**, not by reference to research files. This is "executor self-containment" — the executor must NOT need to read a research file mid-execution to know what to edit. The 230051 task says explicitly (Phase 2 item, line 153): "The verbatim before/after text is in research file ... but it is embedded directly in this item for executor self-containment."
- **Cite line ranges in the Action field** (e.g., "lines 163-170") — these are inside per-item Context, NOT the task-level Execution Context block. R-039 only applies to the header.
- **Embed disambiguating context** when the same pattern appears multiple times (e.g., `"assertions": []` at 3 locations → include `"id": N` and `"name": "..."` in old_string).

### Standard sync-dev + verify-sync item shape

Two consecutive L3 items at the end of the main edit phases:

1. **`make sync-dev` item:** `cd /config/workspace/IronClaude && make sync-dev 2>&1` → tee `phase-outputs/test-results/sync-dev.txt`. Pass criterion: exit 0 + output mentions the edited file paths.
2. **`make verify-sync` item:** `cd /config/workspace/IronClaude && make verify-sync 2>&1` → tee `phase-outputs/test-results/verify-sync.txt`. Plus optionally writes an L5 conditional verdict file. Pass criterion: exit 0 with NO `❌ MISSING` or `⚠️ DIFFERS`.

### Grep-verification item shape

**One L3 item per phase**, batching all greps for that phase into a single Bash invocation:

```
- [ ] Use the Bash tool to run [N] integrity checks against the edited file(s) ...
      and capture combined output to phase-outputs/test-results/phase-N-gates.txt.
      The checks are:
      (1) <command> && echo "<TAG-1> OK" || echo "<TAG-1> FAIL"
      (2) <command> && echo "<TAG-2> OK" || echo "<TAG-2> FAIL"
      (3) <command> && echo "<TAG-3> OK" || echo "<TAG-3> FAIL"
      Pass criteria: <TAG-1> OK, <TAG-2> OK, <TAG-3> OK.
      If any check FAILs, do NOT attempt to fix in this step —
      log the specific failure in ### Phase N Findings, then mark complete.
```

### Phase organization for spec edits

The canonical 5-phase structure for a SKILL.md / spec edit (from Example 1):

1. **Phase 1 — Preparation:** status update, handoff dir verify, baseline snapshots of every modified region
2. **Phase 2+** — One phase per logical fix area; each phase contains: 1+ Edit item(s) → 1 L3 batched grep gate item
3. **Phase N — Sync, Validate, Final Gate:** make sync-dev → make verify-sync → make lint → make lint-architecture (each its own L3 item)
4. **Phase Gate — FINAL_ONLY QA:** L6 aggregation → rf-qa spawn (adversarial + fix_authorization) → L5 conditional-proceed
5. **Post-Completion Actions:** Glob verify outputs, task summary, frontmatter update

### Pitfalls to avoid in the new task file

- `bash -c '...'` collision with single-quoted grep patterns — invoke grep directly
- Repeated patterns require disambiguating context in old_string
- Markdownlint auto-fix may dirty the file — re-stage after gate
- Forgetting `chmod +x` after sync-dev for hook scripts (Makefile L138-143 does this automatically)
- Forgetting to update the OPTIONAL reader-aid comment when emitting Execution Context block (it lives between the heading and the bullets)
- R-039 leak from BUILD_REQUEST verbatim text — rewrite at emission time

---

## Section 5: Recommended BUILD_REQUEST values

For the Wave 1.5 Documentation Grounding task build:

| Field | Recommended Value |
|---|---|
| `TEMPLATE` | `02` (confirmed — discovery + multi-anchor edits + sync gates + QA gate) |
| `QA_GATE_REQUIREMENTS` | `PER_PHASE` (each anchor-edit phase benefits from a phase-level grep gate before sync-dev) |
| `VALIDATION_REQUIREMENTS` | `make sync-dev passes; make verify-sync passes; grep -n "Wave 1.5" SKILL.md returns at least the new wave header; grep -n "no-doc-discovery" troubleshoot.md returns the new flag row; test -f refs/doc-discovery.md returns success; SKILL.md wave list / refs loader table / graceful-degradation table internally consistent.` |
| `TESTING_REQUIREMENTS` | `NONE` (no runtime tests — this is a spec edit; per I18, documentation edits do NOT require testing. Validation gates substitute.) |
| `EXECUTION_CONTEXT_REQUIREMENTS` | `AUTO` (will emit the 3-bullet form per Section 2 verdict; builder MUST apply R-039 rewrite to any Key constraint containing literal `src/`) |

### Builder-emission Execution Context block (recommended verbatim)

```
## Execution Context

<!-- Reader-aid header: rollup of references, source areas, and key constraints
     for the whole task. NO file:line paths here; those live in per-item Context. -->

- **References:** R-001: <verbatim GOAL from BUILD_REQUEST>; R-002: <verbatim WHY from BUILD_REQUEST>; R-003: <verbatim related_docs[0] description if present>.
- **Source areas:** sc:troubleshoot command surface, sc-troubleshoot-protocol skill body, troubleshoot protocol refs subsystem.
- **Key constraints:** Edit the canonical source tree only — never the dev-copy mirror directly; do not reimplement other skills' protocols inline — load on demand only; diagnose-first contract unchanged — Wave 1.5 must not auto-execute fixes.
```

R-039 post-assembly scan against the above renders 0 (no `src/`, no `:NN`).

---

## Summary

- **Section 1:** Template 02 PART 1 (lines 46-870) provides A3 granularity, A4 iterative structure, B2's 6-element self-contained item pattern, L1-L6 handoff patterns, M1 phase-gate QA composite — all quoted verbatim from `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md`.
- **Section 2:** Execution Context block is governed by DM-001 frozen contract (R-033/R-034/R-035 emitters + R-038 degradation + R-039 hidden-input determinism guard). The Wave 1.5 build qualifies for fully-populated 3-bullet form (3 source areas + 3 key constraints); builder must rewrite the `src/superclaude/` Key constraint to "the canonical source tree" to pass R-039.
- **Section 3:** TASK-RF-20260520-230051 (PR #64 remediation — SKILL.md edit + sync gates + adversarial rf-qa) is the closest analog and provides the canonical 5-phase structure: Preparation → per-fix phases (Edit + L3 grep gate) → Sync/Validate → FINAL_ONLY QA Gate → Post-Completion. TASK-RF-20260518-cliEval-P4-wire-and-ship provides a secondary pattern for pure-additive edits with `git diff` line-count assertions.
- **Section 4:** Key pitfalls: do not batch anchors into one item, do not wrap grep with single-quotes inside `bash -c`, embed disambiguating old_string context for repeated patterns, rewrite Key constraints with literal `src/` substring to pre-empt R-039.
- **Section 5:** Recommended BUILD_REQUEST: `TEMPLATE: 02`, `QA_GATE_REQUIREMENTS: PER_PHASE`, `VALIDATION_REQUIREMENTS: make sync-dev + make verify-sync + 3 greps + test -f for refs/doc-discovery.md + internal-consistency check`, `TESTING_REQUIREMENTS: NONE`, `EXECUTION_CONTEXT_REQUIREMENTS: AUTO`.

**Status:** Complete
