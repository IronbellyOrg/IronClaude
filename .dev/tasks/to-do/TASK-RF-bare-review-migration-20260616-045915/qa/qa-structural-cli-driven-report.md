# QA Report — Report Validation (Phase Gate 4, CLI-driven lens)

**Topic:** sc-bare-review M8/M9 migration — rebuilt parity gate is CLI-driven, not library-level
**Date:** 2026-06-16
**Phase:** report-validation (structural CLI-driven verification)
**Fix cycle:** N/A (fix_authorization: FALSE — report only)
**Stance:** ADVERSARIAL — assumed the gate was secretly still library-level until proven CLI-level.

---

## Overall Verdict: PASS

The rebuilt `tests/swarm/test_bare_review_parity.py` is a genuine **CLI-driven** end-to-end
gate. Every assertion-bearing scenario drives the real `superclaude swarm run --lens
bare-review ... --transport stub` surface through click's `CliRunner.invoke`, reads the CLI's
**on-disk** outputs (`bare-review-*.final.md` bodies + `return-contract.yaml`), and parses the
nested-schema contract emitted by the live run. There is **no** in-process `BareReviewV1()` /
`determine_status()` / `.normalize()` composition driving any assertion. All 16 tests pass.

## Items Reviewed

| # | Check (from spawn criteria) | Result | Evidence |
|---|------------------------------|--------|----------|
| 1 | Gate invokes real CLI via `runner.invoke(swarm_group, ["run","--lens","bare-review",...,"--transport","stub"])` through a single helper; every scenario routes through it | PASS | Helper `_run_cli` at `test_bare_review_parity.py:226-291`; `runner = CliRunner()` + `runner.invoke(swarm_group, ["run","--lens","bare-review",...,"--transport","stub"])` at `:255-271`. All 5 contract/body tests call `_run_cli` (`:326, :362, :392, :434, :474`). The 6th test (`:487`) is a pure lens-prompt unit assertion, not a parity scenario. Reference style matches `test_e2e_user_guide.py` `_run`/`runner.invoke(swarm_group, ...)` at `:68-70`. |
| 2 | Gate reads CLI on-disk outputs (`*.final.md` + `return-contract.yaml`) from `--output`, NOT in-process library composition; NO `BareReviewV1(`/`determine_status(` driving assertions | PASS | On-disk reads at `:284-291`: `p.read_text(...)` over `sorted(out.glob("bare-review-*.final.md"))` and `yaml.safe_load((out / "return-contract.yaml").read_text(...))`. Grep for `BareReviewV1(\|determine_status(\|\.normalize(` in the file returns ONLY docstring prose (lines 13,15,19,46 — all referencing the *deleted legacy* `t2_normalize`), zero executable hits. No `import` of `BareReviewV1`/`determine_status`/recipes in the gate or `tests/swarm/conftest.py`. |
| 3 | Transport injection is legitimate (monkeypatch `_resolve_run_transport` → still runs full CLI Wave1→2→3 via `runner.invoke`); does NOT bypass `runner.invoke` | PASS | `monkeypatch.setattr(swarm_commands, "_resolve_run_transport", patched_resolve)` at `:247`. The stub branch of the factory calls the **module-global** at `commands.py:652-655` (`shared = _resolve_run_transport("stub", ...)`), so the patch is reached through the live CLI's `dispatch_wave1` → factory → global path. Injection feeds `StubTransport(fixtures=...)` (`:168,:190`) / `_ScriptedTransport` (`:171`); the full CLI still runs through `runner.invoke`. Legitimate per criterion 3. |
| 4 | Contract assertions parse CLI-emitted `return-contract.yaml` (nested schema), not a hand-built dict | PASS | `contract = yaml.safe_load((out / "return-contract.yaml").read_text(...))` at `:288-290`. Nested-schema accessors: `contract["caller_metadata"]["suspect"]` (`:436`), `o["status"] for o in contract["output_files"]` (`:394`), `contract["workers_succeeded"]`/`["workers_requested"]` (`:399,:403`), `contract["recommended_next_command"]` (`:440`). Live CLI emits the nested form via `ResultContract.caller_metadata: CallerMetadata` (`models.py:1013,1418`). No hand-built dict anywhere. |
| 5 | Referenced symbols actually exist (anti-hallucination) | PASS | `swarm_group` (`__init__.py:101`), `LENSES` dict (`lenses/__init__.py:105`), `CANONICAL_INJECTION_GUARD_SENTENCE` (`schema.py:133`), `iso_now` (`recipes/bare_review_v1.py:109`), `_resolve_run_transport` (`commands.py:492`), CLI flags `--lens/--target/--output/--transport/--reviewers/--label/--target-line-cap/--timeout-sec` (`commands.py:1318-1423`). All confirmed. |
| 6 | Golden tree exists on disk with real nested contracts | PASS | `tests/swarm/fixtures/bare_review_v1/golden/{all-success,partial-with-timeout,salvage-promoted}/` each contain `return-contract.yaml` + `bare-review-*-m.md`. `partial-with-timeout` correctly has only 2 bodies (timeout slot writes no `.final.md`, matching `expected_succeeded=2`). |
| 7 | Suite actually executes and passes | PASS | `uv run pytest tests/swarm/test_bare_review_parity.py -q` → **16 passed in 0.36s**. |

## Summary
- Checks passed: 7 / 7
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization FALSE)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR (observation, non-blocking) | golden `return-contract.yaml:27` vs gate `:436` | The committed **golden** contract carries `suspect: true` as a **top-level** key, while the gate asserts the nested `contract["caller_metadata"]["suspect"]` against the **live CLI** output. This is a golden-vs-live schema skew. It does NOT affect gate correctness: the contract assertions parse ONLY the live CLI `return-contract.yaml` (`:288`), and the golden contract is never consumed for the contract assertions (golden is used solely for body byte-comparison via `_golden_bodies`, `:294-298`). The live CLI emits the nested form (`models.py:1013,1418`), proven by the 16 passing tests. No action required for this gate; noted for golden-regen hygiene only. |

## Adversarial Probes Run (and their disproof of the "still library-level" hypothesis)
- **Hypothesis:** gate secretly composes the library in-process. **Disproof:** grep for `BareReviewV1(`/`determine_status(`/`.normalize(` → only docstring prose; no recipe/library import in the gate or conftest.
- **Hypothesis:** monkeypatch bypasses `runner.invoke`. **Disproof:** the patched global is invoked *inside* the CLI path (`commands.py:652-655` calls the module-global), and every scenario still goes through `runner.invoke(swarm_group, ["run",...])` at `:256`.
- **Hypothesis:** contract is a hand-built dict. **Disproof:** `yaml.safe_load` of the on-disk `return-contract.yaml` at `:288-290`; nested accessors throughout.

## Confidence Gate
- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 | Grep: 8 | Glob: 0 | Bash: 9 (each call maps to a specific criterion: forbidden-pattern grep, runner.invoke grep, test-fn enumeration, symbol-existence greps, flag-surface grep, factory-stub-branch Read, live pytest run, golden-tree ls, contract-nesting inspection)
- No web research performed (all verification was source-truth-local; no external/URL/standards claim in scope).

## Recommendations
- Green light. The gate is CLI-driven at the surface level required by Phase Gate 4 and survives WS-C's deletion of `t2_normalize.py` (no legacy script referenced at run time).
- OPTIONAL (non-blocking): on the next golden-regen, align the golden `return-contract.yaml` `suspect` key under `caller_metadata` to match the live CLI schema, eliminating the cosmetic skew noted in Issue 1.

## QA Complete
