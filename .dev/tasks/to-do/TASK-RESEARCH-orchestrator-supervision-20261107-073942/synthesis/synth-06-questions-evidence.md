# Synthesis 06: Open Questions and Evidence Trail

**Research question context:** Phase 1 is a read-only, coordinator-only `/sc:sweep`. It classifies each session as waiting on a person, working, stalled (proved), could not determine, finished or idle (the research question's six; Section C adds fenced as a seventh class, `research/research-notes.md:188`, and six versus seven is row 98a below), and treats safe-to-close as a separate dimension. A default 6 h window bounds activity only. The sweep writes a dated static report on the #409 layout and adds a WC-14 rule to `src/superclaude/core/WORKER-CONTRACT.md`. `/sc:close`, resume, the trust layer, an orchestrator of orchestrators and the management-server relay are later phases and are only recorded here.

**Inputs:**
- `gaps-and-questions.md` (GQ-01 to GQ-100, sections (b) K1-K4, (c) AMBIGUITIES, (d) C1-C15, (e) per-file UNVERIFIED / CODE-CONTRADICTED claims, (f) stale docs S-01 to S-14)
- `research/research-notes.md`, `research/scope-01-contract.md`, `research/scope-02-orca-recovery.md`, `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`, `research/05-orca-row-schema.md`, `research/06-orca-open-questions.md`, `research/07-gate-gap-fill.md`
- `research/web-01-agent-supervisor-session-health.md`, `research/web-02-static-status-report-conventions.md` (external)
- `qa/qa-nb4-fix-log.md`

**NB-4 fix in effect:** GQ-03 (NB-4, the default argv allowlist) is resolved by the fix pass in `qa/qa-nb4-fix-log.md` (2026-11-07). It was a coordinator-approved exception at the Phase 3 research gate. The `scope-03:99` allowlist now includes `orchestration task-list` (`--ready`, `--run <id>`), `run-list`, `run-current` and `gate-list`; `inbox` stays forbidden.

**Gaps-file counts:** 75 open rows, 25 resolved (`gaps-and-questions.md:125`).

**Evidence labels:** [CODE-VERIFIED], [CODE-CONTRADICTED] (CC), [UNVERIFIED] (UV), [STALE DOC], [EXTERNAL] (web sources). Option A4 (extend sc-crash-recovery) is [CODE-CONTRADICTED] and appears below only as a rejected option.

---

## 9. Open Questions

Issues that need resolving before or during implementation.

### 9.1 Open gaps-file rows (GQ IDs)

Every open GQ row is cited. Rows that share one resolution are grouped.

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| 1 | GQ-01 (G-A, C10): what is the full `worker-list --run <id> --json` row schema? | Critical. The classifier cannot rely on list fields it has never seen. | Use the fallback of one `worker-show` per row (worst case ceil(N/100) list calls plus N show calls). Close only with a live `worker-list --run <id> --json` capture. |
| 2 | GQ-02 (G-B, C11): there is no non-consuming read of pending questions. | Critical. "Waiting on a person" may be missed. | Use the contract fallbacks (`blocked_question`, non-null `agentWait`, frozen plan). The report header says "Messages coverage: partial". |
| 3 | GQ-04 (G1): how does WC-14 state "keep polling"? | Critical. This is the coordinator duty the rule must carry. | Cite the memory note `coordinator-never-stop-polling.md` (owner order 2026-11-05, N-30) in WC-14. |
| 4 | GQ-05 (G2): how is the wait re-armed after an expiry? | WC-14 wording. | State re-arm after every expiry in WC-14. |
| 5 | GQ-06 (G3): the periodic sweep itself. | Critical. It is the feature. | Build `/sc:sweep` in Phase 1 as scoped. |
| 6 | GQ-08 (G5): when does the coordinator tell the person? | WC-14 wording. | Define the trigger in WC-14. |
| 7 | GQ-09 (G6, AMB 8): are person-started sessions in scope? | Scope of the "idle" class. | Owner decision. Idle applies only to person-started sessions. |
| 8 | GQ-10 (G7, AMB 3): where does the report go? | Output path. | Owner decision. |
| 9 | GQ-11 (AMB 4): how does WC-14 relate to WC-1? | Possible contract conflict. | Owner decision; word WC-14 so it does not override WC-1. |
| 10 | GQ-12: the never-as-worker list and its tests. N-34: the "all_seven" test checks 8 entries. | A test name and its count disagree; adding `/sc:sweep` touches this test. | Read the test before editing and update the list and the test together. |
| 11 | GQ-14 [UNVERIFIED]: is the `/sc:help` and HOW-WE-WORK registration test-enforced? | A missed registry fails CI. | Read `tests/commands/test_help_command.py` in full before implementation. |
| 12 | GQ-15: what values can `liveness.reason` take? | Classifier inputs. | Capture live rows; treat unknown values as "could not determine". |
| 13 | GQ-16: what shape does `runtime_unavailable` have? | Error handling. | Capture the error once; copy it verbatim into the report. |
| 14 | GQ-17: how do heartbeat age and liveness relate? | Stall proof. | Never classify a stale heartbeat alone as stalled. |
| 15 | GQ-19 (K2): fix `bootstrap_scan.sh` or write a new scanner? Bugs at `:31` (encoding), `:73` (`.git` file), `:136` (JSON escaping). | Reuse choice. | Write the scan in the new CLI module. A4 (extend sc-crash-recovery) is rejected as [CODE-CONTRADICTED]. |
| 16 | GQ-21 (C3): exclude `git stash *` and `ccsession --list`. | Read-only guarantee. | Keep both out of the sweep. Read `topics/*.txt` directly instead of `ccsession --list` (it migrates names, `scope-02:165`). |
| 17 | GQ-22: what does `--include-remote` cost? | Runtime bound. | Keep `--include-remote` in the default `worker-list` argv (synth-05 step 1.4), because remote rows read `unverifiable` without it (`05:163`). Measure its cost once with one run using the flag; GQ-22 stays open until then. |
| 18 | GQ-23 (K4): lazy or eager `__init__`? `recommend` `__init__.py:12-20` versus `reflect` `:17-30`. | Package layout. | Pick one precedent and follow it. |
| 19 | GQ-24: "Other commands" table versus the excluded set (`test_how_we_work_routing_table.py:299-309`, N-37). | Registry test. | Add `sc:sweep` to `_OTHER_COMMANDS` and the table together. |
| 20 | GQ-25 (K3): pipx PATH form. | The command may not be found. | Bare `superclaude sweep` first, `uv run` fallback. Run `superclaude sweep --help` once outside a uv project. |
| 21 | GQ-26: how do `allowed-tools` patterns combine? | Permission surface. | Pin both `Bash(superclaude sweep:*)` and `Bash(uv run superclaude sweep:*)`; verify on first run. |
| 22 | GQ-27: where does the probe module live? | Testability. | Use an `_orca(*args)` seam, after `reflect/config.py:64-78`. |
| 23 | GQ-28: is the UTILITIES table in `docs/user-guide/commands.md` pinned by a test? | Docs drift. | Add the row; enforcement is [UNVERIFIED] (`scope-03:140`). |
| 24 | GQ-29 (C6): #409 sort tie-break. | Report order. | Choose a deterministic tie-break and state it in the report. |
| 25 | GQ-30: closure evidence in the report. | Safe-to-close dimension. | Record the evidence per row. |
| 26 | GQ-31: per-source coverage line. | Honest reporting. | Print coverage per source in the header. |
| 27 | GQ-32: scope line. | Report header. | Print the worktree-tree root path as the scope line (`scope-04:360`; synth-05 step 1.5). Plan decision, open (`gaps:55`). |
| 28 | GQ-33 (C7): omission bound. | Truncation honesty. | List everything, so `<shown>/<total>` has shown equal to total; a source cut at 100 rows prints "at least 100 (truncated at 100), total could not determine" (`scope-04:361`; synth-05 step 1.5). Plan decision, open (`gaps:56`). |
| 29 | GQ-34 [UNVERIFIED]: Approval label and the `gate-list` mapping. | Approval column. | `gate-list` is now allowed (NB-4); the mapping stays [UNVERIFIED] until a live gate is captured. |
| 30 | GQ-35: pin the layout to `495eb96d` (unmerged). | Layout drift. | Owner decision (AMB 9). |
| 31 | GQ-36: shape of a non-null `agentWait`. | Waiting-on-a-person proof. | Capture a live waiting row. |
| 32 | GQ-37: `unverifiable` and `exited` never captured. | Important. Two liveness states are unseen. | Capture a live stalled row. |
| 33 | GQ-38: worker-list `page.hasMore` past 100 rows (proven only for an empty page). | Paging. | Page on `page.nextCursor` and pass `--run` (synth-05 step 1.4; `05:163`). |
| 33a | GQ-48: non-consuming message enumeration past 100 rows (`--all` and Run `--peek` cap at 100 with no cursor). | Truncation. | Report "at least 100 (truncated at 100), total could not determine" (synth-05 step 1.5). |
| 34 | GQ-39: `counts` keys. | Header totals. | Capture once; do not depend on unknown keys. |
| 35 | GQ-40 (C15): nested workers. The sweep-side rule is settled. | WC-13. | Report a non-null `parent` as a WC-13 violation. Row stays open for the Orca side. |
| 36 | GQ-41: CLI version of the research captures not recorded (captures predate 1.4.245). | Evidence age. | Stays open [UNVERIFIED]. No report header field is promised, because no verified read-only version source exists (`gaps-and-questions.md:82`). |
| 37 | GQ-43: does plain `check` mark messages read? | Read-only guarantee. | Treat it as draining; forbidden. |
| 38 | GQ-44: `--peek` / `--all` side effects. | Read-only guarantee. | Not used until proved. |
| 39 | GQ-46: inbox read-marking. | Read-only guarantee. | `inbox` stays forbidden (NB-4 fix log). |
| 40 | GQ-47: `reply` effects. | Out of scope for a read-only sweep. | Forbidden. |
| 41 | GQ-49 / GQ-50: `ask --dispatch-capability` and peer `ask --to run:<id>`. | Later phases. | Record only; not used in Phase 1. |
| 42 | GQ-51: side effects of the `--agent-wait` probe. | Read-only guarantee. | Excluded. |
| 43 | GQ-52: `agentWait` during `ask`. | Waiting proof. | Capture live. |
| 44 | GQ-53: there is no `caller` in `status --json`. | Coordinator identity. | Do not rely on it. |
| 45 | GQ-54: cross-host joins. | Remote sessions. | Report as "could not determine". |
| 46 | GQ-56: `check --all` and `run:<id>` rows; which end the 100-row cap keeps. | Truncation. | Not used; capture if needed later. |
| 47 | GQ-57: `legacyCompatibility.ackMessageIds` / `compatibilityAck`. | Hidden acknowledgement. | Read the runtime handler under `out/main/chunks/` or run a throwaway-Run test. |
| 48 | GQ-58: null `agentWait`, help text versus guide. | Classifier rule. | Null = no wait observed; absent = could not determine. |
| 49 | GQ-59: runtime-version or `legacyCompatibility` probe before trusting `--peek`. | Read-only guarantee for any later `check`. | No version probe in Phase 1: no read-only verb that reports the runtime version was found (`gaps-and-questions.md:82`). The default stays contracts-only and `check --peek` stays gated (synth-05 8.1, gaps sent to Open Questions). GQ-59 stays open until a runtime-handler read or a throwaway-Run probe settles it. |
| 50 | GQ-60 (AMB 1): where does the logic live? | Architecture. | Leaning A1 (CLI `superclaude sweep` plus a thin skill). A4 rejected as [CODE-CONTRADICTED]: `git stash *` in allowed-tools, `~/workspace` path, bootstrap bugs. |
| 51 | GQ-61 (AMB 2): 6 h or 72 h window? | Default scope. | Owner decision (AMBIGUITY 2). 6 h is the working default; the window bounds activity only (N-41). |
| 52 | GQ-62 (AMB 5): sequencing with PR #422. | Merge conflicts. | Owner decision. |
| 53 | GQ-63 (AMB 6): pragmatic DONE/NEXT "No exceptions" (`pragmatic.md:22`, `:53`). | Report format conflict. | Owner decision. |
| 54 | GQ-64: does `identify` write? | Read-only guarantee. | Not used until proved. |
| 55 | GQ-65: `task-list` / `gate-list` row caps. | Truncation. | Apply the omission rule. |
| 56 | GQ-66 (AMB 10): what is the "management server"? | Later phase. | Record only. |
| 57 | GQ-67 (AMB 11): worktree-first or trigger-based placement? CR-01 unread. | Placement rule. | Read CR-01; owner decision. |
| 58 | GQ-84: fenced exclusion when the transcript is unreadable. | Class precedence. | Rule 2 needs the transcript read: exited, no `worker_done` and an unreadable transcript give could not determine (as synth-05 step 1.3 and `gaps-and-questions.md:107`). Not a WC-10 break. |
| 59 | GQ-85: mixed verb forms at `scope-03:99`. | Wording. | Use the `orca-ide orchestration <verb>` form (C13). |
| 60 | GQ-86 to GQ-95: wording residuals (`--unread` versus `--unread --peek`; `scope-01:64` calls safe-to-close a "class"; `06:57-58` tags help text CODE-VERIFIED; `06:187` stale summary; `filterLegacyPeekResult` on every peek; `scope-04:290`, `:320`; "needs a human"; `research-notes:175`, `:196` say G-A for G-B; `research-notes:241-242` say "MISSING"; a conservative default phrased as fact). | Low. Wording only. | Correct the wording in the final report; do not carry it into the plan. |
| 61 | GQ-97: citation residuals. | Low. | Re-cite at the Phase 5 synthesis gate. |
| 62 | GQ-98: `--retry-of` versus WC-6. | Contract wording. | Check WC-6 before WC-14 cites `--retry-of`. |
| 63 | GQ-99: N `worker-show` calls versus the batching policy. | Runtime cost. | Batch where the policy allows. |
| 64 | GQ-100: APPROVED.md D1-D5 and the ccsession-tag README not verified. | Unread decisions. | Read both before implementation. |

### 9.2 [UNVERIFIED] and [CODE-CONTRADICTED] claims with no GQ row (gaps-file section (e))

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| 65 | `scope-01:118`: is `test_help_command.py` coverage wider than the marker asserts (`:32-33`, `:41`)? | Registry test. | Read the file in full (same as GQ-14). |
| 66 | `scope-01:128`: the memory claim about peer sessions (F2) is UNVERIFIED. | Person-started scope. | Verify with the owner (GQ-09). |
| 67 | `scope-02:115-117`: error rows (`runtime_access_denied`); a bare `orca` may launch the GNOME screen reader. | Wrong binary. | Always call `orca-ide`. |
| 68 | `scope-02:122`: `stale_status`. | Stall proof. | Print the `observedAt` age; never classify stale as stalled. |
| 69 | `scope-02:124`: executable-failure handling. | Error reporting. | Copy the error verbatim. |
| 70 | `scope-02:157`: reuse of `parse_session_log` (a reuse judgement). It reads the whole file and cannot prove a turn is final. | Stall proof. | Tail the file; a missing `worker_done` is stall proof only with separate final-turn proof, otherwise "could not determine". |
| 71 | `scope-02:165` (CC): `ccsession --list` writes (it migrates names). | Read-only guarantee. | Read `topics/*.txt` directly. |
| 72 | `scope-03:108` (CC, low): `recommend.md:2` is `name: sc:recommend`, not bare. | Frontmatter template. | Use the `reflect.md` / `issue.md` bare-name form. |
| 73 | `scope-03:111` (CC, low): `recommend.md` Activation block is not an "identical form". | Activation template. | Copy from `reflect.md:146-151`. |
| 74 | `scope-03:140`: enforcement of the docs command surface is UNVERIFIED. | Docs drift. | Same as GQ-28. |
| 75 | `scope-04:33` (CC, partial): the "generated files" list is wrong; `layouts/group_a.py` and `group_b.py` are hand-written. | Layout reuse. | Read the layout sources before reuse. |
| 76 | `06:15-16`: live-only behaviour not captured. | Classifier inputs. | Live capture. |
| 77 | `06:127-132`: wait semantics. | Waiting proof. | Live capture (GQ-36, GQ-52). |
| 78 | `06:100`: caller identity. | Coordinator identity. | Same as GQ-53. |
| 79 | `07:8`: runtime behaviour not exercised; handler reads prove only what the CLI sends. | All allowlisted verbs. | Confirm read-only behaviour once on a throwaway Run. |
| 80 | `research-notes:193`: the end-of-turn marker was never captured. | Stall proof. | Capture one; until then "could not determine". |
| 81 | `research-notes:186`: "unverifiable is absence" rests on guide text. | Liveness rule. | Confirm with a live row (GQ-37). |

`scope-03:165` (the no-glob claim) is already struck as CC and resolved by B-21 / GQ-76.

### 9.3 Stale docs (gaps-file section (f))

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| 82 | S-01 to S-06 [STALE DOC] in `orca-capabilities.md`: CLI 1.4.237 versus 1.4.245; guide 202 versus 215 lines; `:127` hasMore; `[H:worker-list]` line 22 default scope; `:97-102`; `ask` timeout 600000 ms; shifted guide line numbers. | Plans may cite stale behaviour. | Cite the 1.4.245 captures; refresh the doc separately. |
| 83 | S-07 [STALE DOC]: the issue-339 analysis file was rewritten (F1-F14 at `:32-45`, S1-S5 at `:51-55`). | F1-F12 citations moved (C1). | Use F1-F14 / S1-S5. |
| 84 | S-08, S-09 [STALE DOC]: crash-recovery SKILL.md claims "pure read-only" and uses a `~/workspace` path. | Supports rejecting A4. | Do not reuse; record as rejection reasons. |
| 85 | S-10, S-11 [STALE DOC]: #409 docs on age-ranking and omission counts. | Layout rules. | Follow the layout source, not the docs (GQ-29, GQ-33). |
| 86 | S-12 [STALE DOC]: the `recommend` docstring. | Template copying. | Do not copy the docstring. |
| 87 | S-13, S-14 [STALE DOC]: `06:187` and `research-notes:241-242`. | Wording. | Same as GQ-89, GQ-94. |

### 9.4 Contradictions (gaps-file section (d) and web discrepancies)

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| 88 | C1 (CC): F1-F12 numbering is out of date. | Wrong citations. | Use F1-F14 / S1-S5. |
| 89 | C2 (CC): the test file length; it is 1202 lines. | Citation accuracy. | Use 1202. |
| 90 | C4 (CC): the `~/workspace` path. | A4 rejection reason. | Recorded under GQ-60. |
| 91 | C8 (UV): guide statements not checked against code. | Behaviour claims. | Treat as UNVERIFIED until captured. |
| 92 | C9 (CC): a `python -m` docstring. | Breaks the UV rule if copied. | Do not copy; use `uv run`. |
| 93 | C12: verified for one worker only. | Sample size. | Capture more rows (GQ-01). |
| 94 | web-01 D1 [EXTERNAL]: Kubernetes eviction. | Pattern mismatch. | Codebase wins. |
| 95 | web-01 D2 [EXTERNAL]: the Nagios KB says timeouts are not UNKNOWN, but web-02 says Icinga reports a plugin timeout as UNKNOWN. The two external sources disagree with each other. | Mapping of a probe timeout. | Codebase wins: a timeout is "could not determine". |
| 96 | web-01 D3 [EXTERNAL]: Harmonograf's "stuck". | Class naming. | Codebase wins: "stalled" only when proved. |
| 97 | web-01 D4 [EXTERNAL]: liveness restart. | Read-only sweep. | Codebase wins: the sweep never restarts. |
| 98 | web-02 [EXTERNAL]: Grafana's configurable no-data mapping contradicts WC-10. | Missing data handling. | Rejected; no data stays "could not determine". |
| 98a | Six versus seven classes (synth-02 4.8): the research question lists six; Section C (`research-notes:188`, `:194`) keeps fenced as its own class, resting on WC-12 (`WORKER-CONTRACT.md:60`). Owner choice: keep fenced as a seventh class, or fold it into could not determine. | Classifier, report Class column, SC-4 tests. | Owner decision; the plan uses Section C's seven classes as the working default (synth-05 OQ-13). |

### 9.5 AMBIGUITIES 1-11 (`research-notes.md:303-313`)

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| 99 | AMB 1: where the logic lives (A1-A4). | Architecture. | GQ-60. |
| 100 | AMB 2: default window 6 h or 72 h. | Default scope. | GQ-61. |
| 101 | AMB 3: report location. | Output path. | GQ-10. |
| 102 | AMB 4: WC-14 versus WC-1. | Contract conflict. | GQ-11. |
| 103 | AMB 5: PR #422 sequencing. | Merge order. | GQ-62. |
| 104 | AMB 6: pragmatic DONE/NEXT exception. | Report format. | GQ-63. |
| 105 | AMB 7: routing placement, `_POST_REFRESH_ADDITIONS` (`test_routing_refresh.py:33`), never-as-worker list. | Registry tests. | Add `"sweep"` to `_POST_REFRESH_ADDITIONS`; GQ-12, GQ-24. |
| 106 | AMB 8: person-started sessions. | Idle class scope. | GQ-09. |
| 107 | AMB 9: #409 pinning, tie-break, approval label. | Layout. | GQ-29, GQ-34, GQ-35. |
| 108 | AMB 10: "management server". | Later phase. | GQ-66. |
| 109 | AMB 11: worktree-first versus trigger-based placement (CR-01 / WC-11). | Placement rule. | GQ-67. |

### 9.6 Resolved rows and where they were resolved

| GQ rows | Where resolved |
|---------|----------------|
| GQ-03 (NB-4) | NB-4 fix pass, `qa/qa-nb4-fix-log.md` (2026-11-07); coordinator-approved exception at the Phase 3 research gate; re-checked at the Phase 5 synthesis gate. |
| GQ-07, GQ-13, GQ-18 (K1), GQ-20 (C5), GQ-42, GQ-45, GQ-55, GQ-96 | Marked resolved in `gaps-and-questions.md` with their resolution text. GQ-42's allowlist follow-up pointed at GQ-03. |
| GQ-68 to GQ-83 | Research-gate fix cycle (B-items, for example B-21 / GQ-76); `research/07-gate-gap-fill.md` covers B-04, B-07, B-09 and B-24. |
| C14 | Resolved in `gaps-and-questions.md` section (d). |

### 9.7 Gaps-section coverage per research file

| File | Gaps entries | Covered by |
|------|--------------|------------|
| `research/scope-01-contract.md` | Q1-Q7 | GQ-01, 11, 12, 10, 13, 14, 09 (rows 1, 9, 10, 8, 9.6, 11, 7) |
| `research/scope-02-orca-recovery.md` | Q1-Q9 | GQ-01, 15-22 (rows 1, 12-17, 9.6) |
| `research/scope-03-cli-patterns.md` | OQ1-OQ6 | GQ-23 to GQ-28 (rows 18-23) |
| `research/scope-04-409-layout.md` | Q1-Q8 | GQ-29, 02, 30-35 (rows 24-30, 2) |
| `research/05-orca-row-schema.md` | Gaps 1-10 | GQ-01, 36, 15, 37, 38, 39, 20, 40, 41, 42 |
| `research/06-orca-open-questions.md` | Gaps 1-19 | GQ-43, 44, 45, 46, 02, 47, 48, 49, 50, 51, 52, 17, 53, 54, 55, 40, 56, 57, 58 |
| `research/07-gate-gap-fill.md` | B-04, B-07, B-09, B-24 | Resolved rows (9.6); `07:8` and `07:92` caveats in rows 79 and 39 |
| `research/research-notes.md` | AMBIGUITIES 1-11, C1-C15, K1-K4 | 9.4, 9.5, rows 15, 18, 20 |
| `research/web-01-agent-supervisor-session-health.md` | D1-D4 | Rows 94-97 |
| `research/web-02-static-status-report-conventions.md` | Grafana no-data, I-PASS 403 | Row 98; I-PASS taken from the search excerpt (10, below) |

A file without a Key Takeaways list is not a defect and is not listed as one.

---

## 10. Evidence Trail

All research files produced during this investigation.

### Codebase Research

| File | Topic | Agent Type |
|------|-------|------------|
| `research/research-notes.md` (335 lines) | Research-phase notes: existing files, patterns, solution options A-D, recommended outputs, phases, AMBIGUITIES 1-11, C1-C15 | rf-task-researcher |
| `research/scope-01-contract.md` (152 lines) | Worker contract and its tests | Phase 2 codebase research agent |
| `research/scope-02-orca-recovery.md` (242 lines) | Orca state, crash-recovery and ccsession | Phase 2 codebase research agent |
| `research/scope-03-cli-patterns.md` (215 lines) | CLI, command and skill patterns; default argv allowlist (edited by the NB-4 fix pass) | Phase 2 codebase research agent |
| `research/scope-04-409-layout.md` (374 lines) | #409 observer layout for a static report | Phase 2 codebase research agent |
| `research/05-orca-row-schema.md` (206 lines) | Orca worker-list row schema (G-A) | Phase 2b gap-fill codebase agent |
| `research/06-orca-open-questions.md` (190 lines) | Orca open questions (G-B) | Phase 2b gap-fill codebase agent |
| `research/07-gate-gap-fill.md` (94 lines) | Research-gate gap fill for B-04, B-07, B-09, B-24 (fix cycle 1). Read-only: Orca `--help` on CLI 1.4.245-aidev02.780594c521aa and handler sources under `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/` | Research-gate fix agent |

### Web Research

All entries are [EXTERNAL]. Phase 4 web research used WebSearch and WebFetch because Tavily was unavailable.

| File | Topic |
|------|-------|
| `research/web-01-agent-supervisor-session-health.md` (229 lines) [EXTERNAL] | Supervisor and health-check patterns: Erlang/OTP, Kubernetes probes, phi accrual, "unknown" as a state, LLM agent patterns. 14 sources, some from search results only. Fallback note `[WEB_RESEARCH_FALLBACK: tavily=tool not loaded ...; used=WebSearch+WebFetch]`. Discrepancies D1-D4 resolved as "codebase wins". |
| `research/web-02-static-status-report-conventions.md` (63 lines) [EXTERNAL] | Static status report conventions. Backend WebSearch / WebFetch only (`fallback_reason: tavily_missing`). The research agent had no file-writing tool; the task executor saved its reply unchanged (logged under Deviations in the task file). The I-PASS AHRQ WebFetch returned 403, so that content is from the search excerpt. Grafana's no-data mapping is rejected (contradicts WC-10). |

### Synthesis files

- `synthesis/synth-01-problem-current-state.md`
- `synthesis/synth-02-target-gaps.md`
- `synthesis/synth-03-external-findings.md`
- `synthesis/synth-04-options-recommendation.md`
- `synthesis/synth-05-implementation-plan.md` (planned; not yet written when this file was produced)
- `synthesis/synth-06-questions-evidence.md` (this file)

### Gaps Log

- `gaps-and-questions.md`: GQ-01 to GQ-100; 75 open, 25 resolved (`:125`). GQ-03 (NB-4) was resolved by the NB-4 fix pass and is re-checked at the Phase 5 synthesis gate.

### QA reports

- `qa/` (24 files): analyst completeness reports 1-2, analyst cross-validation reports 1-2, Phase 3 consolidated findings (initial and cycle 1), research evidence / gaps / qualitative reports 1-2, research fix logs (initial and cycle 1), research verification and qualitative verification (initial and cycle 1), task-research alignment report, task validation reports (B2, consolidated, structure, fix cycle 1, verify cycle 1).
- `qa/qa-nb4-fix-log.md`: the NB-4 fix pass (2026-11-07). NB-4 was a coordinator-approved exception at the Phase 3 research gate. Three edits (two at `scope-03:99`, one at GQ-03); the eight dependent lines checked all agree.
