# Reflect report (UC-1 pre-execution): TASK-WF-enforceTheOwnerP-20261108-031809

```yaml
contract_version: 1.8.0
status: needs_human_decision
mode: pre
tier_reached: 2
confidence_calibrated: 0.86
citations_total: 107
citations_revalidated: 107
citations_dropped: 0
citations_inferred: 7
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
needs_human_decision: true
```

`confidence_calibrated` is the mean of the two calibrated Tier 2 cards (0.83, 0.89; reviewer-cards/*-calibration.md); the Tier 1 card calibrated at 0.72 (t1-calibration.md). Evidence gate: evidence-validation.md (107/107 re-read, 0 dropped, 3 partial holds corrected below).

Paths are relative to the repo root `/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test` unless absolute. `plan` = `.dev/tasks/to-do/TASK-WF-enforceTheOwnerP-20261108-031809/TASK-WF-enforceTheOwnerP-20261108-031809.md`; `source.md` = the `source.md` beside it; `orca_worktree.py` = `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`; `SKILL.md` and `refs/claim.md` without a directory = `src/superclaude/skills/sc-issue-protocol/`.

## Summary

- **Verdict:** revise the plan before execution, and record the owner's decision on the `/sc:issue` approach first. Advisory only: this report never edits the plan.
- **best_practice_grade:** 3/5 (Tier 1 card 3/5, t1-card.md; both Tier 2 reviewers 3/5 after the debate, adversarial/debate-transcript.md Round 2; adversarial/merged-verdict.yaml).
- **Coverage:** every source requirement maps to a task or a Constraint. Parsed requirement IDs: 0 (the source is one line with no requirement IDs, source.md:1), so `coverage_pct` is null; union coverage over 34 inferred requirements is 28/34 = 0.8235, and the 6 unmapped rows are Constraints or out-of-scope items the plan states.
- **Findings:** 24 merged (HIGH 4, MEDIUM 14, LOW 6; adversarial/merged-verdict.yaml `findings_by_severity`, full rows in adversarial/merged-output.md §3). The two that would break execution: a crash in Task 3's new warning code (M-2) and an unsafe close on an unknown create reply (R1-4).
- **Decision needed (G-1):** the plan keeps a bare create → copy → `agent launch` for `/sc:issue` and closes Orca's plain tab, while the source says "keep `agent launch` only for an already existing worktree". No artifact records the owner approving that departure.
- **Tier 2 route:** forced by `coverage_degraded: parsed-sparse` (no Tier 1 stop allowed) and rule 4 (4 domains). Reviewers sonnet/analyzer and haiku/qa; calibrator and judge opus (same class as the plan's author, so diversity is degraded). Merge: `sc-adversarial-protocol`, alignment 30/31, status BLOCKED_BY_INVARIANTS (INV-001, now finding M-2). Sources: artifacts/tier_decision.yaml, audit.log Wave 0 step 0.5b, adversarial/debate-transcript.md Convergence Assessment, adversarial/invariant-probe.md.

## Coverage

| Source item | Plan coverage |
|---|---|
| (1) Hook blocking a bare `orca worktree create`, sibling of `block-bare-python.sh` | Task 1 (plan :29-36); gaps R1-1, R1-2, M-6 |
| (1) Register in both `hooks.json` files; enumerating tests | Task 2 (plan :38-47); gap R1-13 |
| (2) `/sc:issue`: agent comes with the create | Departs from the source (plan :20); see G-1 |
| (2) Pending record before the agent starts | Kept (plan :20); existing order `orca_worktree.py:941` then `:954` |
| (2) D2 and FO-18 updated | Kept unchanged with dated notes (plan :75); part of G-1 |
| (3) `CLAUDE.md` worktree rule and bare example | Task 6 (plan :84-92); gap R1-7 |
| (3) `core/CLAUDE.md` and `ccsession-tag/README.md`, 12 pins kept | Task 7 (plan :94-103) |
| Out of scope (WC-13, `worker-start`, Orca changes, existing tabs) | Constraints (plan :22) |
| Respect list (Orca-only, no link flags, no `src/superclaude/` in installed text, sync-dev/verify-sync) | Constraints (plan :23); Task 7 |
| Added by the plan: `--pipeline none` creates no worktree | Tasks 4-5; Authorized expansion (D-001) |

## Inferred requirements (Pass 2)

All 34 rows cite `source.md:1` (the source is a single line). Match = Step 1B.0 containment ≥ 0.6 against a task body; "constraint" = covered by a plan Constraint, not a task; "departure" = matched by word overlap but the task does something different (see G-1).

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | every Orca worktree gets an agent | source.md:1 | matched (Tasks 6, 7) |
| INF-002 | no session creates a worktree for its own use | source.md:1 | matched (Tasks 6, 7) |
| INF-003 | a session that creates a worktree becomes its orchestrator (or coordinator under another orchestrator) and owns that worktree's agent(s) | source.md:1 | matched (Task 6) |
| INF-004 | Instruction-only fixes were rejected because compliance is unproven; enforcement must be deterministic. | source.md:1 | constraint |
| INF-005 | (1) a new PreToolUse(Bash) hook, a sibling of src/superclaude/hooks/scripts/block-bare-python.sh | source.md:1 | matched (Task 1) |
| INF-006 | same decision contract: allow exit 0, block = one stderr message + exit 2, fail open | source.md:1 | matched (Task 1) |
| INF-007 | blocks a Bash command running `orca worktree create` without `--agent` | source.md:1 | matched (Task 1) |
| INF-008 | allow `--help` | source.md:1 | matched (Task 1) |
| INF-009 | prints the exact form `orca worktree create --name <name> --agent claude --prompt "<task>" ...` | source.md:1 | matched (Task 1) |
| INF-010 | register it in src/superclaude/hooks/hooks.json | source.md:1 | matched (Task 2) |
| INF-011 | and the plugins/superclaude/hooks mirror | source.md:1 | matched (Task 2) |
| INF-012 | tests modelled on tests/hooks/test_block_bare_python.py | source.md:1 | matched (Task 1) |
| INF-013 | plus tests/cli/test_install_hooks.py and tests/unit/test_cli_install.py if they enumerate hooks | source.md:1 | matched (Task 2) |
| INF-014 | src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py creates the worktree bare and then runs `orca agent launch`, which by the same Orca rule leaves a plain tab; change new-worktree creation so the agent comes with the create | source.md:1 | departure (Task 3; G-1) |
| INF-015 | keep `agent launch` only for an already existing worktree | source.md:1 | departure (Task 4 word overlap; G-1) |
| INF-016 | keeping the launch-level pending record written before the agent starts | source.md:1 | matched (plan :20) |
| INF-017 | update docs/designs/sc-issue-claim-pipeline-flag.md design default D2 | source.md:1 | departure (Task 5 keeps D2; G-1) |
| INF-018 | and forbidden-flag FO-18 | source.md:1 | departure (Task 5 keeps FO-18; G-1) |
| INF-019 | the pinned tests in tests/skills/test_issue_orca_worktree.py | source.md:1 | matched (Task 3) |
| INF-020 | and tests/skills/test_issue_protocol.py accordingly | source.md:1 | matched (Tasks 3, 4) |
| INF-021 | CLAUDE.md:307-324 worktree rule and its bare example at :320 (the hook would block it) to require --agent | source.md:1 | matched (Task 6) |
| INF-022 | and state the ownership rule | source.md:1 | matched (Task 6) |
| INF-023 | src/superclaude/core/CLAUDE.md "Orca session launches" (45-53) | source.md:1 | matched (Task 7) |
| INF-024 | its copy src/superclaude/skills/ccsession-tag/README.md (228-237): add the rule | source.md:1 | matched (Task 7) |
| INF-025 | while keeping the 12 phrases pinned by tests/core/test_orca_session_launch_guidance.py | source.md:1 | matched (Task 7) |
| INF-026 | Out of scope: supervised workers | source.md:1 | constraint |
| INF-027 | WC-13 in src/superclaude/core/WORKER-CONTRACT.md is the subject of a separate sub-orchestrator/coordinator issue — do not change the worker contract here | source.md:1 | constraint |
| INF-028 | changing Orca itself | source.md:1 | constraint |
| INF-029 | closing existing empty tabs | source.md:1 | constraint |
| INF-030 | Respect: Orca-only worktree creation | source.md:1 | constraint |
| INF-031 | no Orca link flags for this repo | source.md:1 | matched (Task 3) |
| INF-032 | never hardcode src/superclaude/ paths inside installed primitives | source.md:1 | matched (Task 7) |
| INF-033 | make sync-dev | source.md:1 | matched (Task 7) |
| INF-034 | make verify-sync after edits | source.md:1 | matched (Task 7) |

Recompute (Wave 5): the evidence validator found all 34 quotes exact substrings of source.md; no row dropped, so `coverage_pct_union` stays 0.8235, `unmapped_requirements_union` stays [INF-004, INF-026, INF-027, INF-028, INF-029, INF-030], and `S_dev_density` stays 6/34 = 0.1765.

## Deviations

### Deviation D-001: `--pipeline none` creates no worktree

- **Location:** plan:19
- **Mapped tasklist item:** Tasks 4, 5
- **Spec section:** n/a (source is silent on `none`)
- **Evidence:** "`/sc:issue --pipeline none` now creates no worktree" (plan:19)
- **Classification:** authorized
- **Classification rationale:** Recorded in plan Constraints as an owner decision of 2026-11-08; without it, `none` would create an agentless worktree, which the source's first rule forbids. Owner record not verifiable from files.
- **Default remediation:** None; keep the Orca prerequisite for `none` and say so (C-011).

### Deviation D-002: Human-created worktree rule and creator-owns rule in instruction text

- **Location:** plan:19
- **Mapped tasklist item:** Tasks 6, 7
- **Spec section:** n/a
- **Evidence:** "a human-created worktree also needs an agent" (plan:19)
- **Classification:** authorized
- **Classification rationale:** Owner decision recorded in plan Constraints; instruction-only, not hook-enforced (R1-11).
- **Default remediation:** None.

### Deviation D-003: Task 2 checks the `launch-job-identity.sh` interaction

- **Location:** plan:42
- **Mapped tasklist item:** Task 2
- **Spec section:** n/a
- **Evidence:** "Check whether `launch-job-identity.sh` ... changes what the new hook sees" (plan:42)
- **Classification:** authorized
- **Classification rationale:** [INFERRED] Serves the source's "enforcement must be deterministic" (source.md:1).
- **Default remediation:** None (but see R-007 on its acceptance).

### Deviation D-004: Delivery steps file

- **Location:** plan:111
- **Mapped tasklist item:** Task 8
- **Spec section:** n/a
- **Evidence:** "Write `./artifacts/t8-delivery.md` with the operator steps" (plan:111)
- **Classification:** authorized
- **Classification rationale:** [INFERRED] Packaging; no scope change.
- **Default remediation:** None.

The `/sc:issue` departure (plan :20, :53, :75) is not classified here; it is Grounding Gap G-1. Neither Necessary, Drift nor Regression is assigned to it.

## Grounding Gaps

### Gap G-1

- **Hunk ref:** plan:20, :53, :75 (Tasks 3 and 5)
- **Evidence missing:** a recorded owner approval of the plan :20 departure. The plan says only "Deviation from the source, stated to the owner before planning" (plan:20).
- **Why not classifiable:** it is a Necessary deviation if the owner approved it or it is truly forced: `finish()` fails the claim on a copy error (orca_worktree.py:521-524) and `cmd_launch` refuses a stale prompt (orca_worktree.py:934-936), so an agent started by `create --agent` would run before those checks. It is a Regression under the reflect precedence rule if it contradicts the source's explicit restriction "keep `agent launch` only for an already existing worktree" (source.md:1) without approval. Both reviewers withdrew their labels (adversarial/debate-transcript.md Round 2: V1 response 1, V2 item 1). [INFERRED] Alternatives (publishing the pending nonce before the create, `publish_pending` takes no worktree at orca_worktree.py:728; an absolute-path prompt) are untested (adversarial/diff-analysis.md A-005).
- **Next evidence needed:** the owner's answer to: is the bare create → copy → `agent launch` plus first-tab close replacement approved, with D2 and FO-18 kept?

## Inferred-claim audit

- `citations_inferred: 7`
- Inferred-fraction: `7 / 107` = 0.07

## Recommendations

### Recommendation R-001: Answer G-1 and record the answer in plan Constraints

- **File:** plan (Constraints, line 20)
- **Change:** Record whether the `/sc:issue` departure is approved. If yes, Tasks 3 and 5 run as amended below. If no, Tasks 3 and 5 need a redesign that keeps "failed copy = no agent".
- **Verifier:** plan :20 states the owner's decision with a date.
- **Linked deviation(s):** G-1 (finding M-10)
- **Priority:** P0

### Recommendation R-002: Add `W-FIRST-TAB-LEFT` to `WARNING_ORDER` (M-2)

- **File:** src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
- **Change:** Task 3 must add the new code to `WARNING_ORDER` (orca_worktree.py:198-206) at a stated rank and to the warning list in SKILL.md:149. `Outcome.as_dict` picks the warning with `min(..., key=WARNING_ORDER.index)` (orca_worktree.py:232-235), which raises `ValueError` for an unlisted code, so a created worktree carrying the new note prints no JSON.
- **Verifier:** tests in tests/skills/test_issue_orca_worktree.py where `W-FIRST-TAB-LEFT` is the only note, and where it appears with `W-WORKTREE-COPY-FAILED` (orca_worktree.py:526).
- **Linked deviation(s):** none (invariant INV-001)
- **Priority:** P0

### Recommendation R-003: Never close on an unknown create reply (R1-4)

- **File:** src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py; tests/skills/test_issue_orca_worktree.py
- **Change:** Task 3 reads `result.setup` and `result.defaultTabs` from the create reply; a missing, unparseable or timed-out reply means no close plus `W-FIRST-TAB-LEFT`. Today the code continues after a timed-out create (orca_worktree.py:611) and never parses the reply. Plan :53 says "Otherwise run `orca terminal list`", which lets an unknown reply reach the close. Add a valid-reply fixture: `created_scene()` returns "opaque, not json" (tests/skills/test_issue_orca_worktree.py:376), so plan :57's five-call sequence cannot pass with it; FO-11's `warning is None` (tests/skills/test_issue_orca_worktree.py:559) changes for the opaque case.
- **Verifier:** opaque-reply and timed-out tests record no `terminal close` call; the valid-reply test records the five calls of plan :57.
- **Linked deviation(s):** none
- **Priority:** P0

### Recommendation R-004: Make the hook scanner track each command's own words (R1-1)

- **File:** src/superclaude/hooks/scripts/require-orca-worktree-agent.sh (new); tests/hooks/test_require_orca_worktree_agent.py (new)
- **Change:** The sibling scanner ignores a command's later words once its command word is set (`need[o] = 0` at block-bare-python.sh:132, then `if (!need[o]) return` at block-bare-python.sh:106) and exits on the first match (block-bare-python.sh:132-134), so it cannot be reused unchanged. Task 1 must collect each command's arguments, reset at separators, and add tests for `orca … ; orca worktree create --agent x` in both orders, `env X=1 orca`, `sudo orca`, `command orca`, a create after `|`, a heredoc into a shell, backticks, and an inner bare create inside an outer `--agent` command. The plan's 12 cases (plan :34) contain none of these.
- **Verifier:** `uv run pytest tests/hooks/test_require_orca_worktree_agent.py -v` with the added cases.
- **Linked deviation(s):** none
- **Priority:** P0

### Recommendation R-005: Check repository identity before any close, only for `created` (M-1)

- **File:** src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
- **Change:** The git-common-dir check sits inside `finish()` (orca_worktree.py:507-513), after the plan's proposed close point. Close only after that check, and gate it on status `created`, because `finish()` also serves the reused path (orca_worktree.py:575). Decide close-before-copy vs close-after-copy: closing first leaves no tab and no agent when the copy fails (orca_worktree.py:521-524) (M-4).
- **Verifier:** a fixture whose new row points at another repository gives failed/stale with zero `terminal close` calls; a reused run records no close.
- **Linked deviation(s):** none
- **Priority:** P1

### Recommendation R-006: Complete the `--pipeline none` edit list (R1-6, M-9)

- **File:** src/superclaude/skills/sc-issue-protocol/SKILL.md; src/superclaude/skills/sc-issue-protocol/refs/claim.md; docs/user-guide/commands.md; src/superclaude/core/HOW-WE-WORK.md
- **Change:** Add to Task 4/5: SKILL.md:17 and :170 ("create or reuse the Orca worktree"), SKILL.md:90-91 (Wave 6 says "continue with Wave 7 and Wave 8" and Wave 7 has no `none` exclusion; the phrase "Runs for every `--pipeline` value" is at refs/claim.md:97), the return-contract block SKILL.md:121-134 (four worktree fields null for `none`, the ten keys kept), refs/claim.md:93 and :131-136; the user guide docs/user-guide/commands.md:367, :379, :394; the routing row src/superclaude/core/HOW-WE-WORK.md:329 and [INFERRED] its plugin mirror (path not read). Do not edit SKILL.md:89, :92 or :150, which already handle `none`.
- **Verifier:** grep for "create or reuse the Orca worktree" and "Open <wt>" returns no `none` path; a pin that the `none` Final output has no worktree line.
- **Linked deviation(s):** D-001
- **Priority:** P1

### Recommendation R-007: Make the hook-interaction check an executable test (R1-13)

- **File:** tests/hooks/ (new test)
- **Change:** Plan :47 allows "the reason none is needed". `launch-job-identity.sh` replaces the whole input through `updatedInput` (src/superclaude/hooks/scripts/launch-job-identity.sh:14-15). Require a test that feeds a governed-session event with a bare create and expects exit 2; record live hook ordering as unverified.
- **Verifier:** the new test passes.
- **Linked deviation(s):** D-003
- **Priority:** P1

### Recommendation R-008: Fix the contradicting `CLAUDE.md` lines and pin ownership (R1-7)

- **File:** CLAUDE.md; tests/core/
- **Change:** Task 6 must also change CLAUDE.md:305 ("give each session its own worktree") and the Usage block at CLAUDE.md:333-337, which contradict "no session creates a worktree for its own use". Tasks 6 and 7 tests must assert the creator-owns and orchestrator/coordinator wording, not just the agent phrases (plan :88, :98).
- **Verifier:** `uv run pytest tests/core/ -v` with the new assertions.
- **Linked deviation(s):** D-002
- **Priority:** P1

### Recommendation R-009: State the failure paths that leave a plain or empty worktree (R1-8, M-3, M-8)

- **File:** plan (Constraints; Task 3); src/superclaude/skills/sc-issue-protocol/refs/claim.md
- **Change:** Name and accept: a failed launch (orca_worktree.py:954-975) leaves a worktree with no agent, and with the plan's close step also no tab; list failure, AMBIGUOUS, not-listed and not-on-disk paths after a create (orca_worktree.py:614-630) keep the plain tab; [INFERRED] a re-run reuses (orca_worktree.py:575) and, by the plan's "not `reused`" gate, does not close. Each reports `W-FIRST-TAB-LEFT`, and the `/sc:issue` Final output prints `worktree_warning` so an unattended run surfaces it.
- **Verifier:** tests for each path record the warning; a pin that Final output prints the warning.
- **Linked deviation(s):** G-1
- **Priority:** P1

### Recommendation R-010: Pin the hook's matching rule, fail-open branches and message (R1-2)

- **File:** tests/hooks/test_require_orca_worktree_agent.py (new)
- **Change:** `worktree` and `create` are the first two non-option arguments after `orca`; `orca worktree list --name create` is allowed; tests for missing `jq`, missing `awk`, scanner error, empty stdin and `-h`; assert the full message (command form, ownership sentence, `worker-start` sentence) on one stderr line set. [INFERRED] Record `--prompt "--agent"` as a known hole (a quoted value equal to the flag would satisfy a word match).
- **Verifier:** the hook test file passes with these cases.
- **Linked deviation(s):** none
- **Priority:** P1

### Recommendation R-011: List what the hook does not cover (M-5, M-6, M-7, R1-12)

- **File:** src/superclaude/hooks/scripts/require-orca-worktree-agent.sh (header); ./artifacts/t8-delivery.md
- **Change:** Header "Known ceilings" like block-bare-python.sh:48-61: `bash -c`, `sh -c`, `eval`, `ssh host '…'`, a heredoc piped to a shell, `xargs`, `claude --bare` (block-bare-python.sh:61), and [INFERRED] humans, other agent tools, and scripts that call Orca (including `orca_worktree.py`, which calls Orca as a subprocess, not through the Bash tool). Add to Task 8 a live check that `--agent` with `--activate` or hooks does not seed a plain tab (unverified, M-5).
- **Verifier:** header and delivery file contain the list.
- **Linked deviation(s):** none
- **Priority:** P1

### Recommendation R-012: Small text fixes (R1-5, R1-9, R1-10, R1-11)

- **File:** src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py; src/superclaude/core/CLAUDE.md; src/superclaude/skills/ccsession-tag/README.md; plan
- **Change:** close with `--tab` and treat `agentIdentity` as absent or empty (/home/coder/workspaces/IronOrca/src/cli/help.ts:88-89; /home/coder/workspaces/IronOrca/src/shared/runtime-terminal-contracts.ts:38-39); update the module docstring (orca_worktree.py:20-30) for the new `terminal` calls; qualify the new paragraph for supervised workers (src/superclaude/core/WORKER-CONTRACT.md:62); say in Constraints that only the `--agent` half is enforced.
- **Verifier:** re-read the changed lines.
- **Linked deviation(s):** none
- **Priority:** P2
