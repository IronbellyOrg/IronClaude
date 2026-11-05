# QA Report: Domain Accuracy and Cross-Validation Lens (Task Step 6.9)

**Report reviewed:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/RESEARCH-REPORT-review-loops.md` (1,263 lines, read in full)
**Lens:** Domain accuracy and cross-validation
**QA phase:** report-lens-domain-accuracy
**Date:** 2026-10-24
**Fix cycle:** N/A (cycle 0, report-only, `fix_authorization: false`)
**Intended output path:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-lens-domain-accuracy.md`. This reviewer is not allowed to write report files, so this text is the complete report for the parent to save.
**Governing template:** `/config/.claude/skills/tech-research/SKILL.md:1042-1151` (Lens-Specific QA Agent Prompt Template; Domain-Accuracy Checklist :1108-1112)

---

## Overall Verdict: FAIL

## Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|-------------|
| 1 | IMPORTANT | 2.3 (line 177), 6 Option E "Current rule" row (line 603), 7.5 V5 row (line 713), 7.5 layer note (line 716) | **The report's claim about the pin line in each protocol layer is no longer true.** The report says the checkout copy pins the plan at `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:42` and the installed copy (`/config/.claude/skills/...`) pins it at line 43, which presents the two layers as different. Today the two files are byte-identical: both are 86 lines with sha256 prefix `bb1a2a933f51`. In both, the pin text ("The first `T<id>: start` line is the immutability boundary") is at **line 43**, and checkout line 42 is blank. The checkout changed at `2026-10-24T03:42:30Z` (reflog: `checkout: moving from master to fix/retry-citation-line-count`). That is before the Step 6.1 assembly enumeration at `03:51:27Z`, so the current-source anchor was not re-checked when the report was assembled. The report's working premise that "installed and checkout copies later diverged in four of seven pairs" also no longer matches today's state: six of seven pairs are identical, and only `retry.md` differs, because of an uncommitted working-tree edit. | Re-anchor every checkout-layer `managed-workspace.md:42` citation to `:43`. Delete the present-tense "pin text is at line 43" layer-difference sentence at line 716, or rewrite it as a dated observation (time plus commit). Add the time and commit of each current-source read, for example `git show bbbfcc4b:<path>`, so later checkouts cannot silently break the anchors. |
| 2 | IMPORTANT | 2.3 table rows "Plan generation", "Bounded automatic task attempts", "Managed whole-package FINAL", "Pinned plan", "History and concurrency" (lines 173-178) | **Several current-source line ranges labelled "read directly from the current checkout" now point at different text.** (a) `retry.md:142-146`: checkout lines 142-146 are now the A5 ladder-end halt and the Model ladder heading. "Cost and caps" (worst case 5 reviews; each resume adds an operator review) moved to **161-165** after an uncommitted 19-line insertion at line 78 (file mtime `03:54:21Z`, after assembly). The installed copy still has it at 142-146. (b) `managed-workspace.md:44-60` is now 45-61, `:60-68` is now 61-69, and `:78-85` is now 79-86. The enforcement-map row that supports "the state digest does not cover task-owned artifact contents or omitted delivery files" is now **line 86**, outside the cited range. (c) `sc-workflow-protocol/SKILL.md:48-72` is now 50-74, because commit `c6009cd3` added two lines at line 28. The "Will Not ... modify the plan from reflect findings" line is now **74**, outside the range. The claims themselves are still semantically true. The anchors are not, and the section gives no observation time. | Re-anchor (a)-(c) to the current lines, or to a pinned commit or installed-layer path, and state the read time. Keep the "[SOURCE-VERIFIED checkout ...]" label only on anchors re-read at a stated time. |
| 3 | IMPORTANT | 2.3 (line 198), 4 "Available evidence" row (line 321), 5.1 row 1 (line 371), 6 Option C "Evidence strength" (line 550), 7.5 V3 "Must not be inferred: Who changed the rubric" (line 711), 7.7 row (line 743), 9 Q3 (line 922) | **Local history that is available is treated as unavailable.** The report says the credential rubric's updater and version history are unknown and that resolving them needs "relevant historical records". Those records exist locally and were not consulted. The earlier captured rubric hash `0b533765d43a7adc90987581892a0bca849cc19a53638b556b6aba62d425d083` exactly equals the `qa.md` blob at IronClaude commit `6dc56b1a` (`2026-10-03T00:36:23Z`). The later hash `faff03b7b94ca2b70f9b25c35dcefd52636b7df8f7bf9a110c0a956a78d2e7d5` exactly equals the blob at `00448800` (`2026-10-22T18:57:46Z`, "Merge origin/master into feature/implement-retry-ladder"). The IronClaude checkout fast-forwarded `43cb0116 -> 5d79d16c` at `2026-10-22T20:28:00Z`: `00448800` is not an ancestor of `43cb0116` but is an ancestor of `5d79d16c`. The installed `refs/` directory, including `qa.md` and `retry.md`, was written at `20:29:54.0176Z`, and installed `qa.md` has not changed since (current sha `faff03b7...`). The two credential FINAL loads at `20:26:30.085Z` (old) and `20:32:19.277Z` (new) bracket that write. So the version change is a committed framework release that was pulled and installed while the session ran. It is not an untraceable edit. Only the identity of the person or process that ran the install is still unproven. | Record this provenance chain in 2.3, Option C and 7.5, labelled as Git-object, reflog and file-metadata evidence. Narrow Q3 to "which process ran the 20:29:54Z install". Change "who changed the rubric: unknown" to "change = install of commit lineage containing `00448800`; operator identity unproven". Keep the current-file-is-not-historical-load caution, but note that here the hash identity is exact. |
| 4 | IMPORTANT | 6 Option C "Scope" ("a proven amplifier in two runs", line 548) and "Debate record" (line 551), Options Comparison "Direct contexts" for V3 (line 616), 7.4 "Shared clusters" (line 702) | **Two pieces of policy-change evidence are counted as independent when they share one cause.** The same 20:29:54Z installation also explains the monitor's mid-run protocol migration. The monitor session loaded its skill at 19:29 (`05-session-e002bed2.md:83`), before the install. It read the installed `/config/.claude/skills/sc-implement-protocol/refs/ledger.md` at `20:34:06.655Z` (raw 874) and `SKILL.md` at `20:34:18.637Z` (raw 884), both after the install. The retry ladder it newly found was introduced in commit `3ad7e207` (`2026-10-22T15:27:44Z`) and arrived through the 20:28 pull. Option C's two decisive pieces of support (the credential rubric change and the monitor migration) are therefore one deployment event observed in two sessions. The report already treats the Orca and credential clusters as non-independent, but it does not record this shared cause, so V3's reach looks broader than the evidence supports. The debate never weighed this dependency. | Add the shared-deployment dependency to 7.4 "Shared clusters", Option C Scope/Evidence strength and the comparison row. Label it as timing-based for the monitor (the installed `ledger.md` has since been rewritten, at `2026-10-23T17:55:50Z`, so its historical bytes cannot be hash-checked). Do not re-rank inside the report. Per Step 6.18, a correction that affects ranked-cause support must invalidate the affected debate and synthesis checks so they are actually rerun. |

