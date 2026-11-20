# Round 1 — Advocate for Variant 2

Variant: reviewer-2 card (QA, requested haiku). This is a review of a future implementation plan, not a claim that its future modules already exist. No plan or production files are changed.

## 1. Steelman the other cards first

**Variant 1.** Its strongest work follows information from the current watcher into the proposed tests: a retry cannot reconstruct a Status-specific launch from data it never saved, and a value-time predicate needs an unambiguous Project item before the later helper task exists (C-007, C-008). It also correctly spots that the warning task confuses a runtime account value with offline configuration, and that broad completion patterns can block ordinary development commands (C-009, C-004). These are concrete implementation hazards, even where their severity is not Blocking. Confidence: 0.97.

**Variant 3.** Its cross-repository approval finding is the strongest new safety finding: changing watcher reads while deliberately leaving the coordinator's approval reads on the old default can approve work using evidence from another repository (C-001, U-001). It also exposes the empty-Pipeline/time ambiguity and the mismatch between the session that uses the brief and the levels tested there (C-002, C-006, U-002). Those findings materially improve the review beyond Variant 2's narrower acceptance-check pass. Confidence: 0.98.

## 2. Variant 2's strengths and the grading correction

Variant 2 contributes three independent, actionable checks: the only Coder handoff fails to specify the required boot/restart lifecycle (QA-1/C-005/U-004); the required claim-event refusal has no named implementation boundary (QA-2/C-003/U-003); and a literal must-refuse command cannot match any proposed completion alternative (QA-3/C-004). Coverage of a requirement by task number is not proof that the task supplies the required content or a meaningful test.

I withdraw the card's inconsistent severity presentation. Under the supplied rubric, **QA-1 is Blocking (Missing), QA-2 is Blocking (Decision), and QA-3 is Blocking (Decision)**, not MEDIUM. These are failures of required handoff content or explicit acceptance checks; I am not upgrading the text matcher into a security boundary. Confidence: 0.98, 0.98, and 1.00 respectively. QA-4's Project-selection contradiction also needs a Blocking (Decision) correction, as explained at C-014; its missing test alone would not justify that upgrade.

The card's claim that explicit dependency edges point backward is sound, but its blanket conclusion that ordering is sound was too broad (C-010/X-003). Its Q-6 FIXED judgment must also become PARTIAL because the adopted proposal explicitly requires an additional marker-reader test (X-002). Confidence: 0.97.

## 3. Evidence-backed positions, C-001 through C-014

Each position below gives a truth verdict, the severity under the supplied rubric, a confidence from 0 to 1, and the point-by-point concession or critique of the competing cards. All citations are absolute paths in the current checkout; cited ranges were read in this round.

### C-001 — coordinator approval reads are not repo-threaded

**TRUE — Blocking (Safety). Confidence: 0.99.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_pipeline/cli.py:266-282` takes no repo argument and calls both `gh.reread` and `read_stage_evidence` without one; `:343-348` defaults to the single legacy config. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_pipeline/reads.py:65-67,130-148` also fails to pass a repo for comments, events and edits. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/github.py:37,74-89` supplies the fixed fork target today. The plan explicitly preserves those defaulted coordinator reads in `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:227`, while Task 23 at `:313` runs per-repo watchers. The coordinator is required to use this approval gate in `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/core/WORKER-CONTRACT.md:298`.

I concede V3/U-001 outright; V1 and V2 missed an authorization-context boundary. Wrong-repo evidence does not guarantee a false approval on every run, but permits one when the other repo has a matching issue and sufficient matching evidence; fail-closed outcomes on other runs do not remove the defect. Thread repo and per-repo config through the whole coordinator read path, with a second-repo test, or explicitly restrict dispatch until that exists. V3's additional contract observation at `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/core/WORKER-CONTRACT.md:242` is real; retain the upstream ban while making legitimate per-repo targeting consistent.

### C-002 — absent Pipeline versus unreadable time

**TRUE as a plan ambiguity, not a proven implemented outage — Blocking (Decision). Confidence: 0.97.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:61` represents absent Pipeline as Python None and permits optional value times. The same file at `:84,87` requires unreadable times to refuse but never states whether an absent field is unreadable, while `:128,140` requires empty/None Pipeline to be usable and None to launch through the closed gate. There is no current implementation of the added time fields: `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/predicates.py:112-118` has only the existing Status field.

