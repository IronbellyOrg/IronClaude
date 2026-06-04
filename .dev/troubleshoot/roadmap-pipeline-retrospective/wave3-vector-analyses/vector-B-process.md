# Vector B — Process / Workflow Critique

**Role:** Process engineer reviewing the master report through a workflow-and-input-quality lens.
**Inputs reviewed:** `master-report.md` (962 lines, Executive Summary → Architectural-flaw Thesis → Bibliography); SKILL.md for sc-brainstorm-protocol, sc-roadmap-protocol, sc-tasklist-protocol, sc-task-protocol, sc-reflect-protocol.

The master report's verdict (REWRITE, master:§Executive Summary) is built almost entirely on *architectural* substrate claims. This vector argues that a meaningful fraction of the failure tape is not substrate but **workflow** — input shape, upstream artifact discipline, validation-lag, and human-in-the-loop ergonomics — and that a non-trivial subset of those workflow failures can be reduced *without* touching pipeline internals. I also identify which failures are people-trapped (no input reshaping helps) and therefore correctly prioritized as architectural targets.

---

### Q1. Non-architectural failures (workflow-caused)

The following items in the master report's Failure Taxonomy and Recurrence Matrix are causally upstream of the pipeline, not within it. Each is a failure the pipeline merely *exposed* — the originating defect is in the input, the discipline of authoring, or the human gate around the run.

1. **Roadmap fabricates / renumbers FR/NFR/SC/D-### identifiers** (master:§Failure Taxonomy "Spec → Roadmap Fidelity Drift"; recurrence row #4; ~14 findings). The master report treats this as "Flaw 2 — generator/validator asymmetry" (master:§Flaw 2). But the structural antecedent is that **specs ship without an enumerated ID registry**: (A1b:F-A1b-004) v2.22 invented FR-001..FR-032 *because the spec did not name any FR-NNN*; (A5:F-A5-009) SC-009b was invented *because the spec's SC ladder was not explicit*. If specs were authored with a closed, machine-readable ID set, the generator's tabular-formatting bias would have nothing to invent against. **Workflow defect**, not generator defect.

