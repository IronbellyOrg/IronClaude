# Redesign 4, Flag-and-Adjudicate (F7): implementation and test design

Grounding: index_state: fresh (checked_at 2026-11-13T19:30:57Z, projectPath /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel); codegraph tools used: codegraph_status, codegraph_files, codegraph_node (symbolsOnly outlines of findings.py and merge_cmd.py; symbol merge_round); every quoted line was re-read with Read or a shell print.

Review status: three independent reviews (`design-report/review-1.md`, `review-2.md`, `review-3.md`), the cap of the review loop. Review 1 found 6 blocking defects and review 2 found 2; all were fixed and confirmed fixed by the next review. Review 3 (verdict FAIL) found 3 more blocking defects: the home-directory audit rule would flag the brief's own required read of `~/.claude/rules/...`; a killed reviewer's transcript was located by guessing; and the content audit's coverage was overstated. Fixes for all three are in this version (2.10 audit layers, deviation D-5 `--session-id`, the corrected coverage statement) but **have not been re-reviewed**, because the loop allows no fourth review. Review 3's minor findings m3-1 (the concurrency pattern assumes the wrapper's direct-exec path) and m3-6 (the judge step does not wait on the concurrency limit) are not addressed; S0 re-checks the pattern.

## 0. Scope, sources and decisions

**What this builds.** A self-contained harness that runs one review panel (a flagger plus two luna adjudicators) on the three study packages, either with the Flag-and-Adjudicate exchange (`PANEL_COLLAB=1`) or isolated (`PANEL_COLLAB=0`, the arm-A1 baseline), merges each package with `superclaude review merge`, anonymises, judges with the unchanged `judge-one.sh`, and writes one results row.

**Path names used below.**

| Name | Absolute path |
|---|---|
| `REPO` | `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel` |
| `R4` | `REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r4-flag-and-adjudicate` (all code and outputs) |
| `EVAL` | `REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1` (read only: candidates, ground truth, resolution files, `judge-one.sh`) |
| `SBR` | `/tmp/evalsb-collab-r4` (sandbox root: sandboxes, candidate copies, boards, judge staging) |
| `REQ` | `REPO/.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md` (source of truth) |

**Sources read for this design** (all re-read in this run): `REQ` sections 1, 2.0, Redesign 4, 3, 4 and 5.1-5.10; `EVAL/tools/run-reviewer.sh` (called `RR` below, as in `REQ`); `EVAL/tools/tmp-scripts/judge-one.sh`, `anon-b11.sh`, `anon-arms.sh`, `b4-job-one.sh`; `EVAL/analysis/merge-b11.sh`, `b11-launch.sh`, `final-table.py`; `EVAL/combos/SPEC.md`; `REPO/src/superclaude/cli/review/findings.py` and `merge_cmd.py`, and `merge_round` in `ledger.py`; the Claude Code hooks reference (code.claude.com/docs/en/hooks) and `claude --help` (version 2.1.323).

**Isolation rule.** Every file this design creates lives under `R4` or `SBR`, apart from two kinds it does not own: the short-lived judge staging directories `/tmp/jdg.XXXXXXXX` (unique names from `mktemp`, deleted on exit, decision 6) and Claude Code's own session transcripts under `~/.claude/projects`, which every `claude -p` run writes once `--no-session-persistence` is removed (R-05). Nothing is written under `REPO/src/`, under `EVAL`, or under any other `20261113-collab/r*` folder. `EVAL` is read only (candidate, `ground-truth.json` at scoring time only, `resolution-live7.json`, `judge-one.sh`). Five implementers can therefore build in parallel.

**Facts this design relies on, verified on disk in this run.**

| Fact | Evidence |
|---|---|
| The findings parser accepts extra keys on a line and checks only id, severity, blocking, category, anchor (12-200 flattened characters), anchor2, refs (at most 8), claim (at most 300) | `REPO/src/superclaude/cli/review/findings.py:90-121` |
| A merge round is refused only when no reviewer has a valid block; an invalid block's parsable lines are kept | `ledger.py:107-157` (`merge_round` docstring and the `LedgerError` raise) |
| `superclaude review merge` options: `--ledger --doc --round --report RID=PATH (repeat) --resolution --out --cap` | `merge_cmd.py:21-71` |
| `judge-one.sh` hard-codes `EVAL`, takes args `C P L`, reads `$EVAL/$P/ground-truth.json` and `$EVAL/$P/candidate.md`, and writes `judge.json`, `judge.err` and `score.json` into `D="$EVAL/arms/scoring/combos/$C/$P/$L"` | `judge-one.sh:4-27` |
| `RR` line 48 is the launch command the baseline must match | `RR:48` |
| H3 base trees exist: each package's `progress.md` records `T1: start sha=<tree>`, the git tree object in force when implementation began (a tree, not a commit), and `git archive <tree>` works on each | `REPO/.dev/tasks/done/<pkg>/progress.md` line 3; `git cat-file -t` gives `tree`; `git archive` listed 18,513 / 15,604 / 19,537 files |
| The base trees contain every leak directory R-03 removes (`.dev/reflect` 1,675 / 1,334 / 1,847 files, plus `.dev/eval-workspaces`, `.dev/research`, `.dev/tasks/done`) | same `git archive` listings |
| PostToolUse hooks inject text by printing `{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"..."}}` and exiting 0; hook input carries `session_id`, `transcript_path`, `cwd`, `hook_event_name`; default command timeout 600 s, settable per hook; hooks merge across settings sources | hooks reference, fetched this run |
| `claude` 2.1.323 accepts `--settings <file-or-json>`, `--resume`, `--output-format stream-json`, `--verbose`, `--no-session-persistence` | `claude --help` |
| `jq`, `flock` and `timeout` are installed; `bats` is not, so shell is tested from pytest through `subprocess` | `which` |

**Design decisions taken here (each traced to `REQ` or stated as a deviation).**

1. **One implementation per rule.** The card schema check lives in one jq filter (`lib/card.jq`) used by both the writer (`panel-post`) and the reader (`r4-hook`). The k formula lives only in `lib/values.py`. The 12-character overlap test lives only in `lib/collab.py`.
2. **Deviation D-1: peer tags are a sidecar, not a key inside the findings line.** `REQ` R-10 says the harness tags a line `"origin":"peer"`. This design writes the tags to `runs/<row>/<pkg>/tags/<rid>.json` (`{fid: "own"|"peer"}`) and leaves the report the merge reads byte-identical to the normalised report. Reason: R-04 requires the merge input to be the reviewer's single findings-v1 block, and a sidecar can never leak into the judge's input. Every metric that reads `origin` reads the sidecar.
3. **Deviation D-2: the card helper is called by absolute path, not through `PATH`.** `REQ` 2.0 says `panel-post` is "on `PATH`". The flagger's brief names the absolute path of a per-reviewer wrapper that bakes the board path, reviewer id, cap and deadlines into its command line, which is the same no-environment rule R-21 sets for hooks.
4. **Hooks are bash plus jq, never `uv run`.** A hook runs after every tool call and the budget is about 0.1 s per call (`REQ` 2.0, timing constants); starting Python through `uv` costs more than that. Everything that runs after the reviewers exit is Python run with `uv run --frozen --project REPO python <file>`.
5. **No model fallback ladder.** `NOFALLBACK=1` is required; the copied reviewer script has no ladder at all, so no model outside the allowed set (ember, luna, haiku, sonnet, grok; the three panels use only the first four; Opus only as the judge) can ever run. The retry loop of `RR:61-64` is kept (R-44).
6. **The judge runs unchanged.** `judge-one.sh` is called byte for byte (sha256 pinned). Its output directory `D` is steered outside `EVAL` by passing a relative `C` that climbs out of `EVAL/arms/scoring/combos` into a short-lived staging directory `/tmp/jdg.XXXXXXXX` made by `mktemp -d` (section 5.1, step 5). The judge's brief then shows only a random path and a random label, so it cannot tell the arm. The staging directory is **not** under `SBR` and is deleted as soon as its results are copied back, because the judge's `judge.json` holds the ground-truth text it read.
7. **Deviation D-3: the H3 base is the T1 start tree, not a commit.** `REQ` R-03 asks for "the commit the plan was written against (the parent of its first implementing commit)". The packages were squash-merged, so that parent cannot be identified with certainty, while each package's ledger records the exact tree in force when implementation began (`progress.md` line 3, `T1: start sha=<tree>`). `git archive` accepts a tree id, so the sandbox is built from that tree. `manifest.json` also records, for comparison, the parent of the first commit that touched the package folder and whether its tree equals the T1 tree.
8. **Deviation D-5: `--session-id <uuid>` is added to the reviewer launch line.** R-05 lists the allowed differences from `RR:48` and this is not among them. Without it, the transcript of a reviewer killed by the hang guard can only be guessed among sessions that share the sandbox's project directory. The flag names the session file; it changes nothing the model receives. S2 confirms it works with `-p` on each model.
9. **Deviation D-4: Spike 5 is not run by this build.** `REQ` R-27 lists Spike 5 (re-scoring 30 historical runs to measure the H2 part of the harness share) among the Gate 0 spikes. It measures a share this folder does not report (H needs arm A0, risk 9), so it stays with the overall experiment.

## 1. Files to create

All paths are relative to `R4` unless they start with `SBR`. Shell files start with `#!/usr/bin/env bash` and `set -u -o pipefail` (as `RR:4`) and are executable. Python files use the standard library plus `superclaude.cli.review.findings` (installed editable in `REPO`), and run as `uv run --frozen --project REPO python R4/lib/<file>.py ...` (`--frozen` so `REPO/uv.lock` is never rewritten). Size estimates are lines of code.

### 1.1 Frozen inputs (pinned by sha256 before the first run)

| Path | Purpose | Content and interface |
|---|---|---|
| `frozen/packages.json` | The three packages and their H3 trees | `[{"id":"TASK-WF-designSpec-20261107-075614","short":"DS","base_tree":"69f360d58d89456f559ad3de21ea75027cd72bb0","gt_role":"defect"},{"id":"TASK-WF-makeTheAliasOnly-20261105-051649","short":"AL","base_tree":"fdb08e60c8c3f45bcd1681cd1c79c40da4247b65","gt_role":"defect"},{"id":"TASK-WF-design-20261108-041415","short":"DE","base_tree":"c1a436aed894a854f1081211796117d03bda700a","gt_role":"control"}]`. Run order is this order. |
| `frozen/panels.json` | Reviewer ids, models and roles per panel (section 3) | `{"EL2":{"flagger":{"rid":"t2b-1","model":"muse-ember-1.0"},"adjudicators":[{"rid":"t4-1","model":"gpt-6-luna"},{"rid":"t3-1","model":"gpt-6-luna"}],"cp_role":"adjudicator","planning":{"B":116,"turn":6.4,"rep":6.4}},"SL2":{"flagger":{"rid":"t1b-1","model":"claude-sonnet-5-5"},...,"cp_role":"flagger","planning":{"B":273.7,"turn":14,"rep":14}},"HL2":{"flagger":{"rid":"t2-1","model":"claude-haiku-5-5"},...,"cp_role":"flagger","planning":{"B":238,"turn":23,"rep":23}}}`. Adjudicator order fixes luna index 0 (`t4-1`) and 1 (`t3-1`) for the deal. Also holds `"allowed_models":["muse-ember-1.0","gpt-6-luna","claude-haiku-5-5","claude-sonnet-5-5","grok-4.7"]` and the `TIER`/`ALIAS` maps copied from `EVAL/analysis/merge-b11.sh:11-12` (they already cover `t1b-1`, `t2-1`, `t2b-1`, `t3-1` and `t4-1`). |
| `frozen/brief-a1.txt` | The isolated reviewer brief: `RR:13-17` verbatim plus the H1 sentence | Placeholders `{CAND}`, `{SHA}`, `{SRC}`. The only change to `RR`'s text is one sentence inserted after "review 1 of 3.": `Read both the candidate and its source document {SRC} in full before you review.` The "First-review rules" paragraph (the grading text) stays byte-identical to `RR:17`. ~5 lines. |
| `frozen/brief-flagger.txt` | Text appended to the flagger's brief when collaboration is on | Placeholders `{HELPER}`, `{CAP}`, `{MOVES}`. Text in section 2.4. ~10 lines. |
| `frozen/brief-adjudicator.txt` | Text appended to each luna's brief when collaboration is on | No placeholders. Text in section 2.4. ~5 lines. |
| `frozen/moves.json` | The move catalogue M1-M10, text verbatim from `REQ` 2.0 "Move (text sent to a reviewer)" column | `{"M1":"For each file the plan edits, ...", ..., "M10":"..."}`. Only M3, M4, M5, M6 and M9 are legal on a card. |
| `frozen/templates.json` | Every harness-authored string a reviewer can see | Keys `challenge`, `finding`, `finish`, `reask` (texts in section 2.5). |
| `frozen/pins.sha256` | Pins checked by the launcher before any work (R-02, R-07, R-30) | `sha256sum` format over: every `frozen/*` file except itself; `lib/values.py`, `lib/results.py` and `lib/arm_summary.py` (the analysis scripts R-30 requires committed before the first arm); `REQ` (which holds the decision rule); `EVAL/tools/tmp-scripts/judge-one.sh`; `REPO/src/superclaude/cli/review/findings.py` and `ledger.py`. Written once by hand with `sha256sum`; never regenerated during an arm. |

### 1.2 Executables

| Path | Purpose | Interface (all paths absolute; no environment variable is read except where stated) |
|---|---|---|
| `bin/build-sandbox.sh` | H3 and H4: one sandbox per package, plus the candidate and source copies (H1) | `build-sandbox.sh [--rebuild]`. Reads `R4_SBR` and `R4_OUT` (defaults `SBR` and `R4`), as the launcher does, so tests can redirect both the sandboxes and `manifest.json`. Per package: extract `git -C REPO archive <base_tree>` into `SBR/sb/<pkg>/repo`; delete `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research`, `.dev/reflect` inside it; `git init -q`, `git add -A -f`, `git -c user.name=r4 -c user.email=r4@local commit -qm snap`; copy `EVAL/<pkg>/candidate.md` and `REPO/.dev/tasks/done/<pkg>/source.md` to `SBR/cand/<pkg>/`; write `SBR/cand/<pkg>/candidate.flat` (the candidate with every whitespace run replaced by one space, one line). Writes `R4/manifest.json` (per package: base tree, file count, removed leak dirs, candidate sha256, source sha256, sandbox HEAD, and for comparison the parent of the first commit touching `.dev/tasks/*/<pkg>` with a flag saying whether its tree equals the base tree; deviation D-3). Idempotent: skips a package whose `SBR/sb/<pkg>/built.json` names the same tree, unless `--rebuild`. Exits non-zero if a leak directory still exists or the candidate copy's sha256 differs from `EVAL/<pkg>/candidate.md`. ~45 lines. |
| `bin/run-panel.sh` | The one launch script (section 5) | `PANEL_COLLAB=0|1 NOFALLBACK=1 run-panel.sh --panel EL2|SL2|HL2 --row <row-id> --values <values file> [--packages "<ids>"] [--seed <int>] [--block <id>] [--no-judge]`. Reads `PANEL_COLLAB` (default `1`) and `NOFALLBACK`, plus `R4_SBR` and `R4_OUT` (defaults `SBR` and `R4`) so tests can redirect output. Writes `runs/<row>/...` and `results/<row>.json`. ~150 lines. |
| `bin/reviewer.sh` | One reviewer: the copy of `RR` with H1-H4, the hang guard, the retry rule, the H2 re-ask and the collaboration settings | `reviewer.sh <pkgdir> <rid> <model> <role> <collab 0|1>`, where `<pkgdir>` is `runs/<row>/<pkg>` and holds `panel.json` (written by the launcher: `t0_ms`, `finish_ms`, `hang_ms`, `k`, `sandbox`, `cand`, `src`, `cand_sha`, `settings` per rid, `helper` for the flagger). Writes `<pkgdir>/reviews/<rid>.*` (section 2.6). Exit 0 always; outcome is in `<rid>.meta.json`. ~90 lines. |
| `bin/r4-hook` | The PostToolUse hook for every reviewer in a collaboration run | Called by Claude Code with the hook JSON on stdin. Arguments, baked into the settings JSON: `--board <dir> --rid <rid> --role flagger|adjudicator --flagger <rid> --t0-ms <int> --finish-ms <int> --k <int> --deliver 0|1 --c 0|1`. Prints either nothing or one `hookSpecificOutput` JSON object; always exits 0 (R-22). Behaviour in section 2.3. ~70 lines. |
| `bin/panel-post` | The card writer (the `panel-post` helper of `REQ` 2.0) | Baked arguments (by the wrapper `SBR/board/<row>/<pkg>/bin/card`): `--board <dir> --rid <rid> --run <row>/<pkg> --cand-flat <file> --cap <2k> --t0-ms <int> --finish-ms <int> --r 0|1 --peers <ridA>,<ridB>`. Model arguments: `--anchor <text> --move <M3|M4|M5|M6|M9> --category <enum> --severity <enum>`. Prints `card c<i> posted` and exits 0, or prints `refused: <reason>` on stderr and exits 1. Behaviour in section 2.2. ~60 lines. |
| `bin/anon.sh` | Anonymiser for judging (R-29) | `anon.sh <merged-1.md> <merged-anon.md>`. Rules in section 5.1, step 4. ~25 lines. |
| `bin/judge.sh` | Runs the unchanged judge on one anonymised report | `judge.sh <pkgdir> <merged-anon.md>`. Section 5.1, step 5. ~40 lines. |

### 1.3 Python modules (`lib/`)

| Path | Purpose | Interface |
|---|---|---|
| `lib/card.jq` | The only card schema check, shared by writer and reader | `jq -c --arg flagger <rid> -f lib/card.jq` on one line; emits the line if valid, nothing otherwise. Rules in section 2.1. ~15 lines. |
| `lib/normalize.py` | H2: truncate, then parse with the real parser | `normalize.py <raw.md> <final.md> <parse.json>`. Section 2.6. Functions `truncate_block(text) -> (text, n_truncated)`, `check(text) -> dict` (wraps `findings.parse_block`). ~45 lines. |
| `lib/values.py` | The timing formulas and the Spike 4 values builder | `k_of(B, turn, rep, hooks=2.0) -> int`; `finish_offset(B, turn, rep) -> float` (= 1.35 B - turn - rep); `hang_s(B)` (= 1.5 B); all three compute in integer milliseconds (2.7). CLIs: `values.py planning --panel <P>`, `values.py build --panel <P> --runs <A1 row dirs...>`, `values.py srun --panel <P>`, `values.py slowdown --panel <P> --a1 <dirs> --srun <dirs>`; each writes its file of 1.4 and the `.sha256` beside it. Section 2.7. ~90 lines. |
| `lib/collab.py` | Per-package metrics after the reviewers exit: deal check, card Task, delivery, conversion, peer tags, alarms inputs, `collab.json` | `collab.py <pkgdir>`. Functions `overlap12(a, b) -> bool`, `task_of(cand, anchor) -> str|None`, `form_of(i, c) -> "challenge"|"finding"`, `recipient_of(i, r, peers) -> rid`, `own_line_jaccard(task_sets) -> float`. Section 2.8. ~140 lines. |
| `lib/audit.py` | Read-only audit (R-09, section 5.5 of `REQ`) and the contamination checks | `audit.py <rowdir>`; writes `<rowdir>/audit.json`. Section 5.1, step 3. ~80 lines. |
| `lib/results.py` | The results row | `results.py <rowdir> --out results/<row>.json`. Section 5.2. ~70 lines. |
| `lib/arm_summary.py` | Arm-level alarms, stop rules, SLO budget and the form contrast (R-24, R-25, R-36, R-37) | `arm_summary.py --panel <P> --a1 <results files...> --arm <results files...> --out results/<P>-<arm>-summary.json`. Section 2.9. ~90 lines. |

### 1.4 Values, spikes and tests

| Path | Purpose | Interface |
|---|---|---|
| `values/planning-<P>.json` (+ `.sha256`) | Planning values per panel, in the same per-package shape as `values/<P>.json`, used only before Spike 4 has finished (the Spike 4 rows and the first smoke need a hang guard before B_A1 exists) | Written by `values.py planning --panel <P>` from `panels.json` planning numbers (same B for every package); every package carries `"planning": true`. |
| `values/<P>.json` (+ `.sha256`) | Spike 4 output per panel. Per package: `B_A1`, `turn_p90`, `T_report_p90`, `finish_offset_s`, `hang_s`, `k`, `deliver: true`, `cp_role`, `n_runs`, `source_rows` | Written once by `values.py build`, pinned at once, never changed. The launcher refuses any values file whose sha256 differs from its `.sha256` file. |
| `values/<P>-srun.json` (+ `.sha256`) | Spike 4 slowdown runs: `values/<P>.json` with `deliver: false` on every package (briefs, helper and hooks on, no card delivered) | Written by `values.py srun --panel <P>`. Used only for the slowdown measurement s (R-45). |
| `values/<P>-slowdown.json` (+ `.sha256`) | Per package `s`, the section 3 limit for the package's k, and `budget_fail` (open question 4) | Written once by `values.py slowdown`; pinned before the first F7 row. Order: `build`, `srun`, srun rows, `slowdown`. |
| `spikes/s0-req-s3.sh` | Spikes S0 and REQ-S3 for one model | `s0-req-s3.sh <model>`; section 6.3. ~40 lines. |
| `spikes/probe-hook` | Spike-only hook: logs every hook input, injects `run ls /tmp/panel-probe` after tool call 3 and the frozen finish text after call 6 | Same output contract as `r4-hook`. ~25 lines. |
| `spikes/s2-resume.sh` | Spike S2 (the part F7 needs: `--resume` for the H2 re-ask) | `s2-resume.sh <model>`. ~25 lines. |
| `tests/fake-claude` | **Test scaffolding only.** A stand-in `claude` put first on `PATH` by the tests | Reads its arguments; for reviewer runs, replays a fixture script (sleep, then for each simulated tool call write a transcript line and run the hook commands found in `--settings` with a hook JSON on stdin, run any `panel-post` command the fixture lists), then prints a fixture JSON result array; for `--resume`, prints a fixture stream; for `--model claude-opus-5-5`, writes a fixture `score.json` into the `D` directory named in the brief. Behaviour per test is chosen by a fixture file named in `FAKE_CLAUDE_SCRIPT`. ~80 lines. Never used outside `tests/`. |
| `tests/conftest.py`, `tests/fixtures/`, `tests/test_*.py` | The test plan of section 6 | Run with `uv run pytest R4/tests` from `REPO`. No custom markers (the repo runs `--strict-markers`). |

### 1.5 Run-time layout (created by the scripts, never by hand)

```text
SBR/                                    /tmp/evalsb-collab-r4
  sb/<pkg>/repo/                        sandbox, cwd of every reviewer (H3, H4)
  sb/<pkg>/built.json                   tree sha, file count
  cand/<pkg>/{candidate.md,source.md,candidate.flat}
  board/<row>/<pkg>/                    one board per row and package (REQ 2.0)
    msgs/<flagger rid>.jsonl            accepted cards, one panel-msg/1 line each
    state/<rid>.calls                   tool-call counter (written by r4-hook)
    state/<rid>.delivered               delivered card ids with times
    state/<rid>.finished                finish signal sent (time)
    state/<rid>.nosnap                  snapshot failed: deliver nothing to <rid>
    snap/<rid>.jsonl, snap/<rid>.sha256 hook-side transcript snapshot (seal)
    metrics/<rid>.jsonl                 hook and helper events (hook_ms, hook_error, post_rejected, delivery, ...)
    settings/<rid>.json                 the per-reviewer --settings file
    bin/card                            the flagger's helper wrapper
  launch.lock                           flock taken around the concurrency check and reviewer start
/tmp/jdg.XXXXXXXX/<pkg>/<label>/        judge staging, outside SBR, deleted after copy-back (section 5.1, step 5)
R4/runs/refusals.jsonl                  one line per refused launch (the refused row directory is never touched)
R4/runs/schedule.jsonl                  one line per row: row, panel, arm, block, start, end (R-28)
R4/runs/<row>/
  run.json                              panel, PANEL_COLLAB, seed, values sha256, pins check, start/end
  <pkg>/panel.json                      timing and paths for this package (T0, deadlines, k, deal coins)
  <pkg>/reviews/<rid>.*                 reviewer outputs (section 2.6)
  <pkg>/board/                          copy of SBR/board/<row>/<pkg>/ after the package (R-26; the /tmp original is kept)
  <pkg>/tags/<rid>.json                 own/peer tags (deviation D-1)
  <pkg>/slots.json, <pkg>/collab.json   per-card log and package metrics (R-23, R-36)
  <pkg>/resolution.json, ledger.json, merged-1.md, merge-stdout.txt
  <pkg>/scoring/{merged-anon.md,label-key.json,score.json,judge.json,judge.err}
  audit.json
R4/results/<row>.json                   the results row
```

## 2. Behaviour

The mechanism is `REQ` Redesign 4 (a)-(h) and R-34..R-37, run **one way**: the flagger posts cards, the two lunas receive and settle them, nobody else sends anything, and no one is held at Stop.

### 2.1 Card message (`panel-msg/1`, `kind:"card"`)

One JSON object per line in `SBR/board/<row>/<pkg>/msgs/<flagger rid>.jsonl`. A card line has **exactly** these keys:

```json
{"v":"panel-msg/1","id":"c0","run":"<row>/<pkg>","from":"t2b-1","to":"t4-1","t":1763063000123,
 "kind":"card","move":"M3","anchor":"<12-200 characters, whitespace-flattened, a substring of the flattened candidate>",
 "category":"unpassable-check","severity":"MAJOR"}
```

`lib/card.jq` accepts a line only if all of these hold (R-06, R-08, the F7 exception of `REQ` 2.0):

| Rule | Rejects |
|---|---|
| The line is a JSON object whose key set equals the eleven keys above | `claim`, `verdict`, `blocking`, `note`, `items`, `n` or any other key; a missing key |
| `v == "panel-msg/1"`, `kind == "card"`, `id` matches `^c[0-9]+$`, `t` is a number, `from == $flagger` | a card from a luna or any other writer |
| `move` is one of `M3 M4 M5 M6 M9` (the reading moves) | search moves M1, M2, M7, M8, M10 and anything else |
| `category` is one of `contradiction unpassable-check data-loss safety missing-requirement other`; `severity` is one of `CRITICAL MAJOR MINOR` (the findings-v1 enums, `findings.py:14-22`) | any other value |
| `anchor` is a string of 12-200 characters | short or long anchors |
| The serialised line is at most 600 bytes (checked by the caller with `wc -c` before the filter) | long lines |

The substring check against the candidate is done only by the writer, because the reader has no reason to re-read the candidate on every tool call; a line that did not come through the writer has no `post_accepted` event, so the reader never delivers it (2.3 step 7) and the audit counts it (section 5.1, step 3).

### 2.2 Writer: `panel-post` (the flagger's only way to post)

Checks run in this order; the first failure prints `refused: <reason>` on stderr, appends `{"ev":"post_rejected","reason":...,"t":...}` to `metrics/<rid>.jsonl` and exits 1:

1. `after_finish`: now (ms) is at or after `--finish-ms` (helpers refuse to post after PANEL_FINISH_AT, R-41).
2. `too_early`: `state/<rid>.calls` is below 2, so this Bash call is not yet the flagger's 3rd tool call (R-34).
3. `bad_args`: a model argument is missing or repeated.
4. `bad_move`, `bad_category`, `bad_severity`: value outside its enum.
5. `bad_anchor_length`: the flattened anchor (`tr -s '[:space:]' ' '`, trimmed) is not 12-200 characters.
6. `anchor_not_in_candidate`: the flattened anchor is not a fixed-string substring of `candidate.flat` (`grep -qF -- "$anchor"`; the `--` matters because criteria often start with `- `).
7. Under `flock` on `msgs/<rid>.jsonl.lock`: count the existing lines `n`; `over_cap` if `n >= cap` (cap = 2k).
8. Build the line with `id = "c<n>"`, `to = peers[(n + r) mod 2]` (the deal of R-35), `t` = now, then pass it through the 600-byte check and `lib/card.jq`; `invalid` if either rejects it; otherwise append it with one `printf '%s\n' >>` while the lock is held, log `{"ev":"post_accepted","id":"c<n>","sha256":<sha256 of the line's bytes without the trailing newline>}` and print `card c<n> posted`. The reader and the audit hash each board line the same way (line content, no newline).

The writer is the only code that assigns `id` and `to`, so the append index i is the card's board index by construction.

### 2.3 Reader: `r4-hook` (every reviewer, every tool call)

The hook does nothing that can fail the review. A `trap` on `ERR` and `EXIT` makes every error path print nothing, append `{"ev":"hook_error","msg":...}` to `metrics/<rid>.jsonl`, and exit 0 (R-22). Each call:

1. Read stdin into a variable (`transcript_path` and `agent_id` are the only fields used). Record the start time.
2. If the input has a non-empty `agent_id`, the tool call ran inside a subagent (the `/sc:spec-panel` skill can start one): increment `state/<rid>.subcalls`, log `{"ev":"subagent_call"}`, print nothing and stop. Cards and the finish signal go only to the reviewer's main thread, and the main-thread counter is not inflated by subagent calls. (Whether subagent calls fire the session's hooks, and carry `agent_id`, is an S0 check.)
3. Increment `state/<rid>.calls` under `flock`; the new value is `calls`.
4. **Finish signal (all roles).** If now >= `--finish-ms` and `state/<rid>.finished` does not exist: write the time into it, log `{"ev":"finish_signal"}`, print the `finish` template as `additionalContext`, and stop. After this point nothing is ever delivered to this reviewer (R-41).
5. **Flagger:** stop here (the flagger receives nothing; its hook exists for the call counter and the finish signal).
6. **Adjudicator delivery** happens only if all hold: `--deliver 1`; `calls >= 6` (after the 6th tool call); `state/<rid>.nosnap` absent; the number of lines in `state/<rid>.delivered` is below `--k`; now < `--finish-ms`.
7. Select the first card in `msgs/<flagger>.jsonl` (append order) that passes the 600-byte check and `lib/card.jq`, whose sha256 appears in a `post_accepted` event of `metrics/<flagger>.jsonl` (so a line written to the board by anything other than `panel-post`, even with the right `from`, is never delivered), has `to == rid`, and is not in `state/<rid>.delivered`. None: stop.
8. **Seal before the first delivery.** If `snap/<rid>.sha256` does not exist: copy `transcript_path` to `snap/<rid>.jsonl` and write its `sha256sum` to `snap/<rid>.sha256`. If the copy or the hash fails, or `transcript_path` is empty or unreadable: create `state/<rid>.nosnap`, log `{"ev":"snapshot_missing"}`, print nothing, stop. The seal fails closed and the review fails open (`REQ` 2.0).
9. Render the card: index i from its id, form `challenge` when `(i + floor(i/2) + c)` is even, else `finding` (R-35); fill the template from `frozen/templates.json`. If the rendered text exceeds 1,500 characters, log `hook_error` and deliver nothing (cannot happen with the frozen templates: anchor at most 200 plus template and move text under 600).
10. Append `<card id> <now ms> <form>` to `state/<rid>.delivered`, log `{"ev":"delivery","card":...,"form":...}`, and print `{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"<rendered>"}}`.
11. Log `{"ev":"hook_ms","ms":...}` on every path (for `hook_ms_p95`).

