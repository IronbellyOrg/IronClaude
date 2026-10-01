# Research Completeness Verification — Partition P2 (Integration + Meta Cluster)

**Track:** FR-DRS deterministic runtime-surface sweep
**Lens:** Completeness (BREADTH) — eval-harness wiring, SKILL prose demotion, pytest test patterns, MDTM template
**Date:** 2026-06-22
**Partition:** P2 of research set
**Assigned files:** 05-eval-path-grader-cases-materializer.md, 06-skill-prose-demotion-and-refs.md, 07-test-patterns-and-verification.md, 08-mdtm-template-and-examples.md

[PARTITION NOTE: Cross-file checks (contradictions, coverage audit vs full scope) limited to assigned P2 subset. Full cross-file analysis requires merging all partition reports.]

---

## Files in scope

| File | Read | Status field | Substantial | Has Summary | Has Gaps section |
|------|------|-------------|-------------|-------------|------------------|
| 05-eval-path-grader-cases-materializer.md | YES | Complete | YES (~181 lines, dense) | YES | Partial — gaps folded into §4 verdict, no dedicated "Gaps and Questions" header |
| 06-skill-prose-demotion-and-refs.md | YES | Complete | YES (~166 lines) | YES | Partial — caveats inline (e.g. §3.2 ensemble stamp, §4 caveat); no dedicated header |
| 07-test-patterns-and-verification.md | YES | Complete | YES (~373 lines) | YES | YES — explicit `## Gaps and Questions` + `## Stale Documentation Found` |
| 08-mdtm-template-and-examples.md | YES | Complete | YES (~217 lines) | YES | Partial — builder-decision points inline (§4e fidelity gate); no dedicated header |

**Independent spot-verification (this turn, Bash):** grader.py exists (22KB); materializer `.write_text(eval_metadata)` absence INDEPENDENTLY CONFIRMED (zero hits in sc-reflect workspace `.py`); all 5 `cases/uc2-*` dirs exist; `tests/cli/reflect/conftest.py` exists; `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` exists; UC2 exemplar exists. The four files' core existence claims are sound.

---

## Criterion-by-Criterion Findings

### C1 — Eval path coverage (file 05): grader dispatch, check_yaml_list_len_eq, C-6, 5 cases, C-5 materializer disposition

**PASS.**

