# Redesign 5 Gate 0 spike notes

One section per spike run: command, date, transcript folder, PASS/FAIL (DESIGN 6.3). Sections are appended by the spike scripts; S-H3 was recorded by hand from its log.

## S-H3 sandbox build: PASS (2026-11-13, between 20:50Z and 20:59Z; the log has no timestamp)

Command: `bash bin/sandbox-build.sh` (no model calls). Log: `spikes/out/s-h3/build.log`.

- Manifest `/tmp/evalsb-collab-r5/manifest.json` lists the three base SHAs of DESIGN 0.2: designSpec `0e486ab8d0eb24c6f2738ce1f895cc16755b26c1`, alias `38eb3c58afe6988b51060ae14117172869ea4c1e`, control `5fa680778718af9087ccbe7a823e3909f1bcceb6`.
- `.dev/reflect`, `.dev/research`, `.dev/eval-workspaces` and `.dev/tasks/done` are absent in all three sandboxes; `git status --porcelain` is empty in all three.
- The designSpec sandbox contains no `merge-guard.md` anywhere (`find ... -name merge-guard.md` printed nothing).
- The control sandbox has `tests/skills/test_worker_contract.py`.

## S0 hooks: PASS (2026-11-13T21:00:18Z)

Command: `flock /tmp/collab-gateway.lock bash spikes/s0-hooks.sh` (NOFALLBACK=1). Transcripts: `spikes/out/s0/20261113T205926Z/`.

- claude-sonnet-5-5: PASS (rc=0 observed=claude-sonnet-5-5 main_tool_calls=4 hook_calls=4 subagent_calls=0 delivered=1 card_text_in_transcript=3 snapshot_sha_ok=true hook_ms_p95=59 wall_ms=13083)
- claude-haiku-5-5: PASS (rc=0 observed=claude-haiku-5-5 main_tool_calls=4 hook_calls=4 subagent_calls=0 delivered=1 card_text_in_transcript=3 snapshot_sha_ok=true hook_ms_p95=57 wall_ms=10867)
- gpt-6-luna: PASS (rc=0 observed=gpt-6-luna main_tool_calls=5 hook_calls=5 subagent_calls=0 delivered=1 card_text_in_transcript=3 snapshot_sha_ok=true hook_ms_p95=85 wall_ms=27795)
- user/project hooks active in the sandbox: `spikes/out/s0/20261113T205926Z/hooks-active.txt`

## S2 resume: PASS (2026-11-13T21:04:22Z)

Command: `flock /tmp/collab-gateway.lock bash spikes/s2-resume.sh` (NOFALLBACK=1). Transcripts: `spikes/out/s2/20261113T210335Z/`. Planning start cost was 6 s (MR:270); resume_wall_s is the whole resumed call.

- claude-sonnet-5-5: PASS (first_model=claude-sonnet-5-5 resume_model=claude-sonnet-5-5 answer_has_word=yes resume_wall_s=6.2 resume_duration_ms=2997)
- claude-haiku-5-5: PASS (first_model=claude-haiku-5-5 resume_model=claude-haiku-5-5 answer_has_word=yes resume_wall_s=5.1 resume_duration_ms=2040)
- gpt-6-luna: PASS (first_model=gpt-6-luna resume_model=gpt-6-luna answer_has_word=yes resume_wall_s=5.2 resume_duration_ms=2339)
- muse-ember-1.0: PASS (first_model=muse-ember-1.0 resume_model=muse-ember-1.0 answer_has_word=yes resume_wall_s=5.8 resume_duration_ms=3038)

## REQ-S3 act rates: RECORDED (2026-11-13T21:09:27Z)

Command: `flock /tmp/collab-gateway.lock bash spikes/reqs3-act.sh` (NOFALLBACK=1). Transcripts: `spikes/out/reqs3/20261113T210646Z/`. Injection at main tool call 3 of a 6-command task; a trial counts only when the observed model matches and it made at least 3 tool calls. No pass threshold (R-47).

- claude-sonnet-5-5: act (next call runs the command) 5/5, ran it at any later call 5/5; finish (ended within one turn) 5/5
- claude-haiku-5-5: act (next call runs the command) 0/5, ran it at any later call 0/5; finish (ended within one turn) 0/5
- gpt-6-luna: act (next call runs the command) 1/5, ran it at any later call 1/5; finish (ended within one turn) 3/5
- 0/5 act rate on: claude-haiku-5-5  -> owner decision needed before that panel's F6 arm runs (not yet recorded).
- Check added by hand: haiku made one Bash call per turn in every trial (no parallel batch), and the injected probe text is present in its transcripts (for example 4 matches of `panel-probe` in `claude-haiku-5-5/act-1/session.jsonl`), so haiku saw the injection and did not act on it. Its finish trials ran all 6 commands after the finish text.

## Spike 4 sl2 (prefix s4pilot, A1 x2, A2 x1, packages TASK-WF-design-20261108-041415): PASS (2026-11-13T21:29:16Z)

Command: `ROW_PREFIX=s4pilot A1_RUNS=2 A2_RUNS=1 PKGS=TASK-WF-design-20261108-041415 bash spikes/spike4.sh sl2` (NOFALLBACK=1). Values written under `/tmp/collab-r5/config-pilot/values/sl2/`.

