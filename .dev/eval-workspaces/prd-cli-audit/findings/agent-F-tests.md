# Agent F — PRD CLI Test Coverage Audit

Scope: every file under `tests/cli/prd/` (12 test modules, ~1450 lines).
Method: classify each file by harness shape; trace each anchor bug back through tests asking "if I introduced this defect today, which test turns red?"

## Test-surface classification

| File | Lines | Class | Real subprocess? | Touches `_resolve_step_content`? | Touches `_evaluate_gate` real chain? |
|---|---|---|---|---|---|
| `test_cli_smoke.py` | 80 | Click smoke | No (Click testing only) | No | No |
| `test_config.py` | 57 | Unit — path resolution | No | No | No |
| `test_e2e.py` | 564 | "E2E" but mock-heavy | No (mocks `PrdClaudeProcess`) | Indirectly via stream-file path only | Indirectly — gate fed via stream-pathway content |
| `test_executor.py` | 140 | Unit — sentinel/status | No | No | No |
| `test_filtering.py` | 138 | Unit — pure functions | No | No | No |
| `test_gates.py` | 220 | Unit — gate check_fns | No | No | No (calls semantic functions directly; never goes through `_evaluate_gate`) |
| `test_integration.py` | 349 | Integration but `_execute_step` monkeypatched | No | No | One test (`gate_enforcement`) calls `_evaluate_gate` with hand-crafted content |
| `test_inventory.py` | 127 | Unit — filesystem helpers | No | No | No |
| `test_models.py` | 122 | Unit — dataclass properties | No | No | No |
| `test_path_resolution.py` | 205 | Unit — `Path.cwd`/`Path.home` monkeypatch | No | No | No |
| `test_prompts.py` | 277 | Unit — prompt builder strings | No | No | No |
| `test_research_notes_roundtrip.py` | 77 | Round-trip prompt→gate (research-notes only) | No | No | No (calls check_fns directly) |

Net: zero tests exercise the chain `subprocess → Write to arbitrary disk path → stream contains commentary only → _resolve_step_content → _evaluate_gate`. Every "integration" or "e2e" test feeds gate-passing content **through the stream file**, which short-circuits the bug surface.

---

### F-F-1: No test covers the `_resolve_step_content` artifact-fallback path for missing step IDs

**Severity (preliminary)**: HIGH
**Pattern tags**: P1, P9, P6
**File:line**: no test exists; uncovered source path is `src/superclaude/cli/prd/executor.py:246-293` (`_STEP_ARTIFACT_FILES` table + fallback at line 268-269).
**Evidence** (executor.py:267-269 — the unguarded fallback):
```python
artifact_name = _STEP_ARTIFACT_FILES.get(step_id)
if not artifact_name:
    return ndjson_text
```
**Trace**: `_STEP_ARTIFACT_FILES` registers 4 step IDs (`parse-request`, `scope-discovery`, `research-notes`, `sufficiency-review`). The canonical Stage A step list at line 301-316 contains 9 IDs; Stage B/C add more. When a step is missing from the table, the function silently returns the NDJSON commentary text — exactly the prod failure mode. No test enumerates `_STEP_ARTIFACT_FILES.keys()` against the canonical step list, and no test calls `_resolve_step_content` directly with a registered-vs-unregistered step ID to verify the fallback shape.
**Reproduction sketch**: A test would set up a `task_dir` with `TASK-PRD-<slug>.md` on disk, call `_resolve_step_content("build-task-file", task_dir, "stream commentary here")`, and assert the result equals the file content (not the commentary). Or a structural test asserting `set(GATE_CRITERIA) ⊆ set(_STEP_ARTIFACT_FILES) ∪ {NDJSON-OK steps}`.
**Confidence (own)**: 0.97 — `grep -rn` across the test surface shows zero references to `_resolve_step_content` and zero references to `_STEP_ARTIFACT_FILES`. The symbol is exercised only transitively through `_run_subprocess_step`, where the mock harness invariably writes passing content into the *stream* file (e2e/integration both).

---

### F-F-2: No test for `build-task-file` covers the real subprocess→Write→gate chain

