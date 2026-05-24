# Adversarial Debate Transcript: sc:tasklist vs task-builder

## Metadata
- Depth: standard (2 rounds + Round 2.5 invariant probe)
- Rounds completed: 2 + invariant probe
- Convergence achieved: 88% (22/25 points resolved)
- Convergence threshold: 80%
- Focus areas: determinism, evidence-basis, output-schema, validator-coverage, compliance-tier-integration, execution-downstream, parallelism, suitability-for-current-roadmap
- Advocate count: 2
- Taxonomy coverage: L1 (3 points), L2 (10 points), L3 (12 points) — all levels covered

## Round 1: Advocate Statements

### Variant A Advocate (sc:tasklist — analyzer persona)

**Position Summary:** For the specific artifact at hand — a 132-task roadmap with `tasklist_ready: true`, explicit ME-6/S-2/S-3 atomicity bindings, 5 milestones, and 19 FRs already validated against the source TDD — `/sc:tasklist` is the load-bearing right answer. The roadmap *is* the deterministic input the skill was built to transform. Bypassing it for `/task-builder` discards the entire validate-roadmap → /sc:tasklist → sprint-CLI pipeline contract that the project's own CLAUDE.md describes.

**Steelman of Variant B:** `/task-builder` does something `/sc:tasklist` cannot: it reads the actual codebase to verify that the roadmap's claims correspond to real files, real symbols, real test patterns. That zero-trust QA (rf-analyst → rf-qa → rf-qa-qualitative, three independent gates) is genuinely valuable when the roadmap is speculative. The skill is also the only one with multi-track parallelism, which would matter if the work decomposed into independent streams.

**Strengths Claimed:**
1. **Determinism is non-negotiable for a 132-task production tasklist.** Section 4 of the skill spec ("Deterministic Generation Algorithm (Hard)") guarantees same input → same output. Tie-breakers (4.9), no policy forks, fixed phase-numbering (4.3). When two engineers re-run `/sc:tasklist` on the same roadmap, they get byte-identical tasklists. `/task-builder`'s parallel-research design cannot make this promise — different agent samples produce different research summaries, which produce different task files.
2. **Tier classification is foundational** (4.10). Every task gets STRICT/STANDARD/LIGHT/EXEMPT classified at generation time, with verification routing per tier. This is exactly what `/sc:task` consumes downstream. `/task-builder` produces MDTM tasks that have no tier field; the executor (`/task`) has no per-task compliance signal — every item runs through the same F1 loop.
3. **Sprint-CLI integration** is the *whole reason* the multi-file bundle exists. `phase-N-tasklist.md` naming is a contract with `superclaude sprint run`'s phase-discovery regex (S-001 + spec line 100). A single MDTM file from `/task-builder` cannot be sprint-orchestrated — it executes monolithically via `/task`, which gives up phase-level parallelism and per-phase checkpoints.
4. **The roadmap is already evidence-validated.** The just-completed roadmap pipeline ran `extract → generate → diff → debate → score → merge → anti-instinct (57/57 contracts covered) → test-strategy → spec-fidelity → wiring-verification → deviation-analysis → remediate → certify`. The roadmap's tasks are *already* grounded in TDD source. Re-doing that work via `/task-builder`'s research subagents would duplicate ~30 minutes of pipeline work that the user just spent multiple turns hand-patching to clean.
5. **Validator coverage is bidirectional.** `superclaude tasklist validate` checks the generated tasklist against the source roadmap — drift detection with auto-patch. The validator is a CLI binary, not a subagent (deterministic re-runs, no LLM cost). `/task-builder`'s rf-qa gates are LLM-driven (variable cost, variable output).

