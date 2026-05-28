# Matrix: capabilities task-builder has that sc:tasklist lacks

Each row catalogs a task-builder capability absent or weaker in sc:tasklist. Because the merge direction is sc:tasklist → task-builder, these rows are not *import candidates* — they are **constraints on imports**: any imported sc:tasklist mechanism must not erode them.

Inverse-direction relevance values:
- `preserved invariant` — one of the 5 G6 invariants; any import that violates it is REJECT
- `constraint on imports` — a strong task-builder behavior that imports must respect but is not a hard G6 invariant
- `irrelevant` — task-builder has it but the merge direction doesn't put it at risk

---

### M-TB-01: Agent-team delegation (rf-* named ecosystem with explicit message vocab)
- **task-builder source**: SKILL.md:398, 582, 614, 664, 720, 877, 927; Naming Conventions table SKILL.md:1690–1697 — Bucket C digest; agents enumerated in Bucket D
- **FINAL-REPORT reference**: §3.2 (RF agent team), §4 row "Generation stages" (9 outer phases + 10 inner sub-stages)
- **sc:tasklist status**: absent (Bucket A: anonymous `Task` tool agents; only Stage 9 delegates to a named skill `sc:task`)
- **Inverse-direction relevance**: constraint on imports
- **One-line rationale**: any imported mechanism must respect the named-agent topology (analyst/qa/qa-qualitative/builder/researchers); imports should specify host agent rather than introducing anonymous-agent dispatch.

### M-TB-02: Parallel research model (all researchers spawned in same message)
- **task-builder source**: SKILL.md:400–401, 1499, 1673–1677 ("ALL researchers for a track spawned in the SAME message for parallel execution… Multi-track: ALL researchers across ALL tracks in one message") — Bucket C digest
- **FINAL-REPORT reference**: not addressed (FINAL-REPORT focuses on sc:tasklist Stages 7–10 validation parallelism)
- **sc:tasklist status**: partial (Bucket A SKILL.md:1091–1106 — 2N parallel validation agents, but no generation-time parallel researchers)
- **Inverse-direction relevance**: preserved invariant (G6: parallel research)
- **One-line rationale**: imports must not introduce serial generation steps that bottleneck the parallel research model.

### M-TB-03: Self-contained item schema (context + action + output + verification + completion gate)
- **task-builder source**: SKILL.md:900, 1452–1457, 1495, 1515 ("Checklist items are self-contained (context + action + output + verification + completion gate)") — Bucket C digest
- **FINAL-REPORT reference**: §3.2 ("self-contained item innovation"), §7 R2 (sc:tasklist adopts a related Execution Context concept)
- **sc:tasklist status**: different model (Bucket A: task metadata table SKILL.md:791–806 has 13 fields incl. Why/Effort/Risk but lacks per-item context+output+verification+completion-gate quintet)
- **Inverse-direction relevance**: preserved invariant (G6: self-contained-item)
- **One-line rationale**: any imported task-template mechanism must preserve the 5-field item schema; importing sc:tasklist's leaner per-task metadata as a *replacement* would violate this invariant.

