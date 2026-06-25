# Research Completeness Verification — BREADTH Lens

**Topic:** FR-RH2 (sc:reflect Tier-2 ensemble via swarm dispatch library)
**Date:** 2026-06-20
**Lens focus:** BREADTH — every implementation-surface area has corresponding research coverage
**Files analyzed:** 6 (01..06)

---

## Scope of this lens

Verify research coverage for the FR-RH2 implementation surface drawn from §4.6 / §23.2 phases:
- Phase 1: reflect-review lens + output template
- Phase 2: ensemble.py driver + contract.py diversity-source change
- Phase 3: runner.py _audit_once rewire
- Phase 4: config.py --transport/--reviewers
- Phase 5: stub integration test + negative witness
- Phase 6: no-nesting guard extension
- Plus OI-1 field-correspondence table (Q1) and Q6 slug decision.

8 coverage checks below, each PASS (with file evidence) or FAIL (with missing coverage).

---

## File inventory (all 6 read in full, all Status: marked)

| File | Status line | Scope |
|---|---|---|
| 01-reflect-package-runner-config-models.md | "Status: Complete" (§closing); header says "In Progress" (L6) | runner/config/models/commands/__init__ |
| 02-contract-derive-verdict-triggers.md | Complete (L3) | contract.py derive_verdict + triggers + Q6 |
| 03-swarm-seam-dispatch-commands-reduce.md | Complete (L2) | dispatch/commands/reduce/merge/models |
| 04-swarm-lens-precedent-registry-recipes.md | Complete (L3) | bare_review lens / registry / recipes / validator / templates |
| 05-transports-proxy-contract.md | Complete (L3) | transports/stub+openai_compat / env / NFR-RH2.8 grep |
| 06-test-infrastructure-mock-gap.md | Complete (L3) | conftest mock gap / pass.yaml / no-nesting guard / B1-B3 / precedents |

**MINOR FLAG (not breadth-blocking):** File 01 carries `Status: In Progress` in its header frontmatter (L6) but declares `## Status: Complete` at L183 with a full close-out section. The body is complete; the header line is stale. Cosmetic — does not affect coverage. Recommend rf-qa note it so the header is corrected before assembly.

---

## Coverage Check 1 — runner.py seam (_audit_once, expected_tier, Tier-2 launch block)

**PASS.** File 01 documents the full seam with current line anchors, zero-trust verified:
- `_audit_once` full range `runner.py:392-428` (File 01 §1, L33).
- `expected_tier` EXACT quote at `runner.py:403` (`= 2 if config.depth in {"standard","deep"} else 1`) (File 01 §1, L35-38; re-confirmed in DRIFT findings L189).
- The Tier-2 single-`ClaudeProcess` launch block (the FR-RH2 branch point) `runner.py:405-419` with verbatim kwargs incl. `max_turns` G1 note and `_WRAPPER_MARKER` env (File 01 §1, L40-56).
- The parse+derive tail `runner.py:420-428` showing `derive_verdict(...)` call shape the ensemble must preserve (File 01 §1, L58-70).
- Isolation guardrail comment `runner.py:8-12` (NFR-7 "never an Agent/Task surface") (File 01 §1, L28-31).
- Existing imports + `count_model_aliases` (3 ANTHROPIC_DEFAULT_*_MODEL aliases) at L72.
Granularity is sufficient to encode a Phase-3 rewire item with an exact insertion point.

## Coverage Check 2 — contract.py derive_verdict + degraded/halted/blocked triggers + OI-1 left column + Q6 grep

