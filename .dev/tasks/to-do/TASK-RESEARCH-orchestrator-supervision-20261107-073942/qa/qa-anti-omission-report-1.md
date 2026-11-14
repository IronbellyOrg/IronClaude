## Anti-Omission Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md` (289.5 KB, sections 1-10)
**Input files checked:** `research/research-notes.md` (336 lines), `research/scope-01-contract.md` (153 lines), `research/scope-02-orca-recovery.md` (243 lines)
**Total findings enumerated:** about 200 (173 represented, 6 covered by dedup, 21 omitted: 8 blocking, 13 MINOR)
**Date:** 2026-11-07
**QA phase:** anti-omission (partition: 3 assigned input files)
**Fix authorization:** false (report and input files not edited)

**Method.** Every distinct finding, claim, rule, recommendation and item in the three input files was listed (including AMBIGUITIES 1-11, C1-C15 and the critical gaps G-A, G-B in research-notes). For each, the report was searched by meaning (distinctive words, not IDs) with Grep and the matching lines were read. Coverage was judged by whether the report states the same substance, not by whether it cites the ID.

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports.]

### Omissions Found

| # | Source finding | Source file | Status | If deduped, by which report item | Severity |
|---|---|---|---|---|---|
| 1 | WORKER-CONTRACT cleanup refusal (`:108`) also says the coordinator "never runs one managed package in two worktrees at once". The report keeps the refusal conditions but drops this rule, so a sweep could miss a package that is running in two worktrees at the same time. | scope-01 rule 9 (`:64`) | OMITTED | - | IMPORTANT |
| 2 | Fan-in (`:156`) allows at most 10 inputs, and "a sweep reporting a fan-in group should show settled/admitted counts against N". The report keeps only the G5 trigger "a fan-in with fewer than 2 admitted inputs" (report line 1254). It has no per-group settled/admitted-of-N display and no max-10 bound. | scope-01 rule 13 (`:68`) | OMITTED | - | IMPORTANT |
| 3 | A worktree removed mid-sweep must be reported, and must not crash the run (seed-brief.md:45). The report has no row, test or behaviour for a root that disappears while the sweep runs. Greps for "mid-sweep" and "removed during" found nothing. | research-notes (`:178`) | OMITTED | - | IMPORTANT |
| 4 | The #409 reuse pattern counts affected items as a set union across sources (PLAN.md:36), so one item reached by two sources is counted once. The report reuses the #409 ordering and `shown/total` (C6, C7) but never says how counts are deduplicated across sources. A grep for "set-union" / "set union" found nothing. | research-notes (`:143`) | OMITTED | - | IMPORTANT |
| 5 | The coordinator turn guard: when `worker-list --run <id> --terminal-state reclaimable --json` returns rows, the coordinator must not end its turn. The report's WC-14 loop (G1-G7, item 8) and its terminal-releasable rule do not carry this guard. Greps for "turn guard" and "end the turn" found nothing. | scope-02 (`:94`) | OMITTED | - | IMPORTANT |
| 6 | Context-only Dispatches created by `orchestration dispatch` are listed as `unsupervised` with terminal state `retained` [CODE-VERIFIED]. The report's classifier precedence never says how these dispatch-only rows are classified, so they could be misread as stuck or releasable workers. Greps for "dispatch-only" and "Context-only" found nothing. | scope-02 (`:95`) | OMITTED | - | IMPORTANT |
| 7 | The package state "archive-blocked" (a non-Linux refusal, so the folder stays in `to-do/`) and the `.archiving` marker, which means an interrupted archive. The sweep reads `.dev/tasks/{to-do,done}` (report line 362), but no class, row or report rule covers either state. On non-Linux hosts an archive-blocked package would be reported as unfinished work, and an interrupted archive would go unflagged. | scope-02 (`:192`); research-notes (`:177`) | OMITTED | - | IMPORTANT |
| 8 | The new HOW-WE-WORK routing row needs a new row ID (for example `supervise-sessions`) registered in `_EXPECTED_IDS` (`:56-97`) of the routing-table test, or the test fails. The report lists the other registries (RULE_PHRASES, NEVER_AS_WORKER, WRITE_VERB_CLASSIFICATION, the noqa registration at line 1228) but not this one. A grep for `_EXPECTED_IDS` found nothing. Rated IMPORTANT because the omission is a test-break risk and it is unclear whether it is load-bearing. | scope-01 (`:117`) | OMITTED | - | IMPORTANT |
| 9 | When the report dir is missing, no file is written and the error appears only in chat; Orca does not check the file, so the coordinator opens it itself. | scope-02 (`:177`) | COVERED-BY-DEDUP | Classifier precedence rule 7, "everything else" / needs-review (report line 390), plus rule 6: a worker with no readable report lands in a review class | Not blocking |
| 10 | Child cleanup (`:107`): a merge conflict is stopped and reported, never resolved. | scope-01 rule 10 (`:65`) | COVERED-BY-DEDUP | WC-14 item 8 (report line 445: no stop, merge or new Task) and the later-phase `/sc:close` deferral (report line 488) | Not blocking |
| 11 | Never release a worker on weak signals (idle time, a quiet terminal). | scope-02 (`:93`) | COVERED-BY-DEDUP | Terminal-releasable rule (report line 409) and WC-10 "absence is never death" (report line 478) | Not blocking |
| 12 | `worker-show` outranks the `worker-list` row when the two disagree. | scope-02 (`:84`) | COVERED-BY-DEDUP | `worker-show` read per row as the authoritative projection (report line 111) | Not blocking |
| 13 | A workflow contract may already have moved to `done/`. | scope-02 (`:184`) | COVERED-BY-DEDUP | Package source `.dev/tasks/{to-do,done}/*/` (report line 362) | Not blocking |
| 14 | Always pass `--include-remote` to `worker-list`. | scope-02 (`:121`) | COVERED-BY-DEDUP | Deliberately changed and recorded under GQ-22 (report line 354) | Not blocking |
| 15 | The `### Orca session launches` section in core/CLAUDE.md (`:45`) must not be contradicted by the new guidance. | scope-01 (`:112`) | OMITTED | - | MINOR |
| 16 | F12 naming question: `sc:sessionsweep` or `sc:sweep`. | scope-01 (`:138`) | OMITTED | - | MINOR |
| 17 | When a person-mode flag is refused, `worker_status: failed` is written. | scope-02 (`:180`) | OMITTED | - | MINOR |
| 18 | `lastFailure` is a JSON-encoded string and must be parsed a second time. | scope-02 (`:60`) | OMITTED | - | MINOR |
| 19 | The tally of observed enum values for worker state fields. | scope-02 (`:76`) | OMITTED | - | MINOR |
| 20 | `orca-titles` as a title source. | scope-02 (`:166`) | OMITTED | - | MINOR |
| 21 | How the slugify step names sessions/worktrees. | scope-02 (`:162`) | OMITTED | - | MINOR |
| 22 | The shape of the `worker-release` receipt. | scope-02 (`:206`) | OMITTED | - | MINOR |
| 23 | Custom titles are ignored when sessions are matched. | scope-02 (`:156`) | OMITTED | - | MINOR |
| 24 | The `ccsession --here` grouping when a worktree has been removed. | scope-02 (`:164`) | OMITTED | - | MINOR |
| 25 | Why the field is named `worker_status`. | scope-02 (`:176`) | OMITTED | - | MINOR |
| 26 | `json.dumps(..., ensure_ascii=False)` in the reused output pattern. | research-notes (`:130`) | OMITTED | - | MINOR |
| 27 | The #409 footer "source coverage is not fleet-wide assurance". The report's own footer (line 428) partly covers the idea but not this wording. | research-notes (`:143`) | OMITTED | - | MINOR |

