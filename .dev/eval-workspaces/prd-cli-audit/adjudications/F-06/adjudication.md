# F-06 Adjudication — Resume entirely broken

**Mode**: /sc:adversarial Mode B (analyzer / refactorer / architect → convergence)
**Source finding**: `.dev/eval-workspaces/prd-cli-audit/findings/F-06-resume-entirely-broken.md`
**Preliminary severity**: HIGH
**Pattern tags**: P2, P5, P7, P8

---

## Re-verification (read-only, cited)

### 1. Executor never consults `config.resume_from`

`PrdExecutor.run()` at `src/superclaude/cli/prd/executor.py:344-415` iterates `_STAGE_A_STEPS` from index 0 unconditionally:

- `executor.py:371` — `for step_id, step_name, builder_name, _ in _STAGE_A_STEPS:` (no slicing, no `resume_from` lookup)
- `executor.py:393` — Stage B is invoked unconditionally when outcome != "halt"
- `executor.py:398-402` — Step 15 (`present-complete`) is executed unconditionally when not halted

A repo-wide grep for `resume_from` in `src/superclaude/cli/prd/` returns hits ONLY in three writer/validator sites:

| File:line | Role |
|---|---|
| `src/superclaude/cli/prd/models.py:196` | Field declaration on `PrdConfig` |
| `src/superclaude/cli/prd/config.py:57,75,81,93-95,143` | Function arg, validation, dataclass assignment |
| `src/superclaude/cli/prd/commands.py:180` | Set from CLI subcommand |

Zero hits in `executor.py`. The field is **write-only**.

### 2. `prd resume` subcommand flag surface

`src/superclaude/cli/prd/commands.py:135-191` defines `resume` with exactly three options:

- `commands.py:137-141` — `--max-turns`
- `commands.py:143-147` — `--model`
- `commands.py:148-152` — `--debug`

It does **not** declare `--product`, `--tier`, `--output`, or `--where`. Click's default behavior rejects unknown long options with `Error: No such option: --product` and exits non-zero.

### 3. `resume_command()` emits flags the CLI cannot accept

`src/superclaude/cli/prd/models.py:260-271`:

```python
parts = ["superclaude", "prd", "resume", self.halt_step]
if self.config.product_name:
    parts.extend(["--product", self.config.product_name])      # rejected by Click
if self.config.model:
    parts.extend(["--model", self.config.model])               # accepted
if self.config.tier != "standard":
    parts.extend(["--tier", self.config.tier])                 # rejected by Click
```

This emitted string is surfaced to the user via `diagnostics.py:127` (stored on the failure report), `diagnostics.py:232-235` (formatted into the markdown report under a fenced block), and `diagnostics.py:259` (returned from `generate_resume_command`). The user-visible recovery instruction is **non-executable**.

### 4. No base-class consumer

Both `PrdExecutor` (`executor.py:324`) and the sibling `CliPortifyExecutor` are standalone — `grep -ln "class.*Executor"` finds no shared base class for `prd/executor.py`. There is no inherited skip logic that could rescue the missing consumer.

### 5. task_dir continuity

`config.py:119-125` derives `task_dir` from `product_slug` (`prd-<slug>` or `prd-task` fallback). Because the `resume` subcommand omits `--product`, a resumed run constructs `task_dir = <output_path>/prd-task/`, which will not match the original `prd-<original-slug>/` directory created by the initial `run`. Any "resume" therefore writes to a fresh directory and ignores prior artifacts.

`check_existing_work` (`inventory.py:26`) scans `TASK-PRD-*` directories, not `prd-<slug>` directories, so it does not paper over the mismatch.

---

## Persona 1 — Analyzer (reproducibility)

**Scenario A: User pastes `resume_command()` output verbatim.**

```
$ superclaude prd run "Add search" --product foo --tier heavyweight
# Ctrl-C after step 3 → halt_step = "scope-discovery"
# resume_command() emits: superclaude prd resume scope-discovery --product foo --tier heavyweight
$ superclaude prd resume scope-discovery --product foo --tier heavyweight
Error: No such option: --product
$ echo $?
2
```

