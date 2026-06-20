# Research 04: Template & Examples (R4)

Status: In Progress

Focus: MDTM Template 02 PART 1 mechanics + one recent TASK-RF example's structural patterns, so the generated tasklist (replace /sc:forensic with /sc:troubleshoot in TFEP) is conformant.

Source template: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md`

---

## PART A: Template 02 PART 1 rules (with line refs)

### Frontmatter (required fields) — lines 1-61
The template frontmatter block (lines 1-61) defines these fields:
- `id` (L2): `"TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"`
- `title` (L3), `description` (L4), `version` (L5)
- `status` (L7): one of `🔵 Backlog | 🟡 To Do | 🟠 Doing | 🔴 Blocked | 🟢 Done | ⚪ Cancelled` (option list L6). Default `"🟡 To Do"`.
- `type` (L9): from option list L8 (e.g. `📚 Documentation`, `⚙️ Process Improvement`, `🛠️ Tooling/Automation`). For this docs/skill-edit migration, `📚 Documentation` or `⚙️ Process Improvement` fit.
- `priority` (L11): from L10 list.
- `created_date` (L12), `updated_date` (L13), `assigned_to` (L14)
- `autogen` (L15), `autogen_method` (L16), `coordinator` (L17, `orchestrator`)
- `parent_doc` (L18), `parent_task` (L19)
- `depends_on` (L20-22): list
- `spec_path` (L23): driving spec/PRD/TDD path; populated by task-builder (A.2), empty if none
- `reflect_pre` (L24-31): PRE reflect-gate sign-off block — `verdict` (pass|fail|skipped), `coverage_pct`, `depth` (quick|standard|deep), `tcs`, `run_id`, `report`, `reviewed_at`. Populated by task-builder at A.10.7.
- `reflect_post` (L32): POST reflect verdict; recorded by executor after final-phase reflect subagent runs.
- `related_docs` (L33-39): list of {path, description}
- `related_prd` (L40), `related_tdd` (L41)
- `tags` (L42-46): list
- `template_schema_doc` (L47), `estimation` (L48), `sprint` (L49), `due_date` (L50), `start_date` (L51), `completion_date` (L52), `blocker_reason` (L53)
- `ai_model` (L54), `model_settings` (L55)
- `review_info` (L56-59): {last_reviewed_by, last_review_date, next_review_date}
- `task_type` (L60): `static` (vs `dynamic` per I6, L548-549)

Key for a docs task with no driving spec: `spec_path: ""`, `task_type: static`, `type: "📚 Documentation"`.

### Rule A3 — COMPLETE GRANULAR BREAKDOWN (lines 108-112)
- Break down EVERY workflow phase into atomic, verifiable checklist items.
- Create individual checklist items for EVERY file, component, or iteration.
- NO high-level or bulk operations allowed — everything granular.
- Include exact file paths, specific requirements, measurable outcomes.
(Supporting A4 iterative pattern L114-133: pre-enumerate all items, one item each, consolidate after.)

### Rule B2 — SELF-CONTAINED CHECKLIST ITEM (lines 159-166) — the 5/6-field item format
Every checklist item MUST be a complete, self-contained prompt including:
1. **Context Reference with WHY** (L160) — what file(s) to read and why for this action
2. **Action with WHY** (L161) — what to do and why
3. **Output Specification** (L162) — exact output file name, location, content, template to follow
4. **Integrated Verification** (L163) — an "ensuring..." clause; DO NOT assume/hallucinate; 100% accuracy from source; document negative evidence on failure
5. **Evidence on Failure Only** (L164) — log to task notes ONLY if blocked/missing-info/error (success evidenced by the output file itself)
6. **Explicit Completion Gate** (L165) — "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."

Pattern notes (B3 L167-170): ONE FULL PARAGRAPH, verbose, reads like an independently-executable prompt. Worked example at L172-175 (B4). Verification integrated via "ensuring..." clause, NOT separate items (L177-179, C3 L236-240, I12 L609-614).

FORBIDDEN (B5 L181-200): standalone "read context" items, missing context reference, multi-line/bulleted items, separate verification items, overly granular items, separate REMINDER blocks.

### Anti-orphaning / checklist structure (Section E, lines 292-405)
- E1 (L295-309): every actionable item is a flat `- [ ]` checkbox; NO nested checkboxes; NO parent checkboxes summarizing children; use `**Step X.Y:**` headers for grouping.
- E2 (L311-358) FUNDAMENTAL RULE: summary/parent checkboxes MUST come AFTER their component items; never before. Components first, summary last. Forbidden: parent-before-children (L344-350), summary-in-middle (L352-358).
- E3 SEQUENTIAL ORDER (L367-382): top-to-bottom only; never require marking items above current position; never reference later checkboxes; forbidden "see below"/"return to phase" patterns.
- D3 CRITICAL RULE (L286-290): NO checklist items before Phase 1. Order = Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (executable).

This is the anti-orphaning basis: task-completion items live INSIDE the final phase / Post-Completion Actions, ordered last, never floating above their components.

### M3 — LENS-BASED QA SEQUENCE (lines 1059-1096) — the mandatory per-phase QA pattern
M3 is the MANDATORY replacement for the deprecated single-agent M1 (M1 at L1034-1045; "New task files MUST NOT use M1"). The 8-step sequence:
- **Step 1 Aggregation** (L1062, L6 pattern) — Glob all preceding-phase outputs into a summary/inventory file.
- **Step 2 Structural Lens Agents — PARALLEL** (L1064-1071) — spawn rf-qa, one per structural lens, `fix_authorization: false`. Reports to `${TASK_DIR}qa/qa-structural-[lens]-report.md`. Adversarial framing: "Assume this document has at least N errors focused on [lens]. Find them."
- **Step 3 Content Lens Agents — PARALLEL** (L1072-1079) — spawn rf-qa-qualitative, one per content lens, `fix_authorization: false`. Reports to `${TASK_DIR}qa/qa-content-[lens]-report.md`. (Steps 2+3 MAY be one parallel batch, L1080.)
- **Step 4 Domain-Specific Lens Agents** (L1082, if applicable).
- **Step 5 Findings Consolidation** (L1084) — read ALL lens reports → single `${TASK_DIR}qa/qa-consolidated-findings.md`, deduplicated, severity (CRITICAL/IMPORTANT/MINOR) + originating lens.
- **Step 6 Fix Agent** (L1086) — ONE rf-qa `fix_authorization: true`, applies ALL fixes. No other agent edits the doc (serialized, I20 L745-757).
- **Step 7 Verification Round — PARALLEL** (L1088) — min 2 agents (1 rf-qa + 1 rf-qa-qualitative), `fix_authorization: false`. Reports `qa-verification-structural-report.md` + `qa-verification-content-report.md`.
- **Step 8 Conditional Proceed** (L1090, L5 pattern) — IF both PASS proceed; IF either FAIL repeat Steps 5-7. Max cycles per I16 table (L660-668: most gates 3, synthesis/task-integrity 2); then HALT + escalate.
- **Task file encoding** (L1096): EVERY step is an explicit `- [ ]` checklist item; orchestrator MUST NOT collapse steps.

Standard 4 structural lenses (L715-719): template-conformance, internal-consistency, evidence-quality, completeness. Standard 4 content lenses (L721-726): actionability, numbers-metrics, crossref-chain, domain-accuracy.

QA intensity (I22, L793-840) governs agent counts: **lite** = 3 final-gate agents (1 structural+1 content+1 domain), 1 fix cycle, 1 verification agent; **standard** = 7 (3 struct + 3 content + 1 domain), 2 cycles, 2 verification; **full** = per I19 tables (min 6, 6-12+ by size). Serialized fix (I20) applies at ALL levels.

### M4 — SOURCE-DOCUMENT FIDELITY GATE (lines 1098-1121) + I21 (L759-788)
Runs AFTER M3 when outputs are derived from source docs. NOT required for "pure transformation tasks where the output format is mechanically derived from the input (e.g., rename operations)" and "configuration-only tasks with no source-document interpretation" (I21 L773-776). **Relevance to TFEP migration:** a forensic→troubleshoot string/reference replacement in skill/command markdown is closest to a transformation; the builder must decide whether M4 applies. If the TFEP edits reinterpret semantics (not just rename), M4 applies; if pure reference-swap, M4 may be omitted with a logged "Fidelity gate not applicable — [reason]" note (the Post-Completion placeholder at PART2 L1437 explicitly allows this).

### POST reflect gate shape
The template does NOT hardcode a POST reflect checklist item in PART 2 — instead `reflect_post` is a frontmatter field (L32): "POST reflect verdict; recorded by the executor after the final-phase reflect subagent runs." The wired shape comes from the EXAMPLE (see PART B, Step PC.5 below) and from the F2 prohibition list (L430) "Skipping post-completion validation". So the builder must AUTHOR the POST reflect item explicitly in Post-Completion Actions (it is not template-supplied).

### Post-Completion Actions ordering (I13 L616-621, I17 L675-686, PART 2 L1423-1441)
The Post-Completion Actions section (PART 2 L1423) orders items: (1) verify outputs exist on disk via Glob (L1425), (2) tests pass if code modified (L1427), (3) POST-COMPLETION LENS-BASED QA per M3 — MANDATORY (L1435 placeholder), (4) POST-COMPLETION SOURCE FIDELITY gate per M4 if applicable (L1437 placeholder), (5) Write Task Summary (L1439), (6) **update frontmatter status to "🟢 Done" + completion_date — the LAST item** (L1441). This is the anti-orphaning rule applied to task completion: the status-to-Done item is the final checkbox, after all validation/QA/summary items.

### Anti-orphaning summary (task-completion items inside the final phase)
Per E2/E3 + D3 + I13/I17: all task-completion and validation items live INSIDE the Post-Completion Actions section (the final block), ordered so the status→Done flip is the terminal checkbox. No completion or summary checkbox floats above its component work. POST reflect gate, when authored, sits PENULTIMATE — immediately before the status-to-Done item.

### TESTING_REQUIREMENTS for docs/skill-edit tasks (I18 L688-697)
I18 mandates a testing item ONLY for tasks that "create or modify source code files (not documentation, not configuration)". For this docs/skill-editing migration TESTING_REQUIREMENTS=NONE: no pytest item is required. Verification is instead `make verify-sync` (src↔.claude mirror parity) + protocol read-through, and QA gates verify PROSE correctness, not code. The example (PART B) shows `make verify-sync` used as the docs/skill-edit verification analog (its skill-dir edits run `make sync-dev` then `make verify-sync`, and MUST NOT stage `.claude/`).

---

## PART B: Real example structural patterns

**Example chosen:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-bare-review-migration-20260616-045915/TASK-RF-bare-review-migration-20260616-045915.md` (769 lines). Chosen because it is a same-day (2026-06-16) skill/command MIGRATION task built from Template 02, with multiple phases, per-phase M3 QA gates, an M4 fidelity gate, and a fully-wired POST reflect gate — directly analogous to the TFEP forensic→troubleshoot migration.

