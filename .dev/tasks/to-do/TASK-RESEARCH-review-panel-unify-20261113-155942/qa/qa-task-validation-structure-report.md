# QA Report — Task Integrity (Lens: phase-structure)

**Topic:** Review Panel unification research task (E1/E2/E3)
**Date:** 2026-11-13
**Phase:** task-integrity
**Fix cycle:** N/A
**fix_authorization:** false

**Inputs read:** task file (578 lines, 104 `- [ ]` items, read by outline plus full reads of lines 1-175, 206-302, 462-578 and targeted lines 304-460); BUILD-REQUEST.md (full); MDTM template 02 (PART 2 lines 1157-1520, I11-I22 lines 600-800, C4/D lines 225-292, E1-E4 lines 295-394, M3/M4 lines 1063-1126); tech-research SKILL.md A.7 Phase 6 (lines 520-589); anti-orphaning convention (operational-guide SKILL.md:431, :1363; tdd SKILL.md:408).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete and well-formed | PASS | Lines 1-62. Every field of template 02 frontmatter (template lines 1-61) is present: id, title, description, status "🟡 To Do", type, priority, created_date, updated_date, assigned_to, autogen, coordinator, parent_doc, depends_on, spec_path, reflect_pre block, reflect_post, related_docs, tags, template_schema_doc, dates, review_info, task_type. The rf-qa checklist names `created`/`template`/`tracks`; template 02 has none of these (it uses `created_date`, `template_schema_doc`), so the file follows the template. `task_type: dynamic` is justified by the dynamic sub-checklist. |
| 1b | Owner rule: `reflect_post_mode: skill`, no start_commit / executor_model_class | PASS | Line 28 `reflect_post_mode: skill`; Bash grep for `start_commit|executor_model_class` returned no match. |
| 2 | Mandatory template sections present | PASS (notes) | Present: Task Overview (66), Key Objectives (72), Prerequisites & Dependencies with Parent Task (85) and Previous Stage Outputs (92), Execution Context with References/Source Areas/Key Constraints/Handoff File Convention/Frontmatter Update Protocol (106-153), Detailed Task Instructions (155), Phase 1 (157), Task-Specific Context Files (169), Task Log with Task Summary, Execution Log, per-phase Findings, Phase Gate Findings, Follow-Up Items, Deviations (462-577). `## Post-Completion Actions` (template I13, line 616) is absent by design: completion items sit in Phase 7 per the anti-orphaning convention (operational-guide SKILL.md:1363, tdd build-request-template.md:56). No reference to `anti_hallucination_task_completion_rules.md` (template I14; grep count 0) — see minor note N6. |
| 3 | Phase dependencies; Phase 5 order synth-01/02/03/04/07 parallel -> adversarial -> synth-05 -> synth-06 -> gate | PASS for phase order; FAIL at item level (B1) | Line 274 states the owner order; Step 5.1 items 278-286 (synth-01, 02, 03, 04, 07), Step 5.2 items 290/292/294 (enumerate, process, verify-no-`pending`), Step 5.3 item 298 (synth-05 reads synth-04 and debate results first), Step 5.4 item 302 (synth-06 reads synth-04 and synth-05), Step 5.5 gate 308-326, Step 5.6 330-338. Matches BUILD-REQUEST lines 41-43. Item-level data-flow defect between synth-02 and synth-06: see B1. |
| 4 | Phase ordering follows logical progression | PASS | 1 Prep -> 2 Investigation (12) -> 3 Research gate -> 4 Web (4) -> 5 Synthesis + adversarial + gate -> 6 Assembly, report gate, fidelity (6.7), anti-omission (6.7b), final checklist (6.8) -> 7 Present/complete. Matches BUILD-REQUEST lines 117-179 and SKILL.md A.7. |
| 5 | Task completion items inside final phase (anti-orphaning) | PASS | Phase 7 holds 7.1 Glob/hash (446), 7.2 present (450), 7.3 `git add .dev/tasks` (454), 7.4 Task Summary + next step (458), frontmatter Done (460). Total checkbox count 104 equals the count inside Phases 1-7; no checkbox in the Task Log. |
| 6 | Task Log section at bottom | PASS | Lines 462-577 with all template subsections plus Phase 5 Adversarial Sub-Checklist (531) and Open Questions table (492). |
| 7 | Item count reasonable | PASS | 104 items: P1 2, P2 13, P3 17, P4 5, P5 25, P6 37, P7 5. Headers match counts (Phase 2 "12", Phase 3 "10 report-only agents", Phase 4 "4", Phase 6 "13 lens agents", fidelity 4, anti-omission 4). Deep tier with full-intensity gates and 2x partitioning justifies the size. |
| 8 | Open Questions and remaining gaps documented | PASS | Table at lines 494-504 (7 rows, assumption and destination per row); Step 3.3 item 250 builds `gaps-and-questions.md`; synth-07 (286) carries them to Section 9. |
| 9 | QA gates follow M3 / M4; anti-omission 6.7b present | PASS (notes) | Each gate: report-only lens agents -> consolidation -> one fix agent -> 2 verifiers -> decision item with regression -> monotonicity -> hard-cap order (246, 338, 396, 416, 436). Research and synthesis gates use I19 intermediate types 2+2+1 partitioned x2 (212, 306). Report gate 5+5+3 = 13 (342), fidelity 4 rf-qa (400-408), anti-omission 4 rf-analyst (420-428). M4 Step 3 cross-source agent omitted; documented in Deviations (556-559) — note N4. M3 Step 1 aggregation: 6.1 assembler + 348 measure item serve as aggregation. |
| 10 | TB-Add-1: no TBD/TODO/FIXME, no title-only items | PASS | Grep `\b(TBD|TODO|FIXME)\b` hits only lines 320, 322, 346, 354, where the tokens are search targets in "search for `TODO`, `TBD`" instructions. Shortest item is 807 chars (460); every item has the completion gate (104/104). |
| 11 | TB-Add-3: blocked items reference Open Question index | PASS | Line 494: "None blocks this run"; no item is blocked on an open question. |
| 12 | TB-Add-4: item dependencies form a DAG | PASS (notes) | No data-dependency cycle. Backward edges are bounded fix-cycle re-entries sanctioned by template PG.5 / I16. Forward references: 292 processes Task Log entries created by 290 (BUILD-REQUEST-mandated); 454 cites Step 7.4 informationally; 242 pairs with the next item for one-message spawn. One unbounded re-entry path: see B2. |
| 13 | TB-Add-5: XL / multi-file items split or justified | PASS (note) | Spawn items run 3.2-9.4 KB because B2 and BUILD-REQUEST line 125 require the full embedded prompt; each still spawns one agent writing one file. Multi-action items 167 (verify + mkdir + fetch + 3 checks), 290 (index + sub-checklist), 440 (checklist + sha256) carry no justification comment — note N3. |
| 14 | TB-Add-6: uniform verification / acceptance format | PASS (note) | Template 02 uses the "ensuring ..." clause, not `Verify:`. 97/104 items contain "ensuring"; 246, 450, 458 use "Ensure/ensure"; 396, 410, 416, 436 embed the check in IF/record wording. Completion gate present 104/104; failure-logging clause 103/104 (460 has a HALT branch instead). Note N5. |
| 15 | TB-Add-7: Source areas reappear in items; block has no file:line | Coverage PASS; file:line FAIL (minor) | All 9 Source Areas bullets (115-124) reappear in item bodies (grep counts: `src/superclaude/cli/review/` 13, `sc-reflect-protocol` 10, `git show 4a22d742` 23, `shadow-model-combos` 4, `spec-panel.md` 3, `sc-review-ledger` 4, `diffgate` 2, `fix-audit` 1, `sc-workflow-protocol` 3, `sc-pr-submit-protocol` 2, `agents/rf-qa.md` 3, `tests/cli/reflect` 5, `test_spec_panel_review_loop.py` 3, Stage 0-2 artifacts `TASK-WF-implementStages0` in 186/202/406). But Key Constraints line 131 contains `telemetry.py:22`, `panel.py:536-543`, `panel.py:485-494` inside the Execution Context block — note N1. |
| 16 | TB-Add-8: per-item Context with code surface has file:line or evidence-absence | FAIL (minor) | Only 7 items match a `name.ext:NN` pattern (184, 186, 192, 200, 216, 320, 346; 182 also has `findings_v2.py:3`). Phase 2 items 188, 190, 194, 196, 198, 202, 204 name code files (e.g. 188: `src/superclaude/cli/review/panel.py`, `panel_cmd.py`; 194: `src/superclaude/cli/reflect/contract.py`, `panel_lint.py`) with no file:line and no `<!-- evidence-absence -->` (grep count 0). These are L1 discovery items whose agents read the scope slices holding file:line evidence first, so this is citation format — note N2. |
| 17 | Owner scope: no /sc:workflow item, no roadmap item, no c2ddeb1b4 / run-2 hand-off | PASS (note) | No item runs `/sc:workflow` or builds a roadmap; 450 and 458 forbid both; 302 forbids roadmap content. `c2ddeb1b4` grep: no match. "run-2 hand-off" appears only as an exclusion guard (216, 218: "a reference ... to a run-2 hand-off is blocking"; 430: "run-2 material excluded"; 503). Note N7. |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| B1 | IMPORTANT (blocking) | Step 5.1 item line 280 (synth-02) and Step 5.4 item line 302 (synth-06) | Item-level data-flow defect. synth-02 runs in Step 5.1 and is told to record each unwired in-scope capability as Critical and "link it to the Section 8 migration step that wires it". Section 8 is synth-06, written later in Step 5.4, and synth-02's prompt does not give it the track names (M1-M4 exist only in the synth-06 prompt). So synth-02 cannot execute this instruction without inventing a forward reference. The reverse link is also missing: synth-06's "Research files to read" lists synth-04, synth-05, research files and scope slices, but not synth-02 or `gaps-and-questions.md`, so nothing makes Section 8 cover every Section 4 gap. The SKILL synthesis checklist item 7 ("every gap in Section 4 has a step in Section 8") cannot be checked by the synthesis gate either, because synth-02 (partition 1) and synth-06 (partition 2) are in different partitions (line 306). The first check that sees it is the assembler cross-check (346). | (1) In 280, replace "link it to the Section 8 migration step that wires it" with "tag it with the migration track that will wire it (Track M1 reflect shadow, M2 tasklist panel, M3 spec-panel / brainstorm / design, M4 PR review and rf-qa hooks); the exact step is assigned by synth-06". (2) In 302, add `${TASK_DIR}synthesis/synth-02-target-gaps.md` and `${TASK_DIR}gaps-and-questions.md` to the inputs, with the rule "every Section 4 gap of severity Critical or Important maps to a step in 8.2 or a row in 8.1 with DROP reason; list unmapped gaps for Section 9". |
| B2 | IMPORTANT (blocking) | Step 6.8 item line 440; Step 7.1 item line 446 | Unbounded re-entry that skips mandatory gates. A `no` on a required-content row "sends the task back to Step 6.5 for one more report-gate cycle". That fix runs after the fidelity gate (6.7) and the anti-omission gate (6.7b) have passed. The item does not say whether 6.7, 6.7b and 6.8 run again, so the item cannot be executed deterministically. Read literally, the report ships with Gate 4 and Gate 5 results that describe an earlier version. BUILD-REQUEST line 68 says the anti-omission gate is "never skipped". Step 7.1 has the same gap: if the hash differs from the 6.8 hash, it re-runs only the two Step 6.6 verifiers, although its own reason says "the Phase 6 gates ... are only valid if the report has not changed since". | In 440, state the full re-entry path: after the extra 6.5/6.6 cycle, re-run Step 6.7 (fidelity) and Step 6.7b (anti-omission), each counting against its own cap, then re-run 6.8 and record a new hash. In 446, if the hash differs, re-run Steps 6.6, 6.7 and 6.7b (or HALT and escalate), not only the 6.6 verifiers. |