V3/U-002 is right that a literal fail-closed implementation can refuse valid empty-Pipeline issues. I reject the stronger assertion that every implementation necessarily does so. The plan must distinguish absent from malformed values and test an empty Pipeline with a valid older Status time. I qualify V3's suggested "Pipeline cleared after approval passes": absence of a value does not prove absence of a post-approval change. Any exception for clearing must be reconciled with the fresh-approval rule, not silently added by a reviewer.

### C-003 — claim-time event refusal lacks an implementation boundary

**TRUE — Blocking (Decision). Confidence: 0.98.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:173-176` assigns contract/brief edits but additionally requires a test that refuses a claim-time event as plan approval. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_pipeline/approval_record.py:313-359` takes a hash, channel, evidence id and actor; after syntax checks and adoption existence it stores them. It receives neither the worker ask nor evidence of when that event became a plan approval. Therefore adding a syntactically valid hash to claim evidence is not distinguished here. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/core/WORKER-CONTRACT.md:298` is an instruction to the coordinator, not a provenance check in this helper.

This defends V2/U-003 against both cards' omissions. I am not demanding that this low-level persistence helper itself contact GitHub or enforce every coordinator rule. Task 11 must name where the required distinction is enforced and test that boundary with an existing adoption, valid hash, and otherwise valid claim evidence versus genuine plan evidence. A test failing only because the hash is absent proves only the first half of the acceptance check. The named requirement cannot be satisfied by that weaker test.

### C-004 — completion matcher versus required refusals and allowances

**TRUE — Blocking (Decision) for the explicit test contradictions; Medium for incidental over-matches. Confidence: 1.00.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:202` adds five alternatives, all containing `issue-pipeline` or `issue_pipeline`. Its `:207` requires bare `p.complete.run()` to produce the tamper code, although neither token is present. The current matcher examines normalized command text in `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/hooks/scripts/launch-level-guard.sh:427-444`; normalization does not invent either token. This is a literal mismatch, not speculation about an exotic bypass.

V1 and V3 are right that broad alternatives also block harmless commands naming the completion module. V3 is particularly right that the body offers acceptance of the hyphen over-match while `:207` simultaneously requires a `plan-hash` path containing "completed" to pass. V2 is stronger on the unmatched required case, so X-001 is PARTIAL, not FIXED. Preserve the intended ISSUE class, but reconcile these two contradictory tests before claiming Q-1 complete. Best-effort matching permits unenumerated bypasses; it does not excuse failing an explicitly enumerated test. Do not quietly drop that adopted check without recording the change.

### C-005 — lifecycle instructions missing from the Coder handoff

**TRUE — Blocking (Missing). Confidence: 0.98.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/source.md:36` requires package installation, daemon startup and exactly one restored cron entry on every boot. Its `:40` requires checking the coordinator branch, worktree and running session at boot and on every watcher run, creating missing parts and restarting a stopped session. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:356-363` lists cron contents, branch rules, names and launch text, but not that lifecycle or content checks for it.

This is V2/U-004's strongest missing-deliverable finding. I concede that Task 27 names R6 and R9 and its general acceptance asks for their values/text: the requirement is not wholly unmapped. But a reference to the rows is not the exact lifecycle handoff promised here; adding those required instructions changes the handoff's required content. Neither V1's coverage map nor V3's new findings answers this gap. The remedy stays a handoff specification, not implementation in the Coder repo or permission to start a real daemon here.

### C-006 — Task 11 tests levels that do not consume the brief

**TRUE — Blocking (Decision). Confidence: 0.96.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:102` assigns the brief to the None worker and other levels to the launched agent's prompt; `:177` then tests Worktree/Full/Full Submit troubleshoot forms in the brief and omits a None-level case. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_pipeline/templates/worker-brief.txt:1-5,10-14` currently describes a plan-writing worker that stops before implementation and disallows outward actions.

I concede V3's finding, which my card missed. A renderer could mechanically produce unused rows, so this is not proof that Debug at None already edits code before approval. It is proof that the named acceptance checks exercise the wrong execution surface and leave the actual brief consumer underspecified. Put non-None checks on Task 10's launched prompts; explicitly decide and test Debug's None behavior without bypassing the plan-approval boundary. This is Blocking because the required check must change, not simply because another test would be nice.

