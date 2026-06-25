# QA Report — Research Gate (Gap-Detection Lens)

**Topic:** Differential backtest harness under tests/troubleshoot/backtest/ replaying E1-E5 (OLD=MISS vs NEW-gate=CATCH)
**Date:** 2026-06-11
**Phase:** research-gate
**Lens:** gap-detection
**Fix authorization:** false (report-only)
**Fix cycle:** N/A

---

## Adversarial Stance

Assume the research contains gaps that would block or weaken the builder. Verdict of 0 issues requires cited evidence of exhaustive coverage checking.

---

## Files Reviewed (8 total)

| File | Read | Status claimed | Notes |
|------|------|----------------|-------|
| research-notes.md (scope map) | YES (86 lines) | n/a | EXISTING_FILES, GAPS, 7 researcher assignments |
| 01-eval-framework-inventory.md | YES (header + reuse verdict) | Complete | mirror-shape vs import-reuse verdicts |
| 02-test-patterns-and-xfail.md | YES (full) | Complete | xfail/skip conventions, schema-test idiom, pollution guard |
| 03-git-replay-helpers.md | YES (full) | Complete | worktree roundtrip verified live; **SHA-semantics contradiction (see G1)** |
| 04-spec-contract-deepdive.md | YES (full) | Complete | backtest_status contract; **E4 base-commit nuance RESOLVED** |
| 05-replay-targets.md | YES (full) | Complete | per-escape OLD=MISS/NEW=CATCH 1:1 to §8.3 |
| 06-impl-tasklist-crossref.md | YES (full) | Complete | NEW=CATCH = pure-markdown proxy; collision boundary enumerated |
| 07-mdtm-template-and-report-model.md | YES (full) | Complete | CatchRateReport model; schema fidelity test; partial+missing-IDs |

---

## Probe-by-Probe Findings

### Probe 1 — Mechanically-assertable OLD=MISS per E1-E5 — COVERED (strong)
R5 §(b)/(c) gives, per escape, the buggy pre-fix function, the file, and the concrete OLD observable:
- E1: `prd/process.py::_build_file_args` emits `--file <local_path>`; argv-only pre-fix tests accept it.
- E2: `prd/gates.py::_check_parallel_instructions` returns the "Phase N missing parallel..." failure string on a sequential completion phase.
- E3: `pipeline/gates.py::gate_passed` returns `(False, "Semantic check 'parallel_instructions' failed...")` on Task-Log placeholder headings (no advisory severity).
- E4: `prd/executor.py::_evaluate_gate` returns `False` despite `advisory` flag.
- E5: `task-builder/SKILL.md` POST-reflect emits `--diff start_commit..HEAD` → audits none of uncommitted work.
R4 §4.1 CODE-VERIFIES the E4 substrate symbols at file:line. Each maps 1:1 to §8.3. **No gap.**

### Probe 2 — NEW=CATCH vacuity risk — COVERED, and the risk is EXPLICITLY surfaced (strong)
This was the highest-risk probe. R6 §B resolves it decisively and honestly: the NEW gate is **pure-markdown** (no importable Python; the skill dir is `SKILL.md` + `refs/` only — verified on disk). R6 explicitly states the NEW=CATCH half can only be a **documentation-presence proxy** asserting the catch mechanism is documented in the impl's NEW refs, and flags that this is "effectively a redundant cross-validating proxy." The research does NOT oversell it. R6 §E.5 instructs the builder not to duplicate the impl's own `test_hardening_*` modules. This means the OLD=MISS half (which runs green now) carries the real differential weight; the NEW=CATCH half is correctly framed as a guarded doc-presence check until the refs land. **Not a gap — the weakness is named and bounded.** (Residual: see OBS-1 below.)

### Probe 3 — E4 ambiguity (HEAD healed via 20693bb8) — COVERED (strong; independently re-verified)
R4 §4.2 + §6 item 11 fully resolve this. I independently re-verified with git:
- `20693bb8` IS an ancestor of HEAD; `b97c9960` is NOT (confirmed).
- At parent `1b0264f1`, `executor.py::_evaluate_gate` has ZERO `advisory` references (buggy state confirmed).
- Both `b97c9960` and `20693bb8` share parent `1b0264f1`, so checking out `1b0264f1` yields the buggy state regardless of which fix commit is named.
R5's harness table pins the E4 checkout target as `1b0264f1` — correct and unambiguous. R4 additionally warns the builder NOT to expect current HEAD to exhibit the bug. **No gap; the ambiguity is pinned.**

