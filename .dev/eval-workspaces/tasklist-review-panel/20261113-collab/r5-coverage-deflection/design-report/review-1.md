verdict: FAIL

Independent review of `r5-coverage-deflection/DESIGN.md` against `merged-requirements.md` (MR) sections 2.0, Redesign 5, 4 and 5, the cited harness files and `findings.py`. Three blocking findings, eleven minor.

What I checked and found correct: the pinned sha256 values of `judge-one.sh` and `run-reviewer.sh`; the three H3 base commits (each is the only parent of its squash commit); `refs/merge-guard.md` is absent at the DS base and `tests/skills/test_worker_contract.py` is present at the CT base; the Task counts 13/9/12 and the `## Task <n>:` heading form; the reviewer ids in `resolution-live7.json`; that the installed `superclaude` `findings.py`/`ledger.py` currently equal the worktree copies (D10 can pass); that `git archive <base> -- . ':(exclude)…'` works on git 2.47 and drops the four folders; the D9 path walk (four `..` steps from `EVAL/arms/scoring/combos` reach `tasklist-review-panel/`, and that folder exists); that `jq`, `flock`, `sha256sum` and `openssl` are in `/usr/bin` (T-9(g) under `env -i PATH=/usr/bin:/bin` is feasible); the cited line numbers in `run-reviewer.sh`, `judge-one.sh`, `anon-b11.sh`, `merge-b11.sh`, `final-table.py` and `findings.py`; every timing figure in sections 3.1-3.3 (planned ends, finish bounds, hang guards, PANEL_FINISH_AT, slowdown limits 13.8%, 14.8%, 11.2%, 22.2%); that the R-23 field list is complete in 2.8; that the merge accepts a resolution listing a reviewer that has no `--report` (so leaving an INVALID reviewer out works).

## Findings

1. **blocking. DESIGN.md:486 (T-12): two k test cases contradict the k formula the design itself specifies.**
   Evidence: DESIGN.md:246 gives `k = max(0, min(2, floor((0.35 B - 2 - turn_p90 - T_report_p90) / (2 turn_p90))))`. T-12 asserts `(273.7, 14, 23.8) = 2` and `(273.7, 14, 51.8) = 1`. Computed (`uv run python`): (0.35·273.7 − 2 − 14 − 23.8)/28 = 55.995/28 = 1.9998, so k = 1; (0.35·273.7 − 2 − 14 − 51.8)/28 = 27.995/28 = 0.9998, so k = 0. The exact thresholds are 23.795 s and 51.795 s. The source rounds them to 23.8 and 51.8 (MR:293, MR:827), and R-42's check is worded "k >= 1 only if T_report_p90 <= 51.8 s" (MR:1095), which these values do not prove. AC-1 (DESIGN.md:555) needs every test to pass, so an implementer has to break either the formula or the test. Also, `hang offset (273.7) = 410.55` evaluates to 410.54999… in floats, so an exact equality test fails.
   Fix: change the SL2 cases to `(273.7, 14, 23.79) = 2`, `(273.7, 14, 23.80) = 1`, `(273.7, 14, 51.79) = 1`, `(273.7, 14, 51.80) = 0`, or state the thresholds as 23.795/51.795. Compare floats with a tolerance (`pytest.approx`). Keep the exact-boundary cases (100, 6.4, 13.8) and (238, 23, 12.3), which come out at exactly 1.0 today, but add a small epsilon before the floor (or use `Decimal`), so a float rounding change cannot flip them.

