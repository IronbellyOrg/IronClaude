# Recommendation — gate fix for `_check_parallel_instructions`

## Verdict: **Option B (exempt the final phase), framed as "exempt both bookends"** — convergence 0.90, margin 51 pts.

This is a **decision, not a merge** (the two approaches are mutually exclusive). B wins decisively; the one virtue of A (minimal, low-mechanical-risk diff) is grafted in as an implementation constraint, not a competing design.

## Why B, not A
1. **A doesn't fix the bug class.** It only fixes cases where the completion phase number is > 5. A 4- or 5-phase task whose final phase is Phase 4/5 *still* false-positives. The defect is *"the final phase is sequential,"* not *"phase number > 5."*
2. **A introduces a false negative on the live run.** Clamping to 2–5 stops checking **Phase 6** ("Assembly & Validation"), a legitimate parallel work phase. A passes the gate by *dropping a check it should keep*.
3. **A encodes a convention the system already violates.** The pipeline's own heavyweight template generates work phases 2→**6**. Any positional cutoff at 5 is empirically wrong for this codebase's actual output.
4. **B is consistent with what the gate already does.** The gate exempts Phase 1 (setup) by starting at `>= 2`. B exempts the other bookend (the completion phase). *Exempt setup + completion; enforce the middle.* One coherent rule, true to the function's purpose.
5. **Tie on the only thing A wins:** both options immediately unblock this run (INV-001 sufficiency check — phases 2–6 all carry parallel keywords, so both return `True`). So "A is smaller" buys nothing on unblocking and costs correctness everywhere else.

## Recommended implementation (B, kept minimal per A's one virtue)
`src/superclaude/cli/prd/gates.py` — `_check_parallel_instructions`:
- Compute `max_phase = max(captured phase integers)`.
- Work set = phases with `2 <= n < max_phase` (exempt setup *and* the final completion phase).
- Keep the existing early-return (`if not phase_sections / not work_phases: return True`) and the **byte-exact error message** (`"Phase {n} missing parallel execution instructions (expected one of: ...)"`) so nothing downstream shifts.
- Update the docstring to: *"work phases (2..N-1) must contain parallel keywords; the setup (Phase 1) and final completion phase are exempt."*

```python
def _check_parallel_instructions(content: str) -> bool | str:
    """Work phases (2..N-1) must contain parallel execution keywords.

    Phase 1 (setup) and the final phase (sequential completion/presentation,
    per anti-orphaning) are exempt; parallelism applies only to the middle
    work phases.
    """
    parallel_keywords = ["parallel", "concurrent", "simultaneously", "batch"]
    phase_sections = list(re.finditer(r"(?:^|\n)\s*#{1,4}\s+.*Phase\s+(\d+)", content, re.IGNORECASE))
    if not phase_sections:
        return True
    max_phase = max(int(m.group(1)) for m in phase_sections)
    work = [m for m in phase_sections if 2 <= int(m.group(1)) < max_phase]
    if not work:
        return True
    order = sorted(phase_sections, key=lambda m: m.start())
    for m in work:
        i = order.index(m)
        start = m.end()
        end = order[i + 1].start() if i + 1 < len(order) else len(content)
        if not any(kw in content[start:end].lower() for kw in parallel_keywords):
            n = m.group(1)
            return (f"Phase {n} missing parallel execution instructions "
                    f"(expected one of: {', '.join(parallel_keywords)})")
    return True
```

## Tests to add (matching the existing gates test style)
- 7-phase task, work 2–6 parallel, sequential Phase 7 → **PASS** (the live repro; today it FAILS).
- 4-phase task, parallel 2–3, sequential Phase 4 (completion) → **PASS** (proves the short-task FP that A leaves is fixed).
- 5-phase task with a sequential **work** Phase 3 (no keyword) → **FAIL on Phase 3** (proves work-phase enforcement is preserved — guards against the require-somewhere weakening).
- ≤2-phase task → **PASS** (no intervening work phases; degenerate-case guard).

## Note on the rejected sub-variant B′ (require-somewhere)
B′ ("require a parallel keyword in *at least one* phase ≥2") was considered and **rejected**: it would pass a task where only Phase 2 is parallel and 3–6 silently went sequential — defeating the gate's purpose. Plain B (per-work-phase enforcement) is strictly stronger.

## Out of scope (pre-existing, do not bundle here)
The keyword-matching heuristic itself (A-002) — prose containing "parallel" ≠ actual parallel execution — is a separate, pre-existing gate limitation neither option changes.

## Next step
Implement B on a `fix/prd-parallel-gate-final-phase-exempt` branch in IronClaude → `make sync-dev`/`verify-sync` (cli-only → no-op drift guard) → add the 4 tests → `uv run pytest tests/cli/prd/` → then `superclaude prd resume build-task-file …` to continue the halted PRD run.
