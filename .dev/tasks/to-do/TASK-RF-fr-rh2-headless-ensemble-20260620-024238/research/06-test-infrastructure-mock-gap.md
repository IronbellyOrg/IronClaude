# R6: Test Infrastructure & The Mock Gap

**Status:** Complete
**Date:** 2026-06-20
**Topic:** conftest mock gap, no-nesting guard (extend to ensemble.py), regression floor (B1/B2/B3), swarm stub-integration precedent, merge boundary, pool guard
**Worktree:** /config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3

Zero-trust: every line anchor below was re-Read in this turn. Where the TDD's anchor was off, the corrected current anchor is stated.

---

## 1. THE MOCK GAP — `make_claude_process_stub` (the thing the new integration test must NOT reuse)

**File:** `tests/cli/reflect/conftest.py`
**TDD anchor:** L98-138 — **VERIFIED EXACT.** The `make_claude_process_stub` fixture is defined at **L98**, body runs through **L138** (`return _builder`).

### Exact mechanism (conftest.py:98-138)

- `make_claude_process_stub` returns a builder `_builder(fixture_name, rc=0, write_contract=True)` (L114-136).
- The builder reads the fixture bytes eagerly: `fixture_bytes = (FIXTURES_DIR / fixture_name).read_bytes()` (L117-119).
- It returns `factory(**kwargs)` (L121) which builds a `MagicMock()` (L124), sets `mock.start.return_value = None` (L125), and defines a closure `_wait()` (L127-131):
  - `_wait()` does `(output_dir / "return-contract.yaml").write_bytes(fixture_bytes)` **from inside `.wait()`** when `write_contract and fixture_name is not None` (L128-130), then `return rc` (L131).
  - `output_dir = Path(kwargs["output_file"]).parent` (L122-123).
- `mock.wait.side_effect = _wait` (L133).

**Why this is the gap (FR-RH2 driver):** The stub **replaces the entire `ClaudeProcess` object** via `patch("superclaude.cli.reflect.runner.ClaudeProcess", side_effect=factory)`. It **never executes any real reflect code** — it just copies a canned YAML into `return-contract.yaml`. So every B1/B2/B3 verdict path is proven only against a *hand-written* contract, never against a contract an actual ensemble/synthesis path emitted. The new `test_ensemble_stub_integration.py` **must NOT** patch `ClaudeProcess`; it must inject a **StubTransport at the transport seam** so the REAL `ensemble.py` code path runs and emits a real contract shape.

**Sibling fixture (also a mock, also must not be reused for the integration proof):** `make_claude_process_sequence` at **L142-188** — the SEQUENCE-aware variant for the bounded fix-loop (pops `(fixture_name, rc)` per construction; `None` = writes no contract = the `/task` apply launch). Same `MagicMock` + `.wait()`-writes-fixture mechanism (L166-186).

### Supporting fixtures in conftest.py (the new integration test may legitimately reuse these)
- `cli_runner` (L40-43) — fresh `CliRunner`.
- `temp_tasklist` (L46-55) — writes a minimal MDTM tasklist with `start_commit` + `reflect_post: ""`; uses `_TASKLIST_TEMPLATE` (L23-37) and `_FAKE_BASE` (L20).
- `patch_git` (L58-80) — stubs `config._git` so `rev-parse HEAD`→`_FAKE_HEAD`, `merge-base`→`_FAKE_BASE`; exposes `.base`/`.head` (`_FAKE_BASE`=L20, `_FAKE_HEAD`=L21).
- `patch_runner_env` (L83-95) — stubs `runner._child_env`→`{}` and `runner.shutil.which`→`/usr/bin/claude` so the `claude`-binary preflight passes.

---

## 2. `fixtures/pass.yaml` — the reflect contract SHAPE the new ensemble.py must emit

**File:** `tests/cli/reflect/fixtures/pass.yaml` (28 lines, 23 top-level keys).
**TDD claim "line 4 hard-codes `tier_reached: 2`":** **VERIFIED EXACT** — `pass.yaml:4` is `tier_reached: 2`.

