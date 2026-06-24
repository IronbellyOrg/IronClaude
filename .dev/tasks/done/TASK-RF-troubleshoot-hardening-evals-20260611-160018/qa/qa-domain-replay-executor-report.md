# QA Report — Domain Review: ReplayExecutor Seam vs LifecycleExecutor Intent

**Topic:** ReplayExecutor (tests/troubleshoot/backtest/replay_executor.py) mirror-fidelity to LifecycleExecutor (src/superclaude/cli/eval/runner.py)
**Date:** 2026-06-12
**Phase:** doc-qualitative (adapted: domain/seam-fidelity review)
**Fix cycle:** N/A (report-only, fix_authorization: false)
**Stance:** ADVERSARIAL — assumed ≥3 divergences; hunted for them.

---

## Overall Verdict: PASS

All four DOMAIN concerns are satisfied by the source. The adversarial hunt surfaced
candidate divergences (runtime_checkable asymmetry, ERROR-token contract, the
HEAD-vs-parent `_build_file_args` mismatch, the zero-consumer state of the module),
but on verification each is either (a) a deliberate, correctly-reasoned design choice,
or (b) a non-defect for the stated single-seam contract. None rises to a FAIL of the
four enumerated concerns. The divergences are recorded below as MINOR observations,
not gating failures.

---

## Items Reviewed
| # | Concern | Result | Evidence |
|---|---------|--------|----------|
| 1 | ReplayExecutor is a `typing.Protocol` spawn→observe seam (injectable stub-point) mirroring LifecycleExecutor (runner.py:136-156) | PASS | replay_executor.py:77-88 `@runtime_checkable class ReplayExecutor(Protocol)` with single `replay(escape, worktree) -> ReplayResult` method; runner.py:136 `class LifecycleExecutor(Protocol)`. Both are stdlib `typing.Protocol`. InProcessReplayExecutor (replay_executor.py:162-190) is the default impl; docstring (82-83) states "Tests substitute a stub that records the call." Seam is injectable via `invokers` Mapping (173). |
| 2 | Invokes in-process callables, not a literal Claude PTY/pexpect (NFR-3 single-seam bound) | PASS | replay_executor.py:7-10 + 184 `return invoker(escape, Path(worktree))` — pure in-process call. No `pexpect`/`PtyDriver`/`subprocess` import in replay_executor.py (verified by import scan: only importlib/inspect/dataclasses/pathlib/typing). Module docstring 8 explicitly: "NOT a literal Claude PTY -- per NFR-3's single-seam bound." Aligns with research/01:162-167 (PtyDriver NOT needed; mirror the driver *seam*). |
| 3 | ReplayResult is a frozen dataclass mirroring ObservedRun (runner.py:109-133) | PASS | replay_executor.py:43-58 `@dataclass(frozen=True) class ReplayResult`; runner.py:109 `@dataclass(frozen=True) class ObservedRun`. Both frozen. Field shapes differ by domain (4 vs 6 fields) — correct per research/01:129 ("MIRROR → ReplayResult … the captured output of replaying a commit"); a verbatim field copy would be wrong (escape verdict ≠ subprocess exit_code). |
| 4 | Invocation path is signature-ADAPTIVE (reads real pre-fix signature via inspect/resolve_callable); no hardcoded call signature for class-bound (E1/E4) vs module-level (E2/E3) | PASS | replay_executor.py:118-155 `resolve_callable` reads `inspect.signature` from the checked-out object (134, 146); unwraps staticmethod/classmethod descriptors (132 `getattr(target, "__func__", target)`); `is_class_bound` flag (141/152) distinguishes E1/E4 from E2/E3. Default executor delegates to per-escape `invokers` (173,184) rather than hardcoding a shape. VERIFIED against real commits below. |

---

## Signature-adaptivity verification (concern #4 — the load-bearing claim)

The strongest adversarial test: does the design's "read the signature from the
checked-out tree, owning-class names are only guidance" caveat (replay_executor.py:12-22)
actually hold against the real pre-fix-parent commits? Verified each E1-E4 callable at
its pinned `prefix_parent_sha` from git_replay.py:48-56:

| Escape | Parent sha | Callable | Real binding at parent | Concern-4 claim holds? |
|--------|-----------|----------|------------------------|------------------------|
| E1 | 94d5baa0 | `PrdClaudeProcess._build_file_args` | `@staticmethod (config, step_id)` — class-bound but **NO self** | YES — `git show 94d5baa0:.../process.py` line 168-170 confirms `@staticmethod`. A hardcoded `self`-bound call WOULD break here. The `inspect`-driven path + staticmethod unwrap (replay_executor.py:131-132) is REQUIRED, not optional. |
| E2 | 10723863 | `_check_parallel_instructions` | module-level `def (content)` | YES — `git grep … 10723863` → gates.py:197 module-level. |
| E3 | e97aa4fd | `gate_passed` | module-level `def` | YES — `git grep … e97aa4fd` → pipeline/gates.py:20 module-level. |
| E4 | 1b0264f1 | `PrdExecutor._evaluate_gate` | class-bound instance method (`self, step_id, gate, content`) | YES — `git grep … 1b0264f1` → executor.py:480 class / 825 method. |

