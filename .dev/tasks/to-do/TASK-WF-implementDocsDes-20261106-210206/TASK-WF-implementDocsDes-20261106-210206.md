---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-implementDocsDes-20261106-210206
version: "1"
priority: Medium
created_date: "2026-11-06"
---

# Launch-level guard with an actor-isolation feasibility gate

Source: ./source.md
Goal: Implement the current launch-level design only after observed evidence proves governed agent pushes can be selected without restricting human pushes in the same worktree. If the prerequisite fails, preserve reproducible evidence and stop before production enforcement changes.

## Constraints

- The authoritative design is docs/designs/sc-issue-launch-level-hook.md, including section 19 and owner decisions O-13, O-21 and O-22. The historical merged requirements, corpus and old review verdicts provide traceability, not permission to override the current design. Read the panel report at .dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md.
- Human pushes in the same worktree remain unrestricted by launch policy. A worktree marker, environment label, PID alone or an unreadable ancestry chain is not sufficient actor authority. No silently invented launcher/harness contract, root service, managed-policy deployment, server protection or isolation weakening.
- Task 1 is a blocking prerequisite for every later task. A documented unsupported lifecycle is not a compliant gate result. If the candidate cannot meet the required lifecycle distinctions, report the exact missing interface and halt implementation; do not proceed on synthetic payloads or an accepted historical residual.
- Use UV for Python operations. Use disposable local bare repositories for Git experiments; never push protected branches on the real origin. Read-only upstream documentation is allowed except the forbidden SuperClaude upstream, with which no interaction is allowed.
- Preserve the existing dirty design and all pre-existing brainstorm artifacts. No commit, push, issue comment or real global installation is authorized by this plan. Do not activate production enforcement in this live session.
- Source primitives belong under src/superclaude/. Generated .claude/ mirrors are not staged. Stage .dev/tasks, including package evidence, throughout execution. Source changes may remain uncommitted.
- Evidence paths below are package-relative and resolve beside this plan, including after executor archiving. Existing task packages and unrelated source files are not overwritten. Do not change this plan once implementation starts.
- Do not repeat earlier adversarial/spec-panel loops. Run only the executor's prescribed task compliance checks and final review. All claims of runtime proof require observed evidence; no fabricated payload logs.

## Phase 1: Establish a supportable actor identity boundary

## Task 1: Build and execute the bounded process-context feasibility probe

Read design sections 3, 6-8, 14 and 19.1, the panel report's B-CTX finding, and the actual ccsession/ccsession-orca process-ownership implementation located from repository search. Write a log-only probe and its reproducible commands under ./artifacts/actor-context-probe.sh and ./artifacts/actor-context-report.md. The probe records kernel process parentage, process start identity and boot identity without printing credentials or environment secrets. It must not install a production hook, mutate global Claude settings or configure a real repository's hooks. Use temporary local fixtures and actual supported Claude/Orca process observations where available; record unavailable observations as unavailable, never as passed. Child/background lifetime cases may use bounded controlled processes, but simulated harness behavior cannot replace real session reset/resume proof.

Acceptance criteria:
- ./artifacts/actor-context-report.md enumerates main Claude, subagent and nested tool calls, background Bash/Monitor descendants, same-worktree human terminal, ordinary Claude session, detached/reparented jobs, process exit and PID reuse, resume into a new process, /clear/fork, and release with a live old background child. Each has observed evidence or an explicit unsupported result with the missing interface named.
- The report tests the decisive case: a reused Claude process starts an ordinary session while an old governed background child remains alive. It demonstrates separate identities for both without relying on worktree membership or an agent-editable label. Document the bounded ancestry limit and its exhaustion behavior from evidence.
- PID reuse/boot change cannot inherit authority; release invalidates only the intended session; human pushes and ordinary sessions in the same worktree are never selected merely because another session is governed.
- The report contains a binary B-CTX result. PASS requires observed support for every required actor/lifecycle distinction and no new unauthorized launcher/harness integration. Otherwise record FAIL/BLOCKED, the exact missing binding/reset/child-lifetime contract and the smallest required integration, then halt before Task 2. Producing a report alone does not make the task compliant or authorize a gate waiver.
- Retain runnable probe/evidence on disk, capture exit results and negative evidence, and keep sensitive process arguments redacted. No production script/registration/install changes are present from this task.