### Frontmatter (example, L1-63)
- `id` matches dir name (L2); `type: "🧩 Integration"` (L7), `status: "🟠 Doing"` (L6), `task_type: static` (L60).
- `spec_path` populated (L18) pointing at the driving requirements doc; `template_schema_doc` (L47) cites the Template-02 path.
- `reflect_pre` block FULLY populated (L19-27): verdict pass, coverage_pct 0.909, depth deep, tcs 36, run_id, report path, reviewed_at, plus a free-text `notes` subfield. `reflect_post: ""` (L28) left empty for the executor/wrapper to write.
- Two non-template trailing fields added: `start_commit` (L61, the git baseline for diff-stat aggregation) and `executor_model_class: "opus"` (L62).

### Phase headers (how phases are headed)
- `### Phase N: <NAME> (<STRICT/STANDARD/LIGHT>, <dependency note>)` — e.g. L182 `### Phase 2: WS-0 — ... (STRICT, BLOCKING PREREQUISITE)`, L264 `### Phase 3: WS-A — ... (STRICT, depends WS-0 PASS)`.
- QA gates get their own `### Phase Gate N: Lens-Based QA on <X> (M3, full intensity — <gate-type> gate, max 3 fix cycles)` header (e.g. L226, L288, L350, L436, L514).
- Each phase opens with a bold prose preamble paragraph (no checkbox) explaining the phase's purpose, dependencies, and sync/constraint notes (e.g. L184, L228, L266). Phase 1 also carries the literal "YOU MUST complete EVERY item ... IN ORDER" banner (L164).
- Steps headed `**Step N.M:** <short title>` (no checkbox on the header), then exactly ONE `- [ ]` item beneath (e.g. L166/L168, L190/L192). QA-gate steps headed `**Step PGn.M:**` (L230), Post-Completion `**Step PC.N:**` (L574).

