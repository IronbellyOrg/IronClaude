# QA Report - Task Integrity (Lens: phase-structure)

**Topic:** Issue #331 GitHub issue watcher research task file
**Date:** 2026-11-07
**Phase:** task-integrity (lens: phase-structure, fix_authorization: false)
**Fix cycle:** N/A (first review)
**Task file:** .dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/TASK-RESEARCH-issue-watcher-20261107-064950.md

(Report is built incrementally; sections below are appended as checks complete.)

**Scope facts established first (tool-verified):** the task file is 453 lines, 228,472 bytes, 30,031 words; it holds 64 `- [ ]` items (Phase 1: 2, Phase 2: 4, Phase 3: 9, Phase 4: 3, Phase 5: 12, Phase 6: 28, Phase 7: 6) and 0 `- [x]` items. No phase header claims an item count. Template read: `/home/coder/.claude/templates/workflow/02_mdtm_template_complex_task.md` (Part 2 structure, lines 1161-1519). Authority for gate counts: BUILD-REQUEST.md lines 30-38.

## Overall Verdict: FAIL (1 IMPORTANT blocking finding; 12 MINOR notes)

---

## Items Reviewed

PASS / FAIL table over the 16 checks of the lens prompt. "FAIL-MINOR" means the literal rule is not met but the only findings are minor notes that never fail the review (review severity rule). Overall FAIL comes only from the blocking finding on check 8.

| Item ID | Check | Verdict |
|---|---|---|
| C1 | YAML frontmatter complete and well-formed | PASS (notes N-1, N-2) |
| C2 | All mandatory template sections present | PASS (note N-3) |
| C3 | Phase dependencies logical, no circular or missing | PASS (note N-4) |
| C4 | Phase ordering: research, then build, then test | PASS (notes N-5, N-6) |
| C5 | Task completion items inside the final phase (anti-orphaning) | PASS |
| C6 | Task Log section present at the bottom | PASS |
| C7 | Estimated item count reasonable for the scope | PASS (note N-7) |
| C8 | Open Questions and remaining gaps documented | FAIL (blocking, finding B-1) |
| C9 | QA gates follow M3/M4 at STANDARD counts (3 / 3 / 7 / 2 / 2) | PASS (notes N-4, N-6) |
| C10 | TB-Add-1 placeholder scan, 5-field schema | FAIL-MINOR (note N-8) |
| C11 | TB-Add-3 clarification adjacency | PASS (vacuous: no Open Questions section; see B-1) |
| C12 | TB-Add-4 circular dependency (DAG) | PASS (note N-4) |
| C13 | TB-Add-5 granularity / XL splitting | FAIL-MINOR (note N-9) |
| C14 | TB-Add-6 `Verify:` / `- [x]` format consistency | PASS (note N-10) |
| C15 | TB-Add-7 Source areas reappear in items; block has no file:line | PASS |
| C16 | TB-Add-8 per-item Context evidence binding | FAIL-MINOR (note N-11) |

## Evidence per check

**C1 Frontmatter.** Parsed with PyYAML (`uv run python -I -c ...`): 35 keys; every one of the template's 34 keys is present (missing: none); one extra key `reflect_post_mode: skill`, which task-builder SKILL.md line 2168 says is ALWAYS emitted, so it is legitimate. `id` equals the file name. `status` "🟡 To Do", `type` "🔬 Research/Spike" and `priority` "🔼 High" are valid options. Empty values: version, parent_task, depends_on, spec_path, reflect_post, related_prd, related_tdd, template_schema_doc, estimation, sprint, due_date, start_date, completion_date, blocker_reason, ai_model, model_settings (all empty in the template too).

**C2 Template sections.** Task Overview, Key Objectives, Prerequisites & Dependencies (Parent Task & Dependencies, Previous Stage Outputs), Execution Context (References, Source Areas, Key Constraints, Handoff File Convention, Frontmatter Update Protocol), Detailed Task Instructions, Phases 1-7, Task Log / Notes (Task Summary, Execution Log, per-phase Findings, Phase Gate Findings, Follow-Up Items, Deviations) are all present (heading grep, task file lines 65-431). Not present as standalone headings: `## Post-Completion Actions` and `### Phase Gate: Quality Verification`; both are deliberately folded into Phases 6 and 7 (task file line 334 and Deviations line 442) and match the anti-orphaning rule. No `ORCHESTRATOR`/`BUILDER` instruction blocks remain (grep: 0 hits).

