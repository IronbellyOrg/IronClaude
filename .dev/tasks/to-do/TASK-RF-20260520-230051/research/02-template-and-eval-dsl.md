# Research: MDTM Template 02 + Eval-Harness Convention

**Topic type:** Template & Examples + Solution Research
**Scope:** template 02 PART 1, prior small-fix tasks, eval-harness DSL design
**Status:** Complete
**Date:** 2026-05-20
---

## EXECUTIVE SUMMARY FOR TASK BUILDER

**Bottom line for PR #64 remediation task generation:**

1. **Template 02 is the correct choice.** PR #64 has multiple phases (per-file edits, sync, verify-sync, evals.json edit) with cross-item dependencies (later items read earlier outputs), so it needs the L1-L6 handoff patterns Template 02 provides. Template 01 would be wrong because at minimum the verify-sync step depends on the sync step's output.

2. **The assertion JSON shape MUST match the Anthropic skill-creator convention,** not the in-repo cliEval `Expect.*` primitive shape. The file being remediated is `src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json`, which already uses the skill-creator shape (`{skill_name, evals: [{id, name, prompt, expected_output, files, assertions: []}]}`) — see §3.1 below. The cliEval `Expect.*` namespace is a **different** harness (`superclaude eval run`) used for CLI integration evals, NOT skill-creator evals. Do not confuse them.

3. **The three assertion types Fix 3 needs (`file_exists`, `report_contains`, `no_hallucinated_citations`) all fit the canonical skill-creator schema** `{"text": "...", "type": "...", ...extra_fields}`. Schemas are in §4 below — paste-ready.

4. **Prior small-fix exemplar:** TASK-RF-20260517-183817 (hook-sync-and-matcher-fix release) is the closest precedent — multi-file edit + sync + verify-sync triplet + new tests, all on one branch. Cite phase structure from there. See §2.2 below.

---

## SECTION 1: MDTM TEMPLATE 02 — REQUIRED ELEMENTS

Source file (all line numbers verified):
`/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` (1198 lines total)

### 1.1 Required frontmatter fields (PART 2, lines 1-44)

The frontmatter at the top of the template IS part of the output. Required fields with their values for PR #64 remediation:

```yaml
id: "TASK-RF-20260520-230051"             # Already chosen by task-builder
title: "PR #64 remediation: M1/M2/M4 fixes for sc-auggie-review-protocol skill"
description: "<one-paragraph what+why>"
status: "🟡 To Do"
type: "🐞 Bug Fix"                         # Or "🔧 Chore" — both acceptable for remediation
priority: "🔼 High"
created_date: "2026-05-20"
updated_date: "2026-05-20"
assigned_to: "rf-task-executor"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: ""                            # No parent task for this remediation
depends_on: []                             # Or list research/qa task IDs if any
related_docs: [...]                        # MUST list research files used + the 3 target files
tags: ["skills", "evals", "sc-auggie-review-protocol", "remediation", "pr-64"]
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
start_date: ""                             # Filled by executor on Phase 1 Step 1.1
completion_date: ""                        # Filled by executor on final post-completion item
blocker_reason: ""
task_type: static                          # Use "static" — content list is known up front
```

### 1.2 Mandatory body sections (in order, lines 896-1198 of template)

PART 2 of the template, top-to-bottom, defines the **mandatory section order** the output file MUST follow:

1. **`# [Task Title]`** — exact match of frontmatter `title` (line 896)
2. **`## Task Overview`** — comprehensive description of what and why (lines 898-900)
3. **`## Key Objectives`** — numbered list of concrete outcomes (lines 902-908)
4. **`## Prerequisites & Dependencies`** containing:
   - `### Parent Task & Dependencies` — parent task ID, blocking dependencies, what this task blocks (lines 912-917)
   - `### Previous Stage Outputs (MANDATORY INPUTS)` — informational only, list of input files (lines 919-930). Marked **INFORMATIONAL ONLY — NO CHECKLIST ITEMS HERE** at line 921.
   - `### Handoff File Convention` — explains the `phase-outputs/` subdir convention (lines 932-944)
   - `### Frontmatter Update Protocol` — fixed text from template (lines 946-954)