### Minor notes (do not fail the review)

| # | Location | Note |
|---|----------|------|
| N1 | Execution Context, Key Constraints line 131 | The block contains `telemetry.py:22`, `panel.py:536-543`, `panel.py:485-494`. TB-Add-7 says the header must hold no file:line references; per-item Contexts are the right place (items 216/218 already repeat them). Replace them with "moved D7/D11/D12 line numbers (see scope slice 02)". |
| N2 | Phase 2 items 188, 190, 194, 196, 198, 202, 204 | Code files are named without file:line or `<!-- evidence-absence: discovery item; file:line evidence lives in research/scope/0N -->`. Add the absence comment, or the anchor lines from the scope slices. |
| N3 | Items 167, 290, 440 | Each is a multi-action item with no justification comment for keeping it as one item (TB-Add-5). A one-line justification is enough; splitting is not required. |
| N4 | Step 6.7 (400-408) | There is no M4 Step 3 cross-source contradiction agent. This deviation is recorded with a reason at lines 556-559 (it follows SKILL.md A.7, line 557-561). Accepted. |
| N5 | Items 246, 396, 410, 416, 436, 450, 458 | The verification wording varies ("Ensure", IF/record) instead of the "ensuring ..." clause used by the other 97 items. |
| N6 | Whole file | Template I14 requires a reference to `~/.claude/rules/core/anti_hallucination_task_completion_rules.md`; none is present. Every agent prompt does embed no-fabrication rules, so the intent is met. |
| N7 | Items 216, 218, 430; Open Questions row 6 | The text "run-2 hand-off" appears, but only as an exclusion guard. This does not use run-2 material as input. Rewording to "any later hand-off" would remove even the literal mention. |
| N8 | Step 3.2 decision item line 246 | It says "re-executing the five Step 3.2 items above ... and then this item again". Only four Step 3.2 items come before it (238, 240, 242, 244). Phase 5 (338) correctly says "four". |
| N9 | Step 5.1 synth-07 (286) vs Step 5.2/5.3 | synth-07 writes Section 9 before the adversarial step. A conflict whose debate fails becomes an open question in synth-05 (294), but Section 9 is never updated. The assembler's S9 cross-check (346) is the only catch. Add to 294: "append any `debate failed` conflict to synth-07 Section 9". |
| N10 | Item 292 / Task Log 531 | The dynamic sub-checklist puts `- [ ]` entries below Phase 7 (E1: "never reference checkboxes that appear later"). The BUILD-REQUEST (line 42) mandates this, so it is accepted. |

---

## Summary
- Checks passed: 15 / 17 (16 lens checks plus the owner-scope check; 2 checks fail on blocking item-level defects: #3 via B1 and #12 via B2)
- Checks failed (blocking): 2 (B1, B2)
- Checks with minor-only notes: #15 and #16 FAIL as citation format (minor); N1-N10 are notes
- Critical issues: 0; Important (blocking): 2; Minor: 10
- Issues fixed in-place: 0 (fix_authorization: false)

## Confidence Gate
- **Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep: 4 | Glob: 0 | Bash: 9 (all read-only inspections). No web research was performed.
- Limits: the long Phase 2-6 agent prompts were checked for structure, inputs, outputs and ordering, not proofread word by word. Content accuracy of the embedded prompts belongs to the other lenses.

## Recommendations
- Fix B1 and B2 in the task file (both are prompt-text edits to items 280, 302, 440 and 446), then re-run this structure lens on those four items only.
- Apply N1, N8 and N9 in the same pass; they are one-line edits.

VERDICT: FAIL

Blocking issues: B1 (IMPORTANT, synth-02 -> synth-06 gap-to-plan data flow), B2 (IMPORTANT, Step 6.8 / 7.1 re-entry skips the fidelity and anti-omission gates).

## QA Complete

