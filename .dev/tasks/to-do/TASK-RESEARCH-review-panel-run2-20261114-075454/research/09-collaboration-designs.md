# Research: collaboration designs F1-F7 and r1-r5 (what a shared Review Panel core must offer for collaboration)
**Investigation type:** Architecture Analyst
**Scope:** slices 05, 07, 08 in research/scope/; E2 collaboration packages r1-r5 and brainstorm 20261113-163248-panel-collaboration read only via git at tip 6c0984326cbb8fb06c4a36065de58b171d3f8175; HEAD 50d4d2b9d code for the reflect-reviewer agent and Tier 2 kernel
**Status:** Complete
**Date:** 2026-11-14
---

## 0. Method, evidence base and tag legend

- Slices read first: `research/scope/05-brainstorm-panel-collaboration.md`, `07-collab-r1-r2.md`, `08-collab-r3-r4-r5.md`. Every slice number I keep was re-derived against the blob at E2 tip `6c0984326cbb8fb06c4a36065de58b171d3f8175` (via `git show <tip>:<path>`, extracted read-only to `/tmp/review-panel-run2-2.09/x/`) or against HEAD `50d4d2b9d` (branch `ironbelly/shadow-runs`); anything not re-derived is tagged `[UNVERIFIED-slice]`.
- Path shorthand: `BP` = `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/` at the tip; `MR` = `.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md` at the tip (1130 lines; slice 05 cites the 6-line-shorter `nested/adversarial-1/merged-spec.md`, so MR line numbers below are slice numbers + 6; checked on lines 36-55, 204-253, 311-320, 917).
- Tags: `[CODE-VERIFIED]` confirmed in a blob or HEAD file at file:line; `[CODE-CONTRADICTED]` code or record shows otherwise; `[UNVERIFIED]` no corresponding code or not re-derived. pytest was NOT run (assignment does not allow it; no checkout allowed).
- No path under the run-1 research folder or the run-2 queued note was read or cited.
- Naming note: the assignment calls H1-H4 "transport requirements". In the sources H1-H4 are HARNESS FIXES (`MR:311-318`: H1 name source.md in brief, H2 truncate anchor/claim and re-ask once, H3 sandbox from the commit the plan was written against, H4 remove leak dirs). The transport requirements are R-21/R-22 and the board/seal rules (`MR:221-234`, `MR:1048-1049`). Section 6 answers item (b) for both readings.

## 1. The designs: F1-F7 families and the r1-r5 packages

### 1.1 Families and slate
- Slate (`MR:36-42`) [CODE-VERIFIED]: slot 1 F1 Between-phase cross-examination = Redesign 3 Axis-Flip Challenge (r3); slot 2 F4 Searcher-to-reader fact relay = Redesign 2 Idle-Shift Sweeper (r2); slot 3 F3 Content-free coverage steering = Redesign 1 Move Radar (r1); slot 4 F6 Steering a running strong model = Redesign 5 Coverage Deflection (r5, panel sonnet + 2x luna); slot 5 F7 Directed challenge = Redesign 4 Flag-and-Adjudicate (r4).
- Arms (`MR:46-55`) [CODE-VERIFIED]: A0 today's harness; A1 = A0 + H1-H4 (isolated baseline); A2 = A1 + static move kit M1-M10 in every brief, no communication; A3 F1, A4 F4, A5 F7, A6 F3; Stage 2 A1-SL2, A2-SL2, F6-SL2.
- F2 (mid-run method relay) and F5 (structural index / scout map) were evicted from the slate by the distinctness rule; the 25-redesign family table is from the adversarial diff analysis, which I did not open: `[UNVERIFIED-slice]` (slice 05 S6.2). Only the five slate families have packages.
- Transport tally across the 25 proposals (JSON board 17, between-phase digest + `--resume` 5, cross-session SendMessage 3, Orca mail 0, A2A 0) `[UNVERIFIED-slice]`; the rejection table for Orca mail, A2A and cross-session messaging is `[CODE-VERIFIED]` at `MR:245-253`.