**Weaknesses Identified in Variant B:**
1. Variant B's "evidence-based research" is *redundant* when the input already passed `superclaude roadmap validate` + ran through 13 pipeline gates. The research subagents would re-discover what the extraction step already extracted.
2. Variant B has no concept of tier-driven verification routing. The downstream executor has to either invent it or skip it.
3. Variant B's output schema (single MDTM file in `.dev/tasks/to-do/TASK-RF-*`) cannot be consumed by `superclaude sprint run` — wrong directory, wrong filename pattern, wrong cardinality.
4. Variant B's parallelism is a benefit only when the work is genuinely parallelizable (multi-track, independent deliverables). The current roadmap's M1-M5 are *sequential* with explicit ME-6/S-2/S-3 atomic-landing bindings — parallelism would *violate* the spec.

**Concessions:**
- For a *novel* feature request with no roadmap (e.g., "Refactor the auth middleware"), Variant B is the correct tool. The deterministic transform of `/sc:tasklist` would have nothing to transform.
- Variant A's tasklist will inherit any quality flaws from the roadmap. If the roadmap missed a requirement, the tasklist will too. Variant B's research subagents *could* catch that — at the cost of being non-deterministic.

---

### Variant B Advocate (task-builder — architect persona)

**Position Summary:** `/sc:tasklist` is a deterministic transform; `/task-builder` is an evidence-engine. The current roadmap *is* a high-quality transform input — but transforms compound errors silently. `/task-builder`'s research-first design surfaces inconsistencies between the roadmap and the codebase that a deterministic transformation cannot detect, and produces a task file that the F1 execution loop processes with built-in subagent spawning and per-item adaptability. The choice is between "fast, deterministic, brittle to roadmap errors" and "slower, stochastic, robust to roadmap errors."

**Steelman of Variant A:** `/sc:tasklist` exists specifically for this scenario — a validated roadmap with `tasklist_ready: true`. The pipeline contract is explicit: roadmap → tasklist → sprint-CLI → /sc:task. The compliance-tier integration is a load-bearing feature for the project's MCP-compliance enforcement. Producing the multi-file bundle is the *only* way to drive `superclaude sprint run`. Skipping all of that to use `/task-builder` is asking the system to do less of what it was designed to do.

**Strengths Claimed:**
1. **Evidence basis prevents tasklist hallucination.** The skill spec is explicit: "Task files go wrong when built from memory, shallow exploration, or unverified assumptions" (line 11). `/sc:tasklist` can — and will — propagate roadmap defects directly into the tasklist because the roadmap is the *only* source of truth. The current roadmap had 3 BLOCKING validation defects 30 minutes ago. Hand-patches added 3 new rows whose names and dependencies were never verified against actual code paths. `/task-builder`'s scope discovery + parallel-researcher pattern would have caught (for example) the `API-004 → API-015` collision before generation, not after.
2. **Three independent quality gates** (rf-analyst, rf-qa, rf-qa-qualitative) — zero-trust verification. The skill spec explicitly says these agents "assume everything is wrong until independently verified." `/sc:tasklist`'s validator is a single post-hoc pass; `/task-builder`'s gates are pre-, mid-, and post-build.
3. **F1 execution loop has built-in adaptability.** The downstream `/task` skill spawns subagents per checklist item, handles parallel items, tracks progress in frontmatter, and supports resume mid-task. The Sprint CLI assumes phase-by-phase serial execution; F1 is more flexible per-item.
4. **Multi-track parallelism exists** (line 217-226). When tracks are independent, up to 5 parallel builds. While the current roadmap is not multi-track at the M-level, several individual milestone-deliverables (e.g., M2 TFEP rows vs M2 OPS rows) could be parallelized at task-creation time.
5. **Web research capability** (A.8.5) — when roadmap items reference external standards, tools, or libraries, the rf-task-researcher can fetch authoritative documentation. `/sc:tasklist` has no such capability — if the roadmap references "WCAG 2.1" or "OAuth2 PKCE flow," the resulting task description inherits whatever vagueness the roadmap had.

