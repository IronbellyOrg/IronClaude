# QA Report — Final Content Cross-Reference (CROSSREF-CHAIN)

**Topic:** E1–E5 escape_id → §8.3 row → wave → parent sha → OLD=MISS callable → NEW=CATCH ref
**Date:** 2026-06-12
**Phase:** doc-qualitative (adversarial cross-reference audit)
**Fix cycle:** N/A (report-only, `fix_authorization: false` — NO file modified)
**Reviewer stance:** ADVERSARIAL — assumed ≥5 errors in the CROSSREF-CHAIN; hunted, did not confirm.

---

## Overall Verdict: PASS

All five cross-reference chains (E1–E5) are end-to-end intact and internally consistent against the
authoritative RELEASE-SPEC §8.3 (re-read directly, not via research summaries) and against the live git
substrate (every parent SHA + OLD callable re-verified with `git show`/`git cat-file`). Every OLD=MISS
test executes a real-git replay that observes the actual bug at the pinned parent (38 passed, 11 skipped,
0 failed). No test merely NAMES an escape without a semantic oracle.

The "assume ≥5 errors" framing did NOT hold for the CROSSREF-CHAIN: the chain is sound. The candidate
discrepancies I chased (wave-mapping divergence; missing E5 witness text; E4 HEAD-drift) all resolve to
**by-design, spec-faithful** behavior on inspection. Details below so the conclusion is auditable.

---

## Items Reviewed (per-escape chain trace)

| # | Chain link | Result | Evidence |
|---|-----------|--------|----------|
| E1 | E1→H1→`94d5baa0`→`_build_file_args`→runtime-entrypoint-verification.md | PASS | git_replay.py:49 `ReplayEscape("E1","7601ad25","94d5baa0","H1")`; callable at `94d5baa0:cli/prd/process.py:170`; NEW ref read at test_backtest_e1.py:81; §8.3 spec:575 "against H1" |
| E2 | E2→H3→`10723863`→`_check_parallel_instructions`→unmask-and-sweep.md (word-boundary) | PASS | git_replay.py:50; callable at `10723863:cli/prd/gates.py:197`; NEW ref read at test_backtest_e2.py:93; §8.3 spec:576 "against H3 classifier" |
| E3 | E3→H3→`e97aa4fd`→`gate_passed`→unmask-and-sweep.md (sweep) | PASS | git_replay.py:51; callable at `e97aa4fd:cli/pipeline/gates.py:20`; NEW ref read at test_backtest_e3.py:106; §8.3 spec:577 "against H3 unmask/sweep card" |
| E4 | E4→H2→`1b0264f1`→`_evaluate_gate`→contract-enumeration.md | PASS | git_replay.py:52-54 `ReplayEscape("E4","b97c9960","1b0264f1","H2")`; callable at `1b0264f1:cli/prd/executor.py:825`; NEW ref read at test_backtest_e4.py:97; §8.3 spec:578 "with H2 ledger" |
| E5 | E5→H4→`d878bc6d`→SKILL.md POST-reflect selector→effective-input-proof.md | PASS | git_replay.py:55; OLD witness `<BASE>..HEAD` at `d878bc6d:.../task-builder/SKILL.md:2195`; NEW ref read at test_backtest_e5.py:70; §8.3 spec:579 "H4 FAIL closed" |
| X1 | "no test NAMES escape without semantic oracle" | PASS | every OLD test runs a real replay + asserts the bug observable; aggregation parametrizes REPLAY_ESCAPES and asserts CATCH/MISS by ref-presence (see below) |

---

## Summary

- Checks passed: 6 / 6 (5 chains + the no-vacuous-oracle check)
- Checks failed: 0
- Critical issues: 0 | Important: 0 | Minor: 0
- Issues fixed in-place: 0 (report-only)

---

## Per-link verification detail (how each link was proven, not asserted)

### Wave mapping is spec-faithful (the most likely place a planted error would hide)

I re-read RELEASE-SPEC §8.3 **directly** (spec lines 575-579), not via research/05. The §8.3 backtest
rows pin each escape to a SINGLE primary wave:

