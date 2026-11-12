# Research: Template and Examples

**Topic type:** Template rules and prior-art examples
**Scope:** `~/.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1; recent TASK-RF task files under `.dev/tasks/`; skill-mode POST reflect item form in `~/.claude/skills/task-builder/SKILL.md`
**Status:** Complete
**Date:** 2026-11-08

---

Abbreviations: T02 = `~/.claude/templates/workflow/02_mdtm_template_complex_task.md` (1519 lines; PART 1 = lines 63-1135, PART 2 = 1143-1519). TB = `~/.claude/skills/task-builder/SKILL.md` (2606 lines).

## 1. Frontmatter fields (T02:1-60, TB:2156-2180)

- T02 frontmatter keys (T02:2-60): `id`, `title`, `description`, `version`, `status` (default `"🟡 To Do"`, T02:7), `type` (T02:8-9), `priority` (T02:10-11), `created_date`, `updated_date`, `assigned_to`, `autogen`, `autogen_method`, `coordinator: orchestrator`, `parent_doc`, `parent_task`, `depends_on` (list), `spec_path` (T02:23, "populated by task-builder (A.2), empty if none"), `reflect_pre` block with `verdict`/`coverage_pct`/`depth`/`tcs`/`run_id`/`report`/`reviewed_at` (T02:24-31, "populated by task-builder at A.10.7"), `reflect_post: ""` (T02:32, "recorded by the executor after the final-phase reflect subagent runs"), `related_docs` list of `{path, description}` (T02:33-39), `related_prd`, `related_tdd`, `tags`, `template_schema_doc`, `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`, `review_info` block, `task_type: static` (T02:60).
- TB adds `reflect_post_mode: <skill|cli>` — "ALWAYS emitted (every build)" (TB:2170). `start_commit` and `executor_model_class` are CLI-mode only (TB:2171-2172); a skill-mode file must carry NEITHER, a hybrid is MALFORMED (TB:2314).
- `id` pattern in TB: `TASK-RF-<subject>-YYYYMMDD-HHMMSS` (TB:2158); `template_schema_doc` points at the 01/02 template (TB:2167).
- `qa_intensity` is NOT a frontmatter key in T02 (absent from T02:1-60; grep of T02 for `qa_intensity` hits only T02:704, 798, 1068, 1076). TB carries it as the BUILD_REQUEST field `QA_INTENSITY: [lite / standard / full]` (TB:1002). Builder should state the chosen intensity in `## Execution Context` → Key Constraints (T02:1210 says constraints include "QA intensity").
- `task_type`: `static` for fixed content; `dynamic` only if workers add items inside `<!-- DYNAMIC CONTENT START/END -->` markers (T02:548-572). Phase 1 here is fully enumerable, so `static`.
- Blocked status is written `"⚪ Blocked"` in T02:467 and T02:1232 but `"🔴 Blocked"` in the option list (T02:6). The template is inconsistent; the builder should pick one and use it consistently (Unverified which one `/task` checks).

## 2. Section A — granular breakdown (T02:108-133)

- A3 (T02:108-112): break EVERY phase into atomic, verifiable items; one item per file/component/iteration; "NO high-level or bulk operations"; exact file paths and measurable outcomes.
- A4 (T02:114-133): for multi-item processes, pre-enumerate all items, one item per item, incremental updates after each, consolidation only after all complete (pattern Step X.1 enumerate → X.2 per-item → X.3 consolidate).
- Application: steps 1.1-1.28 from design §15 each become their own `- [ ]` item (or several, if a step touches >1 file); the three design fixes R3-B1/B2/B3 are three separate items, not one "apply R3 fixes" item. K2 (T02:886-903) adds that the builder MUST enumerate all items up front; the worker MUST NEVER add items dynamically.

## 3. Section B — self-contained items (T02:151-213)

