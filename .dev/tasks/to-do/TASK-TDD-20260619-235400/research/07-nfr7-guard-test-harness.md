# 07 — NFR-7 No-Nesting Guard + Test-Harness Mock Gap

- **Topic:** NFR-7 no-nesting guard extension to `ensemble.py`; the conftest `ClaudeProcess` mock gap that hid the Tier-2 defect; FR-RH2.5 stub-integration proof
- **Type:** Code Tracer + Doc Analyst
- **Scope:** `tests/cli/reflect/test_no_nesting_guard.py`, `tests/cli/reflect/conftest.py`, `tests/cli/reflect/fixtures/*.yaml`, backward-compat suite (`test_verdict_mapping.py`, `test_runner_e2e.py`, `test_writeback.py`), swarm stub precedent (`tests/swarm/test_commands_run.py`, `tests/swarm/test_inv005_pool_guard.py`)
- **Status:** Complete
- **Date:** 2026-06-19 (updated 2026-06-20)

---

## Investigation Log

(appended incrementally)

### Ground-truth file inventory `[CODE-VERIFIED]`

- `src/superclaude/cli/reflect/` contains exactly: `commands.py`, `config.py`, `contract.py`, `__init__.py`, `models.py`, `runner.py`. **`ensemble.py` does NOT exist yet** — it is the FR-RH2 module to be created. (`ls`, 2026-06-19/20.)
- `tests/cli/reflect/test_ensemble_stub_integration.py` **does NOT exist yet** — it is the FR-RH2.5 test to be authored. The reuse-audit "mirror-shape" verdict is therefore a *prospective* recommendation for the test to be written.
- `tests/cli/reflect/fixtures/` holds 13 `.yaml` fixtures + `__init__.py`. `pass.yaml` (712 bytes) and `degraded_single_vendor.yaml` (713 bytes) are the load-bearing ones for this analysis.

---

## Part 1 — The two-layer NFR-7 no-nesting guard (current state)

File: `tests/cli/reflect/test_no_nesting_guard.py` (143 lines). Module docstring (L1-9) states the two layers explicitly: **Layer A** = the task-builder SKILL SOURCE shells out via Bash and contains no Agent/Task nesting tokens; **Layer B** = `runner.py` launches reflect ONLY via the `ClaudeProcess` subprocess primitive, no agent-surface imports.

### Constants (L18-46) `[CODE-VERIFIED]`

```
_REPO_ROOT     = parents[3]                                    # L19
_SKILL_SRC     = src/superclaude/skills/task-builder/SKILL.md  # L20
_REFLECT_PKG   = src/superclaude/cli/reflect                   # L21
_RUNNER_SRC    = _REFLECT_PKG / "runner.py"                    # L22
_REFLECT_PY    = sorted(*.py in pkg, excluding __init__.py)    # L24  <-- package-wide glob
```

Regexes (all `re.MULTILINE`, anchored to avoid docstring-prose false positives):
- `_SPRINT_ROADMAP_IMPORT_RE` (L29-31): `^\s*(?:from|import)\s+\S*(?:sprint|roadmap)` — bans heavy-sibling imports (NFR-1).
- `_ASYNC_DEF_RE` (L33): `^\s*async\s+def\b`; `_AWAIT_RE` (L34): `^\s*await\s`.
- `_RAW_SUBPROCESS_CALL_RE` (L38): `\b(?:subprocess\.(?:run|Popen)|Popen)\s*\(` — matches a real CALL (identifier.method + `(`), not docstring prose.
- `_IMPORT_SUBPROCESS_RE` (L39-41): `^\s*(?:import\s+subprocess|from\s+subprocess\b)`.
- `_NESTING_TOKENS = ("Task(", "subagent_type")` (L46) — the *prose-safe* nesting tuple used by Layer A.

### Layer A — `test_layer_a_wrapper_branch_is_bash_shellout` (L68-92) `[CODE-VERIFIED]`

Currently decorated `@pytest.mark.xfail(strict=False)` (L68-79) because the marker migrated from the abandoned `Mode 2` taxonomy to the flat `superclaude reflect run` contract; it XPASSes against this worktree's live emission.

