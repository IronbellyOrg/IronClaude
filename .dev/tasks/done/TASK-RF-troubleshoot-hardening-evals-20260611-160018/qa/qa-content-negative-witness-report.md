# QA Report — Negative-Witness Content Verification (OLD=MISS backtest)

**Topic:** troubleshoot-pipeline-hardening — E1–E5 OLD=MISS differential negative witnesses
**Date:** 2026-06-12
**Phase:** task-qualitative (adversarial negative-witness audit)
**Fix cycle:** N/A
**Fix authorization:** false (report-only; no source modified)

---

## Overall Verdict: **PASS**

All 5 OLD=MISS tests are **genuine negative witnesses**. Each observes pre-fix product
logic actually returning the buggy behavior on input the NEW gate would HALT/flag. The
adversarial hypothesis — that ≥3 are vacuous/theatrical — is **REJECTED**: zero vacuous
tests found. The replay genuinely loads PRE-FIX code from the parent tree (proven by
direct subprocess emulation, not assumed).

---

## Suite execution evidence (un-skipped on this full-clone worktree)

`uv run pytest .../test_backtest_e{1..5}.py -v` → **5 passed, 5 skipped in 7.54s**.

- All 5 **OLD=MISS** halves (`*_old_protocol_misses_*`) **PASSED** — they run
  unconditionally because the pre-fix parent commits ARE present locally
  (`missing_replay_commits([...]) == []`; `is_git_worktree() == True`).
- All 5 **NEW=CATCH** halves SKIPPED — guarded by `@requires_impl_ref(...)`; the H1–H4
  refs (`runtime-entrypoint-verification.md`, `unmask-and-sweep.md`,
  `contract-enumeration.md`, `effective-input-proof.md`) are not yet landed. This is the
  designed "un-skips when feat/troubleshoot-pipeline-hardening lands" behavior, NOT a
  defect of the OLD=MISS halves under audit.

---

## Parent-isolation proof (replay loads PRE-FIX code, not the live tree)

This is the load-bearing claim for E1–E4 (which `import superclaude...` in a subprocess).
**Directly emulated** the `run_prefix_replay_snippet` prelude (`sys.path.insert(0, <wt>/src)`
+ purge of inherited `superclaude*` modules) against parent `94d5baa0`:

- `superclaude.cli.prd.process.__file__` resolved to `/tmp/.../wt/src/superclaude/cli/prd/process.py`
  — the **parent worktree path**, NOT the live install
  (`.../troubleshoot-hardening-evals/src/superclaude/__init__.py`).
- `hasattr(PrdClaudeProcess, '_build_file_args') == True` in the subprocess — even though
  `_build_file_args` is **absent in the live tree** (`grep -c` → 0,
  `src/superclaude/cli/prd/process.py`). The only way the symbol exists is by loading the
  parent. **Conclusive.**

Corroborating live-vs-parent deltas (a vacuous "loads-live" replay would invert each verdict):

| Escape | Symbol/text | Live tree | Pre-fix parent | If it loaded LIVE → verdict would be |
|--------|-------------|-----------|----------------|--------------------------------------|
| E1 | `_build_file_args` | absent (0) | present | `AttributeError` → ERROR (it PASSED → parent) |
| E3 | `advisory` in `pipeline/gates.py` | present (1) | absent (0) | WARN/CONTINUE → `halted=False` → FAIL (it PASSED halted → parent) |
| E4 | `advisory` in `_evaluate_gate` | present (5, healed `20693bb8`) | absent (0) | returns True → `halted_despite_advisory=False` → FAIL (it PASSED → parent) |
| E5 | prohibition text | present (1) | absent (0) | `not in text` False → FAIL (it PASSED → parent) |

---

## Per-escape negative-witness verification

