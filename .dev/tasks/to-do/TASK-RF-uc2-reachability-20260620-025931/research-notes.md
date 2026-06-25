# Research Notes: FR-RSR — sc:reflect UC-2 Runtime-Surface Reachability Escalation

**Date:** 2026-06-20
**Scenario:** A (Explicit — BUILD_REQUEST hands a complete T1–T10 decomposition; TDD is the research document of record)
**Depth Tier:** Deep (HIGH complexity 0.85; 10 FRs; multi-file SKILL.md + refs/ + eval suite)
**Track Count:** 1 (single cohesive feature; sequential dependencies; not splittable)
**Template:** 02 (complex — discovery/build/test/QA phases, conditional blocker ordering)
**Spec path (PRE reflect gate `--spec`):** `.dev/reflect-hardening/issue-1-uc2-reachability/tdd.md` (the authoritative GUIDING DOCUMENT per BUILD_REQUEST)

---

## AUTHORITATIVE SOURCES (read by builder)

- **TDD (design of record — drives task set, structure, sequence, DoD):**
  `.dev/reflect-hardening/issue-1-uc2-reachability/tdd.md` (1080 lines).
  Key sections: §6.4 D1–D12 (design decisions), §7.1 (data models), §18.2 (file inventory),
  §19.3 / §23.2 P1–P6 (rollout order + blocker ordering), §24.1/§24.2 (DoD + Release Checklist),
  §20 (risk register), §12 (error handling / edge cases).
- **Spec (secondary — mine ONLY for the six BUILD_REQUEST-named things; NEVER expand scope):**
  `.dev/reflect-hardening/issue-1-uc2-reachability/spec.md` (795 lines).
  Six mining targets: (1) per-FR acceptance criteria `- [ ]` boxes §3; (2) worked Gherkin §2.3;
  (3) NFR measurement methods §6 table; (4) degrade-oracle + lang-table content FR-RSR.3 + §1.1 +
  OQ-RSR.1/2; (5) risk→mitigation §7; (6) blocker ordering §10 "For sc:tasklist".
- **When TDD and spec disagree, the TDD wins** (they were reconciled in a prior reflect pass).

When TDD/spec disagree on counts: TDD §7.1 spec-override annotations already resolved two — both
`runtime_surface_unreached`/`runtime_surface_degraded` count **symbols** (reduced per-symbol verdict,
NOT edges), and `requirement_id` is `str | None` everywhere (symbol-anchored). The spec was updated to
match; treat TDD §7.1 as canonical for the data model.

---

## EXISTING_FILES (scope-verified 2026-06-20)

**Modify targets (source of truth = `src/superclaude/` ONLY; never edit `.claude/` mirrors):**

- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` — **1854 lines** (TDD said ~1850 ✓). The single
  primary target; six surgical edits. TDD-cited anchors (line numbers approximate — researchers MUST
  re-capture exact current anchors): §5.3 decision table (~386–402, first-match-wins; forbid-STOP
  pre-filter precedence ¶ at ~402, `coverage_degraded` shape); §5.4 `tier_decision.yaml`; §6.1 Wave-1A
  grounding chain steps 1..7' (~457–478, step 4 `find_referencing_symbols` at ~463 — the referrer set
  fetched-and-discarded); §6.1.1 verification triangle (untouched); §6.5 fail-open (~563–565); §0.5d
  availability surface; §9.1 stable contract block (~689–708, `contract_version` currently 1.5.0); §9.3
  Consumer Field Map (field-deletion guard ~868); §9.4 versioning rules (~877); §10.3 Drift (~937), §10.4
  Regression (~952), §10.5 precedence (~982), §10.6 Grounding Gap (~1002–1006), §10.8 Reuse-Miss modifier
  (~1014, the pattern §10.9 mirrors); §17.7 Kill List item 6 (~1799, rejected a 5th class); the "Will Not
  run /task" invariant (~1700); sprint-consumer TurnLedger row (~858, reads `deviation_count_by_class.regression`).
- `src/superclaude/skills/sc-reflect-protocol/refs/` — present. Existing files: `cost-profile.yaml`,
  `coverage-mapping.md`, `deviation-taxonomy.md`, `grader-extensions.md`, `input-resolution.md`,
  `ops-integration.md`, `promotion-adapters.md`, `reflection-rubric.md`, `remediation-handoff.md`,
  `report-template.md`, `reviewer-spec.md`. **`runtime-surface.md` does NOT yet exist** (T1 creates it).
  - `reviewer-spec.md` — "exactly three sections" invariant; `## Grounding hunks` H2; FR-4 verify-log
    routing pattern (TDD cites reviewer-spec.md:31 grounding-hunks, :43 verify-log pattern). FR-RSR.9 adds
    a qa-persona ledger entry UNDER the existing H2 — NOT a 4th section.
  - `deviation-taxonomy.md` — contradiction-anchored 4-class taxonomy; FR-RSR.6 adds a §10.9 xref.
  - `grader-extensions.md` — defines the assertion types (`regex_absent`, `yaml_field`,
    `falsifier_skeleton_present`, etc.).
