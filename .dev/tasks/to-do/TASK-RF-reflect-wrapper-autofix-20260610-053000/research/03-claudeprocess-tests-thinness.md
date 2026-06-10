# R3 — ClaudeProcess launch/env API + reflect test harness + thinness guards

Status: Complete
Researcher: R3
Worktree (read-only): `wrapper-onto-master`
Date: 2026-06-10

All file:line citations below are in worktree
`/config/workspace/IronClaude/.claude/worktrees/wrapper-onto-master/` unless noted.

---

## 1. `ClaudeProcess` launch/env API — and how the wrapper builds a SECOND process to run `/task`

Source: `src/superclaude/cli/pipeline/process.py`.

### 1.1 `__init__` signature (all keyword-only after `*`)

`process.py:37-68`:

| Param | Default | Notes |
|---|---|---|
| `prompt: str` | (required) | delivered via **stdin** in `start()`, not as argv (`process.py:73-78,136-146`) — bypasses 128 KB MAX_ARG_STRLEN |
| `output_file: Path` | (required) | stdout sink (opened `"w"`, `process.py:120-122`) |
| `error_file: Path` | (required) | stderr sink (`process.py:123`) |
| `max_turns: int` | `100` | → `--max-turns` (`process.py:86-88`). **Primitive default is 100; the reflect wrapper overrides to 250** — see §1.4 |
| `model: str` | `""` | → `--model <M>` ONLY when truthy (`process.py:92-93`) |
| `permission_flag: str` | `"--dangerously-skip-permissions"` | `process.py:83` |
| `timeout_seconds: int` | `6300` | used by `wait()` (`process.py:162`); **reflect overrides to 3600** via `config._DEFAULT_TIMEOUT_SECONDS` (`config.py:31`) |
| `output_format: str` | `"stream-json"` | → `--output-format` (`process.py:89-90`) |
| `extra_args: list[str] \| None` | `None` → `[]` | appended after `--output-format` and after `--model` (`process.py:63,94`) |
| `on_spawn / on_signal / on_exit` | `None` | lifecycle hooks (`process.py:49-51,64-66`) |
| `env_vars: dict[str,str] \| None` | `None` | stored as `self._extra_env_vars` (`process.py:52,67`); merged in `build_env()` — **this is the marker-injection vector** |
| `tool_write_mode: bool` | `False` | when True, stdout→`.log`, output_file must be written by the child via the Write tool (`process.py:118-122,216-236`) |

### 1.2 `build_env()` behavior — what it preserves / pops

`process.py:97-112`:

```python
env = os.environ.copy()
env.pop("CLAUDECODE", None)
env.pop("CLAUDE_CODE_ENTRYPOINT", None)
if env_vars:
    env.update(env_vars)
return env
```

- **Starts from a full `os.environ.copy()`** — so HOME, MCP config, and all
  `ANTHROPIC_DEFAULT_*_MODEL` aliases are **preserved** into the child.
- **Pops exactly two keys**: `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT` — to
  defeat nested-session detection in the child `claude`.
- `env_vars` (if provided) are merged with **override semantics AFTER the copy**
  (`process.py:110-111`). So a caller-supplied key wins over the inherited env.
- `build_env()` accepts a per-call `env_vars=` kwarg (`process.py:97`), but on the
  real launch path `start()` calls `self.build_env(env_vars=self._extra_env_vars)`
  (`process.py:129`) — i.e. it uses the **constructor's** `env_vars`. The runner's
  `_child_env()` probe calls `build_env()` with no args (`runner.py:241`), so the
  probe overlay is the bare real-env (no marker).

**Confirmed marker behavior today:** the marker
`SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` does NOT exist anywhere in `src/` or `tests/`
(grep, 0 hits). `build_env()` does not set, preserve specially, or pop it — it would
flow through the `os.environ.copy()` if already set in the parent env, but the
wrapper never injects it yet. **The marker injection + self-suppress guard are NET
NEW.**

### 1.3 `build_command()` flag order (load-bearing — tests byte-match it)

`process.py:73-95` produces exactly:

```
claude --print --verbose <permission_flag> --no-session-persistence
       --tools default --max-turns <N> --output-format <fmt>
       [--model <M>] [*extra_args]
```

