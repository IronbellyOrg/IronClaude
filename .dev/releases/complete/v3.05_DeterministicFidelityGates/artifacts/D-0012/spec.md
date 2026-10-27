# D-0012: Checker Callable Interface and Registry (T02.01)

## Interface Contract

```python
CheckerCallable = Callable[[str, str], list[Finding]]
# Signature: (spec_path: str, roadmap_path: str) -> list[Finding]
```

Each checker:
1. Reads spec and roadmap files via `Path.read_text()`
2. Parses both using `parse_document()` from `spec_parser.py`
3. Routes to dimension-relevant sections via `DIMENSION_SECTION_MAP`
4. Compares deterministically — no LLM calls
5. Returns `list[Finding]` with rule-based severity via `get_severity()`

## Registry

```python
CHECKER_REGISTRY: dict[str, CheckerCallable] = {
    "signatures": check_signatures,
    "data_models": check_data_models,
    "gates": check_gates,
    "cli": check_cli,
    "nfrs": check_nfrs,
}
```

All 5 dimensions mapped. All entries callable. Section routing via `_get_sections_for_dimension()`.

## Verification

- `uv run pytest tests/roadmap/test_structural_checkers.py::TestRegistry -v` — 4/4 PASS
