# Research: rf-qa Agent Topology

**Status:** Complete
**Date:** 2026-05-14
**Agent type:** Code Tracer
**Source:** src/superclaude/agents/rf-qa.md (432 lines)

---

## 1. The 4 QA Phases

The rf-qa agent operates as four distinct gates plus a fix-cycle recursion. Each gate has its own input contract, checklist, and verdict rule. All four gates share the same output format (line 316) and the zero-trust PASS/FAIL semantics defined at lines 141-142.

### 1.1 Research Gate (rf-qa.md:96-141)

| Field | Value |
|---|---|
| When | After Phase 2 (Deep Investigation) and Phase 3 (Completeness Verification), before Phase 4/5 (line 98) |
| Purpose | Mandatory quality gate ensuring research is thorough enough to produce reliable synthesis (line 99) |
| Input | ALL research files in `${TASK_DIR}research/` + analyst's completeness verification report in `${TASK_DIR}qa/` (line 103) |
| Parallel posture | Runs in parallel with rf-analyst — both read the same files independently (line 105) |
| Checklist size | 10 items (line 109) |
| Verdict rule | PASS only if all checks pass AND no gaps of any severity (line 141); ANY gap (CRITICAL, IMPORTANT, MINOR) = FAIL (line 142) |

**Checklist topics (10 items, lines 111-137):** file inventory, evidence density, scope coverage, documentation cross-validation, contradiction resolution, gap severity, depth appropriateness, integration point coverage, pattern documentation, incremental writing compliance.

### 1.2 Synthesis Gate (rf-qa.md:146-211)

| Field | Value |
|---|---|
| When | After Phase 5 (Synthesis), before Phase 6 (Assembly) (line 148) |
| Purpose | Ensure synthesis files are high-quality, evidence-based, and ready for assembly (line 149) |
| Input | ALL synthesis files in `${TASK_DIR}synthesis/` matching `synth-*.md` (line 153) |
| Checklist size | 12 items (line 155) |
| Fix authorization | Conditional — keyed off `fix_authorization: true|false` in spawn prompt (lines 201-211) |
| Verdict rule | Implicit — same zero-trust posture; no separate verdict block in this section |

**Checklist topics (12 items, lines 157-199):** section headers, table structure, no fabrication, evidence citations, options analysis quality, implementation plan specificity, cross-section consistency, doc-only claims excluded from architecture, stale docs surfaced, content rules compliance, completeness, no hallucinated file paths.

### 1.3 Report Validation (rf-qa.md:215-256)

| Field | Value |
|---|---|
| When | After Phase 6 (Assembly), before presenting to user (Phase 7) (line 217) |
| Purpose | Final quality check on the assembled research report (line 218) |
| Input | Final research report at `${TASK_DIR}RESEARCH-REPORT-*.md` (line 222) |
| Checklist size | 19 items (15 from SKILL.md validation checklist at lines 226-240 + 4 content quality checks at lines 244-247) — header says "19 items" (line 224) |
| Fix authorization | ALWAYS authorized for this phase (lines 249-255) |

**Checklist topics:** ten-section presence, problem statement linkage, file:line citations, gap severity ratings, source URLs, options ≥2 with table, recommendation linkage, implementation plan specificity, open questions schema, evidence trail, no source dumps, tables over prose, no assumptions-as-facts, no doc-only architecture claims, stale doc surfacing, ToC accuracy, internal consistency, readability, actionability.

### 1.4 Task Integrity (rf-qa.md:259-289)

| Field | Value |
|---|---|
| When | After task file creation (A.8 in tech-research), to verify the task file is well-formed (line 261) |
| Purpose | Ensure the MDTM task file follows template rules and will execute correctly (line 262) |
| Input | The created task file (path passed in spawn prompt) |
| Checklist size | 20 items (line 266) |
| Verdict rule | Inherits zero-trust posture; gates against B2 self-containment (item 3), atomicity (item 10), intra-phase dependencies (item 11), execution-order simulation (item 16) |

**This is the FR-CONV.1 insertion site** — the 8 TB-Add checks land here, producing 28 items post-merge (or consolidating to a smaller count if duplicates exist with current items 11, 15, 16).