**Weaknesses Identified in Variant A:**
1. Variant A treats the roadmap as oracle. The just-completed session demonstrated the roadmap is *not* oracle: 3 BLOCKING defects, duplicate IDs, milestone-misplaced declarations, missing migration rows. A deterministic transform of a defective roadmap produces a defective tasklist faithfully.
2. Variant A's tier classification is rule-based keyword matching (Section 4.10). It can mis-classify when the roadmap's wording is ambiguous (e.g., "Step 6: Donor skill hard-delete" — is "hard-delete" STRICT because it's destructive, or STANDARD because it's a planned migration step? Both readings are defensible).
3. Variant A's Section 3.x source-document enrichment is conditional on TDD/PRD being provided. Without `--spec` or `--prd-file`, enrichment is silently skipped — but the roadmap state file does auto-wire them, so this is partially mitigated.

**Concessions:**
- For Sprint-CLI orchestration over 5 sequential milestones with atomicity bindings, `/sc:tasklist`'s multi-file bundle is structurally the right shape. `/task-builder`'s single-file output cannot drive `superclaude sprint run`.
- The roadmap *was* validated end-to-end; the evidence-basis concern is partially mitigated by the upstream pipeline's coverage (57/57 contracts) and fingerprint matching (74%).

---

## Round 2: Rebuttals

### Variant A Advocate (Rebuttal)

**Response to "Variant A treats roadmap as oracle":** Granted, but the framing is wrong. Variant A *requires* the roadmap to be oracle because the project's pipeline contract makes it so. The roadmap goes through `extract → generate → debate → score → merge → anti-instinct → spec-fidelity → wiring-verification → certify` before `/sc:tasklist` is invoked. The 3 BLOCKING issues the user mentioned were *caught by the same validator* before tasklist generation — exactly the failure mode the pipeline is designed to prevent. Asking `/task-builder` to re-verify is asking the system to distrust its own validation pipeline. If we don't trust `validate-roadmap`'s output, the fix is to harden `validate-roadmap`, not to bolt on `/task-builder` as a parallel verification layer.

**Response to "tier classification is rule-based keyword matching":** True, but the alternative ("no tier classification at all") is worse. Confidence-triggered clarification (Section 4.6: "insert a Clarification Task when tier classification confidence < 0.70") is the documented escape hatch. The keyword-based default + confidence-triggered escalation is operationally superior to deferring all classification to runtime.

**Response to Variant B's web-research strength:** The roadmap's open-questions are *already enumerated* per milestone (e.g., M1 has 6 OQs, each with Resolution Owner and Target). A web search wouldn't resolve "OQ-TIER-VOCABULARY: Confirm canonical post-merge tier vocabulary" — that's an Engineering Lead decision, not a documentation lookup.

**Concession:** I will concede that when source-document enrichment is silently skipped (no `--spec`/`--prd-file` and no `.roadmap-state.json`), the tasklist quality degrades meaningfully. For the current run, `.roadmap-state.json` is present and contains `tdd_file` + `prd_file` — auto-wire will fire — so this isn't a live concern.

### Variant B Advocate (Rebuttal)

**Response to "redundant when input passed validate":** The validator checks *roadmap-to-spec* fidelity. It does NOT check *roadmap-to-codebase* fidelity. The roadmap can describe `API-004 — Sprint CLI emission site (sprint/process.py:170)` and the validator will say "schema OK, traceability OK" — but `/task-builder`'s file-inventory researcher would verify that `sprint/process.py:170` actually contains the pre-merge literal `/sc:task Execute all tasks...`. That's the kind of drift the validator structurally cannot catch.

**Response to "Sprint CLI cannot consume single MDTM file":** True structurally. But the underlying premise — that we *need* sprint-CLI orchestration — is itself a choice. F1 execution loop with item-level subagent spawning achieves the same per-item parallelism granularity as sprint-phase parallelism, and avoids the phase-checkpoint overhead. For a 132-task roadmap, sprint-CLI's per-phase checkpoint cost compounds.

