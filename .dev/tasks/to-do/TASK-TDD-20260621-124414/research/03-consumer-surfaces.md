# Research 03 — Consumer Surfaces Downstream of the `runtime_surface_*` Contract

**Status:** Complete

**Investigation type:** Integration Mapper
**Topic:** Every place that consumes the six `runtime_surface_*` scalars and must read deterministically-written values.
**Component roots:** `src/superclaude/skills/sc-reflect-protocol/`, `src/superclaude/cli/sprint/`
**Worktree root:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/`

Staleness tags: `[CODE-VERIFIED]` = claim read directly from the cited file/lines in this session.
Each SKILL.md claim below was confirmed against the actual file (line numbers shifted from the task brief's estimates; corrected values are recorded inline).

---

## 1. The Six Canonical `runtime_surface_*` Field Names (verbatim)

[CODE-VERIFIED] SKILL.md §9.1, contract block lines 720–736 (not ~721–735 as the brief estimated; the
`# Runtime-surface reachability (FR-RSR — UC-2)` header is at line 720, the six fields at 731–736).

The brief asks for "six `runtime_surface_*` scalars." Read literally, only **five** declared field names
carry the `runtime_surface_` prefix; the sixth member of the contract's six-field surface group is
`unreached_surfaces` (a list, not a scalar). The §9.3 consumer map's UC-2 row enumerates exactly these six
as the consumer's load-bearing set. Both readings are documented so downstream code keys on the right names.

The six fields, verbatim from lines 731–736:

1. `runtime_surface_requirements` — `[<list str>]` — FR-RSR.1: surface requirement ids tagged from symbol kind/decorator; `[]` when none.
2. `runtime_surface_sweep_ran` — `<bool>` — FR-RSR.2: true ONLY when ≥1 tagged surface triggered the sweep.
3. `runtime_surface_ledger_path` — `<abs path> | null` — FR-RSR.2: `<output>/artifacts/runtime-surface-ledger.yaml`; null when sweep did not run.
4. `runtime_surface_unreached` — `<int>` — FR-RSR.2/6: count of SYMBOLS reduced to UNREACHED; 0 on a fully-REACHED run; **drives the §5.3 pre-filter**.
5. `runtime_surface_degraded` — `<bool>` — FR-RSR.3/8: true when ≥1 symbol reduced to DEGRADE (→ §10.6 Grounding Gap); false on a fully-REACHED run.
6. `unreached_surfaces` — `[<list of UnreachedSurface>]` — FR-RSR.6: one entry per UNREACHED symbol; `[]` on REACHED and on DEGRADE-only runs.

[CODE-VERIFIED] `contract_version: "1.6.0"` confirmed at SKILL.md line 671–672. Line 672 comment:
`1.6.0 (FR-RSR) ADDITIVE ONLY: +runtime_surface_* (6 fields)`. So the spec itself counts all six
(including `unreached_surfaces`) as "the `runtime_surface_*` (6 fields)" group — the prefix is used
loosely to name the group, even though one member lacks the literal prefix.

### 1.1 Mandatory-emission rule (the determinism contract)

[CODE-VERIFIED] SKILL.md lines 721–730 — `MANDATORY EMISSION (FR-RSR.7)` comment inside the contract block:

- Whenever `runtime_surface_sweep_ran` is true, ALL SIX fields MUST be emitted with these EXACT names on
  EVERY path — REACHED, DEGRADE, and UNREACHED alike.
- Do NOT invent alternative field names. The comment explicitly forbids `runtime_surface_reachable`,
  `reachability_path`, `static_caller_absent_is_expected` — "those are NOT contract fields and a consumer
  keyed on §9.3 will not see them."
- Per-verdict emission (lines 727–729):
  - REACHED → `runtime_surface_unreached: 0`, `runtime_surface_degraded: false`, `unreached_surfaces: []`
  - DEGRADE → `runtime_surface_degraded: true` (+ a §10.6 Grounding Gap row); symbol NOT in `unreached_surfaces`
  - UNREACHED → `runtime_surface_unreached: <count ≥ 1>`, one `unreached_surfaces[]` entry per UNREACHED symbol
- Count invariant (line 730): `len(unreached_surfaces) == runtime_surface_unreached` MUST hold every run.