### 1.5 Cross-Phase Contract Summary

| Phase | Input | Output Location | Verdict Source | Fix Auth |
|---|---|---|---|---|
| Research Gate | research/ + qa/analyst-report | `${TASK_DIR}qa/qa-research-gate*.md` (implied) | line 141-142 (PASS/FAIL on any gap) | Not specified in section |
| Synthesis Gate | synthesis/synth-*.md | `${TASK_DIR}qa/qa-synthesis-gate*.md` (implied) | Inherits zero-trust | Conditional (`fix_authorization`) |
| Report Validation | RESEARCH-REPORT-*.md | `${TASK_DIR}qa/qa-report-validation*.md` (implied) | Inherits zero-trust | Always authorized |
| Task Integrity | task file | `${TASK_DIR}qa/qa-task-integrity*.md` (implied) | Inherits zero-trust | Not specified |

---

## 2. Partition Protocol (rf-qa.md:49-77)

When the workload is large, the orchestrator spawns multiple rf-qa instances in parallel, each assigned a subset of files. This prevents context rot.

### 2.1 Trigger and Threshold

> "Deciding when to partition (based on file count — typically >6 files warrants partitioning)" (line 74)

The threshold is **>6 files**. Below that, a single rf-qa instance verifies all files (default behavior, lines 67-69).

### 2.2 Partition Instance Contract (lines 59-65)

When `assigned_files` is present in the spawn prompt:
1. Verify ONLY the files in the `assigned_files` list (line 61)
2. Apply the same checklist rigor to the subset (line 62)
3. Cross-file checks (contradictions, cross-refs, scope coverage) are applied only within the subset; note in report: `[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]` (line 63)
4. Report title includes `(Partition [N] of [M])` (line 64)
5. Orchestrator merges all partition reports after all instances complete (line 65)

### 2.3 Orchestrator Responsibilities (lines 73-77)

The skill session or team lead is responsible for:
- Deciding when to partition (line 74)
- Dividing files into balanced subsets (line 75)
- Spawning multiple rf-qa instances in parallel, each with its `assigned_files` list (line 76)
- Merging partition reports — "union of findings, take the more severe rating for shared items" (line 77)

### 2.4 Escalation Ladder and All-Agents-Fail Guard

**IMPORTANT — clarification of task brief:** The rf-qa.md file (lines 49-77) does NOT describe an "initial → retry-1 → retry-2 escalation ladder" or an "all-agents-fail guard" inside the partition section. Those concepts live in `rf-team-lead.md` (escalation around line 414 per task brief). What rf-qa.md DOES describe:
- Partition instances are stateless workers; each produces an independent QA report
- The orchestrator merges reports post-hoc (line 65, 77)
- Failure handling (retries, escalation) is the orchestrator's responsibility, NOT rf-qa's

**Operational implication:** When all partition instances return FAIL (zero successful partitions), the orchestrator — not rf-qa — invokes the rf-team-lead escalation path. rf-qa itself does NOT emit a DNSP; DNSP emission lives in the synthesis edit site (lines 70-77 area, see Section 6 below) and is gated by FR-CONV.6.

---

## 3. Zero-Trust Verdict Semantics (rf-qa.md:144-146 / verified region)

**Sed verification — `sed -n '140,150p' src/superclaude/agents/rf-qa.md`:**

```
(line 140) [blank]
(line 141) - **PASS** — All checks pass, no gaps of any severity. Green light for synthesis.
(line 142) - **FAIL** — Any gaps exist (CRITICAL, IMPORTANT, or MINOR). List each gap with a specific remediation action. ALL gaps must be resolved before proceeding — no severity level is exempt.
(line 143) [blank]
(line 144) ---
(line 145) [blank]
(line 146) ## QA Phase: Synthesis Gate (Pre-Assembly Quality Gate)
```

**Note on drift:** The task brief states the verdict is "expected at 144-146" but sed output confirms the verdict text is actually at **lines 141-142** (with line 139 being the `### Verdict` header). The "144-146" range falls on the section separator and the start of the next phase header. PRD-cited "140-142" is closer to the actual position. See Section 8 for drift severity assessment.

