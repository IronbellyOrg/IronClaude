# Design: Redesign 5, Coverage Deflection (F6), implementation and test specification

Grounding: index_state: fresh (checked_at 2026-11-13T19:32:03Z, projectPath /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel); codegraph tools used: codegraph_status, codegraph_node (merge_round); Grep/Read floor for every quoted line.

## 0. Scope, sources and decisions

### 0.1 What this builds

Redesign 5 lets the reviewers that finish first (the **scouts**) steer the reviewer that is still running (the **receiver**) toward plan Tasks no scout reported a real finding on. When a scout's process exits, a harness **watcher** parses its findings block into the Tasks it covered, drops "surface" findings (artifact path, edit scope, hash, line number), and posts a **request card** naming at most k uncovered Task ids. A `PostToolUse` hook in the receiver prints the card as `additionalContext` at the receiver's next tool call. No model sends anything; cards carry Task ids only.

Short names used below:

| Name | Absolute path |
|---|---|
| `REPO` | `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel` |
| `R5` | `REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r5-coverage-deflection` |
| `EVAL` | `REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1` (read-only for this design) |
| `MR` | `REPO/.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md` (the source) |
| `SB` | `/tmp/evalsb-collab-r5` (this design's own sandbox root) |
| `DS`, `AL`, `CT` | packages `TASK-WF-designSpec-20261107-075614`, `TASK-WF-makeTheAliasOnly-20261105-051649`, `TASK-WF-design-20261108-041415` (CT is the control package) |

### 0.2 Sources read (all on disk, read for this design)

- `MR` sections 1, 2.0, 2.1, Redesign 5 (`MR:803-893`), 3, 4, 5.1, 5.2, 5.5, 5.6, 5.9, 5.10 and the unmeasured-items list (`MR:1105-1130`).
- `EVAL/tools/run-reviewer.sh` (87 lines; launch command at line 48, model check at lines 51-56, retry loop at lines 61-64, fallback ladder at lines 66-83, cost file at line 87).
- `EVAL/tools/tmp-scripts/judge-one.sh` (31 lines; it hard-codes `EVAL` at line 4 and writes into `$EVAL/arms/scoring/combos/$C/$P/$L` at line 6).
- `EVAL/tools/tmp-scripts/anon-b11.sh` and `anon-arms.sh` (reviewer-id and path rewriting, lines 17-25).
- `EVAL/analysis/merge-b11.sh` (resolution build at line 25, merge call at line 34, stale-round retry at lines 36-39) and `b11-launch.sh`.
- `EVAL/combos/SPEC.md` (procedure and hard limits, lines 18-36; batch 11, line 151).
- `REPO/src/superclaude/cli/review/findings.py` (`parse_block` at line 124, `_check_finding` at line 90, `flat` at line 272, `locate` at line 276) and `merge_cmd.py` (the `merge` command, lines 21-118); `ledger.merge_round` (`ledger.py:107`) parses each report with `parse_block` and refuses a round when no reviewer has a valid block.
- `EVAL/analysis/final-table.py` (metric definitions: found, real blocking, judge blocking, wrong blockers, control, lines 31-37 and 62-64).
- Claude Code CLI 2.1.323 `--help` (flags `--settings <file-or-json>`, `--resume`, `--session-id`, `--no-session-persistence`, `--output-format`, `--verbose`) and the hooks reference at `https://code.claude.com/docs/en/hooks` (PostToolUse stdin fields `session_id`, `transcript_path`, `tool_name`, `tool_input`, `tool_use_id`, `agent_id`; output `{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"..."}}`; default command-hook timeout 600 s, `timeout` field in seconds; PostToolUse also fires for tool calls inside subagents, identified by `agent_id`).

Pinned values measured for this design (sha256, 2026-11-13):

| File | sha256 |
|---|---|
| `EVAL/tools/tmp-scripts/judge-one.sh` | `a01bd70d370d73cb32b55a7368aa28e2c12d93403237211c3a71f339ae82cfcc` |
| `EVAL/tools/run-reviewer.sh` (reference for the R-05 diff) | `e1fb50fbe87bff729f5402e2268a9f0c3ed935159f698b28c06bb80299505fba` |

H3 base commits (the packages were squash-merged with their plan, so the base is the squash commit's only parent; R-03's manual check is still required, section 6.3 S-H3):

| Package | Squash commit (plan + implementation) | Base commit for the sandbox |
|---|---|---|
| DS | `0b8a5801d` (#428) | `0e486ab8d0eb24c6f2738ce1f895cc16755b26c1` |
| AL | `4eb75698d` (#385) | `38eb3c58afe6988b51060ae14117172869ea4c1e` |
| CT | `54e21668f` (#486) | `5fa680778718af9087ccbe7a823e3909f1bcceb6` |

Checked: `refs/merge-guard.md` does not exist at the DS base (the plan creates it), and `tests/skills/test_worker_contract.py` exists at the CT base (I7's unnamed test file is reachable).

### 0.3 Decisions this design makes (where the source is silent)

| Id | Decision | Why |
|---|---|---|
| D1 | The F6 arm's briefs are the A2 brief (A1 brief plus the frozen move catalogue M1-M10) for every reviewer, plus the line "Peer coverage is not clearance: a Task a peer looked at is not cleared." in the receiver's brief only. | The card tells the receiver to "apply catalogue moves M1-M10"; that text is meaningless unless the receiver has the catalogue. With the kit in both F6 and A2, C = F6 - A2 measures only the cards, which is how the source books F6 ("P: none booked", `MR:874`). |
| D2 | A card is a harness-rendered fixed template around the card's Task ids. The rendered text never says why a Task was chosen ("nobody covered it"), only "review these Tasks next". | "Nobody covered" plus a short list reveals that the other Tasks were covered, which is the covered-list signal the source withholds (`MR:813`). |
| D3 | Second card (second scout exit): keep the first card's Tasks that are still uncovered, fill up to k from the new ranking; post it only if its Task set differs from the first; the rendered text says it replaces the earlier request. | Keeps "at most k requests in total" (`MR:822`) while letting the second scout's findings deflect away from a Task it covered. |
| D4 | Uncovered Tasks that no scout declared "not checked" are ordered by `sha256("<row>/<pkg>/T<n>")`. | The source ranks only the declared not-checked Tasks first (`MR:809`); luna Coverage sections rarely name Tasks (none of the batch-11 luna Coverage sections sampled for this design named one), so the tie-break decides most cards and must not favour early Tasks. |
| D5 | The surface filter errs toward "surface". | A missed surface finding marks its Task covered and steers the receiver away from it (the I7 failure, `MR:829`); a real finding misread as surface only adds a request. |
| D6 | No `panel-post` helper is built. | In F6 no model posts; the watcher writes cards through the validator (`MR:831`). |
| D7 | Peer/own tags go to a sidecar file `tags/<rid>.jsonl`, never into the report passed to the merge. | The merge input stays byte-identical to the reviewer's normalised report (R-04); nothing has to be stripped for the judge, and the anonymiser still checks that `origin` is absent (R-10). |
| D8 | No session cleanup. Session files under `~/.claude/projects/` are left in place; each reviewer's session transcript is copied into its run folder. | R-46 constrains what a cleanup may delete; no cleanup satisfies it and removes a destructive step. |
| D9 | The judge is the original `EVAL/tools/tmp-scripts/judge-one.sh`, called in place, unchanged and sha256-checked, with a combo argument that walks out of `EVAL` into `R5/scoring/` (section 5.4). | The script hard-codes `EVAL` (line 4) and its output folder (line 6); copying or editing it breaks "unchanged", and writing into `EVAL/arms/scoring/` breaks "no edits to EVAL". |
| D10 | The H2 normaliser imports `parse_block` from the worktree package through `uv run`, and the launcher refuses to start when the worktree's `findings.py` and `ledger.py` differ (sha256) from the copies inside the installed `superclaude` tool that runs the merge. | The merge runs the installed tool (`/home/coder/.local/bin/superclaude`, a uv tool install, as in `merge-b11.sh:34`); the normaliser must use the same parser, and UV is the only allowed way to run Python. |
| D11 | Packages run one after another inside one launch, and so do its three judge calls, so one launch never has more than 3 model sessions alive; the arms of a randomised block are run as separate concurrent launches. | `MR:953` caps concurrent runs (a run is one panel on three packages, `MR:951`) at 10; this design adds a stricter self-imposed cap of 10 concurrent model sessions, which `SPEC.md:99` and `b11-launch.sh` already kept for the gateway. One block of A1, A2 and F6 is then at most 9 sessions. |

## 1. Files to create

Every file lives under `R5/` (code, config, tests, outputs) or under `SB/` (sandboxes, throwaway). Nothing is written to `REPO/src/`, to `EVAL/`, to another redesign's folder, or to `.claude/`. `EVAL` is read only: the candidates, `resolution-live7.json`, `ground-truth.json` (harness scoring only, never a reviewer) and `judge-one.sh` (run in place). Python is run only as `uv run python -m r5.<module>` from `REPO` with `PYTHONPATH=R5/lib`; tests with the command of section 6.

```text
R5/
  DESIGN.md                      this file
  config/
    panels.json                  the three panels: roles, models, reviewer ids, planning timings
    bases.json                   H3 base commit per package (section 0.2)
    catalogue.md                 frozen move text M1-M10 (A2 kit and F6)
    surface.regex                the surface-finding pattern (one line, Python re syntax)
    templates/brief-a1.txt       the A1 brief (run-reviewer.sh brief + H1 sentence), with placeholders
    templates/brief-kit.txt      kit addendum: heading line + catalogue.md
    templates/brief-receiver-f6.txt   the one "peer coverage is not clearance" line
    templates/card-1.txt         rendering of the first card
    templates/card-2.txt         rendering of a replacing card
    templates/finish.txt         the finish-now text
    pins.json                    sha256 of judge-one.sh, catalogue.md, surface.regex, every template, the
                                 installed and worktree findings.py/ledger.py; values-file sums
    values/<panel>/<pkg>.json    Spike 4 values (frozen before any arm), values/<panel>/SHA256SUMS
  bin/
    sandbox-build.sh             build SB/<pkg>/repo (H3+H4) and SB/cand/<pkg>/ (candidate, source.md)
    run-reviewer-r5.sh           one reviewer: H1 brief, attempts, hang guard, H2 normalise + re-ask
    run-panel.sh                 one panel on one package: T0, watcher, reviewers, collab.json
    hook-posttool.sh             receiver PostToolUse hook: snapshot seal, card delivery, finish signal
    merge.sh                     superclaude review merge for one row-package
    anon.sh                      anonymise one merged report for the blind judge
    judge.sh                     call the unchanged EVAL judge-one.sh for one row-package
    launch.sh                    one panel, all three packages: run, merge, anonymise, judge, results row
    pins-check.sh                verify pins.json; exit 1 on any mismatch
  lib/r5/
    __init__.py
    panelmsg.py                  panel-msg/1 validator for kind "coverage" (R-06, R-08)
    coverage.py                  findings -> covered Tasks; surface filter; not-checked parse; ranking; card build
    watcher.py                   poll loop that turns scout exits into cards
    h2.py                        H2 truncation, parse with the real parser, re-ask decision and prompt
    timing.py                    k, PANEL_FINISH_AT, hang guard, slowdown limit; Spike 4 values writer
    tagger.py                    peer/own tags and requests acted on
    collab.py                    collab.json assembly (R-23)
    alarms.py                    CONVERGENCE, DEFLECTION, SNAPSHOT, SLO, drift; per-arm summary
    results.py                   results row JSON from score.json + ground truth + cost + collab
    audit.py                     contamination and read-only audit
  spikes/
    s0-hooks.sh  s2-resume.sh  reqs3-act.sh  spike4.sh  (S3 is the smoke test, section 6.4)
    NOTES.md                     one section per spike: command, date, transcripts, PASS/FAIL
  tests/
    conftest.py  fake/claude  fixtures/  test_*.py   (section 6)
  runs/<row>/<pkg>/              outputs of one panel on one package (section 2.7)
  scoring/<token>/<pkg>/<label>/ merged-anon.md, score.json, judge.json (written by judge-one.sh)
  results/<row>.json, results/results.jsonl, results/arm-summary-<arm>.json
  results/scoring-keys.jsonl     token -> row, pkg, label, arm (outside the judge's folder; never passed to the judge)
```

### 1.1 Config files

| File | Content and interface |
|---|---|
| `config/panels.json` | `{"<panel>": {"name", "baseline": "EL2|SL2|HL2", "reviewers": [{"rid", "model", "role": "receiver|scout"}], "receiver_turn_planning_s", "receiver_report_planning_s", "planning_B_s": {"<pkg>": s}, "min_calls": 6, "deal": "single|split"}}` for panels `sl2`, `hl2`, `el2` exactly as in section 3. Models must be in the allow-list `{muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7}`. |
| `config/bases.json` | `{"<pkg>": {"base": "<40-hex>", "squash": "<sha>", "verified_by": "<check>", "verified_at": "<UTC>"}}`, values from section 0.2. |
| `config/catalogue.md` | Ten lines `M<n>. <move text>`, the "Move (text sent to a reviewer)" column of `MR:182-193` copied exactly. sha256 in `pins.json`; R-07 check in `audit.py`. |
| `config/surface.regex` | One line, matched case-insensitively against a finding's `claim`: `artifact|\b(?:file|output|log|package|repo(?:sitory)?|absolute|relative)\s+paths?\b|\bdirector(?:y|ies)\b|\bedit(?:s|ing)?\s+(?:scope|locations?|paths?|under)\b|\b(?:allowed|permitted|edit)\s+(?:paths|locations|scope)\b|\boutside\s+(?:the|its|their|this)\b|\bsha-?256\b|\bhash(?:es)?\b|\bchecksum|\bline[- ]numbers?\b|\blines?\s+\d+` |
| `config/templates/brief-a1.txt` | Byte-identical to the `BRIEF` string of `run-reviewer.sh:13-17` with `$CAND_SB` and `$SHA` as placeholders `{CAND}` and `{SHA}`, and one sentence inserted after the first sentence of line 15: `The source document this plan was written from is {SOURCE}; read both the candidate and the source document.` (H1, R-01). |
| `config/templates/brief-kit.txt` | `Investigative moves (catalogue M1-M10); apply each where it fits:` followed by `catalogue.md`. Appended after the brief in A2 and F6 (decision D1). |
| `config/templates/brief-receiver-f6.txt` | `Peer coverage is not clearance: a Task a peer looked at is not cleared.` Appended to the receiver brief in F6 only (R-39). |
| `config/templates/card-1.txt` | `Panel request (from the harness, not from a reviewer): review these plan Tasks next: {TASKS}. Apply catalogue moves M1-M10 to them first; finish checks you have already started. Act on at most {K} requested Task(s) in total. Peer coverage is not clearance.` `{TASKS}` renders `T9` as `Task 9`, joined with `, `. |
| `config/templates/card-2.txt` | `Updated panel request (replaces the earlier one): review these plan Tasks next: {TASKS}. Apply catalogue moves M1-M10 to them first; finish checks you have already started. Act on at most {K} requested Task(s) in total, counting any you already started. Peer coverage is not clearance.` |
| `config/templates/finish.txt` | `Finish now with what you have: write your report now, ending with the findings block and the verdict line.` |
| `config/values/<panel>/<pkg>.json` | `{"panel", "pkg", "B_f_s", "turn_p90_s", "T_report_p90_s", "hooks_s": 2, "k", "finish_offset_s", "hang_offset_s", "slowdown_s", "slowdown_limit", "budget_ok", "runs": [...], "measured_at"}`, written once by `timing.py spike4`; `SHA256SUMS` beside them. Never rewritten during an arm (R-30). |

### 1.2 Scripts and modules (interfaces)

| File | Interface | Purpose |
|---|---|---|
| `bin/sandbox-build.sh` | `sandbox-build.sh [--rebuild] [pkg...]`; exit 0 when every sandbox exists and matches `SB/manifest.json` | For each package: `git -C REPO archive <base> -- . ':(exclude).dev/tasks/done' ':(exclude).dev/eval-workspaces' ':(exclude).dev/research' ':(exclude).dev/reflect' \| tar -x -C SB/<pkg>/repo`; then `git init -q`, `git -c user.name=r5 -c user.email=r5@local commit -qam snapshot` after `git add -A` (so `git status` can audit read-only). Copies `EVAL/<pkg>/candidate.md` and `REPO/.dev/tasks/done/<pkg>/source.md` into `SB/cand/<pkg>/`. Writes `SB/manifest.json` (base sha, tree sha, candidate and source sha256). `--rebuild` deletes only `SB/<pkg>/` and `SB/cand/<pkg>/`. Refuses any path outside `SB`. |
| `bin/run-reviewer-r5.sh` | `run-reviewer-r5.sh <outdir> <pkg> <rid> <model> <role> <t0_ms> <values.json\|planning> [settings.json]`; env `PANEL_COLLAB`, `PANEL_KIT`, `NOFALLBACK=1` (required), `DRY_RUN=1` prints the command and brief and exits | Section 2.6. No fallback ladder (NOFALLBACK=1 is mandatory, so `run-reviewer.sh:66-83` is not copied). |
| `bin/run-panel.sh` | `run-panel.sh <row> <panel> <pkg>`; env `PANEL_COLLAB`, `PANEL_KIT`, `SPIKE4=1` (planning values, hang guard 3000 s) | Section 2.7. |
| `bin/hook-posttool.sh` | Called by Claude Code with the PostToolUse JSON on stdin; arguments baked into the settings command string: `<board> <rid> <t0_ms> <finish_ms> <min_calls> <k> <r5_root>`; prints nothing or one hookSpecificOutput JSON; always exits 0 | Section 2.4. |
| `bin/merge.sh` | `merge.sh <row> <pkg>`; exit = merge exit code | Section 5.2. |
| `bin/anon.sh` | `anon.sh <row> <pkg>`; prints `<token> <label>` | Section 5.3. |
| `bin/judge.sh` | `judge.sh <token> <pkg> <label>`; exit = judge-one.sh exit | Section 5.4. |
| `bin/launch.sh` | `launch.sh <panel> <row> [--pkgs <full package id>[,<full package id>...]]` (default: all three); env `PANEL_COLLAB` (default 1), `PANEL_KIT` (default 0; forced to 1 when `PANEL_COLLAB=1`), `SPIKE4=1` (Spike 4 measurement rows only), `NOFALLBACK=1` required | Section 5. |
| `bin/pins-check.sh` | `pins-check.sh`; prints one line per pin, exit 1 on any mismatch | R-02, R-07, R-29, R-30, D10. |
| `lib/r5/panelmsg.py` | `validate(line: str, ctx: Ctx) -> tuple[bool, str]`; `Ctx(candidate_tasks: set[str], receivers: set[str], k: int, run: str)`; CLI `python -m r5.panelmsg <candidate> <k> <receivers> < lines` | Section 2.2. |
| `lib/r5/coverage.py` | `task_index(candidate_text) -> list[tuple[str, int, int]]` (Task id, first line, end line); `tasks_of(finding, candidate_text, index) -> set[str]`; `is_surface(finding, pattern) -> bool`; `covered(findings) -> set[str]`; `declared_not_checked(report_text) -> set[str]`; `rank(uncovered, declared, row, pkg) -> list[str]`; `next_card(state, scout_reports, k, receivers, deal_r) -> list[Card]` | Section 2.3. |
| `lib/r5/watcher.py` | `python -m r5.watcher --run-dir D --candidate C --panel P --k K --finish-ms F --row R --pkg G --deal-r 0\|1`; exits 0 when every scout has a final attempt or at `finish-ms` | Section 2.3. |
| `lib/r5/h2.py` | `normalise(report_text) -> tuple[str, list[dict]]` (normalised text, remaining parser errors); `reask_prompt(errors) -> str`; CLI `python -m r5.h2 normalise <in.md> <out.md>` prints the error list as JSON | Section 2.6. |
| `lib/r5/timing.py` | `k(B, turn, report, hooks=2) -> int`; `finish_offset(B, turn, report) -> float`; `hang_offset(B) -> float`; `slowdown_limit(B, k, turn, hooks=2) -> float`; CLI `spike4 --panel P --rows r1,r2,... [--kit-rows ...]` writes the values files | Section 2.5. |
| `lib/r5/tagger.py` | `tag(run_dir, candidate) -> dict`; writes `tags/<rid>.jsonl` | Section 2.8. |
| `lib/r5/collab.py` | `python -m r5.collab <run_dir>` writes `collab.json` | Section 2.8. |
| `lib/r5/alarms.py` | `python -m r5.alarms package <run_dir> --ref results/arm-summary-A1-<panel>.json`; `python -m r5.alarms arm <arm> <row...>` | Section 2.9. |
| `lib/r5/results.py` | `python -m r5.results <row>` writes `results/<row>.json` and appends `results/results.jsonl` | Section 5.5. |
| `lib/r5/audit.py` | `python -m r5.audit static` (catalogue, templates, regex vs ground truth); `python -m r5.audit row <row>` (board, transcripts, sandbox, candidate); exit 1 on a violation | Section 2.10. |
| `spikes/*.sh` | Each writes `spikes/out/<spike>/...` and appends a PASS/FAIL section to `spikes/NOTES.md` | Section 6.3. |

Size estimate: hook about 70 lines of bash, watcher plus coverage about 180 lines of Python, run-reviewer-r5 about 110, run-panel about 80, launch plus merge, anon, judge about 120, the other Python modules about 350, tests about 700. The source's "about 120 lines" (`MR:880`) counts only the hook and the watcher; the rest is the shared substrate and the harness fixes this design must carry in its own folder.

## 2. Behaviour

### 2.1 Flow of one panel on one package (F6 arm)

1. `run-panel.sh` records T0 (epoch ms), loads the frozen values file, computes `finish_ms = T0 + 1000 x finish_offset_s` and `hang_ms = T0 + 1000 x hang_offset_s`, and writes `runs/<row>/<pkg>/run.json`.
2. If `k = 0` for this package, the package runs exactly as A2 (no hooks, no watcher) and is logged `k0_isolated: true` (R-42 dilution).
3. Otherwise it writes one settings file per receiver (section 2.4), starts the watcher in the background, then starts every reviewer at once (receivers with `--settings`, scouts without).
4. Each scout exit writes `<rid>.attempt<n>.meta.json`. The watcher sees it, parses the scout's report, and appends a card for each receiver to `board/msgs/watcher.jsonl` if the rules of 2.3 allow.
5. At each receiver tool call, the hook counts the call; from the receiver's `min_calls`-th main-session call on, before `finish_ms`, it seals the receiver's transcript (once), then delivers the newest undelivered card as `additionalContext`.
6. At the first receiver tool call at or after `finish_ms` the hook prints the finish text once and delivers nothing more.
7. A reviewer still running at `hang_ms` is killed (`hang_kill`, the package is `SLO_BREACH`).
8. After every reviewer has ended, `run-panel.sh` stops the watcher, runs the tagger, assembles `collab.json` and runs the package alarms and the row audit.

### 2.2 Message schema and validator (`panelmsg.py`)

A card is one `panel-msg/1` line (`MR:204-218`) of kind `coverage`:

```json
{"v":"panel-msg/1","id":"c-<rid>-<n>","run":"<row>/<pkg>","from":"watcher","to":"<receiver rid>","t":1731500000123,"kind":"coverage","items":["T9","T12"]}
```

Validator rules (a line failing any rule is written to `board/rejected.jsonl` with the reason and never delivered):

| Rule | Source |
|---|---|
| Serialised UTF-8 size at most 600 bytes; one JSON object | R-06 |
| Keys exactly `v, id, run, from, to, t, kind, items`; any other key (including `claim`, `verdict`, `blocking`, `severity`, `category`, `note`, `move`, `anchor`, `n`) is rejected | R-06; `MR:813` "no counts, no categories" |
| `v == "panel-msg/1"`, `kind == "coverage"`, `from == "watcher"`, `to` is one of the panel's receiver ids, `run == "<row>/<pkg>"`, `t` an integer | `MR:825` |
| `items` is a non-empty list of at most k distinct strings, each matching `^T[1-9][0-9]?$` and present in the candidate's Task list (`## Task <n>:` headings) | R-08 coverage exception |
| `id` unique within the board | audit trail |

### 2.3 Watcher and coverage (`watcher.py`, `coverage.py`)

**Trigger.** Poll every 2 s (`MR:880`). A scout attempt counts when `<rid>.attempt<n>.meta.json` exists with `model_ok: true`, `findings_block: true` and `api_error: false` (the runner writes the meta to a temp file and renames it, so the watcher never reads a half-written file). An attempt with `model_ok: false` (a wrong model), no block, or an API error (which `run-reviewer.sh:59` retries) contributes nothing and is logged `scout_unusable`. The watcher exits when every scout has a final meta (attempt 2, or attempt 1 that passed) or at `finish_ms`, whichever is first.

**Parse.** Read `<rid>.attempt<n>.md`, apply `h2.normalise` in memory (truncation only, no re-ask), and take `parse_block(...)["findings"]`, the lines the real parser accepts, even when other lines fail.

**Task of a finding.** `task_index` lists each `^## Task (\d+):` heading of the candidate and its line range (to the next `^## ` heading). `tasks_of` locates `anchor` and `anchor2` in the candidate with `findings.locate` (whitespace-flattened exact match) and returns every Task whose range contains a match start. An anchor that lands outside every Task range (Constraints, Phase headings, title) adds no Task. Only when neither anchor locates does it fall back to `Task <n>` tokens in `refs`.

**Surface filter.** A finding is surface when `config/surface.regex` matches its `claim` (case-insensitive). Surface findings never count as coverage (`MR:829`, R-38). The pairs (Task, category, surface yes/no) are logged to `board/coverage.jsonl` for the spot-check audit (`MR:887`).

**Covered and uncovered.** covered = union over usable scout attempts so far of `tasks_of` for non-surface findings. uncovered = candidate Tasks minus covered.

**Declared not checked.** Outside the findings block, split the scout report into sentences; a sentence that matches `\b(did not|didn't|not (?:check|checked|verify|verified|review|reviewed|inspect|inspected|validate|validated|cover|covered)|unchecked|unverified|skipped|out of scope)\b` contributes every Task it names (`Task 7`, `Tasks 3 and 7`, `Tasks 3-5`).

**Rank.** Uncovered Tasks named as not checked come first (more scouts naming it first), then the remaining uncovered Tasks by `sha256("<row>/<pkg>/T<n>")` ascending (decision D4). The rank list is logged.

**Card content.**

| Panel shape | Card 1 (first usable scout exit) | Card 2 (second usable scout exit) |
|---|---|---|
| One receiver (SL2, HL2) | first k of the rank | card-1 Tasks still uncovered, then the next Tasks of the new rank, up to k; posted only if the set differs from card 1 (else logged `dup_card`) |
| Two receivers (EL2) | rank position i goes to receiver `(i + deal_r) mod 2`; each receiver's card holds its first k | none: the only scout is ember |

No card is posted when uncovered is empty (logged `nothing_uncovered`), when k = 0, or at or after `finish_ms` (logged `after_finish`). Every card passes `panelmsg.validate` before the atomic append (write to a temp file in `board/`, then append under `flock board/msgs/.lock`).

### 2.4 Receiver hook (`hook-posttool.sh`)

Settings file `runs/<row>/<pkg>/board/settings/<rid>.json`, passed as `--settings <file>`:

```json
{"hooks":{"PostToolUse":[{"matcher":"*","hooks":[{"type":"command","timeout":10,
 "command":"bash <R5>/bin/hook-posttool.sh <board> <rid> <t0_ms> <finish_ms> <min_calls> <k> <R5>"}]}]}}
```

Every value is an absolute path or a number baked into the command string; the hook reads nothing from the environment (R-21). Steps, each guarded so any failure prints nothing, appends `{"event":"hook_error",...}` to `board/metrics/<rid>.jsonl` and exits 0 (R-22):

1. Read stdin. If `agent_id` is present and non-empty, log `subagent_call` and exit 0 (cards go to the main session only; the docs state PostToolUse fires inside subagents too).
2. Increment `board/state/<rid>.calls` under `flock`.
3. If now >= `finish_ms`: if `board/state/<rid>.finish_sent` is absent, create it, log `finish_signal_t`, print the finish text; exit 0 (R-41).
4. If calls < `min_calls`, or k = 0, or `board/state/<rid>.snapfail` exists, exit 0.
5. Find card lines in `board/msgs/watcher.jsonl` with `to == <rid>` whose id is not in `board/delivered/<rid>.jsonl`. None: exit 0.
6. Seal (first delivery only): copy `transcript_path` to `board/snap/<rid>.jsonl`, write its sha256 to `board/snap/<rid>.sha256` and the time to `board/snap/<rid>.t`. If the copy or the hash fails, or the transcript is missing or empty: create `snapfail`, log `snapshot_missing`, exit 0 with nothing delivered, now and for the rest of the run (`MR:232`).
7. Re-check the newest pending card with jq (size <= 600 bytes, `kind == "coverage"`, `from == "watcher"`, at most k items). Render `card-1.txt` if no card was delivered before, else `card-2.txt`. Older pending cards are marked delivered with status `superseded` and are not shown.
8. Print `{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"<text>"}}` (text at most 1,500 characters; `MR:225`), append `{id, t, call, status:"delivered", text_sha256}` to `board/delivered/<rid>.jsonl`, and log hook duration in ms.

The hook never blocks the reviewer: no Stop hook exists in any arm (`stop_blocks = 0`).

### 2.5 Timing (`timing.py`)

Formulas, exactly as `MR:284-308` and R-41, R-42, with the receiver's turn values (B, turn and report in seconds):

- `k = max(0, min(2, floor((0.35 B - 2 - turn_p90 - T_report_p90) / (2 turn_p90) + 1e-9)))` (the 1e-9 only protects exact boundaries from float rounding)
- `PANEL_FINISH_AT = T0 + 1.35 B_f - turn_p90 - T_report_p90`
- hang guard `= T0 + 1.5 B_f` for every reviewer, scouts included, in every arm (R-43)
- the planned end `B + 2 + 2k turn_p90`; the finish-signal bound `T0 + 1.35 B_f`
- slowdown limit for this design's brief on the receiver: `s_max = (0.35 B - W) / B`, `W = 2 + 2k turn_p90` (13.8% on SL2 at k = 2, `MR:301`); `budget_ok = s <= s_max`

Spike 4 values (section 6.3) replace every planning number. A values file is written once per panel and package, with sha256 in `SHA256SUMS`, and `run-panel.sh` refuses to run when the sum does not match (R-30). In `SPIKE4=1` mode only (the Spike 4 measurement runs themselves), the planning B of section 3 is used for T0 bookkeeping and the hang guard is 3000 s, as in today's harness.

### 2.6 Reviewer runner (`run-reviewer-r5.sh`)

**Brief.** `brief-a1.txt` with `{CAND} = SB/cand/<pkg>/candidate.md`, `{SHA}` its sha256 and `{SOURCE} = SB/cand/<pkg>/source.md`; plus `brief-kit.txt` when `PANEL_KIT=1`; plus `brief-receiver-f6.txt` when `PANEL_COLLAB=1` and role is receiver.

**Command** (A1 form; R-05):

```bash
( cd SB/<pkg>/repo && timeout <remaining_s> claude -p --model "$MODEL" --output-format json \
    --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit [--settings <file>] <<<"$BRIEF" ) \
  >"$OUT/$RID.attempt$N.json" 2>"$OUT/$RID.attempt$N.err"
```

Differences from `run-reviewer.sh:48`: no `--no-session-persistence`; `timeout` is `ceil((hang_ms - now) / 1000)` instead of 3000; the cwd is the package's H3 sandbox; the brief carries H1; `--settings` only for an F6 receiver on attempt 1. Nothing else changes.

**Checks after each attempt.** Copied from `run-reviewer.sh:50-58` unchanged: the report text, observed model, `output_tokens_main`, `output_tokens_all`, the API-error grep, `model_ok`, `findings_block`, and `<rid>.attempt<n>.meta.json`, plus `api_error`, `t_start_ms`, `t_end_ms`, `exit` and `hang_kill` (exit 124 and now >= hang_ms). The meta is written to `<file>.tmp` and then renamed with `mv` (atomic on one filesystem), unlike `run-reviewer.sh:58`. `session_id` is read from the result message; the session file `~/.claude/projects/<cwd with / replaced by ->/<session_id>.jsonl` is copied to `<rid>.attempt<n>.session.jsonl` (needed for Spike 4 turn timings and the audit).

**Attempts** (`run-reviewer.sh:61-64`, R-44). At most 2. Attempt 2 starts only if attempt 1 failed `model_ok && findings_block && !api_error` and `hang_ms - now > 0`; it runs without `--settings` (`retry_isolated: true`). The fallback ladder is not run: `NOFALLBACK=1` is required and the script refuses to start without it.

**H2** (R-02). On the final attempt's report: `h2.normalise` truncates `anchor` and `anchor2` to the longest prefix whose whitespace-flattened length is at most 200, and `claim` to 300, then runs the real `parse_block`. Remaining errors (anchor under 12 characters, refs over 8, bad id, bad severity, MINOR marked blocking, bad category, invalid JSON) trigger one re-ask if `hang_ms - now >= 6 s + turn_p90`:

```bash
( cd SB/<pkg>/repo && timeout <remaining_s> claude -p --resume "$SESSION_ID" --model "$MODEL" \
    --output-format stream-json --verbose --permission-mode bypassPermissions \
    --disallowedTools Edit Write NotebookEdit <<<"$(h2 reask prompt)" ) >"$OUT/$RID.reask.jsonl"
```

The re-ask prompt lists the parser errors by line and asks for the complete corrected report. The re-ask runs with no hooks. Its output is read with `jq -s` through the same filters as `run-reviewer.sh:50-56` (result text, observed model, tokens, API-error grep), written as `reask_observed_model` and `reask_model_ok` (R-28, `MR:933`, `MR:953`). Its report replaces the original only if `reask_model_ok` is true, it has no API error, and its normalised block has fewer parser errors; a model mismatch keeps the original and logs `reask_model_mismatch`. `reask_s`, `reask_skipped` and `dropped_lines` (errors left) go to `<rid>.timing.json`; the final text is `<rid>.md` (fed to the merge), the untouched text `<rid>.raw.md`. `<rid>.cost.json` keeps the `run-reviewer.sh:87` shape (`attempts`, `total_wall_s`, `total_output_tokens_all`) and adds the re-ask's wall time and tokens.

### 2.7 Panel runner and the run folder (`run-panel.sh`)

```text
runs/<row>/<pkg>/
  run.json        row, arm, panel, pkg, T0, finish_ms, hang_ms, k, deal_r, values sha256, env switches
  reviews/        <rid>.attempt<n>.{json,md,err,meta.json,session.jsonl}, <rid>.{raw.md,md,meta.json,cost.json,timing.json}
  board/          msgs/watcher.jsonl, rejected.jsonl, coverage.jsonl, delivered/<rid>.jsonl, state/, snap/,
                  metrics/<rid>.jsonl, settings/<rid>.json, watcher.log     (F6 only; kept, never deleted, R-26)
  tags/<rid>.jsonl
  collab.json     section 2.8
  alarms.json     section 2.9
  audit.json      section 2.10
  resolution.json, ledger.json, merged-1.md, merge-stdout.txt   (section 5.2)
```

`deal_r` is a seeded 0/1 coin: the first bit of `sha256("<row>/<pkg>/deal")`, used only on EL2. `panel elapsed_s = max over reviewers of t_end (re-ask included) - T0`.

### 2.8 Tags and `collab.json` (`tagger.py`, `collab.py`)

**Tags** (R-10, `MR:233`, `MR:853`). For a receiver, a findings line is `peer` when `tasks_of(line)` intersects the Tasks of the cards delivered to it; otherwise `own`. Every scout line is `own`. Written to `tags/<rid>.jsonl` as `{"fid","origin","tasks"}`; never written into a report. `requests_acted` = delivered Tasks with at least one peer-tagged receiver line.

**`collab.json`** carries every R-23 field. Fields that do not apply to F6 are written as `null` so the schema check covers every arm: `resume_fallback`, `phase2_s`, `n_planned`, `n_launched`, `phase2_timeout`, `p2_lines_salvaged`, `slot_type`, `card_form`, `deal_c`, `echo_rate`. Always 0 in F6: `stop_blocks`, `msgs_sent` (the watcher authors every card), `over_cap`. Filled per reviewer: `msgs_received`, `first_delivery_t`, `seal_t`, `hook_calls`, `hook_error`, `hook_ms_p95`, `reask_s`, `attempts`, `retry_s`, `retry_isolated`, `finish_signal_t`, `hang_kill`, `snapshot_missing`, `late`. Panel: `arm`, `k`, `deal_r`, `panel_finish_at`, `finish_would_fire` (A1 and A2: the receiver still running at `finish_ms`, computed from `t_end`), `elapsed_s`, `baseline_elapsed_s` (B_f), `overhead_pct`, `own_line_jaccard`, `pairwise_task_jaccard`, `ledger_rows`, `values_sha256`. F6 additions: `cards` (id, to, items, t_post, t_delivered, status `delivered|superseded|late|undelivered|dup_card|after_finish`), `requests_posted`, `requests_delivered`, `requests_acted`, `scout_covered_tasks`, `receiver_anchored_tasks`, `deflection_overlap`, `union_anchored_tasks`, `k0_isolated`, `slo` (`ok|over_cap|SLO_BREACH`). `late` = a card posted before `finish_ms` that the receiver never received because its process ended first (`MR:225`).

### 2.9 Alarms (`alarms.py`, all computed without ground truth)

| Alarm | Rule | Source |
|---|---|---|
| CONVERGENCE | Per package: mean pairwise Jaccard of the Task sets anchored by each reviewer's own-tagged lines, against the A1 mean of the same panel and package: fires above A1 + 0.15, or when `ledger_rows` < 0.8 x A1 mean. Arm passes if it fires in at most 2 of 12 runs | R-25 |
| DEFLECTION | Fires when `deflection_overlap` = share of the receiver's anchored Tasks that the scouts covered > 0.50, or when `union_anchored_tasks` (all reviewers) < the A1 mean union for that package | R-40, `MR:855` |
| SNAPSHOT | Arm level: `snapshot_missing` in more than 50% of receiving reviewers | R-25 |
| SLO | Per package: `elapsed_s > 1.35 B_f` uses the error budget (1 package in 12 per arm; spending more stops the arm); a hang kill is `SLO_BREACH` | R-24, R-43 |
| drift | `baseline_drift = B_c / B_f` per block; a block outside [0.963, 1.10] is reported but not used for the time verdict | R-45 |

The A1 reference values (`results/arm-summary-A1-<panel>.json`) come from the A1 runs of the same panel; until they exist, `alarms.json` records the raw values and `reference: "missing"`.

### 2.10 Contamination safeguards and audit (`audit.py`)

What crosses between reviewers: uncovered Task ids only, from finished scouts, through the harness. What is withheld: anchors, claims, severities, categories, counts and the covered list (`MR:851-852`). The receiver gets nothing before its first scout exits and its own `min_calls`-th call, and its transcript is sealed before the first card. Reviewers never see ground truth: briefs, templates and cards are generated from the candidate and the catalogue only, and the judge alone reads `ground-truth.json`.

Audit checks, each a pass/fail in `audit.json` (a failure marks the row-package `quarantined` in place; files are kept, R-26):

| Check | Method |
|---|---|
| R-07 static | `catalogue.md`, every template and `surface.regex` contain no 12-character substring of any `plan_quote` in the three `ground-truth.json` files and no file path named in any GT `description`; output is ids only, never GT text |
| Board text | Same check over every card line and every rendered text (`delivered/*.jsonl` stores the text sha; the renderer is re-run to check the text) |
| No free text | Every line in `msgs/watcher.jsonl` re-validates under 2.2 |
| Transcripts | No reviewer tool input (any attempt, any re-ask) contains `.dev/reflect`, `ground-truth`, `20261111-a1`, `20261113-collab`, `/board/`, `r5-coverage-deflection`, `.claude/projects` (other reviewers' session transcripts, which hold the scouts' full reports) or `/home/coder/workspaces/worktrees/IronClaude` (the live repository, with the repaired code and the brainstorm) |
| Read-only | `git -C SB/<pkg>/repo status --porcelain` is empty after the run; `sha256(SB/cand/<pkg>/candidate.md)` and `source.md` equal `SB/manifest.json` (R-09) |
| Model | the final attempt's `model_ok` is true; `expected_model` equals the panel's model for that rid; a re-ask report that was used has `reask_model_ok: true` |

## 3. The three panels

The source designs F6 for one panel only, sonnet + 2x luna (`MR:41`, `MR:813`): two fast scouts finish long before one slow receiver. The rule this design applies to every panel is the same: **the receivers are the reviewers that set the panel's elapsed time; the scouts are the others.** The k formula uses the receiver's own turn_p90 and T_report_p90. Reviewer ids are the ones earlier rows used for the same models, so `resolution-live7.json` (which lists `t1b-1, t2-1, t2b-1, t3-1, t3-2, t4-1, t4-2` in all three packages) and the merge accept them.

| Panel key | Panel | Receiver(s) | Scout(s) | Baseline | Cards per receiver | Fidelity to the source |
|---|---|---|---|---|---|---|
| `sl2` | sonnet + 2x luna | `t1b-1` claude-sonnet-5-5 | `t4-1` gpt-6-luna, `t3-1` gpt-6-luna | SL2 (A1-SL2) | at most 2 | As specified (pre-registered stage 2, `MR:949`) |
| `hl2` | haiku + 2x luna | `t4-1` claude-haiku-5-5 | `t4-2` gpt-6-luna, `t3-1` gpt-6-luna | HL2 (A1-HL2) | at most 2 | Adaptation: haiku replaces sonnet as the slow receiver |
| `el2` | ember + 2x luna | `t4-1` gpt-6-luna, `t3-1` gpt-6-luna | `t2b-1` muse-ember-1.0 | EL2 (A1-EL2) | at most 1 | Adaptation: roles inverted, because ember finishes first |

Only the `sl2` arm is covered by the source's stage-2 screen (`MR:976`). The `hl2` and `el2` runs are owner-requested extensions: they use the same rules, but no decision rule was pre-registered for them, so their results are exploratory.

### 3.1 sonnet + 2x luna (`sl2`), as specified

- Scouts: the two lunas (about 102-110 s). Receiver: sonnet (planning B = 273.7 s, turn 14 s).
- Planning numbers (replaced by Spike 4): k = 2 needs sonnet's T_report_p90 at most 23.8 s, k >= 1 at most 51.8 s (R-42). Per package with the historical medians: designSpec B = 259 s gives k = 2 up to 18.65 s and k >= 1 up to 46.65 s; alias B = 302 s gives 33.7 s and 61.7 s; control B = 269 s gives 22.15 s and 50.15 s.
- Three numbers at B = 273.7 s: planned end 303.7 s (k = 1) or 331.7 s (k = 2); finish-signal bound 369.5 s; hang guard 410.6 s. PANEL_FINISH_AT = T0 + 355.5 s - T_report_p90.
- Run condition (R-39, `MR:827`): the arm runs only if Spike 4 gives k >= 1; a package with k = 0 runs as A2 and is reported as dilution. Brief slowdown limit 13.8% at k = 2 (`MR:301`).

### 3.2 haiku + 2x luna (`hl2`), adaptation

- Scouts: the two lunas. Receiver: haiku, the slowest (median 233 s wall, 23 s per turn, `MR:263-268`); HL2 planning B = 238 s (`MR:277`).
- Haiku is a Claude model, so hook delivery is the same low-risk case as sonnet.
- Planning numbers with turn_p90 = 23 s: k = 2 is impossible on every package (it would need a negative T_report_p90). k >= 1 needs haiku's T_report_p90 at most 12.3 s at B = 238 s; per package, 6.0 s (designSpec, B = 220 s), 12.3 s (alias, B = 238 s) and 8.1 s (control, B = 226 s). Haiku's mean turn is already 23 s (`MR:266`) and a haiku review writes about 40k output tokens in total (`SPEC.md:4`, whole review), so its final report turn is unlikely to take 12.3 s or less, and **k = 0 on all three packages is the likely Spike 4 outcome**. In that case `launch.sh` refuses the F6 arm on `hl2` with exit 3 and the measured reason (section 5.1) rather than running an exchange that cannot fit the +35% window; A1-HL2 and A2-HL2 still run. If only some packages have k >= 1, those packages get cards and the others run as A2 (`k0_isolated`).
- Three numbers at B = 238 s and k = 1: planned end 286 s (+20.2%); finish-signal bound 321.3 s; hang guard 357 s. Slowdown limit at k = 1: (83.3 - 48) / 238 = 14.8%.
- The source's surface filter targets luna's Task 12 artifact objection; the scouts here are the same lunas, so it applies unchanged.

### 3.3 ember + 2x luna (`el2`), adaptation

- Ember is the fastest reviewer (median 41 s, `MR:265`) and the lunas set B, so the source's direction (scouts done before the receiver) holds only with the roles inverted: **ember is the one scout and both lunas are receivers.** Each luna gets at most one card, posted when ember exits.
- The two lunas get disjoint requests: rank position i goes to luna `(i + deal_r) mod 2` (the balanced online deal of R-12 and R-20, `deal_r` logged), so both do not chase the same Task (the source's duplicated-attention evidence, `MR:110`).
- Ember exits at about 41 s, when a luna has made about 6 tool calls (41 / 6.4). `min_calls = 6` (the same gate R-19 sets for luna receivers in F4) keeps the first card behind luna's reading of the plan and source.md.
- Planning numbers with luna turn 6.4 s and T_report_p90 6.4 s (`MR:285-295`): k = 2 at B = 116 s; designSpec (B = 100 s) gives k = 1 at most (needs T_report_p90 <= 13.8 s); alias needs <= 8.0 s and control <= 8.7 s for k = 2.
- Three numbers at B = 116 s: planned end 130.8 s (k = 1) or 143.6 s (k = 2); finish-signal bound 156.6 s; hang guard 174 s; PANEL_FINISH_AT = T0 + 143.8 s at planning values. Slowdown limit 11.2% at k = 2, 22.2% at k = 1.
- What changes in meaning: the source's mechanism is "cheap scouts steer a strong model that is the only one running reverse-dependency sweeps"; on EL2 a cheap searcher steers two cheap readers. Luna's act rate on hook-injected text is unmeasured (REQ-S3 measures it, section 6.3). Gateway-model hook delivery (luna) is S0's question, not a Claude-model certainty as on `sl2` and `hl2`.

## 4. The PANEL_COLLAB=0 baseline

Two environment switches select the arm. `PANEL_COLLAB=1` forces `PANEL_KIT=1` (decision D1).

| `PANEL_COLLAB` | `PANEL_KIT` | Arm label | What runs |
|---|---|---|---|
| 0 | 0 | `A1-<panel>` | Isolated panel with H1-H4: no settings file, no hook, no watcher, no board. The baseline B_A1 and the comparator. |
| 0 | 1 | `A2-<panel>` | A1 plus the catalogue in every brief (static kit), no exchange. Needed because the source compares every exchange arm with the kit (`MR:917`, `MR:976`). |
| 1 | 1 (forced) | `F6-<panel>` | A2 briefs, the receiver line of D1, watcher, cards, hook. |

With `PANEL_COLLAB=0` the harness passes no hooks and creates no board (`MR:258`). The launch command differs from `run-reviewer.sh:48` only by the R-05 list: the H1 sentence in the brief and the H3/H4 sandbox as cwd (R-01, R-03); no `--no-session-persistence`; `--output-format stream-json --verbose` on the H2 re-ask session only; and the hang guard (`timeout` at T0 + 1.5 B_A1 instead of 3000 s). Every other harness fix runs in both arms: the H2 normaliser and re-ask, the 2-attempt retry, `NOFALLBACK=1`, the model check, the session copy, `finish_would_fire` logging, and the same merge, anonymiser and judge. `collab.json` is written in every arm (R-23 schema check), with the F6-only fields `null`.

`run-reviewer-r5.sh` with `DRY_RUN=1` prints the exact command line and brief, which is what the R-05 test diffs (section 6.1, T-11).

## 5. Launch script (`bin/launch.sh`)

`launch.sh <panel> <row> [--pkgs <full package ids, comma-separated>]` runs one panel on the three packages, merges, anonymises, judges, and writes one results row. `<row>` must be new (for example `f6-sl2-r01`, `a1-sl2-r01`); a row folder that already exists is refused.

### 5.1 Preflight (a failure exits before any model call, with exit 2, or exit 3 for step 5, and the reason on stderr and in `runs/<row>/launch.json`)

1. `NOFALLBACK=1` is set.
2. Every reviewer model of the panel is in `{muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7}`; names containing `glm`, `qwen` (any case) or `opus` are refused.
3. `pins-check.sh` passes: judge-one.sh sha256 = `a01bd70d...cfcc`; catalogue, templates and regex sums; worktree and installed `findings.py` and `ledger.py` equal (D10); `audit.py static` passes.
4. `sandbox-build.sh` reports every sandbox present and matching `SB/manifest.json`.
5. `PANEL_COLLAB=1`: the values files exist for all requested packages, their sums match `SHA256SUMS`, at least one package has k >= 1, and `budget_ok` is true; otherwise exit 3 "F6 not runnable on <panel>: <reason>" (the run condition of `MR:827`).
6. `PANEL_COLLAB=0` without values files is allowed only with `SPIKE4=1`.
7. `claude --version` and `superclaude --version` are recorded in `launch.json`.

### 5.2 Run and merge

For each package in order DS, AL, CT (decision D11): `run-panel.sh <row> <panel> <pkg>`, then `merge.sh <row> <pkg>`:

- Resolution: `jq -c --argjson rev "$REV" '.reviewers=$rev' EVAL/<pkg>/resolution-live7.json > runs/<row>/<pkg>/resolution.json`, where `$REV` is built exactly as `merge-b11.sh:17-24` from the panel's ids and models with the tier and alias maps of `merge-b11.sh:11-12` (which already include every id used here).
- Merge: `superclaude review merge --ledger D/ledger.json --doc EVAL/<pkg>/candidate.md --round 1 --report <rid>=D/reviews/<rid>.md ... --resolution D/resolution.json --out D/merged-1.md > D/merge-stdout.txt 2>&1`, the arguments of `merge-b11.sh:34`. A reviewer whose final `model_ok` is false is left out of the merge and recorded as `INVALID` in the results row; the merge is skipped if every reviewer is invalid. A refused round (no valid block) is recorded `merge_refused`; no reviewer is re-run by the launcher.

### 5.3 Anonymise (`anon.sh`, from `anon-b11.sh:17-25`)

- token = 12 random hex characters (`openssl rand -hex 6`); label = one random letter of `Q R S T U V`; `scoring/<token>/<pkg>/<label>/merged-anon.md`; `{"token","row","pkg","label","arm"}` appended to `results/scoring-keys.jsonl` (outside the `scoring/` tree the judge is pointed at).
- Rewrites, every one case-insensitive (`sed -E 's/.../.../gI'`), so the rewrite and the post-check match the same text: every id from `t1b-1|t2b-1|t3-1|t4-1|t4-2` (all ids the three panels use, as whole words) that occurs in the report, mapped to `R1..Rn` in sorted order (narrower than `anon-b11.sh:17`'s generic `\bt[0-9a-z]+-[0-9]+\b`, which also hits prose such as `Task-6`); `EVAL` to `<EVAL>`; the `candidate:` line and `report <path>` as in `anon-b11.sh:24-25`; any path under `R5`, `SB`, or containing `20261113-collab` to `<redacted>`; any `"origin":"peer|own"` pair removed (R-10). Arm markers that A2 and F6 briefs and cards can put into a claim (`MR:953`: the judge must not tell the arms apart): move ids `\bM(10|[1-9])\b` and the phrases `panel request`, `catalogue move(s)`, `peer coverage` and `requested Task(s)` become `<redacted>`, the token every arm's reports already carry (`report <redacted>`), so the replacement itself marks no arm. Reviewers also use `M<n>`/`m<n>` as their own finding ids (32 of 310 historical `merged-anon.md` files, none with the kit); those are rewritten the same way in every arm, which loses no defect content. None of the three candidates contains a move id or one of these phrases (checked with grep), so no candidate quote is changed. The number of redactions per package is written to `scoring-keys.jsonl`.
- Post-check: `grep -ciE '"origin"[[:space:]]*:|/board/|evalsb-collab|20261113-collab|coverage-deflection|\b(t1b-1|t2b-1|t3-1|t4-1|t4-2)\b|\bM(10|[1-9])\b|panel request|catalogue move|peer coverage|requested task'` on `merged-anon.md` must be 0, else the package is not judged and is recorded `anon_failed`.

### 5.4 Judge (`judge.sh`, decision D9)

```bash
bash EVAL/tools/tmp-scripts/judge-one.sh "../../../../20261113-collab/r5-coverage-deflection/scoring/<token>" "<pkg>" "<label>"
```

`judge-one.sh` sets `D="$EVAL/arms/scoring/combos/$C/$P/$L"` (line 6); four `..` steps lead from `EVAL/arms/scoring/combos` to `tasklist-review-panel/`, so D is `R5/scoring/<token>/<pkg>/<label>`, where `merged-anon.md` already is. The script reads `EVAL/<pkg>/ground-truth.json` and `EVAL/<pkg>/candidate.md` (its own lines 8-9), runs `claude-opus-5-5` (the only Opus use), and the judge writes `score.json` into D. `judge.sh` checks the sha256 of `judge-one.sh` before each call, `launch.sh` runs the three packages' judges one after another (so a launch never has more than 3 model sessions alive, decision D11), and after the call requires `score.json` to parse with the keys of `judge-one.sh:21`. A failure is recorded `judge_failed`; the row becomes `partial`. Blinding: the path the judge sees contains a random token, never the row or arm; the folder name `r5-coverage-deflection` is the same for this design's A1, A2 and F6 rows, so it does not reveal the arm.

Per-batch API-error audit (R-29): `judge.sh` greps `judge.json` for `API Error` and records `judge_api_error`.

### 5.5 Results row (`results.py`)

Written to `results/<row>.json` and appended to `results/results.jsonl`. Metric definitions follow `final-table.py:31-37, 62-64`; issue labels follow `MR:22` (designSpec GT1-GT5 = B1-B5, GT6-GT10 = I1-I5; alias GT1-GT3 = B6-B8, GT4 = I6; control GT1-GT2 = I7, I8).

```json
{"row":"f6-sl2-r01","arm":"F6-sl2","panel":"sl2","models":{"t1b-1":"claude-sonnet-5-5","t4-1":"gpt-6-luna","t3-1":"gpt-6-luna"},
 "switches":{"PANEL_COLLAB":1,"PANEL_KIT":1,"NOFALLBACK":1},"values_sha256":{"<pkg>":"..."},
 "found_14":4,"real_blocking_8":2,"judge_blocking":3,"wrong_blockers":1,
 "control_found_2":1,"control_wrong_blockers":0,
 "issues":{"credited_any":["B3","I2"],"credited_blocking":["B3"],"target_reach":true,"hard_credits":1},
 "output_tokens":{"total":0,"per_pkg":{"<pkg>":0},"per_reviewer":{"<pkg>":{"<rid>":0}}},
 "elapsed_s":{"<pkg>":0},"overhead_pct":{"<pkg>":0.0},
 "collab":{"<pkg>":{"k":2,"cards_posted":2,"cards_delivered":1,"requests_delivered":2,"requests_acted":1,"late":0,
   "superseded":0,"dup_card":0,"snapshot_missing":0,"hook_calls":0,"hook_error":0,"hook_ms_p95":0,"finish_signal_t":null,
   "finish_would_fire":false,"hang_kill":0,"retry_isolated":0,"reask_s":0,"dropped_lines":0,"k0_isolated":false,
   "deflection_overlap":0.0,"union_anchored_tasks":0,"own_line_jaccard":0.0,"ledger_rows":0,"slo":"ok"}},
 "alarms":{"<pkg>":{"CONVERGENCE":false,"DEFLECTION":false,"SLO":"ok"}},
 "audit":{"<pkg>":"pass"},"invalid":[],"status":"complete|partial|quarantined"}
```

| Field | Definition |
|---|---|
| `found_14` | `len(gt_covered_any)` on DS + on AL |
| `real_blocking_8` | GT ids in `gt_covered_blocking` whose `blocking_in_implement` is true, DS + AL |
| `judge_blocking` | `len(gt_covered_blocking)`, DS + AL |
| `wrong_blockers` | `wrong_blockers`, DS + AL |
| `control_found_2`, `control_wrong_blockers` | the same two fields on CT |
| `target_reach`, `hard_credits` | credit at any severity on B1, B2, B5, B6, B8, I1, I4, I5, I6 or I7 (`MR:955`); the count of such credits |
| `output_tokens` | sum of `total_output_tokens_all` over every attempt and re-ask of every reviewer (the study's metric) |
| `elapsed_s` | panel elapsed per package (section 2.7), every attempt and re-ask included (R-24) |

`results.py` reads `ground-truth.json` only for the `blocking_in_implement` flags and the id count, after judging; nothing from it reaches a reviewer.

### 5.6 Exit codes and operator use

`0` complete; `1` partial (a package invalid, merge refused, judge failed, or quarantined; the row file says which); `2` preflight refused; `3` F6 not runnable on this panel. One launch keeps at most 3 reviewer sessions running. One randomised block of stage 2 is three concurrent launches in a shuffled start order, 9 sessions in total (`MR:938`, `MR:953`):

```bash
cd REPO && export NOFALLBACK=1
PANEL_COLLAB=0 PANEL_KIT=0 bash R5/bin/launch.sh sl2 a1-sl2-r01 &
PANEL_COLLAB=0 PANEL_KIT=1 bash R5/bin/launch.sh sl2 a2-sl2-r01 &
PANEL_COLLAB=1             bash R5/bin/launch.sh sl2 f6-sl2-r01 &
wait
uv run python -m r5.alarms arm F6-sl2 f6-sl2-r01   # with PYTHONPATH=R5/lib
```

A block scheduler, the interim futility look and the Fisher and permutation tests are not built here: they are shared analysis for all redesigns (section 7, Q4).

## 6. Test plan

All tests run with `mkdir -p /tmp/evalsb-collab-r5 && cd REPO && PYTHONPATH=R5/lib uv run pytest -p no:cacheprovider --basetemp=/tmp/evalsb-collab-r5/pytest R5/tests -v` (`-p no:cacheprovider` keeps pytest from writing `.pytest_cache/` at the repository root, and `--basetemp` keeps every temporary folder inside `SB`; pytest clears that folder at each run but does not create its parent, hence the `mkdir -p`; bats is not installed on this host, so shell scripts are driven from pytest through `subprocess`). Tests never call a real model and never open a real `ground-truth.json`: they use synthetic fixtures under `R5/tests/fixtures/`. `tests/fake/claude` is a bash stand-in put first on `PATH`; it reads `FAKE_SCENARIO` and the arguments it was given, appends its argument list to `$FAKE_LOG`, sleeps as told, may touch files, and prints a canned `--output-format json` array (system, assistant with `message.model`, result with `session_id`, `usage.output_tokens`, `modelUsage`) whose result text is a fixture report. When given `--settings <file>` it runs the hook command from that file once per simulated tool call with a fixture PostToolUse JSON on stdin and records the hook's stdout, so delivery is tested end to end without a model.

### 6.1 Unit tests

| Id | File | Cases (each an assert) | Requirement |
|---|---|---|---|
| T-1 | `test_panelmsg.py` | accepts 3 good cards (1 item, k items, EL2 second receiver); rejects: 601-byte line, keys `claim`, `severity`, `category`, `note`, `n`, `anchor`, `move`, an unknown key, `from != watcher`, `to` not a receiver, `items` empty, k+1 items, duplicate items, `"T99"` not in the candidate, `"Task 9"` format, invalid JSON | R-06, R-08, R-38 |
| T-2 | `test_coverage.py::task_index` | the three real candidates (copied into fixtures) give 13, 9 and 12 Tasks; ranges end at the next `## ` heading | R-38 |
| T-3 | `test_coverage.py::tasks_of` | anchor inside Task 9 gives {T9}; anchor in Constraints gives {}; anchor2 in Task 3 adds T3; whitespace-reflowed anchor still locates; unlocatable anchor falls back to `refs` "Task 12" | R-38 |
| T-4 | `test_coverage.py::surface` | the 9 surface claims and 5 real claims checked while writing this design (artifact outside permitted edit locations, edits under `.claude/`, sha256, line number, output path; single-select read-back, mode label vs two writes, unbounded "every", worker-contract test never updated, halt path mapping) classify 9/9 and 0/5 | R-38, D5 |
| T-5 | `test_coverage.py::uncovered` | a Task covered only by a surface finding stays uncovered (the CT Task 12 case); a Task with one non-surface finding is covered | R-38 verification |
| T-6 | `test_coverage.py::declared` | "I did not check Tasks 3 and 7" gives {T3, T7}; "Tasks 3-5 were skipped" gives {T3, T4, T5}; "I checked Task 2" gives {} | `MR:809` |
| T-7 | `test_coverage.py::rank_and_cards` | declared Tasks rank first; the tie-break equals the sha256 order and is stable across calls; card 1 holds the first k; card 2 keeps still-uncovered card-1 Tasks then fills; identical card 2 is not posted (`dup_card`); k = 0 posts nothing; empty uncovered posts nothing; EL2 deal with deal_r = 0 and rank [a,b,c,d], k = 2 gives luna A {a,c}, luna B {b,d}; deal_r = 1 swaps them; a rendered card contains only `Task <n>` tokens from the template and no count | R-38, R-39, D3, D4 |
| T-8 | `test_watcher.py` | temp run dir; writing a scout meta (`model_ok` true) and report makes a card appear within 2 poll cycles; `model_ok: false` posts nothing and logs `scout_unusable`; a meta with `model_ok` and `findings_block` true but `api_error: true` posts nothing and logs `scout_unusable`; a scout report with no findings block posts nothing; a second scout exit posts card 2; nothing is posted after `finish_ms`; the watcher exits when both scouts are final | R-38, R-41 |
| T-9 | `test_hook.py` | (a) calls 1-5 deliver nothing, call 6 delivers; (b) the snapshot file equals the transcript and its sha256 file matches; (c) output parses as hookSpecificOutput JSON with `hookEventName == "PostToolUse"` and text at most 1,500 characters; (d) a second pending card is delivered with the card-2 text; two pending cards deliver only the newest and mark the other `superseded`; (e) at or after `finish_ms` the finish text prints once, then nothing, and no card is delivered; (f) input with `agent_id` delivers nothing and logs `subagent_call`; (g) run under `env -i` with only `PATH=/usr/bin:/bin` still delivers (R-21); (h) hook duration is logged | R-19 pattern, R-21, R-41 |
| T-10 | `test_h2.py` | a 250-character anchor is cut to flat length 200, is a prefix of the original and still locates in the candidate; a 350-character claim is cut to 300; bad severity and MINOR-blocking lines are reported as errors (re-ask needed); a re-asked fixture with fewer errors replaces the original, one with more errors does not, and one served by another model (`reask_model_ok: false`) does not and logs `reask_model_mismatch`; `dropped_lines` equals the remaining errors | R-02, R-28 |
| T-11 | `test_cmdline.py` | `DRY_RUN=1 PANEL_COLLAB=0 PANEL_KIT=0` command, tokenised and compared with `run-reviewer.sh:48`, differs only by: no `--no-session-persistence`, the timeout value, the cwd; the brief differs from `run-reviewer.sh:13-17` only by the H1 sentence and the paths; `PANEL_KIT=1` adds exactly the kit text; `PANEL_COLLAB=1` adds `--settings` for the receiver only, the D1 line for the receiver only, and forces the kit; the re-ask command has `--resume` and `--output-format stream-json --verbose` | R-05, R-01, R-39 |
| T-12 | `test_timing.py` | k: (116, 6.4, 6.4) = 2; (116, 6.4, 11.0) = 1; (100, 6.4, 13.8) = 1 and (100, 6.4, 13.9) = 0; (273.7, 14, 23.79) = 2, (273.7, 14, 23.80) = 1, (273.7, 14, 51.79) = 1, (273.7, 14, 51.80) = 0 (the exact thresholds are 23.795 s and 51.795 s; the source's 23.8 and 51.8 are rounded); (238, 23, 12.3) = 1, (238, 23, 12.4) = 0; finish offset (116, 6.4, 6.4) = 143.8; hang offset (273.7) = 410.55; slowdown limit (273.7, k = 2, 14) = 0.1381 and (116, k = 2, 6.4) = 0.1121, each compared with `pytest.approx(value, abs=5e-5)` (exact values 37.795/273.7 and 13/116); the offsets are compared with `pytest.approx` at its default tolerance; `k()` adds 1e-9 before the floor so the exact-boundary cases (100, 6.4, 13.8) and (238, 23, 12.3), which evaluate to exactly 1.0, cannot flip on float rounding | R-41, R-42, R-45 |
| T-13 | `test_timing.py::spike4` | fixture session transcripts with known timestamps give the expected turn durations, turn_p90 and T_report_p90; the values file and its SHA256SUMS line are written; a second write without `--force` is refused | R-30, Spike 4 |
| T-14 | `test_tagger.py` | a receiver finding anchored in a delivered Task is `peer`; anchor2 in a delivered Task is `peer`; other receiver findings and every scout finding are `own`; `requests_acted` counts distinct delivered Tasks with a peer line; the report file is byte-identical before and after tagging | R-10, D7 |
| T-15 | `test_collab.py` | `collab.json` has every R-23 key in A1, A2 and F6 fixtures; F6-only keys are `null` in A1; `finish_would_fire` is true when the receiver's `t_end` is after `finish_ms` | R-23, R-41 |
| T-16 | `test_alarms.py` | fixture where peer-tagged lines raise all-line Jaccard but own-line Jaccard stays under A1 + 0.15: CONVERGENCE does not fire; own-line Jaccard above it fires; `ledger_rows` 21% below A1 fires; deflection overlap 0.51 fires and 0.50 does not; union smaller than the A1 mean fires; SNAPSHOT fires at 2 of 3 receivers missing and not at 1 of 3; SLO: 1 over-cap package in 12 passes, 2 stop the arm; drift 0.96 and 1.11 are flagged | R-24, R-25, R-40, R-45 |
| T-17 | `test_results.py` | synthetic score.json files for DS, AL, CT and a synthetic ground-truth map give the expected `found_14`, `real_blocking_8`, `judge_blocking`, `wrong_blockers`, `control_found_2`, `control_wrong_blockers`, issue labels (GT6 on DS = I1, GT4 on AL = I6, GT1 on CT = I7) and `target_reach` | `MR:22`, `MR:955` |
| T-18 | `test_audit.py` | a synthetic GT whose `plan_quote` shares 12 characters with a test catalogue fails R-07, 11 characters passes; a GT description path present in a template fails; a card with a forbidden key fails "no free text"; a transcript whose tool input reads `.dev/reflect/x` fails, and one that reads `~/.claude/projects/<slug>/<id>.jsonl` fails; a dirty sandbox (`git status` not empty) fails; a changed candidate sha fails | R-07, R-09, `MR:970` |
| T-19 | `test_anon.py` | a fixture merged report with ids `t1b-1`, `t4-1`, `t3-1`, an `EVAL` path, an `R5` path and `/tmp/evalsb-collab-r5/...` comes out with `R1..R3`, `<EVAL>`, `<redacted>` and a zero post-check; an injected `"origin":"peer"` is removed; a claim "applying M7 as the panel request asked, Task 9" comes out with `<redacted>` in both places, and the redaction count is recorded; a ledger heading `#### L1.R2 (m1)` and the prose `Task-6` and `T1bModel01-03` come out with a zero post-check and the package is judged; a report where the post-check still matches is not passed on | R-10, R-29, `MR:953` |
| T-20 | `test_launch_preflight.py` | refused (exit 2): `NOFALLBACK` unset; a panel with `glm-5.3`, `Qwen3.8-max` or `claude-opus-5-5`; judge-one.sh sum wrong (pins file pointed at a fixture copy); worktree and installed parser sums differ; an existing row folder; refused (exit 3): F6 with all k = 0, F6 with `budget_ok: false`, F6 with a values sum mismatch | constraints, R-30, R-39 |
| T-21 | `test_judge_path.py` | the combo argument built by `judge.sh`, joined to `EVAL/arms/scoring/combos/` and resolved with `os.path.realpath`, equals `R5/scoring/<token>`; `judge.sh` refuses when the judge sum differs | D9 |
| T-22 | `test_sandbox.py` | against a temporary git repo with a `.dev/reflect` and `.dev/tasks/done` commit: the built sandbox lacks the four excluded folders, is its own git repo with a clean status, and `--rebuild` refuses a path outside its root | R-03, R-09 |

### 6.2 Fault injection (one test per failure mode, `test_faults.py`, fake `claude`, B values scaled to seconds)

| Id | Injected fault | Expected | Requirement or runbook row |
|---|---|---|---|
| F-1 | receiver sleeps past `hang_ms` (A1 and F6) | killed at T0 + 1.5 B_f (within 2 s), `hang_kill: true`, `slo: SLO_BREACH`, other reviewers unaffected | R-43, `MR:890` |
| F-2 | receiver attempt 1 has no findings block | attempt 2 runs without `--settings` (checked in `FAKE_LOG`), `retry_isolated: true`, `elapsed_s` and tokens sum both attempts, no card delivered in attempt 2 | R-44 |
| F-3 | snapshot copy fails (snap dir made read-only; separately: missing transcript) | `snapshot_missing` logged, zero deliveries for the rest of the run, review completes | R-10, `MR:232` |
| F-4 | corrupt line in `msgs/watcher.jsonl` | hook prints nothing, logs `hook_error`, exits 0; review completes | R-22 |
| F-5 | card posted after the receiver's last tool call | card status `late`; package counted isolated for that receiver | `MR:225` |
| F-6 | scout exits after `finish_ms` | watcher posts nothing (`after_finish`); hook delivers nothing | R-41, `MR:826` |
| F-7 | scout served by another model (`model_ok: false`) | no coverage from it; logged `scout_unusable` | R-28 |
| F-8 | scouts' only findings on Task 12 are surface claims | Task 12 can be requested (it is in the rank list) | `MR:829` (I7 protection) |
| F-9 | receiver's block has a bad-severity line; (a) time left: re-ask through `--resume` with stream-json; (b) no time left: re-ask skipped; (c) the re-ask comes back from another model | (a) `reask_s > 0`, corrected report used; (b) `reask_skipped`, `dropped_lines = 1`; (c) original kept, `reask_model_mismatch` logged | R-02, R-28 |
| F-10 | values file edited after its sum was recorded | `launch.sh` exits 3 before any model call | R-30 |
| F-11 | every reviewer of one package has no valid block | that package `merge_refused`; the other packages merge, judge and appear in the row; status `partial` | R-04 |
| F-12 | judge returns non-JSON | `judge_failed`, status `partial`, no score invented | R-29 |
| F-13 | a reviewer's tool input reads `.dev/reflect/...` | row-package `quarantined`, files kept | `MR:970` |
| F-14 | a reviewer writes a file in the sandbox through Bash | audit fails on `git status`; `quarantined` | R-09 |
| F-15 | a subagent tool call (`agent_id` set) is the first call after a card | no delivery to the subagent; the next main-session call delivers | hook step 1 |
| F-16 | receiver ignores the card (fixture report anchors only scout-covered Tasks) | DEFLECTION fires; nothing else fails | `MR:888` |
| F-17 | receiver keeps calling tools after the finish text | `finish_signal_t` logged once; package elapsed beyond 1.35 B_f is counted in the SLO budget, beyond 1.5 B_f hang-killed | `MR:890` |

### 6.3 Gate 0 spikes this design depends on (real models, recorded in `spikes/NOTES.md` with transcripts under `spikes/out/`, all before any arm, R-27)

| Spike | What it does | PASS when |
|---|---|---|
| S-H3 | `sandbox-build.sh` for all three packages, then the R-03 checks | `SB/<pkg>/repo/.dev/reflect` absent in all three; manifest lists the 3 base SHAs of section 0.2; the DS sandbox has no `refs/merge-guard.md` text from the implemented version; the CT sandbox has `tests/skills/test_worker_contract.py` |
| S0 (receivers: claude-sonnet-5-5, claude-haiku-5-5, gpt-6-luna) | a short `claude -p` task ("run `ls` four times, then reply DONE") with the real settings file; card pre-seeded on a temporary board | the hook fires on every main tool call; the card text appears in the session transcript; the snapshot and sha are written; hook ms p95 recorded; the list of user and project hooks active in `SB/<pkg>/repo` is recorded (user hooks under `~/.claude/settings.json` also fire in every arm, as in today's harness); a subagent call, if the model makes one, carries `agent_id` |
| S2 (resume, for H2) | for each panel model: a run, then `claude -p --resume <session_id> --output-format stream-json --verbose` with a one-line follow-up | the resumed reply answers with the earlier context; the observed model is the same; start cost recorded (planning 6 s, `MR:270`) |
| REQ-S3 (act rates) | 5 trials per receiver model: inject "run `ls /tmp/panel-probe`" at call 3; 5 trials of the finish text at call 3 | per model, the share of trials whose next tool call runs the command, and the share that end within one turn after the finish text; recorded, replacing the 0.5-0.85 planning act rates (R-47). No pass threshold is pre-set; a 0/5 act rate on a receiver model is reported and the owner decides whether that panel's F6 arm runs |
| Spike 4 | 4 A1 launches per panel (`SPIKE4=1 PANEL_COLLAB=0 PANEL_KIT=0`, rows `s4-a1-<panel>-r1..r4`) and 2 A2 launches (`PANEL_KIT=1`); then `timing.py spike4` | values files written with sums: B_A1 (median panel elapsed per package), turn_p90 and T_report_p90 of the receiver role from the copied session transcripts (with 4 runs, p90 is close to the maximum; stated in the values file), k, offsets, the kit slowdown s on the receiver and `budget_ok`. Committed before the first arm (R-30) |
| S3 = smoke (6.4) | full chain on one package | section 6.4 |

S1 (SendMessage) is not needed: F6 uses no SendMessage. Spike 5 (re-scoring the 30 cheap historical runs with the normaliser) is not an F6 input and is not built here, but R-27 gates every arm on it (`MR:1059`), so AC-4 requires its result to be recorded by the shared plan before the first non-spike row (section 7.2, Q5).

### 6.4 One-package smoke test

```bash
cd REPO && export NOFALLBACK=1
PANEL_COLLAB=1 bash R5/bin/launch.sh sl2 smoke-f6-sl2-1 --pkgs TASK-WF-design-20261108-041415
PANEL_COLLAB=0 PANEL_KIT=0 bash R5/bin/launch.sh sl2 smoke-a1-sl2-1 --pkgs TASK-WF-design-20261108-041415
```

Run after S-H3, S0, S2 and Spike 4. PASS when every item holds:

1. Exit code 0 for both rows; `results/smoke-*.json` exist with `status: complete`.
2. `model_ok: true` on every final attempt; observed models are the panel's.
3. Zero dropped findings lines after H2 (`dropped_lines = 0`), and the merge lists all 3 reviewer ids (S3, R-04).
4. F6 row: at least one card posted and delivered (`cards_delivered >= 1`), `snapshot_missing = 0`, `hook_error = 0`, the card's rendered text in the receiver's transcript after the seal time, the card JSON passes the validator, and the receiver's snapshot sha equals the recorded one.
5. A1 row: no `board/` folder, no `--settings` in any recorded command, `collab.json` present with F6 fields `null`.
6. `merged-anon.md` post-check is 0; `score.json` exists and parses; `audit.json` passes.
7. `elapsed_s` of the F6 row is at most 1.5 B_f (no hang kill).

### 6.5 Acceptance criteria (pass/fail; the build is accepted only when all pass)

| Id | Criterion |
|---|---|
| AC-1 | `mkdir -p /tmp/evalsb-collab-r5 && PYTHONPATH=R5/lib uv run pytest -p no:cacheprovider --basetemp=/tmp/evalsb-collab-r5/pytest R5/tests` (from `REPO`) passes with 0 failures and 0 skips, covering T-1 to T-22 and F-1 to F-17. |
| AC-2 | Nothing outside `R5/` and `SB/` is written by the build or the smoke test, apart from the session files Claude Code itself writes under `~/.claude/projects/`: `git status --porcelain -- src/ .claude/` is empty; `find EVAL -newer R5/.build-start` and `find REPO -maxdepth 1 -newer R5/.build-start` print nothing (`.build-start` is touched before the build); `grep -rnE 'r[1-4]-(move-radar|idle-shift|axis-flip|flag-and)' R5/bin R5/lib R5/config` finds no path into another redesign's folder. |
| AC-3 | `sha256sum EVAL/tools/tmp-scripts/judge-one.sh` still equals `a01bd70d370d73cb32b55a7368aa28e2c12d93403237211c3a71f339ae82cfcc` after the smoke test. |
| AC-4 | `spikes/NOTES.md` records S-H3, S0, S2 and Spike 4 with PASS, and REQ-S3 with its measured act rates plus the owner's run or no-run decision for any receiver model with a 0/5 rate, each dated before the first non-spike row's T0; a recorded Spike 5 result from the shared plan (or the owner's recorded waiver, Q5) is referenced there before that row. |
| AC-5 | The smoke test of 6.4 passes all 7 items. |
| AC-6 | T-11 shows the A1 command and brief differ from `run-reviewer.sh` only by the allowed R-05 differences. |
| AC-7 | `audit.py static` passes: no 12-character ground-truth quote and no GT description path in the catalogue, templates or regex. |
| AC-8 | No reviewer command recorded in any `FAKE_LOG` or real `launch.json` uses a model outside the allow-list, and every real launch ran with `NOFALLBACK=1`. |
| AC-9 | Every F6 card in the smoke board has only the keys of 2.2 and at most k items; no card was posted or delivered at or after `finish_ms`. |
| AC-10 | `launch.sh hl2 <row>` with `PANEL_COLLAB=1` and k = 0 on all packages exits 3 with the reason; `launch.sh` on `el2` delivers at most one card to each luna in a fixture run. |

## 7. Risks and open questions

### 7.1 Risks

| Risk | Effect | Mitigation in this design |
|---|---|---|
| Sonnet's final report turn is too long (about 30k output tokens per run, `MR:847`) | k = 0 and the arm does not run at all | Spike 4 measures it first; `launch.sh` exits 3 instead of running a hollow arm |
| On `hl2`, k = 0 is near certain at planning values (section 3.2) | No F6 data for haiku + 2x luna | Reported as "not runnable" with the measured T_report_p90; A1-HL2 and A2-HL2 still run |
| A Task-level mapping misses defects that sit in Constraints or in cross-Task text (for example I6, which needs a check carried from one Task to others) | Those defects are never requested | Accepted by the source's form ("uncovered Task ids only", `MR:851`); the per-issue reach comparison against A1 shows it |
| The surface pattern is too broad and marks real findings surface | More requests on Tasks a scout really covered (less deflection) | Errs on the harmless side (D5); `board/coverage.jsonl` keeps every classification for the spot-check audit (`MR:887`) |
| The surface pattern misses a new surface phrasing | A Task is marked covered and the receiver is steered away (the I7 failure) | Spot-check audit; T-4 fixtures; extend `surface.regex` between arms only, never during one (its sha is pinned per row) |
| Hook-injected text is weighed differently by gateway models (luna on `el2`) | Cards ignored; C goes to 0 | S0 and REQ-S3 measure delivery and act rate on luna before any `el2` arm |
| PostToolUse fires inside subagents | A card could land in a subagent and be lost | Hook skips calls with `agent_id` (F-15) |
| The transcript file lags the session (the docs say writes are asynchronous) | The seal snapshot may miss the last turn before delivery | Accepted: the snapshot is an integrity log, and the source already measures mid-run C at arm level only (`MR:232`) |
| User-level hooks in `~/.claude/settings.json` run in every reviewer session (today's harness has the same property) | Extra latency and extra context in every arm | Equal across arms; S0 records the list; `--setting-sources` is not used because it is not an allowed R-05 difference |
| The installed `superclaude` tool and the worktree parser drift | H2 validates against a parser the merge does not use | D10 pin check refuses the launch |
| The judge sees the path `.../r5-coverage-deflection/scoring/<token>` | Reveals the redesign, not the arm | The same folder holds A1, A2 and F6 rows; tokens are random |
| Gateway load drift between arms | Time and quality differences that are not the design | Block-wise concurrent launches (5.6); drift band of R-45 |
| Small samples (n = 12) | The plan cannot detect the central gain estimates (`MR:980`) | Not fixable here; reported as the source states |

### 7.2 Open questions for the owner (one recommendation each)

- **Q1. Brief of the F6 arm.** This design gives every F6 reviewer the static kit (D1), so F6 is compared with A2-SL2 on the exchange alone. The alternative is F6 = A1 brief plus cards, which then needs the catalogue inside each card (over the 1,500-character per-call cap) or a card without move text. Recommendation: keep D1.
- **Q2. What to do if Spike 4's kit slowdown on the receiver exceeds the limit** (13.8% on SL2 at k = 2). The source says "drop brief content until it fits" (`MR:301`) but does not say which content. Recommendation: drop the kit to the moves the catalogue marks "search" or "either" for a searcher receiver and "reading" or "either" for a reader receiver, re-measure once, and stop if it still does not fit.
- **Q3. Panels `hl2` and `el2`.** The source pre-registers F6 only on `sl2`. Recommendation: run `el2` and `hl2` as exploratory rows only after the `sl2` screen, and do not apply the stage-2 decision rule to them.
- **Q4. Shared analysis.** The block scheduler, the interim futility look, and the Fisher and permutation tests of section 4 are common to all five redesigns and are not built here. Recommendation: build them once, outside the redesign folders, reading every redesign's `results/results.jsonl`.
- **Q5. Spike 5.** R-27 gates every arm on Spike 5, which measures the H2 share on cheap historical runs and is not an F6 input. Recommendation: run it once in the shared plan and reference its record here; do not build a copy in this folder.

### 7.3 Not checked by this design (UNVERIFIED until the named spike)

Hook firing, hook cost and act rate on each receiver model (S0, REQ-S3); `--resume` on the gateway models (S2); every timing value and k (Spike 4); whether gateway models make subagent calls during review (S0); the token overhead of F6 on any panel (the arms' measured output tokens, `MR:1122`).
