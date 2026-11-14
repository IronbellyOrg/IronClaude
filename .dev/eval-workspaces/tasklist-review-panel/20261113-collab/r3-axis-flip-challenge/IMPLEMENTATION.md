# Redesign 3 (Axis-Flip Challenge, F1): implementation report

Source: `DESIGN.md` in this folder. Ledger: `.dev/implement/collab-r3-axis-flip-challenge/progress.md` (repo root).
Everything below was observed on disk or in a run on 2026-11-13 (first session until 21:56 UTC, resume session from 22:08 UTC). Nothing was staged, committed or pushed. All files were written under this folder, the ledger folder and `/tmp/collab-r3/`, `/tmp/evalsb-collab-r3/`.

## 1. Status at a glance

| Part | State |
|---|---|
| Harness code (sections 2-14 of the design) | Built and runs: fake end-to-end runs (tests) and four real smoke runs |
| Unit and fault-injection tests (15.2, 15.3) | 89 passed, 0 failed, 0 skipped (`spikes/ac14/resume/tests-final.log`); ruff check and ruff format clean on `r3lib/` and `tests/` |
| Gate 0 spikes G0-H3, G0-HOOKS, S3 | Pass |
| Spike S2 | Resume passes for all four models; the "text before a mid-answer kill" check FAILS for luna in five tries (section 5). Not fixable in this code |
| G0-SURF | Starting regex failed (0% / 4.8%); calibrated regex passes on numbers (22.7% / 16.7%); the human read of the listed samples is still owed |
| G0-ROUTE | Recorded (no pass threshold) |
| Spike 4 and frozen values files | NOT RUN (9 full panel launches, reserved for the orchestrator). Without them every launch except `R3_SMOKE=1` and `R3_SPIKE4=1` is refused at preflight (checked for all six panel and mode combinations, section 3) |
| One-package smoke test (15.5), both modes | Pass. The `PANEL_COLLAB=0` run was repeated on the rebuilt sandbox inside a file-hash pair (section 6) |

## 2. What was built (all paths relative to this folder)

| Path | What it does |
|---|---|
| `config/panels.json`, `config/packages.json`, `config/routing.json` | Panels el2 / sl2 / hl2, package base commits and masked paths, selection and routing rules. The surface regex was changed by the G0-SURF calibration (section 5) |
| `config/catalogue.json` | Moves M1-M10, generated verbatim from `merged-requirements.md` lines 184-193 |
| `config/phase1-brief.txt`, `phase2-frame.txt`, `fallback-frame.txt`, `reask-frame.txt` | Frozen prompt texts; the brief and the fallback frame were generated from `run-reviewer.sh` lines 13-17 |
| `config/pins.json` | sha256 of `judge-one.sh`, `findings.py`, `ledger.py`, `merge_cmd.py`, every other config file, plus the REPO commit (recorded, not checked) |
| `lib/common.sh` | Paths, guards (`r3_assert_writable`, `r3_assert_model`, `r3_assert_nofallback`), `r3_now`, `r3_event`, `r3_py`, admission (`r3_admission_ok`, `r3_admit`) |
| `lib/reviewer.sh` | Phase 1 (2 attempts, model check, H2 re-ask, seal 0444), phase 2 (resume, fresh fallback, deadline kill, phase-2 re-ask), `print-cmd` |
| `lib/package.sh` | One panel on one package: admission, T0, phase 1, 1 s scheduler, combine, merge, sealed merge, transcript capture, metrics, audit |
| `bin/launch-panel.sh` | The launch script: preflight, run record, three packages in parallel, anonymise, judge (at most 4 at once, one retry), results row, cleanup |
| `bin/build-sandbox.sh` | H3/H4 sandbox from the base commit; masked-path check; reuse or `E_SANDBOX_DIRTY` |
| `bin/cleanup-sessions.sh` | Queues this run's transcript files; deletes them only when no run uses the sandbox; `git clean -fdX` |
| `bin/spike-s2.sh` | Spike S2 (fresh, resume, killed resume) |
| `r3lib/cli.py` | Subcommands of design 2.3 plus helpers: `values-show`, `capture-sessions`, `judge-ok`, `p2check`, `reask-errors`, `errcount` |
| `r3lib/findings_io.py` | H2 normaliser, phase-2 extraction and salvage, combiner with self-check |
| `r3lib/digest.py` | Selection, router, deal, gap cards, slots, message lines, validator, prompt rendering |
| `r3lib/metrics.py` | `collab.json`, Jaccard, ECHO, audit, transcript capture, anonymiser, results row, arm summary, Fisher test |
| `r3lib/values.py` | n, k, finish offset, turn durations, p90, planning values, `freeze` |
| `r3lib/paths.py` | Roots and test overrides (overrides honoured only under `/tmp/`). Not in the design's file list; added to keep paths in one place |
| `ruff.toml` | Not in the design. Extends the repo's ruff settings and ignores four naming rules (N802, N803, N806, N812) because the code uses the design's own symbols (`T0`, `B`, `B_f`, `T_report_p90`, `F` for the findings module) |
| `tests/` | `conftest.py`, `fakes/claude`, `fakes/fake_claude.py`, `fakes/pgrep`, 22 test files |
| `spikes/` | `g0-h3/`, `g0-hooks/`, `g0-surf/`, `g0-route/`, `s2/<model>/` (plus `gpt-6-luna-kill12`, `-kill20`, `-kill25`, `-partial20`), `s3/`, `ac14/` (first pair) and `ac14/resume/` (second pair, logs of the resume session), `test-run.log` |
| `runs/`, `scoring/`, `results/smoke.jsonl` | The four smoke runs (section 6) |