**C3/C12 Dependencies.** I mapped every `qa/`, `research/`, `synthesis/`, `phase-outputs/` file and the report to the item lines that mention it. Every consumer comes after its producer: gate reports (188-192) before consolidation (196), fix log (198) before verification (202/204), verification before decision (208), `gaps-and-questions.md` (210) before web agents (216/218) and synthesis (228-234), synth-03 (232) before synth-04 (234, stated at line 226), synthesis files before assembly (264), report before Gate 3/4/5 agents, verdict files before Phase 7 (338, 346). There is no static cycle. The only back-edge is the dynamic "repeat Steps N.2 and N.3 with suffix -cycle2" inside each decision item (208, 258, 300, 316, 332); the earlier items never reference the decision item, so the graph stays acyclic (see N-4).

**C4 Ordering.** Prep (P1), codebase research (P2), research gate (P3), web research (P4), synthesis plus gate (P5), assembly plus Gates 3-5 (P6), presentation, condensed copy, completion (P7). This is the order the BUILD-REQUEST lines 43-66 requires.

**C5 Anti-orphaning.** Task Summary (7.4, line 350) and the final frontmatter update to "🟢 Done" (7.5, line 354) are inside Phase 7, the last phase. Step 7.6 is a NON-BLOCKING suggestion placed after Done; it gates nothing.

**C6 Task Log.** Present at line 360 with every template subsection plus a populated Deviations section.

**C7 Item count.** 64 items for 5 research agents, 4 synthesis agents and 5 gates is proportionate to the BUILD-REQUEST's "individual item for every agent and validation step" rule. See N-7 for the file-size caveat.

**C9 Gate counts (verified by item lines).** Gate 1: 188 rf-analyst completeness, 190 rf-qa evidence-quality, 192 rf-qa-qualitative research-depth = 3. Gate 2: 238 rf-analyst, 240 rf-qa structure, 242 rf-qa-qualitative = 3. Gate 3: 270/272/274 rf-qa (template-conformance, internal-consistency, evidence-quality), 278/280/282 rf-qa-qualitative (actionability, domain-accuracy, crossref-chain), 286 rf-qa-qualitative finding-reproducibility = 7. Gate 4: 304/306 = 2 fidelity. Gate 5: 320/322 = 2 rf-analyst anti-omission. Verification rounds are 2 agents each (202/204, 252/254, 296/298, 312/314, 328/330). Exactly one `fix_authorization: true` agent per gate (198, 248, 292, 310, 326). All five decision items carry the three halt guards in the required order (regression, then monotonicity, then 2-cycle cap) with the byte-exact messages (grep: `Regression detected` and `[HALT-MONOTONICITY]` on lines 208, 258, 300, 316, 332).

**C11 Clarification adjacency.** The task file has no Open Questions section and no item cites an `OQ-` index (grep: 0). The check is vacuous only because the section is missing; see B-1.

**C14 Format consistency.** `Verify:` appears 0 times and `- [x]` 0 times. Every item uses the Template 02 "ensuring ..." / "Ensuring ..." integrated-verification clause, except 164, 354 and 358, which are status-update and non-blocking items with explicit completion gates. So the format is uniform, but it is not the `Verify:` form the check names (N-10).

**C15 Source areas.** `### Source Areas` (lines 115-123) lists 8 groups. All reappear in item bodies: commands and sc-issue-protocol, core, ccsession-tag (item 174); hooks/scripts and docs/designs (item 178); `.github/workflows`, `.github/ISSUE_TEMPLATE` (item 176); pr_submit and cli, tests and Makefile (item 176); External (items 216/218). The block has no `path.py:NN` reference (regex over lines 105-155: 0 hits). The optional consumer-side spot check `grep -cE "src/|/.*:[0-9]+"` returns 5, all area-level `src/...` directory paths that the Source Areas section is required to list.