### 3.1 Zero-Trust QA Invariant — Operational Source

The two-line verdict block is the canonical operational source of the zero-trust QA invariant:

- **PASS** requires (a) all checks pass AND (b) no gaps of any severity
- **FAIL** is mandatory if ANY gap exists at any severity (CRITICAL, IMPORTANT, or MINOR)
- The phrase "ALL gaps must be resolved before proceeding — no severity level is exempt" enforces that MINOR severity is NOT a soft warning — it blocks PASS

This rule is reinforced by:
- Critical Rule 9 (line 430): "Report honestly — A false PASS is worse than a false FAIL. When in doubt, fail it and explain why."
- Critical Rule 10 (line 431): "Maximum 3 fix cycles. ALL findings regardless of severity must be resolved."
- Verification Principle 0 (line 83): adversarial stance — "A review that finds 0 issues should be treated with suspicion"
- Verification Principle 8 (line 91): "NO LENIENCY: Do not give agents the benefit of the doubt"

---

## 4. 20-Item Task-Integrity Checklist (rf-qa.md:266-287 / verified region)

**Sed verification — `sed -n '264,290p' src/superclaude/agents/rf-qa.md`:**

The header `#### Checklist (20 items)` appears at line 266. The numbered items occupy lines 268-287. Line 288 is blank; line 289 is the `---` section terminator.

**Verbatim verbatim items (lines 268-287):**

1. **Frontmatter schema** (line 268) — YAML frontmatter is well-formed AND contains all required fields with non-empty values: `id`, `title`, `status`, `created`, `type`, `template`, `tracks`. Not just "parses as valid YAML" — every mandatory field must be present. Missing fields = FAIL.
2. **Checklist format** (line 269) — All items use `- [ ]` format (not `- []` or `* [ ]`)
3. **B2 self-contained** (line 270) — Each item is a single paragraph containing context + action + output + verification (not split across multiple lines with headers)
4. **No nested checkboxes** (line 271) — No sub-items under checklist items
5. **Agent prompts embedded** (line 272) — For subagent-spawning items, the full prompt is in the item (not "see above" or "use the template from SKILL.md")
6. **Parallel spawning indicated** (line 273) — Items in Phases 2, 4, 5 that spawn independent agents are marked for parallel execution
7. **Phase structure** (line 274) — Phases appear in correct order, no gaps
8. **Output paths specified** (line 275) — Every item that produces a file specifies the output path
9. **No standalone context items** (line 276) — Every `- [ ]` item results in a concrete action, not just "read file X"
10. **Item atomicity** (line 277) — Each item is scoped to a single atomic change. Items exceeding ~15 lines of embedded content or describing multiple distinct file modifications must be split. A 40-line item that modifies 3 files and runs 2 commands is a granularity violation even if it is self-contained. Check: could someone execute this item without scrolling? If not, it's too big.
11. **Intra-phase dependency ordering** (line 278) — Within each phase, items that read or depend on a file must be ordered AFTER items that create or modify that file. Phase-level dependency checks (Phase 4 depends on Phase 3) are NOT sufficient — item-level ordering within a phase matters. Check: for each item that reads a file, is the item that creates that file earlier in the same phase (or a previous phase)?
12. **Duplicate operation detection** (line 279) — Scan ALL items across ALL phases for identical or near-identical shell commands, file operations, or gate invocations. If two items both run the same command (e.g., `make sync-dev` + `make verify-sync`), one is redundant unless there is an intervening change between them that justifies re-running. Flag exact duplicates as IMPORTANT.
13. **Verification durability** (line 280) — Every item has a verification step (existing check from item 3), AND that verification is durable and CI-compatible. Tests must be in the project's test directory as proper test files (pytest, vitest, etc.), not inline `python -c` one-liners or shell scripts that vanish after execution. If the project has a `tests/` directory with an existing test suite, verification items must add to that suite — not bypass it. Inline verification is acceptable ONLY for non-code tasks (e.g., "verify file exists").
14. **Completion criteria honesty** (line 281) — If the task file's Open Questions section contains unresolved critical or important items, the final "mark done" item must NOT unconditionally set status to "Done." It must either: (a) resolve those questions earlier in the plan, (b) mark the task as "Done with caveats" referencing the open items, or (c) include a conditional that checks open questions before setting done status. Claiming "done" while known unknowns remain is a false completion — flag as IMPORTANT.
15. **Phase AND item-level dependencies** (line 282) — Phase dependencies are logical (no circular or missing) AND within each phase, data flow between items is correct. An item that consumes output from another item must come after it, even if both are in the same phase. This supersedes item 7 (phase structure) by extending it to item-level granularity.
16. **Execution-order simulation** (line 283) — For items passing kwargs, verify the function signature is updated BEFORE the kwarg is passed. Walk execution sequence item-by-item and confirm each step has its prerequisites satisfied by earlier items.
17. **Function/class existence verification** (line 284) — Grep cited files to confirm referenced functions exist with claimed visibility (public vs private). Every function name, class name, or method referenced in a checklist item must be verified to exist in the cited source file.
18. **Phase header accuracy** (line 285) — Count `- [ ]` items per phase, verify against header's claimed count. If a header says "Phase 2 (5 items)" but there are 6 items, that's a FAIL.
19. **Prose count accuracy** (line 286) — Verify quantitative claims in Overview/descriptions match actual implementation. If the overview says "refactors 7 functions" but the checklist only touches 4, that's a FAIL.
20. **Template section cross-reference** (line 287) — Read actual templates referenced by the task file, verify §N references match real content. If an item says "per template §A3" confirm that section actually exists and says what the item claims.