This mandatory-emission + count-invariant pair is exactly the "deterministically-written values" that
consumers must be able to read. A consumer reading a field that the producer skipped on the REACHED path
(or that the producer named non-canonically) is the failure mode the rule guards against.

---

## 2. Consumer Surface A — §5.3 Pre-filter (in-skill tiering consumer)

[CODE-VERIFIED] SKILL.md §5.3, paragraph "Pre-filter precedence (D13)" at line 402 (brief estimated ~402; exact).
Also the table rows 1 and 2 at lines 390–391, and the `tier_decision.yaml` audit fields at lines 412.

**The consumer:** the §5.3 tier-decision table — the in-skill mechanism that decides STOP-at-Tier-1 vs.
escalate-to-Tier-2. It reads `runtime_surface_unreached` (the scalar) as a TABLE-WIDE pre-filter.

**Trigger condition (verbatim, line 402):** when `surface_unreached` is set "from a SUCCESSFUL runtime-surface
sweep with `runtime_surface_unreached ≥ 1`, NO STOP row (1, 2, or the row-8 default) may fire and the run
routes to Tier 2." The pre-filter is authoritative; the row-1/row-2 `NOT surface_unreached` conjuncts
(lines 390–391) are "redundant safeties."

**Override precedence (line 402):**
- Explicit user pins outrank the pre-filter: `--tier 1`, `--depth quick`, `--no-escalate` proceed at the
  pinned tier with a loud WARN; for `surface_unreached` the pinned run ALSO forces `status: partial`.
- A degrade-only run (`runtime_surface_unreached == 0`, regardless of `runtime_surface_degraded`) does NOT
  force Tier 2 through this pre-filter; its Grounding Gap path independently prevents a clean PASS.

**Determinism dependency:** this consumer reads field #4 (`runtime_surface_unreached`) and tests `≥ 1`.
It depends on the producer having written `0` (not omitted, not null) on the REACHED path — exactly the
mandatory-emission guarantee of §1.1. If the field were absent on a successful-sweep REACHED run, the
`≥ 1` comparison is undefined and the pre-filter cannot be evaluated deterministically.

**Audit recording:** [CODE-VERIFIED] §5.4 lines 412 — `tier_decision.yaml` records
`surface_unreached: "runtime_surface_unreached"` when the FR-RSR successful-sweep pre-filter forced T2.
This is recording, not deciding (line 423: "The composite is *recording*, not deciding").

---

## 3. Consumer Surface B — §9.3 UC-2 Advisory Row (NON-GATING classification)

[CODE-VERIFIED] SKILL.md §9.3 Consumer Field Map, "Any UC-2 consumer (advisory, FR-RSR)" row at line 890
(brief estimated ~line 890; exact).

**Load-bearing fields declared for this consumer (verbatim, line 890):**
`runtime_surface_requirements`, `runtime_surface_sweep_ran`, `runtime_surface_ledger_path`,
`runtime_surface_unreached`, `runtime_surface_degraded`, `unreached_surfaces` — all six.

**Routing semantics (verbatim):** "NON-GATING advisory: runtime-surface fields MAY be surfaced for
reachability diagnostics, but existing consumers need no load-bearing change; consumers that ignore unknown
fields remain conforming under §9.4 read-and-ignore forward compatibility."

**Key tension to flag:** §9.3 classifies the runtime-surface fields as NON-GATING **advisory** for external
UC-2 consumers, yet §5.3 (Surface A above) makes `runtime_surface_unreached` strictly GATING for the
in-skill tier decision. There is no contradiction once the boundary is read precisely:
- INSIDE the skill, `runtime_surface_unreached ≥ 1` is a hard table-wide pre-filter (gating).
- OUTSIDE the skill (the §9.3 external-consumer contract), the same fields are advisory; an external consumer
  that ignores them stays conforming.

