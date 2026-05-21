# F-16 Adjudication — `_resolve_step_content` picks largest file without validation

**Source finding**: `.dev/eval-workspaces/prd-cli-audit/findings/F-16-resolve-content-largest-file-no-validation.md`
**Re-verified code**: `src/superclaude/cli/prd/executor.py:254-293`
**Supporting context**:
- `_STEP_ARTIFACT_FILES` mapping: `src/superclaude/cli/prd/executor.py:246-251`
- `task_dir` construction: `src/superclaude/cli/prd/config.py:123-125`
- Default output sandbox = `.dev/eval-workspaces/`: `src/superclaude/cli/prd/config.py:109-117`

## Re-verification (read-only)

Confirmed against the live source:

1. `_resolve_step_content` (executor.py:254-293) iterates `search_roots = [task_dir, task_dir.parent]` and calls `root.rglob(base_name)` (executor.py:280-281). The only filters are `-output.txt`, `node_modules`, `.git`, `__pycache__` (executor.py:283-285).
2. The "winner" rule is purely `len(content) > len(best_content)` (executor.py:288). No tie-breaker on path proximity to `task_dir`, no mtime check, no provenance check, no ownership marker.
3. `task_dir` defaults to `.dev/eval-workspaces/prd-<slug>/` (config.py:109-125). Therefore `task_dir.parent = .dev/eval-workspaces/`, which by design is the **shared parent of every prd run on the machine**.
4. `_STEP_ARTIFACT_FILES` (executor.py:246-251) — the four contaminable artifact basenames are `parsed-request.json`, `scope-discovery-raw.md`, `research-notes.md`, `sufficiency-review.md`. None are namespaced by product slug or run id.

Filesystem fact check (`ls .dev/eval-workspaces/`): the current repo already contains `prd-cli-audit/`, `prd-dry-run-test/`, `prd-test-product/` as siblings. The contamination precondition is **already true on disk in this repo**, not a hypothetical.

## Persona findings

### Analyzer (reproducibility)

Scenario: user runs `superclaude prd run "auth flow" --product authy` then later `superclaude prd run "billing" --product billz`. Both runs land in `.dev/eval-workspaces/prd-authy/` and `.dev/eval-workspaces/prd-billz/` respectively. The `billz` run executes `research-notes` step and writes `.dev/eval-workspaces/prd-billz/research-notes.md` (executor.py:995).

When `_resolve_step_content("research-notes", task_dir=.../prd-billz, ...)` is then called for downstream gate evaluation:

- `search_roots = [.../prd-billz, .../eval-workspaces]` (executor.py:275-277).
- `rglob("research-notes.md")` from `.../eval-workspaces` walks **every** sibling prd-* directory.
- It will find both `.../prd-billz/research-notes.md` (this run) and `.../prd-authy/research-notes.md` (prior run).
- Whichever is **longer wins** (executor.py:288), regardless of which run it belongs to.

Reproducibility: **deterministic given file sizes**. No race, no randomness — purely a function of which file on disk is larger. If the prior `authy` run produced a more thorough research-notes (3000 chars) and the current `billz` run produced a shorter one (1500 chars), the gate evaluates **authy's notes as if they were billz's**.

Aggravating second path: the finding's own reproduction sketch (a docs file at `/config/workspace/IronClaude/docs/research-notes.md`) does **not** actually reproduce when output is the default sandbox, because `task_dir.parent = .dev/eval-workspaces`, not the project root. That part of the finding's repro is wrong — but the **sibling-run contamination** path is real and worse, because sibling prd runs are the *expected* shape of `.dev/eval-workspaces/`.

The docs-file path **does** reproduce if the user passes `--output ./docs` or any directory whose parent contains stray matching filenames — a legitimate but narrower scenario.

### Refactorer (blast radius)

- This is the **only** `rglob` in `src/superclaude/cli/prd/` (single match in `executor.py:281`; no others in the package). So the bug is localized — no replicated copies elsewhere in the PRD pipeline to patch.
- Blast radius **within** the PRD pipeline: affects four gate inputs (`parsed-request.json`, `scope-discovery-raw.md`, `research-notes.md`, `sufficiency-review.md` — executor.py:246-251). All four are gate-relevant artifacts whose contents drive downstream prompt construction and gate decisions. Contamination silently substitutes another run's artifact into the current run's gate evaluation; the resulting gate verdict and any persisted artifact (executor.py:993-997 overwrites `task_dir/<artifact>` with whatever `_resolve_step_content` returned upstream of it, if wired that way) become provenance-corrupted.
- Filter set (`node_modules`, `.git`, `__pycache__`, `-output.txt`) is incidental hygiene, not a scoping mechanism. It will not prevent sibling-run matches.
- The `_persist_step_artifact` writer (executor.py:976-1004) correctly writes only to `self._config.task_dir / artifact_name`; the asymmetry is on the **read** side, not the write side. So the bug cannot corrupt sibling runs' files on disk — only this run's *interpretation* of its own artifacts.

