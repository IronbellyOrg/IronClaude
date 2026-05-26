# Matrix: capabilities sc:tasklist has that task-builder lacks

Each row is a candidate import for the inverse-direction merge (sc:tasklist → task-builder). Disposition pre-classifies the Phase 3 proposal:
- `IMPORT-AS-IS` — direct port, no architectural adaptation
- `IMPORT-ADAPTED` — port the intent, adapt the mechanism to task-builder's architecture
- `REJECT` — conflicts with a protected task-builder invariant (CLAUDE.md G6: self-contained-item, evidence-bound-item, persistent .dev/tasks/ artifact, zero-trust QA, parallel research)

---

### M-SC-01: Deterministic generation guarantee (same input → same output)
- **sc:tasklist source**: SKILL.md:14, 36–37 ("Deterministic: same input -> same output", "no discretionary choices") — Bucket A digest
- **FINAL-REPORT reference**: §3.1 ("single-pass deterministic transform"), §4 row "Determinism", §6.2 F4 ("hidden input" framing)
- **task-builder status**: absent (Bucket C SKILL.md:88, 201 — "Scenario B → Researchers do broad exploration", non-determinism explicit)
- **Candidate disposition**: REJECT (conflicts with task-builder invariant: parallel research)
- **One-line rationale**: blanket determinism contradicts the parallel-agent exploration model; CB-5 advises scoped-determinism only (e.g., frontmatter-stable, ID-stable).

### M-SC-02: 17-point pre-write quality gate
- **sc:tasklist source**: SKILL.md:979–1034 (enumerated checks 1–20 across Sprint/Semantic/Structural sections) — Bucket A digest
- **FINAL-REPORT reference**: §3.1 ("17-point quality gate runs before any file is written"), §6.2 F3 (gate redundancy observation)
- **task-builder status**: partial (Bucket C SKILL.md:898–906 task-integrity 9-item; SKILL.md:1491–1507 task-file validation 15-item; CB-3 advisory — "must classify per-check, not in bulk")
- **Candidate disposition**: IMPORT-ADAPTED (residual checks land in rf-qa task-integrity or rf-qa-qualitative checklists)
- **One-line rationale**: many checks already exist in task-builder's 4 gate stages; the unique additions (e.g., placeholder/TBD scan, circular-dependency detection, XL splitting) strengthen zero-trust QA without violating any invariant.

### M-SC-03: 2N-parallel adversarial validation agents
- **sc:tasklist source**: SKILL.md:1091–1106 ("Agent spawning algorithm (deterministic): … split = ceil(task_count / 2)") — Bucket A digest
- **FINAL-REPORT reference**: §3.1 ("Validation Stages 7-10 spawn 2N parallel agents"), §4 row "Quality gates"
- **task-builder status**: partial (Bucket C SKILL.md:643 — partitions when >6 research files; rf-qa supports assigned_files partitioning per Bucket D rf-qa.md:50–77)
- **Candidate disposition**: IMPORT-ADAPTED (extend partitioning to "split task-file checklist into A/B halves for adversarial review")
- **One-line rationale**: task-builder's parallel-research invariant already supports partitioned QA; generalising to task-checklist halves preserves invariants.