5. **`## Detailed Task Instructions`** — preceded by orchestrator instruction block (lines 958-1011) which MUST be removed from output. Contains the actual phases:
   - `### Phase 1: Preparation and Setup` (line 1014)
     - **Step 1.1** — update task status to "🟠 Doing" (line 1045-1046, MANDATORY first item)
     - **Step 1.2** — create handoff directories (line 1048-1049, MANDATORY second item)
     - (Additional Phase 1 steps for context loading IF the task has multiple input files)
   - `### Phase 2: [Main Execution Phase Name]` (line 1062)
     - Step 2.1+ — discovery/build/test/assess per L1-L6 patterns
   - `### Phase Gate: Quality Verification` (line 1088) — REQUIRED for tasks with 2+ phases per I15 (line 599-607)
   - `### Phase [N]: Testing & Verification` (line 1096) — REQUIRED if task modifies source code per I18 (line 637-646)
   - `### Phase 3: [Review and Quality Assessment]` (line 1104)
6. **`## Post-Completion Actions`** (line 1115) containing 4 items per I17 (line 626-635):
   - Verify all output files exist via Glob (line 1117)
   - If source code was modified, run relevant test suite (line 1119)
   - Create Task Summary section in Task Log (line 1121)
   - Update frontmatter to "🟢 Done" + completion_date (line 1123)
7. **`## Task Log / Notes 📋`** (line 1125) containing:
   - `### Task Summary` (line 1127) — filled in Post-Completion Actions
   - `### Execution Log` (line 1149) — with start + complete entries pre-stubbed
   - `### Phase 1 - [Phase Name] Findings` (line 1159)
   - `### Phase 2 - [Phase Name] Findings` (line 1169)
   - `### Phase 3 - [Phase Name] Findings` (line 1178)
   - `### Phase Gate Findings` (line 1180)
   - `### Follow-Up Items Identified` (line 1184)
   - `### Deviations from Process` (line 1190)

### 1.3 Checklist item schema (B2, lines 142-198)

Every `- [ ]` checkbox MUST be ONE PARAGRAPH containing all six elements:

| # | Element | Description | Source |
|---|---------|-------------|--------|
| 1 | **Context Reference + WHY** | What file(s) to read and why that context is needed for this action | B2.1 (line 143) |
| 2 | **Action + WHY** | What to do with the context and why it needs to be done | B2.2 (line 144) |
| 3 | **Output Specification** | Exact file path, name, content requirements, template to follow | B2.3 (line 145) |
| 4 | **Integrated Verification** | "ensuring..." clause — DO NOT assume, hallucinate, or make up any information; all content MUST be derived from source files; 100% accuracy; document negative evidence on failure | B2.4 (line 146) |
| 5 | **Evidence on Failure Only** | "If unable to complete due to ..., log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete." | B2.5 (line 147) |
| 6 | **Explicit Completion Gate** | "Once done, mark this item as complete." | B2.6 (line 148) |

**Critical structural rules:**

- One paragraph only — NO multi-line bullets/headers within a single checklist item (B3 line 152-154; B5 line 175-180)
- NO nested checkboxes (E1 line 280)
- NO parent checkboxes summarising children (E2 line 296)
- Summary checkboxes come at the END of a sequence, never the beginning (E2 line 297)
- Use `**Step X.Y:**` headers (no checkbox) to group items, not parent checkboxes (E1 line 283)
- Checkboxes appear in exact execution order — flow is strictly top-to-bottom (E3 line 350)

### 1.4 Granularity rules (A3, lines 91-95)

> A3. COMPLETE GRANULAR BREAKDOWN
>
> - Break down EVERY workflow phase into atomic, verifiable checklist items
> - Create individual checklist items for EVERY file, component, or iteration
> - NO high-level or bulk operations allowed - everything must be granular
> - Include exact file paths, specific requirements, and measurable outcomes

**For PR #64 remediation specifically:** each of the three target files (`sc-auggie-review/SKILL.md`, `sc-auggie-review-protocol/SKILL.md`, `evals/evals.json`) gets its own individual checklist item for the edit. Do NOT collapse into a single "fix all three files" item.

### 1.5 Self-containment for session rollover (B1, lines 134-140)

> Rigorflow executes tasks in batches across multiple sessions. Due to session
> rollovers (context limits), any context loaded in batch 1 will NOT be available
> in batch 3+. Therefore, EVERY checklist item MUST be self-contained.

For PR #64: the literal before-text and after-text for each file MUST be embedded directly in the relevant checklist item (researcher-01 is providing these strings). The task file is the source of truth at execution time — the executor cannot rely on having read the research notes.

