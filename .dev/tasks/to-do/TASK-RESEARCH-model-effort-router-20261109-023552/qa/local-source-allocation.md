# Local source allocation manifest v2 (qa/local-source-allocation.md)

Supersedes v1 (preserved in git history of this staged file). Corrections driven by the four independent allocation-check FAILs (2.1: B1-B3 + M1-M4; 2.2: B1-B4; 2.4: B1-B4 + N1-N3; 2.5: B1-B2 + N1-N4; reports at `qa/input-allocation/{2.1,2.2,2.4,2.5}/check-1.md`; 2.3's first check launch-failed on a missing node binary, retried after this correction). Revision: worktree HEAD 933cf3a4f, corpus unchanged (`git status` clean for src/tests).

## Measured corpus (unchanged from v1)

18 files, 16,719 lines: F01 ccsession 1975; F02 ccsession-orca 249; F03 session-start.sh 47; F04 session-name.sh 217; F05 models.py 1111; F06 ccsession-models.json 173; F07 ccsession.env.example 31; F08 README.md 772; F09 MODEL-TIERS.md 216; F10 local-gateway-alias-proxy.py 906; F11 install.sh 172; F12 install_ccsession.py 133; F13 main.py 569; F14 test_ccsession_tiers.py 3399; F15 test_ccsession_tag.py 4823; F16 test_install_ccsession.py 323; F17 test_cli_install.py 1106; F18 test_update_command.py 409.

## Function-boundary facts (newly measured for v2)

- F01: pre-parse `case` 684-727; option loop 730-821 (`--claude-args` 749, `--model` 798, loop `done` 821); `session_place` 1358-1406; `shim_listener_pid` 922-935; `shim_health_status` 936-961; `setup_shim` 962-1155; `apply_tier_selection` 1191+; tier call sites at 1079/1132/1254/1755/1838; private-profile markers at 116/881/1833; resume at 1298/1964-1966.
- F05: `user_access` 527-627; `tier_access` 628; `resolve_tiers` 645; `_all_tiers` 655; `compact_settings` 681; `_settings_key` 748-779; `settings_digest` 780-784; `code_digest` 785-800; `shim_port` 801-821; `shim_upstream_problem` 822+.
- F10: `audit` 141; `switch_reason` 393-403; `retry_after_seconds` 404-418; `cool_down` 419-425; `cooling_until` 426; `clock` 432; `plain_body` 436-451; `with_note` 452-479; `_FirstByteResponse` 480-503; `Handler` 504+ (do_GET 535, do_POST 569, _post 572, _proxy 646, _open_upstream 674, _forward_tier 723, _stream 841).
- F13: `install` 46-303; `mcp` 304-339; `update` 340-569.
- F14 boundary tests: 645, 845, 865 (picker section starts 654); `_real_launch` helper 1687-1733; 1734; 2538; 2553; 1018 (`test_no_backup...` 1018-1031); cooldown tests 1057/1072/1082/1091; injected-clock test 1151-1174.
- F15 boundary tests: 833, 848, 882; 1467 (`test_every_launch_restores_grep_and_glob`); 2526, 2552; 3389, 3414; 4217, 4258; 3445, 3456, 3474.
- F18: `native_install` 183-193; `test_real_install_launches_ccsession` 194-222; `test_real_update_restores_packaged_ccsession` 223-409.

## Shared context, measured and charged per slice

- Procedure passage (TASK 140-161): 22 lines — charged to every slice.
- Dispatch brief: measured per topic at dispatch (the brief file itself is read by the worker); counted in budgets below as the actual `wc -l` of the emitted concrete source item text, estimated ≤70.
- Scope digests: scope-01 138, scope-02 142, scope-03 92, scope-04 107, research-notes 112. The full Codebase Research Agent Prompt (from the topic's producer spec) is copied into each slice item; its ~180 lines are charged (measured as the TASK producer-spec span each worker must hold).
- rf-task-researcher role: `.claude/agents/rf-task-researcher.md` pinned passage (role preamble + output format, ~80 lines of its 564) — charged.
- `qa/input-bindings.md` (32) — charged where the item's selection rule applies.
- Governing research template skeleton (~40 lines of the tech-research output format) — charged.

Baseline per-slice fixed context (procedure 22 + brief 70 + prompt 180 + role 80 + bindings 32 + template 40) = 424 lines. Every slice below therefore carries at most 576 source/context lines; where a slice trims role/template to a jointly-measured 100-line quoted excerpt (both are quoted in the brief, not full passages), fixed context is 344.

## Topic 2.1 launcher/caller flow (5 slices, outputs `research/source-slices/2.1/slice-{1..5}.md`)

Files: F01 1975, F02 249, F03 47, F04 217. Context rows: scope-01, scope-02, research-notes (quoted digest rows in briefs, 30-40 lines each, charged).

- **2.1-slice-1**: F01 1-560 (560) + scope-01 rows 40 + fixed 344 = 944. Aspect: usage/prologue/helpers/pre-parse `case` 684-727 ENTRY EDGE (the case lies at the range's tail; the option loop 730 it dispatches into is slice-2's — cite, don't re-derive). Covers private-profile marker 116.
- **2.1-slice-2**: F01 561-1155 (595) + scope-02 rows 40 + fixed 344 = 979. Aspect: option loop 730-821 (`--claude-args` 749 passthrough, `--model` 798, duplicate model/settings options), profile application, `setup_shim` 962-1155 WHOLE, permissions markers 881, tier call sites 1079/1132. ENTRY EDGE: pre-parse case from slice-1.
- **2.1-slice-3**: F01 1156-1400 (245) + research-notes rows 40 + fixed 344 = 629. Aspect: `apply_profile`/`apply_tier_selection` (1191+) /`export_selection` 1157-1281 WHOLE, `session_place` 1358-1406 straddle — 1358-1400 here, 1401-1406 in slice-4, declared shared edge, cross-cite; selection-state set (PROFILE_MODEL 1175/1226, CC_SETTINGS_ARGS 1150-1259 shared with slice-2, declared edge); tier call site 1254. SHARED EDGE rule: slices 2↔3 cross-cite the 1150 shim-settings span; slice-3 owns apply_* bodies.
- **2.1-slice-4**: F01 1401-1975 (575) + research-notes rows 40 + fixed 344 = 959. Aspect: tail exec sites (all six, 1904-1973), resume 1298(comment)/1964-1966, private-profile 1833, tier call sites 1755/1838, session_place tail 1401-1406. ENTRY EDGE: consumes slice-3's selection state as attributed counterpart.
- **2.1-slice-5**: F02 whole (249) + F03 whole (47) + F04 whole (217) + scope-03 rows 30 + fixed 344 = 887. Aspect: Orca wrapper and both session lifecycle hooks; cross-cites F01 exec sites (slice-4) as counterpart.

Coverage: F01 = 560+595+245+575 = 1975 ✓. F02/F03/F04 whole ✓. Obligation map: parser → slice-1 case + slice-2 loop; apply_profile/apply_tier_selection/export_selection → slice-3; setup_shim → slice-2; six exec sites → slice-4; permissions → slices 2/4; private-profile → slices 1/2/4; passthrough --claude-args → slice-2; duplicate options → slice-2; resume → slice-4; immediate callers → slices 3/4; wrapper/hooks → slice-5. ✓

## Topic 2.2 defaults/policy (5 slices, outputs `research/source-slices/2.2/slice-{1..5}.md`)

- **2.2-slice-1**: F05 1-526 (526) + scope-04 rows 40 + fixed 344 = 910. Aspect: defaults parser (defaults_path 325, read_defaults_file 381), tier_env 459, tier_mode 474, _window 487, tier_number 494, owner_name 504, owner_roles 514; registry schema validation (182-198).
- **2.2-slice-2**: F05 527-747 (221) + F06 whole (173) + F07 whole (31) + scope-01 rows 30 = 455 + fixed 344 = 799. Aspect: `user_access` 527-627 WHOLE (username/first-role/wildcard matching — v1's 560/561 mid-body cut eliminated), tier_access 628, unavailable 635, resolve_tiers 645, _all_tiers 655, compact_settings 681, windows/settings/compaction.
- **2.2-slice-3**: F05 748-1111 (364) + scope-02 rows 30 = 394 + fixed 344 = 738. Aspect: `_settings_key` 748-779, settings_digest 780, code_digest 785 (cache/fingerprint), shim_port 801, shim_upstream_problem 822, cache/version. BOUNDARY: 747/748 def edge ✓.
- **2.2-slice-4**: F01 1079-1160 (82) + F01 1191-1300 (110) + F01 1750-1850 (101) + research-notes rows 40 = 333 + fixed 344 = 677. Aspect: selection callers — tier call sites 1079/1132, apply_tier_selection entry 1191-1300 (ANTHROPIC_MODEL default logic 1201-1205, issue 462 Coder-role default), call sites 1755/1838, private-profile 1833. All F01 reads COUNTERPART (2.1 owns F01 full coverage). Exclusion evidence for 1161-1190: setup_shim tail owned by 2.1-slice-2 (declared edge).
- **2.2-slice-5**: F08 430-703 (274) + F09 whole (216) + scope-04 rows 30 = 520 + fixed 344 = 864. Aspect: documentation — README tier/profile sections 430-703 (v1's wrong 1-120 replaced; exclusion evidence: 1-429 is install/gateway setup, grep shows only line 23 tier mention in 1-120), MODEL-TIERS.md whole. F08 COUNTERPART owner is this slice (only topic assigning F08; relevant-range justification recorded).

Coverage: F05 = 526+221+364 = 1111 ✓ (def-edge boundaries 526/527, 747/748). F06/F07/F09 whole ✓. Obligation map: defaults parser → slice-1; identity/access + username/first-role/wildcard → slice-2; default-tier/model resolution + allowed aliases → slices 1/2; windows/settings/compaction → slice-2; registry schema → slice-1 (+F06 in slice-2); cache/fingerprint → slice-3; Coder template evidence → slice-4 (callers) + slice-5 (docs); selection callers → slice-4; relevant documentation → slice-5. ✓

## Topic 2.3 proxy request fidelity (5 slices, outputs `research/source-slices/2.3/slice-{1..5}.md`)

- **2.3-slice-1**: F10 1-451 (451) + scope-03 rows 40 + fixed 344 = 835. Aspect: module head/config/env, `_cooldowns` 94, audit 141, main/startup, `switch_reason` 393, `retry_after_seconds` 404, `cool_down` 419, `cooling_until` 426, `clock` 432, `plain_body` 436-451 WHOLE (boundary at 451 = def edge before `with_note` 452; v1's 460 mid-body cut eliminated).
- **2.3-slice-2**: F10 452-673 (222) + scope-04 rows 30 = 252 + fixed 344 = 596. Aspect: `with_note` 452-479 WHOLE, `_FirstByteResponse` 480-503, Handler do_GET 535/do_POST 569/_post 572/_proxy 646 (malformed/non-object JSON, Content-Length, headers, method/query paths), boundary 673/674 def edge before `_open_upstream`.
- **2.3-slice-3**: F10 674-906 (233) + F05 counterpart 748-830 (83: _settings_key/settings_digest/code_digest/shim_port — whole functions, v1's mid-function 771 start fixed) + scope-03 rows 20 = 336 + fixed 344 = 680. Aspect: `_open_upstream` 674, `_forward_tier` 723 (aliases/tier/literal suffix/model rewriting, effort/thinking/tool fields), `_stream` 841 (response fidelity), module tail; gateway translator source location question recorded (negative search if absent).
- **2.3-slice-4**: F14 654-864 (211: picker/failover section through test 845-864 WHOLE) + F14 1018-1031 (14: test_no_backup WHOLE) + research-notes rows 30 = 255 + fixed 344 = 599. Aspect: proxy request fixtures — picker/show-all/env-window tests. COUNTERPART (2.5 owns F14 full coverage).
- **2.3-slice-5**: F15 882-1150 (269: test_shim_curates_models_and_preserves_wire_aliases 882 WHOLE through packaged-skill-installer test ending 1150) + F14 1215-1230 (16: effort settings) + F14 1414-1553 (140: no-time-limit 1414, non-streamed 1429, small-streamed 1481 — whole tests, ends before test_lowercase 1554) + F14 2296-2352 (57: note-on-plain-text 2296-2302, exhausted-tier 2303-2320 WHOLE) + scope-04 rows 20 = 502 + fixed 344 = 846. Aspect: wire-alias/curation fixtures, effort-field fixture, stream-fidelity fixtures, error-note fixtures. COUNTERPART.

Coverage: F10 = 451+222+233 = 906 ✓ (def-edge boundaries). Obligation map: _post/_proxy → slice-2; _open_upstream/_forward_tier/_stream → slice-3; malformed JSON/Content-Length/headers/method → slice-2; alias/tier/suffix/model rewriting → slice-3; effort/thinking/tools → slice-3 (source) + slice-5 (fixtures); response fidelity → slice-3 + slice-5; backend evidence → slices 2/3; translator location → slice-3. ✓

## Topic 2.4 fallback/replay/state (5 slices, outputs `research/source-slices/2.4/slice-{1..5}.md`)

- **2.4-slice-1**: F10 1-451 (451) + scope-03 rows 40 + fixed 344 = 835. Aspect (architecture lens): cooldown/switch machinery — `_cooldowns` 94, `switch_reason` 393, `retry_after_seconds` 404 (Retry-After), `cool_down` 419, `cooling_until` 426, `clock` 432, `plain_body` 436-451 WHOLE.
- **2.4-slice-2**: F10 452-906 (455) + scope-02 rows 30 = 485 + fixed 344 = 829. Aspect: `with_note` 452-479 WHOLE (error-body; v1's 460 mid-body cut fixed), `_FirstByteResponse` 480 (first-byte vs connect failure), Handler failover path (health 543, audit 598, _open_upstream wait, _forward_tier switch, _stream 841 no-retry-after-stream-start, truncation/context/overload500 handling).
- **2.4-slice-3**: F01 922-1155 (234: `shim_listener_pid` 922-935, `shim_health_status` 936-961 — v1 missed these — and `setup_shim` 962-1155) + F05 748-830 (83: fingerprint functions whole) + scope-03 rows 20 = 337 + fixed 344 = 681. Aspect: shim identity/health/audit setup, helper fingerprinting. COUNTERPART for F01/F05 (owners 2.1/2.2).
- **2.4-slice-4**: F14 1018-1180 (163: test_no_backup 1018-1031, all-models-out 1032, cooldown 1057/1072, no-reply-timeout 1082, unreachable 1091, named-no-failover 1101, changed-env 1109, long-pause 1119, failure-after-reply 1129, connect-timeout 1138, injected-clock 1151-1174 WHOLE) + F14 1414-1553 (140, DECLARED OVERLAP with 2.3-slice-5: first-byte/stream-no-retry whole tests) + research-notes rows 30 = 333 + fixed 344 = 677. Aspect: fallback/cooldown/first-byte tests. COUNTERPART.
- **2.4-slice-5**: F15 1441-1483 (43: label-with-transcript resume 1441-1448, grep/glob restore 1467-1483 WHOLE) + F15 3445-3486 (42: autostart-off 3445-3455, name-list-unwritable 3456-3473, auto-named-listed 3474-3486 — whole tests; v1's 3306-3460 imprecise range replaced) + scope-02 rows 20 = 105 + fixed 344 = 449. Aspect: session replay/state — resume-with-transcript, launch-restore, untagged/state edge tests. Exclusion evidence (v1 N1 fixed): F15 3136-3305 is orca naming/tab tests owned by 2.5 full coverage; "replay" has 0 grep hits in F10 (source-backed negative recorded); replay semantics live in F15 1441-1448 and F14 stream tests (slice-4). COUNTERPART.

Coverage: F10 = 451+455 = 906 ✓. Obligation map: switch_reason → slice-1; cooldown/Retry-After → slices 1 (source) + 4 (tests); _FirstByteResponse → slice-2; first-byte vs connect → slices 2/4; error-body/truncation/context → slice-2; no-retry-after-stream-start → slices 2/4; health/fingerprint/audit → slices 2/3; backend-evidence limits → slice-2; replay → slice-5 (+ negatives); process-local vs session state → slices 1 (`_cooldowns` module-level) / 5 (session files); launch isolation → slice-3. ✓

## Topic 2.5 tests/packaging/callers (22 slices, outputs `research/source-slices/2.5/slice-{0..21}.md`)

Fixed context per slice 344 (role/template as measured excerpts) + caller table 40 (from slice-0).

- **2.5-slice-0 (context/caller-discovery)**: scope-01 (138) + scope-02 (142) + scope-03 (92) + scope-04 (107) + research-notes (112) = 591 whole + fixed (trimmed role/template 100 + 224) = 915. Aspect: whole-context digest for 2.5 + bounded caller discovery (grep `wire_ccsession|install_ccsession` across src/, pinned; F13 entry points 46/304/340; discovered callers recorded ≤30 lines). Output `research/source-slices/2.5/slice-0-context-callers.md`. Downstream slices receive its caller table instead of raw scope files.
- **2.5-slice-1**: F14 1-560 (560) + caller table 40 + fixed 344 = 944.
- **2.5-slice-2**: F14 561-1160 (600) + caller table 40 + fixed 344 = 984.
- **2.5-slice-3**: F14 1161-1686 (526) + caller table 40 + fixed 344 = 910.
- **2.5-slice-4**: F14 1687-2257 (571: `_real_launch` 1687-1733 WHOLE through test ending 2257) + caller table 40 + fixed 344 = 955.
- **2.5-slice-5**: F14 2258-2552 (295: through test 2538-2552 WHOLE) + caller table 40 + fixed 344 = 679.
- **2.5-slice-6**: F14 2553-3050 (498) + caller table 40 + fixed 344 = 882.
- **2.5-slice-7**: F14 3051-3399 (349) + caller table 40 + fixed 344 = 733.
- **2.5-slice-8**: F15 1-560 (560) + caller table 40 + fixed 344 = 944.
- **2.5-slice-9**: F15 561-1100 (540) + caller table 40 + fixed 344 = 924.
- **2.5-slice-10**: F15 1101-1560 (460) + F16 161-323 (163) = 623 + scope rows 20 + fixed 344 = 987.
- **2.5-slice-11**: F15 1561-2120 (560) + caller table 40 + fixed 344 = 944.
- **2.5-slice-12**: F15 2121-2680 (560) + caller table 40 + fixed 344 = 944.
- **2.5-slice-13**: F15 2681-3240 (560) + caller table 40 + fixed 344 = 944.
- **2.5-slice-14**: F15 3241-3800 (560) + caller table 40 + fixed 344 = 944.
- **2.5-slice-15**: F15 3801-4360 (560) + caller table 40 + fixed 344 = 944.
- **2.5-slice-16**: F15 4361-4823 (463) + caller table 40 + fixed 344 = 847.
- **2.5-slice-17**: F17 1-560 (560) + caller table 40 + fixed 344 = 944.
- **2.5-slice-18**: F17 561-1106 (546) + caller table 40 + fixed 344 = 930.
- **2.5-slice-19**: F18 whole (409) + F16 1-160 (160) + caller table 20 + fixed 344 = 933.
- **2.5-slice-20**: F12 whole (133) + F11 whole (172) + F13 1-303 (303: module head + `install` 46-303 WHOLE) = 608 + caller table 40 + fixed 344 = 992.
- **2.5-slice-21**: F13 304-569 (266: `mcp` 304-339, `update` 340-569 with wire call sites 352/388) + research-notes rows 40 + fixed 344 = 650.

Coverage: F14 = 560+600+526+571+295+498+349 = 3399 ✓ (boundaries at whole-test/helper edges: 560/561 within usage→section, 1686/1687 helper edge, 2257/2258, 2552/2553 test edge, 3050/3051). F15 = 560+540+460+560+560+560+560+560+560+463 = 4823 ✓. F16 = 160+163 = 323 ✓. F17 = 560+546 = 1106 ✓. F18 whole ✓ (slice-19). F12/F11 whole ✓ (slice-20). F13 = 303+266 = 569 ✓ (46-303 install whole; 1-45 module head in slice-20's range 1-303 ✓). Aspect note per slice: the brief carries the aspect (which test families the range holds: explicit model/tier, inherited/role/default, non-tier/profile, effort/settings, context/windows/compaction, permissions, stream/tools/history, fallback, installation/package) so obligations map; discovered callers → slice-0 + slice-21 call-site spans. ✓

## Per-slice aspect obligations (all topics)

Every producer-spec obligation keyword maps to exactly one named slice aspect per topic (inline above); none unmapped. Whole-function and whole-test boundaries throughout. Declared shared/counterpart edges: 2.1 slices 2↔3 (selection state, 1150 span), 3↔4 (exec sites), 2.2 slice-2↔3 (747/748 def edge), 2.3-slice-5 ↔ 2.4-slice-4 (F14 1414-1553 declared overlap, whole tests), 2.2-slice-4 ↔ 2.1 (F01 counterpart), 2.5 owns all five test files' full coverage.

## Registration

Pending outputs registered in `qa/input-bindings.md` at dispatch: slice outputs under exact consumer IDs (`2.1-source-1..5`, `2.2-source-1..5`, `2.3-source-1..5`, `2.4-source-1..5`, `2.5-source-0..21`), coverage checks under `2.x-coverage-N`, dependent consumers 1.3, 1.4, 1.5, 1.6, canonical 2.1-2.5, Phase-3+ IDs. Acceptance only on independent PASS.
