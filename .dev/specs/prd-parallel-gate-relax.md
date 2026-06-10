---
title: "Relax the brittle parallel-instructions PRD gate to advisory (non-halting)"
status: draft
type: bug-fix / framework-enhancement design spec
created: 2026-06-10
repo: IronbellyOrg/IronClaude
scope: cli/pipeline/models.py + cli/pipeline/gates.py + cli/prd/gates.py + tests
---

# Relax the parallel-instructions PRD gate to advisory

## 1. Summary
`_check_parallel_instructions` is a **STRICT** semantic check on the
`build-task-file` step. It has false-positived **twice** on well-formed
generated task files, each time **HALTing a ~25-minute heavyweight PRD run**.
The check is inherently brittle (heuristic heading detection + literal-keyword
matching) and the cost is asymmetric: a false positive halts a long, expensive
run, whereas the failure it guards against (a task that runs agents serially)
is merely slower, not wrong. **Make this single check advisory** — it logs a
WARNING but never fails the gate — by adding a per-check `advisory` flag to the
gate framework. The two genuinely-valuable checks on the same gate
(`task_phases_present`, `b2_self_contained`) stay STRICT and halting.

## 2. Root cause (evidence)
| Fact | Evidence |
|------|----------|
| The check is a STRICT semantic check on build-task-file | `prd/gates.py:411-438` (`enforcement_tier="STRICT"`, `parallel_instructions` at `:432-436`) |
| STRICT semantic failure halts the run | `prd/executor.py:575,766`; the STRICT loop returns `(False, …)` at `pipeline/gates.py:89-94` |
| FP #1 — flagged the sequential final completion phase (Phase 7) | fixed by PR #154 (completion-phase exemption) |
| FP #2 — flagged "Phase 2": the regex `Phase\s+(\d+)` also matches Task-Log `### Phase N - … Findings` placeholders; after #154 exempted real Phase 7 the loop reached those and tripped on `Phase 2 - Codebase Research Findings` | live run `scp-run`/`prd.candidate.md` task, headings at lines 496-522; empirically `Phase\d:`-anchored regex → PASS, current → HALT |
| The brittleness is open-ended (heading + keyword heuristics) | two distinct detection bugs already; more are plausible |

**Cost asymmetry (the decisive argument):** FP = halt a 25-min run (severe);
FN = generated task parallelizes less than ideal → executor runs some agents
serially → slower, never incorrect (mild). A hard gate inverts this asymmetry.

## 3. Framework facts (verified)
- Semantic checks run **only at STRICT** tier — `pipeline/gates.py:82` (`STANDARD` returns before the semantic loop); `LIGHT`/`EXEMPT` earlier. So demoting the whole `build-task-file` gate to STANDARD would **disable all three** of its semantic checks, including the two we want to keep.
- `gate_passed(...) -> (bool, reason|None)`; STRICT semantic loop at `pipeline/gates.py:85-94` returns `(False, "Semantic check '<name>' failed: <detail>")` on the first non-`True` check.
- `SemanticCheck` = `{name, check_fn, failure_message}` — **no per-check severity** (`models.py:82-88`). `GateCriteria.enforcement_tier` is per-GATE (`models.py:151`).
- `build-task-file` gate bundles `task_phases_present` + `b2_self_contained` (keep STRICT) + `parallel_instructions` (relax) — `prd/gates.py:421-437`.

## 4. Options considered

### Option A — Remove the check
Delete the `parallel_instructions` entry from build-task-file's semantic_checks.
- ➕ Simplest; zero framework change; other two checks stay STRICT.
- ➖ Loses the signal entirely (not even a warning); discards a (small) quality cue.