## Phase 2: Implement session policy and text checks

## Task 2: Implement hook event dispatch, binding, approval and failure behavior

Depends on: Task 1

Only after an observed B-CTX PASS, implement the proposed src/superclaude/hooks/scripts/launch-level-guard.sh and tests/hooks/test_launch_level_guard.py for design FR-L-01 through FR-L-23, FR-L-51 through FR-L-59 and sections 3, 6-8. Use the existing block-bare-python hook and test subprocess pattern. Integrate the proven process-context identity contract exactly as observed, not an invented approximation. Store fixtures under tests/hooks/fixtures/launch_level/ only for real redacted event captures. Record command results under ./artifacts/session-policy-tests.log.

Acceptance criteria:
- Valid pending records bind once without replacing existing sessions; concurrency, file kinds, unknown levels, malformed JSON/id/event fields and exact event dispatch follow the current design. Remove the historical unsafe raw JSON early-allow prefilter rather than reintroducing it.
- Ordinary sessions pass unchanged. Corrupt/missing identity never silently proves an ordinary actor, and any unsupported case follows the gate's documented stop behavior without blocking unrelated humans.
- Whole-prompt approval and exact supported implementation command names unlock implementation only; they never unlock submission. Subagent identity, scheduling/background prompt caveats and release/resume semantics have runnable cases tied to captured evidence.
- Every block has a defined plain-language diagnostic; tests distinguish script errors and hook timeout limitations from intentional fail-closed decisions. UV-run affected tests pass with captured output.

## Task 3: Implement the complete tool classifier and level decision table

Depends on: Task 2

Extend src/superclaude/hooks/scripts/launch-level-guard.sh and tests/hooks/test_launch_level_guard.py using design sections 4-5, 9-10, 15-18: FR-L-20 through FR-L-50 and FR-L-64 through FR-L-66. Import historical attack/benign/over-block corpus expectations only where the current design retains them; document changed expectations in ./artifacts/classifier-corpus-map.md. Keep the broad am rule and O-13 skills. No general shell parser or new dependency. Store results in ./artifacts/classifier-tests.log.

Acceptance criteria:
- An independent policy oracle covers worktree, approved worktree, full and full-submit for every named action class. All actual Skill aliases including protocol spellings and O-13 additions are tested.
- Normalization, canonical push and gh API forms, git UNKNOWN/plumbing exceptions, MCP names, Edit/Write/NotebookEdit paths, reinstall/settings tamper, Monitor, scheduling, Workflow, SendMessage and launch/terminal escape routes follow the current specification with named regression cases.
- Exact protected-destination policy and explicit residual/bypass cases are not confused. Documented false positives remain tested, with message/body-file workarounds and counters for am-only interruptions.
- All eighteen block messages and state/text notes are defined without unresolved placeholders; tests cover message precedence and internal failure diagnostics. Command-size, stale-store and speed limits are measured rather than asserted.
- UV-run affected tests pass; raw and summary evidence, copied corpus provenance and current-spec expectation differences are retained in the package.

## Phase 3: Add the structural Git layer without restricting humans

## Task 4: Implement owned structural pre-push installation, actor selection and release

Depends on: Task 3

Implement the separate L2 artifact required by design section 19.2-19.4, using the proposed src/superclaude/hooks/scripts/launch-level-pre-push.sh as its distributable source and tests/hooks/test_launch_level_pre_push.py for real-Git fixtures. This source basename is a plan-local delivery choice for the separately required L2 artifact, not an additional mechanism. Reuse the exact actor selector proved in Task 1. Preserve foreign hooks and effective hooksPath configuration. Exercise installation only in disposable fixture repositories. Record ./artifacts/pre-push-tests.log and ./artifacts/l2-lifecycle.md.

