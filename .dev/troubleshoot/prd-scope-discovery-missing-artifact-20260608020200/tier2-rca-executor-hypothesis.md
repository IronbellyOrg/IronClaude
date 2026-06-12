# Tier-2 RCA Hypothesis Card — PRD scope-discovery missing-artifact crash

## Claim

The crash is caused by **halt-gate conflation in the Stage A loop**: the
executor's decision to halt the pipeline keys *exclusively* off the
**downstream gate's `enforcement_tier`** of the step that just ran
(`executor.py:567-575`), not off *how the step ended*. A hard execution
**ERROR** (subprocess exit != 0, no artifact written) on `scope-discovery` —
whose gate is `STANDARD` (`gates.py:334`) — is therefore swallowed as a
"non-fatal STANDARD failure" and the loop continues. But ERROR is a
*production* failure, not a *quality* failure: it leaves
`scope-discovery-raw.md` **absent from disk** (artifact persistence is gated
on `exit_code == 0`, `executor.py:748`). The next step, `research-notes`,
builds its prompt by reading that file **unguarded** (`prompts.py:257` →
`_read_file` → `path.read_text`, `prompts.py:44`), and because the prompt
builder runs **outside** the per-step try/except (`executor.py:672` vs the
guard at `688-695`) and `run()` has a try/**finally** with **no except**
(`executor.py:517,597`), the `FileNotFoundError` escapes uncaught and kills
the whole CLI with a traceback instead of halting gracefully.

The defect is the executor treating "ran-but-gate-failed" (artifact exists,
safe to continue) and "errored/timed-out/crashed" (no artifact, must halt)
as the same class of event, then routing the halt decision through the wrong
discriminator (gate tier) for the second class.

## Evidence (cited file:line + what I verified)

- **`executor.py:541-575`** — VERIFIED. Stage A `for` loop. The only halt
  path is `567-575`: `if step_result.status.is_failure:` → `gate =
  GATE_CRITERIA.get(step_id)` → `if gate and gate.enforcement_tier ==
  "STRICT": result.outcome="halt"; break`. A failure on a step whose gate is
  STANDARD falls through the `if` and the loop proceeds to the next step. The
  loop body has **no try/except** around `self._execute_step(...)` (551).
- **`models.py:144-153`** — VERIFIED. `is_failure` is `True` for
  `HALT, TIMEOUT, ERROR, QA_FAIL_EXHAUSTED, VALIDATION_FAIL`. So `ERROR`
  *does* satisfy `is_failure` at line 567 — the bug is not that the failure
  is missed, it's that the **subsequent tier check discards it**.
- **`gates.py:330-335`** — VERIFIED. `"scope-discovery"` GateCriteria:
  `min_lines=50`, `enforcement_tier="STANDARD"`. `"research-notes"`
  (`337-341`) is `enforcement_tier="STRICT"`.
- **`executor.py:745-749`** — VERIFIED. Artifact persisted **only** `if
  exit_code == 0 and gate_content.strip()`. A hard ERROR (exit != 0) writes
  **no** `scope-discovery-raw.md`. Comment at 745-747 confirms intent:
  persist on exit-0 so STANDARD gate failures can still feed downstream.
- **`executor.py:688-695` + `757-771`** — VERIFIED. ERROR is produced either
  by `start_with_retry()` raising `RuntimeError` (caught → `ERROR`, exit -1,
  691-695) or by `_determine_status` returning `ERROR` for any `exit_code !=
  0` (770-771; `124` → TIMEOUT at 766). A ~0.3s failure is too fast for retry
  exhaustion (process retry delays), consistent with a fast non-zero exit.
- **`executor.py:672`** — VERIFIED. `prompt = self._build_prompt(...)` is the
  **first** statement in `_run_subprocess_step`, executed unconditionally
  *before* the `try:` at 688. `_execute_step` (607-628) calls it with no
  surrounding try. So a builder exception is unguarded at every frame up to
  `run()`.
- **`prompts.py:251-257` + `42-44`** — VERIFIED.
  `build_research_notes_prompt` calls `_read_file(config.task_dir /
  "scope-discovery-raw.md")`; `_read_file` does a bare
  `path.read_text(...)` with no `exists()`/`is_file()` guard → raises
  `FileNotFoundError` when the artifact is absent. This is the literal crash
  site in the transcript trace.
- **`prompts.py:785-788`** — VERIFIED (contrast). The web-research builder
  reads the **same** file *guarded*:
  `scope_path.read_text(...) if scope_path.is_file() else ""`. Proves the
  missing-artifact case is a known, survivable condition elsewhere — the
  research-notes builder is simply the unguarded outlier.
- **`executor.py:517,597`** — VERIFIED. `run()` body is `try: ... finally:`
  with **no `except`** clause. Exceptions propagate out of `run()`.

## Proposed Fix (exact, with diff sketch)

**Layer chosen: executor orchestration — the `run()` Stage A halt logic
(`executor.py:567-575`).** This is the most load-bearing layer: it is the
single chokepoint where *every* step's outcome is adjudicated, and it is
where the category error lives. Guarding one prompt builder (`prompts.py:257`)
would only paper over *this* downstream step; the next unguarded reader, or a
different errored step, reproduces the same class of crash. Fixing the halt
decision contains the failure at its source for all steps.

**Change:** halt on a step that **errored/crashed/timed-out** regardless of
its gate tier, while preserving the existing "STANDARD gate-quality failure
continues" behavior. Distinguish the two by *status*, not by gate tier.

Introduce a hard-failure predicate (production failure → no artifact, unsafe
to continue) separate from the soft gate-quality failure (`VALIDATION_FAIL`,
where exit was 0 and the artifact was persisted).

```python
# models.py — add next to is_failure (~line 153)
@property
def is_hard_failure(self) -> bool:
    """Execution/production failure: process errored, timed out, crashed,
    or budget-exhausted. Artifact is NOT guaranteed on disk -> unsafe for
    downstream steps. Distinct from VALIDATION_FAIL (gate-quality failure
    on a clean exit-0 run, artifact persisted)."""
    return self in (
        PrdStepStatus.ERROR,
        PrdStepStatus.TIMEOUT,
        PrdStepStatus.HALT,
        PrdStepStatus.QA_FAIL_EXHAUSTED,
    )
```

```diff
# executor.py:566-575
-                # STRICT gate failure halts pipeline
-                if step_result.status.is_failure:
-                    gate = GATE_CRITERIA.get(step_id)
-                    if gate and gate.enforcement_tier == "STRICT":
-                        result.outcome = "halt"
-                        result.halt_step = step_id
-                        result.halt_reason = (
-                            f"STRICT gate failure: {step_result.status.value}"
-                        )
-                        break
+                # Halt on (a) any HARD execution failure — errored/timed-out/
+                # crashed/budget-exhausted leaves NO artifact on disk, so
+                # downstream steps that read it would crash; OR (b) a STRICT
+                # gate-quality failure. STANDARD gate-quality failures
+                # (VALIDATION_FAIL on a clean exit-0 run, artifact persisted)
+                # remain intentionally non-fatal.
+                if step_result.status.is_failure:
+                    gate = GATE_CRITERIA.get(step_id)
+                    strict_gate_fail = bool(
+                        gate and gate.enforcement_tier == "STRICT"
+                    )
+                    if step_result.status.is_hard_failure or strict_gate_fail:
+                        result.outcome = "halt"
+                        result.halt_step = step_id
+                        result.halt_reason = (
+                            f"hard failure: {step_result.status.value}"
+                            if step_result.status.is_hard_failure
+                            else f"STRICT gate failure: {step_result.status.value}"
+                        )
+                        break
```

Net behavior: `scope-discovery` ERROR → `is_hard_failure` True → graceful
`result.outcome="halt"` with `halt_step="scope-discovery"`, loop breaks,
`research-notes` never runs, no `FileNotFoundError`, CLI exits cleanly with a
halt reason. STANDARD gate *quality* degradation (`VALIDATION_FAIL`, exit 0,
artifact present) still continues — unchanged.

**Recommended defense-in-depth (not the primary fix):** also guard
`prompts.py:257` to mirror `785-788` (`... if scope_path.is_file() else ""`),
so no future orchestration regression can turn a missing artifact into an
uncaught crash. The executor fix is primary because it addresses the
*category error*; the builder guard is belt-and-suspenders.

## Confidence

Self-reported confidence: 0.88

All seven citations independently verified against the source; the crash
trace maps cleanly onto the verified control flow. The residual 0.12 is
because I confirmed the *mechanism* statically but did not reproduce the
0.3s non-zero exit of the scope-discovery subprocess (the upstream *trigger*
of the ERROR is out of scope for this card and could be a second, separable
defect).

## Risks

- **Must NOT break intentional STANDARD gate-quality continuation**
  (`executor.py:736-741`): scope-discovery failing its `min_lines=50`
  STANDARD gate after `--spec` binding is deliberately non-fatal (the run
  proceeds on a "thin foundation" and emits `_warn_spec_degradation`). That
  path is `exit_code==0` + gate-fail → `VALIDATION_FAIL` (`734`), which is
  **excluded** from `is_hard_failure`, so the fix preserves it. This is the
  single most important invariant not to regress.
- `QA_FAIL_EXHAUSTED` is included in `is_hard_failure`: verify that a
  STANDARD step which exhausts its QA budget (`668`, exit -1, no artifact)
  *should* halt. It leaves no artifact, so halting is correct — but confirm
  no existing flow relies on continuing past it.
- `HALT` (sentinel-driven, `776`) is already terminal via the STRICT path in
  many cases; including it in `is_hard_failure` makes it halt for STANDARD
  steps too. That is the desired explicit-stop semantics, but worth a test.
- Possible **double-counting** of failure semantics: ensure no other call
  site relies on `is_failure` meaning "halt-worthy" — the fix narrows halting
  to `is_hard_failure ∪ STRICT-gate`, a strict subset of `is_failure`.

## consistency_with_docs

aligned — The fix is consistent with the in-code INV-010 contract
(`executor.py:709-718`, channel separation, untouched) and with the
artifact-persistence comment (`745-747`, "STANDARD gate failures don't halt
... downstream steps still need the data"), which presumes the artifact
*exists*; the fix restores that presumption by halting precisely when the
artifact is absent. No conflicting external doc found for the halt-tier
policy; the policy lives only in code.

## If I'm wrong

If I'm wrong it's probably because the scope-discovery subprocess actually
*did* exit 0 (so an artifact was written) and the ERROR/missing-file arose
from a content-resolution or path-pinning defect (`_resolve_step_content` /
task_dir mismatch), in which case the halt-gate conflation is a real but
*secondary* bug and the primary root cause sits upstream in artifact
persistence or path resolution rather than the run() halt logic.
