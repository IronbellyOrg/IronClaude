# QA Report — Synthesis Gate Fix-Cycle Verification

**Topic:** Orchestrator mode Phase 1 (issue #339), synthesis-gate fixes B-01 to B-15
**Date:** 2026-11-07
**Phase:** fix-cycle
**Fix cycle:** 1
**Fix authorization:** false (report only; no synthesis file edited)
**Inputs:** `qa/qa-consolidated-findings-phase5.md` (|F_0| = 15), `qa/qa-synthesis-fix-log.md`, `synthesis/synth-01..06`, cited `research/` files and `gaps-and-questions.md`.

---

## Per-finding verification

(Written incrementally; one row per finding as it is checked.)

| ID | Status | Evidence (re-read this pass) | Notes |
|---|---|---|---|
| B-01 | RESOLVED | S1 `:201` now reads Open 75 / Resolved 25 / no open blocking QA finding, matching `gaps-and-questions.md:125`. | - |
| B-02 | RESOLVED | S4 `:220` X-6 is restated as resolved, with no effect on the option choice; "off by one" is gone. `gaps:125` agrees. | - |
| B-03 | RESOLVED | S5 `:261` X-6 resolved; the coverage row `:283` cites `:125` as 75/25; the C2 row `:172` is labelled as the line-count note (matches S2 4.x C2 = line count). | - |
| B-04 | RESOLVED | S6 row 17 (`:45`) keeps `--include-remote` in the default argv, measures the cost once and leaves GQ-22 open (`gaps:45`). S5 step 1.4 (`:62`) has a matching acceptance line. `research/05-orca-row-schema.md:163` supports it. | - |
| B-05 | RESOLVED | S6 row 58 (`:87`) now matches the S5 step 1.3 resolution (rule 2 needs the transcript; exited, no `worker_done` and an unreadable transcript give could not determine; not a WC-10 break). `gaps:107` (GQ-84). | - |
| B-06 | RESOLVED | S5 `:90` (1.17), `:138`, `:158`, `:159` and OQ-11 `:223` mark GQ-10, GQ-11, GQ-35 and GQ-61 as working defaults pending an owner decision. S6 row 51 (`:80`) marks GQ-61 as an owner decision, with 6 h as the working default. `gaps:33`, `:34`, `:58`, `:84` all read "open (owner decision)". | MINOR note N-1: steps 1.5 and 1.6 still state `.dev/` and the `495eb96d` pin without repeating "working default". OQ-11 covers both, so this is not a false claim. |
| B-07 | RESOLVED | S6 row 33 (`:61`) is GQ-38 paging (`page.nextCursor`, `--run`; `gaps:61`). New row 33a (`:62`) is GQ-48: "at least 100 (truncated at 100), total could not determine" (`gaps:71`). | Extra edit 33a checked: correct, and consistent with S5 `:62-63`. |
| B-08 | RESOLVED | S6 row 49 (`:78`): no version probe in Phase 1, contracts-only default, `--peek` gated, GQ-59 open (`gaps:82`). Row 36 (`:65`): GQ-41 stays open [UNVERIFIED] and no header field is promised (`gaps:64`). | - |
| B-09 | RESOLVED | S5 step 1.19 (`:92`) uses `/sc:sweep` and `_check_never_as_worker`. Grep of `tests/skills/test_worker_contract.py` confirms `:87` (`RULE_PHRASES` entry "**Never-as-worker list**"), `:398-399` (`_check_never_as_worker` reads the `**Never-as-worker list**` line) and `:545-546` (`test_never_as_worker_list_names_all_seven_commands` calls it on `_contract()`). S6 row 10 (`:38`) uses `/sc:sweep`. | - |
| B-10 | RESOLVED | The S5 header (`:12`) is narrowed. Rule 2 (`:61`) says `exited` is guide text only (GQ-37 [UNVERIFIED], `gaps:60`) and is built against synthetic fixtures (step 1.8). | MINOR note N-2: `:61` points to "Open Questions 8.2", but GQ-37 sits in the 8.1 "Gaps sent to Open Questions" subtable (`:195`), not in the 8.2 OQ table (`:209-225`). This is a pointer fault on a true claim. |
| B-11 | RESOLVED | S2 R-2 (`:172`) lists WC-14 clauses G1, G2 and G5 and omits G7 with its reason (GQ-10 is an owner decision; the writer is a separate row). It states "For these rows R-2 wins over R-1 ... source severity is kept in the Severity cell". G1 (`:181`) Critical; G2 (`:182`) and G5 (`:185`) "Critical (R-2, unwired; source severity Important, N-32)"; G7 (`:187`) "Important (N-32; R-1, outside R-2's list)". Sources: `gaps:20` (severity follows N-32), `:27` (GQ-04 Critical), `:28` (GQ-05 Important), `:31` (GQ-08 Important), `:33` (GQ-10 Important, owner decision). A Grep of S1 and S3-S6 for G2, G5 or G7 next to a severity word found no conflicting rating. | - |
| B-12 | **OPEN (IMPORTANT)** | The fix was applied at S3 R4 `:216` and R7 `:219`, at S2 `:90` and `:152`, and at S5 step 1.5 `:63`. But **S3 `:114` still reads "Phase 1 can keep person-wait time out of any age it prints."** That is the very claim B-12 flagged, and it contradicts R4 on the same page (`:216`: the waiting list "prints and sorts on the question's original age"). It also contradicts `scope-04:87` (#409 keeps "original age") and S5 `:63`. | Required fix: change S3 `:114` to "Phase 1 keeps person-wait time out of activity ages and the 6 h activity window; the waiting-on-a-person list prints the time since the wait began (R4)". The fix log does not list `:114`, so the fix was incomplete. |
| B-13 | RESOLVED (with note) | S3 `:183` no longer says "no external source contradicts WC-10". It names D5 (Grafana), D6 (agents-fleet) and D2 (Nagios, in part) as contradicting and rejected, and limits Kubernetes support to "node status at the status layer". | MINOR note N-3: D1 (`:169`, Kubernetes taint/evict after `Unknown`) is also rejected under WC-10 but is not counted in the "three". Graded MINOR, not IMPORTANT: `:183` already scopes Kubernetes support to the status layer, `web-01:186` makes the same status-versus-eviction split, and D1's rejection is stated in the D-table, so nothing in the design changes. Suggested wording: "four ... including Kubernetes eviction (D1)". |
| B-14 | **OPEN (IMPORTANT)** | OQ-13 was added (S5 `:225`), X-7 restated (`:262`), row 98a added (S6 `:145`), and the headers marked (S1 `:5`, S3 `:7`, S4 `:3`, S6 `:3`). But **S5 `:10`, the plan's row labelled "Research question", lists seven classes including "fenced"**. That is a false statement of the research question: the task file `:54` lists six, without fenced, and OQ-13 on the same page (`:225`) says "the research question lists six". The B-14 defect (six versus seven presented inconsistently as the research question's list) survives in the plan's own header. | Required fix: in S5 `:10`, list the research question's six classes and add "(Section C adds fenced as a seventh; OQ-13)", as the other four headers do. |
| B-15 | RESOLVED | S6 row 27 (`:55`) prints the worktree-tree root path as the scope line (`scope-04:360`). Row 28 (`:56`) says list everything, shown equals total, with the 100-row truncation form (`scope-04:361`). Both are marked as open plan decisions (`gaps:55-56`) and match S5 `:63` and `:159`. | - |

## Extra edits outside the finding list

| Edit | Result | Evidence |
|---|---|---|
| S5 step 1.5 (`:63`), B-12 wording | PASS | "person-wait time is excluded from activity ages and the activity window, while the waiting list prints and sorts on time since the wait began". This matches R4/R7 (S3 `:216`, `:219`), `web-01:170-173`, `:205` and `scope-04:87`, `:93`. The tie-break is not stated, but `scope-04:91-93` leaves it unspecified too (not a defect). |
| S6 row 33a (`:62`), GQ-48 | PASS | Matches `gaps:71` ("could not determine: message listing truncated at 100") and S5 `:62-63`. Numbering "33a" is cosmetic. |
| S6 row 98a (`:145`), six versus seven | PASS | It is under 9.4 Contradictions, names Section C `research-notes.md:188`, `:194` and points to OQ-13 with the working default. Consistent with S2 4.8 `:284`. |

## Owner-decision honesty (OQ-11, OQ-13)

- **OQ-11** (S5 `:223`) is tagged "decision". It lists G6, GQ-10, GQ-11, GQ-35 and GQ-61 (plus GQ-63), and each has its working default named. The steps that use those defaults (1.17 `:90`, 8.1 rows `:138`, `:158`, `:159`) say "working default" or "pending owner decision". This is honest: no step presents an owner decision as made. The minor gap is N-1 (steps 1.5 and 1.6 do not repeat the qualifier).
- **OQ-13** (S5 `:225`) is tagged "decision". It states the research question's six against Section C's seven and names the working default. This is honest **in OQ-13 itself**. The plan header S5 `:10` contradicts it (B-14 OPEN above): a reader of the plan's first table sees the seven-class list attributed to the research question.
- **B-15** (S6 rows 27, 28) is marked "plan decision, open", which matches `gaps:55-56`. Honest.

## New findings

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| N-1 | MINOR (note) | S5 steps 1.5 `:63`, 1.6 `:64` | `.dev/` location and `495eb96d` pin are stated without "working default (OQ-11)". | Optional: add "(working default, OQ-11)". |
| N-2 | MINOR (note) | S5 `:61` | Pointer says "Open Questions 8.2"; GQ-37 is in the 8.1 subtable `:195`. | Optional: change to "8.1". |
| N-3 | MINOR (note) | S3 `:183` | D1 (Kubernetes evict, `:169`) is rejected under WC-10 but is not counted among the contradicting sources. | Optional: name D1 as the eviction layer of Kubernetes. |

There are no new blocking findings. The fixes introduced no regression: none of the 13 RESOLVED rows contradicts another synthesis file, as checked by Grep across S1-S6 for the severity, class-list and wait-age terms.

## PASS set and failure count

- **PASS (resolved):** B-01, B-02, B-03, B-04, B-05, B-06, B-07, B-08, B-09, B-10, B-11, B-13, B-15 (13 items), plus the three extra edits.
- **OPEN blocking:** B-12 (S3 `:114`), B-14 (S5 `:10`).
- **|F_0| = 15, |F_1| = 2.** The count strictly shrank, so there is no monotonicity halt. There is no regression: no PASS item from a previous cycle now fails. This is fix cycle 1 of at most 2, so one more fix cycle is allowed. Both residuals are single-sentence edits.

## Confidence and tool engagement

- **Confidence:** Verified: 19/19 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (15 findings, 3 extra edits and 1 honesty judgment, each checked by a Read, Grep or line print of the cited synthesis and source lines this pass)
- **Tool engagement:** Read: 15 | Grep: 8 | Glob: 1 | Bash: 5 (Bash was used for read-only line prints of the cited lines; no file was modified except this report)

## Verdict: FAIL
