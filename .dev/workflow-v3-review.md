# Workflow v3 template gap review

Scope: Compare `src/superclaude/templates/workflow/00_mdtm_template_simple_task.md` with `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md` (A) and `src/superclaude/examples/tasklist_index_template.md` (B). A gap is an inventory item, **not** a recommendation to add it. The intended handoff is `/sc:workflow` to `/sc:implement`, not MDTM `/task` or Sprint `/sc:tasklist`.

## Combined gap inventory (original source order)

| ID | Missing/weak element in 00 | Source evidence | Fit |
|---|---|---|---|
| G01 | Trace each source requirement to an implementing task and observable outcome; optional matrix at scale. | A:98-102,1210-1212; B:105-115,129-140 | Applicable principle; matrix conditional |
| G02 | Identify the concrete output or earlier-task artifact consumed by a dependent task and its purpose. | A:1029-1038,260-279 | Applicable when dependent |
| G03 | Specify exact deliverable location, required content/interface and governing template when known. | A:155-159,219-224,573-579 | Applicable when specified |
| G04 | Specify a targeted check, expected result and scope for code-modifying work. | A:672-679,1234-1240; B:119-127 | Applicable; stored test log conditional |
| G05 | Provide source citations and evidence expectations close to each task; avoid inferred facts. | A:155-160,591-595,621-631 | Applicable for source-driven work |
| G06 | Preserve input provenance when multiple sources govern the plan (spec, PRD, TDD, roadmap). | A:23,33-41,1042-1052; B:16-23,35-48 | Conditional |
| G07 | Explain material scope limits, blockers and non-goals at the relevant task, beyond the existing global Constraints. | A:1054-1056,829-847 | Conditional; no mark-failure-complete behavior |
| G08 | Summarize a long source's relevant starting state for standalone plan readability. | B:81-87 | Conditional |
| G09 | Explicitly identify governing references and relevant source areas beyond the single Source line. | A:33-41,1042-1052 | Conditional; task-local references suffice |
| G10 | Maintain a global deliverable inventory linking tasks, evidence and intended artifact paths. | B:117-127 | Conditional for large multi-artifact plans |
| G11 | Capture planning decisions/rules that materially change execution, rather than a full generator audit log. | B:89-103 | Conditional |
| G12 | Spell out dependency graph including parents/blockers beyond the existing `Depends on: Task 1`. | A:18-22,1020-1027 | Conditional for non-linear plans |
| G13 | Record risk, priority, effort or confidence when they affect scheduling or verification. | A:8-14; B:72-79,119-127 | Conditional; Sprint tier fields not required |
| G14 | Enumerate a bounded set of work items before consolidation when completeness of an inventory matters. | A:110-129,856-881 | Conditional; not one task per file by default |
| G15 | Include enough task-local context to remain understandable after a session rollover. | A:147-175,1080-1105 | Conditional; not MDTM self-contained checkbox paragraphs |
| G16 | Check source-to-output fidelity for major spec-derived outputs (coverage, detail, contradictions). | A:742-771,946-969 | Conditional; no default fidelity-agent gate |
| G17 | Add cross-task/phase acceptance checkpoint for significant dependent output before proceeding. | A:633-657; B:150-167 | Conditional; not mandatory phase report schema |
| G18 | Capture end-of-task handoff notes on outputs, blockers, deviations and follow-ups. | A:1249-1257,1265-1340 | Conditional; `/sc:implement` already has a ledger |
| G19 | Keep per-task status/assignee/category/dates/tags in plan frontmatter. | A:2-14,42-60 | Mostly executor/external tracker concern |
| G20 | Force flat sequential checkboxes, single-item reread/update loop and task-file status mutations. | A:291-303,407-464 | Incompatible with `/sc:implement` task parsing/ledger |
| G21 | Allow worker insertion into dynamic task regions with marker syntax. | A:538-571,1170-1175 | MDTM `/task`-only mechanism |
| G22 | Prescribe multi-agent lens QA, serialized fixes, review reports and agent-count floors. | A:681-740,776-823,1180-1232 | MDTM `/task`-only default; optional explicit ask |
| G23 | Generate Sprint N+1 bundle manifest with phase files, tier distributions and artifact directories. | B:10-12,50-79 | Sprint `/sc:tasklist`-only mechanism |
| G24 | Add separate execution log, checkpoint-report schema and estimate/tier feedback file. | B:142-183; A:1292-1300 | Sprint/MDTM-only; avoid duplicating implement ledger |
| G25 | Replace sentinel placeholders with a zero-sentinel generator self-check. | B:3-8 | Conditional principle; sentinel mechanism Sprint-specific |

## Independent scoring and initial ranking

