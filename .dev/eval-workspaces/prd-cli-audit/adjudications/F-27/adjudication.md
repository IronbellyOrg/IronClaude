# F-27 Adjudication — Test surface gaps (`_evaluate_gate`, mock harness, CLI knobs)

**Mode**: B (three personas → convergence)
**Source finding**: `.dev/eval-workspaces/prd-cli-audit/findings/F-27-test-surface-gaps.md`
**Preliminary severity**: MEDIUM
**Pattern tags**: P6, P9

---

## Re-verification ledger

| # | Claim | Verification | Status |
|---|-------|--------------|--------|
| 1 | `tests/cli/prd/test_integration.py:197-223` is the ONLY `_evaluate_gate` test call site | `grep -rn "_evaluate_gate" tests/` returns exactly two lines, both inside `test_prd_pipeline_gate_enforcement` (`tests/cli/prd/test_integration.py:208` and `:222`) — same function, same hand-built content path | CONFIRMED |
| 2 | Gate is fed hand-built content, never the result of `_resolve_step_content` | `tests/cli/prd/test_integration.py:211` passes `"This content has no GOAL or PRODUCT_SLUG..."`; `:216-221` passes a literal `valid_content` string; neither call ever reaches the disk-vs-stream resolver | CONFIRMED |
| 3 | Mock harness conflates stream and disk | `tests/cli/prd/test_e2e.py:245-250` writes the pre-cooked passing content directly to `output_file` (the NDJSON stream path passed in via `kwargs["output_file"]`). No second write to `task_dir/<resolved-artifact-name>` ever happens | CONFIRMED |
| 4 | No "two-actor" mock exists anywhere in the test surface | `grep -n "two-actor\|two_actor\|commentary\|stream.*disk\|disk.*stream" tests/cli/prd/*.py` returns zero hits | CONFIRMED |
| 5 | Structural claim: tests CANNOT distinguish "gate read disk" from "gate read stream" | Because every e2e mock writes the *full* passing artifact to the stream file (`tests/cli/prd/test_e2e.py:247`), `_resolve_step_content` (`src/superclaude/cli/prd/executor.py:254-293`) finds nothing useful on disk under `task_dir.rglob(artifact_name)` and falls back to `ndjson_text`. The gate then passes on the stream content — but the test cannot tell whether the gate passed because (a) the resolver found a disk artifact or (b) the resolver fell back to stream. Both produce identical observable behavior in this mock. | CONFIRMED |
| 6 | CLI knob coverage is string-presence-only | `tests/cli/prd/test_cli_smoke.py:1-79` checks `--help` listings, dry-run config echoing, and tier-name string presence (`:78` asserts `"heavyweight" in result.output`). No test wires a tier through to an executed pipeline and asserts the tier-specific gate threshold was applied. `--where` has zero behavioral test references. | CONFIRMED |

All six structural claims from F-27 are reproducible. No claim was overstated.

---

## Persona 1 — Analyzer (reproducibility)

**Question**: Bug 1 / F-01 (`build-task-file` missing from `_STEP_ARTIFACT_FILES`) shipped because no test exercised the real chain. Can the existing harness even support a test that would have caught it?

**Trace of F-01 in production**:
1. `_STEP_ARTIFACT_FILES` lookup at `src/superclaude/cli/prd/executor.py:267` returns `None` for `build-task-file`.
2. `_resolve_step_content` short-circuits at `:268-269`, returning `ndjson_text` (~30 lines of subprocess commentary).
3. `_evaluate_gate` (`:532`) receives commentary, sees `min_lines=400` required, halts STRICT.

**Could `test_prd_pipeline_gate_enforcement` (`test_integration.py:197-223`) have caught this?**
No. It calls `_evaluate_gate` directly with literal strings (`:208`, `:222`), bypassing `_resolve_step_content` entirely. F-01 lives in the dispatch-table-to-resolver edge, not in the gate predicate itself.

**Could the e2e harness (`test_e2e.py:224-253`) have caught this?**
No, and this is the architectural finding. The mock factory at `:245-250` writes the passing content directly to the `output_file` path (the NDJSON stream). When `_resolve_step_content` runs for `build-task-file`, the dispatch-table lookup returns `None`, the function falls back to `ndjson_text`, and `ndjson_text` happens to contain the full passing content because the mock conflated the two channels. F-01 is invisible to this harness — the bug is mechanically masked by the mock shape.

