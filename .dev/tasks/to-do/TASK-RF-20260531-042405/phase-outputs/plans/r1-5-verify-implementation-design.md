# R1.5 — `verify-implementation` Terminal Step — DESIGN DOCUMENT

**Task:** TASK-RF-20260531-042405 — Roadmap pipeline brittleness-elimination refactor (R0+R1)
**Phase / Step:** R1.5 / Step 10.1 (DESIGN, doc-only)
**Date:** 2026-06-02
**Status:** Design pinned by task item; this doc records (does not re-litigate) the decisions.
**Scope of this step:** READ source + WRITE this one markdown design doc. **Zero source/test edits.**

> **Doc-only contract.** This step writes only this design file. The working tree carries
> another workstream's uncommitted edits to `executor.py` / `gates.py`; touching source here
> would tangle them. Implementation lands in Step 10.2; tests in Step 10.3.

---

## 0. Citation ledger (verified against on-disk files, 2026-06-02)

All `file:line` references below were re-read against the working-tree files this session.
The following **stale citations** in upstream artifacts were found and **corrected**:

| Source artifact | Stale claim | Corrected fact (verified this session) |
|---|---|---|
| BUILD-REQUEST §MVR §4 (line 126) | fail-open default at `fidelity_checker.py:287-303` | The `found = True` **literals** are at `fidelity_checker.py:302` (the `not mapping.expected_names` branch) **and `:320`** (the partial-evidence branch). `287-303` is the *start of the result loop*, not where the fail-open assignment sits. **Two** fail-open sites exist, not one. |
| BUILD-REQUEST §MVR §4 (line 126) | iterate `envelope.spec_ids[FR]` (subscript) | `spec_ids` is a `SpecIdRegistry` **dataclass**, not a dict. Subscripting raises `TypeError`. Correct accessor is **`envelope.spec_ids.fr_ids`** (`id_registry.py:84`). |
| research/01 §A.4 (line 118) | `_scan_codebase` "cited ~L284" | `FidelityChecker._scan_codebase` is **defined at `fidelity_checker.py:169`**; the *call site* `codebase_names = self._scan_codebase()` is at **`:288`**. AST helper body (`ast.parse` + `ast.walk`) spans **`:183-188`** (research cited the helper range as `165-200`, which is approximately correct: the method spans `169-204`). |
| Task item (Step 10.1 brief) | wiring-verification Step "constructed at ~L2588" | The `Step(id="wiring-verification", ...)` literal opens at **`executor.py:2590`** (block spans `2590-2599`). `2588` is the close-paren of the preceding `merge`-related step. |

Primary grounded references used throughout:

- `src/superclaude/cli/roadmap/executor.py` — `_build_steps` def `L2340`; step literals `L2418-2620`; `wiring-verification` Step `L2590-2599`; `build_certify_step` `L2140`; dynamic certify dispatch `_run_certify_after_remediate` `L2189-2298` (gate eval at `L2259-2270`).
- `src/superclaude/cli/roadmap/gates.py` — `CERTIFY_GATE` `L1433-1474`; `assert_step_reachable` import `L28`; `ALL_GATES` (14 entries) `L1549-1564`.
- `src/superclaude/cli/pipeline/models.py` — `SemanticCheck` `L82`; `CodeAssertion` `L91-117`; `GateCriteria` `L121-142`.
- `src/superclaude/cli/pipeline/gates.py` — `gate_passed(...)` `L20-110`; code_assertion dispatch `L93-104`; **envelope-None skip shim `L94-98`** (INV-002).
- `src/superclaude/cli/roadmap/envelope.py` — `PipelineEnvelope` `L127-202`; `spec_ids` field `L197`; `accepted_deviations` field `L202`; `artifacts` field `L198`.
- `src/superclaude/cli/roadmap/id_registry.py` — `SpecIdRegistry` `L43-132`; `.fr_ids` `L84`; `.accepted_deviation_ids` `L90`; `.union_of_known()` `L94`.
- `src/superclaude/cli/roadmap/code_assertions.py` — `assert_step_reachable` `L27-...`; `assert_envelope_artifacts_present` `L126-...` (the existing "empty-map → no-op PASS" precedent that §6 deliberately inverts).
- `src/superclaude/cli/roadmap/fidelity_checker.py` — `_scan_codebase` `L169`; AST scan `L183-188`; fail-open `L302` + `L320`.