- `.dev/eval-workspaces/sc-reflect/grader.py` — **492 lines**. Assertion anchors verified: `regex_present`
  (def 152), `regex_absent` (def 162, dispatch 391), `yaml_field` (dispatch 336), `yaml_field_min`
  (dispatch 348), `falsifier_skeleton_present` (def 270, dispatch 405). Extend `regex_absent`/`yaml_field`
  ONLY if needed (TDD §18.2).
- `.dev/eval-workspaces/sc-reflect/evals/evals.json` — the eval registry (currently the ONLY file under
  `evals/`; per-case dirs for the 5 new companions are net-new and must be registered here).
- `.dev/eval-workspaces/sc-reflect/skill-snapshot/reflect-v1.md` — the **pre-change skill snapshot** the
  headline eval runs against to prove FAIL-pre / PASS-post.
- `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/` — `T2-converges-on-wrong.yaml`,
  `T2-judge-class-collision.yaml` (the two skeletons that MUST stay green + unmodified), `fixtures/`, `README.md`
  (dual-state skeleton/active lifecycle).

**New files (T1 + T9):**

- `src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md` — source of truth for tagger
  allowlist + lang→(test-marker, comment-syntax) table + degrade-oracle table + rootwalk algorithm + ledger schema.
- `.dev/eval-workspaces/sc-reflect/evals/uc2-unwired-surface-passes/` (+ fixtures) — headline active eval.
- `.dev/eval-workspaces/sc-reflect/evals/uc2-surface-positive-control/` (+ fixtures).
- `.dev/eval-workspaces/sc-reflect/evals/uc2-surface-dynamic-dispatch/` (+ fixtures).
- `.dev/eval-workspaces/sc-reflect/evals/uc2-surface-degraded-backend/` (+ fixtures).
- `.dev/eval-workspaces/sc-reflect/evals/uc2-surface-test-only-ref/` (+ fixtures).
- `<output>/artifacts/runtime-surface-ledger.yaml` — RUNTIME artifact, per-run, NEVER committed.

**In-repo evidence the degrade oracle MUST NOT false-flag:**

- `pyproject.toml:67–69` — `[project.scripts]` `superclaude = "superclaude.cli.main:main"`,
  `ic = "superclaude.cli.ic:main"` (verified). Pure registry entrypoints, zero static callers → must DEGRADE.

**MDTM template location (CORRECTION):** the builder default points at `.claude/templates/workflow/02_...`,
but `.claude/templates/` is EMPTY in this worktree. The live template is
`src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` — the builder MUST read from `src/`.

## PATTERNS_AND_CONVENTIONS

- **Source-of-truth discipline:** edit ONLY `src/superclaude/`; after every SKILL.md/refs edit run
  `make sync-dev` then `make verify-sync` (must exit 0). Never stage `.claude/` mirrors.
- **UV only** for any Python (grader). Before pushing Python: `uv run ruff format --check src/ tests/`
  (green `make lint` ≠ green CI format).
- **Additive minor:** `contract_version` 1.5.0 → 1.6.0; no existing field renamed/removed/retyped/
  re-semanticized; UC-1 and non-surface UC-2 runs keep emitting inert defaults (byte-stable).
- **Two load-bearing invariants (TDD §1, never relax):** (1) tagger is **symbol-anchored, NOT
  requirement-anchored** (keys off Wave-1A resolved symbol kind; `requirement_id` is an optional nullable
  attribute); (2) degrade oracle **defaults all dynamic/registry/decorator/reflection/`[project.scripts]`
  wiring + partial-rootwalk + unknown-lang to DEGRADE → §10.6 Grounding Gap, NEVER blocking Regression**.
- **Counter hygiene (D8):** increment ONLY `deviation_count_by_class.regression`; NEVER
  `verification_regressions_detected` (exit-code-sourced).
- **Eval discipline:** headline `status: active` with REAL fixtures (skeletons pass vacuously); MAIN
  companions under `evals/` use `regex_absent` / `yaml_field`; existing falsifier skeletons stay green.

## GAPS_AND_QUESTIONS (researchers verify / capture)