So the determinism guarantee matters for BOTH: the in-skill §5.3 consumer NEEDS deterministic `0`/`≥1`;
external consumers MAY read but are not required to gate. A future consumer that wants to gate on
reachability must read the canonical names (§1) and tolerate the advisory contract (no version bump needed
to read; a bump WOULD be needed if a consumer's row promotes a field to load-bearing — §9.3 line 880).

[CODE-VERIFIED] §9.4 line 905: minor (additive) bump → consumers MUST tolerate unknown top-level fields
(read-and-ignore); the 1.6.0 addition of the six fields was additive-only (line 672), so no existing
consumer was forced to change.

---

## 4. Deviation-Class Mapping — UNREACHED is NOT a 5th class

[CODE-VERIFIED] SKILL.md §10.9 "Runtime-surface UNREACHED (finding modifier — NOT a 5th deviation class)"
at lines 1055–1065 (brief estimated ~1057–1065; the heading is at 1055).

A decided `UNREACHED` verdict is **NOT a deviation class** — it MAPS onto the existing 4 classes by evidence
(mirroring §10.8 Reuse-Miss). The mapping is **totally ordered** (lines 1059–1061):

1. **DEGRADE first** (line 1059): if reachability could not be soundly decided, there is no UNREACHED verdict
   to map → route to §10.6 Grounding Gaps with `needs_human_decision: true` and `status: partial`; do NOT
   write to `deviation-ledger.yaml`.
2. **Contradiction next** (line 1060): a decided UNREACHED that contradicts a reachability acceptance
   criterion → §10.4 **Regression**, increments ONLY `deviation_count_by_class.regression`. It NEVER
   increments `verification_regressions_detected` (which stays exit-code-sourced from §6.1 step 5.5 / §10.4).
3. **Unmapped fallback** (line 1061): a decided UNREACHED with no tasklist mapping and no contradicted
   criterion → §10.3 **Drift**.

**Precedence (line 1063):** if a decided UNREACHED is both contradiction and unmapped, **Regression wins**
(§10.5 precedence). There is **no** 5th runtime-surface deviation class and **no**
`deviation_count_by_class.runtime_surface` (or equivalent) counter (§17.7). Blocking counts flow ONLY through
the existing Drift/Regression counters.

**Counter-hygiene risk guard (line 1065, "Risk guard (spec §7)"):** a false `UNREACHED → Regression` on
idiomatic wiring can trigger unconditional T2/T3 and TurnLedger rollback, so: Regression increments only
`deviation_count_by_class.regression`; `verification_regressions_detected` is never incremented by
runtime-surface reachability evidence.

**Consumer relevance:** the §9.3 sprint row (Surface C below) keys `deviation_class == regression` to trigger
a TurnLedger rollback. Because §10.9 routes a contradicted UNREACHED into `deviation_count_by_class.regression`,
a sprint consumer that DID read the contract would see the same `regression` signal it already gates on — no
new field needed on the rollback path. The runtime_surface scalars themselves remain advisory to that consumer
(§3); the gating signal is the existing regression counter.

---

## 5. Consumer Surface C — `superclaude sprint run` (executor.py / TurnLedger)

### 5.1 What §9.3 SAYS the sprint executor consumes

[CODE-VERIFIED] SKILL.md §9.3 line 885, row "**`superclaude sprint run` (executor.py TurnLedger)**":

- Surface: "CLI consumer of return-contract.yaml"
- Load-bearing fields: `status`, `per_task_verdicts[].status`, `per_task_verdicts[].per_task_validation_strength`,
  `per_task_verdicts[].deviation_class`, `budget_forced_tier_downgrade`
- Routing semantics: `status: partial OR failed` halts the phase; `per_task_validation_strength < 0.70` flags
  task for re-execution; `deviation_class == regression` triggers TurnLedger rollback;
  `budget_forced_tier_downgrade: true` adjusts subsequent reflect-call budget.

NOTE: the spec's sprint row does **not** list any `runtime_surface_*` field as load-bearing for the sprint
executor. Per §3 the runtime-surface fields are advisory to UC-2 consumers generally; the sprint executor's
gating signal (per §10.9 + §9.3) is the `deviation_class == regression` mapping, not the scalars directly.

### 5.2 What executor.py ACTUALLY consumes today

[CODE-VERIFIED] `src/superclaude/cli/sprint/executor.py` (read directly + grep this session):

- `TurnLedger` is imported (line 42, from `.models`) and used pervasively for **budget-aware gate
  enforcement** — `check_budget_guard` (line 404), `can_launch`/`available`/`minimum_allocation`,
  `can_run_wiring_gate` (line 555). This matches the brief's "imports TurnLedger ~line 42; budget-aware
  gate enforcement." `class TurnLedger` is defined in `cli/sprint/models.py:1016`.
- **Zero references** to any of the §9.3 load-bearing field names. Grep across `executor.py` for
  `runtime_surface`, `return-contract`, `return_contract`, `per_task_verdicts`,
  `per_task_validation_strength`, `budget_forced_tier_downgrade`, `deviation_class` → **no matches**.
- Grep across the entire `src/superclaude/cli/sprint/` package for the same tokens → **no matches**.
- The package does **not import anything from `cli/reflect`** (grep `reflect` + `import` in
  `cli/sprint/*.py` → no matches).
- The ONLY YAML the executor reads is the wiring whitelist (`wiring_whitelist.yaml`, lines 460–466 via
  `yaml.safe_load`) and its own `to_yaml` serializers (line 262). It does NOT `safe_load` a
  `return-contract.yaml` anywhere.
- Task verdicts/status are derived from process exit codes, stream-json parsing (`json.loads`, line 2695),
  provider-failure detection, and the wiring gate — NOT from a reflect contract. Status enum is
  `TaskStatus` (PASS / FAIL_TERMINAL / INCOMPLETE / SKIPPED / FAIL_PROVIDER_EXHAUSTED / PASS_RECOVERED).

[CODE-VERIFIED] Repo-wide: `runtime_surface` appears in source ONLY in skill `.md` files
(`sc-reflect-protocol/SKILL.md`, `refs/runtime-surface.md`, `refs/grader-extensions.md`,
`sc-troubleshoot-protocol/SKILL.md` + `refs/effective-input-proof.md`). It exists in **no Python file**.
`cli/reflect/contract.py` is a pure version-gate (reads only `contract_version`, line 166) and declares
none of the six fields.

### 5.3 How executor.py WOULD read the scalars (and the gap)

The §9.3 sprint row describes an **aspirational / specified** integration that is **not yet implemented**.
For the executor to consume the deterministic scalars per spec it would need to, at minimum:

1. Locate and `yaml.safe_load` the reflect `return-contract.yaml` for each reflect-gated task (no such read
   exists today — the executor never parses a reflect contract).
2. Read `status` (halt phase on `partial`/`failed`), `per_task_verdicts[].*`, and — to honor §10.9 — the
   `deviation_count_by_class.regression` / `deviation_class == regression` signal to drive TurnLedger
   rollback.
3. To consume reachability specifically, read `runtime_surface_unreached` (field #4) and `unreached_surfaces`
   (field #6) as ADVISORY diagnostics (§3); these never gate the sprint directly — the gating arrives via the
   regression mapping (§4).
4. Depend on the §1.1 mandatory-emission + count-invariant guarantee so the read is deterministic on every
   path (REACHED writes `0`/`false`/`[]`, never omits).

**Acceptance-criterion bearing:** the task brief states an acceptance criterion that "the sprint executor
reads the deterministic scalars." As of this worktree, that criterion is **NOT met by existing code** — the
executor reads no reflect contract at all. This is the central integration gap (see §6).

---

## Gaps and Questions

1. **The sprint executor does not read the reflect return-contract today.** §9.3 line 885 declares
   `superclaude sprint run (executor.py TurnLedger)` as a "CLI consumer of return-contract.yaml" with five
   load-bearing fields, but `executor.py` contains zero references to any of those fields, never
   `yaml.safe_load`s a `return-contract.yaml`, and does not import `cli/reflect`. The §9.3 row is
   forward-looking spec, not implemented behavior. → Is wiring the executor to the reflect contract in scope
   for this TDD task, or is the deliverable only the producer-side determinism guarantee plus the spec?
2. **"Six scalars" vs. five-scalars-plus-one-list.** The brief and §9.3 say "six `runtime_surface_*`
   scalars," but `unreached_surfaces` (field #6) is a list, and only five names carry the literal
   `runtime_surface_` prefix. A consumer must key on the exact six names in §1 — relying on a
   `startswith("runtime_surface_")` filter would silently drop `unreached_surfaces`. → Confirm the consumer
   reads `unreached_surfaces` by exact name.
3. **`per_task_verdicts[]` is a §9.3 array the contract block (§9.1) does not visibly define under the names
   used in line 885.** The §9.1 block I read (lines 671–876) defines `deviation_count_by_class`,
   `verification_*`, etc., but the sprint row references `per_task_verdicts[].status`,
   `per_task_validation_strength`, `deviation_class`, and `budget_forced_tier_downgrade` — a "per-task verdict
   array" cited in §12.1/§9.3 line 893 but not enumerated in the §9.1 stable block I read. → Where is
   `per_task_verdicts[]` / `budget_forced_tier_downgrade` formally declared? (Possibly in the
   telemetry/second block beyond line 876 or in `refs/`; not confirmed in this session.)
4. **Determinism dependency is currently only producer-internal.** Today the only real consumer of
   `runtime_surface_unreached` is the in-skill §5.3 pre-filter (Surface A), which runs inside the producing
   skill. No external code depends on it yet. The mandatory-emission guarantee (§1.1) therefore protects a
   future/spec consumer, not a present one. → Should a test assert the count-invariant
   (`len(unreached_surfaces) == runtime_surface_unreached`) at the contract boundary?

## Stale Documentation Found

- **Line-number drift in the task brief (expected, not a doc defect):** the brief's estimates were close but
  off by a few lines. Corrected, verified anchors: §5.3 pre-filter paragraph = line **402** (as estimated);
  contract block `contract_version: "1.6.0"` = line **672**, six fields = lines **731–736**, MANDATORY
  EMISSION comment = lines **721–730** (brief said ~721–735); §9.3 UC-2 advisory row = line **890** (exact);
  §10.9 UNREACHED-mapping heading = line **1055** (brief said ~1057–1065). No SKILL.md content was wrong;
  only the brief's approximate line numbers.
- **§9.3 line 885 describes an unimplemented integration as if it were a live consumer.** The row labels the
  sprint executor a "CLI consumer of return-contract.yaml," but no such consumption exists in
  `cli/sprint/`. This is a documentation-vs-code mismatch: the contract spec promises a consumer surface the
  code has not built. Not a stale *value*, but a stale *integration claim* — flagged because a reader of §9.3
  would reasonably assume `executor.py` already reads these fields.
- **No 5th deviation class anywhere** — §10.9 (UNREACHED) and §10.8 (Reuse-Miss) are both explicitly
  finding-modifiers, not classes; `deviation_count_by_class` keeps exactly four keys
  (`authorized`, `necessary`, `drift`, `regression`, §9.1 lines 701–704). Verified consistent; no stale 5th-class
  reference found.

## Summary

The six canonical contract fields (verbatim, SKILL.md §9.1 lines 731–736, `contract_version: "1.6.0"`):
`runtime_surface_requirements`, `runtime_surface_sweep_ran`, `runtime_surface_ledger_path`,
`runtime_surface_unreached`, `runtime_surface_degraded`, `unreached_surfaces`. They are emitted under a
MANDATORY-EMISSION rule (all six, exact names, on REACHED/DEGRADE/UNREACHED alike) with the count invariant
`len(unreached_surfaces) == runtime_surface_unreached` (lines 721–730) — this is the "deterministically
written" guarantee.

Three consumer surfaces exist:
- **A — §5.3 in-skill pre-filter (GATING):** reads `runtime_surface_unreached`; `≥ 1` from a successful sweep
  is a table-wide pre-filter forcing Tier 2 (line 402). The only consumer that actually executes today.
- **B — §9.3 UC-2 advisory row (NON-GATING):** all six fields advisory to external UC-2 consumers; additive
  at 1.6.0, read-and-ignore forward-compatible (lines 890, 905).
- **C — `sprint run` executor.py (SPEC-ONLY, NOT IMPLEMENTED):** §9.3 line 885 declares it a return-contract
  consumer keyed on `status` / `per_task_verdicts[].*` / `deviation_class` / `budget_forced_tier_downgrade`,
  with `deviation_class == regression` → TurnLedger rollback. In reality `executor.py` imports `TurnLedger`
  (line 42) for budget enforcement only and reads NO reflect contract; `runtime_surface` appears in zero
  Python files.

UNREACHED is **not a 5th deviation class** (§10.9, lines 1055–1065): it maps onto the existing four by a
totally-ordered rule (DEGRADE→Grounding Gap; contradiction→Regression; unmapped→Drift; Regression wins ties),
incrementing only `deviation_count_by_class.regression`/`.drift` — never a new counter, never
`verification_regressions_detected`.

**Central finding for the TDD task:** the acceptance criterion "the sprint executor reads the deterministic
scalars" is currently UNMET — `cli/sprint/executor.py` does not read the reflect return-contract at all. The
determinism guarantee presently protects only the in-skill §5.3 consumer and any future/spec sprint
integration.