### E1 — PASS (genuine). `_build_file_args` emits `--file <local_path>`
Pre-fix `94d5baa0:src/superclaude/cli/prd/process.py` L201–204:
`if base_step in _SPEC_FILE_STEPS: for spec_path in config.spec_files: if Path(spec_path).is_file(): file_args.extend(["--file", spec_path])`.
`_SPEC_FILE_STEPS = frozenset({"scope-discovery", "investigation"})` (L121). The fixture
passes `step_id="scope-discovery"` + a real on-disk `spec_files=[local-spec.md]`, hitting
this branch exactly → argv contains `--file <local_path>`. Test asserts
`emits_local_file` and `"--file" in argv`. The `@staticmethod(config, step_id)` signature
is read live via `inspect.getattr_static` + `__func__` unwrap — matches the parent shape.
**Non-vacuous:** the cloud-only `--file` flag receives a local path, which an argv-only
review accepts as clean. Evidence: `replay_executor.py:200-248`, `test_backtest_e1.py:37-65`.

### E2 — PASS (genuine). `_check_parallel_instructions` false-positive HALT on sequential final phase
Pre-fix `10723863:src/superclaude/cli/prd/gates.py` L37 regex `Phase\s+(\d+)` (digit-only),
L42 `later_phases = [m for m in ... if int(m.group(1)) >= 2]`, L53-55 returns
`f"Phase {phase_num} missing parallel execution instructions ..."`. **Independently
executed the regex** over the fixture: collected phases `['1','2','5']`; later=`['2','5']`;
Phase 2 body has `parallel` (passes), Phase 5 body has no keyword → halt fires on
**Phase 5**, matching the test's `"Phase 5 missing parallel" in observed["result"]`.
**Digit-heading-trap NOT vacuous:** both `Phase 2` and `Phase 5` are concrete digits, so
the `Phase\s+(\d+)` matcher collects them and over-halts (a `Phase N` non-digit heading
would NOT be collected and would yield a vacuous True — the fixture deliberately avoids
this). No `max_phase`/`completion`/final-phase exemption exists at the parent. Evidence:
`test_backtest_e2.py:45-66`, regex re-execution above.

### E3 — PASS (genuine). `gate_passed` hard-HALTs; advisory ignored
Pre-fix `e97aa4fd:src/superclaude/cli/pipeline/gates.py` semantic loop (L67-77) returns
`(False, f"Semantic check '{check.name}' failed: {detail}")` on any non-True check —
**`grep -c "advisory"` on the whole parent file → 0** (no advisory branch). Parent
`SemanticCheck` is a plain `@dataclass` (NOT frozen), so the fixture's
`object.__setattr__(_chk, "advisory", True)` succeeds in *setting* the attr, but
`gate_passed` never reads it → still hard-halts. Test asserts `halted is True` and
`"Semantic check 'parallel_instructions' failed" in reason`. **Non-vacuous:** the advisory
escape-hatch is dynamically applied yet provably ignored. Evidence: `test_backtest_e3.py:43-91`.

### E4 — PASS (genuine). `_evaluate_gate` returns False despite advisory at `1b0264f1`
Pre-fix `1b0264f1:src/superclaude/cli/prd/executor.py` `_evaluate_gate(self, step_id, gate,
content)` semantic loop (L26-35): `for check ...: result = check.check_fn(content); if
result is not True: ... return False`. **`grep -c "advisory"` within `_evaluate_gate` at
parent → 0.** The fixture's stub `self` exposes exactly `_diagnostics.record_gate_failure`
and `_logger.log_gate_result` — the only two attrs the loop touches. `gate.min_lines=0`
skips the `if gate.min_lines > 0` guard (no short-circuit), reaching the semantic loop where
the `advisory=True` failing check is ignored → returns False. Test asserts
`halted_despite_advisory is True`. Pin to parent (NOT HEAD) is correct: HEAD is healed via
`20693bb8` (live `_evaluate_gate` advisory count = 5), so HEAD would not witness the bug.
**Non-vacuous.** Evidence: `test_backtest_e4.py:49-70`.

### E5 — PASS (genuine, carried by assertion 2). `<BASE>..HEAD` wrong-surface selector; prohibition absent
Pre-fix `d878bc6d:src/superclaude/skills/task-builder/SKILL.md` L2195: POST-reflect item
emits `--diff <BASE>..HEAD` (two-dot range; count=1) AND the prohibition
`` Do NOT use `start_commit..HEAD` `` is **absent (count=0)**.

