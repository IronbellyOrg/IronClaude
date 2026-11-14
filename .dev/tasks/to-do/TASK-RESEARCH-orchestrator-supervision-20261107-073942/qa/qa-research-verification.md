# QA Report — Research Gate Fix-Cycle Verification (Agent 1, rf-qa)

**Topic:** Orchestrator mode Phase 1 (issue #339), research gate
**Date:** 2026-11-07
**Phase:** fix-cycle
**Fix cycle:** 1
**Fix authorization:** false (no research file edited)
**Inputs:** `qa/qa-consolidated-findings-phase3.md` (|F_0| = 28), `qa/qa-research-fix-log.md`, every file in `research/` including the new `research/07-gate-gap-fill.md`

Status: COMPLETE (written incrementally)

## Overall Verdict: PASS

---

## Per-finding verification (B-01 to B-28)

| ID | Status | Evidence |
|----|--------|----------|
| B-01 | RESOLVED | `research-notes.md:188` declares Section C the one canonical vocabulary and precedence (rules 1-7; idle only for person-started sessions); `05-orca-row-schema.md:167-180` gives the Orca half per Section C class and withdraws the old idle row; `scope-02-orca-recovery.md:99-109` marks the five draft bullets superseded; C14 (`research-notes.md:332`) records the resolution. Blocked contract is now only "waiting on a person" (rule 1); finished needs the contract read (rule 6). |
| B-02 | RESOLVED (note) | Section C defines safe to close as a separate two-part REVIEW dimension (terminal releasable / worktree removable); `scope-02:103`, `:237` match; `lc17-show-1.json:145-166` confirms `reclaimable` + `release` + attention `failure` on an unread result. Residual MINOR: `scope-01-contract.md:64` still says "A 'safe to close' **class**" (substance = the worktree-removable part, so wording only). |
| B-03 | RESOLVED | `research-notes.md:331` C13 CODE-VERIFIED; data-sources table uses `orca-ide orchestration <verb>`; `scope-02:16`, `:235-236` mark the bare form CODE-CONTRADICTED and give the correct form; `scope-02:223-224` OQ1/OQ2 answered with pointers to 05; `scope-01:142` OQ1 answered. |
| B-04 | RESOLVED | `07-gate-gap-fill.md` Section A covers `pragmatic.md` (`:22`, `:53`, no exception mechanism) and `launch-job-identity.sh` (no env vars; identity file under `~/.claude/state/launch-level/sessions/<id>`); S3 rows `research-notes.md:94-95` updated. |
| B-05 | RESOLVED | Section C rules 2-3 (stalled only with the turn proved final; fenced is its own class); `scope-02:86` stall-proof row and `:157` (parser cannot prove finality, cites `parse_session_log.py:45-55, :85-102`); `scope-01:62` item 7; 05 Answer (2). |
| B-06 | RESOLVED | 05 `:71`, Gap 8, stale-doc bullet; `scope-01:58` item 3 records guide `[G]` 130-131 vs `orca-capabilities.md:97-102` vs WC-8/WC-13; C15 (`research-notes.md:333`) open contradiction with a sweep rule (non-null `parent` = WC-13 violation for review); `lc16-show-4.json:115` `"parent": null` confirmed by sed. |
| B-07 | RESOLVED | `07-gate-gap-fill.md:39-49` Section B; every handler citation re-read this pass: `run-handlers.js:28-34` (`runCurrent`), `:35-48` (`runList`, limit + cursor), `orchestration-run-pagination.js:4` (=100), `task-handlers.js:10-17` (6 statuses), `:32-44` (plain `client.call`), `gate-handlers.js:26-37`, `worker-list-run-scope.js:8-24` with comment `:21`, `mutation-request.js:9`. `scope-02:119` points to it. |
| B-08 | RESOLVED (documentation fix) | No populated `worker-list` row exists (`lc01-step7.txt:28` `"workers": []`, re-checked); 05 Gap 1 and `scope-02:120`, `:223` state row shape UNVERIFIED and make one `worker-show` per row the default with worst case ceil(N/100) + N calls. A live capture is outside this read-only pass; the required fix (state the gap and the conservative cost) is applied. |
| B-09 | RESOLVED | `07-gate-gap-fill.md` Section D and C12: `lc16-show-4.json:11` `assigneeHandle` `term_1a6fde09-...`, `:12` `assigneePaneKey` `ec61f494-...:2844c731-...`; the orca-tabs file `ec61f494-038b-4c5b-a2b2-13e3139342e8+2844c731-8cec-4dee-aa0b-63ff3baac732` exists with 3 lines, line 3 = the handle. `scope-01:56`, G6 `:83`, Q7 `:148` record the evidence route and keep "at all" as an owner decision for WC-14 (the finding allowed "decide in WC-14"). |
| B-10 | RESOLVED | 06 Gap 19 (`:176`) records the help-vs-guide conflict as open; split rule at `:137` (null = no wait observed, valid for working, never stall proof; absent = could not determine); `:144` re-tagged [CODE-CONTRADICTED by help] / [CODE-VERIFIED by guide]. Matches Section C rule 5. |
| B-11 | RESOLVED | Section C rule 4 splits waiting on a person into (a) explicit question and (b) frozen or blocked by policy; `scope-04:285-286` skeleton rows and `:318` precedence follow it; citations re-read (`WORKER-CONTRACT.md:129`, `:133-136`; `agent_focus.py:168` via `git show 495eb96d`). |
| B-12 | RESOLVED (note) | `scope-04` skeleton gains a derived Class column; precedence `:320`, per-source table `:324-330`, view mapping `:332`. Residual MINOR: skeleton "Retained problems" `:290` omits stalled / could not determine although `:332` places them there; `:320` maps a stale row to could not determine where Section C rule 6 makes a settled stale row with a contract "finished" (edge nuance, rule 6 governs). |
| B-13 | RESOLVED | `scope-03:99` keeps the local-write proof (pattern re-read: `tests/cli/reflect/test_contract_status_cli.py:44-66` `side_effect=AssertionError`, docstring `:18-22` `isolated_filesystem()`) and adds the required second test: one `_orca(*args)` seam modelled on `reflect/config.py:64-78` (re-read: `subprocess.run([...], check=True, timeout=10)`), patched with an argv allowlist (peek-only `check`, `worker-list/-show/-read`, `worktree ps` without `--agent-wait`) and an explicit forbidden list (`--ack`, `--wait`, `--unread`, plain `check`, `reply`, `ask`, `send`, `inbox`, `--agent-wait`, any unlisted verb). `message-check-handler.js:17` citation re-verified earlier this pass. |
| B-14 | RESOLVED | `scope-04:293` skeleton columns include Approval, Evidence and Tests/review; per-column sources `:336-351`; the formerly CODE-VERIFIED skeleton line is re-tagged "Partly verified" (`:312`). |
| B-15 | RESOLVED | 06 `:108`, `:127` and Gaps 10-11 re-read; claims match `message-check-handler.js:30`, `:33-34`, `:58-71`. |
| B-16 | RESOLVED | 06 `:39` and Gaps 5-6 re-read against `message-inbox-handlers.js:20-25`, `:32`. |
| B-17 | RESOLVED | 06 Gap 17 `:174`, tagged `:74`, G-B answer `:77` (no read path for a pending `ask`), contracts fallback stated. `question-handler.js:61-68` re-read. |
| B-18 | RESOLVED | 06 `:73` and Gap 7 re-read; consistent with `orchestration-check-output.js:49-59`. |
| B-19 | RESOLVED (note) | `scope-03:208` OQ3 now decides the call form: bare `superclaude sweep ...` on PATH first (precedent `sc-reflect-protocol/SKILL.md:63-64`, re-read: `superclaude reflect contract-status ...`), `uv run superclaude sweep ...` only as dev-checkout fallback; both in `allowed-tools`; a static test pins the order and the plan must run `superclaude sweep --help` once outside a uv project. The pipx behaviour itself stays [UNVERIFIED], honestly tagged; the finding asked for a decision plus a test, which is given. |
| B-20 | RESOLVED | 05 lines 43-48 now carry verification tags. |
| B-21 | RESOLVED | `scope-03:152-157` lists the suite-wide scans and `:165` strikes the old "no glob test" claim as [CODE-CONTRADICTED]. Every citation re-read: `test_model_alias_policy.py:81-100` (globs `:84-86`, alias check `:97-99`); `tests/commands/test_graph_command.py:219-225` (glob `:222`); `test_worker_contract.py:379` `UNATTENDED_COMMANDS`, `:464-472` `_check_no_unattended_sections`, `:476-478` `_ORCA_NAME_RE`, `:519` assertion, `:1090-1094` `AUDIT_ROOTS`, `:1134` use; `test_primitive_dual_surface_lookup.py:16-21` `_ADV_SITES` (pinned sites, not a glob, as stated). |
| B-22 | RESOLVED | 06 `:33`, table cell `:56`, `:81`, `:151` re-read; consistent with the handler code. |
| B-23 | RESOLVED | 06 `:26`, `:181` re-read. |
| B-24 | RESOLVED (note) | 06 relabel rule `:16`, Q2 rows `:59-64`, constraints `:72`, Gaps 3/15 resolved, Gap 18 added. Residual MINOR: rows `:57` (`--ack` "advances inbox") and `:58` (`--wait`) still say [CODE-VERIFIED] on help-only behaviour, against the file's own `:16` rule. |
| B-25 | RESOLVED (note) | 05 Answer (1) corrected; residual MINOR phrasing at 05 `:165` and `scope-01:142` ("only non-consuming waiting signal is agentWait") states the conservative default as fact but points to the corrected answer. |
| B-26 | RESOLVED (note) | Every waiting case is named with its source: `scope-02:99-109` (a) `agentWait`, `blocked_question`, pending `ask` "no read path, G-B"; (b) frozen plan `WORKER-CONTRACT.md:133-136`, foreign ready Task `:129` via `task-list --ready`; `scope-04:328` matches. Residual MINOR: `research-notes.md:175`, `:196` point to "G-A" for `ask`; the correct gap is G-B. |
| B-27 | RESOLVED | `scope-03:143-150` item 9. Every Makefile citation re-read: `lint: lint-architecture` `:48-50`; target `:362`; Check 1 `:368-383`; Check 2 `:385-395`; Checks 3/4 `:398-410` (warn > 200, fail > 500, README excluded); Check 6 `:413-426`; Check 8 `:429-438` (`name:`, `description:`, `allowed-tools:`); Check 9 `:441-450`; Check 11 `:467-476` (`arch_lint --check-contracts ... --scan-paths src/superclaude/cli/`); summary `:484-489` (`exit 1`). `contracts/__init__.py:204-206` `RETURN_CONTRACTS = {"sc:adversarial": AdversarialReturn}` confirmed. |
| B-28 | RESOLVED (note) | "Needs a human" replaced by the Section C vocabulary in the research files. Residual MINOR wording: `research-notes.md:225` Section D heading and `scope-04:356` OQ1 still say "needs-a-human". |

## New blocking findings introduced by the fixes

None. Every residual found this pass is wording, a stale summary or a mis-pointed gap label on a claim whose substance is correct elsewhere in the same file; graded MINOR by the review severity rule.

## Notes (MINOR, non-blocking, not rechecked in later rounds)

| # | Location | Note |
|---|----------|------|
| N1 | `scope-01-contract.md:64` | "safe to close class": Section C makes it a REVIEW dimension, not a class. |
| N2 | `06-orca-open-questions.md:57-58` | `--ack` and `--wait` rows tagged [CODE-VERIFIED] on help text only; should be [UNVERIFIED] or "help-only" per `:16`. |
| N3 | `06-orca-open-questions.md:187` | Summary stale (`inbox`/`--unread` "undocumented", "items 1-15", `worktree ps --agent-wait`); the `:189` gate-fix paragraph corrects it. |
| N4 | `06-orca-open-questions.md` | `filterLegacyPeekResult` (`message-check-handler.js:74-95`) runs on every peek, not only legacy runtimes. |
| N5 | `scope-04:290`, `:320` | Retained-problems row omits stalled / could not determine; stale-row mapping ignores Section C rule 6. |
| N6 | `scope-04:356`, `research-notes.md:225` | "needs-a-human" wording left over. |
| N7 | `research-notes.md:175`, `:196` | "see G-A" for pending `ask`; should be G-B. |
| N8 | `research-notes.md:241-242` | 05/06 still listed as "MISSING, planned" (N-01 carry-over). |
| N9 | 05 `:165`, `scope-01:142` | Conservative default phrased as fact. |
| N10 | `scope-04` skeleton | A blocked `/sc:implement` contract can fit both waiting (a) and (b); dimensions are independent, so acceptable. |

## PASS set (cycle 1)

B-01, B-02, B-03, B-04, B-05, B-06, B-07, B-08, B-09, B-10, B-11, B-12, B-13, B-14, B-15, B-16, B-17, B-18, B-19, B-20, B-21, B-22, B-23, B-24, B-25, B-26, B-27, B-28 (28 of 28). No regression is possible at this cycle (F_0 had no prior PASS set for these IDs).

## Monotonicity

|F_0| = 28, |F_1| = 0. Strictly shrinks; no `[HALT-MONOTONICITY]`.

## Confidence

- **Confidence:** Verified: 28/28 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Adversarial check: the expected 5+ incomplete fixes did not materialise as blocking defects; the 10 residuals above are where the fixes were incomplete, and each is wording or a stale pointer whose substance is correct elsewhere.
- Limits: B-08 (populated `worker-list` row shape) and B-19 (pipx PATH behaviour) are resolved as honest UNVERIFIED gaps with a plan-time test, not by live capture; this pass ran no state-changing or live Orca command.
- **Tool engagement:** Read: 30+ | Grep: 4 | Glob: 1 | Bash: 12 (read-only: sed/nl, `git show 495eb96d`, one batched line-range script). No web research performed.

Status: COMPLETE

## Verdict: PASS
