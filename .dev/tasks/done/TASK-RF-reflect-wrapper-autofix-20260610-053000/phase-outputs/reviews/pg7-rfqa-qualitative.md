# QA Report — Operational Review (PG7, rf-qa-qualitative)

**Topic:** reflect-wrapper AUTO-FIX evolution — end-to-end state-machine + invocation operational review
**Date:** 2026-06-10
**Phase:** report-qualitative (operational lens; adversarial stance)
**Fix cycle:** N/A (report-only; fixed nothing)
**Stance:** ADVERSARIAL — assumed defects existed; traced real code + ran CliRunner/pytest to confirm.

---

## Overall Verdict: PASS

The end-to-end state machine behaves per §1 when traced through the real code (not just the
conformance table's claims). O1/O2 invocation shapes parse and route correctly. The
human-decision-halt invariant is honored end-to-end through three layers of defense. The recursion
is bounded under BOTH the marker (nested gate) AND `--max-fix-iterations` (outer loop).

Two observations are recorded below (one spec-prose-vs-implementation reconciliation already
acknowledged by the conformance report; one cross-component generator obligation already carried as
a Follow-Up). Neither is a code defect. No CRITICAL/IMPORTANT/MINOR issues found in the wrapper code.

---

## Q1 — Does the END-TO-END state machine actually behave per §1?

Traced through real code, all four terminal paths confirmed:

**clean → promote/exit 0.** `runner.run` loop: `_audit_once()` → `derive_verdict` returns
`Verdict.PASS` only when `status == "success" AND tier_reached == expected_tier`
(contract.py:235). Loop breaks (runner.py:539-540). `fix_converged = True`. Promotion itself is NOT
performed by the wrapper — it is reflect's Wave-7, invoked by emitting the `/sc:reflect` prompt
WITHOUT `--no-promote` (runner.py:345-347). Verified via `--print-command`: O1 prompt omits
`--no-promote` (promote-by-default honored). Exit code 0 via `Verdict.PASS.exit_code` (models.py:44).
CONFORMS.

**drift-only → auto-fix → re-verify → exit 0.** `derive_verdict` → HALTED `reason="drift"`
(contract.py:327); runner loop classifies `classify_fix` → `auto-fixable` (contract.py:364),
reads `remediation_task_path`, calls `_apply_remediation` (`/task <path>` as a SECOND top-level
`ClaudeProcess`), increments iteration, re-audits. On a subsequent PASS → exit 0.
EMPIRICALLY CONFIRMED: `test_convergence_exit0_three_launches` PASSES — 2 audits + 1 apply = 3
launches, `fix_converged=True`, `fix_iterations=1`, exit 0. CONFORMS.

**human-required → exit 10, no promote.** See Q3 — confirmed end-to-end. CONFORMS.

**non-convergence → exit 10.** After `max` apply→verify cycles without PASS, terminal HALT.
EMPIRICALLY CONFIRMED: `test_non_convergence_exit10_five_launches` PASSES — with
`--max-fix-iterations 2`: 3 audits + 2 applies = 5 launches, ends HALTED exit 10,
`fix_converged=False`, sidecar `fix_converged: false`. CONFORMS.

Additional fail-closed paths verified in source + suite: DEGRADED/BLOCKED carrying `drift>0` are
NEVER auto-fixed (runner.py:547 `if result.verdict is not Verdict.HALTED: break`;
`test_degraded_with_drift_never_autofixed`, `test_blocked_with_drift_never_autofixed` PASS); a
failed `/task` apply (rc!=0) does NOT re-audit and stays HALTED, never PASS (runner.py:562-571;
`test_failed_apply_fails_closed_no_reaudit` PASS); a missing `remediation_task_path` on an
auto-fixable verdict → terminal HALT, no apply (runner.py:554-556;
`test_cannot_repair_absent_path_halts_no_apply` PASS).

## Q2 — Do the O1 and O2 invocation shapes parse and route correctly?

Ran the real Click parser via `CliRunner` against a real git-repo tasklist with `--print-command`:

**O1** `reflect run <file> --depth deep --fix --promote` → exit 0. Emitted prompt:
`/sc:reflect --mode post --diff <start_commit_sha> --tasklist <abs> --depth deep --remediate
--output ...`. Note: NO `--no-promote` (promote default honored), `--remediate` PRESENT (because
`--fix`), `--diff` is a SINGLE ref (de-ranged). CONFORMS to contract §2 O1.

**O2** `reflect run <file> --depth deep --fix --no-promote --base deadbeef` → exit 0. Emitted prompt:
`/sc:reflect --mode post --no-promote --diff deadbeef ... --depth deep --remediate ...`.
`--no-promote` flows through; `--base deadbeef` OVERRIDES frontmatter `start_commit` (`--diff
deadbeef`, not the start_commit sha) — precedence chain confirmed (config.py:97-105). CONFORMS to
contract §2 O2.

**Forbidden flags rejected at parse:** `--reflect auto` → exit 2 `No such option '--reflect'`;
`--max-turns 100` → exit 2 `No such option '--max-turns'`. CONFORMS to contract §2 forbidden set.

## Q3 — Is feedback_human_decision_items_must_halt honored end-to-end?

YES — confirmed through three independent defensive layers, traced and executed:

1. **Hard-signal precedence over drift (classify_fix, contract.py:356-363).** Probed
   `drift>0` co-occurring with each of `needs_human_decision` / `user_decision_required` /
   `unauthorized_deviation_present` / `regression_present` / `regression>0` — ALL classify
   `human-required` (hard signal wins; drift never overrides). Pure `drift`/`necessary` →
   `auto-fixable`; clean → `none`.

2. **derive_verdict routes hard signals to HALTED before classify is consulted**
   (contract.py:315-322). Executed: complete trustworthy contract with `needs_human_decision: True`
   + `drift:3` → HALTED `reason="needs-human-decision"` exit 10 → `classify_fix` → `human-required`
   → runner loop breaks at runner.py:551-552 with NO `_apply_remediation` call, NO promote.

3. **F2 malformed-bool fail-closed guard (contract.py:200-209).** Adversarial probe: a STRING
   `needs_human_decision: "true"` (not a real bool) with `drift:3` — in the pure classifier this
   would falsely classify `auto-fixable` (a bypass), BUT `derive_verdict` routes it to BLOCKED
   `reason="malformed-contract-boolean"` exit 2 BEFORE the classifier is ever reached. The runner
   only calls `classify_fix` on a `Verdict.HALTED` result, so the malformed signal can never reach
   the auto-fix path. No auto-applied default can ship a human-decision change. HONORED.

## Q4 — Is the recursion bounded under BOTH the marker AND max-fix-iterations?

YES — dual independent bounds confirmed (NFR-3):

**Marker (nested gate, FR-2 / contract §3).** The group-callback guard (commands.py:69) reads
`SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` and `sys.exit(0)` when EXACTLY `"1"`, BEFORE Click's
`exists=True` path validation and before any audit. The marker is exported `=="1"` into BOTH child
launches: the audit `ClaudeProcess` (runner.py:416) AND the apply `/task` `ClaudeProcess`
(runner.py:448). So the auto-run remediation tasklist's OWN terminal gate self-suppresses → the
outer wrapper owns the real re-verification → no wrapper↔remediation recursion.
EMPIRICALLY CONFIRMED: `test_marker_suppression.py` (5 tests) PASS, incl. negative controls proving
ONLY `"1"` suppresses (`"0"`/absent/`"2"` run normally — F2 too-loose-truthiness defense).

**max-fix-iterations (outer loop, FR-3 / D3).** Hand-traced the loop bound for N=1,2,3: for max=N,
exactly N+1 audits + N applies, then a hard `break` at `if iteration > max_iters` (runner.py:558).
Deterministic termination; matches the conformance arithmetic (N=1→3 launches, N=2→5 launches) and
NFR-2 cost band. Even if PASS is never reached and a remediation path is always present, the loop
cannot run unbounded.

The two bounds are orthogonal and jointly total: the marker kills any nested gate regardless of
loop count; the iteration bound kills a non-converging outer loop regardless of nesting.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | clean→promote→exit0 | PASS | runner.py:539-540, models.py:44; `--print-command` O1 omits --no-promote; `test_convergence` |
| 2 | drift→autofix→reverify→exit0 | PASS | runner.py:536-572; `test_convergence_exit0_three_launches` (3 launches, exit 0) |
| 3 | human-required→exit10-no-promote | PASS | contract.py:315-322,356-363; executed end-to-end trace; `test_human_required_halts_no_apply` |
| 4 | non-convergence→exit10 | PASS | runner.py:558; `test_non_convergence_exit10_five_launches` (5 launches, exit 10, converged:false) |
| 5 | O1 shape parse/route | PASS | CliRunner --print-command: exit 0, prompt omits --no-promote, --remediate present, single-ref --diff |
| 6 | O2 shape parse/route | PASS | CliRunner: exit 0, --no-promote flows, --base overrides start_commit |
| 7 | forbidden flags rejected | PASS | `--reflect`/`--max-turns` both exit 2 at parse |
| 8 | human-decision-halt invariant | PASS | 3-layer defense executed; F2 malformed-bool→BLOCKED before classify |
| 9 | marker nested-gate bound | PASS | commands.py:69 guard; markers at runner.py:416,448; `test_marker_suppression` (5) |
| 10 | max-fix-iterations outer bound | PASS | runner.py:558; hand-traced N=1,2,3 → (N+1) audits + N applies then break |
| 11 | DEGRADED/BLOCKED never autofixed | PASS | runner.py:547; `test_degraded_with_drift`/`test_blocked_with_drift` |
| 12 | failed-apply fail-closed | PASS | runner.py:562-571; `test_failed_apply_fails_closed_no_reaudit` |
| 13 | thinness (no sprint/roadmap/async; only ClaudeProcess) | PASS | grep: NONE for imports/async; `test_no_nesting_guard` |

## Summary
- Checks passed: 13 / 13
- Checks failed: 0
- Critical issues: 0
- Confidence: Verified 13/13 | Unverifiable 0 | Unchecked 0 | Confidence: 100.0%
- Tool engagement: Read: 8 | Grep/Bash: 7 (pytest suite, CliRunner traces, classifier probes, derive_verdict probes, loop-bound trace, thinness greps)

## Issues Found
None in wrapper code.

## Observations (non-blocking; not code defects)

1. **Spec-prose vs implementation reconciliation (already acknowledged by conformance §5).**
   merged-requirements §1/FR-5 prose says "O2: the wrapper **forces** `--no-promote`." The
   implementation does NOT force it — the wrapper has no O1/O2 concept; it honors the
   `--promote/--no-promote` it is given (commands.py:90-94). The AUTHORITATIVE contract §5 correctly
   states the GENERATOR emits `--no-promote (REQUIRED)` for O2. Implementation matches the binding
   contract; the merged-requirements wording is loose. Deliberate thinness decision (no O2-detection
   in the wrapper). Conformance report row §5 already resolves this in favor of the contract. NOT a
   defect.

2. **`--base` range-form is a generator obligation, not a wrapper rejection (carried as Follow-Up).**
   The wrapper stores `--base` verbatim as a single ref and never SPLITS a `..` into a range (F3
   de-range invariant). A generator that wrongly emitted `--base aaa..bbb` would have it passed
   through verbatim as `--diff aaa..bbb` (confirmed via --print-command). Contract §2 makes "no
   `..` range" a GENERATOR MUST-NOT; the wrapper-side de-range guarantee is "never construct a
   range," which holds. This is the wrapper↔generator integration-gate item already listed in the
   conformance GAP analysis. NOT a wrapper defect.

## Self-Audit
1. Factual claims independently verified against source: 13 checks, each tied to file:line +
   either a passing test, a CliRunner trace, or an executed probe.
2. Files read: commands.py, runner.py, contract.py, config.py, models.py, test_fix_loop.py,
   test_marker_suppression.py, test_no_nesting_guard.py, test_promote_plumbing.py + the spec,
   contract, and conformance report.
3. Why trust this with 0 wrapper-code issues: I ran the full reflect suite (75 passed, 1 justified
   xfail), drove the real Click parser with CliRunner for O1/O2/forbidden-flags, executed the
   classifier and `derive_verdict` against adversarial malformed-bool and co-occurring-signal
   inputs (the human-decision-halt bypass attempt was the sharpest probe — it is defended by F2),
   and hand-traced the loop bound for three N values. The 1 xfail is generator-side content (NFR-5
   decouple), not wrapper code.
4. No web research was required (all verification was local-file + CLI-bound). Tavily not invoked.

## QA Complete
