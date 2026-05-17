# TDD §5 — Technical Requirements (Synthesis)

**Synthesis file:** synth-02-technical-requirements.md
**Status:** Complete
**Date:** 2026-05-14
**Source research:** 00, 08, 09, 10, 11, 12, 13, 14 + qa/research-gate-consolidated.md
**Synthesis constraints applied:** SC-1..SC-8 (see qa/research-gate-consolidated.md)

**Scope note:** This section specifies the functional (§5.1) and non-functional (§5.2)
requirements for the Task-Builder Convergence v3.9 release — six FRs (FR-CONV.1..6)
landing in strict serial order **PR-06 (FR-CONV.1) 1st → PR-01 (FR-CONV.2) 2nd →
PR-04 (FR-CONV.3) 3rd → PR-07 (FR-CONV.4) 4th → PR-02 (FR-CONV.5) 5th →
PR-03 (FR-CONV.6) 6th** (SC-6 corrected order), plus ten NFRs of which NFR-CONV.6..10
are load-bearing invariant-preservation guarantees.

**Line-citation discipline:** All `file:line` citations below are **current-verified**
as of 2026-05-14 (sed-verified in research files 03/04/07/08..14). Where the PRD
asserted a different line, the drift is noted inline. Per SC-8, the zero-trust verdict
definitions are cited at `rf-qa.md:141-142` (not the PRD-asserted :144-146; :144 is the
surrounding heading). Per file 08, the rf-qa 20-item checklist items span
`rf-qa.md:268-287` (sub-header at :266). Per file 07 + SC-6, `rf-team-lead.md:417` is
**NO DRIFT** — the earlier line-414 hypothesis was wrong.

---

## §5.1 Functional Requirements

All six FRs are **Must Have (P0)** — Phase-1 release scope per PRD §21.1.1 Epics 1-3.
PR-05 (Tier-History Advisory) is **DEFERRED to Phase-2** and is out of scope here.