### 1.6 Phase-gate requirements (I15-I16, lines 599-625)

> Every task with 2+ execution phases MUST include at least one phase-gate QA checkpoint between the primary execution phase and any subsequent phase that depends on its outputs.

PR #64 remediation has multiple phases (edit files → sync → verify-sync → run pre-commit → commit). A phase-gate QA item between "edits applied" and "sync + verify" is required. The QA agent for the body-content of the SKILL.md edits is `rf-qa-qualitative` (text-content gate); for evals.json it's `rf-qa` (structural JSON gate).

Per I16 line 614: `task-integrity` gate type allows max 2 fix cycles; `Any qualitative gate` allows max 3.

### 1.7 Testing requirement for code-modifying tasks (I18, lines 637-646)

> If a task creates or modifies source code files (not documentation, not configuration), the orchestrator MUST include at least one testing checklist item.

`evals.json` is configuration, not source code. The two `SKILL.md` files are documentation, not source code. **Strictly speaking, I18 does NOT apply** — no testing phase is mandatory. However, **the task MUST still include `make verify-sync` (which acts as the structural integrity test) and `pre-commit run --files <changed-files>`** because those are project-mandated by CLAUDE.md and src/.claude sync rule. These belong in a Phase named `Verification` not `Testing`.

### 1.8 Post-completion validation (I17, lines 626-635)

> Before the frontmatter status is set to Done, the task MUST include validation items that verify:
>
> 1. All `- [ ]` items have been marked `- [x]` (no items skipped)
> 2. All output files specified in checklist items exist on disk (verified via Glob)
> 3. Any blocker entries in the Task Log have resolution notes
> 4. If the task modified source code: all relevant tests pass

These items appear in `## Post-Completion Actions` per I13 (line 580), BEFORE the frontmatter update item. Template 02 PART 2 line 1117-1123 shows the four canonical post-completion items.

---

## SECTION 2: PRIOR SMALL-FIX TASK EXAMPLES

### 2.1 Survey results

I scanned `/config/workspace/IronClaude/.dev/tasks/done/` (49 entries). The closest two matches to "3-5 file remediation flavor" are:

| Task | Files modified | Flavor | Status |
|------|----------------|--------|--------|
| `TASK-RF-20260517-183817` (hook-sync-and-matcher-fix) | 2 src files + 1 new test file + Makefile + sync output | Multi-file edit + sync + verify-sync + new tests, single coherent PR | Archived (superseded but never executed — file structure still valid as a model) |
| `TASK-RF-20260518-181333` (Hook-Sync Branch QA + 7-PR Split) | 14 modified + 124 untracked, 7 PRs | Too big — not a useful exemplar | Done |

The 7-PR-split task is too sprawling to mimic; use it only for the phase-gate pattern.

### 2.2 RECOMMENDED EXEMPLAR: TASK-RF-20260517-183817

**Full path:** `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260517-183817/TASK-RF-20260517-183817.md`

**Why it's the best precedent for PR #64 remediation:**

- Multi-file edit landing on a single branch (no PR split)
- Mix of source-code edits, sync targets, and new tests — same flavor as M1/M2/M4 fixes
- Already follows MDTM Template 02 (frontmatter `template_schema_doc` field confirms it at line 49)
- Phase structure is straightforward and reusable

**Its phase structure (verified by reading the file, lines 1-254):**

```
Phase 1: Setup and Git Baseline Snapshot
  Step 1.1: Update task status
  Step 1.2: Confirm handoff directory structure exists
  Step 1.3: Capture git baseline snapshot
  Step 1.4: Read and synthesize research inputs (one paragraph item reading 5+ research files)

Phase 2: [Pre-work fix-up] — drift remediation for failing tests
  Step 2.1: Capture failing-test state (L3 Test/Execute pattern)
  Step 2.2-2.4: Per-test repair items (one self-contained item per test)
  Step 2.5: Confirm all repaired tests pass (L6 Aggregation pattern)

Phase 3+: Main execution phases (file-by-file)
  One checklist item per file with embedded before/after text

Phase Gate: rf-qa or rf-qa-qualitative spawn item

Phase [Final]: Testing & Verification
  Run pre-commit / pytest / make verify-sync

Post-Completion Actions:
  Verify outputs exist (Glob), confirm tests pass, write Task Summary, update frontmatter

Task Log / Notes:
  Task Summary, Execution Log, Phase N Findings sections, Follow-Up Items, Deviations
```