### C-007 — retry output has no saved Status or Pipeline

**TRUE — Medium. Confidence: 0.98.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/cycle.py:1279-1284,1308-1314` promises an offline store-only report and rebuilds the retry prompt from the issue number. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/record.py:68-88,104-117` stores neither Status, Pipeline nor rendered prompt. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:123,131` requires valid per-Status retries but does not assign a store-schema edit.

V1 and V3 are right; V2 missed this data-flow problem. Task 6 already delegates the stored-field/file interface at `:103`, so this is an incomplete implementation allocation, not proof of an unavoidable contradiction in the required behavior. Save enough validated launch context for a faithful retry and assign its writer and migration/tests; merely producing a syntactically valid default command is not faithful to an unknown launch. Keep Medium unless the design explicitly chooses an incompatible source or behavior.

### C-008 — Task 5 precedes the one-live-item helper

**TRUE as underspecification; not a proven impossible task order — Medium. Confidence: 0.96.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:84` requires value-time evaluation before `project_check`; its `:123` introduces the selection helper two tasks later. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/cycle.py:957-958,1012-1016` reads items before checking them, and `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/predicates.py:262-271` currently performs the one-live-item selection inside `project_check` and returns only a reason.

I concede V1/U-005's useful helper-order observation. However Task 5 can implement its own selection within its assigned files, so no backward dependency is logically forced. Put the shared selection and zero/multiple-item behavior in Task 5 and reuse it in Task 7 to avoid duplicate logic and accidental reason changes. This preserves the named rules rather than choosing a new one.

### C-009 — offline warning cites the runtime account value

**TRUE — Note. Confidence: 0.97.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:149` says "config's own account id" but cites `self.account_id`. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/cycle.py:767-769` assigns that runtime value from the user read, whereas its `:97-107` defines the optional configured `owner_account_id`. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/cli.py:185-198` validates locally and prints the existing information, without that runtime object.

V1 identifies the right mistake; V3 grades it more proportionately. The task already states the intended configured-account comparison, so this is primarily a wrong pointer and an unspecified null-account case, not a missing warn-only decision. Name the configured field and document an honest unknown-account outcome when it is absent; do not add an unplanned network lookup merely to satisfy the bad citation.

### C-010 — same-file enumeration omits pairs

**TRUE about omissions; FALSE that the plan affirmatively permits parallel edits — Note. Confidence: 0.96.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:30` lists only Tasks 11 and 14 for the worker contract, yet `:161` assigns that file to Task 10 too. The design/runbook files appear in Tasks 2 and 10 (`:48,161`), while Tasks 10 and 11 have the same dependencies (`:159,171`). V3 correctly identifies the incomplete enumeration and explicit edges; V2 should not call that enumeration complete.

But the first clause of `:30` already says **all tasks editing the same file run in plan order, never in parallel**. The prose rule applies even to omitted pairs, so V3's assertion of unguarded concurrency is stronger than the text warrants. Complete the list for ease of execution; no new behavioral decision or absent deliverable follows. X-003 is PARTIAL as a checklist correction, not a Blocking dependency failure.

### C-011 — Full Submit monitor actions encounter the API refusal

**TRUE for visible command forms; not proof every script invocation is intercepted — Medium. Confidence: 0.96.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md:22-27` specifies an issue-comment POST. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh:73-82,129-142` uses GraphQL reads, REST reply POSTs and a GraphQL mutation. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/hooks/scripts/launch-level-guard.sh:553-581,798` classifies those visible API forms as GHWRITE and denies that class at Full Submit. The plan still promises monitor 3 at `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:27`.

V3 is right to preserve this residual risk, which V1 explicitly did not check. The ship gate remains closed, and a text-only hook cannot see API calls hidden inside arbitrary scripts, so I do not claim a demonstrated runtime failure of every invocation. Keep the issue in the design/release gate and validate the intended command path before enabling Full Submit. Do not adopt V3's alternative of silently dropping monitoring: that changes the owner's named monitor-3 behavior, whereas documenting this pre-existing integration limit does not.

### C-012 — the goal overstates the prohibition