### 4.1 FR-CONV.1 Insertion Site Analysis

The 8 TB-Add checks added by FR-CONV.1 must land here. Two possible merge strategies:

**Strategy A — Append (28 items total):** Add 8 new items as 21-28 with TB-Add semantics. Simplest but produces redundancy with items 11, 15, 16 (all touch execution ordering).

**Strategy B — Consolidate:** Merge TB-Add checks into existing items where overlap exists:
- TB-Add items concerning execution ordering → consolidate with items 11, 15, 16
- TB-Add items concerning B2 self-containment → consolidate with item 3
- TB-Add items concerning function/class existence → consolidate with item 17
- New TB-Add categories (no overlap) → append as items 21-N

**Recommended:** TDD should specify the FR-CONV.1 author's chosen strategy. The merge boundary is between items 20 (line 287) and the section separator at line 289.

---

## 5. Fix-Cycle Limits per Gate Type (rf-qa.md:291-313)

The Fix Cycle phase (line 291) governs how QA re-verifies after failed gates. The global limit is **3 cycles maximum** (line 311). Per-gate limits referenced by the task brief (rf-task-builder I16) are NOT explicitly enumerated in rf-qa.md itself.

### 5.1 Global Limit (line 311)

> "Maximum 3 fix cycles. After 3 cycles, if issues remain, HALT execution and ask the user for guidance. Do NOT convert unfixed findings to Open Questions."

Reinforced by Critical Rule 10 (line 431): "Maximum 3 fix cycles — After 3 rounds of fixes without resolution, HALT and escalate to the user."

### 5.2 Monotonicity Requirement (line 312)

> "Each cycle should have fewer issues than the previous one. If issue count increases, flag this as a systemic problem."

**This is the FR-CONV.5 tie-in:** retry monotonicity. The current text says issue count "should" decrease cycle-over-cycle, and increase = "systemic problem" flag. FR-CONV.5 likely tightens this from advisory to mandatory invariant.

### 5.3 Per-Gate Limits (Task Brief Cites rf-task-builder I16)

| Gate | Limit (per task brief) | Source in rf-qa.md |
|---|---|---|
| research-gate | 3 | NOT in rf-qa.md — sourced from rf-task-builder.md I16 |
| synthesis-gate | 2 | NOT in rf-qa.md — sourced from rf-task-builder.md I16 |
| report-validation | 3 | NOT in rf-qa.md — sourced from rf-task-builder.md I16 |
| task-integrity | 2 | NOT in rf-qa.md — sourced from rf-task-builder.md I16 |

