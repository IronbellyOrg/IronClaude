# Synthesis Source-Tracing Review (Partition 1 of 2)

**Analysis type:** synthesis-review (source tracing, checklist items 6-10)
**Date:** 2026-11-07
**Task:** TASK-RESEARCH-orchestrator-supervision-20261107-073942 (issue #339, orchestrator mode Phase 1)
**Assigned synthesis files:** `synthesis/synth-01-problem-current-state.md`, `synthesis/synth-02-target-gaps.md`, `synthesis/synth-03-external-findings.md`
**Research sources read (inputs of Steps 5.1-5.3):** `research/scope-01-contract.md`, `research/scope-02-orca-recovery.md`, `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`, `research/05-orca-row-schema.md`, `research/06-orca-open-questions.md`, `gaps-and-questions.md`, `research/web-01-agent-supervisor-session-health.md`, `research/web-02-static-status-report-conventions.md` (plus `research/07-gate-gap-fill.md` and `qa/qa-nb4-fix-log.md` for the NB-4 re-check)
**Fix authorization:** false (report only; no synthesis or research file edited)
**Severity rule:** CRITICAL and IMPORTANT block; MINOR are notes.

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports.]

## Integrity baseline (sha256 of synthesis files at start of review)

| File | sha256 |
|---|---|
| synth-01-problem-current-state.md | 3dcdfc7774b71f7651c1984c991a4916484c19b4beb256670a505d338048db9f |
| synth-02-target-gaps.md | e2ebb96d1c782205ee6a1ba0ba18cff60263ff5f0fa693ed7e602eba3f0bca9f |
| synth-03-external-findings.md | 01e6435fb838a84bdebdea889e97e5e319646cd2c09fedd5bea4ed19d5905e53 |

---

## NB-4 re-check (executor extra 1)

Source state: `research/scope-03-cli-patterns.md:99` (mtime 20:22) now allows `orchestration task-list` (`--ready`, `--run`), `run-list`, `run-current` and `gate-list`. Its forbidden list keeps `inbox` (with the [UNVERIFIED] read-marking reason), `--ack`, `--wait`, `--unread`, `check --format`, `reply`, `ask`, `send` and `worktree ps --agent-wait`. `gaps-and-questions.md:26` marks GQ-03 resolved.

Grep of all six synthesis files for `allowlist|inbox|task-list|run-list|run-current|gate-list`:

| File | Locations | Corrected allowlist? | Old-allowlist text? |
|---|---|---|---|
| synth-01 | `:7`, `:185-201` (table), `:255-267` (diagram), `:281` | Yes: the four verbs allowed, `inbox` forbidden | None. `:201` carries a stale count claim, see F1 |
| synth-02 | `:7`, `:26-28`, `:112` (SC-2), `:132`, `:189`, `:230` | Yes | None |
| synth-03 | no allowlist text (external findings only) | N/A | None |
| synth-04 (partition 2, read-only grep) | `:18`, `:34` (K-5), `:62`, `:198`, `:219`, `:259` | Yes | None |
| synth-05 (partition 2, read-only grep) | `:9`, `:157`, `:166`, `:220-221`, `:289` | Yes | None |
| synth-06 (partition 2, read-only grep) | `:11`, `:57`, `:67`, `:83` | Yes | None |

**Result: NB-4 PASS.** No synthesis text uses the old allowlist. Every file that names the allowlist carries the four plain-read verbs and keeps `inbox` forbidden. The bare `worker-list`/`worker-show`/`worker-read` spelling at `scope-03:99` (GQ-85) is handled by SC-3 (synth-02:113) and X-5 (synth-04:219).

---