**TRUE — Note. Confidence: 1.00.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:15` says a launched agent can never write at any level. Its `:24-25` expressly limits the hook to visible commands, exempts the ungoverned claim session and permits its two marked comments. Its `:356` assigns credential separation to the Coder handoff rather than delivering it here.

V3 correctly finds the overclaim, but Medium is unnecessary for correcting a summary to match already-explicit constraints. Narrow the goal to the governed-session policy and its text-check limitation, without revoking the claim session's intended comments. Do not transform this wording repair into a new credential-management feature.

### C-013 — gated candidates consume read budget

**TRUE as a conditional cost risk — Note. Confidence: 0.96.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/cycle.py:941-958` reads markers, events, edits and Project items before the proposed late gate. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/github.py:46-50` caps calls at 35 with 3 reserved. The plan's gate at `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:137` only requires placement before launch, not caching or early filtering.

V1 correctly marks the workload consequence as inferred. However `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/cycle.py:730-736,821-834,1134-1137` orders candidates using considered timestamps and saves those timestamps for skipped candidates. They remain eligible for re-examination but do not necessarily head every subsequent sweep; one delayed candidate is not proof of permanent starvation. A budget/load fixture or a short limitation note is proportionate. The plan already has a bounded-call policy, and no contrary latency or fairness acceptance check has been identified, so this does not meet Blocking.

### C-014 — Project recheck tests and conflicting selection rules

**TRUE — Blocking (Decision) for the selection-rule conflict; Medium for the test omission alone. Confidence: 0.98.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:268,273` permits several Projects when a defaults mapping selects one and requires a generator test for it. The same plan at `:323` calls exactly-one Project the "Task 19 rule", so a config accepted by the generator can be skipped by the loop; `:328` has no zero/multiple-Project acceptance cases. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/source.md:34` requires reporting zero/several Projects before each child.

This defends V2's unique QA-4 observation, but I correct its Medium grade for the conflict itself: choosing whether mapped multi-Project repos can run changes required loop behavior. Either make both stages honor the configured selection with an explicit report, or make both reject multiple Projects; do not let the implementer silently choose between incompatible rules. Add existing-config rechecks for zero and several Projects and prove no child starts on refusal. This needs reconciliation, not an assumed owner grant for either policy.

## 4. Resolve the X- and U-IDs explicitly

| ID | Position and critique | Grade | Confidence |
|---|---|---|---|
| X-001 | Q-1 is **PARTIAL**, supporting V2 over V1/V3. The ISSUE-class repair is present, but the bare alias refusal and the hyphen-pattern allowance conflict remain (C-004). | Blocking (Decision), already counted at C-004 | 1.00 |
| X-002 | Q-6 is **PARTIAL**. I concede V3's correction of V1 and my own card: the adopted proposal explicitly asks for `marker_comments` to ignore a result comment, not only for the marker string to lack the claim substring. | Blocking (Decision) for the omitted named acceptance check; not a claim of a demonstrated marker-reader bug | 0.98 |
| X-003 | Q-10 is **PARTIAL** as an incomplete enumeration. V3's list correction is right, but the universal same-file serial-order rule already covers the omitted pairs; V1/V2 should narrow "FIXED" accordingly (C-010). | Note | 0.96 |
| U-001 | Adopt V3's cross-repo approval-read finding, including a second-repo regression test (C-001). | Blocking (Safety) | 0.99 |
| U-002 | Adopt V3's absent/unreadable distinction, but reject automatic approval preservation after a field is cleared without evidence or a recorded rule (C-002). | Blocking (Decision) | 0.97 |
| U-003 | Retain V2's approval-boundary finding; the missing-hash case cannot stand in for provenance (C-003). | Blocking (Decision) | 0.98 |
| U-004 | Retain V2's missing lifecycle content; naming Coder row numbers is weaker than the promised exact handoff (C-005). | Blocking (Missing) | 0.98 |
| U-005 | Adopt V1's helper allocation fix (C-008) and its grid-maintenance reminder below; neither forces a new product decision. | Medium for helper allocation; Note for grid bookkeeping | 0.97 |

**X-002 evidence.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/remediation/watcher-plan-v3/remediation-proposal.md:201-205` explicitly lists the reader-level test. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:188,191-192` covers per-run/own-login suppression, substring separation and `unchanged_since`, not that reader-level scenario. The underlying projection already uses the claim marker in `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/github.py:60-65`, so I am not asserting an existing functional defect. Add the specifically adopted check; do not alter marker semantics or reopen the per-run-marker decision.

**U-005 grid evidence.** `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/tests/hooks/test_launch_level_guard.py:775-797,843` separately declares `GRID_CLASSES`, `EXPECTED`, and an import-time equality assertion. Adding ISSUE to only the result dictionary would fail collection. The task's broad "expected-result grid" instruction can reasonably include both declarations, so the extra explicit pointer is a Note, not a missing core implementation.

## 5. Shared assumptions A-001 through A-005

### A-001

**QUALIFY** — Some carried line numbers are still right, but they are not a trustworthy blanket assumption. This round directly read the relevant guard, watcher, approval, brief and contract spans; the warning's runtime pointer (C-009) and the "one-second resolution" description are counterexamples to treating every carried citation as correct. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/predicates.py:181-182,205,257` truncates approval-event comparisons in one place but uses raw datetimes in `unchanged_since`. Uninspected ancillary citations are not certified by this report. Confidence: 0.99.