### Probe 5 — backtest_status derivation (partial + missing IDs; separation from verdict) — COVERED (strong)
R4 §2.3 captures the derivation verbatim including "partial → advisory **with missing escape IDs listed**" as a hard schema requirement. R4 §2.4 triple-cites the SEPARATION from `pipeline_hardening_verdict` (§4.5/§5.4/§7) and the "signoff stays advisory even when verdict=pass until complete" rule. R7 PART B encodes `_derive_status` with the all-5/some/none branches and a `__post_init__` invariant. **No gap.**

### Probe 6 — Collision boundary fully enumerated — COVERED (strong)
R6 §D enumerates ALL off-limits paths: entire `src/.../sc-troubleshoot-protocol/**`, `commands/troubleshoot.md`, `.claude/` mirrors, AND the impl's 8 files directly under `tests/troubleshoot/` (the 7 `test_hardening_*.py` + `__init__.py` + `e2e-backtest-scenarios.md`). It flags the two real collision hazards: the shared-parent `__init__.py` race and test-fn-name collision, with concrete guidance (self-contained `backtest/` package, create parent `__init__.py` only-if-absent, distinct fn names). **No gap.**

### Probe 7 — Missing test/verification coverage — COVERED (strong)
- Schema-validation test for the report: R7 PART B + R2 §5 give the full `Draft202012Validator` fidelity-test idiom (in-memory + on-disk + byte-stable hash), valid/invalid fixture layout, required-field + enum pins.
- Report-to-tmp_path pollution guard: R2 §3a explicitly flags the root `_pollution_snapshot` autouse fixture and instructs writing reports to `tmp_path`, NOT under `docs/`. **This is a real, easily-missed trap and the research caught it.**
- Lint/format gates: research-notes VALIDATION_REQUIREMENTS line 81 names `uv run ruff check` + `uv run ruff format --check` per project memory. (See OBS-2.)

### Probe 8 — Actionability — COVERED (strong)
Findings are highly actionable: exact file:line citations, copy-pasteable helper code (R3 §5.1), exact patch-target strings (R3 §1.3), `parents[3]` depth (R6 §C, R2 §3c), skipif guard code (R6 §C). Builder-facing recommendation lists in R3 §7, R6 §E, R7 Summary.

---

## GAPS / ISSUES FOUND

### G1 (IMPORTANT) — Cross-file contradiction on the replay checkout target (R3 vs R5)
**Location:** `research/03-git-replay-helpers.md` §4 (lines 154-170) + §5.1 example (line 225) vs `research/05-replay-targets.md` harness table (lines 272-278) + `research-notes.md` line 71.

R3 §4 treats the per-escape SHA as ambiguous and adopts reading "(a) the listed SHA is the FIX commit; replay `<sha>^`". Its §4 table lists "E1 given SHA = `94d5baa0`" and computes `94d5baa0^ = ac80f176` as the replay target, and its §5.1 usage example hardcodes `_resolve_prefix_parent("94d5baa0")` → `ac80f176`.

**This is wrong.** Verified against git:
- E1 fix = `7601ad25`, parent = `94d5baa0`. So `94d5baa0` IS ALREADY the pre-fix parent (the correct checkout target), NOT the fix. Applying R3's `<sha>^` to `94d5baa0` yields `ac80f176` — **one commit too early** (the wrong tree).
- R5's harness table correctly lists the checkout targets as the PARENTS: E1=`94d5baa0`, E2=`10723863`, E3=`e97aa4fd`, E4=`1b0264f1`, E5=`d878bc6d`. These match `git rev-parse <fix>^` exactly.

R3's own §4 table conflates the *fix* SHAs with the *parent* SHAs (e.g. it lists "E2 given SHA `10723863`" but `10723863` is the E5 FIX and the E2 parent). A builder following R3's `_resolve_prefix_parent(fix_sha)` helper with R5's parent SHAs as input would double-decrement and replay the wrong commit for every escape.