### M-TB-04: Zero-trust QA with adversarial stance
- **task-builder source**: SKILL.md:621, 878, 895, 929 (8× repetition of "Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine"); rule #7 SKILL.md:1540 — Bucket C digest
- **FINAL-REPORT reference**: not addressed (FINAL-REPORT discusses sc:tasklist's 17-point gate but not adversarial-stance language)
- **sc:tasklist status**: absent (Bucket A: gate checks are pass/fail mechanical; no "assume errors" framing)
- **Inverse-direction relevance**: preserved invariant (G6: zero-trust QA)
- **One-line rationale**: imports must reinforce the adversarial stance; mechanically passing structural checks does not satisfy zero-trust QA — rf-qa-qualitative's semantic adversarial review remains mandatory.

### M-TB-05: 4-stage gate pipeline (A.5 self-review, A.8 research-gate, A.10 task-integrity, A.10.5 qualitative)
- **task-builder source**: SKILL.md:357–363 (A.5 7-item), SKILL.md:594–602 (A.8 9-item analyst) + 627–632 (5-item QA) + 1323–1333 (10-item QA), SKILL.md:898–906 (A.10 9-item), SKILL.md:961 (A.10.5 15-item) — Bucket C digest
- **FINAL-REPORT reference**: §3.1 ("17-point quality gate runs before any file is written") — sc:tasklist has one consolidated gate vs task-builder's 4 staged gates
- **sc:tasklist status**: different model (Bucket A: one 17-point gate)
- **Inverse-direction relevance**: preserved invariant (G6: zero-trust QA)
- **One-line rationale**: importing sc:tasklist's 17-point gate must be additive into the existing 4-stage structure (CB-3 disposition), not a replacement.

### M-TB-06: Incremental task-file writes (mandatory, never one-shot)
- **task-builder source**: SKILL.md:819–832 ("INCREMENTAL TASK FILE WRITING (MANDATORY — NEVER ONE-SHOT)"); rule #8 SKILL.md:1542; researcher protocol SKILL.md:437–449 — Bucket C digest
- **FINAL-REPORT reference**: not addressed (FINAL-REPORT §3.1 highlights sc:tasklist's *atomic* write as a strength)
- **sc:tasklist status**: different model (Bucket A SKILL.md:1042 — write-atomicity; partial bundle writes forbidden)
- **Inverse-direction relevance**: preserved invariant (G6: persistent .dev/tasks/ artifact)
- **One-line rationale**: write-atomicity is incompatible with incremental writes; any import that tries to enforce atomic writes would be REJECT.

### M-TB-07: Codebase as source of truth (code > docs > web)
- **task-builder source**: rule #1 SKILL.md:1528; SKILL.md:706, 1167 — Bucket C digest; researcher doc-staleness tagging Bucket D rf-task-researcher.md:253–271
- **FINAL-REPORT reference**: not addressed (sc:tasklist explicitly treats roadmap text as the source of truth, FINAL-REPORT §6.2 F1)
- **sc:tasklist status**: different model (Bucket A SKILL.md:46–55 — "Treat the roadmap as the only source of truth"; FINAL-REPORT §6.2 F1 reinforces "operates on roadmap text, not the live codebase")
- **Inverse-direction relevance**: preserved invariant (G6: evidence-bound-item)
- **One-line rationale**: task-builder's evidence-bound-item invariant requires file:line citations from the live codebase; sc:tasklist's roadmap-as-only-truth model cannot be imported without violating this.

### M-TB-08: Partitioning thresholds (>6 research files → multiple analyst/QA instances)
- **task-builder source**: rule #9 SKILL.md:643, 1544; rf-qa partition protocol Bucket D rf-qa.md:50–77; rf-analyst partition protocol Bucket D rf-analyst.md:42–69 — Bucket C/D digest
- **FINAL-REPORT reference**: not addressed
- **sc:tasklist status**: partial (Bucket A: 2N agents always, no threshold gating)
- **Inverse-direction relevance**: constraint on imports
- **One-line rationale**: partitioning is the host mechanism for any imported parallel-validation behavior; imports should extend existing partition rules rather than introduce a parallel scheme.

### M-TB-09: 18 Critical Rules (rules #1–18)
- **task-builder source**: SKILL.md:1526–1564 — Bucket C digest
- **FINAL-REPORT reference**: not addressed
- **sc:tasklist status**: different model (Bucket A: 6 hard "no-leakage / truthfulness rules" SKILL.md:20–28 and various pinpoint constraints)
- **Inverse-direction relevance**: constraint on imports
- **One-line rationale**: any import must not contradict any of the 18 rules (notably #1 codebase-truth, #2 evidence-based, #7 mandatory QA gates, #8 no-one-shotting, #11 multi-track isolation, #13 no team infrastructure, #14 actionability/self-containment, #15 anti-orphaning).

### M-TB-10: RESEARCH_NEEDED / MALFORMED retry budgets (separate counters)
- **task-builder source**: SKILL.md:859 (RESEARCH_NEEDED max 2), SKILL.md:865 (MALFORMED max 2), SKILL.md:870, 1550 (counters tracked independently) — Bucket C digest
- **FINAL-REPORT reference**: §7 R4 (Dual-Mode Patch Recovery proposal for sc:tasklist mirrors this idea — cap at 2 total passes)
- **sc:tasklist status**: different model (Bucket A SKILL.md:1150 — "retry once before reporting error"; no separate counters; FINAL-REPORT §4 row "Correction capability" → "1 pass")
- **Inverse-direction relevance**: constraint on imports
- **One-line rationale**: any imported patch-recovery mechanism should plug into the existing independent counters rather than collapse them.

### M-TB-11: 3-tier researcher count scaling (Quick 3 / Standard 4–5 / Deep 6–8)
- **task-builder source**: SKILL.md:90–94, 96–101 ("Quick / Standard / Deep tied to file count and researcher count") — Bucket C digest
- **FINAL-REPORT reference**: not addressed
- **sc:tasklist status**: different model (Bucket A: 2N agents derived from phase count, not from a research-depth tier; CB-4 — tier means different things)
- **Inverse-direction relevance**: preserved invariant (research depth = tier; not artifact compliance)
- **One-line rationale**: sc:tasklist's tier algorithm cannot replace this; the two systems classify orthogonal axes (CB-4 disposition).

### M-TB-12: Evidence binding to file:line citations
- **task-builder source**: SKILL.md:452–454 ("Every finding must cite actual file paths, line numbers, function names, class names. No assumptions, no inferences, no guessing"); SKILL.md:1530 (rule #2) — Bucket C digest
- **FINAL-REPORT reference**: §4 row "Evidence model" (sc:tasklist = text-to-text comparison, no programmatic evidence; RF = PABLOV-style evidence)
- **sc:tasklist status**: absent (Bucket A: no per-item file:line citation requirement; SKILL.md:851–852 forbids inventing file paths but does not require citing them)
- **Inverse-direction relevance**: preserved invariant (G6: evidence-bound-item)
- **One-line rationale**: imports must allow file:line citations to remain mandatory in research notes; importing a "no specific file paths" rule wholesale would erode evidence binding (FINAL-REPORT R2 mitigates by confining the no-paths rule to executor context only).

### M-TB-13: Persistent `.dev/tasks/` artifact trail (task file + research-notes + research/*.md + qa/*.md)
- **task-builder source**: SKILL.md:120–129, 1536, 1597–1608 ("Preserve research artifacts… persist after the task file is built. They serve as the evidence trail. Do NOT delete intermediate files") — Bucket C digest
- **FINAL-REPORT reference**: not addressed (sc:tasklist emits only ValidationReport.md and PatchChecklist.md as validation artifacts — FINAL-REPORT §3.1)
- **sc:tasklist status**: different model (Bucket A: emits ValidationReport + PatchChecklist; no persistent evidence trail mandate)
- **Inverse-direction relevance**: preserved invariant (G6: persistent .dev/tasks/ artifact)
- **One-line rationale**: any imported artifact-emission rule must not delete or replace the persistent research/QA evidence chain.

### M-TB-14: BUILD_REQUEST input format (structured input with QA_GATE_REQUIREMENTS, VALIDATION_REQUIREMENTS, TESTING_REQUIREMENTS)
- **task-builder source**: SKILL.md:30–47 (input contract); Bucket D rf-task-builder.md:88–99 (BUILD_REQUEST schema with 7 fields); SKILL.md:1558–1562 (rules #16/17/18 require encoding these requirements in the generated task file) — Bucket C/D digest
- **FINAL-REPORT reference**: not addressed
- **sc:tasklist status**: different model (Bucket A: input is roadmap text + optional --spec/--prd-file; no BUILD_REQUEST schema)
- **Inverse-direction relevance**: constraint on imports
- **One-line rationale**: imports must not require a roadmap as input — task-builder's input contract is GOAL or BUILD_REQUEST, and breaking this would orphan all BUILD_REQUEST consumers (rf-team-lead pipeline, /task-builder direct invocation).

### M-TB-15: Documentation staleness tagging ([CODE-VERIFIED] / [CODE-CONTRADICTED] / [UNVERIFIED])
- **task-builder source**: SKILL.md:519–522, 1150–1153 — Bucket C digest; Bucket D rf-task-researcher.md:253–271 ("Documentation Staleness Protocol")
- **FINAL-REPORT reference**: not addressed
- **sc:tasklist status**: absent
- **Inverse-direction relevance**: constraint on imports
- **One-line rationale**: any import that incorporates documentation/spec content must respect the doc-claim tagging discipline so research notes remain audit-grade.

### M-TB-16: Spawn-the-builder pattern (skill orchestrates; rf-task-builder agent writes the file)
- **task-builder source**: SKILL.md:80–82 ("Skill is the orchestrator, NOT the builder"); SKILL.md:719 (spawns rf-task-builder agent) — Bucket C digest
- **FINAL-REPORT reference**: not addressed
- **sc:tasklist status**: different model (Bucket A SKILL.md:1248–1258 — orchestrator delegates *patches only* to sc:task; *generation* is done by the orchestrator itself)
- **Inverse-direction relevance**: preserved invariant (G6: self-contained-item — builder owns the file lifecycle)
- **One-line rationale**: sc:tasklist's orchestrator-does-not-apply-patches separation is the inverse of task-builder's orchestrator-does-not-build separation; importing the former wholesale would break the latter.
