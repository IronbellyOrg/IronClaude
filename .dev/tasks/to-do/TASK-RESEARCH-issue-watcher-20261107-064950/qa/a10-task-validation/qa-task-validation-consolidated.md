# Consolidated task-validation findings (A.10): TASK-RESEARCH-issue-watcher-20261107-064950

Sources: qa-task-validation-b2-report.md (FAIL, 5 IMPORTANT) and qa-task-validation-structure-report.md (FAIL, 1 IMPORTANT). Consolidated by the orchestrator, 2026-11-07.

## Items Reviewed

### B2 self-containment lens

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


### Phase-structure lens

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


## Blocking findings to fix (apply ALL; minor notes optional)


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


### Structure lens blocking finding

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


VERDICT: FAIL