**Severity (preliminary)**: HIGH
**Pattern tags**: P3, P6, P9
**File:line**: `tests/cli/prd/test_e2e.py:149-178` (the only `build-task-file` mock) and `tests/cli/prd/test_integration.py:150-167` (budget-exhaustion test that pretends `build-task-file` was invoked).
**Evidence** (test_e2e.py:149-178 — mock writes the gate content to the *stream* file, bypassing the real defect):
```python
elif step_id == "build-task-file":
    # Gate: _check_task_phases_present (>= 2 phase headings)
    # + _check_b2_self_contained ...
    # + min_lines=400
    lines.extend([...phase 1/2/3 stubs...])
```
The mock factory at `test_e2e.py:245-251` writes this content via `output_file.write_text(output_text)` — i.e., into the NDJSON-stream file. Because `_resolve_step_content("build-task-file", …)` finds no `build-task-file` entry in `_STEP_ARTIFACT_FILES` and returns the NDJSON text unchanged, the test sees gate-passing content and the bug stays dormant.
**Trace**: The test asserts pipeline outcome `"success"` but the data path it exercises is "stream contains the full task file content." Production exercises "stream contains commentary; Write tool wrote the task file elsewhere on disk." The test could not distinguish these.
**Reproduction sketch**: Mock subprocess that writes commentary like "I wrote the file successfully" to the stream and a real 400+ line task file to `task_dir/TASK-PRD-<slug>.md`. Today the e2e would fail at the `build-task-file` gate with "Min lines: ~5/400"; that is the unwritten test.
**Confidence (own)**: 0.96 — verified by re-reading executor.py:512-546 (the gate reads `gate_content` from `_resolve_step_content`'s return value).

---

### F-F-3: Static dispatch table has no completeness test against the canonical step list

**Severity (preliminary)**: HIGH
**Pattern tags**: P1, P9
**File:line**: no test exists; would belong in `tests/cli/prd/test_executor.py`.
**Evidence**: `_STEP_ARTIFACT_FILES` (executor.py:246-251) lists 4 entries. The canonical Stage A step list (executor.py:301-316) emits 9 step IDs. The mismatch is plain structurally but only one ever surfaces because the bug at line 268 (silent NDJSON fallback) hides it.
**Trace**: This is the prototypical "completeness-of-static-dispatch-table" gap (P1). Any time a new step ID is added to `_STAGE_A_STEPS` (or Stage B/C generators) without a matching `_STEP_ARTIFACT_FILES` entry, the new step will silently use the NDJSON fallback. Bug 1 is exactly this regression having gone unnoticed.
**Reproduction sketch**: A structural test that walks the executor's step generators (Stage A static, Stage B/C dynamic), collects every step ID that ends up gated by `min_lines > 0` or by a semantic check, and asserts each appears either in `_STEP_ARTIFACT_FILES` or in an explicit allow-list of "NDJSON-is-authoritative" step IDs.
**Confidence (own)**: 0.94 — every search for either symbol turns up zero test references.

---

### F-F-4: No test for slug-templated artifact resolution (`TASK-PRD-{slug}.md`)

**Severity (preliminary)**: MEDIUM
**Pattern tags**: P3, P9
**File:line**: no test exists; relevant source path: executor.py:246-293 and prompts.py task-file write target.
**Evidence**: Slugs vary per run (`test-product`, `auth-system`, `superclaude-cli`, `big-platform`, `install-cmd` appear across fixtures). A correct resolver for `build-task-file` cannot be expressed as a static value in `_STEP_ARTIFACT_FILES` — it needs `f"TASK-PRD-{config.product_slug}.md"`. No test sweeps two distinct slugs and asserts the resolver produces the correct disk filename for each.
**Trace**: Even if a maintainer noticed Bug 1 and added `"build-task-file": "TASK-PRD-{slug}.md"` as a literal, the dispatch wouldn't work because the dict is `dict[str, str]` with no template substitution. No test for slug-templated artifact lookup means this design constraint is undocumented in the test suite.
**Reproduction sketch**: Test creates `task_dir/TASK-PRD-alpha.md` and `task_dir/TASK-PRD-beta.md` in two separate fixtures, exercises the resolver with `product_slug=alpha` then `product_slug=beta`, and asserts the correct file is selected for each.
**Confidence (own)**: 0.93 — `_resolve_step_content`'s `rglob(base_name)` could accidentally locate the slug file once a correct entry is added, but no test pins this behavior or warns about slug collision.

---

### F-F-5: No test verifies tier-dependent `min_lines` reaches the gate (Bug 3 latent)

**Severity (preliminary)**: HIGH
**Pattern tags**: P9
**File:line**: no test exists; uncovered source path: `src/superclaude/cli/prd/gates.py:281-292` (the unused `_tier_min_lines` and `_tier_min_lines_assembly` functions).
**Evidence** (gates.py:281-283 — the dead-on-arrival helper):
```python
def _tier_min_lines(tier: str) -> int:
    """Return tier-dependent minimum line count for task file gate."""
    return {"lightweight": 200, "standard": 400, "heavyweight": 600}.get(tier, 400)
```
Grep across `src/` and `tests/`: **only call-site is the definition itself**. `GATE_CRITERIA["build-task-file"].min_lines = 400` is a hard-coded constant (gates.py:367), and `_evaluate_gate` reads `gate.min_lines` directly (executor.py:596). The heavyweight 600-line threshold and lightweight 200-line threshold cannot be exercised.
**Trace**: The two heavyweight tests in the suite (`test_e2e_full_prd_creation_standard` is standard; `lightweight_e2e_config` uses 80-line default; `heavyweight_config` only exercises `_build_investigation_steps` count, not gates) never assert "for a heavyweight run, `build-task-file` requires 600 lines." `test_e2e_lightweight_prd` uses `default_line_count=80` which is below the supposed lightweight floor of 200 — and the test still passes, confirming the tier table is bypassed.
**Reproduction sketch**: Parametrize tier∈{lightweight, standard, heavyweight}, mock subprocess emitting exactly 350 lines of valid build-task-file content, assert standard tier PASSes the gate but heavyweight FAILs (350 < 600) and lightweight PASSes (350 > 200).
**Confidence (own)**: 0.98 — call-site search definitive; behavioral test for tier→min_lines does not exist.

---

### F-F-6: `_evaluate_gate` only exercised once via the real codepath; the rest of the gate tests bypass it

**Severity (preliminary)**: MEDIUM
**Pattern tags**: P6, P9
**File:line**: `tests/cli/prd/test_gates.py:1-220` (the entire module calls `_check_*` helpers directly) and `tests/cli/prd/test_research_notes_roundtrip.py:53-76` (also calls check_fns directly).
**Evidence**: `test_integration.py:197-223` is the **only** test that ever calls `executor._evaluate_gate(...)`. It feeds the gate a hand-built content string, never the result of `_resolve_step_content`. Every other gate test calls the individual `_check_*` predicates standalone.
**Trace**: This means the gate's most important data-source dependency — "did this content come from a disk artifact or from the NDJSON stream?" — is never tested. The bug class that produced "30 lines vs 409 lines" sits exactly in that join, and the test surface has no test that walks the join.
**Reproduction sketch**: A "gate input source assertion" test that intercepts the `gate_content` argument at `executor.py:532`, asserts it equals the on-disk artifact file content (not the stream-extracted text) for steps that have a Write-tool artifact pathway.
**Confidence (own)**: 0.90 — there's some defensible reason to test check_fns in isolation, but the absence of an "is the gate reading the right source" test is exactly what allowed Bug 1 to ship.

---

### F-F-7: `_extract_text_from_stream_json` ↔ malformed/partial NDJSON has no test

**Severity (preliminary)**: MEDIUM
**Pattern tags**: P4, P9
**File:line**: no test exists; uncovered call site at executor.py:518.
**Evidence**: `output_text = _extract_text_from_stream_json(raw_output) if raw_output else ""`. No test in `tests/cli/prd/` feeds malformed NDJSON (truncated mid-line, mixed text and JSON, empty stream, partial write) to either the extractor or downstream. The mock factory always writes a single well-formed text blob.
**Trace**: When the real subprocess crashes after partial output, the gate-evaluation path runs against whatever bytes landed. None of the test paths simulate this. Bug 1 manifested in production *partly* because the NDJSON commentary was treated as authoritative content; tests for malformed NDJSON would have made this asymmetry visible.
**Reproduction sketch**: Feed the executor a stream file containing only `{"type":"assistant","text":"I wrote the file"}` (one line) for `build-task-file` and assert gate fails with "Min lines: 1/400" rather than the mock-rigged passing path.
**Confidence (own)**: 0.85 — speculative connection to Bug 1, but the gap is real.

---

### F-F-8: `--tier`, `--max-turns`, `--where`, `--output`, `--product` knobs lack end-to-end behavioral verification

**Severity (preliminary)**: MEDIUM
**Pattern tags**: P9
**File:line**: `tests/cli/prd/test_cli_smoke.py:28-50` and `test_cli_smoke.py:58-79` only.
**Evidence**:
- `--tier` end-to-end: `test_prd_run_dry_run_validates_config` (test_cli_smoke.py:63-79) checks "the string 'heavyweight' appears in output." No test asserts that `--tier heavyweight` results in heavyweight gate thresholds being applied (Bug 3 corollary).
- `--max-turns`: `test_e2e_budget_exhaustion` (test_e2e.py:511-564) asserts halt occurs, never asserts that the *specific budget* allocation matched the user's value.
- `--where`: no test references this flag with content assertions.
- `--output`: `test_config.py:21-56` confirms default path, but no test exercises a user-supplied `--output` and asserts artifacts land there.
- `--product`: tested only as a string-template input.
**Trace**: Every "knob" is tested as a Click flag string presence (help text) and nothing more. Knobs that gate downstream behavior — esp. `--tier` driving gate thresholds — have no behavioral test.
**Reproduction sketch**: For each knob, one test setting a non-default value and asserting a downstream effect: tier→gate threshold, max-turns→ledger seed, output→artifact filesystem location, where→scope-discovery input, product→artifact filename templating.
**Confidence (own)**: 0.88.

---

### F-F-9: Mock harness in `test_e2e.py` mocks at a too-high level, defeating the "real chain" intent

**Severity (preliminary)**: MEDIUM
**Pattern tags**: P9
**File:line**: `tests/cli/prd/test_e2e.py:224-253` (the `_mock_process_factory`).
**Evidence** (test_e2e.py:245-250):
```python
def write_output_and_return():
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(output_text, encoding="utf-8")
    return exit_code
mock_proc.wait.side_effect = write_output_and_return
```
The mock writes the pre-cooked passing content **directly into the NDJSON stream file path**. There is no mock that simulates a subprocess writing via the Write tool to a *different* path while emitting only commentary on stdout. Production behavior is exactly that other pattern.
**Trace**: Because the mock conflates "what the subprocess streams" with "what the subprocess writes to disk," `_resolve_step_content`'s most interesting branch (search for disk artifact, fall back to stream) never gets exercised under stress. The test that pretends to be E2E is structurally a single-actor test where the stream is the only data source.
**Reproduction sketch**: Two-actor mock that (a) writes a small "I am done" text to the stream file and (b) writes a separate full-content artifact to `task_dir / "<resolved-artifact-name>"`. This would have caught Bug 1 the day it was introduced.
**Confidence (own)**: 0.93.

---

### F-F-10: `test_prd_pipeline_budget_exhaustion` (the only test that names `build-task-file`) doesn't reach the gate at all

**Severity (preliminary)**: LOW
**Pattern tags**: P9
**File:line**: `tests/cli/prd/test_integration.py:150-167`.
**Evidence**:
```python
executor._ledger.allocate(4)
result = executor._run_subprocess_step(
    "build-task-file", "Build Task File", "build_task_file_prompt"
)
assert result.status == PrdStepStatus.QA_FAIL_EXHAUSTED
```
**Trace**: The test name and the step ID hint that `build-task-file` is being covered, but the assertion path is "budget exhausted before subprocess is even launched." Neither the resolver, the NDJSON path, nor the gate is reached. From a regression-coverage standpoint this test does not count as `build-task-file` coverage.
**Reproduction sketch**: N/A — flagging that the only `build-task-file`-named test stops short of any gate-relevant codepath.
**Confidence (own)**: 0.95.

---

### F-F-11: No test for `_resolve_step_content`'s rglob skip-rules or "largest match wins" tie-breaking

**Severity (preliminary)**: LOW
**Pattern tags**: P9
**File:line**: no test exists; source at executor.py:281-291.
**Evidence**:
```python
for match in root.rglob(base_name):
    skip_parts = {"node_modules", ".git", "__pycache__"}
    if "-output.txt" in match.name or skip_parts & set(match.parts):
        continue
    try:
        content = match.read_text(...)
        if len(content) > len(best_content):
            best_content = content
```
Once Bug 1 is fixed, this resolver becomes load-bearing. The "largest match wins" tie-breaker (vulnerable to e.g. a `.bak` copy of a task file being larger than the canonical one) and the skip-rules (could accidentally match `node_modules/foo/research-notes.md` if a dep ships such a file) are untested.
**Trace**: Defensive coverage gap; not the cause of the current incident but the next bug class likely to surface once Bug 1 is patched.
**Reproduction sketch**: One test that creates two files matching `research-notes.md` — one canonical at task_dir, one larger but stale at task_dir.parent — and asserts the canonical wins (or that the existing largest-wins rule is the intentional behavior).
**Confidence (own)**: 0.80.

---

### F-F-12: `test_e2e_lightweight_prd` passes despite using line counts below the supposed lightweight floor — confirms Bug 3 latency

**Severity (preliminary)**: MEDIUM (counterexample-style finding)
**Pattern tags**: P9
**File:line**: `tests/cli/prd/test_e2e.py:323-354`.
**Evidence**: `_mock_process_factory(default_line_count=80)` on line 333. If `_tier_min_lines("lightweight")` were actually reaching the gate, this run would fail at the very first non-trivial-floor step. It doesn't fail, which is the runtime witness that tier scaling never happens.
**Trace**: Strengthens F-F-5 with a direct behavioral counter-witness: a fixture that ought to fail under spec'd tier scaling but passes today.
**Reproduction sketch**: N/A — this is a confirmatory observation, not a missing test per se.
**Confidence (own)**: 0.92.

---

## Considered and rejected

- **`test_research_notes_roundtrip.py` as a counterexample to F-F-6**: Considered claiming this file covers the resolver→gate chain. Rejected: it calls `_check_research_notes_sections` and `_check_suggested_phases_detail` directly with hand-built strings — it does verify prompt/gate schema agreement but does **not** route through `_evaluate_gate` or `_resolve_step_content`. So it does not invalidate F-F-6 or F-F-1.
- **"Maybe the integration test at `test_integration.py:197-223` covers Bug 1"**: Considered. Rejected: that test feeds `_evaluate_gate` hand-built content for `parse-request` (which *is* in `_STEP_ARTIFACT_FILES`), not for `build-task-file` (which isn't). It exercises gate plumbing but not the dispatch-table-completeness defect.
- **Treating `test_models.py::TestPrdConfigDerivedPaths` as artifact-path coverage**: Considered. Rejected: it asserts `research_dir`, `synthesis_dir`, `qa_dir` derive from `task_dir` — none touch artifact filename resolution.
- **Filing a missing-test finding for `_persist_step_artifact` (executor.py:976-1004)**: Considered. Result is a one-liner sibling to F-F-1 (same dict, same gap). Folded into F-F-1 rather than counted twice. The `_persist_step_artifact` early-return at line 988-989 (`if not artifact_name: return`) shares the exact same defect shape as the resolver and would be caught by the same dispatch-completeness test.
- **Filing a finding on `test_executor.py::test_determine_status_qa_fail`**: It uses step_id `"research-qa"` which is not in `_STEP_ARTIFACT_FILES` either, but this codepath legitimately doesn't need an artifact file (QA verdict checks the stream text by design). So this is not a missed test — `_determine_status` reading the stream is correct behavior.
- **A finding on the `output_text = _extract_text_from_stream_json(raw_output) if raw_output else ""` early-empty branch (executor.py:518)**: Considered. The empty-stream path is conservative (returns "" which fails min_lines for everything but exempt steps). Low-severity, not pursued.