**Key item-level structural traits to mimic:**

- Each per-file item embeds the byte-exact target text directly in the prompt (lines 199, 203, 207 show this pattern with pre-identified substring candidates inline)
- Each item ends with the canonical 4-clause tail: "ensuring ...", "If unable to complete due to ...", "log the blocker in ### Phase N Findings", "Once done, mark this item as complete."
- Step 2.x items show the pattern for retry-on-failure: "if it still fails after 2 attempts, log the blocker"
- Per-file items capture the diff for later inclusion in commit: `git diff <file> > phase-outputs/test-results/phase-2-test-diff.patch`

### 2.3 Secondary exemplar (for the QA-gate pattern only)

`/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260518-181333/TASK-RF-20260518-181333.md`

Use it for the `Phase Gate Findings` table-style logging in the Task Log section, and for the OQ-1..OQ-N "Open Questions resolved at task-creation time" pattern (lines 148-163). PR #64 has at least OQ-1 (assertion JSON shape — resolved by this research file).

---

## SECTION 3: EVAL-HARNESS LANDSCAPE — TWO DIFFERENT CONVENTIONS IN THIS REPO

### 3.1 Anthropic skill-creator convention (THE ONE PR #64 USES)

**Confirmed evidence:**

- File on disk: `/config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json` (read fully — 30 lines)
- Shape: `{"skill_name": "<name>", "evals": [{...}]}` where each eval has `id`, `name`, `prompt`, `expected_output`, `files: []`, `assertions: []`
- Identical to the canonical Anthropic skill-creator format documented at the Anthropic Skills Reference (mintlify mirror).

**Per-eval canonical fields (Anthropic public docs):**

```json
{
  "id": 1,
  "prompt": "User's task prompt",
  "expected_output": "Description of expected result",
  "files": [],
  "assertions": [
    {
      "text": "Human-readable description of what this assertion checks",
      "type": "file_exists"
    },
    {
      "text": "Another objective check",
      "type": "custom"
    }
  ]
}
```

**Public docs identify two known `type` values:** `"file_exists"` and `"custom"`. The schema is **open** — additional `type` values are permitted as long as the future harness implementer wires them up. **This is exactly the design surface PR #64 needs.**

**Relevance: HIGH**
**Sources:**

- Anthropic Skills Reference (mintlify mirror): <https://www.mintlify.com/anthropics/skills/reference/skill-creator>
- Official Anthropic skill-creator SKILL.md on GitHub: <https://github.com/anthropics/claude-plugins-official/blob/main/plugins/skill-creator/skills/skill-creator/SKILL.md>

### 3.2 In-repo cliEval `Expect.*` namespace (NOT what PR #64 uses)

**Evidence:** `/config/workspace/IronClaude/src/superclaude/cli/eval/expect.py` (722 lines) implements seven assertion primitives:

- `Expect.file(path, exists, contains, regex, equals)` — file existence + content match
- `Expect.jsonl(path, line_count, filter, assert_each, assert_any)` — JSONL row predicates
- `Expect.settings_json(path, key_path, equals, exists)` — `~/.claude/settings.json` shape
- `Expect.exit_code(equals, in_set, not_equals)` — subprocess exit code
- `Expect.stderr(contains, regex, not_contains)` — ANSI-stripped stderr predicate
- `Expect.stdout(contains, regex, not_contains)` — same for stdout
- `Expect.duration(max_sec, min_sec)` — wall-clock bound

Schema lives in `/config/workspace/IronClaude/src/superclaude/cli/eval/suites/suite.schema.json`. Manifest shape is YAML, NOT JSON, and is loaded by `superclaude eval run --suite <name>`.

**This is a completely separate harness used for CLI integration evals, not for skill-creator skill evals.** Confusing the two would land the wrong JSON shape into the wrong file.

**Do NOT use this convention for PR #64 remediation.** The PR #64 file uses skill-creator shape. If a future PR rewires the skill-creator evals to run under cliEval, that's a separate task.

### 3.3 Eval-harness existence summary (for builder)

