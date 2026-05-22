# F-26 Adjudication — `output_path` CWD-relative default

**Source finding**: `.dev/eval-workspaces/prd-cli-audit/findings/F-26-output-path-cwd-default.md`
**Stage 2 preliminary severity**: MEDIUM
**Adjudication mode**: B (reproducibility / blast-radius / severity-calibration)
**Date**: 2026-05-20

## Re-verification

### Code under review
`src/superclaude/cli/prd/config.py:102-117`:

```python
# -- Path resolution --
if output:
    output_path = Path(output).resolve()
else:
    # Default sandbox: .dev/eval-workspaces/ when running from a repo that
    # has one (avoids polluting the repo root with prd-<slug>/ dirs);
    # fall back to CWD only when no sandbox is available.
    sandbox = Path(".dev/eval-workspaces").resolve()
    # Use is_dir() rather than exists() so a stray `.dev` *file* doesn't
    # falsely trigger the sandbox branch (sandbox.mkdir would then fail
    # in a non-obvious way trying to create a child of a file).
    if sandbox.parent.is_dir():  # i.e. .dev/ exists as a dir → we're in a repo
        sandbox.mkdir(parents=True, exist_ok=True)
        output_path = sandbox
    else:
        output_path = Path(".").resolve()
```

### Actual default (verified)
The trigger is **`<cwd>/.dev/` exists as a directory**, not project-root detection.
Result:

| Scenario | `cwd/.dev/` exists? | Resolved `output_path` |
|---|---|---|
| Inside IronClaude repo root | yes | `<cwd>/.dev/eval-workspaces/` |
| User's `$HOME` (typical) | no | `<cwd>` itself (i.e. `$HOME`) |
| `/tmp` | no | `/tmp` |
| Any unrelated project that happens to have `.dev/` | yes | `<that-project>/.dev/eval-workspaces/` |

Verified empirically by running `Path(".dev/eval-workspaces").resolve()` and
`sandbox.parent.is_dir()` from `$HOME` (False) and from a synthetic
`/tmp/x/` directory containing `.dev/` (True; would write to
`/tmp/x/.dev/eval-workspaces/prd-task/`).

The finding's evidence block and trace are accurate. Two clarifications:

1. **The "never asks permission" claim is partly mitigated**:
   `commands.py:123` prints `Output: {config.output_path}` in `--dry-run`
   mode, so the resolved path *is* surfaced — but only if the user opts
   into dry-run. A normal `superclaude prd run "..."` invocation does
   not echo the resolved output_path before executing.
2. **Help text is wrong** (`commands.py:50`): documents
   `default: current directory` while the actual default is the
   sandbox branch whenever `.dev/` is present. This is an independent
   doc/behavior drift not called out in the finding.

---

## Persona analyses

### Analyzer — reproducibility

**Scenario A — user in `$HOME`** (no `.dev/`):
`output_path` becomes `Path(".").resolve()` = `$HOME`. The pipeline
then creates `$HOME/prd-task/` (since no `--product` was given,
`task_dir_name = "prd-task"`; see `config.py:124-125`). Result:
artefacts land directly in the user's home directory. Recoverable
(one `rm -rf $HOME/prd-task/`) but ugly and surprising.

**Scenario B — user in `$HOME` *that contains a `.dev/` dir***
(e.g. a personal dotfiles repo or unrelated SuperClaude clone with a
sibling `.dev/`): `output_path` becomes `$HOME/.dev/eval-workspaces/`,
silently grafting PRD artefacts onto an unrelated tree. This is the
"unrelated project" risk Agent C flagged. Reproducible exactly as the
finding describes — confirmed by simulating the
`sandbox.parent.is_dir()` check.

**Scenario C — user inside a deep subdir of a repo** (e.g.
`<repo>/src/foo/`): `Path(".dev/eval-workspaces").resolve()` resolves
to `<repo>/src/foo/.dev/eval-workspaces`. Its parent
`<repo>/src/foo/.dev` does *not* exist → fallback to CWD. So the
artefacts land in `<repo>/src/foo/prd-task/`, **not** at the repo
root's sandbox. The "running from a repo that has one" comment in the
code is misleading: it only works from the repo root itself, not from
subdirectories of the same repo.

Reproduction is deterministic.

### Refactorer — blast radius

The CWD-relative-default pattern is **systemic** across the CLI, not
isolated to PRD. Survey of CLI sub-packages
(`grep -rn 'Path("\.\|Path("\.dev' src/superclaude/cli/`):

