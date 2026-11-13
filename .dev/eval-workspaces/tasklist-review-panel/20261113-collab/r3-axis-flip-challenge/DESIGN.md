# Design: Redesign 3, Axis-Flip Challenge (F1), implementation and test specification

Grounding: index_state: fresh (checked_at 2026-11-13T19:30:38Z, projectPath /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel); codegraph tools used: codegraph_status, codegraph_files, codegraph_search, codegraph_node; every quoted line was then read with Read or sed.

Status: design only. Nothing in this document is built. Review: three independent reviews (`design-report/independent-review.md`, `-2.md`, `-3.md`). Every blocking finding was fixed; the last fix (9.4 and 13.5: gitignored writes such as `.venv/` are logged and cleaned, not quarantined) came after review 3, the review cap, and has not been independently re-reviewed. Every number marked "planning" is replaced by the values file (section 14) before an arm runs.

**Path abbreviations.**

| Name | Absolute path |
|---|---|
| `REPO` | `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel` |
| `EVAL` | `REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1` (read only for this design) |
| `R3` | `REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge` (the only place code and outputs are written) |
| `SB` | `/tmp/evalsb-collab-r3` (this design's sandbox root) |
| `REQ` | `REPO/.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md` (source of truth) |
| `RR` | `EVAL/tools/run-reviewer.sh` |

**Sources read for this design**: `REQ` sections 1, 2.0, 2.1, Redesign 3 (lines 576-700), 3, 4 and 5.1-5.10; `RR:1-87`; `EVAL/tools/tmp-scripts/judge-one.sh:1-31`; `anon-b11.sh`, `anon-arms.sh`; `EVAL/analysis/merge-b11.sh`, `b11-launch.sh`, `b8-table.py` (helpers), `b9-table.py`; `EVAL/tools/tmp-scripts/b4-job-one.sh`; `EVAL/combos/SPEC.md:1-152`; `src/superclaude/cli/review/findings.py` (`parse_block` :124-196, `_check_finding` :90-121, `flat` :272, `locate` :276); `ledger.py` (`merge_round` :107-157, `render_merged_report` :408-494); `merge_cmd.py:21-118`; the item ids, classes and `blocking_in_implement` flags of `EVAL/<pkg>/ground-truth.json` (field shape only, for the results row; no description or quote is copied here); `claude --help` of Claude Code 2.1.323.

**How to read.** Sections 2 and 3 list what to create. Sections 4-10 give exact behaviour in run order. Section 11 maps roles onto the three panels. Sections 12-14 cover the switch, the launch script and the values file. Section 15 is the test plan with pass/fail acceptance criteria. Section 17 maps every requirement of `REQ` 5.1, 5.2, 5.3, 5.5, 5.6 and 5.10 to a file and a test.

## 1. Scope, constraints and resolved ambiguities

### 1.1 What is built

One self-contained harness under `R3` that runs one review panel (one strong reviewer plus two luna reviewers) on the three study packages, in two modes:

- `PANEL_COLLAB=1` (arm A3): phase 1 is the isolated review with the harness fixes; after each reviewer's phase 1 the harness sends it a digest of peer anchors (or gap cards), each paired with an "other axis" move, resumes its session for phase 2, and folds the phase-2 findings into the reviewer's single findings-v1 block.
- `PANEL_COLLAB=0` (arm A1): the same phase 1 with the same harness fixes; no digest, no phase 2.

Each launch merges each package with `superclaude review merge`, anonymises the merged report, judges it with the unchanged `EVAL/tools/tmp-scripts/judge-one.sh`, and writes one results row.

### 1.2 Hard constraints

| Id | Constraint | Where enforced |
|---|---|---|
| K1 | All code and outputs under `R3`; sandboxes under `SB`; no write to `REPO/src`, to `EVAL` or to another redesign's folder | `r3_assert_writable` in `lib/common.sh` (refuses any output path outside `R3`, `SB` or the test temp root); acceptance criterion AC-14 |
| K2 | Reviewer models only `muse-ember-1.0`, `gpt-6-luna`, `claude-haiku-5-5`, `claude-sonnet-5-5`, `grok-4.7`; never Qwen or glm; Opus only as the judge | `r3_assert_model` allowlist; unit test `test_model_allowlist` |
| K3 | Reviewers read-only: `--disallowedTools Edit Write NotebookEdit`; because Bash is open, enforced by audit | `lib/reviewer.sh`; `audit` (9.4) |
| K4 | Reviewers never see ground truth; no harness step before judging reads `ground-truth.json` | only `cli.py result` and the judge read it; transcript audit for `ground-truth` reads |
| K5 | `NOFALLBACK=1`: this harness has no fallback ladder; the launcher exports `NOFALLBACK=1` and every runner refuses to start without it | `r3_assert_nofallback` |
| K6 | UV for all Python: `uv run --frozen --project "$REPO" python "$R3/r3lib/cli.py" ...`; tests `uv run --frozen --project "$REPO" pytest -p no:cacheprovider "$R3/tests"`; merge `uv run --frozen --project "$REPO" superclaude review merge ...`. Every Python step runs with `PYTHONDONTWRITEBYTECODE=1`, so importing `superclaude.cli.review` writes no `__pycache__` into `REPO/src`, and `--frozen` never rewrites `uv.lock`. Every `uv run` in this document means this form | `r3_py` in `lib/common.sh`; all callers |
| K7 | Grading rule, judge script and findings-v1 merge contract unchanged and sha256-pinned | `config/pins.json`; launcher preflight |

### 1.3 Ambiguities in `REQ` and how this design resolves them

Each resolution is the default the implementer follows; section 16 lists those the owner may want to overrule.

| # | Ambiguity or conflict | Resolution |
|---|---|---|
| A1 | The routing table pairs two moves per anchor class ("M3 or M2", "M4 and M7", "M5 and M6"), but `panel-msg/1` carries one `move`, and R-13 says search moves go to the searcher and reading moves to luna. | One move per challenge, picked by the receiver's style (table in 6.4). A mapping or constraint anchor has no search move in the catalogue, so the searcher gets M6 or M8. |
| A2 | `REQ` 4 rule 5 forbids any digest that contains a ground-truth `plan_quote` substring of 12+ characters, but every F1 anchor is, by design, an exact candidate quote; a peer anchor on a real defect will contain such a substring. | The ground-truth grep covers every digest byte except the `anchor` field. Anchors are checked for provenance instead: a real anchor equals the flattened anchor of a peer phase-1 finding; a gap anchor comes from the gap extractor, which never opens ground truth. The overlap is logged as `gt_anchor_overlap` (descriptive only). Recorded as Q1 in section 16. |
| A3 | "The digest holds anchors from every peer that has finished at that moment" assumes the strong reviewer finishes first (EL2). On SL2 and HL2 it finishes last. | A receiver launches phase 2 when every one of its source peers has sealed or failed, or gives up (no launch) the moment n would reach 0. On EL2 this reproduces `REQ` exactly (lunas find ember done at about 41 s; ember waits for both lunas). |
| A4 | The phase-2 box `min(35, T0 + 1.30 B_f - t_launch)`: 35 s is about 0.30 x 116 s (34.8), an EL2 constant; on SL2 and HL2 it would give the strong reviewer n = 1 or 0 by construction. | `box_cap` is per panel in `config/panels.json`: 35 on EL2 (as `REQ`), `null` (no cap) on SL2 and HL2, where the box is then the time left to the phase-2 deadline. |
| A5 | A gap card's `from` is "the same value" as a real challenge. | A gap card's `from` is the receiver's first source peer id; the rendered prompt never shows `from`, `id` or `t`. |
| A6 | R-05 lists the only allowed launch-command differences; preassigning `--session-id` would be a new one. | The session id is read from the phase-1 result object (`.session_id`); no new flag. |
| A7 | `judge-one.sh` hardcodes `EVAL` and writes `score.json` to `EVAL/arms/scoring/combos/<C>/<P>/<L>/`, which would put files inside `EVAL`. | Run it byte-unchanged with `C` set to this design's scoring row expressed relative to `EVAL/arms/scoring/combos`, so its `D` resolves under `R3/scoring/` (10.2). Ground truth and candidate are still read from `EVAL/<P>/`. |
| A8 | The merged report prints finding ids (`#### L3.t4-1 (P2-F1)`), which would tell the blind judge which arm produced it. | The anonymiser renumbers every finding id per report in both arms and fails if `P2-` survives. |
| A9 | Phase-1 lines are "verbatim", but must carry `"origin":"own"` (R-10). | Phase-1 lines in the final report are the sealed lines after the H2 normaliser (5.4 step 2, applied identically in A1), plus the `origin` key; nothing else changes. The immutability check compares each final line, `origin` removed, with `normalise(sealed line)`. |
| A10 | The A1 hang guard needs B_A1, which Spike 4 measures with A1 runs. | Every run needs the frozen values file, except two labelled exceptions that never reach `results/results.jsonl`: Spike-4 runs (`R3_SPIKE4=1`, `PANEL_COLLAB=0` only, legacy 3000 s timeout, rows to `spikes/spike4/rows.jsonl`) and smoke runs (`R3_SMOKE=1`, either mode, planning values from `packages.json` per package with hang guard T0 + 1.5 B_planning, rows to `results/smoke.jsonl`). |

### 1.4 Not built

- Arms A0 (today's harness) and A2 (static move kit). Without A2, the prompting share P cannot be separated from C.
- The HL2 shadow variant of `REQ` (haiku isolated, lunas exchange with each other); this design runs the main F1 mechanism on HL2 (section 11).
- A scheduler for 12 block-randomised runs per arm. One launch is one run; 13.4 shows how to drive repeated launches.
- Board hooks, `panel-post`, transcript snapshots and `--settings` JSON from `REQ` 2.0: F1 uses none of them (`REQ` Redesign 3 (g): "No hooks are needed"). The `board/` directory holds only digests and the event log.

## 2. File inventory

### 2.1 Source files to create (all paths relative to `R3`)

| Path | Purpose | Interface |
|---|---|---|
| `config/panels.json` | Panel definitions: roles, reviewer ids, models, styles, caps, `box_cap`, critical role, planning B | JSON, schema in 3.1 |
| `config/packages.json` | Package ids, base commit (H3), planning B per panel | JSON, schema in 3.2 |
| `config/routing.json` | Selection categories, surface regex, anchor-class regexes, move-by-style table | JSON, 3.3 |
| `config/catalogue.json` | Frozen move texts M1-M10, copied verbatim from `REQ:184-193` column "Move (text sent to a reviewer)" | JSON `{"M1":"...",...}` |
| `config/phase1-brief.txt` | The A1 brief: `RR:13-17` text with four placeholders (`{CAND}`, `{SHA}`, `{SRC}`, `{SRC_SHA}`), including the H1 sentence (3.4) | text template |
| `config/phase2-frame.txt` | Frozen phase-2 prompt frame (7.2) | text template |
| `config/fallback-frame.txt` | Frozen fresh-session phase-2 prompt preamble (7.3) | text template |
| `config/reask-frame.txt` | Frozen H2 re-ask prompt (5.4) | text template |
| `config/pins.json` | sha256 of `judge-one.sh`, `findings.py`, `ledger.py`, `merge_cmd.py`, every `config/*` file except `pins.json`, and the `REPO` commit used | JSON; written once by `cli.py pin`, checked by the launcher |
| `lib/common.sh` | Sourced by every shell file: paths, guards (`r3_assert_writable`, `r3_assert_model`, `r3_assert_nofallback`), `r3_now` (epoch seconds with milliseconds), `r3_event` (append one JSON line to `board/events.jsonl` under `flock`), `r3_py` (the UV wrapper) | bash functions |
| `bin/build-sandbox.sh` | Builds `SB/<pkg>/repo` from the package's base commit (H3, H4) and `SB/cand/<pkg>/` (candidate and source.md) | `build-sandbox.sh <pkg>`; exit 0 built or already valid, 2 invalid |
| `lib/reviewer.sh` | Phase 1 (with retry, H2 re-ask, seal) and phase 2 (resume or fresh, deadline kill, phase-2 re-ask) of one reviewer | `reviewer.sh phase1 <pkgdir> <rid> <model>`; `reviewer.sh phase2 <pkgdir> <rid> <model>`; `reviewer.sh print-cmd <pkgdir> <rid> <model> phase1|reask|phase2|fallback|p2reask` (dry run that prints one command form with deadlines as `<T>` and ids as `<id>`, for R-05 and `test_command_diff`) |
| `lib/package.sh` | One panel on one package: T0, phase-1 launches, phase-2 scheduler, combine, merge, sealed merge, metrics, audit | `package.sh <rundir> <pkg>`; exit 0 package valid, 3 package invalid (reason in `pkg.json`) |
| `bin/launch-panel.sh` | The one launch script (section 13) | `PANEL_COLLAB=0|1 launch-panel.sh <el2|sl2|hl2> [--pkgs <id>...] [--tag <text>] [--no-judge]` |
| `bin/cleanup-sessions.sh` | Deletes only the session files this run recorded, once no other run on the same sandbox is active (R-46) | `cleanup-sessions.sh <rundir>` |
| `bin/spike-s2.sh` | Gate 0 spike S2 (resume and stream-json per model) | `spike-s2.sh <model>` |
| `r3lib/__init__.py` | Empty | |
| `r3lib/cli.py` | argparse dispatcher for every Python subcommand below | `uv run --project $REPO python r3lib/cli.py <sub> ...` |
| `r3lib/findings_io.py` | H2 normaliser and validator (through the real parser), phase-2 line extraction and salvage, combiner | functions in 8.1 |
| `r3lib/digest.py` | Selection, surface filter, router, deal, gap cards, n, rendering, `panel-msg/1` validator | functions in 6.9 |
| `r3lib/metrics.py` | `collab.json`, own-line Jaccard, ECHO, ledger rows, audits, anonymiser, results row, arm summary | functions in 9.6 and 10.4 |
| `r3lib/values.py` | Spike-4 measurement and freeze; k and PANEL_FINISH_AT formulas; n formula | functions in 14 |
| `tests/conftest.py` | Temp roots (`R3_RUNS_ROOT`, `R3_SB_ROOT`, `R3_SCORING_ROOT`), fake `claude` on `PATH`, fixture loaders | pytest fixtures |
| `tests/fakes/claude` | Bash wrapper: `exec uv run --project "$REPO" python "$R3/tests/fakes/fake_claude.py" "$@"` | stands in for `claude` |
| `tests/fakes/fake_claude.py` | Scripted fake of `claude -p` (15.1) | reads `FAKE_CLAUDE_PLAN` |
| `tests/fixtures/` | Report, block, stream and score fixtures listed per test in 15 | files |
| `tests/test_*.py` | Unit and fault-injection tests (15.2, 15.3) | pytest |

### 2.2 Generated directories (never deleted; R-26)

```
R3/runs/<run_id>/                      run_id = <panel>-c<0|1>-<YYYYmmddTHHMMSSZ>-<4 hex>
  run.json                             panel, collab, values sha, pins sha, REPO HEAD, NOFALLBACK, tag, smoke flag
  <pkg>/
    pkg.json                           T0, B_f, deadlines, sandbox tree sha, candidate and source sha, valid/invalid + reason
    reviews/<rid>.attempt<a>.json|.err|.md|.meta.json      phase-1 attempts (json output, as RR)
    reviews/<rid>.reask.stream.jsonl|.err|.md               phase-1 H2 re-ask
    reviews/<rid>.p1.md  <rid>.p1.sha256  <rid>.p1.session.jsonl   sealed phase 1, its hash, its session transcript copy
    reviews/<rid>.p2.stream.jsonl|.err|.md|.meta.json       phase 2
    reviews/<rid>.p2reask.stream.jsonl|.err|.md             phase-2 re-ask
    reviews/<rid>.p2.session.jsonl                           phase-2 transcript copy
    reviews/<rid>.md  <rid>.combine.json  <rid>.meta.json  <rid>.cost.json   final report and accounting
    board/<rid>.digest.jsonl  <rid>.digest.json  <rid>.prompt.txt           digest lines, deal/seed log, rendered prompt
    board/events.jsonl                                       scheduler and process events
    merged/resolution.json ledger.json merged-1.md merge-stdout.txt
    merged-sealed/...                                        same, from the sealed p1 reports (collab only)
    collab.json  audit.json
  scoring-keys.json                     label -> (run_id, pkg, kind full|sealed); never under scoring/
  result.json
R3/scoring/<row>/<pkg>/<L>/merged-anon.md, score.json, judge.json, judge.err     row = "s" + 10 random hex
R3/results/results.jsonl               one row per non-smoke launch (append under flock)
R3/results/smoke.jsonl                 smoke rows
R3/values/<panel>.json, <panel>.json.sha256
R3/spikes/<spike>/...                  Gate 0 records
SB/<pkg>/repo/                         sandbox (git repo with one "snap" commit)
SB/<pkg>/active/<run_id>               marker while a run uses that sandbox
SB/<pkg>/pending-cleanup.txt           session files queued for deletion
SB/<pkg>/sandbox.json                  base commit, tree sha, build time (5.1)
SB/<pkg>/p1/<run_id>/<rid>.p1.md       read-only copy of a sealed report, made only for a fresh fallback (7.3)
SB/cand/<pkg>/candidate.md, source.md
SB/admit.lock                          admission lock (13.3)
```

### 2.3 `r3lib/cli.py` subcommands

| Subcommand | Arguments | Output | Exit codes |
|---|---|---|---|
| `pin` | `[--check]` | writes `config/pins.json`; with `--check` compares only | 0 ok; 1 mismatch (`--check`) |
| `normalize` | `--in <report> --out <report> --json <h2.json>` | normalised report and `{block_present, lines_total, lines_valid, errors, would_drop, block_errors}` | 0 clean; 3 lines would drop or block unclosed; 4 heading or block missing |
| `digest` | `--pkgdir D --rid R --t-launch <epoch> --start-cost 6\|16` | `board/<rid>.digest.jsonl`, `.digest.json`, `.prompt.txt`; prints `{"n":..,"slots":[..]}` | 0 at least one slot; 5 nothing to launch |
| `combine` | `--pkgdir D --rid R` | `reviews/<rid>.md`, `<rid>.combine.json`, `<rid>.p1norm.md` | 0; 7 `E_COMBINE` |
| `metrics` | `--pkgdir D` | `collab.json` | 0 |
| `audit` | `--pkgdir D` | `audit.json`, `QUARANTINE` on violation | 0 clean; 8 violation |
| `anon` | `--in <merged-1.md> --out <merged-anon.md>` | anonymised report | 0; 6 residue |
| `result` | `--rundir R` | `result.json` and one appended row | 0 |
| `values-freeze` | `--panel P --runs <run_id>...` | `values/<panel>.json` and `.sha256` | 0; 1 refused |
| `summarize` | `--panel P [--results F]` | JSON and markdown table on stdout | 0 |
| `calibrate-surface` | `--rows <glob of historical reviewer .md files>` | match share per model, 20 sampled matches and non-matches | 0 |
| `dry-digest` | `--rows <glob> --panel P` | per-receiver qualifying anchors and slot counts at planning n | 0 |

Environment overrides (tests only): `R3_RUNS_ROOT`, `R3_SB_ROOT`, `R3_SCORING_ROOT`, `R3_RESULTS_ROOT`, `R3_VALUES_FILE`, `R3_CLAUDE_PROJECTS` (session transcript root, default `~/.claude/projects`; every `~/.claude/projects` in this document means this root). Defaults are the paths above; `r3_assert_writable` accepts an override only under `/tmp/`.

## 3. Frozen configuration

All files in `config/` are written once, then hashed into `config/pins.json` by `cli.py pin`. The launcher refuses to run if any hash differs (`E_PIN_MISMATCH`). Changing a config file therefore needs a new pin and is visible in `run.json`.

### 3.1 `config/panels.json`

```json
{
 "el2": {"label": "ember + 2x luna",
   "searcher": {"rid": "t2b-1", "model": "muse-ember-1.0", "style": "search", "cap": 3},
   "readers":  [{"rid": "t4-1", "model": "gpt-6-luna", "style": "reading", "cap": 2},
                {"rid": "t3-1", "model": "gpt-6-luna", "style": "reading", "cap": 2}],
   "box_cap_s": 35, "critical_role": "readers"},
 "sl2": {"label": "sonnet + 2x luna",
   "searcher": {"rid": "t1b-1", "model": "claude-sonnet-5-5", "style": "search", "cap": 3},
   "readers":  [{"rid": "t4-1", "model": "gpt-6-luna", "style": "reading", "cap": 2},
                {"rid": "t3-1", "model": "gpt-6-luna", "style": "reading", "cap": 2}],
   "box_cap_s": null, "critical_role": "searcher"},
 "hl2": {"label": "haiku + 2x luna",
   "searcher": {"rid": "t2-1", "model": "claude-haiku-5-5", "style": "search", "cap": 3},
   "readers":  [{"rid": "t4-1", "model": "gpt-6-luna", "style": "reading", "cap": 2},
                {"rid": "t3-1", "model": "gpt-6-luna", "style": "reading", "cap": 2}],
   "box_cap_s": null, "critical_role": "searcher"}
}
```

Source peers (who a receiver's challenges come from) follow from the roles: each reader's source is the searcher; the searcher's sources are both readers, in `readers` order. Reviewer ids are labels only (as in `EVAL/combos/SPEC.md:16`); the ids above are the ones earlier batches used for these models (`merge-b11.sh:6`; batch 9 haiku `t2-1`, `SPEC.md:140`), and all match the anonymiser's `\bt[0-9a-z]+-[0-9]+\b` pattern.

### 3.2 `config/packages.json`

| Package | Role | Base commit (H3) | How it was derived | Planning B (s): el2 / sl2 / hl2 |
|---|---|---|---|---|
| `TASK-WF-designSpec-20261107-075614` | defect-rich, 10 GT items | `0e486ab8d0eb24c6f2738ce1f895cc16755b26c1` | parent of `0b8a5801d` (first commit adding the package and `merge_guard.py`, `refs/merge-guard.md`) | 100 / 259 / 220 |
| `TASK-WF-makeTheAliasOnly-20261105-051649` | defect-rich, 4 GT items | `38eb3c58afe6988b51060ae14117172869ea4c1e` | parent of `4eb75698d` (master commit that adds the package and edits `refs/tiers.md`, `refs/chains.md`) | 120 / 302 / 238 |
| `TASK-WF-design-20261108-041415` | control, 2 GT items | `5fa680778718af9087ccbe7a823e3909f1bcceb6` | parent of `54e21668f` (master commit that adds the package and edits `tests/skills/test_worker_contract.py`) | 122 / 269 / 226 |

Planning B values are the historical per-package medians of `REQ:276-278` (without harness fixes). The base commits are this design's resolution of the `REQ:1124` gap ("not recorded in an obvious file"); Gate 0 check G0-H3 (15.4) verifies them before use.

`packages.json` also lists, per package, `masked_paths`: the files the implementing commit changed that the plan edits (designSpec: `src/superclaude/pr_submit/merge_guard.py`, `src/superclaude/skills/sc-pr-submit-protocol/refs/merge-guard.md`, `src/superclaude/commands/pr-submit.md`; alias: `src/superclaude/skills/sc-issue-protocol/refs/tiers.md`, `src/superclaude/skills/sc-issue-protocol/refs/chains.md`; control: `tests/skills/test_worker_contract.py`). `build-sandbox.sh` checks each against the base version (5.1).

### 3.3 `config/routing.json`

```json
{
 "select_categories": ["unpassable-check", "contradiction", "missing-requirement"],
 "surface_regex": "(?i)(artifacts?/|\\bartifact path\\b|\\.dev/|\\bsha-?256\\b|\\bhash(es)?\\b|\\bline (number|\\d+)\\b|\\b(edit|file) scope\\b|:\\d+\\b|\\bpath (does not|doesn't) exist\\b)",
 "classes": [
   {"name": "quantifier", "regex": "(?i)\\b(every|all|complete|completely|only)\\b"},
   {"name": "command",    "regex": "(?i)(`[^`]*\\b(grep|rg|find|pytest|uv|superclaude|jq|git|wc)\\b|\\bgrep\\b)"},
   {"name": "mapping",    "regex": "(?i)(^\\||\\|.*\\||->|→|=>|\\b(maps?|mapping|mapped|table|row|column)\\b)"},
   {"name": "constraint", "regex": "(?i)\\b(must|must not|never|shall|at most|at least|no more than|required|forbidden|do not)\\b"}
 ],
 "move_by_style": {
   "quantifier":    {"reading": "M3", "search": "M2"},
   "command":       {"reading": "M4", "search": "M7"},
   "mapping":       {"reading": "M5", "search": "M6"},
   "constraint":    {"reading": "M8", "search": "M8"},
   "contradiction": {"reading": "M8", "search": "M8"}
 },
 "gap_probability": 0.3333333333333333
}
```

Regexes are Python `re` syntax applied to the whitespace-flattened anchor (`findings.flat`). `surface_regex` applies to the peer's `claim`. The surface regex is a starting value: Gate 0 spike G0-SURF calibrates it on historical findings before it is pinned (15.4).

### 3.4 `config/phase1-brief.txt`

The text of `RR:13-17` with `$CAND_SB` replaced by `{CAND}` and `$SHA` by `{SHA}`, and one sentence inserted immediately after `review 1 of 3.` (H1):

> `Its source document is {SRC} (sha256 of the file: {SRC_SHA}); read the candidate and the source document in full before you review.`

Nothing else differs. Unit test `test_phase1_brief_equals_rr` rebuilds the brief from `RR` lines 13-17 and asserts the only difference is that sentence (and the path values).

### 3.5 `config/phase2-frame.txt` (frozen; placeholders in braces)

```
Second pass on the same candidate {CAND} (sha256 {SHA}); its source document is {SRC}.
Below are {N} places in the candidate, each with one investigative move. A listed place does not mean anything is wrong there; some places are picked at random. For each place, carry out the move at that place (in the candidate, the source document and the repository), then decide whether it shows a concrete wrong outcome, using the same grading rules as your first report.
{CHALLENGES}
Rules: report only new findings; never repeat, change or withdraw a finding from your first report. As soon as you finish a place, write either one complete findings-v1 JSON line for it, with id C1, C2, ... matching the place number, or the line "no finding C<number>". Do not mention this second pass, the places or the moves in any claim. End your reply with the heading '## Findings block', one fenced code block with info string findings-v1 holding only these new lines (it may be empty), and a final 'verdict: PASS' or 'verdict: FAIL' line.
```

`{CHALLENGES}` renders each slot as two lines: `C<k>. Place: "<anchor>"` and `    Move: <catalogue text of the move>`. The move id, `from`, slot type and message id are never rendered.

### 3.6 `config/fallback-frame.txt`

```
Earlier you reviewed the candidate {CAND} and wrote the report {P1COPY}. Read that report first; it is your own first report.
```

followed by the grading-check sentences of `RR:17` only (from `Grading check, for each finding before you mark it blocking:` up to and including `... rather than a stated text that does harm.`), then the findings-v1 field list sentence of `RR:17` (`one JSON object per line: id, severity ..., claim`), and then the full `phase2-frame.txt` text. The report-format sentences of `RR:17` ("write 'review: 1 of 3'", "Your final reply must be the complete report text") are left out, because they conflict with the phase-2 rule "report only new findings, ids C1, C2, ...". A fresh session thus gets the same grading rules a resumed one already holds. `{P1COPY}` is `SB/<pkg>/p1/<run_id>/<rid>.p1.md`, a copy made only for the fresh fallback (7.3).

### 3.7 `config/reask-frame.txt`

```
Your report's findings block has these problems, reported by the findings parser:
{ERRORS}
Reply with your complete report again, with the same findings, each line fixed so it passes: id at most 16 characters, severity CRITICAL, MAJOR or MINOR, a MINOR finding never blocking, anchor and anchor2 12 to 200 characters copied exactly from the candidate, at most 8 refs, claim at most 300 characters. Keep the '## Findings block' heading, exactly one findings-v1 block and the final verdict line.
```

`{ERRORS}` is at most 10 lines `line <n>: <msg>` from `parse_block`; a longer list ends with `... and <m> more`.

## 4. Lifecycle of one panel on one package

`lib/package.sh <rundir> <pkg>` runs these steps. Times are epoch seconds (`r3_now`, millisecond precision); every step appends an event to `board/events.jsonl` (`{"t":..,"rid":..,"ev":..,...}`).

| Step | Action | Collab only |
|---|---|---|
| 1 | Read the values for `<panel>/<pkg>` (B_f, turn_p90 per model, T_report_p90, k, finish offset). Touch `SB/<pkg>/active/<run_id>`. | |
| 2 | Wait for admission (13.3). Record `T0 = r3_now`; derive `P2_DEADLINE = T0 + 1.30 B_f` and `HANG_AT = T0 + 1.5 B_f` (Spike-4 runs: `T0 + 3000`; smoke runs: B_f = the package's planning B; A10). All deadline arithmetic is done on times relative to T0 (`t_rel = now - T0`), never on raw epoch values, so float rounding stays below 1e-12 s. Write `pkg.json`. | |
| 3 | Start `reviewer.sh phase1` for the three reviewers in the background, all at T0. Each writes `reviews/<rid>.p1.state` when done: `sealed`, `failed` (no valid report) or `hang_kill`. | |
| 4 | Scheduler loop, polling every 1 s until every reviewer is settled: for a reviewer in state `sealed` that has not been scheduled, apply the launch rule (6.8). On launch, run `cli.py digest` then `reviewer.sh phase2` in the background. On "no launch", record the reason. | yes |
| 5 | Wait for every background process. | |
| 6 | For each reviewer: `cli.py combine` builds `reviews/<rid>.md` (8.2). A1: the same command with no phase-2 inputs. | |
| 7 | Merge: `resolution.json` from `EVAL/<pkg>/resolution-live7.json` with `.reviewers` replaced by this panel's three reviewers (the `merge-b11.sh:17-25` pattern), then `superclaude review merge --round 1` (8.3). | |
| 8 | Sealed merge from the three `p1` reports (normalised, origin `own`) into `merged-sealed/`. | yes |
| 9 | `cli.py metrics` writes `collab.json`; `cli.py audit` writes `audit.json`. | |
| 10 | Remove `SB/<pkg>/active/<run_id>`; queue this run's session files for cleanup (13.2 step 8). | |

A package is **invalid** (exit 3, reason in `pkg.json`) when the merge refuses the round (no reviewer produced a valid block), or any reviewer ended phase 1 in state `failed` (both attempts failed the model, block or API check) or `hang_kill`. One rule, used everywhere (F8, F10, 10.5): the merge still runs with the reviewers that have a report, an invalid package is still judged when a merged report exists and is recorded in the row's `invalid_pkgs`, it is left out of quality means, and it stays in the time verdict (a `hang_kill` package is an `SLO_BREACH`). This follows `EVAL/combos/SPEC.md:24` ("record the reviewer as INVALID (reason) and continue") and `SPEC.md:79` (never report a degraded panel as a normal one).

Illustrative timeline, as it would run with a frozen values file holding `REQ`'s planning numbers (EL2, B_f = 116 s, turn_p90 luna 6.4 s, ember 3.2 s; `REQ:632-639`). A smoke run instead uses the package's own planning B (100, 120 or 122 s on EL2, section 3.2), and a Spike-4 run has no 1.5 B guard:

```
t=0      T0: ember, luna A, luna B start phase 1
t~41     ember sealed; waits (its sources are both lunas)
t~95     luna A sealed; source (ember) sealed -> launch: box 35, n=2, ends ~126.6
t~116    luna B sealed -> launch: box 34.8, n=2, ends ~147.6;  ember launch: box 34.8, n=3, ends ~141.2
t=150.8  P2_DEADLINE: any phase-2 or phase-2 re-ask process still alive is killed
t=174    HANG_AT: any phase-1 process still alive is killed (hang_kill, SLO_BREACH)
```

## 5. Phase 1 and the harness fixes H1-H4

### 5.1 Sandbox build: H3 and H4 (`bin/build-sandbox.sh <pkg>`)

1. `base=$(jq -r ...packages.json)`. Create `SB/<pkg>/repo.tmp`, run `git -C "$REPO" archive "$base" | tar -x -C SB/<pkg>/repo.tmp`.
2. Remove `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research`, `.dev/reflect` (R-03). Fail (exit 2) if any path containing one of the three package ids remains (`find ... -path '*TASK-WF-<id>*'`).
3. For each `masked_paths` entry: the sandbox file must be byte-equal to `git show base:<path>` (or absent in both); fail otherwise. This proves the repaired text (for example the designSpec `refs/merge-guard.md` content of the implementing commit) is not in the sandbox.
4. `git init -q`, `git add -A`, `git -c user.name=r3 -c user.email=r3@localhost commit -q -m snap`, so `git status --porcelain` is empty and the reviewer sees no history beyond one commit.
5. `mv repo.tmp repo` (atomic). Write `SB/<pkg>/sandbox.json` with base, tree sha (`git rev-parse HEAD^{tree}`), and build time.
6. Candidate and source: copy `EVAL/<pkg>/candidate.md` and `REPO/.dev/tasks/done/<pkg>/source.md` to `SB/cand/<pkg>/` (copy only when the bytes differ, as `RR:8-11`). Fail if source.md is missing (H1 cannot hold without it).

An existing valid sandbox (step 3 passes and `git status --porcelain` is empty) is reused; any other existing sandbox makes the launcher stop with `E_SANDBOX_DIRTY`, because a dirty sandbox means an earlier reviewer wrote to it (K3). Gitignored files (for example `.venv/`) left by a run that is still active on the same sandbox are not a reason to refuse; the last run to finish removes them (13.5).

### 5.2 Phase-1 command (H1, R-05)

`reviewer.sh phase1` renders the brief from `config/phase1-brief.txt` (`{CAND}` = `SB/cand/<pkg>/candidate.md`, `{SHA}` its sha256, `{SRC}` and `{SRC_SHA}` likewise) and runs, from `SB/<pkg>/repo`:

```
timeout --kill-after=5 <HANG_AT - now> claude -p --model "<model>" --output-format json \
  --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <<<"$BRIEF"
```

Differences from `RR:48`, all allowed by R-05: the cwd (R-03), the brief (R-01), `--no-session-persistence` removed, and the `timeout` arguments (`--kill-after=5 <HANG_AT - now>` instead of `3000`), which together are the common hang guard (R-43). `reviewer.sh print-cmd ... phase1` prints this line with the timeout as `<T>` for the R-05 diff test.

**Session environment.** Every reviewer and judge session, in both arms, runs with `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` exported by `lib/common.sh`. The user-level SessionStart hook `~/.claude/hooks/codegraph-session-start.sh` otherwise starts `codegraph init` in the session's cwd (its opt-out is this variable, line 11), which writes a `.codegraph/` index into the sandbox (the old sandbox `/tmp/evalsb/repo` holds one). This is an environment setting, not a command-line difference, and is recorded in `run.json`.

### 5.3 Attempts, model check and retry (R-28, R-44)

Per attempt `a` (at most 2), outputs `reviews/<rid>.attempt<a>.{json,err,md,meta.json}` exactly as `RR:49-58` computes them: report text, observed model (`model_ok`), output tokens (main and all), `API Error` check, findings-block presence (`^```findings-v1`). Added fields: `session_id` (`[.[]|select(.type=="result")|.session_id][0]`), `t_start`, `t_end`, `timed_out` (exit 124 or 137).

- Attempt succeeds when `model_ok && block present && !api_error`.
- If attempt 1 fails and `now + 6 < HANG_AT`, attempt 2 runs (same command). In a collab run, attempt 2 marks the reviewer `retry_isolated`: it gets no digest and no phase 2, and its findings still feed its peers' digests.
- If both fail, phase-1 state is `failed`. If the timeout killed the process, the state is `hang_kill` and the package is marked `SLO_BREACH`.
- No fallback ladder exists. `r3_assert_nofallback` refuses to start unless `NOFALLBACK=1`.

### 5.4 H2: normalise, validate, re-ask once, then seal (R-02, R-11)

After the successful attempt, `cli.py normalize --in <attempt>.md --out <tmp> --json <rid>.h2.json`:

1. Parse with the real `superclaude.cli.review.findings.parse_block`.
2. For every line of the last findings-v1 block that is valid JSON: set `anchor` and `anchor2` to `flat(x)[:200]`, and `claim` to `flat(claim)[:300]`. A prefix of a flattened exact quote is still found by `locate`, which flattens too.
3. Re-parse the rewritten report. `would_drop` = errors whose line number lies inside the last block's body (line-level errors). Block-level errors ("more than one findings-v1 block", "not closed", `findings.py:143-158`) are recorded separately as `block_errors`; more than one block is not a re-ask reason (the combiner emits one block), an unclosed block is (exit 3).
4. Exit 0 when `would_drop == 0`; 3 when lines would drop; 4 when the heading or block is missing.

On exit 3 or 4, re-ask once if `now + 6 + turn_p90(model) < HANG_AT`, from `SB/<pkg>/repo`:

```
timeout --kill-after=5 <HANG_AT - now> claude -p --model "<model>" --resume "<session_id>" \
  --output-format stream-json --verbose --permission-mode bypassPermissions \
  --disallowedTools Edit Write NotebookEdit < <rendered reask-frame.txt> > reviews/<rid>.reask.stream.jsonl 2> reviews/<rid>.reask.err
```

Every resumed or re-asked session (5.4, 7.2, 7.3, 7.4) carries the same `--model`, `--permission-mode` and `--disallowedTools` as phase 1, and its `model_ok` is checked with the `RR:51-56` rule; `test_command_diff` asserts this for all four command forms. Take the result text (`jq -s '[.[]|select(.type=="result")|.result][0]'`); if it parses with fewer errors, it replaces the report; otherwise keep the earlier one. `reask_s` = re-ask wall time. Remaining invalid lines are `dropped_lines` (count and the parser messages) in `<rid>.meta.json`.

**Seal.** The report after the re-ask, before normalisation, is written as `reviews/<rid>.p1.md`; its sha256 goes to `reviews/<rid>.p1.sha256` and `pkg.json`, and the file mode is set to `0444`. It is never written again. The sealed session's transcript `~/.claude/projects/<cwd slug>/<session_id>.jsonl` is copied to `reviews/<rid>.p1.session.jsonl` (timestamps for Spike 4); every other session of the reviewer is captured by 9.5 for the audit. State becomes `sealed`.

## 6. Digest builder

`cli.py digest --pkgdir D --rid R --t-launch T --start-cost {6|16}` builds one receiver's digest from the sealed `p1.md` files of its source peers. It writes `board/<rid>.digest.jsonl`, `board/<rid>.digest.json` (the log) and `board/<rid>.prompt.txt`, prints `{"n":..,"slots":..}`, and exits 0 when at least one slot is filled, 5 when there is nothing to launch. The source of every rule is `REQ:578-616` and R-12, R-13, R-15.

### 6.1 Selection (R-12)

From each source peer's sealed report, parsed with `parse_block` and normalised as in 5.4, keep finding f only if all hold:

1. `f.category` is in `select_categories`.
2. `f.claim` does not match `surface_regex` (log `skipped_surface`).
3. `locate(candidate, f.anchor)` is non-empty (log `skipped_anchor_missing`); the anchor is an exact candidate quote.
4. The router (6.4) returns a move (log `skipped_no_route`).

Duplicates (equal flattened anchors) keep the first. Order: the peer's block order.

### 6.2 Deal (R-12, `REQ:596`)

- `deal_r` = lowest bit of `sha256("<run_id>|<pkg>|deal")`, logged.
- The searcher's qualifying anchor i (i = 0, 1, ...) goes to reader `(i + deal_r) mod 2` (index in `panels.json` `readers` order). The two readers therefore get disjoint anchors.
- The searcher's real queue is both readers' qualifying anchors interleaved: A0, B0, A1, B1, ... (readers order), skipping anchors whose author is the receiver (cannot happen by roles; asserted).

### 6.3 Slots and gap cards (R-12, `REQ:592`)

- Per receiver: `rng = random.Random(int(sha256("<run_id>|<pkg>|<rid>|slots").hexdigest(), 16))`.
- For slot j = 0..n-1: `is_gap = rng.random() < gap_probability`. A gap slot takes the next gap card; a real slot takes the next anchor from the receiver's real queue. A slot whose pool is empty stays empty (logged `slot_empty`); it is never filled from the other pool, so the gap share stays 1/3 by construction.
- **Gap pool** (built once per receiver, before slot draws): candidate lines that are not headings, not fence lines and not blank; flattened; at least 12 characters; truncated to 200 characters; that match one of the four anchor classes; and whose line range does not overlap the span (`locate`) of any anchor in any finished reviewer's phase-1 block, the receiver's own included. Pool order is shuffled with the receiver's `rng` before slot draws; gap anchors are routed with category `null` (no contradiction override).
- With no qualifying peer anchor, real slots are empty; gap slots are still filled when the pool is not empty (`REQ:615`). ECHO is "not applicable" for that receiver.

### 6.4 Router (R-13)

`route(anchor, category, style)`:

1. `category == "contradiction"` → class `contradiction`.
2. Otherwise the first class in `routing.json` order (quantifier, command, mapping, constraint) whose regex matches the flattened anchor.
3. No match → no move (finding not selected; for the gap pool, line not eligible).
4. Move = `move_by_style[class][style]`.

Searcher style is `search`, reader style is `reading` (`panels.json`). Never routes back to the anchor's author (6.2).

### 6.5 n per launch attempt (R-15)

```
box   = 1.30*B_f - (t_launch - T0);  if box_cap_s is not null: box = min(box_cap_s, box)   # relative times, never raw epoch sums
n     = max(0, min(cap, floor((box - start_cost) / (2 * turn_p90[model]))))
```

`floor` is taken as `floor(x + 1e-9)` here and in every k formula, so values that are exact on paper (for example (18.8 - 6) / 12.8 = 1 at a launch at T0 + 132.0 s) are not lost to floating-point error. `cap` from `panels.json` (searcher 3, reader 2); `start_cost` 6 (resume) or 16 (fresh fallback); `turn_p90[model]` from the values file. n is recomputed before every launch attempt, and a re-rendered digest replaces the earlier one (the earlier one is kept as `<rid>.digest.attempt1.jsonl`). `n_planned` = n at the first attempt; `n_launched` = number of filled slots actually sent.

### 6.6 Message lines (`panel-msg/1`)

One line per filled slot, in slot order:

```json
{"v":"panel-msg/1","id":"m-<rid>-<j>","run":"<run_id>/<pkg>","from":"<source peer rid>","to":"<receiver rid>","t":<epoch ms>,"kind":"challenge","move":"M5","anchor":"<12-200 chars>"}
```

For a gap slot, `from` is the receiver's first source peer (A5). No `items` and no `n` key (F1 sends none). Slot type is written only to `digest.json` (`slots[j].slot_type` = `real` or `gap`, plus `source_finding_id` for real slots).

### 6.7 Validator (R-06, R-08, subset used by F1)

`digest.validate_line(line, candidate_text, receiver, sources) -> (ok, reason)`; the builder runs it on every line and drops a failing line (logged `msg_rejected`, reason):

| Check | Reject reason |
|---|---|
| UTF-8 serialised length at most 600 bytes | `too_long` |
| Valid JSON object | `not_json` |
| Keys exactly `v,id,run,from,to,t,kind,move,anchor` (optional `items`, `n` allowed by schema but must be absent for `challenge`) | `forbidden_key:<k>` (includes `claim`, `verdict`, `blocking`, `severity`, `category`, `note`) |
| `v == "panel-msg/1"`, `kind == "challenge"` | `bad_kind` (cards, facts, coverage and moves belong to other redesigns and are rejected here) |
| `move` in M1-M10 | `bad_move` |
| `anchor` 12-200 characters after `flat`, and a substring of `flat(candidate)` | `anchor_not_in_candidate` / `anchor_length` |
| `from != to`, `from` in the receiver's sources | `self_or_unknown_source` |

The concatenated `digest.jsonl` lines must total at most 1,800 bytes (3 x 600, as `REQ:612` derives it; `digest_too_long`, the last slot is dropped until it fits). The rendered prompt is not capped by this rule.

### 6.8 Launch rule (scheduler, `REQ:607-615`, A3)

For a sealed receiver not yet scheduled, at each 1 s tick:

- If `retry_isolated` → no launch (`reason: retry_isolated`).
- Compute `n_now` with `start_cost = 6` at `t_launch = now`. If `n_now == 0` → no launch (`reason: deadline`). Because n never rises with time, this is final.
- If every source peer is `sealed`, `failed` or `hang_kill` → run `cli.py digest`; exit 5 → no launch (`reason: no_slots`); exit 0 → `reviewer.sh phase2`.
- Otherwise wait for the next tick (`waiting_for` logged once).

### 6.9 `r3lib/digest.py` functions

| Function | Signature | Returns |
|---|---|---|
| `load_findings` | `(report_path) -> list[dict]` | normalised findings (5.4 rules) |
| `qualifies` | `(f, candidate, routing, style) -> (bool, reason)` | 6.1 |
| `route` | `(anchor, category, style, routing) -> str or None` | move id |
| `deal` | `(searcher_anchors, readers, deal_r) -> dict[rid, list]` | 6.2 |
| `gap_pool` | `(candidate, all_anchors, routing, rng) -> list[str]` | 6.3 |
| `fill_slots` | `(n, real_queue, gap_pool, rng) -> list[slot]` | 6.3 |
| `compute_n` | `(T0, B_f, t_launch, box_cap, cap, start_cost, turn_p90) -> int` | 6.5 (lives in `values.py`, imported) |
| `render_lines` | `(slots, meta) -> list[str]` | 6.6 |
| `validate_line` | 6.7 | `(ok, reason)` |
| `render_prompt` | `(slots, frame, catalogue, paths) -> str` | 3.5 text |

## 7. Phase 2

### 7.1 Deadline (R-15)

One wall-clock deadline, `P2_DEADLINE = T0 + 1.30 B_f`, covers the resume or fallback, all challenges and any phase-2 re-ask. Every phase-2 process runs under `timeout --kill-after=3 <P2_DEADLINE - now>`. A kill logs `phase2_timeout` for that reviewer.

### 7.2 Resume (R-14)

From `SB/<pkg>/repo` (the same cwd as phase 1, required by `--resume`):

```
timeout --kill-after=3 <P2_DEADLINE - now> claude -p --model "<model>" --resume "<session_id>" \
  --output-format stream-json --verbose --permission-mode bypassPermissions \
  --disallowedTools Edit Write NotebookEdit < board/<rid>.prompt.txt > reviews/<rid>.p2.stream.jsonl 2> reviews/<rid>.p2.err
```

stdout is written to the file as it streams, so a killed process leaves every line already emitted (`REQ:626`). After exit, `reviews/<rid>.p2.md` = `jq -rs '[.[]|select(.type=="result")|.result][0] // ""'`; model check and tokens use the `RR:51-53` filters on `jq -s` input (S3 verifies the filters match).

### 7.3 Resume failure and fresh fallback (R-14)

Resume has failed when, within the first 10 s or at exit, the stream holds no `assistant` event and the process exited non-zero, or the result object has `is_error: true`, or the stream has no `system` init event carrying the same `session_id`. Then:

1. Log `resume_fallback` with the detection time.
2. Recompute n with `start_cost = 16` at `t_launch = now` and re-render the digest (6.5). n = 0 → no launch (`reason: deadline_after_fallback`).
3. Copy `<rid>.p1.md` to `SB/<pkg>/p1/<run_id>/<rid>.p1.md` (mode 0444) and run the same command without `--resume`, with the prompt from `config/fallback-frame.txt` (3.6). Output goes to the same file names with suffix `.fallback`.

### 7.4 Phase-2 re-ask (R-02)

After phase 2 exits normally, extract its lines (8.1). If any extracted line fails the parser after normalisation and `now + 6 + turn_p90(model) < P2_DEADLINE`, resume the phase-2 session once with `reask-frame.txt`, using the 7.2 command with `--resume <phase-2 session_id>` and `timeout --kill-after=3 <P2_DEADLINE - now>` (output `reviews/<rid>.p2reask.*`). Otherwise the invalid lines are dropped with a warning and phase 1 stands.

### 7.5 Accounting

`reviews/<rid>.p2.meta.json`: `mode` (resume or fresh), `t_launch`, `t_end`, `phase2_s`, `n_planned`, `n_launched`, `model_ok`, `observed_model`, `output_tokens_main`, `output_tokens_all`, `phase2_timeout`, `resume_fallback`, `p2reask_s`, `session_id` (the fresh fallback has its own id). The phase-2 session transcript is copied to `reviews/<rid>.p2.session.jsonl` (located by `find ~/.claude/projects -maxdepth 2 -name '<session_id>.jsonl'`). A phase-2 session whose `model_ok` is false contributes no lines (logged `p2_model_mismatch`), because `REQ` 4 requires `model_ok` on every session, phase 2 included.

## 8. Combiner and merge

### 8.1 Phase-2 line extraction and salvage (`findings_io.extract_p2_lines`)

Input: the phase-2 stream file (and the re-ask stream, if any). Steps:

1. If the stream has a `result` event, take the lines of the last findings-v1 block in its result text.
2. Otherwise (killed, `phase2_timeout`), salvage: concatenate the `text` content blocks of every `assistant` event in stream order and take every line that is, after stripping, a complete JSON object.
3. Keep only objects whose `id` matches `^C[0-9]+$`. When an id appears more than once, the last complete occurrence wins.
4. Normalise (5.4 step 2) and validate each line alone by running `parse_block` on `"## Findings block\n```findings-v1\n" + line + "\n```\n"`. Valid lines are kept; invalid ones are counted in `p2_lines_dropped` with the parser message. A partial last line never parses, so it is dropped (`REQ:695`).
5. A re-ask's valid lines replace the earlier ones id by id.
6. Drop a phase-2 line whose flattened anchor and flattened claim both equal a phase-1 line (`p2_dupe_dropped`).

`p2_lines_salvaged` = valid lines taken by step 2.

### 8.2 Combiner (`findings_io.combine`, R-10, R-16)

`combine(p1_text, p2_lines) -> (report_text, log)`:

1. Parse `p1_text`; take its valid findings (5.4 normalised). Add `"origin":"own"` to each; every other key and value is unchanged.
2. Rename phase-2 lines in C-number order to `P2-F1`, `P2-F2`, ...; if a phase-1 id already equals one of these, use `P2X-F<n>` (logged). Add `"origin":"peer"`.
3. Replace the findings section of `p1_text`: everything from the `## Findings block` heading to the end of the last findings-v1 block is replaced by the heading and one block holding the phase-1 lines, then the phase-2 lines. The text before the heading and the verdict line after the block are kept from phase 1, so the verdict line stays the reviewer's sealed phase-1 verdict.
4. Self-check: `parse_block(result)` returns `ok`, exactly one block, `len(findings) == len(p1) + len(p2)`, and each phase-1 finding with `origin` removed equals `normalise(sealed finding)` (the sealed `p1.md` is the raw report; the H2 truncation of 5.4 step 2 is applied the same way in both arms, so the comparison is against the normalised sealed line). A failure raises (`E_COMBINE`) and the package is invalid; it is never silently repaired.

With `PANEL_COLLAB=0` the same function runs with `p2_lines = []`.

`reviews/<rid>.combine.json`: `p1_lines`, `p2_lines_valid`, `p2_lines_dropped`, `p2_lines_salvaged`, `p2_dupe_dropped`, `p2_self_reference` (phase-2 claims matching `(?i)\b(second pass|places?|challenge|move M?\d+|peer)\b`, counted, not changed), `challenges_answered` (launched slots answered by a valid C-line or a `no finding C<k>` line; F1's measured act rate, R-47).

### 8.3 Merge (R-04)

Unchanged merge contract, same arguments as `merge-b11.sh:34`:

```
uv run --project "$REPO" superclaude review merge --ledger merged/ledger.json --doc EVAL/<pkg>/candidate.md \
  --round 1 --report <rid>=<abs>/reviews/<rid>.md ... --resolution merged/resolution.json --out merged/merged-1.md
```

Report paths are passed as absolute paths, because `render_merged_report` prints each one verbatim (`- <rid>: report <path>`, `ledger.py:421-423`, from the `--report` value, `merge_cmd.py:86-95`); the anonymiser then redacts them (10.1 step 3).

`--doc` is the original `EVAL/<pkg>/candidate.md`, byte-equal to the sandbox copy (checked). A refusal (`LedgerError`, no valid block) makes the package invalid. The merge uses the same `findings.py` the harness validated with, because both run from `REPO` through UV; their sha256 values are pinned.

The sealed merge (collab only) runs the same command on `merged-sealed/` with `--report <rid>=<abs>/reviews/<rid>.p1norm.md`, where `p1norm.md` = `combine(p1_text, [])`.

## 9. Metrics, alarms and audits

### 9.1 `collab.json` (R-23), one per package, both arms

Written by `cli.py metrics --pkgdir D`. Every R-23 field is present; fields that only mid-run designs produce are `null` in F1 and listed as such so the schema check is uniform across redesigns.

| Field group | F1 value |
|---|---|
| `arm` | `A3` (collab 1) or `A1` (collab 0); plus `panel`, `run_id`, `pkg`, `values_sha256`, `values_status` |
| per reviewer (`reviewers.<rid>`) | `msgs_sent` 0; `msgs_received` 1 if a digest was launched else 0; `seal_t` (p1 seal time minus T0); `resume_fallback`; `phase2_s`; `reask_s` (phase 1) and `p2reask_s`; `attempts`; `retry_s`; `retry_isolated`; `phase2_timeout`; `p2_lines_salvaged`; `n_planned`; `n_launched`; `hang_kill`; `no_launch_reason`; `output_tokens_all` (all sessions) |
| per reviewer, mid-run only | `first_delivery_t`, `stop_blocks`, `hook_calls`, `hook_error`, `hook_ms_p95`, `snapshot_missing`, `late`, `over_cap`, `finish_signal_t`: `null` |
| per slot (`slots[]`) | `rid`, `j`, `slot_type`, `move`, `source_rid`, `source_finding_id` (real only), `deal_r`; `card_form`, `deal_c`: `null` |
| panel | `T0`, `elapsed_s` (latest end of any process of the package minus T0, every attempt and re-ask included), `baseline_elapsed_s` (B_f), `overhead_pct`, `k`, `panel_finish_at`, `finish_would_fire` (a critical-role reviewer's phase 1 still running at PANEL_FINISH_AT; logged in both arms, acted on in neither), `slo_breach`, `own_line_jaccard`, `pairwise_task_jaccard` (descriptive), `echo_rate` (or `"n/a"`), `ledger_rows`, `challenges_real`, `challenges_gap`, `gt_anchor_overlap` (filled later by `result`, A2) |

### 9.2 Own-line Jaccard and ledger rows (R-25)

- Task of a finding: the nearest heading at or above the first line of `locate(candidate, anchor)` that matches `^#{1,6}\s+Task\s+(\d+)\b` gives `T<n>`; findings with no such heading are left out. (All three candidates use `## Task <n>:` headings; checked: designSpec 13, alias 9, control 12 such headings.)
- `own_line_jaccard`: for each reviewer, the Task set of its `origin:"own"` lines; mean Jaccard over the 3 reviewer pairs, skipping a pair where both sets are empty; `null` if every pair is skipped.
- `pairwise_task_jaccard`: the same over all lines (descriptive only).
- `ledger_rows`: `len(rows)` of `merged/ledger.json`.

### 9.3 ECHO (`REQ:652`)

A phase-2 finding belongs to slot j of its reviewer when its flattened anchor and the slot anchor share a common substring of at least 12 characters. For real slots only: echo when the token Jaccard (lower-case words of 3+ letters) between the phase-2 claim and the source peer finding's claim is above 0.6. `echo_rate` = echoes / phase-2 findings mapped to real slots; `"n/a"` when that count is 0.

### 9.4 Audit (`cli.py audit --pkgdir D`, R-09, `REQ` 4 rule 5)

| Check | Violation when |
|---|---|
| Sandbox untouched | `git -C SB/<pkg>/repo status --porcelain` is not empty (the R-09 check: a tracked file changed or an untracked, non-ignored file appeared). Gitignored paths created during the run (for example `.venv/` from a reviewer's `uv run`, `__pycache__/`, `.pytest_cache/`, `.codegraph/`) are not a violation: `git status --porcelain --ignored --untracked-files=all` output is logged as `ignored_writes` (descriptive), and cleanup removes them after the last run on the sandbox (13.5), so they never carry into the next run |
| Candidate untouched | sha256 of `SB/cand/<pkg>/candidate.md` or `EVAL/<pkg>/candidate.md` differs from `pkg.json` |
| Forbidden reads | any `tool_use` input in any session transcript, stream or `attempt*.json` of the package (every attempt, re-ask, phase 2, fallback and subagent session, 9.5) contains `ground-truth`, `/eval-workspaces/`, `.dev/reflect`, `20261113-collab`, `merged-requirements`, `/brainstorms/`, `/.claude/projects/` (session transcripts of peers and of other sessions on the host, some of which quote ground truth), or a `SB/<pkg>/p1/` path other than the reviewer's own copy |
| No free text | any `board/*.digest.jsonl` line fails `validate_line` |
| Model identity | any session (attempt, re-ask, phase 2, fallback) used for the report with `model_ok` false |

Descriptive, not a violation: `source_read` per reviewer (a tool call naming `SB/cand/<pkg>/source.md`), the R-01 check reported per model.

Any violation: `audit.json` `violations` lists it, a `QUARANTINE` file with the reasons is written in the package directory (quarantine in place, nothing deleted, R-26), and the results row carries `contaminated: true`. The ground-truth text check of digests runs in `cli.py result` after judging (10.4), so no step before judging opens ground truth (K4).

### 9.5 Transcript capture for the audit

Persistence is on, so every session (each phase-1 attempt, each re-ask, phase 2 and the fresh fallback) leaves files under `~/.claude/projects/<cwd slug>/`. Before the audit, `package.sh` copies every file in that slug directory whose path contains one of the package's session ids (the main `<id>.jsonl` and any subagent files under a directory named after the id) into `reviews/sessions/<id>/`, keeping relative paths. Session ids are taken from every `attempt*.json`, `reask.stream.jsonl`, `p2*.stream.jsonl` and their `meta.json` (`session_id` is a field of every `meta.json`, `p2.meta.json` and of the `collab.json` reviewer entries, R-46). A killed `--output-format json` attempt writes no stdout, so its session id is recovered from the slug directory instead: any `.jsonl` there whose first entry's timestamp lies between the attempt's `t_start` and `t_end` and whose first user message equals the rendered brief. The audit reads all captured files plus every stream and `attempt*.json`. Cleanup (13.5) runs only after this copy.

### 9.6 `r3lib/metrics.py` functions

`task_of(candidate, anchor)`, `own_line_jaccard(findings_by_rid, candidate)`, `echo_rate(p2_by_rid, slots, sources)`, `collab_json(pkgdir, values)`, `audit(pkgdir)`, `anonymise(merged_text) -> (text, report)`, `result_row(rundir)`, `summarize(rows, panel)`. Signatures and outputs as in 9.1-9.4 and 10.

## 10. Anonymise, judge and results row

### 10.1 Anonymiser (`cli.py anon --in merged-1.md --out merged-anon.md`)

This design's own Python port of `anon-b11.sh:17-25`, extended for R-10, R-29 and A8. Applied identically to both arms and to sealed reports:

1. Reviewer ids `\bt[0-9a-z]+-[0-9]+\b` → `R1..Rn` in sorted order (as `anon-b11.sh:17-23`).
2. Finding ids in `#### <lid>.<Rk> (<id>)` headings → `(f1)`, `(f2)`, ... in order of appearance; any remaining `\bP2X?-F\d+\b` → the same mapping.
3. `candidate: <path> sha256` → `candidate: <candidate file> sha256`; every `report <path>` token (absolute or relative) → `report <redacted>`; any `/tmp/evalsb-collab-r3[^\s,)]*` → `<sandbox>`.
4. Remove `"origin":"own"` and `"origin":"peer"` (with a leading comma) wherever they appear.
5. Fail (exit 6, nothing written) if the output still contains `P2-`, `"origin"`, `evalsb-collab`, `20261113-collab`, `/board/`, `digest.jsonl`, `p1norm`, `/runs/`, `/reviews/` or a match of `-c[01]-`.

### 10.2 Judge (`judge-one.sh`, byte-unchanged, R-29)

- Preflight: sha256 of `EVAL/tools/tmp-scripts/judge-one.sh` equals `pins.json`; otherwise `E_JUDGE_CHANGED`.
- Per package and per kind (`full`; plus `sealed` when collab 1): `row = "s" + 10 random hex`, `L` = a random upper-case letter; create `R3/scoring/<row>/<pkg>/<L>/merged-anon.md`. The mapping (row, L) → (run_id, pkg, kind) goes only to `runs/<run_id>/scoring-keys.json`.
- `C = $(realpath --relative-to="$EVAL/arms/scoring/combos" "R3/scoring/<row>")`, which is `../../../../20261113-collab/r3-axis-flip-challenge/scoring/<row>` for the default root. Then `bash "$EVAL/tools/tmp-scripts/judge-one.sh" "$C" "<pkg>" "<L>"`. The script's `D="$EVAL/arms/scoring/combos/$C/$P/$L"` resolves to `R3/scoring/<row>/<pkg>/<L>`; it reads `EVAL/<pkg>/ground-truth.json` and `EVAL/<pkg>/candidate.md` and writes `score.json`, `judge.json`, `judge.err` there. The launcher asserts `realpath "$EVAL/arms/scoring/combos/$C" == realpath R3/scoring/<row>` before the call.
- At most 4 judges at once (`run-combo-judges.sh:40` used `-P 4`). A judge that prints `FAIL` or leaves no valid `score.json` is retried once; because the script skips whenever `score.json` exists (`judge-one.sh:7`), an invalid `score.json` (and its `judge.json`, `judge.err`) is first moved aside to `attempt1/` in the same directory. Per-batch API-error audit: `judge_ok` is true only when `score.json` parses, has the schema keys of `judge-one.sh:21`, and `judge.json` has no `is_error: true` and no `API Error` text.
- The judge's `combo` field will hold the relative path; nothing reads it.

### 10.3 Ground-truth issue map (labels of `REQ:22`)

| Label | Package | GT id | Target issue for reach (`REQ:955`) |
|---|---|---|---|
| B1-B5 | designSpec | GT1-GT5 | B1, B2, B5 |
| I1-I5 | designSpec | GT6-GT10 | I1, I4, I5 |
| B6-B8 | alias | GT1-GT3 | B6, B8 |
| I6 | alias | GT4 | I6 |
| I7, I8 | control | GT1, GT2 | I7 |

### 10.4 Results row (`cli.py result --rundir R`)

Reads `scoring-keys.json`, each `score.json`, each `collab.json`, each `<rid>.cost.json` and `p2.meta.json`, and, after judging only, `EVAL/<pkg>/ground-truth.json` (ids, `blocking_in_implement`, and `plan_quote` for `gt_text_leak` and `gt_anchor_overlap`). Writes `runs/<run_id>/result.json` and appends the same object as one line to `results/results.jsonl` (smoke runs: `results/smoke.jsonl`; Spike-4 runs: `spikes/spike4/rows.jsonl`) under `flock` on a `.lock` file in the same directory.

```json
{"schema":"r3-result/1","run_id":"..","panel":"el2","collab":1,"arm":"A3","values_sha256":"..","values_status":"frozen","smoke":false,"tag":"..",
 "found14":2,"real_blocking8":0,"judge_blocking":1,"wrong_blockers":2,"control_found2":1,"control_wrong_blockers":0,
 "reach":true,"target_hits":["I7"],
 "output_tokens":{"total":71234,"by_pkg":{"<pkg>":..},"phase2":7120,"reask":800},
 "elapsed_s":{"<pkg>":141.2,...},"overhead_pct":{"<pkg>":0.217,...},"slo_breach":{"<pkg>":false,...},
 "sealed":{"found14":1,"real_blocking8":0,"judge_blocking":1,"wrong_blockers":2,"control_found2":1,"control_wrong_blockers":0,"reach":true},
 "collab":{"challenges_real":5,"challenges_gap":2,"n_planned":7,"n_launched":7,"resume_fallback":0,"phase2_timeout":0,
           "p2_lines_valid":4,"p2_lines_salvaged":0,"p2_lines_dropped":0,"p2_dupe_dropped":0,"p2_self_reference":0,
           "retry_isolated":0,"hang_kill":0,"reask_count":1,"echo_rate":{"<pkg>":0.0},"own_line_jaccard":{"<pkg>":0.21},
           "ledger_rows":{"<pkg>":9},"finish_would_fire":{"<pkg>":false},"gt_anchor_overlap":3,"gt_text_leak":0},
 "judge_ok":true,"invalid_pkgs":[],"contaminated":false}
```

Definitions (as `HANDOFF-review-panel-unification.md:69` and `COMBO-REPORT.md:291`):

- `found14` = |`gt_covered_any`| on designSpec + alias.
- `real_blocking8` = |`gt_covered_blocking` ∩ {GT items with `blocking_in_implement: true`}| on designSpec + alias (5 + 3 = 8 such items).
- `judge_blocking` = |`gt_covered_blocking`| on designSpec + alias.
- `wrong_blockers` = sum of `wrong_blockers` on designSpec + alias; `control_found2` and `control_wrong_blockers` from the control package.
- `output_tokens.total` = `output_tokens_all` summed over every session of every reviewer of every package (all attempts, re-asks, phase 2, fallback).
- `elapsed_s` per package = `collab.json` `elapsed_s`.
- `reach` = any target issue of 10.3 covered at any severity.
- `gt_text_leak` = count of digest lines whose bytes, with the `anchor` value removed, contain a ground-truth `plan_quote` substring of 12+ characters (must be 0; non-zero sets `contaminated`). `gt_anchor_overlap` = count of digest anchors containing such a substring (descriptive, A2).
- With collab 0, `sealed` and `collab` hold zeros and `null` echo values.

### 10.5 Arm summary (`cli.py summarize --panel P [--results F]`)

Reads `results/results.jsonl` only (smoke and Spike-4 rows live elsewhere) and refuses any row whose `values_status` is not `frozen`. Groups rows by panel and arm (A1 = collab 0, A3 = collab 1). It always prints, per arm, the counts of rows with `slo_breach`, invalid packages, `judge_ok: false` and `contaminated: true`; contaminated rows count as audit violations for decision rule 5 (`REQ:970`), and `SLO_BREACH` packages stay in the time verdict. Quality means use only rows with every package valid, judged and uncontaminated. It prints JSON plus a markdown table: per arm means and ranges of the results-row metrics; per package median elapsed (B_c for A1); the R-24 cap check (median at most 1.35 B_c; packages over 1.35 B_c at most 1 per 12; none over 1.5 B_c); `baseline_drift = B_c / B_f` with the [0.963, 1.10] band; CONVERGENCE count (A3 runs whose `own_line_jaccard` exceeds the A1 mean by more than 0.15, or whose `ledger_rows` is more than 20% below the A1 mean); ECHO count (packages with `echo_rate` above 0.30); reach counts and the one-sided Fisher exact p of A3 against A1 (hypergeometric tail, `math.comb`). It reports what the decision rule needs; it does not decide adoption.

## 11. The three panels

`REQ` designs F1 for EL2 only (ember + 2x luna). The other two panels lack ember. The role that ember plays is "searcher": the reviewer that receives search moves on the lunas' anchors and whose anchors are dealt to the lunas. On SL2 and HL2 the strong model takes that role, because both search outward far more than luna (`REQ:93-94`, `:99`: sonnet touches an unnamed test file in 35% of runs; haiku searches `tests/` in 81%). Every other rule is unchanged.

### 11.1 Role table

| Panel (`panels.json` key) | Searcher: receives search flips (cap 3); its anchors are dealt to the readers | Readers: receive reading flips (cap 2) | Source peers | Critical role (sets B) | `box_cap_s` | Adaptation |
|---|---|---|---|---|---|---|
| `el2` ember + 2x luna | ember `muse-ember-1.0`, id `t2b-1` | luna `gpt-6-luna`, ids `t4-1`, `t3-1` | lunas ← ember; ember ← both lunas | the slower luna | 35 | none: exactly `REQ` Redesign 3 |
| `sl2` sonnet + 2x luna | sonnet `claude-sonnet-5-5`, id `t1b-1` | luna, `t4-1`, `t3-1` | lunas ← sonnet; sonnet ← both lunas | sonnet | none | sonnet replaces ember; lunas wait for sonnet's seal (A3); no 35 s box cap (A4) |
| `hl2` haiku + 2x luna | haiku `claude-haiku-5-5`, id `t2-1` | luna, `t4-1`, `t3-1` | lunas ← haiku; haiku ← both lunas | haiku | none | haiku replaces ember; same waiting and box rules as `sl2`; this is not `REQ`'s HL2 shadow variant (1.4) |

### 11.2 Planning timelines (replaced by the values file)

**EL2** (planning B = 116 s; turn_p90 luna 6.4 s, ember 3.2 s; `REQ:632-639`):

| Reviewer | Phase-1 end | Phase-2 launch, box, n | Planned end |
|---|---|---|---|
| luna A | 95 s | 95 s, box 35, n = 2 | 126.6 s |
| luna B | 116 s | 116 s, box 34.8, n = 2 | 147.6 s (+27.2%) |
| ember | 41 s, waits | 116 s, box 34.8, n = 3 | 141.2 s |
| Enforced | phase-2 kill 150.8 s (+30.0%); phase-1 hang guard 174 s | | |

**SL2** (planning B = 273.7 s, three-package mean `REQ:278`; sonnet turn 14 s, luna 6.4 s):

| Reviewer | Phase-1 end | Phase-2 launch, box, n | Planned end |
|---|---|---|---|
| luna A, luna B | about 100-120 s, then wait for sonnet | 273.7 s, box 82.1, n = min(2, 5) = 2 | 305.3 s (+11.5%) |
| sonnet | 273.7 s | 273.7 s, box 82.1, n = min(3, floor(76.1/28)) = 2 | 335.7 s (+22.7%) |
| Enforced | phase-2 kill 355.8 s (+30.0%); phase-1 hang guard 410.6 s | | |

Sonnet gets n = 2 only while its turn_p90 is at most 19.0 s, and n = 1 up to 38.0 s.

**HL2** (planning B = 238 s, `REQ:277`; haiku turn 23 s, luna 6.4 s):

| Reviewer | Phase-1 end | Phase-2 launch, box, n | Planned end |
|---|---|---|---|
| luna A, luna B | about 100-120 s, then wait for haiku | 238 s, box 71.4, n = 2 | 269.6 s (+13.3%) |
| haiku | 238 s | 238 s, box 71.4, n = min(3, floor(65.4/46)) = 1 | 290 s (+21.8%) |
| Enforced | phase-2 kill 309.4 s (+30.0%); phase-1 hang guard 357 s | | |

Haiku gets n = 1 only while its turn_p90 is at most 32.7 s; above that it gets no phase 2 and only the lunas do.

### 11.3 What the adaptation changes

- On SL2 and HL2 the lunas sit idle (no tokens, no process) from their phase-1 end to the strong reviewer's seal. Elapsed is still bounded by the same kill at T0 + 1.30 B_f.
- On SL2 and HL2 the lunas' challenges come from a stronger model's anchors. `REQ` gives no gain estimate for these panels; the measured arm is the estimate. The decision table of `REQ` 4 is written for EL2 (stage 1) and SL2 is screened differently (`REQ:976`, hard-issue credits per run, because SL2's reach is near saturated). `summarize` reports both reach and hard-issue credits per run so either rule can be applied.
- Model identity, read-only rules and every guard are the same on all three panels.

## 12. The PANEL_COLLAB=0 baseline switch

`PANEL_COLLAB` is read once by `bin/launch-panel.sh` (default `1`; any value other than `0` or `1` stops with `E_BAD_SWITCH`) and written to `run.json`; every other script reads it from `run.json`, never from the environment.

| Behaviour | `PANEL_COLLAB=1` (A3) | `PANEL_COLLAB=0` (A1) |
|---|---|---|
| Sandbox, candidate, source.md, brief (H1, H3, H4) | same | same |
| Phase-1 command, attempts, model check, `NOFALLBACK=1` | same | same |
| `--no-session-persistence` removed | yes | yes (a re-ask resumes) |
| H2 normalise, re-ask, seal as `p1.md` | same | same |
| Hang guard T0 + 1.5 B_f, `hang_kill`, `SLO_BREACH` | same | same |
| Scheduler, digest, phase 2, phase-2 deadline | yes | none: the scheduler is skipped |
| Combiner | phase-1 + phase-2 lines | phase-1 lines only, `origin:"own"` |
| Merge, anonymiser, judge, results row | full + sealed | full only |
| `collab.json` | all fields | same fields; collaboration counters 0, `echo_rate` `"n/a"`, `finish_would_fire` computed |

The R-05 check (`test_command_diff`, 15.2) proves the A1 phase-1 command differs from `RR:48` only by the allowed items. A1 and A3 therefore differ only by the exchange, which is what the collaboration share C needs (`REQ:338`).

## 13. Launch script

### 13.1 Usage

```
NOFALLBACK=1 PANEL_COLLAB=1 bash R3/bin/launch-panel.sh el2              # one A3 run, three packages
NOFALLBACK=1 PANEL_COLLAB=0 bash R3/bin/launch-panel.sh sl2 --tag a1-b3  # one A1 run on sonnet + 2x luna
R3_SMOKE=1 PANEL_COLLAB=1 bash R3/bin/launch-panel.sh hl2 --pkgs TASK-WF-design-20261108-041415
```

Arguments: `<panel>` is `el2`, `sl2` or `hl2`. `--pkgs` limits packages (default all three). `--tag` is free text stored in `run.json` and the row. `--no-judge` stops after the merges (used by Spike 4 runs, which need no scores). `R3_SMOKE=1` allows planning values and writes the row to `results/smoke.jsonl`. `R3_SPIKE4=1` (only with `PANEL_COLLAB=0`) uses the legacy 3000 s timeout and implies `--no-judge`. The launcher exports `NOFALLBACK=1` itself and refuses a caller value other than `1`.

Exit codes: 0 every package valid and judged; 1 preflight refused; 2 at least one package invalid or not judged (the row is still written with `invalid_pkgs` / `judge_ok: false`); 3 audit violation (row has `contaminated: true`).

### 13.2 Steps

1. **Preflight** (any failure → exit 1, nothing launched): `jq`, `timeout`, `flock`, `realpath`, `claude`, `uv` on `PATH`; `NOFALLBACK=1`; `PANEL_COLLAB` in {0, 1}; panel known; every model in the panel passes `r3_assert_model`; `config/pins.json` hashes match (judge script, parser, ledger, merge command, config files); values file: unless `R3_SMOKE=1` or `R3_SPIKE4=1`, `values/<panel>.json` must exist, have `status: frozen`, and match `values/<panel>.json.sha256`, in both modes (the A1 baseline carries the same hang guard as A3); `R3_SPIKE4=1` with `PANEL_COLLAB=1` is refused; `uv run --project "$REPO" superclaude review merge --help` exits 0; `bin/build-sandbox.sh <pkg>` exits 0 for each package.
2. `run_id = <panel>-c<collab>-<UTC stamp>-<4 hex>`; create `runs/<run_id>/`; write `run.json`.
3. Run `lib/package.sh runs/<run_id> <pkg>` for every package, all three in parallel (9 reviewer sessions). Admission (13.3) happens inside `package.sh` before T0.
4. Wait for all packages.
5. Unless `--no-judge`: for every package with a `merged-1.md`, anonymise (10.1) and judge (10.2); with collab 1 also the sealed report. Judges run at most 4 at once.
6. `cli.py result --rundir runs/<run_id>` (10.4).
7. Print one line: `run_id`, found14, real_blocking8, control_found2, total tokens, elapsed per package, exit status.
8. `bin/cleanup-sessions.sh runs/<run_id>` (13.5).

### 13.3 Admission control (R-28 caps)

Before T0, `package.sh` takes `flock SB/admit.lock`, then counts running model sessions by their `timeout` parents, whose command line is stable: `pgrep -fc '^timeout .* claude -p --model '` (total) and `pgrep -fc '^timeout .* claude -p --model muse-ember-1.0 '` (ember). The `claude` processes themselves cannot be matched by `^claude`: on this host `/usr/local/bin/claude` is a wrapper that execs `/opt/nvm/versions/node/v24.22.2/bin/claude` or `ccsession-orca` (`/usr/local/bin/claude:3-10`), so their command lines start with another path. Every session this harness, `RR:48` and `judge-one.sh:25` start runs under `timeout`; a session another tool starts without `timeout` is not counted (Q6). It proceeds when `total + 3 <= 10` and `ember + (ember reviewers in this panel) <= 4`; otherwise it releases the lock, sleeps 5 s and retries. After launching its three phase-1 processes it waits until `pgrep` sees them (at most 5 s) and releases the lock. Phase-2 and re-ask processes replace a finished phase-1 process of the same reviewer, so admission per package covers them. The lock lives under `SB`, so it serialises only this design's launches (risk Q6).

### 13.4 Repeated runs

One launch is one run. An arm of 12 runs is 12 launches, interleaved with the A1 launches in block-randomised order by whoever drives the experiment, for example:

```
for b in $(seq 1 12); do for arm in $(printf '0\n1\n' | shuf); do
  PANEL_COLLAB=$arm NOFALLBACK=1 bash R3/bin/launch-panel.sh el2 --tag block-$b; done; done
```

### 13.5 Session cleanup (`bin/cleanup-sessions.sh`, R-46)

1. Collect this run's session ids (9.5: every attempt, re-ask, phase-2 and fallback session); append the paths of the files 9.5 copied for them (the `<id>.jsonl` files and any subagent files under `<id>/`) to `SB/<pkg>/pending-cleanup.txt` under `flock`.
2. If `SB/<pkg>/active/` is empty (no run uses that sandbox), delete exactly the files listed in `pending-cleanup.txt` (`rm -f -- <path>`, each path checked to end in `/<uuid>.jsonl` under `~/.claude/projects/`), then truncate the list. Never delete a directory.
3. In the same branch (no active run): `git -C SB/<pkg>/repo clean -fdX -q` (removes gitignored files only, such as `.venv/` and caches; tracked files and the snapshot are untouched), then check that `git -C SB/<pkg>/repo status --porcelain --ignored --untracked-files=all` is empty and log the result to `runs/<run_id>/cleanup.json`. A non-empty result here means a non-ignored write that the 9.4 audit already flagged.

Transcripts were already copied into the run directory (5.4, 7.5), so cleanup loses no audit data.

## 14. Values file (Spike 4)

### 14.1 File `values/<panel>.json`

```json
{"schema":"r3-values/1","panel":"el2","status":"frozen","source_runs":["el2-c0-..",".."],"frozen_at":"..",
 "turn_p90":{"muse-ember-1.0":3.4,"gpt-6-luna":6.9},
 "packages":{"TASK-WF-designSpec-20261107-075614":{"B_f":104.0,"T_report_p90":7.1,"k":1,"panel_finish_offset_s":126.4},
             "TASK-WF-makeTheAliasOnly-20261105-051649":{...},"TASK-WF-design-20261108-041415":{...}},
 "slowdown_s":null}
```

`values/<panel>.json.sha256` holds its sha256. A missing file means `status: planning` with B from `packages.json`, turn_p90 = the `REQ:265-268` medians (ember 3.2, luna 6.4, haiku 23, sonnet 14) and T_report_p90 = the critical model's turn.

### 14.2 Measurement (`cli.py values-freeze --panel P --runs <run_id>...`)

Input: at least 3 Spike-4 runs (`PANEL_COLLAB=0 R3_SPIKE4=1`) of that panel; it refuses fewer, or any run with an invalid package.

- `B_f[pkg]` = median over the runs of `collab.json` `elapsed_s` (B_A1 frozen, `REQ:63`).
- Turn durations, from the copied session transcripts (`*.p1.session.jsonl`): for each assistant entry, its `timestamp` minus the `timestamp` of the entry just before it (the user prompt or the last tool result). `turn_p90[model]` = 90th percentile over all turns of that model in all source runs.
- `T_report_p90[pkg]` = 90th percentile of the last assistant entry's duration of the critical-role reviewer, per package.
- `k = max(0, min(2, floor((0.35*B_f - 2 - turn_p90 - T_report_p90) / (2*turn_p90))))` with the critical role's turn_p90 (R-42); `panel_finish_offset_s = 1.35*B_f - turn_p90 - T_report_p90` (R-41). F1 uses neither for control; both are logged in `collab.json` for cross-design comparison and `finish_would_fire`.
- Writes the file with `status: frozen`, then the `.sha256`. It refuses to overwrite a frozen file (R-30: never recomputed during an arm); a new freeze needs the old file moved aside by a person.

### 14.3 Functions (`r3lib/values.py`)

`compute_n(T0, B_f, t_launch, box_cap, cap, start_cost, turn_p90)` (6.5), `compute_k(B, turn_p90, T_report_p90, hooks=2.0)`, `finish_at(T0, B, turn_p90, T_report_p90)`, `turn_durations(session_jsonl)`, `p90(xs)` (nearest-rank), `freeze(panel, run_dirs)`, `load(panel, smoke)`.

`slowdown_s` (R-45) stays `null`: F1's phase-1 brief is the A1 brief, so its slowdown over A1 is 0 by construction; only the phase-2 time counts against the design, and the kill bounds it.

## 15. Test plan

All tests are pytest (bats is not installed on the host; shell scripts are tested through `subprocess`). Command: `uv run --project "$REPO" pytest -p no:cacheprovider "$R3/tests" -q`. Tests never call a real model: `conftest.py` puts `tests/fakes/` first on `PATH` and points every root override (2.2) at a pytest temp directory under `/tmp`. Tests may read `EVAL` files (candidates, `ground-truth.json` for the integrity tests, `RR` for the R-05 diff) and never write there.

### 15.1 Fake `claude` (`tests/fakes/fake_claude.py`)

`FAKE_CLAUDE_PLAN` names a JSON file: a list of rules `{"match":{"model":..,"resume":true|false,"prompt_contains":..,"nth":..},"action":{...}}`; the first matching rule whose `times` is not exhausted is used (counters kept in a file next to the plan, under `flock`). Actions:

| Action key | Effect |
|---|---|
| `report` | path of a fixture report returned as `result` |
| `observed_model` | model written into `assistant` events (default: the requested model) |
| `sleep_s` | sleep before output (hang and deadline tests) |
| `stream_lines` | for stream-json: list of assistant text chunks emitted one event at a time, `flush` after each, with `chunk_delay_s` between |
| `exit` | exit code; `result_is_error: true` gives a result event with `is_error` |
| `no_result` | emit no result event |
| `session_id` | id put in `system` and `result` events (default: a new uuid4); with `--resume <id>` an unknown id gives exit 1 and no events (resume failure) |
| `write_file` | path the fake writes (sandbox-write audit test) |
| `judge_score` | for a prompt containing `blind scoring judge`: parse `Write JSON to <path>` from the prompt and write the given score object there |

Output shapes follow the real CLI: `--output-format json` prints one JSON array of events (`system`, `assistant` with `message.model` and text content, `result` with `result`, `session_id`, `usage.output_tokens`, `modelUsage`); `stream-json` prints the same events one per line. The fake also appends each transcript line, with an ISO `timestamp`, to `$R3_CLAUDE_PROJECTS/<slug>/<session_id>.jsonl`. The harness locates and cleans transcripts under `R3_CLAUDE_PROJECTS` (default `~/.claude/projects`); `conftest.py` points it at a temp directory, so cleanup and Spike-4 parsing are tested on the same layout without changing `HOME` (which would also move the UV cache).

### 15.2 Unit tests (one file per component)

| Test file | Component | Cases (each is one assertion set; all must pass) |
|---|---|---|
| `test_config.py` | catalogue, routing, pins (R-07) | catalogue ids are exactly M1-M10 and texts equal `REQ:184-193`; no catalogue text or frame text contains a ground-truth `plan_quote` substring of 12+ characters, nor a file path named in any ground-truth description (reads the 3 `ground-truth.json`); `cli.py pin --check` passes on the committed files and fails after one byte is changed in a temp copy |
| `test_phase1_brief.py` | brief (R-01, R-11) | rebuilding from `RR:13-17` differs only by the H1 sentence; the rendered brief names the absolute source.md path |
| `test_command_diff.py` | launch commands (R-05) | `reviewer.sh print-cmd ... phase1` tokens against `RR:48` differ only in: cwd, brief, the `timeout` arguments (`--kill-after=5 <T>` in place of `3000`), missing `--no-session-persistence`; nothing else added or removed. For each of `reask`, `phase2`, `fallback`, `p2reask`: the command has `--model <same model>`, `--permission-mode bypassPermissions`, `--disallowedTools Edit Write NotebookEdit`, `--output-format stream-json --verbose`, no `--no-session-persistence`, `--resume <id>` exactly for `reask`, `phase2`, `p2reask`, and a `timeout` whose limit is the matching deadline. The phase-1 command is identical in collab 0 and 1 |
| `test_model_allowlist.py` | guard (K2) | the five allowed ids pass; `Qwen3.8-max`, `glm-5.3`, `claude-opus-5-5`, `gpt-6.1-sol`, `""` are refused by `r3_assert_model` with exit 1; reviewer scripts refuse to start without `NOFALLBACK=1` |
| `test_h2.py` | normaliser (R-02) | a 250-character anchor becomes 200 and the line stays valid (not dropped); a 350-character claim becomes 300; a bad severity gives exit 3 with the parser message; a MINOR blocking line gives exit 3; a report without the heading gives exit 4; a report whose block is already valid is unchanged byte for byte |
| `test_select.py` | selection (R-12) | fixture block with 8 findings: 2 surface claims (artifact path, line number) excluded; `data-loss` and `other` categories excluded; an anchor not in the candidate excluded; result order equals block order |
| `test_router.py` | router (R-13) | 10 fixtures: quantifier → M3 reading / M2 search; command (`` `grep -c ...` ``) → M4 / M7; table row → M5 / M6; constraint → M8 / M8; `contradiction` category on a quantifier anchor → M8 (override); no class → None; a heading-only line → None |
| `test_deal.py` | deal (R-12) | 4 qualifying ember anchors with r = 0 → luna A gets 0 and 2, luna B gets 1 and 3; r = 1 swaps; the two sets are disjoint; the searcher queue interleaves A0, B0, A1, B1 |
| `test_gap.py` | gap cards (R-12) | over 1,000 seeded slot draws the gap share is within 0.333 ± 0.045 (3 standard errors); the same seed gives the same slots; a gap anchor never overlaps any phase-1 anchor span; with an empty real queue, real slots stay empty and gap slots still fill; the rendered prompt and JSON line for a gap slot have the same key set and layout as a real slot, and neither contains `gap`, `real`, `decoy` or a peer id |
| `test_n.py` | n (R-15) | EL2 planning values: luna launched at T0 + 116 → 2; turn_p90 7.3 → 1; fallback at T0 + 118 with start 16 → 1; launch at T0 + 132.0 → 1 and at T0 + 132.01 → 0; ember at T0 + 116, turn 3.2, cap 3 → 3; SL2 (B 273.7, no cap) sonnet at 273.7, turn 14 → 2, turn 20 → 1; HL2 haiku at 238, turn 23 → 1, turn 33 → 0 |
| `test_msg.py` | validator (R-06, R-08) | 6 bad lines rejected with their reasons: over 600 bytes, `claim` key, `category` key, unknown key `x`, `kind:"card"`, anchor not in candidate; 3 good challenge lines accepted; a line with `from == to` rejected; a digest over 1,800 characters loses its last slot |
| `test_combine.py` | combiner (R-10, R-16) | 3 phase-1 + 2 phase-2 lines → one block, 5 lines, ids F.. then P2-F1, P2-F2, origins own/peer; phase-1 lines minus `origin` equal the sealed ones; a phase-1 report with two findings-v1 blocks yields exactly one block (the last block's lines, as the parser uses); a phase-2 line repeating a phase-1 anchor and claim is dropped; a phase-1 id `P2-F1` forces `P2X-F1`; a phase-1 line with a 250-character anchor passes the self-check (compared with its normalised sealed form) and appears truncated to 200; `parse_block` of the output is `ok` |
| `test_salvage.py` | salvage (R-15) | a stream fixture with 2 complete C-lines and 1 partial line and no result event keeps 2 (`p2_lines_salvaged` 2); a repeated `C1` keeps the last; a non-C id is ignored; with a result event the result block wins |
| `test_metrics.py` | alarms (R-23, R-25) | `collab.json` has every R-23 key; a fixture where peer-tagged lines raise all-line Jaccard but not own-line Jaccard leaves `own_line_jaccard` unchanged; a fixture with copied claims gives `echo_rate` 1.0; no real slot gives `"n/a"`; `task_of` maps an anchor under `## Task 3:` to `T3` |
| `test_anon.py` | anonymiser (R-10, R-29) | fixture merged report with ids `t4-1`, `P2-F1`, `"origin":"peer"`, `/tmp/evalsb-collab-r3/...` paths → output has none of them; two reports from different arms with the same findings anonymise to identical text; a merged report built with relative `--report` paths (including `p1norm.md`) is fully redacted; a residue triggers exit 6 |
| `test_result.py` | results row | fixture `score.json` files → found14, real_blocking8 (only `blocking_in_implement` items), judge_blocking, wrong blockers and control fields match hand-computed values; `reach` is true for a control GT1 hit and false for a designSpec GT3-only hit; `gt_text_leak` counts a fixture digest whose non-anchor bytes hold a plan_quote substring |
| `test_values.py` | values (R-41, R-42) | k: B 116 with 6.4/6.4 → 2; T_report 11.0 → 1; B 100 → 1 at T_report 13.8 and 0 at 13.9; SL2 (B 273.7) turn 14 → k = 1 at T_report 51.7 and 0 at 51.9 (the exact edge is 51.795, which `REQ` rounds to 51.8); finish offset at planning values = 143.8; `turn_durations` on a fixture transcript; freeze refuses fewer than 3 runs and refuses to overwrite a frozen file |
| `test_judge_path.py` | judge path (A7) | for the default root and for a `/tmp` test root, `EVAL/arms/scoring/combos/<C>` resolves to the intended scoring row; `judge-one.sh` sha256 equals the pin |
| `test_summary.py` | arm summary (R-24, R-25) | cap check flags a package median over 1.35 B_c and a package over 1.5 B_c; CONVERGENCE counts runs over A1 mean + 0.15; Fisher p for A1 0/12 against A3 4/12 equals 495/10,626 within 1e-9 (`REQ:963`) |
| `test_guards.py` | write guard (K1), admission (13.3), switches | `r3_assert_writable` accepts paths under `R3`, `SB` and a `/tmp` override, and refuses `REPO/src`, `EVAL`, `R3/../r1-move-radar`, a symlink inside `R3` pointing to `EVAL`, and an override outside `/tmp`; admission with a stub `pgrep` (via `PATH`) reporting 7 total proceeds and 8 waits; on `el2` (one ember reviewer) 3 running ember proceeds and 4 waits; the lock is released in every branch; `PANEL_COLLAB=2` and `NOFALLBACK=0` are refused; `R3_SPIKE4=1` with `PANEL_COLLAB=1` is refused; a run without a frozen values file is refused unless `R3_SMOKE=1` or `R3_SPIKE4=1` |
| `test_sandbox.py` | H3, H4 (R-03) | on a throwaway git repo fixture: excluded directories absent; a masked path differing from the base fails the build; the built sandbox has one commit and a clean status |

### 15.3 Fault-injection tests (`test_faults.py`, one per failure mode; fake `claude`; test values B_f 40 s, turn_p90 1.5 s, box_cap null, so the fake's `uv run` start-up (well under 1 s on a synced environment, measured by a first test that fails if it exceeds 2 s) cannot move a deadline outcome; marked `@pytest.mark.slow`, about 6 minutes in total)

| # | Failure mode (`REQ` Redesign 3 (h), 5.x) | Injection | Pass condition |
|---|---|---|---|
| F1 | `--resume` fails on a gateway model (R-14) | resume rule: unknown session, exit 1 | `resume_fallback` 1; fresh session launched with the fallback frame; n recomputed with start 16 (`digest.attempt1.jsonl` kept, new digest written); if the recomputed n is 0, no launch and `no_launch_reason: deadline_after_fallback` |
| F2 | Phase 2 killed at the deadline (R-15) | phase-2 rule: emit 2 complete C-lines and half a third, then `sleep_s` 60 | the process is gone within 3 s after `P2_DEADLINE`; `phase2_timeout` true; final report has the 2 lines; elapsed under 1.30 B_f + 4 s |
| F3 | Phase-2 block malformed, re-ask fits | phase 2 returns a line with severity `HIGH`; re-ask returns it fixed | the fixed line is in the final report; `p2reask_s` logged |
| F4 | Phase-2 block malformed, re-ask does not fit | same, with the deadline 1 s away | no re-ask launched; the bad line dropped (`p2_lines_dropped` 1); phase-1 lines intact |
| F5 | Phase 2 rewrites or withdraws phase-1 findings | phase 2 returns a line with id `F1` (a phase-1 id) and a changed claim, plus one `C1` line | the `F1` line is ignored (only `C<n>` ids are extracted); final report holds phase-1 F1 and F2 unchanged plus `P2-F1` from `C1`; immutability check passes |
| F6 | No qualifying peer anchor | ember fixture report with only surface findings | real slots empty; `challenges_real` 0; ECHO `"n/a"`; gap slots filled when the pool is not empty |
| F7 | Two blocks in one report | phase-1 report with two findings-v1 blocks | exactly one block in `<rid>.md`; merge accepts it |
| F8 | Phase-1 hang (R-43) | phase-1 rule `sleep_s` 60 for one luna | killed at T0 + 1.5 B_f (+ 5 s kill margin); `hang_kill` and `SLO_BREACH` true; the other reviewers' reports still merge |
| F9 | Phase-1 bad block then retry (R-44) | attempt 1 returns no block, attempt 2 valid | `attempts` 2; `elapsed_s` includes both; `retry_isolated` true; no digest for that reviewer; its anchors still reach its peers |
| F10 | Wrong observed model | `observed_model: gpt-6.1-sol` for ember on both attempts | `model_ok` false; no fallback to another model (`fallback.log` absent, no third session); package invalid by the section 4 rule, merged with the two lunas, listed in `invalid_pkgs`, left out of quality means |
| F11 | Phase-1 H2 re-ask before the seal (R-11) | attempt returns a 2-error block, re-ask returns a valid one | `p1.md` mtime after the re-ask end; sha at seal equals sha at judging; mode 0444 |
| F12 | Session storage cleanup with two concurrent runs (R-46) | two fake runs on one sandbox; run 1 finishes first | run 1's cleanup deletes nothing while run 2 is active; run 2's phase-2 resume succeeds; after run 2 ends, exactly both runs' listed files are deleted and the directories remain |
| F13 | Reviewer writes into the sandbox (K3, R-09) | `write_file` into `SB/<pkg>/repo/x.txt` | `audit.json` lists `sandbox_dirty`; `QUARANTINE` written; row `contaminated: true`; launcher exit 3; the next launch stops with `E_SANDBOX_DIRTY` |
| F14 | Reviewer reads ground truth (K4) | a fake `tool_use` event with input `cat .../ground-truth.json` | audit violation `forbidden_read`; row `contaminated: true` |
| F14b | Reviewer reads a peer's session transcript, or a killed attempt read ground truth | (a) a `tool_use` input `cat <R3_CLAUDE_PROJECTS>/<slug>/<peer id>.jsonl`; (b) attempt 1 emits a ground-truth read and is then killed with no stdout, attempt 2 is clean | (a) `forbidden_read`; (b) the killed attempt's transcript is captured (9.5) and the violation is found; both rows `contaminated: true` |
| F15 | Merge refusal | every reviewer returns no block on both attempts | package invalid with the merge message; not judged; row lists it in `invalid_pkgs`; exit 2 |
| F16 | Judge failure | `judge_score` absent on the first judge call, present on the second | one retry; `judge_ok` true; with both calls failing, `judge_ok` false and exit 2 |
| F17 | Late finisher gets n = 0 | luna B seals after T0 + 1.30 B_f - 6 - 2 x turn_p90 | no phase 2 for luna B (`no_launch_reason: deadline`); its peers still get its anchors only if they had not launched yet |
| F18 | `PANEL_COLLAB=0` | full fake run | no `board/*.digest.jsonl`, no `p2.*`, no sealed scoring; `collab.json` counters 0; the phase-1 commands equal those of a collab run byte for byte |
| F19 | Phase-2 wrong model | phase-2 `observed_model` differs | `p2_model_mismatch`; no phase-2 lines in the final report |

### 15.4 Gate 0 spikes (run before any arm; results recorded under `R3/spikes/<id>/` with transcripts; R-27)

| Id | Needed for | Procedure | Pass condition |
|---|---|---|---|
| G0-H3 | sandbox bases | `bin/build-sandbox.sh` on each package; for each masked path, diff the sandbox file against the implementing commit's version | each masked path differs from the implementing commit (or is absent at base); no `TASK-WF-<id>` path of the three packages; `.dev/reflect` absent |
| G0-HOOKS (`REQ` S0, part) | sandbox project hooks | read `SB/<pkg>/repo/.claude/settings.json` (all three bases carry a `PreToolUse` block with `Write|Edit` and `Skill` matchers whose scripts are gitignored, so absent in an archive); run one ember phase 1 and grep its transcript for hook errors | recorded; A1 and A3 see the same hooks; a hook error that stops the review fails the spike; with `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`, `git status --porcelain --ignored` of the sandbox shows no `.codegraph/` after the session |
| S2 | resume and streaming | `bin/spike-s2.sh <model>` for `muse-ember-1.0`, `gpt-6-luna`, `claude-sonnet-5-5`, `claude-haiku-5-5`: one `-p` session without `--no-session-persistence` in `SB/<pkg>/repo`, then `--resume <id>` with `stream-json --verbose`, then the same resume killed by `timeout` mid-answer | resume exits 0 with the same `session_id` and `model_ok`; the killed run's file holds at least one `assistant` text event before the kill (luna required; others recorded); transcripts have per-entry `timestamp`; resume start cost and fresh start cost recorded (planning 6 s and 16 s) |
| S3 | full chain | `R3_SMOKE=1 PANEL_COLLAB=1 launch-panel.sh el2 --pkgs TASK-WF-design-20261108-041415` (15.5) | 0 dropped findings lines after H2; `jq -s` filters give `model_ok` and tokens on stream files; merge, anonymiser and judge succeed |
| Spike 4 | values | 3 launches per panel with `PANEL_COLLAB=0 R3_SPIKE4=1`, then `cli.py values-freeze` | values file frozen, its sha recorded and committed by the coordinator before the first arm (R-30); sonnet's and haiku's turn_p90 reported with the n they imply (11.2) |
| G0-SURF | surface regex calibration | `cli.py calibrate-surface` over historical findings of ember and luna in `EVAL/<pkg>/reviews/combos/g1-ember-luna2-r*/` (read only) | the regex matches 15-30% of ember and luna findings (`REQ:578` gives 21-23%); 20 random matches and 20 random non-matches listed for a human read; then pinned |
| G0-ROUTE | expected challenge supply | `cli.py dry-digest` over the same historical EL2 reports at planning n | per receiver: qualifying anchors, real and gap slots; recorded as the expected `challenges_real` (no pass threshold; informs the risk of many isolated packages) |
| Spike 5 (`REQ`) | H share | not a dependency of this code; run by the experiment owner | n/a here |

REQ-S3 (act rate on injected context) and S0's hook-firing checks concern hooks, which F1 does not use. F1's own act rate is measured in every run as the share of launched slots answered with a C-line or "no finding" line (`challenges_answered` in `combine.json`).

### 15.5 One-package smoke test

```
R3_SMOKE=1 NOFALLBACK=1 PANEL_COLLAB=1 bash R3/bin/launch-panel.sh el2 --pkgs TASK-WF-design-20261108-041415
```

Real models, planning values, one package (3 reviewer sessions, up to 3 phase-2 sessions, 2 judge calls). Pass when: exit 0; `collab.json` validates; at least one phase-2 session ran with `model_ok` true, or the log shows why none launched; `merged-anon.md` passes the residue check; `score.json` exists for `full` and `sealed`; the row is in `results/smoke.jsonl`; `audit.json` has no violations; the sandbox check of 9.4 passes; the AC-14 manifests of `REPO/src` and `EVAL` are equal before and after. Then the same command with `PANEL_COLLAB=0` passes the same checks without phase 2.

### 15.6 Acceptance criteria (each pass or fail)

| Id | Criterion |
|---|---|
| AC-1 | `uv run --project "$REPO" pytest -p no:cacheprovider "$R3/tests"` passes with 0 failures and 0 skips |
| AC-2 | Every fault-injection test F1-F19 passes |
| AC-3 | G0-H3, G0-HOOKS, S2 (luna resume and streaming), S3 and G0-SURF pass and are recorded under `R3/spikes/` |
| AC-4 | The frozen values file exists for the panel being run, and its sha in every `collab.json` equals the committed one |
| AC-5 | The smoke test of 15.5 passes in both modes |
| AC-6 | For every package of a run: one `<rid>.md` per reviewer, each with exactly one findings-v1 block that `parse_block` accepts |
| AC-7 | In a collab run, no phase-2 process is alive after T0 + 1.30 B_f + 3 s (events log), and no phase-1 process after T0 + 1.5 B_f + 5 s |
| AC-8 | Every digest line passes `validate_line`; `gt_text_leak` is 0 |
| AC-9 | `merged-anon.md` contains none of the residue strings of 10.1 step 5 |
| AC-10 | `judge-one.sh` sha256 at run time equals the pin, and `score.json` files are under `R3/scoring/` only |
| AC-11 | The results row has every field of 10.4 and is appended to `results/results.jsonl` exactly once per non-smoke launch |
| AC-12 | `PANEL_COLLAB=0` phase-1 commands differ from `RR:48` only by the R-05 allowed items (test_command_diff) |
| AC-13 | No reviewer session ran a model outside the allowlist, and no fallback happened (`observed_model` equals the requested model in every used session) |
| AC-14 | A sha256 manifest of every file under `REPO/src` and `EVAL` (`find -type f`, ignored files included, `__pycache__` excluded and `PYTHONDONTWRITEBYTECODE=1` set for every Python step) is identical before and after building, testing and one smoke run; `test_guards.py` passes, proving `r3_assert_writable` refuses `REPO/src`, `EVAL` and the four other redesign folders. (A git-status comparison cannot be used: the whole `20261113-collab/` tree is untracked and shows as one `??` line, and the other redesign folders change under their own implementers.) |
| AC-15 | Each sandbox's `git status --porcelain` is empty after the last run on it, and every candidate sha256 is unchanged |

## 16. Risks and open questions

### 16.1 Risks

| # | Risk | Effect | Mitigation in this design |
|---|---|---|---|
| X1 | `--resume` or streaming before exit fails on a gateway model | phase 2 always uses the 16 s fallback (n drops by about 1), or a kill leaves nothing to salvage | S2 before any arm; fallback path tested (F1); salvage tested (F2) |
| X2 | Bash is unrestricted, so a reviewer can read ground truth (`EVAL/<pkg>/ground-truth.json`), peer reports under `R3/runs`, or write to the sandbox | contamination or a broken sandbox | audit of every transcript and the sandbox status (9.4); quarantine in place; `E_SANDBOX_DIRTY` stops later runs. This is detection, not prevention, the same as `REQ` 5.5 |
| X3 | The sandbox project `.claude/settings.json` at each base commit registers `PreToolUse` hooks whose scripts are not in the archive | hook errors in every reviewer session | identical in A1 and A3; G0-HOOKS records the effect |
| X4 | Base commits derived from git history, not from a recorded manifest (`REQ:1124`) | wrong H3 baseline | G0-H3 verifies each masked path against the implementing commit before use |
| X5 | Sonnet's or haiku's turn_p90 above 19.0 s or 32.7 s | n falls (sonnet 1, haiku 0); the panel then exchanges mostly toward the lunas | values file gives the real n; the row's `n_planned` shows it; reported, not hidden |
| X6 | Few qualifying peer anchors (ember's findings are 21-23% surface) | many receivers get only gap cards, which are booked to P, not C | G0-ROUTE estimates the supply in advance; `challenges_real` per run |
| X7 | Phase-2 claims mention the second pass despite the frame | the blind judge could tell arms apart | `p2_self_reference` counted; reported per arm; the anonymiser does not rewrite claims |
| X8 | Single runs are noisy (alias EL2 elapsed 98-171 s) and the plan cannot detect the central gain (`REQ:980`) | null results are likely | the design measures; adoption is decided by the arm summary over 12 runs, not by one launch |
| X9 | Sealed judging doubles Opus judge calls in A3 | cost | required by R-29; 2 extra calls per package |

### 16.2 Open questions (defaults already chosen; the owner may overrule)

| # | Question | Default in this design | Alternative |
|---|---|---|---|
| Q1 | `REQ` 4 rule 5 (no ground-truth `plan_quote` substring of 12+ characters in any digest) contradicts F1's anchors, which are exact candidate quotes. Contradiction marker: CONFLICT[`REQ:970` vs `REQ:580`, `REQ:646`]. | Check every digest byte except `anchor`; report `gt_anchor_overlap` (A2) | Apply the rule literally, which would forbid real-anchor challenges on exactly the sentences F1 targets |
| Q2 | Should the strong reviewer on SL2 and HL2 take ember's role? | Yes (11.1) | Run `REQ`'s HL2 shadow variant (haiku isolated, lunas exchange with each other); needs its own gain derivation |
| Q3 | 35 s box cap on SL2 and HL2 | No cap (A4) | Keep 35 s: sonnet n = 1, haiku n = 0 at planning values |
| Q4 | `judge-one.sh` writes through a relative `C` path into `R3/scoring/` (A7) | Byte-unchanged script, outputs inside `R3` | Write scores under `EVAL/arms/scoring/combos/r3-*/`, which breaks the "no write to `EVAL`" constraint |
| Q5 | Spike 4 run count | 3 A1 launches per panel | More launches for a steadier B_f; `REQ` sets no number |
| Q6 | Admission lock is per design (`SB/admit.lock`); five redesigns launching at once can still exceed 10 sessions or 4 ember | per-design lock plus process counting | a lock shared by all five designs (for example `/tmp/evalsb-collab-admit.lock`), which every implementer would have to adopt |
| Q7 | The gap pool excludes the receiver's own phase-1 anchors as well as its peers' | excluded (a gap card on the receiver's own anchor would repeat its own question) | exclude peers' anchors only, as the literal `REQ:592` text says |

## 17. Requirement traceability

| Requirement | Design section | Code | Test or check |
|---|---|---|---|
| R-01 H1 source.md in brief | 3.4, 5.2 | `config/phase1-brief.txt`, `lib/reviewer.sh` | `test_phase1_brief.py`; audit counts runs with no source.md read (reported per model) |
| R-02 H2 normaliser and re-ask | 5.4, 7.4, 8.1 | `findings_io.py`, `reviewer.sh` | `test_h2.py`, F3, F4, F11 |
| R-03 H3/H4 sandbox | 5.1 | `bin/build-sandbox.sh` | `test_sandbox.py`, G0-H3 |
| R-04 merge unchanged | 8.3 | `lib/package.sh` | AC-6, S3 |
| R-05 kill switch command | 5.2, 12 | `reviewer.sh print-cmd` | `test_command_diff.py`, F18, AC-12 |
| R-06 message rules | 6.6, 6.7 | `digest.validate_line` | `test_msg.py`, AC-8 (card and over-cap cases belong to Redesign 4; this validator rejects every non-challenge kind) |
| R-07 frozen catalogue | 3, 15.2 | `config/catalogue.json`, `pins.json` | `test_config.py` |
| R-08 located anchors | 6.1, 6.7 | `digest.qualifies`, `validate_line` | `test_select.py`, `test_msg.py` (F1 sends no `items`) |
| R-09 read-only | 9.4 | `audit` | F13, AC-15 |
| R-10 origin tags | 8.2, 10.1 | `combine`, `anonymise` | `test_combine.py`, `test_anon.py` (mid-run snapshot parts do not apply to F1) |
| R-11 phase-1 seal | 5.4 | `reviewer.sh` | F11 |
| R-12 selection, deal, gap cards | 6.1-6.3 | `digest.py` | `test_select.py`, `test_deal.py`, `test_gap.py`, F6 |
| R-13 router | 6.4 | `digest.route` | `test_router.py` |
| R-14 resume and fallback | 7.2, 7.3 | `reviewer.sh phase2` | S2, F1 |
| R-15 n, deadline, stream, salvage | 6.5, 7.1, 8.1 | `values.compute_n`, `reviewer.sh`, `findings_io` | `test_n.py`, `test_salvage.py`, F2, AC-7 |
| R-16 one block | 8.2 | `combine` | `test_combine.py`, F7 |
| R-21, R-22 hooks | not used by F1 | none | n/a |
| R-23 `collab.json` | 9.1 | `metrics.collab_json` | `test_metrics.py` |
| R-24 elapsed target, SLO | 9.1, 10.5 | `metrics`, `summarize` | `test_summary.py`, F8 |
| R-25 alarms | 9.2, 9.3, 10.5 | `metrics`, `summarize` | `test_metrics.py`, `test_summary.py` |
| R-26 board kept, quarantine in place | 2.2, 9.4 | `package.sh`, `audit` | F13 |
| R-27 Gate 0 | 15.4 | `bin/spike-s2.sh`, `cli.py calibrate-surface`, `dry-digest` | AC-3 |
| R-28 conduct, caps, model check | 5.3, 13.3 | `reviewer.sh`, `package.sh` | F10, AC-13 |
| R-29 blind judging, sealed judging | 10.1, 10.2 | `anonymise`, `launch-panel.sh` | `test_anon.py`, `test_judge_path.py`, F16, AC-9, AC-10 |
| R-30 values frozen before arms | 14 | `values.freeze` | `test_values.py`, AC-4 |
| R-41, R-42 finish time and k (logged only in F1) | 9.1, 14.2 | `values.py` | `test_values.py` |
| R-43 common hang guard | 4, 5.3 | `reviewer.sh` | F8 |
| R-44 retry accounting | 5.3 | `reviewer.sh` | F9 |
| R-45 slowdown, drift band | 14.3, 10.5 | `summarize` | `test_summary.py` |
| R-46 session cleanup | 13.5 | `bin/cleanup-sessions.sh` | F12 |
| R-47 act rates | 15.4 | `combine.json` `challenges_answered` | reported per arm |
