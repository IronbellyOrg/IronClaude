# Invariant Survival Walkthrough — Phase 7 / T07.03

**Task:** T07.03 — Traceability gap check & invariant-survival walkthrough
**Roadmap Item:** R-026
**Tier:** STRICT
**Generated:** 2026-05-15
**Status:** Deliverable artifact #2 of T07.03 (companion: `traceability-gap-report.md`).

---

## 0. Purpose & method

This artifact constructs a **worked example** of an MDTM task file executing under the *merged* `/task` surface — i.e., `[src] src/superclaude/skills/task/SKILL.md` with every Phase 6 absorption row (CR-TASK-01..10 + CR-FM-01..04) applied — and demonstrates at each step that the five load-bearing invariants **INV-01..INV-05** (see `extension-point-contracts.md` § "Invariant Reference") still hold.

**Method:**

1. Pick a representative MDTM file that exercises all five invariants. The example below is a **STRICT** task with multiple phases, a parallel-spawn batch, an inline `Tier:` per-item override, a test-failure blocker (TFEP-engaging), and a session-restart mid-run (INV-04 stress).
2. Step through the merged `/task` surface execution in order: validation → first-item protocol → F1 loop → phase-gate QA → post-completion validation.
3. At each step, name the absorbed feature(s) interacting with the invariant surface and demonstrate (not just assert) that the invariant holds.
4. Demonstration evidence: the SKILL.md `file:line` anchor where the merged behavior lives, the resulting on-disk state, and a counter-factual (what would break the invariant, with a citation to the manifest exception or ledger entry that REJECTed that variant).

**Invariant labels** (from `extension-point-contracts.md:11-17`):

- **INV-01** F1 loop semantics — READ → IDENTIFY → EXECUTE → UPDATE → REPEAT. No skipping, reordering, or out-of-band substitution.
- **INV-02** Prohibited-actions catalog (F2) — no working from memory, no modifying items mid-execution, no delegating the F1 loop itself.
- **INV-03** Phase-gate `rf-qa` between phases (Phase 2+); post-completion `rf-qa` + `rf-qa-qualitative` validation.
- **INV-04** Resumability — progress recoverable from disk after context compression / session restart.
- **INV-05** Refusal-of-definition — `/task` does not decide *what* to do; the MDTM file does. The F1 loop only *executes*.

---

## 1. The worked example — `TASK-EXAMPLE-20260515-strict-walkthrough.md`

A constructed (representative, not on disk) STRICT MDTM file. It is fabricated for this walkthrough; the merged behaviors below are real on the post-Phase-7 surface.

```yaml
---
id: TASK-EXAMPLE-20260515-strict-walkthrough
title: Implement auth-token rotation in src/auth/
status: 🟡 To Do
created_date: 2026-05-15
updated_date: 2026-05-15
Tier: STRICT
---

## Task Overview
Rotate the legacy JWT issuance path in `src/auth/issuer.py` to use the new key-store interface. Update tests, document the migration.

## Key Objectives
- Replace `legacy_sign()` calls with `keystore.sign()`.
- Add migration test demonstrating zero-downtime cutover.
- Document in `docs/auth/key-rotation.md`.

## Variables
- `KEYSTORE_ADDR`: `https://keystore.internal/v1`
- `LEGACY_HMAC_KEY_ID`: `hmac-2025-09`

## Phase 1 — Investigation
- [ ] Step 1.1 — Update frontmatter: set `status: "🟠 Doing"`, `start_date: 2026-05-15`, `updated_date: 2026-05-15`. Make no other changes to the task file.
- [ ] Step 1.2 — Use `mcp__auggie__codebase-retrieval` (directory_path `/config/workspace/IronClaude`) to enumerate every call site of `legacy_sign()` and write the inventory to `research/legacy-sign-callsites.md`, ensuring the inventory cites file:line for every match.
- [ ] Step 1.3 — Spawn the `security-engineer` subagent (mode `bypassPermissions`, prompt body verbatim below) to assess the cryptographic-boundary implications of cutover, ensuring the output file `research/security-assessment.md` exists and names every threat in numbered form.
- [ ] Step 1.4 — Spawn the `backend-architect` subagent (mode `bypassPermissions`, prompt body verbatim below) in parallel with Step 1.3 (independent, same phase) to propose the migration shim shape, ensuring `research/migration-shim-design.md` exists.

## Phase 2 — Implementation
- [ ] Step 2.1 — (Tier: LIGHT) Update the docstring header in `src/auth/issuer.py` to reflect the new keystore interface, ensuring the docstring matches the keystore.sign() signature.
- [ ] Step 2.2 — Replace `legacy_sign()` calls in `src/auth/issuer.py` with `keystore.sign()`, ensuring `uv run pytest tests/auth/` exits 0 or all failures are TFEP-classified pre-existing.
- [ ] Step 2.3 — Add `tests/auth/test_keystore_rotation.py` exercising zero-downtime cutover, ensuring the new test passes when run in isolation.

## Phase 3 — Documentation
- [ ] Step 3.1 — Author `docs/auth/key-rotation.md` describing the migration, ensuring the document includes the rollback procedure.
- [ ] Step 3.2 — Update frontmatter: `status: "🟢 Done"`, `completion_date: 2026-05-15`.

