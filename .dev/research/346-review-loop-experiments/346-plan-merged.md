# Issue #346: merged remediation plan

Revised 2026-11-09. This merges the owner's v2 plan, with its phase-5 update and do-not-repeat register, with the v3 evidence-driven plan.

- **Source baseline:** IronClaude master `933cf3a4`.
- **Experiment evidence:** branch `ironbelly/exp346-p1-logs`. Paths marked `exp:` are relative to `.dev/experiments/346-validation/` on that branch.
- **How the evidence was read:** as data only. Nothing was rerun.

## 1. Decision and authorization

**Decision.** Fix the remaining document-review convergence problems on top of PR #427. Keep spec-panel retirement (D1) a separate decision.

The phase-5 evidence changes the priority. #427's command text is not what blocks convergence. **The coordinator's review and revise instructions override it**, and nothing in the product stops that. So the first remedy is to remove the conflicting effective prompts and give coordinators a correct brief. Adding more review-loop machinery comes second.

**This document authorizes nothing.** It approves no implementation, experiment, retirement, installation, merge or deployment. Three items are presented for separate approval:

| Item | What it is | Needs |
|---|---|---|
| **A1** | Product PR (§5): effective-prompt, quota, installer and grading fixes | Owner approval to implement |
| **A2** | Review Loop extension (§6), written as a spec, then implemented | Approval to write the spec; separate approval to implement |
| **A3** | Replicated validation run (§8) | Explicit approval of the exact runs and tools |

