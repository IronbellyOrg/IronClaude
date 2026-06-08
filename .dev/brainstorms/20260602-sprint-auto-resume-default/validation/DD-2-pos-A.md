# Position A — DD-2 as designed: deterministic-first + downgrade-only Haiku sign-off

**Claim:** The resume-boundary "doubly validated" gate should run a deterministic
reconciliation first (Signal A = persisted `task_results[].status` from
`phase-N-result.json`; Signal B = `_classify_transcript()` over the task transcript
AND checkpoint/deliverable existence via `_verify_checkpoints` logic). Only when the
deterministic layer says VALIDATED does a single bounded Haiku coherence call run on
the last-completed task — and it may only DOWNGRADE to suspect, never upgrade a
deterministic suspect.

## Why this is the right design

1. **Determinism owns the verdict.** The gate's pass/fail is fully reproducible from
   on-disk artifacts. Haiku is a strictly subtractive safety net, so a flaky/absent
   LLM can only make the gate *more* conservative (STOP), never wrongly *resume*.
   That is the safe failure direction for a non-idempotent pipeline.

2. **Cheap and precedented.** `invoke_sonnet` (summarizer.py:305) already shells
   `claude --print --model <m>` with a 30s timeout and returns "" on any failure
   (never raises). Haiku is already invoked per-phase in the executor
   (executor.py:1173) and in the retrospective. One bounded Haiku call on the single
   last-completed task at resume time is negligible cost (~1-3s, ~$0.001) against a
   multi-minute phase re-run.

3. **Catches the over-claim seam (R1).** A task whose `status==pass` and whose
   transcript classifies PASS but whose *deliverable content is incoherent* (wrote a
   file but it's empty/garbage/wrong-target) is exactly the failure deterministic
   existence checks miss. Coherence = "do the declared deliverables substantively
   satisfy the task's stated intent." A targeted read is precisely what an LLM is
   good at and a hash/existence check is not.

4. **Downgrade-only is loop-safe.** A Haiku false-positive downgrade produces a STOP
   with a report, not a silent retry. The operator resolves with `--start`/`--fresh`/
   `accept_suspect`. There is no automatic re-validation loop in the design — the gate
   runs once per resume invocation, so "infinite loop" is structurally impossible.
