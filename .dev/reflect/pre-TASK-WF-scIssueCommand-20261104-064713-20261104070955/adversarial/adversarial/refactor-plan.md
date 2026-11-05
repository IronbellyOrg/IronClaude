# Refactoring Plan: Merge into Base (Variant 3)

## Overview
- Base: Variant 3 (opus:refactorer), reviewer-3-card.yaml (copy at variant-3-original.md)
- Incorporating strengths from: Variant 1 (reviewer-1, sonnet:analyzer), Variant 2 (reviewer-2, haiku->glm-5.3:qa), the blind calibrations (debate evidence), and the Round 2.5 invariant probe
- Target artifact: `<OUT>/merged-verdict.yaml`, where OUT = `/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command/.dev/reflect/pre-TASK-WF-scIssueCommand-20261104-064713-20261104070955/adversarial`. This is one merged reviewer verdict, in YAML.
- Planned changes: 22
- Risk level: Medium overall (Change 1 restructures the base card into the merged schema; the rest are additive or modify single entries)

## Citation rules for the merge
- Path prefixes in `evidence`: `plan:N` = `.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md` line N; `source.md:N` = `.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md` line N; other paths are relative to the repo root `/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command`. State this legend in a top-level `citation_legend` key.
- Use ONLY the citations listed in this plan. Each one was re-Read during this pipeline by the orchestrator or an advocate (see "Citation provenance" at the end). Do not add, widen or renumber citations.
- Severity rule (caller's): blocking only for wrong behaviour, a false claim, a missing required deliverable, or a security/data-loss risk. Everything else is minor.

## Planned Changes

### Change 1: Restructure the base card into the merged-verdict schema (base restructure)
- **Source**: Base (Variant 3) top-level keys `reviewer`, `persona`, `model_class`, `verdict`, `findings`, `self_reported_confidence`, `self_audit`
- **Target**: `merged-verdict.yaml` top-level keys, in this order: `merge_method: adversarial`, `verdict: FAIL`, `convergence_score: 1.0`, `convergence_status: BLOCKED_BY_INVARIANTS`, `base_variant: "variant-3 (reviewer-3, opus:refactorer)"`, `source_cards: [reviewer-1, reviewer-2, reviewer-3]`, `citation_legend`, `findings`, `rejected_findings`, `unresolved: []`, `unaddressed_invariants: [INV-001, INV-002, INV-003]`, `severity_rule`. Drop `self_reported_confidence` and `self_audit`; they are per-card fields with no merged meaning.
- **Rationale**: The caller's required schema. FAIL because blocking findings F-01 and F-02 survive (debate-transcript.md, Scoring Matrix X-001, 98%).
- **Integration approach**: restructure
- **Risk**: Medium (restructures)
- **Each finding entry has keys**: `id`, `severity`, `category`, `claim`, `evidence` (list of strings), `recommendation`, `source_cards` (list), `debate_ruling`.

### Change 2: F-01 (blocking): Task 16 gated behind smoke tasks whose ACs require "blocked" (base S-1, modified)
- **Source**: Base S-1, with V1 A-2, invariant probe INV-001/INV-002, and V3's Round 2 Branch A evidence
- **Target**: `findings[0]`, id `F-01`, severity `blocking`, category `ordering`
- **claim**: "Task 16, which is the only task running the full `uv run pytest`, `make lint` and the final `git add .dev/tasks`, depends on Tasks 14 and 15. Their acceptance criteria require the task to be 'reported as blocked rather than passed' when the tier is not served or no ClickUp token is available. Under /sc:implement that AC cannot be satisfied as written. If the reviewer marks it met, a truthful E-TIER-UNAVAILABLE or 'not run' row passes as compliant and the task is recorded complete, which is a silent pass. If the reviewer marks it unmet, the task goes through the fix pass and the retry ladder on an environment fact, then halts with E-HALT-QA. Task 16 then runs only after the user confirms a Ruling. This is wrong behaviour."
- **evidence**: `plan:209`, `plan:213`, `plan:223`, `plan:228`, `plan:230-236`, `src/superclaude/skills/sc-implement-protocol/SKILL.md:135`, `src/superclaude/skills/sc-implement-protocol/refs/ledger.md:60`, `src/superclaude/skills/sc-implement-protocol/refs/ledger.md:155`, `src/superclaude/skills/sc-implement-protocol/refs/qa.md:83-87`, `src/superclaude/skills/sc-implement-protocol/refs/qa.md:245-248`, `source.md:400`
- **recommendation**: "(1) Make the full-suite/lint/sync/staging task depend on Task 13 only and run it before the two smoke checks. (2) Rewrite the ACs at plan:213 and plan:223 as pure evidence ACs: the artifact truthfully records served, E-TIER-UNAVAILABLE or 'not run' with the reason. Drop 'reported as blocked' from both, and state in the Goal (plan:15) that the smoke checks may end pending. (3) After any fixture or script edit in Task 15 (plan:219, plan:224), re-run `make sync-dev`, `make verify-sync`, `make lint` and `uv run pytest tests/skills` (INV-001). (4) End each smoke task with `git add .dev/tasks`, so their artifacts are staged (plan:23; src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:36) (INV-001)."
- **source_cards**: `[reviewer-1, reviewer-3]` (reviewer-1 A-2, reviewer-3 S-1)
- **debate_ruling**: "C-001: blocking, unanimous after Round 1 (V2 conceded); winner V3, V1 co-winner, 98%. Invariant probe INV-001 and INV-002 (HIGH, UNADDRESSED in the debate) showed that reordering alone is insufficient. Recommendation parts (2) to (4) come from the probe. Calibration's downgrade of A-2 to minor was rejected in debate: the Ruling path needs explicit user confirmation (qa.md:245-248)."
- **Risk**: Medium (modifies base entry)

### Change 3: F-02 (blocking): Task 15 handles the ClickUp token in-session (new, from calibration + debate)
- **Source**: reviewer-3 calibration `missed_by_card`; debate point A-001; invariant probe INV-003, INV-004
- **Target**: `findings[1]`, id `F-02`, severity `blocking`, category `security`
- **claim**: "Task 15 tells the executor to ask the user for CLICKUP_API_TOKEN and run the script with it set in the environment. A token typed into the conversation, or inlined in a Bash command, is persisted in the session record. That breaks the plan's own 'never write the token to disk' and the spec's 'never printed, logged or written to disk'. The live shape comparison has no defined method, so it invites raw authenticated calls whose responses, including personal GET /user data, can land in the transcript or in committed fixtures."
- **evidence**: `plan:219`, `plan:222`, `source.md:296`, `src/superclaude/skills/sc-implement-protocol/refs/qa.md:51`, `plan:42`, `source.md:302-310`
- **recommendation**: "(1) The user exports CLICKUP_API_TOKEN and CLICKUP_WORKSPACE_ID in their own shell before starting the session that runs Task 15. The executor never asks for the value, never echoes or prints it, and never inlines it in a command (no echo, env, printenv or set -x on it). (2) Because the token may now be exported, isolate the other paths (INV-003). Task 2's no-token check (plan:49) runs as `env -u CLICKUP_API_TOKEN -u CLICKUP_WORKSPACE_ID uv run --no-project python ...`. tests/skills/test_clickup_claim.py clears both variables with monkeypatch.delenv (plan:44). Without that, an exported token makes the Task 2 check do live GET /user, page through the workspace and PUT an assignment on a task linking #302 (source.md:303-309), which is outside the two scheduled live checks (plan:24-25). (3) Define the shape comparison as key paths only, and never copy live values into fixtures (INV-004)."
- **source_cards**: `[reviewer-3-calibration]`
- **debate_ruling**: "A-001: all three cards missed it; all three advocates REJECTED the shared assumption that the token handling is safe; blocking (security), unanimous, 95%. Invariant probe INV-003 (HIGH) and INV-004 (MEDIUM) supplied recommendation parts (2) and (3)."
- **Risk**: Low (additive)

### Change 4: F-03 (minor): Section 20 acceptance criteria never run or recorded pending (from V1 A-1 + V2 Q-3, narrowed)
- **Target**: `findings[2]`, id `F-03`, severity `minor`, category `missing-test`
- **claim**: "No task runs section 20 ACs 1, 2, 3, 4 or 6, and none records them as pending. ACs 3 and 4 stop before any GitHub or ClickUp write, so plan:25's limit on live posting does not excuse them. This is unrecorded verification, not a missing deliverable. The deliverables are the section 15/16 files, which all map to tasks, and the plan's Goal claims no AC verification."
- **evidence**: `source.md:465-472`, `source.md:143`, `source.md:155-156`, `source.md:388-398`, `plan:15`, `plan:25`, `plan:226-236`
- **recommendation**: "Add `./artifacts/t-acceptance.md`, listing section 20 ACs 1-8 each as run (with evidence) or pending live verification with the exact command. Place any AC 3 or AC 4 run after the suite task, next to the smoke checks. AC 3 needs the Wave 1 T3 spawn (source.md:147), so it shares Task 14's tier dependency. Amend plan:25 to allow these runs, and ask the user before any run against a real issue, because a faulty Wave 2 guard reaches `gh issue edit --add-assignee` (source.md:162) (INV-005)."
- **source_cards**: `[reviewer-1, reviewer-2]` (A-1, Q-3)
- **debate_ruling**: "C-002 and X-002: minor, unanimous after Round 2 (V1 and V3 conceded); V2's classification won, 90%. A-1's 'items 1-6, missing required deliverable' was rejected as overstated: AC 5 is covered by Task 2 and Task 15. The calibration's upgrade of Q-3 to blocking was rejected: no missing deliverable, false claim, wrong behaviour or security risk."
- **Risk**: Low (additive)

### Change 5: F-04 (minor): No static check that every gh call carries --repo <R> (debate A-002; V1 A-1 recommendation; reviewer-2 calibration)
- **Target**: `findings[3]`, id `F-04`, severity `minor`, category `missing-test`
- **claim**: "The --repo <R> invariant on every gh issue/pr/label call, and the repos/<R>/ form of every gh api path, is stated only in prose (Constraints, Task 5, Task 6). No test checks the SKILL.md, ref or worker-body lines, although AC 4 requires that no gh call is made without --repo. Without --repo, gh on a fork targets the upstream parent. Section 16 does not require this test."
- **evidence**: `source.md:319`, `source.md:470`, `plan:22`, `plan:91`, `plan:109`, `plan:121`, `source.md:390-398`
- **recommendation**: "Add to tests/skills/test_issue_protocol.py a scan asserting that every `gh issue|pr|label` line in SKILL.md, refs/*.md and the three worker bodies carries `--repo`, and that no `{owner}/{repo}` placeholder appears."
- **source_cards**: `[reviewer-1, reviewer-2-calibration]`
- **debate_ruling**: "A-002: QUALIFY, minor, unanimous after V1 conceded in Round 2; 85%."
- **Risk**: Low (additive)

### Change 6: F-05 (minor): git-fetch-origin rule not bound into Tasks 3/5, and read-only-git wording conflicts with it (V1 A-3 + V2 Q-2 + A-004)
- **Target**: `findings[4]`, id `F-05`, severity `minor`, category `missing-requirement`
- **claim**: "The origin-only fetch rule appears only in the plan Constraints. Task 5 copies 'the gh commands exactly as written', which does not cover the git command in Wave 1. Task 3 tells workers to make 'read-only gh and git calls only' and to write 'only under .dev/issues/', yet Wave 1 requires the worker to run git fetch origin, which updates remote-tracking refs. A literal worker could skip the fetch and report stale commits."
- **evidence**: `source.md:149`, `source.md:320`, `source.md:321`, `plan:22`, `plan:55`, `plan:91`
- **recommendation**: "Task 5: the claim.md Wave 1 bullet includes `git fetch origin` (origin only) and the `git log --since` command. Task 3: the worker body says its only git write is `git fetch origin`, and the test in tests/skills/test_issue_worker_agents.py asserts that sentence."
- **source_cards**: `[reviewer-1, reviewer-2]` (A-3, Q-2)
- **debate_ruling**: "C-003 minor, unanimous, winner V1, 85%. A-004 (shared assumption that 'read-only git' is compatible with the fetch): REJECT by V2 and V3, QUALIFY by V1; minor, 80%."
- **Risk**: Low

### Change 7: F-06 (minor): Task 11 'git diff --stat shows only this file' is not observable (base S-3, kept; V1 A-4 part)
- **Target**: `findings[5]`, id `F-06`, severity `minor`, category `non-observable-ac`
- **claim**: "Task 11's criterion that git diff --stat shows only the developer guide cannot hold literally after Tasks 9 and 10 have left other tracked files modified. The executor's own per-task diff is against its Q0 snapshot, so only the AC wording is wrong."
- **evidence**: `plan:178`, `plan:145`, `plan:159`, `src/superclaude/skills/sc-implement-protocol/SKILL.md:123`
- **recommendation**: keep base S-3 recommendation verbatim.
- **source_cards**: `[reviewer-3, reviewer-1]` (S-3, A-4)
- **debate_ruling**: "C-004: minor, unanimous, winner V3, 90%; S-3's overstatement narrowed per SKILL.md:123."
- **Risk**: Low (modifies base)

### Change 8: F-07 (minor): Task 10 omits the ASCII and live-reference rules (base S-6, kept; V1 A-4 part)
- **Target**: `findings[6]`, id `F-07`, severity `minor`, category `other`
- **claim**: keep base S-6 claim.
- **evidence**: `plan:159`, `plan:168`, `tests/core/test_how_we_work_routing_table.py:290-310`, `tests/core/test_how_we_work_routing_table.py:341-346`
- **recommendation**: keep base S-6 recommendation verbatim.
- **source_cards**: `[reviewer-3, reviewer-1]`
- **debate_ruling**: "C-005: minor, unanimous, winner V3, 85%; Task 10's tests/core run (plan:168) would catch a violation."
- **Risk**: Low

### Change 9: F-08 (minor): Task 2 no-token check does not force the variable unset (V1 A-4 part, split)
- **Target**: `findings[7]`, id `F-08`, severity `minor`, category `unexecutable`
- **claim**: "Task 2's no-token check says 'With CLICKUP_API_TOKEN unset' but runs a plain command, and the tests are not required to clear the environment. In a shell that exports a token, the check would not print no_token."
- **evidence**: `plan:49`, `plan:44`
- **recommendation**: "Covered by F-02 recommendation (2): `env -u CLICKUP_API_TOKEN -u CLICKUP_WORKSPACE_ID` at plan:49 and `monkeypatch.delenv` in the tests."
- **source_cards**: `[reviewer-1]`
- **debate_ruling**: "U-001: keep, minor, unanimous, 90%. The invariant probe (INV-003, HIGH) showed that F-02's fix makes an exported token the default path, so the fix is required as part of F-02."
- **Risk**: Low

### Change 10: F-09 (minor): never-pass-model rule missing from four of the five refs (V2 Q-4, relabelled; INV-006)
- **Target**: `findings[8]`, id `F-09`, severity `minor`, category `missing-requirement`
- **claim**: "The spec requires the spawn rule ('never pass the model parameter') in SKILL.md and every ref. The plan puts it only in SKILL.md and refs/tiers.md, not in claim.md, create.md, chains.md or labels.md, and the Task 7 test checks two files. The risk is contained because SKILL.md carries the rule."
- **evidence**: `source.md:132`, `source.md:354-358`, `plan:91-95`, `plan:103`, `plan:109`, `plan:121`
- **recommendation**: "Task 5: add the spawn-rule sentence to all five refs. Task 7: iterate the phrase check over refs/*.md."
- **source_cards**: `[reviewer-2]`
- **debate_ruling**: "U-003: keep, minor, unanimous, 90%; relabelled from weak-match to missing-requirement. INV-006 widened the fix from two refs to all five."
- **Risk**: Low

### Change 11: F-10 (minor): Task 14 needs a session restart and names no checkable evidence source (base S-2, kept)
- evidence `plan:209`, `plan:212`; keep base claim/recommendation; source_cards `[reviewer-3]`; debate_ruling "U-005: keep, minor, unanimous, 90%. V2 Round 2 noted it makes the F-01 halt branch the likely path."

### Change 12: F-11 (minor): chains.md flag test reads the installed copy first (base S-4, relabelled)
- **Target**: category changed from `false-claim` to `spec-inherited`
- **claim**: "Task 7 makes the chains.md flag test read ~/.claude/commands/sc/<name>.md first, as source.md:391's 'installed-or-source' says. It also calls this the 'same check style' as test_every_notes_flag_exists_in_its_command, but that test reads only src/superclaude/commands. The spec contradicts itself, and the installed read makes the test machine-dependent."
- **evidence**: `plan:121`, `source.md:391`, `tests/core/test_how_we_work_routing_table.py:19`, `tests/core/test_how_we_work_routing_table.py:141-153`
- **recommendation**: keep base S-4 recommendation.
- source_cards `[reviewer-3]`; debate_ruling "U-006: keep, minor, unanimous, 90%; 'false-claim' category rejected because the plan copies the spec."

### Change 13: F-12 (minor): Task 13 greps local master (base S-5, kept)
- evidence `plan:198`; keep base; source_cards `[reviewer-3]`; debate_ruling "U-007: keep, minor, unanimous, 90%; it only mislabels pre-existing hits."

### Change 14: F-13 (minor): Tasks 14/16 act outside the Constraints edit scope; the worktree is never removed (base S-7, kept)
- evidence `plan:20`, `plan:209`, `plan:230`; keep base; source_cards `[reviewer-3]`; debate_ruling "U-008: keep, minor, unanimous, 90%; not destructive."

### Change 15: F-14 (minor): coverage-matrix best-task matches overstate task-level satisfaction (V2 Q-1)
- evidence `.dev/reflect/pre-TASK-WF-scIssueCommand-20261104-064713-20261104070955/artifacts/coverage-matrix.json:8-15`, `plan:24`, `plan:92`; claim and recommendation from V2 Q-1 (no plan change; correct the audit bookkeeping); category `weak-match`; source_cards `[reviewer-2]`; debate_ruling "U-002: keep, minor, unanimous, 90%."

### Change 16: F-15 (minor): Wave 1 merged-PR lookup truncates at gh's default 30 (invariant probe INV-007)
- claim: "The spec's `gh pr list --repo <R> --state merged --search ... --json ...` has no --limit, and gh's default is 30. Task 5 copies the gh commands exactly as written, so for an older issue the accuracy check silently misses later PRs. The label list in create Wave 1 sets --limit 200 explicitly."
- evidence `source.md:149`, `source.md:188`, `plan:91`; recommendation "claim.md adds `--limit 200` (or pages) to the merged-PR query, and the worker records when the result was truncated."; category `spec-inherited`; source_cards `[invariant-probe]`; debate_ruling "INV-007, MEDIUM, UNADDRESSED in the debate; added as minor (robustness, inherited from the spec)."

### Change 17: F-16 (minor): ClickUp page start and invalid CLICKUP_MAX_PAGES are unspecified (INV-008)
- claim: "Neither the plan nor the spec states the first page number for the task-list paging, and the page-cap test does not pin it. Behaviour for a zero, negative or non-integer CLICKUP_MAX_PAGES is undefined; exit 2 covers command-line arguments only."
- evidence `plan:42`, `plan:44`, `source.md:304`; recommendation "State the starting page from the ClickUp v2 reference in the script docstring and pin it in a fixture test; define the outcome for an invalid CLICKUP_MAX_PAGES."; category `missing-requirement`; source_cards `[invariant-probe]`; debate_ruling "INV-008, MEDIUM; minor."

### Change 18: F-17 (minor): bytecode caches can trip the src/superclaude path checks (INV-009)
- claim: "Tasks 1 and 2 load the scripts by path in tests, which can write scripts/__pycache__/*.pyc holding the absolute source path (inferred, not run). The Task 7 'no file contains src/superclaude/' test and the Task 13 `grep -rn` would then match a binary file."
- evidence `plan:121`, `plan:198`, `plan:202`, `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:35`; recommendation "The test skips __pycache__ and binary files; Task 13 uses `grep -rIn`; run checks with PYTHONDONTWRITEBYTECODE=1 as the executor already advises."; category `other`; source_cards `[invariant-probe]`; debate_ruling "INV-009, MEDIUM, inferred; minor. managed-workspace.md:35 already partly mitigates it."

### Change 19: F-18 (minor): the 500-line limit is measured two ways (INV-010)
- evidence `plan:112`, `plan:121`; claim "The AC uses wc -l and the test counts lines in Python; they differ by one for a file with no final newline."; recommendation "Use one counting rule in both, or set the limit at 499 lines."; category `other`; source_cards `[invariant-probe]`; debate_ruling "INV-010, LOW; minor."

### Change 20: rejected_findings
Add these entries (id, reason):
- `Q-5`: "U-004: reviewer-2's own card says no plan change; the omitted matrix regions were spot-checked as covered. Rejected unanimously in Round 2."
- `A-1-as-blocking`: "Reviewer-1's 'items 1-6 have no task ... missing required deliverable' overstated: AC 5 is covered by Task 2 (plan:49) and Task 15 (plan:215-224); section 20 is checks, not deliverables (source.md:465 vs source.md:388-398). Kept as minor F-03."
- `Q-3-calibrated-blocking`: "The calibrator's upgrade of Q-3 to blocking was rejected in debate: no deliverable missing, no false claim, no wrong behaviour, no security risk. Kept as minor F-03."
- `A-2-recommendation-deferred-outcome`: "Reviewer-1's fix of accepting 'not run, deferred' while keeping Task 16 after 14/15 changes the meaning of plan:213/223; replaced by F-01's reorder plus the evidence-AC rewrite."
- `S-4-false-claim-category`: "plan:121 copies source.md:391; the inconsistency is spec-inherited. Kept as minor F-11 with category spec-inherited."
- `A-003-ac7-phrase-test`: "Challenge that a phrase-presence test does not satisfy AC 7's static test: accepted as adequate; source.md:391 defines the static test as phrase presence and plan:121 matches. No finding."
- `calibration-make-test-vs-uv-run-pytest`: "source.md:400 'make test' vs plan:230 'uv run pytest' is no deviation: Makefile:13-15 runs uv run pytest."

### Change 21: unresolved
`unresolved: []`. All 15 diff points reached agreement (debate-transcript.md, Convergence Assessment).

### Change 22: provenance and severity rule
Add `severity_rule` (the caller's text verbatim), plus a YAML comment header: `# Provenance: produced by /sc:adversarial (Mode A, depth standard); Base: Variant 3 (reviewer-3, opus:refactorer); Merge date: <ISO-8601>`. Add one `# Source:` comment line above each finding naming its source change number from this plan (requirement-level provenance).

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| C-001 fix (V1 A-2) | Accept "not run, deferred" as a Task 14/15 outcome, keep order | Changes the meaning of plan:213/223; V1 conceded in Round 1. The base reorder is kept and augmented by INV-002's AC rewrite. |
| X-001 (V2) | verdict PASS | All three advocates agree on FAIL (98%). |
| S-002 (V2 `resolved_model`) | carry per-card model metadata | The merged schema has no per-card metadata; model identity is kept in base-selection.md and the transcript metadata. |
| V1 A-4 bundle | three nits in one finding | Split into F-06, F-07 and F-08 (Structure: separation of concerns). |

### Anchor-level omissions
| Source variant | Anchor type | Anchor | Reason for omission | Debate evidence |
|---|---|---|---|---|
| V1 | recommendation | `./artifacts/t-ac-1-6.md` file name | Replaced by `./artifacts/t-acceptance.md` covering ACs 1-8 | C-002 ruling; V2 Q-3 covered AC 8 |
| V2 | recommendation | `artifacts/t16-manual-acceptance.md` file name | Same replacement | C-002 ruling |
| V1, V2 | self_reported_confidence 0.7 / 0.86 | numeric | Per-card fields with no merged meaning | Change 1 |
| V3 | self_reported_confidence 0.78 | numeric | Same | Change 1 |

## Threshold preservation

| Source | Value | Disposition |
|---|---|---|
| V3 S-1 / F-01 | Task numbers 13, 14, 15, 16 | preserved-exact |
| V1 A-1 / F-03 | section 20 items 1-6 | modified-with-rationale: 1, 2, 3, 4, 6 unrun; 1-8 in the artifact |
| V2 Q-1 / F-14 | five matrix rows INF-013, 054, 058, 059, 062 | preserved-exact |
| V2 Q-3 | ACs 2, 3, 6 | modified-with-rationale: widened to 1, 2, 3, 4, 6 per debate |
| F-15 | `--limit 200`; gh default 30 | preserved-exact |
| F-18 | 500 lines; 499 alternative | preserved-exact |
| F-02 | env vars CLICKUP_API_TOKEN, CLICKUP_WORKSPACE_ID | preserved-exact |
| Change 1 | convergence 1.0, threshold 0.80 | preserved-exact |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Medium | Schema keys missing; caller cannot parse | Re-emit from this plan's key list |
| 2-3 | Medium/Low | Verdict loses its blocking basis | Restore from debate-transcript.md Scoring Matrix C-001, A-001 |
| 4-19 | Low | A minor finding is lost or mis-cited | Restore the entry from this plan |
| 20-22 | Low | Transparency lost | Re-add from this plan |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-04T08:30:00Z

## Citation provenance (every citation above was re-Read in this pipeline)
- Orchestrator Read: plan:1-237 (the whole file); source.md:1-476 (the whole file); sc-implement-protocol SKILL.md:110-149; refs/ledger.md:50-164; refs/qa.md:43-104 and :238-286; refs/managed-workspace.md:29-37; tests/core/test_how_we_work_routing_table.py:10-34, :135-164, :250-354; Makefile:1-20; coverage-matrix.json:1-20.
- Advocates (per transcript "Files and lines re-Read") Read the same plan, source and executor ranges. They did not use any citation outside the orchestrator's set.