### Summary

- **Findings enumerated:** about 200. Counted by meaning across the three input files, including AMBIGUITIES 1-11, C1-C15, G-A and G-B. The count is approximate because compound bullets were split into distinct findings by judgement.
- **REPRESENTED:** about 173. This includes all AMBIGUITIES 1-11 (report 9.5, lines 1653-1663); C1-C7, C9 and C13 (report lines 585-593 and 1359-1367); C8 and C12 (lines 1637, 1639); C14 (line 1672); G-A and G-B; options A1-A4; the data sources; classifier precedence; the 6 h window; the report rules; WC-14 G1-G7 and item 8; the test registries; the routing copies; and the S1-S4 security items.
- **COVERED-BY-DEDUP:** 6 (rows 9-14).
- **OMITTED, blocking (IMPORTANT):** 8 (rows 1-8). None is CRITICAL.
- **OMITTED, MINOR (notes, not blocking):** 13 (rows 15-27).

The adversarial expectation of at least 5 silent drops was met: 8 blocking drops were found. Most are edge cases in the sweep's behaviour: a package running in two worktrees, fan-in counts, a root removed mid-sweep, set-union counting, the turn guard, dispatch-only rows, archive-blocked or interrupted-archive packages, and the `_EXPECTED_IDS` registry. A classifier or test built only from the report would miss each of them.

Verdict: FAIL
