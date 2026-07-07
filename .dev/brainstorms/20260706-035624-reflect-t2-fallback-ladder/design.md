---
title: Reflect Tier-2 Fallback Model Ladder — Grounded Component Design
type: component-design
domain: architecture
status: revised-post-reflect
source_requirements: ./merged-requirements.md
created: 2026-07-06
revised: 2026-07-06
revision_note: "Closed reflect --mode pre findings F1-F7: slot-name fallback routing (F1), stamp/output seam (F2), openai_compat read_env_for_pool (F3), shared run-deadline wall-clock (F4), contract.py-vs-ensemble.py split (F5), first-match degraded reason (F6), tests/cli paths (F7)."
target_root: /config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/
---

# Reflect Tier-2 Fallback Model Ladder — Grounded Component Design

This design takes the accepted `merged-requirements.md` narrative and grounds it
against the **actual current code** in `src/superclaude/cli/reflect/` and
`src/superclaude/cli/swarm/`. Where the requirements described abstract
vocabulary, this document maps it onto the real function signatures, the real
`WorkerStatus` enum, and the exact insertion seam.

`/sc:design` scope: architecture + component + contract specification. It stops
at implementation-ready interfaces. Building it is `/sc:implement`.

---

## 1. Central Architectural Finding (drives the whole design)

The reflect verdict gate (`contract.derive_verdict`) is **already agnostic to how
the reviewer set was assembled**. It reads only these derived facts:

| Gate trigger (contract.py) | Field | Derived in | From |
|---|---|---|---|
| `degraded-tier1` (T6) | `tier_reached` | `build_reflect_contract` L584 | `reviewer_count >= 2` |
| `degraded-model-diversity` (T7) | `t2_model_class_diversity` | `compute_model_class_diversity` L641 | distinct `model_id` of successes |
| `single-vendor` (T8) | `t2_vendor_diversity` | `compute_vendor_diversity` L651 | distinct vendors of successes |
| `single-reviewer-fallback` (T10) | `merge_method` | `build_reflect_contract` L585 | `reviewer_count >= 2` |

Every one of these is computed from the **list of successful `WorkerResult`s**
passed into `build_reflect_contract` (`ensemble.py:553`, the `succeeded` filter at
L579).

> **Therefore the fallback controller does not touch `contract.py` at all.** If it
> appends successful fallback `WorkerResult`s to `normalized_workers` *before*
> `build_reflect_contract` runs, `reviewer_count`, both diversity axes, and
> `merge_method` recompute over the augmented set automatically, and the unchanged
> verdict chain certifies Tier-2 on its own existing rules. This is what makes the
> requirements' non-negotiable "verdict honesty" (§Non-Negotiable Semantics #6)
> structurally guaranteed rather than a promise to be re-verified per field.

This finding is the load-bearing simplification. The rest of the design protects
it.

---

## 2. Exact Insertion Seam

`run_tier2_ensemble` (`ensemble.py:171`) is the only function that changes in the
driver. The seam is **between L225 and L226**:

```text
ensemble.py:210  worker_results   = dispatch_wave1(...)                 # primary fan-out
ensemble.py:216  stamped_workers  = _stamp_worker_paths(...)
ensemble.py:217  normalized_workers = normalize_wave2(...)              # salvage runs here
                 ────────────────────────────────────────────────────  ◄── INSERT CONTROLLER
ensemble.py:226  succeeded_final_paths = [... normalized_workers ...]   # everything below
ensemble.py:239  swarm_contract   = reduce_wave3(normalized_workers,...)#   consumes the
ensemble.py:259  adversarial      = run_adversarial_scorer(...)         #   augmented list
ensemble.py:308  contract         = build_reflect_contract(normalized_workers, ...)
```

Placing the controller here satisfies requirements §"Why Post-Primary Top-Up
Wins": `dispatch_wave1`'s retry matrix and `normalize_wave2`'s salvage have both
already run, so an outcome reaching the controller is genuinely terminal. It also
means fallback successes flow through the **same** `reduce_wave3` merge, the
**same** adversarial scorer, and the **same** contract builder as primaries — the
requirements' "fallback successes pass the same normalization contract" (AC #8)
falls out of reusing the existing pipeline rather than a parallel one.

### 2.1 Augmented driver shape (pseudocode, not implementation)

```python
# run-level wall-clock deadline captured BEFORE primary dispatch (F4, §7.4)
deadline = _monotonic() + config.timeout_seconds if config.timeout_seconds else None

normalized_workers = normalize_wave2(...)          # unchanged, ends at L225

# ── NEW: post-primary quorum top-up controller ──
if _fallback_enabled(config):
    # NOTE (GAP-2 correction): there is NO `swarm_config` at this seam —
    # run_tier2_ensemble receives only ReflectConfig + env. Resolve the T1
    # factory from `env` INTERNALLY, exactly like resolve_t2_transport_factory
    # does for T2 (ensemble.py:139-167 → swarm _resolve_run_transport_factory
    # calls read_env(env) internally; base_url/api_key never surface). The
    # resolver reads the T1 env pool (read_env_for_pool with T1Proxy*/T1Model0)
    # and returns a slot-NAME-keyed factory (§4.3.1, F1); pool/creds are NOT
    # passed in from a swarm_config that doesn't exist here.
    fb_factory = resolve_t1_fallback_factory(      # sibling of resolve_t2_transport_factory
        config.transport,
        ladder=config.tier2_fallback_ladder,
        env=env,                                   # already in scope
    )
    ladder_outcome = run_fallback_ladder(
        primaries=normalized_workers,
        config=config,
        transport_for_fallback_slot=fb_factory,    # slot-name keyed, NOT positional
        prompt=worker_prompt,                      # identical reviewer brief
        swarm_output_dir=swarm_output_dir,         # fallback artifacts stamped here (F2)
        dispatch=dispatch_wave1,                   # injected for test-stubbing
        normalize=normalize_wave2,                 # fallback output salvaged identically
        stamp=_stamp_worker_paths,                 # injected for test-stubbing (F2)
        deadline_monotonic=deadline,               # run-level wall-clock bound (F4)
        env=env,
    )
    normalized_workers = ladder_outcome.contributing_workers  # primaries + fb successes
    fallback_metadata  = ladder_outcome.metadata              # for the contract
else:
    fallback_metadata = None

succeeded_final_paths = [...]                       # unchanged from L226 down
...
contract = build_reflect_contract(
    normalized_workers, ...,
    t2_fallback=fallback_metadata,                  # NEW additive kwarg (default None)
)
```

