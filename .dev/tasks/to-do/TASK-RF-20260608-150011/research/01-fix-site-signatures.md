# Research: Fix-site signatures (exact current code)

Status: Complete

Scope: capture EXACT current signatures, line ranges, and insertion/anchor points for the
4 functions modified by the sprint-recovery hotfix (REPORT at
`.dev/troubleshoot/sprint-merge-stranding-checkpoint-stale-20260608144847/REPORT.md`).
All evidence is `file:line` read directly on branch `fix/prd-document-capture-hotfix`,
2026-06-08. Paths are absolute under `/config/workspace/IronClaude`.

---

## 1. `src/superclaude/cli/sprint/recovery.py` — `merge_recovery_bundle`

### Full current signature (recovery.py:381-386)
```python
def merge_recovery_bundle(
    bundle: RecoveryBundle,
    source_index: Path,
    *,
    release_dir: Optional[Path] = None,
) -> None:
```
- Docstring: recovery.py:387-412 (documents "7-step canonical merge sequence", mutates
  `bundle.status` + `bundle.end_tasklist_sha256` in place).
- `import shutil` is function-local at recovery.py:413.
- `release_dir` resolution: recovery.py:415-420 — when `None`, lazy-imports
  `from .config import _resolve_release_dir` and sets `release_dir = _resolve_release_dir(source_index)`.
  (Note: NOT a naive `source_index.parent` — see docstring lines 405-411. The REPORT's
  "canonical TASKLIST_ROOT = source_index.parent" anchor is the TASKLIST_ROOT, which
  in the sc:tasklist layout = `release_dir/tasklists`, NOT release_dir itself.)

### Path anchors established at top of body (recovery.py:425-431)
```python
results_dir = release_dir / "results"                    # :425
execlog_path = release_dir / "execution-log.jsonl"       # :426
audit_log = results_dir / "recovery-audit.log"           # :427
phase = bundle.affected_phase                            # :428
bundle_id = bundle.bundle_id                             # :429
                                                         # :430 (blank)
failures: list[str] = []                                 # :431
```
- `failures` is the load-bearing list: every step appends `f"<reason>:{...}"` strings to it.
  The final status flip keys off whether it is empty (see status flip below).

### The 7 step boundaries (exact comment line for each "Step N")
| Step | Comment line | What it does |
|------|--------------|--------------|
| Step 1 | recovery.py:433 | `# Step 1 — Rename original task transcripts; copy rerun transcripts to canonical paths.` (loop :440-457) |
| Step 2 | recovery.py:459 | `# Step 2 — Same rename-and-replace for checkpoint reports (phase-N-cp*.md).` (loop :461-479) |
| Step 3 | recovery.py:481 | `# Step 3 — Same for -errors.txt siblings.` (loop :483-500) |
| Step 4 | recovery.py:502 | `# Step 4 — Write phase-N-rerun-manifest.json atomically.` (body :503-523) |
| Step 5 | recovery.py:525 | `# Step 5 — Append phase_rerun_start, task_rerun_complete×N, phase_rerun_complete...` (body :526-574) |
| Step 6 | recovery.py:576 | `# Step 6 — Append phase_complete_superseded_by event...` (body :577-599) |
| Step 7 | recovery.py:601 | `# Step 7 — Rewrite phase-N-result.json atomically...` (body :602-671) |

### EXACT insertion point for a NEW step (after Step 3, before Step 4)
- Step 3's loop ends at **recovery.py:500** (`failures.append(f"copy-errors:{task_id}:{exc}")`).
- recovery.py:501 is **blank**.
- Step 4's comment begins at **recovery.py:502** (`# Step 4 — Write phase-N-rerun-manifest.json atomically.`).
- **A new "Step 3.5 — relocate + verify TASKLIST_ROOT deliverables" step inserts between
  line 501 (blank) and line 502 (the Step 4 comment).** This matches the REPORT's
  "after Step 3, before the manifest at recovery.py:502" anchor exactly.
- If the new step is renumbered as a new "Step 4", the existing Steps 4-7 comments
  (lines 502, 525, 576, 601) must be renumbered to 5-8.

