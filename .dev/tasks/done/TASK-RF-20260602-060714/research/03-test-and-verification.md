# Research 03 — Test & Verification

> **Status:** In Progress
> **Topic:** Existing test coverage for R1–R5 surfaces + where/how to add regression tests.
> **Track goal:** Remediate validated PR #112 + #111 review findings (see `.dev/reviews/PR-112-111-remediation-design.md`).
> **Scope boundary:** Tests/fixtures/verification ONLY. Code sites, conventions, MDTM template covered by other researchers.

All file:line citations below were verified by reading the actual files during this research pass (2026-06-02).

---

## 1. arch_lint tests (R3 surface)

**Test file:** `tests/contracts/test_arch_lint.py` (237 lines, verified).
**Source under test:** `src/superclaude/tools/arch_lint.py` (281 lines, verified).

### Structure / fixtures
- Pure unit tests, `tmp_path`-driven. No conftest fixtures needed — each test writes a synthetic `.py` file into `tmp_path` and calls `scan_file(path, _CANONICAL_NAMES, _CANONICAL_PATTERN_BODIES)` directly (`test_arch_lint.py:45`).
- Module-level constants drive every test: `_CANONICAL_NAMES` (a hand-maintained set, `test_arch_lint.py:24-33`) and `_CANONICAL_PATTERN_BODIES = set(ID_PATTERNS.values())` (`:34`).
- Three public entrypoints are exercised: `scan_file` (single file), `check_paths` (aggregate across a dir, `:113-124`), and `main` (CLI exit codes 0/1/2, `:127-150`).
- Violation kinds asserted via `[v for v in violations if v.kind == "<kind>"]` filtering. Kinds today: `name-rebind`, `literal-duplicate`, `class-redef` (`arch_lint.py:67`).

### How it asserts violations vs clean
- **Clean:** `test_clean_file_yields_no_violations` (`:37-46`) writes a file that imports from contracts → asserts `violations == []`.
- **Violation present:** `test_literal_duplicate_violation_detected` (`:63-74`) writes `PATTERN = {fr_body!r}` using `ID_PATTERNS["FR"]` as the body, then asserts exactly one `literal-duplicate` violation whose `.name == fr_body`.
- **Opt-out:** `test_allow_marker_suppresses_violation` (`:77-86`) appends `# arch-lint: allow-duplicate test-fixture` and asserts the `literal-duplicate` list is empty.

### The Rule 2 false-positive site (what R3 hardens)
`arch_lint.py:168-185` Rule 2: it walks **every** `ast.Constant` string node (`:169`) and flags any whose value is in `canonical_pattern_bodies` via exact set membership (`if node.value in canonical_pattern_bodies:`, `:170`). It does **not** skip docstrings. The only escape today is the per-line allow-marker (`_line_has_allow_marker`, `:103-107`, checked at `:171`). A docstring whose entire value equals a regex body would currently be flagged. The walker passes clean today (0 violations), so this is defensive hardening, not a live bug.

### Where the R3 test goes
Add to `tests/contracts/test_arch_lint.py` (alongside `test_literal_duplicate_violation_detected`). Two assertions, mirroring the design doc acceptance (`design §R3` acceptance, doc line 71):

1. **Docstring-exclusion (must NOT flag):** write a module whose docstring is a verbatim `ID_PATTERNS` body, e.g.
   ```python
   fr_body = ID_PATTERNS["FR"]
   mod = tmp_path / "docstr.py"
   mod.write_text(f'"""{fr_body}"""\nX = 1\n', encoding="utf-8")
   violations = scan_file(mod, _CANONICAL_NAMES, _CANONICAL_PATTERN_BODIES)
   assert [v for v in violations if v.kind == "literal-duplicate"] == []
   ```
   Cover the three docstring positions the design names (module / class / function — `design §R3`, doc line 68): a class docstring and a function docstring as additional cases or parametrize.
