# Research 04 — Test & Verification

**Task:** TASK-RF-troubleshoot-generalize-20260919-015257
**Topic:** Test & Verification (existing tests, break analysis for R-16/R-17, conventions, R-19 fixture design, regression artifact manifest)
**Status:** Complete
**Researcher:** test-verification agent (read-only on repo; writes only this file)
**Date:** 2026-09-19

## Scope

- `tests/troubleshoot/` (all `test_*.py`, `backtest/`, `e2e-backtest-scenarios.md`)
- `tests/conftest.py`, `pyproject.toml` `[tool.pytest.ini_options]` + `[tool.ruff]`
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`
- `merged-report-v2.md` `### R-14` (C1-C8, A1-A10) and `### R-19` (test table + fixture rule)
- `spec-panel-critique.md` `=== TESTING ===` + Guard Condition Boundary Table
- Coder worktrees `sysbox-retry-{glm,fable,astra}/.dev/troubleshoot/` (regression artifacts)

All claims cite `file:line` and quote verbatim.

---

## 0. Baseline (run 2026-09-19)

`uv run pytest tests/troubleshoot/ -q` → **1 failed, 70 passed** (15.2 s).

- **Pre-existing failure, NOT caused by this track**: `tests/troubleshoot/backtest/test_backtest_e4.py:105` — `assert "gate_passed" in low and "_evaluate_gate" in low` against `refs/contract-enumeration.md` (which currently contains neither token). The builder must record this as a known-red baseline so it is not mis-attributed to R-16/R-17 edits, and must NOT count it toward the R-19 acceptance run.
- `uv run ruff check tests/troubleshoot/` → `All checks passed!` (clean baseline).

## 1. Existing tests — what they read, what literal tokens they assert (G5/G6)

Paths below are under `/config/workspace/IronClaude/`. `REPO_ROOT = Path(__file__).resolve().parents[2]` in every top-level file (`tests/troubleshoot/test_hardening_h0.py:12`); `REFS = REPO_ROOT/src/superclaude/skills/sc-troubleshoot-protocol/refs` (`:13-15`). Markdown is read **at import time** into a module constant (`h0.py:16`, `h1.py:15`, `h2.py:16`, `h3.py:15`, `h4.py:15`, `output_contract.py:16-18`, `verdict.py:18,58`).

| Test file | Markdown read | Literal tokens asserted (verbatim) |
|---|---|---|
| `test_hardening_h0.py` | `refs/pipeline-hardening-closure.md` (`:16`) | `pipeline_hardening_applicable = false` / `pipeline_hardening_applicable=false` (`:24-27`), `one-sentence reason` (`:29`), `boundary scan` (`:30`), `looks local`+`invalid` (`:32,:56`), 8 field names `boundary_type, producer, transformers, consumer, evidence_source, risk, decision, rationale` (`:39-50`), `CLI/subprocess` (`:52`), `generated-artifact-parser` (`:53`) |
| `test_hardening_h1.py` | `refs/runtime-entrypoint-verification.md` (`:15`) | 12 field tokens `producer … accepted_substitute_rationale` (`:24-38`), `negative witness` (`:42`), `fix reverted` (`:43`), `never been observed to fail` (`:45`), **`satisfy h1`** (`:46`), `helper construction` (`:48`) |
| `test_hardening_h2.py` | `refs/contract-enumeration.md` (`:16`) | `vacuously pass` (`:23`), `zero-row`+`ledger` (`:24`), `unclassified live consumer` (`:25`), 6 fields `contract_token … unreachability_proof` (`:29-37`), `concept is shared` (`:44`), `sibling pipelines` (`:45`), `duplicate evaluator` (`:46`), `swept` (`:47`), `fail` (`:48`) |
| `test_hardening_h3.py` | `refs/unmask-and-sweep.md` (`:15`) | `word-boundary` (`:22`), ``must not match `complete` `` (`:24`), ``must not match `present` `` (`:27`), `small formal allow-list grammar` (`:37`), `commonmark` (`:38`), `substring` (`:39`), `setext` (`:42`), `decorated` (`:43`), `fixtures` (`:44`), 10 card fields `anchor_failure … heuristic_cost_rationale` (`:51-63`) |
| `test_hardening_h4.py` | `refs/effective-input-proof.md` (`:15`) | `fails closed` (`:23`), `wrong surface` (`:24`), `e > 0`+`sufficient` (`:25`), `true_runtime_surface` (`:28`), `intersection` (`:29`), 11 manifest fields `selector_command … validation_command` (`:35-48`) |
| `test_hardening_output_contract.py` | `SKILL.md` (`:16`), `refs/hardening-output-contract.md` (`:17`), `refs/report-template.md` (`:18`) | 19 `LEGACY_FIELDS` + 11 `HARDENING_FIELDS` as backticked names in SKILL (`:21-56`, `:63-68`) incl. `` `pipeline_hardening_verdict` ``, `` `waiver_status` ``; `` `not_run` `` `` `partial` `` `` `complete` `` in OC (`:75-76`); ``advisory` even if `pipeline_hardening_verdict=pass`` (`:78`); `with missing escape IDs listed` (`:80`); ``May mirror `pipeline_hardening_verdict` `` (`:82`); `## Pipeline Hardening Closure` in RT (`:89`); **`pass|blocked|advisory|not_applicable` OR `pass | blocked | advisory | not_applicable` in RT** (`:92-95`); `advisory` (`:96`); `NOT PROVEN` (`:98`) |
| `test_hardening_verdict.py` | `refs/hardening-output-contract.md` (`:18`), `refs/remediation-handoff.md` (`:58`) | `one-way` (`:26`), ``never resets to `none` `` (`:27`), **`{blocked, advisory}`** (`:27`); H5 rows `` `performed` | `PASS` | `none` `` … `` `waived_with_rationale` | `N/A` with rationale | `latched` `` (`:36-39`); `known_escapes_caught` (`:46`), `only if a passing wave/card is cited` (`:47`), **`pass | blocked | advisory | not_applicable`** (`:51`); `| 1 |`..`| 7 |` (`:66-67`), `` `not_applicable` `` (`:69`), ``OC.count("`blocked`") >= 3`` (`:71`), `ADVISORY — closure relies on waived/substituted proof` (`:73`), `ADVISORY — scoped closure with rationalized N/A` (`:74`), ``OC.count("`advisory`") >= 2`` (`:75`), `` `pass` `` (`:77`), `OC.count("| No |") >= 7` (`:79`); `not** convert` (`:92`), stages `task-builder, sc:reflect, sc:adversarial, report-rendering` (`:93`), `success_with_hardening_blocker` / `_advisory` (`:96-97`), ``never plain `success` `` (`:98`); HANDOFF: `build_request` (`:100`), `pipeline_hardening_verdict` (`:101`), `waiver_status` (`:102`) |
| `backtest/test_waiver_regreen.py` | `refs/hardening-output-contract.md` (`:33`, skip-guarded by `requires_impl_ref`) | `waiver_status`+`latch` (`:36`), `blocked`+`advisory` (`:40`), `success_with_hardening_blocker` OR `_advisory` (`:44-47`) — token-level, not enum-string-level |
| `backtest/test_backtest_e1..e5.py` | `runtime-entrypoint-verification.md`, `unmask-and-sweep.md` (e2,e3), `contract-enumeration.md`, `effective-input-proof.md` | loose OR-assertions (`negative witness`; `incomplete`+`complete`; `k_swept`/`swept`; `ledger`, `gate_passed`+`_evaluate_gate` (e4 — red at baseline); `fail-closed`/`fail closed`, `intersection`) — no H-token, no enum string |
| `backtest/test_git_replay_unit.py:85` | none (Python constant) | `git_replay.escape_by_id("E4").wave == "H2"` — compares against `git_replay.py:52-58` `ReplayEscape(..., "H1"|"H3"|"H2"|"H4")`, **not** markdown |

