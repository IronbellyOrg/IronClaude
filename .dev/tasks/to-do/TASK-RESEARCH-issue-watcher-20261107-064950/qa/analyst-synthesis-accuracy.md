# Synthesis Accuracy and Source-Tracing Analysis

**Topic:** GitHub issue watcher research (issue #331 of IronbellyOrg/IronClaude)
**Analysis type:** synthesis-accuracy (rf-analyst, report-only, fix_authorization false)
**Date:** 2026-11-07
**Status:** Complete

---

## Method and scope

Read in full: research-notes.md (both addenda), synth-01 (508 lines), synth-02 (468), synth-03 (539), synth-04. Research files and gaps-and-questions.md are traced by targeted grep and Read for each claim sampled (see the Source-tracing log below). Working notes are appended as the review proceeds.

## Early notes (appended during the read, before checklist grading)

- N1. synth-03 Section 6 tally recomputed from the Requirement Scoring table: A 2/8/0, B 5/5/0, C 6/4/0, D 3/7/0. The tally matches the table. Arithmetic is correct.
- N2. synth-02 section 5.15 lists nine revisit conditions with 7 = event-time reaction, 8 = change history, 9 = shared ledger. synth-03 "Revisit conditions" and synth-04 "Revisit conditions" list nine conditions but merge event-time and change history into 7, make 8 = shared ledger, and add 9 = "workspaces cannot run a recurring poller" (marked DERIVED). The lists differ although synth-04 step 1.2 says to copy "the nine revisit conditions". To be traced to W02 J3.
- N3. synth-03 6.0 uses `.dev/issues/331/issue-summary.md` ("SUM") as a requirements source. That file is outside research/ and gaps-and-questions.md. Existence to be checked. (Checked: the file exists at `.dev/issues/331/issue-summary.md`; it is an input of the claim step, not a research file, so it is a legitimate but extra source.)

## Addendum conformance (blocking checks, grep-verified against the four synthesis files)

| # | Required by the addenda | Result | Evidence |
|---|---|---|---|
| AC1 | Recommendation is option A labelled "decided by the owner" | PASS | synth-03 line 351 "Option A, the workspace-side poller, decided by the owner (ADDENDUM 2)"; synth-03 6.1 heading "Decided by the owner" |
| AC2 | The words "pending owner decision" appear nowhere | PASS | grep for `pending owner decision`, `pending the owner`, `owner is being asked`, `awaiting owner` over `synthesis/` returned no match |
| AC3 | B, C and hybrid scored against the issue's stated requirements, with revisit conditions | PASS | synth-03 6.0 requirements R1-R10, 6.2 B, 6.3 C, 6.4 D, Requirement Scoring table, nine revisit conditions (synth-03 lines 327-343), synth-02 5.15 and synth-04 closing table repeat them |
| AC4 | Coder#477 cited as sibling dependency with the boundary (listener, registration, transport live in the Coder repo) and the statement that it was filed assuming a push design and A makes it unnecessary unless B or C is revisited | PASS | synth-01 1.2 (lines 45-51); synth-02 3.4 row 2 and G18; synth-03 7.7; synth-04 D5 (line 406) and follow-up row |
| AC5 | Integer-only prompt rule stated | PASS | synth-03 7.3 "Prompt (Q3)"; synth-04 Phase 1 "Integer-only prompt rule recorded in the doc", step 3.2 |
| AC6 | Sender authentication, Coder app exposure and watcher-to-listener contract appear in Section 5 | PASS | synth-02 5.13 (sender authentication), 5.14 (`coder_app` sharing), 5.15 (minimal contract) |
| AC7 | B and C not excluded by assertion; Target State does not use "no inbound endpoint/listener/port" as a requirement or pre-filter | PASS | Grep for `no inbound (endpoint|listener|port)` shows the phrase only as a statement of the owner's decided option (synth-01 lines 25, 39; synth-02 line 86 under "Consequences of the owner-decided option A (stated as consequences, not as pre-filters)"; synth-03 option A description, scored row R8 and "Inbound exposure (one scored criterion, not a pre-filter)"). Section 3 success criteria SC-1..SC-17 and constraints 3.3 contain no such requirement |
| AC8 | Plan targets A with B and C only as follow-up | PASS | synth-04 8.1 "Does not build", "Follow-up, not in this plan" table |
| AC9 | Scope is claim-only, decided by the owner | PASS | synth-01 1.1 Q2 row; synth-03 7.3 "Claim-only (Q2)"; synth-04 D2 |
| AC10 | `ci.py` stated NOT a `gh` subprocess wrapper (imports only `re`, `.classifier`, `.models`) | PASS | synth-01 line 242 (`ci.py:10-15`), synth-02 G2, synth-03 7.6, synth-04 C4 |
| AC11 | A poller needs its own injectable runner | PASS | synth-01 line 243, synth-02 G2, synth-04 step 2.2 (`runner.py`) |
| AC12 | `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md` stated to have been corrected on this point | **FAIL (BLOCKING)** | Grep for `codebase-context` over `synthesis/` returns zero matches. The correction exists in the source (codebase-context.md line 21 "CORRECTION (2026-11-07, research alignment check): `src/superclaude/pr_submit/ci.py` is NOT a `gh` subprocess wrapper...", and gaps-and-questions.md line 35 says "research-notes.md and `enrichment/codebase-context.md` carry the correction"), but no synthesis file says so. synth-02 G29 says only "corrected in research-notes.md". The prompt makes a missing statement a blocking finding |

### Blocking finding B1 (AC12)
- **Where:** all four synthesis files, most naturally synth-01 Section 2.3 bullet "Where `gh` is actually invoked" (line 242, the `[CODE-CONTRADICTED]` ci.py bullet), plus synth-02 G2/G29 notes and synth-04 carry-over row C4 (line 456).
- **Problem:** The synthesis does not state that `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md` was corrected on the `ci.py` point. The brainstorm artifact is a downstream consumer of this research; a reader of the report cannot tell whether that file still carries the wrong claim.
- **Fix:** In synth-01 line 242 and synth-04 row C4, add: "The same wrong claim in `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md` was corrected there (line 21, 'CORRECTION (2026-11-07, research alignment check)') and in `research/research-notes.md` (EXISTING_FILES row for `ci.py` and PATTERNS_AND_CONVENTIONS)." Mirror it in synth-02 G29 Notes (replace "corrected in research-notes.md" with both files).

## Source-tracing log (claims traced to the repo and to the research files)

All items below were re-read against the live worktree or the research file on 2026-11-07. Result: VERIFIED unless stated.

| Claim in synthesis | Checked against | Result |
|---|---|---|
| `issue.md:15` (stops, never runs next steps), `:24` (explicit only), `:71`, `:79`, `:83` (Will Not) | `src/superclaude/commands/issue.md` | VERIFIED (lines 15, 24, 71, 79, 83 match) |
| `WORKER-CONTRACT.md:11, :23, :39, :40, :61, :93, :112` | `src/superclaude/core/WORKER-CONTRACT.md` | VERIFIED (never-as-worker list at 23; WC-13 at 61; "never starts with `/sc:`" at 93) |
| `claim.md:15, :20, :39-42, :47, :80, :89, :90` | `refs/claim.md` | VERIFIED |
| `labels.md:7` ("`--claim` changes no labels"), `:20`, `:22-42` | `refs/labels.md` | VERIFIED |
| `origin_repo.py:74` `_NUMBER`, `:77` ClaimError, `:135` case-insensitive compare, `:156` read_origin, `:177` main, exit table `:45-50` | `scripts/origin_repo.py` | VERIFIED |
| `ci.py` imports only `re`, `.classifier`, `.models` (`:10-15`) | `src/superclaude/pr_submit/ci.py` lines 10-15 | VERIFIED |
| `detection.py:273` `_fetch_payload` and comment at `:268` | `src/superclaude/pr_submit/detection.py` | VERIFIED |
| `main.py:559-561` reflect registration, `:564` `__main__` | `src/superclaude/cli/main.py` | VERIFIED |
| `hooks.json:96-105` launch-job-identity registration | `src/superclaude/hooks/hooks.json` line 101 | VERIFIED (command string at 101; no `launch-level-guard` entry) |
| `test.yml:4-8` triggers, `:151-158` permissions and persist-credentials, `:191-194` test-summary needs | `.github/workflows/test.yml` | VERIFIED |
| `fallback.py:39`, `init_lite.py:221 _atomic_write`, `poll-augment-review.sh:53-55 --method GET -F per_page=100` | respective files | VERIFIED |
| Design doc `sc-issue-launch-level-hook.md:23` ("enforces"), `:40` ("proposed"), `:6` status line | design doc | VERIFIED |
| ccsession `:136-141`, README `:534-535` skip-permissions wording | `ccsession-tag/ccsession`, `README.md` | VERIFIED (default flags at 137; README 535 states `CC_CLAUDE_FLAGS` default) |
| Collaborator counts 1 admin / 2 maintain / 8 read / 0 triage | research/03 line 127 | VERIFIED as research text (observed value, not re-run) |
| Nine revisit conditions "taken from W02 J3" | research/web-02 J3 (lines 308-315) and web-01 14.5 | PARTLY: W02 J3 has six items. Items 7-9 of synth-02 come from web-01 14.5 (event-time, change history, shared ledger), which is traceable. synth-03/04 item 9 is not in either file (see M1) |
| Requirement source `.dev/issues/331/issue-summary.md` "What the issue asks for" | file exists, heading at line 8 | VERIFIED |
| Orca paths under `/opt/Orca/...` | not re-opened by this review; they are cited as read by research/01 | NOT RE-VERIFIED (carried as research-level evidence; tags in synth-01 are as the research states) |

## Checklist results (Synthesis Quality Review, 10 items)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Section headers match Sections 1-10 split 1-2 / 3-5 / 6-7 / 8-10 | PASS | synth-01 `## 1. Problem Statement`, `## 2. Current State Analysis`; synth-02 `## 3. Target State`, `## 4. Gap Analysis`, `## 5. External Research Findings`; synth-03 `## 6. Options Analysis`, `## 7. Recommendation`; synth-04 `## 8.`, `## 9.`, `## 10.` |
| 2 | Table column structures | PASS | Gap table: Gap / Current State / Target State / Severity / Notes (synth-02 line 108). Options: Criterion by option (synth-03 lines 280, 312). Plan: Step / Action / Files / Details (synth-04 throughout). Section 9 table is # / Question / Impact / Suggested Resolution |
| 3 | No fabrication | PASS with notes | Sampled claims trace (log above). Items not in research are labelled [PROPOSAL] or [DERIVED] (all synth-04 NEW paths, defaults 60 min / 3 / 1 / 10, exit codes, the stricter `build_claim_prompt`). Revisit item 9 in synth-03/04 is the synthesizer's own and is labelled DERIVED (M1) |
| 4 | Findings cite paths and evidence | PASS | Every Section 2 row carries file:line; verified sample above |
| 5 | At least 2 options with pros/cons tables | PASS | Four options A-D each with a Pros/Cons assessment table (synth-03 6.1-6.4) |
| 6 | Plan has specific steps with file paths | PASS | synth-04 Phases 1-7 name concrete files (`src/superclaude/cli/issue_watch/*.py`, `tests/issue_watch/*`, `docs/designs/issue-watcher.md`, `main.py` after l.561); NEW paths labelled as proposals |
| 7 | Cross-references consistent | PASS with minor notes | Gaps G1-G30 map to Section 8/9 rows (synth-04 coverage table GAPS row; Q1-Q33). Q-number references in steps match Section 9 rows (checked Q1-Q17, Q23). Minor inconsistencies M1, M2 below |
| 8 | No doc-only claims in Sections 2, 6, 7, 8 | PASS | Doc-only items are tagged `[UNVERIFIED — doc-only, no code confirmation]` (synth-01 lines 296-298, 349) and kept out of the 2.5 diagram. Plan relies on code-verified facts or [PROPOSAL]s |
| 9 | Stale-doc discrepancies surfaced | PASS | synth-02 G26-G30, synth-03 6.0 contradictions 1-6, synth-04 9.3 C1-C11 (ci.py, mock_gh, frozen-snapshot comment, private-fork, launch-level doc, hooks README, third-party headless mirror) |
| 10 | Key-finding coverage | PASS | Summary sections of research/01, 02, 03, web-01, web-02 compared with the coverage tables of synth-02 (lines 442-466), synth-03 (457-511) and synth-04 (499-550). No dropped Summary finding found; exclusions carry rationale (ClickUp, Actions billing, Copilot/OpenHands/Codex, hooks README) |
| – | Web claims keep URLs and external-context marking | PASS | synth-02 Section 5 intro states external context and tavily-unavailable provenance; every row has a source URL; synth-03/04 cite W01/W02 keys and mark "external context" where relied on |
| – | Addendum conformance | FAIL on AC12 only | See the conformance table and B1 above |

## Minor findings (notes, do not fail the gate)

- **M1. Revisit-condition lists differ.** synth-02 5.15 lists nine conditions (7 event-time, 8 change history, 9 shared ledger). synth-03 "Revisit conditions" and synth-04's closing table list nine with 7 = event-time or history, 8 = ledger, 9 = "workspaces cannot run a recurring poller" (marked DERIVED, source W02 A1/A4/A5, GAPS 9). W02 J3 itself has six items; synth-03 says "Each is taken from the research files", which overstates for item 9. synth-04 step 1.2 says to copy "the nine revisit conditions". Fix: pick one list of nine, put it in one place, and have the other sections point to it; reword synth-03's sentence to say item 9 is the synthesizer's derivation.
- **M2. Live-test checklist differs.** synth-04 step 1.10 lists Q1, Q2, Q3, Q6, Q7, Q8, Q15 as the owner-run checks, while step 7.6 has eight checks including Q11 (comment author field) and Q17 (worktree path). Align 1.10 to 7.6.
- **M3. File length stated two ways.** research-notes.md gives `origin_repo.py` as 195 lines; synth-01 says "196 lines". Not re-counted here; harmless.
- **M4. `labels.md:22-42` span.** The creation lines sit at lines 27-41 under the heading at line 22; the span is correct as a section range.
- **M5. Orca paths not independently re-opened.** `/opt/Orca/...` citations (synth-01 section 2.2) are research-level evidence; this review did not re-open them. They are tagged as read by R01 and the unverified parts stay tagged UNVERIFIED.
- **M6. synth-03 requirement R10 and the extra source `.dev/issues/331/issue-summary.md`.** R10 (at-most-once) is attributed to NOTES and R01/R03, not to the issue text; acceptable, since it is labelled by source.

## Summary

**Status:** Complete

- Files reviewed: 4 synthesis files; research notes, research/01-03, web-01, web-02, gaps-and-questions.md consulted; about 30 code citations re-checked against the worktree, all matched.
- Blocking findings: 1 (B1: no synthesis file states that `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md` was corrected on the `ci.py` point; the correction does exist at that file's line 21, so the fix is one added sentence in synth-01 line 242, synth-02 G29 Notes and synth-04 row C4).
- Minor findings: 6 (M1-M6), none gate-failing.
- All other addendum conformance checks pass (decided-by-owner Recommendation, no "pending owner decision", B/C/D scored with revisit conditions, Coder#477 boundary and statement, integer-only rule, Section 5.13-5.15, no "no inbound endpoint" pre-filter, plan targets A, claim-only, ci.py statement, injectable runner).

VERDICT: FAIL
