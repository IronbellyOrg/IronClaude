# Fix log: Phase 5 synthesis gate (Gate 2), fix cycle 1

**Date:** 2026-11-07
**Agent:** rf-qa (fix_authorization: true; the only agent allowed to edit synthesis files in this gate)
**Input:** `qa/qa-consolidated-findings-phase5.md` (4 blocking findings; minor findings stay notes)
**Sources read for wording:** `qa/analyst-synthesis-accuracy.md`, `qa/qa-synthesis-structure.md`, `qa/qa-synthesis-qualitative-report.md`
**Edit scope:** `synthesis/synth-01..04` only. No research file and no `research-notes.md` edit.

Status: Complete (one entry per blocking finding below, then a summary).

---

## Finding 1 (consolidated #1): no synthesis file says `enrichment/codebase-context.md` was corrected on the `ci.py` point

**Status:** FIXED. Three one-clause insertions; every cited line was read this session.

| File | Place | Change |
|---|---|---|
| `synthesis/synth-01-problem-current-state.md` | section 2.3, the `[CODE-CONTRADICTED]` ci.py bullet (line 242) | Added: the same wrong claim in `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md` was corrected there (line 21, "CORRECTION (2026-11-07, research alignment check)") and in `research/research-notes.md` (EXISTING_FILES row for `ci.py`, line 30; GitHub-access pattern, line 37) |
| `synthesis/synth-02-target-gaps-external.md` | row G29 Notes (line 138) | "corrected in research-notes.md" replaced by both files, with the `codebase-context.md` line 21 citation |
| `synthesis/synth-04-plan-questions-evidence.md` | section 9.3 row C4, "How the plan handles it" (line 457) | Added the same clause (`codebase-context.md` line 21; `research-notes.md` lines 30 and 37) |

Evidence read: `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md:21` (CORRECTION text present); `research/research-notes.md:30` and `:37` (ci.py correction present); `gaps-and-questions.md:35` (names both files). Verification: Grep for `codebase-context` over `synthesis/` now returns one hit in each of synth-01 (line 242), synth-02 (line 138) and synth-04 (line 457); it returned none before.

---

## Finding 2 (consolidated #2): Requirement Scoring convention applied unevenly

**Status:** FIXED. File edited: `synthesis/synth-03-options-recommendation.md` only.

**Rule written once, applied to all 40 cells** (the "Scoring convention" paragraph above the table): Meets only when the requirement is satisfied by something that exists today or by the option's own described in-repo mechanism, with no dependency on anything unbuilt outside this repo (Coder#477 listener and registry, a GitHub App, a hosted service, a new organization secret or token-scope grant) and no [UNVERIFIED] fact or open rule in the cell; otherwise Partly; Does not meet only when the mechanism cannot satisfy the requirement. A Partly cell stays Partly even when one setup step would close it, for every option alike. The "(design level)" Meets are removed.

**Cells changed (before -> after):**

| Cell | Before | After | Basis (read this session) |
|---|---|---|---|
| R1, C | Meets | Partly | webhook delivery needs the unbuilt central service, hosting not established (synth-03 6.3 step 2; W01 §12) |
| R2, B | Meets (design level) | Partly | no allow-list exists, location and rule open (GAPS 14; synth-03 7.3 Approval) |
| R2, C | Meets (design level) | Partly | same, plus the service is unbuilt |
| R3, B | Meets | Partly | PAT or App secret does not exist; org token policies [UNVERIFIED] (`research/web-01-github-events-projects-and-limits.md:189`, Gaps item 7 at `:219`) |
| R3, C | Meets | Partly | GitHub App and service unbuilt; same policies [UNVERIFIED] |
| R3, D | Meets | Partly | the central PAT or App secret does not exist; same policies [UNVERIFIED] |
| R4, C | Meets | Partly | `projects_v2_item` is an organization-availability webhook event that needs an App with org Projects read (`research/web-01-github-events-projects-and-limits.md:188`), so it needs the unbuilt App and service |
| R9, B | Meets (design level) | Partly | the audit fields sit in the unbuilt Coder#477 listener |
| R9, C | Meets (design level) | Partly | service unbuilt, hosting not established |
| R10, B | Meets (design level) | Partly | idempotency key stored at the unbuilt listener |
| R10, C | Meets (design level) | Partly | service and listener unbuilt |