Value V (1–10) measures benefit to the `/sc:workflow` → `/sc:implement` handoff; cost C (1–10) measures incremental overhead, 10 = maximum. V was rated independently and challenged with `/ponytail ultra`; C was independently rated assuming a 5–10-task plan. Token estimates are additional **generated-plan** tokens; handling-time ranges are rough incremental authoring/review/operator effort, **not** implementation or test runtime. Conditional entries assume they apply. Rows overlap; do not add estimates together. Sort by V/C descending, tie-break by V descending, C ascending, then ID.

| Rank | ID | V | C | V/C | Extra tokens | Extra handling time | Initial rationale |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | G03 | 9 | 2 | 4.50 | 80–250 | 5–12 min | Known paths/interfaces make outcomes concrete. |
| 2 | G02 | 7 | 2 | 3.50 | 50–180 | 3–8 min | Name consumed artifacts only where dependency is ambiguous. |
| 3 | G04 | 9 | 3 | 3.00 | 100–300 | 5–15 min | Task checks with expected results make AC testable. |
| 4 | G07 | 6 | 2 | 3.00 | 40–150 | 3–10 min | Apply exceptional constraints at affected tasks. |
| 5 | G06 | 6 | 3 | 2.00 | 80–220 | 5–15 min | Distinguish governing inputs when there are several. |
| 6 | G11 | 4 | 2 | 2.00 | 70–200 | 4–10 min | Record consequential choices, not generator history. |
| 7 | G25 | 4 | 2 | 2.00 | 20–100 | 3–10 min | Filled-in output matters; Sprint sentinels do not. |
| 8 | G05 | 7 | 4 | 1.75 | 120–350 | 8–20 min | Source grounding without citation bureaucracy. |
| 9 | G01 | 8 | 5 | 1.60 | 150–600 | 10–30 min | Coverage helps; explicit matrices only at scale. |
| 10 | G12 | 6 | 4 | 1.50 | 100–350 | 6–18 min | Extra graph detail only for non-linear dependencies. |
| 11 | G15 | 6 | 4 | 1.50 | 150–450 | 8–20 min | Local context helps resume without repeated specs. |
| 12 | G08 | 3 | 2 | 1.50 | 100–300 | 5–12 min | Snapshot only for long, opaque sources. |
| 13 | G09 | 4 | 3 | 1.33 | 80–250 | 5–15 min | References beyond task/source line are occasional. |
| 14 | G13 | 3 | 3 | 1.00 | 80–250 | 5–15 min | Risk/effort data only if it changes actions. |
| 15 | G16 | 6 | 7 | 0.86 | 100–350 | 20–60 min | Fidelity review for substantial derived output only. |
| 16 | G14 | 4 | 5 | 0.80 | 150–500 | 10–30 min | Finite inventories matter only when completeness is critical. |
| 17 | G17 | 4 | 6 | 0.67 | 100–300 | 15–45 min | Checkpoints only ahead of costly dependent work. |
| 18 | G10 | 2 | 5 | 0.40 | 180–500 | 10–25 min | Registry duplicates tasks in ordinary plans. |
| 19 | G18 | 1 | 4 | 0.25 | 80–250 | 8–20 min | Executor already records progress and verdicts. |
| 20 | G19 | 1 | 5 | 0.20 | 180–450 | 10–25 min | Status metadata belongs to an external tracker. |
| 21 | G21 | 1 | 8 | 0.13 | 150–450 | 20–60 min, may block | Dynamic insertion is for MDTM `/task`. |
| 22 | G24 | 1 | 8 | 0.13 | 250–750 | 25–75 min | Separate logs duplicate the executor ledger. |
| 23 | G20 | 1 | 9 | 0.11 | 300–800 | 30–90 min, may block | Checkboxes conflict with implement task parsing. |
| 24 | G23 | 1 | 9 | 0.11 | 400–1,200 | 30–90 min, may block | Sprint bundle is a different execution model. |
| 25 | G22 | 1 | 10 | 0.10 | 250–800 | 60–240+ min | Agent floors duplicate implement's per-task review. |

Initial ratings are hypotheses for adversarial review, not instructions to add all 25 items.

## Adversarial findings (one independent reviewer per initial top-10 item)

| Item | Initial V/C | Revised V/C | Finding and decision |
|---|---|---|---|
| G03 | 9/2 | 4/3 | **Conditional:** 00 already requests paths/interfaces when known. Never fabricate exact output paths or templates to fill a form. |
| G02 | 7/2 | 4/2 | **Conditional:** name a consumed output only if several plausible prior outputs make the handoff ambiguous; ordering is already explicit. |
| G04 | 9/3 | 5/2 | **Conditional:** add expected result/scope only when an existing check is vague. No duplicate test-log requirement; implement runs tests as extras. |
| G07 | 6/2 | 3/2 | **Conditional:** put exceptional task-local limits in its existing body; global Constraints already exists. Never mark blocked work complete. |
| G06 | 6/3 | 3/4 | **Conditional:** clarify governing source/precedence only with multiple conflicting inputs; one Source plus task citations otherwise suffice. |
| G11 | 4/2 | 3/2 | **Conditional:** record only consequential choices an executor might otherwise reverse, not a generator audit trail. |
| G25 | 4/2 | 2/2 | **Drop as separate feature:** 00 already says remove unused placeholders. Sprint sentinels do not match 00's bracketed placeholders; check output only if this failure recurs. |
| G05 | 7/4 | 4/2 | **Conditional:** cite source near a task only to resolve ambiguity; implement already requires diff evidence for its verdict. No universal citations table. |
| G01 | 8/5 | 8/2* | **Keep a bounded source-coverage check, not a matrix.** Full matrix would be ~V5/C8 ordinarily; source size, not task count, governs escalation. |
| G12 | 6/4 | 3/3 | **Conditional:** put prerequisite first and add a short note only if non-linear dependency is unclear; implement ignores graph metadata. |