## Findings

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| F1 | IMPORTANT (blocking) | `synth-01-problem-current-state.md:201` | States that `gaps-and-questions.md:125` reads "Open: 76. Resolved: 24" and that the counts "predate the fix and are off by one". The source line now reads "Open: 75. Resolved: 25 ... Open blocking QA finding: none" (gaps file mtime 20:23 predates synth-01 mtime 20:33). synth-02:7 and synth-02:230 correctly say 75/25, so Section 2 and Sections 3/4 contradict each other (check 7) and synth-01 misquotes its source. | Rewrite synth-01:201 to say the summary line reads Open 75 / Resolved 25 with no open blocking QA finding; drop the "off by one" sentence. |
| F2 | IMPORTANT (blocking) | `synth-02-target-gaps.md:172` (R-2) versus `:182` (G2), `:185` (G5), `:187` (G7) | R-2 names "WC-14 and its clauses (G1, G2, G5, G7)" as unwired in-scope capabilities rated Critical, unconditionally. The 4.2 rows rate G2 and G5 "Important (N-32); Critical under R-2 if WC-14 ships without it" and G7 "Important (N-32)", while G1 (`:181`) and G4 (`:184`) are rated Critical under the same rule. The severity rule and the gap table disagree, so Section 8 cannot tell which rows block (check 7). | Either rate G2, G5 and G7 Critical (R-2) and keep N-32 as a source note, or narrow R-2's clause list to the rows the table rates Critical and state why G2/G5/G7 are exempt (for G7, only the directory is a decision). |
| F3 | MINOR | `synth-01-problem-current-state.md:79`, `:89`, `:98` versus `:288-294` | Section 2 states guide-only facts: the `unverifiable`/`exited` verdict values (`:79`), the guide's row fields (`:89`) and the guide's null-`agentWait` meaning (`:98`). They carry [UNVERIFIED] tags and GQ routes, but `:288-290` says guide-only Orca statements are excluded from Section 2 (check 8). | Move them to the Open Questions inputs, or reword `:288-290` to say guide-only statements appear in Section 2 only with an [UNVERIFIED] tag and a GQ route. |
| F4 | MINOR | `synth-01-problem-current-state.md:187-193` | The forbidden column omits `check --format` and the single-read-mode rule (more than one of `--unread`/`--peek`/`--all` is rejected) that `scope-03:99` and synth-02 SC-2 (`:112`) include. | Add `check --format` and the single-read-mode rule to the forbidden column. |
| F5 | MINOR | `synth-01-problem-current-state.md:15` | Lists "fenced" among the classes without pointing to the six-versus-seven class contradiction that synth-02 §4.8 records (synth-02:184 "Six classes versus seven: section 4.8"). | Add a pointer to synth-02 §4.8 where the class list first appears. |
| F6 | MINOR | `synth-02-target-gaps.md:144` and `:243` (C4) | "`~/workspace/` paths where this host uses `~/workspaces/` (`:25-27`)" and "This host uses `~/workspaces/` (`SKILL.md:25-27`)". `sc-crash-recovery/SKILL.md:25-27` shows the skill's own `~/workspace/` path and the 72 h default, not the host layout; the host layout comes from `scope-02:241`. The citation supports the other half of the sentence. | Cite `SKILL.md:25-27` for `~/workspace/` and `scope-02:241` for the host's `~/workspaces/worktrees/` layout. |
| F7 | MINOR | `synth-02-target-gaps.md:16`, `:211` | Section 3.1 states option A1 as the target while GQ-60 (where the logic lives) is still "Open, leaning A1" (`:211`). The target reads as decided. [PARTITION NOTE: whether synth-04 §7 recommends A1 is a cross-partition check.] | Label A1 in 3.1 as the recommended option pending GQ-60, or cite the synth-04 recommendation. |
| F8 | MINOR | `synth-03-external-findings.md:167-174` | The D-table extends web-01's D1-D4 (`web-01:179-184`) with D5 (Grafana, `web-02:30`) and D6 (agents-fleet, `web-01:159`). Both trace to research, but the table reuses web-01's numbering without saying D5/D6 were added in synthesis. | Add one line: "D5 and D6 added from web-02:30 and web-01:159". |

**Spot-checks that passed (no finding):**

- synth-02:105 "Orca unavailable" banner and `orca-capabilities.md:39`: traced to `scope-02:115` and `research-notes.md:182`.
- synth-02:119 (SC-9) "web-02 recommendation 1": `web-02:57` (print the real observation time).
- synth-02:152 Camunda / 6 h window: `web-01:195` (finding 4) and `:205` (recommendation 4).
- synth-03 §5.9 C2 (50 s versus 40 s): `web-01:133`. C1 (Icinga versus Nagios timeouts): `web-02:23` and `web-01:147`.
- synth-03 `orca-capabilities.md` lines 112, 122-125 and 130 "as cited by web-01": `web-01:17-19`, `:74`, `:81`, `:88`, `:118`.
- synth-03 Relevance values and URLs for Statuspage, SRE, I-PASS, PagerDuty/GitLab, Kanban and GitHub CLI match `web-02:17-45`; the LOW product-doc sources match `web-01:159`, `:228-229`.
- scope-04's three [CODE-CONTRADICTED] findings (`scope-04:374`) all reach synth-02: sort (C6), wide-view omission count (C7, `:246`) and the "Not read" generated-files claim (`:254`).

---

## Per-File Review (checklist items 6-10)

### synth-01-problem-current-state.md (Sections 1, 2)
**Verdict:** FAIL (1 blocking: F1)

