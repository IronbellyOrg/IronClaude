# Merge log

Date 2026-11-14. Base A. Inputs read: the three variants, `diff-analysis.md`, `invariant-probe.md`, `tally-round2.md` and `.json`, `round2-A/B/C.md`, the seed brief and the enrichment file. Round 1 was not read. No product file was read or edited; all citations are the debate's own tags.

Merged (by tally winner, details in `refactor-plan.md`):
- A: layer table, event table shape, stages and narrow-only prefix, prefilter and self-timeout, nested pass 2, oversize block, tamper class, grant limits, message shape, log fields, names (`enforce-model-policy.sh`, `SC_MODEL_STAGE`, seed `.json.example`, `allow`).
- B: launcher helper with `build_flag` and the repo test, Agent resolution order and `/model` re-record, missing-policy block, residue classes, no Jev code, REQ method set, registration split, v2 room.
- C: role tiers, exact ids, single-assignment resolver, per-class modes, rollout order, one-file grants, typed `yes`, managed layer, timing test.

Dropped (rejected by the debate): closed-world scan, dormant or shadow Jev, allow on unknown session model, 200-line grant tail, manual 100/150 ms benchmark, allow on missing policy, allow on oversize script, fail-open without `jq`, glob `ids` on the allow side, inline non-human stage and `bindings`, `CLAUDECODE` guard, hash-chained journal and `audit`, `overrides-used.jsonl`, `claude-mention`, C's launcher spawn of the hook, B's README fix, status-table trailers.

Resolved by me, not by the tally:
1. Count: the tally header "own-variant picks" (A 22, B 14, C 11) counts votes for the own variant. Agreed winners are A 22, B 13, C 10, NONE 1, verdicts 4. Both are in `base-selection.md`.
2. C-025 (NONE): added L0 as a generator (`native-floor`, REQ-51) and L3 as `verify-run` (REQ-52), because C-001 (A) and all three advocates asked for REQs. L0 can only deny tiers no stage allows.
3. A-003 (QUALIFY, all three): mechanism for day-one enforcement is my `enforce_always` list (literal flag, Agent `model` parameter). Owner = owner of #546. Rollout durations (7 days, 100 events, 4 weeks) are mine and flagged in section 10.
4. Probe findings adopted without a debate vote (the probe was not debated): INV-001/012/038 (Agent order edge cases), 004 (unreadable policy means enforce), 005 (stage assignment in scripts), 008 (non-model subcommands exempt), 009 (pass 2 only on nesting constructs), 010, 013, 015, 016, 018, 021, 022, 023, 024, 025, 027, 028, 029, 030, 033, 035, 036 (`--fallback-model` only), 040 (as a verify item).
5. Probe findings left open or only noted: INV-002, 003 (only `lint --live`), 006, 031, 034 (cannot-see row plus L3), 037, 036 for `--agents`, 014 (Agent without model still allowed under a broken policy, stated as a ceiling).
6. X-009: followed the tally (B: block `/model` if the prompt event fires, re-record). A's basis text also said not to block a person's own choice; the vote was 3 to 0 for B.
7. X-004: kept A's second flat pass but limited it to nesting constructs and put it in class `bash_script` (no sixth class), because the A advocate agreed a plain mention must pass.
8. X-005: command cap applies to launch-shaped commands only; oversize scripts are decided by a streaming grep. This refines A so large legitimate scripts and heredocs are not blocked.
9. X-003: C's "tier table from the highest layer" changed to "managed, else user"; a project file can only tighten (probe INV-021).
10. C-005: added a `fable` role with empty ids (C conceded it was missing). `claude-gw-tier3` stays unlisted and denied.
11. Policy fields `table_date`, `observed_ok`, `SC_MODEL_POLICY_MANAGED` (test path override) are new here. The one `observed_ok` entry comes from probe INV-034.
12. Timeouts: 3 s registration with internal limit minus 1 s (B's split, probe INV-015); A's 5 s dropped. SessionStart 3 s.
13. Rule ids: A's descriptive names; the tally did not vote on ids.
14. Workflow added to the matcher (B's unique item U-011) with REQ-63; its input shape is UNVERIFIED.

Limits of this merge:
- `merged-output.md` is 8,873 words by `wc`, which counts table pipes and JSON; roughly 8,100 words of prose. That is above the 8,000 target and was not trimmed further.
- Docs facts B1 to B9 were not re-read. Lines marked verified are the advocates' or Step 1's reads.
- REQ list: 63 requirements, numbered 01 to 63 with no gap or duplicate (checked by search), each with a bracketed method.
- Nothing was staged, committed or pushed. Nothing outside the work dir was written. `.dev/eval-workspaces/` was not touched.