At most one card is delivered per tool call, so a luna gets its k cards over k different tool calls. No Stop hook is registered, so `stop_blocks` is always 0.

### 2.4 Brief text added when collaboration is on

The base brief is `frozen/brief-a1.txt` for every reviewer in every arm. With `PANEL_COLLAB=1` and k >= 1 for the package, the launcher appends one paragraph block.

`frozen/brief-flagger.txt` (`{HELPER}` = absolute path of `SBR/board/<row>/<pkg>/bin/card`; `{CAP}` = 2k; `{MOVES}` = the five reading moves from `frozen/moves.json`, one per line as `M3: <text>`):

```text
Panel cards. Two other reviewers are reviewing this candidate at the same time. Your extra job is to flag sentences for them, not to settle them. From your 3rd tool call on, each time you read one of these in the candidate, post a card for it: an acceptance criterion or other sentence that says every, all, only or complete; a command or grep criterion; a mapping table or decision rule.
Post a card with one Bash command:
{HELPER} --anchor '<12-200 characters copied exactly from the candidate>' --move <M3|M4|M5|M6|M9> --category <contradiction|unpassable-check|data-loss|safety|missing-requirement|other> --severity <CRITICAL|MAJOR|MINOR>
Pick the move whose check would settle the sentence:
{MOVES}
Give the category and severity you would give it as a finding. If the sentence contains a single quote, copy a part of it that has none. You can post at most {CAP} cards; the command refuses more. A card has no field for what you think is wrong. Cards do not replace your own review: write your report and findings block exactly as you would without them.
```

