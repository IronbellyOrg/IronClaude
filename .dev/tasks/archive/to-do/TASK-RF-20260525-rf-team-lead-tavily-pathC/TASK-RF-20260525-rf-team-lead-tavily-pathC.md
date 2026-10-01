---
id: "TASK-RF-20260525-rf-team-lead-tavily-pathC"
title: "OQ3 Path C — rf-team-lead Tavily-first refactor with audit-pin remediation (snapshot fixture)"
description: "Apply the held-back Tavily-first refactor to src/superclaude/agents/rf-team-lead.md by first converting the audit test in tests/audit/test_dnsp_all_agents_fail_bypass.py from literal line-number pinning (lines[416], RF_TEAM_LEAD_LINE_417_SHA256 constant, rf-team-lead.md:417 cross-reference assertions) to a snapshot-fixture mechanism that pins the Fix Cycles rule by content+SHA rather than by line number. Preserves the COMP-006-M6 byte-stable preservation invariant via snapshot identity instead of brittle line-pin identity. Drops the line-shift blocker that held rf-team-lead back from commit 11795ec1."
status: "🟡 To Do"
type: "🔧 Refactor"
priority: "🔼 High"
created_date: "2026-05-25"
updated_date: "2026-05-25"
assigned_to: "rf-task-executor"
autogen: false
autogen_method: "rf-task-builder"
coordinator: orchestrator
parent_task: "TASK-RF-20260522-203947-tavily-agents-refactor"
depends_on: []
related_docs:
- path: ".dev/releases/current/TavilyAgents/rf-team-lead-tavily-refactor.md"
  description: "Refactor proposal with 11 acceptance criteria and full Before/After text"
- path: "tests/audit/test_dnsp_all_agents_fail_bypass.py"
  description: "Audit test file containing the line-417 pins to be remediated"
- path: "src/superclaude/agents/rf-team-lead.md"
  description: "Refactor target — Tavily-first frontmatter reorder + WebSearch subsection replacement + Critical Rule 11 addition"
- path: ".dev/tasks/done/TASK-RF-20260522-203947-tavily-agents-refactor/"
  description: "Sibling-completed precedent — Phase 2 review for rf-team-lead PASSED; revert was a Phase 4 audit-pin issue"
- path: "CLAUDE.md"
  description: "src/ is SoT; NEVER stage .claude/ paths; UV only; pre-commit hooks must run cleanly"
tags:
- "tavily-first"
- "rf-team-lead"
- "audit-test-refactor"
- "snapshot-fixture"
- "COMP-006-M6"
- "OQ3-path-C"
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
estimation: "Medium — 7 phases with per-phase QA gates; surgical edits to 5 files plus 1 new fixture"
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static
---

# OQ3 Path C — rf-team-lead Tavily-first refactor with audit-pin remediation

## Task Overview

This task implements OQ3 Path C — the hybrid resolution for the rf-team-lead Tavily-first refactor that was held back from commit `11795ec1` on branch `feat/agents-tavily`. The held-back refactor adds ~36 lines to `src/superclaude/agents/rf-team-lead.md` (frontmatter Tavily tools, "Web Research — Tavily-first Protocol" subsection, Critical Rule 11), shifting the existing Fix Cycles rule from line 417 to approximately line 453. Three audit-test pins in `tests/audit/test_dnsp_all_agents_fail_bypass.py` lock that rule to literal line 417: a SHA-256 constant (`RF_TEAM_LEAD_LINE_417_SHA256` per COMP-006-M6 byte-stable preservation), a `lines[416]` line-index fetch in `test_line_417_sha256_matches_pinned_value`, and cross-referencing assertions that the literal string `"rf-team-lead.md:417"` appears in wrapper sources.

Path C preserves the **spirit** of COMP-006-M6's byte-stable preservation (the Fix Cycles rule content must NOT silently mutate) while replacing the **implementation** (line-pin) with a more robust mechanism (content snapshot). A new fixture file `tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt` captures the exact bytes of the Fix Cycles rule region; the audit test compares SHA-256 of the fixture against SHA-256 of the corresponding region extracted from the live `rf-team-lead.md` by content match (not by line index). The rule's content is still locked byte-for-byte; only the location pointer becomes flexible. Cross-reference strings (`rf-team-lead.md:417`) in `rf-qa.md`, `SKILL.md`, and `rf-task-builder.md` are replaced with line-number-free equivalents (e.g., "rf-team-lead's Fix Cycles rule").

After the audit test refactor lands (Phases 2-3), the held-back Tavily-first refactor is applied to `rf-team-lead.md` (Phase 4) per the proposal at `.dev/releases/current/TavilyAgents/rf-team-lead-tavily-refactor.md` — frontmatter `tools:` reorder (Tavily tools before WebSearch/WebFetch), replace "WebSearch — Understanding Unfamiliar Technologies" with "Web Research — Tavily-first Protocol", add Critical Rule 11 (Tavily-first observability with `web_research_fallback:` output line). Phase 5 sweeps the 6 cross-reference occurrences. Phase 6 enforces the project's markdownlint policy. Phase 7 commits with all 16 pre-commit hooks running cleanly and moves the task to done/.