`build_reflect_contract` (which lives in **`ensemble.py:552`**, not `contract.py`)
gains exactly one new keyword-only parameter, `t2_fallback: dict | None = None`,
defaulted so every existing call site and test stays valid (mirrors how
`reviewer_isolation`/`audit_tree_dirty` were threaded). When present it is emitted
verbatim under a top-level `t2_fallback:` contract key. **No verdict field, and no
`contract.py` verdict-mapping code, is added or changed** — see §6 and the §10
change map for the exact `ensemble.py`-vs-`contract.py` split.

---

## 3. Status Vocabulary — Grounding Correction

The requirements' §"Attempt Classification" table lists 11 outcome tokens
(`transport_retry_exhausted`, `schema_invalid_terminal`, `config_invalid`,
`cancelled_or_aborted`, `blocked_precondition`, …). **The runtime does not have
these.** The real vocabulary is:

```python
# swarm/models.py:69
WorkerStatus = Literal["success", "timeout", "parse_error", "proxy_error"]
```

The controller classifies against these four (post-`normalize_wave2`, so
salvage has already promoted recoverable `parse_error → success` per the §7.4
salvage policy):

| Real `WorkerResult.status` | Counts toward quorum? | Fallback-eligible? | Maps to requirements row |
|---|---:|---:|---|
| `success` | yes | no | `success_normalized` / `success_salvaged` (salvage already applied) |
| `timeout` | no | yes | `timeout_terminal` |
| `proxy_error` | no | yes | `proxy_error_terminal` / `transport_*` |
| `parse_error` | no | yes | `parse_error_terminal` / `schema_invalid_terminal` (only reaches controller if salvage failed) |

The requirements' non-`WorkerResult` rows are handled **before** the controller is
ever reached, and the design must not invent a status enum to represent them:

| Requirements row | Where it actually lives | Controller behavior |
|---|---|---|
| `config_invalid` | `_resolve_run_transport_factory` raises `TransportEnvError` / `ModelPoolTooSmallError` at **factory build** (commands.py:612) | Never enters controller; if the *fallback* factory raises, controller records terminal `fallback_config_missing` |
| `cancelled_or_aborted` | process/orchestration layer above `run_tier2_ensemble` | Never enters controller |
| `blocked_precondition` | reflect runner preflight / isolation gate, before ensemble | Never enters controller |

**Design rule:** the controller's classifier is a pure function over the 4-value
`WorkerStatus`; it must not introduce a richer status enum on `WorkerResult`
(that would ripple into `__post_init__` validation, the swarm schema, and the
round-trip suite). The richer *semantics* live only in the fallback metadata's
`failure_class` field, which is free-form telemetry, never a `WorkerResult`
status.

```python
FALLBACK_ELIGIBLE_STATUSES = frozenset({"timeout", "proxy_error", "parse_error"})

def is_fallback_eligible(worker: WorkerResult) -> bool:
    return worker.status in FALLBACK_ELIGIBLE_STATUSES  # success excluded
```

---

## 4. New Component: `reflect/fallback.py` (pure helpers)