Changes made in the resume session (all inside this folder): `lib/package.sh` no longer waits a fixed 5 s for three `timeout ... claude` processes to appear when all three phase-1 jobs have already ended (with the fast fake `claude` that wait used up the phase-2 time budget of F2, which failed three times in a row after a host restart); `tests/test_faults.py` F4 now sleeps 8 s so its "re-ask does not fit" timing no longer depends on that wait; F6 checks every gap draw (it had required one random draw, which made it fail about one run in three); `r3lib/metrics.py` lost a dead duplicate `"panel"` dictionary key and an unused variable; lint and formatting fixes across `r3lib/` and `tests/`; `ruff.toml` added.

## 3. How to run one panel on all three packages

Run from this folder. Every command that starts model sessions holds the shared gateway lock.

**Step 1, once per panel: Spike 4 and freeze the values file** (required by every non-smoke run; not done yet; verified: without `values/<panel>.json` all six launches below stop at preflight with `E_VALUES ... missing (only R3_SMOKE=1 or R3_SPIKE4=1 may run without it)` and start no session):

```bash
cd /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge
for i in 1 2 3; do flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_COLLAB=0 R3_SPIKE4=1 bash bin/launch-panel.sh el2 --tag spike4-$i; done
bash -c 'source lib/common.sh; r3_py values-freeze --panel el2 --runs <run_id 1> <run_id 2> <run_id 3>'
```

Repeat with `sl2` and `hl2` in place of `el2`. The run ids are printed on the last line of each launch (`run_id=...`).

**Step 2, one run per arm:**

| Panel | Collaboration on (arm A3) | Baseline, `PANEL_COLLAB=0` (arm A1) |
|---|---|---|
| ember + 2x luna | `flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_COLLAB=1 bash bin/launch-panel.sh el2` | `flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_COLLAB=0 bash bin/launch-panel.sh el2` |
| sonnet + 2x luna | `flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_COLLAB=1 bash bin/launch-panel.sh sl2` | `flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_COLLAB=0 bash bin/launch-panel.sh sl2` |
| haiku + 2x luna | `flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_COLLAB=1 bash bin/launch-panel.sh hl2` | `flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_COLLAB=0 bash bin/launch-panel.sh hl2` |

Each launch runs all three packages in parallel (9 reviewer sessions), judges with Opus (at most 4 judge sessions at once), and appends one row to `results/results.jsonl`. Exit codes: 0 all valid and judged, 1 preflight refused, 2 a package invalid or not judged, 3 audit violation. Summary: `bash -c 'source lib/common.sh; r3_py summarize --panel el2'`.

