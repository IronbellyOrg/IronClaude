# QA Report — Synthesis Gate, content-quality lens (Partition 2 of 2)

**Topic:** Orchestrator mode Phase 1 (issue #339), read-only coordinator `/sc:sweep`
**Date:** 2026-11-07
**Phase:** synthesis-gate (content-quality lens, checklist items 7-12)
**Fix cycle:** N/A
**Fix authorization:** false (report only; no synthesis file modified)
**Assigned files:** `synthesis/synth-04-options-recommendation.md`, `synthesis/synth-05-implementation-plan.md`, `synthesis/synth-06-questions-evidence.md`
**Extra check ordered by the coordinator:** NB-4 re-check (corrected Orca read allowlist: `task-list`, `run-list`, `run-current`, `gate-list` allowed; `inbox` forbidden)

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

Pre-review md5 of the assigned files (to prove no modification):

- synth-04 `80717655259a0047bd8234a1e3b4fb04`
- synth-05 `e4236cd49b616f17622fe88aa1191b22`
- synth-06 `ccbb50b1a4dfc3c4ecf11ca976a89619`

---

## Work log (incremental)

- synth-04 read in full (275 lines). `qa/qa-nb4-fix-log.md` read in full.
- synth-05 read in full (309 lines, two parts). synth-06 read in full (231 lines).
- `research/scope-03-cli-patterns.md:99` read: NB-4 allowlist present, `inbox` forbidden with reason.
- `gaps-and-questions.md` status column counted with awk: 24 rows `resolved` + 1 `resolved (for one worker)` = 25; open variants = 75. Line 125 now reads "Open: 75. Resolved: 25".
- Three batched Bash scripts checked ~60 cited paths for existence and ~45 cited line ranges (main.py, WORKER-CONTRACT.md, test_worker_contract.py, test_routing_refresh.py, HOW-WE-WORK.md, test_how_we_work_routing_table.py, test_routing_plugin_parity.py, commands.md, Makefile, contracts/__init__.py, sc-crash-recovery SKILL.md and refs/report-template.md, sc-issue-command.md, recommend/__init__.py, reflect/contract.py, reflect/config.py, tests/cli/reflect/conftest.py, sc-reflect-protocol, swarm-wizard SKILL.md, pragmatic.md, ccsession, pyproject.toml, core/CLAUDE.md, test_model_alias_policy.py, test_graph_command.py, test_orca_session_launch_guidance.py, Orca handler directory, commit 495eb96d).
- Grep of synth-04/05/06 for X-6, `include-remote`, every GQ id in Section 8.1/8.2 and Section 9, `exited`, `report-template`, stale "not yet written" text.
- md5 re-checked at the end: all three synthesis files unchanged.

## NB-4 re-check (coordinator's extra check)

**Result: PASS.** The corrected allowlist (`worker-list`, `worker-show`, `worker-read`, `worktree ps` without `--agent-wait`, and `orchestration` `task-list`, `run-list`, `run-current`, `gate-list`; `inbox` forbidden) appears in synth-04 (`:18`, K-5 `:34`, diagram `:62`), synth-05 (`:9`, step 1.4 `:62`, step 1.6 `:64`) and synth-06 (`:11`, rows 29, 39, 55). No synthesis text lists any of the four plain-read verbs as forbidden, and no text allows `inbox`. No old-allowlist text remains.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | synth-04 `:220` (X-6) | False claim. Says `gaps-and-questions.md:125` "still says 'Open: 76. Resolved: 24' with GQ-03 open ... counts are off by one". Line 125 now reads "Row count: 100 rows. Open: 75. Resolved: 25 (GQ-03, ...)", and an awk count of the status column agrees (25 resolved). synth-06 `:13` and `:226` already use 75/25, so the three files contradict each other. | Delete X-6, or rewrite it as "resolved: gaps:125 was corrected to 75/25 after the NB-4 fix". |
| 2 | IMPORTANT | synth-05 `:260` (X-6) | Same stale claim ("Stale gap count at `gaps-and-questions.md:125`"). It also says the stale text was "sent to Open Questions (C2)", but C2 is the routing-table test length (`gaps-and-questions.md:171`, synth-06 row 89), not the gap count. Neither synth-05 8.2 nor synth-06 Section 9 has a gap-count row. | Delete X-6, or mark it resolved and drop the C2 mapping. |
| 3 | IMPORTANT | synth-06 `:45` row 17 vs synth-04 `:60`, synth-05 step 1.4 `:62` | GQ-22 conflict. Section 9 says "Measure once; keep [`--include-remote`] off by default". The plan's probe and the option diagram call `worker-list --run <id> --include-remote --json` on every sweep. One of them is wrong behaviour: remote rows read `unverifiable` without the flag (`05-orca-row-schema.md:48`, `:87`). | Make the two agree. The plan's default (flag on, so remote rows are not falsely unverifiable) is better evidenced; change row 17 to "on by default; measure its cost once". |
| 4 | IMPORTANT | synth-06 Section 9 rows 8, 9, 27, 28, 51 vs synth-05 Section 8 (`:90`, `:138`, `:153`, `:159`, `:198`, `:223`) | Section 9 resolutions contradict Section 8 decisions. (a) GQ-10 row 8 "Owner decision" vs plan G7 fixes a dated `--output` file under `.dev/` (`:138`). (b) GQ-11 row 9 "Owner decision" vs step 1.17 "GQ-11 decided as WC-14" (`:90`, `:158`); `gaps-and-questions.md` still marks GQ-11 open (owner decision), so synth-05 overstates it. (c) GQ-32 row 27 "Print the window and the Run ids" vs plan "root scope line" (`:159`). (d) GQ-33 row 28 "Print the omission count" vs plan "list everything" (`:159`). (e) GQ-61 row 51 resolves to "6 h" while synth-05 `:153`, `:198`, `:223` and the gaps file call it an open owner decision. | For each id, pick one answer. Where the plan decides (GQ-32, GQ-33), drop the row from Section 9 or make it match. Where it is an owner decision (GQ-10, GQ-11, GQ-61), make synth-05 say "default pending owner decision" and make synth-06 stop pre-deciding 6 h. |
| 5 | IMPORTANT | synth-06 `:77` row 49 (GQ-59) | Unsupported resolution. Row 49 calls GQ-59 a "runtime-version probe" and resolves it with "Add a version probe to the header". The gaps file and synth-05 (`:150`, `:197`) treat GQ-59 as a `--peek` / `--all` / `compatibilityAck` side-effect question gated behind a runtime-handler read, and research found no read-only version verb. The resolution names a probe that the evidence says does not exist. | Rewrite row 49 to match the gaps file: "runtime-handler read or throwaway-Run probe before trusting `--peek`; until then contracts-only default". |
| 6 | IMPORTANT | synth-05 step 1.3 `:61` vs plan header `:12` (checklist item 8) | Section 8 uses a doc-only value as architecture. Rule 2 classifies a row as "stalled (proved)" on `liveness.verdict` `exited`. `exited` is guide text only (`05-orca-row-schema.md:42`, `:63`, both [UNVERIFIED]) and was never captured (GQ-37; synth-05 `:146`, `:195`). The plan header says [UNVERIFIED] items "appear in a step only as 'treated as could not determine' or 'forbidden'", so rule 2 breaks the plan's own rule. | Either tag rule 2's `exited` branch [UNVERIFIED] and make it fall back to could not determine until a stalled-row capture exists (GQ-37), or change the header convention to name this exception with its evidence. |
| 7 | MINOR | synth-06 rows 18, 22, 24, 26 (GQ-23, GQ-27, GQ-29, GQ-31) | Open Questions answered elsewhere (item 7). Section 8 decides lazy export (1.1), `probes.py` seam (1.4), tie-break by ID and all-source coverage (`:159`). The Section 9 rows give compatible but vaguer answers ("pick one precedent"). | Mark these rows "decided in step N" or remove them from Section 9. |
| 8 | MINOR | synth-04 `:117`, `:170`; synth-05 step 1.15 | Path citation. `report-template.md` is listed beside `scripts/bootstrap_scan.sh` as if at the skill root. The file is `src/superclaude/skills/sc-crash-recovery/refs/report-template.md`; its "What I could not determine" section is at `:127-129`, so the cited claim is true. | Write `refs/report-template.md`. |
| 9 | MINOR | synth-06 row 21 vs synth-05 step 1.15 | `allowed-tools` uses the colon form `Bash(superclaude sweep:*)` in row 21 and the space form in synth-05 and GQ-26. Step 1.16 pins both forms, so behaviour is unaffected. | Use one form in prose. |
| 10 | MINOR | synth-06 row 33 vs synth-05 step 1.5 | Truncation wording differs ("message listing truncated at 100" vs "at least 100 (truncated at 100), total could not determine"), and they describe different sources (messages vs worker rows). | Align the strings and name the source. |
| 11 | MINOR | synth-06 row 58 (GQ-84) | "Apply rule 2 before rule 7" is ambiguous. synth-05 states the correct rule: exited + no `worker_done` + unreadable transcript -> could not determine. | Copy the synth-05 wording. |
| 12 | MINOR | synth-06 row 63 (GQ-99) | "Batch where the policy allows" vs synth-05's per-sweep call bound. | Restate as the plan's call bound. |
| 13 | MINOR | synth-06 `:221`, `:230` | Stale evidence trail: synth-05 is listed as "planned; not yet written", and `qa/` is listed as "24 files"; both are out of date now. | Update at assembly. |

## Overall Verdict: FAIL

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 7 | Cross-section consistency | FAIL | Every Section 4 gap maps to a step (synth-05 8.1 mapping table `:136-160`). But issues 1-5 are contradictions between the three files and the gaps file, and issue 7 lists Open Questions answered in Section 8. Options cite Section 2 evidence (synth-04 criteria tables cite code lines that were checked). |
| 8 | No doc-only claims in Sections 6-8 | FAIL | Issue 6 (rule 2 relies on guide-only `exited`). Other guide-only values (`unverifiable`, null `agentWait`) appear only as could not determine, per the header. synth-04 options mark guide-only facts [UNVERIFIED]. |
| 9 | Stale docs surfaced | PASS | S-01 to S-14 are in synth-06 9.3. The CC claims (C2, C3, C5-C7, C10, C11, C13, C15) are in 9.2 and 9.4 or in GQ rows. |
| 10 | Content rules | PASS | Tables throughout, ASCII diagrams in synth-04 (`:55-70`), no reproduced source code, evidence inline. Long single-cell prose in synth-05 1.3-1.5 hurts readability (note only). |
| 11 | No placeholders | PASS (note) | No TBD/TODO. synth-04's `<sweep script>` placeholders describe options and synth-05 names them. Issue 13 is stale trail text, not a placeholder. |
| 12 | No hallucinated paths | PASS (note) | All cited existing files exist. All `(new)` parents exist (`cli/`, `commands/`, `skills/`, `tests/`). About 45 cited line ranges match. Only miss: issue 8 (`refs/` prefix dropped; content true). |
| NB-4 | Corrected allowlist | PASS | See NB-4 section. |

## Summary

- Checks passed: 5 / 7 (including NB-4)
- Checks failed: 2 (items 7 and 8)
- Blocking issues: 6 (IMPORTANT: 1-6; CRITICAL: 0)
- Minor issues (notes): 7 (issues 7-13)
- Issues fixed in-place: 0 (fix authorization false; md5 of all three synthesis files unchanged at the end)

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 9 | Grep: 2 | Glob: 0 | Bash: 6 (three batched inspection scripts plus targeted checks; no web research)

## Recommendations

- Fix issues 1-6 in the synthesis files before assembly. Issues 1 and 2 are deletions. Issues 3-5 need one answer per GQ id across synth-05 and synth-06. Issue 6 needs a decision on whether `exited` stays a positive stall signal before GQ-37's capture.
- Fold the minor notes into the same edit pass where convenient. They do not block.
- At merge, check partition 1's findings on synth-01 to synth-03 against issue 4: the scope-line and window decisions may also appear there.

## QA Complete

## Verdict: FAIL
