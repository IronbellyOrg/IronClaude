# DESIGN: Redesign 2, Idle-Shift Sweeper (F4), implementation and test specification

Grounding: index_state: fresh (checked_at 2026-11-13T19:30:46Z, projectPath /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel); codegraph tools used: codegraph_status, codegraph_node (symbolsOnly outlines of `src/superclaude/cli/review/merge_cmd.py` and `findings.py`); every quoted line was then Read from disk. Shell scripts and Markdown are not indexed, so the harness scripts were read with Read only.

Status: design only. Nothing in this document is built. Every path under "Files to create" is NOT BUILT until an implementer creates it and its tests pass.

Path abbreviations (same as the source):

| Short | Absolute path |
|---|---|
| `REPO` | `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel` |
| `EVAL` | `REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1` (read-only for this design) |
| `R2` | `REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper` (all code and outputs of this design) |
| `MR` | `REPO/.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md` (source of truth) |
| `RR` | `EVAL/tools/run-reviewer.sh` (today's reviewer launcher) |
| `SBR` | `/tmp/evalsb-collab-r2` (this design's own sandbox root) |
| `B` | a board directory, `SBR/board/<runid>/<pkg>/` |

## 0. Scope, sources and decisions taken

### 0.1 What this design builds

One self-contained harness under `R2/` that runs a three-reviewer panel on the three study packages with the Idle-Shift Sweeper (MR "Redesign 2", requirements R-17..R-20), the harness fixes H1-H4 (MR 2.0, R-01..R-05), the board and hook substrate (MR 2.0, R-06..R-10, R-21..R-26), the timing guards (R-41..R-46), and a `PANEL_COLLAB=0` switch that runs the same panel isolated with the same fixes (arm A1). One launch script runs one panel on all three packages, merges with `superclaude review merge`, anonymises, judges with the unchanged `EVAL/tools/tmp-scripts/judge-one.sh`, and writes one results row.

Out of scope (not asked; named so nobody builds them by accident): the arm scheduler with block randomisation across arms (MR section 4 "Conduct"), arm A0 (today's harness, already runnable with `RR`), arms A2/A3/A5/A6 and other redesigns, Spike 5 (a study-wide H2 re-scoring, owned by whoever runs the full experiment), and session-file cleanup (R-46 governs cleanup only if one is done; this design deletes no session files).

### 0.2 Sources read (all read from disk this run)

- `MR` sections 1, 2.0, 2.1, Redesign 2 (lines 483-571), 3, 4, 5.1-5.10.
- `RR` (whole file): launch command at `RR:48`, report and meta extraction at `RR:50-58`, retry loop at `RR:61-64`, fallback ladder at `RR:66-83`, final copy and cost at `RR:85-87`.
- `EVAL/tools/tmp-scripts/judge-one.sh` (whole file): it hard-codes `EVAL`, takes `C P L`, reads `EVAL/$P/ground-truth.json` and `EVAL/$P/candidate.md`, and writes `D=$EVAL/arms/scoring/combos/$C/$P/$L/score.json` with `claude-opus-5-5`.
- `EVAL/tools/tmp-scripts/anon-b11.sh` (whole file): reviewer ids to `R<i>`, `EVAL` path to `<EVAL>`, candidate and report path redaction, random label.
- `EVAL/analysis/merge-b11.sh` and `b11-launch.sh`, `EVAL/tools/tmp-scripts/b4-job-one.sh`, `EVAL/combos/SPEC.md` (hard limits, batch history, model-misroute incidents).
- `src/superclaude/cli/review/merge_cmd.py` (`command`, lines 71-118), `findings.py` (`_check_finding` 90-121, `parse_block` 124-196, `flat` 272-273, `locate` 276-304), `ledger.py` (`merge_round` 107-157: a line that fails `_check_finding` is dropped, other lines of the block are kept; the merge refuses only when no reviewer has a valid block).
- `EVAL/analysis/final-table.py` lines 4-5 and 33-36: "REAL blocking = judge-blocking AND the GT item has `blocking_in_implement=true`", the source of the results-row definitions in section 5.4.
- `REPO/src/superclaude/hooks/scripts/freshness-session-start.sh:148-152` and `freshness-post-read.sh:16-19`: the in-repo examples of the `hookSpecificOutput.additionalContext` output and the `tool_response` input field this design's hooks use.
- `git log` of the three package folders: each package first appears in one squash-merge commit (`0b8a5801d` designSpec, `4eb75698d` alias, `54e21668f` design), which also carries the implementation. That fixes the H3 base rule in section 2.1.

### 0.3 Decisions this design takes (each is explained where it applies)

| # | Decision | Why | Where |
|---|---|---|---|
| D-1 | On sonnet + 2x luna (SL2) and haiku + 2x luna (HL2) the sweeper is an **ember helper session started at T0**, not a second session of a panel member. | The source's sweeper is ember using its idle time after its 41 s review. SL2 and HL2 have no fast searcher with idle time: sonnet (14 s per turn) and haiku (23 s per turn) are the slowest reviewers and finish after the lunas, so a second sonnet or haiku session would post its facts after the lunas (about 102 s) have stopped. Ember is an allowed model. `SWEEPER_MODEL` can override it with any allowed model. | 3, 7 (Q-1) |
| D-2 | `k` is computed from the **receiver's** own end time and turn times: `k = max(0, min(2, floor((PANEL_FINISH_AT - T0 - E_recv - hooks) / (2 x turn_p90_recv))))`. | On EL2 the receiver (luna) sets B, so `E_recv = B_A1` and `turn_p90_recv = turn_p90`, and the formula is exactly R-42. On SL2 and HL2 the receivers are not on the critical path; R-42 taken literally gives k = 0 on HL2 (haiku's 23 s turns) and would make the design isolated there. | 2.7, 3 |
| D-3 | Only the two **receivers** get hooks. The non-receiving reviewer (ember on EL2, sonnet on SL2, haiku on HL2) launches exactly as in A1, with no `--settings`. | The design adds nothing to the non-receiver's work, so a "finish now" injection on it would truncate it in the collaboration arm and not in A1: a treatment difference unrelated to collaboration. On EL2 ember ends at about 41 s, far before PANEL_FINISH_AT, so this changes nothing in practice there. R-41's literal text ("each reviewer's settings") is narrowed here. | 2.5, 7 (Q-2) |
| D-4 | A fact line carries one extra key, `cmd` (the command string), allowed only on `kind:"fact"`. | R-18 and MR (a) require "every fact carries its command string", but the shared schema in MR 2.0 has no field for it and rejects unknown keys. `cmd` is validated against a read-only command allowlist so it cannot carry prose. | 2.3 |
| D-5 | The board is one file per package, `B/msgs/board.jsonl`, written by `panel-post` and by the harvest hook under one lock. | The balanced deal needs one global append order across the sweeper's facts and the harvested facts. MR 2.0 names `msgs/<rid>.jsonl`; one file with a `from` field holds the same information in order. | 2.3 |
| D-6 | Every sandbox is per run and per package under an opaque run id: `SBR/sb/<runid>/<pkg>/`. | A row name such as `f4-el2-r1` in a path the reviewer reads would tell it which arm it is in; concurrent runs never share a sandbox, so the read-only audit (`git status`) and the session files never collide. | 2.1 |
| D-7 | The unchanged `judge-one.sh` is called from its own path; its output directory is moved under `R2/scoring/` by passing a relative combo argument `C=../../../../20261113-collab/r2-idle-shift-sweeper/scoring/<opaque>`. | `judge-one.sh` hard-codes `D=$EVAL/arms/scoring/combos/$C/$P/$L`; with this `C` the path resolves to `R2/scoring/<opaque>/<P>/<L>`, so nothing is written under `EVAL` and the judge file stays byte-identical (sha256 pinned). `<opaque>` is a random id, identical in form for both arms, so the judge cannot tell collaboration from baseline. | 5.2 |
| D-8 | Hooks and `panel-post` are bash + `jq`; all Python (normaliser, tagger, metrics, results, audits, values) runs through `uv run`. | Hooks run on every tool call; a `uv run` start on each call would cost more than the 0.1 s per call the source budgets. | 1 |

## 1. Files to create

All paths are relative to `R2/`. Nothing is created or edited outside `R2/` and `SBR/` (and the Claude session files that `claude -p` itself writes under `~/.claude/projects/`). `EVAL/` and `src/` are read only.

### 1.1 Tree

```text
R2/
  DESIGN.md                      this file
  README.md                      operator quick start: build, Gate 0, smoke, one launch
  config/
    catalogue.json               frozen move catalogue M1-M10 (verbatim MR 2.0 text)
    panels.json                  role map for EL2, SL2, HL2
    manifest.json                base SHAs (H3), pinned sha256 values, values-file sha256
    planning-values.json         planning timing values (smoke tests only; never used for an arm)
    spike4-values.json           bootstrap values for Spike 4's A1 runs (hang guard 3000 s, k 0)
    values/<panel>/<pkg>.json    Spike 4 values, frozen before the first arm
  bin/
    build-sandbox.sh             H3+H4 base tarball per package
    run-reviewer2.sh             reviewer launcher: copy of RR plus H1, H2, hang guard, settings, isolated retry
    run-sweeper.sh               sweeper launcher
    run-package.sh               one panel on one package
    launch-panel.sh              THE launch script: one panel on three packages, merge, anonymise, judge, results row
    make-settings.sh             writes per-session --settings JSON with baked constants
    anon.sh                      anonymiser
    judge.sh                     sha-checked wrapper around the unchanged EVAL judge-one.sh
    panel-post.tmpl              template baked into B/bin/panel-post per package
    hooks/receiver-hook.sh       luna PostToolUse hook: count, seal, deal, deliver, finish signal
    hooks/harvest-hook.sh        sweeper PostToolUse hook: harvest unopened paths into facts
    lib/common.sh                flat, now_ms, atomic append, metric log, error trap
    lib/validate-msg.sh          panel-msg/1 fact validator (the only validator)
    lib/render-fact.sh           fact -> delivered text (fixed template)
  py/
    h2_normalize.py              H2: truncate, parse with the real findings parser, list errors
    tagger.py                    origin own/peer tagging of findings lines
    collab_metrics.py            collab.json writer, late, echo, Jaccard, first-hand and re-run audit
    values.py                    k, PANEL_FINISH_AT, sweeper kill, hang guard; Spike 4 reducer
    results_row.py               results row JSON from score.json + ground truth + costs + collab.json
    audits.py                    contamination, read-only and catalogue audits
    summarize_arm.py             arm-level alarms and stop rules over results rows
  spikes/
    s0-hooks.sh  s2-resume.sh  s3-smoke.sh  reqs3-actrate.sh  spike4-values.sh  h3-base-check.sh  sw1-sweeper.sh
    RESULTS.md                   one PASS/FAIL line per spike with evidence paths
  tests/
    conftest.py                  fixtures, PATH with the fake claude, tmp board/sandbox builders
    fakes/claude                 fake `claude -p` (uv inline script) that replays scripted tool calls through the real hooks
    fixtures/                    candidate, source, reports, transcripts, boards, ground truth (synthetic, not the study's)
    test_*.py                    see section 6
  runs/<row>/<pkg>/              outputs per row and package (never deleted)
  scoring/<opaque>/<pkg>/<label>/  judge inputs and score.json (written by judge-one.sh)
  results/<row>.json             results rows
  results/keys/<opaque>.json     opaque id -> row mapping (never given to the judge)
```

### 1.2 Interfaces

| File | Purpose | Interface (arguments, inputs, outputs, exit codes) |
|---|---|---|
| `config/catalogue.json` | The frozen move texts (R-07). | `{"version":"moves/1","moves":{"M1":"<text>",...,"M10":"<text>"}}`, texts copied verbatim from the MR 2.0 table "Move (text sent to a reviewer)" column. Its sha256 is in `manifest.json`. |
| `config/panels.json` | Roles per panel (section 3). | `{"EL2":{"reviewers":[{"rid":"t2b-1","model":"muse-ember-1.0","role":"searcher"},{"rid":"t4-1","model":"gpt-6-luna","role":"receiver","recv_index":0},{"rid":"t3-1","model":"gpt-6-luna","role":"receiver","recv_index":1}],"sweeper":{"model":"muse-ember-1.0","start":"after:t2b-1"},"critical_role":"gpt-6-luna"}, "SL2":{... "t1b-1" claude-sonnet-5-5 "nonreceiver" ..., "sweeper":{"model":"muse-ember-1.0","start":"t0"},"critical_role":"claude-sonnet-5-5"}, "HL2":{... "t2-1" claude-haiku-5-5 ..., "critical_role":"claude-haiku-5-5"}}`. |
| `config/manifest.json` | Pins (R-03, R-07, R-29, R-30). | `{"base_sha":{"<pkg>":"<40-hex>",...},"base_rule":"first parent of the squash commit that first added the package folder","sha256":{"judge-one.sh":"...","catalogue.json":"...","brief_a1":"...","sweeper_brief":"...","values/<panel>/<pkg>.json":"..."},"committed_at":"<UTC>"}`. |
| `config/values/<panel>/<pkg>.json` | Frozen timing values (R-30, rule 6). | `{"panel","pkg","B_f","turn_p90_crit","T_report_p90_crit","E_recv","turn_p90_recv","T_report_p90_recv","hooks_s":2,"panel_finish_at_s","k","sweeper_kill_s","hang_s","source":"spike4|planning","n_runs"}`; all `*_s` are offsets from T0 in seconds. |
| `bin/build-sandbox.sh <pkg>` | H3+H4: `git -C REPO archive <base_sha> \| tar -x` into a temp dir, delete `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research`, `.dev/reflect`, then tar it to `SBR/base/<pkg>.tar` with its sha256. | Exit 0 and prints the tar sha256; exit 2 if `base_sha` is missing from `manifest.json`; exit 3 if any removed directory still exists in the tar listing. Idempotent: an existing tar with a matching recorded sha256 is kept. |
| `bin/run-reviewer2.sh` | Reviewer launcher (section 2.2). | `run-reviewer2.sh --pkgdir <runs/row/pkg> --sb <SBR/sb/runid/pkg> --pkg <pkg> --rid <rid> --model <m> --deadline-ms <T0+hang> [--settings <file>] [--print-cmd]`. Writes `reviews/<rid>.attempt<N>.{json,md,err,meta.json}`, `<rid>.md`, `<rid>.meta.json`, `<rid>.cost.json`, `<rid>.h2.json`, `<rid>.norm.md`, optional `<rid>.reask.jsonl`, and the marker `<rid>.attempt1.exit` the moment attempt 1's process exits. `--print-cmd` prints the argv of attempt 1 as one JSON array and exits 0 (used by the R-05 test). Exit 0 when `model_ok` and the block parse; 1 otherwise (the package runner marks the reviewer INVALID). |
| `bin/run-sweeper.sh` | Sweeper launcher (section 2.4). | `run-sweeper.sh --pkgdir --sb --board <B> --model <m> --kill-ms <T0+sweeper_kill> --k <k>`. Writes `sweeper/sw-1.{json,md,err,meta.json}`. Never writes a findings block; never passed to the merge. |
| `bin/run-package.sh` | One panel on one package (section 2.2 timeline). | `run-package.sh --row <row> --runid <hex> --pkg <pkg> --panel <EL2\|SL2\|HL2> --values <file>`; reads `PANEL_COLLAB` (0 or 1, default 1). Writes everything under `runs/<row>/<pkg>/`, ending with `collab.json` and the marker `DONE`. Exit 0 if every reviewer and (collab) the sweeper have `model_ok:true`; else 1 with `INVALID` written. |
| `bin/launch-panel.sh` | One panel on all three packages (section 5). | See 5.1. |
| `bin/make-settings.sh` | Writes `--settings` JSON with every constant baked into the hook command (R-21). | `make-settings.sh receiver --board B --rid <rid> --recv-index <0\|1> --t0-ms --finish-ms --k --deal-r --out <file>` and `make-settings.sh sweeper --board B --t0-ms --finish-ms --out <file>`. Resolves `bash` and `jq` to absolute paths at write time and bakes them in. |
| `bin/panel-post.tmpl` | Source of the per-package helper the sweeper calls (MR 2.0 "Writing"). | Baked copy `B/bin/panel-post` (mode 0755) with the board path, sandbox, candidate, source, T0, PANEL_FINISH_AT and the 2k cap substituted. Usage: `panel-post --move M1 --cmd '<command>' [--anchor '<plan phrase>'] [--n <int>] --item <path[:line]> [--item ...]`. Prints `posted f-<n>` (exit 0), `rejected: <reason>` (exit 1) or `refused: finish` (exit 1). Unknown flags are rejected. |
| `bin/hooks/receiver-hook.sh` | Luna hook (section 2.5). | PostToolUse command; all parameters as baked arguments; reads the hook JSON on stdin; prints either nothing or one `{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"<=1500 chars"}}` line; always exits 0. |
| `bin/hooks/harvest-hook.sh` | Sweeper hook (section 2.4). | Same contract; never prints context; posts at most one harvested fact per call through `lib/validate-msg.sh`. |
| `bin/lib/validate-msg.sh` | The only fact validator (R-06, R-08, D-4). | `validate-msg.sh --board B --line '<json>'`; prints `ok` (exit 0) or `reject <reason>` (exit 1). Reasons: `too_long`, `bad_json`, `forbidden_key:<k>`, `unknown_key:<k>`, `bad_kind`, `bad_move`, `bad_anchor`, `anchor_not_in_candidate`, `bad_item:<x>`, `item_missing:<x>`, `too_many_items`, `bad_cmd`, `bad_n`, `second_witness`, `over_cap`, `after_finish`. |
| `bin/lib/render-fact.sh` | Fact rendering (section 2.5.3). | `render-fact.sh --catalogue <file> --line '<json>'` prints the delivered text (at most 1,500 characters, enforced by trimming items from the end). |
| `bin/anon.sh` | Anonymiser (section 5.2). | `anon.sh --merged <runs/row/pkg/merged-1.md> --out-dir <scoring/opaque/pkg>`; picks a random label, writes `<label>/merged-anon.md` and `label-key.json`, then self-checks; exit 4 if any forbidden token survives. |
| `bin/judge.sh` | Calls the unchanged judge. | `judge.sh <opaque> <pkg> <label>`: checks `sha256sum EVAL/tools/tmp-scripts/judge-one.sh` equals `manifest.json`, then runs `bash EVAL/tools/tmp-scripts/judge-one.sh "../../../../20261113-collab/r2-idle-shift-sweeper/scoring/<opaque>" <pkg> <label>`; exit 5 on a sha mismatch (nothing is judged). |
| `py/h2_normalize.py` | H2 (R-02). | `uv run --project REPO python R2/py/h2_normalize.py --report <rid>.md --out <rid>.norm.md --json <rid>.h2.json`. Imports `superclaude.cli.review.findings` (`parse_block`, `flat`). Output JSON: `{"truncated":{"anchor":n,"anchor2":n,"claim":n},"errors":[{"line":..,"msg":..}],"block_ok":bool,"needs_reask":bool}`. |
| `py/tagger.py` | Origin tags (R-10). | `tagger.py --report <rid>.norm.md --board-dir B --rid <rid> --out <rid>.final.md`; adds `"origin":"own"\|"peer"` to every findings line; writes the tag reasons to `<rid>.tags.json`. |
| `py/collab_metrics.py` | `collab.json` (R-23) and the F4 audits (R-20). | `collab_metrics.py --pkgdir runs/<row>/<pkg> --panel <p> --values <file> --arm <F4\|A1>`; validates its own output against the schema in 2.9 before writing. |
| `py/values.py` | Timing arithmetic (R-41, R-42, D-2) and the Spike 4 reducer. | `values.py compute --panel --pkg --B --turn-crit --report-crit --e-recv --turn-recv --report-recv` prints the values JSON; `values.py reduce --runs <dirs...>` computes the inputs from A1 transcripts. Pure functions `k()`, `finish_at()`, `sweeper_kill()`, `hang()` are imported by tests. |
| `py/results_row.py` | Results row (section 5.4). | `results_row.py --row <row> --opaque <id> --out results/<row>.json`. |
| `py/audits.py` | Contamination and read-only audits (section 2.8). | `audits.py run --pkgdir runs/<row>/<pkg>` writes `audit.json` with `ok` and a list of violations; `audits.py catalogue` checks R-07 against the three ground-truth files. |
| `py/summarize_arm.py` | Arm-level alarms and stop rules (R-24, R-25, MR 4 abort rows). | `summarize_arm.py --rows results/*.json --baseline-rows <A1 rows> --out <arm-summary.json>`. |
| `spikes/*.sh` | Gate 0 (section 6.3). | Each writes `spikes/out/<spike>/` and appends one `PASS`/`FAIL` line to `spikes/RESULTS.md`. |
| `tests/fakes/claude` | Test double for `claude -p`. | Same flags the harness uses; reads a scenario file named by the brief's first line marker `#SCENARIO <path>` or by the fixed path `SBR/fake-scenario.json` for launcher tests; replays `tool_calls` (each with a sleep), piping PostToolUse JSON into every hook command found in `--settings`; prints a JSON array in the shape `RR:50-53` parses (`assistant` messages with `.message.model`, one `result` with `.result`, `.usage.output_tokens`, `.modelUsage`, `.session_id`); supports `--resume`. |

## 2. Behaviour

### 2.1 Sandboxes and the harness fixes H1-H4 (R-01, R-03, R-09)

**H3 base commit.** For each package the base is the first parent of the squash-merge commit that first added the package folder (found with `git log --reverse --format=%H -- .dev/tasks/to-do/<pkg> .dev/tasks/done/<pkg> | head -1`):

| Package | Squash commit that added it | Base recorded in `manifest.json` |
|---|---|---|
| `TASK-WF-designSpec-20261107-075614` | `0b8a5801d` | `0b8a5801d^1` (full SHA resolved by `git rev-parse`) |
| `TASK-WF-makeTheAliasOnly-20261105-051649` | `4eb75698d` | `4eb75698d^1` |
| `TASK-WF-design-20261108-041415` | `54e21668f` | `54e21668f^1` |

This is the tree on master just before the package's plan and its implementation landed. It may hold unrelated commits made after the plan's branch point; spike `h3-base-check.sh` (section 6.3) verifies the masking lines are absent, which is the property H3 exists for.

**H4.** `build-sandbox.sh` removes `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research` and `.dev/reflect` from the archive and fails (exit 3) if `tar -tf` still lists any of them.

**Per-run sandbox (D-6).** For each package of a run, `run-package.sh` creates:

```text
SBR/sb/<runid>/<pkg>/repo/        tar -x of SBR/base/<pkg>.tar, then: git init -q; git add -A; git commit -qm snap
SBR/sb/<runid>/<pkg>/cand/candidate.md   byte copy of EVAL/<pkg>/candidate.md
SBR/sb/<runid>/<pkg>/cand/source.md      byte copy of REPO/.dev/tasks/done/<pkg>/source.md
```

`<runid>` is 8 random hex characters (`od -An -N4 -tx1 /dev/urandom | tr -d ' \n'`), the same for the three packages of one launch, and mapped to the row only in `runs/<row>/runid`. The candidate and source sha256 values are recorded in `runs/<row>/<pkg>/inputs.json`.

**H1 brief (A1 brief, used unchanged by every reviewer in both arms).** It is `RR:13-17` with only these substitutions: `$CAND_SB` becomes `SBR/sb/<runid>/<pkg>/cand/candidate.md`, and directly after the sentence `Review the candidate ... (sha256 of the file: $SHA) against the requirements it states, review 1 of 3.` this sentence is inserted:

```text
Its source document is <SBR/sb/<runid>/<pkg>/cand/source.md> (sha256 of the file: <SRC_SHA>); read both files in full before you review.
```

The brief template with placeholders is hashed into `manifest.json` as `brief_a1`. Receivers get no brief change: in this design the extra instruction text goes only to the sweeper (MR 2.0 rule 5(c)), so the critical-path slowdown `s` should be about 0; Spike 4 still measures it (R-45).

**Read-only (R-09, MR 5.5).** After the package ends, `audits.py` checks `git -C SBR/sb/<runid>/<pkg>/repo status --porcelain` is empty and the candidate and source sha256 values are unchanged. Hooks and `panel-post` write only under `B`, which is under `SBR/board/`, outside the sandbox repo and the candidate directory.

### 2.2 Package timeline and the reviewer launcher

**Timeline of one package (`run-package.sh`).**

1. Build the sandbox (2.1) and, when `PANEL_COLLAB=1`, the board `B` (2.3), the per-package `B/bin/panel-post`, `B/named.txt` and the `--settings` files.
2. `T0 = now_ms`, written to `runs/<row>/<pkg>/t0`.
3. Start the three reviewers at once, each in the background: `run-reviewer2.sh ... --deadline-ms $((T0 + hang_s*1000))`, receivers with `--settings` when `PANEL_COLLAB=1`.
4. When `PANEL_COLLAB=1`, start the sweeper: on EL2 as soon as `reviews/t2b-1.attempt1.exit` exists (poll every 0.5 s); on SL2 and HL2 at T0 (D-1). Its actual start is logged as `sweeper_start_t`.
5. Wait for every background process. `elapsed_s = (max end time of every process of the package, re-asks and sweeper included) - T0`.
6. Copy `B` to `runs/<row>/<pkg>/board/` (R-26; the `SBR` copy is also kept), run `tagger.py` for each reviewer, `collab_metrics.py`, `audits.py run`, then write `DONE`.

**`run-reviewer2.sh`: what it keeps from `RR` and what it changes.**

| Part of `RR` | In `run-reviewer2.sh` |
|---|---|
| `RR:13-17` brief | Kept, with the H1 sentence and the sandbox paths (2.1). |
| `RR:48` command | `( cd SBR/sb/<runid>/<pkg>/repo && timeout <remaining_s> claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit [--settings "$SETTINGS_FILE"] <<<"$BRIEF" )`. Differences from `RR:48`: the sandbox path (R-03), the brief (R-01), no `--no-session-persistence` (MR 2.0), `timeout` set to the time left until `T0 + 1.5 B_f` instead of 3000 (R-43), and `--settings` only on a collaboration receiver's attempt 1. |
| `RR:50-58` report, model and token extraction, `model_ok`, `findings_block` | Kept verbatim, plus `session_id` read with `jq -r '[.[]\|select(.type=="result")\|.session_id][0]'`, and `start_ms`, `end_ms`, `hang_kill` (exit code 124 from `timeout`) added to the attempt meta. |
| `RR:61-64` retry loop | Kept (at most 2 attempts). Attempt 2 runs without `--settings` and is logged `retry_isolated:true` (R-44); attempt 2 is not started when the time left before the hang deadline is under 10 s (it is logged `retry_skipped_deadline`). |
| `RR:66-83` fallback ladder | **Removed.** `NOFALLBACK=1` is required by the launcher, and this copy has no ladder, so a misrouted or failed model can never be swapped silently. |
| `RR:85-87` final copy and cost | Kept; `cost.json` also sums `reask_s` and the re-ask output tokens. |

**H2 after the final attempt (R-02).**

1. `h2_normalize.py` reads `<rid>.md`. In the last findings-v1 block it truncates `anchor` and `anchor2` to `flat(x)[:200]` and `claim` to `flat(x)[:300]` when longer (a prefix of a whitespace-flattened exact quote is still found by `findings.locate`, which flattens both sides), writes `<rid>.norm.md`, and parses it with `superclaude.cli.review.findings.parse_block`.
2. If `parse_block(...)["ok"]` is false, and `deadline - now >= 6 s + turn_p90(model)`, the launcher re-asks once, under the same hang deadline (`timeout <deadline - now>`; exit 124 logs `hang_kill: true` and `slo_breach: true`): `claude -p --resume <session_id> --model "$MODEL" --output-format stream-json --verbose --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit` (no `--settings`, so a re-ask never receives a fact), with the prompt `Your findings block has these problems: <one line per error: line N: msg>. Reply with the complete report again, with the same findings, changing only what these errors require.` The stream goes to `<rid>.reask.jsonl`; the model check runs on it with `jq -s`. The re-ask result is normalised again (step 1).
3. Lines still invalid are counted in `meta.json` as `dropped_lines`; `reask_s` is logged in every arm, A1 included, and counts in `elapsed_s`.

### 2.3 Board and message schema (MR 2.0, R-06, R-08, D-4, D-5)

**Board layout `B = SBR/board/<runid>/<pkg>/`:**

```text
B/msgs/board.jsonl      validated facts, one per line, append order = deal order
B/msgs/rejected.jsonl   {"t","from","line","reason"} for every refused post
B/snap/<rid>.jsonl      transcript snapshot (seal), B/snap/<rid>.sha256
B/state/<rid>.calls     tool-call counter; B/state/<rid>.delivered (fact ids, one per line)
B/state/<rid>.sealed | <rid>.snapfail | <rid>.finish_sent
B/state/opened.txt      every path any receiver opened with Read (union, for the harvest filter)
B/state/seq             fact id counter; B/state/lock (flock)
B/metrics/<id>.jsonl    hook events per session id (t4-1, t3-1, sw-1)
B/bin/panel-post        baked helper
B/named.txt             repo paths the candidate names (computed once at package start)
B/cand.flat             whitespace-flattened candidate text (for anchor checks)
```

**Fact line (`panel-msg/1`, `kind:"fact"`).**

```json
{"v":"panel-msg/1","id":"f-3","run":"<runid>/<pkg>","from":"sw-1","to":"*","t":1731500041123,
 "kind":"fact","move":"M1","anchor":"<12-200 chars copied exactly from candidate.md>",
 "items":["tests/skills/test_worker_contract.py","CHANGELOG.md:166"],"n":2,
 "cmd":"grep -rln 'worker-contract' tests/"}
```

`id`, `run`, `from`, `to` and `t` are set by `panel-post` or the harvest hook, never by the model. `from` is `sw-1` (sweeper post) or `hv-1` (harvest). `to` is always `*`: the receiver hook does the deal.

**Validation rules (`lib/validate-msg.sh`), applied in this order; the first failure rejects the line, which is appended to `rejected.jsonl` and never delivered:**

| # | Rule | Reason code |
|---|---|---|
| 1 | Serialized line is at most 600 bytes (`printf %s "$line" \| wc -c`). `panel-post` first drops lowest-ranked items until the line fits; it rejects only if one item still does not fit. | `too_long` |
| 2 | Parses as one JSON object. | `bad_json` |
| 3 | No key from `claim`, `verdict`, `blocking`, `severity`, `category`, `note`. | `forbidden_key:<k>` |
| 4 | Every key is in `{v,id,run,from,to,t,kind,move,anchor,items,n,cmd}`. | `unknown_key:<k>` |
| 5 | `v == "panel-msg/1"` and `kind == "fact"` (this design's board accepts facts only). | `bad_kind` |
| 6 | `move` in `{M1,M2,M7}`, or in `{M6,M9}` for a witness fact; at most one witness fact per package. | `bad_move`, `second_witness` |
| 7 | `anchor`, if present: a string whose flattened length is 12-200 and which is a substring of `B/cand.flat` (`grep -qF`). | `bad_anchor`, `anchor_not_in_candidate` |
| 8 | `items`: an array of at most 8 strings. Each is `path` or `path:line` with a repo-relative path (no leading `/`, no `..` segment) naming a regular file under the sandbox repo, with `line` at most its line count; or, only in a witness fact, `source.md:<line>` with `line` at most the line count of the package's `cand/source.md`. | `too_many_items`, `bad_item:<x>`, `item_missing:<x>` |
| 9 | `n`, if present: an integer >= 0. | `bad_n` |
| 10 | `cmd`: required; at most 240 characters; first word in `{grep, rg, find, ls, wc, git}` (for `git`, the second word in `{grep, ls-files}`); none of `;` `&` `>` `<` `` ` `` `$(` `#` or a newline; a `\|` may only be followed by `wc`, `sort`, `uniq`, `head`, `grep` or `cut`; `find` may not carry `-exec`, `-execdir`, `-delete`, `-ok`, `-fprint`. Absolute paths are allowed only for the package's `cand/` directory. | `bad_cmd` |
| 11 | Cap: the sweeper's posts and the harvested facts together (`from` in `{sw-1, hv-1}`) are at most 2k per package, counted under the board lock (MR (b): "the sweeper posts at most 2k facts"; harvested facts come from the sweeper's own session). | `over_cap` |
| 12 | `t < PANEL_FINISH_AT`. After it `panel-post` prints `refused: finish`. | `after_finish` |

Append is atomic: the validated line plus `\n` is written with one `printf` to `board.jsonl` while holding `flock B/state/lock`; the id counter is incremented under the same lock.

The validator never reads ground truth. The ground-truth substring check runs after the run, in `audits.py` (2.8).

### 2.4 The sweeper (R-17, R-18)

**Launch (`run-sweeper.sh`).**

```text
( cd SBR/sb/<runid>/<pkg>/repo && timeout <kill_s - now> claude -p --model "$SWEEPER_MODEL" --output-format json \
    --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit \
    --settings <B/../settings/sw-1.json> <<<"$SWEEPER_BRIEF" ) > runs/<row>/<pkg>/sweeper/sw-1.json
```

- Kill time: `T0 + sweeper_kill_s`, where `sweeper_kill_s = panel_finish_at_s - 2 x turn_p90_recv` (MR (b): T0 + 131.0 s at EL2 planning values). If the computed timeout is 10 s or less, the sweeper is not started and `sweeper_skipped_late:true` is logged (reported as dilution, never compensated).
- The sweeper's meta gets the same `model_ok` check as a reviewer (`RR:51-56`). A package whose sweeper has `model_ok:false` is marked INVALID (it was contaminated by the wrong model's facts) and is re-run under the study's quarantine-in-place convention.
- The sweeper is never given any reviewer report path. Its brief names only the candidate, the source and `B/bin/panel-post`. `audits.py` fails the package if any sweeper tool input (2.8 rule: tool inputs only) names a path under `R2/runs/`, any `/reviews/` directory, `*/ground-truth*.json`, `20261111-a1` or `.dev/reflect`.
- When `k = 0` for the package, the sweeper is not started (its cap would be 0) and `sweeper_skipped_k0: true` is logged.
- No retry: a failed sweeper simply leaves fewer facts (logged `sweeper_exit`).

**Sweeper brief (generated from `catalogue.json`; template hashed in `manifest.json` as `sweeper_brief`).** `<Mx text>` is the catalogue text verbatim; `<POST>` is the absolute path of `B/bin/panel-post`; `<CAP>` is 2k.

```text
You are a search helper for a review panel. You do not review the plan and you write no findings and no report.
Work read-only in this repository (your current directory). The plan is <CAND>. Its source document is <SRC>.
Run these moves against the plan and the repository:
M1: <M1 text>
M2: <M2 text>
M7: <M7 text>
At most once, instead of one of the above: a line of <SRC> with no counterpart in the plan, or a pair of tables in <SRC> whose reader and writer sit in different tables, checked against <SRC> only, never against the repository files (M9: <M9 text> / M6: <M6 text>).
Post each fact as soon as you find it, with one command per fact:
  <POST> --move <M1|M2|M7|M6|M9> --cmd '<the exact read-only command you ran, re-runnable from the repository root>' --anchor '<12 to 200 characters copied exactly from the plan>' --item <repo-relative path or path:line> [--item ...] [--n <count>]
Rules: facts only: paths, counts and path:line hits. Never a judgement, a severity, an explanation or a recommendation.
At most <CAP> facts, at most 8 items per fact. Prefer files the plan never names. Use source.md:<line> as the item for a source line.
If the helper prints "rejected: <reason>", fix that one thing and post again once. Stop when it prints "refused: finish" or when you have posted <CAP> facts.
End with the single word: done
```

**Harvest hook (`hooks/harvest-hook.sh`, PostToolUse on the sweeper).** On each call:

1. Only for tool names `Bash`, `Grep`, `Glob`; otherwise exit 0.
2. Command string: for `Bash`, `tool_input.command`; for `Grep`, the synthesised `grep -rn -- '<pattern>' <path or .>`; for `Glob`, `find . -path './<pattern>'`. If it fails rule 10 of the validator, stop.
3. Move by observable signature (MR 2.0 table column "Observable tool-call signature"): a recursive grep over `tests/` gives M1; a listing or count across a directory (`grep -l`, `grep -c`, `find`, `\| wc -l`) gives M2; a recursive search from `.` or naming a root-level file gives M7; anything else posts nothing.
4. Paths: every token in `tool_response` (stdout) that matches `^\.?/?([A-Za-z0-9_.@+-]+/)*[A-Za-z0-9_.@+-]+(:[0-9]+)?` at the start of a line and names a file in the sandbox; minus paths in `B/named.txt`, `B/state/opened.txt` and any item already on the board.
5. Rank: unnamed test files (`tests/...` not in `named.txt`) first, then root-level documents (no `/`, extension `.md`), then the rest; keep 8.
6. If at least one path is left, post `{"from":"hv-1","move":...,"cmd":...,"items":[...]}` (no `anchor`, no `n`) through the validator, under the shared 2k cap.

Move precedence when a command matches several signatures: M1, then M2, then M7. Because only the receivers are hooked (D-3), `opened.txt` holds only the lunas' reads; on EL2 ember's own reads are added from its transcript's Read inputs the moment `t2b-1.attempt1.exit` appears, before the sweeper starts.

The hook prints nothing to the sweeper and always exits 0.

### 2.5 The receiver hook (R-19, R-20, R-21, R-22, R-41)

**Settings (one file per receiver, written by `make-settings.sh`; nothing read from the environment).**

```json
{"hooks":{"PostToolUse":[{"matcher":"*","hooks":[{"type":"command","timeout":5,
 "command":"/usr/bin/bash R2/bin/hooks/receiver-hook.sh --jq /usr/bin/jq --board SBR/board/<runid>/<pkg> --rid t4-1 --recv-index 0 --t0-ms <T0> --finish-ms <T0+panel_finish_at_s*1000> --k <k> --deal-r <r> --catalogue R2/config/catalogue.json"}]}]}}
```

(Every path in the real file is absolute; `/usr/bin/bash` and `/usr/bin/jq` are the paths `command -v` returned when the file was written. Both hook scripts start with the constant `PATH=/usr/bin:/bin`, so `cp`, `sha256sum`, `flock` and `date` resolve the same way whatever environment the CLI passes; S0 confirms these binaries exist there.)

**2.5.1 State machine, run on every PostToolUse call (all state changes under `flock B/state/lock`).**

1. Trap: any error prints nothing, appends `{"ev":"hook_error","t","msg"}` to `B/metrics/<rid>.jsonl` and exits 0 (R-22).
2. Read stdin once: `transcript_path`, `tool_name`, `tool_input`. Increment `state/<rid>.calls` to `c`. Log `{"ev":"call","t","c","tool":tool_name,"ms":<hook duration>}` (the duration is written at exit, for `hook_ms_p95`).
3. If `tool_name == "Read"`, append `tool_input.file_path` (made repo-relative when it is inside the sandbox) to `state/opened.txt`.
4. Finish signal: if `now >= finish_ms`: if `state/<rid>.finish_sent` does not exist, create it, log `{"ev":"finish_signal","t"}` and print the context `Time check: finish now with what you have. Write your final report with its findings block now.`; in every case deliver nothing more and exit 0.
5. If `c < 6`, exit 0.
6. If `snapfail` exists, exit 0 now and for the rest of the run (fail closed).
7. If the count of lines in `state/<rid>.delivered` is `>= k`, exit 0.
8. Deal: line `i` (0-based) of `msgs/board.jsonl` belongs to this receiver when `(i + deal_r) mod 2 == recv_index`. Among this receiver's lines not yet delivered, pick the best by rank (the class of its first item after ranking: unnamed test 0, root-level document 1, other or witness 2), ties by lower `i`. If none exists, exit 0.
9. Seal, immediately before the first delivery (MR 2.0 "Independence"): if `sealed` does not exist: `cp "$transcript_path" B/snap/<rid>.jsonl.tmp && sha256sum > B/snap/<rid>.sha256 && mv` into place, then create `state/<rid>.sealed` and log `{"ev":"seal","t","sha256"}`. On any failure create `state/<rid>.snapfail`, log `{"ev":"snapshot_missing","t"}` and exit 0 without delivering.
10. Render the picked fact (2.5.3), print `{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":<text>}}`, append its id to `state/<rid>.delivered`, log `{"ev":"deliver","t","c","fact":id,"i":i}`. At most one fact per call.

There is no Stop hook, so no reviewer is ever held (`stop_blocks = 0` by construction).

**2.5.2 Deal seed.** `deal_r = (first byte of sha256("<runid>/<pkg>/deal")) mod 2`, computed by `run-package.sh` and logged in `collab.json`.

**2.5.3 Rendered text (fixed template; the only variable parts are catalogue text, the exact plan quote, paths, the command and the count).**

```text
Search result to check yourself (not a finding; no conclusion attached).
Move <Mx>: <catalogue text for Mx>
Plan text searched: "<anchor>"                      (line omitted when no anchor)
Command: <cmd>
Paths: <item>, <item>, ...                           (line omitted when no items)
Count: <n>                                           (only when n >= 1)
Re-run this command yourself: its result is not shown here.   (instead of Count, when n == 0)
Before you cite any path above, open it or re-run the command yourself. Decide for yourself whether anything here is a defect.
```

A count fact with `n == 0` is never shown as a count (R-18, "no clearance"). Text over 1,500 characters is cut by dropping items from the end, then by cutting the anchor line.

**2.5.4 What is logged after the run (by `collab_metrics.py`, from the board and the metrics files):**

- `late`: a fact dealt to a receiver, not delivered, with `t` later than the receiver's last logged call. The receiver's package counts as isolated for it when it received 0 facts (`isolated_for` list).
- `not_delivered_cap`: dealt, arrived in time, not delivered because `k` was reached.
- `not_delivered_other`: dealt, arrived before the receiver's last call, `k` not reached, but every later call picked a better-ranked fact or no later call happened. Every dealt fact is in exactly one of `delivered`, `late`, `not_delivered_cap`, `not_delivered_other` (tested).
- `first_delivery_t`, `facts_delivered` (must be `<= k`), `seal_t`, `snapshot_missing`, `finish_signal_t`, `hook_calls`, `hook_error`, `hook_ms_p95`.

### 2.6 Peer tagging and what reaches the merge (R-04, R-10)

`tagger.py` adds `"origin"` to every line of the final findings block (`parse_block` ignores keys it does not check, so the merge accepts it):

- `peer` when the line's flattened `anchor` or `anchor2` shares a common substring of at least 12 characters with the flattened anchor of any fact **delivered to that reviewer**, or when any entry of its `refs` or any path-shaped token (`path` or `path:line`) in its `claim` names a delivered item path (line suffixes ignored);
- `own` otherwise, and always `own` for non-receivers, and always `own` when the receiver's final report comes from the isolated attempt 2 (R-44), which never saw a fact; that receiver is then listed in `isolated_for`.

The merge input for each reviewer is `<rid>.final.md`: the H2-normalised report with tags. The sweeper is never a merge input; the resolution lists exactly the 3 reviewers (R-18).

### 2.7 Timing (MR 2.0 timing rules, R-41..R-45, D-2)

All values come from `config/values/<panel>/<pkg>.json`, frozen before the first arm (R-30), and are baked into the settings and the launch arguments; nothing is recomputed during an arm.

| Quantity | Formula | EL2 at planning values (B 116, luna 6.4/6.4) |
|---|---|---|
| `panel_finish_at_s` | `1.35 B_f - turn_p90_crit - T_report_p90_crit` | 143.8 s |
| `k` | `max(0, min(2, floor((panel_finish_at_s - E_recv - 2) / (2 x turn_p90_recv))))` (D-2) | floor((143.8 - 116 - 2) / 12.8) = 2 |
| `sweeper_kill_s` | `panel_finish_at_s - 2 x turn_p90_recv` | 131.0 s |
| `hang_s` | `1.5 B_f` | 174 s |
| finish-signal bound | `1.35 B_f` | 156.6 s |
| planned end of the slowest receiver | `E_recv + 2 + 2k x turn_p90_recv` | 143.6 s (k = 2), 130.8 s (k = 1) |

On EL2, `E_recv = B_f` and the receiver is the critical role, so `k` equals R-42's `floor((0.35 B - 2 - turn_p90 - T_report_p90) / (2 x turn_p90))`; the unit tests check both forms give the same value on every R-42 test case. `k = 0` means the package is isolated for this design and is reported as dilution.

**Spike 4 inputs per panel and package (`values.py reduce`)**, from `n = 4` A1 runs (`PANEL_COLLAB=0`, hang guard off, i.e. `timeout 3000` as today). `spike4-values.sh` passes the fixed file `config/spike4-values.json` (`hang_s: 3000`, `k: 0`, `panel_finish_at_s: 3000`, `source: "spike4-bootstrap"`) as `--values`, so the launcher needs no extra switch; rows made with it are stamped `planning: true` and never counted.

- `B_f`: median over runs of the package's `elapsed_s`.
- `E_recv`: median over runs of the slowest luna's end minus T0.
- `turn_p90_*`: the 90th percentile of turn durations of that model in that package, a turn being the gap between consecutive `assistant` entries' `timestamp` in the persisted session transcript (`~/.claude/projects/<slug>/<session_id>.jsonl`).
- `T_report_p90_*`: the 90th percentile of the last turn (the one that writes the report) of that model. With 4 runs this is close to the maximum of 4 (or 8 for luna); stated as a limit in section 7.
- The slowdown `s` of each brief on the critical role (R-45): 0 by construction here (receivers' briefs are unchanged); recorded anyway.

### 2.8 Contamination safeguards and audits (MR (e), R-07, R-09, section 4 guard 5)

| Safeguard | How it is enforced | Where checked |
|---|---|---|
| Shared content is repo facts only | validator rules 3-10; `cmd` allowlist | `validate-msg.sh`, `test_validate_msg.py` |
| Withheld: ember's findings, severities, claims, verdict | The sweeper is a fresh session given no report path; the board has no free-text field | `audits.py`: sweeper transcript path audit |
| No zero counts as counts | render rule 2.5.3 | `test_render_fact` |
| Independent first pass | seal snapshot before the first delivery, fail closed | receiver hook step 6; `test_receiver_hook` |
| Peer tagging | `tagger.py` (2.6) | `test_tagger` |
| First-hand evidence | for each `peer` line of a receiver: `first_hand = true` if, after the delivery call index, the receiver's own transcript has a Read of a cited item path, or a re-run (a Bash command whose flattened text equals the fact's flattened `cmd`, or a Grep with the same pattern and path) | `collab_metrics.py`; `peer_lines_first_hand / peer_lines` in `collab.json` |
| Re-run mismatch | for each exact re-run: mismatch if any fact item path is absent from the re-run's `tool_result` text, or, for a fact with `n >= 1`, the re-run's output line count (or the integer printed by a `wc -l` command) differs from `n` | `collab_metrics.py`: `reruns`, `rerun_mismatches`; arm stop above 10% in `summarize_arm.py` |
| Unrun commands | a sweeper fact whose `cmd` does not equal, flattened, any Bash command in the sweeper transcript | `collab_metrics.py`: `cmd_unrun` (reported) |
| No ground truth on the board | every `board.jsonl` line, every rendered delivery and both brief templates contain no `plan_quote` substring of 12+ characters from the three `ground-truth.json` files | `audits.py run` (scoring stage only) |
| No ground truth or other outputs read | Only the **tool inputs** of `assistant` entries are audited (Read `file_path`, Bash `command`, Grep/Glob `path` and `pattern`), never the whole transcript: hook entries, the expanded `/sc:spec-panel` command text and tool outputs legitimately contain words such as "scoring" or the hook's own path. A violation is a tool input naming a path that matches `*/ground-truth*.json`, `*/20261111-a1/*`, `*/20261113-collab/*` (except the sweeper's calls of its own `B/bin/panel-post`), `*/.dev/reflect/*`, or, for reviewers only, `SBR/board/*` | `audits.py run`; `test_audits` includes a clean fixture transcript with a hook entry carrying the R2 hook command and a Read of a sandbox file whose text contains "scoring", which must pass |
| Catalogue clean | `catalogue.json` has no `plan_quote` substring of 12+ characters and no path named in any ground-truth description (R-07) | `audits.py catalogue` (Gate 0) |
| Read-only | clean `git status`, unchanged candidate and source sha256 | `audits.py run` |

A package with any audit violation gets `audit_ok:false`; the launch exits non-zero and the row is flagged; files are quarantined in place (R-26), never deleted.

### 2.9 `collab.json` (R-23), one per package, both arms

Every field of R-23 is present. Fields that belong to other designs are `null`. Types: counts are integers, times are ms since epoch or `null`, rates are floats or `null`.

```json
{"schema":"collab/1","arm":"F4|A1","panel":"EL2|SL2|HL2","row":"<row>","pkg":"<pkg>","values_sha256":"<hex>",
 "k":2,"panel_finish_at":0,"deal_r":0,"deal_c":null,
 "reviewers":{"<rid>":{"role":"receiver|nonreceiver","msgs_sent":0,"msgs_received":0,"first_delivery_t":null,"seal_t":null,
   "resume_fallback":null,"phase2_s":null,"stop_blocks":0,"hook_calls":0,"hook_error":0,"hook_ms_p95":null,"reask_s":0,
   "attempts":1,"retry_s":0,"retry_isolated":false,"phase2_timeout":null,"p2_lines_salvaged":null,"n_planned":null,"n_launched":null,
   "finish_signal_t":null,"finish_would_fire":false,"hang_kill":false,"snapshot_missing":false,"late":0,"not_delivered_cap":0,"not_delivered_other":0,
   "peer_lines":0,"peer_lines_first_hand":0,"reruns":0,"rerun_mismatches":0,"dropped_lines":0,"model_ok":true,"output_tokens":0,"end_t":0}},
 "sweeper":{"model":"muse-ember-1.0","model_ok":true,"start_t":null,"end_t":null,"skipped_late":false,"facts_posted":0,
   "facts_harvested":0,"facts_rejected":0,"over_cap":0,"witness_facts":0,"cmd_unrun":0,"output_tokens":0},
 "slots":[{"fact":"f-0","i":0,"recipient":"t4-1","slot_type":"fact","card_form":null,"delivered":true,"late":false}],
 "elapsed_s":0.0,"baseline_elapsed_s":null,"overhead_pct":null,"own_line_jaccard":null,"pairwise_task_jaccard":null,
 "echo_rate":null,"ledger_rows":0,"isolated_for":[],"slo_breach":false,"audit_ok":true}
```

- `finish_would_fire` (both arms): a receiver whose `end_t` is later than `T0 + panel_finish_at_s` (in A1 nothing acts on it).
- `baseline_elapsed_s` is `B_f` from the values file; `overhead_pct = 100 x (elapsed_s / B_f - 1)`.
- `own_line_jaccard`: map each `origin:"own"` line's anchor to a Task id (the nearest heading above its located line, via `findings.locate`, that matches `^#+\s*(Task|T)\s*(\d+)`), build each reviewer's Task set, and take the mean pairwise Jaccard. `pairwise_task_jaccard`: the same over all lines (descriptive only).
- `echo_rate`: among receiver lines tagged `peer`, the share whose flattened anchor equals a delivered fact's flattened anchor; `null` when there are no peer lines.
- `ledger_rows`: `jq '.rows|length' ledger.json` after the merge (filled by `launch-panel.sh` after step 3).
- `slo_breach`: any `hang_kill`, or `elapsed_s > 1.5 B_f`.

### 2.10 Alarms and stop rules (R-24, R-25, MR 4 "Abort an arm")

Computed by `summarize_arm.py` over one arm's results rows, with the same panel's A1 rows as the reference. None uses ground truth.

| Alarm | Fires when | Effect |
|---|---|---|
| `CONVERGENCE` | a run's mean `own_line_jaccard` exceeds the A1 mean + 0.15, or its ledger rows fall more than 20% below the A1 mean | arm passes the independence guard if it fires in at most 2 of 12 runs (3 of 6 at the interim look stops the arm) |
| `ECHO` | `echo_rate` above 0.60 | logged per package; reported |
| `SNAPSHOT` | `snapshot_missing` in more than 50% of the arm's receiver runs | stop the arm; fix the hook |
| Re-run mismatch | `sum(rerun_mismatches) / sum(reruns)` above 0.10 | stop the arm |
| SLO budget | more than 1 package in 12 with `elapsed_s > 1.35 B_c` or `slo_breach` | stop the arm |
| Wrong blockers | mean wrong blockers above the A1 mean + 1.0 (needs judge scores) | fail the arm (MR 4 rule 3) |
| Flood | facts posted equal to the cap in most packages with low uptake (`facts_delivered`/`k` below 0.5) | runbook: tighten the sweeper brief to "only files outside the plan's named list"; reported, not a stop |

## 3. The three panels

The source designs F4 for ember + 2x luna only (MR slot 2, baseline EL2). The owner will test three panels. Reviewer ids follow the study's existing rows (`merge-b11.sh` for sonnet, batch 9 for haiku `t2-1`); the two lunas are `t4-1` (receiver index 0) and `t3-1` (receiver index 1) on every panel, so receiver logic is identical across panels.

| Role | EL2: ember + 2x luna | SL2: sonnet + 2x luna | HL2: haiku + 2x luna |
|---|---|---|---|
| Reviewer, non-receiver | `t2b-1` = `muse-ember-1.0` | `t1b-1` = `claude-sonnet-5-5` | `t2-1` = `claude-haiku-5-5` |
| Reviewer, receiver 0 | `t4-1` = `gpt-6-luna` | `t4-1` = `gpt-6-luna` | `t4-1` = `gpt-6-luna` |
| Reviewer, receiver 1 | `t3-1` = `gpt-6-luna` | `t3-1` = `gpt-6-luna` | `t3-1` = `gpt-6-luna` |
| Sweeper (helper, not merged) | `sw-1` = `muse-ember-1.0`, a **second** ember session started when `t2b-1`'s attempt 1 exits (source behaviour) | `sw-1` = `muse-ember-1.0` helper started at T0 (**adaptation D-1**) | `sw-1` = `muse-ember-1.0` helper started at T0 (**adaptation D-1**) |
| Critical-path role (sets B; its p90s feed `panel_finish_at_s`) | luna | sonnet | haiku |
| Receiver timing (`E_recv`, `turn_p90_recv`) | luna (equals the critical role, so `k` is R-42 exactly) | luna (**adaptation D-2**) | luna (**adaptation D-2**) |
| Hooks | lunas only (D-3); ember launches as in A1 | lunas only; sonnet as in A1 | lunas only; haiku as in A1 |
| Judge | `claude-opus-5-5` through the unchanged `judge-one.sh` | same | same |

**Planning arithmetic per panel** (planning B from MR 2.0; sonnet and haiku `T_report_p90` have no source value, so their mean turn is used and labelled planning; luna `E_recv` planning = luna median wall 102 s from MR 2.0's timing table). Spike 4 replaces all of it.

| Value | EL2 | SL2 | HL2 |
|---|---|---|---|
| B (planning) | 116 s | 273.7 s | 238 s |
| `turn_p90_crit` / `T_report_p90_crit` | 6.4 / 6.4 s (luna) | 14 / 14 s (sonnet) | 23 / 23 s (haiku) |
| `panel_finish_at_s` | 143.8 s | 341.5 s | 275.3 s |
| `E_recv` | 116 s (= B) | 102 s | 102 s |
| `k` | 2 (1 if `T_report_p90` = 11 s; central row k = 1) | min(2, floor((341.5 - 102 - 2) / 12.8)) = 2 | min(2, floor((275.3 - 102 - 2) / 12.8)) = 2 |
| `sweeper_kill_s` | 131.0 s | 328.7 s (the sweeper ends on its own long before; facts after the lunas end are `late`) | 262.5 s |
| Planned end of the slowest luna | 130.8 s (k = 1), 143.6 s (k = 2) | 129.6 s (k = 2), off the critical path | 129.6 s (k = 2), off the critical path |
| Planned panel elapsed | 130.8 s (+12.8%) / 143.6 s (+23.8%) | 273.7 s (+0%): sonnet still ends last | 238 s (+0%): haiku still ends last |
| Finish-signal bound / hang guard | 156.6 s / 174 s | 369.5 s / 410.6 s | 321.3 s / 357 s |
| Extra output tokens | sweeper session (MR estimates +45% on EL2 including luna's acted-on facts) | ember helper session plus luna's acted-on facts; not derived (UNVERIFIED) | same as SL2 (UNVERIFIED) |

**What each adaptation changes, stated plainly.**

- **D-1 (SL2, HL2 sweeper = ember helper at T0).** The panel the owner names stays the three reviewers whose reports are merged; ember adds only facts and is never merged. Its tokens are counted in the row's output tokens (section 5.4) so the cost comparison with the isolated baseline is honest. Facts should arrive earlier than on EL2 (no 41 s wait), which favours delivery before the lunas' 6th call gate opens at about 38 s. To test a sweeper drawn from the panel itself, set `SWEEPER_MODEL=claude-sonnet-5-5` or `claude-haiku-5-5`; the launcher accepts only the five allowed models and records the sweeper model in the row.
- **D-2 (k from the receiver).** On SL2 and HL2 the lunas' added turns end long before the critical-path reviewer, so the design adds about 0 s of panel elapsed. The binding limit there is not the +35% cap but whether a fact arrives before luna's last tool call (`late`).
- **D-3 (hooks on receivers only).** No "finish now" ever reaches sonnet or haiku, whose work the design does not change.
- **No gain estimate exists for SL2 or HL2.** The MR 2.0 gain chains are for EL2; on the other two panels results are exploratory and reported as such.

**Concurrency.** One launch runs its three packages one after the other; inside a package at most 4 sessions run at once (3 reviewers + sweeper; on EL2 at most 2 ember sessions, the sweeper and a possible ember H2 re-ask). MR 4 "Conduct" and R-28 set the caps: at most 10 concurrent runs and at most 4 ember. This design derives its own launch limit from them: at most 2 launches at once (at most 8 sessions, at most 4 ember on EL2; SL2 and HL2 launches use 1 ember each, so the 2-launch limit is conservative there). `launch-panel.sh` enforces it with `flock -n SBR/slot.1` or `SBR/slot.2` and refuses to start when both are held.

## 4. Kill switch: PANEL_COLLAB=0 (the isolated baseline)

`PANEL_COLLAB=0` runs the same panel (same reviewer ids, models, briefs, sandboxes, H1-H4, H2 re-ask, session persistence, hang guard, retry loop) and nothing else:

| Item | `PANEL_COLLAB=1` (F4) | `PANEL_COLLAB=0` (A1) |
|---|---|---|
| Board `B`, `panel-post`, `named.txt` | created | not created |
| `--settings` on the receivers | yes, attempt 1 only | never |
| Sweeper | started | never started |
| Tagger | tags against delivered facts | tags every line `own` (no deliveries exist) |
| `collab.json` | full | same schema; F4 counters 0, sweeper block `null`, `finish_would_fire` computed |
| Values file | the panel's frozen values | the same file (the hang guard and `finish_would_fire` need `B_f` and `panel_finish_at_s`) |
| Results row | `arm:"F4"` | `arm:"A1"` |

**R-05 check.** `run-reviewer2.sh --print-cmd` with `PANEL_COLLAB=0` produces an argv whose only differences from `RR:48` are, token by token: the `cd` target (R-03), the `timeout` value (R-43), the absence of `--no-session-persistence`, and the brief text (R-01 sentence and sandbox paths). The re-ask command differs further by `--resume <sid>` and `--output-format stream-json --verbose` (allowed by R-05). `test_launch_command_diff.py` asserts exactly this list and fails on any other difference. With `PANEL_COLLAB=1` the only additional token pair on a receiver's attempt 1 is `--settings <file>`; non-receivers' commands are identical to A1's.

The switch is read once by `launch-panel.sh`, recorded in `runs/<row>/panel_collab`, and passed to every child; a child never re-reads the environment.

## 5. Launch script and results row

### 5.1 `bin/launch-panel.sh`

```text
NOFALLBACK=1 [PANEL_COLLAB=1|0] [SWEEPER_MODEL=<model>] \
  bash R2/bin/launch-panel.sh --panel EL2|SL2|HL2 --row <row-name> [--packages "<pkg> ..."] [--planning-values] [--no-judge]
```

Defaults: `--packages` = the three study packages in the order `TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415`; `PANEL_COLLAB=1`; `SWEEPER_MODEL` from `panels.json`.

**Steps.**

0. **Preflight (refuse before any model call; exit 2 with the reason):** `NOFALLBACK` is `1`; `PANEL_COLLAB` is `0` or `1`; `--row` matches `^[a-z0-9][a-z0-9-]{0,40}$`; every model in the panel and the sweeper is one of `muse-ember-1.0`, `gpt-6-luna`, `claude-haiku-5-5`, `claude-sonnet-5-5`, `grok-4.7`; `jq`, `flock`, `superclaude`, `uv` are on `PATH`; `sha256sum` of `EVAL/tools/tmp-scripts/judge-one.sh`, `catalogue.json` and the brief templates match `manifest.json`; each package's values file exists and its sha256 matches `manifest.json`, unless `--planning-values` (then `planning-values.json` is used and the row is stamped `"planning":true`, which `summarize_arm.py` refuses to count); `SBR/base/<pkg>.tar` exists for each package (else run `build-sandbox.sh`); a free concurrency slot (section 3). If `runs/<row>/` exists the launch resumes: `runid`, `opaque`, `panel`, `panel_collab` and `sweeper_model` are read from the files written by the first launch (a mismatch with the current arguments exits 2), and every later step is skipped per package when its output already exists (run: `DONE`; merge: `merged-1.md`; anonymise: a label directory with `merged-anon.md`; judge: `score.json`), so a package is merged once and judged once (R-29). A package directory without `DONE` is moved to `runs/<row>/<pkg>.incomplete-<UTC>` (quarantine in place, never deleted), and so are its sandbox `SBR/sb/<runid>/<pkg>` and its board `SBR/board/<runid>/<pkg>` (each to `<pkg>.incomplete-<UTC>` beside it); the package is then re-run on a freshly built sandbox and an empty board, so no old seal, delivery, call counter or fact carries over. `test_preflight.py` covers a resume after an interruption between merge and judge: no second merge, no second label, one `score.json`.
1. On a first launch only: create `runid` and `opaque` and write `runs/<row>/{runid,opaque,panel,panel_collab,sweeper_model,started_at}`.
2. For each package, in order: `run-package.sh` (section 2.2). A non-zero exit marks the package INVALID and the launch continues with the next package.
3. **Merge**, per valid package, with the same arguments as `merge-b11.sh:34`:

   ```text
   superclaude review merge --ledger runs/<row>/<pkg>/ledger.json --doc EVAL/<pkg>/candidate.md --round 1 \
     --report <rid>=runs/<row>/<pkg>/reviews/<rid>.final.md (x3) --resolution runs/<row>/<pkg>/resolution.json \
     --out runs/<row>/<pkg>/merged-1.md > runs/<row>/<pkg>/merge-stdout.txt 2>&1
   ```

   (Every path above is passed absolute: `R2/runs/...` and `EVAL/...`.)

   `resolution.json` is built exactly as `merge-b11.sh:17-25` does, from `EVAL/<pkg>/resolution-live7.json`, with this panel's three reviewers and their `ALIAS`/`TIER` values from `merge-b11.sh:11-12` (`t2-1` haiku uses `tier2`/`claude-gw-tier2[1m]`). A refused merge marks the package INVALID (no automatic re-run; MR's single re-ask already happened in H2).
4. **Anonymise**, per merged package: `opaque` = 12 random hex characters (created once per row in step 1), `results/keys/<opaque>.json` = `{"row","runid","arm"}`; `anon.sh --merged runs/<row>/<pkg>/merged-1.md --out-dir scoring/<opaque>/<pkg>` (section 5.2).
5. **Judge** (unless `--no-judge`), the three packages in parallel: `judge.sh <opaque> <pkg> <label>`. A judge failure is retried once; a second failure leaves the package unscored (`score:null`), never a guessed score.
6. **Audits**: `audits.py run --pkgdir runs/<row>/<pkg>` for each package (contamination, read-only).
7. **Results row**: `results_row.py --row <row> --opaque <opaque> --out results/<row>.json`.
8. Exit 0 only when all three packages are valid, merged, judged and `audit_ok`; else exit 1, with the reasons in `results/<row>.json` `"invalid"`.

Each step writes a line `STEP <n> <pkg> OK|FAIL <reason> <UTC>` to `runs/<row>/launch.log`. No step waits on a single blocking command for more than the package hang guard plus 60 s, apart from the judge, which keeps `judge-one.sh`'s own `timeout 900`.

### 5.2 Anonymiser and judge call (R-29, D-7)

`anon.sh` reproduces `anon-b11.sh` and adds the stripping R-29 requires:

1. Label: random from `{Q,R,S,T,U,V}` not already used in `scoring/<opaque>/<pkg>/`; `label-key.json` = `{"label","opaque"}` beside it (the judge is told to read only the three files it is given).
2. `sed`: `EVAL` → `<EVAL>`; `R2` → `<EVAL>`; `SBR` → `<SANDBOX>`; reviewer ids (`grep -oE '\bt[0-9a-z]+-[0-9]+\b'`, sorted) → `R1..Rn`; the `candidate:` line and `report <path>` redactions of `anon-b11.sh:24-25`.
3. Strip collaboration traces: every `"origin":"own"` / `"origin":"peer"` key (with its comma); the tokens `f-<digits>`, `sw-1`, `hv-1`, `panel-msg/1`, `panel-post`, `board.jsonl`, any path containing `/board/`; and the rendered-delivery phrases `Search result to check yourself` and `not a finding; no conclusion attached`.
4. Self-check: `grep -cE '"origin"[[:space:]]*:|/board/|panel-(msg|post)|\bf-[0-9]+\b|\bsw-1\b|\bhv-1\b|evalsb-collab|Search result to check|<row>|<runid>'` (with the row name and run id substituted) on `merged-anon.md` must be 0; otherwise exit 4 and the package is not judged. Only the key form of `origin` is checked, because candidates legitimately contain words such as "original" (the designSpec candidate has 7 occurrences of "origin"). `20261113-collab` is not in the list because the judge brief itself names the scoring path (D-7, risk K-13).
5. Every `report \S+` token is redacted to `report <redacted>` (not only `report <EVAL>/...`), because `ledger.py:423` writes the path exactly as passed; the merge is given absolute paths.

`judge.sh` then runs the unchanged judge:

```text
bash EVAL/tools/tmp-scripts/judge-one.sh "../../../../20261113-collab/r2-idle-shift-sweeper/scoring/<opaque>" "<pkg>" "<label>"
```

`judge-one.sh` computes `D=$EVAL/arms/scoring/combos/$C/$P/$L`, which resolves through the existing directory `EVAL/arms/scoring/combos` to `R2/scoring/<opaque>/<pkg>/<label>`, so `score.json`, `judge.json` and `judge.err` land in `R2/`. The `combo` field of `score.json` holds the relative string; `results_row.py` ignores it and keys by `opaque`. `judge-one.sh` reads ground truth from `EVAL/<pkg>/ground-truth.json` (read-only).

### 5.3 Per-batch API-error audit (R-29)

After step 5, `results_row.py` greps every `judge.json` result text and every `score.json` for `API Error`; any hit sets `judge_api_error:true` for that package and its score is excluded. Re-judging deletes nothing: the operator moves the label directory to `<label>.api-error-<UTC>`, runs `anon.sh` again (new label, new `merged-anon.md`), then `judge.sh` with that label.

### 5.4 Results row (`results/<row>.json`)

Definitions follow `EVAL/analysis/final-table.py:4-5, 33-36`: "defect-rich" = designSpec (10 GT items) + alias (4); control = design (2). Real blocking = judge-blocking AND `blocking_in_implement == true` in the ground truth.

```json
{"schema":"r2-results/1","row":"<row>","arm":"F4|A1","panel":"EL2|SL2|HL2","panel_collab":1,
 "models":{"t2b-1":"muse-ember-1.0","t4-1":"gpt-6-luna","t3-1":"gpt-6-luna"},"sweeper_model":"muse-ember-1.0",
 "planning":false,"values_sha256":{"<pkg>":"<hex>"},"opaque":"<hex>","started_at":"<UTC>","finished_at":"<UTC>",
 "found_14":0,"real_blocking_8":0,"judge_blocking":0,"wrong_blockers":0,
 "control_found_2":0,"control_wrong_blockers":0,
 "output_tokens":{"total":0,"reviewers":0,"sweeper":0,"reask":0},
 "elapsed_s":{"<designSpec>":0.0,"<alias>":0.0,"<design>":0.0},
 "overhead_pct":{"<pkg>":0.0},
 "per_package":{"<pkg>":{"gt_covered_any":["GT1"],"gt_covered_blocking":[],"wrong_blockers":0,"ledger_rows":0,
   "label":"Q","score_ok":true,"judge_api_error":false,"valid":true,"audit_ok":true}},
 "collab":{"k":{"<pkg>":2},"facts_posted":0,"facts_harvested":0,"facts_rejected":0,"over_cap":0,"witness_facts":0,
   "facts_delivered":{"t4-1":0,"t3-1":0},"late":0,"not_delivered_cap":0,"isolated_for":{"<pkg>":[]},
   "snapshot_missing":0,"finish_signal_fired":0,"finish_would_fire":0,"hook_error":0,"hook_ms_p95":null,
   "peer_lines":0,"peer_lines_first_hand":0,"reruns":0,"rerun_mismatches":0,"cmd_unrun":0,
   "echo_rate":{"<pkg>":null},"own_line_jaccard":{"<pkg>":null},"sweeper_start_t_s":{"<pkg>":null},
   "hang_kill":0,"slo_breach":0,"retry_isolated":0,"reask_count":0,"dropped_lines":0},
 "invalid":[]}
```

| Field | Formula |
|---|---|
| `found_14` | `|gt_covered_any|` designSpec + alias |
| `real_blocking_8` | count of ids in `gt_covered_blocking` (designSpec + alias) whose GT item has `blocking_in_implement: true` |
| `judge_blocking` | `|gt_covered_blocking|` designSpec + alias |
| `wrong_blockers` | `wrong_blockers` designSpec + alias |
| `control_found_2` / `control_wrong_blockers` | the same two fields on the design package |
| `output_tokens.total` | sum of `output_tokens_all` over every reviewer attempt, every re-ask and the sweeper |
| `elapsed_s` | per package, from `collab.json` (2.2 step 5) |
| collaboration counters | sums or per-package values from `collab.json` (2.9); all present and 0 or `null` in A1 rows |

## 6. Test plan

All automated tests run with `uv run pytest R2/tests -q` from `REPO`. Shell components are tested from pytest through `subprocess.run` (one runner, no bats dependency). No automated test calls a real model: `tests/fakes/claude` stands in for `claude -p` and is put first on `PATH` by `conftest.py`; every fixture is synthetic (a small fake candidate, source and repo), and no test reads the study's `ground-truth.json` files except the R-07 catalogue check, which reads them and asserts only on absence. Tests marked `@pytest.mark.live` (Gate 0 and smoke) are skipped unless `R2_LIVE=1`.

### 6.1 Unit tests

| File | Component | Cases (each a separate test) |
|---|---|---|
| `test_validate_msg.py` | `lib/validate-msg.sh` (R-06, R-08, D-4) | accept: a full M1 fact; an M2 count fact with `n: 0`; a witness M9 fact with `source.md:12`. Reject, each with its reason code: 601-byte line (`too_long`); `claim` key (`forbidden_key:claim`); `severity` key; `category` on a fact (`forbidden_key:category`); `foo` key (`unknown_key:foo`); `kind:"card"` (`bad_kind`); `move:"M3"` (`bad_move`); anchor of 11 flattened chars; anchor not in the candidate; anchor matching only after whitespace flattening (accepted); 9 items; `/etc/passwd`; `../x`; a missing path; `path:9999` beyond the file; second witness fact (`second_witness`); `n: -1`; each forbidden `cmd` character and verb (`rm`, `sed -i`, `find -delete`, `grep x > f`, `grep x; ls`, `$(...)`, `#`); the 2k+1-th sweeper post (`over_cap`); a post after `finish_ms` (`after_finish`). |
| `test_panel_post.py` | `B/bin/panel-post` | builds `id`, `t`, `from`, `to`, `run`; unknown flag rejected; items ranked and trimmed to fit 600 bytes; prints `posted f-N`; concurrent posts from 8 processes produce 8 distinct ids and 8 intact lines (`flock`). |
| `test_receiver_hook.py` | `hooks/receiver-hook.sh` (R-19, R-20, R-41) | no delivery on calls 1-5; no seal while no fact is available; seal written and hashed in the same call as, and before, the first delivery (`seal` logged before `deliver`), never before call 6; deal with `r = 0`: board lines 0..3 go to receivers 0,1,0,1, with `r = 1` to 1,0,1,0; at most `k` deliveries (k = 1 and k = 2); at most one per call; rank order (unnamed test before root doc before other, ties by index); `n == 0` rendered without a count; rendered text at most 1,500 chars; after `finish_ms`: one finish text, then nothing, and no delivery; `Read` calls append to `opened.txt`; output is valid JSON with `hookEventName: PostToolUse`; the hook runs with `env -i` (empty environment) and still delivers a seeded fact (R-21). |
| `test_harvest_hook.py` | `hooks/harvest-hook.sh` (R-18) | grep over `tests/` gives an M1 fact with the unopened unnamed test first; a path in `named.txt` or `opened.txt` is excluded; a path already on the board is excluded; a `find ... -delete` command posts nothing; a `Read` tool call posts nothing; the shared 2k cap holds across both writers: with k = 1, one `panel-post` fact plus one harvested fact fill the cap and a third post of either kind is rejected `over_cap`; it never prints context. |
| `test_render_fact.py` | `lib/render-fact.sh` | fixed template lines; catalogue text equals `catalogue.json`; no `n` line for `n == 0`; trimming order. |
| `test_h2_normalize.py` | `py/h2_normalize.py` (R-02) | a 250-character anchor is truncated to a 200-character prefix and the line parses (not dropped) and is still located by `findings.locate` in the fixture candidate; a 400-character claim is cut to 300; a bad severity sets `needs_reask: true` and lists the error; a clean report gives `block_ok: true` and no change. |
| `test_tagger.py` | `py/tagger.py` (R-10) | a line with a 12-character overlap with a delivered anchor is `peer`; 11 characters is `own`; a `refs` entry naming a delivered item is `peer`; a `claim` naming `tests/x.py:3` when `tests/x.py` was delivered is `peer`; a fact on the board but not delivered to this reviewer does not tag; non-receivers are all `own`; the tagged report still parses with `parse_block` and keeps one block. |
| `test_values.py` | `py/values.py` (R-41, R-42, D-2) | R-42 cases: B 116 with 6.4/6.4 gives k = 2; `T_report_p90` 11.0 gives k = 1; B 100 gives k = 1 only when `T_report_p90 <= 13.8`; SL2 with turn 14 gives k >= 1 only when `T_report_p90 <= 51.8`. D-2 equals R-42 whenever `E_recv = B` and receiver = critical role (property test over a grid); HL2 planning gives k = 2; `panel_finish_at_s` 143.8, `sweeper_kill_s` 131.0, `hang_s` 174 at EL2 planning values; k is never negative or above 2; the Spike 4 reducer computes turn durations from a fixture transcript with known timestamps. |
| `test_collab_metrics.py` | `py/collab_metrics.py` (R-20, R-23, R-25) | schema: every R-23 field present; `late` for a fact whose `t` follows the receiver's last call; `isolated_for` when 0 delivered; `facts_delivered <= k`; first-hand true for a Read of the cited path after delivery, false before delivery; re-run equal/unequal output gives 0/1 mismatch; `cmd_unrun` counted; `echo_rate` on a fixture; own-line Jaccard ignores `peer` lines (a fixture where peer lines raise all-line Jaccard but not own-line Jaccard); `finish_would_fire` true when a receiver ends after `panel_finish_at`. |
| `test_summarize_arm.py` | `py/summarize_arm.py` (R-24, R-25) | `CONVERGENCE` fires above A1 + 0.15 and on a 21% ledger-row drop, not at 19%; independence guard passes at 2 of 12 and fails at 3; `ECHO` above 0.60; `SNAPSHOT` above 50%; re-run mismatch 11% stops the arm, 10% does not; SLO budget: 2 breaches in 12 stops; wrong blockers: an arm mean of A1 + 1.01 fails the arm, A1 + 1.0 does not (MR 4 rule 3); flood: facts at the cap with uptake below 0.5 is reported and does not stop the arm; planning rows are refused. |
| `test_results_row.py` | `py/results_row.py` (5.4) | from fixture `score.json` files and a fixture GT: `found_14`, `real_blocking_8` (a judge-blocking item with `blocking_in_implement: false` is not counted), `judge_blocking`, `wrong_blockers`, control fields, token sum including sweeper and re-ask; a missing score gives `null`, never 0; `API Error` in a judge result sets `judge_api_error`. |
| `test_anon.py` | `bin/anon.sh` (R-29) | reviewer ids replaced; `origin` keys, fact ids, `sw-1`, `/board/` paths and the delivery phrases removed; every `report <path>` redacted, absolute or relative; an anchor quoting "original" passes the self-check; the self-check exits 4 when a planted trace (an `"origin":` key, the row name, the run id) survives; label is one of Q-V and not reused. |
| `test_judge_wrapper.py` | `bin/judge.sh` (D-7) | with a stub `judge-one.sh` copy whose sha256 is pinned in a fixture manifest, the computed `D` resolves under `R2/scoring/<opaque>/...` (asserted with `realpath -m`); a sha mismatch exits 5 and runs nothing. |
| `test_audits.py` | `py/audits.py` (2.8, R-07) | a board line containing a 12-character `plan_quote` substring is a violation (synthetic GT fixture), 11 characters is not; a reviewer transcript reading `ground-truth.json` is a violation; a sweeper transcript naming `/reviews/` is a violation; a dirty sandbox `git status` is a violation; a changed candidate sha256 is a violation; the real `catalogue.json` passes against the three real ground-truth files (the only test that reads them). |
| `test_launch_command_diff.py` | `run-reviewer2.sh --print-cmd` (R-05) | with `PANEL_COLLAB=0` the token diff against `RR:48` (parsed from the file at test time) is exactly: `cd` target, `timeout` value, missing `--no-session-persistence`, brief; with `PANEL_COLLAB=1` a receiver adds only `--settings <file>` and a non-receiver adds nothing; no fallback code path exists (`grep -cE 'FALLBACK\[|fallback\.log' run-reviewer2.sh` is 0). The test drives the two cases by calling `run-reviewer2.sh --print-cmd` without and with `--settings` (children never read `PANEL_COLLAB`). |
| `test_build_sandbox.py` | `bin/build-sandbox.sh` (R-03) | on a throwaway fixture git repo: the four leak directories are absent from the tar; a missing base SHA exits 2; a second run with the same SHA is a no-op. |
| `test_preflight.py` | `launch-panel.sh` step 0 | refuses without `NOFALLBACK=1`; refuses `glm-5.3`, `Qwen3.8-max`, `claude-opus-5-5` as a reviewer or sweeper; refuses a values file whose sha256 differs from the manifest; refuses a bad row name; refuses when both concurrency slots are held. |

### 6.2 Fault injection (one test per failure mode; all with the fake `claude`)

| Failure mode (MR (h), R-22, R-43, R-44) | Injection | Pass condition |
|---|---|---|
| Snapshot not written | `B/snap` made read-only (`chmod 500`) before call 6 | `snapshot_missing` logged, 0 deliveries for that receiver for the whole run, review completes, other receiver unaffected |
| Snapshot hash fails | `B/snap/<rid>.sha256` pre-created as a directory, so writing the hash fails | same as above |
| Corrupt board line | a non-JSON line appended to `board.jsonl` by hand | `hook_error` logged, hook exit 0, review completes (R-22) |
| Hook crashes | baked `--jq` points to a missing binary | hook prints nothing, exits 0; `hook_error` logged |
| Sweeper floods | fake sweeper posts 3k facts | posts beyond 2k rejected `over_cap`; each receiver gets at most `k` |
| Facts after luna finished | fake sweeper posts after the receiver's last tool call | fact logged `late`, package listed in `isolated_for` for that receiver when it got none |
| Receiver cites an unrun fact | fake receiver report cites a delivered path with no Read or re-run | `peer_lines_first_hand < peer_lines` |
| Re-run mismatch | fake receiver re-runs the fact's command and gets different output | `rerun_mismatches` incremented; an arm fixture at 11% stops |
| Ember review ends late | fake ember `t2b-1` sleeps until after `sweeper_kill_s - 10` | sweeper not started, `sweeper_skipped_late: true` |
| Sweeper overruns | fake sweeper sleeps past `sweeper_kill_s` | killed within 1 s of the computed time (exit 124 logged) |
| Sweeper misrouted | fake sweeper reports `message.model = gpt-6.1-terra` | sweeper `model_ok: false`, package INVALID, launch exit 1 |
| Reviewer misrouted | fake luna reports another model twice | reviewer INVALID; no fallback model is tried (no second model in any meta) |
| A luna hangs | fake luna sleeps forever | killed at `T0 + hang_s` (within 1 s), `hang_kill: true`, `slo_breach: true`, in both `PANEL_COLLAB=1` and `0` (R-43) |
| Block check fails, retry | fake luna attempt 1 has no findings block | attempt 2 runs without `--settings` (asserted on the fake's recorded argv), `retry_isolated: true`, no delivery in attempt 2, `elapsed_s` covers both attempts (R-44) |
| H2 re-ask | fake report with a bad severity line | one `--resume` call with `stream-json --verbose`, `reask_s > 0`; a second bad line after the re-ask is counted in `dropped_lines` |
| Re-ask has no time | deadline minus now below `6 + turn_p90` | no re-ask; invalid lines dropped and counted |
| Re-ask hangs | fake `claude --resume` sleeps forever, in both switches | killed at the package hang deadline (within 1 s), `hang_kill: true`, `slo_breach: true`, `elapsed_s` includes it |
| Wrong blockers rise | fake lunas mark every line that cites a delivered fact `blocking: true`; fixture `score.json` files give the arm a wrong-blocker mean above A1 + 1.0 | `summarize_arm.py` fails the arm with reason `wrong_blockers` |
| Resume after interruption | launch killed after the merge of package 1 and before its judge; launch run again | package 1 is not re-run or re-merged, keeps its `runid`, `opaque` and label, and gets exactly one `score.json` |
| Resume of an unfinished package | launch killed while package 2 runs (after a delivery); launch run again | package 2's old run directory, sandbox and board are moved to `*.incomplete-<UTC>`; the re-run starts with call counters at 0, no seal, no delivered list and an empty board |
| Finish signal | fake clock: receiver keeps calling tools past `finish_ms` | exactly one finish text; no delivery after it; `panel-post` prints `refused: finish` |
| Environment cleared | hook run under `env -i` | delivery still happens (R-21) |
| Merge refused | all three fake reports without a block | package INVALID, no anonymise or judge step for it |
| Anonymiser leak | planted `"origin":"peer"` in the merged report after stripping is disabled in a test copy | exit 4, package not judged |
| Judge file changed | fixture manifest pins a different sha | `judge.sh` exit 5, nothing judged |

### 6.3 Gate 0 spikes this design depends on (R-27); each records PASS or FAIL in `spikes/RESULTS.md`

| Spike | Script | What it runs | PASS when |
|---|---|---|---|
| S0 hooks | `s0-hooks.sh` | one real `claude -p` per model (`muse-ember-1.0`, `gpt-6-luna`) in a package sandbox with a receiver `--settings` file and a pre-seeded board | the hook fires on every tool call (metrics `call` count equals the transcript's tool_use count), the snapshot exists with its sha256 before the first delivery, the delivered text appears in the transcript, the hook timeout of 5 s is never hit, `hook_ms_p95 <= 500 ms`, and the active project hooks of the base sandbox's `.claude/settings.json` are listed (recorded, not judged) |
| S2 resume | `s2-resume.sh` | `--resume <sid>` with `stream-json --verbose` for each of the four reviewer models used (`muse-ember-1.0`, `gpt-6-luna`, `claude-sonnet-5-5`, `claude-haiku-5-5`) after a normal run without `--no-session-persistence` | the resumed reply comes from the same model (`model_ok`) and the stream file has lines before exit; resume start cost measured |
| S3 full chain | `s3-smoke.sh` = the smoke test in 6.4 | | see 6.4 |
| REQ-S3 act rate | `reqs3-actrate.sh` | inject via PostToolUse `additionalContext` "run `ls /tmp/panel-probe`" into ember and luna sessions, 5 runs each; and inject the finish text | rate at which the next tool call runs it, and rate of finishing within one turn after the finish text, are recorded (no threshold: these rates replace the planning act rates, R-47) |
| Spike 4 values | `spike4-values.sh <panel>` | 4 A1 runs (`PANEL_COLLAB=0`, hang guard off) per panel on the three packages; `values.py reduce` | a values file per (panel, package) with every field present, committed sha256 in `manifest.json` before the first arm (R-30) |
| H3 base check | `h3-base-check.sh` | inspects the three base tarballs | `.dev/reflect` absent in all three; the designSpec sandbox's `refs/merge-guard.md` lacks the repaired line-146 text and the other masked lines named in MR T3(a) (`merge_guard.py:256`, `pr-submit.md:81`, `refs/tiers.md:42`) differ from today's checkout; each check prints the line it compared |
| SW-1 sweeper | `sw1-sweeper.sh` | the real sweeper alone (no reviewers), 3 packages, ember | at least one fact accepted by the validator on at least 2 of 3 packages; rejection reasons recorded; sweeper `model_ok` on all 3 |
| Catalogue | `audits.py catalogue` | R-07 | no violation |

Spike 5 (study-wide H2 re-scoring) is not a dependency of this design and is not built here.

### 6.4 One-package smoke test (S3)

```text
cd REPO && NOFALLBACK=1 PANEL_COLLAB=1 bash R2/bin/launch-panel.sh --panel EL2 --row smoke-el2-collab \
  --packages TASK-WF-design-20261108-041415 --planning-values
cd REPO && NOFALLBACK=1 PANEL_COLLAB=0 bash R2/bin/launch-panel.sh --panel EL2 --row smoke-el2-iso \
  --packages TASK-WF-design-20261108-041415 --planning-values
```

then the same pair with `--panel SL2` and `--panel HL2`. Real models, one package, planning values (rows stamped `planning:true`, never counted).

### 6.5 Acceptance criteria (each PASS or FAIL)

| # | Criterion |
|---|---|
| AC-1 | `uv run pytest R2/tests -q` exits 0; every test in 6.1 and 6.2 exists and ran (no test skipped except those marked `live`). |
| AC-2 | `grep -rn "src/superclaude\|20261111-a1" R2/bin R2/py` shows only read paths (the merge command, `findings` import via `uv run --project REPO`, `EVAL/<pkg>/candidate.md`, `resolution-live7.json`, `judge-one.sh`, `ground-truth.json` in `results_row.py` and `audits.py`), and nothing under `src/` or `EVAL/` changed: a listing `find REPO/src EVAL -type f -newer <stamp>` taken against a stamp file created just before the test suite and the smoke runs is empty afterwards (`git status` is not used, because `EVAL` already holds thousands of untracked files). |
| AC-2b | Every reviewer meta of every smoke package has `dropped_lines == 0`, and every `.reask.jsonl` that exists parses with `jq -s` and gives `model_ok: true` through the `RR:50-52` filters (MR Gate 0 S3, R-02 verification). |
| AC-3 | Every Gate 0 spike in 6.3 has a PASS line in `spikes/RESULTS.md` with an evidence path, before any non-smoke row runs. |
| AC-4 | Smoke EL2 collab: exit 0; `collab.json` passes the schema; `facts_posted + facts_harvested >= 1`; at least one receiver has `facts_delivered >= 1`; every receiver with a delivery has `seal_t` earlier than its `first_delivery_t` and a matching snapshot sha256; `facts_delivered <= k` for both; `stop_blocks == 0`. |
| AC-5 | Smoke EL2 collab: `merged-1.md` lists exactly 3 reviewers; `merged-anon.md` passes the anonymiser self-check; `score.json` exists under `R2/scoring/`; nothing new exists under `EVAL/arms/`; `results/smoke-el2-collab.json` has every field of 5.4. |
| AC-6 | Smoke EL2 collab: `audit.json` `ok: true` (clean sandbox `git status`, unchanged candidate and source sha256, no transcript reading ground truth or other outputs, no ground-truth substring on the board). |
| AC-7 | Smoke EL2 isolated (`PANEL_COLLAB=0`): no board directory, no `--settings` in any recorded argv, no sweeper output, every findings line `origin: own`, collaboration counters 0, `finish_would_fire` present; `test_launch_command_diff.py` passes. |
| AC-8 | Smoke SL2 and HL2 (both switches): exit 0; `model_ok` true for every session including the ember sweeper; the row records `sweeper_model: muse-ember-1.0` and the D-2 `k`. |
| AC-9 | Every session meta in the smoke rows has `observed_model` equal to the requested model, and no fallback log exists. |
| AC-10 | `elapsed_s` of every smoke package is at most `hang_s` (no `hang_kill`), or the row says `slo_breach: true`; a smoke run is never re-run to hide a breach. |

## 7. Risks and open questions

### 7.1 Risks

| # | Risk | Consequence | Mitigation in this design |
|---|---|---|---|
| K-1 | PostToolUse hooks may not fire, or `additionalContext` may not reach the gateway models, in `claude -p` (UNVERIFIED, MR 2.0). | No delivery; F4 equals A1. | S0 and REQ-S3 gate every arm. |
| K-2 | The lunas finish at about 102-120 s. On EL2 the sweeper starts at about 41 s (later when H1 makes ember read source.md), and the deliveries open only at the 6th luna tool call (about 38 s). | Few facts arrive in time; many packages count as isolated (dilution). | `late`, `isolated_for`, `sweeper_start_t` logged; reported as dilution, never compensated (MR (h)). |
| K-3 | `T_report_p90` from 4 Spike 4 runs is close to a maximum, so `k` and `panel_finish_at_s` may be conservative or noisy. | k = 1 where k = 2 was possible, or the reverse. | Values are frozen per R-30; drift handled by the band in R-45, not by changing k. |
| K-4 | The base-commit sandbox (H3) lacks the project `.claude/{agents,commands,skills}` copies present in today's `/tmp/evalsb/repo`, so `/sc:spec-panel` resolves from `~/.claude`. | A1 and F4 differ from A0 in that respect (it is part of H). | Same for every arm of this design; S0 records which project hooks are active. |
| K-5 | H3 base = squash parent may include commits made after the plan's branch point. | A small amount of later code in the sandbox. | `h3-base-check.sh` verifies the masking lines are absent. |
| K-6 | A luna may paraphrase the delivered text ("the search shows...") in a claim, which the anonymiser cannot strip. | A judge could infer the arm. | Neutral render wording; fixed phrases stripped; residual risk reported. |
| K-7 | Luna reports almost only blocker-grade findings (MR T3(b)); facts may become wrong blockers. | Wrong blockers rise. | MR 4 rule 3 fails the arm at A1 + 1.0. |
| K-8 | `cmd` (D-4) is a string field; a model could hide words in grep patterns. | Weak free-text channel. | Allowlist, length cap 240, no comments or redirection; the ground-truth substring audit covers `cmd`. |
| K-9 | The gateway has misrouted models before (`EVAL/combos/SPEC.md` muse and glm incidents). | Wrong-model data. | `model_ok` on every session including the sweeper; `NOFALLBACK=1` and no ladder in `run-reviewer2.sh`. |
| K-10 | Statistical power: MR 4 states the plan cannot detect the central gain of any slot at n = 12. | A null result does not mean no effect. | Rows report mechanism counters (delivered, first-hand, mismatches) so the mechanism can be judged separately from reach. |
| K-11 | `judge-one.sh` hard-codes `EVAL`; the relative `C` trick (D-7) depends on `EVAL/arms/scoring/combos` existing. | Judge writes fail. | `judge.sh` checks the resolved directory with `realpath -m` and exits before calling the judge if it is not under `R2/scoring/`. |
| K-12 | On SL2 and HL2 the ember helper adds a model the named panel does not contain. | Results describe "panel + ember helper". | Recorded in every row (`sweeper_model`); `SWEEPER_MODEL` can switch to a panel member (Q-1). |
| K-13 | `judge-one.sh` puts the path of `merged-anon.md` into the judge's brief, and that path names `20261113-collab/r2-idle-shift-sweeper/scoring/<opaque>`. | The judge can tell these rows come from this harness rather than from the earlier `EVAL` study; it still cannot tell F4 from A1, which share the path form. | Compare F4 only with A1 rows from this harness, never with `EVAL` rows as if the judge were blind to the harness. |

### 7.2 Open questions for the owner (each with this design's default)

| # | Question | Default taken | What the other choice would do |
|---|---|---|---|
| Q-1 | On sonnet + 2x luna and haiku + 2x luna, should the sweeper be an ember helper (D-1) or a second session of the panel's own sonnet or haiku? | Ember helper at T0. | `SWEEPER_MODEL=claude-sonnet-5-5` (or `claude-haiku-5-5`): no outside model, but at 14 s or 23 s per turn most facts would arrive after the lunas finish, so most packages would count as isolated. |
| Q-2 | Should "finish now" go to every reviewer, as R-41 literally says, or only to the receivers (D-3)? | Receivers only. | Every reviewer: on SL2 and HL2 a slow sonnet or haiku would be cut short in the collaboration arm but not in the isolated arm, a difference that has nothing to do with collaboration. |
| Q-3 | Spike 4 run count: 4 A1 runs per panel is what this design assumes. | 4. | More runs give a steadier `T_report_p90` at the cost of 3 packages x 3 reviewers per extra run. |

### 7.3 Not verified in this design (replaced by the named spike)

Hook firing and timing (S0); `--resume` on the four models (S2); act rates on delivered text and on "finish now" (REQ-S3, replacing every planning act rate, R-47); every timing value (Spike 4); the H3 base property (`h3-base-check.sh`); whether ember uses `panel-post` correctly (SW-1); the token overhead on SL2 and HL2 (measured by the rows).

## Appendix A. Requirement traceability

| Requirement | Where designed | Where tested |
|---|---|---|
| R-01 (H1) | 2.1 brief | `test_launch_command_diff`, AC-6 transcripts |
| R-02 (H2) | 2.2 H2 | `test_h2_normalize`, 6.2 re-ask rows |
| R-03 (H3, H4) | 2.1 | `test_build_sandbox`, `h3-base-check.sh` |
| R-04 | 2.6, 5.1 step 3 | AC-5 |
| R-05 | 4 | `test_launch_command_diff`, AC-7 |
| R-06, R-08 | 2.3 | `test_validate_msg`, `test_panel_post` |
| R-07 | 2.8 | `test_audits`, catalogue spike |
| R-09 | 2.1, 2.8 | `test_audits`, AC-6 |
| R-10 | 2.5 step 6, 2.6 | `test_receiver_hook`, `test_tagger`, `test_anon`, 6.2 snapshot rows |
| R-17 | 2.4 launch, 2.2 step 4 | 6.2 "ember review ends late", "sweeper overruns"; `audits` sweeper path check |
| R-18 | 2.3, 2.4, 2.5.3 | `test_validate_msg`, `test_harvest_hook`, `test_render_fact`, 6.2 flood |
| R-19 | 2.5.1 steps 5-6 | `test_receiver_hook`, 6.2 snapshot rows |
| R-20 | 2.5.1 steps 7-9, 2.5.4, 2.8 | `test_receiver_hook`, `test_collab_metrics`, 6.2 late, first-hand, mismatch rows |
| R-21 | 2.5 settings | `test_receiver_hook` (`env -i`), S0 |
| R-22 | 2.5.1 step 1 | 6.2 corrupt line, hook crash |
| R-23 | 2.9 | `test_collab_metrics`, AC-4 |
| R-24, R-25 | 2.10 | `test_summarize_arm` |
| R-26 | 2.2 step 6 | AC-4 (board copy present) |
| R-27 | 6.3 | AC-3 |
| R-28 | 3 (concurrency), 5.1 step 0 | `test_preflight`, AC-9 |
| R-29 | 5.2, 5.3 | `test_anon`, `test_judge_wrapper`, `test_results_row` |
| R-30 | 2.7, 5.1 step 0 | `test_preflight` (values sha), Spike 4 |
| R-41 | 2.5.1 step 4, 2.7, D-3 | `test_receiver_hook`, 6.2 finish signal |
| R-42 | 2.7, D-2 | `test_values` |
| R-43 | 2.2 command | 6.2 hang rows (both switches) |
| R-44 | 2.2 retry | 6.2 retry row |
| R-45 | 2.7 Spike 4 | Spike 4 record |
| R-46 | 0.1 (no cleanup done) | none needed |
| R-47 | 6.3 REQ-S3 | REQ-S3 record |