---

## 1. §MVR §4 canonical definition + Contract #2 / #4 mapping

### 1.1 §MVR §4 — verbatim (BUILD-REQUEST lines 123-128)

> **4. Terminal verification link — Tasklist → AST**
>
> - New step `verify-implementation` runs after `tasklist` (or after `certify` in the
>   roadmap-only path), with a `CodeAssertion`-only gate:
>   - For each FR in `envelope.spec_ids[FR]`, the assertion either (a) finds an importable
>     callable matching the spec's name binding, (b) finds it via `fidelity_checker`'s AST
>     scan (`fidelity_checker.py:165-200`), or (c) matches an accepted deviation. No
>     fail-open default (`fidelity_checker.py:287-303` `found=True` is deleted).
>   - Failure produces a HIGH `Finding` and halts. **Kills master:§Flaw 1 evidence chain entirely.**

**Two phrasings in the verbatim above are SUPERSEDED by pinned decisions in this doc** (and
are *not* to be implemented literally):

1. `envelope.spec_ids[FR]` (subscript) → use **`envelope.spec_ids.fr_ids`** (the registry is a
   dataclass; §4 and §5 below). Subscripting raises `TypeError`.
2. Branch (a) "finds an importable callable" + branch (b) "`fidelity_checker`'s AST scan over
   `src/`" describe **source-tree / `importlib` resolution**. Per the R1.3 CI-vs-runtime split,
   **source-tree resolution is CI-ONLY** and lives in the Step 10.3 test scaffold, NEVER the live
   runtime gate. The live runtime substrate is the run's OWN emitted artifacts (§5). The
   `fidelity_checker.py:302`/`:320` fail-open deletion is **R1.6 Step 11.4**, not this step — see
   §8 sequencing constraint.

### 1.2 Contract #2 — Dispatch-reachability invariant (verbatim, line 58)

> **2. Dispatch-reachability invariant.** If the fix adds a new builder, runner, gate, or hook
> symbol, a test MUST assert the symbol is reachable from a production entry point
> (`_build_steps()`, `execute_sprint()`, `run_portify()`, `execute_pipeline()`). Mechanism: AST
> walk + dispatch-graph trace. Failure mode targeted: master:§Flaw 1 "written but not wired."

**Mapping:** `verify-implementation` is itself a new step symbol. It MUST be reachable from the
production `_build_steps()` dispatch (terminal position). The existing `assert_step_reachable`
(`code_assertions.py:27`, wired on `CERTIFY_GATE`, `gates.py:1463-1473`) is the precedent
mechanism — an AST walk over `executor.py:_build_steps`. Acceptance Gate #8 ("`verify-implementation`
terminal step is live and wired") is the dispatch-reachability obligation for THIS step.

### 1.3 Contract #4 — No silent PASS on empty / wrong-target inputs (verbatim, line 62)

> **4. No silent PASS on empty / wrong-target inputs.** Every gate that consumes a directory,
> file list, or token set MUST assert `len(input) > 0` before emitting PASS. Test:
> `tests/roadmap/test_gate_empty_target.py` enumerates every gate symbol and asserts
> `gate(empty_input).status != PASS`. Failure mode: master:§Recurrence #3 wiring-verification
> silent PASS.

**Mapping:** the FR token set consumed by `verify-implementation` is `envelope.spec_ids.fr_ids`.
Contract #4 makes the **empty-`fr_ids` case a FAIL, not a silent PASS** (§6). This is the exact
master:§Recurrence #3 failure mode that the step it *replaces* (`wiring-verification`) historically
exhibited — so consolidating `wiring-verification` into a Contract-#4-compliant assertion is a net
hardening, not a regression (§3).

---

## 2. Step ID, terminal position, dispatch wiring point