### Self-contained item shape (how items embed context/action/output/verification/completion gate)
Each `- [ ]` is ONE verbose paragraph embedding the B2 six elements. Canonical structure observed (e.g. Step 1.1 L168, Step 2.1 L188, Step 2.2 L192):
1. **Context+WHY:** "Read the file `X` at `path` ... because <reason>"
2. **Action+WHY:** "then add/create/modify ... so that <reason>"
3. **Output spec:** exact handoff path under `.dev/tasks/to-do/TASK-RF-bare-review-migration-20260616-045915/phase-outputs/{discovery,test-results,plans,reports}/` or `qa/`.
4. **Integrated verification:** "ensuring <criteria> ... with no fabrication" (the "ensuring..." clause).
5. **Evidence-on-failure:** "If unable to complete due to ..., log the specific blocker using the templated format in the ### Phase N Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete."
6. **Completion gate:** "Once done, mark this item as complete."
Items carry explicit `file:line` anchors in context references (e.g. Step 2.1 L188 cites `commands.py` ~L1304-1578, `reduce.py` `CONTRACT_FILENAME` ~L139) — matching M3 evidence-quality lens expectations.

### Per-phase QA gate encoding (M3 mapped to checklist items)
Phase Gate 2 (L226-262) is the model. Each M3 step is a discrete `**Step PG2.M:**` + `- [ ]`:
- PG2.1 Aggregate (L230-232) — Glob WS-0 handoffs + `git diff --stat <start_commit>` → `reports/ws0-output-summary.md` (L6).
- PG2.2 Structural lens agents (L234-240) — THREE separate `- [ ]` items, one rf-qa each, custom lenses (flag-completeness, pipeline-wiring, test-evidence), each `fix_authorization: false`, adversarial framing "Assume this WS-0 diff has at least 10 errors focused on X. Find them.", each writing `qa/qa-structural-<lens>-report.md` with binary PASS/FAIL.
- PG2.3 Content lens agents (L242-248) — THREE separate `- [ ]` rf-qa-qualitative items (legacy-parity-faithfulness, regression-safety, constraint-compliance), `fix_authorization: false`, → `qa/qa-content-<lens>-report.md`. (6 report-only agents total = full-intensity floor.)
- PG2.4 Consolidate + fix (L250-254) — TWO items: (a) read all 6 reports → `qa/qa-consolidated-findings-pg2.md` dedup+severity+verdict (FAIL if ANY issue); (b) IF PASS skip to PG2.6, IF FAIL spawn ONE rf-qa `fix_authorization: true` (serialized I20).
- PG2.5 Verification round (L256-258) — ONE item spawning 1 rf-qa + 1 rf-qa-qualitative (`fix_authorization: false`) → `qa-verification-{structural,content}-pg2.md`.
- PG2.6 Conditional proceed (L260-262, L5) — durably reads/writes a fix-cycle counter at `phase-outputs/plans/pg2-cycle-count.md` (survives session rollover so the I16 3-cycle cap can't silently reset), IF both PASS writes `pg2-verdict.md` authorizing next phase, IF FAIL loops PG2.4-PG2.5 max 3 cycles then HALT + set status "⚪ Blocked".
Custom lens names (not the generic 8) are used, tailored to the phase's actual risk surface — a pattern the TFEP builder should follow (e.g. reference-completeness, no-orphan-forensic-refs lenses).

### M4 fidelity gate encoding (example)
Phase Gate 6 (L514-554) adds `**Step PG6.4:** Source-fidelity gate (M4, PARALLEL fidelity agents)` (L538) — used for the WS-D net-new OPS docs (derived from source spec). Confirms M4 is gated on whether the phase output is derived from source documents.

### Final phase ordering: POST reflect → update-status-to-Done
Post-Completion Actions (L570-596) ordered exactly per template, with the POST reflect gate authored explicitly:
- **PC.1** (L574-576): verify all deliverables exist on disk via Glob/Bash (I17 anti-attestation) → `reports/final-deliverable-verification.md`.
- **PC.2** (L578-580): final full-suite + `make verify-sync` regression check (HARD failure gate) → `final-regression-summary.md`. (For a docs/skill task with TESTING_REQUIREMENTS=NONE, the analog is `make verify-sync` alone.)
- **PC.3** (L582-584): POST-COMPLETION lens-based QA on the FULL migration (M3, min 6 agents, custom lenses incl. anti-attestation + constraint-compliance), durable cycle counter `plans/pc3-cycle-count.md`.
- **PC.4** (L586-588): Write the Task Summary — authored BEFORE the reflect gate "so the independent reflect audit can review the completed summary as part of the final state."
- **PC.5** (L590-592): **POST reflect anti-bias gate — PENULTIMATE, "the LAST gate before completion."** Encoded as a FLAT WRAPPER Bash shell-out (NOT an agent spawn, NOT `--mode post`, NOT a `<base>..HEAD` range): `git add -A` first, then a single guarded command with a `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion-breaker guard, invoking `superclaude reflect run <task-file> --depth deep --fix --promote` and echoing `reflect_exit=$?`. The wrapper itself writes the `reflect_post` frontmatter field ("do NOT hand-author `reflect_post`"). Exit-code consumption: only `reflect_exit=0` passes; 10/11/2 = FAIL → set status "⚪ Blocked", log, HALT before PC.6. Output → `reports/post-reflect-summary.md`.
- **PC.6** (L594-596): Close out frontmatter — update `completion_date`/`updated_date` + set status "🟢 Done" ONLY IF PC.1-PC.5 all passed (in particular PC.5 exited 0); else leave "⚪ Blocked". This is the TERMINAL checkbox.

So ordering is: ...validation → post-completion M3 QA → Task Summary → **POST reflect wrapper (penultimate)** → **status-to-Done (final)**.

### Task Log / Notes structure (example L598-769)
Mirrors template PART 2: `### Task Summary` (filled in PC.4), `### Execution Log`, per-phase `### Phase N - <name> Findings` blocks (one per phase + `### Phase Gate Findings`), `### Follow-Up Items Identified`, `### Deviations from Process`. Blockers logged here per the J1 embedded error-handling pattern referenced in every item.

---

## SUMMARY (for the TFEP troubleshoot-migration builder)

Conformance checklist the generated tasklist MUST satisfy:
1. **Frontmatter** (template L1-61): use Template-02 frontmatter; set `type` (📚 Documentation or 🧩 Integration), `task_type: static`, `template_schema_doc` = the Template-02 path, `reflect_pre` populated by the builder at A.10.7, `reflect_post: ""` (executor/wrapper writes it). Populate `spec_path` if a driving spec exists.
2. **No checklist items before Phase 1** (D3 L286-290). Order: Frontmatter → Task Overview/Objectives → Prerequisites (informational) → Execution Context → Phase 1 (status-update first per I11) → execution phases → Post-Completion Actions.
3. **Every item self-contained (B2, 6 elements)** as ONE paragraph: Context+WHY, Action+WHY, Output spec, "ensuring..." verification clause, evidence-on-failure-only blocker-log clause, "Once done, mark this item as complete." gate. No standalone read-context items, no separate verification items (B5/C3/I12).
4. **Granular (A3)**: one `- [ ]` per file edited (each forensic→troubleshoot target file = its own item with exact path).
5. **Per-phase M3 QA gate** (I15/M3) between any phase and a dependent phase: aggregate (L6) → ≥3 structural rf-qa lenses + ≥3 content rf-qa-qualitative lenses in PARALLEL `fix_authorization: false` → consolidate → ONE serialized fix agent (I20) → 2-agent verification → conditional-proceed with durable cycle counter. Agent counts scale by qa_intensity (I22). For a docs task, lenses verify PROSE (e.g. reference-completeness, no-orphaned-forensic-refs, command-name-accuracy), not code.
6. **M4 fidelity gate** only if outputs are derived from source docs (I21); a pure reference-rename may log "not applicable — [reason]" (PART 2 L1437 permits this).
7. **TESTING_REQUIREMENTS=NONE** for this docs/skill-edit task (I18): no pytest item; verification = `make verify-sync` + protocol read-through. Skill-dir edits MUST `make sync-dev` then `make verify-sync` and MUST NOT stage `.claude/`.
8. **Post-Completion Actions ordering** (I13/I17, PART 2 L1423-1441): verify-outputs-exist → (`make verify-sync` for docs) → post-completion M3 QA → Task Summary → **POST reflect wrapper (penultimate, flat Bash shell-out with recursion guard + exit-code consumption; wrapper writes reflect_post)** → **status-to-Done (terminal checkbox)**. Anti-orphaning: completion/summary items never float above their components.

Key reference files:
- Template: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md`
- Example: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-bare-review-migration-20260616-045915/TASK-RF-bare-review-migration-20260616-045915.md`

Status: Complete
