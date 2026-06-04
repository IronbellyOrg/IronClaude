# Position B — Strongest alternative: PURE-DETERMINISTIC gate, no LLM in the path

**Claim:** Drop the Haiku sign-off entirely. "Doubly validated" = Signal A (persisted
status) reconciled against Signal B (`_classify_transcript` + checkpoint/deliverable
existence). Disagreement ⇒ suspect ⇒ STOP. No LLM anywhere in the gate verdict path.
(A symmetric extreme — full-LLM-coherence-on-every-resume — is rejected outright: it
puts a non-reproducible judgment on the critical path and is the design's own NFR-3
violation.)

## Why pure-deterministic may be superior

1. **Reproducibility (NFR-3).** The design itself mandates "deterministic core; any
   LLM-judgment step must be isolated, explainable, and overridable." A Haiku call —
   even downgrade-only — makes the gate's verdict *non-reproducible*: the same on-disk
   state can pass on Monday and STOP on Tuesday because Haiku is non-deterministic and
   model-version-dependent. Two operators (or CI vs local) can get different gate
   outcomes on identical inputs. That is a real regression in a gate whose entire
   value is trustworthy, auditable verdicts.

2. **"Coherence" is undefined and unbounded.** The design never specifies what Haiku
   is shown or what rubric it applies. A single bounded call cannot read arbitrarily
   large deliverables; transcripts can be tens of KB. Either the call is truncated
   (judging on partial evidence — worse than no judgment) or it is not actually
   "bounded." Without a concrete prompt/rubric, `test_haiku_signoff_downgrade_only`
   only tests the *plumbing* (mock verdict → downgrade), never the *quality* of the
   judgment, giving false confidence.

3. **The transcript gap undercuts Signal B itself.** When the boundary phase ran via
   the single-process path (no task inventory), there is NO per-task transcript — only
   `phase-N-output.txt` — and `task_results[]` is empty. DD-2's "last-completed task"
   Signal B has nothing per-task to classify, and there is no per-task deliverable for
   Haiku to judge coherence against. The LLM layer adds cost/non-determinism precisely
   where it has the least to work with.

4. **CI fragility.** FR-NFR-4 demands documented non-interactive behavior. A Haiku
   call on every resume adds a `claude`-binary dependency and 30s timeout to the gate.
   In CI without `claude` on PATH, `invoke_sonnet` returns "" — what does an empty
   verdict mean? If "empty ⇒ no downgrade," the LLM layer silently no-ops in CI (so
   why have it?); if "empty ⇒ suspect," CI resumes are blocked by infrastructure
   absence, not by real risk.

5. **Simpler = smaller attack/test surface (R6).** Removing the LLM hook removes a
   whole class of edge cases (timeout, PATH-absence, model drift, prompt injection via
   transcript content) from the gate. The deterministic signals already catch
   over-claim where it is *checkable* (R1's deterministic-first mitigation).

## Concession Position B must answer
Pure-deterministic genuinely cannot detect "file exists, content is wrong." If that
failure mode is common and high-cost, an advisory (flag-only, NEVER gating) coherence
note may be worth it — but it must not change the gate verdict.
