# Track 1 Gap-Fill Report (FU-001 sprint runner .sprint-exitcode)

**Date**: 2026-05-18
**Trigger**: A.8 quality-gate finding — `executor.py` grew ~40 lines after PR-A landed; all cited `file:line` refs in T1 research were drifted.
**Files updated**: `research/01-file-inventory.md`, `research/02-config-pattern.md`
**Verification method**: Direct `grep -n` against current master HEAD (cwd `/config/workspace/IronClaude`).

## Issues addressed

1. **Drift: executor.py sentinel writer** — `1714 → 1754` (drift +40 from PR-A growth: 2096 → 2136 lines).
2. **Drift: other executor.py `release_dir` reads** — `1668→1708`, `1669→1709`, `1789→1829`, `1845→1885`, `1861→1901`, `1869→1909`.
3. **Drift: commands.py `--release-dir` block** — option `170→176-177`, `run()` param `189→198`, override write `224-228→234-237`, `CLAUDE_MODEL` `211→220`.
4. **Drift: models.py SprintConfig** — class def `347→348`, field block `357-396→358-397`, `__post_init__` body `398-444→399-445`, `work_dir` mirror `403→404`, wiring_gate derivation `441-444→442-445`, computed properties shifted +1 line.
5. **Drift: file line counts** — executor.py 2096→2136, commands.py 423→433, models.py 850→857, config.py 501→503, tmux.py 317 unchanged. Total 8417→8464.
6. **`tmux.py:166` (reader)** — **UNCHANGED**; no edit needed.
7. **`config.py:236/266/336` (resolver/loader)** — **UNCHANGED**; no edit needed.
8. **Gap: 02 missing "Gaps and Questions"** — appended OQ-1 (`--release-dir` override should re-derive `state_dir`, recommended YES), OQ-2 (env-var routing via loader), OQ-3 (line-drift warning for builder if >3 days elapse before Phase 1).
9. **Gap: 01 cross-skill dependency unclear** — added explicit "Scope decision needed" note offering (a) in-scope co-patch of `bootstrap_scan.sh:90,126` or (b) defer to sibling follow-up via Open Question. Builder must pick one.

## Values used after re-verification

| Reference | Old | New |
|---|---|---|
| executor.py sentinel writer | :1714 | :1754 |
| executor.py file size | 2096 lines | 2136 lines |
| commands.py override write | :224-228 | :234-237 |
| commands.py CLAUDE_MODEL | :211 | :220 |
| models.py SprintConfig def | :347 | :348 |
| models.py work_dir mirror | :403 | :404 |
| models.py wiring_gate derive | :441-444 | :442-445 |
| commands.py file size | 423 lines | 433 lines |
| models.py file size | 850 lines | 857 lines |

## Sign-off

Track 1 research files are now line-accurate as of master HEAD 2026-05-18. Builder may consume `01-file-inventory.md` and `02-config-pattern.md` directly. The `bootstrap_scan.sh` scope decision is now explicitly flagged for builder resolution.
