# Research Notes: Markdownlint Remediation Across 9 RF Agent Files

**Date:** 2026-05-23
**Scenario:** A (Explicit BUILD_REQUEST with per-file violation breakdown)
**Depth Tier:** Standard
**Track Count:** 1
**BUILD_REQUEST:** `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reports/BUILD-REQUEST-markdownlint-remediation.md`
**Parent task (paused):** `TASK-RF-20260522-203947-tavily-agents-refactor` — Phase 5 commit blocked by pre-commit markdownlint gate.

---

## EXISTING_FILES

Nine `src/superclaude/agents/*.md` files currently in working-tree modified state (post-parent-task Phase 2 edits, pre-commit), each with documented markdownlint violation counts:

| File | Total violations | Dominant rule(s) |
|---|---|---|
| `src/superclaude/agents/deep-research.md` | 1 | MD040 (1) |
| `src/superclaude/agents/deep-research-agent.md` | 15 | MD036 (15) |
| `src/superclaude/agents/rf-task-researcher.md` | 18 | MD040 (18) |
| `src/superclaude/agents/rf-task-builder.md` | 21 | MD040 (14), MD013 (7) |
| `src/superclaude/agents/rf-task-executor.md` | 17 | MD040 (16), MD013 (1) |
| `src/superclaude/agents/rf-assembler.md` | 2 | MD040 (2) |
| `src/superclaude/agents/rf-analyst.md` | 7 | MD024 (5), MD040 (1), MD013 (1) |
| `src/superclaude/agents/rf-qa.md` | 22 | MD029 (12), MD013 (6), MD024 (3), MD040 (1) |
| `src/superclaude/agents/rf-qa-qualitative.md` | 131 | MD029 (67), MD024 (29), MD036 (24), MD013 (10), MD040 (1) |
| **Total** | **234** | — |

The full raw markdownlint output (every violation with file:line:col + rule + context excerpt) is at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reports/markdownlint-raw-output.txt`.

## PATTERNS_AND_CONVENTIONS

Five distinct markdownlint rule categories fire across these prose-heavy agent definition files:

1. **MD013 (line-length, 25 violations)** — Lines exceed the project's 160-char limit. The parent task's `.markdownlint.json` change (160 → 500) reduced these but did not eliminate them; the remediation must reflow at sentence boundaries while preserving semantic content of the Tavily-first prose added by the parent task. Note: the `.markdownlint.json` change to line_length=500 is currently uncommitted in the working tree.
2. **MD040 (fenced-code-language, 54 violations)** — Code fences ` ``` ` opened without a language tag. Remediation: classify each code block by content (`bash`, `python`, `markdown`, `yaml`, `json`, `text`) and add the language tag. Mechanical, low-risk.
3. **MD036 (no-emphasis-as-heading, 39 violations)** — `**Bold paragraph**` used where a heading (`####`) should be. Per-file judgment: convert standalone-line bold paragraphs to `####` headings where they introduce a section; leave as `**bold**` inline when the bold is mid-sentence emphasis. Concentrated in `deep-research-agent.md` (15) and `rf-qa-qualitative.md` (24).
4. **MD024 (no-duplicate-heading, 37 violations)** — Same heading text repeated (e.g. `### What You Verify` appears 3+ times under different parent contexts in `rf-qa.md` and `rf-qa-qualitative.md`). Remediation: disambiguate via parent-context suffix (`### What You Verify (Research Gate)`, `### What You Verify (Synthesis Gate)`) or restructure using `####` sub-headings under a single canonical `###`.
5. **MD029 (ol-prefix, 79 violations)** — Ordered list numbers don't restart at 1 (using sequential 16, 17, 18… instead). Remediation: renumber lists to `1./2./3.` form OR `1./1./1.` form consistently. Concentrated in `rf-qa-qualitative.md` (67) and `rf-qa.md` (12).

**File complexity profile:**

- **Trivial** (1-2 violations): `deep-research.md` (1), `rf-assembler.md` (2)
- **Small** (5-25): `rf-analyst.md` (7), `deep-research-agent.md` (15), `rf-task-researcher.md` (18), `rf-task-builder.md` (21), `rf-task-executor.md` (17), `rf-qa.md` (22)
- **Large** (>50): `rf-qa-qualitative.md` (131) — likely needs the heaviest investment of editor attention

**Parent task constraint:** the Tavily-first prose content added by the parent task is in-scope for line reflow (MD013) but the substantive content must not change — only formatting.

## GAPS_AND_QUESTIONS

- For each MD036 violation, is the bold paragraph a structural heading (convert to `####`) or genuine inline emphasis (leave as `**bold**`)? Per-file judgment required during execution. Researchers should sample 2-3 MD036 instances per heavy file (`deep-research-agent.md`, `rf-qa-qualitative.md`) and classify the pattern.
- For each MD024 duplicate heading, is the canonical disambiguation pattern "parent-context suffix" or "demote to ####"? Need to look at surrounding section structure.
- For each MD029 ol-prefix run, is the intent a single logical list (renumber 1/2/3…) or multiple sub-lists (restart at 1 for each)? Need to see structural intent.
- For each MD040 fenced code block: what's the actual content type? Most are bash/markdown/text, but specific instances need verification.
- Are there any MD013 violations that are inside code blocks (which markdownlint config sets `code_blocks: false` to skip)? Some long lines may already be exempt.