## Key Objectives

- Convert the audit test's line-417 pin mechanism from brittle line-index pinning to robust snapshot-content pinning, preserving the COMP-006-M6 byte-stable preservation invariant via content identity
- Apply the held-back Tavily-first refactor to `src/superclaude/agents/rf-team-lead.md` (the 10th agent that did not land in commit `11795ec1`)
- Replace all 6 occurrences of `rf-team-lead.md:417` cross-references in `rf-qa.md`, `SKILL.md`, and `rf-task-builder.md` with line-number-free references
- Maintain pytest baseline exactly: 0 NEW failures vs current 102-failed / 7263-passed / 110-skipped / 1-error baseline
- Pass all 16 pre-commit hooks cleanly with no `--no-verify` bypasses

## Prerequisites & Dependencies

- Branch off `master` (NOT off `feat/agents-tavily`) since Path C is a separate concern from the in-flight Tavily 9-agent PR
- Current `master` HEAD includes the `11795ec1` Tavily-first refactor for 9 agents; rf-team-lead is the 10th and is currently unrefactored
- All references to "line 417" in this task file refer to the **pre-refactor** line number (the current live position of the Fix Cycles rule in master). After Phase 4, the rule will live at approximately line 453 — this is expected and the new snapshot-based test mechanism MUST tolerate it.
- `make sync-dev` must be run after every src/ edit to propagate to `.claude/` (the dev-copy directory)
- `make verify-sync` must exit 0 after every sync (CI gate)
- UV is the mandatory Python runner — never `python -m`, never bare `pip`

## Execution Context

<!-- OPTIONAL header — task-level reading aid; per-item Context fields and research-notes.md remain the evidence venue with file:line citations. Block contains NO specific file:line references per NFR-CONV.3. -->

- **References:** R-001: Implement OQ3 Path C (hybrid) for the rf-team-lead Tavily-first refactor that was held back from feat/agents-tavily commit 11795ec1, by replacing brittle line-417 pins in the audit test with a snapshot-fixture mechanism that preserves the COMP-006-M6 byte-stable preservation invariant via content identity; R-002: Path C preserves the spirit of byte-stable preservation (Fix Cycles rule content must not silently mutate) while replacing the implementation (line-pin → content snapshot); R-003: refactor proposal with 11 acceptance criteria; R-004: sibling-completed parent task precedent (rf-team-lead Phase 2 review PASSED, revert was a Phase 4 audit-pin issue only)
- **Source areas:** rf-team-lead agent prompt, DNSP audit test suite, audit-fixture directory, cross-reference files (rf-qa agent prompt, task-builder skill body, rf-task-builder agent prompt), Tavily-first refactor proposal
- **Key constraints:** pytest baseline must be preserved exactly (current 102 failed / 7263 passed / 110 skipped / 1 error — 0 NEW failures permitted); pre-commit hooks must run cleanly (NO --no-verify); src/superclaude/ is SoT and NEVER stage .claude/ paths (CLAUDE.md absolute rule)

---

## Phase 1: Setup & Branch Preparation

- [ ] Verify the working directory is clean and the current branch is `master` by running `git status` and `git branch --show-current`, then create a new feature branch `fix/rf-team-lead-tavily-pathC` off `master` via `git checkout -b fix/rf-team-lead-tavily-pathC`, ensuring the branch is created from `master` (NOT from `feat/agents-tavily` — Path C is a separate concern from the in-flight Tavily 9-agent PR), no uncommitted changes carry over, and the new branch HEAD matches `master` HEAD. If the working directory is dirty, the wrong branch is checked out, or branch creation fails due to a naming collision, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Create the `phase-outputs/` directory structure for this task by running `mkdir -p .dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/{discovery,test-results,reviews,plans,reports}`, ensuring all five subdirectories exist as receptacles for downstream L1-L6 handoff artifacts (discovery findings, test outputs, QA verdicts, conditional plans, aggregation reports). If `mkdir` fails due to permissions or path issues, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Capture the pytest baseline for comparison by running `uv run pytest --tb=no -q 2>&1 | tail -20 > .dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/discovery/01-pytest-baseline.txt`, ensuring the output file contains the current PASS/FAIL/SKIP/ERROR counts (expected: 102 failed / 7263 passed / 110 skipped / 1 error or similar) which will serve as the "0 NEW failures" comparison point in Phase 7. If pytest fails to run or output capture fails, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Update the frontmatter status of this task file from `🟡 To Do` to `🟢 In Progress` and set `start_date:` to today's date `2026-05-25` using the Edit tool, ensuring the status field reflects active execution for downstream observability and the start_date is populated for time-tracking. If the Edit fails due to file conflicts or schema issues, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 1 Gate (QA: structural readiness)