Key ordering invariants asserted by tests (see §3):
- `--max-turns` **precedes** `--output-format` (`process.py:86-90`).
- `--model` is appended **only when truthy**, AFTER `--output-format`
  (`process.py:92-93`).
- The prompt is NOT in argv — it is written to stdin in `start()` (`process.py:140-146`).

### 1.4 How the CURRENT runner constructs its (single) ClaudeProcess

`runner.py:459-470` — the audit launch:

```python
proc = ClaudeProcess(
    prompt=prompt,                                   # "/sc:reflect --mode post ..."
    output_file=config.output_dir / "reflect-stdout.json",
    error_file=config.output_dir / "reflect-stderr.log",
    model=config.model,
    timeout_seconds=config.timeout_seconds,
    max_turns=config.max_turns,    # G1: explicit 250, never the primitive's 100
    output_format="stream-json",
    env_vars=None,                 # FR-10: bare real-env overlay (no custom scrub)
)
proc.start()
rc = proc.wait()
```

Note `env_vars=None` TODAY. The auto-fix evolution must change this to inject the
marker (see §1.5).

### 1.5 RECOMMENDED: how the wrapper builds a SECOND ClaudeProcess to run `/task <path>`

The contract (FR-1/FR-2, `merged-requirements.md:87-106`, `reflect-wrapper-contract.md:76-108`)
requires the apply step to run `/task <remediation_task_path>` as **another
top-level `claude --print` subprocess** with the marker exported. The exact-fit
construction, reusing the existing primitive with zero new launch surface:

```python
MARKER = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"

apply_proc = ClaudeProcess(
    prompt=f"/task {remediation_task_path}",
    output_file=config.output_dir / f"fix-{iteration}-stdout.json",
    error_file=config.output_dir / f"fix-{iteration}-stderr.log",
    model=config.model,
    timeout_seconds=config.timeout_seconds,
    max_turns=config.max_turns,
    output_format="stream-json",
    env_vars={MARKER: "1"},        # <-- the only delta vs the audit launch
)
apply_proc.start()
apply_rc = apply_proc.wait()
```

**Why `env_vars={MARKER: "1"}` is exactly right:** `build_env()` does
`os.environ.copy()` then `env.update(env_vars)` (`process.py:107-111`), so the
marker is overlaid on top of the full inherited env without scrubbing anything
else. The `/task` child therefore sees the marker AND inherits the
`ANTHROPIC_DEFAULT_*` aliases. When that `/task` reaches its own terminal reflect
gate (`superclaude reflect run`), the **self-suppress guard** (§4.1) sees the
marker and exits 0 — breaking recursion.

**Two design notes for the tasklist:**
1. The contract (`reflect-wrapper-contract.md:88-92`) says the marker is exported
   into the env of *every child the wrapper spawns inside the fix subtree* — both
   the audit AND the `/task`. So once the wrapper itself runs under `--fix`, the
   **re-verify audit launches** should arguably also carry the marker. BUT the
   marker also triggers the wrapper's own self-suppress — meaning the OUTER wrapper
   must read the marker from `os.environ` at its OWN startup, NOT from a value it
   injected into children. The injection target is the child env (`env_vars=`); the
   self-suppress read is `os.environ.get(MARKER)`. These are distinct surfaces and
   must not be conflated. (Verified: today the wrapper reads no env marker at all;
   the self-suppress is net new — see §4.1.)
2. The current `_child_env()` probe (`runner.py:236-241`) builds a throwaway
   `ClaudeProcess(prompt="", output_file=devnull, error_file=devnull)` and calls
   `build_env()` with NO args to count `ANTHROPIC_DEFAULT_*` aliases. That probe
   must NOT count the marker as an alias (it doesn't — marker isn't in
   `_MODEL_ALIAS_ENV_VARS`, `runner.py:37-41`). Safe.

---

## 2. Exact contents/structure of `tests/cli/reflect/`

Directory listing (`tests/cli/reflect/`): `conftest.py`, `__init__.py`,
`test_cli_smoke.py`, `test_no_nesting_guard.py`, `test_runner_e2e.py`,
`test_verdict_mapping.py`, `test_writeback.py`, plus `fixtures/`.

