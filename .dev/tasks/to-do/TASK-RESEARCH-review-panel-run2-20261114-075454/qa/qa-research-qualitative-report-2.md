# QA Report - Research Gate, Research-Depth Lens (Partition B, Item 3.14)

**Topic:** which ONE unified central Review Panel (shared core plus thin modules) captures all the value of E1, E2 and E3
**Date:** 2026-11-14
**Phase:** report-qualitative / research-gate (research-depth lens)
**Files reviewed:** research/09-collaboration-designs.md, 10-process-redesign.md, 11-consumers-tasklist-workflow.md, 12-consumers-spec-review.md, 13-future-pr-review-and-rfqa.md, 14-e3-variants-and-experiments.md, 15-telemetry-manifest-run-record.md, 16-eval-governance.md (plus research/research-notes.md as reference)
**Fix cycle:** N/A (report-only, fix_authorization: false)
**Status: Complete**

---

## Reading log

Read completely, in order: line 258 of the task file (my prompt), research/research-notes.md, then 09-collaboration-designs.md (223 lines), 10-process-redesign.md (244), 11-consumers-tasklist-workflow.md (188), 12-consumers-spec-review.md (230), 13-future-pr-review-and-rfqa.md (278), 14-e3-variants-and-experiments.md (277), 15-telemetry-manifest-run-record.md (250), 16-eval-governance.md (301). For checklist item 6 I read the `## Gaps and Questions` section of all 12 scope slices (01 to 12), and then looked for where each carried gap or question was resolved, logged or ledger-carried.