**Finding:** rf-qa.md defines only the global maximum (3 cycles). Per-gate differentiation lives in `rf-task-builder.md` (I16 reference). This is a cross-file coupling point the TDD must surface.

### 5.4 Fix Cycle Process (lines 297-307)

1. Read the previous QA report (path provided in prompt)
2. For each issue flagged in the previous report: verify the fix was applied, verify the fix is correct (not just present), flag if the fix introduced new issues
3. Produce an updated QA report listing previously-failed-now-pass, previously-failed-still-fail, and new issues
4. Updated verdict: PASS / FAIL

---

## 6. DNSP Emission Edit Site (rf-qa.md:70-77)

The task brief identifies lines 70-77 as the FR-CONV.6 DNSP emission contract edit site. Current content at this range:

```
(line 70) ### Orchestrator Responsibilities (Not Your Job)
(line 71) [blank]
(line 72) The orchestrator (skill session or team lead) is responsible for:
(line 73) - Deciding when to partition (based on file count — typically >6 files warrants partitioning)
(line 74) - Dividing files into balanced subsets
(line 75) - Spawning multiple rf-qa instances in parallel, each with its `assigned_files` list
(line 76) - Merging partition reports after all instances complete (union of findings, take the more severe rating for shared items)
(line 77) [blank]
```

**Analysis:** This section explicitly disclaims rf-qa responsibility for partition orchestration ("Not Your Job"). FR-CONV.6 will append a **synthetic-dnsp emission contract** — likely specifying:
- When rf-qa emits a `synthetic-dnsp` signal (e.g., when partition reports show all-fail)
- Format of the DNSP payload
- Recipient (rf-team-lead per task brief)
- Boundary: rf-qa emits, orchestrator decides what to do with it

The append boundary is line 77 (blank line before next section). The TDD should preserve the "Not Your Job" framing — DNSP emission is a *signal* not an *action*; rf-qa fires the signal but does not orchestrate the response.

**Cross-reference:** rf-team-lead.md:~414 receives the DNSP per task brief Section 2.4. This is the consumer side of the FR-CONV.6 contract.

---

## 7. Critical Rules and Prohibited Behaviors

### 7.1 Critical Rules (rf-qa.md:420-432)

11 numbered rules governing agent execution:

1. **NEVER one-shot your output file** (line 422) — Create with Write, append with Edit. One-shotting hits max token output limits. "#1 failure mode for all agents."
2. **Assume everything is wrong** (line 423) — Verify independently. Do not trust agent claims, worker outputs, or previous QA passes.
3. **Evidence for every verdict** (line 424) — Never say "looks good" without citing exactly what you checked and how.
4. **Fix then verify** (line 425) — A fix that doesn't verify = still failed.
5. **Zero tolerance for fabrication** (line 426) — If an agent fabricated paths/data/claims, flag the ENTIRE output, not just the fabricated item.
6. **Contradictions are critical** (line 427) — Never resolve silently. Always surface.
7. **Be specific about fixes** (line 428) — "This needs to be better" is useless. Concrete location + concrete fix required.
8. **Read EVERY file in scope** (line 429) — No skipping or skimming.
9. **Report honestly** (line 430) — A false PASS is worse than a false FAIL. When in doubt, fail it.
10. **Maximum 3 fix cycles** (line 431) — HALT and escalate. ALL findings regardless of severity must be resolved.
11. **You are the last line of defense** (line 432) — If you miss it, it goes into the final report as fact.

### 7.2 Prohibited Behaviors (rf-qa.md:407-413)

Six absolute prohibitions in the Confidence Gate Protocol:

1. NEVER adjust confidence based on subjective feeling — confidence is COMPUTED from the checklist (line 408)
2. NEVER report confidence without raw numbers (line 409)
3. NEVER claim VERIFIED without citing specific tool output (line 410)
4. NEVER mark an item VERIFIED if you only read about it in another report — "that is RELIANCE, not VERIFICATION" (line 411)
5. NEVER issue a PASS verdict without meeting the threshold (line 412)
6. NEVER make generic tool calls to inflate engagement counts — "Tool calls that don't map to specific verifications are padding, not evidence" (line 413)

### 7.3 Confidence Gate Protocol (rf-qa.md:376-413)

