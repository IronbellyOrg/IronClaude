---
status: success
tier_reached: 2
confidence: 0.90
escalation_reason: forced_by_depth_deep
test_is_wrong: false
behavior_is_documented: false
---

# Troubleshoot Report — PRD pipeline crashes with uncaught FileNotFoundError on `scope-discovery-raw.md`

**Target:** `superclaude prd run` (src/superclaude/cli/prd/)
**Type:** bug · **Tier reached:** 2 (forced by `--depth deep`) · **Confidence:** 0.90 (calibrated)
**Output dir:** `.dev/troubleshoot/prd-scope-discovery-missing-artifact-20260608020200/`

## Summary

The PRD pipeline dies with a raw Python traceback (`FileNotFoundError: .../scope-discovery-raw.md`) instead of halting gracefully. Two coupled defects produce it. **(A) Halt-gate conflation:** when `scope-discovery` hard-ERRORs (its subprocess exited non-zero in ~0.3s and therefore wrote no artifact), the Stage-A loop does not halt, because the halt decision keys off the downstream *gate enforcement tier* (`scope-discovery` is `STANDARD`, not `STRICT`) rather than off whether the step actually *crashed*. **(B) Unguarded required-artifact read:** the next step, `research-notes`, builds its prompt by unconditionally reading the missing `scope-discovery-raw.md`; that read happens *outside* any try/except, so the exception escapes `executor.run()` (which has `try/finally` but no `except`) and crashes the CLI. The fix is defense-in-depth: halt on any hard execution failure regardless of gate tier (closes A at the source), and convert the required Stage-A artifact reads to a typed, catchable error that yields a graceful HALT (closes B as a backstop).

## Diagnosis

The 0.3s ERROR on `scope-discovery` is the *trigger*; the *defect* is that the pipeline cannot survive any upstream step failing without crashing the whole CLI. Trace:

1. `scope-discovery` subprocess exits non-zero fast (~0.3s — too fast to be retry-exhaustion, since `process.py` retry delays are `[5.0, 15.0]`). `_determine_status` returns `ERROR` (`executor.py:770-771`).
2. Because `exit_code != 0`, the artifact-persist guard at `executor.py:748` (`if exit_code == 0 and gate_content.strip()`) is skipped — **`scope-discovery-raw.md` is never written.**
3. Back in the Stage-A loop, `step_result.status.is_failure` is `True` (ERROR ∈ failure set, `models.py:145-152`), but the halt at `executor.py:567-575` only fires when `gate.enforcement_tier == "STRICT"`. `scope-discovery`'s gate is `STANDARD` (`gates.py:331-335`) → **no halt; loop continues to `research-notes`.**
4. `research-notes` → `_run_subprocess_step` → `_build_prompt` (`executor.py:672`) → `build_research_notes_prompt` (`prompts.py:257`) → `_read_file(scope-discovery-raw.md)` (`prompts.py:42-47`) → `read_text()` on a non-existent file → **`FileNotFoundError`**.
5. `_build_prompt` is invoked *before/outside* the per-step `try/except RuntimeError` (`executor.py:688-695`), and `run()` wraps Stage A in `try/finally` with **no `except`** (`executor.py:517`, `597`) → the exception is uncaught → **CLI traceback.**

**Smoking gun that B is a defect, not intended design:** the *same* artifact is read in two builders — `build_research_notes_prompt` reads it **unguarded** (`prompts.py:257`), while the web-research builder reads it **guarded** (`prompts.py:785-788`: `scope_path.read_text(...) if scope_path.is_file() else ""`). The contract is informal and inconsistent. The quality-engineer audit found the split is clean along the Stage-A/Stage-B seam: all five Stage-A `build_*` `task_dir` reads are unguarded and **required** (`prompts.py:158, 257, 258, 340, 440`); all four Stage-B `_derive_*` reads are guarded and **optional** (`prompts.py:740, 755, 775, 787`).

This is single-domain (orchestration robustness). It is not a documented-behavior case (`behavior_is_documented=false`) and not a wrong-test case (`test_is_wrong=false`): the executor comment at `executor.py:736-741` documents that *STANDARD gate-quality* degradation is intentionally non-fatal — but that reasoning assumes the step **ran and wrote its artifact** (exit 0, gate-fail). A hard ERROR (exit≠0, no artifact) is a different failure mode the current code conflates with gate-quality degradation.

## Evidence

