# Adversarial Debate Transcript — Phase 13 (Final Acceptance) Pre-Validation

## Metadata
- Mode: B (inline; sub-agent spawning unavailable — three advocate lenses simulated)
- Advocate lenses: opus:architect (necessity/redundancy/architecture), sonnet:qa (correctness vs Acceptance gates, pre-existing-failure/disk realities), haiku:analyzer (fragility, citation grounding)
- Source: TASK-RF-20260531-042405 §Phase 13 (L703–797) vs BUILD-REQUEST §Acceptance gates 1–8 + §Contract items 1–10; master §Recurrence Matrix
- Convergence threshold: 0.80
- Depth: deep (Round 2.5 invariant probe included)

## Round 1 — Advocate Statements (per item, condensed to load-bearing positions)

### Step 13.1 (Seed recurrence corpus — derive seeding map)
- **architect**: KEEP. This is the discovery anchor for M4. The 18-row → failure-class → citation → fixture-filename table is exactly the named-incident mapping sc:reflect M4 demanded "at the start of Phase 13, not at the end". Steelman of DISCARD: "could fold into 13.2" — rejected; separating discovery from creation is correct MDTM hygiene and lets the DEFERRED-row decision happen once, up front.
- **qa**: KEEP w/ caveat. Correct against Gate #4 (enumerates the exact 18 rows). The "Already created? Y/N" provenance column is verifiable: corpus today has `anti_instinct` (#6) + `id_containment` (#4); task asserts #9 (retry) lands in R1.6 Step 11.6. So at Phase 13 entry only 2 of the 3 claimed "already created" may physically exist — the map must verify, not assume.
- **analyzer**: KEEP. Anti-fabrication clause ("each maps to a real master/partition citation") is the right guard. Fragility: row→class is non-injective; the item must allow a row to map to a NEW subdir.

### Step 13.2 (Create 15 NEW fixture pairs)
- **architect**: REFACTOR. The "15 NEW" count is arithmetically sound (18 RECURRENT − 3 already = 15). But several rows are NOT fixture-as-scanner-input testable: #17 (context-window OOM — a runtime resource failure, no scanner resolves it), #21 (sprint executor — explicitly OUT of scope per BUILD-REQUEST §Scope "Out: src/superclaude/cli/sprint/"), #10/#3-lint (generator/validator asymmetry — a PR-description lint, not a corpus case). The DEFERRED escape exists but must be pre-pointed at these rows, else the agent burns cycles trying to fabricate scanner inputs for non-scannable failures.
- **qa**: REFACTOR. The <200-line / well-formed-JSON constraints are good. The risk is "DEFERRED" being used as an escape hatch that silently drops Gate #4 coverage. Gate #4 says "≥1 named fixture for EVERY RECURRENT row". A DEFERRED row with no fixture file FAILS Gate #4 literally. Need: a DEFERRED row still gets a fixture stub + xfail/skip marker with a reason, so the count is honored and the test surface is honest.
- **analyzer**: KEEP-leaning-REFACTOR. Verbatim-from-incident derivation is correct anti-hallucination discipline. Subdir pre-creation list is incomplete vs the 18 rows' true class spread.

### Step 13.3 (Create test_recurrence_regression.py — Contract #1)
- **architect**: REFACTOR (highest-severity item). File genuinely MISSING (no redundancy). BUT the hard-coded dispatch map covers only 6 classes (anti_instinct→scanner, spec_fidelity→fidelity_checker, frontmatter_parser→parse_frontmatter, retry_contract→walker, threshold_registry→arch_lint, id_containment→id_registry+MERGE_GATE). Rows #2/#14 (written-but-not-wired) → dispatch-reachability, #15 (merge completeness), #16 (telemetry), #5/#12/#19/#22 — have NO entry in that map. The item demands "every fixture exercised, no fixture silently skipped, all 6+ failure classes" — but a fixture in a 7th class would hit the dispatch `else` and either error or skip. Self-contradiction unless the dispatch map is made explicitly extensible with an enumerated skip/xfail registry.
- **qa**: REFACTOR. Contract #1's defining property — "MUST FAIL on pre-fix codebase and PASS post-fix" — is UNVERIFIABLE for fixtures whose fix already landed in R0/R1 (anti_instinct, id_containment, threshold). Those will PASS today (post-fix) but there's no pre-fix checkout to prove they'd have failed. The item should accept the Contract-#1 fail/pass property as established per-class at the phase that landed the fix (R0.1/R0.2/R0.3/R1.x), and have 13.3 assert only the steady-state PASS + the "no silent skip" invariant.
- **analyzer**: KEEP-mechanism, REFACTOR-scope. Glob-enumerate-all is the right anti-skip mechanism. The dispatch-ambiguity blocker escape is present, which softens the contradiction, but the item should name the extensibility requirement rather than rely on the blocker.