### `failures` list usage (the "fail loudly" mechanism)
- Init: recovery.py:431 — `failures: list[str] = []`.
- Append sites (existing): :451, :457, :473, :479, :494, :500, :523, :574, :599, :634, :648-651, :670-671.
- A new step that detects a stranded/empty deliverable must
  `failures.append(f"deliverable-not-landed:{task_id}:{rel}")` to downgrade status (see flip).

### Atomic tmp + replace idiom (REPORT cited ~519-521; exact = recovery.py:519-521)
```python
tmp = manifest_path.with_suffix(manifest_path.suffix + ".tmp")
tmp.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
tmp.replace(manifest_path)
```
- Same idiom repeated for result.json at recovery.py:667-669.
- Note: this idiom is for **single text files**. For copying deliverable *trees* the existing
  code uses `shutil.copy2(produced, canonical)` (single file, e.g. :455, :477, :498).
  There is no existing directory-tree copy helper in this module — `shutil` is the only
  import (function-local at :413). A new tree copy would use `shutil.copytree`/`copy2`
  per-file; no existing recursive-copy precedent in recovery.py.

### `.failed-<ts>` forensic-rename idiom (mirror for clobber preservation)
- Steps 1/2/3 each rename a clobbered canonical to `.failed-<orig_mtime>` BEFORE copying the
  replacement, and record it in `bundle.artifacts_replaced[canonical] = preserved`:
  - Step 1: recovery.py:444-449.
  - Step 2: recovery.py:466-471.
  - Step 3: recovery.py:487-492.
- `orig_ts = int(canonical.stat().st_mtime)` is the timestamp source (e.g. :444).

### Final status flip (REPORT cited ~674; exact = recovery.py:674)
```python
bundle.status = RecoveryStatus.PARTIAL if failures else RecoveryStatus.SUCCESS   # :674
bundle.end_tasklist_sha256 = compute_tasklist_sha256(source_index)                # :675
```
- So a non-empty `failures` → `PARTIAL`; empty → `SUCCESS`. This is the only place status is set.

### `write_recovery_audit_log` call (REPORT cited ~676-687; exact = recovery.py:676-687)
```python
write_recovery_audit_log(
    audit_log,
    {
        "event": "merge_recovery_bundle",
        "bundle_id": bundle_id,
        "affected_phase": phase,
        "affected_tasks": list(bundle.affected_tasks),
        "status": bundle.status.value,
        "failures": failures,
        "rerun_attempt": bundle.rerun_attempt,
    },
)
```
- `failures` is surfaced verbatim in the audit log event → new failure strings show up here.

### `write_recovery_audit_log` signature (recovery.py:250)
```python
def write_recovery_audit_log(audit_log_path: Path, event: dict) -> None:
```
- Body recovery.py:250-267: prepends a `timestamp` key, appends one JSON line in append
  mode (`"a"`), `mkdir(parents=True, exist_ok=True)` first, swallows `OSError`.
- Exported in `__all__` (recovery.py:39).

### `RecoveryBundle` dataclass (recovery.py:76-114; `@dataclass` at :76)
Fields (recovery.py:105-114), in order:
```python
bundle_id: str                                              # :105 (required, positional)
affected_phase: int                                         # :106 (required, positional)
verb: str = "rerun-tasks"                                   # :107
affected_tasks: list[str] = field(default_factory=list)     # :108
artifacts_produced: list[Path] = field(default_factory=list)# :109
artifacts_replaced: dict[Path, Path] = field(default_factory=dict)  # :110
source_tasklist_sha256: str = ""                            # :111
end_tasklist_sha256: Optional[str] = None                   # :112
status: RecoveryStatus = RecoveryStatus.DRYRUN              # :113
rerun_attempt: int = 1                                      # :114
```
- The REPORT-named fields: `artifacts_produced` (:109), `affected_tasks` (:108),
  `affected_phase` (:106), `status` (:113). All present.