### Full pass.yaml key list (with the constants R6 was asked to capture)
| Line | Key | Value |
|---|---|---|
| 1 | `contract_version` | `"1.3.0"` |
| 2 | `status` | `success` |
| 3 | `mode` | `post` |
| 4 | `tier_reached` | `2` ← hard-coded |
| 5 | `report_path` | `/tmp/reflect-out/REPORT.md` |
| 6 | `audit_log_path` | `/tmp/reflect-out/audit.log` |
| 7-11 | `deviation_count_by_class` | `authorized:0 necessary:0 drift:0 regression:0` |
| 12 | `t2_model_class_diversity` | `full` |
| 13 | `t2_vendor_diversity` | `multi` |
| 14 | `adversarial_unavailable` | `false` |
| 15 | `merge_method` | `adversarial` |
| 16 | `adversarial_convergence_score` | `0.86` |
| 17 | `verification_ran` | `true` |
| 18 | `verification_skip_reason` | `null` |
| 19 | `citations_dropped` | `0` |
| 20 | `citations_dropped_extrapolated` | `0` |
| 21 | `input_drift_detected` | `false` |
| 22 | `regression_present` | `false` |
| 23 | `unauthorized_deviation_present` | `false` |
| 24 | `needs_human_decision` | `false` |
| 25 | `user_decision_required` | `false` |
| 26 | `serena_summary_corroboration` | `unavailable` |
| 27 | `degraded_components` | `[]` |

Key constants R6 was told to note: `tier_reached: 2` (L4), `t2_model_class_diversity: full` (L12), `merge_method: adversarial` (L15), `adversarial_convergence_score: 0.86` (L16). (`t2_vendor_diversity: multi` at L13 is the vendor-diversity sibling.)

### Other fixtures present (`tests/cli/reflect/fixtures/`)
PASS: `pass.yaml`, `postfix_pass.yaml`.
HALTED/regression: `halted_regression.yaml`.
DEGRADED: `degraded_serena.yaml`, `degraded_single_vendor.yaml`, `degraded_tier1.yaml`, `degraded_with_drift.yaml`.
BLOCKED: `blocked_unknown_major.yaml`, `blocked_with_drift.yaml`.
DRIFT/fix-loop: `autofixable_drift.yaml`, `autofixable_drift_no_path.yaml`.
HUMAN: `human_required_needs_decision.yaml`.
TOLERANCE: `tolerant_unknown_field.yaml`.
Plus `__init__.py` (empty). **Confirmed: fail/degraded/blocked fixtures are all present** (there is no single `fail.yaml`; failure states are split across `halted_*`/`blocked_*`/`degraded_*`).

---

## 3. `test_no_nesting_guard.py` — STRUCTURE + how to EXTEND to `ensemble.py`

**File:** `tests/cli/reflect/test_no_nesting_guard.py` (143 lines).
**TDD anchor "L95-102":** **PARTIAL.** L95-102 is only Layer-B's `test_layer_b_wrapper_module_has_no_agent_imports`. The full guard is 6 tests spanning L80-143. Corrected anchors below.

### Module-level constants (the scan inputs — L18-46)
- `_REPO_ROOT = Path(__file__).resolve().parents[3]` (L19).
- `_REFLECT_PKG = _REPO_ROOT / "src/superclaude/cli/reflect"` (L21).
- `_RUNNER_SRC = _REFLECT_PKG / "runner.py"` (L22).
- **THE LIST TO EXTEND →** `_REFLECT_PY = sorted(p for p in _REFLECT_PKG.glob("*.py") if p.name != "__init__.py")` (**L24**). This is a package-wide glob — **it ALREADY auto-includes `ensemble.py` once that file exists** in `src/superclaude/cli/reflect/`. The two package-wide tests that iterate `_REFLECT_PY` (sprint/roadmap import + async/await, see below) will cover `ensemble.py` for free.