### Step 13.4 (Final CI gate wiring for Contract 1–10)
- **architect**: REFACTOR. Big redundancy risk. Contracts #5/#8 (constant-dup arch-lint) already wired (Makefile `lint-architecture` Check 11); #2 dispatch-reachability test exists (test_dispatch_reachability.py); #9 id-containment test exists; #3 phantom-ID via tool-write schemas (R1.4); #10 anti-instinct recurrence test exists. The item reads "extend the CI wiring to ensure all 10 run" — that's fine IF it is "verify + fill gaps", but as written it lists re-wiring all 10 as if greenfield. REFACTOR to "audit what R0/R5/R1.3/R1.4 already wired, then wire only the genuinely-missing surfaces (the 5 new test files + the Contract #3 PR-description lint mechanism)".
- **qa**: REFACTOR. Reads a Phase-5 plan (`r0-ci-gate-wiring.md`) that does not yet exist (Phase 5 unrun) — fine as forward-ref, but the item must tolerate its absence (reconstruct from Makefile + test tree). The pipeline-blocking vs PR-blocking split is verbatim-correct vs Contract §Pass-criterion. M1 gap: Contract #3 "Generator-Constraint Considered" PR-lint mechanism is named ("CI lint") but not specified — must name the actual mechanism (pre-commit hook / GH Action grep on PR body touching gates.py/structural_checkers.py/*_validator.py).
- **analyzer**: KEEP-leaning-REFACTOR. The override-with-reason requirement is correctly sourced. Fragility: "GitHub Actions if present" — repo CI mechanism should be confirmed before asserting a workflow file.

### Step 13.5 (Run complete suite — Acceptance gate #2)
- **qa**: REFACTOR (correctness defect). VERIFIED: `tests/roadmap/` currently has 3 FAILING tests — `test_models.py::TestRoadmapConfig::test_default_agents`, `test_cli_contract.py::TestAgentsParsing::test_default_agents_when_not_provided`, `test_validate_unit.py::TestValidateConfigDefaults::test_default_agents_two` (haiku-vs-sonnet model default). These are PRE-EXISTING and OUT of scope (model defaults, not pipeline-rewrite). The item says "all 64 existing tests + all new contract tests pass with zero failures" and "If any failure, fix it (edit src/ only) and re-run until green." As written 13.5 can NEVER pass — it would force the agent to mutate unrelated model-default code or loop forever. Gate #2's real bar is "all CURRENTLY-PASSING tests still pass (no regressions)", NOT "green suite". REFACTOR to baseline-delta semantics with a known-pre-existing-failure allowlist (the 3 test_default_agents).
- **architect**: AGREE REFACTOR. Gate #2 BUILD-REQUEST text is literally "All current passing tests in tests/roadmap/ still pass" — a no-regression bar, not a zero-fail bar. The item over-tightened it.
- **analyzer**: AGREE. The "64 existing tests" figure is also stale — `tests/roadmap/` now holds ~1900+ collected tests; the literal "64" assertion is a citation that will mislead.