| ID | Requirement | Priority | Acceptance Criteria (Given/When/Then) |
|----|-------------|----------|----------------------------------------|
| **FR-CONV.1** | Append 8 structural checks (TB-Add-1..8) to rf-qa's task-integrity gate, mirrored across all three definition surfaces (rf-qa.md 20-item checklist, SKILL.md A.10 9-item block, SKILL.md 15-item validation block). CASE D (vs `/sc:tasklist` 17-point gate; per-check CB-3 import, not bulk). Protected invariant: **zero-trust QA**. | Must Have | **Given** a generated MDTM task file is submitted to rf-qa A.10, **when** any of TB-Add-1/3/4/5/6/7/8 detects a violation, **then** that check emits a distinct item-ID-naming error and the gate verdict is FAIL; **when** TB-Add-2 detects an out-of-bounds item count, **then** it emits an `[ADVISORY]`-prefixed message and does **not** block the gate. *Verification:* `grep -nE "TB-Add-[1-8]" src/superclaude/agents/rf-qa.md src/superclaude/skills/task-builder/SKILL.md` returns ≥3 hits per ID across the three definition sites — **rf-qa.md:268-287** (current-verified; items 1-20, sub-header at :266; PRD-cited 264-287 measured from `### What You Verify` opener at :264), **SKILL.md:898-906** (9-item A.10 block, current-verified, append point after line 906), **SKILL.md:1491-1507** (15-item validation block, current-verified — first `- [ ]` at :1494, last at :1508, append point after :1508). A synthetic fixture with one placeholder-titled item runs rf-qa and TB-Add-1 fires in the gate log. *Negative:* No existing rf-qa check is renamed, renumbered, or removed; the 9-item, 15-item, and 20-item existing items are preserved verbatim; bundle-specific `/sc:tasklist` checks (phase-file naming, checkpoint emission, R-### roadmap traceability — checks 12/18/19/20) MUST NOT appear in any TB-Add. **TB-Add catalogue:** TB-Add-1 placeholder scan (Hard); TB-Add-2 item-count bounds ≥3/≤40-track/≤50-single-track (`[ADVISORY]` until OPEN-INV-006 calibration); TB-Add-3 clarification adjacency (Hard); TB-Add-4 circular-dependency DAG check (Hard); TB-Add-5 granularity / XL-has-subtasks (Hard); TB-Add-6 Confidence/Verification format consistency (Hard); TB-Add-7 Execution-Context source-areas reappear in items — absorbs PR-01 failure-mode #4 (Hard); TB-Add-8 per-item Context field has ≥1 file:line citation OR justified-absence comment — resolves INV-015 (Hard). |
| **FR-CONV.2** | Insert a task-level `## Execution Context` block in generated MDTM task files (after frontmatter, before checklist) with exactly three labeled lines: References / Source areas / Key constraints. CASE D (vs `/sc:tasklist` tasklist-wide context block; scope-confinement adaptation). Protected invariant: **evidence-bound-item**. | Must Have | **Given** a BUILD_REQUEST with GOAL + WHY + related_docs, **when** rf-task-builder generates the task file, **then** it emits a `## Execution Context` block with exactly three labeled lines (`References:` / `Source areas:` / `Key constraints:`) placed after `## Prerequisites & Dependencies` and before the `## Phase 1` checklist; **when** the BUILD_REQUEST is minimal (GOAL only), **then** the block degrades to References-only with the other two lines explicitly omitted. *Verification:* `grep -n "## Execution Context" <generated-task-file>` returns line N; the next 10 lines contain ≥1 of `References:`/`Source areas:`/`Key constraints:`; `grep -E "src/|/.*:[0-9]+" <header-block-range>` returns **zero hits** (no file paths or file:line citations inside the header). *Insertion sites (current-verified, drift noted):* primary template at **SKILL.md:1407-1487** (generated-task-file template; PRD-cited 1409-1485, matches within ±2 lines; `## Execution Context` lands between end of Prerequisites at ~:1448 and the `---`/`## Phase 1` at ~:1449-1450); BUILD_REQUEST prompt guidance near **SKILL.md:715-725** (PRD-cited :719 is the `GOAL:` line *inside* the BUILD_REQUEST code block — drift: the `## Execution Overview` header is at :139, not :719); tier-aware header policy at **SKILL.md:86-103** (`## Tier Selection` — **STALE PRD citation:** PRD cited :228-238, but :226-240 is actually the A.2 template-selection table; the only `## Tier Selection` header is at :86). *Negative:* per-item Context fields MUST retain file:line citations OR justified-absence comments (validated by TB-Add-8); the per-item self-contained 5-field schema MUST NOT be altered or supplemented by header content; research/*.md and `related_docs:` frontmatter are out of scope of the "no paths" rule. |
| **FR-CONV.3** | Inject rf-qa's task-integrity verdict table verbatim into rf-qa-qualitative's spawn prompt under `## Inherited Structural Verdict`, with the directive "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality." Add a `## Self-Audit` section to rf-qa-qualitative's output schema. CASE B (no `/sc:tasklist` conflict — task-builder was silent). Invariant alignment: **zero-trust QA**. | Must Have | **Given** rf-qa A.10 has emitted a task-integrity verdict, **when** the orchestrator spawns rf-qa-qualitative at A.10.5, **then** the spawn prompt contains `## Inherited Structural Verdict` with the rf-qa Items Reviewed table copied byte-for-byte plus the directive; **when** a fix-cycle re-run occurs, **then** the orchestrator re-reads and re-injects the NEW (cycle-N) verdict — stale verdicts forbidden (INV-002); **when** rf-qa-qualitative runs, **then** its output contains a `## Self-Audit` section listing relied-on rf-qa PASS items AND ≥1 semantic check where rf-qa PASS is insufficient (INV-019). *Verification:* `grep -n "## Inherited Structural Verdict" <spawn-log>` returns line N and the block below diffs identically against `${TASK_DIR}qa/qa-task-integrity.md`; a synthetic 2-cycle fixture shows the cycle-2 verdict (not cycle-1) in the cycle-2 spawn log; the same fixture's output contains a Self-Audit section with ≥1 entry per category. *Insertion sites (current-verified — no drift):* **SKILL.md:923-1000** (A.10.5 spawn prompt; injection at ~:966 inside the fenced prompt block, after TARGET FILES, before INSTRUCTIONS); **rf-qa-qualitative.md:794** (EOF — append "Handling the Inherited Structural Verdict" section + add `## Self-Audit` to output schema). *Negative:* rf-qa-qualitative MUST NOT mark any item VERIFIED solely from the inherited verdict — every VERIFIED item shows an independent semantic-check engagement in the Self-Audit; the anti-inflation rule at **rf-qa-qualitative.md:766-775** MUST NOT be weakened, removed, or rephrased; no stale verdict from a prior fix cycle governs current-cycle decisions. |
| **FR-CONV.4** | Insert a `### Five Adversarial Axes` header subsection BEFORE rf-qa-qualitative's existing 15-item task-qualitative checklist, and add an `axis` column to the Items Reviewed table. Five axes: drift / contradictions / omissions / weakened-criteria / invented-content (plus `none` sentinel). CASE D (vs `/sc:tasklist` 5-category adversarial prompt; overlay-only CB-3). Protected invariant: **zero-trust QA**. | Must Have | **Given** rf-qa-qualitative runs the task-qualitative phase, **when** it produces output, **then** a `### Five Adversarial Axes` subsection renders BEFORE the 15-item checklist heading and the Items Reviewed table carries a populated `axis` column with one canonical value per row from {drift, contradictions, omissions, weakened-criteria, invented-content, none}; **when** no checklist item restates BUILD_REQUEST.GOAL verbatim, **then** the report emits a single-line `drift-axis-inactive` annotation in the Summary block. *Verification:* `grep -n "### Five Adversarial Axes" src/superclaude/agents/rf-qa-qualitative.md` returns ≥1 match; the emitted Items Reviewed table parses to N rows each with a non-empty `axis` ∈ the canonical six; a no-GOAL-baseline fixture produces the `drift-axis-inactive` substring. *Insertion sites (current-verified — ±2-line drift from PRD, normal post-PRD editing):* 15-item checklist body at **rf-qa-qualitative.md:525-585** (PRD-cited 527-583 — body MUST be unmodified; header inserts at ~:528 before `#### Checklist (15 items)`); Items Reviewed table at **rf-qa-qualitative.md:673-716** (PRD-cited 675-714 — insert `axis` column between `Check` and `Result`); axis-annotation directive in the task-builder Task-Qualitative prompt at **SKILL.md:961** (after the ADVERSARIAL STANCE paragraph, before INSTRUCTIONS). *Negative:* the existing 15-item checklist MUST NOT be removed, reordered, renamed, or replaced — axes annotate, they do not substitute; the severity floor at **rf-qa-qualitative.md:789** ("Contradictions are always IMPORTANT or CRITICAL", reinforced by items 9-10 at :792-793) MUST NOT be weakened; no axis introduces a new conditional code path (overlay-only); the `axis` column MUST NOT merge into the Issues Found table's `Severity` column. |
| **FR-CONV.5** | Add two stop-conditions to the EXISTING fix-cycle retry loops (no new loop or stage): (1) Monotonicity guard — HALT if `|F_{n+1}| >= |F_n|`; (2) Regression detection — HALT if any item PASS at cycle N is FAIL at cycle N+1. Precedence: **Regression > monotonicity** (regression check runs FIRST). CASE D (vs `/sc:tasklist` Stages 9-10 monotonicity guard). Protected invariant: **zero-trust QA**. | Must Have | **Given** a fix-cycle transition N→N+1, **when** any item that held PASS at cycle N flips to FAIL at cycle N+1, **then** the loop emits the verbatim message `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` and exits BEFORE the monotonicity check; **when** no regression but `|F_{n+1}| >= |F_n|`, **then** the loop emits `[HALT-MONOTONICITY] |F|=<n>` and exits; **when** a synthetic-dnsp finding with identical dedup-key appears in both cycles N and N+1, **then** no halt fires (dedup recognized, not a regression — its prior verdict was already FAIL). *Verification:* a 3-cycle fixture with `|F|=5,5,5` halts at cycle 2 with `[HALT-MONOTONICITY] |F|=5`; a 2-cycle fixture with Item 2.3 PASS@1/FAIL@2 halts with the verbatim regression message regardless of `|F_2| < |F_1|`; a 2-cycle dedup fixture proceeds to cycle 3 without halting; `grep -n "Retry Monotonicity Protocol" src/superclaude/skills/task-builder/SKILL.md` returns ≥2 lines. *Insertion sites (current-verified — within ±3 lines of PRD, no material drift):* **SKILL.md:867-873** (PRD-cited :870 — A.9 separate-counters invariant tail; new subsection lands here); **SKILL.md:1547-1553** (PRD-cited :1550 — Behavioral Constraints hard-invariants list, new item ~12.5); **rf-task-builder.md:334-361** (PRD-cited 336-359 — QA-gate fix-cycle encoding table); **rf-qa.md:308-315** (PRD-cited 310-313 — Fix Cycle Protocol Rules; the existing SHOULD bullet at ~:312 is promoted to a MUST-halt). *Negative:* legitimate slow-cycle correction MUST NOT be halted — any cycle where `|F|` strictly shrinks (even by 1) continues; the four independent retry counters MUST NOT be collapsed into a shared monotonicity state; no halt-on-slow-convergence threshold is permitted (X-003 REJECTED); monotonicity is consulted only when `|F_n| > 0` (gate-PASS termination precedes the check). The existing 3-cycle hard cap at **rf-team-lead.md:417** and the per-gate fix-cycle table at **rf-task-builder.md:354-360** are preserved unchanged; the new halts compose as earlier exit paths. |
| **FR-CONV.6** | After a partition agent's entire escalation ladder exhausts (rf-analyst, rf-qa, or rf-qa-qualitative partition instance), emit a synthetic HIGH-severity finding (`source: "synthetic-dnsp"`) into the agent's output stream rather than silently aborting the gate. Dedup key: `(assigned_files_range, escalation_ladder_exhaust_point)`. CASE B (PR-03 BASE — no `/sc:tasklist` conflict). Invariant alignment: **zero-trust QA + evidence-bound-item + parallel-research**. | Must Have | **Given** ≥1 partition agent succeeded AND ≥1 partition agent's escalation ladder exhausted, **when** the exhaust occurs, **then** the exhausted agent emits a JSON-or-block finding with all 5 fixed fields (`severity: HIGH`, `source: "synthetic-dnsp"`, `affected_range`, `evidence`, `recommendation: "Manual review required — partition agent failed twice"`) plus `dedup_key` and `found_n_times`; **when** two synthetic findings share an identical dedup-key, **then** they collapse into one record with a `found N times` note; **when** zero partition agents succeeded, **then** NO synthetic emits and the existing all-agents-fail escalation runs. *Verification:* a twice-timeout partition fixture produces a synthetic-dnsp finding with all 5 fields in the gate output; two identical-exhaust events collapse to one finding with `found N times`; an all-agents-fail fixture emits zero synthetic and activates the existing escalation; `grep -n "synthetic-dnsp" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md` returns ≥1 hit per file at the partition-protocol section. *Insertion sites (current-verified — within ±2 lines of PRD):* **SKILL.md:572-656** (A.8 Research Quality Gate — orchestrator-side consumption); **SKILL.md:870-918** (A.10 Task File Validation — orchestrator-side consumption); **rf-analyst.md:58-71**, **rf-qa.md:68-79**, **rf-qa-qualitative.md:70-80** (partition-protocol blocks — within-agent emission contract). *Negative:* synthetic-dnsp MUST NOT emit before the escalation ladder exhausts — the all-agents-fail guard runs first; the existing escalation at **rf-team-lead.md:417** ("Fix Cycles … max 3 cycles per phase") MUST NOT be replaced or short-circuited — **this line is current-verified with NO DRIFT** (file 07 sed-verification; the research-notes earlier line-414 hypothesis was WRONG, per SC-6); synthetic findings MUST NOT mask real findings (HIGH severity ensures gate visibility); the dedup-key collapse MUST NOT cross-cycle (FR-CONV.5 monotonicity treats cross-cycle identical-key as not-regression per INV-012). |

**Cross-FR dependency chain (PRD §17, SC-6 corrected):** FR-CONV.1 (first-mover, zero
outbound deps) → FR-CONV.2 (depends on TB-Add-7/8 live) → FR-CONV.3 (depends on TB-Add
catalogue for INV-010 dynamic enumeration + TB-Add-7 cross-validation in the verdict
table) → FR-CONV.4 (depends on FR-CONV.3 inherited-PASS composition INV-013 + FR-CONV.1
GOAL plumbing) → FR-CONV.5 (depends on FR-CONV.1 `F_n` count + FR-CONV.6 synthetic-dnsp
dedup-key shape) → FR-CONV.6 (depends on FR-CONV.5 monotonicity to consume the dedup-key).
Note the FR-CONV.5 ↔ FR-CONV.6 mutual reference is resolved by landing order: FR-CONV.5
lands 5th specifying the dedup-key *shape it will consume*; FR-CONV.6 lands 6th *emitting*
that shape.

---

## §5.2 Non-Functional Requirements

This is a **generation-time skill** (task-builder), not a runtime service. The template
sub-sections below have been adapted accordingly: RPS / latency / MTTR / MTBF rows are
N/A and have been replaced with token-cost ratio, Determinism SLOs, and
invariant-preservation guarantees.

### §5.2.1 Performance Requirements

| NFR | Requirement | Target | Measurement |
|-----|-------------|--------|-------------|
| **NFR-CONV.4** | Token-cost ratio (post-merge / pre-merge) per equivalent BUILD_REQUEST | **≤1.10** | Sample 5 representative BUILD_REQUESTs covering Quick/Standard/Deep tiers; record pre-merge and post-merge total token counts for the full task-builder generation pipeline; compute ratio. OPEN-TOKEN tracks empirical measurement post-merge. Contingency K-010: if exceeded, profile per-FR contribution and summarise the FR-CONV.3 Inherited Structural Verdict table rather than emit it verbatim. |
| **NFR-CONV.5** | Wall-clock impact: no new external dependencies, no synchronous network calls added; gate additions are local checks | Diff inspection shows only existing tools (Read, Grep, Glob, Bash) used | Inspect the rf-qa.md and SKILL.md diffs for any new tool invocation beyond the four-tool set; reject the diff if any new external dep or synchronous network call appears. |

(RPS, latency, throughput rows omitted — N/A for a generation-time skill.)

### §5.2.2 Reliability Requirements

| NFR | Requirement | Target | Measurement |
|-----|-------------|--------|-------------|
| **NFR-CONV-R1** | Single-pass gate PASS rate (baseline) | **≥80%** of representative BUILD_REQUESTs PASS the task-integrity gate on the first cycle (no fix-cycle required) | Run the 5 representative BUILD_REQUESTs from NFR-CONV.4 measurement; count first-cycle PASS verdicts. Failures route through the FR-CONV.5 fix-cycle protocol (max 3 cycles, monotonicity + regression guards). |
| **NFR-CONV.3** | Hidden-input determinism (per FR §6.2 F4) | Fixture-populated `.dev/tasks/done/` produces byte-identical structural output to empty `.dev/tasks/done/` | Run task-builder against an identical BUILD_REQUEST with `.dev/tasks/done/` (a) empty and (b) populated with 10+ historical tasks of ≥3 distinct task_types; diff the structural output fields (TB-Add-* verdicts, synthetic-dnsp 5 fields, dedup-key, axis column); structural fields must be byte-identical. **PR-05 advisory mechanism is REJECTED for Phase-1** — task-builder MUST NOT read any input outside BUILD_REQUEST + source-tree that could modify behavior. |

(MTTR / MTBF / availability rows omitted — N/A for generation-time skill.)

### §5.2.3 Determinism SLOs (replacing "Service Level Objectives")

| NFR | Determinism scope | Target | Measurement |
|-----|-------------------|--------|-------------|
| **NFR-CONV.1** | Structural fields — gate outputs deterministic | TB-Add-1..8 PASS/FAIL verdicts, synthetic-dnsp 5 fixed fields + dedup-key, axis column values, Items Reviewed table structure are **byte-identical** across two runs on the same BUILD_REQUEST + source tree | Re-run task-builder on identical BUILD_REQUEST twice; diff the rf-qa A.10 verdict table and the rf-qa-qualitative Items Reviewed table; all structural fields must be byte-equal. |
| **NFR-CONV.2** | Research-driven prose — explicitly excluded from determinism scope | Per-item Context prose and rf-qa-qualitative semantic-check prose remain LLM-research-driven; byte-equality is **not** required | Diff prose between two runs; non-byte-equality is acceptable. Structural annotations within prose (axis labels, finding counts, dedup-keys) MUST remain byte-equal regardless of surrounding prose drift. |

### §5.2.4 Security Requirements

This is an internal generation-time framework. The security model is minimal and is
operationalised as **invariant preservation** rather than authn/authz/encryption.

| Requirement | Statement |
|-------------|-----------|
| **No new data collection / storage / transmission** | NFR-CONV.5 forbids new external deps and synchronous network calls; no new data sinks introduced. |
| **Anti-inflation rule preservation** | The anti-inflation rule at **rf-qa-qualitative.md:766-775** (Prohibited Behaviors items 1-6 + Tool Engagement Minimum) MUST NOT be weakened, removed, or rephrased by FR-CONV.3. The rule's load-bearing line is :770 ("NEVER mark an item VERIFIED if you only read about it in another report — that is RELIANCE, not VERIFICATION"). FR-CONV.3's inherited verdict is a deliberately-scoped RELIANCE channel for **structural** items only; semantic items continue to require independent tool calls. |
| **Five load-bearing invariants ARE the security model** | self-contained-item, evidence-bound-item, persistent-`.dev/tasks/`-artifact, zero-trust QA, parallel-research are preserved by the NFR-CONV.6..10 acceptance fixtures (§5.2.5). A regression in any invariant surfaces as a gate failure rather than silent drift. |

### §5.2.5 Invariant Preservation (NFR-CONV.6..10)

Each row maps an invariant to its current-verified operational source, and the synthetic
acceptance fixture defined in PRD §14.2.

| NFR | Invariant | Operational source (current-verified file:line) | Fixture / Pass-Fail Behavior |
|-----|-----------|-------------------------------------------------|-------------------------------|
| **NFR-CONV.6** | self-contained-item | **SKILL.md:1452-1457** (5-field per-item schema). **SC-1 OPEN:** PRD §25.4 declares the schema is `{Description, Context, Acceptance, Confidence, Verification}` but current SKILL.md:1450-1460 reads `{Context, Action, Output, Verification, Completion gate}`. This contradiction is escalated to TDD §22 Open Questions — Engineering Lead decision required. The fixture targets *whichever schema lands* (schema integrity, not field naming). | Synthetic fixture with all 5 fields populated **PASSES** all 8 TB-Add checks; same fixture with one field stripped **FAILS** TB-Add-1 (fails closed). |
| **NFR-CONV.7** | evidence-bound-item | **SKILL.md:1530 rule #2** ("Evidence-based claims only. Every finding must cite actual file paths, line numbers, function names...") | Three-fixture triple: (a) `Context: src/foo` (bare, no `:N`) → **FAILS** TB-Add-8; (b) `Context: src/foo:42` → **PASSES**; (c) `Context: <none — pure refactor> [justified-absence]` → **PASSES**. |
| **NFR-CONV.8** | persistent-`.dev/tasks/`-artifact | OPEN-INV-018 / `SKILL.md:1536 rule #5` ("Preserve research artifacts...persist after the task file is built"). Convention-bound; no single line number. | Diff the `.dev/tasks/<task-id>/` directory layout pre-merge vs post-merge. **PASS** when zero structural changes occur: no new mandatory subdirectory, no rename of `research/`/`qa/`/`synthesis/`/`reviews/`/`adversarial/`, no naming-pattern change for the task-file name. |
| **NFR-CONV.9** | zero-trust QA | **rf-qa.md:141-142** (verbatim PASS/FAIL definitions; surrounding heading at :144 — per SC-8, cite :141-142 for the verdict definitions, **not** the PRD-asserted :144-146). Verbatim: `**PASS** — All checks pass, no gaps of any severity. … **FAIL** — Any gaps exist (CRITICAL, IMPORTANT, or MINOR). … ALL gaps must be resolved before proceeding — no severity level is exempt.` | Two-part fixture: (a) 1-LOW-finding fixture → gate **FAILS** (proves "any gap regardless of severity = FAIL"); (b) FR-CONV.3 inherited-verdict applied to a task file → no item is marked VERIFIED unless the Self-Audit lists an independent semantic-check engagement. |
| **NFR-CONV.10** | parallel-research | **rf-qa.md:49-77** (Parallel Partitioning) + **rf-qa-qualitative.md:50-82** (identical Parallel Partitioning). INV-021: DNSP fires within-agent-instance. | Spawn-log inspection fixture: **N partition agents spawn concurrently** (timestamp overlap proves concurrency); on one agent's escalation exhaust, **N-1 partitions continue to completion** before that one synthesises a DNSP finding. **FAIL** if the cohort serialises or DNSP fires cross-cohort. |

**Cross-coverage check (from invariant-preservation research file 14 §3):** Every
UNADDRESSED-MEDIUM finding from the Round-2.5 invariant probe (INV-002, INV-010,
INV-012, INV-015) is routed through ≥1 FR Negative Criterion in §5.1, so a regression
manifests as a gate failure rather than silent invariant drift. Across the six FRs the
coverage matrix is: self-contained-item (FR-CONV.2 negative); evidence-bound-item
(FR-CONV.1 TB-Add-8 + FR-CONV.2 negative); persistent-artifact (FR-CONV.3 read-target
stability); zero-trust QA (FR-CONV.1/3/4/5/6 negatives — 4-of-6 coverage);
parallel-research (FR-CONV.6 negative). No invariant is uncovered.

---

## Open Questions Routed from §5

Surfaced during research-gate consolidation (SC-1..SC-8); summarised here for
traceability, treated in full elsewhere in the TDD:

1. **SC-1 [Critical → TDD §22 Open Question]** — PRD §25.4 vs current SKILL.md:1452-1457
   schema contradiction. Affects the NFR-CONV.6 fixture phrasing. Resolution requires
   Engineering Lead input; NFR-CONV.6 here targets the schema that ultimately lands.
2. **SC-2 [resolved in FR-CONV.6, §5.1]** — DNSP partial-vs-all-fail semantics codified
   as the all-agents-fail guard precedence rule.
3. **SC-3 [resolved in FR-CONV.4, §5.1]** — Five Adversarial Axes canonical definitions
   listed inline in the FR-CONV.4 row.
4. **SC-4 [resolved in FR-CONV.5, §5.1]** — Per-gate fix-cycle cross-file coupling
   disambiguated: caps live in rf-task-builder.md:354-360, global cap in
   rf-team-lead.md:417, monotonicity guards layered on top per FR-CONV.5.
5. **OPEN-INV-006** — TB-Add-2 item-count bounds remain `[ADVISORY]` until empirical
   calibration in Phase-2 alongside PR-05 re-evaluation.
6. **OPEN-TOKEN (NFR-CONV.4)** — empirical token-ceiling measurement on 5 representative
   BUILD_REQUESTs post-merge.
7. **OPEN-INV-018** — `.dev/tasks/` directory-structure stability contract; portfolio
   re-integration trigger if layout changes.

---

**Status:** Complete