### Regexes (quoted exactly, L29-46)
- `_SPRINT_ROADMAP_IMPORT_RE = re.compile(r"^\s*(?:from|import)\s+\S*(?:sprint|roadmap)", re.MULTILINE)` (L29-31).
- `_ASYNC_DEF_RE = re.compile(r"^\s*async\s+def\b", re.MULTILINE)` (L33).
- `_AWAIT_RE = re.compile(r"^\s*await\s", re.MULTILINE)` (L34).
- `_RAW_SUBPROCESS_CALL_RE = re.compile(r"\b(?:subprocess\.(?:run|Popen)|Popen)\s*\(")` (L38).
- `_IMPORT_SUBPROCESS_RE = re.compile(r"^\s*(?:import\s+subprocess|from\s+subprocess\b)", re.MULTILINE)` (L39-41).
- `_NESTING_TOKENS = ("Task(", "subagent_type")` (**L46**) — NOTE: tuple is `("Task(", "subagent_type")`, NOT the TDD's hand-wave `Task(`/`subagent`/`anthropic`. The `anthropic` import check lives only in the Layer-B per-file loop (L99).

### The 6 tests
1. `test_layer_a_wrapper_branch_is_bash_shellout` (L80, decorated `@pytest.mark.xfail(strict=False)` L68-79; currently XPASS). Asserts the task-builder SKILL O1 gate is a Bash `superclaude reflect run --depth deep --fix` shell-out carrying `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`, and contains no `_NESTING_TOKENS` (L84-92). **Reflect-pkg-agnostic — does not scan ensemble.py.**
2. **`test_layer_b_wrapper_module_has_no_agent_imports` (L95-102)** — scans ONLY `runner.py`: asserts `"ClaudeProcess" in src` (L98) and that none of `("import anthropic", "from anthropic", "subagent", "Task(")` appear (L99-102).
3. **`test_no_sprint_or_roadmap_import_anywhere_in_reflect_pkg` (L105-113)** — iterates `_REFLECT_PY` (L108), asserts `_SPRINT_ROADMAP_IMPORT_RE.search(src) is None` per file. **Auto-covers ensemble.py.**
4. **`test_no_async_await_anywhere_in_reflect_pkg` (L116-125)** — iterates `_REFLECT_PY` (L122), asserts no `async def`/`await`. **Auto-covers ensemble.py.**
5. `test_apply_remediation_launches_only_via_claudeprocess` (L128-142) — scans ONLY `runner.py`: `ClaudeProcess`/`_apply_remediation`/`/task ` present, no raw `subprocess.run`/`Popen` call or import.

### HOW TO EXTEND the guard to `ensemble.py` (the deliverable)
Two complementary moves; pick per FR-RH2's intent (the headless ensemble must also be subprocess-only, no agent surface):

**(a) Free coverage (already wired):** Tests #3 and #4 iterate `_REFLECT_PY` (L24 glob), so once `src/superclaude/cli/reflect/ensemble.py` exists it is automatically scanned for sprint/roadmap imports and async/await. No edit needed for those two invariants.