**Adversarial finding (non-blocking — test is still genuine):** assertion 1
(`"<BASE>..HEAD" in text`) does **NOT** discriminate parent from live by itself — the live
(post-fix) SKILL.md L2195 ALSO contains the substring `<BASE>..HEAD`, because the fixed prose
*names the prohibited form* (`Pass <BASE> as a SINGLE ref (NOT <BASE>..HEAD)`). The
**discriminating guard is assertion 2** (`` "Do NOT use `start_commit..HEAD`" not in text ``):
parent=0 → passes; live=1 → would fail. Because the test reads the **checked-out parent
worktree** via `checkout_worktree(d878bc6d)` + `read_source_from_worktree` (verified: parent
worktree prohibition count=0, `<BASE>..HEAD` count=1), assertion 2 holds and the witness is
genuine. **Not vacuous** — but assertion 1 is weak/redundant on its own (see Recommendation).
Evidence: `test_backtest_e5.py:43-64`, live `SKILL.md:2195`.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | E1 pre-fix emits `--file <local_path>` | PASS | `git show 94d5baa0:.../process.py` L201-204; argv branch on `scope-discovery` |
| 2 | E2 pre-fix HALTs on sequential final phase (digit-trap avoided) | PASS | parent gates.py L37/L42/L53; regex re-run → halt on Phase 5 |
| 3 | E3 pre-fix `gate_passed` hard-HALTs, advisory absent | PASS | parent gates.py `grep advisory`=0; loop L67-77 |
| 4 | E4 pre-fix `_evaluate_gate` returns False despite advisory | PASS | parent executor.py L26-35; `grep advisory`=0; min_lines=0 reaches loop |
| 5 | E5 pre-fix uses `<BASE>..HEAD`, prohibition absent | PASS | parent SKILL.md L2195; prohibition count=0 |
| 6 | Replay loads PRE-FIX code (parent tree), not live | PASS | subprocess emulation → `process.__file__` = `/tmp/.../wt/src/...`, `has_bfa=True` |
| 7 | OLD=MISS halves execute (not skip) on full clone | PASS | pytest: 5 passed (OLD) / 5 skipped (NEW refs) |
| 8 | No vacuous trivially-passing assertion | PASS (1 weak sub-assertion) | E5 assertion 1 non-discriminating but assertion 2 carries the witness |

## Summary
- Checks passed: 8 / 8
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (E5 assertion-1 redundancy — does not affect verdict)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | `test_backtest_e5.py:48` | Assertion 1 (`"<BASE>..HEAD" in text`) does not discriminate parent vs live (live post-fix prose also contains `<BASE>..HEAD` as the named-prohibited form). The genuine discrimination is carried solely by assertion 2 (`"Do NOT use \`start_commit..HEAD\`" not in text`). | Optional hardening: tighten assertion 1 to match the *command* form, e.g. assert `--diff <BASE>..HEAD` (with the `--diff ` prefix) is present at parent, which the post-fix command (`--diff <BASE>`) lacks. Not required for correctness — assertion 2 already makes the test non-vacuous. |

## Self-Audit
**(a) Reliance list — structural items relied on (not re-verified):**
- Relied on the test harness's skip-guard/collection structure (rf-qa structural domain); did not re-audit `_impl_guard.py` or `catch_rate.EscapeResult` field shapes.

**(b) Independent semantic checks (≥1 required):**
- Re-read all 5 pre-fix bodies via `git show <parent>:<file>` (E1 process.py, E2/E3 gates.py, E4 executor.py, E5 SKILL.md) — independent of the test's own claims.
- Re-executed the E2 pre-fix regex over the fixture in a standalone interpreter → confirmed halt fires on Phase 5 (not a vacuous True).
- Emulated the `run_prefix_replay_snippet` prelude in a real subprocess → proved `superclaude.cli.prd.process` resolves to the parent worktree path with `_build_file_args` present (absent in live) — parent isolation is real, not assumed.
- Spot-checked the real `checkout_worktree(d878bc6d)` mechanism → parent SKILL.md prohibition count=0, proving E5 reads parent content where assertion 2 discriminates.

**Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 7 | Grep: 0 (via Bash grep) | Glob: 0 | Bash: 7

## Recommendations
- Verdict is **PASS** — all 5 OLD=MISS tests are genuine negative witnesses; proceed.
- Optionally apply the MINOR E5 assertion-1 hardening above to make both E5 assertions
  independently discriminating (defense-in-depth; not blocking).

## QA Complete