`_extract_wrapper_branch` (L49-65) slices the SKILL text between anchor `"Independent post-execution reflection gate (wrapper shell-out)"` (L61) and the next bullet `"- [ ] **N.X"` (L64). The test then asserts on that slice:
- POSITIVE: `"superclaude reflect run"`, `"--depth deep"`, `"--fix"` present (L85-87); recursion-breaker `"SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"` present (L89).
- NEGATIVE: for `token in _NESTING_TOKENS` (`Task(`, `subagent_type`), assert `token not in branch` (L91-92).

**What Layer A scans:** the *skill shell-out text block* — it proves the SKILL emits a Bash CLI call (not an Agent/Task spawn) for the terminal reflect gate. It does NOT scan Python source.

### Layer B — `test_layer_b_wrapper_module_has_no_agent_imports` (L95-102) `[CODE-VERIFIED]`

```python
src = _RUNNER_SRC.read_text(...)               # runner.py ONLY
assert "ClaudeProcess" in src                  # L98 positive witness
for banned in ("import anthropic", "from anthropic", "subagent", "Task("):
    assert banned not in src                   # L99-102 negative witness
```

**What Layer B scans:** `runner.py` ONLY (single file via `_RUNNER_SRC`). Bans the literal substrings `import anthropic`, `from anthropic`, `subagent`, `Task(`. These are bare-substring checks (not the anchored regexes), so they would false-positive on docstring prose — but `runner.py`'s docstring is written to avoid those exact tokens (L11 says "never an Agent/Task" with a slash, not "Task(").

### The other three guards (package-wide vs runner-scoped) `[CODE-VERIFIED]`

- `test_no_sprint_or_roadmap_import_anywhere_in_reflect_pkg` (L105-113): iterates **all** `_REFLECT_PY` files, applies `_SPRINT_ROADMAP_IMPORT_RE`. **Package-wide.**
- `test_no_async_await_anywhere_in_reflect_pkg` (L116-125): iterates **all** `_REFLECT_PY`, applies `_ASYNC_DEF_RE` + `_AWAIT_RE`. **Package-wide.**
- `test_apply_remediation_launches_only_via_claudeprocess` (L128-142): scoped to **`runner.py` only** (L131-133 docstring explains: `commands.py:267-274` legitimately uses `subprocess.run` for `--tmux`). Asserts `ClaudeProcess`, `_apply_remediation`, `/task ` present; `_RAW_SUBPROCESS_CALL_RE` and `_IMPORT_SUBPROCESS_RE` absent.

**Key structural observation:** the raw-`subprocess` ban is currently **runner.py-scoped, not package-wide** — because `commands.py` is allowed to call `subprocess.run` for the `--tmux` launch. This is the seam FR-RH2.8 must navigate.

---

## Part 2 — (a) Extending the guard to `ensemble.py` (FR-RH2.8)

The guard must, post-change, forbid in **both `runner.py` AND `ensemble.py`**: `Task(` / `subagent` / `import anthropic` / `from anthropic` AND raw `subprocess.run`/`Popen` calls + `import subprocess`. The cleanest minimal extension, consistent with the existing structure:

1. **Add a constant** `_ENSEMBLE_SRC = _REFLECT_PKG / "ensemble.py"` next to `_RUNNER_SRC` (L22).
2. **Define a guarded-module set:** `_NO_NEST_SRCS = [_RUNNER_SRC, _ENSEMBLE_SRC]` (the two modules that may dispatch reviewers/launch children). This is the precise scope: NOT package-wide for the raw-subprocess ban (because `commands.py` keeps its legitimate `--tmux` `subprocess.run`), but no longer single-file.
3. **Generalize `test_layer_b_...`** to loop over `_NO_NEST_SRCS`, asserting `"ClaudeProcess" in src` (positive) and the four banned agent-surface substrings absent (negative) for each. Equivalently, parametrize on the module.
4. **Generalize `test_apply_remediation_launches_only_via_claudeprocess`** (the raw-subprocess ban) to loop over `_NO_NEST_SRCS`, applying `_RAW_SUBPROCESS_CALL_RE` + `_IMPORT_SUBPROCESS_RE` to each. The `_apply_remediation` / `/task ` positive witnesses remain runner-scoped (they are runner-specific), but the **negative** raw-subprocess witnesses extend to `ensemble.py`.
5. **`_REFLECT_PY` already auto-covers `ensemble.py`** for the sprint/roadmap-import and async/await package-wide guards (it globs `*.py`), so those two tests need **no change** — once `ensemble.py` lands, it is automatically scanned. This is a free win worth stating in the TDD: the async/await + sprint/roadmap guards are already future-proof.

