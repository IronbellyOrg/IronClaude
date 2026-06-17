# QA Report — Post-Completion (final-invariant-compliance lens)

**Topic:** sc-bare-review M8/M9 corrective migration — final-state hard-invariant re-verification
**Date:** 2026-06-17
**Phase:** report-validation (post-completion, adversarial)
**Fix authorization:** FALSE (report only)
**Working dir:** `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9` (git worktree)

---

## Overall Verdict: PASS

All 6 hard invariants hold in the final state with measured evidence. Two non-blocking observations are documented below; neither violates any literal invariant.

---

## Invariant Results

| # | Invariant | Result | Measured Evidence |
|---|-----------|--------|-------------------|
| 1 | SKILL.md ≤80 lines, ZERO `t2_`/`scripts/t2_` refs | PASS | `wc -l` = **80** (src) / **80** (mirror, byte-identical via `diff`). `grep -nE 't2_|scripts/t2_'` exit **1** (no match) in BOTH src and mirror. |
| 2 | 3 legacy scripts + 2 orphan refs ABSENT from src AND mirror; survivor present in both | PASS | `find` for `t2_preflight.sh`/`t2_dispatch.sh`/`t2_normalize.py`/`prompts.md`/`output-template.md` over both skill dirs → **0 hits**. `bare-review-output.md` present in BOTH at `refs/templates/`. |
| 3 | Parity gate RUNS + PASSES, no SKIPPED, no `skipif`/`LEGACY_SCRIPT`/`importlib` exec dep | PASS | `test_bare_review_parity.py`: **16 passed, 0 skipped** in 0.37s. The only `t2_normalize` strings (lines 13-46) are inside the module docstring (`"""..."""`) — prose, not executable. No `skipif`/`pytest.skip`/`importlib`/`LEGACY_SCRIPT` token in the file. |
| 4 | `make verify-sync` exits 0 | PASS | `make verify-sync` → `✅ All components in sync.`, exit **0**. |
| 5 | 4 WS-0 flags on `swarm run` | PASS | `uv run superclaude swarm run --help` shows `--reviewers` (B-1), `--target-line-cap` (B-2), `--timeout-sec` (B-3), `--label` (B-4). |
| 6 | Frozen golden: 3 scenario dirs, each with per-reviewer `.md` + `return-contract.yaml` | PASS | `all-success` (3×md + contract), `partial-with-timeout` (2×md + contract), `salvage-promoted` (3×md + contract). All 3 `return-contract.yaml` non-empty (954/882/954 bytes) and parse as valid YAML. |

---

## Observations (non-blocking — do NOT violate any invariant)

| # | Severity | Location | Observation | Why it does NOT fail an invariant |
|---|----------|----------|-------------|-----------------------------------|
| O1 | INFO | `src/.../SKILL.md:10` (and mirror) | Meta comment contains the hyphenated token `t2-bare-reviewer-adjunct` (a brainstorm spec-dir path) and the substring `T2`. | INV-1 literal pattern is `t2_`/`scripts/t2_` (underscore). Exact pattern is clean (exit 1). The hyphenated spec-path reference is historical provenance, not a legacy-script reference. Case-insensitive fuzzy sweep only surfaces this one benign hit. |
| O2 | MINOR | `tests/swarm/test_bare_review_golden_regen.py:57-64,264,278` | The **golden-regen** test holds an executable dependency on the deleted `LEGACY_SCRIPT` (`scripts/t2_normalize.py`) via `LEGACY_SCRIPT` path + `sys.argv` patching. | INV-3 scopes the "no legacy dep" requirement to the **parity gate** (`test_bare_review_parity.py`), which is clean. The regen test is gated behind `pytest.mark.skipif(SWARM_REGEN_GOLDEN != "1")` — it SKIPS in normal/CI runs (verified: **1 skipped**). It is a deliberate, human-approved golden re-capture tool that, by design, reads the legacy aggregator. Latent risk: if someone exports `SWARM_REGEN_GOLDEN=1` today it would fail — but line 264 asserts the script's presence with an explicit error message, so it fails LOUDLY, not silently. The golden is already frozen + committed, so regen is not needed. Out of scope for the 6 invariants. |
| O3 | INFO | `.venv/lib/.../superclaude/_src/.../scripts/t2_*` | The 3 deleted scripts still exist under `.venv` site-packages. | This is an installed superclaude wheel copy (SuperClaude 4.3.5 pre-migration), NOT the worktree source. Git-tracked source has zero `t2_` files (`git ls-files ... | grep t2_` → exit 1). Not in scope of the src↔mirror invariants. |

---

## Confidence

- **Verified:** 6/6 invariants | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 2 | Grep: (embedded in Bash) | Glob: 0 | Bash: 9
- Every invariant mapped to ≥1 dedicated Bash measurement; cross-checked src vs mirror independently.

## QA Complete
