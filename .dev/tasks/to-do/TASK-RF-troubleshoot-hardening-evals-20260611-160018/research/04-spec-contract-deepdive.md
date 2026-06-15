# R4 — Doc Cross-Validator: RELEASE-SPEC Backtest Contracts

**Status: In Progress**

**Topic**: Extract the exact contracts the differential backtest harness (replays E1–E5, sets `backtest_status` per NFR-1) must satisfy, verbatim from the RELEASE-SPEC, and cross-validate each against actual code.

**Spec under analysis**: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-RELEASE-SPEC.md` (v1.1.0, status: draft, feature_id TSH-HARDEN-1).

**Cross-validation legend**:
- `[CODE-VERIFIED]` — confirmed in actual code at file:line
- `[CODE-CONTRADICTED]` — spec claim disagrees with actual code
- `[UNVERIFIED]` — cannot confirm in code; for the NEW H0–H5 gate logic this is EXPECTED (impl branch has not landed; this is a G1 spec, implementation halted pending approval per §1.2)

---

## §0 — Cross-Validation Posture (read first)

The RELEASE-SPEC is a **G1 spec; implementation is HALTED pending G1 approval** (§1.2 "Out of scope": "Building/validating the hardening (this is the G1 spec; implementation is halted pending G1 approval). Any edit to `src/superclaude/` or `.claude/` skill/command files before approval."). Therefore the entire H0–H5 gate apparatus, the new output-contract fields, the 6 new refs, the `tests/troubleshoot/` suite, and the backtest harness are **greenfield**. For all of those, `[UNVERIFIED]` is the EXPECTED and CORRECT tag — the impl branch has not landed.

What CAN be code-verified are the **substrate facts the backtest replays depend on**: the real E1–E5 escape mechanisms in existing code (esp. E4's `_evaluate_gate` / `gate_passed` / `SemanticCheck.advisory`), the existing skill surface that the new contract appends to, and the absence of any pre-existing harness.

**Greenfield confirmation (verification agent #2):**
- 6 proposed refs (`pipeline-hardening-closure.md`, `runtime-entrypoint-verification.md`, `contract-enumeration.md`, `unmask-and-sweep.md`, `effective-input-proof.md`, `hardening-output-contract.md`) — **NONE exist** under `src/superclaude/skills/sc-troubleshoot-protocol/refs/` (existing refs: calibrator-eval-cases, diagnosability-audit, doc-discovery, escalation-rubric, hypothesis-card-template, remediation-handoff, report-template, triage-checklist). `[UNVERIFIED — expected]`
- Output fields `pipeline_hardening_applicable`, `pipeline_hardening_verdict`, `backtest_status`, `waiver_status`, `known_escapes_caught`, `off_path_review_decision` — **zero hits in source code** (only in `.dev/tasks/.../research` notes). `[UNVERIFIED — expected]`
- `contract_version` — EXISTS but belongs to the **swarm** result contract (`tests/swarm/test_result_contract.py`), NOT troubleshoot-protocol. The spec reuses the name for a new purpose. `[CODE-VERIFIED that the name is taken elsewhere — note for impl: namespacing]`
- `tests/troubleshoot/` directory — **DOES NOT EXIST**; none of `test_hardening_{h0,h1,h2,h3,h4,verdict,output_contract}.py` exist. `[UNVERIFIED — expected]`
- `report-template.md` has **no "Pipeline Hardening Closure" section** (259 lines, ends at Audit). `[UNVERIFIED — expected]`
- No E1–E5 backtest/replay harness anywhere; string "negative witness" has **zero repo hits**. The E1–E5 escapes exist only as **description directories** under `.dev/troubleshoot-meta/20260610T141100Z/escape-E{1..5}-*/`. `[UNVERIFIED — expected; these dirs are the replay source material]`

---

## §1 — CONTRACT A: The E1→Wave→FR→Backtest-Scenario 1:1 Mapping (verbatim, §3.1 Traceability Matrix, spec lines 251–257)

The harness MUST replay exactly these 5 escapes; each row binds escape → closing wave(s) → FR(s) → required evidence card(s) → backtest scenario. Reproduced VERBATIM:

| Escape | Mechanism | Closing Wave(s) | FR(s) | Required Evidence Card(s) | Backtest Scenario |
|--------|-----------|-----------------|-------|---------------------------|-------------------|
| **E1** | CLI/helper proof accepted while headless subprocess rejected local paths | **H1, H2** | FR-3, FR-4, FR-6 | Runtime-entrypoint card with replay reaching production subprocess; contract ledger proving sibling file-delivery consumers swept | Replay headless PRD `--spec` with local-path `--file`; negative witness fails pre-fix and positive passes post-fix |
| **E2** | Substring classifier accepted `complete` inside `incomplete` and applied the wrong phase invariant | **H3** | FR-7, FR-8 | Whole-artifact classifier card with positive executable violation plus `incomplete` near-miss negative | Full generated artifact containing setup/work/completion sections; only executable target hard-fails |
| **E3** | Single reported heading fixed while same-token sibling headings remained unswept | **H3** | FR-7, FR-8, FR-9 | Unmask-and-sweep card with `K_true`, `K_swept`, same-token/same-shape family evidence, and false-positive fixture results | Artifact containing Task-Log/Findings sibling headings; non-executable headings WARN/CONTINUE rather than HALT |
| **E4** | Shared `SemanticCheck.advisory` honored by generic gate but not PRD evaluator | **H1, H2** | FR-3, FR-5, FR-12 | Runtime-entrypoint card proving PRD path reaches `_evaluate_gate`; H2 ledger classifying generic gate, PRD evaluator, trailing gate, remediation dispatch | Advisory semantic check runs through PRD evaluator; ledger fails until all live consumers classified |
| **E5** | Review selector consumed an adjacent/foreign range instead of dirty `/task` work | **H4, H5** | FR-10, FR-11, FR-12 | Effective-input manifest proving dirty/staged/unstaged inclusion and foreign-commit exclusion; off-path review decision | POST-reflect with dirty task work plus foreign commit; H4 fails until `E ∩ true_runtime_surface` is proven |

**Cross-cut with §1.1 Evidence (E1–E5 table, spec lines 31–35) — the provenance commits the replay material derives from:**
- E1 ← MERGED #151 `7601ad25` (root-cause: `escape-E1-*/root-cause.md`). `[CODE-VERIFIED: escape-E1 dir exists]`
- E2 ← MERGED #154 `e97aa4fd`, review `r3383060121`. `[CODE-VERIFIED: escape-E2 dir exists]`
- E3 ← MERGED #155 `eb9a2633`. `[CODE-VERIFIED: escape-E3 dir exists]`
- E4 ← **UNMERGED `b97c9960`** (merged report §9). `[CODE-VERIFIED: b97c9960 exists, NOT ancestor of HEAD; but see §4 — the fix DID land via a different commit 20693bb8]`
- E5 ← MERGED #153 `10723863`. `[CODE-VERIFIED: escape-E5 dir exists]`

**Mapping is referenced consistently across the spec** (Quantity-Flow §2.2 lines 63–93 and Phase Contracts §5.3 lines 377–386 use the same H1=runtime, H2=ledger, H3=unmask, H4=effective-input, H5=off-path numbering). The spec EXPLICITLY warns this numbering differs from "merged report §10's variant (H3=classifier, H4=unmask, H5=effective-input)" and declares **this spec's H0–H5 canonical** (§2.1 Key Design Decisions line 53; Appendix A "Wave-numbering crosswalk" line 641). **HARNESS IMPLICATION:** the backtest must use the SPEC's wave numbers, not the merged report's. `[UNVERIFIED — gate logic greenfield; the crosswalk caveat is a real trap for the harness author]`

---

## §2 — CONTRACT B: `backtest_status` — enum, default, type, derivation, and the CRITICAL separation from `pipeline_hardening_verdict`

This is the single most load-bearing contract for the harness. Three spec locations define it; they are mutually consistent.

### 2.1 Type / Default / Invariant — §4.5 State Variable Registry (spec line 316, verbatim)

| Variable | Type | Initial | Invariant | Read | Write |
|----------|------|---------|-----------|------|-------|
| `backtest_status` | enum `not_run\|partial\|complete` | `not_run` | Production-facing coverage signoff remains advisory until E1–E5 backtests complete | report, roadmap | E1–E5 backtest gate (NFR-1) |

- **Enum values (exactly 3):** `not_run`, `partial`, `complete`. `[UNVERIFIED — greenfield enum; no code defines it]`
- **Default / initial:** `not_run`.
- **Writer:** the **E1–E5 backtest gate (NFR-1)** — i.e. THIS harness is the sole producer.
- **Readers:** `report` (REPORT.md) and `roadmap`.

### 2.2 Field Schema — §5.5 Output Contract Field Schema (spec line 433, verbatim)

| Field | Type | Required | Default | Nullability | Producer | Consumer Behavior If Missing |
|-------|------|----------|---------|-------------|----------|------------------------------|
| `backtest_status` | enum `not_run\|partial\|complete` | **yes** | `not_run` | **non-null** | NFR-1 replay suite | **Missing ⇒ treat production-facing signoff as `advisory`** |

- Required: **yes**. Non-null. Fail-safe default on absence = `advisory` signoff (never silently `complete`).

### 2.3 Derivation Rule — §5.4 "Backtest Status vs Run-Level Verdict" (spec lines 413–423, verbatim)

> `pipeline_hardening_verdict` is the **run-level H0–H5 closure verdict**. It may be `pass` when every applicable wave passes and `waiver_status=none`. `backtest_status` is the separate **coverage-validation state** for NFR-1:

| Backtest Status | Meaning | Production-Facing Pipeline-Health Signoff |
|-----------------|---------|-------------------------------------------|
| `not_run` | No E1–E5 replay suite has run against the built hardening gates | **`advisory` even if `pipeline_hardening_verdict=pass`** |
| `partial` | Some, but not all, E1–E5 replay scenarios have passed | **`advisory` with missing escape IDs listed** |
| `complete` | E1–E5 replay scenarios all pass against the built gates | **May mirror `pipeline_hardening_verdict`** |

> REPORT.md must render **both** fields so downstream consumers do not confuse a clean H0–H5 run with validated E1–E5 catch-rate coverage. (spec line 423)

**DERIVATION RULE the harness MUST implement (canonical, restated for the harness author):**
- **all 5 of E1–E5 pass** → `backtest_status = complete`
- **some (1–4) pass** → `backtest_status = partial` **AND the report must list the missing escape IDs** (the not-yet-passing E-IDs) — per §5.4 row "`partial` ... advisory with missing escape IDs listed". This is a hard schema requirement, not optional.
- **none pass / suite not run** → `backtest_status = not_run`

### 2.4 THE CRITICAL DISTINCTION (the reason this contract exists)

`backtest_status` is **SEPARATE from `pipeline_hardening_verdict`**. They answer different questions:
- `pipeline_hardening_verdict ∈ {pass, blocked, advisory, not_applicable}` = "did THIS run's H0–H5 waves close?" (run-level; §4.5 line 311).
- `backtest_status ∈ {not_run, partial, complete}` = "have the built gates been PROVEN to catch the canonical escape corpus E1–E5?" (coverage-level; §4.5 line 316).

**Hard rule:** production-facing pipeline-health **signoff stays `advisory`** even when `pipeline_hardening_verdict=pass`, UNTIL `backtest_status=complete`. A clean H0–H5 run does NOT earn production signoff by itself. Only `complete` lets the signoff "**May mirror** `pipeline_hardening_verdict`" (note: "may", not "must" — even at `complete` the mirror is permissive, not forced).

This is reinforced as a **Risk-Assessment mitigation** (§7, spec line 538): *"Predicted coverage never validated post-G1 / Medium / High / `backtest_status` separates H0-H5 run verdict from production-facing coverage signoff; signoff stays `advisory` until E1-E5 `complete`."* `[UNVERIFIED — greenfield; but the separation is unambiguous and triple-stated: §4.5, §5.4, §7]`

### 2.5 NFR-1 — the catch-rate target the harness measures (§6, spec line 523, verbatim)

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-1 | E1–E5 backtest catch rate | **100% would-have-caught (post-build, predicted until then)** | Replay each escape against the built gates |

**Interpretation for the harness:**
- Target = **100% would-have-caught** across E1–E5 (all 5 gates must catch their escape).
- "**predicted until then**" / "(post-build, predicted until then)" = until the hardening gates are actually BUILT, the catch claim is a *prediction*, not a measurement. The harness only produces a real (non-predicted) `complete` once the gates exist and all 5 replays pass against them. Before build, `backtest_status` cannot legitimately be `complete` — it is `not_run`.
- Governing integration test named in the spec: `test_backtest_status_keeps_pipeline_health_advisory_until_complete` (§8.2, spec line 568) — validates "separates H0-H5 run verdict from production-facing E1-E5 catch-rate signoff." `[UNVERIFIED — test does not exist; greenfield]`

---

## §3 — CONTRACT C: Per-Escape Expected Outcomes — §8.3 Manual/E2E (spec lines 573–580, verbatim) cross-cut with §2.2 Quantity-Flow divergence scenarios

These are the exact pass/fail oracles each replay must assert. Reproduced VERBATIM from §8.3, with the matching §2.2 divergence note and a code-cross-validation tag per escape.

| Scenario | Steps (verbatim §8.3) | Expected Outcome (verbatim §8.3) | Cross-validation |
|----------|------------------------|----------------------------------|------------------|
| **E1 backtest** | Replay headless PRD `--spec` with local-path `--file` against H1 | **H1 FAIL pre-fix (negative witness), PASS post-fix** | E1 product fix MERGED #151 `7601ad25`. The replay needs a fix-reverted run (negative witness) → FAIL, fix-applied → PASS. `[UNVERIFIED — H1 gate greenfield; substrate `--spec`/`--file` CLI surface verified to exist via R1 scope]` |
| **E2 backtest** | Replay full generated artifact containing `complete` and near-miss `incomplete` phase text against H3 classifier | **Intended executable violation still HALTs; near-miss sibling negative does not hard-fail** | E2 = substring `complete`⊂`incomplete` (§1.1 line 32; MERGED #154 `e97aa4fd`). §2.2 DIVERGENCE: "1 fix → ... only executable target hard-fails". `[UNVERIFIED — H3 greenfield]` |
| **E3 backtest** | Replay Task-Log/Findings sibling-heading artifact against H3 unmask/sweep card | **H3 FAILs until `K_swept == K_true` and non-executable headings WARN/CONTINUE rather than HALT** | E3 = same-token sibling headings unswept (MERGED #155 `eb9a2633`). §2.2: "1 fix → 4 sibling 'Findings' headings; sweeping 1 → 3 escape" (so K_true=4). The harness asserts K_swept==K_true AND severity downgrade (WARN/CONTINUE) for non-executable headings. `[UNVERIFIED — H3 greenfield]` |
| **E4 backtest** | Run advisory check through PRD `_evaluate_gate` with H2 ledger | **H2 FAIL until both `gate_passed` and `_evaluate_gate` consumers classified** | **SEE §4 — CODE-VERIFIED substrate, with a state nuance.** The H2 gate is greenfield, but its replay targets REAL functions that currently exist on HEAD. `[UNVERIFIED for H2 gate; CODE-VERIFIED for the `_evaluate_gate`/`gate_passed`/`advisory` substrate]` |
| **E5 backtest** | POST-reflect with dirty `/task` work + a foreign commit in range | **H4 FAIL closed (wrong surface) until selector proven correct** | E5 = review selector wrong diff base (MERGED #153 `10723863`). §2.2: "selector → 5 commits, intersection with real /task work = 0". H4 must FAIL on non-empty-but-wrong-surface (the F-D1 fix, FR-10 line 208), not just on E=0. `[UNVERIFIED — H4 greenfield]` |

**Plus the cross-cutting waiver replay (§8.3 last row, spec line 580, verbatim):**

| Scenario | Steps | Expected Outcome |
|----------|-------|------------------|
| Waiver re-green attempt | Waive H1, then run downstream reflect/adversarial | **Verdict stays `blocked`/`advisory`; never `pass`** |

This is the NFR-4 durability check (§6 line 526: "No-re-greening durability / 100% / Adversarial test: attempt downstream re-green") and is bound to the one-way `waiver_status` latch (FR-12 line 231, SV `waiver_status` §4.5 line 315). Not strictly an E1–E5 replay, but the same harness should cover it. `[UNVERIFIED — latch logic greenfield]`

### 3.1 Per-escape FAIL-oracle precision (what "FAIL" must mean, so the harness is not theatre)

- **E1 H1:** FAIL is only valid if it is a **negative witness** — fix-reverted run through the *production headless subprocess boundary*, observed to FAIL. A test never observed to fail does NOT satisfy H1 (FR-4 line 140). The positive (fix-applied) must PASS at the same boundary.
- **E2 H3:** Two assertions — (a) intended executable violation **still HALTs** (positive control), (b) the `incomplete` near-miss **does not hard-fail** (sibling negative). Word-boundary/grammar match required (FR-8 line 184; §5.7 grammar lines 510–517).
- **E3 H3:** FAIL **until** `K_swept == K_true` (sweep completeness) AND non-executable headings map to **WARN/CONTINUE not HALT** (severity-by-consumer, FR-7 line 173 / H3 card `severity_assertions_by_consumer` line 492).
- **E4 H2:** FAIL **until** the ledger classifies **all** live consumers — explicitly **both `gate_passed` AND `_evaluate_gate`** (and per §3.1 matrix also "trailing gate, remediation dispatch"). An empty/zero-row ledger does NOT vacuously pass (FR-5 line 150, F-N3).
- **E5 H4:** **FAIL closed** on non-empty-but-wrong-surface — correctness of `|E ∩ true_runtime_surface|` must be proven, not merely `E>0` (FR-10 line 208, F-D1). Proof via machine-checkable manifest with dirty/staged/unstaged inclusion + foreign-commit exclusion.

---

## §4 — CODE-VERIFIED SUBSTRATE: E4's `_evaluate_gate` / `gate_passed` / `SemanticCheck.advisory` — with a CRITICAL state nuance for the harness

E4 is the **one escape whose substrate is real existing code** (not a markdown gate). The spec's E4 mechanism claim and the E4 replay both reference concrete symbols. I cross-validated every one.

### 4.1 Symbol existence — all `[CODE-VERIFIED]`

| Spec claim | Code location | Tag |
|------------|---------------|-----|
| `_evaluate_gate` is the "live PRD path" evaluator (§1.1 E4 line 34; §3.1 E4 line 256; §8.3 E4 line 578) | `src/superclaude/cli/prd/executor.py:823` — method `_evaluate_gate(self, step_id, gate, content) -> bool` on `PrdExecutor` | `[CODE-VERIFIED]` |
| `gate_passed` is the "generic" gate (§1.1 E4 line 34; §3.1 E4 line 256) | `src/superclaude/cli/pipeline/gates.py:23` — `gate_passed(output_file, criteria, *, envelope, repo_root) -> tuple[bool, str\|None]` | `[CODE-VERIFIED]` |
| `SemanticCheck.advisory` is a shared field (§1.1 E4 line 34; §3.1 E4 line 256; §8.3 E4 line 578) | `src/superclaude/cli/pipeline/models.py:82–94` — `class SemanticCheck` with `advisory: bool = False` | `[CODE-VERIFIED]` |

### 4.2 The CRITICAL state nuance — E4 is currently in a POST-FIX state on HEAD

The spec (v1.1.0, drafted 2026-06-10) describes E4 as **"fix committed-but-unmerged"** (§1.1 line 34: "Advisory treated as fatal on the live PRD path; fix committed-but-unmerged"; §1.2 line 42: "E4 fix `b97c9960` committed-but-unmerged and tracked separately"; §3.1 E4 row implies divergence still latent).

**CURRENT CODE STATE (verified on HEAD, 2026-06-11):**
- `b97c9960` ("fix(prd): honor advisory checks in the executor's `_evaluate_gate`") — **EXISTS but is NOT an ancestor of HEAD** (`git merge-base --is-ancestor b97c9960 HEAD` → false). It lives only on `origin/fix/prd-executor-advisory-gate`. So the spec's literal claim "`b97c9960` unmerged" is **`[CODE-VERIFIED]` as still-unmerged**.
- **HOWEVER** the *same fix landed via a different commit*: **`20693bb8`** ("fix(prd): honor advisory semantic-check flag in executor._evaluate_gate", author RyanW, 2026-06-11 12:15) — **IS an ancestor of HEAD** (`git merge-base --is-ancestor 20693bb8 HEAD` → true).
- Therefore on HEAD **both** paths now honor `advisory`:
  - `executor.py:859` — `if getattr(check, "advisory", False):` → logs `True`/non-fatal and `continue` (does NOT return False). Comment at lines 853–858 explicitly says "The generic pipeline/gates.py:gate_passed honors this; the PRD executor must too."
  - `gates.py:94` — `if getattr(check, "advisory", False):` → `_log.warning(...)` then `continue`.

**⚠ HARNESS IMPLICATION (this is the load-bearing nuance):** The §8.3 E4 expected outcome is "H2 **FAIL until** both `gate_passed` and `_evaluate_gate` consumers classified" — that oracle is about the **H2 ledger gate's behavior** (does the ledger enumerate both consumers?), NOT about whether the advisory divergence is currently live. The E4 *product divergence* is already healed on HEAD via `20693bb8`. So an E4 replay that tries to reproduce "advisory treated as fatal on `_evaluate_gate`" by running CURRENT code will **NOT reproduce the bug** — the harness must either (a) replay against the **pre-fix tree** (revert `20693bb8` / check out a parent, the negative-witness pattern from FR-4), or (b) treat E4 as a **ledger-completeness** test (assert the H2 ledger names both `gate_passed`+`_evaluate_gate`+trailing-gate+remediation-dispatch), which is exactly what §8.3 E4 asserts. Option (b) matches the spec's wording; option (a) is needed only if a literal advisory-fatal negative witness is required.

This is a `[CODE-CONTRADICTED]` on the spec's *narrative state* ("fix committed-but-unmerged") **only in the sense that the fix has since landed via a sibling commit** — the spec was accurate at its 2026-06-10 authoring; HEAD moved on 2026-06-11. The harness author MUST NOT assume current `main`/HEAD still exhibits the E4 advisory-fatal bug. R5 (git-level replay-commit semantics) should pin the exact base commit for the E4 negative witness.

### 4.3 R3.1 matrix note: §3.1 lists the E4 ledger consumers explicitly
The §3.1 E4 "Required Evidence Card(s)" column names the full live-consumer set the H2 ledger must classify: **"generic gate, PRD evaluator, trailing gate, remediation dispatch"** (spec line 256). The first two are `[CODE-VERIFIED]` (`gates.py:gate_passed`, `executor.py:_evaluate_gate`). "Trailing gate" and "remediation dispatch" are not pinned to a file here — R1 (eval API) / R6 (impl tasklist) should resolve those two for the ledger-completeness oracle. `[PARTIALLY CODE-VERIFIED — 2 of 4 consumers located]`

---

## §5 — CONTRACT D: Executable Validation Architecture the harness must plug into (§4.7, spec lines 334–347)

The spec mandates that **every closure artifact affecting `pipeline_hardening_verdict` has an executable validation surface "so tests cannot pass from prose alone"** (§4.7 line 336). The backtest harness is the NFR-1 surface in this architecture. Verbatim component → location → responsibility the harness depends on:

| Component | Location (spec) | Responsibility | Tag |
|-----------|-----------------|----------------|-----|
| Verdict aggregation contract | `refs/hardening-output-contract.md` + `tests/troubleshoot/test_hardening_verdict.py` | truth table §5.4; reject `waiver_status=latched → pass` | `[UNVERIFIED — greenfield]` |
| Boundary scan schema | `refs/pipeline-hardening-closure.md` + H0 tests | typed boundary rows before applicable=false skip | `[UNVERIFIED]` |
| Contract ledger validator | `refs/contract-enumeration.md` + H2 tests | reject empty ledgers, unclassified consumers, unproven dead/legacy | `[UNVERIFIED]` |
| Classifier fixture harness | `refs/unmask-and-sweep.md` + H3 fixtures | run full artifacts; assert HALT/WARN/CONTINUE by consumer | `[UNVERIFIED]` |
| Effective-input manifest validator | `refs/effective-input-proof.md` + H4 tests | prove selector ∩ runtime surface; exclude foreign/stale | `[UNVERIFIED]` |
| Output-contract compatibility harness | `tests/troubleshoot/test_hardening_output_contract.py` | new fields additive, defaulted/nullable; old consumers still pass | `[UNVERIFIED]` |

**Constraint on the harness (§4.7 line 347, verbatim):** "Test-only helpers may live under `tests/troubleshoot/` if they are purely validators for markdown contracts. **Any reusable runtime logic promoted beyond tests must live under `src/superclaude/`** and be referenced from this section before implementation." → The backtest replay harness, if it carries reusable runtime logic (e.g. a replay driver, a base-commit reverter), must live under `src/superclaude/`, not `tests/`. Pure markdown-contract validators may stay in `tests/troubleshoot/`. `[UNVERIFIED — both dirs greenfield; this is a placement RULE the impl tasklist must honor]`

**Implementation-order placement of the backtest (§4.6 line 331):** the backtest + `make sync-dev`/`make verify-sync` are **step 7 (last)** — "Tests (§8) + make sync-dev + make verify-sync — depends on 6". And the roadmap milestone (§10 line 592) puts it at **M5: "backtest + sync"**. So the harness is explicitly the LAST thing built, after all H0–H5 gates exist (which is consistent with NFR-1 "predicted until built" — you cannot run a real backtest before the gates exist). `[UNVERIFIED — ordering is spec prose]`

---

## §6 — Consolidated Contract Checklist for the Backtest Harness (what the task DoD must enforce)

A merged, de-duplicated set of MUST-satisfy contracts, each tagged:

1. **Replay corpus = exactly E1–E5** per the §3.1 1:1 matrix; use the SPEC's H0–H5 wave numbering (NOT merged-report §10's). `[UNVERIFIED gate / CODE-VERIFIED corpus dirs exist]`
2. **`backtest_status` enum = `{not_run, partial, complete}`**, default `not_run`, type enum, non-null, required:yes. `[UNVERIFIED — greenfield enum]`
3. **Derivation:** all 5 pass→`complete`; 1–4 pass→`partial` **+ list missing escape IDs**; 0/not-run→`not_run`. `[UNVERIFIED]`
4. **Separation invariant:** `backtest_status` is SEPARATE from `pipeline_hardening_verdict`; production-facing signoff stays **`advisory` even when `pipeline_hardening_verdict=pass`** until `backtest_status=complete` (then "may mirror"). `[UNVERIFIED — but triple-stated §4.5/§5.4/§7]`
5. **Missing-field fail-safe:** absent `backtest_status` ⇒ signoff treated as `advisory` (never `complete`). `[UNVERIFIED]`
6. **NFR-1 target = 100% would-have-caught**, "predicted until built"; real `complete` only after gates exist + all 5 replays pass. `[UNVERIFIED]`
7. **Per-escape oracles (§8.3):** E1 H1 FAIL-pre/PASS-post (negative+positive witness); E2 executable HALTs / `incomplete` near-miss does not; E3 FAIL until `K_swept==K_true` + non-exec headings WARN/CONTINUE; E4 H2 FAIL until both `gate_passed`+`_evaluate_gate` (+trailing gate+remediation dispatch) classified; E5 H4 FAIL-closed on wrong surface until `|E ∩ true_runtime_surface|` proven. `[UNVERIFIED gates / CODE-VERIFIED E4 symbols]`
8. **Waiver re-green replay:** waive H1 → downstream cannot upgrade `blocked`/`advisory`→`pass` (NFR-4, one-way latch). `[UNVERIFIED]`
9. **Placement rule (§4.7):** reusable runtime replay logic under `src/superclaude/`; pure markdown-contract validators may live under `tests/troubleshoot/`. `[UNVERIFIED — placement rule]`
10. **Governing tests named by spec:** integration `test_backtest_status_keeps_pipeline_health_advisory_until_complete` (§8.2 line 568); the per-wave H1–H4 unit tests + `test_hardening_verdict.py` (§8.1) the replays exercise. `[UNVERIFIED — none exist]`
11. **⚠ E4 base-commit caveat (CODE-VERIFIED):** the E4 advisory-fatal bug is **already healed on HEAD** via `20693bb8` (both `_evaluate_gate@executor.py:859` and `gate_passed@gates.py:94` honor `advisory`). A literal E4 negative witness must replay against a PRE-`20693bb8` tree, OR E4 must be framed as a ledger-completeness assertion (the §8.3 wording supports the latter). Coordinate with R5 for the exact base commit. `[CODE-VERIFIED]`

---

## Cross-Validation Tally

- `[CODE-VERIFIED]`: E4 substrate symbols (`_evaluate_gate` executor.py:823, advisory branch :859; `gate_passed` gates.py:23, advisory branch :94; `SemanticCheck.advisory` models.py:94); commit ancestry (`b97c9960` unmerged, `20693bb8` on HEAD); E1–E5 escape description dirs exist; `contract_version` name already used by swarm contract.
- `[CODE-CONTRADICTED]` (narrative-only): spec's "E4 fix committed-but-unmerged" — true at authoring (2026-06-10) but the fix landed on HEAD via sibling commit `20693bb8` (2026-06-11). Material for the harness's E4 base-commit choice.
- `[UNVERIFIED — EXPECTED]`: all H0–H5 gate logic, all 8 new output fields, 6 new refs, `tests/troubleshoot/` suite, REPORT.md closure section, the backtest harness itself, and the `backtest_status` enum — all greenfield, consistent with §1.2 "implementation halted pending G1 approval."

---

**Status: Complete**

### Summary
Extracted the four authoritative backtest contracts from the RELEASE-SPEC and cross-validated each against HEAD:
- **CONTRACT A** (§3.1) — the verbatim E1→wave→FR→evidence-card→backtest-scenario 1:1 matrix, with the canonical-wave-numbering trap (use spec H0–H5, not merged-report §10).
- **CONTRACT B** (§4.5/§5.4/§5.5/§6) — `backtest_status` enum `{not_run|partial|complete}`, default `not_run`, non-null/required; derivation (all 5→complete; some→partial+missing IDs; none→not_run); the CRITICAL separation from `pipeline_hardening_verdict` (signoff stays `advisory` even at `verdict=pass` until `complete`); NFR-1 = 100% would-have-caught, "predicted until built".
- **CONTRACT C** (§8.3) — verbatim per-escape FAIL/PASS oracles, each with a precision note so the replay is not theatre.
- **CONTRACT D** (§4.7/§4.6/§10) — the executable-validation architecture + placement rule (reusable runtime logic under `src/superclaude/`) + M5/step-7 ordering (backtest is last).

**Most load-bearing finding:** E4's substrate is the only one backed by real code — `_evaluate_gate` (executor.py:823/859), `gate_passed` (gates.py:23/94), `SemanticCheck.advisory` (models.py:94) all CODE-VERIFIED — but the E4 advisory-fatal divergence is **already healed on HEAD** via commit `20693bb8` (NOT the spec's `b97c9960`, which remains unmerged). The harness must replay E4 against a pre-`20693bb8` tree for a literal negative witness, or frame E4 as the §8.3 ledger-completeness assertion. Everything else (gate logic, fields, refs, tests, harness, enum) is correctly `[UNVERIFIED — greenfield]` per the G1-halt.
