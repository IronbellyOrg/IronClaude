# Diff Analysis: Position paper Comparison (D11 observability stack)

Prerequisites validated.

## Metadata
- Generated: 2026-11-20T04:10:00Z
- Variants compared: 2 (Variant 1 = OURS, `position-OURS.md`; Variant 2 = CLAY, `position-CLAY.md`)
- Total differences found: 18 (2 + 10 + 2 + 4 shared assumptions)
- Categories: structural (2), content (10), contradictions (2), unique (10), shared assumptions (4)
- Taxonomy tags (AD-5): L1 surface = C-010; L2 structural = S-001, S-002, C-001, C-002, C-003, C-005, C-006, C-007, C-009, X-001, X-002, A-002, A-004; L3 state mechanics = C-004, C-008, A-001, A-003

## Structural Differences

| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity |
|---|------|------------------|------------------|----------|
| S-001 | Section "mechanism" | A target architecture in four layers (facts, screen, work item, notice policy). Part of it is not built: contract note not written. | A description of the built report pipeline (entry files, join, sort, compare, gate) plus the escalation rule. All of it is on master as code or spec text. | Medium |
| S-002 | Evidence frame | 8 cited facts mostly about what the report is NOT (third collector, person-specific, needs a model, absent from design 681). | 8 cited facts mostly about what the report DOES (answers the 409 asks, built, tested, no silent loss). | Low |

## Content Differences

| # | Topic | Variant 1 (OURS) approach | Variant 2 (CLAY) approach | Severity |
|---|-------|---------------------------|---------------------------|----------|
| C-001 | Source of session facts | Sweep JSON (schema v1) is the one source; observer reads it; the report must not read Orca sessions itself in the long run. | The report keeps its own session reading (`sessions.py`) because it reads whole transcripts from a saved position; sweep reads a 256 KiB tail. | High |
| C-002 | Who owns GitHub, ClickUp and plain-English item text | The report layer is an added source joined into the same pipeline through a written contract note. | It stays in the report skill, which already has the code; the sweep stays Orca-only (issue 409 item 3 answered by existing code). | High |
| C-003 | Meeting Clay's issue 409 asks (summary, done, left, needs me, links) | Through the observer Decision Desk later, fed by the shared source; the report is an interim second layer. | The report meets them today; it is the only piece that does. | High |
| C-004 | Read-only and "recommend nothing" rules | Sweep says "Will Not: recommend anything", observer is navigation only; report entries carry Options, Recommendation, typed answer, DM and commit writes. The owner's rule must win on sweep and observer surfaces. | Concedes the DM and commit are writes the sweep and observer rules forbid, but treats the report as a separate surface with its own rules. | Medium |
| C-005 | Person-specific design and cost | `config.json` names `clayphi`, America/Chicago, one ClickUp token; a model step costs tokens each run; sweep is zero-token. | Same facts listed as costs; adds that `refresh` is no-model and only the daily run spends tokens. | Medium |
| C-006 | Nine-row "what reaches Clay" table | Policy text that can be adopted; nothing built depends on it; matches the owner's "decision ledger only" rule. | Not duplicated anywhere; the sweep has "waiting on a person" with no reason list; test-pinned in the design plan. | Medium |
| C-007 | Cap of 5 notices a day | Config key `reach_daily_max` parsed only in PR 686 (`repos.py:91,262`); no verb enforces it; "5 is this design's number". | Settled by ruling 39; cap holds back notices, never entries. | Medium |
| C-008 | Status vocabulary | Sweep has eight classes with proof rules and "could not determine". | The report has six statuses (working, progressed, waiting on you, stuck, stalled, done); raised as a risk that the two disagree about one session. | Medium |
| C-009 | Living report (entry file per issue) | Not addressed beyond "design 681 never mentions sweep, observe or 409". | One entry file per held issue, excluded from the daily run, rebuilt without a model (`exclude.py`, `run.py refresh`). | Medium |
| C-010 | Naming and state layout | Silent. | Admits the skill still says `/sc:orchestrator` and `.dev/coordinator/` (singular) against the owner's naming and layout decisions. | Low |

## Contradictions

| # | Point of Conflict | Variant 1 (OURS) Position | Variant 2 (CLAY) Position | Impact |
|---|-------------------|---------------------------|---------------------------|--------|
| X-001 | Direction of the dependency | "it must sit on top of that source" (claim): the report depends on the sweep JSON. | "let the sweep and the observer feed or read it where they overlap" (claim): the report is a node others may read. | High |
| X-002 | Sequencing | Contract note and pinning test first; "a third collector makes the unification harder". | "Do not hold working code until a contract note and a schema change exist"; waiting delays a daily tool that works now. | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | OURS | Observer questions panel is switched on (`QUESTION_GATE_PASSED = True`, `observe/commands.py:67`) and the chain watcher, orchestrator, dashboard is the owner's decided order. | High |
| U-002 | OURS | Sweep reads Orca only through a fixed allowlist of argv templates (`probes.py:49-56`) and uses no model; WC-16 runs it at most every 5 minutes. | Medium |
| U-003 | OURS | Owner rule "automated checks display outstanding user decisions only, no heartbeat chatter" supports the cap and "when in doubt it does not reach". | Medium |
| U-004 | OURS | Verified that no `escalate` verb, no `orchestrator` command group and no `asks.json` exist in master, pr-a or pr-p: the cap and table are spec only. | High |
| U-005 | CLAY | Script gate: `check.py` and `run.py gate` stop a bad report; nothing silently dropped; unanswered Needs-you entries are carried. | High |
| U-006 | CLAY | 142 test functions in `tests/skills/test_agent_work_report.py`; waker automations verified 2026-11-03; page served at 127.0.0.1:8765 and opened in Orca. | Medium |
| U-007 | CLAY | `run.py refresh` rebuilds the living page with no model call. | Medium |
| U-008 | CLAY | Maps Clay's 409 comment word for word onto the item template (state, Done, Still to do, Needs you, Next, links). | High |
| U-009 | CLAY | Admits `/sc:orchestrator` and `.dev/coordinator/` text in a merged skill that conflicts with owner naming. | Medium |
| U-010 | CLAY | Names the status-vocabulary disagreement risk and the DM and commit writes as risks. | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | Both treat sweep rows, observer rows and report session items as the same sessions | A session can be joined across the three readers by one stable key (Orca terminal handle, Claude session id or worktree path). The report joins by the Orca hook file and transcript; sweep by Run and worker rows. No paper says what the key is. | UNSTATED | Yes |
| A-002 | Both accept the nine rows | The nine rows, written for Clay's five product reasons and Jay's six classes, fit the owner and other users unchanged (row 1 "his own identity" names one person). | UNSTATED | Yes |
| A-003 | Both accept "additive change to the sweep JSON" as the way to add fields | Adding fields to the sweep JSON v1 is cheap. Source: the v1 key set is pinned by a golden test (NFR-009, `docs/designs/orchestrator-mode.md:605`), so a change needs a reviewed test edit. | UNSTATED | Yes |
| A-004 | Both treat the report skill as placeable in any workspace | The report needs an "orchestrator repo" path in `~/.config/superclaude/issue-watch.json` (`orchestrator_repo`) or `$AWR_ROOT`; without it the skill exits (`common.py:22-42`). So it is not zero-setup. | UNSTATED | Yes |

## Summary
- Total structural differences: 2
- Total content differences: 10
- Total contradictions: 2
- Total unique contributions: 10
- Total shared assumptions surfaced: 4 (UNSTATED: 4, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003, X-001, X-002
- Similarity check: 18 of 18 comparable items differ, far above the 10% threshold; the debate proceeds.