**(b) Explicit agent-surface guard (the edit FR-RH2 wants):** The `anthropic`/`subagent`/`Task(` import check is currently scoped to `runner.py` ONLY (test #2, via `_RUNNER_SRC`). To assert ensemble.py also carries no agent-routing surface, add a constant and a new test that mirrors #2 against ensemble.py — OR generalize #2 to a list. Recommended minimal edit:
- Add near L22: `_ENSEMBLE_SRC = _REFLECT_PKG / "ensemble.py"`.
- Add a test mirroring L95-102 that reads `_ENSEMBLE_SRC` and asserts none of `("import anthropic", "from anthropic", "subagent", "Task(")` appear, and (positively) that it dispatches via the transport seam / `ClaudeProcess`, not an agent tool. Reuse `_NESTING_TOKENS` (L46) for the `Task(`/`subagent_type` half.
- Alternatively, define `_AGENT_SURFACE_MODULES = (_RUNNER_SRC, _ENSEMBLE_SRC)` and loop test #2 over it so a single test pins both modules. (Cleaner; one edit point, survives future module additions if the tuple is maintained.)

**Citations:** scan list L24; per-file agent-token loop L99-102; package-wide loops L108 & L122; `_NESTING_TOKENS` L46.

---

## 4. REGRESSION FLOOR — B1/B2/B3 (must stay green UNMODIFIED — FR-RH2.7 / NFR-RH2.6)

| Tag | File | Lines | Pins (one-line) | Patches ClaudeProcess? |
|---|---|---|---|---|
| **B1** | `tests/cli/reflect/test_verdict_mapping.py` | **276** | `contract.derive_verdict` §6 verdict/exit matrix — calls `derive_verdict` DIRECTLY on each fixture, asserts exact `Verdict` + `.exit_code` (0/10/11/2), first-match-wins order blocked→degraded→halted→pass. 22 test fns (L22-263). | **No** — pure function call on YAML fixtures (`derive_verdict(..., expected_tier=2, allow_single_vendor=…, child_rc=…)`), no subprocess. |
| **B2** | `tests/cli/reflect/test_runner_e2e.py` | **220** | Mocked end-to-end `ReflectRunner.run` (launch→parse→verdict→writeback) across the §6 matrix + G1 `max_turns=250` threading (L50) + G2 resume short-circuit (L142-172) + FR-6 fail-closed write-back downgrades (L175-221). | **YES** — patches `superclaude.cli.reflect.runner.ClaudeProcess` via `_PATCH_TARGET` (L22) using `make_claude_process_stub`. This is the file most coupled to the mock gap; the new integration test exists to complement (NOT replace) it. |
| **B3** | `tests/cli/reflect/test_writeback.py` | **172** | FR-6 frontmatter write-back + FR-7 sidecar: atomic success preserves body byte-for-byte & emits §6 `reflect_post`; compare-mismatch bails to `frontmatter-stale` without overwrite + sidecars; CRLF round-trip. 3 test fns (L61, L106, L139). | **No** — calls `write_reflect_post`/`write_sidecar` directly (import L18); patches `write_reflect_post` only inside one case, not ClaudeProcess. |

**Floor rule:** All three must remain green with **zero edits** after FR-RH2. B2 is the canary — it depends on `make_claude_process_stub` and the `pass.yaml` shape; if FR-RH2 changes the emitted contract shape, B1/B2 fixtures break, which is the signal that the contract changed (R2/contract owns that).

---

## 5. SWARM STUB-INTEGRATION PRECEDENT (the MIRROR-SHAPE for `test_ensemble_stub_integration.py`)

**File:** `tests/swarm/test_commands_run.py`, function `test_run_cmd_stub_transport_dispatches_workers_not_noop`.
**TDD anchor L507-568:** **VERIFIED EXACT** — `def` at **L507**, body ends **L568**.

### Structure (the shape to mirror)
1. **Real CLI invocation, NO monkeypatch of the dispatch.** Writes a real target file (L520-526, padded past the IMM-4 non-whitespace-byte floor), then `CliRunner().invoke(run_cmd, [...])` (L529-542) with `--transport stub` (L535-536) — the stub transport is selected by a CLI FLAG, not by patching the process object. This is the seam-injection precedent: choose a deterministic transport, then run the REAL dispatch.
2. **Assert success.** `result.exit_code == EXIT_OK` (L544-547).
3. **KEY ASSERTION — results == workers, not zero (the no-op witness).**
   - `assert "workers=3" in result.stdout` (**L550**).
   - `assert "results=3" in result.stdout` (**L551-554**) — comment: "the F-P3-1 no-op signature was `results=0`". This is the **negative witness** pattern FR-RH2 wants to mirror: prove the real path produced N results, where the bug-signature would be 0.
4. **Assert real side-effects (log events), not just stdout.** `execution-log.jsonl` exists (L559-560); `"worker_done" in log_body` (L562-565); `log_body.count("worker_done") == 3` (**L566-568**) — exactly one terminal event per worker slot.

### Why it is the right mirror for ensemble
It is the canonical "stub transport drives the REAL dispatch, asserts results==workers, fails if it degenerates to a no-op" test. `test_ensemble_stub_integration.py` should: select a StubTransport at the reflect transport seam (NOT patch `ClaudeProcess`), run the REAL `ensemble.py` fan-out, assert the per-reviewer result count equals the configured reviewer count (the positive proof) AND that a degenerate single-call / no-op path would yield a smaller count (the negative witness). Companion non-no-op precedent: `test_dispatch_wave1` style at L490-499 (asserts `call_count==3`, `len(results)==3`, worker indices `[0,1,2]`).

---

## 6. MERGE BOUNDARY TESTS — must stay green after FR-RH2.3

Both filenames CONFIRMED to exist.

- **`tests/swarm/test_merge_loc_ceiling.py`** (77 lines) — enforces NFR-008/AC-018: body of `src/superclaude/cli/swarm/merge.py` must be **≤ 30 LOC** (`LOC_CEILING = 30`, L37). `test_merge_module_body_at_or_below_loc_ceiling` (L54-62) counts non-blank non-module-docstring lines via `_count_body_loc` (L40-51) and asserts `loc <= 30`. `test_merge_module_loc_counter_excludes_module_docstring` (L65-77) sanity-checks the counter (synthetic → 3).
- **`tests/swarm/test_merge_mechanical_only.py`** (191 lines) — pins AC-012/NFR-009: `mechanical_merge` concatenates per-worker `final_path` bodies **verbatim, in slot-index order**, with ONE `## From {model_label} ({elapsed_ms}ms)` provenance header per section — **nothing else (no sort beyond slot index, no score, no dedup, no filter, no rewrite)**. Key asserts: slot order preserved `pos_zero<pos_one<pos_two` (L94); exactly 3 provenance headers (L109); bodies verbatim (L116-118); **no dedup** — `merged.count("DUPLICATE_FINDING") == 2` (L150); empty list → `""` (L154); graceful on missing `final_path`/missing file (L157-191). Module docstring (L9-12) notes this file is a **CI-flagged PR-review-discipline guard** (any PR touching it forces human review).

**Floor rule:** FR-RH2.3 (whatever it touches in merge.py) must keep both green — i.e., must NOT push merge.py past 30 LOC and must NOT add scoring/sort/dedup/filter to the mechanical merge.

---

## 7. POOL-GUARD PRECEDENT for U4 — CORRECTION TO THE TDD

**TDD said:** "`test_inv005_pool_guard.py` — what it asserts about `ModelPoolTooSmallError`."
**FINDING (corrected):** `test_inv005_pool_guard.py` does **NOT** reference `ModelPoolTooSmallError`. `grep -rn "ModelPoolTooSmall"` confirms the class is defined in `src/superclaude/cli/swarm/commands.py:589` and tested by a **different** file: `tests/swarm/test_model_pool_guard.py`. The two are distinct guards:

- **`tests/swarm/test_inv005_pool_guard.py`** (354 lines) — INV-005 *preflight* guard `workers.count` vs the lens-placeholder `spec.workers.models`. Pins `workers_exceed_pool` (detection) + `check_pool_size` (policy-aware) + `run_preflight` wiring. Errors via `PreflightError` / `RULE_WORKERS_EXCEED_POOL` (imports L33-41), reason `"workers-exceed-pool"`, path `"workers.count"`, message names both counts (L216-223). Two policies: warn (clamp+log, project default) vs stop (abort). **No `ModelPoolTooSmallError`.**
- **`tests/swarm/test_model_pool_guard.py`** (the REAL `ModelPoolTooSmallError` precedent for U4) — D2 guard in `_resolve_run_transport_factory`: the *live env* `T2Model0N` pool smaller than worker count must raise `ModelPoolTooSmallError` **eagerly before any slot dispatches** (docstring L1-15). Key asserts (L40-47): `pytest.raises(ModelPoolTooSmallError)`, `err.pool_size == 2`, `err.workers_requested == 3`, message contains `"2 model(s)"` and `"3 worker(s)"`. Equal-pool case returns a usable factory with distinct per-slot models, no wraparound (L50-58). Surfaced at CLI as `EXIT_INVALID` (import L26).

**U4 guidance:** if U4 references "the ModelPoolTooSmallError precedent," cite **`tests/swarm/test_model_pool_guard.py:40-47`** (eager raise naming both counts), NOT `test_inv005_pool_guard.py`. Use `test_inv005_pool_guard.py` only if U4 is about the *preflight* `PreflightError`/policy precedent.

---

## 8. COLLECTION SANITY

`uv run pytest tests/cli/reflect -q --co` → **79 tests collected in 0.37s**, no collection errors. The reflect suite is healthy as a baseline before FR-RH2 work.

---

## SUMMARY (deliverables)

**(a) How to extend `test_no_nesting_guard.py` to `ensemble.py`:**
- Free: the package-wide loops `test_no_sprint_or_roadmap_import_anywhere_in_reflect_pkg` (L108) and `test_no_async_await_anywhere_in_reflect_pkg` (L122) iterate `_REFLECT_PY` (the `glob("*.py")` at **L24**) — they auto-cover `ensemble.py` the moment the file lands. No edit needed for those invariants.
- Explicit edit (FR-RH2's agent-surface guard): the `anthropic`/`subagent`/`Task(` check is `runner.py`-only today (test #2, L95-102, via `_RUNNER_SRC` L22). Add `_ENSEMBLE_SRC = _REFLECT_PKG / "ensemble.py"` and either a mirrored test against it or generalize #2 to loop over `(_RUNNER_SRC, _ENSEMBLE_SRC)`. Reuse `_NESTING_TOKENS` (L46).

**(b) Swarm stub-integration precedent to mirror:** `tests/swarm/test_commands_run.py::test_run_cmd_stub_transport_dispatches_workers_not_noop` (**L507-568**). Shape = pick stub transport via CLI flag (NOT patch the process), run the REAL dispatch, assert `results==workers` (`"results=3"` L551) as the positive proof + a `results=0`-would-mean-no-op negative witness, and assert real side-effects (`worker_done` count == workers, L566-568). The new `test_ensemble_stub_integration.py` mirrors this at the reflect transport seam — it must NOT reuse `make_claude_process_stub`.

**(c) B1/B2/B3 regression floor (stay green, UNMODIFIED):**
- B1 `tests/cli/reflect/test_verdict_mapping.py` (276 L) — direct `derive_verdict` matrix; no ClaudeProcess patch.
- B2 `tests/cli/reflect/test_runner_e2e.py` (220 L) — mocked E2E; **patches ClaudeProcess** (`_PATCH_TARGET` L22) — the file coupled to the mock gap.
- B3 `tests/cli/reflect/test_writeback.py` (172 L) — FR-6/FR-7 write-back+sidecar; no ClaudeProcess patch.

**(d) Full `pass.yaml` key list:** `contract_version`(1.3.0), `status`(success), `mode`(post), `tier_reached`(2, L4), `report_path`, `audit_log_path`, `deviation_count_by_class`{authorized,necessary,drift,regression all 0}, `t2_model_class_diversity`(full), `t2_vendor_diversity`(multi), `adversarial_unavailable`(false), `merge_method`(adversarial), `adversarial_convergence_score`(0.86), `verification_ran`(true), `verification_skip_reason`(null), `citations_dropped`(0), `citations_dropped_extrapolated`(0), `input_drift_detected`(false), `regression_present`(false), `unauthorized_deviation_present`(false), `needs_human_decision`(false), `user_decision_required`(false), `serena_summary_corroboration`(unavailable), `degraded_components`([]).

**TDD anchor corrections logged:** `make_claude_process_stub` L98-138 ✔; `pass.yaml` `tier_reached:2` L4 ✔; no-nesting-guard "L95-102" is only Layer-B test #2 (full guard L80-143); swarm precedent L507-568 ✔; **U4 pool-guard precedent is `test_model_pool_guard.py:40-47`, NOT `test_inv005_pool_guard.py`** (the latter is the preflight `PreflightError` guard, no `ModelPoolTooSmallError`).
