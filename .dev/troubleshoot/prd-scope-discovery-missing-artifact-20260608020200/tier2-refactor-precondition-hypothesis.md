# Tier-2 Hypothesis (Structural / Systemic-Design angle)

## Claim

The crash is not fundamentally "scope-discovery errored" — that is the *trigger*. The
**class** of bug is: the PRD pipeline encodes step-to-step data dependencies **implicitly
and unchecked**. Every step that consumes an upstream artifact (`research-notes` reads
`scope-discovery-raw.md`, `web-research`/`synthesis` read `research-notes.md`, etc.) trusts
that the file exists because the producer "should have" run. There is a canonical
producer-side map (`_STEP_ARTIFACT_FILES`, executor.py:252-263) but **no consumer-side
precondition gate**: no declared edge `research-notes -> requires(scope-discovery-raw.md)`
and no assertion run before a builder touches disk. When any producing step fails to write
its artifact *without* tripping a STRICT halt, the next consumer's prompt builder does an
unguarded `read_text()` and the raw `FileNotFoundError` escapes to the CLI top level. The
same missing file is read defensively elsewhere (prompts.py:785-788), proving the contract
is informal and inconsistently enforced — a structural inconsistency, not a one-step bug.

## Evidence (file:line verified)

- **executor.py:252-263** — `_STEP_ARTIFACT_FILES` maps each step to its canonical *output*
  artifact (`"scope-discovery": "scope-discovery-raw.md"`, `"research-notes": "research-notes.md"`).
  The system already knows producer-side filenames. There is **no** corresponding
  *consumer-side* `required_inputs` map. Verified.
- **executor.py:541-575** — `run()` Stage-A loop. After `_execute_step`, the only halt path
  (567-575) is `if step_result.status.is_failure:` **AND** `gate.enforcement_tier == "STRICT"`.
  Both conditions required. Verified.
- **gates.py:331-335** — `scope-discovery` has `enforcement_tier="STANDARD"`. Its failure
  satisfies `is_failure` but **fails the STRICT check**, so the loop does not break and the
  next iteration runs `research-notes`. Verified.
- **gates.py:337-340** — `research-notes` is `STRICT`, but that tier is only consulted
  *after* the step runs and gates; it does nothing to protect the prompt-build phase that
  crashes first. Verified.
- **models.py:144-153** — `is_failure` includes `ERROR` (subprocess exit non-zero ->
  `_determine_status` returns `ERROR` at executor.py:770-771). So scope-discovery's
  ERROR *is* a failure — it just isn't a STRICT one. Verified.
- **executor.py:745-749** — artifact is persisted only `if exit_code == 0 and gate_content.strip()`.
  A 0.3s non-zero exit writes nothing, so `scope-discovery-raw.md` never lands. Verified.
- **executor.py:672** — `prompt = self._build_prompt(builder_name, step_id=step_id)` runs
  unconditionally at the top of `_run_subprocess_step`, before any per-step I/O guard. This
  is the crash site for the *consumer*. Verified.
- **prompts.py:42-47** — `_read_file` does `content = path.read_text(...)` with **no
  `.is_file()` guard** -> raises `FileNotFoundError`. Verified.
- **prompts.py:257** — `build_research_notes_prompt` -> `_read_file(task_dir / "scope-discovery-raw.md")`.
  Unguarded. This is the uncaught throw. Verified.
- **prompts.py:785-788** — the *same* file read elsewhere is guarded:
  `scope_path.read_text(...)[:2000] if scope_path.is_file() else ""`. Inconsistent contract
  proven by the codebase contradicting itself on the identical path. Verified.

## Proposed Fix (exact + diff sketch + the dependency map)

**One structural fix: a declared input-artifact precondition gate in the executor, reusing
the existing canonical-artifact map.**

### 1. New data structure (executor.py, beside `_STEP_ARTIFACT_FILES`, ~line 264)

A consumer-side dependency map keyed by *step_id producing the artifact*, so it is derived
from — not duplicated against — `_STEP_ARTIFACT_FILES`:

```python
# Consumer-side: step_id -> list of PRODUCER step_ids whose canonical
# artifacts must exist on disk before this step's prompt is built.
# Filenames are resolved via _STEP_ARTIFACT_FILES (single source of truth),
# so renaming an artifact never desyncs this table.
_STEP_REQUIRED_INPUTS: dict[str, list[str]] = {
    "research-notes": ["scope-discovery"],
    "sufficiency-review": ["research-notes"],
    "web-research": ["research-notes"],
    "synthesis": ["research-notes"],
    "assembly": ["research-notes"],
    # extend as the dynamic Stage-B graph is declared
}
```

Filenames are looked up, not restated:
`required_file = self._config.task_dir / _STEP_ARTIFACT_FILES[producer]`.

### 2. The check (top of `_execute_step`, executor.py ~620, before the subprocess dispatch at 627-628)

```python
missing = self._check_input_preconditions(step_id)
if missing:
    producer, fname = missing[0]
    return PrdStepResult(
        status=PrdStepStatus.HALT,
        exit_code=-1,
        # surfaced via diagnostics.record_step + halt_reason below
    )
```

Helper:

```python
def _check_input_preconditions(self, step_id: str) -> list[tuple[str, str]]:
    missing: list[tuple[str, str]] = []
    for producer in _STEP_REQUIRED_INPUTS.get(step_id, ()):
        fname = _STEP_ARTIFACT_FILES.get(producer)
        if fname and not (self._config.task_dir / fname).is_file():
            missing.append((producer, fname))
    return missing
```

Putting it at the top of `_execute_step` means it covers **both** internal and subprocess
steps and runs *before* `_build_prompt` at 672 — so the builder's `_read_file` is never
reached with a missing file. (Placing it just before line 672 inside `_run_subprocess_step`
also works and is a smaller blast radius; top-of-`_execute_step` is the more complete edge.)

### 3. Integrating with `result.outcome="halt"` (run loop, executor.py:566-575)

The current halt branch is STRICT-gate-only. Add a precondition branch so a HALT status
caused by a missing input is treated as fatal **regardless of the failed step's own tier**
(the point is the *consumer* cannot proceed):

```python
if step_result.status is PrdStepStatus.HALT and step_result.exit_code == -1 \
        and step_id in _STEP_REQUIRED_INPUTS:
    result.outcome = "halt"
    result.halt_step = step_id
    miss = self._check_input_preconditions(step_id)
    if miss:
        producer, fname = miss[0]
        result.halt_reason = (
            f"upstream artifact '{fname}' missing "
            f"(producer step '{producer}' did not write it); cannot build {step_id}"
        )
    break
```

This sets `result.outcome = "halt"` exactly like the existing STRICT path (570), so Stage B
(578) and present-complete (582) are skipped and the existing finalize/`finally` cleanup
(593-599) runs unchanged. The CLI then renders a structured halt instead of a traceback.

**Why this is the structural fix, not a patch:** the producer-side map already exists; this
adds the missing consumer-side half of the same contract and a single chokepoint that
asserts it. New steps declare their inputs in one table; the guard is automatic. It also
eliminates the prompts.py:257-vs-785 inconsistency *at the level above both* — the builder
is simply never invoked without its inputs, so individual builders no longer each need to
remember a guard.

## Confidence

Self-reported confidence: **0.82**

Root cause and the four citation chains are verified against source. Confidence is not higher
because: (a) the exact integration shape depends on how `result.halt_reason` /
`diagnostics.record_step` render to the CLI (I read the call sites but not the renderer), and
(b) Stage-B steps are dynamic (executor.py:577-579, `_execute_stage_b`) so the
`_STEP_REQUIRED_INPUTS` entries for `web-research`/`synthesis`/`assembly` need confirmation
against the dynamic dispatch, not just the static `_STAGE_A_STEPS` list.

## Comparison vs narrower fixes