### 2.1 `conftest.py` — the shared harness (`conftest.py:1-139`)

- `FIXTURES_DIR` constant (`conftest.py:17`).
- `_FAKE_BASE` / `_FAKE_HEAD` 40-char SHAs (`conftest.py:20-21`).
- `_TASKLIST_TEMPLATE` (`conftest.py:23-37`): frontmatter with `id`, `title`,
  `status`, `start_commit: {base}`, `spec_path: ""`, `reflect_post: ""` + a 2-line body.
- **`cli_runner`** fixture (`conftest.py:40-43`): a fresh Click `CliRunner`.
- **`temp_tasklist`** fixture (`conftest.py:46-55`): writes the template into
  `tmp_path` and returns the path. Carries `start_commit` so `<BASE>` resolves
  without git.
- **`patch_git`** fixture (`conftest.py:58-80`): monkeypatches
  `config._git` so `rev-parse HEAD` → `_FAKE_HEAD` and `merge-base` → `_FAKE_BASE`;
  returns a `_Git` holder exposing `.base` / `.head`. **This is how `--base`
  precedence tests will need to be wired** (the new tests must extend or parametrize
  this).
- **`patch_runner_env`** fixture (`conftest.py:83-95`): monkeypatches
  `runner._child_env` → `lambda: {}` (so the alias-count probe does NOT construct a
  throwaway `ClaudeProcess`, keeping the patched-`ClaudeProcess` call count equal to
  REAL launches), and `runner.shutil.which` → `/usr/bin/claude` so the
  `claude`-binary preflight passes. **Critical for thinness/loop tests: the
  `mock_cls.call_count` reflects exactly the real audit + apply launches.**
- **`make_claude_process_stub`** fixture (`conftest.py:98-138`): the **Idiom-B**
  factory builder. `_builder(fixture_name, rc=0, write_contract=True)` returns a
  `factory(**kwargs)` that:
  - reads `output_file` from kwargs, derives `output_dir = output_file.parent`,
  - returns a `MagicMock` whose `.start()` is a no-op and whose `.wait()` side
    effect **writes the chosen fixture YAML into
    `<output_dir>/return-contract.yaml`** then returns `rc`
    (`conftest.py:121-136`).
  - `fixture_name=None` or `write_contract=False` simulates a run that writes NO
    contract → verdict routes `blocked`.
  - The contract is written from inside `.wait()` (not `.start()`) so it appears
    only after the "subprocess" completes — matching real launch ordering.

**Idiom-B usage pattern** (`conftest.py:103-105`, used throughout
`test_runner_e2e.py`):
```python
factory = make_claude_process_stub("pass.yaml", rc=0)
with patch("superclaude.cli.reflect.runner.ClaudeProcess", side_effect=factory) as mock_cls:
    result = ReflectRunner(config).run()
```
Patch target string is `superclaude.cli.reflect.runner.ClaudeProcess`
(`test_runner_e2e.py:22` `_PATCH_TARGET`).

### 2.2 `fixtures/` — contract YAMLs

`tests/cli/reflect/fixtures/`: `__init__.py`, `pass.yaml`,
`halted_regression.yaml`, `degraded_serena.yaml`, `degraded_single_vendor.yaml`,
`degraded_tier1.yaml`, `blocked_unknown_major.yaml`, `tolerant_unknown_field.yaml`.

- `pass.yaml` (`fixtures/pass.yaml:1-28`): `contract_version: "1.3.0"`, `status:
  success`, `tier_reached: 2`, all `deviation_count_by_class` zero, all
  load-bearing booleans `false`, `degraded_components: []`.
- `halted_regression.yaml` (`fixtures/halted_regression.yaml:1-28`): `status:
  partial`, `deviation_count_by_class.regression: 1`, `regression_present: true`.

**GAP for the tasklist:** every fixture is `contract_version: "1.3.0"` and **none
contains `remediation_task_path`**. The auto-fix work needs NEW fixtures:
  - an **AUTO-FIXABLE** drift-only contract (`status: partial`,
    `deviation_count_by_class.drift > 0`, all human-required booleans `false`,
    empty grounding-gaps) **with `remediation_task_path: <abs>`** at `1.4.0`;
  - the same drift-only shape **with `remediation_task_path: null`** (cannot-repair → HALT);
  - a **HUMAN-REQUIRED** contract (e.g. `needs_human_decision: true` and/or
    non-empty grounding-gaps) at `1.4.0`;
  - a post-fix **PASS** contract (for the convergence re-audit) at `1.4.0`.