**PASS.** File 02 is comprehensive on the contract consumer side:
- `derive_verdict` range `contract.py:130-246` + verbatim ordering blocked→degraded→halted→pass first-match-wins (File 02 §1).
- Every DEGRADED trigger: 10 distinct branches (TDD's 1-14, collapsed 1-5) with line, exact predicate, returned slug (File 02 §2 table) — incl. `t2_model_class_diversity`, `t2_vendor_diversity`, `merge_method`, `adversarial_convergence_score`, `verification_ran`, `citations_dropped`, `input_drift_detected`.
- Every HALTED trigger with line + slug (File 02 §3 table): status-failed/partial, regression_present, unauthorized_deviation_present, needs_human_decision, user_decision_required, deviation counts.
- Every Stage-1 BLOCKED guard with line + slug (File 02 §4 table): timeout(124), child-crash(F0 veto), contract-missing, contract-version-missing, unknown-major-version, malformed-degraded-components, malformed-contract-boolean.
- **OI-1 LEFT COLUMN fully enumerated** (File 02 §7) — the complete consolidated field list (20 fields) the ensemble must synthesize, grouped by stage with read-lines. This directly satisfies the Q1 field-correspondence requirement.
- **Q6 grep result** (File 02 §0): `ensemble-empty` = ZERO matches, `ensemble` substring in contract.py = ZERO. Full existing BLOCKED slug set enumerated (§6). Both Q6 options (A: net-new branch / B: map onto existing structural slug) are spelled out with the byte-for-byte preservation implication.
Granularity supports per-FR (FR-RH2.7), per-trigger checklist items.

## Coverage Check 3 — three swarm seam signatures + ModelPoolTooSmallError + mechanical_merge boundary + DM records

**PASS.** File 03 covers all required swarm-seam surfaces with verbatim signatures:
- `dispatch_wave1` verbatim signature `dispatch.py:334-343`, return contract (one WorkerResult/slot, proxy_error backstop), `transport_for_slot` precedence, early-exits (File 03 §1).
- `_resolve_run_transport_factory` verbatim signature `commands.py:612-618`, **flagged PRIVATE (Q7 coupling smell)**, openai_compat + stub branches, slot binding `pool[i % len(pool)]` (File 03 §2).
- `reduce_wave3` verbatim signature `reduce.py:555-577`, M/N computation, determine_status/IMM-5 matrix, merge gate `M >= floor` (File 03 §4).
- `ModelPoolTooSmallError` class `commands.py:589`, two args (pool_size, workers_requested), eager raise site `commands.py:688` (File 03 §3).
- `mechanical_merge` boundary `merge.py:50-57` (8 LOC) + the full DISALLOWED-operations enumeration (the FR-RH2.3 boundary) (File 03 §5).
- DM records: WorkerResult/DM-013 (§6a), ResultContract/DM-012 frozen 19-field (§6b), DoneSentinel/DM-017 (§6c), LensEntry/DM-010 14-field (§6d) — all with field order + line anchors.
- Plus OI-1 ABSENCE confirmation (§7, grep exit 1): tier_reached/merge_method/t2_*/reviewer_count/adversarial_convergence_score absent from swarm seam; only shared key `status` (different semantics).
- 4 line-anchor DRIFT findings logged (§c): done.json NOT in reduce_wave3, Literal-not-enum, LensEntry 14-not-11, ResultContract 19-not-18.

## Coverage Check 4 — bare_review lens precedent + 3 registry edit points + recipe reuse + 6 validator assertions + template precedents

**PASS.** File 04 is field-for-field complete:
- `bare_review.py` verbatim LENS block + field-by-field crib table (14 kwargs with lines) (File 04 §1).
- The 3 registry edit points in `lenses/__init__.py` verified against actual structure (import L49-67, LENS_NAMES tuple L73-82, LENSES dict L105-114) with the net-new insertion shown; `__all__` correctly noted as NOT needing edit (File 04 §2).
- Recipe reuse: `bare-review-v1` confirmed present in `recipes.REGISTRY` (L182) AND `recipes.STRATEGIES` (L209) → ZERO recipe-package edits (File 04 §4).
- The 6 validator assertions with field, rule constant, helper lines, and pass-condition for reflect-review (File 04 §3 table), incl. the suspect↔{suspect_files} decision fork.
- Template precedents: bare-review prose (6a) vs feasibility-probe full-frontmatter (6b), with the shape decision for reflect-review (File 04 §6).
- Net-new confirmation (§0): `reflect-review`/`reflect_review` = ZERO hits.
- CANONICAL_INJECTION_GUARD_SENTENCE source `schema.py:133-137` (§5, validator assertion 5).
Granularity supports per-edit-point and per-assertion checklist items.

## Coverage Check 5 — StubTransport (network-free) + read_env env contract + NFR-RH2.8 forbidden-literal grep

**PASS.** File 05 fully covers the transport/proxy surface:
- StubTransport class `stub.py:70`, full import list proving network-free (only hashlib/threading/typing/WorkerResult — no httpx/socket/os/time) (File 05 §1, §SUMMARY(a)). The FR-RH2.5 injection point and deterministic `send` documented.
- `read_env` `openai_compat.py:159`, reads from os.environ (not .aienv file in-code), the three mandatory groups (T2ProxyUrl/T2ProxyKey/T2Model0N), TransportEnvError raise condition (File 05 §2). Matches the .aienv contract.
- **NFR-RH2.8 forbidden-literal grep** (File 05 §4): `:4000`=NONE, `:8317`=NONE, `/cli`=NONE, `/v1`=3 hits ALL docstring-only. VERDICT SATISFIED, grounds U9. Caveat correctly flags R6 should widen the grep to the whole cli/swarm package (the U9 test lane).
- Bonus: URL construction (base 100% from T2ProxyUrl), Bearer header, send() status mapping, Transport protocol — all anchored.
Granularity supports the U9 test-case item and the StubTransport injection item.

## Coverage Check 6 — conftest mock gap + pass.yaml shape + no-nesting guard extension + B1/B2/B3 floor + swarm stub-integration precedent

**PASS.** File 06 is the most directly test-matrix-oriented and covers every sub-item:
- The mock gap: `make_claude_process_stub` `conftest.py:98-138`, exact mechanism, and WHY the new integration test must NOT reuse it (must inject StubTransport at the transport seam) (File 06 §1). Sibling `make_claude_process_sequence` also flagged.
- `pass.yaml` full key list (27 lines / 23 keys) with `tier_reached:2` (L4), `t2_model_class_diversity:full`, `merge_method:adversarial`, `adversarial_convergence_score:0.86` (File 06 §2). Other fixtures enumerated.
- No-nesting guard structure: the 6 tests, the `_REFLECT_PY` glob `L24` that auto-covers ensemble.py for free (tests #3/#4), and the explicit edit needed for the agent-surface guard (test #2 currently runner.py-only) — two concrete extension options (File 06 §3, §SUMMARY(a)).
- B1/B2/B3 regression floor table (File 06 §4): files, line counts, what each pins, whether each patches ClaudeProcess. B2 flagged as the canary coupled to the mock gap.
- Swarm stub-integration precedent `test_commands_run.py::...:507-568` with the mirror structure (stub via CLI flag, results==workers positive proof, results=0 negative witness, worker_done side-effect count) (File 06 §5).
- Bonus: merge-boundary tests (§6), pool-guard precedent CORRECTION (U4 → `test_model_pool_guard.py:40-47`, NOT test_inv005) (§7), collection sanity 79 tests green (§8).
Granularity directly supports per-test-case items B1-B3 and the I-series integration test.

## Coverage Check 7 — Q1 (OI-1) and Q6 resolutions researched enough to encode as BLOCKING gates before FR-RH2.3

**PASS.** Both OI-1 (Q1) and Q6 are researched to encode-able depth:
- **Q1/OI-1:** File 02 §7 gives the complete LEFT column (20 contract fields derive_verdict + helpers read, grouped by stage, with read-lines). File 03 §7 gives the RIGHT column complement — the verdict-driver fields CONFIRMED ABSENT from the swarm ResultContract (grep exit 1), with the only shared key (`status`) and its differing semantics. Together these two halves are exactly the field-correspondence table the OI-1 BLOCKING gate needs: "every field on the left must be synthesized by ensemble.py because none of them comes free off the swarm contract." This is sufficient to author a BLOCKING gate that fails FR-RH2.3 code until the mapping table is filled.
- **Q6:** File 02 §0 + §6 give the grep proof (`ensemble-empty` absent) AND the full existing BLOCKED-slug set AND both decision options with their preservation implications (Option B keeps derive_verdict byte-for-byte). This is sufficient to author the Q6 slug decision as a BLOCKING resolve-before-FR-RH2.3 gate.
No additional research is required to phrase these as blocking gates.

## Coverage Check 8 — granularity sufficient for per-file, per-FR, per-test-case (U1-U9, I1-I9, B1-B3) checklist items

**PASS, with one observation.** Granularity is sufficient across the board:
- **Per-file:** Every target file the implementation touches has a dedicated section with current line anchors (runner/config/models/commands, contract, dispatch/commands/reduce/merge/models, lens+registry+recipes+validator, transports, conftest+fixtures+guards+regression tests).
- **Per-FR:** Mappable — FR-RH2.3 (mechanical_merge boundary: File 03 §5 / File 06 §6), FR-RH2.5 (StubTransport injection: File 05 §1 / File 06 §5), FR-RH2.7 (Q6 + BLOCKED slugs: File 02), NFR-RH2.6 (B1/B2/B3 floor: File 06 §4), NFR-RH2.8 (forbidden-literal grep: File 05 §4).
- **Per-test-case:** B1/B2/B3 fully specified (File 06 §4). U4 (pool guard) and U9 (forbidden-literal) have explicit precedent citations. The swarm stub-integration precedent grounds the I-series shape.
- **OBSERVATION (not a gap):** The research does NOT enumerate the literal U1-U9 / I1-I9 list verbatim from tdd.md §15 — it supplies the *building blocks* (precedents, anchors, fixture shapes, the negative-witness pattern) rather than a one-to-one transcription of each numbered case. That is the correct division of labor (the §15 matrix lives in tdd.md, which is the acceptance oracle the task-builder reads directly); the research provides the code-grounded evidence each case needs. Breadth is satisfied. If the task-builder needs each U#/I# spelled out, it reads tdd.md §15 — not the research files.

---

## Cross-file consistency (breadth seams)

No contradictions across the six files. The seams are internally consistent and cross-referenced:
- OI-1 is covered from BOTH sides without overlap: File 02 = fields read (left column); File 03 = fields absent from swarm contract (right column). They agree on `status` being the only shared key.
- The `bare-review-v1` recipe reuse (File 04 §4) is consistent with the LensEntry field set (File 03 §6d).
- The StubTransport seam (File 05 §1) and the "do NOT patch ClaudeProcess" mock-gap finding (File 06 §1) describe the same injection decision from transport and test angles respectively — consistent.
- Files explicitly delineate cross-track ownership (e.g., File 05 defers retry arithmetic to R3/dispatch; File 04 defers LensEntry dataclass to R3; File 06 defers contract shape to R2). No double-coverage, no orphaned area.

## Depth assessment

Expected: Deep tier (Tier-2 ensemble implementation across reflect + swarm packages). Achieved: Deep — every file traces data flow, gives verbatim signatures, cross-validates TDD anchors against shipped source (zero-trust), and logs anchor DRIFT corrections. The DRIFT findings (File 01 PASS→BLOCKED location nuance; File 03 done.json/Literal/field-count; File 06 U4 pool-guard file correction) are exactly the kind of adversarial cross-checking the depth tier requires.

---

## VERDICT: PASS

All 8 breadth coverage checks PASS. Every area the FR-RH2 implementation surface touches (Phases 1-6 per §4.6/§23.2, plus the OI-1/Q1 field-correspondence table and the Q6 slug decision) has corresponding, code-grounded research coverage with current line anchors. The Q1 (OI-1) and Q6 resolutions are researched to encode-able-as-BLOCKING-gate depth. Granularity supports per-file, per-FR, and per-test-case (B1-B3 explicit; U/I series via precedents + tdd.md §15 oracle) checklist items.

### Non-blocking observations for rf-qa / task-builder (no gaps)
1. **File 01 header staleness (cosmetic):** frontmatter `Status: In Progress` (L6) contradicts the `## Status: Complete` close-out (L183). Body is complete; correct the header before assembly.
2. **U1-U9 / I1-I9 not transcribed verbatim** in research (by design — the §15 matrix lives in tdd.md, the acceptance oracle). Task-builder should source each numbered case from tdd.md §15 and attach the research evidence (precedents/anchors) to it. Not a coverage gap.
3. **Anchor DRIFT corrections** logged by researchers (done.json emitter, Literal-vs-enum, LensEntry 14 fields, ResultContract 19 fields, U4 pool-guard file = test_model_pool_guard.py) MUST flow into the task file so item anchors match shipped source, not the TDD's original (sometimes-off) anchors.
4. **Q7 coupling smell** (`_resolve_run_transport_factory` is module-private) is surfaced by File 03 §2 but is a design decision, not a research gap — the task-builder must decide import-private vs expose-public-wrapper.
