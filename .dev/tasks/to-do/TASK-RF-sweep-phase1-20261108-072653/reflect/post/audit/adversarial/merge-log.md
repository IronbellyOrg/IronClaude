# Merge Log

## Metadata
- Pipeline: /sc:adversarial Mode A inside reflect post-execution audit (Step 5), run `reflect-post-20261112T192600Z-TASK-RF-sweep-phase1`
- Base variant: variant 3 (reviewer 3, refactorer, opus; final score 0.796, `base-selection.md`)
- Executor: merge-executor agent
- Plan: `refactor-plan.md` (13 planned changes)
- Changes applied: 13 of 13
- Status: COMPLETE (no change failed or skipped)
- Output: `merged-verdict.yaml` (schema `sc-reflect-merged-verdict/v1`, 17 findings F-01..F-17)
- Timestamp: 2026-11-12
- Scope: only `merged-verdict.yaml` and this log were written. No repository file was edited.
- Provenance convention: each finding carries `provenance: {cards, debate, invariants}`; the aliases TL, DESIGN, SPEC, PROBES, CLASSIFY (and PLANS, added by this merge as shorthand for the decision-record folder) are defined in `path_aliases`.

## Per-Change Status

| # | Change | Finding(s) | Status | Before (base V3) | After (merged) | Provenance tag |
|---|---|---|---|---|---|---|
| 1 | Keep the C-003 Regression, add the dissent note | F-01 | APPLIED | R3-F3 Regression medium, confidence 0.65, no dissent | Regression medium, `contested: [F-01]`, confidence 0.62; notes carry the V1 and blind-calibrator Drift-medium dissent, the fallback rule and INV-005 | V3 R3-F3; V1 R1-F4; INV-005, INV-003 |
| 2 | Lower R3-F4 to Drift minor | F-05 | APPLIED | R3-F4 Regression medium | Drift minor; unread head and misnamed test in one finding; INV-007 note | V3 R3-F4; V2 R2-F5; INV-007 |
| 3 | Hardening findings to Drift minor follow-ups | F-10, F-11, F-12 | APPLIED | R3-F1, R3-F2, R3-F5 Drift medium | Drift minor, "V1 view: medium" note on each; F-11 names the tab-map reader as the `is_file` sibling (the PROBES:837 mis-cite is corrected) | V3 R3-F1, R3-F2, R3-F5 |
| 4 | Split C-008 by field | F-07 | APPLIED | R3-F8 Drift minor, no split | Drift minor with a note listing `mtime` and `agent_wait_since` as Necessary; V1's `authorized` label not carried | V3 R3-F8; V1 R1-F6, R1-F7 |
| 5 | Add the Rule 5 finding with its footnote residual | F-13 | APPLIED | not examined by V3 | Authorized minor; `authorization_source` is the owner decision; SPEC FR-006 never amended; residual footnote Drift (FIN-F15); agent-wait feed Necessary | V1 R1-F1, R1-F2; V2 R2-F6 |
| 6 | Add the dropped-worker-row finding | F-04 | APPLIED | not examined by V3 | Drift medium; conditional escalation (id-less rows from real Orca) and INV-008 note | V1 R1-F3; INV-001, INV-002, INV-008 |
| 7 | Add the `_git` reason-wording finding | F-06 | APPLIED | only mentioned inside R3-F3 | Drift minor; absorbs DC-12; `_orca` prints MiB noted | V1 R1-F5; V3 R3-F3 mention; DC-12 |
| 8 | Add the stale-text finding | F-03 | APPLIED | not examined by V3 | Drift medium; recommendation set OQ-2..OQ-8 RESOLVED with record paths and update DESIGN lines 5-11 | V2 R2-F1 |
| 9 | Add the NFR-007 publication-test finding at Drift medium | F-02 | APPLIED | not examined by V3 | Drift medium; FIN-F19 cross-reference flagged as wrong; INV-012 note | V2 R2-F4; INV-012 |
| 10 | Add the FIN-F7 limitation and the environmental test failures | F-15, F-17 | APPLIED | not examined by V3 | F-15 Authorized medium (owner words are the executor's own recommendation pasted back); F-17 Necessary medium (qualified completion, not a pass of the full suite) | V2 R2-F2, R2-F3 |
| 11 | Keep V3's own Authorized findings unchanged | F-14, F-16 | APPLIED | R3-F9, R3-F10 | Unchanged class and severity (Authorized minor); renumbered | V3 R3-F9, R3-F10 |
| 12 | Keep V3's R3-F6 and R3-F7 unchanged | F-08, F-09 | APPLIED | R3-F6, R3-F7 Drift minor | Unchanged; the weak `commands.py:219-221` cite is replaced by the `_PublishError` second-line cite (`commands.py:137-143`) | V3 R3-F6, R3-F7 |
| 13 | Carry the objective qualification and shared-assumption rulings | summary keys | APPLIED | none | `objective_summary` (1, 2, 4, 5 pass; 3 qualified pass because of F-05; 6 not fully satisfied because of F-17 and F-02; 7 pending); `shared_assumption_rulings` A-001 QUALIFY, A-002 QUALIFY, A-004 ACCEPT with the debate wording | V2 objective_checks and concession; A-001, A-002, A-004 |

### Notes on how the plan was executed
- Finding order follows the plan's id map exactly (F-01 Regression; F-02..F-04 Drift medium; F-05..F-12 Drift minor; F-13, F-14, F-16 Authorized minor and F-15 Authorized medium; F-17 Necessary medium). F-15 sits before F-16 as the id map orders it.
- The finding `class` is the primary class. F-13 (Authorized) carries the residual footnote Drift and F-07 (Drift) the Necessary sub-part in `notes`; `deviation_counts` says so in a header comment.
- `severity_counts`: medium 6 (F-01, F-02, F-03, F-04, F-15, F-17), minor 11, blocking 0. Computed from the findings, not copied.
- Two small differences from the plan text, both fixes of a source error, not changes of outcome:
  1. `FINAL-GATE-halt-resolution-decision.md`: the plan and V1 cite `:17-19` for "All 3 approved". The quote is at `:13`; the three approved changes are at `:17-19`. F-13 cites `:13` and `:18`.
  2. `qa-readonly-safety-report.md` is cited without a folder in the plan; the file is `qa/final/qa-readonly-safety-report.md` (RO-1 at `:13`, RO-2 at `:14`, follow-up lines `:55-56`). F-10 and F-11 give the full path.
- F-15 gives its authorization as `FINAL-GATE-FIN-F7-ruling.md:15-17` (the plan said `:17`; `:15` holds the limitation text, `:17` the continuation).

## Post-Merge Validation

### 1. Structural check
| Check | Result |
|---|---|
| YAML parses (`yaml.safe_load`) | PASS |
| Top-level key order | PASS: schema, merge_method, base_variant, sources, convergence_score, convergence_detail, convergence_status, taxonomy_coverage, unaddressed_invariants_high, unaddressed_invariants_medium, path_aliases, deviation_counts, severity_counts, regression_present, contested, findings, not_carried, objective_summary, shared_assumption_rulings, grounding_gaps_carried, reviewer_calibration, verdict_inputs |
| Number of findings | 17 |
| Unique ids F-01..F-17, in order | PASS (17 unique) |
| Required fields on every finding (id, title, class, severity, diff_point, lead_ref, location, claim, evidence, authorization_source, recommendation, confidence, provenance, notes) | PASS (none missing) |
| Class counts from the findings | drift 11, authorized 4, regression 1, necessary 1 (matches `deviation_counts`) |
| Severity counts from the findings | medium 6, minor 11, blocking 0 (matches `severity_counts`) |
| Evidence entries | 116 in total: 113 with a verbatim quote, 3 with a `note` (F-03 `OQ-2` record exists per Glob; F-04 fixture count from a search; F-10 search of the sweep package for `fsmonitor` finds no match) |
| `merge_method` value | `adversarial` (exact) |

### 2. Contradiction re-scan
- The 17 findings carry 17 distinct diff points; no diff point appears in two findings, and no diff point has more than one class. So no finding says both Regression and Authorized for the same diff point (C-001/X-001 appears only as Authorized in F-13; C-003/X-003 only as Regression in F-01).
- The only mentions of "regression" outside F-01 are in `notes` of F-02, F-05 and F-13, where they record a label that was NOT carried (V2's blocking Regression labels, V3's withdrawn R3-F4 label). They are not class claims.
- F-01 is contested by design (2 of 3 majority, dissent recorded); that is a recorded dissent, not an internal contradiction.
- No finding is blocking, consistent with S-002.

### 3. Broken-reference check (cited file:line refs re-Read)
All 113 quoted evidence entries were checked by script against the cited line (or line range) of the cited file; every quote was found (113 resolved, 0 broken, 27 distinct files). The refs below were also re-Read by hand while writing:

| # | Ref | Check | Result |
|---|---|---|---|
| 1 | SPEC:286 | "run it with `subprocess.Popen`" | resolved |
| 2 | PROBES:257, :270, :308, :316 | `subprocess.run(` seams and the after-exit size checks | resolved |
| 3 | tests/sweep/conftest.py:40-42 | `subprocess.run`, `Popen` and `os.system` all patched | resolved |
| 4 | TL:1452 | "subprocess guard only catches calls made as `subprocess.run`" | resolved |
| 5 | TL:2992 | note (13) "output is held in memory before the 8 MiB check" | resolved |
| 6 | PROBES:355-357 | first-call `call_failed` becomes `unavailable` (INV-005) | resolved |
| 7 | PROBES:1105-1119 | dropped-row logic and the `row {index}` source row | resolved |
| 8 | CLASSIFY:690-694, :730, :739, :759-762 | origin guard reads two list rows only; fail-open path | resolved |
| 9 | tests/sweep/test_probes_allowlist.py:1144-1147, :1169 | tests stop at `report.render` | resolved |
| 10 | tests/sweep/test_probes_allowlist.py:1328-1331, :1336 | misnamed head-and-tail test; first-line drop test | resolved |
| 11 | PROBES:557-569 | tail-only ledger read, `seek(size - LEDGER_SPLIT)` | resolved |
| 12 | DESIGN:5, :7 | stale approval and "NOT a clean pass" text | resolved |
| 13 | TL:3037-3043 | OQ-2..OQ-8 still PENDING | resolved |
| 14 | DESIGN:62, :491, :680, :717, :760, :840, :1050, :1052 | quoted rows and addendum | resolved |
| 15 | SPEC:100, :136, :286, :291, :295 | FR-006, NFR-007, section 8, budget scope, byte limits | resolved |
| 16 | CLASSIFY:251-257; report.py:42-45; test_classify.py:368, :376 | Rule 5 inert; footnote names stalled and fenced only; every class but working | resolved |
| 17 | PLANS/FINAL-GATE-halt-resolution-decision.md:13, :17-19, :24 | "All 3 approved"; the three changes; section 13 not changed | resolved |
| 18 | PLANS/FINAL-GATE-FIN-F7-ruling.md:11, :15, :16 | owner words; documented limitation; gate decision text | resolved |
| 19 | src/superclaude/skills/sc-sweep-protocol/SKILL.md:25, :27, :35, :49 | summary-only parse; "standard error line"; exempt reply; stale-copy fallback | resolved |
| 20 | src/superclaude/core/HOW-WE-WORK.md:405 and WORKER-CONTRACT.md:277 | "on every wake" versus "wake or wait timeout" | resolved |
| 21 | report.py:590-598, :664, :694 | sanitizer replacement table and its use in `to_json` | resolved |
| 22 | phase14-full-pytest.md:9, :22, :23, :25 | 3 failed / 25252 passed; no module named ruff; timing test; pre-existing wording | resolved |
| 23 | commands.py:137-143, :153, :253; PROBES:589, :944, :1247, :1253-1255 | second stderr line; `_publish`; duplicated XDG path; wrappers | resolved |
| 24 | models.py:21, :28, :104, :148; PROBES:132 | constants, `mtime`, `freshness_age_s`, `share_shows(wanted)` | resolved |

No cited ref was found broken. Source-card citations that failed calibration were not carried as written: V1's `FINAL-GATE...:18-19` (F-13), V3's `probes.py:837` (F-11) and `commands.py:219-221` (F-08), V2's "FIN-F19" cross-reference (F-02).

## Summary

| Item | Count |
|---|---|
| Planned changes | 13 |
| Applied | 13 |
| Failed | 0 |
| Skipped | 0 |
| Findings in merged verdict | 17 (Regression 1, Drift 11, Authorized 4, Necessary 1) |
| Severity | blocking 0, medium 6, minor 11 |
| Evidence entries | 116 (113 quoted and verified, 3 notes) |
| Quotes unresolved | 0 |

Open points left for the orchestrator or a person (not merge problems):
- F-01 class is contested (Regression versus Drift medium); needs a human decision.
- F-04 escalation depends on whether real Orca emits id-less worker rows (UNVERIFIED).
- F-03 includes an edit of DESIGN, which is edited only by owner decision.
- Five grounding gaps are carried in the verdict (`grounding_gaps_carried`).