### 2.3 `test_cli_smoke.py` — CLI surface (`test_cli_smoke.py:1-125`)

- Imports `reflect_group` from `superclaude.cli.reflect.commands` (`:13`).
- `_SPEC9_FLAGS` list (`:15-26`) — the EXACT help-flag whitelist; `--fix`,
  `--no-fix`, `--max-fix-iterations`, `--base` must be ADDED here when the help test
  is extended (else the new flags are untested and the spec-9 list drifts).
- `test_group_help_shows_run` / `test_run_help_shows_all_spec9_flags` (`:29-39`).
- `test_dry_run_never_launches` (`:42-49`) and
  `test_print_command_prints_and_never_launches` (`:52-63`): patch
  `runner.ClaudeProcess` as a plain `MagicMock` and `assert_not_called()` — the
  FR-12 no-launch guarantee.
- `test_print_command_argv_preview_matches_build_command` (`:72-97`): byte-matches
  the argv preview to `build_command()` order (`--max-turns` before
  `--output-format stream-json`).
- `test_config_stop_writes_blocked_sidecar` (`:100-124`): patches
  `config.resolve_config` to raise `ValueError`, asserts exit 2 + a
  `wrapper-result.yaml` sidecar with `verdict: blocked`.

### 2.4 `test_runner_e2e.py` — mocked end-to-end (`test_runner_e2e.py:1-221`)

- `_config(tasklist, **overrides)` helper (`:33-37`): calls real
  `resolve_config(str(tasklist), depth="standard", model="test-model", **overrides)`.
- `_read_reflect_post(path)` (`:26-31`): reads back the written `reflect_post`
  block for assertions.
- Verdict-matrix e2e: `test_e2e_pass` / `_halted` / `_degraded` /
  `_blocked_no_contract` / `_blocked_timeout` (rc=124) / `_blocked_child_crash`
  (rc=1) (`:39-114`). Each uses the Idiom-B factory + `mock_cls.assert_called_once()`.
- `test_e2e_pass` also asserts **`mock_cls.call_args.kwargs["max_turns"] ==
  config.max_turns == 250`** (`:50`) — the G1 max-turns-threading probe. **The
  apply-launch tests will assert `mock_cls.call_args_list[k].kwargs["env_vars"]`
  contains the marker, by direct analogy.**
- `test_e2e_resume_clean_head_skips_launch` (`:142-155`): `mock_cls.assert_not_called()`
  — the resume short-circuit, the existing precedent for **the marker
  self-suppress test shape** (assert exit 0 + `ClaudeProcess` never constructed).
- `test_e2e_resume_stale_head_launches` (`:158-172`): `assert_called_once()`.
- `test_e2e_frontmatter_stale_downgrades_pass_to_blocked` /
  `_missing_...` (`:175-221`): patch
  `runner.write_reflect_post` → `"frontmatter-stale"`/`"frontmatter-missing"`,
  assert PASS downgrades to BLOCKED/exit 2.

### 2.5 `test_verdict_mapping.py` — pure `derive_verdict` unit tests (`:1-277`)

Calls `contract.derive_verdict(contract_dict, expected_tier=2,
allow_single_vendor=..., child_rc=...)` directly against loaded fixtures. Covers
the first-match-wins ordering blocked→degraded→halted→pass and the F0/F2/F5
hardening. **The AUTO-FIXABLE-vs-HUMAN-REQUIRED classifier (FR-4), if implemented
as a pure function in `contract.py`, should get its unit tests here** in the same
direct-call style (no subprocess, no CliRunner).

### 2.6 `test_writeback.py` — FR-6 write-back + FR-7 sidecar (`:1-173`)

Direct calls to `runner.write_reflect_post` / `runner.write_sidecar`. Covers
body-byte preservation, the compare-mismatch stale path, and the CRLF round-trip.
**The sidecar `fix_iterations` / `fix_converged` fields (FR-3) extend
`write_sidecar` and need new assertions here.**

