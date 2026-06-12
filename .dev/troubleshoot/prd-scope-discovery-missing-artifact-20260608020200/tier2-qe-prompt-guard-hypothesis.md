# Tier-2 QE Hypothesis — PRD Prompt-Builder Missing-Artifact Crash

Angle: defensive robustness / edge-case coverage.

## Claim

`superclaude prd run` dies with a raw `FileNotFoundError` because the prompt-builder
layer (`prompts.py`) has an **inconsistent precondition contract**: most builders read
upstream task-dir artifacts with a hard, unguarded `path.read_text(...)` via `_read_file`
/`_load_json`, while one builder (web-research, line 787) reads the *same* artifact
guarded with `if scope_path.is_file() else ""`. When an upstream step ERRORs (exit != 0)
it never persists its artifact (`executor.py:748` writes only when `exit_code == 0`), and
because `scope-discovery` is a **STANDARD** gate — not STRICT — its ERROR does **not**
trigger the halt path at `executor.py:567-575`. The pipeline therefore advances to
`research-notes`, whose builder is invoked at `executor.py:672` **outside** any
`except` block, so the unguarded read at `prompts.py:257` raises `FileNotFoundError`
that propagates through `run()`'s `try/finally` (no `except`) and reaches the CLI as a
bare traceback. The defect is the missing precondition check in the builder layer, and
the fix belongs there: a *required* missing upstream artifact must become a structured,
catchable error that halts the pipeline gracefully — not an empty-string fallback, and
not a raw stack trace.

## Evidence (file:line verified)

- `prompts.py:42-47` — `_read_file(path, max_bytes=50_000)`: `content = path.read_text(encoding="utf-8")` with **no existence guard**. Verified.
- `prompts.py:37-39` — `_load_json(path)`: `json.loads(path.read_text(...))`, **no existence guard**. Verified.
- `prompts.py:257` — `build_research_notes_prompt`: `scope_content = _read_file(config.task_dir / "scope-discovery-raw.md")` — UNGUARDED. This is the exact crash site. Verified.
- `prompts.py:258` — same builder: `parsed = _load_json(config.task_dir / "parsed-request.json")` — UNGUARDED, same bug class. Verified.
- `prompts.py:785-788` — SMOKING GUN: web-research builder reads the *same* `scope-discovery-raw.md` **guarded**: `scope_path.read_text(...)[:2000] if scope_path.is_file() else ""`. Confirms the unguarded reads are an inconsistency, not intent. Verified.
- `executor.py:672` — `prompt = self._build_prompt(builder_name, step_id=step_id)` runs **before** and **outside** the `try:` at 688 (which catches only `RuntimeError` from `proc.start_with_retry()/wait()`, lines 688-695). A builder exception is not caught here. Verified.
- `executor.py:500/517/597` — `run()` is `try: ... finally:` with **no `except`**; builder exceptions are not converted to a graceful outcome. Verified.
- `executor.py:748` — `if exit_code == 0 and gate_content.strip(): self._persist_step_artifact(...)`. ERROR (exit != 0) ⇒ artifact never written. Verified.
- `gates.py:331-335` — `scope-discovery` `enforcement_tier="STANDARD"`. **Refines the grounding**: at `executor.py:567-575` only a **STRICT** gate failure halts the loop, so a scope-discovery ERROR lets the loop fall through to `research-notes`. This is the precise reason the crash is reachable. Verified.
- `models.py:145-153` — `is_failure` includes `ERROR`; but the halt at `executor.py:569` additionally requires `enforcement_tier == "STRICT"`, which scope-discovery is not. Verified.
- `_build_prompt` (`executor.py:1196-1232`): the doc comment at 1216-1218 deliberately invokes the builder body *outside* the `try` "so a TypeError raised inside the builder surfaces as the real bug" — confirming builder exceptions are intentionally un-trapped at this layer, which is exactly why a `FileNotFoundError` escapes. Verified.

## Unguarded-read inventory

task_dir artifacts = files produced by *upstream pipeline steps* (crash surface).
skill_refs_dir / spec files = packaged-with-skill or operator inputs (different failure class).