- [ ] Spawn the rf-qa agent with **ADVERSARIAL STANCE** and `fix_authorization: true` to verify Phase 1 setup outputs: confirm the new branch `fix/rf-team-lead-tavily-pathC` exists and is checked out, confirm `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/{discovery,test-results,reviews,plans,reports}/` all exist, confirm `phase-outputs/discovery/01-pytest-baseline.txt` contains the captured counts, and confirm this task file's frontmatter shows `status: "🟢 In Progress"` with `start_date: "2026-05-25"`, writing the verdict to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/reviews/PG-1-rf-qa-report.md` with explicit PASS or FAIL determination. Ensure the verdict file contains either `VERDICT: PASS — proceed to Phase 2` or `VERDICT: FAIL — fix cycle required` with specific remediation guidance on FAIL. On FAIL apply the fix-cycle protocol (max 2 cycles for task-integrity gate, then Open Questions per the agent rules); on PASS proceed to Phase 2. If rf-qa spawn fails or verdict file is not produced, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

---

## Phase 2: Snapshot Fixture Creation (Pre-Refactor Baseline)

- [ ] Read the file `src/superclaude/agents/rf-team-lead.md` at `/config/workspace/IronClaude/src/superclaude/agents/rf-team-lead.md` and the audit test file `tests/audit/test_dnsp_all_agents_fail_bypass.py` at `/config/workspace/IronClaude/tests/audit/test_dnsp_all_agents_fail_bypass.py` to identify the exact byte range of the Fix Cycles rule region currently pinned to line 417 (the region whose SHA-256 is encoded in the `RF_TEAM_LEAD_LINE_417_SHA256` constant); locate the rule's start anchor (the line beginning with `**Fix cycle limits per gate type` or equivalent header from COMP-006-M6) and end anchor (the closing line of the rule region before the next major heading), then write the discovered byte range, start-anchor string, end-anchor string, and current SHA-256 to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/discovery/02-fix-cycles-rule-region.md`, ensuring the anchors are unique strings within the file (verified by grep count = 1), the byte range captures the full rule content including the table and the halt-precedence rule paragraph, and the SHA-256 matches the existing `RF_TEAM_LEAD_LINE_417_SHA256` constant value byte-for-byte. If anchor strings are not unique, the byte range is ambiguous, or SHA-256 mismatch occurs, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Create the fixtures directory `tests/audit/fixtures/` if it does not yet exist by running `mkdir -p /config/workspace/IronClaude/tests/audit/fixtures`, then extract the exact byte range identified in the previous item from `src/superclaude/agents/rf-team-lead.md` and write it verbatim to `/config/workspace/IronClaude/tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt`, ensuring the fixture file's SHA-256 matches the current `RF_TEAM_LEAD_LINE_417_SHA256` constant value byte-for-byte (this is the byte-stable baseline before the Phase 4 Tavily-first refactor — the fixture captures the protected content), the file ends with a newline only if the source region ends with one (no trailing-newline mutation), and no BOM or character-encoding transformation is introduced. If SHA-256 mismatch occurs after extraction or the fixture cannot be written, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Verify the fixture's SHA-256 matches the audit test's pinned constant by running `python3 -c "import hashlib; print(hashlib.sha256(open('/config/workspace/IronClaude/tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt','rb').read()).hexdigest())"` and `grep -E 'RF_TEAM_LEAD_LINE_417_SHA256\s*=' /config/workspace/IronClaude/tests/audit/test_dnsp_all_agents_fail_bypass.py`, writing both outputs to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/test-results/02-fixture-sha-verification.txt`, ensuring the two SHA-256 values are byte-identical (this proves the fixture captures the protected content losslessly). If SHAs do not match, the fixture is wrong and Phase 4 refactor MUST NOT proceed; log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 2 Gate (QA: fixture-baseline correctness)

- [ ] Spawn the rf-qa agent with **ADVERSARIAL STANCE** and `fix_authorization: true` to verify Phase 2 fixture creation: confirm `tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt` exists and is non-empty, confirm its SHA-256 matches the `RF_TEAM_LEAD_LINE_417_SHA256` constant in `tests/audit/test_dnsp_all_agents_fail_bypass.py` byte-for-byte, confirm the discovery notes at `phase-outputs/discovery/02-fix-cycles-rule-region.md` document unambiguous start/end anchors, and confirm the fixture content semantically corresponds to the Fix Cycles rule (header + table + halt-precedence paragraph all present), writing the verdict to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/reviews/PG-2-rf-qa-report.md` with explicit `VERDICT: PASS — proceed to Phase 3` or `VERDICT: FAIL — fix cycle required`. On FAIL apply the fix-cycle protocol (max 2 cycles for task-integrity gate, then Open Questions); on PASS proceed to Phase 3. If rf-qa spawn fails or verdict is missing, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

---

## Phase 3: Audit-Test Refactor (Line-Pin → Snapshot-Content)

