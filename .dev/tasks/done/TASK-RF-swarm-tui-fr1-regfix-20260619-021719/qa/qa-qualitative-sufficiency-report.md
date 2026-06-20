# QA Report — task-qualitative (verification-sufficiency lens)

**Topic:** swarm --tui FR-1 REG-1 + DRIFT-2/3/4 corrective code-remediation
**Date:** 2026-06-19
**Phase:** task-qualitative
**Lens:** verification-sufficiency
**Fix authorization:** false (report-only)
**Fix cycle:** N/A

---

## Framing acknowledgement

This is a CODE-REMEDIATION task built `QA_GATE_REQUIREMENTS: NONE` BY DESIGN.
The "≥6 rf-qa agents per gate" rule is N/A here — verification is deterministic
test/lint execution + an executor-disjoint POST reflect gate. The sufficiency
lens asks: would the task's verification net actually CATCH a regression of
each fix (REG-1, DRIFT-2/3/4)?

---

---

## Overall Verdict: PASS

The verification net is ADEQUATE to catch a regression of every fix this task
makes (REG-1, DRIFT-2, DRIFT-3, DRIFT-4). Each fix has at least one verification
item that would FAIL pre-fix and PASS post-fix, and the deterministic surface
(ruff check + ruff format --check repo-wide + full `tests/swarm/` suite) plus the
executor-disjoint POST reflect gate together close the holes that let REG-1 ship
green originally. No coverage hole was found where a regression of REG-1/DRIFT-3/
DRIFT-4 could occur while all verification still passes green.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | REG-1 net catches BOTH co-causes (redirect + worker print) | none | PASS | Step 3.1 audit extension flags unguarded `print(`/stdout writes on parallel.py+dispatch.py (test_inv012:600-643 visitor verified extendable); Step 3.3 real-PTY smoke asserts crash-ABSENCE under concurrent worker stdout — distinct from existing PTY test (test_inv012:558 asserts ANSI-PRESENCE only, terminates proc → cannot catch a crash). Step 3.2 mutation guard proves detector ≠ no-op. The two co-causes are covered by complementary structural (audit) + runtime (PTY) checks. |
| 2 | Existing PTY test provably CANNOT catch REG-1 (justifies new smoke) | none | PASS | test_inv012:520-563: `proc.terminate()` masks exit code; assertion is `_ANSI_CSI_RE.search(payload) is not None` only — a worker render-crash leaves ANSI bytes present + terminate hides nonzero exit → green. Confirms Step 3.3's new crash-absence smoke is non-duplicative and necessary. |
| 3 | Frozen-signature tripwire re-run (Step 1.7) | none | PASS | test_run_tui_integration:666-674 pins `__init__`==`["self","max_workers"]`,default 10. A `quiet` CLASS attr (Step 1.4) does not enter the sig; a `quiet=` kwarg would. Step 1.7 re-runs `test_frozen_signatures_unchanged` after Phase-1 edits as a tripwire. Drift to a kwarg is caught. |
| 4 | DRIFT-3 regression test fails pre-fix / passes post-fix (Step 3.4) | none | PASS | Seam verified live: `_dispatch_worker` (commands.py:1904-1918) captures `dispatch_wave1` exceptions into `exc_box`; readers at 1944-1947 are OUTSIDE the try(1956)/except-KeyboardInterrupt(1969). Pre-fix a reader `ValueError` (read_state raises per state.py:178-184) escapes past finally and NEVER reaches the exc_box re-raise at 1990. Existing `test_fr5...` (line 290-311) already proves the `dispatch_wave1`→`_boom` + `_tail_events` monkeypatch (line 483) seams work. Test would surface ValueError pre-fix, worker exc post-fix. |
| 5 | DRIFT-4 regression test fails pre-fix / passes post-fix (Step 3.5) | none | PASS | Precedence inversion confirmed live: `if interrupted: raise Exit(130)` (1984-1986) BEFORE `if "e" in exc_box: raise exc_box["e"]` (1990-1991). SIGINT seam exists: `_update_raises_kbd` monkeypatch on `TUI.update` (test:437-441) drives `interrupted=True`. Pre-fix Exit(130) masks; post-fix reorder surfaces worker exc. Genuine pre/post differential. |
| 6 | FR-6 SIGINT-only invariant protected from false-positive break | none | PASS | Existing `test_fr6_stop_runs_on_all_three_exit_paths` (test:365-450) asserts SIGINT-only → exit 130 (line 443). Step 2.2 reorder leaves the SIGINT-only path (no exc_box["e"]) still reaching Exit(130); Step 3.5 explicitly leaves the FR-6 invariant to the existing test. Guards scoped to `Exception` (not BaseException) per FR-6 — KeyboardInterrupt still propagates (commands.py:1958-1962 pattern matched). |
| 7 | CI parity — BOTH ruff check AND ruff format --check repo-wide (Steps 4.1/4.2) | none | PASS | CI runs them as SEPARATE steps: quick-check.yml:37,41 + test.yml:133,137. `make lint`=ruff check only (Makefile:50). Step 4.1 `ruff check src/ tests/` + Step 4.2 `ruff format --check src/ tests/` match CI exactly. Memory `make_lint_vs_ci_ruff_format` corroborated. |
| 8 | Executor-disjoint POST reflect gate present, FLAT, exit-consumed, penultimate (Step 4.5) | none | PASS | `superclaude reflect run --depth deep --fix --promote` surface verified: reflect/commands.py:102(--depth),299(--promote),140(--base exists but task forbids it). Recursion-breaker `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` real (commands.py:44, runner.py:53). Exit-code consumption (0=pass;10/11/2=fail/degraded) with benign exit-11 caveat matches memory `reflect_exit11_degraded_benign`. Penultimate (only 4.6 status→Done follows). |
| 9 | Step 1.5 print-gating scope correct (no over/under reach) | none | PASS | ParallelExecutor class prints at parallel.py:110,111,164,165,176,177,183,191,196-200,225,232 (verified exact); module-level convenience prints at 331,334,336 are OUTSIDE class — Step 1.5 correctly leaves them. dispatch.py:424 is SOLE swarm construction (340 is param default). Non-swarm callers (execution/__init__.py:108,200) keep prints via quiet=False default. |
| 10 | Step 3.6 covers injected-executor paths (no silent break from quiet flip) | none | PASS | test_imm3_parallel.py + test_dispatch.py have NO capsys/capfd/readouterr stdout assertions → flipping `executor.quiet=True` on injected instances cannot break them. Step 3.6 runs full `tests/swarm/` so they execute. Research 01 line 90 claim verified. |
| 11 | Audit guard-awareness adequately specified (guarded prints not flagged) | none | PASS | Step 3.1 requires the detector to treat `print` reachable only under `if not self.quiet:` as guarded (research 03 option (a)). This needs ancestor tracking in the AST walk — non-trivial but the task acknowledges it and Step 3.2's mutation guard tests BOTH the unguarded-flagged AND guarded-not-flagged cases, making the requirement falsifiable. See MINOR note M-1. |

