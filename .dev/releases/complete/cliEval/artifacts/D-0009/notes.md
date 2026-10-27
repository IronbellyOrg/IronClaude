# D-0009 — Implementation notes

## Design choices

1. **Tuples instead of lists.** A frozen dataclass with mutable list
   defaults would be either (a) unhashable, or (b) a foot-gun if a
   caller passed in a shared list. `tuple` plus
   `field(default_factory=tuple)` gives an immutable, hashable report
   while remaining trivially JSON-serialisable (json.dumps converts
   tuples to arrays anyway, and `to_json()` materialises lists
   explicitly for clarity).

2. **Why a dedicated `CapabilityStatus` instead of `dict`s?**
   `report[]` carries structured per-capability outcomes that the
   doctor renders into a green checklist (design-spec §11). Using a
   dataclass:
   - matches the pattern set by `Capability` (T01.09) and `EvalSpec`
     (T01.03),
   - documents the row shape at the type level rather than in
     freeform dicts,
   - lets `to_json()` produce stable key ordering via an explicit
     `to_dict()` method instead of relying on Python dict insertion
     order from arbitrary call sites.

3. **`to_json()` returns `dict`, not `str`.** DM-008 says "serializable
   to JSON" and the validation report (L2 patch) demoted byte-level
   determinism to a Notes-level concern. Returning a mapping lets
   callers compose it (e.g. doctor wrapping it in a larger envelope)
   without re-parsing.

4. **`skipped_by_flag` field on `CapabilityStatus`.** Distinguishes
   "capability genuinely failed" from "capability passed but the user
   asked us to ignore it (`--no-mcp`)". COMP-009 (T01.11) sets this
   bit when it sees a `Capability.skip_flag` in the active skip set.

5. **Key ordering.** `to_json()` emits keys in dataclass-field order,
   not alphabetical, so the JSON layout mirrors how a reader would read
   the dataclass definition. This makes diffs in doctor snapshot tests
   meaningful (see T01.13 Notes about derived determinism).

## Trade-offs and follow-ups

- **No reverse `from_dict()`.** DM-008 only requires serialisation,
  not round-tripping. If a future test asserts JSON → `CapabilityReport`
  parity we can add `from_json()` then; right now it would be
  speculative.
- **Tuple ordering is caller-controlled.** `CapabilityGates.check_all`
  (T01.11) is responsible for emitting capabilities in the canonical
  `CAPABILITIES` order, which is what gives the doctor output its
  stable shape. `CapabilityReport` does not sort defensively.
- **`Capability` not used as a `report[]` entry.** A `Capability`
  holds a `Callable`, which is not JSON-safe. Hence the dedicated
  `CapabilityStatus` value type.
