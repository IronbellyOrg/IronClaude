# Research Completeness Verification (Partition 2 of 2)

**Topic:** Orchestrator mode Phase 1 (issue #339): read-only `/sc:sweep` and coordinator-loop rules
**Date:** 2026-11-07
**Analysis type:** completeness-verification (checklist items 1, 4 and 5 only)
**Assigned files:** `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`, `research/06-orca-open-questions.md`
**Scope source:** `research/research-notes.md` (EXISTING_FILES, RECOMMENDED_OUTPUTS, gaps G-A, G-B)
**Depth tier:** Deep
**Fix authorization:** false (no research file was edited)

[PARTITION NOTE: Cross-file checks limited to assigned subset plus `research-notes.md`. Full cross-file analysis requires merging all partition reports.]

---

## Method

- Read in full: `research/research-notes.md` (EXISTING_FILES `:15-108`, RECOMMENDED_OUTPUTS `:215-216`, SUGGESTED_PHASES `:229-245`, claims C8-C12 `:300-306`), `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`, `research/06-orca-open-questions.md`.
- Coverage: `grep -cF` of every EXISTING_FILES path in the S3 and S4 sections against the three files, then a directory-wide grep for the two paths with zero hits.
- Claim re-verification (read-only): scope-03 citations re-read with `cat -n` (main.py, recommend, reflect, tests, registries, command and skill files, Makefile/pyproject/pre-commit/CI, design doc); scope-04 citations re-read with `git show 495eb96d:<path>`; 06 citations re-read with `orca-ide --version`, `orca-ide orchestration [check|ask|reply|inbox|worker-list|worker-show] --help`, `orca-ide orchestration --help`, `orca-ide status --help`, `orca-ide worktree ps --help`, `orca-ide skills get orchestration [--reference messaging-and-gates|recovery-and-cleanup]`, `orca-ide skills get orca-cli`, each through `cat -n`, plus `cat -n` of `WORKER-CONTRACT.md` and `orca-capabilities.md`. No state-changing or message-consuming Orca command was run.

## Coverage Audit (checklist item 1)

Scope items are the EXISTING_FILES rows of the S3 section (`research-notes.md:69-95`), the S4 section (`:97-99`) and the G-B planned output (`:216`, `:245`). Rows of the S1/S2 sections belong to partition 1.

| Scope item (research-notes line) | Covered by | Status |
|---|---|---|
| `cli/main.py` (:73) | scope-03 (10 mentions; `:18`, `:20`, decorators, `:519-561`, `:564` re-verified) | COVERED |
| `cli/recommend/__init__.py`, `recommend/commands.py` (:74-75) | scope-03 (lazy `__getattr__` `:12-20`; group `:34-48`; `python -m` claim `:40-41`; stderr + `sys.exit(1)` `:108-112`) | COVERED |
| `cli/reflect/__init__.py`, `config.py`, `contract.py`, `models.py`, `commands.py`, `runner.py` (:76-80) | scope-03 (`_git` `:64-78`; fail-closed `:103-109`, `:158-159`; `contract.py:7`, `:397`; `which` `runner.py:387`, `commands.py:494`) | COVERED |
| `tests/cli/test_cli_registration.py` (:81) | scope-03 (`EXPECTED_TOP_LEVEL_COMMANDS` `:31-49`, omits swarm and reflect) | COVERED |
| `tests/recommend/test_cli_registration.py`, `conftest.py` (:82) | scope-03 | COVERED |
| `tests/cli/reflect/conftest.py`, `test_contract_status_cli.py`, `test_isolate_reviewers_cli.py`, `test_cli_smoke.py`, `test_preflight_phase_complete.py` (:83-85) | scope-03 (1-3 mentions each) | COVERED |
| `tests/recommend/test_routing_refresh.py` (:86) | scope-03 (`:33`, `:39`, `:472`, `:647-648`) | COVERED |
| `tests/commands/test_issue_command.py`, `tests/unit/test_cli_install.py` (:87-88) | scope-03 (2 mentions each) | COVERED |
| `commands/issue.md`, `reflect.md`, `recommend.md`, `help.md`, `graph.md`, `README.md` (:89) | scope-03 (all re-verified) | COVERED |
| `sc-issue-protocol`, `sc-reflect-protocol`, `sc-recommend`, `sc-swarm-wizard-protocol` SKILL.md (:90) | scope-03 | COVERED |
| `Makefile`, `pyproject.toml`, `.pre-commit-config.yaml`, `test.yml` (:91) | scope-03 | COVERED |
| `docs/designs/sc-issue-command.md` (:92) | scope-03 (20 headings and `:380`, `:384` re-verified) | COVERED |
| `docs/user-guide/commands.md` (:93) | scope-03 (`:105`, `:115`, `:347`) | COVERED |
| `src/superclaude/output-styles/pragmatic.md` (:94) | none: 0 hits in all three files and 0 in the whole `research/` directory except `research-notes.md` itself | **GAP** (F1) |
| `src/superclaude/hooks/scripts/launch-job-identity.sh` (:95) | none: 0 hits anywhere in `research/` except `research-notes.md` | **GAP** (F2) |
| #409 package at `495eb96d` (:97-99): README, DESIGN-CONTRACT, PLAN, QA, concepts, data-dictionary, integration-gaps, canvas, fixtures, render, layouts/agent_focus, tests | scope-04 (6-27 mentions each; line counts and anchors re-verified with `git show`) | COVERED |
| G-B planned output `06-orca-open-questions.md` (:216, :245) and its sources `orca-capabilities.md:56-68,148-151`, WC-3, `WORKER-CONTRACT.md:133-136`, `integration-gaps.md:11` | 06 (all cited) | COVERED |
| G-B planned fallback list "`agentWait`, `blocked_question`, Ruling halt, frozen plan" (:216) | 06 covers `agentWait` (Q4.2), `blocked_question` (Q1), frozen plan (Q4.1); Ruling halt only inside the freeze definition, no own fallback line | PARTIAL (F6) |

**Coverage result:** 2 S3 rows uncovered by any research file; 1 planned fallback partially covered.

## Completeness (checklist item 4)

| Research file | Status | Summary | Gaps section | Key Takeaways | Rating |
|---|---|---|---|---|---|
| `scope-03-cli-patterns.md` | `**Status:** Complete` (`:3`) | Y, `## Summary` (`:198`) | Y, `## Open questions` (`:189`) | not required | Complete |
| `scope-04-409-layout.md` | `**Status:** Complete` (`:4`) | Y, `## Summary` (`:322`) | Y, `## Open questions` (`:311`) | not required | Complete |
| `06-orca-open-questions.md` | `**Status:** Complete` (`:5`) | Y, `## Summary` (`:179`) | Y, `## Gaps and Questions` (`:153`, 16 items) | Y, one `**Key Takeaways**` list per question (`:40`, `:77`, `:110`, `:138`); no file-level heading, which the prompt does not require | Complete |

All three files pass item 4. One related stale statement sits outside the assigned files: `research-notes.md:237` still says scope-03 has no "Summary" heading (F3).

## Cross-reference check (checklist item 5)

| # | Cross-cutting concern | Where raised | Where it should be picked up | Result |
|---|---|---|---|---|
| X1 | `check --wait` is destructive | `research-notes.md:178` "`check --wait` (consumes messages, assumed; UNVERIFIED)"; C8 `:300` | 06 Q1 `:32` and Q2 table `:57`: "waiting reserves nothing", does not drain, "still a consuming-mode check" | 06 refines the note but never names `research-notes.md:178` or C8 as superseded (F4) |
| X2 | C11 "A non-consuming read of pending questions exists" (`research-notes.md:303`, G-B) | research-notes | 06 Q2: `--peek`/`--all` documented non-marking, capped at 100 rows, not exercised live | Answered as "documented, unexercised"; 06 does not state the new C11 status (F4) |
| X3 | C12 pane-key join (`research-notes.md:304`, `:175`) | research-notes (no agent) | 06 Q3 `:95` cites `[CLI]:227` `agents[].paneKey` (`<tabId>:<leafId>`) | Relevant evidence present, not linked to C12 (F5) |
| X4 | Ruling halt as needs-person fallback (`research-notes.md:186`, `:216`) | research-notes | 06 cites WC-3 range `:52-57`, which contains the Ruling-halt rule at `WORKER-CONTRACT.md:56`, but never discusses it | Partial (F6) |
| X5 | integration-gaps line 11 (non-consuming enumeration) | research-notes `:171`, `:216`; scope-04 | 06 Q2 `:67`, Gaps item 7 | Linked |
| X6 | integration-gaps line 12 (cross-host joins) and line 28 (Next experiment) | scope-04 | 06 `:98`, `:136` | Linked; `git show` confirms line 28 holds "locate a frozen worktree" (heading at `:26`) |
| X7 | Inventory staleness (`orca-capabilities.md:8`, `:58`, `:63`, `:68`, `:177`) | inventory (S2 source) | 06 "Stale Documentation Found" `:172-177` | Linked; all five inventory lines re-read and match 06's description |
| X8 | Nested-worker depth vs helper `worker-start` (`orca-capabilities.md:35`, `:97-98`; WC-13 `WORKER-CONTRACT.md:61`) | inventory, contract | 06 Gaps item 16 | Linked |
| X9 | Read-only CLI precedent (`config.py` owns subprocess; `contract.py` pure) for a sweep CLI | scope-03 | 06 says which Orca verbs a sweep may call, but not where such calls would live | Not required by 06's prompt; recorded as a note for synthesis, not a finding |
| X10 | Observer layout (scope-04) vs sweep classes (needs-person, frozen, unknown) | scope-04, research-notes `:186-190` | 06 Q4 "Consequence" `:133-135` maps to the same classes | Consistent; no contradiction found |

## Claim-verification evidence (adversarial pass)

The stance assumed at least 5 errors. Every citation below was re-read; results:

| File | Citations re-checked | Confirmed | Wrong or unsupported |
|---|---|---|---|
| scope-03 | about 120 file:line anchors and counts (main.py, recommend, reflect, 8 test files, 6 command files, 4 skills, build/lint/CI, design doc, user guide, HOW-WE-WORK markers `:318`, `:337`) | all | 0. The tag-count claim at `:200` ("58 findings tagged [CODE-VERIFIED]") against 59 grep hits is not an error: line 200 itself carries the 59th tag. |
| scope-04 | `495eb96d` file line counts (render.py 130 and others), anchors in canvas, agent_focus, fixtures, data-dictionary, integration-gaps, DESIGN-CONTRACT `:11`, `:14`, concepts, PLAN, QA, README, render, tests; ancestry (not on `origin/master`); seed-brief `:44` | all | 0. `data-dictionary.md:15` lists 4 source ids while fixtures carry 5 (`demo:resources`); scope-04 reports 5 from the fixtures, which is correct. |
| 06 | CLI version; `[H:check]` 3-8, 24, 28, 35-37; `[H:ask]` 3, 5, 16, 23, 24; `[H:reply]` 3, 5; `[H:inbox]` 3-14; `[H:worker-list]` 5, 20, 22; `[H:worker-show]` 16; `[H:status]` 14; `[H:worktree-ps]` 3, 5, 13, 16-17, 19; `[H:orch]` 19-20, 25; `[G]` 42, 62-64, 81-83, 113, 130-131, 135, 140, 156-161; `[G:messaging]` 12-19, 26-27, 60-63, 76; `[G:recovery]` 28-31, 54-61; `[CLI]` 84, 161-162, 227; `WORKER-CONTRACT.md` 11, 30, 45, 52-58, 61, 133-136; `orca-capabilities.md` 8, 35, 58, 63, 68, 97-98, 148-151, 177, 182, 185; integration-gaps 11, 12, 28 | all line numbers and quotes | 3 content issues: F7 (WC-10 cited for a rule it does not contain), F8 (internal inconsistency on what drains a Delivery), F9 (`terminal list`/`terminal read` labelled verified without their help being read) |

## Findings

| ID | Severity | File | Finding | Evidence | Remediation |
|---|---|---|---|---|---|
| F1 | IMPORTANT | coverage (S3 row `research-notes.md:94`) | `src/superclaude/output-styles/pragmatic.md` is in scope (mandatory DONE / NEXT table, "No exceptions", open owner decision 6 at `research-notes.md:282`) but no research file investigated it; the only anchors (`:22`, `:53`) are marked "not re-read" in the notes. The sweep's output format depends on whether this rule applies, so synthesis would rest on an unverified anchor. | 0 grep hits for `pragmatic` in all `research/` files except `research-notes.md` | Gap-fill: a codebase agent reads `pragmatic.md` `:22` and `:53`, records the exact rule text and whether an exception mechanism exists, tagged [CODE-VERIFIED], in a research file (for example an addendum to scope-03 by its owner, or a new `research/07-*.md`). |
| F2 | MINOR | coverage (S3 row `research-notes.md:95`) | `src/superclaude/hooks/scripts/launch-job-identity.sh` (PR #414 same-user job identity, anchor `:2-9`) is in scope but no research file covers it. It bears on telling person-started sessions from jobs. | 0 grep hits for `launch-job-identity` outside `research-notes.md` | Either cover `:2-9` in the F1 gap-fill or drop the row from EXISTING_FILES with a one-line reason. |
| F3 | MINOR | `research-notes.md:237` | Stale: says scope-03 has no "Summary" heading; scope-03 has `## Summary` at `:198`. | `research-notes.md:237`; `scope-03-cli-patterns.md:198` | Correct the row (owner of research-notes) or note the correction in the gaps log. |
| F4 | MINOR | 06 vs `research-notes.md:178`, `:300`, `:303` | 06 changes the status of three notes items without saying so: the `check --wait` "consumes messages" assumption (now: reserves nothing, drains only with acknowledgement, still consuming mode), C8 (guide-sourced `check --wait` consumption) and C11 (a documented, capped, unexercised non-consuming read exists). A synthesis agent reading the notes first may carry the older status forward. | 06 `:32`, `:57`, `:58-59`, `:71-75` | Synthesis must take C8/C11 and the `:178` exclusion reason from 06, recording C11 as "documented, not exercised; 100-row cap". Optionally add a "Notes items resolved" line to 06 via its owner. |
| F5 | MINOR | 06 Q3 `:95` vs C12 | 06 quotes the documented pane key format `agents[].paneKey` (`<tabId>:<leafId>`, `[CLI]:227`) but does not link it to C12 (`orca-tabs` pane key joins `dispatch.assigneePaneKey`, UNVERIFIED, "no agent"). | `research-notes.md:304`, `:175`; 06 `:95` | Synthesis should cite 06 `:95` as partial evidence for C12 and keep C12 UNVERIFIED until an `orca-tabs` file name is compared with a `paneKey` value. |
| F6 | MINOR | 06 Q1/Q4 | The planned fallback list names a Ruling halt (`research-notes.md:216`), and the needs-person class includes it (`:186`). 06 covers it only inside the freeze definition (`:123`) and never cites WC-3's Ruling rule (`WORKER-CONTRACT.md:56`: a Ruling halt "is never asked" and is reported blocked whatever the policy line says). | 06 `:29`, `:123`; `WORKER-CONTRACT.md:56` | Synthesis should state that a Ruling halt is always a needs-person row read from the contract/ledger, never from Orca, citing `WORKER-CONTRACT.md:56`. |
| F7 | MINOR | 06 Q2 `:72` | Mis-attribution: "WC-10's no-guess rule, `WORKER-CONTRACT.md:45`" for reporting a 100-row truncation as "could not determine". WC-10 is the heartbeat-liveness rule ("treats a missing heartbeat as absence, never as death"); `WORKER-CONTRACT.md` has no "no-guess" or "could not determine" text (grep: 0 hits for `guess`, `could not determine`). | `WORKER-CONTRACT.md:45`; grep results | Cite the conclusion as derived (absence-is-not-proof by analogy with WC-10 and `[G:recovery]:58-61`), or cite the sweep's own "What I could not determine" precedent (`sc-crash-recovery/SKILL.md:139-150`, research-notes `:52`). |
| F8 | MINOR | 06 Q1 `:32` vs Q2 `:49`, `:55` | Internal inconsistency: Q1 says a Delivery "is drained only by `--ack`"; Q2 (and `[H:check]:37`, `[G:messaging]:17-19`) say it replays "until acknowledged or all its messages are marked read". | 06 `:32`, `:49`; `[H:check]:37` | Synthesis should use the Q2 wording; the "only" in Q1 is wrong. |
| F9 | MINOR | 06 Q3 `:101` | `terminal list` and `terminal read` are labelled "[CODE-VERIFIED as wording]" as views, but their `--help` is not in the commands-run list (`:13`) and no `[CLI]` or `[H:*]` line is cited for them; only `worktree ps` and `reference find` wording is cited. | 06 `:13`, `:101` | Mark `terminal list`/`terminal read` side effects [UNVERIFIED], or read `orca-ide terminal list --help` and `terminal read --help` before synthesis relies on them. |

**Withdrawn candidates (checked, not errors):** scope-03 tag count 58 vs 59 (line 200 holds the extra tag); 06's integration-gaps "line 28" citation (confirmed by `git show`; the heading is at `:26` and the text at `:28`); 06's `[G]:135` quote ("replays that batch until acknowledged", present on line 135).

**Severity count:** CRITICAL 0, IMPORTANT 1 (F1), MINOR 8 (F2-F9).

## Compiled gaps (from the assigned files' gaps sections, plus findings)

| Category | Gap | Source |
|---|---|---|
| Important | `pragmatic.md` DONE / NEXT rule not investigated (F1) | coverage audit |
| Important | Non-consuming question read is documented but not exercised; plain `check` read-marking, `--peek`/`--all` side effects, `inbox` and `--unread` semantics UNVERIFIED | 06 Gaps 1-4 |
| Important | 100-row cap with no cursor on `--all` and Run `--peek` (integration-gaps line 11 still open) | 06 Gaps 7 |
| Important | Answered vs pending question state not visible (`reply` effect, question-reply link) | 06 Gaps 5-6 |
| Important | `agentWait` probe side effects, and whether `agentWait` is set during `ask` | 06 Gaps 10-11 |
| Minor | `ask --dispatch-capability` meaning; peer `ask --to run:<id>`; heartbeat age vs `projection.liveness`; missing `caller` in `status --json`; cross-host joins; `check --format` help contradiction | 06 Gaps 8, 9, 12-15 |
| Important | Where a static sweep gets human questions; header must say message coverage is partial if enumeration is incomplete (same gap as 06 Q2) | scope-04 Q2 `:314` |
| Minor | scope-03 open questions: lazy vs eager `cli/sweep/__init__`; HOW-WE-WORK "Other commands" row vs excluded set (`test_how_we_work_routing_table.py:299-309`); `uv run superclaude` in a pipx-installed non-IronClaude project (UNVERIFIED); command-file `allowed-tools` interaction (UNVERIFIED); probe placement (recommendation); UTILITIES table pinning (UNVERIFIED) | scope-03 `:191-196` |
| Minor | scope-04 open questions: needs-a-human sort tie-break; "explicit closure evidence" for real sessions; print five or three source coverages; unrendered scope line; omission bound for Markdown; approval label wording; which #409 version to follow while `495eb96d` is unmerged | scope-04 `:313`, `:315-320` |
| Minor | F2-F9 | this report |

## Recommendations

1. Before synthesis: run one gap-fill read for F1 (and F2) and record the result in a research file.
2. Synthesis agents take C8, C11 and the `check --wait` exclusion reason from 06, not from `research-notes.md:178`, `:300`, `:303` (F4), and use 06 Q2's drain wording (F8).
3. Synthesis cites the Ruling-halt rule `WORKER-CONTRACT.md:56` for the needs-person class (F6), links 06 `:95` to C12 (F5), and does not cite WC-10 as a "no-guess" rule (F7).
4. Treat every 06 behaviour claim as "documented in CLI 1.4.245, not exercised"; the sweep design keeps the contracts-only fallback (06 `:75`) until a throwaway-Run test or handler read settles 06 Gaps 1-4.
5. Merge step: combine with partition 1 for S1/S2 coverage and cross-file contradictions.

**Verdict basis:** 1 IMPORTANT finding (F1: `pragmatic.md` in scope but covered by no research file) and 8 MINOR findings; 0 CRITICAL. All three assigned files pass item 4 (completeness), and every re-checked citation in them is correct.

## Verdict: FAIL

