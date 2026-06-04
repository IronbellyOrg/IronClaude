---
fixture: retry_loop_no_terminal_case
failure_class: retry_contract
contract: 7
master_recurrence_row: 9
---

# Recurrence #9 — Retry Without Input Mutation (futile-by-construction retry)

> **Documented incident** (master:§Recurrence Matrix row #9):
> *"Retry without input mutation — identical prompt re-run produces identical
> output, exhausts retry budget."*
> Partition findings: `A1b:F-A1b-006`, `A11:F-A11-017`, `A12:F-A12-02`.

## What happened

`v2.24-cli-portify` halted at `spec-fidelity` after exhausting its 2-attempt
retry budget producing **identical output**, because the retry re-ran the same
prompt against an **unchanged `roadmap.md`** (`A1b:F-A1b-006`). The retry could
never converge: nothing about the input changed between attempts, so the
deterministic portion of the step produced byte-identical output each time and
the gate failed identically. This single incident drove the entire v5 pipeline
redesign (the `deviation-analysis` + `remediate` steps with the 4-class
taxonomy).

The same shape recurred as the `A12:F-A12-02` D-family flatline (58 → 54 → 54
HIGH findings over 3 runs): once structural progress stalled, additional runs
re-ran identical inputs and burned budget without moving the needle.

## The anti-pattern (pre-fix)

A pipeline step that is **deterministic** (no LLM call — the output is a pure
function of its inputs) but is configured with `retry_limit > 0` and whose
inputs are NOT mutated between attempts. Re-running it is futile by
construction:

```python
# ANTI-PATTERN — deterministic step that retries identical input.
Step(
    id="spec-fidelity",
    prompt="",            # deterministic: output is f(inputs), inputs unchanged
    output_file=spec_fidelity_file,
    gate=SPEC_FIDELITY_GATE,
    timeout_seconds=600,
    inputs=[spec_file, roadmap_file],   # never rewritten between attempts
    retry_limit=2,        # <-- futile: attempt 2 == attempt 1, byte-identical
)
```

## The invariant (post-fix — Contract #7)

A retry site MUST satisfy at least one of:

1. **Input mutation between attempts** — the retried step is non-deterministic
   (an LLM / tool-write step whose re-invocation yields new output) OR a
   remediation step that rewrites its input before the next attempt (so the
   `content_hash` / `envelope.findings` count differs between attempts); OR
2. **`retry_reason: transient_failure_only`** annotation — the retry is
   explicitly scoped to transient (I/O, timeout, rate-limit) failures, not to
   re-attempting a structurally-identical computation.

A **deterministic** step (`prompt=""`, non-LLM) configured with
`retry_limit > 0` and lacking the transient annotation is the Contract #7
violation. Post-fix, every deterministic roadmap step carries `retry_limit=0`
(convergence/remediation handles progress via genuine input mutation under a
bounded `max_runs`, not via identical-input retries).