---

## 3. Thinness-guard test pattern — PRESENT (`test_no_nesting_guard.py`)

`test_no_nesting_guard.py:1-59` is the existing thinness/isolation guard. It has
TWO layers:

- **Layer A** (`:40-49`): reads the **task-builder SKILL SOURCE**
  (`src/superclaude/skills/task-builder/SKILL.md`, `:17`) and asserts the Mode-2
  wrapper block (a) contains `superclaude reflect run` + `--depth` (Bash shell-out)
  and (b) contains NO nesting tokens `("Task(", "subagent_type")` (`:23`).
- **Layer B** (`:52-59`): reads `runner.py` source (`:18`) and asserts
  `"ClaudeProcess" in src` AND none of
  `("import anthropic", "from anthropic", "subagent", "Task(")` appear.

**What is ASSERTED today vs. what the contract requires:**

| Thinness invariant (NFR-1, `merged-requirements.md:26-29,216-217`) | Asserted today? | Where |
|---|---|---|
| `runner.py` launches reflect only via `ClaudeProcess` (no agent surface) | YES | `test_no_nesting_guard.py:52-59` |
| task-builder SKILL Mode-2 block is a Bash shell-out, no `Task(`/`subagent_type` | YES | `:40-49` |
| **NO `cli.sprint` / `cli.roadmap` import** | **NO explicit test** | only in-source docstrings (`runner.py:9`, `config.py:8`, `models.py:9`) + `process.py:9` NFR-007 note |
| **NO `async` / `await`** | **NO explicit test** | only docstrings |
| only `ClaudeProcess` launch (no `subprocess.Popen` direct, etc.) | partial (Layer B is a source-string grep) | `:52-59` |

**Tasklist must ADD thinness assertions** (a grep over the package confirms the
properties HOLD in source today, but they are not pinned by a test):
1. A test asserting NO `cli.sprint` / `cli.roadmap` import across the reflect
   package — e.g. read each `cli/reflect/*.py` source and assert
   `"cli.sprint"`/`"cli.roadmap"` / `"from superclaude.cli.sprint"` /
   `"from superclaude.cli.roadmap"` absent (Layer-B grep style). Or, stronger, walk
   `sys.modules` after `import superclaude.cli.reflect.*` and assert neither sprint
   nor roadmap module is loaded.
2. A test asserting NO `async`/`await` — grep `r"\basync\s+def\b"` / `r"\bawait\b"`
   absent in each `cli/reflect/*.py`. (Be careful to exclude the docstring lines
   that literally contain the words "async def" — the existing files mention them in
   prose at `runner.py:10`, `config.py:9`, `models.py:10`. A regex anchored on
   `^\s*async def` / `^\s*await ` avoids the docstring false-positives.)
3. Extend Layer B's banned-token set to cover the new `/task` apply launch — assert
   the apply path ALSO goes through `ClaudeProcess` and not a raw `subprocess.run`
   / `Popen` (the contract's "only subprocess-launch path is `ClaudeProcess`",
   `merged-requirements.md:29`). Note the existing `commands.py` legitimately uses
   `subprocess.run` for the `--tmux` mechanic (`commands.py:267-274`), so a blanket
   "no subprocess" grep over the whole package would FALSE-POSITIVE — scope the new
   guard to `runner.py` (the fix-loop module), per Layer B's existing precedent.

---

## 4. Test design recommendations (evidence-based, from observed patterns)

All recommendations mirror existing precedents so the new tests slot into the
established harness.

### 4.1 Marker self-suppression (exit 0)

- **Mechanism location:** net-new guard at command entry in `commands.py` `run()`
  (before `resolve_config`, before any `ClaudeProcess`). Read
  `os.environ.get("SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE")`; if `== "1"`, emit a
  one-line notice and `sys.exit(0)`. (Truthy value is EXACTLY `"1"` per
  `reflect-wrapper-contract.md:107` — absent/empty/other ⇒ normal run.)
