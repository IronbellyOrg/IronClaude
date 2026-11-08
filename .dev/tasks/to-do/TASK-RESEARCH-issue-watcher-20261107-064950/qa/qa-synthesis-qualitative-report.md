# QA Report - Synthesis Qualitative (synthesis-coherence)

**Topic:** GitHub issue watcher research (issue #331, IronbellyOrg/IronClaude)
**Date:** 2026-11-07
**Phase:** synthesis-qualitative (lens: synthesis-coherence)
**Fix cycle:** N/A
**Status:** Complete
**Fix authorization:** false (report only)

---

## Scope and method

- Spawn prompt: line 253 of the task file, read verbatim (Read offset 253 limit 1). Report-only; no synthesis or research file was modified.
- Read in full: `synthesis/synth-01..04` (all pages), `research/research-notes.md` (ADDENDUM and ADDENDUM 2), `.dev/issues/331/issue-summary.md`.
- No `## Inherited Structural Verdict` block was in the spawn prompt, so this review ran standalone (no reliance on rf-qa PASS items).
- Local read-only spot checks against source: `claim.md`, `WORKER-CONTRACT.md`, `main.py`, `tests/cli/test_cli_registration.py`, `origin_repo.py`, `issue.md`, workflows, `ci.py`, the launch-level design, `labels.md`, `ccsession-orca`, `/opt/Orca/.../agent-launch*.js`, `poll-augment-review.sh`, plus read-only `gh` calls (help text, issue events, issue comments, label list, repo visibility).

## Findings log (appended incrementally)

### BLOCKING findings

**F1 - IMPORTANT - Requirement Scoring applies its own convention unevenly, so the tally (A 2, B 5, C 6, D 3 Meets) is not decision-grade.**
- Where: `synth-03-options-recommendation.md`, "Requirement Scoring" (convention paragraph, R2, R3, R4, R9, R10 rows) and "Tally"; carried into 7.2 ("By raw count B and C score above A").
- Evidence: the convention says cells that depend on the unbuilt Coder#477 listener are Partly. The same paragraph then exempts "(design level)" cells as "conditional on the listener existing". R10 for B ("idempotency key stored at the receiver") and R9 for B ("listener-side log") depend on that listener, yet both are Meets. R3 for B and C is Meets with no qualifier although it needs a PAT or App secret that does not exist and org token policy that the synthesis itself lists as [UNVERIFIED] (W01 Gaps 7). R4 for C is Meets on the strength of a webhook receiver and App that are unbuilt. Meanwhile A's R3, R4 and R6 are Partly for facts that synth-03's own "Reading the scores honestly" says are "closable by setup" (one `gh auth refresh`, one live call). Same standard, opposite outcomes.
- Why it blocks: a reader deciding whether to revisit B or C will read the tally as 5 and 6 versus 2. The convention text and the cells contradict each other.
- Required fix: apply one rule to all four options. Either (a) rate every cell on what exists today (B and C then drop R2, R3, R4 (C), R9, R10 to Partly, and A's setup-closable cells stay Partly), or (b) add a second column "Meets once built/set up" for all four options, A included, and tally both columns. Then recompute the Tally and reword 7.2 "Where A scores lower".

**F2 - IMPORTANT - The plan states an at-most-once layer ("post-write re-read") that the algorithm does not contain and that SC-13 forbids.**
- Where: `synth-04-plan-questions-evidence.md`, Phase 5 intro ("best-effort exclusion across logins (intended-owner filter, own claim marker, post-write re-read)") and Phase 1 step 1.7 ("Layers ... post-write re-read"); also `synth-03` 6.1 step 5 and 7.4 (the optional reservation for candidate 4).
- Evidence: the `run_cycle` table has no step after the launch. Step 8 is a re-read before the launch, not after a write. The poller never writes to GitHub (`synth-02` SC-13: "no write-shaped `gh` call is made by the poller"; `synth-04` step 4.5 asserts it). The only write to the issue is the claim's `--add-assignee @me` (`claim.md:47`, verified by Read), which runs later in a different session. A "post-write re-read" would only exist for routing candidate 4 (poller adds `@me`), which the plan does not implement.
- Why it blocks: the design doc (step 1.7) is told to record a guarantee layer that the code and tests do not build. Contradiction between plan prose and plan algorithm.
- Required fix: replace "post-write re-read" with "pre-launch re-read (step 8)" in Phase 5 intro and step 1.7, and state that a post-write re-read belongs only to candidate 4 and is not built.

**F3 - IMPORTANT - The approval check (filter 2) fails open when the events read hits its page cap.**
- Where: `synth-04`, step 4.2 (`label_events(..., max_pages: int = 5)`, "`max_pages = 5` is a [PROPOSAL]"), step 4.3 (`is_approved`: "latest event for `cfg.approval_label` by `event_id` order"), and the `run_cycle` table step 5.
- Evidence: I ran `gh api --method GET repos/IronbellyOrg/IronClaude/issues/331/events -F per_page=100`. The list is oldest first (first item `labeled` 2026-10-30, last item `subscribed` 2026-11-07). A cap of 5 pages x 100 therefore drops the newest events. If the cap is reached, `is_approved` still takes the "latest" event among the older ones, so a later `labeled` by a non-approver (after an approver's label was removed) is never seen and the issue is treated as approved. Neither step says what happens when the cap is reached. The repo's own precedent reads all pages: `poll-augment-review.sh:51` loops `page<=1000` (verified by Grep).
- Why it blocks: "human-approved" is the only human gate in the design, the repo is public, and the plan specifies the check as passing on partial data. Likelihood is low (needs more than 500 events on one issue), but the behaviour is unspecified and the fix is one sentence.
- Required fix: in steps 4.2, 4.3 and the cycle table, specify that reaching `max_pages` without reaching the end of the list makes `label_events` raise `CommandError("E-GH-TRUNCATED")` and the issue is rejected with reason `approval-unverifiable`. Add a test to `test_selection.py` or `test_github_reads.py` that feeds a full last page and asserts rejection.

### NON-BLOCKING notes (MINOR; recorded, never fail the gate)

- **M1** Revisit conditions exist in two different "nine" lists. `synth-02` 5.15 has conditions 7 (event-time reaction) and 8 (change history) separate and no "workspaces cannot run a recurring poller"; `synth-03` and `synth-04` have 7 combined, 8 shared ledger, 9 poller cannot run. Condition numbers 7 to 9 mean different things in the two lists. Harmonise when the report is assembled (use the `synth-03` list).
- **M2** "Q" numbering collides across files. `synth-02` "Carried to Open Questions" uses Q1 to Q19 (its Q3 is the same-login race), `synth-04` Section 9 uses Q1 to Q33 (its Q3 is `--retry-launch`, its Q14 is the same-login race). Plan steps cite the `synth-04` numbers. Keep only the `synth-04` numbering in the assembled report.
- **M3** `synth-01` 2.3 tags "whether `gh issue list --json` exposes a native issue-type field" as [UNVERIFIED]. `gh issue list --help` on this host lists `issueType` and `projectItems` among the JSON fields (verified by running it), and `synth-02` 5.5 already says the field exists. Update the `synth-01` line and Open Question 5.
- **M4** `synth-04` step 1.10 lists the owner-run live checks as "Q1, Q2, Q3, Q6, Q7, Q8, Q15"; step 7.6 lists eight checks that also cover Q11 and Q17 and do not mention a separate Q2/Q3 check. Align the two lists.
- **M5** `synth-04` Q11 says the REST comment author field name "is not shown". The live read of issue #331 comments shows it is `user.login` (and `author_association` is present), so the `marker-jq` in Phase 4 is right and Q11 can drop that sub-question. The live read also shows the claim marker `<!-- sc:issue:claim -->` on a comment by `ironbelly`, which supports the marker design.
- **M6** Intended-owner rule is open (Q4, 7.9 item 1) but `synth-04` acceptance criterion 4 (step 6.4) and step 7.4 write "assigned to the own login only" / "as implemented (routing candidate 1)" as the rule. The rows are flagged [PROPOSAL] and open, so this is not an assumed owner decision, but criterion 4 should read "default rule (candidate 1), subject to Q4".
- **M7** Gap G7 is rated Critical and option A's R10 cell stresses cross-login double claims. With the routing the plan implements (candidate 1: issue assigned to the own login and nobody else), a second login's poller skips the issue and a manual claim by that login stops at `claim.md:41`. Only the same-login multi-workspace case and a failed-after-Wave-3 claim remain. State this next to G7 and R10 so the severity is conditioned on the routing candidate.
- **M8** Section 7 (7.1 to 7.9) never restates the three questions of issue #331 as a block. They are answered in `synth-01` Section 1 (table) and per option in 6.1 to 6.4, which is enough, but 7.1 should carry a three-line answer. It also gives no B-versus-C preference if a push design is revisited (issue question 1 literally asks microservice versus Action); the revisit table only says "B or C" for most conditions and C for condition 7.
- **M9** Options B and C share steps 4 to 7 (same sender contract, same Coder#477 listener) and differ in sender host only; D is A plus a workflow and the synthesis itself says it "collapses to A" when the token can read the Project. The four options are therefore two families (pull, push) with variants. The synthesis is honest about it; say so in one sentence in 6.0.
- **M10** A's Risk is rated "Medium" (6.1) while the same file's Open Questions rate the live-launch check (Q1), host prerequisites (Q5) and permission posture (Q6, "High (security)") as High, and 7.3 describes all three legs of the lethal trifecta as present. The risk is shared by all options so it does not change the ranking, but the Risk row should point to 7.3 so it is not read as the whole risk.
- **M11** The cost figure "0.24 percent of the allowance per call type" is for one call per poll. The plan's own cycle can make up to about 2 + 4 x `max_candidates` (10) = 42 calls per poll (about 504 an hour, roughly 10 percent of 5,000, more if several workspaces share one login). Still affordable, but 6.1 Pros and 7.2 should quote the plan's worst case, not the one-call figure.
- **M12** The `superclaude` CLI itself (with the new verb) must be installed in each workspace for the scheduler line to work; it is not in the 3.3 environment list or Q5. Add it.
- **M13** Design-doc ID collision: `synth-04` uses D1 to D6 for owner decisions, while the house design format (`sc-issue-command.md`) uses `B1..` for binding decisions and `D1..` for defaults (step 1.9 plans a Defaults table "IDs `D1..`"). Rename the owner decisions `B1..B6` in the design doc.

---

## Overall Verdict: FAIL

## Items Reviewed (the nine evaluation points of the spawn prompt)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Findings build logically from current state to gaps to options to plan | PASS | synth-01 2.1 to 2.5 feeds synth-02 G1 to G30 (each gap cites a current-state fact), which feeds synth-03 scoring (carried-gap list in 4.5) and synth-04 phases. Spot checks of cited facts held: `claim.md:26,29,37,39-43,47` (Read), `WORKER-CONTRACT.md:23,39,61,93` (Grep), `main.py:555-565` (Read), 15 names in `EXPECTED_TOP_LEVEL_COMMANDS` with `swarm` and `reflect` absent (Read), `origin_repo.py:74,102,156,177` (Grep), `issue.md:15,24,82` (Grep), `launch-level-guard` absent from `src` (Grep). Notes M1, M2 only. |
| 2 | Conclusions proportionate to evidence | FAIL | F1 (tally built on an unevenly applied convention); notes M7, M10, M11. Hedging elsewhere is good: the double-claim race is tagged derived and unobserved, rate-limit arithmetic re-computed and correct (12 x 1 = 0.24 percent; 288 x 30 x $0.006 = about $52), the `claude -p` finding is kept at docs level. |
| 3 | Contradictions between research files resolved or flagged | PASS | synth-02 4.4 and synth-03 6.0 list six contradictions with the stronger source named. I re-checked the assignee predicate (research 02 section 2c, Grep: amended text present), the option-letter clash (web files vs ADDENDUM 2 naming, mapped by description), rate limits (web-01 over web-02 J3), and the stale-doc items (`ci.py` imports only `re`, `.classifier`, `.models`, Grep; `test_cli_registration.py:28-30` comment contradicted by the set, Read). Residual cross-file drift is note M1 to M5. |
| 4 | Four options genuinely distinct | PASS (note M9) | A pull poller, B Action + listener, C service + listener are architecturally distinct on inbound exposure, token holder and decision point. D is A plus a workflow and the synthesis says so. |
| 5 | Recommendation follows from comparison and answers the three issue questions | PASS (notes M8, M10) | The recommendation is the owner's decision and is presented as such; 7.2 states where A scores lower. Issue question 1 (microservice vs Action): answered "neither" in synth-01 Section 1; question 2 (account binding): A = the workspace's own `gh` login, with the owner-equals-login gap flagged; question 3 (Coder-side listener): none under A, poller is the whole component. The issue's text matches `.dev/issues/331/issue-summary.md` lines 8-10 (Read). |
| 6 | Plan consistent with recommendation and fit to this repo | FAIL | F2 (plan prose vs algorithm), F3 (approval check specified on partial data). Repo fit is otherwise sound: registration block position, `noqa` marker, no `pyproject.toml` change, no `.claude/` mirror, `gh project item-list --query/--limit/--owner/--format json` all exist in local `gh` help (run), `gh issue list --json` has `issueType` and `projectItems` (run), PATH-stub test precedent exists. Notes M4, M5, M6, M12, M13. |
| 7 | Owner decisions recorded as decided; B, C fairly scored with revisit conditions; Coder#477 stated | PASS | Grep over `synthesis/` for "pending owner", "not decided", "do not favor", "must not present A" found only the quotation of the superseded rule in synth-01 line 35 (marked superseded) and an unrelated "location not decided" at synth-03 line 220. 7.1 reads "decided by the owner (ADDENDUM 2)". D1 to D6 in synth-04 9.1. Coder#477 statement (filed assuming a push design; unnecessary under A unless B or C is revisited; Coder repo boundary) appears in synth-01 1.2, synth-02 3.4 and G18, synth-03 7.7, synth-04 D5. B and C each have description, flow, assessment, three-question answers and nine revisit conditions. Note M6 on criterion 4. |
| 8 | External research is a supplement, never an override | PASS | synth-02 Section 5 opens with the rule and ends "No external finding contradicts a verified code finding"; web claims carry [EXTERNAL-VERIFIED] or [UNVERIFIED]; local runs of `gh` help and live GETs agree with the code findings and with the web file on `--query`, `--limit` and the events order. |
| 9 | No circular arguments; unverified assumptions not stated as fact | PASS (notes M3, M5, M11) | Each [UNVERIFIED] item is carried to a numbered open question in synth-01, synth-02, synth-03 and synth-04. The recommendation rests on the owner decision plus code facts (synth-03 "Carried to Open Questions" intro). No claim cites a synthesis file as evidence for itself; evidence is research files and source. |

## Summary
- Checks passed: 7 / 9
- Checks failed: 2 (items 2 and 6)
- Blocking findings: 3 (F1, F2, F3), all IMPORTANT; Critical issues: 0
- Minor notes: 13 (M1 to M13)
- Issues fixed in-place: 0 (report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F1 | IMPORTANT | synth-03, Requirement Scoring, Tally, 7.2 | Scoring convention contradicted by its own cells; B and C get credit for unbuilt pieces that A is denied | Apply one rule to all options, or add a "Meets once built/set up" column for all four; recompute the Tally; reword 7.2 |
| F2 | IMPORTANT | synth-04, Phase 5 intro and step 1.7 (also synth-03 6.1 step 5) | "Post-write re-read" layer is not in the algorithm and conflicts with SC-13 (poller never writes) | Say "pre-launch re-read (step 8)"; note post-write re-read belongs to candidate 4 and is not built |
| F3 | IMPORTANT | synth-04, steps 4.2, 4.3 and cycle step 5 | Page cap on the events read (oldest-first list) lets the approval check pass on partial data | Reaching `max_pages` raises `E-GH-TRUNCATED`; reject with `approval-unverifiable`; add a test |
| M1 to M13 | MINOR | see notes above | Wording, numbering, cross-file drift, small omissions | Optional; fix at assembly |

## Actions Taken
None (fix authorization false). No synthesis or research file was modified. The only file written is this report.

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` section was present in the spawn prompt, so no rf-qa PASS item was relied on.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. The spawn prompt carried no Inherited Structural Verdict; standalone behaviour applied.

**(b) Independent semantic checks (at least one required, INV-019):**
- Convention-versus-cells consistency of the scoring table -- verified by re-reading every R1 to R10 cell of synth-03 against its convention paragraph and recomputing the tally (A 2/8, B 5/5, C 6/4, D 3/7 all match their cells); this produced F1.
- Plan prose versus plan algorithm -- verified by comparing Phase 5 intro and step 1.7 with the 13-step `run_cycle` table and with SC-13 and step 4.5; this produced F2.
- Approval-check robustness -- verified by running a read-only `gh api` events call on issue #331 to establish list order (oldest first), and Grep of `poll-augment-review.sh:51` for the repo's full-pagination precedent; this produced F3.
- Cited line numbers and facts -- verified against source by Read or Grep (claim.md, WORKER-CONTRACT.md, main.py, test_cli_registration.py, origin_repo.py, issue.md, ci.py, workflows, launch-level design, labels.md, ccsession-orca, Orca agent-launch file set).
- Live-state facts -- verified by read-only `gh`: the fork has exactly the nine default labels; it is PUBLIC and a fork; `gh project item-list` has `--query`, `-L` (default 30), `--owner`, `--format {json}`; `gh issue list --json` includes `issueType` and `projectItems`; the REST comment object has `user.login`.

Factual claims independently verified against source or live read-only commands: 44. Files read: the four synthesis files, research-notes.md, issue-summary.md, claim.md, labels.md, main.py, test_cli_registration.py, ccsession-orca, and Grep passes over WORKER-CONTRACT.md, origin_repo.py, issue.md, ci.py, workflows, the launch-level design, poll-augment-review.sh, tests and src. Not independently re-verified (relied on research files, not the source): Orca handler and request line numbers beyond confirming the file set exists, Coder and GitHub web pages, per-workspace host facts.
Web research: none performed in this review (no Tavily or fallback call), so no fallback condition to record.

## Confidence Gate

- Checklist items (the nine evaluation points): TOTAL 9; VERIFIED 9; UNVERIFIABLE 0; UNCHECKED 0.
- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 18 | Grep: 12 | Glob: 3 | Bash: 3 (Read + Grep + Glob = 33, above the 9 checklist items)
- Confidence measures coverage of the checklist, not quality of the work; the verdict is FAIL because of the three blocking findings.

## Recommendations
1. Fix F1: make the scoring rule uniform and recompute the Tally (synth-03).
2. Fix F2: correct "post-write re-read" in synth-04 Phase 5 intro and step 1.7 (and the matching mention in synth-03 6.1 step 5).
3. Fix F3: specify fail-closed behaviour for a truncated events read and add the test (synth-04 steps 4.2, 4.3, 4.5, cycle step 5).
4. Optionally fold M1 to M13 into the same pass; none is required for the gate.
5. Re-review is limited to F1 to F3 (fix cycle 1 of at most 2).

VERDICT: FAIL

## QA Complete