**Net regex/assertion delta for FR-RH2.8:**
- New constant `_ENSEMBLE_SRC`; new list `_NO_NEST_SRCS`.
- `test_layer_b` and `test_apply_remediation` change from single-file `read_text(_RUNNER_SRC)` to a per-module loop over `_NO_NEST_SRCS`.
- No new regex needed — reuse `_RAW_SUBPROCESS_CALL_RE`, `_IMPORT_SUBPROCESS_RE`, and the `("import anthropic", "from anthropic", "subagent", "Task(")` tuple.
- **Caveat to flag in the TDD:** if `ensemble.py` legitimately needs to fan out reviewer subprocesses, the ban on `subprocess.run`/`Popen` forces dispatch through `ClaudeProcess` (or an injected transport) — the guard *intends* this (it is the NFR-7 no-nesting invariant). The stub-integration test (Part 4) must therefore inject a `StubTransport`, not monkeypatch `subprocess`.

---

## Part 3 — THE MOCK GAP: how "Tier 2 works" was a fixture assertion, never behavior

File: `tests/cli/reflect/conftest.py` (189 lines). The relevant region is `make_claude_process_stub` at **L98-138** (task brief said ~L98-138 — confirmed exact).

### The `ClaudeProcess` stub factory mechanics `[CODE-VERIFIED]`

`make_claude_process_stub` (L98) returns a builder `_builder(fixture_name, rc=0, write_contract=True)` (L114-136):

1. **At build time (L117-119):** if `fixture_name is not None`, eagerly read the canned fixture bytes: `fixture_bytes = (FIXTURES_DIR / fixture_name).read_bytes()`.
2. **`factory(**kwargs)` (L121):** resolves `output_dir = Path(kwargs["output_file"]).parent` (L122-123), builds a bare `MagicMock()` (L124), sets `mock.start.return_value = None` (L125) — `.start()` is a **no-op**.
3. **`_wait()` closure (L127-131):** when `write_contract and fixture_name is not None`, it `mkdir(parents=True)` then writes **`(output_dir / "return-contract.yaml").write_bytes(fixture_bytes)`** and returns `rc`. This is the entire "subprocess": copy a canned YAML into place, return an exit code.
4. **`mock.wait.side_effect = _wait`** (L133) — so `proc.wait()` triggers the copy.

**The gap, stated precisely:** No real `claude` subprocess ever runs. No reviewer is ever dispatched. No merge/reduce ever happens. The `return-contract.yaml` the runner parses is a **byte-for-byte copy of a hand-authored fixture** placed there by `.wait()`. The runner then `parse_contract`s it and `derive_verdict`s it — but every field it reads (`tier_reached`, `t2_vendor_diversity`, `merge_method`, `adversarial_convergence_score`) is **whatever the fixture author typed**, not anything the system computed.

### `pass.yaml` hard-codes `tier_reached: 2` `[CODE-VERIFIED]`

`tests/cli/reflect/fixtures/pass.yaml` L4 is literally `tier_reached: 2`, with L12 `t2_model_class_diversity: full`, L13 `t2_vendor_diversity: multi`, L15 `merge_method: adversarial`, L16 `adversarial_convergence_score: 0.86`. Every "Tier-2 succeeded with full diversity and adversarial merge" property is a **typed constant in the fixture**.

**Therefore:** the existing e2e suite proves `derive_verdict(pass.yaml) → PASS/exit 0` — i.e., *the verdict mapping correctly reads a contract that claims tier 2*. It proves NOTHING about whether the ensemble actually reached tier 2, dispatched ≥2 reviewers, or merged adversarially. "Tier 2 works" was an **assertion baked into the fixture**, validated against itself. This is exactly the representational-bias trap: the test and the thing-under-test share the same fabricated witness.

### The sequence variant (L141-188) `[CODE-VERIFIED]`

`make_claude_process_sequence` (L141) is the same trick for the bounded fix-loop: `_builder(steps)` pops `(fixture_name, rc)` per construction (L163-186); `fixture_name=None` writes NO contract (the apply `/task` launch); exhausted sequence defaults to `(None, 0)` (L169). Same mock gap — every audit step's contract is a canned fixture, never a computed result.