Unchanged: every A cell (R1 and R8 Meets, the rest Partly), B R1, D R1 and R8 Meets, every R5, R6 and R7 cell. In A's R10 cell and the Options Comparison "At-most-once" row, "post-write re-read" / "re-read" became "pre-launch re-read" (consistent with finding 3).

**Tally recomputed from the cells** (Grep of the `**Meets`/`**Partly` markers per row: R1 = Meets, Meets, Partly, Meets for A, B, C, D; R8 = Meets, Partly, Partly, Meets; every other row all Partly): A 2 (R1, R8), B 1 (R1), C 0, D 2 (R1, R8). Old tally: A 2, B 5, C 6, D 3.

**Every place that quoted the old tally or ranking was updated** (Grep of `synthesis/` for `raw count|tally|score above|Meets (design|design level|A 2|B 5|C 6|D 3`): the Tally table (plus a note that the count is not a measure of design quality); "Reading the scores honestly" bullets 1 and 2 (they now state the count under the rule, name R2, R9 and R10 as properties in which B and C are structurally stronger that the count does not show, and list the setup-closable Partly cells for B, C and D as well as A); the Options Comparison "At-most-once" row; 7.2 rows "Where B and C are structurally stronger than A", "Where A is Partly but closable" and "What the score does and does not say". synth-01, synth-02 and synth-04 never quoted the tally (Grep: no match), so they needed no change. The owner-decision statements (7.1, 7.2: A chosen for removing the listener, inbound port and registry; B and C kept as documented alternatives with the nine revisit conditions) are untouched.

---

## Finding 3 (consolidated #3): "post-write re-read" at-most-once layer that the algorithm does not contain

**Status:** FIXED. Files edited: `synth-04` (3 places) and `synth-02` (3 places, same wording).

Basis read this session: the 13-step `run_cycle` table (synth-04 Phase 5) has no step after the launch; step 8 is a second `snapshot` before the launch; SC-13 (`synth-02` line 60) says a test asserts the poller makes no write-shaped `gh` call; the post-write re-read is the W02 G7 pattern "after assigning `@me`, re-read the assignees" (`research/web-02-coder-claude-dispatch-and-security.md:186`, [PROPOSAL]) and the R01 §9 poller-side reservation for routing candidate 4 (`research/01-claim-flow-and-session-launch.md:157`, UNVERIFIED), which the plan does not build.

| File | Place | Change |
|---|---|---|
| `synth-04` | step 1.7 (design doc section 8 text) | "post-write re-read" replaced by "pre-launch re-read (step 8 of the `run_cycle` algorithm)", plus an instruction to record that a post-write re-read belongs only to routing candidate 4 and is not built because the poller never writes (SC-13, step 4.5) |
| `synth-04` | Phase 5 intro (at-most-once paragraph) | same replacement, and a sentence saying the post-write layer would exist only for candidate 4 and is not built |
| `synth-04` | `run_cycle` table, row 8 | labelled "the pre-launch re-read and the only re-read in the cycle" |
| `synth-02` | row G7 Notes | "a post-write re-read of the assignees" replaced by "a pre-launch re-read of the issue snapshot" with the candidate 4 qualification |
| `synth-02` | Section 5 table row on `POST .../assignees` (Relationship to codebase) | "A post-write re-read ... reduces but does not close the window" reworded: a re-read reduces the window; the plan re-reads before the launch; a post-write re-read applies only to candidate 4 |
| `synth-02` | Section 5 summary row "At-most-once" | "post-write re-read" replaced by "pre-launch re-read (a post-write re-read applies only to routing candidate 4, not built)" |

Left as is on purpose: `synth-03` 7.4 (the optional poller-side reservation for candidate 4, already described as a design suggestion, [UNVERIFIED]). Verification: Grep for `post-write` over `synthesis/` now returns only the five "belongs only to candidate 4 / not built" statements above (synth-02 lines 116, 305, 407; synth-04 lines 108, 213).

---