### 1.2 Mechanism per package (what is exchanged, who writes, how it is delivered)
| Pkg / family | Content exchanged | Author | Delivery | Evidence |
|---|---|---|---|---|
| r1 Move Radar (F3) | one catalogue move text (<= 300 chars) or a "source.md not opened" check; no finding, path, count | harness (jq classifier on the reviewer's own telemetry) | PostToolUse hook, JSON `additionalContext`, at tool-call checkpoints | `BP r1-move-radar/tools/radar-hook.sh:39-51, :86-107` [CODE-VERIFIED] |
| r2 Sweeper (F4) | repo facts (paths, counts, path:line, the exact command) | a helper ember session via Bash helper `panel-post`, plus a harvest hook | PostToolUse hook on the two luna receivers, one fact per call from call 6 | `r2-idle-shift-sweeper/bin/hooks/receiver-hook.sh:52-88` [CODE-VERIFIED] |
| r3 Axis-Flip (F1) | a peer anchor (or a random "gap card" line) + one move, in a digest | harness from sealed phase-1 findings | between-phase `claude -p --resume <session_id>` second pass | `r3-axis-flip-challenge/bin/launch-panel.sh:5,:55` sources/launches `lib/` [CODE-VERIFIED]; mechanism text `[UNVERIFIED-slice]` (engine absent, section 3) |
| r4 Flag-Adjudicate (F7) | a card: anchor + move (+ category/severity enums in "finding form") | the flagger model (ember) via `panel-post` | PostToolUse hook on two luna adjudicators after their call 6 | `r4-flag-and-adjudicate/bin/r4-hook:75-137` [CODE-VERIFIED] |
| r5 Deflection (F6) | Task ids not covered by any finished scout (`kind:"coverage"`) | harness watcher parsing finished scouts' findings blocks | PostToolUse hook on the receiver (sonnet on SL2) | `r5-coverage-deflection/bin/hook-posttool.sh:33-72` [CODE-VERIFIED] |

Key Takeaways:
- Only F1 needs no hook; every other family needs a per-session PostToolUse hook that returns `hookSpecificOutput.additionalContext`.
- Only F4 and F7 need a model that can WRITE (Bash helper `panel-post`); F1, F3, F6 are harness-authored, so the exchange itself needs no model-side write.
- All five share one message envelope `panel-msg/1` (`MR:204-218`) but with three incompatible kinds in the packages (`challenge`, `card`, `coverage`) plus `move`, `fact` (conflict C-07).

### 1.3 The shared hook skeleton (compared line by line across r1, r2, r4, r5)
All four hook scripts implement the same skeleton, written four times [CODE-VERIFIED]:
1. every parameter baked into the command string, nothing read from the environment (R-21): `r2-receiver-hook.sh:7-9`, `r4-hook:29-36`, `r5 hook-posttool.sh:4-6`, `r1 radar-hook.sh:2-8`;
2. always exit 0, any error prints nothing and logs `hook_error` (R-22): `r1 radar-hook.sh:110-120`, `r2 receiver-hook.sh:92-101`, `r4-hook:16-27`, `r5 hook-posttool.sh:11`;
3. a subagent call (`.agent_id` non-empty) is logged and never counted or delivered: `r1:24-28`, `r4-hook:55-59`, `r5:14-15` (r2's receiver hook has no agent_id branch, whole file read);
4. per-reviewer call counter under `flock` (parallel tool calls fire several hooks at once): `r1:22`, `r2:27-28`, `r4-hook:82`, `r5:17-18`;
5. finish signal once at `now >= FINISH_MS`, nothing delivered afterwards: `r1:39-45`, `r2:43-51`, `r4-hook:66-73`, `r5:23-32`;
6. no delivery before the 6th main call (r1 uses checkpoints 6/10 and 8/12 passed as args `CP1 CP2`): `r2:52`, `r4-hook:81`, `r5:33`, `r1:47-48`;
7. seal = copy `transcript_path` to `snap/<rid>.jsonl` + sha256 immediately before the first delivery, fail closed (`snapshot_missing`), review fails open: `r1:53-65`, `r2:69-83`, `r4-hook:108-118`, `r5:42-53`;
8. output is exactly `{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":...}}`: `r1:107`, `r2:88`, `r4-hook:137`, `r5:65`.

Differences: r1 seals at the checkpoint even if no item is then chosen (`r1:53-65` precedes item choice at `:66-84`); r2/r4/r5 seal only when a delivery is about to happen (conflict X8). r4 adds a forgery check: only cards with a `post_accepted` sha in the flagger's metrics are delivered (`r4-hook:93-99`). r5 holds the `flock` to exit (`r5:17-18`), r4 holds a separate delivery lock for steps 6-10 (`r4-hook:78-82`), r2 wraps the whole call in one critical section (`r2:25-28`).

Key Takeaways:
- One shared hook library (args baked, fail-open, flock, agent_id, finish, seal, JSON output) would replace four near-identical copies; the per-design part is only "what to deliver next" (steps 7-10).
- The parallel-tool-call race (two hooks delivering the same item) was found by real smoke runs in r2 and r4 and not foreseen by their reviewed designs `[UNVERIFIED-slice]` for the review history; the fixes are visible at the lines above.

## 2. Honest evidence status per design (open item c)

### 2.1 What is in the E2 commit (re-derived)
- `git ls-tree -r --name-only <tip> -- BP/<pkg>` file counts: r1 107, r2 321, r3 130, r4 70, r5 274; paths containing `/lib/`: 0 in every package [CODE-VERIFIED]. Root `.gitignore:13` is `lib/` (unanchored), `.gitignore:79` is `*.log` [CODE-VERIFIED, blob of `.gitignore` at the tip].
- Tracked code that depends on the missing `lib/`: `r2 bin/launch-panel.sh:6` (`. "$(dirname "$0")/lib/common.sh"`), `r2 bin/hooks/receiver-hook.sh:10,:85` (`LIB=.../lib`, `render-fact.sh`), `r3 bin/launch-panel.sh:5,:55` (`../lib/common.sh`, `$R3/lib/package.sh`), `r4 bin/r4-hook:10` (`../lib/card.jq`) [CODE-VERIFIED]. r5's `lib/r5/*.py` and r4's `lib/*.py` absence is verified by the zero `/lib/` count; their call sites in r4/r5 bash are `[UNVERIFIED-slice]` beyond `r4-hook:10`.
- Consequence [CODE-VERIFIED for r2, r3, r4 by the call sites above]: r2, r3, r4 (and r5 per its own IMPLEMENTATION.md, `[UNVERIFIED-slice]` line) cannot run from the commit; their validators/renderers/engines exist only on the producer's disk. r1 keeps all its tools tracked (its tree has no `lib/` by design, slice 07 A1 package inventory) but `values/` and `runs/` are not tracked, so a collab-1 launch exits 2 for lack of a values file.
- `runs/` (boards, reviews, collab.json, audit.json, session copies) absent at the tip for r3/r4/r5 `[UNVERIFIED-slice]` (slice 08 D-ALL-1; only the `/lib/` count was re-run by me). So even the smoke rows below cannot be re-derived from the commit beyond their summary JSON.

### 2.2 Claimed vs static test counts (pytest NOT run; no checkout allowed)
| Pkg | Claimed passed (source line) | Static `def test_` count at tip | `parametrize` markers | Reading |
|---|---|---|---|---|
| r1 | 138 (`r1 IMPLEMENTATION.md:14,:74`) | 103 in 21 files | 5 | claim plausible only through parametrize expansion `[UNVERIFIED]` |
| r2 | 358 (`r2 IMPLEMENTATION.md:80`) | 163 in 18 files | 10 | same; 176 cases claimed for `test_values` `[UNVERIFIED]` |
| r3 | 89 (`r3 IMPLEMENTATION.md:11,:77`) | 89 in 22 files | 0 | static count equals the claim [CODE-VERIFIED static]; the cited log `spikes/ac14/resume/tests-final.log` is not in the tree `[UNVERIFIED-slice]` |
| r4 | 106 (`r4 IMPLEMENTATION.md:12,:94`) | 90 in 15 files | 5 | gap of 16 not reproducible; log `/tmp/collab-r4/pytest-final.log` outside the commit |
| r5 | 108 (`r5 IMPLEMENTATION.md`, slice I1) | 82 in 13 files | 4 | `tests/last-run.txt` tail reads `108 passed in 97.06s` and `rc=0` [CODE-VERIFIED as a recorded log, not a re-run]; gap of 26 not reproducible |
The claimed totals (138, 358, 89, 106, 108) are therefore `[UNVERIFIED]` as counts of passing tests; at most they are recorded self-reports.

### 2.3 Measured results: single smoke rows only
- r1 (`BP r1-move-radar/spikes/gate0.json`, checked 2026-11-13T23:24:19Z): G-BASE pass, G-PINS pass, S0 pass, S2 pass, REQ-S3 recorded, S3 missing, Spike 4 missing [CODE-VERIFIED]. `results/el2-c0-r0.json`: collab 0, status `incomplete`, designSpec only, elapsed 107.105 s, output tokens 21,127, ledger rows 2, `gt_covered_any` [], wrong blockers 0, `reask` 1, `dropped_lines` 0, injections 0 [CODE-VERIFIED]. The one collab-1 row is a scratch "provisional" row, not a Gate 0 pass `[UNVERIFIED-slice]` (file not re-opened).
- r2 (`spikes/RESULTS.md`, 34 lines) [CODE-VERIFIED]: H3 FAIL then PASS; Catalogue PASS; S0 PASS ember and luna (hook p95 73 ms and 81 ms, line 8-9); S2 PASS four models (first line 997-1094 ms, wall 3,564-5,094 ms, lines 11-14); SW-1 PASS; REQ-S3 ember probe 0/4, finish 0/5, luna probe 4/5, finish 5/5 (lines 25-28); S3 FAIL at 21:39:26Z, 21:55:56Z and 23:01:47Z, then "PASS" at 23:02:08Z as "re-check after audit rule fix (no new model runs)" (line 33). Six smoke rows, control package only, all `planning:true`, k=2 (`results/smoke-*.json`): elapsed el2 collab 97.235 s vs iso 130.422 s; sl2 collab 184.372 s vs iso 220.371 s; hl2 collab 230.535 s vs iso 161.314 s [CODE-VERIFIED]. The collab arm is faster in two of three pairs and slower in the third; with n=1 per cell this is noise (see r3 below where the same arm varies 95-155 s). Spike 4 has no line in RESULTS.md (not run).
- r3 (`results/smoke.jsonl`, 4 rows, el2, control package) [CODE-VERIFIED]: A3 158.831 s and 158.810 s; A1 95.168 s and 154.784 s; output tokens 41,044 / 29,898 (A3) and 19,059 / 25,704 (A1); `control_found2` 0 in all four; control wrong blockers 2, 4 (A3) and 2, 2 (A1); `phase2_timeout` 1 in both A3 rows. The A1 baseline alone spans 95.2-154.8 s, so the +30% overhead of the A3 rows cannot be read as a design effect. Gate 0 detail (luna kill-text FAIL, S2 resume wall times, G0-SURF 4.8% then calibrated) `[UNVERIFIED-slice]`.
- r4: act rates in `spikes/out/act-rates.json`: haiku 0/0, sonnet 0.6 / 1, luna 0 / 0.4, ember 0 / 0 (act / finish; 5, 5, 5, 4 sessions) [CODE-VERIFIED]. `manifest.json`: base trees `69f360d5...`, `fdb08e60...`, `c1a436ae...`, with `first_commit` and `first_commit_parent` empty and `parent_tree_equals_base:false` [CODE-VERIFIED]. By its own gate ("F7 runs only with a non-zero luna act rate", `r4 IMPLEMENTATION.md:159`) the F7 arm should not run on a 0/5 luna rate; the smoke rows (EL2, control, one valid F7 row, one A1 row) are `[UNVERIFIED-slice]` (results files not re-opened).
- r5 (`results/results.jsonl`, 5 rows, sl2, control package) [CODE-VERIFIED]: A1 179.561 s and 174.274 s (29,688 and 29,622 tokens), A1 smoke 180.318 s, A2 281.567 s (46,018 tokens), F6 diagnostic 266.372 s `quarantined` (12,798 tokens). Derived by me: A2 vs mean of the two A1 pilot rows = 281.567 / 176.9175 = 1.59 (+59%), tokens 46,018 / 29,655 = 1.55 (+55%): the static kit alone is a large treatment on sonnet (one package, three runs). `spikes/NOTES.md:36-39` REQ-S3: sonnet act 5/5 finish 5/5, haiku 0/5 and 0/5, luna 1/5 and 3/5; `:50` Spike 4 pilot row gives `k` 0, `budget_ok` false; `:67-75` the diagnostic row proves the watcher-to-card-to-hook-to-receiver chain delivered one card to sonnet at call 18 and then sonnet ran to the hang guard [CODE-VERIFIED].
- No design has a measured effect on the 14 known defects: every defect-package row is absent; control-package rows find 0 or 1 of 2 items. `found_14` is null or 0 everywhere. The packages' own text says so (`MR:1128`: the plan cannot detect the central gain estimate of any slot [CODE-VERIFIED]).

Key Takeaways:
- Evidence status of every design is the same: built (partly, with an absent engine), gate-0 partly passed, one to six single smoke rows on a 2-item control package, no quality or cost measurement.
- `lib/` is absent for r2 to r5 so they cannot run from the commit; the claimed test counts (138, 358, 89, 106, 108) are self-reports, and static counts agree only for r3.
- The only number with some weight is the kit cost on sonnet in r5 (+59% elapsed, +55% tokens, n=3 runs, one package).

## 3. Per-design requirement tables (what each needs of a core, what it offers)

| Need / offer | r1 F3 | r2 F4 | r3 F1 | r4 F7 | r5 F6 |
|---|---|---|---|---|---|
| Session persistence ON (drop `--no-session-persistence`) | yes (snapshot reads `transcript_path`, resume for H2 re-ask) | yes | yes (resume) | yes (`--session-id`, resume re-ask) | yes (resume re-ask only) |
| Per-session `--settings` hook JSON | yes, all 3 reviewers | receivers + sweeper | none | yes, all reviewers | receiver only |
| Model-side write (Bash helper) | none | sweeper `panel-post` | none | flagger `panel-post` | none |
| `--resume` second pass | H2 re-ask only | H2 re-ask only | the mechanism | H2 re-ask only | H2 re-ask only |
| Extra model session | none | sweeper ember | none | none | none |
| Baseline timing needed (B_f, turn_p90, T_report_p90) | yes | yes | yes | yes | yes |
| Role map per panel | searcher / reader | receiver / non-receiver / sweeper | searcher / reader | flagger / adjudicator (HL2 refused if k=0) | scout / receiver (roles inverted on EL2) |
(rows from slices 07 and 08 C2/S5.4/S7.3 tables, `[UNVERIFIED-slice]` except the hook rows verified in section 1.3.)

Direction-of-flow contradiction for the strong model on SL2/HL2 (`[UNVERIFIED-slice]` slice 08 S9.1/C-06): r3 searcher (sends and receives), r4 flagger (sends only), r5 receiver (receives only). The core cannot fix a role per model; the role must be a per-use-case table.

## 4. What a shared core must offer for collaboration vs what `reflect-reviewer` can host (open item a)

### 4.1 Capabilities the five designs demand of a core (union, from sections 1.3 and 3)
1. A headless reviewer runtime where the core owns the process: `claude -p` with per-session `--settings`, a hang guard (`timeout --kill-after=5`), model identity check per session, no fallback ladder (R-05, `MR:1009`).
2. Session persistence ON (needed for resume and for `transcript_path` snapshots). HEAD's Tier-1 reflect child is launched with `--no-session-persistence` (`src/superclaude/cli/reflect/runner.py:503-505`, command text at `:496-505`) [CODE-VERIFIED].
3. Hook points: PostToolUse with JSON `additionalContext`, a finish signal, a per-session call counter under `flock`, distinction of subagent calls (section 1.3).
4. Resume: `claude -p --resume <session_id> --output-format stream-json --verbose`. S2 PASS for ember, luna, sonnet, haiku in r2 (`BP r2 spikes/RESULTS.md:11-14`: first stream line 997-1094 ms, wall 3,564-5,094 ms) [CODE-VERIFIED]; r4 records a haiku "strict fail" and r3 a luna kill-text FAIL `[UNVERIFIED-slice]`.
5. A board path outside the reviewed tree: `$BOARD/<row>/<pkg>/`, baked absolute into the hook command, atomic appends, model-authored lines only through a validated helper (`MR:221-227`) [CODE-VERIFIED].
6. A seal: process exit (F1) or hook-side transcript copy + sha256 before first delivery, fail closed (`MR:229-234`, hook lines in 1.3) [CODE-VERIFIED].
7. A message-kind registry with per-kind key tables and a leak check (three incompatible kinds today, conflict C-07), forbidden keys `claim verdict blocking severity category note` (`MR:215`) [CODE-VERIFIED].
8. Budget math needing a per-package baseline (`B_f`, `turn_p90`, `T_report_p90`): none of the five packages has run Spike 4 (r1 gate0.json "Spike 4: missing"; r4 and r5 per slice `[UNVERIFIED-slice]`; r2 RESULTS.md has no Spike 4 line).
9. Ground-truth-free alarms (CONVERGENCE, SNAPSHOT, SLO, DEFLECTION) and an arm kill switch `PANEL_COLLAB` that must restore the isolated panel (`MR:258`) [CODE-VERIFIED]. The judge, anonymiser and score rows are study scaffolding (eval-only), not product runtime.

### 4.2 What the read-only `reflect-reviewer` agent can host (HEAD `50d4d2b9d`)
- Tool allowlist is `Read, Grep, Glob, augment search, auggie retrieval, codegraph search/node/callers/impact`; no Bash, Edit, Write or Task (`src/superclaude/agents/reflect-reviewer.md:5`; same statement in `src/superclaude/skills/sc-reflect-protocol/SKILL.md:640`) [CODE-VERIFIED]. `model: sonnet`, `maxTurns: 50`, `permissionMode: plan` (`reflect-reviewer.md:6-8`). The agent has no `hooks:` frontmatter key (lines 1-9 read) [CODE-VERIFIED].
- It is told "you do not coordinate with the other reviewers" (`reflect-reviewer.md:28`) and the brief "MUST NOT instruct you to run anything" (`:59`). F4's delivery text asks the receiver to re-run a command itself and F7's adjudicator is told to "run a finite check" (r2/r4 text, `[UNVERIFIED-slice]`); a no-Bash reviewer can only Grep/Read, so those two instructions are not executable as written.
- Hosting by family:
  - F4 sweeper and F7 flagger are model-authored through the Bash helper `panel-post` (`MR:224`): a no-Bash agent cannot post, so it can be a RECEIVER but never a sweeper or flagger. A flagger or sweeper must be a separate Bash-capable session.
  - F3, F6 (harness-authored) and F1 (between-phase) need no model write; they need a delivery path.
  - Delivery by hook: the Claude Code subagent documentation (https://code.claude.com/docs/en/sub-agents, section "Define hooks for subagents", extracted 2026-11-14) says settings.json PostToolUse hooks fire for a subagent's tool calls and that a subagent's frontmatter may declare `hooks`. So a hook CAN run for a `reflect-reviewer` subagent. But the E2 hook scripts deliberately skip any call carrying `agent_id` (`r1 radar-hook.sh:24-28`, `r4-hook:55-59`, `r5 hook-posttool.sh:14-15`) [CODE-VERIFIED]: a reviewer that is itself a subagent of an orchestrator session would receive nothing from them. Whether `additionalContext` from a PostToolUse hook reaches a SUBAGENT's model is [UNVERIFIED]: the E2 S0 spikes show delivery only for main-thread `claude -p` sessions (`r2 RESULTS.md:8-9` `delivered_in_transcript=true`; r5 `NOTES.md:18-20` `subagent_calls=0`).
  - Radar classifier signatures M1/M2/M4/M7 are Bash grep/find patterns; a Grep/Glob/codegraph reviewer leaves a different trace (slice 05 DEF-11 `[UNVERIFIED-slice]`; slice 07 says M2 also matches Grep `output_mode` `[UNVERIFIED-slice]`).
- HEAD's CLI Tier-2 path does not use agents at all: `src/superclaude/cli/reflect/ensemble.py:1-24` says Tier 2 invokes the swarm run surface (`dispatch_wave1`) with no in-process agent fan-out, and the swarm transport sends one user message and reads text back (`src/superclaude/cli/swarm/transports/openai_compat.py:384-388`, `"messages": [{"role": "user", "content": prompt}]`) [CODE-VERIFIED]. There is no tool loop, so no PostToolUse hook point and no session to resume; only a between-phase exchange (a second prompt carrying the first answer) is expressible there.
- `reflect --resume` at HEAD (`src/superclaude/cli/reflect/commands.py:290-294, :552-553`) means "skip the launch when the prior reflect_post is a pass on the current HEAD", not a model-session resume [CODE-VERIFIED]; the name collides with `claude --resume`.
- Review-sandbox isolation exists at HEAD for the reflect children (`create_review_snapshot`, `src/superclaude/cli/reflect/config.py:155-210`, `git worktree add --detach`), pinned off by default (`models.py:94` "PINNED OFF") [CODE-VERIFIED]; it plays the role of E2's H3/H4 sandbox but with a different base rule (committed ref of the audit), see C-01.

Resolution of (a): the core must define an OPTIONAL exchange capability with three implementations by runtime: (i) between-phase (F1-style; needs neither a hook nor a model-side write, only the two prompts and a seal by process exit, so it is the only family expressible in every runtime HEAD has; it has no clean measured success in any runtime: both r3 A3 smoke rows record `phase2_timeout` 1 (s2.3, `results/smoke.jsonl`), r3's luna kill-text FAIL is [UNVERIFIED-slice], and F1 as built is a `claude -p --resume <session_id>` second pass whose `--resume` dependency for gateway ids is [UNVERIFIED] (research-notes.md:262); no F1 run exists on a swarm worker, which gets one user message and no session, or on an Agent-tool agent) [fix cycle 1: the earlier wording "works for a swarm or any runtime" was an unsupported conclusion built on an [UNVERIFIED] row], (ii) hook-delivered (needs a `claude -p` main-thread session with persistence and `--settings`; excludes the swarm workers and, unverified, subagents), (iii) Bash-authored board posts (needs a Bash-capable session; excludes `reflect-reviewer`). The `reflect-reviewer` agent as defined can host only receiver-side delivery of harness-authored items, and only after an unverified subagent-delivery check; nothing in the core should assume more.

Key Takeaways:
- Of the exchange families, F1 is the only one that needs neither a hook nor a model-side write, so it is the only one expressible in every runtime HEAD already has (swarm text-in/out, headless sessions, Agent-tool agents). It has no clean measured success in any runtime (both r3 A3 smoke rows `phase2_timeout` 1, s2.3; r3 luna kill-text FAIL [UNVERIFIED-slice]; r4 haiku "strict fail" [UNVERIFIED-slice], see the S2 line at :107) and its `--resume` dependency for gateway ids is [UNVERIFIED]. Keep the recommendation to leave exchange optional. [Fix cycle 1: "works in every runtime" was unsupported.]
- Hook-based families are tied to main-thread `claude -p` sessions; the packages' own hooks skip subagent calls by design.
- A no-Bash agent can never be a sweeper or flagger; it can at most be a receiver.

## 5. Should H1-H4 (and the transport rules) be unconditional core requirements? (open item b)

| Item | Evidence | Verdict |
|---|---|---|
| H1 name the driving document in the brief | motive: 156 of 665 historical runs never opened source.md `[UNVERIFIED-slice]` (from the study report, not re-derived); estimated +0.03 per run (0.01-0.08) `[UNVERIFIED]` planning value (`MR` H table, slice 05 S3.27) | UNCONDITIONAL as a general rule "every driving document is named by path and hash in the brief" (cost near 0, independent of collaboration); effect size unmeasured |
| H2 truncate anchor/claim, validate with the real parser, one re-ask | HEAD still rejects anchor over 200 and claim over 300 characters: `src/superclaude/cli/review/findings.py:104,118` and `findings_v2.py:111,126,132,136` [CODE-VERIFIED]; a real ember re-ask happened in r1's one real row (`el2-c0-r0.json` `reask` 1, `dropped_lines` 0) [CODE-VERIFIED]; five packages re-implemented it (slice 07 C3 `[UNVERIFIED-slice]`) | UNCONDITIONAL, belongs in the core as a pre-merge normaliser; independent of collaboration |
| H3 sandbox from the commit the plan was written against | meaningful only for plan-vs-implemented-repo review; the three E2 packages disagree on the base (C-01, r4 `manifest.json` first_commit empty [CODE-VERIFIED]); r5's snapshot loses tracked-but-ignored files (`r5 bin/sandbox-build.sh:25` `git add -A` without `-f`) [CODE-VERIFIED] | CONDITIONAL: a core "evidence snapshot" interface with a recorded base; the base rule is per module (PR review = PR base, reflect = committed ref) |
| H4 remove leak directories | the principle (no earlier review output reachable) is general; the list (`.dev/reflect`, `.dev/research`, `.dev/eval-workspaces`, `.dev/tasks/done`, `MR:317-318`) is repo- and study-specific; HEAD's L2 snapshot is off by default (`models.py:94`) | principle UNCONDITIONAL, list per module |
Transport reading (R-21/R-22/seal/board): NOT unconditional. They are required only when an exchange arm is on. Always-on core pieces from this family are: session-persistence choice, transcript capture, fail-open semantics, per-kind schema validators, and a kill switch whose off state is byte-comparable to the isolated arm (argv-diff test; `r1` T-10 and r2 `test_launch_command_diff.py`, `[UNVERIFIED-slice]`). Reasons: three of HEAD's reviewer runtimes (swarm workers, Agent-tool reviewers, headless sessions) cannot all carry hooks (section 4.2), and no design has measured value (section 2).

## 6. Conflicts X1-X17 (slice 07 C9, r1 vs r2) and C-01..C-19 (slice 08 S9.2): decidable by evidence or not (open item d)

Classes: **E** = decidable by evidence in hand; **E-partial** = part decidable, rest needs a measurement not yet run; **D** = a design or owner decision, evidence cannot settle it; **N** = not decidable now (needs a measurement that does not exist). Every statement below is re-derived unless tagged.

### 6.1 X1-X17
| ID | Conflict | Class | Evidence |
|---|---|---|---|
| X1 | ember act rate on injected text: r1 1.00 / r2 0/4 | N | r1 `reqs3.json` ember: item acted next call in 3 of 3 sessions, finish acted in 1 of 3 (sessions 1 and 3 kept calling 7 and 4 times after the finish text) [CODE-VERIFIED]; r2 `RESULTS.md:25-26` 0/4 and 0/5; r4 `act-rates.json` ember 0 and 0 over 4 sessions [CODE-VERIFIED]. Three different probes; none is a production measure; a common probe is missing |
| X2 | luna act rates | N | r1 item 0.33 next call / 1.00 later, finish 1.00 (3 sessions) [CODE-VERIFIED]; r2 4/5 and 5/5 (`RESULTS.md:27-28`); r4 0 and 0.4; r5 1/5 and 3/5 (`NOTES.md:38`). Slice 07 called r1 and r2 "compatible"; adding r4 (0/5) contradicts that reading. Same model, rates 0 to 0.8 |
| X3 | which reviewers get "finish now" | D | the signal is ignored by ember in every probe (X1 data), so only luna/sonnet are bounded by it; the hang guard is the real bound. r1 all three, r2 receivers only: owner/symmetry decision |
| X4 | k on HL2 | E-partial | k formula and planning thresholds are arithmetic (r1 `values.py:89-100` region, `[UNVERIFIED-slice]` for the thresholds); measured k needs Spike 4, run by none. r5 pilot gave k=0 for sonnet on one package (`NOTES.md:50`) [CODE-VERIFIED] |
| X5 | turn measurement for Spike 4 | E | `r1 tools/values.py:89-100` groups assistant entries by `message.id`, skips `parent_tool_use_id` entries, leaves out the first response; `r2 py/values.py:70` `turn_durations` and `:112` `ds[-1]` as `T_report` do not [CODE-VERIFIED]. r1's rule is the right one; bias magnitude (-3% to -11% per model) `[UNVERIFIED-slice]` |
| X6 | gateway lock | D | process rule; r1 kept to 3 sessions, r2 used `flock /tmp/collab-gateway.lock` and ran 4 sessions on SL2/HL2 `[UNVERIFIED-slice]` |
| X7 | session files kept vs deleted | D | depends on which reducer reads them; r2 `values.py:70` reads transcripts, r1 reads kept attempt JSON `[UNVERIFIED-slice]` for the r1 side |
| X8 | seal timing | E | r1 seals at the checkpoint before choosing an item (`radar-hook.sh:53-65`, item choice `:66-84`); r2 seals immediately before the first delivery (`receiver-hook.sh:69-83`) [CODE-VERIFIED]; `MR:232` says "Immediately before the first delivery". r2 matches the requirement, r1 deviates |
| X9 | retry and re-ask time thresholds (r1 30 s / r2 10 s) | D | unify; no evidence either value is better |
| X10 | catalogue artifact hash | E | same M1-M10 text, different wrapper (`r1-cat/1` vs `moves/1`) `[UNVERIFIED-slice]` (diff done by slice 07, not repeated); settle by one source file |
| X11 | `origin` tag in the findings line | E-partial | HEAD `findings.py:_check_finding` (lines 90-121) and `findings_v2.py:check_finding` (lines 84-153) reject no unknown key; v2 rejects only `calibrated_confidence` (`findings_v2.py:96-97`) [CODE-VERIFIED, negative grep for key-set checks in both files]. So an in-line `origin` key passes both checkers; clustering and card conversion downstream not checked [UNVERIFIED]. Placement (in-line vs sidecar) remains D |
| X12 | smoke honesty | E | r1 `gate0.json` shows S3 "missing" and labels the collab-1 row provisional; r2 `RESULTS.md:30-33` three S3 FAILs then PASS "no new model runs" after an audit-rule change [CODE-VERIFIED]. r2's PASS is a re-grading, not a re-run |
| X13 | hand-off claims vs files | E | r2 `lib/` absent (`/lib/` count 0; call sites in 2.1); r1 138 claimed vs 103 static (2.2) [CODE-VERIFIED] |
| X14 | contract shape: "succeeded" over a FAIL | D | return contracts `[UNVERIFIED-slice]`; a `last_verdict`/unreviewed-fix field is a contract design choice |
| X15 | DESIGN says "not implemented" beside an IMPLEMENTATION.md | E | `r1 DESIGN.md:7` "Nothing here is implemented yet", `r2 DESIGN.md:5` "design only. Nothing in this document is built" while both packages have IMPLEMENTATION.md [CODE-VERIFIED]; status lines are stale by construction |
| X16 | planning numbers vs real | E | r1 collab-0 107.105 s vs planning B 116 s = -7.67% (`el2-c0-r0.json`); r5 A1 179.561 s vs planning 269 s = -33.25% in its row (`results.jsonl`) [CODE-VERIFIED]; planning B is not a baseline |
| X17 | Opus used outside the judge | D | self-reported in r1 `IMPLEMENTATION.md` `[UNVERIFIED-slice]` for the line; a rule to encode in the runner |

### 6.2 C-01..C-19
| ID | Conflict | Class | Evidence |
|---|---|---|---|
| C-01 | H3 base: r3/r5 parent commit vs r4 T1-start tree | D (facts E) | r4 `manifest.json` lists base trees `69f360d5...`, `fdb08e60...`, `c1a436ae...`, `first_commit` "" and `parent_tree_equals_base` false [CODE-VERIFIED]; the commit/tree object comparison of slice 08 `[UNVERIFIED-slice]`. Choice is a module rule |
| C-02 | peer/own tag in-line vs sidecar | D | see X11: both checkers tolerate an extra key |
| C-03 | transcript of a hang-killed reviewer | E-partial | r5 `NOTES.md:74` shows no copy exists for a killed receiver and the card text is then not visible to the check; r4's `--session-id` is the alternative (`[UNVERIFIED-slice]`); whether `--session-id` is an allowed R-05 difference is D |
| C-04 | admission / concurrency counting | D | three mechanisms (slice 08 S9.1) `[UNVERIFIED-slice]`; one shared launcher mechanism is needed |
| C-05 | judge output location | D | study-only (judge wrapper) |
| C-06 | strong-model direction on SL2/HL2 | N | r3 sends+receives, r4 sends only, r5 receives only; no quality data for any |
| C-07 | one schema, three kinds | D | union with per-kind key table (`MR:204-218` is the base) |
| C-08 | 12-char rule vs exact-quote anchors | E (logic) | an exact 12-200 character substring of the candidate (`MR:216`) necessarily shares 12 characters with the plan text; the rule as written (`MR:970` in slice numbering) cannot hold for anchored kinds; three designs resolved it three ways `[UNVERIFIED-slice]` for the resolutions |
| C-09 | re-ask without model identity check | E | defect class found independently in r3, r4, r5 reviews `[UNVERIFIED-slice]`; resolved in designs |
| C-10 | k test-vector rounding (23.8 vs 23.795) | E | pure arithmetic; origin in the source wording `[UNVERIFIED-slice]` |
| C-11 | r5 snapshot flag | E | `r5 bin/sandbox-build.sh:25` runs `git add -A` with no `-f` [CODE-VERIFIED]; r3/r4 use `-f` `[UNVERIFIED-slice]`; r3's smoke found tracked-but-ignored files lost `[UNVERIFIED-slice]` |
| C-12 | session cleanup | D | |
| C-13 | only r5 builds A2 | E-partial | r5 pilot: kit alone +59% elapsed, +55% tokens (section 2.3) [CODE-VERIFIED]; whether any exchange beats the kit is N |
| C-14 | act rate measured twice, different results | N | same as X1/X2 (`act-rates.json` vs `NOTES.md:36-39`) [CODE-VERIFIED] |
| C-15 | hook latency vs 0.1 s budget | E | measured p95 ranges: r2 73 and 81 ms (`RESULTS.md:8-9`), r5 57-85 ms (`NOTES.md:18-20`) [CODE-VERIFIED]; r4 143 and 90 ms `[UNVERIFIED-slice]`. Measured cost is tens to about 150 ms per call; the 0.1 s design budget is exceeded in one package |
| C-16 | sealed judging | D | study-only |
| C-17 | reviewer id conventions | D | `t4-1` is luna in r3/r4 and haiku in r5 hl2 `[UNVERIFIED-slice]` |
| C-18 | orchestrator rule drift | D | process, not product |
| C-19 | ledger outcome differs | E | process record; r2's ledger `blocked` and r1 `complete` per slice 07 `[UNVERIFIED-slice]` |

Count (mine, from the two tables; classes as assigned above): 36 conflicts = 13 class E (X5, X8, X10, X12, X13, X15, X16, C-08, C-09, C-10, C-11, C-15, C-19), 4 class E-partial (X4, X11, C-03, C-13), 4 class N (X1, X2, C-06, C-14), 15 class D (X3, X6, X7, X9, X14, X17, C-01, C-02, C-04, C-05, C-07, C-12, C-16, C-17, C-18). Three class-E rows (X10, C-09, C-10) rest on slice statements I did not repeat and carry `[UNVERIFIED-slice]`.

## 7. E2's own statement that a static move kit may beat every exchange design (open item e)

- `MR:917` [CODE-VERIFIED]: "The static kit (A2) may beat every exchange design on gross gain, because it gives every reviewer all the moves from the first second. An exchange design earns its place only if it beats A2 by the margin set in section 4. If none does, the right design is the cheapest one: the harness fixes plus the kit in the brief."
- `MR:396` [CODE-VERIFIED]: for Move Radar "F3's collaboration share may be near 0"; A6 vs A2 is read as "telemetry-timed kit against static kit". `MR:909` lists A2 at about +29% elapsed (V5 estimate, UNVERIFIED) and `MR:1117` lists the kit cost as unmeasured pending Spike 4.
- Evidence now: r5 measured the kit alone on sonnet at +59% elapsed and +55% output tokens (one package, three runs); r3 and r4 did not build A2 so their results cannot separate collaboration from prompting; r1 K-2 and r2 likewise `[UNVERIFIED-slice]`. No measurement compares any exchange arm with A2. `MR:1128` states the plan cannot detect the central gain of any slot at n=12.
- Conclusion supported by the evidence: the kit-beats-exchange hypothesis is neither confirmed nor refuted; it is the cheaper default and the only treatment with any measured cost. A core should therefore (1) ship the harness fixes and a per-module lens/move catalogue as the unconditional layer, (2) treat exchange as an optional capability behind a kill switch whose off state is the A1/A2 arm, and (3) not build the hook transport into the core until an exchange arm beats A2 on a package with real ground truth.

## Gaps and Questions

1. [UNVERIFIED] No pytest run: claimed 138 / 358 / 89 / 106 / 108 and the claimed durations are self-reports. Static counts: 103 / 163 / 89 / 90 / 82 (searched: `git show <tip>:<file>` over every `test_*.py`, count of `def test_`; parametrize markers 5 / 10 / 0 / 5 / 4). Only a run in a checkout of the E2 branch can settle it; not allowed here.
2. [UNVERIFIED] r2-r5 engine code: `lib/` absent from the commit (0 paths); so the r2 validator and renderer (`validate-msg.sh`, `render-fact.sh`), r3's whole engine, r4's `lib/*.py` + `card.jq`, r5's `lib/r5/*.py` could not be read. Searched: `git ls-tree -r --name-only <tip> -- BP/<pkg> | grep /lib/` for each package (0 hits). The mechanisms of r3 (digest selection, deal, combiner) rest on DESIGN text only.
3. [UNVERIFIED] r3 and r4 results rows, r4 `results/*.json` smoke rows, r1 provisional collab-1 row, r2 token ratios and hook p95 for r4 (143/90 ms) were not re-opened; they are cited from the slices and tagged `[UNVERIFIED-slice]`.
4. [UNVERIFIED] Whether PostToolUse `additionalContext` reaches a subagent's own model (needed for `reflect-reviewer` as a hook receiver). Searched: Claude Code sub-agents documentation (hooks fire inside subagents; frontmatter `hooks`), E2 spike records (main-thread sessions only). No test exists in this repo.
5. [UNVERIFIED] Whether downstream HEAD consumers (`cluster.py`, `card_convert.py`, `merge_cmd.py`) preserve or drop an extra in-line key such as `origin`; only the two checkers were read (X11).
6. Naming ambiguity: the assignment says "transport requirements H1-H4"; the sources define H1-H4 as harness fixes. Answered for both readings (section 5). If the task author meant a different numbered set, no H-numbered transport list exists in the tip's `merged-requirements.md` (searched for `H1`, `H2` headings; only `MR:311-318`).
7. Question for the synthesis: which common act-rate probe (X1/X2/C-14) should become the capability-table entry per model? The three probes disagree by 0 to 0.8 for luna.
8. Question: is an exchange capability worth a core interface before any arm beats the static kit (section 7)? Evidence says no measurement exists; recommendation in section 7 is to keep it optional.
9. The brainstorm folder's debate and diff-analysis artifacts (family table of 25 proposals, A-001..A-011 assumptions) were not opened; family F2/F5 content is `[UNVERIFIED-slice]`.
10. Scratch copies of tip blobs were made under `/tmp/review-panel-run2-2.09/` (permitted scratch dir) and are deleted before return.

## Stale Documentation Found

- **[STALE DOC]** `r1 DESIGN.md:7` "Nothing here is implemented yet" and `r2 DESIGN.md:5` "design only. Nothing in this document is built": both packages contain built tools and an IMPLEMENTATION.md [CODE-CONTRADICTED] (X15).
- **[STALE DOC]** `r2 IMPLEMENTATION.md` lists `bin/lib/*` as built; the committed tree has no `lib/` paths and `.gitignore:13` ignores `lib/` [CODE-CONTRADICTED].
- **[STALE DOC]** r3, r4 and r5 IMPLEMENTATION files cite logs (`spikes/ac14/resume/tests-final.log`, `/tmp/collab-r4/pytest-final.log`) and `runs/` folders that are not in the commit [UNVERIFIED for r3's log and `runs/` per slice; `/tmp` path is outside the repo by construction].
- **[STALE DOC]** Slice 07 conflict X2 "compatible once the next-call caveat is applied" is weakened by r4 and r5 act rates (0/5, 1/5 for luna) which slice 07 did not have [CODE-CONTRADICTED by `act-rates.json`, `NOTES.md:38`].
- Slice 05 cites `merged-spec.md` line numbers; the copy in the brainstorm folder (`merged-requirements.md`) has the same text at line + 6 (checked at five anchors); not a content conflict.

## Summary

Five collaboration designs (F1 Axis-Flip, F3 Move Radar, F4 Idle-Shift Sweeper, F6 Coverage Deflection, F7 Flag-and-Adjudicate) were built as packages r1-r5 on the E2 branch; four of the five rely on the same hook skeleton (baked args, fail-open, flock, agent_id skip, finish signal, transcript seal, JSON additionalContext), written four times, and only F4/F7 need a model that can write via Bash. Evidence is thin: single smoke rows on a 2-item control package, no Spike 4, no defect-package run, `lib/` missing from the commit for r2-r5, and claimed test counts that match static counts only for r3; the one weighty number is r5's static kit costing +59% elapsed on sonnet. A shared core should make H1 and H2 unconditional (HEAD still rejects anchors over 200 and claims over 300 characters), make H3/H4 per-module snapshot rules, and offer exchange only as an optional capability: the HEAD Tier-2 swarm has no tool loop, `reflect-reviewer` has no Bash and is skipped by the packages' own subagent filter, so only a between-phase exchange fits every runtime. Of 36 logged conflicts, 13 are settled by evidence, 4 partly, 4 cannot be decided without a common act-rate probe or Spike 4, and 15 are design decisions; E2's own claim that a static kit may beat every exchange design is neither confirmed nor refuted.
