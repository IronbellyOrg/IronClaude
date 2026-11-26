# Redesign 1: Move Radar (F3): implementation and test design

Grounding: index_state: fresh (checked_at 2026-11-13T19:30:46Z, projectPath /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel); codegraph_status, codegraph_node (symbolsOnly outlines of `src/superclaude/cli/review/findings.py` and `merge_cmd.py`); every quoted line was then Read from disk. Shell scripts and markdown are not indexed, so the harness was read with Read and Bash.

## 0. Scope, sources and conventions

**What this is.** A build specification for Redesign 1, Move Radar (family F3, slot 3, arm A6), plus its isolated baseline (arm A1) on three panels. An implementer builds from this file alone. Nothing here is implemented yet.

**Path abbreviations** (absolute paths; every script bakes them in, nothing is read from the environment except the two launch switches `PANEL_COLLAB` and `NOFALLBACK`):

| Name | Absolute path |
|---|---|
| `REPO` | `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel` |
| `R1` | `REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar` |
| `A1DIR` | `REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1` (read only: candidates, resolutions, ground truth for the judge and the results builder, the unchanged `judge-one.sh`) |
| `SB` | `/tmp/evalsb-collab-r1` (this redesign's sandbox root; no other redesign writes here) |
| `SRCREQ` | `REPO/.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md` (the source of truth) |

Packages: `DS` = `TASK-WF-designSpec-20261107-075614`, `AL` = `TASK-WF-makeTheAliasOnly-20261105-051649`, `DE` = `TASK-WF-design-20261108-041415` (the control package).

**Source requirements this design implements.** `SRCREQ` §2.0 (catalogue, `panel-msg/1`, board, seals, convergence alarm, kill switch, timing rules, H1-H4), the Redesign 1 section (a)-(h), §4 (Gate 0, conduct, audits), R-01..R-10, R-21..R-30, R-31..R-33 and R-41..R-47. Where this design narrows or adapts a source rule, the text says "Adaptation" and section 7 lists it.

**Hard limits carried into every script.**

- Writes go only under `R1/` and `SB/` (plus the reviewers' own Claude session files, deleted by `cleanup-sessions.sh`). No write to `src/`, to `A1DIR`, or to any other redesign folder. The judge's outputs reach `R1/scoring/` through a path that starts in `A1DIR` but resolves into `R1` (section 5.3); nothing is created under `A1DIR`.
- Models: ember `muse-ember-1.0`, luna `gpt-6-luna`, haiku `claude-haiku-5-5`, sonnet `claude-sonnet-5-5` as reviewers; `claude-opus-5-5` only inside the unchanged `judge-one.sh`. No Qwen, no glm. grok is allowed but no panel here uses it. The R1 reviewer runner has **no fallback ladder at all**; `launch.sh` exports `NOFALLBACK=1` and refuses to start if the caller set it to anything else.
- Reviewers are read-only (`--disallowedTools Edit Write NotebookEdit`, audited by `git status` in the sandbox and the candidate sha256, R-09) and never see ground truth (the sandbox excludes `.dev/eval-workspaces`, `.dev/research`, `.dev/reflect` and `.dev/tasks/done`; candidates are copied out to `SB/cand/`).
- Python runs only as `uv run python <script>` or `uv run pytest`, from `REPO`, so `superclaude.cli.review.findings` imports from the project environment.

**What is deliberately not built** (not needed by F3): no `panel-post` helper (no model writes to the board in F3); no peer tagger (F3 delivers no anchor and no locator, so every findings line is `own` by construction and no `origin` key is ever added, so the anonymiser has none to strip); no Stop hook; no fallback ladder; no scheduler across the five redesigns (section 7, risk K-8).

## 1. Files to create

All paths are under `R1/`. Shell scripts use `#!/usr/bin/env bash` and `set -u -o pipefail` (no blanket `set -e`, matching `A1DIR/tools/run-reviewer.sh`). Hook-path scripts use only bash, coreutils, `flock`, `sha256sum` and `jq` 1.7 (installed), because a `uv run` start on every tool call is too slow. Offline steps are Python run with `uv run python`.

### 1.1 Configuration and frozen inputs

| Path | Purpose | Interface / content |
|---|---|---|
| `config/panels.json` | The three panels and their roles (section 3). | `{"el2":{"critical_role":"reader","planning_B":116,"roles":{"searcher":{"rid":"t2b-1","model":"muse-ember-1.0","checkpoints":[6,10],"planning_turn":3.2},"reader":{"rids":["t4-1","t3-1"],"model":"gpt-6-luna","checkpoints":[8,12],"planning_turn":6.4}}}, "sl2":{...sonnet t1b-1...}, "hl2":{...haiku t2-1...}}` plus a `resolution` block per reviewer id copied from `A1DIR/analysis/merge-b11.sh:11-12` (tier and alias: `t1b-1` tier1b `claude-gw-tier1b[1m]`, `t2-1` tier2 `claude-gw-tier2[1m]`, `t2b-1` tier2b `claude-gw-tier2b[1m]`, `t3-1` tier3 `claude-gw-tier3[1m]`, `t4-1` tier4 `claude-gw-tier4[1m]`). |
| `config/catalogue.json` | Frozen move texts (R-07). | `{"version":"r1-cat/1","moves":{"M1":"<text>",...,"M10":"<text>"},"observable":["M1","M2","M4","M7"],"observable_suffix":" No panel member has done this yet.","src_text":"source.md has not been opened yet: open the plan's source document named in your brief and read it.","finish_text":"Finish now with what you have: write your final report, ending with the findings block and the verdict line."}`. Move texts are copied **verbatim** from the "Move (text sent to a reviewer)" column of `SRCREQ` §2.0 (lines 184-193). Every rendered injection is at most 300 characters (move text plus suffix for an observable move). |
| `config/catalogue.sha256` | Pin of the catalogue (R-07). | One line, `sha256sum config/catalogue.json` output; checked by `launch.sh` preflight. |
| `config/brief.txt` | The reviewer brief template, H1 applied. | Byte-identical to the `BRIEF=` text of `A1DIR/tools/run-reviewer.sh:13-17` with the placeholders `@@CAND@@`, `@@SHA@@`, `@@SRC@@`, `@@SRCSHA@@`, and one inserted sentence right after "(sha256 of the file: @@SHA@@) against the requirements it states, review 1 of 3.": `The plan's source document is @@SRC@@ (sha256 of the file: @@SRCSHA@@); read both the candidate and the source document.` Nothing else changes. Identical in both arms (so the brief slowdown s of R-45 is 0 for F3 by construction). |
| `manifest.json` | Pins and base commits (R-03, R-07, R-30). | `{"base_commits":{"<pkg>":{"sha":"<40 hex>","method":"t1-start|squash-first-parent","t1_start":"<sha from progress.md>"}},"catalogue_sha256":"…","brief_sha256":"…","judge_one_sha256":"<sha256 of A1DIR/tools/tmp-scripts/judge-one.sh>","merge_cli":"superclaude review merge","created_utc":"…"}`. Written by `spikes/g-base.sh` and `spikes/g-pins.sh`; never edited by a run. |
| `values/<panel>/<pkg>.json` | Spike 4 values (R-30, timing rule 6). | `{"panel","pkg","B_f","turn_p90":{"searcher":s,"reader":s},"T_report_p90":{...},"E_p90":{...},"critical_role","finish_offset_s","guard_offset_s","hang_offset_s","k":{"searcher":n,"reader":n},"source_runs":[row ids],"computed_utc"}` plus `values/<panel>/<pkg>.json.sha256`. Written once by `tools/values.py spike4`; `launch.sh` refuses `PANEL_COLLAB=1` without it and never rewrites it. |

### 1.2 Tools

| Path | Purpose | Interface |
|---|---|---|
| `tools/sandbox.sh` | Builds the per-package sandbox (H3, H4) and the candidate copies (H1). Idempotent. | `sandbox.sh <pkg>`. Creates `SB/<pkg>/repo` = `git -C REPO archive <base sha from manifest>` extracted, minus `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research`, `.dev/reflect`; then `git init -q && git add -A && git commit -qm snapshot` inside it (own throwaway repo, as `A1DIR/manifest.md` describes, so the `git status` audit works). Copies `A1DIR/<pkg>/candidate.md` and `REPO/.dev/tasks/done/<pkg>/source.md` to `SB/cand/<pkg>/`. Writes `SB/<pkg>/repo.ok` with the base sha. Refuses (exit 2) if `SB/<pkg>/repo.ok` names a different sha. |
| `tools/radar-index.sh` | Per-package index of the candidate, used by the classifier (no ground truth). | `radar-index.sh <pkg>` writes `R1/index/<pkg>.json`: `{"paths":[repo-relative paths named in candidate.md that exist in SB/<pkg>/repo or are created by a Task],"keys":[basename stems of those paths, length >= 4],"task_of_path":{"<path>":["T3",...]},"tasks":["T1",...],"criterion_greps":["<pattern>",...],"root_files":[names of regular files at SB/<pkg>/repo root]}`. Tasks come from `^## Task (\d+):` headings (verified format in all three candidates); a path belongs to the Task whose section contains it. `criterion_greps` are the pattern arguments of every backticked `grep …` command in the candidate (first quoted argument, else first non-option token after `grep`). |
| `tools/radar-classify.jq` | The deterministic classifier (R-31): one tool-call record in, a list of signature ids out. | `jq -c --slurpfile ix index/<pkg>.json --arg srcpath <SB/cand/<pkg>/source.md> -f radar-classify.jq` over a stream of tele records; emits `{"n":…,"sig":["M1","M7",…]}`. Signature ids: `M1`, `M2`, `M4`, `M7`, `SRC_OPENED`, `UNNAMED_TEST`. Rules in section 2.3. Never emits M3, M5, M6, M8, M9 or M10. |
| `tools/radar-hook.sh` | The PostToolUse hook: telemetry, checkpoint logic, seal, injection, finish signal (section 2.4). | Called by Claude Code with the hook JSON on stdin. All parameters are positional arguments baked into the command string by `settings-gen.sh`: `radar-hook.sh <BOARD> <RUN> <RID> <ROLE> <T0_MS> <FINISH_MS> <GUARD_MS> <K> <CP1> <CP2> <ORDER> <PKG> <CLOCK_FILE>`. `ORDER` is a comma list of move ids for this receiver (section 2.5). `CLOCK_FILE` is the empty string in production; tests pass a file whose content is the current time in ms. Prints either nothing or one JSON object `{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"<text>"}}`; always exits 0. |
| `tools/settings-gen.sh` | Writes the per-reviewer `--settings` JSON (R-21). | `settings-gen.sh <args as radar-hook.sh>` prints `{"hooks":{"PostToolUse":[{"matcher":"*","hooks":[{"type":"command","command":"bash <R1>/tools/radar-hook.sh '<BOARD>' '<RUN>' … ''","timeout":5}]}]}}`. Every value single-quoted; no `$` in the output (asserted by test). |
| `tools/msg-validate.sh` | `panel-msg/1` validator restricted to what F3 emits (R-06, R-08, leak lookup of (e)). | Reads lines on stdin, prints each valid line to stdout and each rejected line to stderr as `{"reject":"<reason>","line":…}`; exit 0 if all valid, 1 otherwise. Rules in section 2.2. Used by the hook before every append, and by `collab_summary.py` over the whole board after the run. |
| `tools/run-reviewer.sh` | R1's own reviewer launcher, derived from `A1DIR/tools/run-reviewer.sh` (section 2.7). | `run-reviewer.sh <row> <pkg> <rid> <model> <collab 0|1> <T0_MS>`; reads `config/brief.txt`, the values file (or planning values for collab 0, section 4), writes into `R1/runs/<row>/<pkg>/reviews/`. Also `run-reviewer.sh --print-cmd …` prints the exact `claude` argv for attempt 1 and exits (used by the R-05 diff test). |
| `tools/h2_normalize.py` | H2 (R-02): truncate, validate with the real parser, list remaining errors. | `uv run python tools/h2_normalize.py <in.md> <out.md> <errors.json>`: imports `superclaude.cli.review.findings` (`parse_block`, `flat`); for each line of the last findings-v1 block, replaces `anchor` and `anchor2` by `flat(x)[:200].rstrip()` and `claim` by `flat(x)[:300].rstrip()` when longer; writes the report with only the block rewritten; runs `parse_block` on the result and writes `{"ok":bool,"errors":[{"line","msg"}],"truncated":n}`. Exit 0 always (the caller reads `ok`). |
| `tools/values.py` | Timing values: k, PANEL_FINISH_AT, guard, hang guard; Spike 4 aggregation (section 2.6). | `uv run python tools/values.py spike4 <panel> <row> [<row> …]` writes `values/<panel>/<pkg>.json` for the 3 packages from A1 rows (refuses fewer than 3 rows, and refuses to overwrite). `uv run python tools/values.py show <panel> <pkg>` prints the values or the planning fallback. Pure functions `k_for(...)`, `finish_offset(...)`, `guard_offset(...)` are imported by tests. |
| `tools/collab_summary.py` | Two passes per package: `collab.json` (R-23), audits (R-09, leak lookup, §4 rule 5), alarm inputs, quarantine. | `uv run python tools/collab_summary.py pre <row> <pkg>` runs after the reviewers and before the merge: audits and leak lookup, writes `audit.json` and a first `collab.json`; on a hard audit failure writes `runs/<row>/<pkg>/QUARANTINED` (one line: reason) and exits 3. `uv run python tools/collab_summary.py post <row> <pkg>` runs after the anonymiser: adds `ledger_rows` (from `ledger.json`) and `anon_leak` (from `merged-anon.md`) and rewrites `collab.json` and `audit.json` whole. |
| `tools/anon.sh` | Anonymiser for one merged report (adapted from `A1DIR/tools/tmp-scripts/anon-b11.sh`). | `anon.sh <row> <pkg>` → `R1/scoring/<opaque>/<pkg>/<L>/merged-anon.md`, with `<opaque>` a fresh 12-hex token and `<L>` one letter from Q..V; writes the key `R1/runs/<row>/<pkg>/label-key.json` = `{"opaque","label"}` (never under `scoring/`). |
| `tools/results.py` | The results row (section 5.4). | `uv run python tools/results.py <row>` reads the three packages' `score.json`, `collab.json`, cost files and ground truth (for `blocking_in_implement` only); writes `results/<row>.json` and appends one line to `results/results.jsonl` (refuses to append a row id that is already there). |
| `tools/launch.sh` | The one launch script (section 5). | `PANEL_COLLAB=<0|1> bash tools/launch.sh <panel> <rep> [<pkg> …]`. |
| `tools/cleanup-sessions.sh` | R-46. | `cleanup-sessions.sh <row>`: deletes only the session files whose ids are listed in that row's `reviews/<rid>.meta.json` (`session_ids`, written as soon as each id is known) and `collab.json` files, from `~/.claude/projects/<encoded SB/<pkg>/repo path>/<id>.jsonl`; never a directory. |
| `tools/alarms.py` | Arm-level alarms and the time verdict over many rows (R-24, R-25, R-45). | `uv run python tools/alarms.py <panel>` reads `results/results.jsonl`, prints per arm (collab 0 / 1): CONVERGENCE fire count, SLO budget spent, `baseline_drift`, SNAPSHOT alarm, median overhead per package. Read-only. |

### 1.3 Gate 0 spikes (section 6.3)

| Path | Spike | Output |
|---|---|---|
| `spikes/g-base.sh` | Base commit per package (H3). | Fills `manifest.json` `base_commits`. |
| `spikes/g-pins.sh` | sha256 of catalogue, brief, `judge-one.sh`; catalogue ground-truth check (R-07). | Fills the pins in `manifest.json`; `spikes/g-cat.json`. |
| `spikes/s0-hooks.sh` | S0 on all four reviewer models. | `spikes/s0/<model>.json`. |
| `spikes/s2-resume.sh` | S2 for the H2 re-ask on all four models. | `spikes/s2/<model>.json`. |
| `spikes/reqs3-actrate.sh` | REQ-S3 act rates (injected item and "finish now"). | `spikes/reqs3.json`. |
| `spikes/spike4.sh` | Spike 4: runs A1 rows, then `values.py spike4`. | `values/<panel>/<pkg>.json`. |
| `spikes/gate0-check.sh` | Reads every spike record and decides each pass condition of section 6.3. | `spikes/gate0.json` = `{"<spike>":"pass|fail|recorded", "checked_utc"}`; `launch.sh` enforces the gate order of section 6.3. |

### 1.4 Tests

`tests/` holds `conftest.py` (fixtures: temp board, fake `claude` executable put first on `PATH` by the test, fixed clock file), `fixtures/` (a small candidate with three `## Task N:` sections and two backticked grep criteria, tele records, findings reports, a fake ground truth with two items, a fake `judge-one` brief target) and the test modules listed in section 6. Run from `REPO`: `uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests -q`. `bats` is not installed on this host, so shell scripts are tested through `subprocess` in pytest.

### 1.5 Run outputs (created by runs, never by hand)

```text
R1/runs/<row>/run.json                      panel, collab, rep, start time, values sha256 per package
R1/runs/<row>/<pkg>/run.json                T0_MS, FINISH_MS, GUARD_MS, HANG_MS, k per role, order per rid
R1/runs/<row>/<pkg>/settings/<rid>.json     the exact --settings JSON passed (collab 1 only)
R1/runs/<row>/<pkg>/reviews/<rid>.*         attempt<n>.json/.err/.md/.meta.json, reask.*, norm.md, h2.json, cost.json, md, meta.json
R1/runs/<row>/<pkg>/board/                  BOARD (R-26): tele/<rid>.jsonl, msgs/radar.jsonl, metrics/<rid>.jsonl,
                                            snap/<rid>.jsonl + snap/<rid>.sha256, state/<rid>.{count,lock,sealed,finish}
R1/runs/<row>/<pkg>/resolution.json, ledger.json, merged-1.md, merge-stdout.txt
R1/runs/<row>/<pkg>/collab.json, audit.json, label-key.json, [QUARANTINED]
R1/scoring/<opaque>/<pkg>/<L>/merged-anon.md, judge.json, judge.err, score.json
R1/results/<row>.json, R1/results/results.jsonl
```

Row id: `<panel>-c<collab>-r<rep>`, for example `el2-c1-r3`. Raw transcripts and snapshots (`reviews/*.attempt*.json`, `board/snap/`) are large; following `A1DIR/analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md`, they are kept on disk and listed, and whether they are committed is the owner's choice (section 7, Q-6).

## 2. Behaviour

### 2.1 One package, end to end

1. **Preflight** (`launch.sh`): pins match `manifest.json`; sandbox built (`sandbox.sh`); index built (`radar-index.sh`); values loaded (section 2.6).
2. **T0.** `T0_MS = $(date +%s%3N)`. From the values: `FINISH_MS = T0 + 1000 × finish_offset`, `GUARD_MS = T0 + 1000 × guard_offset`, `HANG_MS = T0 + 1000 × hang_offset`. Written to `runs/<row>/<pkg>/run.json` before any reviewer starts.
3. **Launch.** The three reviewers of the panel start concurrently (`run-reviewer.sh … &`, then `wait`). With `PANEL_COLLAB=1` each gets its own `--settings` JSON; the radar hook runs inside each session.
4. **During the run** each tool call of each reviewer appends one telemetry line to the board; at the reviewer's checkpoints the hook may inject one item (section 2.4).
5. **After each reviewer's main session:** H2 normalise, at most one re-ask, normalise again (section 2.7).
6. **After all three:** `collab_summary.py pre` (audits, quarantine), merge, anonymise, `collab_summary.py post` (ledger rows, anonymiser leak count), judge.
7. **After the three packages:** `results.py` writes the row; `cleanup-sessions.sh` removes this row's session files.

No reviewer ever waits for a peer. Nothing is delivered after a reviewer's last tool call, so `late` is always 0 in F3 (the hook injects synchronously on a call or not at all).

### 2.2 Message schema (`panel-msg/1`, F3 subset) and validator

Every injection is first written to `board/msgs/radar.jsonl` as one `panel-msg/1` line, then rendered as text. F3 lines are harness-authored and have exactly these keys:

```json
{"v":"panel-msg/1","id":"m-t4-1-08","run":"el2-c1-r3/TASK-WF-designSpec-20261107-075614","from":"radar","to":"t4-1","t":1763062000123,"kind":"move","move":"M5"}
```

- The `source.md` check is the same line **without the `move` key** (the source gives the check no move id and R-07 allows only M1-M10 in `move`; Adaptation, Q-4). The "finish now" signal is **not** a board message: it is logged in `metrics/<rid>.jsonl` as `{"ev":"finish"}` and its text is the fixed `finish_text`.
- `id` = `m-<rid>-<two-digit tool-call number>`.

`msg-validate.sh` accepts a line only if all hold, else rejects with the reason in brackets:

| Rule | Reject reason |
|---|---|
| Serialised line is at most 600 bytes | `too_long` |
| Valid JSON object | `not_json` |
| Keys are a subset of `v,id,run,from,to,t,kind,move` (F3 never uses `anchor`, `items` or `n`, so they are rejected here; the forbidden keys `claim`, `verdict`, `blocking`, `severity`, `category`, `note` fall under the same rule) | `bad_key:<key>` |
| `v == "panel-msg/1"`, `from == "radar"`, `kind == "move"`, `to` is one of the panel's reviewer ids, `t` an integer | `bad_field:<key>` |
| `move` absent, or one of `M1`..`M10` | `bad_move` |
| Leak lookup (Redesign 1 (e)): the text the hook rendered for the line is exactly `moves[move]` (plus `observable_suffix` if `move` is observable and the receiver is the searcher), or `src_text` when `move` is absent | `leak` |

The hook passes the rendered text alongside the line (`{"line":…,"text":…}` on stdin) so the leak lookup checks what the model actually receives, and it stores that exact text in the `inject` metrics event (`"text"` and `"text_sha256"`, joined to the board line by `id`). Any rejection inside the hook means nothing is injected and `hook_error` is logged. After the run, `collab_summary.py pre` re-runs the validator over every (board line, logged text) pair, and also flags an `inject` event with no board line or a board line with no `inject` event; any rejection there is a **hard failure** (Redesign 1 (h)): it writes `QUARANTINED` and the package is excluded from results (quarantine in place, nothing deleted, R-26).

### 2.3 Classifier signatures (`radar-classify.jq`, R-31)

Input record (one per tool call, written by the hook to `board/tele/<rid>.jsonl`): `{"n":<call number>,"t":<ms>,"rid":"…","sub":false,"tool":"<tool_name>","input":<tool_input with every string cut to 2000 chars>}`. `sub` is true when the hook stdin carries a non-null `agent_id` (a subagent call): such calls are logged but never counted toward checkpoints and never classified as panel coverage.

Let `cmd` = `input.command` for Bash; for the Grep tool, `pat` = `input.pattern`, `gpath` = `input.path` (absent means the session cwd, which is the sandbox repo root); for Read, `fp` = `input.file_path`. Paths are compared after stripping the prefix `SB/<pkg>/repo/` and a leading `./`.

| Signature | Fires when |
|---|---|
| `M1` | (Bash `cmd` matches `\b(grep|egrep|rg)\b` with a recursive flag (`-r`, `-R`, `--recursive`, or `rg`) **and** a path argument equal to or under `tests` **and** the command contains any `paths[]` entry or any `keys[]` entry) or (Grep tool with `gpath` equal to or under `tests` and `pat` containing a `paths[]` or `keys[]` entry). |
| `M2` | Bash `cmd` contains `grep -l`, `grep -c`, `grep -L`, combined short flags containing `l` or `c` after `grep -`, `find `, or a pipe into `wc -l` (`\|\s*wc\s+-l`); or Grep tool with `input.output_mode` in `files_with_matches`, `count`. |
| `M4` | Bash grep or Grep tool whose pattern, with surrounding quotes removed, equals one of `criterion_greps[]`. Bash pattern = first quoted argument after `grep`, else first token after `grep` that does not start with `-`. |
| `M7` | A recursive search from the repository root: Bash recursive grep/rg whose path argument is `.`, `./`, the absolute repo root, or absent for `rg`; or Grep tool with `gpath` absent or equal to the repo root; or any search command naming a `root_files[]` entry (for example `CHANGELOG.md`) as a path argument. |
| `SRC_OPENED` | Read with `fp` ending in `/cand/<pkg>/source.md`, or Bash `cmd` matching `\b(cat|sed|head|tail|less|nl|awk)\b` and naming that path. |
| `UNNAMED_TEST` | Read with `fp` under `tests/` and not in `paths[]`. |

One record may yield several signatures. Unobservable moves are never emitted; therefore the text "No panel member has done this yet" can only accompany M1, M2, M4 or M7 (R-31). The classifier runs live in the hook (panel coverage) and post hoc in `collab_summary.py` over the same telemetry (move executed, audit spot-check), and post hoc over the `--output-format json` transcripts of collab-0 rows (the tool_use blocks are in that output), so the baseline gets the same coverage counters without hooks.

### 2.4 The radar hook (`radar-hook.sh`)

Per call, under `flock state/<rid>.lock`:

1. Read stdin (at most 1 MB). Any error from here on: trap → append `{"ev":"hook_error","t","msg"}` to `metrics/<rid>.jsonl` if possible, print nothing, exit 0 (R-22).
2. `now` = `CLOCK_FILE` content if `CLOCK_FILE` is non-empty, else `date +%s%3N`.
3. If `agent_id` is non-null: append tele with `sub:true`, exit 0.
4. `n` = `state/<rid>.count` + 1 (write back). Append the tele record with one `printf '%s\n' … >>` call (one small write with O_APPEND; readers skip unparsable lines with `fromjson? // empty`, so a torn or corrupt line never breaks a hook, R-22).
5. **Finish signal.** If `now >= FINISH_MS` and `state/<rid>.finish` is absent: create it, log `{"ev":"finish","t":now,"n":n}`, print the `finish_text` injection, exit 0. After `FINISH_MS` nothing else is ever injected.
6. **Checkpoint test.** Eligible checkpoints = the first `K` of `[CP1, CP2]`. If `n` is not an eligible checkpoint, or the count of `inject` events for this rid is already `K`, exit 0. If `now >= GUARD_MS`: log `{"ev":"skip","reason":"guard","n"}` and exit 0.
7. **Seal (fail closed).** If `state/<rid>.sealed` is absent: copy `transcript_path` (from stdin) to `snap/<rid>.jsonl`, write `sha256sum` to `snap/<rid>.sha256`, log `{"ev":"seal","t","sha256"}`, create `state/<rid>.sealed` containing `ok`. If any part fails: write `state/<rid>.sealed` containing `failed`, log `{"ev":"snapshot_missing","t"}`, exit 0. A rid whose sealed state is `failed` never receives anything for the rest of the package.
8. **Choose the item** (section 2.5). If nothing qualifies: log `{"ev":"skip","reason":"no_gap","n"}`, exit 0 (the checkpoint is used, K is not).
9. **Task hint.** Every `paths[]` entry that appears in this call's input string maps through `task_of_path` to Task ids; log them as `task_hint` in the inject event only (R-32). They never enter the message.
10. Build the line (section 2.2), validate it with `msg-validate.sh`; on reject log `hook_error` and exit 0. Else append it to `msgs/radar.jsonl`, log `{"ev":"inject","id","t","n","move":"M5"|null,"slot_type":"search|static|src","task_hint":[…],"text":"<rendered text>","text_sha256":"…"}` and print `{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"<text>"}}` (the documented PostToolUse output shape; plain stdout is not shown to the model for PostToolUse, so the JSON form is mandatory).

`slot_type`: `src` for the source.md check, `search` for an observable move to the searcher (booked to C), `static` for a reading move to a luna (booked to P, R-33).

Cost: the classifier runs only at a checkpoint (at most 2 per reviewer), over at most a few hundred tele lines; every other call is steps 1-6 only. On every exit path the hook appends `{"ev":"t","n","ms":<its own run time>}` to `metrics/<rid>.jsonl` (start time taken at step 2), from which `hook_ms_p95` is computed; S0 and every collab-1 row record it.

### 2.5 Item choice and receiver order

- **Order.** For each receiver, `ORDER` is its role list rotated left by `int(sha256(rid)[0:8], 16) mod len(list)`. Searcher list `[M1, M2, M7, M4]`, reader list `[M3, M5, M6, M9, M8, M10]` (the source's table order). Computed by `launch.sh` and baked into the hook command. Worked values (computed with `printf %s <rid> | sha256sum`): `t4-1` → offset 0 → M3, M5, M6, M9, M8, M10; `t3-1` → offset 4 → M8, M10, M3, M5, M6, M9; so the two lunas never get the same move at the same checkpoint. Searchers: `t2b-1` (ember) offset 1 → M2, M7, M4, M1; `t1b-1` (sonnet) offset 2 → M7, M4, M1, M2; `t2-1` (haiku) offset 0 → M1, M2, M7, M4.
- **source.md check first.** At the reviewer's first eligible checkpoint, if its own tele has no `SRC_OPENED`, the item is the check (`slot_type: src`); it counts inside K.
- **Searcher.** Otherwise the first move in `ORDER` that (a) has not been injected to this rid and (b) no panel member's non-sub tele classifies to (panel-wide coverage over `board/tele/*.jsonl`). This is the only place peer telemetry is used, and only as a yes/no per move id.
- **Reader.** Otherwise the first move in `ORDER` not yet injected to this rid (no coverage test: reading moves are unobservable, so the text never claims "no panel member").
- A move a peer has covered is skipped silently; no message ever states coverage (Redesign 1 (a)).

### 2.6 Timing values (R-41, R-42, R-43, R-45)

`values.py` holds the formulas; all times in seconds from T0.

- `finish_offset = 1.35 × B_f − turn_p90[crit] − T_report_p90[crit]` (PANEL_FINISH_AT).
- `k[crit] = max(0, min(2, floor((0.35 × B_f − 2 − turn_p90[crit] − T_report_p90[crit]) / (2 × turn_p90[crit]))))` (R-42 verbatim; `crit` = the panel's critical-path role, section 3).
- `k[other role]`: on EL2, `= k[crit]` (R-42 applies to every receiver, as the source states). On SL2 and HL2 the luna role is off the critical path, and gets **Adaptation A-2**: `k[reader] = max(0, min(2, floor((finish_offset − E_p90[reader] − 2) / (2 × turn_p90[reader]))))`, where `E_p90[reader]` is the luna role's p90 end time. On EL2 this adaptation is not used, so arm A6 stays exactly the source arm.
- `guard_offset = min(1.35 × B_f − G, finish_offset)` with `G = 47 s` on EL2 (source, Redesign 1 (b)) and, **Adaptation A-3**, `G = 47 × turn_p90[crit] / 6.4` on SL2 and HL2 (the same number of critical-role turns of headroom, about 7.3).
- `hang_offset = 1.5 × B_f` (R-43; the source writes B_A1, and in-run deadlines use the frozen value, timing rule 5(b)).
- **Spike 4** (`values.py spike4`): from at least 3 collab-0 rows of that panel (`source_runs`; minimum of 3 is a design choice, Q-3): `B_f` = median over rows of the package's panel elapsed; per role, turns are measured from `reviews/<rid>.attempt<n>.json` of the final attempt (the `--output-format json` array carries a `timestamp` on its entries; entries without one are skipped). This file is kept, unlike the session transcript that `cleanup-sessions.sh` deletes. One response is split over several entries (thinking, each tool call, text), so entries are first **grouped by `message.id`**; a turn's duration = the last timestamp of a response group minus the timestamp of the latest tool-result entry before the group. The first response has no earlier tool result (the file's first entry is a `system` entry without a timestamp), so it is left out. `turn_p90` = the 90th percentile of all turns **except the first and the final response**, pooled over rows; `T_report_p90` = the 90th percentile of the final response's duration (the report turn); `E_p90` = 90th percentile of that role's end time minus T0. Brief slowdown s (R-45) is 0 for F3 (same brief in both arms), so no brief content is dropped.

### 2.7 Reviewer runner (`run-reviewer.sh`): harness fixes H1-H4 and run lifecycle

- **H1 (R-01).** The brief from `config/brief.txt` with `@@CAND@@ = SB/cand/<pkg>/candidate.md`, `@@SRC@@ = SB/cand/<pkg>/source.md` and their sha256.
- **H3, H4 (R-03).** `cd SB/<pkg>/repo` (one sandbox per package, built from the base commit, without the leak directories).
- **Command (attempt 1):** `timeout --kill-after=5 <hang_left> claude -p --model <M> --output-format json --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit [--settings '<json>'] <<<"$BRIEF"`, where `hang_left = (HANG_MS − now) / 1000` rounded down. Against `A1DIR/tools/run-reviewer.sh:48` the only differences are the R-05 allowed set: no `--no-session-persistence`; the hang guard replaces `timeout 3000`; `--settings` only with collab 1; the brief differs only by H1; the cwd is the H3/H4 sandbox.
- **Model and block check:** the same jq expressions as `A1DIR/tools/run-reviewer.sh:50-57` (observed model of top-level assistant messages; `model_ok`; `findings_block` present; `API Error` text). Plus `session_id` = `.[]|select(.type=="result")|.session_id`.
- **Retry (R-44).** If `model_ok && block_ok && !apierr` fails and at least 30 s remain before `HANG_MS`, attempt 2 runs with **no `--settings`** (logged `retry_isolated: true`; the package counts as isolated for that reviewer). No fallback model, ever. If attempt 2 also fails, the reviewer is INVALID and the package is not merged (the rule of `A1DIR/combos/SPEC.md:79`: never merge a degraded panel).
- **Hang guard (R-43).** Exit status 124 or 137 from `timeout` → `hang_kill: true`, the package raises `SLO_BREACH`, and the reviewer is INVALID unless its last attempt already produced a valid block.
- **H2 (R-02).** `h2_normalize.py attempt<n>.md norm.md h2.json`. If `h2.json.ok` is false and at least `6 + T_report_p90[role]` seconds remain before `HANG_MS`: one re-ask, `timeout <left> claude -p --resume <session_id> --model <M> --output-format stream-json --verbose --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit` (no `--settings`: nothing is delivered in a re-ask), prompt `Your findings-v1 block has these parser errors: <one line per error>. Reply with the complete corrected report, ending with the ## Findings block and the final verdict line.`; the final text is the `result` event of the stream (`jq -s '[.[]|select(.type=="result")|.result][0]'`, the `jq -s` form S3 requires). Then normalise that text. Lines still invalid are counted as `dropped_lines` in `meta.json`; `reask_s` is logged. The merge receives `norm.md`; the model's own report files are never edited.
- **Outputs.** `<rid>.md` = final normalised report, `<rid>.meta.json` = the `A1DIR` meta fields plus `session_ids` (written as soon as each id is known), `start_ms`, `end_ms`, `attempts`, `retry_s`, `retry_isolated`, `reask_s`, `dropped_lines`, `hang_kill`; `<rid>.cost.json` = `{attempts, total_wall_s, total_output_tokens_all}` summed over attempts and the re-ask. Every term uses the same measure as `A1DIR/tools/run-reviewer.sh:53`: the sum of `modelUsage[*].outputTokens` of the `result` event (for the re-ask, the `result` event of the stream).

### 2.8 Contamination safeguards (Redesign 1 (e), §4 rule 5)

| Safeguard | Mechanism | Check |
|---|---|---|
| Shared content is move ids only, plus the source.md check | Message keys limited (section 2.2); text fixed by the catalogue | Validator in the hook; post-run validator pass over `msgs/` |
| Withheld: findings, anchors, paths, counts, Tasks | No such key is accepted; Task hints go to metrics only | Same; `grep -c '"task_hint"' msgs/radar.jsonl` = 0 |
| Independent first pass | No injection before tool call 6 (searcher) or 8 (reader); snapshot written before the first injection | Hook unit tests; `seal_t <= first_delivery_t` logged (integrity log only, the same hook writes both) |
| Blind-spot spread impossible | No peer content and no coverage statement is ever sent | Leak lookup |
| Leak check | Only catalogue texts, `src_text`, `finish_text` | Hard failure → `QUARANTINED` |
| Ground truth never reaches a reviewer | Sandbox excludes `.dev/eval-workspaces`; catalogue checked against every `ground-truth.json` (`spikes/g-pins.sh`, R-07) | Post-run: no board line contains a 12-character substring of any `plan_quote`; no tele record names `.dev/reflect` or `ground-truth`; `SB/<pkg>/repo/.dev/reflect` absent |
| Reviewers read-only | `--disallowedTools`; helpers write only under `R1/runs/` | `git -C SB/<pkg>/repo status --porcelain` empty after the run; `sha256sum` of `SB/cand/<pkg>/candidate.md` unchanged |
| Arm blinding at the judge | Anonymiser (section 5.3) | No row id, `c0`/`c1`, `radar`, `evalsb-collab-r1` or reviewer id in `merged-anon.md` (`anon_leak` count in `audit.json`) |

### 2.9 Metrics, `collab.json` and alarms

`collab_summary.py` writes `collab.json` with **every** R-23 field, including `arm` (`"A6-F3"` for collab 1, `"A1"` for collab 0), `panel_finish_at` (ms) and `pairwise_task_jaccard` as its own key. Fields that F3 has no concept for are present with value `null`: `resume_fallback`, `phase2_s`, `phase2_timeout`, `p2_lines_salvaged`, `n_planned`, `n_launched`, `stop_blocks` (always 0, no Stop hook; written as 0), `card_form`, `deal_r`, `deal_c`, `echo_rate`, `over_cap` (0). Per reviewer: `msgs_sent` (0), `msgs_received` (inject count), `first_delivery_t`, `seal_t`, `hook_calls` (non-sub tele lines), `hook_error`, `hook_ms_p95`, `reask_s`, `attempts`, `retry_s`, `retry_isolated`, `k`, `finish_signal_t`, `finish_would_fire` (collab 0: a reviewer still running at `FINISH_MS`), `hang_kill`, `snapshot_missing`, `late` (0). Per slot: `slot_type`, `move`, `task_hint`, `move_executed` (observable moves: the receiver's later tele classifies to that move; else `null`). Panel: `elapsed_s` (max reviewer `end_ms` − T0, so every attempt and re-ask is included), `baseline_elapsed_s` (`B_f`), `overhead_pct`, `own_line_jaccard` (= `pairwise_task_jaccard`, since every line is own), `ledger_rows` (rows in `ledger.json`), `slo_breach`, `values_sha256`, plus F3 extras `moves_covered` (panel coverage by signature), `injections_by_move`.

`own_line_jaccard`: for each reviewer, the set of Task ids whose `## Task N:` section contains the anchor of each parsed finding (located with `findings.locate` on the candidate); mean pairwise Jaccard over the three reviewers (an empty pair counts 0).

`alarms.py` (arm level, needs both arms): CONVERGENCE fires for a collab-1 row when its `own_line_jaccard` mean exceeds the collab-0 mean + 0.15 or its `ledger_rows` fall more than 20% below the collab-0 mean (pass: at most 2 of 12 rows); SNAPSHOT fires when `snapshot_missing` exceeds 50% of receiving reviewers; the SLO budget is spent by each package with `elapsed_s > 1.35 × B_c` (B_c = the concurrent collab-0 median), budget 1 in 12; `baseline_drift = B_c / B_f` per block, outside [0.963, 1.10] → the block is reported but not used for the time verdict. A **block** is the pair (collab-0 row, collab-1 row) of one panel with the same `rep`; the owner runs the two rows of a block concurrently or back to back in an order drawn by coin (`launch.sh` does not schedule; this replaces R-28's block-randomised scheduler, which spans every arm and is outside this folder). Rows with `rep` 0 (smoke) are ignored.

### 2.10 Failure modes and runbook (Redesign 1 (h), plus harness)

| Failure | Detection (implemented in) | Action |
|---|---|---|
| Classifier mislabels a move, so a done move is re-injected | `collab_summary.py` re-classifies the full tele and compares with what was live at each checkpoint; spot-check list in `audit.json` | Fix the regex; extra cost is at most k moves |
| The gaps are always the same moves | `injections_by_move` histogram in `alarms.py` | Expected; report it |
| A reviewer ignores the injection | `move_executed: false` (observable moves only) | Logged; the gain falls toward A2 |
| An injection carries anything other than a catalogue text | Hook validator (blocks it) and post-run validator (hard failure) | `QUARANTINED`; the package is excluded |
| Hook not firing on a model | `hook_calls = 0` in `collab.json` | The package counts as isolated for that reviewer; `launch.sh` prints `ALARM hook_calls=0 <rid>` |
| Sandbox project hooks or user hooks also fire | S0 lists the `hooks` keys of `~/.claude/settings.json` and of each sandbox's `.claude/settings.json` with `jq` | Confirm none emits PostToolUse `additionalContext`; the tracked `.claude/settings.json` at the designSpec base commit `0e486ab8d` has only `PreToolUse` hooks (checked with `git show`); S0 checks the other two bases. User-level hooks fire in both arms, as they did in every earlier batch |
| A reviewer ignores "finish now" | `finish_signal_t` against `end_ms`; `hang_kill` | SLO budget (R-24); beyond `1.5 × B_f` it is `SLO_BREACH` |
| Snapshot fails | `snapshot_missing` | Nothing delivered to that rid; SNAPSHOT alarm at arm level |
| Corrupt or torn board line | Readers skip it; `hook_error` if the hook itself fails | Review continues (R-22) |
| Model misrouted or binary missing (exit 127) | `model_ok` false on both attempts | Reviewer INVALID; package not merged; no fallback (NOFALLBACK) |
| Merge refuses the round | non-zero rc of `superclaude review merge` | Package INVALID in the row. `A1DIR/combos/SPEC.md` step 3 re-runs the reviewer once, but a lone re-run outside the timed panel would corrupt `elapsed_s`, so here the owner re-runs the whole package as a new row (Adaptation A-6) |
| Judge fails or API error | `judge-one.sh` prints `FAIL`, or `judge.json` result contains `API Error` | One re-run of the judge (it skips if `score.json` exists); still failing → `judge_failed` in the row |

## 3. The three panels

The source designs F3 for ember + 2x luna only. The design keeps two roles, **searcher** (one reviewer: gets the observable search moves M1, M2, M7, M4, booked to C) and **reader** (two lunas: get the reading moves M3, M5, M6, M9, M8, M10 as timed static prompts, booked to P). Every reviewer may get the source.md check. The catalogue's "style" column lists ember, haiku and sonnet as search-style models, so the panel's non-luna model plays the searcher (Adaptation A-1).

### 3.1 Roles per panel

| Panel (row prefix) | Searcher (rid, model) | Readers (rids, model) | Critical-path role (sets B) | Source baseline |
|---|---|---|---|---|
| `el2` ember + 2x luna | `t2b-1` `muse-ember-1.0` | `t4-1`, `t3-1` `gpt-6-luna` | reader (slowest luna) | EL2, the source's arm A6 exactly |
| `sl2` sonnet + 2x luna | `t1b-1` `claude-sonnet-5-5` | `t4-1`, `t3-1` `gpt-6-luna` | searcher (sonnet) | SL2 (source uses it for F6 only) |
| `hl2` haiku + 2x luna | `t2-1` `claude-haiku-5-5` | `t4-1`, `t3-1` `gpt-6-luna` | searcher (haiku) | HL2 (named in §2.0, no design uses it) |

Reviewer ids are labels from the existing resolutions (`t2b-1` for ember and `t1b-1` for sonnet as in batches 8-11, `t2-1` for haiku as in batch 9); the merge resolution is built as in `A1DIR/analysis/merge-b11.sh:17-25`. Checkpoints: searcher after tool calls 6 and 10, readers after 8 and 12, on every panel (the source's ember and luna values; A-5).

### 3.2 Planning timing per panel (replaced by Spike 4 values)

Planning inputs: B from `SRCREQ` §2.0; turn time = median wall / median turns (ember 3.2 s, luna 6.4 s, sonnet 14 s, haiku 23 s); T_report_p90 = one turn of the critical role (the source's value for luna; for sonnet and haiku the source has none, so one turn is assumed, A-8). Luna's own end for A-2 uses its median wall, 102 s.

| Value | el2 | sl2 | hl2 |
|---|---|---|---|
| B (planning) | 116 s | 273.7 s | 238 s |
| crit turn_p90 / T_report_p90 | 6.4 / 6.4 s | 14 / 14 s | 23 / 23 s |
| PANEL_FINISH_AT − T0 | 156.6 − 12.8 = **143.8 s** | 369.5 − 28 = **341.5 s** | 321.3 − 46 = **275.3 s** |
| k, critical role (R-42) | floor(25.8 / 12.8) = **2**; k = 2 needs T_report_p90 ≤ 6.6 s, k ≥ 1 needs ≤ 19.4 s | floor(65.8 / 28) = **2**; k = 2 needs T_report_p90 ≤ 23.8 s, k ≥ 1 needs ≤ 51.8 s | floor(35.3 / 46) = **0**; k ≥ 1 needs T_report_p90 ≤ 12.3 s |
| k, searcher | = k crit = 2 (ember, off path, source rule) | = k crit = 2 | = k crit = **0** |
| k, readers | = k crit = 2 | A-2: floor((341.5 − 102 − 2) / 12.8) → 2 | A-2: floor((275.3 − 102 − 2) / 12.8) → 2 |
| Injection guard (no injection after) | 156.6 − 47 = **109.6 s** (source: 110 s) | A-3: 369.5 − 102.8 = **266.7 s** | A-3: 321.3 − 168.9 = **152.4 s** |
| Hang guard 1.5 B | 174 s | 410.6 s | 357 s |
| Planned end, k = 1 | 116 + 2 + 12.8 = 130.8 s (+12.8%) | 273.7 + 2 + 28 = 303.7 s (+11.0%) | 238 + 2 = 240 s (+0.8%): the critical haiku gets nothing |
| Planned end, k = 2 | 143.6 s (+23.8%) | 331.7 s (+21.2%) | 240 s; the lunas end near 102 + 2 + 25.6 ≈ 130 s, off the path |
| Finish-signal bound 1.35 B | 156.6 s | 369.5 s | 321.3 s |

### 3.3 What each panel measures

- **el2**: the source design. C comes from ember's search-move rows (I4 via M4, I5 via M7, B8 and B6 via M2; I7 via M1 on control); P from the luna rows. The (f) gain block of the source applies as written.
- **sl2**: sonnet already opens unnamed tests in 35% of runs and touches 3.1 unnamed files per run (`SRCREQ` §1, T1 table), so panel-wide coverage will mark more search moves as done and the searcher will get fewer injections than ember (more `skip no_gap` events). Every searcher injection sits on the critical path (2 sonnet turns, about 28 s each); the R-42 count keeps the planned end under PANEL_FINISH_AT. No source gain block exists for this panel; report measured values only.
- **hl2**: at planning values haiku gets **k = 0**, so the panel receives only the lunas' timed reading prompts and the lunas' source.md checks: its C share is 0 by construction and the arm measures P only. If Spike 4 gives haiku T_report_p90 ≤ 12.3 s, haiku gets k = 1. Whether to accept this or relax the time rule for haiku is the owner's decision (Q-1); the design defaults to the source time rule.
- On every panel the luna reading-move injections are `slot_type: static` and booked to P (R-33); the collab-1 versus collab-0 comparison is reported as "telemetry-timed kit against no kit" because this design has no A2 (static kit) arm of its own (section 7, K-2).

## 4. Kill switch: PANEL_COLLAB=0

`PANEL_COLLAB` is read once, by `launch.sh`, and must be `0` or `1` (default `1`; any other value: refuse, exit 2). It is passed to `run-reviewer.sh` as a positional argument; no hook or helper reads it.

| Item | `PANEL_COLLAB=1` (arm A6 on el2) | `PANEL_COLLAB=0` (arm A1, the baseline) |
|---|---|---|
| `--settings` / radar hook | yes, per reviewer | **none**: no `--settings` argument at all |
| Board | `tele/`, `msgs/`, `metrics/`, `snap/`, `state/` | only `board/` with a `metrics/` line per reviewer for `finish_would_fire` (written by `collab_summary.py`, not a hook) |
| Brief | `config/brief.txt` (H1) | the same file, byte-identical |
| Sandbox | `SB/<pkg>/repo` (H3, H4) | the same sandbox |
| H2 normaliser and one re-ask | yes | yes |
| Retry loop, attempt 2 | isolated (no `--settings`) | the same |
| Hang guard `T0 + 1.5 B_f` | yes | yes (2.0 × planning B when no values file exists yet, see below) |
| Session persistence | on (no `--no-session-persistence`) | on |
| NOFALLBACK, no ladder | yes | yes |
| Merge, anonymiser, judge, results | same scripts | same scripts; collab counters are 0 or null, coverage counters come from the post-hoc classifier over the JSON transcripts |

**R-05 check.** `run-reviewer.sh --print-cmd <row> <pkg> <rid> <model> 0 <T0>` prints the attempt-1 argv. Its token list, compared with `A1DIR/tools/run-reviewer.sh:48`, may differ only in: `timeout 3000` → `timeout --kill-after=5 <hang_left>`; `--no-session-persistence` removed; the cwd `SB/<pkg>/repo` instead of `/tmp/evalsb/repo`; the brief (H1 sentence and the `SB/cand/` paths). With collab 1 the only further difference is `--settings '<json>'`. A test (section 6, T-10) enforces this list.

**Values for collab 0.** Spike 4 itself runs collab-0 rows before any values file exists, so with `PANEL_COLLAB=0` and no values file `launch.sh` uses the planning B of `config/panels.json` for `finish_would_fire` and a hang guard of **2.0 × planning B** (232 s, 547.4 s, 476 s), and records `"values":"planning"` in `run.json`. The wider guard keeps Spike 4 from truncating slow rows (historical SL2 maxima 416 s and 440 s exceed 1.5 × 273.7 = 410.6 s) and so from biasing B_f low; once values exist, collab-0 rows use 1.5 × B_f like every arm (R-43). `PANEL_COLLAB=1` without a values file is refused (exit 2): k cannot be computed.

## 5. Launch script and results row

### 5.1 Interface

```bash
cd /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
PANEL_COLLAB=1 bash .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh el2 3
PANEL_COLLAB=0 bash .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh hl2 1 TASK-WF-designSpec-20261107-075614   # smoke: one package
```

Arguments: `<panel>` in `el2|sl2|hl2`, `<rep>` a non-negative integer (0 is reserved for smoke rows), optional package list (default all three, in the order DS, AL, DE). Exit 0 when the row is written with every package `ok`; 1 when the row is written but some package is `invalid`, `quarantined` or `judge_failed`; 2 on a preflight refusal (nothing run). Log: `R1/runs/<row>/launch.log` (one line per step, `START`/`END`/`FAIL` with UTC time). Run it with `nohup … &` or the Bash tool's background mode; it never prompts.

### 5.2 Steps

1. **Preflight** (refuse with exit 2 on any failure): `PANEL_COLLAB` in {0,1}; `NOFALLBACK` unset or `1`, then `export NOFALLBACK=1`; `claude`, `jq`, `flock`, `uv`, `superclaude` on `PATH`; `sha256sum` of `config/catalogue.json`, `config/brief.txt` and `A1DIR/tools/tmp-scripts/judge-one.sh` equal the pins in `manifest.json` (judge pin at design time: `a01bd70d370d73cb32b55a7368aa28e2c12d93403237211c3a71f339ae82cfcc`); `manifest.json` has a base sha for each requested package; for collab 1, a values file per requested package whose `.sha256` matches; `R1/runs/<row>/` does not already hold a finished row (`results/<row>.json` exists → refuse; a partial row is resumed package by package: a package with `score.json` reached is skipped).
2. Per package, **sequentially** (3 reviewer sessions at a time per launch; section 7, K-8): `sandbox.sh <pkg>`; `radar-index.sh <pkg>`; compute T0 and deadlines; per reviewer compute `ORDER`, `K`, checkpoints and (collab 1) `settings/<rid>.json` via `settings-gen.sh`; start the three `run-reviewer.sh` processes; `wait`.
3. `collab_summary.py pre <row> <pkg>`; exit 3 → package `quarantined`, skip merge and judge.
4. If any reviewer is INVALID → package `invalid`, skip merge and judge.
5. **Merge** (R-04, same arguments as `A1DIR/analysis/merge-b11.sh:34`): build `resolution.json` from `A1DIR/<pkg>/resolution-live7.json` with the panel's three reviewers (as `merge-b11.sh:17-25`), then `superclaude review merge --ledger R1/runs/<row>/<pkg>/ledger.json --doc A1DIR/<pkg>/candidate.md --round 1 --report <rid>=R1/runs/<row>/<pkg>/reviews/<rid>.md …(3) --resolution R1/runs/<row>/<pkg>/resolution.json --out R1/runs/<row>/<pkg>/merged-1.md > merge-stdout.txt 2>&1`. **Every path is absolute**: the merged report prints `report <path>` per reviewer (`src/superclaude/cli/review/ledger.py:423`), and only an absolute `R1` path is rewritten to `<EVAL>` and then redacted by the anonymiser; a relative path would carry the row id (with `c0`/`c1`) to the judge. Non-zero rc → package `invalid`.
6. **Anonymise:** `anon.sh <row> <pkg>` (section 5.3), then `collab_summary.py post <row> <pkg>`. If `anon_leak` > 0 (a row id, `c0`/`c1`, `radar`, `evalsb-collab-r1` or a reviewer id survived), the package is `quarantined` and not judged: arm blinding would be broken.
7. **Judge** with the unchanged script: `bash A1DIR/tools/tmp-scripts/judge-one.sh "../../../../20261113-collab/r1-move-radar/scoring/<opaque>" "<pkg>" "<L>"` (section 5.3). On `FAIL` or `API Error` in `judge.json`: delete nothing, run it once more (it skips when `score.json` exists); still no `score.json` → `judge_failed`.
8. After all packages: `results.py <row>`; `cleanup-sessions.sh <row>`; print the row JSON path.

### 5.3 Anonymiser and the unchanged judge

`anon.sh` copies `merged-1.md` and applies, in order: replace `R1` (absolute) and `A1DIR` (absolute) by `<EVAL>`; replace `SB` (`/tmp/evalsb-collab-r1`) by `/tmp/evalsb`; replace each reviewer id matching `\bt[0-9a-z]+-[0-9]+\b` by `R1`, `R2`, `R3` in sorted order; the two `sed` rules of `A1DIR/tools/tmp-scripts/anon-b11.sh:24-25` (candidate line and report paths); then deletes any remaining `"origin":"…"` key (defensive; F3 never writes one). The label `<L>` is drawn from Q..V and the directory token `<opaque>` is 12 random hex characters, both stored only in `runs/<row>/<pkg>/label-key.json`. Collab-0 and collab-1 rows go through the same path pattern, so the judge cannot tell the arms apart.

`judge-one.sh` hard-codes `EVAL=A1DIR` and writes to `D="$EVAL/arms/scoring/combos/$C/$P/$L"` (`A1DIR/tools/tmp-scripts/judge-one.sh:4-6`). Passing `C = ../../../../20261113-collab/r1-move-radar/scoring/<opaque>` makes `D` resolve to `R1/scoring/<opaque>/<pkg>/<L>` (checked with `realpath -m`; the intermediate directory `A1DIR/arms/scoring/combos` exists). The script then reads ground truth and the candidate from `A1DIR` (read only), and the judge writes `judge.json`, `judge.err` and `score.json` inside `R1`. The script stays byte-identical (sha256 pinned), and nothing is created under `A1DIR`. The `combo` field of `score.json` will hold that relative path; `results.py` ignores it and keys rows by the label key.

### 5.4 Results row (`results.py`)

Per package, from `score.json` (judge) and `A1DIR/<pkg>/ground-truth.json` (only `id` and `blocking_in_implement`, read by the harness, never by a reviewer), with the same definitions as `A1DIR/analysis/final-table.py:31-37`: `any` = `|gt_covered_any|`; `jb` = `|gt_covered_blocking|`; `rb` = judge-blocking items whose `blocking_in_implement` is true; `wb` = `wrong_blockers`. Tokens = sum of the three `cost.json` `total_output_tokens_all`. Elapsed = `collab.json` `elapsed_s` (panel wall from T0 to the last reviewer end, including every attempt and re-ask; this is stricter than `final-table.py`'s max of per-reviewer walls, which ignores start skew).

`results/<row>.json` (schema `r1-results/1`):

```json
{
 "schema": "r1-results/1", "design": "r1-move-radar", "row": "el2-c1-r3",
 "panel": "el2", "models": {"t2b-1": "muse-ember-1.0", "t4-1": "gpt-6-luna", "t3-1": "gpt-6-luna"},
 "collab": 1, "rep": 3, "started_utc": "…", "values": {"<pkg>": "<sha256>|planning"},
 "status": "complete|incomplete",
 "found_14": 3, "real_blocking_8": 1, "judge_blocking": 2, "wrong_blockers": 1,
 "control_found_2": 0, "control_wrong_blockers": 0,
 "output_tokens": 61234,
 "elapsed_s": {"TASK-WF-designSpec-20261107-075614": 131.2, "TASK-WF-makeTheAliasOnly-20261105-051649": 140.9, "TASK-WF-design-20261108-041415": 128.0},
 "packages": {"<pkg>": {"status": "ok|invalid|quarantined|judge_failed", "label": "R",
   "gt_covered_any": ["GT2"], "real_blocking": ["GT2"], "judge_blocking": ["GT2"], "wrong_blockers": 0,
   "ledger_rows": 9, "output_tokens": 20411, "elapsed_s": 131.2, "overhead_pct": 13.1, "slo_breach": false,
   "k": {"searcher": 2, "reader": 2}, "dropped_lines": 0, "reask": 1, "retry_isolated": 0, "hang_kill": 0}},
 "collab_counters": {
   "injections": 6, "injections_by_move": {"M2": 1, "M7": 1, "M3": 1, "M8": 1}, "src_checks": 2,
   "search_injections": 2, "static_injections": 2, "observable_moves_executed": 1,
   "skips_no_gap": 1, "skips_guard": 0, "finish_signals": 0, "finish_would_fire": 0,
   "hook_calls": 143, "hook_errors": 0, "hook_ms_p95": 41, "snapshot_missing": 0, "late": 0,
   "leak_violations": 0, "moves_covered_panel": {"M1": 0, "M2": 2, "M4": 0, "M7": 1, "SRC_OPENED": 3, "UNNAMED_TEST": 0},
   "own_line_jaccard": {"<pkg>": 0.31}}
}
```

Rules: `found_14` = DS `any` + AL `any`; `real_blocking_8` = DS `rb` + AL `rb`; `judge_blocking` and `wrong_blockers` = DS + AL (the defect-rich packages, as in `final-table.py`); `control_found_2` = DE `any`; `control_wrong_blockers` = DE `wb`; `output_tokens` = sum over the three packages. A package that is not `ok` contributes `null` and the row `status` is `incomplete`; sums are then `null`, never a partial number. Counters are summed over packages except `own_line_jaccard`. With collab 0 the injection counters are 0, `moves_covered_panel` comes from the post-hoc classifier, and `finish_would_fire` is filled. `results.jsonl` gets the same object on one line.

## 6. Test plan

All tests: `uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests -q` from `REPO`. No test calls the gateway: tests that need `claude` put `tests/fixtures/bin/claude` (a bash stub that replays a canned JSON file chosen by an argument file, or sleeps, or exits 127) first on `PATH` for the subprocess only. Tests write only under pytest's `tmp_path`; each script under test takes its roots from arguments or from a `tests`-only override argument, never from the real `R1/runs`.

### 6.1 Unit tests (one module per component)

| Id | Module | Checks (each is an assert) |
|---|---|---|
| T-1 | `test_catalogue.py` | `catalogue.json` has M1-M10, each text equal to the `SRCREQ` §2.0 column (read from `SRCREQ` lines 184-193); every rendered injection ≤ 300 chars; `observable` = M1, M2, M4, M7; sha256 equals `catalogue.sha256`. R-07 check on fixture ground truth: a fixture `plan_quote` copied into a move text is detected (12-char window), the real catalogue gives 0 hits against the three real `ground-truth.json` files (this test reads ground truth; it is the harness, not a reviewer). |
| T-2 | `test_index.py` | On the fixture candidate: Tasks T1-T3 found from `## Task N:`; a path inside Task 2's section maps to `["T2"]`; both backticked grep patterns extracted exactly; `root_files` lists a fixture repo's root files only. |
| T-3 | `test_classify.py` | One positive fixture record per signature (M1 Bash `grep -rn merge_guard tests/`; M1 Grep tool `path=tests`; M2 `grep -l x src/`; M2 `ls docs \| wc -l`; M2 Grep `output_mode=count`; M4 exact criterion pattern, quoted and unquoted; M7 `grep -rn 43 .`; M7 Grep with no path; M7 `grep 43 CHANGELOG.md`; SRC_OPENED Read and `sed -n 1,80p …/source.md`; UNNAMED_TEST Read `tests/x/test_y.py` not in the index). Negatives: recursive grep over `src/` is not M1; a grep over `tests/` with an unrelated pattern is not M1; Read of a test named in the candidate is not UNNAMED_TEST; a near-miss pattern is not M4; `sub:true` records are never counted. No output ever contains M3, M5, M6, M8, M9, M10 (property check over all fixtures). |
| T-4 | `test_order.py` | Rotation offsets: `t4-1` → 0, `t3-1` → 4, `t2b-1` → 1, `t1b-1` → 2, `t2-1` → 0; the two lunas' first moves differ (M3 vs M8) and their second moves differ (M5 vs M10). |
| T-5 | `test_hook_schedule.py` | Driving `radar-hook.sh` with a sequence of fixture stdin records and a clock file: searcher with K=2 injects at calls 6 and 10 only; with K=1 at call 6 only; reader at 8 and 12; at most K inject events; the source.md check is delivered at the first checkpoint when no SRC_OPENED exists and not when one exists; a move covered by a peer's tele (M2 in another rid's file) is skipped and the next uncovered one injected; when every searcher move is covered the event is `skip no_gap` and nothing is printed; no injection when the clock is ≥ GUARD; output is the exact `hookSpecificOutput` JSON shape with `hookEventName` `PostToolUse`; the text equals the catalogue text (+ suffix only for the searcher's observable moves; never the suffix on a reader). |
| T-6 | `test_hook_finish.py` | With the clock ≥ FINISH: the first call after it prints `finish_text` and logs `finish`; later calls print nothing; no inject event after FINISH (R-41). |
| T-7 | `test_hook_seal.py` | First delivery writes `snap/<rid>.jsonl` byte-equal to the fixture transcript and its sha256, and the `seal` event precedes the `inject` event; with an unreadable `transcript_path` → `snapshot_missing`, no output at that checkpoint nor at the next (R-10, R-19 pattern). |
| T-8 | `test_hook_errors.py` | A corrupt line in a peer's tele file: the hook still works; an unwritable `msgs/` directory: exit 0, empty stdout, `hook_error` logged; stdin that is not JSON: exit 0, empty stdout (R-22). |
| T-9 | `test_validate.py` | Accepted: a radar move line; a radar source-check line (no `move`). Rejected with the right reason: 601-byte line (`too_long`); each of `claim`, `verdict`, `blocking`, `severity`, `category`, `note`, `anchor`, `items`, `extra` keys (`bad_key`); `from:"t4-1"` (`bad_field`); `move:"M11"` (`bad_move`); text not equal to the catalogue text (`leak`); the observable suffix sent with a reading move (`leak`). |
| T-10 | `test_settings_and_cmd.py` | `settings-gen.sh` output parses as JSON, has one PostToolUse handler with `timeout` 5, contains the absolute board path, rid, T0, FINISH and no `$`; `run-reviewer.sh --print-cmd` with collab 0 differs from the `A1DIR/tools/run-reviewer.sh:48` token list only by the R-05 allowed set (section 4) and contains no `--settings`; with collab 1 the only extra tokens are `--settings` and its JSON. Gate order: with a fixture `gate0.json` lacking S3, `launch.sh` collab 1 accepts `rep` 0 up to the first reviewer start (stubbed) and refuses `rep` 1 with exit 2; without S0 it refuses both. |
| T-11 | `test_h2.py` | A 250-char anchor is truncated to 200, still found by `findings.locate` in the fixture candidate, and the line is kept; a 400-char claim → 300; a bad severity line makes `ok` false with that error; after a stubbed re-ask whose answer is still bad, `dropped_lines` = 1 and `reask_s` is recorded; a stubbed good re-ask gives `dropped_lines` = 0 (R-02). |
| T-12 | `test_values.py` | Turn extraction on a fixture attempt file with a response split over three entries sharing one `message.id`, two parallel tool calls, and a long final report response: the split response counts as one turn, the parallel calls add no extra turn, the first response (preceded only by an untimed `system` entry) adds no turn, and the final response feeds only `T_report_p90`. R-42 cases: B 116, 6.4/6.4 → 2; T_report 11.0 → 1; B 100 → 1 only when T_report ≤ 13.8; SL2 B 273.7 turn 14 → k ≥ 1 only when T_report ≤ 51.8; HL2 B 238 turn 23 / 23 → 0, and → 1 at T_report 12.3. finish_offset 143.8 on EL2; guard 109.6 (EL2), 266.7 (SL2), 152.4 (HL2) within 0.1 s; A-2 reader k on HL2 planning → 2; EL2 never uses A-2 (reader k = searcher k = crit k). `spike4` refuses 2 rows and refuses to overwrite an existing values file. |
| T-13 | `test_runner_retry.py` | Stub returns no findings block on attempt 1: attempt 2 runs without `--settings`, `retry_isolated` true, `attempts` 2, wall summed in `cost.json`; stub misroutes (observed model differs) twice: reviewer INVALID, no third attempt, no other model invoked (R-44, NOFALLBACK). |
| T-14 | `test_anon.py` | Fixture merged report with reviewer ids, `R1`/`A1DIR`/`SB` paths and a stray `"origin":"own"`: output has no `t*-N` id, no `/tmp/evalsb-collab-r1`, no `r1-move-radar` outside `<EVAL>`, no `origin`, no row id; label in Q..V; key written to the run dir only. |
| T-15 | `test_judge_path.py` | Runs the real, unchanged `A1DIR/tools/tmp-scripts/judge-one.sh` with a stub `claude` (on `PATH`) that writes `score.json` to the path named in its brief, and `C = os.path.relpath(<tmp_path>/scoring/<opaque>, A1DIR/arms/scoring/combos)` (the same mechanism as production, aimed at `tmp_path`). Asserts: `score.json` and `judge.json` exist under `tmp_path`; a recursive listing of `A1DIR/arms/scoring/combos` before and after is identical; `sha256sum judge-one.sh` equals the pin. |
| T-16 | `test_results.py` | Fixture `score.json` for three packages plus fake ground truth: `found_14`, `real_blocking_8` (only `blocking_in_implement` items), `judge_blocking`, `wrong_blockers`, `control_found_2`, `control_wrong_blockers` match hand-computed values; one package `invalid` → sums `null`, status `incomplete`; a duplicate row id is refused. |
| T-17 | `test_collab_summary.py` | `pre` works without `ledger.json` and `merged-anon.md`; `post` adds `ledger_rows` and `anon_leak`; every R-23 key present after `post` (null where F3 has none); `own_line_jaccard` from fixture blocks equals the hand value; `move_executed` true when a later tele record classifies to the injected move, false otherwise, null for reading moves; `elapsed_s` = max end − T0; audit flags a fixture board line containing a 12-char ground-truth substring; audit flags a dirty sandbox (`git status` non-empty) and a changed candidate sha. |
| T-18 | `test_alarms.py` | CONVERGENCE fires on a fixture row whose Jaccard exceeds the collab-0 mean + 0.15, and on ledger rows down more than 20%; SLO budget counts packages above 1.35 B_c; drift outside [0.963, 1.10] marks the block unused. |
| T-19 | `test_cleanup.py` | Two fake rows share one fake projects directory: cleanup of row A removes only A's recorded session files; B's file remains (R-46). |

### 6.2 Fault-injection tests (one per failure mode)

| Id | Failure mode | Injection | Pass condition |
|---|---|---|---|
| F-1 | Classifier mislabel | Index with a wrong `keys[]` entry so a real M1 call is missed live | `audit.json` spot-check lists the mismatch (re-classification differs from the live decision) |
| F-2 | Same gaps every time | 5 fixture rows with identical injections | `alarms.py` histogram reports it; no failure raised |
| F-3 | Reviewer ignores the injection | Tele with no M2 signature after an M2 injection | `move_executed: false`, counted in `observable_moves_executed` = 0 |
| F-4 | Leak | Three fixture boards: a `msgs/radar.jsonl` line with an `anchor` key; an `inject` metrics event whose `text` differs from the catalogue text of its line's move; a board line with no matching `inject` event | Each case: `collab_summary.py pre` exits 3 and writes `QUARANTINED`; `launch.sh` marks the package `quarantined` and skips merge and judge |
| F-5 | Hook not firing | Stub run with no tele written | `hook_calls` 0, `ALARM hook_calls=0` line in `launch.log`, package treated as isolated for that rid |
| F-6 | Snapshot failure | Unreadable transcript path (T-7) | `snapshot_missing` 1, zero deliveries to that rid |
| F-7 | Corrupt board line | Garbage line in `tele/` (T-8) | Hook output unaffected, review continues |
| F-8 | Reviewer ignores "finish now" / hangs | Stub that sleeps past the hang deadline (deadline set to 3 s in the test) | Process killed within 5 s of the deadline (`timeout --kill-after=5`), `hang_kill` true, `slo_breach` true (R-43); same result with collab 0 |
| F-9 | Failed block on attempt 1 | T-13 | Attempt 2 isolated, elapsed summed (R-44) |
| F-10 | Model misroute / binary missing | Stub exits 127 twice | Reviewer INVALID; package `invalid`; `launch.sh` exit 1; no fallback model in any argv |
| F-11 | Merge refuses | Reports with no valid block (stub) | Package `invalid`, merge stdout kept |
| F-12 | Judge failure | Stub judge exits non-zero once, then succeeds | Exactly two judge calls; `score.json` present; a stub that always fails → `judge_failed` |
| F-13 | Hook error must not kill a review | Hook script made to `exit 1` mid-run in a stub session | Reviewer completes; `hook_error` logged; (for the real CLI this is checked in S0) |
| F-14 | Environment cleared | Run the hook with `env -i PATH=/usr/bin:/bin` | Same decisions and outputs as with the full environment (R-21) |

### 6.3 Gate 0 spikes this design depends on (R-27)

Each spike writes its record under `R1/spikes/`; a spike passes only on the stated condition, decided mechanically by `spikes/gate0-check.sh` into `spikes/gate0.json`. Gate order, so no spike depends on itself: collab-0 rows need G-BASE and G-PINS; the collab-1 smoke row (`rep` 0) needs G-BASE, G-PINS, S0, S2 and Spike 4; every collab-1 row with `rep` ≥ 1 needs all of those **and** S3. Spike 5 (re-scoring historical runs to measure the H2 part of H) is not run here: it measures the harness share shared by all designs, and F3 does not depend on it.

| Spike | What it runs | Pass condition |
|---|---|---|
| G-BASE | `spikes/g-base.sh`: per package, the `T1: start sha=` value of `REPO/.dev/tasks/done/<pkg>/progress.md` (designSpec `69f360d58d89…`, alias `fdb08e60c8c3…`, design `c1a436aed894…`). None of the three exists in this clone (checked with `git cat-file -e`). The script tries `git fetch origin <sha>` (the fork; read-only); if that fails it uses the first parent of the squash commit that added the package and its implementation: designSpec `0e486ab8d` (parent of `0b8a5801d`), alias `38eb3c58a` (parent of `4eb75698d`), design `5fa680778` (parent of `54e21668f`); `method` is recorded. | `manifest.json` has 3 base SHAs; each sandbox lacks `.dev/reflect`; the package's own plan folder is absent from its sandbox; R-03's repaired-code check: in the designSpec sandbox, `src/superclaude/skills/sc-pr-submit-protocol/refs/merge-guard.md` is absent or differs from its version at `0b8a5801d` (the squash commit adds 196 lines to it), and the same holds for every file that package's squash commit changed under `src/` |
| G-PINS | `spikes/g-pins.sh` | Pins written; catalogue has 0 ground-truth hits (T-1 logic) |
| S0 | One 3-call probe session per model (ember, luna, sonnet, haiku: Adaptation A-7, the source names only ember and luna) in `SB/<DS>/repo` with a settings JSON whose hook logs stdin and returns an `additionalContext`; plus a hook that sleeps past its `timeout` | For every model: hook stdin has `tool_name`, `tool_input`, `transcript_path`; a probe that makes the model call one subagent shows whether subagent tool calls reach the hook and carry `agent_id` (if they reach it without `agent_id`, the design cannot tell them apart and S0 fails until the `sub` rule is replaced); the snapshot is written and hashed; a hook that exceeds its timeout does not kill the session; the hooks keys of the user and sandbox settings are listed and none is a PostToolUse `additionalContext` producer |
| S2 | Per model, a short `claude -p` (persistence on) then `--resume <session_id>` with `--output-format stream-json --verbose` | Resume answers in the same session for all four models; the `result` event is parsed by the `jq -s` filter; record the resume start time (planning 6 s) |
| REQ-S3 | Per model, 3 sessions with the real A1 brief on DS; the hook injects "run `ls /tmp/panel-probe`" at call 3, and `finish_text` at call 8 | Recorded, not gated: act rate (next tool call runs the probe) and finish act rate (at most 1 further tool call after the finish text) per model, in `spikes/reqs3.json`; these replace the planning act rates 0.5-0.8 of Redesign 1 (f) before any result is compared with a gain range (R-47) |
| S3 | The smoke test below | As in 6.4 |
| Spike 4 | `spikes/spike4.sh <panel>`: 3 collab-0 rows (`launch.sh` with `PANEL_COLLAB=0`), then `values.py spike4` | One values file per package with its sha256, written before the first collab-1 row (S0 records `hook_ms_p95`; the R-42 formula keeps its fixed 2 s hook allowance, see K-5) |

### 6.4 One-package smoke test (S3)

`PANEL_COLLAB=1 bash tools/launch.sh el2 0 TASK-WF-designSpec-20261107-075614` (rep 0 is reserved for smoke rows and excluded by `alarms.py`), then the same with `PANEL_COLLAB=0`. Pass when all hold:

1. Three reviewers with `model_ok: true` and observed model equal to the panel model.
2. `dropped_lines` is 0 for every reviewer, or the re-ask ran and the remaining drops are recorded.
3. Collab 1: `hook_calls` > 0 for all three; injections per rid ≤ k; no injection after GUARD; `seal_t` before `first_delivery_t`; leak lookup clean; collab 0: no `settings/` directory, no `msgs/`, no `--settings` in any argv in `meta.json`.
4. `superclaude review merge` rc 0; the merged report lists the three reviewer ids.
5. `merged-anon.md` passes the T-14 assertions; the judge wrote a parseable `score.json` under `R1/scoring/`; no new entry under `A1DIR`.
6. `results/el2-c1-r0.json` validates against the section 5.4 shape; `status` `incomplete` is expected for a one-package smoke and is the only accepted reason for null sums.
7. `git -C SB/<DS>/repo status --porcelain` empty; candidate sha256 unchanged; `cleanup-sessions.sh` removed exactly the recorded session files.

### 6.5 Acceptance criteria (pass/fail)

| Id | Criterion | Pass when |
|---|---|---|
| AC-1 | Unit and fault-injection tests | `uv run pytest …/r1-move-radar/tests -q` exits 0 with T-1..T-19 and F-1..F-14 collected and passed (no skips) |
| AC-2 | Gate 0 | `spikes/gate0.json` lists G-BASE, G-PINS, S0, S2 and Spike 4 as `pass` before the smoke row, S3 as `pass` after it, and REQ-S3 as `recorded`; `launch.sh` refuses a collab-1 row with `rep` ≥ 1 while S3 is not `pass` (tested in T-10 with a fixture `gate0.json`) |
| AC-3 | Smoke | All 7 conditions of 6.4 hold for collab 1 and collab 0 |
| AC-4 | Kill switch | T-10 passes and the collab-0 smoke row has 0 injections, no `settings/` and no `msgs/` |
| AC-5 | Isolation | After AC-3, `git status --porcelain` in `REPO` shows changes only under `R1/`; `find A1DIR -newer R1/manifest.json` prints nothing; no file outside `R1/` and `SB/` was written except session files removed by cleanup |
| AC-6 | Each panel runs | One full row (three packages, `status` `complete`) exists for each of `el2`, `sl2`, `hl2` with collab 1 and with collab 0 |
| AC-7 | Read-only and ground-truth safety | Every `audit.json` in AC-3 and AC-6 rows: sandbox clean, candidate sha unchanged, 0 ground-truth substrings in the board, 0 tele records naming `.dev/reflect` or `ground-truth` |
| AC-8 | Models | Every `meta.json` in AC-3 and AC-6 rows has `model_ok: true`, the expected model, and no `fallback.log` exists anywhere under `R1/runs/` |

## 7. Risks and open questions

### 7.1 Adaptations of the source (where the source assumes something this setup lacks)

| Id | Source says | This design does | Why |
|---|---|---|---|
| A-1 | F3 runs on ember + 2x luna; ember is the searcher | On sl2 and hl2, sonnet or haiku plays the searcher role | The owner tests three panels; the catalogue lists sonnet and haiku as search-style models |
| A-2 | One k per package from the critical-path reviewer, for every receiver (R-42) | On sl2 and hl2 the luna role, which is off the critical path, gets its own k from its p90 end; el2 keeps R-42 verbatim | On hl2 R-42 gives k = 0 to everyone at planning values, which would make the whole panel isolated although the lunas finish about 140 s before PANEL_FINISH_AT |
| A-3 | No injection after T0 + 1.35 B − 47 s (EL2) | On sl2 and hl2, 47 s is scaled by the critical role's turn time (102.8 s, 168.9 s) | 47 s is about 7 luna turns of headroom; the source gives no value for other panels. UNVERIFIED derivation |
| A-4 | The source.md check is an injection; `move` takes only M1-M10 | The check's board line has no `move` key | Keeps R-07 intact without inventing a move id |
| A-5 | Checkpoints: ember 6 and 10, luna 8 and 12 | Searcher 6 and 10, readers 8 and 12, on every panel | No source value for sonnet or haiku; keeps the independent-first-pass rule (no injection before call 6) |
| A-6 | Merge refused → re-run the reviewer once (`A1DIR/combos/SPEC.md` step 3) | The package is `invalid`; the owner re-runs it as a new row | A lone re-run breaks the panel's elapsed time |
| A-7 | S0, S2 and REQ-S3 on ember and luna | Also on sonnet and haiku | They are reviewers on sl2 and hl2 |
| A-8 | T_report_p90 planning value only for luna | One turn of sonnet (14 s) or haiku (23 s) as planning | Spike 4 replaces it |

Design choices not fixed by the source: the H2 re-ask runs without hooks; attempt 2 runs only with at least 30 s left before the hang deadline; packages run one after another; the hash order is a rotation; the `src_text` and `finish_text` wordings; Spike 4 needs at least 3 rows, and its rows use a 2.0 × planning B hang guard; a block is one collab-0 and one collab-1 row of the same panel and `rep`, ordered by the owner (no scheduler); Spike 5 is not run here.

### 7.2 Risks

| Id | Risk | Consequence | Mitigation in this design |
|---|---|---|---|
| K-1 | PostToolUse hooks with `additionalContext` are unverified on the gateway models | No injection is delivered; the arm equals the baseline | S0 gates every collab-1 run; `hook_calls = 0` alarm |
| K-2 | This folder has no A2 (static kit) arm | collab 1 vs collab 0 measures P + C together; the C share (ember search moves) cannot be separated from the P share (luna timed prompts) without A2 | `slot_type` per injection lets the analysis count search and static injections separately; the decision is Q-5 |
| K-3 | The source expects F3's C share may be near 0 (ember's "not done" mostly reflects ember's own history) | Little or no measurable effect; on hl2 C is 0 by construction at planning values | Report measured values; Q-1 |
| K-4 | Sample size | `SRCREQ` §4: even 12 runs per arm cannot detect the central estimates; a few rows per panel are a screen, not a test | Results rows carry per-package values; `alarms.py` reports, never adopts |
| K-5 | The 2 s hook allowance in R-42 is a planning value; every tool call pays the hook cost, not only checkpoints | Elapsed overhead larger than planned | S0 records `hook_ms_p95`; `collab.json` logs it per reviewer |
| K-6 | H3 changes the evidence (sandbox at the base commit, not today's HEAD) | R1 numbers are not comparable with the historical batches in `A1DIR`; only collab 1 vs collab 0 inside R1 is comparable | Both arms use the same sandbox |
| K-7 | Session persistence is on; a crash before `collab.json` exists would leave session files | Disk growth under `~/.claude/projects` | `run-reviewer.sh` writes `session_ids` into `meta.json` as soon as known, and `cleanup-sessions.sh` reads `meta.json` too |
| K-8 | The caps "at most 10 concurrent runs and at most 4 ember" span all five redesigns, and no script enforces them across folders | Gateway overload or model-identity bleed (seen in batch 3) | Each launch runs 3 sessions at a time (at most 1 ember); the owner runs at most 3 launches at once across all redesigns |
| K-9 | Gateway misrouting (batches 3, 5, 6) | A reviewer runs on another model | `model_ok` on every session; NOFALLBACK; invalid packages are never merged |
| K-10 | The judge's file path contains `r1-move-radar` | The judge can tell this design's reports from another design's, though not collab 1 from collab 0 | Opaque per-package token; both arms share the path pattern |
| K-11 | User-level hooks in `~/.claude/settings.json` add context to every reviewer session | A confound, the same in both arms and in every earlier batch | S0 lists them; held constant |
| K-12 | Haiku's median is 10 turns, so its second checkpoint (call 10) is rarely reached | Effective k ≤ 1 for haiku even if Spike 4 allows 2 | Logged as `skip` counts; moot while haiku k = 0 |

### 7.3 Open questions (owner decisions; each has a default the design already uses)

| Id | Question | Default (recommended) | What the alternative does |
|---|---|---|---|
| Q-1 | On hl2, haiku gets k = 0 at planning values. Keep the source time rule? | Keep it: hl2 then measures only the lunas' timed reading prompts and source.md checks | Allowing haiku k = 1 adds about 2 haiku turns (46 s) on the critical path; planned end about 286 s, above PANEL_FINISH_AT (275.3 s), so the +35% target is likely broken |
| Q-2 | The plan-time commits (`T1: start sha`) are not in this clone. If `git fetch origin <sha>` fails, use the first parent of each squash commit? | Yes (designSpec `0e486ab8d`, alias `38eb3c58a`, design `5fa680778`) | Those parents may hold master changes made after the plan was written, but none of the package's own repairs |
| Q-3 | Spike 4 needs how many collab-0 rows per panel? | 3 | More rows give steadier p90 values at about 9 reviewer runs per extra row |
| Q-4 | Encode the source.md check as a board line with no `move` key? | Yes | An extra id such as `SRC` would break R-07 |
| Q-5 | Add an A2 (static kit) mode to this folder, to split C from P? | No: A2 is a control shared by every design and belongs to whoever runs the stage-1 controls | Adds a `PANEL_COLLAB=kit` mode: brief with M1-M10 appended, no hooks |
| Q-6 | Commit raw transcripts and snapshots? | No, follow `A1DIR/analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md`; commit configs, values, results and audits | Large binary-like diffs in the repo |
