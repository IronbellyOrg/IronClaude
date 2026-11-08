# QA Report - Task Integrity, Lens b2-self-containment

**Topic:** Research task file for GitHub issue watcher (issue #331)
**Date:** 2026-11-07
**Phase:** task-integrity (lens: b2-self-containment)
**Fix cycle:** N/A (fix_authorization: false; task file not modified)
**Task file:** .dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/TASK-RESEARCH-issue-watcher-20261107-064950.md

(Findings appended incrementally below.)

**Method:** read all 453 lines of the task file (Phases 1-7 and the Task Log), research/research-notes.md including the 2026-11-07T07:03Z addendum, and spot-checked cited paths with Glob and Grep. Line numbers below are task-file line numbers as read in this session. The task file was built at 06:50, before the 07:03Z addendum, which explains but does not excuse the addendum gaps.

## Overall Verdict: FAIL

## Items Reviewed

### B2 checklist (seven checks)

| Item ID | Check | Verdict |
|---|---|---|
| B2-1 | Every checklist item has all 5 B2 components (context, action, output, verification, completion gate) | PASS with notes (all items end with a completion gate; items 164, 350, 354 have thin context; see M-3) |
| B2-2 | No item references context from a prior item without restating it | FAIL (I-4 cycle-2 back-references at lines 208, 258, 300, 316, 332; I-5 "named above" inside embedded prompts at lines 320, 322) |
| B2-3 | Agent-spawning items have fully embedded prompts | FAIL (I-5: lines 320 and 322 embed a prompt whose input list is a dangling reference; I-4: cycle-2 spawns have no prompt of their own; M-4: nested agents spawned by fix agents have no embedded prompt) |
| B2-4 | File paths are specific | PASS (spot-checked with Glob: every cited repo path, template path and .dev path exists; agent-chosen example CLI package at line 176 is explicitly delegated and justified) |
| B2-5 | Verification criteria measurable | PASS with notes (most are countable: Status line, section headings, wc -w; M-2 lists unmeasurable "no content fabricated" clauses and the unperformable check 18 in line 266) |
| B2-6 | No batch items; one item per file/component | PASS with notes (each research, synthesis, lens, fidelity and anti-omission agent has its own item; aggregation items 182, 222, 290, 346 are inventories by design; M-6) |
| B2-7 | No items based on CODE-CONTRADICTED or UNVERIFIED findings | PASS with note (ci.py "gh subprocess wrapper", "no schedule", "projects_v2_item is org-only" are all routed to verification at lines 176, 190, 216; but synth-02 line 230 imports the unverified "no inbound endpoint if avoidable" as a Target State constraint, see I-2) |
| ADD-1 | Research addendum (2026-11-07T07:03Z): options A/B/C stay open and are scored; Coder#477 is a sibling dependency; items cause agents to read research-notes.md | FAIL (I-1, I-2, I-3) |

### Phases

| Item ID | Check | Verdict |
|---|---|---|
| Phase 1 (lines 160-168, 2 items) | B2 self-containment | PASS with notes (M-3 thin context on 164) |
| Phase 2 (lines 170-182, 4 items) | B2 self-containment; addendum | PASS for B2 on the three codebase prompts (full prompts, specific anchors, evidence-absence comments); notes M-1 (dangling "the notes say" at line 176), M-5; addendum does not apply to codebase agents except the contract question (I-3) |
| Phase 3 (lines 184-210, 9 items) | B2 self-containment | FAIL (I-4 at line 208: fix cycle 2 by back-reference; prompts hardcode cycle-1 file names) |
| Phase 4 (lines 212-222, 3 items) | B2; addendum | FAIL (I-1: web-02 prompt omits sender-authentication, coder_app sharing levels, contract schema, Coder#477; no item tells the web agents to read research-notes.md; M-1 dangling "the notes say" at line 216) |
| Phase 5 (lines 224-258, 12 items) | B2; addendum | FAIL (I-2 recommendation items bias to a pull design and force one option; I-3; I-4 at line 258) |
| Phase 6 (lines 260-332, 28 items) | B2 self-containment | FAIL (I-4 at lines 300, 316, 332; I-5 at lines 320, 322) |
| Phase 7 (lines 334-358, 6 items) | B2 self-containment | PASS with notes (M-2: line 342 and 358 repeat the D1-D3 framing and do not carry "pending owner decision"; covered by I-3) |
| Task Log (lines 360-451) | Template stubs referenced by items exist | PASS (Task Summary stub, Execution Log, Phase 1-7 Findings, Phase Gate Findings, Follow-Up Items and Deviations headings all present) |

## Blocking Findings (CRITICAL / IMPORTANT)

No CRITICAL findings. Five IMPORTANT findings.

### I-1 IMPORTANT: Addendum research requirements are not carried into any web or synthesis item (ADD-1, B2-3)

- **Evidence:** Grep of the task file for `477|addendum|ADDENDUM|OIDC|mTLS|HMAC|coder_app|app proxy|sharing level|pending owner|integer` returned no matches. Grep for `research-notes` shows it is passed for reading only to the Phase 3 gate agents (lines 188, 190, 192; line 198 only forbids editing it, line 168 and line 264 only confirm it exists) and listed in References (lines 31, 99, 109); the web items (lines 216, 218) and the four synthesis items (lines 228, 230, 232, 234) never name it.
- **Addendum point 4 requires** research on, for options B and C: how a push listener authenticates the sender (mTLS, signed requests/HMAC, GitHub OIDC tokens from Actions, Coder session tokens), how Coder exposes workspace apps and ports safely (authenticated app proxy, `coder_app` sharing levels, agent API), and a minimal watcher-to-listener contract (request schema, idempotency key, response codes). The web-02 prompt (line 218) covers reachability, `coder ssh`/port-forward, API tokens, autostop, `coder_script`, external auth, headless Claude, dispatchers, injection and at-most-once, but no sender authentication, no `coder_app` sharing level or app proxy, no GitHub OIDC from Actions, and no contract schema. The web-01 prompt (line 216) covers only "signature header" for webhooks (question 8).
- **Addendum point 2 requires** Coder#477 to be treated as a sibling dependency with the boundary "listener, registration and transport live in the Coder repo, not IronClaude". No prompt mentions IronbellyOrg/Coder#477 or that boundary, so the web and synthesis agents cannot honor it.
- **Required fix:** (a) Add `research/research-notes.md` (path given) to the read list and prompt text of both web items and all four synthesis items, naming the "ADDENDUM 2026-11-07T07:03Z" section as binding. (b) Add to the web-02 prompt questions on: sender authentication for a push listener (mTLS, HMAC-signed requests, GitHub Actions OIDC token claims, Coder session/API tokens), `coder_app` `share` levels and the authenticated app proxy, and a minimal request/response contract with idempotency key and response codes. (c) Embed the Coder#477 summary and the repo boundary in the web-02 and synth-02/03/04 prompts.

### I-2 IMPORTANT: Recommendation and plan items would steer to a pull design and force a single option (ADD-1)

- **Evidence, constraint bias:** the synth-02 prompt (line 230) states the Target State constraints as "no inbound endpoint if avoidable, no live deployment from this repo, claim assigns to the gh login that runs it". The "no inbound endpoint" constraint comes from research-notes SOLUTION_RESEARCH (a criterion "to be assessed"), not from the issue; the issue and Coder#477 describe a push design (addendum point 1). Stated as a Target State constraint it pre-penalizes B and C before they are scored. Option D in the synth-03 prompt (line 232) is described "so no workspace address is needed", and the comparison criteria include "Inbound exposure" and "Fit with the never-as-worker and claim-stops-after-next-steps facts", but no criterion is derived from the issue's stated requirements (tagged, human-approved, in a Project, in Backlog, routed to the right developer's workspace, secure account binding, audit).
- **Evidence, no scoring against issue requirements:** line 232 asks for assessment tables and a comparison table but never says to score A, B and C against the issue's stated requirements, which is what the addendum point 1 requires.
- **Evidence, forced single pick without the required label:** line 232 verification says "the recommendation names exactly one option and states what stays open for the owner"; nowhere is the recommendation required to be marked "pending owner decision". Line 234 (synth-04) says "Phase 1 holds the steps every option needs, later phases are specific to the recommended option", so the whole Section 8 plan is written for the single recommended option. Line 342 (condensed copy) copies the Section 7 recommendation without a pending marker.
- **Net effect:** given the biased constraint and the pull-leaning option D, the likely output is architecture A or D recommended and planned, which the addendum forbids ("Do NOT finalize or favor architecture A").
- **Required fix:** in lines 230, 232, 234, 266, 338 and 342: (a) drop "no inbound endpoint if avoidable" from the Target State constraints and treat it as one scored criterion; (b) require synth-03 to score each of A, B, C (and hybrids) against an explicit list of the issue's stated requirements taken from `.dev/issues/331/issue-summary.md` and Coder#477, and to state the best-scoring option as "pending owner decision"; (c) require synth-04 to give Phase 1 steps common to all options plus a short per-option branch (or per-option plan skeleton) so no option is silently dropped; (d) add the "pending owner decision" label to the verification text and to the condensed copy and presentation items.

### I-3 IMPORTANT: Accepted scope and boundary items from the addendum are not encoded, and the gates never check the addendum (ADD-1)

- **Evidence:** the addendum (point 3) records that the owner's coordinator accepted claim-only scope and that only a validated integer issue number may reach a session prompt, never issue title or body text. The task file still lists "claim-only versus full pipeline" as an open owner decision D2 (line 130; items 232, 266 check 17, 312-314, 338, 342, 358) and contains no instruction about the integer-only prompt. Neither the codebase prompt on session launch (line 174, question 6) nor the governance prompt (line 178, question 2) asks the agent to evaluate the integer-only prompt rule, and no synthesis prompt carries it into the contract or the plan.
- **Evidence, gates do not verify the addendum:** the Gate 3 lenses (lines 270-286), the fidelity gate (304-306) and the anti-omission gate (320-322) have no check that A/B/C are all scored, that the recommendation is marked pending, that Coder#477 and the repo boundary appear, or that the sender-authentication topics were researched. The only addendum-adjacent check is line 266 check 17 (D1-D3 kept open), which keeps D2 open even though the addendum says it is accepted.
- **Required fix:** (a) update Key Constraints (line 130) and D2 wording to "claim-only accepted by the owner's coordinator, confirm with owner" and add the integer-only prompt rule as a constraint that web-02, governance research and synth-03/04 must evaluate; (b) add an addendum-conformance check (A/B/C scored against issue requirements; "pending owner decision" label present; Coder#477 sibling dependency and boundary stated; sender-authentication and contract topics present) to the validation checklist at line 266 and to the actionability or crossref lens at lines 278 and 282.

### I-4 IMPORTANT: Fix cycle 2 is a back-reference, and the embedded prompts contradict the cycle-2 file naming (B2-2, B2-3)

- **Evidence:** lines 208, 258, 300 and 316 say to run fix cycle 2 by "repeating Steps 3.2 ... and 3.3 ... spawning the same agents with the same prompts", and lines 316 and 332 say "repeating the consolidate, fix and verify items of this step" (items not named). The cycle-2 spawns therefore have no prompt of their own and depend on earlier items, which is the "see above" pattern B2 forbids. The Deviations note at line 437 records this as a deliberate encoding but does not make the items self-contained.
- **Contradiction:** the embedded prompts hardcode cycle-1 paths (for example line 198 reads `qa-consolidated-findings-phase3.md` and writes `qa-fix-log-phase3.md`; lines 202 and 204 take those as inputs), while the decision item demands the `-cycle2` suffix on every new report. "Same prompts" would make the cycle-2 fix agent re-apply the cycle-1 list and the cycle-2 verifiers read the cycle-1 logs. In Step 6.5/6.6 the consolidation glob `qa-lens-*.md` expects seven reports (line 290) while line 300 allows re-running only some lens agents.
- **Required fix:** either add explicit cycle-2 items (consolidate, fix, two verifiers, decision) for each of the five gates with embedded prompts and the `-cycle2` paths, or embed in each gate one parameterized prompt using a named `{SUFFIX}` placeholder with an instruction to substitute `""` in cycle 1 and `-cycle2` in cycle 2 in every path, and state which items re-run.

### I-5 IMPORTANT: Embedded anti-omission prompts contain a dangling input reference (B2-2, B2-3)

- **Evidence:** the prompts at line 320 and line 322 (the text the executor must pass "in full") both contain `Assigned input files: the five files named above.` The prompt text itself names no files; the files are listed only in the item wrapper text before "Give the agent this prompt in full". The spawned `rf-analyst` receives no input list and cannot know which research and synthesis files it owns, so the two agents may enumerate overlapping or wrong sets, and the "count adds up" verification at those items cannot be satisfied.
- **Required fix:** replace the sentence in both prompts with the explicit paths (line 320: files 01, 02, 03, gaps-and-questions.md, synth-01; line 322: web-01, web-02, synth-02, synth-03, synth-04), as lines 304 and 306 already do with their `[INSERT ...]` markers.

## Minor Findings (notes, non-blocking)

| ID | Location | Note |
|---|---|---|
| M-1 | Lines 176 (three times), 216 (twice) | Embedded prompts say "the notes say ..." / "the research notes say ..." without giving the agent the notes path. The claim is restated in the same sentence with "verify", so the agent can still act; add the path or drop the phrase. |
| M-2 | Lines 174, 176, 178, 216, 218, 228, 230, 232, 234 and line 266 check 18 | Verification clauses "no content fabricated beyond the source files" cannot be measured by the executor in the same item. Line 266 check 18 asks the executor to prove which protocol blocks each prompt contained "by reading the qa/ and research/ files' headers", but output headers do not show prompt content; compare the prompts in this task file instead. |
| M-3 | Lines 164, 350, 354 | Items have no purpose/"because" clause (thin context). Completion gates and outputs are present. |
| M-4 | Line 198 (and 248, 292, 310, 326 by pattern) | The fix agent is told to "spawn one targeted research agent per gap" (rf-task-researcher) but that nested prompt is not embedded; the protocols are only summarized in parentheses. Embed the research-agent prompt skeleton. |
| M-5 | Line 228 | The executor is told to read the `GOAL` and `WHY` lines of BUILD-REQUEST.md (headings exist at BUILD-REQUEST.md lines 12 and 14) but the embedded prompt neither includes them nor names the file, so the read has no consumer. |
| M-6 | Line 346 | Single item does about 30 file-existence checks, three `stat` calls, a Task Log read and a file write. It is an aggregation check by design, but it will be hard to mark partially. Consider splitting existence checks from the freshness (stat) check. |
| M-7 | Line 151 vs line 6 | Blocked status is "⚪ Blocked" in the Frontmatter Update Protocol but "🔴 Blocked" in the frontmatter status options; "⚪" is Cancelled. |
| M-8 | Lines 188-210, 246-258, 290-300 and similar | Every spawn item ends "If the agent fails ... log the blocker ... then mark this item complete". For the gate-decision items (208, 258, 300, 316, 332) this lets the executor complete the item without a verdict while the same item says "Do NOT proceed ... until the verdict is PASS". Change the missing-report branch of decision items to HALT. |
| M-9 | Lines 270-286 | Prompts name the "Report Structure template" and the lens checklists without giving the path of the installed tech-research SKILL.md (listed only in References, line 109). The relevant section list is embedded, so this is low risk. |

## Checks that held up (evidence)

- Glob confirmed existence of: all `.github/workflows/*` and `.github/ISSUE_TEMPLATE/*` files named in line 176; `src/superclaude/skills/sc-issue-protocol/{SKILL.md,refs/claim.md,refs/labels.md,scripts/origin_repo.py,scripts/clickup_claim.py}`; `.dev/issues/331/{accuracy-check.md,analysis/analyze-sc-issue-protocol.md}`; the brainstorm `enrichment/codebase-context.md`; and the template `/home/coder/.claude/templates/workflow/02_mdtm_template_complex_task.md`.
- Grep of `src/superclaude/core/WORKER-CONTRACT.md` confirmed the never-as-worker list at line 23 (includes `/sc:issue`) and WC-8 at line 39, matching the anchors in lines 174 and 178.
- Every `- [ ]` item (64 counted by phase: 2, 4, 9, 3, 12, 28, 6) ends with a completion gate sentence ("Once done, mark this item as complete"), and agent-spawning items in Phases 2 to 6 embed the full prompt, with the exceptions listed in I-4 and I-5.
- The ci.py "gh subprocess wrapper" claim from research-notes is not built on: it is flagged in the Task Log (line 436), verified in the Integration Mapper prompt (line 176) and re-verified at line 190.

## Summary

- B2 checks passed: 5 of 7 (B2-1, B2-4, B2-5, B2-6, B2-7 pass, some with notes; B2-2 and B2-3 fail), plus the addendum check ADD-1 failed. Blocking findings: 5 IMPORTANT (I-1 to I-5), 0 CRITICAL. Minor notes: 9.
- The addendum finding (I-1, I-2, I-3) is the one the coordinator asked about: as written, the recommendation items (lines 230-234) would force a single, pull-leaning recommendation, the web items would not research push-listener authentication or the Coder#477 contract, and no item makes any agent read the research-notes addendum.
- **Confidence:** Verified: 7/7 B2 checks plus addendum check | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (all 64 items and 453 lines were read).
- **Tool engagement:** Read: 13 | Grep: 8 | Glob: 7 | Bash: 0. (Read count exceeds items reviewed by chunks because task-file lines are very long; Glob and Grep targeted specific claims: path existence, never-as-worker anchor, addendum keywords, dangling-reference phrases.)

VERDICT: FAIL

QA Complete

