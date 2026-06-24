# QA Report — Phase 4 Content-Collision / NodeID Boundary (task-qualitative, adversarial)

**Topic:** Phase 4 backtest harness collision-boundary + nodeid distinctness vs sibling impl tasklist
**Date:** 2026-06-12
**Phase:** task-qualitative (adversarial collision-boundary audit)
**Fix cycle:** N/A
**Fix authorization:** false (report-only — NO source file modified)

---

## Overall Verdict: FAIL

**One MINOR boundary-touch found** (empty parent `tests/troubleshoot/__init__.py` created on the Phase 4 side, a path research §D.3 L255 lists as impl-owned). Per this phase's no-leniency rule (any issue of any severity = FAIL), the verdict is **FAIL**. The finding is idempotent, empty-file, and was *conditionally pre-authorized* by research §D.1 (L280-289) as a "create-ONLY-IF-ABSENT bootstrap" — so it is a process/ownership-clarity defect, **not** a functional collision and **not** a hard violation of the harness's write discipline. The four substantive VERIFY criteria (1, 3, 4, and the src/skill/.claude half of 2) all PASS with zero violations. The adversarial hypothesis ("≥3 collisions") is **not borne out** — 0 nodeid collisions, 0 off-limits src/skill/.claude writes, 0 replay writes under src/.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Every Phase 4 file lives ONLY under `tests/troubleshoot/backtest/` | omissions | **FAIL** | All 9 named harness files ARE under `backtest/` (ls, `tests/troubleshoot/backtest/`). BUT a 10th artifact — the empty parent `tests/troubleshoot/__init__.py` (0 bytes, Jun 12 00:40) — was created one level UP, outside `backtest/`. See Issue #1. |
| 2 | NO writes under skill dir / `commands/troubleshoot.md` / `.claude/**` / impl-owned `tests/troubleshoot/{__init__.py, test_hardening_*, e2e-backtest-scenarios.md}` | invented-content | **FAIL (partial)** | src/skill/.claude half: PASS — `git status --porcelain` shows only `?? tests/troubleshoot/` + the two `.dev/` task dirs; grep for `src/superclaude/skills/sc-troubleshoot`/`commands/troubleshoot`/`.claude/` = NONE. NEW=CATCH proxies only READ refs, each guarded by `requires_impl_ref(...)` skipif (`_impl_guard.py:43-57`; e1.py:78, e2.py:90, e3.py:103, e4.py:94, e5.py:67, waiver:25). The impl-owned-`__init__.py` clause is touched: see Issue #1. `test_hardening_*` / `e2e-backtest-scenarios.md` NOT created (ls: No such file). |
| 3 | Per-escape test FN names distinct from impl `test_hardening_*` (and waiver from `test_waiver_latch_one_way`) | contradictions | **PASS** | `comm -12` of impl fn-name set (research §A.1) vs backtest fn-name set = EMPTY (0 collisions). Waiver handled: impl `test_waiver_latch_one_way` (verdict module) vs ours `test_waiver_latch_one_way_blocks_downstream_regreen` (waiver_regreen.py:26) — distinct, per waiver docstring L29-31. NodeID prefixes structurally distinct (`tests/troubleshoot/backtest/...` vs `tests/troubleshoot/test_hardening_*`). |
| 4 | No Phase 4 test WRITES under src/ or skill dir (replay only checks out throwaway worktrees + reads) | invented-content | **PASS** | `checkout_worktree` adds `git worktree add --detach` into `tempfile.mkdtemp()` and `shutil.rmtree`+`prune` in `finally` (git_replay.py:154-227). `run_prefix_replay_snippet` runs in the throwaway `wt`, `sys.path.insert(0, wt/src)` — reads pre-fix code, never writes src (replay_executor.py:200-248). E5 uses `read_source_from_worktree` (read-only, e5.py:45-47). Replay snippets write only to their own `tempfile.mkdtemp()` (e1.py:42, e3.py:50). `_repo_anchor` pins add/remove/prune to one repo (git_replay.py:117-140). Worktree-leak guard test exists (`test_backtest_replay_leaves_no_leaked_worktree`). |

