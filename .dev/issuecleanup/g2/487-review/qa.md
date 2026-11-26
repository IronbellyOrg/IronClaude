VERDICT: FAIL
# Independent evidence review: issue 487

Template: `.dev/issuecleanup/g2/468/report-template.md`, Review skeleton; first-line verdict follows this task's explicit format.

## Verdict
FAIL: three blocking defects change the next build plan or its dependency assessment: the wrong process adapter is recommended, the prerequisite schema/policy phase is omitted, and the explicit framework-dependent portion of issue #489 is missed. The review work itself succeeded. The narrower conclusion that the integrated framework is still relevant and unimplemented in this checkout is supported; this is not a recommendation to close the issue or start implementation.

## Scope checked
Independent review on 2026-11-24, in the assigned shared worktree at HEAD `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, matching the locally stored `origin/master`. Scope was the two submitted reports, the live issue and both comments, the specification's process-layer decision and phased acceptance plan, current eval source, relevant follow-ups, PR provenance, local refs/history, and the completeness/support of the verdict, complexity, size, priority and dependencies. No reviewed source or findings file was edited.

| Submitted claim | Independent result and evidence |
|---|---|
| Issue remains open, no labels, specification exists and was merged | Confirmed from live issue #487 and PR #500. PR #500 merged 2026-11-11 as `ec259f1b718ccdb9f08bba0237bfa47b2b7601a2`, adding the 641-line specification. Local path history attributes the spec to that commit. |
| Original commit not in HEAD, source branch tip | Confirmed: `git merge-base --is-ancestor 2813b945 HEAD` returned 1; `git rev-parse origin/346Claude-ab-experiment-artifacts` returned `0150d187f447352b441a2d475b13402205ca74aa`. This does not prove that branch has no other merged commits. |
| Null executor remains the default | Confirmed at `src/superclaude/cli/eval/commands.py:1357-1405`: spawn/inject return None, observe returns exit 0, and the factory constructs this executor. No model was launched. |
| Concurrency clamp remains 15, default 8 | Confirmed at `src/superclaude/cli/eval/orchestrator.py:140-142,194-198`. The report's line 140 reference points to the group of constants, rather than the precise maximum at 142: form-only note. |
| Exit-code values remain 0,1,2,3 | Confirmed at `src/superclaude/cli/eval/exit_codes.py:21-24`. This is a local contract, not proof that a Click subgroup must reuse the executor or orchestration layer. |
| Strict eval-id pattern | Confirmed at `src/superclaude/cli/eval/artifact_layout.py:108` and loader import at `loader.py:39-45`; the separate permissive path-safety regex at `artifact_layout.py:96-105` is not the manifest contract. |
| Home isolation and runner exist | Confirmed at `src/superclaude/cli/eval/isolation.py:363-402` and `runner.py:712-783`: real isolation record, JSONL lifecycle and timeout handling. |
| RetryOncePolicy is not HTTP 429 backoff | Confirmed at `src/superclaude/cli/eval/retry.py:93-142`: tagged MCP-flaky eligibility and outcome-based retry; no HTTP status/backoff mechanism in that policy. |
| Adapter is real but not wired into default executor | Confirmed existence at `src/superclaude/cli/eval/claude_process.py:107,317-367`; graph dependents locate package exports/tests, and the actual default factory above still returns the null executor. Recommended reuse is nevertheless wrong, as Blocking 1 explains. |
| No lab implementation in this checkout | Supported by the tracked-tree check for `src/superclaude/cli/lab`, source text search for the lab command/framework, and indexed file inventory. This is narrower than proving that no implementation exists on any branch. |
| 39 files: 24 Python, 15 YAML; largest symbol counts | Confirmed as the codegraph indexed inventory, not as every physical file: `commands.py` 93, `runner.py` 65, `expect.py` 42, `models.py` 43, `loader.py` 40. Markdown, JSON schemas and caches are outside that indexed count. |
| No recent eval changes | Incorrect: local `git log origin/master --since=2026-11-17 --name-status -- src/superclaude/cli/eval src/superclaude/cli/lab` reports three commits, detailed under notes. |
| Complex / XL | Reasonable reviewer estimates from nine issue scope areas and phases P0-P7, not independently measured project fields. The 35-40% experiment-tree port and 25-30% new-code figures are correctly quoted, but expressly rough judgments at `SPEC-AND-CONTEXT.md:598-606`, not workload measurements. |
| P2 and backlog decision | P2 is a reviewer recommendation, not a verified owner-set priority. The owner gate matches issue #487's latest status comment; the related hold wording is now read, but whether it applies to this framework remains UNVERIFIED. |
| Still relevant, not complete | Supported for the missing integrated lab framework and unmet end-to-end acceptance. Not a license to claim that none of its reusable code exists or that no branch work is in progress. |
| No downstream issue waiting | Incorrect: #489's original prerequisites and owner configuration decisions establish a framework-dependent portion (Blocking 3). |
| Required issue-cleanup deliverables | Findings and analyze report both exist and include state, evidence, next steps, estimates, dependencies and related work. Their substantive defects, rather than missing files, cause this FAIL. |

## Blocking findings
### Blocking 1: The proposed reuse contradicts the specification's process-layer decision

- Claim: `.dev/issuecleanup/g2/487/findings.md:26-27` says Part E selects a sibling importing `ClaudeProcessAdapter` and the runner lifecycle. `.dev/issuecleanup/g2/487/analyze/analyze-report.md:35` also recommends that adapter as an import candidate.
- Evidence: `.dev/designs/spec-task-eval-framework/SPEC-AND-CONTEXT.md:621-624` instead selects `ClaudeProcess(cwd=...)` directly, explicitly rejecting `ClaudeProcessAdapter` for thread safety and requiring extraction of the companion's process hardening. Current code confirms the reason: `src/superclaude/cli/eval/claude_process.py:352-365` changes and restores the entire parent process's working directory during spawn, and lines 335-342 explicitly warn that concurrent threads can race.
- Grade: Blocking (Decision). The named next consumer is the build plan requested in findings line 34. Following this reuse recommendation selects the adapter the governing specification rejects; under parallel launches it can also give a child the wrong working directory.
- Required correction: Report the Part E decision accurately, including direct `ClaudeProcess` use and extracted hardening, and remove the adapter from the framework's recommended process components.

### Blocking 2: The next-step instruction drops the prerequisite phase

- Claim: `.dev/issuecleanup/g2/487/findings.md:34` directs planning to start at P1 (the engine).
- Evidence: `.dev/designs/spec-task-eval-framework/SPEC-AND-CONTEXT.md:394-399` defines P0 first: task/arm/slots/experiment schemas, policy validation, and frozen assets including the task and defect ledger. Its exit checks are validation and the forbidden-model test. The engine follows in P1.
- Grade: Blocking (Missing and Decision). This is the direct instruction for the next build planner and omits the prerequisite input and policy contracts. Correcting it changes the starting phase and required acceptance checks.
- Required correction: Start planning at P0, retaining the later phases and acceptance checks, subject to the owner gate already stated in the findings.

### Blocking 3: The claimed absence of downstream dependencies is contradicted by the named follow-up

- Claim: `.dev/issuecleanup/g2/487/findings.md:51` says no open issue cites #487 as something it is waiting on; line 56 leaves the #489 relationship unverified.
- Evidence: https://github.com/IronbellyOrg/IronClaude/issues/489 is OPEN. Its original body says, "Do this after both of these have landed: (1) the experiment/framework work from #346 and #487 is merged, and (2) #488 is deployed." Its scope includes the framework policy and panel switch; its owner-decision comment requires the framework to expose the tier list and optional Tier 4 configuration, with a membership/lane test (https://github.com/IronbellyOrg/IronClaude/issues/489#issuecomment-6774682023). The specification itself records these requirements at `.dev/designs/spec-task-eval-framework/SPEC-AND-CONTEXT.md:636-640`.
- Grade: Blocking (Decision). Correcting this changes the explicit dependency assessment used by the findings' next-step/prioritization handoff: at least #489's framework-policy portion needs #487. This is an implementation dependency, not a claim about formal GitHub blocked-by links, and does not mean every #489 task must wait.
- Required correction: Record the partial dependency and the settled panel configuration requirements; do not claim that no issue is waiting on this framework.

## Follow-up candidates and notes
### Medium: The historical-change claim is false, but does not by itself overturn the integrated-framework verdict

Findings line 17 says no commit since the 2026-11-17 review touched eval or lab. The exact local history query returns `b637fd0d8` (#616, modifies `orchestrator.py`), `af5fb69eb` (#632, modifies `isolation.py` and `reporter.py`, deletes the tasklist deterministic-shape suite), and `a3edd84db` (#656, modifies the suites README and deletes `workflow_vs_task_builder.yaml`). Consequence: the claimed no-change verification cannot support continuity from the old review. The core runtime constraints were independently re-read and still hold, so this historical error alone does not require changing the still-relevant recommendation. Correct the evidence statement; it does not add a fourth blocking finding.

### Notes and bounded uncertainty

- Findings lines 22/29/64 and analyze lines 26/36 overstate absence. No lab package at this checkout and no PR search match are not proof that no unlinked branch or partial implementation exists. Local branches include experiment-related work and a retained experiment-artifacts ref. Global absence of in-progress work is UNVERIFIED; report the searched scope instead. The integrated-framework verdict remains supported independently.
- The analyze recommendation that a subgroup necessarily inherits every runtime restriction is too broad: the cited restrictions belong to particular runtime/schema components, not merely the command's position in the menu. The sibling package remains the recorded Part E decision; no new architectural choice is needed in this review.
- The analyze report labels schema closure UNVERIFIED. Direct inspection now confirms manifest-root closure at `src/superclaude/cli/eval/suites/suite.schema.json:16` and summary concurrency maximum at `schemas/summary.schema.json:49-53`; not every schema object is closed (summary-root `additionalProperties` is true at line 18, manifest `defaults` permits additional fields at line 34). Keep any closure claim scoped to the actual object.
- The hold wording is real: #560 and #561 contain the 2026-11-16 instruction that nothing running headless Claude is to be worked on; #560-#562 also carry 2026-11-18 comments parking that eval harness until it is used again. Those are source records, not authorization from this reviewer. Applicability to #487 is still UNVERIFIED; preserving the owner gate is correct and no implementation was started.
- Live title/state checks confirm #346 CLOSED; #489, #520, #531, #549, #550, #552, #290, #429, #560, #561 and #562 OPEN. Cross-reference dates and the detailed relationships beyond #489/#560-#562 remain UNVERIFIED, as the findings already acknowledge.
- Complex, XL and P2 are defensible proposals, not measured effort, a scheduling grant, or verified GitHub project fields. The nine areas and rough porting percentages support the broad scale; they do not establish a precise duration. No defect of form alone contributes to FAIL.

## Verification limits and negative evidence
- Read-only GitHub access used only `gh issue view` and `gh pr list/view`, always with `--repo IronbellyOrg/IronClaude`. Issue #487 and both comments were read in full. No posts, labels, links, closures, commits, staging, model calls, tests, installs, `uv`, `pip`, or environment creation were performed.
- No fetch was authorized or run. All branch and history claims here are about the local refs observed during this review, not a refreshed remote branch inventory. Ancestry exit 1 is negative evidence of non-ancestry, not a tooling failure.
- PR searches for `487`, the quoted lab command, and `Spec-Task` found no relevant implementation PR. The last search returned unrelated merged PR #76, which was not treated as evidence for this framework. PR #500 was read directly to confirm the spec merge. These searches cannot exclude unlinked implementation work.
- The exact issue open timestamp, all GitHub event-timeline cross-reference dates, all other branches' contents, the six-module exit-code consumer count, and the isolation/runner/orchestrator graph-dependent totals (28/9/9) are UNVERIFIED here. Indexed file and symbol counts were checked separately. No numerical claim in this unverified set is used as an acceptance check or as a reason for FAIL.
- Tool recovery: one report Edit was blocked because the initial Write did not satisfy the freshness hook; a tracked Read preceded the successful Edit. A later Glob and Grep failed with `EACCES: permission denied, posix_spawn 'rg'`; their specific missing-lab lookup was recovered with the read-only tracked Git tree inventory and codegraph file inventory. Earlier source text search had already succeeded. The failed searches are not treated as proof of absence.
- The codegraph readiness check reported zero added/modified/removed files; indexed source was used for locations/counts and direct Reads established the cited implementation. No index initialization or files outside the assigned report directory were created by this review.
- Only this report, its return contract and its short handoff are worker-owned outputs. The reviewed findings and analyze report remain unchanged. This reviewer does not repair their blocking findings or authorize the next build.