### M-SC-04: Drift / contradiction / omission / weakened-criteria / invented-content checks
- **sc:tasklist source**: SKILL.md:1112–1117 (5-category adversarial agent prompt) — Bucket A digest
- **FINAL-REPORT reference**: §3.1 ("Checks: drift, contradictions, omissions, weakened criteria, invented content")
- **task-builder status**: partial (Bucket C SKILL.md:621/878/895/929 adversarial stance "find what was missed"; rf-qa-qualitative has contradiction/scope checks per Bucket D rf-qa-qualitative.md:789, 791)
- **Candidate disposition**: IMPORT-ADAPTED (named checklist topics into rf-qa-qualitative's task-qualitative phase)
- **One-line rationale**: same adversarial intent already lives in rf-qa-qualitative; named categories sharpen the existing checklist without violating any invariant.

### M-SC-05: R-### → T<PP>.<TT> → D-#### traceability matrix
- **sc:tasklist source**: SKILL.md:596–600, 672–707 (Roadmap Item Registry / Deliverable Registry / Traceability Matrix) — Bucket A digest
- **FINAL-REPORT reference**: §4 row "Traceability" ("Full: R-### → T<PP>.<TT> → D-#### → artifact paths → Tier → Confidence")
- **task-builder status**: absent (Bucket C §"Traceability matrix: absent", CB-6)
- **Candidate disposition**: IMPORT-ADAPTED (partial only — T<PP>.<TT> → D-#### inside a task file; R-### half requires roadmap input task-builder does not consume)
- **One-line rationale**: per-checklist-item IDs and deliverable IDs are additive (CASE-B clean), but the upstream `R-###` namespace presupposes a roadmap input that violates task-builder's BUILD_REQUEST/GOAL input contract.

### M-SC-06: Tier classification (STRICT / STANDARD / LIGHT / EXEMPT with keyword scoring)
- **sc:tasklist source**: SKILL.md:505–575, rules/tier-classification.md:33–71 (compound-phrase overrides + keyword scoring + context boosters + confidence formula) — Bucket A digest
- **FINAL-REPORT reference**: §4 row "Tier classification" ("Deterministic: compound phrases → keyword scan → context boosters. 4 tiers, confidence scoring")
- **task-builder status**: different model (Bucket C SKILL.md:90–101 — 3-tier Quick/Standard/Deep controls *research depth*, not artifact compliance; CB-4)
- **Candidate disposition**: REJECT (conflicts with task-builder invariant: tier ≡ research depth)
- **One-line rationale**: the two tier systems classify orthogonal things; importing the compliance-tier keyword algorithm would either replace the working research-depth rule or produce a parallel scoring with no consumer.

### M-SC-07: DNSP synthetic-finding behavior (Detect → Nudge → Synthesize → Proceed)
- **sc:tasklist source**: SKILL.md:1150 ("Zero agent failures (if an agent fails, retry once before reporting error)") — Bucket A digest (current behavior is abort-on-fail)
- **FINAL-REPORT reference**: §7 R1 (proposed DNSP for Validation Agents — synthesize conservative HIGH-severity finding flagging the affected task range)
- **task-builder status**: absent (Bucket D rf-analyst.md is read-only and currently has no synthesis-on-agent-failure behavior; rf-team-lead spawns gap-fills but not synthetic findings)
- **Candidate disposition**: IMPORT-AS-IS (host: rf-analyst per Bucket D §"Surfaces relevant"; emit `source: "synthetic-dnsp"` HIGH-severity finding when a partition agent fails after retry)
- **One-line rationale**: synthetic findings preserve evidence-bound-item (cite the failed range), preserve zero-trust QA (surface gap rather than hide), and survive without violating parallel-research.

### M-SC-08: Quality-gate results passthrough to validation agents
- **sc:tasklist source**: FINAL-REPORT R3 design (extend Stage 6 to emit `validation/gate-results.txt`; inject into Stage 7 agent prompts) — design proposal, not yet in SKILL.md
- **FINAL-REPORT reference**: §7 R3 (Quality Gate Evidence Passthrough)
- **task-builder status**: absent (rf-qa structural results are reported via SendMessage but not piped as context into rf-qa-qualitative's prompt — Bucket D rf-qa-qualitative.md:101 just spawns after structural pass without inheriting findings)
- **Candidate disposition**: IMPORT-AS-IS (rf-qa → rf-qa-qualitative gate-results context injection)
- **One-line rationale**: pipes verified PASS items so qualitative review skips structural re-checking and focuses on semantic quality; consistent with rf-qa-qualitative's existing "do not re-verify what rf-qa already checks" rule (Bucket D rf-qa-qualitative.md:794).

### M-SC-09: Dual-mode patch recovery with monotonicity guard
- **sc:tasklist source**: FINAL-REPORT R4 design (interactive: AskUserQuestion on UNRESOLVED; automated: one retry cycle with full-set re-validation + monotonicity guard + regression detection, cap at 2 passes) — design proposal
- **FINAL-REPORT reference**: §7 R4 (Dual-Mode Patch Recovery), §6.2 F2 (subset-only re-validation oscillation defect)
- **task-builder status**: partial (Bucket C SKILL.md:651, 859, 865, 870 — retry budgets exist: research-gate 3, RESEARCH_NEEDED 2, MALFORMED 2; but no monotonicity guard or full-set re-validation requirement; no regression detection)
- **Candidate disposition**: IMPORT-ADAPTED (formalize existing retry budgets with monotonicity guard and regression detection)
- **One-line rationale**: task-builder already retries; adding "halt if |UNRESOLVED| doesn't shrink" and "halt if previously-passing item regresses" hardens the existing loop without violating any invariant.

### M-SC-10: Tier-calibration advisory (read feedback-log.md, surface override patterns)
- **sc:tasklist source**: FINAL-REPORT R5 design (Stage 0 reads `feedback-log.md`, emits `## Tier Calibration Advisory` in index; advisory-only, all tiers still computed from roadmap text alone) — design proposal
- **FINAL-REPORT reference**: §7 R5, §6.2 F4 (hidden-input framing — advisory-only resolves the determinism violation)
- **task-builder status**: absent (no feedback-log mechanism; task files are one-shot per GOAL)
- **Candidate disposition**: IMPORT-ADAPTED (advisory-only form; surface override patterns from prior `.dev/tasks/` runs as a non-binding header section)
- **One-line rationale**: advisory-only preserves evidence-bound-item (feedback log is itself an evidence file with file:line citations) and does not violate determinism because no scoring is modified.

### M-SC-11: Task-execution-context block (roadmap refs + source areas, no specific file paths)
- **sc:tasklist source**: FINAL-REPORT R2 design (`## Execution Context` section per task: roadmap item refs always, source areas when inferable, no specific file paths) — design proposal
- **FINAL-REPORT reference**: §7 R2, §6.2 F1 (per-step paths unreliable; roadmap refs are the high-value low-risk element)
- **task-builder status**: different model (Bucket C SKILL.md:900, 1452–1457 — self-contained items already embed context+action+output+verification+completion-gate; but task-builder *requires* file:line citations per evidence-bound-item invariant)
- **Candidate disposition**: IMPORT-ADAPTED (adopt "source areas not specific paths" framing for the executor's view of context; evidence-bound file:line citations stay in research notes)
- **One-line rationale**: source-area framing protects against path staleness while file:line citations in the persistent research/*.md files preserve evidence-bound-item.

### M-SC-12: Appearance-order ID assignment + explicit 4-rule tiebreakers
- **sc:tasklist source**: SKILL.md:156–159, 276–280, 419–426 (R-### and T<PP>.<TT> and D-#### appearance-order); SKILL.md:374–383 (4-rule cascade: roadmap-named > no new deps > reversible > fewest interface changes) — Bucket A digest
- **FINAL-REPORT reference**: §3.1 ("keyword-based scoring, appearance-order IDs, explicit tiebreakers")
- **task-builder status**: absent (Bucket C: only `TASK_ID` and template `1.1`/`1.2` numbering)
- **Candidate disposition**: IMPORT-ADAPTED (formal T<PP>.<TT> scheme for checklist items inside a task file; tiebreaker rules for "which checklist item to write first when several appear in research")
- **One-line rationale**: deterministic-within-a-task ID assignment is additive and complements evidence-bound-item by giving each checklist item a stable handle for QA references.

### M-SC-13: Spot-check no-loop policy
- **sc:tasklist source**: SKILL.md:1266, 1288 ("A single verification pass… If any remain UNRESOLVED, they are logged but the skill does NOT loop") — Bucket A digest
- **FINAL-REPORT reference**: §4 row "Correction capability" ("1 pass: patch + spot-check, log UNRESOLVED, stop")
- **task-builder status**: different model (Bucket C / Bucket D — multi-cycle: rf-qa 3 fix cycles, rf-task-builder per-gate fix limits 2–3, multiple retry budgets stacked)
- **Candidate disposition**: REJECT (conflicts with task-builder invariant: zero-trust QA depends on fix-cycle retries)
- **One-line rationale**: no-loop is a sc:tasklist-specific token-saving optimisation; importing it would remove the multi-cycle correction that zero-trust QA in task-builder relies on (Bucket D rf-qa.md:310–313).

### M-SC-14: Write atomicity (all-or-nothing bundle write after full gate pass)
- **sc:tasklist source**: SKILL.md:981, 1042 ("All checks in this section MUST pass before any Write() call. Invalid output is never written.") — Bucket A digest
- **FINAL-REPORT reference**: §3.1 ("Write atomicity… No partial bundle writes are permitted")
- **task-builder status**: different model (Bucket C SKILL.md:819–832, 437–449, 1196–1209, 1542 — "INCREMENTAL TASK FILE WRITING (MANDATORY — NEVER ONE-SHOT)")
- **Candidate disposition**: REJECT (conflicts with task-builder invariant: persistent .dev/tasks/ artifact + no-one-shotting rule)
- **One-line rationale**: write-atomicity directly contradicts task-builder's mandated incremental write protocol and would prevent the persistent evidence trail from existing during the build.