| Builder (fn) | Line | Artifact read | Source | Required? | Guarded? |
|---|---|---|---|---|---|
| `build_scope_discovery_prompt` | 158 | `parsed-request.json` | task_dir (upstream) | REQUIRED | NO (`_load_json`) |
| `build_research_notes_prompt` | 257 | `scope-discovery-raw.md` | task_dir (upstream) | REQUIRED | NO (`_read_file`) — **crash site** |
| `build_research_notes_prompt` | 258 | `parsed-request.json` | task_dir (upstream) | REQUIRED | NO (`_load_json`) |
| `build_sufficiency_review_prompt` | 340 | `research-notes.md` | task_dir (upstream) | REQUIRED | NO (`_read_file`) |
| `build_task_file_prompt` | 440 | `research-notes.md` | task_dir (upstream) | REQUIRED | NO (`_read_file`) |
| `build_task_file_prompt` | 441-445 | `build-request-template.md`, `agent-prompts.md`, `synthesis-mapping.md`, `validation-checklists.md`, `operational-guidance.md` | skill_refs_dir (packaged) | REQUIRED (install integrity) | NO (`_read_file`) |
| `build_verify_task_file_prompt` | 538-540 | `TASK-PRD-*.md` (glob, falls back to `task-file.md`) | task_dir (upstream) | REQUIRED | NO (`_read_file`); path-fallback only, no existence guard |
| `_derive_investigation_render_kwargs` | 740 | `research-notes.md` | task_dir (upstream) | OPTIONAL | YES (`if notes_path.is_file() else ""`) |
| `_derive_investigation_render_kwargs` | 755-758 | `parsed-request.json` (SPECS) | task_dir (upstream) | OPTIONAL | YES (`if parsed_path.is_file()` + try/except) |
| `_derive_web_research_render_kwargs` | 775 | `research-notes.md` | task_dir (upstream) | OPTIONAL | YES (`if notes_path.is_file() else ""`) |
| `_derive_web_research_render_kwargs` | 787 | `scope-discovery-raw.md` | task_dir (upstream) | OPTIONAL | YES (`if scope_path.is_file() else ""`) — **the guarded twin** |

Pattern: every **Stage-B dynamic** builder (`_derive_*`) is guarded; every **Stage-A
sequential** builder (`build_*`) is unguarded. The contract is split exactly along the
Stage A / Stage B seam — Stage A authors assumed strict sequential ordering guarantees
presence, which is false the moment an upstream STANDARD-gate step ERRORs.

## Proposed Fix

**Decision: raise-structured-and-halt for REQUIRED reads; keep empty-string fallback
for OPTIONAL reads.** Justification: `research-notes` is itself a STRICT gate
(`gates.py:340`) with `min_lines=100` and semantic section checks. Feeding it an empty
`scope_content` would let it generate fabricated/hollow notes from nothing, defeating the
gate's purpose and silently degrading the PRD — a worse failure than halting. A missing
*required* input must stop the run with a clear, actionable message naming the producing
step. Stage-B `_derive_*` reads are correctly optional and stay as-is.

Single layer, two coordinated edits:

**1. `prompts.py` — add a structured error + a required-read helper (near line 34-47):**

```python
class MissingArtifactError(RuntimeError):
    """A required upstream artifact was not produced by the step that owns it."""
    def __init__(self, path: Path, produced_by: str):
        self.path = path
        self.produced_by = produced_by
        super().__init__(
            f"Required artifact '{path.name}' is missing at {path}. "
            f"It should have been produced by the '{produced_by}' step, "
            f"which likely failed (ERROR/incomplete) without persisting output. "
            f"Re-run that step or resume with --resume-from {produced_by}."
        )

# producer map keyed by canonical artifact filename
_ARTIFACT_PRODUCER = {
    "scope-discovery-raw.md": "scope-discovery",
    "research-notes.md": "research-notes",
    "parsed-request.json": "parse-request",
}

def _read_required(path: Path, max_bytes: int = 50_000) -> str:
    if not path.is_file():
        raise MissingArtifactError(path, _ARTIFACT_PRODUCER.get(path.name, "an upstream step"))
    return _read_file(path, max_bytes)

def _load_required_json(path: Path) -> dict:
    if not path.is_file():
        raise MissingArtifactError(path, _ARTIFACT_PRODUCER.get(path.name, "an upstream step"))
    return _load_json(path)
```

Then convert the REQUIRED task_dir call sites:
- `:158` `_load_json(... parsed-request.json)` → `_load_required_json(...)`
- `:257` `_read_file(... scope-discovery-raw.md)` → `_read_required(...)`
- `:258` `_load_json(... parsed-request.json)` → `_load_required_json(...)`
- `:340` `_read_file(... research-notes.md)` → `_read_required(...)`
- `:440` `_read_file(... research-notes.md)` → `_read_required(...)`

(skill_refs_dir reads at 441-445 are a distinct install-integrity class; leave for a
follow-up or wrap with a separate `MissingSkillRefError` — out of scope for this crash.)

**2. `executor.py:_run_subprocess_step` — catch it at the builder call (line 672), turning
the crash into a graceful step ERROR that flows into the existing halt machinery:**