**No test under `tests/` reads `agents/confidence-calibrator.md` or `agents/evidence-validator.md`** (grep `confidence-calibrator.md|evidence-validator.md` in `tests/` → 0 files). The only other test reading the troubleshoot SKILL is `tests/skills/test_tier2_tavily_consistency.py` (`:16`), asserting `mcp__tavily__tavily_search` (`:33`), no `tavily-extract|map|crawl` (`:37`), `≤2|at most 2 quer|2 queries` (`:59`), `fail-open|fail open|degrad` (`:68`), `search_depth: advanced` (`:75`) — untouched by R-01..R-19 unless the SKILL rewrite drops those strings.

### 1a. Breaks under R-16 (`blocked-on-authorization` appended; change list `hardening-output-contract.md:5,15,68` + validator A4 — `merged-report-v2.md:510-511`)

Current source strings (verified 2026-09-19):
- `refs/hardening-output-contract.md:5` — `` `pipeline_hardening_verdict` is the **four-token** enum `pass | blocked | advisory | not_applicable`. ``
- `refs/hardening-output-contract.md:15` — `` | `pipeline_hardening_verdict` | enum `pass\|blocked\|advisory\|not_applicable` | … ``
- `refs/hardening-output-contract.md:68` — `` Once `latched`, `pipeline_hardening_verdict ∈ {blocked, advisory}` … ``