| Question | Answer |
|----------|--------|
| Does any eval-runner code currently read `evals.json` and execute the assertions? | **NO.** Search of `src/` and `scripts/` shows no harness consumes the skill-creator-shape `evals.json`. The file is currently only a manifest — its assertions are not enforced by an automated runner in this repo. |
| Is there a runner for cliEval `Expect.*`? | **YES** — `superclaude eval run` (full implementation in `src/superclaude/cli/eval/`) but it consumes the YAML cliEval manifest, NOT skill-creator JSON evals. |
| Are the Fix 3 assertions therefore "wired up" by the task? | **NO.** Fix 3 only POPULATES the assertions array with the right JSON shape so a future harness implementer (or an Anthropic skill-creator harness running externally) has the discriminated-union ready. |

**Implication for the builder:** the task should clearly state in Phase 2 prose (or in the OQ table) that the Fix 3 assertion entries are "harness-ready" but not currently runtime-enforced. This sets correct executor and reviewer expectations.

---

## SECTION 4: PROPOSED ASSERTION DSL — DISCRIMINATED UNION BY `type`

### 4.1 Design rationale (one paragraph for the OQ table)

The Anthropic public docs leave the `assertions[]` schema open beyond two named types (`file_exists`, `custom`). Fix 3 in PR #64 specifies three assertion behaviors we need: (a) presence of an output file; (b) presence of named markers in a report; (c) absence of hallucinated file:line citations. Two of the three (file_exists and report-markers) are conceptually close to the Anthropic-published `file_exists` type. The third is novel but maps cleanly onto a regex-scan-and-invert pattern. We adopt a **discriminated-union shape keyed on `type`** — every assertion is `{"text": <human-readable>, "type": <enum>, ...type-specific-fields}`. The `text` field is preserved from the Anthropic schema so external skill-creator tooling can render the assertion in benchmarks. The `type`-specific fields below are the minimum needed for a future runner to execute the assertion without re-reading prose.

### 4.2 SCHEMA #1 — `file_exists`

**Purpose:** assert a single output file exists after the eval prompt completes.

**Aligns with:** Anthropic-published `file_exists` type (canonical).

**JSON schema (paste-ready into evals.json):**

```json
{
  "text": "Output file <PATH> exists after the eval completes",
  "type": "file_exists",
  "path": "/tmp/eval-pr62/REVIEW.md"
}
```

**Required fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | yes | Human-readable assertion description (Anthropic-canonical) |
| `type` | string literal `"file_exists"` | yes | Discriminator |
| `path` | string | yes | Absolute path OR eval-output-dir-relative path (e.g. `"REVIEW.md"` resolves under whatever `--output-dir` the prompt used). If the value starts with `/`, treat as absolute; otherwise relative-to-eval-output-dir. |

**Optional fields (for future extensibility, not in Fix 3):**
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `min_size_bytes` | int | `1` | Refuse to PASS on zero-byte file |
| `must_be_readable` | bool | `true` | Refuse to PASS on permission-denied file |

**Example placement in the three current evals:**

```json
"assertions": [
  {
    "text": "Output file /tmp/eval-pr62/REVIEW.md exists after the eval completes",
    "type": "file_exists",
    "path": "/tmp/eval-pr62/REVIEW.md"
  }
]
```

### 4.3 SCHEMA #2 — `report_contains`

**Purpose:** assert the generated report file contains a set of expected markers (section headers, severity labels, template artifacts).

**Aligns with:** extends Anthropic-published `file_exists` with content checks. Conceptually similar to cliEval's `Expect.file(contains=...)` primitive but expressed in skill-creator-flavored JSON.

**JSON schema (paste-ready):**

```json
{
  "text": "REVIEW.md contains all required severity-tagged section headers and a finding-count summary line",
  "type": "report_contains",
  "report": "/tmp/eval-pr62/REVIEW.md",
  "markers": [
    "## Critical Findings",
    "## High Findings",
    "## Medium Findings",
    "## Low Findings",
    "## Summary"
  ]
}
```

**Required fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | yes | Human-readable assertion description |
| `type` | string literal `"report_contains"` | yes | Discriminator |
| `report` | string | yes | Path to the report file (resolution rules same as `file_exists.path`) |
| `markers` | array of strings | yes | List of literal substrings that MUST all appear in the report. Empty list is a configuration error — at least one marker required. |

**Optional fields:**
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `case_sensitive` | bool | `true` | Whether substring match is case-sensitive |
| `markers_mode` | string `"all"` or `"any"` | `"all"` | Whether all markers must be present (default) or at least one |