| Property | Value |
|---|---|
| **Step ID** | `verify-implementation` |
| **Position** | **TERMINAL** — after `certify` (the roadmap-only path; §MVR §4 "after `certify`") |
| **Gate** | `VERIFY_IMPLEMENTATION_GATE` (§7) — a `CodeAssertion`-only gate |
| **Dispatch wiring point** | `executor.py:_build_steps` (`L2340`), terminal position. The `wiring-verification` Step literal (`L2590-2599`) is **deleted** and `verify-implementation` takes the budget slot (§3). |
| **`ALL_GATES` register** | `gates.py:1549-1564` — replace the `("wiring-verification", WIRING_GATE)` entry (`L1560`) with `("verify-implementation", VERIFY_IMPLEMENTATION_GATE)`. |

**Terminal-after-certify nuance.** `certify` is constructed *dynamically* by
`_run_certify_after_remediate` (`executor.py:2189`) — it is NOT a static `_build_steps` literal
(only its budget slot lives in `ALL_GATES`). `verify-implementation`, by contrast, is pinned to be
a **static terminal `_build_steps` literal** so its own Contract #2 dispatch-reachability is
trivially satisfied by `assert_step_reachable`-shaped logic (shape 1: static `Step(id=...)` literal).
The 10.2 implementation appends the `verify-implementation` Step literal at the end of the
`_build_steps` list (replacing the deleted `wiring-verification` block) so the live dispatch runs it
after the dynamic certify step has produced its artifact.

---

## 3. Consolidation choice — REPLACE `wiring-verification` (PINNED)

**Decision (pinned, not re-litigated): `verify-implementation` REPLACES `wiring-verification`.**
`certify` is **PRESERVED** (it carries the R1.3 runtime `semantic_checks` + the
`assert_step_reachable` `CodeAssertion`, `gates.py:1443-1473`).

### 3.1 Rationale

- `wiring-verification` (`executor.py:2590-2599`, gate `WIRING_GATE` from
  `superclaude.cli.audit.wiring_gate`) AST-grounds the "is the spec's named binding wired" property
  in *shadow/trailing* mode (`gate_mode=GateMode.TRAILING`, `L2598`). `verify-implementation`
  AST-grounds the **same property** (FR → named-binding resolution) but as a **blocking, fail-closed,
  Contract-#4-compliant** terminal gate. The properties overlap; keeping both would be redundant and
  would *grow* the step count.
- `wiring-verification` is the canonical master:§Recurrence #3 "silent PASS" offender (Contract #4
  line 62 names it explicitly). Replacing it with a fail-closed assertion *closes* that recurrence
  rather than leaving a second weaker gate alongside the strong one.

### 3.2 Step-count math (Acceptance Gate #6: final count ≤ 14)

Acceptance Gate #6 (BUILD-REQUEST line 202): *"Step count does not increase … final pipeline step
count ≤ current (14)."* The canonical step-count register is `ALL_GATES` (`gates.py:1549-1564`),
which has **14 entries** today (executor.py:2202-2205 comment confirms "`ALL_GATES` stays at 14").

```
Current step count (ALL_GATES):                 14
  + verify-implementation  (terminal, new)      +1   -> 15   (would BREACH Gate #6)
  - wiring-verification    (deleted/replaced)   -1   -> 14   (budget preserved)
-----------------------------------------------------------
Final step count:                               14   OK  <= 14  (Acceptance Gate #6 satisfied)
```

**Net delta = 0.** The replacement keeps the count at exactly 14. If `verify-implementation` were
*appended* without deleting `wiring-verification`, the count would be 15 and Gate #6 would FAIL —
this is why "replace" (not "add") is the pinned choice.

### 3.3 Touch points for the deletion (10.2 work, not done here)

1. `executor.py:2590-2599` — delete the `Step(id="wiring-verification", ...)` literal.
2. `gates.py:1560` — replace `("wiring-verification", WIRING_GATE)` in `ALL_GATES` with the new entry.
3. `executor.py:1086` — the `if step.id == "wiring-verification":` dispatch branch (the runner's
   special-case for the shadow gate) is removed or repointed (10.2 to confirm exact handling).