Click aborts before the executor is touched. The documented recovery path is **un-executable**. Reproducibility: **deterministic** (Click's option parser is configured with the default `ignore_unknown_options=False`).

**Scenario B: User manually strips the unknown flags.**

```
$ superclaude prd resume scope-discovery
```

Click accepts the invocation. `resolve_config(request="", resume_from="scope-discovery")` succeeds (config.py:93-100 validates the step ID against `_STEP_ID_PATTERN`). `PrdExecutor(config).run()` is called.

- `executor.py:353-356`: dry_run gate skipped (not set)
- `executor.py:363`: `create_task_dirs(self._config.task_dir)` creates `prd-task/` fresh (no `--product` → `product_slug = ""` → `task_dir_name = "prd-task"` per config.py:124)
- `executor.py:371`: loop starts at index 0 (`check-existing`), runs **every** Stage A step
- Stage B and Step 15 run unconditionally afterward (executor.py:391-404)

Outcome: full pipeline re-run from `check-existing` at `standard` tier in a fresh `prd-task/` directory, ignoring the original `prd-foo/` artifacts. The user has no feedback that resume was a no-op — output looks identical to a fresh `run` with an empty request.

**Reproducibility verdict**: Both scenarios are deterministic and traceable to specific line numbers. Confidence in the bug: 0.99.

---

## Persona 2 — Refactorer (blast radius)

**Other flag-emission sites producing user-paste commands?**

Grep for command-construction patterns:

- `diagnostics.py:53,127,232-235,241,259` — all flow through `PrdPipelineResult.resume_command()`. Single emission site; single fix point.
- No other `["superclaude", "prd", ...]` list construction found in `src/superclaude/cli/prd/`.

**Affected downstream surfaces**:

1. The markdown failure report (`diagnostics.py:232-235`) prints the broken command in a fenced code block under a heading — users will copy-paste it directly.
2. `generate_resume_command()` (`diagnostics.py:241-259`) is a public-looking helper that returns the same broken string; any future caller inherits the bug.
3. The `resume` subcommand docstring (`commands.py:159-170`) advertises `superclaude prd resume parse-request` as the recovery path, reinforcing the expectation that resume works.

**Collateral on dependent state**:

- A "resumed" run with no `--product` writes to `prd-task/` and never sees `prd-<slug>/`. Earlier artifacts are not overwritten — they are **orphaned**. Disk fills with stale partials.
- The completion step (`present-complete`) runs unconditionally on the re-run, potentially emitting a "PRD complete" message based on the fresh (and likely lower-quality) standard-tier pipeline. Downstream consumers reading the "complete" PRD see degraded output without warning.
- Budget accounting (`TurnLedger`, executor.py:333) restarts from `--max-turns`, masking that double the turns have actually been consumed across the two runs.

**Blast radius**: Localized to PRD CLI surface (one subcommand + one model method + the executor loop), but the **user-trust** blast radius is wide — every halt produces broken guidance.

**Fix surface (estimate)**:

| Change | Lines touched |
|---|---|
| Add `--product/--tier/--output/--where` options to `resume` (commands.py:135-152) | ~25 |
| Plumb new args through `resolve_config` call (commands.py:174-181) | ~5 |
| Slice `_STAGE_A_STEPS` by `resume_from` index in `run()` (executor.py:371) | ~10 |
| Handle Stage B / Step 15 resume points (executor.py:391-404) | ~15 |
| Tests covering both flag-acceptance and skip-to-step behavior | new file, ~80 |

Total: ~50 production LOC + ~80 test LOC. Self-contained, no cross-module ripples.

---

## Persona 3 — Architect (severity calibration)

**Is HIGH the right floor, or is this CRITICAL?**

The documented recovery path is broken **in two independent ways**:
1. The flag the executor would need (`resume_from`) is silently ignored.
2. The exact command string the system tells the user to run is rejected by the CLI.

This is not a "rare edge case." The codebase actively produces halts:

- `executor.py:385-389` — STRICT gate failure halts; happens on the well-known `parse-request`/`research-notes` gates.
- `executor.py:686-689` — assembly STRICT gate halt.
- `executor.py:836-838` — budget exhaustion mid-fix-cycle halt.
- `executor.py:872-876` — fix-cycle exhaustion halt.
- `executor.py:957-970` — `_handle_shutdown` triggered by SIGINT/SIGTERM.

Halts are designed into the pipeline as a first-class flow. The expected mitigation — resume — is the **only** documented way to avoid re-spending the entire turn budget (300 turns × subprocess cost) on a re-run. A broken resume effectively turns every halt into "throw it all away and pay the full cost again."

**User-blocking?** Yes — the user can no longer make incremental progress on long pipelines once any halt occurs. `heavyweight` tier with 8 investigation agents + 3 web research agents is exactly the configuration where resume matters most.

**Data loss?** Soft — old artifacts remain on disk under `prd-<original-slug>/` but are orphaned and never re-consulted. No silent corruption, but silent waste.

**Severity calibration**:

- Not MEDIUM. The feature is advertised in command help text and emitted in diagnostic output; users will discover it the moment they hit any halt.
- Not CRITICAL in the "data destruction / security breach" sense — no irreversible harm.
- **HIGH is correct.** The documented happy-path recovery is non-functional, the user receives misleading guidance, and the only workaround (re-running from scratch with manual flag reconstruction) defeats the purpose of the feature.

Optional escalation argument: if the original finding's preliminary HIGH is taken as a soft ceiling, the dual-failure nature (executor + CLI both broken independently) and the breakage of user-facing diagnostic output could justify CRITICAL. I land on **HIGH (firm)** because no data is destroyed and a workaround exists, but I would not contest a CRITICAL re-classification.

---

## Convergence

| Field | Value |
|---|---|
| **Verdict** | CONFIRMED |
| **Convergence score** | 1.00 (all three personas agree; all citations re-verified file:line) |
| **Final severity** | HIGH (firm; would not contest CRITICAL) |
| **Fix difficulty** | LOW-MEDIUM (~50 prod LOC + ~80 test LOC, single module, no API breakage) |
| **Effort estimate** | 0.5–1 dev-day including tests |
| **Blast radius** | Localized code; wide user-trust impact |
| **Regression risk** | Low — adding options is additive; loop-slicing is well-contained behind a `resume_from` guard |

### Synthesis

The finding is fully reproduced. Three independent defects collaborate to break the resume contract:

1. **`PrdExecutor.run()` (`executor.py:344-415`)** never reads `config.resume_from`; the field is write-only.
2. **`resume` subcommand (`commands.py:135-191`)** declares only `--max-turns`, `--model`, `--debug` — missing `--product`, `--tier`, `--output`, `--where`. Click hard-rejects unknown options.
3. **`PrdPipelineResult.resume_command()` (`models.py:260-271`)** emits `--product` and `--tier` that the resume subcommand cannot accept, so the user-facing recovery string is non-executable.

Even when a user manually strips the rejected flags, the executor re-runs every step from index 0 in a fresh `prd-task/` directory (because `task_dir` is derived from `product_slug` and no `--product` is passed). The original artifacts are orphaned, the turn budget is double-spent, and the run silently completes at `standard` tier regardless of the original `--tier` selection.

**Recommended minimum fix**:
- Extend the `resume` subcommand surface to match `run` for `--product`, `--tier`, `--output`, `--where`.
- Add a slice/skip path in `PrdExecutor.run()` that consults `config.resume_from`, locates the index in `_STAGE_A_STEPS` (and Stage B equivalents), and starts the loop there.
- Audit `_handle_shutdown` (executor.py:957) to ensure `halt_step` is set to a value `_STEP_ID_PATTERN` accepts — currently it pulls from `getattr(last.step, "name", "unknown")` (line 967) which may not match the step-id regex.
- Add a test that round-trips: run → halt → copy `result.resume_command()` → exec it → assert pipeline continues from the halt step in the original `task_dir`.

**No fixes performed (read-only adjudication).**
