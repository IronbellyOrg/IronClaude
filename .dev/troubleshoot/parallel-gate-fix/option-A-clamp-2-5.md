# Option A — Clamp the check to the documented range (phases 2–5)

## The change
`src/superclaude/cli/prd/gates.py:212`
```python
# before
later_phases = [m for m in phase_sections if int(m.group(1)) >= 2]
# after
later_phases = [m for m in phase_sections if 2 <= int(m.group(1)) <= 5]
```

## Rationale
Make the code match its own docstring (`"Check that phases 2-5 contain parallel
execution keywords."`). The function name and docstring already declare the
intended range; the `>= 2` predicate is simply a coding error against that
stated intent. Smallest possible diff — one comparison.

## Strengths
- **Minimal, surgical** — a single bounded-range edit; trivially reviewable.
- **Faithful to documented intent** — removes a code/docstring contradiction
  rather than introducing new behavior.
- **Deterministic, no heuristic** — a fixed numeric window; nothing to mis-detect.
- **No new failure modes** — cannot mis-identify a "final phase"; there is no
  phase-classification logic to get wrong.

## Weaknesses / risks
- **Positional, not semantic.** The cutoff `5` is arbitrary. The false positive
  is caused by *completion phases being sequential*, not by *phase number > 5*.
  Clamping the range only *coincidentally* fixes the current case (completion =
  Phase 7).
- **Under-covers real work phases.** Evidence from the live run: the generated
  task's PARALLEL work phases run **2 through 6** (Phase 6 = "Assembly &
  Validation", lens + fidelity QA gates, parallel). Clamping to 2–5 **stops
  checking Phase 6** — a legitimate work phase the gate *should* enforce. So A
  buys a false-positive fix at the cost of a **false-negative** on Phase 6.
- **Does not fix the bug class.** A shorter task whose completion phase is
  Phase 4 or 5 would *still* false-positive (the completion phase falls inside
  2–5). A longer task with work phases 6–8 would escape the check entirely.
- **Leaves a latent landmine.** The next person who reads "phases 2-5" still has
  no idea *why* 5 — the magic number encodes an unstated assumption ("tasks have
  ≤5 work phases then a completion phase") that the heavyweight template already
  violates.

## Edge cases
- Task with 4 phases (completion = Phase 4): **still false-positives** (not fixed).
- Task with 8 work phases: phases 6–8 silently unchecked (**false negative**).
- This task (7 phases, work 2–6): fixes Phase 7 FP **but introduces** a Phase 6 FN.
