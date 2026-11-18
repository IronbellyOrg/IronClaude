# Final Summary: Review Panel Unification, Run 2

Status: In Progress

Scope of this file: a plain-English summary of the finished research report. Every number and name below was read from the report, from the final validation checklist, or from file counts (Glob). Nothing is estimated. Short ids are kept only where the report uses them, each with a one-clause meaning.

## 1. What this is and what was not done

- **Report path:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/RESEARCH-REPORT-review-panel-unification-run2.md` (5,098 lines, 10 sections plus two appendices).
- **Question it answers (Section 1):** which ONE unified central Review Panel design (a shared core plus thin modules) captures the value of the three earlier efforts and keeps future PR code review and rf-qa replacement unblocked. The three efforts are E1 (the reflect Tier 2 panel kernel with its shadow mode and model-combination experiment), E2 (the tasklist review-panel study, collaboration designs and process-redesign brainstorms) and E3 (the #346 spec-panel review loop plus five installed-only variants).
- **Final validation (qa/final-validation-checklist.md):** Overall Verdict PASS, 0 blocking failures. 21 of 23 checks pass outright; 2 checks (item 3, citation form in the Section 2 measurement tables; item 13, one miscount) failed as MINOR only. The one wrong figure: the report says `tests/pr_submit/` has 50 test files, but 47 `test_*.py` files exist. No decision depends on it.
- **FINAL_REPORT_SHA256:** `b3195608a09aa4c9d069dd4779e8b8e04284bc975cbaa84f1e90d4b56ce50775` (the validation read the report without modifying it; its hash equals the Gate 3 pass hash).
- **The report is report-only.** It contains no roadmap, no branch plan, no PR plan, no risk register, no schedule and no implementation. Section 8 is explicitly "inputs for a later plan".
- **No commit and no push was made.** A read-only check at the time of writing showed HEAD still at `50d4d2b9d` (the run-1 commit) and the run-2 task folder listed as untracked (`??`). This summary step wrote one file and ran no git write command.

## 2. Key findings (10 bullets, each with its report section)

1. **The three efforts overlap very little and conflict a lot** (Sections 1 and 2.9.10). The overlap matrix has 16 rows: 11 conflicting, 1 identical (ids), 2 unique to E1 (calibration, memory) and 2 unique to E2 (eval harness, collaboration). 12 of 48 cells carry no mechanism. 21 conflicts are logged in the overlap section (CF-01 to CF-21, the conflict ids of Section 2.9).
2. **E1 holds two different Tier 2 engines** (Section 1). The in-process swarm ensemble behind `superclaude reflect run` (engine A) and the prose skill panel with its shadow mode (engine B) share only `contract.py`. The panel kernel in `cli/review` is wired only to engine B.
3. **E2 shipped no product code, and the quality evidence is thin** (Sections 1 and 7.0). E2 changed no file under `src/` or `tests/` at any commit. E1 has no ground-truth scoring for any of its 30 runs, and its Stage 2 exit reads `OVERALL: FAIL (shadow runs 13 of 20)`. E1 and E2 are one evidence family (the E1 input is byte-identical to the E2 candidate).
4. **The defects that decide verdicts are real and pinned by tests as intended** (Section 7.0, facts F-6 and axis 4). A row clears by silence, one valid reviewer of N gives PASS, a stored verdict goes stale, and `defer` can rewrite ESCALATE to PASS. All were reproduced.
5. **No product code records the model that actually served a reviewer** (Sections 1 and 2.9.10). Every diversity, parity and identity field is computed from requested values.
6. **Gap analysis: 148 gaps** (G-01 to G-148): 24 Critical, 93 Important, 31 Minor (Section 4.1).
7. **Conflict log: 189 conflict rows** (Section 6.12.10): 134 decided by evidence, 55 not decidable by evidence and routed to 15 debates.
8. **All 15 debates produced a winner, but every one returned status `partial`** (Sections 6.12.9.1 and 7.3). No debate ran a third round, and the debates left 244 invariants unaddressed: 60 HIGH, 161 MEDIUM, 23 LOW.
9. **The final shape does not block any future use** (Section 7.2.4): PR code review NO, rf-qa and rf-qa-qualitative replacement NO, later reviewers NO, each with stated conditions. Five candidate skills were not read and carry no verdict (7.2.3).
10. **The value inventory is complete and reconciled** (Section 8.1.0): 5,950 rows in, 5,950 rows out (5,779 ledger rows plus 171 defect-register rows), every row with exactly one destination.

## 3. The recommendation (Section 7), in one paragraph

The report recommends ONE design, named **One Shared Review Panel Core: a Thin Shared Contract with Per-Module Engines**, living in the existing package `src/superclaude/cli/review/` and reached by installed skills and commands only through the `superclaude review ...` command line. The shared core is a thin contract: one finding id grammar, one limits module and one repair step that both parsers call, one reference-token list (with the tasklist `T<PP>.<TT>` task reference added once), hash and identity helpers, panel and tier resolution from one reviewed tier file, a run record (per-run events file, a manifest lock, a cross-run telemetry export), a dispatch contract (the core launches nothing; a reviewer is launched with its `launch` word), and a tested evaluation script set. It does not force one engine: the spec-review module keeps the v1 anchor engine (`findings.py`, `ledger.py`, `review-ledger/1`), while reflect and later PR review use the v2 citation kernel. Every consumer is a thin module made of profile data (vocabularies, label maps, reference patterns, lens and role tables, cap), brief blocks and an output adapter; no consumer copies core text. Reflect keeps contract 1.8.0, the pure `derive_verdict` function with its 36-test matrix, and, for now, engine A as the production Tier 2 engine. Convergence to a single engine is a recorded later path with three triggers (T-a, T-b, T-c), not the starting point. The report notes this differs in one respect from the owner's wording "one shared core with thin modules": the core is a shared contract plus two engines side by side, not one engine (Section 7.0.1).

### What each use needs from the design (Sections 7.0.1, 7.1 and 7.2)

| Use | What it needs | Report verdict |
|---|---|---|
| Reflect | Contract 1.8.0 byte-identical; `derive_verdict` and its 36 tests unchanged; engine A stays production Tier 2; deterministic shadow steps move into code as helpers that write comparison siblings; the six `review-panel.reflect-*.json` templates and the `reflect-pre` and `reflect-post` lenses | Kept; no engine moves now (debate C-04) |
| Tasklist and workflow review | Reflect UC-1 stays the only entry (`/sc:reflect --mode pre`); the panel enters inside reflect Tier 2; advisory at workflow Wave 4, "advisory-blocking" at tasklist Stage 10.5, blocking at the post gate T5; a ref pattern for `T<PP>.<TT>`, the five Stage 7 dimensions as lenses, a High/Medium/Low label map as module data; no plugin copy | Kept (debate C-05); whether Medium blocks is unresolved (Section 8.3 of this file, question Q-89) |
| Spec review (`sc:spec-panel`, later `sc:brainstorm` and `sc:design`) | The v1 anchor engine with quorum-gated explicit clearing (silence never clears), typed `blocking` plus a CRITICAL floor, `defer` terminal and counted open, verdict derived on read, any-blocking union with a merge-time quorum refusal | Kept (debates C-02, C-03) |
| Later PR code review | The v2 engine; a separate main-session pre-step; a pure converter on the `pr_submit` side from `cluster_v2` output to `pr_submit.Finding`; a sibling `panel` field in the Output Contract; module-declared category, lens and severity sets; reviewers read-only at process or tool level; first release report-only | NO block (Section 7.2.4, debate C-10) |
| Later rf-qa and rf-qa-qualitative replacement | Mechanically read-only reviewers on every launch lane it uses; one separate fix agent; first change is lens-level: one new read-only lens-reviewer agent plus a replay oracle, no panel engine in any rf-qa gate; checklist mode, document-type packs and agent-count floors only for a full replacement | NO block (Section 7.2.4, debate C-11) |

## 4. Overlap and value-inventory headline numbers

### Overlap matrix (report Section 2.9.4)

| Measure | Number |
|---|---|
| Capability rows in the matrix | 16 |
| Rows classed conflicting | 11 (finding schema, identity and hash, merge and dedupe, clustering, citation verification, verdict, ledger and rounds, panel/tier/profile, dispatch, brief, telemetry/manifest/run record) |
| Rows classed identical | 1 (ids) |
| Rows unique to E1 | 2 (calibration, memory) |
| Rows unique to E2 | 2 (eval harness, collaboration) |
| Rows classed superset or unique to E3 as a primary class | 0 and 0 |
| Cells with no mechanism (of 48 = 3 efforts x 16 rows) | 12 in total: E1 2, E2 6, E3 4; 33 cells have a mechanism of their own and 3 reuse another effort's mechanism |
| Conflicts logged in the overlap section | 21 (CF-01 to CF-21) |
| Section 1 wording of the same finding | the efforts overlap in 4 places and conflict in 12 registered places (conflict ids C-1 to C-12 of research file 01) |

### Value inventory (report Section 8.1.0): rows per destination

| Destination | Rows |
|---|---|
| CORE (the shared core) | 948 |
| MODULE-reflect | 278 |
| MODULE-tasklist | 340 |
| MODULE-spec | 69 |
| MODULE-pr-review | 45 |
| MODULE-rfqa | 53 |
| EVAL (evaluation) | 1,365 |
| HARNESS (study harness) | 467 |
| KNOWLEDGE | 416 |
| DROP | 1,969 |
| **Total** | **5,950** |

Rows by source ledger (research files 19 to 24 plus the defect register): ledger 19 (handoffs) 886; ledger 20 (E2 study) 868; ledger 21 (brainstorms) 1,685; ledger 22 (collaboration designs) 955; ledger 23 (E1 and E3 code) 796; ledger 24 (evidence and consumers) 589; defect register (DR-001 to DR-171, the 171 numbered defect rows) 171. Rows in: 886 + 868 + 1,685 + 955 + 796 + 589 = 5,779 ledger rows plus 171 defect-register rows = 5,950. Rows out: 5,950. DROP reasons: duplicate of a named id 1,753; obsolete 126; out of scope for a report-only task or evidence-free 86; [CODE-CONTRADICTED] 4. The rows themselves are carried unchanged in Appendix A (the file `synthesis/synth-08-value-inventory.md`).

## 5. Conflict outcomes (report Sections 6.12.10 and 6.12.9.1)

### Counts

| Outcome | Count |
|---|---|
| Conflict rows in the log (tables A to G) | 189 |
| Decided by evidence (the code or a measurement settles it) | 134 |
| Undecidable by evidence, routed to a debate | 55, grouped into 15 debate slots |
| Adjudicated by debate (each folder has an `ADJUDICATION-RESULT.md`, counted with Glob) | 15 of 15 |
| Left open as NOT ADJUDICATED | 0 |
| Points left unresolved inside a debate | Debates did not fully converge in most cases (for example 24 of 28 points converged in C-06, 21 of 26 in C-07, 32 of 37 in X-15). Examples: the claim cut in C-06, whether Medium blocks in X-15. These are carried as open questions (Section 7 of this file) |

The report states: every debate ran at depth `standard` (Rounds 1, 2 and 2.5, no Round 3), returned status `partial`, and the "winner" is always a hybrid the debate itself produced on the named base; no proposal won as written. The margins are the debates' own scores.

### What the evidence decided (134 rows, examples the debates had to respect)

MINOR is never blocking; the reflect convergence threshold is 0.80 and a single-vendor panel degrades (decided by `contract.py:310-326` and the 36-test matrix); the verdict is derived from rows on every read and never stored; the served model is recorded from the transcript, never from the orchestrator; reviewers are mechanically read-only and the reviser is a separate role; E1 and E2 are one derivation set; where documentation contradicts the code, the code wins (13 claims and 15 research-versus-research or document-versus-code contradictions).

### The 15 debates and their winners (as the report states them)

| Slot | Topic | Winner (as stated in the report) |
|---|---|---|
| C-01 | Core shape and finding contract | Variant B as base (a thin shared contract with per-module engines), plus one change from A (anchor status of each blocking row shown in the per-row block). Scores: A 0.8760, B 0.8515, margin 2.45 percent, decided by the tiebreaker. |
| C-02 | Ledger clearing and verdict authority | Variant B (explicit per-row verification) as base, with A's quorum gate, record-only evidence key and CRITICAL floor. Scores: A 0.9000, B 0.9148. |
| C-03 | Merge verdict policy and quorum | Variant A as base: any-blocking union as a pluggable policy, quorum as a merge-time refusal, no calibrator in the default. Scores: A 0.9007, B 0.8590. |
| C-04 | Reflect Tier 2 engine composition | Variant 1 (A) as base, merged as H-C04: a code-owned write side behind a gated shell; no engine moves now. Scores: V1 0.9302, V2 0.8611. |
| C-05 | Consumer entry, effect and delivery | Variant A as base: reflect UC-1 stays the single entry, no direct panel call, no panel-only plugin copy. Scores: A 0.8728, B 0.8904 (B ahead; the tiebreaker selects A). |
| C-06 | Limits and repair policy | Variant B as base: itemised drop record, dropped-blocking refusal, cut of the three location fields to 200 characters behind `repair=False`, one stateless re-ask. Scores: A 0.8466, B 0.9474. The claim cut stays unresolved. |
| C-07 | Dispatch and launch mechanism | Variant 2 (B) as base: the core launches nothing; the class-word Agent call ships; the raw-id `claude -p` launcher is gated, not built. Scores: V1 0.8053, V2 0.9233. |
| C-08 | Run record and served-model capture | Variant 1 (A) as base: per-run `events.jsonl`, manifest keeps five keys plus a lock, `review-telemetry/1` with a strict mode. Scores: A 0.8969, B 0.8956 (margin 0.13 percent, tiebreaker). |
| C-09 | Panel resolution and tier source | Variant B as base: Coder env slots decide models, packaged tier file is the reviewed copy, soft distinctness stays the default. Scores: A 0.8969, B 0.8767 (tiebreaker). |
| C-10 | PR review wire format and slot | Variant A as base, resolution C10-R: separate pre-step, pure converter on the `pr_submit` side, sibling `panel` field. Scores: A 0.8452, B 0.8679 (B ahead; tiebreaker level 1 selects A). |
| C-11 | rf-qa first step and read-only scope | Variant B as base: lens-level first change, one new read-only lens agent and a replay oracle. Scores: A 0.8809, B 0.9167. |
| C-12 | Collaboration exchange capability | A staged hybrid on Variant A: the static kit and H1 to H4 now with `kit: off`; exchange not built. Scores: A 0.9198, B 0.8747. |
| X-13 (report slot C-13) | Process-redesign modules | Variant A (Sweep-Sheet-shaped) as base: optional card format and row block, advisory row check, no demotion or promotion. Scores: A 0.8685, B 0.8591 (tiebreaker). |
| X-14 (report slot C-14) | Evaluation acceptance and harness owner | Variant A as base: three acceptance tiers (S, Q, G), tested `scripts/` plus `tests/` set, kernel `verify-run` deferred. Scores: A 0.9157, B 0.9060 (tiebreaker). |
| X-15 (report slot C-15) | Tasklist Medium and fidelity vocabulary | Variant B as base: label map as module data, fidelity prompt stays outside the core. Scores: A 0.9138, B 0.8664 (B wins by the tiebreaker). Whether Medium blocks stays UNRESOLVED (50 percent). |

Meaning of the slot ids: C-nn is the conflict slot in the report's conflict log; X-13, X-14 and X-15 are the names the debates used for slots C-13, C-14 and C-15. Debate folders are under `reviews/adversarial/<slug>/`.

## 6. Research file counts (Glob, run on this task folder)

| Group | Pattern | Expected | Found |
|---|---|---|---|
| Research files | `research/[0-2][0-9]-*.md` | 24 | 24 |
| Web research files | `research/web-*.md` | 4 | 4 |
| Scope slices | `research/scope/*.md` | 12 | 12 |
| Synthesis files | `synthesis/synth-*.md` | 10 | 10 |
| Debate folders with an adjudication result | `reviews/adversarial/*/ADJUDICATION-RESULT.md` | 15 (the report's 15 debates) | 15 |

All counts match the expected numbers and the report's Evidence Trail (Section 10).

## 7. Open questions that matter most (report Section 9)

Section 9 holds 93 questions (Q-01 to Q-93), each with impact and a suggested resolution. Its coverage check counts 363 logged-open rows from the gaps log: 185 [UNVERIFIED] rows, 124 Important and 49 Minor open-question rows, and 5 stale-documentation rows. No [CODE-CONTRADICTED] row is open; one follow-up remains (Q-34, a memory line about cluster calibration parsing). The ones that decide the most:

| Question | What it is, in plain words | What it blocks |
|---|---|---|
| Q-42 | Where does the per-round "requested reviewers" count come from when the resolution file is absent? Four debates use it (quorum, floor, eligibility, resolution record) and none fixes its source. | The quorum rule of the v1 engine: a partial panel can pass or a one-reviewer re-review can deadlock. Marked HIGH. |
| Q-43 | Can the shared repair step sit inside both parsers while every existing test pin stays unchanged? | Debate C-01's one HIGH invariant, the C-06 repair policy and the H2 half of C-12. |
| Q-44 | What does "accepted" mean while the identity check reads `unrecorded` (no writer of the observed-model record exists; the usage clause measured 0 of 15)? | Acceptance of every use case. Marked HIGH. |
| Q-41 | What does "no change to `cli/reflect`" allow? The H1 brief edit at `cli/reflect/ensemble.py:601-630` and the placement of the write-side helpers are not covered by the weak reading. | Whether H1 reaches reflect at all in the first change. |
| Q-09 | Does the reflect wrapper switch to engine B, or does engine A gain executor exclusion? Who supplies the executor class for tasklist plans? | The single-engine decision, named but not scheduled in debate C-04. |
| Q-06 | What is the quorum for PASS, and is clearing a row on an invalid reviewer block a bug or a contract? | The defect fixes in the v1 engine; the fix rewrites tests that pin today's behaviour. |
| Q-39 | [POST-BASELINE] Do the newer commits on the tasklist study branch (newest `e2f2ac268`) answer the premise of debate C-12? They were not read. | The "defer" half of the C-12 outcome. |
| Q-46 | Which caller makes gateway panels reachable? `--env gateway` still refuses without an explicit tier file. | The gateway benefit claimed for C-09 and the reach of C-07. |
| Q-37 | External evidence the web research could not settle (no peer-reviewed study comparing quorum rules for finding-set review; hook schema and GitHub API behaviour only partly retrieved). | Quorum choice and the hook-based collaboration design rest on partial evidence. |

Evidence limits the report itself states: no run compares core shapes; no quality measurement of any merge policy exists; every E2 ledger is round 1 only; re-ask recovery is unmeasured on gateway models; the debates scored the documents as written, not measured outcomes; nothing in the design has been run.

## 8. Owner decisions the report leaves open

### 8.1 Commit and push

- **Q-35: may this run's `.dev/tasks` output be committed and pushed (no PR)?** The owner ordered commit and push (no PR) after run 1; no instruction covers run 2. The report says the task only stages `.dev/tasks` at its last phase, and staging is not committing. Recommended by the report: wait for the owner's word unless the owner repeats the run-1 instruction. No commit and no push has been made.

### 8.2 Conflicts and invariants

- **Conflicts marked NOT ADJUDICATED: none.** All 15 slots were adjudicated and all 55 routed conflict rows have an outcome (Sections 6.12.9.1 and 6.12.10).
- **Unaddressed HIGH invariants: 60** (of 244 invariants the debates left open: 60 HIGH, 161 MEDIUM, 23 LOW; Section 7.3). No debate ran a Round 3, so none is resolved. Per debate (HIGH): C-01 1, C-02 3, C-03 2, C-04 0, C-05 7, C-06 4, C-07 1, C-08 13, C-09 0, C-10 5, C-11 6, C-12 2, X-13 2, X-14 12, X-15 2. Every HIGH and MEDIUM one is mapped to an open question in Q-41 to Q-88. The largest groups are C-08 (run record, 13) and X-14 (evaluation, 12).

### 8.3 Decisions only the owner can make (named in the report)

| Question | Decision | Why it is open |
|---|---|---|
| Q-40 | Does the owner accept the reading of "one shared core with thin modules" as a thin shared contract with per-module engines (spec review on v1, reflect and PR review on v2)? Or does the owner want one engine now? | The debate for C-01 produced the two-engine reading. If the owner wants one engine, the triggers T-a, T-b, T-c and an anchor-span precondition become plan inputs. |
| Q-41 | What does "no change to `cli/reflect`" allow (the H1 brief edit and where the helpers live)? | Two debates adopted the weak reading (additive files only); these edits are not covered by it. |
| Q-89 | Does Medium block in the tasklist module? | Debate X-15 left it UNRESOLVED (50 percent): keeping Medium blocking touches no pinned test; making it a warning rewrites pinned tests and is adopted only if measurements F1 to F3 pass. |
| Q-90 | May panel findings drive a push in PR review, beyond the report-only first release? | The debate leaves it to the owner, ideally after the per-round cost measurement and the acceptance work. |
| Q-91 | Are the `/task` standard lens dimensions switched to the new read-only lens agent, and which "eight lens" set is meant? | The switch also needs a pre-registered rule that does not exist yet; otherwise `task/SKILL.md` stays byte-identical. |
| Q-92 | Who owns the E2 harness in the main line (the study tip is not an ancestor of HEAD and `lib/` is hidden by `.gitignore:13`), who writes and pays for the Tier G tests, is `_blocks_after` exposed as a public helper, and is a kernel `verify-run` built? | No recorded owner and no CODEOWNERS entry. |
| Q-93 | Plugin delivery for the panel, reflect, the reviewer agent and the CLI, decided once as one set; and the product decision DO4 on the tasklist and workflow entry. | Plugin installs have no reflect, tasklist or panel path today. |
| Q-38 | Keep or archive the five installed-only spec-panel variants under `~/.claude`? | No debate slot; machine-state cleanup with no effect on the core design. |
| Q-36 | The list of earlier owner decisions carried together: bug versus contract for the clearing defect and the quorum rule (Q-06), reflect threshold and single-vendor posture wording (Q-08, the code already decides 0.80 and degrade), verdict owner (Q-05), canonical severity pair (Q-04), location type and container (Q-02), repair policy and H1/H2 (Q-01), roster and exclusion ownership (Q-13), `lib/` gitignore (Q-30), approval of the success targets T-1 to T-10 (Q-26), the +35% elapsed limit (Q-20), funding of the 326-run validation, the arm-A rerun, the blind scoring of the 15 E1 runs and a controlled dispatch replay (Q-10, Q-20, Q-25), the named owner of `verify-run` (Q-27), whether the E2 recommendation `ember + 2x luna` counts as evidence (Q-25), and removal or archiving of the installed variants (Q-29). | Each decides an axis of Section 6 or a gate input of Section 8.2 of the report. |

The report names the next step after this report as an adversarial comparison and merge of the two reports, then a workflow plan (`/sc:workflow ... --depth standard --handoff none`). It does not start either.

## 9. Final state

- The report is report-only: no roadmap, plan or implementation was produced.
- No commit and no push was made.
- Independence held: this summary read no file of the earlier run-1 folder or of the queued-run note.

Status: Complete


