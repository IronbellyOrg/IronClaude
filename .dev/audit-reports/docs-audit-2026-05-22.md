# Documentation Audit — Post cliEval Phase 5+6 Remediation

**Audit date:** 2026-05-22
**Branch:** `feat/sc-troubleshoot-wave-1.5-doc-grounding`
**Reference task:** TASK-RF-20260522-153212 (Phase 5+6 cliEval remediation)
**Reference AC matrix:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260522-153212/phase-outputs/reports/06-ac-matrix.md`
**Gold-standard reference doc:** `/config/workspace/IronClaude/docs/user-guide/eval-pipeline.md` (already updated for the remediation; "Last verified: 2026-05-22 against `src/superclaude/cli/eval/` post-remediation")

---

## Summary

| Priority | Count | Document(s) |
|---|---|---|
| **P1 CRITICAL** | 4 | `docs/eval/validation-commands.md`, `docs/eval/release-checklist.md`, `docs/eval/retention.md`, `docs/eval/retry.md` + `docs/eval/runtime.md` (shared issue #5/#6 — counted as P1 for `validation-commands.md` only; runtime/retry tracked as P2) |
| **P2 IMPORTANT** | 4 | `docs/eval/retention.md`, `docs/eval/runtime.md`, `docs/eval/retry.md`, `docs/eval/scratch-roots.md` |
| **P3 NICE-TO-HAVE** | 2 | `CHANGELOG.md`, `docs/developer-guide/documentation-index.md` (or sibling index) |
| **TOTAL** | 10 distinct docs (some appear twice across priorities) | |

### Scope of the remediation reflected in this audit

The audit checks each doc against these landed changes (from AC matrix):

- **H1** — `eval run --output-dir <X>` now produces `<X>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/` (no longer a flat layout)
- **H2** — coverage gate fails closed on corrupt `~/.claude/settings.json`
- **H3** — `_format_run_summary_line` renders full DM-012 taxonomy `P/F/S/E/I/T`
- **H4** — `resolve_scratch_root("/tmp/eval-runs")` (bare prefix) now **rejects**; only strict sub-paths accepted
- **H5a/H5b** — allowlist extension happens **before** any `mkdir` at commands.py and isolation.py sites
- **M2** — `_NullLifecycleExecutor` now emits stderr WARNING on every run
- **M3** — `RunTotals` keys derived from `EVAL_STATUSES` partitions (no hardcoded literals)
- **M4** — Both `Reporter.write` and `write_aggregated_report` emit `summary.yaml` (the +1 yaml divergence is closed)
- **M5** — `orchestrator.allocate_session_id(run_id, eval_id)` is the canonical session-id allocator
- **M6** — `eval doctor --output-dir` now has `file_okay=False` (symmetric with `eval run`)
- **CC1** — `EVAL_ID_PATTERN` is the single source of truth in `artifact_layout.py`; `loader.py` imports as alias
- **CC2** — exactly 4 canonical exit codes in `src/superclaude/cli/eval/exit_codes.py` (`SUCCESS=0`, `FAILURES=1`, `USAGE_ERROR=2`, `INTERRUPTED=3`); all 11 `*_EXIT_CODE` constants re-export from there
- **B1 closure** — `_new_run_id` and `_default_output_dir` helpers now exist in `commands.py` (lines 1326-1347)

---

## P1 CRITICAL findings

> Docs that contradict current runtime behavior. An operator following them today would fail or get misled about the harness state.

### P1-1. `docs/eval/validation-commands.md` — claims `eval run --suite real --eval E1` is BROKEN (B1 NameError)

**Document path:** `/config/workspace/IronClaude/docs/eval/validation-commands.md`

**Reason for update:**
Lines 99-104, 132-142, and §5 entirely declare that command 4 (`uv run superclaude eval run --suite real --eval E1`) is BLOCKED with `NameError: name '_new_run_id' is not defined` at `commands.py:1467`. **This is wrong on the current tree.** The helpers `_new_run_id` and `_default_output_dir` exist at `src/superclaude/cli/eval/commands.py:1326` and `:1339` respectively. The B1 blocker described in §5 has been resolved by the cliEval Phase 5+6 work (this is confirmed in commit `1ca25953 feat(cliEval): land cliEval CLI module + task track + supporting infra changes (#66)` and the recent PR #66 review remediation in `dce3c3cb`).

**Specific recommended changes:**

1. **Replace §5 — Known blockers § B1.** Existing text (line ~134-148):
   > **B1 — `eval run` body references undefined helpers**
   > **Symptom:** `uv run superclaude eval run --suite real --eval E1` exits with `NameError: name '_new_run_id' is not defined` …

   Replace with a **B1 closure note**:
   > **B1 (closed at PR #66 / dce3c3cb) — `eval run` helpers now landed**
   > The previously-missing `_new_run_id` and `_default_output_dir` helpers in `src/superclaude/cli/eval/commands.py` were landed in commit `1ca25953` and remediated for the PR review in `dce3c3cb`. They live at `commands.py:1326` (`_new_run_id`) and `:1339` (`_default_output_dir`) respectively. Command 4 no longer raises `NameError`. The remaining gate on full attestation is B2 (ptytest vendoring SOFT-SKIP); see B2 below.

2. **Re-attest command 4 in §2.4 and §1 table.** Change "Observed result (2026-05-20): NameError ❌" → "Observed result (2026-05-22): exits with structured FAIL or PASS depending on B2 state; NameError gate cleared at PR #66." Update §1 table row 4 "Expected exit: 0" to either record the current behavior, or capture fresh evidence and update the log path.

3. **Update §7 follow-ups in the sibling release-checklist** (see P1-2).

**Verification protocol:**
- `grep -n "_new_run_id\|_default_output_dir" /config/workspace/IronClaude/src/superclaude/cli/eval/commands.py` should return at least lines 1326 (`def _new_run_id`) and 1339 (`def _default_output_dir`).
- `uv run python -c "from superclaude.cli.eval.commands import _new_run_id, _default_output_dir; print('helpers exist:', bool(_new_run_id), bool(_default_output_dir))"` should print `helpers exist: True True` (verified during this audit).
- Run `uv run superclaude eval run --suite real --eval E1 2>&1 | head -50` and confirm no `NameError` for `_new_run_id` or `_default_output_dir`.
- Cross-reference AC matrix row **CC2** (canonical exit codes landed) and **M5** (`allocate_session_id`); both depend on the helpers being present.

---

### P1-2. `docs/eval/release-checklist.md` — same B1 staleness; §5 row 5.4 ❌ contradicts current tree

**Document path:** `/config/workspace/IronClaude/docs/eval/release-checklist.md`

**Reason for update:**
Lines 83 and 116-117 carry the same B1 NameError claim transitively from `validation-commands.md`. Specifically:

- Line 83: §5 row 5.4 records `**1 (NameError)** ❌ → B1/B2`
- Lines 115-117 (§7.1 P0 — OPS-004 command-4 closure): describes T06.11-FU01 as needing to land `_new_run_id` and `_default_output_dir`.

Both are stale.

**Specific recommended changes:**

1. **§5 row 5.4** — replace the observed-result column. Existing:
   > | 5.4 | `uv run superclaude eval run --suite real --eval E1` | End-to-end | exit 0 | **1 (NameError)** ❌ → [B1/B2](#7-follow-ups) | … |

   Replace with:
   > | 5.4 | `uv run superclaude eval run --suite real --eval E1` | End-to-end | exit 0 | **B1 closed at PR #66 (dce3c3cb); B2 (ptytest vendoring) still open — see §7.1** | (refreshed evidence link) |

2. **§7.1 (P0 — OPS-004 command-4 closure)** — change B1 row status from "open follow-up" to "RESOLVED". Move B2 (ptytest vendoring) to remain the only blocker. Existing line ~115-117 says:
   > | **B1** | `uv run superclaude eval run --suite real --eval E1` exits with `NameError: name '_new_run_id' is not defined` at `commands.py:1467`; a second undefined `_default_output_dir` is referenced at line 1469. T04.10 full body landed past the T04.09 deferral skeleton without the supporting private helpers. | **T06.11-FU01** … | RyanW |

   Replace with:
   > | **B1** (closed 2026-05-22) | The previously-missing `_new_run_id` and `_default_output_dir` helpers landed at PR #66 (`1ca25953`) and were remediated in `dce3c3cb`. `commands.py:1326` defines `_new_run_id`; `:1339` defines `_default_output_dir`. **T06.11-FU01 is RESOLVED.** | resolved at PR #66 / dce3c3cb | RyanW |

3. **§8 Sign-off** — Reconsider "Conditional GO" wording. With B1 closed, the conditional-GO authority sentence ("Per `Fallback Allowed: Yes` on T06.11 and T06.13, the v1 release MAY ship with §5 row 5.4 marked PARTIAL provided §7.1 names successor tasks with owners …") should be re-stated to reflect that only B2 (ptytest vendoring) gates an unconditional GO.

**Verification protocol:**
- `grep -n "_new_run_id\|_default_output_dir" /config/workspace/IronClaude/src/superclaude/cli/eval/commands.py` returns the two definitions (lines 1326 and 1339).
- After the doc edit: `grep -nE "B1.*(closed|RESOLVED|landed)" /config/workspace/IronClaude/docs/eval/release-checklist.md` should match.
- Cross-reference: PR #66 (`1ca25953`) merged the cliEval CLI module track; commit `dce3c3cb` cleared the NameError specifically.

---

### P1-3. `docs/eval/retention.md` — output-dir layout uses `<ISO>` instead of `<YYYY-MM-DD>`

**Document path:** `/config/workspace/IronClaude/docs/eval/retention.md`

**Reason for update:**
Lines 13 and 39 say the default run-dir is `.dev/eval-runs/<ISO>/<run-id>/`. The canonical reference doc `docs/user-guide/eval-pipeline.md` line 204 (and the actual `compose_run_dir` docstring at `artifact_layout.py:179`) say `<YYYY-MM-DD>/<run-id>/`. The `<ISO>` term is incorrect — the date segment is **only** the date portion, not a full ISO 8601 timestamp. An operator using the doc verbatim to look up artifacts at `.dev/eval-runs/2026-05-22T14:38:21Z/...` would fail. (H1 is the FR-G4 finding that anchored this layout via `compose_run_dir`.)

**Specific recommended changes:**

1. **Line 13.** Existing:
   > * The **run directory** under `--output-dir` (default `.dev/eval-runs/<ISO>/<run-id>/`)

   Replace with:
   > * The **run directory** under `--output-dir` (default `<cwd>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/`, anchored via `compose_run_dir` per FR-G4)

2. **Line 39.** Existing:
   > `--output-dir` (default the FR-G4 layout root `.dev/eval-runs/<ISO>/<run-id>/`) is treated as **append-only** by the harness.

   Replace with:
   > `--output-dir` (default the FR-G4 layout root `<cwd>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/`, anchored via `compose_run_dir`) is treated as **append-only** by the harness. When `--output-dir <X>` is supplied, the layout is layered underneath as `<X>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/` (H1 / FR-G4 — no longer flat under `<X>`).

3. **Add a note about the H1 fix** somewhere in §1 or §2 — operators reading this doc on its own should understand that `--output-dir <X>` is the OUTPUT ROOT, not the run-dir.

**Verification protocol:**
- `grep -n "compose_run_dir\b" /config/workspace/IronClaude/src/superclaude/cli/eval/artifact_layout.py` should match line 174 (`def compose_run_dir`) — the docstring at line 179 reads `<YYYY-MM-DD>`.
- `uv run python -c "from superclaude.cli.eval.artifact_layout import compose_run_dir; from pathlib import Path; print(compose_run_dir(Path('/tmp/x'), '2026-05-22T14:38:21Z', 'real'))"` should print a path containing `/tmp/x/.dev/eval-runs/2026-05-22/...` (with date only, not full ISO).
- Cross-reference AC matrix row **H1** (commands.py:eval_run resolved_output_root + compose_run_dir + writer rebinding) and test `test_run_anchors_output_via_compose_run_dir` at `tests/cli/eval/test_eval_run.py`.

---

### P1-4. `docs/eval/runtime.md` and `docs/eval/retry.md` — reference non-existent `suites/full.yaml` and `suites/quick.yaml`

**Document paths:**
- `/config/workspace/IronClaude/docs/eval/runtime.md`
- `/config/workspace/IronClaude/docs/eval/retry.md`

**Reason for update:**

Both docs use example invocations like:
- `superclaude eval run suites/full.yaml --parallel 8` (runtime.md L57, retry.md L65)
- `superclaude eval run suites/quick.yaml --eval E01 --eval E02` (runtime.md L63, retry.md L71)

But the canonical suite manifest is **`real.yaml`** (see `src/superclaude/cli/eval/suites/README.md` and the cliEval `eval list` enumeration), and `quick.yaml` is **explicitly deferred per DOC-OQ6** (see `src/superclaude/cli/eval/suites/README.md` §"Planned follow-up — `quick.yaml`"). There is no `full.yaml` and no `quick.yaml` shipped in v1. Additionally, the invocations use a positional argument shape (`eval run suites/full.yaml`) — actual CLI is `eval run --suite real` (flag, not positional; lookups use stem / name / path resolution per `commands.py:1008-1044`).

An operator copying these commands will hit `SuiteNotFound` for `full.yaml` or `quick.yaml` and `MissingOption '--suite'` for the positional form.

**Specific recommended changes:**

1. **`docs/eval/runtime.md` L55-64.** Existing:
   ```bash
   # Full baseline run (15 evals at the design default)
   superclaude eval run suites/full.yaml --parallel 8

   # Re-run only the failing ids after diagnosis (any number of --eval)
   superclaude eval run suites/full.yaml --eval E03 --eval E07

   # Quick smoke (3-4 evals); same flag, different subset
   superclaude eval run suites/quick.yaml --eval E01 --eval E02
   ```

   Replace with:
   ```bash
   # Full baseline run (15 evals at the design default)
   superclaude eval run --suite real --parallel 8

   # Re-run only the failing ids after diagnosis (any number of --eval)
   superclaude eval run --suite real --eval E3 --eval E7

   # Quick smoke via subset filter (quick.yaml deferred per DOC-OQ6; --eval is the v1 subset escape hatch)
   superclaude eval run --suite real --eval E1 --eval E2
   ```

2. **`docs/eval/retry.md` L63-72.** Same pattern as above — replace `suites/full.yaml` with `--suite real` and `suites/quick.yaml --eval E01 --eval E02` with `--suite real --eval E1 --eval E2`.

3. Both files also use eval-id format `E01`, `E03`, `E07` — but the actual suite uses `E1`, `E2.1`, `E2.2`, `E2.3`, `E3` … `E15` (see `src/superclaude/cli/eval/suites/real.yaml` and the EVAL_ID_PATTERN regex). The `E0n`-padded form does not match the regex (which is `[A-Z]\d+(\.\d+)?`). Update the examples to use `E1`, `E2`, `E3`, `E7`, `E10`, etc.

**Verification protocol:**
- `ls /config/workspace/IronClaude/src/superclaude/cli/eval/suites/*.yaml` should return only `real.yaml` (plus `suite.schema.json`).
- `uv run superclaude eval list` should enumerate the `real` suite only.
- After the doc edit: `grep -n "suites/full.yaml\|suites/quick.yaml" /config/workspace/IronClaude/docs/eval/runtime.md /config/workspace/IronClaude/docs/eval/retry.md` should return zero matches.
- `uv run superclaude eval describe --suite real --eval E2.1` should succeed; `uv run superclaude eval describe --suite full` should fail with `SuiteNotFound`. (Counter-validates the rename.)
- Cross-reference `src/superclaude/cli/eval/suites/README.md` §"Planned follow-up — `quick.yaml`" — the deferral is authoritative; do not invent a `quick.yaml` ahead of the trigger.

---

## P2 IMPORTANT findings

> Docs that omit new capabilities or have material drift from current behavior. An operator wouldn't discover the new flag/feature/invariant or would be confused about scope.

### P2-1. `docs/eval/retention.md` — silent on `summary.yaml`; only mentions `summary.{md,json}` + `junit.xml`

**Document path:** `/config/workspace/IronClaude/docs/eval/retention.md`

**Reason for update:**
Throughout the doc (lines 15, 47-49, 63, 152-156, 161-162) the artifact set is listed as `summary.md`, `summary.json`, `junit.xml`. Post M4 (the +1 yaml divergence closure), `summary.yaml` is **always** emitted alongside `.md` and `.json` (and `.junit.xml` only when `--junit`). See `src/superclaude/cli/eval/run_report.py:339` (`render_summary_yaml`) and `:366` (`_write_artifact_set` writes md/json/yaml unconditionally). The user-guide `eval-pipeline.md` line 35 calls this out: *"three canonical artifacts per run — `summary.md` (human-readable), `summary.json` (machine-readable), `summary.yaml` (CI-friendly) — plus an optional `junit.xml`"*.

**Specific recommended changes:**

1. **§1 TL;DR L14-15** — add `summary.yaml` to the artifact-set sentence:
   > * **Run-level summaries** (`summary.md`, `summary.json`, **`summary.yaml`**, `junit.xml` when `--junit`) are written before the process exits …

2. **§1 L47-49** — same edit to the Reporter writes list.

3. **§6 Summary retention matrix L156-162** — split the `summary.{md,json}` column into `summary.{md,json,yaml}` (or add a separate column). The matrix currently reads:
   > | Exit code | Run dir | summary.{md,json} | junit.xml | … |

   Replace with:
   > | Exit code | Run dir | summary.{md,json,yaml} | junit.xml | … |

4. **§4 Disk-budget breach advice L132** — the constant `DISK_BUDGET_RETENTION_ADVICE` quoted there says `summary.{md,json}`. Verify against `src/superclaude/cli/eval/disk_budget.py:149` — if the constant itself has been updated to include `.yaml`, copy the new text verbatim; if not, file a separate edit to the constant first (the doc says it must match the constant byte-for-byte and that drift is a test failure per `tests/cli/eval/test_retention_policy.py`).

**Verification protocol:**
- `grep -n "summary\.yaml\|summary.yaml\|render_summary_yaml" /config/workspace/IronClaude/src/superclaude/cli/eval/run_report.py` returns lines 339 (`render_summary_yaml`), 393 (`yaml_path = out / "summary.yaml"`), and 397 (write).
- `grep -n "summary\.yaml" /config/workspace/IronClaude/src/superclaude/cli/eval/reporter.py` confirms the writer-method delegation.
- After the doc edit: `grep -n "summary\.yaml" /config/workspace/IronClaude/docs/eval/retention.md` should return ≥3 matches.
- Cross-reference AC matrix row **M4** (`Promoted render_summary_yaml to run_report.py + shared `_write_artifact_set` helper; both writers delegate`).
- Cross-reference test `test_writer_emits_markdown_json_and_yaml` in `tests/cli/eval/test_run_report.py`.

---

### P2-2. `docs/eval/runtime.md` — no mention of `_NullLifecycleExecutor` warning, the new H3 summary line shape, or the H1 output-dir-is-output-root contract

**Document path:** `/config/workspace/IronClaude/docs/eval/runtime.md`

**Reason for update:**
This is the "runtime architecture" doc and currently describes scheduling and budget but **does not** surface three operator-visible behaviors that landed during the remediation:

1. The **stderr WARNING from `_NullLifecycleExecutor`** (M2 / CC3) — every `eval run` against the current code path emits `eval run: WARNING: _NullLifecycleExecutor active — non-production executor selected`. Operators reading runtime.md to understand what they see during a run will be surprised.
2. The **`--output-dir <X>` is the OUTPUT ROOT not the run-dir** (H1) — currently `runtime.md` does not call this out at all; the user-guide does (eval-pipeline.md L218).
3. The **`--verbose` summary line shape** `<P>P/<F>F/<S>S/<E>E/<I>I/<T>T` (H3) — runtime.md never describes what the operator sees on stdout post-run when `--verbose` is set.

**Specific recommended changes:**

1. **Add a new §"Operator-visible runtime warnings"** after §2 ("Why a 10-minute budget?") and before §"Re-running a subset". Suggested content:
   > ### `_NullLifecycleExecutor` warning (M2 / CC3)
   >
   > Until the production lifecycle executor ships, `eval run` is wired to a null executor and **the WARNING `eval run: WARNING: _NullLifecycleExecutor active — non-production executor selected` fires on stderr at the start of every run**. Run results from the null executor MUST NOT be treated as authoritative for production gating. The warning will stop firing once the production executor replaces the null stub.

2. **Add a §"Verbose summary line"** (or merge into the §"Re-running a subset" section) describing the H3 taxonomy:
   > When `--verbose` is set, `eval run` prints a single line to stdout post-run with the full DM-012 taxonomy: `run <run-id>: <P>P/<F>F/<S>S/<E>E/<I>I/<T>T in <duration>s -> <output_dir>`. P=PASS/XFAIL, F=FAIL/XPASS, S=SKIPPED, E=ERRORED, I=INTERRUPTED, T=TIMEOUT (see `EVAL_STATUSES` in `src/superclaude/cli/eval/models.py`).

3. **Add an `--output-dir` paragraph** to clarify that the FR-G4 layout is layered underneath any operator-supplied root (cross-reference `docs/eval/retention.md` once it's updated).

**Verification protocol:**
- `grep -n "_NullLifecycleExecutor active" /config/workspace/IronClaude/src/superclaude/cli/eval/commands.py` returns line 1876 — the literal WARNING string.
- `grep -n "_format_run_summary_line" /config/workspace/IronClaude/src/superclaude/cli/eval/commands.py` returns line 1531; the format-string at L1542-1550 emits the `P/F/S/E/I/T` shape.
- Cross-reference AC matrix rows **M2** (NullLifecycleExecutor WARNING), **H3** (`_format_run_summary_line` full taxonomy), and **H1** (compose_run_dir anchoring).
- Test `test_format_run_summary_line_renders_errored_interrupted_timeout` at `tests/cli/eval/test_run_summary.py` and `test_run_emits_warning_when_null_lifecycle_executor_active` at `tests/cli/eval/test_eval_run.py` pin the contracts.

---

### P2-3. `docs/eval/retry.md` — silent on the `_NullLifecycleExecutor` warning and the H3 verbose summary line

**Document path:** `/config/workspace/IronClaude/docs/eval/retry.md`

**Reason for update:**
Mirror issue of P2-2: an operator running `eval run … --eval E03 --eval E07` after a failure (the doc's main use case) will see the stderr WARNING and the new P/F/S/E/I/T summary line. Neither is mentioned. The doc references "the `--keep-home` flag" and "the summary table" but never describes the new H3 shape.

**Specific recommended changes:**

1. **§"Re-running a failed eval — the `--eval` subset path" L57-73** — after the bash block, add a one-paragraph aside:
   > After the subset re-run, the Reporter writes the same `summary.{md,json,yaml}` artifact set under the subset run's own run-dir (which is independent of the original run-dir). If you pass `--verbose`, the post-run stdout line carries the full P/F/S/E/I/T taxonomy (see `docs/user-guide/eval-pipeline.md` §"Reading the verbose summary line"). Subset runs against the current code path emit the same `_NullLifecycleExecutor` WARNING on stderr as full runs (M2 / CC3 — see `docs/eval/runtime.md` §"Operator-visible runtime warnings" once that section lands per P2-2).

2. **Add a sub-section** under §"Operator-facing invariants" (line ~155) noting that `RUN_INTERRUPTED_EXIT_CODE` is exit code `3` (not 130) — pinned in `exit_codes.py::INTERRUPTED` (helpful when operators write CI scripts that key off the exit code).

**Verification protocol:**
- Same checks as P2-2 (the symbols and constants are identical).
- After the edit: `grep -n "_NullLifecycleExecutor\|P/F/S/E/I/T\|summary.yaml" /config/workspace/IronClaude/docs/eval/retry.md` should return matches in the new sub-sections.

---

### P2-4. `docs/eval/scratch-roots.md` — does not document the H4 bare-prefix rejection or the H5 write-before-validate ordering

**Document path:** `/config/workspace/IronClaude/docs/eval/scratch-roots.md`

**Reason for update:**
This is the **authoritative AC12 / OPS-002 doc**. Two recent H-level invariants tightened the allowlist semantics, but the doc still describes the old behavior:

1. **H4 — Bare-prefix rejection.** Line 19 says root #2 is `<repo>/.dev/eval-runs/` and root #3 is `--output-dir <path>`. **Missing:** "Passing the allowlist prefix itself with no sub-path (e.g. `/tmp/eval-runs`) raises `ScratchRootViolation` — only strict sub-paths are accepted." This was the AC12 tautology removed at H4 (config.py:243-249 removed the `resolved == prefix` branch). Operators on the old behavior could pass the bare prefix and get accepted; the doc still implies that's fine.

2. **H5 — Allowlist extension before any `mkdir`.** §"Why an allowlist (and not a denylist)" §3 ("HomeIsolation containment") describes the layered defense, but says nothing about the **ordering invariant**: at both `commands.py:1727-1752` and `isolation.py:550-577`, the runtime allowlist is extended **before** the corresponding `mkdir` runs. An operator reading the doc would not know that a write-before-validate path is closed at both sites.

**Specific recommended changes:**

1. **§"The 3 allowed roots" table footer (after L20)** — add a new paragraph:
   > **H4 / strict-sub-path rule:** A bare allowlist prefix (e.g. `resolve_scratch_root("/tmp/eval-runs")` with no sub-path) **raises `ScratchRootViolation`**. Only strict sub-paths of one of the three allowed roots are accepted — `/tmp/eval-runs/<run-id>/` is fine, but `/tmp/eval-runs` itself is not. This closes the AC12 tautology where the allowlist check would silently accept the prefix as a "match" of itself. See `test_resolve_scratch_root_rejects_bare_prefix` in `tests/cli/eval/test_scratch_root_allowlist.py`.

2. **§"Why an allowlist (and not a denylist)" §3 (HomeIsolation containment)** — extend the entry to mention the H5 ordering invariant:
   > 3. **HomeIsolation containment** (`containment_guard`, T02.08) re-applies the check after `mkdtemp` so a symlink swap between loader-time and setup-time is still caught. **H5 ordering invariant:** the runtime allowlist is extended with the resolved `--output-dir` (and the derived `home_root`) **before** the corresponding `mkdir(parents=True)` runs at both call sites (`commands.py:eval_run` and `isolation.py:HomeIsolation.setup`). A non-allowlisted path raises **before** any on-disk side effect.

3. **§"Updating the policy"** — add a fourth update site: "test_scratch_root_allowlist.py and test_containment.py also pin the H4/H5 invariants; any allowlist change must update them too."

**Verification protocol:**
- `grep -n "resolved == prefix" /config/workspace/IronClaude/src/superclaude/cli/eval/config.py` should return **zero matches** (H4 fix removed this branch).
- `grep -n "runtime_allowed\|home_root.mkdir" /config/workspace/IronClaude/src/superclaude/cli/eval/commands.py` confirms `runtime_allowed = …` (line 1768) precedes `home_root.mkdir` (after line 1783) — the H5a fix.
- `uv run python -c "from superclaude.cli.eval.config import resolve_scratch_root, EvalConfig; resolve_scratch_root('/tmp/eval-runs', config=EvalConfig())"` should raise `ScratchRootViolation`.
- Tests pinning H4: `tests/cli/eval/test_scratch_root_allowlist.py::test_resolve_scratch_root_rejects_bare_prefix` + `test_accepts_immediate_subdir_of_allowlist_root`.
- Tests pinning H5: `tests/cli/eval/test_home_isolation_extend.py::test_eval_run_extends_allowlist_before_mkdir` + `tests/cli/eval/test_containment.py::test_home_isolation_setup_rejects_non_allowlisted_home_root_before_mkdir`.
- Cross-reference AC matrix rows **H4**, **H5a**, **H5b**.

---

## P3 NICE-TO-HAVE findings

> Docs that could be more thorough but aren't actively misleading.

### P3-1. `CHANGELOG.md` — no entry for the cliEval Phase 5+6 remediation

**Document path:** `/config/workspace/IronClaude/CHANGELOG.md`

**Reason for update:**
The changelog has no entry for the remediation task (TASK-RF-20260522-153212) or the recent merges (PRs #66, #68, #70, #72, #73, sc-troubleshoot v2). A changelog entry would let downstream consumers see the surfaced changes (canonical exit codes, layout fix, summary.yaml, etc.) without reading the AC matrix.

**Specific recommended changes:**

Add a new entry at the top of the changelog (assuming Keep-a-Changelog style):

```markdown
## [Unreleased]

### cliEval (Phase 5+6 remediation, TASK-RF-20260522-153212)

#### Added
- `src/superclaude/cli/eval/exit_codes.py` with exactly 4 canonical exit codes (SUCCESS=0, FAILURES=1, USAGE_ERROR=2, INTERRUPTED=3). All 11 `*_EXIT_CODE` constants in the eval module re-export from here (CC2).
- `orchestrator.allocate_session_id(run_id, eval_id)` helper — the canonical session-id allocator (M5).
- `eval doctor --output-dir` now rejects file paths via `file_okay=False` (symmetric with `eval run`) (M6).
- Stderr WARNING when `_NullLifecycleExecutor` is the active executor (M2 / CC3).

#### Changed
- `eval run --output-dir <X>` now anchors via `compose_run_dir` so artifacts land at `<X>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/` (no more flat layout under `<X>`) (H1 / FR-G4).
- `_format_run_summary_line` renders the full DM-012 taxonomy `P/F/S/E/I/T` instead of eliding ERRORED/INTERRUPTED/TIMEOUT (H3).
- Coverage gate fails closed on corrupt `~/.claude/settings.json` instead of silently passing (H2 / FR-G5).
- `resolve_scratch_root("/tmp/eval-runs")` (bare allowlist prefix with no sub-path) now raises `ScratchRootViolation`; only strict sub-paths are accepted (H4 / AC12).
- Runtime allowlist extension now happens **before** any `mkdir` at both `commands.py` and `isolation.py` call sites (H5a, H5b / OPS-002).
- `EVAL_ID_PATTERN` is now the single source of truth in `artifact_layout.py`; `loader.py` imports it as alias (CC1).
- Both `Reporter.write` and `write_aggregated_report` now emit `summary.yaml` alongside `summary.md` / `summary.json` (M4).
- `RunTotals` keys derived from `EVAL_STATUSES` partitions in `models.py` (no hardcoded literals) (M3).

#### Fixed
- `_new_run_id` and `_default_output_dir` helpers — previously raised `NameError` (closed via PR #66 / `dce3c3cb`); `validation-commands.md` B1 follow-up now RESOLVED.
```

**Verification protocol:**
- After the doc edit: `grep -n "exit_codes\|compose_run_dir\|summary.yaml\|allocate_session_id" /config/workspace/IronClaude/CHANGELOG.md` should match.
- Cross-reference AC matrix rows H1–H5, M2–M6, CC1–CC3 — every entry above maps to an AC row.

---

### P3-2. `docs/developer-guide/documentation-index.md` (or sibling index) — no link to `docs/user-guide/eval-pipeline.md`

**Document path:** `/config/workspace/IronClaude/docs/developer-guide/documentation-index.md` (and possibly `docs/developer-guide/README.md` if it carries the same index)

**Reason for update:**
The user-guide gold-standard doc `docs/user-guide/eval-pipeline.md` is the single best entry point for operators (it links to every eval doc, every source file, every test). The developer-guide documentation index should link to it prominently. Currently no `eval` references exist in the index (confirmed by grep returning empty). New operators discovering the harness will hit `docs/eval/*.md` (the deep-tech refs) without the orientation the user-guide provides.

**Specific recommended changes:**

Add a row / link to the documentation-index pointing at:
- `docs/user-guide/eval-pipeline.md` — "cliEval (`superclaude eval`) — operator user guide"
- with a one-line description: "Task-oriented walkthrough of `eval doctor` / `eval list` / `eval describe` / `eval run`. Source of truth for flag tables, exit codes, output layout, and the scratch-root allowlist."

Also: cross-link from `docs/developer-guide/technical-architecture.md` (or the sibling testing-debugging.md) if those docs describe the wider CLI architecture — none of them currently mention the eval harness at all (confirmed via grep).

**Verification protocol:**
- After the doc edit: `grep -n "eval-pipeline\|cliEval" /config/workspace/IronClaude/docs/developer-guide/documentation-index.md` should match.
- `wc -l /config/workspace/IronClaude/docs/user-guide/eval-pipeline.md` confirms the target doc exists at ~400 lines (verified during this audit).

---

## Out of scope (no edit recommended)

The following docs were inspected and **do not need edits** for the cliEval remediation:

- **`docs/user-guide/eval-pipeline.md`** — already updated for the remediation; serves as the gold-standard reference doc for the audit. Last-verified header at line 5 confirms 2026-05-22 post-remediation.
- **`docs/eval/mig-002-batch-plan.md`** — describes the eval-batch rollout policy and coverage map. No remediation-relevant drift; the matcher families, batch defs, and `coverage.py::default_matcher_filter` references are still current.
- **`docs/eval/v2-followups.md`** — v2 follow-up roadmap (macOS + CI). Independent of the remediation surface; no drift.
- **`src/superclaude/cli/eval/suites/README.md`** — already-canonical naming convention doc; the `quick.yaml` deferral is intact and referenced correctly by the user-guide.
- **`docs/user-guide/{commands,flags,agents,modes,...}.md`** — none reference the eval CLI; out of scope.
- **`docs/reference/*.md`, `docs/developer-guide/{contributing-code,technical-architecture,testing-debugging,sprint-tui-reference}.md`** — no eval refs.
- **`README.md` (repo root, Platform support section, lines 243-265)** — already correct: declares Linux-only v1, refers to AC1 / DOC-OQ9 / decisions.md. No remediation-relevant drift.
- **`src/superclaude/commands/troubleshoot.md`** + **`src/superclaude/skills/sc-troubleshoot-protocol/*`** — already documents Wave 1.5 doc grounding (commit `9f4503f8`) and Tier 1/2/3 structure. The `eval_run.py` references in `refs/hypothesis-card-template.md` are illustrative examples (showing a fictional "missing Path import" bug), not behavior-of-record claims about the actual cliEval module.
- **`.claude/agents/*`** + **`src/superclaude/agents/*`** — no cliEval references.
- **`.dev/releases/current/cliEval/*`** — release-spec ground truth; these are inputs to the remediation, not consumers of it. They will be updated as part of the OPS-005 release-time walk-through (already tracked in T06.11 / T06.13 / T06.16).

---

## Audit methodology notes

- **Auggie semantic discovery** was used to surface all docs referencing the cliEval CLI surface, exit codes, output layout, scratch-root policy, summary-line shape, and the M2/M3/M4/M5/M6/CC1/CC2 changes (single fan-out call, results filtered manually).
- **Grep + git log** were used to cross-validate against the actual source-of-truth in `src/superclaude/cli/eval/*.py` and the recent commits (`af97a054` … `1ca25953`).
- **Runtime verification** via `uv run python -c …` and `CliRunner().invoke(eval_group, [<sub>, '--help'])` confirmed:
  - `_new_run_id` and `_default_output_dir` exist (B1 cleared)
  - `exit_codes.{SUCCESS,FAILURES,USAGE_ERROR,INTERRUPTED}` = `0,1,2,3`
  - `eval doctor --help`, `eval run --help`, `eval list --help`, `eval describe --help` all render the post-remediation flag set
- **AC matrix cross-reference**: every P1/P2 finding cites at least one row in `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260522-153212/phase-outputs/reports/06-ac-matrix.md`.

---

**End of audit.** No code or doc was modified during this audit.