**Narrow fix A — halt on any hard ERROR** (relax executor.py:567-569 so ERROR/TIMEOUT halt
regardless of tier):
- *Pro:* ~3 lines; kills this crash and the whole class of "producer died -> consumer reads
  void" because no consumer ever runs after a dead producer.
- *Con:* discards the STANDARD-vs-STRICT design intent. STANDARD exists precisely so a thin
  scope-discovery can degrade and the pipeline continues on a weaker foundation (see the
  `_warn_spec_degradation` path at executor.py:740-741 — the system *wants* to continue here).
  Halting on every ERROR throws that away and makes STANDARD == STRICT for the error case.

**Narrow fix B — per-builder guard** (add `.is_file()` to `_read_file` at prompts.py:257,
matching 785-788):
- *Pro:* 1 line; no traceback.
- *Con:* treats the symptom. The consumer silently proceeds with an empty scope section and
  produces a hollow PRD with **no operator signal** — the worst failure mode (silent
  degradation, which R5 at 736-741 explicitly tries to avoid). And it must be repeated at
  every consumer (257, 340, 440-445, 540); miss one and the class reopens.

**When the systemic precondition gate is worth the extra surface:** when you want to
**preserve the STANDARD/STRICT distinction** (continue on degraded data) *and* still fail
loud and fast specifically when a *required input file* is absent. The gate draws the line
correctly: a STANDARD gate-fail with a written artifact -> continue (intended); a producer
that wrote **nothing** -> halt with a precise message. Narrow fix A cannot make that
distinction (it halts both); narrow fix B makes neither halt (it hides both).

**Over-engineering risk for a V1 CLI (honest):** real. The dependency map is a mini-DAG, and
a V1 has ~15 mostly-linear steps where "halt on hard ERROR" (fix A) gets you 90% of the
safety for 5% of the code. If the team has no near-term plan to let STANDARD steps degrade-
and-continue, **fix A is the right V1 call** and this gate is premature. The gate earns its
keep the moment (1) Stage B's dynamic graph gains real fan-out (multiple consumers of the
same artifact) or (2) the degrade-and-continue behavior at 740-741 is a deliberate product
requirement you must keep. My recommendation: ship **fix A now** as the safety net, and adopt
this gate when the dynamic graph lands — they compose (A is the backstop, the gate is the
precise message).

## Risks

- **Map drift / incompleteness:** a consumer not listed in `_STEP_REQUIRED_INPUTS` is still
  unprotected. Mitigation: derive entries from builder source or add a test asserting every
  builder that calls `_read_file(task_dir / X)` has a matching map entry.
- **Dynamic Stage-B steps** (executor.py:577-579) may not flow through `_execute_step` the
  same way; the check could be bypassed there. Must verify `_execute_stage_b` dispatch.
- **Legit-empty artifacts:** if a producer can legitimately write a zero-byte but present
  file, `.is_file()` passes and the crash class shifts to "empty content," not "missing
  file." The gate handles *missing*, not *empty* — pair with a min-bytes check if needed.
- **Behavior change:** runs that previously limped to a hollow PRD now halt. That is the
  intended improvement, but it is a user-visible behavior change to flag.

## consistency_with_docs

Consistent with project principles: the existing INV-010 comment block (executor.py:709-718)
and the R5 "make silent degradation loud" note (736-741) show the codebase already values
**explicit, loud failure over silent degradation** — this gate extends that ethos to the
missing-input case. It reuses the documented single-source-of-truth `_STEP_ARTIFACT_FILES`
map rather than duplicating filenames, matching the "no drift" discipline emphasized in
CLAUDE.md. No conflict with the STANDARD/STRICT gate model — it operates orthogonally
(input-presence vs output-quality).

## If I'm wrong

If I'm wrong it's probably because the dynamic Stage-B steps don't route through
`_execute_step`/`_run_subprocess_step` the same way Stage-A does, so a top-of-`_execute_step`
check wouldn't actually cover the steps most likely to fan out — meaning the gate guards the
linear spine but not the branchy part that needed it most.