| # | Assertion (file:line, verbatim) | Verdict under R-16 | Why |
|---|---|---|---|
| B1 | `test_hardening_verdict.py:51` `assert "pass \| blocked \| advisory \| not_applicable" in OC` | **SURVIVES if appended, BREAKS if reordered/rewritten**; semantically stale either way (docstring `:44` "FOUR-token … a 3-token enum is a defect") | substring check; `pass \| blocked \| advisory \| not_applicable \| blocked-on-authorization` still contains it. Must be updated to assert the 5-token string so the test guards the new contract. |
| B2 | `test_hardening_verdict.py:27` `assert "{blocked, advisory}" in OC` | **CONDITIONAL BREAK** — `:68` is on R-16's change list | If `:68` becomes `{blocked, advisory, blocked-on-authorization}` the literal `{blocked, advisory}` disappears (next char is `,` not `}`). Recommend R-16 leave the latch set as `{blocked, advisory}` (authorization block is a hard-stop outcome, not a latch outcome — `merged-report-v2.md:511` ties it to "emitter row … AND re-run refused", not to `waiver_status`), OR update this assertion in the same commit. |
| B3 | `test_hardening_verdict.py:71` ``OC.count("`blocked`") >= 3`` | survives | `` `blocked-on-authorization` `` does not contain `` `blocked` `` (backtick-hyphen). |
| B4 | `test_hardening_verdict.py:66-67,79` `| {n} |` rows 1-7; `OC.count("\| No \|") >= 7` | survives | `>=`; an 8th truth-table row (if R-16 adds one for the new verdict) only increases counts. |
| B5 | `test_hardening_output_contract.py:92-95` `"pass\|blocked\|advisory\|not_applicable" in RT or "pass \| blocked \| advisory \| not_applicable" in RT` | survives (RT not on R-16's list) — but **cross-file drift** | `report-template.md:223` `<pass\|blocked\|advisory\|not_applicable>` and `:315` "four-token enum" stay 4-token unless the builder extends R-16 to RT, `pipeline-hardening-closure.md:13`, `remediation-handoff.md:11,35,69`, `SKILL.md:64,420` (all currently 4-token — grep above). If those ARE extended by appending, this assertion still passes. |
| B6 | `test_hardening_output_contract.py:78` ``"advisory` even if `pipeline_hardening_verdict=pass`" in OC`` | survives | `:62` not on change list. |
| B7 | `backtest/test_waiver_regreen.py:40` `"blocked" in low and "advisory" in low` | survives | token-level. |

**R-16 tally: 0 unconditional breaks; 1 conditional (B2); 1 must-update-to-remain-meaningful (B1).** No test anywhere asserts the literal word `four-token` (grep → 0 asserts), so the prose at OC:5 / RT:315 / closure:13 can change freely.

### 1b. Breaks under R-17 (`H0-H5` → `HC0-HC5` in `SKILL:104, :410-420, :595-600` + refs; field names unchanged; guard `grep -E '\bH[0-5]\b'` = 0 hits outside contract field names — `merged-report-v2.md:518`)

Current `\bH[0-5]\b` hit counts (2026-09-19): `SKILL.md` 23, `pipeline-hardening-closure.md` 19, `hardening-output-contract.md` 20, `report-template.md` 7, `unmask-and-sweep.md` 7, `runtime-entrypoint-verification.md` 6, `contract-enumeration.md` 5, `effective-input-proof.md` 4, `calibrator-eval-cases.md` 2, `escalation-rubric.md` 1; agents + command file 0.

| # | Assertion (file:line, verbatim) | Verdict under R-17 | Why |
|---|---|---|---|
| B8 | `test_hardening_h1.py:46` `assert "satisfy h1" in low` | **BREAKS (definite)** | Source: `refs/runtime-entrypoint-verification.md:7` "…does not satisfy H1." and `:28` "…does **not** satisfy H1." Both become `satisfy HC1`; `"satisfy h1" in "…satisfy hc1…"` is False. Fix: assert `"satisfy hc1"`. |
| B9 | `test_hardening_verdict.py:36-39` H5 mapping rows | survives | Asserted cells (`` `performed` | `PASS` | `none` `` …) contain no H token; only the column header `H5 Decision` (`OC:45`) is renamed. |
| B10 | `test_hardening_output_contract.py:63-68` field names | survives | R-17 explicitly keeps output-contract field names (`merged-report-v2.md:518` "output-contract field names unchanged (`SKILL:62`)"). |
| B11 | `backtest/_impl_guard.py:28,43-57` ref filename guards | survives | Ref filenames contain no H token; R-17 does not rename files. |
| B12 | `backtest/git_replay.py:52-58`, `test_git_replay_unit.py:85`, `test_backtest_status_separation.py:23,43`, `test_catch_rate_*` `EscapeResult(..., "H1")` | survives (Python constants, never compared to markdown) | Becomes nomenclature-inconsistent with the renamed protocol; optional follow-up rename to `HC*` is out of R-17's stated scope ("skill and refs"). |
| B13 | Error-message strings mentioning `H0`..`H4` (`h0.py:27,50`, `h1.py:38`, `h2.py:37`, `h3.py:63`, `h4.py:48`, backtest e1-e5 messages) | survives | messages only, not assertions. |

**R-17 tally: 1 definite break (B8).**

**R-17 guard vs. T14 conflict (must be resolved in the task file):** the guard `grep -E '\bH[0-5]\b'` over skill+refs also hits three *hypothesis-label* uses that are NOT hardening waves — exactly the label class R-17 exists to protect:
- `refs/calibrator-eval-cases.md:49` "Replays actual H2 card from T4."
- `refs/calibrator-eval-cases.md:54` "Replays actual H1 card from T4 (0.82 self-reported CONFIRM…)"
- `refs/escalation-rubric.md:35` "…(the H3 0.95-REFUTE case)…"
R-19 T14 (`merged-report-v2.md:583`) requires "fixtures 1-9 and P1-P5 unchanged". Either (a) the guard allow-lists these three lines (recommended: guard = `grep -nE '\bH[0-5]\b' SKILL.md refs/*.md | grep -vE 'calibrator-eval-cases.md:(49|54)|escalation-rubric.md:35'`), or (b) the builder rewords them to "hypothesis card 2/1/3" and T14 is defined as *semantic* (expected-score table unchanged), not byte-identical. Option (a) is the smaller diff.

**Combined tally (G5/G6 resolved): 1 definite break (`test_hardening_h1.py:46`), 1 conditional break (`test_hardening_verdict.py:27`), 1 assertion that survives but must be tightened (`test_hardening_verdict.py:51`), plus 1 pre-existing unrelated red (`backtest/test_backtest_e4.py:105`).**

## 2. Test conventions the builder must follow

- **Invocation**: `uv run pytest tests/troubleshoot/ -v` (`pyproject.toml:108-117`: `testpaths=["tests"]`, `python_files=["test_*.py"]`, `addopts=["-v","--strict-markers","--tb=short"]`). `--strict-markers` ⇒ any new marker MUST be registered at `pyproject.toml:118-137`; the existing troubleshoot tests use **no markers** (auto-markers only fire for paths containing `/unit/` or `/integration/`, `src/superclaude/pytest_plugin.py:219-221` — `tests/troubleshoot/` matches neither). Recommendation: no markers.
- **Package layout**: `tests/__init__.py`, `tests/troubleshoot/__init__.py` (5-line comment header), `tests/troubleshoot/backtest/__init__.py` all exist ⇒ absolute imports of helpers work (`backtest/test_waiver_regreen.py:22` `from tests.troubleshoot.backtest._impl_guard import HARDENING_REFS, requires_impl_ref`). A shared helper for R-19 (e.g. the assertion evaluators) should live as `tests/troubleshoot/_assertions.py` (underscore prefix = not collected, matches `_impl_guard.py` precedent) and be imported as `from tests.troubleshoot._assertions import ...`.
- **REPO_ROOT**: `Path(__file__).resolve().parents[2]` in `tests/troubleshoot/*.py` (`test_hardening_h0.py:12`); `parents[3]` in `backtest/` (`_impl_guard.py:21`, pinned by `backtest/test_path_resolution.py`). Fixture dir: `Path(__file__).parent / "fixtures"`.
- **Fixtures available**: root `tests/conftest.py` — `_pollution_snapshot` (session autouse, `:28`; asserts nothing under `docs/mistakes/` / `docs/memory/solutions_learned.jsonl` changed), `_redirect_reflexion_writes` (autouse, `:82`), `sample_context` (`:120`), `low_confidence_context` (`:140`), `sample_implementation` (`:160`), `failing_implementation` (`:184`), `temp_memory_dir` (`:205`). `backtest/conftest.py` — `replay_scratch_root` (`:20`), `catch_rate_output_dir` (`:40`). None are needed for content-assertion tests; any test that writes (T3 `producers.md`, T9 counter, T11 derived) must use `tmp_path`, never `docs/`.
- **Ruff** (`pyproject.toml:191-211`): `line-length = 88`, `select = ["E","F","I","N","W","TID"]`, `E501` ignored (long assertion strings OK), `N818` ignored. Import order (`I`): `from __future__ import annotations` → stdlib → third-party (`pytest`) → first-party (`tests.…`). **Fixture code files are linted**: `tests/troubleshoot/fixtures/procedures/producers/nonio.py` (R-19 layout, `merged-report-v2.md:554`) is inside ruff's scope (only `docs/`, `.dev/`, `tests/audit/fixtures/syntax_error.py` are excluded, `:194-199`); it must pass ruff or be added to `extend-exclude` following the `syntax_error.py` precedent. `.sh`/`.md`/`.log` fixtures are not linted. pytest will not collect `nonio.py` (`python_files=test_*.py`).
- **Style** (from `test_hardening_h0.py:1-6,19-21`): module docstring names the FR/§ and the source-of-truth ref path; each test docstring quotes the AC; every `assert` carries a message naming the missing rule; markdown read once at module import via `read_text(encoding="utf-8")`; lowercase compare via `low = X.lower()` for prose, exact-case for field names.
- **Pre-commit**: `make verify-sync` before commit (`CLAUDE.md` Component Sync) — any SKILL/refs/agents edit needs `make sync-dev`; tests do not.

## 3. Fixture design for R-19 (19 generic + 1 regression)

**Layout**: use the spec layout verbatim (`merged-report-v2.md:551-565`): `tests/troubleshoot/fixtures/{assertions,procedures,counters,regression}/`. The brief's shorthand `fixtures/{io,nonio,regression-sysbox}/` maps to `assertions/<ID>/{io,nonio}/` + `regression/sysbox-20260918/`. Coverage rule (`:590`): every assertion/procedure id has ≥1 `pos` and ≥1 `neg` in BOTH `io/` and `nonio/`; regression dirs hold expected-flag entries only, never the sole fixture.

**Architecture forced by "No LLM in CI" (`:547`)**: the assertion rules exist only as prose in `agents/evidence-validator.md` / `agents/confidence-calibrator.md` / SKILL inline-fallback. To make T1/T2 executable the builder must write **one pure-Python evaluator per assertion** in `tests/troubleshoot/_assertions.py` (`evaluate_validator(fixture_dir) -> set[str]`, `evaluate_calibrator(fixture_dir) -> (set[str], caps: dict)`), each reading only the fixture files. That module IS the executable form of the inline fallback; T13 parity then compares its flag names against both markdown surfaces (see §4). Keep evaluators regex/`in`-based (stdlib only; no new dependency). Flag tokens are the R-14 strings verbatim.

**Fixture shape for `assertions/<ID>/<domain>/{pos,neg}.md`**: one self-contained markdown file with YAML-ish frontmatter naming the artifact role (`artifact: REPORT|card|calibration|tasklist|candidate-fixes|locus`) and, where an assertion needs two artifacts (A5, A7, C5), a second fenced block headed `--- file: <name> ---`. Domain `io` = filesystem/CI/proc symptom; `nonio` = queue/HTTP/DB symptom (R-07 worked example 2, `merged-report-v2.md:383`). Sketches below give the *trigger line(s)*; the neg twin is the same file with the trigger line replaced by the bracketed alternative.

### 3.1 T1 `test_validator_assertions.py` — A1-A10 (parametrize `id × {io,nonio} × {pos,neg}` = 40)

Rule source: `merged-report-v2.md:469`.

| ID | Flag / effect | `pos.md` trigger lines (io / nonio variant) | `neg.md` swap |
|---|---|---|---|
| A1 | `deduced_headline` → `partial` | `**Confidence**: 0.42` + `## Diagnosis` line `Root cause: the outcome is `clone-failed`` (nonio: `` `redelivered=true` ``) + `## Grounding Gaps` "enum is deduced, not observed" | confidence `0.72`, headline token present in an `artifacts/seed-checkout.txt` block (grep -F hit) |
| A2 | `instrumentation_without_falsifier` → `partial` | `--- file: diff.patch ---` touching `test-startup-boot.sh` collector line (nonio: `consumer.py` invocation site) + REPORT `## Next Steps` with **no** sentence `The report stays `partial` until <row>=<value>` | add `The report stays `partial` until uptime-regex=false` (nonio: `…until redelivered=false`) |
| A3 | `timestamp_invalid` (line dropped) | `**Date**: 2026-09-19T00:00:00Z`; second pos: `Timestamp: <mtime+00:05:01>` where fixture frontmatter pins `artifact_mtime: 2026-09-18T18:36:00Z` | `Timestamp: 2026-09-18T18:40:59Z` (+4m59s) |
| A4 | `verdict_not_in_contract` → `partial` | `pipeline_hardening_verdict: blocked_pending_retry_run` (nonio: `pipeline_hardening_verdict: needs_review`) | `pipeline_hardening_verdict: blocked-on-authorization` (asserts the 5th token is accepted) and a second neg `not_applicable` |
| A5 | `consensus_on_unobserved` → `partial` | `--- file: candidate-fixes.md ---` row ending `**consensus**` + REPORT `Adversarial: not invoked` + `--- file: card ---` `evidence_class: source_static`, `claim_class: runtime_behavior` | card `evidence_class: runtime_repro` |
| A6 | FAIL | R-07 form line `Reference-context value: true if seekable, false otherwise` (nonio: `false/true`) | `Reference-context value: true` |
| A7 | FAIL | locus `RUN-SITE: pending-producers @ ci-runner` + `--- file: producers.md ---` with header + 1 row `startup.sh:583 \| … \| surviving=yes` (nonio: `consumer.py:41`) | **two negs required** (`:569`): (i) `RUN-SITE: startup.sh:583 @ ci-runner`; (ii) sentinel kept but `producers.md` has header `observation-kind: categorical` and **zero rows** |
| A8 | `status=blocked`, `UNDETERMINED — CI verdict unobserved` | locus `OBSERVE-VIA: artifact-file` + frontmatter `files_present: [REPORT.md]` (no `job-*.log`) | `files_present: [REPORT.md, job-105704643590.log]` (nonio: `job-7781.log`) |
| A9 | probe `suspect`, outcome table skipped | form `Reference-context value: true` + `--- file: tier1-observation.md ---` `uptime-regex=false` observed in the **reference** arm (nonio: `redelivered=true` on the known-good consumer) | observed reference value `true` |
| A10 | `capability_block_unproven` → `partial` | tasklist header `**capability-verdict**: blocked` with no `## Emitter search` block | add `## Emitter search` / `emitters-found: 0` / `already-read-files: 0` |

### 3.2 T2 `test_calibrator_assertions.py` — C1-C8 incl. C3b (parametrize = 36; TS-01 says 32 for C1-C8 — the extra 4 are C3b, `:570`)

Rule source: `merged-report-v2.md:468`. Each `pos.md` is a hypothesis card (frontmatter `claim_class`, `evidence_class`, `verdict_direction`, `Self-reported confidence`) plus a `--- file: calibration ---` block with `calibrated: <n>` where the assertion needs it.

| ID | Flag / effect | `pos.md` trigger | `neg.md` swap |
|---|---|---|---|
| C1 | `headline_definite_low_confidence`, verdict forced `ESCALATE` | headline `the outcome is `clone-failed`` + `calibrated: 0.42` | `calibrated: 0.72` (also T11 boundary: neg at exactly `0.50`) |
| C2 | Runtime check `:= 0.0`, `unproven_exclusion:<token>` | `Excluded: `auth-denied` (unreachable for anonymous clone)` — no `file:line` | `Excluded: `auth-denied` — exit statement startup.sh:663` |
| C3 | Symptom coverage `≤0.5`, `control_unproven` | `Control: the DinD arm passed the same script` with locus `CONTROL-PROOF: no: startup.sh:753` (or absent) | `CONTROL-PROOF: yes: startup.sh:583` |
| C3b | Runtime check `≤0.5`, `locus_unknown` | card line `runs-in=unknown` | `runs-in=sysbox-runc-runner` (nonio: `runs-in=worker-pod-b`) |
| C4 | Fix directness `≤0.5`, `no_prereg_falsifier` | `## Proposed instrumentation` row `dns-github \| \| ` (empty `value-if-true \| value-if-false`) | `dns-github \| true \| false` |
| C5 | `timestamp_invalid` | `**Timestamp**: 2026-09-19T00:00:00Z` with input `card_mtime: 2026-09-18T18:30:00Z`; second pos `+5m01s` | `+4m59s` |
| C6 | evidence quality `≤0.3` | headline `fails above 73 layers` (nonio: `fails above 512 in-flight messages`) with `--- file: bracket.md ---` empty | `bracket.md` contains `bracket=[72,74] width=2` |
| C7 | cap `0.5`, `uncited` | mechanism names an environment property (`/proc/uptime is non-seekable under this runtime` / `broker requeues with redelivered=true`) and no `2x2:` / `## Discriminator rows` cite | add `2x2 row: uptime-exact=1 uptime-ref=0 (failing) / 0,0 (passing)` |
| C8 | cap `0.5`, `behaviour-cite: missing` | evidence lacks `behaviour-definition: row N`; second pos: `behaviour-definition: row 2` + `--- file: behaviour-definitions.md ---` row 2 Status **empty** | `behaviour-definition: row 1` + row 1 `Status: fetched:context7` |

### 3.3 T3-T19 procedure fixtures

| Test | Fixture files (`tests/troubleshoot/fixtures/…`) | Content sketch (≤10 lines each) | What the test asserts (from `merged-report-v2.md:571-587`) |
|---|---|---|---|
| T3 `test_producers_enumeration.py` | `procedures/producers/io.sh` (≈12 lines: function with `rc=runner-unavailable` at 3 sites, one `return 1`, one `exit 2`, and a `## Mechanism rows`-only decoy string in a comment), `procedures/producers/nonio.py` (function setting `status = "DEAD_LETTER"` at 2 sites + one `return`; must pass ruff or be excluded) | the test runs the R-02 procedure in Python (`re.finditer`) over the fixture and writes `producers.md` to `tmp_path` | header `observation-kind:` always present; 7 columns; `len(rows) == grep_hits`; computed enum (`rc=$prefix-unavailable` line in `io.sh`) ⇒ `producer-count=unknown`; all rows `surviving=no` ⇒ every row rewritten `surviving=re-opened`; rows under `## Mechanism rows` excluded from count |
| T4 `test_primitivegrep_targeting.py` | `procedures/primitivegrep/sink.sh` (lines: `read -r u _ </proc/uptime`; `cat /sys/class/net`; `exec 2>/dev/null`; `echo x >/dev/null`; `: </dev/tty`; plus a non-producer file `decoy.sh` containing `/proc/cpuinfo`) | grep runs only over files listed in a `producers.md` fixture (`sink.sh` only) | hits exclude `/dev/null`, `2>/dev/null`; ≤8 rows; `decoy.sh` never hit; `RUN-SITE: pending-producers` overwritten with `sink.sh:<n>` |
| T5 `test_locus_card.py` | `procedures/locus/complete.md` (PRINT-SITE/RUN-SITE/SAME-ENV/OBSERVE-VIA + arm blocks with `CONTROL-PROOF: yes: f:1`), `missing-run-site.md` (RUN-SITE line deleted), `one-env.md` (issue text names one host), `two-env.md` (CI matrix with 2 jobs), `no-env.md` (bare stack trace) | plain-text cards, 4-8 lines | complete ⇒ pass; missing line ⇒ Wave 1 exit FAIL; `SAME-ENV` derives `yes`/`no`/`unknown` from the three texts; card without `runs-in=` ⇒ "returned" |
| T5b `test_verdict_source.py` | `procedures/verdict-source/marker.log` (`RESULT: PASS` then `RESULT: FAIL` last), `no-marker.log`, `conclusion-only.log` (`conclusion: success` only) | 3-6 lines each | verdict = last marker (`FAIL`); no marker ⇒ `unobservable` (=FAIL); conclusion-only never PASS |
| T6 `test_discriminator_form.py` | `procedures/discriminator/io.md` (R-07 worked example 1 verbatim, `merged-report-v2.md:382`), `nonio.md` (worked example 2, `:383`) | the fill-in form (`:364-379`) | parses; exactly one outcome row matches truth vector `false/true/true` (io) / `true` (nonio); A9 marks probe `suspect` when reference mismatch |
| T7 `test_threshold_bracket.py` | inline table in the test (no file) | vectors e.g. `{76:P,78:F,80:F}`, non-monotone `{76:F,78:P}` | trigger on "limit named in text" and "passes at smaller value"; guard == highest pass; `width == 2`; non-monotone ⇒ `UNDETERMINED`; `diagnosability-rounds.json` counter untouched |
| T8 `test_cosmetic_counter.py` | `counters/cosmetic-log.txt` (tool-call log: `Read out/REPORT.md.draft` ×5, `ls out/`, `Write out/x.md`, `Read out/job-1.log`, `Read src/a.sh`, then ×5 more) | one call per line | fires at 5 with `cosmetic_overrun=5`; re-fires at 10; `ls`/`Write`/`job-*.log` exempt; source Read resets |
| T9 `test_counter_key.py` | two synthetic tasklists written to `tmp_path` (`discriminator-required=yes` / `=no`), two slugs | JSON counter under `tmp_path` | same `<branch>:<repro-venue-id>` key persists across slugs; only `=yes` increments; at round 3 tasklist still written, `status: blocked` |
| T10 `test_hardstop_verdicts.py` | `procedures/tasklist/authorized.md` (emitter row + `re-run permitted: yes`), `refused.md` (emitter row + `re-run permitted: no`), `no-emitter-no-file.md` (`emitters-found: 0`, `already-read-files: 0`, `capability-verdict: blocked`), `source-only-read.md` (`already-read-files: 0` because only `*.sh` read) | tasklist header + `## Emitter search` block | refused ⇒ `blocked-on-authorization`, `status: blocked`, file written; authorized ⇒ task row required and `capability-verdict: blocked` fails A10; N=0 + already-read log ⇒ append row; N=0 + source-only ⇒ `capability-verdict: blocked` valid, no source edit |
| T11 `test_headline_threshold.py` | derived from T1/T2 calibrated values | — | `max(neg calibrated) < 0.5 <= min(pos calibrated)` (fixture interval 0.42/0.72, `:429`); missing confidence ⇒ `UNDETERMINED` (GB-05: treated as 0.0) |
| T12 `test_timestamp_tolerance.py` | synthetic | — | `mtime+4m59s` passes, `+5m01s` fails, `T00:00:00Z` always fails |
| T13 `test_inline_fallback_parity.py` | all fixtures above | — | see §4 |
| T14 `test_calibrator_eval_cases.py` | existing `refs/calibrator-eval-cases.md` | — | see §5 |
| T16 `test_primitive_differential.py` | `procedures/differential/table.md` (2×2 rows: `sysbox 1/0, dind 0/0`; `all-unobserved`; `single-env`) | 3 tables, 4 lines each | `exact≠ref failing ∧ equal passing` ⇒ `substituted primitive`; any cell `unobserved` or one env ⇒ `comparator=none`, cap `0.4` |
| T17 `test_discriminator_rows.py` | `procedures/rows/distinguishing.md`, `indistinguishable.md` (header `indistinguishable: a,b` after 2 added rows), `exact-only.md` (missing `-ref` half), `overflow.md` (9 pairs ⇒ `probe-rows-truncated: 1`) | tasklist `## Discriminator rows` tables | pair completeness; control row present; ≤8 pairs + header; `verdict` forced `sufficient|unknown` → `partial`; zero-surviving re-open (AD-02) |
| T18 `test_behaviour_definition_row.py` | `procedures/behaviour/fetched.md` (Status `fetched:context7`), `recalled.md` (`recalled, not load-bearing`), `missing.md` (no row) | 6-col table (`:409-410`) | row written before fetch (ordering token in audit); query built from column-3 words only (assert no `format|output|appearance`); `recalled` ⇒ probe row appended; missing ⇒ C8 cap 0.5 |
| T19 `test_menu_equality.py` | derived from T3 `producers.md` + a synthetic prompt text | — | `len(distinct enum tokens in prompt) == count(surviving=yes)`; mismatch ⇒ FAIL |

### 3.4 T15 `test_regression_sysbox.py` — vendored artifacts + MANIFEST

Source root `/config/workspace/Coder/.claude/worktrees/`. All files below confirmed present (`ls`) 2026-09-19; sizes in bytes; `sha256sum`.

| Param | Vendor as `fixtures/regression/sysbox-20260918/<Param>/<name>` | Source (absolute) | Bytes | sha256 |
|---|---|---|---|---|
| GLM-RUN2 | `REPORT-RUN2.md` | `sysbox-retry-glm/.dev/troubleshoot/sysbox-deep/REPORT-RUN2.md` | 7016 | `3e6a9902b80cb6fcf133ffc356cc1824d3f5c6dd972a018ecf706c2a276aaabb` |
| GLM-RUN2 | `run2-tier2-root-cause-analyst-calibration.md` | `sysbox-retry-glm/.dev/troubleshoot/sysbox-deep/run2-tier2-root-cause-analyst-calibration.md` | 4060 | `62acf9283e3a1134b65113e021b582a0a9dba1813557fa42263b06c2a6cd0df8` |
| GLM-RUN2 (**add**, needed for C2/C3) | `run2-tier2-root-cause-analyst-hypothesis.md` | `sysbox-retry-glm/.dev/troubleshoot/sysbox-deep/run2-tier2-root-cause-analyst-hypothesis.md` | 8358 | `d8bef2f015603ab800a455a192be38c2d734c306f7542b1aa17415a36f6708da` |
| GLM-RUN2 (optional, A5 corroboration) | `candidate-fixes.md` | `sysbox-retry-glm/.dev/troubleshoot/sysbox-deep/candidate-fixes.md` | 2157 | `76cf294c9fae7e940101b1dd4d453197905e70e971c35ce5c519154e7fca6bdf` — NOTE run-1 vintage (mtime 13:35 vs run-2 18:xx); A5 already fires from `REPORT-RUN2.md:72` "Adversarial: not invoked — consensus" + calibration `evidence_class none` |
| Fable-D3 | `REPORT.md` | `sysbox-retry-fable/.dev/troubleshoot/sysbox-deep-3/REPORT.md` | 6869 | `4910ffa683c357ba23d5b002f2ef8ba501d7da06fad4f1361b359872e3ef037d` |
| Fable-D3 (optional) | `candidate-fixes.md` | `sysbox-retry-fable/.dev/troubleshoot/sysbox-deep-3/candidate-fixes.md` | 2820 | `1fde1d0f936d5cbd40303424628a1993483827c92512bbbfc7f5a2bac900ecf6` |
| Astra-A3 | `diagnosability-tasklist.md` | `sysbox-retry-astra/.dev/troubleshoot/sysbox-deep/retry3-internal-runner/diagnosability-tasklist.md` | 4446 | `967cede52133387697b8d7458f7a2384619575e703126ea9b6e8be7d67ba93fd` |
| Astra-A3 | `tier1-observation.md` | `sysbox-retry-astra/.dev/troubleshoot/sysbox-deep/retry3-internal-runner/tier1-observation.md` | 11565 | `3eca299bf79d6107019f2125720872097b344f3061684977a01bee3d67f916ed` |
| Astra-A3 (optional) | `REPORT.md` | `sysbox-retry-astra/.dev/troubleshoot/sysbox-deep/retry3-internal-runner/REPORT.md` | 6633 | `54a4205c0333e9a63614f156a94698efd555a6e88788876c238ab4e412502895` |

`MANIFEST` format: one line per file `<sha256>  <bytes>  <relative path>`; T15 first re-hashes every vendored file against `MANIFEST` (byte-copy guard), then evaluates.

**Expected-flag table (T15 parameters) and the evidence lines that make them fire:**

- **GLM-RUN2 ⇒ {A1, A3, A4, A5, C2, C3}** (`merged-report-v2.md:471,588`):
  - A1: `REPORT-RUN2.md:6` `**Confidence**: 0.42`; `:21` "**Root cause** (probable, pending enum): … `clone-failed`"; `:57` "`clone-failed` is source-logic-deduced, not read" (Grounding Gaps `deduced`).
  - A3: `run2-tier2-root-cause-analyst-calibration.md:6` `**Timestamp**: 2026-09-19T00:00:00Z` (also `T00:00:00Z` literal ⇒ C5 fires on the calibration report — the builder should decide whether C5 is in-scope for T15; R-14's claim lists only C2/C3).
  - A4: `REPORT-RUN2.md:63` "**Verdict: blocked_pending_retry_run**".
  - A5: `REPORT-RUN2.md:72` "Adversarial: not invoked — consensus"; calibration `:13` "evidence_class `none`", `:46` "claim_class … runtime_behavior".
  - C2: hypothesis card `:33` excludes `skipped`/`rejected-input`/… citing `startup.sh:753-758` and `:509-534` **without the exit statement line per enum** (R-14 C2 requires a `file:line` for *that enum's exit statement*).
  - C3: card `:5` "proven passing … by the two control runs (DinD-public …)" with no `CONTROL-PROOF: yes` anywhere in the GLM artifacts (grep `CONTROL-PROOF` → 0).
- **Fable-D3 ⇒ none fire, `0.72` kept** (`:471,588`): `REPORT.md:4` `confidence: 0.72`; `:10` `pipeline_hardening_applicable: false` and **no `pipeline_hardening_verdict` key** — A4 evaluator must treat an absent key with `applicable=false` as pass; no `T00:00:00Z`; headline "cannot read `/proc/uptime`" at 0.72 ≥ 0.50 ⇒ A1 silent. **Caveat**: Fable's hypothesis card (`tier2-root-cause-analyst-hypothesis.md`, sha `e34871bc…`, 13186 B) predates the 2×2/behaviour-row conventions and WOULD trip C7/C8 if fed to the calibrator evaluators — scope Fable-D3 to REPORT-level validator assertions + C1/C5, or the claim "none fire" is false. Record the in-scope assertion set per param in the test.
- **Astra-A3 ⇒ T10 emitter rule fires; cards lacking `runs-in=` returned; A7 does not fire** (`:588`, TS-01 `spec-panel-critique.md:296`): `diagnosability-tasklist.md:24` "**Blocked on capability, not permission**" with no `## Emitter search` block (grep → 0) ⇒ A10 `capability_block_unproven`. **Token caveat**: the artifact says "Blocked on capability", not the R-03 header `capability-verdict: blocked`; the A10 evaluator must match both the header form and the prose form (`(?i)blocked on capability|capability-verdict:\s*blocked`) or T15-Astra cannot fire. `tier1-observation.md` contains no `runs-in=` (grep → 0) ⇒ C3b/T5 "returned". No `producers.md` exists in the Astra dir and no `RUN-SITE` line ⇒ A7 silent (AD-04).

## 4. Test 13 (`test_inline_fallback_parity.py`) — what "inline fallback equals agent path" can mean without an LLM

Current surfaces: `SKILL.md:282` "fall back to inline orchestrator calibration against the rubric and mark `calibration: inline-fallback`"; `:452,:563` "inline-validate citations in the orchestrator context"; `:539-540` "the `confidence-calibrator` agent or the inline fallback applies the rubric"; `agents/confidence-calibrator.md:138`, `agents/evidence-validator.md:126-127` (crash ⇒ inline). R-09 step 6 (`merged-report-v2.md:417`) is the only R-card that names the inline fallback as an asserting party: "Calibrator (C8) **and the inline fallback** assert the referenced row exists".

Testable without an LLM (three content/parity assertions, all deterministic):

1. **ID parity**: the set of assertion IDs parsed from `agents/evidence-validator.md` `## Structural assertions` table (R-14: `VAL:63-97` gains it) == `{A1..A10}`; from `agents/confidence-calibrator.md` step 5b / Notes == `{C1,C2,C3,C3b,C4..C8}`; and the SKILL inline-fallback section (new text R-14 must add next to `SKILL:282`/`:452`, or a shared `refs/agent-assertions.md` both cite) lists the **same IDs with the same flag tokens** (`deduced_headline`, `timestamp_invalid`, `verdict_not_in_contract`, `consensus_on_unobserved`, `capability_block_unproven`, `unproven_exclusion`, `control_unproven`, `locus_unknown`, `no_prereg_falsifier`, `uncited`, `behaviour-cite: missing`, `headline_definite_low_confidence`). Simplest lazy design: put the table ONCE in `refs/agent-assertions.md`, have both agents and the SKILL fallback reference it, and have T13 assert (a) the ref contains all 19 IDs+flags, (b) each agent file and the SKILL fallback paragraph cite the ref path — then parity is structural, not textual.
2. **Evaluator parity**: `tests/troubleshoot/_assertions.py` exposes `FLAGS: dict[id, flag]`; T13 asserts `FLAGS` == the table parsed from the markdown (so Python and prose cannot drift).
3. **Fixture-wide parity** (`merged-report-v2.md:547` "parity is a fixture-wide assertion"): for every fixture under `assertions/` and `regression/`, `evaluate_*(fixture)` flag set == the fixture's declared `expected_flags:` frontmatter, AND the flag names ⊆ the markdown table. Because there is one evaluator, "agent flag set == inline flag set" reduces to "the single evaluator's output matches the declared expectation on every fixture" — state this reduction in the test docstring so a reviewer does not look for a second engine.

Not testable in CI: that a live agent applies the prose identically — mark that as the placebo-check already documented at `agents/confidence-calibrator.md:141`.

## 5. Test 14 (`test_calibrator_eval_cases.py`) — what proves fixtures 1-9 / P1-P5 non-regression

`refs/calibrator-eval-cases.md` (81 lines) is a **spec of expected scores, not a fixture corpus**: no `fixture-*.md` files exist anywhere in the repo (`Glob fixture-h3-style.md` → none; `:81` "Pytest harness … OUT OF SCOPE … Expected landing path: `tests/troubleshoot/test_calibrator_eval_cases.py`"). So T14 must (a) pin the spec text and (b) exercise the formula the spec fixes.

Assert, per fixture, the literal expectation lines (verbatim from the ref):
- F1 `:10` "**Expected calibrated**: ≤ 0.70 (M3a cap fires)."
- F2 `:16` "**Expected calibrated**: ≤ 0.80 (gate_M2 = 0.80)."
- F3 `:22` "**Expected calibrated**: 1.0."
- F4 `:27` "**Expected calibrated**: ≤ 0.80 (gate_M1 = 0.80)."
- F5 `:32` "calibrator defaults claim_class to `runtime_behavior`, evidence_class to `none`, verdict_direction to `AFFIRM`"
- F6 `:38` "**Expected calibrated**: 1.0. **Asserts**: M3a cap does NOT fire when runtime_check=1.0."
- F7 `:45` "**Expected calibrated**: ≤ 0.65 (per V2 rule 1) or ≤ 0.70 (per V1 M3a)."
- F8 `:50` "**Expected calibrated**: ≤ 0.70."
- F9 `:55` "**Expected calibrated**: 0.70-0.85 range; NO hard cap fires."
- P1-P5 rows `:61-65` (`evidence_grounding ≤ 0.5 ⟹ calibrated ≤ 0.80`; `runtime_check ≤ 0.5 AND claim_class ∈ {runtime_behavior, environment_dependent} ⟹ ≤ 0.80`; `REFUTE AND runtime_behavior AND runtime_check < 1.0 ⟹ ≤ 0.70`; determinism; anchoring ±0.05 soft).

Plus one executable check: implement the rubric formula in the test (`min(mean(six), eg+0.30, rc+0.30)` then cap 0.70 REFUTE / 0.84 AFFIRM — `agents/confidence-calibrator.md` steps 5/5a; formula at `refs/escalation-rubric.md:20` which R-14 says must NOT change) and feed the nine dimension vectors written in the ref (`:9,:15,:21,:26,:37`); assert each result satisfies its expectation line and P1-P3 hold on a small grid. This proves R-14's new C-assertions (caps at 0.5/0.3) are applied **after** and do not alter the base formula. Keep the H-label lines `:49,:54` out of the byte-compare (see §1b) — assert on the expectation lines only.

## Status: Complete

**Summary**
1. Existing `tests/troubleshoot/` = 7 top-level content-assertion modules (18 tests) + backtest (53 tests); baseline **70 pass / 1 pre-existing fail** (`backtest/test_backtest_e4.py:105`, unrelated).
2. Assertions that break: **1 definite** under R-17 (`test_hardening_h1.py:46` `"satisfy h1"`), **1 conditional** under R-16 (`test_hardening_verdict.py:27` `"{blocked, advisory}"` iff OC:68 set is extended), **1 to tighten** (`test_hardening_verdict.py:51` 4-token substring still passes after append). No test reads the agent files.
3. R-17's `\bH[0-5]\b` guard collides with 3 hypothesis-label lines (`calibrator-eval-cases.md:49,54`, `escalation-rubric.md:35`) and with T14 "unchanged" — allow-list them.
4. R-19 needs a stdlib-only evaluator module (`tests/troubleshoot/_assertions.py`) because no LLM runs in CI; T13 parity reduces to markdown-table ⇔ evaluator ⇔ fixture-frontmatter agreement; fixture `nonio.py` falls under ruff.
5. Regression artifacts: all 11 candidate files exist; 9 sha256+sizes recorded above; GLM needs the hypothesis card added for C2/C3; Fable "none fire" holds only if C7/C8 are scoped out; Astra A10 must match prose "Blocked on capability" as well as the `capability-verdict:` header.