| Check # | Check | Result | Evidence/Issue |
|---|---|---|---|
| 6 | Implementation steps name files | N/A | Sections 1-2 hold no implementation steps. The registry list (`:212-217`) names files. |
| 7 | Cross-references consistent | FAIL | F1: `:201` quotes stale 76/24 counts; synth-02:7, :230 say 75/25. F5 (minor): class list lacks the §4.8 pointer. |
| 8 | No doc-only claims in Section 2 | PASS with note | Guide text is tagged [UNVERIFIED] and routed to GQ items, but contradicts the `:288-290` exclusion note (F3, minor). Code-backed rows cite handler/test lines (`:189-193`, `:281`). |
| 9 | CC / STALE DOC surfaced | PASS | Section 2 marks the crash-recovery (`:283`) and #409 (`:241`, `:286`) contradictions; Section 4 rows live in synth-02 (C1-C15, S-01 to S-14). |
| 10 | Key Takeaway coverage | PASS | scope-01 to scope-04, 05 and 06 summaries map to §2.1-2.6 and the `:281-286` table (envelope-only paging from 05, `check` consuming from 06, #409 header/ledger/brief from scope-04:367-373, crash-recovery reuse limits from scope-02:239-241). |

### synth-02-target-gaps.md (Sections 3, 4)
**Verdict:** FAIL (1 blocking: F2)

| Check # | Check | Result | Evidence/Issue |
|---|---|---|---|
| 6 | Implementation steps name files | PASS | Target and SC rows name files: `commands/sweep.md`, `sc-sweep-protocol/SKILL.md` (`:16`), `main.py:559-561` (`:120`), `test_routing_refresh.py:33` and others (`:121`), `tests/cli/reflect/test_contract_status_cli.py:44-66` (`:111`). |
| 7 | Cross-references consistent | FAIL | F2: R-2 (`:172`) versus G2/G5/G7 ratings (`:182`, `:185`, `:187`). Gap IDs G-A, G-B, G1-G7 and K1-K4 all reach synth-05 steps or its "Gaps sent to Open Questions" (synth-05:130-145, :191) [PARTITION NOTE]. F7 (minor). |
| 8 | No doc-only claims in Section 2 | N/A | Not Section 2. Section 3 targets cite research and code. |
| 9 | CC / STALE DOC surfaced | PASS | C1-C7, C9, C13 residual, scope-02:146/:165, scope-01:100, scope-03:108/:111/:165, scope-04:33, 06:63/:85/:144 and S-01 to S-14 all appear in §4.6/§4.7. F6 (minor) is a citation slip inside C4. |
| 10 | Key Takeaway coverage | PASS | web-01 findings 4 and recommendations 1-4 feed §3 (Camunda `:152`); web-02 recommendation 1 feeds SC-9 (`:119`); scope-04 omission and sort CC feed C6/C7 and SC-8. |

### synth-03-external-findings.md (Section 5)
**Verdict:** PASS (MINOR F8 only)

| Check # | Check | Result | Evidence/Issue |
|---|---|---|---|
| 6 | Implementation steps name files | N/A | External findings; R1-R9 are statements for the plan, not steps. |
| 7 | Cross-references consistent | PASS | Each finding carries a source URL, Relevance and WC-10 mapping that match web-01 and web-02. D1-D6 and C1-C2 trace to `web-01:133`, `:147`, `:159`, `:179-184` and `web-02:23`, `:30`. F8 (minor) on D-table numbering. |
| 8 | No doc-only claims in Section 2 | N/A | Not Section 2. |
| 9 | CC / STALE DOC surfaced | PASS | Rejected option A4 is kept [CODE-CONTRADICTED] (`:185`); external contradictions are tabled in §5.9. |
| 10 | Key Takeaway coverage | PASS | §5.10 maps all 7 web-01 Key External Findings (`web-01:192-198`) and all 6 web-02 findings (`web-02:49-54`). R1-R4 and L1-L2 match web-01 recommendations 1-6 (`:202-207`); R5-R9 match web-02 recommendations (`:57-63`). No exclusion. |

---

## Integrity check (end of review)

sha256 of synth-01, synth-02 and synth-03 re-run after writing this report: identical to the baseline. No synthesis or research file was edited.

## Summary

- Files reviewed: 3 (partition 1 of 2)
- Files passed: 1 (synth-03)
- Files failed: 2 (synth-01, synth-02)
- Total findings: 8 (CRITICAL 0, IMPORTANT 2, MINOR 6)
- Blocking findings: 2 (F1, F2)
- NB-4 re-check: PASS (corrected allowlist in every synthesis file; no old-allowlist text; `inbox` still forbidden)

## Verdict: FAIL