- B1 (T02:151-157): session rollover — context loaded in batch 1 is gone by batch 3+.
- B2 six required elements (T02:159-165): (1) context reference with WHY; (2) action with WHY; (3) output spec (exact path, content, template); (4) integrated verification "ensuring..." clause with no-fabrication language; (5) evidence on failure only (log blocker to Task Log); (6) explicit completion gate: "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."
- B3 (T02:167-170): ONE FULL PARAGRAPH per item.
- B5 forbidden (T02:181-200): standalone "read context" items; items with no source reference; multi-line/bulleted items; separate verification items; over-granular items ("create directory" alone); REMINDER blocks between items.
- **Conflict to resolve (builder must pick):** TB's own Output Structure uses a five-sub-bullet form per item — `**Context** / **Action** / **Output** / **Verification** / **Completion gate**` (TB:2203-2208, and the POST reflect item TB:2219-2235) — which contradicts T02 B3/B5 "single paragraph, not bulleted" (T02:168, T02:192-197). TB Rule 14 requires "context, action, output, verification, and completion gate" (TB:2361); validation checklist: "Items follow B2 self-contained pattern (context + action + output + verification + completion gate)" (TB:2288); TB-Add-1 "5-field schema enforced" (TB:2305). Recommendation: use the TB 5-field form, since TB's validators check it. Unverified whether an A.10 lens would flag it against B3.

## 4. Sections D/E/F/J — structure and execution rules

- D3 (T02:286-289): no checklist items before Phase 1.
- E1-E4 (T02:295-405): flat `- [ ]` only, no nested checkboxes, no parent checkbox before children, summaries last, step numbers are bold headers without checkboxes, strictly top-to-bottom, no "see below / go back".
- F2 (T02:422-429): one item at a time; a subagent receives work from a SINGLE item; phase-gate QA mandatory after Phase 2+; post-completion validation mandatory. F2a (T02:447) allows parallel spawn of consecutive INDEPENDENT subagent items in the same phase.
- F5 (T02:464-468) and I11 (T02:605-607): first action is status → "🟠 Doing" + `start_date` (example item T02:1327).
- **J1/J2 (T02:854-865): the default error clause is "log the specific blocker ... then mark this item complete", and "Items are NEVER left unchecked".** J3 (T02:867-868): mark the task Blocked only if ALL remaining items are blocked by the same issue. This default is WRONG for a human gate: it would let `/task` mark an owner-decision item done and proceed. See section 9.
- TB Rule 19 (TB:2371): the only permitted mid-execution halts are (a) all items blocked by the same unrecoverable issue, (b) phase-gate QA failing 2 fix cycles, (c) an item output that fundamentally invalidates the rest of the task. No scope or cost pauses.

## 5. Section I — QA rules

