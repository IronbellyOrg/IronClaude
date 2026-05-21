# F-14 Adjudication — `output_path` file-vs-directory pun

**Mode**: B (three personas, focused validation)
**Inputs read**:
- `.dev/eval-workspaces/prd-cli-audit/findings/F-14-output-path-file-dir-pun.md`
- `src/superclaude/cli/prd/config.py:46-144`
- `src/superclaude/cli/prd/commands.py:46-51`
- `src/superclaude/cli/prd/models.py:170-209`
- `src/superclaude/cli/prd/prompts.py:914-1024, 1079-1119`
- `src/superclaude/cli/prd/executor.py:363` (`create_task_dirs(self._config.task_dir)`)
- `src/superclaude/cli/prd/inventory.py:193-199` (`create_task_dirs` body)
- `src/superclaude/cli/roadmap/commands.py:44-50` (sibling `--output` flag)

## Re-verification (read-only)

### R1. How does `resolve_config` treat `--output`?
`src/superclaude/cli/prd/config.py:102-117`:
```python
if output:
    output_path = Path(output).resolve()        # no is_file/is_dir/suffix check
else:
    sandbox = Path(".dev/eval-workspaces").resolve()
    if sandbox.parent.is_dir():
        sandbox.mkdir(parents=True, exist_ok=True)
        output_path = sandbox                   # always a directory
    else:
        output_path = Path(".").resolve()       # always a directory (cwd)
```
The default branch *always* produces a directory. The user-supplied branch is **type-blind** — any string is `Path.resolve()`-d as-is.

Then `config.py:123-125`:
```python
task_dir_name = f"prd-{product_slug}" if product_slug else "prd-task"
task_dir = output_path / task_dir_name
```
The writer **unconditionally treats `output_path` as a parent directory**.

### R2. How do prompts present `output_path` to the LLM?
- `prompts.py:919` (assembly step): `Output path: {config.output_path}`
- `prompts.py:986` (structural-QA): `Report path: {config.output_path}`
- `prompts.py:1042` (qualitative-QA): `Report path: {config.output_path}`
- `prompts.py:1093` (completion step): `Final PRD: {config.output_path}`

All four sites label the value with file-noun semantics ("Output path", "Report path", "Final PRD") and the assembly prompt at lines 924-927 then commands the LLM to "Create the output file with PRD frontmatter" at that path. The LLM is told to write a single PRD file *at* `output_path`.

### R3. CLI help text
`src/superclaude/cli/prd/commands.py:46-51`:
```python
@click.option(
    "--output", "-o",
    default=None,
    help="Output path for final PRD (default: current directory).",
)
```
"Output path for final PRD" reads file-ish; "default: current directory" is directory-ish. The help text itself is internally ambiguous. The docstring in `config.py:65-68` is directory-leaning ("defaults to `<cwd>/.dev/eval-workspaces/`").

### R4. What happens on `--output /tmp/prd.md`?
Walk-through:
1. `resolve_config` → `output_path = Path("/tmp/prd.md").resolve()` (no type check). `config.py:104`.
2. `task_dir = Path("/tmp/prd.md") / "prd-foo"`. `config.py:125`.
3. `executor.py:363` → `create_task_dirs(task_dir)` → `inventory.py:198-199`:
   `(task_dir / subdir).mkdir(parents=True, exist_ok=True)` for each of
   `research/`, `synthesis/`, `qa/`, `reviews/`, `results/`.
4. Because `parents=True, exist_ok=True`, `mkdir` happily creates `/tmp/prd.md/` **as a directory**, then `prd-foo/research/` inside it. No `FileExistsError` is raised against the suffix.
5. Prompts then tell the LLM: "Output path: /tmp/prd.md … Create the output file with PRD frontmatter" (prompts.py:919-927). The LLM will attempt to write to `/tmp/prd.md`, which now resolves to a directory — `Write`/`Edit` against a directory will fail at the tool layer, *or* the LLM will improvise a different filename inside it (e.g. `/tmp/prd.md/PRD.md`), silently diverging from the user's stated path.

The wrong interpretation **succeeds at the OS layer** (mkdir does not fail on a `.md`-suffixed name) and **fails opaquely later** inside the LLM step. Both failure modes are possible; the first (LLM picks a different file) is the most likely and the most damaging because the user never sees their `prd.md` materialize.

---

## Persona analyses

### Analyzer — Reproducibility

**Scenario**: User runs `superclaude prd run "weather app" --output ./mydoc.md --product weather`.

**Observed sequence**:
1. `resolve_config` returns `PrdConfig(output_path=/abs/cwd/mydoc.md, task_dir=/abs/cwd/mydoc.md/prd-weather, ...)`.
2. Executor calls `create_task_dirs(task_dir)` → `mkdir -p /abs/cwd/mydoc.md/prd-weather/{research,synthesis,qa,reviews,results}`. **A directory literally named `mydoc.md` is created in cwd.** No error, no warning.
3. Prompts to subagents now contain `Output path: /abs/cwd/mydoc.md` and `Final PRD: /abs/cwd/mydoc.md`. The assembly prompt (prompts.py:924) instructs: "FIRST ACTION: Create the output file with PRD frontmatter".
4. The LLM either (a) errors when calling `Write` against a directory, or (b) silently writes `mydoc.md/<something>.md` or `mydoc.md/PRD.md`. Either way the file `./mydoc.md` the user expected does not appear.

**Verdict**: Reproducible from the code. The dry-run note in the finding (`commands.py` prints the resolved `output_path`) is the only user-visible signal, and a `.md`-suffixed directory path is not flagged as anomalous.

### Refactorer — Blast radius