---

## Part 4 — (b) WHY FR-RH2.5's stub proof must NOT reuse the canned-fixture path

The canned-fixture path (`make_claude_process_stub` → fixture-copy → `parse_contract` → `derive_verdict`) **short-circuits the entire ensemble**. If FR-RH2.5 reused it, the test would once again assert against a YAML the author wrote — re-creating the exact mock gap that hid the original Tier-2 defect. A `pass.yaml`-driven e2e can be 100% green while `ensemble.py`'s real dispatch→reduce→derive is broken or absent.

**FR-RH2.5's stub proof must instead exercise the REAL flow** — `ensemble.dispatch(...)` → `reduce(...)` → `derive_verdict(...)` — with the reviewer LLM calls replaced by a `StubTransport` (a deterministic in-process fake that returns canned *per-reviewer* responses), NOT by pre-writing the final `return-contract.yaml`. The contract must be **produced by the real reduce step from real (stubbed) reviewer outputs**, so the test proves:
- the dispatch actually fans out N reviewers,
- reduce actually counts them and sets `tier_reached` / `merge_method` / diversity from observed reviewers,
- `derive_verdict` then maps that *computed* contract.

The boundary moved one layer down: stub the **transport** (the thing that would call out to a model), let **everything above it run for real**. This is precisely the swarm F-P3-1 lesson (Part 5): "real stub dispatch is NOT a no-op."

### Grounding the witnesses against `contract.derive_verdict` `[CODE-VERIFIED]`

The positive/negative assertions below are enforceable because `derive_verdict`'s degraded triggers already key on these exact fields (`src/superclaude/cli/reflect/contract.py`, `_degraded_reason`, L249-304):
- **Trigger 6** `degraded-tier1` (L263): `expected_tier >= 2 and tier_reached == 1`.
- **Trigger 8** `single-vendor` (L272): `t2_vendor_diversity == "single" and not allow_single_vendor`.
- **Trigger 10** `single-reviewer-fallback` (L280-281): `merge_method == "single-reviewer-fallback"`.

So a 1-reviewer reduce that writes `tier_reached: 1` and/or `merge_method: single-reviewer-fallback` deterministically routes DEGRADED / exit 11 — the negative witness is grounded in real verdict logic, not a fixture.

---

## Part 5 — (c) The stub-integration test template shape

### Swarm precedent `[CODE-VERIFIED]`

`tests/swarm/test_commands_run.py::test_run_cmd_stub_transport_dispatches_workers_not_noop` (L507-568) is the canonical "real stub dispatch" template:
- Builds a real target file (L520-526), invokes the REAL `run_cmd` with `--transport stub` (no monkeypatch of the dispatcher; L529-542).
- POSITIVE witness: `result.exit_code == EXIT_OK` (L544), `"workers=3" in result.stdout` (L550), `"results=3" in result.stdout` (L551-554) — *results == workers*, NOT zero.
- Behavioral artifact witness: `execution-log.jsonl` exists (L559-560), contains `worker_done` (L562), and `log_body.count("worker_done") == 3` (L566-568) — proves the fan-out actually happened, not just a stdout string.
- The docstring (L510-519) names the anti-pattern explicitly: pre-fix, `run_cmd` passed `transport=None` to `dispatch_wave1`, which "short-circuits to an empty list — so a real `swarm run` produced `results=0`." The stub transport makes the dispatch run for real.

Companion at L480-499 (`dispatch_wave1` with a `_RecordingTransport`): asserts `call_count == 3`, `len(results) == 3`, and `[r.index for r in results] == [0, 1, 2]` — the *results==workers* + slot-order invariant at the function level.

`tests/swarm/test_inv005_pool_guard.py` is the pool-guard precedent: detection helper (`workers_exceed_pool`, parametrized L191-208) pinned separately from policy emission (`check_pool_size`, L216-253) pinned separately from end-to-end wiring (`run_preflight`, L261-354). The two-tier "pin the helper, then pin the wiring" structure is the model for testing `ensemble`'s reviewer-count/diversity logic distinctly from its dispatch wiring.

### Reuse-audit re-confirmation `[CODE-VERIFIED]`