## Task Log / Notes
(empty until execution)
```

Key example properties exercised:

- **STRICT tier**: triggers TU-1 STRICT profile (Gate 1), TU-4 pre-flight (D15b), TU-5 baseline (TFEP D21), TU-3 widened Gate 2 (`rf-qa` + `quality-engineer`).
- **`auth/` path-glob**: triggers TU-2 critical-path override → forces STRICT even if the frontmatter said LIGHT.
- **Per-item LIGHT override** at Step 2.1 (`(Tier: LIGHT)`): exercises CR-TASK-03 (per-item annotation read) under ME-1 (PRE-LOOP DISPATCH ONLY — the loop profile is *not* re-dispatched; only the per-item budget/roster narrows).
- **Parallel-spawn batch** at Steps 1.3 + 1.4: exercises Critical Rule 8 / the existing parallel-spawn extension point (row 7).
- **Phase boundary** between Phase 1 → 2 → 3: exercises INV-03 (phase-gate `rf-qa` runs twice).
- **Phase 2 test-failure path** at Step 2.2: exercises TU-6 (TFEP prohibitions + carve-outs) + TU-7 (escalation classification against the TU-5 baseline) + TU-8 (incident report at Post-Completion if escalation fired and resolved).
- **Mid-run session restart** between Step 1.3 returning and the loop re-reading: exercises INV-04 (resumability) with the new `Tier:` field and the new `research/test-baseline.yaml` and `research/tfep-incident-report.md` side-effect files.

---

## 2. Step-by-step run through the merged `/task` surface

### 2.0 Task entry — pre-loop validation block (CR-TASK-01 + CR-TASK-02 + CR-FM-01..04)

**Surface:** `[src] src/superclaude/skills/task/SKILL.md` rows 64–73 (Task File Validation gate), with the merged additions:

- CR-TASK-01: `path_override_check` fires FIRST (CR-7 ordering).
- CR-TASK-02: closed-enum `Tier:` validator; then Gate 1 dispatch (PRE-LOOP).
- CR-FM-01..04: schema rules consumed by the validator.

**Sequence at the row 1 surface (per CR-7):**

1. `path_override_check(task_target_paths=[src/auth/issuer.py, tests/auth/test_keystore_rotation.py, docs/auth/key-rotation.md])`:
   - `src/auth/issuer.py` matches critical-path glob `auth/` (sourced from `[src] src/superclaude/skills/sc-task-protocol/SKILL.md:121` per CR-TASK-01 row, inlined into the merged surface).
   - Returns `forced_stance=STRICT (matched: auth/)`.
   - **Task Log line written (R-RULE-10-safe, side-channel):** `path-override: forced_stance=STRICT (matched: auth/)`.
2. `tier_field_validate(Tier: "STRICT")`:
   - Closed-enum check: `STRICT ∈ {STRICT, STANDARD, LIGHT, EXEMPT}` → pass.
3. `gate_1_dispatch(forced_stance=STRICT, tier_value=STRICT)`:
   - STRICT profile chosen. Single Task Log line written: `gate-1: dispatch_profile=STRICT source=path-override` (path-override wins precedence — the worked example happens to have both align, but the precedence is unambiguous).

**Invariants demonstrated:**

- **INV-01 (F1 loop semantics):** validation + dispatch run **pre-loop**. The first F1 iteration has not started yet. ME-1 (PRE-LOOP DISPATCH ONLY) explicitly forbids re-entering this block per-item, so the loop's READ → IDENTIFY → EXECUTE → UPDATE → REPEAT is untouched. **Counter-factual:** if Gate 1 dispatched *per-item*, every iteration would re-evaluate `path_override_check` and `tier_field_validate`, re-entering loop control flow — auto-REJECT under ME-1. The manifest blocks this variant.
- **INV-05 (refusal-of-definition):** the validator reads schema fields (`Tier:`, frontmatter) but does **not** decide what work to do — the checklist body is untouched. **Counter-factual:** if the validator synthesized missing items from the frontmatter (e.g., consumed a `tasks: [...]` array), it would be defining work — REJECTed at extension-point row 13 (`SKILL.md:169-175`) per the "Required fields whose values define the work" admit-reject for INV-05.

---

### 2.1 First Item Protocol — pre-flight scaffolding (CR-TASK-06) + baseline (CR-TASK-07)

**Surface:** `[src] src/superclaude/skills/task/SKILL.md:100-102` (First Item Protocol).

**Sequence (STRICT profile dispatched at step 2.0, so both run):**

1. **CR-TASK-06 — Pre-flight scaffolding (TU-4 / D15b):**
   - `serena_activate_if_available()` → if MCP available, activate project; else gracefully skip.
   - `git_status_clean_tree_check()` → fast read.
   - `codebase_retrieval_on_relevant_code_if_available()` → primes auggie MCP cache for `src/auth/`.
   - `list_memories_read_memory_for_relevant_prior_context()`.
   - **Task Log line:** `gate-1.5: pre-flight tier=STRICT ran=[serena, git, codebase-retrieval, memory]`.
2. **CR-TASK-07 — TFEP baseline snapshot (TU-5 / D21):**
   - `uv run pytest --collect-only -q` collects test IDs.
   - `uv run pytest --tb=no -q` captures PASS/FAIL state for each ID.
   - Persists `research/test-baseline.yaml` (YAML list `[{test_id, status}, …]`).
   - **Side-effect file written:** `${TASK_DIR}/research/test-baseline.yaml`.
3. **Existing first-item protocol step** — the loop is about to enter; F1 has not started.

**Invariants demonstrated:**

- **INV-01 (F1 loop semantics):** CR-TASK-06 and CR-TASK-07 are **additive pre-loop setup** per ME-5 (NO PER-ITEM EXECUTE SUBSTITUTION). They do not synthesize checklist items, do not consume the first `- [ ]`, and do not execute inside the loop. The loop will start at Step 1.1 (the existing status-update item) — unchanged. **Counter-factual:** D15c (per-tier procedure synthesis at execute-time) WAS REJECTed (LR-REJECT-7) precisely because it would generate runtime checklist items the loop did not READ from disk — collision with INV-01 + INV-05. The manifest blocks this variant; CR-TASK-06 absorbs only the D15b half.
- **INV-04 (resumability):** the baseline file lives on disk at `${TASK_DIR}/research/test-baseline.yaml` (TU-5 observable post-condition). On any later session restart, the file is re-readable; the comparator behavior for TU-7 has a disk anchor. **Counter-factual:** an in-memory baseline cache would be lost on context compression — TU-5's tier-gated *file-resident* choice is the INV-04-safe variant the manifest selected.
- **INV-05 (refusal-of-definition):** pre-flight steps are environment setup; they do not consume a checklist item or decide what the loop will execute. The MDTM file is still the definition of work.

---

### 2.2 F1 Loop — Phase 1 sequential items (Step 1.1 → 1.2)

**Surface:** `[src] src/superclaude/skills/task/SKILL.md:79-98` (F1 EXECUTE).

**Iteration 1 — Step 1.1 (frontmatter update):**

1. **READ:** the merged `/task` re-reads `TASK-EXAMPLE-20260515-strict-walkthrough.md` from disk.
2. **IDENTIFY:** first unchecked `- [ ]` is Step 1.1.
3. **EXECUTE:** `/task` edits the task file's frontmatter — sets `status: "🟠 Doing"`, `start_date: 2026-05-15`, `updated_date: 2026-05-15`. This is the F5 frontmatter-update protocol (`SKILL.md:159-168`).
4. **UPDATE:** mark Step 1.1 as `- [x]` on disk. Append Phase Findings line: `Step 1.1 complete; status flipped to 🟠 Doing`.
5. **REPEAT:** return to READ.

**Iteration 2 — Step 1.2 (auggie codebase enumeration):**

1. **READ:** re-read the task file. Step 1.1 is now `- [x]`; Step 1.2 is the first unchecked.
2. **IDENTIFY:** Step 1.2.
3. **EXECUTE:** call `mcp__auggie__codebase-retrieval` with the item's verbatim parameters; write `research/legacy-sign-callsites.md`. Per the "ensuring…" clause hook (`SKILL.md:96`), verify the file cites `file:line` for every match.
4. **UPDATE:** mark Step 1.2 `- [x]`. Append Phase Findings with the call-site count.
5. **REPEAT.**

**Invariants demonstrated:**

- **INV-01 (F1 loop):** every iteration is READ → IDENTIFY → EXECUTE → UPDATE → REPEAT, in exact order. The merged Gate 1 (step 2.0) and pre-flight (step 2.1) ran BEFORE the loop, so they do not interfere. The merged per-item `Tier:` annotation read (CR-TASK-03) is silent on these items (no inline `(Tier: ...)` marker), so the default behavior is the STRICT profile chosen at Gate 1.
- **INV-02 (prohibited actions):** Step 1.1 is a frontmatter update — explicitly admitted by F4 (`SKILL.md:144-158`). Step 1.2 spawns a tool, writes a file, marks complete only after disk evidence (the new `.md` file) exists.
- **INV-04 (resumability):** every UPDATE is incremental (`SKILL.md:252-264` — Incremental Writing Protocol). If the session ends after Step 1.2's UPDATE, the next session's READ sees Step 1.1 + 1.2 as `- [x]` and resumes at Step 1.3.
- **INV-05:** the loop did not synthesize, rewrite, or reinterpret the items. Step 1.2 ran exactly as written.

---

### 2.3 F1 Loop — Phase 1 parallel batch (Step 1.3 + 1.4)

**Surface:** `[src] src/superclaude/skills/task/SKILL.md:119-142` (Parallel Agent Spawning).

**Iteration 3 — parallel batch:**

1. **READ:** re-read the task file. Step 1.3 is the first unchecked.
2. **IDENTIFY (batch detection):** scan forward from Step 1.3; Step 1.4 is an independent subagent spawn in the same phase (Phase 1) with no inter-item output dependency. Both are added to the batch.
3. **EXECUTE:** spawn `security-engineer` and `backend-architect` agents in a single response (one tool-call message containing two Agent tool uses, per Critical Rule 8 / the parallel-spawn extension point).
4. **UPDATE:** as each agent returns, mark its corresponding item `- [x]` immediately. Do not wait for both to finish before checking one off.
5. **REPEAT (after batch):** re-read the task file before proceeding to the next phase (the row-7 admit criterion "re-read after batch").

**Mid-batch session-restart simulation (INV-04 stress):**

Suppose the `security-engineer` agent returns first; the loop marks Step 1.3 `- [x]` on disk. The session then terminates (context compaction or user kill). On restart:

1. The merged `/task` validates the file (CR-TASK-01 + CR-TASK-02 + CR-FM-01..04 — same as step 2.0). `path-override: forced_stance=STRICT` and `gate-1: dispatch_profile=STRICT source=path-override` lines already exist in the Task Log; the resume code (`SKILL.md:268-283`) does NOT re-emit them (it inspects disk state and resumes).
2. Pre-flight (step 2.1): the resume code observes `research/test-baseline.yaml` exists on disk — TU-5 baseline is already captured; do not recapture (file-resident anchor honors INV-04).
3. F1 re-enters: READ; IDENTIFY first unchecked = Step 1.4; spawn only `backend-architect` (the other batch slot); when it returns, mark Step 1.4 `- [x]`. Step 1.3's output file (`research/security-assessment.md`) already exists on disk — do not re-spawn `security-engineer`.

**Invariants demonstrated:**

- **INV-01:** the loop never delegated *itself*; it dispatched two single-item subagents. The "ensuring…" clauses are verified against the output files post-batch. Critical Rule 12 (`SKILL.md:115`) — "no delegating the F1 loop itself" — holds.
- **INV-02:** parallel-spawn is the explicitly carved-out exception in F2 (`SKILL.md:109`); it is not a violation. Items are marked `- [x]` only after their agent's output file exists (no assuming completion).
- **INV-04 (resumability under restart):** the disk state (`Step 1.3` checked, `Step 1.4` unchecked, `research/security-assessment.md` present, `research/test-baseline.yaml` present, `path-override` + `gate-1` lines in Task Log) is sufficient to reconstruct everything the merged `/task` decided pre-loop. The new CR-FM-03 backward-compat default (`STANDARD`) does NOT apply here (this file declares `Tier: STRICT`), but if a future restart hit an older file without `Tier:`, the validator emits `gate-1: dispatch_profile=STANDARD source=default` and resumes — no break.
- **INV-05:** the loop honored the batch as written in the file; it did not regroup items, did not split a single batch into multiple iterations, did not skip the `ensuring…` clause.

---

### 2.4 Phase boundary — Phase 1 → Phase 2 — phase-gate `rf-qa` with widened roster (CR-TASK-04 + CR-TASK-05)

**Surface:** `[src] src/superclaude/skills/task/SKILL.md:182-211` (Phase-Gate QA Verification).

**Sequence at the row 10 surface (per CR-8):**

1. **CR-TASK-04:** `path_override_check` consumed FIRST. `forced_stance=STRICT` (from step 2.0; carried via the task-log line which the gate re-reads) — STRICT profile applies.
2. **CR-TASK-05 (TU-3 widening):** the Phase-Gate QA block now reads:
   - `verifier_roster: [rf-qa, quality-engineer]` (STRICT — `quality-engineer` added per ME-2).
   - `budget: ~5K tokens, 60s timeout`.
3. **Adversarial-stance `rf-qa` runs** (INV-03 floor — *always*, regardless of tier). It reads `research/legacy-sign-callsites.md`, `research/security-assessment.md`, `research/migration-shim-design.md`, extracts "ensuring…" clauses as acceptance criteria, produces `reviews/qa-phase-1-report.md`. Verdict: PASS.
4. **`quality-engineer` runs in parallel** as the supplementary STRICT-tier verifier. It produces its own report at `reviews/qa-phase-1-quality-engineer-report.md`. Verdict: PASS.
5. **Task Log line:** `gate-2: profile=STRICT budget=5K/60s roster=[rf-qa, quality-engineer]`.

**Invariants demonstrated:**

- **INV-03 (phase-gate `rf-qa`):** `rf-qa` runs with adversarial stance and produces the report on disk before Phase 2 begins. The roster widening (CR-TASK-05) **adds** `quality-engineer` but does NOT replace `rf-qa` (ME-2 — `rf-qa` SUPPLEMENTED NOT REPLACED). **Counter-factual:** the donor's verifier-replacement variant (D15a's per-tier verifier rewriting) was REJECTed by ME-2 / extension-point row 10 admit-reject rule ("Gates that downgrade adversarial stance to 'summarize what was done'"). The manifest blocks the replacement variant.
- **INV-04 (resumability):** both report files exist on disk before Phase 2 starts. Session restart between Phase 1's last item and Phase 2's first item re-reads the report files and confirms PASS — no re-run.
- **INV-01:** the gate is between phases, not inside the loop; Critical Rule 11 (`SKILL.md:116` — "Skipping phase-gate QA" prohibition) is satisfied.

---

### 2.5 F1 Loop — Phase 2 with inline-tier override (Step 2.1, `(Tier: LIGHT)`) — CR-TASK-03 + CR-FM-02

**Surface:** `[src] src/superclaude/skills/task/SKILL.md:79-98` (F1 EXECUTE), CR-TASK-03 inline-marker read.

**Iteration 4 — Step 2.1 (LIGHT-marked docstring fix):**

1. **READ:** task file. Step 2.1 is the first unchecked.
2. **IDENTIFY:** Step 2.1 with inline marker `(Tier: LIGHT)`.
3. **EXECUTE (with CR-TASK-03 read):**
   - The CR-TASK-03 hook reads the inline `(Tier: LIGHT)` marker per CR-FM-02 grammar.
   - Per ME-1, the **loop profile** stays STRICT (decided pre-loop at Gate 1 — not re-evaluated). The inline marker is a per-item *budget hint* only: it does NOT re-dispatch the profile, does NOT skip the phase-gate QA after this item, does NOT skip post-completion validation. What it MAY do (per CR-TASK-05 row, item budget surface): allow the phase-gate QA for this single trivial item to use a reduced budget IF the phase-gate ran per-item — but the gate is per-PHASE, not per-item, so this hint is in practice silent at Phase 2's gate (the phase's overall STRICT profile still applies).
   - Edit `src/auth/issuer.py`'s docstring header.
4. **UPDATE:** mark Step 2.1 `- [x]`. Append Phase Findings.
5. **REPEAT.**

**Invariants demonstrated:**

- **INV-01:** the loop ran one item, one read, one update. Per-item `Tier:` annotation did NOT re-trigger Gate 1 dispatch. **Counter-factual:** per-item per-tier dispatch is auto-REJECT under ME-1 / CR-10 (`stack-rank.md:239`) precisely because it re-evaluates loop control each iteration. The merged surface absorbs the *read* (CR-TASK-03 + CR-FM-02) without absorbing the *dispatch* — exactly the manifest's exception-bound shape.
- **INV-05:** the inline marker is data; the work itself is defined by Step 2.1's body. The loop did not reinterpret the item.

---

### 2.6 F1 Loop — Phase 2 with test-failure blocker (Step 2.2) — TFEP cluster fires (CR-TASK-08 + CR-TASK-09 + CR-TASK-10)

**Surface:** `[src] src/superclaude/skills/task/SKILL.md:170-179` (Error Handling); Post-Completion uses `:213-248`.

**Iteration 5 — Step 2.2 (`legacy_sign` → `keystore.sign` replacement):**

1. **READ, IDENTIFY:** Step 2.2.
2. **EXECUTE:** edit `src/auth/issuer.py`; run `uv run pytest tests/auth/`. Three failures observed:
   - `tests/auth/test_legacy_clock_skew.py::test_clock_skew_grace` — FAIL.
   - `tests/auth/test_keystore_integration.py::test_keystore_handshake` — FAIL.
   - `tests/auth/test_issuer.py::test_keystore_signature_round_trip` — FAIL.
3. **CR-TASK-08 (TU-6) — TFEP prohibition + carve-out checks fire (side-channel, no F1 halt):**
   - `tfep_prohibition_check(blocker_type=test_failure)`:
     - VIOLATION-1 (ad-hoc-fix without RC) — refuse if `/task` is about to "tweak until green."
     - VIOLATION-2 (modify test expectations without adversarial validation) — refuse if `/task` is about to edit `tests/`.
     - VIOLATION-3 (one-shot patch from test output alone) — refuse if `/task` did not look at production code.
   - For Step 2.2 (which is a *production code* edit, not a test edit), no prohibition fires — but if `/task` instinctively had attempted to silence the tests, the prohibition surface would have refused.
   - `tfep_carve_out_check(failure_class)`:
     - Carve-out 1 (`ImportError`/`NameError` in test scaffolding, ≤2 tests): not applicable (failures are integration, not scaffolding).
     - Carve-out 2 (lint/formatting): not applicable.
     - Carve-out 3 (deprecation warnings): not applicable.
4. **CR-TASK-09 (TU-7) — TFEP escalation classification:**
   - Read `research/test-baseline.yaml`. Findings:
     - `test_clock_skew_grace` was PASSING in baseline → now FAIL → **pre-existing-now-broken** = MUST-escalate trigger #1.
     - `test_keystore_handshake` is new (not in baseline) → **new** = neutral.
     - `test_keystore_signature_round_trip` is new → **new** = neutral.
   - Count of new failures: 2. Trigger #2 (≥3 new tests fail) — NOT fired.
   - Trigger #3 (runtime exception in implementation code) — not fired.
   - **Trigger #1 fires (regression).** Route to `rf-qa` for adjudication (existing INV-03 surface — Phase-Gate QA's 3-cycle loop, per LR-REJECT-2 rationale).
   - **Task Log:** `tfep: escalation-trigger fired=1 tests=[test_clock_skew_grace] classification=pre-existing-now-broken`.
5. `rf-qa` adjudicates (within Phase-Gate QA's 3-cycle loop). Verdict: legacy_sign path uses a HMAC-grace window that keystore.sign doesn't; `/task` fixes the grace-window handling in `src/auth/issuer.py`. Re-run pytest: all green except the two new tests (which were planned in Step 2.3).
6. **UPDATE:** mark Step 2.2 `- [x]` (production code now correct; the two new tests' fix is Step 2.3's job).
7. **REPEAT.**

**Invariants demonstrated:**

- **INV-01:** the TFEP cluster fired entirely **side-channel** (ME-3 — SIDE-CHANNEL ONLY, NO F1 HALT). The failing item flips to `- [x]` via existing blocker logging or via successful resolution (here, successful resolution); the F1 loop continues to Step 2.3. **Counter-factual:** halting F1 on TFEP engagement is auto-REJECT under ME-3 / CR-12. The donor's F1-halting variant is blocked.
- **INV-02:** prohibitions explicitly forbid the F2 anti-patterns (`SKILL.md:108-117`) — "Working from memory" is mirrored by "ad-hoc-fix without root cause"; "Modifying items" is mirrored by "modify test expectations to make a failure go away." The TFEP surface reinforces F2 at the same extension point (row 8).
- **INV-03:** TU-7 explicitly routes to `rf-qa` rather than authoring a parallel adjudicator (D25's "3-strike FULL STOP" budget is REJECTed — LR-REJECT-2). The existing Phase-Gate QA 3-cycle loop is the only QA mechanism.
- **INV-04:** `research/test-baseline.yaml` is the disk anchor that made the pre-existing-vs-new classification possible. If the loop had relied on in-memory baseline state and a session restart happened between Step 1.* and Step 2.2, the classification would still be deterministic because the file exists.

---

### 2.7 Phase 2 → 3 phase-gate (CR-TASK-04 + CR-TASK-05 again)

Same shape as step 2.4. Same widened roster (`rf-qa, quality-engineer`). Reports persist to `reviews/qa-phase-2-report.md` + `reviews/qa-phase-2-quality-engineer-report.md`. INV-03 holds.

---

### 2.8 F1 Loop — Phase 3 (Step 3.1 + 3.2)

Two sequential items: doc authoring + final frontmatter flip. Both run under the standard loop; no TFEP triggers (no test failures). Step 3.2 is the F5 frontmatter terminal update (`status: "🟢 Done"`, `completion_date: 2026-05-15`).

**At Step 3.2's UPDATE,** the loop has reached the final phase's final item — but the loop does NOT mark the task "🟢 Done" via Step 3.2 directly until Post-Completion Validation runs (per `SKILL.md:117` — "Skipping post-completion validation" is a prohibited action). Step 3.2's mechanical frontmatter edit happens, but `/task` then enters Post-Completion Validation before issuing the "task is now Done" final report.

---

### 2.9 Post-Completion Validation (CR-TASK-10 + existing `rf-qa-qualitative`)

**Surface:** `[src] src/superclaude/skills/task/SKILL.md:213-248` (Post-Completion Validation).

**Sequence:**

1. **Existing structural `rf-qa` pass** runs over every output file (all `research/*.md` + `reviews/*.md` + the source edits in `src/auth/issuer.py` + the new tests + the doc).
2. **Existing `rf-qa-qualitative` pass** runs with zero-leniency operational checklist (`SKILL.md:248`).
3. **CR-TASK-10 (TU-8 / D24) — TFEP incident-report check:**
   - This task is STRICT and had a TFEP escalation fire at Step 2.2.
   - Check for `${TASK_DIR}/research/tfep-incident-report.md`. Per TU-8's contract, the loop must have written this file at TFEP-resolve time (Step 2.2's adjudication).
   - The file exists. The seven-field schema is read and verified:
     - Trigger: `escalation-trigger #1 (pre-existing-now-broken)`.
     - Escalation count: `1`.
     - Failing tests: `[test_clock_skew_grace]`.
     - Root cause: `HMAC-grace-window timing-window incompatibility between legacy_sign and keystore.sign in src/auth/issuer.py:178-194`.
     - Solution: `Apply the grace-window adapter in keystore_signer; explicit comment at line 191 cites the migration`.
     - Outcome: `resolved`.
     - Forensic artifacts: `[reviews/qa-phase-2-report.md, research/test-baseline.yaml]`.
   - All seven fields populated → CR-TASK-10 PASS.
4. **All three validators PASS** → `/task` finalizes "🟢 Done" status (Step 3.2's frontmatter flip is now confirmed).

**Invariants demonstrated:**

- **INV-03 (post-completion):** both `rf-qa` and `rf-qa-qualitative` ran. CR-TASK-10 is an *additive* validator (per the extension-point row 11 admit "Additive analyzers"); it did NOT replace either of the existing two (which would violate INV-03). **Counter-factual:** replacing `rf-qa-qualitative` with a lighter-weight validator is REJECTed at extension-point row 11 reject rules; the manifest does not author that variant.
- **INV-04:** all reports + the incident report file persist on disk. A future task that needs to cite this task's outcome reads the files directly.
- **INV-05:** post-completion validation reports outcome but does not redefine the task — the MDTM file's `Key Objectives` section is the original definition.

---

## 3. Cross-cutting invariant summary

This section summarizes, per invariant, every absorbed feature that interacts with that invariant surface and the demonstration that the invariant still holds (per T07.03 AC #4).

### INV-01 — F1 loop semantics

| Absorbed feature | Interaction | Demonstration that INV-01 holds |
|---|---|---|
| TU-1 (Gate 1 dispatch, CR-TASK-02) | Pre-loop block — fires once at task entry | ME-1 binds: per-item per-tier dispatch is auto-REJECT. Counter-factual (re-dispatching inside the loop) is blocked by the manifest exception. Step 2.0 in this walkthrough fires before the first F1 iteration. |
| TU-1 (per-item `Tier:` read, CR-TASK-03) | Inside F1 EXECUTE | The read is a budget hint, not a dispatch trigger. The loop's profile decided at Gate 1 is not re-evaluated. Step 2.5 in this walkthrough shows `(Tier: LIGHT)` on Step 2.1 does not narrow the loop profile. |
| TU-2 (path-override at row 1 + row 10, CR-TASK-01 + CR-TASK-04) | Pre-loop and at the phase-gate | CR-7 / CR-8 ordering: override fires FIRST, then validator/dispatch. No mid-loop side-effect. |
| TU-4 (pre-flight scaffolding, CR-TASK-06) | First Item Protocol — pre-loop | ME-5 binds: additive pre-loop setup only; D15c's execute-time procedure synthesis (which would generate runtime items) is REJECTed. Step 2.1 shows the steps run before the loop. |
| TU-5 (baseline snapshot, CR-TASK-07) | First Item Protocol — pre-loop | Pre-loop file-system action; does not enter EXECUTE. Step 2.1. |
| TU-6 / TU-7 / TU-8 (TFEP cluster) | Side-channel at Error Handling + Post-Completion | ME-3 binds: NO F1 HALT. The failing item flips to `- [x]` (resolved or via blocker logging); loop continues. Step 2.6 demonstrates resolution-without-halt. |

**Verdict: INV-01 SURVIVES.**

### INV-02 — Prohibited actions catalog (F2)

| Absorbed feature | Interaction | Demonstration that INV-02 holds |
|---|---|---|
| TU-6 (TFEP prohibitions, CR-TASK-08) | Error Handling — *reinforces* F2 | Three VIOLATION rules mirror existing F2 prohibitions ("ad-hoc-fix without RC" ≈ "Working from memory"; "modify test expectations to silence" ≈ "Modifying items"). TU-6 strengthens F2; it does not weaken any F2 entry. Step 2.6. |
| Subagent dispatcher entries (rows 15–19, no change in this sprint) | F2 N3 — non-delegable loop | The merged surface does not author a loop-driver subagent type. Parallel batch in step 2.3 spawns single-item subagents within one phase; Critical Rule 12 holds. |
| All other absorbed features | Do not touch F2 (constraint surface — extension-point N1 admits nothing) | C1 auto-REJECT rule (R-RULE-05) means no merged feature can relax F2. |

**Verdict: INV-02 SURVIVES.**

### INV-03 — Phase-gate `rf-qa` + post-completion validation

| Absorbed feature | Interaction | Demonstration that INV-03 holds |
|---|---|---|
| TU-3 (Phase-Gate QA widening, CR-TASK-05) | Row 10 — verifier roster widening | ME-2 binds: `rf-qa` SUPPLEMENTED NOT REPLACED. `quality-engineer` is *additional* on STRICT; never substitutes. Step 2.4 shows both reports persist. |
| TU-2 (path-override at row 10, CR-TASK-04) | Row 10 — pre-gate stance decision | Overrides only the *stance* (STRICT/LIGHT) — does not bypass the gate. Step 2.4 shows the gate runs with the override-determined profile. |
| TU-7 (escalation, CR-TASK-09) | Routes test-failure escalations to `rf-qa` | Routes to the existing INV-03 surface; D25's parallel 3-strike adjudicator is REJECTed (LR-REJECT-2). Step 2.6. |
| TU-8 (incident report check, CR-TASK-10) | Row 11 — Post-Completion *additive* | Row 11 admit "Additive analyzers"; does not replace `rf-qa-qualitative`. Step 2.9. |

**Verdict: INV-03 SURVIVES.**

### INV-04 — Resumability

| Absorbed feature | Interaction | Demonstration that INV-04 holds |
|---|---|---|
| CR-FM-03 (backward-compat default `STANDARD`) | Required-frontmatter validator | Existing TASK-* files without `Tier:` validate clean and dispatch `STANDARD`. HZ-01 in `compat-hazard-report.md` is mitigated. |
| TU-5 (baseline file, CR-TASK-07) | Disk-resident comparator | `research/test-baseline.yaml` is the file anchor for TU-7. Session restart between baseline write and Step 2.2 still allows TU-7 to classify failures. Step 2.3 simulates this. |
| TU-8 (incident-report file, CR-TASK-10) | Disk-resident validator input | `research/tfep-incident-report.md` is the disk anchor for Post-Completion. Step 2.9. |
| TU-1 task-log lines (path-override, gate-1, gate-1.5, gate-2) | Append-only Task Log | Resume code re-reads the lines; no re-emission. INV-04 holds because every dispatch decision is also persisted. |
| Existing F1 `- [x]` durability | Untouched by merge | Step 2.3's mid-batch restart shows the partial batch resumes correctly. |

**Verdict: INV-04 SURVIVES.**

### INV-05 — Refusal-of-definition

| Absorbed feature | Interaction | Demonstration that INV-05 holds |
|---|---|---|
| TU-1 `Tier:` field (CR-FM-01..04) | Frontmatter metadata, not work definition | Extension-point row 13 reject rule: "Required fields whose values define the work" — REJECTed. `Tier:` is dispatch metadata; work is still in the checklist. Step 2.0. |
| TU-1 Gate 1 dispatch (CR-TASK-02) | Pre-loop branching | Dispatch chooses a *profile* (budget, roster, pre-flight enablement). It does not synthesize, reorder, or skip items. Step 2.0. |
| TU-4 pre-flight (CR-TASK-06) | Pre-loop environment setup | Does not consume an item, does not generate runtime items (D15c REJECTed). Step 2.1. |
| TU-6 / TU-7 / TU-8 TFEP cluster | Side-channel verification | Does not decide what work `/task` does next; only audits failures already produced by the loop. Step 2.6 + 2.9. |
| D09b classifier (donor's runtime classifier inside `/task`) | NOT MERGED (LR-REJECT-3) | The merged surface does not author a runtime classifier. `Tier:` arrives declaratively from the task file (author-tagged). Step 2.0 shows CR-TASK-02 *reads* the field; it does not classify the task. |
| D08 classification header emission (LR-DEFER-5 / ME-7) | NOT MERGED | No CR-NN row implements header emission; the deferred precondition (parser ships) remains terminal. |

**Verdict: INV-05 SURVIVES.**

---

## 4. Counter-factual register — what would have broken an invariant

Each row below names a donor variant that *would* have broken an invariant, and cites the manifest exception (ME-NN) or ledger entry (LR-REJECT-NN / LR-DEFER-NN) that blocked it. T07.03 AC #3 demands the walkthrough *demonstrate*, not just assert, invariant survival; this register names the alternative shapes the manifest explicitly rejected.

| INV | Donor variant that would have broken it | Block source |
|---|---|---|
| INV-01 | Per-item per-tier dispatch (Gate 1 fires inside F1 EXECUTE) | ME-1 / CR-10 |
| INV-01 | D15c per-tier procedure synthesis at execute-time (generates runtime checklist items) | LR-REJECT-7 / ME-5 |
| INV-01 | TFEP F1-halting behavior on engagement | ME-3 / CR-12 |
| INV-01 | D04 Strategy axis (multi-axis routing inside the loop) | LR-REJECT-9 (Stack-rank Row 28) |
| INV-02 | Persona auto-activation that injects role text mid-loop | LR-REJECT-5 (D03, Row 24) |
| INV-02 | Tool Coordination layer that duplicates F1 EXECUTE | LR-REJECT-16 (D28, Row 38) |
| INV-03 | Verifier replacement on STRICT (`quality-engineer` REPLACES `rf-qa`) | ME-2 / CR-11 |
| INV-03 | D25 3-strike FULL STOP budget (parallel adjudicator) | LR-REJECT-2 (D25, Row 20) |
| INV-03 | Gate 5 override flags that let users bypass the gate | LR-REJECT-4 (Row 22) |
| INV-04 | In-memory baseline cache (no file write) | TU-5's file-resident shape is the chosen variant; in-memory variant was not authored |
| INV-04 | D23 Step 6 — "resume from inserted task" (IDENTIFY reads items the loop didn't author) | LR-DEFER-6 / TU-8's REJECTion of D23 Step 5+6 at the attach surface |
| INV-05 | D09b runtime classifier (decides Tier from task body) | LR-REJECT-3 (D09b, Row 21) |
| INV-05 | D06 auto-trigger heuristics (prompt-scanning attach) | LR-REJECT-8 (D06, Row 27) |
| INV-05 | D08 classification header emission without ME-7 precondition | ME-7 / LR-DEFER-5 |
| INV-05 | D01 `allowed-tools:` enforcement without ME-8 precondition | ME-8 / LR-DEFER-4 |
| INV-05 | D13 auto-suggest keywords | LR-REJECT-6 (D13, Row 25) |
| INV-05 | D02 / Layer A `mcp-servers:` advertisement (re-affirmed REJECT) | ME-9 / LR-REJECT-1 |

**16 explicit alternatives blocked.** The merged surface is the only shape consistent with INV-01..INV-05.

---

## 5. Acceptance Criteria recap (T07.03 #3, #4)

| AC | Statement | Evidence |
|---|---|---|
| **AC #3** | `invariant-survival-walkthrough.md` runs a worked example through the merged `/task` and demonstrates INV-01..INV-05 each still hold | § 1 (worked example) + § 2 (step-by-step run, 10 stages) + § 3 (per-invariant survival summary with absorbed-feature interaction table). Each invariant has a "verdict: SURVIVES" line with disk-evidence demonstration. |
| **AC #4** | Interactions between absorbed features and invariant surfaces are shown explicitly | § 3 — per-invariant tables list every absorbed feature touching that invariant surface with the interaction + the demonstration. § 4 — counter-factual register names every donor variant that *would* have broken an invariant and cites the block source. |

---

**T07.03 deliverable #2: COMPLETE.** All five invariants demonstrated to survive under the merged `/task` surface via a worked example exercising every absorbed feature. The counter-factual register names 16 donor variants that the manifest explicitly blocks; the merged shape is the only INV-safe shape.