**Before the values files exist** only smoke runs start (planning values, rows to `results/smoke.jsonl`, not to `results/results.jsonl`): add `R3_SMOKE=1`, for example `flock /tmp/collab-gateway.lock env R3_SMOKE=1 NOFALLBACK=1 PANEL_COLLAB=1 bash bin/launch-panel.sh el2` (all three packages) or add `--pkgs TASK-WF-design-20261108-041415` for the control package only.

**Tests:** `PYTHONDONTWRITEBYTECODE=1 uv run --frozen --project /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel pytest -p no:cacheprovider .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests -q` (about 3.5 minutes; no model calls). The timing-sensitive fault tests (F2, F4, F17) use deadlines of 10 to 13 s; a heavily loaded host can still move them.

## 4. Test results

`spikes/ac14/resume/tests-final.log`: **89 passed, 0 failed, 0 skipped in 219 s**. Ruff: `ruff check` "All checks passed!" and `ruff format --check` "31 files already formatted" (`spikes/ac14/resume/ruff.log`).

| Group | Files | Count |
|---|---|---|
| Unit tests of 15.2 | `test_config`, `test_phase1_brief`, `test_command_diff`, `test_model_allowlist`, `test_h2`, `test_select`, `test_router`, `test_deal`, `test_gap`, `test_n`, `test_msg`, `test_combine`, `test_salvage`, `test_metrics`, `test_anon`, `test_result`, `test_values`, `test_judge_path`, `test_summary`, `test_guards`, `test_sandbox` | 65 |
| Fault injection of 15.3 (`test_faults.py`) | F1, F1b (n = 0 after fallback), F2-F13, F14, F14b (peer transcript), F14b (killed attempt), F15, F16, F16b (judge fails twice), F17, F18, F19, plus the fake start-up check | 24 |

Runs of the full suite in the resume session: first run 1 failed (F2, caused by the 5 s wait described in section 2), after that fix 88 passed and 1 failed (F4, timing), and after the F4 change 89 passed. F2, F3, F4 and F17 then passed three times in a row. `spikes/ac14/resume/tests.log` is the 88/1 run; `tests-final.log` is the passing run.

## 5. Spike results (records under `spikes/`)