Runs after every QA phase checklist BEFORE writing the verdict (line 378). Five-step protocol:

1. **Categorize** every checklist item: VERIFIED `[x]`, UNVERIFIABLE `[?]`, UNCHECKED `[ ]` (lines 380-384)
2. **Count** TOTAL, VERIFIED, UNVERIFIABLE, UNCHECKED (lines 386-390)
3. **Compute** `confidence = VERIFIED / (TOTAL - UNVERIFIABLE) * 100` (lines 392-393)
4. **Apply thresholds:**
   - ≥95% AND UNCHECKED == 0 → eligible for PASS (line 396)
   - <95% OR UNCHECKED > 0 → NOT eligible; up to 3 additional verification rounds (line 397)
   - After 3 rounds still <95% → FAIL with documented limitations (line 398)
5. **Report (MANDATORY):** confidence string, tool engagement counts, every UNCHECKED with reason, every UNVERIFIABLE with blocker (lines 400-405)

### 7.4 Tool Engagement Minimum (rf-qa.md:415-416)

> "If your total (Read + Grep + Glob) calls < TOTAL checklist items, the review is automatically suspect. You cannot have verified more items than you made tool calls."

This is the FR-CONV.4 anchor (per task brief — tool-engagement minimum is part of the protocol convergence work).

---

## 8. Line-Number Drift Confirmation

| Drift entry | PRD cite | Task brief expectation | Actual sed-verified location | Drift Δ | Severity |
|---|---|---|---|---|---|
| Zero-trust verdict | lines 140-142 | lines 144-146 | **lines 141-142** (verdict block); section sep at 144; next phase header at 146 | PRD off by ~1; task brief off by ~3 | LOW |
| 20-item task-integrity checklist | lines 264-287 | lines 266-287 | **lines 268-287** (numbered items 1-20); header `#### Checklist (20 items)` at line 266 | PRD off by ~4 (items only); task brief off by ~2 (items only) | LOW |

**Sed evidence — verdict drift:**
```
$ sed -n '140,150p' src/superclaude/agents/rf-qa.md
(140) [blank]
(141) - **PASS** — All checks pass, no gaps of any severity. Green light for synthesis.
(142) - **FAIL** — Any gaps exist (CRITICAL, IMPORTANT, or MINOR). [...]
(143) [blank]
(144) ---
(145) [blank]
(146) ## QA Phase: Synthesis Gate (Pre-Assembly Quality Gate)
```

**Sed evidence — checklist drift:**
```
$ sed -n '264,290p' src/superclaude/agents/rf-qa.md
(264) ### What You Verify
(265) [blank]
(266) #### Checklist (20 items)
(267) [blank]
(268) 1. **Frontmatter schema** [...]
(...) [items 2-19]
(287) 20. **Template section cross-reference** [...]
(288) [blank]
(289) ---
```

**Drift severity assessment: LOW.** Semantic content matches; only line numbers differ by ≤4. The PRD's "264-287" range correctly bounds the checklist body if interpreted as "the block containing the checklist including its header." The task brief's "144-146" range for the verdict appears to be off-by-three relative to current file state, possibly reflecting an older version. No content has changed materially; line drift is purely the result of upstream additions in surrounding sections.

**TDD impact:** All PRD line citations referencing rf-qa.md must be re-verified against the current file state at TDD authoring time. A drift table (this section) should be included in the TDD or its appendix.

---

## 9. Gaps and Questions