- I14 (T02:623-633): every task references `~/.claude/rules/core/anti_hallucination_task_completion_rules.md`; G1 (T02:474) says framework rule files are NOT auto-loaded into headless workers, so an item that needs one must name it.
- I15 (T02:635-651): every task with 2+ phases needs at least one phase-gate QA between the primary execution phase and any dependent phase. Full sequence: aggregation (L6) → parallel lens agents `fix_authorization: false` → consolidation → ONE fix agent `fix_authorization: true` → verification round (at least 2) → conditional proceed (L5) → M4 if applicable. Each spawn item names agent type, lens, inputs, report path, `fix_authorization: false`, and adversarial framing "Assume this document has at least N errors focused on your lens. Find them." (T02:649). "No QA is implicit. No QA lives only in prose." (T02:651).
- I16 (T02:653-677): binary PASS/FAIL; blocking = wrong behaviour, false claim, missing deliverable, security/data-loss; minor never fails a review; max 2 fix cycles (3 reviews), then HALT and escalate to the user; CRITICAL/IMPORTANT = blocking, MINOR = minor, graded by definition not label; fix-cycle logic encoded as L5 items.
- I17 (T02:679-690): before Done — all items `[x]`; outputs exist (Glob); blockers have resolution notes; tests pass if code modified; post-completion lens QA per M3; M4 if source-derived.
- I18 (T02:692-701): code-modifying tasks need at least one testing item with exact command, pass criteria and results location; use L3.
- **I19 (T02:703-747), full-intensity floors:** final gate <500 lines 3+3=6, 500-1500 4+4=8, 1500-3000 5+5=10, >3000 6+6=12 (T02:710-715). Standard structural lenses: template-conformance, internal-consistency, evidence-quality, completeness (T02:719-723). Content lenses: actionability, numbers-metrics, crossref-chain, domain-accuracy (T02:725-729). Adversarial N = 5/10/15/20 by size (T02:733). Intermediate gates: 5 agents (T02:737-741).
- **I20 (T02:749-761):** serialized fix. Report (parallel, false) → consolidate to `${TASK_DIR}qa/qa-consolidated-findings.md` → ONE fix agent (none if only minor findings) → verification by at least 2 agents (1 rf-qa + 1 rf-qa-qualitative) → repeat from consolidation, max 2 cycles. Every step an explicit `- [ ]` item (T02:761). Applies at ALL intensities (T02:842-844).
- **I21 (T02:763-792):** fidelity gate mandatory for "Any task where the orchestrator reads source documents to produce output" (T02:775); not required for mechanical transforms or config-only work (T02:777-779). Checks semantic coverage, detail preservation, cross-source contradiction, phantom coverage, operational completeness (T02:781-786). Minimum 2 agents; partition to 3-4 if sources exceed 1000 lines (T02:788). Runs AFTER M3 (T02:792). M2 (T02:1056): for code-modifying tasks, "Fidelity gate only if code was derived from spec documents". Phase 1 code IS derived from `docs/designs/orchestrator-mode.md` §15, so M4 applies to the implementation gate, and to each design-fix gate (each fix is derived from the R3 findings plus code).
- **I22 (T02:797-844):** lite = intermediate 2, final 3 (1+1+1 domain), fidelity 1, 1 fix cycle, 1 verifier. Standard = intermediate 3, final 7 (3 structural: template-conformance, internal-consistency, evidence-quality; 3 content: actionability, domain-accuracy, crossref-chain; 1 domain), fidelity 2, 2 fix cycles, 2 verifiers, partition only above 10 files. Full = I19/I20/I21 unchanged. Double QA is disabled at lite and standard (T02:827, 836).
- TB Rule 16 (TB:2365): each final-document gate must meet the I22 minimum for its intensity (lite 3, standard 7, full 6+); intermediate gates at least 5; any shortfall is MALFORMED. The TB A.10.5 sufficiency lens rejects any gate with fewer than 6 agents (TB:2142), which conflicts with I22's lite count of 3. Standard (7) or full avoids that conflict.

## 6. Section L / M — handoff and gate patterns (T02:905-1125)

