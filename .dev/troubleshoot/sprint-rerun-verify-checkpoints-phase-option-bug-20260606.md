# SuperClaude sprint rerun-tasks post-merge verify-checkpoints option bug

## Observed symptom

After a successful surgical rerun/merge such as:

```bash
superclaude sprint rerun-tasks .dev/releases/current/v1-MVP/tasklists/tasklist-index.md --phase 13 --tasks T13.02 --ignore-deps
```

or equivalent reruns for `T13.06` / `T13.17`, the command prints the success message:

```text
Rerun merged: 1 task(s) re-executed for phase 13.
```

and then emits a secondary Click usage error:

```text
Usage: superclaude sprint verify-checkpoints [OPTIONS] OUTPUT_DIR
Try 'superclaude sprint verify-checkpoints --help' for help.

Error: No such option '--phase'. Did you mean '--help'?
```

I reproduced the option parser error directly with the installed CLI:

```bash
superclaude sprint verify-checkpoints --recover --phase 13 --quiet 2>&1 || true
```

Output:

```text
Usage: superclaude sprint verify-checkpoints [OPTIONS] OUTPUT_DIR
Try 'superclaude sprint verify-checkpoints --help' for help.

Error: No such option '--phase'. Did you mean '--help'?
```

## Root cause

The post-merge `rerun-tasks` success path invokes `verify-checkpoints` with an argument vector that does not match the `verify-checkpoints` Click contract.

### Installed CLI evidence

Installed `rerun_tasks.py` auto-invokes `verify-checkpoints` after a successful merge when checkpoint verification is not disabled:

- `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/cli/sprint/rerun_tasks.py:1446` labels this as the auto-invoke step.
- `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/cli/sprint/rerun_tasks.py:1447` gates it on `exit_code == 0 and merge_back and not no_verify_checkpoints`.
- `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/cli/sprint/rerun_tasks.py:1450-1460` builds `uv run superclaude sprint verify-checkpoints --recover --phase <phase> --quiet`.

Installed `commands.py` defines `verify-checkpoints` differently:

- `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/cli/sprint/commands.py:387` registers `@sprint_group.command("verify-checkpoints")`.
- `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/cli/sprint/commands.py:388-391` requires positional `OUTPUT_DIR`.
- `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/cli/sprint/commands.py:392-402` defines only `--recover` and `--json`.
- `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/cli/sprint/commands.py:403` has function signature `verify_checkpoints(output_dir: Path, recover: bool, as_json: bool)`.

Installed `superclaude sprint verify-checkpoints --help` confirms the runtime contract exposes only:

```text
Usage: superclaude sprint verify-checkpoints [OPTIONS] OUTPUT_DIR
Options:
  --recover
  --json
  --help
```

### Source-of-truth evidence in IronClaude

The same mismatch exists in the source tree at `/config/workspace/IronClaude`:

- `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1446-1460` uses the same invalid post-merge subprocess argv with `--phase`, `--quiet`, and no `OUTPUT_DIR`.
- `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py:387-403` defines `verify-checkpoints` with required positional `output_dir` and only `--recover` / `--json` options.
- `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py:420-424` derives `tasklist-index.md` from `output_dir` and builds the manifest for that release directory.
- `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py:426-433` performs recovery for the full discovered phase set when `--recover` is provided.
- `/config/workspace/IronClaude/src/superclaude/cli/sprint/config.py:347-352` shows `load_sprint_config()` already computes `config.release_dir`, which is the release directory `verify-checkpoints` expects as `OUTPUT_DIR`.

Existing regression tests are too weak to catch this exact bug:

- `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks_e2e.py:287-294` asserts the subprocess was called and contains `verify-checkpoints` plus `--recover`, but does not assert that the argv is parseable or includes `OUTPUT_DIR`.
- `/config/workspace/IronClaude/tests/sprint/e2e_real/test_e2e_rerun_happy_path.py:229-233` has the same weak assertion pattern.
- `/config/workspace/IronClaude/tests/sprint/test_checkpoints.py:529-571` covers the `verify_checkpoints` CLI itself, but only for the documented contract: positional output directory, `--json`, and `--recover`.

## Fix options, ranked

### 1. Recommended: patch `rerun_tasks.py` to call the existing CLI contract correctly

Change the post-merge subprocess argv to pass the release directory and remove unsupported flags:

```python
[
    "uv",
    "run",
    "superclaude",
    "sprint",
    "verify-checkpoints",
    str(config.release_dir),
    "--recover",
]
```

Why this ranks first:

- It fixes the immediate bug at the call site that is demonstrably wrong.
- It preserves the current public `verify-checkpoints` contract.
- `verify-checkpoints` already knows how to discover all phases from `OUTPUT_DIR/tasklist-index.md` and recover missing checkpoints.
- It avoids adding half-implemented `--phase` semantics to checkpoint recovery.
- It requires the smallest code and test changes.

Tradeoff: it verifies/recovers all declared checkpoints in the release, not just the rerun phase. That is already the current documented behavior of `verify-checkpoints`.

### 2. Add `--quiet` only, but still patch the call site

Add a `--quiet` flag to `verify-checkpoints` that suppresses `_print_checkpoint_table()` after writing `manifest.json`, then invoke:

```python
[
    "uv",
    "run",
    "superclaude",
    "sprint",
    "verify-checkpoints",
    str(config.release_dir),
    "--recover",
    "--quiet",
]
```

Why this is second:

- It may match the original author intent to avoid noisy checkpoint table output after `rerun-tasks`.
- It is backward-compatible because `--quiet` is additive.
- It still requires passing `OUTPUT_DIR` and should not include `--phase` unless true phase filtering is implemented.

