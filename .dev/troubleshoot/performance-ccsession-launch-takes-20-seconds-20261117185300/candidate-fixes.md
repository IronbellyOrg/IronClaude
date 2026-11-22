# Candidate fixes (Wave 3 step 4)

Calibrated confidence of each card (independent calibrators, not self-reports): Tier 1 0.83; Tier 2 root-cause-analyst 0.83; system-architect 0.83; performance-engineer 0.50 (C7 cap, see tier2-performance-engineer-calibration.md notes).

| Fix | Supporting cards | Summary | Verdict |
|---|---|---|---|
| fix-1: python3 batch helper for the index and head/tail cwd scan, bash path kept as fallback with the locale and `date` fixes | Tier 1 (0.83), root-cause-analyst (0.83) | one helper called once per list; saves about 13.4 s of 27.07 s (derived) | competing |
| fix-2: bash-only: real C locale for grep, builtins instead of per-row spawns, one file, no helper | performance-engineer (0.50) | derived remaining 11.6-14.1 s of 27.07 s | competing (outlier on confidence) |
| fix-3: staged: bash quick win first (becomes the fallback), then the helper | system-architect (0.83) | stage 1 about 14.6 s remaining (itemised, one proxy), stage 2 A-core 4.62 s remaining | competing |

All three agree on the diagnosis (per-row process spawning plus the unexported `LC_ALL=C` at ccsession:1383/1403) and on keeping the output contract; they differ in mechanism (helper vs builtins vs both, in what order). No split-pending cluster: no two cards cite the same file:line for different mechanisms; the end-to-end locale probe (median gap 6.99 s) settled the one open mechanism question (locale). Wave 4 debates the fix mechanism for the shared diagnosis.