**Required fix:** Reconcile R3 and R5. The authoritative mapping is R5's table: the harness checks out the PARENT SHAs **directly** (no `^` applied). R3's `_resolve_prefix_parent` helper and §4 reading-(a) must be corrected so the builder does NOT apply `<sha>^` to R5's already-parent checkout targets. The git-replay helper should accept a parent SHA directly (`checkout_worktree(parent_sha)`), or if it resolves `<fix>^`, it must be fed the FIX SHAs from R5's "Fix SHA" column — not the "pre-fix parent" column. This contradiction is exactly the kind that silently produces a green-but-meaningless backtest.

### G2 (IMPORTANT) — CI shallow-clone isolation gap is flagged but UNRESOLVED
**Location:** `research/03-git-replay-helpers.md` §6.2 (line 276) — marked **(Unverified)**; handed to R2. `research/02` does NOT pick it up.

R3 explicitly flags: "if CI does shallow `fetch-depth: 1`, these 5 commits won't be present and the integration test must `skip`, not `fail`" and defers verification to R2. R2 covers skip/skipif conventions in general but **never inspects the actual CI checkout depth** — neither file closes it. So the probe-4 sub-question ("no leaked worktrees on CI shallow-clone") is left as an open hand-off across two files with neither closing it.

**Required fix:** One researcher (or the builder via a Phase-1 discovery item) must (a) inspect the CI workflow's checkout `fetch-depth`, and (b) specify the skip-guard predicate for the integration replay (e.g. `git cat-file -e <parent_sha>^{commit}` existence probe) so a shallow clone SKIPs rather than FAILs. R3 gives the pattern (`git rev-parse --is-inside-work-tree` + `git cat-file -e`) but the concrete CI-depth fact is missing. Without it the builder may ship an integration test that hard-fails in CI.

### G3 (MINOR) — Worktree teardown leak-on-failure: covered but no explicit "verify no leaked worktree" assertion specified
**Location:** `research/03-git-replay-helpers.md` §5.2 + §6.1.

R3's try/finally contract is correct (teardown in `finally`, `check=False`, `rmtree(ignore_errors=True)`, `prune`) and §6.1 says the unit test should "assert the `finally` teardown still fires" on a failure path. However, neither R3 nor R2 specifies a concrete post-condition assertion that **no worktree admin entry leaks into `.git/worktrees/`** after an assertion-failing replay (e.g. asserting `git worktree list` is back to baseline). The cleanup mechanism is prescribed; the *verification that cleanup happened on the failure path* is described only in prose, not as a concrete assertable post-condition. Probe-4 asked specifically about "no leaked worktrees on assertion failure" — the mechanism is solid but the proof-of-cleanup test is under-specified.

**Suggested fix:** Add to builder guidance a test that forces an assertion failure inside the `checkout_worktree` context, then asserts `git worktree list --porcelain` returns to its pre-test baseline. Low severity because the `finally`+`prune` mechanism is already correct; this hardens the verification, not the mechanism.

---

## OBSERVATIONS (not gaps; for builder awareness)

- **OBS-1:** With the NEW=CATCH half being a pure-markdown doc-presence proxy (R6 §B), `backtest_status=complete` does NOT mean the gates were *executed* against the escapes — it means the catch mechanism is *documented* + the OLD=MISS replay reproduced the historical miss. R4 §2.5 ("predicted until built") and R7's per-escape `negative_witness` field cover the OLD side. The builder should ensure the report / REPORT.md wording does not imply executed-catch when only documentation-presence was asserted. Consistent with NFR-1's "predicted until then" language — an intent-alignment note, not a defect.
- **OBS-2:** Lint/format validation (`ruff check` + `ruff format --check`) appears only in `research-notes.md` (scope map, line 81), not deeply in a researcher file. The builder should still encode it as an L3/validation item. Minor because the scope map captures it and project memory reinforces it.

---

## Confidence Gate