`frozen/brief-adjudicator.txt` (kept short because luna sets the critical path on EL2, where the brief slowdown limit is 5.7%, `REQ` timing rule 5c):

```text
Panel cards. Another reviewer may flag candidate sentences for you while you work. A card appears after a tool result and starts with "[panel card". Settle every card you receive: run a finite check on that sentence yourself. If the check shows a defect, report it in your findings block with that sentence, or a part of it, as the anchor. Write that finding as your own check result and do not mention the card or a peer in it. If it passes, write one line in your coverage statement: "card <id>: passed" and the check you ran. Cite a fact or count only if you ran the check yourself. Grade a card's defect with the same grading check as any other finding.
```

Each luna's paragraph is the same whatever form its cards take, so the form contrast (2.5) is carried only by the card text.

### 2.5 Harness-authored texts (`frozen/templates.json`)

| Key | Text (placeholders in braces) | When |
|---|---|---|
| `challenge` | `[panel card {id}] Candidate sentence: "{anchor}" Required finite check: {move_text}` | form = challenge (anchor plus the required finite check) |
| `finding` | `[panel card {id}] A peer reviewer flagged this candidate sentence as category {category}, severity {severity}: "{anchor}"` | form = finding (anchor plus the flagger's enums, never a claim) |
| `finish` | `[panel] finish now with what you have` | first hook call at or after PANEL_FINISH_AT, once per reviewer |
| `reask` | `Your findings block has lines the merge parser rejects:` + newline + `{errors}` (one `line <n>: <msg>` per error, parser messages verbatim) + newline + `Reply with the complete report again, changed only so that every listed line passes: anchor and anchor2 12-200 characters copied exactly from the candidate, at most 8 refs, an id of at most 16 characters (letters, digits, dot, underscore, hyphen), severity CRITICAL, MAJOR or MINOR, a MINOR finding never blocking, category one of contradiction, unpassable-check, data-loss, safety, missing-requirement, other.` | the H2 re-ask (2.6) |

`{move_text}` is the card move's text from `frozen/moves.json`. No template contains a package name, Task number, file path or ground-truth text; the audit (section 5.1, step 3) proves it on every run.

### 2.6 Reviewer lifecycle (`bin/reviewer.sh`)

1. Read `panel.json`. Build the brief: `brief-a1.txt` with `{CAND}` = `SBR/cand/<pkg>/candidate.md`, `{SHA}` = its sha256, `{SRC}` = `SBR/cand/<pkg>/source.md` (H1); plus the role paragraph when `collab=1` and k >= 1.
2. **Attempt loop (`RR:61-64`, at most 2 attempts).** Before each attempt, `TMO = floor((hang_ms - now_ms) / 1000)`; if `TMO < 1`, skip the attempt and set `hang_kill: true`. Command (cwd `SBR/sb/<pkg>/repo`):

   ```bash
   timeout --kill-after=5 "$TMO" claude -p --model "$MODEL" --output-format json --session-id "$SID" --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit $SETTINGS <<<"$BRIEF"
   ```

   `$SID` is a fresh `uuidgen` value per attempt (step 4).

   `$SETTINGS` is `--settings <SBR/board/<row>/<pkg>/settings/<rid>.json>` on attempt 1 of a collaboration run and empty otherwise. **Attempt 2 always runs isolated**: no settings and the A1 brief, and the meta records `retry_isolated: true` when `collab=1` (R-44), so hooks never deliver twice. Exit code 124 or 137 from `timeout` sets `hang_kill: true` (R-43).
3. Per attempt, exactly as `RR:50-58`: extract the result text to `<rid>.attempt<n>.md`, the observed model, `output_tokens_main` and `output_tokens_all`, `API Error`, `model_ok` (observed equals expected or expected plus `-build`), `findings_block`; plus `session_id` (the `--session-id` value passed), `t_start_ms`, `t_end_ms`, `timeout_s`, `settings` (true or false). Success is `model_ok && findings_block && !api_error` (`RR:59`). There is no fallback ladder. A reviewer that fails both attempts is recorded `final_ok: false`; it still gets a `<rid>.final.md` (step 5), so the merge reads it as an invalid block and keeps the other reviewers (`ledger.py:127-157`). The meta also records `model_mismatch`: true only when the observed model is non-empty and differs from the expected one (a misroute), as opposed to an empty run (killed, API error, no output).
4. After every attempt, including one killed by the hang guard, copy the session transcript to `<rid>.attempt<n>.transcript.jsonl` and the last attempt's to `<rid>.transcript.jsonl` (`find ~/.claude/projects -name "<session id>.jsonl"`). The session id is known before launch: each attempt passes `--session-id <uuid>` with a fresh `uuidgen` value recorded in the attempt's meta (deviation D-5), so a killed session's transcript is found exactly, never guessed among the other reviewers and rows that share the sandbox's project directory. The launch no longer passes `--no-session-persistence`, so the file exists. It is used for timing (2.7) and the audit, so a killed reviewer is audited too. Copy the last attempt's `.md` to `<rid>.md` (as `RR:85`): `<rid>.md` is the raw final report.
5. **H2.** `<rid>.final.md` is always written. If the last attempt has no findings block, it is a copy of `<rid>.md` (an empty file when the process produced no text), and `parse.json` records `ok: false`; no re-ask follows. Otherwise: `normalize.py <rid>.md <rid>.final.md <rid>.parse.json`. `normalize.py` finds the last findings-v1 block with the parser's own fence rules, and in each JSON line replaces `anchor` and `anchor2` with `flat(x)[:200]` and `claim` with `flat(x)[:300]` when longer (a prefix of a flattened exact quote is still a substring of the flattened candidate), rewrites only changed lines, then calls `findings.parse_block` on the result and writes `{ok, errors, truncated}`.
6. **Re-ask once** if `errors` is non-empty, `session_id` is known and `hang_ms - now >= 1 s`. `TMO` is recomputed immediately before the re-ask as `floor((hang_ms - now_ms) / 1000)`, so the re-ask also dies at T0 + 1.5 B_A1 (R-43), and the cwd is the same sandbox `SBR/sb/<pkg>/repo`, because `--resume` finds the session under the cwd's project directory:

   ```bash
   timeout --kill-after=5 "$TMO" claude -p --resume "$SID" --model "$MODEL" --output-format stream-json --verbose --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <<<"$REASK" > <rid>.reask.jsonl
   ```

   No settings are passed, so nothing is delivered during a re-ask. Take the last `result` event's text as `<rid>.reask.md`, check its observed model (`reask_model_ok`), normalise it to `<rid>.final.md` if it has a block and the model is right; otherwise keep the first normalised report. Log `reask_s` (wall seconds) in every arm, A1 included (R-02).
7. Write `<rid>.meta.json`: `reviewer_id`, `role`, `expected_model`, `observed_model`, `model_ok`, `model_mismatch`, `findings_block`, `final_ok`, `source_md_opened` (a tool call in the transcript names `SBR/cand/<pkg>/source.md`; the R-01 verification), `attempts`, `retry_s` (wall of attempt 2), `retry_isolated`, `hang_kill`, `reask`, `reask_s`, `reask_model_ok`, `truncated`, `dropped_lines` (errors left in the final parse), `t_start_ms` (first attempt), `t_end_ms` (last process end, re-ask included), `wall_s`, `output_tokens_all` (attempts plus re-ask). Write `<rid>.cost.json` in `RR:87`'s shape (`attempts`, `total_wall_s`, `total_output_tokens_all`), re-ask included.

The merge input is `<rid>.final.md`.

### 2.7 Timing (values file, k, deadlines)

All formulas are `REQ` 2.0 timing rules 1-6 and R-41..R-43, computed only in `lib/values.py` and written to the values file; the launcher copies them into `panel.json`, and hooks receive them as baked arguments (R-21).

| Quantity | Formula | Written as |
|---|---|---|
| B_A1 | median per-package `elapsed_s` of the panel's `PANEL_COLLAB=0` rows used for Spike 4 | `B_A1` |
| turn_p90, T_report_p90 | 90th percentiles (nearest rank: the value at position `ceil(0.9 n)` of the sorted list) over the critical-path role's turns in those rows (role per panel in section 3). A turn is one assistant message: the transcript writes one entry per content block, so consecutive entries with the same `message.id` are grouped (main thread only, `isSidechain` false) in `<rid>.transcript.jsonl`; a group ends at the first entry that is not part of that assistant message (a tool result or user entry), and S0 records whether any tool result ever appears between two entries of one message. A turn's duration is the **last** entry's `timestamp` in the group minus the `timestamp` of the last entry before the group, so the time spent writing every block (the long report text included) is counted. T_report is the last turn's duration in each transcript. | `turn_p90`, `T_report_p90` |
| k | `max(0, min(2, floor((0.35 B_A1 - 2 - turn_p90 - T_report_p90) / (2 turn_p90))))`, computed in integer milliseconds (every input rounded to ms first, `0.35 B` as `B_ms * 35 // 100`), so the thresholds of section 3 hold exactly: SL2 gives k = 1 at T_report_p90 = 51.795 s and k = 0 at 51.8 s | `k` |
| PANEL_FINISH_AT | `T0 + 1.35 B_A1 - turn_p90 - T_report_p90` | `finish_offset_s` |
| Hang guard | `T0 + 1.5 B_A1` | `hang_s` |
| Card cap | `2k` | derived |

T0 is the launcher's clock (ms) immediately before it starts the three reviewers of one package. B_f in `REQ` is this frozen B_A1. A package with k = 0 runs fully isolated even when `PANEL_COLLAB=1` (no settings, no paragraphs) and is logged `k0_isolated: true`, which is how `REQ`'s "counts as isolated" is made exact.

**Schedule (`REQ` Redesign 4 (b)).**

| Item | Value |
|---|---|
| Flagger posting | from its 3rd tool call, at most 2k cards per package; refusals logged `too_early`, `over_cap`, `after_finish` |
| Luna posting | none: lunas get no helper and the reader drops any card whose `from` is not the flagger |
| Delivery | PostToolUse, from the luna's 6th tool call, after its snapshot is written and hashed; one card per tool call; at most k per luna |
| Messages per reviewer | flagger at most 2k sent, 0 received; each luna at most k received, 0 sent |
| Size caps | 600 bytes per card line; 1,500 characters per hook output |
| Deadline guard | nothing delivered and nothing posted at or after PANEL_FINISH_AT; no Stop hold; a dealt card not delivered by the luna's end is `late` |
| Hang guard | every reviewer process, every arm: killed at T0 + 1.5 B_A1, `hang_kill`, the package is `SLO_BREACH` |

### 2.8 Per-package metrics (`lib/collab.py`, after all three reviewers exit)

`collab.py` reads `panel.json`, the board copy, the reviews and (after the merge) `ledger.json`, and writes `tags/<rid>.json`, `slots.json` and `collab.json`. Definitions:

- `overlap12(a, b)`: true when the flattened strings share a common substring of at least 12 characters (`difflib.SequenceMatcher(None, a, b, autojunk=False).find_longest_match(...)`). The only overlap test in the design.
- `task_of(cand, anchor)`: `findings.locate` gives the anchor's first line; the Task is the last heading above it matching `^## Task (\d+):` (all three candidates use this form), returned as `"T<n>"`, else `None`.
- **Slot** (one per accepted card, R-36, field names as R-23): `id`, `i`, `recipient` (`to`), `card_form` (recomputed from i and c and checked against the hook's logged form; a mismatch is a `hook_error`), `deal_r`, `deal_c`, `slot_type` (`null`; an F1 field), `card_task`, `t_posted`, `t_delivered` or null, `status` (`delivered`, `late`, `no_snapshot`, `held` when `deliver` is 0), `converted`, `converted_fids`, `passed_line` (the receiver's report contains `card <id>: passed`). Judge-credited and uncredited conversion are filled by `results.py` (section 5.2) because they need ground truth.
- **Conversion**: a delivered card is converted when a line of the receiver's final findings block has `anchor` or `anchor2` with `overlap12` against the card anchor.
- **Peer tag (R-10, sidecar D-1)**: a luna's line is `peer` when its `anchor` or `anchor2` has `overlap12` with any card delivered to that luna; every other line, and every flagger line, is `own`.
- `late`: a card dealt to a luna that was never delivered although nothing else blocked it (the luna had no `nosnap`, `deliver` was 1 and the luna had received fewer than k cards): the luna made no tool call after the card became deliverable, so its last tool call came first (`REQ` (b), deadline guard).
- `own_line_jaccard`: mean pairwise Jaccard of the three reviewers' Task sets built from `own` lines only (pairs where both sets are empty are skipped; null if all are skipped). `pairwise_task_jaccard`: the same over all lines (descriptive only).
- `flag_finding_overlap`: share of the flagger's accepted cards whose flattened anchor equals the flattened `anchor` or `anchor2` of a line in the flagger's own final block (null with no cards).
- `adjudication_agreement`: converted cards / delivered cards (null with no delivery).
- `finish_would_fire`: a reviewer of the critical-path role (EL2: a luna, as R-41 states; SL2 and HL2: the flagger) has `t_end_ms` later than `finish_ms` (logged in every arm; `PANEL_COLLAB=0` never acts on it).

`collab.json` carries every R-23 field. Fields of other designs are present with value `null` (`resume_fallback`, `phase2_s`, `phase2_timeout`, `p2_lines_salvaged`, `n_planned`, `n_launched`, `slot_type`, `echo_rate`), so the same schema check applies to every arm. Per reviewer: `msgs_sent`, `msgs_received`, `first_delivery_t`, `seal_t` (snapshot time), `seal_sha256`, `seal_sha_ok` (the harness re-hashes the snapshot and compares), `stop_blocks` (0), `hook_calls`, `hook_error`, `hook_ms_p95`, `reask_s`, `attempts`, `retry_s`, `retry_isolated`, `hang_kill`, `snapshot_missing`, `late`, `over_cap`, `too_early`, `after_finish`, `finish_signal_t`. Panel: `arm` (`F7` or `A1`), `panel`, `k`, `k0_isolated`, `deal_r`, `deal_c`, `panel_finish_at`, `finish_would_fire`, `elapsed_s`, `baseline_elapsed_s` (B_A1), `overhead_pct`, `own_line_jaccard`, `pairwise_task_jaccard`, `ledger_rows`, `cards_sent`, `cards_delivered`, `flag_finding_overlap`, `adjudication_agreement`, `slo_breach`, `values_sha256`, and `slots` (the R-36 list).

### 2.9 Arm-level rules (`lib/arm_summary.py`)

Inputs are results rows (section 5.2) for one panel: the `PANEL_COLLAB=0` rows (A1) and the `PANEL_COLLAB=1` rows (the F7 arm). A **run** is one row (one panel on all three packages). Outputs, each with the evidence numbers:

| Check | Rule | Source |
|---|---|---|
| `STOP:no_cards` | `cards_sent = 0` in more than 50% of the arm's runs | R-37, (h) |
| `STOP:flag_finding_overlap` | pooled flag_finding_overlap above 0.5 | R-37, (e) |
| `CONVERGENCE` per run | the run's mean `own_line_jaccard` exceeds the A1 mean + 0.15, or its total `ledger_rows` is more than 20% below the A1 mean; the arm passes the independence guard if it fires in at most 2 runs (of 12) | R-25 |
| `SNAPSHOT` | `snapshot_missing` for more than 50% of the arm's receiving lunas (lunas dealt at least one card) | R-25 |
| `independence` | CONVERGENCE in at most 2 runs and zero audit violations: every row `audit_ok: true` and `harness_text_gt_overlap = 0` | `REQ` 4, rule 5 |
| `AGREEMENT` | pooled adjudication agreement above 0.90 or below 0.05 | (e) |
| `SLO budget` | share of package-runs with `elapsed_s > 1.35 B_c(pkg)` (B_c = the median of the A1 rows run alongside, the after-the-fact reference of R-24) above 1/12 stops the arm; any `hang_kill` is an `SLO_BREACH` | R-24 |
| `time verdict` | per package, median `elapsed_s` at most 1.35 B_c, and no package-run above 1.5 B_A1 (the hang guard); `baseline_drift = B_c / B_f` per randomised block (blocks read from `runs/schedule.jsonl`), and a block outside [0.963, 1.10] is reported but left out of the time verdict | R-24, R-45 |
| `no loss` | mean found /14 at least A1 - 0.25; mean wrong blockers at most A1 + 1.0; mean control wrong blockers at most A1 + 0.5 | `REQ` 4, rule 3 |
| `reach` | a run reaches if it has a credit on designSpec GT1, GT2, GT5, GT6, GT9, GT10 (B1, B2, B5, I1, I4, I5), alias GT1, GT3, GT4 (B6, B8, I6) or control GT1 (I7); one-sided Fisher exact p against A1, computed with `math.comb` | `REQ` 4, rule 1 |
| `form contrast` | conversion by form over delivered cards: counts, two-proportion z test (pooled), and the mean run-paired difference (challenge minus finding, runs with both forms delivered) | R-36 |
| `interim futility` (after 6 runs) | hard-issue credits at or below A1's, or median overhead above 35%, or CONVERGENCE in 3 or more of 6 | `REQ` 4 |
| `act rates` | the act rates measured by spike REQ-S3 (`spikes/out/act-rates.json`) listed beside the planning factors they replace (0.6-0.8 for posting, 0.3-0.5 for reaching the defect, `REQ` Redesign 4 (f)) | R-47 |

The decision against the static kit (A2) needs an A2 arm, which this folder does not build (section 7, risk 9).

### 2.10 Contamination safeguards and how each is enforced

| Safeguard (`REQ` (e), R-06..R-10) | Mechanism | Check |
|---|---|---|
| Shared content is an anchor plus a required move, or an anchor plus enum category and severity | writer builds every line from validated arguments; `card.jq` allows only the eleven keys; templates are frozen | validator tests; audit of every board line with `card.jq` |
| No claim or free text from the flagger | the schema has no field for it; the anchor must be a substring of the candidate | `anchor_not_in_candidate` and `invalid` rejections are logged |
| Each luna's first pass is sealed before its first card | hook-side transcript snapshot with sha256, fail closed | `seal_sha_ok`; fault-injection test |
| The flagger receives nothing | its hook has no delivery branch | `msgs_received = 0` for the flagger |
| Adjudicator is a different model family than the flagger | `panels.json`: ember, sonnet or haiku flags; luna adjudicates | launcher refuses a panel whose flagger model is `gpt-6-luna` |
| First-hand rule | adjudicator brief: cite a fact only if you ran the check | audit counts adjudicator findings that cite a count with no matching Bash call in the transcript (`first_hand_suspect`, descriptive) |
| Reviewers never see ground truth | ground truth is read only by `results.py` and `audit.py` after all reviewers and the merge of the row have finished; the judge is the only model given a ground-truth path, and its working files (`judge.json` holds the ground truth it read) live only in a `/tmp/jdg.*` directory outside `SBR` that a `trap ... EXIT` in `judge.sh` deletes on every exit path, success or failure; kept copies are under `R4/runs/`, which reviewers are never pointed at. Reviewers of other rows can run while a row is judged, and they run as the same user, so a determined reviewer could still reach ground truth (`EVAL` has always been readable by absolute path); this is detected, not prevented | audit, three layers. **Content:** a reviewer's tool results (the `tool_result` entries of its transcript) must not contain the ground-truth and judge key markers `"blocking_in_implement"`, `"plan_quote"`, `"gt_covered_any"`, `"wrong_blockers"`, the file-name markers `ground-truth.json`, `ground-truth-draft.json`, `judge.json`, `score.json`, `merged-anon.md` (a recursive `grep`, `find` or `ls` prints the file name of every hit), nor the board marker `"panel-msg/1"`; any hit is a violation. **Paths:** a tool call naming `ground-truth`, `judge.json`, `score.json`, `/tmp/jdg.`, `.claude/projects`, `/.dev/reflect`, the `workspaces` directory that holds `REPO`, `EVAL`, `R4` and every other checkout (`/home/coder/workspaces`, `~/workspaces` or `$HOME/workspaces`), another package's sandbox, or (for a luna) the board directory is a violation. Other paths under the home directory are allowed, because the unchanged brief (`RR:17`) tells every reviewer to read `~/.claude/rules/prompts/document_review_loop_prompts.md` and the skill reads `~/.claude` files; they are listed as `home_other`. **Broad searches:** a recursive search (`grep -r`/`-R`, `rg`, `find`, `ls -R`) rooted at `/`, `/tmp`, `/home`, `~` or `$HOME` is a violation (`broad_search`); reviewers search their own cwd. Any other `/tmp` path outside the reviewer's own sandbox and candidate directory is listed as `tmp_other` (descriptive, since reviewers may use scratch files). These layers detect the routes they name; a read whose output carries no marker and whose command names no listed path (for example a path assembled at run time) can still escape. This is detection, not prevention. The five content markers occur in none of the three sandbox trees (`git grep -F` over each base tree minus the removed leak directories gave 0 files each while this design was written), so a hit cannot come from the sandbox itself |
| Reviewers are read only | `--disallowedTools Edit Write NotebookEdit`; helpers and hooks write only under `SBR/board` | audit: `git status --porcelain` (tracked and untracked changes) empty in each sandbox, and the candidate sha256 unchanged, after the row; files that only `--ignored` shows (caches such as `__pycache__`, `.pytest_cache` from a reviewer's test run) are listed as `ignored_only`, not a violation; rows of other launchers that overlapped in time on the same sandbox are listed from `runs/schedule.jsonl` |
| No leak directory | H4 removal in `build-sandbox.sh` | `manifest.json`; audit re-checks `.dev/reflect` is absent |
| The judge cannot tell the arm | anonymiser strips reviewer ids, paths, board references and card mentions; random label; random staging path | case-insensitive `grep` of `merged-anon.md` for `"origin":`, `panel card`, `\bcards? c[0-9]+\b`, `evalsb-collab`, `/tmp/jdg`, `r4-flag`, `20261113-collab` and the panel's reviewer ids (whole words) returns 0. The key pattern `"origin":` is used instead of `REQ` R-10's bare word `origin`, because the designSpec candidate itself contains "origin" 8 times as a substring (2 as a whole word) and quoted anchors would fail a bare-word check |

## 3. The three panels

`REQ` designs F7 only for EL2 (ember + 2x luna), with ember as the flagger because it is fast (median 41 s, 3.2 s per turn) and therefore off the critical path. The owner tests three panels. This design keeps **the same role mapping on all three**: the one non-luna model is the flagger, the two lunas are the adjudicators. That keeps the treatment identical across panels (same briefs, same deal, same within-luna form contrast) and respects the rule that the adjudicator is a different model family from the flagger.

| Panel | Flagger (posts cards) | Adjudicator A, deal index 0 | Adjudicator B, deal index 1 | Critical-path role (sets B) | Merge resolution ids |
|---|---|---|---|---|---|
| EL2: ember + 2x luna | `t2b-1` = muse-ember-1.0 | `t4-1` = gpt-6-luna | `t3-1` = gpt-6-luna | luna (adjudicator) | as in batch `b4-muse-ember-luna2` |
| SL2: sonnet + 2x luna | `t1b-1` = claude-sonnet-5-5 | `t4-1` = gpt-6-luna | `t3-1` = gpt-6-luna | sonnet (flagger) | as in batch 11 (`merge-b11.sh:6`) |
| HL2: haiku + 2x luna | `t2-1` = claude-haiku-5-5 | `t4-1` = gpt-6-luna | `t3-1` = gpt-6-luna | haiku (flagger) | `t2-1` as haiku, as in batch 9 |

**Adaptation where `REQ` assumes ember.** On SL2 and HL2 the flagger is the slowest reviewer, so the flagger's card posts land **on** the critical path, and the cards reach the lunas later in the lunas' own runs. The design does not change the mechanism for this; it changes only which role's turn times enter the k formula (the critical-path role, as `REQ` timing rule 2 already does for F6 on SL2), and it logs the consequence (`late`, `k0_isolated`).

Planning numbers per panel (planning B and per-turn medians from `REQ` 2.0; T_report_p90 is unmeasured for every model and is set equal to the turn time here, as `REQ` does for luna; every number is replaced by Spike 4):

| Quantity | EL2 | SL2 | HL2 |
|---|---|---|---|
| Planning B per package | 116 s | 273.7 s | 238 s |
| Critical-path turn_p90 / T_report_p90 (planning) | luna 6.4 / 6.4 s | sonnet 14 / 14 s | haiku 23 / 23 s |
| k at planning values | 2 (optimistic; `REQ` books k = 1 as central) | 2 | **0** |
| k >= 1 needs | T_report_p90 <= 19.4 s (B = 116 s) | T_report_p90 <= 51.795 s (`REQ` rounds it to 51.8) | 3 turn_p90 + T_report_p90 <= 81.3 s, for example both at most 20.3 s |
| Card cap 2k | 4 (k = 2) or 2 (k = 1) | 4 or 2 | 0 at planning values |
| PANEL_FINISH_AT - T0 | 143.8 s | 341.5 s | 275.3 s |
| Planned end, k = 1 / k = 2 | 130.8 s / 143.6 s (luna adjudicates; `REQ` (d)) | 303.7 s / 331.7 s (sonnet posts 2k cards at 14 s each) | 286 s at k = 1 (above PANEL_FINISH_AT at planning turn times, which is why k is 0) |
| Finish-signal bound 1.35 B | 156.6 s | 369.5 s | 321.3 s |
| Hang guard 1.5 B | 174 s | 410.6 s | 357 s |
| Flagger's 3rd tool call (first possible card) | about 10 s | about 42 s | about 69 s |
| Luna's delivery window (6th call to end, historical medians) | about 38-102 s | about 38-102 s | about 38-102 s |
| Brief slowdown limit s on the critical-path role, k = 2 / k = 1 (W = hooks 2 s + 2k turns + one turn of slip) | 5.7% / 16.7% | 8.7% / 18.9% | not runnable / 5.2% |
| What the slowdown falls on | the luna paragraph (5 lines) | the sonnet paragraph plus card posts | the haiku paragraph plus card posts |

Consequences the owner should expect, stated now so they are not read as results later:

- **EL2** is the design as `REQ` specifies it; every gain row of `REQ` (f) applies.
- **SL2**: sonnet's first card can come at about 42 s, while the lunas usually finish near 102 s; cards posted late in sonnet's 270 s run arrive after the lunas have ended and are logged `late`. The `late` share is the main mechanism number on this panel. The extra 2k sonnet turns add to the panel's elapsed time directly.
- **HL2**: at planning turn times k = 0 on every package, so the launcher would run the whole row isolated. The launcher therefore **refuses** `PANEL_COLLAB=1` on a values file where k = 0 for all three packages and prints `F7 not runnable on <panel>: k = 0 on every package (values <sha>)`, rather than producing an isolated run labelled F7. Whether HL2 runs depends on Spike 4's measured haiku turn times (section 7, open question 1).
- On every panel the deal and the forms are identical, so the form contrast (challenge against finding) is measured the same way.

The flagger paragraph is the same text on every panel; only `{CAP}` and `{HELPER}` differ.

## 4. `PANEL_COLLAB=0`: the isolated baseline (arm A1) on the same harness

`PANEL_COLLAB=0` is read only by `run-panel.sh`. With it, the launcher creates no board, writes no settings file and no helper, appends no brief paragraph, and passes no `--settings`; everything else is the same code path: the same sandboxes (H3, H4), the same brief with the source.md sentence (H1), the same H2 normalise and re-ask, the same hang guard at T0 + 1.5 B_A1, the same retry rule, the same concurrent start of the three reviewers, the same merge, anonymiser, judge and results row. This is `REQ`'s kill switch (R-05): it restores the isolated panel **with** the harness fixes, not today's `RR`.

The reviewer launch line under `PANEL_COLLAB=0`, compared token by token with `RR:48`:

| `RR:48` | `PANEL_COLLAB=0` | Allowed by |
|---|---|---|
| `cd /tmp/evalsb/repo` | `cd SBR/sb/<pkg>/repo` | R-03 (H3, H4) |
| `timeout 3000` | `timeout --kill-after=5 <seconds to T0 + 1.5 B_A1>` | R-43 hang guard |
| `--no-session-persistence` | removed | R-05 (needed for the H2 `--resume`) |
| (absent) | `--session-id <uuid>` | deviation D-5: not in R-05's list; it fixes the transcript name in advance so a killed reviewer's transcript is found exactly (timing and audit) and has no effect on what the model sees |
| brief text | `RR:13-17` plus one H1 sentence | R-01 |
| every other token (`claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit`, brief on stdin) | identical | none needed |

The re-ask line adds `--resume <id> --output-format stream-json --verbose` (R-05 allows stream-json on re-ask sessions). Under `PANEL_COLLAB=1` the only further difference is `--settings <file>` on attempt 1 and the role paragraph in the brief; attempt 2 is always the `PANEL_COLLAB=0` line.

What the baseline still records, so the two arms are compared on the same fields: `finish_would_fire` (a reviewer still running at PANEL_FINISH_AT, not acted on, R-41), `reask_s`, `attempts`, `retry_s`, `hang_kill`, `own_line_jaccard`, `ledger_rows`, `elapsed_s`, `overhead_pct`, and `collab.json` with `arm: "A1"`, card fields 0 and design-only fields `null`.

The A1 rows of a panel are also Spike 4's input: B_A1, turn_p90 and T_report_p90 come from them (2.7). Recommended order per panel: 4 `PANEL_COLLAB=0` rows with `values/planning-<P>.json` (Spike 4), freeze `values/<P>.json`, then interleave further A1 rows and F7 rows in blocks (one A1 row, one F7 row per block, order chosen by a coin) so gateway drift hits both arms alike (`REQ` 4, block randomisation). Whether the 4 Spike-4 rows count toward A1's 12 is open question 2.

## 5. The launch script (`bin/run-panel.sh`) and the results row

### 5.1 Steps

```bash
PANEL_COLLAB=1 NOFALLBACK=1 R4/bin/run-panel.sh --panel EL2 --row f7-el2-r01 --values R4/values/EL2.json --block b01
PANEL_COLLAB=0 NOFALLBACK=1 R4/bin/run-panel.sh --panel EL2 --row a1-el2-r01 --values R4/values/EL2.json --block b01
```

`--block <id>` (optional) names the randomised block the row belongs to; it is written to `runs/schedule.jsonl` with the row's panel, arm, start and end (R-28) and used for `baseline_drift` (2.9).

0. **Preflight (refuse before any work).** Exit 2 with one line on stderr, and append `{"row":...,"time":...,"reason":...}` to `runs/refusals.jsonl`, never creating or touching `runs/<row>/` (so a refused re-run can never damage a finished row), when: `NOFALLBACK` is not `1`; `PANEL_COLLAB` is not `0` or `1`; the panel is unknown; `runs/<row>/` already exists (a retry is a new row id, so no attempt mixes with another); `sha256sum -c frozen/pins.sha256` fails; the values file's sha256 differs from `<values>.sha256`; any panel model is outside `allowed_models`, matches `glm` or `qwen` (case-insensitive) or is an Opus model; the flagger model is `gpt-6-luna`; `PANEL_COLLAB=1` and k = 0 on every selected package; a sandbox's `built.json` is missing or `SBR/cand/<pkg>/candidate.md` does not match `manifest.json`. **Concurrency** (`REQ` 4: at most 10 concurrent runs and at most 4 ember): before each package, take `flock SBR/launch.lock`, count model sessions host-wide with `pgrep -fc '(^|/)claude -p( |$)'` and ember sessions with `pgrep -fc '(^|/)claude -p --model muse-ember-1.0( |$)'`. On this host `/usr/local/bin/claude` is a wrapper that `exec`s the real binary by its full path (`/opt/nvm/versions/node/v24.22.2/bin/claude -p --model ...`, seen with `ps` while this design was written), so the pattern matches the path ending in `/claude`, while the `timeout` and `bash reviewer.sh` processes (whose command lines contain ` claude -p` after other words, not after `/` or at the start) are not counted; S0 re-checks the pattern against a live session. The count is host-wide on purpose, so other experiments' sessions on the same gateway also count. Start the package only when at most 7 sessions and, for EL2, at most 3 ember sessions are running; otherwise release the lock and poll every 30 s, refusing the remaining packages after 30 minutes. The lock is released once the three reviewers are started. Three panels launched together therefore stay at 9 reviewer sessions, plus any judge sessions.
1. **Row start.** Write `run.json` (panel, models, `PANEL_COLLAB`, `NOFALLBACK`, values path and sha256, pins result, seed, start time). The seed is `--seed` or 32 bits from `/dev/urandom`; package j (0, 1, 2 in `packages.json` order) gets coins `r = (seed >> 2j) & 1` and `c = (seed >> (2j+1)) & 1` (`REQ`'s `run` is `<row>/<pkg>`, so coins are per package-run).
2. **Per package, in order** (packages run one after another; the three reviewers of a package run at the same time, which F7 needs):
   1. `mkdir -p runs/<row>/<pkg>/{reviews,tags,scoring}`. If `PANEL_COLLAB=1` and k >= 1: create `SBR/board/<row>/<pkg>/{msgs,state,snap,metrics,settings,bin}`; write `settings/<rid>.json` for each reviewer as `{"hooks":{"PostToolUse":[{"hooks":[{"type":"command","command":"<R4>/bin/r4-hook --board <dir> --rid <rid> --role <role> --flagger <flagger rid> --t0-ms <T0> --finish-ms <F> --k <k> --deliver <0|1> --c <c>","timeout":5}]}]}}` (no matcher, so every tool fires it; S0 confirms); write `bin/card` as `exec <R4>/bin/panel-post --board <dir> --rid <flagger> --run <row>/<pkg> --cand-flat <file> --cap <2k> --t0-ms <T0> --finish-ms <F> --r <r> --peers t4-1,t3-1 "$@"` and `chmod +x` it. T0 and F are filled in step 2.2, before any reviewer starts.
   2. `T0` = now in ms; `F = T0 + 1000 x finish_offset_s`; `H = T0 + 1000 x hang_s`. Write `panel.json`.
   3. Start the three `reviewer.sh` processes in the background and `wait` for all three.
   4. If a board exists, `cp -a` it to `runs/<row>/<pkg>/board/` (R-26; the original stays in `SBR`).
   5. **Merge** (R-04, the `merge-b11.sh:17-38` pattern). If any reviewer has `model_mismatch: true` (served by another model), the package is `invalid_model` and is not merged (the `SPEC.md` batch-3 rule: never merge a degraded panel). A reviewer that was killed or produced no block is still passed to the merge through its always-present `<rid>.final.md`; the merge keeps the others and records that reviewer's block as invalid. Otherwise build `resolution.json` from `EVAL/<pkg>/resolution-live7.json` with `.reviewers` replaced by the panel's three entries (`reviewer_id`, `model`, `alias`, `tier` from `panels.json`, `strategy: "fixed"`, `stand_in: false`, `fallback_depth: 0`, `fallbacks: []`, `launch: null`, `seed: null`, `slot_id`), then run `superclaude review merge --ledger <pkgdir>/ledger.json --doc SBR/cand/<pkg>/candidate.md --round 1 --report <rid>=<pkgdir>/reviews/<rid>.final.md (x3) --resolution <pkgdir>/resolution.json --out <pkgdir>/merged-1.md > <pkgdir>/merge-stdout.txt 2>&1`. A non-zero exit is recorded as `merge_refused` with the first line of the output; it is never retried by editing a report.
   6. `uv run --frozen --project REPO python R4/lib/collab.py <pkgdir>`.
3. **Audit** (after the last package, so every reviewer of the row has exited before any ground truth is opened): `audit.py runs/<row>`. It checks each used sandbox with `git -C SBR/sb/<pkg>/repo status --porcelain` (must be empty; `--ignored`-only files are listed as `ignored_only`), the candidate's sha256 against `manifest.json`, `.dev/reflect` absent, every board line through `card.jq` (a line that fails, or whose sha does not match a `post_accepted` metrics event, counts in `board_lines_invalid`), and every reviewer transcript's tool calls against the violation patterns of 2.10 (row "Reviewers never see ground truth"). Then the contamination check against each `EVAL/<pkg>/ground-truth.json`. Harness-authored text is the frozen move catalogue, the frozen templates and the two role paragraphs; a rendered card is exactly that text plus the model-authored anchor, so checking the frozen files covers every rendered card. That text must contain no `plan_quote` substring of 12 characters or more and no path named in a `description` (`harness_text_gt_overlap`, must be 0). `brief-a1.txt`, which must stay byte-identical to `RR` in both arms, is checked the same way but its overlap is only reported (`a1_brief_gt_overlap`), because no arm could change it. Card anchors that overlap a `plan_quote` by 12 characters or more are counted in `anchor_gt_overlap` and listed, not failed (open question 3). Any violation sets `audit.json` `"violations"` non-empty; the row stays scored but `results.py` marks it `audit_ok: false`, and the launcher writes a `QUARANTINED` file naming the violations into `runs/<row>/` and into each board copy (R-26's quarantine in place; nothing is moved or deleted).
4. **Anonymise** each merged package: `anon.sh merged-1.md scoring/merged-anon.md`. Rules: reviewer ids from `panels.json` are replaced, whole word, by `R1`, `R2`, `R3` in a random order (saved in `scoring/label-key.json`, never shown to the judge); the `candidate:` header line becomes `candidate: <candidate file> sha256 <8 hex>`; `report <path>` becomes `report <redacted>`; any path containing `evalsb-collab-r4`, `r4-flag-and-adjudicate` or `20261113-collab` becomes `<redacted>`; the `EVAL` prefix becomes `<EVAL>`; `"origin":"own"`/`"origin":"peer"` keys are deleted; `[panel card cN]`, `panel card cN`, a bare `panel card`, `card cN: passed` and every other `card cN` (all case-insensitive, `\bcards? c[0-9]+\b`) are deleted. `\b(a|another|the) peer reviewer\b` is replaced by `a reviewer` (a phrase the lunas may use naturally; failing on it would drop only F7 packages and bias the comparison). The script then greps the output, case-insensitively, for the forbidden strings of 2.10, which after these rules can only survive through a rule bug, and exits 1 (the package is `anon_failed`, not judged) on any hit. Together with the adjudicator brief's instruction not to mention a card or a peer in a finding (2.4), this keeps the F7 arm from being recognisable by its wording; a residual phrase the patterns do not foresee is a known limit (risk 14).
5. **Judge** each anonymised package: `judge.sh <pkgdir> <pkgdir>/scoring/merged-anon.md`:
   1. `L` = 4 random capital letters; `STAGE = mktemp -d /tmp/jdg.XXXXXXXX` (outside `SBR`, so it is never next to a reviewer sandbox); copy the file to `STAGE/<pkg>/<L>/merged-anon.md`.
   2. `C = realpath -m --relative-to="$EVAL/arms/scoring/combos" "$STAGE"`; assert that `realpath -m "$EVAL/arms/scoring/combos/$C"` equals `STAGE` and that `STAGE` is not inside `EVAL`.
   3. Touch a stamp file, then run `(cd "$STAGE" && bash "$EVAL/tools/tmp-scripts/judge-one.sh" "$C" "<pkg>" "$L")`. `judge-one.sh` then writes `judge.json`, `judge.err` and (through the Opus judge) `score.json` into `STAGE/<pkg>/<L>/`.
   4. Accept when `score.json` parses and has `gt_covered_any`, `gt_covered_blocking` and `wrong_blockers`, and `judge.json`'s result text has no `API Error` (the R-29 API-error audit). Otherwise rename the three files to `*.attempt1.*` (so `judge-one.sh` does not skip) and run once more; a second failure marks the package `judge_failed`.
   5. Fail the package with `judge_wrote_into_eval` if `find "$EVAL" -newer <stamp>` lists anything.
   6. Copy `score.json`, `judge.json`, `judge.err` (and any `*.attempt1.*`) to `<pkgdir>/scoring/` and add `label`, `stage` and `C` to `label-key.json`. `STAGE` is deleted by a `trap` set right after `mktemp` (`rm -rf -- "$STAGE"`, guarded by a check that `$STAGE` matches `/tmp/jdg.*`), so it is removed on success, on failure and on a signal; it holds ground truth in `judge.json`, and the kept copy is the one under `R4/runs/`.
6. **Results**: `uv run --frozen --project REPO python R4/lib/results.py runs/<row> --out results/<row>.json`; print one summary line (`found /14, real blocking /8, control /2, elapsed per package, cards sent/delivered`).
7. Write the end time and `"status":"done"` (or the first failing package status) into `run.json`. The launcher's own exit code is 0 when the row is fully scored, 1 otherwise.

`--no-judge` stops after step 3 (used by Spike 4 runs, which need timing only, and by offline tests). There is no session cleanup step: transcripts are copied into `runs/` and the originals are left in place (R-46 only constrains a cleanup if one is done).

### 5.2 Results row (`results/<row>.json`)

`results.py` is the first code that reads ground truth for scoring; it runs only after every reviewer of the row has exited.

| Field | Definition |
|---|---|
| `schema`, `row`, `panel`, `arm` (`F7` or `A1`), `panel_collab`, `models` (rid to model), `values_sha256`, `pins_ok`, `seed`, `started`, `finished` | from `run.json` |
| `valid` | true only when all three packages are merged and judged and no reviewer has `model_mismatch`; when false, every total below is `null` (never a partial sum) |
| `found_14` | `len(gt_covered_any)` designSpec + alias |
| `real_blocking_8` | count of `gt_covered_blocking` ids whose `blocking_in_implement` is true, designSpec + alias (the "REAL" view of `final-table.py:3-4`) |
| `judge_blocking` | `len(gt_covered_blocking)` designSpec + alias |
| `wrong_blockers` | `wrong_blockers` designSpec + alias |
| `control_found_2` | `len(gt_covered_any)` on `TASK-WF-design-20261108-041415` |
| `control_wrong_blockers` | `wrong_blockers` on the control package |
| `output_tokens` | sum of `output_tokens_all` over every reviewer, every attempt and every re-ask (judge tokens excluded, as in `final-table.py`) |
| `elapsed_s` | per package `{DS, AL, DE}`: `(max reviewer t_end_ms - T0) / 1000`, retries and re-asks included (R-24) |
| `overhead_pct` | per package, against the values file's B_A1 |
| `reach`, `reach_ids` | the hard-target credits (2.9 `reach`) |
| `packages.<pkg>` | `status` (`ok`, `invalid_model`, `merge_refused`, `anon_failed`, `judge_failed`), `label`, `gt_covered_any`, `gt_covered_blocking`, `real_blocking`, `wrong_blockers`, `ledger_rows_total`, `ledger_rows_blocking`, `output_tokens`, `slo_breach`, `dropped_lines`, `reask_count` |
| `collab.<pkg>` (collaboration counters) | `k`, `k0_isolated`, `deal_r`, `deal_c`, `cards_sent`, `cards_rejected` (by reason: `too_early`, `over_cap`, `after_finish`, `bad_*`, `anchor_not_in_candidate`, `invalid`), `cards_delivered`, `late`, `no_snapshot`, `snapshot_missing`, `conversions` (`challenge` and `finding`, each `delivered`, `converted`, `credited`, `uncredited`), `passed_lines`, `card_tasks`, `early_tasks_only` (designSpec only: every card Task is before Task 8, the falsifier of `REQ` (f)), `flag_finding_overlap`, `adjudication_agreement`, `finish_signal_fired`, `finish_would_fire`, `hang_kill`, `retry_isolated`, `hook_error`, `hook_ms_p95`, `own_line_jaccard`, `pairwise_task_jaccard`, `ledger_rows`; for A1 rows the same keys, card counts 0 |
| `audit` | `audit_ok`, `violations`, `sandbox_clean`, `candidate_sha_ok`, `board_lines_invalid`, `harness_text_gt_overlap`, `a1_brief_gt_overlap`, `anchor_gt_overlap`, `first_hand_suspect`, and the descriptive lists `ignored_only`, `tmp_other`, `home_other` |

**Judge-credited conversion** (R-36) is computed here: a converted line (receiver id plus finding id) belongs to the ledger row whose `members` contain it; the conversion is `credited` when that row's `anchor` or `anchor2` has `overlap12` with the `plan_quote` of a ground-truth item listed in the package's `gt_covered_any`, else `uncredited`. The unchanged judge does not output which row matched which item, so this is an approximation, labelled in the row as `"credited_method": "row anchor overlaps a covered plan_quote"` (section 7, risk 6).

## 6. Test plan

All automated tests run offline with `uv run pytest R4/tests` from `REPO` (bats is not installed, so shell scripts are driven through `subprocess`). Tests set `R4_SBR` and `R4_OUT` to a `tmp_path`, put `tests/fake-claude` first on `PATH` where a model call would happen, and never call a real model. Real-model checks are the Gate 0 spikes (6.3) and the smoke test (6.4).

### 6.1 Unit tests

| File | Component | Cases (each a separate test) | Pass condition |
|---|---|---|---|
| `test_card_validator.py` | `lib/card.jq`, `panel-post` | 3 good cards (M3, M4, M9; different categories); 1 enum-tagged flagger card; 6 bad lines: `claim` on a card, `verdict` key, `category` on a non-card line (`kind:"move"`), move `M1`, anchor of 11 characters, a 601-byte line; plus `from` = a luna id, and an extra `note` key; a 3rd post with cap 2 | the 4 good lines pass unchanged; every bad line yields no output; the 3rd post exits 1 with `refused: over_cap` and logs `post_rejected` (R-06 verification set) |
| `test_panel_post.py` | `panel-post` | `calls` = 1 refused `too_early`, `calls` = 2 accepted (R-34); post at `finish_ms` refused `after_finish`; an anchor that differs from the candidate only in whitespace is accepted and stored flattened; text not in the candidate refused `anchor_not_in_candidate`; deal with `r = 0` gives `to` = t4-1, t3-1, t4-1, t3-1 for c0..c3 and with `r = 1` the reverse; 8 concurrent posts with cap 8 | each case's exit code, stderr reason and metrics line match; the concurrent case yields exactly 8 valid lines with ids c0..c7, each once |
| `test_hook.py` | `r4-hook` | simulated tool calls 1..10 for a luna with 4 cards on the board (k = 2, c = 0, r = 0); same with c = 1; a flagger hook with cards on the board; `--deliver 0`; a clock past `finish_ms`; the hook run under `env -i` with only the baked arguments | no delivery before call 6; luna t4-1 receives c0 then c2, forms challenge then finding; luna t3-1 receives c1 (finding) then c3 (challenge); with c = 1 the forms are F, C, C, F for c0..c3 (R-35); never more than one card per call or more than k per luna; the flagger never receives a card; `--deliver 0` delivers nothing; past `finish_ms` the finish text is printed exactly once and nothing is delivered afterwards (R-41); under `env -i` delivery still works (R-21); every output is exactly the `hookSpecificOutput` object and at most 1,500 characters; `snap/<rid>.sha256` matches the snapshot and was written before the first delivery |
| `test_normalize.py` | `lib/normalize.py` | a fixture report with a 250-character anchor; a 350-character claim; an anchor with line breaks; a bad severity; a report with no findings block; running it twice | anchor cut to its first 200 flattened characters and still found by `findings.locate` in the candidate, `parse.json` `ok: true`, `truncated: 1` (R-02); claim cut to 300; unchanged lines byte-identical; bad severity gives `ok: false` with the parser's message; no block gives `ok: false`; second run changes nothing |
| `test_values.py` | `lib/values.py` | `k_of(116, 6.4, 6.4)`; `k_of(116, 6.4, 11.0)`; `k_of(100, 6.4, 13.8)` and `13.9`; `k_of(273.7, 14, 51.795)` and `51.8`; `k_of(238, 23, 23)`; `k_of(238, 20.3, 20.3)`; `finish_offset(116, 6.4, 6.4)`; `hang_s(116)`; turn parsing on a fixture transcript with known timestamps, including a final assistant message written as two entries (thinking, then a long text block) and a sidechain entry; p90 over 4 and over 10 samples; `build`, `srun` and `slowdown` on fixture rows | 2; 1; 1 and 0; 1 and 0; 0; 1; 143.8 and 174.0 (compared with `pytest.approx`) (R-42 verification set, with the exact SL2 threshold, plus the HL2 rows of section 3); the two-entry final turn's duration runs to its **last** entry; the sidechain entry is ignored; nearest-rank p90 equals the hand-picked sample; each CLI writes its file and a matching `.sha256` |
| `test_collab.py` | `lib/collab.py` | `overlap12` on strings sharing exactly 12 and exactly 11 characters; `task_of` on an anchor in Task 3 of a fixture candidate and on one in Constraints; a luna line overlapping a delivered card anchor by 12 characters and one by 11; a flagger line that equals a card anchor; the `REQ` R-25 fixture where peer-tagged lines raise all-line Jaccard but not own-line Jaccard; `flag_finding_overlap` with 1 of 2 cards equal; a dealt card the luna never reached; `collab.json` schema | true and false; `"T3"` and `None`; `peer` and `own`; the flagger line stays `own`; own-line Jaccard unchanged while `pairwise_task_jaccard` rises; 0.5; status `late`; every R-23 key present, design-only keys `null` |
| `test_anon.py` | `bin/anon.sh` | a fixture merged report holding the three reviewer ids, the `EVAL` candidate path, an `SBR` path, `"origin":"peer"`, `[panel card c1]`, `card c0: passed` and a claim saying "Card c1 asks for the finite check"; a fixture whose claim says "a peer reviewer flagged this"; a fixture where an id is written as `T4-1` in a claim (case-sensitive replacement misses it, the case-insensitive check catches it) | the first output contains none of the forbidden strings and maps each id to the same `R<n>` everywhere; the second exits 0 with the phrase rewritten to "a reviewer flagged this"; the third exits 1 |
| `test_judge.py` | `bin/judge.sh` with `fake-claude` | one judge run; a run whose first `judge.json` contains `API Error`; a run that fails twice | `score.json` copied to `<pkgdir>/scoring/`; `realpath` of `EVAL/arms/scoring/combos/$C` is the staging directory, which is under `/tmp/jdg.` and not under `R4_SBR`; the staging directory no longer exists afterwards; `find EVAL -newer stamp` is empty; the `judge-one.sh` file's sha256 is unchanged after the run; the API-error case runs the judge exactly twice; the double failure marks `judge_failed` |
| `test_results.py` | `lib/results.py` | fixture `score.json` files for the three packages plus fixture ground truth (copies with known `blocking_in_implement` and `plan_quote` values); one package `judge_failed`; a converted line whose ledger row overlaps a covered `plan_quote` | totals equal hand-computed `found_14`, `real_blocking_8`, `judge_blocking`, `wrong_blockers`, `control_found_2`, `control_wrong_blockers`; with a failed package `valid: false` and every total `null`; the conversion counted `credited` |
| `test_arm_summary.py` | `lib/arm_summary.py` | 12 fixture F7 rows with `cards_sent = 0` in 7; pooled `flag_finding_overlap` 0.6; own-line Jaccard 0.16 above A1; ledger rows 21% below A1; snapshot missing for 3 of 4 receiving lunas; agreement 0.95 and 0.04; 12 runs (36 package-runs) with 4 and with 3 package-runs above 1.35 B_c; one row with `audit_ok: false`; reach 0 vs 4, 1 vs 6, 2 vs 7 of 12; a form-contrast fixture | `STOP:no_cards`; `STOP:flag_finding_overlap`; `CONVERGENCE` fires for both the Jaccard and the ledger-row case; `SNAPSHOT`; `AGREEMENT` both ways; SLO budget exceeded at 4/36 and not at 3/36 (limit 1/12); `independence` fails on the audit row; Fisher p = 0.047, 0.034 and 0.045 to 3 decimals (`REQ` 4 table); z and run-paired difference equal hand-computed values |
| `test_reviewer.py` | `bin/reviewer.sh` with `fake-claude` (argv logged) | `PANEL_COLLAB=0` launch; `PANEL_COLLAB=1` launch | the logged argv equals `RR:48`'s tokens except the differences listed in section 4 (R-05); collaboration adds only `--settings <file>` and the role paragraph |
| `test_launcher.py` | `bin/run-panel.sh` with `fake-claude` | each refusal of 5.1 step 0 (no `NOFALLBACK`, a `glm`, `Qwen` or Opus model in a test copy of `panels.json`, luna as flagger, pins mismatch, values sha mismatch, all k = 0 under `PANEL_COLLAB=1`, existing row); one full offline row with `PANEL_COLLAB=1`; one with `PANEL_COLLAB=0` | each refusal exits 2 before any reviewer starts and appends its reason to `runs/refusals.jsonl`; in the existing-row case the row's files (its `run.json` included) are byte-identical after the refused call; the full row writes every file of 1.5 and a results row with every 5.2 key, and appends one line to `runs/schedule.jsonl`; the three reviewers of a package start within 2 s of each other; the `PANEL_COLLAB=0` row creates no board directory and no settings file; the concurrency count ignores `timeout` and `bash reviewer.sh` processes whose command lines contain `claude -p` or the model name |
| `test_build_sandbox.py` | `bin/build-sandbox.sh` (real trees, slow) | build into a `tmp_path` `R4_SBR`; build again | no `.dev/reflect`, `.dev/eval-workspaces`, `.dev/research` or `.dev/tasks/done` in any sandbox; `manifest.json` lists the 3 trees of `packages.json`; `git status --porcelain --ignored` is empty; candidate sha256 equals `EVAL`'s; at least one file the designSpec candidate's Tasks edit differs between the sandbox and `REPO` HEAD (H3 spot check); the second build skips all three |
| `test_pins.py` | `frozen/` | the catalogue, the templates and the two role paragraphs against the three `ground-truth.json` files (this test reads ground truth; it touches no reviewer path) | no `plan_quote` substring of 12 or more characters and no path from a `description` appears in any of them (R-07); `brief-a1.txt`'s overlap is printed, not asserted; `sha256sum -c frozen/pins.sha256` passes |
| `test_hook.py` (additional cases) | `r4-hook` | a hook input with a non-empty `agent_id`; a card line appended to `msgs/` with the flagger's `from` but no `post_accepted` event | the subagent call increments `subcalls`, not `calls`, and delivers nothing; the forged line is never delivered |

### 6.2 Fault injection (one test per failure mode)

| Failure mode | Injection | Expected |
|---|---|---|
| Flagger never posts (`REQ` (h) row 1) | fake flagger makes no `panel-post` call | `cards_sent = 0`; 7 such rows of 12 give `STOP:no_cards` |
| Cards spent on early Tasks (row 2) | fake flagger posts its cap on Task 1 sentences of the designSpec fixture | `card_tasks = ["T1", "T1"]`; results row flags `early_tasks_only: true` for designSpec (every card Task before Task 8, the falsifier of `REQ` (f)) |
| Flags behave like findings (row 3) | fake flagger's findings reuse 3 of its 4 card anchors | `flag_finding_overlap = 0.75`; arm summary `STOP:flag_finding_overlap` |
| Card overload (row 4) | fake lunas drop their own findings when they get cards | `ledger_rows` more than 20% below A1 fixtures; `CONVERGENCE` fires |
| Snapshot not written (row 5) | fake luna's hook JSON names a missing `transcript_path`; second variant makes `snap/` read-only | `snapshot_missing` logged, `state/<rid>.nosnap` exists, zero deliveries to that luna, the review completes with `final_ok: true` (R-10 fault test) |
| Wrong blockers from adjudications (row 6) | fixture rows with wrong blockers A1 + 1.5 | arm summary `no loss` fails |
| A luna runs past the finish signal (row 7) | fake luna keeps making tool calls past `finish_ms` | the finish text once, no delivery after it, `finish_signal_t` logged |
| A reviewer hangs (R-43) | fake luna sleeps past `hang_ms` in an A1 row and in an F7 row | killed at T0 + 1.5 B_A1 (within 6 s), `hang_kill: true`, `slo_breach: true`, the other reviewers' results kept |
| Hook error (R-22) | `state/<rid>.calls` holds `abc`; a garbage line before a valid card on the board | the hook prints nothing and exits 0, logs `hook_error`; the review completes; the garbage line is skipped and the valid card is still delivered |
| Attempt 1 fails (R-44) | fake run 1 has no findings block | attempt 2's argv has no `--settings` and the A1 brief; `retry_isolated: true`; `elapsed_s` covers both attempts; no delivery during attempt 2 |
| Parser drop (R-02) | fake report with a bad severity, and a re-ask reply still bad | exactly one re-ask (argv has `--resume`, `stream-json`, `--verbose`, no `--settings`); `reask_s` logged; `dropped_lines = 1` |
| Wrong model served (R-28) | fake result reports another model | `model_ok: false`, `model_mismatch: true`; the package is `invalid_model`, not merged; `valid: false` |
| One reviewer without a block | one fake luna returns a report with no findings block on both attempts | its `<rid>.final.md` exists (a copy of its report); the merge runs with all three `--report` arguments, exits 0, records that reviewer's `block_ok: false`, and the package is judged |
| No valid block from any reviewer | three fake reports without blocks | `merge_refused`; no judge call |
| Judge API error (R-29) | fake judge returns `API Error` twice | `judge_failed` after exactly two judge runs |
| Forged board line | a fake luna appends card lines directly to `msgs/`: one with its own id as `from`, one with the flagger's id | neither is delivered (the first fails `card.jq`, the second has no `post_accepted` event); `board_lines_invalid = 2` |
| Ground-truth access | fake transcripts with a Bash call naming `ground-truth.json`; one running `grep -r x /tmp`; one reading a `/tmp/jdg.` path | each gives a violation in `audit.json`, `audit_ok: false`, and a `QUARANTINED` file in the row |
| Sandbox write | fake reviewer runs `touch x` in its cwd | `sandbox_clean: false`, violation listed |
| Harness text leak | a test copy of `templates.json` containing a 12-character `plan_quote` substring | `harness_text_gt_overlap > 0`, violation listed |

### 6.3 Gate 0 spikes this design depends on (real models; results written under `R4/spikes/out/`)

| Spike | Command | Pass condition | If it fails |
|---|---|---|---|
| S0, for each of muse-ember-1.0, gpt-6-luna, claude-sonnet-5-5, claude-haiku-5-5 | `spikes/s0-req-s3.sh <model>`: one `claude -p` in the designSpec sandbox with `--settings` naming `spikes/probe-hook`, a brief of 8 simple read steps then `DONE` | the probe log has one hook input per tool call (at least 6) with a readable `transcript_path`; the probe-hook's copy and sha256 of the transcript at call 2 succeed; hook time per call is recorded; the log records which sandbox project hooks also fired; the transcript entries carry `timestamp` (needed by 2.7) and whether one assistant message is written as several entries; whether a tool call that exits non-zero (a refused `panel-post`) still fires PostToolUse; whether tool calls inside a subagent fire the session's hook and carry `agent_id`; that the concurrency pattern of 5.1 counts the live session exactly once; and that the `claude` wrapper (`/usr/local/bin/claude`, which `exec`s `ccsession-orca`) adds no `--settings` of its own to a `-p` run (two settings sources must merge, not replace) | hooks not firing, or no `transcript_path`: F7 cannot run on that model, so no panel using it runs. A "no" on the non-zero-exit or subagent question is recorded and the counter rules of 2.2 and 2.3 are re-checked against it before any arm. A wrong concurrency count or an extra `--settings` is a harness fix (adjust the pattern, or call the real binary), not a model failure |
| REQ-S3 act rate, same four models, 5 sessions each | same script: the probe-hook injects `run ls /tmp/panel-probe` after call 3 and the finish text after call 6 | the act rate (next tool call is that `ls`) and the finish act rate (the session ends within one turn) are recorded per model; they replace the planning act rates (R-47). The F7 arm runs only with a non-zero act rate for luna (the receiver) | the arm is not run; report the rate |
| S2, resume part, same four models | `spikes/s2-resume.sh <model>`: a `-p` session without `--no-session-persistence` says `ALPHA`; `--resume <session_id>` with `stream-json --verbose` says `BETA` and repeats the first word | a first session started with `--session-id <uuid>` writes `~/.claude/projects/<cwd project>/<uuid>.jsonl` (deviation D-5); the resumed reply contains both words and the observed model is right | H2 re-ask is skipped (`reask_skipped: no_session`) and reported for every arm; the run still proceeds |
| S3 full-chain smoke | section 6.4 | as 6.4 | fix before any arm |
| Spike 4, per panel | `values.py planning --panel <P>`; 4 rows of `PANEL_COLLAB=0 run-panel.sh --values values/planning-<P>.json --no-judge`; `values.py build`; `values.py srun`; 2 rows of `PANEL_COLLAB=1 --values values/<P>-srun.json --no-judge`; `values.py slowdown` | `values/<P>.json`, `values/<P>-slowdown.json` and their `.sha256` files committed before the first F7 row (R-30); s on the critical-path role within the section 3 limit for the package's k | a package whose budget fails is run at the measured k and the failure is reported (open question 4); a panel with k = 0 on every package is not run (section 3) |
| G0-F7 cards (the `REQ` 4 gate "`cards_sent > 0` in the spike") | the smoke test once per flagger model | `cards_sent > 0` on at least one package for each flagger model | the panel with that flagger is not run |
| Not needed | S1 (cross-session `SendMessage` fallback): the board is the only transport built here. Spike 5 (H2 re-scoring) measures the H share and is owned by the overall experiment, not by this build. | | |

### 6.4 One-package smoke test (spike S3)

```bash
R4/bin/build-sandbox.sh
uv run --frozen --project REPO python R4/lib/values.py planning --panel EL2
PANEL_COLLAB=1 NOFALLBACK=1 R4/bin/run-panel.sh --panel EL2 --row smoke-f7-el2-1 --values R4/values/planning-EL2.json --packages TASK-WF-design-20261108-041415
PANEL_COLLAB=0 NOFALLBACK=1 R4/bin/run-panel.sh --panel EL2 --row smoke-a1-el2-1 --values R4/values/planning-EL2.json --packages TASK-WF-design-20261108-041415
```

The smoke runs before Spike 4, so it uses the planning values file; after Spike 4, a repeat with `values/EL2.json` is part of AC-11. The smoke passes when, for the F7 row: all three `meta.json` have `model_ok: true`; `dropped_lines = 0` for every reviewer (the S3 rule, lesson `HO2:259`); `merged-1.md`, `merged-anon.md` and `score.json` exist; `collab.json` passes the schema check; `cards_sent >= 1`; every dealt card has a status (`delivered`, `late`, `no_snapshot` or `held`) and at least one is `delivered`, or every undelivered card is `late` with the luna's last tool call earlier than the card; every delivered luna has `seal_sha_ok: true`; `audit_ok: true`; the anonymiser's grep is clean; nothing under `EVAL` is newer than the run start; the results row has every 5.2 key. For the A1 row: the same, plus no board directory and no `--settings` in any argv. A single-package row is `valid: false` by definition (two packages are missing); the smoke checks the package entry, not the totals.

### 6.5 Acceptance criteria (each pass or fail)

| Id | Criterion |
|---|---|
| AC-01 | `uv run pytest R4/tests` passes with 0 failures and 0 errors. |
| AC-02 | Comparing `git status --porcelain --untracked-files=all` in `REPO` taken before the build with the same command after a full row, every new or changed path is under `R4/` (paths under the four other `20261113-collab/r*` folders are ignored, since other implementers write there); nothing under `src/` or `EVAL` changed. |
| AC-03 | `frozen/pins.sha256` checks out, and the pinned files keep the values measured when this design was written, before and after every judged row: `judge-one.sh` `a01bd70d370d73cb32b55a7368aa28e2c12d93403237211c3a71f339ae82cfcc`, `findings.py` `f0e53967a229e1d64a57451987e2922d98c0eb8808090110f1904ae1ba90ad5a`, `ledger.py` `2908549846e1a6c63f692d18c7e4c375e257590eb4671a17dba1b315218b8179`. A changed parser or ledger is not silently accepted: the pin fails and the implementer re-pins only on the owner's instruction. |
| AC-04 | Under `PANEL_COLLAB=0`, the reviewer argv differs from `RR:48` only as section 4 lists (test_reviewer). |
| AC-05 | No code path can start a reviewer model outside `allowed_models` (ember, luna, haiku, sonnet, grok; the three panels use only the first four), or a judge other than `claude-opus-5-5`: the reviewer script has no fallback ladder, and the launcher refuses `glm`, `Qwen`, Opus and luna-as-flagger panels and runs only with `NOFALLBACK=1` (test_launcher). |
| AC-06 | Every board line written in any test or run passes `card.jq`; every refused post is logged with a reason; no luna ever posts (board counts in every `collab.json`). |
| AC-07 | No card is delivered before a luna's 6th tool call, before its snapshot hash exists, after PANEL_FINISH_AT, or beyond k per luna; the flagger receives none (test_hook plus every smoke `collab.json`). |
| AC-08 | Dealing and forms follow R-35 exactly (test_hook vectors). |
| AC-09 | The hook never fails a review: every injected hook fault leaves `final_ok: true` and a `hook_error` line. |
| AC-10 | The hang guard kills at T0 + 1.5 B_A1 in both arms (fault test), and `elapsed_s` includes retries and re-asks. |
| AC-11 | The smoke test of 6.4 passes for EL2, and for each other panel that Spike 4 makes runnable. |
| AC-12 | A full EL2 row under each switch value produces `results/<row>.json` with `valid: true` and every 5.2 field, and `audit_ok: true`. |
| AC-13 | In every run, no reviewer tool result contains a content marker of 2.10 and no reviewer tool call names a path that 2.10 lists as a violation; `harness_text_gt_overlap = 0` on every row; no `/tmp/jdg.*` directory exists after a launcher exits. |
| AC-14 | No file under `EVAL` is created or changed by any run (`find EVAL -newer <row start>` is empty after every row). |

## 7. Risks and open questions

### 7.1 Risks

| # | Risk | Effect | Mitigation in this design |
|---|---|---|---|
| 1 | Reviewers have unrestricted Bash, so a reviewer can read the board, other runs' outputs or `EVAL/<pkg>/ground-truth.json` by absolute path | contamination that no tool list prevents | enforced by audit, as `REQ` 5.5 accepts: transcript scan for those paths, `audit_ok: false` on any hit (AC-13); detected after the fact, not prevented |
| 2 | On SL2 and HL2 the flagger is the slowest reviewer | card posts add directly to panel elapsed time, and many cards arrive after the lunas end (`late`); results on these panels measure a different time profile from `REQ`'s EL2 design | k is computed from the flagger's turn times; `late` is logged per card; the expectation is stated in section 3 before any run |
| 3 | HL2 is probably not runnable: k = 0 at planning haiku turn times | an HL2 F7 row would be an isolated run | the launcher refuses `PANEL_COLLAB=1` when k = 0 on every package (open question 1) |
| 4 | The judge's output is steered by a relative `C` through `EVAL/arms/scoring/combos` | if that directory is ever removed, every judge call fails; if the judge model's Read tool mishandles `..` in a path, scores are wrong | `judge.sh` asserts the resolved path and fails the package (`judge_failed`), never writing into `EVAL`; the smoke test checks a real judge run end to end |
| 5 | Unverified CLI behaviour: `session_id` in the `--output-format json` result; `timestamp` on transcript entries in `-p` sessions; a hook with no matcher firing for every tool; `transcript_path` in PostToolUse input | timing (k), re-ask and snapshot code paths | each is a pass condition of S0 or S2 (6.3); a failure blocks or degrades exactly the part named there |
| 6 | Judge-credited conversion is an approximation (row anchor overlapping a covered `plan_quote`), because the unchanged judge does not report row-to-item matches | the R-36 credited and uncredited split may misassign some conversions | labelled `credited_method` in every row; the primary endpoints (found, reach) do not use it |
| 7 | The base trees' own `.claude/settings.json` registers project hooks whose scripts are gitignored and therefore absent from the sandbox | non-blocking hook errors in every reviewer session | identical in both arms; S0 records which fire |
| 8 | A reviewer whose first attempt fails runs attempt 2 isolated | its cards are lost for that package | logged `retry_isolated`; counted in the arm's delivery numbers |
| 9 | This folder builds A1 and F7 only; `REQ` defines collaboration C as F7 - A2 (static kit) and the harness share H as A1 - A0 | F7 - A1 here mixes C with any prompting effect of the card briefs; H is not measured here | results are labelled "F7 against A1"; A2 and A0 belong to the shared controls, outside this build |
| 10 | Power: at 12 runs the plan cannot detect the central gain estimate of any slot (`REQ` 4) | a null result is likely even if F7 helps a little | stated in every summary; the mechanism logs (cards sent, delivered, converted by form) are the main output of a screen |
| 11 | The flagger meets early Tasks first and may spend its 2k cards before designSpec Task 8 or 12 | the B5, I1 and I4 gain rows go toward 0 | `card_tasks` and `early_tasks_only` logged per package (the falsifier `REQ` (f) names); the brief is not changed to steer selection, because that would change the treatment |
| 12 | `/tmp` can be cleared by a reboot | `SBR` boards and sandboxes lost | every board is copied into `runs/` right after its package; sandboxes are rebuilt by `build-sandbox.sh` from pinned trees |
| 13 | `REQ` R-10's check "grep `merged-anon.md` for `origin` returns 0" cannot pass on designSpec, whose candidate contains "origin" 8 times as a substring (2 as a whole word) | a literal implementation fails any designSpec package whose findings quote those sentences | the anonymiser check uses the key pattern `"origin":` (2.10) |
| 14 | A luna may still describe a card in words no pattern foresees ("the flagged sentence") | the judge could guess the F7 arm from wording | the adjudicator brief forbids mentioning a card or a peer in a finding; the anonymiser deletes the `card cN` forms and rewrites "peer reviewer" to "a reviewer" (it never fails a package for natural wording, which would drop only F7 packages); residual wording is not detectable mechanically |
| 16 | Reviewers of other rows run while a row is judged, as the same user, so ground truth in `/tmp/jdg.*` (and `EVAL`, as always) is reachable in principle | contamination of a concurrent row | staging is deleted on every exit path; the two-layer audit (content markers in tool results, plus path names) flags the row; prevention would need a separate OS user, which this build does not have |
| 15 | Subagent tool calls and failed tool calls may or may not fire PostToolUse | call counts (the 3rd-call and 6th-call gates) could be off by those calls | subagent calls are counted apart and never receive cards (2.3 step 2); both behaviours are S0 checks |

### 7.2 Open questions (each needs the owner's decision; a recommendation is given)

1. **HL2 when k = 0.** At planning haiku turn times (23 s) k = 0 on every package, so F7 cannot run on haiku + 2x luna without breaking `REQ`'s k rule. **Recommendation:** keep the same role mapping on every panel and the same k rule; run HL2 only if Spike 4 measures haiku's turn_p90 and T_report_p90 low enough for k >= 1 on at least one package (3 turn_p90 + T_report_p90 <= 81.3 s), and otherwise report "F7 not runnable on HL2" with the measured values. The alternative (computing k from luna's turns on HL2) would put the haiku card posts outside any budget and break the +35% target by design.
2. **Do the 4 Spike 4 rows count toward A1's 12 runs?** They run the same code as A1 but with the planning hang guard instead of the measured one. **Recommendation:** count a Spike 4 row toward A1 only if no `hang_kill` fired in it, and record which rows were counted.
3. **CONTRADICTION[`REQ`:970 vs `REQ`:216-217 and `REQ`:1017].** Section 4, decision rule 5 (`REQ`:970) requires that "no board message ... contains a ground-truth `plan_quote` substring of 12 characters or more". Redesign 4 and R-08 (`REQ`:216-217, :1017) require every card anchor to be an exact substring of the candidate, taken from the flagger's flagged sentence, and the ground-truth `plan_quote` values are themselves quotes from the same candidate. A card that flags the right sentence therefore always breaks rule 5 as written. The evidence cannot resolve which reading the authors meant. **Recommendation (implemented by default):** apply the zero-tolerance rule to harness-authored text only (the move catalogue, the templates and the two role paragraphs, which are every part of a rendered card except its anchor), where a ground-truth quote could only come from a leak, and report model-authored card anchors that overlap a `plan_quote` as the descriptive count `anchor_gt_overlap`, which is also a direct measure of how often the flagger flagged a defect sentence.
4. **Brief budget failure.** `REQ` timing rule 5c says a design whose budget B_A1 (1 + s) + W exceeds 1.35 B_A1 "drops brief content until it fits"; F7's brief additions are already minimal and have nothing optional. **Recommendation:** if Spike 4's s exceeds the section 3 limit for a package, still run the F7 arm at the measured k, mark the package `budget_fail` in `values/<P>-slowdown.json`, and let the time verdict (R-24) record the failure, rather than shortening the move texts, which would change the treatment.
5. **SLO error budget unit.** R-24 says "1 package in 12 per arm". **Recommendation (implemented):** at most 1/12 of the arm's package-runs may exceed 1.35 B_c (3 of 36 at 12 runs; B_c as in 2.9); the stricter reading (1 package-run per arm) would stop an arm after two slow packages.
