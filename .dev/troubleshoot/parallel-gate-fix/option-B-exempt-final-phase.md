# Option B — Exempt the final (completion) phase; check every work phase before it

## The change
`src/superclaude/cli/prd/gates.py:197-227`
```python
# Check phases 2..(N-1): every WORK phase must show parallel intent;
# the final phase is the sequential completion/presentation phase (anti-orphaning).
numbered = [(int(m.group(1)), m) for m in phase_sections]
if not numbered:
    return True
max_phase = max(n for n, _ in numbered)
later_phases = [m for n, m in numbered if n >= 2 and n < max_phase]  # exempt final
```
(Update the docstring to say "every work phase ≥2, excluding the final
completion phase, must contain parallel keywords.")

Optional sub-variant **B′ (require-somewhere)**: instead of "every work phase",
require parallel keywords in **at least one** phase ≥2 — weaker, but immune to
any single sequential work phase.

## Rationale
The false positive is **structural**: by MDTM/anti-orphaning convention the
final phase is always sequential completion (present to user → summary → mark
Done). Parallelism is inapplicable there *by design*. The gate's true intent is
"the **work** phases should leverage parallel execution," so the fix targets the
actual invariant rather than a positional proxy.

## Strengths
- **Fixes the whole bug class, not one instance.** Works for any task length —
  4 phases, 7 phases, 12 phases — because it keys on "final phase," which is
  always the completion phase.
- **Correct for the live evidence.** Checks phases **2–6** (all PARALLEL work
  phases — investigation, gates, web-research, synthesis, assembly → all pass)
  and exempts only **Phase 7** (sequential completion). No false positive AND no
  false negative; A cannot achieve both here.
- **Semantically honest** — the rule now means what it says; no magic number.
- **Robust final-phase detection** — `max(phase_number)` is deterministic and
  template-agnostic.

## Weaknesses / risks
- **Larger diff** (a few lines vs one), so marginally more review surface.
- **Assumes the final phase is the completion phase.** True for the PRD task
  template (Phase N = "Present & Complete"), but a malformed task that put real
  parallel work in its last phase would be exempted. Mitigated: such a task
  violates anti-orphaning anyway (a separate, already-enforced rule).
- **B′ weakens the gate** — "require-somewhere" lets a task with only one
  parallel phase pass. Use plain B (per-work-phase) unless that strictness is
  unwanted.
- Slightly more logic = marginally more to test (final-phase exemption +
  per-work-phase enforcement).

## Edge cases
- Task with 4 phases (completion = Phase 4): checks 2–3, exempts 4 → **correct**.
- Task with 8 work phases + completion: checks 2–8, exempts 9 → **correct, full coverage**.
- This task (7 phases): checks 2–6 (all pass), exempts 7 → **correct, no FN**.
- Single-phase or no-phase task: `not numbered`/`max==1` → returns True (no later phases).