**Other path-shaped flags**:
- `src/superclaude/cli/roadmap/commands.py:44-50`: `--output` is bound to the Python name `output_dir`, typed `click.Path(path_type=Path)`, help text "Output directory for all artifacts. Default: parent dir of spec-file." **This sibling command names the flag correctly and unambiguously** — proof the project knows the right pattern.
- `src/superclaude/cli/prd/commands.py:46-51`: `--output` is the *only* path-shaped user-supplied flag on `prd run` (other paths — `task_dir`, `research_dir`, `synthesis_dir`, `qa_dir`, `skill_refs_dir`, `template_path` — are derived inside `PrdConfig` and not user-tunable through the CLI surface; see `models.py:184-209`).
- `--where` (`commands.py:40-44`) takes source *directories* and is multiplied; it is not file-vs-directory ambiguous because the help text and usage make "source directories" explicit and the value is never `mkdir`-ed under.

**Blast radius**: Narrow. The pun is local to `prd run --output`. No other CLI surfaces propagate the same confusion. The fix is one-flag-deep and does not require ripple updates to roadmap/sprint commands. Within the PRD module itself, however, the impact is wider: four prompt sites (prompts.py:919, 986, 1042, 1093) all consume `config.output_path` with file-noun framing, so any fix must either rename the semantic to "directory" in those prompts or compute a derived file path before injection.

### Architect — Severity calibration

Severity hinges on the failure mode:

1. **Does the wrong interpretation silently succeed?** Partly. The `mkdir` step silently succeeds — a directory literally named `whatever.md` is created on the user's filesystem. This is silent filesystem pollution that survives the run.
2. **Does it fail loudly?** Yes, but downstream and opaquely. The LLM step that tries to `Write` to a directory will surface a tool error inside a stream-json log, not a clean CLI error. Or the LLM will pick a different filename and produce output the user does not look for.
3. **Is data lost?** No data is lost — the user simply does not get the file they asked for, and they get a misnamed directory.
4. **Is this exploitable / security-relevant?** Not in the traditional sense, but `Path(output).resolve()` with no validation will follow `..` segments and could `mkdir` arbitrary directories the process can write to. That is a minor sharp edge, not a vulnerability.
5. **Recoverability**: trivial — remove the spurious directory and re-run with the correct flag value. No corruption of prior artifacts.

The defect is a clear UX bug with concrete filesystem side-effects, but it does not corrupt prior work, does not silently produce wrong content (the LLM either errors or produces a divergently-named file), and is recoverable. The preliminary HIGH calls it correctly given that downstream LLM tool-error reporting is poor and the misnamed directory is a confusing artifact for the user to diagnose, but it does not reach CRITICAL because no data is lost and there is no security implication.

**Calibrated severity: HIGH** (confirmed, not downgraded).

---

## Convergence

**Verdict**: **CONFIRMED** — the finding is accurate, reproducible from code, and the evidence cited in `F-14-output-path-file-dir-pun.md` matches the source. No claim in the finding was contradicted by re-verification. One small enrichment: the sibling `roadmap run --output` flag (`src/superclaude/cli/roadmap/commands.py:44-50`) demonstrates the canonical pattern — naming the Click destination `output_dir`, typing it as `click.Path`, and labeling the help text "Output directory" — which is exactly the fix shape.

**Convergence score**: **0.95**. All three personas land on the same diagnosis; the only minor divergence is the architect's note that the failure mode mixes silent filesystem mutation with opaque downstream tool errors rather than failing loudly at the CLI boundary.

**Final severity**: **HIGH** (preliminary upheld).
- Reproducible: yes
- User-visible filesystem side-effect: yes (a `.md`-suffixed directory)
- Recoverable: yes
- Data loss: no
- Security implication: minimal (arbitrary `mkdir` via `..` is bounded by process permissions)

**Fix difficulty**: **LOW** (≤30 LOC, single-module, no migration).

Concrete shape:
1. Rename Click param destination: `--output` → `output_dir`, type `click.Path(path_type=Path)`. Update help to "Output *directory* for the PRD task tree (default: `.dev/eval-workspaces/`)" — matches `roadmap/commands.py:49`.
2. In `resolve_config` (`config.py:102-117`), validate: if the provided path has a file suffix or `is_file()`, raise `click.BadParameter` with a clear message ("`--output` must be a directory; got file-like path `…`. Did you mean `--output <dir>/` ?").
3. In `PrdConfig` (`models.py:184`), rename `output_path` → `output_dir` to match semantics; keep `task_dir` as the actual mkdir target.
4. In `prompts.py`, replace the four `output_path` injection sites with a derived **file** path (e.g. `config.task_dir / "PRD.md"` or a new `config.final_prd_path` property), so the prompts present an actual file path that matches the noun ("Output path", "Final PRD"). This eliminates the pun entirely rather than papering over it.

The roadmap CLI provides a working reference implementation for steps 1-3.

## Synthesis

The finding is fully validated. `--output` is a single-flag UX defect in the `prd run` command surface: the writer (`config.py:103-125`) treats the value as a directory parent and `mkdir`s into it; four prompt sites (prompts.py:919, 986, 1042, 1093) present the same value to the LLM with file-noun framing. The CLI help text (commands.py:50) is internally ambiguous ("Output path for final PRD" + "default: current directory"). The failure mode is mixed: silent filesystem pollution (a `.md`-named directory) plus opaque downstream LLM tool errors. The blast radius is local — the sibling `roadmap run --output` already implements the correct pattern. Severity HIGH is correctly calibrated; the fix is low-effort (≤30 LOC, single module) and the reference implementation already exists inside the same repo.