Per requirements §"Module and File Surface" ("prefer pure helper functions
first"). All functions are pure and side-effect-free **except** `run_fallback_ladder`,
which is the only one that dispatches — and it dispatches through injected
`dispatch`/`normalize` callables so unit tests never hit a transport.

### 4.1 Data types

```python
@dataclass(frozen=True)
class FallbackDecision:
    """Output of the pure planner: whether to dispatch, which slot, why."""
    action: Literal["dispatch", "certified", "degraded"]
    slot: str | None                 # "T1Model01" | "T1Model02" | None
    reason: str                      # terminal_reason enum token (see §6)

@dataclass(frozen=True)
class QuorumState:
    """Pure snapshot of the current contributing set vs the Tier-2 gate."""
    reviewer_count: int
    model_class_diversity: str       # reuse ensemble.compute_model_class_diversity
    vendor_diversity: str | None     # reuse ensemble.compute_vendor_diversity
    satisfies_tier2: bool            # count>=2 AND mcd=="full" AND vendor=="multi"
                                     #   (allow_single_vendor relaxes the vendor term)

@dataclass(frozen=True)
class LadderOutcome:
    contributing_workers: list[WorkerResult]   # primaries + selected fb successes
    attempt_ledger: list[dict]                 # every attempt, audit-oriented (§5)
    metadata: dict                             # the t2_fallback: contract block (§6)
```

### 4.2 Pure functions (100% unit-testable, no I/O)

```python
def classify_outcomes(workers: list[WorkerResult]) -> tuple[list, list]:
    """Split into (successes, fallback_eligible_failures) over WorkerStatus."""

def evaluate_quorum(
    workers: list[WorkerResult], *, allow_single_vendor: bool
) -> QuorumState:
    """Reuse ensemble.compute_model_class_diversity + compute_vendor_diversity.
    satisfies_tier2 encodes the SAME predicate the verdict chain will apply."""

def plan_next_attempt(
    quorum: QuorumState,
    eligible_failures: list[WorkerResult],
    attempts_made: list[str],          # ["T1Model01", ...]
    ladder: tuple[str, ...],           # ("T1Model01", "T1Model02")
    *,
    fallback_available: dict[str, bool],   # slot -> configured?
    wall_clock_ok: bool,
) -> FallbackDecision:
    """The state machine of requirements §"Transition Rules", as one pure
    function. Implements the F1/F2 escalation rules literally:
      - certified when quorum.satisfies_tier2
      - dispatch T1Model01 when >=1 eligible failure, quorum unmet, slot free
      - escalate to T1Model02 when: >1 terminal primary failure, OR the prior
        T1Model01 attempt failed, OR T1Model01 succeeded but did not repair
        quorum/diversity
      - degraded (with a specific reason) when the ladder is exhausted,
        a slot is unconfigured, or wall-clock is spent.

    ORDERING INVARIANT (closes the dispatch-vs-escalate ambiguity): the ladder is
    SEQUENTIAL — `T1Model01` is ALWAYS the first fallback dispatched (at most one
    attempt) whenever quorum is unmet and slot 0 is free and un-attempted, EVEN
    when >1 primary failed. The ">1 terminal primary failure" condition permits
    the SECOND (`T1Model02`) attempt AFTER `T1Model01` has run and quorum is still
    unmet; it never skips `T1Model01`. Concretely `plan_next_attempt` keys off
    `attempts_made`: if `"T1Model01" not in attempts_made` and quorum unmet and a
    fallback-eligible failure exists → dispatch `T1Model01`; only once
    `"T1Model01" in attempts_made` (regardless of its success) and quorum is still
    unmet does the T1Model02 branch evaluate. A unit test MUST cover the
    first-pass-with-2-primary-failures case and assert it dispatches `T1Model01`
    first (not `T1Model02`)."""

def select_contributing_set(
    primaries: list[WorkerResult],
    fallback_successes: list[WorkerResult],
    *, allow_single_vendor: bool,
) -> list[WorkerResult]:
    """Requirements §"Contributing Reviewer Set" selection order:
      1. successful primaries in slot order
      2. successful fallbacks in ladder order
      3. smallest set satisfying count + model-class + vendor diversity
      4. prefer more primaries on ties
      5. deterministic slot order otherwise."""
```

### 4.3 The one impure function

```python
def run_fallback_ladder(
    *,
    primaries: list[WorkerResult],
    config: ReflectConfig,
    transport_for_fallback_slot: FallbackTransportFactory,  # slot-NAME keyed (see §4.3.1)
    prompt: str,
    swarm_output_dir: Path,                   # where fallback artifacts are stamped (F2)
    stamp: Callable,                          # REQUIRED (no module-level default — see note)
    dispatch: Callable = dispatch_wave1,      # injected for tests; dispatch.py is a leaf swarm module (no cycle)
    normalize: Callable = normalize_wave2,    # injected for tests; normalize.py is a leaf swarm module (no cycle)
    deadline_monotonic: float | None = None,  # run-level wall-clock deadline (F4)
    env: Mapping[str, str] | None = None,
) -> LadderOutcome:
    """Loop: evaluate_quorum -> plan_next_attempt -> (dispatch one slot ->
    STAMP -> normalize) -> repeat, bounded by max_attempts and wall clock.
    Dispatches ONE fallback slot per iteration (a 1-worker WorkerSpec), so
    each T1 attempt reuses the identical reviewer brief + normalize recipe as
    primaries. Builds the attempt ledger and metadata, then calls
    select_contributing_set for the final worker list.

    Per-attempt flow (F2 — mirrors the primary seam order at ensemble.py:216-225,
    which stamps BEFORE normalize):
        raw = dispatch(preflight_1, transport_for_slot=slot_factory,
                       prompt=prompt, worker_spec=WorkerSpec(count=1, ...))
        stamped = stamp(raw, swarm_output_dir / f"fallback-{slot_name}")
        normalized = normalize(stamped, REFLECT_REVIEW_RECIPE, recipe_args={...})
    so every fallback worker carries a stable raw_path/meta_path/final_path before
    it can be selected into the contributing set, reduce_wave3, or the adversarial
    scorer. The per-attempt WorkerSpec inherits config.timeout_seconds — the SAME
    per-worker timeout/retry contract as primaries (requirements §Interaction with
    Existing Retry Matrix, merged-requirements.md:412,435)."""
```

Dispatching one slot at a time (a `WorkerSpec(count=1, ...)`) keeps
"at most one `T1Model01` attempt, at most one `T1Model02` attempt" (requirements
§Bounds) mechanically true and makes the state machine a simple bounded loop
rather than a batch.

### 4.3.1 Fallback slot resolution — the T1Model02 escalation guarantee (F1)

**Problem the naive seam hits.** `dispatch_wave1` builds tasks indexed
`0..workers_requested-1` (`dispatch.py:464-471`) and hands that local `slot_index`
to the factory (`dispatch.py:453-459`); the existing resolver maps it through
`pool[slot_index % len(pool)]` (`commands.py:691-692`). A one-worker fallback
`WorkerSpec(count=1)` therefore always passes `slot_index == 0`, so a naive second
fallback attempt would re-select **pool index 0 (`T1Model01`) again** and the
`T1Model02` escalation (AC #2/#3/#4) would never be mechanically reachable.

**Design rule.** The ladder MUST resolve fallback transport by **ladder-slot
NAME**, not by the positional `slot_index` the one-worker dispatch emits. The
name→model binding is built by the env-reading resolver `resolve_t1_fallback_factory`
(§7.3, sibling of `resolve_t2_transport_factory`), which reads the T1 env pool
INTERNALLY — the pool + proxy creds are NOT passed in from a `swarm_config`
(there is none at the ensemble seam; see the §2.1 GAP-2 note). `make_fallback_slot_factory`
is the pure slot-NAME binding helper the resolver uses once it has the pool:

```python
FallbackTransportFactory = Callable[[str], Transport]   # keyed by "T1Model01" | "T1Model02"

def make_fallback_slot_factory(
    pool: tuple[str, ...],                 # T1Model0N pool from read_env_for_pool(env)
    ladder: tuple[str, ...],               # ("T1Model01", "T1Model02")
    build_transport: Callable[[str], Transport],   # closes over base_url/api_key from read_env_for_pool
) -> FallbackTransportFactory:
    """Bind each ladder slot NAME to a distinct pool model by ladder position.
    ladder[0] -> pool[0] (T1Model01), ladder[1] -> pool[1] (T1Model02).
    Raises fallback_config_missing (caught by the controller) if the pool is
    too small to cover the ladder position being attempted. The proxy creds live
    in `build_transport`'s closure (read once via read_env_for_pool), never as
    loose params — mirrors how the T2 resolver caches OpenAICompatTransport."""
```

Each fallback iteration calls `transport_for_fallback_slot(slot_name)` with the
slot NAME chosen by `plan_next_attempt`, so `T1Model02` binds to `pool[1]`
regardless of the local `slot_index == 0` the one-worker dispatch emits. This is
the concrete resolution of AC #2/#3/#4: escalation selects a genuinely different
model. A unit test MUST assert the second fallback attempt resolves the
`T1Model02`→`pool[1]` model, not `pool[0]` a second time (§9 row "plan").

---

## 5. Two Views: Attempt Ledger vs Contributing Set

The requirements' two-view model maps directly onto the existing `WorkerResult`
type — **no new worker fields**. Provenance that the ledger needs but
`WorkerResult` doesn't carry (role, fallback_for, fallback_reason) lives in the
**metadata dict**, keyed by a synthetic `attempt_id`, not on the dataclass:

```yaml
# emitted under contract["t2_fallback"]["reviewer_attempts"]
reviewer_attempts:
  - attempt_id: primary:00           # role:index — derived from WorkerResult.index
    role: primary
    model_id: <worker.model_id>      # real field
    vendor: <_vendor_from_model_id>  # reuse ensemble helper
    status: success                  # real WorkerStatus
    contributes_to_quorum: true
  - attempt_id: primary:02
    role: primary
    status: parse_error
    failure_class: parse_error       # telemetry only, NOT a WorkerStatus
    contributes_to_quorum: false
  - attempt_id: fallback:T1Model01
    role: fallback
    fallback_for: [primary:02]
    fallback_reason: primary_terminal_failure
    status: success
    contributes_to_quorum: true
```

`contributing_reviewer_attempt_ids` is the subset chosen by
`select_contributing_set`. `reviewer_count`/diversity/`merge_method` derive from
that subset (which is literally the `normalized_workers` list handed to
`build_reflect_contract`), never from the full ledger. This satisfies contract
test "`reviewer_count` equals contributing count, not attempt count."

---

## 6. Contract Additions (additive only)

`build_reflect_contract` emits one new top-level key. **No existing key changes
type or meaning; no `_LOAD_BEARING_BOOL_FIELDS` member is added** (so the
malformed-boolean BLOCKED guard at contract.py:206 is unaffected).

```yaml
t2_fallback:
  enabled: true
  policy_version: reflect-t2-fallback-ladder-v1
  strategy: post_primary_quorum_top_up
  ladder: [T1Model01, T1Model02]
  engaged: true
  certified_with_fallback: true
  fallback_attempt_count: 1
  exhausted: false
  terminal_reason: certified_t2_with_fallback
  original_primary_pool_fully_succeeded: false
  reviewer_attempts: [...]                 # the ledger (§5)
  contributing_reviewer_attempt_ids: [...]
  primary_failures_preserved: [primary:02] # visible even when fallback certifies
  tier2_certification_basis: primary_plus_fallback_quorum  # source-recommended field
```

`tier2_certification_basis` (source: `merged-requirements.md:350`) is emitted as
an explicit enum so consumers get the certification basis without inferring it
from `certified_with_fallback` + `original_primary_pool_fully_succeeded`. Values:

```text
primary_only_quorum            # primaries alone certified; no fallback engaged
primary_plus_fallback_quorum   # ≥1 fallback contributed to the certifying set
not_certified                  # degraded — Tier-2 not reached
```

**Source-metadata reconciliation (F-coverage).** The source ledger example
(`merged-requirements.md:185-216`) also shows `model_slot`, `retry_count`, and
`normalization` per attempt. These are **illustrative, not required**: `model_slot`
is redundant with `attempt_id` (`role:slot` already encodes it), and `retry_count`
/`normalization` are per-worker internals the current `WorkerResult` does not
surface as stable fields. v1 emits `attempt_id` / `role` / `model_id` / `vendor` /
`status` / `failure_class` / `fallback_for` / `fallback_reason` /
`contributes_to_quorum` (§5) and deliberately OMITS `model_slot` /`retry_count`/
`normalization` to avoid widening `WorkerResult`. The source enum item
`aborted_or_cancelled` (`merged-requirements.md:364`) is intentionally NOT in the
`terminal_reason` set below because cancellation is handled **before** the
controller (§3, `cancelled_or_aborted` never enters the controller) — it is
out-of-scope-by-architecture, not silently dropped.

`terminal_reason` enum (grounded to the real degraded paths):

```text
not_needed_primary_quorum_met      # controller no-op; primaries already certify
certified_t2_with_fallback         # a fallback contributed to quorum
fallback_config_missing            # fallback factory raised TransportEnvError/pool-too-small
fallback_pool_exhausted            # the WHOLE ladder was attempted (all slots) and quorum still unmet
fallback_wall_clock_exhausted      # bounded_by_reflect_run_budget hit
fallback_attempts_failed           # the attempts that RAN all terminal-failed but the ladder was NOT
                                    #   fully exhausted (e.g. max_attempts < len(ladder) truncated it)
diversity_unrepairable             # successes exist but model/vendor diversity can't reach full/multi
no_fallback_eligible_primary_failure  # quorum short for a non-fallback reason
```

**`fallback_pool_exhausted` vs `fallback_attempts_failed` precedence (disambiguation).**
For the default `ladder=(T1Model01, T1Model02)` with `max_attempts=2`, "both slots
attempted and still short" is `fallback_pool_exhausted` (the ladder is fully
exhausted). `fallback_attempts_failed` is RESERVED for the case where the attempts
that ran all terminal-failed but the ladder was NOT fully walked — i.e. a config
where `max_attempts < len(ladder)` truncates the ladder before its last slot. The
§8 counter-case (both fallbacks fail on the default 2/2 ladder) therefore reports
`fallback_pool_exhausted`, NOT `fallback_attempts_failed`. `plan_next_attempt`
applies this precedence: full-ladder-walked → `fallback_pool_exhausted` wins.

**Verdict interaction (the honesty guarantee, restated concretely):** when the
controller ends `degraded`, it does **not** set any degraded field itself. It
simply leaves the contributing set short, and the *existing unchanged* triggers
fire on their own. `_degraded_reason` (`contract.py:265-293`) is **first-match**:
it returns the FIRST trigger slug in its fixed order, not a set. So the verdict
reason for each degraded shape is exactly:
- fewer than 2 successes → `reviewer_count < 2` → `tier_reached == 1` →
  first-match **`degraded-tier1`** (T6). The contract still ALSO carries
  `merge_method == "single-reviewer-fallback"` (the T10 field), but T6 fires
  first in the chain, so `single-reviewer-fallback` is NOT the returned verdict
  reason in this shape — it is a contract field, not the verdict slug. Tests/
  telemetry MUST assert `degraded-tier1` as the reason, and MAY assert
  `merge_method` as a field, but MUST NOT assert both as the verdict reason.
- 2 successes, same model_id → `t2_model_class_diversity != "full"` →
  **`degraded-model-diversity`** (T7).
- 2 successes, same vendor (distinct model_ids) → `t2_vendor_diversity ==
  "single"` → **`single-vendor`** (T8, unless `--allow-single-vendor`). Note T7
  precedes T8 in the chain, so a same-vendor pair that is ALSO same-model_id
  reports `degraded-model-diversity`, not `single-vendor`.

The `t2_fallback.terminal_reason` is **explanatory telemetry riding alongside**
the real first-match degrade reason, never the gate.

---

## 7. Config Surface

### 7.1 swarm/config.py — add the T1 slot family (parallel to T2)

The only swarm change: a fallback-pool env contract mirroring the T2 one
(config.py:51-63). Additive constants + one collector; `SwarmConfig` gains one
frozen field with an empty-tuple default so `from_env` stays total.

```python
# NEW constants alongside T2_MODEL_ENV_PREFIX
T1_MODEL_ENV_PREFIX = "T1Model0"      # T1Model01..T1Model0N fallback pool
T1_MODEL_MAX_SLOTS  = 9

# NEW frozen field (default () keeps every existing constructor call valid)
t1_models: tuple[str, ...] = ()

# from_env: t1_models = cls._collect_models(env_map, T1_MODEL_ENV_PREFIX, T1_MODEL_MAX_SLOTS)
```

`_collect_t2_models` should be generalized to
`_collect_models(env_map, prefix, max_slots)` and called twice — avoids a
copy-paste divergence between the two pools. This is the "model-slot resolution
capability, not a global fallback policy" split from requirements §"Swarm
Awareness": swarm learns *how to resolve* `T1Model0N`; it learns nothing about
*when* to use them.

### 7.2 reflect policy wrapper (reflect-owned)

The *when* lives in reflect. Add to `ReflectConfig` (models.py:57) as defaulted
fields so all existing construction sites stay valid:

```python
tier2_fallback_enabled: bool = True
tier2_fallback_ladder: tuple[str, ...] = ("T1Model01", "T1Model02")
tier2_fallback_max_attempts: int = 2
```

(A `--no-tier2-fallback` CLI flag flips `tier2_fallback_enabled` for the
credit-free / deterministic lane; `--transport stub` should default fallback OFF
since the stub pool already certifies.)

### 7.3 Fallback transport resolution (F3 — three files, not two)

The controller needs a **single-slot** factory for `T1Model01`/`T1Model02`,
analogous to `_resolve_run_transport_factory` but reading the `T1Model0N` pool.
Grounding correction: the current transport env reader
(`swarm/transports/openai_compat.py:read_env`) is **hard-coded to T2** — it
imports only `T2_MODEL_ENV_PREFIX` / `T2_PROXY_URL_ENV` / `T2_PROXY_KEY_ENV`
(`openai_compat.py:98-103`) and reads only those + `T2Model0N`
(`openai_compat.py:159-196`), raising a T2-specific `TransportEnvError`. So this
work touches **three** swarm files, not two:

1. `swarm/config.py` — add `T1Model0N` constants + `t1_models` field (§7.1).
2. `swarm/transports/openai_compat.py` — make the env reader **pool-parameterized**
   so it can read either pool without a T2/T1 fork. Recommended shape:

   ```python
   # generalize read_env to accept the model prefix + proxy env names; keep a
   # thin read_env() wrapper bound to the T2 constants so EVERY existing caller
   # and test stays byte-valid (additive, mirrors the config _collect_models split).
   def read_env_for_pool(
       *, model_prefix: str, max_slots: int,
       proxy_url_env: str, proxy_key_env: str,
       env: Mapping[str, str] | None = None,
   ) -> TransportConfig: ...
   def read_env(env=None) -> TransportConfig:          # unchanged public signature
       return read_env_for_pool(model_prefix=T2_MODEL_ENV_PREFIX,
           max_slots=T2_MODEL_MAX_SLOTS, proxy_url_env=T2_PROXY_URL_ENV,
           proxy_key_env=T2_PROXY_KEY_ENV, env=env)
   ```

3. `swarm/commands.py` — parameterize `_resolve_run_transport_factory` on the
   env prefix/pool (or add `_resolve_fallback_transport`) so the
   `ModelPoolTooSmallError`/`TransportEnvError` guards are inherited by the T1
   path. If the T1 pool is unset, the resolver raises at build time and the
   controller catches it into `terminal_reason: fallback_config_missing` — never
   a stack trace.

**No proxy keys are ever surfaced** — the resolver binds the proxy key internally
and emits only `model_id` (AC #12; contract test asserts absence in dumped YAML).

**Proxy binding decision (resolved by env grounding — supersedes the earlier
T2-reuse default).** Environment grounding for this project (read of env-var
NAMES only, values never read per `feedback_aienv_only_proxy_contract`) shows a
**dedicated T1 proxy contract exists**: `T1ProxyUrl`, `T1ProxyKey`, `T1Model01`,
`T1Model02` are all present as distinct names. Therefore the governing binding is:

```python
read_env_for_pool(model_prefix="T1Model0", max_slots=T1_MODEL_MAX_SLOTS,
                  proxy_url_env="T1ProxyUrl", proxy_key_env="T1ProxyKey")
```

NOT the `T2ProxyUrl`/`T2ProxyKey` reuse the first draft assumed. The `read_env_for_pool`
shape (F3) parameterizes the proxy-env names, so this is a call-site argument
choice, not a fork. **Because the fallback slots ride a separate proxy contract,
`/sc:implement` MUST treat wiring *real* fallback dispatch as a `needs_human_decision`
HALT** (rollout step 5): confirm — read-only, names only, no `:4000/v1` probe — that
`~/.aienv`/env exposes `T1ProxyUrl`/`T1ProxyKey`/`T1Model01`, record the binding
decision, and proceed; if unconfirmed, write a PENDING Open-Question and HALT
rather than falling back to the T2 arm. Stub-transport work (rollout steps 1–4)
does not depend on this and proceeds. (This paragraph governs; the two `read_env_for_pool`
examples above in this section that still show `T2_PROXY_*` are illustrative of the
*generalized reader shape*, not the binding to wire.)

### 7.4 Wall-clock accounting (F4 — decided, not deferred)

AC #6 requires fallback attempts to be bounded by BOTH attempt count AND
wall-clock policy (`merged-requirements.md:638`; `aggregate_wall_clock_policy:
bounded_by_reflect_run_budget`, `merged-requirements.md:405`). The in-process
Tier-2 route has **no outer `ClaudeProcess` timeout** around the ensemble — it
calls `run_tier2_ensemble` directly and sets `rc = 0` afterward
(`runner.py:508-513`); `WorkerSpec.timeout_sec = config.timeout_seconds` is a
**per-worker** bound only (`ensemble.py:207-215`). So sequential fallback attempts
would extend total wall time unbounded unless a run-level bound is added.

**Decision (v1): shared run deadline, not a separate fallback budget.** Capture a
monotonic deadline ONCE at the top of `run_tier2_ensemble`, before primary
dispatch:

```python
deadline = _monotonic() + config.timeout_seconds if config.timeout_seconds else None
```

Thread it into `run_fallback_ladder(deadline_monotonic=deadline)`. Before dispatching
each fallback attempt, the loop computes `remaining = deadline - _monotonic()`
(when `deadline` is not None) and:

- if `remaining <= 0` (or below a small floor, e.g. one per-worker timeout), it
  does NOT dispatch; it stops with `terminal_reason: fallback_wall_clock_exhausted`
  and the existing degraded chain fires on the short contributing set;
- otherwise it dispatches the one-worker attempt with
  `timeout_sec = min(config.timeout_seconds, remaining)`, so a single fallback can
  never overrun the run deadline.

`deadline is None` (no configured timeout) means the wall-clock bound is inert and
only `max_attempts` bounds the ladder — the pure `plan_next_attempt` still receives
`wall_clock_ok` and this remains fully unit-testable by passing the flag directly.
This keeps the budget source single and unambiguous (the run's own
`config.timeout_seconds`), satisfying AC #6 without inventing a second budget knob.

---

## 8. Sequence — the 2026-07-05 incident, replayed

```text
primary dispatch_wave1  ─┬─ T2Model01 → proxy_error   (terminal after retry)
                         ├─ T2Model02 → success
                         └─ T2Model03 → parse_error    (salvage failed → terminal)
normalize_wave2 ─────────  (salvage runs; T2Model03 stays parse_error)
                         │
run_fallback_ladder ─────┤ evaluate_quorum: 1 success → NOT satisfies_tier2
                         │ plan: 2 eligible failures, slot T1Model01 free → dispatch
                         ├─ T1Model01 → success (distinct vendor)
                         │ evaluate_quorum: {T2Model02, T1Model01}
                         │   count=2, mcd=full, vendor=multi → satisfies_tier2 ✓
                         │ plan: certified → stop (T1Model02 NOT dispatched)
                         │ select_contributing_set → [T2Model02, T1Model01]
reduce_wave3 / adversarial / build_reflect_contract  over the 2-worker set
                         │
return-contract: tier_reached=2, reviewer_count=2, merge_method=adversarial,
                 status=success, verdict=PASS(exit 0)
                 t2_fallback.certified_with_fallback=true,
                 primary_failures_preserved=[primary:00, primary:02]
```

Counter-case (both fallbacks fail): contributing set stays `{T2Model02}` →
`reviewer_count=1` → `tier_reached=1` → **existing first-match** `degraded-tier1`
(T6) → exit 11. The contract also carries `merge_method=single-reviewer-fallback`
(T10 field) and `t2_fallback.terminal_reason=fallback_pool_exhausted`, but the
returned verdict reason is `degraded-tier1` (T6 precedes T10 in the first-match
chain). The gate degrades on its own rules; the fallback block only explains *why
it couldn't help*.

---

## 9. Test Surface (maps to requirements §Test Plan)

Test paths are grounded to the CURRENT layout (verified against the live tree):
reflect tests live under `tests/cli/reflect/` (see `tests/cli/reflect/conftest.py`)
but swarm tests live under **`tests/swarm/`** (NOT `tests/cli/swarm/`, which does
not exist; see `tests/swarm/conftest.py`). NOT a new `tests/reflect/` namespace.
Note: `tests/cli/reflect/test_contract.py` does NOT currently exist — the
verdict-unchanged regression assertions are added to the existing
`tests/cli/reflect/test_verdict_mapping.py` (which already drives `derive_verdict`
against `tests/cli/reflect/fixtures/*.yaml`, incl. `degraded_tier1.yaml`).

| Layer | File | What it pins |
|---|---|---|
| Unit: classify | `tests/cli/reflect/test_fallback_classify.py` | 4-value `WorkerStatus` → eligibility; salvaged `parse_error` is `success` (not eligible) |
| Unit: plan | `tests/cli/reflect/test_fallback_plan.py` | every §"Transition Rules" branch incl. T1Model01-success-but-diversity-short → escalate; **F1: second fallback attempt resolves `T1Model02`→pool[1], not pool[0] twice**; **F4: wall-clock-exhausted stops before dispatch** |
| Unit: select | `tests/cli/reflect/test_fallback_select.py` | smallest passing set, prefer-primaries, same-vendor/same-model insufficiency |
| Unit: slot factory | `tests/cli/reflect/test_fallback_slot_factory.py` | **F1** `make_fallback_slot_factory` binds slot NAME→pool position; pool-too-small raises → `fallback_config_missing` |
| Contract | `tests/cli/reflect/test_contract_fallback_metadata.py` | `reviewer_count`==contributing not attempts; `t2_fallback` never flips verdict; primary failures preserved; `tier2_certification_basis` correct; **no proxy keys** in dumped YAML |
| Verdict-unchanged regression | `tests/cli/reflect/test_verdict_mapping.py` (existing — extend) | must stay green with `t2_fallback=None` default — proves additive-only; **F6: degraded reason is first-match `degraded-tier1`, not both** (uses `degraded_tier1.yaml` fixture) |
| Stub integration | `tests/cli/reflect/test_ensemble_fallback_stub.py` | inject `dispatch`/`normalize`/`stamp` stubs; replay §8 incident + counter-case, no network; **F2: fallback workers carry stable final_path after stamp→normalize** |
| Swarm config | `tests/swarm/test_config.py` (existing — extend) | `T1Model0N` collection parallels `T2Model0N`; `t1_models` empty-tuple default |
| Swarm transport | `tests/swarm/test_openai_compat.py` (existing — extend) | **F3** `read_env_for_pool` reads a T1 pool; thin `read_env()` wrapper still passes existing T2 assertions (whole existing body is the regression harness) |

Injecting `dispatch`/`normalize` into `run_fallback_ladder` is what keeps the
stub-integration test transport-free and deterministic (aligns with the
memory note: test live producers top-level, but here the producer is a plain
CLI-lib call, stubbable in-process).

---

## 10. Module & File Change Map

| File | Change | Risk |
|---|---|---|
| `src/superclaude/cli/reflect/fallback.py` | **NEW** — pure helpers (`classify_outcomes`/`evaluate_quorum`/`plan_next_attempt`/`select_contributing_set`/`make_fallback_slot_factory`) + `run_fallback_ladder` | low (isolated, injectable) |
| `src/superclaude/cli/reflect/ensemble.py` | insert controller call at L225→226 seam; capture run deadline (F4); one new `t2_fallback=` kwarg on `build_reflect_contract` (which is DEFINED here, ensemble.py:552, NOT in contract.py) | medium (the driver) |
| `src/superclaude/cli/reflect/models.py` | 3 defaulted `ReflectConfig` fields (§7.2) | low (defaults) |
| `src/superclaude/cli/reflect/contract.py` | **none** — the verdict map (`derive_verdict`/`_degraded_reason`, `contract.py:265-293`) is unchanged. NOTE: `build_reflect_contract` is NOT in this file (it lives in `ensemble.py`); the earlier draft's "contract additions" refer to that `ensemble.py` builder, not to `contract.py`. | none |
| `src/superclaude/cli/reflect/commands.py` | `--no-tier2-fallback` flag wiring | low |
| `src/superclaude/cli/swarm/config.py` | `T1Model0N` constants + `t1_models` field + generalize `_collect_t2_models`→`_collect_models` | low (additive) |
| `src/superclaude/cli/swarm/transports/openai_compat.py` | **F3** — generalize `read_env`→`read_env_for_pool(model_prefix, max_slots, proxy_url_env, proxy_key_env)`; keep a thin T2-bound `read_env()` wrapper so all existing callers/tests stay valid | medium (shared env reader) |
| `src/superclaude/cli/swarm/commands.py` | parameterize `_resolve_run_transport_factory` on env prefix (or add `_resolve_fallback_transport`) | medium (shared with primary path) |
| `src/superclaude/cli/swarm/models.py` | **none** — no new `WorkerStatus`, no new `WorkerResult` field | none (deliberate, §3) |

`contract.py`'s **verdict map** and `swarm/models.py`'s **worker type** untouched
is the design's headline: the two structures that own verdict semantics and the
worker schema are exactly the ones that must not move. `build_reflect_contract`
(the contract *builder*) lives in `ensemble.py` and DOES gain the additive
`t2_fallback=` kwarg — that is not a `contract.py` change.

**Circular-import guard (F-review MEDIUM).** `reflect/fallback.py` reuses
`compute_model_class_diversity` / `compute_vendor_diversity`, which currently live
in `ensemble.py` — while `ensemble.py` imports `run_fallback_ladder` from
`fallback.py`. A top-level `ensemble → fallback → ensemble` cycle is likely.
Resolve at implementation by ONE of: (a) move the two diversity helpers into a
neutral `reflect/_diversity.py` (or reuse the swarm-side helpers) imported by both;
or (b) have `fallback.py` do a function-local `from .ensemble import ...` inside
`evaluate_quorum`. Option (a) is preferred (no local-import smell); the choice is
an implementation task, not an open design question.

---

## 11. Acceptance Criteria Traceability

| Requirements AC | Satisfied by |
|---|---|
| 1. single failure repaired by T1Model01 | §8 sequence; `plan_next_attempt` dispatch branch |
| 2. multi-failure escalates to T1Model02 | `plan_next_attempt` escalation (>1 terminal failure) |
| 3. T1Model01 terminal → T1Model02 | `plan_next_attempt` (prior attempt failed) |
| 4. T1Model01 success but diversity-short → T1Model02 | `plan_next_attempt` (succeeded-but-unrepaired) |
| 5. fallback never before retry+salvage | §2 seam is post-`normalize_wave2` |
| 6. bounded by attempts + wall clock | `run_fallback_ladder` loop bound; one-slot-per-iteration |
| 7. primary failures visible | `t2_fallback.primary_failures_preserved`; ledger keeps them |
| 8. fallback uses same normalize contract | reused `normalize_wave2` + reviewer `prompt` |
| 9. Tier-2 still needs 2 heterogeneous successes | unchanged `build_reflect_contract` + `derive_verdict` |
| 10. genuine failure stays degraded/exit 11 | §6/§8 counter-case — existing triggers fire |
| 11. metadata distinguishes primary-only vs fallback | `certified_with_fallback` + `original_primary_pool_fully_succeeded` |
| 12. no proxy keys | resolver emits only `model_id`; contract test asserts absence |

---

## 12. Rollout (unchanged from requirements §Rollout, verification commands verified against repo)

1. `reflect/fallback.py` pure helpers (incl. `make_fallback_slot_factory`, F1) +
   unit tests (§9 rows classify/plan/select/slot-factory).
2. Additive `build_reflect_contract(t2_fallback=…)` in `ensemble.py` + contract
   tests (metadata + verdict-unchanged regression rows).
3. Wire controller into `ensemble.py` behind `tier2_fallback_enabled`, capturing
   the run deadline (F4); stub transport first (stub-integration row).
4. `T1Model0N` swarm slot resolution: `swarm/config.py` collector + the
   `read_env_for_pool` generalization in `swarm/transports/openai_compat.py` (F3)
   + `swarm/commands.py` resolver parameterization + swarm config/transport tests.
5. Real fallback dispatch behind the flag; confirm `~/.aienv` exposes `T1Model0N`
   under the T2 proxy (§7.3 decision).
6. `--no-tier2-fallback` flag; docs for reflect reviewer behavior.

Verification (paths grounded to this worktree):

```
cd /config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback && uv run pytest tests/ -k "reflect or swarm"
cd /config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback && make sync-dev && make verify-sync
```

Source-of-truth: all edits land under `src/superclaude/`; `.claude/` is
sync-dev output and is never staged.

---

## 13. Open Items for `/sc:implement`

The reflect pre-execution review closed the design-level decisions; the remaining
items are implementation confirmations, not open design questions:

1. **Proxy binding for T1 slots** (§7.3) — **decided**: reuse the T2 proxy
   endpoint/key, vary only the `T1Model0N` model id. The single confirmation
   `/sc:implement` still owes: verify `~/.aienv` actually exposes `T1Model0N`
   model ids under that same proxy before wiring real dispatch (rollout step 5).
   If — and only if — `~/.aienv` proves a distinct T1 proxy contract, switch the
   `read_env_for_pool` proxy-env parameters to `T1ProxyUrl`/`T1ProxyKey` (the
   generalized reader already accepts them; no structural change).
2. **`_resolve_run_transport_factory` parameterization vs fork** (§7.3/§10) —
   **decided**: parameterize on env prefix/pool (thin parameter, not a copy) so
   the `ModelPoolTooSmallError`/`TransportEnvError` guards stay single-sourced.
   Implementation task, not an open question.
3. **Wall-clock accounting** (§7.4) — **decided**: a shared run deadline derived
   from `config.timeout_seconds` at the top of `run_tier2_ensemble`, threaded as
   `deadline_monotonic` and clamping each fallback attempt's `timeout_sec`. No
   separate fallback budget knob.
4. **Diversity-helper import cycle** (§10 change map) — pick option (a) neutral
   `reflect/_diversity.py` (preferred) vs (b) function-local import, at
   implementation time.