## Summary
- Checks passed: 2 / 4 (substantive); src/skill/.claude half of #2 also clean
- Checks failed: 2 (#1 boundary-touch; #2 impl-`__init__` clause) — same single root cause
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (the parent `__init__.py` boundary-touch)
- Adversarial hypothesis (≥3 collisions): NOT BORNE OUT — 0 nodeid collisions, 0 off-limits content writes
- Issues fixed in-place: 0 (report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `tests/troubleshoot/__init__.py` (0 bytes; `?? tests/troubleshoot/` in git status) | Empty parent package marker created on the Phase 4 side. Research §D.3 L255 enumerates this exact path as impl-owned ("impl CREATES, Step 7.1") in the OFF-LIMITS list, so a literal reading of VERIFY #2 flags it. It is, however, (a) empty/0-byte — byte-identical to what impl Step 7.1 produces, (b) idempotent, (c) explicitly conditionally-authorized by research §D.1 L280-289 + §E L314-316 as a "create-ONLY-IF-ABSENT empty-file bootstrap" for `backtest/` collection. Soft collision, not hard. | EITHER (preferred) make `backtest/` a self-contained package and DELETE the parent `tests/troubleshoot/__init__.py`, relying on pytest rootdir for collection (research §D.1 L283-286); OR encode an explicit "create parent `__init__.py` ONLY-IF-ABSENT, never overwrite" guard + a comment crediting impl Step 7.1 as the true owner, so the impl's idempotent re-create is a no-op and no diff-doubling occurs. Confirm `uv run pytest tests/troubleshoot/backtest/` still collects without the parent marker before deleting. |

## Actions Taken
None — report-only (`fix_authorization: false`). No source file modified. Verified via `git status --porcelain`: only `?? tests/troubleshoot/` and the two expected `.dev/` task directories are dirty; NO off-limits `src/`, skill, `commands/troubleshoot.md`, or `.claude/` path was written.

## Detail — why the adversarial "≥3 collisions" hypothesis fails

I assumed ≥3 collision-boundary violations existed and hunted for them. The genuinely load-bearing collision surfaces were each checked and found clean:

1. **NodeID/function-name collisions across the shared `tests/troubleshoot/` tree** — the most likely place for ≥3 hits. `comm -12` of the impl fn-name set vs the backtest fn-name set = EMPTY. The near-miss the research warned about (waiver) is correctly disambiguated: `test_waiver_latch_one_way` (impl) vs `test_waiver_latch_one_way_blocks_downstream_regreen` (ours). Module nodeid prefixes differ (`backtest/` subpackage). **0 collisions.**
2. **Off-limits content writes (skill refs, SKILL.md, commands/troubleshoot.md, .claude mirrors)** — `git status` + targeted grep = NONE. The NEW=CATCH proxies READ refs guarded by `requires_impl_ref` skipif; they never create/edit them. **0 violations.**
3. **Replay writing under src/ or the skill dir** — the replay seam checks out throwaway detached worktrees under `tempfile.mkdtemp()`, reads pre-fix source, and tears down in `finally` (rmtree + mandatory `git worktree prune`). Snippets write only to their own temp dirs. **0 violations.**

The ONLY boundary-touch is the empty parent `__init__.py` (Issue #1) — a single MINOR ownership-clarity defect, not the ≥3 substantive collisions hypothesized.

## Self-Audit

**(a) Reliance list — items I did NOT take on faith (no Inherited Structural Verdict was supplied; standalone mode):**
- No `## Inherited Structural Verdict` block in the spawn prompt → standalone behavior; I independently verified every VERIFY claim with my own tool engagement (no reliance on a prior rf-qa pass).

**(b) Independent semantic checks (≥1 required, INV-019):**
- Collision-boundary write-discipline — verified by `git status --porcelain` (only `?? tests/troubleshoot/` + `.dev/` task dirs dirty; 0 off-limits paths) and targeted grep for `src/superclaude/skills/sc-troubleshoot`/`commands/troubleshoot`/`.claude/` = NONE.
- NodeID distinctness — verified by `comm -12` set-intersection of impl fn-names (research §A.1) vs backtest fn-names (`grep def test_` over all 9 modules) = EMPTY.
- Replay write-safety — verified by Reading `git_replay.py:154-227` (mkdtemp + finally-teardown) and `replay_executor.py:200-248` (`sys.path.insert` read path, cwd=throwaway wt), confirming no src/ write surface.
- Parent-`__init__.py` ownership — verified by `wc -c` (0 bytes) + `cat -A` (empty) + grep of research §D.3 L255 confirming the path is impl-owned, cross-read against §D.1 L280-289 conditional authorization.

## Confidence Gate
- **Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (boundary checks fully tool-grounded)
- **Tool engagement:** Read: 11 | Grep: 4 | Glob: 0 | Bash: 6
- No web research performed (all checks local-file-bound; Tavily-first N/A this review).
- UNCHECKED items: none. UNVERIFIABLE items: none.

## Recommendations
- Resolve Issue #1 before the harness lands: prefer making `backtest/` self-contained and deleting the parent `tests/troubleshoot/__init__.py` (research §D.1 L283-286 preferred path), OR add the explicit create-if-absent guard + impl-Step-7.1 ownership comment. This removes the only diff-doubling / ownership-ambiguity surface vs the impl branch.
- Everything else (write discipline, nodeid distinctness, replay isolation, skipif-guarded reads) is clean and may proceed.

## QA Complete
