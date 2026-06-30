# Research: run_log/models Patterns

Topic type: Patterns & Conventions
Scope: `src/superclaude/pr_submit/run_log.py` + `src/superclaude/pr_submit/models.py`
Status: Complete
Date: 2026-06-12

---

## SUMMARY (read first)

The V1.1 deltas slot into four well-isolated, mechanically simple patterns. Each existing
example is a literal you can mirror line-for-line:

1. **Add an idempotency set** → append a string to the `IDEMPOTENCY_SETS` tuple (run_log.py:27-33). Everything downstream auto-derives (init seeding, snapshot key, dedup membership) — EXCEPT the *fold* that populates it, which you write by hand in `rebuild_state()`.
2. **Add an `EventType` member + bump the count** → add a `NAME = "value"` line in the closed enum (models.py:19-70), then update **three** count-bearing strings: the class docstring (models.py:20 "EXACTLY 33"), the module docstring (models.py:3-4 "exactly 33 members"), and the `ValueError` message + append docstring in run_log.py:103-110 ("the 33 §11.3 events" / "one of the 33").
3. **Add a `SkillResult` field** → add a `name: type = default` line to the dataclass (models.py:166-187). Plain (non-frozen) `@dataclass`; mutable defaults use `field(default_factory=...)`, scalars use inline literals.
4. **Add a `rebuild_state` fold** → add an `elif et == EventType.X.value` branch inside the loop (run_log.py:162-187), using the matching fold idiom (append-to-set / increment / monotone-min).

Key correctness notes for the builder:
- `record_idempotent` returns **True = newly recorded (proceed)**, **False = already present (skipped, `idempotency_skip` appended)**. It does NOT mutate any set itself — membership is reconstructed via `rebuild_state()` each call (run_log.py:200-219). So the new `auggie_review_invoked` set only becomes non-empty once a `rebuild_state` fold writes into it.
- `_VALID_EVENT_VALUES` (run_log.py:35) is auto-derived from `EventType` — adding enum members needs NO change there; the guard widens automatically.
- The "min (monotone)" fold for `effective_max_rounds` has **no existing example** in `rebuild_state` (all current folds are append-to-set or `+= 1`). The builder must author a new idiom. See §4.3 below for the exact recommended form.
- Count assertion is enforced by a test (R5 details it); the enum count "EXACTLY 33" is documented in docstrings but the load-bearing gate is a test. Updating the enum WITHOUT updating that test count will fail CI.

---

## 1. run_log.py — IDEMPOTENCY_SETS pattern

### 1.1 Declaration (run_log.py:26-33)

```python
# The 5 idempotency sets (§11.4).
IDEMPOTENCY_SETS = (
    "processed_review_ids",
    "processed_finding_ids",  # keyed on fix_key
    "replied_comment_ids",
    "resolved_thread_ids",
    "pushed_commit_shas",
)
```

A module-level **tuple of strings**. The comment `# The 5 idempotency sets (§11.4).` carries the count — V1.1 must change `5` → `6` here too.

### 1.2 How it is CONSUMED (3 auto-derived sites — no manual change needed)

The tuple is the single source; three sites iterate it generically:

- **State seeding** (run_log.py:159): `**{s: [] for s in IDEMPOTENCY_SETS}` — every set initialized to an empty list in the state dict.
- **Working-set construction** (run_log.py:161): `sets = {s: set() for s in IDEMPOTENCY_SETS}` — a Python `set()` per name for fold accumulation.
- **Serialization** (run_log.py:188-189): `for s in IDEMPOTENCY_SETS: state[s] = sorted(sets[s], key=str)` — each accumulated set sorted (by `str`) back into the state dict as a list.

Adding `"auggie_review_invoked"` to the tuple automatically gives it: an empty-list seed, a working `set()`, and sorted serialization. **It will remain empty forever unless a fold in `rebuild_state` adds to `sets["auggie_review_invoked"]`** — see §4.2.