2. **Real assignment (MUST still flag):** the existing `test_literal_duplicate_violation_detected` (`:63-74`) already locks this — keep it green to prove the hardening did not over-suppress. Optionally add an explicit paired test in the same module so the "docstring exempt / top-level literal still caught" contrast is self-documenting in one place.

**Caveat (unverified, implementation note for builder):** the current `scan_file` uses `ast.walk` (`:143`) which flattens the tree and loses parent context, so a docstring node is indistinguishable from any other `ast.Constant` at walk time. The R3 implementation must pre-compute docstring node identities (one pass over `Module`/`ClassDef`/`FunctionDef`/`AsyncFunctionDef` `.body[0]` `Expr` values) — the test only asserts the *behavior*, but the builder should know `ast.walk` alone cannot tell them apart.

---

## 2. Contract #9 / gates tests (R2 surface)

### Files read
- `tests/roadmap/conftest.py` (173 lines) — fixture registry.
- `tests/roadmap/test_spec_roadmap_id_containment.py` (259 lines) — the Contract #9 regression suite.
- `tests/roadmap/test_gates_data.py` — MERGE_GATE composition assertions.
- `tests/roadmap/test_executor.py` (imports + pytestmark).
- Source: `src/superclaude/cli/roadmap/gates.py:1028-1113`; executor wiring `executor.py:650-674`.

### How the sidecar / registry is set up in fixtures
Two distinct mechanisms:

1. **`_merge_gate_id_registry_sidecar`** (`conftest.py:52-81`) — a **non-autouse** fixture that writes a *permissive* sidecar covering synthetic ID families (`FR-001..FR-999`, `NFR/SC/G-001..099`, `D1..D99` + `D-01..D-99`, `conftest.py:64-72`), registers it via `_gates.set_id_registry_sidecar_path(sidecar)` (`:77`), and clears it to `None` on teardown (`:81`). Applied per-module via `pytestmark = pytest.mark.usefixtures("_merge_gate_id_registry_sidecar")` — e.g. `test_executor.py:45`. The docstring (`conftest.py:44-49`) explicitly says use the `pytestmark` opt-in, NOT `autouse=True`, so it scopes only to integration tests that exercise MERGE_GATE with synthetic IDs.

2. **Per-test build-from-fixture** (`test_spec_roadmap_id_containment.py`) — tests build a real `SpecIdRegistry` via `build_id_registry(spec_path)` (`:83`), serialize with `registry.to_dict()` to `tmp_path/spec_id_registry.json`, then `_gates.set_id_registry_sidecar_path(sidecar)` (`:91`), then drive `_gates._roadmap_ids_within_spec(roadmap_body)` directly (`:100`).

### How `set_id_registry_sidecar_path` is reset between tests today
`test_spec_roadmap_id_containment.py:57-62` has an **`autouse=True`** isolation fixture `_isolate_gates_state` that calls `_gates.set_id_registry_sidecar_path(None)` **both before yield and after yield**. This is the per-test reset. The `gates.py:1046` docstring confirms `None` clears the hint "(used by tests for isolation)". Outside this one module, reset relies on `_merge_gate_id_registry_sidecar`'s teardown (`conftest.py:81`).

**Key R2 insight:** the reset is enforced **only at the test layer** (autouse fixtures + fixture teardown). The **production code path** (`executor.py:662-664`) only ever *sets* the path after a successful extract; it **never resets to `None` at run start**. `grep` confirms the only `set_id_registry_sidecar_path` call sites in `src/` are the executor set (`executor.py:664`) and the gates definition itself (`gates.py:1042`) — no reset call anywhere in production. This is exactly the leak R2 targets: a second in-process run that skips extract inherits the first run's sidecar instead of failing shut.

### Existing fail-shut tests (the R2 regression complements these)
- `test_fail_shut_when_sidecar_missing` (`:165-170`) — `None` hint → returns a str containing `"Contract #9"`.
- `test_fail_shut_when_sidecar_unreadable` (`:173-179`) — nonexistent path → str failure.
- The fail-shut branch is `gates.py:1069-1074` (returns the "(set_id_registry_sidecar_path was never called)" message when the global is `None`).