- `executor.py:567-575` — Stage-A halt fires only on `is_failure` **AND** `gate.enforcement_tier == "STRICT"`.
- `models.py:145-152` — `is_failure` includes `ERROR`, `TIMEOUT`, `QA_FAIL_EXHAUSTED`, `VALIDATION_FAIL`, `HALT`.
- `gates.py:331-335` — `scope-discovery` gate `enforcement_tier="STANDARD"`.
- `gates.py:336-353` — `research-notes` gate `enforcement_tier="STRICT"` (so feeding it empty scope content would be wrong, not merely degraded).
- `executor.py:744-749` — artifact persisted only `if exit_code == 0 and gate_content.strip()`.
- `executor.py:770-771` — `if exit_code != 0: return PrdStepStatus.ERROR`.
- `executor.py:672` — `_build_prompt(...)` called outside the `try/except RuntimeError` at `688-695`.
- `executor.py:517, 597` — `run()` Stage-A body is `try/finally`, no `except`.
- `prompts.py:42-47` — `_read_file` calls `path.read_text` with no existence guard. `_load_json` (`prompts.py:37-39`) likewise calls `read_text` unguarded.
- `prompts.py:257` (`_read_file` → `scope-discovery-raw.md`) and `258` (`_load_json` → `parsed-request.json`) — `build_research_notes_prompt` reads both unguarded. The other REQUIRED Stage-A reads: `158` (`_load_json` → `parsed-request.json`), `340` and `440` (`_read_file` → `research-notes.md`). Verified inline: 257/340/440 are `_read_file` (str), 158/258 are `_load_json` (dict).
- `prompts.py:785-788` — web-research builder reads the **same** `scope-discovery-raw.md` guarded with `.is_file()` (one of four correctly-guarded optional Stage-B `_derive_*` reads).
- `executor.py:247-270` — canonical step→artifact map already exists (`scope-discovery → scope-discovery-raw.md`), available for a precondition check.

## Proposed Fix (defense-in-depth — two load-bearing atoms)

**Atom 1 — Executor: halt on any hard execution failure, independent of gate tier** (closes defect A at the source; minimal-surface correctness fix).

In `models.py`, add a predicate distinguishing a *production* failure (crashed/timed-out → no artifact) from a *quality* failure (clean exit-0 gate-fail → artifact persisted):

```python
# models.py — PrdStepStatus
@property
def is_hard_failure(self) -> bool:
    return self in {
        PrdStepStatus.ERROR,
        PrdStepStatus.TIMEOUT,
        PrdStepStatus.QA_FAIL_EXHAUSTED,
        PrdStepStatus.HALT,
    }
```

In `executor.py:567-575`, halt on a hard failure of **any** step, OR a STRICT-gate failure (preserving the existing STRICT semantics):

```python
if step_result.status.is_failure:
    gate = GATE_CRITERIA.get(step_id)
    strict_gate_fail = bool(gate and gate.enforcement_tier == "STRICT")
    if step_result.status.is_hard_failure or strict_gate_fail:
        result.outcome = "halt"
        result.halt_step = step_id
        result.halt_reason = (
            f"hard failure: {step_result.status.value}"
            if step_result.status.is_hard_failure
            else f"STRICT gate failure: {step_result.status.value}"
        )
        break
```

This preserves the intentional non-fatal STANDARD gate-quality path (`VALIDATION_FAIL`, exit 0, artifact written — `executor.py:736-741`) while halting cleanly when a step actually errored.

**Atom 2 — Prompt builders: typed, catchable error for missing REQUIRED artifacts** (closes defect B; backstop for any future path that reaches a builder without its input — e.g. `--resume-from` against a missing artifact, or a step that exits 0 but writes nothing).

> ⚠️ **Atom 2 depends on Atom 1 — do not ship it alone.** Atom 2 raises an error that the executor converts to a `HALT` step result, but `HALT` on a `STANDARD`-tier step only actually breaks the Stage-A loop once Atom 1 makes `is_hard_failure` include `HALT` (the current `executor.py:567-575` breaks only on a `STRICT` gate). Several converted reads live in `STANDARD`/non-STRICT builders (e.g. `scope-discovery` reads `parsed-request.json` at `prompts.py:158`), so without Atom 1 a `HALT` there would not halt and the pipeline would limp onward. Ship Atom 1 first; Atom 1 is independently sufficient to prevent the reported crash and independently revertable, Atom 2 is not.

In `prompts.py`, add `MissingArtifactError` plus **two** required-read helpers — note the two reader families: `_read_file` (returns `str`) and `_load_json` (returns `dict`). The five REQUIRED Stage-A reads split across both: `_read_file` sites → `prompts.py:257` (`scope-discovery-raw.md`), `340` and `440` (`research-notes.md`); `_load_json` sites → `prompts.py:158` and `258` (`parsed-request.json`). A single str-returning helper cannot wrap the JSON sites (type error breaking the dict consumers), so add a parallel JSON helper:

```python
class MissingArtifactError(FileNotFoundError):
    def __init__(self, path: Path, producer_step: str):
        self.path, self.producer_step = path, producer_step
        super().__init__(
            f"Required artifact {path.name} is missing — its producer step "
            f"'{producer_step}' did not complete successfully. Path: {path}"
        )

def _read_required(path: Path, producer_step: str, max_bytes: int = 50_000) -> str:
    if not path.is_file():
        raise MissingArtifactError(path, producer_step)
    return _read_file(path, max_bytes)

def _load_json_required(path: Path, producer_step: str) -> dict:
    if not path.is_file():
        raise MissingArtifactError(path, producer_step)
    return _load_json(path)
```