Independence: grep of 09-16 for `TASK-RESEARCH-review-panel-unify` and `REVIEW-PANEL-UNIFY-RUN2-QUEUED` found no hit in any assigned file (the only two hits are the slices' own "not read" statements in scope/11 and scope/12). I did not open either forbidden location.

## Independent verification performed (read-only; none of it relied on another report)

HEAD `50d4d2b9d` code:
1. `findings_v2.py:84-187` read whole: `check_finding` rejects only `calibrated_confidence` (`:96-97`) and never iterates keys; `parse_block` keeps the whole object (`:289-290`). Confirms 09 X11, 10 Unit 2, 13 section 6.
2. `findings.py:14-29` (SEVERITIES, CATEGORIES, `_REF_TOKEN`), `ledger.py:93-157` (`_decision`, `_brief_ids`, `merge_round`, quorum behaviour), `cluster_cmd.py:27-34` (fenced yaml calibration handled at HEAD).
3. `runner.py:497,504` `--no-session-persistence` (09 section 4.1).
4. `pr_submit/fsm.py:364-372` `is_groundable`; `fsm.py:32-33` and `loop_guard.py:19-20` define the cap pair twice; `wc -l pr_submit/*.py` = 6,511 over 13 files; `REVIEWERS` and `_CODEX_HINTS` as in 13.
5. `panel.py:46` `_SLOT_KEYS`, `:215` rejection; `contract.py:310-321` 0.80 degrade; `reflect_shadow_exit.py:59,313` and `panel_lint.py:188` (16 Part 3.4).
6. `telemetry.py:362-379` `model_scores` view: SUM of `r.cost_tokens_out` over a LEFT JOIN on outcomes, `cost_per_confirmed_tp` computed in the view (15 section 2).
7. `install_skills.py:85-116` (14 section 3.2); `wc -l cli/review/*.py` = 5,086 over 16 files.
8. `swarm/lenses/__init__.py:75-118` (9 entries incl. `custom`); tasklist `SKILL.md:1640,1646,1667`; `spec-panel.md:256-266`; reflect `SKILL.md:87,309-313`; U1 grep `subagent_type ... rf-` = 44 over 8 SKILL.md files; `test_verdict_mapping.py` = 36 `def test_`; `test_review_severity_rule.py:215` `CANONICAL_CAP_TEXT`.

Recorded runs in this worktree:
9. 29 `panel/manifest.json` files: 28 published, 1 clustered; 20 with dispatched = collected = 3; 9 with only `collected` attempts (A-r2, A-r3, B-r2, C-r2, shadow04, 05, 08, 09, 10), all with `dispatched` in `stages`; reviewers_complete = 3 everywhere (15 section 7 exact).
10. 13 coverage sidecars: 39 entries, assigned 0 to 9 per reviewer, 11 files with a duplicated row id, 2 with empty `observed` everywhere; precheck totals 275/110 and 772/400 with the by-flag splits (10 Unit 10 exact).
11. E1 `results.jsonl`: 15 rows, 4,119,747 output tokens, USD 478.4, `calibrator_diversity` degraded 14 / full 1; orchestrator-alias share min 0.38 (E1), median 0.59, max 0.87 (B3) (15 section 4.4 exact).
12. `~/.claude/skills/sc-review-ledger/scripts/review_ledger.py` imports only the standard library (so the installed ledger variant is a stand-alone re-implementation, consistent with 14 section 7.2).

E2 tip `6c0984326` via `git show` / `git ls-tree` only:
13. Static `def test_` counts r1..r5 = 103 / 163 / 89 / 90 / 82 over 21 / 18 / 22 / 15 / 13 files; `/lib/` paths = 0 in each package; `.gitignore:13` = `lib/`, `:79` = `*.log` (09 section 2.1-2.2 exact).
14. `final-table.py:15-18` `fullpkg()` as quoted; `run-reviewer.sh` fallback ladder overwrites `MODEL` (16 Part 1.1, 2.2); ground-truth.json item counts 10 (5 blocking), 4 (3 blocking, 2 dropped), 2 (0 blocking); `j1-` appears in 0 of the six `flags.tsv`; audit row counts 106 / 230 / 409 / 438 / 62 / 55; `three-way.py:6` family list holds one b4 and five j1 rows (16 Part 2.3, 7.1).

Not independently re-derived (relied on the file's own tagged statements): the 175 / 247 prose spawn-line census (13 section 4.2), the 449-occurrence test grep, E2 smoke-row values other than those listed above, the FINAL-REPORT byte and hash arithmetic in 14 sections 1-2, transcript counts under `~/.claude/projects/`, and the external documentation claims (Claude Code docs).

## Checklist results (research-depth lens)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Findings genuinely deep or superficial | PASS | Each of 09-16 traces mechanisms to file:line (hook skeleton compared across four scripts in 09 section 1.3; D-17 and D-23 reproduced by scratch run in 15 sections 2-3; fullpkg bug executed and reach recounted in 16 section 2.2; clause-by-clause #479 mapping in 14 section 4.2). Every number I re-derived (items 9-14 above) matched. Shallow areas are confined to material the files themselves flag (finding M4, M10 below). |
| 2 | Key findings actionable for core and thin modules | PASS | Each file ends in a concrete core-versus-module allocation: 09 section 4.1 and 5 (exchange optional, H1/H2 core, H3/H4 per module); 10 Unit 9 (19 ideas with destination); 12 section 8 (blocking boolean plus label maps, `max_fix_cycles = 2` default, no Medium token); 13 section 8 (M1-M14 core exposures); 14 section 7 (value classes); 15 section 8 (event-row run record); 16 Parts 4-5 (Tier S/Q/G, layer ownership). |
| 3 | Beyond surface reading: data flow, edge cases, callers and consumers | PASS | Examples I re-verified: consumers of `reflect_status` mapped to four readers (11 section 5.3); pr_submit `is_groundable` identified as the hard blocker for text-anchored findings (13 P1, fsm.py:364-372 read); `model_scores` fan-out reproduced with numbers; 29 real manifests scanned for D-23. Edge cases and failure modes are checked, not asserted. |
| 4 | Conclusions proportionate to evidence | PASS with notes | Strong claims are backed by verified code or recount. The design recommendations that outrun their evidence are explicitly labelled (15 section 8 "PROPOSAL", 16 Part 4 "derived", 09 section 7 "neither confirmed nor refuted"). Three places are a notch firmer than their evidence (M1, M6, M12 below). |
| 5 | Circularity or unverified assumption stated as fact | PASS with notes | No conclusion cites its own synthesis. Residual: M6 (15 section 7, "not a race") and M7 (15 section 6.2 item 4). |
| 6 | Open items honestly acknowledged | PASS with notes | Every open item in research-notes rows 09-16 is answered in its file (09: three items; 10: a-d; 11: a-c plus DO4; 12: a-d; 13: a-d; 14: a-d; 15: a-d; 16: a-d). Slice gaps and questions are resolved, logged in each file's `## Gaps and Questions`, or carried to value-ledger rows (examples: slice 06 Q8 to VL-21-986/1683; slice 05 O-8 to the 21/22 ledgers; slice 12 gap 5 resolved in 13 section 5; slice 01 G6 resolved in 12 section 6 for `src/`). Remaining soft spots are M4, M9, M10, M13. |
| 7 | [CODE-CONTRADICTED] or [UNVERIFIED] AMBIGUITIES claim used as fact | PASS with notes | Handled correctly: "no tasklist review step" (11 section 5.2), "no missing-task category / no severity levels" (10 Unit 8), "four verdict flips" (16 stale-doc row), "159 functions" not reused. One soft restatement: M7. The 92/80/49 figure appears in 16 Part 4.2 with its source line and unit as stated by the report, not as an adjudicated fact. |

## Findings

All findings are minor (notes only). No blocking finding was found after the verification above.

| # | Severity | Blocking Y/N | File and location | Finding | Evidence | Proposed fix |
|---|----------|--------------|-------------------|---------|----------|--------------|
| M1 | MINOR | N | 09 section 5, row H1 | H1 is labelled UNCONDITIONAL on "cost near 0" (an assertion) and a motive figure (156 of 665 runs never opened source.md) that the file itself tags `[UNVERIFIED-slice]`. The effect size is stated as unmeasured, so the hedge is present, but the verdict word is firmer than the 09 evidence. | 09 line 137. Independent corroboration exists in other files: 10 Unit 8 (brief placeholders `{{CANDIDATE}}`..`{{IDS}}`, no driving-document slot; brief file lines 17-21 confirmed) and 12 section 6 (E2 harness brief names no source). | Cite 10 Unit 8 and 12 section 6 as the verified basis and call H1 "recommended unconditional (design choice, effect unmeasured)". |
| M2 | MINOR | N | 09 Summary versus sections 1.3 and 4.2 | The Summary says `reflect-reviewer` "is skipped by the packages' own subagent filter". The body shows only r1, r4 and r5 skip calls that carry `agent_id`; r2's receiver hook has no such branch (09 line 42), and r3 has no hook. | 09 lines 42, 120, 223. | Reword the Summary to "the r1, r4 and r5 hooks skip subagent calls". |
| M3 | MINOR | N | 13 section 6 and section 8 row M3; 09 gap 5 | 13 lists `in_diff`, `confidence`, `original_line` as having "no field in either version" and M3 treats passthrough as something to add, but 09 X11 and 10 Unit 2 (and my read of `findings_v2.py:84-187, 289-290`) show unknown keys already pass `check_finding` and are retained by `parse_block`. 09 leaves downstream retention (cluster, card_convert, merge) open although it is a short read. | 13 line 168 and M3 row; 09 line 160 and gap 5; findings_v2.py as read. | Add one sentence to 13 M3: extra keys are tolerated at parse but have no defined semantics; resolve downstream retention in synthesis or a short follow-up read. |
| M4 | MINOR | N | 13 sections 4.1, 7.2 (R8, R12), 8 (M1-M14); gap 5 | rf-qa-qualitative (1,154 lines) and rf-analyst (428) were read by headings only. The M-list therefore omits two interface items the research already saw: the spawn contract's `assigned_files` partition and the inherited-structural-verdict passthrough pinned by `tests/skills/test_task_builder_merge.py:236-271` (13 section 5 cites that test). `assigned_files` is the same concept as E1's coverage sidecar `{assigned, observed}` (10 Unit 4) but the link is not drawn. Both items are carried only as value-ledger rows. | 13 line 119, 157, 255; research/24 rows VL-24-413 and VL-24-422; 10 Unit 4. The gap is logged in 13 gap 5, so this is not an unacknowledged gap. | In synthesis, add "partition by assigned slice" and "upstream verdict as input" to the rf-qa module requirements and tie the first to the coverage sidecar. |
| M5 | MINOR | N | 13 section 8 row M12 | "A panel fan-out cannot be started from inside a subagent (pr-submit's rule applies to any caller)" generalises pr-submit's own activation rule (SKILL.md l.47-49, about its FSM) to any panel caller. No evidence in 13 supports the generalisation. | 13 lines 67, 225. | Phrase M12 as a constraint of pr-submit as a caller, or cite the Claude Code subagent documentation if the broader claim is meant. |
| M6 | MINOR | N | 15 section 7 and Summary | The 9 manifests with no `dispatched` attempts are called "a protocol omission ... not a race". I confirmed the 9 manifests and that each lists `dispatched` in `stages`, which fits the stage-rule reading (`record_attempt` refuses once the stage is committed). The corroboration is a memory lesson (slice 11 line 58) that 15 itself says it did not re-read, and a lost update could also remove `dispatched` rows. | 15 line 163; manifest scan above. | Say "consistent with" instead of "explained by ... not a race"; D-23 is already correctly kept as a latent hazard. |
| M7 | MINOR | N | 15 section 6.2 item 4 | "One wrong lesson already lives in it" restates a [CODE-CONTRADICTED] AMBIGUITIES row (memory line 64) as a fact, tagged only "[UNVERIFIED by me]". Slice 11 G-2 says the lesson may reflect an older installed CLI. I confirmed `cluster_cmd.py:27-34` handles fenced yaml at HEAD, so the contradiction holds against current code only. | 15 line 156; scope/11 G-2; cluster_cmd.py:27-34. | Say "contradicted by current code (cluster_cmd.py:27-34); true of an older CLI is not excluded". |
| M8 | MINOR | N | 14 Stale Documentation row 5 versus 12 last Stale Documentation bullet | The two files explain the slice 12 "15 modules, 5131 lines" figure differently. 14 says the slice list omits `telemetry_cmd.py` (98 lines), but omitting a module would lower the total below 5,086, not raise it to 5,131. 12 says the count is consistent (16 including `__init__.py`) and totals were not re-derived. My `wc -l` gives 16 files, 5,086 lines. | 14 line 266; 12 line 226; wc output. | State only that 5,131 does not equal 5,086 and drop the omission explanation. |
| M9 | MINOR | N | 16 Part 4.1 row 6 and Part 6 | The held-out and independence analysis covers E1 versus E2 only. It lists the process-redesign hold-outs HO-1..HO-6 as held-out without noting that HO-5, the only spec hold-out, is E3's tuning spec (slice 06 Q8; 14 section 5 row s7 shows both E3 families use the same S1 spec). The caveat exists only in ledger rows VL-21-986/1287/1683. | 16 lines 132, 137; 14 line 146; research/21 rows named. | Add one sentence to 16 Part 4.1 row 6 that HO-5 is contaminated by E3 tuning, so spec-module generality has no clean hold-out. |
| M10 | MINOR | N | 11 gap 1; 13 gap 9 | 11 does not determine which tier `--depth standard --tier auto` selects for Stage 10.5 phases (reflect SKILL section 5, not read), so how many consumer runs can reach a panel at all stays unanswered although it decides where a panel plugs in. 13 gap 9 lists candidate reviewers not read but omits `sc-roadmap-protocol`, `sc-issue-protocol` and `cli/roadmap`, which slice 12 gap 3 names. Both are logged. | 11 line 165; 13 line 259; scope/12 gap 3. | Resolve in file 06 or synthesis; add the three names to the 13 gap list. |
| M11 | MINOR | N | 12 section 2.2 row V8 versus section 8 E-b; 12 count paragraph | V8 is tagged "[UNVERIFIED here: findings_v2.py ... not re-read]" while E-b cites `findings_v2.py:155-162` from a read in the same file. The severity-vocabulary count also omits the `reflect-reviewer` HIGH/MEDIUM/LOW table and the `auggie-reviewer` lower-case `severity_hint` that 13 section 2.2 documents. | 12 lines 64, 187; 13 lines 98, 105. | Re-tag V8 as read; add the two code-reviewer dialects to the synthesis vocabulary table. |
| M12 | MINOR | N | 15 section 8.5 | Confidence in the run-record split is stated "moderate-high" although its load-bearing input (a transcript adapter that supplies per-agent usage and observed model for every harness) is unverified (15 gap 3, question 8). | 15 lines 199, 230, 235. | Use "moderate" until the adapter is shown for at least the two harnesses in the repo. |
| M13 | MINOR | N | 12 Stale Documentation (last two bullets) | Line totals of the slices are called "not re-derived" while the same file reports counts for cli/review it did derive; a one-line `wc` would settle it (see M8). | 12 line 226. | Fold into the M8 fix. |

## Summary

- Files reviewed: 8 research files (09-16) plus research-notes.md; all 12 slice Gaps sections cross-checked.
- Checks passed: 7 / 7 (items 4, 5, 6, 7 pass with minor notes).
- Blocking findings: 0. Minor findings (notes only): 13 (M1-M13).
- Factual verification: about 35 independent checks against HEAD code, recorded run data and the E2 tip; every number and citation I re-derived matched the file that stated it. No fabricated, circular or contradicted claim was found in the assigned files.
- Distinguishing observation for the gate: the research is deep and unusually honest about its own limits; its weaknesses are cross-file seams (M3, M4, M9, M11) that synthesis should close, not defects inside a file.

## Overall Verdict: PASS (with notes; zero blocking findings)

## Self-Audit

1. Factual claims independently verified: about 35 (list under "Independent verification performed").
2. Files read to verify: the eight research files, research-notes.md, 12 slice Gaps sections, and code and data at HEAD (findings_v2.py, findings.py, ledger.py, cluster_cmd.py, fsm.py, loop_guard.py, panel.py, contract.py, telemetry.py, runner.py, install_skills.py, swarm lenses, spec-panel.md, tasklist and reflect SKILL.md, manifests, coverage/precheck JSON, results.jsonl, the installed ledger script) plus E2-tip blobs through `git show`.
3. Why a PASS with no blocking item can be trusted: I tried to break the claims most likely to be wrong (exact counts, line citations, "absent" claims, contradiction claims between files) and all matched; the minor list shows where I found real seams (for example M8 is a numeric inconsistency between two files, M3 a cross-file omission).
4. Web research: none performed; no Tavily or fallback call was needed (14's documentation claim was left unverified and is listed above).
5. Inherited Structural Verdict: none was supplied in my prompt; standalone mode, so no reliance entries. (a) Reliance list: none. (b) Independent semantic checks: items 1-14 above.

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (item-level; the limits on what I did not re-derive are listed above)
**Tool engagement:** Read: 28 | Grep: 12 | Glob: 2 | Bash: 10 (Read + Grep + Glob = 42, above the 7 checklist items)

Status: Complete