- Handoff convention (T02:913-925): outputs under `.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/`, persisted across batches.
- L1 Discovery (T02:932-942): the discovery file IS the deliverable, machine-readable. Fits step 1.0a (Orca capture).
- L2 Build-from-discovery (T02:944-954): read the discovery file AND the source file.
- L3 Test/Execute (T02:956-966): capture raw output AND a structured summary; execution failures (not test failures) go to the blocker log.
- L4 Review (T02:968-978): structured PASS/FAIL verdict, criteria checklist, issues with severity, recommendation.
- L5 Conditional (T02:980-992): MUST handle BOTH branches; output file always created whichever branch runs. Use for every gate's "IF PASS proceed / IF FAIL" item and for human-gate checks.
- L6 Aggregation (T02:994-1004): Glob for inputs dynamically.
- L7 (T02:1006-1030): "Full Lifecycle with QA Gates: L1 → L2 → M3 → L3 → L5 → L4 → L6 → M3".
- M1 is deprecated and MUST NOT be used (T02:1038-1049).
- M2 applicability (T02:1051-1061): code-modifying tasks gate after implementation and before testing (or after combined implement+test); document-creation tasks get M3 + M4. "When in doubt, include a gate" (T02:1059).
- **M3 steps (T02:1063-1100):** 1 aggregation; 2 structural-lens rf-qa agents (report `${TASK_DIR}qa/qa-structural-[lens]-report.md`); 3 content-lens rf-qa-qualitative agents (`${TASK_DIR}qa/qa-content-[lens]-report.md`); steps 2 and 3 may share one parallel batch (T02:1084); 4 domain lenses; 5 consolidation `${TASK_DIR}qa/qa-consolidated-findings.md`; 6 ONE fix agent; 7 at least 2 verifiers → `qa-verification-structural-report.md` / `qa-verification-content-report.md`; 8 conditional proceed, max 2 cycles. EVERY step is an explicit item; steps MUST NOT be collapsed (T02:1100).
- **M4 steps (T02:1102-1125):** 1 source identification (explicit, not discovered); 2 at least 2 fidelity agents → `${TASK_DIR}qa/qa-source-fidelity-report-[N].md`; 3 cross-source contradiction agent (reads sources only) → `qa-cross-source-contradictions-report.md`; 4 consolidation → `qa-fidelity-consolidated-findings.md`; 5 one fidelity fix agent; 6 at least 2 verifiers, max 2 cycles.
- **Report-path collision risk:** the M3/M4 default report names are fixed (`qa-consolidated-findings.md`, `qa-verification-*-report.md`). With three design-fix gates, an implementation gate and a final gate in one task, the builder MUST give each gate its own path prefix (for example `qa/r3-b1/`, `qa/impl/`, `qa/post/`), or later gates overwrite earlier evidence. This is an inference from T02:1073-1092; the template does not state it.
- The PART 2 phase-gate skeleton (T02:1369-1406) shows the expected per-agent item shape: PG.1 aggregate; PG.2 structural x4; PG.3 content x4; PG.4 consolidate + fix; PG.5 verify x2 + conditional; PG.6 fidelity x2 + contradictions + consolidate + fix + verify + conditional.

## 7. Execution Context section (T02:1197-1235, TB:1072-1077, TB:1243, TB:1401)

- Required in every generated file, immediately after Prerequisites & Dependencies (T02:1199, TB:1072, TB:1243).
- Three subsections (T02:1201-1211): References (`- [Doc](path): purpose`), Source Areas (`- path/: why`), Key Constraints (QA intensity, scope limits, blockers, prohibitions).
- TB:1073-1077 tightens this: References = BUILD_REQUEST GOAL verbatim + WHY + related-doc IDs; Source areas = named modules, **NEVER specific file:line paths**; Key constraints = top 1-3 invariants. TB-Add-7 (TB:1401, TB:2310): every Source-areas entry must reappear in at least one item's Context, and the block contains no file:line citations.
- T02 PART 2 also places "Handoff File Convention" and "Frontmatter Update Protocol" subsections inside Execution Context (T02:1213-1235).

## 8. Anti-orphaning and completion (TB:2363, T02:1427-1445)

- **TB Rule 15 (TB:2363):** completion items (status → Done, task summary) MUST be inside the final phase, "never in a separate Post-Completion section". Downstream offers come after the completion items and are marked `NON-BLOCKING`. Validation line: TB:2298.
- **Conflict:** T02 PART 2 puts these items in a separate `## Post-Completion Actions` section (T02:1427-1445), and I13/I17 name that section (T02:616-621, T02:688). TB is the stricter rule and is what TB's validators check, so put the post-completion QA, the test re-run, the Task Summary, POST reflect and Update-to-Done inside a final numbered phase (for example "Phase N: Final Validation and Completion").
- TB final-phase order (TB:2215-2260): ... → `N.{X-1}` POST reflect (penultimate) → `N.X` Update task status to Done (last).

## 9. How to encode a human-gated item so `/task` cannot invent an owner decision

**Neither T02 nor TB has a dedicated human-gate pattern.** T02 PART 1 has no rule for it (grep of T02 for human/owner/manual finds only "escalate to the user" at QA cycle caps, T02:657-1123). The relevant rules, and why the defaults are dangerous:

- `/task` default error handling: "If unrecoverable ... mark the item `- [x]` with a note in Task Log ... then continue to next item. Items are NEVER left unchecked" (`~/.claude/skills/task/SKILL.md:183`), matching T02 J1/J2 (T02:854-865). An owner-decision item written with the standard J1 clause WILL be ticked and passed.
- `/task` may stop only "If ALL remaining items are blocked by the same issue" (`~/.claude/skills/task/SKILL.md:184`); TB Rule 19 (TB:2371) allows halts only for that case, QA cap exhaustion, or an output that invalidates the rest of the task. A human gate must therefore state, in its own text, that every later implementation item depends on it, so the HALT is a permitted halt and not a "scope pause".
- TB Rule 6 (TB:2345): uncertainty and judgment go in `### Open Questions`. TB-Add-3 (TB:1397, TB:2306): "each blocked item references its blocking Open Question by index in Context". TCS S5 (TB:2416) counts `OQ-\d+` tokens that appear in an item's Context AND have a matching `### Open Questions` entry (weight ×5), and override O1 floors POST depth at `standard` when S5 > 0 (TB:2439).

**Recommended encoding (built from the two prior examples below):**

1. Give each owner decision an `OQ-N` ID and list it under `### Open Questions` in Execution Context, tagged `needs_human_decision`, with the options and the non-binding recommendation (example: detection-contract task, lines 143-146 of `.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/TASK-RF-detection-contract-20260701-164700.md`).
2. Use TWO items per decision (pattern from `.dev/tasks/to-do/TASK-RF-reflect-d1d4-fix-20260623-192000/TASK-RF-reflect-d1d4-fix-20260623-192000.md:192-202`):
   - **Record item:** write a decision file under `phase-outputs/plans/OQ-N-<slug>-decision.md` with `needs_human_decision: true`, `status: PENDING`, the options verbatim, a recommendation explicitly labelled "does NOT authorize adoption", and an empty `OPERATOR DECISION:` / `Chosen:` / `Decided by:` block (d1d4:196). The phase banner says "YOU MUST NOT auto-pick a design, and YOU MUST NOT ship a default" (d1d4:194).
   - **HALT gate item (L5 with both branches):** read the decision file; IF `Chosen` is empty or `status` is PENDING → set frontmatter `status` to "⚪ Blocked", fill `blocker_reason`, log a HALT note, "then STOP execution of this task (do NOT mark any further items, do NOT auto-select a design)" and do NOT tick this item; IF resolved → record which option and by whom, reset `status` to "🟠 Doing", tick the item (d1d4:200-202).
3. Override the J1 clause explicitly. Replace "log the blocker ... then mark this item complete" with "log the blocker ... then stop before marking this item complete until the blocker is resolved" (detection-contract:176-184 uses exactly this).
4. Require the decision SOURCE to be recorded. The detection-contract run's decision file says "Decision source: user selected Package (Recommended) during the Step 1.3 human-decision gate." (`.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/phase-outputs/plans/OQ-1-helper-granularity-decision.md`, "Decision source" line). That item's text did not require it (detection-contract:176). Require it, and say that a recommended default is never a decision ("no recommended default is treated as approved unless the decision file says so", detection-contract:188).
5. Every dependent item's Context cites the gating `OQ-N` (TB-Add-3) and reads the decision file before acting.
6. A short decision-integrity QA gate after the decision items is good practice: the detection-contract task gated Phase 1 with "lens: decision-gate-structure", adversarial framing "find every case where a dependent phase could proceed without a non-PENDING decision" and FAIL "if ... any default is silently auto-applied" (detection-contract:192).

**Mapping to Phase 1 human/live gates:**

- **Step 1.0b (owner decisions):** use the OQ-N record + HALT pattern above, one pair per decision.
- **Step 1.0a (read-only Orca capture against an existing Run, allowlisted verbs only):** this is an L1 discovery item, not an owner decision, but it needs a live Run that may not exist. Encode it as: list the exact allowlisted command strings in the item (no other verb permitted; state this as a "MUST NOT run any other orca verb" clause), write raw output to `phase-outputs/discovery/` plus a summary (L1 + L3 shape, T02:932-966), and an L5 branch: IF no Run is available or a verb outside the allowlist would be needed → write `status: PENDING` and HALT as above (do not substitute a fixture or invent output); IF captured → proceed. Which verbs are allowlisted is the integration researcher's topic (not covered here).
- **Step 1.16a (gh PR check):** an L3 item with the exact command spelled with `--repo IronbellyOrg/IronClaude` (project CLAUDE.md fork rule), raw output + summary, and an L5 branch for the not-merged / not-found case that HALTs instead of guessing.