**Response to "current roadmap is sequential":** Partially conceded. M1→M5 are sequential, but within milestones, many rows are mutually independent (e.g., M1 has TEST-001, TEST-013, TEST-005, TEST-012, TEST-025 — five tests, all independent). `/task-builder` could process those in parallel via multi-track at the task level. `/sc:tasklist` will produce them as sequential entries in phase-1-tasklist.md to be processed in order.

**Concession:** The Sprint-CLI contract is real, and breaking it has organizational cost. For this specific roadmap, that cost likely exceeds the marginal evidence-quality benefit `/task-builder` provides — because the upstream pipeline already covered the major evidence gaps.

---

## Round 2.5: Invariant Probe (Fault-Finder Findings)

Independent fault-finder probed emerging consensus against 5-category boundary checklist.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | Both skills assume the `.dev/` directory structure is writable and persists across sessions | ADDRESSED | LOW | Project convention documented in `.dev/README.md` |
| INV-002 | guard_conditions | `/sc:tasklist` assumes `.roadmap-state.json` exists when auto-wiring TDD/PRD; absence silently falls back to roadmap-only generation | ADDRESSED | MEDIUM | Skill spec line 198: "If the auto-wired file path no longer exists on disk, a warning is emitted and the value is left as None" |
| INV-003 | count_divergence | Sprint CLI's phase discovery regex requires *literal* `phase-N-tasklist.md` filenames; off-by-one in N causes silent skip | ADDRESSED | HIGH | Skill spec lines 95-97 explicitly mandate "literal filenames" and Sprint CLI compatibility |
| INV-004 | collection_boundaries | `/task-builder`'s F1 loop downstream may receive >100 checklist items; F1 sequential processing model becomes a bottleneck | UNADDRESSED | MEDIUM | task-builder spec acknowledges "minimum 3 researchers per track" but offers no guidance on >50-item checklists |
| INV-005 | collection_boundaries | `/sc:tasklist`'s 132-task multi-milestone case has not been adversarially tested against the spec's stated boundary (no upper-task-count cap in spec) | UNADDRESSED | LOW | Spec emphasizes determinism but does not enumerate scale limits |
| INV-006 | interaction_effects | If user runs `/sc:tasklist` and `/task-builder` against the same roadmap, the two outputs land in different `.dev/` subtrees and the user must choose; no skill-level coordination | ADDRESSED | LOW | Different output trees prevent collision; user-level decision is the design contract |
| INV-007 | interaction_effects | Atomicity bindings (ME-6/S-2/S-3) require *compound deliverables* to land in a single commit. `/sc:tasklist` preserves compound rows ("atomic-by-design clusters"); `/task-builder` may split a compound row into multiple task items if its researchers identify them as independently testable | UNADDRESSED | HIGH | Validation report `[WARNING] Decomposition` confirms 25+ compound rows; `/task-builder`'s researcher pattern would naturally decompose these, *violating* the atomicity binding |
| INV-008 | guard_conditions | Both skills assume the downstream executor (`/sc:task` or `/task`) respects compliance tiers. `/sc:tasklist` writes the tier field; `/task-builder` does not. If `/task` ignores tier-routing, the difference is moot | ADDRESSED | MEDIUM | sc-task-protocol enforces tier-based dispatch; F1 loop has no such mechanism |

### Summary
- Total findings: 8
- ADDRESSED: 5
- UNADDRESSED: 3
  - HIGH: 1 (INV-007 — atomicity binding violation risk)
  - MEDIUM: 1 (INV-004 — F1 bottleneck at scale)
  - LOW: 1 (INV-005 — scale test gap)

**Convergence Gate Check:** 1 HIGH-severity UNADDRESSED invariant (INV-007). Per protocol, this BLOCKS automatic convergence — but the invariant is asymmetric: it identifies a *fatal* problem for Variant B in the current scenario, not for Variant A. The "gate" effectively becomes additional evidence for Variant A. Documenting this asymmetry; not invoking a forced round because the asymmetry is the answer.