Acceptance criteria:
- Positive governed actor selection uses kernel lifetime identity and the established session contract. Human and ordinary Claude pushes in the same marked worktree pass concurrently without removing markers, changing environment flags or lifting restrictions.
- After selection, inspect every actual pre-push record's third field; exact refs/heads/main and refs/heads/master veto the entire create/update/delete/force/mixed push. Empty input, malformed selected input, SHA-format independence and exact-name near misses follow section 19.3.
- Resolve actual common/private Git paths, publish atomically without replacing foreign/concurrent files, verify exact owned content/executable/version, and preserve every unrelated hook. Unsupported effective lookup or foreign pre-push yields W-L2-ABSENT and refuses an advertised protected launch rather than calling it success.
- No hooksPath migration, worktreeConfig extension, forwarding stub or foreign-hook replay is introduced. Release invalidates intended membership, preserves concurrent sessions/human freedom and leaves the shared owned hook inert when unused; no destructive shared-hook removal on single-session release.
- Real Git tests assert hook invocation and before/after disposable remote refs for mapped source-only refspecs, script/alias pushes, protected-last mixed input, known bypasses, rename/re-add and actor lifecycle. UV-run tests pass. Known --no-verify, direct send-pack, hooksPath overrides and API bypasses remain explicit limitations, not false enforcement guarantees.

## Phase 4: Integrate distribution and prove the supported workflow

## Task 5: Integrate hook distribution and the existing claim launch boundary

Depends on: Task 4

Update src/superclaude/hooks/hooks.json and src/superclaude/cli/install_hooks.py for the Claude hook entry points and required script distribution, retaining existing registrations. Read actual src/superclaude/skills/sc-issue-protocol/refs/claim.md and src/superclaude/commands/issue.md; implement only compatible interface prerequisites IR-1 through IR-7 where the parallel pipeline feature actually exists. If that launch feature is still absent, add the explicit interface contract to those source primitives and report deployment blocked rather than inventing the out-of-scope pipeline or pretending it launches. Add affected installer/registration tests under tests/hooks/test_launch_level_guard.py or the existing installer test file located from source. Run make sync-dev and make verify-sync, never staging generated mirrors. Capture ./artifacts/distribution-tests.log and ./artifacts/claim-interface.md.

Acceptance criteria:
- New registrations retain the existing bare-python/freshness/user hooks; scripts distribute through the current installer source list and generic sync checks without duplicate registration or a Makefile list invented from historical claims. Installed primitives use installed/project lookup paths, never runtime src/superclaude paths.
- IR-1 through IR-7 each have an implemented integration point and test, or a precise absent-dependency entry that prevents a protected claim launch. Existing ordinary/no-pipeline claim behavior remains unchanged. No new pipeline implementation is silently added.
- Pending record and launch marker setup, effective hook/config validation, separate claim launch/session identity, no resume-based re-claim, release instructions and mandatory L2 presence are explicit. A warning is not protection.
- Sync and affected UV-run installer/registration tests pass, and .claude mirrors remain unstaged. Required .dev/tasks evidence is staged.

## Task 6: Complete runtime evidence, operator documentation and bounded rollout behavior

Depends on: Task 5

Update docs/designs/sc-issue-launch-level-hook.md only with actual implemented behavior, evidence links and resolved/current deployment status; preserve historical review findings as historical. Execute the design's OB-H1, OB-H2 and OB-H3 through isolated supported sessions only when the real launch dependency exists; use disposable local bare destinations and safe fixture issues without posting externally. If a required observed step needs unavailable integration/authorization, record the exact blocker in ./artifacts/observed-checks.md and retain deployment blocked. Include test results under ./artifacts/full-verification.log; no separate verification-only task is introduced because this task delivers the operator-facing runtime contract and measured rollout rules.

Acceptance criteria:
- Actual payload/provenance fixtures cover supported main/subagent/nested/background events, whole-prompt approval, repeated claim, process membership and same-worktree unrestricted humans. No fabricated or merely synthetic payload is described as an observed check.
- A full-submit cycle's actual push/gh/commit forms, retries and am-only false positives are recorded, with no real protected-branch writes or GitHub posts. If this cannot be performed safely without unimplemented external integration, it remains explicitly blocked rather than reported passed.
- All source acceptance criteria, FR-L-01 through FR-L-66, current NFRs, IR-1 through IR-7, sections 19.1-19.6, owner decisions and named tests map to implemented behavior, measured evidence or a precise deployment-blocking dependency in ./artifacts/requirements-coverage.md. No requirement silently disappears.
- Existing tests/hooks regressions and affected installer/primitive tests run via UV; shell syntax checks and measured speed results are recorded. Document exact covered routes, client-side bypass limits, timeout limitations and human-isolation guarantees without upgrading partial evidence to full approval.
- No production activation, real remote writes, commit or push has occurred. The executor performs its prescribed whole-package final review and archiving only if every task genuinely passes; missing gates are not accepted implicitly.
