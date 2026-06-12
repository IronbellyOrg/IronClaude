# QA Report — Collision-Boundary + Path-Resolution Discipline (Phase 2)

**Topic:** sc:troubleshoot pipeline-hardening backtest harness — Phase 2 collision boundary
**Date:** 2026-06-12
**Phase:** doc-qualitative (content QA lens; collision-boundary + path-resolution)
**Fix cycle:** N/A
**Fix authorization:** false (report-only — NO source file modified)
**Stance:** Adversarial. Assumed >=3 boundary violations existed; hunted for them.

---

## Overall Verdict: PASS

No collision-boundary violation and no `parents[2]` path-resolution defect was
found across the four Phase 2 files. The adversarial hypothesis (>=3 violations)
was **not** borne out by the evidence; three candidate "violations" were probed
and each was ruled out with file:line + git evidence (see Adversarial Probes).

---

## Files Reviewed (4)

| # | File | Lines | Verdict |
|---|------|-------|---------|
| 1 | `tests/troubleshoot/backtest/git_replay.py` | 127 | PASS |
| 2 | `tests/troubleshoot/backtest/test_git_replay_unit.py` | 82 | PASS |
| 3 | `tests/troubleshoot/backtest/test_git_replay_integration.py` | 107 | PASS |
| 4 | `.dev/tasks/.../research/06-impl-tasklist-crossref.md` (cross-ref) | 339 | PASS (read-only reference) |

---

## VERIFY-1 — Every Phase 2 file lives ONLY under `tests/troubleshoot/backtest/`

**Result: PASS**

Evidence (`ls -la tests/troubleshoot/backtest/`):
- `git_replay.py`, `__init__.py`, `test_git_replay_integration.py`,
  `test_git_replay_unit.py` — all four executable/source artifacts are inside
  `tests/troubleshoot/backtest/`.
- `git status --porcelain` shows the ONLY untracked tree touched under `tests/`
  is `?? tests/troubleshoot/` — no Phase 2 file landed anywhere else under
  `tests/`.

---

## VERIFY-2 — No edits/creates under impl-owned paths

**Result: PASS**

`git status --porcelain` for each off-limits surface returned EMPTY (no entry):
- `src/superclaude/skills/sc-troubleshoot-protocol/**` — clean. `refs/` still
  holds only the 8 pre-existing refs (`calibrator-eval-cases.md`,
  `diagnosability-audit.md`, `doc-discovery.md`, `escalation-rubric.md`,
  `hypothesis-card-template.md`, `remediation-handoff.md`, `report-template.md`,
  `triage-checklist.md`); NONE of the 6 impl-CREATE refs exist (so nothing was
  pre-authored by us).
- `src/superclaude/commands/troubleshoot.md` — clean (no status entry).
- `.claude/**` — clean (no status entry).
- Impl-owned files directly under `tests/troubleshoot/` — all 8 ABSENT
  (`test_hardening_h0..h4.py`, `test_hardening_verdict.py`,
  `test_hardening_output_contract.py`, `e2e-backtest-scenarios.md`): probed via
  `test -e` loop, every one reported `absent`.

Source-code references to impl-owned paths are **read-only mentions in
docstrings/comments**, NOT edits or creates:
- `git_replay.py:3` — names `src/superclaude/cli/sprint/process.py` as the
  subprocess-seam it mirrors (prose; not the sc-troubleshoot skill dir; not edited).