*G01's revised V8/C2 applies only to the cheap task-local check against already-extracted, bounded requirements. For a long/unstructured source, the reviewer estimated V6/C3; a full registry/matrix is a different, much costlier choice. No reviewer recommended changing the `00_` template as part of this scoring exercise.

## Final ranked gap list (most value per lowest incremental cost)

The first ten **initially** ranked items above received adversarial reviews. Newcomers to the final top ten (G15, G08, G09) retain independent initial scores, not adversarially reviewed scores. All estimates are rough, conditional, and non-additive.

| Rank | ID | V | C | V/C | Approx. extra plan tokens | Approx. handling overhead | Disposition |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | G01 | 8 | 2 | 4.00 | 0–120 | 3–10 min | Keep bounded coverage check; no default matrix |
| 2 | G04 | 5 | 2 | 2.50 | 20–80 | 1–4 min | Conditional: clarify vague checks |
| 3 | G02 | 4 | 2 | 2.00 | 20–80 | 1–4 min | Conditional: ambiguous handoffs only |
| 4 | G05 | 4 | 2 | 2.00 | 20–90 | 2–6 min | Conditional: disambiguating source citations |
| 5 | G15 | 6 | 4 | 1.50 | 150–450 | 8–20 min | Conditional: rollover-sensitive work |
| 6 | G07 | 3 | 2 | 1.50 | 0–60 | 0–4 min | Conditional: task-specific constraint |
| 7 | G08 | 3 | 2 | 1.50 | 100–300 | 5–12 min | Conditional: long source only |
| 8 | G11 | 3 | 2 | 1.50 | 30–90 | 2–5 min | Conditional: consequential decision |
| 9 | G03 | 4 | 3 | 1.33 | 30–100 | 3–8 min | Conditional: source-grounded specificity |
| 10 | G09 | 4 | 3 | 1.33 | 80–250 | 5–15 min | Conditional: references not already in tasks |
| 11 | G12 | 3 | 3 | 1.00 | 40–120 | 2–6 min | Conditional: complex dependencies |
| 12 | G13 | 3 | 3 | 1.00 | 80–250 | 5–15 min | Conditional: scheduling changes |
| 13 | G25 | 2 | 2 | 1.00 | 0–20 | 1–3 min if needed | Drop extra placeholder gate |
| 14 | G16 | 6 | 7 | 0.86 | 100–350 | 20–60 min | Conditional: major spec-derived output |
| 15 | G14 | 4 | 5 | 0.80 | 150–500 | 10–30 min | Conditional: inventory-sensitive task |
| 16 | G06 | 3 | 4 | 0.75 | 0–100 | 0–6 min | Conditional: multiple governing sources |
| 17 | G17 | 4 | 6 | 0.67 | 100–300 | 15–45 min | Conditional: costly dependent work |
| 18 | G10 | 2 | 5 | 0.40 | 180–500 | 10–25 min | Skip ordinary registry |
| 19 | G18 | 1 | 4 | 0.25 | 80–250 | 8–20 min | Skip duplicate handoff ledger |
| 20 | G19 | 1 | 5 | 0.20 | 180–450 | 10–25 min | Skip tracking frontmatter |
| 21 | G21 | 1 | 8 | 0.13 | 150–450 | 20–60 min; may block | Exclude dynamic MDTM markers |
| 22 | G24 | 1 | 8 | 0.13 | 250–750 | 25–75 min | Exclude duplicate logs/feedback |
| 23 | G20 | 1 | 9 | 0.11 | 300–800 | 30–90 min; may block | Exclude MDTM checkboxes |
| 24 | G23 | 1 | 9 | 0.11 | 400–1,200 | 30–90 min; may block | Exclude Sprint bundle |
| 25 | G22 | 1 | 10 | 0.10 | 250–800 | 60–240+ min | Exclude mandatory multi-agent gates |

**Practical takeaway:** If improving `00_` later, first check that source requirements have tasks and observable acceptance criteria (G01). Clarify ambiguous checks or handoffs in existing task text (G04/G02), rather than importing fields, registries or MDTM process. This report is evaluation only; no template edits were authorized by the review request.