Tradeoff: it expands the CLI surface for convenience, but does not address phase-scoped recovery.

### 3. Extend `verify-checkpoints` with `--phase` and `--quiet`

Add options:

- `--phase INTEGER`: filter the manifest and recovery pass to one phase.
- `--quiet`: suppress table output.

Implementation would need to filter `manifest` before `recover_missing_checkpoints()` and pass only the selected phase's tasklist in `phase_tasklists`, or else recover all phases and then filter output. Filtering before recovery is less surprising.

Why this is lower-ranked:

- It changes the public CLI contract and introduces new behavior that must be specified.
- Current `build_manifest()` always discovers all phases; true phase filtering needs careful handling to avoid accidentally writing a manifest that drops entries for other phases.
- If `manifest.json` is intended to represent the full sprint, writing a phase-filtered manifest to the same path could be data-loss/confusing. A phase-filtered command may need either a full manifest with filtered display, or a different output mode.

### 4. Make `OUTPUT_DIR` optional and infer it from cwd or the rerun index

This is not recommended.

Why it is risky:

- `verify-checkpoints` is currently documented around explicit `OUTPUT_DIR`.
- `rerun-tasks` already has the correct `config.release_dir`; implicit cwd inference would paper over the caller bug.
- The observed invocation is still invalid because `--phase` and `--quiet` are not defined.

## Recommended implementation sketch

1. In `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py`, update the subprocess argv at lines 1450-1460 to call the existing CLI contract:

   ```python
   subprocess.run(
       [
           "uv",
           "run",
           "superclaude",
           "sprint",
           "verify-checkpoints",
           str(config.release_dir),
           "--recover",
       ],
       check=False,
   )
   ```

2. Optionally add `--quiet` as a small additive feature in `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py`:
   - Add `@click.option("--quiet", is_flag=True, help="Write manifest without printing the status table.")`.
   - Change the signature to `verify_checkpoints(output_dir: Path, recover: bool, as_json: bool, quiet: bool)`.
   - After `write_manifest()`, return early when `quiet` is true and `as_json` is false.
   - Keep `--json` behavior unchanged; decide whether `--json --quiet` should emit JSON or whether those flags should be mutually exclusive. Prefer letting `--json` win for backward compatibility.

3. Do not add `--phase` in the minimal fix unless there is a concrete product requirement for phase-scoped checkpoint manifests. If that requirement exists, define how `manifest.json` should behave before implementation.

## Test plan

### Minimal patch tests

1. Strengthen rerun auto-invoke tests:
   - In `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks_e2e.py`, extend the assertion around lines 291-294 to require:
     - `verify_argv` contains `str(config.release_dir)` or the seeded release directory path.
     - `verify_argv` does not contain `--phase`.
     - `verify_argv` does not contain `--quiet` unless `--quiet` is implemented.
   - Apply the same strengthening to `/config/workspace/IronClaude/tests/sprint/e2e_real/test_e2e_rerun_happy_path.py` around lines 229-233.

2. Add a focused unit test for parseability of the constructed argv shape. The test can invoke `verify_checkpoints` directly with `[str(tmp_path), "--recover"]` using the fixture pattern in `/config/workspace/IronClaude/tests/sprint/test_checkpoints.py:529-571`.

3. Run targeted tests with UV only:

   ```bash
   uv run pytest tests/sprint/test_checkpoints.py -q
   uv run pytest tests/sprint/test_rerun_tasks_e2e.py -q
   uv run pytest tests/sprint/e2e_real/test_e2e_rerun_happy_path.py -q
   uv run pytest tests/sprint/test_cli_contract.py -q
   ```

### If adding `--quiet`

Add tests to `/config/workspace/IronClaude/tests/sprint/test_checkpoints.py`:

- `verify_checkpoints [OUTPUT_DIR, --recover, --quiet]` exits 0.
- It writes `manifest.json`.
- It does not print the table text.
- `--json` still emits JSON when combined with `--quiet`, or the command errors cleanly if the chosen contract makes them mutually exclusive.

### If adding `--phase`

Add tests before implementation that lock down the intended manifest behavior:

- `--phase 13 --recover` recovers only phase 13 checkpoint reports.
- The generated `manifest.json` behavior is explicitly asserted: either full-sprint manifest with per-entry recovery updates, or phase-filtered manifest. Avoid ambiguous partial overwrite of a file named simply `manifest.json`.
- Invalid phase numbers error cleanly.

## Rollout and backward compatibility notes

- The minimal call-site patch is backward-compatible for users because it does not change public CLI flags.
- Existing direct users of `superclaude sprint verify-checkpoints OUTPUT_DIR --recover` continue to work.
- Existing `rerun-tasks --no-verify-checkpoints` behavior remains unchanged because the auto-invoke is still gated by `not no_verify_checkpoints`.
- Adding `--quiet` is backward-compatible if additive and if `--json` keeps its current behavior.
- Adding `--phase` is potentially backward-compatible syntactically, but semantically risky unless manifest output semantics are defined. A phase-filtered manifest written to `OUTPUT_DIR/manifest.json` could surprise tooling that expects a full-sprint manifest.
- The installed package and source tree currently match on the buggy code path, so fixing source and reinstalling/upgrading the CLI should resolve the observed TUIBBS-scp symptom.

## Uncertainties

- I did not modify `/config/workspace/TUIBBS-scp` or rerun the full `rerun-tasks` command, per instruction.
- The original intent behind `--phase` and `--quiet` is not documented in the inspected source. It may have come from a planned but unfinished phase-scoped/quiet `verify-checkpoints` feature.
- I did not inspect roadmap/TDD documents for `TDD §T9`; if those docs require phase-scoped quiet verification, implement option 3 deliberately rather than only applying the minimal call-site patch.