### A-002

**REJECT** — The assumption that the executor itself performs the owner's field changes is explicitly contradicted by `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:73-78`: ask in chat, wait for each owner answer, make only read calls, and stop dependents on a failed observation. This is a deliberately attended gate, not an undisclosed unattended capability. Whether the executor's interrupt handling needs adjustment should be checked against that executor before alleging a defect; I did not inspect or run that executor here. Confidence: 0.99.

### A-003

**QUALIFY** — The text-only limitation is real, but "a script or other client bypasses any pattern" is too absolute: commands that visibly mention protected tokens or API URLs can still be refused. The supported claim is that a matcher cannot reliably inspect hidden behavior inside an arbitrary wrapper or non-gh client. The plan states that limitation and the separate credential boundary at `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:24`; the guard also acknowledges text limitations at `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/hooks/scripts/launch-level-guard.sh:774-775`. Neither this qualification nor best-effort status erases C-004's explicit must-refuse requirement. Confidence: 0.99.

### A-004

**ACCEPT** — For the watcher-started top-level None claim session under review, this is the intended and supported boundary, not a promise that running a None command removes an existing session's governance. `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:25` states it; `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/skills/sc-issue-protocol/refs/claim.md:118,144` skips governed launch for None; `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/hooks/scripts/launch-level-guard.sh:254-272,387-391` bases tool governance on the stored session record and allows unbound calls. I did not run a live session or prove the absence of every possible inherited record. Confidence: 0.96.

### A-005

**REJECT** — "Every acceptance check uses fakes only" is false: `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md:22,61,73,356` makes live read-only exceptions for schema, field observations and cron-like authentication. More importantly, fake runners can catch C-001 by asserting that every coordinator read names the second repo; a live cross-repo test is unnecessary. Accept only the narrower warning: the currently named tests do not explicitly require that coordinator-path case, so merely running existing tests would not prove isolation. Confidence: 0.99.

## 6. Round 1 conclusion and scope

Variant 2's central QA findings survive; its grading column and its unconditional Q-6/Q-10 closure claims do not. I also adopt V3's C-001, C-002 and C-006, V1/V3's C-007, and V1's C-008, while narrowing speculative workload claims and over-strong concurrency claims. Confidence in this combined position: 0.97.

The C-list contains **seven Blocking positions** (C-001 through C-006, plus C-014), **three Medium positions** (C-007, C-008, C-011), and **four Notes** (C-009, C-010, C-012, C-013), with the explicit sub-claim qualifications above. X-002 adds one separately named required-check omission; the other X/U entries are cross-references, not new findings to double-count.

Recommended next action for the merge: retain the seven C-list blockers and the X-002 acceptance-check correction, fix their plan wording/work allocation, and preserve the closed ship gate. The review does not authorize a live watcher, credential change, GitHub write, daemon start or owner-field mutation.

Checked: the requested plan, driving requirements, all three cards, the diff analysis, the adopted remediation's relevant requirements, and the cited local implementation/test spans. Not checked or executed: tests, live GitHub/schema/timestamps, cron authentication, Orca session behavior, or every ancillary carried line reference. No production files, plan files, external records, commits or staging were changed; only this requested debate report was created and appended.