- [ ] Read the file `tests/audit/test_dnsp_all_agents_fail_bypass.py` at `/config/workspace/IronClaude/tests/audit/test_dnsp_all_agents_fail_bypass.py` to locate the `RF_TEAM_LEAD_LINE_417_SHA256` constant declaration, the `test_line_417_sha256_matches_pinned_value` test function (containing the `lines[416]` line-index fetch), and any `"rf-team-lead.md:417"` cross-reference assertions, recording each occurrence's line number and surrounding context to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/discovery/03-audit-test-pin-locations.md`, ensuring all three pin mechanisms are catalogued (constant, line-index fetch, cross-ref string) and no occurrence is missed (verified by `grep -c '417' tests/audit/test_dnsp_all_agents_fail_bypass.py`). If any occurrence cannot be located or grep counts disagree with the catalogue, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Refactor `tests/audit/test_dnsp_all_agents_fail_bypass.py` to replace the `RF_TEAM_LEAD_LINE_417_SHA256` constant with a `RF_TEAM_LEAD_FIX_CYCLES_FIXTURE_PATH` constant pointing to `tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt`, replace the `test_line_417_sha256_matches_pinned_value` function with `test_fix_cycles_rule_present_and_byte_stable` that (a) loads the fixture content, (b) computes the fixture's SHA-256, (c) reads `src/superclaude/agents/rf-team-lead.md`, (d) locates the Fix Cycles rule region by **content match** using the start anchor identified in Phase 2 (NOT by line index — no `lines[N]` access), (e) extracts that region's bytes from the live file, (f) asserts the extracted region's SHA-256 equals the fixture's SHA-256, and (g) raises a clear failure message identifying the rule has mutated if SHAs differ; ensure the new test function name `test_fix_cycles_rule_present_and_byte_stable` is unique within the file, no `lines[416]` (or any literal line-index access tied to line 417) remains in the file, no `"rf-team-lead.md:417"` literal string remains in this file, and the test still asserts byte-stable preservation of the Fix Cycles rule content. If refactor introduces unrelated test changes or breaks the test's ability to detect a content mutation, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Search the codebase for any remaining `"rf-team-lead.md:417"` cross-reference strings in `src/superclaude/agents/` and `src/superclaude/skills/` by running `grep -rn 'rf-team-lead.md:417' src/superclaude/ tests/` and writing the results to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/discovery/03-cross-ref-occurrences.md`, then for each occurrence (expected: `rf-qa.md`, `SKILL.md` for task-builder skill, `rf-task-builder.md` per the BUILD_REQUEST), replace the literal `rf-team-lead.md:417` string with a line-number-free reference such as `rf-team-lead's Fix Cycles rule` or `rf-team-lead's Fix Cycles section (the table whose first row is research-gate)`, ensuring each replacement preserves semantic meaning (the reader can still locate the rule), no occurrence of `rf-team-lead.md:417` remains anywhere in `src/superclaude/` or `tests/` after the sweep (verified by post-sweep `grep -c 'rf-team-lead.md:417' src/superclaude/ tests/` returning 0), and no unrelated text is modified. If grep finds occurrences in files NOT enumerated in the BUILD_REQUEST or any replacement introduces semantic ambiguity, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Run the refactored audit test in isolation to verify it passes against the PRE-refactor `rf-team-lead.md` (the Tavily-first refactor has NOT been applied yet — the Fix Cycles rule is still at line 417) by executing `uv run pytest tests/audit/test_dnsp_all_agents_fail_bypass.py -v` and writing the output to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/test-results/03-audit-test-pre-refactor.txt`, ensuring `test_fix_cycles_rule_present_and_byte_stable` passes (proves the content-match mechanism works with the current file layout), no test in this file regresses vs the baseline (compare to `phase-outputs/discovery/01-pytest-baseline.txt`), and the test's failure message format is informative (verified by temporarily mutating the fixture, re-running, and confirming the failure message identifies the mutation — then restore the fixture). If the test fails on pre-refactor `rf-team-lead.md` or the failure message is unhelpful, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 3 Gate (QA: refactor correctness + invariant preservation)

