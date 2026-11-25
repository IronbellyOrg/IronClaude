# Diff Analysis: authority-model position papers Comparison

Variant A = `variant-1-original.md` (OURS, the owner's line). Variant B = `variant-2-original.md` (CLAY). Taxonomy tags: L1 surface, L2 structural, L3 state-mechanics.

## Metadata
- Generated: 2026-11-20 (UTC)
- Variants compared: 2
- Total differences found: 23 debate points (S 3, C 10, X 5, A 5) plus 10 unique contributions
- Categories: structural (3), content (10), contradictions (5), unique (10), shared assumptions (5)

## Structural Differences

| # | Area | Variant A (OURS) | Variant B (CLAY) | Severity |
|---|------|------------------|------------------|----------|
| S-001 | Document layout [L1] | Claim, mechanism (5 items), 9 cited facts, costs, risks, "gets right" | Same layout; mechanism 5 items, 9 cited facts | Low |
| S-002 | Evidence base [L2] | Owner decision records (APPROVED.md, D3/D5 recommendations), master contract lines, owner's local unpushed requirements rows | Almost only lines of the merged design doc (D:nnn) plus two code files (`reviewers.py`, `repos.py`) | Medium |
| S-003 | Nature of the candid weakness [L2] | Costs and risks are about human bottleneck and prose-only enforcement | Costs and risks are about unbuilt machinery, unprotected master, self-declared answer source | Low |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Who may merge [L3] | Person's named go for every merge (WORKER-CONTRACT:108, :241) | Orchestrator merges when a 13-reason gate passes; human only for failing check, merge-safety file, changes_requested (D:586-593) | High |
| C-002 | Script-started coordinator [L2] | Allowed when the owner recorded a standing authorization in the launch prompt (R9, R17); "person opened" is the rule | Allowed: terminal + `ccsession`, depth 0, not `worker-start` (D:112) | Medium |
| C-003 | Who runs `/sc:pr-submit` [L2] | Never an Orca worker (D3); ordinary session per PR; Full Submit launch (R25) is the automated route | A `worker-start` worker with brief line `Flow: orchestrated-issue` runs it, never merges (ADD1, D:135) | High |
| C-004 | Silent reviewer [L3] | Skipped, recorded absent, ignored for the rest of the run (SKILL.md:29-32) | Merge hold after 60 min, then row 9 escalation; `reviewers` list per repo (ADD4, D:138) | Medium |
| C-005 | How a human answer is recognized [L3] | Chat message, prose rules (D2, 2026-11-17 order) | `answer-check` with source, entry id, freshness, question key bound to PR and head sha (D:694) | Medium |
| C-006 | When the human is reached [L2] | At every outward action, at the moment of action | Closed nine-row list; everything else decided and recorded; unanswered question waits (D:664-696) | High |
| C-007 | Grant scope [L2] | Per-issue go (R25 Full Submit; per-issue grant row) | Repo-level standing `grants` list in repos.yaml (DQ6) | Medium |
| C-008 | Unguarded workers on an unprotected master [L3] | A reason to keep outward actions out of workers | Accepted risk K12, mitigated by prompt, merge-by-orchestrator rule and live test | High |
| C-009 | Implementation status [L2] | Rules live on master as contract prose; no hook enforces them | Design merged; merge-gate and answer-check not in master, PR 686 or branch issue-655-pr-p | Medium |
| C-010 | Source of authority [L2] | Owner decisions D3, D4, D5, GIT of 2026-11-02 | Clay's rulings 3, 4, 5, 6 of 2026-11-19, approved by Clay | Medium |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | What D5's "person opened" protects [L3] | Partly the depth rule: a `worker-start` coordinator is depth 1 (D5 rec:9); so the rule has a technical reason | That depth reason only covers `worker-start` starts; a terminal + ccsession start is depth 0 (D:112, U3 at D:1261) | Medium |
| X-002 | Is the ADD1 flow a conflict with D3/D4? [L2] | Yes: reverses D3, D4, D5 and contract lines 23, 244-245 | The design names the conflict and decides it with one new contract section (D:135, OD1) | Medium |
| X-003 | Is the pr-submit skip rule defective? [L3] | A skipped reviewer can be late; A has no merge-time check (A concedes it) | The skip is sticky for the run and loses late reviews; a merge-time check on the final head fixes it | Low |
| X-004 | Is the typed answer mechanically checkable? [L3] | Prose only; no hook binds the coordinator | `answer-check` makes four results checkable (B fact 5); yet B's own risk says the verb cannot tell person from script (D:694) | Medium |
| X-005 | Is the owner's R25 a rule in force? [L3] | R25 is "the person's go for that issue's push and PR" (A fact 7) | n/a for B; but master contract :245 says "no earlier pre-authorization waives this", and R25 sits in an unpushed local plan (A's own text) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | D5's technical depth reason (a `worker-start` coordinator cannot start workers) | High |
| U-002 | A | D3: worker per PR deferred; AC-4.3 live check never run; pr-submit has no unattended mode | Medium |
| U-003 | A | R25 and R9/R17: an owner-recorded, per-issue or standing authorization is the way to automate push, PR and coordinator start | High |
| U-004 | A | Chat-approval order and D2: only the person gives a Ruling; relayed approval never counts | High |
| U-005 | B | merge-gate verb: 13 closed reasons, head-pinned `gh pr merge`, no `--auto/--admin/--delete-branch`, fail-closed file list, restart reads PR state first | High |
| U-006 | B | answer-check: answer bound to one question key and one head sha, newer than the notice, never a relayed answer | High |
| U-007 | B | Nine-row "what reaches the human" table and "an unanswered question waits, no default" | Medium |
| U-008 | B | Per-repo `reviewers` list (and `none`) plus per-repo `merge_method` and `release_merge_method` | Medium |
| U-009 | B | Code fact: `merge_wait` separates absent from incomplete; `no_response` only when all reviewers are absent | Medium |
| U-010 | B | `merge_safety_files` hold: changes to CI, CODEOWNERS, hooks wait for an explicit OK even when green | High |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | Both treat "skip a silent reviewer" and "hold a PR for a silent reviewer" as one rule to pick | The PR-fix loop (what to wait for while fixing) and the merge decision (what must be true to merge) are separable layers | UNSTATED | Yes |
| A-002 | Both rest on a person who answers | A person is reachable within a useful time for a go, an OK or an answer | UNSTATED | Yes |
| A-003 | Both rely on "the person's go" | The system can tell a person's typed go from text typed or relayed by an agent (A: prose, B: v1 guard) | STATED (B) | Yes |
| A-004 | Both take `master` as unprotected (D:118) | A GitHub-side control (branch protection, ruleset, merge queue, required review) is not part of the choice; only a repo admin can add one | UNSTATED | Yes |
| A-005 | Both name Augment and Codex as the reviewers | The reviewer set per repo is stable enough to list (B marks the lists UNVERIFIED at D:138) | STATED (B) | Yes |

Promoted assumptions are extra debate points (A-001 to A-005). Taxonomy level of the A-points: A-001 L2, A-002 L2, A-003 L3 (guard), A-004 L3 (guard), A-005 L2.

## Summary
- Total structural differences: 3
- Total content differences: 10
- Total contradictions: 5
- Total unique contributions: 10
- Total shared assumptions surfaced: 5 (UNSTATED: 3, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, C-003, C-006, C-008; unique U-001, U-003, U-004, U-005, U-006, U-010
- Debate points for convergence: 23 (S 3 + C 10 + X 5 + A 5)
