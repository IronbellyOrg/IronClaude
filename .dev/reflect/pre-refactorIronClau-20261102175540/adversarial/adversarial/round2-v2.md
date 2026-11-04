# Round 2 — Variant 2 Advocate rebuttal

## Response to criticisms
- C-001 missed (V1): conceded. Check 1 runs `gh repo view` without `--repo`; check 3 "close it immediately and reopen" acts on an upstream PR; plan line 73 bans such calls. Mitigation: plan line 78 says the pre-PR checks "stay. Edit them only where they contradict the rules above", a generic hook that does not name the lines. C-001 goes to V1.
- `missing_requirements: []` (V1, V3): conceded; eval_runner.py:143 is in scope. The section is the right place for a coverage verdict; its verdict was wrong.
- R2-F4 misquotes .gitignore:129: conceded and withdrawn. Real line 129: "(R3) Lookup-cache tracked artifacts — user-authorized exception (merged-requirements.md Gitignore Exception)". The plan's constraint copies repo CLAUDE.md wording; residual point (CLAUDE.md ignores the R3 exception) is informational and outside this plan.
- Vacuous test run (V3): conceded. test_git_replay_integration.py:56-68 skips the module when `git cat-file -e <sha>^{commit}` misses a pinned parent. Add `-rs` and require zero SKIPPED lines.
- R2-F3 equals R1-4 (round2-v1): accepted; extra is the fixture citation at test_implement_retry_revert.py:613. C-004 tie.

## Updated assessment of other variants
- V1: strongest on correctness; only card naming CLAUDE.md:66; Round 2 concessions bring it closer to V2 on C-005 and C-004; R1-3 minor.
- V3: R3-F1 is the most valuable finding of the debate; R3-F4 and R3-F5 real; weak on all-drift labelling and check-1-only coverage.

## New evidence
- `git rev-parse --is-shallow-repository` prints `false` in this checkout, so the replay module may run here; environment-dependent, so the zero-skip guard is still needed (A-003 open risk, not sure failure).
- Plan line 78 partly covers C-001 generically.

## Final per-point positions
| Point | Superior | Reason |
|---|---|---|
| S-001 | 2 | Only explicit missing-requirements audit; wrong but checkable |
| S-002 | 1 | Mixed labels fit the taxonomy |
| S-003 | 1 | Engages F1-F4 with verified corrections |
| C-001 | 1 | Only card naming CLAUDE.md:64 and :66 |
| C-002 | tie | All three require a decision on :251 |
| C-003 | 1 | Necessary class plus Blocked status (POST-REFLECT-TASK.md:6) |
| C-004 | tie (changed from 2) | Same three tests; both need `-rs` and zero skips |
| C-005 | 2 | Literal reading; V1 conceded |
| X-001 | 2 | Plan line 73 covers a static URL |
| X-002 | 3 | eval_runner.py:143, never removed |
| A-001 | tie | Only test_how_we_work_routing_table.py:352 reads root CLAUDE.md |
| A-002 | tie | Holds on this host only |
| A-003 | 3 | Module-level skipif at :56; not shallow here but environment-dependent |