- [ ] Spawn the rf-qa agent with **ADVERSARIAL STANCE** and `fix_authorization: true` to verify Phase 3 audit-test refactor: confirm `grep -c '417' tests/audit/test_dnsp_all_agents_fail_bypass.py` shows no literal line-417 references remain, confirm `grep -rc 'rf-team-lead.md:417' src/superclaude/ tests/` returns 0 across all files, confirm the new `test_fix_cycles_rule_present_and_byte_stable` function exists and uses content-match (not line-index) extraction, confirm the audit test still passes against pre-refactor `rf-team-lead.md` per `phase-outputs/test-results/03-audit-test-pre-refactor.txt`, and confirm the COMP-006-M6 byte-stable preservation invariant is preserved in spirit (the test will still fail if the Fix Cycles rule content mutates), writing the verdict to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/reviews/PG-3-rf-qa-report.md` with explicit `VERDICT: PASS — proceed to Phase 4` or `VERDICT: FAIL — fix cycle required`. On FAIL apply the fix-cycle protocol (max 2 cycles for task-integrity gate, then Open Questions); on PASS proceed to Phase 4. If rf-qa spawn fails or verdict is missing, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

---

## Phase 4: Tavily-First Refactor — rf-team-lead.md

- [ ] Read the refactor proposal `.dev/releases/current/TavilyAgents/rf-team-lead-tavily-refactor.md` at `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-team-lead-tavily-refactor.md` to extract the exact Before/After text for the three required edits: (1) the frontmatter `tools:` reorder (Tavily tools `mcp__tavily__tavily-search`, `mcp__tavily__tavily-extract` placed BEFORE `WebSearch`, `WebFetch`), (2) the body subsection swap (replace "WebSearch — Understanding Unfamiliar Technologies" heading and its content with "Web Research — Tavily-first Protocol" per the proposal's verbatim After text), and (3) the Critical Rule 11 addition (Tavily-first observability rule with the `web_research_fallback:` output line per the proposal), recording each edit's exact source string and target string in `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/discovery/04-rf-team-lead-edits.md`, ensuring all three edits' Before strings are unique in `rf-team-lead.md` (verified by grep count = 1) and the After strings match the proposal byte-for-byte. If the proposal cannot be read, any Before string is non-unique, or any After string is malformed, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Apply edit (1) — the frontmatter `tools:` reorder — to `src/superclaude/agents/rf-team-lead.md` using the Edit tool, replacing the existing `tools:` list with the reordered list (Tavily tools first), ensuring the new ordering places `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract` BEFORE `WebSearch` and `WebFetch` per the proposal, no tool entries are added or removed beyond what the proposal specifies, and YAML frontmatter syntax remains valid (verified by `python3 -c "import yaml; yaml.safe_load(open('src/superclaude/agents/rf-team-lead.md').read().split('---')[1])"` exiting 0). If YAML validation fails or tool entries drift from the proposal, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Apply edit (2) — the body subsection swap — to `src/superclaude/agents/rf-team-lead.md` using the Edit tool, replacing the entire "WebSearch — Understanding Unfamiliar Technologies" subsection (heading + body paragraphs + examples + any "Do NOT use" guidance) with the verbatim "Web Research — Tavily-first Protocol" content from the proposal, ensuring the new subsection heading reads exactly `## Web Research — Tavily-first Protocol` (or the proposal's exact heading level/text), the Tavily-first precedence is documented (primary tool = Tavily, fallback = WebSearch/WebFetch under specific conditions), no unrelated body content is modified, and the subsection's surrounding context (previous heading, next heading) remains untouched. If the Before string spans an ambiguous region or the After content does not match the proposal, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Apply edit (3) — the Critical Rule 11 addition — to `src/superclaude/agents/rf-team-lead.md` using the Edit tool, appending a new Critical Rule 11 to the "Critical Rules" numbered list immediately after Critical Rule 10 (or at the proposal's specified insertion point), with the rule's verbatim text from the proposal including the Tavily-first observability requirement and the `web_research_fallback:` output-line convention, ensuring the new rule is numbered `11.` (or the proposal's specified next number in sequence), the rule's text is byte-identical to the proposal's verbatim After text, no existing rules are renumbered incorrectly, and the rule introduces no conflicts with existing rules 1-10. If the numbered list's surrounding structure is non-trivial to extend or the rule text drifts from the proposal, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Run `make sync-dev` from the repository root `/config/workspace/IronClaude/` to propagate the `src/superclaude/agents/rf-team-lead.md` edits to `.claude/agents/rf-team-lead.md` (the dev-copy directory), then run `make verify-sync` to confirm src/ and .claude/ match, writing both commands' output to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/test-results/04-sync-dev-verify.txt`, ensuring `make sync-dev` exits 0, `make verify-sync` exits 0, and `.claude/agents/rf-team-lead.md`'s content matches `src/superclaude/agents/rf-team-lead.md` byte-for-byte. If either command exits non-zero or the verify-sync diff reports drift, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Run the refactored audit test against the POST-refactor `rf-team-lead.md` (where the Fix Cycles rule has shifted from line 417 to approximately line 453 due to the ~36 added lines from edits 1-3) by executing `uv run pytest tests/audit/test_dnsp_all_agents_fail_bypass.py -v` and writing the output to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/test-results/04-audit-test-post-refactor.txt`, ensuring `test_fix_cycles_rule_present_and_byte_stable` still passes (proving the content-match mechanism tolerates the line shift introduced by the Tavily-first refactor — this is the central acceptance criterion for Path C), no test in this file regresses vs the baseline, and the test correctly locates the Fix Cycles rule at its new line position via content match. If the audit test fails post-refactor, the Path C hypothesis is invalidated and the work MUST halt; log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 4 Gate (QA: refactor application + invariant survival across line shift)