2. **blocking. DESIGN.md:268-280 (section 2.6, H2 re-ask): the re-ask session's model is never checked, but its text can become the final judged report.**
   Evidence: DESIGN.md:268 copies the model check of `run-reviewer.sh:50-58` for "each attempt" only. The re-ask (DESIGN.md:274-277) writes `$RID.reask.jsonl` in stream-json, and DESIGN.md:280 says "Its report replaces the original only if its normalised block has fewer parser errors". No observed-model check applies to it. The audit row "Model" (DESIGN.md:330) also covers attempts only. The source requires `model_ok` "checked on every session, including the sweeper and phase-2 sessions" (MR:953) and R-28 (MR:1060), and S3 requires stream-json output to be parsed "with `jq -s` through the same `RR:50-52` filters" (MR:933). With NOFALLBACK=1 there is no ladder, but a gateway misroute on the `--resume` session would still put another model's text into `<rid>.md`. That text is fed to the merge and the judge, which breaks the model allow-list.
   Fix: after the re-ask, run the `RR:51-56` filters through `jq -s` on `$RID.reask.jsonl`. Write `reask_model_ok` and `reask_observed_model` to `<rid>.timing.json`/meta. Use the re-ask report only when `reask_model_ok` is true, otherwise keep the original and log `reask_model_mismatch`. Extend the audit "Model" row and T-10/F-9 to cover the re-ask session.

3. **blocking. DESIGN.md:403-407 (section 5.3, anonymiser): arm-identifying text in reviewer claims reaches the judge.**
   Evidence: the source requires that "the judge cannot tell which arm a report came from" (MR:953) and that board references are stripped (R-29, MR:1061). The design's rewrites and post-check (DESIGN.md:406-407) cover reviewer ids, paths, `origin`, `/board/`, `evalsb-collab`, `20261113-collab` and `coverage-deflection` only. A2 and F6 briefs carry the catalogue "M1-M10" (D1, DESIGN.md:130), and F6 receivers are shown "Panel request … Apply catalogue moves M1-M10 … Peer coverage is not clearance" (DESIGN.md:132-133). A claim that says "applying M7" or "as the panel requested, Task 9" survives into `merged-anon.md`. The judge can then tell A1 apart from A2/F6 and F6 apart from A2, and all three arms share one scoring folder by design (DESIGN.md:415).
   Fix: in `anon.sh`, replace `\bM(10|[1-9])\b` with `<move>`, and redact the phrases `panel request`, `catalogue move`, `peer coverage` and `requested Task` (case-insensitive). Add those patterns to the post-check and to T-19. Record how many redactions each package needed.

4. **minor. DESIGN.md:347 (section 3.1): the per-package thresholds are rounded up, but they are "at most" bounds.**
   Evidence: 0.35·259 − 72 = 18.65 (stated 18.7), 0.35·259 − 44 = 46.65 (46.7), 0.35·269 − 72 = 22.15 (22.2), 0.35·269 − 44 = 50.15 (50.2). At the stated values k drops by one.
   Fix: give two decimals (18.65, 46.65, 22.15, 50.15), or round down.

5. **minor. DESIGN.md:400 (section 5.2): "(adding `t4-2`)" is wrong, because the maps already contain it.**
   Evidence: `merge-b11.sh:11` has `TIER[t4-2]=tier4`, and `merge-b11.sh:12` has `ALIAS[t4-2]="claude-gw-tier4[1m]"`.
   Fix: drop "(adding `t4-2`)".

6. **minor. DESIGN.md:355 (section 3.2): `SPEC.md:4` is misquoted.**
   Evidence: `combos/SPEC.md:4` says "claude-haiku-5-5 185-610 (real reviews, ~40k tokens)", which is the whole run's output, not the final report turn.
   Fix: say "about 40k output tokens per run (whole review)". The k = 0 inference still holds from the 12.3 s threshold against haiku's 23 s mean turn.

7. **minor. DESIGN.md:531 (section 6.3): Spike 5 is declared "not needed", but R-27 gates every arm on it.**
   Evidence: R-27 says "Gate 0 spikes S0, S2, S3, REQ-S3, Spike 4 and Spike 5 … pass and are recorded before any arm runs" (MR:1059).
   Fix: keep Spike 5 out of this build, but make AC-4 (or the launch preflight) require a recorded Spike 5 result from the shared plan before any non-spike row, or record this as an owner-approved deviation in 7.2.