- Bundle-root derivation idiom already used inside merge: `bundle.artifacts_produced[0].parent`
  (= `<bundle>/results`) at :581 and :623, guarded for empty list. The REPORT's proposed
  "bundle root = artifacts_produced[0].parent.parent" extends this by one `.parent`.

### `RecoveryStatus` enum (recovery.py:58+, values used: SUCCESS / PARTIAL / DRYRUN)
- `.PARTIAL.value` and `.SUCCESS.value` used at recovery.py:659-661.

### CONFIRMED: no import of `_declared_deliverables` into recovery.py
- `grep _declared_deliverables src/superclaude/cli/sprint/recovery.py` → **0 hits**
  (only doc-comment mentions of `rerun_tasks` at :3, :44, :394, :406, :528, :612).
- `_declared_deliverables` is defined ONLY in `rerun_tasks.py:954` (see §2). recovery.py
  does NOT import rerun_tasks (would be a cycle: recovery is imported BY rerun_tasks).
  → If the fix needs declared deliverables inside `merge_recovery_bundle`, the REPORT's
  recommendation is to thread them in as a new optional param (e.g. `expected_deliverables`),
  NOT import the helper (the import direction forbids it).

---

## 2. `src/superclaude/cli/sprint/rerun_tasks.py` — merge site in `run_rerun_tasks`

`merge_recovery_bundle` is imported at rerun_tasks.py:49 (`from .recovery import ... merge_recovery_bundle`).

### Binding of `phase_obj` / `resolved` / `config` available at the merge site
- `config` is the `SprintConfig` param of `run_rerun_tasks` (resolved/loaded upstream;
  `config.index_path`, `config.release_dir`, `config.phases` all available).
- `phase_obj`: rerun_tasks.py:1304 — `phase_obj = next((p for p in config.phases if p.number == phase), None)`;
  guarded None at :1305-1306. `phase_obj.file` = the phase tasklist path.
- `resolved`: produced by `walk_dependencies(...)` at rerun_tasks.py:1368, returned as
  `resolved, warnings` and used as `list(resolved)` thereafter. It is the full set of
  task IDs re-executed (targets + dep closure).
- `config.index_path` is absolute (resolved in `load_sprint_config`), so `.parent` is
  cwd-independent (used at Step 14, :1526).

### `produced` glob (REPORT cited ~1444-1446; exact = rerun_tasks.py:1444-1446)
```python
produced = sorted(
    p for p in (bundle / "results").glob(f"phase-{phase}-*") if p.is_file()
)
```
- `bundle` here = the bundle directory (a `Path`); `produced` is ONLY files matching
  `<bundle>/results/phase-{phase}-*`. **This is the Defect-1 root: it never globs the
  bundle-root deliverable trees (`artifacts/`, `evidence/`).**

### `RecoveryBundle(...)` construction (REPORT cited ~1451-1459; exact = rerun_tasks.py:1451-1459)
```python
recovery = RecoveryBundle(
    bundle_id=bundle.name,
    affected_phase=phase,
    affected_tasks=list(resolved),
    artifacts_produced=produced,
    source_tasklist_sha256=source_sha,
    status=RecoveryStatus.SUCCESS,
    rerun_attempt=attempt,
)
```
- Wrapped by `if rerun_succeeded and merge_back:` at rerun_tasks.py:1436.
- `attempt` computed at :1447-1450.

### `merge_recovery_bundle(...)` call (REPORT cited ~1484-1485; exact = rerun_tasks.py:1484-1486)
```python
merge_recovery_bundle(
    recovery, config.index_path, release_dir=config.release_dir
)
```
- Both `config.index_path` (source_index) and `config.release_dir` are passed →
  inside merge, `release_dir` is authoritative (not re-resolved).
- **If the fix threads a new `expected_deliverables` kwarg into `merge_recovery_bundle`,
  this is the call to update** — and `phase_obj.file` + `resolved` are both in scope here
  to compute it via `_declared_deliverables(phase_obj.file, tid) for tid in resolved`.