## Finding 4 (consolidated #4): approval check passes on partial data when the events read hits the page cap

**Status:** FIXED. File edited: `synthesis/synth-04-plan-questions-evidence.md` only.

Basis: the qualitative report's observation was re-run by me with a read-only call, `gh api --method GET repos/IronbellyOrg/IronClaude/issues/331/events -F per_page=100 --jq '[.[0].created_at, .[-1].created_at, length]'` on 2026-11-07, which returned `["2026-10-30T14:39:35Z","2026-11-07T06:48:14Z",9]` (oldest first). The same call on `/comments` returned two comments in ascending time order. The repo's own precedent was read: `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh:46-47` (comment "Explicit page numbers ...", "1000 pages per source; fail incomplete at the cap, never silently truncate") and `:51` (`for ((page=1; page<=1000; page++))`).

| Place in synth-04 | Change |
|---|---|
| Filter 2 table row, "Extra gh calls" | now "1 or more events calls per survivor (... reaching the cap fails closed: step 4.2)" |
| Calls table, "Label events" row, Evidence | added the oldest-first observation on issue #331 and the `poll-augment-review.sh:47`, `:51` precedent |
| Step 4.2 (`github.py`) | added the rule: if page `max_pages` is reached and still full (100 items), `label_events` and `own_claim_comment_ids` raise `CommandError("E-GH-TRUNCATED")` and never return a partial list [PROPOSAL, same rule as `poll-augment-review.sh:47`] |
| Step 4.3 (`is_approved`) | added: it is called only with a complete list; the cycle maps `E-GH-TRUNCATED` to `Decision(selected=False, rejected_by="approval-unverifiable")` |
| Step 4.5 tests | added the truncation test for `label_events` and `own_claim_comment_ids` |
| `run_cycle` table rows 5 and 6 | row 5: `E-GH-TRUNCATED` rejects with reason `approval-unverifiable`; row 6: `E-GH-TRUNCATED` skips with reason `claim-marker-unverifiable` |
| Phase 5 test scenarios | new row "Truncated read" (full pages to the cap give `approval-unverifiable` / `claim-marker-unverifiable`, no `orca` call, no store write; a short last page is decided normally) |

Scope note: the finding names the approval check. The claim-marker read (`own_claim_comment_ids`, same `max_pages = 5` and the same oldest-first list, where the newest comment is the claim marker) has the identical defect, so the same fail-closed rule was applied to it in the same sentences; it adds no new fact beyond the comments-order observation above.

---

## Summary

| Consolidated finding | Resolution | Files edited |
|---|---|---|
| 1. `codebase-context.md` correction not stated | Fixed | synth-01, synth-02, synth-04 |
| 2. Requirement Scoring uneven; tally overstated B and C | Fixed (one rule, 11 cells re-scored, tally A 2 / B 1 / C 0 / D 2, all quotes updated) | synth-03 |
| 3. "post-write re-read" layer not in the algorithm | Fixed (renamed pre-launch re-read; post-write kept only for candidate 4, not built) | synth-04, synth-02 |
| 4. Events read page cap fails open | Fixed (`E-GH-TRUNCATED`, `approval-unverifiable`, test added) | synth-04 |

All 4 blocking findings resolved. Minor findings (M1 to M13 of the qualitative report, M1 to M6 of the analyst report, M-1 to M-4 of the structure report) were not touched, per the instruction. Only `synthesis/synth-01..04` were edited besides this fix log; no research file and no `research/research-notes.md` edit (`git status` shows the whole task folder as one untracked directory, so per-file diff is not available; every Edit call targeted a path under `synthesis/`). Addenda conformance kept: no "pending owner decision" text added (Grep over `synthesis/` for the phrase returns nothing), option A stays "decided by the owner", B and C stay scored with the nine revisit conditions, Coder#477 statements untouched.

Not checked: whether the next re-review (fix cycle 2) accepts the choice of rule in finding 2; the rule is the one the consolidated findings proposed ("Meets only when satisfied by something that exists today or by the option's own described mechanism with no unbuilt dependency; otherwise Partly"), with the unbuilt-dependency list made explicit.

Status: Complete