- `test_git_replay_unit.py:6` — names `test_hardening_*` only to explain the
  deliberate `test_backtest_*` nodeid disambiguation (§D.3 hazard #2 honored).

Reading off-limits refs for assertion targets is explicitly permitted by the
cross-ref (§D.1: "Reading these refs … is fine; editing/creating … is the
violation"). No such read even occurs at Phase 2 (NEW=CATCH proxy deferred).

---

## VERIFY-3 — Repo-root path resolution uses `parents[3]` (NOT `parents[2]`)

**Result: N/A for Phase 2 — no repo-root path resolution exists in any Phase 2 file.**

This is the legitimate N/A the task brief anticipated. Evidence:
- `grep -rn "parents\[" tests/troubleshoot/backtest/` → **no `parents[N]`
  indexing anywhere**.
- The only `parents` token is `git_replay.py:98` `base.mkdir(parents=True, …)` —
  that is the `mkdir` **`parents=True` kwarg** (create intermediate dirs), NOT a
  `Path(__file__).resolve().parents[N]` repo-root walk. Flagging it would be a
  false positive; explicitly cleared.
- `grep -rn "Path(__file__)|REPO_ROOT|resolve()"` → no matches in any Phase 2
  file.
- Consistent with cross-ref §C: repo-root resolution (`REPO_ROOT =
  Path(__file__).resolve().parents[3]`) arrives later with the NEW=CATCH
  skipif guard / Phase 4 `_impl_guard.py` — and `_impl_guard.py` confirmed
  ABSENT today (`ls` → No such file). When that code lands, `parents[3]` is the
  required depth for `tests/troubleshoot/backtest/<file>` → root; Phase 2 simply
  has no such code yet.

---

## Adversarial Probes (the 3+ hypothesized violations, each ruled out)

| # | Hypothesized violation | Probe | Outcome |
|---|------------------------|-------|---------|
| P1 | A Phase 2 file edits/creates the parent `tests/troubleshoot/__init__.py` (impl-owned per §D.3) | `ls`+`git status` | **Not a violation.** Parent `__init__.py` exists (0 bytes, untracked). §D.4 + §E.6 explicitly authorize creating the parent `__init__.py` **ONLY-IF-ABSENT, never overwrite** as a one-time idempotent bootstrap; impl's Step 7.1 will (idempotently) own it. 0-byte empty file = no content collision; impl can overwrite/extend freely. SOFT-collision, sanctioned. Not flagged. |
| P2 | `git_replay.py:98` `parents=True` is a `parents[2]` repo-root walk | Read line 98 in context | **False positive.** It is `Path.mkdir(parents=True)` (dir-creation kwarg), not `Path(__file__).parents[2]`. Ruled out. |
| P3 | Docstring/comment mentions of `src/...` or `test_hardening_*` constitute editing impl-owned surfaces | `grep` + `git status` on each path | **Not a violation.** All mentions are read-only prose (`git_replay.py:3`, `test_git_replay_unit.py:6`); `git status` shows zero edits to any named off-limits path. Ruled out. |

All three adversarial hypotheses failed to find a real breach. The boundary holds.

---

## Self-Audit (MANDATORY)

1. **Factual claims independently verified against repo state:** 11 —
   (a) 4 files all under `backtest/` (ls); (b) parent `__init__.py` exists +
   untracked (ls+git status); (c) parent is 0-byte empty (ls size); (d) no
   `parents[N]` indexing (grep); (e) `mkdir(parents=True)` is the only `parents`
   token (Read L98); (f) no `Path(__file__)`/`REPO_ROOT`/`resolve()` (grep);
   (g) src skill `refs/` holds only 8 pre-existing refs, none of the 6 new
   (ls); (h) `commands/troubleshoot.md` / skill dir / `.claude/` all clean
   (git status); (i) all 8 impl-owned `tests/troubleshoot/` files absent
   (`test -e` loop); (j) `_impl_guard.py` absent (ls); (k) docstring path
   mentions are prose, not edits (Read + grep + git status).
2. **Tools used to verify:** Read (×5 — 4 target files + backtest `__init__.py`),
   Grep/Bash-grep (parents, Path/REPO_ROOT, src/.claude tokens), Bash
   (`ls`, `git status --porcelain`, `git ls-files`, `git ls-tree origin/master`,
   `test -e` presence loop, `ls refs/`).
3. **Why trust a PASS here:** the verdict is not "looks fine" — every off-limits
   surface was independently probed with `git status` (empty = untouched) and the
   one genuinely ambiguous artifact (parent `__init__.py`) was traced to an
   explicit cross-ref sanction (§D.4/§E.6 ONLY-IF-ABSENT bootstrap) and confirmed
   0-byte/untracked. The single most-likely real violation (P1) was the one I
   pushed hardest on and it resolved to sanctioned-soft-collision, not breach.
4. **Web research performed:** none. All verification was local-file/git-bound;
   Tavily-first precedence did not apply this review.

---

## Confidence

**Verified: 3/3 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**
(VERIFY-1 PASS, VERIFY-2 PASS, VERIFY-3 N/A-adapted-and-cleared — N/A here means
"no such code exists to check," documented per check-#3's own escape clause, not
an un-run check.)

**Tool engagement:** Read: 5 | Grep: 3 | Glob: 0 | Bash: 4

---

## Issues Found

None. No CRITICAL, IMPORTANT, or MINOR issues.

(Advisory, non-blocking — NOT an issue against Phase 2: the parent
`tests/troubleshoot/__init__.py` was created as the §E.6 ONLY-IF-ABSENT
bootstrap. It is currently a hard 0-byte empty file with no overwrite-guard
comment. When the impl's Step 7.1 lands, it must treat this as create-if-absent
too. This is the impl's responsibility per §D.4, already documented; flagged
here only for traceability, not as a Phase 2 defect.)

## QA Complete