1. **Per-gate fix-cycle limits not in rf-qa.md.** Task brief cites limits (research-gate 3 / synthesis-gate 2 / report-validation 3 / task-integrity 2) as living in rf-task-builder.md I16. rf-qa.md defines only the global maximum of 3. The TDD must clarify whether per-gate limits are authoritative there, or whether rf-qa.md should be updated to encode them.
2. **DNSP emission contract is not yet present.** Lines 70-77 are the *target* edit site but contain no DNSP language today. FR-CONV.6 must specify format, trigger condition, and recipient.
3. **All-agents-fail guard semantics.** Task brief asserts "all-agents-fail guard = zero successful partitions activates rf-team-lead.md:~414 escalation, NOT DNSP." But the relationship between *partition failure* and *DNSP emission* needs explicit specification in the TDD — is DNSP emitted on partial partition failure? On all-fail only? Never (orchestrator decides)?
4. **Fix-cycle monotonicity strength.** Line 312 says "should have fewer issues" (advisory). FR-CONV.5 needs to specify whether this becomes a hard invariant (FAIL if count increases) or remains advisory.
5. **FR-CONV.1 merge strategy.** TDD must choose between append (28 items) or consolidate (smaller count). Items 11, 15, 16 overlap with likely TB-Add checks on execution ordering.
6. **Output file path convention.** All four phases imply outputs land in `${TASK_DIR}qa/` but no explicit path convention is documented in rf-qa.md. Naming convention (e.g., `qa-{phase}-{partition-N-of-M}.md`) should be specified in the TDD.
7. **Fix authorization defaults.** Research Gate and Task Integrity sections do not specify default fix authorization. Synthesis Gate is conditional. Report Validation is always-authorized. Defaults need pinning.

---

## 10. Stale Documentation Found

| Claim | Severity | Tag | Notes |
|---|---|---|---|
| PRD cites verdict block at lines 140-142 | LOW | CODE-CONTRADICTED | Actual: lines 141-142 (off by 1). Content semantically identical. |
| Task brief expects verdict at lines 144-146 | LOW | CODE-CONTRADICTED | Actual: lines 141-142. Lines 144-146 contain section separator and next phase header. |
| PRD cites task-integrity checklist body at lines 264-287 | LOW | CODE-CONTRADICTED | Items 1-20 actually at lines 268-287; line 266 is the header. PRD range includes header + 2 blank lines. |
| Task brief expects checklist body at 266-287 | LOW | CODE-CONTRADICTED | Header at 266; items at 268-287. Off by 2 if "body" means numbered items only. |
| Partition threshold ">6 files" | n/a | CODE-VERIFIED | Confirmed at line 74 verbatim. |
| Fix-cycle max = 3 | n/a | CODE-VERIFIED | Confirmed at lines 311, 431. |
| Confidence threshold ≥95% | n/a | CODE-VERIFIED | Confirmed at line 396. |
| Per-gate fix-cycle limits per rf-task-builder I16 | UNVERIFIED | UNVERIFIED | Not present in rf-qa.md; cross-file claim requires rf-task-builder.md verification (out of scope for this trace). |
| rf-team-lead escalation at ~414 | UNVERIFIED | UNVERIFIED | Cross-file claim; not visible in rf-qa.md. Requires rf-team-lead.md verification (out of scope). |
| 19-item validation checklist count | LOW | CODE-VERIFIED | Header says 19 (line 224); body shows 15 items in first group (lines 226-240) + 4 in Content Quality Checks (lines 244-247) = 19. Math confirms. |

---

## 11. Summary

The rf-qa agent (`src/superclaude/agents/rf-qa.md`, 432 lines) is a four-phase quality gate (Research Gate / Synthesis Gate / Report Validation / Task Integrity) plus a Fix Cycle recursion, all governed by a uniform zero-trust verdict invariant: PASS requires zero gaps of any severity, FAIL is mandatory on any gap. Partition Protocol (lines 49-77) allows the orchestrator to spawn parallel rf-qa instances on subsets when file count exceeds 6, with rf-qa explicitly disclaiming orchestration responsibility — the section at lines 70-77 is the designated FR-CONV.6 DNSP emission edit site. The 20-item Task Integrity checklist (lines 268-287; header at 266) is the FR-CONV.1 insertion point for 8 TB-Add checks, with potential consolidation against existing items 11, 15, 16, 17 governing execution ordering and function/class existence. Fix-cycle global max is 3 (line 311) with advisory monotonicity (line 312) that FR-CONV.5 likely upgrades to invariant; per-gate limits cited by the task brief live in rf-task-builder.md, not rf-qa.md. Line drift is LOW severity — content semantically matches PRD/task-brief citations but line numbers have shifted by ≤4 due to upstream additions; the TDD must include a drift-corrected citation table.

---

**Status:** Complete