- Exact CURRENT line anchors for every SKILL.md section above (TDD numbers are approximate vs the 1854-line
  file). Researchers MUST re-capture so the builder's per-item Context carries accurate `file:line` (TB-Add-8).
- `reviewer-spec.md` exact three-section names + the `## Grounding hunks` line + FR-4 verify-log pattern line.
- `deviation-taxonomy.md` structure + the right insertion point for the §10.9 xref.
- `evals.json` registration schema (how a new case dir is declared) + an existing MAIN case
  (`cases/post-small-diff-clean/`) as a structural template for the 5 new `evals/` companions.
- grader.py exact call signatures/arg keys for `regex_absent` and `yaml_field`.
- Whether any oracle/lang-table row content beyond py/rust/ts/js/go is needed (OQ-RSR.2: others DEGRADE).

## RECOMMENDED_OUTPUTS (researcher → output file)

- `research/01-skill-gather-gate-anchors.md` — SKILL.md §5.3/§5.4/§6.1 anchors + content (gather + gate sites).
- `research/02-skill-contract-classify-failopen-anchors.md` — SKILL.md §9.1/§9.3/§9.4/§10/§17.7/§6.5/§0.5d anchors.
- `research/03-refs-inventory.md` — reviewer-spec.md, deviation-taxonomy.md, coverage-mapping.md, grader-extensions.md.
- `research/04-eval-grader-inventory.md` — evals.json schema, existing MAIN case template, grader.py signatures, skill-snapshot, falsifier-suite README.
- `research/05-template-and-examples.md` — MDTM template 02 PART 1 rules + an existing TASK-RF complex example.

## SUGGESTED_PHASES (researcher assignments)

- **R1 (File Inventory / Patterns):** SKILL.md gather+gate sites — §5.3 decision table + forbid-STOP
  pre-filter precedence ¶, §5.4 tier_decision.yaml, §6.1 Wave-1A steps 1..7' (esp. step 4
  find_referencing_symbols), §6.1.1 (note untouched), §6.5 fail-open. → `01-...`. No overlap with R2.
- **R2 (File Inventory / Patterns):** SKILL.md contract+classify+fail-open sites — §9.1 stable contract
  block (+ contract_version), §9.3 consumer map (field-deletion guard), §9.4 versioning, §10.3/10.4/10.5/
  10.6/10.8 (+ §10.9 insertion point), §17.7 Kill List item 6, §0.5d, sprint-consumer TurnLedger row. → `02-...`.
- **R3 (Integration Points / Doc Cross-Validator):** refs/ — reviewer-spec.md three-section invariant +
  grounding-hunks + FR-4 pattern, deviation-taxonomy.md structure + xref point, coverage-mapping.md (fact 3),
  grader-extensions.md assertion defs. → `03-...`.
- **R4 (Test & Verification):** eval workspace — evals.json registration schema, `cases/post-small-diff-clean/`
  as a MAIN-case structural template, grader.py `regex_absent`/`yaml_field` signatures, skill-snapshot/
  reflect-v1.md, falsifier-suite README dual-state lifecycle. → `04-...`.
- **R5 (Template & Examples):** `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` PART 1
  (rules A3 granular, B2 self-contained, L1–L6 handoff) + one existing complex TASK-RF example. → `05-...`.

## TEMPLATE_NOTES

- Template **02** (complex) — confirmed by BUILD_REQUEST. Discovery/build/test/QA phases + conditional
  blocker ordering (T4 blocks T2's UNREACHED path; T1 blocks all).
- Tier **Deep** — HIGH complexity, 10 FRs, multi-file, blocker ordering.
- QA_GATE_REQUIREMENTS: **PER_PHASE** (Template 02). Use adversarial-stance rf-qa with `fix_authorization`
  for the MDTM gates (BUILD_REQUEST PER-TASK DoD).
- POST_REFLECT_GATE: **ENABLED** (this is an executed code change to a skill + evals).
- Granularity: one FR → one task (T1–T10), each its own phase or item-cluster with embedded acceptance
  criteria. NOT batch items.

## AMBIGUITIES_FOR_USER

None blocking — intent is fully specified by the BUILD_REQUEST + authoritative TDD. The five OQ-RSR.1–5
have stated resolution targets (enumerate allowlist/lang-table/oracle rows in `runtime-surface.md`, pick
rootwalk depth=1 mirroring §4.0; OQ-RSR.5 already ACCEPTED per TDD D12). Per BUILD_REQUEST "HUMAN-DECISION
HANDLING": resolve each OQ per its target during implementation; only a genuine NEW scope/product ambiguity
not covered by a resolution target gets a `PENDING` halt item — never auto-default a scope-shaping choice.