Convert `prompts.py:257, 340, 440` to `_read_required(...)` and `prompts.py:158, 258` to `_load_json_required(...)`. In `executor._build_prompt` (the real call site at `executor.py:672`), catch `MissingArtifactError` and convert it to a `PrdStepResult(status=HALT, ...)` with a clear `halt_reason`, so it surfaces as a graceful pipeline halt rather than a raw traceback. (Leave the four Stage-B `_derive_*` reads as-is — they are correctly guarded/optional. `MissingArtifactError` subclasses `OSError`, but the only nearby `except OSError` is at `executor.py:701`, a different code region — the `raw_output` read — so there is no accidental swallow.)

**Deferred (Atom 3, not recommended for V1):** a declared `_STEP_REQUIRED_INPUTS` precondition map checked before every step. The refactoring-expert's own assessment: for a mostly-linear V1 CLI, "halt on any hard ERROR" (Atom 1) gets ~90% of the safety for ~5% of the code; adopt the full precondition gate only when the dynamic Stage-B graph gains real fan-out. Atoms 1+2 already close the reported crash.

## Alternative Fixes Considered

- **Per-builder `.is_file()` guard + empty-string fallback only** (mirroring `prompts.py:787`): rejected as the *primary* fix — `research-notes` is a STRICT gate, so silently feeding it empty scope content would produce a hollow PRD that fails downstream rather than failing loudly at the real cause. Empty-string fallback is correct only for the optional Stage-B reads.
- **Precondition dependency-map gate (Atom 3):** structurally cleanest and catches the whole class, but over-engineered for the current mostly-linear pipeline; deferred per the refactoring-expert's honest cost/benefit call. Composes cleanly with Atoms 1+2 later.

## Risk + Rollback

- **Atom 1 risk:** must not break the *intentional* non-fatal STANDARD gate-quality degradation (`executor.py:736-741`). Mitigated: `VALIDATION_FAIL` (exit 0) is excluded from `is_hard_failure`; only genuine crashes/timeouts halt. Add a regression test: a STANDARD step that returns `VALIDATION_FAIL` must NOT halt; one that returns `ERROR` MUST halt.
- **Atom 2 risk:** mis-classifying an optional read as required would turn a tolerable empty input into a halt. Mitigated: only the five enumerated Stage-A `build_*` reads are converted; Stage-B `_derive_*` untouched.
- **Atom 2 ordering dependency (load-bearing):** Atom 2's `HALT` only halts once Atom 1 is in place (see the ⚠️ box above). Ship/merge Atom 1 first. Atom 1 alone already prevents the reported crash; Atom 2 alone is **not** independently sufficient.
- **Test stubbing caveat:** `_build_prompt` is monkeypatched in the e2e suite (`tests/.../test_e2e.py:549`). The Atom 2 regression test must exercise the **real** `_build_prompt` call site (not a stub) or it bypasses the `MissingArtifactError` catch.
- **Rollback:** atoms are localized (`models.py`, `executor.py` loop, `prompts.py` reads). Atom 1 reverts independently; Atom 2 should be reverted with or before Atom 1 (it relies on Atom 1's `is_hard_failure`).
- **Separate, lower-priority follow-up:** the *root trigger* — why the `scope-discovery` Claude subprocess exits non-zero in 0.3s — is environment-specific (likely the `claude` binary/auth/model unavailable or rejecting args in that container) and not diagnosable from the repo alone. After the robustness fix, the pipeline will HALT at `scope-discovery` with a clear message instead of crashing at `research-notes`, making that trigger far easier to diagnose. Recommend capturing `scope-discovery-error.txt` content on ERROR.

## Grounding Gaps

- The 0.3s non-zero exit of the `scope-discovery` subprocess could not be reproduced here (no `claude` runtime / captured `scope-discovery-error.txt` in this environment); the ERROR→no-artifact→no-halt→downstream-crash chain is fully grounded in code, but the *first-cause* of the subprocess exit is inferred, not observed.
- The dedicated `evidence-validator` agent produced no output this run. Citations were validated via the documented inline fallback **and** independently corroborated by the `self-review` agent's re-trace; **zero citations were dropped**, and the `_read_file`/`_load_json` split (158/258/340/440) was re-confirmed inline against source. Status is retained as `success` on that basis, with this substitution disclosed.

## Next Steps

- This run used `--fix`: on confirmation, proceed to the Tier 3 remediation chain (build an MDTM task file for Atoms 1+2; you run `/task`; `/sc:reflect --type task --validate` gates the commit). Source-of-truth edits go in `src/superclaude/cli/prd/`, then `make sync-dev` + `make verify-sync`.