```python
        # Build prompt
        try:
            prompt = self._build_prompt(builder_name, step_id=step_id)
        except prompts.MissingArtifactError as exc:
            self._logger.log_gate_result(step_id, False, str(exc))
            self._tui.update_step(step_id, gate_state="FAIL")
            return PrdStepResult(status=PrdStepStatus.HALT, exit_code=-1)
```

Returning `HALT` (a STRICT-class terminal status) makes `run()` set `result.outcome =
"halt"` via the existing `executor.py:567-575` path *regardless* of the current step's
gate tier — appropriate, since a missing required input is unrecoverable in-loop. The
operator sees a named, actionable halt instead of a traceback.

**Who catches it:** the new `try` at `executor.py:672` is the sole catch point. Because
every REQUIRED read is funneled through `_read_required`/`_load_required_json`, and every
builder is invoked through `_build_prompt`, this one catch covers all Stage-A builders.
`run()`'s `try/finally` still needs no `except` — the exception never escapes the step.

Diff sketch (executor side):

```diff
-        prompt = self._build_prompt(builder_name, step_id=step_id)
+        try:
+            prompt = self._build_prompt(builder_name, step_id=step_id)
+        except prompts.MissingArtifactError as exc:
+            self._logger.log_gate_result(step_id, False, str(exc))
+            self._tui.update_step(step_id, gate_state="FAIL")
+            return PrdStepResult(status=PrdStepStatus.HALT, exit_code=-1)
```

(import: add `from . import prompts` at the top of the method or reuse the existing
local import already present in `_build_prompt` at `executor.py:1202`.)

## Confidence

Self-reported confidence: 0.9

Every link in the chain was Read and verified: unguarded read (257) → no persist on
ERROR (748) → STANDARD gate doesn't halt (gates.py:334 + executor.py:569) → builder
outside try (672) → run() has no except (597). The one residual uncertainty is whether
the upstream step in the live repro truly ERRORed vs. wrote a zero-length/empty artifact
(see If I'm wrong) and whether returning HALT vs ERROR changes downstream resume
ergonomics — both are minor and don't change the fix layer.

## Risks

- **Optional vs required misclassification:** The Stage-B `_derive_*` empty-string
  fallbacks are *correct* (research-notes/scope can legitimately be thin for web/broad
  investigation). Converting those to required would break `--where-only`/bare runs
  (comment at `prompts.py:752` documents the intended optionality). Fix must touch ONLY
  the `build_*` Stage-A sites, not `_derive_*`.
- **skill_refs_dir reads (441-445)** are a different failure class (install integrity, not
  pipeline ordering). Lumping them into the same `MissingArtifactError` with a step-name
  producer would emit a misleading "re-run step X" message. Keep separate.
- **`verify-task-file` glob fallback (538-540)** silently falls back to `task-file.md`
  then reads unguarded — a latent variant of this same bug. Worth flagging but the
  `_read_required` conversion there needs care because the path is computed, not canonical.
- **HALT vs ERROR choice:** returning HALT forces `outcome="halt"`; if any caller expects
  ERROR semantics for resume-from logic, prefer ERROR + an explicit `result.halt_reason`.
  Low risk, behavior-preserving either way since both are `is_failure`.

## consistency_with_docs

- `prompts.py:1-11` module docstring documents size caps and async/import bans but says
  nothing about precondition guarantees — consistent with the contract being implicit and
  under-specified, which is the root of the inconsistency.
- `executor.py:1216-1218` explicitly states builder bodies run *outside* the try so
  internal exceptions "surface as the real bug" — this fix aligns with that intent by
  making the bug surface as a *typed, catchable* error rather than a raw traceback, then
  catching exactly that type at the call boundary.
- `executor.py:736-741` (R5 "make silent degradation loud") shows the codebase already
  prefers loud, actionable failure over silent thin-foundation continuation — the
  raise-and-halt choice for required inputs is consistent with that established principle.
- The guarded twin at `prompts.py:787` is the in-repo precedent for handling this artifact;
  the fix generalizes the *intent* (don't crash on absence) while correctly diverging on
  *policy* (halt for required, empty for optional).

## If I'm wrong

If I'm wrong it's probably because the upstream step didn't ERROR-with-no-output but
instead wrote an empty or wrong-named `scope-discovery-raw.md` (note the `scope-discovery*.md`
glob tolerance at `executor.py:267`), in which case the file *exists* and the real defect
is in artifact-name resolution / persist-on-success, not the unguarded read — though the
builder guard is still a correct defensive hardening regardless.