### Option B — Per-check advisory severity (CHOSEN)
Add `SemanticCheck.advisory: bool = False`; in the STRICT loop, an advisory
check's failure is **logged as a WARNING and skipped** (does not fail the gate).
Mark only `parallel_instructions` advisory.
- ➕ Matches the stated preference (warn, don't halt); keeps the signal.
- ➕ **Robust to ALL detection brittleness** — a wrong advisory warning is
  harmless, so we never have to chase another heading/keyword bug.
- ➕ Reusable: any future check can be marked advisory.
- ➖ A small, careful framework change (model + evaluator + a logger) with tests.

### Option C — Lenient hard gate (require-somewhere + detection fixes)
Keep STRICT; require parallel keywords in only one work phase + add colon/heading
fixes.
- ➖ Still a hard gate → still halts if detection fails on every phase; keeps
  chasing brittleness; does not fix the cost asymmetry.

**Decision: Option B.** It removes the failure *class* (no hard gate can FP-halt
a good run), preserves the signal as a warning, and is reusable — at the price of
a small, well-contained framework change.

## 5. Changes

### 5.1 `src/superclaude/cli/pipeline/models.py`
Add a field to `SemanticCheck` (default preserves all existing behavior):
```python
@dataclass
class SemanticCheck:
    name: str
    check_fn: Callable[[str], bool | str]
    failure_message: str
    advisory: bool = False  # advisory checks WARN but never fail the gate
```

### 5.2 `src/superclaude/cli/pipeline/gates.py`
Add a module logger (if absent) and branch the STRICT semantic loop on `advisory`:
```python
import logging
_log = logging.getLogger("superclaude.pipeline.gates")
...
    if criteria.semantic_checks:
        for check in criteria.semantic_checks:
            result = check.check_fn(content)
            if result is not True:
                detail = result if isinstance(result, str) else check.failure_message
                if getattr(check, "advisory", False):
                    _log.warning(
                        "Advisory gate check '%s' did not pass (non-fatal): %s",
                        check.name, detail,
                    )
                    continue  # advisory: record + proceed, do NOT fail the gate
                return (False, f"Semantic check '{check.name}' failed: {detail}")
```
The `gate_passed` return contract is unchanged (`(True, None)` on pass); advisory
failures surface via the WARNING log so the signal is not silently lost.
*(Optional nice-to-have, not required: also thread a `warnings` list into the
gate result so it lands in `execution-log.jsonl`; deferred — the log line is
sufficient for acceptance.)*

### 5.3 `src/superclaude/cli/prd/gates.py`
- Extend the `_make_semantic_check(...)` factory to accept and forward `advisory: bool = False`.
- Mark only the parallel check advisory in the build-task-file registration:
```python
_make_semantic_check(
    "parallel_instructions",
    _check_parallel_instructions,
    "Later phases missing parallel execution instructions",
    advisory=True,
),
```
`task_phases_present` and `b2_self_contained` are untouched (stay STRICT/halting).

### 5.4 Disposition of prior detection fixes
- **Keep PR #154** (completion-phase exemption) — already merged, harmless, and
  it makes the now-advisory warning fire less spuriously (more signal, less noise).
- **The colon/findings-heading detection fix is NOT needed** under Option B
  (advisory makes detection accuracy non-critical). Do **not** spend a PR on it;
  at most leave a one-line code comment that detection is best-effort because the
  check is advisory.
- `_check_parallel_instructions` itself is **unchanged** by this spec — it stays
  exactly as merged; only its *severity* changes (STRICT→advisory).

## 6. Backward-compat & regression
- Every existing `SemanticCheck` defaults `advisory=False` → identical behavior; only `parallel_instructions` changes severity.
- All other STRICT gates and their checks are unaffected (`gate_passed` contract unchanged).
- `task_phases_present` + `b2_self_contained` still halt build-task-file on failure.

## 7. Test plan (`uv run pytest`)
1. **Advisory check does not fail the gate** (`tests/.../pipeline` or prd gates): a `GateCriteria(enforcement_tier="STRICT")` whose semantic_checks include one `advisory=True` check that returns an error string → `gate_passed(...)` returns `(True, None)`; assert a WARNING was logged (caplog).
2. **Non-advisory check still halts**: same gate with a non-advisory failing check → `(False, "Semantic check … failed: …")`.
3. **Mixed**: advisory-fail + non-advisory-pass → `(True, None)` + warning; advisory-fail + non-advisory-fail → `(False, …)` (the strict one still halts).
4. **build-task-file integration**: run `gate_passed` against the live-repro task file (the one with Task-Log `Phase N - … Findings` headings) → **PASS** (parallel_instructions now advisory; phases/self-contained pass).
5. **Existing `_check_parallel_instructions` unit tests stay green** (the function is unchanged; it's just no longer halting).

## 8. Acceptance criteria
- [ ] `SemanticCheck.advisory` exists; defaults False; all existing gates unchanged.
- [ ] An advisory semantic-check failure logs a WARNING and does NOT fail the gate; a non-advisory failure still does.
- [ ] `parallel_instructions` is the only check marked advisory; the other two build-task-file checks still halt.
- [ ] New + existing tests pass under `uv run pytest tests/cli/prd/ tests/pipeline/`.
- [ ] `make sync-dev && make verify-sync` clean (cli-only → no-op drift guard).
- [ ] The halted heavyweight run advances: `superclaude prd resume build-task-file --product octodive --tier heavyweight --output …` clears build-task-file and proceeds to the next step.

## 9. Out of scope
- Improving `_check_parallel_instructions` detection accuracy (advisory makes it non-critical).
- Threading structured gate warnings into `execution-log.jsonl` (optional follow-up).
- Any change to other gates' tiers or to the STRICT/STANDARD/LIGHT/EXEMPT model.

## 10. Rollout
Edit `src/superclaude/cli/{pipeline/models.py,pipeline/gates.py,prd/gates.py}` →
`make sync-dev` → `make verify-sync` → `uv run pytest tests/cli/prd/ tests/pipeline/` →
single PR on `fix/prd-parallel-gate-advisory` → `IronbellyOrg/IronClaude`.
