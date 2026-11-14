# QA Report: Synthesis Coherence (report-qualitative, adapted) (Partition 1 of 2)

**Topic:** Orchestrator mode Phase 1 (issue #339), `/sc:sweep` read-only coordinator status
**Date:** 2026-11-07
**Phase:** report-qualitative, adapted to synthesis coherence
**Fix cycle:** N/A (first review)
**Fix authorization:** false (report only; no synthesis file edited)
**Assigned files:** `synthesis/synth-01-problem-current-state.md`, `synthesis/synth-02-target-gaps.md`, `synthesis/synth-03-external-findings.md`
**Research sources read for this partition:** `research/research-notes.md` (Sections B and C, :150-229), `research/web-01-agent-supervisor-session-health.md` (grep), `research/web-02-static-status-report-conventions.md` (grep), `gaps-and-questions.md` (grep: :26, :57, :74, :84, :125), `qa/qa-nb4-fix-log.md` (whole, 45 lines), `src/superclaude/skills/sc-crash-recovery/SKILL.md:1-56`, `src/superclaude/core/WORKER-CONTRACT.md` (grep)

[PARTITION NOTE: Cross-file checks are limited to synth-01, synth-02 and synth-03. Full cross-file verification needs the partition 2 report (synth-04, 05, 06) merged with this one. The NB-4 recheck grep covered all six synthesis files, as the coordinator ordered.]

---

## Overall Verdict: FAIL

## Items Reviewed

| # | Check (adapted to synthesis coherence) | Result | Evidence |
|---|---|---|---|
| 1 | Problem statement matches findings: the synthesis answers the research question (a read-only sweep that classifies Orca workers without guessing) | PASS | synth-01 opens with the research question and #339 Phase 1 scope; synth-02 gives the target (sweep CLI group, command, skill, `_orca` seam) and gaps; synth-03 keeps to supervision and status-report conventions. No drift into later-phase actions; actions (abort, retry, close) are marked later-phase. |
| 2 | Current state is current: the code paths described exist now, and planned or unmerged work is marked | PASS | synth-01 places the #409 layout at unmerged `495eb96d` and does not present it as merged; the A4 rejection (crash-recovery skill) cites `SKILL.md:4` (allowed-tools hard-codes `~/workspace/IronClaude/...`) and `:25-27` (`--all` sweeps `~/workspace/`, 72 h default). Read of `SKILL.md:1-56` confirms both: `:4` and `:25-26`. |
| 3 | Options are genuinely distinct | PASS | A1 (Python CLI group + command + skill), the skill-only option and A4 (extend sc-crash-recovery) differ in where the reads run and who owns the seam. A4 is kept as rejected in all three files, not reintroduced. |
| 4 | Recommendation follows from analysis; ratings in a section agree with the rule that section states | FAIL | synth-02 R-2 (:172) says G1, G2, G5 and G7 unwired is Critical; the 4.2 table rates G1 Critical (:181) but G2 (:182), G5 (:185) and G7 (:187) Important or conditional. Finding 2. |
| 5 | Implementation path is actionable (data sources, classifier order, outputs named well enough to build from) | PASS | synth-02:19-33 names every data source with its verb; :35-63 gives the classifier diagram and table in Section C order (contract, stalled-proved, fenced, waiting on a person (a)/(b), working, finished, could not determine). |
| 6 | Gaps are honest; WC-10 respected (unknown is "could not determine", never guessed) | PASS (with notes) | Every class with missing evidence falls to "could not determine" (synth-02 classifier row 7; synth-01 precedence rule 7). Stalled needs positive stop proof and no `consumer_fenced` evidence. The Approval mapping stays [UNVERIFIED] (GQ-34). Note on synth-01:244 tally under Finding 8. |
| 7 | External research is relevant and kept as context, never presented as this repo's architecture | FAIL | Tagging is correct: every external item is [EXTERNAL], and synth-03:3 states that the codebase wins. But synth-03:183 says no external source contradicts WC-10, while its own 5.4 (Grafana) and 5.5 (agents fleet) say they do. Finding 4. |
| 8 | Scale claims are substantiated (counts, windows, ages) | FAIL | The 6 h window and age rules contradict each other across synth-02:90/:152 and synth-03 R4 (:216) / R7 (:219). Finding 3. The open/resolved counts disagree between synth-01:201 and synth-02:7/:230. Finding 1. |
| 9 | Risk assessment is complete | PASS | synth-02 risks cover inbox read-marking (the reason inbox stays forbidden), `--agent-wait` side effects (GQ-51), stale contracts, and the unmerged #409 dependency. |
| 10 | Evidence trail is complete: claims trace to research files, research to code | PASS (with notes) | Spot traces: allowlist to `scope-03:99` and `qa-nb4-fix-log.md` edits 1-2; precedence to `research-notes.md:188-204`; A4 to `SKILL.md:4`, `:25-27`; Camunda R4 to `web-01:173`, `:205`; Grafana D5 to `web-02:30`, `:50`. Each traced. |
| 11 | No circular reasoning | PASS | The synthesis files cite research files and code, not each other, for their factual claims. Cross-references between synthesis files are used only to point. |
| 12 | Conclusions are proportionate; contradictions between research files are resolved or stated | FAIL | web-01:186 ("No external source contradicts WC-10's core claim") and web-02:30/:50 (Grafana contradicts WC-10) disagree. synth-03 states both without resolving them (Finding 4). synth-01 restates a pre-fix count that later research superseded (Finding 1). |

## NB-4 Recheck (coordinator-ordered)

**Question:** Do the synthesis files carry the corrected allowlist (`orchestration task-list`, `run-list`, `run-current` and `gate-list` allowed; `inbox` still forbidden), and does any synthesis text still use the old allowlist?

**Method:** Grep over `synthesis/` (all six files) for `allowlist|inbox|task-list|run-list|run-current|gate-list`. I read every hit in context and compared it with `qa/qa-nb4-fix-log.md` edits 1-2 and the corrected `scope-03:99`.

**Result: PASS.**

- synth-01:185-201 (allowlist table): the four verbs are allowed (`task-list` with `--ready` and `--run`); `inbox` is forbidden with the read-marking [UNVERIFIED] reason; `worktree ps --agent-wait` and plain `check` are forbidden.
- synth-02:19-33 (data sources) lists the four verbs as sources; SC-2 (:112) keeps `inbox` on the forbidden list.
- synth-04, synth-05, synth-06: every hit names the four verbs as allowed reads and keeps `inbox` forbidden.
- synth-03 has no allowlist text (external findings only).
- No synthesis text uses the old (pre-NB-4) allowlist, and none treats `inbox` as allowed.
- Residual, not blocking: the bare verb forms (`worker-list` and the others, without the `orca-ide orchestration` prefix) carried over from `scope-03:99` (`qa-nb4-fix-log.md:41`). Minor; Finding 10.
- Related stale text: synth-01:201 still carries the pre-fix 76/24 count. This is Finding 1, and it is a count, not allowlist text.

## Summary

- Checks passed: 8 / 12 (two of them with notes)
- Checks failed: 4 (items 4, 7, 8, 12)
- Critical issues: 0
- Important (blocking) issues: 4
- Minor issues (notes): 6
- Issues fixed in-place: 0 (fix authorization false)
- NB-4 recheck: PASS

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | IMPORTANT | `synth-01-problem-current-state.md:201` | Says the counts at `gaps-and-questions.md:125` ("Open: 76. Resolved: 24") predate the fix and are off by one. The current `:125` reads "Open: 75. Resolved: 25" and "Open blocking QA finding: none; GQ-03 (NB-4) was fixed". synth-02:7 and :230 report 75/25 correctly, so the two synthesis files disagree. A reader of synth-01 would think the ledger is still stale and that NB-4 is still open. | Rewrite synth-01:201 to state the current summary: 100 rows, 75 open, 25 resolved, no open blocking QA finding (GQ-03 resolved by the NB-4 fix pass). |
| 2 | IMPORTANT | `synth-02-target-gaps.md:172` (R-2) vs the 4.2 gap table `:181`, `:182`, `:185`, `:187` | R-2 says shipping WC-14 with G1, G2, G5 or G7 unwired is Critical. The table rates G1 Critical but G2 "Important (N-32); Critical under R-2 if WC-14 ships without it", G5 likewise, and G7 Important with no R-2 condition. The section's own rule and its ratings disagree; G7 contradicts R-2 outright. | Pick one: (a) rate G2, G5 and G7 Critical, as R-2 requires (G7 included); or (b) narrow R-2 to the gaps that really block WC-14 and give the reason G7 is excluded. Then make every 4.2 row match. |
| 3 | IMPORTANT | `synth-03-external-findings.md:216` (R4) and `synth-02-target-gaps.md:152` vs `synth-03:219` (R7) and `synth-02:90` | R4 and synth-02:152 say to exclude person-wait time from every printed age and from the 6 h window (from Camunda, `web-01:173`, `:205`). R7 and synth-02:90 sort waiting items oldest first, which needs the wait age printed and used. The research also says the window bounds activity only and that waiting items are listed whatever their age (`gaps-and-questions.md:84`, GQ-61, N-41). Taken literally, R4 hides the age by which R7 sorts, and an implementer cannot satisfy both. | Restrict R4 to activity and working-duration ages: person-wait time is excluded from the working duration and from the 6 h activity window. Waiting-on-a-person items print their wait age and sort oldest first. Make the same change at synth-02:152. |
| 4 | IMPORTANT | `synth-03-external-findings.md:183` vs `synth-03` 5.4 (Grafana, D5) and 5.5 (agents fleet, D6), and `synth-02:157` | :183 says "no external source contradicts WC-10's core claim" (copied from `web-01:186`). The same file's 5.4 says Grafana's no-data mapping "partly contradicts" WC-10, 5.5 says the agents-fleet automatic abort contradicts WC-10, and synth-02:157 says Grafana "Contradicts WC-10; rejected". `web-02:30`, `:50` and `:63` record the Grafana conflict. The synthesis passes on a contradiction between web-01 and web-02 instead of resolving it, and the summary sentence overstates how strongly the external sources agree. | Replace :183 with: "No authoritative status-layer source contradicts WC-10 (F2.2, F3.3, F4.1). Grafana's configurable no-data mapping (5.4, D5) and the agents-fleet automatic abort (5.5, D6) do contradict it; both are rejected because the codebase rule governs." |
| 5 | MINOR | `synth-01:5`, `synth-03:7` | The research-question context lists six classes without fenced, while synth-01:15 and the Section C precedence (`research-notes.md:188-204`) have seven. synth-02:65 explains the six-to-seven change; synth-01:5 and synth-03:7 do not. | Add fenced to both lists, or add a one-line pointer to the synth-02:65 explanation. |
| 6 | MINOR | `synth-01:90-97` (precedence rule 4) | Rule 4(b) omits "Ruling halt" from the frozen or policy-blocked examples given in `research-notes.md:197` and the synth-02 classifier table. | Add "Ruling halt" to rule 4(b). |
| 7 | MINOR | `synth-01` forbidden table (:185-201) vs `synth-02:112` (SC-2) | SC-2 forbids `--format`; synth-01's forbidden list does not mention it. The lists do not conflict (the catch-all covers it), but they are not the same. | Add `--format` to synth-01's forbidden list, or note that SC-2 is the complete list. |
| 8 | MINOR | `synth-01:244` | "Tally from scope-04: 3 CONTRADICTED, 0 UNVERIFIED" sits next to the Approval mapping, which is marked [UNVERIFIED] (GQ-34). The tally may count only the verified claims, but it reads as if no claim were unverified. | Say what the tally covers, or count the Approval mapping as 1 UNVERIFIED. |
| 9 | MINOR | `synth-03:113` | Calls the N-41 note in GQ-61 an "owner note". `gaps-and-questions.md:84` records GQ-61 as "open (owner decision)", so the owner has not decided yet. | Say "the N-41 note at GQ-61 (open, owner decision)". |
| 10 | MINOR | synth-01 allowlist table, synth-02:19-33 | Bare verb forms (`worker-list`, `worker-show`, `worker-read`) without the `orca-ide orchestration` prefix that C13 requires (`research-notes.md:331`). This residual comes from `scope-03:99` (`qa-nb4-fix-log.md:41`). | Use the `orca-ide orchestration <verb>` form throughout. |

Withdrawn during verification: a draft note that synth-02:144 and :243 cite `SKILL.md:25-27` for the `~/workspace` path in error. The read of `SKILL.md:25` shows "`--all` — sweep every project under `~/workspace/`", so that citation is valid. `:4` is also valid, for the hard-coded allowed-tools path.

## Actions Taken

None. Fix authorization is false. No synthesis or research file was edited; the only file written is this report.

## Confidence Gate

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Each item counts as verified because it cites the file and line it was checked against. The four FAIL items are verified failures, not unchecked ones.
- **Tool engagement:** Read: about 14 | Grep: about 10 | Glob: 0 | Bash: 0. The counts are approximate because the session was compacted partway through. Every call targeted a specific claim: the three synthesis files read in full, research-notes Sections B and C, the NB-4 fix log, the SKILL.md lines, and greps over synthesis/, gaps-and-questions.md, web-01/web-02 and WORKER-CONTRACT.md. The call total is above the 12 checklist items.
- Web research: none. The external findings were checked against the saved research files (`web-01`, `web-02`), not the live web, so Tavily was not used and no fallback happened.

## Recommendations

- Fix findings 1 to 4 in the synthesis files (a separate fix pass; this gate has no fix authorization). Then re-run this partition's review as fix cycle 1.
- Findings 5 to 10 are notes. They do not block, and later rounds do not recheck them.
- Merge with the partition 2 report (synth-04 to 06) before the gate verdict is final.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was in the spawn prompt, so I relied on no inherited PASS. I did not re-check structural matters (section numbering, file existence) beyond what the semantic checks needed.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Ledger counts: I grepped `gaps-and-questions.md:125` and found 75/25 with no open blocking finding, against synth-01:201's claim of 76/24 (Finding 1).
- R-2 against the 4.2 ratings: I read synth-02:172 and :181-187 together and found G7 rated Important despite R-2 (Finding 2).
- Age and window rules: I traced R4 to `web-01:173` and `:205`, and the window rule to `gaps-and-questions.md:84` (GQ-61). R4 conflicts with R7 and synth-02:90 (Finding 3).
- WC-10 agreement claim: I grepped web-01 and web-02 and found `web-01:186` ("no external source contradicts") against `web-02:30`, `:50`, `:63` (Grafana contradicts) (Finding 4).
- A4 citations: I read `SKILL.md:1-56`, which confirms `:4` (the hard-coded `~/workspace/IronClaude` allowed-tools path) and `:25-26` (`--all` over `~/workspace/`, 72 h default). This withdrew a draft finding.
- NB-4 recheck: I grepped all six synthesis files for allowlist verbs and compared them with `qa-nb4-fix-log.md` edits 1-2.

Answers to the mandatory questions:
1. Claims independently verified against sources: about 25 (allowlist entries, ledger counts, gap ratings, precedence rules, the A4 citations, the external contradiction statements, the GQ-61 status).
2. Files read: the three synthesis files; `research/research-notes.md:150-229`; `qa/qa-nb4-fix-log.md`; `src/superclaude/skills/sc-crash-recovery/SKILL.md:1-56`; greps over `gaps-and-questions.md`, `research/web-01-*.md`, `research/web-02-*.md`, `src/superclaude/core/WORKER-CONTRACT.md` and `synthesis/`.
3. Not applicable; 10 issues were found.
4. No web research was performed.

## QA Complete

## Verdict: FAIL