---

## Summary
- Checks passed: 11 / 11
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (advisory, non-blocking — see M-1)
- Issues fixed in-place: 0 (fix_authorization: false)

**Confidence:** Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 7 | Grep/Bash: 6 | Glob: 0 (Bash-driven greps used instead)

---

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| M-1 | MINOR (advisory) | Step 3.1 (test_inv012 audit visitor) | The "guarded by `if not self.quiet:`" detection requires AST ancestor/parent tracking (`ast.NodeVisitor` is flat by default). The task acknowledges this and the Step 3.2 mutation guard tests both polarities, so it is falsifiable — but the executor should not under-implement to a substring check. | No task change required. Advisory: the executor must implement true guard-context tracking (e.g. walk `If` test for `not self.quiet`, or track enclosing-If stack), and Step 3.2's guarded-not-flagged assertion will catch a substring shortcut. This is already encoded as a Step 3.2 assertion, so the net self-protects. |

**Note on M-1:** This is NOT a verification-net hole. The mutation guard (Step 3.2) explicitly asserts the guarded case is NOT flagged AND the unguarded case IS flagged, so a wrong implementation (flat substring, or over-flagging guarded prints) fails Step 3.2 or Step 3.6 (the gated parallel.py prints would be falsely flagged → audit fails). The net catches its own mis-build. Recorded as advisory only; it does not warrant a FAIL.