### Step 13.6 (End-to-end live pipeline over corpus — Acceptance gate #3)
- **architect**: REFACTOR. Corpus VERIFIED: 38 `spec*.md` under `.dev/releases/complete/*/`. Running the full live pipeline (with R1.3 Option B certify now executing real LLM subprocesses) over 38 specs = 38 multi-step LLM pipeline runs writing artifacts. M5 time-budget guard (4h/spec, escalate at 80%) is NOT in the current 13.6 text — must be added. Disk: this worktree is 72% full (34G free) and the session already hit ENOSPC during pipeline work; 38 runs × debate+remediate+certify artifacts is a real ENOSPC risk. Output path `.dev/releases/Current/` collides with an existing lowercase `.dev/releases/current/` (both present) — case-insensitive FS hazard.
- **qa**: REFACTOR. Gate #3's actual bar is "no halts on anti-instinct FALSE-POSITIVES of the master's taxonomy classes" — NOT "every spec reaches terminal step". The item already states new halts = follow-ups not failures (correct). But it must add: per-spec wall-clock cap + disk pre-check + cost ceiling, and a sampling fallback (run a representative subset if 38 full runs blow the budget) so the gate is achievable.
- **analyzer**: KEEP-leaning-REFACTOR. The FP-class focus is correctly sourced to Gate #3 + Contract #10. The empty-corpus blocker escape exists. Add the Current/current path disambiguation.

### Step 13.7 (Verify Acceptance Gates 1–8)
- **architect**: KEEP. Per-gate evidence + explicit verification command per gate is exactly right; no hand-waving. Gate #6 (step count ≤14) verification command VERIFIED to return 12 today — gate already satisfied with headroom. Gate #7 grep-for-fragility-stubs and Gate #8 test_certify_step_reachable both verified present.
- **qa**: KEEP w/ caveat. Gate 5 references `r0-acceptance-multimodelswarm-summary.md` (a forward R0 artifact) — must tolerate its location. Otherwise the 8-gate enumeration matches BUILD-REQUEST §Acceptance gates verbatim. The Gate-2 sub-verification inherits 13.5's baseline-delta fix — must read summary as "no regressions" not "zero fails".
- **analyzer**: KEEP. Strongest item in the phase: every gate has a falsifiable command. Minor: the `grep 'return True\s*#...'` Gate-7 pattern must be byte-aligned with Contract #5's exact regex to avoid a false-clean.

### PG13.1 / PG13.2 (Terminal QA gate + act on verdict)
- **architect**: KEEP. Independent re-verification of every gate by re-running the command (not trusting the report) is the correct anti-overclaim mechanism. Sampling 3 contracts on synthetic violations is sound. fix_authorization:true + ADVERSARIAL STANCE + halt-precedence + 3-cycle cap matches the project's rf-qa pattern (MEMORY: feedback_rfqa_adversarial_pattern).
- **qa**: KEEP. The "cannot pass with FAIL findings — escalate to user" terminal property is correct for a final acceptance gate.
- **analyzer**: KEEP. Will-spawn-fail fallback (log blocker, mark complete) is present and consistent with every other gate item. The MVR-preservation re-checks (commands.py 20 options, structural_checkers/convergence/cosmetic_remediator) are correctly sourced to BUILD-REQUEST §Scope "Out".

### Post-Completion items (verify-outputs, final-regression, task-summary, status-flip)
- **all three**: KEEP. Standard MDTM closure. One caveat (qa): the final-regression item (L749) inherits the same green-suite-vs-baseline issue as 13.5 — "confirming all tests still pass with no regressions" must mean no-regressions, and the 3 pre-existing failures must be acknowledged or the closure loops.

## Round 2 — Rebuttals (convergence-relevant)
- DISCARD was floated only against 13.1 (fold into 13.2) and 13.4 (claimed fully-redundant). Both rejected: 13.1's up-front DEFERRED decision has standalone value; 13.4 is partially-redundant not fully (5 test files + Contract #3 lint genuinely unwired) → REFACTOR not DISCARD.
- No advocate defended the literal "zero failures / 64 tests" wording of 13.5 → unanimous REFACTOR.
- Disagreement on 13.3 severity resolved: the dispatch-ambiguity blocker escape exists, so it is not a blocker-class defect, but the self-contradiction ("no silent skip" vs 6-class dispatch) is real → REFACTOR.

## Convergence
- Converged: 0.91 (10/11 items unanimous; 13.3 reached majority after Round 2). All taxonomy levels covered (L2 architecture, L3 state/gate mechanics). No HIGH-unaddressed invariants after probe (see invariant-probe.md).