### 1.3 record_idempotent — first/repeat contract (run_log.py:200-219)

```python
def record_idempotent(self, set_name: str, key) -> bool:
    if set_name not in IDEMPOTENCY_SETS:
        raise ValueError(f"unknown idempotency set: {set_name!r}")
    state = self.rebuild_state()
    if str(key) in {str(k) for k in state.get(set_name, [])}:
        self.append({
            "event_type": EventType.IDEMPOTENCY_SKIP.value,
            "set": set_name,
            "key": str(key),
        })
        return False
    return True
```

Contract (matches the task brief's question exactly):
- **Returns `True`** when the key is NOT yet present → newly recorded / **action should proceed**.
- **Returns `False`** when the key IS already present → appends an `idempotency_skip` event and the action is **skipped**.
- Membership is checked by **stringified comparison** (`str(key) in {str(k) ...}`), so int and str keys interoperate.
- It validates `set_name in IDEMPOTENCY_SETS` first (raises `ValueError` otherwise) — so the new set name is accepted automatically once added to the tuple.
- IMPORTANT subtlety: `record_idempotent` does **not** itself persist the key into the set — it only emits the skip on a repeat. The set is populated by `rebuild_state` folding the *real* event (e.g. `fix_applied` → `processed_finding_ids`). So for `auggie_review_invoked` to ever return False on repeat, the V1.1 fold (AUGGIE_FALLBACK_INVOKED.pr_number → set) must land first.

---

## 2. run_log.py — append() / EventType validation (the `_VALID_EVENT_VALUES` guard)

### 2.1 The closed-enum guard (run_log.py:35, 100-122)

```python
_VALID_EVENT_VALUES = frozenset(e.value for e in EventType)   # line 35
...
def append(self, event: dict) -> dict:
    event_type = event.get("event_type")
    if event_type not in _VALID_EVENT_VALUES:
        raise ValueError(
            f"unknown event_type: {event_type!r} (not one of the 33 §11.3 events)"
        )
    self._event_id += 1
    record = {
        "schema_version": "1.0",
        "event_id": self._event_id,
        **_redact(event),
    }
    record.setdefault("timestamp", None)
    with self.jsonl_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")
        fh.flush()
        os.fsync(fh.fileno())
    return record
```

Patterns for the builder:
- `_VALID_EVENT_VALUES` is **auto-derived** from `EventType` at import (`frozenset(e.value for e in EventType)`). Adding the 4 new enum members **requires NO edit here** — the guard widens automatically.
- **BUT** the `ValueError` message hard-codes the count: `"not one of the 33 §11.3 events"` (run_log.py:109). V1.1 must update `33` → `37` here.
- The `append()` docstring (run_log.py:103-104) also says "not one of the 33 closed enum values" — update to `37`.

### 2.2 Write-ahead / fsync discipline (run_log.py:118-130)

Present and load-bearing:
- Every `append()` does `fh.write(... + "\n"); fh.flush(); os.fsync(fh.fileno())` (run_log.py:118-121) — durable before return.
- `write_ahead()` (run_log.py:124-130) is a thin alias of `append()` with identical durability, named distinctly to mark sites where the fsync MUST precede the external side effect (§11.1). New V1.1 events that gate a side effect should be emitted via `write_ahead`; pure bookkeeping events (e.g. recording a clamp that already happened) use `append`.
- `_event_id` is monotonic and resume-safe: on an existing log, `__init__` calls `_last_event_id()` (run_log.py:83-98) to continue the counter — no change needed for V1.1.

---

## 3. run_log.py — rebuild_state() fold idioms (run_log.py:145-190)

This is the most important section for V1.1: the existing folds are the templates to mirror.

### 3.1 State dict shape (run_log.py:152-160)

```python
state = {
    "pr_number": self.pr_number,
    "state": None,
    "round_counter": 0,
    "push_count": 0,
    "reply_count": 0,
    "last_event_id": 0,
    **{s: [] for s in IDEMPOTENCY_SETS},
}
sets = {s: set() for s in IDEMPOTENCY_SETS}
```

V1.1 SkillResult adds scalar counters/flags (`rereview_request_count`, `fallback_round_counter`, `effective_max_rounds`, etc.). If those must be rebuildable from JSONL, the builder should add matching keys to this `state` dict with their zero/None seeds (mirror `"round_counter": 0` and `"last_event_id": 0`). NOTE: not every SkillResult field is necessarily rebuilt here — only the ones the V1.1 spec (§6.3) says fold from events. The brief names three: `auggie_review_invoked` (set), `effective_max_rounds` (min), `rereview_request_count` (count).

### 3.2 The fold loop — three existing idioms (run_log.py:162-187)

```python
for ev in self.read_events():
    state["last_event_id"] = ev.get("event_id", state["last_event_id"])
    et = ev.get("event_type")
    if ev.get("state_after"):
        state["state"] = ev["state_after"]
    if et == EventType.ROUND_INCREMENTED.value:
        state["round_counter"] += 1                       # IDIOM A: increment (count)
    elif et == EventType.PUSH_COMPLETED.value:
        state["push_count"] += 1                          # IDIOM A: increment
        if ev.get("target_sha"):
            sets["pushed_commit_shas"].add(ev["target_sha"])   # IDIOM B: add-to-set
    elif et == EventType.REPLY_POSTED.value:
        state["reply_count"] += 1
        if ev.get("comment_id") is not None:
            sets["replied_comment_ids"].add(ev["comment_id"])
    elif et == EventType.THREAD_RESOLVED.value and ev.get("thread_id"):
        sets["resolved_thread_ids"].add(ev["thread_id"])  # IDIOM B (guard in the elif)
    elif (
        et == EventType.FINDINGS_NORMALIZED.value
        and ev.get("review_id") is not None
    ):
        sets["processed_review_ids"].add(ev["review_id"])
    elif et == EventType.FIX_APPLIED.value and ev.get("fix_key"):
        sets["processed_finding_ids"].add(ev["fix_key"])
for s in IDEMPOTENCY_SETS:
    state[s] = sorted(sets[s], key=str)
```

The two existing idioms, named:
- **IDIOM A (count / `+= 1`)**: a scalar counter incremented once per matching event (`round_counter`, `push_count`, `reply_count`). The V1.1 `rereview_request_count` (count `REREVIEW_REQUESTED`) mirrors this exactly.
- **IDIOM B (add-to-set)**: `sets["<name>"].add(ev["<field>"])`, usually guarded by a presence check (`if ev.get(...)` or `and ev.get(...)` in the `elif`). The V1.1 `auggie_review_invoked` (fold `AUGGIE_FALLBACK_INVOKED.pr_number`) mirrors this.
- **IDIOM C (monotone-min)**: does NOT exist yet — must be authored for `effective_max_rounds`. See §4.3.

Note the structural rule: matches are a single `if/elif` chain keyed on `et`. **Each event_type appears in at most one branch.** New folds for distinct event types add new `elif` branches; folds keyed on the same event but writing different state belong in the same branch's body.

---

## 4. EXACT V1.1 patterns to mirror (file:line of the example for each)

### 4.1 Add enum member + bump count (models.py)

Example to mirror — any member line, e.g. models.py:70:
```python
    PUSH_ABORTED_OR_NOT_LANDED = "push_aborted_or_not_landed"
```
Add the four new members in the closed enum (models.py:19-70), e.g. a new section:
```python
    # --- V1.1 re-review / fallback (§6.1) ---
    REREVIEW_REQUESTED = "rereview_requested"
    DECLINE_DETECTED = "decline_detected"
    AUGGIE_FALLBACK_INVOKED = "auggie_fallback_invoked"
    MAX_ROUNDS_CLAMPED = "max_rounds_clamped"
```
Then bump the count in ALL of these locations (33 → 37):
- **models.py:20** — class docstring `"EXACTLY 33 members"`.
- **models.py:3-4** — module docstring `"exactly 33 members — the 32 from spec §11.3 plus ..."`. This sentence enumerates the provenance ("32 from §11.3 plus push_aborted_or_not_landed"); V1.1 should extend it to describe the 4 new members so the docstring stays truthful (e.g. "37 members — the 33 prior plus 4 V1.1 re-review/fallback events §6.1").
- **run_log.py:109** — `ValueError` message `"(not one of the 33 §11.3 events)"`.
- **run_log.py:103-104** — `append()` docstring `"not one of the 33 closed enum values"`.
- **Test count** — the `EventType` count assertion in the test suite (R5 details) must become 37.

### 4.2 Add idempotency set + its fold (run_log.py)

Step 1 — extend the tuple (run_log.py:27-33), and update the count comment:
```python
# The 6 idempotency sets (§11.4 + §6.1 V1.1).
IDEMPOTENCY_SETS = (
    "processed_review_ids",
    "processed_finding_ids",  # keyed on fix_key
    "replied_comment_ids",
    "resolved_thread_ids",
    "pushed_commit_shas",
    "auggie_review_invoked",  # V1.1: keyed on pr_number (§6.1/§6.3)
)
```
Step 2 — add the fold (mirror IDIOM B at run_log.py:177, the `THREAD_RESOLVED` branch) inside the `if/elif` chain in `rebuild_state` (run_log.py:162-187):
```python
    elif et == EventType.AUGGIE_FALLBACK_INVOKED.value and ev.get("pr_number") is not None:
        sets["auggie_review_invoked"].add(ev["pr_number"])
```
The serialization at run_log.py:188-189 then picks it up automatically.

### 4.3 Add the monotone-min fold for effective_max_rounds (run_log.py — NEW IDIOM)

No existing min-fold template — author it. Two sub-steps:

Step 1 — seed the scalar in the `state` dict (run_log.py:152-160), alongside `"round_counter": 0`:
```python
    "effective_max_rounds": None,
    "rereview_request_count": 0,
```
Step 2 — add the fold branches in the loop (run_log.py:162-187). For the **count** (IDIOM A, mirror `round_counter` at run_log.py:167-168):
```python
    elif et == EventType.REREVIEW_REQUESTED.value:
        state["rereview_request_count"] += 1
```
For the **monotone-min** (NEW IDIOM C) — recommended None-safe form:
```python
    elif et == EventType.MAX_ROUNDS_CLAMPED.value and ev.get("effective_max_rounds") is not None:
        prev = state["effective_max_rounds"]
        clamp = ev["effective_max_rounds"]
        state["effective_max_rounds"] = clamp if prev is None else min(prev, clamp)
```
Rationale for min: clamping is monotone-decreasing — once max_rounds is clamped lower, a later (higher) value must not raise it back. `None` means "never clamped". This matches the brief's "→min (monotone)" instruction. The builder should add a test asserting two `MAX_ROUNDS_CLAMPED` events fold to the smaller value (R5 territory).

### 4.4 Add SkillResult fields (models.py:165-187)

Existing field-declaration examples to mirror:
- scalar with literal default — `round_counter: int = 0` (models.py:177), `summary_posted: bool = False` (models.py:180), `applied_edits: int = 0` (models.py:181).
- Optional with None — `proposal: str | None = None` (models.py:187), `push_decision: "PushDecision | None" = None` (models.py:184).
- mutable default — `findings: list[Finding] = field(default_factory=list)` (models.py:182) [the `field` import is already present, models.py:15].

`@dataclass` is a **plain (non-frozen) dataclass** (models.py:165 — bare `@dataclass`, no `frozen=True`/`eq=`/`order=`). Mutating attributes is allowed (matches `run_skill` populating it). Add the V1.1 fields after `proposal` (models.py:187):
```python
    rereview_request_count: int = 0
    fallback_engaged: bool = False
    auggie_review_invoked: bool = False
    decline_detected: bool = False
    effective_max_rounds: int | None = None
    fallback_round_counter: int = 0
```
All six are scalar/Optional — inline literal defaults, no `field(default_factory=...)` needed. The brief's exact defaults (`=0`, `=False`, `=None`) match this pattern verbatim.

---

## 5. models.py — count-enforcement, MonitorState/TERMINAL_STATES, dataclass conventions

### 5.1 EventType "EXACTLY N members" enforcement
- The count lives in **prose docstrings** (models.py:3-4 module, models.py:20-26 class) and the **run_log ValueError** (run_log.py:109) — none of these is self-asserting in source.
- The actual assertion is a **test** (R5 owns the detail): the `test_models` suite contains an `EventType` count check (`len(list(EventType)) == 33` or equivalent). This is the gate that fails if you add members without bumping. The docstring count is documentation; the test count is enforcement. (Unverified exact line/wording — flagged for R5.)

### 5.2 MonitorState ↔ TERMINAL_STATES (models.py:83-126)
- `MonitorState` is a `str, Enum` of working + terminal states (models.py:83-113).
- `TERMINAL_STATES` (models.py:117-126) is a `frozenset` of the 6 terminal `MonitorState` members the FSM never leaves: `TERMINAL_CLEAN, HALT_MAX_ROUNDS, HALT_HUMAN, VALIDATION_FAIL, TERMINAL_TIMEOUT, TERMINAL_FAILED`.
- The V1.1 deltas in this brief add NO new MonitorState or terminal — they are EventType + SkillResult + idempotency-set + fold changes only. (If a later V1.1 item adds a terminal, the pattern is: add the `MonitorState` member AND add it to the `TERMINAL_STATES` frozenset — two coordinated edits. R2 owns fsm.py transition wiring.)

### 5.3 Dataclass conventions (models.py)
- All four dataclasses (`Finding` models.py:129, `SkillResult` models.py:165, `PushDecision` models.py:190) are **plain `@dataclass`**, none frozen.
- Forward-ref types are quoted strings: `push_decision: "PushDecision | None" = None` (models.py:184) — needed because `PushDecision` is defined later in the file. The V1.1 SkillResult fields are all builtin/Optional-builtin, so no forward refs required.
- `from dataclasses import dataclass, field` (models.py:15) and `from enum import Enum` (models.py:16) are already imported — no import changes for V1.1.

---

## 6. Tests that exist asserting these patterns (WHICH only — R5 details HOW)

From the file headers and docstrings, the following test surfaces assert the patterns above (pointers for R5):
- `test_models` suite — EventType member count (the "EXACTLY 33" enforcement), Finding/SkillResult/PushDecision field+default assertions, MonitorState/TERMINAL_STATES.
- `test_run_log` suite (Unverified exact filename) — `rebuild_state` fold correctness, `record_idempotent` first/repeat True/False contract, `append`'s closed-enum `ValueError`, fsync/write-ahead, `_redact` (NFR-7), resume `_last_event_id`.
- The module docstrings cite test IDs: `T-N51` (redaction, run_log.py:10), `T-402` (PROPOSED proposal, models.py:186), `T-ZERO-EDIT-NO-PUSH` (PushDecision predicate_5, models.py:196-197), `INV-001`/`INV-009`/`INV-016` invariants.

R5 should: (a) read the exact `EventType` count assertion and update 33→37; (b) confirm whether `rebuild_state` has fold tests to extend for the 3 new folds; (c) confirm `record_idempotent` test covers the 6th set.

---

## Verification notes
- All run_log.py / models.py citations verified by full Read of both files (2026-06-12).
- Test file names/contents NOT read in this track (R5 scope) — `test_run_log` filename marked Unverified; `test_models` EventType count assertion inferred from the docstring's "asserted by a test" framing and standard pattern, flagged Unverified for R5 to confirm exact line.
- "min (monotone)" idiom (§4.3) has no in-repo precedent in rebuild_state; the recommended form is authored here, not mirrored from existing code.