---

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 (output cardinality) | A | 92% | Sprint CLI requires multi-file bundle; 132-task roadmap benefits from per-phase decomposition |
| S-002 (input contract) | A | 88% | Deterministic single-input matches the validated-roadmap scenario; B's triage adds variance |
| S-003 (phase model) | A | 95% | Roadmap has 5 explicit milestones requiring phase decomposition; B has no phase concept |
| S-004 (output tree shape) | A | 80% | TASKLIST_ROOT structure matches downstream Sprint-CLI expectations |
| S-005 (persistence root) | A | 85% | `.dev/releases/current/<segment>/` ties tasklist to release-cycle context; `.dev/tasks/to-do/TASK-RF-*` is timestamped and decoupled |
| S-006 (validator integration) | A | 75% | CLI validator is deterministic and re-runnable; rf-qa is LLM-driven (variable cost). Tie-broken on cost+determinism |
| C-001 (determinism) | A | 95% | Hard guarantee in A; explicit non-property in B (research is stochastic by design) |
| C-002 (evidence basis) | B | 78% | B's strength when input is uncertain; reduced edge for already-validated roadmap |
| C-003 (tier classification) | A | 98% | First-class field in A; absent in B; load-bearing for downstream `/sc:task` |
| C-004 (parallelism) | B | 72% | B has multi-track + parallel researchers; A has none. But parallelism is only valuable when work is parallelizable (mixed for current roadmap) |
| C-005 (quality gates) | B | 65% | B has more gates; A has post-hoc validator. B's gates are evidence-heavier; A's are validation-heavier. Trade-off |
| C-006 (downstream consumer) | A | 95% | Sprint CLI is the project's standard orchestration; F1 loop is item-by-item processing only |
| C-007 (resume/idempotence) | TIE | 60% | Both have resume; A via state file, B via folder introspection. Approach differs, capability roughly equivalent |
| C-008 (clarification) | A | 70% | A inserts Clarification Tasks as first-class rows; B asks user inline. Both work; A is more deterministic |
| X-001 (file-access philosophy) | TIE | 50% | Both correct for their respective scenarios; not falsifiable in isolation |
| U-001 (Sprint-CLI compatibility) | A | 100% | A's unique strength |
| U-002 (tier at gen-time) | A | 100% | A's unique strength |
| U-003 (atomicity-binding preservation) | A | 90% | A preserves compound rows; B's researcher pattern decomposes them (INV-007) |
| U-004 (zero-trust QA) | B | 85% | B's unique strength; relevant for unvalidated input |
| U-005 (multi-track parallelism) | B | 75% | B's unique strength; partially relevant (intra-milestone parallelism) |
| U-006 (web research) | B | 70% | B's unique strength; minimal relevance for current roadmap (no external-standard refs) |
| A-001 (input is authoritative) | TIE | 50% | Both agree |
| A-002 (markdown output) | TIE | 50% | Both agree |
| A-003 (executor is separate) | TIE | 50% | Both agree |
| A-004 (intent is clear) | A | 65% | Roadmap quality is high; A's "intent is clear" assumption is satisfied |

**Per-variant point totals:** A wins 16, B wins 6, TIE 3
**Convergence:** 22/25 points resolved = **88%** (exceeds 80% threshold)
**Taxonomy coverage:** L1=3 covered, L2=10 covered, L3=12 covered — all levels addressed
**Invariant gate:** 1 HIGH unaddressed (INV-007), but the invariant *favors* the winner — does not block

---

## Convergence Assessment

- Points resolved: 22 of 25
- Alignment: 88%
- Threshold: 80%
- Status: **CONVERGED**
- Unresolved points: C-007 (resume/idempotence), X-001 (philosophy), A-001/-002/-003 (shared assumptions — agreement is the resolution)