4. `envelope.py:634-643` + `POST_EXTRACTORS["wiring-verification"]` (`L700`) — the post-extractor
   entry is repointed to `verify-implementation` (10.2 to confirm; not blocking for the design).

---

## 4. The `CodeAssertion` — `assert_all_frs_resolved` + the `.fr_ids` accessor guard

### 4.1 Signature

```python
# new in: src/superclaude/cli/roadmap/code_assertions.py  (10.2)
def assert_all_frs_resolved(
    envelope: PipelineEnvelope,
    repo_path: Path | None = None,
) -> Finding | None:
    ...
```

- Return convention matches the existing `CodeAssertion` contract (`models.py:110-113`):
  **`None` -> PASS**, **`Finding` (HIGH severity) -> FAIL**.
- `repo_path` is accepted for signature-parity with `assert_step_reachable(envelope, repo_root)`
  (`code_assertions.py:27`) and the `gate_passed` dispatch (`pipeline/gates.py:100`,
  `assertion.check_fn(envelope, repo_root)`). **In the live runtime path `repo_path` is NOT used to
  resolve FRs against the source tree** (§5) — it is reserved/ignored at runtime, mirroring the
  `del envelope  # reserved` pattern at `code_assertions.py:76`. Source-tree resolution that *does*
  consult a path is the CI-only test scaffold (§5, §9).

### 4.2 The `.fr_ids` accessor guard (REGRESSION GUARD — load-bearing)

The assertion iterates **`envelope.spec_ids.fr_ids`** — the tuple-typed dataclass **accessor**
(`id_registry.py:84`). It MUST **NEVER** subscript `envelope.spec_ids[FR]`.

```python
# CORRECT (pinned):
for fr_id in envelope.spec_ids.fr_ids:        # tuple[str, ...] — id_registry.py:84
    ...

# FORBIDDEN — raises TypeError at runtime:
for fr_id in envelope.spec_ids["FR"]:         # SpecIdRegistry is a @dataclass(frozen=True),
                                              # NOT a dict — id_registry.py:43-92
```

**Why this is a regression guard, not a style note:** `SpecIdRegistry` (`id_registry.py:43`) is a
`@dataclass(frozen=True)` with tuple fields (`fr_ids`, `nfr_ids`, …, `accepted_deviation_ids`). It
exposes **no `__getitem__`**, so `spec_ids[FR]` raises `TypeError: 'SpecIdRegistry' object is not
subscriptable`. The §MVR §4 verbatim text uses the subscript form (`envelope.spec_ids[FR]`); copying
that pseudocode literally is the exact bug this guard prevents. The companion accessors the assertion
also reads — `envelope.spec_ids.accepted_deviation_ids` (`id_registry.py:90`) and
`envelope.accepted_deviations` (`envelope.py:202`) — are likewise field accessors, never subscripts.

---

## 5. FR-resolution substrate — RUN ARTIFACTS, not the `src/` tree (LOAD-BEARING)

This is the section that distinguishes the live runtime gate from the historical
`fidelity_checker` behavior. It is the single most important design decision in R1.5.

### 5.1 What "resolve an FR" means at RUNTIME

For each `fr_id` in `envelope.spec_ids.fr_ids`, the runtime assertion resolves it against the
**run's OWN emitted artifacts** — the tasklist / roadmap markdown this very pipeline run produced —
plus the accepted-deviation channels. Concretely, an `fr_id` is **resolved** iff at least one of:

| # | Resolution channel | Substrate (runtime) |
|---|---|---|
| (a) | The FR's named binding appears in the run's emitted tasklist/roadmap artifacts | Read from the run output dir via `envelope.artifacts` (`envelope.py:198`, `ArtifactRef.path`) — AST/text-scan each artifact for the FR's named binding. |
| (b) | The FR ID is in `envelope.spec_ids.accepted_deviation_ids` | `id_registry.py:90` (the ID-only tuple). |
| (c) | The FR ID matches a full accepted-deviation record | `envelope.accepted_deviations` (`envelope.py:202`, `list[AcceptedDeviation]`, each `.id`). |

