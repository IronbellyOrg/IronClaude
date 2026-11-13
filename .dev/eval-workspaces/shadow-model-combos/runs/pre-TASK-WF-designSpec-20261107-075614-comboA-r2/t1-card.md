# T1 Reflection Card — UC-1 pre-execution (comboA-r2)

- Run: pre-TASK-WF-designSpec-20261107-075614-comboA-r2 (shadow experiment, combo A repeat 2)
- Mode: UC-1 | tier pinned 2 (`--tier 2`) | t2-engine shadow | reviewers 3
- Inputs: spec sha a865f397…, tasklist sha 044809e3… (frozen, byte-identical to r1's)
- Temporal grounding: spec pin `e8db2fe6` (2026-11-07). HEAD `c2e3347d3` carries the LANDED
  feature (EventType now 60 members, `merge_guard.py` present). All facts verified AT THE PIN
  via `git show e8db2fe6:<path>`; the landed diff is excluded from the audit (same policy as r1).
  The `.dev/tasks/done/TASK-WF-designSpec-20261107-075614/` package (implement history) was NOT
  read — it is the answer key for this corpus.

## Grounding (Wave 1A, at pin e8db2fe6)

Verified: EventType exactly 43 members; `merge_guard.py` absent; `RunLog.append` rejects unknown
types (run_log.py:117 docstring "43 closed"); `detect_crash_window` push-only, pairs by
`idempotency_key` (recovery.py:69-92); `CONFLICT_CYCLE_PREFIXES = ("sync-", "conflict-")`
(conflicts.py:46), `is_conflict_cycle` (conflicts.py:1242); `recovery.py` imports `run_log`
(recovery.py:37) and `run_log` imports only `models`, while `conflicts` imports `fsm` and `fsm`
imports `loop_guard/models/severity_router` — so `run_log → merge_guard → conflicts → fsm` closes
NO cycle (no import-cycle risk in Task 5's wiring); `BRANCH_A_LANDED/"landed"`, `BRANCH_B_NOT_LANDED`,
`BRANCH_C_AMBIGUOUS` (recovery.py:40-42); `FIX_APPLIED`/`PUSH_INITIATED`/`PUSH_COMPLETED`/
`REREVIEW_REQUESTED` exist (models.py:63,69-70,84) so Task 11's acceptance trace is well-formed;
`CORE_PURE_FILES` incl. state-machine.md, loop-guard.md (test_static_grep.py) and the whole-word
gh/git regex; `WRITE_VERB_RE`/`WRITE_VERB_CLASSIFICATION`/both stale tests
(test_worker_contract.py:1090-1166,2199-2205); `test_intent_and_validator_lines_say_tier_2`
(test_conflict_sync_protocol.py:412 — Tier-2 label rule with 2 pre-existing validator-line
exemptions); `test_no_src_superclaude_path` (:576) and `test_allowed_tools_cover_every_program`
(:587, scans NEW_REFS=(conflict-mechanical, conflict-intent) only — merge-guard.md is NOT auto-
scanned by it); `_RESOLUTION_SCRIPTS` (4 scripts, origin-URL sed tests); `_NEW_KEY_DEFAULTS`
(test_run_log.py:312) and `test_eventtype_is_43_members…` (:171); `len(EventType)==43`
(test_codex_reviews.py:441); `test_conflict_max_tier_default_and_bounds`
(test_skill_parse.py:110); one-python-fence gates (test_cosmos_protocol.py:34-44,
test_codex_reviews.py:685-697); wait-only sentence pin (test_static_grep.py:~791);
`test_skill_forbids_force_push` (:761); `IDEMPOTENCY_SETS == 7` (test_idempotency.py:89);
front matter `allowed-tools: … Bash(gh *), Bash(git *), Bash(uv *), Bash(make *), Bash(jq *) …`.

## Coverage (Wave 1B, Step 1B.0 two-pass)

- Pass 1 (deterministic): 0 parsed IDs in BOTH docs — the spec labels requirements `FR-1..FR-23`,
  outside `ID_REGEX` (`R-|REQ-|SPEC-|T-`). `coverage_pct` (parsed-only) = null.
- Pass 2 (requirements-analyst, quote-pinned): 45 rows INF-001..INF-045, every row
  quote+citation verified (8-row random spot-check passed, 0 bad). NOTE vs r1: r1's analyst
  emitted 15 rows; extraction granularity varies per run. Both are honest counts; union
  denominators are therefore not directly comparable across runs.
- Deterministic containment floor: 26/45 matched (0.5778), 19 unmapped, S_dev_density 0.4222.
- Step 1B.2b: inferred 45 > parsed 0 → `coverage_degraded: parsed-sparse` (T1-stop pre-filter;
  run is T2-pinned regardless).

### Semantic resolution of the 19 floor-unmapped rows (T1 judgment, all resolved COVERED)

The containment rule (case-folded word overlap ≥0.6 within a single task) under-matches
cross-cutting constraints that the plan restates at PLAN level (Constraints section) rather
than inside one task. Resolutions (each verified by reading the plan):

- INF-001 owner decisions → plan Goal (L15) + Constraints "Owner decisions already accepted" (L26)
- INF-003 core-decides/SKILL-performs, no new MonitorState → Constraints L20 (purity) + Task 10 overlay note ("folded values, not MonitorState members")
- INF-004 ordinal<3/off/conflict → no mutation → Task 4 AC (engage row 1 NOOP at ordinal 2/off/`sync-1`/`conflict-1`) + Task 11 `test_guard_modes_ordinals_and_resume_authority`
- INF-009 merge_guard.py purity + import allowlist → Constraints L20 + Task 3 text
- INF-011 held_cycle_published contract → Task 3 (normal + recovered test) + Task 4 resume row 4
- INF-012 BRANCH_* == recovery constants, dual-import test → Task 3 AC (explicit)
- INF-015 EventType 43→45 + all count texts → Task 2 (models docstrings, run_log docstring, loop-guard enumeration)
- INF-016 request appended+fsynced BEFORE the call → Task 8 protocol step ("append … with fsync before the call")
- INF-019 original_is_draft never re-read from GitHub → Task 3 fold AC ("taken only from the first guard record or a first skip, never from a later read")
- INF-030 WRITE_VERB_CLASSIFICATION discipline → Constraints L22 + add-last steps in Tasks 7, 8, 9, 12
- INF-033 crash after normal push_completed (published path) → Task 11 AC ("asserts detect_crash_window returns None and published is true")
- INF-034 make sync-dev per editing task → Constraints L27
- INF-035 twelve minimum tests → Task 11 AC names all twelve test functions one-for-one (verified against spec §7 table)
- INF-039 O4 S5a text unchanged → Task 1 O4 + Task 10 byte-identical constants
- INF-040 symbol-name citation rule → Constraints L23
- INF-041 complete Depends-on declarations → verified: T5→{3,4}, T8→{1,4,7}, T9→{6,8}, T10→{9}, T11→{3,4,5,7}, T12→{6,8}, T13→{2,10,11,12} — every consumer edge present
- INF-042 wrong-implementation-fails ACs → Tasks 3/4 ACs ("each of these cases fails if the row is implemented wrongly")
- INF-043 no file:NNN / no evidence-validator / conflict-intent.md words → Constraints L21+L23
- INF-044 test hygiene (no test_* imports; pr_not_open asserted on RunLog.read_events) → Task 11 AC (explicit)

**Coverage after semantic resolution: 45/45 = 1.0** (deterministic floor 0.5778; resolution is
T1 judgment, to be pressure-tested by the T2 panel). unmapped_requirements_union after
resolution: []. Section-6 file table fully mapped to tasks 1-13; §7 twelve tests all named in
Task 11; §10 plan-authoring notes all present as plan constraints or Task 1 ACs.

## Hypotheses (candidate findings, pre-calibration)

- **H1 [MINOR — spec wording]** Spec F5 calls `--conflict-max-tier` "the one enum flag of this
  parser (`choices=`)" but `--monitor` also uses `choices=` at fsm.py:81 at the pin. Not
  load-bearing for the plan (Task 6 copies the SHAPE of --conflict-max-tier, not a uniqueness
  claim), but the fact as stated is imprecise. Grounded: fsm.py:80-81,103-109 at pin.
- **H2 [MINOR — method transparency]** The deterministic containment floor reports 0.5778 with
  19 unmapped rows that all resolve semantically; any downstream consumer reading
  `coverage_pct_union` without the resolution table would misread plan quality. Mitigated inside
  this report; no plan change required.
- **H3 [CONFORMANCE — verified]** All 13 tasks map onto spec sections 3-10 with no uncovered
  requirement found at T1 depth; the dependency graph is complete; the add-last classification
  discipline and per-task `make sync-dev` are restated everywhere the spec demands them.
- **H4 [MINOR — scope note]** `test_allowed_tools_cover_every_program` scans only the two
  conflict refs; `refs/merge-guard.md` fenced commands are covered instead by Task 8's own
  protocol test (allowed-program rule + repo-scope + script-exists). Residual exposure: nothing
  checks the new ref's fenced programs against the SKILL front-matter grants; Task 1 O2 is the
  plan's own resolution path for script invocation grants. Acceptable; reviewers should confirm.
- **H5 [note]** The spec's own line-number citations (models.py:24, run_log.py:117-125,
  test_run_log.py:171-175, test_codex_reviews.py:441, test_static_grep.py:791) were all
  verified accurate at the pin; the plan correctly avoids bare line numbers per spec §10/INF-040.

No REGRESSION-class candidate exists in UC-1 (nothing has executed). No blocking candidate at
T1 depth. Blind calibration of this card is deferred to the Wave-3C single calibrator pass
(tier pinned 2; same convention as r1).
