# D-0045 — implementation notes

## Decisions

1. **`Literal` + runtime tuple, not `Enum`.** DM-001 specifies a Literal of 8 string values. An `Enum` would force every call site (JSONL emit, JSON replay on SIGINT, manifest authoring) to convert between enum and string, adding boilerplate. Using `Literal["PASS",...]` plus a derived `EVAL_STATUSES` tuple keeps the wire format identical to the model field and gives one runtime source of truth (`typing.get_args(EvalStatus)`) for membership checks.

2. **`__post_init__` validation.** DM-001 requires "invalid status raises `ValueError`; valid statuses are exactly the 8 listed". `Literal` is a static-typing hint and not enforced at runtime, so a small `__post_init__` check is the cheapest enforcement that survives mypy being absent at runtime and callers that build outcomes from dynamic strings (the partial-summary path on SIGINT and JSON replay both do this).

3. **`expects: tuple[ExpectResult, ...]`, not `list[...]`.** A frozen dataclass with a `list` field would still allow callers to mutate the list in place, breaking equality and hashability. Tuple is the canonical immutable container for `field`-default and equality.

4. **`artifacts: Mapping[str, str]` with `default_factory=dict`.** Same hashability argument as for `expects` — but DM-001 spells `artifacts` as `dict[str, str]`. We accept it as `Mapping` so the Reporter can pass `MappingProxyType` without rejection, and `to_dict()` always returns a fresh `dict` copy so consumer mutation does not leak back into the frozen source.

5. **`to_dict()` builds an explicit ordered dict.** `dataclasses.asdict` recursively unwraps nested dataclasses but does not guarantee field ordering across Python versions for tests that compare serialised JSON. Using `_EVAL_OUTCOME_FIELDS` mirrors the pattern already established by `ExpectFailure.to_dict()` (DM-005 / T01.16) so the Reporter has a single shape to lean on.

6. **`Optional[ExpectResult]` is not needed.** DM-001 lists `expects` as a list (zero-or-more) — `()` is the default for `SKIPPED` outcomes that produced no assertions. No `Optional` wrapper is required.

7. **No coupling enforced between `status` and `skip_reason` / `error_class`.** DM-001 does not mandate "SKIPPED requires non-None skip_reason" or "ERRORED requires non-None error_class". The validators upstream (loader, lifecycle) populate these consistently; the model accepts both shapes so partial-summary paths on SIGINT can construct outcomes without all metadata.

## Cross-references

- DM-001 source: `cliEval/roadmap-haiku-architect.md:190`.
- Sibling models in `models.py`: `EvalSpec` (DM-002 / T01.03), `ExpectResult` (DM-009 / T01.15), `ExpectFailure` (DM-005 / T01.16).
- Consumed by: `EvalRunner` (T03.04 / T03.05), `Reporter` (T03.13), `RunOrchestrator` (T03.15).

## Out-of-band considerations

- `EvalContext.artifacts` (DM-010 / T03.03) has the same name but a different role — DM-010 is the runtime context fed into ExpectCallable; DM-001 `EvalOutcome.artifacts` is the post-run inventory. Both stay `Mapping[str, str]` to keep call sites consistent.
- The `__post_init__` validator raises `ValueError` rather than a bespoke exception. The Reporter and orchestrator already handle generic value errors via the FR-RPT1 contract guard (T03.11 / `ReporterContractViolation`); a dedicated exception class for invalid status would not buy anything until that guard differentiates more error types.