### `finalize_checkboxes_on_success` call + signature
- Call: rerun_tasks.py:1487 — `finalize_checkboxes_on_success(phase_obj.file, resolved, bundle)`.
- Signature: rerun_tasks.py:888-890 —
  ```python
  def finalize_checkboxes_on_success(
      phase_tasklist: Path, target_ids: list[str], bundle_dir: Path
  ) -> None:
  ```
  Body :891-927; flips `- [ ]`→`- [x]`, appends rerun_history, writes audit-log event
  `rerun_checkboxes_finalized` via `write_recovery_audit_log` (:918-926).

### Step-14 verify-checkpoints subprocess (REPORT cited ~1508-1532; exact = rerun_tasks.py:1508-1532)
```python
# Step 14 — auto-invoke verify-checkpoints --recover (gated; TDD §T9).
if exit_code == 0 and merge_back and not no_verify_checkpoints:        # :1509
    try:
        subprocess.run(
            [
                "uv", "run", "superclaude", "sprint", "verify-checkpoints",
                str(config.index_path.parent),                          # :1526  (OUTPUT_DIR positional)
                "--recover",                                            # :1527
            ],
            check=False,                                                # :1529
        )
    except OSError as exc:
        click.echo(f"verify-checkpoints invocation failed: {exc}")     # :1532
```
- Gating flags: `exit_code == 0`, `merge_back`, `not no_verify_checkpoints` (:1509).
- Comment block :1518-1525 documents that the positional is `config.index_path.parent`
  (the dir holding `tasklist-index.md`), explicitly NOT `config.release_dir`, and notes
  "verify-checkpoints has no --phase/--quiet".
- **For Fix 2 (re-evaluate stale checkpoints), if a new flag like `--reevaluate-stale`
  is added to verify-checkpoints, this is the invocation list to extend.**

### `_declared_deliverables` full body (REPORT cited ~954-978; exact = rerun_tasks.py:954-978)
```python
def _declared_deliverables(source_tasklist: Path, task_id: str) -> list[Path]:
    """Best-effort: deliverable file paths declared for ``task_id``.
    ...
    """
    try:
        content = source_tasklist.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    block_re = re.compile(
        r"(^### " + re.escape(task_id) + r"\b.*?)(?=^### T\d{2}\.\d{2}|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    block_match = block_re.search(content)
    if block_match is None:
        return []
    paths: list[Path] = []
    for section in _ARTIFACTS_SECTION_RE.findall(block_match.group(1)):
        for raw in _ARTIFACT_BULLET_RE.findall(section):
            p = Path(raw)
            paths.append(p if p.is_absolute() else (Path.cwd() / p))
    return paths
```
- Returns absolute Paths (relative resolved against `Path.cwd()`, :977). Never raises.
- Supporting regexes: `_ARTIFACT_BULLET_RE` (rerun_tasks.py:947) matches
  `^\s*-\s+\`([^\`\s]+)\`\s*$`; `_ARTIFACTS_SECTION_RE` (:948-951) matches the
  `**Artifacts (Intended Paths):**` section. Defined immediately above the function.
- This is the helper the REPORT recommends threading into the merge to know which trees
  to verify landed.

---

## 3. `src/superclaude/cli/sprint/checkpoints.py` — `recover_missing_checkpoints` + `_render_recovered_checkpoint`

### `recover_missing_checkpoints` signature (checkpoints.py:213-219)
```python
def recover_missing_checkpoints(
    manifest: list[CheckpointEntry],
    artifacts_dir: Path,
    phase_tasklists: dict[int, Path],
    *,
    return_bundle: bool = False,
) -> list[CheckpointEntry] | RecoveryBundle:
```
- Docstring checkpoints.py:220-245 — explicitly documents "regenerate **missing** checkpoint
  reports" and "idempotent: if the expected file already exists on disk ... the entry is
  returned unchanged." (This is the Defect-2 design omission: it never reads/re-evaluates
  an existing file's verdict.)