Recorded verdict: `tests/cli/reflect/test_ensemble_stub_integration.py` = **mirror-shape** of `tests/swarm/test_commands_run.py`'s stub pattern. **Re-confirmed:** the new reflect test does not yet exist (`ls` miss), so it cannot reuse-by-import; the swarm stub pattern lives in a different package (`cli/swarm` vs `cli/reflect`) with a different transport surface. The correct relationship is **mirror-shape** — replicate the *structure* (real dispatch under an injected stub transport + results==N + behavioral-artifact witnesses at L507-568 / L480-499), authored against the reflect ensemble's own API. Not extract-shared (the two transports/CLIs differ enough that a shared helper would over-couple), not reuse-by-import.

### Template shape for `test_ensemble_stub_integration.py`

**Positive witness (≥2 reviewers):** drive the real `ensemble` dispatch→reduce with a `StubTransport` returning ≥2 distinct reviewer responses, then assert the *computed* contract / result satisfies:
- `tier_reached == 2`,
- `reviewer_count >= 2` (results == workers, the swarm L551 analogue),
- `merge_method != "single-reviewer-fallback"` (e.g. `== "adversarial"`),
- diversity == "full" (`t2_model_class_diversity == "full"`),
- and the end-to-end verdict via `derive_verdict` is `Verdict.PASS` / exit 0.

**Negative witness (1 reviewer):** same real flow, `StubTransport` returns a single reviewer response, then assert:
- the reduce sets `tier_reached == 1` and/or `merge_method == "single-reviewer-fallback"`,
- `derive_verdict(...)` → `Verdict.DEGRADED` / exit 11 with reason `single-reviewer-fallback` (or `degraded-tier1`),
- **and the positive assertions FAIL here** — i.e. explicitly assert `reviewer_count < 2`, `tier_reached != 2`, diversity != "full". This is the mutation-catching contrast: the same harness that greens on ≥2 reviewers must go red (degraded) on 1, proving the assertions are wired to *observed reviewer count*, not a fixture constant.

The defining contrast vs the canned-fixture path: in the positive witness the `tier_reached: 2` field is **produced by reduce from 2 stubbed reviewers**, whereas in `pass.yaml` it is a typed constant. That single difference is the whole point of FR-RH2.5.

---

## Key Takeaways

1. **Layer A** scans the task-builder SKILL shell-out text block (anchored slice) proving a Bash `superclaude reflect run --depth deep --fix` call with the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion-breaker and NO `Task(`/`subagent_type`. **Layer B** scans `runner.py` ONLY for `ClaudeProcess` presence + absence of `import/from anthropic`, `subagent`, `Task(`.
2. **FR-RH2.8 extension (a):** add `_ENSEMBLE_SRC` + a `_NO_NEST_SRCS = [_RUNNER_SRC, _ENSEMBLE_SRC]` list; loop the Layer-B agent-import test and the raw-`subprocess` test over both modules. Reuse existing regexes (`_RAW_SUBPROCESS_CALL_RE`, `_IMPORT_SUBPROCESS_RE`) — no new regex. The package-wide async/await + sprint/roadmap guards already auto-cover `ensemble.py` via the `_REFLECT_PY` glob (no change). Keep the raw-subprocess ban scoped to the two no-nest modules, NOT package-wide (`commands.py` keeps its `--tmux` `subprocess.run`).
3. **The mock gap (Part 3):** `conftest.py` L98-138's `make_claude_process_stub` makes `.wait()` copy a canned `fixtures/*.yaml` into `return-contract.yaml`. `pass.yaml` L4 hard-codes `tier_reached: 2`. So "Tier 2 works" was a fixture assertion validated against itself — no dispatch, no reduce, no reviewers ever ran.
4. **(b) FR-RH2.5 must NOT reuse the canned path** — that path short-circuits the ensemble and re-creates the gap. It must run the REAL dispatch→reduce→derive_verdict with a `StubTransport`, so `tier_reached`/`merge_method`/diversity are COMPUTED from stubbed reviewer outputs, then mapped by `derive_verdict`.
5. **(c) Template = swarm mirror-shape:** positive witness (≥2 reviewers → tier 2 / reviewer_count≥2 / merge≠single-reviewer-fallback / diversity full / PASS) + negative witness (1 reviewer → degraded / exit 11 / single-reviewer-fallback, and the positive assertions FAIL). Mirrors `test_commands_run.py` L507-568 (`results==workers`, behavioral-artifact witnesses) and the two-tier pin structure of `test_inv005_pool_guard.py`.