**What would catch F-01?**
A two-actor mock where the side_effect writes:
- A short commentary string (~30 lines, `EXIT_RECOMMENDATION: CONTINUE` only) to `output_file` (simulating real `ClaudeProcess` NDJSON output)
- The full passing artifact to `task_dir / <resolved-artifact-name>` (simulating the subprocess's `Write` tool call)

With that harness, every step whose `step_id` is missing from `_STEP_ARTIFACT_FILES` would fail its gate immediately. F-01 would have surfaced on the first run.

**Infrastructure delta**: Replacing `write_output_and_return` (`test_e2e.py:245-250`) with a two-path writer is ~10 lines. The fixture knows `task_dir` (it's in `kwargs["task_dir"]` or derivable from `output_file.parent.parent`). No new dependencies, no new abstractions — just stop conflating the channels in the mock. The fact that this hasn't been done is the meta-defect.

**Analyzer verdict**: Finding is reproducible and the structural claim is sharp. The existing harness cannot, in its current shape, distinguish disk-source from stream-source content — which is precisely the contract `_resolve_step_content` exists to enforce. **Severity stays MEDIUM at minimum; arguments for HIGH below.**

---

## Persona 2 — Refactorer (blast radius)

**Question**: Are similar structural test gaps elsewhere? Mock factories that always succeed too easily?

**Survey of CLI test mock surface**:
- `grep -rln "MagicMock\|mock_factory" tests/cli/` returns *only* `tests/cli/prd/test_e2e.py`. The CLI test surface has one mock factory, and it's the one F-27 flags.
- Within that file: every `_mock_process_factory` invocation (`test_e2e.py:274, 333, 393, 443, 522`) inherits the same conflation. All five scenarios (standard, lightweight, fix-cycle, fan-out, budget-exhaustion) share the defect.
- Smoke tests (`test_cli_smoke.py`) don't mock — they invoke `--dry-run` or `--help`, so they don't exercise the chain at all.
- `test_executor.py`, `test_gates.py`, `test_filtering.py`, `test_path_resolution.py`, `test_inventory.py`, `test_models.py`, `test_config.py`, `test_prompts.py`, `test_research_notes_roundtrip.py` are unit tests over isolated predicates — they don't claim to exercise the integration chain.

**Pattern observation (P9 — "happy-path mocks")**:
The mock writes `exit_code = 0` (`test_e2e.py:240`) and full passing content (`:241`) by default. Overrides exist (`step_overrides`), but the default shape is "subprocess succeeded with valid output." Any defect in the *resolution* path between subprocess completion and gate evaluation is invisible because the mock pre-resolves it.

This is a single-point-of-failure in the test architecture: one mock factory, used by every e2e test, baking in one wrong assumption (stream == disk artifact). Fixing it once fixes every e2e scenario simultaneously — but until it's fixed, no e2e scenario can catch a dispatch-table or resolver bug.

**Blast radius**: All five e2e scenarios are affected by the same mock defect. No other mock factories exist in the CLI test surface, so there is no parallel structural gap to address — but there is also no second line of defense. The integration test (`test_integration.py:197-223`) is the only other gate-touching test, and it bypasses the resolver entirely. The CLI test surface has **zero tests** that exercise `_STEP_ARTIFACT_FILES` → `_resolve_step_content` → `_evaluate_gate` end-to-end.

**Refactorer verdict**: Blast radius is "all e2e tests, one fix." This argues for **fixing it once** rather than re-scoring severity upward. But the absence of a second line of defense (no other path through the chain is tested) means the dispatch-table edge is structurally unguardable today.

---

## Persona 3 — Architect (severity calibration)

**Question**: Preliminary MEDIUM. Is this a process gap or a defect-severity-equivalent?

**The case for MEDIUM (preliminary stance)**:
- No user-facing behavior is currently broken by F-27 itself. F-27 is the *reason* F-01 shipped, not F-01.
- Test gaps are conventionally rated MEDIUM unless they actively produce wrong assertions.
- Cost of fixing is ~10 lines in `_mock_process_factory`.

**The case for HIGH**:
- F-27 is the *meta-defect*. It is causally responsible for F-01 (CRITICAL) shipping to production. F-01 is rated CRITICAL because it halts the pipeline; F-27 is the structural condition that let F-01 in.
- The dispatch table `_STEP_ARTIFACT_FILES` (`src/superclaude/cli/prd/executor.py:246-251`) is a hand-maintained mapping that must stay in sync with `_STAGE_A_STEPS` (`:301-316`) and `_STAGE_B_*` step lists. The current test surface cannot catch drift in this mapping. Any future step added to `_STAGE_*_STEPS` without a corresponding `_STEP_ARTIFACT_FILES` entry will repeat F-01.
- The "fool me once" calibration: the dispatch table already drifted once (F-01). Without F-27 remediation, it will drift again.
- The mock conflation also masks any future defect in `_resolve_step_content`'s search/skip logic (`:280-291`) — e.g., if the skip set (`node_modules`, `.git`, `__pycache__`) ever misses a new exclusion case, no e2e test will notice.

**Severity calibration framework**:
- *Defect severity* = blast radius × likelihood × user impact of the underlying bug.
- *Meta-defect severity* = defect severity of the worst bug it can mask × probability the meta-defect masks similar bugs in the future.
- F-01 is CRITICAL. Dispatch-table maintenance is recurring (every new step requires updating two lists). Probability of repeat: HIGH. Therefore F-27 inherits a severity floor close to F-01's CRITICAL rating, discounted by the fact that F-27 alone causes no user-facing failure.

**Architect verdict**: Preliminary MEDIUM is **defensible but soft**. The structural argument (this is the meta-defect that allowed CRITICAL F-01 to ship and will allow similar bugs to ship) supports **HIGH**. Final calibration: **HIGH**, on the grounds that "process gap with proven causal link to a CRITICAL bug, in a hand-maintained dispatch table requiring ongoing maintenance" is materially worse than a generic missing-test-case.

---

## Convergence

| Dimension | Value |
|---|---|
| **Verdict** | VALID — finding is fully reproducible; all six structural claims hold under verification |
| **Convergence score** | 0.95 — all three personas agree the finding is real and well-scoped; only disagreement is on severity (MEDIUM vs HIGH), and Refactorer + Architect both lean toward upgrade |
| **Final severity** | **HIGH** (upgraded from MEDIUM) |
| **Fix difficulty** | LOW — ~10-line rewrite of `_mock_process_factory` (`tests/cli/prd/test_e2e.py:245-250`) into a two-actor mock; plus add one positive test that wires `_resolve_step_content` → `_evaluate_gate` through a real `task_dir` with a known-good artifact; plus three CLI-knob behavioral tests (`--tier` threshold application, `--where` placement, `--output` placement) |
| **Pattern tags** | P6 (test surface gap), P9 (happy-path mock), plus newly recognized **P-meta** (test infrastructure cannot guard the very contract it claims to test) |

### Synthesis

F-27 documents the architectural reason F-01 shipped. The PRD CLI test surface has exactly one test that calls `_evaluate_gate` (`tests/cli/prd/test_integration.py:197-223`), and it bypasses `_resolve_step_content` by feeding hand-built strings. The only mock factory that drives e2e scenarios (`tests/cli/prd/test_e2e.py:224-253`) writes the full passing artifact directly into the NDJSON stream file, conflating two channels that production code is specifically designed to disambiguate. As a result, the test surface is mechanically incapable of detecting drift between `_STEP_ARTIFACT_FILES` (`src/superclaude/cli/prd/executor.py:246-251`) and the step lists in `_STAGE_*_STEPS`. Bug F-01 — `build-task-file` missing from the dispatch table — was the inevitable consequence and will recur with any future step addition unless the meta-defect is fixed.

Severity upgrade from MEDIUM to HIGH is warranted on three grounds: (1) causal link to a shipped CRITICAL bug, (2) the dispatch table requires ongoing hand maintenance with no automated guard, and (3) the same mock conflation will mask future resolver defects (skip-set drift, search-root drift, artifact-name drift). Fix difficulty remains LOW because the remediation is a localized rewrite of one mock factory plus a small handful of new tests — not an architectural rework.

**Recommended remediation order** (LOW effort, HIGH leverage):
1. Rewrite `_mock_process_factory` to accept a `disk_artifact` kwarg and write commentary-only NDJSON to `output_file` while writing real artifact content to `task_dir / <resolved-artifact-name>`. This single change forces every existing e2e scenario to exercise the real `_resolve_step_content` path.
2. Add a regression test asserting every entry in `_STAGE_A_STEPS + _STAGE_B_*` that produces an artifact has a corresponding `_STEP_ARTIFACT_FILES` entry. Pure invariant test; catches future F-01-class bugs at PR time.
3. Add three behavioral CLI-knob tests: `--tier heavyweight` invokes heavyweight gate thresholds, `--where <path>` resolves correctly, `--output <path>` places artifacts at the user-supplied location.