**C16 Evidence binding.** I verified every line anchor in the three Phase 2 prompts against the repository and all are correct: issue.md 8/15/24/45-51/68/71/79; SKILL.md 70-72 and 82-85; origin_repo.py 28-49 and 105-137; WORKER-CONTRACT.md 23 and 39; ccsession-tag README 21 and 228-234; core/CLAUDE.md 45-53; test.yml 3-8; boundary-guard.yml 25-26; contract3 lint 22-23; ci.py imports 10-15 and `def classify_checks(` at 25; main.py 521 and 561; Makefile 13/48/53/109/166; launch-hook design 6-10/23/41/52; launch-job-identity.sh 1-8. Each of items 174, 176 and 178 carries an `<!-- evidence-absence: ... -->` comment for the files without anchors. All cited source paths exist; `launch-level-guard.sh` does not exist, and item 178 correctly asks the agent to check that.

## Issues Found

### Blocking

**B-1 (IMPORTANT, check C8, also affects C11 and C15). The task file does not carry the binding ADDENDUM in research-notes.md, so the open owner questions and the extra research scope are missing.**

Evidence. `research/research-notes.md` lines 99-104 hold an "ADDENDUM 2026-11-07T07:03Z: coordinator guidance and sibling issue (binding on all agents)". The file was last written 07:02:34; the task file's Execution Log (line 390) records the build at 06:50 and `BUILD-REQUEST.md` is dated 06:50. A grep of the task file for `477`, `Coder#`, `IronbellyOrg/Coder`, `ADDENDUM`, `sibling`, `pending owner decision`, `mTLS`, `HMAC`, `OIDC`, `coder_app`, `app proxy`, `integer issue number` returns 0 hits for every term. The task file's `related_docs` (line 31) still calls the notes "scope-discovery research notes that drive the agent assignments", so the executors will be driven by the pre-addendum scope. Four concrete gaps:

1. Sibling dependency and boundary (addendum point 2). `IronbellyOrg/Coder#477` (workspace listener, monitor registration, secure prompt routing) and the boundary "listener, registration and transport live in the Coder repo; this repo's deliverable is the watcher/selection/dispatch side and the contract it needs from the listener" appear nowhere: not in References (lines 107-113), Source Areas (115-123), Key Constraints (125-130), the Overview, or any agent prompt.
2. Option scoring (addendum point 1). The addendum requires all of A, B and C to be scored against the issue's stated requirements, A not to be favoured, and the Recommendation to be marked "pending owner decision". Item 232 (synth-03) uses generic criteria (Effort, Risk, Maintainability, Integration complexity, Reuse potential, Security posture, Inbound exposure, At-most-once, Fit) and asks for "the recommended option"; grep finds no "score" and no "pending" anywhere in the task file.
3. Owner-accepted scope (addendum point 3). The addendum says claim-only scope was accepted by the owner's coordinator and that only a validated integer issue number may ever reach a session prompt, never issue title or body text. The task file keeps "claim-only versus full pipeline" open as D2 (lines 130, 232, 234, 238, 338, 342) and states the integer-only rule nowhere, so the report may re-open a settled decision and may not set the constraint.
4. Required extra research (addendum point 4). For options B and C the research must cover how a push listener authenticates the sender (mTLS, signed requests or HMAC, GitHub OIDC tokens, Coder session tokens), how Coder exposes workspace apps and ports safely (authenticated app proxy, `coder_app` sharing levels, agent API), and a minimal watcher-to-listener contract (request schema, idempotency key, response codes). Item 218 (web-02) asks about Coder reachability, `coder ssh`/`exec`, REST API tokens, `coder_script`, external auth, `claude -p`, the Claude Code Action, comparable dispatchers, prompt injection and at-most-once patterns, but contains none of the sender-authentication, app-sharing or contract questions (grep over line 218: no OIDC, no sharing level, no signed request). Issue #331's second and third questions (secure workspace binding, what the Coder-side listener is) are therefore under-researched.