- [ ] Spawn the rf-qa agent with **ADVERSARIAL STANCE** and `fix_authorization: true` to verify Phase 4 Tavily-first refactor application: confirm all three edits (frontmatter reorder, subsection swap, Critical Rule 11) are present in `src/superclaude/agents/rf-team-lead.md` and match the proposal verbatim, confirm `.claude/agents/rf-team-lead.md` matches `src/` byte-for-byte after sync, confirm the audit test passes against the post-refactor file (proving the snapshot mechanism survives the line shift), and confirm no unrelated content in `rf-team-lead.md` was modified (verified by `git diff src/superclaude/agents/rf-team-lead.md` showing only the three intended edit regions), writing the verdict to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/reviews/PG-4-rf-qa-report.md` with explicit `VERDICT: PASS — proceed to Phase 5` or `VERDICT: FAIL — fix cycle required`. On FAIL apply the fix-cycle protocol (max 2 cycles for task-integrity gate, then Open Questions); on PASS proceed to Phase 5. If rf-qa spawn fails or verdict is missing, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

---

## Phase 5: Markdownlint Compliance Sweep

- [ ] Run the project's markdownlint pre-commit hook against the modified files by executing `pre-commit run markdownlint --files src/superclaude/agents/rf-team-lead.md src/superclaude/agents/rf-qa.md src/superclaude/skills/task-builder/SKILL.md src/superclaude/agents/rf-task-builder.md` (and any additional files modified in Phase 3's cross-ref sweep per `phase-outputs/discovery/03-cross-ref-occurrences.md`) and capture the output to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/test-results/05-markdownlint-initial.txt`, ensuring the command runs and produces an exit code (0 = clean, non-zero = violations found); the parent task's child precedent confirms MD029 style=one is already configured in the repo's markdownlint config, so most violations should be MD013 (line length), MD031 (blanks around fences), or MD032 (blanks around lists). If pre-commit is not installed or the markdownlint hook is not registered, log the specific blocker using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] For each markdownlint violation reported in the initial sweep, apply a minimal surgical fix to the offending line using the Edit tool, prioritising the project's established pattern (MD029 style=one already configured, MD013 line-length use the project's existing exception markers, MD031/MD032 add the missing blank lines), ensuring each fix touches ONLY the offending line and immediate context (no reformatting of unrelated paragraphs), no Tavily-first refactor content (frontmatter, subsection, Critical Rule 11) is structurally changed by markdownlint fixes (only formatting whitespace), and each fix preserves the proposal's verbatim Tavily content byte-for-byte where possible (if a violation lands inside the verbatim Tavily content, prefer adjusting markdownlint config over rewriting the verbatim content). If a fix would require rewriting verbatim Tavily proposal text, log the conflict using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Re-run markdownlint after the surgical fixes by executing `pre-commit run markdownlint --files src/superclaude/agents/rf-team-lead.md src/superclaude/agents/rf-qa.md src/superclaude/skills/task-builder/SKILL.md src/superclaude/agents/rf-task-builder.md` and writing the output to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/test-results/05-markdownlint-final.txt`, ensuring the hook exits 0 (no remaining violations), no new files were touched outside the explicit Phase 3-4 modification set, and `make sync-dev` is re-run if any `src/superclaude/` file was edited (followed by `make verify-sync` returning 0). If markdownlint still reports violations after fixes, escalate the specific rule IDs and lines in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 5 Gate (QA: markdownlint compliance + no structural drift)