- **Test shape (precedent: `test_e2e_resume_clean_head_skips_launch`,
  `test_runner_e2e.py:142-155`, and `test_dry_run_never_launches`,
  `test_cli_smoke.py:42-49`):**
  - Use `cli_runner.invoke(reflect_group, ["run", str(temp_tasklist)])` with
    `monkeypatch.setenv("SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE", "1")`.
  - Patch `runner.ClaudeProcess` as a `MagicMock`; assert `result.exit_code == 0`
    AND `mock_cls.assert_not_called()`.
  - **Negative control** (mirror `test_e2e_resume_stale_head_launches`): set the
    marker to `"0"` (and to absent, and to `"2"`) and assert a normal run proceeds
    (NOT suppressed) — guards against a too-loose truthiness check, exactly the F2
    "malformed truthy" failure class the codebase already defends
    (`test_verdict_mapping.py:228-260`).
  - Decide and TEST whether suppression fires BEFORE the Click `exists=True`
    tasklist guard (`commands.py:58-61`). Recommendation: suppress first so a
    nested gate on a since-moved file still exits 0 cleanly (the contract says
    "immediately exits 0 ... before any audit", `reflect-wrapper-contract.md:88`).
    Note: a Click `exists=True` argument is validated during parsing, BEFORE the
    `run()` body executes — so an in-`run()` guard CANNOT pre-empt it. If
    suppress-before-exists-guard is required, the marker check must move to a
    group-level `callback`/`invoke_without_command` or an eager option callback.
    Flag this as an open implementation question for the tasklist.

### 4.2 AUTO-FIXABLE vs HUMAN-REQUIRED carve-out routing

- **Mechanism location:** a PURE classifier in `contract.py` (the spec's chosen
  surface, `merged-requirements.md:271-272`), reading ONLY existing fields. Test it
  in `test_verdict_mapping.py` style — direct function calls, no subprocess.
- **AUTO-FIXABLE predicate** (`merged-requirements.md:114-118`,
  `reflect-wrapper-contract.md:118-121`): HALTED caused solely by `drift>0` and/or
  `necessary`-class items AND NOT (`regression_present` /
  `deviation_count_by_class.regression>0` / `needs_human_decision` /
  `user_decision_required` / `unauthorized_deviation_present` / non-empty
  grounding-gaps / degraded / blocked).