### Where the R2 regression test belongs
**File:** `tests/roadmap/test_spec_roadmap_id_containment.py` — it already owns every `_roadmap_ids_within_spec` fail-shut test and has the `_isolate_gates_state` autouse reset.

**Critical test-design hazard:** the autouse `_isolate_gates_state` fixture resets the global to `None` *between* tests, which would mask the cross-run leak if the regression naively used two test functions. The R2 regression must simulate **two sequential runs in ONE test body / one process window** where the reset does NOT fire between them:
- Run 1: register a sidecar (spec A), call `_roadmap_ids_within_spec(roadmap_A)` → expect a meaningful result.
- Run 2 (no extract, no reset): call `_roadmap_ids_within_spec(roadmap_B)` where `roadmap_B` carries IDs valid only under spec B → **must return a fail-shut string**, not `True`, not a stale-spec-A pass.

This proves the R2 fix (reset-at-run-start, design §R2 guard 1, doc line 53; or the path-identity guard, doc line 54) closes the leak. After the fix, the simplest assertion is: with no extract/reset between runs, run 2 fails shut. Existing Contract #9 fixtures (`test_phantom_id_rejected`, `test_spec_ids_contained_when_roadmap_matches_spec`, etc.) must stay green.

**MERGE_GATE composition guard (do not break):** `test_gates_data.py:108-126` asserts MERGE_GATE has exactly 8 semantic checks including `roadmap_ids_within_spec`. Any R2 change to gate wiring must preserve this count and name set.

---

## 3. Fixtures format (R5 reproduction-fixture template)

**Dir:** `tests/roadmap/fixtures/recurrence/id_containment/` — two files (verified):
- `spec_roadmap_drift_case.md` (3507 bytes) — single doc bundling `## spec` and `## roadmap` H2 sections; tests slice by heading via `_slice_section` (`test_spec_roadmap_id_containment.py:33-48`).
- `spec_roadmap_drift_case.expected.json` (807 bytes) — assertion oracle.