**This is the key positive finding.** At **HEAD**, `_build_file_args` does NOT exist on
`PrdClaudeProcess` at all (GAP-003 replaced `--file` delivery with inline prompt content;
`grep _build_file_args src/` returns only the replay_executor docstring). If the seam
resolved against HEAD or hardcoded a signature, E1 would be unrunnable. Because
`resolve_callable` reads from the **checked-out worktree** (replay_executor.py:118-125,
matching read_source_from_worktree/load_module_from_worktree at 91-115), it adapts to the
pre-fix `@staticmethod (config, step_id)` shape. Concern #4 is not just nominally
satisfied — it is *necessary* and the code earns it.

---

## Summary
- Concerns passed: 4 / 4
- Concerns failed: 0
- Critical issues: 0
- MINOR observations (non-gating): 3

## Issues Found
| # | Severity | Location | Issue | Note |
|---|----------|----------|-------|------|
| 1 | MINOR (non-gating) | replay_executor.py:77 vs runner.py:136 | `runtime_checkable` ASYMMETRY: ReplayExecutor is `@runtime_checkable`; LifecycleExecutor is a plain `Protocol` (not decorated). This is a divergence from the mirrored intent, but a *strengthening* one (enables `isinstance` stub checks) and does not violate concern #1 ("is a typing.Protocol seam"). Both remain structural Protocols. Not a FAIL. |
| 2 | MINOR (non-gating) | replay_executor.py:38-40, 50, 168-190 vs catch_rate.py:79-94 | VERDICT_ERROR contract seam: ReplayResult carries a 3rd verdict token `ERROR` (40) that `EscapeResult.__post_init__` (catch_rate.py:85-88) REJECTS (only {CATCH,MISS}). The replay_executor docstring (36-37,50) correctly labels ERROR an "executor-internal sentinel … never a legitimate catch-rate verdict," so the boundary is documented — but no code currently maps ReplayResult→EscapeResult (zero consumers, see #3), so the ERROR-must-be-filtered-before-EscapeResult obligation is asserted in prose only and untested. Latent integration risk for the Phase-4 per-escape runners, NOT a defect in the four reviewed concerns. |
| 3 | MINOR (non-gating) | whole module | ZERO CONSUMERS: `grep -rn` across src/ + tests/ finds no import of `replay_executor`, `InProcessReplayExecutor`, `resolve_callable`, or `ReplayResult` outside the module itself, and there is no `test_replay_executor*.py` (sibling tests exist for git_replay, catch_rate, backtest_status). The seam is defined but not yet wired or unit-tested. This matches the module's own intent (it documents "per-escape Phase 4 runners supply these") so it is a not-yet-integrated state, not a divergence from LifecycleExecutor intent. Flagged for honesty per adversarial mandate. |

## Adversarial hunt log (claims I tried to break and could not)
- **"Owning-class names are wrong/misleading"** → FALSE; verified all four bindings at the real parent shas. The caveat that names are "guidance, actual signature may differ" is itself vindicated by E1's staticmethod.
- **"ReplayResult should mirror ObservedRun's 6 fields verbatim"** → FALSE; research/01:129 mandates a domain re-shape, not a field copy. Frozen-dataclass mirroring (the load-bearing property) holds.
- **"Seam secretly spawns a PTY/subprocess"** → FALSE; import scan clean, invocation is `invoker(escape, worktree)` in-process only.
- **"Hardcoded call signature somewhere"** → FALSE; `resolve_callable` + injected `invokers` is the only call path; `inspect.signature` read at 134/146.

## Self-Audit
**(a) Reliance list — structural items skipped for re-check:** None. No inherited
structural verdict was supplied; this was a standalone domain review. I independently
verified every claim with tool engagement (no reliance).

**(b) Independent semantic checks (≥1 required, INV-019):**
- Concern #4 signature-adaptivity verified by `git show`/`git grep` at four distinct
  pre-fix parent commits (94d5baa0, 10723863, e97aa4fd, 1b0264f1) — confirmed E1 is a
  `@staticmethod` and absent at HEAD, proving the inspect-driven path is necessary.
- Concern #2 PTY-absence verified by scanning replay_executor.py imports (no pexpect/
  subprocess/PtyDriver) — not merely trusting the docstring.
- Cross-module contract (#2 of Issues) verified by reading catch_rate.py:85-88
  `EscapeResult.__post_init__` and confirming the ERROR token is rejected there.

### Self-Audit answers
1. Independently verified claims against source: 8 (4 concerns + 4 escape bindings at
   real commits) plus 2 cross-module contracts.
2. Files read/grepped: replay_executor.py, runner.py, git_replay.py, catch_rate.py,
   research/01; `git show`/`git grep` on process.py/gates.py/executor.py/pipeline-gates.py
   at four parent shas; directory listing of tests/troubleshoot/backtest/.
3. Why trust the PASS: the verdict is not "looked fine" — the one concern that could
   silently rot (signature-adaptivity) was tested against real historical commits and
   shown to be *necessary*, and three honest non-gating divergences are documented rather
   than suppressed.
4. Web research: none performed (all verification was local-file / git-bound). Tavily
   not required this review.

## Confidence
Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 4 | Grep/Bash: 5 | Glob: 0

## Recommendations
- (For Phase-4 wiring, not gating now) Add a `test_replay_executor.py` that (a) asserts
  a stub satisfies the `@runtime_checkable` ReplayExecutor, (b) exercises `resolve_callable`
  against a staticmethod and a module-level fn to lock the E1-vs-E2 shape split, and
  (c) asserts the ERROR→EscapeResult filter at the integration boundary (Issue #2).
- Consider noting in the module docstring that LifecycleExecutor is NOT runtime_checkable,
  so the asymmetry (Issue #1) is intentional rather than accidental drift.

## QA Complete