## Gaps and Questions

- **`[UNVERIFIED]` — `ensemble.py` API surface.** The module does not exist yet, so the exact function names (`dispatch`, `reduce`, `derive_verdict` re-entry), the `StubTransport` injection point, and whether `reviewer_count` is a contract field or a result attribute are TDD design decisions, not facts. The witness field names above (`reviewer_count`, diversity) are inferred from `derive_verdict`'s existing trigger fields (`t2_vendor_diversity`, `t2_model_class_diversity`, `merge_method`, `tier_reached`) — the TDD must define the canonical names.
- **`[UNVERIFIED]` — NFR-RH2.6 backward-compat scope.** I documented what `test_verdict_mapping.py`, `test_runner_e2e.py`, `test_writeback.py` assert today (below), but whether FR-RH2 keeps these EXACTLY green or expects updates (e.g. if `pass.yaml` gains reviewer fields) is a design choice. As written, the e2e suite drives the SINGLE-`ClaudeProcess` runner; if `ensemble.py` changes the launch path, `make_claude_process_stub` may need an ensemble-aware variant for these to stay representative.
- **`[CODE-VERIFIED]` backward-compat suite content (NFR-RH2.6):**
  - `test_verdict_mapping.py` (277 lines): calls `derive_verdict` directly against fixtures; pins the §6 matrix (PASS/0, HALTED/10, DEGRADED/11, BLOCKED/2), first-match ordering, single-vendor flag behavior (L67-88), fail-loud unknown major version (L119-128), NFR-8 unknown-field tolerance (L131-140), and the F0/F2/F5 fail-closed fixes (L204-277: child-crash veto, malformed-boolean block, status-failed reason).
  - `test_runner_e2e.py` (221 lines): drives the real `ReflectRunner.run` with `ClaudeProcess` patched to the Idiom-B factory; asserts verdict + exit code + `reflect_post.verdict` write-back for pass/halted/degraded/blocked, G1 `max_turns==250` threading (L49-50), G2 resume short-circuit (L142-172), and FR-6 fail-closed write-back downgrades (L175-221).
  - `test_writeback.py` (173 lines): pins `write_reflect_post`/`write_sidecar` — atomic write-back preserves body byte-for-byte + emits §6 block (L61-104), compare-mismatch → `frontmatter-stale` no-overwrite + sidecar (L106-136), CRLF round-trip → `written` (L139-172).
  - These must stay green through FR-RH2 because they pin the verdict-mapping + write-back contracts that `ensemble.py` feeds into — they are the regression floor.

## Summary

The NFR-7 guard (`test_no_nesting_guard.py`) is structurally ready to extend to `ensemble.py` with a small, regex-reusing change: introduce `_ENSEMBLE_SRC` + `_NO_NEST_SRCS` and loop the Layer-B agent-import and raw-subprocess tests over both modules; the package-wide async/await and sprint/roadmap guards already auto-cover the new file via the `_REFLECT_PY` glob. The defect that hid Tier-2 breakage is concrete and proven: `conftest.py` L98-138 makes the stubbed `ClaudeProcess.wait()` copy a hand-authored `fixtures/*.yaml` (e.g. `pass.yaml` L4 `tier_reached: 2`) into `return-contract.yaml`, so every "Tier 2 / full diversity / adversarial merge" property the e2e suite reads is a typed fixture constant — never a computed result. FR-RH2.5's stub proof must therefore abandon the canned-fixture path and exercise the real `ensemble` dispatch→reduce→derive_verdict under an injected `StubTransport`, with a positive witness (≥2 reviewers → tier 2 / reviewer_count≥2 / merge≠fallback / diversity full / PASS) and a negative witness (1 reviewer → degraded / exit 11 / single-reviewer-fallback where the positive assertions FAIL). That shape mirrors `tests/swarm/test_commands_run.py` L507-568 ("real stub dispatch is NOT a no-op", results==workers, behavioral-artifact witnesses) — confirming the reuse verdict of **mirror-shape** for the not-yet-existing `test_ensemble_stub_integration.py`, authored against reflect's own API rather than imported from swarm.