The "named binding" scan reuses the **same AST/text mechanism** as
`fidelity_checker._scan_codebase` (`fidelity_checker.py:169`, `ast.parse`+`ast.walk` over
`FunctionDef`/`AsyncFunctionDef`/`ClassDef`, `L183-188`) — but pointed at the run's emitted artifact
files (resolved from `envelope.artifacts`), **NOT** at the pipeline `src/` tree.

### 5.2 What the runtime gate MUST NOT do

- **MUST NOT** scan / import / `importlib`-resolve against the pipeline's own `src/` source tree.
- **MUST NOT** call `FidelityChecker(source_dir=<pipeline src>)._scan_codebase()` on the live path.
- **MUST NOT** consult `repo_path` to walk source modules at runtime (§4.1 — `repo_path` is
  reserved/ignored on the live path).

**Why.** The pipeline *generates a roadmap/tasklist* — it does not, at runtime, have access to a
post-implementation source tree where the FRs' callables would already exist. Resolving FRs against
the pipeline's own `src/` would (i) measure the wrong artifact (the generator's code, not the run's
output), and (ii) reintroduce the master:§Flaw 1 "evidence chain" confusion §MVR §4 exists to kill.
Per the **R1.3 CI-vs-runtime split**, source-tree / `importlib` / `fidelity_checker._scan_codebase`
resolution is **CI-ONLY** and belongs in the Step 10.3 test scaffold (§9.2), never the live gate.

### 5.3 Substrate summary (the canonical runtime inputs)

```
RUNTIME inputs to assert_all_frs_resolved (ALL from the envelope, NONE from src/):
  - envelope.spec_ids.fr_ids                    # the FR token set to resolve  (id_registry.py:84)
  - envelope.artifacts                          # run's emitted tasklist/roadmap (envelope.py:198)
  - envelope.spec_ids.accepted_deviation_ids    # ID-only accepted deviations  (id_registry.py:90)
  - envelope.accepted_deviations                # full deviation records       (envelope.py:202)

CI-ONLY (Step 10.3 test scaffold, NEVER the live gate):
  - FidelityChecker(source_dir=...)._scan_codebase()  # source-tree AST resolution
  - importlib-based callable resolution
```

---

## 6. Fail-closed semantics (Contract #4)

The gate is **fail-closed**. There is **no fail-open `found=True` fallback anywhere** in the runtime
path (contrast `fidelity_checker.py:302` and `:320`, which R1.6 Step 11.4 deletes — §8).

### 6.1 Rules

1. **Every unmatched FR → one HIGH `Finding`.** For each `fr_id` not resolved via channel (a)/(b)/(c)
   of §5.1, emit a HIGH-severity `Finding` (`models.py:33` `severity`, `:34` `dimension`,
   `:35` `description`, `:36` `location`). The first such Finding is returned by the assertion (PASS
   ⇔ returns `None`). 10.2 decides whether to aggregate all unmatched FRs into one Finding's evidence
   or return on first — but the gate verdict is FAIL the moment any FR is unmatched.