- **Grader dispatch:** documented at `grader.py:318-434`, 19 assertion types (8 baseline inline + 11 extension delegated), with the flat `if a_type ==` ladder and the unknown-type fallthrough (`:434`). §1.1. Evidence-cited.
- **check_yaml_list_len_eq:** full signature + body walk at `grader.py:191-210`, tied to AC-3 count-invariant re-check and explicitly mapped to case 41 (`list_field: unreached_surfaces`, `count_field: runtime_surface_unreached`, both from same `contract.yaml`). §1.2. Strong.
- **C-6 target-key constraint:** the load-bearing finding is front-and-center (TL;DR #2 + dedicated §2): bucketing at `grader.py:448-449` keys solely on `target.startswith("with_skill/"|"old_skill/")`; any new FR-DRS oracle assertion without a prefixed `target` is "silently never graded." The non-`target`-key assertion-type trap (citation_resolves, checkpoint_logged, matrix_covers_items, deviation_class_matches) is enumerated. The compliant design (reuse `yaml_field*`/`yaml_list_len_eq` against a written `contract.yaml`, no new type) is given. Excellent — this is a builder-actionable hard constraint.
- **5 cases:** ids 37–41 fully tabulated (§3) with name, key assertions (with evals.json line cites), expected.yaml shape, and per-case verdict. Maps exactly to the assignment's expected verdicts (37 unreached≥1/regression1; 38 unreached0/degraded false; 39 degraded true/regression0; 40 degraded true/status partial; 41 unreached≥1 + count-invariant host). Verified case dirs all exist.
- **C-5 materializer disposition (the top-priority deliverable):** §4 is thorough. VERDICT "CONFIRMED NOT LOCATED in tracked repo code" with 5 evidence points: (1) only 2 read-only `.py` touch eval_metadata.json, (2) `make reflect-eval` runs grader on an empty fresh dir, (3) eval_metadata.json files exist as flattened projections but were LLM-harness-produced, (4) skill-creator run_loop.py is a trigger-loop not a materializer, (5) SPEC.md confirms hybrid harness. The "located vs must-build" disposition is resolved decisively → **must-build**, with two landing options (Option B recommended) and the concrete Phase-3 task-item implication. I INDEPENDENTLY re-confirmed the `.write_text(eval_metadata)` absence this turn.

This criterion exceeds the depth bar.

### C2 — SKILL demotion coverage (file 06): §6.1 4b/4b′ text + line numbers, PRESERVE list, conditional fallback signal, §9.1, sync model

**PASS.**

- **Exact §6.1 4b/4b′ text + line numbers:** the one-line step entries (SKILL.md:465 for 4b′, :466 for 4b) AND the full prose paragraphs (:487 tagger, :489 sweep, :491 contract-emission) are quoted verbatim with line numbers. A re-anchor headline confirms every TDD-cited line number is current. §1.1–1.2.
- **PRESERVE safety list:** §2 gives a P1–P8 table of verbatim safety sentences with current line numbers (P1 = the FR-S9-04 "never emits a clean PASS for a tagged surface whose reachability could not be evaluated" at :489; oracle/rootwalk-before-UNREACHED P2; NEVER-STOP P3; DEGRADE>UNREACHED>REACHED P4; dynamic→DEGRADE P5; UC-2-only P6; tagger-failure→DEGRADE P7; count-invariant P8), PLUS P9–P11 §5.3 pre-filter clauses (390/391/402/412) flagged as do-not-touch. This is exactly the "PRESERVE safety list" the lens asked for, with explicit "the demotion changes who computes, never what a verdict means."
- **Conditional fallback signal (runtime_surface_sweep_ran):** §1.3 gives the precise I6 contract — the demotion is keyed on PRESENCE/ABSENCE of `runtime_surface_sweep_ran` in return-contract.yaml: key present (true OR false) → narrate-only; key fully ABSENT (bare `claude -p`) → legacy LLM-emission fallback. The exact injectable producer sentence is supplied. Tied to TDD:1193/1390/1391. This is builder-ready Phase-4 wording.
- **§9.1:** §3 covers the contract block — version stays 1.6.0 (no bump, OQ-DRS.3 resolved), the six canonical field names + line numbers (731–736), the FR-RSR.7 retarget (not deletion), and the §9.3 consumer map at :890. Also flags the ensemble.py:59 `"1.0"` stale stamp as a CODE change to keep OUT of the Phase-4 SKILL item.
- **Sync model:** §5 gives the edit-src/-only → `make sync-dev` → `make verify-sync` chain with the CLAUDE.md staging-discipline guardrail and confirms `.claude/` currently in sync.

Strong, surgical, and correctly scoped. Exceeds the bar.

### C3 — Test patterns coverage (file 07): conftest/fixtures conventions, 3 new files + derivation test, verification commands

**PASS.**

- **Existing conventions:** §1 fully maps `tests/cli/reflect/` (15 files listed), the conftest fixtures table (FIXTURES_DIR, cli_runner, temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub, make_claude_process_sequence — with line ranges), import style, and the assertion idioms (enum-identity `is Verdict.X` + exact exit_code, reason-slug, call-count arithmetic, "falsifier + control", and the load-bearing **no `@pytest.mark.parametrize` anywhere** house rule). The two construction patterns (pure dict→function→assert vs runner-driven 4-fixture quartet) are spelled out with line cites.
- **Structure for the 3 new files + derivation test:** §2 gives each its own subsection: 2.1 `test_runtime_surface.py` (6 units + count-invariant N∈{0,1,2} + fast-path), 2.2 `test_runtime_surface_eval_determinism.py` (≥3-run AC-2 byte-identical), 2.3 `test_runtime_surface_safety_regression.py` (cases 37/39/40/41 verdict-layer AC-5 gate, with id 38 deliberately excluded), 2.4 §15.4a derivation test (the 4-row truth table 0→null / 1→"runtime_surface_unreached" / 2→"…" / degrade-only→null). Each names module-under-test units, asserts, and per-case expected outcomes.
- **Verification commands:** §3 table is complete — per-file pytest commands, the whole-dir regression run, the grader inner step, AND the MANDATORY-but-separate `uv run ruff format --check` callout (with the `make lint` ≠ ruff-format split verified at Makefile:48-50, and the surgical-scope warning re: the worktree-venv ruff version mismatch). `make verify-sync` applicability is correctly scoped to the SKILL edits only.

This is the most thorough of the four. Exceeds the bar.

### C4 — MDTM template coverage (file 08): required sections, B2 format, A3 granularity, QA-gate encoding, POST reflect gate item shape, a real example mined

**PASS.**

- **Required sections:** §1 gives the full frontmatter key table (base + reflect extensions `start_commit`, `executor_model_class`, `reflect_pre`, `reflect_post: ""` with the do-not-author room comment) AND the ordered body-section skeleton (Task Overview → Key Objectives → Prerequisites → Execution Context → Detailed Task Instructions → Phases → Post-Completion → Task Log), with the D3 "no checklist items before Phase 1" rule.
- **B2 format:** §2 gives the 6-field self-contained-paragraph spec, the FORBIDDEN list (B5), the canonical B4 example verbatim, and an FR-DRS adaptation.
- **A3 granularity:** §3 maps A3/A4/I2 onto the 4-phase rollout with a WRONG-vs-RIGHT table per phase (module / product wire / eval wire / SKILL demotion) and the per-phase verify+sync idiom. Sufficient for per-unit/per-case/per-site item decomposition.
- **QA-gate encoding:** §4 is detailed — qa_intensity=full (I22), M3 lens gate (≥6 agents = 3 rf-qa + 3 rf-qa-qualitative) with the agent-floor table, the I20 serialized-fix sequence (PG.1→PG.5c), the standard + domain lenses, max-cycle table, and the M4/I21 source-fidelity applicability decision (recommends including a light spec→code fidelity gate).
- **POST reflect gate item shape:** §5 gives the EXACT verbatim flat-wrapper item (skip guard `;` wrapper, `--depth deep --fix --promote`, NO base/range/staging, consume exit code, exit 0 only, HALT on 10/11/2), the Update-to-Done terminal item, and placement/anti-orphaning ordering — substituting the FR-DRS absolute task-file path. This is the highest-fidelity deliverable and is builder-ready.
- **Real example mined:** §6 mines 10 concrete patterns from the UC2 exemplar (`TASK-RF-uc2-reachability-20260620-025931.md`, confirmed to exist) with line cites — phase-id-tagged objectives, BLOCKS ordering, per-edit-site precision with do-not-edit carve-outs, per-phase verify+sync, eval-phase shape, full M3 gate, the wrapper/Done pair, and the blocker_reason audit trail that names the FR-DRS spec_path.

Exceeds the bar.

### C5 — Granularity sufficient for per-case / per-test / per-phase checklist items?

**PASS.** Cross-cluster, the four files give a builder enough to write granular items:
- **Per eval-case:** file 05 §3 tabulates each of ids 37–41 with assertions, expected.yaml, verdict; file 07 §2.2/2.3 gives per-case expected outcomes; file 08 §3 P3 row prescribes "one item PER eval case + register + run + assess."
- **Per test:** file 07 enumerates each new test file's per-unit functions, the N∈{0,1,2} count-invariant cases, the 4-row derivation truth table, and the exact pytest commands.
- **Per phase / per edit-site:** file 06 pins the exact SKILL.md lines to edit (465/466/487/489/491) and the lines NOT to touch (390/391/402/412, 672); file 08 §3 gives the per-phase verify+sync idiom and the A3/A4 WRONG-vs-RIGHT decomposition.

### C6 — Doc-sourced claims tagged [CODE-VERIFIED] / [SPEC] / [UNVERIFIED]?

**PASS.** All four files use an explicit tag legend and apply it:
- 05: `[CODE-VERIFIED]` / `[UNVERIFIED]` (+ "[CODE-VERIFIED — absence confirmed]" for the materializer); a citation ledger table (§7) re-verified this turn.
- 06: `[CODE-VERIFIED]` throughout, with a re-anchor headline confirming TDD-cited line numbers are current.
- 07: `[CODE-VERIFIED]` (actual file:line read) vs `[SPEC]` (TDD-derived, test files don't exist yet) — a clean, honest distinction since the test files are greenfield.
- 08: `[CODE-VERIFIED]` by direct Read, with per-claim line cites.

No untagged doc-sourced architectural claims found. No `[CODE-CONTRADICTED]` claims present. The materializer-absence claim is appropriately the strongest-evidenced negative finding.

### C7 — Unresolved ambiguities documented (e.g. the materializer-must-be-built finding)?

**PASS, with one structural note.** The headline ambiguity — the C-5 materializer — is documented in BOTH the files that depend on it: file 05 §4 owns it (NOT LOCATED → must-build, with options and Phase-3 implication) and file 07 §2.2 + Gaps correctly flags it as an UNVERIFIED precondition the determinism test depends on, explicitly handing ownership to R5. This cross-file consistency (R7 defers to R5, no contradiction) is a positive completeness signal. Other documented ambiguities: §15.4a derivation-test home not pinned by TDD (07 recommends default + flags R3 coordination); no `runtime_surface_*`-bearing fixture exists yet (07); coverage-measurement command not TDD-pinned (07); the ensemble.py:59 stale `"1.0"` stamp (06 §3.2, 07 Stale-Doc) routed to the product-wire phase, not Phase-4.

**Structural note (Minor):** Only file 07 uses a dedicated `## Gaps and Questions` header. Files 05, 06, 08 fold their gaps/caveats/builder-decision-points inline into the relevant sections rather than into a single named section. The content is present and findable, but a strict completeness checklist would FLAG the missing dedicated header. This is a Minor finding (does not block synthesis/build) — see gap list.

---

## Contradictions Found (within P2 subset)

None. The one cross-file dependency (materializer) is handled consistently: file 05 owns and resolves it as must-build; file 07 flags it as a precondition and defers to R5. The ensemble.py:59 stale-stamp observation appears in both 06 and 07 with the same disposition (CODE change, out of Phase-4 SKILL scope). No conflicting descriptions of the same component.

[PARTITION NOTE: contradiction detection limited to the P2 subset (05–08). A contradiction between a P2 file and a P1 file (01–04) would only surface when partition reports are merged.]

---

## Compiled Gaps

### Critical Gaps (block synthesis/build)
- None.

### Important Gaps (affect quality)
- None within P2. (The materializer "must-build" is not a research gap — it is a *resolved finding* that the research correctly surfaces as a build deliverable. It is flagged here only so the orchestrator/builder ensures a Phase-1/Phase-3 "build the materializer" item lands; the research did its job.)

### Minor Gaps (must still be fixed)
- **M-1 (files 05, 06, 08):** No dedicated `## Gaps and Questions` section header. Gaps/caveats are present but folded inline. For consistency with file 07 and the standard research-file shape, each could surface a short explicit gaps section. Does not block downstream work — all gap content is present and traceable.
- **M-2 (file 07):** Coverage-measurement command is noted as not-TDD-pinned; the file recommends `--cov=superclaude.cli.reflect.runtime_surface --cov-report=term-missing`. This is a recommendation, not a verified command — acceptable, but the builder should confirm the `--cov` target import path resolves once the module exists.

---

## Depth Assessment

**Expected depth:** Deep tier (per track — Phase-3/Phase-4/test granular checklist items).
**Actual depth achieved:** Deep, and consistently so across all four files. Every file traces to exact file:line or exact TDD section, supplies builder-ready item wording (verbatim SKILL injection sentence in 06; verbatim POST-reflect-wrapper item in 08; per-unit test structure in 07; per-case eval table in 05), and resolves the load-bearing ambiguity (materializer) with independent evidence.
**Missing depth elements:** None material. The cluster provides per-case, per-test, per-edit-site, and per-phase granularity sufficient for the builder to author Phase-3/Phase-4/test checklist items without re-deriving facts.

---

## Recommendations
- Proceed. The integration+meta cluster (eval-wire, SKILL demotion, test patterns, MDTM template) has breadth coverage sufficient for granular Phase-3/Phase-4/test item authoring.
- Builder MUST carry forward two surfaced obligations from the research (both already documented, not gaps): (1) a "build the materializer" item (flatten evals.json ids 37–41 → eval_metadata.json + copy `cases/uc2-*/{expected.yaml,input/}` into `iterations/<iter>/eval-<name>/`) wired into `make reflect-eval` upstream of the grader — file 05 §4 Option B; (2) the explicit `uv run ruff format --check src/superclaude/cli/reflect/ tests/cli/reflect/` item (make lint does NOT cover it) — file 07 §3.1.
- Minor (optional): add a dedicated `## Gaps and Questions` header to files 05/06/08 for consistency, though all gap content is already present inline.

---

## VERDICT: PASS

The P2 integration+meta cluster (05 eval-path, 06 SKILL-demotion, 07 test-patterns, 08 MDTM-template) passes completeness verification on the BREADTH lens. All 7 criteria PASS. Zero critical gaps, zero important gaps, two minor findings (M-1 missing dedicated gaps-header in 3 of 4 files; M-2 unverified `--cov` target path). The headline ambiguity (C-5 materializer) is correctly identified, independently re-confirmed this turn as NOT LOCATED, and resolved as a build deliverable with concrete options — this is a completeness strength, not a gap. Doc-sourced claims are uniformly tagged; no contradictions within the subset.

[PARTITION NOTE: This verdict covers ONLY assigned files 05–08. Cross-file checks (contradictions, coverage-vs-full-scope, cross-references) were applied within the P2 subset only. Full cross-file analysis requires merging this report with the P1 partition report.]
