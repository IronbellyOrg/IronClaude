# QA Report — Final Content / Actionability (Non-Vacuity)

**Topic:** troubleshoot-hardening-evals backtest harness — OLD=MISS witnesses, NEW=CATCH proxies, waiver invariant
**Date:** 2026-06-12
**Phase:** task-qualitative (final content / actionability gate)
**Fix authorization:** false (report-only; NO file modified)

---

## Overall Verdict: PASS (with 1 MINOR caveat on E5 — non-vacuous, but one of E5's two OLD assertions is non-discriminating)

Top-line binary: **PASS**. Every OLD=MISS test is a real, load-bearing negative witness (proven by
differential replay against the post-fix/HEAD trees). Every NEW=CATCH proxy asserts documented-mechanism
tokens via `read_text()`, skip-guarded on its own specific ref. The waiver test asserts a real verdict-state
invariant. Nothing anywhere is `assert True` / `assert 1` / a pass-through.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | OLD=MISS are REAL negative witnesses (pre-fix callable returns buggy behavior, loaded via sys.path→worktree-src) | PASS (E5 MINOR) | Differential replay below: each snippet behaves differently pre-fix vs post-fix/HEAD |
| 2 | NEW=CATCH proxies assert DOCUMENTED mechanism (substantive read_text token asserts), skip-guarded on specific ref | PASS | All 14 proxy asserts inspected; each `@requires_impl_ref("<distinct>.md")` + AND-anchored tokens |
| 3 | Waiver test asserts a real verdict-state invariant (single guarded test by design) | PASS | `test_waiver_regreen.py:36-50` asserts waiver_status latch + {blocked,advisory} + success_with_hardening_* |
| 4 | Nothing is `assert True` / `assert 1` / pass-through | PASS | grep clean across whole `tests/troubleshoot/backtest/` |

## Summary

- Checks passed: 4 / 4
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (E5 first assertion non-discriminating)

---

## Item 1 — OLD=MISS real negative witnesses (DIFFERENTIAL PROOF)

Each OLD test's trailing `assert result.verdict == VERDICT_MISS and result.negative_witness is True` IS
tautological (it re-asserts the literals just passed to `EscapeResult(...)`). That line is decorative. The
**load-bearing** assertions are the EARLIER `assert observed[...]` checks driven by the real pre-fix callable
replayed in a fresh subprocess whose `sys.path[0]` is the worktree's `src/` (replay_executor.py:218-233, prelude
purges inherited `superclaude` modules). I proved each earlier assertion is load-bearing by replaying the SAME
snippet against the post-fix / HEAD tree:

- **E1** (`test_backtest_e1.py:60-65`, load-bearing `assert observed["emits_local_file"] is True` + `assert "--file" in argv`):
  pre-fix parent `94d5baa0` → PASS. Same snippet against **post-fix `7601ad25`** → `PrefixReplayError`:
  `AttributeError: _build_file_args` (method removed by fix). Witness real and load-bearing.
- **E2** (`test_backtest_e2.py:72-78`, `assert observed["halted"] is True` + `assert "Phase 5 missing parallel" in result`):
  pre-fix `10723863` → `halted: True`. Against **post-fix `e97aa4fd`** → `halted: False, result: True`
  (final-phase exemption lands). Real differential. Digit-heading trap (docstring L9-14) verified: fixture uses
  concrete-digit `## Phase 2` / `## Phase 5: Present Results`, so the pre-fix `Phase \d+` matcher collects them.
- **E3** (`test_backtest_e3.py:84-91`, `assert observed["halted"] is True` + `assert "Semantic check 'parallel_instructions' failed" in reason`):
  pre-fix `e97aa4fd` → halted. Against **post-fix `eb9a2633`** → `halted: False, ok: True` (advisory branch
  honors the dynamically-tagged check). Real differential.
- **E4** (`test_backtest_e4.py:78-82`, `assert observed["halted_despite_advisory"] is True`):
  pre-fix parent `1b0264f1` → halt-despite-advisory True. Against **HEAD** (healed via 20693bb8) the snippet
  RAISES `AttributeError: 'SimpleNamespace' has no attribute 'name'` at `executor.py:867` — HEAD's healed
  `_evaluate_gate` reaches the advisory-logging path the pre-fix code never reached. Confirms HEAD-DRIFT is real
  and the replay is correctly PINNED to the pre-fix parent, NOT HEAD. Witness real and parent-specific.
- **E5** (`test_backtest_e5.py:43-55`, source-text witness on checked-out parent tree): see MINOR below. The
  load-bearing witness is `assert "Do NOT use \`start_commit..HEAD\`" not in text` — prohibition count is
  **0 @ pre-fix `d878bc6d`** vs **1 @ post-fix `10723863`**. Real differential.

Full-suite confirmation: `uv run pytest tests/troubleshoot/backtest/` → **38 passed, 11 skipped** (matches
final-harness-inventory.md:44). The 5 OLD=MISS run + pass; the 6 NEW/waiver proxies SKIP (refs absent).

## Item 2 — NEW=CATCH proxies (documented mechanism, specific-ref skip-guard)