## 10. How to encode a QA gate as `- [ ]` items with embedded prompts (examples)

Two recent code-plus-tests task files, both `🟢 Done`:

- **E1:** `.dev/tasks/to-do/TASK-RF-t2-fallback-ladder-20260706-050832/TASK-RF-t2-fallback-ladder-20260706-050832.md` (628 lines, `reflect_post_mode: cli` at line 45). Per-phase "lighter intermediate gate — standard intensity" (line 238): Steps 1.G1 aggregate → 1.G2 rf-analyst completeness → 1.G3 rf-qa evidence/anchor-fidelity → 1.G4 rf-qa-qualitative test-actionability → 1.G5 consolidate → 1.G6 single fix agent (L5: IF PASS write "no fixes needed", IF FAIL spawn ONE `rf-qa` `fix_authorization: true`) → 1.G7 verification of 2 agents + re-run tests + conditional proceed, max 2 cycles, then a PENDING Open Questions entry and HALT (lines 240-259). **One `- [ ]` item per agent** (for example line 244: one rf-analyst, `fix_authorization: false`, input files, design sections, adversarial framing "Assume Phase 1 is missing at least 5 required elements focused on completeness. Find them.", report `qa/qa-phase1-completeness-report.md`, "does NOT modify any source file"). This is the shape M3 asks for (T02:1100).
- E1 also opens with an **anti-drift gate**, Step 1.3 "Re-verify live code anchors" (line 196-197): read the current state of every seam the research cited and confirm it is still present before editing. Useful before Phase 1 step 1.1, since design §15 line references can drift.
- E1 test items (line 221 test-file creation; line 233 L3 run with `uv run pytest ... -v 2>&1`, raw + summary, fix-and-rerun loop, "UV-only — never `python -m`").
- **E2:** `.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/TASK-RF-detection-contract-20260701-164700.md` (686 lines). Phase 4 gate and the Phase 5 final gate (lines 360-432) show the full serialized sequence as separate items: lens spawns → consolidate → fix/no-fix decision item → single fix agent → structural verifier → content verifier → conditional proceed. Final phase (lines 378-444): aggregate inventory → final pytest → ruff → `make verify-sync` → combined verdict → M3 final gate → M4 fidelity gate (2 agents partitioned by source sections, lines 420) → Task Summary → POST reflect → Done. This satisfies anti-orphaning (all inside Phase 5).

**Do NOT copy these points from E1/E2 (they predate current rules):**

- Both consolidate with "FAIL if ANY report contains ANY issue of any severity" (E1 line 253; E2 lines 196, 366, 406, 422). Current I16 says minor findings never fail a review (T02:655-656) and I20 spawns no fix agent for a minors-only list (T02:755). Use the current rule.
- E2 spawns three or six lens agents from ONE `- [ ]` item (E2 lines 362, 364, 404). I15/M3 want each lens spawn as its own item (T02:651, T02:1100); E1's one-item-per-agent form is the compliant one.
- E2 has no `reflect_post_mode` key; both are CLI mode (E1 line 45; E2 lines 83-84 `start_commit`/`executor_model_class`). Phase 1 here uses skill mode (per the BUILD_REQUEST topic), so their POST items are not the right form.

## 11. "Fix a design document, then gate it" — prior art