2. **Architects re-decompose phases** (master:Recurrence Matrix row #5; (A1b:F-A1b-004), (A7:F-A7-04), (A7:F-A7-05), (A7:F-A7-07)). Architects produce 7-phase roadmaps from 4-phase specs not because the LLM is broken but because the **spec did not declare phase boundaries as a hard constraint**. v2.24's "architecturally superior to spec" deviation (A7:F-A7-05) is the canonical sign: when the input under-specifies, the model legitimately fills the gap, and the gate then halts because the input failed to commit. Input-quality contract gap.

3. **Manual override / hand-classification recurs every release** (master:§Remediation Taxonomy "Manual override"; ~7 attempts, 5 Stuck). (A7:F-A7-05) `dev-001-accepted-deviation.md` (28KB) and (A10:F-A10-008) 7 manually-declared IC contracts both demonstrate that *humans had to author the answer the scanner expected to find*. This is a missing **authoring discipline**: specs should carry pre-approved-deviation manifests at submission time, not be patched post-halt by operators. The remediation log is full of evidence that this is process, not architecture.

4. **Verification tasks silently skipped** (master:§Failure Taxonomy "Process / Discipline Erosion"; ~4 findings; (A3:F-A3-19) v3.2 shipped with all 6 T17-T22 verification tasks SKIPPED; (A4:F-A4-013) v3.05 Wave 3 NOT EXECUTED). Master classifies as "MEDIUM" and treats as part of Flaw 1 (artifact-centric). But the operators *did skip the verification waves under explicit "honor-system"*. A workflow gate that simply blocked release-tagging until verification tasks were completed (no pipeline change needed) would have caught both. **Discipline failure, not substrate failure.**

5. **PRD/TDD source-document collapse (49% fewer tasks on richer inputs)** ((A11:F-A11-005), (A12:F-A12-12), Recurrence row #20). The master report's late correction (A12:F-A12-12) reclassifies this as a **roadmap format artifact** (table-row dense vs delivery-milestone narrative), not extraction destroying granularity. That makes it a **roadmap-authoring style failure**, not a pipeline defect: the same R-items mapped 1:1:1 to tasks in both cases, but the upstream roadmap's prose density chose how many task-stubs the downstream parser would see. Authoring guidance — "roadmaps for tasklist-generation must use the dense tabular form" — would prevent this without changing tasklist code.

6. **Skill / SKILL.md drift from CLI** (master:Recurrence row #11; 17 flag mismatches, A9:F-A9-003, A9:F-A9-004). Master groups under Flaw 5 (no contract schema). But this is fundamentally a **documentation-discipline failure** — flags evolved in CLI without parallel SKILL.md edits, and the convergence release closed *one round* without making the discipline durable. A pre-commit `--help`-vs-SKILL diff would catch this without any architectural change. (A10:F-A10-006, A10:F-A10-007) further show that `make verify-sync` existed but was *not invoked from CI*; mechanical detection without invocation is a workflow gap.

7. **Plugin / convention override without enforcement** ((A10:F-A10-005) skill-creator wrote ~100 eval artifacts to `.claude/skills/` instead of `.dev/`; Recurrence row "Plugin/Convention" in §Failure Taxonomy). Master classifies as governance/MEDIUM and ultimately routes through a 5-layer remediation. The root cause is that **CLAUDE.md was instructional prose only** — there was no PreToolUse hook, no commit gate. Adding hook + `.gitignore` (the eventual fix) was a workflow correction layered on top of instructional discipline failure.

8. **Anti-instinct halts on legitimate vocabulary (Strategy / hardcoded / Scaffold)** ((A11:F-A11-002), (A11:F-A11-003), (A2a:F-A2a-003); Recurrence row #6). The pipeline is patchable here (allowlist), but the **upstream cause is that source specs and TDDs use natural-language section headings like "Testing Strategy"** that collide with the scanner vocabulary. An input contract requiring TDDs to use ID-prefixed section headings (e.g., `## §15 Testing Strategy [non-obligation]`) would shrink the false-positive surface from the source side. *People-flexible* (see Q5).

9. **Convergence threshold drift across sibling skills (0.7/0.5 vs 0.6/0.5)** ((A10:F-A10-003); Recurrence row #7). Skills were authored independently, each with locally-chosen thresholds. Not an architectural problem — a **skill-authoring policy gap**. A single project-level "skill conventions" document with thresholds as a shared constant would prevent this. The master report acknowledges (master:Flaw 5) that there is no SoT layer for thresholds; my reframing: there *could* be one, and creating it is process work, not architecture.

10. **`integration` branch assumption broke on the fork** ((A12:F-A12-08) Step 1.3 assumed upstream branch convention). Pure environment-mismatch from an upstream CLAUDE.md being inherited. **Onboarding/configuration discipline**, not pipeline architecture.

These ten items account for roughly 40-50 distinct findings (cross-referenced across the failure taxonomy and remediation taxonomy). The master report folds them into the five flaws because the framing question is architectural; under a workflow framing, they fall out as input-quality + discipline.

---

### Q2. The input-quality contract — what upstream artifacts owe the pipeline

The pipeline assumes much more about its inputs than the skill protocols formally require. Below is the *implicit* input-quality contract reconstructed from observed failures, with the skill-protocol clauses that partially honor or entirely fail to honor it.

**Implicit contract clauses (what the pipeline NEEDS):**

| Clause | What pipeline needs from inputs | Skill-protocol coverage | Evidence of violation |
|---|---|---|---|
| **C1: Enumerated ID registry** | Spec declares every FR-, NFR-, SC-, D- ID up front as a closed set | sc-roadmap §6 declares an *output* ID schema (`src/superclaude/skills/sc-roadmap-protocol/SKILL.md:383-392`) but specifies nothing about input IDs | (A1b:F-A1b-004), (A12:F-A12-01) — generator invents IDs because none are declared |
| **C2: Phase-boundary commitment** | Spec declares whether phase decomposition is rigid or advisory | NONE. sc-roadmap Wave 2 step 4 (`SKILL.md:256`) computes milestone count via formula with no input check on spec phasing intent | (A1b:F-A1b-004) 4 spec phases → 7 roadmap phases; (A7:F-A7-07) 7→5 consolidation losing `config.py` |
| **C3: Pre-approved-deviation manifest** | Spec ships a machine-readable list of intentional deviations from prior contracts | NONE. sc-roadmap and sc-tasklist treat deviations as *generated* artifacts, not input artifacts | (A7:F-A7-05) operator hand-wrote `dev-001-accepted-deviation.md` 28KB *after* halt; (A10:F-A10-011) PRE_APPROVED templates re-flagged every release |
| **C4: Obligation/scaffold vocabulary discipline** | TDD/PRD use section-heading conventions that don't collide with anti-instinct scanner vocabulary | NONE. sc-brainstorm produces seed-briefs in free prose (SKILL.md:151-165); no vocabulary-discipline reference in tdd-skill | (A11:F-A11-002) "Testing Strategy" headings; (A2a:F-A2a-003) "Scaffold" as verb |
| **C5: Spec hash + change-tracking** | Spec carries a hash so downstream gates know if it changed mid-pipeline | sc-roadmap §7 "Session schema" tracks `spec file hash for mismatch detection` (`SKILL.md:421`) — PARTIAL: only for resume, not for cross-step | (A4:F-A4-005) v3.0 Run 4 silently regenerated roadmap from scratch, losing edits — no input-mutation tracking |
| **C6: Format declaration (TDD vs PRD vs Spec)** | Input declares its document type so the right extraction prompt fires | sc-tasklist §4.1a does format detection HEURISTICALLY (`tasklist-protocol SKILL.md:171-172`: "20+ section headings matching TDD numbering pattern") | (A11:F-A11-005) 49% fewer tasks because format detection didn't engage the right extraction path |
| **C7: Convergence-threshold authority** | All skills cite a single project-level threshold constant | NONE. sc-brainstorm uses 0.65/0.50/0.50 (`SKILL.md:287-289`); sc-roadmap uses 0.6/0.5/0.5 (`sc-roadmap-protocol SKILL.md:144`); sc-reflect uses its own; release-split uses 0.7/0.5 | (A10:F-A10-003) threshold drift; (A9:F-A9-007) v2.20 shipped at 0.72 below documented 0.85 floor |
| **C8: Bidirectional traceability table** | Spec ships a table mapping spec-ID → expected roadmap-ID prefix; merge enforces every roadmap ID resolves back | sc-roadmap Wave 4 dispatches a quality-engineer for traceability check (`SKILL.md:296`) — but the spec is not required to publish the traceability source-of-truth | (A11:F-A11-022), (A3:F-A3-16) — `_cross_refs_resolve` cannot detect fabricated IDs because no input registry exists |
| **C9: Anti-instinct exemption declaration** | Spec/TDD ships explicit `non_obligation_sections: [...]` frontmatter listing prose-only sections | NONE. anti-instinct scanner has no input-side opt-out (sc-roadmap step 8 — `SKILL.md:120`) | (A11:F-A11-001) every TDD/PRD-enriched run halted; (A2b:F-A2b-006) V3/V5 relational variants merge-rejected on cost |

**Contracts the protocols DO honor (positive coverage):**

- sc-brainstorm Wave 0 step 8 (`SKILL.md:108`) — collision suffix discipline (output-side input contract).
- sc-brainstorm Wave 2B step 3 (`SKILL.md:222-227`) — sanitization of interpolated parameters (defends against injection).
- sc-roadmap Wave 0 step 1 (`SKILL.md:165`) — spec emptiness / <5 lines warning.
- sc-tasklist §3 "Non-Leakage Rules" (`SKILL.md:21-28`) — explicit input-as-only-source-of-truth contract.
- sc-reflect §4.0 step 0.4 (`SKILL.md:174-194`) — `input_sha256` tree-snapshot is **the only protocol with proper input-drift detection**. [INFERRED] This is the model the upstream skills should adopt.

**Diagnostic:** Of the 9 substantive input-quality contract clauses C1–C9, **only C5 (partial) and C7 (partial)** receive any protocol-level acknowledgement, and only sc-reflect §4.0 implements a robust input-drift guard. The other seven clauses are *implicit* — the pipeline assumes them, fails when they're violated, and adds a downstream validator instead of asking the input author to honor them.

---

### Q3. Skill protocol enforcement gaps

| Protocol | What it enforces | What it should but doesn't |
|---|---|---|
| **sc-brainstorm** (`SKILL.md`) | (a) Topic-non-empty (Wave 0 step 1); (b) flag validation (Wave 0 steps 2-4); (c) adversarial skill presence (step 5); (d) handoff-skill presence (step 7); (e) param sanitization (Wave 2B step 3); (f) FAIL-fast on empty adversarial response (Wave 3 step 3) | (1) No output-side **enumerated ID emission** for downstream roadmap to use (C1); (2) seed-brief frontmatter has no `non_obligation_sections` declaration (C9); (3) merged-requirements.md has no requirement-ID schema, so downstream roadmap's `_cross_refs_resolve` has nothing to anchor against; (4) `--handoff tasklist` validates "≥3 enumerated requirements" by regex (`SKILL.md:313`) but does not validate they have IDs |
| **sc-roadmap** (`SKILL.md`) | (a) Spec emptiness (Wave 0); (b) `_cross_refs_resolve` (Wave 4 — known-broken stub per A9:F-A9-005); (c) DAG cycle check (Wave 2 step 5); (d) frontmatter exactly-one of `spec_source`/`spec_sources` (Wave 3); (e) acknowledges inference-thresholds vs CLI-gates split (`SKILL.md:140-146`) — DOCUMENTATION only | (1) **No input-ID-set extraction** before generator runs — so the generator can invent IDs and merge cannot catch them (C1, C8); (2) no spec-phase-count check before milestone-count formula fires (C2); (3) no input-side `accepted-deviation` manifest read (C3); (4) `_cross_refs_resolve` shipped as known-stub, no enforced gate before fix; (5) convergence threshold hardcoded per-skill (C7); (6) no input-format declaration check — relies on heuristic 8-step extraction pipeline |
| **sc-tasklist** (`SKILL.md`) | (a) Strong non-leakage rules §3 (`SKILL.md:21-28`); (b) deterministic TASKLIST_ROOT resolution §3; (c) post-generation validation against roadmap (Stage 7-10, `SKILL.md:1172+`); (d) TDD format detection heuristic §4.1a; (e) write-atomicity (`SKILL.md:1125`) | (1) Format detection is *heuristic* not contract — input is not required to declare type (C6); (2) supplementary-context extraction is best-effort, no fail-loud on missing TDD sections; (3) generation enrichment is skill-only, NOT CLI (per `SKILL.md:129` scope-note) — so CLI users get the un-enriched path with no warning; (4) clarification-task escape (§4.6 ref) is per-task, not gated on input-quality at ingest |
| **sc-task** (`SKILL.md`) | (a) Tier classification with confidence (Section 0); (b) STRICT path runs quality-engineer (Section 3); (c) TFEP prohibits ad-hoc test-fix (Section 4.5); (d) Critical Path Override (auth/security/crypto) bypasses tier (Section 4) | (1) **Does not validate inputs against the source roadmap's task contract** — accepts whatever the tasklist generator produced; (2) no check that the upstream tasklist actually conforms to phase-N-tasklist.md convention before running (sprint discovery just fails silently — A6:F-A6-007); (3) no escalation path back to roadmap when sprint discovers task-DAG impossibility (A11:F-A11-024 — "no feedback loop back to roadmap") |
| **sc-reflect** (`SKILL.md`) | (a) Mode selection 6-rule first-match (§3.2); (b) Hard STOP conditions including output path under `.claude/` (§3.3); (c) **input_sha256 tree-snapshot** as drift guard (§4.0 step 0.4) — best-in-class; (d) heterogeneous reviewers + blind calibration (§1); (e) evidence-validator gate — unfounded citations DROPPED not downgraded; (f) Wave 7 SRP boundary for mutation | (1) Operates *after* the work — UC-2 mode is the durable one but cannot prevent the failures it audits; (2) UC-1 mode exists but is **not auto-triggered by sc:roadmap or sc:tasklist** — only by sc:troubleshoot Wave 6 (§2); (3) `--budget-remaining` hint exists but no upstream skill emits it; (4) Wave 7 promotion is the *only* repository-mutation gate in the whole system — but it's `--no-promote` opt-out, meaning the strictest mutator is also the easiest to disable |

The pattern across the table: each protocol enforces its *internal* invariants competently, but **no protocol enforces an input-quality contract on the artifact it consumes**. The fidelity chain is `spec → roadmap → tasklist → task → reflect`, and each link trusts the upstream artifact's shape without re-validating its semantic contract. This is the protocol-layer manifestation of master:Flaw 5 (no contract-schema layer), but framed as a *process gap* it is fixable per-skill without an architectural rewrite.

---

### Q4. Process-level interventions (ranked by expected value)

These interventions do not touch pipeline internals. Each is rankable by `(failures prevented) × (frequency observed) / (intervention cost)`.

**Rank 1 — Input-quality preflight (gate moved upstream).** Add a single `sc:input-validate` skill that runs before `sc:roadmap` and rejects specs missing: (a) frontmatter `requirement_ids: [FR-001, ...]` registry (C1); (b) `phase_boundaries: rigid|advisory` declaration (C2); (c) `non_obligation_sections: [...]` (C9); (d) `accepted_deviations: [...]` manifest (C3). **Expected value: HIGH.** Targets recurrence rows #1 (~12 fixes), #4 (~7), #5 (~5), #6 (~4) — roughly 28 of the top fix-attempt count. Cost: one new ~100-line skill, opt-in flag on sc:roadmap. No pipeline change.

**Rank 2 — Pre-execution UC-1 reflect as default (not opt-in).** `sc-reflect-protocol` UC-1 mode (`SKILL.md:38-39`) explicitly cites "ROI band: 200-500 tokens to potentially save 5,000-50,000" — same economics as confidence-check. Currently it only auto-fires from sc:troubleshoot Wave 6 (`sc-reflect SKILL.md:53-54`). **Move it to fire automatically between sc:roadmap completion and sc:tasklist invocation**, so the tasklist generator never starts on a roadmap that fails coverage. Expected value HIGH: catches Recurrence rows #1, #4, #15 (adversarial findings dropped at merge), #19 (UNCLASSIFIED deviations). Cost: one cron/hook wiring; no protocol change.

**Rank 3 — Contracts-made-explicit policy file.** Author `docs/skill-contracts.md` declaring the single project-wide values for: convergence thresholds, severity gate predicates, ID schemas, frontmatter fields. Have each skill `Read` it at Wave 0. **Expected value: MEDIUM-HIGH.** Targets Recurrence rows #7 (~3 threshold-drift fixes) and #11 (~2 skill-CLI drift) directly; indirectly defends against future drift on every release. Cost: one document + a `Read` per skill startup.

**Rank 4 — Authored-deviation manifest discipline.** Require every spec/PRD that has been generated from a *previous* roadmap to ship `accepted-deviations.yaml` listing intentional contract changes. The roadmap's spec-fidelity gate consumes this manifest as an allowlist before flagging HIGHs. **Expected value: MEDIUM-HIGH.** Targets the entire "Manual override" remediation shape (master:§Remediation Taxonomy, 7 attempts, 5 Stuck) — every one of those was a human authoring the manifest *after* halt. Cost: one schema definition + a documentation policy. The gate already exists (or its absence is the bug); this is purely an upstream authoring habit.

**Rank 5 — Dry-run reviewer step before destructive pipeline phases.** Insert a mandatory pre-merge human-readable `--dry-run` preview before any step that consumes >50K tokens (debate, generate-architect). User sees the *plan* before the spend. **Expected value: MEDIUM.** sc-roadmap and sc-brainstorm both have `--dry-run` modes (sc-roadmap `SKILL.md:83`, sc-brainstorm `SKILL.md:246`), but they're opt-in. Making them the default for budget-intensive steps catches Recurrence row #17 (context-window/OOM) — at least operators see what's coming. Cost: flag-flip + 1 confirmation prompt.

**Rank 6 — Escape hatch: `--allow-anti-instinct-warnings`.** Add a single bypass flag on the anti-instinct hard-zero AND-composition that lets operators ship with warnings instead of halt. Master report explicitly calls out the lack of this (master:§Pipeline-step Heat Map "anti-instinct" — "no `--allow-anti-instinct-warnings` escape valve means any one false positive halts the entire downstream pipeline"). **Expected value: MEDIUM, but with the caveat** that this is a workaround, not a fix — it trades one form of brittleness (false-positive halt) for another (silent-skip institutionalization, master:Flaw 4). Use *only* in conjunction with Rank 1 input-validate.

**Rank 7 — CI invocation of `make verify-sync` + `--help`-vs-SKILL diff.** Master report (A10:F-A10-006, A10:F-A10-007) shows verify-sync existed but no CI ran it; A9:F-A9-003 shows 17 flag mismatches. Adding a CI workflow that fails on either is pure process — no code, no pipeline. **Expected value: MEDIUM** (closes one recurrent class permanently). Cost: ~50 lines of GitHub Actions YAML.

**Rank 8 — Onboarding/configuration sanity check.** A pre-pipeline `superclaude doctor --pipeline` that fails loud on missing branches (master:F-A12-08 `integration` branch), missing env vars (sc-reflect §3.4 alias resolution), or upstream-vs-fork mismatch. **Expected value: LOW-MEDIUM.** Cost: extend existing `superclaude doctor`.

**Cumulative coverage:** Rank 1+2+3+4 alone target ~50 of the ~159 failure findings (cited rows above plus their cross-references). They are all **process work**, not pipeline rewrite.

---

### Q5. People-flexible vs people-trapped

The crucial distinction for Vector B's verdict: not every failure can be avoided by rephrasing the input. The people-trapped failures are the ones that justify the master report's REWRITE verdict.

**People-flexible (operator can rephrase to avoid):**

- **Anti-instinct vocabulary collisions** ((A11:F-A11-002), (A2a:F-A2a-003)). An operator who knows the scanner's vocabulary can author TDDs that say "Test Approach" instead of "Testing Strategy", `config_factor=12` instead of `bcryptjs cost factor (12)`. People-flexible.
- **Phase-restructure deviation** (Recurrence #5). Operator can write specs that explicitly say "phases are rigid, do not consolidate" in frontmatter or prose. People-flexible — sc-roadmap doesn't currently enforce it but a disciplined author can pin it.
- **Convergence threshold drift across skills** (#7). An operator who knows each skill's threshold can pre-tune their invocation flags. People-flexible (clunky, but possible).
- **Format detection collapse on TDD+PRD** ((A11:F-A11-005), (A12:F-A12-12)). After the (A12:F-A12-12) reframing, this is *roadmap format* — operators can author the roadmap in the dense-tabular style. People-flexible.
- **Plugin convention overrides** ((A10:F-A10-005)). Operators can simply not run skill-creator without `--output .dev/eval-workspaces/...`. People-flexible (now backed by hook, but originally flexible).
- **`integration` branch assumption** ((A12:F-A12-08)). Operator creates the branch manually. People-flexible.

**People-trapped (no realistic input shape avoids the failure — PRIORITY-1 architectural targets):**

- **Spec-fidelity LLM-only / non-deterministic** (Recurrence row #1, ~12 fix attempts). The (A4:F-A4-005) evidence — 5 runs / 4 distinct deviation counts on *identical* input — proves that *no input rephrasing* changes the outcome. The gate itself is the source of non-determinism. People-trapped. **PRIORITY-1.**
- **Written but not wired** (Recurrence row #2, ~8 attempts). No input the operator can author exercises a dead production path. (A11:F-A11-011) `build_certify_step` cannot be invoked by any spec that an operator writes. People-trapped. **PRIORITY-1.**
- **Wiring-verification scans wrong directory** ((A2b:F-A2b-002), Recurrence row #3). Operator has no input lever over the gate's target-directory bug. People-trapped. **PRIORITY-1.**
- **Retry without input mutation** (Recurrence row #9, (A1b:F-A1b-006), (A12:F-A12-02)). The retry loop re-runs the same prompt against unchanged inputs by construction; nothing an operator can author causes the second attempt to differ from the first. People-trapped. **PRIORITY-1.**
- **Generator/validator asymmetry** (Recurrence row #10). Defines the substrate; no input can balance it. People-trapped. **PRIORITY-1.**
- **Validation declared CLEAN with implementation incomplete** (Recurrence row #12, (A2b:F-A2b-004)). 8 sub-agents marked CLEAN while 3 CRITICAL bugs shipped — *no input the operator authored* would have flipped that verdict, because the gate validates the *report frontmatter*, not the behavior. People-trapped. **PRIORITY-1.**
- **Two frontmatter parsers disagree** ((A11:F-A11-010)). The disagreement is internal to the pipeline; the operator cannot author a file that satisfies both. People-trapped.
- **Adversarial findings dropped silently at merge ~10-15%** (Recurrence row #15). No input shape affects merge's silent-drop rate. People-trapped.
- **`_cross_refs_resolve` always-True stub** (Recurrence row #8). The stub returns True regardless of input. People-trapped.

**Verdict on the people-trapped set:** Six of the top-ten Recurrence Matrix rows (#1, #2, #3, #9, #10, #12) are *fully people-trapped* — no input-quality intervention helps. These six are the correct target population for the master report's REWRITE verdict. They cluster around Flaws 1, 2, and 3 in master:§Architectural-flaw Thesis and they share a common signature: **gate logic that operates on LLM-generated text where the operator has no lever over the gate's verdict**.

**Vector B's structural disagreement with master:**

The master report's verdict bundles ALL recurring failures into the REWRITE rationale. Vector B's reframing: **the ~40-50 findings in the workflow/discipline bucket (Q1) can be retired via Q4's process interventions (Ranks 1-4) for a fraction of a rewrite's cost**, leaving the rewrite scope to focus on the ~6 truly people-trapped failure classes. This is a smaller, cheaper, and lower-risk target than the all-in REWRITE the master report concludes with. The two views are compatible — process work neutralizes the people-flexible half of the failure surface; the rewrite (or targeted refactor) addresses the people-trapped half — but they are not the same work and should not be conflated. The master report's section "Cost of leaving unaddressed" under each Flaw (master:§Flaws 1-5) does not currently distinguish these two cost basins, and that conflation is the most actionable critique Vector B offers.

---

**Citation notes.** `(master:§X)` refers to sections of `master-report.md`. `(A<N>:F-A<N>-<seq>)` are partition findings carried verbatim from the master report. File-and-line citations to skill protocols: `<protocol> SKILL.md:<line>`. INFERRED tag is used in §Q2 for the claim that sc-reflect §4.0's input_sha256 model is the template upstream skills should adopt — that claim synthesizes across the protocol comparisons and is not a direct citation.