- E1 backtest → **H1**, E2 → **H3**, E3 → **H3**, E4 → **H2**, E5 → **H4**.

`git_replay.py::REPLAY_ESCAPES` encodes exactly this (E1=H1, E2=H3, E3=H3, E4=H2, E5=H4).

**Trap defused:** spec §3.1 Traceability Matrix (lines 253-257) lists *closing waves* as E1→"H1,H2",
E4→"H1,H2", E5→"H4,H5" — multi-wave. A naive reviewer could flag the harness's single-wave values as
"wrong." They are NOT wrong: §3.1 is closing-waves; §8.3 is the backtest-against-wave. The harness binds
to §8.3 (the backtest contract), which is the correct authority for a backtest runner. The task
assignment's chain uses the §8.3 values. Consistent.

### Git substrate (every parent SHA + OLD callable re-verified at the pinned commit)

- E1 `94d5baa0`: `_build_file_args` present (`process.py:170`), called at `:155`. Fix `7601ad25` removes it.
- E2 `10723863`: `_check_parallel_instructions` present (`gates.py:197`); pre-fix body enforces the
  parallel-keyword rule on EVERY phase ≥2 with a DIGITS-ONLY `Phase\s+(\d+)` matcher. Traced the E2
  fixture (Phase 2 has "parallel"; Phase 5 "Present and complete" has none) → returns
  `"Phase 5 missing parallel execution instructions (...)"`. Runner asserts exactly this string. Valid.
- E3 `e97aa4fd`: `gate_passed(output_file, criteria, *, envelope=None, repo_root=None)` present
  (`gates.py:20`); `SemanticCheck` is a non-frozen `@dataclass` with NO `advisory` field
  (`models.py:81-87`). So the snippet's `object.__setattr__(_chk,"advisory",True)` is settable but the
  parent loop never reads it → hard HALT. Correct OLD=MISS. (E3's callable is the MODULE-LEVEL
  `gate_passed`; the task assignment names `gate_passed` — match.)
- E4 `1b0264f1`: `_evaluate_gate` present (`executor.py:825`). The task assignment correctly maps E4 to
  the SECOND consumer `_evaluate_gate` (E3 is `gate_passed`); the dual-evaluator pair is faithfully split.
- E5 `d878bc6d`: `SKILL.md:2195` POST-reflect item emits `--diff <BASE>..HEAD` (exactly 1 occurrence);
  `start_commit..HEAD` literal = 0; the fix's prohibition string ``Do NOT use `start_commit..HEAD` `` = 0.
  Both runner assertions (witness present, prohibition absent) hold. **Trap defused:** a casual grep for
  `<BASE>..HEAD` over the whole SKILL.md can appear to miss because many unrelated "Do NOT use…" lines
  exist; the precise line is 2195. The witness IS present.

### NEW=CATCH refs map 1:1 to the task assignment + are not vacuous

The 6 hardening refs do NOT exist on this branch (`feat/troubleshoot-hardening-evals`); they land on the
sibling impl branch. So all 5 NEW tests SKIP via `requires_impl_ref(...)` (confirmed: 11 skipped). When
they run, each asserts ≥2 mechanism-specific substrings (not just the escape name):

- E1 runtime-entrypoint-verification.md: `negative witness` + (`--file`|`runtime`|`entrypoint`).
- E2 unmask-and-sweep.md (word-boundary facet): `incomplete`+`complete` + (`word-boundary`|`\b`).
- E3 unmask-and-sweep.md (sweep facet): (`k_swept`|`swept`) + (`warn`|`advisory`|`continue`).
- E4 contract-enumeration.md: `ledger` + (`gate_passed` AND `_evaluate_gate`).
- E5 effective-input-proof.md: `fail-closed` + (`intersection`|`∩`|`effective input`).

E2 and E3 share `unmask-and-sweep.md` but assert DISTINCT facets (word-boundary vs sweep+severity) — the
task assignment calls these out explicitly and the runners honor the split. `_ESCAPE_REFS` in
`test_catch_rate_aggregation.py:40-44` is identical to the per-runner ref map → no aggregation drift.