- s4pilot-a1-sl2-r1: launch exit 0
- s4pilot-a1-sl2-r2: launch exit 0
- s4pilot-a2-sl2-r1: launch exit 0
```
{"pkg": "TASK-WF-design-20261108-041415", "B_f_s": 176.91750000000002, "turn_p90_s": 26.552000045776367, "T_report_p90_s": 43.509000062942505, "k": 0, "budget_ok": false}
```

## Smoke test (DESIGN 6.4): FAIL (2026-11-13T23:51:16Z)

Rows `smoke-f6diag-sl2-1` and `smoke-a1-sl2-1` on `TASK-WF-design-20261108-041415`; checked by `spikes/smoke-check.sh`.

- FAIL 1 exits f6=1 a1=0; status f6=quarantined a1=complete
- FAIL 2 final model_ok and observed models: t1b-1= t3-1=gpt-6-luna t4-1=gpt-6-luna t1b-1=claude-sonnet-5-5 t3-1=gpt-6-luna t4-1=gpt-6-luna 
- FAIL 3 dropped_lines total=1; reviewer ids in each merge=2
- FAIL 4 f6 cards_delivered=1 snapshot_missing=0 hook_error=0 card_text_in_transcript_at=0 seal_t=1794613360334 validator=ok snapshot_sha_ok=true
- PASS 5 a1 board_dir=no settings_used=false f6_fields_null=true
- FAIL 6 smoke-f6diag-sl2-1: anon=ok score=parsed audit=quarantined; smoke-a1-sl2-1: anon=ok score=parsed audit=pass; 
- FAIL 7 f6 elapsed_s=266.372 B_f=176.91750000000002 hang_kill=true

## Smoke test reading, added by hand after the resume (2026-11-13, ~23:55Z)

The F6 smoke row of DESIGN 6.4 (`smoke-f6-sl2-1`) was refused by `launch.sh` with exit 3 before any model call, because the Spike 4 pilot gave k = 0 and `budget_ok` false for sonnet (`runs/smoke-f6-sl2-1/launch.json`). That refusal is the design's own run condition (DESIGN 5.1 step 5), not a harness fault. So the smoke test as written cannot pass on the pilot values; AC-5 is NOT MET.

To exercise the real-model card chain anyway, one diagnostic row ran with a scratch config (`/tmp/collab-r5/config-diag`, a copy of `config/` plus the pilot values file with `k` forced to 1 and `budget_ok` forced true; the sums were regenerated). Row `smoke-f6diag-sl2-1`, package TASK-WF-design-20261108-041415, command `flock /tmp/collab-gateway.lock env R5_CONFIG=/tmp/collab-r5/config-diag PANEL_COLLAB=1 bash bin/launch.sh sl2 smoke-f6diag-sl2-1 --pkgs TASK-WF-design-20261108-041415`. It is NOT a valid F6 measurement.

What the row showed (from `runs/smoke-f6diag-sl2-1/TASK-WF-design-20261108-041415/`):

- Both luna scouts finished (t4-1 about 124 s, t3-1 about 144 s after T0); the watcher posted one card, `items ["T5"]`, at 4 s before delivery; the validator accepted it; the sonnet receiver got it as `additionalContext` at its tool call 18 (`board/delivered/t1b-1.jsonl`); the sealed snapshot and its sha256 were written (`snapshot_sha_ok=true`); `hook_error = 0`, `hook_ms_p95 = 27`; the second scout exit produced `dup_card` (same Task set, not posted). Card keys and size pass the 2.2 rules; the card was posted and delivered before `finish_ms` (AC-9 holds on this board).
- The card text and the finish text are both in the real sonnet session transcript under `~/.claude/projects/-tmp-evalsb-collab-r5-TASK-WF-design-20261108-041415-repo/99c55825-d4e1-4806-bbda-ac6183d846d6.jsonl` (3 matches each). `smoke-check.sh` item 4 reports `card_text_in_transcript_at=0` only because the runner copies the session file after the attempt, and a hang-killed process leaves no result message and no session id, so no copy exists.
- The sonnet receiver then ran to the hang guard: finish text printed once at about 219 s, process killed at 266.4 s (1.5 x B_f = 265.4 s), `hang_kill: true`, `slo: SLO_BREACH`, no valid report (`model_ok` false), recorded INVALID in the merge, row `quarantined` (the audit's model check fails for t1b-1; the other audit checks pass). The A2 pilot row ended at 281.6 s, so sonnet with the catalogue kit takes about 280 s against 177 s for A1: this is the kit slowdown the pilot measured (0.59 against a limit of 0.34), seen again in a real F6 run.
- Smoke items on this row: 1 FAIL (exit 1, quarantined), 2 FAIL (t1b-1 killed), 3 FAIL (1 dropped line from the killed receiver, 2 reviewer ids in the merge), 4 partial (card delivered, snapshot ok, no hook error, validator ok; card text in the transcript only in the uncopied session file), 5 PASS (A1 row), 6 FAIL (audit quarantined; the A1 row passes), 7 FAIL (elapsed 266.4 s, hang kill). The A1 row `smoke-a1-sl2-1` passes every A1-side item (exit 0, complete, all three models ok, 0 dropped lines, 3 ids in the merge, no board, no `--settings`, F6 fields null, anon post-check 0, score parsed, audit pass, 180.3 s elapsed).
