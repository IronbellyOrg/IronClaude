# A.10 + A.10.25 Consolidated Findings — task-integrity gate

**Task file:** TASK-RF-swarm-tui-fr1-regfix-20260619-021719.md
**Gate verdicts:** B2 self-containment = PASS · phase-structure = FAIL (zero-tolerance on cosmetic drift) · research-alignment = PASS
**Resolution:** single serialized fix actor (orchestrator) applies all consolidated fixes (I20). No execution-blocking defect; all fixes are precision/hardening.

## Fixes applied

| # | Source | Sev | Fix |
|---|--------|-----|-----|
| F1 | phase-structure TB-Add-7 | IMPORTANT | `### Source Areas`/`### References`/`### Key Constraints` → canonical `**Source areas:**` / `**References:**` / `**Key constraints:**` bold-label tokens. Substantive invariant already held (all 6 source areas reappear in item Contexts; no file:line in header). |
| F2 | phase-structure #2 | MINOR | DRIFT-1 out-of-scope note: the `commands.py:1880` import is **function-local but unconditional** (runs on every `run_cmd` before the `_tui_active` gate), NOT module-level. Reworded for accuracy. |
| F3 | B2 I-3 | IMPORTANT | Steps 3.4/3.5: `exc_box`/`interrupted`/`result_box` are `run_cmd` locals with no direct injection seam. Restated the concrete monkeypatch mechanism: 3.4 = monkeypatch `dispatch_wave1`→raise (seeds `exc_box`) + `read_state`→`ValueError`; 3.5 = `dispatch_wave1`→raise + a reader→`KeyboardInterrupt` (drives the `except KeyboardInterrupt`→`interrupted=True` path). |
| F4 | alignment GAP-2 | LOW | Step 1.6 + 3.6: noted `test_imm3_parallel.py` + `test_dispatch.py` (injected-executor paths) are UNDER `tests/swarm/`, so Step 3.6's full-suite run already covers any injected-executor-silencing regression. |
| F5 | alignment GAP-3 | LOW | Step 3.1: added the explicit "per-file, non-transitive — documented limitation" clause the research sub-directive required. |

## Not changed (judged adequate)
- B2 I-1/I-2/I-4 (MINOR, last-good seed point / PTY harness choice / --fix-after-summary): left to executor judgment with existing blocker escape hatches; the items remain B2-complete.
- alignment GAP-1 (LOW): Step 1.5 and Step 3.1 already share the literal `if not self.quiet:` guard token; reinforced via F5 wording.