## RECOMMENDED_OUTPUTS

Two research files (lightweight — most context is already in the BUILD_REQUEST and raw lint output):

1. `01-per-file-violation-extracts.md` — For each of the 9 files, extract the verbatim violation lines from `markdownlint-raw-output.txt`, grouped by rule. Each Phase 2 item's Context field will reference this file.
2. `02-remediation-pattern-samples.md` — Read 2-3 MD036/MD024/MD029 examples from `deep-research-agent.md`, `rf-qa.md`, and `rf-qa-qualitative.md`. Classify each as "convert" vs "preserve" with reasoning. Establishes the per-rule remediation playbook the Phase 2 executor follows.

## SUGGESTED_PHASES

**Researcher assignments:**

- **Researcher 1 (File Inventory)**: Read `markdownlint-raw-output.txt`. For each of the 9 files, extract all violation lines grouped by rule. Output to `research/01-per-file-violation-extracts.md`.
- **Researcher 2 (Patterns & Conventions)**: Read `deep-research-agent.md`, `rf-qa.md`, `rf-qa-qualitative.md` directly. Sample 2-3 MD036/MD024/MD029 instances per file. Classify with rationale. Output to `research/02-remediation-pattern-samples.md`.
- **Researcher 3 (Template & Examples)**: Read `01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md`. Document MDTM features the generated task file should use (B2 self-contained items, A3 granularity, F2a parallel-spawning exception). Output to `research/03-mdtm-template-notes.md`.

**Phase structure for the task to be built:**

- **Phase 1: Preparation** — Status update, capture pre-edit lint baseline, mirror `.markdownlint.json` working-tree state, verify pre-commit invocation works.
- **Phase 2: Per-file remediation** — 9 parallel items, one per `src/superclaude/agents/*.md` file. Each item: read file, apply MD013/MD040/MD036/MD024/MD029 fixes per the remediation pattern playbook, write per-file review file confirming `pre-commit run markdownlint --files <file>` passes for that one file.
- **Phase Gate: Cross-file QA** — Spawn rf-qa adversarial to re-verify each file independently. Fix-cycle limit: 2.
- **Phase 3: Sync & Verify** — `make sync-dev`, `make verify-sync` (must both pass).
- **Phase 4: Smoke tests** — `uv run pytest` must return identical 102 failed / 7263 passed baseline as parent task established (0 NEW failures). Audit-test pin counts unchanged (14 baseline in `tests/audit/test_dnsp_all_agents_fail_bypass.py + test_dnsp_twice_exhaust.py`).
- **Phase 5: Stage & commit** — Stage ONLY 9 `src/superclaude/agents/*.md` files (NOT `.claude/agents/`). Conventional message: `style(agents): remediate 234 markdownlint violations across 9 agent files`. Pre-commit must PASS cleanly (success criterion).
- **Phase 6: Completion aggregation + parent-task handoff** — Update parent task `TASK-RF-20260522-203947-tavily-agents-refactor` notes to mark Phase 5 unblocked, ready to resume.

## TEMPLATE_NOTES

**Template selection:** Template 02 (complex task). The work requires per-file investigation (each file has unique violation profile), parallel subagent spawning (9 independent Phase 2 items), QA gates between phases, and a verification chain (per-file lint → cross-file QA → sync → smoke tests → commit).

**Tier selection:** Standard — 9 files, moderate complexity, scope is well-bounded by the BUILD_REQUEST, no codebase exploration needed beyond what's already done.

**MDTM features required:**

- **B2 self-contained items** — Each Phase 2 item embeds the file's full violation list + remediation instructions inline (no "see SKILL.md").
- **A3 granularity** — One item per file (NOT batch "fix all 9 files").
- **A4 iterative structure** — Phase 2 items are parallelizable: yes (F2a exception applies).
- **F2a parallel-spawning** — 9 Phase 2 items run as ONE parallel batch (user-stated requirement).
- **Per-item completion gate** — Each item ends with `uv run pre-commit run markdownlint --files <the_one_file>` returning 0 violations for that file.

## AMBIGUITIES_FOR_USER

None — BUILD_REQUEST is fully specified. The user has already authorized:

- Scope: 9 specific agent files (rf-team-lead held back from this remediation per parent-task decision)
- Approach: edit each file in-place using Edit tool, preserve Tavily-first content semantics
- Output: a single commit ready to land cleanly through pre-commit
- Parallelism: maximize per F2a exception (user-stated)
- Validation chain: per-file lint + adversarial rf-qa + sync + verify + pytest baseline + final pre-commit pass

The only judgment call during execution is the per-rule remediation pattern (convert MD036 vs preserve inline emphasis; renumber MD029 vs restart-at-1; disambiguate MD024 vs demote-to-####), which is handled by the remediation pattern samples in Research Output 2.

**Status:** Complete