- No prior RF task file found that edits a `docs/designs/` file and immediately gates it. Closest is E-d1d4 (`.dev/tasks/to-do/TASK-RF-reflect-d1d4-fix-20260623-192000/TASK-RF-reflect-d1d4-fix-20260623-192000.md`): Phase 4 "D3 Citation Fix (reflect-reviewer.md) + Sync" (lines 224-232) edits a document, and its Step 4.1 (line 228) starts with "**D3 PREMISE RE-VERIFICATION FIRST (the research premise is stale — verify ground truth before editing)**" and branches on what is actually on disk. The gate for that edit only runs later, at PG (lines 256-290), not right after the edit.
- Recommended shape for each of R3-B1, R3-B2, R3-B3 (inference from T02 L2/L4/M3/M4 + the d1d4 premise check):
  1. **Edit item (L2):** context = the R3 finding text + the exact `docs/designs/orchestrator-mode.md` section + the code it describes (file:line); first re-verify the finding still applies; then edit only that section; output = the edited doc plus a short change note in `phase-outputs/reports/r3-bN-change.md` (before/after text); ensuring nothing outside the named section changes.
  2. **Gate items (M3 + M4, one `- [ ]` per agent, unique report prefix `qa/r3-bN/`):** at standard intensity, 3 structural + 3 content + 1 domain-accuracy lens (design claim vs code) = 7 (I22, T02:831); then consolidate → single fix agent (if blocking) → 2 verifiers → L5 conditional; then M4 with 2 fidelity agents comparing the edited section against the R3 finding and the code (T02:1110-1123). Lenses should review the edited section and its cross-references, not the whole design doc, to keep the adversarial N and the agent load proportionate (the design doc size decides N per T02:733; Unverified current line count, researcher 4 covers the doc).
  3. Order: B1 edit → B1 gate → B2 edit → B2 gate → B3 edit → B3 gate, all before step 1.1 (top-to-bottom rule, T02:367-382). Three gates in a row on one file are serialized by design (I20 forbids parallel fix agents on one file, T02:750).

## 12. Skill-mode POST reflect item (TB:2215-2235, Rule 20 TB:2373, validation TB:2312)

Header (exact): `- [ ] **N.{X-1} - Independent post-execution reflection gate (a dedicated subagent runs /sc:reflect --mode post end-to-end)**` (TB:2219). Emit exactly one of the two arms, never both (TB:2217).

Required parts:

1. **Position:** penultimate item of the final phase, immediately before "Update task status to Done" (TB:2373, TB:2312).
2. **Context** (TB:2220): all implementation/test/QA above complete; inline rf-qa ran in the executor's frame; independent ensemble catches blind spots; run by a DEDICATED SUBAGENT; the disclosure that skill-mode nesting is expected but not session-validated (prefer `--cli` for mission-critical builds).
3. **Action** (TB:2221): spawn EXACTLY ONE subagent via the Agent tool (`subagent_type: general-purpose`, `mode: bypassPermissions`) and pass the COMPLETE prompt VERBATIM, no paraphrase/summary/reorder/omission.
4. **Verbatim runner prompt** (TB:2223-2231), 5 numbered steps + COMPLETION CONTRACT: (1) `Skill(skill: "sc-reflect-protocol", args: "--mode post --remediate --diff {BASE}..HEAD --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --depth {DEPTH} --output {OUTPUT_DIR}")`, and do NOT pass `--executor-model`; (2) let the skill run its full pipeline for whatever tier it resolves: Tier 2 = Wave 3 ensemble, 3C blind calibration, 4 adversarial merge, 5 evidence-validator; Tier 1 = grounding + reflection card + Wave 1D calibration; (3) classify under Authorized / Necessary / Drift / Regression; apply `--remediate` fixes; unresolved Regression or unauthorized Drift → HALT and escalate to the user; only Authorized/Necessary/minor go to `### Open Questions` as notes; (4) persist all artifacts under {OUTPUT_DIR}; (5) return exactly verdict (PASS | PASS-with-deviations | FAIL), `run_id`, absolute report path, resolved tier, one-line waves-attestation. COMPLETION CONTRACT: a partial run, a self-assembled panel, a synthesized verdict, a skipped calibration/merge/evidence gate, or a Tier-1-only run when Tier 2 was eligible are each explicit non-satisfaction; else return `RUN_INCOMPLETE`.
5. **Output** (TB:2233): record `{verdict, run_id, report}` into frontmatter `reflect_post`.
6. **Verification** (TB:2234): `reflect_post` non-empty; waves attestation matches tier; deviations remediated or HALTed. **EV-3 on-disk check:** the executor itself reads `{OUTPUT_DIR}/adversarial/merged-verdict.yaml` (must exist with `merge_method: adversarial`) and `{OUTPUT_DIR}/reviewer-cards/` (at least the `--reviewers` count, min 2), or confirms the loud fallback (`adversarial_unavailable: true` + `merge_method: single-reviewer-fallback` + an F-step in audit.log). If MALFORMED, re-spawn up to 2 more times, then HALT.
7. **Completion gate** (TB:2235): full run done; `--depth` equals the TCS-derived `post_depth` (floored at `standard`, never `quick`); `tier_reached` is at least the band floor (the `deep` band, TCS >= 35, requires Tier 2); EV-3 passed; THEN Update-to-Done.
8. **MALFORMED if** (TB:2312): omitted; direct self-run form; paraphrased or abbreviated prompt; no completion contract; passes `--executor-model`; halts for a human. Frontmatter: `reflect_post_mode: skill` and NO `start_commit`/`executor_model_class` (TB:2314).