All hardening refs ABSENT under `src/superclaude/skills/sc-troubleshoot-protocol/refs/` today (confirmed via
`ls` — only the 8 pre-existing troubleshoot refs are present), so all 6 proxy/waiver tests SKIP. The skip is
keyed to the SPECIFIC ref per proxy via `_impl_guard.requires_impl_ref(<filename>)` (`_impl_guard.py:43-57`,
`skipif(not ref_path.exists())` — never importorskip / xfail / try-except). Each proxy then does
`read_text(encoding="utf-8")` + substantive token asserts mapping 1:1 to research/05 §(d):

- E1 `runtime-entrypoint-verification.md`: `"negative witness"` AND (`--file`/`runtime`/`entrypoint`)
- E2 `unmask-and-sweep.md` (word-boundary facet): (`incomplete` AND `complete`) + (`word-boundary`/`\b`)
- E3 `unmask-and-sweep.md` (sweep facet): (`k_swept`/`swept`) + (`warn`/`advisory`/`continue`)
- E4 `contract-enumeration.md`: `ledger` + (`gate_passed` AND `_evaluate_gate`)
- E5 `effective-input-proof.md`: (`fail-closed`/`fail closed`) + (`intersection`/`∩`/`effective input`)

E2/E3 sharing `unmask-and-sweep.md` but asserting DISTINCT facets is by design (docstrings L17 / L13-14). No
proxy assertion is satisfiable by the ref FILENAME alone — each requires content tokens. Not no-ops.

## Item 3 — Waiver test (real verdict-state invariant)

`test_waiver_regreen.py:26-50`, guarded `@requires_impl_ref("hardening-output-contract.md")` (a `_FOUNDATION_REF`,
`_impl_guard.py:28`). Asserts three real one-way-latch invariants on the contract ref: (1) `waiver_status` AND
`latch` present (none→latched); (2) `blocked` AND `advisory` present (latch forces verdict); (3)
`success_with_hardening_blocker` OR `success_with_hardening_advisory` (no downstream re-green to plain success).
Single-guarded-test shape is correct and complete by design (docstring L1-18: forward state-machine invariant on
the impl surface, no pre-fix commit to replay, excluded from the `total_escapes == 5` catch_rate arithmetic).
Distinct function name avoids nodeid collision with the impl suite's `test_waiver_latch_one_way`.

## Item 4 — No vacuous assertions

`grep -rn 'assert True\|assert 1\b\|assert 1$'` over `tests/troubleshoot/backtest/` → none. Bare `pass` in test
bodies → none. The only tautological lines are the decorative trailing `EscapeResult`-echo asserts in E1-E4,
which are NOT the load-bearing checks (Item 1 proves the earlier `observed[...]` asserts carry the witness).

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `test_backtest_e5.py:48` | `assert "<BASE>..HEAD" in text` is NON-discriminating: `<BASE>..HEAD` appears in BOTH pre-fix `d878bc6d` (as the diff selector) AND post-fix `10723863` (inside the NEW prohibition sentence "Pass `<BASE>` as a SINGLE ref (NOT `<BASE>..HEAD`)"). So this assertion alone does not distinguish buggy from fixed — only the SECOND assertion (`"Do NOT use \`start_commit..HEAD\`" not in text`, prohibition 0 pre-fix vs 1 post-fix) is the load-bearing differential. The docstring (L8-10) frames the presence of `<BASE>..HEAD` as the escape, which is imprecise. NOT vacuous (the literal could be absent) and the test DOES correctly discriminate via assert 2, so non-blocking. | Either tighten assert 1 to the pre-fix-only form (e.g. assert the selector appears as the actual `--diff` action, not inside a prohibition), or annotate that assert 2 is the load-bearing witness and assert 1 is a coarse presence smoke-check. |

## Actions Taken

None — report-only (`fix_authorization: false`). No file modified.

---

## Self-Audit

**(a) Reliance list — items relied upon without re-deriving from scratch:**
- Relied on final-harness-inventory.md's 38/11 suite-state claim → independently re-ran the suite (38 passed,
  11 skipped) rather than trusting the inventory.
- Relied on research/05 §(d) for the documented NEW=CATCH mechanism token set → independently cross-checked
  each proxy assertion's tokens against §(d).

**(b) Independent semantic checks (≥1 required):**
- Item 1 load-bearing proof: replayed each E1-E4 snippet against the POST-FIX/HEAD tree
  (`run_prefix_replay_snippet` from a one-off script) and observed the witness flip/raise — tool evidence:
  E1→AttributeError `_build_file_args`; E2→`halted: False`; E3→`ok: True`; E4 @ HEAD→AttributeError at
  `executor.py:867`. This is the check the anti-inflation rule exists for: the trailing asserts LOOK
  tautological, and only independent differential replay proves the witness is real.
- Item 1 E5: `git show <parent>:SKILL.md` vs `git show <fix>:SKILL.md` token counts (prohibition 0 vs 1;
  `<BASE>..HEAD` 1 vs 1) → surfaced the MINOR that the inventory/docstring did not flag.

## Tool engagement

Read: 9 | Grep: 6 | Glob: 0 | Bash: 8 (incl. 3 live differential replays + 1 full-suite run)

Confidence: Verified 4/4 | Unverifiable 0 | Unchecked 0 | Confidence: 100%

## QA Complete