- [ ] Spawn the rf-qa agent with **ADVERSARIAL STANCE** and `fix_authorization: true` to verify Phase 5 markdownlint compliance: confirm `pre-commit run markdownlint --files <modified-list>` exits 0, confirm no Tavily-first verbatim content was mutated (compare against the proposal text), confirm `make verify-sync` returns 0 after any post-markdownlint sync, and confirm the audit test from Phase 3-4 still passes against the now-lint-clean `rf-team-lead.md` (whitespace-only changes near the Fix Cycles rule region MUST NOT affect the snapshot SHA — if they did, the rule region's content has been mutated and Phase 5 has introduced a regression), writing the verdict to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/reviews/PG-5-rf-qa-report.md` with explicit `VERDICT: PASS — proceed to Phase 6` or `VERDICT: FAIL — fix cycle required`. On FAIL apply the fix-cycle protocol (max 2 cycles for task-integrity gate, then Open Questions); on PASS proceed to Phase 6. If rf-qa spawn fails or verdict is missing, log the specific blocker using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

---

## Phase 6: Stage, Pre-Commit Pipeline, Commit

- [ ] Run a full pytest sweep to confirm 0 NEW failures versus the Phase 1 baseline by executing `uv run pytest --tb=no -q 2>&1 | tail -20 > .dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/test-results/06-pytest-final.txt`, then `diff .dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/discovery/01-pytest-baseline.txt .dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/test-results/06-pytest-final.txt > .dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/reports/06-pytest-baseline-diff.txt`, ensuring the final counts match or improve on the baseline (102 failed / 7263 passed / 110 skipped / 1 error), passed count does NOT decrease, failed count does NOT increase, and any deltas are documented in the diff report. If a regression is detected, do NOT proceed to staging; log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Identify the exact file list to stage by running `git status --short` and `git diff --name-only` and writing the candidate file list to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/discovery/06-staging-candidates.md`, ensuring the candidate list includes (a) `src/superclaude/agents/rf-team-lead.md` (Tavily-first refactor), (b) `tests/audit/test_dnsp_all_agents_fail_bypass.py` (audit-test refactor), (c) `tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt` (new snapshot fixture), (d) any cross-ref files modified in Phase 3 (likely `src/superclaude/agents/rf-qa.md`, `src/superclaude/skills/task-builder/SKILL.md`, `src/superclaude/agents/rf-task-builder.md`), and explicitly EXCLUDES any `.claude/` paths per the CLAUDE.md absolute rule (`.claude/` is sync-dev output, NOT a staging target except for `.claude/settings.json` which is unchanged here). If any `.claude/` path appears in the candidate list (other than `settings.json`), this is a violation and MUST be removed; log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Stage the candidate files by running `git add` with each file path explicitly (NEVER `git add -A` or `git add .`, NEVER `git add -f` on any `.claude/` path — both per the CLAUDE.md absolute rule), then run `git status --short` to confirm the staging matches the candidate list, writing the post-stage status to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/test-results/06-git-status-post-stage.txt`, ensuring only the intended files are staged, no `.claude/` paths are staged (other than `settings.json` if it was independently modified, which it should not be), and the staged set covers all Phase 2-5 deliverables. If any unintended file is staged or any intended file is missing from the stage, log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Run the full pre-commit pipeline against staged files by executing `pre-commit run` (no `--no-verify` bypass — all 16 hooks MUST run cleanly per the BUILD_REQUEST constraint) and writing the output to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/test-results/06-precommit-output.txt`, ensuring every hook exits 0 (including `verify-sync`, `markdownlint`, ruff, and any custom hooks), no hook is skipped, and any hook-applied auto-fixes are re-staged via `git add` of the modified files before commit. If any hook fails and the failure is NOT auto-fixable (e.g., a logic/test failure), do NOT bypass with `--no-verify` — instead fix the root cause and re-run; if the failure is irrecoverable, log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Create the commit using a single-line commit message (per the user's "no multi-line paste-ready" memory rule) by running `git commit -m "fix(rf-team-lead): Tavily-first refactor with snapshot-fixture audit-pin (OQ3 Path C)"`, ensuring the commit message is conventional-commits format (`fix(scope): summary`), the commit includes ONLY the intended staged files (verified by `git show --stat HEAD` showing the expected file list), no `Co-Authored-By` or auto-generated trailers are added unless the user has explicitly authorised them in this session, and the commit hash is captured to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/test-results/06-commit-hash.txt` via `git rev-parse HEAD`. If the commit fails (e.g., a pre-commit hook re-asserts itself), follow the "create a NEW commit, never --amend" rule from the agent base rules; log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 6 Gate (QA: clean commit + baseline preservation)

- [ ] Spawn the rf-qa agent with **ADVERSARIAL STANCE** and `fix_authorization: true` to verify Phase 6 commit integrity: confirm the commit hash exists in `git log`, confirm the commit's file list exactly matches the candidate list from `phase-outputs/discovery/06-staging-candidates.md` (no `.claude/` mirrors except possibly `settings.json`), confirm `pre-commit run --all-files` exits 0 on the committed HEAD (proving no hook was bypassed), confirm pytest baseline is preserved per `phase-outputs/reports/06-pytest-baseline-diff.txt`, and confirm the commit message follows conventional-commits format, writing the verdict to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/reviews/PG-6-rf-qa-report.md` with explicit `VERDICT: PASS — proceed to Phase 7` or `VERDICT: FAIL — fix cycle required`. On FAIL apply the fix-cycle protocol (max 2 cycles for task-integrity gate, then Open Questions); on PASS proceed to Phase 7. If rf-qa spawn fails or verdict is missing, log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

---

## Phase 7: Aggregation, Post-Completion Validation, Close-out

- [ ] Aggregate the Phase 1-6 verdicts and discovery artifacts by globbing `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/reviews/PG-*-rf-qa-report.md`, reading each PG-N verdict file, and synthesising a final acceptance-criteria matrix to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/reports/07-ac-matrix.md` that maps each of the 11 acceptance criteria from `.dev/releases/current/TavilyAgents/rf-team-lead-tavily-refactor.md` to a PASS/FAIL determination plus the supporting Phase-N evidence file, ensuring all 11 criteria are addressed, every PASS is backed by a specific artifact reference, and any FAIL or partial-pass is flagged for the Task Summary. If a PG-N verdict file is missing or the criteria mapping is incomplete, log the specific blocker using the templated format in the ### Phase 7 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Run the post-completion structural validation by spawning the rf-qa agent with **ADVERSARIAL STANCE** and `fix_authorization: true` for a final task-integrity sweep, verifying: (a) all 6 phase gates passed (PG-1 through PG-6 verdicts all PASS), (b) the acceptance-criteria matrix shows 11/11 PASS, (c) the commit at HEAD contains the expected file set with no `.claude/` mirrors, (d) `git log -1 --format='%H %s'` shows the conventional-commits message, (e) `make verify-sync` returns 0, and (f) pytest baseline is preserved per `phase-outputs/reports/06-pytest-baseline-diff.txt`, writing the verdict to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/reviews/PG-FINAL-structural.md` with explicit `VERDICT: PASS — proceed to qualitative validation` or `VERDICT: FAIL — fix cycle required`. On FAIL apply the fix-cycle protocol (max 2 cycles); on PASS proceed to the qualitative validation item. If rf-qa spawn fails or verdict is missing, log the specific blocker using the templated format in the ### Phase 7 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Run the post-completion qualitative validation by spawning the rf-qa-qualitative agent with **ADVERSARIAL STANCE** and `fix_authorization: true` to assess the OPERATIONAL quality of the Path C outcome, verifying: (a) the snapshot-fixture mechanism genuinely improves robustness over line-pin (will future line shifts in `rf-team-lead.md` no longer break the audit test?), (b) the Tavily-first refactor reads naturally in the agent prompt (the new "Web Research — Tavily-first Protocol" subsection and Critical Rule 11 integrate cleanly with the existing rule set), (c) cross-reference replacements preserve human-readability (a reader navigating to the Fix Cycles rule can still find it without the line number pointer), and (d) the commit's `fix(rf-team-lead):` scoping accurately conveys the work to a future contributor reading `git log`, writing the verdict to `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/phase-outputs/reviews/PG-FINAL-qualitative.md` with explicit `VERDICT: PASS — task complete` or `VERDICT: FAIL — fix cycle required`. On FAIL apply the qualitative-gate fix-cycle protocol (max 3 cycles, then HALT and escalate per the agent rules); on PASS proceed to the close-out item. If rf-qa-qualitative spawn fails or verdict is missing, log the specific blocker using the templated format in the ### Phase 7 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Populate the Task Summary section at the bottom of this task file with a concise narrative (3-6 sentences) covering: what was done (snapshot-fixture audit-pin remediation + Tavily-first refactor for rf-team-lead), how the COMP-006-M6 byte-stable invariant was preserved (content snapshot vs line index), the file delta (5 files modified + 1 fixture added + 1 commit), the pytest baseline result (0 NEW failures), and the next observed state (rf-team-lead is now the 10th Tavily-first-refactored agent and the line-shift blocker is dropped), ensuring the summary references the final commit hash from `phase-outputs/test-results/06-commit-hash.txt`, all 11 acceptance criteria are addressed by status, and no contradictions exist with the PG-FINAL verdicts. If a contradiction is detected between the summary and the verdicts, resolve in favour of the verdicts and log the discrepancy in the ### Phase 7 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] Close out the task by updating this file's frontmatter — set `status: "🟢 Done"`, `completion_date: "2026-05-25"` (or the actual completion date if work spans days), `updated_date: "2026-05-25"` — then move the entire task directory from `.dev/tasks/to-do/TASK-RF-20260525-rf-team-lead-tavily-pathC/` to `.dev/tasks/done/TASK-RF-20260525-rf-team-lead-tavily-pathC/` via `git mv` (preserving git history of phase-outputs/), ensuring the move preserves all phase-outputs/, the task file's frontmatter updates are committed in a separate close-out commit `chore(tasks): close TASK-RF-20260525-rf-team-lead-tavily-pathC`, and the moved task directory is verifiable at the new path via `ls .dev/tasks/done/TASK-RF-20260525-rf-team-lead-tavily-pathC/`. If `git mv` fails or the close-out commit fails any pre-commit hook, log the specific blocker using the templated format in the ### Phase 7 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

---

## Task Log / Notes

### Task Summary

<!-- Populated by Phase 7 close-out item. 3-6 sentences covering: what was done, how the COMP-006-M6 byte-stable invariant was preserved (content snapshot vs line index), file delta, pytest baseline result, next observed state. Must reference the final commit hash from phase-outputs/test-results/06-commit-hash.txt and address all 11 acceptance criteria by status. -->

_(To be populated upon Phase 7 completion.)_

### Open Questions

<!-- Populated when a per-gate fix cycle exhausts its retry ceiling (task-integrity gate: max 2 cycles; qualitative gate: max 3 cycles) or when an item logs an irrecoverable blocker. Each entry: question, context, blocking phase/item, proposed resolution path. -->

_(None at task creation. Populate if any gate exhausts its retry ceiling.)_

### Execution Log

<!-- Append-only chronological log of significant execution events: phase starts, gate verdicts (PASS/FAIL with cycle number), retries, mode transitions, commits, branch operations. Format: `YYYY-MM-DDTHH:MM:SSZ — <agent> — <event>`. -->

_(Append entries during execution.)_

### Phase 1 Findings

<!-- Templated blocker log entries for Phase 1 items. Format per blocker:
- **Item:** <item summary>
- **Blocker:** <specific issue>
- **Attempted resolution:** <what was tried>
- **Outcome:** <log-and-continue | escalated-to-Open-Questions | resolved>
-->

_(None unless a Phase 1 item logs a blocker.)_

### Phase 2 Findings

<!-- Same templated blocker log format as Phase 1. -->

_(None unless a Phase 2 item logs a blocker.)_

### Phase 3 Findings

<!-- Same templated blocker log format as Phase 1. -->

_(None unless a Phase 3 item logs a blocker.)_

### Phase 4 Findings

<!-- Same templated blocker log format as Phase 1. -->

_(None unless a Phase 4 item logs a blocker.)_

### Phase 5 Findings

<!-- Same templated blocker log format as Phase 1. -->

_(None unless a Phase 5 item logs a blocker.)_

### Phase 6 Findings

<!-- Same templated blocker log format as Phase 1. -->

_(None unless a Phase 6 item logs a blocker.)_

### Phase 7 Findings

<!-- Same templated blocker log format as Phase 1. -->

_(None unless a Phase 7 item logs a blocker.)_