- **Test matrix (one row per existing HALT/HUMAN trigger in `_halted_reason`,
  `contract.py:304-325`):**
  - drift-only (`drift>0`, all booleans false) → AUTO-FIXABLE.
  - necessary-only → AUTO-FIXABLE (per spec).
  - `regression_present: true` → HUMAN-REQUIRED (terminal HALT).
  - `deviation_count_by_class.regression > 0` → HUMAN-REQUIRED.
  - `needs_human_decision: true` → HUMAN-REQUIRED.
  - `user_decision_required: true` → HUMAN-REQUIRED.
  - `unauthorized_deviation_present: true` → HUMAN-REQUIRED.
  - drift>0 BUT also regression>0 → HUMAN-REQUIRED (mixed → human wins; the
    carve-out is "solely drift/necessary").
  - **Reuse F2's malformed-boolean defense:** a truthy-but-not-bool
    `needs_human_decision` ("true"/1) already routes BLOCKED upstream
    (`contract.py:194-206`, `test_verdict_mapping.py:228-260`) — so the classifier
    only ever sees real bools / absent. Add an explicit test that the classifier is
    NOT reached for a malformed contract (it's BLOCKED before HALT classification).

### 4.3 Bounded fix-loop non-convergence → exit 10

- **Test shape (precedent: the verdict-matrix e2e tests, but with a
  `side_effect` LIST so successive `.wait()` calls return different fixtures):**
  The Idiom-B `factory(**kwargs)` returns a fresh `MagicMock` per construction
  (`conftest.py:121-135`), and `runner.ClaudeProcess` is patched with
  `side_effect=<factory>`. For a multi-launch loop test, supply a factory whose
  successive invocations write DIFFERENT contracts — e.g. extend
  `make_claude_process_stub` to accept a *sequence* of `(fixture, rc)` and pop one
  per construction. Then:
  - With `--max-fix-iterations 2` and a contract that stays AUTO-FIXABLE-HALTED for
    every re-audit (never converges), assert: final `result.verdict is
    Verdict.HALTED`, `exit_code == 10`, and the sidecar records
    `fix_iterations == 2`, `fix_converged is False`
    (`merged-requirements.md:110-111`).
  - Assert the construction count: `(N+1)` audit launches + `N` `/task` applies
    (`reflect-wrapper-contract.md:181-183`) — i.e. for N=2,
    `mock_cls.call_count == 5`. The `patch_runner_env` fixture
    (`conftest.py:83-95`) keeps the count equal to REAL launches (no throwaway probe).
  - Convergence-on-iteration-1 companion: audit#1 AUTO-FIXABLE-HALTED, apply, audit#2
    PASS → exit 0, `fix_converged is True`, `fix_iterations == 1`,
    `mock_cls.call_count == 3`.
  - **`remediation_task_path` absent** on an AUTO-FIXABLE verdict → terminal HALT
    exit 10, NO `/task` launched (`merged-requirements.md:182-184`):
    `mock_cls.call_count == 1`.

### 4.4 O1 promote vs O2 `--no-promote`

- The promote flag is plumbed today: `commands.py:70-75` (`--promote/--no-promote`,
  default flips to True per FR-5), threaded via `resolve_config(promote=...)`
  (`commands.py:138`, `config.py:121,206→ReflectConfig.promote`), and the prompt
  drops `--no-promote` only when `config.promote` (`runner.py:335-337`).
- **Test shape (precedent: `test_print_command_...`, asserting prompt content):**
  - O1: invoke with `--promote` (or default), assert the built prompt
    (`runner._build_prompt`, `runner.py:331-352`) does NOT contain `--no-promote`.
  - O2: invoke with `--no-promote`, assert the prompt DOES contain `--no-promote`.
  - The actual `task`-adapter promotion is reflect-internal (Wave 7) and not
    re-implemented in the wrapper (SoT stays in `sc-reflect-protocol`,
    `reflect-wrapper-contract.md:142-153`), so the wrapper test asserts the FLAG
    PLUMBING + sidecar `promote` state, not a directory move.
  - **GAP:** today's default is `default=False` (`commands.py:74`). FR-5 requires
    flipping to `default=True`. Add a test asserting the bare `run <file>` (no
    promote flag) yields a promote-on prompt. Also test that O2's forced
    `--no-promote` (the generator emits it explicitly) is honored.

### 4.5 `--base` precedence

- **Mechanism:** extend `_resolve_base` (`config.py:81-93`) to honor an explicit
  `--base` ABOVE frontmatter `start_commit` ABOVE `git merge-base HEAD master`
  (`merged-requirements.md:135-139`, FR-6). Add `--base` to `commands.py` options
  and a `base_override` param to `resolve_config`.
- **Test shape (precedent: `patch_git` fixture + `_config` helper):**
  - With `temp_tasklist` (frontmatter `start_commit=_FAKE_BASE`) and `patch_git`
    active, call `resolve_config(..., base_override="<explicit-sha>")` and assert
    `config.base == "<explicit-sha>"` (explicit beats frontmatter).
  - Omit `--base`: assert `config.base == _FAKE_BASE` (frontmatter wins over merge-base).
  - Omit `--base` AND strip frontmatter `start_commit`: assert `config.base ==
    _FAKE_BASE` via the `merge-base` branch of `patch_git` (`conftest.py:70-72`).
  - **De-range invariant (FR-6, `merged-requirements.md:137-139`):** assert the
    built prompt uses `--diff <BASE>` as a SINGLE ref, never `<BASE>..HEAD`
    (`runner.py:344` already does `parts += ["--diff", config.base]`). A regex
    assert that `".." not in` the `--diff` argument guards against a range-form
    regression.

---

## 5. `pipx install --force` exposure + `reflect_group` registration in `main.py`

- **Registration** (`src/superclaude/cli/main.py:440-442`):
  ```python
  from superclaude.cli.reflect.commands import reflect_group  # noqa: E402,I001 ...
  main.add_command(reflect_group, name="reflect")
  ```
  This sits at the BOTTOM of `main.py` (after `eval`, `swarm`, `recommend`,
  `init-lite` — `main.py:426-442`), in the **deferred-import block**. The comment
  `# intentional: deferred subcommand registration to avoid circular imports`
  (`main.py:440`) confirms the import is at module-load time but placed late to
  dodge circular imports.

- **Import-time cost / lazy pattern (CONFIRMED LAZY at the heavy level):**
  Importing `reflect.commands` is cheap — `commands.py` only imports stdlib +
  `click` at module level (`commands.py:15-24`). The HEAVY imports (`config`,
  `runner`, and transitively `pipeline.process`/`ClaudeProcess`) are deferred to
  INSIDE the `run()` command body: `from .config import resolve_config` / `from
  .runner import ReflectRunner` at `commands.py:126-127`. The docstring states the
  house convention explicitly: "Heavy imports (config/runner) are lazy inside the
  command body" (`commands.py:5-6`). So `superclaude --help` / `superclaude reflect
  --help` do NOT pull in `ClaudeProcess`. **The new `--fix` loop logic must keep
  its heavy bits behind the same lazy boundary** (inside `run()` / inside `runner`,
  not at `commands.py` module scope) to preserve this.

- **`pipx install --force` vector** (per memory `reference_superclaude_install_vector`;
  the pyproject entry point was not re-confirmed in this worktree — out of R3
  scope; marked **Unverified** for the pyproject specifics): the operator install is
  `pipx install --force <src-dir>`, which re-installs the `superclaude` console
  entry point. Because `reflect_group` is registered in `main.py` (the `superclaude`
  entry point's module), a `pipx install --force` rebuild exposes `superclaude
  reflect run` on PATH. NFR-5 (`merged-requirements.md:226-228`,
  `reflect-wrapper-contract.md:26-29`) is satisfied by this existing registration —
  the wrapper command ALREADY exists and is registered; the auto-fix evolution adds
  flags/logic to it, it does not add a new command. **Caveat for the tasklist:** the
  generator worktree's gates must not go live until the EVOLVED wrapper (with
  `--fix`/`--base`/`--max-fix-iterations`) is merged and `pipx install --force`-ed,
  else generated tasklists emit flags the installed wrapper rejects
  (`reflect-wrapper-contract.md:26-29`).

---

## Summary (for the parent / tasklist author)

- **`ClaudeProcess` is launch-ready for the second `/task` subprocess with ONE
  delta:** pass `env_vars={"SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE": "1"}`. `build_env()`
  (`process.py:97-112`) does `os.environ.copy()` → pop `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT`
  → `update(env_vars)`, so the marker overlays the full inherited env (aliases
  preserved). The current audit launch passes `env_vars=None` (`runner.py:467`).
- **The marker does NOT exist anywhere yet** (0 grep hits in `src/`+`tests/`). Both
  the child-env INJECTION (`env_vars=`) and the wrapper-startup SELF-SUPPRESS read
  (`os.environ.get(...)` at command entry) are NET NEW and are distinct surfaces —
  do not conflate. Note Click's `exists=True` arg-validation runs before the `run()`
  body, so a suppress-before-exists guard needs a group/eager-callback placement.
- **Test harness is mature and reusable:** `conftest.py` Idiom-B
  `make_claude_process_stub` + `patch_git` + `patch_runner_env` cover launch,
  contract-write, git, and call-count fidelity. New work mostly = new fixtures
  (`1.4.0` + `remediation_task_path`, AUTO-FIXABLE/HUMAN-REQUIRED/post-fix-PASS
  shapes) + a multi-launch `side_effect`-sequence extension to the stub factory.
- **Thinness guards: PARTIALLY present.** `test_no_nesting_guard.py` pins
  "`runner.py` launches via `ClaudeProcess`, no agent tokens" and the task-builder
  SKILL Bash shell-out. **MISSING and must be ADDED:** explicit "no
  `cli.sprint`/`cli.roadmap` import" and "no `async`/`await`" assertions (anchor
  regexes to avoid the docstring false-positives at `runner.py:10` etc.), and an
  extension of the apply-launch-only-via-`ClaudeProcess` guard scoped to
  `runner.py` (NOT a package-wide subprocess grep — `commands.py:267-274` uses
  `subprocess.run` for `--tmux`).
- **Registration is done + lazy:** `main.py:440-442` registers `reflect_group`;
  heavy imports (`config`/`runner`/`ClaudeProcess`) are deferred into the `run()`
  body (`commands.py:126-127`). Keep new fix-loop heavy logic behind that boundary.