### Architect (severity calibration)

Preliminary tag was MEDIUM with rationale "only triggers with shared parent dirs." Calibration:

- The shared-parent-dir condition is not exotic; it is the **default invariant** of the CLI (config.py:109-117 deliberately routes all runs into the shared sandbox). Any user running PRD a second time on the same machine satisfies the precondition.
- Failure mode is **silent semantic corruption**, not a crash. The gate evaluates contaminated content and produces a verdict that looks valid. No log line, no warning, no provenance breadcrumb. This is the worst class of correctness bug: invisible until someone manually diff's the persisted artifact against expectations.
- Detection cost is high: a developer would have to notice that two unrelated PRD runs produced suspiciously similar research notes, then trace the resolver.
- Mitigating factor: artifact files are write-once per step within a run (executor.py:995-997), so the *most recent* same-run write to `task_dir/<artifact>` will usually be the longest content path-of-least-resistance unless a prior run happens to have a larger file. So contamination is not 100% — it's conditional on `len(other_run.file) > len(this_run.file)`. That probability rises with longer-running PRDs that accumulate hand-edited notes in older sibling dirs.
- Not a security boundary issue — same-user, same-machine, same-pipeline. No privilege crossing. So not HIGH on a confidentiality/integrity-of-secrets axis. But it is HIGH on the **pipeline correctness** axis because the resolver is the seam that decides "what did this step actually produce", and getting that wrong invalidates every downstream gate.

Net calibration: MEDIUM is defensible if you weight "requires a prior run to exist with a larger same-named artifact". HIGH is defensible if you weight "default invariant + silent + corrupts gate inputs + zero detection signal". I land on **MEDIUM-HIGH**, leaning HIGH for users with any non-trivial PRD history.

## Convergence

**Verdict**: Confirmed. The bug is real, the reproduction is deterministic given a sibling prd run with a larger matching artifact, and the original finding's diagnosis is correct on the mechanism (though its specific repro sketch via `docs/research-notes.md` only fires under non-default `--output`).

**Convergence score**: 0.92. All three personas agree on existence, mechanism, and that the original "shared parent dir" precondition is in fact the CLI's default state. The only spread is severity (MEDIUM vs HIGH), which is a calibration axis, not a disagreement on facts.

**Final severity**: **MEDIUM-HIGH** (lean HIGH). The original MEDIUM tag underweights the fact that `.dev/eval-workspaces/` is the *default* sandbox, making the contamination precondition the rule rather than the exception. I would not block release on this alone, but it warrants a fix in the same release as any other gate-correctness work.

**Fix difficulty**: **Low** (≤30 LoC, single function).
- Option A (minimal): drop `task_dir.parent` from `search_roots` (executor.py:275-277). Restricts search to `task_dir` only. Risk: if subprocesses really do write to `task_dir.parent` as the docstring (executor.py:262-263) claims, that path is lost. Worth checking against the actual subprocess Write-tool behavior.
- Option B (correct): keep both roots but constrain `rglob` matches to paths where `match.is_relative_to(task_dir)` OR `match.parent == task_dir.parent` (i.e. project-root drops, not sibling-run drops). One predicate, no behavioral regression for the legitimate `.dev/` / `results/` write paths.
- Option C (belt-and-braces): add a provenance check — only accept files whose mtime is `>=` the start time of this step (the executor already has timing in `_logger.log_step_complete` at executor.py:1000-1004). Combines well with B.

**Synthesis**:

The resolver was designed to recover content that subprocesses write to disk outside the captured NDJSON stream — a legitimate goal. The implementation conflates "find files the subprocess wrote" with "find any file by that name under the project tree," and uses file size as the disambiguator. Both choices fail in the presence of sibling PRD runs, which is the *default* state of `.dev/eval-workspaces/` (config.py:109-117). The bug is narrow in code (one `rglob` call, one comparison) but broad in consequence: it feeds contaminated content into four gate-relevant artifacts (executor.py:246-251) with no warning, no log line, and no provenance trail.

Fix is small and well-contained (Option B above). Recommend pairing it with a one-line log breadcrumb when the chosen file is not a direct child of `task_dir`, so future contamination is observable rather than silent.
