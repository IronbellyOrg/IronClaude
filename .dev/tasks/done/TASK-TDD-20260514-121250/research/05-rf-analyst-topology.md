# Research: rf-analyst Agent Topology

**Status:** Complete
**Date:** 2026-05-14
**Agent type:** Code Tracer
**Source:** src/superclaude/agents/rf-analyst.md (349 lines)

---

## 1. Partition Protocol (lines 1-60)

Front matter declares the agent (`src/superclaude/agents/rf-analyst.md:1-26`):

```
name: rf-analyst
description: "Rigorflow Analyst - Performs data extraction, cross-validation, and synthesis across research and output files. Used for completeness verification, synthesis quality review, gap analysis, and coverage audits. Supports parallel partitioning — multiple analyst instances can each handle a subset of files to prevent context rot. Each spawn handles one specific analysis task."
memory: project
permissionMode: bypassPermissions
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
  - NotebookEdit
  - Task
  - TaskOutput
  - TaskStop
  - SendMessage
  - TaskCreate
  - TaskGet
  - TaskUpdate
  - TaskList
  - Skill
  - AskUserQuestion
```

**Spawn-prompt contract (rf-analyst.md:32-39):**

> Your spawn prompt will contain:
> - **Which analysis type:** completeness-verification, cross-validation, synthesis-review, gap-analysis, or coverage-audit
> - **Research directory path** and **topic context**
> - **Specific files to analyze** (or "all files in directory")
> - **Output file path** for your analysis report
> - **Team name** for SendMessage (if running in a team context)

**Parallel Partitioning mechanism (rf-analyst.md:41-69) — verbatim:**

> ## Parallel Partitioning
>
> When the workload is large (many files to analyze), the orchestrator can spawn **multiple rf-analyst instances in parallel**, each assigned a different subset of files. This prevents context rot — no single analyst needs to hold all files in context simultaneously.
>
> ### How It Works
>
> Your spawn prompt may include an **assigned files** list. If present, you analyze ONLY those files (not all files in the directory). If no assigned files list is present, you analyze ALL files in scope.
>
> **Prompt field:** `assigned_files: [list of specific file paths]`
>
> ### When You Are a Partition Instance
>
> 1. Analyze ONLY the files in your `assigned_files` list
> 2. Apply the same checklist rigor to your subset as you would to the full set
> 3. For checks that require cross-file analysis (contradictions, cross-references, coverage audit against scope), apply them only within your assigned subset and note in your report: `[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports.]`
> 4. Your report title should include: `(Partition [N] of [M])`
> 5. The orchestrator merges all partition reports after all instances complete
>
> ### When You Are a Single Instance (Default)
>
> If no `assigned_files` field is present, you are the sole analyst. Analyze ALL files in scope as described in each analysis type below. This is the default behavior.
>
> ### Orchestrator Responsibilities (Not Your Job)
>
> The orchestrator (skill session or team lead) is responsible for:
> - Deciding when to partition (based on file count — typically >6 files warrants partitioning)
> - Dividing files into balanced subsets
> - Spawning multiple rf-analyst instances in parallel, each with its `assigned_files` list
> - Merging partition reports after all instances complete (union of findings, take the more severe rating for shared items, merge gap compilations with deduplication)

**Key extraction:**

| Behavior axis | Single instance (default) | Partition instance |
|---|---|---|
| File scope | ALL files in directory (Glob discovery) | Only `assigned_files` list |
| Cross-file checks | Full scope | Limited to subset; must emit `[PARTITION NOTE: ...]` marker |
| Report title | Standard | Must include `(Partition [N] of [M])` |
| Merge | N/A | Orchestrator unions findings; severer rating wins on shared items; gaps deduplicated |

**Partition threshold:** `>6 files warrants partitioning` (`rf-analyst.md:66`). Orchestrator decides; partition instance does not self-partition.

---

## 2. Completeness Verification analysis_type (lines 70-186)

This is the Phase 3 quality gate that rf-analyst partitions will run over the 16 codebase research files.

**Purpose & I/O (rf-analyst.md:84-89):**