### No-vacuous-oracle check (task's explicit ask)

- Each OLD=MISS test runs `run_prefix_replay_snippet`/`read_source_from_worktree` against the real pinned
  parent and asserts the bug is OBSERVABLE (argv contains local `--file`; gate returns the halt string;
  `_evaluate_gate` returns `False`; SKILL.md contains the range selector). These are behavioral oracles,
  not name checks. All 5 PASS live (the 5 `.` before each `s` in the run).
- `test_catch_rate_aggregation.py:94-107` parametrizes over `REPLAY_ESCAPES` and asserts
  `verdict == (CATCH if ref_present else MISS)` — a real per-escape verdict, gated on ref existence, never
  a vacuous PASS (the denominator is fixed at the five E1–E5; partial landing derives `partial`, not a
  silent `complete`).
- `json` is injected into every snippet (`replay_executor.py:221` `"import sys, json\n"`), so the bare
  `json.dumps` in each snippet is real — the green is genuine, not an import-error mask.

### Suite state (re-run live, this session)

`uv run pytest tests/troubleshoot/backtest/` → **38 passed, 11 skipped, 0 failed/errored** (10.37s),
matching the final inventory. The 5 OLD halves pass (real replay observed the bug); the 5 NEW halves +
6 aggregation/waiver guards skip (refs absent, by design).

---

## Self-Audit

**(a) Reliance list — items I did NOT re-derive (relied on prior structural QA / inventory):**
- Relied on final-harness-inventory.md for the file/line roster (then independently re-read each runner).
- Relied on the inventory's "38 passed/11 skipped" claim — then independently re-ran the suite to confirm.

**(b) Independent semantic checks (≥1 required, INV-019) — where my own tool work was load-bearing:**
- Wave mapping: re-read RELEASE-SPEC §8.3 directly (`grep -n` spec lines 575-579) rather than trust
  research/05's mapping — confirmed E1=H1/E2=H3/E3=H3/E4=H2/E5=H4 from the spec, then matched against
  `git_replay.py::REPLAY_ESCAPES`. (Research summaries cannot substitute for the spec.)
- Git substrate: `git show <parent>:<file>` for all 5 parents + `git cat-file -e` ancestry — proved each
  OLD callable exists at its pinned parent and each parent commit is present locally.
- E2 oracle: read the FULL pre-fix `_check_parallel_instructions` body at `10723863` and hand-traced the
  E2 fixture through it to confirm the `"Phase 5 missing parallel"` halt string the runner asserts.
- E5 witness: precise `grep -c` for `<BASE>..HEAD` vs `start_commit..HEAD` vs the prohibition string at
  `d878bc6d` — confirmed witness present / prohibition absent (not assumed from the docstring).
- No-vacuous-oracle: read `replay_executor.py` to confirm `json` injection so the live green is real,
  and read `test_catch_rate_aggregation.py:94-107` to confirm the CATCH/MISS verdict is actually asserted.

**Tool engagement:** Read: 9 | Grep (via Bash): 8 | Glob/find: 2 | Bash(pytest+git): 7
**Confidence:** Verified 6/6 chain checks with tool evidence | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%

---

## Notes (NOT defects — by-design observations, surfaced for transparency)

1. **NEW=CATCH is a markdown-ref proxy, never executed gate behavior.** By design (`_impl_guard.py`
   docstring: NEW gate logic is "PURE MARKDOWN… NOTHING importable to probe"). The NEW tests assert ref
   *content*, not gate *behavior*, and skip until the impl branch lands the refs. This is the documented
   architecture, not a chain break — flagged only so the reader knows the NEW half's oracle is a
   ref-substring contract, not a runtime catch.
2. **`10723863` is BOTH E5's fix SHA AND E2's checkout parent** (and `e97aa4fd` is BOTH E2's fix AND E3's
   parent). This interleave is intentional and documented in `git_replay.py:45-47`; per-escape parent
   pinning is precisely why a single shared "BASE" wouldn't work. Internally consistent.

## QA Complete
