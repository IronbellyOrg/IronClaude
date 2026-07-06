# Consolidated Findings — Phase Gate B M3 (serialized fix protocol, I20)

**Generated:** 2026-06-11 13:10
**Step:** PGB.4
**6 lens reports:**
- template-conformance → PASS (0)
- internal-consistency → PASS (0)
- core-purity/evidence → PASS (0)
- domain-accuracy → **FAIL (1 IMPORTANT + 2 MINOR seam notes)**
- crossref-chain/test-coverage → **FAIL (7 IMPORTANT + 1 MINOR)**
- actionability/spec-correction → PASS (0)

## CONSOLIDATED VERDICT: FAIL (any-finding rule) → one serialized fix agent (PGB.5)

## Findings (deduplicated)

### B-1 — IMPORTANT — `src/superclaude/pr_submit/fsm.py` `parse_args` (EC-8 unreachable via CLI)
- **Lens:** domain-accuracy.
- **Issue:** `parse_args` raises `ValueError("--max-rounds must be >= 1")` on `max_rounds < 1`, but spec **EC-8** (lines 550-554) mandates `--max-rounds=0` as a VALID "monitor but never remediate" config (gate `0 >= 0` True → HALT before any fix, zero rounds). The core (`run_skill` via `RunConfig(max_rounds=0)`) honors EC-8 (test_ec8 passes), but the documented CLI surface rejects it.
- **Fix:** Change the lower-bound guard in `parse_args` to allow `0` (reject only negative): `if ns.max_rounds < 0: raise ValueError(...)`. Keep the `> 5` hard-cap. Add a parse test asserting `--max-rounds 0` parses to 0 (and is accepted).

### B-2 — IMPORTANT — `tests/pr_submit/test_static_grep.py` (T-105 missing — runtime --repo assertion)
- **Lens:** crossref-chain.
- **Issue:** spec §6.2 maps FR-1.3/AC-7 → **T-104 AND T-105**. T-104 (static grep) exists; **T-105** (runtime: a gh call asserts `--repo` is present) has no test.
- **Fix:** Add a `test_t105_*` runtime test (in `test_static_grep.py` or `test_pre_pr_checks.py`) asserting that a constructed gh poll/reply invocation includes `--repo IronbellyOrg/IronClaude` (e.g. via the `mock_gh` recorder or by asserting the poll script's command shape). Map T-105 in the docstring.

### B-3 — IMPORTANT — `tests/pr_submit/test_severity_router.py` or detection test (T-N31 missing)
- **Lens:** crossref-chain.
- **Issue:** spec §6.2 maps NFR-4 → **T-N30 AND T-N31**. T-N30 exists; **T-N31** (`github-actions[bot]` → ignored, stays "polling") has no named test (behavior covered by FM-4/EC-10 but the ID is unresolvable).
- **Fix:** Add a `test_tn31_*` test asserting a known non-Augment bot (`github-actions[bot]`) classifies as `"polling"` (review not detected, NFR-4 fail-safe). Map T-N31 in the docstring.

### B-4 — IMPORTANT — 5 orphan fixtures unreferenced by any test
- **Lens:** crossref-chain.
- **Issue:** `finding-empty.json`, `finding-malformed.json`, `finding-max.json`, `finding-needs-human.json`, `round-sequence-2.json` are created but NEVER `load_fixture`-ed — their behavior-twin tests (EC-1, EC-9, EC-3, EC-7/FM-10, a round-sequence) build data inline. Spec §6.3 intends each edge case to use its dedicated fixture.
- **Fix:** Wire the relevant tests to `load_fixture` the corresponding fixture (so each fixture is referenced): EC-1→finding-empty, EC-9→finding-malformed, EC-3→finding-max, EC-7→finding-needs-human, and add a round-sequence test (or T-E... ) loading round-sequence-2.json. Keep the existing inline assertions; ADD a load_fixture reference + an assertion using it. Re-run the suite after.

### B-5 — MINOR — 3 comment-only fixtures (drift risk)
- **Lens:** crossref-chain (MINOR) + domain-accuracy (seam notes).
- **Issue:** `round-sequence-residual-x3.json`, `behavioral-drift.json`, `crash-after-push-before-completed.json` are named only in docstrings, never loaded (their tests build the scenario inline for robustness). This is acceptable (the inline scenarios mirror the fixtures) but the fixtures could drift from the tests.
- **Fix (light):** Add a parity assertion in the relevant test that loads each fixture and asserts a key field matches the inline scenario (e.g. the residual-x3 cycle count, the crash fixture's dangling push_initiated, the drift fixture's behavioral_test_failures). This makes the fixture genuinely referenced and guards drift. (MINOR — apply if cheap.)

## Fix scope (PGB.5)
`src/superclaude/pr_submit/fsm.py` (B-1) + several `tests/pr_submit/*.py` (B-2..B-5). After fixes,
re-run `uv run pytest tests/pr_submit/ -v` + `make lint` (ruff check pr_submit) + `uv run ruff format
--check` and record the result. A fix that breaks tests/lint/format is itself a finding.
