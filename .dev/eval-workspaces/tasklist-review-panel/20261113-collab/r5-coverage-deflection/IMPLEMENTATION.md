# Redesign 5 (coverage deflection): implementation record

Source: `DESIGN.md` in this folder. Ledger: `.dev/implement/collab-r5-coverage-deflection/progress.md`.
Written after a resume (the first implementation session was killed); every number below was re-measured or re-read on 2026-11-13 in the resumed session, not copied from the first session's claims.

**Status in one line:** the harness is built and its 108 tests pass; the Gate 0 spikes S-H3, S0, S2 and REQ-S3 ran; Spike 4 ran only as a one-package pilot; the F6 smoke test does NOT pass (sonnet is too slow with the catalogue kit, so the design's own rule refuses F6 on `sl2`). Acceptance criteria AC-4 and AC-5 are not met, and AC-7 is met only through one disclosed exemption (section 5). The ledger line for T1 is therefore `blocked`, not `complete` (section 7).

## 1. What was built

Every file is under this folder (`R5`). Nothing was written to `src/`, `tests/`, `.claude/`, `.dev/tasks/`, the `20261111-a1` eval folder or another redesign's folder. Scratch: `/tmp/evalsb-collab-r5/` (sandboxes, pytest temp) and `/tmp/collab-r5/` (launch logs, the diagnostic config). `/tmp` was cleared once between the two sessions, so the sandbox of the control package was rebuilt (`bin/sandbox-build.sh`) before the diagnostic row.

| Path | What it is |
|---|---|
| `config/panels.json` | The three panels `sl2`, `hl2`, `el2`: reviewer ids, models, receiver/scout roles, planning B per package, `min_calls` 6, deal `single`/`split` (DESIGN 3) |
| `config/bases.json` | H3 base commit per package (the squash commit's only parent, DESIGN 0.2) |
| `config/catalogue.md` | Moves M1-M10, the "Move (text sent to a reviewer)" column of `merged-requirements.md:184-193` copied exactly |
| `config/surface.regex` | The surface-finding pattern of DESIGN 1.1, one line |
| `config/templates/*.txt` | `brief-a1.txt` (the `run-reviewer.sh:13-17` brief with `{CAND}`, `{SHA}`, `{SOURCE}` and the H1 sentence), `brief-kit.txt` (heading line; the runner appends `catalogue.md`), `brief-receiver-f6.txt`, `card-1.txt`, `card-2.txt`, `finish.txt` |
| `config/pins.json` | sha256 of `judge-one.sh`, every config file and template, and the worktree and installed `findings.py`/`ledger.py` (D10) |
| `config/values/` | Empty on purpose: the full Spike 4 (orchestrator) writes `values/<panel>/<pkg>.json` and `SHA256SUMS` here |
| `bin/sandbox-build.sh` | Builds `/tmp/evalsb-collab-r5/<pkg>/repo` from the base commit minus `.dev/{tasks/done,eval-workspaces,research,reflect}`, plus `cand/<pkg>/{candidate,source}.md` and `manifest.json` |
| `bin/run-reviewer-r5.sh` | One reviewer: H1 brief (+ kit, + receiver line), at most 2 attempts, hang guard via `timeout`, atomic meta write, session copy, H2 normalise and one `--resume` re-ask (stream-json), cost and timing files. Refuses without `NOFALLBACK=1`; no fallback ladder |
| `bin/run-panel.sh` | One panel on one package: T0, values check, settings files, watcher, reviewers, tagger, collab, alarms, audit |
| `bin/hook-posttool.sh` | Receiver PostToolUse hook: subagent skip, call count, finish signal, `min_calls` gate, seal before the first delivery (fail closed), newest-card delivery with supersede, logs |
| `bin/merge.sh`, `bin/anon.sh`, `bin/judge.sh` | Merge (arguments of `merge-b11.sh:34`), anonymise for the blind judge (DESIGN 5.3), call the unchanged `judge-one.sh` in place through a relative combo path (D9) |
| `bin/launch.sh` | One panel on the requested packages: preflight (exit 2/3), run, merge, anonymise, judge, results row |
| `bin/pins-check.sh` | Checks `pins.json`, values sums and `audit static`; `--write` regenerates `pins.json` (an addition: the design names no way to create the file) |
| `lib/r5/__init__.py` | Paths (with `R5_*` env overrides for tests), JSON helpers |
| `lib/r5/panelmsg.py` | `panel-msg/1` validator for kind `coverage` (DESIGN 2.2) |
| `lib/r5/coverage.py` | Task index, Task of a finding, surface filter, declared not-checked, rank (D4), `next_card` (D3, EL2 deal), `render_card` |
| `lib/r5/watcher.py` | Poll loop: scout meta, parse, coverage log, rank, validated card append under `flock` |
| `lib/r5/h2.py` | Anchor/claim truncation, real-parser errors, re-ask prompt, re-ask decision |
| `lib/r5/timing.py` | `k`, finish/hang offsets, slowdown limit, session turn parser, `spike4` values writer |
| `lib/r5/tagger.py`, `collab.py`, `alarms.py`, `results.py`, `audit.py` | Peer/own sidecar tags; `collab.json` (R-23 keys in every arm); alarms and arm summary; results row; static and per-package audit |
| `ruff.toml` | Lint config for this folder: the repository rules minus the naming rules N803/N806 (the design's own formula names `B`, `B_f`, `T0`). Added in the resume |
| `spikes/s0-hooks.sh`, `s2-resume.sh`, `reqs3-act.sh`, `spike4.sh`, `smoke-check.sh` | Gate 0 spikes (real models) and the smoke checker; each appends to `spikes/NOTES.md`. `spike4.sh` now creates `/tmp/collab-r5` itself (resume fix) |
| `spikes/NOTES.md`, `spikes/out/` | Spike records and transcripts |
| `tests/conftest.py`, `tests/fake/claude`, `tests/fixtures/` | Fixtures (synthetic ground truth only), fake `claude` (bash), copies of the three candidates and `resolution-live7.json` |
| `tests/test_*.py` | T-1 to T-22 and F-1 to F-17 (section 3) |
| `tests/last-run.txt` | Output of the AC-1 command (re-run in the resume) |
| `runs/`, `scoring/`, `results/` | Outputs of the Spike 4 pilot, the smoke launches and the diagnostic row (section 4) |

## 2. How to run one panel on all three packages

One launch runs one panel on all three packages (designSpec, alias, control, one after another), then merges, anonymises, judges (Opus, one package at a time) and writes `results/<row>.json`. Row names must be new; a launch never reuses a row folder. Run from the repository root:

```bash
cd /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
export NOFALLBACK=1
R5=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r5-coverage-deflection
```

**Prerequisite, once per panel (the full Spike 4, not run by this implementer):** it writes the frozen `config/values/<panel>/` files that every non-spike launch needs (4 A1 and 2 A2 launches per panel, each holding the gateway lock):

```bash
bash $R5/spikes/spike4.sh el2
bash $R5/spikes/spike4.sh sl2
bash $R5/spikes/spike4.sh hl2
```

**F6 (collaboration on; `PANEL_COLLAB=1` forces the kit):**

```bash
flock /tmp/collab-gateway.lock env PANEL_COLLAB=1 bash $R5/bin/launch.sh el2 f6-el2-r01   # ember + 2x luna
flock /tmp/collab-gateway.lock env PANEL_COLLAB=1 bash $R5/bin/launch.sh sl2 f6-sl2-r01   # sonnet + 2x luna
flock /tmp/collab-gateway.lock env PANEL_COLLAB=1 bash $R5/bin/launch.sh hl2 f6-hl2-r01   # haiku + 2x luna
```

**`PANEL_COLLAB=0` baseline (A1: no hooks, no watcher, no board, no kit):**

```bash
flock /tmp/collab-gateway.lock env PANEL_COLLAB=0 PANEL_KIT=0 bash $R5/bin/launch.sh el2 a1-el2-r01
flock /tmp/collab-gateway.lock env PANEL_COLLAB=0 PANEL_KIT=0 bash $R5/bin/launch.sh sl2 a1-sl2-r01
flock /tmp/collab-gateway.lock env PANEL_COLLAB=0 PANEL_KIT=0 bash $R5/bin/launch.sh hl2 a1-hl2-r01
```

The static-kit comparator A2 is the same with `PANEL_COLLAB=0 PANEL_KIT=1`. Drop the `flock ...` prefix when the gateway is not shared. Add `--pkgs <full package id>[,<id>...]` to run fewer than three packages. Exit codes: 0 complete, 1 partial or quarantined (the row file says which), 2 preflight refused, 3 F6 not runnable on that panel (no values, values sum mismatch, `budget_ok` false, or k = 0 on every package; the reason is on stderr and in `runs/<row>/launch.json`). Per-arm alarms after a block: `cd <repo> && PYTHONPATH=$R5/lib uv run python -m r5.alarms arm F6-sl2 f6-sl2-r01 ...`; run the A1 arm summary first (`... r5.alarms arm A1-sl2 a1-sl2-r01 ...`) so the package alarms have their reference.

**What to expect on the three panels with today's evidence (measured, not planned):** on `sl2` the pilot gave sonnet turn_p90 26.6 s, T_report_p90 43.5 s, so k = 0, and a kit slowdown of 0.59 against a limit of 0.34 (`budget_ok` false); an F6 launch on `sl2` is therefore refused with exit 3 unless the full Spike 4 gives different values (the pilot had 2 A1 and 1 A2 runs on one package). `hl2` is expected to be refused as well (DESIGN 3.2), and REQ-S3 measured haiku acting on an injected request in 0 of 5 trials (section 4). `el2` has no measurement of its own yet: Spike 4 for `el2` has not run.

## 3. Test results

Command (AC-1, run exactly as DESIGN 6 states, from the repository root):

```bash
mkdir -p /tmp/evalsb-collab-r5 && PYTHONPATH=$R5/lib uv run pytest -p no:cacheprovider --basetemp=/tmp/evalsb-collab-r5/pytest $R5/tests -v -rs
```

Result (re-run in the resumed session, twice: once before and once after the lint fixes below): **108 passed, 0 failed, 0 skipped in 97.06 s** (full log of the last run: `tests/last-run.txt`, ending `rc=0`). Tests never call a model and never open a real `ground-truth.json` (fixtures carry synthetic ground truth; the fake `claude` is first on `PATH`).

Lint: `uv run --no-sync ruff check` over `lib/` and `tests/` found 25 errors at the start of the resume (import order, an unused import, and naming rules on the design's formula names). `ruff --fix` fixed the 10 import and unused-import ones; the 15 naming ones are switched off for this folder by `ruff.toml` (they would force renaming `B`, `B_f`, `T0` away from the design's notation). The check now reports no errors. `ruff format` was not applied (25 files would be reformatted; the design does not ask for it).

| File | Tests | Covers |
|---|---|---|
| `test_panelmsg.py` | 20 | T-1 |
| `test_coverage.py` | 6 | T-2 to T-7 |
| `test_watcher.py` | 4 | T-8 |
| `test_hook.py` | 7 | T-9 (a)-(h); F-3 (missing transcript and read-only snapshot folder), F-4, F-15 at hook level |
| `test_h2.py` | 3 | T-10 |
| `test_cmdline.py` | 3 | T-11 (AC-6) |
| `test_timing.py` | 13 | T-12, T-13 |
| `test_tagger_collab.py` | 3 | T-14, T-15 |
| `test_alarms_results.py` | 5 | T-16, T-17 |
| `test_audit.py` | 8 | T-18 |
| `test_anon_judge.py` | 5 | T-19, T-21 |
| `test_launch_preflight.py` | 11 | T-20, T-22, F-10, AC-10 (hl2 with k = 0 everywhere exits 3 with the reason) |
| `test_faults.py` | 20 | F-1 (A1 and F6), F-2, F-5, F-6, F-7, F-8, F-9 (a), (b), (c), F-11, F-12, F-13, F-14, F-15 end to end, F-16, F-17 (finish signal once plus hang kill, and over-cap budget), AC-10 (el2: one card per luna, disjoint), an F6 happy path |
| **Total** | **108** | |

Where a test checks less than the DESIGN wording:

- F-1 checks the kill lands within 2 s of `hang_ms` (exit 124, `hang_kill: true`, `SLO_BREACH`, the scouts unaffected).
- F-15 end to end checks that a subagent call is logged and not served and that a later main call delivers; it does not force the subagent call to be exactly the first call after a card (the hook-level test does).
- F-17 checks the two sides separately: a receiver that keeps calling tools gets the finish text once and is hang-killed (`SLO_BREACH`); a run that ends after 1.35 B_f but before 1.5 B_f is `over_cap`.
- T-22 and T-21 are in `test_launch_preflight.py` / `test_anon_judge.py` rather than in files named `test_sandbox.py` / `test_judge_path.py` as the design's table names them (the cases are the same).

## 4. Spike and smoke-test results

All spike text, commands, dates and transcript folders are in `spikes/NOTES.md` and `spikes/out/`. Model sessions of the first session were reused, not repeated.

| Spike | Result | Evidence |
|---|---|---|
| S-H3 sandbox build | PASS. Three base SHAs in the manifest; `.dev/reflect`, `.dev/research`, `.dev/eval-workspaces`, `.dev/tasks/done` absent; clean `git status`; no `merge-guard.md` in the designSpec sandbox; `test_worker_contract.py` in the control sandbox | `spikes/out/s-h3/build.log` |
| S0 hooks (sonnet, haiku, luna) | PASS on all three: hook fired on every main tool call, card text in the transcript, snapshot sha ok, hook p95 59 / 57 / 85 ms, 0 subagent calls | `spikes/out/s0/20261113T205926Z/` |
| S2 resume (sonnet, haiku, luna, ember) | PASS on all four: same model after `--resume`, answer carries the earlier context, resume wall 5.1 to 6.2 s | `spikes/out/s2/20261113T210335Z/` |
| REQ-S3 act rates | RECORDED, no threshold. Act on an injected request / end after the finish text: sonnet 5/5 and 5/5; haiku 0/5 and 0/5; luna 1/5 and 3/5. Haiku saw the text (probe string present in its transcripts) and did not act | `spikes/out/reqs3/20261113T210646Z/` |
| Spike 4, pilot only | Ran on sonnet + 2x luna, control package, 2 A1 and 1 A2 launches (not 4 + 2, one package, one panel). Values (scratch config, copied to `spikes/out/spike4-pilot/`): B_f 176.9 s, turn_p90 26.6 s, T_report_p90 43.5 s, **k = 0**, kit slowdown 0.592 against limit 0.339, **`budget_ok` false**. The NOTES.md heading says PASS because the script ran to the end; the values themselves say F6 is not runnable on `sl2` at these numbers | `spikes/out/spike4-pilot/values/sl2/` |
| Smoke F6 row `smoke-f6-sl2-1` | REFUSED by `launch.sh`, exit 3, before any model call: "budget_ok false ... slowdown 0.592 > limit 0.339" (the design's run condition, DESIGN 5.1 step 5). **Both smoke rows (this one and the A1 row below) ran with `R5_CONFIG` pointing at the scratch pilot config (`/tmp/collab-r5/config-pilot`, now cleared; its values file is kept in `spikes/out/spike4-pilot/`).** With the committed `config/`, whose `values/` folder is empty, the same command is refused earlier with "no values file for <pkg> (run Spike 4)" (`bin/launch.sh:43`) | `runs/smoke-f6-sl2-1/launch.json` |
| Smoke A1 row `smoke-a1-sl2-1` | (pilot config, see the row above) PASS on every A1-side item: exit 0, status complete, three models ok, 0 dropped lines, 3 reviewer ids in the merge, no `board/`, no `--settings`, F6 fields null, anon post-check 0, score parsed, audit pass, 180.3 s (1.9% over B_f) | `results/smoke-a1-sl2-1.json`, `runs/smoke-a1-sl2-1/` |
| Diagnostic F6 row `smoke-f6diag-sl2-1` | Not a valid F6 measurement: ran with `k` forced to 1 and `budget_ok` forced true in a scratch config (`/tmp/collab-r5/config-diag`, a copy of `config/` plus the pilot values file, sums regenerated). It proved the real-model chain: scouts finished at about 124 s and 144 s, one card `["T5"]` validated and posted, delivered to sonnet at its call 18 four seconds later, seal and sha ok, `hook_error` 0, hook p95 27 ms, second card correctly `dup_card`, card and finish text present in the real session transcript. Then sonnet ran to the hang guard (killed at 266.4 s = 1.5 x B_f, `SLO_BREACH`, no valid report, recorded INVALID in the merge), so the row is `quarantined`. Against the 7 smoke items: 1, 2, 3, 6, 7 FAIL, 4 partial (card text is only in the uncopied session file), 5 PASS (A1 row) | `runs/smoke-f6diag-sl2-1/`, `results/smoke-f6diag-sl2-1.json`, `spikes/NOTES.md` (last section) |

Models used in the resume: claude-sonnet-5-5 and gpt-6-luna x2 (the diagnostic row, three sessions at once) and claude-opus-5-5 as the blind judge, all with `NOFALLBACK=1`. No Qwen, glm, or other model.

Observed harness limit (not fixed, not in the design): when a reviewer is hang-killed, the runner has no session id and does not copy the session file, so `smoke-check.sh` item 4 cannot see the card text. The card text is in the file under `~/.claude/projects/` (path in `spikes/NOTES.md`).

## 5. Requirements and acceptance criteria not met

| Id | Status | Reason |
|---|---|---|
| AC-1 | MET | 108 passed, 0 failed, 0 skipped (section 3) |
| AC-2 | MET in substance; the literal `find` check prints cache folders | `git status --porcelain -- src/ .claude/` is empty; `find EVAL -newer R5/.build-start` prints nothing; the grep for other redesigns' folders finds nothing. `find REPO -maxdepth 1 -newer R5/.build-start` prints `.`, `.pytest_cache`, `.ruff_cache`, `.claude`, `.codegraph`: gitignored tool and cache folders. This resume's commands used `-p no:cacheprovider` and `--no-cache`, but the independent reviewer's own ruff run, the sibling session and the tools themselves also write there, so none of the five names can be attributed to the R5 build with certainty (`.pytest_cache` holds only test ids of another redesign, per the reviewer). They were not deleted (the resume rules forbid deleting). The literal AC-2 command therefore does not print nothing |
| AC-3 | MET | `sha256sum judge-one.sh` is `a01bd70d...cfcc` after the smoke and diagnostic launches |
| AC-4 | NOT MET | S-H3, S0 and S2 are recorded PASS and REQ-S3 is recorded with its act rates, all dated before the smoke rows. Missing: (a) the full Spike 4 on three panels (the orchestrator runs it; only a one-package pilot ran), so there are no frozen values files and no PASS Spike 4; (b) the owner's decision for haiku, whose act rate is 0/5; (c) a Spike 5 result from the shared plan or the owner's waiver |
| AC-5 | NOT MET | The F6 smoke row is refused by the design's own rule (k = 0, `budget_ok` false on the pilot values); the forced diagnostic row fails smoke items 1, 2, 3, 6, 7 because the sonnet receiver runs past the hang guard with the catalogue kit |
| AC-6 | MET | `test_cmdline.py` (3 tests) pass |
| AC-7 | NOT MET literally; passes only through a disclosed exemption | `pins-check.sh` prints `OK   audit static`, but only because `audit.static` exempts 12-character windows that also occur in the historical `run-reviewer.sh` brief (`lib/r5/audit.py:35`, section 6 row 1). Without the exemption `config/templates/brief-a1.txt` shares one 12-character window with a designSpec `plan_quote` (the independent reviewer recomputed it). The cause is a conflict inside the design: R-05 and T-11 require that brief byte-identical to the historical one, and AC-7 forbids the window. Needs an owner decision (amend DESIGN 2.10 or change the brief wording) |
| AC-8 | MET for real launches; not asserted for fake logs | Every real `launch.json` lists only claude-sonnet-5-5 and gpt-6-luna and `NOFALLBACK: 1`; `test_launch_preflight.py` refuses panels with glm, Qwen or Opus models; Opus ran only inside `judge-one.sh`. No test reads the fake-claude `FAKE_LOG` to assert the allow-list; the panels those tests run use the allowed models from `config/panels.json` |
| AC-9 | MET on the diagnostic board | its one card has exactly the keys `v,id,run,from,to,t,kind,items`, 1 item (k = 1), was posted and delivered before `finish_ms`; no card after it |
| AC-10 | MET | hl2 with k = 0 everywhere exits 3 with the reason; el2 gives at most one card per luna (fixture runs in `test_launch_preflight.py` and `test_faults.py`) |

Open design questions that the results now bear on (owner decisions, not made here): DESIGN Q2 (what to drop from the kit when the receiver's slowdown exceeds the limit: the pilot shows 0.59 against 0.34 on sonnet) and the haiku 0/5 act rate. Not built, by design: the block scheduler, the interim futility look and the Fisher and permutation tests (DESIGN Q4); Spike 5 (DESIGN Q5).

## 6. Deviations from DESIGN.md

| # | Where | What differs from DESIGN.md, and why |
|---|---|---|
| 1 | `lib/r5/audit.py` `static` (R-07, AC-7) | 12-character windows that also occur in the historical brief of `run-reviewer.sh:13-17` are exempt from the window check. `brief-a1.txt` must stay byte-identical to that brief (R-05, T-11), and it shares the generic phrase "or when the" with one designSpec `plan_quote`; that text was in every historical run, so it carries no ground-truth information. Without the exemption AC-7 and AC-6 cannot both pass. Card texts are checked without any exemption (every possible 1- and 2-Task card was checked: 0 hits). |
| 2 | `config/templates/brief-kit.txt` | Holds only the heading line; `run-reviewer-r5.sh` appends `catalogue.md` after it, so the move text exists in one file only. The brief the reviewer receives is the same. |
| 3 | `bin/pins-check.sh` | Added `--write` (the design names no way to create `pins.json`). Exit 3 when only a values sum fails, so `launch.sh` can report that as "F6 not runnable" (exit 3, F-10) instead of a generic preflight refusal (exit 2). |
| 4 | Spike 4 | Run as a pilot only (sonnet + 2x luna, control package, 2 A1 + 1 A2 one-package launches) because the orchestrator runs full panel runs; its values went to a scratch config (`/tmp/collab-r5/config-pilot`, copied to `spikes/out/spike4-pilot/`) so `config/values/` stays empty for the real Spike 4 and its write-once rule. |
| 5 | `lib/r5/collab.py` | `scout_covered_tasks`, `receiver_anchored_tasks`, `deflection_overlap`, `union_anchored_tasks`, `k0_isolated` and `slo` are computed in every arm, not only F6, because the DEFLECTION alarm compares F6 with the A1 mean union. The card and request fields are `null` outside F6, as specified. |
| 6 | `tests/test_coverage.py` T-4 | The design does not list the 9 surface and 5 real claim sentences it checked; the test uses sentences written to the same descriptions (artifact outside permitted locations, edits under `.claude/`, sha256, line number, output path; single-select read-back, mode label vs two writes, unbounded "every", worker-contract test never updated, halt mapping). |
| 7 | Scripts | Python runs as `uv run --no-sync python -m r5.<module>` (so a launch never re-syncs the shared `.venv`); the tests use the design's exact `uv run pytest` command. Every path has an `R5_*` environment override (`R5_OUT`, `R5_SB`, `R5_EVAL`, `R5_CONFIG`, `R5_PINS`, `R5_REPO`, plus `CLAUDE_PROJECTS_DIR`, `SUPERCLAUDE`, `R5_POLL_S`) used only by the tests, the pilot and the diagnostic row; the defaults are the design's paths. |
| 8 | `spikes/s0-hooks.sh` | Uses `min_calls` 2, not 6, because the S0 task makes only 4 tool calls. |
| 9 | `bin/run-reviewer-r5.sh` | `DRY_RUN=1` also prints the attempt-2 command and the re-ask command (T-11 checks them). In `SPIKE4=1` mode the re-ask time gate uses a planning turn of 14 s. |
| 10 | `bin/merge.sh` | No stale-round retry (`merge-b11.sh:36-39`): every row folder is new, so a stale ledger cannot exist. |
| 11 | Smoke test | Under the pilot values the design's F6 smoke row is refused (k = 0). The one extra diagnostic F6 row, `smoke-f6diag-sl2-1`, ran with k forced to 1 and `budget_ok` forced true in a scratch config to exercise the real-model card chain; it is not a valid F6 measurement (section 4). It stays in `results/results.jsonl` as `quarantined`; its row name marks it. |
| 12 | `ruff.toml`, `spikes/spike4.sh` (resume) | Added a folder lint config (naming rules off) and a `mkdir -p /tmp/collab-r5` in `spike4.sh`; neither changes behaviour. Import order was fixed by `ruff --fix` in `lib/` and `tests/`; tests re-ran green. |

## 7. Things the orchestrator must know (found by the independent review)

- **Staging.** The repository `.gitignore` ignores `lib/` (line 13) and `*.log` (line 79). So `R5/lib/r5/*.py`, the whole Python half of this build, and every `*.runner.log` and `spikes/out/**/build.log` are silently skipped by `git add .dev/eval-workspaces/...`. `git check-ignore -v R5/lib/r5/watcher.py` confirms it. Staging them needs an explicit force-add, or an owner decision to rename `lib/` (the design mandates `R5/lib`). Nothing was staged or committed here.
- **Ledger state.** `.dev/implement/collab-r5-coverage-deflection/progress.md` ends with `T1: blocked verdict=missing`, because the independent review confirmed that AC-4, AC-5 and (literally) AC-7 are unmet. The retry ladder was not run: its advisers need Opus or other models that the orchestrator's model list forbids, and no retry can produce a full Spike 4 or make sonnet fast enough. A resume of this ledger goes to an operator review of the tree as it stands. The way to a `complete` line is a Ruling from the user that accepts, as explained here, the gaps in AC-4 (full Spike 4, haiku decision, Spike 5), AC-5 (smoke test fails on sonnet's kit slowdown) and AC-7 (design conflict).
- **Sonnet + kit is the blocker for `sl2`.** Pilot: A1 about 177 s to 180 s, A2 281.6 s, F6 diagnostic killed at 266.4 s. If the full Spike 4 confirms this, the design's own Q2 applies (cut the kit down to the moves that fit) before any F6 row on `sl2` can run.