| Spike | Result | Evidence |
|---|---|---|
| G0-H3 | PASS, re-run on the rebuilt sandboxes in the resume session. All three base commits equal the parent of the implementing commit; every masked path differs from the implementing commit or is absent at base; no package path and no `.dev/reflect` in any sandbox | `spikes/g0-h3/result.json` |
| G0-HOOKS | PASS. The sandbox's `Skill` PreToolUse hook script is missing, so it fails non-blocking (exit 127) in both arms; every review still finished with a valid block. No `.codegraph/` in the sandbox after the sessions (`SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`). Evidence comes from the smoke runs' sessions, not a separate ember session | `spikes/g0-hooks/result.json` |
| S2 resume | PASS for luna, ember, sonnet and haiku: resume exits 0 with the same session id, model identity holds, transcripts carry timestamps. Wall times for a one-line answer over all six S2 records: fresh 8.3-14.2 s, resume 5.5-7.3 s (planning: 16 s and 6 s) | `spikes/s2/<model>/result.json` |
| S2 kill mid-answer | FAIL for luna (required by the design). Five tries: with 25 s the answer finished before the kill; killed at 12 s and at 20 s, luna's stream held only `thinking` and `tool_use` events; a fourth try at 20 s with a prompt telling luna to write a sentence before every tool call also held no text; a fifth try in the resume session, at 20 s with `--include-partial-messages`, produced only `input_json_delta` and `signature_delta` events and no `text_delta` (`spikes/s2/gpt-6-luna-partial20/result.json`; a probe outside the design's 15.4 procedure, no code uses that flag). Luna writes its text in one final message, and the real smoke runs' killed luna phase 2 shows the same. A killed luna phase 2 therefore leaves nothing to salvage (risk X1 of the design is real). The `pass` field of every S2 record applies the design's kill condition: luna records show `pass: false`, `resume_pass: true` | `spikes/s2/gpt-6-luna-kill25/`, `-kill12/`, `-kill20/`, `gpt-6-luna/`, `gpt-6-luna-partial20/` |
| G0-SURF | Design regex FAILED the 15-30% band (ember 0.0%, luna 4.8%). Calibrated regex (adds artifact path/location, line anchors/numbers/references, `stale`) gives ember 22.7%, luna 16.7%; re-pinned. The human read of the 17 matches (all there are) and 20 sampled non-matches in `result.json` has NOT been done | `spikes/g0-surf/NOTES.md`, `result.json`, `result-starting-regex.json` |
| G0-ROUTE | Recorded at planning n over 36 historical EL2 receiver slots: 1.03 qualifying anchors per receiver on average, 9 of 36 receivers with none | `spikes/g0-route/result.json` |
| S3 (smoke, collab) | PASS: 0 dropped H2 lines, stream filters give model identity and tokens, merge, anonymiser and both judges succeed | `spikes/s3/result.json` |
| Spike 4 | NOT RUN (full panel launches are the orchestrator's) | none |

## 6. Smoke test (15.5), control package on el2, real models

Four smoke runs exist; their rows are in `results/smoke.jsonl`. All exited 0, had 0 audit violations, `contaminated: false`, `judge_ok: true`, no SLO breach, observed model equal to the requested model in every session.

| Run | Mode | Sandbox | Elapsed | Notes |
|---|---|---|---|---|
| `runs/el2-c1-20261113T210019Z-b40c` | `PANEL_COLLAB=1` | before the snapshot fix | 158.8 s | 3 phase-2 sessions launched; one luna killed at the deadline with 0 salvaged lines; 1 phase-2 finding in the final reports |
| `runs/el2-c0-20261113T210437Z-169d` | `PANEL_COLLAB=0` | before the snapshot fix | 95.2 s | no digest, no `p2.*` files |
| `runs/el2-c1-20261113T214437Z-42fb` | `PANEL_COLLAB=1` | rebuilt, with the fix | 158.8 s | 3 real and 3 gap challenges; one luna's phase 2 killed at the deadline; 0 ignored writes in the sandbox; `gt_text_leak` 0 |
| `runs/el2-c0-20261113T221655Z-2f0d` | `PANEL_COLLAB=0` | rebuilt from scratch in the resume session (`/tmp` was empty after a host restart) | 154.8 s | all 3 reviewers attempt 1, model identity true; no digest, no phase 2; `cleanup.json` clean; tokens 25,704 |

The first two runs used the sandbox from before the snapshot fix (its snapshot left out files tracked at the base commit that the base `.gitignore` matches; the collab run still had them on disk as ignored files, the cleanup after it deleted them, so the baseline run reviewed without them). They stand for the harness path, not for sandbox parity between arms. The last two runs are the post-fix pair. A single run's elapsed time says nothing about the arms: the baseline took 95.2 s once and 154.8 s once, because the slowest luna took 155 s in the second run.

AC-14: two file-hash manifests of `REPO/src` and `EVAL` (13,243 files each, `find -type f`, ignored files included, `__pycache__` excluded, `PYTHONDONTWRITEBYTECODE=1`) were each identical before and after:
- first pair (`spikes/ac14/`, 21:30:28Z to 21:47:49Z): sandbox rebuild, full tests, the post-fix `PANEL_COLLAB=1` smoke run;
- second pair (`spikes/ac14/resume/before.sha256` 22:13:09Z, `after.sha256` 22:20:02Z and `after2.sha256` 22:27:53Z; both after-files equal the before-file): sandbox rebuild from scratch, G0-H3, the full test run, the `PANEL_COLLAB=0` smoke run, the lint edits, the F4 and F2 reruns and the final full test run.

All four smoke runs found 0 of the 2 control ground-truth items (`control_found2` 0) and had 2, 2, 4 and 2 wrong blockers (`control_wrong_blockers`); single runs say nothing about quality.

## 7. Requirements and acceptance criteria not met, or met differently

| Item | State and reason |
|---|---|
| AC-3 (Gate 0 spikes pass) | Not met. S2's "text before a mid-answer kill" check fails for luna (section 5, five tries, including `--include-partial-messages`): luna sends no text before its final message, so the design's pass condition cannot be reached with any command or prompt tried. G0-SURF passes only after recalibrating the design's regex (the design allows that), and its human read is pending. G0-H3, G0-HOOKS, S3 and the resume part of S2 pass. Owner decision needed: accept the luna result as the design's risk X1 and drop the kill-text condition, or change the phase-2 design |
| AC-4 (frozen values file) | Not met. Needs Spike 4 (9 full launches), reserved for the orchestrator. Until then only `R3_SMOKE=1` and `R3_SPIKE4=1` runs start |
| AC-7, AC-11, AC-13, AC-15 over real arms | Shown only on the smoke runs and in fake tests; no non-smoke launch was run, so no row has reached `results/results.jsonl` |
| Surface regex (design 3.3) | Changed by calibration, as 3.3 allows; differs from the design's printed value |
| Salvage of a killed phase 2 (R-15) | Code and tests work on the fake; on real luna a kill yields no lines (S2), so the phase-2 time of a late luna can be spent for nothing |
| Phase-2 tokens of a killed session | Counted as 0: a killed stream has no result event, so `output_tokens` under-counts killed sessions |
| Resume-failure detection (7.3) | Checked when the process exits, not within the first 10 s |
| `pkg.json` sealed hashes (5.4) | The sealed sha256 is in `reviews/<rid>.p1.sha256` and `<rid>.meta.json`, not in `pkg.json` (three reviewers would write one file at once) |
| `pins.json` REPO commit | Recorded, not checked by `pin --check` (other sessions may commit while arms run) |
| Admission (13.3) | The `timeout ... claude -p --model` pattern also counts the implementer sessions of other designs on this host (they are launched that way), so admission headroom is smaller while they run |
| Fault-test values (15.3) | B_f is 40 s (10 s or 12 s where a deadline must be reached quickly), turn_p90 1.5 s, and el2's box cap of 35 s stays in force (the design says box cap null) |
| Fake `claude` | Runs the interpreter that uv resolved directly instead of `uv run`, so `timeout` signals reach the fake itself |
| `test_gap` "no peer id" | Checked on the rendered prompt only; the `panel-msg/1` line must carry `from` and `to` by schema |
| `test_config` ground-truth check | 12-character runs shared with `run-reviewer.sh` itself (", or when the") are allowed in the fallback frame, which quotes RR:17 verbatim |
| F17 test | Asserts that a late luna gets `no_launch_reason: deadline`; it does not pin which luna |
| Timing-sensitive tests | F2, F4 and F17 depend on 10-13 s deadlines; they failed after a host restart until the 5 s wait in `lib/package.sh` was removed and may move again on a heavily loaded host |
| `ruff.toml` | Added beyond the design; ignores four naming rules for the design's own symbols |
| HL2 shadow variant, arms A0 and A2, block scheduler | Not built (design 1.4) |

## 8. Review and ledger state

A fresh independent reviewer (not the implementer) graded the tree `b17c024f94be...` (worktree snapshot after the resume session's last edits to the harness; IMPLEMENTATION.md sections 1 to 7 as written then) against the 15 acceptance criteria of design 15.6. Result: AC-1, AC-2 and AC-5 to AC-15 met, and AC-4 met in the sense that this report states it is not met and why (the orchestrator's instructions reserve Spike 4); **AC-3 unmet** (finding F1.1, section 7). All other earlier findings (F1.2-F1.7, F2.1, F2.2) are resolved. The reviewer's own run of the test suite also gave 89 passed, 0 skipped.

Ledger `.dev/implement/collab-r3-axis-flip-challenge/progress.md`: T1 ends with `blocked verdict=missing ac=T1.AC3` and `halt review=2 reason=operator-review`. The task is NOT marked complete. It can only complete through a `Ruling:` line that records the owner accepting the luna result of S2 (nothing in the code can make luna write text before a kill), after which the executor appends the `complete` line. Review files and prompts are in `.dev/implement/collab-r3-axis-flip-challenge/retries/T1/` (`review-2.md` is the last review; `review-2.r2-1.preserved.md` is the earlier review it replaced).