| Module | CWD-relative default | Severity profile |
|---|---|---|
| `cli/prd/config.py:109,117` | `.dev/eval-workspaces/` or `Path(".")` | this finding |
| `cli/prd/models.py:184,186` | dataclass default `Path(".")` for `output_path`, `task_dir` | sentinel — overridden by `resolve_config`; low standalone risk |
| `cli/prd/models.py:54,60,73,79` | `Path.cwd() / ".claude" / ...` and `Path.cwd() / "src" / ...` for skill_refs/template discovery | same CWD coupling — fails silently if invoked from elsewhere |
| `cli/sprint/commands.py:262,267` | `Path(".dev/sprint-state") / ...` | analogous sandbox; same blast radius |
| `cli/sprint/models.py:470` | `Path(".dev/sprint-state") / tasklist_id` | analogous |
| `cli/eval/config.py:67` | `Path(".dev/eval-runs")` | analogous; documented in `cli/eval/config.py:14,189` as intentional |
| `cli/eval/artifact_layout.py:76` | `RUN_DIR_PREFIX = Path(".dev/eval-runs")` | analogous |
| `cli/roadmap/executor.py:1019` | `Path("src/superclaude") if … else Path(".")` | tier-discovery CWD coupling |
| `cli/cleanup_audit/models.py:72,78` | `Path(".")` defaults for `target_path`, `output_dir` | semantically intended (audit the CWD) |
| `cli/tasklist/models.py:22-24` | `Path(".")` defaults | dataclass sentinels |
| `cli/cli_portify/steps/*.py` | `config.workflow_path or Path(".")` | sentinel fallback |

**Pattern**: every sub-pipeline that has a "sandbox" (`prd`, `sprint`,
`eval`) uses the same CWD-relative `.dev/<scope>` convention.
`cli/eval/config.py` documents this explicitly as an AC requirement
("AC12 in the cliEval roadmap"). So PRD is following an existing house
convention, not inventing one.

**Where PRD diverges from the convention**:

1. **`sprint` and `eval` do not silently fall back to CWD itself** when
   `.dev/` is absent — they error out or use an explicit
   `--release-dir` / `--out-dir`. PRD silently falls back to `Path(".")`
   which is the riskier branch (the one that drops `prd-task/` into
   `$HOME`).
2. **`sprint` resolves relative to the *release directory* it was
   given**, not raw CWD; the `.dev/sprint-state` lookup is parameterised
   by a tasklist ID derived from the release. PRD has no equivalent
   anchor.
3. **`cli/eval/config.py:189`** documents a two-tier search
   (`/tmp/eval-runs`, `.dev/eval-runs`) — PRD has no such layering.

**Blast radius assessment**: the CWD-relative default itself is house
convention and arguably acceptable; the *specific* hazard in F-26 is
(a) silent fallback to bare CWD when sandbox is absent and (b) the
"running from a repo that has one" detection being too permissive
(any `.dev/` qualifies). Other CLI commands could replicate the same
mistake but currently don't, because they require an explicit
release/run identifier.

### Architect — severity calibration

**UX impact**:

- **Best case** (user is at repo root with `.dev/`): correct,
  invisible, matches house convention. No harm.
- **Common-but-wrong case** (user from `$HOME` or a subdir): artefacts
  land somewhere unexpected. `prd-task/` (the `task_dir_name` when no
  `--product` is given) is generic enough that the user may not
  recognise it as PRD output later. Discoverable on the next `ls` and
  recoverable with a single `rm -rf`. No data loss to existing files
  (the directory is freshly created).
- **Pathological case** (user in an unrelated project with `.dev/`):
  PRD artefacts pollute that project's `.dev/eval-workspaces/`. Still
  recoverable, still discoverable; the project's own tooling may
  surface the stray directory as drift. Not destructive.

**Recoverability**: all failure modes are pure additive directory
creation. Nothing is overwritten (each pipeline run uses a slug-based
subdir; existing `prd-<slug>/` would be merged into but not deleted).
Recovery is `rm -rf <unexpected-path>/prd-*` with no side effects.

**Discoverability**: dry-run prints the resolved `output_path`
(`commands.py:123`), so a user who runs `--dry-run` first sees the
target. Without dry-run there is no pre-execution surface. The CLI
help text (`commands.py:50`) is actively wrong (`default: current
directory`), which compounds the surprise.

**Aggravators**:

1. Help-text drift makes it harder for the user to predict behaviour.
2. The `.dev/` test is too permissive (any sibling project qualifies).
3. Bare-CWD fallback (the `else` branch) drops artefacts directly in
   `$HOME`/wherever — strictly worse than refusing to default.

**Mitigators**:

1. No data loss; non-destructive.
2. Dry-run does surface the path.
3. Behaviour matches an existing house convention used by `sprint` and
   `eval`; users familiar with those pipelines will recognise it.
4. The user can always pass `--output` to override.

**Calibration**: the preliminary MEDIUM is defensible. This is not
LOW because:

- help text is wrong, breaking user expectations;
- the unrelated-project case (Agent C's concern) is reachable in
  practice (any `.dev/` dir triggers it);
- the bare-CWD fallback can dump artefacts in `$HOME`.

This is not HIGH because:

- non-destructive and recoverable;
- discoverable via dry-run;
- conforms to an existing house convention.

---

## Convergence

| Dimension | Value |
|---|---|
| **Verdict** | Confirmed — the CWD-relative default is real, the bare-CWD fallback is the riskier branch, and help text drift is an independent bug colocated with the same code. |
| **Convergence score** | 0.88 (Analyzer: confirmed reproducible; Refactorer: house convention but PRD diverges in two specific ways; Architect: MEDIUM defensible). |
| **Final severity** | **MEDIUM** (confirmed). |
| **Fix difficulty** | **LOW** — ~15-30 lines in one file. |

### Synthesis

The finding is accurate as written. Three concrete defects coexist at
`src/superclaude/cli/prd/config.py:102-117` and the adjacent help
text:

1. **Permissive sandbox detection** (`config.py:113`): a bare
   `.dev/` directory in CWD is treated as "we're in a repo." This
   triggers in unrelated projects and in any directory the user
   happens to have created `.dev/` in (e.g. dotfiles, scratch dirs).
2. **Bare-CWD fallback** (`config.py:117`): when no sandbox is found
   the default becomes `Path(".").resolve()`, which silently drops
   `prd-task/` into the user's CWD — including `$HOME`. Worse than
   the sandbox case because it has no scoping at all.
3. **Help-text drift** (`commands.py:50`): documents
   `default: current directory`, which is true *only* in the fallback
   branch. The dominant case (any CWD with `.dev/`) goes to the
   sandbox, contradicting the help text.

Subdirectory invocation (`<repo>/src/foo/`) also misbehaves: the
`.dev/` check is purely sibling-of-CWD, not project-root-aware, so
artefacts land inside `src/foo/` instead of the repo's sandbox.

**Recommended remediation** (out of scope for this adjudication, noted
for the eventual fix):

- Either walk upward from CWD to find a `pyproject.toml` /
  `.git/` anchor before declaring "we're in a repo," or require an
  explicit `--output` / config-file value (matching how `sprint` and
  `eval` require explicit release/run identifiers).
- Refuse the bare-CWD fallback. Error out with a usage message
  pointing to `--output` when no sandbox anchor is found.
- Fix `commands.py:50` help text to describe the *actual* resolution
  order.
- Optionally surface `config.output_path` in non-dry-run startup
  output so the user sees where artefacts will land before the
  pipeline begins.

No upstream blast-radius changes are required — `sprint` and `eval`
already use stricter resolution (release/run IDs); PRD just needs to
join them.

---

## Citations

- `src/superclaude/cli/prd/config.py:102-117` — default resolution logic.
- `src/superclaude/cli/prd/config.py:113` — `sandbox.parent.is_dir()` trigger.
- `src/superclaude/cli/prd/config.py:117` — bare-CWD fallback.
- `src/superclaude/cli/prd/config.py:124-125` — `task_dir_name = "prd-task"` when no product.
- `src/superclaude/cli/prd/commands.py:50` — incorrect help text (`default: current directory`).
- `src/superclaude/cli/prd/commands.py:119-125` — dry-run echoes resolved `output_path`.
- `src/superclaude/cli/prd/models.py:184,186` — dataclass sentinel defaults for `output_path`, `task_dir`.
- `src/superclaude/cli/sprint/commands.py:262,267` — analogous `.dev/sprint-state/` pattern (anchored by tasklist ID).
- `src/superclaude/cli/sprint/models.py:470` — sprint state path resolution.
- `src/superclaude/cli/eval/config.py:14,45,67,158,189` — documented two-tier `.dev/eval-runs` convention (cliEval AC12).
- `src/superclaude/cli/eval/artifact_layout.py:76` — `RUN_DIR_PREFIX = Path(".dev/eval-runs")`.
- `src/superclaude/cli/roadmap/executor.py:1019` — `Path("src/superclaude") if … else Path(".")` (analogous CWD coupling).
- `src/superclaude/cli/cleanup_audit/models.py:72,78` — `Path(".")` defaults (semantically intended for "audit CWD").