### Fixture .md format (the template for an R5 `M{n}-D{nn}` case)
- Front-matter-free markdown. A `## spec` H2 section listing requirement IDs as bullets (`- **FR-1** — ...`, `.md:13-17`), then a `## roadmap` H2 section with a deliverable table (`| # | ID | Title | ... |`, `.md:25-34`).
- Heavily commented: documents the source incident (master:§Recurrence #4, A12:F-A12-01 TUIBBS), and explains exactly which surface forms are phantom and why (`.md:36-39`).

### expected.json schema (verified)
```json
{
  "fixture": "id_containment/spec_roadmap_drift_case",
  "source_authority": { "master_recurrence_row": 4, "partition_finding": "...", "incident_summary": "..." },
  "spec_section_heading": "spec",
  "roadmap_section_heading": "roadmap",
  "expected_spec_ids": { "fr_ids": [...], "nfr_ids": [...], "sc_ids": [], "g_ids": [], "d_ids": [...] },
  "expected_phantom_violations": ["D-1","D-2","D-3","D-7","D-99","FR-99"],
  "expected_semantic_check_result_type": "str",
  "expected_failure_substring": "Contract #9: roadmap contains 6 IDs not in spec",
  "expected_contains_fr_99": false,
  "expected_contains_fr_1": true
}
```

### Loader / convention
- `recurrence_corpus_dir` session fixture → `tests/roadmap/fixtures/recurrence/` (`conftest.py:91-101`).
- `recurrence_case` indirect-parametrized fixture (`conftest.py:104-122`) takes `(failure_class, case_name)` and returns `(input_path, json.loads(expected_path))`. Used as `@pytest.mark.parametrize("recurrence_case", [("id_containment","spec_roadmap_drift_case")], indirect=True)` (`test_spec_roadmap_id_containment.py:70-74`).
- `README.md` (`fixtures/recurrence/README.md`) documents the layout, naming (`<failure_class>/<case_name>.md` + `.expected.json`), the "Adding a new case" procedure (must trace to a documented incident; verify Contract #1 fail-pre/pass-post), and **"No fabricated cases"**.

### R5 fixture template guidance
For an R5 `M{n}-D{nn}` reproduction fixture, the **most faithful home is `tests/roadmap/test_structural_checkers.py`** (in-test fixtures), because that is where PR #111's oracle tests live and where `check_signatures` is exercised — see §4. The recurrence-corpus disk format above is the alternative if a disk-backed `M{n}-D{nn}` case is desired (it would slot under a new or existing `failure_class` dir, traced to the TUIBBS v1-MVP incident already cited in `spec_roadmap_drift_case.md:3` and `TASK-RF-20260531-044100`). For the Contract #9 *sidecar* angle (the `md_ids` round-trip, design §R5 step 3, doc line 118), a new disk case under `id_containment/` would extend `expected.json` with an `md_ids` key.

---

## 4. R5 oracle — PR #111's 3 added unit tests (LOCATED, reachable locally)

PR #111 head `861047c2` ("fix(roadmap): honor M{n}-D{nn} milestone-prefixed IDs in tokenizer + canonicalizer") **is reachable** via `git show`. It added **3 unit tests** to `tests/roadmap/test_structural_checkers.py` inside `class TestSignaturesChecker` (113 insertions). They are the correct-behavior oracle for R5 path (b). Summary of each assertion (verified from the commit diff):

1. **`test_phantom_id_honors_explicit_non_references_for_milestone_d_ids`** — the canonical v1-MVP bug shape. Spec declares `M1-D01, M1-D02, M2-D01, M2-D02, M3-D01`; roadmap implements the same MD IDs and also references bare `D01..D05` as roadmap-internal indices, with an **"Explicit non-references (do not resolve against spec):"** allowlist annotation listing `D01..D05`. Asserts **0** `phantom_id`/`id_schema_drift` findings in the `signatures` dimension. Proves (a) the allowlist exempts bare D01..D05 AND (b) MD-family resolves `M1-D01 != M2-D01` distinctly.
2. **`test_phantom_id_backward_compatible_without_explicit_non_references`** — spec `D1,D3,D5`; roadmap `D01,D03,D05`; **no** allowlist annotation. Asserts **0 HIGH** `phantom_id` and **exactly 3** `id_schema_drift` MEDIUM findings (D01↔D1, D03↔D3, D05↔D5). Pins that the new allowlist machinery does not regress legacy zero-pad canonicalization.
3. **`test_phantom_id_bare_d_still_resolves_when_spec_uses_bare_d`** — spec `D7,D8`; roadmap `D7,D9`; no annotation. Asserts **exactly 1 HIGH** phantom (`D9`, `high_phantoms[0].roadmap_quote == "D9"`) and **0** drift (D7 matches spec D7 exactly). Confirms the MD tokenizer change does not break bare-D resolution for specs that legitimately use bare D-family.

The diff also added a helper `_write_md_fixture_with_allowlist(tmp_path, spec_body, roadmap_body, allowlist_tokens)` (static method) that writes a spec+roadmap pair where the roadmap carries the canonical `**Explicit non-references (do not resolve against spec):** the tokens \`...\` are **roadmap-internal deliverable sequence numbers** ...` annotation.

### Forward-port readiness on the current branch (verified)
- `class TestSignaturesChecker` exists (`test_structural_checkers.py:255`), and the reused helper `_write_id_fixture` exists (`:316`) — so tests 2 and 3 forward-port with minimal change; test 1 needs the new `_write_md_fixture_with_allowlist` helper ported alongside.
- `check_signatures` is imported in the current test module (`test_structural_checkers.py:17-25` block).
- **MD is absent on the current branch:** `grep` for MD/milestone/`md_ids` in `src/superclaude/cli/roadmap/spec_parser.py` and `structural_checkers.py` returns nothing (exit 0, no matches). The current tokenizer `_REQUIREMENT_PATTERNS` (`spec_parser.py:329-332`) is **auto-derived** from `_CONTRACTS_ID_PATTERNS` (i.e. `superclaude.contracts.ID_PATTERNS`) — so the only families are FR/NFR/SC/G/D (`contracts/__init__.py:64-70`). This confirms design §R5's framing: the FP can reproduce, and the SoT-correct fix is to add an `MD` key to `contracts.ID_PATTERNS`, which propagates to the tokenizer automatically (the canonicalizer + allowlist in `structural_checkers.py` still need explicit edits — those are not auto-derived).

---

## 5. Make targets / commands (verification surface)

Verified in `Makefile`:
- `make test` → `uv run pytest` (`Makefile:13-15`).
- `make lint` → `lint-architecture` then `uv run ruff check .` (`Makefile:48-51`).
- `make format` → `uv run ruff format .` (`:53-55`).
- `make lint-architecture` (`:362+`) — shell target; Checks 1-2 (bidirectional command↔skill links, naming). **Note:** the contract arch-lint walker (the R3 surface) is run via its own module, **not** via `make lint-architecture` directly — see exact invocation below.
- `make verify-sync` (`:166+`) — verifies `src/superclaude/{skills,agents,...}` ↔ `.claude/` parity; needed after R4's `make sync-dev`.
- `make verify-deps` (`:355+`) → `uv run python scripts/verify_deps.py`.

### Exact per-surface pytest invocations (UV only)
- **R3 arch_lint:** `uv run pytest tests/contracts/test_arch_lint.py -v`
- **R3 walker CLI (the actual lint):** `uv run python -m superclaude.tools.arch_lint --check-contracts src/superclaude/contracts/__init__.py --scan-paths src/superclaude/cli/` (usage block `arch_lint.py:28-30`; must exit 0).
- **R2 Contract #9:** `uv run pytest tests/roadmap/test_spec_roadmap_id_containment.py -v`
- **R2 MERGE_GATE composition:** `uv run pytest tests/roadmap/test_gates_data.py -v`
- **R2 executor integration:** `uv run pytest tests/roadmap/test_executor.py -v`
- **R5 structural checkers (oracle):** `uv run pytest tests/roadmap/test_structural_checkers.py -v` (the `TestSignaturesChecker` class; `-k TestSignaturesChecker` to scope).
- **R1 id_registry:** `uv run pytest tests/ -k id_registry` (per design §R1 acceptance, doc line 43).
- **R4 (shell script):** no pytest surface; acceptance is behavioral — run the script with a malformed `EXCLUDE:` and assert non-zero exit + diagnostic (design §R4, doc line 102), then `make sync-dev` + `make verify-sync`.

---

## 6. Baseline — "full suite delta vs parent baseline unchanged"

The design doc requires (design §R5 acceptance, doc line 124): *"full suite delta vs parent baseline unchanged."* There is no dedicated harness for this in the repo; the practical method (inferred, **unverified as an existing automated check**):

1. **Capture parent baseline:** on the parent/base commit (the design notes PR #112 reviewed at `1c56b50f`, HEAD `e22b7df3`; the natural parent for this branch is `origin/master` or the branch point), run `uv run pytest -q` and record the pass/fail/skip counts (e.g. a clean worktree, then `uv run pytest -q tests/ 2>&1 | tail -3`).
2. **Capture post-change:** after remediation, run the same `uv run pytest -q` and diff the summary line (passed / failed / skipped / xfailed).
3. **Delta rule:** the only permitted change is **added** tests (the new R2/R3/R5 regressions go from absent→passing) — **no** previously-passing test may flip to fail/skip. Per-surface, the targeted commands in §5 plus a full `make test` run at the end establish the delta.
4. **Contract #1 invariant** (`fixtures/recurrence/README.md` "Adding a new case" step 5; `test_spec_roadmap_id_containment.py:9-11`): each new regression test **must FAIL against the parent commit and PASS against the fix commit** — this is the per-test version of the baseline-delta check and is the strongest evidence that the test actually locks the fix.

**Recommendation for the builder:** capture the baseline count *before* starting (a single `uv run pytest -q tests/ | tail -3` on a clean tree) so the final delta is a concrete number comparison, not a vibe. A git worktree on the parent commit is the cleanest way to run the parent baseline without disturbing the working tree.

---

## Cross-cutting notes for the task builder

- **R2 and R3 tests are additive to existing files** — no new test files needed. R2 → `tests/roadmap/test_spec_roadmap_id_containment.py`; R3 → `tests/contracts/test_arch_lint.py`.
- **R5 oracle is fully recoverable** from commit `861047c2` (local, via `git show 861047c2 -- tests/roadmap/test_structural_checkers.py`) — the 3 tests + the `_write_md_fixture_with_allowlist` helper can be ported verbatim with only import/path adjustments. They target `tests/roadmap/test_structural_checkers.py::TestSignaturesChecker`.
- **R5 Contract #9 cross-cut:** if path (b), the sidecar schema test `test_registry_sidecar_schema_stable` (`test_spec_roadmap_id_containment.py:201-222`) and `test_sidecar_schema_round_trip` (`:236-258`) hardcode the 8-key set (`fr_ids, nfr_ids, sc_ids, g_ids, d_ids, accepted_deviation_ids, spec_hash, spec_path`). Adding `md_ids` requires updating **both** of these (the `expected_keys` set at `:207-217` and the reconstruction at `:248-257`), plus the conftest permissive sidecar (`conftest.py:63-75`) to include an `md_ids` list. Miss any of these and MD IDs become unrepresentable → Contract #9 fail-shut re-triggers (design §R5, doc line 118).
- **The arch_lint test asserts behavior, not parent-context plumbing** — the R3 builder still must implement docstring-node detection (ast.walk is parent-blind); the test is necessary but not sufficient to guide the implementation. Flagged so the builder reads design §R3 doc line 68 for the precompute approach.

---

> **Status:** Complete
>
> **Summary:** All 5 remediation surfaces have a concrete test home. **R2** (sidecar leak) → add a single two-runs-in-one-process regression to `tests/roadmap/test_spec_roadmap_id_containment.py`, working *around* the autouse `_isolate_gates_state` reset (`:57-62`) that would otherwise mask the leak; production code has NO run-start reset (`executor.py:664` only sets). **R3** (arch_lint docstring FP) → add docstring-exclusion + paired top-level-literal tests to `tests/contracts/test_arch_lint.py` next to `test_literal_duplicate_violation_detected` (`:63-74`); builder must implement parent-context docstring detection since `ast.walk` (`arch_lint.py:143`) is parent-blind. **R5** oracle = PR #111's 3 tests in commit `861047c2`, reachable locally, targeting `tests/roadmap/test_structural_checkers.py::TestSignaturesChecker` — forward-port verbatim (helpers `_write_id_fixture` exist at `:316`; port `_write_md_fixture_with_allowlist`). Current branch confirmed MD-free (`spec_parser.py:329-332` auto-derives families from `contracts.ID_PATTERNS` FR/NFR/SC/G/D only); path (b) additionally requires `md_ids` in sidecar schema tests (`:207-217`, `:248-257`) + conftest (`:63-75`). Recurrence-fixture format documented for any disk-backed R5 case. Per-surface `uv run pytest` commands enumerated (§5). Baseline-delta method (§6) is manual: capture `uv run pytest -q | tail -3` on parent vs post-fix; new tests must satisfy Contract #1 (fail-pre/pass-post). No new test files required for R2/R3; R5 reuses an existing one.