8. **minor. DESIGN.md:558 (AC-4) contradicts DESIGN.md:527 (REQ-S3).**
   Evidence: AC-4 requires "REQ-S3 … with PASS", but REQ-S3 says "No pass threshold is pre-set".
   Fix: AC-4 should require REQ-S3 to be *recorded* with its measured rates, and the owner's run/no-run decision for any receiver model with a 0/5 rate.

9. **minor. DESIGN.md:65 (D11) misreads MR:953, and the judge sessions are not counted.**
   Evidence: MR:951 defines "A run is one panel on all three packages", so "at most 10 concurrent runs" (MR:953) caps panels, not sessions. Separately, `judge.sh` "runs the three packages' judges in parallel" (DESIGN.md:415). A launch that finishes early adds 3 Opus sessions while the other two launches still have reviewers running, which can exceed the design's own 10-session reading.
   Fix: restate D11 as a stricter self-imposed cap, and either count the judge sessions in it or run the judges after `wait` in the block driver.

10. **minor. DESIGN.md:328 (audit "Transcripts" row): two read routes to peer conclusions are not flagged.**
    Evidence: all reviewers of one package (A1, A2 and F6 launches run concurrently on the same `SB/<pkg>/repo`, DESIGN.md:456-461) write their session transcripts to the same `~/.claude/projects/-tmp-evalsb-collab-r5-<pkg>-repo/` folder (DESIGN.md:268). Those transcripts hold the scouts' full reports. The forbidden-substring list does not include `.claude/projects`, nor the REPO root path (where the repaired code and the brainstorm live).
    Fix: add `.claude/projects` and `/home/coder/workspaces/worktrees/IronClaude` to the forbidden tool-input substrings, with a T-18 case.

11. **minor. DESIGN.md:469 and DESIGN.md:556 (AC-2): the test command writes outside `R5/`.**
    Evidence: `cd REPO && … uv run pytest R5/tests` uses REPO's `pyproject.toml` as the pytest rootdir, so `.pytest_cache/` is created or updated at the REPO root. AC-2's `git status -- src/ .claude/` and `find EVAL -newer` would not see it.
    Fix: run with `-p no:cacheprovider` (or `-o cache_dir=R5/.pytest_cache`), and extend AC-2 to `git status --porcelain` on the whole repo, excluding `R5/`.

12. **minor. DESIGN.md:148 and DESIGN.md:384 (launch interface): the interface is inconsistent.**
    Evidence: the `launch.sh` env list omits `SPIKE4`, which preflight step 6 (DESIGN.md:393) and Spike 4 (DESIGN.md:528) rely on. `--pkgs` is shown as `DS,AL,CT` (DESIGN.md:384) but used with the full package id (DESIGN.md:537).
    Fix: list `SPIKE4` in the `launch.sh` interface, and state that `--pkgs` takes full package ids (or accepts both forms).

13. **minor. DESIGN.md:197 (watcher trigger): the meta file can be read half-written, and an API-error attempt counts as usable.**
    Evidence: `run-reviewer.sh:58` writes `meta.json` with a plain `>` redirect, so the 2 s poll can read a partial file. An attempt with `model_ok` and `findings_block` true but `API Error` in its text is retried by `run-reviewer.sh:59`, yet the watcher would already take it as a usable scout exit.
    Fix: write the meta through a temp file and `mv`, add `api_error` to the meta, and require `api_error: false` in the watcher's usable-attempt test.

14. **minor. DESIGN.md:117 and DESIGN.md:405: the token-to-arm key sits beside the judged folder.**
    Evidence: `scoring/keys.jsonl` maps token to row and arm, and it is the parent folder of the token directory the judge is pointed at. The judge runs with `bypassPermissions` (`judge-one.sh:25-26`). The old harness had the same exposure (`label-key.json` in `anon-b11.sh:16`), so this is not a regression.
    Fix: keep the keys file outside the judge-visible tree, for example `R5/results/scoring-keys.jsonl`.