Phase 1 placeholders to fill: `{TASK_FILE}` = absolute task path; `{SPEC_PATH}` = `docs/designs/orchestrator-mode.md` (absolute); `{DEPTH}` = TCS-derived (TCS formula, bands and overrides at TB:2404-2440; a 28-step multi-file task with OQ items will very likely score >= 35 → `deep`, Unverified until computed); `{OUTPUT_DIR}` = `<task-dir>/reflect/post/`; `{BASE}` = the commit before Phase 1 work.

**Risk:** the skill arm audits `--diff {BASE}..HEAD`, a commit range, so uncommitted Phase 1 edits are NOT in that diff (the CLI arm instead diffs a single ref against the working tree, TB:2239). The builder must either add a commit item before the POST gate (needs user authorization under the repo's "commit only when asked" rule), or say how reflect sees uncommitted work. The recent skill-mode example (`.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:362`) avoided this by dropping `--diff` and passing an explicit file list, but it also paraphrased the runner prompt, which TB:2312 calls MALFORMED. Do not copy that example's prompt.

---

## Summary

- **Template rules the builder must follow:** one `- [ ]` per atomic action (A3/A4); every item self-contained with context, action, output, "ensuring" verification, failure logging and a completion gate (B2); every QA step its own item (I15, M3, I20); fidelity gate after M3 because Phase 1 code and design fixes are derived from source documents (I21, M2); intensity counts per I22 (standard: 7 per final gate, 2 fidelity, 2 verifiers, 2 fix cycles); minor findings never fail a gate (I16).
- **Conflicts the builder must resolve:** single-paragraph items (T02 B3) vs the 5-field form (TB:2203-2208, which TB validators check); separate `## Post-Completion Actions` (T02:1427) vs anti-orphaning in the final phase (TB:2363), so follow TB; fixed QA report names, so give each gate its own `qa/<gate>/` prefix; "⚪ Blocked" vs "🔴 Blocked".
- **Human gates:** the default `/task` and J1 behavior ticks a blocked item and moves on (`task/SKILL.md:183`, T02:854-865). Encode each owner decision as an `OQ-N` Open Question, then a PENDING record item, then an L5 HALT gate item that sets Blocked and stops without ticking (d1d4:192-202), with the J1 clause overridden ("stop before marking this item complete"), the decision source recorded, and every dependent item citing the OQ ID (TB-Add-3). Live gates (1.0a Orca capture, 1.16a gh check) are L1/L3 items with literal commands and an L5 HALT branch, never a fixture.
- **POST reflect:** skill-mode dedicated-subagent form, verbatim prompt TB:2223-2231, penultimate, EV-3 on-disk check, depth from TCS. Risk: `--diff {BASE}..HEAD` misses uncommitted work.
- **Best examples:** E1 t2-fallback (one item per lens agent, anti-drift anchor check, L3 tests) and E2 detection-contract (decision gates, full final phase). Do not copy their "any severity fails" consolidation or E2's multi-agent single items.