**Note on AND-vs-OR semantics:** the default is "all markers must be present" because that's what most report-template adherence checks need. If a runner wants OR semantics it sets `markers_mode: "any"`.

### 4.4 SCHEMA #3 — `no_hallucinated_citations`

**Purpose:** assert every `file:line` citation in the report points to a file that actually exists in the working tree (and optionally that the line number is within the file's line count). This catches the most common skill failure mode for code-review skills.

**Aligns with:** no canonical Anthropic equivalent (this is a novel type proposed by this research). Conceptually similar to a custom validation step a human reviewer performs manually.

**JSON schema (paste-ready):**

```json
{
  "text": "All file:line citations in the report point to files that exist in the working tree, with no hallucinated paths",
  "type": "no_hallucinated_citations",
  "report": "/tmp/eval-pr62/REVIEW.md",
  "citation_regex": "(?<![A-Za-z0-9_/])([A-Za-z0-9_./-]+\\.(?:py|md|json|yaml|yml|sh|ts|tsx|js))(?::(\\d+))?",
  "repo_root": "/config/workspace/IronClaude"
}
```

**Required fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | yes | Human-readable assertion description |
| `type` | string literal `"no_hallucinated_citations"` | yes | Discriminator |
| `report` | string | yes | Path to the report file (same resolution rules as above) |
| `citation_regex` | string | yes | Python `re`-flavored regex that captures file paths (group 1) and optionally line numbers (group 2). Default value above is suitable for most code-review report formats; eval authors override when they need a stricter or looser pattern. The regex MUST have at least one capture group; the FIRST capture group is the file path. |

**Optional fields:**
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `repo_root` | string | `"."` | Directory against which captured relative paths are resolved. Absolute paths in the citation are used verbatim. |
| `allow_external_paths` | bool | `false` | When `true`, paths starting with `/` that exist outside `repo_root` are accepted; when `false` (default), only paths under `repo_root` are valid. |
| `verify_line_in_range` | bool | `false` | When `true` AND group 2 captured a number, verify `1 <= line <= line_count(file)`. When `false` (default), only file existence is checked. |
| `ignore_patterns` | array of strings | `[]` | List of regex patterns; citations matching any pattern are skipped (e.g. `["^vendor/", "^\\.venv/"]`). |

**Failure mode:** the assertion FAILS when ANY captured citation maps to a non-existent file (or, with `verify_line_in_range`, an out-of-range line). The failure message MUST include the list of hallucinated citations (path + line + report-line-number where it appeared) so the eval author can fix the report-generation prompt.

**Why this is the right design for the third type:** the existing sc-auggie-review evals (all three) include in their `expected_output` field the phrase "no hallucinated paths" — which is exactly what this assertion type encodes. Today that phrase is a soft expectation only an LLM grader could enforce; encoding it as a discriminated-union assertion type lets a deterministic future runner enforce it.

### 4.5 Combined: the three assertions a typical PR-review eval needs

```json
"assertions": [
  {
    "text": "Output file /tmp/eval-pr62/REVIEW.md exists after the eval completes",
    "type": "file_exists",
    "path": "/tmp/eval-pr62/REVIEW.md"
  },
  {
    "text": "REVIEW.md contains all required severity-tagged section headers",
    "type": "report_contains",
    "report": "/tmp/eval-pr62/REVIEW.md",
    "markers": [
      "## Critical Findings",
      "## High Findings",
      "## Medium Findings",
      "## Low Findings",
      "## Summary"
    ]
  },
  {
    "text": "All file:line citations in REVIEW.md point to files that exist in the IronClaude working tree",
    "type": "no_hallucinated_citations",
    "report": "/tmp/eval-pr62/REVIEW.md",
    "citation_regex": "(?<![A-Za-z0-9_/])([A-Za-z0-9_./-]+\\.(?:py|md|json|yaml|yml|sh|ts|tsx|js))(?::(\\d+))?",
    "repo_root": "/config/workspace/IronClaude"
  }
]
```

This entire block is what the builder embeds (verbatim, possibly with per-eval path adjustments) into the Phase 2 checklist item that edits `evals.json`.

### 4.6 Open question for the OQ table

The builder SHOULD include the following Open Question in the task file's OQ table (resolved at task-creation time per the precedent in TASK-RF-20260518-181333):

> **OQ-1: Which assertion JSON shape should populate the `assertions: []` arrays in `src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json`?**
> **RESOLVED** — Use the discriminated-union shape `{"text": "...", "type": "<file_exists|report_contains|no_hallucinated_citations>", ...type-specific-fields}` documented in research file `02-template-and-eval-dsl.md` §4. The shape extends the canonical Anthropic skill-creator schema (which publishes only `file_exists` and `custom` types) with two additional types — `report_contains` and `no_hallucinated_citations` — chosen to encode the existing `expected_output` prose checks deterministically. No runtime harness consumes these fields today; they are populated harness-ready for future enforcement.

---

## SECTION 5: BUILDER QUICK-REFERENCE CHECKLIST

When the builder constructs the task file for PR #64 remediation, it MUST:

- Use template 02 PART 2 verbatim, then customise. PART 1 is instructions and must be deleted from the output entirely.
- Pre-create the phase-outputs subdirs at `.dev/tasks/to-do/TASK-RF-20260520-230051/phase-outputs/{discovery,test-results,reviews,plans,reports}` BEFORE writing the task file (so Phase 1 Step 1.2 just verifies they exist).
- Put the assertion JSON blocks (§4.2-§4.5) byte-exact into the Phase 2 checklist item that edits `evals.json`. The executor must not have to reconstruct them from prose.
- Mimic TASK-RF-20260517-183817 phase ordering: setup → optional drift-fix → per-file edits (one item per file) → sync (`make sync-dev`) → verify (`make verify-sync` + `pre-commit run --files <files>`) → phase-gate QA → post-completion.
- Include the OQ-1 from §4.6 in the task file's Open Questions table.
- Embed the file:line evidence inline in each per-file checklist item (researcher-01 is supplying the byte-exact strings). Do NOT defer to "read the research file" — that violates B1 self-containment.
- Use exactly the I15-I16 phase-gate pattern between the edit phase and the verify phase. Spawn `rf-qa-qualitative` for the SKILL.md text edits (qualitative gate, max 3 cycles) and `rf-qa` for the evals.json shape (task-integrity gate, max 2 cycles).
- DO NOT add a "Phase: Testing" section — I18 doesn't apply (docs/config edits only). The verification done by `make verify-sync` + `pre-commit` + (manual eyeball) is sufficient. Name the phase `Verification & Sync` instead of `Testing & Verification`.

---

## SECTION 6: SOURCES & RELEVANCE RATINGS

| Source | URL / Path | Relevance | Notes |
|--------|------------|-----------|-------|
| MDTM Template 02 PART 1+PART 2 | `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` | HIGH | Read in full (1198 lines). Authoritative for all template-required structure. |
| Anthropic Skills Reference — skill-creator | <https://www.mintlify.com/anthropics/skills/reference/skill-creator> | HIGH | Source of canonical `evals.json` schema and the two published `type` values. |
| Anthropic claude-plugins-official skill-creator | <https://github.com/anthropics/claude-plugins-official/blob/main/plugins/skill-creator/skills/skill-creator/SKILL.md> | HIGH | Pointer to the full schema, validates §3.1 shape. |
| Anthropic Skills bundled-resources docs | <https://www.mintlify.com/anthropics/skills/creating-skills/bundled-resources> | MEDIUM | Mentions `references/schemas.md` for full evals.json schema (not directly readable without auth). |
| In-repo cliEval suite schema | `/config/workspace/IronClaude/src/superclaude/cli/eval/suites/suite.schema.json` | MEDIUM | Confirms cliEval is a SEPARATE harness from skill-creator evals — important to keep them disambiguated for the builder. |
| In-repo cliEval `Expect.*` source | `/config/workspace/IronClaude/src/superclaude/cli/eval/expect.py` | MEDIUM | Reference shape for what a deterministic Python runner can do; NOT the convention PR #64 uses. |
| Current evals.json under remediation | `/config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json` | HIGH | The file Fix 3 edits. Confirms skill-creator shape with empty `assertions: []` arrays — exactly what Fix 3 populates. |
| TASK-RF-20260517-183817 task file | `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260517-183817/TASK-RF-20260517-183817.md` | HIGH | Best prior small-fix-task exemplar to mimic. Same Template 02 lineage, same multi-file + sync + verify-sync flavor. |
| TASK-RF-20260518-181333 task file | `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260518-181333/TASK-RF-20260518-181333.md` | LOW-MEDIUM | Useful for OQ-table pattern and phase-gate findings format; otherwise too large to mimic. |