**Standing constraints.**
- Do not invoke IronClaude, Orca, RF, Ponytail or affected workflow launchers for this work. Reading their source is allowed.
- A disposable environment does not relax this.
- DESIGN-BRIEF's required `Skill sc:design` invocation (`exp:phase5/DESIGN-BRIEF.md:28`) is not permission to override it.
- Portify is outdated and out of scope (owner's decision). It is excluded from remediation, completion gates and the D1 caller list.
- **PR route (owner's decision, 2026-11-09):** PRs for this work use the documented CLAUDE.md fallback, `gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> …`, after the mandatory pre-PR checks. `/sc:pr-submit` is not used, because it is an IronClaude invocation.

**Primary outcome.** A representative stalled document loop reaches either an implemented candidate or an explicit, bounded disposition within 3 reviews. Delivering known defects is a fallback, not a clean PASS. Critical or high-consequence defects stay visible for an explicit decision.

## 2. What the evidence shows

**Scope of the experiments.**
- **One document only.** It was the S1 Orca worker-contract spec (57,763 B), run through 3 reviews and 2 fix cycles. The other four incidents never call spec-panel (`exp:DECISIONS.md:41-42`).
- **The shipped #427 text was tested.** Its Review Loop is byte-identical to master `spec-panel.md:256-264`.

**Results.**

| # | Finding | Evidence |
|---|---|---|
| E1 | **#427 roughly halves growth.** Mean growth fell from 63.5% to 29.7%, and every #427 run grew less than every control run. The effect (33.8 points) is larger than the biggest within-arm spread (13.2). This is the only robust effect. | `exp:phase4/AB-REPORT.md:12-24` |
| E2 | **#427 does not make the loop converge.** No arm reached PASS. Mean new CRITICAL+MAJOR labels at the last review: 5.5 with #427 against 6 for the control, and 3.5 with the re-review flags. The flagged arm's improvement (2.5) is smaller than its spread (5). | `exp:phase5/FINAL-REPORT.md:75`, `:94-107`; `exp:phase4/ARMB-REPORT.md:59-67` |
| E3 | **Re-reviews still find defects in freshly fixed text.** Under #427, 89% (review 2) and 100% (review 3) of new findings are `origin=changed`. | `exp:phase4/AB-REPORT.md:30` |
| E4 | **The coordinator's briefs caused the FAILs.** Every arm kept "assume defects remain" and "any finding of any severity is FAIL", which contradicts #427 bullet 7. Under #427, revisers still acted on 7 and then 8 MINOR findings. Ponytail ended FAIL only because of a carried MINOR. So "no clean PASS" was partly built into the experiment. | `exp:DECISIONS.md:74` item 2; `exp:phase2/S1/briefs/task-text/T07…`, `T09…`; `exp:phase5/FINAL-REPORT.md:150-152` |
| E5 | **Restricted re-reviews miss real defects.** Diffgate had the lowest growth (10.31%), but its last review covered about 2% of the document, and a later full-document audit found 4 MAJOR. The ledger sweep found 9 MAJOR, including some in rows the loop had marked verified. | `exp:phase5/FINAL-REPORT.md:103-105`, `:120` |
| E6 | **The user's installed command copy shadows the project copy.** `make sync-dev` cannot activate a changed command, so stale installed copies are the real exposure. | `exp:DECISIONS.md:46` |
| E7 | **No variant is a validated winner.** Each was single and unreplicated: one reviewer's model changed, a parser recorded an invalid zero, the stoprule transcript check failed, and the minfix build halted. Prototypes must not be selected or combined. | `exp:phase5/FINAL-REPORT.md:101-107`, `:197-204` |
| E8 | **The control noise floor is contaminated.** The low control (ctl-r2) read the finished answer in `origin/master`. At n=2, no count effect below about 4 can pass. | `exp:phase4/AB-REPORT.md:29`; `exp:phase4/ARMB-REPORT.md:83` |

**Never tested.**
- Seeded severe or deletion-induced defects.
- A clean document, or a document with only minor findings.
- Interrupt and resume.
- PRD/TDD documents.
- **Any arm without the any-severity brief clause.**

**Measures are not interchangeable.** New severity labels, confirmed blockers, unresolved prior findings, carried-forward findings and audit unions measure different things. Controls had no post-loop audit, so audit unions must not be compared with the control's label counts. "Significant" in the reports means a predeclared practical screen, not statistical significance. Historical verdicts stay as reported; failed runs are not relabelled.

**Incident evidence from #346** is the author's observation, not a replay. Sizes went from 57,763 to 82,643 to 92,194 B. Findings went 24, 13, 14. Fix-induced defects were 10/24 and then 8/15; the 15 fixes include two citation fixes, so fixes are not findings. The constrained round 4 shrank the spec to 89,089 B with 7 findings, one of them a real logic defect introduced by a deletion.

## 3. Current status on master

| Concern | Status at 933cf3a4 | Action |
|---|---|---|
| Whole-document re-review | #427 Review Loop, `spec-panel.md:256-264`: re-review, baseline, changed-line scope | Keep. Extend it (§6). Do not reimplement. |
| Additive reviser | #427 bullet 6: revise only blocking text, no unrequested mechanism, cite finding ids, report bytes. Growth was halved (E1). | Add "prefer delete or narrow" and gross added/deleted bytes per finding (§6). No numeric cap. |
| Any-severity FAIL | `pragmatic.md:225-229` lets minor-only reviews PASS and caps loops at 2 fixes / 3 reviews. Briefs override this in practice (E4). | Precedence clause (§6), coordinator template (§5 A1-e), severity policy (§4). |
| Pressure to find defects | `pragmatic.md:221-222`: adversarial stance, zero findings treated as suspect. `task/SKILL.md:233`, `:430`: "at least N errors". | A1-a, A1-c |
| Pressure against simplifying | `pragmatic.md:232-233`: "Ship NO partial or simplified versions" | A1-b |
| Boundary table | `spec-panel.md:313`: at least 6 rows per guard. `:328-329`: FR-8/9 are MAJOR minimum and always blocking (`:259`). `:330`: FR-10 synthesis gate. | A1-g |
| Stale installs | `install_user_setup.py:67-83` skips existing files; `:140-152` only counts them. `superclaude update` force-overwrites without a backup. User copy shadows project copy (E6). | A1-f, porting #419's `install_core.py:94-101` |
| Coordinator brief | `HOW-WE-WORK.md:65` shows re-review arguments and the cap, but there is no paste-ready brief. E4 shows briefs win over the command. | A1-e |

## 4. Severity policy (owner's directive, to be specified)

**The directive.** Findings graded Medium or below trigger a warning only, plus a prompt asking whether to create a follow-up issue. They never fail a gate, demand a repair cycle or restart planning. Their evidence is kept. No issue is created and no PR is promised without the user's approval.

**Proposed mapping, by consequence and not by label.** The owner approves or corrects it before it is applied.

| Source label | Normalized | Gate effect |
|---|---|---|
| spec-panel CRITICAL; MAJOR that names a concrete wrong implementer outcome; FR-8/9 GAP with a concrete wrong outcome | High+ | Blocking |
| spec-panel MAJOR without a concrete outcome; FR-8/9 GAP without one | Medium | Warning, plus a follow-up candidate |
| spec-panel MINOR; pragmatic MINOR | Low | Note |
| pragmatic CRITICAL / IMPORTANT | Graded by the same consequence test | Blocking only if the consequence is concrete |
| Any label whose consequence is security, data loss or a safety boundary | Escalated regardless of label | Visible decision, never suppressed |

**Scope.** The policy covers **document-review gates**: spec-panel, `pragmatic.md` review rules, and RF document QA.

`/sc:pr-submit` currently routes Medium to `--fix` (`sc-pr-submit-protocol/SKILL.md:282`), and CLAUDE.md requires it to fix "Medium severity or higher". Extending the policy to pr-submit is a separate decision (D6) with its own tests. Until then, the two policies differ by design and that difference is documented.

**Who asks the question.**
- Reviewer subagents cannot prompt the user. They list Medium findings in a `follow-up candidates` section of their report.
- The top-level session asks **once per loop**, as a batched question.
- Under `spec-panel --unattended` (`spec-panel.md:451-459`), the list is only recorded.
- Approved issues use `~/.claude/ISSUE-BACKLOG.md` (core rule 10).

## 5. A1: product PR (requires approval to implement)

The evidence (E4) is enough to justify these without a new experiment. Each gets a text-contract test in the existing `tests/` style. Then run `make sync-dev` and `make verify-sync`, and run the CLAUDE.md `grep 'src/superclaude'` check over primitives.

| Id | File (master 933cf3a4) | Change |
|---|---|---|
| A1-a | `output-styles/pragmatic.md:221-222` | Report concrete defects with evidence. A zero-finding result is valid if it states what was checked. No quotas, no suspicion of zero. |
| A1-b | `output-styles/pragmatic.md:232-233` | Deleting or narrowing redundant text is allowed when requirements still hold. "No simplified versions" means no stubs. |
| A1-c | `skills/task/SKILL.md:233`, `:430` | Remove "assume at least N errors". Keep the checked-scope evidence. Reviewer-count floors stay under D2. |
| A1-d | `output-styles/pragmatic.md:225-229` and `spec-panel.md:259` | Apply the §4 mapping once the owner approves it. |
| A1-e | `core/HOW-WE-WORK.md` near `:65` | Paste-ready review and revise briefs (§7) that defer to the command's Review Loop. They may not contain any-severity FAIL, defect quotas or "apply all findings". After editing, copy the file to the plugin ref and the core CLAUDE.md level table, per CLAUDE.md. |
| A1-f | `cli/install_user_setup.py:140-152`, plus the command installer | Port #419's kept-file-differs warning to output styles and commands. Under `update`/force, back up a differing file before overwriting. Never overwrite customized or unknown files without a backup. |
| A1-g | `commands/spec-panel.md:313`, `:328-329` | Replace "at least 6 rows per guard" with one row per input class that applies. A GAP blocks only with a concrete wrong outcome, otherwise it is a Medium warning (§4). Keep FR-10. Real missing behavior, invalid states and safety boundaries stay blocking. |

**Budget:** about 4 engineering hours, including one review by someone who did not implement it.

## 6. A2: Review Loop extension, smallest coherent version

These are edits to `spec-panel.md:256-264` in place, written as prose. There are no scripts, parsers, state machines or new commands. Each bullet answers an observed failure but is unvalidated. If a script is chosen later, its machinery requirements (receipt handling, atomic writes, recovery) attach to that script, not to this contract.

1. **Precedence (bullet 7).** A brief cannot fail a minor finding, and cannot authorize editing one, including through "apply all findings". The report names any brief clause it overrode. *Answers E4.*
2. **Identity (bullet 5).** Prior blocking findings keep stable ids and get one disposition: `resolved`, `open`, `regressed`, `deferred` or `withdrawn`. `deferred` and `withdrawn` count as open for the verdict and for escalation. An uncertain identity match stays uncertain. *Answers the ledger and diffgate count drift.*
3. **Fail closed (bullet 3).** A missing or ambiguous resolution table or verdict line means FAIL. A zero is never inferred. *Answers ponytail's invalid zero.*
4. **Coverage.** A re-review PASS reads `scoped PASS: changed lines + prior blockers`. Whole-document assurance is a separate, labelled audit. Its blockers go to escalation, never to a fourth review. *Answers E5.*
5. **Reviser (bullet 6).** Prefer deleting or narrowing. Each addition traces to a blocking finding id. Report gross bytes added and deleted per id. No numeric budget and no forced shrink. *Diffgate hid growth inside long existing lines; minfix's budget was never measured.*
6. **Provenance (bullet 1).** The report header carries the baseline and candidate SHA-256, the command version and the actual reviewer model. *Answers the model switches in ponytail and ledger.*
7. **Cap (bullet 4).** No edits between fix 2 and review 3. A severity or necessity audit only reports. *This keeps 2 fixes / 3 reviews. Ponytail's audit saved 91 B, which does not justify an extra edit pass.*
8. **Medium findings (§4).** Listed under `follow-up candidates`. They never appear in the Reviser brief.

**Traceability.** The spec carries a table with columns existing behavior | observation (E#) | hypothesis | future validation (§8). This meets DESIGN-BRIEF's traceability requirement without its 06 template. It does not adopt the brief's requirements for asynchronous transport, parser or atomicity, for the reason given above.

**Budget:** about 3 hours for the spec, plus implementation and tests if approved.

## 7. Coordinator briefs, shipped through A1-e

**Review brief.**
> Review candidate [hash] for requirements [IDs], baseline [hash], prior report [ID], review [N of 3]. Re-check prior blocking findings as resolved/open/regressed/deferred/withdrawn. Inspect changed behavior and its dependencies; for inherited text, cite the changed line it depends on. Report concrete wrong outcomes, with no minimum count. Medium and below are warnings or notes and never fail the review; list Medium under follow-up candidates. Record severe older defects with their origin. If inputs are missing, return incomplete. Do not edit the candidate or launch another review. State coverage.

**Revision brief.**
> Repair only blocking findings [IDs] in candidate [hash]. Prefer deletion or narrowing while requirements still hold. Add no mechanism a listed finding does not call for, and link each addition to its id. Report bytes before and after, and gross bytes added and deleted per id. Leave minor and Medium findings untouched. Return the candidate and its disposition once. Do not award yourself a PASS.

There is one canonical copy, in `HOW-WE-WORK.md`, and it defers to `spec-panel.md` §Review Loop. There are no competing copies.

## 8. A3: future validation (requires exact-run authorization)

Before any run, cite the matching row of the register (Appendix B), name the prerequisite now satisfied and the hypothesis being tested.

**Arms.** Each changes one factor.
1. #427 with the original briefs. Reuse the existing phase-4 data (E1, E2).
2. #427 with the A1-e briefs. Only the brief changes.
3. Arm 2 plus the A2 extension. Only the contract changes.

**Design.**
- At least 3 replicates per arm, run concurrently.
- No access to `origin/master` or the answer.
- Model continuity verified.
- The loaded command bytes checked against E6.
- The same post-loop whole-document audit in every arm.
- Additive command names, so arms can run in parallel (`exp:phase4/AB-REPORT.md:47`).
- Fresh ids; original evidence preserved.

**Cases.**
- The S1 frozen packet.
- Seeded severe defects, including one introduced by a deletion and one regression of a prior PASS.
- A clean document.
- A minor-only document; request the SpecStory packet if available.
- One interrupt and resume.
- One PRD/TDD document.
- If the exact incident packet can't be obtained in time, use a clearly labelled surrogate.

**Record at each review:**
- bytes, plus gross bytes added and deleted
- new mechanisms
- findings by normalized severity and origin (missed-old, fix-induced, reopened, prior-PASS regressed)
- reviews and fixes
- transport retries
- elapsed time
- measured tokens or cost when available, never assistant turns as a stand-in for dollars

**Five checks.**
1. Each run ends at an implemented candidate or an explicit disposition within 3 reviews. Report which one occurred.
2. Clean and minor-only cases PASS without invented defects or a full restart. Unreadable input returns incomplete.
3. Every seeded severe defect stays visible. A smaller document that lost required behavior fails.
4. Corrections address only the named blockers and report growth. Medium and minor findings stay recorded.
5. Resume preserves identity, baseline, spent budget and prior findings. Nothing runs automatically after the cap.

**Success** means arm 2 or 3 beats arm 1's last-round blocking count by more than the within-arm spread, with growth no worse and checks 2 and 3 passing. When the budget runs out the run terminates; that is never a PASS. Publish once. Continuing needs a new scoped approval.

## 9. Separate decisions

- **D1. Retire the spec-panel family.** Deferred. The evidence shows no harm unique to the panel; the FAILs trace to briefs (E4). Retirement would require complete migration of verified active callers (CLI-eval, generated tasks, installed overlays; Portify excluded), preserving PRD/TDD, evaluation, roadmap/comparison, Ponytail and Coder distribution, tests on clean, existing and customized homes, and a rollback path.
- **D2. RF reviewer floors** (`task/SKILL.md:121-122`, `:194`). Follow-up. Compare a scoped reviewer against matched work before claiming equivalent severe-defect coverage. The quota text itself moves to A1-c.
- **D3. Bound correction.** Covered by #427, A2-7 and the 2-fix / 3-review cap. One correction plus one recheck is only an optional matched variant. Separate from `/sc:implement`'s A1–A5 ladder.
- **D4. Read-only reviewer, report-write enforcement.** Follows up #465, unless report delivery blocks A3.
- **D5. Remove finding quotas and conflicting FAIL rules.** Now carried by A1 and A2-1. Do not substitute Coder's BMAD reviewer: its pinned contract demands 10 findings and halts on zero.
- **D6. Whether the §4 severity policy applies to `/sc:pr-submit`.** New. Needs an owner decision and pr-submit tests.

Delivery, provider retries and #431 liveness keep their own acceptance criteria and do not gate this work.

## 10. Open items and limits

**Open items.**
- FINAL-REPORT still has a stale bundle checksum inventory (`:252`) and a history row marked "pending" (`:257`).
- REFACTOR-SPEC was never written; A2 replaces it.
- The exploratory repeats stay paused.
- A dev checkout cannot exercise a changed command (E6). File this as its own issue.

**Not validated.**
- The original private incident artifacts.
- The exact historical effective prompts.
- The current host installation.
- Severe-defect detection under the affected runtime.
- Runtime cost.

**Earlier local work.** A two-agent report-write and blocking-label patch, with 22 passing contract tests and 5 caught mutations. This is not a deployed fix.

---

## Appendix A: Provenance

- **IronClaude master:** `933cf3a4f5fd3e4d8cce8f69c9168a2631574179`.
- **Coder:** `ad26796a00f9a11b443f8ecff50e20ec833e3087` (BMAD contract).
- **Phase-5 blobs:**

| File | Git blob |
|---|---|
| FINAL-REPORT.md | `e14f5070…` |
| DESIGN-BRIEF.md | `441a97b6…` |
| FINAL-REPORT-QA.md | `7f8e9cb5…` |
| final-summary.json | `009ee215…` |
| PR-427 command (provenance copy) | SHA-256 `c8d80346…df2f` |

- **First research:** libfile_1360c047…, SHA-256 `a346b5e7…`. Fifty sessions back to Oct 28. Numbers: 19,305 primary turns; 204 failed / 130 passed gate observations; 120 retries / 94 fixes; RF 342 invocations / 9,512 responses. These are overlapping observations, not causal rates.
- **Removal proposal:** libfile_1319ca1b…, SHA-256 `da2cd98a…`. Shares provenance with #346 comment 6743577180, so it is not independent corroboration.
- **Critical feedback:** libfile_1967512c… (56 lines). Its score is opinion; its claims were assessed one by one.
- **Links:** issue #346 and comments 6580209959 and 6580582388; PR #427; issues #465 and #431; PR #419.

### Critique history (condensed)

- **Accepted.** The earlier plan was too broad, buried the distinction between shipped and open work, omitted growth as a measure and had no stop rule.
- **Qualified.**
  - The earlier plan did gate retirement and did acknowledge #427.
  - A reviser contract already existed.
  - D4 is related to #465 but distinct from it.
- **Rejected.** A live rerun under the current authorization.

## Appendix B: Do-not-repeat register (condensed; full v2 tables retained as companion)

**Rule.** Before proposing a repeat, cite the row, state the prerequisite now satisfied and name the hypothesis still untested. Never rerun an unchanged invalid setup. A repaired parser, a completed build or an approved report is a milestone, not convergence evidence. Retests use new ids and preserve the original endpoints.

| Attempt | Endpoint and limit | Prerequisite before any authorized retest |
|---|---|---|
| Phase-1 log/tasklist searches | 5 incidents found; I1–I3 original briefs absent | Immutable originals, or a labelled surrogate |
| Phase-2 S1–S5 reach | Only S1 uses spec-panel; S2–S5 not rerun | Tool-specific hypotheses, not #427 evidence |
| Precedence probes A/B | User command shadows project copy (E6) | Verify the loaded bytes before dispatch; no unapproved machine-wide swaps |
| Phase-3 T-pinned A/B | Confounded by global #343 rules, mid-run install and answer file, and terminal intervention | Concurrent control, stable inputs, no exposure |
| ctl-r1 | Labels 11/9/8; 57.72% growth; FAIL | Matched instruments |
| ctl-r2 | Labels 12/7/4; 69.34% growth; FAIL; **read the finished answer in origin/master** | Exclude or rerun without exposure |
| trt-r1 / trt-r2 (exact 427) | Labels 9/5/6 and 9/7/5; 23.11% and 36.27% growth; FAIL; installation-stability check failed | Stable effective source |
| flg-r1 / flg-r2 | Labels 16/5/6 and 17/6/1; 27.78% and 32.14% growth; FAIL; 6 MAJOR labels against 4 blocking grades | Separate labels from grades; matched timing |
| Brainstorm specs (5) | Predictions only, not measurements; ledger effort exceeded its estimate | Do not rebuild every candidate automatically |
| Smoke dispatch | Partial; ledger heartbeat prerequisite unmet | Receipts per route |
| Diffgate build and loop | Labels 7/2/2; 10.31% growth; FAIL; about 2% final coverage; answer exposure; external replacement | Immutable isolated target, coverage accounting, model continuity |
| Diffgate audit | 4 MAJOR; union 5–6; audit model differed; controls had no audit | Matched audit, or label it safety-only |
| Ponytail build, audit and loop | Labels 9/7/0; FAIL on a carried MINOR; parser exit 2 with an invalid zero; model changed; audit saved 91 B; writes the spec before its logs | Fail-closed format checks, model continuity, write-failure injection |
| Ledger build, loop and sweep | Labels 13/9/3; ESCALATE; sweep 9 MAJOR, union 11–14; model change; 429 retries | Matched or safety-only sweep, stable ids |
| Stoprule build and review | Replay gave 8/0 against the predicted 5/3; first review had 6 confirmed of 8; asynchronous receipts unrecognized; trial invalid | Receipt-integrity tests; keep the counterexample |
| Minfix plan and build | 4 blocking plan issues; task 3 halted (F5.1/F5.2, then F6.1); 84 tests pass; tasks 4–8 unbuilt | Minimal F6.1 regression and a runnable candidate before any trial |
| Exploratory repeats (diffgate-r2/r3, ponytail-r2/r3) | Unauthorized; first reviews only; paused; specs unchanged | Explicit exploratory approval; no resume on a generic "proceed" |
| Pause-command delivery | `worker_identity_changed`; recorded as attempted, not delivered; misattributed as an owner order | Receipt verification; accurate attribution of authority |
| Cooldown and watch loops | Many 429 retries; monitor gaps | Bounded retry budget; evidence of progress |
| Final-report worker and retries | Launch failed; repeated 429s; the coordinator wrote the report directly | A bounded fallback for report delivery |
| Numeric checker | KeyError fixed; later checks PASS | A checker PASS is not semantic truth |
| First-run fidelity review | Measurements PASS; overall FAIL for unauthorized repeats | Keep the original FAIL |
| FINAL-REPORT-QA | Source-fidelity PASS | Not design acceptance or convergence |
| Design-session attempt | API 429; no completed design | Independent-tools constraint; A2 replaces it |
| Bundle inventory | Original SHA256SUMS incomplete; final inventory still pending | Regenerate after the authorized deliverables |