### Summary
- Total findings: 4
- Critical: 0
- Important: 4
- Minor: 0
- Verdict: **FAIL** (any issue of any severity fails the gate)

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| a | Codebase architecture claims match the actual code structure | FAIL | Findings 1-2. The claims checked against current files are semantically correct: qa.md:9-11, 27-52, 56-68, 82, 86-90; ledger.md:142, 148-158; managed-workspace.md:43, 49-61, 65-69, 79-86; quality-gates.md:24-41; workflow SKILL.md:50-74; installed retry.md:142-146 and :392 (`head-moved` = "HEAD moved since Q0, or no Q0 record", which matches the report's checkpoint-guard claim). The anchors and the layer-identity claim are stale. |
| b | Capabilities match what the code implements; no aspirational feature described as current | PASS | The report consistently labels current rules as instruction text, not enforced behavior. This agrees with managed-workspace.md:83-86, which separates protocol, executable helper (`scripts/archive_workspace.py`, which exists) and unsupported concurrency. `sc-workflow-protocol/` has no scripts directory, which supports the claim that its generation gate is agent-performed rather than an executable proof (Option A, line 498). |
| c | Technology version claims match dependency files | PASS (adapted) | A regex scan of the report for version tokens found none. The report makes no package, runtime or tool version claims. Adapted check: the protocol-version (rubric-version) claims were audited under check d. |
| d | Integration and event-chain descriptions match verified behavior | FAIL | Findings 3-4: the rule-change event chain (pull, then install, then new rubric load and migration) is reported as unknown or as two independent events. Verified as correct: `/usr/bin/man` is a minimization-notice shell script; the rendering artifacts `t6-fix-evidence.log:1-3`, `progress.md:14-18` and plan `:81-87` say what Section 8 claims; `t10-markdownlint.log` is 1,006 bytes at the stated candidate path; trees `f60d2c3`, `3c5fdfa` and `00d8f4a` exist as Coder Git trees; the oracle `artifacts/` path, `t12-held-back-before-authorization.json` and `t12-review-2.md:20-28` (frozen `default_path=false` retained defect) exist and match. |
| e | Code, documentation and historical versions kept separate; current rules not presented as observed historical execution | PASS with one exception | The report consistently separates current rules from historical loads (2.3 caveat, 7.5 columns, Q20). The exception is Finding 3: it declined to use historical Git records that are neither current text nor inference. |
| f | Invalid review findings judged against original acceptance and historical state | PASS | Spot checks: the Task 6 AC text ("renders both without a warning when `man` is available", plan :87) matches the report's "weak availability guard" and the accepted `cannot-verify` endpoint (progress.md:14-17). The oracle review-2 finding cites the frozen fixture and the original requirement, which matches Option E. |
| g | Unavailable evidence stays unknown; available evidence is not called unknown | FAIL | Finding 3. |

## Confidence Gate
- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 18 | Grep: 0 | Glob: 0 | Bash: 12. Searches ran through Bash grep and git; they are counted under Bash.
- UNCHECKED items: none. UNVERIFIABLE items: none. The bytes of the monitor's historical `ledger.md` cannot be hash-checked because the installed copy was rewritten at `2026-10-23T17:55:50Z`, so Finding 4 is stated as timing evidence, not hash evidence.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- No Inherited Structural Verdict was supplied. Sibling Phase 6 lens reports were not relied on. Section 10's inventory counts, the TOC and the template structure were not re-verified; other lenses own them.

**(b) Independent semantic checks (at least one required, INV-019):**
- Layer identity: sha256 and line count of all seven checkout/installed pairs (Bash), plus Reads of checkout managed-workspace.md:30-86, workflow SKILL.md:40-74, qa.md:1-90, ledger.md:134-161, quality-gates.md:1-41, installed retry.md:138-179 and checkout retry.md:138-169.
- Change provenance: `git diff` of retry.md (19-line insertion at :78); `git reflog` (03:42:30Z branch switch; 20:28:00Z pull); `git show <commit>:qa.md | sha256sum` for `6dc56b1a` and `00448800` (full-hash matches to the scope-rules.md:70-71 captured hashes); `merge-base --is-ancestor` checks; installed `refs/` mtimes.
- Historical loads: bounded reads of record 18 in both credential FINAL subagent JSONLs (timestamps 20:26:30.085Z and 20:32:19.277Z, both loading `sc-implement-protocol/refs/qa.md`), and records 874 and 884 of the monitor JSONL (installed ledger.md and SKILL.md read at 20:34:06Z and 20:34:18Z).
- Artifact claims: rendering artifacts, the notice script, the t10 log, Coder trees, and the oracle artifacts and review-2 lines (Bash).
- Why the four findings are real: each is a direct mismatch between a report sentence and a file, hash or reflog entry read in this session. No finding is inferred from another report.

**Web research:** none performed. Tavily was not needed because every check was local.

## QA Complete

---

| Status | Result |
|---|---|
| DONE | Reviewed the full report under the domain-accuracy lens. Verdict FAIL: 4 IMPORTANT findings, 0 critical, 0 minor. |
| DONE | Edited nothing. Ran no agents, tests, Git mutations or staging. |
| NEXT | The parent saves this text verbatim to `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-lens-domain-accuracy.md` with attribution. This reviewer could not write the file. |
| NEXT | Step 6.17 consolidates. Findings 3-4 affect the evidence behind the V3 ranking, so per Step 6.18 they should invalidate the affected debate and synthesis checks for an actual rerun rather than be patched only in the report. |