2. **Empty `fr_ids` → FAIL (NOT silent PASS).** If `envelope.spec_ids.fr_ids` is empty, the assertion
   **MUST return a HIGH `Finding`**, not `None`. An empty FR set means the run never extracted any FRs
   to verify — the master:§Recurrence #3 "silent PASS on empty input" shape Contract #4 (line 62)
   forbids.

   > **Deliberate inversion of the existing precedent.** `assert_envelope_artifacts_present`
   > (`code_assertions.py:126`) treats an empty `artifacts` map as a **no-op PASS** ("nothing recorded
   > yet is a vacuous PASS, not a failure" — `code_assertions.py:143`). `assert_all_frs_resolved`
   > does the **opposite** for `fr_ids`: empty is a FAIL. The difference is intentional and
   > Contract-#4-driven — an FR token set is a *consumed input* the gate emits PASS over, so
   > `len(fr_ids) > 0` is the Contract #4 precondition; artifact presence is a structural sanity
   > check with different semantics. 10.2 MUST NOT copy the empty-map=PASS pattern for `fr_ids`.

3. **No fail-open default.** No branch may set a resolved/`found=True` sentinel "because names
   couldn't be extracted" (the `fidelity_checker.py:302` anti-pattern). Inability to extract a name
   for an FR is itself an unmatched-FR FAIL, unless the FR is an accepted deviation (channel b/c).

### 6.2 Decision table

| `fr_ids` | All FRs resolved via (a)/(b)/(c)? | Assertion returns | Gate verdict |
|---|---|---|---|
| empty `()` | n/a | **HIGH `Finding`** | **FAIL** (Contract #4 empty-input guard) |
| non-empty | yes | `None` | PASS |
| non-empty | no (≥1 unmatched) | **HIGH `Finding`** | **FAIL** |

---

## 7. `VERIFY_IMPLEMENTATION_GATE` definition + live-path envelope plumbing (INV-002)

### 7.1 Gate definition (pinned)

```python
# new in: src/superclaude/cli/roadmap/gates.py  (10.2)
VERIFY_IMPLEMENTATION_GATE = GateCriteria(
    required_envelope_fields=["spec_ids"],
    min_lines=0,
    enforcement_tier="STRICT",
    semantic_checks=None,
    code_assertions=[
        CodeAssertion(
            name="all_frs_resolved",
            check_fn=assert_all_frs_resolved,
            failure_message=(
                "Contract #2 + #4: every FR must resolve against the run's own "
                "emitted artifacts or be in accepted_deviations (fail-closed)"
            ),
        ),
    ],
)
```

### 7.2 ⚠ Field-name reconciliation (10.2 MUST resolve)

The pinned spec above uses `required_envelope_fields=[...]`, taken verbatim from §MVR §2's
pseudocode. **The actual on-disk `GateCriteria` dataclass field is named
`required_frontmatter_fields`** (`models.py:138`), NOT `required_envelope_fields`. §MVR §2 (line 109)
explicitly flags this rename intent ("`required_envelope_fields` — was: `required_frontmatter_keys`"),
but R1.3 landed the field as `required_frontmatter_fields` and it has not been renamed. **10.2 MUST
either** (i) construct the gate with the *actual* field name `required_frontmatter_fields=["spec_ids"]`,
or (ii) rename the dataclass field first (out of R1.5 scope; touches every gate). The
**`CodeAssertion`-only** intent (`semantic_checks=None`, `min_lines=0`) is satisfiable today with the
existing field shape: a `code_assertions`-only gate with `required_frontmatter_fields=[]` and
`min_lines=0` runs zero frontmatter/semantic checks and dispatches only the assertion. This doc pins
the *intent*; 10.2 pins the *exact constructor* against the real field name. (`CodeAssertion` fields
are `name` / `check_fn` / `failure_message` — `models.py:115-117`; no per-assertion `min_lines`.)

### 7.3 INV-002 — live-path envelope plumbing (10.2 requirement)

`assert_all_frs_resolved` is a **runtime-artifact-based** assertion: it consumes `envelope`. The
gate dispatcher `gate_passed(...)` (`pipeline/gates.py:20`) accepts `envelope` / `repo_root` as
**optional kwargs** and contains a backward-compat shim:

```python
# pipeline/gates.py:93-98  (verified this session)
if criteria.code_assertions:
    if envelope is None or repo_root is None:
        # ... assertions are SILENTLY SKIPPED ...
        return True, None      # <-- fail-OPEN skip when envelope not plumbed
    for assertion in criteria.code_assertions:
        finding = assertion.check_fn(envelope, repo_root)
        ...
```

**INV-002:** if the live dispatch for `verify-implementation` does **not** pass `envelope`
(and `repo_root`) into `gate_passed`, the shim at `pipeline/gates.py:94-98` makes the gate **return
`(True, None)` — a silent PASS — and the assertion never runs (dormant).** This is the same gap that
already neuters `CERTIFY_GATE`'s code_assertion on the dynamic certify path (`executor.py:2259-2270`
explicitly omits `envelope`, running only the three SemanticChecks).

**10.2 implementation requirement:** the `verify-implementation` gate evaluation MUST plumb the live
`PipelineEnvelope` (and `repo_root`) into the `gate_passed` call so `assert_all_frs_resolved` actually
executes. A `verify-implementation` gate that omits `envelope` is **worse than useless** — it presents
as a passing terminal verification while verifying nothing. Step 10.3 MUST include a test that the
live dispatch passes a non-`None` envelope (i.e. asserts the assertion is reached, not skipped).

---

## 8. H2 sequencing prerequisite — coupling to R1.6 Step 11.4 (MUST appear)

`verify-implementation` **MUST NOT ship to production before R1.6 Step 11.4** deletes the fail-open
`found = True` assignments at **`fidelity_checker.py:302` and `:320`** (the `not
mapping.expected_names` fail-open branch and the partial-evidence fail-open branch). *(Citation
correction: the task brief / §MVR §4 cite `fidelity_checker.py:287-303`; the actual `found = True`
literals are at `:302` and `:320` — `287-303` is the start of the result loop. See §0.)*

**Why the coupling exists (H2).** `verify-implementation` is the blocking, fail-closed terminal gate
for FR resolution. If the legacy fail-open `fidelity_checker` path is still live and reachable when
the new gate ships, two FR-resolution substrates coexist — one fail-closed (new), one fail-open
(legacy `:302`/`:320`) — and a run can present a green `verify-implementation` while the legacy
shadow path silently masks unresolved FRs. Shipping the strong gate while the weak one is still wired
recreates exactly the master:§Flaw 1 dual-path confusion §MVR §4 exists to eliminate.

**Acceptable orderings (either is valid):**

- **(A)** Ship R1.6 Step 11.4 (fail-open deletion) **before** the R1.5/Step 10.x gate goes live in
  production.
- **(B)** Ship Phase 10 (R1.5) + Phase 11 (R1.6) **atomically** in one production cutover.

10.2/10.3 may *land code* ahead of 11.4 (behind the dual-write / non-production posture), but the
**production go-live** of `verify-implementation` is gated on 11.4 by one of (A)/(B).

---

## 9. Downstream notes — Steps 10.2 (implementation) and 10.3 (tests)

### 9.1 Step 10.2 — implementation checklist (NOT done in this doc)

1. Add `assert_all_frs_resolved(envelope, repo_path=None) -> Finding | None` to
   `code_assertions.py` — iterate `envelope.spec_ids.fr_ids` (§4.2 accessor guard), resolve via the
   three runtime channels (§5.1), fail-closed incl. empty-`fr_ids` (§6).
2. Add `VERIFY_IMPLEMENTATION_GATE` to `gates.py` — reconcile the `required_frontmatter_fields`
   field-name (§7.2); `code_assertions`-only.
3. Append the `Step(id="verify-implementation", gate=VERIFY_IMPLEMENTATION_GATE, ...)` literal as the
   **terminal** entry in `_build_steps` (`executor.py`), and **delete** the `wiring-verification` Step
   literal (`executor.py:2590-2599`) — net step delta 0 (§3.2).
4. Replace the `("wiring-verification", WIRING_GATE)` entry in `ALL_GATES` (`gates.py:1560`) with
   `("verify-implementation", VERIFY_IMPLEMENTATION_GATE)`.
5. **Plumb `envelope` + `repo_root` into the live `gate_passed` call** for this step (INV-002, §7.3) —
   otherwise the assertion is dormant.
6. Handle / remove the `if step.id == "wiring-verification":` runner branch (`executor.py:1086`).
7. Repoint the `POST_EXTRACTORS` entry (`envelope.py:700`) from `wiring-verification` to
   `verify-implementation` (or confirm no extractor is required).

### 9.2 Step 10.3 — tests checklist (NOT done in this doc)

1. **CI-only source-tree resolution test path.** The §MVR §4 branches (a)/(b) (importable-callable /
   `fidelity_checker._scan_codebase` source-tree resolution) live HERE, in the test scaffold — NOT in
   the live gate (§5.2). A CI test may construct `FidelityChecker(source_dir=<repo>)._scan_codebase()`
   to cross-check FR bindings against actual source; this is explicitly CI-only.
2. **Empty-`fr_ids` → FAIL** test (Contract #4, §6 — the `test_gate_empty_target.py` enumeration
   from Contract #4 line 62 should include `VERIFY_IMPLEMENTATION_GATE`).
3. **Every-unmatched-FR → HIGH Finding** test (§6.1).
4. **`.fr_ids` accessor regression test** — assert the assertion uses the accessor, e.g. by passing a
   real `SpecIdRegistry` and confirming no `TypeError` (§4.2).
5. **INV-002 plumbing test** — assert the live dispatch passes a non-`None` envelope so the assertion
   is reached, not skipped by the `pipeline/gates.py:94-98` shim (§7.3).
6. **Dispatch-reachability (Contract #2)** — assert `verify-implementation` is reachable from
   `_build_steps` (AST walk), mirroring the `assert_step_reachable` test for certify.
7. **Step-count budget test** — assert `len(ALL_GATES) <= 14` after the change (Acceptance Gate #6).

---

## 10. Acceptance-criteria checklist (this design)

| # | Criterion | Status in this design |
|---|---|---|
| 1 | Step-count budget ≤ 14 PRESERVED | ✅ §3.2: 14 +verify-implementation −wiring-verification = **14**; net delta 0 (Acceptance Gate #6). |
| 2 | Consolidation rationale clear | ✅ §3.1: replaces `wiring-verification` (same property, fail-closed); `certify` preserved (R1.3 semantic_checks). |
| 3 | Fail-closed enforced (Contract #4) | ✅ §6: every unmatched FR → HIGH Finding; **empty `fr_ids` → FAIL** (not silent PASS); no fail-open `found=True`. |
| 4 | `.fr_ids` accessor guard documented | ✅ §4.2: iterate `envelope.spec_ids.fr_ids`; never subscript `spec_ids[FR]` (TypeError). |
| 5 | FR-resolution substrate = run artifacts, not `src/` | ✅ §5: runtime resolves vs `envelope.artifacts` + accepted_deviations; source-tree/`importlib`/`_scan_codebase` is CI-only. |
| 6 | `VERIFY_IMPLEMENTATION_GATE` + INV-002 plumbing | ✅ §7: gate pinned; field-name reconciliation flagged; envelope-plumbing requirement for 10.2. |
| 7 | H2 sequencing (couple to R1.6 Step 11.4) | ✅ §8: go-live gated on `fidelity_checker.py:302`/`:320` fail-open deletion; orderings (A)/(B). |
| 8 | Contract #2 dispatch-reachability | ✅ §1.2 + §2: terminal static `_build_steps` literal; AST-walk reachable. |
| 9 | Doc-only — zero source/test edits | ✅ Only this `.md` created; all other files READ-ONLY. |
| 10 | Stale citations corrected | ✅ §0 ledger: `:287-303` → `:302`/`:320`; `spec_ids[FR]` → `.fr_ids`; `_scan_codebase` `L169`/call `L288`; wiring Step `L2590`. |

---

## 11. Summary

`verify-implementation` is a fail-closed, `CodeAssertion`-only **terminal** step (after `certify`)
that **replaces** `wiring-verification` (keeping `ALL_GATES` at 14, Acceptance Gate #6). Its single
assertion `assert_all_frs_resolved(envelope, repo_path=None)` iterates `envelope.spec_ids.fr_ids`
(accessor, never subscript) and resolves each FR against the **run's own emitted artifacts** +
`accepted_deviations` — **never** the pipeline `src/` tree (source-tree resolution is CI-only).
Empty `fr_ids` is a FAIL (Contract #4); every unmatched FR yields a HIGH `Finding` (no fail-open).
The live gate dispatch MUST plumb the envelope (INV-002) or the assertion is dormant, and production
go-live is sequenced behind R1.6 Step 11.4's `fidelity_checker.py:302`/`:320` fail-open deletion.