---

## Adversarial Axis Sweep (AX-1..AX-5)
- **AX-1 Drift:** No GOAL-verbatim drift. The task verbs are unconditional ("assert", "must FAIL pre-fix"). Cited line numbers were checked against live source — all current (poll loop 1943-1995, visitor 600-643, frozen-sig 666-674, PTY 477, parallel prints 110-232, dispatch 424). No stale citations. The task itself defends against drift with "re-locate by searching for X because line numbers may have shifted" on every Read. TRACK GOAL verbatim was provided in the spawn prompt, so AX-1 is ACTIVE and fired no findings.
- **AX-2 Contradictions:** None. The frozen-sig constraint (class-attr, not kwarg) is consistently stated in research 01, the task constraints block, Steps 1.4/1.7. No item asserts a fact another contradicts.
- **AX-3 Omissions:** No omitted touchpoint. All ParallelExecutor callers accounted for; both reader calls guarded; both precedence branches reordered; injected-executor regression covered (3.6); CI format parity covered (4.2); independent gate present (4.5). The one acknowledged out-of-scope item (DRIFT-1 eager import) is explicitly deferred with rationale, not silently dropped.
- **AX-4 Weakened criteria:** None. Acceptance phrasing is unconditional where the source demands it: "assert the WORKER exception reaches the caller — not the ValueError, not a clean exit"; "would FAIL against pre-fix … PASS against post-fix"; PTY smoke "asserts on the ABSENCE of a crash". No "may"/"if applicable" softening on load-bearing assertions. Step 3.6 explicitly forbids weakening an assertion to make a test pass.
- **AX-5 Invented content:** None. Every named artifact (dispatch_wave1, _dispatch_worker, exc_box, read_state, _tail_events, _TuiSymbolVisitor, test_frozen_signatures_unchanged, pty.openpty idiom, SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE, _TUI_POLL_MAX_ITERATIONS) exists in the live codebase or research files and was grep/Read-verified.

---

## Self-Audit (PR-04 / INV-019 reliance audit)

**(a) Reliance list — inherited-PASS items I relied on (skipped structural re-check):**
- Relied on rf-qa A.10 PASS for B2 self-containment — did NOT re-verify item self-containment structure.
- Relied on rf-qa A.10.25 PASS for Phase-structure — did NOT re-verify phase numbering/ordering as a structural gate.
- Relied on rf-qa PASS for Research-alignment (structural) — did NOT re-verify the research-file cross-reference table format.

**(b) Independent semantic checks (≥1 required, INV-019) — where structural PASS was insufficient and my own reading was required:**
- **Verification ADEQUACY of the REG-1 net** — structural PASS only confirms the items exist and are well-formed; it does NOT confirm the existing PTY test cannot catch REG-1. I Read test_inv012:520-563 and found `proc.terminate()` + ANSI-only assertion → proved the existing test is crash-blind, which is the entire justification for Step 3.3. Tool evidence: Read test_inv012_tui_opt_in.py:430-563.
- **DRIFT-3/DRIFT-4 pre-fix/post-fix differential** — structural PASS cannot tell whether a regression test would actually fail pre-fix. I Read commands.py:1895-1995 and traced that a reader ValueError escapes past the finally and never reaches the exc_box re-raise (DRIFT-3), and that interrupted precedes exc_box (DRIFT-4). I cross-checked the injection seam against the already-passing `test_fr5...` (test:290-311) and the SIGINT seam (`_update_raises_kbd`, test:437-441). Tool evidence: Read commands.py:1895-1995 + test_run_tui_integration.py:280-450.
- **CI parity literal** — structural PASS does not verify the CI actually runs `ruff format --check` separately. I grepped .github/workflows and confirmed quick-check.yml:41 + test.yml:137. Tool evidence: Bash grep over .github/workflows + Makefile.

---

## Recommendations
- **PROCEED.** The verification net is sufficient for a ~4-file surgical fix. No CRITICAL/IMPORTANT issues.
- Carry M-1 forward as an executor advisory only (the Step 3.2 mutation guard already self-protects against a substring-shortcut audit implementation).
- No web research was required for this review (all checks are local-file-bound); Tavily-first policy not triggered.

## QA Complete

---

VERDICT: PASS