> **Purpose:** Quality gate between research (Phase 2) and web research/synthesis (Phase 4/5). Ensures research agents produced thorough, evidence-based findings before downstream work begins.
>
> **Input:** ALL research files in `${TASK_DIR}research/` (files matching `[NN]-*.md`)
> **Output:** Completeness verification report at specified path

### Checklist — verbatim 8 items (rf-analyst.md:91-129)

> ### Checklist (8 items)
>
> 1. **Coverage audit** — Does every key source file identified in the scope discovery appear in at least one research file?
>    - Read the research-notes.md EXISTING_FILES section
>    - Cross-reference against all research file findings
>    - If a key file/directory was listed in scope but no agent investigated it, FLAG as a gap
>
> 2. **Evidence quality check** — Does every finding cite specific file paths, line numbers, function names, or class names?
>    - Scan each research file for claims without evidence
>    - Vague descriptions like "the system uses X architecture" without file paths = FLAG
>    - Count ratio: evidenced claims vs unsupported claims per file
>
> 3. **Documentation staleness check** — Are all doc-sourced claims tagged with verification status?
>    - Scan for claims sourced from documentation files (docs/, README, etc.)
>    - Every doc-sourced architectural claim MUST have: `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]`
>    - Any doc-sourced claim without a tag = FLAG (research agent failed to cross-validate)
>    - Any `[CODE-CONTRADICTED]` claim reported as current fact = CRITICAL FLAG
>
> 4. **Completeness check** — Does every research file have Status: Complete with a Summary section?
>    - Files with Status: In Progress = FLAG (agent didn't finish)
>    - Files without a Gaps and Questions section = FLAG (agent didn't assess gaps)
>    - Files without Key Takeaways = FLAG (agent didn't synthesize)
>
> 5. **Cross-reference check** — When one agent's findings reference another agent's domain, is the cross-reference noted?
>    - Look for cross-cutting concerns mentioned in multiple files
>    - If Agent A mentions a dependency that Agent B should have documented, verify Agent B covered it
>
> 6. **Contradiction detection** — Do any research files contradict each other?
>    - Compare findings about the same files, classes, or data flows across agents
>    - If two agents describe the same component differently, FLAG with both versions
>
> 7. **Gap compilation** — Compile all gaps from all agents into a unified gaps list
>    - Read every "Gaps and Questions" section
>    - Deduplicate and categorize: Critical (blocks synthesis), Important (affects quality), Minor (lower priority but must still be fixed)
>
> 8. **Depth assessment** — Is the investigation deep enough for the stated depth tier?
>    - For Deep tier: expect data flow traces, integration point mapping, pattern analysis
>    - For Standard tier: expect file-level understanding with key function documentation
>    - For Quick tier: expect focused answers to specific questions

### Output format for Completeness Verification (rf-analyst.md:131-185)

> ```markdown
> # Research Completeness Verification
>
> **Topic:** [topic]
> **Date:** [today]
> **Files analyzed:** [count]
> **Depth tier:** [Quick/Standard/Deep]
>
> ---
>
> ## Verdict: [PASS / FAIL — with gap count]
>
> ## Coverage Audit
> | Scope Item | Covered By | Status |
> |-----------|-----------|--------|
> | [file/directory from scope] | [research file that covered it] | COVERED / GAP |
>
> ## Evidence Quality
> | Research File | Evidenced Claims | Unsupported Claims | Quality Rating |
> |--------------|-----------------|-------------------|---------------|
> | [filename] | [count] | [count] | Strong / Adequate / Weak |
>
> ## Documentation Staleness
> | Claim | Source Doc | Verification Tag | Status |
> |-------|----------|-----------------|--------|
> | [claim] | [doc path] | [tag or MISSING] | OK / FLAG |
>
> ## Completeness
> | Research File | Status | Summary | Gaps Section | Key Takeaways | Rating |
> |--------------|--------|---------|-------------|---------------|--------|
> | [filename] | [status] | [Y/N] | [Y/N] | [Y/N] | Complete / Incomplete |
>
> ## Contradictions Found
> - [description of contradiction, citing both files]
>
> ## Compiled Gaps
> ### Critical Gaps (block synthesis)
> - [gap description — source file — why critical]
>
> ### Important Gaps (affect quality)
> - [gap description — source file]
>
> ### Minor Gaps (must still be fixed)
> - [gap description — source file]
>
> ## Depth Assessment
> **Expected depth:** [tier]
> **Actual depth achieved:** [assessment]
> **Missing depth elements:** [list or "None"]
>
> ## Recommendations
> - [specific actions to address gaps before proceeding]
> ```

**Stale-doc note:** The Investigation Focus prompt described items 1-60 as front-matter + intro + partition protocol; the actual partition protocol runs **lines 41-69**. Lines 60-69 specifically are the boundary between "single-instance default" (60-62) and "orchestrator responsibilities" (63-69). The prompt's "70-180" range for the completeness checklist is approximate; the checklist proper runs `rf-analyst.md:91-129`, and the bundled output format extends to `rf-analyst.md:185`. [STALE-PROMPT-RANGE]

---

## 3. Synthesis Quality Review analysis_type (lines 218-281)

This is the Phase 5 quality gate that rf-analyst runs over the 10 synthesis files.

**Purpose & I/O (rf-analyst.md:218-223):**

> **Purpose:** Verify synthesis files meet quality standards before final report assembly. This is the quality gate between synthesis (Phase 5) and assembly (Phase 6).
>
> **Input:** ALL synthesis files in `${TASK_DIR}synthesis/` (files matching `synth-*.md`)
> **Output:** Synthesis quality review report

### CRITICAL FINDING: Checklist is 10 items, not 9

The Investigation Focus prompt describes a "9-item Synthesis Quality Review checklist". The actual source file header at `rf-analyst.md:225` says **"### Checklist (10 items — from SKILL.md Synthesis Quality Review Checklist)"** and the body lists 10 numbered items (`rf-analyst.md:227-236`). [STALE-PROMPT-COUNT — fix: TDD authors should treat this as a 10-item checklist; the "9-item" figure in the spawn prompt is stale.]

### Checklist — verbatim 10 items (rf-analyst.md:225-236)

> ### Checklist (10 items — from SKILL.md Synthesis Quality Review Checklist)
>
> 1. Report section headers match the expected format from the Report Structure template
> 2. Tables use the correct column structure (Gap/Current/Target/Severity, Criterion/OptionA/OptionB, Step/Action/Files/Details)
> 3. No content was fabricated beyond what research files contain
> 4. Findings cite actual file paths and evidence (not vague descriptions)
> 5. Options analysis includes at least 2 options with pros/cons assessment tables
> 6. Implementation plan has specific steps with file paths (not generic actions like "create a service")
> 7. All cross-references between sections are consistent (e.g., gaps in Section 4 are addressed in Section 8)
> 8. **No doc-only claims in Current State or Implementation Plan.** Verify that Sections 2 and 8 only contain architecture descriptions backed by code-traced evidence
> 9. **Stale documentation discrepancies are surfaced.** Any `[CODE-CONTRADICTED]` or `[STALE DOC]` findings from research files should appear in the Gap Analysis (Section 4) or Open Questions (Section 9)
> 10. **Key finding coverage.** Each research file's Summary/Key Takeaway section contains findings that should be reflected in the synthesis. Verify that the strongest findings from source research are represented in synthesis conclusions/recommendations. Flag any research Key Takeaway that has no corresponding synthesis content.

### Process & Output format (rf-analyst.md:238-281)

> ### Process
>
> For each synthesis file:
> 1. Read the synthesis file completely
> 2. For each check, evaluate and document pass/fail with evidence
> 3. If a check fails, document the specific issue and the fix needed
> 4. Produce a per-file verdict and an overall verdict

Output template:

> ```markdown
> # Synthesis Quality Review
>
> **Date:** [today]
> **Files reviewed:** [count]
>
> ## Overall Verdict: [PASS / FAIL — with issue count]
>
> ## Per-File Review
>
> ### [synth-filename]
> **Sections covered:** [list]
> **Verdict:** PASS / FAIL
>
> | Check # | Check | Result | Evidence/Issue |
> |---------|-------|--------|---------------|
> | 1 | Section headers match template | PASS/FAIL | [detail] |
> | 2 | Table column structure correct | PASS/FAIL | [detail] |
> | ... | ... | ... | ... |
>
> ### [next synth file...]
> [same structure]
>
> ## Issues Requiring Fixes
> | # | File | Check | Issue | Required Fix |
> |---|------|-------|-------|-------------|
> | 1 | [file] | [check #] | [what's wrong] | [what to do] |
>
> ## Summary
> - Files passed: [count]
> - Files failed: [count]
> - Total issues: [count]
> - Critical issues (block assembly): [count]
> ```

---

## 4. Escalation Ladder Behavior on Partition Exhaust (lines 60-69)

The Investigation Focus calls out "60-69 (DNSP emission edit site — FR-CONV.6)" and "Escalation Ladder Behavior on Partition Exhaust". Reading the file directly: **lines 60-69 currently contain NO DNSP-emission contract and NO escalation language.** They cover only the single-instance default and the orchestrator's responsibilities. Verbatim (`rf-analyst.md:60-69`):

> ### When You Are a Single Instance (Default)
>
> If no `assigned_files` field is present, you are the sole analyst. Analyze ALL files in scope as described in each analysis type below. This is the default behavior.
>
> ### Orchestrator Responsibilities (Not Your Job)
>
> The orchestrator (skill session or team lead) is responsible for:
> - Deciding when to partition (based on file count — typically >6 files warrants partitioning)
> - Dividing files into balanced subsets
> - Spawning multiple rf-analyst instances in parallel, each with its `assigned_files` list
> - Merging partition reports after all instances complete (union of findings, take the more severe rating for shared items, merge gap compilations with deduplication)

**Implication for FR-CONV.6 (Did-Not-Synthesize-Properly emission):** This contract is NOT yet implemented in `rf-analyst.md`. The current text describes happy-path merge only ("union of findings, take the more severe rating, deduplicate gaps") — there is no per-partition exhaust signal, no synthetic-DNSP emission, and no ALL-agents-fail guard. The TDD must therefore add a NEW edit site here. Recommended insertion point: between `rf-analyst.md:68` (last merge bullet) and `rf-analyst.md:71` (the `---` separator) — a new sub-section titled `### Partition Exhaust / Did-Not-Synthesize-Properly (DNSP) Emission` describing:

- The per-partition exhaust signal a rf-analyst instance must emit when its own scan cannot complete (token cap, file unreadable, schema-invalid scope).
- The output channel for that signal (likely a SendMessage `type: "dnsp"` or a sentinel block in the output file).
- The orchestrator-side aggregation: if SOME partitions emit DNSP, merge survivors and surface DNSP claims to rf-team-lead; if **ALL** partitions emit DNSP, the ALL-agents-fail guard at `src/superclaude/agents/rf-team-lead.md:~414` (the escalation instructions) is the next handler instead of attempting a fallback synthesis. [VERIFY-PENDING — `rf-team-lead.md` line ~414 was not opened in this scan; the TDD author should cross-check the precise line.]

**Cross-validation responsibility split (current state, rf-analyst.md vs. rf-qa):** rf-analyst is INDEPENDENT analytical verification — its 8-item Completeness Verification checklist and 10-item Synthesis Quality Review checklist focus on completeness/coverage/depth and synthesis fidelity. rf-qa (per the parallel research file `03-rf-qa-topology.md`) is INDEPENDENT QA verification — its 10-item research-gate and synthesis-gate checklists are framed as QA acceptance criteria. NFR-CONV.10 (parallel-cross-check) mandates that **both run IN PARALLEL on the same artifacts**, and the orchestrator (rf-team-lead) reconciles their findings. The two roles are complementary: rf-analyst surfaces gaps/contradictions (analytical), rf-qa enforces structural/process compliance (gate). Disagreements between the two are a deliberate signal, not a bug.

---

## 5. Cross-validation responsibility relative to rf-qa

| Axis | rf-analyst | rf-qa |
|---|---|---|
| Stance | Independent analytical verification | Independent QA verification |
| Phase 3 checklist | 8 items (Research Completeness Verification) — `rf-analyst.md:91-129` | 10 items (research-gate) — see `03-rf-qa-topology.md` |
| Phase 5 checklist | 10 items (Synthesis Quality Review) — `rf-analyst.md:225-236` | 10 items (synthesis-gate) — see `03-rf-qa-topology.md` |
| Adversarial framing | "find problems, not rubber-stamp" (`rf-analyst.md:343`) | QA gate (PASS/FAIL acceptance) |
| Parallel execution | Required by NFR-CONV.10 | Required by NFR-CONV.10 |
| Conflict reconciliation | Orchestrator (rf-team-lead) merges; severer rating wins on shared items (`rf-analyst.md:69`) | Same orchestrator |

Both pipelines emit reports that flow into the orchestrator for reconciliation; neither can suppress the other. The TDD should preserve this dual-track independence and explicitly forbid serial chaining (rf-qa → rf-analyst or vice versa).

---

## 6. Output Format

The agent has **two output formats**, one per analysis type. Both are reproduced verbatim above:

- **Completeness Verification report:** `rf-analyst.md:131-185`. Sections: Topic/Date/Files-analyzed/Depth-tier header; Verdict line; Coverage Audit table; Evidence Quality table; Documentation Staleness table; Completeness table; Contradictions Found bullets; Compiled Gaps (Critical/Important/Minor); Depth Assessment block; Recommendations bullets.
- **Synthesis Quality Review report:** `rf-analyst.md:248-281`. Sections: Date/Files-reviewed header; Overall Verdict line; Per-File Review blocks (one per synthesis file, each with section list, verdict, per-check table); Issues Requiring Fixes table; Summary counters.

A third minor format exists for **Cross-Validation** (`rf-analyst.md:206-214`):

> ```markdown
> # Cross-Validation Report
>
> **Date:** [today]
> **Claims verified:** [count]
>
> | # | Claim | Source | Code Path Checked | Verdict | Notes |
> |---|-------|--------|-------------------|---------|-------|
> | 1 | [claim] | [research file] | [code path:line] | VERIFIED / CONTRADICTED / UNVERIFIED | [what code actually shows] |
> ```

**Completion protocol (rf-analyst.md:325-338):**

> ## Completion Protocol
>
> After writing your output file:
>
> 1. Verify the file exists and has substantial content (Read it back)
> 2. If running in a team context, send completion message:
>    ```
>    SendMessage:
>      type: "message"
>      recipient: "team-lead"
>      content: "Analysis complete: [type]. Verdict: [PASS/FAIL]. [Brief summary — e.g., '8 research files analyzed, 3 gaps found (1 critical), 2 doc claims unverified']. Report written to [path]."
>      summary: "[Type] analysis complete"
>    ```
> 3. If running as a subagent (no team context), return the report path and verdict as your final output

---

## 7. Critical Rules + Prohibited Behaviors

**Quality Standards (rf-analyst.md:316-323) — verbatim:**

> - **Every claim must be traceable** — cite specific files, sections, and line numbers
> - **Counts must be accurate** — double-check totals against actual files
> - **Tables must be complete** — include EVERY relevant data point
> - **Do not invent data** — if you can't verify something, mark it as unverified
> - **Be adversarial** — your job is to find problems, not confirm things work
> - **Fix nothing yourself** — report issues for the appropriate agent to fix. You are read-only on research/synthesis files.

**Critical Rules (rf-analyst.md:340-349) — verbatim:**

> ## Critical Rules
>
> 1. **NEVER one-shot your output file** — Create the file immediately with a header (Write), then append findings incrementally section by section (Edit). Never accumulate the entire report in context and write it in one shot. One-shotting hits max token output limits and freezes the process. This is the #1 failure mode for all agents.
> 2. **Be thorough, not superficial** — your job is to find problems, not rubber-stamp
> 3. **Evidence for every verdict** — never say "looks good" without citing what you checked
> 4. **Report honestly** — if something is borderline, flag it rather than passing it
> 5. **Read EVERY file** — do not skip files or skim
> 6. **Do not modify research or synthesis files** — report issues, let the appropriate agent fix them
> 7. **Zero tolerance for fabrication** — if a research file contains invented claims, flag the entire file
> 8. **Contradictions are important** — always surface them, never resolve them silently

**Confidence Gate Protocol — NOT FOUND:** The Investigation Focus prompt lists "Confidence Gate Protocol" in the 280-349 range. No section by that name exists in `rf-analyst.md` (full read of lines 1-349 performed). The agent enforces evidence-based rigor via Quality Standards + Critical Rules instead. The TDD must either (a) introduce a Confidence Gate Protocol section as a NEW edit, or (b) reconcile the prompt's expectation with the existing Quality Standards section. [STALE-PROMPT-SECTION]

---

## 8. Gaps and Questions

1. **FR-CONV.6 DNSP emission contract has no edit site yet.** Lines 60-69 cover happy-path merge only; the synthetic-DNSP emission contract per-partition exhaust must be inserted as a new sub-section (recommended: after `rf-analyst.md:68`).
2. **ALL-agents-fail escalation target unverified.** The prompt cites `rf-team-lead.md:~414` for the ALL-agents-fail guard; this research did not open `rf-team-lead.md`, so the precise line and current content remain unverified. [VERIFY-PENDING]
3. **No Confidence Gate Protocol section exists** despite the prompt's claim it lives at lines 280-349. Decide: introduce it, or update the prompt to point to Quality Standards (rf-analyst.md:316-323) + Critical Rules (340-349) as the existing equivalents.
4. **Checklist-count drift:** Prompt says "9-item Synthesis Quality Review checklist". Source says 10 items. [STALE-PROMPT-COUNT]
5. **Per-partition `[PARTITION NOTE: ...]` marker semantics** — the marker is defined (`rf-analyst.md:55`) but there is no machine-parseable schema. If the orchestrator's merge step needs to discriminate "subset-limited" from "complete" findings, the TDD should either keep this as a prose convention or upgrade to a structured field.
6. **Spawn-prompt schema is informal.** The five-field contract at `rf-analyst.md:32-39` is plain prose. If a future supervisor needs to validate spawn prompts, the TDD should formalize the schema.

---

## 9. Stale Documentation Found

- [STALE-PROMPT-RANGE] — Investigation Focus described "1-60 (front matter + intro + partition protocol)" but the actual partition protocol body runs `rf-analyst.md:41-69`, and the front-matter ends at line 26.
- [STALE-PROMPT-COUNT] — Investigation Focus described a "9-item Synthesis Quality Review checklist" but the source header at `rf-analyst.md:225` says "Checklist (10 items)" and lists 10 items.
- [STALE-PROMPT-SECTION] — Investigation Focus listed "Confidence Gate Protocol" in lines 280-349, but no such section exists in `rf-analyst.md`. The Quality Standards (316-323) and Critical Rules (340-349) sections are the closest analogs.
- [STALE-PROMPT-SECTION] — Investigation Focus described "60-69 (DNSP emission edit site — FR-CONV.6)" as if it already exists; the current text at those lines covers only Single-Instance default and Orchestrator Responsibilities, with no DNSP emission language. This is an intentional NEW edit site for the TDD, not stale doc per se — but the prompt phrasing implies a state that does not exist.
- [VERIFY-PENDING] — `rf-team-lead.md:~414` ALL-agents-fail escalation reference not opened in this scan.

---

## 10. Summary

The rf-analyst agent supports parallel partitioning out of the box (`rf-analyst.md:41-69`): when the orchestrator passes an `assigned_files` list, the instance scopes its analysis to that subset and tags cross-file checks with `[PARTITION NOTE: ...]`; otherwise it runs as the sole analyst over the full directory. The Phase 3 Research Completeness Verification checklist (`rf-analyst.md:91-129`) is exactly 8 items, and the Phase 5 Synthesis Quality Review checklist (`rf-analyst.md:225-236`) is in fact **10 items, not 9** as the spawn prompt claims — TDD authors should rely on the source count. Cross-validation responsibility is dual-track: rf-analyst performs independent analytical verification while rf-qa performs independent QA verification, both running in parallel under NFR-CONV.10 with the orchestrator reconciling. The DNSP emission contract from FR-CONV.6 and the ALL-agents-fail guard pointing to rf-team-lead are NOT yet present in `rf-analyst.md` lines 60-69; the TDD must add them as new edit sites between `rf-analyst.md:68` and the `---` at line 71. Similarly, no Confidence Gate Protocol section currently exists at lines 280-349 — either author one or remap the requirement to the existing Quality Standards + Critical Rules sections.

---

**Status:** Complete