### Full body (checkpoints.py:246-321)
Loop over `manifest` (:247), per entry:
- **Existence short-circuit (REPORT cited ~248-264; exact = checkpoints.py:248-260):**
  ```python
  # Refresh existence — a previous iteration may have written the file.
  if entry.expected_path.is_file():                       # :249
      out.append(
          CheckpointEntry(
              phase=entry.phase,
              name=entry.name,
              expected_path=entry.expected_path,
              exists=True,
              recovered=entry.recovered,
              recovery_source=entry.recovery_source,
          )
      )
      continue                                            # :260
  ```
  **This is the Defect-2 site: if the file exists it is appended unchanged and `continue`d —
  the existing frontmatter/verdict is never read or re-evaluated.** A `--reevaluate-stale`
  branch would hook in here (before the `continue`).
- Second short-circuit checkpoints.py:262-264:
  ```python
  if entry.exists or entry.phase not in phase_tasklists:
      out.append(entry)
      continue
  ```
- Recovery path (file truly missing): :266-299 — extracts verification block (:267),
  discovers evidence (:268), renders via `_render_recovered_checkpoint` (:270-274),
  `mkdir` + `write_text` (:276-277), appends a new `CheckpointEntry(..., exists=True,
  recovered=True, recovery_source=...)` (:290-299).
- **`return_bundle` branch (checkpoints.py:301-319):** when True, lazy-imports
  `from .recovery import RecoveryBundle, RecoveryStatus` (:305), computes
  `all_recovered = all(e.exists for e in out)` (:307), returns a `RecoveryBundle(...)` with
  `verb="verify-checkpoints"`, `affected_tasks=[]`, `artifacts_produced=[e.expected_path ...]`,
  status SUCCESS/PARTIAL (:308-318).
- Default return: `return out` (checkpoints.py:321).

### `_render_recovered_checkpoint` (REPORT cited ~398-439; exact = checkpoints.py:398-439)
Signature (checkpoints.py:398-403):
```python
def _render_recovered_checkpoint(
    *,
    entry: CheckpointEntry,
    verification_block: str,
    evidence: list[Path],
) -> str:
```
- **Frontmatter shape emitted (checkpoints.py:415-421):**
  ```python
  return (
      "---\n"
      f"checkpoint: {entry.name}\n"            # :417
      f"phase: {entry.phase}\n"                # :418
      "recovered: true\n"                      # :419
      f"generated_at: {timestamp}\n"           # :420
      "---\n\n"                                # :421
      ...
  ```
  Note: frontmatter has NO `status:` key — the verdict lives in the `## Result` body section.
- `## Note: Auto-Recovered` banner :422-427.
- **UNKNOWN-not-PASS lines (REPORT cited ~436-437; exact = checkpoints.py:435-438):**
  ```python
  "## Result\n\n"                                                          # :435
  "`UNKNOWN` — recovered without live verification. Re-run the phase or\n"  # :436
  "manually inspect the evidence artifacts listed above to confirm the\n"   # :437
  "acceptance criteria were met.\n"                                         # :438
  ```
  **HARD CONSTRAINT on the fix: recovered checkpoints are stamped `UNKNOWN`, NEVER `PASS`.**
  Any Fix-2 re-stamp path must emit `UNKNOWN`/Auto-Recovered, not auto-PASS.

---

## 4. `src/superclaude/cli/sprint/commands.py` — `verify_checkpoints` CLI

### Decorators + signature (commands.py:647-663)
```python
@sprint_group.command("verify-checkpoints")                                   # :647
@click.argument(
    "output_dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
)                                                                              # :648-651
@click.option("--recover", is_flag=True,
    help="Auto-generate missing checkpoint reports from evidence artifacts.") # :652-656
@click.option("--json", "as_json", is_flag=True,
    help="Emit the manifest as machine-readable JSON instead of a table.")    # :657-662
def verify_checkpoints(output_dir: Path, recover: bool, as_json: bool):       # :663
```
- Docstring :664-672. Confirms there is **no --phase / --quiet** option (matches the
  rerun_tasks Step-14 comment). Current options: only `--recover` and `--json`.
- **A new `--reevaluate-stale` flag (Fix 2 fallback) inserts as a new `@click.option`
  here (e.g. after :656), threaded into the signature and the recover call below.**

### Body + `recover_missing_checkpoints` call (commands.py:673-702)
- Lazy imports `build_manifest, recover_missing_checkpoints, write_manifest` from `.checkpoints`
  (:673-677) and `discover_phases` from `.config` (:678).