Why blocking. This is a missing required deliverable and a scope drift: the executors will research and the report will conclude against stale scope, and nothing in the task file records the gap (check 8 asks for remaining gaps to be documented; the builder's Deviations notes at lines 435-444 all date from 06:50 and none mentions the addendum).

Required fix (not applied; fix_authorization is false). Update the task file from the current research notes: (a) add Coder#477 and the repo boundary to References and Key Constraints, and "External: IronbellyOrg/Coder#477 (read-only)" to Source Areas; (b) in item 232 require scoring of A/B/C and the hybrid against the issue's stated requirements and a "pending owner decision" mark on the recommendation, and reconcile D2 with the accepted claim-only scope (or record in Deviations why it stays open); (c) add the integer-only prompt constraint to Key Constraints and to the synth-03/synth-04 prompts; (d) add the sender-authentication, app-sharing and listener-contract questions to item 218 (web-02), and make Gate 2 and Gate 3 prompts check them; (e) log the addendum in the Deviations section with its timestamp.

### Minor notes (recorded, never fail the review)

**N-1 (C1).** The rf-qa task-integrity checklist item 1 names the fields `created`, `template` and `tracks`. Neither template 02 (34 keys, verified above) nor the task-builder Output Structure has them, and the task file has none. This is a checklist-versus-template mismatch, not a task file defect. Related: `template_schema_doc` and `estimation` are empty although the task-builder Output Structure (SKILL.md lines 2165-2166) shows them filled; consider setting `template_schema_doc` to the template 02 path for traceability.

**N-2 (C1/C2).** Line 151 says "If Blocked: Update `status` to "⚪ Blocked"", but the status options (line 6) contain "🔴 Blocked" and "⚪ Cancelled", not "⚪ Blocked". Inherited verbatim from template line 1232; an executor following it writes an invalid status.

**N-3 (C2).** Items cite `### Phase N Findings` (28 times for Phase 6) but the headings are `### Phase N - <Name> Findings` (lines 392-419). Inherited from the template; an executor must infer the target heading.

**N-4 (C3/C9/C12).** Fix cycle 2 is a prose "repeat Steps N.2 and N.3 with suffix -cycle2" inside decision items 208, 258, 300, 316 and 332, with no checkbox items. It follows the template's PG.5 pattern and is documented at Deviations line 437, so it is acceptable, but a session rollover during cycle 2 leaves no item state showing which cycle-2 sub-step finished.

**N-5 (C4).** Web research (Phase 4) has no pre-synthesis research gate; Gate 1 covers only files 01-03. Web findings reach synthesis checked only by the Phase 4 inventory (item 222), then Gate 2 (traces synthesis to research) and Gate 4 agent 2 (spot-checks URLs). This follows the BUILD-REQUEST phase list, so it is a design note only.

**N-6 (C4/C9).** Gate 4 and Gate 5 fix agents edit the report after Gate 3 verified it. Item 346 only stats the files and logs a Follow-Up if a later gate changed the report without covering it ("do not run extra QA agents here"). Matches the BUILD-REQUEST order; the residual risk is that late edits never see the lens agents.

**N-7 (C7).** The file is 228,472 bytes (about 57,000 tokens); one Read call is capped at 25,000 tokens, so a resuming executor must page it. Phase 6 holds 28 of 64 items. Acceptable under the granularity rule, but note it for resume behaviour.

**N-8 (C10).** The literal tokens `TODO` and `TBD` appear in items 240, 264 and 270 as search targets for QA agents ("search for TODO, TBD, PLACEHOLDER"). A mechanical TB-Add-1 grep will flag them although they are not placeholders. Reword (for example "unfilled to-do markers") to keep the gate clean. Also `[INSERT THE BRIEF]` (216, 218) and `[INSERT THE LIST]`/`[INSERT THE URL LIST]` (304, 306) are deliberate prompt slots, not placeholders; every item has the full 5-field body.

**N-9 (C13).** Agent-spawn items 174, 176, 178, 216, 218 and 228-234 are 5,600-7,600 characters each; the compound items 198, 248, 292, 310 and 326 combine a conditional "no fix needed" branch with a fix-agent spawn. The skill requires embedded prompts, and each item has one agent and one output, but no critical-rule-aware justification comment exists, as TB-Add-5 asks. Add one line to Deviations.

**N-10 (C14).** No `Verify:` prefix and no `- [x]` acceptance form exists; template 02 uses the "ensuring ..." clause, used uniformly. Treat the check as satisfied by consistency.

**N-11 (C16).** Items that name code surfaces after Phase 2 carry neither a file:line nor an evidence-absence comment: 190 (re-verify ci.py and the workflow triggers), 234 (plan targets), 280 (domain-accuracy re-reads cited files), 304 and 306 (fidelity source lists). These list assignment files rather than assert behaviour, so no wrong claim results, but the literal rule is unmet. Also, the `<!-- evidence-absence: ... -->` comments in items 174, 176 and 178 sit inside the double-quoted prompt that the executor must pass to the agent "in full", so the builder bookkeeping leaks into the agent prompt; move the comment outside the quote.

**N-12 (cross-lens, C5/C6).** Orphan or inconsistent outputs: `phase-2-research-inventory.md` (item 182) and `phase-4-web-inventory.md` (item 222) are created "to give later items a dynamic list" but no later item reads them (grep: lines 182/222 only); the subdirectories `phase-outputs/discovery/`, `phase-outputs/test-results/`, `phase-outputs/reviews/` and the task-root `reviews/` are created (line 168) and never used. Item 338 (7.1) must report Gate 1 to Gate 5 verdicts but lists only the three Phase 6 verdict files as inputs, omitting `phase3-gate-verdict.md` and `phase5-gate-verdict.md`. Item 346 says it confirms "every output file named in the items above" but lists a subset (it omits the inventories, `validation-checklist-result.md`, `presentation-summary.md`, consolidated findings, fix logs and Gate 1/2 reports).

## Summary

- Checks passed: 12 of 16 clean PASS or PASS with notes; 3 FAIL-MINOR (C10, C13, C16); 1 FAIL blocking (C8).
- Blocking findings: 1 (IMPORTANT). Minor notes: 12. Critical: 0.
- Structure and ordering are sound: seven phases in the order the BUILD-REQUEST demands, standard gate counts exactly 3 / 3 / 7 / 2 / 2 with 2-agent verification rounds, one fix agent per gate, halt guards in the required order, completion items inside Phase 7, no static dependency cycle, all Phase 2 line anchors correct.
- The one real defect is staleness: the task file was built before the coordinator's binding addendum in research-notes.md and carries none of it (sibling Coder#477 and boundary, option scoring and "pending owner decision", claim-only acceptance and the integer-only prompt rule, sender-authentication and listener-contract research).

## Recommendations

1. Before execution, update the task file for B-1 (items 218, 232, 234, Key Constraints, References, Source Areas, Deviations). Then re-run this structure review; only B-1 needs rechecking, the minor notes are not rechecked.
2. Optional clean-ups while the file is open: N-2 (use a valid Blocked status), N-8 (reword the TODO/TBD search targets), N-11 (move the evidence-absence comments outside the quoted prompts), N-12 (add the two verdict files to item 338 and drop or consume the two inventories).

## Confidence and tool engagement

- **Confidence:** Verified: 16/16 checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% at the structural level. Limitation stated openly: I read the task file text in full for lines 1-185, 194-211 and 334-453, and read the other item bodies (186-192, 212-332) through targeted extracts of item headers, step headers, decision items 258/300/316/332, synth-03 item 232, web-02 item 218, assembly item 264 and pattern scans over all 64 items. Prompt bodies not read word for word could hide content defects, but the structural checks above (counts, ordering, producer/consumer map, token scans) ran over every item mechanically.
- **Tool engagement:** Read: 9 | Grep: 5 | Glob: 0 | Bash: about 27 (awk/grep/sed scans, existence and anchor checks, one `uv run python -I` YAML parse). Side effect to note: the YAML parse made `uv` create a `.venv` in the worktree; it is gitignored (`.gitignore:56`) and `git status` is unchanged (three untracked `.dev/` paths as before). The task file was not modified.
- No web research was performed (no Tavily or fallback calls).

## QA Complete

VERDICT: FAIL