- [x] Probe 1 (OLD=MISS mechanically assertable) — VERIFIED via R5 read + git SHA/parent re-verification
- [x] Probe 2 (NEW=CATCH vacuity) — VERIFIED via R6 §B read + on-disk skill-dir structure
- [x] Probe 3 (E4 ambiguity) — VERIFIED via R4 §4.2 + independent git `merge-base --is-ancestor` + parent advisory-absence check
- [x] Probe 4 (cleanup/isolation) — VERIFIED: worktree roundtrip R3 §3 + try/finally §5.2; gaps G2/G3 raised
- [x] Probe 5 (backtest_status derivation + separation) — VERIFIED via R4 §2.3/§2.4 + R7 PART B read
- [x] Probe 6 (collision boundary) — VERIFIED via R6 §D read
- [x] Probe 7 (schema test / pollution guard / lint) — VERIFIED via R7 PART B + R2 §3a/§5 read; OBS-2 raised
- [x] Probe 8 (actionability) — VERIFIED via citation density across R3/R5/R6/R7
- [x] Cross-file contradiction scan — VERIFIED: found G1 via git ground-truth
- [x] All 8 files Read in full or header+core — VERIFIED

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 (8 research files + report self) | Grep: 0 | Glob: 0 | Bash: 3 (SHA/parent table, dir listing, E4 ancestry + parent advisory probe)

Tool-engagement note: Bash was used for ground-truth git verification (the decisive evidence for G1 and Probe 3), not padding; each call mapped to a specific probe. No web research performed (all claims repo-internal).

---

## Items Reviewed (summary table)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory + status | PASS | 8/8 files present, all marked Complete; sizes 18-30KB |
| 2 | OLD=MISS mechanically defined per E1-E5 | PASS | R5 §(b)/(c) per-escape buggy fn + observable |
| 3 | NEW=CATCH meaningfulness / not vacuous | PASS | R6 §B: pure-markdown proxy, weakness named + bounded |
| 4 | E4 replay base pinned (20693bb8 nuance) | PASS | R4 §4.2 + git re-verify: parent 1b0264f1 unambiguous |
| 5 | Cleanup/isolation (worktree teardown) | PASS w/ G2,G3 | R3 §3/§5.2 mechanism solid; CI-depth + leak-assert gaps |
| 6 | backtest_status derivation + separation | PASS | R4 §2.3/§2.4, R7 PART B; partial+missing-IDs captured |
| 7 | Collision boundary enumerated | PASS | R6 §D: all off-limits paths + 2 hazards |
| 8 | Schema test / pollution / lint coverage | PASS | R7 PART B, R2 §3a/§5; OBS-2 minor |
| 9 | Cross-file contradiction scan | FAIL | **G1: R3 §4/§5.1 vs R5 checkout-target contradiction** |
| 10 | Actionability of findings | PASS | dense file:line + copy-paste code throughout |

---

## Summary

- Checks passed: 9 / 10
- Checks failed: 1 (cross-file contradiction)
- Gaps: G1 (IMPORTANT), G2 (IMPORTANT), G3 (MINOR)
- Observations: OBS-1, OBS-2 (non-blocking)

The research corpus is genuinely strong and unusually self-aware (R6 honestly names the NEW=CATCH proxy weakness; R2 catches the pollution-snapshot trap; R4 independently catches the E4 HEAD-healing nuance). However, per zero-tolerance research-gate rules, **ANY gap = FAIL**. Three gaps exist:
- **G1** is genuinely dangerous: a builder following R3's `<sha>^` helper prescription against R5's parent SHAs would replay the wrong commit for all 5 escapes, producing a green-but-meaningless backtest. The two files must be reconciled to a single authoritative checkout-target mapping (R5's parents, checked out directly).
- **G2** leaves the CI shallow-clone skip-guard unverified across an R3→R2 hand-off that R2 never closed.
- **G3** under-specifies the proof-of-cleanup-on-failure assertion (mechanism correct; verification prose-only).

---

## VERDICT: FAIL

Resolve G1 (reconcile R3/R5 checkout-target mapping — authoritative = R5 parents, checked out directly, no `^`), G2 (pin CI fetch-depth + integration skip-guard predicate), and G3 (add a no-leaked-worktree post-condition assertion to builder guidance) before greenlighting synthesis/task-build. G1 is the blocking concern; G2/G3 are isolation/CI hardening that must also be closed under zero-tolerance.

## QA Complete