- `index_path = output_dir / "tasklist-index.md"` (:680); guarded `.is_file()` (:681-682).
- `manifest = build_manifest(index_path, output_dir)` (:684).
- **`recover_missing_checkpoints` call (REPORT cited ~693; exact = commands.py:686-693):**
  ```python
  if recover:                                                                 # :686
      artifacts_dir = output_dir / "artifacts"                                # :687
      try:
          phases = discover_phases(index_path)                                # :689
      except Exception as exc:  # noqa: BLE001
          raise click.ClickException(f"Phase discovery failed: {exc}") from exc
      phase_tasklists = {p.number: p.file for p in phases}                    # :692
      manifest = recover_missing_checkpoints(manifest, artifacts_dir, phase_tasklists)  # :693
  ```
  - Called positionally with 3 args; `return_bundle` defaults False → returns a
    `list[CheckpointEntry]`. **If Fix 2 adds a kwarg (e.g. `reevaluate_stale=...`), this
    is the call to update.**
- `write_manifest(manifest, manifest_path)` (:696); JSON or table output (:698-702).

---

## 5. `CheckpointEntry` fields (models.py:485-514)
`@dataclass` at models.py:485. Fields in order:
```python
phase: int                                  # :509 (required)
name: str                                   # :510 (required)
expected_path: Path                         # :511 (required)
exists: bool                                # :512 (required)
recovered: bool = False                     # :513
recovery_source: Optional[str] = None       # :514
```
- Docstring models.py:486-507. Note `recovery_source` (description string of artifacts used),
  `recovered` (bool). **No verdict/status field** — `build_manifest` records only `exists`
  (per REPORT, checkpoints.py:167), so the current model carries no per-checkpoint verdict.
  A Fix-2 that re-evaluates a stale verdict has no existing field to read the verdict from;
  it must parse the on-disk file's `## Result` body (no frontmatter `status:` key either —
  see §3 frontmatter shape).

---

## Summary of load-bearing anchors for the builder

1. **New merge step inserts at recovery.py:501→502** (blank line after Step-3 loop end at
   :500, before the Step-4 comment at :502). Renumber existing Steps 4-7 (comments at
   :502/:525/:576/:601) if the new step claims "Step 4".
2. **`failures.append(...)` is the only mechanism that downgrades status to PARTIAL**
   (flip at recovery.py:674). New "deliverable not landed" failures must go into `failures`.
3. **Atomic write idiom** = recovery.py:519-521 (`.tmp` + `tmp.replace`); clobber-preserve
   idiom = `.failed-<mtime>` rename (recovery.py:444-449 etc.). No recursive tree-copy
   helper exists; `shutil` is function-local at :413.
4. **No `_declared_deliverables` import in recovery.py** (confirmed 0 hits); it lives only at
   rerun_tasks.py:954. Thread declared deliverables IN as a new optional param — do not
   import (cycle: recovery is imported by rerun_tasks at rerun_tasks.py:49).
5. **Merge call to update** = rerun_tasks.py:1484-1486; `phase_obj.file` + `resolved` are
   both in scope there to compute the declared-deliverables list.
6. **Defect-2 short-circuit** = checkpoints.py:249-260 (file exists → appended unchanged →
   `continue`, verdict never read). A `--reevaluate-stale` branch hooks before the `continue`.
7. **UNKNOWN-not-PASS hard constraint** = checkpoints.py:436 (`\`UNKNOWN\` — recovered
   without live verification`). Recovered/re-stamped checkpoints must never be auto-PASS.
8. **CLI flag site** = commands.py:652-662 (add new option) + call at :693 (thread kwarg);
   verify-checkpoints currently has only `--recover` and `--json`, no `--phase`/`--quiet`.
9. **CheckpointEntry has no verdict field** (models.py:509-514) and recovered-checkpoint
   frontmatter has no `status:` key (checkpoints.py:415-421) — verdict lives only in the
   `## Result` body. Fix 2 must parse the body to read a stale verdict.
